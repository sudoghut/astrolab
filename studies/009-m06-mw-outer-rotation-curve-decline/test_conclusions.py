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
