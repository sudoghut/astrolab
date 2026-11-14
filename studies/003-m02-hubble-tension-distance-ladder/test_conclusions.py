"""Assertions that this study's conclusions still hold, read from results/.

Run the study first: python -m astrolab run 003-m02-hubble-tension-distance-ladder
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


def test_summary_exists():
    assert load("summary")


def test_r1_printed_baseline_reproduced():
    r1 = load("r1")
    assert abs(r1["fivelogh0"] - 9.318) < 0.001          # R22: H0 = 73.04
    assert abs(r1["chi2_dof"] - 1.03) < 0.005
    assert r1["verdict"] == "not reproduced"              # the public lstsq file is a different fit


def test_r2_anchor_step_reproduced():
    a = load("r2")["anchor_step"]
    assert a["verdict"] == "reproduced"
    assert abs(a["shift"] - (-0.0158)) <= 0.005


def test_r2_host_step_amended():
    h = load("r2")["host_step"]
    assert h["preregistered_verdict"] == "not evaluable (host identification)"
    assert "amended" in h["status"]
    assert h["z"] <= -2 and abs(h["shift"] - (-0.0405)) <= 2 * h["shift_sigma"] + 0.02
    assert abs(h["shift_check_ay"] - h["shift"]) < 1e-8
    assert abs(h["nested_var_check"] - h["shift_sigma"] ** 2) < 1e-8


def test_host_labelling_unique_cchp_set():
    i = load("host_identification")
    assert i["matching_found"] and not i["alt_changes_cchp_set"]


def test_r3_same_hosts_agree():
    r3 = load("r3")
    assert r3["cchp_match"] == "matched"
    assert abs(r3["d"]) < 2 * r3["sigma_d"]


def test_r4_descriptive():
    r4 = load("r4")
    assert r4["draws"] >= 2000 and 0 <= r4["percentile"] <= 100
