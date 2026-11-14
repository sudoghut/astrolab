"""Pre-registered selection and labelling rules of M4 (README section 2 and its DR4 addendum).

Pure functions on pandas frames: no network, no reading of run.py. run.py passes PARAMS values
and the RELEASES entry in as arguments (AGENTS.md section 2), so explorations that override
PARAMS take effect here too.
"""
from __future__ import annotations

import math

import numpy as np
import pandas as pd

from astrolab import orbits

KMS_PER_AU_PER_YR = 4.740470

# R-sel type preference among validated solutions (lower is preferred); other types rank last.
TYPE_RANK = {"AstroSpectroSB1": 0, "Orbital": 1}

LABELS = ("unresolved", "solution-gone", "type-vetoed", "insufficient", "rv-vetoed", "mass-below",
          "period-changed", "persists")


# ---------------------------------------------------------------------------------------------
# Primary solution (R-sel)

def primary_solutions(sol: pd.DataFrame, unvalidated_types, astrometric_types) -> pd.DataFrame:
    """One row per source_id, chosen by R-sel; never depends on row order.

    Order: validated before non-validated; AstroSpectroSB1, Orbital, others; highest significance;
    smallest |goodness_of_fit|; lexicographically smallest type; smallest period; then the Thiele-Innes
    constants A, B, F, G ascending (rows equal on all of these are the same solution and are collapsed
    upstream); missing values last.
    Only solutions of astrometric type are eligible.
    """
    if sol.empty:
        return sol.copy()
    s = sol[sol.nss_solution_type.isin(list(astrometric_types))].copy()
    if s.empty:
        return s
    big = np.inf
    s["_k1"] = s.nss_solution_type.isin(list(unvalidated_types)).astype(int)
    s["_k2"] = s.nss_solution_type.map(lambda t: TYPE_RANK.get(t, 2))
    s["_k3"] = -s.significance.astype(float).fillna(-big) if "significance" in s else 0.0
    s["_k4"] = s.goodness_of_fit.astype(float).abs().fillna(big) if "goodness_of_fit" in s else 0.0
    s["_k5"] = s.nss_solution_type.astype(str)
    s["_k6"] = s.period.astype(float).fillna(big)
    ti = []
    for i, c in enumerate(("a_thiele_innes", "b_thiele_innes", "f_thiele_innes", "g_thiele_innes")):
        if c not in s:   # without them a full tie would fall back on row order
            raise ValueError(f"R-sel needs column {c}")
        s[f"_k7{i}"] = s[c].astype(float).fillna(big)
        ti.append(f"_k7{i}")
    s = s.sort_values(["source_id", "_k1", "_k2", "_k3", "_k4", "_k5", "_k6"] + ti, kind="mergesort")
    out = s.drop_duplicates("source_id", keep="first")
    return out.drop(columns=[c for c in out if c.startswith("_k")]).reset_index(drop=True)


# ---------------------------------------------------------------------------------------------
# Vetoes

def predicted_rv_range(A, B, F, G, ecc, period_d, parallax):
    """Min-to-max RV of the luminous star implied by the astrometric orbit [km/s] (= 2K).

    cos i = (AG - BF) / a0^2 from the Thiele-Innes constants.
    """
    A, B, F, G, ecc, period_d, parallax = (np.asarray(x, float) for x in (A, B, F, G, ecc, period_d, parallax))
    G = np.where(np.isfinite(G), G, -A * F / B)
    a0 = orbits.a0_mas(A, B, F, G)
    cos_i = np.clip((A * G - B * F) / a0**2, -1, 1)
    a1_au = a0 / parallax
    p_yr = period_d / orbits.DAYS_PER_YEAR
    K = 2 * np.pi * a1_au * np.sqrt(1 - cos_i**2) / (p_yr * np.sqrt(1 - ecc**2)) * KMS_PER_AU_PER_YR
    return 2 * K, np.degrees(np.arccos(cos_i))


def rv_veto_applicable(period_d, ecc, rule) -> np.ndarray:
    """RELEASES[...]["rv_veto"]: None = always applicable (DR3 rule); else {"max_period_d", "max_ecc"}."""
    period_d = np.asarray(period_d, float)
    if rule is None:
        return np.ones(period_d.shape, bool)
    ecc = np.nan_to_num(np.asarray(ecc, float), nan=0.0)
    return (period_d < rule["max_period_d"]) & (ecc < rule["max_ecc"])


def apply_vetoes(sol: pd.DataFrame, unvalidated_types, rv_ratio_min, rv_rule) -> pd.DataFrame:
    """Add rv_range_pred, inclination_deg, rv_ratio, rv_veto_applicable, veto_type, veto_rv, vetoed."""
    df = sol.copy()
    if df.empty:
        for c in ("rv_range_pred", "inclination_deg", "rv_ratio"):
            df[c] = pd.Series(dtype=float)
        for c in ("rv_veto_applicable", "veto_type", "veto_rv", "vetoed"):
            df[c] = pd.Series(dtype=bool)
        return df
    rng, inc = predicted_rv_range(df.a_thiele_innes, df.b_thiele_innes, df.f_thiele_innes, df.g_thiele_innes,
                                  df.eccentricity.fillna(0), df.period, df.parallax)
    df["rv_range_pred"], df["inclination_deg"] = rng, inc
    amp = df["rv_amplitude_robust"] if "rv_amplitude_robust" in df else pd.Series(np.nan, index=df.index)
    df["rv_ratio"] = amp / df.rv_range_pred
    df["rv_veto_applicable"] = rv_veto_applicable(df.period, df.eccentricity, rv_rule) & amp.notna().to_numpy()
    df["veto_type"] = df.nss_solution_type.isin(list(unvalidated_types))
    df["veto_rv"] = df.rv_veto_applicable & (df.rv_ratio < rv_ratio_min)   # NaN ratio -> False
    df["vetoed"] = df.veto_type | df.veto_rv
    return df


# ---------------------------------------------------------------------------------------------
# Mass

def central_mass(row, m1) -> dict:
    """Central-value a0, f_M, M2 of one solution (used when the covariance is not trusted)."""
    G = row["g_thiele_innes"]
    if not np.isfinite(G):
        G = -row["a_thiele_innes"] * row["f_thiele_innes"] / row["b_thiele_innes"]
    a0 = float(orbits.a0_mas(row["a_thiele_innes"], row["b_thiele_innes"], row["f_thiele_innes"], G))
    fm = float(orbits.mass_function(a0, row["parallax"], row["period"]))
    return {"a0_mas": a0, "f_m": fm, "m2": float(orbits.companion_mass(fm, m1))}


def solution_m2(sol: pd.DataFrame, m1) -> np.ndarray:
    G = np.where(np.isfinite(sol.g_thiele_innes), sol.g_thiele_innes, -sol.a_thiele_innes * sol.f_thiele_innes / sol.b_thiele_innes)
    a0 = orbits.a0_mas(sol.a_thiele_innes, sol.b_thiele_innes, sol.f_thiele_innes, G)
    fm = orbits.mass_function(a0, sol.parallax, sol.period)
    return orbits.companion_mass(fm, m1), a0, fm


def in_screen_cuts(row, astrometric_types, plx_snr_min, fm_min) -> bool:
    """The screen's cuts evaluated on one fetched solution (S2: same meaning as in_screen on DR3)."""
    if row["nss_solution_type"] not in set(astrometric_types):
        return False
    plx, plx_err = row["parallax"], row["parallax_error"]
    if not (np.isfinite(plx) and np.isfinite(plx_err) and plx > 0 and plx_err > 0 and plx / plx_err > plx_snr_min):
        return False
    _, _, fm = solution_m2(pd.DataFrame([row]), 1.0)
    return bool(np.isfinite(fm[0]) and fm[0] > fm_min)


# ---------------------------------------------------------------------------------------------
# Resolution of DR3 ids in DR4

def identity_check(ref: dict, new: dict, epoch_gap_yr: float, max_offset_arcsec=2.0, max_dg=0.3):
    """(ok, reason). ref: DR3 ra, dec, phot_g_mean_mag; new: DR4 ra, dec, pmra, pmdec, phot_g_mean_mag.

    The DR3 position is moved to the DR4 epoch with the DR4 proper motion (none if DR4 has none).
    """
    pmra, pmdec = new.get("pmra"), new.get("pmdec")
    dra_pm = (pmra if pmra is not None and np.isfinite(pmra) else 0.0) * epoch_gap_yr / 1000.0   # arcsec
    ddec_pm = (pmdec if pmdec is not None and np.isfinite(pmdec) else 0.0) * epoch_gap_yr / 1000.0
    dra_deg = (new["ra"] - ref["ra"] + 180.0) % 360.0 - 180.0          # wrap at 0/360
    dra = dra_deg * math.cos(math.radians(ref["dec"])) * 3600 - dra_pm
    ddec = (new["dec"] - ref["dec"]) * 3600 - ddec_pm
    if not math.hypot(dra, ddec) < max_offset_arcsec:
        return False, "offset"
    g_new, g_ref = new.get("phot_g_mean_mag"), ref.get("phot_g_mean_mag")
    if g_new is None or g_ref is None or not np.isfinite(g_new) or not np.isfinite(g_ref) or not abs(g_new - g_ref) < max_dg:
        return False, "magnitude"
    return True, ""


def resolve_ids(reference: pd.DataFrame, found: pd.DataFrame, epoch_gap_yr: float) -> pd.DataFrame:
    """Direct-id resolution with the identity check. Columns: dr3_id, dr4_id (or <NA>), reason."""
    ids = found.source_id.astype("int64")
    dup = set(ids[ids.duplicated(keep=False)].tolist())
    by_id = {int(r.source_id): r._asdict() for r in found.itertuples(index=False)}
    rows = []
    for r in reference.itertuples(index=False):
        sid = int(r.source_id)
        if sid in dup:   # several rows for one id: ambiguous, never chosen by row order
            rows.append((sid, None, "ambiguous"))
            continue
        new = by_id.get(sid)
        if new is None:
            rows.append((sid, None, "not-found"))
            continue
        ok, why = identity_check(r._asdict(), new, epoch_gap_yr)
        rows.append((sid, sid if ok else None, why))
    # Build the id columns as exact integers: a None among 19-digit ids would otherwise make pandas
    # go through float64 and silently corrupt every id (> 2**53).
    return pd.DataFrame({
        "dr3_id": pd.array([r[0] for r in rows], dtype="int64"),
        "dr4_id": pd.array([r[1] for r in rows], dtype="Int64"),
        "reason": [r[2] for r in rows],
    })


def apply_neighbourhood(res: pd.DataFrame, reference: pd.DataFrame, nb: pd.DataFrame, found_new: pd.DataFrame,
                        epoch_gap_yr: float, tie_arcsec=0.1) -> pd.DataFrame:
    """Cross-match fallback for ids the direct lookup did not resolve (README DR4 addendum, Resolution).

    nb: columns old_id, new_id, dist_arcsec (the release's DR3-DR4 neighbourhood table, converted).
    found_new: DR4 gaia_source rows (source_id, ra, dec, pmra, pmdec, phot_g_mean_mag) of the new ids.
    Nearest neighbour; two within tie_arcsec of the same distance, or a failed identity check: no match.
    """
    out = res.copy()
    ref_by = {int(r.source_id): r._asdict() for r in reference.itertuples(index=False)}
    new_by = {int(r.source_id): r._asdict() for r in found_new.itertuples(index=False)}
    nb = nb.assign(old_id=nb.old_id.astype("int64"), new_id=nb.new_id.astype("int64"))
    dr4 = list(out.dr4_id)
    reason = list(out.reason)
    for k, r in enumerate(out.itertuples(index=False)):
        if not pd.isna(r.dr4_id):
            continue
        cand = nb[nb.old_id == int(r.dr3_id)].sort_values(["dist_arcsec", "new_id"], kind="mergesort")
        if cand.empty:
            continue
        if len(cand) > 1 and cand.dist_arcsec.iloc[1] - cand.dist_arcsec.iloc[0] <= tie_arcsec:
            reason[k] = "neighbourhood-ambiguous"
            continue
        new_id = int(cand.new_id.iloc[0])
        new = new_by.get(new_id)
        if new is None:
            reason[k] = "neighbourhood-not-found"
            continue
        ok, why = identity_check(ref_by[int(r.dr3_id)], new, epoch_gap_yr)
        if ok:
            dr4[k], reason[k] = new_id, "neighbourhood"
        else:
            reason[k] = f"neighbourhood-{why}"
    out["dr4_id"] = pd.array([None if pd.isna(x) else int(x) for x in dr4], dtype="Int64")
    out["reason"] = reason
    return out


# ---------------------------------------------------------------------------------------------
# DR4 criteria

def s2_dr4(n_candidates: int, primaries_pass: list[bool], n_min=15, frac=0.9) -> dict:
    """primaries_pass: one bool per NS candidate that resolves and has a DR4 astrometric solution."""
    n_eval, n_pass = len(primaries_pass), int(sum(primaries_pass))
    need = math.ceil(frac * n_eval)
    verdict = "not evaluable" if n_eval < n_min else ("pass" if n_pass >= need else "fail")
    return {"n_candidates": n_candidates, "n_eval": n_eval, "passed": n_pass, "needed": need, "verdict": verdict}


def v_dr4(control_primaries: pd.DataFrame, n_controls: int, n_min=15, rv_weak_below=5) -> dict:
    """control_primaries: vetted primary solutions of the controls that resolve and have one."""
    n = len(control_primaries)
    vetoed = control_primaries[control_primaries.vetoed.astype(bool)] if n else control_primaries
    n_rv = int(control_primaries.rv_veto_applicable.sum()) if n else 0
    verdict = "not evaluable" if n < n_min else ("pass" if len(vetoed) == 0 else "fail")
    return {"n_controls": n_controls, "n_counted": n, "n_vetoed": int(len(vetoed)),
            "vetoed": [str(int(i)) for i in vetoed.source_id] if n else [],
            "n_rv_applicable": n_rv, "rv_half_weak": n_rv < rv_weak_below, "verdict": verdict}


def s1_targets(target_m2: dict, m2_min: float, n_min=2) -> dict:
    """target_m2: name -> M2, or None when the target is missing (unresolved / no solution).

    A target that has a solution but a non-finite M2 (e.g. parallax <= 0) is evaluable and fails:
    only a missing target is "not evaluable" (README S1-DR4).
    """
    ev = {k: v for k, v in target_m2.items() if v is not None}
    ok = all(np.isfinite(v) and v > m2_min for v in ev.values())
    verdict = "not evaluable" if len(ev) < n_min else ("pass" if ok else "fail")
    return {"m2": target_m2, "n_evaluable": len(ev), "verdict": verdict}


def label_survivor(resolved: bool, primary, ref: dict, unvalidated_types, plx_snr_min, m2_min) -> str:
    """F-DR4 label of one DR3 survivor (first that applies; README DR4 addendum to section 2).

    primary: the vetted primary DR4 solution (dict-like) or None; ref: archived DR3 row with
    period, period_error, m1_used. primary must carry m2 (computed with the pre-registered M1).
    """
    if not resolved:
        return "unresolved"
    if primary is None:
        return "solution-gone"
    if primary["nss_solution_type"] in set(unvalidated_types):
        return "type-vetoed"

    def bad(x):
        return x is None or not np.isfinite(x)

    plx, plx_err = primary["parallax"], primary["parallax_error"]
    if (bad(plx) or bad(plx_err) or plx <= 0 or plx_err <= 0 or plx / plx_err <= plx_snr_min
            or bad(primary["period"]) or bad(primary["period_error"]) or bad(primary["a0_mas"])
            or bad(ref.get("period")) or bad(ref.get("period_error"))):
        return "insufficient"
    if bool(primary["veto_rv"]):
        return "rv-vetoed"
    if not primary["m2"] > m2_min:
        return "mass-below"
    sig = math.hypot(ref["period_error"], primary["period_error"])
    if not abs(primary["period"] - ref["period"]) < 3 * sig:
        return "period-changed"
    return "persists"


def possible_alias(period_ratio, rel_tol=0.1) -> bool:
    """P_DR4/P_DR3 within 10 per cent of 1/2 or 2 (reported only; not used for labels)."""
    r = float(period_ratio)
    return bool(np.isfinite(r) and (abs(r / 0.5 - 1) < rel_tol or abs(r / 2.0 - 1) < rel_tol))


def m1_for(primary, fallback: float) -> float:
    """DR4 FLAME mass if it is a finite number, else the fallback (README F-DR4 label 6)."""
    v = primary.get("mass_flame") if hasattr(primary, "get") else None
    return float(v) if v is not None and np.isfinite(v) else float(fallback)


# ---------------------------------------------------------------------------------------------
# Result-file size caps (AGENTS.md section 1; design plan 008 section 2.4)

def thin_screen_points(df: pd.DataFrame, cap=5000, keep_m2=3.0, keep_cap=2000, seed=0):
    """At most `cap` rows: all M2 > keep_m2 (top keep_cap by M2), the rest a seeded sample."""
    n = len(df)
    if n <= cap:
        return df, {"rows_total": n, "rows_kept": n, "sampled": False}
    hi = df[df.m2 > keep_m2].sort_values("m2", ascending=False).head(keep_cap)
    rest = df.drop(index=hi.index)
    k = min(cap - len(hi), len(rest))
    sample = rest.sample(n=k, random_state=seed) if k > 0 else rest.iloc[:0]
    out = pd.concat([hi, sample]).sort_index()
    return out, {"rows_total": n, "rows_kept": len(out), "sampled": True}


def cap_rows(df: pd.DataFrame, cap: int, by="m2"):
    n = len(df)
    if n <= cap:
        return df, {"rows_total": n, "rows_kept": n, "truncated": False}
    out = df.sort_values(by, ascending=False).head(cap)
    return out, {"rows_total": n, "rows_kept": cap, "truncated": True}
