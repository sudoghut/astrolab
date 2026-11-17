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
    import os
    for f in (hit.payload, hit.meta_path):           # older than the mtime granularity (T-035)
        os.utime(f, (1, 1))
    assert cache.prune(limit_bytes=0) == 1
    assert cache.get(key, ".bin") is None


def test_cache_json_payload_kept_apart_from_sidecar(tmp_cache):
    key = cache.key_for("t", {"j": 1})
    src = cache.staging_path(".json")
    src.write_text('{"events": {"a": 1, "b": 2}}', encoding="utf-8")
    cache.put_file(key, ".json", src, {"provenance": {"source": "test", "request": "r"}})
    hit = cache.get(key, ".json")
    assert hit and hit.payload != hit.meta_path
    assert json.loads(hit.payload.read_text(encoding="utf-8")) == {"events": {"a": 1, "b": 2}}
    assert hit.meta["provenance"]["source"] == "test"
    assert cache.info()["entries"] == 1


def test_tap_refuses_above_hard_ceiling(tmp_cache):
    with pytest.raises(fetch.TooLarge):
        fetch.tap("SELECT 1", "gaia", max_rows=config.TAP_HARD_MAX_ROWS + 1)


def test_tap_cache_hit_needs_no_network(tmp_cache):
    adql = "SELECT  a FROM t"
    key = cache.key_for("tap", {"url": fetch.tap_url("gaia"), "adql": "SELECT a FROM t"})
    tmp = cache.staging_path(".parquet")
    pd.DataFrame({"a": [1, 2]}).to_parquet(tmp)
    cache.put_file(key, ".parquet", tmp, {"provenance": {"source": "tap:gaia", "request": "SELECT a FROM t",
                                                         "sha256": fetch._sha256(tmp)}})
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

        status_code = 200

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


def test_sync_tap_streams_with_byte_cap_and_reports_errors(tmp_cache, monkeypatch):
    """Sync queries POST to <base>/sync and are streamed under the cap; HTTP errors keep the code."""
    seen = {}

    class _Resp:
        def __init__(self, code):
            self.status_code = code

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def iter_content(self, n):
            for _ in range(100):
                yield b"x" * 1000

    class _Sess:
        code = 200

        def post(self, uri, data=None, stream=True, timeout=0):
            seen.update(uri=uri, data=data)
            return _Resp(self.code)

    class _Svc:
        baseurl = "http://example.invalid/tap/"
        _session = _Sess()

    monkeypatch.setattr(config, "HTTP_MAX_BYTES", 5000)
    with pytest.raises(fetch.TooLarge):
        fetch._run_sync(_Svc(), "SELECT 1", 10)
    assert seen["uri"] == "http://example.invalid/tap/sync"
    assert seen["data"]["QUERY"] == "SELECT 1" and seen["data"]["MAXREC"] == "10"
    _Svc._session.code = 401
    with pytest.raises(RuntimeError) as e:
        fetch._run_sync(_Svc(), "SELECT 1", 10)
    assert fetch._unauthorized(e.value) and not fetch._transient(e.value)
    _Svc._session.code = 503
    with pytest.raises(RuntimeError) as e:
        fetch._run_sync(_Svc(), "SELECT TOP 500 a FROM t", 10)
    assert fetch._transient(e.value)
    _Svc._session.code = 400
    with pytest.raises(RuntimeError) as e:
        fetch._run_sync(_Svc(), "SELECT TOP 500 a FROM t", 10)
    assert not fetch._transient(e.value)


_VOT = """<?xml version="1.0"?>
<VOTABLE version="1.3" xmlns="http://www.ivoa.net/xml/VOTable/v1.3">
<RESOURCE type="results">
<INFO name="QUERY_STATUS" value="{status}">{msg}</INFO>
{table}
</RESOURCE>
{tail}
</VOTABLE>"""
_TAB = """<TABLE><FIELD name="a" datatype="int"/><DATA><TABLEDATA>
<TR><TD>1</TD></TR></TABLEDATA></DATA></TABLE>"""


def _vot_svc(body):
    class _Resp:
        status_code = 200

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def iter_content(self, n):
            yield body.encode()

    class _Sess:
        def post(self, uri, data=None, stream=True, timeout=0):
            return _Resp()

    class _Svc:
        baseurl = "http://example.invalid/tap"
        _session = _Sess()

    return _Svc()


def test_sync_tap_votable_status_handling(tmp_cache):
    ok = fetch._run_sync(_vot_svc(_VOT.format(status="OK", msg="", table=_TAB, tail="")), "q", 5)
    assert len(ok.to_table()) == 1 and ok.query_status == "OK"
    trailing = _VOT.format(status="OK", msg="", table=_TAB + '\n<INFO name="QUERY_STATUS" value="OVERFLOW"/>', tail="")
    assert fetch._run_sync(_vot_svc(trailing), "q", 5).query_status == "OVERFLOW"
    for status in ("ERROR", "error"):
        with pytest.raises(RuntimeError) as e:
            fetch._run_sync(_vot_svc(_VOT.format(status=status, msg="bad column", table="", tail="")), "q", 5)
        assert "bad column" in str(e.value) and not fetch._transient(e.value)
    with pytest.raises(RuntimeError):      # no table, no status: not an empty success
        fetch._run_sync(_vot_svc(_VOT.format(status="OK", msg="", table="", tail="")), "q", 5)


def test_cached_tap_result_over_limit_refused(tmp_cache, monkeypatch):
    key = cache.key_for("tap", {"url": fetch.tap_url("gaia"), "adql": "SELECT b FROM t"})
    tmp = cache.staging_path(".parquet")
    pd.DataFrame({"b": np.arange(20000.0)}).to_parquet(tmp)
    cache.put_file(key, ".parquet", tmp, {"provenance": {"source": "tap:gaia", "request": "SELECT b FROM t",
                                                         "sha256": fetch._sha256(tmp)}})
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
    assert "{{" not in (s.path / "README.zh.md").read_text(encoding="utf-8")
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
    for payload, rep in ((b"a" * 10, False), (b"b" * 10, False), (b"c" * 10, True)):
        src = cache.staging_path(".bin")
        src.write_bytes(payload)
        cache.put_file(key, ".bin", src, {"provenance": {"source": "test", "request": "r"}}, replace=rep)
        assert not src.exists()
        # a complete entry is kept unless replace=True (explicit refresh)
        assert cache.get(key, ".bin").payload.read_bytes() == (b"a" * 10 if not rep else b"c" * 10)
    # many threads storing the same key: payload and meta always come from the same write
    def store(i):
        src = cache.staging_path(".bin")
        src.write_bytes(str(i).encode() * 100)
        cache.put_file(key, ".bin", src, {"provenance": {"source": "test", "request": str(i)}})

    key = cache.key_for("t", {"dup": 2})
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
    monkeypatch.setattr(fetch, "_run_sync", lambda svc, q, maxrec: svc.run_sync(q, maxrec=maxrec))
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


def test_cache_read_blocks_a_concurrent_refresh(tmp_cache):
    """cache.read holds the writers' key lock: a refresh of the same key waits until the read
    (meta and payload) is finished, so they always come from the same write."""
    import threading

    key = cache.key_for("test", {"x": 1})
    assert cache.read(key, ".txt", lambda p: p.read_text()) is None

    def write(gen):
        src = cache.staging_path(".txt")
        src.write_text(str(gen))
        cache.put_file(key, ".txt", src, {"gen": gen}, replace=True)

    write(0)
    writer = threading.Thread(target=write, args=(1,))

    def reader(path):
        writer.start()
        writer.join(0.3)
        assert writer.is_alive()            # blocked on the key lock while we read
        return path.read_text()

    meta, text = cache.read(key, ".txt", reader)
    writer.join()
    assert meta["gen"] == 0 and text == "0"
    meta, text = cache.read(key, ".txt", lambda p: p.read_text())
    assert meta["gen"] == 1 and text == "1"


def test_rejected_gaia_login_not_repeated(monkeypatch, tmp_path):
    from astrolab import gaia_auth

    calls = []
    monkeypatch.setattr(gaia_auth, "_LOGIN_FAILED", False)
    monkeypatch.setattr(gaia_auth, "load_cookies", lambda: None)
    monkeypatch.setattr(gaia_auth, "credentials", lambda: ("u", "p"))

    def reject(u, p):
        calls.append(1)
        raise gaia_auth.LoginRejected("Gaia archive login failed (HTTP 401)")

    monkeypatch.setattr(gaia_auth, "_post_login", reject)
    url = "https://" + gaia_auth.GAIA_HOST + "/tap-server/tap"
    assert gaia_auth.session_with_cookies(url) == (None, None)
    assert gaia_auth.session_with_cookies(url) == (None, None)
    assert calls == [1]

    monkeypatch.setattr(gaia_auth, "_LOGIN_FAILED", False)

    def blip(u, p):
        calls.append(2)
        raise RuntimeError("Gaia archive login failed (HTTP 503)")

    monkeypatch.setattr(gaia_auth, "_post_login", blip)
    gaia_auth.session_with_cookies(url)
    gaia_auth.session_with_cookies(url)
    assert calls == [1, 2, 2]


def _fake_http(monkeypatch, body: bytes, length: int | None = None):
    import requests

    class _R:
        headers = {"Content-Length": str(len(body) if length is None else length)}

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def raise_for_status(self):
            pass

        def iter_content(self, n):
            yield body

    monkeypatch.setattr(requests, "head", lambda *a, **k: _R())
    monkeypatch.setattr(requests, "get", lambda *a, **k: _R())


def test_http_cap_cannot_be_raised_by_caller(tmp_cache, monkeypatch):
    monkeypatch.setattr(config, "HTTP_MAX_BYTES", 1000)
    _fake_http(monkeypatch, b"x" * 2000)
    with pytest.raises(ValueError, match="cap_consent"):     # no consent: refused before any request
        fetch.http("http://example.invalid/f.txt", max_bytes=10_000_000)
    with pytest.raises(fetch.TooLarge):
        fetch.http("http://example.invalid/f.txt")
    _fake_http(monkeypatch, b"x" * 2000, length=0)     # no Content-Length: the streaming check
    with pytest.raises(fetch.TooLarge):
        fetch.http("http://example.invalid/f.txt")


def test_http_cached_payload_verified_against_provenance(tmp_cache, monkeypatch):
    _fake_http(monkeypatch, b"first")
    a = fetch.http("http://example.invalid/g.txt")
    b = fetch.http("http://example.invalid/g.txt")
    assert b.from_cache and b.data.read_bytes() == b"first"
    a.data.write_bytes(b"tampered")           # bytes no longer match the stored sha256
    c = fetch.http("http://example.invalid/g.txt")
    assert not c.from_cache and c.data.read_bytes() == b"first"


def test_http_refresh_keeps_identical_file_and_updates_meta(tmp_cache, monkeypatch):
    _fake_http(monkeypatch, b"same")
    a = fetch.http("http://example.invalid/h.txt", note="one")
    ino = a.data.stat().st_ino            # read() touches mtime; the inode shows the file was kept
    b = fetch.http("http://example.invalid/h.txt", note="two", refresh=True)
    assert b.data == a.data and b.data.stat().st_ino == ino and b.provenance.note == "two"
    assert fetch.http("http://example.invalid/h.txt").provenance.note == "two"
    _fake_http(monkeypatch, b"changed")
    c = fetch.http("http://example.invalid/h.txt", refresh=True)
    assert c.data.read_bytes() == b"changed" and c.provenance.sha256 == fetch._sha256(c.data)


def test_tap_cache_hit_with_mismatched_payload_is_refetched(tmp_cache, monkeypatch):
    """Another process may leave one write's payload under another's meta: the sha256 recorded in
    the provenance must match the payload, else the entry is a miss and is fetched again."""
    class _Res:
        query_status = "OK"

        def to_table(self):
            from astropy.table import Table
            return Table({"a": [7, 8]})

    adql = "SELECT a FROM mixed"
    key = cache.key_for("tap", {"url": fetch.tap_url("gaia"), "adql": fetch._normalize_adql(adql)})
    tmp = cache.staging_path(".parquet")
    pd.DataFrame({"a": [1, 2]}).to_parquet(tmp)
    cache.put_file(key, ".parquet", tmp, {"provenance": {"source": "tap:gaia", "request": adql,
                                                         "sha256": "0" * 64}})
    monkeypatch.setattr(fetch, "_run_tap", lambda url, q, maxrec, mode: _Res())
    res = fetch.tap(adql, "gaia")
    assert not res.from_cache and list(res.data.a) == [7, 8]
    again = fetch.tap(adql, "gaia")
    assert again.from_cache and list(again.data.a) == [7, 8]


def test_prune_skips_entry_used_since_snapshot(tmp_cache, monkeypatch):
    """prune deletes an entry only under its key lock and only if it was not touched meanwhile."""
    import os

    keys = []
    for i in range(2):
        key = cache.key_for("test", {"p": i})
        src = cache.staging_path(".bin")
        src.write_bytes(b"x" * 100)
        cache.put_file(key, ".bin", src, {"provenance": {"source": "test", "request": str(i)}})
        keys.append(key)
    old = cache.get(keys[0], ".bin")
    for f in (old.payload, old.meta_path):
        os.utime(f, (1, 1))                      # oldest entry by far
    new = cache.get(keys[1], ".bin")
    for f in (new.payload, new.meta_path):
        os.utime(f, (2, 2))                      # also older than the mtime granularity (T-035)
    real = cache._entries

    def snapshot_then_touch(root):
        out = real(root)
        cache.read(keys[0], ".bin", lambda p: None)   # used after the snapshot
        return out

    monkeypatch.setattr(cache, "_entries", snapshot_then_touch)
    cache.prune(limit_bytes=1)
    assert cache.read(keys[0], ".bin", lambda p: p.read_bytes()) is not None
    assert cache.get(keys[1], ".bin") is None      # the unused entry is still pruned


def test_tap_never_requests_more_than_hard_ceiling(tmp_cache, monkeypatch):
    seen = {}

    class _Res:
        query_status = "OK"

        def to_table(self):
            from astropy.table import Table
            return Table({"a": [1]})

    def fake(url, q, maxrec, mode):
        seen["maxrec"] = maxrec
        return _Res()

    monkeypatch.setattr(fetch, "_run_tap", fake)
    fetch.tap("SELECT a FROM ceiling", "gaia", max_rows=config.TAP_HARD_MAX_ROWS)
    assert seen["maxrec"] == config.TAP_HARD_MAX_ROWS


def test_prune_keeps_entries_touched_within_mtime_granularity(tmp_cache):
    """A recently used entry is kept while an old entry can be removed instead."""
    import os

    def put(i):
        key = cache.key_for("test", {"recent": i})
        src = cache.staging_path(".bin")
        src.write_bytes(b"x" * 100)
        cache.put_file(key, ".bin", src, {"provenance": {"source": "test", "request": str(i)}})
        return key

    old, new = put(0), put(1)
    e = cache.get(old, ".bin")
    for f in (e.payload, e.meta_path):
        os.utime(f, (1, 1))
    n_new = sum(f.stat().st_size for f in (cache.get(new, ".bin").payload, cache.get(new, ".bin").meta_path))
    cache.prune(limit_bytes=n_new)                   # removing the old entry is enough
    assert cache.get(old, ".bin") is None and cache.get(new, ".bin") is not None

def test_replace_retries_then_explains(tmp_path, monkeypatch):
    import os

    calls = {"n": 0}
    os_replace = os.replace

    def flaky(a, b):
        calls["n"] += 1
        if calls["n"] < 3:
            raise PermissionError("busy")
        return os_replace(a, b)

    monkeypatch.setattr(cache.os, "replace", flaky)
    a, b = tmp_path / "a", tmp_path / "b"
    a.write_text("1")
    cache._replace(a, b)
    assert b.read_text() == "1" and calls["n"] == 3
    monkeypatch.setattr(cache.os, "replace", lambda a, b: (_ for _ in ()).throw(PermissionError("busy")))
    c = tmp_path / "c"
    c.write_text("2")
    with pytest.raises(PermissionError, match="another run may hold the file open"):
        cache._replace(c, b, tries=2)



def test_clear_removes_recent_entries(tmp_cache):
    key = cache.key_for("test", {"clear": 1})
    src = cache.staging_path(".bin")
    src.write_bytes(b"x")
    cache.put_file(key, ".bin", src, {"provenance": {"source": "test", "request": "r"}})
    assert cache.clear() == 1 and cache.get(key, ".bin") is None


def test_prune_second_pass_when_only_recent_entries_exceed(tmp_cache):
    keys = []
    for i in range(3):
        key = cache.key_for("test", {"burst": i})
        src = cache.staging_path(".bin")
        src.write_bytes(b"x" * 100)
        cache.put_file(key, ".bin", src, {"provenance": {"source": "test", "request": str(i)}})
        keys.append(key)
    assert cache.prune(limit_bytes=1) >= 1          # all recent, still over the limit: removed
    assert sum(e[1] for e in cache._entries(cache.config.cache_dir())) <= 1


def test_http_cap_needs_consent_and_records_it(tmp_cache, monkeypatch):
    monkeypatch.setattr(config, "HTTP_MAX_BYTES", 1000)
    _fake_http(monkeypatch, b"x" * 2000)
    with pytest.raises(ValueError, match="cap_consent"):
        fetch.http("http://example.invalid/big.txt", max_bytes=5000)
    with pytest.raises(ValueError, match="cap_consent"):
        fetch.http("http://example.invalid/big.txt", max_bytes=5000, cap_consent="ok")
    why = "user approved 2026-11-15 in the study log"
    r = fetch.http("http://example.invalid/big.txt", max_bytes=5000, cap_consent=why)
    assert r.data.stat().st_size == 2000 and why in r.provenance.note
    again = fetch.http("http://example.invalid/big.txt", max_bytes=5000, cap_consent=why)
    assert again.from_cache and why in again.provenance.note
    with pytest.raises(fetch.TooLarge):             # without the exception the cap still applies
        fetch.http("http://example.invalid/big.txt")


def test_http_raised_cap_is_still_enforced(tmp_cache, monkeypatch):
    monkeypatch.setattr(config, "HTTP_MAX_BYTES", 1000)
    why = "user approved 2026-11-15 in the study log"
    _fake_http(monkeypatch, b"x" * 6000)                       # HEAD reports 6000 > 5000
    with pytest.raises(fetch.TooLarge):
        fetch.http("http://example.invalid/c.txt", max_bytes=5000, cap_consent=why)
    _fake_http(monkeypatch, b"x" * 6000, length=0)             # streaming check
    with pytest.raises(fetch.TooLarge):
        fetch.http("http://example.invalid/c.txt", max_bytes=5000, cap_consent=why)
