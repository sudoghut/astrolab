"""M6 Milky Way outer rotation curve: Keplerian decline, mass and systematics (README sections 1-4).

Pre-registration: README sections 1-4 (frozen 2026-11-15). Inputs: the transcribed tables in data/.
Run with:
    python -m astrolab run 009-m06-mw-outer-rotation-curve-decline

R1  power law beyond 19 kpc on J23 Table 3 (verdict) and prior sensitivity.
R2  Einasto + baryon fits for seven baryon models, compared with J23 Table 4 (descriptive).
R3  bias stress tests (exploration).
R4  comparison with Ou et al. 2024 and Eilers et al. 2019 (descriptive).
R5  measured versus extrapolated mass; NFW halo (descriptive).
R6  R6-COV: the tests under correlated covariances calibrated to chi^2 = dof (addendum 2026-11-17).
"""
import csv
from pathlib import Path

import numpy as np
from scipy import optimize

import r6cov
import rc

HERE = Path(__file__).parent

# Tunable knobs (AGENTS.md section 2). Read inside main() and passed on as arguments.
PARAMS = {
    "r_min_powerlaw": 19.0,
    "gamma_target": -0.47, "gamma_tol": 0.05, "s_target": 3.1, "s_tol": 0.3,
    "a_max": 1e5, "a_max_pivot": 1e3,
    "nwalkers": 32, "nsteps": 6000, "burn": 1000, "seed": 0, "seed_check": 1, "seed_diff": 0.01,
    "nsteps_scan": 3000,
    "rho_cr": 134.0,                         # Msun / kpc^3 (1.34e-7 Msun / pc^3)
    "m0_range": [1e10, 1e14], "h_range": [0.0, 20.0], "invn_range": [0.0, 5.0],
    "n_derived": 4000,                       # posterior samples used for R_vir and masses
    "bias_const": [-0.10, -0.05, 0.05, 0.10],
    "bmax_grid": [round(0.005 * i, 3) for i in range(41)],
    "ramp_start": 19.0, "ramp_end": 26.5,
    "quad_frac": [0.05, 0.10, 0.15], "corr_rho": [0.5, 0.99], "corr_r_min": 23.5,
    "r_min_o24_r2": 9.5,
    "nfw_rhos_range": [1e4, 1e10], "nfw_rs_range": [1.0, 100.0],
    "mass_radii": [26.5, 32.4, 100.0],
    "streams": {"Koposov+2023 M(<32.4 kpc)": [32.4, 2.85e11, 0.10e11],
                "Vasiliev+2021 M(<100 kpc)": [100.0, 5.6e11, 0.4e11]},
    "r6_check": True,                        # R6-COV (README 2.6, addendum 2026-11-17)
    "r6_target": 15.0, "r6_high_f": 0.9, "r6_bisect_tol": 1e-4,
    "models": ["E dJ", "E J", "E CM", "G dJ", "G J", "G CM", "B2"],
}


def _csv(name):
    with open(HERE / "data" / name, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def load_inputs():
    t3 = _csv("j23_table3.csv")
    j23 = {k: np.array([float(r[c]) for r in t3]) for k, c in (("R", "R_kpc"), ("V", "Vc_kms"), ("sig", "sigma_Vc_kms"))}
    t4 = {r["model"]: r for r in _csv("j23_table4.csv")}
    bar = {}
    for r in _csv("j23_baryons.csv"):
        try:
            bar.setdefault((r["model"], r["component"]), {})[r["parameter"]] = float(r["value"])
        except ValueError:
            pass
    o = _csv("o24_table1.csv")
    o24 = {"R": np.array([float(r["R_kpc"]) for r in o]), "V": np.array([float(r["vc_kms"]) for r in o]),
           "sig": np.array([0.5 * (float(r["sigma_plus_kms"]) + float(r["sigma_minus_kms"])) for r in o])}
    e = _csv("e19_table1.csv")
    e19 = {"R": np.array([float(r["R_kpc"]) for r in e]), "V": np.array([float(r["vc_kms"]) for r in e]),
           "sig": np.array([0.5 * (float(r["sigma_plus_kms"]) + float(r["sigma_minus_kms"])) for r in e])}
    return j23, t4, bar, o24, e19


def baryon_model(name, bar):
    """README 2.2: bulge and discs of a baryon model (masses in Msun)."""
    if name == "B2":
        b = bar[("B2", "bulge")]
        model = {"bulge": ("hernquist", b["M_bulge"] * 1e10, b["r_b"]), "discs": []}
        d = bar[("B2", "disk")]
        model["discs"].append((d["M_thin"] * 1e10, d["L_thin"], d["H_thin"]))
        for comp in ("cold dust", "warm dust", "H2 gas", "HI gas"):
            g = bar[("B2", comp)]
            model["discs"].append((g["M"], g["R_d"], g["z_d"]))
        return model
    bk, dk = name.split()
    b = bar[(bk, "bulge")]
    d = bar[(dk, "disk")]
    return {"bulge": ("point", b["M_bulge"] * 1e10, None),
            "discs": [(d["M_thin"] * 1e10, d["L_thin"], d["H_thin"]),
                      (d["M_thick"] * 1e10, d["L_thick"], d["H_thick"])]}


def component_mass(model):
    return model["bulge"][1] + sum(m for m, _, _ in model["discs"])


# ------------------------------------------------------------------ R1 ----

def powerlaw_fit(R, V, sig, P, pivot=1.0, a_max=None, log_a=False, cov=None, nsteps=None, seed=None, double=True):
    """README 2.1 posterior; sampled in (V at the inverse-variance-weighted radius, gamma) for mixing."""
    a_max = P["a_max"] if a_max is None else a_max
    cov_inv = None if cov is None else np.linalg.inv(cov)
    rs = float(np.sum(R / sig ** 2) / np.sum(1 / sig ** 2))
    args = (R, V, sig, pivot, a_max, cov_inv, log_a, rs)
    nll = lambda th: -rc.powerlaw_lnpost(th, *args) if np.isfinite(rc.powerlaw_lnpost(th, *args)) else 1e30
    start = optimize.minimize(nll, [float(np.interp(rs, R, V)), -0.4], method="Nelder-Mead").x
    seed = P["seed"] if seed is None else seed
    steps = nsteps or P["nsteps"]
    chain, tau, ok = rc.run_emcee(rc.powerlaw_lnpost, np.array(start), args, P["nwalkers"], steps, P["burn"], seed)
    doubled = False
    if not ok and double and nsteps is None:
        chain, tau, ok = rc.run_emcee(rc.powerlaw_lnpost, np.array(start), args, P["nwalkers"], 2 * steps, P["burn"], seed)
        doubled = True
    g = chain[:, 1]
    p0 = float(np.mean(g >= 0))
    sig1, lb = rc.one_sided_sigma(p0, len(g))
    return {"median_gamma": float(np.median(g)), "p16": float(np.percentile(g, 16)), "p84": float(np.percentile(g, 84)),
            "S": rc.s_statistic(g), "p_gamma_ge_0": p0, "one_sided_sigma": sig1, "one_sided_is_lower_bound": lb,
            "tau": tau, "converged": ok, "steps_doubled": doubled, "sampling_radius_kpc": rs,
            "contains_minus_half": bool(np.percentile(g, 16) <= -0.5 <= np.percentile(g, 84))}


def delta_chi2(R, V, sig):
    flat = np.sum(((V - np.average(V, weights=sig ** -2)) / sig) ** 2)
    f = lambda th: np.sum(((V - th[0] * R ** th[1]) / sig) ** 2)
    best = optimize.minimize(f, [np.median(V) * np.median(R) ** 0.4, -0.4], method="Nelder-Mead",
                             options={"xatol": 1e-10, "fatol": 1e-10, "maxiter": 20000})
    d = float(flat - best.fun)
    return {"delta_chi2": d, "sigma_1dof": float(np.sqrt(max(d, 0))), "gamma_best": float(best.x[1])}


# ------------------------------------------------------------------ R2 ----

def einasto_lnpost(theta, R, V, sig, vb2, P):
    M0, h, inv_n = theta
    if not (P["m0_range"][0] <= M0 <= P["m0_range"][1] and P["h_range"][0] < h <= P["h_range"][1]
            and P["invn_range"][0] < inv_n <= P["invn_range"][1]):
        return -np.inf
    v2 = vb2 + rc.G * rc.einasto_mass(R, M0, h, inv_n) / R
    if np.any(v2 <= 0) or not np.all(np.isfinite(v2)):
        return -np.inf
    return -0.5 * np.sum(((V - np.sqrt(v2)) / sig) ** 2)


def einasto_lnpost_logm0(theta, R, V, sig, vb2, P):
    lm0, h, inv_n = theta
    if not (np.log10(P["m0_range"][0]) <= lm0 <= np.log10(P["m0_range"][1])):
        return -np.inf
    return einasto_lnpost([10 ** lm0, h, inv_n], R, V, sig, vb2, P)


def nfw_lnpost(theta, R, V, sig, vb2, P):
    lrho, lrs = theta
    if not (np.log10(P["nfw_rhos_range"][0]) <= lrho <= np.log10(P["nfw_rhos_range"][1])
            and np.log10(P["nfw_rs_range"][0]) <= lrs <= np.log10(P["nfw_rs_range"][1])):
        return -np.inf
    v2 = vb2 + rc.G * rc.nfw_mass(R, 10 ** lrho, 10 ** lrs) / R
    return -0.5 * np.sum(((V - np.sqrt(v2)) / sig) ** 2)


def summarise(x):
    x = np.asarray([v for v in x if v is not None and np.isfinite(v)])
    if x.size == 0:
        return None
    return {"median": float(np.median(x)), "p16": float(np.percentile(x, 16)), "p84": float(np.percentile(x, 84))}


def derived_masses(chain, mass_fn_of, m_bar, P, radii, m_bar_sphere=None):
    """Per-sample R_vir (primary: DM-only; secondary: DM + all of M_bar), M_dyn and enclosed masses."""
    rng = np.random.default_rng(P["seed"])
    idx = rng.choice(len(chain), size=min(P["n_derived"], len(chain)), replace=False)
    out = {"rvir_dm": [], "rvir_tot": [], "mdyn_dm": [], "mdyn_tot": [],
           "no_root_dm": 0, "no_root_wide_dm": 0, "no_root_tot": 0, "no_root_wide_tot": 0}
    out.update({f"m_lt_{r}": [] for r in radii})
    for i in idx:
        mfn = mass_fn_of(chain[i])
        for key, extra in (("dm", 0.0), ("tot", m_bar)):
            rv = rc.r_vir(mfn, P["rho_cr"], extra)
            if rv is None:
                out[f"no_root_{key}"] += 1
                rv = rc.r_vir(mfn, P["rho_cr"], extra, bracket=(1.0, 1e4))
                if rv is None:
                    out[f"no_root_wide_{key}"] += 1
            out[f"rvir_{key}"].append(rv)
            out[f"mdyn_{key}"].append(None if rv is None else m_bar + mfn(rv))
        for r in radii:
            out[f"m_lt_{r}"].append((m_bar_sphere or {}).get(r, m_bar) + mfn(r))
    return {k: (summarise(v) if isinstance(v, list) else v) for k, v in out.items()}


def fit_halo(kind, R, V, sig, vb2, P, start, seed=None):
    lnp = {"einasto": einasto_lnpost, "einasto_logm0": einasto_lnpost_logm0, "nfw": nfw_lnpost}[kind]
    nll = lambda th: -lnp(th, R, V, sig, vb2, P) if np.isfinite(lnp(th, R, V, sig, vb2, P)) else 1e30
    best = optimize.minimize(nll, start, method="Nelder-Mead", options={"maxiter": 20000, "xatol": 1e-4, "fatol": 1e-6})
    chain, tau, ok = rc.run_emcee(lnp, np.array(best.x), (R, V, sig, vb2, P), P["nwalkers"], P["nsteps"], P["burn"],
                                  P["seed"] if seed is None else seed)
    if not ok:
        chain, tau, ok = rc.run_emcee(lnp, np.array(best.x), (R, V, sig, vb2, P), P["nwalkers"], 2 * P["nsteps"],
                                      P["burn"], P["seed"] if seed is None else seed)
    return chain, tau, ok


def einasto_r2(R, V, sig, model, m_bar, P, radii=(), kind="einasto", m_bar_sphere=None):
    vb2 = np.array([rc.baryon_v2(r, model) for r in R])
    start = [3.7e11, 12.0, 2.4] if kind == "einasto" else [np.log10(3.7e11), 12.0, 2.4]
    chain, tau, ok = fit_halo(kind, R, V, sig, vb2, P, start)
    if kind == "einasto_logm0":
        chain = chain.copy()
        chain[:, 0] = 10 ** chain[:, 0]
    mfn = lambda th: (lambda r: rc.einasto_mass(r, th[0], th[1], th[2]))
    d = derived_masses(chain, mfn, m_bar, P, radii, m_bar_sphere)
    d.update({"M0": summarise(chain[:, 0]), "h": summarise(chain[:, 1]), "n": summarise(1 / chain[:, 2]),
              "tau": tau, "converged": ok})
    return d


# ---------------------------------------------------------------- R6-COV ----

R6_COVS = {"se_2": ("se", 2.0), "se_4": ("se", 4.0), "se_8": ("se", 8.0), "global": ("global", None),
           "fractional": ("fractional", None)}


def r6_tests(R, V, sig, vb2, kind, value, m_bar, P, sel):
    """T1-T3 of README 2.6 at one covariance value."""
    C = r6cov.make_cov(kind, value, R, V, sig)
    cho = r6cov.linalg.cho_factor(C)
    pl = r6cov.powerlaw_tests(R[sel], V[sel], C[np.ix_(sel, sel)])
    halos = {}
    for h in ("einasto", "nfw", "lcdm"):
        fit = r6cov.fit_halo(h, R, V, vb2, cho)
        fit.update(r6cov.m_vir(h, fit["x"], m_bar, P["rho_cr"]))
        halos[h] = fit
    t3 = {}
    for h in ("nfw", "lcdm"):
        ok = halos["einasto"]["converged"] and halos[h]["converged"]
        t3[h] = float(halos[h]["chi2"] - halos["einasto"]["chi2"]) if ok else None
    return {"value": float(value), "max_corr_fraction": r6cov.max_corr_fraction(kind, value, V, sig),
            "powerlaw": pl, "halos": halos, "dchi2_nfw": t3["nfw"], "dchi2_lcdm": t3["lcdm"]}


def r6_cov(ctx, j23, model, m_bar, P):
    """README 2.6 (R6-COV): calibrate each covariance on the free Einasto fit, then T1-T3 and labels."""
    R, V, sig = j23["R"], j23["V"], j23["sig"]
    vb2 = np.array([rc.baryon_v2(r, model) for r in R])
    sel = R > P["r_min_powerlaw"]
    target = P["r6_target"]
    spread = float(np.sqrt(2 * target))
    import scipy
    out = {"covariances": {}, "target": target, "spread": spread, "scipy_version": scipy.__version__}
    if scipy.__version__ != "1.13.1":
        ctx.log(f"WARNING R6-COV: scipy {scipy.__version__}, pre-registered 1.13.1 (README 2.6)")
    for name, kind in R6_COVS.items():
        if kind[0] == "fractional":
            c_max = 0.99 * float(np.min(sig / V))
            grid = np.array([k * c_max / 99 for k in range(100)])
        else:
            grid = np.round(np.arange(100) * 0.01, 2)
        memo = {}

        def chi2_at(v, kind=kind, memo=memo):
            if v not in memo:
                cho = r6cov.linalg.cho_factor(r6cov.make_cov(kind, v, R, V, sig))
                fit = r6cov.fit_halo("einasto", R, V, vb2, cho)
                memo[v] = fit["chi2"] if fit["converged"] else None
            return memo[v]

        cal = r6cov.calibrate(chi2_at, grid, target, P["r6_bisect_tol"])
        res = {"kind": list(kind), "status": cal["status"], "value": cal["value"], "curve": cal["curve"]}
        if cal["value"] is not None:
            res["tests"] = r6_tests(R, V, sig, vb2, kind, cal["value"], m_bar, P, sel)
            res["high_f"] = bool(res["tests"]["max_corr_fraction"] > P["r6_high_f"])
        side = {}
        for tag, t in (("minus", target - spread), ("plus", target + spread)):
            c2 = r6cov.calibrate(chi2_at, grid, t, P["r6_bisect_tol"])
            side[tag] = {"target": t, "status": c2["status"], "value": c2["value"]}
            if c2["status"] == "calibrated":
                side[tag]["tests"] = r6_tests(R, V, sig, vb2, kind, c2["value"], m_bar, P, sel)
        res["spread_points"] = side
        out["covariances"][name] = res
        ctx.log(f"R6-COV {name}: {cal['status']} at {cal['value']}")

    def vals(getter):
        v = {}
        for name, res in out["covariances"].items():
            if res["status"] != "calibrated":
                v[name] = None
                continue
            v[name] = getter(res["tests"])
        return v

    # contrast (README 2.6 reading; no label): independent errors rescaled so that the Einasto chi^2 = target
    chi2_0 = out["covariances"]["se_2"]["curve"][0][1]          # f = 0: independent errors (any kernel)
    if chi2_0 is not None:
        scale = float(np.sqrt(chi2_0 / target))
        Cs = np.diag((sig * scale) ** 2)
        out["rescaled_independent"] = {"chi2_f0": chi2_0, "scale": scale,
                                       "powerlaw": r6cov.powerlaw_tests(R[sel], V[sel], Cs[np.ix_(sel, sel)])}
    flags = {n: r.get("high_f", False) for n, r in out["covariances"].items() if r["status"] == "calibrated"}
    pl = lambda key, ok: (lambda t: t["powerlaw"][key] if t["powerlaw"][ok] else None)
    values = {"t1": vals(pl("sigma_flat", "t1_evaluable")), "t2": vals(pl("pref_kepler", "t2_evaluable")),
              "t3_nfw": vals(lambda t: t["dchi2_nfw"]), "t3_lcdm": vals(lambda t: t["dchi2_lcdm"])}
    rule = {"t1": "t1", "t2": "t2", "t3_nfw": "t3", "t3_lcdm": "t3"}
    out["values"] = values
    out["high_f"] = flags
    out["labels"] = {k: r6cov.label(rule[k], v, flags) for k, v in values.items()}
    ctx.log(f"R6-COV labels: {out['labels']}")
    return out


# ---------------------------------------------------------------- main ----

def main(ctx):
    P = dict(PARAMS)
    j23, t4, bar, o24, e19 = load_inputs()
    # checks (README section 4, step 1)
    assert len(j23["R"]) == 18 and len(t4) == 8 and len(o24["R"]) == 37 and len(e19["R"]) == 38
    assert abs(j23["V"][j23["R"] == 19.5][0] - 206.25) < 1e-9 and abs(j23["V"][j23["R"] == 26.5][0] - 175.68) < 1e-9
    models = {m: baryon_model(m, bar) for m in P["models"]}
    mbar = {m: float(t4[m]["Mbar_1e11Msun"]) * 1e11 for m in P["models"]}
    sums = {m: component_mass(models[m]) for m in P["models"]}
    for m in P["models"]:
        assert abs(sums[m] - mbar[m]) <= 0.005e11, (m, sums[m], mbar[m])
    ctx.log("inputs checked: row counts, Table 3 anchors, baryon mass sums")

    # ------------------------------------------------------------ R1 ----
    sel = j23["R"] > P["r_min_powerlaw"]
    R, V, sig = j23["R"][sel], j23["V"][sel], j23["sig"][sel]
    base = powerlaw_fit(R, V, sig, P)
    check = powerlaw_fit(R, V, sig, P, seed=P["seed_check"])
    seed_rerun = None
    if abs(check["median_gamma"] - base["median_gamma"]) > P["seed_diff"]:
        seed_rerun = {"first_base": base, "first_check": check}
        P2 = dict(P, nsteps=2 * P["nsteps"])
        base = powerlaw_fit(R, V, sig, P2, double=False)
        check = powerlaw_fit(R, V, sig, P2, seed=P["seed_check"], double=False)
    ok = (abs(base["median_gamma"] - P["gamma_target"]) <= P["gamma_tol"]
          and abs(base["S"] - P["s_target"]) <= P["s_tol"])
    pivot = float(np.sum(R / sig ** 2) / np.sum(1 / sig ** 2))
    r1 = {"bins": R.tolist(), "base": base, "seed_check": check, "seed_rerun": seed_rerun,
          "seed_check_S_diff": abs(check["S"] - base["S"]), "converged": bool(base["converged"]),
          "verdict": "reproduced" if ok else "not reproduced",
          "sensitivity_log_a": powerlaw_fit(R, V, sig, P, log_a=True),
          "sensitivity_pivot": dict(powerlaw_fit(R, V, sig, P, pivot=pivot, a_max=P["a_max_pivot"]), pivot_kpc=pivot),
          "delta_chi2": delta_chi2(R, V, sig),
          "leave_one_out": {str(r): powerlaw_fit(np.delete(R, i), np.delete(V, i), np.delete(sig, i), P,
                                                 nsteps=P["nsteps_scan"])["S"] for i, r in enumerate(R)}}
    ctx.log(f"R1: median gamma {base['median_gamma']:.3f}, S {base['S']:.2f} (converged {base['converged']}, "
            f"tau {base['tau']:.1f}) -> {r1['verdict']}; "
            f"log-A S {r1['sensitivity_log_a']['S']:.2f}; pivot S {r1['sensitivity_pivot']['S']:.2f}")
    ctx.save("r1", r1)

    # ------------------------------------------------------------ R2 ----
    r2 = {"models": {}}
    for m in P["models"]:
        res = einasto_r2(j23["R"], j23["V"], j23["sig"], models[m], mbar[m], P)
        res["table4_mdyn"] = float(t4[m]["Mdyn_TW"]) * 1e11
        res["diff_primary"] = res["mdyn_dm"]["median"] - res["table4_mdyn"]
        res["diff_secondary"] = res["mdyn_tot"]["median"] - res["table4_mdyn"]
        res["rvir_dm_minus_121"] = res["rvir_dm"]["median"] - 121.03
        res["rvir_tot_minus_121"] = res["rvir_tot"]["median"] - 121.03
        r2["models"][m] = res
        ctx.log(f"R2 {m}: Mdyn {res['mdyn_dm']['median']:.3e} (DM rule), {res['mdyn_tot']['median']:.3e} (total rule); "
                f"Table 4 {res['table4_mdyn']:.3e}; Rvir {res['rvir_dm']['median']:.1f} / {res['rvir_tot']['median']:.1f} kpc")
    six = [m for m in P["models"] if m != "B2"]
    r2["six_mean"] = {"ours_primary": float(np.mean([r2["models"][m]["mdyn_dm"]["median"] for m in six])),
                      "ours_secondary": float(np.mean([r2["models"][m]["mdyn_tot"]["median"] for m in six])),
                      "table4": float(np.mean([r2["models"][m]["table4_mdyn"] for m in six]))}
    r2["variant_logm0_EdJ"] = einasto_r2(j23["R"], j23["V"], j23["sig"], models["E dJ"], mbar["E dJ"], P,
                                         kind="einasto_logm0")
    r2["j23_rvir_kpc"] = 121.03
    ctx.save("r2", r2)

    # ------------------------------------------------------------ R3 ----
    r3 = {"constant_gamma": {}, "constant_mass_EdJ": {}, "ramp": {}, "quadrature": {}, "correlated": {}}
    for b in P["bias_const"]:
        f = 1.0 / (1 - b)
        r3["constant_gamma"][str(b)] = powerlaw_fit(R, V * f, sig * f, P, nsteps=P["nsteps_scan"])["median_gamma"]
        res = einasto_r2(j23["R"], j23["V"] * f, j23["sig"] * f, models["E dJ"], mbar["E dJ"], P)
        r3["constant_mass_EdJ"][str(b)] = {"mdyn_dm": res["mdyn_dm"], "mdyn_tot": res["mdyn_tot"]}
    r3["constant_gamma"]["0.0"] = powerlaw_fit(R, V, sig, P, nsteps=P["nsteps_scan"])["median_gamma"]
    # Monte Carlo noise of S at the scan length (5 seeds at b = 0), the basis of the monotonicity tolerance
    s_noise = [powerlaw_fit(R, V, sig, P, nsteps=P["nsteps_scan"], seed=sd)["S"] for sd in (10, 11, 12, 13, 14)]
    r3["s_noise_sd_scan"] = float(np.std(s_noise, ddof=1))
    s_curve = []
    for bmax in P["bmax_grid"]:
        b = np.clip((R - P["ramp_start"]) / (P["ramp_end"] - P["ramp_start"]), 0, 1) * bmax
        f = 1.0 / (1 - b)
        s_curve.append(powerlaw_fit(R, V * f, sig * f, P, nsteps=P["nsteps_scan"])["S"])
    crossing = next((bm for bm, s in zip(P["bmax_grid"], s_curve) if s < 2), None)
    r3["ramp"] = {"b_max": P["bmax_grid"], "S": s_curve, "first_below_2": crossing,
                  "monotonic_tolerance": 3 * r3["s_noise_sd_scan"],
                  "monotonic": bool(np.all(np.diff(s_curve) <= 3 * r3["s_noise_sd_scan"]))}
    if crossing is not None:
        b = np.clip((R - P["ramp_start"]) / (P["ramp_end"] - P["ramp_start"]), 0, 1) * crossing
        f = 1.0 / (1 - b)
        r3["ramp"]["at_crossing"] = {"log_a": powerlaw_fit(R, V * f, sig * f, P, log_a=True),
                                     "pivot": powerlaw_fit(R, V * f, sig * f, P, pivot=pivot, a_max=P["a_max_pivot"])}
    for q in P["quad_frac"]:
        r3["quadrature"][str(q)] = powerlaw_fit(R, V, np.hypot(sig, q * V), P, nsteps=P["nsteps_scan"])["S"]
    outer = R >= P["corr_r_min"]
    for rho in P["corr_rho"]:
        cov = np.diag(sig ** 2)
        for i in range(len(R)):
            for j in range(len(R)):
                if i != j and outer[i] and outer[j]:
                    cov[i, j] = rho * sig[i] * sig[j]
        r3["correlated"][str(rho)] = powerlaw_fit(R, V, sig, P, cov=cov, nsteps=P["nsteps_scan"])["S"]
    ctx.log(f"R3: ramp first S<2 at b_max = {crossing}; quadrature {r3['quadrature']}; correlated {r3['correlated']}")
    ctx.save("r3", r3)

    # ------------------------------------------------------------ R4 ----
    r4 = {}
    for name, cur in (("O24", o24), ("E19", e19)):
        inside = (j23["R"] >= cur["R"].min()) & (j23["R"] <= cur["R"].max())
        vi = np.interp(j23["R"][inside], cur["R"], cur["V"])
        si = np.interp(j23["R"][inside], cur["R"], cur["sig"])
        d = (j23["V"][inside] - vi) / np.hypot(j23["sig"][inside], si)
        r4[f"diff_{name}"] = {"R": j23["R"][inside].tolist(), "dV": (j23["V"][inside] - vi).tolist(),
                              "pull": d.tolist(), "chi2": float(np.sum(d ** 2)), "n": int(inside.sum())}
    so = o24["R"] > P["r_min_powerlaw"]
    po = float(np.sum(o24["R"][so] / o24["sig"][so] ** 2) / np.sum(1 / o24["sig"][so] ** 2))
    Ro, Vo, so_sig = o24["R"][so], o24["V"][so], o24["sig"][so]
    r4["r1_on_O24"] = {"base": powerlaw_fit(Ro, Vo, so_sig, P),
                       "seed_check": powerlaw_fit(Ro, Vo, so_sig, P, seed=P["seed_check"]),
                       "log_a": powerlaw_fit(Ro, Vo, so_sig, P, log_a=True),
                       "pivot": dict(powerlaw_fit(Ro, Vo, so_sig, P, pivot=po, a_max=P["a_max_pivot"]), pivot_kpc=po),
                       "delta_chi2": delta_chi2(Ro, Vo, so_sig),
                       "n_bins": int(so.sum()), "j23_gamma": -0.56}
    sr = o24["R"] >= P["r_min_o24_r2"]
    r4["r2_on_O24"] = {}
    for m in P["models"]:
        res = einasto_r2(o24["R"][sr], o24["V"][sr], o24["sig"][sr], models[m], mbar[m], P)
        r4["r2_on_O24"][m] = {"mdyn_dm": res["mdyn_dm"], "mdyn_tot": res["mdyn_tot"],
                              "table4_O23": float(t4[m]["Mdyn_O23"]) * 1e11}
    ctx.save("r4", r4)

    # ------------------------------------------------------------ R5 ----
    radii = P["mass_radii"]
    vr = float(j23["V"][-1] ** 2 * j23["R"][-1] / rc.G)
    med = models["E dJ"]
    m_sph = {r: med["bulge"][1] + sum(rc.disc_mass_sphere(r, M, L, H) for M, L, H in med["discs"]) for r in radii}
    ein = einasto_r2(j23["R"], j23["V"], j23["sig"], med, mbar["E dJ"], P, radii=radii, m_bar_sphere=m_sph)
    vb2 = np.array([rc.baryon_v2(r, models["E dJ"]) for r in j23["R"]])
    chain, tau, ok = fit_halo("nfw", j23["R"], j23["V"], j23["sig"], vb2, P, [7.0, 1.2])
    nfw = derived_masses(chain, lambda th: (lambda r: rc.nfw_mass(r, 10 ** th[0], 10 ** th[1])), mbar["E dJ"], P, radii, m_sph)
    nfw.update({"rho_s": summarise(10 ** chain[:, 0]), "r_s": summarise(10 ** chain[:, 1]), "tau": tau, "converged": ok})
    r5 = {"v2r_over_G_26.5": vr, "baryon_mass_in_sphere": m_sph, "einasto_EdJ": ein, "nfw_EdJ": nfw, "streams": P["streams"],
          "note": "enclosed masses use the baryon mass inside each sphere (numerical); stream masses are cross-model, order of magnitude"}
    ctx.log(f"R5: V^2R/G(26.5) {vr:.3e}; Einasto Mvir {ein['mdyn_dm']['median']:.3e}; NFW Mvir {nfw['mdyn_dm']['median']:.3e}")
    ctx.save("r5", r5)
    out = {}
    if P["r6_check"]:
        r6 = r6_cov(ctx, j23, models["E dJ"], mbar["E dJ"], P)
        ctx.save("r6", r6)
        out["r6"] = r6["labels"]
    return {**out, "r1": r1["verdict"], "gamma": base["median_gamma"], "S": base["S"],
            "six_mean": r2["six_mean"], "ramp_crossing": crossing}
