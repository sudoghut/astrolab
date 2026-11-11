"""Checks on the smoke-test results (run the study first)."""
import json
from pathlib import Path

import pytest

RESULTS = Path(__file__).parent / "results"


def load(name):
    path = RESULTS / f"{name}.json"
    if not path.exists():
        pytest.skip(f"{path.name} missing; run: python -m astrolab run 000")
    return json.loads(path.read_text(encoding="utf-8"))


def test_nearest_is_proxima():
    nearest = load("summary")["nearest_5"][0]
    assert 1.29 < nearest["dist_pc"] < 1.31  # Proxima Cen, 1.3020 pc


def test_density_covers_full_sky():
    d = load("density_healpix3")
    assert len(d["n"]) == 12 * 4**3


def test_provenance_recorded():
    prov = load("provenance")
    assert all("request" in r and "sha256" in r for r in prov["inputs"])
