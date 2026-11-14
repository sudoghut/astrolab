"""Offline test of run.dr4_criteria (the DR4 glue) on synthetic DR4-shaped data (design plan 008)."""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
_spec = importlib.util.spec_from_file_location("m04_run_for_tests", HERE / "run.py")
run = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(run)
import selection as sel  # noqa: E402

BH1, BH2, BH3 = (run.TARGETS[n]["gaia_dr3"] for n in ("Gaia BH1", "Gaia BH2", "Gaia BH3"))
NEW = 1234567890123456789


def solution(sid, **kw):
    s = dict(source_id=sid, nss_solution_type="Orbital", significance=40.0, goodness_of_fit=0.2, period=300.0,
             period_error=1.0, parallax=2.0, parallax_error=0.05, eccentricity=0.2, a_thiele_innes=5.0,
             b_thiele_innes=0.5, f_thiele_innes=-0.5, g_thiele_innes=5.0, rv_amplitude_robust=np.nan,
             mass_flame=1.0, radius_flame=1.0, phot_g_mean_mag=12.0, bp_rp=0.8)
    s.update(kw)
    return s


def build(tmp_path):
    ns, _ = run.ns_table()
    ns_ids = [int(i) for i in ns.gaia_dr3]
    surv = [9000000000000000001, 9000000000000000003, 9000000000000000005, 9000000000000000007]  # 19 digits
    ref = pd.DataFrame({
        "source_id": [str(i) for i in surv] + [str(BH1)],
        "known": [False] * 4 + [True], "vetoed": [False] * 5, "literature": [""] * 5,
        "period": [300.0, 300.0, 300.0, 300.0, 185.6], "period_error": [2.0] * 5,
        "m1_used": [1.0] * 5, "a0_mas": [1.0] * 5})
    d = tmp_path / "dr3"
    d.mkdir()
    (d / "bh_candidates.json").write_text(ref.to_json(orient="columns"), encoding="utf-8")

    ids = [BH1, BH2, BH3] + ns_ids + surv
    dr4 = {i: i for i in ids}
    dr4[surv[3]] = None                    # the fourth survivor does not resolve
    res = pd.DataFrame({"dr3_id": pd.array(ids, dtype="int64"), "dr4_id": pd.array([dr4[i] for i in ids], dtype="Int64"),
                        "reason": ["" if dr4[i] else "offset" for i in ids]})

    rows = [solution(BH1), solution(BH2, nss_solution_type="AstroSpectroSB1")]       # BH3: no solution
    rows += [solution(i) for i in ns_ids[:18]]                                         # 3 NS without solution
    rows += [solution(surv[0]),                                                        # persists
             solution(surv[1], nss_solution_type="OrbitalAlternative"),                # type-vetoed
             solution(surv[2], period=400.0)]                                          # period-changed
    rows += [solution(NEW, a_thiele_innes=20.0, g_thiele_innes=20.0)]                  # new S3 candidate
    sol = sel.apply_vetoes(pd.DataFrame(rows), run.PARAMS["unvalidated_types"], 0.5, run.RELEASES["dr4"]["rv_veto"])
    _, a0, fm = sel.solution_m2(sol, 1.0)
    sol["a0_mas"], sol["f_m"] = a0, fm
    screen = pd.DataFrame({"source_id": pd.array([surv[0], NEW], dtype="int64"), "m2": [5.0, 40.0]})
    recs = [{"name": n, "status": "computed", "evaluable": False} for n in run.TARGETS]
    return d, res, sol, recs, screen


def test_dr4_criteria_on_synthetic_release(tmp_path):
    d, res, sol, recs, screen = build(tmp_path)
    params = dict(run.PARAMS, release="dr4")
    out, f_rows, new_rows = run.dr4_criteria(params, run.RELEASES["dr4"], res, sol, recs, screen, 2, d, sol, len(sol))

    labels = {r["source_id"]: r["label"] for r in f_rows}
    assert labels == {"9000000000000000001": "persists", "9000000000000000003": "type-vetoed",
                      "9000000000000000005": "period-changed", "9000000000000000007": "unresolved"}
    assert out["F"]["n"] == 4 and sum(out["F"]["counts"].values()) == 4

    assert out["S1"]["n_evaluable"] == 2 and out["S1"]["verdict"] == "pass"          # BH3 missing: not counted
    assert out["S2"]["n_eval"] == 18 and out["S2"]["catalogue_recall"] == "18/21"
    assert out["S2"]["verdict"] == "pass"
    assert out["V"]["n_counted"] == 20 and out["V"]["verdict"] == "pass"
    assert str(BH3) in out["V"]["without_solution_or_unresolved"]
    assert all(r["verdict"] == "not evaluable" for r in out["R"].values())
    assert out["S3"]["n_new"] == 1 and out["S3"]["_ids"] == [str(NEW)] and len(new_rows) == 1
    assert int(new_rows.source_id.iloc[0]) == NEW
    assert out["resolution"]["unresolved"] == 1


def test_dr4_criteria_s3_stop_rule_and_no_screen(tmp_path):
    d, res, sol, recs, screen = build(tmp_path)
    params = dict(run.PARAMS, release="dr4")
    out, _, new_rows = run.dr4_criteria(params, run.RELEASES["dr4"], res, sol, recs, screen, 2, d, None, 60000)
    assert out["S3"]["verdict"] == "not evaluable" and len(new_rows) == 0
    out, _, _ = run.dr4_criteria(params, run.RELEASES["dr4"], res, sol, recs, None, 60000, d, None, 0)
    assert out["S1"]["verdict"] == "fail" and out["S3"]["verdict"] == "not evaluable"
    assert out["S2"]["verdict"] == "pass"                                                 # independent of the screen


def test_outputs_list_covers_every_saved_name():
    import re
    src = (HERE / "run.py").read_text(encoding="utf-8")
    assigned = set(re.findall(r'(?<![A-Za-z_])out\["([a-z0-9_]+)"\]', src))
    assert assigned <= set(run.OUTPUTS)


class FakeCtx:
    """tap() answers from canned frames keyed by a substring of the query; records every query."""
    def __init__(self, answers):
        self.answers, self.queries = answers, []

    def tap(self, adql, *a, **k):
        self.queries.append(adql)
        for key, df in self.answers.items():
            if key in adql:
                return df.copy()
        raise AssertionError(f"unexpected query: {adql[:120]}")


def test_fetch_solutions_empty_is_typed_and_concat_keeps_ids_exact():
    empty = run.fetch_solutions(FakeCtx({}), "gaiadr4", "Gaia DR4", [], "x", optional=set())
    assert empty.source_id.dtype == "int64" and len(empty) == 0
    more = pd.DataFrame([solution(NEW)])
    both = pd.concat([empty, more], ignore_index=True)
    assert int(both.source_id.iloc[0]) == NEW


def test_fetch_solutions_keeps_same_type_solutions_and_blanks_doubled_flame():
    rows = pd.DataFrame([solution(NEW, period=300.0), solution(NEW, period=600.0, significance=10.0),
                         solution(BH1, mass_flame=1.0), solution(BH1, mass_flame=2.0)])   # BH1: doubled join row
    df = run.fetch_solutions(FakeCtx({"nss_two_body_orbit": rows}), "gaiadr4", "Gaia DR4", [NEW, BH1], "x")
    assert (df.source_id == NEW).sum() == 2                      # both Orbital solutions kept for R-sel
    b = df[df.source_id == BH1]
    assert len(b) == 1 and np.isnan(b.mass_flame.iloc[0]) and df.attrs["ambiguous_flame_sources"] == 1
    prim = sel.primary_solutions(df, run.PARAMS["unvalidated_types"], run.ASTROMETRIC_TYPES)
    assert prim[prim.source_id == NEW].period.iloc[0] == 300.0   # R-sel, not row order


def test_available_columns_stops_when_metadata_lookup_fails():
    import pytest
    meta = pd.DataFrame({"table_name": ["gaiadr4.gaia_source"], "column_name": ["source_id"]})
    with pytest.raises(SystemExit, match="metadata lookup failed"):
        run.available_columns(FakeCtx({"tap_schema": meta}), "gaiadr4", "Gaia DR4")
    meta = pd.DataFrame({"table_name": ["gaiadr4.gaia_source"] * 2 + ["gaiadr4.astrophysical_parameters"] * 2,
                         "column_name": ["source_id", "rv_amplitude_robust", "source_id", "mass_flame"]})
    assert run.available_columns(FakeCtx({"tap_schema": meta}), "gaiadr4", "Gaia DR4") == {"rv_amplitude_robust",
                                                                                           "mass_flame"}


def test_screen_selects_only_available_flame_columns():
    from screen import screen_adql
    q = screen_adql("dr4", flame=["mass_flame"])
    assert "ap.mass_flame " in q and "mass_flame_lower" not in q and "astrophysical_parameters" in q
    assert "astrophysical_parameters" not in screen_adql("dr4", flame=[])


def test_run_screen_collapses_doubled_flame_join():
    class Ctx(FakeCtx):
        def count(self, q):
            return 2
        def log(self, m):
            pass
    base = dict(source_id=NEW, nss_solution_type="Orbital", period=300.0, period_error=1.0, eccentricity=0.2,
                parallax=2.0, parallax_error=0.05, significance=40.0, goodness_of_fit=0.1, flags=0, a0_mas=5.0,
                f_m=1.0, ra=1.0, dec=1.0, l=1.0, b=1.0, phot_g_mean_mag=12.0, bp_rp=0.8, ruwe=1.0,
                mass_flame=1.0, mass_flame_lower=0.9, mass_flame_upper=1.1, radius_flame=1.0)
    rows = pd.DataFrame([base, dict(base, mass_flame=2.0), dict(base, source_id=BH1, period=185.0)])
    df, n = run.run_screen(Ctx({"WHERE q.f_m": rows}), run.PARAMS, "gaiadr4", "Gaia DR4", "dr4")
    assert n == 2 and len(df) == 2 and df.attrs["ambiguous_flame_sources"] == 1
    assert np.isnan(df[df.source_id == NEW].mass_flame.iloc[0]) and df[df.source_id == NEW].m1_used.iloc[0] == 1.0


def test_screen_adql_partial_flame_list_is_well_formed():
    from screen import screen_adql
    q = screen_adql("dr4", flame=["mass_flame", "radius_flame"])
    assert "g.ruwe, ap.mass_flame, ap.radius_flame FROM" in q and "mass_flame_upper" not in q
