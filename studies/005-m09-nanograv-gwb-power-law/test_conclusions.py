"""Assertions that this study's results are complete and internally consistent, read from results/.

Run the study first: python -m astrolab run 005-m09-nanograv-gwb-power-law
The pre-registered verdicts are recorded in the results; these tests check that each criterion was
evaluated as written (README section 2), not that it came out a particular way.
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


def test_r1_verdict_follows_threshold():
    r1 = load("r1")
    if r1.get("verdict") == "not evaluable":
        pytest.skip(r1.get("reason"))
    assert r1["q05_A"] < r1["median_A"] < r1["q95_A"]
    expected = "consistent with L8's interval" if r1["hellinger"] < r1["h_max"] else "differs"
    assert r1["verdict"] == expected
    assert r1["h_max"] == 0.15


def test_r2_category_follows_q():
    r2 = load("r2")
    if r2.get("verdict") == "not evaluable":
        pytest.skip(r2.get("reason"))
    q = r2["q_hpd_13_3"]
    assert 0.0 <= q <= r2["q_hpd_13_3_ge"] <= 1.0
    word = "weaker" if q < 0.95 else ("stronger" if q > 0.997 else "same order")
    assert r2["category"].startswith(word) and r2["category"].endswith("(descriptive category)")


def test_r2b_counts_consistent():
    r2b = load("r2b")
    if r2b.get("verdict") == "not evaluable":
        pytest.skip(r2b.get("reason"))
    rows = r2b["rows"]
    assert len(rows) == r2b["n_rows"] == 24
    assert r2b["n_models_overlap_ci90"] == sum(r["overlap_ci90"] for r in rows)
    assert r2b["n_models_contain_median"] == sum(r["contains_median"] for r in rows)
    assert r2b["n_models_contain_median"] <= r2b["n_models_overlap_ci90"]
    assert r2b["n_models_overlap_ci90_merged"] <= r2b["n_models_overlap_ci90"]
    assert r2b["n_models_contain_median_merged"] <= r2b["n_models_contain_median"]


def test_result_files_small():
    for path in RESULTS.glob("*.json"):
        assert path.stat().st_size < 1024 ** 2, path.name


def test_r4_present():
    r4 = load("r4")
    if r4.get("verdict") == "not evaluable":
        pytest.skip(r4.get("reason"))
    assert abs(r4["ln_bf_turnover_vs_pl"] - (r4["ln_Z_turn"] - r4["ln_Z_pl"])) < 1e-9
