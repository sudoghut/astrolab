"""Exploration (post hoc, referee item 4): how much of R4's ln BF is a preference for gamma < 13/3?

Evidence of the free-gamma power law (log10 A ~ U(-18, -11), gamma ~ U(0, 7)) against the
gamma = 13/3 power law and the turnover model, on the same data product and grid conventions as
run.py. Run with:
    python -m astrolab explore 005 --tag r4-gamma-free --script explore/r4_gamma_free.py
"""
import numpy as np

import gwb
import run


def main(ctx):
    P = dict(run.PARAMS)
    prod = run._load(ctx, P, P["versions"][0])
    f = prod["freqs"][:P["n_freq"]]
    sa, sg = 0.01, 0.01
    xa = gwb.axis(-18.0, -11.0, sa)
    xg = gwb.axis(0.0, 7.0, sg)
    lw_a, lw_g = np.log(gwb.trap_weights(xa.size)), np.log(gwb.trap_weights(xg.size))
    terms = []
    for i0 in range(0, xg.size, 64):
        g = xg[i0:i0 + 64]
        A, G = np.meshgrid(xa, g)
        ll = gwb.lnlike(prod, gwb.log10rho_powerlaw(A, G, f, prod["T"]), below_grid=P["below_grid"])
        terms.append(gwb._logsumexp(ll + lw_g[i0:i0 + 64, None] + lw_a[None, :]))
    ln_z_free = gwb._logsumexp(terms) + np.log(sa * sg) - np.log(7.0) - np.log(7.0)
    r4 = gwb.r4(prod, n_freq=P["n_freq"], gamma=P["gamma_fixed"], lo_a=-18.0, hi_a=-11.0,
                lo_fb=P["r4_range_fb"][0], hi_fb=P["r4_range_fb"][1], lo_k=P["r4_range_k"][0],
                hi_k=P["r4_range_k"][1], steps=tuple(P["r4_steps"]), below_grid=P["below_grid"],
                edge_frac=P["edge_frac"], edge_max=P["edge_max"], chunk=8)
    out = {"version": P["versions"][0], "ln_Z_free_gamma": ln_z_free, "ln_Z_pl_13_3": r4["ln_Z_pl"],
           "ln_Z_turn": r4["ln_Z_turn"],
           "ln_bf_free_vs_13_3": ln_z_free - r4["ln_Z_pl"],
           "ln_bf_turn_vs_free": r4["ln_Z_turn"] - ln_z_free,
           "ln_bf_turn_vs_13_3": r4["ln_bf_turnover_vs_pl"]}
    ctx.save("r4_gamma_free", out)
    ctx.log(f"ln BF free-gamma vs 13/3 = {out['ln_bf_free_vs_13_3']:.3f}; turnover vs free = "
            f"{out['ln_bf_turn_vs_free']:.3f}; turnover vs 13/3 = {out['ln_bf_turn_vs_13_3']:.3f}")
    return out
