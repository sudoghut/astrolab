"""Assertions that this study's labels follow from its stored numbers (README section 2).

The decision rules are written out again here, independently of stats011.py, so a slip in either
place shows up. Run the study first: python -m astrolab run 011-m11-radcliffe-wave-oscillation
"""
import json
import math
from pathlib import Path

import pytest
from scipy.stats import chi2

RESULTS = Path(__file__).parent / "results"


def load(name):
    path = RESULTS / f"{name}.json"
    if not path.exists():
        pytest.skip(f"{path.name} missing; run the study first")
    return json.loads(path.read_text(encoding="utf-8"))


def test_summary_exists():
    s = load("summary")
    assert s["status"] == "complete"
    assert s["load_check"]["passed"] and abs(s["load_check"]["weighted_mean_vz"]) < 3.0


def test_files_small():
    for p in RESULTS.glob("*.json"):
        assert p.stat().st_size < 1024 ** 2, p.name


def test_t1_labels():
    t1 = load("t1_t2")["t1"]
    for col in ("col4", "col6"):
        rows = t1[col]["parameters"]
        n = 0
        for k in ("A", "p", "delta", "s0", "gamma", "phi"):
            r = rows[k]
            inside = r["k24"]["median"] - r["k24"]["minus"] <= r["ours"]["median"] <= r["k24"]["median"] + r["k24"]["plus"]
            assert inside == r["inside_k24_1sigma"]
            n += inside
        assert n == t1[col]["n_inside_of_6"]
        want = "reproduced" if n >= 5 else ("partly reproduced" if n >= 3 else "not reproduced")
        assert t1[col]["label"] == want


def test_t2_reported():
    t2 = load("t1_t2")["t2"]
    assert 0.0 <= t2["B"]["p16"] <= t2["B"]["median"] <= t2["B"]["p84"] <= 1.0
    assert 0.0 <= t2["P_B_gt_0p95"] <= 1.0 and 0.0 <= t2["P_B_lt_0p5"] <= 1.0


def _p_boot(k, n):
    return (1 + k) / (1 + n)


def _t3_check(st, d):
    mocks = st["mocks_two_dlnL"]
    k = sum(m >= st["two_dlnL"] for m in mocks)
    assert k == st["k_mocks_at_least_obs"]
    assert st["p_boot"] == pytest.approx(_p_boot(k, len(mocks)))
    assert st["p_raw"] == pytest.approx(chi2.sf(st["two_dlnL"], d))
    m = sum(mocks) / len(mocks)
    if m > 0:
        assert st["p_cal"] == pytest.approx(chi2.sf(st["two_dlnL"] * d / m, d), rel=1e-6, abs=1e-12)
    else:
        assert st["p_cal"] is None


def test_t3_labels():
    t3 = load("t3")
    s, t = t3["standing_stat"], t3["travelling_stat"]
    _t3_check(s, 1)
    _t3_check(t, 2)
    if s["p_cal"] is None:
        want = "not evaluable"
    elif s["p_cal"] < 0.001 and s["p_raw"] < 0.001 and s["k_mocks_at_least_obs"] == 0:
        want = "standing excluded strongly"
    elif s["p_cal"] < 0.05 and s["p_boot"] < 0.05:
        want = "standing excluded"
    else:
        want = "standing not excluded"
    assert t3["standing"] == want
    if t["p_cal"] is None:
        want = "not evaluable"
    elif t["p_cal"] < 0.05 and t["p_boot"] < 0.05:
        want = "pure travelling (B = 1) disfavoured"
    else:
        want = "pure travelling (B = 1) not disfavoured"
    assert t3["pure_travelling"] == want


def _t4_want(p, power):
    if power < 0.8:
        return "undetermined"
    if p < 0.01:
        return "standing excluded by the phases"
    if p > 0.05:
        return "standing not excluded by the phases"
    return "undetermined"


def _t4_check(g):
    """p and power from the stored mock counts (and from the stored R values when present)."""
    assert g["p"] == pytest.approx(_p_boot(g["k_standing_at_or_below"], g["n_standing"]))
    assert g["power_B1"] == pytest.approx(g["k_power_B1_p_below"] / g["n_power_B1"])
    assert g["label"] == _t4_want(g["p"], g["power_B1"])


def test_t4_label():
    t4 = load("t4")
    g = t4["gauss"]
    _t4_check(g)
    assert t4["label"] == g["label"]
    if "R_standing" in g:
        st = sorted(g["R_standing"])
        k = sum(r <= t4["R_obs"] for r in st)
        assert k == g["k_standing_at_or_below"]
        n_low = 0
        for r in g["R_power_B1"]:
            kk = sum(x <= r for x in st)
            n_low += _p_boot(kk, len(st)) < 0.01
        assert n_low == g["k_power_B1_p_below"]


def _wl_want(lo, hi):
    if lo is None or hi is None:
        return "not evaluable"
    if 0.8 <= lo and hi <= 1.25:
        return "consistent"
    if hi < 0.8 or lo > 1.25:
        return "different"
    return "undetermined"


def _bhat_want(lo, hi, wl, ka):
    if lo is None or hi is None:
        return "not evaluable"
    if wl == "different":
        return "not applicable (wavelengths differ)"
    if not ka:
        return "undetermined"
    if lo > 0.4:
        return "travelling component in K24's direction dominates"
    if hi < 0.4:
        return "no travelling dominance in K24's direction"
    return "undetermined"


def test_t5_labels_and_known_answer():
    t5 = load("t5")
    ka = t5["known_answer"]
    ok = True
    for B, row in ka["injections"].items():
        lo, hi = row["median_mock_interval"]
        if float(B) >= 1.0:
            this = lo is not None and lo > 0.4
        else:
            this = lo is not None and lo <= 2 * float(B) - 1 <= hi
        assert this == row["pass"]
        ok &= this
    assert ok == ka["passed"] == t5["known_answer_passed"]
    wl = _wl_want(*t5["k_ratio_interval"])
    assert t5["wavelengths_label"] == wl
    assert t5["bhat_label"] == _bhat_want(*t5["bhat_interval"], wl, ka["passed"])


def _reduced_standing(obs, factor):
    if factor is None:
        return "not evaluable"
    pc, pr = chi2.sf(obs * factor, 1), chi2.sf(obs, 1)
    if pc < 0.001 and pr < 0.001:
        return "standing excluded strongly"
    return "standing excluded" if pc < 0.05 else "standing not excluded"


def _reduced_travel(obs, factor):
    if factor is None:
        return "not evaluable"
    return ("pure travelling (B = 1) disfavoured" if chi2.sf(obs * factor, 2) < 0.05
            else "pure travelling (B = 1) not disfavoured")


def test_t6_robustness():
    t6 = load("t6")
    assert len(t6["variants"]) == 15
    n_changes = sum(len(v["changed"]) for v in t6["variants"])
    assert n_changes == len(t6["changes"])
    assert t6["label"] == ("robust" if n_changes == 0 else "fragile")
    main_full, main_red = t6["main_labels_full_rule"], t6["main_labels_reduced_rule"]
    t3 = load("t3")
    fs, ft = t3["standing_stat"]["factor"], t3["travelling_stat"]["factor"]
    # the main run's reduced-rule labels, from its own numbers
    assert main_red["standing"] == _reduced_standing(t3["standing_stat"]["two_dlnL"], fs)
    assert main_red["pure_travelling"] == _reduced_travel(t3["travelling_stat"]["two_dlnL"], ft)
    for v in t6["variants"]:
        if v["t3"]["rule"] == "reduced":
            assert v["labels"]["T3 standing"] == _reduced_standing(v["two_dlnL_standing"], fs)
            assert v["labels"]["T3 pure travelling"] == _reduced_travel(v["two_dlnL_travelling"], ft)
        else:
            _t3_check(v["t3"]["standing_stat"], 1)
            _t3_check(v["t3"]["travelling_stat"], 2)
        _t4_check(v["t4"]["gauss"])
        for c in t6["changes"]:
            assert "mcse" in c
    for v in t6["variants"]:
        ref = main_full if v["t3"]["rule"] == "full" else main_red
        assert v["t5"]["known_answer_passed"] == load("t5")["known_answer_passed"]
        changed = []
        for key, mk in (("T3 standing", "standing"), ("T3 pure travelling", "pure_travelling"), ("T4", "t4"),
                        ("T5 wavelengths", "t5_wavelengths"), ("T5 bhat", "t5_bhat")):
            if v["labels"][key] != ref[mk]:
                changed.append(key)
        assert changed == v["changed"], v["variant"]


def test_t7_label():
    t7 = load("t7")
    a, b, c = t7["a_col6_B1"]["m2lnL"], t7["b_vz_zero"]["m2lnL"], t7["c_B0p5"]["m2lnL"]
    want = "CO prefers the travelling wave" if (a + 9 <= b and a + 9 <= c) else "CO does not distinguish"
    assert t7["label"] == want


def test_t8_label():
    t8 = load("t8")
    pb, pk = t8["ln_omega0_broad_prior"], t8["ln_omega0_k24_prior"]
    half = 0.5 * (pb["p84"] - pb["p16"])
    assert half == pytest.approx(t8["halfwidth_broad"])
    narrow = half < 0.5 * 0.17
    stable = abs(pk["median"] - pb["median"]) / half < 0.5
    want = "data-driven" if (narrow and stable) else ("prior-driven" if not (narrow or stable) else "partly data-driven")
    assert t8["label"] == want


def test_overall_reading():
    s = load("summary")
    t1 = s["T1"]["col4"]
    t3, t4, t5, t6 = s["T3"]["standing"], s["T4"]["label"], s["T5"]["bhat"], s["T6"]["label"]
    support = (t1 in ("reproduced", "partly reproduced") and t3 in ("standing excluded", "standing excluded strongly")
               and t4 == "standing excluded by the phases"
               and t5 == "travelling component in K24's direction dominates" and t6 == "robust")
    if support:
        want = "K24's travelling-wave reading is supported by these data"
    elif t3 == "standing not excluded" and t5 == "no travelling dominance in K24's direction":
        want = "not supported"
    else:
        want = "mixed"
    assert s["overall"]["reading"] == want
    both_not = s["T1"]["col4"] == "not reproduced" and s["T1"]["col6"] == "not reproduced"
    assert ("qualifier" in s["overall"]) == both_not
    assert math.isfinite(s["T3"]["two_dlnL_standing"])
