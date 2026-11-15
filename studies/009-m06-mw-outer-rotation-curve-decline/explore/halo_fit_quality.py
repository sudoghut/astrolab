"""Exploration (post hoc, 2026-11-15): goodness of fit of the Einasto and NFW halos (model E dJ).

R5 shows that the extrapolated mass depends on the halo shape (Einasto about 2e11, NFW about 7e11
Msun). This script reports the best-fit chi^2 of both halos on the 18 points of J23 Table 3 (combined
errors) and on the 8 points beyond 19 kpc, so that the two extrapolations can be weighed. Run with:
    python -m astrolab explore 009 --tag halo-fit-quality --script explore/halo_fit_quality.py
"""
import numpy as np
from scipy import optimize

import rc
import run


def main(ctx):
    P = dict(run.PARAMS)
    j23, t4, bar, o24, e19 = run.load_inputs()
    model = run.baryon_model("E dJ", bar)
    R, V, sig = j23["R"], j23["V"], j23["sig"]
    vb2 = np.array([rc.baryon_v2(r, model) for r in R])
    out = {}
    for kind, start, fn in (("einasto", [3.7e11, 12.0, 2.4], lambda th, r: rc.einasto_mass(r, *th)),
                            ("nfw", [7.0, 1.2], lambda th, r: rc.nfw_mass(r, 10 ** th[0], 10 ** th[1]))):
        lnp = run.einasto_lnpost if kind == "einasto" else run.nfw_lnpost
        nll = lambda th: -lnp(th, R, V, sig, vb2, P) if np.isfinite(lnp(th, R, V, sig, vb2, P)) else 1e30
        best = optimize.minimize(nll, start, method="Nelder-Mead", options={"maxiter": 40000, "xatol": 1e-6, "fatol": 1e-8})
        model_v = np.sqrt(vb2 + rc.G * fn(best.x, R) / R)
        res = (V - model_v) / sig
        outer = R > 19
        out[kind] = {"chi2": float(np.sum(res ** 2)), "n_points": int(R.size), "n_params": len(start),
                     "chi2_outer": float(np.sum(res[outer] ** 2)), "residuals": res.tolist(), "best": list(map(float, best.x))}
        ctx.log(f"{kind}: chi2 {out[kind]['chi2']:.2f} for {R.size} points ({len(start)} params); outer chi2 {out[kind]['chi2_outer']:.2f}")
    out["delta_chi2_nfw_minus_einasto"] = out["nfw"]["chi2"] - out["einasto"]["chi2"]
    ctx.save("halo_fit_quality", out)
