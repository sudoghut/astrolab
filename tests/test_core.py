"""Offline tests of the core library."""
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from astrolab import cache, claims, config, fetch, results, study


@pytest.fixture
def tmp_cache(tmp_path, monkeypatch):
    monkeypatch.setenv("ASTROLAB_CACHE_DIR", str(tmp_path / "cache"))
    return tmp_path / "cache"


def test_cache_dir_outside_project(tmp_cache):
    assert config.cache_dir() == tmp_cache


def test_default_cache_dir_not_in_project(monkeypatch):
    monkeypatch.delenv("ASTROLAB_CACHE_DIR", raising=False)
    assert config.ROOT not in config.cache_dir().parents


def test_cache_roundtrip_and_prune(tmp_cache):
    key = cache.key_for("t", {"a": 1})
    assert key == cache.key_for("t", {"a": 1}) != cache.key_for("t", {"a": 2})
    src = cache.staging_path(".bin")
    src.write_bytes(b"x" * 1000)
    cache.put_file(key, ".bin", src, {"provenance": {"source": "test", "request": "r"}})
    hit = cache.get(key, ".bin")
    assert hit and hit.payload.read_bytes() == b"x" * 1000
    assert cache.info()["entries"] == 1
    assert cache.prune(limit_bytes=0) == 1
    assert cache.get(key, ".bin") is None


def test_tap_refuses_above_hard_ceiling(tmp_cache):
    with pytest.raises(fetch.TooLarge):
        fetch.tap("SELECT 1", "gaia", max_rows=config.TAP_HARD_MAX_ROWS + 1)


def test_tap_cache_hit_needs_no_network(tmp_cache):
    adql = "SELECT  a FROM t"
    key = cache.key_for("tap", {"url": fetch.tap_url("gaia"), "adql": "SELECT a FROM t"})
    tmp = cache.staging_path(".parquet")
    pd.DataFrame({"a": [1, 2]}).to_parquet(tmp)
    cache.put_file(key, ".parquet", tmp, {"provenance": {"source": "tap:gaia", "request": "SELECT a FROM t"}})
    res = fetch.tap(adql, "gaia")
    assert res.from_cache and list(res.data.a) == [1, 2]


def test_study_budget_enforced(monkeypatch):
    monkeypatch.setattr(config, "STUDY_BUDGET_BYTES", 1000)
    ctx = study.Context(study.Study(Path(".")))
    ctx._charge(600, "a")
    with pytest.raises(fetch.TooLarge):
        ctx._charge(600, "b")


def test_unknown_service():
    with pytest.raises(KeyError):
        fetch.tap_url("nope")


def test_results_jsonable(tmp_path):
    obj = {"a": np.float64(1.5), "b": np.array([1, 2]), "c": float("nan"),
           "df": pd.DataFrame({"x": [1.0, 2.0]}), "i": np.int64(3), "t": np.bool_(True)}
    p = results.write_json(tmp_path / "r.json", obj)
    data = json.loads(p.read_text())
    assert data == {"a": 1.5, "b": [1, 2], "c": None, "df": {"x": [1.0, 2.0]}, "i": 3, "t": True}


def test_new_study_from_template(tmp_path, monkeypatch):
    studies = tmp_path / "studies"
    monkeypatch.setattr(config, "STUDIES", studies)
    monkeypatch.setattr(config, "TEMPLATE", Path(__file__).parent.parent / "studies" / "_template")
    s = study.new("My Question!", "My question", "L3")
    assert s.id == "000-my-question"
    assert s.meta["level"] == "L3" and s.meta["status"] == "planned"
    assert "{{" not in (s.path / "README.md").read_text(encoding="utf-8")
    assert study.new("second", "Second").id == "001-second"
    assert study.resolve("1").id == "001-second"


def test_repo_claims_valid():
    assert claims.validate_all() == {}


def test_claim_validation_catches_errors():
    bad = {"_file": "x.yaml", "id": "y", "title": "t", "statement": "s", "level": "L9",
           "grade": "maybe", "sources": [], "reproduction": {"status": "?"}}
    errs = claims.validate(bad)
    assert len(errs) == 7  # 5 schema errors + missing title_zh / statement_zh
    good = {**bad, "_file": "y.yaml", "level": "L3", "grade": "hint", "sources": [{"cite": "c"}],
            "reproduction": {"status": "not-started"}, "title_zh": "标题", "statement_zh": "陈述"}
    assert claims.validate(good) == []
    assert claims.validate({**good, "title_zh": "TODO: 中文标题"}) == ["'title_zh' must be a non-empty Chinese string"]


def test_studies_have_chinese_fields():
    for s in study.discover():
        assert claims.zh_errors(s.meta, ("title_zh", "question_zh")) == [], s.id
