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
    est = r6.get("estimate")               # amendment 2026-11-18: cap only for the reported cases
    if est is not None:
        assert est["by_case"]["main"]["max_iter"] == 1000 and est["by_case"]["s8_for_as"]["max_iter"] == 1000
        assert all(est["by_case"][n]["max_iter"] == 100 for n in ("constrained", "flow_1d", "flow_2d"))
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
