"""Project paths and resource limits.

All limits can be overridden by environment variables, but the defaults encode
the project's core principle: laptop-scale data (MB) and compute (minutes).
"""
from __future__ import annotations

import os
from pathlib import Path

from platformdirs import user_cache_dir

ROOT = Path(__file__).resolve().parent.parent
STUDIES = ROOT / "studies"
ATLAS = ROOT / "atlas"
CLAIMS = ATLAS / "claims"
TEMPLATE = STUDIES / "_template"


def _env_int(name: str, default: int) -> int:
    value = os.environ.get(name)
    return int(value) if value else default


def cache_dir() -> Path:
    """System cache dir (never inside the Dropbox-synced project folder)."""
    path = Path(os.environ.get("ASTROLAB_CACHE_DIR") or user_cache_dir("astrolab", appauthor=False))
    path.mkdir(parents=True, exist_ok=True)
    return path


# Total cache budget; least-recently-used entries are pruned beyond this.
CACHE_LIMIT_BYTES = _env_int("ASTROLAB_CACHE_LIMIT_MB", 2048) * 1024**2
# Default row cap for a TAP query; a query hitting it is refused, not truncated.
TAP_DEFAULT_MAX_ROWS = _env_int("ASTROLAB_TAP_MAX_ROWS", 50_000)
# Hard ceiling even when a study explicitly raises max_rows.
TAP_HARD_MAX_ROWS = _env_int("ASTROLAB_TAP_HARD_MAX_ROWS", 2_000_000)
# Single HTTP download cap.
HTTP_MAX_BYTES = _env_int("ASTROLAB_HTTP_MAX_MB", 50) * 1024**2
# Total input bytes one study run may pull in (cached or not).
STUDY_BUDGET_BYTES = _env_int("ASTROLAB_STUDY_BUDGET_MB", 200) * 1024**2

# NOTE FOR AGENTS: do not raise any of these limits (here or via ASTROLAB_* env
# vars) without explicit user approval. See AGENTS.md, section 1.
