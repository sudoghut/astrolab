"""M4: Gaia dormant black holes - DR3 reproduction and DR4 screen.

Run with:  python -m astrolab run 001          (formal run: results/)
Explore:   python -m astrolab explore 001 --tag <topic> --set release=dr4
Pre-registered hypotheses and criteria: README.md sections 1-4 (with the DR4 addendum).
Release parameterisation: design/008-plan_m04-release-parameterisation-and-dr4-pre-registration.md.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

from astrolab import orbits
from astrolab.results import to_jsonable
from screen import ASTROMETRIC_TYPES, FLAME_COLS, SCHEMAS, mass_function_subquery, screen_adql, screen_from_where
import selection as sel

# Knobs (AGENTS.md section 2). Read inside main(); saved with the results.
PARAMS = {
    "release": "dr3",
    "fm_min": 0.25,           # server-side pre-selection on the mass function [Msun]
    "plx_snr_min": 5.0,       # parallax S/N cut
    "m2_bh_min": 3.0,         # companion mass above which a source is a BH candidate [Msun]
    "rv_ratio_min": 0.5,      # RV veto: rv_amplitude_robust < this x predicted min-to-max RV
    "unvalidated_types": ["OrbitalAlternative", "OrbitalTargetedSearch"],  # type veto (Holl et al. 2023)
}

# Per-release constants. Part of the pre-registration (README DR4 addendum): changes are recorded.
RELEASES = {
    "dr3": {"label": "Gaia DR3", "rv_veto": None, "covariance_trusted": True, "epoch_gap_yr": 0.0},
    # Set on release day from metadata/documentation only, before any source-level DR4 data are
    # fetched (information barrier): covariance_trusted (corr_vec order), epoch_gap_yr (DR4
    # reference epoch - 2016.0).
    "dr4": {"label": "Gaia DR4", "rv_veto": {"max_period_d": 1000.0, "max_ecc": 0.8},
            "covariance_trusted": False, "epoch_gap_yr": 1.5},
}

# Published values (verified against arXiv full text: plan 003; BH3 plan 008)
TARGETS = {
    "Gaia BH1": {"gaia_dr3": 4373465352415301632, "m1": 0.93, "m1_err": 0.05, "m2_paper": 9.62, "m2_paper_err": 0.18,
                 "p_paper": 185.59, "ref": "El-Badry et al. 2023a, arXiv:2209.06833"},
    "Gaia BH2": {"gaia_dr3": 5870569352746779008, "m1": 1.07, "m1_err": 0.19, "m2_paper": 8.9, "m2_paper_err": 0.3,
                 "p_paper": 1276.7, "ref": "El-Badry et al. 2023b, arXiv:2302.07880"},
    "Gaia BH3": {"gaia_dr3": 4318465066420528000, "m1": 0.76, "m1_err": 0.05, "m2_paper": 32.70, "m2_paper_err": 0.82,
                 "p_paper": 4253.1, "ref": "Gaia Collaboration, Panuzzo et al. 2024, arXiv:2404.10486 (Tables 2, 3)"},
}

ERR_PARAMS = ["ra", "dec", "parallax", "pmra", "pmdec", "a_thiele_innes", "b_thiele_innes", "f_thiele_innes",
              "g_thiele_innes", "c_thiele_innes", "h_thiele_innes", "center_of_mass_velocity",
              "eccentricity", "period", "t_periastron"]

# Optional per-row columns: if a release lacks one, it is fetched as missing (README DR4 addendum:
# no RV column -> RV veto not applicable; no FLAME mass -> counts as absent).
OPTIONAL_COLUMNS = {"gaia_source": ["rv_amplitude_robust", "rv_nb_transits"],
                    "astrophysical_parameters": list(FLAME_COLS)}
# Columns that must exist; if TAP_SCHEMA does not list them, the metadata lookup failed: stop.
CORE_COLUMNS = {"gaia_source": "source_id", "astrophysical_parameters": "source_id"}
# Orbit columns identifying one solution (a LEFT JOIN that doubles a row repeats these exactly).
SOLUTION_KEY = ["source_id", "nss_solution_type", "period", "a_thiele_innes", "b_thiele_innes",
                "f_thiele_innes", "g_thiele_innes"]

# Every result file this study writes; a run writes all of them (placeholders where not applicable),
# so results/ never mixes files of two releases.
OUTPUTS = ["targets", "reproduction", "vetting_controls", "bh_candidates", "screen_points", "ns_recall",
           "dr4_screen_query", "reference_ids", "survivors_dr4", "new_candidates_dr4", "summary", "release"]

RESULT_MAX_BYTES = 1024**2       # AGENTS.md section 1: each results file < 1 MB
SCREEN_ROWS_MAX = 50000          # pre-registered S1 (and S1-DR4, S3-DR4 stop rule) bound
CANDIDATE_ROWS_MAX = 2000        # bh_candidates / new_candidates_dr4 cap (~0.8 MB)
CHUNK = 500                      # ids per IN (...) list
DATA = Path(__file__).parent / "data"


def _ids(values):
    return ", ".join(str(int(v)) for v in values)


def _chunks(ids, n=CHUNK):
    ids = sorted({int(i) for i in ids})
    return [ids[k:k + n] for k in range(0, len(ids), n)]


def _rows(obj):
    """results JSON (column dict or list of records) -> DataFrame."""
    return pd.DataFrame(obj) if isinstance(obj, dict) else pd.DataFrame.from_records(obj)


def _placeholder(release, why):
    return {"release": release, "status": why}


# ---------------------------------------------------------------------------------------------
# Results directory: release marker, guard, DR3 reference

def _release_of(d: Path):
    for name in ("release.json", "summary.json"):
        f = d / name
        if f.exists():
            return json.loads(f.read_text(encoding="utf-8")).get("release")
    return None


def _finished_at(d: Path):
    f = d / "run_info.json"
    return json.loads(f.read_text(encoding="utf-8")).get("finished_at") if f.exists() else None


def guard_results(ctx, release):
    """A formal run never overwrites another release's results unless an up-to-date archive exists."""
    if ctx.results != ctx.study.results_dir:
        return  # exploration: writes to explore/<date>-<tag>/
    res = ctx.study.results_dir
    old = _release_of(res)
    if not old or old == release:
        return
    arch = res / old
    hint = (f"python .claude/skills/gaia-dr4-release-day/dr4_query.py archive {old} "
            f"(remove a stale results/{old}/ first; it is in git)")
    if _release_of(arch) != old:
        raise SystemExit(f"results/ holds the {old} run, not archived in results/{old}/. Archive it: {hint}")
    if _finished_at(arch) != _finished_at(res):
        raise SystemExit(f"results/{old}/ is older than the {old} run in results/ (run_info.json differs). "
                         f"Re-archive: {hint}")


def dr3_reference_dir(ctx) -> Path:
    """Archived DR3 results (results/dr3/), or results/ itself while it still holds the DR3 run."""
    for d in (ctx.study.results_dir / "dr3", ctx.study.results_dir):
        if _release_of(d) == "dr3":
            return d
    raise SystemExit("no DR3 results to compare with (results/dr3/ or results/ with release dr3)")


# ---------------------------------------------------------------------------------------------
# Queries

def available_columns(ctx, schema, label):
    """Which optional per-row columns this release has (TAP_SCHEMA: metadata, barrier-safe)."""
    names = ", ".join(f"'{schema}.{t}'" for t in OPTIONAL_COLUMNS)
    meta = ctx.tap(f"SELECT table_name, column_name FROM tap_schema.columns WHERE table_name IN ({names})",
                   label="optional columns (TAP_SCHEMA)", release=label, max_rows=2000)
    have = {(str(t).split(".")[-1], str(c).lower()) for t, c in zip(meta.table_name, meta.column_name)}
    missing_core = [f"{t}.{c}" for t, c in CORE_COLUMNS.items() if (t, c) not in have]
    if missing_core:
        raise SystemExit(f"TAP_SCHEMA lists no {missing_core} for schema {schema}: the metadata lookup failed "
                         f"(table renamed or table_name format differs). Fix before running; nothing written.")
    return {c for t, cols in OPTIONAL_COLUMNS.items() for c in cols if (t, c) in have}


def fetch_solutions(ctx, schema, label, ids, what, optional=None):
    """All NSS solutions of `ids`, with photometry, RV amplitude and FLAME mass; chunked IN lists.

    optional: available optional columns (None = all, the DR3 query text); missing ones are NaN.
    """
    optional = set(OPTIONAL_COLUMNS["gaia_source"] + OPTIONAL_COLUMNS["astrophysical_parameters"]) \
        if optional is None else set(optional)
    o_cols = ", ".join(f"o.{p}, o.{p}_error" for p in ERR_PARAMS)
    g_opt = "".join(f", g.{c}" for c in OPTIONAL_COLUMNS["gaia_source"] if c in optional)
    ap_opt = [c for c in OPTIONAL_COLUMNS["astrophysical_parameters"] if c in optional]
    ap_sel = "".join(f", ap.{c}" for c in ap_opt)
    ap_join = (f"LEFT OUTER JOIN {schema}.astrophysical_parameters AS ap ON ap.source_id = o.source_id "
               if ap_opt else "")
    frames = []
    for chunk in _chunks(ids):
        frames.append(ctx.tap(
            f"SELECT o.source_id, o.nss_solution_type, {o_cols}, o.bit_index, o.corr_vec, o.significance, "
            f"o.goodness_of_fit, o.flags, g.phot_g_mean_mag, g.bp_rp, g.ruwe{g_opt}{ap_sel} "
            f"FROM {schema}.nss_two_body_orbit AS o JOIN {schema}.gaia_source AS g ON g.source_id = o.source_id "
            f"{ap_join}WHERE o.source_id IN ({_ids(chunk)})",
            label=f"{what} solutions", release=label, max_rows=SCREEN_ROWS_MAX))
    df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    if df.empty:   # typed empty frame: a later concat must not turn 19-digit ids into float64
        df = pd.DataFrame({c: pd.Series(dtype="int64" if c == "source_id" else "object" if c == "nss_solution_type"
                                        else "float64") for c in SOLUTION_KEY + ["significance", "goodness_of_fit",
                                                                                 "parallax", "parallax_error",
                                                                                 "period_error", "eccentricity"]})
    for c in OPTIONAL_COLUMNS["gaia_source"] + OPTIONAL_COLUMNS["astrophysical_parameters"]:
        if c not in df:
            df[c] = np.nan
    df["source_id"] = df.source_id.astype("int64")
    # A doubled LEFT JOIN row (several FLAME rows per source) repeats the solution: keep one, and treat
    # its FLAME values as absent (ambiguous). Distinct solutions, even of the same type, all stay:
    # R-sel chooses between them, never the server's row order (README DR4 addendum).
    dup = df.duplicated(SOLUTION_KEY, keep=False)
    if dup.any():
        for c in OPTIONAL_COLUMNS["astrophysical_parameters"]:
            df.loc[dup, c] = np.nan
        df = df.drop_duplicates(SOLUTION_KEY).reset_index(drop=True)
    df.attrs["ambiguous_flame_sources"] = int(dup.sum())
    if len(df):
        _, a0, fm = sel.solution_m2(df, 1.0)
        df["a0_mas"], df["f_m"] = a0, fm
    else:
        df["a0_mas"], df["f_m"] = pd.Series(dtype=float), pd.Series(dtype=float)
    return df


def count_solutions(ctx, schema, ids):
    return sum(ctx.count(f"{schema}.nss_two_body_orbit WHERE source_id IN ({_ids(c)})") for c in _chunks(ids))


def target_positions(ctx, schema, label):
    return ctx.tap(f"SELECT source_id, ra, dec, l, b, parallax, phot_g_mean_mag, bp_rp FROM {schema}.gaia_source "
                   f"WHERE source_id IN ({_ids(t['gaia_dr3'] for t in TARGETS.values())})",
                   label="BH positions", release=label, max_rows=10)


def run_screen(ctx, params, schema, label, release, flame=True):
    n = ctx.count(screen_from_where(release, params["fm_min"], params["plx_snr_min"]))
    if n >= SCREEN_ROWS_MAX:
        ctx.log(f"screen count {n:,} >= {SCREEN_ROWS_MAX:,}: S1 fails; screen not fetched")
        return None, n
    df = ctx.tap(screen_adql(release, params["fm_min"], params["plx_snr_min"], flame=flame),
                 label=f"screen f_M>{params['fm_min']}", release=label, max_rows=SCREEN_ROWS_MAX, mode="async")
    assert len(df) == n, (len(df), n)
    for c in ("mass_flame", "mass_flame_lower", "mass_flame_upper", "radius_flame"):
        if c not in df:
            df[c] = np.nan
    df["m1_used"] = df.mass_flame.where(np.isfinite(df.mass_flame), 1.0)
    df["m2"] = orbits.companion_mass(df.f_m.to_numpy(), df.m1_used.to_numpy())
    df["abs_g"] = df.phot_g_mean_mag + 5 * np.log10(df.parallax / 100.0)
    df["qc"] = [",".join(flag_row(r)) for r in df.itertuples()]
    return df, n


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


def ns_table():
    tab = json.loads((DATA / "ns_candidates_elbadry2024.json").read_text(encoding="utf-8"))
    ns = pd.DataFrame(tab["rows"], columns=tab["columns"])
    ns["gaia_dr3"] = ns.gaia_dr3.astype("int64")
    return ns, tab["source"]


def ns_recall(ctx, release, label, screen_df):
    ns, src = ns_table()
    direct = ctx.tap(f"SELECT q.source_id, q.nss_solution_type, q.f_m, q.parallax, q.parallax_error, q.period "
                     f"FROM ({mass_function_subquery(release, 0.0)}) AS q WHERE q.source_id IN ({_ids(ns.gaia_dr3)})",
                     label="NS candidates f_M", release=label, max_rows=500)
    ns = ns.merge(direct, how="left", left_on="gaia_dr3", right_on="source_id")
    ns["in_screen"] = ns.gaia_dr3.isin(screen_df.source_id)
    return ns, src


# ---------------------------------------------------------------------------------------------
# Targets (R1-R3)

def reproduce_targets(ctx, params, rel, id_map, sol, positions):
    """id_map: name -> source_id in this release (None: unresolved). sol: vetted solutions."""
    label = rel["label"]
    prim = sel.primary_solutions(sol, params["unvalidated_types"], ASTROMETRIC_TYPES) if not sol.empty else sol
    out, targets = [], []
    for name, t in TARGETS.items():
        p = positions[positions.source_id == t["gaia_dr3"]]
        if len(p):
            r = p.iloc[0]
            targets.append({"name": name, "source_id": str(t["gaia_dr3"]), "ra": r.ra, "dec": r.dec, "l": r.l,
                            "b": r.b, "dist_pc": 1000 / r.parallax, "G": r.phot_g_mean_mag})
        rec = {"name": name, "source_id": str(t["gaia_dr3"]), "ref": t["ref"], "m2_paper": t["m2_paper"],
               "m2_paper_err": t["m2_paper_err"], "p_paper_d": t["p_paper"], "m1": t["m1"], "m1_err": t["m1_err"]}
        sid = id_map.get(name)
        if sid is None:
            rec.update(status="unresolved", evaluable=False)
            out.append(rec)
            continue
        rows = prim[prim.source_id == sid] if not prim.empty else prim
        if rows.empty:
            rec.update(status=f"no {label} orbital solution", evaluable=False)
            out.append(rec)
            continue
        row = rows.iloc[0]
        rec["solutions"] = sorted(sol[sol.source_id == sid].nss_solution_type.tolist())
        rec.update(status="computed", solution_type=row.nss_solution_type, period_d=row.period,
                   period_err_d=row.period_error, parallax_mas=row.parallax)
        c = sel.central_mass(row, t["m1"])
        mc = None
        if rel["covariance_trusted"]:
            try:
                mc = orbits.sample_companion_mass(row, t["m1"], t["m1_err"], n=20000, seed=42)
            except (ValueError, KeyError, np.linalg.LinAlgError) as e:
                # corr_vec length, unfitted G, unknown type, missing field, non-PSD covariance
                rec["covariance_error"] = f"{type(e).__name__}: {e}"
        if mc is not None:
            q = lambda a: np.percentile(a, [16, 50, 84])
            m2_lo, m2, m2_hi = q(mc["m2"])
            sig_ours = 0.5 * (m2_hi - m2_lo)
            sig_comb = float(np.hypot(sig_ours, t["m2_paper_err"]))
            dev = (m2 - t["m2_paper"]) / sig_comb
            hist, edges = np.histogram(mc["m2"], bins=60, range=(max(0, m2 - 5 * sig_ours), m2 + 5 * sig_ours))
            rec.update(a0_mas=float(np.median(mc["a0_mas"])), f_m=[float(x) for x in q(mc["f_m"])],
                       m2=[m2_lo, m2, m2_hi], deviation_sigma=float(dev), pass_2sigma=bool(abs(dev) < 2),
                       evaluable=True, m2_hist={"counts": hist, "edges": edges})
            ctx.log(f"{name}: M2 = {m2:.2f} (+{m2_hi - m2:.2f}/-{m2 - m2_lo:.2f}) vs paper {t['m2_paper']} "
                    f"-> {dev:+.2f} sigma")
        else:
            why = rec.get("covariance_error") or "covariance not trusted for this release"
            rec.update(a0_mas=c["a0_mas"], f_m=[None, c["f_m"], None], m2=[None, c["m2"], None],
                       deviation_sigma=None, pass_2sigma=None, evaluable=False,
                       note=f"{why}: central values only (README DR4 addendum)")
            ctx.log(f"{name}: central M2 = {c['m2']:.2f} ({why}; not evaluable)")
        out.append(rec)
    return out, targets


# ---------------------------------------------------------------------------------------------
# DR4-only criteria (README DR4 addendum to section 2)

def resolve_dr3_ids(ctx, schema, label, rel, ref_dir):
    ref = _rows(json.loads((ref_dir / "reference_ids.json").read_text(encoding="utf-8")))
    ref["source_id"] = ref.source_id.astype("int64")
    frames = [ctx.tap(f"SELECT source_id, ra, dec, pmra, pmdec, phot_g_mean_mag FROM {schema}.gaia_source "
                      f"WHERE source_id IN ({_ids(c)})", label="DR3 id resolution", release=label,
                      max_rows=len(c) + 10) for c in _chunks(ref.source_id)]
    found = pd.concat(frames, ignore_index=True)
    return sel.resolve_ids(ref, found, rel["epoch_gap_yr"])


def dr4_criteria(params, rel, res, sol_all, target_recs, screen_df, screen_n, ref_dir, s3_sol, s3_count):
    """All DR4 criteria from data already fetched (no network here). Returns (summary, survivors, new_cands).

    s3_sol: vetted solutions of the screen sources with M2 > m2_bh_min, or None if the stop rule fired.
    """
    unval, m2_min = params["unvalidated_types"], params["m2_bh_min"]
    dmap = {int(r.dr3_id): (None if pd.isna(r.dr4_id) else int(r.dr4_id)) for r in res.itertuples()}
    prim = sel.primary_solutions(sol_all, unval, ASTROMETRIC_TYPES)
    prim_by = {int(r.source_id): r._asdict() for r in prim.itertuples(index=False)} if not prim.empty else {}

    def primary_of(dr3_id):
        d4 = dmap.get(int(dr3_id))
        return (d4 is not None), (dict(prim_by[d4]) if d4 in prim_by else None)

    # R1-R3
    r = {}
    for rec in target_recs:
        ok = rec.get("evaluable", False)
        r[rec["name"]] = {"status": rec["status"], "evaluable": ok, "m2": rec.get("m2"),
                          "deviation_sigma": rec.get("deviation_sigma"), "note": rec.get("note"),
                          "verdict": ("pass" if rec.get("pass_2sigma") else "fail") if ok else "not evaluable"}

    # S1-DR4
    s1_m2 = {}
    for name, t in TARGETS.items():
        _, p = primary_of(t["gaia_dr3"])
        s1_m2[name] = sel.central_mass(p, t["m1"])["m2"] if p is not None else None
    s1 = sel.s1_targets(s1_m2, m2_min)
    s1["screen_rows"] = screen_n
    s1["screen_rows_ok"] = screen_n < SCREEN_ROWS_MAX
    if not s1["screen_rows_ok"]:
        s1["verdict"] = "fail"

    # S2-DR4 (independent of the screen)
    ns, _ = ns_table()
    passes, ns_rows = [], []
    for sid in ns.gaia_dr3:
        resolved, p = primary_of(sid)
        ok = sel.in_screen_cuts(p, ASTROMETRIC_TYPES, params["plx_snr_min"], params["fm_min"]) if p else None
        if p is not None:
            passes.append(ok)
        ns_rows.append({"gaia_dr3": str(sid), "resolved": resolved, "has_solution": p is not None, "passes_cuts": ok})
    s2 = sel.s2_dr4(len(ns), passes)
    s2["catalogue_recall"] = f"{sum(x['has_solution'] for x in ns_rows)}/{len(ns)}"
    s2["rows"] = ns_rows

    # V-DR4 (controls judged on their primary solution)
    ctrl_ids = [t["gaia_dr3"] for t in TARGETS.values()] + list(ns.gaia_dr3)
    ctrl_prims = [prim_by[dmap[i]] for i in ctrl_ids if dmap.get(i) in prim_by]
    v = sel.v_dr4(pd.DataFrame(ctrl_prims), len(ctrl_ids))
    v["without_solution_or_unresolved"] = [str(i) for i in ctrl_ids if dmap.get(i) not in prim_by]

    # F-DR4 (the 51 DR3 survivors)
    cand3 = _rows(json.loads((ref_dir / "bh_candidates.json").read_text(encoding="utf-8")))
    cand3["source_id"] = cand3.source_id.astype("int64")
    surv = cand3[~cand3.known.astype(bool) & ~cand3.vetoed.astype(bool) & (cand3.literature != "refuted")]
    surv = surv.drop_duplicates("source_id")
    f_rows = []
    for ref in surv.to_dict("records"):
        resolved, p = primary_of(ref["source_id"])
        if p is not None:
            p["m2"] = float(sel.central_mass(p, sel.m1_for(p, ref["m1_used"]))["m2"])
        lab = sel.label_survivor(resolved, p, ref, unval, params["plx_snr_min"], m2_min)
        row = {"source_id": str(ref["source_id"]), "label": lab, "period_dr3": ref["period"],
               "period_err_dr3": ref.get("period_error"), "resolution": None if resolved else
               res.set_index("dr3_id").reason.get(int(ref["source_id"]))}
        if p is not None:
            pr = p["period"] / ref["period"]
            row.update(type_dr4=p["nss_solution_type"], period_dr4=p["period"], m2_dr4=p["m2"],
                       rv_veto_applicable=bool(p["rv_veto_applicable"]), period_ratio=pr,
                       a0_ratio=p["a0_mas"] / ref["a0_mas"], possible_alias=sel.possible_alias(pr))
        f_rows.append(row)
    labels = pd.Series([x["label"] for x in f_rows], dtype=object)
    f = {"n": len(f_rows), "counts": {k: int((labels == k).sum()) for k in sel.LABELS},
         "n_rv_applicable": int(sum(x.get("rv_veto_applicable", False) for x in f_rows)),
         "n_period_dr3_gt_1000d": int((surv.period > 1000).sum())}

    # S3-DR4 (new candidates; primary among all solutions)
    new_rows = pd.DataFrame()
    if screen_df is None:
        s3 = {"verdict": "not evaluable", "reason": "screen not fetched (S1-DR4 row bound)"}
    elif s3_sol is None:
        s3 = {"verdict": "not evaluable", "reason": f"all-solutions count {s3_count} > {SCREEN_ROWS_MAX}"}
    else:
        dr3_87 = {dmap.get(int(i)) for i in cand3.source_id}
        hi = screen_df[screen_df.m2 > m2_min]
        new_ids = sorted(set(hi.source_id.astype("int64")) - dr3_87)
        p3 = sel.primary_solutions(s3_sol[s3_sol.source_id.isin(new_ids)], unval, ASTROMETRIC_TYPES)
        if len(p3):
            p3 = p3.copy()
            p3["m1_used"] = p3.mass_flame.where(np.isfinite(p3.mass_flame), 1.0)
            p3["m2"] = sel.solution_m2(p3, p3.m1_used.to_numpy())[0]
            p3["qc"] = [",".join(flag_row(x)) for x in p3.itertuples()]
            p3["known_target"] = p3.source_id.isin([dmap.get(t["gaia_dr3"]) for t in TARGETS.values()])
            new_rows = p3
        s3 = {"verdict": "reported", "n_new": len(new_ids),
              "n_primary_m2_gt_min": int((new_rows.m2 > m2_min).sum()) if len(new_rows) else 0,
              "n_vetoed": int(new_rows.vetoed.sum()) if len(new_rows) else 0,
              "known_targets_among_new": [str(i) for i in new_rows.source_id[new_rows.known_target]]
              if len(new_rows) else [],
              "ids": [str(i) for i in new_ids], "n_candidate_solutions_counted": s3_count}

    return {"R": r, "S1": s1, "S2": s2, "V": v, "F": f, "S3": s3,
            "resolution": {"n": len(res), "unresolved": int(res.dr4_id.isna().sum()),
                           "reasons": res[res.dr4_id.isna()].reason.value_counts().to_dict()}}, f_rows, new_rows


# ---------------------------------------------------------------------------------------------

def main(ctx):
    params = dict(PARAMS)
    release = params["release"]
    if release not in RELEASES or release not in SCHEMAS:
        raise SystemExit(f"release must be one of {sorted(RELEASES)}, not {release!r}")
    rel, schema = RELEASES[release], SCHEMAS[release]
    label = rel["label"]
    unval = params["unvalidated_types"]
    guard_results(ctx, release)
    out = {name: _placeholder(release, "not applicable to this release") for name in OUTPUTS}

    ns, ns_src = ns_table()
    lit_tab = json.loads((DATA / "literature_vetting.json").read_text(encoding="utf-8"))
    lit = {int(r[0]): r[1] for r in lit_tab["rows"]}
    controls = {name: t["gaia_dr3"] for name, t in TARGETS.items()}
    ctrl_dr3 = list(controls.values()) + list(ns.gaia_dr3)

    # DR3 ids -> ids in this release (DR3: identity; DR4: identity-checked resolution)
    if release == "dr3":
        res, ref_dir, optional = None, None, None
        dmap = {int(i): int(i) for i in ctrl_dr3}
    else:
        ref_dir = dr3_reference_dir(ctx)
        optional = available_columns(ctx, schema, label)
        res = resolve_dr3_ids(ctx, schema, label, rel, ref_dir)
        dmap = {int(r.dr3_id): (None if pd.isna(r.dr4_id) else int(r.dr4_id)) for r in res.itertuples()}
    id_map = {name: dmap.get(int(sid)) for name, sid in controls.items()}
    flame = True if optional is None else [c for c in FLAME_COLS if c in optional]

    sc, screen_n = run_screen(ctx, params, schema, label, release, flame=flame)
    cand = sc[sc.m2 > params["m2_bh_min"]].sort_values("m2", ascending=False) if sc is not None else None

    # Solutions, vetted per row. DR3: controls + candidates (as before). DR4: controls and resolved
    # DR3 ids first; the screen candidates' solutions only after a server-side count (S3 stop rule).
    want = {dmap.get(int(i)) for i in ctrl_dr3} - {None}
    if release == "dr3" and cand is not None:
        want |= set(cand.source_id.astype("int64"))
    if res is not None:
        want |= {int(i) for i in res.dr4_id.dropna()}
    sol = fetch_solutions(ctx, schema, label, want, "vetting", optional)
    ambiguous_flame = sol.attrs.get("ambiguous_flame_sources", 0)
    s3_sol, s3_count = None, 0
    if release != "dr3" and cand is not None:
        extra = set(cand.source_id.astype("int64")) - set(sol.source_id if not sol.empty else [])
        s3_count = count_solutions(ctx, schema, extra) if extra else 0
        if s3_count <= SCREEN_ROWS_MAX:
            more = fetch_solutions(ctx, schema, label, extra, "screen candidates", optional) if extra else sol.iloc[:0]
            ambiguous_flame += more.attrs.get("ambiguous_flame_sources", 0)
            sol = pd.concat([sol, more], ignore_index=True) if len(more) else sol   # extra excludes ids in sol
            s3_sol = True
    sol = sel.apply_vetoes(sol, unval, params["rv_ratio_min"], rel["rv_veto"])
    if s3_sol is True:
        s3_sol = sol

    repro, targets = reproduce_targets(ctx, params, rel, id_map, sol, target_positions(ctx, schema, label))
    out["targets"], out["reproduction"] = targets, repro

    # Controls: vetoed if the primary solution is vetoed (README s5 note 2026-11-14). Ids in this release.
    prim = sel.primary_solutions(sol, unval, ASTROMETRIC_TYPES)
    ctrl_ids = {dmap.get(int(i)): int(i) for i in ctrl_dr3}
    ctrl_prim = prim[prim.source_id.isin([i for i in ctrl_ids if i is not None])].set_index("source_id")
    controls_vetoed = [f"{i} ({r.nss_solution_type})" for i, r in ctrl_prim.iterrows() if r.vetoed]
    controls_without = [str(i) for i in ctrl_dr3 if dmap.get(int(i)) not in ctrl_prim.index]
    multi = sol.groupby("source_id").size() if not sol.empty else pd.Series(dtype=int)
    out["vetting_controls"] = {
        "release": release,
        "note": "Vetoes validated on positive controls (post-hoc 2026-11-11; per primary solution from 2026-11-14).",
        "rules": {"veto_type": sorted(unval),
                  "veto_rv": f"rv_amplitude_robust < {params['rv_ratio_min']} x predicted min-to-max RV",
                  "rv_veto_applicable": rel["rv_veto"] or "always"},
        "rows": [{"source_id": str(i), "dr3_id": str(ctrl_ids[i]),
                  "role": next((k for k, x in controls.items() if x == ctrl_ids[i]), "NS candidate"),
                  "type": r.nss_solution_type, "rv_amplitude_robust": r.rv_amplitude_robust,
                  "rv_range_pred": r.rv_range_pred, "rv_ratio": r.rv_ratio, "vetoed": bool(r.vetoed)}
                 for i, r in ctrl_prim.iterrows()],
    }

    summary = {"release": release, "params": params, "astrometric_types": list(ASTROMETRIC_TYPES),
               "release_constants": rel, "optional_columns": sorted(optional) if optional is not None else "all",
               "ambiguous_flame_sources": int(ambiguous_flame),
               "sources_with_same_type_solutions": [str(i) for i, n in
                                                    sol.groupby(["source_id", "nss_solution_type"]).size().items()
                                                    if n > 1] if len(sol) else []}
    screen_desc = {}
    if sc is None:
        why = f"screen not fetched: {screen_n} rows >= {SCREEN_ROWS_MAX} (S1 fails)"
        for name in ("bh_candidates", "screen_points", "ns_recall"):
            out[name] = _placeholder(release, why)
    else:
        bh_ids = {dmap.get(int(i)) for i in controls.values()} - {None}
        cand = cand.assign(known=cand.source_id.isin(bh_ids))
        cand["literature"] = cand.source_id.map(lambda i: lit.get(int(i), ""))
        vcols = ["source_id", "nss_solution_type", "rv_amplitude_robust", "rv_range_pred", "rv_ratio", "veto_type",
                 "veto_rv", "vetoed"]
        # one screen row = one solution: match on the solution, not only its type
        cand = cand.merge(sol[vcols + ["period"]], how="left", on=["source_id", "nss_solution_type", "period"])
        cand["vetted"] = cand.vetoed.notna()                # False only if the S3 stop rule fired
        cand["vetoed"] = cand.vetoed.fillna(False).astype(bool)
        cand = cand.sort_values("m2", ascending=False)
        keep = ["source_id", "nss_solution_type", "period", "period_error", "eccentricity", "parallax",
                "parallax_error", "significance", "a0_mas", "f_m", "m1_used", "m2", "ra", "dec", "phot_g_mean_mag",
                "bp_rp", "abs_g", "ruwe", "qc", "known", "literature", "rv_amplitude_robust", "rv_range_pred",
                "rv_ratio", "veto_type", "veto_rv", "vetoed"] + ([] if release == "dr3" else ["vetted"])
        cout = cand[keep].copy()
        cout["source_id"] = cout.source_id.astype(str)
        survivors = cout[~cout.known & ~cout.vetoed & (cout.literature != "refuted")]
        unexplained = cout[~cout.known & (cout.qc == "")]
        cout_capped, cap_info = sel.cap_rows(cout, CANDIDATE_ROWS_MAX)
        out["bh_candidates"] = cout_capped.round(4)
        plot = sc[["f_m", "period", "m2", "m1_used", "abs_g", "bp_rp", "nss_solution_type"]].copy()
        plot["source_id"] = sc.source_id.astype(str)
        plot, thin_info = sel.thin_screen_points(plot)
        out["screen_points"] = plot.round(4)
        ns_r, _ = ns_recall(ctx, release, label, sc)
        ns_out = ns_r[["name", "gaia_dr3", "m2", "m2_err", "period_d", "nss_solution_type", "f_m", "parallax",
                       "in_screen"]].copy()
        ns_out["gaia_dr3"] = ns_out.gaia_dr3.astype(str)
        out["ns_recall"] = {"release": release, "source": ns_src, "rows": ns_out.round(4)}
        n_recall = int(ns_r.in_screen.sum())
        screen_desc = {
            "S1_rows": len(sc), "S1_rows_ok": len(sc) < SCREEN_ROWS_MAX,
            "S2_ns_recall": f"{n_recall}/{len(ns_r)}", "S2_pass": n_recall >= 19,
            "S2_weakest_ns_f_m": float(ns_r.f_m.min()),
            "S3_candidates_m2_gt_3": len(cout), "S3_known": int(cout.known.sum()),
            "S3_unflagged_unknown_preregistered_labels": len(unexplained),
            "S3_flag_counts": cout.qc.str.split(",").explode().replace("", "none").value_counts().to_dict(),
            "S3_labels_on_known_bh": dict(zip(cout[cout.known].source_id, cout[cout.known].qc)),
            "bh_candidates_rows": cap_info, "screen_points_rows": thin_info,
        }

    summary["astrometric_solutions_total"] = ctx.count(f"{schema}.nss_two_body_orbit WHERE a_thiele_innes IS NOT NULL")
    summary["rows_dropped_null_a0"] = ctx.count(f"({mass_function_subquery(release, params['plx_snr_min'])}) AS q "
                                                f"WHERE q.a0_mas IS NULL")
    post_hoc = {"note": "Added 2026-11-11 after referee review; not pre-registered. Controls judged on their "
                        "primary solution from 2026-11-14 (no DR3 verdict or count changes).",
                "controls_vetoed": controls_vetoed, "controls_checked": len(ctrl_prim),
                "controls_without_solution": controls_without,
                "sources_with_multiple_solutions_among_vetted": [str(i) for i in multi[multi > 1].index]}

    if release == "dr3":
        rec = {r["name"]: r for r in repro}
        summary.update(screen_desc)   # the DR3 pre-registered keys, top level as before
        s1 = {}
        for name in ("Gaia BH1", "Gaia BH2"):
            t = TARGETS[name]
            row = sc[sc.source_id == t["gaia_dr3"]]
            m2 = float(orbits.companion_mass(row.f_m.iloc[0], t["m1"])) if len(row) else None
            s1[name] = {"m2_published_m1": m2, "pass": bool(m2 is not None and m2 > params["m2_bh_min"])}
        b1 = rec["Gaia BH1"]
        ref1 = lit_tab["dr3_only_reference"]["Gaia BH1"]
        summary.update({
            "R1_BH1": {k: b1.get(k) for k in ("m2", "deviation_sigma", "pass_2sigma", "period_d")},
            "R2_BH2": {k: rec["Gaia BH2"].get(k) for k in ("m2", "deviation_sigma", "pass_2sigma", "period_d")},
            "S1_published_m1": s1, "S1_pass": len(sc) < SCREEN_ROWS_MAX and all(x["pass"] for x in s1.values()),
            "D1_dr4_query_ok": f"FROM {SCHEMAS['dr4']}.nss_two_body_orbit" in screen_adql("dr4", params["fm_min"],
                                                                                         params["plx_snr_min"]),
        })
        post_hoc.update({
            "R1b_bh1_vs_dr3_only_paper": {
                "a0_ours": b1["a0_mas"], "a0_paper": ref1["a0_mas"],
                "a0_dev_sigma": (b1["a0_mas"] - ref1["a0_mas"][0]) / ref1["a0_mas"][1],
                "m2_ours": b1["m2"][1], "m2_paper": ref1["m2"],
                "m2_dev_sigma": (b1["m2"][1] - ref1["m2"][0]) / ref1["m2"][1]},
            "candidates_vetoed_type": int(cout.veto_type.fillna(False).astype(bool).sum()),
            "candidates_vetoed_rv": int(cout.veto_rv.fillna(False).astype(bool).sum()),
            "literature_refuted_in_list": int((cout.literature == "refuted").sum()),
            "survivors_not_known_not_vetoed_not_refuted": len(survivors),
            "survivors_by_label": survivors.qc.replace("", "none").value_counts().to_dict(),
        })
        out["dr4_screen_query"] = {"release": "dr4", "fm_min": params["fm_min"], "plx_snr_min": params["plx_snr_min"],
                                   "adql": screen_adql("dr4", params["fm_min"], params["plx_snr_min"])}
        # DR3 position and G of every DR3 id the study uses, for the DR4 identity check
        ref_ids = sorted(set(cand.source_id.astype("int64")) | set(int(i) for i in ns.gaia_dr3) | set(lit)
                         | set(controls.values()))
        refs = pd.concat([ctx.tap(f"SELECT source_id, ra, dec, phot_g_mean_mag FROM {schema}.gaia_source "
                                  f"WHERE source_id IN ({_ids(c)})", label="DR3 reference ids", release=label,
                                  max_rows=len(c) + 10) for c in _chunks(ref_ids)], ignore_index=True)
        refs["source_id"] = refs.source_id.astype(str)
        out["reference_ids"] = refs
        summary["reference_ids"] = len(refs)
    else:
        summary["screen_descriptive"] = dict(screen_desc, note=(
            "Descriptive only: DR3-style counts on this release's screen (raw DR3 ids for the NS recall). "
            "The pre-registered DR4 verdicts are in summary.dr4."))
        dr4, f_rows, new_rows = dr4_criteria(params, rel, res, sol, repro, sc, screen_n, ref_dir, s3_sol, s3_count)
        summary["dr4"] = dr4
        out["survivors_dr4"] = {"release": release, "rows": f_rows}
        if len(new_rows):
            s3_out = new_rows[["source_id", "nss_solution_type", "period", "parallax", "a0_mas", "f_m", "m1_used",
                               "m2", "qc", "known_target", "veto_type", "veto_rv", "vetoed"]].copy()
            s3_out["source_id"] = s3_out.source_id.astype(str)
            s3_out, info = sel.cap_rows(s3_out, CANDIDATE_ROWS_MAX)
            out["new_candidates_dr4"] = s3_out.round(4)
            summary["dr4"]["S3"]["rows_saved"] = info
        else:
            out["new_candidates_dr4"] = _placeholder(release, dr4["S3"].get("reason", "no new candidates"))
    summary["post_hoc"] = post_hoc
    out["summary"] = summary
    out["release"] = {"release": release}

    # size check for every file before anything is written (no half-written results/); no default=str,
    # so an unserialisable value fails here, not in the middle of the save loop
    too_big = {}
    for name, obj in out.items():
        size = len(json.dumps(to_jsonable(obj), indent=1, ensure_ascii=False).encode("utf-8"))
        if size > RESULT_MAX_BYTES:
            too_big[name] = size
    if too_big:
        raise SystemExit(f"result files over {RESULT_MAX_BYTES} bytes: {too_big}; nothing written")
    for name in OUTPUTS:
        ctx.save(name, out[name])
    return summary
