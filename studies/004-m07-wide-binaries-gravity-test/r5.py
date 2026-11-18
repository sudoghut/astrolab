"""Pure helpers for R5 (README section 2.1 and the section 3 R5 data block; T-034).

No data access here: run.py fetches through ctx.tap and passes tables in. Parameters are passed as
arguments (AGENTS.md section 2: no `import run`, no module-level use of PARAMS). The G1b simulation
(steps 2-5) and the symmetric G2 rule live in explore/t034_power_mock.py, the single implementation
named by the README; `power_mock()` loads that file.
"""
from __future__ import annotations

import importlib.util
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

import queries as Q
import wb

# README section 2.1 / section 3 (fixed by the pre-registration)
PARENT = "parallax > 3.4783 AND parallax_over_error > 40"
PARENT_RV = PARENT + " AND radial_velocity IS NOT NULL"
NEIGHBOUR = "parallax_over_error > 5 AND phot_g_mean_flux_over_error > 5 AND parallax + 3 * parallax_error > 3.4783"
NEIGHBOUR_C25 = "parallax_over_error > 40 AND phot_g_mean_flux_over_error > 5 AND parallax + 3 * parallax_error > 3.4783"
RSKY_MAX_KAU = 30.0
PAIR_PC = RSKY_MAX_KAU * 1000.0 / wb.PC_AU        # 30 kAU in pc (search circle, as queries.PAIR_PC)
MERGE_TIME_UTC = "2026-11-18T12:04:20Z"      # merge of README 2.1 to main (PR #40); blinding trigger
N1_EXTRA_COLS = ["pmra_error", "pmdec_error"]
LABELS = {
    "invalid": "R5: invalid fit (no label)",
    "g1b_fail": "R5: not run (insufficient predicted power)",
    "no_data": "R5: not run (data not obtained)",
    "g2fail_newton": "R5: no verdict at C26's strength (insufficient power, data-conditional); Newton weakly preferred (descriptive)",
    "g2fail_none": "R5: no verdict at C26's strength (insufficient power, data-conditional); no preference (descriptive)",
    "g2fail_mond": "R5: no verdict at C26's strength (insufficient power, data-conditional); MOND weakly preferred (descriptive)",
    "newton": "R5: Newton has the higher relative likelihood (agrees with C26's conclusion)",
    "cannot": "R5: cannot distinguish",
    "mond": "R5: MOND has the higher relative likelihood (contradicts C26)",
}
UNBLINDED_PREFIX = "R5 (unblinded, descriptive):"
GRADES = ("Newton weakly preferred (descriptive)", "no preference (descriptive)",
          "MOND weakly preferred (descriptive)")


def power_mock():
    """The explore/t034_power_mock.py module (G1b steps 2-5, symmetric G2)."""
    path = Path(__file__).parent / "explore" / "t034_power_mock.py"
    spec = importlib.util.spec_from_file_location("t034_power_mock", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------- ADQL (section 3, R5 data)
_PBAR = ("((b.parallax_error*b.parallax_error*a.parallax + a.parallax_error*a.parallax_error*b.parallax)"
         " / (a.parallax_error*a.parallax_error + b.parallax_error*b.parallax_error))")
_RSKY_KAU = f"DISTANCE(POINT(a.ra, a.dec), POINT(b.ra, b.dec)) * 3.141592653589793 / 180.0 * 1000.0 / {_PBAR} * 206.264806"
_SIG3 = ("ABS(a.parallax - b.parallax) < 3 * SQRT(a.parallax_error*a.parallax_error"
         " + b.parallax_error*b.parallax_error)")
N1_COLS = Q.A_COLS + N1_EXTRA_COLS
N4_COLS = ["source_id", "ra", "dec", "parallax", "parallax_error", "ruwe"] + [c for c in Q.B1_COLS if c != "source_id"]


def _pair_from(region, near, near_b, cols, alias_a="a", alias_b="b"):
    a = Q._sub(Q.star_a_where(region, PARENT_RV, near), cols, alias_a)
    bf = PARENT_RV + (f" AND {near_b}" if near else "")
    b = Q._sub(Q.star_b_where(region, bf, near), cols, alias_b)
    return a, b


def pair_conds():
    """N1 pair conditions: the strict 3-sigma rule and r_sky <= 30 kAU at the weighted parallax."""
    return [_SIG3, f"{_RSKY_KAU} <= {RSKY_MAX_KAU}"]


def n1_query(region, near, near_b, select):
    """N1: canonical pairs (a.source_id < b.source_id) of parent RV stars within 30 kAU.
    select is 'count' or 'rows'."""
    a, b = _pair_from(region, near, near_b, N1_COLS)
    circ = f"CIRCLE(a.ra, a.dec, {PAIR_PC} * a.parallax * 1.12 / 1000.0 * 180.0 / 3.141592653589793)"
    where = " AND ".join(["a.source_id < b.source_id"] + pair_conds())
    sel = "COUNT(*) AS n" if select == "count" else ", ".join(
        f"{s}.{c} AS {c}_{s}" for s in ("a", "b") for c in N1_COLS)
    return f"SELECT {sel} FROM {a} JOIN {b} ON 1 = CONTAINS(POINT(b.ra, b.dec), {circ}) WHERE {where}"


def n4_query(region, near, near_b, select):
    """N4: N1's WHERE plus the server-side velocity-free cuts (pbar > 4.0 mas, r_sky >= 300 AU,
    RUWE < 1.25 for both stars); velocity columns (B1) only after G1b passes."""
    a, b = _pair_from(region, near, near_b, N4_COLS)
    circ = f"CIRCLE(a.ra, a.dec, {PAIR_PC} * a.parallax * 1.12 / 1000.0 * 180.0 / 3.141592653589793)"
    conds = ["a.source_id < b.source_id"] + pair_conds() + [
        f"{_PBAR} > 4.0", f"{_RSKY_KAU} >= 0.3", "a.ruwe < 1.25", "b.ruwe < 1.25"]
    sel = "COUNT(*) AS n" if select == "count" else Q.b1_select()
    return (f"SELECT {sel} FROM {a} JOIN {b} ON 1 = CONTAINS(POINT(b.ra, b.dec), {circ}) "
            f"WHERE {' AND '.join(conds)}")


def member_subquery(region, near, near_b):
    """Source ids of the region's parent RV stars that belong to any N1 pair (either orientation)."""
    cols = ["source_id", "ra", "dec", "parallax", "parallax_error"]
    a, b = _pair_from(region, near, near_b, cols)
    circ = f"CIRCLE(a.ra, a.dec, {PAIR_PC} * a.parallax * 1.12 / 1000.0 * 180.0 / 3.141592653589793)"
    where = " AND ".join(["a.source_id <> b.source_id"] + pair_conds())
    return f"SELECT a.source_id FROM {a} JOIN {b} ON 1 = CONTAINS(POINT(b.ra, b.dec), {circ}) WHERE {where}"


def neighbour_query(region, near, near_b, neighbour, select, restricted=True):
    """N2 / N2-C25: per parent RV star of the region (restricted: only N1 members), the number of
    neighbours within 100 kAU (<=) and 3 sigma (<), and the smallest neighbour id."""
    cols = ["source_id", "ra", "dec", "parallax", "parallax_error"]
    aw = Q.star_a_where(region, PARENT_RV, near)
    if restricted:
        aw += f" AND source_id IN ({member_subquery(region, near, near_b)})"
    a = Q._sub(aw, cols, "a")
    nb = neighbour + (f" AND {near_b}" if near else "")
    b = Q._sub(Q.star_b_where(region, nb, near), cols, "b")
    conds = ["a.source_id <> b.source_id"] + Q.pair_conditions(None, Q.DEGROUP_PC)
    inner = (f"SELECT a.source_id AS source_id, COUNT(*) AS n, MIN(b.source_id) AS first_neighbour "
             f"FROM {a} JOIN {b} ON 1 = CONTAINS(POINT(b.ra, b.dec), {Q._circle(radius_pc=Q.DEGROUP_PC)}) "
             f"WHERE {' AND '.join(conds)} GROUP BY a.source_id")
    return f"SELECT COUNT(*) AS n FROM ({inner}) AS g" if select == "count" else inner


def flame_query(region, near, near_b, select, restricted=True):
    """N3: FLAME masses of the region's parent RV stars (restricted: only N1 members)."""
    aw = Q.star_a_where(region, PARENT_RV, near)
    if restricted:
        aw += f" AND source_id IN ({member_subquery(region, near, near_b)})"
    inner = (f"FROM (SELECT source_id FROM gaiadr3.gaia_source WHERE {aw}) AS g "
             f"JOIN gaiadr3.astrophysical_parameters AS ap ON ap.source_id = g.source_id "
             f"WHERE ap.mass_flame IS NOT NULL")
    if select == "count":
        return f"SELECT COUNT(*) AS n {inner}"
    return f"SELECT g.source_id AS source_id, ap.mass_flame AS mass_flame {inner}"


# ---------------------------------------------------------------- G1b step 1 (velocity-free)
def degroup_mask(df, a2):
    """Each member has exactly one neighbour (A2/N2 table) and it is the partner."""
    if a2["source_id"].duplicated().any():
        raise RuntimeError("neighbour table has duplicate source_id rows; stop")
    nb = {int(s): (int(n), int(f)) for s, n, f in zip(a2["source_id"], a2["n"], a2["first_neighbour"])}

    def single(sid, partner):
        v = nb.get(int(sid))
        return v is not None and v[0] == 1 and v[1] == int(partner)
    return np.array([single(a, b) and single(b, a) for a, b in zip(df["source_id_a"], df["source_id_b"])], bool)


def masses(df, a3, mg_sun):
    flame = (a3.drop_duplicates("source_id").set_index("source_id")["mass_flame"]
             if len(a3) else pd.Series(dtype=float))

    def one(s):
        m_lum = wb.mass_from_mg(df[f"phot_g_mean_mag_{s}"] + 5 * np.log10(df["pbar"] / 100.0), mg_sun)
        f = df[f"source_id_{s}"].map(flame)
        return np.where(f.notna(), f, m_lum)
    return one("a") + one("b")


def sigma_proxy(df, M):
    """sigma~ = 4.740470464/pbar * sqrt((e_pmra1^2 + e_pmdec1^2 + e_pmra2^2 + e_pmdec2^2)/2) / v_c."""
    s2 = (df["pmra_error_a"] ** 2 + df["pmdec_error_a"] ** 2 + df["pmra_error_b"] ** 2 + df["pmdec_error_b"] ** 2) / 2.0
    return 4.740470464 / df["pbar"].to_numpy() * np.sqrt(s2.to_numpy()) / wb.vc_kms(M, df["rsky"].to_numpy())


def g1b_step1(n1, n2, n3, P):
    """README 2.1 G1b step 1, in order. Returns (x of the surviving pairs, trace of counts)."""
    df = n1.iloc[wb.canonical_pairs(n1["source_id_a"].to_numpy(), n1["source_id_b"].to_numpy())].reset_index(drop=True)
    tr = {"canonical": int(len(df))}
    df = df[degroup_mask(df, n2)]
    tr["degroup"] = int(len(df))
    pbar, _, _ = wb.weighted_parallax(df["parallax_a"].to_numpy(), df["parallax_error_a"].to_numpy(),
                                      df["parallax_b"].to_numpy(), df["parallax_error_b"].to_numpy())
    df = df.assign(pbar=pbar)
    df = df[df["pbar"] > 1000.0 / P["d_max_pc"]]
    tr["distance"] = int(len(df))
    rsky = wb.sky_separation_au(df["ra_a"].to_numpy(), df["dec_a"].to_numpy(), df["ra_b"].to_numpy(),
                                df["dec_b"].to_numpy(), df["pbar"].to_numpy())
    df = df.assign(rsky=np.asarray(rsky))
    df = df[(df["rsky"] >= P["rsky_min_au"]) & (df["rsky"] <= P["rsky_max_au"])]
    tr["r_sky"] = int(len(df))
    df = df[(df["ruwe_a"] < P["ruwe_max"]) & (df["ruwe_b"] < P["ruwe_max"])]
    tr["ruwe"] = int(len(df))
    c = P["hr_c"]
    for s in ("a", "b"):
        x = df[f"bp_rp_{s}"]
        mg = df[f"phot_g_mean_mag_{s}"] + 5 * np.log10(df["pbar"] / 100.0)
        df = df[(x > 0.5) & (x < 3.5) & (mg > 4) & (mg < 14) & (mg > 3.3 * x + c) & (mg < 3.3 * x + c + 0.8)]
    tr["hr"] = int(len(df))
    M = masses(df, n3, P["mg_sun"])
    x = df["rsky"].to_numpy() / wb.r_mond_au(M, P["a0"])
    keep = sigma_proxy(df, M) < P["sig_vt_max"]
    tr["sigma_proxy"] = int(np.sum(keep))
    return x[keep], tr


# ---------------------------------------------------------------- statistics
def stratified_sigma(vt_sorted, b_sorted, nbins, n_boot=10000, seed=0, chunk=500):
    """README 2.1 error model: one default_rng(seed); for each final bin in increasing x one
    rng.integers(0, N_j, size=(n_boot, N_j)) (drawn in row chunks, which consumes the generator
    identically); sigma_j = std(ddof=1) of the replicate medians. Inputs sorted by
    (source_id_a, source_id_b)."""
    # Chunking is equivalent to one call: Generator.integers with a scalar bound fills its output in
    # C order from one stream, drawing values one after another (Lemire's method, with rejections
    # consumed in place), so rows 0..m-1 then m..2m-1 are the same numbers as rows 0..2m-1 of a
    # single call. test_r5 checks this against single calls.
    rng = np.random.default_rng(seed)
    out = []
    for k in range(nbins):
        v = vt_sorted[b_sorted == k]
        n = len(v)
        meds = []
        done = 0
        while done < n_boot:
            m = min(chunk, n_boot - done)
            meds.append(np.median(v[rng.integers(0, n, size=(m, n))], axis=1))
            done += m
        out.append(float(np.std(np.concatenate(meds), ddof=1)) if n else float("nan"))
    return np.array(out)


def grade(L):
    if L >= 10:
        return GRADES[0]
    if L <= 0.1:
        return GRADES[2]
    return GRADES[1]


def verdict_label(fit_valid, g2_pass, L, unblinded=False):
    if not fit_valid:
        lab = LABELS["invalid"]
    elif not g2_pass:
        lab = LABELS["g2fail_newton"] if L >= 10 else LABELS["g2fail_mond"] if L <= 0.1 else LABELS["g2fail_none"]
    else:
        lab = LABELS["newton"] if L >= 100 else LABELS["mond"] if L <= 0.01 else LABELS["cannot"]
    return relabel(lab, unblinded)


def relabel(label, unblinded):
    if not unblinded:
        return label
    return f"{UNBLINDED_PREFIX} {label[len('R5: '):] if label.startswith('R5: ') else label}"


def _fit(med, xmed, sig, a0, gne, pm):
    from scipy import stats
    cov = np.diag(sig ** 2)
    r = wb.compare_models(med, xmed, cov, a0, gne)
    out = {k: r[k] for k in ("A_newton", "A_mond", "chi2_newton", "chi2_mond", "dchi2", "L", "valid")}
    if r["valid"]:
        out["p_newton"] = float(stats.chi2.sf(r["chi2_newton"], len(med) - 1))
        _, LN, LM, ok = pm.g2_symmetric(np.asarray(med), np.asarray(sig), xmed)
        out["g2"] = {"L_N_data": LN, "L_M_data": LM, "passes": ok}
        out["grade"] = grade(r["L"])
    return out


def analyse(df, edges, min_per_bin, n_boot, seed, a0, gne, pm, error_models=False):
    """R5 statistic on a sample from build_sample: bins, merge, stratified bootstrap, fits, G2."""
    x = df["x"].to_numpy()
    b = wb.bin_index(x, edges)
    counts_raw = [int(np.sum(b == k)) for k in range(len(edges) + 1)]
    mapping, evaluable = wb.merge_outer(counts_raw, min_per_bin)
    out = {"N": int(len(df)), "counts_raw": counts_raw, "evaluable": bool(evaluable)}
    if not evaluable:
        out["valid"] = False
        return out
    fb = np.array([mapping[k] for k in b])
    nfin = max(mapping) + 1
    order = np.lexsort((df["source_id_b"].to_numpy(), df["source_id_a"].to_numpy()))
    vt = df["vt"].to_numpy()
    med = wb.bin_medians(vt, fb, nfin)
    xmed = np.array([np.median(x[fb == k]) for k in range(nfin)])
    sig = stratified_sigma(vt[order], fb[order], nfin, n_boot, seed)
    sig_ok = bool(np.all(np.isfinite(sig)) and np.all(sig > 0))
    out.update({"mapping": [int(m) for m in mapping], "counts": [int(np.sum(fb == k)) for k in range(nfin)],
                "medians": med.tolist(), "x_median": xmed.tolist(), "sigma": sig.tolist(), "sigma_ok": sig_ok})
    fit = _fit(med, xmed, sig, a0, gne, pm) if sig_ok else {"valid": False}
    out["valid"] = bool(sig_ok and fit.get("valid"))
    out["fit"] = fit if out["valid"] else {"valid": False}      # invalid: listed without L
    if error_models and out["valid"]:
        out["error_models"] = error_model_variants(vt, fb, nfin, med, xmed, sig, a0, gne, pm, min_per_bin)
    return out


def error_model_variants(vt, fb, nfin, med, xmed, sig, a0, gne, pm, min_per_bin):
    """E1-E5 of README 2.1 on the R5 main sample (descriptive)."""
    N = np.array([int(np.sum(fb == k)) for k in range(nfin)])
    res = {}
    cov, frac, ok = wb.bootstrap_cov(vt, fb, nfin, 2000, 0, min_per_bin)
    r = wb.compare_models(med, xmed, cov, a0, gne)
    e1 = {"L": r["L"], "dchi2": r["dchi2"], "valid": bool(ok and r["valid"]), "redraw_fraction": frac,
          "used_diagonal": r["used_diagonal"]}
    if e1["valid"]:
        e1["grade"] = grade(r["L"])
        _, LN, LM, g = pm.g2_symmetric(med, np.sqrt(np.diag(cov)), xmed)
        e1["g2"] = {"L_N_data": LN, "L_M_data": LM, "passes": g}
    res["E1_whole_sample_bootstrap"] = e1
    k2 = float(np.sum(N * (N * sig ** 2 / med ** 2)) / np.sum(N))
    res["E2_pooled_scale"] = _fit(med, xmed, med * np.sqrt(k2) / np.sqrt(N), a0, gne, pm) | {"k": math.sqrt(k2)}
    res["E3_mad"] = _fit(med, xmed, wb.mad_errors(vt, fb, nfin, 1.0), a0, gne, pm)
    res["E4_mad_1.4826"] = _fit(med, xmed, wb.mad_errors(vt, fb, nfin, 1.4826), a0, gne, pm)
    f = wb.compare_models(med, xmed, np.diag(sig ** 2), a0, gne)
    if f["valid"]:
        shape = wb.mond_boost(xmed, a0, gne)
        chi2_tied = float(np.sum(((med - f["A_newton"] * shape) / sig) ** 2))
        d = chi2_tied - f["chi2_newton"]
        L = float(math.exp(min(d / 2.0, 700.0)))
        res["E5_tied_A"] = {"chi2_mond_tied": chi2_tied, "dchi2": d, "L": L, "grade": grade(L), "valid": True}
    else:
        res["E5_tied_A"] = {"valid": False}
    return res


def shell_descriptives(df, edges, mapping, pbar_split=6.6667):
    """Per final bin, the medians of v~ and x and N for d < 150 pc (pbar > 6.6667) and 150-250 pc."""
    x = df["x"].to_numpy()
    fb = np.array([mapping[k] for k in wb.bin_index(x, edges)])
    nfin = max(mapping) + 1
    out = {}
    for name, m in (("d_lt_150", df["pbar"].to_numpy() > pbar_split), ("d_150_250", df["pbar"].to_numpy() <= pbar_split)):
        rows = []
        for k in range(nfin):
            sel = m & (fb == k)
            rows.append({"N": int(sel.sum()),
                         "median_vt": float(np.median(df["vt"].to_numpy()[sel])) if sel.any() else None,
                         "median_x": float(np.median(x[sel])) if sel.any() else None})
        out[name] = rows
    return out


# R5 variants (README 2.1): keys understood by run.build_sample, plus P overrides
VARIANTS = {
    "R5": ({}, {}),
    "V1_d130": ({"d_max_pc": 130.0}, {}),
    "V2_d200": ({"d_max_pc": 200.0}, {}),
    "V3_theta_ge_2.31": ({"theta_min_arcsec": 2.31}, {}),
    "V4_rsky_ge_1000": ({}, {"rsky_min_au": 1000.0}),
    "V5_x_ge_0.0504": ({"x_min": 0.0504}, {}),
    "V6_no_hr": ({"no_hr": True}, {}),
    "V7a_c_plus_0.2": ({"c_shift": 0.2}, {}),
    "V7b_c_minus_0.2": ({"c_shift": -0.2}, {}),
    "V8_no_degroup": ({"no_degroup": True}, {}),
    "V9_c25_degroup": ({}, {}),            # same flags; run.py passes the N2-C25 table
    "V10_vt_le_2": ({"vt_max": 2.0}, {}),
    "V11_vt_le_1.5": ({"vt_max": 1.5}, {}),
    "V12_ipd0": ({"ipd_zero": True}, {}),
    "V13_parallax_snr100": ({"parallax_snr_min": 100.0}, {}),
    "V14_shell_150_250": ({"pbar_max": 6.6667}, {}),
}


def now_utc():
    return datetime.now(timezone.utc)


def parse_utc(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def read_before_merge(retrieved_at_list, merge=MERGE_TIME_UTC):
    """True if any N4 record with rows was retrieved (downloaded) before the merge time."""
    m = parse_utc(merge)
    for t in retrieved_at_list:
        d = parse_utc(t)
        if d.tzinfo is None:
            d = d.replace(tzinfo=timezone.utc)
        if d < m:
            return True
    return False
