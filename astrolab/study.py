"""Studies: one folder per research question under ``studies/``.

Layout of a study folder::

    NNN-slug/
      study.yaml      machine-readable metadata (title, level, status, claims)
      README.md       question, hypothesis, criteria, method (written BEFORE running)
      log.md          research log: what was done, found, and abandoned
      run.py          defines main(ctx); deterministic, re-runnable
      test_*.py       assertions that the study's conclusions still hold
      results/        small JSON outputs + provenance.json (committed)
      web/index.html  visualization page reading ../results/*.json
"""
from __future__ import annotations

import importlib.util
import re
import shutil
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from . import config, fetch
from .provenance import ProvenanceLog, now_iso
from .results import summarize, write_json

STATUSES = ("planned", "active", "reproduced", "concluded", "paused", "abandoned")
LEVELS = ("L0", "L1", "L2", "L3", "L4", "X")


@dataclass
class Study:
    path: Path

    @property
    def id(self) -> str:
        return self.path.name

    @property
    def number(self) -> int | None:
        m = re.match(r"(\d+)-", self.id)
        return int(m.group(1)) if m else None

    @property
    def meta(self) -> dict[str, Any]:
        f = self.path / "study.yaml"
        if not f.exists():
            return {}
        return yaml.safe_load(f.read_text(encoding="utf-8")) or {}

    @property
    def results_dir(self) -> Path:
        return self.path / "results"


def discover() -> list[Study]:
    if not config.STUDIES.exists():
        return []
    dirs = [p for p in config.STUDIES.iterdir() if p.is_dir() and not p.name.startswith(("_", "."))]
    return sorted((Study(p) for p in dirs), key=lambda s: (s.number is None, s.number or 0, s.id))


def resolve(name: str) -> Study:
    """Accept a path, a folder name, a number ('3' / '003') or a unique substring."""
    p = Path(name)
    if p.is_dir() and (p / "run.py").exists():
        return Study(p.resolve())
    studies = discover()
    if name.isdigit():
        hits = [s for s in studies if s.number == int(name)]
    else:
        hits = [s for s in studies if s.id == name] or [s for s in studies if name in s.id]
    if len(hits) != 1:
        raise SystemExit(f"Study {name!r} matched {len(hits)} studies: {[s.id for s in hits]}")
    return hits[0]


def next_number() -> int:
    nums = [s.number for s in discover() if s.number is not None]
    return max(nums, default=-1) + 1


def new(slug: str, title: str, level: str = "L0") -> Study:
    slug = re.sub(r"[^a-z0-9]+", "-", slug.lower()).strip("-")
    if level not in LEVELS:
        raise SystemExit(f"level must be one of {LEVELS}")
    dest = config.STUDIES / f"{next_number():03d}-{slug}"
    shutil.copytree(config.TEMPLATE, dest)
    for f in dest.rglob("*"):
        if f.is_file() and f.suffix in {".md", ".yaml", ".py", ".html"}:
            text = f.read_text(encoding="utf-8")
            text = (text.replace("{{TITLE}}", title).replace("{{ID}}", dest.name)
                        .replace("{{LEVEL}}", level).replace("{{DATE}}", now_iso()[:10]))
            f.write_text(text, encoding="utf-8")
    return Study(dest)


class Context:
    """Handed to a study's ``main(ctx)``. Fetches are cached and provenance-logged."""

    def __init__(self, study: Study, refresh: bool = False) -> None:
        self.study = study
        self.path = study.path
        self.results = study.results_dir
        self.refresh = refresh
        self.provenance = ProvenanceLog()
        self.saved: list[str] = []
        self.bytes_in = 0

    def _charge(self, nbytes: int | None, what: str) -> None:
        """Enforce the per-run input budget (AGENTS.md section 1)."""
        self.bytes_in += nbytes or 0
        if self.bytes_in > config.STUDY_BUDGET_BYTES:
            raise fetch.TooLarge(
                f"Study input budget exceeded after {what}: {self.bytes_in / 1024**2:.1f} MB > "
                f"{config.STUDY_BUDGET_BYTES / 1024**2:.0f} MB. Narrow or aggregate server-side; "
                "ask the user before raising the budget."
            )

    def count(self, from_where: str, service: str = "gaia") -> int:
        n = fetch.tap_count(from_where, service, refresh=self.refresh)
        self.log(f"count:{service} -> {n:,} rows")
        return n

    def tap(self, adql: str, service: str = "gaia", *, label: str | None = None, **kw):
        res = fetch.tap(adql, service, refresh=self.refresh, **kw)
        self.provenance.add(res.provenance, label)
        self._charge(res.provenance.bytes, f"tap {label or ''}")
        self.log(f"tap:{service} {label or ''} -> {res.provenance.rows} rows{' (cache)' if res.from_cache else ''}")
        return res.data

    def http(self, url: str, *, label: str | None = None, **kw) -> Path:
        res = fetch.http(url, refresh=self.refresh, **kw)
        self.provenance.add(res.provenance, label)
        self._charge(res.provenance.bytes, f"http {label or url}")
        self.log(f"http {label or url} -> {res.provenance.bytes} bytes{' (cache)' if res.from_cache else ''}")
        return res.data

    def save(self, name: str, obj: Any) -> Path:
        path = write_json(self.results / f"{name}.json", obj)
        self.saved.append(path.name)
        return path

    def log(self, msg: str) -> None:
        print(f"[{self.study.id}] {msg}")


def run(study: Study, refresh: bool = False) -> dict[str, Any]:
    import sys

    # Let run.py import helper modules that live next to it (e.g. screen.py).
    sys.path.insert(0, str(study.path))
    spec = importlib.util.spec_from_file_location(f"study_{study.number}", study.path / "run.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    ctx = Context(study, refresh=refresh)
    t0 = time.time()
    summary = module.main(ctx) or {}
    elapsed = round(time.time() - t0, 2)
    ctx.provenance.write(study.results_dir / "provenance.json")
    write_json(study.results_dir / "run_info.json",
               {"study": study.id, "finished_at": now_iso(), "seconds": elapsed, "outputs": ctx.saved})
    print(f"[{study.id}] done in {elapsed}s; outputs: {', '.join(ctx.saved) or '-'}")
    if summary:
        print(summarize(summary))
    return summary
