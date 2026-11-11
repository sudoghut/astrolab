"""Content-addressed cache in the system cache directory.

An entry is identified by a hash of (kind, params). Each entry is a payload file
plus a ``.json`` sidecar holding metadata (incl. provenance). Total size is kept
under ``config.CACHE_LIMIT_BYTES`` by pruning least-recently-used entries.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import time
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


def put_file(key: str, suffix: str, src: Path, meta: dict[str, Any], root: Path | None = None) -> Entry:
    payload, meta_path = _paths(key, suffix, root)
    payload.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), payload)
    meta_path.write_text(json.dumps(meta, indent=2, default=str), encoding="utf-8")
    prune(root=root)
    return Entry(key, payload, meta_path)


def staging_path(suffix: str, root: Path | None = None) -> Path:
    root = root or config.cache_dir()
    tmp = root / "_staging"
    tmp.mkdir(parents=True, exist_ok=True)
    return tmp / f"{time.time_ns()}{suffix}"


def _entries(root: Path) -> list[tuple[float, int, list[Path]]]:
    groups: dict[str, list[Path]] = {}
    for p in root.glob("??/*"):
        groups.setdefault(p.name.split(".")[0], []).append(p)
    out = []
    for files in groups.values():
        atime = max(f.stat().st_mtime for f in files)
        size = sum(f.stat().st_size for f in files)
        out.append((atime, size, files))
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
            f.unlink(missing_ok=True)
        total -= size
        removed += 1
    return removed


def clear(root: Path | None = None) -> int:
    return prune(limit_bytes=0, root=root)
