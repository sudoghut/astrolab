"""Assertions that study 012's labels follow from its stored numbers (README section 2).

The decision rules are written out again here, independently of stats012.py / kin012.py / data012.py,
so a slip in either place shows up. Run the study first: python -m astrolab run 012-m12-poor-old-heart
"""
import json
from pathlib import Path

import pytest

RESULTS = Path(__file__).parent / "results"
MISSING = "undetermined (data not in the files)"


def load(name):
    path = RESULTS / f"{name}.json"
    if not path.exists():
        pytest.skip(f"{path.name} missing; run the study first")
    return json.loads(path.read_text(encoding="utf-8"))


def summary():
    s = load("summary")
    if s.get("status") != "complete":
        pytest.skip(f"run not complete: {s.get('status')}")
    return s


def test_files_small():
    if not RESULTS.exists():
        pytest.skip("no results yet")
    for p in RESULTS.glob("*.json"):
        assert p.stat().st_size < 1024 ** 2, p.name


def test_load_checks_passed():
    summary()
    ld = load("load")
    assert ld["L1"]["passed"]
    assert ld["L3_mh"]["duplicated_fraction"] < 0.01 and ld["L3_kin"]["duplicated_fraction"] < 0.01
    assert 2.0 <= ld["L5"]["median_rapo"] <= 15.0


def _agrees(x, kind, v):
    return {"approx": 0.95 * v <= x <= 1.05 * v, "almost100k": 90000 <= x <= 99999, "above": x > v}[kind]


def test_t1():
    summary()
    t1 = load("t1")
    c = t1["counts"]
    for st in t1["statements"].values():
        assert st["ours"] == c[st["count_key"]]
        assert st["count_label"] == ("agrees" if _agrees(st["ours"], st["kind"], st["r22"]) else "disagrees")
        if st["sample"]:
            scaled = st["ours"] / c["total"] * st["sample"]
            assert st["fraction_label"] == ("agrees" if _agrees(scaled, st["kind"], st["r22"]) else "disagrees")
    ab = t1["statements"]["abstract"]
    assert t1["summary"] == ("abstract reproduced" if ab["count_label"] == "agrees" else "not reproduced")


def _t2():
    t2 = load("t2")
    if t2["t2a"]["reproduction_label"] == MISSING:
        pytest.skip("T2 undetermined (data not in the files)")
    return t2


def test_t2a():
    summary()
    a = _t2()["t2a"]
    si, fi = a["fits"]["i"]["sigma"], a["fits"]["i"]["at_bound"]
    want = "not reproduced" if fi else ("reproduced" if 2.4 <= si <= 3.0 else "not reproduced")
    assert a["reproduction_label"] == want
    lo, hi = a["intervals"]["ii"]
    if a["fits"]["ii"]["at_bound"]:
        want = "undetermined (fit at bound)"
    elif abs(a["mock_bias"]["ii"]["bias"]) > 0.1:
        want = "undetermined (method bias)"
    elif a["unmodelled_selection"]:
        want = "undetermined (unmodelled selection)"
    elif lo >= 2.4 and hi <= 3.0:
        want = "consistent with 2.7 kpc"
    elif hi < 2.4 or lo > 3.0:
        want = "different"
    else:
        want = "undetermined"
    assert a["population_label"] == want
    for v in ("i", "ii"):
        assert a["fits"][v]["at_bound"] == (a["fits"][v]["sigma"] - 0.5 < 0.05 or 10.0 - a["fits"][v]["sigma"] < 0.05)


def test_t2b():
    summary()
    t2 = _t2()
    b = t2["t2b"]
    d = b["data"]
    iv = d["profile"]["interval"]
    if d["two_dlnl"] > 10 and iv["hi"] is not None and iv["hi"] < 0.8:
        s1 = "flattened preferred"
    elif d["two_dlnl"] > 10 and iv["lo"] is not None and iv["lo"] > 1.0:
        s1 = "prolate preferred"
    else:
        s1 = "spherical adequate"
    assert d["step1_label"] == s1
    for name, c in b["checks"].items():
        assert c["pass"] == (c["passed_mocks"] >= 0.8 * c["n"])
    fp = all(c["pass"] for n, c in b["checks"].items() if n.startswith("fp"))
    if not (fp and b["checks"]["power"]["pass"]):
        assert b["shape_label"].startswith("undetermined") and b["f5_model"] == "sph"
    elif s1 == "spherical adequate":
        assert b["shape_label"] == s1
    elif s1 == "prolate preferred":
        assert b["shape_label"] == s1 and b["f5_model"] == "flat"
    else:
        assert b["step2"]["reached"]
        if not b["checks"]["step2"]["pass"]:
            assert b["shape_label"] == "flattened (step 2 undetermined)"
        else:
            assert b["shape_label"] == ("power law preferred" if b["step2"]["dbic"] > 10 else
                                        "flattened Gaussian adequate")
    pop = t2["t2a"]["population_label"]
    lo, hi = b["f5_interval"]
    if pop in (MISSING, "undetermined (fit at bound)", "undetermined (method bias)",
               "undetermined (unmodelled selection)"):
        want = pop
    elif lo > 0.5:
        want = "most within 5 kpc confirmed"
    elif hi < 0.5:
        want = "not confirmed"
    else:
        want = "undetermined"
    assert b["f5_label"] == want


def test_t3():
    summary()
    t3 = load("t3")
    if "missing" in t3:
        pytest.skip("T3 data not in the files")
    for key in ("primary", "all_rapo"):
        p = t3[key]
        lo, hi = p["a_interval"]
        want = ("no net rotation" if lo >= -0.05 and hi <= 0.05 else "net rotation" if lo > 0 else
                "net counter-rotation" if hi < 0 else "undetermined")
        assert p["a_label"] == want
        lo, hi = p["b_interval"]
        assert p["b_label"] == ("rotation dominated" if lo > 0.5 else "not rotation dominated" if hi < 0.5
                                else "undetermined")
        w0 = t3["w0"][t3["primary_w0"]]["w0"]
        lo, hi = p["width_interval"]
        if not p["logistic"]["converged"]:
            want = "undetermined (fit failed)"
        elif hi < w0 + 0.1:
            want = "sharp"
        elif lo > max(0.4, w0 + 0.1):
            want = "gradual"
        else:
            want = "undetermined"
        assert p["c_label"] == want
    assert t3["a_label"] == t3["primary"]["a_label"] and t3["b_label"] == t3["primary"]["b_label"]


def test_t5():
    summary()
    t5 = load("t5")
    if "missing" in t5:
        pytest.skip("T5 data not in the files")
    for s in t5["samples"].values():
        lo, hi = s["g_interval"]
        want = ("minor" if hi < 0.10 else "moderate" if lo >= 0.10 and hi <= 0.25 else "major" if lo > 0.25
                else "undetermined")
        assert s["g_label"] == want
        lo, hi = s["a5_interval"]
        assert s["a5_label"] == ("most apocentres below 5 kpc confirmed" if lo > 0.5 else
                                 "not confirmed" if hi < 0.5 else "undetermined")


def test_t4_t6():
    summary()
    t1, t6 = load("t1"), load("t6")
    m = t1["counts"]["lt_m1p5"] * 800 * 2.5
    assert t6["r22_choices_mass"] == pytest.approx(m)
    assert t6["r22_choices_at_least_5e7"] == (m >= 5e7)
    t4 = load("t4")
    assert t4["label"] == ("robust" if not t4["broken"] else "sensitive")
    base = t4["baseline"]
    for name, v in t4["variants"].items():
        ratio = v["mass"] / base["mass"]
        assert (["%s" % name, "T6 mass"] in t4["broken"]) == (not (1 / 3 < ratio < 3))
        if not t4["sigma_condition_skipped"]:
            assert ([name, "sigma"] in t4["broken"]) == (not abs(v["sigma_ii"] - base["sigma_ii"]) < 0.3)


def test_readings():
    s = summary()
    lab = s["labels"]
    bad = [n for n, c in (("T1", lab["T1"] != "abstract reproduced"), ("T2a", lab["T2a_reproduction"] == "not reproduced"),
                          ("T3 (a)", lab["T3a"] in ("net rotation", "net counter-rotation")),
                          ("T3 (b)", lab["T3b"] == "not rotation dominated")) if c]
    if bad:
        want = "not reproduced"
    elif (lab["T2a_reproduction"] == "reproduced" and lab["T3a"] == "no net rotation"
          and lab["T3b"] == "rotation dominated"):
        want = "R22's numbers reproduce from the public sample"
    else:
        want = "partly reproduced"
    assert s["reading_reproduction"]["label"] == want
    good = (lab["T2a_population"] == "consistent with 2.7 kpc" and lab["T2b_f5"] == "most within 5 kpc confirmed"
            and lab["T4"] == "robust" and lab["T5_g"] in ("minor", "moderate")
            and lab["T5_a5"] == "most apocentres below 5 kpc confirmed")
    chal = (lab["T2a_population"] == "different" or lab["T2b_f5"] == "not confirmed" or lab["T4"] == "sensitive"
            or lab["T5_g"] == "major" or lab["T5_a5"] == "not confirmed")
    want = "holds under our checks" if good else ("challenged" if chal else "undetermined")
    assert s["reading_robustness"]["label"] == want
