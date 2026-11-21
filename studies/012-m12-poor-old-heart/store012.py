"""Checkpoints of study 012 (outside the project folder) and the pause guard.

Every tunable arrives as an argument; this module never imports run.
"""
from __future__ import annotations

import hashlib
import os
import pickle
import shutil
import time
from pathlib import Path


def replace_with_retry(src, dst, tries=5, wait=0.2):
    """os.replace with retries: on Windows a scanner or sync client can hold the file briefly."""
    for i in range(tries):
        try:
            os.replace(src, dst)
            return
        except PermissionError:
            if i == tries - 1:
                raise
            time.sleep(wait * (2 ** i))


CRLF, LF = chr(13) + chr(10), chr(10)


class Paused(Exception):
    """Raised when the run's time budget is used up; rerunning continues from the checkpoints."""


class Store:
    def __init__(self, root: Path, key: str, stop_after_s: float | None = None):
        self.dir = Path(root) / key
        self.dir.mkdir(parents=True, exist_ok=True)
        self.t0 = time.time()
        self.stop_after_s = stop_after_s
        self.computed = 0

    def _p(self, name):
        return self.dir / f"{name}.pkl"

    def has(self, name):
        return self._p(name).exists()

    def get(self, name, default=None):
        p = self._p(name)
        if not p.exists():
            return default
        with open(p, "rb") as f:
            return pickle.load(f)

    def put(self, name, obj):
        p = self._p(name)
        tmp = p.with_suffix(".tmp")
        with open(tmp, "wb") as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
        replace_with_retry(tmp, p)

    def check_time(self, where=""):
        # at least one unit is computed per run, so a short time budget still makes progress
        if self.stop_after_s is not None and self.computed and time.time() - self.t0 > self.stop_after_s:
            raise Paused(f"time budget used up at {where}; rerun to continue from {self.dir}")

    def cached(self, name, fn):
        """Return the stored value of `name`, computing and storing it if missing."""
        if self.has(name):
            return self.get(name)
        self.check_time(name)
        val = fn()
        self.put(name, val)
        self.computed += 1
        return val

    def size_bytes(self):
        return sum(f.stat().st_size for f in self.dir.glob("*") if f.is_file())

    def remove_all(self):
        shutil.rmtree(self.dir, ignore_errors=True)
        return not self.dir.exists()


class NullStore(Store):
    """No checkpoints (unit tests)."""

    def __init__(self, stop_after_s=None):
        self.dir = Path(".")
        self.computed = 0
        self.t0 = time.time()
        self.stop_after_s = stop_after_s
        self._mem = {}

    def has(self, name):
        return name in self._mem

    def get(self, name, default=None):
        return self._mem.get(name, default)

    def put(self, name, obj):
        self._mem[name] = obj

    def size_bytes(self):
        return 0

    def remove_all(self):
        self._mem.clear()
        return True


def source_without_assignment(path, name="PARAMS") -> bytes:
    """A module's source with the top-level `name = ...` assignment removed (its values enter the key
    separately, minus the run-only keys), so resetting a run-only flag in the file keeps the key."""
    import ast
    text = Path(path).read_text(encoding="utf-8").replace(CRLF, LF)
    tree = ast.parse(text)
    lines = text.split(LF)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            del lines[node.lineno - 1:node.end_lineno]
            break
    return LF.join(lines).encode()


def checkpoint_key(params: dict, sources: list, data_ids: list, params_source=None) -> str:
    h = hashlib.sha256()
    h.update(repr(sorted((k, repr(v)) for k, v in params.items())).encode())
    if params_source is not None:
        h.update(source_without_assignment(params_source))
    for p in sources:
        h.update(Path(p).read_text(encoding="utf-8").replace(CRLF, LF).encode())
    for s in data_ids:
        h.update(str(s).encode())
    return h.hexdigest()[:20]
