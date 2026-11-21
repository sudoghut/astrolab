"""Offline tests of R2-RE-D (README section 2, addendum 2026-11-21, T-048) on synthetic data only: the
statistics on a small synthetic system, the offset only on the chosen rows, the common eps_s across models,
D and J from known inputs, the calibration of J on two bivariate-normal toys, the reading rules (1)-(5) in
order with their qualifiers, every not-evaluable rule, the standalone summary update, and the label
re-derivation from the saved files (test_conclusions.test_r2_re_d_labels)."""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import onehost  # noqa: E402
import rob  # noqa: E402
import sel  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


COL = 26
TAU, OUTLIER, N_SUB = 0.05, 0.8, 120     # synthetic host scatter, N5584 offset (mag), subsets
TAUS = [0.05, 0.077, 0.105]


def _direct_spread(run, L, y, C, rows, base, host_rows, use):
    """Delta_k / sigma_k over subsets by direct fits (no estimator rows) against the reference fit on rows."""
    full = run.fit(L, y, C, rows)
    zk = []
    for pk in use:
        r = run.fit(L, y, C, np.union1d(base, np.concatenate([host_rows[j] for j in pk])))
        zk.append((r["q"][run.C_H0] - full["q"][run.C_H0])
                  / np.sqrt(r["sigma"][run.C_H0] ** 2 - full["sigma"][run.C_H0] ** 2))
    return np.array(zk)


def _direct_delta(L, y, C, rows, h_rows):
    """delta_hat by an independent weighted least-squares solve (C is diagonal in the synthetic system)."""
    X = L[rows]
    X = X[:, np.any(X != 0, axis=0)]
    h = np.isin(rows, h_rows).astype(float)[:, None]
    X = np.hstack([X, h])
    w = 1.0 / np.diag(C)[rows]
    F = X.T @ (w[:, None] * X)
    q = np.linalg.solve(F, X.T @ (w * y[rows]))
    return q[-1], np.sqrt(np.linalg.inv(F)[-1, -1])


def _build(name):
    run = _load(name, "run.py")
    tn = _load("tn003_" + name, "test_n5584.py")
    L, y, C = tn._synthetic(run, tau=TAU, outlier=OUTLIER)
    rows_a = np.arange(len(y))
    run.N_ROWS = len(y)
    nz, cls, _ = run.row_classes(L, y)
    groups = [np.flatnonzero(cls["calib"] & nz[:, j]) for j in range(run.NH)]
    labels = [f"H{j:02d}" for j in range(run.NH)]
    labels[COL] = "N5584"
    host_rows = [np.flatnonzero(nz[:, j]) for j in range(run.NH)]
    picks = sel.index_stream(N_SUB, 0, run.NH, 10)
    fns = {"reml_tau": run.reml_tau, "reml_m2l": run.reml_m2l, "fit": run.fit, "shift_vector": run.shift_vector,
           "with_re": run.with_re, "is_fit_failure": run.is_fit_failure, "C_H0": run.C_H0}
    any_host = nz[:, :run.NH].any(axis=1)
    base = np.array([i for i in rows_a if not any_host[i]])
    # independent observed values (direct fits)
    z37 = _direct_spread(run, L, y, C, rows_a, base, host_rows, picks)
    excl = np.array([[j not in pk for pk in picks] for j in range(run.NH)])
    s_excl = np.array([np.std(z37[e]) for e in excl])
    red = sel.reduced_system(nz, rows_a, COL, groups, host_rows)
    use36 = [red["host_cols_n"][ix] for ix in sel.index_stream(N_SUB, 0, 36, 10)]
    z36 = _direct_spread(run, L, y, C, red["rows_n"], red["base_n"], red["host_rows_n"], use36)
    est = run.reml_tau(lambda t: run.reml_m2l(L, y, C, red["rows_n"], red["groups_n"], t), 0.5, 0.01,
                       interval=False)
    delta, sd = _direct_delta(L, y, C, rows_a, groups[COL])
    recorded = {"spread_37": float(np.std(z37)), "spread_36": float(np.std(z36)),
                "crit_s": float(s_excl[COL]), "delta_hat": float(delta),
                "tau_n": 0.0 if est["at_zero"] else est["tau_hat"]}
    P = dict(run.PARAMS, rob_n_subsets=N_SUB, d_n_sims=40, d_kde_boot=5)
    return dict(run=run, L=L, y=y, C=C, nz=nz, groups=groups, rows_a=rows_a, labels=labels, host_rows=host_rows,
                picks=picks, fns=fns, P=P, recorded=recorded, s_excl=s_excl, sigma_delta=sd, base=base,
                red=red, use36=use36)


@pytest.fixture(scope="module")
def lad():
    return _build("run003_d")


def _block(lad, P=None, fns=None, picks=None, recorded=None, **kw):
    rc = dict(lad["recorded"])
    rc.update(recorded or {})
    kw.setdefault("expected_col", COL)
    return onehost.run_block(lad["L"], lad["y"], lad["C"], lad["nz"], lad["rows_a"], lad["groups"],
                             lad["labels"], lad["host_rows"], lad["picks"] if picks is None else picks,
                             lad["P"] if P is None else P, lad["fns"] if fns is None else fns, lambda m: None,
                             n_pick=10, recorded=rc, **kw)


@pytest.fixture(scope="module")
def base(lad):
    return _block(lad)


def _small(lad, **kw):
    return dict(lad["P"], **{"d_n_sims": 6, "d_kde_boot": 2, **kw})


# ---------------------------------------------------------------- settings and names
def test_params_and_constants():
    run = _load("run003_d_params", "run.py")
    P = run.PARAMS
    assert (P["d_check"], P["d_seed_base"], P["d_n_sims"], P["d_taus"], P["d_host_seed_base"], P["d_kde_boot"],
            P["d_only"]) == (True, 100_000, 10_000, [0.05, 0.077, 0.105], 200_000, 200, False)
    assert onehost.model_keys(P["d_taus"]) == ["C", "V050", "V077", "V105", "O", "Olo", "OVN", "Oany"]
    assert onehost.decisive_keys(P["d_taus"]) == ["V050", "V077", "V105", "O"]
    assert onehost.RECORDED_SPREAD_37 == 1.3070929081086322
    assert onehost.RECORDED_SPREAD_36 == 1.0325254787240916
    assert (onehost.RECORDED_DELTA, onehost.DELTA_ATOL, onehost.SPREAD_RTOL) == (0.33634, 5e-6, 1e-9)
    assert abs(0.33633686472064284 - onehost.RECORDED_DELTA) <= onehost.DELTA_ATOL   # the cache-only reproduction
    assert (onehost.CRIT_S_EXPECTED, onehost.CRIT_S_TOL) == (1.027, 0.001)
    assert onehost.RECORDED_TAU_N == 0.03137144323410943 and onehost.KDE_SEED_BASE == 300_000
    tc = _load("tc003_d_consts", "test_conclusions.py")
    assert tc.D_RECORDED == {"spread_37": onehost.RECORDED_SPREAD_37, "spread_36": onehost.RECORDED_SPREAD_36,
                             "crit_s": onehost.CRIT_S_EXPECTED, "delta_hat": onehost.RECORDED_DELTA}


def test_r4_draws_are_the_r4_index_stream(lad):
    """The standalone mode regenerates R4's subsets with sel.index_stream(n, r4_seed, 37, 10): the same
    subsets, in order, as R4's draw loop."""
    run, L, y, C, rows_a = lad["run"], lad["L"], lad["y"], lad["C"], lad["rows_a"]
    res_a = run.fit(L, y, C, rows_a, est=True)
    _, _, _, picks = run.r4_draws(L, y, C, rows_a, res_a, float(res_a["q"][run.C_H0]),
                                  float(res_a["sigma"][run.C_H0]), lad["base"],
                                  lad["host_rows"], np.arange(run.NH), 10, 30, 0, 60.0, [1] * run.NH, {},
                                  lambda m: None)
    assert [list(p) for p in picks] == [list(p) for p in sel.index_stream(30, 0, run.NH, 10)]


# ---------------------------------------------------------------- the statistic on the synthetic system
def test_observed_statistic_matches_direct_fits(lad, base):
    out, _ = base
    ob, rc = out["observed"], lad["recorded"]
    assert out["status"] == "evaluated", out["status"]
    assert abs(ob["spread_37"] - rc["spread_37"]) <= 1e-9 * rc["spread_37"]
    assert abs(ob["spread_36"] - rc["spread_36"]) <= 1e-9 * rc["spread_36"]
    assert ob["D"] == ob["spread_37"] - ob["spread_36"]
    assert ob["crit_s_selects_host"] and ob["crit_s_selected"] == "N5584"
    assert abs(ob["crit_s_host_value"] - lad["s_excl"][COL]) < 1e-9
    assert abs(ob["D_proxy"] - (ob["spread_37"] - np.min(lad["s_excl"]))) < 1e-9
    assert abs(ob["delta_hat"] - rc["delta_hat"]) <= 1e-9 * abs(rc["delta_hat"])
    assert abs(ob["sigma_delta"] - lad["sigma_delta"]) <= 1e-9 * lad["sigma_delta"]
    assert ob["delta_hat"] > 0.5            # the planted offset (0.8 mag) shows up
    assert out["tau_hat_N"]["status"] == "reproduced"
    assert out["checks"]["first_subsets_36"] == [[int(j) for j in c] for c in lad["use36"][:5]]


def test_simulated_statistics_match_direct_computation(lad, base):
    """Simulations s = 0, 1, 5 under C, V(0.077), O and O_any rebuilt by hand (eps from default_rng(100_000 + s),
    the offset host from default_rng(200_000 + s)): spread_37 (direct fits), d' (argmin of spread_excl) and
    spread_36 for d' (direct fits on the reduced system) equal the saved values."""
    run, L, y, C, rows_a, groups = lad["run"], lad["L"], lad["y"], lad["C"], lad["rows_a"], lad["groups"]
    _, sims = base
    full = run.fit(L, y, C, rows_a)
    yhat = L[np.ix_(rows_a, full["kept"])] @ full["q"][full["kept"]]
    Kc = np.linalg.cholesky(C[np.ix_(rows_a, rows_a)])
    Kv = np.linalg.cholesky(run.with_re(C, groups, 0.077)[np.ix_(rows_a, rows_a)])
    delta = lad["recorded"]["delta_hat"]
    excl = np.array([[j not in pk for pk in lad["picks"]] for j in range(run.NH)])
    for s in (0, 1, 5):
        eps = np.random.default_rng(100_000 + s).standard_normal(len(rows_a))
        hany = int(np.random.default_rng(200_000 + s).integers(0, 37))
        yc = yhat + Kc @ eps
        cases = {"C": yc, "V077": yhat + Kv @ eps, "O": yc.copy(), "Oany": yc.copy()}
        cases["O"][groups[COL]] += delta
        cases["Oany"][groups[hany]] += delta
        assert sims["Oany"]["offset_host"][s] == hany
        for k, ya in cases.items():
            ys = y.copy()
            ys[rows_a] = ya
            z = _direct_spread(run, L, ys, C, rows_a, lad["base"], lad["host_rows"], lad["picks"])
            d = int(np.argmin([np.std(z[e]) for e in excl]))
            assert sims[k]["dropped"][s] == d, (k, s)
            red = sel.reduced_system(lad["nz"], rows_a, d, groups, lad["host_rows"])
            use = [red["host_cols_n"][ix] for ix in sel.index_stream(N_SUB, 0, 36, 10)]
            z36 = _direct_spread(run, L, ys, C, red["rows_n"], red["base_n"], red["host_rows_n"], use)
            assert abs(sims[k]["pairs"][s][0] - np.std(z)) <= 5e-5 + 1e-9, (k, s)
            assert abs(sims[k]["pairs"][s][1] - np.std(z36)) <= 5e-5 + 1e-9, (k, s)


def test_crit_s_batch_equals_sel(lad):
    run = lad["run"]
    full = run.fit(lad["L"], lad["y"], lad["C"], lad["rows_a"], est=True)
    M, sig = rob.shift_rows(lad["L"], lad["y"], lad["C"], lad["rows_a"], full, lad["picks"], lad["base"],
                            lad["host_rows"], lad["fns"])
    excl = [np.array([j not in pk for pk in lad["picks"]]) for j in range(run.NH)]
    Y = lad["y"][lad["rows_a"]][:, None] + np.random.default_rng(1).normal(0, 0.05, (len(lad["rows_a"]), 4))
    got = onehost.crit_s_batch((M @ Y) / sig[:, None], excl)
    for i in range(4):
        assert np.allclose(got[:, i], sel.crit_s_values(M, sig, excl, Y[:, i]), rtol=1e-12, atol=0)


# ---------------------------------------------------------------- models: offset rows, common eps
def test_offset_only_on_the_chosen_rows(lad):
    rows_a, groups = lad["rows_a"], lad["groups"]
    n = len(rows_a)
    gpos = [np.searchsorted(rows_a, g) for g in groups]
    specs = onehost.model_specs(TAUS, COL, 0.3, 0.1, 0.03)
    K = np.eye(n) * 0.1
    yhat = np.linspace(0, 1, n)
    s_list = np.array([0, 3, 9])
    E = onehost.eps_block(100_000, s_list, n)
    hosts = onehost.offset_hosts(200_000, 10, 37)
    assert list(hosts) == [int(np.random.default_rng(200_000 + s).integers(0, 37)) for s in range(10)]
    yc = onehost.model_y(specs["C"], K, yhat, E, s_list, gpos, hosts)
    for key, dlt in (("O", 0.3), ("Olo", 0.2)):
        diff = onehost.model_y(specs[key], K, yhat, E, s_list, gpos, hosts) - yc
        mask = np.zeros(n, bool)
        mask[gpos[COL]] = True
        assert np.allclose(diff[mask], dlt, rtol=0, atol=1e-15) and np.all(diff[~mask] == 0)
    diff = onehost.model_y(specs["Oany"], K, yhat, E, s_list, gpos, hosts) - yc
    for i, s in enumerate(s_list):
        mask = np.zeros(n, bool)
        mask[gpos[hosts[s]]] = True
        assert np.allclose(diff[mask, i], 0.3, rtol=0, atol=1e-15) and np.all(diff[~mask, i] == 0)
    assert specs["O"]["offset"] == COL and np.array_equal(groups[COL], rows_a[gpos[COL]])


def test_common_eps_across_models(lad):
    """eps_s = default_rng(100_000 + s).standard_normal(len(rows_a)) for every model; V(tau) differs from C
    only through K; O(delta) is exactly y_C + delta h."""
    run, C, rows_a, groups = lad["run"], lad["C"], lad["rows_a"], lad["groups"]
    n = len(rows_a)
    s_list = np.array([2, 7])
    E = onehost.eps_block(100_000, s_list, n)
    for i, s in enumerate(s_list):
        assert np.array_equal(E[:, i], np.random.default_rng(100_000 + s).standard_normal(n))
    specs = onehost.model_specs(TAUS, COL, 0.3, 0.1, 0.03)
    yhat = np.zeros(n)
    gpos = [np.searchsorted(rows_a, g) for g in groups]
    Kc = np.linalg.cholesky(C[np.ix_(rows_a, rows_a)])
    Kv = np.linalg.cholesky(run.with_re(C, groups, 0.105)[np.ix_(rows_a, rows_a)])
    yc = onehost.model_y(specs["C"], Kc, yhat, E, s_list, gpos)
    yv = onehost.model_y(specs["V105"], Kv, yhat, E, s_list, gpos)
    yo = onehost.model_y(specs["O"], Kc, yhat, E, s_list, gpos)
    assert np.array_equal(yc, Kc @ E) and np.array_equal(yv, Kv @ E)
    assert np.allclose(yo - yc, 0.3 * np.isin(rows_a, groups[COL])[:, None], rtol=0, atol=1e-15)
    assert specs["V105"]["tau"] == 0.105 and specs["OVN"]["tau"] == 0.03 and specs["OVN"]["offset"] == COL


def test_models_share_eps_in_the_block(lad, base):
    """O is C plus the offset on N5584's rows (same eps_s): the offset makes criterion S select N5584 more often."""
    out, sims = base
    nC = sum(1 for d in sims["C"]["dropped"] if d == COL)
    nO = sum(1 for d in sims["O"]["dropped"] if d == COL)
    assert nO > nC and out["models"]["O"]["selected"]["n_host"] == nO


# ---------------------------------------------------------------- D and J from known inputs
def test_quadrant_counts_and_j_known_inputs():
    ref = np.array([[1.0, 0.0], [2.0, 1.0], [0.5, 0.5], [1.0, 1.0]])
    pts = np.array([[1.0, 1.0], [0.0, 2.0], [3.0, 0.0], [1.0, 0.0]])
    # quadrant: ref0 >= x0 and ref1 <= x1 (ties inside)
    assert list(onehost.quadrant_counts(pts, ref)) == [3, 4, 0, 1]
    # J: s even -> A, s odd -> B
    pairs = np.array([[1.0, 0.0], [1.0, 1.0], [2.0, 1.0], [0.0, 2.0], [0.5, 0.5], [3.0, 0.0], [1.0, 1.0], [1.0, 0.0]])
    js = onehost.j_stat(pairs, [1.0, 0.5])
    # A = [1,0], [2,1], [0.5,0.5], [1,1]; B = [1,1], [0,2], [3,0], [1,0]
    assert list(js["counts_b"]) == [3, 4, 0, 1]
    assert js["count_obs"] == 1                       # only [1, 0] has ref0 >= 1 and ref1 <= 0.5
    assert js["k"] == 2 and (js["n_A"], js["n_B"]) == (4, 4)   # counts 0 and 1 are <= 1 (ties counted)
    assert onehost.d_stat([0.1, 0.2, 0.3, 0.2], 0.2) == (3, 4)   # ties counted
    # a chunked count equals the direct one
    rng = np.random.default_rng(0)
    p, r = rng.normal(size=(1203, 2)), rng.normal(size=(777, 2))
    direct = np.array([np.sum((r[:, 0] >= x[0]) & (r[:, 1] <= x[1])) for x in p])
    assert np.array_equal(onehost.quadrant_counts(p, r, chunk=100), direct)


def test_j_calibration_toys():
    """The addendum's calibration check: bivariate-normal toys (correlation 0 and 0.8, fixed seed), 2,000 toy
    replicates of 2,000 simulations each (plus one observed draw from the same model). The share of replicates
    with calibrated p_J <= 0.05 does not exceed the upper end of the 99% Clopper-Pearson interval of 0.05
    (100 of 2,000): a valid test may be conservative (amendment 2026-11-21: one-sided, ties are counted
    towards larger p); at correlation 0.8 the raw quadrant probability's share lies above it."""
    n_rep, n_sim = 2000, 2000
    lo, hi = rob._cp(100, n_rep, level=0.99)
    res = {}
    for rho in (0.0, 0.8):
        rng = np.random.default_rng(48)
        cov = np.array([[1.0, rho], [rho, 1.0]])
        Lc = np.linalg.cholesky(cov)
        pj, praw = np.empty(n_rep), np.empty(n_rep)
        for r in range(n_rep):
            z = rng.standard_normal((n_sim + 1, 2)) @ Lc.T
            sims, obs = z[:n_sim], z[n_sim]
            js = onehost.j_stat(sims, obs)
            pj[r] = (1 + js["k"]) / (1 + js["n_B"])
            praw[r] = np.mean((sims[:, 0] >= obs[0]) & (sims[:, 1] <= obs[1]))
        res[rho] = (float(np.mean(pj <= 0.05)), float(np.mean(praw <= 0.05)), float(np.mean(pj <= 0.5)))
    for rho, (sj, _, half) in res.items():
        assert sj <= hi, (rho, sj, lo, hi)            # one-sided (amendment 2026-11-21): a valid test may be conservative
        assert sj >= 0.02, (rho, sj)                  # lower guard: a J that always returns large p fails
        assert 0.45 <= half <= 0.55, (rho, half)
    assert not (lo <= res[0.8][1] <= hi), res
    assert res[0.8][1] > hi                       # the raw quadrant probability is anti-conservative


# ---------------------------------------------------------------- labels and reading (pure)
def _m(dl, jl):
    return {"status": "evaluated", "D": {"label": f"{dl} (D)"}, "J": {"label": f"{jl} (J)"}}


E_, N_, U_ = "excluded", "not excluded", "undetermined (Monte Carlo)"


def _mods(v, o):
    """v: three (D, J) pairs for V050, V077, V105; o: (D, J) for O."""
    m = {"C": _m(E_, N_)}
    for k, (d, j) in zip(("V050", "V077", "V105"), v):
        m[k] = {"status": "evaluated", "D": {"label": d if d == U_ else f"{d} (D)"},
                "J": {"label": j if j == U_ else f"{j} (J)"}}
    d, j = o
    m["O"] = {"status": "evaluated", "D": {"label": d if d == U_ else f"{d} (D)"},
              "J": {"label": j if j == U_ else f"{j} (J)"}}
    return m


def test_labels_three_way():
    assert onehost.stat_label(5, 5000, "J")[0] == "excluded (J)"
    assert onehost.stat_label(2000, 10000, "D")[0] == "not excluded (D)"
    assert onehost.stat_label(500, 10000, "D")[0] == "undetermined (Monte Carlo)"
    assert onehost.vkey(0.05) == "V050" and onehost.vkey(0.077) == "V077" and onehost.vkey(0.105) == "V105"


def test_reading_rules_order_and_qualifiers():
    R = lambda v, o: onehost.reading(_mods(v, o), TAUS)
    one = "the three tested diffuse models V(0.05), V(0.077), V(0.105) excluded by J; one offset host not excluded "
    # (2) both statistics / joint statistic only (list of tau not excluded by D)
    assert R([(E_, E_)] * 3, (N_, N_)) == one + "(both statistics)"
    assert R([(E_, E_), (N_, E_), (U_, E_)], (N_, N_)) == one + "(joint statistic only; D does not exclude τ = 0.077, 0.105)"
    # (3) any V not excluded by J, regardless of O
    assert R([(E_, E_), (E_, N_), (E_, N_)], (E_, E_)) == "tested diffuse model(s) not excluded (τ = 0.077, 0.105)"
    assert R([(E_, N_), (E_, U_), (E_, E_)], (N_, N_)) == "tested diffuse model(s) not excluded (τ = 0.05)"
    # (4) every V excluded by J, O excluded by J or by D
    neither = "neither one offset host nor diffuse scatter reproduces the observed spreads"
    assert R([(E_, E_)] * 3, (N_, E_)) == neither
    assert R([(E_, E_)] * 3, (E_, N_)) == neither
    assert R([(E_, E_)] * 3, (E_, U_)) == neither
    # (5) otherwise
    assert R([(E_, E_), (E_, U_), (E_, E_)], (N_, N_)) == "undetermined"
    assert R([(E_, E_)] * 3, (U_, N_)) == "undetermined"
    assert R([(E_, E_)] * 3, (N_, U_)) == "undetermined"
    # (1) a decisive model not evaluable comes first, even with labels that would give (3)
    m = _mods([(E_, N_)] * 3, (N_, N_))
    m["V105"] = {"status": "not evaluable (Cholesky factor failed: x)"}
    assert onehost.reading(m, TAUS) == "not evaluable"
    m = _mods([(E_, E_)] * 3, (N_, N_))
    del m["O"]
    assert onehost.reading(m, TAUS) == "not evaluable"
    # C and the reported variants enter no rule
    m = _mods([(E_, E_)] * 3, (N_, N_))
    m["C"] = {"status": "not evaluable (x)"}
    m["OVN"] = {"status": "not run (x)"}
    assert onehost.reading(m, TAUS) == one + "(both statistics)"


def test_section5_actions():
    one = "the three tested diffuse models V(0.05), V(0.077), V(0.105) excluded by J; one offset host not excluded "
    a = onehost.section5_action(one + "(both statistics)")
    assert a.startswith("the R2-RE-SEL post-hoc bullet") and "joint statistic only" not in a
    b = onehost.section5_action(one + "(joint statistic only; D does not exclude τ = 0.105)")
    assert b.endswith(", and 'joint statistic only'")
    assert onehost.section5_action("tested diffuse model(s) not excluded (τ = 0.105)") == onehost.SECTION5["diffuse"]
    assert onehost.section5_action(onehost.READ_NEITHER) == onehost.SECTION5["neither"]
    assert onehost.section5_action("undetermined") == onehost.SECTION5["stays"]
    assert onehost.section5_action("not evaluable") == onehost.SECTION5["stays"]


def test_observed_value_tolerances():
    rec = {"spread_37": 1.3, "spread_36": 1.0, "crit_s": 1.027, "delta_hat": 0.33634}
    ob = {"spread_37": 1.3 * (1 + 9e-10), "spread_36": 1.0 * (1 - 9e-10), "delta_hat": 0.33634 - 4.9e-6,
          "crit_s_selects_host": True, "crit_s_selected": "N5584", "host": "N5584", "crit_s_host_value": 1.0279}
    assert onehost.observed_mismatches(ob, rec) == []
    for key, val in (("spread_37", 1.3 * (1 + 2e-9)), ("spread_36", 1.0 * (1 + 2e-9)),
                     ("delta_hat", 0.33634 + 5.1e-6), ("delta_hat", 0.33634 - 5.1e-6),
                     ("crit_s_host_value", 1.0281)):
        assert len(onehost.observed_mismatches(dict(ob, **{key: val}), rec)) == 1, key
    assert len(onehost.observed_mismatches(dict(ob, crit_s_selects_host=False, crit_s_selected="H01"), rec)) == 1


# ---------------------------------------------------------------- the block, end to end
def test_block_end_to_end(lad, base, tmp_path, monkeypatch):
    out, sims = base
    P = lad["P"]
    assert out["status"] == "evaluated"
    assert out["model_keys"] == ["C", "V050", "V077", "V105", "O", "Olo", "OVN", "Oany"]
    for k in out["model_keys"]:
        m = out["models"][k]
        assert m["status"] == "evaluated", (k, m["status"])
        assert m["D"]["n"] == 40 and m["J"]["n_B"] == 20 and m["J"]["n_A"] == 20
        assert m["D"]["label"] == onehost.stat_label(m["D"]["k"], 40, "D")[0]
        assert m["J"]["label"] == onehost.stat_label(m["J"]["k"], 20, "J")[0]
        assert len(sims[k]["pairs"]) == 40 and len(sims[k]["half_b_counts"]) == 20
    assert out["models"]["OVN"]["tau"] == lad["recorded"]["tau_n"]
    assert abs(out["models"]["Olo"]["delta"] - (out["observed"]["delta_hat"] - out["observed"]["sigma_delta"])) < 1e-15
    assert out["reading"] == onehost.reading(out["models"], TAUS)
    assert out["section5"] == onehost.section5_action(out["reading"])
    for k in ("O_over_V050", "O_over_V077", "O_over_V105", "O_over_C"):
        assert set(out["kde"][k]) == {"2d", "1d_D"} and out["kde"][k]["2d"]["n_boot"] == 5
    assert out["dropped_hosts_built"]["n_distinct"] == len({d for k in sims for d in sims[k]["dropped"]} | {COL})
    s = onehost.summary(out)
    assert s["reading"] == out["reading"] and set(s["models"]) == set(out["model_keys"])
    # the conclusion test re-derives every label from the saved files
    from astrolab.results import write_json
    write_json(tmp_path / "r2_re_d.json", out)
    for k, v in sims.items():
        write_json(tmp_path / f"r2_re_d_sims_{k}.json", v)
    write_json(tmp_path / "summary.json", {"R2_RE_D": s})
    tc = _load("tc003_d", "test_conclusions.py")
    monkeypatch.setattr(tc, "RESULTS", tmp_path)
    rc = lad["recorded"]
    monkeypatch.setattr(tc, "D_RECORDED", {k: rc[k] for k in ("spread_37", "spread_36", "crit_s", "delta_hat")})
    tc.test_r2_re_d_labels()
    # a tampered count or label is caught
    bad = json.loads((tmp_path / "r2_re_d_sims_V077.json").read_text(encoding="utf-8"))
    bad["count_obs"] += 3
    write_json(tmp_path / "r2_re_d_sims_V077.json", bad)
    with pytest.raises(AssertionError):
        tc.test_r2_re_d_labels()


def test_tau_n_from_the_same_run_and_not_reproduced(lad):
    out, sims = _block(lad, P=_small(lad), tau_n=lad["recorded"]["tau_n"])
    assert out["tau_hat_N"]["source"].startswith("R2-RE-N5584") and out["models"]["OVN"]["status"] == "evaluated"
    out, sims = _block(lad, P=_small(lad), recorded={"tau_n": lad["recorded"]["tau_n"] * (1 + 2e-6)})
    assert out["models"]["OVN"]["status"].startswith("not run (τ̂_N")
    assert sims["OVN"]["status"] == out["models"]["OVN"]["status"]
    assert out["status"] == "evaluated" and out["models"]["O"]["status"] == "evaluated"
    assert out["reading"] == onehost.reading(out["models"], TAUS)


# ---------------------------------------------------------------- not-evaluable rules
@pytest.mark.parametrize("key,factor,shift", [("spread_37", 1 + 2e-9, 0.0), ("spread_36", 1 - 2e-9, 0.0),
                                               ("delta_hat", 1.0, 6e-6)])
def test_observed_mismatch_stops_the_block(lad, key, factor, shift):
    out, sims = _block(lad, P=_small(lad), recorded={key: lad["recorded"][key] * factor + shift})
    assert out["status"] == onehost.BLOCK_NE_OBSERVED and out["reading"] == "not evaluable"
    assert "models" not in out and all(v["status"] == onehost.BLOCK_NE_OBSERVED for v in sims.values())
    assert len(out["observed"]["mismatches"]) == 1


def test_criterion_s_reproduction_and_selection(lad, monkeypatch):
    out, _ = _block(lad, P=_small(lad), recorded={"crit_s": lad["recorded"]["crit_s"] + 0.0011})
    assert out["status"] == onehost.BLOCK_NE_OBSERVED
    out, _ = _block(lad, P=_small(lad), recorded={"crit_s": lad["recorded"]["crit_s"] + 0.0009})
    assert out["status"] == "evaluated"
    calls = []
    real = sel.pick_min

    def first_wrong(v):
        calls.append(1)
        return 1 if len(calls) == 1 else real(v)
    monkeypatch.setattr(sel, "pick_min", first_wrong)
    out, _ = _block(lad, P=_small(lad))
    assert out["status"] == onehost.BLOCK_NE_OBSERVED
    assert "criterion S selects H01, not N5584" in out["observed"]["mismatches"]


def test_empty_index_stream(lad):
    out, sims = _block(lad, P=_small(lad), picks=[])
    assert out["status"] == "not evaluable (empty index stream: R4 has no draws)" and out["reading"] == "not evaluable"
    assert set(sims) == set(onehost.model_keys(TAUS))


def test_short_index_stream_is_not_truncated(lad):
    out, sims = _block(lad, P=_small(lad), picks=lad["picks"][:N_SUB - 1])
    assert out["status"] == "not evaluable (index stream shorter than rob_n_subsets)"
    assert out["reading"] == "not evaluable" and "models" not in out
    assert all(v["status"] == out["status"] for v in sims.values())


def test_fit_failure_building_the_37_host_rows_or_the_host_rows(lad):
    real = lad["run"].fit
    n = [0]

    def fit_37(L, y, C, rows, est=False):
        if L.shape[1] == lad["run"].N_PAR and len(rows) < len(lad["rows_a"]) and est and n[0] == 0:
            n[0] += 1
            raise ValueError("L^T C^-1 L is rank deficient (forced)")
        return real(L, y, C, rows, est=est)
    out, _ = _block(lad, P=_small(lad), fns=dict(lad["fns"], fit=fit_37))
    assert out["status"].startswith("not evaluable (fit: building the 37-host shift rows")
    rows_n = lad["red"]["rows_n"]

    def fit_host(L, y, C, rows, est=False):
        if np.array_equal(np.asarray(rows), rows_n):
            raise ValueError("C is not positive definite: forced")
        return real(L, y, C, rows, est=est)
    out, _ = _block(lad, P=_small(lad), fns=dict(lad["fns"], fit=fit_host))
    assert out["status"].startswith("not evaluable (fit: building the rows of the reduced system without N5584")
    assert out["reading"] == "not evaluable"


def test_cholesky_failure_makes_that_model_not_evaluable(lad):
    real = lad["run"].with_re

    def with_re(C, groups, tau):
        V = real(C, groups, tau)
        if abs(tau - 0.105) < 1e-12:
            V = V.copy()
            V[0, 0] = -1.0
        return V
    out, sims = _block(lad, P=_small(lad), fns=dict(lad["fns"], with_re=with_re))
    assert out["models"]["V105"]["status"].startswith("not evaluable (Cholesky factor failed")
    assert sims["V105"]["status"] == out["models"]["V105"]["status"]
    for k in ("C", "V050", "V077", "O", "Olo", "OVN", "Oany"):
        assert out["models"][k]["status"] == "evaluated"
    assert out["reading"] == "not evaluable"
    assert out["status"] == "not evaluable (a decisive model is not evaluable)"    # block status follows rule (1)


def test_fit_failure_for_another_dropped_host(lad, base):
    _, sims = base
    ds = {k: sims[k]["dropped"][:6] for k in sims}
    cands = sorted({d for k in ds for d in ds[k] if d != COL})
    if not cands:
        pytest.skip("no simulation drops another host in the first 6")
    d = cands[0]
    rows_n = sel.reduced_system(lad["nz"], lad["rows_a"], d, lad["groups"], lad["host_rows"])["rows_n"]
    real = lad["run"].fit

    def fit(L, y, C, rows, est=False):
        if np.array_equal(np.asarray(rows), rows_n):
            raise ValueError("C is not positive definite: forced")
        return real(L, y, C, rows, est=est)
    out, _ = _block(lad, P=_small(lad), fns=dict(lad["fns"], fit=fit))
    for k, dl in ds.items():
        st = out["models"][k]["status"]
        if d in dl:
            assert st == f"not evaluable (fit: building the rows for dropped host {lad['labels'][d]})", k
        else:
            assert st == "evaluated", k
    assert lad["labels"][d] in out["dropped_hosts_built"]["failed"]
    dec_hit = any(d in ds[k] for k in ("V050", "V077", "V105", "O"))
    assert (out["reading"] == "not evaluable") == dec_hit


def test_wrong_column_is_refused(lad):
    with pytest.raises(RuntimeError):
        _block(lad, P=_small(lad), expected_col=25)


# ---------------------------------------------------------------- the standalone summary update
def test_summary_update_keeps_other_keys_byte_identical():
    from astrolab.results import to_jsonable
    dump = lambda o: json.dumps(to_jsonable(o), indent=1, ensure_ascii=False)
    old = {"params": {"a": [1, 2.5]}, "R2_RE_SEL": {"reading": "τ excess"}, "x": 0.1 + 0.2, "runtime_s": 3.25}
    text = dump(old)
    new = onehost.summary_with_key(text, "R2_RE_D", {"status": "evaluated"})
    assert list(new) == ["params", "R2_RE_SEL", "x", "R2_RE_D", "runtime_s"]
    new_text = dump(new)
    for k in old:
        assert dump(new[k]) == dump(old[k])
    # removing the new key's lines gives back the old file exactly
    back = dict(new)
    del back["R2_RE_D"]
    assert dump(back) == text
    # an existing key is replaced in place
    again = onehost.summary_with_key(new_text, "R2_RE_D", {"status": "x"})
    assert list(again) == list(new) and again["R2_RE_D"] == {"status": "x"}
    # a file that does not re-serialise to itself is refused
    with pytest.raises(RuntimeError):
        onehost.summary_with_key(text.replace("\n", "\r\n"), "R2_RE_D", {})
    with pytest.raises(RuntimeError):
        onehost.summary_with_key(json.dumps(old), "R2_RE_D", {})


# ---------------------------------------------------------------- run.main in the standalone mode
class _Ctx:
    """A stand-in for astrolab's Context: results folder, record_suffix, save into memory, log."""
    max_save_bytes = None

    def __init__(self, results):
        self.results = results
        self.record_suffix = ""
        self.saved = {}

    def save(self, name, obj):
        self.saved[name] = obj

    def log(self, msg):
        pass


def _main_d(tmp_path, monkeypatch, name, stub=None, summary=True):
    run = _load(name, "run.py")
    tn = _load("tn003_" + name, "test_n5584.py")
    L, y, C = tn._synthetic(run, tau=TAU, outlier=OUTLIER)
    # an LMC row and two Milky Way rows, as anchor_rows expects; then the shapes run.main checks
    for c, val in ((run.C_LMC, 0.0), (run.C_MH, -5.85), (run.C_MH, -5.80)):
        r = np.zeros(run.N_PAR)
        r[c] = 1.0
        L = np.vstack([L, r])
        y = np.append(y, val)
        C = np.pad(C, ((0, 1), (0, 1)))
        C[-1, -1] = 0.03 ** 2
    monkeypatch.setattr(run, "N_ROWS", len(y))
    monkeypatch.setattr(run, "load", lambda ctx: (C, L, y, np.zeros((run.N_PAR, 2))))
    monkeypatch.setitem(run.PARAMS, "d_only", True)
    if stub is not None:
        monkeypatch.setattr(run, "run_d", stub)
    from astrolab.results import write_json
    old = {"params": {"a": 1}, "R2_RE_SEL": {"reading": "τ̂ x"}, "runtime_s": 1.5}
    if summary:
        write_json(tmp_path / "summary.json", old)
    ctx = _Ctx(tmp_path)
    return run, ctx, old


def test_main_d_only_refuses_without_summary(tmp_path, monkeypatch):
    run, ctx, _ = _main_d(tmp_path, monkeypatch, "run003_donly_a", summary=False)
    with pytest.raises(RuntimeError, match="run the full study first"):
        run.main(ctx)
    assert ctx.saved == {} and ctx.record_suffix == "_d"


def test_main_d_only_writes_only_its_files(tmp_path, monkeypatch):
    """d_only: provenance_d / run_info_d suffix, r2_re_d.json, the eight sims files and summary.json with only
    R2_RE_D added; nothing else saved (r1 and host_identification computed but not saved)."""
    keys = onehost.model_keys(TAUS)
    seen = {}

    def stub(ctx, P, L, y, C, nz, cls, rows_a, col_host, ident, n_pick, picks=None, tau_n=None,
             rob_spread_obs=None):
        seen.update(n_pick=n_pick, picks=picks, tau_n=tau_n, n_rows=len(rows_a), n=len(y))
        out = {"status": "evaluated", "reading": "undetermined", "models": {k: {"status": "not run (stub)"} for k in keys}}
        return out, {k: {"model": k, "status": "not run (stub)"} for k in keys}
    run, ctx, old = _main_d(tmp_path, monkeypatch, "run003_donly_b", stub=stub)
    ret = run.main(ctx)
    assert ctx.record_suffix == "_d"
    assert set(ctx.saved) == {"r2_re_d", "summary"} | {f"r2_re_d_sims_{k}" for k in keys}
    assert seen["picks"] is None and seen["tau_n"] is None and seen["n_rows"] == seen["n"] - 3
    s = ctx.saved["summary"]
    assert list(s) == ["params", "R2_RE_SEL", "R2_RE_D", "runtime_s"] and ret == s
    assert all(s[k] == old[k] for k in old)
    assert s["R2_RE_D"] == onehost.summary(ctx.saved["r2_re_d"])


def test_main_d_only_real_wiring(tmp_path, monkeypatch):
    """Without the stub: the synthetic columns do not match R22's hosts, so the host step is not evaluable and
    the block is recorded as such; still only the R2-RE-D files and summary.json are saved."""
    run, ctx, old = _main_d(tmp_path, monkeypatch, "run003_donly_c")
    run.main(ctx)
    keys = onehost.model_keys(TAUS)
    assert set(ctx.saved) == {"r2_re_d", "summary"} | {f"r2_re_d_sims_{k}" for k in keys}
    assert ctx.saved["r2_re_d"]["status"] == "not evaluable (host step not evaluable)"
    assert ctx.saved["summary"]["R2_RE_D"]["reading"] == "not evaluable"
