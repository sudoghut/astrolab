"""Assertions that this study's results are complete and internally consistent, read from results/.

Run the study first: python -m astrolab run 006-m08-z14-galaxies-number-density
These check that each pre-registered criterion (README section 2) was evaluated as written.
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


def test_r1_verdicts_follow_tolerances():
    r1 = load("r1")
    ok = abs(r1["log_phi"] + 5.36) < 0.01 and abs(r1["err_hi"] - 0.37) < 0.05 and abs(r1["err_lo"] - 0.45) < 0.05
    assert r1["verdict_density"] == ("reproduced" if ok else "not reproduced")
    assert r1["verdict_volume"] == ("reproduced" if abs(r1["volume_ratio"] - 1) < 0.05 else "not reproduced")
    assert r1["mod_poisson_bound_holds"] == (r1["p_tail_n26_ppm"] <= 200 and r1["p_tail_ratio100_ppm"] <= 200)


def test_r2_verdict_follows_ratio():
    r2 = load("r2")
    if r2.get("verdict") == "not evaluable":
        pytest.skip(r2.get("reason"))
    ratio = r2["ratio_to_n26"]
    want = "same order as N26's baseline" if 1 / 3 <= ratio <= 3 else ("higher" if ratio > 3 else "lower")
    assert r2["verdict"] == want
    assert r2["robustness"] in ("robust", "calibration-dependent", "not assessable")
    assert r2["variant_counts"]["total"] == 72


def test_r3_roots_ordered():
    r3 = load("r3")
    if r3.get("verdict") == "not evaluable":
        pytest.skip(r3.get("reason"))
    roots = r3["sigma_roots"]
    assert roots["upper"]["value"] >= roots["central"]["value"] >= roots["lower"]["value"]


def test_result_files_small():
    for path in RESULTS.glob("*.json"):
        assert path.stat().st_size < 1024 ** 2, path.name
