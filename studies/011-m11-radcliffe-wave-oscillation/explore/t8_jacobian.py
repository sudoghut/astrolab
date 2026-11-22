"""Exploration (referee 2026-11-21, section 6): does T8's free-omega0 fit need the ln(omega0) normalisation?

No verdict. In the column-(7) setup the fourth component of each cluster vector is v_z / omega0 with sigma
fixed, so the implied density of v_z carries a factor 1/omega0 per cluster that the formal likelihood
(wave011.Model.evaluate) leaves out. This script finds the posterior mode (MAP) of the column-(7) setup
under K24's priors and under the broad priors, with and without the term -sum_k w_k ln(omega0), from K24's
column-(7) vector plus a few prior draws, and reports omega0 at each mode. It fits nothing else and does
not touch results/.

Run: python -m astrolab explore 011-m11-radcliffe-wave-oscillation --tag t8-jacobian --script explore/t8_jacobian.py
"""
import json
import math
from pathlib import Path

import numpy as np

import fit011 as F
import run as R
import wave011 as W


class JacobianModel(W.Model):
    """Column-(7) likelihood plus -sum_k w_k ln(divisor) when the divisor is the fitted omega0."""

    def evaluate(self, v):
        out = super().evaluate(v)
        if out is not None and self.setup.divisor is None and "lnL_cl" in out:
            extra = -float(np.sum(self.w_cl)) * math.log(self.divisor(v))
            out["lnL_cl"] += extra
            out["lnL"] += extra
        return out


def main(ctx):
    res = Path(__file__).resolve().parents[1] / "results" / "t8.json"
    P = json.loads(res.read_text(encoding="utf-8"))["params"]
    cl, co, _ = R.load_tables(ctx)
    data = R.make_data(cl, co)
    grid = W.Grid(int(P["grid_n"]), float(P["u_min"]), float(P["u_max"]))
    wc, wo = W.fixed_weights(data, grid, P["bandwidth_pc"], "half")
    st = R.setups(P)
    n_starts = int(P.get("explore_starts", 4))
    out = {}
    for name in ("col7", "col7_broad"):
        for tag, cls in (("formal", W.Model), ("with_ln_omega0", JacobianModel)):
            m = cls(st[name], data, grid, wc, wo)
            rng = R.rng_for(P["seed"], "explore_t8j_" + name)
            starts = [m.theta_of(W.k24_vector(7))] + [m.prior_draw(rng) for _ in range(n_starts - 1)]
            best = None
            for s in starts:
                r = F.optimise(m, s, nm_maxfev=P["ml_nm_maxfev"], lbfgs_maxfun=P["ml_lbfgs_maxfun"],
                               objective="post")
                if best is None or r["value"] > best["value"]:
                    best = r
            v = m.full(best["theta"])
            om = 1000.0 * math.exp(v[W.IDX["ln_omega0"]])
            out[f"{name}_{tag}"] = {"omega0_kms_kpc_map": om, "logpost": best["value"]}
            ctx.log(f"{name} {tag}: MAP omega0 = {om:.1f} km/s/kpc (log posterior {best['value']:.2f})")
    ctx.save("t8_jacobian", out)
    return out
