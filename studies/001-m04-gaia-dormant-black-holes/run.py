"""M4: Gaia dormant black holes - DR3 reproduction and DR4-ready screen.

Run with:  python -m astrolab run 001
Pre-registered hypotheses and criteria: README.md sections 1-4.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

from astrolab import orbits
from screen import SCHEMAS, mass_function_subquery, screen_adql

RELEASE = "dr3"
FM_MIN = 0.25
PLX_SNR_MIN = 5.0
M2_BH_MIN = 3.0          # Msun; above the maximum neutron-star mass

# Published values (verified against arXiv full text, plan 003)
TARGETS = {
    "Gaia BH1": {"gaia_dr3": 4373465352415301632, "m1": 0.93, "m1_err": 0.05, "m2_paper": 9.62, "m2_paper_err": 0.18,
                 "p_paper": 185.59, "ref": "El-Badry et al. 2023a, arXiv:2209.06833"},
    "Gaia BH2": {"gaia_dr3": 5870569352746779008, "m1": 1.07, "m1_err": 0.19, "m2_paper": 8.9, "m2_paper_err": 0.3,
                 "p_paper": 1276.7, "ref": "El-Badry et al. 2023b, arXiv:2302.07880"},
    "Gaia BH3": {"gaia_dr3": 4318465066420528000, "m1": None, "m1_err": None, "m2_paper": 32.70, "m2_paper_err": 0.82,
                 "p_paper": 11.6 * 365.25, "ref": "Gaia Collaboration, Panuzzo et al. 2024, arXiv:2404.10486"},
}

ERR_PARAMS = ["ra", "dec", "parallax", "pmra", "pmdec", "a_thiele_innes", "b_thiele_innes", "f_thiele_innes",
              "g_thiele_innes", "c_thiele_innes", "h_thiele_innes", "center_of_mass_velocity",
              "eccentricity", "period", "t_periastron"]


def _ids(values):
    return ", ".join(str(int(v)) for v in values)


def reproduce_targets(ctx):
    s = SCHEMAS[RELEASE]
    ids = _ids(t["gaia_dr3"] for t in TARGETS.values())
    cols = ", ".join([f"{p}, {p}_error" for p in ERR_PARAMS])
    nss = ctx.tap(f"SELECT source_id, nss_solution_type, {cols}, bit_index, corr_vec, significance, goodness_of_fit "
                  f"FROM {s}.nss_two_body_orbit WHERE source_id IN ({ids})",
                  label="BH NSS solutions", release="Gaia DR3", max_rows=10)
    pos = ctx.tap(f"SELECT source_id, ra, dec, l, b, parallax, phot_g_mean_mag, bp_rp FROM {s}.gaia_source "
                  f"WHERE source_id IN ({ids})", label="BH positions", release="Gaia DR3", max_rows=10)

    out, targets = [], []
    for name, t in TARGETS.items():
        p = pos[pos.source_id == t["gaia_dr3"]]
        if len(p):
            r = p.iloc[0]
            targets.append({"name": name, "gaia_dr3": str(t["gaia_dr3"]), "ra": r.ra, "dec": r.dec, "l": r.l, "b": r.b,
                            "dist_pc": 1000 / r.parallax, "G": r.phot_g_mean_mag})
        rows = nss[nss.source_id == t["gaia_dr3"]]
        rec = {"name": name, "gaia_dr3": str(t["gaia_dr3"]), "ref": t["ref"], "m2_paper": t["m2_paper"],
               "m2_paper_err": t["m2_paper_err"], "p_paper_d": t["p_paper"]}
        if rows.empty:
            rec["status"] = "no DR3 orbital solution (expected for BH3)"
            out.append(rec)
            continue
        row = rows.iloc[0]
        mc = orbits.sample_companion_mass(row, t["m1"], t["m1_err"], n=20000, seed=42)
        q = lambda a: np.percentile(a, [16, 50, 84])
        m2_lo, m2, m2_hi = q(mc["m2"])
        sig_ours = 0.5 * (m2_hi - m2_lo)
        sig_comb = float(np.hypot(sig_ours, t["m2_paper_err"]))
        dev = (m2 - t["m2_paper"]) / sig_comb
        hist, edges = np.histogram(mc["m2"], bins=60, range=(max(0, m2 - 5 * sig_ours), m2 + 5 * sig_ours))
        rec.update({
            "status": "computed", "solution_type": row.nss_solution_type,
            "period_dr3_d": row.period, "period_dr3_err_d": row.period_error,
            "parallax_mas": row.parallax, "a0_mas": float(np.median(mc["a0_mas"])),
            "f_m": [float(x) for x in q(mc["f_m"])],
            "m1": t["m1"], "m1_err": t["m1_err"],
            "m2": [m2_lo, m2, m2_hi], "deviation_sigma": float(dev),
            "pass_2sigma": bool(abs(dev) < 2),
            "m2_hist": {"counts": hist, "edges": edges},
        })
        ctx.log(f"{name}: M2 = {m2:.2f} (+{m2_hi - m2:.2f}/-{m2 - m2_lo:.2f}) vs paper {t['m2_paper']} "
                f"-> {dev:+.2f} sigma")
        out.append(rec)
    return out, targets


def flag_row(r):
    flags = []
    if not np.isfinite(r.mass_flame):
        flags.append("no-FLAME-mass")
    abs_g = r.phot_g_mean_mag + 5 * np.log10(r.parallax / 100.0)
    if (np.isfinite(r.radius_flame) and r.radius_flame > 3) or (abs_g < 3.0 and r.bp_rp > 0.9):
        flags.append("giant")
    if r.significance < 20:
        flags.append("low-significance")
    if r.parallax / r.parallax_error < 20:
        flags.append("plx-snr<20")
    if r.eccentricity > 0.8:
        flags.append("e>0.8")
    return flags


def run_screen(ctx):
    n = ctx.count(f"({mass_function_subquery(RELEASE, PLX_SNR_MIN)}) AS q WHERE q.f_m > {FM_MIN}")
    df = ctx.tap(screen_adql(RELEASE, FM_MIN, PLX_SNR_MIN), label=f"screen f_M>{FM_MIN}", release="Gaia DR3",
                 max_rows=50000, mode="async")
    assert len(df) == n, (len(df), n)
    df["m1_used"] = df.mass_flame.where(np.isfinite(df.mass_flame), 1.0)
    df["m2"] = orbits.companion_mass(df.f_m.to_numpy(), df.m1_used.to_numpy())
    df["abs_g"] = df.phot_g_mean_mag + 5 * np.log10(df.parallax / 100.0)
    df["qc"] = [",".join(flag_row(r)) for r in df.itertuples()]
    return df


def ns_recall(ctx, screen_df):
    path = Path(__file__).parent / "data" / "ns_candidates_elbadry2024.json"
    tab = json.loads(path.read_text(encoding="utf-8"))
    ns = pd.DataFrame(tab["rows"], columns=tab["columns"])
    ns["gaia_dr3"] = ns.gaia_dr3.astype("int64")
    # their f_M regardless of the screen cut, computed server-side
    direct = ctx.tap(f"SELECT q.source_id, q.nss_solution_type, q.f_m, q.parallax, q.parallax_error, q.period "
                     f"FROM ({mass_function_subquery(RELEASE, 0.0)}) AS q WHERE q.source_id IN ({_ids(ns.gaia_dr3)})",
                     label="NS candidates f_M", release="Gaia DR3", max_rows=50)
    ns = ns.merge(direct, how="left", left_on="gaia_dr3", right_on="source_id")
    ns["in_screen"] = ns.gaia_dr3.isin(screen_df.source_id)
    return ns, tab["source"]


# ---------------------------------------------------------------------------
# POST-HOC (added 2026-11-11 after the independent referee review; see README s6).
# Not part of the pre-registration. Every veto is validated on positive controls
# (BH1, BH2, the 21 El-Badry+24 NS candidates) and reported as such.
# ---------------------------------------------------------------------------
UNVALIDATED_TYPES = {"OrbitalAlternative", "OrbitalTargetedSearch"}  # Holl et al. 2023: non-validated subsets
RV_RATIO_MIN = 0.5   # veto if rv_amplitude_robust < 0.5 x predicted min-to-max RV amplitude
KMS_PER_AU_PER_YR = 4.740470


def predicted_rv_range(A, B, F, G, ecc, period_d, parallax):
    """Min-to-max RV of the luminous star implied by the astrometric orbit [km/s] (= 2K).

    cos i = (AG - BF) / a0^2 from the Thiele-Innes constants.
    """
    G = np.where(np.isfinite(G), G, -A * F / B)
    a0 = orbits.a0_mas(A, B, F, G)
    cos_i = np.clip((A * G - B * F) / a0**2, -1, 1)
    a1_au = a0 / parallax
    p_yr = period_d / orbits.DAYS_PER_YEAR
    K = 2 * np.pi * a1_au * np.sqrt(1 - cos_i**2) / (p_yr * np.sqrt(1 - ecc**2)) * KMS_PER_AU_PER_YR
    return 2 * K, np.degrees(np.arccos(cos_i))


def vet(ctx, ids):
    s = SCHEMAS[RELEASE]
    df = ctx.tap(
        f"SELECT o.source_id, o.nss_solution_type, o.a_thiele_innes, o.b_thiele_innes, o.f_thiele_innes, "
        f"o.g_thiele_innes, o.eccentricity, o.period, o.parallax, g.rv_amplitude_robust, g.rv_nb_transits "
        f"FROM {s}.nss_two_body_orbit AS o JOIN {s}.gaia_source AS g ON g.source_id = o.source_id "
        f"WHERE o.source_id IN ({_ids(ids)})", label="vetting inputs", release="Gaia DR3", max_rows=2000)
    rng, inc = predicted_rv_range(df.a_thiele_innes.to_numpy(), df.b_thiele_innes.to_numpy(), df.f_thiele_innes.to_numpy(),
                                  df.g_thiele_innes.to_numpy(), df.eccentricity.fillna(0).to_numpy(),
                                  df.period.to_numpy(), df.parallax.to_numpy())
    df["rv_range_pred"], df["inclination_deg"] = rng, inc
    df["rv_ratio"] = df.rv_amplitude_robust / df.rv_range_pred
    df["veto_type"] = df.nss_solution_type.isin(UNVALIDATED_TYPES)
    df["veto_rv"] = df.rv_ratio < RV_RATIO_MIN          # NaN (no RV amplitude) -> False
    df["vetoed"] = df.veto_type | df.veto_rv
    # A source can carry more than one NSS solution: key = (source_id, nss_solution_type).
    return df


def main(ctx):
    repro, targets = reproduce_targets(ctx)
    ctx.save("targets", targets)
    ctx.save("reproduction", repro)

    sc = run_screen(ctx)
    bh_ids = {t["gaia_dr3"] for t in TARGETS.values()}
    cand = sc[sc.m2 > M2_BH_MIN].sort_values("m2", ascending=False)
    cand = cand.assign(known=cand.source_id.isin(bh_ids))

    # literature verdicts (El-Badry+23a Table E1)
    lit_tab = json.loads((Path(__file__).parent / "data" / "literature_vetting.json").read_text(encoding="utf-8"))
    lit = {int(r[0]): r[1] for r in lit_tab["rows"]}
    cand["literature"] = cand.source_id.map(lambda i: lit.get(int(i), ""))

    # post-hoc vetoes on candidates and on positive controls
    ns_tab = json.loads((Path(__file__).parent / "data" / "ns_candidates_elbadry2024.json").read_text(encoding="utf-8"))
    ns_ids = [int(r[1]) for r in ns_tab["rows"]]
    controls = {"Gaia BH1": TARGETS["Gaia BH1"]["gaia_dr3"], "Gaia BH2": TARGETS["Gaia BH2"]["gaia_dr3"]}
    v = vet(ctx, sorted(set(cand.source_id.astype("int64")) | set(controls.values()) | set(ns_ids)))
    vcols = ["source_id", "nss_solution_type", "rv_amplitude_robust", "rv_range_pred", "rv_ratio", "veto_type", "veto_rv", "vetoed"]
    cand = cand.drop(columns=[c for c in vcols[2:] if c in cand]).merge(v[vcols], how="left", on=["source_id", "nss_solution_type"])
    cand = cand.sort_values("m2", ascending=False)
    ctrl_ids = list(controls.values()) + ns_ids
    ctrl = v[v.source_id.isin(ctrl_ids)].set_index("source_id")
    controls_vetoed = [f"{i} ({r.nss_solution_type})" for i, r in ctrl.iterrows() if r.vetoed]
    multi = v.groupby("source_id").size()
    multi_solution_ids = [str(i) for i in multi[multi > 1].index]

    keep = ["source_id", "nss_solution_type", "period", "eccentricity", "parallax", "parallax_error", "significance",
            "a0_mas", "f_m", "m1_used", "m2", "ra", "dec", "phot_g_mean_mag", "bp_rp", "abs_g", "ruwe", "qc", "known",
            "literature", "rv_amplitude_robust", "rv_range_pred", "rv_ratio", "veto_type", "veto_rv", "vetoed"]
    out = cand[keep].copy()
    out["source_id"] = out.source_id.astype(str)
    ctx.save("bh_candidates", out.round(4))
    ctx.save("vetting_controls", {
        "note": "POST-HOC vetoes (2026-11-11, after referee). Positive controls must not be vetoed.",
        "rules": {"veto_type": sorted(UNVALIDATED_TYPES), "veto_rv": f"rv_amplitude_robust < {RV_RATIO_MIN} x predicted min-to-max RV"},
        "rows": [{"source_id": str(i), "role": next((k for k, x in controls.items() if x == i), "NS candidate"),
                  "type": r.nss_solution_type, "rv_amplitude_robust": r.rv_amplitude_robust,
                  "rv_range_pred": r.rv_range_pred, "rv_ratio": r.rv_ratio, "vetoed": bool(r.vetoed)}
                 for i, r in ctrl.iterrows()],
    })
    plot = sc[["f_m", "period", "m2", "m1_used", "abs_g", "bp_rp", "nss_solution_type"]].copy()
    plot["source_id"] = sc.source_id.astype(str)
    ctx.save("screen_points", plot.round(4))

    ns, ns_src = ns_recall(ctx, sc)
    ns_out = ns[["name", "gaia_dr3", "m2", "m2_err", "period_d", "nss_solution_type", "f_m", "parallax", "in_screen"]].copy()
    ns_out["gaia_dr3"] = ns_out.gaia_dr3.astype(str)
    ctx.save("ns_recall", {"source": ns_src, "rows": ns_out.round(4)})

    bh_rec = {r["name"]: r for r in repro}
    # S1 as pre-registered: BH1/BH2 M2 from the screen's f_M with their PUBLISHED M1 (fixed after referee).
    s1 = {}
    for name in ("Gaia BH1", "Gaia BH2"):
        t = TARGETS[name]
        row = sc[sc.source_id == t["gaia_dr3"]]
        m2 = float(orbits.companion_mass(row.f_m.iloc[0], t["m1"])) if len(row) else None
        s1[name] = {"m2_published_m1": m2, "pass": bool(m2 is not None and m2 > M2_BH_MIN)}
    n_recall = int(ns.in_screen.sum())
    unexplained = out[~out.known & (out.qc == "")]
    survivors = out[~out.known & ~out.vetoed & (out.literature != "refuted")]
    n_total = ctx.count(f"{SCHEMAS[RELEASE]}.nss_two_body_orbit WHERE a_thiele_innes IS NOT NULL")
    n_null_a0 = ctx.count(f"({mass_function_subquery(RELEASE, PLX_SNR_MIN)}) AS q WHERE q.a0_mas IS NULL")
    b1 = bh_rec["Gaia BH1"]
    ref1 = lit_tab["dr3_only_reference"]["Gaia BH1"]
    summary = {
        "release": RELEASE,
        "R1_BH1": {k: b1.get(k) for k in ("m2", "deviation_sigma", "pass_2sigma", "period_dr3_d")},
        "R2_BH2": {k: bh_rec["Gaia BH2"].get(k) for k in ("m2", "deviation_sigma", "pass_2sigma", "period_dr3_d")},
        "S1_rows": len(sc), "S1_rows_ok": len(sc) < 50000, "S1_published_m1": s1,
        "S1_pass": len(sc) < 50000 and all(x["pass"] for x in s1.values()),
        "S2_ns_recall": f"{n_recall}/{len(ns)}", "S2_pass": n_recall >= 19,
        "S2_weakest_ns_f_m": float(ns.f_m.min()),
        "S3_candidates_m2_gt_3": len(out), "S3_known": int(out.known.sum()),
        "S3_unflagged_unknown_preregistered_labels": len(unexplained),
        "S3_flag_counts": out.qc.str.split(",").explode().replace("", "none").value_counts().to_dict(),
        "S3_labels_on_known_bh": dict(zip(out[out.known].source_id, out[out.known].qc)),
        "D1_dr4_query_ok": "FROM gaiadr4.nss_two_body_orbit" in screen_adql("dr4", FM_MIN, PLX_SNR_MIN),
        "astrometric_solutions_total": n_total,
        "rows_dropped_null_a0": n_null_a0,
        "post_hoc": {
            "note": "Added 2026-11-11 after referee review; not pre-registered.",
            "R1b_bh1_vs_dr3_only_paper": {
                "a0_ours": b1["a0_mas"], "a0_paper": ref1["a0_mas"],
                "a0_dev_sigma": (b1["a0_mas"] - ref1["a0_mas"][0]) / ref1["a0_mas"][1],
                "m2_ours": b1["m2"][1], "m2_paper": ref1["m2"],
                "m2_dev_sigma": (b1["m2"][1] - ref1["m2"][0]) / ref1["m2"][1],
            },
            "controls_vetoed": controls_vetoed,
            "controls_checked": len(ctrl),
            "sources_with_multiple_solutions_among_vetted": multi_solution_ids,
            "candidates_vetoed_type": int(out.veto_type.sum()), "candidates_vetoed_rv": int(out.veto_rv.sum()),
            "literature_refuted_in_list": int((out.literature == "refuted").sum()),
            "survivors_not_known_not_vetoed_not_refuted": len(survivors),
            "survivors_by_label": survivors.qc.replace("", "none").value_counts().to_dict(),
        },
    }
    # Full DR4 screen query, ready for release day (confirm schema/columns via TAP_SCHEMA first).
    ctx.save("dr4_screen_query", {"release": "dr4", "fm_min": FM_MIN, "plx_snr_min": PLX_SNR_MIN,
                                  "adql": screen_adql("dr4", FM_MIN, PLX_SNR_MIN)})
    ctx.save("summary", summary)
    return summary
