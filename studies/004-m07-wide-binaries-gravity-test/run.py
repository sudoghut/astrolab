"""M7: wide binaries, Newton or MOND at low acceleration (pre-registration: README sections 1-4).

Run with:      python -m astrolab run 004-m07-wide-binaries-gravity-test
Explore with:  python -m astrolab explore 004-m07-wide-binaries-gravity-test --tag <topic> --set KEY=VALUE

Steps (README section 3, two-step fetch for blinding):
  A  velocity-free: per region, count then fetch candidate pairs (A1) and neighbour counts (A2);
     saves only counts, byte estimates and the HR-band constant c (results/step_a.json).
  B  after the dated pre-registration commit: velocities for the pairs (B1), then the analysis.
"""
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd

import queries as Q
import wb

# Tunable knobs (AGENTS.md section 2). Read inside main() and passed on as arguments.
PARAMS = {
    "step": "B",                       # "A" (velocity-free) or "B" (after the pre-registration commit)
    "parent": "parallax > 6.6667 AND parallax_over_error > 40",
    # main degrouping uses relaxed neighbours (C26 section 3.2.2); C25-only is a diagnostic
    "neighbour": ("parallax_over_error > 5 AND phot_g_mean_flux_over_error > 5"
                  " AND parallax + 3 * parallax_error > 6.6667"),
    "neighbour_c25": ("parallax_over_error > 40 AND phot_g_mean_flux_over_error > 5"
                      " AND parallax + 3 * parallax_error > 6.6667"),
    "near_plx": 100.0, "near_b": "parallax + 3 * parallax_error > 80",
    "vcap_kms": None,                  # no velocity condition in A1 (README section 3)
    "max_rows": 50000,
    "bytes_a1": 600, "bytes_a2": 40, "bytes_a3": 24, "bytes_b1": 600,   # README section 3 estimates
    "budget_bytes": 200 * 1024 ** 2,
    "workers": 4,
    "region_limit": None,              # exploration only: run the first N regions
    # step B (README sections 2 and 4); fixed by the pre-registration
    "hr_c": 1.590861779261529,         # HR constant from step A (README 4.5, dated note 2026-11-16)
    "a0": 1.2e-10, "gne_over_a0": 1.184, "mg_sun": 4.67,
    "edges": [0.1057, 0.2307, 0.5088, 1.0275, 2.0902],
    "min_per_bin": 15, "n_boot": 2000, "boot_seed": 0, "L_threshold": 100.0,
    "d_max_pc": 130.0, "rsky_min_au": 1000.0, "rsky_max_au": 30000.0, "ruwe_max": 1.25,
    "drv_max": 10.0, "sig_vt_max": 0.1, "vt_max": 2.5,
    # run mode: "r2" (the 2026-11-16 study, unchanged) or "r5" (README 2.1, T-034). The "mode" and
    # "r5_*" keys are not part of the R2 parameters and are not saved with the R2 results.
    "mode": "r2",
    "r5_d_max_pc": 250.0, "r5_rsky_min_au": 300.0, "r5_n_boot": 10000, "r5_seed": 0,
    "r5_bytes_n1": 720, "r5_bytes_n2": 40, "r5_bytes_n3": 24, "r5_bytes_n4": 600,
    "r5_run_c25": True,                # variant V9 (N2-C25, restricted form only)
    "r5_stop_after_g1b": False,        # True: fetch N1-N3, evaluate G1b, save, and stop before N4
}


def _max_bytes():
    from astrolab import config
    return config.HTTP_MAX_BYTES


def _same(n, df, label):
    if len(df) != n:
        raise RuntimeError(f"{label}: fetched {len(df)} rows but the server count was {n}; stop")


def _count(ctx, q, label):
    df = ctx.tap(q, "gaia", label=f"count {label}", max_rows=2, mode="async", release="Gaia DR3")
    return int(df["n"].iloc[0])


def _regions(P):
    plan = wb.strip_plan()
    regs = [("r%03d" % k, r, False) for k, r in enumerate(plan)]
    regs.append(("near", dict(ra0=0.0, ra1=360.0, dec0=-90.0, dec1=90.0, bra0=0.0, bra1=360.0,
                              bdec0=-90.0, bdec1=90.0), True))
    if P["region_limit"]:
        regs = regs[: int(P["region_limit"])]
    return regs


class BudgetStop(RuntimeError):
    """The cumulative estimate would exceed the study budget (stop and ask the user)."""


class Budget:
    """Cumulative byte estimate shared by the worker threads; checked BEFORE each fetch."""

    def __init__(self, limit):
        self.limit, self.used, self.lock = limit, 0, threading.Lock()

    def reserve(self, nbytes, what):
        with self.lock:
            if self.used + nbytes > self.limit:
                raise BudgetStop(f"{what}: cumulative estimate {(self.used + nbytes) / 1e6:.1f} MB exceeds "
                                   "the study budget; stop and ask the user (README section 3)")
            self.used += nbytes


def _split(ctx, P, name, r, near, budget, fn, *extra):
    """README section 3: a region over the row cap is split in two in right ascension and counted
    again (recursively). Returns the summed count and the concatenated rows."""
    if near:
        raise RuntimeError(f"{name}: the near-star query exceeded the row cap, which README section 3 rules out; stop")
    if r["ra1"] - r["ra0"] < 0.1:
        raise RuntimeError(f"{name}: still over the row cap at 0.1 deg; stop and ask the user")
    parts = wb.split_region(r)
    ns, dfs = 0, []
    for i, sub in enumerate(parts):
        n, df = fn(ctx, P, f"{name}.{i}", sub, near, *extra, budget) if extra else fn(ctx, P, f"{name}.{i}", sub, near, budget)
        ns += n
        dfs.append(df)
    return ns, pd.concat(dfs, ignore_index=True)


def _a1(ctx, P, name, r, near, budget):
    parent = P["parent"]
    qc = Q.pair_query(r, parent, P["vcap_kms"], "COUNT(*) AS n", near=near) if not near else \
        Q.pair_query(r, parent, P["vcap_kms"], "COUNT(*) AS n", near=True).replace(
            f"FROM gaiadr3.gaia_source WHERE {parent}) AS b",
            f"FROM gaiadr3.gaia_source WHERE {parent} AND {P['near_b']}) AS b")
    n = _count(ctx, qc, f"A1 {name}")
    if n >= P["max_rows"]:
        return _split(ctx, P, name, r, near, budget, _a1)
    if n * P["bytes_a1"] > _max_bytes():
        return _split(ctx, P, name, r, near, budget, _a1)
    budget.reserve(n * P["bytes_a1"], f"A1 {name}")
    q = qc.replace("SELECT COUNT(*) AS n", "SELECT " + Q.a1_select(), 1)
    df = ctx.tap(q, "gaia", label=f"A1 {name}", max_rows=P["max_rows"], mode="async", release="Gaia DR3")
    _same(n, df, f"A1 {name}")
    return n, df


def _a2(ctx, P, name, r, near, neighbour_key, budget):
    nb = P[neighbour_key]
    if near:
        nb = f"{nb} AND {P['near_b']}"
    qc = Q.neighbour_query(r, P["parent"], nb, "count", near=near)
    n = _count(ctx, qc, f"A2 {name}")
    if n >= P["max_rows"]:
        return _split(ctx, P, name, r, near, budget, _a2, neighbour_key)
    budget.reserve(n * P["bytes_a2"], f"A2 {name}")
    q = Q.neighbour_query(r, P["parent"], nb, "rows", near=near)
    df = ctx.tap(q, "gaia", label=f"A2 {name}", max_rows=P["max_rows"], mode="async", release="Gaia DR3")
    _same(n, df, f"A2 {name}")
    return n, df


def _a3(ctx, P, name, r, near, budget):
    qc = Q.flame_query(r, P["parent"], "count", near=near)
    n = _count(ctx, qc, f"A3 {name}")
    if n >= P["max_rows"]:
        return _split(ctx, P, name, r, near, budget, _a3)
    budget.reserve(n * P["bytes_a3"], f"A3 {name}")
    df = ctx.tap(Q.flame_query(r, P["parent"], "rows", near=near), "gaia", label=f"A3 {name}",
                 max_rows=P["max_rows"], mode="async", release="Gaia DR3")
    _same(n, df, f"A3 {name}")
    return n, df


def step_a(ctx, P):
    regs = _regions(P)
    t0 = time.time()
    counts = {}
    budget = Budget(P["budget_bytes"])

    def one(item):
        name, r, near = item
        n1, d1 = _a1(ctx, P, name, r, near, budget)
        n2, d2 = _a2(ctx, P, name, r, near, "neighbour", budget)
        n3, d3 = _a3(ctx, P, name, r, near, budget)
        return name, n1, d1, n2, d2, n3, d3

    a1_parts, a2_parts, a3_parts = [], [], []
    with ThreadPoolExecutor(max_workers=int(P["workers"])) as ex:
        for name, n1, d1, n2, d2, n3, d3 in ex.map(one, regs):
            counts[name] = {"A1": n1, "A2": n2, "A3": n3}
            a1_parts.append(d1)
            a2_parts.append(d2)
            a3_parts.append(d3)
    a1 = pd.concat(a1_parts, ignore_index=True) if a1_parts else pd.DataFrame()
    a2 = pd.concat(a2_parts, ignore_index=True) if a2_parts else pd.DataFrame()
    if len(a1):
        keep = wb.canonical_pairs(a1["source_id_a"].to_numpy(), a1["source_id_b"].to_numpy())
        a1 = a1.iloc[keep].reset_index(drop=True)
    c_band = hr_constant(a1)
    out = {"step": "A", "regions": len(regs), "n_pairs_a1": int(len(a1)), "n_stars_a2": int(len(a2)),
           "n_flame_a3": int(sum(len(d) for d in a3_parts)),
           "est_bytes": int(budget.used), "hr_constant": c_band, "seconds": time.time() - t0,
           "counts_per_region": counts}
    ctx.save("step_a", out)
    return out


def hr_constant(a1):
    """README section 4.5: c from deduplicated A1 stars (own parallax), velocity-free."""
    if not len(a1):
        return {"c": None, "n": 0, "window": None}
    rows = []
    for s in ("a", "b"):
        rows.append(pd.DataFrame({"source_id": a1[f"source_id_{s}"], "parallax": a1[f"parallax_{s}"],
                                  "g": a1[f"phot_g_mean_mag_{s}"], "bp_rp": a1[f"bp_rp_{s}"],
                                  "ruwe": a1[f"ruwe_{s}"]}))
    st = pd.concat(rows).drop_duplicates("source_id")
    st = st[st["bp_rp"].notna() & (st["ruwe"] < 1.25) & (st["parallax"] > 7.6923)]
    mg = st["g"] + 5 * np.log10(st["parallax"] / 100.0)
    for w in (0.05, 0.15):
        sel = (st["bp_rp"] - 1.8).abs() < w
        if int(sel.sum()) >= 30:
            c = float(np.median(mg[sel] - 3.3 * st["bp_rp"][sel]) - 0.4)
            return {"c": c, "n": int(sel.sum()), "window": w}
    return {"c": None, "n": int(((st["bp_rp"] - 1.8).abs() < 0.15).sum()), "window": None}


# ---------------------------------------------------------------- step B
def _b1(ctx, P, name, r, near, budget):
    parent = P["parent"]
    extra = Q.b1_extra(P["rsky_max_au"] / 1000.0)
    qc = Q.pair_query(r, parent, None, "COUNT(*) AS n", near=near, extra_where=extra)
    if near:
        qc = qc.replace(f"FROM gaiadr3.gaia_source WHERE {parent}) AS b",
                        f"FROM gaiadr3.gaia_source WHERE {parent} AND {P['near_b']}) AS b")
    n = _count(ctx, qc, f"B1 {name}")
    if n >= P["max_rows"] or n * P["bytes_b1"] > _max_bytes():
        return _split(ctx, P, name, r, near, budget, _b1)
    budget.reserve(n * P["bytes_b1"], f"B1 {name}")
    q = qc.replace("SELECT COUNT(*) AS n", "SELECT " + Q.b1_select(), 1)
    df = ctx.tap(q, "gaia", label=f"B1 {name}", max_rows=P["max_rows"], mode="async", release="Gaia DR3")
    _same(n, df, f"B1 {name}")
    return n, df


def gather(ctx, P):
    """Step A tables (cache hits) and B1 velocities, merged per pair."""
    import json
    from pathlib import Path
    regs = _regions(P)
    free = Budget(float("inf"))                 # step A rows are already counted in step_a.json
    sa = json.loads((Path(__file__).parent / "results" / "step_a.json").read_text(encoding="utf-8"))
    budget = Budget(P["budget_bytes"])
    budget.used = int(sa["est_bytes"])

    known = sa.get("counts_per_region", {})

    def one(item):
        name, r, near = item
        n1, d1 = _a1(ctx, P, name, r, near, free)
        n2, d2 = _a2(ctx, P, name, r, near, "neighbour", free)
        n3, d3 = _a3(ctx, P, name, r, near, free)
        if name in known and known[name] != {"A1": n1, "A2": n2, "A3": n3}:
            raise RuntimeError(f"{name}: step A counts changed since step_a.json; stop (README section 3)")
        _, db = _b1(ctx, P, name, r, near, budget)
        return d1, d2, d3, db

    parts = [[], [], [], []]
    with ThreadPoolExecutor(max_workers=int(P["workers"])) as ex:
        for res in ex.map(one, regs):
            for k in range(4):
                parts[k].append(res[k])
    a1, a2, a3, b1 = (pd.concat(x, ignore_index=True) if x else pd.DataFrame() for x in parts)
    keep = wb.canonical_pairs(a1["source_id_a"].to_numpy(), a1["source_id_b"].to_numpy())
    a1 = a1.iloc[keep].reset_index(drop=True)
    keep_b = wb.canonical_pairs(b1["source_id_a"].to_numpy(), b1["source_id_b"].to_numpy())
    b1 = b1.iloc[keep_b].reset_index(drop=True)
    pairs = a1.merge(b1, on=["source_id_a", "source_id_b"], how="inner")
    if len(pairs) != len(b1):
        raise RuntimeError(f"{len(b1) - len(pairs)} B1 pairs are missing from A1; stop")
    ctx.log(f"A1 pairs {len(a1)}, B1 pairs {len(b1)}, merged {len(pairs)}")
    return pairs, a2, a3, budget.used


def _star(r, s):
    return dict(p=r[f"parallax_{s}"], pmra=r[f"pmra_{s}"], pmdec=r[f"pmdec_{s}"], e_p=r[f"parallax_error_{s}"],
                e_pmra=r[f"pmra_error_{s}"], e_pmdec=r[f"pmdec_error_{s}"], c_ppa=r[f"parallax_pmra_corr_{s}"],
                c_ppd=r[f"parallax_pmdec_corr_{s}"], c_pad=r[f"pmra_pmdec_corr_{s}"])


def build_sample(pairs, a2, a3, P, variant, trace=None):
    """Apply README section 4 to the merged pairs; returns a DataFrame with x, vt, sig_vt.
    If `trace` is a dict, the number of pairs left after each cut (in section 4.5 order) is recorded."""
    v = dict(variant)
    df = pairs.copy()

    def note(label):
        if trace is not None:
            trace[label] = int(len(df))

    note("merged_pairs")
    if not v.get("no_degroup"):          # each member's only neighbour is its partner (A2)
        if a2["source_id"].duplicated().any():
            raise RuntimeError("A2 has duplicate source_id rows; stop")
        nb = {int(s): (int(n), int(f)) for s, n, f in
              zip(a2["source_id"], a2["n"], a2["first_neighbour"])}       # exact integer ids

        def single(sid, partner):
            v = nb.get(int(sid))
            return v is not None and v[0] == 1 and v[1] == int(partner)
        ok = [single(a, b) and single(b, a) for a, b in zip(df["source_id_a"], df["source_id_b"])]
        df = df[np.array(ok, dtype=bool)]
    note("degroup")
    pbar, _, _ = wb.weighted_parallax(df["parallax_a"].to_numpy(), df["parallax_error_a"].to_numpy(),
                                      df["parallax_b"].to_numpy(), df["parallax_error_b"].to_numpy())
    df = df.assign(pbar=pbar)
    df = df[df["pbar"] > 1000.0 / v.get("d_max_pc", P["d_max_pc"])]
    if v.get("pbar_max") is not None:     # R5 V14: the 150-250 pc shell only
        df = df[df["pbar"] <= v["pbar_max"]]
    note("distance")
    rsky = wb.sky_separation_au(df["ra_a"].to_numpy(), df["dec_a"].to_numpy(), df["ra_b"].to_numpy(),
                                df["dec_b"].to_numpy(), df["pbar"].to_numpy())
    df = df.assign(rsky=np.asarray(rsky))
    df = df[(df["rsky"] >= P["rsky_min_au"]) & (df["rsky"] <= P["rsky_max_au"])]
    if v.get("theta_min_arcsec") is not None:     # R5 V3: angular floor (theta = r_sky * pbar / 1000)
        df = df[df["rsky"] * df["pbar"] / 1000.0 >= v["theta_min_arcsec"]]
    note("r_sky")
    if v.get("parallax_snr_min"):
        df = df[(df["parallax_a"] / df["parallax_error_a"] > v["parallax_snr_min"])
                & (df["parallax_b"] / df["parallax_error_b"] > v["parallax_snr_min"])]
    df = df[(df["ruwe_a"] < P["ruwe_max"]) & (df["ruwe_b"] < P["ruwe_max"])]
    note("ruwe")
    if v.get("ipd_zero"):
        df = df[(df["ipd_frac_multi_peak_a"] == 0) & (df["ipd_frac_multi_peak_b"] == 0)]
    if not v.get("no_hr"):
        c = P["hr_c"] + v.get("c_shift", 0.0)
        for s in ("a", "b"):
            x = df[f"bp_rp_{s}"]
            mg = df[f"phot_g_mean_mag_{s}"] + 5 * np.log10(df["pbar"] / 100.0)
            df = df[(x > 0.5) & (x < 3.5) & (mg > 4) & (mg < 14) & (mg > 3.3 * x + c) & (mg < 3.3 * x + c + 0.8)]
    note("hr")
    df = df[df["radial_velocity_a"].notna() & df["radial_velocity_b"].notna()
            & ((df["radial_velocity_a"] - df["radial_velocity_b"]).abs() < P["drv_max"])]
    note("rv")
    flame = (a3.drop_duplicates("source_id").set_index("source_id")["mass_flame"]
             if len(a3) else pd.Series(dtype=float))

    def mass(s):
        m_lum = wb.mass_from_mg(df[f"phot_g_mean_mag_{s}"] + 5 * np.log10(df["pbar"] / 100.0), P["mg_sun"])
        f = df[f"source_id_{s}"].map(flame)
        return np.where(f.notna(), f, m_lum)

    df = df.assign(M=mass("a") + mass("b"))
    prim_a = (df["phot_g_mean_mag_a"] <= df["phot_g_mean_mag_b"]).to_numpy()
    vs_list, sig_list = [], []
    for i, (_, r) in enumerate(df.iterrows()):
        p, q = ("a", "b") if prim_a[i] else ("b", "a")
        rv1 = r[f"radial_velocity_{p}"]
        if v.get("mean_rv"):
            w1, w2 = 1 / r[f"radial_velocity_error_{p}"] ** 2, 1 / r[f"radial_velocity_error_{q}"] ** 2
            rv1 = (w1 * r[f"radial_velocity_{p}"] + w2 * r[f"radial_velocity_{q}"]) / (w1 + w2)
        vcor, sig = wb.vsky_corrected_sigma(r[f"ra_{p}"], r[f"dec_{p}"], r[f"ra_{q}"], r[f"dec_{q}"], rv1,
                                            _star(r, p), _star(r, q))
        if v.get("no_projection"):
            s1, s2 = _star(r, p), _star(r, q)
            vcor = float(wb.KAPPA / r["pbar"] * np.hypot(r[f"pmra_{q}"] - r[f"pmra_{p}"],
                                                         r[f"pmdec_{q}"] - r[f"pmdec_{p}"]))
            sig = float(wb.vsky_sigma((s1["pmra"], s1["pmdec"]), (s2["pmra"], s2["pmdec"]), s1["p"], s2["p"],
                                      s1["e_p"], s2["e_p"], s1["e_pmra"], s1["e_pmdec"], s2["e_pmra"],
                                      s2["e_pmdec"], s1["c_ppa"], s1["c_ppd"], s1["c_pad"], s2["c_ppa"],
                                      s2["c_ppd"], s2["c_pad"]))
        vs_list.append(vcor)
        sig_list.append(sig)
    vsky = np.array(vs_list)
    sig = np.array(sig_list)
    vc = wb.vc_kms(df["M"].to_numpy(), df["rsky"].to_numpy())
    df = df.assign(vsky=vsky, vt=vsky / vc, sig_vt=sig / vc,
                   x=df["rsky"].to_numpy() / wb.r_mond_au(df["M"].to_numpy(), P["a0"]))
    if v.get("x_min") is not None:        # R5 V5
        df = df[df["x"] >= v["x_min"]]
    df = df[df["sig_vt"] < P["sig_vt_max"]]
    note("sigma_vt")
    df = df[df["vt"] <= v.get("vt_max", P["vt_max"])]
    note("vt_cap")
    return df


def analyse(df, P, with_boot=True):
    from scipy import stats
    edges = P["edges"]
    b = wb.bin_index(df["x"].to_numpy(), edges)
    nb = len(edges) + 1
    counts = [int(np.sum(b == k)) for k in range(nb)]
    mapping, evaluable = wb.merge_outer(counts, P["min_per_bin"])
    out = {"N": int(len(df)), "counts_raw": counts, "evaluable": bool(evaluable)}
    if not evaluable:
        return out
    b = np.array([mapping[k] for k in b])
    nfin = max(mapping) + 1
    vt = df["vt"].to_numpy()
    x = df["x"].to_numpy()
    med = wb.bin_medians(vt, b, nfin)
    xmed = np.array([np.median(x[b == k]) for k in range(nfin)])
    xgeo = np.array([float(np.exp(np.mean(np.log(x[b == k])))) for k in range(nfin)])
    out.update({"n_bins": nfin, "counts": [int(np.sum(b == k)) for k in range(nfin)],
                "medians": med.tolist(), "x_median": xmed.tolist(), "x_geomean": xgeo.tolist()})
    repro = {}
    for name, scale in (("mad", 1.0), ("mad1.4826", 1.4826)):
        e = wb.mad_errors(vt, b, nfin, scale)
        r = wb.compare_models(med, xmed, np.diag(e ** 2), P["a0"], P["gne_over_a0"])
        repro[name] = dict(r, errors=e.tolist())
    out["reproduction"] = repro
    if with_boot:
        cov, frac, ok = wb.bootstrap_cov(vt, b, nfin, P["n_boot"], P["boot_seed"], P["min_per_bin"])
        r = wb.compare_models(med, xmed, cov, P["a0"], P["gne_over_a0"])
        dof = nfin - 1
        r["p_newton"] = float(stats.chi2.sf(r["chi2_newton"], dof)) if r["valid"] else None
        if r["valid"]:      # tied normalisation (sensitivity): MOND with A fixed at the Newtonian fit
            shape = wb.mond_boost(xmed, P["a0"], P["gne_over_a0"])
            resid = med - r["A_newton"] * shape
            ci = np.linalg.inv(np.diag(np.diag(cov)) if r["used_diagonal"] else cov)
            r["chi2_mond_tied"] = float(resid @ ci @ resid)
        r.update({"redraw_fraction": frac, "boot_valid": ok, "boot_errors": np.sqrt(np.diag(cov)).tolist(),
                  "dof": dof, "boot_over_mad": (np.sqrt(np.diag(cov)) / np.array(repro["mad"]["errors"])).tolist()})
        L = r["L"]
        if not (ok and r["valid"]):
            verdict = "invalid fit (no verdict)"
        elif L >= P["L_threshold"]:
            verdict = "Newton has the higher relative likelihood (agrees with the C26 conclusion)"
        elif L <= 1.0 / P["L_threshold"]:
            verdict = "MOND has the higher relative likelihood (contradicts C26)"
        else:
            verdict = "cannot distinguish (does not support the strength of the C26 conclusion)"
        r["verdict"] = verdict
        out["primary"] = r
    return out


VARIANTS = {
    "main": {},
    "vt_le_2": {"vt_max": 2.0},
    "vt_le_1.5": {"vt_max": 1.5},
    "cleanest_vt1.5_ipd0": {"vt_max": 1.5, "ipd_zero": True},
    "no_projection": {"no_projection": True},
    "no_hr": {"no_hr": True},
    "hr_c_plus_0.2": {"c_shift": 0.2},
    "hr_c_minus_0.2": {"c_shift": -0.2},
    "d150": {"d_max_pc": 150.0},
    "d150_ipd0": {"d_max_pc": 150.0, "ipd_zero": True},
    "ipd0": {"ipd_zero": True},
    "c10_parallax_snr100": {"parallax_snr_min": 100.0},
    "no_degroup": {"no_degroup": True},
    "mean_rv": {"mean_rv": True},
}


def _clean(obj):
    """Replace NaN/inf by None so the saved JSON is standard."""
    import math
    if isinstance(obj, dict):
        return {k: _clean(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_clean(v) for v in obj]
    if isinstance(obj, float) and not math.isfinite(obj):
        return None
    return obj


def step_b(ctx, P):
    if P["hr_c"] is None:
        raise RuntimeError("PARAMS['hr_c'] must be committed (dated) from step A before step B")
    pairs, a2, a3, used = gather(ctx, P)
    results = {}
    traces = {}
    for name, var in VARIANTS.items():
        tr = {}
        df = build_sample(pairs, a2, a3, P, var, trace=tr)
        traces[name] = tr
        results[name] = analyse(df, P, with_boot=True)
        results[name]["cut_trace"] = tr
        ctx.log(f"variant {name}: N={results[name]['N']} "
                f"{results[name].get('primary', {}).get('verdict', 'not evaluable')}")
    main_r = results["main"]
    r1 = {"N_main": main_r["N"], "target": 1421, "within_20pct": abs(main_r["N"] - 1421) <= 0.2 * 1421,
          "N_cleanest": results["cleanest_vt1.5_ipd0"]["N"], "target_cleanest": 1216,
          "fig8_counts": [368, 228, 144, 99, 33, 28]}
    r1["verdict"] = "reproduced sample size" if r1["within_20pct"] else "different sample"
    r1["N_vs_fig8_sum"] = {"N": main_r["N"], "fig8_sum": 900}
    r1["counts_vs_fig8"] = {"ours": main_r.get("counts_raw"), "fig8": r1["fig8_counts"]}
    r1["A_newton_vs_0.489"] = main_r.get("primary", {}).get("A_newton")
    r1["diagnostic_chain"] = traces["main"]   # cumulative counts after each cut, section 4.5 order
    ctx.save("variants", _clean(results))
    return _clean({"step": "B", "R1": r1, "R2": main_r.get("primary", {}).get("verdict"),
            "R2_L": main_r.get("primary", {}).get("L"), "n_candidate_pairs": int(len(pairs)),
            "est_bytes": int(used),
            "not_run": {"d200": "not attempted: needs its own A and B queries beyond the 150 pc parent cut (dated note in README)",
                        "c25_neighbour_degrouping": "diagnostic; its extra A2 queries were not run"}})


# ---------------------------------------------------------------- R5 (README 2.1, T-034)
class DataNotObtained(RuntimeError):
    """A required R5 query could not be completed."""


def _too_large():
    from astrolab.fetch import TooLarge
    return TooLarge


def _r5_region(ctx, P, label, name, r, near, budget, build, bpr):
    """Count first; split a region over the row or byte cap in RA (as section 3); then fetch.
    build(region, near, select) returns the ADQL; select is 'count' or 'rows'."""
    n = _count(ctx, build(r, near, "count"), f"{label} {name}")
    if n >= P["max_rows"] or n * bpr > _max_bytes():
        if near:
            raise RuntimeError(f"{label} {name}: the near-star query exceeded the row cap; stop")
        if r["ra1"] - r["ra0"] < 0.1:
            raise RuntimeError(f"{label} {name}: still over the row cap at 0.1 deg; stop and ask the user")
        ns, dfs = 0, []
        for i, sub in enumerate(wb.split_region(r)):
            k, d = _r5_region(ctx, P, label, f"{name}.{i}", sub, near, budget, build, bpr)
            ns += k
            dfs.append(d)
        return ns, pd.concat(dfs, ignore_index=True)
    if n == 0:
        return 0, pd.DataFrame()
    budget.reserve(n * bpr, f"{label} {name}")
    df = ctx.tap(build(r, near, "rows"), "gaia", label=f"{label} {name}", max_rows=P["max_rows"],
                 mode="async", release="Gaia DR3")
    _same(n, df, f"{label} {name}")
    return n, df


def _r5_with_fallback(ctx, P, label, name, r, near, budget, build_restricted, build_full, bpr):
    """Restricted query; if the archive refuses or times out, the unrestricted region-partitioned
    query (section 3, restricted-join risk). Budget stops are never retried."""
    try:
        n, d = _r5_region(ctx, P, label, name, r, near, budget, build_restricted, bpr)
        return n, d, False
    except (BudgetStop, _too_large()):
        raise
    except Exception as e:  # noqa: BLE001 - archive refusal or timeout of the restricted join
        ctx.log(f"{label} {name}: restricted query failed ({type(e).__name__}: {str(e)[:120]}); fallback")
    try:
        n, d = _r5_region(ctx, P, f"{label}-fallback", name, r, near, budget, build_full, bpr)
        return n, d, True
    except (BudgetStop, _too_large()):
        raise
    except Exception as e:  # noqa: BLE001
        raise DataNotObtained(f"{label} {name}: {type(e).__name__}: {e}") from e


def r5_gather_a(ctx, P, R, budget):
    """Step A' (velocity-free): N1, N2 (restricted, fallback), N3 (restricted, fallback) and
    N2-C25 (restricted only; V9), per region."""
    import r5
    nb = P["near_b"]

    def one(item):
        name, r, near = item
        try:
            _, d1 = _r5_region(ctx, P, "N1", name, r, near, budget,
                               lambda rr, nn, sel: r5.n1_query(rr, nn, nb, sel), R["r5_bytes_n1"])
        except (BudgetStop, _too_large()):
            raise
        except Exception as e:  # noqa: BLE001
            raise DataNotObtained(f"N1 {name}: {type(e).__name__}: {e}") from e
        _, d2, f2 = _r5_with_fallback(
            ctx, P, "N2", name, r, near, budget,
            lambda rr, nn, sel: r5.neighbour_query(rr, nn, nb, r5.NEIGHBOUR, sel, True),
            lambda rr, nn, sel: r5.neighbour_query(rr, nn, nb, r5.NEIGHBOUR, sel, False), R["r5_bytes_n2"])
        _, d3, f3 = _r5_with_fallback(
            ctx, P, "N3", name, r, near, budget,
            lambda rr, nn, sel: r5.flame_query(rr, nn, nb, sel, True),
            lambda rr, nn, sel: r5.flame_query(rr, nn, nb, sel, False), R["r5_bytes_n3"])
        dc, c25_error = None, None
        if R["r5_run_c25"]:
            try:
                _, dc = _r5_region(ctx, P, "N2-C25", name, r, near, budget,
                                   lambda rr, nn, sel: r5.neighbour_query(rr, nn, nb, r5.NEIGHBOUR_C25, sel, True),
                                   R["r5_bytes_n2"])
            except (BudgetStop, _too_large()):
                raise
            except Exception as e:  # noqa: BLE001 - V9 runs only in restricted form
                c25_error = f"{type(e).__name__}: {str(e)[:200]}"
        return name, d1, d2, d3, dc, f2, f3, c25_error

    parts = {"n1": [], "n2": [], "n3": [], "c25": []}
    fallback, c25_errors = {"N2": [], "N3": []}, {}
    with ThreadPoolExecutor(max_workers=int(P["workers"])) as ex:
        for name, d1, d2, d3, dc, f2, f3, ce in ex.map(one, _regions(P)):
            parts["n1"].append(d1)
            parts["n2"].append(d2)
            parts["n3"].append(d3)
            if f2:
                fallback["N2"].append(name)
            if f3:
                fallback["N3"].append(name)
            if ce:
                c25_errors[name] = ce
            elif dc is not None:
                parts["c25"].append(dc)
    cat = {k: (pd.concat(v, ignore_index=True) if v else pd.DataFrame()) for k, v in parts.items()}
    if not R["r5_run_c25"] or c25_errors:
        cat["c25"] = None
    for k in ("n2", "c25"):
        if cat[k] is not None and len(cat[k]) == 0:
            cat[k] = pd.DataFrame({"source_id": [], "n": [], "first_neighbour": []})
    if len(cat["n3"]) == 0:
        cat["n3"] = pd.DataFrame({"source_id": [], "mass_flame": []})
    return cat, fallback, c25_errors


def r5_fetch_n4(ctx, P, R, budget):
    """Step B': N4 per region (only after G1b passes and the blinding check)."""
    import r5
    nb = P["near_b"]

    def one(item):
        name, r, near = item
        try:
            return _r5_region(ctx, P, "N4", name, r, near, budget,
                              lambda rr, nn, sel: r5.n4_query(rr, nn, nb, sel), R["r5_bytes_n4"])[1]
        except (BudgetStop, _too_large()):
            raise
        except Exception as e:  # noqa: BLE001
            raise DataNotObtained(f"N4 {name}: {type(e).__name__}: {e}") from e
    with ThreadPoolExecutor(max_workers=int(P["workers"])) as ex:
        dfs = list(ex.map(one, _regions(P)))
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()


def r5_analyse_all(pairs, cat, P, R, pm, unblinded):
    """Statistic, G2 and label for R5; V1-V14 and E1-E5 (descriptive); per-shell medians."""
    import r5
    P5 = dict(P, d_max_pc=R["r5_d_max_pc"], rsky_min_au=R["r5_rsky_min_au"])
    res = {}
    for name, (vflags, pover) in r5.VARIANTS.items():
        if name == "V9_c25_degroup" and cat["c25"] is None:
            res[name] = {"not_run": "N2-C25 not obtained in restricted form" if R["r5_run_c25"] else "switched off"}
            continue
        tr = {}
        a2 = cat["c25"] if name == "V9_c25_degroup" else cat["n2"]
        df = build_sample(pairs, a2, cat["n3"], dict(P5, **pover), vflags, trace=tr)
        rr = r5.analyse(df, P["edges"], P["min_per_bin"], R["r5_n_boot"], R["r5_seed"], P["a0"],
                        P["gne_over_a0"], pm, error_models=(name == "R5"))
        rr["cut_trace"] = tr
        if name == "R5" and rr.get("valid"):
            rr["shells"] = r5.shell_descriptives(df, P["edges"], rr["mapping"])
        res[name] = rr
    main_r = res.pop("R5")
    if not main_r.get("valid"):
        label = r5.relabel(r5.LABELS["invalid"], unblinded)
    else:
        label = r5.verdict_label(True, main_r["fit"]["g2"]["passes"], main_r["fit"]["L"], unblinded)
    return main_r, res, label


def step_r5(ctx, P, R):
    """README 2.1 R5 (T-034): N1-N3 (+N2-C25), G1b, blinding check, N4, statistic, variants."""
    import r5
    ctx.record_suffix = "_r5"          # keep R2's provenance.json and run_info.json untouched
    pm = r5.power_mock()
    P5 = dict(P, d_max_pc=R["r5_d_max_pc"], rsky_min_au=R["r5_rsky_min_au"])
    out = {"mode": "r5", "not_reproduction": "enlarged sample; not a reproduction",
           "params": {**R, "parent": r5.PARENT_RV, "neighbour": r5.NEIGHBOUR, "neighbour_c25": r5.NEIGHBOUR_C25,
                      "merge_time_utc": r5.MERGE_TIME_UTC, "edges": P["edges"], "min_per_bin": P["min_per_bin"],
                      "hr_c": P["hr_c"], "g1b_factors": [float(f) for f in pm.G1B_FACTORS]}}
    budget = Budget(P["budget_bytes"])

    def finish(label):
        out["label"] = label
        out["est_bytes"] = int(budget.used)
        ctx.save("r5", _clean(out))
        ctx.log(f"R5: {label}")
        return out

    try:
        cat, fallback, c25_errors = r5_gather_a(ctx, P, R, budget)
    except DataNotObtained as e:
        out["error"] = str(e)
        return finish(r5.LABELS["no_data"])
    out["queries_a"] = {"n1_rows": int(len(cat["n1"])), "n2_rows": int(len(cat["n2"])),
                        "n3_rows": int(len(cat["n3"])),
                        "n2_c25_rows": None if cat["c25"] is None else int(len(cat["c25"])),
                        "fallback_regions": fallback, "n2_c25_errors": c25_errors}
    if len(cat["n1"]) == 0:
        out["error"] = "N1 returned no pairs"
        return finish(r5.LABELS["no_data"])
    x, trace = r5.g1b_step1(cat["n1"], cat["n2"], cat["n3"], P5)
    g = pm.g1b_pipeline(x, P["edges"], P["min_per_bin"])
    out["g1b"] = {"step1_trace": trace, **g}
    ctx.log(f"G1b: {g}")
    if not g["passes"]:
        return finish(r5.LABELS["g1b_fail"])
    if R["r5_stop_after_g1b"]:
        out["stopped_after_g1b"] = True
        return finish("R5: G1b passed; stopped before N4 (r5_stop_after_g1b)")
    # blinding check (README 2.1 unblinded rule; section 3 schedule)
    t_read = r5.now_utc()
    if t_read < r5.parse_utc(r5.MERGE_TIME_UTC):
        raise RuntimeError("refusing to read N4 before the merge of README 2.1 to main")
    n_prov = len(ctx.provenance.records)
    try:
        n4 = r5_fetch_n4(ctx, P, R, budget)
    except DataNotObtained as e:
        out["error"] = str(e)
        return finish(r5.LABELS["no_data"])
    recs = [rec for rec in ctx.provenance.records[n_prov:]
            if str(rec.get("label", "")).startswith("N4 ") and (rec.get("rows") or 0) > 0]
    stamps = [rec["retrieved_at"] for rec in recs if rec.get("retrieved_at")]
    unblinded = r5.read_before_merge(stamps)
    out["blinding"] = {"n4_read_started_utc": t_read.replace(microsecond=0).isoformat(),
                       "n4_earliest_retrieved_at": min(stamps) if stamps else None,
                       "merge_time_utc": r5.MERGE_TIME_UTC, "n4_read_before_merge": bool(unblinded)}
    n1 = cat["n1"].iloc[wb.canonical_pairs(cat["n1"]["source_id_a"].to_numpy(),
                                           cat["n1"]["source_id_b"].to_numpy())].reset_index(drop=True)
    n1 = n1.drop(columns=[f"{c}_{s}" for c in r5.N1_EXTRA_COLS for s in ("a", "b")])
    n4 = n4.iloc[wb.canonical_pairs(n4["source_id_a"].to_numpy(), n4["source_id_b"].to_numpy())].reset_index(drop=True)
    pairs = n1.merge(n4, on=["source_id_a", "source_id_b"], how="inner")
    if len(pairs) != len(n4):
        raise RuntimeError(f"{len(n4) - len(pairs)} N4 pairs are missing from N1; stop")
    out["queries_b"] = {"n4_rows": int(len(n4)), "merged": int(len(pairs))}
    out["main"], out["variants"], label = r5_analyse_all(pairs, cat, P, R, pm, unblinded)
    return finish(label)


def main(ctx):
    P = dict(PARAMS)
    mode = P.pop("mode", "r2")
    R = {k: P.pop(k) for k in list(P) if k.startswith("r5_")}
    if mode == "r5":
        return step_r5(ctx, P, R)
    if mode != "r2":
        raise RuntimeError(f"unknown mode {mode!r}")
    if P["step"] == "B":
        out = step_b(ctx, P)
        ctx.save("summary", {"params": P, **out})
        return out
    if P["step"] == "A":
        out = step_a(ctx, P)
        ctx.log(f"step A: {out['n_pairs_a1']} candidate pairs, {out['n_stars_a2']} stars with neighbours, "
                f"est {out['est_bytes'] / 1e6:.1f} MB, c = {out['hr_constant']}")
        ctx.save("summary", {"params": P, "step_a": {k: v for k, v in out.items() if k != "counts_per_region"}})
        return out
    raise RuntimeError(f"unknown step {P['step']!r}")
