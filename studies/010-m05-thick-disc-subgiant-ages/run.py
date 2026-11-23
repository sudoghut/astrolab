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
R-SEL  re-test of R1, R3/R4 and the intrinsic scatter with the empirical selection term E and
    term N (README 2.5, T-031; PARAMS["parts"] = ["sel"], results r1_sel.json, r34_sel.json, sel.json;
    the original pipeline above is parts = ["orig"] and writes r1/r2/r34/r56/r7/summary.json).
R1-SEL-FIT  R1-SEL with data-independent starts added to every mock fit (README 2.6, T-049;
    PARAMS["parts"] = ["selfit"], results r1_selfit.json, records provenance_selfit/run_info_selfit).
R1-ERR  error-scale power test of R1-SEL-FIT: power mocks of the metal-poor bins drawn with true errors
    f x e_Age, fitted with f = 1 (README 2.7, T-054; PARAMS["parts"] = ["err"], results r1_err.json,
    records provenance_err/run_info_err).
R1-ERRCAL  calibration of R1 under enlarged age errors with the error scale in the fit: data, null and
    power mocks drawn with true errors f x e_Age and fitted with f (README 2.8, T-059;
    PARAMS["parts"] = ["errcal"], results r1_errcal.json, records provenance_errcal/run_info_errcal).
"""
from __future__ import annotations

import json
import os
import shutil
import time
from pathlib import Path

import numpy as np
import pandas as pd

import m0
import mocks
import selaux

HERE = Path(__file__).parent

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
    # which pipeline runs: "orig" (README 2.0-2.4; r1/r2/r34/r56/r7/summary.json), "sel"
    # (README 2.5 R-SEL re-test, T-031; r1_sel/r34_sel/sel.json) or "selfit" alone (README 2.6
    # R1-SEL-FIT, T-049; r1_selfit.json) alone, or "err" alone (README 2.7 R1-ERR, T-054; r1_err.json),
    # or "errcal" alone (README 2.8 R1-ERRCAL, T-059; r1_errcal.json); no part overwrites another part's files
    "parts": ["err"],
    # R-SEL (README 2.5): pass tables (SEL-0), power floor and edge loop (SEL-3), mocks and stop (SEL-8)
    "sel_slices": [[-1.2, -0.6], [-0.6, 0.0], [0.0, 0.5]], "sel_pass_width": 1.0,
    "sel_pass_width_alt": 0.5, "sel_n_min": 200,
    "sel_power_floor": 0.12, "sel_power_floor_sens": 0.20, "sel_floor_sens_bins": [2, 3, 4],
    "sel_edge_min": 2.0, "sel_n_mock": 50, "sel_q_rank": 3, "sel_seed_tag": 31, "sel_stop_h": 16.0,
    # R1-SEL-FIT (README 2.6, T-049): data-independent starts in every R1 mock fit; results r1_selfit.json
    "selfit_seed_tag": 45, "selfit_nstart": 8, "selfit_stop_h": 12.0,
    # R1-ERR (README 2.7, T-054): error-scale ladder, metal-poor bins, rule settings; results r1_err.json
    "err_f": [1.2, 1.5, 2.0, 2.81], "err_bins": [0, 1, 2], "err_n_mock": 50, "err_reach_frac": 0.05,
    "err_min_bins": 2, "err_seed_tag": 54, "err_seed_tag_indep": 154, "err_stop_h": 16.0,
    # R1-ERRCAL (README 2.8, T-059): error scales, metal-poor bins, mocks per set, stream tags, stop limit;
    # results r1_errcal.json
    "errcal_f": [2.0, 2.81], "errcal_bins": [0, 1, 2], "errcal_n_mock": 50, "errcal_seed_tag": 59,
    "errcal_seed_tag_indep": 159, "errcal_stop_h": 16.0,
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


def onedim(C, age, eage, s15, *, f=1.0, nclass=None, none=False, truncate=True, grid=None, sel="cut",
           ptab=None):
    cells = m0.compress(age, eage, s15=s15, step_a=C.P["grid_step"], nclass=nclass or C.P["nclass"],
                        cut=C.P["cut"], none=none)
    return m0.OneD(grid or C.grid, cells, f=f, truncate=truncate, sel=sel, ptab=ptab)


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


def r1_decide(P, D, res, nmock, qrank=None):
    """Threshold d* and per-bin result from the mock sets of one bin/sample. qrank: rank of q_s
    (default: the 2.1 rule, 3rd smallest of 50 or 2nd smallest of the reduced 30)."""
    if qrank is None:
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
def grouped(C, sub, s15, *, f=1.0, feh_err=False, nclass=None, none=False, truncate=True, grid=None,
            sel="cut", ptab=None, slices=None):
    """slices (term E only): [Fe/H] slice bounds; the slice index becomes a cell key (m0.compress)."""
    P = C.P
    sl = None if slices is None else slice_index(sub["feh"].to_numpy(), slices)
    cells = m0.compress(sub["age"].to_numpy(), sub["eage"].to_numpy(), s15=s15, step_a=P["grid_step"],
                        nclass=nclass or P["nclass"], feh=sub["feh"].to_numpy(),
                        efeh=sub["efeh"].to_numpy() if feh_err else None, feh_step=P["feh_step"],
                        nefe=P["nefe"], cut=P["cut"], none=none, sl=sl)
    return m0.Grouped(grid or C.grid, cells, f=f, truncate=truncate, feh_err=feh_err, sel=sel, ptab=ptab)


def slice_index(feh, slices):
    """[Fe/H] slice of each star (lo <= [Fe/H] < hi); a star outside every slice is an error."""
    feh = np.asarray(feh, float)
    out = np.full(len(feh), -1, np.int64)
    for s, (lo, hi) in enumerate(slices):
        out[(feh >= lo) & (feh < hi)] = s
    if (out < 0).any():
        raise ValueError(f"{int((out < 0).sum())} stars outside the [Fe/H] slices")
    return out


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
    parts = list(P["parts"])
    if not parts or any(x not in ("orig", "sel", "selfit", "err", "errcal") for x in parts):
        raise ValueError("PARAMS['parts'] must be a non-empty subset of ['orig', 'sel', 'selfit', 'err', 'errcal'], "
                         f"got {parts}")
    if "selfit" in parts and len(parts) > 1:
        raise ValueError("PARAMS['parts'] = ['selfit'] runs alone (it reads r1_sel.json and keeps its own records)")
    if "err" in parts and len(parts) > 1:
        raise ValueError("PARAMS['parts'] = ['err'] runs alone (it reads r1_sel.json and r1_selfit.json and keeps "
                         "its own records)")
    if "errcal" in parts and len(parts) > 1:
        raise ValueError("PARAMS['parts'] = ['errcal'] runs alone (it reads r1_sel.json, r1_selfit.json and r1_err.json "
                         "and keeps its own records)")
    out = {}
    if "orig" in parts:
        out = main_orig(ctx, P)
    if "sel" in parts:
        sel = main_sel(ctx, P)
        out = sel if not out else {"orig": out, "sel": sel}
    if "selfit" in parts:
        out = main_selfit(ctx, P)
    if "err" in parts:
        out = main_err(ctx, P)
    if "errcal" in parts:
        out = main_errcal(ctx, P)
    return out


def main_orig(ctx, P):
    """The pre-registered pipeline of README 2.0-2.4 (unchanged)."""
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


# =============================================================================================
# R-SEL re-test (README 2.5, T-031)
# =============================================================================================
TERM_MODE = {"E": "emp", "N": "none"}
R1_SEL_MODE = {"S15E": "emp", "S15N": "none", "Full": "none"}


def r1_power_model_sel(C, fc, raw, floor):
    """SEL-3 power model: old weight max(raw, floor); young edge from the edge loop."""
    P = C.P
    t0, a, so = P["power_old"]
    wold = max(float(raw), float(floor))
    q, _, _ = m0.tn_cells(C.grid, t0 + a * fc, so)

    def gen(edge):
        young = ((C.grid.mid >= P["power_young"][0]) & (C.grid.mid < edge)).astype(float)
        return wold * q[0] + (1 - wold) * young / young.sum()

    def evaluate(edge):
        v = m0.valley(C.grid, gen(edge), lo=P["valley_lo"], hi=P["valley_hi"], side_mass=P["side_mass"],
                      prom=P["prom"])
        return v["valley"], v["d"]
    loop = selaux.edge_loop(evaluate, start=P["power_young"][1], step=P["power_edge_step"],
                            stop=P["sel_edge_min"], dmax=P["power_true_d_max"])
    return {"mu_old": t0 + a * fc, "s_old": so, "w_old": wold, "w_old_raw": float(raw), "floor": float(floor),
            "young": [P["power_young"][0], loop["edge"]], "true_d": loop["true_d"], "valid": loop["valid"],
            "invalid_reason": loop["reason"], "edge_trace": loop["trace"]}


def r1_data_sel(C, df, F, b, variant, coef):
    """R1-SEL data fit of one bin and variant (S15E, S15N, Full): the 2.1 fits (40 starts, K = 5
    rule, the two null families) with the variant's denominator, and the power models at the
    primary and the sensitivity floor (SEL-3). Random stream as 2.0 with sample codes
    0 = S15 term E, 1 = Full, 2 = S15 term N."""
    P = C.P
    lo, hi = P["r1_bins"][b]
    feh = df["feh"].to_numpy()
    s15 = variant != "Full"
    base = F["s15"] if s15 else F["valid"]
    m = base & (feh >= lo) & (feh < hi)
    age, eage = df["age"].to_numpy()[m], df["eage"].to_numpy()[m]
    model = onedim(C, age, eage, s15, sel=R1_SEL_MODE[variant], ptab=coef if variant == "S15E" else None)
    w = model.cells.w
    rng = np.random.default_rng([P["seed"], 1000 + b, selaux.R1_CODES[variant], int(round(C.grid.step * 1000))])
    fits = fit_mixtures(C, model, model.cells.A, w, P["kmax"], nstart=P["nstart_r1_data"], rng=rng)
    kbest, bics = choose_k(fits, model.cells.nstar)
    v, p, k5 = shape_from_fits(C, model, fits, kbest, model.cells.A, w, rng=rng, nstart=P["nstart_r1_data"])
    starts = {K: th for K, (th, _) in fits.items()}
    if k5 is not None:
        starts[P["kmax"] + 1] = k5
    sn, sp = r1_null_fits(P, model, rng)
    conv = {str(k): v_ for k, v_ in model.converged.items()}
    del model
    fc = 0.5 * (lo + hi)
    raw = float((F["early"] & (df["jphi"].to_numpy() > 500) & F["above"])[m].mean())
    pms = {"primary": r1_power_model_sel(C, fc, raw, P["sel_power_floor"]),
           "sens": r1_power_model_sel(C, fc, raw, P["sel_power_floor_sens"])}
    return {
        "variant": variant, "bin": [lo, hi], "n": int(m.sum()), "ncells": int(len(w)),
        "bic": {str(k): float(v_) for k, v_ in bics.items()}, "shape": v,
        "fits": {str(K): [float(x) for x in th] for K, (th, _) in fits.items()},
        "skewnorm": [float(x) for x in sn.x], "splitnorm": [float(x) for x in sp.x],
        "null_converged": {"skewnorm": bool(sn.success), "splitnorm": bool(sp.success)},
        "mix_converged": conv, "power_models": pms,
        "_starts": starts, "_n": int(m.sum()), "_p": p,
    }


def r1_null_fits(P, model, rng):
    """The two unimodal null families of the R1 data fit (README 2.0/2.1; R1-SEL 2.5): skew-normal and
    split-normal, 8 starts each (3 deterministic + 5 seeded perturbations of the first, drawn from rng),
    bounds as recorded, with the model's own selection term and error scale. Shared by r1_data_sel (f = 1)
    and r1_data_refit (README 2.8: the same fits with f)."""
    w = model.cells.w
    a0 = model.cells.A
    mu0 = float(np.average(a0, weights=w))
    sd0 = float(np.sqrt(np.average((a0 - mu0) ** 2, weights=w)))

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
    return sn, sp


def r1_mock_sel(C, D, kind, mech, floor, rng, pools):
    """One R1-SEL mock (SEL-2 generator; the S15 term-E mock builds its term E from its parent)."""
    P = C.P
    variant = D["variant"]
    s15 = variant != "Full"
    if kind == "null_sn":
        loc, lsc, al = D["skewnorm"]
        lat = lambda k: mocks.latent_skewnorm(loc, np.exp(lsc), al, k, rng, P["tmax"])
    elif kind == "null_sp":
        mm, l1, l2 = D["splitnorm"]
        lat = lambda k: mocks.latent_split(mm, np.exp(l1), np.exp(l2), k, rng, P["tmax"])
    else:
        pm = D["power_models"][floor]
        lat = lambda k: mocks.latent_power(pm["mu_old"], pm["s_old"], pm["w_old"], pm["young"][1], k, rng,
                                           lo=pm["young"][0], tmax=P["tmax"])
    edges, rpools = pools

    def draw(k):
        tau = lat(k)
        sl = np.zeros(k, np.int64)
        return {"tau": tau, "r": mocks.draw_r_keyed(tau, sl, edges, rpools, rng), "sl": sl}
    cat, par = mocks.catalogue_sel(draw, D["_n"], mech, rng, s15=s15, cut=P["cut"], tmax=P["tmax"])
    coef = None
    if variant == "S15E":
        coef = m0.pass_coefs(_pass_table(P, par["A"], par["e"] / par["A"], None, 1))
    model = onedim(C, cat["A"], cat["e"], s15, sel=R1_SEL_MODE[variant], ptab=coef)
    fits = fit_mixtures(C, model, model.cells.A, model.cells.w, P["kmax"], starts_from=D["_starts"], rng=rng)
    kbest, _ = choose_k(fits, model.cells.nstar)
    v, _, _ = shape_from_fits(C, model, fits, kbest, model.cells.A, model.cells.w, starts_from=D["_starts"], rng=rng)
    return {"d": float(v["d"]), "valley": bool(v["valley"]), "k": int(v["k"]),
            "pass_rate": (D["_n"] / len(par["A"])) if par is not None else None}


def r1_sel_bins(P, r1d, results, kof, nf, data_frac, v, floor, nbins, mechs, sens_bins, nmock):
    """R1-SEL per-bin decisions and verdict of one variant (2.1 rules, SEL-3); shared by R1-SEL-FIT (2.6)."""
    bins = []
    nfv = {}
    for b in range(nbins):
        D = r1d[(v, b)]
        res, mk = {}, {}
        for kind in selaux.R1_KINDS:
            for mech in mechs:
                fl = "sens" if (kind == "power" and floor == "sens" and b in sens_bins) else "primary"
                k = kof[("R1", v, b, None, kind, mech, fl)]
                res[(kind, mech)] = results[k]
                mk[f"{kind}_{mech}"] = {"k": k, "d": [r["d"] for r in results[k]], "valley": [r["valley"] for r in results[k]]}
                if nf[k]:
                    nfv[str(k)] = nf[k]
        dec = r1_decide(P, D, res, nmock, qrank=P["sel_q_rank"])
        pm = D["power_models"]["sens" if (floor == "sens" and b in sens_bins) else "primary"]
        if floor == "sens" and b not in sens_bins:
            dec["model_changed_without_set"] = bool(D["power_models"]["sens"]["w_old"] != D["power_models"]["primary"]["w_old"]
                                                    or D["power_models"]["sens"]["young"] != D["power_models"]["primary"]["young"])
        dec["resolvable_by_power"] = dec["resolvable"]
        dec["power_model_invalid"] = not pm["valid"]
        dec["resolvable"] = bool(dec["resolvable"] and pm["valid"])
        dec.update({"bin": D["bin"], "n": D["n"], "k": D["shape"]["k"], "cap": D["shape"]["cap"],
                    "valley": D["shape"]["valley"], "peaks": D["shape"]["peaks"], "power_model": pm,
                    "bic": D["bic"], "mocks": mk,
                    "pass_rate": {kk: (float(np.mean([r["pass_rate"] for r in res[(kn, me)]]))
                                       if v != "Full" else None)
                                  for kn in selaux.R1_KINDS for me in mechs for kk in [f"{kn}_{me}"]},
                    "data_pass_frac": data_frac[f"R1_{b}"] if v != "Full" else None})
        bins.append(dec)
    verdict, med = selaux.r1_verdict(bins, P["min_bins"], P["edge_range"])
    if nfv:                                          # any non-finite mock result of a set used here
        verdict, med = selaux.NONFINITE, None
    return {"bins": bins, "verdict": verdict, "median_edge": med, "nonfinite": nfv}


def _pass_table(P, age, rel, sl, nslice, width=None):
    return m0.pass_table(age, rel, sl, nslice=nslice, width=width or P["sel_pass_width"], tmax=P["tmax"],
                         n_min=P["sel_n_min"], cut=P["cut"])


def _pools(tab, rel):
    """(edges per slice, r pools per slice and pass bin) of a data pass table."""
    return [t["edges"] for t in tab], [[rel[ix] for ix in t["pools"]] for t in tab]


def _frac(tab):
    n = sum(sum(t["n"]) for t in tab)
    return sum(sum(t["n_pass"]) for t in tab) / n if n else None


def _clean(d):
    return {k: v for k, v in d.items() if not k.startswith("_")}


def _sel_key(P, df):
    """Checkpoint key (selaux.checkpoint_key): PARAMS values without selaux.NO_KEY_PARAMS ('parts' and the
    stop limits; they change no mock), the code of this study with run.py's PARAMS literal removed, and the catalogue."""
    src = {n: (HERE / n).read_text(encoding="utf-8") for n in ("run.py", "m0.py", "mocks.py", "selaux.py")}
    src["run.py"] = selaux.strip_params(src["run.py"])
    data = np.ascontiguousarray(pd.util.hash_pandas_object(df, index=True).to_numpy()).tobytes()
    return selaux.checkpoint_key(P, src, data)


ORIG_SEQ_INDEX = {"full": 1, "feh_err_full": 3, "full_f_min": 6}


def orig_seq_rng(P, index):
    """The 2.0 pipeline's shared stream C.rng = default_rng(seed), positioned as it was before that
    pipeline's index-th sequence fit (SEL-8: data fits keep the 2.0 streams). In main_orig, C.rng is
    first used by seven K = 1 mixture fits (R2 deconvolved S15 and Full, and the checks nclass_40,
    no_compression, untruncated, full_nclass_40, full_no_compression), whose start draws do not
    depend on the data; then each sequence fit draws its 8-start perturbations, in the order sample A
    (0), Full (1), a^2 e_[Fe/H]^2 (2), Full a^2 e_[Fe/H]^2 (3), f_min (4), f_max (5), Full f_min (6)."""
    rng = np.random.default_rng(P["seed"])
    dummy, w = np.array([1.0, 2.0]), np.ones(2)
    for _ in range(7):
        m0.mixture_starts(dummy, w, 1, P["nstart"], rng)
    Cx = Ctx(P)
    for _ in range(index):
        seq_starts(Cx, None, rng)
    return rng


def main_sel(ctx, P, store_root=None):
    """The R-SEL re-test (README 2.5). Writes r1_sel.json, r34_sel.json and sel.json."""

    t_start = time.time()
    C = Ctx(P)
    df = load(ctx, P)
    F = flags(df, P)
    A_all, E_all = df["age"].to_numpy(), df["eage"].to_numpy()
    feh, jphi = df["feh"].to_numpy(), df["jphi"].to_numpy()
    assert len(df) == P["n_rows"], f"row count {len(df)} != {P['n_rows']}"
    assert df["id"].is_unique, "Id not unique"
    jmed = float(np.nanmedian(jphi))
    assert P["jphi_median_range"][0] <= jmed <= P["jphi_median_range"][1], f"median JPHI {jmed}"
    with np.errstate(divide="ignore", invalid="ignore"):
        rel_all = E_all / A_all
    # SEL-0: rows with Age <= 0 have no relative error and are not in any parent; they are dropped from
    # every S15 sample of the re-test (so S15 is a subset of the parent) and from every r pool.
    pos = A_all > 0
    n_le0 = {"valid": int((F["valid"] & ~pos).sum()), "s15": int((F["s15"] & ~pos).sum())}
    ctx.log(f"R-SEL: rows with Age <= 0 dropped from the S15 samples and pools: {n_le0}")
    s15 = F["s15"] & pos
    F = dict(F, s15=s15)
    nbins = len(P["r1_bins"])
    mechs = P["mechs"]
    sens_bins = list(P["sel_floor_sens_bins"])
    nmock = int(P["sel_n_mock"])
    slices = P["sel_slices"]
    sets = selaux.sel_sets(nbins, mechs, sens_bins)
    # keep the original run's provenance and run_info before astrolab rewrites them after this run
    res_dir = getattr(ctx, "results", None)
    if res_dir is not None and Path(res_dir).resolve() == (HERE / "results").resolve():
        for name in ("provenance", "run_info"):
            src, dst = Path(res_dir) / f"{name}.json", Path(res_dir) / f"orig_{name}.json"
            if src.exists() and not dst.exists():
                shutil.copy2(src, dst)
    root = _store_root(ctx, store_root, "s010_sel_mocks")
    store = selaux.MockStore(root, _sel_key(P, df))   # refuses a stopped run without consent
    ctx.log(f"R-SEL checkpoints: {store.dir} ({'resumed with consent' if store.resumed else 'new or continued'})")
    memory = {}

    def mark(stage):
        memory[stage] = selaux.peak_memory_mb()
        ctx.log(f"R-SEL stage '{stage}' done; peak memory {memory[stage]} MB; elapsed {(time.time() - t_start) / 3600:.2f} h")

    try:
        out = _sel_body(ctx, P, C, df, F, A_all, E_all, feh, jphi, rel_all, s15, nbins, mechs, sens_bins,
                        nmock, slices, sets, store, mark, t_start)
    except selaux.StopRun:
        raise
    except BaseException:
        store.release()                    # checkpoints are kept for a rerun
        raise
    out["sel"]["memory_peak_mb"] = memory
    out["sel"]["age_le0_dropped"] = n_le0
    ctx.save("r1_sel", out["r1"])
    ctx.save("r34_sel", out["r34"])
    ctx.save("sel", out["sel"])
    store.release()
    ctx.log(f"R-SEL checkpoints kept in {store.dir} (a rerun reuses them; removed by the 7-day cleanup of "
            "a later run with another key)")
    return out["summary"]


def _sel_body(ctx, P, C, df, F, A_all, E_all, feh, jphi, rel_all, s15, nbins, mechs, sens_bins, nmock,
              slices, sets, store, mark, t_start):
    cut, tmax = P["cut"], P["tmax"]
    pos = A_all > 0                                       # SEL-0 parents and pools: Age > 0

    # ---------------- parents and pass tables (SEL-0)
    win = (feh > P["seq_feh"][0]) & (feh < P["seq_feh"][1])
    selA_full = F["valid"] & F["above"] & (jphi > P["seq_jphi"]) & win
    selA = selA_full & s15
    selB_full = F["valid"] & F["early"] & (jphi > P["seq_jphi"]) & win
    selB = selB_full & s15
    sel2e_full = F["valid"] & F["early"] & win
    sel2e = sel2e_full & s15

    def r2_sel(base):
        return base & (jphi > P["r2_jphi"]) & (feh > P["r2_feh"][0]) & (feh < P["r2_feh"][1]) & F["early"]

    def table(mask, sliced, width=None):
        sl = slice_index(feh[mask], slices) if sliced else None
        return _pass_table(P, A_all[mask], rel_all[mask], sl, len(slices) if sliced else 1, width)

    tabs = {"sampleA": (selA_full, True), "sampleB": (selB_full, True), "fig2e": (sel2e_full, True),
            "R2": (r2_sel(F["valid"]), False)}
    for b, (lo, hi) in enumerate(P["r1_bins"]):
        tabs[f"R1_{b}"] = (F["valid"] & (feh >= lo) & (feh < hi), False)
    T = {name: table(mask, sliced) for name, (mask, sliced) in tabs.items()}
    T_alt = {"sampleA_w0p5": table(selA_full, True, P["sel_pass_width_alt"]),
             "sampleB_w0p5": table(selB_full, True, P["sel_pass_width_alt"]),
             "sampleA_1slice": table(selA_full, False), "sampleB_1slice": table(selB_full, False)}
    coefs = {k: m0.pass_coefs(v) for k, v in {**T, **T_alt}.items()}
    pools = {name: _pools(T[name], rel_all[mask]) for name, (mask, _) in tabs.items()}
    data_frac = {name: _frac(T[name]) for name in T}
    pass_tables = {k: m0.table_json(v) for k, v in {**T, **T_alt}.items()}
    mark("pass tables")

    # ---------------- R2 deconvolved latent Gaussian, terms E and N (SEL-6)
    r2s = {}
    m2 = r2_sel(s15)
    for term in ("E", "N"):
        mod = onedim(C, A_all[m2], E_all[m2], True, sel=TERM_MODE[term], ptab=coefs["R2"] if term == "E" else None)
        th = fit_mixtures(C, mod, mod.cells.A, mod.cells.w, 1)[1][0]
        r2s[term] = {"mu": float(th[0]), "sigma": float(np.exp(th[1])), "n": int(m2.sum())}
        del mod
    mark("R2 deconvolved")

    # ---------------- sample A (SEL-4)
    subA, subAf, subB, sub2e = (df[m] for m in (selA, selA_full, selB, sel2e))

    def gsel(sub, term, coef, **kw):
        if term == "E":
            return grouped(C, sub, True, sel="emp", ptab=coef,
                           slices=slices if coef["c"].shape[0] > 1 else None, **kw)
        return grouped(C, sub, True, sel="none", **kw)

    seq = {t: fit_seq(C, gsel(subA, t, coefs["sampleA"])) for t in ("E", "N")}
    lb = P["late_bins"]
    ratios = []
    for lo in np.arange(lb[0], lb[1] - 1e-9, lb[2]):
        mm = F["valid"] & F["late"] & (feh >= lo) & (feh < lo + lb[2]) & (A_all - 2 * E_all > 0) & (A_all + 2 * E_all < tmax)
        if mm.sum() > 50:
            ratios.append({"bin": [float(lo), float(lo + lb[2])], "ratio": float(A_all[mm].std() / np.sqrt(np.mean(E_all[mm] ** 2))), "n": int(mm.sum())})
    f_i = min(r["ratio"] for r in ratios)
    e2A = float(np.mean(subA["eage"].to_numpy() ** 2))
    fscale = {}
    for t in ("E", "N"):
        f_ii = float(np.sqrt(1 + seq[t]["sigma"] ** 2 / e2A))
        fscale[t] = {"f_i": f_i, "f_ii": f_ii, "f_max": float(min(f_i, f_ii)), "f_min": P["f_min"],
                     "e2_mean": e2A}
    # robustness fits (2.3 / SEL-4); Full fits have denominator 1 and are shared by both terms; they
    # use the 2.0 stream positions, so they reproduce the original run's Full fits (orig_seq_rng)
    shared = {"full": fit_seq(C, grouped(C, subAf, False), rng=orig_seq_rng(P, ORIG_SEQ_INDEX["full"])),
              "feh_err_full": fit_seq(C, grouped(C, subAf, False, feh_err=True),
                                      rng=orig_seq_rng(P, ORIG_SEQ_INDEX["feh_err_full"])),
              "full_f_min": fit_seq(C, grouped(C, subAf, False, f=P["f_min"]),
                                    rng=orig_seq_rng(P, ORIG_SEQ_INDEX["full_f_min"]))}
    orig_full = None
    try:                                     # the recorded 2.0 values, saved next to the re-fits
        o = json.loads((HERE / "results" / "r34.json").read_text(encoding="utf-8"))["sampleA_sensitivity"]
        orig_full = {k: {kk: o[k][kk] for kk in ("tau0", "a", "sigma", "span")} for k in ORIG_SEQ_INDEX if k in o}
    except (OSError, ValueError, KeyError):
        pass
    rob = {}
    for t in ("E", "N"):
        fm = fscale[t]["f_max"]
        rob[t] = {"feh_err": fit_seq(C, gsel(subA, t, coefs["sampleA"], feh_err=True)),
                  "f_min": fit_seq(C, gsel(subA, t, coefs["sampleA"], f=P["f_min"])),
                  "f_max": fit_seq(C, gsel(subA, t, coefs["sampleA"], f=fm)),
                  "full_f_max": fit_seq(C, grouped(C, subAf, False, f=fm))}
    mark("sample A fits")
    # term-E extra fits without verdict (SEL-4)
    extra = {}
    for tcut in P["span_trunc"]:
        extra[f"feh_lt_{tcut}"] = fit_seq(C, gsel(subA[subA["feh"] < tcut], "E", coefs["sampleA"]))
    extra["edge_drop"] = fit_seq(C, gsel(subA[subA["age"] + 2 * subA["eage"] < tmax], "E", coefs["sampleA"]))
    extra["untruncated"] = fit_seq(C, gsel(subA, "E", coefs["sampleA"], truncate=False))
    Cg = Ctx(P, P["grid_check_step"])
    extra["grid_0p02"] = fit_seq(Cg, grouped(Cg, subA, True, grid=Cg.grid, sel="emp", ptab=coefs["sampleA"], slices=slices))
    extra["nclass_40"] = fit_seq(C, gsel(subA, "E", coefs["sampleA"], nclass=P["nclass_check"]))
    extra["no_compression"] = fit_seq(C, gsel(subA, "E", coefs["sampleA"], none=True))
    fig2e = fit_seq(C, gsel(sub2e, "E", coefs["fig2e"]))
    rngb = np.random.default_rng(P["seed"] + 34)
    boots = []
    for _ in range(P["n_boot"]):
        bs = subA.iloc[rngb.integers(0, len(subA), len(subA))]
        boots.append(fit_seq(C, gsel(bs, "E", coefs["sampleA"]), th=seq["E"]["_x"])["sigma"])
    mark("sample A extra fits")

    # ---------------- sample B (SEL-5)
    mixB, mixB_f = {}, {}
    for t in ("E", "N"):
        mixB[t] = fit_mixB(C, gsel(subB, t, coefs["sampleB"]), seq=seq[t])
        mixB_f[t] = {"f_min": fit_mixB(C, gsel(subB, t, coefs["sampleB"], f=P["f_min"]), seq=seq[t], th=mixB[t]["_x"]),
                     "f_max": fit_mixB(C, gsel(subB, t, coefs["sampleB"], f=fscale[t]["f_max"]), seq=seq[t], th=mixB[t]["_x"])}
    mark("sample B fits")
    # SEL-7: term E with 0.5 Gyr pass bins and with one slice (data fits only)
    sel7 = {}
    for name, ca, cb in (("pass_bins_0p5", "sampleA_w0p5", "sampleB_w0p5"), ("one_slice", "sampleA_1slice", "sampleB_1slice")):
        fa = fit_seq(C, gsel(subA, "E", coefs[ca]))
        fb = fit_mixB(C, gsel(subB, "E", coefs[cb]), seq=fa, th=mixB["E"]["_x"])
        sel7[name] = {"sampleA": {"sigma_sel": fa["sigma"], "span": fa["span"], "tau0": fa["tau0"], "a": fa["a"]},
                      "sampleB": {"sigma_int": fb["sigma"], "sigma_err": fb["sigma_err"], "f_bg": fb["f_bg"]}}
    mark("SEL-7 fits")

    # ---------------- R1 data fits (SEL-3)
    r1d = {}
    for v in selaux.R1_VARIANTS:
        for b in range(nbins):
            D = r1_data_sel(C, df, F, b, v, coefs[f"R1_{b}"])
            r1d[(v, b)] = D
            pm, ps = D["power_models"]["primary"], D["power_models"]["sens"]
            ctx.log(f"R1-SEL data {v} bin {b}: K={D['shape']['k']} d={D['shape']['d']:.3f}; power model "
                    f"w_old={pm['w_old']:.3f} edge={pm['young'][1]} true d={pm['true_d']:.3f} valid={pm['valid']}; "
                    f"floor {P['sel_power_floor_sens']}: edge={ps['young'][1]} true d={ps['true_d']:.3f} valid={ps['valid']}")
    Cc = Ctx(P, P["grid_check_step"])
    r1_check = r1_data_sel(Cc, df, F, P["r1_check_bin"], "S15E", coefs[f"R1_{P['r1_check_bin']}"])["shape"]
    mark("R1 data fits")

    # ---------------- background fits for the misspecification mocks (2.3, 40 starts)
    bgsel = F["valid"] & F["early"] & (jphi > P["seq_jphi"]) & ~F["above"] & F["has_a"]
    bgfits = []
    for lo, hi in P["bg_slices"]:
        mm = bgsel & (feh >= lo) & (feh < hi)
        mod = onedim(C, A_all[mm], E_all[mm], False)
        fits = fit_mixtures(C, mod, mod.cells.A, mod.cells.w, P["kmax"], nstart=P["nstart_r1_data"])
        kb, _ = choose_k(fits, mod.cells.nstar)
        mu_, s_, w_ = m0.mix_unpack(fits[kb][0], kb)
        bgfits.append({"slice": [lo, hi], "mu": mu_, "s": s_, "w": w_, "feh": feh[mm], "k": int(kb)})
        del mod
    mark("background fits")

    # ---------------- mocks (SEL-2, SEL-8)
    nA, nB = len(subA), len(subB)
    parA_feh = feh[selA_full & (A_all > 0)]
    parB_feh = feh[selB_full & (A_all > 0)]
    subAf_pos = df[selA_full & pos]                                                  # Age > 0 (SEL-0)
    parA_rows = subAf_pos[["feh"]].assign(r=subAf_pos["eage"] / subAf_pos["age"]).to_numpy()   # SEL-2 diagnostic only
    allf_bg = np.concatenate([g["feh"] for g in bgfits])

    def seq_cat(term, mech, fe_draw, rng, keyed=True):
        t0, a, ls = seq[term]["_x"]

        def draw(k):
            if keyed:
                fe = fe_draw(k)
                tau = _seq_latent(fe, t0, a, np.exp(ls), rng, tmax)
                sl = slice_index(fe, slices)
                return {"tau": tau, "r": mocks.draw_r_keyed(tau, sl, *pools["sampleA"], rng), "feh": fe, "sl": sl}
            rows = parA_rows[rng.integers(0, len(parA_rows), k)]
            tau = _seq_latent(rows[:, 0], t0, a, np.exp(ls), rng, tmax)
            return {"tau": tau, "r": rows[:, 1], "feh": rows[:, 0], "sl": slice_index(rows[:, 0], slices)}
        return mocks.catalogue_sel(draw, nA, mech, rng, s15=True, cut=cut, tmax=tmax)

    def fit_mock_seq(term, cat, par, rng):
        sub = pd.DataFrame({"age": cat["A"], "eage": cat["e"], "feh": cat["feh"], "efeh": 0.0})
        coef = None
        if term == "E":
            coef = m0.pass_coefs(_pass_table(P, par["A"], par["e"] / par["A"], par["sl"], len(slices)))
        return fit_seq(C, gsel(sub, term, coef), th=seq[term]["_x"], rng=rng)

    def run_one(s, rng):
        if s["tag"] == "R1":
            D = r1d[(s["variant"], s["bin"])]
            return r1_mock_sel(C, D, s["kind"], s["mech"], s["floor"], rng, pools[f"R1_{s['bin']}"])
        if s["tag"] in ("A_rec", "diag"):
            keyed = s["tag"] == "A_rec"
            cat, par = seq_cat(s["term"], s["mech"], lambda k: parA_feh[rng.integers(0, len(parA_feh), k)], rng, keyed)
            fit = fit_mock_seq(s["term"], cat, par, rng)
            return {"sigma": fit["sigma"], "a": fit["a"], "tau0": fit["tau0"], "pass_rate": nA / len(par["A"])}
        # sample B: identifiability (id) and misspecification (mis) mocks
        term = s["term"]
        t0, a, ls, b0, b1, lsb, eta = mixB[term]["_x"]
        fb = 1 / (1 + np.exp(-eta))

        def draw(k):
            bg = rng.random(k) < fb
            fe = parB_feh[rng.integers(0, len(parB_feh), k)]
            tau = np.empty(k)
            ko = ~bg
            tau[ko] = _seq_latent(fe[ko], t0, a, np.exp(ls), rng, tmax)
            nb_ = int(bg.sum())
            if s["kind"] == "id":
                tau[bg] = _seq_latent(fe[bg], b0, b1, np.exp(lsb), rng, tmax)
            else:
                fsel = rng.choice(allf_bg, nb_)
                tb = np.empty(nb_)
                for g in bgfits:
                    mm = (fsel >= g["slice"][0]) & (fsel < g["slice"][1])
                    kk = int(mm.sum())
                    if kk:
                        tb[mm] = mocks.latent_mixture(g["mu"], g["s"], g["w"], kk, rng, tmax)
                fe[bg], tau[bg] = fsel, tb
            sl = slice_index(fe, slices)
            return {"tau": tau, "r": mocks.draw_r_keyed(tau, sl, *pools["sampleB"], rng), "feh": fe, "sl": sl}
        cat, par = mocks.catalogue_sel(draw, nB, s["mech"], rng, s15=True, cut=cut, tmax=tmax)
        sub = pd.DataFrame({"age": cat["A"], "eage": cat["e"], "feh": cat["feh"], "efeh": 0.0})
        coef = None
        if term == "E":
            coef = m0.pass_coefs(_pass_table(P, par["A"], par["e"] / par["A"], par["sl"], len(slices)))
        fit = fit_mixB(C, gsel(sub, term, coef), th=mixB[term]["_x"], rng=rng)
        return {"sigma": fit["sigma"], "pass_rate": nB / len(par["A"])}

    t_m = time.time()
    results, state, proj_log = selaux.run_mock_sets(
        sets, nmock, store, run_one, lambda k, j: selaux.mock_rng(P["seed"], P["sel_seed_tag"], k, j),
        P["sel_stop_h"], ctx.log)
    mark("mocks")
    mock_info = {"n_per_set": nmock, "n_sets": len(sets), "n_main_sets": sum(1 for s in sets if s.get("floor") != "sens"),
                 "elapsed_h_this_session": (time.time() - t_m) / 3600, "elapsed_h_total": store.elapsed_s() / 3600,
                 "projections": proj_log, "resumed": store.resumed, "resumes": store.resumes(),
                 "stop_limit_h": store.limit_h if store.limit_h is not None else P["sel_stop_h"],
                 "stop_limit_source": ("consent limit.json (takes precedence over PARAMS['sel_stop_h'] for this "
                                       "checkpoint folder)" if store.limit_h is not None else "PARAMS['sel_stop_h']"),
                 "nonfinite_per_set": {s["k"]: sum(selaux.nonfinite(r) for r in results[s["k"]]) for s in sets},
                 "mean_s_per_mock": {g: float(np.mean([t for st in state.values() if st["group"] == g for t in st["times"]]))
                                     for g in ("R1", "AB", "diag")}}
    nf = {s["k"]: sum(selaux.nonfinite(r) for r in results[s["k"]]) for s in sets}
    kof = {}
    for s in sets:
        kof[(s["tag"], s.get("variant"), s.get("bin"), s.get("term"), s["kind"], s["mech"], s.get("floor"))] = s["k"]

    # ---------------- R1-SEL decisions
    def r1_bins(v, floor):
        return r1_sel_bins(P, r1d, results, kof, nf, data_frac, v, floor, nbins, mechs, sens_bins, nmock)

    r1v = {v: r1_bins(v, "primary") for v in selaux.R1_VARIANTS}
    r1s = {v: r1_bins(v, "sens") for v in selaux.R1_VARIANTS}
    for v in r1s.values():                                 # the sensitivity copy: power-related fields only
        for b in v["bins"]:
            b["mocks"] = {k: x for k, x in b["mocks"].items() if k.startswith("power")}
    lab1 = selaux.r1_label(r1v["S15E"]["verdict"], r1v["S15N"]["verdict"], r1v["Full"]["verdict"])
    lab1s = selaux.r1_label(r1s["S15E"]["verdict"], r1s["S15N"]["verdict"], r1s["Full"]["verdict"])
    r1_out = {"variants": r1v, "floor_sensitivity": r1s, "label": lab1, "label_floor_sensitivity": lab1s,
              "floor": P["sel_power_floor"], "floor_sens": P["sel_power_floor_sens"], "q_rank": P["sel_q_rank"],
              "n_mock": nmock, "check_grid_0p02_bin": r1_check,
              "data_fits": {f"{v}_{b}": _clean({k: x for k, x in D.items() if k not in ("shape",)}) for (v, b), D in r1d.items()},
              "latent_density": {f"{v}_{b}": (D["_p"] / C.grid.step).round(5).tolist() for (v, b), D in r1d.items()},
              "grid_mid": C.grid.mid.round(3).tolist()}

    # ---------------- R3-SEL / R4-SEL decisions
    def bias(vals, true):
        v_ = np.asarray(vals, float) - true
        n_ = len(v_)
        return {"bias": float(v_.mean()), "mc_err": float(v_.std(ddof=1) / np.sqrt(n_)) if n_ > 1 else None}

    def near(b_, tol):
        return b_["mc_err"] is not None and abs(abs(b_["bias"]) - tol) <= b_["mc_err"]

    r34t = {}
    for t in ("E", "N"):
        rec = {}
        nft = {}
        for mech in mechs:
            kk_ = kof[("A_rec", None, None, t, "rec", mech, None)]
            if nf[kk_]:
                nft[str(kk_)] = nf[kk_]
            rr = results[kk_]
            bs = bias([r["sigma"] for r in rr], seq[t]["sigma"])
            ba = bias([r["a"] for r in rr], seq[t]["a"])
            rec[mech] = {"sigma": bs, "a": ba,
                         "pass": bool(selaux.recovery_pass(bs["bias"], ba["bias"], P["rec_tol_sigma"], P["rec_tol_a"])),
                         "near_tolerance": bool(near(bs, P["rec_tol_sigma"]) or near(ba, P["rec_tol_a"])),
                         "sigma_values": [r["sigma"] for r in rr], "a_values": [r["a"] for r in rr],
                         "pass_rate": float(np.mean([r["pass_rate"] for r in rr]))}
        prim, flag = selaux.primacy(rec["rA"]["pass"], rec["rtau"]["pass"])
        if nft:                                          # recovery biases undefined: no primacy, no verdict
            prim, flag = None, False
        pfit = seq[t] if prim == "S15" else shared["full"] if prim == "Full" else None
        R3, R4 = selaux.r34_bare(pfit, P["span_range"], P["sigma_paper"], P["sigma_tol"])
        if nft:
            R3 = R4 = selaux.NONFINITE
        if prim == "S15":
            r3_set = {"full": shared["full"], "feh_err": rob[t]["feh_err"], "f_min": rob[t]["f_min"], "f_max": rob[t]["f_max"]}
            r4_set = {"full": shared["full"], "feh_err": rob[t]["feh_err"]}
        elif prim == "Full":
            r3_set = {"feh_err_full": shared["feh_err_full"], "full_f_min": shared["full_f_min"], "full_f_max": rob[t]["full_f_max"]}
            r4_set = {"feh_err_full": shared["feh_err_full"]}
        else:
            r3_set, r4_set = {}, {}
        lo_s, hi_s = P["span_range"]
        r3_rob = bool(r3_set) and all(lo_s <= x["span"] <= hi_s for x in r3_set.values())
        r4_rob = bool(r4_set) and all(abs(x["sigma"] - P["sigma_paper"]) <= P["sigma_tol"] for x in r4_set.values())
        r34t[t] = {"sampleA": _clean(seq[t]), "error_scale": fscale[t], "recovery": rec, "nonfinite": nft,
                   "primary": prim, "flag_rtau_recovery_failed": bool(flag),
                   "R3": {"bare": R3, "robust": r3_rob, "label": selaux.with_robust(R3, r3_rob), "set": sorted(r3_set)},
                   "R4": {"bare": R4, "robust": r4_rob, "label": selaux.with_robust(R4, r4_rob), "set": sorted(r4_set)},
                   "robustness_fits": {**{k: _clean(x) for k, x in rob[t].items()}}}
    for name in ("R3", "R4"):
        q = selaux.selterm(r34t["E"][name]["bare"], r34t["N"][name]["bare"])
        r34t["E"][name]["selection_term"] = q
        r34t["E"][name]["label_full"] = f"{r34t['E'][name]['label']}; {q}"

    # ---------------- intrinsic-SEL decisions
    intr = {}
    for t in ("E", "N"):
        bsets = {}
        nfb = {}
        for kind in selaux.B_KINDS:
            for mech in mechs:
                kk_ = kof[("B", None, None, t, kind, mech, None)]
                if nf[kk_]:
                    nfb[str(kk_)] = nf[kk_]
                rr = results[kk_]
                bb = bias([r["sigma"] for r in rr], mixB[t]["sigma"])
                bb["near_tolerance"] = bool(near(bb, P["rec_tol_sigma"]))
                bb["sigma_values"] = [r["sigma"] for r in rr]
                bb["pass_rate"] = float(np.mean([r["pass_rate"] for r in rr]))
                bsets[f"{kind}_{mech}"] = bb
        ids = [r["sigma"] for mech in mechs for r in results[kof[("B", None, None, t, "id", mech, None)]]]
        sd_id = float(np.std(ids, ddof=1)) if len(ids) > 1 else 0.0
        biases = [b_["bias"] for b_ in bsets.values()]

        def lab(fit):
            if nfb:
                return selaux.NONFINITE, None
            if not (np.isfinite(fit["sigma_err"]) and np.isfinite(sd_id) and np.isfinite(fit["sigma"])):
                return "cannot determine (non-finite standard error)", None
            se = max(fit["sigma_err"], sd_id)
            return selaux.intrinsic_bare(fit["sigma"], se, biases, P["rec_tol_sigma"], P["z_one_sided"], P["sigma_paper"]), se
        v0, se0 = lab(mixB[t])
        vf = {k: lab(x)[0] for k, x in mixB_f[t].items()}
        robust = bool(selaux.same_category(v0, vf["f_min"], vf["f_max"]))
        intr[t] = {"sampleB": _clean(mixB[t]), "sampleB_f": {k: _clean(x) for k, x in mixB_f[t].items()},
                   "mock_bias": bsets, "sd_id": sd_id, "se_used": se0, "bare": v0, "f_labels": vf, "robust": robust,
                   "nonfinite": nfb,
                   "label": f"{v0}, {'robust' if robust else 'not robust'}"}
    q = selaux.selterm(intr["E"]["bare"], intr["N"]["bare"])
    intr["E"]["selection_term"] = q
    intr["E"]["label_full"] = f"{intr['E']['label']}; {q}"

    # ---------------- SEL-2 diagnostic
    diag = {}
    for t in ("E", "N"):
        for mech in mechs:
            kk_ = kof[("diag", None, None, t, "diag", mech, None)]
            rr = results[kk_]
            diag[f"{t}_{mech}"] = {"nonfinite": nf[kk_], "sigma": bias([r["sigma"] for r in rr], seq[t]["sigma"]),
                                   "a": bias([r["a"] for r in rr], seq[t]["a"]),
                                   "pass_rate": float(np.mean([r["pass_rate"] for r in rr]))}

    # ---------------- per-set pass rates against the data (SEL-6)
    rates = []
    for s in sets:
        pr = [r.get("pass_rate") for r in results[s["k"]]]
        pr = [x for x in pr if x is not None]
        if s["tag"] == "R1":
            df_ = data_frac[f"R1_{s['bin']}"] if s["variant"] != "Full" else None
        else:
            df_ = data_frac["sampleA" if s["tag"] in ("A_rec", "diag") else "sampleB"]
        rates.append({**{k: v for k, v in s.items() if k != "group"},
                      "mock_pass_rate": float(np.mean(pr)) if pr else None,
                      "mock_pass_rate_sd": float(np.std(pr)) if len(pr) > 1 else None, "data_pass_frac": df_})

    r34_out = {"terms": r34t, "shared_full_fits": {k: _clean(x) for k, x in shared.items()},
               "shared_full_fits_orig_recorded": orig_full,
               "sampleA_extra_E": {k: _clean(x) for k, x in extra.items()},
               "sampleA_sigma_boot_sd_E": float(np.std(boots)),
               "fig2e_E": _clean(fig2e), "intrinsic": intr, "n_mock": nmock,
               "labels": {"R3-SEL": r34t["E"]["R3"]["label_full"], "R4-SEL": r34t["E"]["R4"]["label_full"],
                          "intrinsic-SEL": intr["E"]["label_full"],
                          "term_N": {"R3": r34t["N"]["R3"]["label"], "R4": r34t["N"]["R4"]["label"],
                                     "intrinsic": intr["N"]["label"]}}}
    sel_out = {"pass_tables": pass_tables, "data_pass_frac": data_frac, "r2_deconvolved": r2s,
               "sel7": sel7, "diagnostic": diag, "mock_pass_rates": rates, "mocks": mock_info,
               "sets": [{k: v for k, v in s.items()} for s in sets],
               "background_fits": [{"slice": g["slice"], "k": g["k"], "mu": g["mu"], "s": g["s"], "w": g["w"],
                                    "n": int(len(g["feh"]))} for g in bgfits],
               "labels": {"R1-SEL": lab1["label"], "R1-SEL_floor_0.20": lab1s["label"],
                          "R3-SEL": r34_out["labels"]["R3-SEL"], "R4-SEL": r34_out["labels"]["R4-SEL"],
                          "intrinsic-SEL": r34_out["labels"]["intrinsic-SEL"]},
               "runtime_h": (time.time() - t_start) / 3600, "params": P}
    summary = {"labels": sel_out["labels"], "mocks": {k: mock_info[k] for k in ("n_per_set", "n_sets", "elapsed_h_total")},
               "runtime_h": sel_out["runtime_h"]}
    return {"r1": r1_out, "r34": r34_out, "sel": sel_out, "summary": summary}


# =============================================================================================
# R1-SEL-FIT (README 2.6, T-049): R1-SEL with data-independent starts in every mock fit
# =============================================================================================
def r1_mock_selfit(C, D, kind, mech, floor, rngs, pools, nstart, f=1.0):
    """One R1-SEL-FIT mock: the R1-SEL mock of r1_mock_sel (catalogue and fit (o) on the SEL-8 stream,
    unchanged), then fit (i) from nstart data-independent starts per K on its own stream, consumed in
    the order K = 1..kmax, then kmax + 1; per K the better fit (selaux.better_fit) is used (README 2.6).
    f scales the deviate of the generator (README 2.7; f = 1 is the R1-SEL-FIT generator)."""
    cat, par = selfit_catalogue(C, D, kind, mech, floor, rngs[0], pools, f=f)
    return selfit_fits(C, D, cat, par, rngs, nstart)


def selfit_catalogue(C, D, kind, mech, floor, rng, pools, f=1.0, stats=None):
    """The catalogue of an R1-SEL-FIT / R1-ERR mock (SEL-2 generator on the mock's first stream; f scales
    the deviate, README 2.7). Returns (sample, parent) of mocks.catalogue_sel."""
    P = C.P
    variant = D["variant"]
    s15 = variant != "Full"
    if kind == "null_sn":
        loc, lsc, al = D["skewnorm"]
        lat = lambda k: mocks.latent_skewnorm(loc, np.exp(lsc), al, k, rng, P["tmax"])
    elif kind == "null_sp":
        mm, l1, l2 = D["splitnorm"]
        lat = lambda k: mocks.latent_split(mm, np.exp(l1), np.exp(l2), k, rng, P["tmax"])
    else:
        pm = D["power_models"][floor]
        lat = lambda k: mocks.latent_power(pm["mu_old"], pm["s_old"], pm["w_old"], pm["young"][1], k, rng,
                                           lo=pm["young"][0], tmax=P["tmax"])
    edges, rpools = pools

    def draw(k):
        tau = lat(k)
        sl = np.zeros(k, np.int64)
        return {"tau": tau, "r": mocks.draw_r_keyed(tau, sl, edges, rpools, rng), "sl": sl}
    return mocks.catalogue_sel(draw, D["_n"], mech, rng, s15=s15, cut=P["cut"], tmax=P["tmax"], f=f, stats=stats)


def selfit_fits(C, D, cat, par, rngs, nstart, f=1.0):
    """Fits (o) and (i) of an R1-SEL-FIT / R1-ERR / R1-ERRCAL mock catalogue. The model is built with the
    error scale f: f = 1 for R1-SEL-FIT and R1-ERR (README 2.6, 2.7), the mock's own f for R1-ERRCAL
    (README 2.8). At f = 1 this is the R1-SEL-FIT fit path, unchanged."""
    P = C.P
    rng, rng2 = rngs
    variant = D["variant"]
    s15 = variant != "Full"
    coef = None
    if variant == "S15E":
        coef = m0.pass_coefs(_pass_table(P, par["A"], par["e"] / par["A"], None, 1))
    model = onedim(C, cat["A"], cat["e"], s15, f=f, sel=R1_SEL_MODE[variant], ptab=coef)
    A, w, n = model.cells.A, model.cells.w, model.cells.nstar
    kmax, K5 = P["kmax"], P["kmax"] + 1
    # (o): exactly r1_mock_sel's fits, on the SEL-8 stream
    fits_o = fit_mixtures(C, model, A, w, kmax, starts_from=D["_starts"], rng=rng)
    kb_o, _ = choose_k(fits_o, n)
    v_o, _, k5_o = shape_from_fits(C, model, fits_o, kb_o, A, w, starts_from=D["_starts"], rng=rng)
    nll_o = {K: float(x[1]) for K, x in fits_o.items()}
    # (i): data-independent starts on stream (i), K = 1..kmax in order
    fits_i = {}
    for K in range(1, kmax + 1):
        try:
            r = model.fit_mixture(K, m0.mixture_starts(A, w, K, nstart, rng2))
            fits_i[K] = (r.x, float(r.fun))
        except RuntimeError:                       # every start non-finite: (i) not available for this K
            fits_i[K] = (None, float("nan"))
    use = {K: selaux.better_fit(nll_o[K], fits_i[K][1]) for K in range(1, kmax + 1)}
    fits = {K: (fits_i[K] if use[K] == "i" else fits_o[K]) for K in range(1, kmax + 1)}
    kb, _ = choose_k(fits, n)
    th5, use5 = None, None
    if kb == kmax:
        nll5 = float("nan")
        try:
            r5 = model.fit_mixture(K5, m0.mixture_starts(A, w, K5, nstart, rng2))
            th5, nll5 = r5.x, float(r5.fun)
        except RuntimeError:
            pass
        use5 = "i"
        if k5_o is not None:
            nll5_o = float(model.mix_negll(k5_o, K5)[0])
            use5 = selaux.better_fit(nll5_o, nll5)
            if use5 == "o":
                th5 = k5_o
        if th5 is None:
            raise RuntimeError("K = 5 fit (i) failed and no (o) K = 5 fit exists")
    p = m0.mix_cells(C.grid, fits[kb][0], kb)
    keep = None
    if kb == kmax:
        p5 = m0.mix_cells(C.grid, th5, K5)
        pk5 = [C.grid.mid[i] for i in m0.peaks(p5 / C.grid.step, P["prom"])]
        keep = lambda t: any(abs(t - u) <= P["mode_match"] for u in pk5)
    v = m0.valley(C.grid, p, lo=P["valley_lo"], hi=P["valley_hi"], side_mass=P["side_mass"],
                  prom=P["prom"], keep_peaks=keep)
    nll = {K: float(fits[K][1]) for K in fits}
    return {"d": float(v["d"]), "valley": bool(v["valley"]), "k": int(kb),
            "valley_t": (float(v["t"]) if v["t"] is not None else None),
            "o_d": float(v_o["d"]), "o_valley": bool(v_o["valley"]), "o_k": int(v_o["k"]),
            **{f"i_used_k{K}": use[K] == "i" for K in range(1, kmax + 1)},
            "i_used_k5": {None: -1, "o": 0, "i": 1}[use5],          # -1: no K = 5 fit (K = 4 not chosen)
            # NLL rising with K, over K = 1..kmax (T-045 also counted K = 5 for its better fits)
            "o_nonmonotone": len(selaux.nonmonotone_k(nll_o)), "nonmonotone": len(selaux.nonmonotone_k(nll)),
            "pass_rate": (D["_n"] / len(par["A"])) if par is not None else None}


def selfit_data_check(D, rf, rb, tag, tol=1e-9):
    """README 2.6 reproduction check of one R1 data fit against r1_sel.json (absolute tol); list of mismatches."""
    bad = []

    def cmp(name, a, b_):
        a, b_ = np.asarray(a, float), np.asarray(b_, float)
        if a.shape != b_.shape or not np.all(np.abs(a - b_) <= tol):
            bad.append(f"{tag}.{name}")
    if set(D["fits"]) != set(rf["fits"]):
        bad.append(f"{tag}.fits.keys")
    for K, th in rf["fits"].items():
        if K in D["fits"]:
            cmp(f"fits.{K}", D["fits"][K], th)
    cmp("skewnorm", D["skewnorm"], rf["skewnorm"])
    cmp("splitnorm", D["splitnorm"], rf["splitnorm"])
    for fl in ("primary", "sens"):
        for key, val in rf["power_models"][fl].items():     # every numeric field of the recorded power model
            if isinstance(val, bool) or val is None or isinstance(val, str):
                if D["power_models"][fl].get(key) != val:
                    bad.append(f"{tag}.power_models.{fl}.{key}")
            elif key != "edge_trace":
                cmp(f"power_models.{fl}.{key}", D["power_models"][fl][key], val)
        if "edge_trace" in rf["power_models"][fl]:          # rows (edge, has valley, true d), as floats
            cmp(f"power_models.{fl}.edge_trace", [[float(x) for x in row] for row in D["power_models"][fl]["edge_trace"]],
                [[float(x) for x in row] for row in rf["power_models"][fl]["edge_trace"]])
    cmp("d", D["shape"]["d"], rb["d"])
    cmp("k", D["shape"]["k"], rb["k"])
    return bad


def selfit_mock_check(results, sets, recorded):
    """README 2.6: fit (o) must reproduce every recorded R1-SEL mock (d within 1e-9, same valley flag).
    recorded: r1_sel.json. Returns the list of [k, j] that differ (a missing record counts)."""
    recmock = {}
    for src in ("variants", "floor_sensitivity"):
        for v in selaux.R1_VARIANTS:
            for B in recorded[src][v]["bins"]:
                for x in B["mocks"].values():
                    recmock[x["k"]] = x
    bad = []
    for s in sets:
        x = recmock.get(s["k"])
        for j, r in enumerate(results[s["k"]]):
            if (x is None or j >= len(x["d"]) or x["d"][j] is None or r["o_d"] is None
                    or abs(r["o_d"] - x["d"][j]) > 1e-9 or r["o_valley"] != x["valley"][j]):
                bad.append([s["k"], j])
    return bad, recmock


def main_selfit(ctx, P, store_root=None, recorded=None):
    """R1-SEL-FIT (README 2.6, T-049). Writes r1_selfit.json; r1_sel.json is read, never written."""

    t_start = time.time()
    if hasattr(ctx, "record_suffix"):
        ctx.record_suffix = "_selfit"            # provenance_selfit.json, run_info_selfit.json
    C = Ctx(P)
    df = load(ctx, P)
    F = flags(df, P)
    A_all, E_all = df["age"].to_numpy(), df["eage"].to_numpy()
    feh = df["feh"].to_numpy()
    assert len(df) == P["n_rows"], f"row count {len(df)} != {P['n_rows']}"
    with np.errstate(divide="ignore", invalid="ignore"):
        rel_all = E_all / A_all
    F = dict(F, s15=F["s15"] & (A_all > 0))       # SEL-0, as main_sel
    nbins, mechs = len(P["r1_bins"]), P["mechs"]
    sens_bins = list(P["sel_floor_sens_bins"])
    nmock = int(P["sel_n_mock"])
    rec = recorded if recorded is not None else json.loads((HERE / "results" / "r1_sel.json").read_text(encoding="utf-8"))
    # pass tables and pools of the R1 bins (as _sel_body: Full parent of the bin, all rows)
    pools, coefs, data_frac = {}, {}, {}
    for b, (lo, hi) in enumerate(P["r1_bins"]):
        mask = F["valid"] & (feh >= lo) & (feh < hi)
        tab = _pass_table(P, A_all[mask], rel_all[mask], None, 1)
        coefs[b] = m0.pass_coefs(tab)
        pools[b] = _pools(tab, rel_all[mask])
        data_frac[f"R1_{b}"] = _frac(tab)
    r1d, mism = {}, []
    for v in selaux.R1_VARIANTS:
        for b in range(nbins):
            D = r1_data_sel(C, df, F, b, v, coefs[b])
            r1d[(v, b)] = D
            mism += selfit_data_check(D, rec["data_fits"][f"{v}_{b}"], rec["variants"][v]["bins"][b], f"{v}_{b}")
            ctx.log(f"R1-SEL-FIT data {v} bin {b}: K={D['shape']['k']} d={D['shape']['d']:.3f}")
    out = {"status": None, "data_fit_mismatches": mism, "n_mock": nmock,
           "nstart_indep": int(P["selfit_nstart"]), "seed_tag_indep": int(P["selfit_seed_tag"])}
    if mism:
        out["status"] = "not evaluable (reproduction): data fits differ from r1_sel.json"
        out["label"] = {"label": out["status"]}
        out["params"] = P
        ctx.save("r1_selfit", out)
        return {"R1-SEL-FIT": out["status"]}
    sets = selaux.selfit_sets(nbins, mechs, sens_bins)
    root = _store_root(ctx, store_root, "s010_selfit_mocks")
    store = selaux.MockStore(root, _sel_key(P, df))
    ctx.log(f"R1-SEL-FIT checkpoints: {store.dir}")

    def run_one(s, rngs):
        D = r1d[(s["variant"], s["bin"])]
        return r1_mock_selfit(C, D, s["kind"], s["mech"], s["floor"], rngs, pools[s["bin"]], int(P["selfit_nstart"]))

    def make_rng(k, j):
        return (selaux.mock_rng(P["seed"], P["sel_seed_tag"], k, j),
                np.random.default_rng([int(P["seed"]), int(P["selfit_seed_tag"]), int(k), int(j)]))
    try:                                           # the lock is released on every path; checkpoints stay
        return _selfit_finish(ctx, P, store, sets, nmock, run_one, make_rng, r1d, data_frac, rec, out, t_start)
    finally:
        store.release()


USED_FIELDS = ("d", "valley", "k", "pass_rate")      # fields the R1 rules use (the non-finite rule looks at these)


def _selfit_finish(ctx, P, store, sets, nmock, run_one, make_rng, r1d, data_frac, rec, out, t_start):
    nbins, mechs, sens_bins = len(P["r1_bins"]), P["mechs"], list(P["sel_floor_sens_bins"])
    results, state, proj_log = selaux.run_mock_sets(sets, nmock, store, run_one, make_rng,
                                                    P["selfit_stop_h"], ctx.log)
    nf = {s["k"]: sum(selaux.nonfinite({f: r.get(f) for f in USED_FIELDS}) for r in results[s["k"]]) for s in sets}
    kof = {("R1", s["variant"], s["bin"], None, s["kind"], s["mech"], s["floor"]): s["k"] for s in sets}
    repro_bad, recmock = selfit_mock_check(results, sets, rec)
    out["mock_reproduction"] = {"n_mocks": sum(len(results[s["k"]]) for s in sets),
                                "n_mismatches": len(repro_bad), "mismatches": repro_bad[:50]}
    r1v = {v: r1_sel_bins(P, r1d, results, kof, nf, data_frac, v, "primary", nbins, mechs, sens_bins, nmock)
           for v in selaux.R1_VARIANTS}
    r1s = {v: r1_sel_bins(P, r1d, results, kof, nf, data_frac, v, "sens", nbins, mechs, sens_bins, nmock)
           for v in selaux.R1_VARIANTS}
    for vv in r1s.values():                       # the sensitivity copy: power-related fields only
        for B in vv["bins"]:
            B["mocks"] = {k: x for k, x in B["mocks"].items() if k.startswith("power")}
    lab = selaux.r1_label(r1v["S15E"]["verdict"], r1v["S15N"]["verdict"], r1v["Full"]["verdict"])
    labs = selaux.r1_label(r1s["S15E"]["verdict"], r1s["S15N"]["verdict"], r1s["Full"]["verdict"])
    if repro_bad:
        out["status"] = "not evaluable (reproduction): fit (o) differs from the recorded R1-SEL mocks"
        lab = {"label": out["status"], "computed_label_not_used": lab}
        labs = {"label": out["status"], "computed_label_not_used": labs}
    elif nmock != 50:                              # README 2.6: labels need 50 mocks in every set
        out["status"] = f"no label (exploration with {nmock} mocks per set; the label needs 50)"
        lab = {"label": out["status"], "computed_label_not_used": lab}
        labs = {"label": out["status"], "computed_label_not_used": labs}
    else:
        out["status"] = "evaluated"
    dstar_new, dstar_rec = {}, {}
    for v in selaux.R1_VARIANTS:
        for b in range(nbins):
            for fl, src_new, src_rec in (("primary", r1v, "variants"), ("sens", r1s, "floor_sensitivity")):
                dstar_new[(v, b, fl)] = src_new[v]["bins"][b]["d_star"]
                dstar_rec[(v, b, fl)] = rec[src_rec][v]["bins"][b]["d_star"]
    per_set = []                                   # reported, no verdict
    for s in sets:
        rr, x = results[s["k"]], recmock.get(s["k"])
        key = (s["variant"], s["bin"], s["floor"])
        dn, dr = dstar_new[key], dstar_rec[key]
        passes = lambda valley, d, ds: bool(valley and d is not None and d < ds)
        per_set.append({**{k: s[k] for k in ("k", "variant", "bin", "kind", "mech", "floor")},
                        "valley_new": int(sum(r["valley"] for r in rr)),
                        "valley_recorded": int(sum(x["valley"])) if x else None,
                        "valley_changed": int(sum(r["valley"] != r["o_valley"] for r in rr)),
                        "pass_changed": (int(sum(passes(r["valley"], r["d"], dn) != passes(x["valley"][j], x["d"][j], dr)
                                                 for j, r in enumerate(rr))) if x else None),
                        "i_used_by_k": {str(K): int(sum(r[f"i_used_k{K}"] for r in rr)) for K in range(1, P["kmax"] + 1)},
                        "i_used_k5": int(sum(r["i_used_k5"] == 1 for r in rr)),
                        "o_nonmonotone": int(sum(r["o_nonmonotone"] > 0 for r in rr)),
                        "new_nonmonotone": int(sum(r["nonmonotone"] > 0 for r in rr)),
                        "k_o": {str(K): int(sum(r["o_k"] == K for r in rr)) for K in range(1, P["kmax"] + 1)},
                        "k_new": {str(K): int(sum(r["k"] == K for r in rr)) for K in range(1, P["kmax"] + 1)},
                        "d_new_quantiles_5_50_80_95": [float(q) for q in np.percentile([r["d"] for r in rr], [5, 50, 80, 95])],
                        "mean_s_per_mock": float(np.mean(state[s["k"]]["times"]))})
    recv = rec["variants"]
    out.update({"label": lab, "label_floor_sensitivity": labs, "variants": r1v, "floor_sensitivity": r1s,
                "recorded_r1_sel": {"label": rec["label"]["label"],
                                    "verdicts": {v: recv[v]["verdict"] for v in selaux.R1_VARIANTS},
                                    **{key: {v: [B[key] for B in recv[v]["bins"]] for v in selaux.R1_VARIANTS}
                                       for key in ("power", "d_star", "q", "fpr", "resolvable")}},
                "per_set": per_set, "nonfinite": {str(k): x for k, x in nf.items() if x},
                "mocks": {"n_sets": len(sets), "projections": proj_log, "elapsed_h_total": store.elapsed_s() / 3600,
                          "resumed": store.resumed, "resumes": store.resumes(),
                          "stop_limit_h": store.limit_h if store.limit_h is not None else P["selfit_stop_h"]},
                "runtime_h": (time.time() - t_start) / 3600, "params": P})
    ctx.save("r1_selfit", out)
    return {"R1-SEL-FIT": lab["label"], "R1-SEL-FIT floor 0.20": labs["label"], "status": out["status"]}


# =============================================================================================
# R1-ERR (README 2.7, T-054): error-scale power test of R1-SEL-FIT
# =============================================================================================
ERR_PCT_D = [5, 50, 80, 95]
ERR_PCT_AGE = [5, 50, 95]


def r1_mock_err(C, D, mech, rngs, pools, nstart, f):
    """One R1-ERR power mock (README 2.7): the R1-SEL-FIT power mock (primary power model) with the
    deviate scaled by f, fitted with f = 1 exactly as in R1-SEL-FIT. A RuntimeError of the generator
    (mocks.catalogue_sel, the latent sampler or the r draw inside it) is a generator failure, returned
    as gen_fail = True (feasibility rule); an error of the fits is raised, as in R1-SEL-FIT."""
    return mock_scaled(C, D, "power", mech, rngs, pools, nstart, f, 1.0)


def mock_scaled(C, D, kind, mech, rngs, pools, nstart, f, fit_f):
    """An R1 mock drawn with true errors f x e (selfit_catalogue on rngs[0]; kind null_sn, null_sp or power
    with the primary power model) and fitted by the R1-SEL-FIT procedure with the error scale fit_f
    (R1-ERR: fit_f = 1; R1-ERRCAL: fit_f = f). A RuntimeError of the generator is returned as
    gen_fail = True; an error of the fits is raised."""
    stats = {}
    try:
        cat, par = selfit_catalogue(C, D, kind, mech, "primary", rngs[0], pools, f=f, stats=stats)
    except RuntimeError:
        return {"gen_fail": True, "d": None, "valley": None, "k": None, "pass_rate": None,
                "dropped": stats.get("dropped"), "drawn": stats.get("drawn")}
    res = selfit_fits(C, D, cat, par, rngs, nstart, f=fit_f)
    age = np.percentile(cat["A"], ERR_PCT_AGE)
    res.update({"gen_fail": False, "dropped": int(stats["dropped"]), "drawn": int(stats["drawn"]),
                **{f"age_p{q}": float(a) for q, a in zip(ERR_PCT_AGE, age)}})
    return res


def r1_data_refit(C, df, F, b, variant, coef, f, nulls=False):
    """README 2.7 companion data refit: the R1 data fit of one metal-poor bin and variant with the error
    scale f in the likelihood (run.onedim with f); 40 starts on default_rng([seed, 1000 + b, code, 50,
    round(100 f)]); K = 1..kmax by BIC and the K = 5 rule. No power model.
    nulls=True (README 2.8, R1-ERRCAL): after the mixture fits, computed exactly as above (so d and K are
    R1-ERR's companion refits), the two null families are fitted with f on the same stream
    (r1_null_fits), and the result also carries what the R1-ERRCAL mocks need: the young-side edge and
    peaks, the fits per K, the null parameters, and (private) the mock fit starts per K (with K = 5 if
    fitted) and the latent density."""
    P = C.P
    lo, hi = P["r1_bins"][b]
    feh = df["feh"].to_numpy()
    s15 = variant != "Full"
    m = (F["s15"] if s15 else F["valid"]) & (feh >= lo) & (feh < hi)
    model = onedim(C, df["age"].to_numpy()[m], df["eage"].to_numpy()[m], s15, f=f, sel=R1_SEL_MODE[variant],
                   ptab=coef if variant == "S15E" else None)
    w = model.cells.w
    rng = np.random.default_rng([P["seed"], 1000 + b, selaux.R1_CODES[variant], 50, int(round(100 * f))])
    fits = fit_mixtures(C, model, model.cells.A, w, P["kmax"], nstart=P["nstart_r1_data"], rng=rng)
    kbest, bics = choose_k(fits, model.cells.nstar)
    v, p, k5 = shape_from_fits(C, model, fits, kbest, model.cells.A, w, rng=rng, nstart=P["nstart_r1_data"])
    out = {"f": float(f), "variant": variant, "bin": [lo, hi], "n": int(m.sum()), "d": float(v["d"]),
           "k": int(v["k"]), "valley": bool(v["valley"]), "d_lt_d_cap": bool(v["d"] < P["d_cap"]),
           "valley_t": v["t"], "bic": {str(k): float(x) for k, x in bics.items()}}
    if nulls:
        starts = {K: th for K, (th, _) in fits.items()}
        if k5 is not None:
            starts[P["kmax"] + 1] = k5
        sn, sp = r1_null_fits(P, model, rng)
        out.update({"edge": v["edge"], "peaks": v["peaks"], "cap": bool(v["cap"]), "ncells": int(len(w)),
                    "fits": {str(K): [float(x) for x in th] for K, (th, _) in fits.items()},
                    "k5": None if k5 is None else [float(x) for x in k5],
                    "skewnorm": [float(x) for x in sn.x], "splitnorm": [float(x) for x in sp.x],
                    "null_converged": {"skewnorm": bool(sn.success), "splitnorm": bool(sp.success)},
                    "mix_converged": {str(k): bool(x) for k, x in model.converged.items()},
                    "_starts": starts, "_p": p})
    return out


def bin_name(P, b):
    lo, hi = P["r1_bins"][b]
    return f"[{lo:g}, {hi:g})"


def err_generator_check(P, rfit, run_one_f1):
    """README 2.7 check (b): mock j = 0 of each primary power set of the R1-ERR bins, regenerated by the
    new code at f = 1 on R1-SEL-FIT's streams and set numbers, must give the recorded d (absolute 1e-9)
    and valley flag. run_one_f1(variant, bin, mech, k) returns the mock result."""
    nbins = len(P["r1_bins"])
    kfit = {(s["variant"], s["bin"], s["mech"]): s["k"]
            for s in selaux.selfit_sets(nbins, P["mechs"], list(P["sel_floor_sens_bins"]))
            if s["kind"] == "power" and s["floor"] == "primary"}
    rows, bad = [], []
    for v in selaux.R1_VARIANTS:
        for b in P["err_bins"]:
            for mech in P["mechs"]:
                k = kfit[(v, b, mech)]
                recm = rfit["variants"][v]["bins"][b]["mocks"][f"power_{mech}"]
                r = run_one_f1(v, b, mech, k)
                ok = (recm["k"] == k and not r.get("gen_fail") and r["d"] is not None
                      and abs(r["d"] - recm["d"][0]) <= 1e-9 and bool(r["valley"]) == bool(recm["valley"][0]))
                rows.append({"variant": v, "bin": b, "mech": mech, "k": k, "d": r["d"], "valley": r["valley"],
                             "d_recorded": recm["d"][0], "valley_recorded": recm["valley"][0], "ok": bool(ok)})
                if not ok:
                    bad.append([v, b, mech])
    return {"n": len(rows), "mismatches": bad, "rows": rows}


def _pct(xs, qs):
    xs = [x for x in xs if x is not None]
    return [float(q) for q in np.percentile(xs, qs)] if xs else None


def err_evaluate(P, sets, results, times, rfit, data_age_pct=None, data_frac=None):
    """README 2.7 decision rules and reported items from the mock results (k -> list of result dicts).
    rfit: r1_selfit.json (data d, the f = 1 row, the metal-rich bins of the R1 verdict at f). Pure: no
    fits, no files. Returns the r1_err.json body without the checks and run records."""
    nmock = int(P["err_n_mock"])
    bins, mechs = [int(b) for b in P["err_bins"]], list(P["mechs"])
    ladder = [float(x) for x in P["err_f"]]
    frac, frac_med = float(P["err_reach_frac"]), 0.5
    dcap = float(P["d_cap"])
    kmax = int(P["kmax"])
    data_d = {v: {b: float(rfit["variants"][v]["bins"][b]["d"]) for b in bins} for v in selaux.R1_VARIANTS}
    names = {b: bin_name(P, b) for b in bins}
    by = {(s["f"], s["variant"], s["bin"], s["mech"]): s for s in sets}
    # ---- per set (reported)
    per_set = []
    for s in sets:
        rr = results.get(s["k"], [])
        ok = [r for r in rr if not r.get("gen_fail")]
        ds, vs = [r["d"] for r in rr], [r["valley"] for r in rr]
        dd = data_d[s["variant"]][s["bin"]]
        n_reach, n_nov = selaux.err_counts(ds, vs, dd)
        row = {**{k: s[k] for k in ("k", "f", "variant", "bin", "mech")}, "bin_name": names[s["bin"]],
               "n_run": len(rr), "complete": len(rr) == nmock, "gen_fail": sum(1 for r in rr if r.get("gen_fail")),
               "d": ds, "valley": vs, "d_data": dd, "n_reach": n_reach,
               # 95% interval of n_reach / 50; for a set the feasibility rule left incomplete, of n_reach over
               # the mocks it ran (flagged; such a set enters no rule)
               "n_reach_cp95": (selaux.clopper_pearson(n_reach, nmock) if len(rr) >= nmock
                                else (selaux.clopper_pearson(n_reach, len(rr)) if rr else None)),
               "n_reach_cp95_over_completed": len(rr) < nmock, "n_novalley": n_nov,
               "n_d_ge_data_incl_novalley": n_reach + n_nov}
        if ok:
            has_age = all(f"age_p{q}" in r for r in ok for q in ERR_PCT_AGE)
            row.update({
                "frac_valley": sum(1 for r in ok if r["valley"]) / len(ok),
                "power_at_d_cap": sum(1 for r in ok if r["valley"] and r["d"] < dcap) / len(ok),
                "d_pct_5_50_80_95": _pct([r["d"] for r in ok], ERR_PCT_D),   # all mocks (d = 1 without a valley)
                "d_pct_5_50_80_95_valley_only": _pct([r["d"] for r in ok if r["valley"]], ERR_PCT_D),
                "k_chosen": {str(K): sum(1 for r in ok if r["k"] == K) for K in range(1, kmax + 1)},
                "i_used_by_k": {str(K): sum(1 for r in ok if r.get(f"i_used_k{K}")) for K in range(1, kmax + 1)},
                "i_used_k5": sum(1 for r in ok if r.get("i_used_k5") == 1),
                "nonmonotone": sum(1 for r in ok if (r.get("nonmonotone") or 0) > 0),
                "o_nonmonotone": sum(1 for r in ok if (r.get("o_nonmonotone") or 0) > 0),
                "mean_pass_rate": (float(np.mean([r["pass_rate"] for r in ok]))
                                   if s["variant"] != "Full" and all(r.get("pass_rate") is not None for r in ok)
                                   else None),
                "data_pass_frac": (data_frac or {}).get(f"R1_{s['bin']}") if s["variant"] != "Full" else None,
                "age_pct_5_50_95_median_over_mocks": ([float(np.median([r[f"age_p{q}"] for r in ok]))
                                                       for q in ERR_PCT_AGE] if has_age else None),
                "data_age_pct_5_50_95": (data_age_pct or {}).get(f"{s['variant']}_{s['bin']}"),
            })
        row["dropped_by_redraw_limit"] = sum(int(r.get("dropped") or 0) for r in rr)
        row["stars_drawn"] = sum(int(r.get("drawn") or 0) for r in rr)
        tt = times.get(s["k"], [])
        row["mean_s_per_mock"] = float(np.mean(tt)) if tt else None
        per_set.append(row)
    ps = {r["k"]: r for r in per_set}
    # ---- feasibility (the S15 term E sets decide; the ladder is cut at the first failing f)
    fails = [s["f"] for s in sets if s["variant"] == "S15E" and ps[s["k"]]["gen_fail"] > 0]
    cut_f = min(fails) if fails else None
    feasible = {f: (cut_f is None or f < cut_f) for f in ladder}
    for s in sets:                                  # every set of a feasible f has all its mocks
        if feasible[s["f"]] and not ps[s["k"]]["complete"]:
            raise RuntimeError(f"R1-ERR set k={s['k']} at feasible f={s['f']} has {ps[s['k']]['n_run']} "
                               f"of {nmock} mocks")
    # ---- per variant and f
    variants, f1 = {}, {}
    for v in selaux.R1_VARIANTS:
        rb = rfit["variants"][v]["bins"]
        row1 = []                                   # the f = 1 row from the R1-SEL-FIT per-mock d (reported)
        for b in bins:
            mk = rb[b]["mocks"]
            nr = {m: selaux.err_counts(mk[f"power_{m}"]["d"], mk[f"power_{m}"]["valley"], data_d[v][b])[0]
                  for m in mechs}
            row1.append({"bin": b, "bin_name": names[b], "n_reach": nr,
                         "explainable": selaux.err_explainable(nr, len(mk[f"power_{mechs[0]}"]["d"]), frac)})
        f1[v] = {"E": sum(x["explainable"] for x in row1), "bins": row1}
        per_f, E, Em, ex_names, exm_names, not_eval, nonfin = {}, {}, {}, {}, {}, [], False
        for f in ladder:
            ks = [by[(f, v, b, m)]["k"] for b in bins for m in mechs]
            nfail = sum(ps[k]["gen_fail"] for k in ks)
            if not feasible[f]:
                per_f[selaux.ffmt(f)] = {"status": "not feasible", "gen_fail": nfail}
                E[f] = Em[f] = None
                continue
            if nfail:                                # S15 term N / Full only (S15E failures cut the ladder)
                per_f[selaux.ffmt(f)] = {"status": "not evaluable at f", "gen_fail": nfail}
                E[f] = Em[f] = None
                not_eval.append(f)
                continue
            if any(selaux.nonfinite({fld: r.get(fld) for fld in USED_FIELDS}) for k in ks for r in results[k]):
                nonfin = True
            brows = []
            for b in bins:
                kk = {m: by[(f, v, b, m)]["k"] for m in mechs}
                nr = {m: ps[kk[m]]["n_reach"] for m in mechs}
                brows.append({"bin": b, "bin_name": names[b], "d_data": data_d[v][b], "n_reach": nr,
                              "n_novalley": {m: ps[kk[m]]["n_novalley"] for m in mechs},
                              "explainable": selaux.err_explainable(nr, nmock, frac),
                              "explainable_median_rule": selaux.err_explainable(nr, nmock, frac_med),
                              "power_at_d_cap": {m: ps[kk[m]]["power_at_d_cap"] for m in mechs}})
            E[f] = sum(x["explainable"] for x in brows)
            Em[f] = sum(x["explainable_median_rule"] for x in brows)
            ex_names[f] = [x["bin_name"] for x in brows if x["explainable"]]
            exm_names[f] = [x["bin_name"] for x in brows if x["explainable_median_rule"]]
            # the 2.1 verdict R1 would read at f: power at d* = 0.25 in the R1-ERR bins; data d, power-model
            # validity and the other bins (not run) as recorded in R1-SEL-FIT
            r1bins = []
            for b, B in enumerate(rb):
                B = dict(B)
                if b in bins:
                    pwb = next(x["power_at_d_cap"] for x in brows if x["bin"] == b)
                    B["resolvable"] = bool(all(p_ >= P["power_needed"] for p_ in pwb.values())
                                           and B["power_model"]["valid"])
                r1bins.append(B)
            verdict, _ = selaux.r1_verdict(r1bins, P["min_bins"], P["edge_range"])
            per_f[selaux.ffmt(f)] = {"status": "evaluated", "E": E[f], "E_median_rule": Em[f],
                                     "explainable_bins": ex_names[f], "explainable_bins_median_rule": exm_names[f],
                                     "bins": brows, "r1_verdict_at_f": verdict}
        ne = not_eval if v != "S15E" else ()
        variants[v] = {"per_f": per_f, "nonfinite": nonfin, "not_evaluable_at": not_eval,
                       "label": selaux.err_label(ladder, E, cut_f, ex_names, min_bins=int(P["err_min_bins"]),
                                                 n_bins=len(bins), nonfinite=nonfin, not_evaluable=ne),
                       "label_median_rule": selaux.err_label(ladder, Em, cut_f, exm_names,
                                                             min_bins=int(P["err_min_bins"]), n_bins=len(bins),
                                                             nonfinite=nonfin, not_evaluable=ne)}
    return {"ladder": ladder, "bins": bins, "bin_names": [names[b] for b in bins], "d_cap": dcap,
            "data_d": {v: [data_d[v][b] for b in bins] for v in selaux.R1_VARIANTS},
            "cut_f": cut_f, "feasible": {selaux.ffmt(f): x for f, x in feasible.items()},
            "f1_row": f1, "variants": variants, "per_set": per_set,
            "label": variants["S15E"]["label"], "label_median_rule": variants["S15E"]["label_median_rule"]}


def _is_formal(ctx):
    """True for `astrolab run` (writes results/), False for `astrolab explore` (explore/<date>-<tag>/)."""
    res = getattr(ctx, "results", None)
    return (getattr(ctx, "max_save_bytes", None) is None and res is not None
            and Path(res).resolve() == (HERE / "results").resolve())


def _store_root(ctx, store_root, name):
    """Checkpoint root of a mock block (R-SEL, R1-SEL-FIT, R1-ERR, R1-ERRCAL): an explicit store_root (tests) as given;
    the formal run's `<cache>/<name>`; an exploration's own `<cache>/<name>_explore/<date>-<tag>`, so that an
    exploration never writes into (or is pruned together with) the formal checkpoints (T-058)."""
    from astrolab import config
    if store_root:
        return Path(store_root)
    if _is_formal(ctx):
        return config.cache_dir() / name
    return config.cache_dir() / f"{name}_explore" / Path(ctx.results).name


def main_err(ctx, P, store_root=None, recorded=None, recorded_fit=None):
    """R1-ERR (README 2.7, T-054). Writes r1_err.json; r1_sel.json and r1_selfit.json are read, never written."""

    t_start = time.time()
    if hasattr(ctx, "record_suffix"):
        ctx.record_suffix = "_err"               # provenance_err.json, run_info_err.json
    C = Ctx(P)
    df = load(ctx, P)
    F = flags(df, P)
    A_all, E_all = df["age"].to_numpy(), df["eage"].to_numpy()
    feh = df["feh"].to_numpy()
    assert len(df) == P["n_rows"], f"row count {len(df)} != {P['n_rows']}"
    with np.errstate(divide="ignore", invalid="ignore"):
        rel_all = E_all / A_all
    F = dict(F, s15=F["s15"] & (A_all > 0))       # S15 samples without Age <= 0 (README 2.5 SEL-0, kept by 2.7)
    bins = [int(b) for b in P["err_bins"]]
    nmock = int(P["err_n_mock"])
    nstart = int(P["selfit_nstart"])
    seed = int(P["seed"])
    rec = recorded if recorded is not None else json.loads((HERE / "results" / "r1_sel.json").read_text(encoding="utf-8"))
    rfit = (recorded_fit if recorded_fit is not None
            else json.loads((HERE / "results" / "r1_selfit.json").read_text(encoding="utf-8")))
    # pass tables and pools of the R1-ERR bins (as main_selfit); the data bins' observed-age percentiles
    pools, coefs, data_frac, data_age = {}, {}, {}, {}
    for b in bins:
        lo, hi = P["r1_bins"][b]
        mask = F["valid"] & (feh >= lo) & (feh < hi)
        tab = _pass_table(P, A_all[mask], rel_all[mask], None, 1)
        coefs[b] = m0.pass_coefs(tab)
        pools[b] = _pools(tab, rel_all[mask])
        data_frac[f"R1_{b}"] = _frac(tab)
        for v in selaux.R1_VARIANTS:
            mv = (F["s15"] if v != "Full" else F["valid"]) & (feh >= lo) & (feh < hi)
            data_age[f"{v}_{b}"] = [float(x) for x in np.percentile(A_all[mv], ERR_PCT_AGE)]
    # check (a): the data fits equal r1_sel.json
    r1d, mism = {}, []
    for v in selaux.R1_VARIANTS:
        for b in bins:
            D = r1_data_sel(C, df, F, b, v, coefs[b])
            r1d[(v, b)] = D
            mism += selfit_data_check(D, rec["data_fits"][f"{v}_{b}"], rec["variants"][v]["bins"][b], f"{v}_{b}")
            ctx.log(f"R1-ERR data {v} bin {b}: K={D['shape']['k']} d={D['shape']['d']:.3f}")
    out = {"status": None, "n_mock": nmock, "seed_tags": [int(P["err_seed_tag"]), int(P["err_seed_tag_indep"])],
           "checks": {"data_fit_mismatches": mism},
           "threads": {**{k: os.environ.get(k) for k in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS")},
                       "cpu_count": os.cpu_count(),
                       "note": "environment variables of the last session (null: the libraries chose their own thread counts); every session of a run must use the same settings"}}

    def fail(status):
        out["status"] = status
        out["label"] = {"case": 1, "label": "not evaluable (reproduction)"}
        out.update({"runtime_h": (time.time() - t_start) / 3600, "params": P})
        ctx.save("r1_err", out)
        return {"R1-ERR": out["label"]["label"], "status": status}
    if mism:
        return fail("not evaluable (reproduction): data fits differ from r1_sel.json")

    # check (b): the generator at f = 1 on R1-SEL-FIT's streams and set numbers
    def one_f1(v, b, mech, k):
        rngs = (selaux.mock_rng(seed, P["sel_seed_tag"], k, 0),
                np.random.default_rng([seed, int(P["selfit_seed_tag"]), int(k), 0]))
        return r1_mock_err(C, r1d[(v, b)], mech, rngs, pools[b], nstart, 1.0)
    gen = err_generator_check(P, rfit, one_f1)
    out["checks"]["generator_f1"] = gen
    ctx.log(f"R1-ERR check (b): {gen['n'] - len(gen['mismatches'])} of {gen['n']} mocks reproduced")
    if gen["mismatches"]:
        return fail("not evaluable (reproduction): the f = 1 generator differs from the recorded R1-SEL-FIT mocks")
    sets = selaux.err_sets(P["err_f"], bins, P["mechs"])
    root = _store_root(ctx, store_root, "s010_err_mocks")
    store = selaux.MockStore(root, _sel_key(P, df), name="R1-ERR", rule="README 2.7")   # refuses a stopped run without consent
    ctx.log(f"R1-ERR checkpoints: {store.dir} ({'resumed with consent' if store.resumed else 'new or continued'})")

    def run_one(s, rngs):
        return r1_mock_err(C, r1d[(s["variant"], s["bin"])], s["mech"], rngs, pools[s["bin"]], nstart, s["f"])

    def make_rng(k, j):
        return (selaux.mock_rng(seed, P["err_seed_tag"], k, j),
                np.random.default_rng([seed, int(P["err_seed_tag_indep"]), int(k), int(j)]))
    try:                                           # the lock is released on every path; checkpoints stay
        results, state, proj_log = selaux.run_mock_sets(sets, nmock, store, run_one, make_rng, P["err_stop_h"],
                                                        ctx.log, cut=err_cut, name="R1-ERR", rule="README 2.7")
        mock_info = {"n_sets": len(sets), "projections": proj_log, "elapsed_h_total": store.elapsed_s() / 3600,
                     "resumed": store.resumed, "resumes": store.resumes(),
                     "stop_limit_h": store.limit_h if store.limit_h is not None else P["err_stop_h"]}
    finally:
        store.release()
    ev = err_evaluate(P, sets, results, {k: st["times"] for k, st in state.items()}, rfit, data_age, data_frac)
    out.update(ev)
    if nmock != 50:                                # README 2.7: 50 mocks per set, no reduced fallback
        out["status"] = f"no label (exploration with {nmock} mocks per set; the label needs 50)"
        out["label"] = {"label": out["status"], "computed_label_not_used": ev["label"]}
        out["label_median_rule"] = {"label": out["status"], "computed_label_not_used": ev["label_median_rule"]}
    else:
        out["status"] = "evaluated"
    out["mocks"] = mock_info
    # companion data refits at each ladder f (reported; not decisive)
    comp = {v: {} for v in selaux.R1_VARIANTS}
    for f in [float(x) for x in P["err_f"]]:
        for v in selaux.R1_VARIANTS:
            comp[v][selaux.ffmt(f)] = []
            for b in bins:
                x = r1_data_refit(C, df, F, b, v, coefs[b], f)
                comp[v][selaux.ffmt(f)].append(x)
                ctx.log(f"R1-ERR companion refit f={f} {v} bin {b}: K={x['k']} d={x['d']:.3f}")
    out["companion_refits"] = comp
    out.update({"runtime_h": (time.time() - t_start) / 3600, "params": P})
    ctx.save("r1_err", out)
    return {"R1-ERR": out["label"]["label"], "status": out["status"]}


def err_cut(s, res):
    """README 2.7 feasibility rule for selaux.run_mock_sets: a generator failure in an S15 term E set cuts
    the ladder at its f (no further mock of any set at that f or a larger one); a failure in a term N or
    Full set does not cut."""
    if s["variant"] == "S15E" and res.get("gen_fail"):
        f0 = s["f"]
        return lambda s2: s2["f"] >= f0
    return None


# =============================================================================================
# R1-ERRCAL (README 2.8, T-059): calibration of R1 with the error scale f in the data and mock fits
# =============================================================================================
def r1_mock_errcal(C, D, kind, mech, rngs, pools, nstart, f):
    """One R1-ERRCAL mock (README 2.8): drawn by R1-ERR's generator with true errors f x e (kind null_sn or
    null_sp from the null fits at f in D, or power from R1-SEL-FIT's primary power model) and fitted WITH f
    (the m0 kernels at f) by R1-SEL-FIT's procedure: fit (o) from the data fit at f (D["_starts"]) plus
    2 perturbations on rngs[0], fit (i) from data-independent starts on rngs[1]. A RuntimeError of the
    generator is returned as gen_fail = True; an error of the fits is raised."""
    return mock_scaled(C, D, kind, mech, rngs, pools, nstart, f, f)


def errcal_rngs(seed, P, k, j):
    """README 2.8 streams of mock j of set k: catalogue and fit (o) from default_rng([seed, 59, k, j]), fit (i)
    from default_rng([seed, 159, k, j])."""
    return (selaux.mock_rng(seed, P["errcal_seed_tag"], k, j),
            np.random.default_rng([int(seed), int(P["errcal_seed_tag_indep"]), int(k), int(j)]))


def errcal_cut(s, res):
    """README 2.8 generator-failure rule for selaux.run_mock_sets: after a generator failure no further
    mock of that f and variant is run (the other f and the other variants are unaffected)."""
    if res.get("gen_fail"):
        f0, v0 = s["f"], s["variant"]
        return lambda s2: s2["f"] == f0 and s2["variant"] == v0
    return None


def errcal_data_check(x, rerr, P, b, tol=1e-9):
    """README 2.8 check (a): d and K of a data fit at f equal R1-ERR's companion refit (r1_err.json
    companion_refits.<variant>.<f>, matched by bin; absolute tol). A missing record counts as a mismatch."""
    tag = f"{x['variant']}_{b}@f={selaux.ffmt(x['f'])}"
    recs = (rerr.get("companion_refits") or {}).get(x["variant"], {}).get(selaux.ffmt(x["f"]), [])
    rr = next((r for r in recs if list(r["bin"]) == list(P["r1_bins"][b])), None)
    if rr is None:
        return [f"{tag}.missing"]
    bad = []
    if not abs(float(x["d"]) - float(rr["d"])) <= tol:
        bad.append(f"{tag}.d")
    if int(x["k"]) != int(rr["k"]):
        bad.append(f"{tag}.k")
    return bad


def errcal_evaluate(P, sets, results, times, dfit, rfit, pmodels):
    """README 2.8 decision rules and reported items from the mock results (k -> list of result dicts).
    dfit: (f, variant, bin) -> data fit at f (r1_data_refit with nulls, public fields); rfit: r1_selfit.json
    (the two metal-rich bins of the five-bin verdict); pmodels: (variant, bin) -> the primary power model
    (its 'valid' flag enters resolvability, as in R1-SEL-FIT). Pure: no fits, no files. Returns the
    r1_errcal.json body without the checks and run records."""
    nmock = int(P["errcal_n_mock"])
    bins, mechs = [int(b) for b in P["errcal_bins"]], list(P["mechs"])
    fs = [float(x) for x in P["errcal_f"]]
    kmax, qrank, nbins = int(P["kmax"]), int(P["sel_q_rank"]), len(P["r1_bins"])
    names = {b: bin_name(P, b) for b in range(nbins)}
    # ---- per set (reported)
    per_set = []
    for s in sets:
        rr = results.get(s["k"], [])
        ok = [r for r in rr if not r.get("gen_fail")]
        row = {**{k: s[k] for k in ("k", "f", "variant", "bin", "kind", "mech")}, "bin_name": names[s["bin"]],
               "n_run": len(rr), "complete": len(rr) == nmock, "gen_fail": sum(1 for r in rr if r.get("gen_fail")),
               "d": [r["d"] for r in rr], "valley": [r["valley"] for r in rr]}
        if ok:
            vt = [r["valley_t"] for r in ok if r["valley"] and r.get("valley_t") is not None]
            row.update({
                "frac_valley": sum(1 for r in ok if r["valley"]) / len(ok),
                "d_pct_5_50_80_95": _pct([r["d"] for r in ok], ERR_PCT_D),     # all mocks (d = 1 without a valley)
                "d_pct_5_50_80_95_valley_only": _pct([r["d"] for r in ok if r["valley"]], ERR_PCT_D),
                "k_chosen": {str(K): sum(1 for r in ok if r["k"] == K) for K in range(1, kmax + 1)},
                "i_used_by_k": {str(K): sum(1 for r in ok if r.get(f"i_used_k{K}")) for K in range(1, kmax + 1)},
                "i_used_k5": sum(1 for r in ok if r.get("i_used_k5") == 1),
                "nonmonotone": sum(1 for r in ok if (r.get("nonmonotone") or 0) > 0),
                "o_nonmonotone": sum(1 for r in ok if (r.get("o_nonmonotone") or 0) > 0),
                "median_valley_t_mocks": float(np.median(vt)) if vt else None,
                "mean_pass_rate": (float(np.mean([r["pass_rate"] for r in ok]))
                                   if s["variant"] != "Full" and all(r.get("pass_rate") is not None for r in ok)
                                   else None),
            })
        row["data_valley_t"] = dfit[(s["f"], s["variant"], s["bin"])].get("valley_t")
        row["dropped_by_redraw_limit"] = sum(int(r.get("dropped") or 0) for r in rr)
        tt = times.get(s["k"], [])
        row["mean_s_per_mock"] = float(np.mean(tt)) if tt else None
        per_set.append(row)
    ps = {r["k"]: r for r in per_set}
    by = {(s["f"], s["variant"], s["bin"], s["kind"], s["mech"]): s["k"] for s in sets}
    # ---- per variant and f
    variants = {}
    for v in selaux.R1_VARIANTS:
        rb = rfit["variants"][v]["bins"]
        per_f, verdicts = {}, {}
        for f in fs:
            ks = [by[(f, v, b, kind, m)] for b in bins for kind in selaux.R1_KINDS for m in mechs]
            nfail = sum(ps[k]["gen_fail"] for k in ks)
            if nfail:                                  # README 2.8: the generator failed in this f and variant
                per_f[selaux.ffmt(f)] = {"status": selaux.ERRCAL_GENERATOR, "gen_fail": nfail,
                                         "verdict": selaux.ERRCAL_GENERATOR}
                verdicts[f] = selaux.ERRCAL_GENERATOR
                continue
            for k in ks:                               # without a failure every set has all its mocks
                if not ps[k]["complete"]:
                    raise RuntimeError(f"R1-ERRCAL set k={k} (f={f}, {v}) has {ps[k]['n_run']} of {nmock} mocks")
            if any(selaux.nonfinite({fld: r.get(fld) for fld in USED_FIELDS}) for k in ks for r in results[k]):
                per_f[selaux.ffmt(f)] = {"status": selaux.ERRCAL_NONFINITE, "gen_fail": 0,
                                         "verdict": selaux.ERRCAL_NONFINITE}
                verdicts[f] = selaux.ERRCAL_NONFINITE
                continue
            brows, r1bins = [], []
            for b in range(nbins):
                if b not in bins:                      # metal-rich bins: R1-SEL-FIT's record, never almost disjoint
                    B = rb[b]
                    r1bins.append({"bin": list(P["r1_bins"][b]), "bin_name": names[b], "source": "r1_selfit.json",
                                   "resolvable": bool(B["resolvable"]), "almost_disjoint": False,
                                   "edge": B.get("edge"), "d": B.get("d")})
                    continue
                D_ = dfit[(f, v, b)]
                shape = {"d": D_["d"], "valley": D_["valley"], "edge": D_.get("edge"), "t": D_.get("valley_t")}
                res = {(kind, m): results[by[(f, v, b, kind, m)]] for kind in selaux.R1_KINDS for m in mechs}
                dec = r1_decide(P, {"shape": shape}, res, nmock, qrank=qrank)
                pm = pmodels[(v, b)]
                dec["resolvable_by_power"] = dec["resolvable"]
                dec["power_model_invalid"] = not pm["valid"]
                dec["resolvable"] = bool(dec["resolvable"] and pm["valid"])
                dec.update({"bin": D_["bin"], "bin_name": names[b], "source": "R1-ERRCAL", "k": D_["k"],
                            "valley": D_["valley"], "n": D_["n"],
                            "sets": {f"{kind}_{m}": by[(f, v, b, kind, m)] for kind in selaux.R1_KINDS for m in mechs}})
                for kind in selaux.R1_KINDS:           # q_s and the pass fraction at d* in the per-set rows
                    for m in mechs:
                        row = ps[by[(f, v, b, kind, m)]]
                        row["d_star"] = dec["d_star"]
                        if kind == "power":
                            row["power_at_d_star"] = dec["power"][m]
                        else:
                            row["q_s"] = dec["q"][f"{kind}_{m}"]
                            row["fpr_at_d_star"] = dec["fpr"][f"{kind}_{m}"]
                brows.append(dec)
                r1bins.append(dec)
            verdict, med = selaux.r1_verdict(r1bins, P["min_bins"], P["edge_range"])
            verdicts[f] = verdict
            per_f[selaux.ffmt(f)] = {
                "status": "evaluated", "verdict": verdict, "median_edge": med,
                "n_resolvable": sum(1 for x in r1bins if x["resolvable"]),
                "n_almost_disjoint": sum(1 for x in r1bins if x["resolvable"] and x["almost_disjoint"]),
                "bins": brows, "metal_rich_from_r1_selfit": [x for x in r1bins if x.get("source") == "r1_selfit.json"]}
        variants[v] = {"per_f": per_f, "verdicts": {selaux.ffmt(f): verdicts[f] for f in fs},
                       "label": selaux.errcal_label(fs, verdicts)}
    return {"f": fs, "bins": bins, "bin_names": [names[b] for b in bins], "d_cap": float(P["d_cap"]),
            "variants": variants, "per_set": per_set, "label": variants["S15E"]["label"],
            "labels": {v: variants[v]["label"] for v in selaux.R1_VARIANTS}}


def main_errcal(ctx, P, store_root=None, recorded=None, recorded_fit=None, recorded_err=None):
    """R1-ERRCAL (README 2.8, T-059). Writes r1_errcal.json; r1_sel.json, r1_selfit.json and r1_err.json are
    read, never written."""

    t_start = time.time()
    if hasattr(ctx, "record_suffix"):
        ctx.record_suffix = "_errcal"            # provenance_errcal.json, run_info_errcal.json
    C = Ctx(P)
    df = load(ctx, P)
    F = flags(df, P)
    A_all, E_all = df["age"].to_numpy(), df["eage"].to_numpy()
    feh = df["feh"].to_numpy()
    assert len(df) == P["n_rows"], f"row count {len(df)} != {P['n_rows']}"
    with np.errstate(divide="ignore", invalid="ignore"):
        rel_all = E_all / A_all
    F = dict(F, s15=F["s15"] & (A_all > 0))       # S15 samples without Age <= 0 (README 2.5 SEL-0, as R1-ERR)
    bins = [int(b) for b in P["errcal_bins"]]
    fs = [float(x) for x in P["errcal_f"]]
    nmock = int(P["errcal_n_mock"])
    nstart = int(P["selfit_nstart"])
    seed = int(P["seed"])

    def load_res(name):
        return json.loads((HERE / "results" / f"{name}.json").read_text(encoding="utf-8"))
    rec = recorded if recorded is not None else load_res("r1_sel")
    rfit = recorded_fit if recorded_fit is not None else load_res("r1_selfit")
    rerr = recorded_err if recorded_err is not None else load_res("r1_err")
    # pass tables and pools of the R1-ERRCAL bins (as main_err)
    pools, coefs = {}, {}
    for b in bins:
        lo, hi = P["r1_bins"][b]
        mask = F["valid"] & (feh >= lo) & (feh < hi)
        tab = _pass_table(P, A_all[mask], rel_all[mask], None, 1)
        coefs[b] = m0.pass_coefs(tab)
        pools[b] = _pools(tab, rel_all[mask])
    # data fits at f (mixtures as R1-ERR's companion refits, then the null fits with f); check (a)
    r1d, dfit, pmodels, mism = {}, {}, {}, []
    for f in fs:
        for v in selaux.R1_VARIANTS:
            for b in bins:
                recd = rec["data_fits"][f"{v}_{b}"]
                x = r1_data_refit(C, df, F, b, v, coefs[b], f, nulls=True)
                if x["n"] != recd["n"]:
                    raise RuntimeError(f"R1-ERRCAL data bin {v} {b}: n = {x['n']} differs from r1_sel.json ({recd['n']})")
                pm = recd["power_models"]["primary"]          # R1-SEL-FIT's primary power model, floor 0.12
                pmodels[(v, b)] = pm
                r1d[(f, v, b)] = {"variant": v, "_n": x["n"], "_starts": x["_starts"], "skewnorm": x["skewnorm"],
                                  "splitnorm": x["splitnorm"], "power_models": {"primary": pm}}
                dfit[(f, v, b)] = _clean(x)
                mism += errcal_data_check(x, rerr, P, b)
                ctx.log(f"R1-ERRCAL data f={f} {v} bin {b}: K={x['k']} d={x['d']:.3f} "
                        f"skewnorm={x['skewnorm']} splitnorm={x['splitnorm']}")
    out = {"status": None, "n_mock": nmock,
           "seed_tags": [int(P["errcal_seed_tag"]), int(P["errcal_seed_tag_indep"])],
           "checks": {"data_fit_mismatches": mism},
           "threads": {**{k: os.environ.get(k) for k in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS")},
                       "cpu_count": os.cpu_count(),
                       "note": "environment variables of the last session (null: the libraries chose their own "
                               "thread counts); every session of a run must use the same settings"},
           "data_fits": {selaux.ffmt(f): {v: [dfit[(f, v, b)] for b in bins] for v in selaux.R1_VARIANTS} for f in fs},
           "power_models": {v: [pmodels[(v, b)] for b in bins] for v in selaux.R1_VARIANTS}}
    if mism:
        out["status"] = "not evaluable (reproduction): data fits at f differ from r1_err.json companion_refits"
        out["label"] = selaux.errcal_label(fs, {}, reproduction_ok=False)
        out["labels"] = {v: out["label"] for v in selaux.R1_VARIANTS}
        out.update({"runtime_h": (time.time() - t_start) / 3600, "params": P})
        ctx.save("r1_errcal", out)
        return {"R1-ERRCAL": out["label"], "status": out["status"]}
    sets = selaux.errcal_sets(fs, bins, P["mechs"])
    root = _store_root(ctx, store_root, "s010_errcal_mocks")
    store = selaux.MockStore(root, _sel_key(P, df), name="R1-ERRCAL", rule="README 2.8")
    ctx.log(f"R1-ERRCAL checkpoints: {store.dir} ({'resumed with consent' if store.resumed else 'new or continued'})")
    # README 2.8 amendment 11 (gate 1): the mock inputs (the 18 data and null fits at f) are fixed by the first
    # session; a later session must reproduce them exactly, else it stops before any mock
    side = Path(store.dir) / "errcal_data_fits.json"
    cur = json.dumps(out["data_fits"], sort_keys=True)
    if side.exists():
        if side.read_text(encoding="utf-8") != cur:
            store.release()
            raise RuntimeError("R1-ERRCAL refused: the data and null fits at f differ from the first session's "
                               "(the same thread settings are required in every session, README 2.8 amendment 11)")
    else:
        side.write_text(cur, encoding="utf-8")

    def run_one(s, rngs):
        return r1_mock_errcal(C, r1d[(s["f"], s["variant"], s["bin"])], s["kind"], s["mech"], rngs,
                              pools[s["bin"]], nstart, s["f"])

    def make_rng(k, j):
        return errcal_rngs(seed, P, k, j)
    try:                                           # the lock is released on every path; checkpoints stay
        results, state, proj_log = selaux.run_mock_sets(sets, nmock, store, run_one, make_rng, P["errcal_stop_h"],
                                                        ctx.log, cut=errcal_cut, name="R1-ERRCAL", rule="README 2.8")
        mock_info = {"n_sets": len(sets), "projections": proj_log, "elapsed_h_total": store.elapsed_s() / 3600,
                     "resumed": store.resumed, "resumes": store.resumes(),
                     "stop_limit_h": store.limit_h if store.limit_h is not None else P["errcal_stop_h"]}
    finally:
        store.release()
    ev = errcal_evaluate(P, sets, results, {k: st["times"] for k, st in state.items()}, dfit, rfit, pmodels)
    out.update(ev)
    if nmock != 50:                                # as 2.6 and 2.7: labels need 50 mocks in every set
        out["status"] = f"no label (exploration with {nmock} mocks per set; the label needs 50)"
        out["computed_labels_not_used"] = ev["labels"]
        out["label"] = out["status"]
        out["labels"] = {v: out["status"] for v in selaux.R1_VARIANTS}
    else:
        out["status"] = "evaluated"
    out["mocks"] = mock_info
    out.update({"runtime_h": (time.time() - t_start) / 3600, "params": P})
    ctx.save("r1_errcal", out)
    return {"R1-ERRCAL": out["label"], "S15N": out["labels"]["S15N"], "Full": out["labels"]["Full"],
            "status": out["status"]}
