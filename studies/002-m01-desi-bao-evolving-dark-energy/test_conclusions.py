"""Assertions that this study's conclusions still hold, read from results/.

Run the study first: python -m astrolab run 002-m01-desi-bao-evolving-dark-energy
Thresholds are the pre-registered ones (README section 2); the verdicts asserted here are the
results of the 2026-11-14 run.
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
    assert r1["chain_ok"]
    assert abs(r1["posterior"]["Om"]["mean"] - 0.2975) <= 0.3 * 0.0086
    assert abs(r1["posterior"]["hrd"]["mean"] - 101.54) <= 0.3 * 0.73
    assert r1["verdict"] == "reproduced"


def test_r2_compressed_cmb_depends_on_reading():
    r2 = load("summary")["R2"]
    assert abs(r2["reading_B_without_nu"]["dchi2"] - (-8.0)) <= 1.0
    assert abs(r2["reading_A_with_nu"]["dchi2"] - (-8.0)) > 1.0
    assert r2["overall"] == "conditionally reproduced (reading B)"
    # the theta_* calibration (K +- 1 prior sigma) does not move reading A into the tolerance
    kc = r2["K_check"]
    assert all(abs(kc[k] - (-8.0)) > 1.0 for k in ("A+", "A-"))


def test_r3_no_cmb():
    r3 = load("summary")["R3"]
    for name, target in (("desi", -4.7), ("desi_pantheonplus", -4.9), ("desi_union3", -10.1)):
        assert abs(r3[name]["dchi2"] - target) <= 1.0, name
    assert r3["overall"] == "reproduced"
