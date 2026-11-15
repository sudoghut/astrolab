"""Assertions that this study's results are complete and internally consistent, read from results/.

Run the study first: python -m astrolab run 007-m10-gwtc4-bbh-mass-35msun
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
    o3_ok = r1["o3_part"] == "reproduced"
    if not o3_ok:
        want = "not reproduced"
    elif r1["target_ambiguous"]:
        want = "described"
    else:
        want = "reproduced" if r1["o4a_part"] == "reproduced" else "not reproduced"
    assert r1["verdict"] == want
    assert r1["target_ambiguous"] == (r1["target_size"] == 0 or r1["target_size"] != 84)


def test_r1_named_checks_recorded():
    r1 = load("r1")
    assert len(r1["named_checks"]) == 7
    if r1["o3_part"] == "reproduced":
        assert all(v["pass"] for v in r1["named_checks"].values())


def test_r2_fractions():
    r2 = load("r2")
    n = r2["n_lo"] + r2["n_hi"]
    for p in r2["per_turnover"]:
        assert abs(p["frac_obs"] - r2["n_hi"] / n) < 1e-12 and 0 < p["f_pred"] < 1 and 0 <= p["binom_p"] <= 1


def test_r3_nested():
    r3 = load("r3")
    for f in r3["fits"]:
        assert f["two_dlnl"] >= -1e-6


def test_result_files_small():
    for path in RESULTS.glob("*.json"):
        assert path.stat().st_size < 1024 ** 2, path.name
