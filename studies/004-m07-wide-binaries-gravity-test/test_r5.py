"""Offline tests for R5 (README 2.1 and the section 3 R5 block; T-034). No archive access: the
pipeline is driven by a fake context that serves synthetic tables."""
import importlib.util
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import queries as Q  # noqa: E402
import r5  # noqa: E402
import wb  # noqa: E402


def _run_module():
    spec = importlib.util.spec_from_file_location("run004_r5_test", HERE / "run.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _test_wb():
    spec = importlib.util.spec_from_file_location("test_wb004_r5", HERE / "test_wb.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


REGION = wb.strip_plan()[100]
_ORIG_POWER_MOCK = r5.power_mock


# ---------------------------------------------------------------- queries
def _select_list(q):
    return q.split(" FROM ", 1)[0]


def test_n1_query_is_velocity_free_and_has_the_readme_conditions():
    q = r5.n1_query(REGION, False, "parallax + 3 * parallax_error > 80", "rows")
    sel = _select_list(q)
    cols = set(re.findall(r"[ab]\.(\w+) AS", sel))
    assert cols == set(Q.A_COLS) | {"pmra_error", "pmdec_error"}
    assert not ({"pmra", "pmdec", "radial_velocity"} & cols)
    assert q.count("parallax > 3.4783 AND parallax_over_error > 40 AND radial_velocity IS NOT NULL") == 2
    assert "a.source_id < b.source_id" in q
    assert "ABS(a.parallax - b.parallax) < 3 * SQRT(" in q          # strict, as queries.pair_conditions
    assert "* 206.264806 <= 30.0" in q                               # r_sky <= 30 kAU, as b1_extra
    c = r5.n1_query(REGION, False, "x", "count")
    assert c.startswith("SELECT COUNT(*) AS n FROM") and c.split(" FROM ", 1)[1] == q.split(" FROM ", 1)[1]


def test_n4_query_has_server_side_velocity_free_cuts_and_no_hr_cut():
    q = r5.n4_query(REGION, False, "x", "rows")
    assert "> 4.0" in q and ">= 0.3" in q and "a.ruwe < 1.25" in q and "b.ruwe < 1.25" in q
    assert "bp_rp" not in q and "phot_g_mean_mag" not in q             # V6 stays possible
    assert "a.radial_velocity AS radial_velocity_a" in _select_list(q)
    # N4's WHERE contains N1's WHERE
    w1 = r5.n1_query(REGION, False, "x", "rows").split(" WHERE ")[-1]
    assert w1 in q


def test_neighbour_and_flame_queries_restricted_and_fallback():
    nr = r5.neighbour_query(REGION, False, "x", r5.NEIGHBOUR, "rows", True)
    nf = r5.neighbour_query(REGION, False, "x", r5.NEIGHBOUR, "rows", False)
    assert "source_id IN (SELECT a.source_id FROM" in nr and " IN (" not in nf
    assert f"<= {Q.DEGROUP_PC}" in nr and "ABS(a.parallax - b.parallax) < 3 * SQRT(" in nr
    assert r5.NEIGHBOUR in nr and "GROUP BY a.source_id" in nr
    c25 = r5.neighbour_query(REGION, False, "x", r5.NEIGHBOUR_C25, "count", True)
    assert c25.startswith("SELECT COUNT(*) AS n FROM (") and "parallax_over_error > 40 AND phot_g_mean_flux" in c25
    fr = r5.flame_query(REGION, False, "x", "rows", True)
    assert "mass_flame IS NOT NULL" in fr and " IN (" in fr
    assert " IN (" not in r5.flame_query(REGION, False, "x", "rows", False)
    NEAR = dict(ra0=0.0, ra1=360.0, dec0=-90.0, dec1=90.0, bra0=0.0, bra1=360.0, bdec0=-90.0, bdec1=90.0)
    near = r5.n1_query(NEAR, True, "parallax + 3 * parallax_error > 80", "rows")
    assert "parallax >= 100.0" in near and "parallax + 3 * parallax_error > 80" in near


# ---------------------------------------------------------------- statistics
def test_stratified_bootstrap_chunks_consume_the_generator_as_one_call():
    rng = np.random.default_rng(3)
    vt = rng.normal(0.5, 0.2, 300)
    b = np.repeat([0, 1, 2], 100)
    s1 = r5.stratified_sigma(vt, b, 3, n_boot=1200, seed=0, chunk=1200)
    s2 = r5.stratified_sigma(vt, b, 3, n_boot=1200, seed=0, chunk=250)
    assert np.array_equal(s1, s2)
    # reference: one rng.integers call per bin, in bin order
    g = np.random.default_rng(0)
    ref = [np.std(np.median(vt[b == k][g.integers(0, 100, size=(1200, 100))], axis=1), ddof=1) for k in range(3)]
    assert np.allclose(s1, ref, rtol=0, atol=0)


def test_labels_and_grades_follow_the_readme_table():
    L5 = r5.LABELS
    assert r5.verdict_label(False, True, 1e6) == L5["invalid"]
    assert r5.verdict_label(True, True, 100.0) == L5["newton"]
    assert r5.verdict_label(True, True, 0.01) == L5["mond"]
    assert r5.verdict_label(True, True, 5.0) == L5["cannot"]
    assert r5.verdict_label(True, False, 10.0) == L5["g2fail_newton"]
    assert r5.verdict_label(True, False, 0.1) == L5["g2fail_mond"]
    assert r5.verdict_label(True, False, 1.0) == L5["g2fail_none"]
    assert r5.grade(10.0).startswith("Newton") and r5.grade(0.1).startswith("MOND") and r5.grade(1.0).startswith("no ")
    u = r5.verdict_label(True, True, 1000.0, unblinded=True)
    assert u.startswith("R5 (unblinded, descriptive): Newton has")
    assert L5["g1b_fail"] == "R5: not run (insufficient predicted power)"
    assert L5["no_data"] == "R5: not run (data not obtained)"


def test_read_before_merge():
    assert r5.read_before_merge(["2026-11-18T12:04:19+00:00"])
    assert not r5.read_before_merge(["2026-11-18T12:04:20+00:00", "2026-11-20T00:00:00+00:00"])
    assert not r5.read_before_merge([])


def test_g1b_counts_rounding_and_merge():
    pm = r5.power_mock()
    final, mapping, ok = pm.g1b_counts([1453, 1054, 828, 417, 272, 138])
    assert final == [1408, 988, 789, 375, 220, 72] and ok
    final, mapping, ok = pm.g1b_counts([10, 100, 100, 100, 100, 20])   # 10*0.969 -> 10; 20*0.521 -> 10
    assert mapping[0] == mapping[1] and mapping[4] == mapping[5] and ok


# ---------------------------------------------------------------- pipeline on synthetic tables
def _tables(n=900, seed=11):
    pairs, a2, a3 = _test_wb()._synthetic(n, seed)
    n1 = pairs[[f"{c}_{s}" for s in ("a", "b") for c in r5.N1_COLS]].copy()
    n4 = pairs[["source_id_a", "source_id_b"] + [f"{c}_{s}" for s in ("a", "b") for c in Q.B1_COLS if c != "source_id"]].copy()
    return pairs, n1, n4, a2, a3


class FakeCtx:
    """Serves synthetic tables by query label; counts return the table length."""

    def __init__(self, tables, fail_restricted=False, retrieved_at="2026-11-19T00:00:00+00:00"):
        from astrolab.provenance import ProvenanceLog
        self.tables, self.fail_restricted, self.retrieved_at = tables, fail_restricted, retrieved_at
        self.provenance = ProvenanceLog()
        self.saved = {}

    def _table(self, label):
        kind = label.replace("count ", "").split(" ")[0].replace("-fallback", "")
        return self.tables[kind]

    def tap(self, q, service, label="", **kw):
        if self.fail_restricted and " IN (" in q:
            raise TimeoutError("restricted join refused (fake)")
        t = self._table(label)
        if label.startswith("count "):
            return pd.DataFrame({"n": [len(t)]})
        self.provenance.add({"label": label, "rows": len(t), "retrieved_at": self.retrieved_at})
        return t.copy()

    def save(self, name, obj):
        self.saved[name] = obj

    def log(self, msg):
        pass


def _stub_pm(passes=True):
    pm = _ORIG_POWER_MOCK()
    pm.g1b = lambda final, xmed: (1e4 if passes else 1.0, 1e-4 if passes else 0.5, passes)
    return pm


def _setup(monkeypatch, passes=True):
    run = _run_module()
    monkeypatch.setattr(r5, "power_mock", lambda: _stub_pm(passes))
    P = dict(run.PARAMS)
    P.pop("mode")
    R = {k: P.pop(k) for k in list(P) if k.startswith("r5_")}
    P.update(hr_c=1.0, region_limit=1, workers=1)
    R.update(r5_n_boot=300)
    return run, P, R


def test_r5_pipeline_end_to_end_with_fallback(monkeypatch):
    run, P, R = _setup(monkeypatch)
    pairs, n1, n4, a2, a3 = _tables()
    ctx = FakeCtx({"N1": n1, "N2": a2, "N3": a3, "N2-C25": a2, "N4": n4}, fail_restricted=True)
    out = run.step_r5(ctx, P, R)
    assert ctx.record_suffix == "_r5"
    s = ctx.saved["r5"]
    assert s["queries_a"]["fallback_regions"] == {"N2": ["r000"], "N3": ["r000"]}
    assert s["queries_a"]["n2_c25_rows"] is None                      # V9 only in restricted form
    assert s["variants"]["V9_c25_degroup"]["not_run"]
    assert s["g1b"]["passes"] and s["g1b"]["raw"] and "sigma_proxy" in s["g1b"]["step1_trace"]
    assert s["blinding"]["n4_read_before_merge"] is False
    m = s["main"]
    assert m["N"] > 100 and m["valid"]
    fit = m["fit"]
    expect = r5.verdict_label(True, fit["g2"]["passes"], fit["L"])
    assert out["label"] == s["label"] == expect
    assert set(m["error_models"]) == {"E1_whole_sample_bootstrap", "E2_pooled_scale", "E3_mad",
                                      "E4_mad_1.4826", "E5_tied_A"}
    assert set(m["shells"]) == {"d_lt_150", "d_150_250"}
    assert set(s["variants"]) == set(r5.VARIANTS) - {"R5"}


def test_r5_unblinded_and_c25(monkeypatch):
    run, P, R = _setup(monkeypatch)
    pairs, n1, n4, a2, a3 = _tables()
    ctx = FakeCtx({"N1": n1, "N2": a2, "N3": a3, "N2-C25": a2, "N4": n4}, retrieved_at="2026-11-18T10:00:00+00:00")
    run.step_r5(ctx, P, R)
    s = ctx.saved["r5"]
    assert s["blinding"]["n4_read_before_merge"] is True
    assert s["label"].startswith("R5 (unblinded, descriptive):")
    assert s["variants"]["V9_c25_degroup"]["N"] == s["main"]["N"]   # same neighbour table here


def test_r5_g1b_fail_stops_before_n4(monkeypatch):
    run, P, R = _setup(monkeypatch, passes=False)
    pairs, n1, n4, a2, a3 = _tables()
    ctx = FakeCtx({"N1": n1, "N2": a2, "N3": a3, "N2-C25": a2, "N4": n4})
    run.step_r5(ctx, P, R)
    s = ctx.saved["r5"]
    assert s["label"] == "R5: not run (insufficient predicted power)"
    assert not any(str(rec["label"]).startswith("N4") for rec in ctx.provenance.records)


def test_r5_stop_after_g1b_and_data_not_obtained(monkeypatch):
    run, P, R = _setup(monkeypatch)
    pairs, n1, n4, a2, a3 = _tables()
    R["r5_stop_after_g1b"] = True
    ctx = FakeCtx({"N1": n1, "N2": a2, "N3": a3, "N2-C25": a2, "N4": n4})
    run.step_r5(ctx, P, R)
    assert ctx.saved["r5"]["stopped_after_g1b"]
    assert not any(str(rec["label"]).startswith("N4") for rec in ctx.provenance.records)

    class Broken(FakeCtx):
        def tap(self, q, service, label="", **kw):
            if label.startswith("count N1"):
                raise TimeoutError("archive down (fake)")
            return super().tap(q, service, label, **kw)
    R["r5_stop_after_g1b"] = False
    from datetime import datetime, timezone
    # before the 2026-11-24 deadline: the attempt is recorded, no final label, retry status
    monkeypatch.setattr(r5, "now_utc", lambda: datetime(2026, 11, 20, 9, 0, tzinfo=timezone.utc))
    ctx = Broken({"N1": n1, "N2": a2, "N3": a3, "N2-C25": a2, "N4": n4})
    with pytest.raises(run.R5Retry):
        run.step_r5(ctx, P, R)
    assert ctx.saved["r5"]["status"] == "retry" and "label" not in ctx.saved["r5"]
    assert ctx.saved["r5"]["attempted_utc"].startswith("2026-11-20T09:00")
    # from the deadline on: final label
    monkeypatch.setattr(r5, "now_utc", lambda: datetime(2026, 11, 24, 1, 0, tzinfo=timezone.utc))
    ctx = Broken({"N1": n1, "N2": a2, "N3": a3, "N2-C25": a2, "N4": n4})
    run.step_r5(ctx, P, R)
    assert ctx.saved["r5"]["label"] == "R5: not run (data not obtained)"


def test_r5_refuses_n4_before_merge(monkeypatch):
    run, P, R = _setup(monkeypatch)
    from datetime import datetime, timezone
    monkeypatch.setattr(r5, "now_utc", lambda: datetime(2026, 11, 18, 12, 0, tzinfo=timezone.utc))
    pairs, n1, n4, a2, a3 = _tables()
    ctx = FakeCtx({"N1": n1, "N2": a2, "N3": a3, "N2-C25": a2, "N4": n4})
    with pytest.raises(RuntimeError, match="refusing to read N4"):
        run.step_r5(ctx, P, R)


def test_new_variant_keys_cut_as_specified():
    run = _run_module()
    P = dict(run.PARAMS, hr_c=1.0)
    pairs, a2, a3 = _test_wb()._synthetic()
    base = run.build_sample(pairs, a2, a3, P, {})
    shell = run.build_sample(pairs, a2, a3, P, {"pbar_max": 15.0})
    assert len(shell) and (shell["pbar"] <= 15.0).all() and len(shell) < len(base)
    th = run.build_sample(pairs, a2, a3, P, {"theta_min_arcsec": 100.0})
    assert (th["rsky"] * th["pbar"] / 1000.0 >= 100.0).all() and len(th) < len(base)
    xm = run.build_sample(pairs, a2, a3, P, {"x_min": 0.5})
    assert (xm["x"] >= 0.5).all() and len(xm) < len(base)


def test_r2_mode_parameters_unchanged(monkeypatch):
    """The R2 path receives exactly the pre-T-034 PARAMS (no mode, no r5_* keys)."""
    run = _run_module()
    seen = {}
    monkeypatch.setattr(run, "step_b", lambda ctx, P: seen.setdefault("P", P) and {} or {})

    class C:
        def save(self, name, obj):
            seen[name] = obj

        def log(self, m):
            pass
    run.main(C())
    assert "mode" not in seen["P"] and not any(k.startswith("r5_") for k in seen["P"])
    assert set(seen["summary"]["params"]) == set(seen["P"])


# ---------------------------------------------------------------- gate-1 minors
def test_g1b_step1_rederived_on_a_hand_table():
    """Cut order, masses (FLAME overrides M_G) and the sigma~ formula, re-derived by hand."""
    run = _run_module()
    P = dict(run.PARAMS, hr_c=1.0, d_max_pc=250.0, rsky_min_au=300.0)
    pairs, n1, n4, a2, a3 = _tables(n=60, seed=5)
    n1 = n1.copy()
    a2 = a2.copy()
    a2.loc[a2["source_id"] == n1.loc[0, "source_id_a"], "n"] = 2          # pair 0: degrouped
    n1.loc[1, ["parallax_a", "parallax_b"]] = 3.9                          # pair 1: d > 250 pc
    n1.loc[2, "ruwe_b"] = 1.3                                              # pair 2: RUWE
    n1.loc[3, "bp_rp_a"] = 0.4                                             # pair 3: HR band
    n1.loc[4, ["pmra_error_a", "pmdec_error_a", "pmra_error_b", "pmdec_error_b"]] = 50.0   # pair 4: sigma~
    x, tr = r5.g1b_step1(n1, a2, a3, P)
    assert tr["canonical"] == 60 and tr["degroup"] == 59 and tr["distance"] == 58
    assert tr["ruwe"] == tr["r_sky"] - 1 and tr["hr"] == tr["ruwe"] - 1 and tr["sigma_proxy"] == tr["hr"] - 1
    df = n1.iloc[5:].copy()
    pbar = (df.parallax_error_b ** 2 * df.parallax_a + df.parallax_error_a ** 2 * df.parallax_b) / (
        df.parallax_error_a ** 2 + df.parallax_error_b ** 2)
    rsky = wb.sky_separation_au(df.ra_a.values, df.dec_a.values, df.ra_b.values, df.dec_b.values, pbar.values)
    keep = (rsky >= 300) & (rsky <= 30000)
    flame = dict(zip(a3.source_id, a3.mass_flame))

    def m(s):
        ml = wb.mass_from_mg(df[f"phot_g_mean_mag_{s}"].values + 5 * np.log10(pbar.values / 100.0), 4.67)
        return np.array([flame.get(i, v) for i, v in zip(df[f"source_id_{s}"], ml)])
    M = m("a") + m("b")
    sig = 4.740470464 / pbar.values * np.sqrt((df.pmra_error_a ** 2 + df.pmdec_error_a ** 2 + df.pmra_error_b ** 2
                                                + df.pmdec_error_b ** 2).values / 2) / wb.vc_kms(M, rsky)
    xx = rsky / wb.r_mond_au(M, 1.2e-10)
    assert np.allclose(np.sort(x), np.sort(xx[keep & (sig < 0.1)]))


def test_e2_pooled_scale_k():
    pm = r5.power_mock()
    rng = np.random.default_rng(1)
    vt = rng.normal(0.5, 0.15, 400)
    fb = np.repeat([0, 1], 200)
    med = np.array([np.median(vt[fb == k]) for k in range(2)])
    sig = np.array([0.02, 0.03])
    out = r5.error_model_variants(vt, fb, 2, med, np.array([0.1, 2.0]), sig, 1.2e-10, 1.184, pm, 15)
    N = np.array([200, 200])
    k2 = np.sum(N * (N * sig ** 2 / med ** 2)) / np.sum(N)
    assert np.isclose(out["E2_pooled_scale"]["k"], np.sqrt(k2))


def test_r5_region_split_budget_release_and_stop():
    run = _run_module()
    P = dict(run.PARAMS, max_rows=100)
    calls = []

    class C:
        def tap(self, q, service, label="", **kw):
            calls.append(label)
            if label.startswith("count"):
                return pd.DataFrame({"n": [150 if label.endswith(" r") else 60]})
            if label.endswith(".1"):
                raise TimeoutError("fake")
            return pd.DataFrame({"x": range(60)})

        def log(self, m):
            pass
    budget = run.Budget(10 ** 9)
    region = dict(wb.strip_plan()[0])
    with pytest.raises(TimeoutError):
        run._r5_region(C(), P, "N1", "r", region, False, budget, lambda rr, nn, sel: sel, 10)
    assert calls[:3] == ["count N1 r", "count N1 r.0", "N1 r.0"] and "N1 r.1" in calls
    assert budget.used == 600                         # r.0 charged; the failed r.1 released
    with pytest.raises(run.StopAndAsk):
        run._r5_region(C(), P, "N1", "r", region, True, budget, lambda rr, nn, sel: sel, 10)
    with pytest.raises(run.StopAndAsk):               # StopAndAsk never falls back
        run._r5_with_fallback(C(), P, "N2", "r", region, True, budget,
                              lambda rr, nn, sel: sel, lambda rr, nn, sel: sel, 10)


def test_c25_budget_stop_marks_v9_not_run(monkeypatch):
    run, P, R = _setup(monkeypatch)
    pairs, n1, n4, a2, a3 = _tables()

    class C25Over(FakeCtx):
        def tap(self, q, service, label="", **kw):
            if label.startswith("count N2-C25"):
                return pd.DataFrame({"n": [6 * 10 ** 6]})       # 240 MB at 40 B per row: over the 200 MB budget
            return super().tap(q, service, label, **kw)
    P["max_rows"] = 10 ** 7
    monkeypatch.setattr(run, "_max_bytes", lambda: 10 ** 12)
    R["r5_stop_after_g1b"] = True
    ctx = C25Over({"N1": n1, "N2": a2, "N3": a3, "N2-C25": a2, "N4": n4})
    run.step_r5(ctx, P, R)
    s = ctx.saved["r5"]
    assert s["queries_a"]["n2_c25_rows"] is None
    assert "BudgetStop" in next(iter(s["queries_a"]["n2_c25_errors"].values()))
    assert s["g1b"]["passes"]


def test_map_regions_cancels_pending_on_first_failure():
    run = _run_module()
    P = dict(run.PARAMS, workers=1, region_limit=20)
    seen = []

    def fn(item):
        seen.append(item[0])
        if item[0] == "r001":
            raise TimeoutError("fake")
        if item[0] > "r001":
            time.sleep(0.2)          # still pending when r001 fails
        return item[0]
    with pytest.raises(TimeoutError):
        run._map_regions(P, fn)
    assert len(seen) < 20
