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
    # variant grid (README section 4, step 7)
    "variants": {
        "hmf": ["st", "reed07"],
        "accretion": ["fakhouri_mean", "fakhouri_median", "dekel13"],
        "cal": ["z8", "z7"],
        "sigma_cal": [0.5, 0.7, 0.9],
        "eps_extrap": ["dpl", "const"],
    },
    "run_variants": True,
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


def run_model(S, P, combo, phi_obs):
    """Calibrate, predict R2 and solve R3 for one model combination."""
    lf = inp.BOUWENS21[combo["cal"]]
    z_cal = lf["z"]
    m_grid = np.arange(P["cal_m_bright"], P["cal_m_faint"] + 1e-9, P["cal_dm"])
    hmf_cal = S.hmf(z_cal, combo["hmf"])
    cal = zm.calibrate(S.lnM, hmf_cal, z_cal, S.c, combo["accretion"], combo["sigma_cal"], lf, m_grid)
    out = {"combo": combo, "calibration": cal}
    if cal["rms"] >= P["rms_max"]:
        out["evaluable"] = False
        out["reason"] = f"calibration rms {cal['rms']:.3f} >= {P['rms_max']}"
        return out
    theta = cal["theta"]
    med_cal = zm.muv_median(S.M, z_cal, S.c, theta, combo["accretion"])
    shape_cal = zm.median_shape(S.M, med_cal, P["cal_m_bright"], P["cal_m_faint"])
    floor = shape_cal["m_cal_lo"] if combo["eps_extrap"] == "const" else None
    hmf_z = [zm.dndlnm(S.lnM, S.sig0, d, S.rho_m, combo["hmf"]) for d in S.D_pred]
    med_z = [zm.muv_median(S.M, z, S.c, theta, combo["accretion"], floor) for z in S.z_pred]
    n = inp.N26

    def phi_bin(sigma):
        return zm.bin_average(S.lnM, hmf_z, med_z, sigma, S.dvdz, n["m_lo"], n["m_hi"], P["n_m"])[0]

    phi_ours = phi_bin(combo["sigma_cal"])
    i_mid = len(S.z_pred) // 2
    out.update({
        "evaluable": True,
        "median_shape_zcal": shape_cal,
        "median_shape_z14_5": zm.median_shape(S.M, med_z[i_mid], P["cal_m_bright"], P["cal_m_faint"]),
        "phi_ours": phi_ours,
    })
    # halos in the target bin at z = 14.5: are their z_cal medians inside the calibrated range?
    in_bin = (med_z[i_mid] >= n["m_lo"]) & (med_z[i_mid] <= n["m_hi"])
    if in_bin.any():
        mb = S.M[in_bin]
        lo, hi = shape_cal["m_cal_lo"], shape_cal["m_cal_hi"]
        out["bin_halo_mass_range_z14_5"] = [float(mb.min()), float(mb.max())]
        out["bin_halos_inside_calibrated_range"] = bool(lo is not None and mb.min() >= lo and mb.max() <= hi)
    # R3: required sigma
    sg = np.arange(P["sigma_range"][0], P["sigma_range"][1] + 1e-9, P["sigma_step"])
    phis = np.array([phi_bin(s) for s in sg])
    out["phi_vs_sigma"] = {"sigma": sg.tolist(), "phi": phis.tolist()}
    if not np.all(np.diff(phis) > 0):
        out["r3_evaluable"] = False
        out["r3_reason"] = "phi(sigma) not monotonic on the search range"
        return out
    out["r3_evaluable"] = True
    lam_lo, lam_hi = zm.gehrels(n["n_sources"])
    targets = {"central": phi_obs, "lower": phi_obs * lam_lo / n["n_sources"],
               "upper": phi_obs * lam_hi / n["n_sources"]}
    roots = {}
    for key, tgt in targets.items():
        if phis[0] >= tgt:
            roots[key] = {"value": float(sg[0]), "censored": "le" if phis[0] > tgt else None}
        elif phis[-1] < tgt:
            roots[key] = {"value": float(sg[-1]), "censored": "gt"}
        else:
            f = lambda s: np.log(phi_bin(s)) - np.log(tgt)  # noqa: E731
            roots[key] = {"value": float(optimize.brentq(f, sg[0], sg[-1], xtol=1e-4)), "censored": None}
    out["sigma_roots"] = roots
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

    S = Setup(P)
    checks = {"sigma8": float(S.pk.sigma_R(8.0 / S.c["h"])[0]), "st_normalisation": zm.st_normalisation()}
    ctx.log(f"checks: sigma8 = {checks['sigma8']:.4f}, ST normalisation = {checks['st_normalisation']:.4f}")

    fid = {k: P[k] for k in ("hmf", "accretion", "cal", "sigma_cal", "eps_extrap")}
    fres = run_model(S, P, fid, phi_obs)
    r2 = {"fiducial": fid, "phi_obs": phi_obs, "phi_n26_baseline": phi_n26, "checks": checks,
          "calibration": fres["calibration"], "evaluable": fres["evaluable"]}
    if fres["evaluable"]:
        ratio = fres["phi_ours"] / phi_n26
        mu = fres["phi_ours"] * inp.N26["volume_mpc3"] * P["area_factor"]
        r2.update({"phi_ours": fres["phi_ours"], "ratio_to_n26": ratio,
                   "verdict": r2_verdict(ratio, P["r2_factor"]),
                   "p_tail_ours": zm.poisson_tail(inp.N26["n_sources"], mu),
                   "median_shape_zcal": fres["median_shape_zcal"],
                   "median_shape_z14_5": fres["median_shape_z14_5"],
                   "bin_halo_mass_range_z14_5": fres.get("bin_halo_mass_range_z14_5"),
                   "bin_halos_inside_calibrated_range": fres.get("bin_halos_inside_calibrated_range")})
        ctx.log(f"R2 fiducial: phi_ours = {fres['phi_ours']:.3e}, ratio to N26 baseline = {ratio:.2f} -> {r2['verdict']}")
    else:
        r2["verdict"] = "not evaluable"
        r2["reason"] = fres.get("reason")

    r3 = {"fiducial": fid, "target": P["r3_target"], "conditional_on_r2": r2.get("verdict")}
    if fres.get("r3_evaluable"):
        r3.update({"sigma_roots": fres["sigma_roots"], "verdict": r3_verdict(fres["sigma_roots"], P["r3_target"]),
                   "phi_vs_sigma": fres["phi_vs_sigma"]})
        # descriptive: roots with the floor at 10 M_min
        P10 = dict(P, m_h_min=10 * P["m_h_min"])
        S10 = Setup(P10)
        f10 = run_model(S10, P10, fid, phi_obs)
        r3["sigma_roots_10mmin"] = f10.get("sigma_roots")
        r3["verdict_10mmin"] = r3_verdict(f10["sigma_roots"], P["r3_target"]) if f10.get("r3_evaluable") else "not evaluable"
        ctx.log(f"R3: sigma central = {fres['sigma_roots']['central']}, verdict {r3['verdict']}")
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
                    row["r3"] = r3_verdict(res["sigma_roots"], P["r3_target"])
            else:
                row["reason"] = res.get("reason")
            variants.append(row)
        ev = [v for v in variants if v["evaluable"]]
        n_min = P["robust_min_evaluable"]

        def robustness(rows, key, fid_verdict):
            if len(rows) < n_min:
                return "not assessable"
            return "robust" if all(r[key] == fid_verdict for r in rows) else "calibration-dependent"

        counts2 = {}
        for v in ev:
            counts2[v["r2"]] = counts2.get(v["r2"], 0) + 1
        r2["robustness"] = robustness(ev, "r2", r2.get("verdict")) if r2.get("verdict") != "not evaluable" else "not assessable"
        r2["variant_counts"] = {"evaluable": len(ev), "total": len(variants), "by_verdict": counts2}
        if ev:
            r2["envelope_phi_ours"] = [min(v["phi_ours"] for v in ev), max(v["phi_ours"] for v in ev)]
            r2["envelope_p_tail"] = [zm.poisson_tail(2, min(v["phi_ours"] for v in ev) * inp.N26["volume_mpc3"]),
                                     zm.poisson_tail(2, max(v["phi_ours"] for v in ev) * inp.N26["volume_mpc3"])]
        r2["phi_ours_by_sigma"] = {str(s): v["phi_ours"] for v in ev for s in [v["combo"]["sigma_cal"]]
                                   if {k: v["combo"][k] for k in ("hmf", "accretion", "cal", "eps_extrap")}
                                   == {k: fid[k] for k in ("hmf", "accretion", "cal", "eps_extrap")}}
        ev3 = [v for v in ev if v.get("r3_evaluable")]
        counts3 = {}
        for v in ev3:
            counts3[v["r3"]] = counts3.get(v["r3"], 0) + 1
        r3["robustness"] = robustness(ev3, "r3", r3.get("verdict")) if r3.get("verdict") != "not evaluable" else "not assessable"
        r3["variant_counts"] = {"evaluable": len(ev3), "total": len(variants), "by_verdict": counts3,
                                "not_monotonic": sum(1 for v in ev if not v.get("r3_evaluable"))}
        if ev3:
            sc = [v["sigma_central"]["value"] for v in ev3]
            r3["envelope_sigma_central"] = [min(sc), max(sc)]
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
        med_cal = zm.muv_median(S.M, lf["z"], S.c, theta, fid["accretion"])
        hmf_cal = S.hmf(lf["z"], fid["hmf"])
        med14 = zm.muv_median(S.M, 14.5, S.c, theta, fid["accretion"])
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
    ctx.save("summary", summary)
    return summary
