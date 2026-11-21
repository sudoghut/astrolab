"""Offline tests of R2-RE-G (README section 2, addendum 2026-11-21, T-055) on synthetic data only: z = W y against
one-column GLS fits, Cov(u) = M + tau^2 M^2, the reduced REML form against R2-RE's reml_m2l and reml_tau, the exact
inner draws and their fixed matrix, G and its argmax, the offset only on the chosen host's rows and its
sigma-matching, common eps_s, the size of the bootstrap test at a known tau, a rank-deficient and a singular system,
the rules (1)-(5) and the sub-label, every not-evaluable condition, the runtime guard, the two-stage count
reproduction, the power stage's outputs and log free of G_obs / sum z^2 / other hosts' z_j, the standalone mode, and
the label re-derivation from the saved files (test_conclusions.check_r2_re_g)."""
import importlib.util
import json
import re
import sys
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import onehost  # noqa: E402
import rob  # noqa: E402
import shape  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


COL = 26
TAU, OUTLIER = 0.05, 0.8
N_SIMS = 40
TAUS_REP = [0.05, 0.105]
Z_CURVE = [2.5, 3.0, 4.0, 4.5, 5.0]
SIM_KEYS = ["VHAT", "V050", "V105", "C", "OANY", "OANYLO", "OANYVN", "O"]
GRID = np.round(np.arange(0.0, 0.5 + 0.005, 0.01), 10)


def _system(run, tau=TAU, outlier=OUTLIER, seed=3, pin_mb=False, no_ceph_host=None):
    tn = _load(f"tn003_g_{seed}_{pin_mb}_{no_ceph_host}", "test_n5584.py")
    L, y, C = tn._synthetic(run, tau=tau, outlier=outlier, seed=seed)
    if pin_mb:                       # one external row on M0_B: the 37 offsets become jointly estimable
        r = np.zeros(run.N_PAR)
        r[run.C_MB] = 1.0
        L, y = np.vstack([L, r]), np.append(y, -19.25)
        C = np.pad(C, ((0, 1), (0, 1)))
        C[-1, -1] = 0.02 ** 2
    if no_ceph_host is not None:     # host j's distance only on its SN rows: its offset is not identifiable
        keep = ~((L[:, no_ceph_host] != 0) & (L[:, run.C_MB] == 0))
        L, y, C = L[keep], y[keep], C[np.ix_(keep, keep)]
    return L, y, C


def _fns(run):
    return {"reml_tau": run.reml_tau, "reml_m2l": run.reml_m2l, "fit": run.fit, "with_re": run.with_re,
            "is_fit_failure": run.is_fit_failure}


def _build(name, **kw):
    run = _load(name, "run.py")
    L, y, C = _system(run, **kw)
    run.N_ROWS = len(y)
    nz, cls, _ = run.row_classes(L, y)
    groups = [np.flatnonzero(cls["calib"] & nz[:, j]) for j in range(run.NH)]
    labels = [f"H{j:02d}" for j in range(run.NH)]
    labels[COL] = "N5584"
    rows_a = np.arange(len(y))
    fns = _fns(run)
    grid = [run.reml_m2l(L, y, C, rows_a, groups, t) for t in GRID]
    est = run.reml_tau(lambda t: run.reml_m2l(L, y, C, rows_a, groups, t), 0.5, 0.01, interval=False)
    d, s = onehost.fit_delta(L, y, C, rows_a, groups[COL], fns)
    rec = {"tau_obs": est["tau_hat"], "delta_hat": d, "sigma_delta": s, "z_obs": d / s, "tau_n": 0.0314}
    P = dict(run.PARAMS, g_n_sims=N_SIMS, g_check=True)
    return dict(run=run, L=L, y=y, C=C, nz=nz, cls=cls, groups=groups, labels=labels, rows_a=rows_a, fns=fns,
                grid=grid, rec=rec, P=P)


@pytest.fixture(scope="module")
def lad():
    return _build("run003_g")


def _stage(lad, stage, P=None, fns=None, power_rec=None, recorded=None, log=None, grid=None):
    rc = dict(lad["rec"])
    rc.update(recorded or {})
    return shape.run_stage(stage, lad["L"], lad["y"], lad["C"], lad["rows_a"], lad["groups"], lad["labels"],
                           lad["P"] if P is None else P, lad["fns"] if fns is None else fns,
                           (lambda m: None) if log is None else log, lad["grid"] if grid is None else grid,
                           power_rec=power_rec, expected_col=COL, recorded=rc)


@pytest.fixture(scope="module")
def stages(lad):
    logs = []
    p_out, none = _stage(lad, "power", log=logs.append)
    assert none is None
    p_json = json.loads(json.dumps(_jsonable(p_out)))
    g_out, sims = _stage(lad, "full", power_rec=p_json)
    return dict(power=p_out, power_json=p_json, power_log=logs, full=g_out, sims=sims)


def _jsonable(o):
    from astrolab.results import to_jsonable
    return to_jsonable(o)


def _des(lad):
    des, problem = shape.design(lad["L"], lad["y"], lad["C"], lad["rows_a"], lad["groups"], lad["fns"])
    assert problem is None
    return des


# ---------------------------------------------------------------- settings and names
def test_params_and_constants():
    run = _load("run003_g_params", "run.py")
    P = run.PARAMS
    assert (P["g_check"], P["g_seed_base"], P["g_host_seed_base"], P["g_inner_seed"], P["g_n_sims"], P["g_n_inner"],
            P["g_power_min"], P["g_z_curve"], P["g_taus_rep"], P["g_max_minutes"], P["g_min_sims"], P["g_only"],
            P["g_stage"]) == (False, 400_000, 500_000, 600_000, 10_000, 20_000, 0.8, Z_CURVE, TAUS_REP, 120, 5_000,
                              False, "full")
    assert shape.RECORDED_TAU_OBS == 0.07669875579792439 and shape.TAU_OBS_ATOL == 2e-5
    assert (shape.RECORDED_DELTA, shape.DELTA_ATOL) == (0.33634, 5e-6)
    assert (shape.RECORDED_SIGMA_DELTA, shape.RECORDED_Z_OBS, shape.REL_TOL) == (0.09251604267299487,
                                                                                3.6354437025541553, 1e-6)
    assert shape.RECORDED_TAU_N == 0.03137144323410943 and shape.GRID_ATOL == 1e-5 and shape.Z_ATOL == 1e-8
    assert (shape.EIG_RTOL, shape.N_POINTWISE, shape.TIME_SIMS, shape.TIE_G) == (1e-10, 3, 1000, 1e-5)
    assert shape.sim_keys(TAUS_REP) == SIM_KEYS
    assert shape.set_keys(TAUS_REP, Z_CURVE) == SIM_KEYS + ["Z250", "Z300", "Z400", "Z450", "Z500"]
    tc = _load("tc003_g_consts", "test_conclusions.py")
    assert tc.G_TIE == shape.TIE_G
    # the recorded values agree with the saved R2-RE and R2-RE-D results (when present)
    res = HERE / "results"
    if (res / "r2_re.json").exists():
        r2 = json.loads((res / "r2_re.json").read_text(encoding="utf-8"))
        assert r2["reml"]["tau_hat"] == shape.RECORDED_TAU_OBS and len(r2["reml"]["grid_m2l"]) == 51
    if (res / "r2_re_d.json").exists():
        ob = json.loads((res / "r2_re_d.json").read_text(encoding="utf-8"))["observed"]
        assert abs(ob["sigma_delta"] - shape.RECORDED_SIGMA_DELTA) <= 1e-6 * shape.RECORDED_SIGMA_DELTA
        assert abs(ob["delta_over_sigma"] - shape.RECORDED_Z_OBS) <= 1e-6 * shape.RECORDED_Z_OBS
        assert abs(ob["delta_hat"] - shape.RECORDED_DELTA) <= shape.DELTA_ATOL
    # seeds collide with no earlier block (R4 0, ROB 10,000-11,999, SEL 20,000-21,999, referee 50,000-50,999,
    # R2-RE-D 100,000-109,999 and 200,000-209,999, its KDE 300,000-300,199)
    used = [(0, 0), (10_000, 11_999), (20_000, 21_999), (50_000, 50_999), (100_000, 109_999), (200_000, 209_999),
            (300_000, 300_199)]
    for lo, hi in [(400_000, 409_999), (500_000, 509_999), (600_000, 600_000)]:
        assert all(hi < a or lo > b for a, b in used)


# ---------------------------------------------------------------- identities
def test_z_is_the_one_column_t_statistic(lad):
    """z = W y equals delta_hat_j / sigma_delta_j of the one-extra-column GLS fit for every host; W X = 0;
    sigma_delta_j = M_jj^-1/2."""
    des = _des(lad)
    z = des["W"] @ lad["y"][lad["rows_a"]]
    d, s = shape.one_column_z(lad["L"], lad["y"], lad["C"], lad["rows_a"], lad["groups"], lad["fns"])
    assert np.max(np.abs(z - d / s)) < 1e-9
    assert np.max(np.abs(des["dinv"] - s)) < 1e-12 * 1e3
    assert np.max(np.abs(des["W"] @ des["X"])) < 1e-9
    assert np.max(np.abs(des["W"] @ des["yhat"])) < 1e-9
    assert abs(z[COL] - lad["rec"]["z_obs"]) < 1e-9
    u = des["PZt"] @ lad["y"][lad["rows_a"]]                 # u = Z^T P y (the power stage's route to v)
    assert np.max(np.abs(u - z * des["sqrt_m"])) < 1e-9 * np.max(np.abs(u))


def _P_explicit(lad, des):
    Ca = lad["C"][np.ix_(lad["rows_a"], lad["rows_a"])]
    Ci = np.linalg.inv(Ca)
    X = des["X"]
    return Ci - Ci @ X @ np.linalg.solve(X.T @ Ci @ X, X.T @ Ci)


def _Zm(des):
    Zm = np.zeros((des["n_a"], des["n_hosts"]))
    for j, p in enumerate(des["gpos"]):
        Zm[p, j] = 1.0
    return Zm


@pytest.mark.parametrize("tau", [0.0, 0.07, 0.2])
def test_cov_u_is_m_plus_tau2_m2(lad, tau):
    des = _des(lad)
    P_ = _P_explicit(lad, des)
    Zm = _Zm(des)
    V = lad["run"].with_re(lad["C"], lad["groups"], tau)[np.ix_(lad["rows_a"], lad["rows_a"])]
    cov = Zm.T @ P_ @ V @ P_ @ Zm
    M = des["M"]
    assert np.max(np.abs(cov - (M + tau * tau * M @ M))) < 1e-8 * np.max(np.abs(M))
    assert np.max(np.abs(Zm.T @ P_ @ Zm - M)) < 1e-8 * np.max(np.abs(M))
    # the exact inner draws: A A^T = D (M + tau^2 M^2) D (clipped spectrum)
    A = shape.inner_matrix(tau, des)
    D = np.diag(des["dinv"])
    assert np.max(np.abs(A @ A.T - D @ (M + tau * tau * M @ M) @ D)) < 1e-8


def test_reduced_reml_equals_reml_m2l_differences(lad):
    """f(tau; u) = -2 l_R(tau) - (-2 l_R(0)) on the whole grid, and the refitted tau_hat equals reml_tau on
    reml_m2l."""
    des = _des(lad)
    v = shape.v_of_z(des["W"] @ lad["y"][lad["rows_a"]], des)
    f = np.array([shape.reml_f(t, v, des["lam"]) for t in GRID])
    g = np.array(lad["grid"])
    assert np.max(np.abs(f - (g - g[0]))) < 1e-8
    est = shape.tau_refit(v, des["lam"], lad["run"].reml_tau)
    assert abs(est["tau_hat"] - lad["rec"]["tau_obs"]) < 2e-5


def _sim_one(lad, des, spec, tau_cov, s):
    """One simulated data vector built in full: y_s on rows_a."""
    from scipy import linalg
    V = lad["run"].with_re(lad["C"], lad["groups"], tau_cov)[np.ix_(lad["rows_a"], lad["rows_a"])]
    K = linalg.cholesky(V, lower=True)
    eps = onehost.eps_block(400_000, [s], des["n_a"])[:, 0]
    return K, eps


@pytest.mark.parametrize("seed,tau", [(5, 0.0), (6, 0.15)])
def test_reduced_reml_on_other_data(lad, seed, tau):
    des = _des(lad)
    rng = np.random.default_rng(seed)
    V = lad["run"].with_re(lad["C"], lad["groups"], tau)[np.ix_(lad["rows_a"], lad["rows_a"])]
    y = np.array(lad["y"], dtype=float)
    y[lad["rows_a"]] = des["yhat"] + np.linalg.cholesky(V) @ rng.standard_normal(des["n_a"])
    v = shape.v_of_z(des["W"] @ y[lad["rows_a"]], des)
    run = lad["run"]
    m0 = run.reml_m2l(lad["L"], y, lad["C"], lad["rows_a"], lad["groups"], 0.0)
    for t in (0.03, 0.1, 0.3):
        full = run.reml_m2l(lad["L"], y, lad["C"], lad["rows_a"], lad["groups"], t) - m0
        assert abs(shape.reml_f(t, v, des["lam"]) - full) < 1e-8
    a = shape.tau_refit(v, des["lam"], run.reml_tau)["tau_hat"]
    b = run.reml_tau(lambda t: run.reml_m2l(lad["L"], y, lad["C"], lad["rows_a"], lad["groups"], t), 0.5, 0.01,
                     interval=False)["tau_hat"]
    assert abs(a - b) < 2e-5


def test_rank_deficient_and_full_rank_systems():
    """The standard synthetic ladder is rank-deficient (the 37 offsets sum to the calibrator part of M0_B):
    rank M = 36, one eigenvalue clipped, and no G, tau_hat or p_boot is NaN; with M0_B pinned by an external row
    the rank is 37 and the identities hold."""
    for pin, rank in ((False, 36), (True, 37)):
        lad = _build(f"run003_g_rank_{pin}", pin_mb=pin)
        des = _des(lad)
        assert des["rank_M"] == rank and des["n_clipped"] == 37 - rank
        z = des["W"] @ lad["y"][lad["rows_a"]]
        d, s = shape.one_column_z(lad["L"], lad["y"], lad["C"], lad["rows_a"], lad["groups"], lad["fns"])
        assert np.max(np.abs(z - d / s)) < 1e-9
        E_in = shape.inner_draws(600_000, 2_000, 37)
        sp = shape.model_specs(TAUS_REP, Z_CURVE, 0.08, 0.03, 3.6, 0.3, COL)
        from scipy import linalg
        K = linalg.cholesky(lad["run"].with_re(lad["C"], lad["groups"], 0.08), lower=True)
        hosts = onehost.offset_hosts(500_000, 20, 37)
        for key in ("VHAT", "OANY", "O"):
            B = des["W"] @ (K if key == "VHAT" else des["Kc"])
            a = shape.simulate(sp[key], B, des, E_in, 400_000, 0, 20, hosts, lad["run"].reml_tau, 2_000)
            assert np.all(np.isfinite(a["G"])) and np.all(np.isfinite(a["tau"]))
            assert np.all((a["G"] >= 1 / 37 - 1e-12) & (a["G"] <= 1 + 1e-12))
            assert np.all(np.isfinite([shape.p_boot(k, 2_000) for k in a["k"]]))
        A = shape.inner_matrix(0.08, des)
        assert np.all(np.isfinite(A))


def test_singular_m_jj_is_rule_1():
    """A host whose distance is only on its SN rows has M_jj = 0: rule (1)."""
    lad = _build("run003_g_mjj", no_ceph_host=3)
    des, problem = shape.design(lad["L"], lad["y"], lad["C"], lad["rows_a"], lad["groups"], lad["fns"])
    assert des is None and problem.startswith("some M_jj ≤ 0")
    p, _ = _stage(lad, "power")
    assert p["status"].startswith("not evaluable (some M_jj ≤ 0")
    out, sims = _stage(lad, "full", power_rec=json.loads(json.dumps(_jsonable(p))))
    assert out["status"] == p["status"] and out["reading"] == out["status"]
    assert set(sims) == set(SIM_KEYS) and "G_obs" not in json.dumps(_jsonable(out))


# ---------------------------------------------------------------- G, inner draws, offsets, common numbers
def test_g_stat_and_ties():
    G, j = shape.g_stat(np.array([1.0, -3.0, 3.0, 0.5]))
    assert j == 1 and abs(G - 9 / (1 + 9 + 9 + 0.25)) < 1e-15
    G, j = shape.g_stat(np.array([[2.0, 1.0], [0.0, -1.0]]))
    assert list(j) == [0, 1] and np.allclose(G, [0.8, 1.0])


def test_inner_draws_fixed_and_distributed(lad):
    des = _des(lad)
    E = shape.inner_draws(600_000, 20_000, 37)
    assert np.array_equal(E, np.random.default_rng(600_000).standard_normal((20_000, 37)))
    assert shape.inner_k(0.3, 0.08, des, E) == shape.inner_k(0.3, 0.08, des, E)
    Zi = E @ shape.inner_matrix(0.08, des).T
    D = np.diag(des["dinv"])
    target = D @ (des["M"] + 0.0064 * des["M"] @ des["M"]) @ D
    assert np.max(np.abs(np.cov(Zi.T) - target)) < 0.04 * np.max(np.diag(target))
    # k counts G_i >= G exactly
    Z2 = Zi ** 2
    Gi = Z2.max(axis=1) / Z2.sum(axis=1)
    assert shape.inner_k(0.25, 0.08, des, E) == int(np.sum(Gi >= 0.25))


def test_offset_only_on_the_chosen_rows_and_sigma_matched(lad):
    des = _des(lad)
    sp = shape.model_specs(TAUS_REP, Z_CURVE, 0.08, 0.03, 3.6354, 0.33, COL)
    for k in (0, 7, COL):
        off = shape.offset_y(sp["OANY"], k, des)
        assert set(np.flatnonzero(off)) == set(des["gpos"][k])
        assert np.allclose(off[des["gpos"][k]], 3.6354 * des["dinv"][k])
        zo = shape.offset_z(sp["OANY"], k, des)
        assert np.max(np.abs(zo - des["W"] @ off)) < 1e-10
        assert abs(zo[k] - 3.6354) < 1e-10          # the offset host's expected z is z_alt, whatever sigma_k
    off = shape.offset_y(sp["O"], None, des)
    assert set(np.flatnonzero(off)) == set(des["gpos"][COL]) and np.allclose(off[des["gpos"][COL]], 0.33)
    assert np.max(np.abs(shape.offset_z(sp["O"], None, des) - des["W"] @ off)) < 1e-10
    assert np.all(shape.offset_z(sp["C"], None, des) == 0.0)


def test_common_eps_and_host_draws(lad):
    """OANY with z_alt = 0 reproduces C exactly (same eps_s); every OANY variant uses the same host draws."""
    des = _des(lad)
    E_in = shape.inner_draws(600_000, 2_000, 37)
    sp = shape.model_specs(TAUS_REP, Z_CURVE, 0.08, 0.03, 3.6, 0.3, COL)
    hosts = onehost.offset_hosts(500_000, 12, 37)
    assert list(hosts) == [int(np.random.default_rng(500_000 + s).integers(0, 37)) for s in range(12)]
    B = des["W"] @ des["Kc"]
    a = shape.simulate(sp["C"], B, des, E_in, 400_000, 0, 12, hosts, lad["run"].reml_tau, 2_000)
    b = shape.simulate(dict(sp["OANY"], z_alt=0.0), B, des, E_in, 400_000, 0, 12, hosts, lad["run"].reml_tau, 2_000)
    for k in ("G", "tau", "k", "j"):
        assert np.array_equal(a[k], b[k])
    # splitting the range changes only the last bits of B eps (BLAS blocking); the stages split it identically
    c = shape._cat([shape.simulate(sp["OANY"], B, des, E_in, 400_000, 0, 5, hosts, lad["run"].reml_tau, 2_000),
                    shape.simulate(sp["OANY"], B, des, E_in, 400_000, 5, 12, hosts, lad["run"].reml_tau, 2_000)])
    d = shape.simulate(sp["OANY"], B, des, E_in, 400_000, 0, 12, hosts, lad["run"].reml_tau, 2_000)
    assert np.allclose(c["G"], d["G"], rtol=1e-12, atol=0) and np.allclose(c["tau"], d["tau"], rtol=0, atol=1e-9)
    for k in ("k", "j"):
        assert np.array_equal(c[k], d[k])


def test_simulated_z_equals_full_build(lad):
    """z_s = B eps_s (+ offset) equals the 37 one-column fits on y_s built in full (OANY, s = 0..2)."""
    des = _des(lad)
    sp = shape.model_specs(TAUS_REP, Z_CURVE, 0.08, 0.03, 3.6, 0.3, COL)
    hosts = onehost.offset_hosts(500_000, 3, 37)
    B = des["W"] @ des["Kc"]
    for s in range(3):
        eps = onehost.eps_block(400_000, [s], des["n_a"])[:, 0]
        z = B @ eps + shape.offset_z(sp["OANY"], int(hosts[s]), des)
        y = np.array(lad["y"], dtype=float)
        y[lad["rows_a"]] = des["yhat"] + des["Kc"] @ eps + shape.offset_y(sp["OANY"], int(hosts[s]), des)
        d, sd = shape.one_column_z(lad["L"], y, lad["C"], lad["rows_a"], lad["groups"], lad["fns"])
        assert np.max(np.abs(d / sd - z)) < 1e-9


def test_size_at_a_known_tau(lad):
    """The whole procedure (tau refitted, bootstrap, label) under V(0.08) on the synthetic system: the rejection
    rate is not above the upper end of the 99% Clopper-Pearson interval of 0.05."""
    from scipy import linalg
    des = _des(lad)
    n = 400
    K = linalg.cholesky(lad["run"].with_re(lad["C"], lad["groups"], 0.08), lower=True)
    sp = shape.model_specs(TAUS_REP, Z_CURVE, 0.08, 0.03, 3.6, 0.3, COL)
    E_in = shape.inner_draws(600_000, 20_000, 37)
    a = shape.simulate(sp["VHAT"], des["W"] @ K, des, E_in, 400_000, 0, n, onehost.offset_hosts(500_000, n, 37),
                       lad["run"].reml_tau, 20_000)
    rej = sum(1 for k in a["k"] if shape.p_label(k, 20_000)[0] == shape.EXCL)
    hi99 = rob._cp(int(round(0.05 * n)), n, level=0.99)[1]
    assert rej / n <= hi99, rej
    assert np.all(np.isfinite(a["G"]))


# ---------------------------------------------------------------- rules
def test_reading_rules_order_and_sub_label():
    R = shape.reading
    assert R(["x"], 0.9, "excluded") == ("not evaluable (x)", None)
    assert R(["x", "y"], 0.9, "excluded") == ("not evaluable (x; y)", None)
    assert R([shape.RUNTIME], 0.9, "excluded") == ("not evaluated (runtime)", None)
    assert R(["anti-conservative at τ = 0.05"], 0.9, "excluded") == ("not evaluable (anti-conservative at τ = 0.05)",
                                                                    None)
    assert R([], 0.79, "excluded") == ("undetermined (underpowered)",
                                       "diffuse excluded; test underpowered against the σ-matched alternative")
    assert R([], 0.79, "not excluded") == ("undetermined (underpowered)", None)
    assert R([], 0.2, shape.UNDET_MC) == ("undetermined (underpowered)", None)
    assert R([], 0.8, "excluded") == ("one offset host preferred over diffuse scatter", None)   # 0.8 is powered
    assert R([], 0.95, "not excluded") == ("diffuse scatter not excluded", None)
    assert R([], 0.95, shape.UNDET_MC) == ("undetermined (Monte Carlo)", None)
    assert 8000 / 10000 >= 0.8
    assert shape.section5_action(shape.READ_PREFERRED) == shape.SECTION5["preferred"]
    assert shape.section5_action(shape.READ_NOT_EXCL) == shape.SECTION5["not_excluded"]
    for r in (shape.READ_UNDERPOWERED, shape.READ_UNDET_MC, "not evaluable (x)", shape.NE_RUNTIME):
        assert shape.section5_action(r) == shape.SECTION5["none"]


def test_three_way_label_of_one_data_vector():
    assert shape.p_label(0, 20_000)[0] == "excluded"
    assert shape.p_label(20_000, 20_000)[0] == "not excluded"
    assert shape.p_label(1000, 20_000)[0] == "undetermined (Monte Carlo)"
    assert shape.p_label(1000, 20_000) == rob.three_way(1000, 20_000, "excluded", "not excluded")
    assert shape.p_boot(0, 20_000) == 1 / 20_001


def test_anti_conservative_and_guard():
    m = lambda k, n, t: {"status": "evaluated", "tau": t, "ci95": list(rob._cp(k, n))}
    models = {"VHAT": m(700, 10_000, 0.0767), "V050": m(500, 10_000, 0.05), "V105": m(520, 10_000, 0.105)}
    assert shape.anti_conservative(models, TAUS_REP) == [0.0767]
    models["V105"] = m(600, 10_000, 0.105)
    assert shape.anti_conservative(models, TAUS_REP) == [0.0767, 0.105]
    assert shape.rule1_status(["anti-conservative at τ = " + ", ".join(shape.fmt_tau(t) for t in [0.0767, 0.105])]) \
        == "not evaluable (anti-conservative at τ = 0.0767, 0.105)"
    # runtime guard: 13 sets; fits, reduced to a multiple of 1,000, floor
    assert shape.guard_n(0.005, 10_000, 13, 120, 5_000) == (10_000, 0.005 * 10_000 * 13 / 60, False)
    n, proj, red = shape.guard_n(0.07, 10_000, 13, 120, 5_000)
    assert red and n == int(120 * 60 / (0.07 * 13)) // 1000 * 1000 == 7_000
    assert shape.guard_n(0.2, 10_000, 13, 120, 5_000)[0] is None


def test_smallest_curve_z():
    c = [{"z_alt": 2.5, "rate": 0.3}, {"z_alt": 3.0, "rate": 0.8}, {"z_alt": 4.0, "rate": 0.95}]
    assert shape.smallest_z(c, 0.8) == 3.0
    assert shape.smallest_z(c[:1], 0.8) is None


# ---------------------------------------------------------------- the block on the synthetic system
def test_power_and_full_stage(lad, stages):
    p, g, sims = stages["power"], stages["full"], stages["sims"]
    assert p["status"] == "evaluated" and p["stage"] == "power" and p["n_sims"] == N_SIMS
    assert p["design"]["rank_M"] == 36 and p["design"]["joint_rank"] == p["design"]["joint_columns"] - 1
    assert all(q["ok"] for q in p["checks"]["pointwise"]) and len(p["checks"]["pointwise"]) == 6
    assert p["checks"]["reproduction"]["mismatches"] == []
    assert set(p["models"]) == set(shape.set_keys(TAUS_REP, Z_CURVE))
    assert p["power"]["power"] == min(p["models"]["OANY"]["rate"], p["models"]["OANYVN"]["rate"])
    assert g["checks"]["power_stage_counts_reproduced"] and all(g["checks"]["power_stage_k_sha256_equal"].values())
    assert g["status"] == "evaluated" and g["observed"]["host_j_hat"] == "N5584"
    assert g["checks"]["real_W_y_vs_one_column_fits"]["ok"]
    jf = g["joint_fit"]
    assert jf["attempt"].startswith("not fitted") and jf["rank"] == jf["n_columns"] - 1
    assert set(sims) == set(SIM_KEYS)
    # the synthetic N5584 offset (0.8 mag, z = 11.7) is far out: every σ-matched OANY simulation is rejected (power
    # 1.0), G picks N5584 and p_G is 1/20,001, so rule (3) applies
    assert g["power"]["power"] == p["power"]["power"] == 1.0 and g["p_G"]["k"] == 0
    assert g["reading"] == shape.READ_PREFERRED and g["sub_label"] is None
    tc0 = _load("tc003_g_power", "test_conclusions.py")
    tc0.check_r2_re_g_power(stages["power_json"], len(json.dumps(stages["power_json"], indent=1).encode("utf-8")))
    assert tc0.G_FORBIDDEN_POWER_KEYS == shape.FORBIDDEN_POWER_KEYS
    # every per-model number re-derived from the saved files (the test_conclusions check)
    tc = _load("tc003_g_check", "test_conclusions.py")
    gj = json.loads(json.dumps(_jsonable(g)))
    sj = {k: json.loads(json.dumps(_jsonable(v))) for k, v in sims.items()}
    tc.check_r2_re_g(gj, sj, json.loads(json.dumps(_jsonable(shape.summary(g)))), power_rec=stages["power_json"])


def test_power_stage_never_writes_g_obs_or_other_hosts_z(lad, stages):
    """README: the power stage never forms, saves or logs G_obs, sum z^2 or the z_j of hosts other than N5584."""
    des = _des(lad)
    z = des["W"] @ lad["y"][lad["rows_a"]]
    G, _ = shape.g_stat(z)
    forbidden = [float(G), float(np.sum(z * z))] + [float(v) for j, v in enumerate(z) if j != COL]
    forbidden += [abs(v) for v in forbidden]
    text = json.dumps(_jsonable(stages["power"]), ensure_ascii=False)

    def keys(o):
        if isinstance(o, dict):
            for k, v in o.items():
                yield k
                yield from keys(v)
        elif isinstance(o, list):
            for v in o:
                yield from keys(v)
    assert not set(keys(stages["power_json"])) & set(shape.FORBIDDEN_POWER_KEYS)
    nums = [float(t) for t in re.findall(r"-?\d+\.\d{6,}(?:e-?\d+)?", text)]
    for v in forbidden:
        assert not any(abs(x - v) <= 1e-9 * max(abs(v), 1e-12) for x in nums), v
    log = "\n".join(stages["power_log"])
    lognums = [t for t in re.findall(r"-?\d+\.\d+", log)]
    for v in forbidden:
        for t in lognums:
            d = len(t.split(".")[1])
            assert d < 4 or abs(float(t) - v) > 0.5 * 10 ** -d, (t, v)
    assert "G_obs" not in log and "Σz" not in log
    # the power line for log.md uses nothing beyond the power record
    line = shape.power_log_line(stages["power"])
    assert "power" in line and "G_obs" not in line


def test_two_stage_count_mismatch_is_rule_1(lad, stages):
    bad = json.loads(json.dumps(stages["power_json"]))
    bad["models"]["OANY"]["n_excluded"] += 1
    out, sims = _stage(lad, "full", power_rec=bad)
    assert out["status"].startswith("not evaluable (the full stage does not reproduce the power stage's counts")
    assert out["reading"] == out["status"] and "observed" not in out and "p_G" not in out
    assert out["checks"]["power_stage_count_mismatches"] == [
        f"OANY: {stages['power']['models']['OANY']['n_excluded']} vs power stage "
        f"{stages['power']['models']['OANY']['n_excluded'] + 1}"]
    assert set(sims) == set(SIM_KEYS)


def test_full_stage_after_a_power_stage_stopped_by_rule_1(lad):
    p, _ = _stage(lad, "power", recorded={"tau_obs": lad["rec"]["tau_obs"] + 1e-3})
    assert "n_sims" not in p and p["rule1"]
    g, sims = _stage(lad, "full", power_rec=json.loads(json.dumps(_jsonable(p))))
    assert g["status"] == p["status"] == g["reading"] and "observed" not in g and "models" not in g
    assert set(sims) == set(SIM_KEYS)


def test_full_stage_refuses_a_stub_or_different_settings(lad, stages, monkeypatch):
    """M1/M3 (gate 1): a "not run" stub, another stage's record, different settings or different thread settings
    are an error, not rule (1)."""
    run = lad["run"]
    stub, _ = run.g_not_run(lad["P"], "not run (PARAMS)", "power")
    for rec in (stub, dict(stages["power_json"], stage="full")):
        with pytest.raises(RuntimeError, match="stub or not a power-stage record"):
            _stage(lad, "full", power_rec=json.loads(json.dumps(rec)))
    for key, val in (("g_seed_base", 1), ("g_n_inner", 10), ("g_taus_rep", [0.05]), ("g_z_curve", [3.0]),
                     ("g_power_min", 0.9), ("g_host_seed_base", 7)):
        rec = json.loads(json.dumps(stages["power_json"]))
        rec["settings"][key] = val
        with pytest.raises(RuntimeError, match=key):
            _stage(lad, "full", power_rec=rec)
    real = shape.thread_settings
    monkeypatch.setattr(shape, "thread_settings", lambda: dict(real(), env={"OMP_NUM_THREADS": "7"}))
    with pytest.raises(RuntimeError, match="threads"):
        _stage(lad, "full", power_rec=stages["power_json"])
    assert stages["power"]["settings"]["threads"] == real()


def test_runtime_guard_floor(lad):
    P = dict(lad["P"], g_max_minutes=1e-9, g_min_sims=10)
    p, _ = _stage(lad, "power", P=P)
    assert p["status"] == "not evaluated (runtime)" and p["n_sims"] is None and "models" not in p
    assert p["runtime_guard"]["n"] is None
    g, sims = _stage(lad, "full", P=P, power_rec=json.loads(json.dumps(_jsonable(p))))
    assert g["status"] == g["reading"] == "not evaluated (runtime)" and "observed" not in g
    assert all(v["status"] == "not evaluated (runtime)" for v in sims.values())


@pytest.mark.parametrize("key,shift", [("tau_obs", 3e-5), ("delta_hat", 6e-6), ("sigma_delta", 2e-6),
                                       ("z_obs", 1e-4)])
def test_reproduction_mismatch_stops_before_simulations(lad, key, shift):
    rec = {key: lad["rec"][key] + shift}
    p, _ = _stage(lad, "power", recorded=rec)
    assert p["status"].startswith("not evaluable (reproduction check failed")
    assert "models" not in p and p["checks"]["reproduction"]["mismatches"]


def test_reml_grid_mismatch_and_length(lad):
    g = list(lad["grid"])
    g[10] += 2e-5
    p, _ = _stage(lad, "power", grid=g)
    assert "REML grid differences" in p["status"]
    p, _ = _stage(lad, "power", grid=lad["grid"][:50])
    assert "REML grid has 50 values" in p["status"]
    g = [v + 7.0 for v in lad["grid"]]                  # a constant offset does not matter (differences)
    p, _ = _stage(lad, "power", grid=g, P=dict(lad["P"], g_n_sims=2))
    assert p["status"] == "evaluated"


def test_pointwise_failure_is_rule_1(lad):
    fns = dict(lad["fns"])
    run = lad["run"]
    fns["reml_m2l"] = lambda L, y, C, rows, groups, t: run.reml_m2l(L, y, C, rows, groups, t) + 400.0 * (t - 0.3) ** 2
    p, _ = _stage(lad, "power", fns=fns, P=dict(lad["P"], g_n_sims=3))
    assert p["status"].startswith("not evaluable (pointwise check failed") and "models" not in p


def test_tau_obs_at_the_upper_bound_is_rule_1(lad, monkeypatch):
    fns = dict(lad["fns"])
    orig = lad["run"].reml_tau

    def fake(f, tau_max, step, interval=True):
        r = orig(f, tau_max, step, interval=interval)
        return dict(r, at_upper_bound=True)
    fns["reml_tau"] = fake
    p, _ = _stage(lad, "power", fns=fns)
    assert p["status"] == "not evaluable (τ̂_obs at the upper bound)"


def test_cholesky_failure_is_rule_1(lad):
    fns = dict(lad["fns"])
    run = lad["run"]

    def with_re(C, groups, tau):
        V = run.with_re(C, groups, tau)
        if abs(tau - 0.105) < 1e-12:
            V = V.copy()
            V[0, 0] = -1.0
        return V
    fns["with_re"] = with_re
    p, _ = _stage(lad, "power", fns=fns)
    assert p["status"] == "not evaluable (the Cholesky factor of V(0.105) failed)"
    assert p["checks"]["cholesky_failed"] and "models" not in p


def test_wrong_column_is_refused(lad):
    with pytest.raises(RuntimeError, match="documented as column"):
        shape.run_stage("power", lad["L"], lad["y"], lad["C"], lad["rows_a"], lad["groups"], lad["labels"], lad["P"],
                        lad["fns"], lambda m: None, lad["grid"], expected_col=COL + 1, recorded=lad["rec"])
    with pytest.raises(ValueError):
        shape.run_stage("full", lad["L"], lad["y"], lad["C"], lad["rows_a"], lad["groups"], lad["labels"], lad["P"],
                        lad["fns"], lambda m: None, lad["grid"], expected_col=COL, recorded=lad["rec"])


def test_sims_files_below_1_mb():
    """A per-simulation file of the registered size (10,000 simulations, offset hosts included) serialised as
    ctx.save does stays below 1 MB."""
    from astrolab.results import write_json
    import tempfile
    rng = np.random.default_rng(0)
    n = 10_000
    arr = {"G": rng.uniform(0.05, 0.9, n), "tau": rng.uniform(0, 0.4, n), "k": rng.integers(0, 20_000, n),
           "j": rng.integers(0, 37, n)}
    spec = {"offset": "any"}
    rec = shape.sims_file("OANY", spec, arr, {"g_seed_base": 400_000, "g_n_inner": 20_000, "g_inner_seed": 600_000,
                                              "g_host_seed_base": 500_000}, rng.integers(0, 37, n))
    with tempfile.TemporaryDirectory() as d:
        p = write_json(Path(d) / "x.json", rec)
        assert p.stat().st_size < 1_000_000, p.stat().st_size


# ---------------------------------------------------------------- run.main in the standalone mode
class _Ctx:
    """A stand-in for astrolab's Context: results folder, record_suffix, save into the folder, log."""
    max_save_bytes = None

    def __init__(self, results):
        self.results = results
        self.record_suffix = ""
        self.saved = {}
        self.logs = []

    def save(self, name, obj):
        from astrolab.results import write_json
        self.saved[name] = obj
        write_json(self.results / f"{name}.json", obj)

    def log(self, msg):
        self.logs.append(msg)


def _main_g(tmp_path, monkeypatch, name, lad, stage, summary=True):
    run = _load(name, "run.py")
    L, y, C = lad["L"], lad["y"], lad["C"]
    for c, val in ((run.C_LMC, 0.0), (run.C_MH, -5.85), (run.C_MH, -5.80)):
        r = np.zeros(run.N_PAR)
        r[c] = 1.0
        L = np.vstack([L, r])
        y = np.append(y, val)
        C = np.pad(C, ((0, 1), (0, 1)))
        C[-1, -1] = 0.03 ** 2
    monkeypatch.setattr(run, "N_ROWS", len(y))
    monkeypatch.setattr(run, "load", lambda ctx: (C, L, y, np.zeros((run.N_PAR, 2))))
    monkeypatch.setattr(run, "recorded_reml_grid", lambda: list(lad["grid"]))
    for k, v in (("g_only", True), ("g_check", True), ("g_stage", stage), ("g_n_sims", N_SIMS)):
        monkeypatch.setitem(run.PARAMS, k, v)
    real = run.run_g

    def stub(ctx, P, L_, y_, C_, nz, cls, rows_a, col_host, ident, stage_, grid, power_rec=None, grid_source=None,
             recorded=None):
        # the synthetic columns do not match R22's hosts: force the host step evaluable, label column 26 N5584
        labels = list(lad["labels"])
        return real(ctx, P, L_, y_, C_, nz, cls, rows_a, labels, dict(ident, host_step_evaluable=True), stage_, grid,
                    power_rec=power_rec, grid_source=grid_source, recorded=lad["rec"])
    monkeypatch.setattr(run, "run_g", stub)
    from astrolab.results import write_json
    old = {"params": {"a": 1}, "R2_RE_D": {"reading": "τ̂ x"}, "runtime_s": 1.5}
    if summary:
        write_json(tmp_path / "summary.json", old)
    return run, _Ctx(tmp_path), old


def test_main_g_only_power_then_full(tmp_path, monkeypatch, lad):
    run, ctx, old = _main_g(tmp_path, monkeypatch, "run003_gonly_p", lad, "power")
    run.main(ctx)
    assert ctx.record_suffix == "_gp" and set(ctx.saved) == {"r2_re_g_power"}
    p = ctx.saved["r2_re_g_power"]
    assert p["status"] == "evaluated" and "G_obs" not in json.dumps(_jsonable(p))
    assert any(m.startswith("R2-RE-G power stage (n = 40)") for m in ctx.logs)
    assert "(committed file, standalone mode)" in p["settings"]["reml_grid_source"]
    # full stage: reads the power record from results/, writes r2_re_g, the eight sims files and R2_RE_G only;
    # it needs the power line in log.md (M2, gate 1 round 2)
    run2, ctx2, _ = _main_g(tmp_path, monkeypatch, "run003_gonly_f", lad, "full", summary=False)
    line = shape.power_log_line(json.loads((tmp_path / "r2_re_g_power.json").read_text(encoding="utf-8")))
    assert line in ctx.logs
    monkeypatch.setattr(run2, "study_log_text", lambda: "# log\n- " + line + "\n")
    ret = run2.main(ctx2)
    assert ctx2.record_suffix == "_g"
    assert set(ctx2.saved) == {"r2_re_g", "summary"} | {f"r2_re_g_sims_{k}" for k in SIM_KEYS}
    g = ctx2.saved["r2_re_g"]
    assert g["checks"]["power_stage_counts_reproduced"] and g["n_sims"] == p["n_sims"]
    s = ctx2.saved["summary"]
    assert list(s) == ["params", "R2_RE_D", "R2_RE_G", "runtime_s"] and ret == s
    assert all(s[k] == old[k] for k in old) and s["R2_RE_G"] == shape.summary(g)


def test_main_g_only_full_stage_checks_before_loading(tmp_path, monkeypatch, lad):
    """M2 (gate 1 round 2): a formal g_only full stage reads the power record before loading any data and refuses a
    stub, different settings, or a power line missing from log.md."""
    run, ctx, _ = _main_g(tmp_path, monkeypatch, "run003_gonly_c0", lad, "power")
    run.main(ctx)
    p = json.loads((tmp_path / "r2_re_g_power.json").read_text(encoding="utf-8"))
    from astrolab.results import write_json
    run2, ctx2, _ = _main_g(tmp_path, monkeypatch, "run003_gonly_c1", lad, "full", summary=False)
    monkeypatch.setattr(run2, "load", lambda ctx: pytest.fail("data loaded"))
    monkeypatch.setattr(run2, "study_log_text", lambda: "nothing here")
    with pytest.raises(RuntimeError, match="not in log.md"):
        run2.main(ctx2)
    monkeypatch.setattr(run2, "study_log_text", lambda: shape.power_log_line(p))
    write_json(tmp_path / "r2_re_g_power.json", dict(p, settings=dict(p["settings"], g_inner_seed=1)))
    with pytest.raises(RuntimeError, match="g_inner_seed"):
        run2.main(ctx2)
    stub, _ = run2.g_not_run(run2.PARAMS, "not run (PARAMS)", "power")
    write_json(tmp_path / "r2_re_g_power.json", stub)
    with pytest.raises(RuntimeError, match="stub"):
        run2.main(ctx2)
    assert set(ctx2.saved) == set()


def test_thread_settings_comparison():
    """M1 (gate 1 round 2): the environment is compared strictly; thread pools only for libraries in both."""
    a = {"env": {"OMP_NUM_THREADS": "1"}, "threadpools": [["blas", 1], ["openmp", 1]]}
    assert shape.thread_problems(a, a) == []
    assert shape.thread_problems(a, {"env": {"OMP_NUM_THREADS": "1"}, "threadpools": [["blas", 1]]}) == []
    assert shape.thread_problems(a, dict(a, threadpools=[["blas", 1], ["openmp", 1], ["other", 8]])) == []
    assert shape.thread_problems(a, dict(a, threadpools=[["blas", 4]]))[0].startswith("threads blas")
    assert shape.thread_problems(a, dict(a, env={"OMP_NUM_THREADS": None}))[0].startswith("threads env")


def test_main_g_only_refusals(tmp_path, monkeypatch, lad):
    run, ctx, _ = _main_g(tmp_path, monkeypatch, "run003_gonly_r1", lad, "full")
    with pytest.raises(RuntimeError, match="run g_stage = 'power' first"):
        run.main(ctx)
    (tmp_path / "x").mkdir()
    run, ctx, _ = _main_g(tmp_path / "x", monkeypatch, "run003_gonly_r2", lad, "full", summary=False)
    with pytest.raises(RuntimeError, match="run the full study first"):
        run.main(ctx)
    run, ctx, _ = _main_g(tmp_path, monkeypatch, "run003_gonly_r3", lad, "power")
    monkeypatch.setitem(run.PARAMS, "g_check", False)
    with pytest.raises(ValueError, match="g_check"):
        run.main(ctx)
    monkeypatch.setitem(run.PARAMS, "g_check", True)
    monkeypatch.setitem(run.PARAMS, "d_only", True)
    with pytest.raises(ValueError, match="d_only and g_only"):
        run.main(ctx)
    monkeypatch.setitem(run.PARAMS, "d_only", False)
    monkeypatch.setitem(run.PARAMS, "g_stage", "both")
    with pytest.raises(ValueError, match="g_stage"):
        run.main(ctx)


def test_exploration_cannot_reach_g_obs_before_the_formal_full_stage(tmp_path, monkeypatch, lad):
    """S1 (gate 1): until the formal results/r2_re_g.json is committed, an exploration may run only the power stage;
    a g_only full stage and a full-study exploration with g_check = true are refused before any data is loaded."""
    run, ctx, _ = _main_g(tmp_path, monkeypatch, "run003_gonly_x1", lad, "full", summary=False)
    monkeypatch.setattr(run, "formal_g_done", lambda: False)
    monkeypatch.setattr(run, "load", lambda ctx: pytest.fail("data loaded"))
    ctx.max_save_bytes = 1024 ** 2
    with pytest.raises(RuntimeError, match="only g_stage = 'power'"):
        run.main(ctx)
    monkeypatch.setitem(run.PARAMS, "g_only", False)
    with pytest.raises(RuntimeError, match="would compute G on the data"):
        run.main(ctx)
    # S1 (gate 1 round 2): also a formal (non-exploration) full study run with g_check = true
    ctx.max_save_bytes = None
    with pytest.raises(RuntimeError, match="would compute G on the data"):
        run.main(ctx)
    assert ctx.saved == {}
    ctx.max_save_bytes = 1024 ** 2
    # the power stage is allowed in an exploration
    (tmp_path / "p").mkdir()
    run2, ctx2, _ = _main_g(tmp_path / "p", monkeypatch, "run003_gonly_x2", lad, "power", summary=False)
    monkeypatch.setattr(run2, "formal_g_done", lambda: False)
    ctx2.max_save_bytes = 1024 ** 2
    run2.main(ctx2)
    assert set(ctx2.saved) == {"r2_re_g_power"}
    # formal_g_done (M3, gate 1 round 2): absent, a stub, a not-evaluable record without `observed`, a formal record
    run3 = _load("run003_g_done", "run.py")
    from astrolab.results import write_json
    f = tmp_path / "g.json"
    assert not run3.formal_g_done(f)
    for rec, exp in (({"status": "not run (PARAMS)"}, False),
                     ({"status": "not evaluable (R2-RE not run or host step not evaluable)"}, False),
                     ({"status": "not evaluable (anti-conservative at τ = 0.05)", "observed": {}}, True),
                     ({"status": "evaluated"}, True)):
        write_json(f, rec)
        assert run3.formal_g_done(f) == exp, rec


def test_g_check_false_full_run_keeps_formal_files(tmp_path):
    """M2 (gate 1): with g_check = false a full study run writes the "not run" records only where no R2-RE-G file
    exists and takes the summary from an existing r2_re_g.json."""
    run = _load("run003_g_stubs", "run.py")
    from astrolab.results import write_json
    formal = {"stage": "full", "status": "evaluated", "reading": "diffuse scatter not excluded"}
    write_json(tmp_path / "r2_re_g.json", formal)
    write_json(tmp_path / "r2_re_g_sims_VHAT.json", {"model": "VHAT", "status": "evaluated"})
    ctx = _Ctx(tmp_path)
    g = run.save_g_stubs(ctx, run.PARAMS, "not run (PARAMS)")
    assert g == formal and "r2_re_g" not in ctx.saved and "r2_re_g_sims_VHAT" not in ctx.saved
    assert set(ctx.saved) == {"r2_re_g_power"} | {f"r2_re_g_sims_{k}" for k in SIM_KEYS if k != "VHAT"}
    assert json.loads((tmp_path / "r2_re_g.json").read_text(encoding="utf-8")) == formal
    (tmp_path / "e").mkdir()
    ctx2 = _Ctx(tmp_path / "e")
    g2 = run.save_g_stubs(ctx2, run.PARAMS, "not run (PARAMS)")
    assert g2["status"] == "not run (PARAMS)" and len(ctx2.saved) == 10
    # M3 (gate 1 round 2): the not-evaluable records of a g_check = true run follow the same rule
    ctx3 = _Ctx(tmp_path)
    g3 = run.save_g_stubs(ctx3, run.PARAMS, "not evaluable (R2-RE not run or host step not evaluable)")
    assert g3 == formal and "r2_re_g" not in ctx3.saved
    assert json.loads((tmp_path / "r2_re_g.json").read_text(encoding="utf-8")) == formal


def test_main_g_only_exploration_runs_both_stages(tmp_path, monkeypatch, lad):
    """In an exploration (empty folder, no power record) after the formal full stage, both stages run in one
    process, the power record saved first."""
    run, ctx, _ = _main_g(tmp_path, monkeypatch, "run003_gonly_e", lad, "full", summary=False)
    monkeypatch.setattr(run, "formal_g_done", lambda: True)
    ctx.max_save_bytes = 1024 ** 2
    run.main(ctx)
    assert list(ctx.saved)[0] == "r2_re_g_power"
    assert set(ctx.saved) == {"r2_re_g_power", "r2_re_g", "summary"} | {f"r2_re_g_sims_{k}" for k in SIM_KEYS}
    assert ctx.saved["summary"] == {"R2_RE_G": shape.summary(ctx.saved["r2_re_g"])}
    assert ctx.saved["r2_re_g"]["checks"]["power_stage_counts_reproduced"]


def test_not_run_records():
    run = _load("run003_g_notrun", "run.py")
    out, sims = run.g_not_run(run.PARAMS, "not run (PARAMS)", "full")
    assert out["status"] == "not run (PARAMS)" and set(sims) == set(SIM_KEYS)
    assert shape.summary(out) == {"status": "not run (PARAMS)", "reading": None}
