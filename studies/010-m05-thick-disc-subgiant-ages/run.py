"""M5 Milky Way thick disc: early formation from subgiant ages (README sections 1-4).

Pre-registration: README sections 1-4 (frozen 2026-11-15). Input: the Xiang & Rix 2022 catalogue
(VizieR J/other/Nat/603.599/table1), fetched once through ctx.http from the CfA VizieR mirror.
Run with:
    python -m astrolab run 010-m05-thick-disc-subgiant-ages
Explore with:
    python -m astrolab explore 010-m05-thick-disc-subgiant-ages --tag <topic> --set KEY=VALUE

R1  8 Gyr split: deconvolved age densities in [Fe/H] bins, valley depth, mock calibration (verdict).
R2  13 Gyr mean of Extended Data Fig. 1 (verdict) and sensitivities.
R3  5-6 Gyr span of the old-disc sequence (verdict); R4 its scatter (verdict); intrinsic scatter
    with a background component (verdict).
R7  total age spread of the high-alpha disc (descriptive); R5, R6 plots and percentiles.
"""
from __future__ import annotations

import time

import numpy as np
import pandas as pd

import m0
import mocks

# Tunable knobs (AGENTS.md section 2). Read inside main() and passed on as arguments.
PARAMS = {
    "url": ("https://vizier.cfa.harvard.edu/viz-bin/asu-tsv?-source=J/other/Nat/603.599/table1"
            "&-out=Id,Age,e_Age,[Fe/H],e_[Fe/H],[alpha/Fe],e_[alpha/Fe],JPHI,MKcomb&-out.max=300000"),
    "n_rows": 247104,
    "jphi_median_range": [1500.0, 2100.0],
    "cut": 0.15, "tmax": 20.0, "grid_step": 0.05, "grid_check_step": 0.02,
    "nclass": 20, "nclass_check": 40, "feh_step": 0.05, "nefe": 5,
    "nstart": 8, "nstart_r1_data": 40, "mock_extra_starts": 2, "seed": 0,
    # R1
    "r1_bins": [[-0.7, -0.5], [-0.5, -0.3], [-0.3, -0.1], [-0.1, 0.1], [0.1, 0.3]],
    "r1_check_bin": 2, "kmax": 4, "valley_lo": 5.0, "valley_hi": 11.0, "side_mass": 0.10,
    "prom": 0.10, "d_cap": 0.25, "mode_match": 0.5, "edge_q": 0.975,
    "power_old": [9.38, -3.8, 0.82], "power_young": [1.5, 7.0], "power_true_d_max": 0.1,
    "power_edge_step": 0.5, "power_min_wold": 0.10, "power_needed": 0.80,
    "edge_range": [6.5, 9.5], "min_bins": 3,
    "n_mock": 50, "n_mock_reduced": 30, "budget_h": 4.0, "budget_bg_h": 8.0,
    "mechs": ["rtau", "rA"],
    # R2
    "r2_feh": [-1.05, -0.95], "r2_jphi": 500.0, "r2_range": [12.5, 13.5], "r2_sigma_paper": 1.81,
    "r2_jphi_alt": [300.0, 700.0], "r2_cut_alt": [0.10, 0.20], "universe": 13.8,
    # R3/R4
    "seq_feh": [-1.2, 0.5], "seq_jphi": 500.0, "seq_start": [9.38, -3.8, 0.82],
    "sigma_paper": 0.82, "sigma_tol": 0.1, "span_dex": 1.5, "span_range": [4.5, 6.5],
    "span_trunc": [-0.2, 0.0], "rec_tol_sigma": 0.1, "rec_tol_a": 0.2, "n_boot": 50,
    "f_min": 0.8, "late_bins": [-0.5, 0.3, 0.1], "z_one_sided": 1.645,
    "bg_slices": [[-1.2, -0.6], [-0.6, 0.0], [0.0, 0.5]],
    # R7
    "r7_alpha": [0.10, 0.18], "r7_feh_cut": -0.2, "r7_window": 1.5, "miglio_95": [1.52, 0.54, 0.46],
    # R5/R6
    "r6_feh": [-1.0, -0.4], "n_boot_r6": 200,
    "hist_age": [0.0, 20.0, 0.25], "hist_feh": [-2.5, 0.6, 0.1],
    # age-scale envelope (literature magnitudes, not recomputed)
    "env_mist": 0.5, "env_alpha": [0.5, 1.0], "env_chen_frac": -0.129,
}


# =============================================================================================
# data
# =============================================================================================
def load(ctx, P):
    path = ctx.http(P["url"], label="XR22 subgiant catalogue (VizieR J/other/Nat/603.599/table1, CfA mirror)",
                    release="Xiang & Rix 2022", suffix=".tsv")
    lines = [l for l in open(path, encoding="utf-8").read().splitlines() if l and not l.startswith("#")]
    head = lines[0].split("\t")
    rows = [l.split("\t") for l in lines[3:]]           # header, units, dashes
    df = pd.DataFrame(rows, columns=head)
    out = pd.DataFrame({
        "id": pd.to_numeric(df["Id"], errors="coerce"),
        "age": pd.to_numeric(df["Age"], errors="coerce"),
        "eage": pd.to_numeric(df["e_Age"], errors="coerce"),
        "feh": pd.to_numeric(df["[Fe/H]"], errors="coerce"),
        "efeh": pd.to_numeric(df["e_[Fe/H]"], errors="coerce"),
        "afe": pd.to_numeric(df["[alpha/Fe]"].str.strip().replace("", np.nan), errors="coerce"),
        "eafe": pd.to_numeric(df["e_[alpha/Fe]"].str.strip().replace("", np.nan), errors="coerce"),
        "jphi": pd.to_numeric(df["JPHI"], errors="coerce"),
        "mk": pd.to_numeric(df["MKcomb"], errors="coerce"),
    })
    return out


def flags(df, P):
    afe, feh, jphi = df["afe"].to_numpy(), df["feh"].to_numpy(), df["jphi"].to_numpy()
    line = np.where(feh < -0.5, 0.16, -0.16 * feh + 0.08)
    has_a = np.isfinite(afe)
    above = has_a & (afe >= line)
    late = has_a & (jphi > 1500) & (afe < line)
    early = has_a & ~late
    valid = np.isfinite(df["age"].to_numpy()) & (df["eage"].to_numpy() > 0) & np.isfinite(feh)
    s15 = valid & (df["eage"].to_numpy() / df["age"].to_numpy() < P["cut"])
    return {"valid": valid, "s15": s15, "late": late, "early": early, "above": above, "has_a": has_a}


# =============================================================================================
# helpers
# =============================================================================================
class Ctx:
    """Shared fitting context (grid, settings, rng)."""

    def __init__(self, P, step=None):
        self.P = P
        self.grid = m0.Grid(step or P["grid_step"], P["tmax"])
        self.rng = np.random.default_rng(P["seed"])


def onedim(C, age, eage, s15, *, f=1.0, nclass=None, none=False, truncate=True, grid=None):
    cells = m0.compress(age, eage, s15=s15, step_a=C.P["grid_step"], nclass=nclass or C.P["nclass"],
                        cut=C.P["cut"], none=none)
    return m0.OneD(grid or C.grid, cells, f=f, truncate=truncate)


def fit_mixtures(C, model, ages, weights, kmax, starts_from=None, nstart=None, rng=None):
    """Fit K = 1..kmax; returns dict K -> (theta, nll). starts_from: dict K -> theta (mock fits)."""
    rng = rng or C.rng
    fits = {}
    for K in range(1, kmax + 1):
        if starts_from is not None and K in starts_from:
            starts = m0.perturb(starts_from[K], C.P["mock_extra_starts"], rng)
        else:
            starts = m0.mixture_starts(ages, weights, K, nstart or C.P["nstart"], rng)
        r = model.fit_mixture(K, starts)
        fits[K] = (r.x, float(r.fun))
        model.converged = {**getattr(model, "converged", {}), K: bool(r.success)}
    return fits


def choose_k(fits, n):
    bics = {K: m0.bic(nll, 3 * K - 1, n) for K, (th, nll) in fits.items()}
    return min(bics, key=lambda k: (bics[k], k)), bics


def shape_from_fits(C, model, fits, kbest, ages, weights, starts_from=None, rng=None, nstart=None):
    """Valley analysis with the K = 5 mode-matching rule."""
    P = C.P
    th = fits[kbest][0]
    p = m0.mix_cells(C.grid, th, kbest)
    keep = None
    k5 = None
    k5_conv = None
    if kbest == P["kmax"]:
        K5 = P["kmax"] + 1
        if starts_from is not None and K5 in starts_from:
            starts = m0.perturb(starts_from[K5], P["mock_extra_starts"], rng or C.rng)
        else:
            starts = m0.mixture_starts(ages, weights, K5, (nstart or P["nstart"]) if starts_from is None else 1 + P["mock_extra_starts"], rng or C.rng)
        r5 = model.fit_mixture(K5, starts)
        k5 = r5.x
        k5_conv = bool(r5.success)
        p5 = m0.mix_cells(C.grid, k5, K5)
        pk5 = [C.grid.mid[i] for i in m0.peaks(p5 / C.grid.step, P["prom"])]
        keep = lambda t: any(abs(t - u) <= P["mode_match"] for u in pk5)
    v = m0.valley(C.grid, p, lo=P["valley_lo"], hi=P["valley_hi"], side_mass=P["side_mass"],
                  prom=P["prom"], keep_peaks=keep)
    v["k"] = int(kbest)
    v["cap"] = bool(kbest == P["kmax"])
    v["k5_converged"] = k5_conv
    return v, p, k5


def gauss_ml(x):
    x = np.asarray(x, float)
    n = len(x)
    mu, sd = float(x.mean()), float(x.std())
    return {"n": int(n), "mu": mu, "mu_err": sd / np.sqrt(n), "sigma": sd, "sigma_err": sd / np.sqrt(2 * n)}


def timed(fn):
    t = time.time()
    out = fn()
    return out, time.time() - t


# =============================================================================================
# R1
# =============================================================================================
def r1_data(C, df, F, b, sample):
    P = C.P
    lo, hi = P["r1_bins"][b]
    feh = df["feh"].to_numpy()
    base = F["s15"] if sample == "S15" else F["valid"]
    m = base & (feh >= lo) & (feh < hi)
    age, eage = df["age"].to_numpy()[m], df["eage"].to_numpy()[m]
    model = onedim(C, age, eage, sample == "S15")
    w = model.cells.w
    # per-bin random stream: a bin's starts must not depend on how many draws earlier bins used
    rng = np.random.default_rng([P["seed"], 1000 + b, 0 if sample == "S15" else 1, int(round(C.grid.step * 1000))])
    # amendment 2026-11-15: 40 starts for the R1 data fits (README 2.0, "Fitting")
    fits = fit_mixtures(C, model, model.cells.A, w, P["kmax"], nstart=P["nstart_r1_data"], rng=rng)
    kbest, bics = choose_k(fits, model.cells.nstar)
    v, p, k5 = shape_from_fits(C, model, fits, kbest, model.cells.A, w, rng=rng, nstart=P["nstart_r1_data"])
    starts = {K: th for K, (th, _) in fits.items()}
    if k5 is not None:
        starts[P["kmax"] + 1] = k5
    # r pool from the bin's Full sample
    mf = F["valid"] & (feh >= lo) & (feh < hi)
    rpool = (df["eage"].to_numpy() / df["age"].to_numpy())[mf]
    # null fits
    a0 = model.cells.A
    mu0 = float(np.average(a0, weights=w))
    sd0 = float(np.sqrt(np.average((a0 - mu0) ** 2, weights=w)))
    # 8 starts per null model (README 2.0): 3 deterministic + 5 seeded perturbations of the first
    def null_starts(det):
        extra = m0.perturb(det[0], P["nstart"] - len(det), rng, 0.3)[1:]
        return det + extra
    sn = model.fit_param(m0.skewnorm_cells, null_starts([np.array([mu0, np.log(sd0), 0.0]), np.array([mu0 + sd0, np.log(sd0 * 1.3), -3.0]),
                                                         np.array([mu0 - sd0, np.log(sd0 * 1.3), 3.0])]),
                         [(-5, 25), (np.log(0.1), np.log(20)), (-30, 30)])
    sp = model.fit_param(m0.splitnorm_cells, null_starts([np.array([mu0, np.log(sd0), np.log(sd0)]),
                                                          np.array([mu0 + sd0, np.log(sd0 * 1.5), np.log(sd0 * 0.5)]),
                                                          np.array([mu0 - sd0, np.log(sd0 * 0.5), np.log(sd0 * 1.5)])]),
                         [(-5, 25), (np.log(0.05), np.log(20)), (np.log(0.05), np.log(20))])
    # power model
    t0, a, so = P["power_old"]
    fc = 0.5 * (lo + hi)
    pool_w = (F["early"] & (df["jphi"].to_numpy() > 500) & F["above"])[m].mean()
    wold = max(float(pool_w), P["power_min_wold"])
    edge = P["power_young"][1]
    for _ in range(20):
        q, _, _ = m0.tn_cells(C.grid, t0 + a * fc, so)
        young = ((C.grid.mid >= P["power_young"][0]) & (C.grid.mid < edge)).astype(float)
        pgen = wold * q[0] + (1 - wold) * young / young.sum()
        vtrue = m0.valley(C.grid, pgen, lo=P["valley_lo"], hi=P["valley_hi"], side_mass=P["side_mass"], prom=P["prom"])
        if vtrue["d"] <= P["power_true_d_max"]:
            break
        if edge - P["power_edge_step"] <= P["power_young"][0] + C.grid.step:
            break  # young window would be empty; keep the last non-empty edge (true_d recorded)
        edge -= P["power_edge_step"]
    return {
        "sample": sample, "bin": [lo, hi], "n": int(m.sum()), "ncells": int(len(w)),
        "bic": {str(k): float(v_) for k, v_ in bics.items()}, "shape": v,
        "fits": {str(K): [float(x) for x in th] for K, (th, _) in fits.items()},
        "skewnorm": [float(x) for x in sn.x], "splitnorm": [float(x) for x in sp.x],
        "null_converged": {"skewnorm": bool(sn.success), "splitnorm": bool(sp.success)},
        "mix_converged": {str(k): v_ for k, v_ in model.converged.items()},
        "power_model": {"mu_old": t0 + a * fc, "s_old": so, "w_old": wold, "w_old_raw": float(pool_w),
                        "young": [P["power_young"][0], edge], "true_d": vtrue["d"]},
        "_starts": starts, "_rpool": rpool, "_n": int(m.sum()), "_p": p,
    }


def r1_mock(C, D, kind, mech, rng):
    P = C.P
    s15 = D["sample"] == "S15"
    rp = D["_rpool"]
    if kind == "null_sn":
        loc, lsc, al = D["skewnorm"]
        lat = lambda k: mocks.latent_skewnorm(loc, np.exp(lsc), al, k, rng, P["tmax"])
    elif kind == "null_sp":
        mm, l1, l2 = D["splitnorm"]
        lat = lambda k: mocks.latent_split(mm, np.exp(l1), np.exp(l2), k, rng, P["tmax"])
    else:
        pm = D["power_model"]
        lat = lambda k: mocks.latent_power(pm["mu_old"], pm["s_old"], pm["w_old"], pm["young"][1], k, rng,
                                           lo=pm["young"][0], tmax=P["tmax"])
    draw = lambda k: {"tau": lat(k), "r": rng.choice(rp, size=k)}
    cat = mocks.catalogue(draw, D["_n"], mech, rng, s15=s15, cut=P["cut"], tmax=P["tmax"])
    model = onedim(C, cat["A"], cat["e"], s15)
    fits = fit_mixtures(C, model, model.cells.A, model.cells.w, P["kmax"], starts_from=D["_starts"], rng=rng)
    kbest, _ = choose_k(fits, model.cells.nstar)
    v, _, _ = shape_from_fits(C, model, fits, kbest, model.cells.A, model.cells.w, starts_from=D["_starts"], rng=rng)
    return {"d": v["d"], "valley": v["valley"], "k": v["k"]}


def r1_decide(P, D, res, nmock):
    """Threshold d* and per-bin result from the mock sets of one bin/sample."""
    qrank = 3 if nmock >= 50 else 2
    q = {}
    fpr = {}
    for kind in ("null_sn", "null_sp"):
        for mech in P["mechs"]:
            ds = sorted(r["d"] for r in res[(kind, mech)] if r["valley"])
            q[f"{kind}_{mech}"] = float(ds[qrank - 1]) if len(ds) >= qrank else P["d_cap"]
    dstar = min([P["d_cap"]] + list(q.values()))
    passes = lambda r: r["valley"] and r["d"] < dstar
    for kind in ("null_sn", "null_sp"):
        for mech in P["mechs"]:
            rr = res[(kind, mech)]
            fpr[f"{kind}_{mech}"] = float(np.mean([passes(r) for r in rr]))
    power = {mech: float(np.mean([passes(r) for r in res[("power", mech)]])) for mech in P["mechs"]}
    resolvable = all(v >= P["power_needed"] for v in power.values())
    sh = D["shape"]
    disjoint = bool(sh["valley"] and sh["d"] < dstar)
    mc = lambda p_: float(np.sqrt(p_ * (1 - p_) / nmock))   # binomial Monte Carlo uncertainty
    return {"fpr_err": {k: mc(v) for k, v in fpr.items()}, "power_err": {k: mc(v) for k, v in power.items()},
            "q": q, "d_star": dstar, "applied": min(q, key=q.get) if dstar < P["d_cap"] else "cap",
            "fpr": fpr, "power": power, "resolvable": resolvable, "almost_disjoint": disjoint,
            "d": sh["d"], "edge": sh["edge"], "valley_t": sh["t"], "nmock": nmock}


def r1_verdict(P, bins):
    res = [b for b in bins if b["resolvable"]]
    disj = [b for b in res if b["almost_disjoint"]]
    if len(res) < P["min_bins"]:
        return "undetermined", None
    edges = [b["edge"] for b in disj if b["edge"] is not None]
    med = float(np.median(edges)) if edges else None
    ok = len(disj) >= P["min_bins"] and med is not None and P["edge_range"][0] <= med <= P["edge_range"][1]
    return ("reproduced" if ok else "not reproduced"), med


# =============================================================================================
# R3/R4 models
# =============================================================================================
def grouped(C, sub, s15, *, f=1.0, feh_err=False, nclass=None, none=False, truncate=True, grid=None):
    P = C.P
    cells = m0.compress(sub["age"].to_numpy(), sub["eage"].to_numpy(), s15=s15, step_a=P["grid_step"],
                        nclass=nclass or P["nclass"], feh=sub["feh"].to_numpy(),
                        efeh=sub["efeh"].to_numpy() if feh_err else None, feh_step=P["feh_step"],
                        nefe=P["nefe"], cut=P["cut"], none=none)
    return m0.Grouped(grid or C.grid, cells, f=f, truncate=truncate, feh_err=feh_err)


def seq_starts(C, th=None, rng=None):
    t0, a, s = C.P["seq_start"]
    base = np.array([t0, a, np.log(s)]) if th is None else np.asarray(th, float)
    return m0.perturb(base, C.P["nstart"] - 1 if th is None else C.P["mock_extra_starts"], rng or C.rng, 0.3)


def fit_seq(C, model, th=None, rng=None):
    r = model.fit_seq(seq_starts(C, th, rng))
    se, _ = m0.hessian_se(model.seq_negll, r.x)
    t0, a, ls = r.x
    s = float(np.exp(ls))
    return {"tau0": float(t0), "a": float(a), "sigma": s, "tau0_err": float(se[0]), "a_err": float(se[1]),
            "sigma_err": float(se[2] * s), "span": float(abs(a) * C.P["span_dex"]), "nll": float(r.fun),
            "n": int(model.c.nstar), "converged": bool(r.success), "_x": r.x}


def fit_degenerate(sub):
    from scipy.optimize import minimize
    A, e, fe = sub["age"].to_numpy(), sub["eage"].to_numpy(), sub["feh"].to_numpy()

    def nll(th):
        t0, a, ls = th
        v = np.exp(2 * ls) + e ** 2
        r = A - t0 - a * fe
        return 0.5 * np.sum(r * r / v + np.log(2 * np.pi * v))
    r = minimize(nll, [9.38, -3.8, np.log(0.8)], method="L-BFGS-B")
    return {"tau0": float(r.x[0]), "a": float(r.x[1]), "sigma": float(np.exp(r.x[2]))}


def mix_starts(C, seq, th=None, rng=None):
    """Mock fits: th plus 2 perturbations. Data fits: 8 starts around seq; with th also given
    (the f-sensitivity data fits), th is added as a ninth start."""
    rng = rng or C.rng
    if th is not None and seq is None:
        return m0.perturb(np.asarray(th, float), C.P["mock_extra_starts"], rng, 0.2)
    base = np.array([seq["tau0"], seq["a"], np.log(max(seq["sigma"], 0.3)), 5.0, 0.0, np.log(2.0), -1.0])
    starts = list(m0.perturb(base, C.P["nstart"] - 1, rng, 0.3))
    if th is not None:
        starts.append(np.asarray(th, float))
    return starts


def fit_mixB(C, model, seq=None, th=None, rng=None):
    r = model.fit_mix(mix_starts(C, seq, th, rng))
    se, _ = m0.hessian_se(model.mix_negll, r.x)
    t0, a, ls, b0, b1, lsb, eta = r.x
    s = float(np.exp(ls))
    return {"tau0": float(t0), "a": float(a), "sigma": s, "sigma_err": float(se[2] * s),
            "b0": float(b0), "b1": float(b1), "s_bg": float(np.exp(lsb)), "f_bg": float(1 / (1 + np.exp(-eta))),
            "nll": float(r.fun), "n": int(model.c.nstar), "converged": bool(r.success), "_x": r.x}


# =============================================================================================
# main
# =============================================================================================
def main(ctx):
    P = dict(PARAMS)
    t_start = time.time()
    C = Ctx(P)
    df = load(ctx, P)
    F = flags(df, P)
    A_all, E_all = df["age"].to_numpy(), df["eage"].to_numpy()
    feh, jphi, afe = df["feh"].to_numpy(), df["jphi"].to_numpy(), df["afe"].to_numpy()

    # ---------------- checks
    assert len(df) == P["n_rows"], f"row count {len(df)} != {P['n_rows']}"
    assert df["id"].is_unique, "Id not unique"
    jmed = float(np.nanmedian(jphi))
    assert P["jphi_median_range"][0] <= jmed <= P["jphi_median_range"][1], f"median JPHI {jmed}"
    v = F["valid"]
    rel = E_all[v] / A_all[v]
    checks = {
        "n_rows": int(len(df)), "id_unique": True, "jphi_median": jmed,
        "n_valid": int(v.sum()), "n_s15": int(F["s15"].sum()), "n_blank_alpha": int((~F["has_a"]).sum()),
        "corr_relerr_age": float(np.corrcoef(rel, A_all[v])[0, 1]),
        "median_relerr": float(np.median(rel)),
        "frac_age_gt_13p8_all": float(np.mean(A_all[v] > P["universe"])),
    }
    ctx.log(f"checks: {checks}")

    # ---------------- R5/R6 and eq. 1 cross-fractions (cheap)
    s15 = F["s15"]
    cross = {"late_older_8": float(np.mean(A_all[s15 & F["late"]] > 8.0)),
             "early_younger_8": float(np.mean(A_all[s15 & F["early"]] < 8.0)),
             "n_late": int((s15 & F["late"]).sum()), "n_early": int((s15 & F["early"]).sum())}
    ha, hf = P["hist_age"], P["hist_feh"]
    aedges = np.arange(ha[0], ha[1] + 1e-9, ha[2])
    fedges = np.arange(hf[0], hf[1] + 1e-9, hf[2])
    hists = {}
    for name, m in {"all": s15, "late": s15 & F["late"], "early_hiJ": s15 & F["early"] & (jphi > 500),
                    "early_loJ": s15 & F["early"] & (jphi <= 500)}.items():
        H, _, _ = np.histogram2d(feh[m], A_all[m], bins=[fedges, aedges])
        hists[name] = H.astype(int).tolist()
    r6 = {}
    rng6 = np.random.default_rng(P["seed"] + 6)
    for name, m in {"loJ": s15 & F["early"] & (jphi < 500), "hiJ": s15 & F["early"] & (jphi > 500)}.items():
        mm = m & (feh > P["r6_feh"][0]) & (feh < P["r6_feh"][1])
        x = A_all[mm]
        boots = np.array([np.percentile(rng6.choice(x, len(x)), [5, 10]) for _ in range(P["n_boot_r6"])])
        r6[name] = {"n": int(len(x)), "p5": float(np.percentile(x, 5)), "p10": float(np.percentile(x, 10)),
                    "p5_err": float(boots[:, 0].std()), "p10_err": float(boots[:, 1].std())}
    mpk = s15 & F["early"] & (jphi > 500)
    hh, ee = np.histogram(A_all[mpk], bins=aedges)
    r6["peak_hiJ_observed"] = float(0.5 * (ee[hh.argmax()] + ee[hh.argmax() + 1]))
    ctx.save("r56", {"cross_fractions": cross, "r6": r6, "hist": {"age_edges": aedges.tolist(), "feh_edges": fedges.tolist(), **hists}})

    # ---------------- R2
    def r2_sel(base, early=True, jcut=P["r2_jphi"]):
        m = base & (jphi > jcut) & (feh > P["r2_feh"][0]) & (feh < P["r2_feh"][1])
        return m & F["early"] if early else m
    prim = r2_sel(s15)
    r2 = {"primary": gauss_ml(A_all[prim])}
    r2["primary"]["frac_gt_13p8"] = float(np.mean(A_all[prim] > P["universe"]))
    r2["primary"]["frac_gt_18"] = float(np.mean(A_all[prim] > 18.0))
    mu = r2["primary"]["mu"]
    r2["verdict"] = "reproduced" if P["r2_range"][0] <= mu <= P["r2_range"][1] else "not reproduced"
    sens = {"no_early_filter": gauss_ml(A_all[r2_sel(s15, early=False)]),
            "full": gauss_ml(A_all[r2_sel(F["valid"])])}
    for jc in P["r2_jphi_alt"]:
        sens[f"jphi_{int(jc)}"] = gauss_ml(A_all[r2_sel(s15, jcut=jc)])
    for cu in P["r2_cut_alt"]:
        base = F["valid"] & (E_all / np.where(A_all > 0, A_all, np.nan) < cu)
        sens[f"cut_{cu:.2f}"] = gauss_ml(A_all[r2_sel(base)])
    # deconvolved latent Gaussian (M0, K = 1) and checks
    def deconv(step=None, nclass=None, none=False, truncate=True, sample="S15"):
        CC = C if step is None else Ctx(P, step)
        base = s15 if sample == "S15" else F["valid"]
        m = r2_sel(base)
        mod = onedim(CC, A_all[m], E_all[m], sample == "S15", nclass=nclass, none=none, truncate=truncate, grid=CC.grid)
        fits = fit_mixtures(CC, mod, mod.cells.A, mod.cells.w, 1)
        th = fits[1][0]
        return {"mu": float(th[0]), "sigma": float(np.exp(th[1]))}
    sens["deconvolved"] = deconv()
    sens["deconvolved_full"] = deconv(sample="Full")
    r2_checks = {"grid_0p02": deconv(step=P["grid_check_step"]), "nclass_40": deconv(nclass=P["nclass_check"]),
                 "no_compression": deconv(none=True), "untruncated": deconv(truncate=False),
                 "full_nclass_40": deconv(nclass=P["nclass_check"], sample="Full"),
                 "full_no_compression": deconv(none=True, sample="Full")}
    r2["sensitivity"] = sens
    r2["checks"] = r2_checks
    env = {"mist": P["env_mist"], "alpha": P["env_alpha"],
           "quadrature": [float(np.hypot(P["env_mist"], a)) for a in P["env_alpha"]],
           "chen_shift_at_mu": float(P["env_chen_frac"] * mu), "margin_to_big_bang": float(P["universe"] - mu),
           "listed_without_shift": ["LAMOST [Fe/H]/Teff offsets", "Gaia EDR3 parallax zero point (-17 to -21 uas)"]}
    r2["envelope"] = env
    ctx.save("r2", r2)
    ctx.log(f"R2: mu = {mu:.2f} -> {r2['verdict']}")

    # ---------------- R3/R4 data fits
    win = (feh > P["seq_feh"][0]) & (feh < P["seq_feh"][1])
    selA_full = F["valid"] & F["above"] & (jphi > P["seq_jphi"]) & win
    selA = selA_full & s15
    selB_full = F["valid"] & F["early"] & (jphi > P["seq_jphi"]) & win
    selB = selB_full & s15
    sel2e = s15 & F["early"] & win
    subA, subAf, subB, subBf, sub2e = (df[m] for m in (selA, selA_full, selB, selB_full, sel2e))
    modA = grouped(C, subA, True)
    seqA = fit_seq(C, modA)
    r34 = {"sampleA": {k: v_ for k, v_ in seqA.items() if not k.startswith("_")}}
    r34["sampleA"]["degenerate"] = fit_degenerate(subA)
    # error-scale factor
    lb = P["late_bins"]
    ratios = []
    for lo in np.arange(lb[0], lb[1] - 1e-9, lb[2]):
        mm = F["valid"] & F["late"] & (feh >= lo) & (feh < lo + lb[2]) & (A_all - 2 * E_all > 0) & (A_all + 2 * E_all < P["tmax"])
        if mm.sum() > 50:
            ratios.append({"bin": [float(lo), float(lo + lb[2])], "ratio": float(A_all[mm].std() / np.sqrt(np.mean(E_all[mm] ** 2))), "n": int(mm.sum())})
    f_i = min(r["ratio"] for r in ratios)
    f_ii = float(np.sqrt(1 + seqA["sigma"] ** 2 / np.mean(subA["eage"].to_numpy() ** 2)))
    f_max = float(min(f_i, f_ii))
    r34["error_scale"] = {"late_ratios": ratios, "f_i": f_i, "f_ii": f_ii, "f_max": f_max, "f_min": P["f_min"]}
    ctx.log(f"R3/R4 sample A: {r34['sampleA']}; f_max = {f_max:.3f}")

    t_rob = time.time()
    sensA = {}
    sensA["full"] = fit_seq(C, grouped(C, subAf, False))
    sensA["feh_err"] = fit_seq(C, grouped(C, subA, True, feh_err=True))
    sensA["feh_err_full"] = fit_seq(C, grouped(C, subAf, False, feh_err=True))
    sensA["f_min"] = fit_seq(C, grouped(C, subA, True, f=P["f_min"]))
    sensA["f_max"] = fit_seq(C, grouped(C, subA, True, f=f_max))
    sensA["full_f_min"] = fit_seq(C, grouped(C, subAf, False, f=P["f_min"]))
    sensA["full_f_max"] = fit_seq(C, grouped(C, subAf, False, f=f_max))
    for tcut in P["span_trunc"]:
        sensA[f"feh_lt_{tcut}"] = fit_seq(C, grouped(C, subA[subA["feh"] < tcut], True))
    sensA["edge_drop"] = fit_seq(C, grouped(C, subA[subA["age"] + 2 * subA["eage"] < P["tmax"]], True))
    sensA["untruncated"] = fit_seq(C, grouped(C, subA, True, truncate=False))
    Cg = Ctx(P, P["grid_check_step"])
    sensA["grid_0p02"] = fit_seq(Cg, grouped(Cg, subA, True, grid=Cg.grid))
    sensA["nclass_40"] = fit_seq(C, grouped(C, subA, True, nclass=P["nclass_check"]))
    sensA["no_compression"] = fit_seq(C, grouped(C, subA, True, none=True))
    sensA["full_nclass_40"] = fit_seq(C, grouped(C, subAf, False, nclass=P["nclass_check"]))
    sensA["full_no_compression"] = fit_seq(C, grouped(C, subAf, False, none=True))
    r34["sampleA_sensitivity"] = {k: {kk: vv for kk, vv in v_.items() if not kk.startswith("_")} for k, v_ in sensA.items()}
    fig2e = fit_seq(C, grouped(C, sub2e, True))
    r34["fig2e"] = {k: v_ for k, v_ in fig2e.items() if not k.startswith("_")}
    r34["fig2e"]["degenerate"] = fit_degenerate(sub2e)
    # bootstrap of sigma_sel
    rngb = np.random.default_rng(P["seed"] + 34)
    boots = []
    for _ in range(P["n_boot"]):
        bs = subA.iloc[rngb.integers(0, len(subA), len(subA))]
        boots.append(fit_seq(C, grouped(C, bs, True), th=seqA["_x"])["sigma"])
    r34["sampleA"]["sigma_boot_sd"] = float(np.std(boots))
    # sample B mixture
    modB = grouped(C, subB, True)
    mixB = fit_mixB(C, modB, seq=seqA)
    # data fits: 8 starts (README 2.0) plus the f = 1 optimum
    mixB_f = {"f_min": fit_mixB(C, grouped(C, subB, True, f=P["f_min"]), seq=seqA, th=mixB["_x"]),
              "f_max": fit_mixB(C, grouped(C, subB, True, f=f_max), seq=seqA, th=mixB["_x"])}
    r34["robustness_refit_h"] = (time.time() - t_rob) / 3600
    ctx.save("r34_partial", {**r34, "sampleB": {k: v_ for k, v_ in mixB.items() if not k.startswith("_")}})
    ctx.log(f"sample B mixture: {mixB['sigma']:.3f} +- {mixB['sigma_err']:.3f}")

    # ---------------- R7
    r7 = []
    hiJ = s15 & F["early"] & (jphi > P["seq_jphi"])
    r7_samples = {"sampleA": selA}
    for al in P["r7_alpha"]:
        r7_samples[f"alpha_gt_{al:.2f}"] = hiJ & (afe > al)
    for name, m in r7_samples.items():
        for fc in (None, P["r7_feh_cut"]):
            mm = m & (feh < fc) if fc is not None else m
            for f in (P["f_min"], 1.0, f_max):
                mod = onedim(C, A_all[mm], E_all[mm], True, f=f)
                fits = fit_mixtures(C, mod, mod.cells.A, mod.cells.w, P["kmax"], nstart=P["nstart_r1_data"])
                kb, _ = choose_k(fits, mod.cells.nstar)
                p = m0.mix_cells(C.grid, fits[kb][0], kb)
                q = m0.quantile_cells(C.grid, p, [0.025, 0.5, 0.975])
                r7.append({"sample": name, "feh_lt": fc, "f": float(f), "n": int(mm.sum()), "k": int(kb),
                           "median": q[1], "width95": q[2] - q[0],
                           "max_frac_window": m0.max_window(C.grid, p, P["r7_window"])})
    ctx.save("r7", {"rows": r7, "miglio_95": P["miglio_95"]})
    ctx.log("R7 done")

    # ---------------- R1 data fits
    r1d = {}
    for sample in ("S15", "Full"):
        for b in range(len(P["r1_bins"])):
            r1d[(sample, b)] = r1_data(C, df, F, b, sample)
            ctx.log(f"R1 data {sample} bin {b}: K={r1d[(sample, b)]['shape']['k']} d={r1d[(sample, b)]['shape']['d']:.3f} "
                    f"power-model true d={r1d[(sample, b)]['power_model']['true_d']:.3f}")
    Cc = Ctx(P, P["grid_check_step"])
    r1_check = r1_data(Cc, df, F, P["r1_check_bin"], "S15")["shape"]

    # ---------------- mock sets
    sets = []
    for key, D in r1d.items():
        for kind in ("null_sn", "null_sp", "power"):
            for mech in P["mechs"]:
                sets.append(("R1", key, kind, mech))
    for mech in P["mechs"]:
        sets.append(("A_rec", None, "rec", mech))
        sets.append(("B_id", None, "id", mech))
        sets.append(("B_mis", None, "mis", mech))

    # background empirical fits for misspecification mocks
    bgsel = F["valid"] & F["early"] & (jphi > P["seq_jphi"]) & ~F["above"] & F["has_a"]
    bgfits = []
    for lo, hi in P["bg_slices"]:
        mm = bgsel & (feh >= lo) & (feh < hi)
        mod = onedim(C, A_all[mm], E_all[mm], False)
        fits = fit_mixtures(C, mod, mod.cells.A, mod.cells.w, P["kmax"], nstart=P["nstart_r1_data"])
        kb, _ = choose_k(fits, mod.cells.nstar)
        mu_, s_, w_ = m0.mix_unpack(fits[kb][0], kb)
        rp_slice = (E_all / A_all)[F["valid"] & F["early"] & (jphi > P["seq_jphi"]) & (feh >= lo) & (feh < hi)]
        bgfits.append({"slice": [lo, hi], "mu": mu_, "s": s_, "w": w_, "feh": feh[mm], "rpool": rp_slice})

    parA = subAf[["feh"]].assign(r=subAf["eage"] / subAf["age"]).to_numpy()
    parB = subBf[["feh"]].assign(r=subBf["eage"] / subBf["age"]).to_numpy()
    nA, nB = len(subA), len(subB)

    def run_one(s, rng):
        tag, key, kind, mech = s
        if tag == "R1":
            return r1_mock(C, r1d[key], kind, mech, rng)
        if tag == "A_rec":
            t0, a, ls = seqA["_x"]
            def draw(k):
                rows = parA[rng.integers(0, len(parA), k)]
                tau = _seq_latent(rows[:, 0], t0, a, np.exp(ls), rng, P["tmax"])
                return {"tau": tau, "r": rows[:, 1], "feh": rows[:, 0]}
            cat = mocks.catalogue(draw, nA, mech, rng, s15=True, cut=P["cut"], tmax=P["tmax"])
            sub = pd.DataFrame({"age": cat["A"], "eage": cat["e"], "feh": cat["feh"], "efeh": 0.0})
            fit = fit_seq(C, grouped(C, sub, True), th=seqA["_x"], rng=rng)
            return {"sigma": fit["sigma"], "a": fit["a"], "tau0": fit["tau0"]}
        # sample B mocks
        t0, a, ls, b0, b1, lsb, eta = mixB["_x"]
        fb = 1 / (1 + np.exp(-eta))
        def draw(k):
            bg = rng.random(k) < fb
            out_tau = np.empty(k)
            out_r = np.empty(k)
            out_f = np.empty(k)
            rows = parB[rng.integers(0, len(parB), k)]
            ko = ~bg
            out_f[ko] = rows[ko, 0]
            out_r[ko] = rows[ko, 1]
            out_tau[ko] = _seq_latent(rows[ko, 0], t0, a, np.exp(ls), rng, P["tmax"])
            nb = int(bg.sum())
            if kind == "id":
                out_f[bg] = rows[bg, 0]
                out_r[bg] = rows[bg, 1]
                out_tau[bg] = _seq_latent(rows[bg, 0], b0, b1, np.exp(lsb), rng, P["tmax"])
            else:
                allf = np.concatenate([g["feh"] for g in bgfits])
                fsel = rng.choice(allf, nb)
                tb = np.empty(nb)
                rb = np.empty(nb)
                for g in bgfits:
                    mm = (fsel >= g["slice"][0]) & (fsel < g["slice"][1])
                    kk = int(mm.sum())
                    if kk:
                        tb[mm] = mocks.latent_mixture(g["mu"], g["s"], g["w"], kk, rng, P["tmax"])
                        rb[mm] = rng.choice(g["rpool"], kk)
                out_f[bg], out_tau[bg], out_r[bg] = fsel, tb, rb
                # old-sequence stars take r from the Full stars of their slice
                for g in bgfits:
                    mm = ko & (out_f >= g["slice"][0]) & (out_f < g["slice"][1])
                    if mm.any():
                        out_r[mm] = rng.choice(g["rpool"], int(mm.sum()))
            return {"tau": out_tau, "r": out_r, "feh": out_f}
        cat = mocks.catalogue(draw, nB, mech, rng, s15=True, cut=P["cut"], tmax=P["tmax"])
        sub = pd.DataFrame({"age": cat["A"], "eage": cat["e"], "feh": cat["feh"], "efeh": 0.0})
        fit = fit_mixB(C, grouped(C, sub, True), th=mixB["_x"], rng=rng)
        return {"sigma": fit["sigma"]}

    # phase B: first mock of every set, timing, budget
    results = {s: [] for s in sets}
    rngs = {s: np.random.default_rng([P["seed"], i]) for i, s in enumerate(sets)}
    tfirst = {}
    for s in sets:
        out, dt = timed(lambda: run_one(s, rngs[s]))
        results[s].append(out)
        tfirst[s] = dt
    proj = sum(P["n_mock"] * tfirst[s] for s in sets) / 3600
    nmock = P["n_mock"]
    mode = "full"
    if proj > P["budget_h"]:
        nmock = P["n_mock_reduced"]
        proj2 = sum(nmock * tfirst[s] for s in sets) / 3600
        mode = "reduced" + (" (background, above budget)" if proj2 > P["budget_bg_h"] else "")
    ctx.log(f"mock projection {proj:.2f} h at {P['n_mock']} per set -> using {nmock} per set ({mode})")
    t_m = time.time()
    for s in sets:
        while len(results[s]) < nmock:
            results[s].append(run_one(s, rngs[s]))
    mock_info = {"projection_h_at_50": proj, "n_per_set": nmock, "mode": mode,
                 "elapsed_h": (time.time() - t_m) / 3600, "n_sets": len(sets)}

    # ---------------- R1 decisions
    r1 = {"bins": {}, "verdict": {}, "check_grid_0p02_bin": r1_check}
    for sample in ("S15", "Full"):
        bins = []
        for b in range(len(P["r1_bins"])):
            D = r1d[(sample, b)]
            res = {(kind, mech): results[("R1", (sample, b), kind, mech)] for kind in ("null_sn", "null_sp", "power") for mech in P["mechs"]}
            dec = r1_decide(P, D, res, nmock)
            dec.update({"bin": D["bin"], "n": D["n"], "k": D["shape"]["k"], "cap": D["shape"]["cap"],
                        "peaks": D["shape"]["peaks"], "power_model": D["power_model"], "bic": D["bic"]})
            bins.append(dec)
        verdict, med = r1_verdict(P, bins)
        r1["bins"][sample] = bins
        r1["verdict"][sample] = {"verdict": verdict, "median_edge": med}
    r1["robust"] = r1["verdict"]["S15"]["verdict"] == r1["verdict"]["Full"]["verdict"]
    r1["latent_density"] = {f"{s}_{b}": (r1d[(s, b)]["_p"] / C.grid.step).round(5).tolist() for (s, b) in r1d}
    r1["grid_mid"] = C.grid.mid.round(3).tolist()
    ctx.save("r1", r1)

    # ---------------- R3/R4 decisions
    def bias(vals, true):
        v_ = np.asarray(vals) - true
        return {"bias": float(v_.mean()), "mc_err": float(v_.std(ddof=1) / np.sqrt(len(v_)))}
    rec = {}
    for mech in P["mechs"]:
        rr = results[("A_rec", None, "rec", mech)]
        bs = bias([r["sigma"] for r in rr], seqA["sigma"])
        ba = bias([r["a"] for r in rr], seqA["a"])
        ok = abs(bs["bias"]) <= P["rec_tol_sigma"] and abs(ba["bias"]) <= P["rec_tol_a"]
        near = (abs(abs(bs["bias"]) - P["rec_tol_sigma"]) <= bs["mc_err"]) or (abs(abs(ba["bias"]) - P["rec_tol_a"]) <= ba["mc_err"])
        rec[mech] = {"sigma": bs, "a": ba, "pass": bool(ok), "near_tolerance": bool(near)}
    rtau_only_fail = bool(rec["rA"]["pass"] and not rec["rtau"]["pass"])
    if rec["rA"]["pass"]:
        primary, primary_name = seqA, "S15" + (" (flag: e = r*tau recovery failed)" if rtau_only_fail else "")
    elif rec["rtau"]["pass"]:
        primary, primary_name = sensA["full"], "Full (S15 not robust: rA recovery failed)"
    else:
        primary, primary_name = None, "cannot determine (recovery failed)"
    lo_s, hi_s = P["span_range"]
    span_ok = lambda fit: lo_s <= fit["span"] <= hi_s
    sig_ok = lambda fit: abs(fit["sigma"] - P["sigma_paper"]) <= P["sigma_tol"]
    if primary is None:
        R3 = R4 = "cannot determine"
        r3_rob = r4_rob = False
    else:
        R3 = "reproduced" if span_ok(primary) else "not reproduced"
        R4 = "reproduced" if sig_ok(primary) else "not reproduced"
        if primary is seqA:
            r3_set = [sensA["full"], sensA["feh_err"], sensA["f_min"], sensA["f_max"]]
            r4_set = [sensA["full"], sensA["feh_err"]]
        else:   # Full primary: its own variants (clarification 2026-11-15, README 2.3)
            r3_set = [sensA["feh_err_full"], sensA["full_f_min"], sensA["full_f_max"]]
            r4_set = [sensA["feh_err_full"]]
        r3_rob = all(span_ok(x) for x in r3_set)
        r4_rob = all(sig_ok(x) for x in r4_set)
    def label(v_, rob):
        return v_ + ("" if v_ != "reproduced" else (", robust" if rob else ", not robust"))
    # intrinsic scatter (sample B)
    bsets = {}
    for kind in ("id", "mis"):
        for mech in P["mechs"]:
            bb = bias([r["sigma"] for r in results[("B_" + kind, None, kind, mech)]], mixB["sigma"])
            bb["near_tolerance"] = bool(abs(abs(bb["bias"]) - P["rec_tol_sigma"]) <= bb["mc_err"])
            bsets[f"{kind}_{mech}"] = bb
    sd_id = float(np.std([r["sigma"] for mech in P["mechs"] for r in results[("B_id", None, "id", mech)]], ddof=1))
    def intrinsic(fit):
        se = max(fit["sigma_err"], sd_id)   # reported even when the bias rule decides
        if any(abs(b_["bias"]) > P["rec_tol_sigma"] for b_ in bsets.values()):
            return "cannot determine", se
        z = P["z_one_sided"]
        if fit["sigma"] + z * se < P["sigma_paper"]:
            return "confirmed", se
        if fit["sigma"] - z * se >= P["sigma_paper"]:
            return "not confirmed", se
        return "cannot determine", se
    vB, seB = intrinsic(mixB)
    vB_f = {k: intrinsic(v_)[0] for k, v_ in mixB_f.items()}
    r34.update({
        "sampleB": {k: v_ for k, v_ in mixB.items() if not k.startswith("_")},
        "sampleB_f": {k: {kk: vv for kk, vv in v_.items() if not kk.startswith("_")} for k, v_ in mixB_f.items()},
        "sampleB_mock_bias": bsets, "sampleB_sd_id": sd_id, "sampleB_se_used": seB,
        "recovery": rec, "primary": primary_name,
        "verdict": {"R3": label(R3, r3_rob), "R4": label(R4, r4_rob),
                    "intrinsic": vB, "intrinsic_f": vB_f,
                    "intrinsic_robust": bool(vB == vB_f["f_min"] == vB_f["f_max"])},
    })
    ctx.save("r34", r34)

    summary = {
        "R1": r1["verdict"], "R1_robust": r1["robust"],
        "R2": {"verdict": r2["verdict"], "mu": r2["primary"]["mu"], "sigma": r2["primary"]["sigma"], "n": r2["primary"]["n"]},
        "R3": r34["verdict"]["R3"], "R4": r34["verdict"]["R4"], "R34_primary": r34["primary"],
        "intrinsic": {"verdict": vB, "robust": r34["verdict"]["intrinsic_robust"], "sigma_int": mixB["sigma"], "se": seB},
        "sampleA": {k: r34["sampleA"][k] for k in ("tau0", "a", "sigma", "span", "n")},
        "f_max": f_max, "checks": checks, "mocks": mock_info,
        "runtime_h": (time.time() - t_start) / 3600, "params": P,
    }
    ctx.save("summary", summary)
    return summary


def _seq_latent(fe, t0, a, s, rng, tmax):
    """Truncated normal latent ages on (0, tmax) with star-specific means t0 + a fe (inverse CDF,
    so a mean far outside the interval cannot stall the sampler)."""
    from scipy.stats import truncnorm
    mu = t0 + a * np.asarray(fe, float)
    lo, hi = (0.0 - mu) / s, (tmax - mu) / s
    return truncnorm.rvs(lo, hi, loc=mu, scale=s, size=len(mu), random_state=rng)
