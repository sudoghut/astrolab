"""Claims registry: landmark results as first-class, graded, reproducible objects.

One YAML file per claim in ``atlas/claims/``. Required fields::

    id: desi-dr2-bao                # = file stem
    title: short English title
    statement: one-sentence claim as made in the literature
    level: L0 | L1 | L2 | L3 | L4 | X
    grade: established | tension | hint | contested | refuted
    sources:                        # at least one
      - cite: "DESI Collaboration 2025, PRD ..."
        arxiv: "2503.14738"
    reproduction:
      status: not-started | in-progress | reproduced | partial | failed
      study: NNN-slug               # folder in studies/ (optional until started)
      quantities:                   # paper vs ours
        - {name: H0rd, paper: ..., ours: ..., unit: ...}
    depends_on: [other-claim-id]    # optional
    open_questions: [...]           # optional: seeds for real research
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from . import config
from .study import LEVELS, discover

GRADES = ("established", "tension", "hint", "contested", "refuted")
REPRO_STATUSES = ("not-started", "in-progress", "reproduced", "partial", "failed")
REQUIRED = ("id", "title", "statement", "level", "grade", "sources", "reproduction")


def load_all(root: Path | None = None) -> list[dict[str, Any]]:
    root = root or config.CLAIMS
    out = []
    for f in sorted(root.glob("*.yaml")):
        data = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        data["_file"] = f.name
        out.append(data)
    return out


def validate(claim: dict[str, Any], study_ids: set[str] | None = None) -> list[str]:
    errs = [f"missing field '{k}'" for k in REQUIRED if k not in claim]
    if errs:
        return errs
    if claim["_file"] != f"{claim['id']}.yaml":
        errs.append(f"id '{claim['id']}' does not match file name")
    if claim["level"] not in LEVELS:
        errs.append(f"level must be one of {LEVELS}")
    if claim["grade"] not in GRADES:
        errs.append(f"grade must be one of {GRADES}")
    if not claim["sources"] or not all("cite" in s for s in claim["sources"]):
        errs.append("sources must be a non-empty list of {cite, arxiv?}")
    repro = claim["reproduction"] or {}
    if repro.get("status") not in REPRO_STATUSES:
        errs.append(f"reproduction.status must be one of {REPRO_STATUSES}")
    if study_ids is not None and repro.get("study") and repro["study"] not in study_ids:
        errs.append(f"reproduction.study '{repro['study']}' not found in studies/")
    return errs


def validate_all() -> dict[str, list[str]]:
    ids = {s.id for s in discover()}
    claims = load_all()
    problems = {c["_file"]: validate(c, ids) for c in claims}
    known = {c.get("id") for c in claims}
    for c in claims:
        for dep in c.get("depends_on") or []:
            if dep not in known:
                problems[c["_file"]].append(f"depends_on '{dep}' is not a known claim")
    return {k: v for k, v in problems.items() if v}


def atlas_data() -> dict[str, Any]:
    """Everything the Atlas page needs, as one JSON-able dict."""
    from .provenance import now_iso

    studies = []
    for s in discover():
        meta = s.meta
        run_info = s.results_dir / "run_info.json"
        studies.append({
            "id": s.id,
            "title": meta.get("title", s.id),
            "level": meta.get("level"),
            "status": meta.get("status"),
            "question": meta.get("question"),
            "claims": meta.get("claims", []),
            "has_web": (s.path / "web" / "index.html").exists(),
            "last_run": run_info.exists(),
        })
    claims = [{k: v for k, v in c.items() if not k.startswith("_")} for c in load_all()]
    return {"generated_at": now_iso(), "levels": list(LEVELS), "claims": claims, "studies": studies}
