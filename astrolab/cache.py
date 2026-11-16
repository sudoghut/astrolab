"""Content-addressed cache in the system cache directory.

An entry is identified by a hash of (kind, params). Each entry is a payload file
plus a ``.json`` sidecar holding metadata (incl. provenance). Total size is kept
under ``config.CACHE_LIMIT_BYTES`` by pruning least-recently-used entries.
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
    return sub / f"{key}{suffix}", sub / f"{key}.json"


def get(key: str, suffix: str, root: Path | None = None) -> Entry | None:
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


def put_file(key: str, suffix: str, src: Path, meta: dict[str, Any], root: Path | None = None,
             replace: bool = False) -> Entry:
    """Store `src` (moved) with its meta. A complete entry already stored under `key` (for example
    by another thread that ran the identical query) is kept and `src` is discarded, so a stored
    payload and its meta are never modified implicitly and always come from one write; only
    `replace=True` (an explicit refresh) overwrites, removing the old meta first so readers miss
    the entry while it is rewritten."""
    payload, meta_path = _paths(key, suffix, root)
    payload.parent.mkdir(parents=True, exist_ok=True)
    with _key_lock(payload):                 # one writer per key within the process
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
        meta_path.unlink(missing_ok=True)
        os.replace(src, payload)
        tmp_meta = staging_path(".json", root)
        try:
            tmp_meta.write_text(json.dumps(meta, indent=2, default=str), encoding="utf-8")
            os.replace(tmp_meta, meta_path)
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


def prune(limit_bytes: int | None = None, root: Path | None = None) -> int:
    """Delete LRU entries until total size <= limit. Returns number removed."""
    root = root or config.cache_dir()
    limit = config.CACHE_LIMIT_BYTES if limit_bytes is None else limit_bytes
    entries = sorted(_entries(root))  # oldest first
    total = sum(e[1] for e in entries)
    removed = 0
    for _, size, files in entries:
        if total <= limit:
            break
        for f in files:
            try:
                f.unlink(missing_ok=True)
            except PermissionError:   # open in another thread (Windows): left for a later prune
                pass
        total -= size
        removed += 1
    return removed


def clear(root: Path | None = None) -> int:
    return prune(limit_bytes=0, root=root)
