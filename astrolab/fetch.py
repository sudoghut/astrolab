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


def _transient(exc: Exception) -> bool:
    text = str(exc)
    return any(code in text for code in ("500", "502", "503", "504", "timed out", "Connection"))


def _run_tap(url: str, query: str, maxrec: int, mode: str):
    """Run a TAP query, retrying transient server errors and falling back sync -> async."""
    import time

    import pyvo  # imported lazily: slow import

    svc = pyvo.dal.TAPService(url)
    modes = [mode] + (["async"] if mode == "sync" else [])
    last: Exception | None = None
    for attempt, delay in enumerate((0,) + RETRY_DELAYS):
        if delay:
            print(f"  TAP transient error ({last}); retry {attempt}/{len(RETRY_DELAYS)} in {delay}s")
            time.sleep(delay)
        m = modes[min(attempt, len(modes) - 1)] if attempt < 2 else modes[-1]
        try:
            return svc.run_async(query, maxrec=maxrec) if m == "async" else svc.run_sync(query, maxrec=maxrec)
        except Exception as exc:  # pyvo raises several DAL* types
            if not _transient(exc):
                raise
            last = exc
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

    if not refresh and (hit := cache.get(key, ".parquet")):
        meta = hit.meta
        prov = Provenance(**meta["provenance"])
        return Fetched(pd.read_parquet(hit.payload), prov, True)

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
    prov = Provenance(
        source=f"tap:{service}", request=query, release=release, rows=len(df),
        bytes=tmp.stat().st_size, sha256=_sha256(tmp), cache_key=key, note=note,
    )
    cache.put_file(key, ".parquet", tmp, {"provenance": prov.to_dict()})
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
    max_bytes = max_bytes or config.HTTP_MAX_BYTES
    suffix = suffix or (Path(url.split("?")[0]).suffix or ".bin")
    key = cache.key_for("http", {"url": url})

    if not refresh and (hit := cache.get(key, suffix)):
        return Fetched(hit.payload, Provenance(**hit.meta["provenance"]), True)

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
    entry = cache.put_file(key, suffix, tmp, {"provenance": prov.to_dict()})
    return Fetched(entry.payload, prov, False)
