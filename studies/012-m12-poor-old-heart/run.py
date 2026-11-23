"""M12 Poor old heart: Gaia XP metallicities of the oldest Milky Way stars

Implements the pre-registration of README sections 1-4 (load checks L1-L7, T1-T6, overall readings),
with the amendments of README 4.12.

Run with:      python -m astrolab run 012-m12-poor-old-heart
Explore with:  python -m astrolab explore 012-m12-poor-old-heart --tag <topic> --set KEY=VALUE

Data: R22's two Zenodo files (213.8 MB), fetched once under the user's exception of 2026-11-21
(TODO.md T-021, log.md): the per-file cap is lifted with cap_consent and the files are kept out of
the study budget with budget_consent. Without PARAMS["first_download"] the files are read from the
cache only (astrolab.study.Context.http); the formal first run sets it once, then it is reset to False.

The formal run takes about a day on one core (README 4.10). It writes checkpoints outside the project
folder (astrolab cache dir / PARAMS["checkpoint_subdir"] / <key>), so an interrupted or paused run
(PARAMS["stop_after_hours"]) continues where it stopped when started again with the same PARAMS, code
and data. Results are written only when every requested part has finished.
"""
import re
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

import data012 as D
import kin012 as K
import model012 as M
import stats012 as S
import store012 as C

HERE = Path(__file__).resolve().parent
FILES = {
    "mh": {"url": "https://zenodo.org/records/7035810/files/xp_gc_mh.csv?download=1",
           "md5": "7257c98622573a4a625571fc973859c5", "max_bytes": 110_000_000,
           "label": "R22 metallicity file xp_gc_mh.csv (Zenodo 7035810, CC BY 4.0)"},
    "kin": {"url": "https://zenodo.org/records/7035810/files/xp_gc_kinematics.csv?download=1",
            "md5": "b220c27aacff1f2f03d5a1f2b5fca147", "max_bytes": 125_000_000,
            "label": "R22 kinematics file xp_gc_kinematics.csv (Zenodo 7035810, CC BY 4.0)"},
}
BUDGET_CONSENT = ("user consent 2026-11-21 (TODO.md T-021, studies/012 log.md 2026-11-21): R22's two Zenodo "
                  "files are kept out of the study budget, downloaded once")
CAP_CONSENT = ("user consent 2026-11-21 (TODO.md T-021, studies/012 log.md 2026-11-21): the per-file "
               "50 MB cap is lifted for R22's two Zenodo files (98.5 and 115.3 MB)")

# Tunable knobs (AGENTS.md section 2). Read them inside main() at call time, never into
# module-level constants, and pass values to helper modules as arguments (a helper that does
# `import run` gets a fresh copy without the override): `astrolab explore --set` overrides
# this dict in memory. The defaults are the pre-registered values (README sections 2-4 and 4.12);
# changing one in the committed file is a change to the pre-registration.
PARAMS = {
    "first_download": False,          # True only for the one consented download (README section 8)
    "t2_missing_ok": False,           # True only after the user declines the TAP addition (README 3)
    "gaia_addition": True,            # the optional Gaia DR3 TAP addition, user consent 2026-11-23 (README 4.13)
    "seed": 20261121,
    "subsample_seed": 12012,
    # frame (README 4.1)
    "R0_kpc": 8.2,
    "plx_zp_mas": 0.02,
    # T2 sample and likelihood (README 4.3)
    "t2_mh_range": [-99.0, -1.5],     # lo <= [M/H] < hi; the pre-registered sample is [M/H] < -1.5
    "grid_nodes": 300,
    "grid_dmin_kpc": 0.2,
    "grid_dmax_kpc": 30.0,
    "grid_d1_i_kpc": 1.0,
    "grid_check_tol_kpc": 0.01,
    "grid_max_nodes": 1200,           # memory bound of the grid check (README 4.12 item 4)
    "sigma_bounds_kpc": [0.5, 10.0],
    "bound_tol_kpc": 0.05,
    "sigma_true_kpc": 2.7,
    "t2a_boot": 200,
    "t2a_mocks": 100,
    "t2a_bias_max_kpc": 0.1,
    "ref_bins": [[-1.5, -1.0], [-1.0, -0.5]],
    "ref_max_stars": 50000,
    # mocks: luminosity function and extinction (README 4.3)
    "lf_snr_min": 10.0,
    "lf_mh_max": -1.0,
    "lf_min_stars": 500,
    "ext_a_grid": [0.0, 5.0, 0.05],
    "ext_bd_grid_deg": [1.0, 20.0, 0.5],
    # T2b (README 4.4)
    "t2b_bmin_deg": 5.0,
    "t2b_bmin_variants_deg": [3.0, 8.0],
    "t2b_boot": 200,
    "t2b_mocks": 100,
    "t2b_starts": 5,
    "t2b_q_power": 0.5,
    "t2b_pass_of_100": 80,
    "t2b_second_fp_kpc": 0.2,
    "control_mh": [-1.0, -0.5],
    # T3 (README 4.5)
    "t3_rapo_kpc": [3.0, 7.0],
    "t3_boot": 1000,
    "t3_w0_mocks": 100,
    "t3_w0_blur_dex": [0.1, 0.15, 0.2],
    "t3_delta": 0.05,
    "t3_bin_centers": [-2.0, -1.8, -1.6, -1.4, -1.2, -1.0, -0.8, -0.6],
    "t3_bin_width": 0.2,
    "t3_R0_variants_kpc": [8.0, 8.4],
    # T4 (README 4.6)
    "t4_shift_dex": 0.1,
    "t4_noise_dex": [0.1, 0.2],
    "t4_realisations": 10,
    "t4_trim_pct": [[1.0, 99.0], [5.0, 95.0]],
    "t4_bin_dex": 0.25,
    "t4_boot": 1000,
    # T5 (README 4.7)
    "t5_boot": 1000,
    "t5_variants": [[-1.9, -1.2], [-99.0, -1.2]],
    # T6 (README 4.8)
    "t6_m_giant": [800.0, 1000.0, 2000.0],
    "t6_f": [1.0, 2.5],
    "t6_snr_min": 5.0,
    "t6_mg_max": 0.5,
    "t6_target_msun": 5.0e7,
    # running
    "parts": ["t1", "t2", "t3", "t4", "t5", "t6"],
    "timing_evals": 5,
    "stop_after_hours": 10.0,          # pause (checkpointed) after this long; 0 = no limit
    "checkpoint_subdir": "s012_checkpoints",
}
# Floors of README 4.10: a formal run may not go below them.
FLOORS = {"t2a_boot": 200, "t2a_mocks": 100, "t2b_boot": 200, "t2b_mocks": 100, "t3_boot": 1000,
          "t3_w0_mocks": 100, "t4_boot": 1000, "t4_realisations": 10, "t5_boot": 1000}
# README section 2: the run stops if the metallicity file is not R22's sample (fewer than 1.0 million rows
# after L3). A module constant (not a PARAMS knob) so no exploration can lower it; tests patch it.
MIN_MH_ROWS = 1_000_000
# README 3 (optional TAP row) and 4.13: the Gaia DR3 addition for the stars with [M/H] < -0.5, queried on
# sorted source_id lists of 2,000. Module constants (not PARAMS knobs); tests patch ADDITION_CHUNK.
ADDITION_MH_MAX = -0.5
ADDITION_CHUNK = 2000
ADDITION_COLS = {"parallax": "parallax", "parallax_error": "parallax_error", "g": "phot_g_mean_mag",
                 "bp_rp": "bp_rp", "bp": "phot_bp_mean_mag"}
ALL_PARTS = ["t1", "t2", "t3", "t4", "t5", "t6"]
# a formal run uses these pre-registered sizes (README 4.3, 4.10)
FORMAL_FIXED = {"parts": ALL_PARTS, "grid_nodes": 300, "ext_a_grid": [0.0, 5.0, 0.05],
                "ext_bd_grid_deg": [1.0, 20.0, 0.5], "t2_mh_range": [-99.0, -1.5]}
_RUN_ONLY = ("stop_after_hours", "timing_evals", "parts", "checkpoint_subdir", "first_download")


def rng_for(seed, name):
    return np.random.default_rng([int(seed) % (2 ** 32), zlib.crc32(name.encode())])


def frange(spec):
    a, b, step = spec
    n = int(round((b - a) / step)) + 1
    return [round(a + i * step, 10) for i in range(n)]


def _cache_dir():
    from astrolab import config
    return config.cache_dir()


# =============================================================================================
# Data

def fetch_files(ctx, P):
    paths = {}
    for key, f in FILES.items():
        paths[key] = ctx.http(f["url"], label=f["label"], max_bytes=f["max_bytes"], suffix=".csv",
                              cap_consent=CAP_CONSENT, budget_consent=BUDGET_CONSENT,
                              allow_download=bool(P["first_download"]))
    return paths


def load_and_check(paths, P, ctx):
    """README 3, L1-L7. Raises D.StopRun(message, record) on a stopping failure; returns
    (mh, kin, joined, load record)."""
    rec = {}
    try:
        return _load_and_check(paths, P, ctx, rec)
    except D.StopRun as e:
        raise D.StopRun(e.args[0], rec) from None


def _load_and_check(paths, P, ctx, rec):
    rec["L1"] = D.check_md5(paths, {k: f["md5"] for k, f in FILES.items()})
    if not rec["L1"]["passed"]:
        raise D.StopRun("L1: MD5 mismatch")
    cols_mh = list(pd.read_csv(paths["mh"], nrows=0).columns)
    cols_kin = list(pd.read_csv(paths["kin"], nrows=0).columns)
    try:
        map_mh = D.map_columns(cols_mh, D.MH_CANDIDATES, D.MH_REQUIRED, "metallicity file")
        map_kin = D.map_columns(cols_kin, D.KIN_CANDIDATES, D.KIN_REQUIRED, "kinematics file")
    except D.StopRun:
        rec["L2"] = {"columns_mh": cols_mh, "columns_kin": cols_kin}
        raise
    t2_need = ("parallax", "parallax_error", "g", "bp_rp", "bp")
    have_lb = (map_mh["l"] and map_mh["b"]) or (map_mh["ra"] and map_mh["dec"])
    rec["L2"] = {"columns_mh": cols_mh, "columns_kin": cols_kin, "mapping_mh": map_mh, "mapping_kin": map_kin,
                 "present_mh": D.presence(map_mh, ("l", "b", "ra", "dec", "parallax", "parallax_error", "g",
                                                   "bp_rp", "bp", "mh_err", "teff", "logg")),
                 "t2_columns_missing": [q for q in t2_need if not map_mh[q]] + ([] if have_lb else ["l, b"]),
                 "kin_missing_t3": [q for q in ("jr", "jphi", "jz", "rapo") if not map_kin[q]],
                 "kin_missing_t5": [q for q in ("ecc", "rapo") if not map_kin[q]]}
    add_q = [q for q in t2_need if not map_mh[q]] if (P["gaia_addition"] and have_lb) else []
    if rec["L2"]["t2_columns_missing"] and not P["t2_missing_ok"] and not add_q:
        raise D.StopRun(
            f"L2: the metallicity file lacks {rec['L2']['t2_columns_missing']}. README 3: T2 and the "
            "parallax-based part of T6 then need the optional Gaia TAP addition, which needs the user's "
            "agreement (and BP magnitudes are not in that addition: the mocks' BP < 15.5 cut would need a "
            "dated amendment). Ask the user; if they decline, rerun with t2_missing_ok=true (T2 and f_bright "
            "'undetermined (data not in the files)').")
    mh = D.read_mapped(paths["mh"], map_mh)
    kin = D.read_mapped(paths["kin"], map_kin)
    mh, rec["L3_mh"] = D.drop_duplicates(mh, "metallicity file")
    if len(mh) < MIN_MH_ROWS:
        raise D.StopRun(f"L3: the metallicity file has {len(mh):,} rows after duplicates, fewer than "
                        f"{MIN_MH_ROWS:,}: not R22's sample; stop (README section 2), the reading is fixed by "
                        "a dated amendment")
    kin, rec["L3_kin"] = D.drop_duplicates(kin, "kinematics file")
    if add_q:
        mh, rec["L2"]["addition"] = gaia_addition(ctx, mh, add_q)
        rec["L2"]["t2_columns_missing_in_file"] = rec["L2"]["t2_columns_missing"]
        rec["L2"]["t2_columns_missing"] = []
    mh = D.add_galactic(mh)
    mh["mh_row"] = np.arange(len(mh))
    joined, rec["L4"] = D.join(kin.drop(columns=[c for c in ("mh",) if c in kin]), mh, cols=("mh", "mh_row"))
    rec["L5"] = D.check_units(joined)
    if rec["L5"]["jphi_flipped"]:
        joined["jphi"] = -joined["jphi"]
    rec["L6"] = D.l6_checks(mh)
    rec["L7"] = D.l7_range(mh["mh"].to_numpy(float))
    rec["rows"] = {"mh": len(mh), "kin": len(kin), "joined": len(joined)}
    ctx.log(f"load: {len(mh):,} metallicity rows, {len(kin):,} kinematics rows, join {rec['L4']['fraction']:.4f}")
    return mh, kin, joined, rec


def gaia_addition(ctx, mh, quantities):
    """README 3 (optional TAP row) and 4.13: fetch the missing T2 columns from gaiadr3.gaia_source for the
    stars with [M/H] < ADDITION_MH_MAX, on sorted source_id lists of ADDITION_CHUNK (each query returns at
    most one row per listed id, so max_rows is the list length). Stars above the limit get NaN. A returned
    id that was not asked for, or a duplicated one, stops the run. Returns (mh with the columns, record)."""
    ids = np.sort(mh.loc[mh["mh"] < ADDITION_MH_MAX, "source_id"].to_numpy(np.int64))
    cols = ["source_id"] + [ADDITION_COLS[q] for q in quantities]
    n_q = -(-ids.size // ADDITION_CHUNK)
    ctx.log(f"Gaia DR3 addition: {ids.size:,} stars with [M/H] < {ADDITION_MH_MAX}, {n_q} queries of "
            f"<= {ADDITION_CHUNK:,} source_ids, columns {cols[1:]}")
    frames = []
    for i in range(n_q):
        chunk = ids[i * ADDITION_CHUNK:(i + 1) * ADDITION_CHUNK]
        adql = (f"SELECT {', '.join(cols)} FROM gaiadr3.gaia_source "
                f"WHERE source_id IN ({', '.join(str(int(x)) for x in chunk)})")
        frames.append(ctx.tap(adql, "gaia", label=f"Gaia DR3 addition {i + 1}/{n_q}", max_rows=int(chunk.size),
                              release="Gaia DR3"))
    got = (pd.concat(frames, ignore_index=True) if frames
           else pd.DataFrame({c: pd.Series(dtype=float) for c in cols}))
    got = got[cols].rename(columns={ADDITION_COLS[q]: q for q in quantities})
    got["source_id"] = got["source_id"].astype("int64")
    if got["source_id"].duplicated().any() or not got["source_id"].isin(ids).all():
        raise D.StopRun("L2 Gaia addition: the archive returned a duplicated source_id or one not asked for")
    for q in quantities:
        got[q] = pd.to_numeric(got[q], errors="coerce").astype(float)
    out = mh.merge(got, on="source_id", how="left", validate="one_to_one")
    rec = {"consent": "user consent 2026-11-23 (studies/012 log.md 2026-11-23; README 4.13)",
           "table": "gaiadr3.gaia_source", "mh_max": ADDITION_MH_MAX, "chunk": ADDITION_CHUNK,
           "quantities": list(quantities), "columns": cols[1:], "n_ids": int(ids.size), "n_queries": n_q,
           "n_rows": int(len(got)), "n_unmatched": int(ids.size - len(got)),
           "n_finite": {q: int(np.isfinite(out[q].to_numpy(float)).sum()) for q in quantities}}
    ctx.log(f"Gaia DR3 addition: {len(got):,} rows for {ids.size:,} ids")
    return out, rec


def t2_arrays(df, lo, hi):
    """Stars with lo <= [M/H] < hi and finite T2 quantities (README 4.12 item 4)."""
    m = (df["mh"] >= lo) & (df["mh"] < hi)
    sub = df.loc[m]
    need = ["l", "b", "parallax", "parallax_error", "g", "bp_rp"]
    ok = np.isfinite(sub[need].to_numpy(float)).all(axis=1) & (sub["parallax_error"].to_numpy(float) > 0)
    s = sub.loc[ok]
    return {k: s[k].to_numpy(float) for k in need} | {"n_dropped_nonfinite": int((~ok).sum())}


def subsample(arr, n_max, seed):
    n = arr["l"].size
    if n <= n_max:
        return arr, False
    idx = np.sort(np.random.default_rng(seed).choice(n, n_max, replace=False))
    return {k: (v[idx] if isinstance(v, np.ndarray) else v) for k, v in arr.items()}, True


def lik_from(arr, version, P, k, mask=None):
    a = arr if mask is None else {kk: v[mask] for kk, v in arr.items() if isinstance(v, np.ndarray)}
    return M.Lik(a["l"], a["b"], a["parallax"], a["parallax_error"], a["g"], a["bp_rp"], version=version, k=k,
                 R0=P["R0_kpc"], zp=P["plx_zp_mas"], dmin=P["grid_dmin_kpc"], dmax=P["grid_dmax_kpc"],
                 d1_i=P["grid_d1_i_kpc"])


def lik_from_sim(sim, version, P, k):
    return M.Lik(sim["l"], sim["b"], sim["plx"], sim["err"], sim["g"], sim["bp_rp"], version=version, k=k,
                 R0=P["R0_kpc"], zp=P["plx_zp_mas"], dmin=P["grid_dmin_kpc"], dmax=P["grid_dmax_kpc"],
                 d1_i=P["grid_d1_i_kpc"])


def mock_inputs(mh, P):
    """LF sample and parallax-error sampler (README 4.3; README 4.12 items 5 and 8)."""
    need = ["g", "bp_rp", "bp", "parallax", "parallax_error", "b", "mh"]
    df = mh[need].dropna()
    df = df[df["parallax_error"] > 0]
    snr = df["parallax"] / df["parallax_error"]
    lf = df[(snr > P["lf_snr_min"]) & (df["mh"] < P["lf_mh_max"])]
    lf_rule = f"plx/err > {P['lf_snr_min']} and [M/H] < {P['lf_mh_max']}"
    if len(lf) < P["lf_min_stars"]:
        lf = df[snr > P["lf_snr_min"]]
        lf_rule = f"plx/err > {P['lf_snr_min']} (all metallicities: fewer than {P['lf_min_stars']} metal-poor)"
    lfs = M.LFSample(lf["g"], lf["bp_rp"], lf["bp"], lf["parallax"], lf["b"], zp=P["plx_zp_mas"])
    errs = M.ErrSampler(df["g"].to_numpy(float), df["parallax_error"].to_numpy(float))
    return lfs, errs, {"lf_rule": lf_rule, "lf_stars": int(len(lf)), "err_stars": int(len(df))}


def sim_cuts(load):
    """L6-declared cuts with a value (README 3 L6 and 4.3)."""
    return {q: [c for c in cuts if c.get("c") is not None] for q, cuts in load["L6"]["declared"].items()}


# =============================================================================================
# Timing (README 4.10: measured before the formal run)

def timing_estimate(P, n_stars, ctx):
    """Per-evaluation times on synthetic stars of the real size, and the projected hours with README
    4.10's evaluation counts and with the counts measured on a synthetic mock (model012.MEASURED_EVALS)."""
    n = max(int(n_stars), 100)
    t = M.time_evaluations(n, k=P["grid_nodes"], n_eval=max(int(P["timing_evals"]), 1))
    kw = dict(n_boot=P["t2b_boot"], n_mocks=P["t2b_mocks"], n_starts=P["t2b_starts"], n_stars=n,
              n_ref=P["ref_max_stars"])
    proj = {}
    for name, ev in (("prereg_counts", M.PREREG_EVALS), ("measured_counts", M.MEASURED_EVALS)):
        lo = M.project_hours(t, step2=False, **ev, **kw)["total"]
        mid = M.project_hours(t, **ev, **kw)
        hi = M.project_hours(t, second_fp=True, **ev, **kw)["total"]
        proj[name] = {"hours": {k: round(v, 2) for k, v in mid.items()}, "without_step2": round(lo, 2),
                      "with_step2_and_second_fp": round(hi, 2)}
    out = {"per_evaluation_s": {k: round(v, 4) for k, v in t.items() if k.endswith("_s")},
           "n_stars": t["n_stars"], "nodes": t["nodes"], "projected": proj,
           "note": "likelihood work only (T3, T5, T6 and the T3 parts of T4 add minutes); synthetic stars "
                   "of the real size"}
    ctx.log(f"timing: {out['per_evaluation_s']} s per evaluation; projected "
            f"{proj['measured_counts']['without_step2']}-{proj['measured_counts']['with_step2_and_second_fp']} h "
            f"(measured counts), {proj['prereg_counts']['without_step2']}-"
            f"{proj['prereg_counts']['with_step2_and_second_fp']} h (README 4.10 counts)")
    return out


# =============================================================================================
# T2

def t2_mock(P, store, name, k, gen, fit):
    """A mock is regenerated from its seed (deterministic) and its fit stored under the grid size."""
    return store.cached(f"{name}_K{k}", lambda: fit(gen()))


def t2a_fit_mock(P, k):
    def fit(sim):
        out = {}
        for v in ("i", "ii"):
            f = M.fit_sigma(lik_from_sim(sim, v, P, k), bounds=tuple(P["sigma_bounds_kpc"]))
            out[v] = f["sigma"]
        return out
    return fit


def t2b_fit_mock_step1(P, k, rng):
    def fit(sim):
        s1 = M.step1(lik_from_sim(sim, "ii", P, k), rng, n_starts=P["t2b_starts"])
        return {"label": s1["label"], "two_dlnl": s1["two_dlnl"], "q": s1["flat"]["theta"][1],
                "interval": s1["profile"]["interval"], "sigma_sph": s1["sph"]["sigma"]}
    return fit


def t2b_fit_mock_step2(P, k, rng):
    def fit(sim):
        lik = lik_from_sim(sim, "ii", P, k)
        sph = M.fit_sigma(lik)
        s1 = M.step1(lik, rng, sph=sph, n_starts=P["t2b_starts"], profile=False)
        pw = M.fit_pow(lik, rng, s1["flat"]["theta"], n_starts=P["t2b_starts"])
        dbic = M.delta_bic(pw["lnl"], s1["flat"]["lnl"], sim["l"].size)
        return {"label": M.step2_label(dbic), "dbic": dbic}
    return fit


def gen_sim(P, mi, name, i, n_target, sigma, q, bmin=0.0, completeness=False):
    def gen():
        return M.simulate(rng_for(P["seed"], f"{name}_{i}"), n_target, sigma=sigma, q=q, lf=mi["lf"],
                          ext=mi["ext"], errs=mi["errs"], R0=P["R0_kpc"], zp=P["plx_zp_mas"],
                          declared=mi["declared"], bmin=bmin, completeness=completeness)
    return gen


def grid_check(P, arr, ctx):
    """README 4.3: doubling the nodes must change sigma-hat by less than P["grid_check_tol_kpc"] (pre-registered 0.01 kpc; both versions)."""
    k = int(P["grid_nodes"])
    kmax = int(P["grid_max_nodes"])
    hist = []
    conv = {"i": False, "ii": False}
    diff = float("nan")
    # 300 vs 600, then 600 vs 1,200, then stop: no grid above grid_max_nodes is ever built (README 4.12 item 4)
    while 2 * k <= kmax:
        a = {v: M.fit_sigma(lik_from(arr, v, P, k), bounds=tuple(P["sigma_bounds_kpc"]))["sigma"] for v in ("i", "ii")}
        b = {v: M.fit_sigma(lik_from(arr, v, P, 2 * k), bounds=tuple(P["sigma_bounds_kpc"]))["sigma"] for v in ("i", "ii")}
        diff = max(abs(a[v] - b[v]) for v in a)
        hist.append({"nodes": k, "sigma": a, "sigma_doubled": b, "max_change": diff})
        conv = {v: bool(abs(a[v] - b[v]) < P["grid_check_tol_kpc"]) for v in a}
        if all(conv.values()) or 4 * k > kmax:
            break
        k *= 2
    ctx.log(f"grid check: {k} nodes (max change {diff:.4f} kpc; converged {conv})")
    return {"nodes": k, "passed": all(conv.values()), "converged": conv, "history": hist}


def run_t2(P, store, ctx, mh, load, before_data=None):
    lo, hi = P["t2_mh_range"]
    arr = t2_arrays(mh, lo, hi)
    n = arr["l"].size
    bmin = P["t2b_bmin_deg"]
    nb5 = int(np.sum(np.abs(arr["b"]) >= bmin))
    out = {"sample": {"mh_range": [lo, hi], "n": n, "n_b_ge_5": nb5, "n_dropped_nonfinite": arr["n_dropped_nonfinite"]}}
    l6 = load["L6"]
    unmodelled = bool(l6["parallax_dependent_cut"])

    # --- mock ingredients and the extinction grid (README 4.3), before any fit to the data's parallaxes
    lf, errs, mrec = mock_inputs(mh, P)
    declared = sim_cuts(load)
    mrec["declared_cuts_in_mocks"] = declared
    ext = M.extinction_grid(
        arr["b"], arr["bp_rp"], n_target=n, lf=lf, errs=errs, a_values=frange(P["ext_a_grid"]),
        bd_values=frange(P["ext_bd_grid_deg"]), seed=int(rng_for(P["seed"], "extgrid").integers(2 ** 31)),
        sigma=P["sigma_true_kpc"], R0=P["R0_kpc"], zp=P["plx_zp_mas"], declared=declared,
        row_cache=store.cached)
    ctx.log(f"extinction grid: a = {ext['a']} mag, b_d = {ext['b_d']} deg")
    mi = {"lf": lf, "errs": errs, "ext": (ext["a"], ext["b_d"]), "declared": declared}
    out["mocks"] = mrec | {"extinction": ext, "extinction_coefficients": {"A_G/A_V": M.EXT_G, "A_BP/A_V": M.EXT_BP,
                                                                         "A_RP/A_V": M.EXT_RP}}
    k0 = int(P["grid_nodes"])
    st = P["sigma_true_kpc"]
    nm = P["t2a_mocks"]
    nbm = P["t2b_mocks"]

    def t2a_mocks(k):
        return [t2_mock(P, store, f"t2a_mock_{i}", k, gen_sim(P, mi, "t2a_mock", i, n, st, 1.0),
                        t2a_fit_mock(P, k)) for i in range(nm)]

    def t2b_mocks(k, kind, sigma, q, completeness):
        return [t2_mock(P, store, f"t2b_{kind}_{i}", k,
                        gen_sim(P, mi, f"t2b_{kind}", i, nb5, sigma, q, bmin, completeness),
                        t2b_fit_mock_step1(P, k, rng_for(P["seed"], f"t2b_{kind}_{i}_starts")))
                for i in range(nbm)]

    t2a_mocks(k0)
    t2b_mocks(k0, "fp", st, 1.0, True)
    t2b_mocks(k0, "power", st, P["t2b_q_power"], False)
    if before_data:          # README 4.10 order: the T3 w0 mocks and T1 come before the T2a data fit
        before_data()

    # --- T2a on the data
    gc = store.cached("grid_check", lambda: grid_check(P, arr, ctx))
    grid_i, grid_ok = bool(gc["converged"]["i"]), bool(gc["converged"]["ii"])   # per version (README 4.12 item 4)
    k = gc["nodes"]
    out["grid_check"] = gc
    bnd = tuple(P["sigma_bounds_kpc"])
    fits = {v: store.cached(f"t2a_fit_{v}_K{k}", lambda v=v: M.fit_sigma(lik_from(arr, v, P, k), bounds=bnd))
            for v in ("i", "ii")}
    for f in fits.values():
        f["at_bound"] = M.at_bound(f["sigma"], *bnd, tol=P["bound_tol_kpc"])
    boot = {"i": [], "ii": []}
    chunk = 20
    for c0 in range(0, P["t2a_boot"], chunk):
        def go(c0=c0):
            liks = {v: lik_from(arr, v, P, k) for v in ("i", "ii")}
            res = {"i": [], "ii": []}
            for j in range(c0, min(c0 + chunk, P["t2a_boot"])):
                w = np.bincount(rng_for(P["seed"], f"t2a_boot_{j}").integers(0, n, n), minlength=n).astype(float)
                for v in ("i", "ii"):
                    res[v].append(M.fit_sigma(liks[v], w, bounds=bnd)["sigma"])
            return res
        r = store.cached(f"t2a_boot_{c0}_K{k}", go)
        for v in ("i", "ii"):
            boot[v] += r[v]
    mocks = t2a_mocks(k)
    brng = rng_for(P["seed"], "t2a_bias_se")
    bias = {}
    for v in ("i", "ii"):
        med, se = S.median_with_se([m[v] for m in mocks], brng)
        bias[v] = {"median_sigma": med, "bias": med - st, "bias_se": se,
                   "p16_p84": [float(np.percentile([m[v] for m in mocks], q)) for q in (16, 84)]}
    iv = {v: S.pct_interval(boot[v]) for v in ("i", "ii")}
    missing = False
    t2a = {"fits": fits, "intervals": iv, "boot_sigma_quantiles": {v: np.percentile(boot[v], [2.5, 16, 50, 84, 97.5]).tolist() for v in boot},
           "mock_bias": bias, "ii_minus_i": fits["ii"]["sigma"] - fits["i"]["sigma"],
           "unmodelled_selection": unmodelled,
           "reproduction_label": S.t2a_reproduction(missing, fits["i"]["sigma"], fits["i"]["at_bound"],
                                                     grid_ok=grid_i),
           "population_label": S.t2a_population(missing, fits["ii"]["at_bound"], bias["ii"]["bias"], unmodelled,
                                                iv["ii"], bias_max=P["t2a_bias_max_kpc"], grid_ok=grid_ok),
           "grid_converged": {"i": grid_i, "ii": grid_ok}}
    # reference fits (README 4.3)
    refs = {}
    for lo_r, hi_r in P["ref_bins"]:
        ra, sub = subsample(t2_arrays(mh, lo_r, hi_r), P["ref_max_stars"], P["subsample_seed"])
        key = f"{lo_r}_{hi_r}"
        refs[key] = store.cached(f"t2a_ref_{key}_K{k}", lambda ra=ra, sub=sub: {
            "n": int(ra["l"].size), "subsampled": sub,
            **{v: M.fit_sigma(lik_from(ra, v, P, k), bounds=bnd) for v in ("i", "ii")}})
    t2a["reference_fits"] = refs | {"subsample_seed": P["subsample_seed"]}
    out["t2a"] = t2a
    ctx.log(f"T2a: sigma (i) {fits['i']['sigma']:.3f}, (ii) {fits['ii']['sigma']:.3f} kpc -> "
            f"{t2a['reproduction_label']} / {t2a['population_label']}")

    # --- T2b
    mask5 = np.abs(arr["b"]) >= bmin
    fp_sets = {"fp": t2b_mocks(k, "fp", st, 1.0, True)}
    sig_ii = fits["ii"]["sigma"]
    if abs(sig_ii - st) > P["t2b_second_fp_kpc"]:
        fp_sets["fp2"] = t2b_mocks(k, "fp2", sig_ii, 1.0, True)
    power = t2b_mocks(k, "power", st, P["t2b_q_power"], False)
    need = P["t2b_pass_of_100"]
    checks = {name: S.check_pass(sum(m["label"] == "spherical adequate" for m in ms), len(ms), need)
              for name, ms in fp_sets.items()}
    checks["power"] = S.check_pass(sum(m["label"] == "flattened preferred" for m in power), len(power), need)
    fp_pass = all(checks[nm_]["pass"] for nm_ in fp_sets)
    pw_pass = checks["power"]["pass"]

    def data_step(bm, tag):
        msk = np.abs(arr["b"]) >= bm
        lik = lik_from(arr, "ii", P, k, mask=msk)
        rng = rng_for(P["seed"], f"t2b_data_{tag}")
        s1 = M.step1(lik, rng, n_starts=P["t2b_starts"])
        pw = M.fit_pow(lik, rng, s1["flat"]["theta"], n_starts=P["t2b_starts"])
        nn = int(msk.sum())
        return {"n": nn, "sph": s1["sph"], "flat": s1["flat"], "pow": pw, "two_dlnl": s1["two_dlnl"],
                "profile": s1["profile"], "step1_label": s1["label"],
                "dbic_pow_vs_flat": M.delta_bic(pw["lnl"], s1["flat"]["lnl"], nn),
                "f5": {"sph": M.f5_sph(s1["sph"]["sigma"]), "flat": M.f5_of("flat", s1["flat"]["theta"]),
                       "pow": M.f5_of("pow", pw["theta"])}}

    d5 = store.cached(f"t2b_data_b{bmin}_K{k}", lambda: data_step(bmin, f"b{bmin}"))
    t2b = {"checks": checks, "fp_pass": fp_pass, "power_pass": pw_pass, "data": d5,
           "mock_step1_summary": {nm_: {"labels": _count([m["label"] for m in ms]),
                                        "q_median": float(np.median([m["q"] for m in ms]))}
                                  for nm_, ms in {**fp_sets, "power": power}.items()}}
    step2_pass = step2 = None
    if fp_pass and pw_pass and d5["step1_label"] == "flattened preferred":
        sf, qf = d5["flat"]["theta"]
        s2m = [t2_mock(P, store, f"t2b_step2_{i}", k, gen_sim(P, mi, "t2b_step2", i, nb5, sf, qf, bmin, False),
                       t2b_fit_mock_step2(P, k, rng_for(P["seed"], f"t2b_step2_{i}_starts"))) for i in range(nbm)]
        checks["step2"] = S.check_pass(sum(m["label"] == "flattened Gaussian adequate" for m in s2m), len(s2m), need)
        step2_pass = checks["step2"]["pass"]
        step2 = M.step2_label(d5["dbic_pow_vs_flat"])
        t2b["step2"] = {"reached": True, "label": step2, "dbic": d5["dbic_pow_vs_flat"],
                        "mock_labels": _count([m["label"] for m in s2m])}
    else:
        t2b["step2"] = {"reached": False, "mocks": "not run" if not (fp_pass and pw_pass) else "not reached"}
    shape, f5_model = S.t2b_shape(False, fp_pass, pw_pass, d5["step1_label"], step2_pass, step2)
    if not grid_ok:          # README 4.12 item 4: undetermined until a dated amendment
        shape = S.GRID
    # bootstrap (README 4.4): all three models refitted, 5 starts each
    bres = []
    for j in range(P["t2b_boot"]):
        def go(j=j):
            lik = lik_from(arr, "ii", P, k, mask=mask5)
            w = np.bincount(rng_for(P["seed"], f"t2b_boot_{j}").integers(0, nb5, nb5), minlength=nb5).astype(float)
            rng = rng_for(P["seed"], f"t2b_boot_{j}_starts")
            s1 = M.step1(lik, rng, weights=w, n_starts=P["t2b_starts"], profile=False)
            pw = M.fit_pow(lik, rng, s1["flat"]["theta"], weights=w, n_starts=P["t2b_starts"])
            return {"q": s1["flat"]["theta"][1], "f5": {"sph": M.f5_sph(s1["sph"]["sigma"]),
                                                        "flat": M.f5_of("flat", s1["flat"]["theta"]),
                                                        "pow": M.f5_of("pow", pw["theta"])}}
        bres.append(store.cached(f"t2b_boot_{j}_K{k}", go))
    f5_iv = S.pct_interval([b["f5"][f5_model] for b in bres])
    t2b |= {"shape_label": shape, "f5_model": f5_model, "f5": d5["f5"][f5_model], "f5_interval": f5_iv,
            "f5_label": S.t2b_f5(t2a["population_label"], f5_iv),
            "boot_q_interval": S.pct_interval([b["q"] for b in bres]),
            "boot_f5_intervals": {m: S.pct_interval([b["f5"][m] for b in bres]) for m in M.MODELS}}
    # reported only: latitude variants and the control population (point fits)
    t2b["latitude_variants"] = {str(bm): _brief(store.cached(f"t2b_data_b{bm}_K{k}", lambda bm=bm: data_step(bm, f"b{bm}")))
                                for bm in P["t2b_bmin_variants_deg"]}
    lo_c, hi_c = P["control_mh"]
    ca = t2_arrays(mh, lo_c, hi_c)
    ca = {kk: v[np.abs(ca["b"]) >= bmin] for kk, v in ca.items() if isinstance(v, np.ndarray)}
    ca, csub = subsample(ca, P["ref_max_stars"], P["subsample_seed"])

    def control():
        lik = lik_from(ca, "ii", P, k)
        rng = rng_for(P["seed"], "t2b_control")
        s1 = M.step1(lik, rng, n_starts=P["t2b_starts"])
        pw = M.fit_pow(lik, rng, s1["flat"]["theta"], n_starts=P["t2b_starts"])
        return {"n": int(ca["l"].size), "subsampled": csub, "sph": s1["sph"], "flat": s1["flat"], "pow": pw,
                "two_dlnl": s1["two_dlnl"], "q_interval": s1["profile"]["interval"], "step1_label": s1["label"],
                "dbic_pow_vs_flat": M.delta_bic(pw["lnl"], s1["flat"]["lnl"], int(ca["l"].size))}
    t2b["control"] = store.cached(f"t2b_control_K{k}", control)
    out["t2b"] = t2b
    ctx.log(f"T2b: {shape}; f5 {t2b['f5']:.3f} {f5_iv} -> {t2b['f5_label']}")
    return out


def _count(labels):
    out = {}
    for x in labels:
        out[x] = out.get(x, 0) + 1
    return out


def _brief(d):
    return {"n": d["n"], "sigma_sph": d["sph"]["sigma"], "flat": d["flat"]["theta"], "pow": d["pow"]["theta"],
            "two_dlnl": d["two_dlnl"], "q_interval": d["profile"]["interval"], "step1_label": d["step1_label"],
            "dbic_pow_vs_flat": d["dbic_pow_vs_flat"], "f5": d["f5"]}


def t2_missing_record(lab=S.MISSING):
    return {"t2a": {"reproduction_label": lab, "population_label": lab},
            "t2b": {"shape_label": lab, "f5_label": lab}}


# =============================================================================================
# T3

def t3_samples(joined, P, mh_values=None):
    mhv = joined["mh"].to_numpy(float) if mh_values is None else mh_values
    f = K.ratio(joined["jr"], joined["jphi"], joined["jz"])
    rapo = joined["rapo"].to_numpy(float)
    lo, hi = P["t3_rapo_kpc"]
    prim = (rapo > lo) & (rapo < hi)
    cs, w = P["t3_bin_centers"], P["t3_bin_width"]
    return (K.T3Sample(mhv[prim], f[prim], cs, w), K.T3Sample(mhv, f, cs, w), prim, f)


def t3_w0(P, store, joined, mh, load):
    """README 4.5 known-answer widths (run before the T2a data fit, README 4.10)."""
    if load["L2"]["kin_missing_t3"]:
        return None
    _, _, prim, f = t3_samples(joined, P)
    cs, w = P["t3_bin_centers"], P["t3_bin_width"]
    mhv = joined["mh"].to_numpy(float)
    have_err = "mh_err" in mh.columns
    w0 = {}
    models = ([("errors", mh["mh_err"].to_numpy(float)[joined["mh_row"].to_numpy()][prim])] if have_err else [])
    models += [(f"{b:g} dex", b) for b in P["t3_w0_blur_dex"]]
    for name, err in models:
        w0[name] = store.cached(f"t3_w0_{name}", lambda err=err, name=name: K.w0_mocks(
            mhv[prim], f[prim], rng_for(P["seed"], f"t3_w0_{name}"), n_mocks=P["t3_w0_mocks"], err=err,
            centers=cs, width=w, n_boot=P["t3_boot"]))
    primary_w0 = "errors" if have_err else f"{P['t3_w0_blur_dex'][0]:g} dex"
    return {"w0": w0, "primary": primary_w0}


def run_t3(P, store, ctx, joined, load, w0res):
    if load["L2"]["kin_missing_t3"]:
        return {"missing": load["L2"]["kin_missing_t3"], "a_label": S.MISSING, "b_label": S.MISSING,
                "c_label": S.MISSING}
    prim_s, all_s, prim, f = t3_samples(joined, P)
    mhv = joined["mh"].to_numpy(float)
    w0, primary_w0 = w0res["w0"], w0res["primary"]
    w0v = w0[primary_w0]["w0"]
    prim_res = store.cached("t3_primary", lambda: K.t3_full(prim_s, rng_for(P["seed"], "t3_primary"),
                                                             P["t3_boot"], P["t3_boot"], w0v, P["t3_delta"]))
    all_res = store.cached("t3_all", lambda: K.t3_full(all_s, rng_for(P["seed"], "t3_all"),
                                                        P["t3_boot"], P["t3_boot"], w0v, P["t3_delta"]))
    out = {"primary": prim_res, "all_rapo": all_res, "w0": w0, "primary_w0": primary_w0,
           "a_label": prim_res["a_label"], "b_label": prim_res["b_label"], "c_label": prim_res["c_label"],
           "jphi_sign_flipped": load["L5"]["jphi_flipped"]}
    # v_phi (reported only)
    rich = mhv > -0.5
    vf = K.signed_like_disc(K.vphi_from_file(joined), rich)
    sel_a = prim & (mhv < -2.0)
    sel_b = prim & (mhv > -1.1) & (mhv < -0.9)
    vrep = {}
    if vf is not None:
        vrep["file"] = {"a_mean": _nanmean(vf[sel_a]), "b_mean": _nanmean(vf[sel_b])}
    for r0 in P["t3_R0_variants_kpc"]:
        sub = joined.loc[sel_a | sel_b]
        v = K.vphi_heliocentric(sub, r0, zp=P["plx_zp_mas"])
        if v is None:
            vrep[f"R0_{r0}"] = "not computed (no heliocentric observables in the kinematics file)"
            continue
        ma = (sub["mh"].to_numpy(float) < -2.0)
        vrep[f"R0_{r0}"] = {"a_mean": _nanmean(v[ma]), "b_mean": _nanmean(v[~ma])}
    out["vphi"] = vrep or "not computed (no velocities in the kinematics file)"
    ctx.log(f"T3: (a) {out['a_label']}, (b) {out['b_label']}, (c) {out['c_label']} (w0 {w0v:.3f})")
    return out


def _nanmean(x):
    x = np.asarray(x, float)
    return float(np.nanmean(x)) if np.isfinite(x).any() else None


# =============================================================================================
# T5, T6

def run_t5(P, joined, load):
    if load["L2"]["kin_missing_t5"]:
        return {"missing": load["L2"]["kin_missing_t5"], "g_label": S.MISSING, "a5_label": S.MISSING}
    mhv = joined["mh"].to_numpy(float)
    ecc, rapo = joined["ecc"].to_numpy(float), joined["rapo"].to_numpy(float)
    res = {}
    for name, (lo, hi) in {"primary": (-99.0, -1.5), **{f"{a}_{b}": (a, b) for a, b in P["t5_variants"]}}.items():
        m = (mhv > lo) & (mhv < hi)
        res[name] = K.t5_fractions(ecc[m], rapo[m], rng_for(P["seed"], f"t5_{name}"), P["t5_boot"])
        res[name]["mh_range"] = [lo, hi]
    return {"samples": res, "g_label": res["primary"]["g_label"], "a5_label": res["primary"]["a5_label"],
            "g": res["primary"].get("g"), "note": "R22's RVS, plx/err >= 5 and dv_RVS < 5 km/s selection favours "
            "the near side of the Centre and biases R_apo (README 4.7)"}


def f_bright(mh, P):
    need = ("parallax", "parallax_error", "g", "bp_rp")
    if not all(c in mh.columns for c in need):
        return None
    s = mh[mh["mh"] < -1.5]
    pc = s["parallax"].to_numpy(float) + P["plx_zp_mas"]
    snr = pc / s["parallax_error"].to_numpy(float)
    m = np.isfinite(snr) & (snr > P["t6_snr_min"])
    mg = s["g"].to_numpy(float)[m] - 1.5 * (s["bp_rp"].to_numpy(float)[m] - 1.0) + 5.0 * np.log10(pc[m] / 100.0)
    return {"f_bright": float(np.mean(mg < P["t6_mg_max"])) if m.any() else None, "n_used": int(m.sum()),
            "note": "the plx/err > 5 cut favours nearer stars (README 4.8)"}


R22_M_GIANT, R22_F = 800.0, 2.5      # R22's own choices (README 4.8), not knobs


def mass_r22(n, P=None):
    return n * R22_M_GIANT * 1.0 * R22_F


def run_t6(P, counts, t5, fb):
    n = counts["lt_m1p5"]
    g = t5.get("g")
    ns = {"N(<-1.5)": n}
    if g is not None:
        ns["N(<-1.5) x (1 - g)"] = n * (1.0 - g)
    fbs = {"1 (R22)": 1.0}
    if fb and fb["f_bright"] is not None:
        fbs["computed"] = fb["f_bright"]
    rows = []
    for nk, nv in ns.items():
        for m in P["t6_m_giant"]:
            for fk, fv in fbs.items():
                for f in P["t6_f"]:
                    rows.append({"N": nk, "N_value": nv, "m_giant": m, "f_bright": fk, "f_bright_value": fv,
                                 "f": f, "mass_msun": nv * m * fv * f})
    mr = mass_r22(n, P)
    return {"table": rows, "f_bright": fb or "not computed", "r22_choices_mass": mr,
            "r22_choices_at_least_5e7": bool(mr >= P["t6_target_msun"])}


# =============================================================================================
# T4

def t4_variants(P, mh):
    """Variant [M/H] arrays over the metallicity file (with a keep mask). README 4.6."""
    base = mh["mh"].to_numpy(float)
    keep_all = np.ones(base.size, bool)
    out = [("shift +0.1", base + P["t4_shift_dex"], keep_all, None),
           ("shift -0.1", base - P["t4_shift_dex"], keep_all, None)]
    for s in P["t4_noise_dex"]:
        for r in range(P["t4_realisations"]):
            rng = rng_for(P["seed"], f"t4_noise_{s}_{r}")
            out.append((f"noise {s:g}", base + rng.normal(0.0, s, base.size), keep_all, r))
    if "teff" in mh.columns and "logg" in mh.columns:
        te, lg = mh["teff"].to_numpy(float), mh["logg"].to_numpy(float)
        jb = np.floor(base / P["t4_bin_dex"]).astype(int)
        for lo, hi in P["t4_trim_pct"]:
            keep = np.zeros(base.size, bool)
            for j in np.unique(jb[np.isfinite(base)]):
                m = jb == j
                ok = m.copy()
                for x in (te, lg):
                    a, b = np.nanpercentile(x[m], [lo, hi])
                    ok &= (x >= a) & (x <= b)
                keep |= ok
            out.append((f"trim {lo:g}-{hi:g}", base, keep, None))
    return out


def t4_elasticity(base, shifted_plus, shifted_minus, cuts=(-2.0, -1.5, -1.0), step=0.1):
    rows = {}
    for c in cuts:
        n0 = np.sum(base < c)
        npl, nmi = np.sum(shifted_plus < c), np.sum(shifted_minus < c)
        slope = (np.log10(max(np.sum(base < c + 0.2), 1)) - np.log10(max(np.sum(base < c - 0.2), 1))) / 0.4
        rows[str(c)] = {"n": int(n0), "dlnN_plus": float(np.log(npl / n0)) if n0 and npl else None,
                        "dlnN_minus": float(np.log(nmi / n0)) if n0 and nmi else None,
                        "predicted_plus": float(-step * np.log(10) * slope),
                        "predicted_minus": float(step * np.log(10) * slope), "slope_log10N_per_dex": float(slope)}
    return rows


def run_t4(P, store, ctx, mh, joined, base, t2_ok, k, grid_ok=True):
    runs = []
    rows = joined["mh_row"].to_numpy()
    for name, mhv, keep, r in t4_variants(P, mh):
        def go(name=name, mhv=mhv, keep=keep, r=r):
            rec = {"variant": name, "realisation": r}
            m_keep = mhv[keep]
            rec["counts"] = D.t1_counts(m_keep)
            rec["mass"] = mass_r22(rec["counts"]["lt_m1p5"], P)
            if t2_ok:
                df = mh.loc[keep].copy()
                df["mh"] = m_keep
                lo, hi = P["t2_mh_range"]
                arr = t2_arrays(df, lo, hi)
                for v in ("i", "ii"):
                    rec[f"sigma_{v}"] = M.fit_sigma(lik_from(arr, v, P, k), bounds=tuple(P["sigma_bounds_kpc"]))["sigma"]
            if base.get("t3_ok"):
                jk = keep[rows]
                jm = mhv[rows]
                sub = joined.loc[jk]
                prim_s = t3_samples(sub, P, jm[jk])[0]
                rec |= K.t3_ab(prim_s, rng_for(P["seed"], f"t4_t3_{name}_{r}"), P["t4_boot"], P["t3_delta"])
            return rec
        runs.append(store.cached(f"t4_{name}_{r}_K{k}".replace(" ", "_"), go))
    # aggregate per variant (README 4.6: medians and the 6-of-10 rule for the noise variants)
    variants = {}
    for name in dict.fromkeys(r_["variant"] for r_ in runs):
        rr = [x for x in runs if x["variant"] == name]
        v = {"n_realisations": len(rr), "mass": float(np.median([x["mass"] for x in rr])),
             "counts_median": {kk: float(np.median([x["counts"][kk] for x in rr])) for kk in rr[0]["counts"]}}
        if t2_ok:
            for s in ("i", "ii"):
                v[f"sigma_{s}"] = float(np.median([x[f"sigma_{s}"] for x in rr]))
        if base.get("t3_ok"):
            for kk in ("a", "b"):
                labs = [x[f"{kk}_label"] for x in rr]
                v[f"{kk}_labels"] = _count(labs)
                if len(rr) > 1:
                    v[f"{kk}_changed"] = sum(lab != base[f"{kk}_label"] for lab in labs) >= 6 * len(rr) / 10
                else:
                    v[f"{kk}_label"] = labs[0]
        variants[name] = v
    sigma_skipped = not t2_ok
    bl = {"sigma_ii": base.get("sigma_ii"), "a_label": base.get("a_label"), "b_label": base.get("b_label"),
          "mass": base["mass"]}
    check_vars = {}
    for nm_, v in variants.items():
        cv = dict(v)
        if not base.get("t3_ok"):
            cv["a_changed"] = cv["b_changed"] = False
        check_vars[nm_] = cv
    label, broken = S.t4_label(bl, check_vars, sigma_skipped, grid_ok=grid_ok)
    plus = next(x for x in runs if x["variant"] == "shift +0.1")
    flags = {}
    n0 = base["counts"]
    for s in P["t4_noise_dex"][:1]:
        med = variants[f"noise {s:g}"]["counts_median"]
        flags = {kk: bool(n0[kk] > 0 and (med[kk] / n0[kk] > 2 or med[kk] / n0[kk] < 0.5))
                 for kk in ("lt_m2", "lt_m1p5", "m2p7_to_m1p5", "lt_m1")}
    base_mh = mh["mh"].to_numpy(float)
    el = t4_elasticity(base_mh, base_mh + P["t4_shift_dex"], base_mh - P["t4_shift_dex"])
    ctx.log(f"T4: {label} {broken}")
    return {"label": label, "broken": [list(b) for b in broken], "variants": variants,
            "sigma_condition_skipped": sigma_skipped,
            "sigma_condition": "skipped (T2 data not in the files)" if sigma_skipped else (
                "evaluated" if grid_ok else S.GRID), "elasticity": el,
            "dominated_by_scatter_from_above": flags, "baseline": bl,
            "trim_computed": any(x["variant"].startswith("trim") for x in runs),
            "plus_counts": plus["counts"]}


# =============================================================================================
# main

def main(ctx):
    P = dict(PARAMS)
    parts = set(P["parts"])
    formal = is_formal_run(ctx)
    if formal:
        low = {k: P[k] for k, v in FLOORS.items() if P[k] < v}
        if low:
            raise ValueError(f"formal run below the floors of README 4.10: {low}")
        off = {k: P[k] for k, v in FORMAL_FIXED.items() if P[k] != v}
        if off:
            raise ValueError(f"a formal run needs all parts and the pre-registered sizes: {off}")
    paths = fetch_files(ctx, P)
    try:
        mh, kin, joined, load = load_and_check(paths, P, ctx)
    except D.StopRun as e:
        rec = e.args[1] if len(e.args) > 1 else {}
        summary = {"status": f"stopped at load: {e.args[0]}", "params": P}
        ctx.save("load", rec | {"stopped": e.args[0], "params": P})
        ctx.save("summary", summary)
        ctx.log(f"STOPPED: {e.args[0]}")
        return summary
    t2_ok = not load["L2"]["t2_columns_missing"]
    lo, hi = P["t2_mh_range"]
    n_t2 = int(((mh["mh"] >= lo) & (mh["mh"] < hi)).sum())
    timing = timing_estimate(P, n_t2, ctx)
    key = run_key(P, [load["L1"][k]["md5"] for k in FILES])
    stop = float(P["stop_after_hours"]) * 3600 if P["stop_after_hours"] else None
    store = C.Store(checkpoint_root(_cache_dir(), P, ctx), key, stop)
    ctx.log(f"checkpoints ({'formal run' if formal else 'exploration'}): {store.dir}")
    try:
        files = pipeline(ctx, P, parts, store, mh, joined, load, t2_ok)
    except C.Paused as e:
        ctx.log(f"PAUSED: {e}")
        if formal:
            ctx.record_suffix = "_paused"
        return {"status": "paused", "reason": str(e), "checkpoints": str(store.dir), "timing": timing}
    files["summary"] |= {"timing": timing, "checkpoints": str(store.dir)}
    ctx.save("load", load | {"params": P})
    for name, obj in files.items():
        ctx.save(name, obj | {"params": P})
    if formal:
        finish_checkpoints(store, ctx)
        remove_paused_records(ctx)
    else:
        ctx.log(f"exploration checkpoints kept in {store.dir} (delete them when done)")
    return files["summary"]


def pipeline(ctx, P, parts, store, mh, joined, load, t2_ok):
    files = {}
    need_t3 = "t3" in parts or "t4" in parts
    early = {}

    def before_data():
        # README 4.10 order: ... T2a/T2b mocks, T3 w0 mocks -> T1 -> T2a data fit
        if need_t3:
            early["w0"] = t3_w0(P, store, joined, mh, load)
        counts = D.t1_counts(mh["mh"].to_numpy(float))
        early["counts"] = counts
        early["t1"] = D.t1_labels(counts) | {"counts": counts}
        ctx.log(f"T1: {counts} -> {early['t1']['summary']}")

    if t2_ok and ("t2" in parts or "t4" in parts):
        t2 = run_t2(P, store, ctx, mh, load, before_data)
        files["t2"] = t2
    else:
        before_data()
        if t2_ok:
            t2 = t2_missing_record("not run (parts)")
        else:
            t2 = t2_missing_record()
            files["t2"] = t2
    counts, t1 = early["counts"], early["t1"]
    files["t1"] = t1
    t3 = run_t3(P, store, ctx, joined, load, early.get("w0")) if need_t3 else None
    if t3 is not None:
        files["t3"] = t3
    t5 = run_t5(P, joined, load)
    files["t5"] = t5
    fb = f_bright(mh, P) if t2_ok else None
    files["t6"] = run_t6(P, counts, t5, fb)
    conv = t2["grid_check"]["converged"] if (t2_ok and "grid_check" in t2) else {"i": True, "ii": True}
    grid_ok = bool(conv["ii"])        # version (ii) drives T2a's population label, T2b and T4's sigma
    t4 = None
    if "t4" in parts:
        base = {"counts": counts, "mass": mass_r22(counts["lt_m1p5"], P),
                "sigma_ii": t2["t2a"]["fits"]["ii"]["sigma"] if t2_ok else None,
                "t3_ok": t3 is not None and "missing" not in t3,
                "a_label": t3["a_label"] if t3 else None, "b_label": t3["b_label"] if t3 else None}
        k = t2["grid_check"]["nodes"] if t2_ok else int(P["grid_nodes"])
        t4 = run_t4(P, store, ctx, mh, joined, base, t2_ok, k, grid_ok=grid_ok)
        files["t4"] = t4
    # reason codes (README 4.12 item 4); the web page maps them to English and Chinese text
    pending = [f"grid_not_converged_{v}" for v in ("i", "ii") if not conv[v]]
    rep = S.reading_reproduction(t1["summary"], t2["t2a"]["reproduction_label"],
                                 t3["a_label"] if t3 else "undetermined", t3["b_label"] if t3 else "undetermined")
    rob = S.reading_robustness(t2["t2a"]["population_label"], t2["t2b"]["f5_label"],
                               t4["label"] if t4 else "undetermined", t5["g_label"], t5["a5_label"])
    files["summary"] = {
        "status": "complete", "parts": sorted(parts),
        "labels": {"T1": t1["summary"], "T1_abstract_fraction": t1["abstract_fraction_label"],
                   "T2a_reproduction": t2["t2a"]["reproduction_label"], "T2a_population": t2["t2a"]["population_label"],
                   "T2b_shape": t2["t2b"]["shape_label"], "T2b_f5": t2["t2b"]["f5_label"],
                   "T3a": t3["a_label"] if t3 else None, "T3b": t3["b_label"] if t3 else None,
                   "T3c": t3["c_label"] if t3 else None, "T4": t4["label"] if t4 else None,
                   "T5_g": t5["g_label"], "T5_a5": t5["a5_label"],
                   "T6_r22_at_least_5e7": files["t6"]["r22_choices_at_least_5e7"]},
        "reading_reproduction": {"label": rep[0], "tests": rep[1], "pending_amendment": bool(pending)},
        "reading_robustness": {"label": rob[0], "tests": rob[1], "pending_amendment": bool(pending)},
        "pending_amendment": pending,
    }
    return files


def run_key(P, data_ids):
    """Checkpoint key: the effective PARAMS minus run-only keys, the helper modules and run.py without
    its PARAMS literal, and the data checksums (README section 8: resetting first_download keeps it)."""
    return C.checkpoint_key({k: v for k, v in P.items() if k not in _RUN_ONLY},
                            [HERE / f for f in ("data012.py", "model012.py", "kin012.py", "stats012.py",
                                                "store012.py")], data_ids, params_source=HERE / "run.py")


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


def finish_checkpoints(store, ctx):
    """Once every result is written, the run's checkpoint folder is deleted, and so are stale key
    folders directly under the formal root; explore/ is left alone."""
    import shutil
    size = store.size_bytes()
    ok = store.remove_all()
    ctx.log(f"checkpoints {'removed' if ok else 'could NOT be removed'}: {store.dir} ({size / 1024 ** 2:.1f} MB)")
    root = store.dir.parent
    if root.is_dir():
        for d in sorted(root.iterdir()):
            if d.is_dir() and d.name != "explore" and re.fullmatch(r"[0-9a-f]{20}", d.name):
                shutil.rmtree(d, ignore_errors=True)
    return ok


def remove_paused_records(ctx):
    """A completed formal run supersedes the records of an earlier paused attempt."""
    removed = []
    for name in ("provenance_paused.json", "run_info_paused.json"):
        p = Path(ctx.results) / name
        if p.exists():
            p.unlink()
            removed.append(name)
    return removed
