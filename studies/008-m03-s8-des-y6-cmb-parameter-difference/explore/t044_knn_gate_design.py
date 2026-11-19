"""Design check for README section 2.8 (T-044; 2026-11-19, before the addendum was fixed). Synthetic data
only, no chains.

Is the k-nearest-neighbour (kNN) parameter-difference estimator used by the R6-NOMNU referee calibrated?
It is run on R6's 6-D and R6-NOMNU's 5-D known-answer gate distributions (`flowshift.synthetic`, the
gate settings recorded in results/r6_nomnu.json), seeds 10-12 drawn as the gates draw them
(`default_rng(seed + sample_seed_offset)`), N = 100,000, k = 20, 50, 100, and compared with the
recorded exact n_sigma (6-D 2.3710, 5-D 2.3862). Result when the addendum was drafted: 6-D 2.03-2.24,
5-D 2.02-2.16 (0.13-0.37 sigma low), so section 2.8 uses flows and reports kNN only as descriptive.

kNN estimator (section 2.8): whiten with the sample mean m and covariance S (z = (x - m) L, L L^T =
S^-1); the density proxy of a point is its distance to its k-th nearest neighbour among the samples;
n_sigma = sqrt(2) erfinv(f), f the fraction of samples whose proxy distance is smaller than the
origin's.
Run with:
    python -m astrolab explore 008 --tag t044-knn-gate --script explore/t044_knn_gate_design.py
"""
import json
from pathlib import Path

import numpy as np

import flowshift

HERE = Path(__file__).resolve().parent.parent


def knn_nsigma(x, k):
    from scipy.spatial import cKDTree
    from scipy.special import erfinv
    m = x.mean(0)
    L = np.linalg.cholesky(np.linalg.inv(np.cov(x.T)))
    z = (x - m) @ L
    z0 = (-m) @ L
    tree = cKDTree(z)
    dk = tree.query(z, k + 1)[0][:, -1]          # the sample itself is its own nearest neighbour
    d0 = tree.query(z0[None], k)[0][0, -1]
    return float(np.sqrt(2.0) * erfinv(np.mean(dk < d0)))


def main(ctx):
    rec = json.loads((HERE / "results" / "r6_nomnu.json").read_text(encoding="utf-8"))
    gates = rec["settings"]["gates"]
    exact = {"gate6": rec["flows"]["gate6_pop1"]["exact"]["n_sigma"],
             "gate5": rec["flows"]["gate5"]["exact"]["n_sigma"]}
    out = {"n": 100000, "k": [20, 50, 100], "exact": exact, "values": {}}
    for name in ("gate6", "gate5"):
        g = gates[name]
        out["values"][name] = {}
        for seed in g["seeds"]:
            x = flowshift.synthetic(out["n"], np.random.default_rng(seed + g["sample_seed_offset"]), g)
            vals = [knn_nsigma(x, k) for k in out["k"]]
            out["values"][name][str(seed)] = vals
            ctx.log(f"{name} seed {seed}: kNN {[round(v, 3) for v in vals]} (exact {exact[name]:.4f})")
    ctx.save("t044_knn_gate_design", out)
