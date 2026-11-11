"""Provenance: every number must be traceable to a query, a data release and a time."""
from __future__ import annotations

import json
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
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"generated_at": now_iso(), "inputs": self.records}, indent=2), encoding="utf-8")
