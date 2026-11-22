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


REAL_FORMAL_G_DONE = shape.formal_g_done


@pytest.fixture(scope="module", autouse=True)
def _formal_gate_open():
    """The full stage's own gate (shape.formal_g_done or the power line in log.md) is opened for the synthetic
    tests; test_full_stage_gate_in_shape closes it."""
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(shape, "formal_g_done", lambda path=None: True)
        yield


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
    with pytest.raises(RuntimeError, match="not present in log.md"):
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


def test_full_stage_gate_in_shape(lad, stages, monkeypatch, tmp_path):
    """Gate 1 round 3: shape.run_stage itself refuses a full stage (so an explore/ script cannot bypass the gate)
    unless the formal r2_re_g.json exists or the power record's line is present in log.md."""
    monkeypatch.setattr(shape, "formal_g_done", lambda path=None: False)
    monkeypatch.setattr(shape, "study_log_text", lambda: "no power line")
    with pytest.raises(RuntimeError, match="not present in log.md"):
        _stage(lad, "full", power_rec=stages["power_json"])
    monkeypatch.setattr(shape, "study_log_text", lambda: "x\n" + shape.power_log_line(stages["power_json"]) + "\n")
    g, _ = _stage(lad, "full", power_rec=stages["power_json"], P=dict(lad["P"]))
    assert g["status"] == "evaluated"
    # formal_outcome: a full-stage record with settings (any status), not a "not run" record
    from astrolab.results import write_json
    f = tmp_path / "g.json"
    assert not shape.formal_outcome(f)
    write_json(f, {"stage": "full", "status": "not run (PARAMS)", "reading": None})
    assert not shape.formal_outcome(f)
    write_json(f, {"stage": "full", "status": "not evaluable (x)", "settings": {}})
    assert shape.formal_outcome(f)


def test_g_only_full_rerun_needs_a_reason(tmp_path, monkeypatch, lad):
    """Gate 1 round 3: a formal g_only full stage over an existing formal outcome needs g_rerun_reason, a non-empty
    text also present in log.md."""
    run, ctx, _ = _main_g(tmp_path, monkeypatch, "run003_gonly_rr0", lad, "power")
    run.main(ctx)
    p = json.loads((tmp_path / "r2_re_g_power.json").read_text(encoding="utf-8"))
    from astrolab.results import write_json
    write_json(tmp_path / "r2_re_g.json", {"stage": "full", "status": "not evaluable (x)", "settings": {}})
    run2, ctx2, _ = _main_g(tmp_path, monkeypatch, "run003_gonly_rr1", lad, "full", summary=False)
    monkeypatch.setattr(run2, "load", lambda ctx: pytest.fail("data loaded"))
    monkeypatch.setattr(run2, "study_log_text", lambda: shape.power_log_line(p) + "\nrerun: fixed a bug in x\n")
    for why in ("", "   ", "not in the log"):
        monkeypatch.setitem(run2.PARAMS, "g_rerun_reason", why)
        with pytest.raises(RuntimeError, match="g_rerun_reason"):
            run2.main(ctx2)
    monkeypatch.setitem(run2.PARAMS, "g_rerun_reason", "rerun: fixed a bug in x")
    with pytest.raises(pytest.fail.Exception, match="data loaded"):     # past the gate: it would load the data
        run2.main(ctx2)


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
    monkeypatch.setattr(shape, "formal_g_done", REAL_FORMAL_G_DONE)      # run.formal_g_done delegates to it
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


# ==================================================================================================================
# R2-RE-GT (README section 2, addendum 2026-11-21, T-057), synthetic data only: the variance matching of the t host
# effects, u = Z^T P K_C eps + M b against full y_s, the inner covariance M + tau^2 M^2, the size of the T test at a
# known tau under T(tau), the rules and the sub-labels of rule (2), the gloss, the power record free of p_T,obs,
# the reproduction of R2-RE-G's simulations, the two stages, the standalone mode and its gates, and R2-RE-G's code
# unchanged.
# ==================================================================================================================
GT_SIM_KEYS = ["THAT", "T050", "T105", "OANY", "OANYVN", "TC", "VHAT"]
REAL_GT_FORMAL_DONE = shape.gt_formal_done

# R2-RE-G's text as reviewed (T-055): shape.py up to the R2-RE-GT block, and run.py's R2-RE-G functions
SHAPE_G_CHARS = 45500
SHAPE_G_SHA256 = "1f16cec73fb049ed52ab3604aae41452690b9b8339c889642d7bfd7d8daf71bd"
RUN_G_SHA256 = {
    "fit": "f9550ff1308d2e0f5229657b11e1a3dace089e5908cefc663b1b040b4610a9ae",
    "is_fit_failure": "e49debb4690c29fe1207057d13db72f1550daee90dc78e5c34c01c9303fdae03",
    "with_re": "53feab23d4e77f7137b49c1484cf1d707e740d463f0412cbecdd23e889bd27e7",
    "reml_m2l": "fe34c134f3707d6096e3fe1718d703687ef8b3cf8c5de245849e4c935935de19",
    "reml_tau": "f44d3cb1b6351f05cebcc9b332ede823f2dcaa741bf17ab6e3ca49dfd618c6b8",
    "save_g": "614d671895986ef50ef0316e251306d603100f2bbbc5e1b40e1bc037e4240ed6",
    "recorded_reml_grid": "0fe53d04897a57ca48f5f298e6abdba0342a1dfcfb52bcf711743792b51adee8",
    "save_g_stubs": "7d9d4c26266f4dfa4fbc7eedaef8018b5afca638588ae308148226b5d5a915d7",
    "g_not_run": "ab10cf129fb09fd815f470118eb94f7fe5d76fd2b12b64892fc967db5c30d3f1",
    "run_g": "82887ea8c64b418cb23ba5a6127565b20997e19f111846904d282ca7c6068444",
    "run_g_both": "2f3c0d8bba5687b57d548a418979bdf74e8f1ae9d4315c4b2e2cd39b7e096291",
}


def test_r2_re_g_code_unchanged():
    """R2-RE-GT adds to shape.py and run.py without changing R2-RE-G's code (README R2-RE-GT: no change to
    R2-RE-G's functions or results)."""
    import ast
    import hashlib
    text = (HERE / "shape.py").read_text(encoding="utf-8")
    assert hashlib.sha256(text[:SHAPE_G_CHARS].encode("utf-8")).hexdigest() == SHAPE_G_SHA256
    assert text[SHAPE_G_CHARS:].startswith("\n\n# ====") and "R2-RE-GT" in text[SHAPE_G_CHARS:SHAPE_G_CHARS + 300]
    src = (HERE / "run.py").read_text(encoding="utf-8")
    found = {n.name: hashlib.sha256(ast.get_source_segment(src, n).encode("utf-8")).hexdigest()
             for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name in RUN_G_SHA256}
    assert found == RUN_G_SHA256


def test_gt_params_and_constants():
    run = _load("run003_gt_params", "run.py")
    P = run.PARAMS
    assert (P["gt_check"], P["gt_only"], P["gt_stage"], P["gt_seed_base"], P["gt_inner_seed"],
            P["gt_inner_seeds_rep"], P["gt_nu"], P["gt_nu_rep"], P["gt_n_sims"], P["gt_n_inner"], P["gt_power_min"],
            P["gt_max_minutes"], P["gt_min_sims"], P["gt_rerun_reason"]) == (
        False, False, "full", 410_000, 610_000, [611_000, 612_000], 4, [3, 10], 10_000, 20_000, 0.8, 120, 5_000, "")
    assert (P["g_seed_base"], P["g_host_seed_base"], P["g_inner_seed"], P["g_taus_rep"]) == (400_000, 500_000,
                                                                                              600_000, TAUS_REP)
    assert shape.gt_sim_keys(TAUS_REP) == GT_SIM_KEYS and shape.gt_size_keys(TAUS_REP) == GT_SIM_KEYS[:3]
    assert (shape.GT_RECORDED_G_OBS, shape.GT_G_OBS_RTOL, shape.GT_RECORDED_K_G) == (0.30485762235426483, 1e-8, 326)
    assert shape.GT_EM_SCALE == 0.07521926289752753 and shape.GT_N_POINTWISE == 3
    assert shape.GT_REPRO_KEYS == ("VHAT", "OANY", "OANYVN")
    assert abs(shape.gt_scale(1.0, 4) - 2 ** -0.5) < 1e-15 and abs(shape.gt_scale(1.0, 3) - 3 ** -0.5) < 1e-15
    assert abs(shape.gt_scale(1.0, 10) - 0.8 ** 0.5) < 1e-15
    tc = _load("tc003_gt_consts", "test_conclusions.py")
    assert tc.GT_FORBIDDEN_POWER_KEYS == shape.GT_FORBIDDEN_POWER_KEYS and tc.GT_SIM_KEYS == GT_SIM_KEYS
    # the recorded values agree with the saved R2-RE-G and R2-RE-N5584 results (when present)
    res = HERE / "results"
    if (res / "r2_re_g.json").exists():
        g = json.loads((res / "r2_re_g.json").read_text(encoding="utf-8"))
        if "observed" in g:
            assert g["observed"]["G_obs"] == shape.GT_RECORDED_G_OBS and g["p_G"]["k"] == shape.GT_RECORDED_K_G
            assert g["settings"]["g_n_inner"] == P["gt_n_inner"]
    if (res / "r2_re_n5584.json").exists():
        n = json.loads((res / "r2_re_n5584.json").read_text(encoding="utf-8"))
        assert n["heavy_tail"]["nu_main"]["tau_hat"] == shape.GT_EM_SCALE and n["heavy_tail"]["nu_main"]["nu"] == 4
    # seeds collide with no earlier block (R2-RE-G's list plus 400,000-409,999, 500,000-509,999, 600,000)
    used = [(0, 0), (10_000, 11_999), (20_000, 21_999), (50_000, 50_999), (100_000, 109_999), (200_000, 209_999),
            (300_000, 300_199), (400_000, 409_999), (500_000, 509_999), (600_000, 600_000)]
    for lo, hi in [(410_000, 419_999), (610_000, 610_000), (611_000, 611_000), (612_000, 612_000)]:
        assert all(hi < a or lo > b for a, b in used)


def test_gt_variance_matching():
    """b = s t with s = tau sqrt((nu - 2) / nu): the sample variance of b equals tau^2 within Monte Carlo error (t4's
    fourth moment is infinite, so the tolerance is loose); the same for nu = 3 and 10."""
    tau = 0.08
    for nu, seed in ((4, 610_000), (3, 611_000), (10, 612_000)):
        b = shape.gt_scale(tau, nu) * shape.t_draws(seed, nu, (40_000, 37))
        assert abs(b.var() / tau ** 2 - 1) < (0.05 if nu > 3 else 0.15), (nu, b.var() / tau ** 2)
    T = shape.t_block(410_000, [0, 5], 4, 37)
    assert np.array_equal(T[:, 1], np.random.default_rng(410_005).standard_t(4, 37))
    assert np.array_equal(shape.t_draws(610_000, 4, (20, 37)),
                          np.random.default_rng(610_000).standard_t(4, (20, 37)))


def test_gt_u_identity_against_full_y(lad):
    """u = Z^T P K_C eps + M b: z = B_C eps + WH b equals the 37 one-column fits on y_s = y_hat + K_C eps + Z b
    built in full, and Z^T P y_s equals diag(sqrt(M_jj)) z."""
    des = _des(lad)
    assert np.max(np.abs(des["WH"] - des["dinv"][:, None] * des["M"])) < 1e-9 * np.max(np.abs(des["WH"]))
    B = des["W"] @ des["Kc"]
    for s in range(2):
        eps = onehost.eps_block(400_000, [s], des["n_a"])[:, 0]
        b = shape.gt_scale(0.15, 4) * shape.t_block(410_000, [s], 4, 37)[:, 0]
        z = B @ eps + des["WH"] @ b
        y = np.array(lad["y"], dtype=float)
        y[lad["rows_a"]] = des["yhat"] + des["Kc"] @ eps + shape.host_effect_y(b, des)
        d, sd = shape.one_column_z(lad["L"], y, lad["C"], lad["rows_a"], lad["groups"], lad["fns"])
        assert np.max(np.abs(d / sd - z)) < 1e-9
        u = des["PZt"] @ y[lad["rows_a"]]
        assert np.max(np.abs(u - z * des["sqrt_m"])) < 1e-9 * np.max(np.abs(u))
        hy = shape.host_effect_y(b, des)
        for j in (0, COL):
            assert np.allclose(hy[des["gpos"][j]], b[j])


def test_gt_inner_covariance(lad):
    """The inner draws z_i = A0_i + s T0_i: Cov = D (M + tau^2 M^2) D (variance matching), exactly for the two
    factors and within Monte Carlo error for the fixed draws; k counts G_i >= G exactly; the draw is linear in s."""
    des = _des(lad)
    D = np.diag(des["dinv"])
    M = des["M"]
    A = shape.inner_matrix(0.0, des)
    assert np.max(np.abs(A @ A.T - D @ M @ D)) < 1e-8
    tau = 0.12
    s = shape.gt_scale(tau, 4)
    # Var(t4) = 2: s^2 * 2 * WH WH^T = tau^2 D M^2 D
    assert np.max(np.abs(s * s * 2.0 * des["WH"] @ des["WH"].T - tau ** 2 * D @ M @ M @ D)) < 1e-8
    E = shape.inner_draws(600_000, 20_000, 37)
    T = shape.t_draws(610_000, 4, (20_000, 37))
    inner = shape.TInner(des, E, T, 4)
    Zi = inner.draws(s)
    target = D @ (M + tau * tau * M @ M) @ D
    assert np.max(np.abs(np.cov(Zi.T) - target)) < 0.08 * np.max(np.diag(target))
    Z2 = Zi ** 2
    Gi = Z2.max(axis=1) / Z2.sum(axis=1)
    assert inner.k(0.25, tau) == inner.k_scale(0.25, s) == int(np.sum(Gi >= 0.25))
    assert np.array_equal(inner.draws(0.0), inner.A0) and np.allclose(inner.A0, E @ A.T)
    # at s = 0 the T test is R2-RE-G's Gaussian test at tau = 0
    assert inner.k(0.2, 0.0) == shape.inner_k(0.2, 0.0, des, E)


def test_gt_size_at_a_known_tau(lad):
    """The whole T procedure (tau refitted, T inner draws, label) under T(0.08) on the synthetic system: the rejection
    rate is not above the upper end of the 99% Clopper-Pearson interval of 0.05."""
    des = _des(lad)
    n = 300
    sp = shape.gt_model_specs(TAUS_REP, 0.08, 0.03, 3.6, 4)
    inner = shape.TInner(des, shape.inner_draws(600_000, 20_000, 37), shape.t_draws(610_000, 4, (20_000, 37)), 4)
    a = shape.gt_simulate(sp["THAT"], des["W"] @ des["Kc"], des, inner, 400_000, 410_000, 4, 0, n,
                          onehost.offset_hosts(500_000, n, 37), lad["run"].reml_tau)
    rej = sum(1 for k in a["k"] if shape.p_label(k, 20_000)[0] == shape.EXCL)
    hi99 = rob._cp(int(round(0.05 * n)), n, level=0.99)[1]
    assert rej / n <= hi99, rej
    assert np.all(np.isfinite(a["G"])) and np.all(np.isfinite(a["tau"]))


def test_gt_models_without_t_effects_equal_r2_re_g_simulate(lad):
    """OANY, OANYVN, VHAT and TC draw z_s exactly as R2-RE-G's simulate (same G_s, tau_s, j_s)."""
    des = _des(lad)
    sp_g = shape.model_specs(TAUS_REP, Z_CURVE, 0.08, 0.03, 3.6, 0.3, COL)
    sp_t = shape.gt_model_specs(TAUS_REP, 0.08, 0.03, 3.6, 4)
    E = shape.inner_draws(600_000, 2_000, 37)
    inner = shape.TInner(des, E, shape.t_draws(610_000, 4, (2_000, 37)), 4)
    hosts = onehost.offset_hosts(500_000, 12, 37)
    B = des["W"] @ des["Kc"]
    for kg, kt in (("OANY", "OANY"), ("C", "TC")):
        a = shape.simulate(sp_g[kg], B, des, E, 400_000, 0, 12, hosts, lad["run"].reml_tau, 2_000)
        b = shape.gt_simulate(sp_t[kt], B, des, inner, 400_000, 410_000, 4, 0, 12, hosts, lad["run"].reml_tau)
        for k in ("G", "tau", "j", "at_zero"):
            assert np.array_equal(a[k], b[k]), (kt, k)


def test_gt_reading_rules_and_sub_labels():
    R = shape.gt_reading
    assert R(["x"], 0.9, "excluded") == ("not evaluable (x)", None)
    assert R(["anti-conservative at τ = 0.05"], 0.3, "excluded") == (
        "not evaluable (anti-conservative at τ = 0.05)", None)
    assert R([shape.RUNTIME], 0.9, None) == ("not evaluated (runtime)", None)
    assert R([], 0.79, "excluded") == ("undetermined (underpowered)", "t₄ diffuse excluded")
    assert R([], 0.79, "not excluded") == ("undetermined (underpowered)", "t₄ diffuse not excluded")
    assert R([], 0.2, shape.UNDET_MC) == ("undetermined (underpowered)", "t₄ diffuse undetermined (Monte Carlo)")
    assert R([], 0.8, "excluded") == ("one offset host preferred over t₄ diffuse scatter", None)   # 0.8 is powered
    assert R([], 0.95, "not excluded") == ("t₄ diffuse scatter not excluded", None)
    assert R([], 0.95, shape.UNDET_MC) == ("undetermined (Monte Carlo)", None)
    G = shape.gt_gloss
    assert G(*R([], 0.5, "excluded"), []) == G(*R([], 0.9, "excluded"), []) == "not only Gaussian tails"
    assert G(*R([], 0.5, "not excluded"), []) == G(*R([], 0.9, "not excluded"), []) == \
        "not shown to hold beyond Gaussian tails"
    assert G(*R([], 0.5, shape.UNDET_MC), []) == G(*R([], 0.9, shape.UNDET_MC), []) == \
        "t₄ comparison undetermined (Monte Carlo)"
    assert G(*R(["a", "b"], 0.9, "excluded"), ["a", "b"]) == "t₄ comparison not evaluable (a; b)"
    assert shape.gt_t(10) == "t₁₀" and shape.tkey(0.05) == "T050" and shape.tkey(0.105) == "T105"
    m = lambda k, n, t: {"status": "evaluated", "tau_t": t, "ci95": list(rob._cp(k, n))}
    models = {"THAT": m(700, 10_000, 0.0767), "T050": m(500, 10_000, 0.05), "T105": m(520, 10_000, 0.105)}
    assert shape.gt_anti_conservative(models, TAUS_REP) == [0.0767]


def test_check_g_sims_errors(stages, lad):
    P = dict(lad["P"])
    ok = shape.check_g_sims(_jsonable(stages["sims"]), P)
    assert set(ok) == set(shape.GT_REPRO_KEYS) and len(ok["OANY"]["G"]) == N_SIMS
    bad = json.loads(json.dumps(_jsonable(stages["sims"])))
    bad["OANY"]["host_seed_base"] = 1
    with pytest.raises(RuntimeError, match="OANY: host_seed_base"):
        shape.check_g_sims(bad, P)
    with pytest.raises(RuntimeError, match="VHAT: not an evaluated"):
        shape.check_g_sims({k: v for k, v in _jsonable(stages["sims"]).items() if k != "VHAT"}, P)
    with pytest.raises(RuntimeError, match="g_seed_base"):
        shape.check_g_sims(_jsonable(stages["sims"]), dict(P, g_seed_base=7))


@pytest.fixture(scope="module", autouse=True)
def _formal_gt_gate_open():
    """The R2-RE-GT full stage's own gate is opened for the synthetic tests; test_gt_full_stage_gate closes it."""
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(shape, "gt_formal_done", lambda path=None: True)
        yield


def _gt_rec(lad, stages):
    g = stages["full"]
    return dict(lad["rec"], g_obs=g["observed"]["G_obs"], k_g_obs=g["p_G"]["k"])


def _gt_stage(lad, stages, stage, P=None, power_rec=None, recorded=None, log=None, g_saved=None, fns=None):
    rc = _gt_rec(lad, stages)
    rc.update(recorded or {})
    P = dict(lad["P"], gt_n_sims=N_SIMS) if P is None else P
    gs = shape.check_g_sims(_jsonable(stages["sims"]), P) if g_saved is None else g_saved
    return shape.run_gt_stage(stage, lad["L"], lad["y"], lad["C"], lad["rows_a"], lad["groups"], lad["labels"], P,
                              lad["fns"] if fns is None else fns, (lambda m: None) if log is None else log,
                              lad["grid"], gs, power_rec=power_rec, expected_col=COL, recorded=rc)


@pytest.fixture(scope="module")
def gt_stages(lad, stages):
    logs = []
    p_out, none = _gt_stage(lad, stages, "power", log=logs.append)
    assert none is None
    p_json = json.loads(json.dumps(_jsonable(p_out)))
    g_out, sims = _gt_stage(lad, stages, "full", power_rec=p_json)
    return dict(power=p_out, power_json=p_json, power_log=logs, full=g_out, sims=sims)


def test_gt_power_and_full_stage(lad, stages, gt_stages):
    p, g, sims = gt_stages["power"], gt_stages["full"], gt_stages["sims"]
    assert p["status"] == "evaluated" and p["stage"] == "power" and p["n_sims"] == N_SIMS
    assert all(q["ok"] for q in p["checks"]["pointwise"]) and len(p["checks"]["pointwise"]) == 3
    assert p["checks"]["reproduction"]["mismatches"] == []
    rg = p["checks"]["r2_re_g_simulations_reproduced"]
    assert all(rg[k]["ok"] and rg[k]["n_compared"] == N_SIMS for k in shape.GT_REPRO_KEYS)
    # bit for bit here: the same blocks of B eps_s and the same refit
    for k in shape.GT_REPRO_KEYS:
        assert rg[k]["max_abs_dG"] <= 0.5e-5 and rg[k]["max_abs_dtau"] <= 0.5e-6
    assert set(p["models"]) == set(GT_SIM_KEYS) and p["sim_keys"] == GT_SIM_KEYS
    assert p["power"]["power"] == min(p["models"]["OANY"]["rate"], p["models"]["OANYVN"]["rate"])
    assert g["checks"]["power_stage_counts_reproduced"] and all(g["checks"]["power_stage_k_sha256_equal"].values())
    assert g["status"] == "evaluated" and g["observed"]["host_j_hat"] == "N5584"
    assert g["checks"]["real_data"]["mismatches"] == []
    assert g["checks"]["real_data"]["k_gauss_obs"] == stages["full"]["p_G"]["k"]
    assert set(sims) == set(GT_SIM_KEYS)
    # the synthetic N5584 offset (z = 11.7) is far out: power 1.0 and p_T,obs "excluded" (heavier tails than
    # R2-RE-G's null, so k > 0 where R2-RE-G's k is 0), rule (3)
    assert g["power"]["power"] == 1.0 and g["p_T_obs"]["label"] == "excluded"
    assert g["p_T_obs"]["k"] >= stages["full"]["p_G"]["k"]
    assert g["reading"] == "one offset host preferred over t₄ diffuse scatter" and g["sub_label"] is None
    assert g["gloss"] == "not only Gaussian tails"
    assert set(g["sensitivities"]["nu"]) == {"3", "10"} and set(g["sensitivities"]["fixed_tau"]) == {"0.05", "0.105"}
    assert g["sensitivities"]["em_scale"]["scale"] == shape.GT_EM_SCALE
    # T models carry t host effects, the others are R2-RE-G's draws
    assert sims["THAT"]["tau_t"] == g["observed"]["tau_hat_obs"] and "tau_t" not in sims["OANY"]
    tc = _load("tc003_gt_check", "test_conclusions.py")
    tc.check_r2_re_gt_power(gt_stages["power_json"], len(json.dumps(gt_stages["power_json"], indent=1).encode()))
    gj = json.loads(json.dumps(_jsonable(g)))
    sj = {k: json.loads(json.dumps(_jsonable(v))) for k, v in sims.items()}
    tc.check_r2_re_gt(gj, sj, json.loads(json.dumps(_jsonable(shape.gt_summary(g)))),
                      power_rec=gt_stages["power_json"], g_sims=_jsonable(stages["sims"]))


def test_gt_power_record_has_no_p_t(lad, gt_stages):
    """README R2-RE-GT: the power stage never computes p_T,obs (no such key, no real-data check, no G_obs; its log
    and its log.md line hold power and size only)."""
    pj = gt_stages["power_json"]
    tc = _load("tc003_gt_keys", "test_conclusions.py")
    assert not set(tc._keys_of(pj)) & set(shape.GT_FORBIDDEN_POWER_KEYS)
    log = "\n".join(gt_stages["power_log"])
    assert "p_T" not in log and "G_obs" not in log
    line = shape.gt_power_log_line(pj)
    assert line.startswith(f"R2-RE-GT power stage (n = {N_SIMS}): power = min(R_OANY") and "p_T" not in line
    assert line == shape.gt_power_log_line(gt_stages["power"])


def test_gt_reproduction_of_r2_re_g_fails_is_rule_1(lad, stages):
    P = dict(lad["P"], gt_n_sims=N_SIMS)
    gs = shape.check_g_sims(_jsonable(stages["sims"]), P)
    gs["OANYVN"]["G"] = gs["OANYVN"]["G"].copy()
    gs["OANYVN"]["G"][3] += 2e-5
    p, _ = _gt_stage(lad, stages, "power", g_saved=gs)
    assert p["status"].startswith("not evaluable (reproduction of R2-RE-G's simulations failed (OANYVN: 1 G_s")
    assert "models" in p


def test_gt_real_data_checks_are_rule_1(lad, stages, gt_stages):
    for rec, msg in (({"g_obs": stages["full"]["observed"]["G_obs"] * (1 + 2e-8)}, "G_obs"),
                     ({"k_g_obs": stages["full"]["p_G"]["k"] + 1}, "Gaussian inner draws")):
        g, sims = _gt_stage(lad, stages, "full", power_rec=gt_stages["power_json"], recorded=rec)
        assert g["status"].startswith("not evaluable (reproduction check failed: ") and msg in g["status"]
        assert "p_T_obs" not in g and g["reading"] == g["status"] and g["sub_label"] is None
        assert g["gloss"].startswith("t₄ comparison not evaluable (")
        assert set(sims) == set(GT_SIM_KEYS)


def test_gt_anti_conservative_only_still_reports_p_t(lad, stages, gt_stages, monkeypatch):
    """Rule (1) with anti-conservativeness as the only reason: p_T,obs and its label are computed and reported, with
    no sub-label (README R2-RE-GT, as R2-RE-G amendment 5)."""
    monkeypatch.setattr(shape, "gt_anti_conservative", lambda models, taus: [0.105])
    g, _ = _gt_stage(lad, stages, "full", power_rec=gt_stages["power_json"])
    assert g["status"] == g["reading"] == "not evaluable (anti-conservative at τ = 0.105)"
    assert "p_T_obs" in g and g["sub_label"] is None and g["gloss"] == \
        "t₄ comparison not evaluable (anti-conservative at τ = 0.105)"


def test_gt_two_stage_count_mismatch_and_refusals(lad, stages, gt_stages, monkeypatch):
    bad = json.loads(json.dumps(gt_stages["power_json"]))
    bad["models"]["THAT"]["n_excluded"] += 1
    g, _ = _gt_stage(lad, stages, "full", power_rec=bad)
    assert g["status"].startswith("not evaluable (the full stage does not reproduce the power stage's counts")
    assert "p_T_obs" not in g
    stub, _ = lad["run"].gt_not_run(lad["P"], "not run (PARAMS)", "power")
    with pytest.raises(RuntimeError, match="stub or not a power-stage record"):
        _gt_stage(lad, stages, "full", power_rec=json.loads(json.dumps(stub)))
    for key, val in (("gt_seed_base", 1), ("gt_nu", 3), ("gt_inner_seeds_rep", [1, 2]), ("g_taus_rep", [0.05]),
                     ("g_inner_seed", 7), ("gt_n_inner", 10)):
        rec = json.loads(json.dumps(gt_stages["power_json"]))
        rec["settings"][key] = val
        with pytest.raises(RuntimeError, match=key):
            _gt_stage(lad, stages, "full", power_rec=rec)
    real = shape.thread_settings
    monkeypatch.setattr(shape, "thread_settings", lambda: dict(real(), env={"OMP_NUM_THREADS": "7"}))
    with pytest.raises(RuntimeError, match="threads"):
        _gt_stage(lad, stages, "full", power_rec=gt_stages["power_json"])


def test_gt_full_stage_gate(lad, stages, gt_stages, monkeypatch, tmp_path):
    """run_gt_stage itself refuses a full stage unless the formal r2_re_gt.json exists or the power line is in
    log.md; gt_formal_done reads the formal record."""
    monkeypatch.setattr(shape, "gt_formal_done", lambda path=None: False)
    monkeypatch.setattr(shape, "study_log_text", lambda: "no power line")
    with pytest.raises(RuntimeError, match="not present in log.md"):
        _gt_stage(lad, stages, "full", power_rec=gt_stages["power_json"])
    monkeypatch.undo()
    from astrolab.results import write_json
    f = tmp_path / "gt.json"
    assert REAL_GT_FORMAL_DONE(f) is False
    for rec, exp in (({"status": "not run (PARAMS)"}, False), ({"status": "not evaluable (x)", "p_T_obs": {}}, True),
                     ({"status": "evaluated"}, True)):
        write_json(f, rec)
        assert REAL_GT_FORMAL_DONE(f) == exp, rec


def test_gt_runtime_guard_floor_and_stopped_power_stage(lad, stages):
    P = dict(lad["P"], gt_n_sims=N_SIMS, gt_max_minutes=1e-9, gt_min_sims=10)
    p, _ = _gt_stage(lad, stages, "power", P=P)
    assert p["status"] == "not evaluated (runtime)" and p["n_sims"] is None and "models" not in p
    g, sims = _gt_stage(lad, stages, "full", P=P, power_rec=json.loads(json.dumps(_jsonable(p))))
    assert g["status"] == g["reading"] == "not evaluated (runtime)" and "p_T_obs" not in g
    assert g["gloss"] == "t₄ comparison not evaluable (runtime)"
    assert all(v["status"] == "not evaluated (runtime)" for v in sims.values())
    p, _ = _gt_stage(lad, stages, "power", recorded={"tau_obs": lad["rec"]["tau_obs"] + 1e-3})
    assert p["status"].startswith("not evaluable (reproduction check failed") and "models" not in p
    g, _ = _gt_stage(lad, stages, "full", power_rec=json.loads(json.dumps(_jsonable(p))))
    assert g["status"] == p["status"] == g["reading"] and "p_T_obs" not in g


def test_gt_pointwise_tau_failure_is_rule_1(lad, stages):
    fns = dict(lad["fns"])
    run = lad["run"]
    fns["reml_m2l"] = lambda L, y, C, rows, groups, t: run.reml_m2l(L, y, C, rows, groups, t) + 400.0 * (t - 0.3) ** 2
    p, _ = _gt_stage(lad, stages, "power", fns=fns, P=dict(lad["P"], gt_n_sims=3))
    assert p["status"].startswith("not evaluable (reduced-form τ̂_s differs from reml_tau on reml_m2l")
    assert "models" not in p and all(q["z_ok"] for q in p["checks"]["pointwise"])


def test_gt_cholesky_failure(lad, stages):
    """V(τ̂_N) (OANYVN, decisive) fails: rule (1); V(τ̂_obs) (VHAT, reported) fails: VHAT alone not evaluable."""
    run = lad["run"]

    def fns_failing(target):
        fns = dict(lad["fns"])

        def with_re(C, groups, tau):
            V = run.with_re(C, groups, tau)
            if abs(tau - target) < 1e-4:
                V = V.copy()
                V[0, 0] = -1.0
            return V
        fns["with_re"] = with_re
        return fns
    p, _ = _gt_stage(lad, stages, "power", fns=fns_failing(0.0314), P=dict(lad["P"], gt_n_sims=3))
    assert p["status"] == "not evaluable (the Cholesky factor of V(0.0314) failed)" and "models" not in p
    g_saved = shape.check_g_sims(_jsonable(stages["sims"]), lad["P"])
    p, _ = _gt_stage(lad, stages, "power", fns=fns_failing(lad["rec"]["tau_obs"]), P=dict(lad["P"], gt_n_sims=3),
                     g_saved=g_saved)
    assert p["models"]["VHAT"]["status"].startswith("not evaluable (Cholesky factor failed")
    assert p["status"] == "evaluated" and p["checks"]["r2_re_g_simulations_reproduced"]["VHAT"]["status"].startswith(
        "not compared")


def test_gt_sims_files_below_1_mb():
    from astrolab.results import write_json
    import tempfile
    rng = np.random.default_rng(0)
    n = 10_000
    arr = {"G": rng.uniform(0.05, 0.9, n), "tau": rng.uniform(0, 0.4, n), "k": rng.integers(0, 20_000, n),
           "j": rng.integers(0, 37, n)}
    P = {"g_seed_base": 400_000, "gt_n_inner": 20_000, "g_inner_seed": 600_000, "gt_inner_seed": 610_000,
         "g_host_seed_base": 500_000, "gt_seed_base": 410_000, "gt_nu": 4}
    rec = shape.gt_sims_file("OANY", {"offset": "any", "tau_t": None}, arr, P, rng.integers(0, 37, n))
    with tempfile.TemporaryDirectory() as d:
        p = write_json(Path(d) / "x.json", rec)
        assert p.stat().st_size < 1_000_000, p.stat().st_size


# ---------------------------------------------------------------- run.main in the R2-RE-GT standalone mode
def _main_gt(tmp_path, monkeypatch, name, lad, stages, stage, summary=True):
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
    g_sims = _jsonable(stages["sims"])
    monkeypatch.setattr(run, "recorded_g_sims", lambda P: (shape.check_g_sims(g_sims, P), shape.thread_settings()))
    for k, v in (("gt_only", True), ("gt_check", True), ("gt_stage", stage), ("gt_n_sims", N_SIMS),
                 ("g_n_sims", N_SIMS)):
        monkeypatch.setitem(run.PARAMS, k, v)
    real = run.run_gt
    rec = _gt_rec(lad, stages)

    def stub(ctx, P, L_, y_, C_, nz, cls, rows_a, col_host, ident, stage_, grid, g_saved, power_rec=None,
             grid_source=None, recorded=None):
        labels = list(lad["labels"])
        return real(ctx, P, L_, y_, C_, nz, cls, rows_a, labels, dict(ident, host_step_evaluable=True), stage_, grid,
                    g_saved, power_rec=power_rec, grid_source=grid_source, recorded=rec)
    monkeypatch.setattr(run, "run_gt", stub)
    from astrolab.results import write_json
    old = {"params": {"a": 1}, "R2_RE_G": {"reading": "τ̂ x"}, "runtime_s": 1.5}
    if summary:
        write_json(tmp_path / "summary.json", old)
    return run, _Ctx(tmp_path), old


def test_main_gt_only_power_then_full(tmp_path, monkeypatch, lad, stages):
    run, ctx, old = _main_gt(tmp_path, monkeypatch, "run003_gtonly_p", lad, stages, "power")
    run.main(ctx)
    assert ctx.record_suffix == "_gtp" and set(ctx.saved) == {"r2_re_gt_power"}
    p = ctx.saved["r2_re_gt_power"]
    assert p["status"] == "evaluated" and "p_T_obs" not in json.dumps(_jsonable(p))
    line = shape.gt_power_log_line(json.loads((tmp_path / "r2_re_gt_power.json").read_text(encoding="utf-8")))
    assert line in ctx.logs and "(committed file, standalone mode)" in p["settings"]["reml_grid_source"]
    run2, ctx2, _ = _main_gt(tmp_path, monkeypatch, "run003_gtonly_f", lad, stages, "full", summary=False)
    monkeypatch.setattr(run2, "study_log_text", lambda: "# log\n- " + line + "\n")
    ret = run2.main(ctx2)
    assert ctx2.record_suffix == "_gt"
    assert set(ctx2.saved) == {"r2_re_gt", "summary"} | {f"r2_re_gt_sims_{k}" for k in GT_SIM_KEYS}
    g = ctx2.saved["r2_re_gt"]
    assert g["checks"]["power_stage_counts_reproduced"] and g["n_sims"] == p["n_sims"] and "p_T_obs" in g
    s = ctx2.saved["summary"]
    assert list(s) == ["params", "R2_RE_G", "R2_RE_GT", "runtime_s"] and ret == s
    assert all(s[k] == old[k] for k in old) and s["R2_RE_GT"] == shape.gt_summary(g)


def test_main_gt_only_refusals_before_loading(tmp_path, monkeypatch, lad, stages):
    """The formal gt_only full stage reads the power record before loading any data and refuses a missing power
    line, other settings, a stub, a rerun without a reason, and thread settings other than R2-RE-G's; an
    exploration may run only the power stage until the formal r2_re_gt.json exists."""
    run, ctx, _ = _main_gt(tmp_path, monkeypatch, "run003_gtonly_c0", lad, stages, "power")
    run.main(ctx)
    p = json.loads((tmp_path / "r2_re_gt_power.json").read_text(encoding="utf-8"))
    from astrolab.results import write_json
    run2, ctx2, _ = _main_gt(tmp_path, monkeypatch, "run003_gtonly_c1", lad, stages, "full", summary=False)
    monkeypatch.setattr(run2, "load", lambda ctx: pytest.fail("data loaded"))
    monkeypatch.setattr(run2, "study_log_text", lambda: "nothing here")
    with pytest.raises(RuntimeError, match="not present in log.md"):
        run2.main(ctx2)
    monkeypatch.setattr(run2, "study_log_text", lambda: shape.gt_power_log_line(p) + "\nrerun: fixed x\n")
    write_json(tmp_path / "r2_re_gt_power.json", dict(p, settings=dict(p["settings"], gt_inner_seed=1)))
    with pytest.raises(RuntimeError, match="gt_inner_seed"):
        run2.main(ctx2)
    stub, _ = run2.gt_not_run(run2.PARAMS, "not run (PARAMS)", "power")
    write_json(tmp_path / "r2_re_gt_power.json", stub)
    with pytest.raises(RuntimeError, match="stub"):
        run2.main(ctx2)
    write_json(tmp_path / "r2_re_gt_power.json", p)
    write_json(tmp_path / "r2_re_gt.json", {"stage": "full", "status": "not evaluable (x)", "settings": {}})
    for why in ("", "not in the log"):
        monkeypatch.setitem(run2.PARAMS, "gt_rerun_reason", why)
        with pytest.raises(RuntimeError, match="gt_rerun_reason"):
            run2.main(ctx2)
    monkeypatch.setitem(run2.PARAMS, "gt_rerun_reason", "rerun: fixed x")
    with pytest.raises(pytest.fail.Exception, match="data loaded"):     # past every gate
        run2.main(ctx2)
    # other thread settings than R2-RE-G's formal run: refused (its saved simulations would not reproduce exactly)
    monkeypatch.setattr(run2, "recorded_g_sims", lambda P: (shape.check_g_sims(_jsonable(stages["sims"]), P),
                                                            {"env": {"OMP_NUM_THREADS": "8"}, "threadpools": []}))
    with pytest.raises(RuntimeError, match="thread settings differ from R2-RE-G"):
        run2.main(ctx2)
    assert set(ctx2.saved) == set()
    # an exploration: the full stage is refused before loading until the formal r2_re_gt.json exists
    (tmp_path / "x").mkdir()
    run3, ctx3, _ = _main_gt(tmp_path / "x", monkeypatch, "run003_gtonly_x", lad, stages, "full", summary=False)
    monkeypatch.setattr(run3, "formal_gt_done", lambda: False)
    monkeypatch.setattr(run3, "load", lambda ctx: pytest.fail("data loaded"))
    ctx3.max_save_bytes = 1024 ** 2
    with pytest.raises(RuntimeError, match="only gt_stage = 'power'"):
        run3.main(ctx3)
    # gt_check outside gt_only before the formal run, and the mode combinations
    monkeypatch.setitem(run3.PARAMS, "gt_only", False)
    with pytest.raises(RuntimeError, match="would compute p_T on the data"):
        run3.main(ctx3)
    monkeypatch.setitem(run3.PARAMS, "gt_only", True)
    monkeypatch.setitem(run3.PARAMS, "g_only", True)
    with pytest.raises(ValueError, match="gt_only cannot be combined"):
        run3.main(ctx3)
    monkeypatch.setitem(run3.PARAMS, "g_only", False)
    monkeypatch.setitem(run3.PARAMS, "gt_check", False)
    with pytest.raises(ValueError, match="gt_only needs gt_check"):
        run3.main(ctx3)
    monkeypatch.setitem(run3.PARAMS, "gt_check", True)
    monkeypatch.setitem(run3.PARAMS, "gt_stage", "both")
    with pytest.raises(ValueError, match="gt_stage"):
        run3.main(ctx3)
    assert ctx3.saved == {}


def test_main_gt_only_exploration_runs_both_stages(tmp_path, monkeypatch, lad, stages):
    run, ctx, _ = _main_gt(tmp_path, monkeypatch, "run003_gtonly_e", lad, stages, "full", summary=False)
    monkeypatch.setattr(run, "formal_gt_done", lambda: True)
    ctx.max_save_bytes = 1024 ** 2
    run.main(ctx)
    assert list(ctx.saved)[0] == "r2_re_gt_power"
    assert set(ctx.saved) == {"r2_re_gt_power", "r2_re_gt", "summary"} | {f"r2_re_gt_sims_{k}" for k in GT_SIM_KEYS}
    assert ctx.saved["summary"] == {"R2_RE_GT": shape.gt_summary(ctx.saved["r2_re_gt"])}


def test_gt_check_false_full_run_keeps_formal_files(tmp_path):
    run = _load("run003_gt_stubs", "run.py")
    from astrolab.results import write_json
    formal = {"stage": "full", "status": "evaluated", "reading": "t₄ diffuse scatter not excluded"}
    write_json(tmp_path / "r2_re_gt.json", formal)
    ctx = _Ctx(tmp_path)
    g = run.save_gt_stubs(ctx, run.PARAMS, "not run (PARAMS)")
    assert g == formal and "r2_re_gt" not in ctx.saved
    assert set(ctx.saved) == {"r2_re_gt_power"} | {f"r2_re_gt_sims_{k}" for k in GT_SIM_KEYS}
    out, sims = run.gt_not_run(run.PARAMS, "not run (PARAMS)", "full")
    assert shape.gt_summary(out) == {"status": "not run (PARAMS)", "reading": None} and set(sims) == set(GT_SIM_KEYS)


# ==== R2-RE-GTP (README section 2, addendum 2026-11-22, T-060) =====================================================
def test_gtp_params_and_seeds():
    run = _load("run003_gtp_params", "run.py")
    P = run.PARAMS
    assert (P["gtp_check"], P["gtp_only"], P["gtp_nus"], P["gtp_t_seeds"], P["gtp_inner_seeds"], P["gtp_n_sims"],
            P["gtp_rerun_reason"]) == (False, False, [3, 4, 6, 10, 30, "inf"],
                                       {3: 430_000, 6: 440_000, 10: 450_000, 30: 460_000},
                                       {6: 613_000, 30: 614_000}, 10_000, "")
    assert [shape.gtp_inner_seed(v, P) for v in (3, 4, 6, 10, 30)] == [611_000, 610_000, 613_000, 612_000, 614_000]
    assert [shape.gtp_t_seed(v, P) for v in (3, 6, 10, 30)] == [430_000, 440_000, 450_000, 460_000]
    assert [shape.gtp_nu_key(v) for v in P["gtp_nus"]] == ["3", "4", "6", "10", "30", "inf"]
    # the new seeds collide with no earlier block (R2-RE-GT's list plus 410,000-419,999 and 610,000-612,000)
    used = [(0, 0), (10_000, 11_999), (20_000, 21_999), (50_000, 50_999), (100_000, 109_999), (200_000, 209_999),
            (300_000, 300_199), (400_000, 409_999), (410_000, 419_999), (500_000, 509_999), (600_000, 600_000),
            (610_000, 612_000)]
    for lo, hi in [(430_000, 439_999), (440_000, 449_999), (450_000, 459_999), (460_000, 469_999),
                   (613_000, 613_000), (614_000, 614_000)]:
        assert all(hi < a or lo > b for a, b in used)
    assert shape.GTP_RECORDED_K == {("4", "tau_obs"): 1047, ("4", "0.05"): 501, ("4", "0.105"): 1806,
                                    ("3", "tau_obs"): 1476, ("10", "tau_obs"): 422,
                                    ("inf", "tau_obs"): 326, ("inf", "0.05"): 254, ("inf", "0.105"): 453}
    # the recorded k agree with the committed R2-RE-GT and R2-RE-G records (when present)
    res = HERE / "results"
    if (res / "r2_re_gt.json").exists() and (res / "r2_re_g.json").exists():
        gt = json.loads((res / "r2_re_gt.json").read_text(encoding="utf-8"))
        g = json.loads((res / "r2_re_g.json").read_text(encoding="utf-8"))
        if "p_T_obs" in gt and "p_G" in g:
            sens = gt["sensitivities"]
            found = {("4", "tau_obs"): gt["p_T_obs"]["k"], ("4", "0.05"): sens["fixed_tau"]["0.05"]["k"],
                     ("4", "0.105"): sens["fixed_tau"]["0.105"]["k"], ("3", "tau_obs"): sens["nu"]["3"]["k"],
                     ("10", "tau_obs"): sens["nu"]["10"]["k"], ("inf", "tau_obs"): g["p_G"]["k"],
                     ("inf", "0.05"): g["p_G_fixed"]["V050"]["k"], ("inf", "0.105"): g["p_G_fixed"]["V105"]["k"]}
            assert found == shape.GTP_RECORDED_K


def test_gtp_variance_matching_new_nu():
    """Var(b) = tau^2 for b = s t, s = tau sqrt((nu - 2) / nu): exactly in the scale, and the sample variance within
    Monte Carlo error at the new nu (6 and 30; nu = 3's is checked loosely by test_gt_variance_matching)."""
    tau = 0.08
    for nu in (3, 4, 6, 10, 30):
        assert abs(shape.gt_scale(tau, nu) ** 2 * nu / (nu - 2) - tau ** 2) < 1e-15
    for nu, seed in ((6, 613_000), (30, 614_000)):
        b = shape.gt_scale(tau, nu) * shape.t_draws(seed, nu, (40_000, 37))
        assert abs(b.var() / tau ** 2 - 1) < 0.03, (nu, b.var() / tau ** 2)


def test_gtp_statement_rule():
    E, N, U = shape.EXCL, shape.NOT_EXCL, "undetermined (Monte Carlo)"
    pre = shape.GTP_PROFILE
    assert shape.gtp_statement([E] * 18, [0.01] * 18) == pre + "excluded across the profile"
    assert shape.gtp_statement([N] * 18, [0.2] * 18) == pre + "not excluded across the profile"
    assert shape.gtp_statement([E] * 17 + [N], [0.01] * 17 + [0.2]) == pre + "model-limited (p_fix from 0.010 to 0.200)"
    # mixes with Monte Carlo-undetermined points are model-limited too; min and max over all points
    assert shape.gtp_statement([E] * 17 + [U], [0.01] * 17 + [0.05]) == pre + "model-limited (p_fix from 0.010 to 0.050)"
    assert shape.gtp_statement([N, U], [0.3, 0.05]) == pre + "model-limited (p_fix from 0.050 to 0.300)"


def test_gtp_refit_record():
    n_in = 20_000
    k_s = np.array([10] * 10 + [5000] * 90)          # 10 of 100 clearly "excluded" (k = 10 of 20,000)
    r = shape.gtp_refit_record(k_s, 1000, n_in)
    assert r["n"] == 100 and r["n_excluded"] == 10 and abs(r["size"] - 0.1) < 1e-15
    assert r["anti_conservative"] is False                 # CP interval of 10/100 contains 0.05
    assert r["p_cal"]["count"] == 10 and abs(r["p_cal"]["p"] - 11 / 101) < 1e-15
    r2 = shape.gtp_refit_record(np.array([10] * 300 + [5000] * 700), 10, n_in)
    assert r2["anti_conservative"] is True and r2["p_cal"]["count"] == 300   # ties k_s = k_obs count
    lo, hi = rob._cp(300, 1000)
    assert r2["size_ci95"] == [lo, hi] and lo > 0.05


def _gtp_inputs(lad, stages, n):
    """Synthetic reused k_s and the records they must reproduce."""
    rng = np.random.default_rng(7)
    reused = {nk: {tk: rng.integers(0, 3000, n) for tk in shape.GTP_TAU_KEYS} for nk in ("4", "inf")}
    models = {}
    for nk, keys in shape.GTP_REUSED_SETS.items():
        for tk, key in keys.items():
            r = shape.gtp_refit_record(reused[nk][tk], 0, shape_n_in())
            models[(nk, key)] = {"n": n, "n_excluded": r["n_excluded"]}
    gt_rec = {"models": {key: v for (nk, key), v in models.items() if nk == "4"}}
    g_rec = {"models": {key: v for (nk, key), v in models.items() if nk == "inf"}}
    return reused, gt_rec, g_rec


def shape_n_in():
    return 20_000


def _gtp(lad, stages, recorded=None, n=N_SIMS, reused=None, gt_rec=None, g_rec=None, log=None):
    P = dict(lad["P"], gtp_n_sims=n, gtp_nus=[3, 4, 6, 10, 30, "inf"],
             gtp_t_seeds={3: 430_000, 6: 440_000, 10: 450_000, 30: 460_000},
             gtp_inner_seeds={6: 613_000, 30: 614_000})
    r0, gt0, g0 = _gtp_inputs(lad, stages, n)
    rc = dict(lad["rec"], g_obs=stages["full"]["observed"]["G_obs"], k={})
    rc.update(recorded or {})
    return shape.run_gtp(lad["L"], lad["y"], lad["C"], lad["rows_a"], lad["groups"], lad["labels"], P, lad["fns"],
                         (lambda m: None) if log is None else log, lad["grid"],
                         gt0 if gt_rec is None else gt_rec, g0 if g_rec is None else g_rec,
                         r0 if reused is None else reused, recorded=rc)


@pytest.fixture(scope="module")
def gtp_out(lad, stages):
    return _gtp(lad, stages)


def test_gtp_synthetic_run(lad, stages, gtp_out):
    out, sims = gtp_out
    assert out["status"] == "evaluated", out["status"]
    nus = ["3", "4", "6", "10", "30", "inf"]
    assert set(out["p_fix"]) == set(nus) and all(set(out["p_fix"][a]) == set(shape.GTP_TAU_KEYS) for a in nus)
    assert set(sims) == {f"{a}_{b}" for a in ("3", "6", "10", "30") for b in shape.GTP_TAU_KEYS}
    for name, f in sims.items():
        assert len(f["k"]) == N_SIMS and len(f["G"]) == N_SIMS and len(f["tau_hat"]) == N_SIMS
    assert all(p["ok"] for p in out["checks"]["pointwise"]) and len(out["checks"]["pointwise"]) == 12 * 3
    # p_plug is p_fix at tau_obs; every refit record has its size and p_cal, computed from the k_s
    for a in nus:
        assert out["p_plug"][a] == out["p_fix"][a]["tau_obs"]["p"]
        for b in shape.GTP_TAU_KEYS:
            r = out["refit"][a][b]
            k_s = sims[f"{a}_{b}"]["k"] if a not in shape.GTP_REUSED_SETS else None
            if k_s is not None:
                assert r == shape.gtp_refit_record(k_s, out["p_fix"][a]["tau_obs"]["k"], 20_000)
    labs = [out["p_fix"][a][b]["label"] for a in nus for b in shape.GTP_TAU_KEYS]
    ps = [out["p_fix"][a][b]["p"] for a in nus for b in shape.GTP_TAU_KEYS]
    assert out["statement"] == shape.gtp_statement(labs, ps)
    assert out["p_fix_min"] == min(ps) and out["p_fix_max"] == max(ps)
    ok = [a for a in nus if a not in out["anti_conservative_nu"]]
    pc = [out["refit"][a][b]["p_cal"]["p"] for a in ok for b in shape.GTP_TAU_KEYS]
    assert out["p_cal_max"] == (max(pc) if pc else None)
    # nu = inf uses R2-RE-G's Gaussian inner draws (inner_k), nu = 4 R2-RE-GT's T_in
    des, _ = shape.design(lad["L"], lad["y"], lad["C"], lad["rows_a"], lad["groups"], lad["fns"])
    E_in = shape.inner_draws(lad["P"]["g_inner_seed"], 20_000, len(lad["groups"]))
    g = out["observed"]["G_obs"]
    assert out["p_fix"]["inf"]["0.05"]["k"] == shape.inner_k(g, 0.05, des, E_in)
    inner4 = shape.TInner(des, E_in, shape.t_draws(610_000, 4, (20_000, len(lad["groups"]))), 4)
    assert out["p_fix"]["4"]["0.105"]["k"] == inner4.k(g, 0.105)
    s = shape.gtp_summary(out)
    assert s["status"] == "evaluated" and s["statement"] == out["statement"]


def test_gtp_recorded_k_mismatch_is_not_evaluable(lad, stages, gtp_out):
    out, _ = gtp_out
    k = {("4", "0.05"): out["p_fix"]["4"]["0.05"]["k"] + 1}
    bad, sims = _gtp(lad, stages, recorded={"k": k})
    assert bad["status"].startswith("not evaluable (reproduction check failed") and sims == {}
    good, _ = _gtp(lad, stages, recorded={"k": {("4", "0.05"): out["p_fix"]["4"]["0.05"]["k"]}}, n=2)
    assert good["status"] == "evaluated"


def test_gtp_reused_count_mismatch_and_g_obs(lad, stages):
    reused, gt_rec, g_rec = _gtp_inputs(lad, stages, N_SIMS)
    gt_rec["models"]["THAT"]["n_excluded"] += 1
    bad, _ = _gtp(lad, stages, reused=reused, gt_rec=gt_rec, g_rec=g_rec)
    assert "THAT: n_excluded" in bad["status"]
    bad2, _ = _gtp(lad, stages, recorded={"g_obs": stages["full"]["observed"]["G_obs"] * 1.001}, n=2)
    assert bad2["status"].startswith("not evaluable (reproduction check failed: G_obs")


def test_main_gtp_refusals(tmp_path, monkeypatch):
    run = _load("run003_gtp_refuse", "run.py")
    ctx = _Ctx(tmp_path)
    monkeypatch.setitem(run.PARAMS, "gtp_check", True)
    with pytest.raises(ValueError, match="only standalone"):
        run.main(ctx)
    monkeypatch.setitem(run.PARAMS, "gtp_check", False)
    monkeypatch.setitem(run.PARAMS, "gtp_only", True)
    with pytest.raises(ValueError, match="gtp_only needs gtp_check"):
        run.main(ctx)
    monkeypatch.setitem(run.PARAMS, "gtp_check", True)
    monkeypatch.setitem(run.PARAMS, "gt_only", True)
    with pytest.raises(ValueError, match="cannot be combined"):
        run.main(ctx)


def test_main_gtp_exploration_before_formal(tmp_path, monkeypatch):
    run = _load("run003_gtp_explore", "run.py")
    ctx = _Ctx(tmp_path)
    ctx.max_save_bytes = 1_000_000
    monkeypatch.setattr(run, "formal_gtp_done", lambda path=None: False)
    for k, v in (("gtp_check", True), ("gtp_only", True)):
        monkeypatch.setitem(run.PARAMS, k, v)
    with pytest.raises(RuntimeError, match="only after the formal"):
        run.main(ctx)


def test_gtp_conclusion_check_on_synthetic_output(lad, stages, gtp_out):
    """test_conclusions.check_r2_re_gtp accepts the synthetic output and rejects a changed statement."""
    out, sims = gtp_out
    tc = _load("tc003_gtp", "test_conclusions.py")
    reused, _, _ = _gtp_inputs(lad, stages, N_SIMS)
    o = json.loads(json.dumps(_jsonable(out)))
    sm = json.loads(json.dumps(_jsonable(sims)))
    ru = {a: {b: [int(k) for k in v] for b, v in d.items()} for a, d in reused.items()}
    s = json.loads(json.dumps(_jsonable(shape.gtp_summary(out))))
    tc.check_r2_re_gtp(o, sm, ru, s, recorded_k={})
    bad = dict(o, statement=o["statement"] + " x")
    with pytest.raises(AssertionError):
        tc.check_r2_re_gtp(bad, sm, ru, dict(s, statement=bad["statement"]), recorded_k={})


def test_run_gtp_only_saves_and_updates_only_its_summary_key(tmp_path, monkeypatch):
    """run_gtp_only: r2_re_gtp.json, the new sims files and summary.json's R2_RE_GTP key (other keys unchanged); a
    not-evaluable outcome writes no sims files."""
    run = _load("run003_gtp_only", "run.py")
    from astrolab.results import write_json
    old = {"params": {"a": 1}, "R2_RE_GT": {"reading": "τ̂ x"}, "runtime_s": 1.5}
    write_json(tmp_path / "summary.json", old)
    old_text = (tmp_path / "summary.json").read_text(encoding="utf-8")
    monkeypatch.setattr(run, "anchor_rows", lambda nz, cls, y: (np.arange(3), None))
    monkeypatch.setattr(run, "recorded_reml_grid", lambda: [0.0])
    fake = {"stage": "full", "status": "evaluated", "statement": "t-tail comparison: model-limited (p_fix from "
            "0.010 to 0.100)", "p_fix_min": 0.01, "p_fix_max": 0.1, "p_cal_min": 0.02, "p_cal_max": 0.09,
            "anti_conservative_nu": []}
    monkeypatch.setattr(run.shape, "run_gtp", lambda *a, **k: (fake, {"3_0.05": {"k": [1, 2]}}))
    ctx = _Ctx(tmp_path)
    cls = {"calib": np.zeros(3, dtype=bool)}
    new = run.run_gtp_only(ctx, run.PARAMS, None, np.zeros(3), None, np.zeros((3, run.NH), dtype=bool), cls,
                           ["h"] * run.NH, {"host_step_evaluable": True}, ({}, {}, {}))
    assert set(ctx.saved) == {"r2_re_gtp", "r2_re_gtp_sims_3_0.05", "summary"}
    assert new["R2_RE_GTP"] == shape.gtp_summary(fake)
    assert list(new) == ["params", "R2_RE_GT", "R2_RE_GTP", "runtime_s"]
    assert {k: new[k] for k in old} == old
    write_json(tmp_path / "summary.json", old)
    ctx2 = _Ctx(tmp_path)
    run.run_gtp_only(ctx2, run.PARAMS, None, np.zeros(3), None, np.zeros((3, run.NH), dtype=bool), cls,
                     ["h"] * run.NH, {"host_step_evaluable": False}, ({}, {}, {}))
    assert set(ctx2.saved) == {"r2_re_gtp", "summary"}
    assert ctx2.saved["r2_re_gtp"]["status"] == "not evaluable (host step not evaluable)"
    assert (tmp_path / "summary.json").read_text(encoding="utf-8") != old_text
