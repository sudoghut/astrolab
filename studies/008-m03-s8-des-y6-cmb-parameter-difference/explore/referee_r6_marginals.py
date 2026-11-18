"""Exploration (post hoc, R6 referee item 1; 2026-11-18). Uses the cached chains only.

Per-parameter view of the six-parameter difference that R6 estimates with flows: weighted mean and
standard deviation of each sampled parameter in each chain, and the binned-KDE n_sigma (the R2
estimator, one seed) of the 1-D difference in each parameter and of the pairs (mnu, A_s) and
(mnu, Omega_m). Delta = DES 3x2pt - CMB, equally weighted draws as in R2/R6.
Run with:
    python -m astrolab explore 008 --tag referee-r6-marginals --script explore/referee_r6_marginals.py
"""
import numpy as np

import run
import s8diff

NAMES = ["omega_m", "h0", "omega_b", "n_s", "a_s_1e9", "mnu"]


def _load(ctx, P, key):
    path = run._fetch(ctx, P, key)
    fmt = s8diff.read_format(path)
    cmap, _ = s8diff.column_map(fmt, key, key in P["positional_ok"])
    chain, info = s8diff.load_chain(path, cmap, 0.0)
    hdr = [h.lower() for h in fmt["header"]]
    X = np.column_stack([chain["data"][:, hdr.index("cosmological_parameters--" + n)] for n in NAMES])
    return X, chain["w"] / chain["w"].sum(), info


def main(ctx):
    P = dict(run.PARAMS)
    des, wd, idd = _load(ctx, P, "des_3x2pt")
    cmb, wc, ic = _load(ctx, P, "cmb")
    rng = np.random.default_rng(0)
    n = 400_000
    d = des[rng.choice(len(wd), n, p=wd)] - cmb[rng.choice(len(wc), n, p=wc)]
    out = {"n_draws": n, "rows": {"des_3x2pt": int(len(wd)), "cmb": int(len(wc))},
           "ess": {"des_3x2pt": idd.get("ess"), "cmb": ic.get("ess")}, "parameters": {}}
    for j, name in enumerate(NAMES):
        def mv(X, w):
            m = float(np.average(X[:, j], weights=w))
            return m, float(np.sqrt(np.average((X[:, j] - m) ** 2, weights=w)))
        md, sd = mv(des, wd)
        mc, sc = mv(cmb, wc)
        out["parameters"][name] = {
            "des_mean": md, "des_sd": sd, "cmb_mean": mc, "cmb_sd": sc,
            "p_delta_gt_0": float(np.mean(d[:, j] > 0)),
            "n_sigma_1d": float(s8diff.nsigma_binned(d[:, [j]])["n_sigma"]),
        }
        ctx.log(f"{name}: DES {md:.4f} +- {sd:.4f}, CMB {mc:.4f} +- {sc:.4f}, "
                f"1-D n_sigma {out['parameters'][name]['n_sigma_1d']:.3f}")
    im, ia, io = NAMES.index("mnu"), NAMES.index("a_s_1e9"), NAMES.index("omega_m")
    out["pairs"] = {"mnu_a_s": float(s8diff.nsigma_binned(d[:, [im, ia]])["n_sigma"]),
                    "mnu_omega_m": float(s8diff.nsigma_binned(d[:, [im, io]])["n_sigma"])}
    ctx.log(f"pairs: {out['pairs']}")
    ctx.save("referee_r6_marginals", out)
