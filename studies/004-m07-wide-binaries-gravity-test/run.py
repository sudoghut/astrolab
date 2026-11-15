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
    "step": "A",                       # "A" (velocity-free) or "B" (after the pre-registration commit)
    "parent": "parallax > 6.6667 AND parallax_over_error > 40",
    # main degrouping uses relaxed neighbours (C26 section 3.2.2); C25-only is a diagnostic
    "neighbour": ("parallax_over_error > 5 AND phot_g_mean_flux_over_error > 5"
                  " AND parallax + 3 * parallax_error > 6.6667"),
    "neighbour_c25": ("parallax_over_error > 40 AND phot_g_mean_flux_over_error > 5"
                      " AND parallax + 3 * parallax_error > 6.6667"),
    "near_plx": 100.0, "near_b": "parallax + 3 * parallax_error > 80",
    "vcap_kms": None,                  # no velocity condition in A1 (README section 3)
    "max_rows": 50000,
    "bytes_per_row_pair": 400, "bytes_per_row_count": 40,
    "budget_bytes": 200 * 1024 ** 2,
    "workers": 4,
    "region_limit": None,              # exploration only: run the first N regions
    # step B (README sections 2 and 4); fixed by the pre-registration
    "hr_c": None,                      # numeric HR constant, committed (dated) after step A, before step B
    "a0": 1.2e-10, "gne_over_a0": 1.184, "mg_sun": 4.67,
    "edges": [0.1057, 0.2307, 0.5088, 1.0275, 2.0902],
    "min_per_bin": 15, "n_boot": 2000, "boot_seed": 0, "L_threshold": 100.0,
    "d_max_pc": 130.0, "rsky_min_au": 1000.0, "rsky_max_au": 30000.0, "ruwe_max": 1.25,
    "drv_max": 10.0, "sig_vt_max": 0.1, "vt_max": 2.5,
}


def _max_bytes():
    from astrolab import config
    return config.HTTP_MAX_BYTES


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


class Budget:
    """Cumulative byte estimate shared by the worker threads; checked BEFORE each fetch."""

    def __init__(self, limit):
        self.limit, self.used, self.lock = limit, 0, threading.Lock()

    def reserve(self, nbytes, what):
        with self.lock:
            if self.used + nbytes > self.limit:
                raise RuntimeError(f"{what}: cumulative estimate {(self.used + nbytes) / 1e6:.1f} MB exceeds "
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
    if n * 600 > _max_bytes():
        return _split(ctx, P, name, r, near, budget, _a1)
    budget.reserve(n * 600, f"A1 {name}")
    q = qc.replace("SELECT COUNT(*) AS n", "SELECT " + Q.a1_select(), 1)
    df = ctx.tap(q, "gaia", label=f"A1 {name}", max_rows=P["max_rows"], mode="async", release="Gaia DR3")
    return n, df


def _a2(ctx, P, name, r, near, neighbour_key, budget):
    nb = P[neighbour_key]
    if near:
        nb = f"{nb} AND {P['near_b']}"
    qc = Q.neighbour_query(r, P["parent"], nb, "count", near=near)
    n = _count(ctx, qc, f"A2 {name}")
    if n >= P["max_rows"]:
        return _split(ctx, P, name, r, near, budget, _a2, neighbour_key)
    budget.reserve(n * P["bytes_per_row_count"], f"A2 {name}")
    q = Q.neighbour_query(r, P["parent"], nb, "rows", near=near)
    df = ctx.tap(q, "gaia", label=f"A2 {name}", max_rows=P["max_rows"], mode="async", release="Gaia DR3")
    return n, df


def _a3(ctx, P, name, r, near, budget):
    qc = Q.flame_query(r, P["parent"], "count", near=near)
    n = _count(ctx, qc, f"A3 {name}")
    if n >= P["max_rows"]:
        return _split(ctx, P, name, r, near, budget, _a3)
    budget.reserve(n * 24, f"A3 {name}")
    df = ctx.tap(Q.flame_query(r, P["parent"], "rows", near=near), "gaia", label=f"A3 {name}",
                 max_rows=P["max_rows"], mode="async", release="Gaia DR3")
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
    if n >= P["max_rows"] or n * 300 > _max_bytes():
        return _split(ctx, P, name, r, near, budget, _b1)
    budget.reserve(n * 300, f"B1 {name}")
    q = qc.replace("SELECT COUNT(*) AS n", "SELECT " + Q.b1_select(), 1)
    df = ctx.tap(q, "gaia", label=f"B1 {name}", max_rows=P["max_rows"], mode="async", release="Gaia DR3")
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

    def one(item):
        name, r, near = item
        _, d1 = _a1(ctx, P, name, r, near, free)
        _, d2 = _a2(ctx, P, name, r, near, "neighbour", free)
        _, d3 = _a3(ctx, P, name, r, near, free)
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
    pairs = a1.merge(b1, on=["source_id_a", "source_id_b"], how="inner")
    return pairs, a2, a3, budget.used


def _star(r, s):
    return dict(p=r[f"parallax_{s}"], pmra=r[f"pmra_{s}"], pmdec=r[f"pmdec_{s}"], e_p=r[f"parallax_error_{s}"],
                e_pmra=r[f"pmra_error_{s}"], e_pmdec=r[f"pmdec_error_{s}"], c_ppa=r[f"parallax_pmra_corr_{s}"],
                c_ppd=r[f"parallax_pmdec_corr_{s}"], c_pad=r[f"pmra_pmdec_corr_{s}"])


def build_sample(pairs, a2, a3, P, variant):
    """Apply README section 4 to the merged pairs; returns a DataFrame with x, vt, sig_vt."""
    v = dict(variant)
    df = pairs.copy()
    if not v.get("no_degroup"):          # each member's only neighbour is its partner (A2)
        nb = a2.drop_duplicates("source_id").set_index("source_id")
        n_a = df["source_id_a"].map(nb["n"])
        n_b = df["source_id_b"].map(nb["n"])
        f_a = df["source_id_a"].map(nb["first_neighbour"])
        f_b = df["source_id_b"].map(nb["first_neighbour"])
        ok = (n_a == 1) & (n_b == 1) & (f_a == df["source_id_b"]) & (f_b == df["source_id_a"])
        df = df[ok.fillna(False).astype(bool)]
    pbar, _, _ = wb.weighted_parallax(df["parallax_a"].to_numpy(), df["parallax_error_a"].to_numpy(),
                                      df["parallax_b"].to_numpy(), df["parallax_error_b"].to_numpy())
    df = df.assign(pbar=pbar)
    df = df[df["pbar"] > 1000.0 / v.get("d_max_pc", P["d_max_pc"])]
    rsky = wb.sky_separation_au(df["ra_a"].to_numpy(), df["dec_a"].to_numpy(), df["ra_b"].to_numpy(),
                                df["dec_b"].to_numpy(), df["pbar"].to_numpy())
    df = df.assign(rsky=np.asarray(rsky))
    df = df[(df["rsky"] >= P["rsky_min_au"]) & (df["rsky"] <= P["rsky_max_au"])]
    if v.get("parallax_snr_min"):
        df = df[(df["parallax_a"] / df["parallax_error_a"] > v["parallax_snr_min"])
                & (df["parallax_b"] / df["parallax_error_b"] > v["parallax_snr_min"])]
    df = df[(df["ruwe_a"] < P["ruwe_max"]) & (df["ruwe_b"] < P["ruwe_max"])]
    if v.get("ipd_zero"):
        df = df[(df["ipd_frac_multi_peak_a"] == 0) & (df["ipd_frac_multi_peak_b"] == 0)]
    if not v.get("no_hr"):
        c = P["hr_c"] + v.get("c_shift", 0.0)
        for s in ("a", "b"):
            x = df[f"bp_rp_{s}"]
            mg = df[f"phot_g_mean_mag_{s}"] + 5 * np.log10(df["pbar"] / 100.0)
            df = df[(x > 0.5) & (x < 3.5) & (mg > 4) & (mg < 14) & (mg > 3.3 * x + c) & (mg < 3.3 * x + c + 0.8)]
    df = df[df["radial_velocity_a"].notna() & df["radial_velocity_b"].notna()
            & ((df["radial_velocity_a"] - df["radial_velocity_b"]).abs() < P["drv_max"])]
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
            vcor = float(wb.KAPPA / r["pbar"] * np.hypot(r[f"pmra_{q}"] - r[f"pmra_{p}"],
                                                         r[f"pmdec_{q}"] - r[f"pmdec_{p}"]))
        vs_list.append(vcor)
        sig_list.append(sig)
    vsky = np.array(vs_list)
    sig = np.array(sig_list)
    vc = wb.vc_kms(df["M"].to_numpy(), df["rsky"].to_numpy())
    df = df.assign(vsky=vsky, vt=vsky / vc, sig_vt=sig / vc,
                   x=df["rsky"].to_numpy() / wb.r_mond_au(df["M"].to_numpy(), P["a0"]))
    return df[(df["sig_vt"] < P["sig_vt_max"]) & (df["vt"] <= v.get("vt_max", P["vt_max"]))]


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


def step_b(ctx, P):
    if P["hr_c"] is None:
        raise RuntimeError("PARAMS['hr_c'] must be committed (dated) from step A before step B")
    pairs, a2, a3, used = gather(ctx, P)
    results = {}
    for name, var in VARIANTS.items():
        df = build_sample(pairs, a2, a3, P, var)
        results[name] = analyse(df, P, with_boot=True)
        ctx.log(f"variant {name}: N={results[name]['N']} "
                f"{results[name].get('primary', {}).get('verdict', 'not evaluable')}")
    main_r = results["main"]
    r1 = {"N_main": main_r["N"], "target": 1421, "within_20pct": abs(main_r["N"] - 1421) <= 0.2 * 1421,
          "N_cleanest": results["cleanest_vt1.5_ipd0"]["N"], "target_cleanest": 1216,
          "fig8_counts": [368, 228, 144, 99, 33, 28]}
    r1["verdict"] = "reproduced sample size" if r1["within_20pct"] else "different sample"
    ctx.save("variants", results)
    return {"step": "B", "R1": r1, "R2": main_r.get("primary", {}).get("verdict"),
            "R2_L": main_r.get("primary", {}).get("L"), "n_candidate_pairs": int(len(pairs)),
            "est_bytes": int(used),
            "not_run": {"d200": "needs its own queries beyond the 150 pc parent cut",
                        "c25_neighbour_degrouping": "diagnostic; its extra A2 queries were not run"}}


def main(ctx):
    P = dict(PARAMS)
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
