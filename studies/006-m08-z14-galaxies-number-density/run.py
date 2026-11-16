"""M8 z ~ 14 galaxies: number density and the UV scatter a constant-efficiency model needs.

Pre-registration: README sections 1-4. Run with:
    python -m astrolab run 006-m08-z14-galaxies-number-density
Explore with:
    python -m astrolab explore 006-m08-z14-galaxies-number-density --tag <topic> --set KEY=VALUE

R1  N26 number density, Gehrels errors, volume, Poisson tails (checks the Lean mod_poisson bound).
R2  Constant-SFE halo model prediction vs N26's baseline (phi_obs/182); 72-variant robustness.
R3  sigma_UV needed at z = 14-15 with the median relation fixed.
R4  H25's z ~ 14 point (context).
No data are downloaded: inputs are hand-transcribed in z14inputs.py.
"""
import itertools

import numpy as np
from astropy import units as u
from astropy.cosmology import Planck18
from scipy import optimize

import z14inputs as inp
import z14model as zm

# Tunable knobs (AGENTS.md section 2). Read inside main() and passed on as arguments.
PARAMS = {
    # fiducial model (README section 4)
    "hmf": "st",
    "accretion": "fakhouri_mean",
    "cal": "z8",                       # Bouwens et al. 2021 z ~ 8 (z = 7.9) or "z7" (z = 6.8)
    "sigma_cal": 0.7,
    "eps_extrap": "dpl",               # "dpl" or "const" (constant below the calibrated range)
    "m_h_min": 1e8,
    "log_m_max": 14.0, "dlog_m": 0.02,
    "cal_m_bright": -22.0, "cal_m_faint": -17.0, "cal_dm": 0.25,
    "rms_max": 0.05,
    "n_z": 11, "n_m": 21,
    "sigma_range": [0.7, 4.0], "sigma_step": 0.05,
    # pre-registered thresholds
    "r1_tol_logphi": 0.01, "r1_tol_err": 0.05, "r1_tol_volume": 0.05,
    "tail_max_ppm": 200.0,
    "r2_factor": 3.0,
    "r3_target": [1.5, 2.0],
    "robust_min_evaluable": 48,
    "sigma8_tol": 1e-3,
    # variant grid (README section 4, step 7)
    "variants": {
        "hmf": ["st", "reed07"],
        "accretion": ["fakhouri_mean", "fakhouri_median", "dekel13"],
        "cal": ["z8", "z7"],
        "sigma_cal": [0.5, 0.7, 0.9],
        "eps_extrap": ["dpl", "const"],
    },
    "run_variants": True,
    # R2/R3-POST (README section 2, addendum 2026-11-16)
    "post_check": True, "post_walkers": 32, "post_steps": 100000, "post_burn": 20000, "post_draws": 500,
    "post_seed": 0, "post_tau_factor": 50, "post_p_threshold": 0.95, "post_r3_min_frac": 0.9,
    "post_misfit_p": 0.01, "post_bound_frac": 0.05, "post_sensitivity": True,
    # exploration-only knobs (README section 8); defaults leave the pre-registered analysis unchanged
    "completeness": 1.0,
    "area_factor": 1.0,
}


# ------------------------------------------------------------------ R1 ----

def r1(P):
    n = inp.N26
    N, V = n["n_sources"], n["volume_mpc3"]
    phi = N / (V * (n["m_hi"] - n["m_lo"]))
    lam_lo, lam_hi = zm.gehrels(N)
    err_hi = float(np.log10(lam_hi / N))
    err_lo = float(np.log10(N / lam_lo))
    omega = n["area_arcmin2"] * (np.pi / (180 * 60)) ** 2
    zz = np.linspace(n["z_lo"], n["z_hi"], 201)
    dvdz = Planck18.differential_comoving_volume(zz).to(u.Mpc ** 3 / u.sr).value
    vol = float(np.trapz(dvdz, zz) * omega)
    tail182 = zm.poisson_tail(N, N / n["ratio"]) * 1e6
    tail100 = zm.poisson_tail(N, N / 100.0) * 1e6
    ok_phi = abs(np.log10(phi) - n["log_phi"]) < P["r1_tol_logphi"]
    ok_err = abs(err_hi - n["err_hi"]) < P["r1_tol_err"] and abs(err_lo - n["err_lo"]) < P["r1_tol_err"]
    ok_vol = abs(vol / V - 1) < P["r1_tol_volume"]
    return {
        "phi_obs": phi, "log_phi": float(np.log10(phi)), "err_hi": err_hi, "err_lo": err_lo,
        "gehrels_lo": lam_lo, "gehrels_hi": lam_hi,
        "volume_mpc3": vol, "volume_ratio": vol / V,
        "p_tail_n26_ppm": tail182, "p_tail_ratio100_ppm": tail100,
        "verdict_density": "reproduced" if (ok_phi and ok_err) else "not reproduced",
        "verdict_volume": "reproduced" if ok_vol else "not reproduced",
        "mod_poisson_bound_holds": bool(tail182 <= P["tail_max_ppm"] and tail100 <= P["tail_max_ppm"]),
        "note": "Poisson errors only (no cosmic variance, no completeness)",
    }


# ------------------------------------------------------------- the model ----

class Setup:
    """Cosmology, sigma(M) and dV/dz shared by all variants."""

    def __init__(self, P):
        self.c = zm.cosmo_params(Planck18)
        self.pk = zm.LinearPower(self.c)
        self.lnM = np.log(10.0 ** np.arange(np.log10(P["m_h_min"]), P["log_m_max"] + 1e-9, P["dlog_m"]))
        self.M = np.exp(self.lnM)
        self.sig0 = self.pk.sigma_M(self.M)
        self.rho_m = self.pk.rho_m()
        n = inp.N26
        self.z_pred = np.linspace(n["z_lo"], n["z_hi"], P["n_z"])
        self.dvdz = Planck18.differential_comoving_volume(self.z_pred).to(u.Mpc ** 3 / u.sr).value
        self.D_pred = zm.growth(self.z_pred, self.c)
        self._dcache = {}

    def D(self, z):
        if z not in self._dcache:
            self._dcache[z] = float(zm.growth(z, self.c)[0])
        return self._dcache[z]

    def hmf(self, z, kind):
        return zm.dndlnm(self.lnM, self.sig0, self.D(z), self.rho_m, kind)


def solve_sigma(sg, phis, targets, phi_fn):
    """R3 roots on an increasing phi(sigma) (README section 2): censoring and equality rules."""
    roots = {}
    for key, tgt in targets.items():
        if phis[0] >= tgt:
            roots[key] = {"value": float(sg[0]), "censored": "le" if phis[0] > tgt else None}
        elif phis[-1] <= tgt:
            roots[key] = {"value": float(sg[-1]), "censored": "gt" if phis[-1] < tgt else None}
        else:
            f = lambda s: np.log(phi_fn(s)) - np.log(tgt)  # noqa: E731
            roots[key] = {"value": float(optimize.brentq(f, sg[0], sg[-1], xtol=1e-4)), "censored": None}
    return roots


def monotonic_kind(phis):
    d = np.diff(phis)
    if np.all(d > 0):
        return "increasing"
    if np.all(d < 0):
        return "decreasing"
    return "not monotonic"


def run_model(S, P, combo, phi_obs, fixed=None):
    """Calibrate (or take a fixed calibration), predict R2 and solve R3 for one combination.

    `fixed` = {"theta": ..., "m_cal_lo": ..., "calibration": ...} keeps the median relation of a
    previous calibration (used for the descriptive 10 M_min roots).
    """
    lf = inp.BOUWENS21[combo["cal"]]
    z_cal = lf["z"]
    if fixed is None:
        m_grid = np.arange(P["cal_m_bright"], P["cal_m_faint"] + 1e-9, P["cal_dm"])
        hmf_cal = S.hmf(z_cal, combo["hmf"])
        cal = zm.calibrate(S.lnM, hmf_cal, z_cal, S.c, combo["accretion"], combo["sigma_cal"], lf, m_grid)
    else:
        cal = fixed["calibration"]
    out = {"combo": combo, "calibration": cal}
    if cal["rms"] >= P["rms_max"]:
        out["evaluable"] = False
        out["reason"] = f"calibration rms {cal['rms']:.3f} >= {P['rms_max']}"
        return out
    theta = cal["theta"]
    med_cal = zm.muv_median(S.M, z_cal, S.c, theta, combo["accretion"])
    shape_cal = zm.median_shape(S.M, med_cal, P["cal_m_bright"], P["cal_m_faint"])
    m_cal_lo = fixed["m_cal_lo"] if fixed is not None else shape_cal["m_cal_lo"]
    if combo["eps_extrap"] == "const" and m_cal_lo is None:
        out["evaluable"] = False
        out["reason"] = "no median <= -17 on the rising branch: calibrated range undefined for 'const'"
        return out
    floor = m_cal_lo if combo["eps_extrap"] == "const" else None
    hmf_z = [zm.dndlnm(S.lnM, S.sig0, d, S.rho_m, combo["hmf"]) for d in S.D_pred]
    med_z = [zm.muv_median(S.M, z, S.c, theta, combo["accretion"], floor) for z in S.z_pred]
    n = inp.N26

    def phi_bin(sigma):
        return zm.bin_average(S.lnM, hmf_z, med_z, sigma, S.dvdz, n["m_lo"], n["m_hi"], P["n_m"])[0]

    i_mid = len(S.z_pred) // 2
    out.update({
        "evaluable": True,
        "median_shape_zcal": shape_cal,
        "median_shape_z14_5": zm.median_shape(S.M, med_z[i_mid], P["cal_m_bright"], P["cal_m_faint"]),
        "phi_ours": phi_bin(combo["sigma_cal"]),
        "m_cal_lo": m_cal_lo,
    })
    in_bin = (med_z[i_mid] >= n["m_lo"]) & (med_z[i_mid] <= n["m_hi"])
    if in_bin.any():
        mb = S.M[in_bin]
        lo, hi = shape_cal["m_cal_lo"], shape_cal["m_cal_hi"]
        out["bin_halo_mass_range_z14_5"] = [float(mb.min()), float(mb.max())]
        out["bin_halos_inside_calibrated_range"] = bool(lo is not None and mb.min() >= lo and mb.max() <= hi)
        # abundance-weighted: fraction of the bin's halos (by number) inside the calibrated range
        w = hmf_z[i_mid][in_bin]
        inside = (mb >= (lo or np.inf)) & (mb <= hi)
        out["bin_abundance_fraction_inside_calibrated_range"] = float(w[inside].sum() / w.sum())
    # R3: required sigma
    sg = np.arange(P["sigma_range"][0], P["sigma_range"][1] + 1e-9, P["sigma_step"])
    phis = np.array([phi_bin(s) for s in sg])
    out["phi_vs_sigma"] = {"sigma": sg.tolist(), "phi": phis.tolist()}
    kind = monotonic_kind(phis)
    if kind != "increasing":
        out["r3_evaluable"] = False
        out["r3_reason"] = f"phi(sigma) {kind} on the search range"
        return out
    out["r3_evaluable"] = True
    lam_lo, lam_hi = zm.gehrels(n["n_sources"])
    targets = {"central": phi_obs, "lower": phi_obs * lam_lo / n["n_sources"],
               "upper": phi_obs * lam_hi / n["n_sources"]}
    out["sigma_roots"] = solve_sigma(sg, phis, targets, phi_bin)
    return out


def r3_verdict(roots, target):
    """Overlap of [sigma(lower), sigma(upper)] with the target interval; censored ends half-open."""
    lo, hi = roots["lower"], roots["upper"]
    a = -np.inf if lo["censored"] == "le" else lo["value"]
    b = np.inf if hi["censored"] == "gt" else hi["value"]
    return "consistent with N26" if (a <= target[1] and b >= target[0]) else "different"


def r2_verdict(ratio, factor):
    if 1.0 / factor <= ratio <= factor:
        return "same order as N26's baseline"
    return "higher" if ratio > factor else "lower"


def robustness(rows, key, fid_verdict, n_min):
    """README section 2: over evaluable rows; at least n_min evaluable; all agree with the fiducial."""
    if fid_verdict in (None, "not evaluable") or len(rows) < n_min:
        return "not assessable"
    return "robust" if all(r[key] == fid_verdict for r in rows) else "calibration-dependent"


# ------------------------------------------------------------------ main ----

def main(ctx):
    P = dict(PARAMS)
    out1 = r1(P)
    ctx.log(f"R1: log phi = {out1['log_phi']:.3f} (+{out1['err_hi']:.3f}/-{out1['err_lo']:.3f}), "
            f"V = {out1['volume_mpc3']:.0f} Mpc^3 ({out1['volume_ratio']:.4f}), tails "
            f"{out1['p_tail_n26_ppm']:.1f} / {out1['p_tail_ratio100_ppm']:.1f} ppm")
    ctx.save("r1", out1)

    # exploration-only adjustments of the observed density (defaults: none)
    phi_obs = out1["phi_obs"] / P["completeness"] / P["area_factor"]
    phi_n26 = out1["phi_obs"] / inp.N26["ratio"]
    vol_eff = inp.N26["volume_mpc3"] * P["area_factor"]

    S = Setup(P)
    s8 = float(S.pk.sigma_R(8.0 / S.c["h"])[0])
    checks = {"sigma8": s8, "sigma8_ok": bool(abs(s8 - S.c["sigma8"]) < P["sigma8_tol"]),
              "st_normalisation": zm.st_normalisation(),
              "mass_fraction_z0": zm.mass_fraction_check(S.lnM, S.sig0, S.rho_m)}
    checks["st_normalisation_ok"] = bool(abs(checks["st_normalisation"] - 1) < 0.01)
    if not (checks["sigma8_ok"] and checks["st_normalisation_ok"]):
        raise RuntimeError(f"pre-registered checks failed: {checks}")
    ctx.log(f"checks: sigma8 = {s8:.4f}, ST normalisation = {checks['st_normalisation']:.4f}, "
            f"z=0 mass fraction grid/ST = {checks['mass_fraction_z0']}")

    fid = {k: P[k] for k in ("hmf", "accretion", "cal", "sigma_cal", "eps_extrap")}
    fres = run_model(S, P, fid, phi_obs)
    r2 = {"fiducial": fid, "phi_obs": phi_obs, "phi_n26_baseline": phi_n26, "checks": checks,
          "calibration": fres["calibration"], "evaluable": fres["evaluable"]}
    if fres["evaluable"]:
        ratio = fres["phi_ours"] / phi_n26
        r2.update({"phi_ours": fres["phi_ours"], "ratio_to_n26": ratio,
                   "verdict": r2_verdict(ratio, P["r2_factor"]),
                   "p_tail_ours": zm.poisson_tail(inp.N26["n_sources"], fres["phi_ours"] * vol_eff),
                   "median_shape_zcal": fres["median_shape_zcal"],
                   "median_shape_z14_5": fres["median_shape_z14_5"],
                   "bin_halo_mass_range_z14_5": fres.get("bin_halo_mass_range_z14_5"),
                   "bin_halos_inside_calibrated_range": fres.get("bin_halos_inside_calibrated_range"),
                   "bin_abundance_fraction_inside_calibrated_range":
                       fres.get("bin_abundance_fraction_inside_calibrated_range")})
        ctx.log(f"R2 fiducial: phi_ours = {fres['phi_ours']:.3e}, ratio to N26 baseline = {ratio:.2f} -> {r2['verdict']}")
    else:
        r2["verdict"] = "not evaluable"
        r2["reason"] = fres.get("reason")

    r3 = {"fiducial": fid, "target": P["r3_target"], "conditional_on_r2": r2.get("verdict")}
    if fres.get("r3_evaluable"):
        r3.update({"sigma_roots": fres["sigma_roots"], "verdict": r3_verdict(fres["sigma_roots"], P["r3_target"]),
                   "phi_vs_sigma": fres["phi_vs_sigma"]})
        # descriptive: same calibration (median relation fixed), halos above 10 M_min only
        P10 = dict(P, m_h_min=10 * P["m_h_min"])
        S10 = Setup(P10)
        f10 = run_model(S10, P10, fid, phi_obs,
                        fixed={"theta": fres["calibration"]["theta"], "m_cal_lo": fres.get("m_cal_lo"),
                               "calibration": fres["calibration"]})
        r3["sigma_roots_10mmin"] = f10.get("sigma_roots")
        r3["verdict_10mmin"] = (r3_verdict(f10["sigma_roots"], P["r3_target"]) if f10.get("r3_evaluable")
                                else f"not evaluable ({f10.get('r3_reason') or f10.get('reason')})")
        ctx.log(f"R3: sigma roots = {fres['sigma_roots']}, verdict {r3['verdict']}; 10 M_min: {r3['verdict_10mmin']}")
    else:
        r3["verdict"] = "not evaluable"
        r3["reason"] = fres.get("r3_reason") or fres.get("reason")

    # variant grid
    variants = []
    if P["run_variants"]:
        keys = list(P["variants"])
        for vals in itertools.product(*[P["variants"][k] for k in keys]):
            combo = dict(zip(keys, vals))
            res = fres if combo == fid else run_model(S, P, combo, phi_obs)
            row = {"combo": combo, "evaluable": res["evaluable"], "rms": res["calibration"]["rms"]}
            if res["evaluable"]:
                ratio = res["phi_ours"] / phi_n26
                row.update({"phi_ours": res["phi_ours"], "ratio": ratio, "r2": r2_verdict(ratio, P["r2_factor"]),
                            "r3_evaluable": res.get("r3_evaluable", False)})
                if res.get("r3_evaluable"):
                    row["sigma_central"] = res["sigma_roots"]["central"]
                    row["sigma_roots"] = res["sigma_roots"]
                    row["r3"] = r3_verdict(res["sigma_roots"], P["r3_target"])
                else:
                    row["r3_reason"] = res.get("r3_reason")
            else:
                row["reason"] = res.get("reason")
            variants.append(row)
        ev = [v for v in variants if v["evaluable"]]
        n_min = P["robust_min_evaluable"]
        counts2 = {}
        for v in ev:
            counts2[v["r2"]] = counts2.get(v["r2"], 0) + 1
        r2["robustness"] = robustness(ev, "r2", r2.get("verdict"), n_min)
        r2["variant_counts"] = {"evaluable": len(ev), "total": len(variants), "by_verdict": counts2}
        if ev:
            lo, hi = min(v["phi_ours"] for v in ev), max(v["phi_ours"] for v in ev)
            r2["envelope_phi_ours"] = [lo, hi]
            r2["envelope_p_tail"] = [zm.poisson_tail(2, lo * vol_eff), zm.poisson_tail(2, hi * vol_eff)]
        base = {k: fid[k] for k in ("hmf", "accretion", "cal", "eps_extrap")}
        r2["phi_ours_by_sigma"] = {str(v["combo"]["sigma_cal"]): v["phi_ours"] for v in ev
                                   if {k: v["combo"][k] for k in base} == base}
        ev3 = [v for v in ev if v.get("r3_evaluable")]
        counts3 = {}
        for v in ev3:
            counts3[v["r3"]] = counts3.get(v["r3"], 0) + 1
        r3["robustness"] = robustness(ev3, "r3", r3.get("verdict"), n_min)
        r3["variant_counts"] = {
            "evaluable": len(ev3), "total": len(variants), "by_verdict": counts3,
            "not_evaluable_reasons": {
                reason: sum(1 for v in variants if (v.get("r3_reason") or v.get("reason")) == reason)
                for reason in {v.get("r3_reason") or v.get("reason") for v in variants
                               if not v.get("r3_evaluable")}},
            "n_central_censored_le": sum(1 for v in ev3 if v["sigma_central"]["censored"] == "le"),
            "n_central_censored_gt": sum(1 for v in ev3 if v["sigma_central"]["censored"] == "gt"),
        }
        sc = [v["sigma_central"]["value"] for v in ev3 if v["sigma_central"]["censored"] is None]
        if sc:
            r3["envelope_sigma_central_uncensored"] = [min(sc), max(sc)]
        ctx.log(f"variants: {len(ev)}/{len(variants)} evaluable; R2 {r2['robustness']} {counts2}; "
                f"R3 {r3['robustness']} {counts3}")

    ctx.save("r2", r2)
    ctx.save("r3", r3)
    ctx.save("variants", {"rows": variants})

    h = inp.H25_Z14
    ctx.save("r4", {"phi_h25": h["phi"], "m_uv_h25": h["m_uv"], "ratio_h25_to_n26": h["phi"] / out1["phi_obs"],
                    "area_ratio_n26_to_h25": inp.N26["area_arcmin2"] / h["area_arcmin2_approx"],
                    "note": "context only: shares JADES-GS-z14-0 with N26; H25 errors include cosmic variance"})

    curves = {}
    if fres["evaluable"]:
        lf = inp.BOUWENS21[fid["cal"]]
        mg = np.arange(-23.0, -16.0 + 1e-9, 0.25)
        theta = fres["calibration"]["theta"]
        floor = fres.get("m_cal_lo") if fid["eps_extrap"] == "const" else None
        med_cal = zm.muv_median(S.M, lf["z"], S.c, theta, fid["accretion"])
        hmf_cal = S.hmf(lf["z"], fid["hmf"])
        med14 = zm.muv_median(S.M, 14.5, S.c, theta, fid["accretion"], floor)
        hmf14 = S.hmf(14.5, fid["hmf"])
        curves = {
            "muv": mg.tolist(),
            "lf_cal_model": zm.lf_model(mg, S.lnM, hmf_cal, med_cal, fid["sigma_cal"]).tolist(),
            "lf_cal_schechter": zm.schechter_mag(mg, lf["m_star"], lf["phi_star"], lf["alpha"]).tolist(),
            "lf_z14_5": {str(s): zm.lf_model(mg, S.lnM, hmf14, med14, s).tolist() for s in (0.7, 1.0, 1.5, 2.0)},
            "median_logm": np.log10(S.M[::10]).tolist(),
            "median_zcal": med_cal[::10].tolist(), "median_z14_5": med14[::10].tolist(),
        }
    ctx.save("curves", curves)
    summary = {"params": {k: v for k, v in P.items() if k != "variants"},
               "r1": {k: out1[k] for k in ("log_phi", "err_hi", "err_lo", "volume_ratio", "verdict_density",
                                           "verdict_volume", "p_tail_n26_ppm", "p_tail_ratio100_ppm")},
               "r2": {k: r2.get(k) for k in ("phi_ours", "ratio_to_n26", "verdict", "robustness")},
               "r3": {k: r3.get(k) for k in ("verdict", "robustness")}}
    if P["post_check"]:
        post = {"primary": r23_post(ctx, S, P, phi_obs, phi_n26, P["sigma_cal"], faint=False)}
        if P["post_sensitivity"]:
            for name, sc, faint in (("sigma_cal_0.5", 0.5, False), ("sigma_cal_0.9", 0.9, False),
                                    ("faint_rows", P["sigma_cal"], True)):
                post[name] = r23_post(ctx, S, P, phi_obs, phi_n26, sc, faint=faint)
        ctx.save("post", post)
        summary["R2_post"] = {k: post["primary"].get(k) for k in ("r2_label", "r2_probabilities")}
        summary["R3_post"] = {k: post["primary"].get(k) for k in ("r3_label", "r3_probabilities")}
    ctx.save("summary", summary)
    return summary


def post_label(probs, threshold, n_eff):
    """README section 2, R2/R3-POST: 'robust' if the leading verdict has P - 2 SE >= threshold
    (SE = sqrt(P(1-P)/n_eff)); 'borderline' if only P >= threshold; else 'calibration-uncertain'."""
    best = max(probs, key=probs.get)
    p = probs[best]
    se = float(np.sqrt(p * (1.0 - p) / n_eff))
    if p - 2.0 * se >= threshold:
        return f"robust to the calibration uncertainty ({best})"
    if p >= threshold:
        return "calibration-uncertain (borderline)"
    return "calibration-uncertain"


def r23_post(ctx, S, P, phi_obs, phi_n26, sigma_cal, faint):
    """R2/R3-POST: binned-LF calibration posterior (emcee) propagated to the R2/R3 verdicts."""
    import emcee

    combo = {"hmf": P["hmf"], "accretion": P["accretion"], "cal": "z8", "sigma_cal": sigma_cal,
             "eps_extrap": "dpl"}
    z_cal = inp.BOUWENS21["z8"]["z"]
    hmf_cal = S.hmf(z_cal, combo["hmf"])
    lens = inp.BINNED_Z8_LENS + (inp.BINNED_Z8_LENS_FAINT if faint else [])
    limits = inp.BINNED_Z8_LENS_LIMITS if faint else []

    def resid(x):
        return zm.binned_residuals(x, S.M, S.lnM, hmf_cal, z_cal, S.c, combo["accretion"], sigma_cal,
                                   inp.BINNED_Z8_BLANK, lens, limits)

    def logp(x):
        if not zm.in_box(x):
            return -np.inf
        r = resid(x)
        return -0.5 * float(r @ r)

    lsq = optimize.least_squares(resid, np.array([0.1, 11.5, 1.0, 0.5, 1.0]), bounds=(zm.POST_LO, zm.POST_HI),
                                 loss="linear", ftol=1e-10, xtol=1e-10, gtol=1e-10, max_nfev=2000)
    r0 = resid(lsq.x)
    chi2 = float(r0[:-1] @ r0[:-1])           # data chi2, prior residual excluded
    rng_b = np.random.default_rng(1)
    boot = []
    for _ in range(200):
        sb, sl, su = zm.simulate_binned(rng_b, lsq.x, S.M, S.lnM, hmf_cal, z_cal, S.c, combo["accretion"],
                                        sigma_cal, inp.BINNED_Z8_BLANK, lens, limits)

        def resid_b(x, sb=sb, sl=sl, su=su):
            return zm.binned_residuals(x, S.M, S.lnM, hmf_cal, z_cal, S.c, combo["accretion"], sigma_cal,
                                       sb, sl, su)
        rb = optimize.least_squares(resid_b, np.array([0.1, 11.5, 1.0, 0.5, 1.0]), bounds=(zm.POST_LO, zm.POST_HI), loss="linear",
                                    ftol=1e-10, xtol=1e-10, gtol=1e-10, max_nfev=2000)
        fb = resid_b(rb.x)
        boot.append(float(fb[:-1] @ fb[:-1]))
    p_fit = float(np.mean(np.array(boot) >= chi2))
    rng = np.random.default_rng(P["post_seed"])
    nw = int(P["post_walkers"])
    width = 1e-3 * (zm.POST_HI - zm.POST_LO)
    start = np.array([zm.reflect_into_box(lsq.x + rng.normal(0.0, width)) for _ in range(nw)])
    np.random.seed(int(rng.integers(2 ** 32)))   # emcee 3 copies the global numpy state
    sampler = emcee.EnsembleSampler(nw, 5, logp)
    sampler.run_mcmc(start, int(P["post_steps"]), progress=False)
    burn = int(P["post_burn"])
    chain = sampler.get_chain(discard=burn)
    tau = emcee.autocorr.integrated_time(chain, c=5, tol=0)
    n_post = chain.shape[0]
    converged = bool(n_post >= P["post_tau_factor"] * float(np.max(tau)))
    flat = sampler.get_chain(discard=burn, flat=True)
    idx = np.linspace(0, len(flat) - 1, int(P["post_draws"])).round().astype(int)
    draws = flat[idx]
    out = {"combo": combo, "faint_rows": faint, "lsq": {"x": lsq.x.tolist(), "chi2_data": chi2,
                                                         "p_bootstrap": p_fit, "n_bootstrap": len(boot),
                                                         "boot_chi2_quantiles": [float(q) for q in
                                                                                 np.percentile(boot, [5, 50, 95])],
                                                         "success": bool(lsq.success)},
           "tau": [float(t) if np.isfinite(t) else None for t in tau], "n_post_steps": n_post,
           "converged": converged, "n_points": int(len(r0) - 1),
           "acceptance": float(np.mean(sampler.acceptance_fraction)),
           "posterior": {n: {"median": float(np.median(flat[:, j])),
                             "p16": float(np.percentile(flat[:, j], 16)),
                             "p84": float(np.percentile(flat[:, j], 84))}
                         for j, n in enumerate(["eps0", "log_m1", "beta", "gamma", "f"])},
           "bound_fractions": zm.bound_fractions(draws)}
    r2v, r3v, ratios, centrals, roots_list = [], [], [], [], []
    for x in draws:
        theta = [float(v) for v in x[:4]]
        fres = run_model(S, P, combo, phi_obs, fixed={"theta": theta, "m_cal_lo": None,
                                                       "calibration": {"theta": theta, "rms": 0.0}})
        ratio = fres["phi_ours"] / phi_n26
        ratios.append(float(ratio))
        r2v.append(r2_verdict(ratio, P["r2_factor"]))
        roots_list.append(fres.get("sigma_roots") if fres.get("r3_evaluable") else None)
        if fres.get("r3_evaluable"):
            r3v.append(r3_verdict(fres["sigma_roots"], P["r3_target"]))
            centrals.append(fres["sigma_roots"].get("central"))
        else:
            r3v.append("not evaluable")
    n = len(draws)
    p2 = {k: r2v.count(k) / n for k in ("higher", "same order as N26's baseline", "lower")}
    ev3 = [v for v in r3v if v != "not evaluable"]
    p3 = {k: (ev3.count(k) / len(ev3) if ev3 else None) for k in ("consistent with N26", "different")}
    if abs(sum(p2.values()) - 1.0) > 1e-9 or (ev3 and abs(sum(p3.values()) - 1.0) > 1e-9):
        raise RuntimeError(f"verdict labels not all counted: {set(r2v)} {set(r3v)}")
    bounded = any(max(b["lower"], b["upper"]) > P["post_bound_frac"] for b in out["bound_fractions"].values())

    n_eff_chain = nw * n_post / float(np.max(tau))

    def label(probs, evaluable, n_draws):
        if not converged or not evaluable:
            return "not evaluable"
        lab = post_label(probs, P["post_p_threshold"], min(n_draws, n_eff_chain))
        if p_fit < P["post_misfit_p"]:
            lab = "model misfit (probabilities reported, not a verdict)"
        return lab + ("; prior-bounded" if bounded else "")

    med_theta = [float(np.median(flat[:, j])) for j in range(4)]
    fmed = run_model(S, P, combo, phi_obs, fixed={"theta": med_theta, "m_cal_lo": None,
                                                    "calibration": {"theta": med_theta, "rms": 0.0}})
    out["at_posterior_median"] = {"theta": med_theta, "ratio": float(fmed["phi_ours"] / phi_n26),
                                  "sigma_roots": fmed.get("sigma_roots")}
    out.update({"r2_verdicts": r2v, "r3_verdicts": r3v, "ratios": ratios, "r3_central_roots": centrals, "r3_roots": roots_list,
                "r2_probabilities": p2, "r3_probabilities": p3,
                "r3_evaluable_fraction": len(ev3) / n,
                "n_eff": float(min(n, n_eff_chain)),
                "r2_label": label(p2, True, n),
                "r3_label": label(p3, len(ev3) >= P["post_r3_min_frac"] * n, len(ev3)),
                "ratio_quantiles": [float(q) for q in np.percentile(ratios, [5, 16, 50, 84, 95])],
                "prior_bounded": bounded})
    ctx.log(f"R2/R3-POST sigma_cal={sigma_cal} faint={faint}: data chi2 {chi2:.1f} (bootstrap p {p_fit:.3f}), "
            f"converged {converged} (max tau {np.max(tau):.0f}), R2 {p2} -> {out['r2_label']}; "
            f"R3 {p3} -> {out['r3_label']}")
    return out
