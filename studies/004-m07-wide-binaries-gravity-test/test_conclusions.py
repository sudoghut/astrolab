"""Assertions that this study's conclusions still hold, read from results/.

Run the study first: python -m astrolab run 004-m07-wide-binaries-gravity-test
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


def test_r1_different_sample():
    r1 = load("summary")["R1"]
    assert r1["verdict"] == "different sample"
    assert r1["N_main"] == 639
    assert r1["target"] == 1421 and not r1["within_20pct"]


def test_r2_cannot_distinguish():
    s = load("summary")
    assert s["R2"].startswith("cannot distinguish")
    assert 1 / 100 < s["R2_L"] < 100


def test_mad_errors_favour_mond():
    # C26's stated MAD/sqrt(N) errors turn the same medians into "MOND favoured":
    # the error convention, not the data, decides (Lean gap gap_err).
    mad = load("variants")["main"]["reproduction"]["mad"]
    assert mad["valid"] and mad["L"] < 1 / 100
