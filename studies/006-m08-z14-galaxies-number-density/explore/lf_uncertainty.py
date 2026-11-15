"""Exploration (post hoc, referee items b1 and b5): sensitivity of R2 and R3 to the z ~ 8 LF
uncertainties and to a uniform dust shift at z ~ 8.

Each Bouwens et al. 2021 z ~ 8 Schechter parameter is moved by its 1 sigma error, one at a time
(independent shifts, not the true covariance); dust is a uniform A_UV removed from the z ~ 8 LF
(the calibration target is brightened by A_UV). Fiducial model otherwise.
    python -m astrolab explore 006 --tag lf-uncertainty --script explore/lf_uncertainty.py
"""
import copy

import numpy as np

import run
import z14inputs as inp
import z14model as zm


def evaluate(ctx, P, S, lf_override, label, phi_obs, phi_n26):
    saved = copy.deepcopy(inp.BOUWENS21["z8"])
    inp.BOUWENS21["z8"].update(lf_override)
    try:
        fid = {k: P[k] for k in ("hmf", "accretion", "cal", "sigma_cal", "eps_extrap")}
        res = run.run_model(S, P, fid, phi_obs)
    finally:
        inp.BOUWENS21["z8"].clear()
        inp.BOUWENS21["z8"].update(saved)
    row = {"label": label, "override": lf_override, "evaluable": res["evaluable"]}
    if res["evaluable"]:
        row["ratio"] = res["phi_ours"] / phi_n26
        row["r2"] = run.r2_verdict(row["ratio"], P["r2_factor"])
        if res.get("r3_evaluable"):
            row["sigma_roots"] = res["sigma_roots"]
            row["r3"] = run.r3_verdict(res["sigma_roots"], P["r3_target"])
    ctx.log(f"{label}: ratio {row.get('ratio', float('nan')):.2f} {row.get('r2')}; "
            f"sigma {row.get('sigma_roots', {}).get('central', {}).get('value')} "
            f"[{row.get('sigma_roots', {}).get('lower', {}).get('value')}, "
            f"{row.get('sigma_roots', {}).get('upper', {}).get('value')}] {row.get('r3')}")
    return row


def main(ctx):
    P = dict(run.PARAMS)
    S = run.Setup(P)
    phi_obs = 2.0 / inp.N26["volume_mpc3"]
    phi_n26 = phi_obs / inp.N26["ratio"]
    b = inp.BOUWENS21["z8"]
    cases = [({}, "fiducial"),
             ({"phi_star": 0.04e-3}, "phi* -1 sigma (0.04e-3)"), ({"phi_star": 0.18e-3}, "phi* +1 sigma (0.18e-3)"),
             ({"m_star": b["m_star"] + 0.28}, "M* +0.28 (fainter)"), ({"m_star": b["m_star"] - 0.28}, "M* -0.28 (brighter)"),
             ({"alpha": b["alpha"] + 0.20}, "alpha +0.20"), ({"alpha": b["alpha"] - 0.20}, "alpha -0.20")]
    for a_uv in (0.3, 0.5, 1.0):
        cases.append(({"m_star": b["m_star"] - a_uv}, f"dust: A_UV = {a_uv} mag removed at z ~ 8"))
    rows = [evaluate(ctx, P, S, o, lab, phi_obs, phi_n26) for o, lab in cases]
    ctx.save("lf_uncertainty", {"rows": rows,
                                "note": "post hoc; one parameter at a time; dust as a uniform brightening of the z ~ 8 LF"})
    return {"n": len(rows)}
