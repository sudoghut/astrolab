"""Offline tests for Atlas footprints (design plan 011)."""
import json
import math

from astrolab import claims


def test_footprint_schema_accepts_valid():
    meta = {"footprint": {"scale": {"min_pc": 1, "max_pc": 10},
                          "sky": {"mode": "survey + targets", "survey": {"name": "S"},
                                  "targets": [{"name": "a", "ra": 10, "dec": 20}, {"name": "b"}]}}}
    assert claims.footprint_errors(meta) == []
    assert claims.footprint_errors({}) == []                   # footprint is optional


def test_footprint_schema_rejects_invalid():
    bad = [
        {"footprint": {"scale": {"min_pc": 10, "max_pc": 1}}},
        {"footprint": {"scale": {"min_pc": 0, "max_pc": 1}}},
        {"footprint": {"scale": {"min_pc": "x", "max_pc": 1}}},
        {"footprint": {"sky": {"mode": "everywhere"}}},
        {"footprint": {"sky": {"mode": "survey"}}},
        {"footprint": {"sky": {"mode": "targets"}}},
        {"footprint": {"sky": {"mode": "targets", "targets": [{"name": "a", "ra": 1}]}}},
        {"footprint": "all-sky"},
        {"footprint": {"scale": {"min_pc": 1, "max_pc": float("inf")}}},
        {"footprint": {"scale": {"min_pc": True, "max_pc": 10}}},
        {"footprint": {"sky": {"mode": "none + all-sky"}}},
        {"footprint": {"sky": {"mode": "all-sky + all-sky"}}},
        {"footprint": {"sky": {"mode": "targets", "targets": "x"}}},
        {"footprint": {"sky": {"mode": "targets", "targets": [{"name": "a", "ra": None, "dec": None}]}}},
        {"footprint": {"sky": {"mode": "targets", "targets": [{"name": "a", "ra": 10, "dec": 100}]}}},
        {"footprint": {"sky": {"mode": "targets", "targets": [{"name": "a", "ra": "x", "dec": 1}]}}},
        {"footprint": {"sky": {"mode": "all-sky", "targets": [{"name": "a", "ra": 1, "dec": 1}]}}},
    ]
    for meta in bad:
        assert claims.footprint_errors(meta), meta


def test_resolve_footprint_uses_targets_file_and_galactic(tmp_path):
    (tmp_path / "results").mkdir()
    # the Galactic centre and the north Galactic pole in ICRS
    (tmp_path / "results" / "targets.json").write_text(json.dumps(
        [{"name": "GC", "ra": 266.40500, "dec": -28.93617}]), encoding="utf-8")
    meta = {"level": "L3", "footprint": {"scale": {"min_pc": 100, "max_pc": 1000},
            "sky": {"mode": "targets", "targets": [{"name": "GC"}, {"name": "NGP", "ra": 192.85948, "dec": 27.12825},
                                                   {"name": "unknown"}]}}}
    fp = claims.resolve_footprint(tmp_path, meta)
    assert fp["scale"]["log10_min"] == 2.0 and fp["scale"]["log10_max"] == 3.0 and not fp["scale"]["default"]
    gc, ngp, unk = fp["sky"]["targets"]
    assert min(gc["l"], 360 - gc["l"]) < 0.01 and abs(gc["b"]) < 0.01
    assert ngp["b"] > 89.99
    assert unk["ra"] is None and unk["l"] is None                # unresolved, not dropped


def test_resolve_footprint_level_default(tmp_path):
    fp = claims.resolve_footprint(tmp_path, {"level": "L0"})
    lo, hi = claims.LEVEL_SCALE_LOG10["L0"]
    assert fp["scale"] == {"log10_min": lo, "log10_max": hi, "note": None, "default": True}
    assert fp["sky"]["modes"] == [] and fp["sky"]["targets"] == []


def test_repo_studies_have_valid_footprints():
    problems = {k: v for k, v in claims.validate_all().items() if k.startswith("studies/")}
    assert problems == {}
    data = claims.atlas_data()
    for s in data["studies"]:
        sc = s["footprint"]["scale"]
        assert math.isfinite(sc["log10_min"]) and sc["log10_min"] < sc["log10_max"]
    assert set(data["level_scale_log10"]) == set(data["levels"])


def test_invalid_footprint_does_not_crash_atlas(tmp_path):
    for fp in ({"scale": {"min_pc": 1, "max_pc": float("inf")}},
               {"sky": {"mode": "targets", "targets": [{"name": "a", "ra": None, "dec": None}]}},
               {"sky": {"mode": "targets", "targets": [{"name": "a", "ra": 10, "dec": 100}]}},
               {"sky": {"mode": "targets", "targets": "x"}}):
        out = claims.resolve_footprint(tmp_path, {"level": "L4", "footprint": fp})
        assert out["scale"]["default"] and out["sky"]["targets"] == []
        json.dumps(out, allow_nan=False)                         # valid JSON for the page


def test_yaml_exponent_forms():
    import yaml
    assert claims.footprint_errors(yaml.safe_load("footprint: {scale: {min_pc: 4.0e+8, max_pc: 1.4e+10}}")) == []
    assert claims.footprint_errors(yaml.safe_load("footprint: {scale: {min_pc: 4e8, max_pc: 1e10}}")) == []  # strings


def test_study_001_targets_resolve():
    data = claims.atlas_data()
    s = next(s for s in data["studies"] if s["id"].startswith("001-"))
    names = {t["name"]: t for t in s["footprint"]["sky"]["targets"]}
    assert set(names) == {"Gaia BH1", "Gaia BH2", "Gaia BH3"}
    assert all(t["l"] is not None and t["b"] is not None for t in names.values())
