"""Claims registry: landmark results as first-class, graded, reproducible objects.

One YAML file per claim in ``atlas/claims/``. Required fields::

    id: desi-dr2-bao                # = file stem
    title: short English title
    title_zh: 中文标题                # Chinese for the web pages' zh mode (AGENTS.md bilingual rule)
    statement: one-sentence claim as made in the literature
    statement_zh: 中文陈述
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

import re
from pathlib import Path
from typing import Any

import yaml

from . import config
from .study import LEVELS, discover

GRADES = ("established", "tension", "hint", "contested", "refuted")
REPRO_STATUSES = ("not-started", "in-progress", "reproduced", "partial", "failed")
REQUIRED = ("id", "title", "statement", "level", "grade", "sources", "reproduction")
ZH_FIELDS = ("title_zh", "statement_zh")  # required Chinese twins of title / statement
STUDY_ZH_FIELDS = ("title_zh", "question_zh")  # required in every studies/*/study.yaml

# Atlas footprints (design plan 011). Default distance range per level [log10 pc], for entries
# without a footprint; deliberately loose orders of magnitude.
LEVEL_SCALE_LOG10 = {"L0": (8.0, 10.15), "L1": (7.0, 10.0), "L2": (4.0, 8.5), "L3": (0.0, 5.0),
                     "L4": (-6.0, 4.0), "X": (-6.0, 10.15)}
SKY_MODES = ("all-sky", "survey", "targets", "none")


def zh_errors(data: dict[str, Any], fields: tuple[str, ...]) -> list[str]:
    """Chinese fields must contain Chinese text and must not be template placeholders."""
    errs = []
    for k in fields:
        v = data.get(k)
        if not isinstance(v, str) or not re.search(r"[\u4e00-\u9fff]", v):
            errs.append(f"'{k}' must be a non-empty Chinese string")
        elif v.strip().upper().startswith("TODO"):
            errs.append(f"'{k}' is still the template placeholder; fill in the Chinese text")
    return errs


def load_all(root: Path | None = None) -> list[dict[str, Any]]:
    root = root or config.CLAIMS
    out = []
    for f in sorted(root.glob("*.yaml")):
        data = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        data["_file"] = f.name
        out.append(data)
    return out


def validate(claim: dict[str, Any], study_ids: set[str] | None = None) -> list[str]:
    errs = [f"missing field '{k}'" for k in REQUIRED if k not in claim] + zh_errors(claim, ZH_FIELDS)
    if any(e.startswith("missing field") for e in errs):
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


def sky_modes(mode: Any) -> list[str]:
    """'all-sky + targets' -> ['all-sky', 'targets']."""
    return [m.strip() for m in str(mode or "none").split("+") if m.strip()]


def _num(x: Any) -> float | None:
    """A finite float, or None (bools and non-numbers rejected)."""
    import math

    if isinstance(x, bool):
        return None
    try:
        v = float(x)
    except (TypeError, ValueError, OverflowError):
        return None
    return v if math.isfinite(v) else None


def _text_ok(x: Any) -> bool:
    """Optional free text emitted to the page: absent or a string."""
    return x is None or isinstance(x, str)


def _name_ok(x: Any) -> bool:
    return isinstance(x, str) and bool(x.strip())


def _coord_ok(t: dict[str, Any]) -> bool:
    ra, dec = _num(t.get("ra")), _num(t.get("dec"))
    return ra is not None and dec is not None and 0.0 <= ra < 360.0 and -90.0 <= dec <= 90.0


def footprint_errors(meta: dict[str, Any]) -> list[str]:
    """Schema check of the optional ``footprint`` field of a study.yaml (design plan 011)."""
    fp = meta.get("footprint")
    if fp is None:
        return []
    if not isinstance(fp, dict):
        return ["footprint must be a mapping"]
    errs = []
    sc = fp.get("scale")
    if sc is not None:
        lo, hi = (_num(sc.get("min_pc")), _num(sc.get("max_pc"))) if isinstance(sc, dict) else (None, None)
        if lo is None or hi is None:
            errs.append("footprint.scale needs finite numeric min_pc and max_pc")
        elif not (0 < lo < hi):
            errs.append("footprint.scale needs 0 < min_pc < max_pc")
        if isinstance(sc, dict) and not _text_ok(sc.get("note")):
            errs.append("footprint.scale.note must be text")
    sky = fp.get("sky")
    if sky is not None:
        if not isinstance(sky, dict):
            return errs + ["footprint.sky must be a mapping"]
        modes = sky_modes(sky.get("mode"))
        if not modes:
            errs.append("footprint.sky.mode is empty")
        bad = [m for m in modes if m not in SKY_MODES]
        if bad:
            errs.append(f"footprint.sky.mode: unknown {bad}; use {SKY_MODES} joined by ' + '")
        if "none" in modes and len(modes) > 1:
            errs.append("footprint.sky.mode: 'none' cannot be combined with other modes")
        if len(set(modes)) != len(modes):
            errs.append("footprint.sky.mode: repeated mode")
        sv = sky.get("survey")
        if sv is not None and not (isinstance(sv, dict) and _name_ok(sv.get("name")) and _text_ok(sv.get("note"))):
            errs.append("footprint.sky.survey must be a mapping with a text name (and optional text note)")
        elif "survey" in modes and sv is None:
            errs.append("footprint.sky.mode includes survey: give survey.name")
        tg = sky.get("targets")
        if "targets" in modes:
            if not isinstance(tg, list) or not tg or not all(isinstance(t, dict) and _name_ok(t.get("name")) for t in tg):
                return errs + ["footprint.sky.mode includes targets: give a list of targets with a name (and ra, dec)"]
            for t in tg:
                if ("ra" in t) != ("dec" in t):
                    errs.append(f"footprint target {t.get('name')}: give both ra and dec or neither")
                elif "ra" in t and not _coord_ok(t):
                    errs.append(f"footprint target {t.get('name')}: ra in [0, 360) and dec in [-90, 90] degrees")
        elif tg:
            errs.append("footprint.sky.targets given but mode does not include targets")
    return errs


def resolve_footprint(study_path: Path, meta: dict[str, Any]) -> dict[str, Any]:
    """Footprint for the Atlas: scale as log10 pc (or the level default) and sky targets with
    ICRS and Galactic coordinates; missing coordinates are taken from results/targets.json."""
    import json
    import math

    fp = meta.get("footprint") or {}
    if footprint_errors(meta):          # invalid footprint: fall back to the level default, no sky
        fp = {}
    sc = fp.get("scale")
    if sc:
        scale = {"log10_min": math.log10(float(sc["min_pc"])), "log10_max": math.log10(float(sc["max_pc"])),
                 "note": sc.get("note"), "default": False}
    else:
        lo, hi = LEVEL_SCALE_LOG10.get(meta.get("level"), LEVEL_SCALE_LOG10["X"])
        scale = {"log10_min": lo, "log10_max": hi, "note": None, "default": True}
    sky = fp.get("sky") or {}
    modes = sky_modes(sky.get("mode")) if fp.get("sky") else []
    known = {}
    tfile = study_path / "results" / "targets.json"
    if tfile.exists():
        try:
            for t in json.loads(tfile.read_text(encoding="utf-8")):
                if isinstance(t, dict) and _name_ok(t.get("name")) and _coord_ok(t):
                    known[t["name"]] = (float(t["ra"]), float(t["dec"]))
        except (ValueError, TypeError):
            pass
    targets = []
    for t in (sky.get("targets") or []) if "targets" in modes else []:
        if "ra" in t and "dec" in t:
            ra, dec = float(t["ra"]), float(t["dec"])
        else:
            ra, dec = known.get(t.get("name"), (None, None))
        entry = {"name": t.get("name"), "ra": ra, "dec": dec, "l": None, "b": None}
        if ra is not None and dec is not None:
            entry["l"], entry["b"] = _galactic(ra, dec)
        targets.append(entry)
    sv = sky.get("survey")
    survey = {"name": sv["name"], "note": sv.get("note")} if isinstance(sv, dict) and "survey" in modes else None
    return {"scale": scale, "sky": {"modes": modes, "survey": survey, "targets": targets}}


def _galactic(ra: float, dec: float) -> tuple[float, float]:
    import astropy.units as u
    from astropy.coordinates import SkyCoord

    g = SkyCoord(ra=ra * u.deg, dec=dec * u.deg, frame="icrs").galactic
    return float(g.l.deg), float(g.b.deg)


def validate_all() -> dict[str, list[str]]:
    ids = {s.id for s in discover()}
    claims = load_all()
    problems = {c["_file"]: validate(c, ids) for c in claims}
    for s in discover():  # studies must carry Chinese title/question too (bilingual rule)
        errs = zh_errors(s.meta, STUDY_ZH_FIELDS) + footprint_errors(s.meta)
        if errs:
            problems[f"studies/{s.id}/study.yaml"] = errs
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
            "title_zh": meta.get("title_zh"),
            "level": meta.get("level"),
            "status": meta.get("status"),
            "question": meta.get("question"),
            "question_zh": meta.get("question_zh"),
            "claims": meta.get("claims", []),
            "has_web": (s.path / "web" / "index.html").exists(),
            "last_run": run_info.exists(),
            "footprint": resolve_footprint(s.path, meta),
        })
    claims = [{k: v for k, v in c.items() if not k.startswith("_")} for c in load_all()]
    return {"generated_at": now_iso(), "levels": list(LEVELS), "claims": claims, "studies": studies,
            "level_scale_log10": {k: list(v) for k, v in LEVEL_SCALE_LOG10.items()}}
