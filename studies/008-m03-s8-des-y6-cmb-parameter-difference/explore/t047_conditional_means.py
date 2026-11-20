"""Exploration (post hoc, T-047 first part; 2026-11-20). No flow is trained. Reads the two chains through
the study's guarded fetch (from the cache, where they already are).

Question: does the DES 3x2pt chain's Sigma m_nu column raise the six-parameter difference to the CMB
(R6-SHUF) through its correlation with the other DES parameters? Without a flow, look at the conditional
means: in bins of Sigma m_nu (weighted quantiles of the DES chain), the weighted mean of each other
parameter in each chain, and its offset DES - CMB in units of the combined conditional standard
deviation. Also the weighted correlation of each parameter with Sigma m_nu in each chain.
Run with:
    python -m astrolab explore 008 --tag t047-conditional-means --script explore/t047_conditional_means.py
"""
import numpy as np

import run
import s8diff

NAMES = ["omega_m", "h0", "omega_b", "n_s", "a_s_1e9", "mnu"]
N_BINS = 5


def _load(ctx, P, key):
    path = run._fetch(ctx, P, key)
    fmt = s8diff.read_format(path)
    cmap, _ = s8diff.column_map(fmt, key, key in P["positional_ok"])
    chain, info = s8diff.load_chain(path, cmap, 0.0)
    hdr = [h.lower() for h in fmt["header"]]
    X = np.column_stack([chain["data"][:, hdr.index("cosmological_parameters--" + n)] for n in NAMES])
    w = chain["w"] / chain["w"].sum()
    ok = np.all(np.isfinite(X), axis=1) & np.isfinite(w)
    return X[ok], w[ok] / w[ok].sum(), info


def weighted_quantiles(x, w, qs):
    o = np.argsort(x)
    c = np.cumsum(w[o])
    c = (c - 0.5 * w[o]) / c[-1]
    return np.interp(qs, c, x[o])


def mean_sd(x, w):
    if w.sum() <= 0:
        return float("nan"), float("nan")
    m = float(np.average(x, weights=w))
    return m, float(np.sqrt(np.average((x - m) ** 2, weights=w)))


def corr(x, y, w):
    mx, sx = mean_sd(x, w)
    my, sy = mean_sd(y, w)
    return float(np.average((x - mx) * (y - my), weights=w) / (sx * sy))


def ess(w):
    return float(w.sum() ** 2 / np.sum(w ** 2)) if w.sum() > 0 else 0.0


def main(ctx):
    P = dict(run.PARAMS)
    des, wd, _ = _load(ctx, P, "des_3x2pt")
    cmb, wc, _ = _load(ctx, P, "cmb")
    im = NAMES.index("mnu")
    edges = weighted_quantiles(des[:, im], wd, np.linspace(0, 1, N_BINS + 1))
    edges[0], edges[-1] = -np.inf, np.inf          # open outer bins: every row of both chains is binned
    out = {"n_bins": N_BINS, "mnu_edges_des_quantiles": [float(e) for e in edges[1:-1]],
           "mnu": {"des": mean_sd(des[:, im], wd), "cmb": mean_sd(cmb[:, im], wc)},
           "corr_with_mnu": {}, "overall": {}, "bins": []}
    for j, name in enumerate(NAMES):
        if j == im:
            continue
        md, sd = mean_sd(des[:, j], wd)
        mc, sc = mean_sd(cmb[:, j], wc)
        out["overall"][name] = {"des_mean": md, "des_sd": sd, "cmb_mean": mc, "cmb_sd": sc,
                                "offset_sigma": (md - mc) / np.hypot(sd, sc)}
        out["corr_with_mnu"][name] = {"des": corr(des[:, j], des[:, im], wd),
                                      "cmb": corr(cmb[:, j], cmb[:, im], wc)}
    for b in range(N_BINS):
        lo, hi = edges[b], edges[b + 1]
        md_ = (des[:, im] >= lo) & (des[:, im] < hi)
        mc_ = (cmb[:, im] >= lo) & (cmb[:, im] < hi)
        row = {"lo": float(lo), "hi": float(hi),
               "des_weight": float(wd[md_].sum()), "cmb_weight": float(wc[mc_].sum()),
               "des_ess": ess(wd[md_]), "cmb_ess": ess(wc[mc_]),
               "mnu_mean": {"des": mean_sd(des[md_, im], wd[md_])[0], "cmb": mean_sd(cmb[mc_, im], wc[mc_])[0]},
               "params": {}}
        for j, name in enumerate(NAMES):
            if j == im:
                continue
            dm, ds = mean_sd(des[md_, j], wd[md_])
            cm, cs = mean_sd(cmb[mc_, j], wc[mc_])
            row["params"][name] = {"des_mean": dm, "des_sd": ds, "cmb_mean": cm, "cmb_sd": cs,
                                   "offset_sigma": (dm - cm) / np.hypot(ds, cs)}
        out["bins"].append(row)
        ctx.log(f"mnu bin {b} [{lo:.3f}, {hi:.3f}): DES w {row['des_weight']:.3f} (ESS {row['des_ess']:.0f}), "
                f"CMB w {row['cmb_weight']:.3f} (ESS {row['cmb_ess']:.0f}); offsets (sigma) "
                + ", ".join(f"{k} {v['offset_sigma']:+.2f}" for k, v in row["params"].items()))
    ctx.log("overall offsets (sigma): " + ", ".join(f"{k} {v['offset_sigma']:+.2f}" for k, v in out["overall"].items()))
    ctx.log("corr with mnu (DES / CMB): " + ", ".join(
        f"{k} {v['des']:+.2f} / {v['cmb']:+.2f}" for k, v in out["corr_with_mnu"].items()))
    ctx.save("t047_conditional_means", out)
    return {"overall": {k: v["offset_sigma"] for k, v in out["overall"].items()}}
