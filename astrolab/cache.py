"""Content-addressed cache in the system cache directory.

An entry is identified by a hash of (kind, params). Each entry is a payload file
plus a ``.json`` sidecar holding metadata (incl. provenance). Total size is kept
under ``config.CACHE_LIMIT_BYTES`` by pruning least-recently-used entries.

Accepted limits (T-035, rare cases):
- One URL fetched with two suffixes shares one meta file; fetch's sha256 check turns the other
  payload into a miss (a re-download, never mismatched data), and prune, which locks one payload
  per entry, may then remove the other payload mid-read (a miss on POSIX; kept on Windows).
- The per-key lock map grows with the number of keys a process touches (small for one run).
- Every HTTP cache hit hashes its payload (at most the 50 MB per-download cap).
"""
from __future__ import annotations

import hashlib
import json
import os
import threading
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from . import config


def key_for(kind: str, params: dict[str, Any]) -> str:
    blob = json.dumps({"kind": kind, "params": params}, sort_keys=True, default=str)
    return hashlib.sha256(blob.encode()).hexdigest()[:24]


@dataclass
class Entry:
    key: str
    payload: Path
    meta_path: Path

    @property
    def meta(self) -> dict[str, Any]:
        return json.loads(self.meta_path.read_text(encoding="utf-8"))

    def touch(self) -> None:
        """Mark as recently used (mtime drives LRU pruning)."""
        for p in (self.payload, self.meta_path):
            if p.exists():
                p.touch()


def _paths(key: str, suffix: str, root: Path | None = None) -> tuple[Path, Path]:
    root = root or config.cache_dir()
    sub = root / key[:2]
    if suffix.lower() == ".json":  # a JSON payload must not share its name with the metadata sidecar
        suffix = ".payload.json"
    return sub / f"{key}{suffix}", sub / f"{key}.json"


def get(key: str, suffix: str, root: Path | None = None) -> Entry | None:
    """Unlocked lookup (existence only). To read an entry use read(), which pairs meta and payload
    from one write."""
    payload, meta = _paths(key, suffix, root)
    if payload.exists() and meta.exists():
        entry = Entry(key, payload, meta)
        entry.touch()
        return entry
    return None


_KEY_LOCKS: dict[str, threading.Lock] = {}
_KEY_LOCKS_GUARD = threading.Lock()


def _key_lock(path: Path) -> threading.Lock:
    with _KEY_LOCKS_GUARD:
        return _KEY_LOCKS.setdefault(str(path), threading.Lock())


def read(key: str, suffix: str, reader, root: Path | None = None):
    """Read one cache entry consistently: under the same per-key lock as writers, return
    (meta, reader(payload_path)), or None on a miss. A refresh of the same key in another thread
    cannot then pair one write's metadata with another write's payload while it is read. The locks
    are per process: separate processes refreshing the same key are not serialised and may leave a
    payload under the other's meta, so callers check the payload against the sha256 in its
    provenance (fetch.tap and fetch.http do) and treat a mismatch as a miss. An entry pruned
    meanwhile is a miss."""
    payload, meta_path = _paths(key, suffix, root)
    with _key_lock(payload):
        if not (payload.exists() and meta_path.exists()):
            return None
        entry = Entry(key, payload, meta_path)
        try:
            entry.touch()                     # most recently used before the read: prune skips it
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            value = reader(payload)
        except FileNotFoundError:
            return None
        return meta, value


MTIME_GRANULARITY_S = 2.0      # FAT/exFAT and some network or synced drives store mtime in 2 s steps


def _retry(op, what: str, tries: int = 6) -> None:
    """Run a file operation, retried for about 1.5 s when Windows refuses (another process holding
    the file open, an indexer or antivirus); the last failure keeps its cause in the message."""
    for i in range(tries):
        try:
            op()
            return
        except PermissionError as exc:
            if i == tries - 1:
                raise PermissionError(f"cache {what} refused ({exc}); another run may hold the file "
                                      "open: close it and fetch again") from exc
            time.sleep(0.05 * 2 ** i)


def _replace(src: Path, dst: Path, tries: int = 6) -> None:
    _retry(lambda: os.replace(src, dst), f"replace of {dst.name}", tries)


def put_file(key: str, suffix: str, src: Path, meta: dict[str, Any], root: Path | None = None,
             replace: bool = False, same_payload=None) -> Entry:
    """Store `src` (moved) with its meta. A complete entry already stored under `key` (for example
    by another thread that ran the identical query) is kept and `src` is discarded, so a stored
    payload and its meta are never modified implicitly and always come from one write; only
    `replace=True` (an explicit refresh) overwrites, removing the old meta first so readers miss
    the entry while it is rewritten. With `replace=True`, `same_payload(stored_path) -> bool` is
    called under the key lock; when it is true the stored payload is kept (a path a caller holds is
    not replaced) and only the meta is rewritten. Callers read the stored entry back with read()."""
    payload, meta_path = _paths(key, suffix, root)
    payload.parent.mkdir(parents=True, exist_ok=True)
    with _key_lock(payload):                 # one writer per key within the process
        if (replace and same_payload is not None and payload.exists() and meta_path.exists()
                and same_payload(payload)):
            Path(src).unlink(missing_ok=True)
            tmp_meta = staging_path(".json", root)
            try:
                tmp_meta.write_text(json.dumps(meta, indent=2, default=str), encoding="utf-8")
                _replace(tmp_meta, meta_path)
            finally:
                tmp_meta.unlink(missing_ok=True)
        else:
            _store(Path(src), payload, meta, meta_path, root, replace)
    prune(root=root)
    return Entry(key, payload, meta_path)


def _store(src: Path, payload: Path, meta: dict[str, Any], meta_path: Path, root: Path | None,
           replace: bool) -> None:
    if not replace and payload.exists() and meta_path.exists():
        src.unlink(missing_ok=True)          # keep the complete pair already stored
        return
    try:
        # get() needs both files: without a meta file the entry is invisible while it is written
        _retry(lambda: meta_path.unlink(missing_ok=True), f"removal of {meta_path.name}")
        # if the payload replace finally fails, the old payload is left without its meta: the entry
        # is invisible (a miss) and the next fetch rewrites it; prune removes the orphan
        _replace(src, payload)
        tmp_meta = staging_path(".json", root)
        try:
            tmp_meta.write_text(json.dumps(meta, indent=2, default=str), encoding="utf-8")
            _replace(tmp_meta, meta_path)
        except BaseException:
            tmp_meta.unlink(missing_ok=True)
            payload.unlink(missing_ok=True)  # no payload without its own meta
            raise
    finally:
        src.unlink(missing_ok=True)


def staging_path(suffix: str, root: Path | None = None) -> Path:
    root = root or config.cache_dir()
    tmp = root / "_staging"
    tmp.mkdir(parents=True, exist_ok=True)
    # unique per call: time_ns alone collides between threads on Windows' coarse clock
    return tmp / f"{time.time_ns()}-{uuid.uuid4().hex}{suffix}"


def _entries(root: Path) -> list[tuple[float, int, list[Path]]]:
    groups: dict[str, list[Path]] = {}
    for p in root.glob("??/*"):
        groups.setdefault(p.name.split(".")[0], []).append(p)
    out = []
    for files in groups.values():
        try:                      # another thread may prune or replace files meanwhile
            stats = [f.stat() for f in files]
        except OSError:
            continue
        out.append((max(s.st_mtime for s in stats), sum(s.st_size for s in stats), files))
    return out


def info(root: Path | None = None) -> dict[str, Any]:
    root = root or config.cache_dir()
    entries = _entries(root)
    return {
        "path": str(root),
        "entries": len(entries),
        "size_mb": round(sum(e[1] for e in entries) / 1024**2, 2),
        "limit_mb": round(config.CACHE_LIMIT_BYTES / 1024**2),
    }


def prune(limit_bytes: int | None = None, root: Path | None = None, keep_recent: bool = True) -> int:
    """Delete LRU entries until total size <= limit. Returns number removed. With keep_recent, an
    entry used within MTIME_GRANULARITY_S before the prune started is kept (so the cache can exceed
    the limit by what was written in the last ~2 s until the next prune); clear() does not keep it."""
    root = root or config.cache_dir()
    limit = config.CACHE_LIMIT_BYTES if limit_bytes is None else limit_bytes
    started = time.time()
    entries = sorted(_entries(root))  # oldest first
    total = sum(e[1] for e in entries)
    removed = 0
    for mtime, size, files in entries:
        if total <= limit:
            break
        # under the entry's key lock (as read() and put_file() take it), and only if nobody has
        # used the entry since the snapshot: an entry being read or just stored is never deleted
        payload = next((f for f in files if not (f.name.endswith(".json")
                                                 and not f.name.endswith(".payload.json"))), files[0])
        with _key_lock(payload):
            try:
                newest = max(f.stat().st_mtime for f in files if f.exists())
                # used since the snapshot, or so recently that a coarse mtime cannot tell (T-035);
                # an mtime in the future (clock set back) does not protect an entry for ever
                recent = keep_recent and started - MTIME_GRANULARITY_S <= newest <= started + MTIME_GRANULARITY_S
                if newest > mtime or recent:
                    continue
            except (OSError, ValueError):         # removed meanwhile: no longer counts
                total -= size
                continue
            kept = False
            for f in files:
                try:
                    f.unlink(missing_ok=True)
                except PermissionError:   # open in another process (Windows): left for a later prune
                    kept = True
        if kept:                          # still on disk: does not reduce the total
            continue
        total -= size
        removed += 1
    return removed


def clear(root: Path | None = None) -> int:
    """Remove every entry (explicit: recently used entries are not kept)."""
    return prune(limit_bytes=0, root=root, keep_recent=False)
