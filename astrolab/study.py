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
      argument/       paper studies: the paper's argument in Lean 4 (design/007)
      explore/        chat explorations: scripts (committed), <date>-<tag>/ outputs (not committed)
"""
from __future__ import annotations

import datetime as _dt
import importlib.util
import json
import math
import re
import shutil
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from . import config, fetch
from .provenance import ProvenanceLog, now_iso
from .results import summarize, to_jsonable, write_json

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
    shutil.copytree(config.TEMPLATE, dest, ignore=shutil.ignore_patterns(".lake", "__pycache__"))
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
        self.max_save_bytes: int | None = None  # set by explore(): outputs must stay small

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
        if not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.-]*", name) or ".." in name:
            raise ValueError(f"result name {name!r} must be a plain file name (no paths)")
        if self.max_save_bytes is not None and name in ("provenance", "run_info"):
            raise ValueError(f"{name!r} is reserved for the exploration's own records")
        if self.max_save_bytes is not None:
            size = len(json.dumps(to_jsonable(obj), indent=1, ensure_ascii=False,
                                  default=str).encode("utf-8"))
            if size > self.max_save_bytes:
                raise ValueError(f"{name}.json would be {size / 1024**2:.1f} MB; exploration outputs must "
                                 f"stay under {self.max_save_bytes / 1024**2:.0f} MB (summarise first)")
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


# ---------------------------------------------------------------------------------------------
# Chat explorations (AGENTS.md section 2, design/007 section 2.3): rerun run.py with in-memory
# PARAMS overrides, or run an explore/ script, writing only to explore/<date>-<tag>/.

EXPLORE_MAX_BYTES = 1024**2
_TAG_RE = re.compile(r"[a-z0-9-]{1,40}")


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_overrides(pairs: list[str], defaults: dict[str, Any]) -> dict[str, Any]:
    """``KEY=VALUE`` strings -> values; JSON-parsed and type-checked against ``defaults``."""
    out: dict[str, Any] = {}
    for pair in pairs:
        if "=" not in pair:
            raise SystemExit(f"--set expects KEY=VALUE, got {pair!r}")
        key, raw = pair.split("=", 1)
        if key not in defaults:
            raise SystemExit(f"unknown parameter {key!r}; PARAMS has: {', '.join(sorted(defaults))}")
        default = defaults[key]
        try:
            value = json.loads(raw)
        except (json.JSONDecodeError, ValueError):
            value = raw
        if isinstance(default, str) and not isinstance(value, str):
            value = raw  # a string parameter takes the text as typed
        int_for_float = isinstance(default, float) and type(value) is int
        if not (type(value) is type(default) or int_for_float or default is None):
            raise SystemExit(f"parameter {key}: expected {type(default).__name__} like the default "
                             f"{default!r}, got {value!r}")
        if int_for_float:
            try:
                value = float(value)
            except OverflowError:
                raise SystemExit(f"parameter {key}: {raw} is too large") from None
        if isinstance(value, float) and not math.isfinite(value):
            raise SystemExit(f"parameter {key}: {raw} is not a finite number")
        out[key] = value
    return out


def explore(study: Study, tag: str, sets: list[str] | None = None, script: str | None = None,
            refresh: bool = False) -> dict[str, Any]:
    """Run an exploration without touching ``results/`` or the committed ``PARAMS``."""
    import sys

    if not _TAG_RE.fullmatch(tag or ""):
        raise SystemExit("--tag must match [a-z0-9-]{1,40}")
    explore_root = (study.path / "explore").resolve()
    if explore_root != study.path.resolve() / "explore":
        raise SystemExit("explore/ must be a real folder inside the study (not a link elsewhere)")
    out = (explore_root / f"{_dt.date.today().isoformat()}-{tag}").resolve()
    if out.parent != explore_root:
        raise SystemExit("output directory must stay inside explore/")
    if script:
        path = (study.path / script).resolve()
        if path.suffix != ".py" or path.parent != explore_root or not path.is_file():
            raise SystemExit("--script must be an existing .py file directly in the study's explore/ folder")
        if sets:
            raise SystemExit("--set applies to run.py's PARAMS; put a script's options inside the script")
    old_path = list(sys.path)
    sys.path.insert(0, str(study.path))
    try:
        params: dict[str, Any] = {}
        if script:
            module = _load_module(path, f"explore_{study.number}_{path.stem}")
            overrides: dict[str, Any] = {}
        else:
            module = _load_module(study.path / "run.py", f"study_{study.number}_explore")
            params = getattr(module, "PARAMS", None)
            if not isinstance(params, dict):
                raise SystemExit("run.py has no PARAMS dict; add one (AGENTS.md section 2) or use --script")
            overrides = parse_overrides(sets or [], params)
            params.update(overrides)  # in memory only: the module was freshly loaded
        if not hasattr(module, "main"):
            raise SystemExit("the exploration module has no main(ctx)")
        if out.exists():
            shutil.rmtree(out)  # same date and tag: overwrite
        out.mkdir(parents=True)
        ctx = Context(study, refresh=refresh)
        ctx.results = out
        ctx.max_save_bytes = EXPLORE_MAX_BYTES
        t0 = time.time()
        summary = module.main(ctx) or {}
    finally:
        sys.path[:] = old_path
    ctx.provenance.write(out / "provenance.json")
    write_json(out / "run_info.json", {
        "study": study.id, "finished_at": now_iso(), "seconds": round(time.time() - t0, 2),
        "script": script or "run.py", "overrides": overrides, "params": dict(params),
        "outputs": ctx.saved})
    print(f"[{study.id}] exploration written to {out.relative_to(study.path.resolve())}")
    if summary:
        print(summarize(summary))
    return summary
