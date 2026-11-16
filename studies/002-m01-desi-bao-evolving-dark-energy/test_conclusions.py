"""Assertions that this study's conclusions still hold, read from results/.

Run the study first: python -m astrolab run 002-m01-desi-bao-evolving-dark-energy
Thresholds are the pre-registered ones (README section 2); the R1-R3 verdicts asserted here are the
results of the 2026-11-14 run; R2-CAMB (addendum 2026-11-16) is recomputed from its rule.
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


def test_fits_valid():
    d = load("summary")
    for fit in [d["R2"]["reading_A_with_nu"], d["R2"]["reading_B_without_nu"],
                d["R3"]["desi"], d["R3"]["desi_pantheonplus"], d["R3"]["desi_union3"]]:
        assert fit["valid"], fit.get("reason")
        assert fit["w0wa"]["chi2"] <= fit["lcdm"]["chi2"] + 1e-3      # nesting
        assert fit["lcdm"]["n_agree"] >= 3 and fit["w0wa"]["n_agree"] >= 3


def test_r1_bao_only_lcdm():
    r1 = load("summary")["R1"]
    assert r1["chain_ok"] and r1["map_ok"]
    assert abs(r1["posterior"]["Om"]["mean"] - 0.2975) <= 0.3 * 0.0086
    assert abs(r1["posterior"]["hrd"]["mean"] - 101.54) <= 0.3 * 0.73
    assert r1["verdict"] == "reproduced"


def test_r2_compressed_cmb_depends_on_reading():
    r2 = load("summary")["R2"]
    assert abs(r2["reading_B_without_nu"]["dchi2"] - (-8.0)) <= 1.0
    assert abs(r2["reading_A_with_nu"]["dchi2"] - (-8.0)) > 1.0
    assert r2["overall"] == "conditionally reproduced (reading B)"
    # the K check is diagnostic (README section 2); only its fits' validity is asserted
    kc = r2["K_check"]
    assert all(kc[k + "_valid"] for k in ("A+", "A-", "B+", "B-"))


def test_r3_no_cmb():
    r3 = load("summary")["R3"]
    for name, target in (("desi", -4.7), ("desi_pantheonplus", -4.9), ("desi_union3", -10.1)):
        assert abs(r3[name]["dchi2"] - target) <= 1.0, name
    assert r3["overall"] == "reproduced"


def test_r2_camb_rule():
    """R2-CAMB (README section 2, addendum 2026-11-16): per-reading verdicts and the T-022
    conclusion recomputed from the saved numbers with the pre-registered rules."""
    rc = load("r2_camb")
    rec = {"A": "not reproduced", "B": "reproduced"}
    assert rc["recorded"] == rec
    assert rc["settings"]["camb_version"] and rc["settings"]["dark_energy_model"] == "ppf"
    keys = {"A": "reading_A_with_nu", "B": "reading_B_without_nu"}
    verdicts = {}
    for var in ("anchored", "raw"):
        v = rc["variants"][var]
        verdicts[var] = {}
        for rd, key in keys.items():
            fit = v[key]
            lc, wc = fit["lcdm"], fit.get("w0wa")
            # validity recomputed from the saved diagnostics (README section 2 checks)
            ok = (lc["converged"] and wc is not None and wc["converged"] and lc["n_agree"] >= 3
                  and wc["n_agree"] >= 3 and wc["chi2"] <= lc["chi2"] + 1e-3)
            assert bool(fit["valid"]) == bool(ok), (var, rd)
            if not ok:
                exp = "failed fit"
            else:
                assert abs(fit["dchi2"] - (wc["chi2"] - lc["chi2"])) < 1e-9
                exp = "reproduced" if abs(fit["dchi2"] - (-8.0)) <= 1.0 else "not reproduced"
            assert fit["verdict"] == exp, (var, rd)
            verdicts[var][rd] = exp
    valid = {k: "failed fit" not in v.values() for k, v in verdicts.items()}
    changed = {k: [r for r in rec if v[r] != rec[r]] for k, v in verdicts.items()}
    if all(valid.values()) and not any(changed.values()):
        expected = ["R2 robust to the theta* calibration"]
    else:
        expected = []
        a_flip = valid["anchored"] and bool(changed["anchored"])
        if a_flip:
            expected.append("R2 depends on the cosmology dependence of the theta* calibration "
                            "(reading %s)" % ", ".join(changed["anchored"]))
        if valid["raw"] and changed["raw"] and not a_flip:
            expected.append("R2 depends on the absolute theta* calibration (anchor) (reading %s)"
                            % ", ".join(changed["raw"]))
        expected += [f"inconclusive ({k} variant: failed fit)" for k in ("anchored", "raw") if not valid[k]]
    concl = rc["conclusion"]
    assert concl == expected
    assert load("summary")["R2_camb"]["conclusion"] == concl
