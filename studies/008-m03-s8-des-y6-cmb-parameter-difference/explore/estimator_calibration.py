"""Calibration of the R2 estimator on synthetic data (no download); README section 2.2.

A Gaussian P(dp) with known n_sigma (2.6 in 1-D, 2.2 in 2-D) is sampled N times and passed to
the same estimator as run.py. Run with:
    python -m astrolab explore 008 --tag estimator-calibration --script explore/estimator_calibration.py
"""
import numpy as np
from scipy import special

import s8diff


def main(ctx):
    out = {}
    for dim, true in ((1, 2.6), (2, 2.2)):
        shift = true if dim == 1 else np.sqrt(-2 * np.log(1 - special.erf(true / np.sqrt(2))))
        for bw in (1.0, 0.5, 2.0):
            vals = []
            for seed in range(5):
                rng = np.random.default_rng(seed)
                x = rng.standard_normal((4_000_000, dim))
                x[:, 0] += shift
                vals.append(s8diff.nsigma_binned(x, bw_factor=bw)["n_sigma"])
            out[f"d{dim}_bw{bw}"] = {"true": true, "mean": float(np.mean(vals)),
                                     "s": float(np.std(vals, ddof=1)), "values": vals}
            ctx.log(f"{dim}-D bw x{bw}: mean {np.mean(vals):.4f}, s {np.std(vals, ddof=1):.4f}")
    ctx.save("calibration", out)
