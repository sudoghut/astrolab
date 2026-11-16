"""Guarded, cached data access.

Two entry points:

- ``tap(adql, service=...)``: run an ADQL query on a public TAP service. Results
  are capped at ``max_rows``; if the cap is reached the query is *refused*
  (``TooLarge``), never silently truncated. Push filtering and aggregation to
  the server (WHERE, GROUP BY healpix, TOP) instead of raising the cap.
- ``http(url)``: download a file, refusing anything above ``max_bytes``.

Both cache results in the system cache directory and return provenance.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import requests

from . import cache, config
from .provenance import Provenance
from .services import tap_url


class TooLarge(RuntimeError):
    """Raised when a request would exceed the project's resource limits."""


@dataclass
class Fetched:
    data: Any                 # pandas.DataFrame for tap(), Path for http()
    provenance: Provenance
    from_cache: bool


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _normalize_adql(adql: str) -> str:
    return " ".join(adql.split())


def _to_frame(table) -> pd.DataFrame:
    df = table.to_pandas()
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].map(lambda v: v.decode() if isinstance(v, bytes) else v)
    return df


RETRY_DELAYS = (5, 20, 60)  # seconds between attempts on transient server errors


class _TapHTTPError(RuntimeError):
    """HTTP error from a streamed TAP request; ``code`` is the status (read by _unauthorized)."""

    def __init__(self, code: int, detail: str):
        super().__init__(f"TAP HTTP {code}: {detail}")
        self.code = code


class _TapQueryError(RuntimeError):
    """The service answered with QUERY_STATUS=ERROR (or no result table): never transient."""


def _transient(exc: Exception) -> bool:
    if isinstance(exc, _TapQueryError):
        return False
    if isinstance(exc, _TapHTTPError):
        return exc.code >= 500
    text = str(exc)
    return any(code in text for code in ("500", "502", "503", "504", "timed out", "Connection"))


class _VOResult:
    """Minimal stand-in for pyvo's result: to_table() and query_status."""

    def __init__(self, table, status):
        self._table, self.query_status = table, status

    def to_table(self):
        return self._table


def _download_votable(svc, uri: str, data: dict | None = None):
    """Stream a VOTable with the per-download byte cap enforced during transfer.

    GET for an async job's result URI; POST with ``data`` for a synchronous query, so that a sync
    result is never buffered whole before its size is checked.
    """
    from astropy.io import votable

    session = getattr(svc, "_session", None)
    if session is None:
        import requests
        session = requests.Session()
    tmp = cache.staging_path(".xml")
    written = 0
    try:
        req = (session.post(uri, data=data, stream=True, timeout=600) if data is not None
               else session.get(uri, stream=True, timeout=600))
        with req as r:
            if r.status_code >= 400:
                # keep the code in the message: _unauthorized and _transient read it
                import re

                body = b"".join(c for _, c in zip(range(4), r.iter_content(4096))).decode("utf-8", "replace")
                m = re.search(r'<INFO\b[^>]*name="QUERY_STATUS"[^>]*?(?:/>|>(.*?)</INFO>)', body, re.S | re.I)
                detail = ((m.group(1) or "").strip() if m else body)[:500] or body[:500]
                raise _TapHTTPError(r.status_code, detail)
            with open(tmp, "wb") as fh:
                for chunk in r.iter_content(1 << 16):
                    written += len(chunk)
                    if written > config.HTTP_MAX_BYTES:
                        raise TooLarge(f"TAP result exceeded {config.HTTP_MAX_BYTES / 1024**2:.0f} MB while "
                                       "downloading; narrow the query.")
                    fh.write(chunk)
        vot = votable.parse(str(tmp))
        res = _results_resource(vot)
        status, message = _query_status(vot, res)
        if status is not None and status.lower() not in ("ok", "overflow"):
            raise _TapQueryError(f"TAP query error ({status}): {message or 'no error message'}")
        if res is None or not res.tables:
            # a real zero-row result still has a TABLE element: never cache this as empty
            raise _TapQueryError(f"TAP response has no result table: {message or 'no message'}")
        table = res.tables[0].to_table(use_names_over_ids=True)
        return _VOResult(table, status.upper() if status else None)
    finally:
        tmp.unlink(missing_ok=True)


def _results_resource(vot):
    """The RESOURCE of type "results", else the first RESOURCE, else None."""
    return next((r for r in vot.resources if (r.type or "").lower() == "results"),
                vot.resources[0] if vot.resources else None)


def _query_status(vot, res):
    """(QUERY_STATUS value, message) as pyvo finds it: the results RESOURCE, then the first TABLE,
    then the VOTABLE root; the last match within a list wins (a trailing OVERFLOW counts)."""
    def scan(infos):
        found = None
        for info in infos:
            if (info.name or "").lower() == "query_status":
                found = (info.value, info.content)
        return found

    places = []
    if res is not None:
        places.append(res.infos)
        if res.tables:
            places.append(res.tables[0].infos)
    places.append(vot.infos)
    for infos in places:
        hit = scan(infos)
        if hit is not None:
            return hit
    return None, None


def _run_async(svc, query: str, maxrec: int):
    """Async TAP job that reports the server's own error message when the job fails."""
    job = svc.submit_job(query, maxrec=maxrec)
    try:
        import time as _time

        job.run()
        t0 = _time.time()
        delay = 2.0
        while True:
            phase = job.phase
            if phase not in ("PENDING", "QUEUED", "EXECUTING", "HELD", "SUSPENDED", "UNKNOWN"):
                break
            if _time.time() - t0 > 3600:
                raise RuntimeError("TAP async job still running after 3600 s")
            _time.sleep(delay)
            delay = min(delay * 1.5, 30.0)
        if phase != "COMPLETED":
            msg = None
            try:
                summary = job.job.errorsummary
                msg = summary.message.content if summary is not None and summary.message is not None else None
            except Exception:  # noqa: BLE001 - best effort
                msg = None
            # the job ran and failed (bad query, aborted): not a transient server error
            raise _TapQueryError(f"TAP async job {phase}: {msg or 'no error message'}")
        return _download_votable(svc, job.result_uri)
    finally:
        try:
            job.delete()
        except Exception:  # noqa: BLE001
            pass


def _run_sync(svc, query: str, maxrec: int):
    """Synchronous TAP query, streamed through the byte-capped download (not pyvo's run_sync,
    which reads the whole response into memory before any size check)."""
    data = {"REQUEST": "doQuery", "LANG": "ADQL", "QUERY": query}   # same parameters as pyvo
    if maxrec is not None:
        data["MAXREC"] = str(int(maxrec))
    return _download_votable(svc, svc.baseurl.rstrip("/") + "/sync", data=data)


def _unauthorized(exc: Exception) -> bool:
    """HTTP 401 from the TAP server (pyvo wraps the requests error; check the chain and message)."""
    e: BaseException | None = exc
    while e is not None:
        resp = getattr(e, "response", None)
        msg = str(e)
        if (getattr(resp, "status_code", None) == 401 or getattr(e, "code", None) == 401
                or "401 Client Error" in msg or "HTTP 401" in msg or "401 Unauthorized" in msg):
            return True
        e = e.__cause__ or e.__context__
    return False


def _run_tap(url: str, query: str, maxrec: int, mode: str):
    """Run a TAP query, retrying transient server errors and falling back sync -> async."""
    import time

    import pyvo  # imported lazily: slow import

    from . import gaia_auth

    # the user's own Gaia login, if any (longer job limits), with the saved cookie it was built from
    session, saved = gaia_auth.session_with_cookies(url)
    svc = pyvo.dal.TAPService(url, session=session) if session is not None else pyvo.dal.TAPService(url)
    modes = [mode] + (["async"] if mode == "sync" else [])
    last: Exception | None = None
    relogged = False
    for attempt, delay in enumerate((0,) + RETRY_DELAYS):
        if delay:
            print(f"  TAP transient error ({type(last).__name__}: {str(last)[:200]}); retry {attempt}/{len(RETRY_DELAYS)} in {delay}s")
            time.sleep(delay)
        m = modes[min(attempt, len(modes) - 1)] if attempt < 2 else modes[-1]
        while True:   # runs at most twice: once more after a single re-login on HTTP 401
            try:
                if m == "async":
                    return _run_async(svc, query, maxrec)
                return _run_sync(svc, query, maxrec)
            except Exception as exc:  # pyvo raises several DAL* types
                if session is not None and not relogged and _unauthorized(exc):
                    # saved Gaia cookie no longer valid (e.g. after an archive restart): drop it,
                    # log in again once from configured credentials (else anonymous), retry now
                    relogged = True
                    session.close()
                    session, saved = gaia_auth.refresh_session(url, saved)
                    svc = (pyvo.dal.TAPService(url, session=session) if session is not None
                           else pyvo.dal.TAPService(url))
                    print("  TAP 401 with the saved Gaia session; " +
                          ("logged in again, retrying" if session is not None else "continuing anonymously"))
                    continue
                if not _transient(exc):
                    raise
                last = exc
                break
    raise RuntimeError(f"TAP service {url} kept failing: {last}")


def tap(
    adql: str,
    service: str = "gaia",
    *,
    max_rows: int | None = None,
    release: str | None = None,
    mode: str = "sync",
    refresh: bool = False,
    note: str | None = None,
) -> Fetched:
    max_rows = max_rows or config.TAP_DEFAULT_MAX_ROWS
    if max_rows > config.TAP_HARD_MAX_ROWS:
        raise TooLarge(
            f"max_rows={max_rows:,} exceeds hard ceiling {config.TAP_HARD_MAX_ROWS:,}. "
            "Aggregate server-side (GROUP BY, healpix index) or narrow the selection."
        )
    query = _normalize_adql(adql)
    url = tap_url(service)
    key = cache.key_for("tap", {"url": url, "adql": query})

    def _read_parquet(path: Path):
        if path.stat().st_size > config.HTTP_MAX_BYTES:
            raise TooLarge(f"cached TAP result {path.stat().st_size / 1024**2:.1f} MB exceeds the "
                           "per-download limit; narrow the query (or clear this entry deliberately).")
        return pd.read_parquet(path)

    if not refresh and (hit := cache.read(key, ".parquet", _read_parquet)):
        meta, df = hit
        prov = Provenance(**meta["provenance"])
        if int(df.memory_usage(deep=True).sum()) > config.HTTP_MAX_BYTES:
            raise TooLarge("cached TAP result exceeds the per-download limit in memory; narrow the query.")
        return Fetched(df, prov, True)

    result = _run_tap(url, query, max_rows + 1, mode)
    table = result.to_table()
    if len(table) > max_rows or getattr(result, "query_status", None) == "OVERFLOW":
        raise TooLarge(
            f"Query returned more than max_rows={max_rows:,} rows and was refused. "
            "Aggregate server-side or narrow the WHERE clause; raise max_rows only deliberately."
        )

    df = _to_frame(table)
    tmp = cache.staging_path(".parquet")
    df.to_parquet(tmp, index=False)
    mem = int(df.memory_usage(deep=True).sum())
    stored = tmp.stat().st_size
    if max(stored, mem) > config.HTTP_MAX_BYTES:
        tmp.unlink(missing_ok=True)
        raise TooLarge(
            f"TAP result is {max(stored, mem) / 1024**2:.1f} MB "
            f"> per-download limit {config.HTTP_MAX_BYTES / 1024**2:.0f} MB; narrow the query."
        )
    prov = Provenance(
        source=f"tap:{service}", request=query, release=release, rows=len(df),
        bytes=tmp.stat().st_size, sha256=_sha256(tmp), cache_key=key, note=note,
    )
    cache.put_file(key, ".parquet", tmp, {"provenance": prov.to_dict()}, replace=refresh)
    return Fetched(df, prov, False)


def tap_count(from_where: str, service: str = "gaia", *, refresh: bool = False) -> int:
    """Row count of ``SELECT ... FROM <from_where>`` computed on the server.

    Use before fetching a selection of unknown size, e.g.
    ``tap_count("gaiadr3.gaia_source WHERE parallax > 5 AND ruwe < 1.4")``.
    """
    res = tap(f"SELECT COUNT(*) AS n FROM {from_where}", service, max_rows=1, refresh=refresh,
              note="row-count estimate")
    return int(res.data["n"].iloc[0])


def http(
    url: str,
    *,
    release: str | None = None,
    max_bytes: int | None = None,
    suffix: str | None = None,
    refresh: bool = False,
    note: str | None = None,
) -> Fetched:
    # a caller may lower the per-download cap, never raise it (AGENTS.md section 1)
    max_bytes = min(max_bytes or config.HTTP_MAX_BYTES, config.HTTP_MAX_BYTES)
    suffix = suffix or (Path(url.split("?")[0]).suffix or ".bin")
    key = cache.key_for("http", {"url": url})

    # The caller reads the returned path later. Under the key lock the file is checked against its
    # provenance sha256 (a mismatch is a miss and is downloaded again) and against the size cap; a
    # refresh that fetches identical bytes keeps the stored file (put_file same_payload), so a path
    # in use is replaced only when the server's content changed during a refresh in this process.
    def _verified(p: Path):
        if p.stat().st_size > max_bytes:
            raise TooLarge(f"cached {url} is {p.stat().st_size / 1024**2:.1f} MB > limit "
                           f"{max_bytes / 1024**2:.0f} MB.")
        return p, _sha256(p)

    def _consistent(hit):
        if hit is None:
            return None
        meta, (path, digest) = hit
        return (path, Provenance(**meta["provenance"])) if digest == meta["provenance"].get("sha256") else None

    if not refresh and (ok := _consistent(cache.read(key, suffix, _verified))):
        return Fetched(ok[0], ok[1], True)
    if not refresh and cache.get(key, suffix) is not None:
        refresh = True                       # stored bytes do not match their provenance

    head = requests.head(url, allow_redirects=True, timeout=30)
    size = int(head.headers.get("Content-Length", 0) or 0)
    if size > max_bytes:
        raise TooLarge(f"{url} is {size / 1024**2:.1f} MB > limit {max_bytes / 1024**2:.0f} MB.")

    tmp = cache.staging_path(suffix)
    written = 0
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(1 << 16):
                written += len(chunk)
                if written > max_bytes:
                    f.close()
                    tmp.unlink(missing_ok=True)
                    raise TooLarge(f"{url} exceeded {max_bytes / 1024**2:.0f} MB while downloading.")
                f.write(chunk)

    prov = Provenance(
        source="http", request=url, release=release, bytes=written,
        sha256=_sha256(tmp), cache_key=key, note=note,
    )
    entry = cache.put_file(key, suffix, tmp, {"provenance": prov.to_dict()}, replace=refresh,
                           same_payload=lambda p: _sha256(p) == prov.sha256)
    # return what is stored now (another thread's complete entry may have been kept), with its
    # own provenance, so the path and the provenance always describe the same bytes
    if ok := _consistent(cache.read(key, suffix, _verified)):
        return Fetched(ok[0], ok[1], False)
    return Fetched(entry.payload, prov, False)
