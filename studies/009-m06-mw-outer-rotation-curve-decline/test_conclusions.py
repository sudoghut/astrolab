"""Assertions that this study's results are complete and internally consistent, read from results/.

Run the study first: python -m astrolab run 009-m06-mw-outer-rotation-curve-decline
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
    b = r1["base"]
    ok = abs(b["median_gamma"] + 0.47) <= 0.05 and abs(b["S"] - 3.1) <= 0.3
    assert r1["verdict"] == ("reproduced" if ok else "not reproduced")


def test_r2_all_models_present():
    r2 = load("r2")
    assert set(r2["models"]) == {"E dJ", "E J", "E CM", "G dJ", "G J", "G CM", "B2"}


def test_r3_constant_bias_null_control():
    r3 = load("r3")
    g = list(r3["constant_gamma"].values())
    assert max(g) - min(g) < 0.05


def test_result_files_small():
    for path in RESULTS.glob("*.json"):
        assert path.stat().st_size < 1024 ** 2, path.name


def test_r6_cov_rules():
    """R6-COV (README 2.6, addendum 2026-11-17): calibration, flags, test values and labels recomputed
    from the saved curves and fits."""
    import math
    r6 = load("r6")
    t = r6["target"]
    assert t == 15.0 and abs(r6["spread"] - math.sqrt(30)) < 1e-12
    assert set(r6["covariances"]) == {"se_2", "se_4", "se_8", "global", "fractional"}
    vals = {"t1": {}, "t2": {}, "t3_nfw": {}, "t3_lcdm": {}}
    flags = {}
    for name, res in r6["covariances"].items():
        curve = res["curve"]
        assert len(curve) == 100
        first = next((i for i, (v, c) in enumerate(curve) if c is not None and c >= t), None)
        if first is None:
            assert res["status"] == "not calibratable"
        elif first > 0 and curve[first - 1][1] is None:
            assert res["status"] == "not evaluable"
        else:
            if res["status"] == "calibrated" and first > 0:
                assert curve[first - 1][0] <= res["value"] <= curve[first][0]
        if res["status"] != "calibrated":
            for k in vals:
                vals[k][name] = None
            continue
        tt = res["tests"]
        frac = tt["max_corr_fraction"]
        if name != "fractional":
            assert frac == res["value"]
        flags[name] = frac > 0.9
        assert res["high_f"] == flags[name]
        pl = tt["powerlaw"]
        vals["t1"][name] = pl.get("sigma_flat") if pl["t1_evaluable"] else None
        vals["t2"][name] = (pl["D_02"] - pl["D_K"]) if pl["t2_evaluable"] else None
        if pl["t1_evaluable"]:
            assert abs(pl["sigma_flat"] - math.sqrt(pl["dchi2_flat"])) < 1e-12
        h = tt["halos"]
        for key, model in (("t3_nfw", "nfw"), ("t3_lcdm", "lcdm")):
            ok = h["einasto"]["converged"] and h[model]["converged"]
            vals[key][name] = (h[model]["chi2"] - h["einasto"]["chi2"]) if ok else None
        for m in h.values():
            assert m["converged"] == (m["n_agree"] >= 3)

    def rule(test, v):
        if test == "t1":
            return ("flat rejected at >= 3 sigma" if all(x >= 3 for x in v) else
                    "flat rejected at >= 2 sigma" if all(x >= 2 for x in v) else
                    "flat not rejected at 2 sigma" if all(x < 2 for x in v) else "kernel-dependent")
        if test == "t2":
            return ("Keplerian favoured over gamma = -0.2" if all(x >= 4 for x in v) else
                    "gamma = -0.2 favoured over Keplerian" if all(x <= -4 for x in v) else
                    "not distinguished" if all(abs(x) < 4 for x in v) else "kernel-dependent")
        bands = {("not disfavoured" if x < 4 else "mildly disfavoured" if x < 9 else "disfavoured") for x in v}
        return bands.pop() if len(bands) == 1 else "kernel-dependent"

    for key, v in vals.items():
        test = "t3" if key.startswith("t3") else key
        use = {k: x for k, x in v.items() if x is not None}
        if len(use) < 3:
            exp = "not evaluable"
        else:
            a = rule(test, list(use.values()))
            unf = [x for k, x in use.items() if not flags.get(k)]
            if len(unf) < 3:
                exp = a + " (only with high-f covariances)"
            else:
                exp = a if a == rule(test, unf) else "kernel-dependent (high-f)"
        assert r6["labels"][key] == exp, key
        for name, x in v.items():
            assert (r6["values"][key][name] is None) == (x is None)
            if x is not None:
                assert abs(r6["values"][key][name] - x) < 1e-9
