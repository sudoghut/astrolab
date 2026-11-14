"""M1: DESI DR2 BAO and evolving dark energy (pre-registration: README sections 1-4).

Run with:      python -m astrolab run 002-m01-desi-bao-evolving-dark-energy
Explore with:  python -m astrolab explore 002-m01-desi-bao-evolving-dark-energy --tag <topic> --set KEY=VALUE

R1  BAO only, LCDM: Omega_m and h r_d (posterior means, 68% half-widths).
R2  DESI + compressed CMB prior (theta_*, omega_b, omega_bc): Delta chi2_MAP under readings A and B.
R3  No CMB: DESI alone, DESI + Pantheon+, DESI + Union3: Delta chi2_MAP.
"""
import numpy as np

from astrolab import cosmo, infer

# Tunable knobs (AGENTS.md section 2). Read inside main() and passed on as arguments.
PARAMS = {
    "sn_zmin": 0.01,                 # Pantheon+ cut on zHD (pre-registered)
    "n_starts": 20,                  # random starts per fit, plus nested and paper starts
    "seed": 0,
    "r1_walkers": 32, "r1_steps": 4000,
    "r2_walkers": 40, "r2_steps": 6000,   # secondary (posterior means of w0, wa)
    "r2_mcmc": True,
    "k_check": True,
    "mnu": 0.06,
    "tol_dchi2": 1.0, "tol_r1_sigma": 0.3, "tol_r1_err": 0.2,   # pre-registered (README section 2)
    "drop_z": [],                    # exploration: BAO effective redshifts to leave out
}

RAW = "https://raw.githubusercontent.com/CobayaSampler/"
BAO_DIR = RAW + "bao_data/master/desi_bao_dr2/"
SN = {"pantheonplus": (RAW + "sn_data/master/PantheonPlus/Pantheon+SH0ES.dat",
                       RAW + "sn_data/master/PantheonPlus/Pantheon+SH0ES_STAT+SYS.cov"),
      "union3": (RAW + "sn_data/master/Union3/lcparam_full.txt",
                 RAW + "sn_data/master/Union3/mag_covmat.txt")}
# DESI DR2 Appendix A, Eqs. 35-36; theta_* to 6 digits from cmbant/PlanckEarlyLCDM (plan 010)
CMB_MEAN = np.array([0.0104103, 0.02223, 0.14208])
CMB_COV = 1e-9 * np.array([[0.006621, 0.12444, -1.1929],
                           [0.12444, 21.344, -94.001],
                           [-1.1929, -94.001, 1488.4]])
# paper targets (Eq. 17, Table 6) and paper points (Table 5) used as extra starts
TARGET = {"R1": {"Om": (0.2975, 0.0086), "hrd": (101.54, 0.73)},
          "R2": -8.0, "desi": -4.7, "desi_pantheonplus": -4.9, "desi_union3": -10.1}
PAPER_POINT = {"desi": (0.352, -0.48, -1.34), "desi_pantheonplus": (0.298, -0.888, -0.17),
               "desi_union3": (0.328, -0.70, -0.99), "R2": (0.353, 63.7, -0.43, -1.72)}
W_BOUNDS = [(-3.0, 1.0), (-3.0, 2.0)]


def w_constraint(x):
    return -(x[-2] + x[-1]) - 1e-9          # w0 + wa <= -1e-9


# ---------------------------------------------------------------- data
def load_bao(ctx, drop_z):
    mean_p = ctx.http(BAO_DIR + "desi_gaussian_bao_ALL_GCcomb_mean.txt", label="DESI DR2 BAO mean")
    cov_p = ctx.http(BAO_DIR + "desi_gaussian_bao_ALL_GCcomb_cov.txt", label="DESI DR2 BAO cov")
    rows = [l.split() for l in mean_p.read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.startswith("#")]
    z = np.array([float(r[0]) for r in rows])
    val = np.array([float(r[1]) for r in rows])
    kind = [r[2] for r in rows]
    cov = np.loadtxt(cov_p)
    keep = np.array([not any(abs(zz - d) < 1e-6 for d in drop_z) for zz in z])
    cov = cov[np.ix_(keep, keep)]
    return {"z": z[keep], "val": val[keep], "kind": [k for k, m in zip(kind, keep) if m],
            "cinv": np.linalg.inv(cov), "n": int(keep.sum())}


def load_sn(ctx, name, zmin):
    dat_url, cov_url = SN[name]
    dat_p = ctx.http(dat_url, label=f"{name} data")
    cov_p = ctx.http(cov_url, label=f"{name} covariance")
    if name == "pantheonplus":
        lines = dat_p.read_text(encoding="utf-8").splitlines()
        cols = lines[0].split()
        arr = [l.split() for l in lines[1:] if l.strip()]
        get = lambda c: np.array([float(r[cols.index(c)]) for r in arr])
        zcmb, zhel, mag = get("zHD"), get("zHEL"), get("m_b_corr")
        flat = np.loadtxt(cov_p)
        n = int(flat[0])
        cov = flat[1:].reshape(n, n)
        keep = zcmb > zmin
    else:   # Union3: Cobaya reads zcmb and mb, zhel = zcmb, covariance from mag_covmat only
        rows = [l.split() for l in dat_p.read_text(encoding="utf-8").splitlines()
                if l.strip() and not l.startswith("#")]
        zcmb = np.array([float(r[1]) for r in rows])
        zhel = zcmb.copy()
        mag = np.array([float(r[4]) for r in rows])
        flat = np.loadtxt(cov_p)
        n = int(flat[0])
        cov = flat[1:].reshape(n, n)
        keep = np.ones(n, dtype=bool)
    cov = cov[np.ix_(keep, keep)]
    return {"zcmb": zcmb[keep], "zhel": zhel[keep], "mag": mag[keep],
            "cinv": np.linalg.inv(cov), "n": int(keep.sum())}


# ---------------------------------------------------------------- models
def bao_pred_late(bao, Om, hrd, w0=-1.0, wa=0.0):
    dm, dh, dv = cosmo.bao_late(Om, hrd, bao["z"], w0, wa)
    pick = {"DM_over_rs": dm, "DH_over_rs": dh, "DV_over_rs": dv}
    return np.array([pick[k][i] for i, k in enumerate(bao["kind"])])


def bao_pred_full(bao, b):
    zu, inv = np.unique(bao["z"], return_inverse=True)
    dm = b.DM(zu)[inv]
    dh = b.DH(zu)[inv]
    dv = (bao["z"] * dm ** 2 * dh) ** (1.0 / 3.0)
    rd = b.rd()
    pick = {"DM_over_rs": dm, "DH_over_rs": dh, "DV_over_rs": dv}
    return np.array([pick[k][i] for i, k in enumerate(bao["kind"])]) / rd


def chi2_bao_late(bao, x, w=True):
    Om, hrd = x[0], x[1]
    w0, wa = (x[2], x[3]) if w else (-1.0, 0.0)
    return infer.gaussian_chi2(bao_pred_late(bao, Om, hrd, w0, wa) - bao["val"], bao["cinv"])


def chi2_sn(sn, Om, w0, wa):
    dl = (1.0 + sn["zhel"]) * cosmo.late_dc(Om, sn["zcmb"], w0, wa)    # in units of c/H0
    mu = 5.0 * np.log10(dl)
    return infer.chi2_marg_offset(sn["mag"] - mu, sn["cinv"])


def chi2_r2(bao, x, reading, mnu, K, w=True):
    H0, ob, oc = x[0], x[1], x[2]
    w0, wa = (x[3], x[4]) if w else (-1.0, 0.0)
    b = cosmo.Background(H0, ob, oc, w0=w0, wa=wa, mnu=mnu)
    if not np.isfinite(b.omde) or b.omde <= 0:
        return np.inf
    c = infer.gaussian_chi2(bao_pred_full(bao, b) - bao["val"], bao["cinv"])
    obc = b.ombc + (cosmo.omega_nu_today(mnu) if reading == "A" else 0.0)
    cm = np.array([b.theta_star(K), ob, obc])
    return c + infer.gaussian_chi2(cm - CMB_MEAN, np.linalg.inv(CMB_COV))


# ---------------------------------------------------------------- fits
def fit_pair(f_lcdm, f_w, b_lcdm, paper_x, n_starts, seed):
    """Fit LCDM and w0waCDM; the w0wa fit also starts from the nested optimum and the paper."""
    r0 = infer.minimize_multistart(f_lcdm, b_lcdm, n_starts=n_starts, seed=seed)
    out = {"lcdm": summarise(r0)}
    if not r0["converged"]:
        out.update(valid=False, reason="LCDM fit did not converge")
        return out
    nested = list(r0["x"]) + [-1.0, -1e-6]
    r1 = infer.minimize_multistart(f_w, b_lcdm + W_BOUNDS, n_starts=n_starts, seed=seed + 1,
                                   constraint=w_constraint, x0_extra=[nested, paper_x(r0["x"])])
    out["w0wa"] = summarise(r1)
    if not r1["converged"]:
        out.update(valid=False, reason="w0waCDM fit did not converge")
        return out
    d = r1["f"] - r0["f"]
    valid = (r0["n_agree"] >= 3 and r1["n_agree"] >= 3 and r1["f"] <= r0["f"] + 1e-3)
    out.update(valid=bool(valid), dchi2=float(d), sigma=infer.sigma_from_dchi2(d),
               reason=None if valid else "fit-validity check failed (agreement or nesting)")
    return out


def summarise(r):
    return {"chi2": r["f"], "x": None if r["x"] is None else [float(v) for v in r["x"]],
            "converged": r["converged"], "n_conv": r["n_conv"], "n_agree": r["n_agree"],
            "x_spread": r["x_spread"], "n_ok": r["n_ok"]}


def verdict_dchi2(fit, target, tol):
    if not fit.get("valid"):
        return "failed fit"
    return "reproduced" if abs(fit["dchi2"] - target) <= tol else "not reproduced"


def mc_summary(samples, tau, nwalkers, names):
    n_eff = samples.shape[0] / np.max(tau) if np.all(np.isfinite(tau)) else float("nan")
    out = {}
    for i, n in enumerate(names):
        s = samples[:, i]
        lo, hi = np.percentile(s, [15.865, 84.135])
        out[n] = {"mean": float(s.mean()), "sigma68": float((hi - lo) / 2.0),
                  "mc_err": float(s.std() / np.sqrt(n_eff))}
    return out, float(n_eff)


# ---------------------------------------------------------------- main
def main(ctx):
    P = dict(PARAMS)
    bao = load_bao(ctx, P["drop_z"])
    ctx.log(f"BAO points: {bao['n']}")
    out = {"params": P, "targets": TARGET}

    # R1: BAO only, LCDM
    b_r1 = [(0.01, 0.99), (50.0, 150.0)]
    f_r1 = lambda x: chi2_bao_late(bao, x, w=False)
    r = infer.minimize_multistart(f_r1, b_r1, n_starts=P["n_starts"], seed=P["seed"])

    def logp_r1(x):
        if not all(lo <= v <= hi for v, (lo, hi) in zip(x, b_r1)):
            return -np.inf
        return -0.5 * f_r1(x)

    mc = infer.run_emcee(logp_r1, r["x"], nwalkers=P["r1_walkers"], nsteps=P["r1_steps"], seed=P["seed"])
    stats, n_eff = mc_summary(mc["samples"], mc["tau"], P["r1_walkers"], ["Om", "hrd"])
    ok_chain = mc["n_over_tau"] >= 50 and all(
        stats[k]["mc_err"] < 0.05 * stats[k]["sigma68"] for k in stats)
    checks = {}
    for k in ("Om", "hrd"):
        tv, ts = TARGET["R1"][k]
        checks[k] = {"mean_ok": abs(stats[k]["mean"] - tv) <= P["tol_r1_sigma"] * ts,
                     "err_ok": abs(stats[k]["sigma68"] / ts - 1.0) <= P["tol_r1_err"],
                     "dev_sigma": (stats[k]["mean"] - tv) / ts}
    map_ok = r["converged"] and r["n_agree"] >= 3
    r1_pass = ok_chain and map_ok and all(c["mean_ok"] and c["err_ok"] for c in checks.values())
    out["R1"] = {"map": summarise(r), "posterior": stats, "n_eff": n_eff,
                 "n_over_tau": mc["n_over_tau"], "acceptance": mc["acceptance"],
                 "chain_ok": bool(ok_chain), "checks": checks,
                 "map_ok": bool(map_ok),
                 "verdict": ("reproduced" if r1_pass else
                             ("failed fit" if not (ok_chain and map_ok) else "not reproduced"))}
    ctx.log(f"R1: {out['R1']['verdict']} {stats}")

    # R3: no CMB
    r3 = {}
    sn_data = {k: load_sn(ctx, k, P["sn_zmin"]) for k in SN}
    for name, sn in [("desi", None), ("desi_pantheonplus", sn_data["pantheonplus"]),
                     ("desi_union3", sn_data["union3"])]:
        def f_l(x, sn=sn):
            return chi2_bao_late(bao, x, w=False) + (0.0 if sn is None else chi2_sn(sn, x[0], -1.0, 0.0))

        def f_w(x, sn=sn):
            return chi2_bao_late(bao, x) + (0.0 if sn is None else chi2_sn(sn, x[0], x[2], x[3]))

        pp = PAPER_POINT[name]
        fit = fit_pair(f_l, f_w, b_r1, lambda xl, pp=pp: [pp[0], xl[1], pp[1], pp[2]],
                       P["n_starts"], P["seed"])
        fit["n_sn"] = None if sn is None else sn["n"]
        fit["target"] = TARGET[name]
        fit["verdict"] = verdict_dchi2(fit, TARGET[name], P["tol_dchi2"])
        r3[name] = fit
        ctx.log(f"R3 {name}: {fit.get('dchi2')} -> {fit['verdict']}")
    verd = [r3[k]["verdict"] for k in r3]
    r3["overall"] = ("reproduced" if all(v == "reproduced" for v in verd) else
                     "failed fit" if any(v == "failed fit" for v in verd) else "not reproduced")
    out["R3"] = r3

    # R2: DESI + compressed CMB prior, readings A and B
    b_r2 = [(20.0, 100.0), (0.005, 0.1), (0.001, 0.99)]
    K0 = cosmo.theta_calibration()
    pp = PAPER_POINT["R2"]

    def paper_r2(xl):
        h = pp[1] / 100.0
        oc = pp[0] * h * h - xl[1] - cosmo.omega_nu_today(P["mnu"])
        return [pp[1], xl[1], oc, pp[2], pp[3]]

    r2 = {"K": K0}
    for reading, key in (("A", "reading_A_with_nu"), ("B", "reading_B_without_nu")):
        fl = lambda x, rd=reading: chi2_r2(bao, x, rd, P["mnu"], K0, w=False)
        fw = lambda x, rd=reading: chi2_r2(bao, x, rd, P["mnu"], K0, w=True)
        fit = fit_pair(fl, fw, b_r2, paper_r2, P["n_starts"], P["seed"])
        fit["target"] = TARGET["R2"]
        fit["verdict"] = verdict_dchi2(fit, TARGET["R2"], P["tol_dchi2"])
        if P["r2_mcmc"] and fit.get("valid"):
            bnds = b_r2 + W_BOUNDS

            def logp(x, fw=fw, bnds=bnds):
                if not all(lo <= v <= hi for v, (lo, hi) in zip(x, bnds)) or w_constraint(x) < 0:
                    return -np.inf
                c = fw(x)
                return -0.5 * c if np.isfinite(c) else -np.inf

            mc = infer.run_emcee(logp, fit["w0wa"]["x"], nwalkers=P["r2_walkers"],
                                 nsteps=P["r2_steps"], seed=P["seed"] + 7)
            st, ne = mc_summary(mc["samples"], mc["tau"], P["r2_walkers"], ["H0", "ombh2", "omch2", "w0", "wa"])
            fit["posterior"] = {"w0": st["w0"], "wa": st["wa"], "H0": st["H0"],
                                "n_eff": ne, "n_over_tau": mc["n_over_tau"],
                                "paper": {"w0": [-0.43, 0.22], "wa": [-1.72, 0.64], "H0": [63.7, 2.0]}}
        r2[key] = fit
        ctx.log(f"R2 {key}: {fit.get('dchi2')} -> {fit['verdict']}")
    va, vb = r2["reading_A_with_nu"]["verdict"], r2["reading_B_without_nu"]["verdict"]
    if "failed fit" in (va, vb):
        r2["overall"] = "failed fit"
    elif va == vb == "reproduced":
        r2["overall"] = "reproduced"
    elif "reproduced" in (va, vb):
        r2["overall"] = "conditionally reproduced (reading %s)" % ("A" if va == "reproduced" else "B")
    else:
        r2["overall"] = "not reproduced"

    # K check (diagnostic only)
    if P["k_check"]:
        dK = np.sqrt(CMB_COV[0, 0]) / CMB_MEAN[0]
        kc = {"dK_rel": float(dK)}
        for reading in ("A", "B"):
            for sgn in (+1, -1):
                K = K0 * (1.0 + sgn * dK)
                fl = lambda x, rd=reading, K=K: chi2_r2(bao, x, rd, P["mnu"], K, w=False)
                fw = lambda x, rd=reading, K=K: chi2_r2(bao, x, rd, P["mnu"], K, w=True)
                f = fit_pair(fl, fw, b_r2, paper_r2, P["n_starts"] // 2, P["seed"] + 3)
                kc[f"{reading}{'+' if sgn > 0 else '-'}"] = f.get("dchi2")
                kc[f"{reading}{'+' if sgn > 0 else '-'}_valid"] = bool(f.get("valid"))
        cam = cosmo.Background(67.39, 0.02229, 0.1197, mnu=P["mnu"])
        kc["second_point_dtheta100"] = float(100 * cam.theta_star(K0) - 1.04106)
        r2["K_check"] = kc
    out["R2"] = r2

    ctx.save("summary", out)
    return {"R1": out["R1"]["verdict"], "R2": r2["overall"], "R3": r3["overall"]}
