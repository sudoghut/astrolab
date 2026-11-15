"""Exploration (post hoc, referee item a2, 2026-11-15): R3 with widened bounds.

In the registered R3 every model-B fit has its break at the lower bound (20 Msun), and for
M_t >= 80 the peak width sits at its upper bound (10 Msun). This script reruns R3 with the FAR
fallback of explore/gwtc1_far.py (153 events) and with wider bounds: m_break in [10.5, 60] for both
models, sigma in [1, 25] for model B. Peak centre stays in [25, 45]. Run with:
    python -m astrolab explore 007 --tag r3-wide-bounds --script explore/r3_wide_bounds.py
"""
import importlib.util
from pathlib import Path

import gwtc

_spec = importlib.util.spec_from_file_location("explore_007_gwtc1_far", Path(__file__).parent / "gwtc1_far.py")
gwtc1_far = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gwtc1_far)

_A, _B = gwtc.BOUNDS_A, gwtc.BOUNDS_B


def main(ctx):
    gwtc.BOUNDS_A = [(-2.0, 10.0), (-2.0, 10.0), (10.5, 60.0)]
    gwtc.BOUNDS_B = gwtc.BOUNDS_A + [(25.0, 45.0), (1.0, 25.0), (0.0, 1.0)]
    ctx.save("bounds", {"BOUNDS_A": gwtc.BOUNDS_A, "BOUNDS_B": gwtc.BOUNDS_B})
    try:
        return gwtc1_far.main(ctx)
    finally:
        gwtc.BOUNDS_A, gwtc.BOUNDS_B = _A, _B
