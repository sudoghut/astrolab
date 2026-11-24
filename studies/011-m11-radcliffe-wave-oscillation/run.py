"""M11 Radcliffe Wave: is the young-cluster wave oscillating?

Implements the pre-registration of README sections 1-4 (T1-T8, overall reading).

Run with:      python -m astrolab run 011-m11-radcliffe-wave-oscillation
Explore with:  python -m astrolab explore 011-m11-radcliffe-wave-oscillation --tag <topic> --set KEY=VALUE

The formal run takes many hours on one core (README 4.7). It writes checkpoints outside the project
folder (astrolab cache dir / PARAMS["checkpoint_subdir"] / <key>), so an interrupted or paused run
(PARAMS["stop_after_hours"]) continues where it stopped when it is started again with the same PARAMS
and code. Results are written only when every requested part has finished.

The post-hoc parts of README 4.10 (T-056) run alone: PARAMS["parts"] = ["conv"] (R-CONV) or ["t8p"] (T8-P)
write rconv.json / t8p.json and only the R_CONV / T8_P keys of summary.json (main_standalone). So does README
4.11's R-DIAG (T-061): PARAMS["parts"] = ["diag"] writes rdiag.json and the R_DIAG key.
"""
import hashlib
import json
import re
import math
import time
import zlib
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar

import diag011 as D
import fit011 as F
import stats011 as S
import wave011 as W

CLUSTERS_URL = "https://dataverse.harvard.edu/api/access/datafile/7211931"
CLOUDS_URL = "https://dataverse.harvard.edu/api/access/datafile/7211929"
# README 4.11 (R-DIAG only): Zucker et al. 2020 Table A.1, Alves et al. 2020 bridging sightlines, K24's curve
HANDBOOK_URL = "https://dataverse.harvard.edu/api/access/datafile/4361456"
BRIDGING_URL = "https://dataverse.harvard.edu/api/access/datafile/4361453"
BESTFIT_URL = "https://dataverse.harvard.edu/api/access/datafile/8954305"
HERE = Path(__file__).resolve().parent

# Tunable knobs (AGENTS.md section 2). Read them inside main() at call time, never into
# module-level constants, and pass values to helper modules as arguments (a helper that does
# `import run` gets a fresh copy without the override): `astrolab explore --set` overrides
# this dict in memory. The defaults are the pre-registered values (README sections 2-4); changing
# one in the committed file is a change to the pre-registration.
PARAMS = {
    "seed": 20261121,
    # model (README 4.1)
    "sigma_pc": 47.0,
    "bandwidth_pc": 100.0,
    "grid_n": 2000,
    "u_min": -0.2,
    "u_max": 1.4,
    # sampler and optimiser (README 4.2)
    "mcmc_walkers": 48,
    "mcmc_steps": 6000,
    "mcmc_burn": 2000,
    "mcmc_min_tau_mult": 50.0,
    "mcmc_chunk": 250,
    "mcmc_thin_keep": 10,
    "ml_starts": 20,
    "ml_nm_maxfev": 6000,
    "ml_lbfgs_maxfun": 3000,
    # T3 / T4 (README 4.3)
    "t3_mocks": 100,
    "t3_resid_variant": True,
    "t3_strong": 0.001,
    "alpha": 0.05,
    "t4_mocks": 1000,
    "t4_p_excl": 0.01,
    "t4_p_not": 0.05,
    "t4_power_min": 0.8,
    # T5 (README 4.4)
    "t5_boot": 1000,
    "t5_ka_mocks": 20,
    "t5_ka_B": [0.5, 0.84, 1.0],
    "t5_ka_w0t": -0.38,
    "t5_b_t": 0.4,
    "t5_band": [0.8, 1.25],
    "t5_k_min": 0.3,
    "t5_k_max": 3.0,
    "t5_k_step": 0.01,
    "t5_cut_sigma": 1.7320508075688772,       # sqrt(3) x 47 pc
    "t5_omega0_sens_kms_kpc": 68.0,
    # T6 (README 4.6)
    "variants": ["v1_outlier_3sigma", "v2_no_outlier_model", "v3_no_weights", "v4_bandwidth_50",
                 "v5_bandwidth_200", "v6_wsun_7p25", "v7_no_orion", "v8_leave_out_reference",
                 "v9_low_sigmavz", "v10_chord_u1"],
    "v4_bandwidth_pc": 50.0,
    "v5_bandwidth_pc": 200.0,
    "v1_cut_sigma": 3.0,
    "v6_dvz_kms": -0.55,
    "v7_orion_l_deg": [180.0, 220.0],
    "v7_orion_b_deg": [-25.0, -5.0],
    # T7 (README 4.5)
    "t7_vc_kms": 242.0,
    "t7_margin": 9.0,
    # T8 (README section 2)
    "t8_broad_omega0_kms_kpc": [30.0, 150.0],
    "t8_broad_mu0_kpc": [0.3, 3.0],
    "t8_broad_r0_pc": [1000.0, 10000.0],
    "t8_prior_sigma_ln_omega0": 0.17,
    "t8_width_frac": 0.5,
    "t8_shift_max": 0.5,
    "t8_divisor_variant_kms_kpc": 74.0,
    "t8_draws": 2000,
    "sun_vz_kms": 7.8,
    # R-CONV and T8-P (README 4.10, T-056, post hoc); run alone with parts ["conv"] or ["t8p"]
    "conv_indices": list(range(16)),          # the 16 conventions (index = baseline*4 + sigma*2 + weights)
    "conv_seed_offset": 3000,                 # column-(3) chain of convention i: seed (seed, 3000 + i)
    "conv_min_count": 3,
    "conv_repro_count": 5,
    "conv_width_range": [0.6666666666666666, 1.5],
    "t8p_bound_frac": 0.05,                   # broad-prior median within 5% of a bound -> at the bound
    # R-DIAG (README 4.11, T-061, post hoc); run alone with parts ["diag"]
    "rdiag_member_k": 3.0,                    # Part B tolerance t = k max(spread, floor) per axis
    "rdiag_member_floor_pc": 5.0,             # ... and the gate on the mean: max(spread, floor)
    "rdiag_pt_names": ["Perseus", "Taurus"],  # S+PT adds all sightlines of these Zucker names
    "rdiag_s_all_n": 169,                     # the run stops unless S_all has 169 points
    "rdiag_pt_n": 28,                         # ... and S+PT has 28 more than S
    "rdiag_map_prior_draws": 19,              # Part A MAP: v_K, v_P and 19 prior draws (21 starts)
    "rdiag_top_n": 10,                        # Part A: the ten largest Delta_i
    "rdiag_c_prior_pc": [-400.0, 400.0],      # Part D (c): c ~ U(-400, 400) pc; also Part C (ii)'s bound on c
    "rdiag_c_scale_pc": 100.0,                # c's walker-ball and simplex scale
    "rdiag_cref_s0_prior_pc": [-1000.0, 3000.0],   # c-ref: s0 flat
    "rdiag_c_halfwidth_max_pc": 100.0,        # c data-driven if c-ref's 16-84% half-width <= 100 pc
    "rdiag_zsun_pc": 20.8,                    # Part D (z_sun): every cloud's z + 20.8 pc
    "rdiag_d6_max": 8.781,                    # reading: D6 <= 9.781 - 1 (formal L-F-W, rconv.json convention 0)
    "rdiag_m6_max": 3.192,                    # ... and M6 <= 3.692 - 0.5
    "rdiag_curve_match_median_pc": 5.0,       # Part C label: "matches" if median <= 5 and p95 <= 15 pc
    "rdiag_curve_match_p95_pc": 15.0,
    "rdiag_curve_approx_median_pc": 20.0,     # "approximately matches" if median <= 20 pc
    "rdiag_curve_excl_frac": 0.10,            # suffix when more than 10% of the points are excluded in x-y
    # load check (README 3)
    "load_check_max_abs_vz": 3.0,
    # running ("conv", "t8p" and "diag" are standalone parts, README 4.10, 4.11 and section 8)
    "parts": ["t1t2", "t3", "t4", "t5", "t6", "t7", "t8"],
    "timing_evals": 100,
    "stop_after_hours": 10.0,                 # pause (checkpointed) after this long; 0 = no limit
    "checkpoint_subdir": "s011_checkpoints",
}

# keys that do not change any result (excluded from the checkpoint key)
_RUN_ONLY = ("stop_after_hours", "timing_evals", "parts", "checkpoint_subdir")
SHAPE = W.SHAPE_NAMES
T1_KEYS = ("A", "p", "delta", "s0", "gamma", "phi")
ANCHORS = ("x0", "y0", "x1", "y1", "x2", "y2")


def rng_for(seed, name):
    return np.random.default_rng([int(seed) % (2 ** 32), zlib.crc32(name.encode())])


# =============================================================================================
# Data

def load_tables(ctx):
    pc = ctx.http(CLUSTERS_URL, label="K24 young-cluster table (Dataverse doi:10.7910/DVN/XSCB9N, file 7211931)")
    po = ctx.http(CLOUDS_URL, label="K24 12CO cloud table (Dataverse doi:10.7910/DVN/Q7F4PC, file 7211929)")
    cl = pd.read_csv(pc, sep="\t")
    co = pd.read_csv(po, sep="\t")
    shas = [hashlib.sha256(Path(pc).read_bytes()).hexdigest(), hashlib.sha256(Path(po).read_bytes()).hexdigest()]
    return cl, co, shas


def check_columns(cl, co):
    need_cl = ["name", "reference", "x", "sigmax", "y", "sigmay", "z", "sigmaz", "vx", "sigmavx", "vy",
               "sigmavy", "vz", "sigmavz", "age", "inlier"]
    need_co = ["name", "x", "y", "z", "l", "b", "d", "vr", "vr16", "vr84"]
    miss = [c for c in need_cl if c not in cl.columns] + [c for c in need_co if c not in co.columns]
    if miss:
        raise ValueError(f"missing columns: {miss}")


def make_data(cl, co, vz_shift=0.0):
    return W.Data(cx=cl["x"].to_numpy(float), cy=cl["y"].to_numpy(float), cz=cl["z"].to_numpy(float),
                  cvz=cl["vz"].to_numpy(float) + vz_shift,
                  csig=cl[["sigmax", "sigmay", "sigmaz", "sigmavz"]].to_numpy(float),
                  ox=co["x"].to_numpy(float), oy=co["y"].to_numpy(float), oz=co["z"].to_numpy(float))


def load_check(vz, weights, max_abs):
    """README 3: |weighted mean v_z| < 3 km/s. Weighted = the fixed kernel weights of the likelihood
    (inverse-variance weights are undefined: some sigmavz are 0.0 in the table)."""
    vz = np.asarray(vz, float)
    wmean = float(np.sum(weights * vz) / np.sum(weights))
    return {"weighted_mean_vz": wmean, "unweighted_mean_vz": float(np.mean(vz)),
            "weights": "kernel weights of README 4.1 (K24 column-(6) medians, bandwidth from PARAMS)",
            "threshold": max_abs, "passed": bool(abs(wmean) < max_abs)}


def galactic_lb(x, y, z):
    l = np.degrees(np.arctan2(y, x)) % 360.0
    b = np.degrees(np.arctan2(z, np.hypot(x, y)))
    return l, b


# =============================================================================================
# Setups

def setups(P, outlier="k24", u1_mode="half"):
    sig = P["sigma_pc"]
    broad = {"omega0": tuple(v / 1000.0 for v in P["t8_broad_omega0_kms_kpc"]),
             "mu0_kpc": tuple(P["t8_broad_mu0_kpc"]), "r0": tuple(P["t8_broad_r0_pc"])}
    common = dict(sigma=sig, outlier=outlier, u1_mode=u1_mode)
    return {
        "col3": W.Setup(free=SHAPE, clusters=False, clouds=True, **common),
        "col4": W.Setup(free=SHAPE, **common),
        "col5": W.Setup(free=SHAPE + ("w0t", "B"), **common),
        "b05": W.Setup(free=SHAPE + ("w0t",), fixed={"B": 0.5}, **common),
        "col6": W.Setup(free=SHAPE, clouds=True, **common),
        "t7c": W.Setup(free=SHAPE + ("w0t",), fixed={"B": 0.5}, clouds=True, **common),
        "col7": W.Setup(free=SHAPE + ("ln_omega0", "ln_mu0", "r0"), clouds=True, divisor=None, prior="k24",
                        **common),
        "col7_broad": W.Setup(free=SHAPE + ("ln_omega0", "ln_mu0", "r0"), clouds=True, divisor=None,
                              prior="broad", broad=broad, **common),
        "col7_div": W.Setup(free=SHAPE + ("ln_omega0", "ln_mu0", "r0"), clouds=True,
                            divisor=P["t8_divisor_variant_kms_kpc"] / 1000.0, prior="k24", **common),
        # T8-P (README 4.10 Part B): the divisor fixed at 74 under the broad priors
        "col7_div_broad": W.Setup(free=SHAPE + ("ln_omega0", "ln_mu0", "r0"), clouds=True,
                                  divisor=P["t8_divisor_variant_kms_kpc"] / 1000.0, prior="broad", broad=broad,
                                  **common),
    }


def models_for(P, data, grid, bandwidth, outlier="k24", u1_mode="half"):
    wc, wo = W.fixed_weights(data, grid, bandwidth, u1_mode)
    st = setups(P, outlier, u1_mode)
    return {k: W.Model(s, data, grid, wc, wo) for k, s in st.items()}, wc, wo


# =============================================================================================
# Timing (logged early, README 4.7)

def timing_estimate(P, models, data, grid, ctx):
    n = max(int(P["timing_evals"]), 5)
    t = {}
    for key in ("col3", "col4", "col6"):
        m = models[key]
        th = m.theta_of(W.k24_vector(6))
        m.loglike(th)
        t0 = time.perf_counter()
        for _ in range(n):
            m.loglike(th)
        t[key] = (time.perf_counter() - t0) / n
    cur = F.t5_curve(W.k24_vector(3), grid)
    syn = F.synthetic_clusters(grid, data.n_clusters, rng_for(P["seed"], "timing"), sigma=P["sigma_pc"])
    t0 = time.perf_counter()
    for _ in range(20):           # synthetic clusters: nothing is fitted to the data here
        F.t5_analyse(cur, syn.cx, syn.cy, syn.cz, syn.cvz, syn.csig, cut=P["t5_cut_sigma"] * P["sigma_pc"],
                     bandwidth=P["bandwidth_pc"], sigma=P["sigma_pc"])
    t5 = (time.perf_counter() - t0) / 20
    mc = P["mcmc_walkers"] * P["mcmc_steps"]
    start_ml = P["ml_nm_maxfev"] + 0.5 * P["ml_lbfgs_maxfun"]   # NM budget plus a typical L-BFGS-B polish
    ml = P["ml_starts"] * start_ml
    sec = {
        "mcmc": mc * (t["col3"] + 2 * t["col4"] + 4 * t["col6"]),
        "ml_main": ml * (3 * t["col4"] + 2 * t["col6"]) + 5 * start_ml * t["col4"],
        "t3_mocks": P["t3_mocks"] * 2 * (2 + 4) * start_ml * t["col4"] * (2 if P["t3_resid_variant"] else 1),
        "t4": 3 * P["t4_mocks"] * 0.002 * 2,
        "t5": (P["t5_boot"] * 2 + len(P["t5_ka_B"]) * P["t5_ka_mocks"] * (P["t5_boot"] + 1)) * t5,
    }
    nv = len(variant_list(P, None))
    sec["t6"] = (nv * (3 * ml * t["col4"] + 2 * P["t4_mocks"] * 0.002 + P["t5_boot"] * t5)
                 + 2 * P["t3_mocks"] * 2 * 6 * start_ml * t["col4"] + mc * t["col3"])
    tot = sum(sec.values())
    out = {"seconds_per_loglike": {k: round(v * 1e3, 3) for k, v in t.items()}, "unit": "ms",
           "seconds_per_t5_analysis_ms": round(t5 * 1e3, 3),
           "projected_hours": {k: round(v / 3600, 2) for k, v in sec.items()},
           "projected_total_hours": round(tot / 3600, 2),
           "note": "MCMC at the pre-registered length (reruns with doubled steps not included); ML fits "
                   "at the full Nelder-Mead budget per start (upper end)"}
    ctx.log(f"timing: loglike {out['seconds_per_loglike']} ms; T5 analysis {out['seconds_per_t5_analysis_ms']} ms; "
            f"projected {out['projected_total_hours']} h ({out['projected_hours']})")
    return out


# =============================================================================================
# Fits

def mcmc(P, store, name, model, center_vec, ctx, seed_int=None):
    ctx.log(f"MCMC {name} ({len(model.setup.free)} parameters)")
    if seed_int is None:
        seed_int = int(rng_for(P["seed"], "mcmc_" + name).integers(2 ** 31))
    return F.run_mcmc(model, center_vec, seed=seed_int,
                      n_walkers=P["mcmc_walkers"], n_steps=P["mcmc_steps"], n_burn=P["mcmc_burn"], store=store,
                      name="mcmc_" + name, chunk=P["mcmc_chunk"], log=ctx.log,
                      min_tau_mult=P["mcmc_min_tau_mult"], thin_keep=P["mcmc_thin_keep"])


def ml(P, store, name, model, first_starts, ctx, extra_starts=()):
    """Best of ml_starts starts: the given first start(s) plus prior draws (README 4.2)."""
    def go():
        rng = rng_for(P["seed"], "ml_" + name)
        starts = [np.asarray(s, float) for s in first_starts]
        while len(starts) < P["ml_starts"]:
            starts.append(model.prior_draw(rng))
        starts += [np.asarray(s, float) for s in extra_starts]
        t0 = time.time()
        r = F.ml_fit(model, starts, nm_maxfev=P["ml_nm_maxfev"], lbfgs_maxfun=P["ml_lbfgs_maxfun"])
        ctx.log(f"ML {name}: lnL = {r['lnL']:.3f} ({len(starts)} starts, {time.time() - t0:.0f} s)")
        return r
    return store.cached("ml_" + name, go)


def chain_summary(model, res, names):
    sam = res["samples"]
    out = {}
    for n in names:
        if n in ("delta", "gamma"):
            x = np.exp(sam[:, model.setup.free.index("ln_" + n)])
        elif n == "omega0":
            x = 1000.0 * np.exp(sam[:, model.setup.free.index("ln_omega0")])
        elif n == "mu0_kpc":
            x = np.exp(sam[:, model.setup.free.index("ln_mu0")])
        else:
            x = sam[:, model.setup.free.index(n)]
        out[n] = S.percentiles(x)
    return out


def chain_meta(res):
    return {k: res[k] for k in ("n_walkers", "n_steps", "n_burn", "acceptance", "tau_max", "long_enough",
                                "rerun", "chain_short")} | {"tau": [round(t, 1) for t in res["tau"]],
                                                            "free": res["free"]}


def inlier_overlap(a, b):
    a, b = np.asarray(a, bool), np.asarray(b, bool)
    return {"both": int(np.sum(a & b)), "first_only": int(np.sum(a & ~b)), "second_only": int(np.sum(~a & b)),
            "neither": int(np.sum(~a & ~b)), "n_first": int(a.sum()), "n_second": int(b.sum())}


# =============================================================================================
# T1 / T2

def t1_column(model, res, col):
    k24 = W.K24_TABLE2[col]
    summ = chain_summary(model, res, T1_KEYS + ANCHORS)
    rows, n_in = {}, 0
    for n in T1_KEYS + ANCHORS:
        med, plus, minus = k24[n]
        ours = summ[n]["median"]
        inside = (med - minus) <= ours <= (med + plus)
        d = ours - med
        sig = (d / plus) if d > 0 else (d / minus if minus > 0 else float("nan"))
        rows[n] = {"ours": summ[n], "k24": {"median": med, "plus": plus, "minus": minus},
                   "inside_k24_1sigma": bool(inside), "sigma_scaled_difference": sig}
        if n in T1_KEYS and inside:
            n_in += 1
    return {"parameters": rows, "n_inside_of_6": n_in, "label": S.t1_label(n_in)}


def model_curve_for_plot(model, v, n=240):
    wv = W.wave_on_grid(v, model.grid, model.setup.u1_mode)
    vi = np.flatnonzero(wv["valid"])
    pick = vi[np.linspace(0, len(vi) - 1, min(n, len(vi))).astype(int)]
    return {"s": np.round(wv["s"][pick], 1).tolist(), "z": np.round(wv["z"][pick], 2).tolist(),
            "vz": np.round(wv["vz"][pick], 3).tolist(), "x": np.round(wv["x"][pick], 1).tolist(),
            "y": np.round(wv["y"][pick], 1).tolist()}


def points_for_plot(model, v, cl):
    ev = model.evaluate(v)
    s = ev["wave"]["s"][ev["cl_idx"]]
    return {"name": cl["name"].astype(str).tolist(), "s": np.round(s, 1).tolist(),
            "z": cl["z"].round(1).tolist(), "vz": cl["vz"].round(2).tolist(),
            "sigmavz": cl["sigmavz"].round(2).tolist(),
            "inlier": (~ev["cl_outlier"]).astype(int).tolist(), "table_inlier": cl["inlier"].astype(int).tolist()}


# =============================================================================================
# T3

def t3_ml_three(P, store, prefix, mods, starts, ctx, extra_free_starts=True):
    """B = 1 (omega0 t = 0), B = 0.5 profile, and the B-free maximum on one data set."""
    f1 = ml(P, store, prefix + "b1", mods["col4"], starts["b1"], ctx)
    f05 = ml(P, store, prefix + "b05", mods["b05"], starts["b05"], ctx)
    extra = []
    if extra_free_starts:     # nesting: the B-free search also starts from both null optima
        extra = [F.to_model(mods["col4"], mods["col5"], f1["theta"]), F.to_model(mods["b05"], mods["col5"], f05["theta"])]
    ff = ml(P, store, prefix + "free", mods["col5"], starts["free"], ctx, extra_starts=extra)
    return {"b1": f1, "b05": f05, "free": ff}


def t3_mocks(P, store, prefix, null_model, null_fit, free_model, free_fit, data, noise, ctx):
    vals, clipped = [], 0
    resid = None
    if noise == "resid":
        ev = null_model.evaluate(null_fit["vector"])
        resid = ev["cl_res"][np.asarray(null_fit["inlier"], bool)]
    for i in range(P["t3_mocks"]):
        name = f"{prefix}{noise}_{i}"

        def one(i=i, name=name):
            rng = rng_for(P["seed"], name)
            x, y, z, vz = F.mock_vectors(null_model, null_fit["vector"], data, null_fit["inlier"], rng,
                                         noise=noise, sigma=P["sigma_pc"], resid=resid)
            dm = data.with_clusters(x, y, z, vz)
            mn, mf = null_model.clone(data=dm), free_model.clone(data=dm)
            gen_free = F.to_model(null_model, mf, null_fit["theta"])
            # null refit: the generating parameters (= the data's best null fit) and one prior draw
            rn = F.ml_fit(mn, [null_fit["theta"], mn.prior_draw(rng)], nm_maxfev=P["ml_nm_maxfev"], lbfgs_maxfun=P["ml_lbfgs_maxfun"], with_map=False)
            rf = F.ml_fit(mf, [gen_free, free_fit["theta"], mf.prior_draw(rng), F.to_model(mn, mf, rn["theta"])],
                          nm_maxfev=P["ml_nm_maxfev"], lbfgs_maxfun=P["ml_lbfgs_maxfun"], with_map=False)
            return 2.0 * (rf["lnL"] - rn["lnL"])
        v = store.cached(name, one)
        if v < 0:
            clipped += 1
            v = 0.0
        vals.append(v)
        if (i + 1) % 20 == 0:
            ctx.log(f"T3 mocks {prefix}{noise}: {i + 1}/{P['t3_mocks']}")
    return np.array(vals), clipped


def t3_stat(obs, mocks, d, P):
    pb, k = S.p_boot_ge(obs, mocks)
    cal = S.calibrated_p(obs, mocks, d)
    pr = S.p_raw(obs, d)
    return {"two_dlnL": obs, "d": d, "p_raw": pr, "p_boot": pb, "k_mocks_at_least_obs": k,
            "p_boot_mcse": S.p_mcse(pb, len(mocks)), **cal,
            "mocks_two_dlnL": np.asarray(mocks, float).tolist()}


def t3_labels(st_s, st_t, P):
    return {
        "standing": S.t3_standing_label(st_s.get("p_cal"), st_s["p_raw"], st_s["p_boot"],
                                        st_s["k_mocks_at_least_obs"], strong=P["t3_strong"], alpha=P["alpha"]),
        "pure_travelling": S.t3_travel_label(st_t.get("p_cal"), st_t["p_boot"], alpha=P["alpha"]),
    }


def t3_reduced(obs_s, obs_t, factor_s, factor_t, P):
    pc_s, pc_t = S.p_with_factor(obs_s, factor_s, 1), S.p_with_factor(obs_t, factor_t, 2)
    pr_s, pr_t = S.p_raw(obs_s, 1), S.p_raw(obs_t, 2)
    return {"p_cal_standing": pc_s, "p_raw_standing": pr_s, "p_cal_travelling": pc_t, "p_raw_travelling": pr_t,
            "standing": S.t3_standing_label_reduced(pc_s, pr_s, strong=P["t3_strong"], alpha=P["alpha"]),
            "pure_travelling": S.t3_travel_label_reduced(pc_t, alpha=P["alpha"])}


def fit_record(model, f):
    rec = {"lnL": f["lnL"], "parameters": W.physical(f["vector"]), "free": list(model.setup.free),
           "start_lnL": [round(x, 4) for x in f["start_values"]], "n_eval": f["n_eval"]}
    if "map_vector" in f:
        rec["map_parameters"] = W.physical(f["map_vector"])
        rec["map_logpost"] = f["map_logpost"]
    if f.get("inlier") is not None:
        rec["n_inliers"] = int(np.sum(f["inlier"]))
    return rec


# =============================================================================================
# T4

def gen_inliers(model, fit, fallback):
    """Inliers of a generating fit; with no outlier model (variant 2) every cluster, or `fallback`."""
    if model.setup.outlier == "gauss" or fit.get("inlier") is None:
        n = model.data.n_clusters
        return np.ones(n, bool) if fallback is None else np.asarray(fallback, bool)
    return np.asarray(fit["inlier"], bool)


def t4_run(P, store, prefix, mods, fits, data, idx_mask, ctx, with_free_power=True, with_resid=True,
           keep_arrays=False):
    """R over the B = 0.5 fit's inliers; standing mocks from the B = 0.5 fit, power mocks from the
    B = 1 (and B-free) fit; closest points recomputed on the B = 0.5 curve (README 4.3)."""
    idx = np.flatnonzero(idx_mask)
    m05 = mods["b05"]
    v05 = fits["b05"]["vector"]
    wv05 = W.wave_on_grid(v05, m05.grid, m05.setup.u1_mode)
    vi = np.flatnonzero(wv05["valid"])
    div = m05.divisor(v05)
    M05 = np.column_stack([wv05["x"], wv05["y"], wv05["z"], wv05["vz"] / div])[vi]
    om05 = wv05["omega"][vi]

    def R_of(x, y, z, vz):
        j = W.closest(np.column_stack([x, y, z, vz / div]), M05)
        return S.circular_R(z, om05[j], vz)

    d = data
    r_obs = R_of(d.cx[idx], d.cy[idx], d.cz[idx], d.cvz[idx])
    sig_meas = d.csig[idx] / np.array([1.0, 1.0, 1.0, div])
    sd = np.sqrt(P["sigma_pc"] ** 2 + sig_meas ** 2)

    def gen_points(model, v, gen_inlier):
        """Model points of the T4 clusters, and the residual pool: the generating fit's own inliers."""
        ev = model.evaluate(v)
        dv = model.divisor(v)
        Mall = model.model_vectors(ev["wave"], v)[ev["cl_idx"]]
        Dall = model.cluster_vectors(v)
        pool = (Dall - Mall)[np.asarray(gen_inlier, bool)]
        return Mall[idx], pool, dv

    def draws(name, model, v, noise, gen_inlier):
        def go():
            Mp, res, dv = gen_points(model, v, gen_inlier)
            rng = rng_for(P["seed"], name)
            out = np.empty(P["t4_mocks"])
            for i in range(P["t4_mocks"]):
                if noise == "gauss":
                    new = Mp + rng.standard_normal(Mp.shape) * sd
                else:
                    new = Mp + res[rng.integers(0, len(res), len(Mp))]
                out[i] = R_of(new[:, 0], new[:, 1], new[:, 2], new[:, 3] * dv)
            return out
        return store.cached(name, go)

    out = {"n_clusters": int(len(idx)), "R_obs": r_obs}
    for noise in (("gauss", "resid") if with_resid else ("gauss",)):
        st = draws(f"{prefix}t4_stand_{noise}", m05, v05, noise, gen_inliers(mods["b05"], fits["b05"], idx_mask))
        pw1 = draws(f"{prefix}t4_pow1_{noise}", mods["col4"], fits["b1"]["vector"], noise,
                    gen_inliers(mods["col4"], fits["b1"], None))
        p, k = S.p_low(r_obs, st)
        k_pow1, n_pow1 = S.power_count(pw1, st, P["t4_p_excl"])
        pow1 = k_pow1 / n_pow1
        rec = {"p": p, "k_standing_at_or_below": k, "n_standing": int(len(st)), "p_mcse": S.p_mcse(p, len(st)),
               "power_B1": pow1, "n_power_B1": int(len(pw1)),
               "k_power_B1_p_below": k_pow1,
               "power_B1_mcse": S.p_mcse(pow1, len(pw1)),
               "R_standing_quantiles": np.round(np.quantile(st, [0.001, 0.01, 0.05, 0.5, 0.95]), 4).tolist(),
               "R_power_B1_quantiles": np.round(np.quantile(pw1, [0.05, 0.5, 0.95]), 4).tolist(),
               "label": S.t4_label(p, pow1, p_excl=P["t4_p_excl"], p_not=P["t4_p_not"],
                                   power_min=P["t4_power_min"])}
        if with_free_power:
            pwf = draws(f"{prefix}t4_powfree_{noise}", mods["col5"], fits["free"]["vector"], noise,
                        gen_inliers(mods["col5"], fits["free"], None))
            rec["power_Bfree"] = S.power(pwf, st, P["t4_p_excl"])
            rec["R_power_Bfree_quantiles"] = np.round(np.quantile(pwf, [0.05, 0.5, 0.95]), 4).tolist()
        if keep_arrays and noise == "gauss":
            rec["R_standing"] = st.tolist()
            rec["R_power_B1"] = pw1.tolist()
        out[noise] = rec
    out["label"] = out["gauss"]["label"]
    ctx.log(f"T4 {prefix or 'main'}: R_obs = {r_obs:.3f}, p = {out['gauss']['p']:.4f}, "
            f"power = {out['gauss']['power_B1']:.3f} -> {out['label']}")
    return out


def end_of_grid_mask(model, v):
    ev = model.evaluate(v)
    vi = ev["valid_idx"]
    return (ev["cl_idx"] != vi[0]) & (ev["cl_idx"] != vi[-1])


# =============================================================================================
# T5

def t5_run(P, store, prefix, data, grid, chain_vectors, median_vector, ctx, *, cut_sigma, bandwidth, u1_mode,
           known_answer=None, sens=True):
    kr = (P["t5_k_min"], P["t5_k_max"], P["t5_k_step"])
    cut = None if cut_sigma is None else cut_sigma * P["sigma_pc"]
    d = data

    def point(omega0):
        cur = F.t5_curve(median_vector, grid, u1_mode, omega0=omega0)
        return F.t5_analyse(cur, d.cx, d.cy, d.cz, d.cvz, d.csig, cut=cut, bandwidth=bandwidth,
                            sigma=P["sigma_pc"], k_range=kr)

    def boot(omega0, tag):
        def go():
            rng = rng_for(P["seed"], prefix + "t5boot" + tag)
            return F.t5_bootstrap(chain_vectors, grid, d.cx, d.cy, d.cz, d.cvz, d.csig, rng, n_boot=P["t5_boot"],
                                  cut=cut, bandwidth=bandwidth, u1_mode=u1_mode, omega0=omega0, k_range=kr,
                                  sigma=P["sigma_pc"])
        return store.cached(prefix + "t5boot" + tag, go)

    pt = point(W.OMEGA0_ADOPTED)
    bt = boot(W.OMEGA0_ADOPTED, "")
    out = summarise_t5(P, pt, bt, known_answer)
    if sens:
        om = P["t5_omega0_sens_kms_kpc"] / 1000.0
        pt2, bt2 = point(om), boot(om, "_sens")
        lo, hi = S.interval(bt2["bhat"])
        out["sensitivity_omega0"] = {"omega0_kms_kpc": P["t5_omega0_sens_kms_kpc"],
                                     "bhat": pt2["fit"]["bhat"] if pt2["fit"] else None, "bhat_interval": [lo, hi]}
    ctx.log(f"T5 {prefix or 'main'}: bhat = {out['bhat']}, interval {out['bhat_interval']}, "
            f"k_z/k_vz interval {out['k_ratio_interval']} -> {out['wavelengths_label']} / {out['bhat_label']}")
    return out


def summarise_t5(P, pt, bt, known_answer):
    f = pt["fit"]
    blo, bhi = S.interval(bt["bhat"])
    klo, khi = S.interval(bt["k_ratio"])
    rlo, rhi = S.interval(bt["rho"])
    dlo, dhi = F.circ_interval(bt["Delta"])
    wl = S.wavelength_label(klo, khi, tuple(P["t5_band"]))
    ka_pass = True if known_answer is None else bool(known_answer["passed"])
    bl = S.bhat_label(blo, bhi, b_t=P["t5_b_t"], wavelengths=wl, known_answer_pass=ka_pass)
    n = len(bt["bhat"])
    return {
        "n_in": pt["n_in"], "n_end_of_grid_dropped": pt["n_end"], "n_kept": pt["n_kept"],
        "fit": f, "bhat": f["bhat"] if f else None, "bhat_interval": [blo, bhi],
        "bhat_interval_mcse": [S.quantile_mcse(bt["bhat"], 0.025), S.quantile_mcse(bt["bhat"], 0.975)],
        "k_ratio": f["k_ratio"] if f else None, "k_ratio_interval": [klo, khi],
        "k_ratio_interval_mcse": [S.quantile_mcse(bt["k_ratio"], 0.025), S.quantile_mcse(bt["k_ratio"], 0.975)],
        "Delta": f["Delta"] if f else None, "Delta_interval": [dlo, dhi],
        "rho": f["rho"] if f else None, "rho_interval": [rlo, rhi],
        "interval_contains_0": bool(blo is not None and blo <= 0.0 <= bhi),
        "interval_contains_0p68": bool(blo is not None and blo <= 0.68 <= bhi),
        "n_boot_ok": n, "n_boot_failed": bt["n_fail"],
        "k_at_bound_fraction": {"k_z": float(np.mean((np.abs(bt["k_z"] - P["t5_k_min"]) < 1e-4) |
                                                     (np.abs(bt["k_z"] - P["t5_k_max"]) < 1e-4))) if n else None,
                                "k_vz": float(np.mean((np.abs(bt["k_vz"] - P["t5_k_min"]) < 1e-4) |
                                                      (np.abs(bt["k_vz"] - P["t5_k_max"]) < 1e-4))) if n else None},
        "wavelengths_label": wl, "bhat_label": bl["label"], "bhat_opposite_direction": bl["opposite_direction"],
        "bhat_caveat_wavelengths_undetermined": bl["caveat_wavelengths_undetermined"],
        "known_answer_passed": ka_pass,
    }


def t5_known_answer(P, store, grid, data, sel_mask, chain_vectors, median_vector, ctx, *, inject=None,
                    u1_mode="half", prefix=""):
    """README 4.4: mocks on K24's column-(6) medians with omega0 t = -0.38 at B = 0.5, 0.84, 1.

    README 4.10 (R-CONV reruns): `inject(B)` gives the injected vector instead, `u1_mode` the convention's
    baseline and `prefix` separates the checkpoint names; the defaults are the formal run's check."""
    kr = (P["t5_k_min"], P["t5_k_max"], P["t5_k_step"])
    cut = P["t5_cut_sigma"] * P["sigma_pc"]
    dsel = data.cluster_subset(sel_mask)
    m6 = W.Model(W.Setup(free=SHAPE, sigma=P["sigma_pc"], u1_mode=u1_mode), dsel, grid)
    cur = F.t5_curve(median_vector, grid, u1_mode)
    rows = {}
    passed = True
    for B in P["t5_ka_B"]:
        v_inj = W.k24_vector(6, w0t=P["t5_ka_w0t"], B=B) if inject is None else inject(B)
        mocks = []
        for i in range(P["t5_ka_mocks"]):
            name = f"{prefix}t5ka_B{B}_{i}"

            def one(name=name):
                rng = rng_for(P["seed"], name)
                x, y, z, vz = F.known_answer_vectors(m6, v_inj, dsel, rng, sigma=P["sigma_pc"])
                pt = F.t5_analyse(cur, x, y, z, vz, dsel.csig, cut=cut, bandwidth=P["bandwidth_pc"],
                                  sigma=P["sigma_pc"], k_range=kr)
                bt = F.t5_bootstrap(chain_vectors, grid, x, y, z, vz, dsel.csig, rng, n_boot=P["t5_boot"], cut=cut,
                                    bandwidth=P["bandwidth_pc"], u1_mode=u1_mode, k_range=kr, sigma=P["sigma_pc"])
                lo, hi = S.interval(bt["bhat"])
                return {"bhat": pt["fit"]["bhat"] if pt["fit"] else float("nan"), "interval": [lo, hi]}
            mocks.append(store.cached(name, one))
        target = 2 * B - 1
        order = np.argsort([m["bhat"] for m in mocks], kind="stable")
        med = mocks[order[(len(mocks) // 2) - 1]]          # the 10th of 20 when ranked by bhat
        lo, hi = med["interval"]
        if B >= 1.0:
            ok = lo is not None and lo > P["t5_b_t"]
            cover = float(np.mean([m["interval"][0] is not None and m["interval"][0] > P["t5_b_t"] for m in mocks]))
        else:
            ok = lo is not None and lo <= target <= hi
            cover = float(np.mean([m["interval"][0] is not None and m["interval"][0] <= target <= m["interval"][1]
                                   for m in mocks]))
        passed &= bool(ok)
        bh = np.array([m["bhat"] for m in mocks])
        rows[str(B)] = {"target_2B_minus_1": target, "median_mock_bhat": med["bhat"], "median_mock_interval": [lo, hi],
                        "pass": bool(ok), "coverage_or_above_bT_fraction": cover,
                        "mean_bhat": float(np.nanmean(bh)), "bias": float(np.nanmean(bh) - target),
                        "bhat_all": np.round(bh, 4).tolist()}
        ctx.log(f"T5 known-answer B = {B}: median mock bhat {med['bhat']:.3f} interval {[lo, hi]} -> "
                f"{'pass' if ok else 'FAIL'}")
    return {"passed": bool(passed), "injections": rows, "n_selected": int(sel_mask.sum()),
            "placement": "each selected cluster at the injected model's point closest to its (x, y, z)"}


# =============================================================================================
# T7

def rotation_lsr(x, y, vc):
    """Flat rotation curve relative to the LSR at heliocentric (x, y); x towards the Galactic Centre."""
    rx, ry = x - W.R_SUN, y
    r = np.hypot(rx, ry)
    return vc * ry / r, vc * (-rx) / r - vc


def theta2(cl, inlier, w, vc):
    vrx, vry = rotation_lsr(cl["x"].to_numpy(float), cl["y"].to_numpy(float), vc)
    rx = cl["vx"].to_numpy(float) - vrx
    ry = cl["vy"].to_numpy(float) - vry
    m = np.asarray(inlier, bool)
    ww = w[m]
    return float(np.sum(ww * rx[m]) / ww.sum()), float(np.sum(ww * ry[m]) / ww.sum())


def co_m2lnl(model, v, co, th2, vc, vz_zero=False):
    ev = model.evaluate(v)
    j = ev["co_idx"]
    wv = ev["wave"]
    x, y = wv["x"][j], wv["y"][j]
    vrx, vry = rotation_lsr(x, y, vc)
    vx, vy = vrx + th2[0], vry + th2[1]
    vz = np.zeros_like(x) if vz_zero else wv["vz"][j]
    l, b = np.radians(co["l"].to_numpy(float)), np.radians(co["b"].to_numpy(float))
    vm = np.cos(l) * np.cos(b) * vx + np.sin(l) * np.cos(b) * vy + np.sin(b) * vz
    e = 0.5 * (co["vr84"].to_numpy(float) - co["vr16"].to_numpy(float))
    r = co["vr"].to_numpy(float) - vm

    def f(s):
        var = e ** 2 + s ** 2
        return float(np.sum(r ** 2 / var + np.log(2 * math.pi * var)))
    opt = minimize_scalar(f, bounds=(0.0, 50.0), method="bounded", options={"xatol": 1e-6})
    s_best = float(opt.x) if opt.fun < f(0.0) else 0.0
    return {"m2lnL": f(s_best), "sigma_int": s_best, "max_abs_vz_los": float(np.max(np.abs(np.sin(b) * vz)))}


# =============================================================================================
# T8

def t8_run(P, models, res_k, res_b, res_div):
    i = models["col7"].setup.free.index("ln_omega0")
    lk, lb = res_k["samples"][:, i], res_b["samples"][:, i]
    pk, pb = S.percentiles(lk), S.percentiles(lb)
    half_b = 0.5 * (pb["p84"] - pb["p16"])
    shift = (pk["median"] - pb["median"]) / half_b if half_b > 0 else float("inf")
    label = S.t8_label(half_b, P["t8_prior_sigma_ln_omega0"], shift, width_frac=P["t8_width_frac"],
                       shift_max=P["t8_shift_max"])

    def derived(res, name):
        return t8_derived(P, models[name], res, "t8draws_" + name)
    return {"ln_omega0_k24_prior": pk, "ln_omega0_broad_prior": pb, "halfwidth_broad": half_b,
            "k24_prior_sigma": P["t8_prior_sigma_ln_omega0"], "median_shift_in_sigma_broad": shift,
            "label": label, "k24_priors": derived(res_k, "col7"), "broad_priors": derived(res_b, "col7_broad"),
            "variant_divisor_fixed": derived(res_div, "col7_div") | {"divisor_kms_kpc": P["t8_divisor_variant_kms_kpc"]}}


def t8_derived(P, m, res, draws_name):
    """omega0, rho0 = omega0^2/(4 pi G), the Sun's vertical period, mu0, r0 from t8_draws posterior draws."""
    rng = rng_for(P["seed"], draws_name)
    sam = res["samples"][rng.integers(0, len(res["samples"]), P["t8_draws"])]
    om = np.exp(sam[:, m.setup.free.index("ln_omega0")])
    mu = np.exp(sam[:, m.setup.free.index("ln_mu0")]) * 1e-3
    r0 = sam[:, m.setup.free.index("r0")]
    rho = np.array([W.rho0(o) for o in om])
    per = np.array([W.sun_period_myr(o, u, r, P["sun_vz_kms"]) for o, u, r in zip(om, mu, r0)])
    return {"omega0_kms_kpc": S.percentiles(1000 * om), "rho0_msun_pc3": S.percentiles(rho),
            "sun_period_myr": S.percentiles(per[np.isfinite(per)]), "mu0_kpc": S.percentiles(mu * 1e3),
            "r0_pc": S.percentiles(r0)}


# =============================================================================================
# T6

def variant_list(P, cl):
    out = []
    for v in P["variants"]:
        if v == "v8_leave_out_reference":
            if cl is None:
                out += [f"v8_{i}" for i in range(6)]
                continue
            counts = cl["reference"].value_counts()
            singles = sorted(counts[counts == 1].index.tolist())
            for ref in sorted(counts[counts > 1].index.tolist()):
                out.append(("v8_leave_out", (ref,)))
            if singles:
                out.append(("v8_leave_out", tuple(singles)))
        else:
            out.append((v, ()))
    return out


def variant_name(v):
    name, refs = v
    return name if not refs else name + ":" + "+".join(refs)


def variant_config(P, v, cl):
    name, refs = v
    n = len(cl)
    cfg = {"outlier": "k24", "bandwidth": P["bandwidth_pc"], "mask": np.ones(n, bool), "dvz": 0.0,
           "u1_mode": "half", "t5_cut_sigma": P["t5_cut_sigma"], "t3_mocks": False}
    if name == "v1_outlier_3sigma":
        cfg.update(outlier="3sigma", t5_cut_sigma=P["v1_cut_sigma"], t3_mocks=True)
    elif name == "v2_no_outlier_model":
        cfg.update(outlier="gauss", t5_cut_sigma=None, t3_mocks=True)
    elif name == "v3_no_weights":
        cfg.update(bandwidth=0.0)
    elif name == "v4_bandwidth_50":
        cfg.update(bandwidth=P["v4_bandwidth_pc"])
    elif name == "v5_bandwidth_200":
        cfg.update(bandwidth=P["v5_bandwidth_pc"])
    elif name == "v6_wsun_7p25":
        cfg.update(dvz=P["v6_dvz_kms"])
    elif name == "v7_no_orion":
        l, b = galactic_lb(cl["x"].to_numpy(float), cl["y"].to_numpy(float), cl["z"].to_numpy(float))
        (l0, l1), (b0, b1) = P["v7_orion_l_deg"], P["v7_orion_b_deg"]
        cfg["mask"] = ~((l > l0) & (l < l1) & (b > b0) & (b < b1))
    elif name == "v8_leave_out":
        cfg["mask"] = ~cl["reference"].isin(refs).to_numpy()
    elif name == "v9_low_sigmavz":
        cfg["mask"] = cl["sigmavz"].to_numpy(float) < np.median(cl["sigmavz"].to_numpy(float))
    elif name == "v10_chord_u1":
        cfg.update(u1_mode="chord")
    else:
        raise ValueError(f"unknown variant {name}")
    return cfg


def run_variant(P, store, v, cl, co, grid, main, ctx):
    vn = variant_name(v)
    cfg = variant_config(P, v, cl)
    prefix = "v_" + hashlib.sha1(vn.encode()).hexdigest()[:10] + "_"
    data = make_data(cl, co, cfg["dvz"]).cluster_subset(cfg["mask"])
    mods, wc, wo = models_for(P, data, grid, cfg["bandwidth"], cfg["outlier"], cfg["u1_mode"])
    mf = main["fits"]
    starts = {"b1": [mf["b1"]["theta"]], "b05": [mf["b05"]["theta"]], "free": [mf["free"]["theta"]]}
    fits = t3_ml_three(P, store, prefix, mods, starts, ctx)
    obs_s = max(2 * (fits["free"]["lnL"] - fits["b05"]["lnL"]), 0.0)
    obs_t = max(2 * (fits["free"]["lnL"] - fits["b1"]["lnL"]), 0.0)
    rec = {"variant": vn, "n_clusters": int(data.n_clusters), "two_dlnL_standing": obs_s,
           "two_dlnL_travelling": obs_t}
    if cfg["t3_mocks"]:
        ms, cs = t3_mocks(P, store, prefix + "t3s_", mods["b05"], fits["b05"], mods["col5"], fits["free"], data,
                          "gauss", ctx)
        mt, ct = t3_mocks(P, store, prefix + "t3t_", mods["col4"], fits["b1"], mods["col5"], fits["free"], data,
                          "gauss", ctx)
        st_s, st_t = t3_stat(obs_s, ms, 1, P), t3_stat(obs_t, mt, 2, P)
        lab = t3_labels(st_s, st_t, P)
        rec["t3"] = {"rule": "full", "standing_stat": st_s, "travelling_stat": st_t, "clipped": [cs, ct], **lab}
    else:
        red = t3_reduced(obs_s, obs_t, main["t3"]["standing_stat"]["factor"], main["t3"]["travelling_stat"]["factor"], P)
        ms_, mt_ = main["t3"]["standing_stat"], main["t3"]["travelling_stat"]
        red["p_cal_standing_mcse"] = S.calibrated_p_mcse(obs_s, ms_["m"], ms_["se_m"], 1)
        red["p_cal_travelling_mcse"] = S.calibrated_p_mcse(obs_t, mt_["m"], mt_["se_m"], 2)
        rec["t3"] = {"rule": "reduced", **red}
    if cfg["outlier"] == "gauss":
        t4_mask = end_of_grid_mask(mods["b05"], fits["b05"]["vector"])
    else:
        t4_mask = np.asarray(fits["b05"]["inlier"], bool)
    rec["t4"] = t4_run(P, store, prefix, mods, fits, data, t4_mask, ctx, with_free_power=False, with_resid=False)
    if cfg["u1_mode"] == "chord":
        res3 = mcmc(P, store, "col3_chord", mods["col3"], main["col3_median_vector"], ctx)
        chain_vec = np.array([mods["col3"].full(s) for s in res3["samples"]])
        med_vec = F.posterior_median_vector(mods["col3"], res3["samples"])
        rec["col3_chain"] = chain_meta(res3)
    else:
        chain_vec, med_vec = main["col3_chain_vectors"], main["col3_median_vector"]
    rec["t5"] = t5_run(P, store, prefix, data, grid, chain_vec, med_vec, ctx, cut_sigma=cfg["t5_cut_sigma"],
                       bandwidth=cfg["bandwidth"], u1_mode=cfg["u1_mode"], known_answer=main["known_answer"],
                       sens=False)
    for k in ("fit",):
        rec["t5"].pop(k, None)
    return rec


def change_mcse(rec, label):
    """Monte Carlo standard errors of the quantities behind a variant's label (README section 2, T6)."""
    t3 = rec["t3"]
    if label in ("T3 standing", "T3 pure travelling"):
        side = "standing" if label == "T3 standing" else "travelling"
        if t3["rule"] == "full":
            s = t3[side + "_stat"]
            return {"p_cal": s.get("p_cal"), "p_cal_mcse": s.get("p_cal_mcse"), "p_boot": s["p_boot"],
                    "p_boot_mcse": s["p_boot_mcse"]}
        return {"p_cal": t3[f"p_cal_{side}"], "p_cal_mcse": t3.get(f"p_cal_{side}_mcse")}
    if label == "T4":
        g = rec["t4"]["gauss"]
        return {"p": g["p"], "p_mcse": g["p_mcse"], "power_B1": g["power_B1"], "power_B1_mcse": g["power_B1_mcse"]}
    t5 = rec["t5"]
    if label == "T5 wavelengths":
        return {"k_ratio_interval": t5["k_ratio_interval"], "k_ratio_interval_mcse": t5["k_ratio_interval_mcse"]}
    return {"bhat_interval": t5["bhat_interval"], "bhat_interval_mcse": t5["bhat_interval_mcse"]}


def compare_variants(main_labels, main_reduced, variants):
    changes = []
    for rec in variants:
        t3 = rec["t3"]
        ref = main_labels if t3["rule"] == "full" else main_reduced
        pairs = {
            "T3 standing": (ref["standing"], t3["standing"]),
            "T3 pure travelling": (ref["pure_travelling"], t3["pure_travelling"]),
            "T4": (main_labels["t4"], rec["t4"]["label"]),
            "T5 wavelengths": (main_labels["t5_wavelengths"], rec["t5"]["wavelengths_label"]),
            "T5 bhat": (main_labels["t5_bhat"], rec["t5"]["bhat_label"]),
        }
        rec["labels"] = {k: b for k, (a, b) in pairs.items()}
        rec["changed"] = [k for k, (a, b) in pairs.items() if a != b]
        for k in rec["changed"]:
            changes.append({"variant": rec["variant"], "label": k, "main": pairs[k][0], "variant_label": pairs[k][1],
                            "mcse": change_mcse(rec, k)})
    return ("robust" if not changes else "fragile"), changes


# =============================================================================================
# README 4.10 (T-056, post hoc): R-CONV (which convention reproduces column (3)?) and T8-P (omega0 with
# the v_z divisor fixed at 74). Standalone parts: run alone, write rconv.json / t8p.json and only the
# R_CONV / T8_P keys of summary.json; every other results file is left untouched.

STANDALONE = ("conv", "t8p", "diag")
STANDALONE_KEYS = {"conv": ("rconv", "R_CONV"), "t8p": ("t8p", "T8_P"), "diag": ("rdiag", "R_DIAG")}


def conv_seed(P, index):
    """Column-(3) chain seed of convention `index`: the integer drawn from the seed sequence
    (seed, conv_seed_offset + index), i.e. (seed, 3000 + index) at the defaults."""
    ss = [int(P["seed"]) % (2 ** 32), int(P["conv_seed_offset"]) + int(index)]
    return int(np.random.default_rng(ss).integers(2 ** 31))


def conv_models(P, data, grid, conv):
    """Column (3)-(6) models under one convention (README 4.10). sigma: the convention's (F or P) for the
    clouds-only column (3); 47 pc (sigma_pc) for every cluster fit. Weights W: fixed at K24's column-(6)
    medians on the convention's curve; R: recomputed at each parameter vector (same bandwidth)."""
    bw = P["bandwidth_pc"]
    wc, wo = W.fixed_weights(data, grid, bw, conv["u1_mode"])
    common = dict(sigma=P["sigma_pc"], outlier="k24", u1_mode=conv["u1_mode"], weights_mode=conv["weights_mode"],
                  bandwidth=bw)
    st = {"col3": W.Setup(free=SHAPE, clusters=False, clouds=True, sigma_mode=conv["sigma_mode"], **common),
          "col4": W.Setup(free=SHAPE, **common),
          "col5": W.Setup(free=SHAPE + ("w0t", "B"), **common),
          "col6": W.Setup(free=SHAPE, clouds=True, **common)}
    return {k: W.Model(s, data, grid, wc, wo) for k, s in st.items()}


def sigma_p_of(model, v):
    """README 4.10 P's sigma at v: sqrt(0.5 x the unweighted standard deviation of the clouds' d^2)."""
    ev = model.evaluate(v)
    if ev is None or "co_res" not in ev:
        return None
    d2 = (ev["co_res"] ** 2).sum(1)
    return float(math.sqrt(0.5 * float(np.std(d2))))


def conv_row(conv, model, res):
    """One convention's column-(3) record: T1 count, sigma-scaled differences, width ratio, chain."""
    t1 = t1_column(model, res, 3)
    k24 = W.K24_TABLE2[3]
    ours = {n: (t1["parameters"][n]["ours"]["p16"], t1["parameters"][n]["ours"]["p84"]) for n in T1_KEYS}
    theirs = {n: (k24[n][1], k24[n][2]) for n in T1_KEYS}
    med = F.posterior_median_vector(model, res["samples"])
    return {**{k: conv[k] for k in ("index", "name", "baseline", "sigma", "weights", "n_factors_differing")},
            "count": t1["n_inside_of_6"], "t1_label": t1["label"],
            "inside": {n: t1["parameters"][n]["inside_k24_1sigma"] for n in T1_KEYS},
            "sigma_scaled_differences": {n: t1["parameters"][n]["sigma_scaled_difference"] for n in T1_KEYS + ANCHORS},
            "width_ratio": S.width_ratio(ours, theirs),
            "halfwidth_ratios": {n: S.half_width(*ours[n]) / (0.5 * sum(theirs[n])) for n in T1_KEYS},
            "parameters": {n: t1["parameters"][n]["ours"] for n in T1_KEYS + ANCHORS},
            "sigma_P_at_median_pc": sigma_p_of(model, med),
            "chain": chain_meta(res)}


def ka_injection_vector(v3, v5, B):
    """README 4.10 known-answer injection: the chosen convention's column-(3) posterior median (anchors and
    A, p, delta, s0, gamma, phi; omega0, mu0, r0 adopted), omega0 t from its column-(5) median, and B."""
    v = np.array(v3, float)
    v[W.IDX["w0t"]] = float(v5[W.IDX["w0t"]])
    v[W.IDX["B"]] = float(B)
    return v


def conv_reruns(P, store, data, grid, conv, mods, res3, ctx):
    """Columns (4), (5), (6), T1 for (4) and (6), T5 and its known-answer check under the chosen convention."""
    pre = f"conv{conv['index']:02d}_"
    qual = f"under {conv['name']}, post hoc"
    col3_vecs = np.array([mods["col3"].full(s) for s in res3["samples"]])
    col3_med = F.posterior_median_vector(mods["col3"], res3["samples"])
    res4 = mcmc(P, store, pre + "col4", mods["col4"], W.k24_vector(4), ctx)
    res5 = mcmc(P, store, pre + "col5", mods["col5"], W.k24_vector(5), ctx)
    res6 = mcmc(P, store, pre + "col6", mods["col6"], W.k24_vector(6), ctx)
    v5 = F.posterior_median_vector(mods["col5"], res5["samples"])
    t1 = {}
    for c, r, col in (("col4", res4, 4), ("col6", res6, 6)):
        t1[c] = t1_column(mods[c], r, col)
        t1[c]["label_qualified"] = f"{t1[c]['label']} {qual}"
    f5 = mods["col5"].setup.free
    col5 = {"B": S.percentiles(res5["samples"][:, f5.index("B")]),
            "w0t": S.percentiles(res5["samples"][:, f5.index("w0t")]), "median": W.physical(v5)}
    # T5 (README 4.4) on the chosen convention's column-(3) median curve; its known-answer check is
    # injected on that same curve (README 4.10)
    cur = F.t5_curve(col3_med, grid, conv["u1_mode"])
    _, _, sel = F.t5_select(cur, data.cx, data.cy, data.cz, cut=P["t5_cut_sigma"] * P["sigma_pc"])
    ka = t5_known_answer(P, store, grid, data, sel, col3_vecs, col3_med, ctx,
                         inject=lambda B: ka_injection_vector(col3_med, v5, B), u1_mode=conv["u1_mode"], prefix=pre)
    inj = W.physical(ka_injection_vector(col3_med, v5, 1.0))
    inj.pop("B")
    ka["injected_vector"] = inj
    ka["injected_B"] = list(P["t5_ka_B"])
    t5 = t5_run(P, store, pre, data, grid, col3_vecs, col3_med, ctx, cut_sigma=P["t5_cut_sigma"],
                bandwidth=P["bandwidth_pc"], u1_mode=conv["u1_mode"], known_answer=ka)
    t5["known_answer"] = ka
    labels = {"T1_col4": t1["col4"]["label_qualified"], "T1_col6": t1["col6"]["label_qualified"],
              "T5_wavelengths": f"{t5['wavelengths_label']} ({qual})", "T5_bhat": f"{t5['bhat_label']} ({qual})",
              "T5_known_answer_passed": bool(ka["passed"])}
    chains = {k: chain_meta(r) for k, r in (("col4", res4), ("col5", res5), ("col6", res6))}
    return {"convention": conv["name"], "index": conv["index"], "sigma_pc_cluster_fits": P["sigma_pc"],
            "t1": t1, "col5": col5, "t5": t5, "labels": labels, "chains": chains,
            "chain_short": [k for k, r in (("col4", res4), ("col5", res5), ("col6", res6)) if r["chain_short"]],
            "note": "reported next to the formal run's labels; the formal labels, the overall reading and T6 "
                    "stay as recorded; T3, T4, T6, T7 are not rerun (README 4.10)"}


def conv_run(P, store, data, grid, ctx):
    """README 4.10 Part A: the sixteen column-(3) chains, the choice rule, and the reruns if one is chosen."""
    idxs = [int(i) for i in P["conv_indices"]]
    rows, keep = [], {}
    for i in idxs:
        conv = W.convention(i)
        mods = conv_models(P, data, grid, conv)
        res = mcmc(P, store, f"conv{i:02d}_col3", mods["col3"], W.k24_vector(3), ctx, seed_int=conv_seed(P, i))
        row = conv_row(conv, mods["col3"], res)
        rows.append(row)
        keep[i] = (conv, mods, res)
        ctx.log(f"R-CONV {conv['name']} (index {i}): count {row['count']}/6, width ratio {row['width_ratio']:.3f}"
                f"{' (chain short)' if res['chain_short'] else ''}")
    choice = S.rconv_choose(rows, min_count=P["conv_min_count"], repro_count=P["conv_repro_count"],
                            ratio_range=tuple(P["conv_width_range"]))
    ctx.log(f"R-CONV: {choice['label']}" + (f" ({choice['reason']})" if choice["reason"] else ""))
    out = {"post_hoc": True, "conventions": rows, "choice": choice, "label": choice["label"],
           "complete_set": sorted(idxs) == list(range(16)),
           "k24_column3": {n: dict(zip(("median", "plus", "minus"), W.K24_TABLE2[3][n])) for n in T1_KEYS + ANCHORS},
           "reruns": None}
    if choice["chosen"] is not None:
        conv, mods, res3 = keep[choice["chosen"]]
        out["reruns"] = conv_reruns(P, store, data, grid, conv, mods, res3, ctx)
    return out


def conv_summary(rc):
    rr = rc["reruns"]
    return {"label": rc["label"], "case": rc["choice"]["case"], "chosen": rc["choice"].get("chosen_name"),
            "reason": rc["choice"]["reason"], "complete_set": rc["complete_set"],
            "counts": {r["name"]: r["count"] for r in rc["conventions"]},
            "width_ratios": {r["name"]: r["width_ratio"] for r in rc["conventions"]},
            "reruns": rr["labels"] if rr else None,
            "chain_short": [r["name"] + ":col3" for r in rc["conventions"] if r["chain"]["chain_short"]]
            + ([rr["convention"] + ":" + k for k in rr["chain_short"]] if rr else [])}


def t8p_run(P, store, mods, ctx):
    """README 4.10 Part B: column-(7) setup with the divisor fixed at 74 under the formal convention (L, F, W),
    under K24's priors and under the broad priors; section 2's T8 rule plus the bound rule."""
    rk = mcmc(P, store, "t8p_k24", mods["col7_div"], W.k24_vector(7), ctx)
    rb = mcmc(P, store, "t8p_broad", mods["col7_div_broad"], W.k24_vector(7), ctx)
    return t8p_evaluate(P, mods, rk, rb, ctx)


def t8p_evaluate(P, mods, rk, rb, ctx):
    i = mods["col7_div"].setup.free.index("ln_omega0")
    lk, lb = np.asarray(rk["samples"][:, i], float), np.asarray(rb["samples"][:, i], float)
    pk, pb = S.percentiles(lk), S.percentiles(lb)
    half_b = 0.5 * (pb["p84"] - pb["p16"])
    shift = (pk["median"] - pb["median"]) / half_b if half_b > 0 else float("inf")
    om_med_b = 1000.0 * math.exp(pb["median"])
    lo, hi = P["t8_broad_omega0_kms_kpc"]
    lab = S.t8p_label(half_b, P["t8_prior_sigma_ln_omega0"], shift, om_med_b, (lo, hi), bound_frac=P["t8p_bound_frac"],
                      width_frac=P["t8_width_frac"], shift_max=P["t8_shift_max"])
    om_b = 1000.0 * np.exp(lb)
    kd = t8_derived(P, mods["col7_div"], rk, "t8p_draws_k24")
    bd = t8_derived(P, mods["col7_div_broad"], rb, "t8p_draws_broad")
    out = {"post_hoc": True, "divisor_kms_kpc": P["t8_divisor_variant_kms_kpc"], "convention": "L-F-W",
           "ln_omega0_k24_prior": pk, "ln_omega0_broad_prior": pb, "halfwidth_broad": half_b,
           "k24_prior_sigma": P["t8_prior_sigma_ln_omega0"], "width_frac": P["t8_width_frac"],
           "shift_max": P["t8_shift_max"], "median_shift_in_sigma_broad": shift,
           "broad_median_omega0_kms_kpc": om_med_b, "label": lab["label"], "at_bound": lab["at_bound"],
           "width_shift_rule_label": lab["width_shift_rule_label"], "bound_thresholds_kms_kpc": lab["bound_thresholds"],
           "broad_bounds_kms_kpc": [lo, hi],
           "distance_to_upper_bound": {"median_kms_kpc": hi - om_med_b,
                                       "p84_kms_kpc": hi - bd["omega0_kms_kpc"]["p84"],
                                       "fraction_above_threshold": float(np.mean(om_b > lab["bound_thresholds"][1]))},
           "distance_to_lower_bound": {"median_kms_kpc": om_med_b - lo,
                                       "p16_kms_kpc": bd["omega0_kms_kpc"]["p16"] - lo,
                                       "fraction_below_threshold": float(np.mean(om_b < lab["bound_thresholds"][0]))},
           "k24_priors": kd, "broad_priors": bd,
           "chains": {"k24": chain_meta(rk), "broad": chain_meta(rb)},
           "chain_short": [k for k, r in (("k24", rk), ("broad", rb)) if r["chain_short"]],
           "note": "the withdrawn T8 stays withdrawn (README 4.10)"}
    ctx.log(f"T8-P: half-width {half_b:.3f} (limit {P['t8_width_frac'] * P['t8_prior_sigma_ln_omega0']:.3f}), "
            f"shift {shift:.2f} sigma, broad median {om_med_b:.1f} km/s/kpc -> {lab['label']}")
    return out


def t8p_summary(t8p):
    return {"label": t8p["label"], "at_bound": t8p["at_bound"], "halfwidth_broad": t8p["halfwidth_broad"],
            "median_shift_in_sigma_broad": t8p["median_shift_in_sigma_broad"],
            "omega0_k24": t8p["k24_priors"]["omega0_kms_kpc"], "omega0_broad": t8p["broad_priors"]["omega0_kms_kpc"],
            "chain_short": t8p["chain_short"]}


# =============================================================================================
# README 4.11 (T-061, post hoc): R-DIAG, where the column-(3) difference comes from. Standalone part "diag":
# Part A (per-object terms on the 79 rows), Part B (the reconstructed sightline sample S, with S_all and S+PT),
# Part C (K24's published curve), Part D (the origin of s free, with the reference chain c-ref; z_sun), reading.

def load_diag_tables(ctx):
    """The three R-DIAG files via ctx.http (55,870 + 9,894 + 47,253 bytes)."""
    ph = ctx.http(HANDBOOK_URL, label="Zucker et al. 2020 Table A.1 (Dataverse doi:10.7910/DVN/07L7YZ, file 4361456)")
    pb = ctx.http(BRIDGING_URL, label="Alves et al. 2020 bridging sightlines (doi:10.7910/DVN/K16GQX, file 4361453)")
    pf = ctx.http(BESTFIT_URL, label="K24 best-fit model curve (doi:10.7910/DVN/F98QHY, file 8954305)")
    hb = pd.read_csv(ph, sep=r"\s+")
    br = pd.read_csv(pb, sep=r"\s+")
    bf = pd.read_csv(pf, sep="\t")
    for nm, df, need in (("Zucker", hb, ["name", "x", "y", "z"]), ("bridging", br, ["name", "x", "y", "z"]),
                         ("K24 curve", bf, ["x", "y", "z", "vz"])):
        miss = [c for c in need if c not in df.columns]
        if miss:
            raise ValueError(f"{nm} table: missing columns {miss}")
    shas = [hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in (ph, pb, pf)]
    return {"zucker": hb, "bridging": br, "curve": bf, "shas": shas,
            "rows": {"zucker": len(hb), "bridging": len(br), "curve": len(bf)}}


def diag_inputs(P, co, tables, ctx):
    """README 4.11 Part B: the named rows, the membership rule, S, S_all and S+PT. Stops (RuntimeError) unless
    S_all has rdiag_s_all_n points and S+PT has rdiag_pt_n more than S."""
    hb, br = tables["zucker"], tables["bridging"]
    bridge_names = set(br["name"].astype(str))
    named, bridge_rows = [], []
    for i, r in co.reset_index(drop=True).iterrows():
        nm = str(r["name"])
        if nm in D.NAME_MAP:
            named.append({"name": nm, "p": (float(r["x"]), float(r["y"]), float(r["z"])),
                          "sig": (float(r["xspread"]), float(r["yspread"]), float(r["zspread"])), "co_index": int(i)})
        elif nm in bridge_names:
            bridge_rows.append(i)
        else:
            raise RuntimeError(f"12CO row {nm!r} is neither in the name map nor a bridging sightline (README 4.11)")
    missing = sorted(set(D.NAME_MAP.values()) - set(hb["name"].astype(str)))
    if missing:
        raise RuntimeError(f"mapped Zucker names absent from the table: {missing}")
    members = D.membership(named, hb, k=P["rdiag_member_k"], floor=P["rdiag_member_floor_pc"])
    samples = D.build_samples(named, hb, br, members, pt_names=tuple(P["rdiag_pt_names"]))
    n = {k: int(len(v["x"])) for k, v in samples.items()}
    # agreement of the 12CO bridge rows with the bridging table (README 4.11: within 1 pc), reported only
    bt = br.set_index(br["name"].astype(str))
    dev = [float(np.max(np.abs(np.array([co.loc[i, a] for a in ("x", "y", "z")], float)
                                - bt.loc[str(co.loc[i, "name"]), ["x", "y", "z"]].to_numpy(float))))
           for i in bridge_rows]
    out = {"co_names": [str(x) for x in co["name"]], "n_named_rows": len(named),
           "n_bridge_rows_12co": len(bridge_rows), "n_points": n,
           "n_kept_sightlines": int(sum(len(m["kept"]) for m in members if m["status"] == "pass")),
           "fallback_rows": [m["name"] for m in members if m["status"] == "fallback"],
           "absorbed_rows": {m["name"]: m["absorbed_by"] for m in members if m["status"] == "absorbed"},
           "bridge_rows_max_abs_diff_pc": max(dev) if dev else None,
           "named": named, "members": members, "samples": samples}
    ctx.log(f"R-DIAG samples: S {n['S']} ({out['n_kept_sightlines']} sightlines, fallback {out['fallback_rows']}, "
            f"absorbed {out['absorbed_rows']}), S_all {n['S_all']}, S+PT {n['S+PT']}")
    if n["S_all"] != int(P["rdiag_s_all_n"]) or n["S+PT"] - n["S"] != int(P["rdiag_pt_n"]):
        raise RuntimeError(f"R-DIAG sample check failed: S_all has {n['S_all']} points (want {P['rdiag_s_all_n']}), "
                           f"S+PT - S = {n['S+PT'] - n['S']} (want {P['rdiag_pt_n']}); nothing is fitted (README 4.11)")
    return out


def diag_formal_reference(P, rconv_path):
    """The formal L-F-W column-(3) fit (rconv.json convention 0): count, D6, M6, and v_P (posterior medians)."""
    rconv_path = Path(rconv_path)
    if not rconv_path.exists():
        raise RuntimeError(f"R-DIAG needs {rconv_path.name} (R-CONV, README 4.10): run part 'conv' first")
    rc = json.loads(rconv_path.read_text(encoding="utf-8"))
    row = [r for r in rc["conventions"] if r["index"] == 0]
    if not row or row[0]["name"] != "L-F-W":
        raise RuntimeError("rconv.json has no convention 0 (L-F-W)")
    row = row[0]
    d6, m6, m6_name = D.d6_m6(row["sigma_scaled_differences"])
    v = W.k24_vector(3)
    par = row["parameters"]
    for n in ("x0", "y0", "x1", "y1", "x2", "y2", "A", "p", "s0", "phi"):
        v[W.IDX[n]] = par[n]["median"]
    v[W.IDX["ln_delta"]] = math.log(par["delta"]["median"])
    v[W.IDX["ln_gamma"]] = math.log(par["gamma"]["median"])
    return {"convention": "L-F-W", "count": int(row["count"]), "D6": d6, "M6": m6, "M6_parameter": m6_name,
            "width_ratio": row["width_ratio"], "D6_max": P["rdiag_d6_max"], "M6_max": P["rdiag_m6_max"],
            "v_P": v, "source": "results/rconv.json, convention 0"}


def diag_sample_data(sample):
    e = np.zeros(0)
    return W.Data(cx=e, cy=e, cz=e, cvz=e, csig=np.zeros((0, 4)), ox=np.asarray(sample["x"], float),
                  oy=np.asarray(sample["y"], float), oz=np.asarray(sample["z"], float))


def diag_fit_row(P, model, res, what):
    """One R-DIAG column-(3) chain: T1 count, sigma-scaled differences, D6, M6, width ratio, sigma_P, label."""
    t1 = t1_column(model, res, 3)
    k24 = W.K24_TABLE2[3]
    ours = {n: (t1["parameters"][n]["ours"]["p16"], t1["parameters"][n]["ours"]["p84"]) for n in T1_KEYS}
    theirs = {n: (k24[n][1], k24[n][2]) for n in T1_KEYS}
    diffs = {n: t1["parameters"][n]["sigma_scaled_difference"] for n in T1_KEYS + ANCHORS}
    d6, m6, m6_name = D.d6_m6(diffs)
    ratio = S.width_ratio(ours, theirs)
    status, reason = D.fit_status(t1["n_inside_of_6"], ratio, repro_count=P["conv_repro_count"],
                                  min_count=P["conv_min_count"], ratio_range=tuple(P["conv_width_range"]))
    med = F.posterior_median_vector(model, res["samples"])
    return {"what": what, "count": t1["n_inside_of_6"], "inside": {n: t1["parameters"][n]["inside_k24_1sigma"] for n in T1_KEYS},
            "sigma_scaled_differences": diffs, "D6": d6, "M6": m6, "M6_parameter": m6_name, "width_ratio": ratio,
            "halfwidth_ratios": {n: S.half_width(*ours[n]) / (0.5 * sum(theirs[n])) for n in T1_KEYS},
            "parameters": {n: t1["parameters"][n]["ours"] for n in T1_KEYS + ANCHORS},
            "sigma_P_at_median_pc": sigma_p_of(model, med), "status": status, "reason": reason,
            "label": D.fit_label(status, what), "chain": chain_meta(res)}


def diag_part_a(P, store, model, v_P, names, named_mask, ctx):
    """README 4.11 Part A on the 79 rows (formal L-F-W column-(3) setup): v_K, v_P and the MAP v_M."""
    v_K = W.k24_vector(3)

    def go():
        rng = rng_for(P["seed"], "ml_rdiag_map")
        starts = [model.theta_of(v_K), model.theta_of(v_P)]
        starts += [model.prior_draw(rng) for _ in range(int(P["rdiag_map_prior_draws"]))]
        best, vals, n_eval = None, [], 0
        t0 = time.time()
        for st in starts:
            r = F.optimise(model, st, nm_maxfev=P["ml_nm_maxfev"], lbfgs_maxfun=P["ml_lbfgs_maxfun"], objective="post")
            vals.append(r["value"])
            n_eval += r["n_eval"]
            if best is None or r["value"] > best["value"]:
                best = r
        ctx.log(f"R-DIAG MAP: ln posterior {best['value']:.3f} ({len(starts)} starts, {time.time() - t0:.0f} s)")
        return {"theta": best["theta"], "logpost": best["value"], "start_values": vals, "n_eval": n_eval,
                "n_starts": len(starts)}

    mp = store.cached("rdiag_map", go)
    vecs = {"K": v_K, "P": np.asarray(v_P, float), "M": model.full(mp["theta"])}
    at, terms = {}, {}
    for k, v in vecs.items():
        tm = D.object_terms(model, v)
        th = model.theta_of(v)
        lp = model.logprior(th)
        terms[k] = tm
        at[k] = {"parameters": W.physical(v), "lnL": tm["lnL"], "ln_prior": float(lp), "ln_posterior": float(tm["lnL"] + lp),
                 "sigma_P_pc": sigma_p_of(model, v), "sum_terms": float(tm["t"].sum()), "constant": tm["constant"]}
    objects = [{"name": str(names[i]), "named_row": bool(named_mask[i]), "weight": float(terms["K"]["w"][i]),
                **{f"s_{k}": float(terms[k]["s"][i]) for k in vecs}, **{f"d2_{k}": float(terms[k]["d2"][i]) for k in vecs},
                **{f"t_{k}": float(terms[k]["t"][i]) for k in vecs}} for i in range(len(names))]
    n = int(P["rdiag_top_n"])
    comp = {"K_minus_M": D.top_contributors(names, terms["K"]["t"] - terms["M"]["t"], named_mask, n),
            "K_minus_P": D.top_contributors(names, terms["K"]["t"] - terms["P"]["t"], named_mask, n)}
    return {"vectors": at, "map": {"logpost": mp["logpost"], "start_values": mp["start_values"],
                                   "n_starts": mp["n_starts"], "n_eval": mp["n_eval"]},
            "comparisons": comp, "objects": objects,
            "note": "descriptive, no label (README 4.11 Part A); t_i = w_i d_i^2 / (2 sigma^2), sigma = 47 pc"}


def diag_part_c(P, store, grid, curve_df, ctx):
    """README 4.11 Part C: (i) our curve at K24's column-(6) medians against K24's published curve; (ii) a least-
    squares fit of our curve (12 shape and anchor parameters plus c) to the published points."""
    v6 = W.k24_vector(6)
    wv = W.wave_on_grid(v6, grid, "half")
    cur = D.valid_curve(wv)
    pub = curve_df[["x", "y", "z", "vz"]].to_numpy(float)
    cmp = D.curve_compare(cur, pub)
    summ = D.curve_summary(cmp, match_median=P["rdiag_curve_match_median_pc"], match_p95=P["rdiag_curve_match_p95_pc"],
                           approx_median=P["rdiag_curve_approx_median_pc"], excl_frac=P["rdiag_curve_excl_frac"])
    keep3 = ~cmp["end_3d"]
    model = D.lsq_model(grid, v6, c_bounds=P["rdiag_c_prior_pc"], c_scale=P["rdiag_c_scale_pc"])

    def go():
        t0 = time.time()
        r = D.curve_lsq(model, pub[keep3, :3], nm_maxfev=P["ml_nm_maxfev"], lbfgs_maxfun=P["ml_lbfgs_maxfun"])
        ctx.log(f"R-DIAG curve fit: RMS {r['rms_start_pc']:.2f} -> {r['rms_pc']:.2f} pc ({r['n_eval']} evaluations, "
                f"{time.time() - t0:.0f} s)")
        return r

    lsq = store.cached("rdiag_curve_lsq", go)
    phys = W.physical(lsq["vector"])
    k6 = W.K24_TABLE2[6]
    fit = {"parameters": {n: phys[n] for n in D.SHAPE_PHYS}, "c_pc": float(lsq["vector"][W.IDX["s_origin"]]),
           "sigma_scaled_differences_from_k24_col6": {n: D.sigma_scaled(phys[n], k6[n]) for n in D.SHAPE_PHYS},
           "rms_pc": lsq["rms_pc"], "rms_start_pc": lsq["rms_start_pc"], "n_points": lsq["n_points"],
           "n_eval": lsq["n_eval"], "c_bounds_pc": list(P["rdiag_c_prior_pc"]),
           "note": "read in README section 5, without a label (README 4.11 Part C (ii))"}
    ctx.log(f"R-DIAG Part C: {summ['label']} (x-y median {summ['xy']['median']}, p95 {summ['xy']['p95']} pc; "
            f"excluded x-y {summ['n_excluded_xy']}, 3-D {summ['n_excluded_3d']})")
    return {"comparison": summ, "lsq_fit": fit, "label": summ["label"],
            "note": "x-y nearest points decide the label; the 3-D numbers depend on which posterior point K24 published"}


def diag_models_d(P, data, grid, wo):
    """README 4.11 Part D setups on the 79 rows: (c) the origin free, c-ref (s0 flat), (z_sun) z + 20.8 pc."""
    base = setups(P)["col3"]
    cset = replace(base, free=SHAPE + ("s_origin",), uniform={"s_origin": tuple(P["rdiag_c_prior_pc"])},
                   scales={"s_origin": float(P["rdiag_c_scale_pc"])})
    crset = replace(cset, uniform={"s_origin": tuple(P["rdiag_c_prior_pc"]), "s0": tuple(P["rdiag_cref_s0_prior_pc"])})
    dz = replace(data, oz=np.asarray(data.oz, float) + float(P["rdiag_zsun_pc"]))
    # weights of the shifted clouds as the formal rule defines them (each object's s at K24's column-(6) medians),
    # recomputed for the variant's data as README 4.9 item 9 does for the variants
    _, wz = W.fixed_weights(dz, grid, P["bandwidth_pc"])
    return {"c": W.Model(cset, data, grid, None, wo), "cref": W.Model(crset, data, grid, None, wo),
            "zsun": W.Model(base, dz, grid, None, wz), "w_zsun": wz}


def diag_c_posterior(model, res):
    f = model.setup.free
    sam = np.asarray(res["samples"], float)
    c = sam[:, f.index("s_origin")]
    pc = S.percentiles(c)
    other = {"s0": sam[:, f.index("s0")], "p": sam[:, f.index("p")], "gamma": np.exp(sam[:, f.index("ln_gamma")])}
    return {"c": pc, "halfwidth_pc": 0.5 * (pc["p84"] - pc["p16"]),
            "correlations": {k: float(np.corrcoef(c, x)[0, 1]) for k, x in other.items()},
            "s0": S.percentiles(other["s0"])}


def diag_timing(P, m79, mS):
    n = max(int(P["timing_evals"]), 5)
    out = {}
    for k, m in (("rows_79", m79), ("S", mS)):
        th = m.theta_of(W.k24_vector(3))
        m.loglike(th)
        t0 = time.perf_counter()
        for _ in range(n):
            m.loglike(th)
        out[k] = round((time.perf_counter() - t0) / n * 1e3, 3)
    return {"ms_per_loglike": out, "n_points": {"rows_79": m79.data.n_clouds, "S": mS.data.n_clouds}}


def diag_run(P, store, data, grid, mods, tables, inputs, formal, ctx):
    """README 4.11: Parts A-D and the reading."""
    bw = P["bandwidth_pc"]
    m79 = mods["col3"]
    names = inputs["co_names"]
    named_mask = np.array([n in D.NAME_MAP for n in names])
    samples = inputs["samples"]
    smods, sw = {}, {}
    for key in ("S", "S_all", "S+PT"):
        ds = diag_sample_data(samples[key])
        _, wo = W.fixed_weights(ds, grid, bw)
        sw[key] = wo
        smods[key] = W.Model(setups(P)["col3"], ds, grid, None, wo)
    timing = diag_timing(P, m79, smods["S"])
    ctx.log(f"R-DIAG timing: one column-(3) likelihood {timing['ms_per_loglike']} ms")

    part_a = diag_part_a(P, store, m79, formal["v_P"], names, named_mask, ctx)
    part_c = diag_part_c(P, store, grid, tables["curve"], ctx)

    w79 = {n: float(w) for n, w in zip(names, m79.w_co)}
    table = D.consistency_table(inputs["members"], tables["zucker"], w_s=sw["S"], s_rows=samples["S"]["row"], w79=w79)
    fits = {}
    for key, chain in (("S", "rdiag_S"), ("S_all", "rdiag_Sall"), ("S+PT", "rdiag_SPT")):
        res = mcmc(P, store, chain, smods[key], W.k24_vector(3), ctx)
        fits[key] = diag_fit_row(P, smods[key], res, f"with sample {key}")
        fits[key]["n_points"] = int(smods[key].data.n_clouds)
        ctx.log(f"R-DIAG {key}: {fits[key]['label']} (count {fits[key]['count']}, D6 {fits[key]['D6']:.3f}, "
                f"M6 {fits[key]['M6']:.3f}, width ratio {fits[key]['width_ratio']:.3f})")
    part_b = {"samples": {k: {"n_points": int(len(v["x"])), "points": [
        {"source": s, "row": r, "id": i, "x": float(x), "y": float(y), "z": float(z), "weight": float(w)}
        for s, r, i, x, y, z, w in zip(v["source"], v["row"], v["id"], v["x"], v["y"], v["z"], sw[k])]}
        for k, v in samples.items()},
        "n_kept_sightlines": inputs["n_kept_sightlines"], "fallback_rows": inputs["fallback_rows"],
        "absorbed_rows": inputs["absorbed_rows"], "n_named_rows": inputs["n_named_rows"],
        "bridge_rows_max_abs_diff_pc": inputs["bridge_rows_max_abs_diff_pc"],
        "consistency_table": table, "fits": fits,
        "rule": {"k": P["rdiag_member_k"], "floor_pc": P["rdiag_member_floor_pc"], "name_map": D.NAME_MAP,
                 "pt_names": list(P["rdiag_pt_names"])}}

    dm = diag_models_d(P, data, grid, m79.w_co)
    zname = f"z☉ = {float(P['rdiag_zsun_pc']):g} pc"
    rc = mcmc(P, store, "rdiag_c", dm["c"], W.k24_vector(3), ctx)
    rcr = mcmc(P, store, "rdiag_cref", dm["cref"], W.k24_vector(3), ctx)
    rz = mcmc(P, store, "rdiag_zsun", dm["zsun"], W.k24_vector(3), ctx)
    fc = diag_fit_row(P, dm["c"], rc, "with the origin free")
    fc["c_posterior"] = diag_c_posterior(dm["c"], rc)
    fz = diag_fit_row(P, dm["zsun"], rz, f"with {zname}")
    fz["weights_max_abs_change"] = float(np.max(np.abs(dm["w_zsun"] - m79.w_co)))
    cref = diag_c_posterior(dm["cref"], rcr)
    c_read = D.c_reading(cref["halfwidth_pc"], P["rdiag_c_halfwidth_max_pc"])
    part_d = {"c": fc, "zsun": fz,
              "c_ref": {"c_posterior": cref, "c_reading": c_read, "halfwidth_max_pc": P["rdiag_c_halfwidth_max_pc"],
                        "s0_prior_pc": list(P["rdiag_cref_s0_prior_pc"]), "chain": chain_meta(rcr),
                        "note": "reference chain: its count and labels are not reported or used (README 4.11)"},
              "c_reading": c_read, "c_prior_pc": list(P["rdiag_c_prior_pc"]), "zsun_pc": P["rdiag_zsun_pc"]}
    ctx.log(f"R-DIAG (c): {fc['label']}; c = {fc['c_posterior']['c']['median']:.0f} pc; c-ref half-width "
            f"{cref['halfwidth_pc']:.0f} pc -> c {c_read}; (z_sun): {fz['label']}")

    rd = D.reading(fits["S"], fc, fz, c_read, d6_max=P["rdiag_d6_max"], m6_max=P["rdiag_m6_max"],
                   c_name="the origin of s free", z_name=zname)
    ctx.log(f"R-DIAG reading: {rd['reading']}")
    chains = {"S": fits["S"], "S_all": fits["S_all"], "S+PT": fits["S+PT"], "c": fc, "zsun": fz}
    short = [k for k, r in chains.items() if r["chain"]["chain_short"]] + (["c_ref"] if rcr["chain_short"] else [])
    fr = {k: v for k, v in formal.items() if k != "v_P"}
    return {"post_hoc": True, "reading": rd["reading"], "reading_detail": rd, "formal_reference": fr,
            "v_P": W.physical(formal["v_P"]), "part_a": part_a, "part_b": part_b, "part_c": part_c, "part_d": part_d,
            "labels": {"S": fits["S"]["label"], "S_all": fits["S_all"]["label"], "S+PT": fits["S+PT"]["label"],
                       "c": fc["label"], "zsun": fz["label"], "c_reading": c_read, "curve": part_c["label"]},
            "chain_short": short, "timing": timing,
            "input_rows": tables["rows"],
            "note": "post hoc (README 4.11); the formal labels, the overall reading, T6, R-CONV and T8-P stay as recorded"}


def diag_summary(rd):
    pb = rd["part_b"]
    return {"reading": rd["reading"], "labels": rd["labels"],
            "n_points": {k: v["n_points"] for k, v in pb["samples"].items()},
            "counts": {k: pb["fits"][k]["count"] for k in pb["fits"]} | {"c": rd["part_d"]["c"]["count"],
                                                                        "zsun": rd["part_d"]["zsun"]["count"]},
            "D6": {k: pb["fits"][k]["D6"] for k in pb["fits"]} | {"c": rd["part_d"]["c"]["D6"],
                                                                 "zsun": rd["part_d"]["zsun"]["D6"]},
            "c_median_pc": rd["part_d"]["c"]["c_posterior"]["c"]["median"],
            "c_ref_halfwidth_pc": rd["part_d"]["c_ref"]["c_posterior"]["halfwidth_pc"],
            "chain_short": rd["chain_short"]}


def _dump(o):
    from astrolab.results import to_jsonable
    return json.dumps(to_jsonable(o), indent=1, ensure_ascii=False)


def summary_with_key(old_text, key, value, before="overall"):
    """summary.json with only `key` set to `value` (standalone parts). Every other key keeps its serialised
    bytes: refuses (RuntimeError) when the existing file does not re-serialise to itself. An existing key is
    replaced in place; a new one goes before `before`, or at the end."""
    old = json.loads(old_text)
    if not isinstance(old, dict) or _dump(old) != old_text:
        raise RuntimeError("summary.json does not re-serialise byte-identically; refusing to update it")
    new = {}
    for k, v in old.items():
        if k == before and key not in old:
            new[key] = value
        new[k] = value if k == key else v
    if key not in new:
        new[key] = value
    for k in old:
        if k != key and _dump(new[k]) != _dump(old[k]):
            raise RuntimeError(f"summary.json key {k} would change")
    return new


def standalone_tag(parts):
    return "".join(p for p in STANDALONE if p in parts)


def check_standalone(P, parts, formal):
    """README 4.10, 4.11: 'conv', 't8p' and 'diag' run alone; a formal run takes one of them, R-CONV with all 16
    conventions."""
    other = sorted(set(parts) - set(STANDALONE))
    if other:
        raise ValueError(f"parts {sorted(set(STANDALONE) & set(parts))} run alone (README 4.10, 4.11), not with {other}")
    if formal and len(parts) != 1:
        raise ValueError("a formal run takes one standalone part at a time: parts ['conv'], ['t8p'] or ['diag']")
    if formal and "conv" in parts and sorted(int(i) for i in P["conv_indices"]) != list(range(16)):
        raise ValueError("the formal R-CONV run uses all 16 conventions (conv_indices = 0..15)")


def main_standalone(ctx, P, parts):
    """README 4.10, 4.11: parts 'conv', 't8p' and/or 'diag' (one at a time in a formal run). Other parts' results
    are read, never written; summary.json changes only in its R_CONV / T8_P / R_DIAG key."""
    from astrolab import config

    formal = is_formal_run(ctx)
    check_standalone(P, parts, formal)
    tag = standalone_tag(parts)
    ctx.record_suffix = "_" + tag
    sum_path = Path(ctx.results) / "summary.json"
    if sum_path.exists():                       # refuse before any work if the summary cannot be updated
        for p in STANDALONE:
            if p in parts:
                summary_with_key(sum_path.read_text(encoding="utf-8"), STANDALONE_KEYS[p][1], None)
    elif formal:
        raise RuntimeError("standalone parts update summary.json: the formal full run must exist first")

    cl, co, shas = load_tables(ctx)
    check_columns(cl, co)
    diag_tables = diag_in = diag_formal = None
    if "diag" in parts:                          # README 4.11: the three files of R-DIAG (113,017 bytes)
        diag_tables = load_diag_tables(ctx)
        shas = shas + diag_tables["shas"]
    grid = W.Grid(int(P["grid_n"]), float(P["u_min"]), float(P["u_max"]))
    data = make_data(cl, co)
    mods, wc, wo = models_for(P, data, grid, P["bandwidth_pc"])
    lc = load_check(data.cvz, wc, P["load_check_max_abs_vz"])
    ctx.log(f"load check: weighted mean v_z = {lc['weighted_mean_vz']:.2f} km/s -> {'pass' if lc['passed'] else 'FAIL'}")
    if not lc["passed"]:
        raise RuntimeError("load check failed (README 3); nothing is written")
    if diag_tables is not None:                  # the sample checks stop the run before any fit (README 4.11)
        diag_in = diag_inputs(P, co, diag_tables, ctx)
        diag_formal = diag_formal_reference(P, HERE / "results" / "rconv.json")
    key = F.checkpoint_key({k: v for k, v in P.items() if k not in _RUN_ONLY} | {"standalone_parts": tag},
                           [HERE / "run.py", HERE / "wave011.py", HERE / "fit011.py", HERE / "stats011.py",
                            HERE / "diag011.py"], shas)
    stop = float(P["stop_after_hours"]) * 3600 if P["stop_after_hours"] else None
    store = F.Store(checkpoint_root(config.cache_dir(), P, ctx) / tag, key, stop)
    ctx.log(f"checkpoints ({'formal run' if formal else 'exploration'}, {tag}): {store.dir}")
    files = {}
    try:
        if "conv" in parts:
            files["rconv"] = conv_run(P, store, data, grid, ctx)
        if "t8p" in parts:
            files["t8p"] = t8p_run(P, store, mods, ctx)
        if "diag" in parts:
            files["rdiag"] = diag_run(P, store, data, grid, mods, diag_tables, diag_in, diag_formal, ctx)
    except F.Paused as e:
        ctx.log(f"PAUSED: {e}")
        ctx.record_suffix = "_" + tag + "paused"     # keep the records of the last complete run
        return {"status": "paused", "reason": str(e), "checkpoints": str(store.dir)}
    values = {"rconv": conv_summary(files["rconv"]) if "rconv" in files else None,
              "t8p": t8p_summary(files["t8p"]) if "t8p" in files else None,
              "rdiag": diag_summary(files["rdiag"]) if "rdiag" in files else None}
    if sum_path.exists():
        text = sum_path.read_text(encoding="utf-8")
        new = None
        for fname, skey in STANDALONE_KEYS.values():
            if fname in files:
                new = summary_with_key(text, skey, values[fname])
                text = _dump(new)
    else:                                        # an exploration starts from an empty folder
        new = {STANDALONE_KEYS[p][1]: values[STANDALONE_KEYS[p][0]] for p in STANDALONE if p in parts}
    for name, obj in files.items():
        ctx.save(name, obj | {"load_check": lc, "checkpoints": store.dir.name, "params": P})
    ctx.save("summary", new)
    if formal:
        finish_checkpoints(store, ctx)
        remove_paused_records(ctx, (f"provenance_{tag}paused.json", f"run_info_{tag}paused.json"))
    else:
        ctx.log(f"exploration checkpoints kept in {store.dir} (delete them when done)")
    return {STANDALONE_KEYS[p][1]: new[STANDALONE_KEYS[p][1]] for p in STANDALONE if p in parts}


# =============================================================================================
# main

def main(ctx):
    from astrolab import config

    P = dict(PARAMS)
    parts = set(P["parts"])
    if parts & set(STANDALONE):
        return main_standalone(ctx, P, parts)
    cl, co, shas = load_tables(ctx)
    check_columns(cl, co)
    grid = W.Grid(int(P["grid_n"]), float(P["u_min"]), float(P["u_max"]))
    data = make_data(cl, co)
    mods, wc, wo = models_for(P, data, grid, P["bandwidth_pc"])

    # 1. load check (README 3)
    lc = load_check(data.cvz, wc, P["load_check_max_abs_vz"])
    ctx.log(f"load check: weighted mean v_z = {lc['weighted_mean_vz']:.2f} km/s -> "
            f"{'pass' if lc['passed'] else 'FAIL'}")
    if not lc["passed"]:
        summary = {"status": "stopped: load check failed (README 3); the reading is fixed by a dated amendment",
                   "load_check": lc, "params": P}
        ctx.save("summary", summary)
        return summary

    timing = timing_estimate(P, mods, data, grid, ctx)
    key = F.checkpoint_key({k: v for k, v in P.items() if k not in _RUN_ONLY},
                           [HERE / "run.py", HERE / "wave011.py", HERE / "fit011.py", HERE / "stats011.py"], shas)
    stop = float(P["stop_after_hours"]) * 3600 if P["stop_after_hours"] else None
    formal = is_formal_run(ctx)
    store = F.Store(checkpoint_root(config.cache_dir(), P, ctx), key, stop)
    ctx.log(f"checkpoints ({'formal run' if formal else 'exploration'}): {store.dir}")
    try:
        out = pipeline(ctx, P, parts, cl, co, data, grid, mods, wc, store)
    except F.Paused as e:
        ctx.log(f"PAUSED: {e}")
        if formal:
            ctx.record_suffix = "_paused"    # keep provenance.json / run_info.json of the last complete run
        return {"status": "paused", "reason": str(e), "checkpoints": str(store.dir), "timing": timing}
    out["summary"]["load_check"] = lc
    out["summary"]["timing"] = timing
    out["summary"]["checkpoints"] = store.dir.name     # key folder only: no local path in results/
    for name, obj in out["files"].items():
        ctx.save(name, obj | {"params": P})
    ctx.save("summary", out["summary"] | {"params": P})
    if formal:
        finish_checkpoints(store, ctx)
        remove_paused_records(ctx)
    else:
        ctx.log(f"exploration checkpoints kept in {store.dir} (delete them when done)")
    return out["summary"]


def is_formal_run(ctx):
    """True for `astrolab run` (writes results/), False for `astrolab explore` (explore/<date>-<tag>/)."""
    return (getattr(ctx, "max_save_bytes", None) is None
            and Path(ctx.results).resolve() == (HERE / "results").resolve())


def checkpoint_root(cache_dir, P, ctx):
    """Formal runs: <cache>/<subdir>; explorations: <cache>/<subdir>/explore/<date>-<tag>, so an
    exploration never reads or deletes the formal run's checkpoints."""
    root = Path(cache_dir) / P["checkpoint_subdir"]
    if not is_formal_run(ctx):
        root = root / "explore" / Path(ctx.results).name
    return root


def _dir_bytes(d):
    return sum(f.stat().st_size for f in Path(d).rglob("*") if f.is_file())


def finish_checkpoints(store, ctx):
    """README 4.9 item 13: once every result is written, the run's checkpoint folder is deleted, and so
    are stale key folders (other code or PARAMS) directly under the formal root; explore/ is left alone."""
    import shutil
    size = store.size_bytes()
    ok = store.remove_all()
    ctx.log(f"checkpoints {'removed' if ok else 'could NOT be removed'}: {store.dir} ({size / 1024 ** 2:.1f} MB)")
    root = store.dir.parent
    if root.is_dir():
        for d in sorted(root.iterdir()):
            if d.is_dir() and d.name != "explore" and re.fullmatch(r"[0-9a-f]{20}", d.name):
                n = _dir_bytes(d)
                shutil.rmtree(d, ignore_errors=True)
                ctx.log(f"stale checkpoint folder {'removed' if not d.exists() else 'could NOT be removed'}: "
                        f"{d.name} ({n / 1024 ** 2:.1f} MB)")
    return ok


def remove_paused_records(ctx, names=("provenance_paused.json", "run_info_paused.json")):
    """A completed formal run supersedes the records of an earlier paused attempt."""
    removed = []
    for name in names:
        p = Path(ctx.results) / name
        if p.exists():
            p.unlink()
            removed.append(name)
    if removed:
        ctx.log(f"removed records of the paused attempt: {', '.join(removed)}")
    return removed


def pipeline(ctx, P, parts, cl, co, data, grid, mods, wc, store):
    files = {}
    # 2. column (3), clouds only
    res3 = mcmc(P, store, "col3", mods["col3"], W.k24_vector(3), ctx)
    col3_vecs = np.array([mods["col3"].full(s) for s in res3["samples"]])
    col3_med = F.posterior_median_vector(mods["col3"], res3["samples"])

    # 3. T5 known-answer check (no cluster fitted yet; positions only)
    cur0 = F.t5_curve(col3_med, grid)
    _, _, sel_mask = F.t5_select(cur0, data.cx, data.cy, data.cz, cut=P["t5_cut_sigma"] * P["sigma_pc"])
    known = None
    if "t5" in parts or "t6" in parts:
        known = t5_known_answer(P, store, grid, data, sel_mask, col3_vecs, col3_med, ctx)

    # 4. everything else
    main = {"col3_chain_vectors": col3_vecs, "col3_median_vector": col3_med, "known_answer": known}
    summary = {"status": "complete", "parts": sorted(parts)}
    res4 = mcmc(P, store, "col4", mods["col4"], W.k24_vector(4), ctx)
    res5 = mcmc(P, store, "col5", mods["col5"], W.k24_vector(5), ctx)
    res6 = mcmc(P, store, "col6", mods["col6"], W.k24_vector(6), ctx)
    v4 = F.posterior_median_vector(mods["col4"], res4["samples"])
    v6 = F.posterior_median_vector(mods["col6"], res6["samples"])
    v5 = F.posterior_median_vector(mods["col5"], res5["samples"])
    table_inlier = cl["inlier"].to_numpy(int) == 1

    if "t1t2" in parts:
        t1 = {"col4": t1_column(mods["col4"], res4, 4), "col6": t1_column(mods["col6"], res6, 6)}
        t1["col3_for_reference"] = t1_column(mods["col3"], res3, 3)
        for c, m, v in (("col4", mods["col4"], v4), ("col6", mods["col6"], v6)):
            ours = ~m.evaluate(v)["cl_outlier"]
            t1[c]["inliers_vs_table_flag"] = inlier_overlap(ours, table_inlier)
        bi = mods["col5"].setup.free.index("B")
        Bs = res5["samples"][:, bi]
        t2 = {"B": S.percentiles(Bs), "k24": {"median": 0.84, "plus": 0.07, "minus": 0.06},
              "P_B_gt_0p95": float(np.mean(Bs > 0.95)), "P_B_lt_0p5": float(np.mean(Bs < 0.5)),
              "w0t": S.percentiles(res5["samples"][:, mods["col5"].setup.free.index("w0t")]),
              "B_histogram": np.histogram(Bs, bins=20, range=(0, 1))[0].tolist()}
        both_not = t1["col4"]["label"] == "not reproduced" and t1["col6"]["label"] == "not reproduced"
        files["t1_t2"] = {"t1": t1, "t2": t2, "chains": {k: chain_meta(r) for k, r in
                                                          (("col3", res3), ("col4", res4), ("col5", res5), ("col6", res6))},
                          "plot": {"col6_median": model_curve_for_plot(mods["col6"], v6),
                                   "col4_median": model_curve_for_plot(mods["col4"], v4),
                                   "col5_median": model_curve_for_plot(mods["col5"], v5),
                                   "clusters_col6": points_for_plot(mods["col6"], v6, cl)}}
        summary["T1"] = {"col4": t1["col4"]["label"], "col6": t1["col6"]["label"],
                         "on_our_reproduction_only": both_not}
        summary["T2"] = {"B_median": t2["B"]["median"], "B_p16": t2["B"]["p16"], "B_p84": t2["B"]["p84"],
                         "P_B_gt_0p95": t2["P_B_gt_0p95"], "P_B_lt_0p5": t2["P_B_lt_0p5"]}
        summary["chain_short"] = [k for k, r in (("col3", res3), ("col4", res4), ("col5", res5), ("col6", res6))
                                  if r["chain_short"]]

    # T3: nested maximum-likelihood fits and mocks
    th05 = mods["b05"].theta_of(v5)
    fits = t3_ml_three(P, store, "main_", mods, {"b1": [mods["col4"].theta_of(v4)], "b05": [th05],
                                                 "free": [mods["col5"].theta_of(v5)]}, ctx)
    main["fits"] = fits
    obs_s = 2 * (fits["free"]["lnL"] - fits["b05"]["lnL"])
    obs_t = 2 * (fits["free"]["lnL"] - fits["b1"]["lnL"])
    neg = {"standing": obs_s < 0, "travelling": obs_t < 0}
    obs_s, obs_t = max(obs_s, 0.0), max(obs_t, 0.0)
    t3 = None
    if "t3" in parts or "t6" in parts:
        ms, cs = t3_mocks(P, store, "t3s_", mods["b05"], fits["b05"], mods["col5"], fits["free"], data, "gauss", ctx)
        mt, ct = t3_mocks(P, store, "t3t_", mods["col4"], fits["b1"], mods["col5"], fits["free"], data, "gauss", ctx)
        st_s, st_t = t3_stat(obs_s, ms, 1, P), t3_stat(obs_t, mt, 2, P)
        lab = t3_labels(st_s, st_t, P)
        t3 = {"standing_stat": st_s, "travelling_stat": st_t, "clipped": {"standing": cs, "travelling": ct},
              "data_negative_clipped": neg, **lab,
              "reduced_rule_main": t3_reduced(obs_s, obs_t, st_s["factor"], st_t["factor"], P),
              "fits": {k: fit_record(mods[m], fits[k]) for k, m in (("b1", "col4"), ("b05", "b05"), ("free", "col5"))}}
        inl = {k: np.asarray(fits[k]["inlier"], bool) for k in fits}
        t3["inlier_overlaps"] = {"b1_vs_b05": inlier_overlap(inl["b1"], inl["b05"]),
                                 "b1_vs_free": inlier_overlap(inl["b1"], inl["free"]),
                                 "b05_vs_free": inlier_overlap(inl["b05"], inl["free"]),
                                 "free_vs_table": inlier_overlap(inl["free"], table_inlier)}
        if P["t3_resid_variant"]:
            msr, csr = t3_mocks(P, store, "t3s_", mods["b05"], fits["b05"], mods["col5"], fits["free"], data, "resid", ctx)
            mtr, ctr = t3_mocks(P, store, "t3t_", mods["col4"], fits["b1"], mods["col5"], fits["free"], data, "resid", ctx)
            sr, tr = t3_stat(obs_s, msr, 1, P), t3_stat(obs_t, mtr, 2, P)
            t3["residual_resampling_variant"] = {"standing_stat": sr, "travelling_stat": tr,
                                                 "clipped": {"standing": csr, "travelling": ctr}, **t3_labels(sr, tr, P)}
        main["t3"] = t3
        files["t3"] = t3
        summary["T3"] = {"standing": t3["standing"], "pure_travelling": t3["pure_travelling"],
                         "two_dlnL_standing": obs_s, "two_dlnL_travelling": obs_t,
                         "p_cal_standing": st_s.get("p_cal"), "p_boot_standing": st_s["p_boot"],
                         "p_cal_travelling": st_t.get("p_cal"), "p_boot_travelling": st_t["p_boot"]}

    # T4
    t4 = None
    if "t4" in parts or "t6" in parts:
        t4 = t4_run(P, store, "main_", mods, fits, data, np.asarray(fits["b05"]["inlier"], bool), ctx,
                    keep_arrays=True)
        files["t4"] = t4
        summary["T4"] = {"label": t4["label"], "R_obs": t4["R_obs"], "p": t4["gauss"]["p"],
                         "power_B1": t4["gauss"]["power_B1"]}

    # T5
    t5 = None
    if "t5" in parts or "t6" in parts:
        t5 = t5_run(P, store, "main_", data, grid, col3_vecs, col3_med, ctx, cut_sigma=P["t5_cut_sigma"],
                    bandwidth=P["bandwidth_pc"], u1_mode="half", known_answer=known)
        t5["known_answer"] = known
        files["t5"] = t5
        summary["T5"] = {"wavelengths": t5["wavelengths_label"], "bhat": t5["bhat_label"],
                         "bhat_value": t5["bhat"], "bhat_interval": t5["bhat_interval"],
                         "k_ratio_interval": t5["k_ratio_interval"], "known_answer_passed": known["passed"]}

    # T6
    if "t6" in parts:
        main_labels = {"standing": t3["standing"], "pure_travelling": t3["pure_travelling"], "t4": t4["label"],
                       "t5_wavelengths": t5["wavelengths_label"], "t5_bhat": t5["bhat_label"]}
        main_red = dict(main_labels)
        main_red.update(standing=t3["reduced_rule_main"]["standing"],
                        pure_travelling=t3["reduced_rule_main"]["pure_travelling"])
        recs = []
        for v in variant_list(P, cl):
            ctx.log(f"T6 variant {variant_name(v)}")
            recs.append(run_variant(P, store, v, cl, co, grid, main, ctx))
        label, changes = compare_variants(main_labels, main_red, recs)
        files["t6"] = {"label": label, "changes": changes, "main_labels_full_rule": main_labels,
                       "main_labels_reduced_rule": main_red, "variants": recs}
        summary["T6"] = {"label": label, "changes": changes}

    # T7
    if "t7" in parts:
        f6 = ml(P, store, "col6", mods["col6"], [mods["col6"].theta_of(v6)], ctx)
        fc = ml(P, store, "t7c", mods["t7c"], [mods["t7c"].theta_of(v6)], ctx)
        vc = P["t7_vc_kms"]
        th_a = theta2(cl, f6["inlier"], wc, vc)
        th_c = theta2(cl, fc["inlier"], wc, vc)
        a = co_m2lnl(mods["col6"], f6["vector"], co, th_a, vc)
        b = co_m2lnl(mods["col6"], f6["vector"], co, th_a, vc, vz_zero=True)
        c = co_m2lnl(mods["t7c"], fc["vector"], co, th_c, vc)
        lab = S.t7_label(a["m2lnL"], b["m2lnL"], c["m2lnL"], P["t7_margin"])
        files["t7"] = {"a_col6_B1": a, "b_vz_zero": b, "c_B0p5": c, "theta2_a": th_a, "theta2_c": th_c,
                       "label": lab, "n_clouds": int(len(co)),
                       "fits": {"col6": fit_record(mods["col6"], f6), "t7c": fit_record(mods["t7c"], fc)}}
        summary["T7"] = {"label": lab, "m2lnL": [a["m2lnL"], b["m2lnL"], c["m2lnL"]]}

    # T8
    if "t8" in parts:
        rk = mcmc(P, store, "col7", mods["col7"], W.k24_vector(7), ctx)
        rb = mcmc(P, store, "col7_broad", mods["col7_broad"], W.k24_vector(7), ctx)
        rd = mcmc(P, store, "col7_div", mods["col7_div"], W.k24_vector(7), ctx)
        t8 = t8_run(P, mods, rk, rb, rd)
        t8["chains"] = {"col7": chain_meta(rk), "col7_broad": chain_meta(rb), "col7_div": chain_meta(rd)}
        files["t8"] = t8
        summary["T8"] = {"label": t8["label"], "omega0_k24": t8["k24_priors"]["omega0_kms_kpc"],
                         "omega0_broad": t8["broad_priors"]["omega0_kms_kpc"]}
        summary.setdefault("chain_short", [])
        summary["chain_short"] += [k for k, r in (("col7", rk), ("col7_broad", rb), ("col7_div", rd)) if r["chain_short"]]

    # overall reading (README section 2)
    if {"t1t2", "t3", "t4", "t5", "t6"} <= parts:
        ov = S.overall_reading(summary["T1"]["col4"], t3["standing"], t4["label"], t5["bhat_label"],
                               summary["T6"]["label"])
        if summary["T1"]["on_our_reproduction_only"]:
            ov["qualifier"] = "on our reproduction, which does not match K24's fit"
        summary["overall"] = ov
    else:
        summary["overall"] = {"reading": "not formed (not all of T1, T3-T6 were run)"}
    return {"files": files, "summary": summary}
