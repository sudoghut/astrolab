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


def test_tap_refuses_result_above_download_limit(tmp_cache, monkeypatch):
    class _Res:
        query_status = "OK"

        def to_table(self):
            from astropy.table import Table
            return Table({"a": np.arange(5000.0)})

    monkeypatch.setattr(fetch, "_run_tap", lambda url, q, maxrec, mode: _Res())
    monkeypatch.setattr(config, "HTTP_MAX_BYTES", 1000)
    with pytest.raises(fetch.TooLarge):
        fetch.tap("SELECT a FROM big", "gaia", max_rows=10000)


def test_streamed_votable_download_capped(tmp_cache, monkeypatch):
    class _Resp:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def raise_for_status(self):
            pass

        def iter_content(self, n):
            for _ in range(100):
                yield b"x" * 1000

    class _Sess:
        def get(self, uri, stream=True, timeout=0):
            return _Resp()

    class _Svc:
        _session = _Sess()

    monkeypatch.setattr(config, "HTTP_MAX_BYTES", 5000)
    with pytest.raises(fetch.TooLarge):
        fetch._download_votable(_Svc(), "http://example.invalid/result")


def test_cached_tap_result_over_limit_refused(tmp_cache, monkeypatch):
    key = cache.key_for("tap", {"url": fetch.tap_url("gaia"), "adql": "SELECT b FROM t"})
    tmp = cache.staging_path(".parquet")
    pd.DataFrame({"b": np.arange(20000.0)}).to_parquet(tmp)
    cache.put_file(key, ".parquet", tmp, {"provenance": {"source": "tap:gaia", "request": "SELECT b FROM t"}})
    monkeypatch.setattr(config, "HTTP_MAX_BYTES", 1000)
    with pytest.raises(fetch.TooLarge):
        fetch.tap("SELECT b FROM t", "gaia")


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
    assert claims.validate({**good, "title_zh": "TODO: 中文标题"}) == \
        ["'title_zh' is still the template placeholder; fill in the Chinese text"]
    assert claims.validate({**good, "statement_zh": "   "}) == ["'statement_zh' must be a non-empty Chinese string"]


def test_validate_all_reports_study_placeholders(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "STUDIES", tmp_path / "studies")
    monkeypatch.setattr(config, "TEMPLATE", Path(__file__).parent.parent / "studies" / "_template")
    s = study.new("fresh", "Fresh", "L3")  # template placeholders, Chinese not filled in yet
    errs = claims.validate_all()[f"studies/{s.id}/study.yaml"]
    assert len(errs) == 2 and all("placeholder" in e for e in errs)


def test_studies_have_chinese_fields():
    for s in study.discover():
        assert claims.zh_errors(s.meta, claims.STUDY_ZH_FIELDS) == [], s.id


def test_every_web_page_loads_i18n():
    """Bilingual rule (AGENTS.md): every page loads the shared English/Chinese switch."""
    root = config.ROOT
    pages = [root / "atlas" / "web" / "index.html"]
    for d in sorted((root / "studies").iterdir()):
        if (d / "web").is_dir():
            pages += sorted((d / "web").rglob("*.html"))
    assert len(pages) >= 4
    for p in pages:
        text = p.read_text(encoding="utf-8")
        head = text.split("</head>", 1)[0]
        tag = re.search(r'<script[^>]*\ssrc="[^"]*i18n\.js"', head)
        assert tag, f"{p} does not load i18n.js in <head>"
        title = head.find("<title>")
        assert title < 0 or title < tag.start(), f"{p}: load i18n.js after <title>"
        assert 'class="zh"' in text or "L(" in text or "t(" in text, f"{p} has no Chinese text"
        if "_template" not in p.parts:
            assert "TODO: 中文" not in text, f"{p} still has the template's Chinese placeholder"


def test_staging_paths_unique_and_put_file_overwrites(tmp_cache):
    """Parallel fetches of the same key (e.g. two threads issuing an identical count query) must not
    collide in staging, and storing an existing key again must succeed (Windows)."""
    import threading

    paths = []
    th = [threading.Thread(target=lambda: paths.append(cache.staging_path(".bin"))) for _ in range(50)]
    [t.start() for t in th]
    [t.join() for t in th]
    assert len(set(paths)) == 50
    key = cache.key_for("t", {"dup": 1})
    for payload in (b"a" * 10, b"b" * 10):
        src = cache.staging_path(".bin")
        src.write_bytes(payload)
        cache.put_file(key, ".bin", src, {"provenance": {"source": "test", "request": "r"}})
        assert not src.exists()
    assert cache.get(key, ".bin").payload.read_bytes() == b"b" * 10
    # many threads storing the same key: payload and meta always come from the same write
    def store(i):
        src = cache.staging_path(".bin")
        src.write_bytes(str(i).encode() * 100)
        cache.put_file(key, ".bin", src, {"provenance": {"source": "test", "request": str(i)}})

    th = [threading.Thread(target=store, args=(i,)) for i in range(20)]
    [t.start() for t in th]
    [t.join() for t in th]
    hit = cache.get(key, ".bin")
    req = hit.meta["provenance"]["request"]
    assert hit.payload.read_bytes() == req.encode() * 100


def test_unauthorized_detected_through_exception_chain():
    class _Resp:
        status_code = 401

    inner = Exception("boom")
    inner.response = _Resp()
    try:
        try:
            raise inner
        except Exception as e:
            raise RuntimeError("wrapped") from e
    except RuntimeError as outer:
        assert fetch._unauthorized(outer)
    assert fetch._unauthorized(Exception("401 Client Error: 401 for url: https://x"))
    assert fetch._unauthorized(Exception("job failed: HTTP 401 Unauthorized"))
    assert not fetch._unauthorized(Exception("503 Server Error"))
    assert not fetch._unauthorized(Exception("Unauthorized column access"))


def test_run_tap_relogs_once_with_saved_cookie_on_401(monkeypatch):
    """A 401 refreshes the session with the cookie loaded from disk (not the live jar, which the
    server's response may have changed), retries at once in the same mode, and only once."""
    import pyvo
    import requests

    from astrolab import gaia_auth

    calls = {"run": 0, "stale": []}

    class _Svc:
        def __init__(self, url, session=None):
            self.session = session

        def run_sync(self, q, maxrec=None):
            calls["run"] += 1
            if self.session is not None and any(c.value == "dead" for c in self.session.cookies):
                raise Exception("401 Client Error: 401 for url: https://gea.esac.esa.int/tap-server/tap/sync")
            return "ok"

    def fake_session(cookie):
        s = requests.Session()
        s.cookies.set("JSESSIONID", cookie, domain=gaia_auth.GAIA_HOST)
        s.cookies.set("JSESSIONID", "server-set", domain=gaia_auth.GAIA_HOST, path="/tap-server")
        return s

    disk = {"cookies": {"JSESSIONID": "dead"}}
    monkeypatch.setattr(pyvo.dal, "TAPService", _Svc)
    monkeypatch.setattr(gaia_auth, "load_cookies", lambda: dict(disk["cookies"]))
    monkeypatch.setattr(gaia_auth, "session_with_cookies",
                        lambda url: (fake_session(disk["cookies"]["JSESSIONID"]), dict(disk["cookies"])))

    def refresh(url, stale):
        calls["stale"].append(stale)
        disk["cookies"] = {"JSESSIONID": "fresh"}
        return fake_session("fresh"), dict(disk["cookies"])

    monkeypatch.setattr(gaia_auth, "refresh_session", refresh)
    url = "https://gea.esac.esa.int/tap-server/tap"
    assert fetch._run_tap(url, "SELECT 1", 2, "sync") == "ok"
    assert calls["stale"] == [{"JSESSIONID": "dead"}] and calls["run"] == 2
