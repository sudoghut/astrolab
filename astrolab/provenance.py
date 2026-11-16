"""Provenance: every number must be traceable to a query, a data release and a time."""
from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class Provenance:
    source: str                     # e.g. "tap:gaia", "http"
    request: str                    # ADQL text or URL
    release: str | None = None      # e.g. "Gaia DR3"
    retrieved_at: str = field(default_factory=now_iso)
    sha256: str | None = None
    rows: int | None = None
    bytes: int | None = None
    cache_key: str | None = None
    note: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


class ProvenanceLog:
    """Collects provenance records during a study run and writes them to results/."""

    def __init__(self) -> None:
        self.records: list[dict[str, Any]] = []

    def add(self, prov: Provenance | dict[str, Any], label: str | None = None) -> None:
        rec = prov.to_dict() if isinstance(prov, Provenance) else dict(prov)
        if label:
            rec["label"] = label
        self.records.append(rec)

    def write(self, path: Path) -> None:
        """Write the log. Small logs keep the plain format ({"generated_at", "inputs"}); a log whose
        plain form would exceed COMPACT_ABOVE_BYTES (a query-heavy study) is written in the
        lossless templated format, which `expand` turns back into the plain form."""
        path.parent.mkdir(parents=True, exist_ok=True)
        doc = {"generated_at": now_iso(), "inputs": self.records}
        text = json.dumps(doc, indent=2)
        if len(text.encode("utf-8")) > COMPACT_ABOVE_BYTES:
            text = _dump_compact(compact(doc))
        path.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------------------------------------
# Templated format for query-heavy studies (T-033). A study that issues thousands of similar ADQL
# queries (e.g. one per sky region) would otherwise write megabytes of near-identical text.
# Each request is split into literal text and numeric tokens; within a group of requests that share
# the same literal text, tokens that are identical in every request are put back into the template,
# and only the varying tokens are stored per record. Fields equal in every record are hoisted into
# "defaults". The transformation is exact: expand(compact(doc)) == doc.

COMPACT_ABOVE_BYTES = 256 * 1024
COMPACT_FORMAT = "templated-v1"
_NUM = re.compile(r"(?<![A-Za-z_\d.])-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?")
_SLOT = re.compile(r"\{\{|\}\}|\{\}")
_HOIST = ("source", "release")


def _split(request: str) -> tuple[str, list[str]]:
    """(skeleton with every numeric token as {} and literal braces doubled, the tokens)."""
    escaped = request.replace("{", "{{").replace("}", "}}")
    return _NUM.sub("{}", escaped), _NUM.findall(escaped)


def _fill(template: str, params: list[str]) -> str:
    it = iter(params)

    def repl(m: re.Match) -> str:
        tok = m.group(0)
        return "{" if tok == "{{" else "}" if tok == "}}" else next(it)

    out = _SLOT.sub(repl, template)
    if next(it, None) is not None:
        raise ValueError("more parameters than template slots")
    return out


def compact(doc: dict[str, Any]) -> dict[str, Any]:
    records = doc["inputs"]
    groups: dict[str, list[list[str]]] = {}
    for r in records:
        skel, toks = _split(r["request"])
        groups.setdefault(skel, []).append(toks)
    varying = {skel: [i for i in range(len(toks[0])) if len({t[i] for t in toks}) > 1]
               for skel, toks in groups.items()}

    templates: dict[str, int] = {}
    defaults = {k: records[0][k] for k in _HOIST
                if records and k in records[0] and all(r.get(k) == records[0][k] for r in records)}
    out = []
    for r in records:
        skel, toks = _split(r["request"])
        var = set(varying[skel])
        k = iter(range(len(toks)))
        template = _SLOT.sub(lambda m: m.group(0) if m.group(0) != "{}" or (i := next(k)) in var
                             else toks[i].replace("{", "{{").replace("}", "}}"), skel)
        rec = {key: v for key, v in r.items() if key != "request" and key not in defaults}
        rec["request_template"] = templates.setdefault(template, len(templates))
        rec["request_params"] = [toks[i] for i in sorted(var)]
        out.append(rec)
    return {"generated_at": doc["generated_at"], "format": COMPACT_FORMAT,
            "how_to_read": "astrolab.provenance.expand(json) restores the plain records",
            "defaults": defaults, "templates": list(templates), "inputs": out}


def expand(doc: dict[str, Any]) -> dict[str, Any]:
    """The plain form {"generated_at", "inputs": [records with "request"]} of either format."""
    if doc.get("format") != COMPACT_FORMAT:
        return doc
    templates, defaults = doc["templates"], doc.get("defaults", {})
    inputs = []
    for rec in doc["inputs"]:
        r = dict(defaults)
        r.update({k: v for k, v in rec.items() if k not in ("request_template", "request_params")})
        r["request"] = _fill(templates[rec["request_template"]], rec["request_params"])
        inputs.append(r)
    return {"generated_at": doc["generated_at"], "inputs": inputs}


def _dump_compact(doc: dict[str, Any]) -> str:
    """One record per line: compact, but still diffable."""
    head = {k: v for k, v in doc.items() if k != "inputs"}
    body = ",\n".join("    " + json.dumps(r, separators=(",", ":")) for r in doc["inputs"])
    return json.dumps(head, indent=2)[:-2] + ',\n  "inputs": [\n' + body + "\n  ]\n}\n"
