"""Write study results as small JSON files that web pages and agents can read."""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

# Keep results small: web pages and agents read these directly.
RESULT_WARN_BYTES = 5 * 1024**2


def to_jsonable(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {str(k): to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [to_jsonable(v) for v in obj]
    if isinstance(obj, pd.DataFrame):
        return {c: to_jsonable(obj[c].to_numpy()) for c in obj.columns}
    if isinstance(obj, pd.Series):
        return to_jsonable(obj.to_numpy())
    if isinstance(obj, np.ndarray):
        return [to_jsonable(v) for v in obj.tolist()]
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating, float)):
        f = float(obj)
        return None if math.isnan(f) or math.isinf(f) else f
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    if obj is pd.NA or obj is None:
        return None
    if hasattr(obj, "to_value"):  # astropy Quantity
        return to_jsonable(obj.to_value())
    return obj


def write_json(path: Path, obj: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(to_jsonable(obj), indent=1, ensure_ascii=False)
    path.write_text(text, encoding="utf-8")
    if len(text.encode()) > RESULT_WARN_BYTES:
        print(f"WARNING: {path.name} is {len(text) / 1024**2:.1f} MB; results should stay small.")
    return path


def summarize(obj: Any, max_items: int = 12) -> str:
    """Compact one-screen summary of a result dict, for agent-facing output."""
    lines = []
    for k, v in list(obj.items())[:max_items]:
        if isinstance(v, (list, tuple)) and len(v) > 6:
            lines.append(f"  {k}: [{len(v)} items]")
        elif isinstance(v, dict):
            lines.append(f"  {k}: {{{', '.join(list(map(str, v))[:6])}{', ...' if len(v) > 6 else ''}}}")
        else:
            lines.append(f"  {k}: {v}")
    if len(obj) > max_items:
        lines.append(f"  ... ({len(obj) - max_items} more keys)")
    return "\n".join(lines)
