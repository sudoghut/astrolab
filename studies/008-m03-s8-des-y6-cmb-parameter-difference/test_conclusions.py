"""Assertions that this study's results are complete and internally consistent, read from results/.

Run the study first: python -m astrolab run 008-m03-s8-des-y6-cmb-parameter-difference
"""
import json
from pathlib import Path

import pytest

RESULTS = Path(__file__).parent / "results"


def load(name):
    path = RESULTS / f"{name}.json"
    if not path.exists():
        pytest.skip(f"{path.name} missing; run the study first")
    return json.loads(path.read_text(encoding="utf-8"))


def test_r1_verdict_rule():
    r1 = load("r1")
    for key in ("cmb", "des_3x2pt"):
        v = r1[key]
        if "mean" not in v:
            continue
        pub = v["published"]
        mean_ok = abs(v["mean"] - pub[0]) <= 0.002
        ends_ok = abs(v["hi"] - (pub[0] + pub[1])) <= 0.003 and abs(v["lo"] - (pub[0] - pub[2])) <= 0.003
        assert v["verdict"] == ("reproduced" if mean_ok and ends_ok else "not reproduced")


def test_r2_verdict_rule():
    r1, r2 = load("r1"), load("r2")
    gate = r1["cmb"].get("mean_ok") and r1["des_3x2pt"].get("mean_ok")
    for tag in ("1d", "2d"):
        if tag not in r2:
            continue
        v = r2[tag]
        ok = abs(v["n_sigma"] - v["published"]) <= 0.15 + 2 * v["s"]
        if not gate or not v.get("finite", True):
            assert v["verdict"].startswith("not evaluable")
        elif v["s"] > 0.03:
            assert v["verdict"] == "not evaluable (s > s_max)"
        elif r2["support"].get("fails"):
            assert v["verdict"].startswith("not evaluable (prior support)")
        else:
            assert v["verdict"] == ("reproduced" if ok else "not reproduced")


def test_result_files_small():
    for path in RESULTS.glob("*.json"):
        assert path.stat().st_size < 1024 ** 2, path.name


def test_r6_verdict_rule():
    """README 2.6: re-derive R6 from the saved numbers (independently of r6flow.verdict)."""
    import math

    r6 = load("r6")
    if "verdict" not in r6:
        pytest.skip(r6.get("status", "R6 not run"))
    assert "not run" in r6["flow_1d"]["status"]         # amendment 2026-11-18: no 1-D flow
    assert "flow_1d" not in (r6.get("flows") or {}).get("cases", {}) and "flow_1d" not in (r6.get("flows") or {})
    res = r6["flows"]
    if not load("r2")["gate_r1_means"]:             # README 2.6 order (1)
        assert r6["verdict"] == "not evaluable" and "R1" in r6["reason"]
        return
    if "status" in res:
        assert r6["verdict"] == "not evaluable" and r6["reason"] == res["status"]
        return
    gate = res["gate"]
    exact = gate["exact"]["n_sigma"]
    vals = [r.get("n_sigma") for r in gate["repetitions"]]
    passed = all(v is not None and math.isfinite(v) and r.get("converged") and not r.get("lower_bound")
                 for v, r in zip(vals, gate["repetitions"])) and \
        abs(sum(vals) / len(vals) - exact) <= 0.10 and all(abs(v - exact) <= 0.20 for v in vals)
    assert gate["passed"] == passed
    if not passed:
        assert r6["verdict"] == "not evaluable"
        return
    reps = res["main"]["repetitions"]
    assert [r["seed"] for r in reps] == [0, 1, 2, 3, 4]
    ns = [r.get("n_sigma") for r in reps]
    if any(v is None or not math.isfinite(v) for v in ns) or not all(r["converged"] for r in reps):
        assert r6["verdict"] == "not evaluable"
        return
    if r6["support"]["fails"]:
        assert r6["verdict"] == "descriptive (prior support)"
        return
    if any(r["lower_bound"] for r in reps):
        low = min(r["n_sigma"] for r in reps if r["lower_bound"])
        assert r6["verdict"] == ("not reproduced" if low > 1.8 + 0.15 + 0.10 else "not evaluable")
        return
    n_bar = sum(ns) / len(ns)
    s = math.sqrt(sum((v - n_bar) ** 2 for v in ns) / (len(ns) - 1))
    assert abs(n_bar - res["main"]["n_bar"]) < 1e-9 and abs(s - res["main"]["s"]) < 1e-9
    if s > 0.07:
        expected = "not evaluable"
    else:
        expected = "reproduced" if abs(n_bar - 1.8) <= 0.15 + 2 * s else "not reproduced"
    assert r6["verdict"] == expected


def _r6_reusable(r6):
    """README 2.7 reuse checks, re-implemented here independently of r6nomnu.check_r6."""
    import math

    f = r6.get("flows") or {}
    main = f.get("main") or {}
    reps = main.get("repetitions") or []
    return (f.get("complete") is True and (f.get("gate") or {}).get("passed") is True
            and [r.get("seed") for r in reps] == [0, 1, 2, 3, 4]
            and all(isinstance(r.get("n_sigma"), float) and math.isfinite(r["n_sigma"]) for r in reps)
            and isinstance(main.get("n_bar"), float) and round(main["n_bar"], 4) == 1.6985
            and isinstance(main.get("s"), float) and round(main["s"], 4) == 0.0977)


def _sd(v):
    import math
    m = sum(v) / len(v)
    return math.sqrt(sum((x - m) ** 2 for x in v) / (len(v) - 1))


def test_r6_nomnu_label_rule():
    """README 2.7: re-derive the R6-NOMNU label and the pop_size statements from the saved numbers."""
    import math

    out = load("r6_nomnu")
    r6 = load("r6")
    flows = out["flows"]
    if not _r6_reusable(r6):
        assert out["label"] == "not evaluable" and "not run" in flows["status"]
        return
    six = r6["flows"]["main"]["parameters"]
    assert out["r6_reused"]["ok"] is True and out["summary"]["r6_reused"]["ok"] is True
    if out["parameters"] != six:                                    # pairing with R6 impossible
        assert out["label"] == "not evaluable" and "parameter set differs" in flows["status"]
        return
    assert out["parameters_match_r6"] is True
    if not load("r2")["gate_r1_means"] or "status" in flows:         # rule 1 (R1) or no flows
        assert out["label"] == "not evaluable"
        return
    # rule 1: the 5-D gate (curved pair + three flat boxes), R6's tolerances
    g5 = flows["gate5"]
    gv = [r.get("n_sigma") for r in g5["repetitions"]]
    assert [r["seed"] for r in g5["repetitions"]] == [10, 11, 12]
    assert all(r.get("pop_size_passed") is False and r.get("pop_size") is None
               for r in g5["repetitions"] if "error" not in r)
    passed = all(v is not None and math.isfinite(v) and r.get("converged") and not r.get("lower_bound")
                 for v, r in zip(gv, g5["repetitions"])) and \
        abs(sum(gv) / 3 - g5["exact"]["n_sigma"]) <= 0.10 and all(abs(v - g5["exact"]["n_sigma"]) <= 0.20 for v in gv)
    assert g5["passed"] == passed
    if not passed:
        assert out["label"] == "not evaluable" and "not run" in flows["nomnu"]["status"]
        expected = "not evaluable"
    else:
        case = flows["nomnu"]
        assert case["parameters"] == [c for c in six if c != "mnu"] and len(six) == 6
        assert "mnu" not in case["parameters"]
        reps = case["repetitions"]
        assert [r["seed"] for r in reps] == [0, 1, 2, 3, 4]
        assert all(r.get("pop_size_passed") is False and r.get("pop_size") is None
                   for r in reps if "error" not in r)
        ns = [r.get("n_sigma") for r in reps]
        if any(v is None or not math.isfinite(v) for v in ns) or not all(r.get("converged") for r in reps):
            expected = "not evaluable"                                   # rule 2
        elif any(r.get("lower_bound") for r in reps):                    # rule 3
            expected = ("not mainly Σmν: the other directions carry most of the shift" if min(ns) >= 1.40
                        else "not evaluable")
        else:
            n_bar, s = sum(ns) / 5, _sd(ns)
            assert abs(n_bar - case["n_bar"]) < 1e-9 and abs(s - case["s"]) < 1e-9
            if s > 0.15:                                                 # rule 4
                expected = "not evaluable"
            else:                                                        # rule 5
                lo, hi = n_bar - 2 * s / math.sqrt(5), n_bar + 2 * s / math.sqrt(5)
                if hi <= 1.00:
                    expected = "the full-space shift is mainly the Σmν direction"
                elif lo >= 1.40:
                    expected = "not mainly Σmν: the other directions carry most of the shift"
                elif lo > 1.00 and hi < 1.40:
                    expected = "partly the Σmν direction"
                else:
                    expected = "between the two adjacent labels (not decided)"
                assert out["s5_within_r6_s_max"]["value"] == (s <= 0.07)  # rule 6: a flag only
    assert out["label"] == expected
    assert out["summary"]["label"] == expected

    # pop_size comparison (descriptive): 6-D against R6's recorded repetitions, 5-D against (b)
    if "main_pop1" not in flows:
        return
    assert flows["gate6_pop1"]["exact"]["n_sigma"] == r6["flows"]["gate"]["exact"]["n_sigma"]
    pairs = {"6d": (r6["flows"]["main"]["repetitions"], flows["main_pop1"]["repetitions"])}
    if passed:
        pairs["5d"] = (flows["nomnu"]["repetitions"], flows["nomnu_pop1"]["repetitions"])
    for dim, (r10, r1) in pairs.items():
        cmp = out["pop_size_comparison"][dim]
        assert all(r.get("pop_size") == 1 and r.get("pop_size_passed") is True for r in r1 if "error" not in r)
        ok = all("error" not in r and r.get("n_sigma") is not None and math.isfinite(r["n_sigma"])
                 and not r.get("lower_bound") for r in r10 + r1)
        if not ok:
            assert cmp["status"].startswith("not computed")
            continue
        v10, v1 = [r["n_sigma"] for r in r10], [r["n_sigma"] for r in r1]
        a, b = _sd(v10) ** 2, _sd(v1) ** 2
        big, small = max(a, b), min(a, b)
        differ = small == 0 and big > 0 or (small > 0 and big / small > 6.39)
        assert cmp["spread"] == ("spreads differ" if differ else "no detectable difference in spread with five repetitions")
        m10, m1 = sum(v10) / 5, sum(v1) / 5
        thr = 2 * math.sqrt(b / 5 + a / 5)
        assert cmp["means"] == ("means differ" if abs(m1 - m10) > thr else "means do not differ by the heuristic")
        for r_10, r_1 in zip(r10, r1):
            assert abs(cmp["paired_pop1_minus_default"]["per_seed"][str(r_1["seed"])]
                       - (r_1["n_sigma"] - r_10["n_sigma"])) < 1e-12
