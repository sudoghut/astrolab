"""Unit tests (no network) of the pre-registered rules in selection.py (README DR4 addendum)."""
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent))
import selection as sel  # noqa: E402

AST = ("Orbital", "AstroSpectroSB1", "OrbitalTargetedSearch", "OrbitalTargetedSearchValidated",
       "OrbitalAlternative", "OrbitalAlternativeValidated")
UNVAL = ["OrbitalAlternative", "OrbitalTargetedSearch"]
DR4_RV = {"max_period_d": 1000.0, "max_ecc": 0.8}


def sol(**kw):
    base = dict(source_id=1, nss_solution_type="Orbital", significance=30.0, goodness_of_fit=0.5, period=300.0,
                period_error=1.0, parallax=2.0, parallax_error=0.05, eccentricity=0.2,
                a_thiele_innes=1.0, b_thiele_innes=0.2, f_thiele_innes=-0.3, g_thiele_innes=0.9,
                rv_amplitude_robust=np.nan)
    base.update(kw)
    return base


# --- R-sel -----------------------------------------------------------------------------------

def test_rsel_prefers_validated_then_type_then_significance():
    df = pd.DataFrame([sol(nss_solution_type="OrbitalAlternative", significance=99),
                       sol(nss_solution_type="Orbital", significance=10),
                       sol(nss_solution_type="AstroSpectroSB1", significance=5)])
    assert sel.primary_solutions(df, UNVAL, AST).nss_solution_type.tolist() == ["AstroSpectroSB1"]


def test_rsel_only_unvalidated_is_kept_so_type_veto_is_reachable():
    df = pd.DataFrame([sol(nss_solution_type="OrbitalAlternative")])
    assert sel.primary_solutions(df, UNVAL, AST).nss_solution_type.tolist() == ["OrbitalAlternative"]


def test_rsel_ignores_non_astrometric_types():
    df = pd.DataFrame([sol(nss_solution_type="SB1")])
    assert sel.primary_solutions(df, UNVAL, AST).empty


def test_rsel_does_not_depend_on_row_order():
    rows = [sol(nss_solution_type="OrbitalTargetedSearchValidated", significance=20, goodness_of_fit=1, period=500),
            sol(nss_solution_type="OrbitalAlternativeValidated", significance=20, goodness_of_fit=1, period=400)]
    a = sel.primary_solutions(pd.DataFrame(rows), UNVAL, AST)
    b = sel.primary_solutions(pd.DataFrame(rows[::-1]), UNVAL, AST)
    assert a.nss_solution_type.tolist() == b.nss_solution_type.tolist() == ["OrbitalAlternativeValidated"]


def test_rsel_missing_significance_sorts_last():
    df = pd.DataFrame([sol(nss_solution_type="OrbitalTargetedSearchValidated", significance=np.nan),
                       sol(nss_solution_type="OrbitalAlternativeValidated", significance=5)])
    assert sel.primary_solutions(df, UNVAL, AST).nss_solution_type.tolist() == ["OrbitalAlternativeValidated"]


# --- vetoes ----------------------------------------------------------------------------------

def test_rv_veto_applicability_dr4_window():
    assert sel.rv_veto_applicable([500, 1500, 500], [0.2, 0.2, 0.85], DR4_RV).tolist() == [True, False, False]
    assert sel.rv_veto_applicable([5000], [0.9], None).tolist() == [True]   # DR3 rule unchanged


def test_rv_veto_not_applicable_without_amplitude_or_for_long_period():
    df = pd.DataFrame([sol(period=1500, rv_amplitude_robust=0.0), sol(source_id=2, rv_amplitude_robust=np.nan)])
    v = sel.apply_vetoes(df, UNVAL, 0.5, DR4_RV)
    assert not v.veto_rv.any() and not v.rv_veto_applicable.any()


def test_rv_veto_fires_inside_window():
    v = sel.apply_vetoes(pd.DataFrame([sol(rv_amplitude_robust=0.01)]), UNVAL, 0.5, DR4_RV)
    assert v.veto_rv.iloc[0] and v.vetoed.iloc[0]


# --- S2, V, S1 -------------------------------------------------------------------------------

def test_s2_threshold_scales_with_denominator():
    assert sel.s2_dr4(21, [True] * 17 + [False] * 1)["verdict"] == "pass"     # 17/18 >= ceil(16.2)
    assert sel.s2_dr4(21, [True] * 16 + [False] * 2)["verdict"] == "fail"
    assert sel.s2_dr4(21, [True] * 14)["verdict"] == "not evaluable"


def test_v_requires_enough_controls_and_judges_primary():
    ok = pd.DataFrame({"source_id": range(15), "vetoed": [False] * 15, "rv_veto_applicable": [True] * 3 + [False] * 12})
    r = sel.v_dr4(ok, 24)
    assert r["verdict"] == "pass" and r["rv_half_weak"]
    assert sel.v_dr4(ok.head(14), 24)["verdict"] == "not evaluable"
    bad = ok.assign(vetoed=[True] + [False] * 14)
    assert sel.v_dr4(bad, 24)["verdict"] == "fail"
    assert sel.v_dr4(pd.DataFrame(), 24)["verdict"] == "not evaluable"


def test_s1_targets_not_vacuous():
    assert sel.s1_targets({"a": None, "b": None, "c": 30.0}, 3.0)["verdict"] == "not evaluable"
    assert sel.s1_targets({"a": 9.0, "b": None, "c": 30.0}, 3.0)["verdict"] == "pass"
    assert sel.s1_targets({"a": 2.0, "b": 9.0, "c": None}, 3.0)["verdict"] == "fail"


# --- F-DR4 labels ----------------------------------------------------------------------------

REF = {"period": 300.0, "period_error": 2.0, "m1_used": 1.0}


def prim(**kw):
    p = sol(**kw)
    p.update(a0_mas=1.0, veto_rv=False, m2=5.0)
    p.update({k: v for k, v in kw.items() if k in ("a0_mas", "veto_rv", "m2")})
    return p


@pytest.mark.parametrize("resolved, primary, label", [
    (False, None, "unresolved"),
    (True, None, "solution-gone"),
    (True, prim(nss_solution_type="OrbitalAlternative"), "type-vetoed"),
    (True, prim(parallax=0.2, parallax_error=0.05), "insufficient"),
    (True, prim(period_error=np.nan), "insufficient"),
    (True, prim(veto_rv=True), "rv-vetoed"),
    (True, prim(m2=2.9), "mass-below"),
    (True, prim(period=330.0), "period-changed"),
    (True, prim(period=303.0), "persists"),
])
def test_label_order(resolved, primary, label):
    assert sel.label_survivor(resolved, primary, REF, UNVAL, 5.0, 3.0) == label


def test_labels_cover_every_outcome():
    assert len(set(sel.LABELS)) == 8


def test_m1_for_null_flame_uses_fallback():
    assert sel.m1_for({"mass_flame": np.nan}, 0.9) == 0.9
    assert sel.m1_for({"mass_flame": None}, 0.9) == 0.9
    assert sel.m1_for({"mass_flame": 1.2}, 0.9) == 1.2


# --- resolution ------------------------------------------------------------------------------

def test_identity_check_offset_magnitude_and_proper_motion():
    ref = {"ra": 10.0, "dec": 0.0, "phot_g_mean_mag": 12.0}
    same = {"ra": 10.0, "dec": 0.0, "pmra": 0.0, "pmdec": 0.0, "phot_g_mean_mag": 12.1}
    assert sel.identity_check(ref, same, 1.5) == (True, "")
    far = dict(same, ra=10.0 + 3 / 3600)
    assert sel.identity_check(ref, far, 1.5) == (False, "offset")
    moved = dict(same, ra=10.0 + 1.5 / 3600, pmra=1000.0)   # 1.5 arcsec explained by 1 arcsec/yr x 1.5 yr
    assert sel.identity_check(ref, moved, 1.5)[0]
    nopm = dict(same, pmra=np.nan, pmdec=None)
    assert sel.identity_check(ref, nopm, 1.5)[0]
    assert sel.identity_check(ref, dict(same, phot_g_mean_mag=12.5), 1.5) == (False, "magnitude")


def test_resolve_ids_reports_reasons():
    ref = pd.DataFrame({"source_id": [1, 2, 3], "ra": [10.0] * 3, "dec": [0.0] * 3, "phot_g_mean_mag": [12.0] * 3})
    found = pd.DataFrame({"source_id": [1, 2], "ra": [10.0, 10.1], "dec": [0.0, 0.0], "pmra": [0.0, 0.0],
                          "pmdec": [0.0, 0.0], "phot_g_mean_mag": [12.0, 12.0]})
    r = sel.resolve_ids(ref, found, 1.5).set_index("dr3_id")
    assert r.loc[1, "dr4_id"] == 1 and pd.isna(r.loc[2, "dr4_id"]) and pd.isna(r.loc[3, "dr4_id"])
    assert r.loc[2, "reason"] == "offset" and r.loc[3, "reason"] == "not-found"


# --- masses and caps -------------------------------------------------------------------------

def test_central_mass_matches_orbits():
    from astrolab import orbits
    row = sol()
    c = sel.central_mass(row, 1.0)
    a0 = float(orbits.a0_mas(1.0, 0.2, -0.3, 0.9))
    assert math.isclose(c["a0_mas"], a0)
    assert math.isclose(c["m2"], float(orbits.companion_mass(orbits.mass_function(a0, 2.0, 300.0), 1.0)))


def test_in_screen_cuts():
    assert sel.in_screen_cuts(sol(a_thiele_innes=5, g_thiele_innes=5), AST, 5.0, 0.25)
    assert not sel.in_screen_cuts(sol(a_thiele_innes=5, g_thiele_innes=5, parallax_error=1.0), AST, 5.0, 0.25)
    assert not sel.in_screen_cuts(sol(nss_solution_type="SB1"), AST, 5.0, 0.25)


def test_thin_screen_points_has_hard_cap():
    n = 20000
    df = pd.DataFrame({"m2": np.r_[np.full(3000, 4.0), np.full(n - 3000, 1.5)], "x": np.arange(n)})
    out, info = sel.thin_screen_points(df)
    assert len(out) == 5000 and info["sampled"]
    assert (out.m2 > 3).sum() >= 2000   # the top 2,000 by M2 always kept; the rest sampled with the others
    small, info = sel.thin_screen_points(df.head(100))
    assert len(small) == 100 and not info["sampled"]


def test_cap_rows():
    df = pd.DataFrame({"m2": np.arange(3000.0)})
    out, info = sel.cap_rows(df, 2500)
    assert len(out) == 2500 and info["truncated"] and out.m2.min() == 500


# --- tests that pin the order of each rule (gate-1 round 1, stage 2) ---------------------------

def test_rsel_highest_significance_wins():
    df = pd.DataFrame([sol(nss_solution_type="OrbitalTargetedSearchValidated", significance=10),
                       sol(nss_solution_type="OrbitalAlternativeValidated", significance=50)])
    assert sel.primary_solutions(df, UNVAL, AST).nss_solution_type.tolist() == ["OrbitalAlternativeValidated"]
    df = pd.DataFrame([sol(nss_solution_type="OrbitalAlternativeValidated", significance=10),
                       sol(nss_solution_type="OrbitalTargetedSearchValidated", significance=50)])
    assert sel.primary_solutions(df, UNVAL, AST).nss_solution_type.tolist() == ["OrbitalTargetedSearchValidated"]


def test_rsel_nan_significance_loses_even_against_type_name_order():
    # the type-name tie-break alone would pick OrbitalAlternativeValidated; NaN significance must lose first
    df = pd.DataFrame([sol(nss_solution_type="OrbitalAlternativeValidated", significance=np.nan),
                       sol(nss_solution_type="OrbitalTargetedSearchValidated", significance=5)])
    assert sel.primary_solutions(df, UNVAL, AST).nss_solution_type.tolist() == ["OrbitalTargetedSearchValidated"]


def test_rsel_goodness_of_fit_then_type_name_then_period():
    df = pd.DataFrame([sol(nss_solution_type="OrbitalAlternativeValidated", goodness_of_fit=-3),
                       sol(nss_solution_type="OrbitalTargetedSearchValidated", goodness_of_fit=1)])
    assert sel.primary_solutions(df, UNVAL, AST).nss_solution_type.tolist() == ["OrbitalTargetedSearchValidated"]


def test_rsel_orbital_beats_other_validated_types():
    df = pd.DataFrame([sol(nss_solution_type="OrbitalAlternativeValidated", significance=99),
                       sol(nss_solution_type="Orbital", significance=1)])
    assert sel.primary_solutions(df, UNVAL, AST).nss_solution_type.tolist() == ["Orbital"]


@pytest.mark.parametrize("primary, label", [
    (prim(nss_solution_type="OrbitalAlternative", parallax=-1.0), "type-vetoed"),      # type before insufficient
    (prim(period_error=np.nan, veto_rv=True), "insufficient"),                          # insufficient before RV
    (prim(veto_rv=True, m2=1.0), "rv-vetoed"),                                          # RV before mass
    (prim(m2=1.0, period=400.0), "mass-below"),                                         # mass before period
])
def test_first_label_that_applies(primary, label):
    assert sel.label_survivor(True, primary, REF, UNVAL, 5.0, 3.0) == label


def test_period_test_uses_both_errors():
    # |dP| = 9: fails with sigma_DR3 = 2 alone (3 x 2 = 6), passes with sigma_DR4 = 3 (3 x 3.6 = 10.8)
    assert sel.label_survivor(True, prim(period=309.0, period_error=3.0), REF, UNVAL, 5.0, 3.0) == "persists"
    assert sel.label_survivor(True, prim(period=309.0, period_error=0.1), REF, UNVAL, 5.0, 3.0) == "period-changed"


def test_insufficient_on_zero_parallax_error():
    assert sel.label_survivor(True, prim(parallax_error=0.0), REF, UNVAL, 5.0, 3.0) == "insufficient"


def test_in_screen_cuts_fail_on_mass_function_only():
    small = sol(a_thiele_innes=0.01, b_thiele_innes=0.0, f_thiele_innes=0.0, g_thiele_innes=0.01)
    assert not sel.in_screen_cuts(small, AST, 5.0, 0.25)


def test_boundaries():
    assert sel.s2_dr4(21, [True] * 14 + [False])["verdict"] == "pass"          # N_eval = 15, 14 >= ceil(13.5)
    assert sel.s2_dr4(21, [True] * 13 + [False] * 2)["verdict"] == "fail"
    assert sel.rv_veto_applicable([999.9, 1000.0], [0.0, 0.0], DR4_RV).tolist() == [True, False]
    assert sel.rv_veto_applicable([500, 500], [0.79, 0.8], DR4_RV).tolist() == [True, False]


def test_s1_nan_mass_counts_as_evaluable_failure():
    assert sel.s1_targets({"a": 9.0, "b": float("nan"), "c": None}, 3.0)["verdict"] == "fail"


def test_identity_check_uses_cos_dec_and_wraps_ra():
    ref = {"ra": 10.0, "dec": 80.0, "phot_g_mean_mag": 12.0}
    # 10 arcsec in RA at dec 80 is 1.74 arcsec on the sky: within 2 arcsec
    assert sel.identity_check(ref, {"ra": 10.0 + 10 / 3600, "dec": 80.0, "phot_g_mean_mag": 12.0}, 0.0)[0]
    ref0 = {"ra": 359.99999, "dec": 0.0, "phot_g_mean_mag": 12.0}
    assert sel.identity_check(ref0, {"ra": 0.00001, "dec": 0.0, "phot_g_mean_mag": 12.0}, 0.0)[0]


def test_possible_alias_is_relative():
    assert sel.possible_alias(0.52) and sel.possible_alias(2.15) and not sel.possible_alias(1.0)
    assert not sel.possible_alias(0.6) and not sel.possible_alias(float("nan"))


def test_resolve_ids_keeps_19_digit_ids_exact_with_unresolved_present():
    big = [6481502062263141504, 5820382041374661888, 2995961897685517313]
    ref = pd.DataFrame({"source_id": big, "ra": [10.0] * 3, "dec": [0.0] * 3, "phot_g_mean_mag": [12.0] * 3})
    found = pd.DataFrame({"source_id": big[:2], "ra": [10.0] * 2, "dec": [0.0] * 2, "pmra": [0.0] * 2,
                          "pmdec": [0.0] * 2, "phot_g_mean_mag": [12.0] * 2})
    r = sel.resolve_ids(ref, found, 1.5)
    assert [int(x) for x in r.dr4_id.dropna()] == big[:2] and r.dr4_id.isna().sum() == 1


def test_rsel_full_tie_broken_by_thiele_innes_not_row_order():
    a = sol(a_thiele_innes=2.0)
    b = sol(a_thiele_innes=1.0)
    for rows in ([a, b], [b, a]):
        assert sel.primary_solutions(pd.DataFrame(rows), UNVAL, AST).a_thiele_innes.tolist() == [1.0]


def test_resolve_ids_duplicate_rows_are_ambiguous():
    ref = pd.DataFrame({"source_id": [7], "ra": [10.0], "dec": [0.0], "phot_g_mean_mag": [12.0]})
    found = pd.DataFrame({"source_id": [7, 7], "ra": [10.0, 10.0], "dec": [0.0, 0.0], "pmra": [0.0, 0.0],
                          "pmdec": [0.0, 0.0], "phot_g_mean_mag": [12.0, 15.0]})
    r = sel.resolve_ids(ref, found, 1.5)
    assert r.dr4_id.isna().all() and r.reason.tolist() == ["ambiguous"]


def test_missing_dr3_period_error_is_insufficient():
    assert sel.label_survivor(True, prim(), dict(REF, period_error=None), UNVAL, 5.0, 3.0) == "insufficient"
    assert sel.label_survivor(True, prim(), dict(REF, period_error=float("nan")), UNVAL, 5.0, 3.0) == "insufficient"


def test_rsel_requires_thiele_innes_columns():
    df = pd.DataFrame([sol()]).drop(columns=["g_thiele_innes"])
    with pytest.raises(ValueError, match="g_thiele_innes"):
        sel.primary_solutions(df, UNVAL, AST)


def test_neighbourhood_fallback_nearest_tie_and_identity():
    ref = pd.DataFrame({"source_id": [1, 2, 3, 4], "ra": [10.0] * 4, "dec": [0.0] * 4, "phot_g_mean_mag": [12.0] * 4})
    res = pd.DataFrame({"dr3_id": pd.array([1, 2, 3, 4], dtype="int64"),
                        "dr4_id": pd.array([1, None, None, None], dtype="Int64"),
                        "reason": ["", "not-found", "not-found", "offset"]})
    nb = pd.DataFrame({"old_id": [2, 2, 3, 3, 4], "new_id": [20, 21, 30, 31, 40],
                       "dist_arcsec": [0.05, 0.9, 0.30, 0.35, 0.1]})
    found = pd.DataFrame({"source_id": [20, 21, 30, 31, 40], "ra": [10.0, 10.0, 10.0, 10.0, 10.1],
                          "dec": [0.0] * 5, "pmra": [0.0] * 5, "pmdec": [0.0] * 5, "phot_g_mean_mag": [12.0] * 5})
    out = sel.apply_neighbourhood(res, ref, nb, found, 1.5).set_index("dr3_id")
    assert out.loc[1, "dr4_id"] == 1                                                # direct match untouched
    assert out.loc[2, "dr4_id"] == 20 and out.loc[2, "reason"] == "neighbourhood"   # nearest neighbour
    assert pd.isna(out.loc[3, "dr4_id"]) and out.loc[3, "reason"] == "neighbourhood-ambiguous"
    assert pd.isna(out.loc[4, "dr4_id"]) and out.loc[4, "reason"] == "neighbourhood-offset"
