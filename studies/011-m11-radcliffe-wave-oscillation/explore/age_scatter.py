"""Exploration (wiki Part 3, "Age and birth in the Wave"): do older clusters scatter more about the fit?

No verdict. Uses the clusters-only B = 1 maximum-likelihood fit stored in results/t3.json (fits.b1) and
the cached cluster table; fits nothing. Splits the clusters at 10 and 20 Myr and reports the RMS of the
z and v_z residuals at each cluster's closest point, for all clusters and for that fit's inliers.

Run: python -m astrolab explore 011-m11-radcliffe-wave-oscillation --tag age-scatter --script explore/age_scatter.py
"""
import json
import math
from pathlib import Path

import numpy as np

import run as R
import wave011 as W

AGE_EDGES = (0, 10, 20, 31)      # Myr; bins [0, 10), [10, 20), [20, 31)


def vector_from_physical(par):
    v = W.default_vector()
    for k in ("x0", "y0", "x1", "y1", "x2", "y2", "A", "p", "s0", "phi", "w0t", "B", "r0"):
        v[W.IDX[k]] = par[k]
    v[W.IDX["ln_delta"]] = math.log(par["delta"])
    v[W.IDX["ln_gamma"]] = math.log(par["gamma"])
    v[W.IDX["ln_omega0"]] = math.log(par["omega0_kms_kpc"] / 1000.0)
    v[W.IDX["ln_mu0"]] = math.log(par["mu0_kpc"])
    return v


def main(ctx):
    res = Path(__file__).resolve().parents[1] / "results" / "t3.json"
    if not res.exists():
        raise SystemExit("results/t3.json missing: run the study first")
    t3 = json.loads(res.read_text(encoding="utf-8"))
    P = t3["params"]
    cl, co, _ = R.load_tables(ctx)
    data = R.make_data(cl, co)
    grid = W.Grid(int(P["grid_n"]), float(P["u_min"]), float(P["u_max"]))
    wc, _ = W.fixed_weights(data, grid, P["bandwidth_pc"])
    m = W.Model(W.Setup(free=W.SHAPE_NAMES, sigma=P["sigma_pc"]), data, grid, wc)
    v = vector_from_physical(t3["fits"]["b1"]["parameters"])
    ev = m.evaluate(v)
    dz = ev["cl_res"][:, 2]
    dvz = ev["cl_res"][:, 3] * m.divisor(v)
    inl = ~ev["cl_outlier"]
    age = cl["age"].to_numpy(float)
    rows = []
    for lo, hi in zip(AGE_EDGES[:-1], AGE_EDGES[1:]):
        sel = (age >= lo) & (age < hi)
        for name, mask in (("all", sel), ("inliers", sel & inl)):
            n = int(mask.sum())
            rows.append({"age_myr": [lo, hi], "set": name, "n": n,
                         "rms_dz_pc": float(np.sqrt(np.mean(dz[mask] ** 2))) if n else None,
                         "rms_dvz_kms": float(np.sqrt(np.mean(dvz[mask] ** 2))) if n else None})
    for r in rows:
        print(r)
    ctx.save("age_scatter", {"fit": "results/t3.json fits.b1 (clusters only, B = 1, maximum likelihood)",
                             "rows": rows})
    return {"rows": len(rows)}
