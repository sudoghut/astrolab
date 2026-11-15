"""Assertions that this study's results are complete and internally consistent, read from results/.

Run the study first: python -m astrolab run 008-m03-s8-des-y6-cmb-parameter-difference
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
    for key in ("cmb", "des_3x2pt"):
        v = r1[key]
        if "mean" not in v:
            continue
        pub = v["published"]
        mean_ok = abs(v["mean"] - pub[0]) <= 0.002
        ends_ok = abs(v["hi"] - (pub[0] + pub[1])) <= 0.003 and abs(v["lo"] - (pub[0] - pub[2])) <= 0.003
        assert v["verdict"] == ("reproduced" if mean_ok and ends_ok else "not reproduced")


def test_r2_verdict_rule():
    r1, r2 = load("r1"), load("r2")
    gate = r1["cmb"].get("mean_ok") and r1["des_3x2pt"].get("mean_ok")
    for tag in ("1d", "2d"):
        if tag not in r2:
            continue
        v = r2[tag]
        ok = abs(v["n_sigma"] - v["published"]) <= 0.15 + 2 * v["s"]
        if not gate:
            assert v["verdict"].startswith("not evaluable")
        elif v["s"] > 0.03:
            assert v["verdict"] == "not evaluable (s > s_max)"
        elif r2["support"].get("fails"):
            assert v["verdict"].startswith("not evaluable (prior support)")
        else:
            assert v["verdict"] == ("reproduced" if ok else "not reproduced")


def test_result_files_small():
    for path in RESULTS.glob("*.json"):
        assert path.stat().st_size < 1024 ** 2, path.name
