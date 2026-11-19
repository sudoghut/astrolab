"""Offline tests of R2-RE-SEL (README section 2, addendum 2026-11-19, T-042) on synthetic data: the two
selection criteria, the reduced system, the subset stream, seeds, labels, the reading rules and their
order, every not-evaluable rule, and an end-to-end pass whose d = N5584 path reproduces R2-RE-N5584 (a)."""
import copy
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).parent


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import n5584  # noqa: E402
import rob  # noqa: E402
import sel  # noqa: E402

COL = 26
TAU, OUTLIER, N_SUB = 0.05, 0.8, 120   # synthetic host scatter, N5584 offset (mag), subsets
CCHP = [0, 3, 7, 10, 12, 19, 21, 30, 33, 36]


@pytest.fixture(scope="module")
def lad():
    """The synthetic 37-host ladder of test_n5584 (host 26 = 'N5584' with an outlying SN), R4 draws on
    37 hosts, and the R2-RE-N5584 block run on it with small counts."""
    run = _load("run003_sel", "run.py")
    tn = _load("tn003_sel", "test_n5584.py")
    L, y, C = tn._synthetic(run, tau=TAU, outlier=OUTLIER)
    run.N_ROWS = len(y)
    nz, cls, _ = run.row_classes(L, y)
    groups = [np.flatnonzero(cls["calib"] & nz[:, j]) for j in range(run.NH)]
    rows_a = np.arange(len(y))
    other = [j for j in range(run.NH) if j not in CCHP]
    rows_s = np.array([i for i in rows_a if not nz[i, other].any()])
    labels = [f"H{j:02d}" for j in range(run.NH)]
    labels[COL] = "N5584"
    host_rows = [np.flatnonzero(nz[:, j]) for j in range(run.NH)]
    n_sn_col = [len(g) for g in groups]
    P = dict(run.PARAMS, r4_draws=N_SUB + 10, rob_n_tau=3, rob_n_spread=20, rob_n_subsets=N_SUB,
             sel_n_tau=6, sel_n_spread=40, sel_n_subsets=N_SUB)
    verdict = lambda z_, d_, s_: run.host_step_verdict(z_, d_, s_, P["host_ref"], P["host_ref_extra"])
    fns_n = {"reml_tau": run.reml_tau, "reml_m2l": run.reml_m2l, "host_step_under": run.host_step_under,
             "with_re": run.with_re, "fit": run.fit, "shift_vector": run.shift_vector,
             "is_fit_failure": run.is_fit_failure, "C_H0": run.C_H0, "r4_draws": run.r4_draws,
             "r4_summary": run.r4_summary, "r2_re_r4": run.r2_re_r4, "verdict": verdict}
    est = run.reml_tau(lambda t: run.reml_m2l(L, y, C, rows_a, groups, t), 0.5, 0.01)
    tau = 0.0 if est["at_zero"] else est["tau_hat"]
    hs, _ = run.host_step_under(L, y, run.with_re(C, groups, tau), rows_a, rows_s)
    re_out = {"status": "evaluated", "tau_hat": tau, "z": hs["z"],
              "verdict": verdict(hs["z"], hs["shift"], hs["shift_sigma"])}
    hc, res_a = run.host_step_under(L, y, C, rows_a, rows_s)
    r4 = {}
    any_host = nz[:, :run.NH].any(axis=1)
    base_rows = rows_a[~any_host]
    _, _, _, picks = run.r4_draws(L, y, C, rows_a, res_a, hc["fivelogh0_37"], hc["sigma_37"], base_rows,
                                  host_rows, np.arange(run.NH), 10, P["r4_draws"], P["r4_seed"], 60.0,
                                  n_sn_col, r4, lambda m: None)
    n_out = n5584.run_block(L, y, C, nz, cls, rows_a, rows_s, CCHP, groups, labels, host_rows, n_sn_col,
                            re_out, hc, P, fns_n, lambda m: None, expected_col=COL)
    fns = {"reml_tau": run.reml_tau, "reml_m2l": run.reml_m2l, "fit": run.fit,
           "shift_vector": run.shift_vector, "is_fit_failure": run.is_fit_failure, "loo_chi2": run.loo_chi2,
           "C_H0": run.C_H0}
    # criterion S on the real y, computed independently (direct fits, no estimator rows)
    use = picks[:P["sel_n_subsets"]]
    full = run.fit(L, y, C, rows_a)
    zk = []
    for pk in use:
        rows = np.union1d(base_rows, np.concatenate([host_rows[j] for j in pk]))
        r = run.fit(L, y, C, rows)
        zk.append((r["q"][run.C_H0] - full["q"][run.C_H0])
                  / np.sqrt(r["sigma"][run.C_H0] ** 2 - full["sigma"][run.C_H0] ** 2))
    zk = np.array(zk)
    s_indep = np.array([np.std(zk[[j not in pk for pk in use]]) for j in range(run.NH)])
    return dict(run=run, L=L, y=y, C=C, nz=nz, cls=cls, groups=groups, rows_a=rows_a, rows_s=rows_s,
                labels=labels, host_rows=host_rows, P=P, picks=picks, n_out=n_out, fns=fns,
                base_rows=base_rows, s_indep=s_indep, re_out=re_out, hc=hc)


def _rec(lad):
    a = lad["n_out"]["drop"]
    return a["r2_re"]["tau_hat"], a["bn"]["spread"]["spread_obs"]


def _block(lad, P=None, n_out=None, fns=None, picks=None, **kw):
    rt, rs = _rec(lad)
    args = dict(recorded_tau=rt, recorded_spread=rs, crit_s_expected=float(lad["s_indep"][COL]),
                expected_col=COL, n_pick=10)
    args.update(kw)
    return sel.run_block(lad["L"], lad["y"], lad["C"], lad["nz"], lad["rows_a"], lad["groups"], lad["labels"],
                         lad["host_rows"], lad["picks"] if picks is None else picks,
                         lad["n_out"] if n_out is None else n_out, lad["P"] if P is None else P,
                         lad["fns"] if fns is None else fns, lambda m: None, **args)


@pytest.fixture(scope="module")
def base_out(lad):
    return _block(lad)


# ---------------------------------------------------------------- criteria
def test_criterion_x_maps_reproduce_loo_chi2(lad):
    run, L, y, C, rows_a, groups = lad["run"], lad["L"], lad["y"], lad["C"], lad["rows_a"], lad["groups"]
    maps = sel.loo_maps(L, y, C, rows_a, groups, lad["fns"])
    for yy in (y, y + np.random.default_rng(5).normal(0, 0.1, len(y))):      # a fixed map: any y
        ref = np.array([h["chi2"] for h in run.loo_chi2(L, yy, C, rows_a, groups, lad["labels"])["per_host"]])
        got = sel.crit_x_values(maps, yy[rows_a])
        assert np.max(np.abs(got - ref) / ref) <= 1e-8           # the pre-registered tolerance
    assert sel.pick_max(sel.crit_x_values(maps, y[rows_a])) == COL


def test_criterion_s_matches_independent_fits(lad):
    """spread_excl from the estimator rows equals the direct-fit computation; it selects N5584."""
    run = lad["run"]
    use = lad["picks"][:lad["P"]["sel_n_subsets"]]
    full = run.fit(lad["L"], lad["y"], lad["C"], lad["rows_a"], est=True)
    M, sig = rob.shift_rows(lad["L"], lad["y"], lad["C"], lad["rows_a"], full, use, lad["base_rows"],
                            lad["host_rows"], lad["fns"])
    excl = [np.array([j not in pk for pk in use]) for j in range(run.NH)]
    v = sel.crit_s_values(M, sig, excl, lad["y"][lad["rows_a"]])
    assert np.allclose(v, lad["s_indep"], rtol=1e-9, atol=0)
    assert sel.pick_min(v) == COL


def test_ties_go_to_the_lowest_column():
    assert sel.pick_max(np.array([1.0, 3.0, 2.0, 3.0])) == 1
    assert sel.pick_min(np.array([2.0, 0.5, np.nan, 0.5])) == 1
    assert sel.pick_min(np.array([np.nan, 0.5, 0.5])) == 1


def test_reduced_system_is_drop_host_without_cchp_guard(lad):
    """For d = N5584 the reduced system is n5584.drop_host's; for a CCHP host drop_host refuses (guard) while
    this block builds it."""
    nz, rows_a, groups, host_rows = lad["nz"], lad["rows_a"], lad["groups"], lad["host_rows"]
    red = sel.reduced_system(nz, rows_a, COL, groups, host_rows)
    a = lad["n_out"]["drop"]
    assert len(red["rows_n"]) == a["rows_reduced"] == len(rows_a) - a["rows_removed"]["total"]
    assert not nz[red["rows_n"], COL].any() and len(red["groups_n"]) == 36
    assert list(red["host_cols_n"]) == [j for j in range(37) if j != COL]
    any_host = nz[:, :37].any(axis=1)
    assert np.array_equal(red["base_n"], np.array([i for i in red["rows_n"] if not any_host[i]]))
    assert all(np.array_equal(red["host_rows_n"][j], np.intersect1d(host_rows[j], red["rows_n"]))
               for j in range(37))
    # tau_hat on the real y for d = N5584 equals (a)'s reduced-system tau_hat bitwise
    run, L, y, C = lad["run"], lad["L"], lad["y"], lad["C"]
    est = run.reml_tau(lambda t: run.reml_m2l(L, y, C, red["rows_n"], red["groups_n"], t), 0.5, 0.01,
                       interval=False)
    assert est["tau_hat"] == a["r2_re"]["reml"]["tau_hat"]
    # a CCHP host
    d = CCHP[0]
    with pytest.raises(RuntimeError):
        n5584.drop_host(L, y, C, nz, lad["cls"], rows_a, lad["rows_s"], d, CCHP, groups, lad["labels"],
                        host_rows, [1] * 37, lad["P"], {}, lambda m: None)
    red_c = sel.reduced_system(nz, rows_a, d, groups, host_rows)
    assert not nz[red_c["rows_n"], d].any() and d not in red_c["host_cols_n"]
    res = run.fit(L, y, C, red_c["rows_n"], est=True)
    stream = sel.index_stream(5, 0, 36, 10)
    M, sig = rob.shift_rows(L, y, C, red_c["rows_n"], res, [red_c["host_cols_n"][ix] for ix in stream],
                            red_c["base_n"], red_c["host_rows_n"], lad["fns"])
    assert M.shape == (5, len(red_c["rows_n"])) and np.all(sig > 0)


def test_index_stream_is_r4n_stream(lad):
    stream = sel.index_stream(5, lad["P"]["r4_seed"], 36, 10)
    cols = np.array([j for j in range(37) if j != COL])
    assert [[int(j) for j in cols[ix]] for ix in stream] == lad["n_out"]["drop"]["r4n"]["first_picks"]
    assert all(ix.dtype == np.int64 for ix in stream)


# ---------------------------------------------------------------- labels and reading (pure)
def test_labels_three_way():
    assert sel.tau_label(2, 400)[0] == sel.TAU_UNUSUAL == "τ̂_N unusual under the selected null"
    assert sel.tau_label(60, 400)[0] == sel.TAU_USUAL == "τ̂_N not unusual under the selected null"
    assert sel.tau_label(14, 400)[0] == "undetermined (Monte Carlo)"
    assert sel.spread_label(5, 2000, "X")[0] == "the 36-host spread is unusual under the selected null (X)"
    assert sel.spread_label(500, 2000, "S")[0] == "the 36-host spread is consistent with the selected null (S)"
    assert sel.spread_label(100, 2000, "S")[0] == "undetermined (Monte Carlo)"


def _ev(label):
    return {"status": "evaluated", "label": label}


def test_reading_rules_and_order():
    ux, us = sel.SPREAD_UNUSUAL.format(c="X"), sel.SPREAD_UNUSUAL.format(c="S")
    cx, cs = sel.SPREAD_USUAL.format(c="X"), sel.SPREAD_USUAL.format(c="S")
    und = "undetermined (Monte Carlo)"
    ne = {"status": "not evaluable (R4 has no draws)"}
    T_U, T_N = sel.TAU_UNUSUAL, sel.TAU_USUAL
    # (1) any part not evaluable, even with labels that would otherwise give (3)
    assert sel.reading(ne, _ev(ux), _ev(us)) == "not evaluable"
    assert sel.reading(_ev(T_N), ne, _ev(cs)) == "not evaluable"
    assert sel.reading(_ev(T_N), _ev(cx), ne) == "not evaluable"
    # (2)
    for t in (T_N, und):
        assert sel.reading(_ev(t), _ev(cx), _ev(cs)) == (
            "the excess calibrator scatter of R2-RE-ROB is consistent with one outlying host, selection included")
    # (3) X, S or both; before (4) and regardless of tau
    base = "excess scatter remains after removing the most extreme host, selection included (criterion "
    assert sel.reading(_ev(T_U), _ev(ux), _ev(cs)) == base + "X)"
    assert sel.reading(_ev(T_N), _ev(und), _ev(us)) == base + "S)"
    assert sel.reading(_ev(und), _ev(ux), _ev(us)) == base + "both)"
    # (4)
    assert sel.reading(_ev(T_U), _ev(cx), _ev(cs)) == (
        "τ excess remains after removing the most extreme host, selection included")
    # (5)
    assert sel.reading(_ev(T_N), _ev(und), _ev(cs)) == "undetermined"
    assert sel.reading(_ev(T_U), _ev(cx), _ev(und)) == "undetermined"
    # what each reading changes in section 5
    assert sel.section5_action(sel.READ_CONSISTENT) == sel.SECTION5["consistent"]
    assert sel.section5_action(base + "both)") == sel.SECTION5["withdrawn"]
    assert sel.section5_action(sel.READ_TAU) == sel.SECTION5["withdrawn"]
    assert sel.section5_action("undetermined") == sel.SECTION5["stays"]
    assert sel.section5_action("not evaluable") == sel.SECTION5["stays"]
    assert sel.not_lowered(0.34, 0.339) is True and sel.not_lowered(0.2, 0.339) is False
    assert sel.not_lowered(None, 0.3) is None


def test_observed_value_tolerances():
    t, s = sel.RECORDED_TAU_N, sel.RECORDED_SPREAD_OBS
    assert sel.observed_mismatches(t * (1 + 9e-7), s * (1 + 9e-10), t, s) == []
    assert len(sel.observed_mismatches(t * (1 + 2e-6), s, t, s)) == 1
    assert len(sel.observed_mismatches(t, s * (1 + 2e-9), t, s)) == 1
    assert sel.observed_mismatches(None, None, t, s) == []
    assert (t, s) == (0.03137144323410943, 1.0325254787240916)


# ---------------------------------------------------------------- the block, end to end
def test_block_end_to_end(lad, base_out, tmp_path, monkeypatch):
    out, P = base_out, lad["P"]
    assert out["status"] == "evaluated" and out["column"] == COL and out["host"] == "N5584"
    for part in ("tau", "spread_X", "spread_S"):
        assert out[part]["status"] == "evaluated", out[part]
    # the d = N5584 path reproduces B-N's spread_obs bitwise and (a)'s tau_hat is the observed value
    _, rs = _rec(lad)
    assert out["checks"]["spread_obs_d_host"]["value"] == rs
    assert out["tau"]["tau_obs"] == lad["n_out"]["drop"]["r2_re"]["tau_hat"]
    assert out["checks"]["loo_maps"]["max_rel_diff"] <= 1e-8
    assert out["checks"]["criterion_x_selects"]["column"] == COL
    assert out["checks"]["criterion_s"]["selects"]["column"] == COL
    assert abs(out["checks"]["criterion_s"]["host_value"] - lad["s_indep"][COL]) < 1e-9
    assert out["checks"]["first_subsets"]["first_picks"] == lad["n_out"]["drop"]["r4n"]["first_picks"]
    # counts, p values, labels and the reading follow the rules
    t = out["tau"]
    assert t["n_sims"] == 6 and t["n_ok"] + t["n_failed"] == 6
    assert t["p"] == (1 + t["k"]) / (1 + t["n_ok"]) and t["label"] == sel.tau_label(t["k"], t["n_ok"])[0]
    for name, c in (("spread_X", "X"), ("spread_S", "S")):
        sp = out[name]
        assert sp["n_sims"] == 40 and len(sp["spreads"]) == 40
        near = sum(1 for v in sp["spreads"] if abs(v - rs) <= 5e-7)      # spreads saved rounded to 1e-6
        assert abs(sp["k"] - sum(1 for v in sp["spreads"] if v >= rs)) <= near
        assert sp["p"] == (1 + sp["k"]) / 41 and sp["label"] == sel.spread_label(sp["k"], 40, c)[0]
    assert out["reading"] == sel.reading(out["tau"], out["spread_X"], out["spread_S"])
    assert out["section5"] == sel.section5_action(out["reading"])
    dx, ds = out["selection"]["X"]["dropped"], out["selection"]["S"]["dropped"]
    assert len(dx) == len(ds) == 40
    assert sum(out["selection"]["X"]["frequency_all"].values()) == 40
    assert sum(out["selection"]["X"]["frequency_first_tau"].values()) == 6
    assert out["selection"]["n_same_X_S"] == sum(a == b for a, b in zip(dx, ds))
    assert out["dropped_hosts_built"]["n_distinct"] == len(set(dx) | set(ds) | {COL})
    assert out["extremeness"]["max_loo_chi2"]["n"] == 40
    assert len(out["real_criteria"]) == 37
    # the conclusion test re-derives the labels from the saved file
    from astrolab.results import write_json
    write_json(tmp_path / "r2_re_sel.json", out)
    write_json(tmp_path / "r2_re_n5584.json", lad["n_out"])
    write_json(tmp_path / "summary.json", {"R2_RE_SEL": sel.summary(out)})
    tc = _load("tc003_sel", "test_conclusions.py")
    monkeypatch.setattr(tc, "RESULTS", tmp_path)
    monkeypatch.setattr(tc, "SEL_RECORDED", _rec(lad))
    tc.test_r2_re_sel_labels()


def test_seeds_and_selection_on_simulated_data(lad, base_out):
    """Simulation s uses default_rng(sel_seed_base + s) on len(rows_a); its X host is loo_chi2's argmax and
    its tau_hat is REML on that host's reduced system."""
    run, L, y, C, rows_a, groups = lad["run"], lad["L"], lad["y"], lad["C"], lad["rows_a"], lad["groups"]
    full = run.fit(L, y, C, rows_a)
    kept = full["kept"]
    yhat = L[np.ix_(rows_a, kept)] @ full["q"][kept]
    K = np.linalg.cholesky(C[np.ix_(rows_a, rows_a)])
    for s in (0, 1, 5):
        ys = y.copy()
        ys[rows_a] = yhat + K @ np.random.default_rng(20_000 + s).standard_normal(len(rows_a))
        chi = [h["chi2"] for h in run.loo_chi2(L, ys, C, rows_a, groups, lad["labels"])["per_host"]]
        d = int(np.argmax(chi))
        assert base_out["selection"]["X"]["dropped"][s] == d
        red = sel.reduced_system(lad["nz"], rows_a, d, groups, lad["host_rows"])
        est = run.reml_tau(lambda t: run.reml_m2l(L, ys, C, red["rows_n"], red["groups_n"], t), 0.5, 0.01,
                           interval=False)
        assert base_out["tau"]["taus"][s] == round(est["tau_hat"], 5)
    other = _block(lad, P=dict(lad["P"], sel_seed_base=10_000, sel_n_tau=1, sel_n_spread=6))
    assert other["selection"]["X"]["dropped"] != base_out["selection"]["X"]["dropped"][:6] or \
        other["tau"]["taus"][0] != base_out["tau"]["taus"][0]


# ---------------------------------------------------------------- not-evaluable rules
SMALL = dict(sel_n_tau=2, sel_n_spread=6)


def _small(lad, **kw):
    return dict(lad["P"], **{**SMALL, **kw})


def test_observed_mismatch_stops_the_block(lad):
    rt, rs = _rec(lad)
    out = _block(lad, P=_small(lad), recorded_tau=rt * (1 + 2e-6))
    assert out["status"] == sel.BLOCK_NE_OBSERVED and out["reading"] == "not evaluable"
    assert "tau" not in out and "spread_X" not in out
    out = _block(lad, P=_small(lad), recorded_spread=rs * (1 + 2e-9))
    assert out["status"] == sel.BLOCK_NE_OBSERVED
    out = _block(lad, P=_small(lad), recorded_tau=rt * (1 + 5e-7))       # within 1e-6: runs
    assert out["status"] == "evaluated" and out["tau"]["status"] == "evaluated"


def test_tau_part_not_evaluable_without_reduced_r2_re(lad):
    n_out = copy.deepcopy(lad["n_out"])
    n_out["drop"]["r2_re"]["status"] = "not evaluable (bound)"
    out = _block(lad, P=_small(lad), n_out=n_out)
    assert out["tau"]["status"].startswith("not evaluable (R2-RE-N5584 (a)")
    assert out["spread_X"]["status"] == out["spread_S"]["status"] == "evaluated"
    assert out["reading"] == "not evaluable"


def test_spread_parts_not_evaluable_without_bn_spread(lad):
    n_out = copy.deepcopy(lad["n_out"])
    n_out["drop"]["bn"]["spread"] = {"status": "not evaluable (R4 has no draws)"}
    out = _block(lad, P=_small(lad), n_out=n_out)
    assert out["tau"]["status"] == "evaluated"
    for p in ("spread_X", "spread_S"):
        assert out[p]["status"] == "not evaluable (B-N's spread part not evaluated)"
    assert out["reading"] == "not evaluable"


def test_criterion_s_not_evaluable_without_r4_draws(lad):
    out = _block(lad, P=_small(lad), picks=[])
    assert out["spread_S"]["status"] == "not evaluable (R4 has no draws)"
    assert out["tau"]["status"] == out["spread_X"]["status"] == "evaluated"
    assert "S" not in out["selection"]


def test_loo_fit_failure_x_parts_not_evaluable(lad):
    def bad(*a, **k):
        raise ValueError("L^T C^-1 L is rank deficient (forced)")
    out = _block(lad, P=_small(lad), fns=dict(lad["fns"], loo_chi2=bad))
    assert out["tau"]["status"].startswith("not evaluable (a leave-one-out fit under C failed")
    assert out["spread_X"]["status"].startswith("not evaluable (a leave-one-out fit under C failed")
    assert out["spread_S"]["status"] == "evaluated"


def test_loo_map_mismatch_is_a_bug(lad):
    def off(*a, **k):
        r = lad["run"].loo_chi2(*a, **k)
        r["per_host"][3]["chi2"] *= 1 + 1e-6
        return r
    with pytest.raises(RuntimeError, match="do not reproduce loo_chi2"):
        _block(lad, P=_small(lad), fns=dict(lad["fns"], loo_chi2=off))


def test_criterion_x_not_selecting_host(lad, monkeypatch):
    calls = []
    real = sel.pick_max

    def first_wrong(v):
        calls.append(1)
        return 0 if len(calls) == 1 else real(v)
    monkeypatch.setattr(sel, "pick_max", first_wrong)
    out = _block(lad, P=_small(lad))
    for p in ("tau", "spread_X"):
        assert out[p]["status"] == "not evaluable (criterion X does not select N5584 on the real data (selects H00))"
    assert out["spread_S"]["status"] == "evaluated"


def test_criterion_s_not_selecting_host_or_not_reproduced(lad, monkeypatch):
    v = float(lad["s_indep"][COL])
    out = _block(lad, P=_small(lad), crit_s_expected=v + 0.002)
    assert out["spread_S"]["status"].startswith("not evaluable (criterion S reproduction")
    assert out["tau"]["status"] == out["spread_X"]["status"] == "evaluated"
    out = _block(lad, P=_small(lad), crit_s_expected=v + 0.0009)
    assert out["spread_S"]["status"] == "evaluated"
    calls = []
    real = sel.pick_min

    def first_wrong(x):
        calls.append(1)
        return 1 if len(calls) == 1 else real(x)
    monkeypatch.setattr(sel, "pick_min", first_wrong)
    out = _block(lad, P=_small(lad))
    assert out["spread_S"]["status"] == "not evaluable (criterion S does not select N5584 on the real data (selects H01))"
    assert out["tau"]["status"] == "evaluated"


@pytest.mark.parametrize("n_fail,expect", [(1, "evaluated"), (2, "not evaluable (too many failed fits)")])
def test_tau_failed_fit_limit(lad, n_fail, expect):
    n = [0]

    def flaky(f, *a, **k):
        n[0] += 1
        if n[0] <= n_fail:
            raise np.linalg.LinAlgError("forced")
        return lad["run"].reml_tau(f, *a, **k)
    out = _block(lad, P=_small(lad, sel_n_tau=3, sel_max_failed=1), fns=dict(lad["fns"], reml_tau=flaky))
    t = out["tau"]
    assert t["status"] == expect and t["n_failed"] == n_fail and t["n_ok"] == 3 - n_fail
    if expect == "evaluated":
        assert t["p"] == (1 + t["k"]) / (1 + t["n_ok"])
    else:
        assert out["reading"] == "not evaluable"


def test_fit_failure_building_rows_for_a_dropped_host(lad, base_out):
    """A failed fit while building the rows for a dropped host d != N5584 makes the parts that selected d
    not evaluable (fit)."""
    dx = base_out["selection"]["X"]["dropped"][:6]
    ds = base_out["selection"]["S"]["dropped"][:6]
    cands = [d for d in dx if d != COL]
    if not cands:
        pytest.skip("no simulation drops another host under X in the first 6")
    d = cands[0]
    rows_n = sel.reduced_system(lad["nz"], lad["rows_a"], d, lad["groups"], lad["host_rows"])["rows_n"]
    real_fit = lad["run"].fit

    def fit(L, y, C, rows, est=False):
        if np.array_equal(np.asarray(rows), rows_n):
            raise ValueError("C is not positive definite: forced")
        return real_fit(L, y, C, rows, est=est)
    out = _block(lad, P=_small(lad), fns=dict(lad["fns"], fit=fit))
    assert out["spread_X"]["status"] == f"not evaluable (fit: building the rows for dropped host {lad['labels'][d]})"
    if d in ds:
        assert out["spread_S"]["status"].startswith("not evaluable (fit: building the rows for dropped host")
    else:
        assert out["spread_S"]["status"] == "evaluated"
    assert lad["labels"][d] in out["dropped_hosts_built"]["failed"]
    assert out["reading"] == "not evaluable"


def test_reproduction_failures_stop_the_run(lad):
    n_out = copy.deepcopy(lad["n_out"])
    n_out["drop"]["r4n"]["first_picks"][0][0] += 1
    with pytest.raises(RuntimeError, match="first subsets"):
        _block(lad, P=_small(lad), n_out=n_out)
    # spread_obs consistent with the recorded value but not reproduced by the d = N5584 path
    n_out = copy.deepcopy(lad["n_out"])
    rs = n_out["drop"]["bn"]["spread"]["spread_obs"] * (1 + 1e-6)
    n_out["drop"]["bn"]["spread"]["spread_obs"] = rs
    with pytest.raises(RuntimeError, match="d = N5584 path"):
        _block(lad, P=_small(lad), n_out=n_out, recorded_spread=rs)


def test_wrong_column_is_refused(lad):
    with pytest.raises(RuntimeError):
        _block(lad, P=_small(lad), expected_col=25)
