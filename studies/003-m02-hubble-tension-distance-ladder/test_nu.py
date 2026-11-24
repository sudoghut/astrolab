"""Offline tests of R2-RE-NU (README section 2, addendum 2026-11-24, T-062) on synthetic data only (no real Hubble-flow
row of y is used anywhere): g(D) against direct REML; the importance sampler (same defensive estimator and
diagnostics) against per-SN quadrature of the Gaussian-t convolution and, at nu = 1e6, the Gaussian closed form; the
k_hat estimator against generalized Pareto samples; the variance matching and the heteroscedastic scaling; the
grouping and its count check; the truncation by whole-mock rejection; the usecols read of Pantheon+SH0ES.dat; the 1/nu
weights; the gate, the label order, the scale condition, the pass rule and the p_int arithmetic; the check record
without L(nu), weights, label or p_int; the checks that give label 1; the escalation; the two stages and their
refusals; and the run path end to end with a fake ctx (run.main in the nu_only mode)."""
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np
import pytest
from scipy import integrate, linalg, special, stats

HERE = Path(__file__).parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import nu  # noqa: E402
import shape  # noqa: E402

GRID = np.round(np.arange(0.0, 0.5 + 0.005, 0.01), 10)


def _load(name, file="run.py"):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------- synthetic inputs
def _system(run, tau_hf=0.15, n_sn=30, seed=5, tau_host=0.05, dup_every=4, rho_dup=0.6, rho_cross=0.1, sig_hf=0.10):
    """A small ladder with run.py's column layout (37 hosts, NGC 4258, LMC and MW rows that anchor_rows removes) and
    Hubble-flow rows with Gaussian per-SN effects; every dup_every-th SN has two light curves correlated at rho_dup, and
    six Hubble-flow rows are weakly correlated with calibrator SN rows (as C's SN block). Returns (L, y, C)."""
    rng = np.random.default_rng(seed)
    rows, mean, sig = [], [], []
    mu = rng.uniform(30.5, 33.0, run.NH)
    m_h, m_b, q = -5.9, -19.25, 9.32
    u_host = rng.normal(0.0, tau_host, run.NH)

    def add(cols, val, s):
        r = np.zeros(run.N_PAR)
        for c, v in cols:
            r[c] = v
        rows.append(r)
        mean.append(val)
        sig.append(s)

    calib = []
    for j in range(run.NH):
        for _ in range(4):
            add([(j, 1), (run.C_MH, 1)], mu[j] + m_h, 0.08)
        for _ in range(1 + (j % 3 == 0)):
            calib.append(len(rows))
            add([(j, 1), (run.C_MB, 1)], mu[j] + m_b + u_host[j], 0.05)
    for _ in range(6):
        add([(run.C_N4258, 1), (run.C_MH, 1)], 29.4 + m_h, 0.08)
    add([(run.C_N4258, 1)], 0.0, 0.03)
    maser = len(rows) - 1
    b = rng.normal(0.0, tau_hf, n_sn)
    pairs, hf = [], []
    for k in range(n_sn):
        n_lc = 2 if k % dup_every == 0 else 1
        first = len(rows)
        for _ in range(n_lc):
            hf.append(len(rows))
            add([(run.C_MB, 1), (run.C_H0, -1)], m_b - q + b[k], sig_hf)
        if n_lc == 2:
            pairs.append((first, first + 1))
    n = len(rows)
    sig = np.array(sig)
    C = np.diag(sig ** 2)
    for a, c in pairs:
        C[a, c] = C[c, a] = rho_dup * sig[a] * sig[c]
    for i, h in enumerate(hf[:6]):
        k = calib[i]
        C[h, k] = C[k, h] = rho_cross * sig[h] * sig[k]
    L = np.array(rows)
    y = np.array(mean) + np.linalg.cholesky(C) @ rng.standard_normal(n)
    y[maser] = 0.0
    for c, val in ((run.C_LMC, 0.0), (run.C_MH, -5.85), (run.C_MH, -5.80)):
        r = np.zeros(run.N_PAR)
        r[c] = 1.0
        L = np.vstack([L, r])
        y = np.append(y, val)
        C = np.pad(C, ((0, 1), (0, 1)))
        C[-1, -1] = 0.03 ** 2
    return L, y, C


def _pantheon_text(n_cid, n_extra=5):
    """A Pantheon+SH0ES.dat stand-in whose other columns hold text a numeric parse would reject."""
    lines = ["CID IDSURVEY zHD m_b_corr m_b_corr_err_DIAG USED_IN_SH0ES_HF"]
    for k in range(n_cid):
        for _ in range(1 + (k % 5 == 0)):
            lines.append(f"sn{k:04d} x y z w 1")
    for k in range(n_extra):
        lines.append(f"cal{k:03d} x y z w 0")
    return "\n".join(lines) + "\n"


SMALL = {"nu_n_is": 200, "nu_n_is_escalate": 300, "nu_n_mocks": 4, "nu_n_is_mock": 100, "nu_profile_m": [0.5, 1, 2]}


def _fns(run):
    return {"reml_tau": run.reml_tau, "reml_m2l": run.reml_m2l, "fit": run.fit, "with_re": run.with_re,
            "is_fit_failure": run.is_fit_failure}


def _build(name, **kw):
    run = _load(name)
    L, y, C = _system(run, **kw)
    run.N_ROWS = len(y)
    nz, cls, _ = run.row_classes(L, y)
    rows_a, _ = run.anchor_rows(nz, cls, y)
    hf = np.flatnonzero(cls["hflow"])
    calib = [np.flatnonzero(cls["calib"] & nz[:, j]) for j in range(run.NH)]
    fns = _fns(run)
    grid = [run.reml_m2l(L, y, C, rows_a, calib, t) for t in GRID]
    est = run.reml_tau(lambda t: run.reml_m2l(L, y, C, rows_a, calib, t), 0.5, 0.01, interval=False)
    groups = nu.hf_groups(C, hf, 0.3)
    P = dict(run.PARAMS, **SMALL)
    return dict(run=run, L=L, y=y, C=C, nz=nz, cls=cls, rows_a=rows_a, hf=hf, calib=calib, fns=fns, grid=grid,
                rec={"tau_obs": est["tau_hat"]}, exp={"n_hf": len(hf), "n_rows_a": len(rows_a)}, groups=groups,
                cid={"n_cid": len(groups)}, P=P)


@pytest.fixture(scope="module")
def lad():
    return _build("run003_nu")


def _des(lad, groups=None, Cb=None):
    des, problem = nu.hf_design(lad["L"], lad["y"], lad["C"] if Cb is None else Cb, lad["rows_a"],
                                lad["groups"] if groups is None else groups, lad["fns"])
    assert problem is None, problem
    return des


GTP = {"status": "evaluated", "refit": {k: {"tau_obs": {"p_cal": {"p": v}}} for k, v in nu.P_CAL_README.items()},
       "p_cal_max_over_tau": dict(nu.P_CAL_MAX_README)}


def _open_rules(mp):
    """The known-answer rules cannot be met with four mocks: opened for the run-path tests (pass_rule and trunc_rule
    are tested on their own)."""
    mp.setattr(nu, "DELTA_B_MIN", -1.0)
    real = nu.trunc_rule
    mp.setattr(nu, "trunc_rule", lambda *a: (True, real(*a)[1]))


def _open_mc(mp):
    """The accuracy check cannot be met with 200 draws: opened where the label path is tested."""
    mp.setattr(nu, "ESS_MIN", 0)
    mp.setattr(nu, "KHAT_MAX", float("inf"))
    mp.setattr(nu, "STREAM_DIFF_MAX", float("inf"))


def _check(lad, log=None, **kw):
    return nu.run_check(lad["L"], lad["y"], lad["C"], lad["rows_a"], lad["hf"], lad["calib"], dict(lad["P"], **kw),
                        lad["fns"], log or (lambda m: None), lad["grid"], lad["cid"], recorded=lad["rec"],
                        expected=lad["exp"])


def _full(lad, check_rec, log=None, gtp=GTP, **kw):
    return nu.run_full(lad["L"], lad["y"], lad["C"], lad["rows_a"], lad["hf"], lad["calib"], dict(lad["P"], **kw),
                       lad["fns"], log or (lambda m: None), lad["grid"], lad["cid"], nu.json_like(check_rec), gtp,
                       recorded=lad["rec"], expected=lad["exp"])


@pytest.fixture(scope="module")
def stages(lad):
    with pytest.MonkeyPatch.context() as mp:
        _open_rules(mp)
        _open_mc(mp)
        chk = _check(lad)
        full = _full(lad, chk)
    return {"check": chk, "full": full}


# ---------------------------------------------------------------- settings
def test_params_preregistered_and_seed_ranges():
    run = _load("run003_nu_params")
    P = run.PARAMS
    assert (P["nu_check"], P["nu_only"], P["nu_stage"], P["nu_rerun_reason"]) == (False, False, "check", "")
    assert nu.preregistered_problems(P) == []
    assert {k: P[k] for k in nu.PREREGISTERED} == nu.PREREGISTERED
    seeds = P["nu_mock_seeds"]
    used = [P["nu_is_seed"] + 10 * j + r for j in range(5) for r in range(2)]
    used += [P["nu_is_seed_escalate"] + 10 * j + r for j in range(5) for r in range(2)]
    used += [P["nu_profile_seed"] + 100 * k + 10 * j + r for k in range(4) for j in range(5) for r in range(2)]
    used += [P[k] + 10 * j + r for k in ("nu_vbase_seed", "nu_group_sens_seed") for j in range(5) for r in range(2)]
    used += [seeds[k] + s for k in ("eps", "t3", "t10", "het") for s in range(200)]
    used += [seeds["is_" + k] + 10 * s + j for k in ("t3", "t10", "het", "trunc") for s in range(200) for j in range(5)]
    used += [seeds["trunc_joint"] + 1000 * s + k for s in range(200) for k in range(1, 100)]
    assert len(used) == len(set(used))           # no seed used twice
    ok = lambda v: 700_000 <= v <= 789_999 or 800_000 <= v <= 839_999 or 1_000_000 <= v <= 1_199_099
    assert all(ok(v) for v in used)
    for lo, hi in ((430_000, 469_999), (613_000, 613_000), (614_000, 614_000), (400_000, 409_999),
                   (600_000, 612_000)):
        assert not any(lo <= v <= hi for v in used)


def test_inv_nu_weights():
    assert np.allclose(nu.inv_nu_prior(), nu.PRIOR_INV_NU, atol=1e-12)
    assert abs(sum(nu.PRIOR_INV_NU) - 1.0) < 1e-12
    assert abs(nu.PRIOR_INV_NU[0] + nu.PRIOR_INV_NU[1] - 0.375) < 1e-12


# ---------------------------------------------------------------- grouping and the count check
def test_grouping_connected_components():
    sig = np.array([0.1, 0.2, 0.1, 0.15, 0.1, 0.1])
    R = np.eye(6)
    R[0, 1] = R[1, 0] = 0.5          # 0-1-2 a chain at 0.3; at 0.45 only 0-1
    R[1, 2] = R[2, 1] = 0.4
    R[4, 5] = R[5, 4] = 0.29         # below 0.3: separate
    C = R * np.outer(sig, sig)
    Cfull = np.pad(C, ((2, 0), (2, 0)))
    Cfull[0, 0] = Cfull[1, 1] = 1.0
    hf = np.arange(2, 8)
    g = nu.hf_groups(Cfull, hf, 0.3)
    assert [x.tolist() for x in g] == [[2, 3, 4], [5], [6], [7]]
    g45 = nu.hf_groups(Cfull, hf, 0.45)
    assert [x.tolist() for x in g45] == [[2, 3], [4], [5], [6], [7]]


def test_count_check_main_only():
    assert nu.count_check(242, 238)["ok"] and nu.count_check(242, 238)["tolerance"] == 11
    assert nu.count_check(249, 238)["ok"] and not nu.count_check(250, 238)["ok"]
    assert nu.count_check(227, 238)["ok"] and not nu.count_check(226, 238)["ok"]


def test_count_check_failure_is_label_1(lad):
    rec = nu.run_check(lad["L"], lad["y"], lad["C"], lad["rows_a"], lad["hf"], lad["calib"], lad["P"], lad["fns"],
                       lambda m: None, lad["grid"], {"n_cid": len(lad["groups"]) + 5}, recorded=lad["rec"],
                       expected=lad["exp"])
    assert rec["outcome"] == "ν not evaluable (grouping count check)"
    assert "stage1" not in rec and rec["checks"]["grouping"]["count_check"]["ok"] is False


def test_pantheon_read_uses_only_cid_and_used_columns(tmp_path):
    p = tmp_path / "Pantheon+SH0ES.dat"
    p.write_text(_pantheon_text(12), encoding="utf-8")
    calls = []
    import pandas as pd

    def spy(path, **kw):
        calls.append(kw)
        return pd.read_csv(path, **kw)
    out = nu.read_hf_cid_count(p, read_csv=spy)
    assert len(calls) == 1 and calls[0]["usecols"] == ["CID", "USED_IN_SH0ES_HF"]
    assert set(calls[0]) == {"sep", "usecols", "dtype"}
    assert out == {"n_rows_used": 12 + 3, "n_cid": 12, "columns_read": ["CID", "USED_IN_SH0ES_HF"]}
    assert nu.read_hf_cid_count(p) == out                   # the default reader, same columns
    # a reader that returned another column is refused
    with pytest.raises(RuntimeError, match="columns"):
        nu.read_hf_cid_count(p, read_csv=lambda path, **kw: pd.read_csv(path, sep=r"\s+",
                                                                         usecols=["CID", "zHD", "USED_IN_SH0ES_HF"]))


# ---------------------------------------------------------------- the reduced form
def _m2l_direct(X, ya, V):
    cf = linalg.cho_factor(V, lower=True)
    F = X.T @ linalg.cho_solve(cf, X)
    cfF = linalg.cho_factor(F, lower=True)
    q = linalg.cho_solve(cfF, X.T @ linalg.cho_solve(cf, ya))
    r = ya - X @ q
    return (2 * np.sum(np.log(np.diag(cf[0]))) + 2 * np.sum(np.log(np.diag(cfF[0])))
            + r @ linalg.cho_solve(cf, r))


def test_g_of_d_against_direct_reml_random_d(lad):
    des = _des(lad)
    assert des["n_clipped"] == 1 and des["rank_M"] == des["n_g"] - 1
    assert des["n_g"] < len(lad["hf"])                       # grouped: duplicate light curves share one b_g
    ya = lad["y"][lad["rows_a"]]
    Ca = lad["C"][np.ix_(lad["rows_a"], lad["rows_a"])]
    u = nu.u_of(lad["y"], des)
    base = _m2l_direct(des["X"], ya, Ca)
    rng = np.random.default_rng(1)
    for _ in range(4):
        d = rng.uniform(0.0, 0.08, des["n_g"]) ** 2 * rng.choice([0.1, 1, 10], des["n_g"])
        V = Ca + des["Zm"] @ np.diag(d) @ des["Zm"].T
        assert abs(nu.g_of_d(d, u, des["Mc"]) - (_m2l_direct(des["X"], ya, V) - base)) < 1e-8
    # g(tau^2 I) from the eigen-decomposition equals g_of_d and reml_m2l differences
    for t in (0.01, 0.05, 0.13):
        g1 = nu.g_iso(t, u, des)
        assert abs(g1 - nu.g_of_d(np.full(des["n_g"], t * t), u, des["Mc"])) < 1e-8
        m2l = lambda tt: lad["run"].reml_m2l(lad["L"], lad["y"], lad["C"], lad["rows_a"], lad["groups"], tt)
        assert abs(g1 - (m2l(t) - m2l(0.0))) < shape.GRID_ATOL


def test_design_rules_two_zero_eigenvalues_and_cholesky(lad):
    groups = list(lad["groups"]) + [lad["groups"][0]]       # a repeated column: a second zero eigenvalue
    des, problem = nu.hf_design(lad["L"], lad["y"], lad["C"], lad["rows_a"], groups, lad["fns"])
    assert problem.startswith("design: M has 2 zero eigenvalues")
    bad = lad["C"].copy()
    h = lad["hf"][3]
    bad[h, h] = -0.01
    rec = nu.run_check(lad["L"], lad["y"], bad, lad["rows_a"], lad["hf"], lad["calib"], lad["P"], lad["fns"],
                       lambda m: None, lad["grid"], lad["cid"], recorded=lad["rec"], expected=lad["exp"])
    assert rec["outcome"].startswith("ν not evaluable (") and "stage1" not in rec


def test_residual_maps_equal_gls_residuals(lad):
    des = _des(lad)
    rng = np.random.default_rng(3)
    eps, b = rng.standard_normal(des["n_a"]), rng.normal(0, 0.1, des["n_g"])
    e = des["K"] @ eps + des["Zm"] @ b
    Ca = lad["C"][np.ix_(lad["rows_a"], lad["rows_a"])]
    X = des["X"]
    q = np.linalg.solve(X.T @ np.linalg.solve(Ca, X), X.T @ np.linalg.solve(Ca, e))
    r = (e - X @ q)[des["hf_pos"]]
    assert np.allclose(des["R_eps"] @ eps + des["R_b"] @ b, r, atol=1e-10)
    # u_s = B eps + M b equals Z^T P (K eps + Z b)
    assert np.allclose(nu.mock_u(eps, b, des), des["PZ"].T @ e, atol=1e-9)
    assert np.allclose(des["sig_hf"], np.sqrt(np.diag(Ca))[des["hf_pos"]])


# ---------------------------------------------------------------- the importance sampler
def _factorised(n=8, seed=2, sig=0.1, tau=0.1, nu_true=3):
    """A factorised reduced form: M diagonal (single-row groups, diagonal C, no cross terms)."""
    rng = np.random.default_rng(seed)
    m = 1.0 / (sig * rng.uniform(0.8, 1.4, n)) ** 2
    b = tau * math.sqrt((nu_true - 2) / nu_true) * rng.standard_t(nu_true, n)
    u = m * b + np.sqrt(m) * rng.standard_normal(n)
    des = {"Q": np.eye(n), "lam": m, "Mc": np.diag(m), "n_g": n}
    return des, u, m


def _quad_log_lambda(nu_, tau, u, m):
    s = tau * math.sqrt((nu_ - 2) / nu_)
    out = 0.0
    for ug, mg in zip(u, m):
        f = lambda b: stats.norm.pdf(ug, mg * b, math.sqrt(mg)) * stats.t.pdf(b / s, nu_) / s
        val, _ = integrate.quad(f, -np.inf, np.inf, epsabs=0, epsrel=1e-10, limit=200)
        out += math.log(val) - stats.norm.logpdf(ug, 0.0, math.sqrt(mg))
    return out


@pytest.mark.parametrize("nu_", [3.0, 10.0])
def test_importance_sampler_against_quadrature(nu_):
    des, u, m = _factorised()
    tau = 0.1
    seeds = [11, 12]
    rec = nu.lambda_finite(nu_, tau, u, des, 4000, seeds, 0.1)
    mpost = nu.posterior_m(tau, u, des)
    lw = np.concatenate([nu.is_log_weights(nu_, tau, u, des, mpost, 4000, s, 0.1) for s in seeds])
    w = np.exp(lw - lw.max())
    se = float(np.std(w) / (np.mean(w) * math.sqrt(len(w))))
    assert abs(rec["log_lambda"] - (special.logsumexp(lw) - math.log(len(lw)))) < 1e-12
    exact = _quad_log_lambda(nu_, tau, u, m)
    assert abs(rec["log_lambda"] - exact) <= 3 * se, (rec["log_lambda"], exact, se)
    assert rec["ok"], rec["problems"]
    assert all(st["ess"] >= nu.ESS_MIN and st["khat"] < nu.KHAT_MAX for st in rec["streams"])


def test_nu_1e6_against_gaussian_closed_form():
    des, u, m = _factorised(nu_true=30)
    tau = 0.1
    rec = nu.lambda_finite(1e6, tau, u, des, 2000, [5, 6], 0.1)
    exact = nu.lambda_inf(tau, u, des)
    direct = float(np.sum(-0.5 * (np.log1p(tau ** 2 * m) - tau ** 2 * u ** 2 / (1 + tau ** 2 * m))))
    assert abs(exact - direct) < 1e-10
    assert abs(rec["log_lambda"] - exact) < 1e-3 and rec["ok"]


def test_proposal_draw_order():
    """Indicators for all N x n_g coordinates, then the prior-component Gammas, then the posterior-component Gammas,
    each in row-major order, from one default_rng(seed)."""
    m = np.array([50.0, 80.0, 120.0])
    s2, nu_, n, seed, q = 0.01, 4.0, 7, 123, 0.1
    w, lp, lq = nu.proposal_draws(nu_, s2, m, n, seed, q)
    rng = np.random.default_rng(seed)
    ind = rng.random((n, 3)) < q
    exp = np.empty((n, 3))
    g0 = rng.gamma(nu_ / 2, 2 / nu_, size=int(ind.sum()))
    r1 = (nu_ + m / s2) / 2
    g1 = [rng.gamma((nu_ + 1) / 2, 1 / r1[c]) for c in np.nonzero(~ind)[1]]
    exp[ind] = g0
    # numpy draws an array of scales element by element in order: the same stream as one call
    rng2 = np.random.default_rng(seed)
    rng2.random((n, 3))
    rng2.gamma(nu_ / 2, 2 / nu_, size=int(ind.sum()))
    exp[~ind] = rng2.gamma((nu_ + 1) / 2, 1 / r1[np.nonzero(~ind)[1]])
    assert np.array_equal(w, exp)
    assert np.allclose(exp[~ind], g1)
    # the log densities: prior Gamma(nu/2, rate nu/2), mixture q prior + (1 - q) posterior component
    assert np.allclose(lp, stats.gamma.logpdf(w, nu_ / 2, scale=2 / nu_))
    mix = q * stats.gamma.pdf(w, nu_ / 2, scale=2 / nu_) + (1 - q) * stats.gamma.pdf(w, (nu_ + 1) / 2,
                                                                                     scale=1 / r1[None, :])
    assert np.allclose(lq, np.log(mix))


@pytest.mark.parametrize("k", [0.2, 0.5, 0.9])
def test_khat_against_generalized_pareto(k):
    x = np.sort(stats.genpareto.rvs(k, scale=1.3, size=2000, random_state=np.random.default_rng(int(k * 10))))
    kh, sigma = nu.gpd_fit(x)
    assert abs(kh - k) < 0.12, (kh, k)
    # psis_khat on log weights whose upper tail is that Pareto
    lw = np.log(stats.genpareto.rvs(k, scale=1.0, size=4000, random_state=np.random.default_rng(7)) + 1.0)
    assert abs(nu.psis_khat(lw) - k) < 0.2
    assert nu.psis_khat(np.zeros(100)) == float("inf")      # no tail beyond the cutoff


def test_variance_matching_and_heteroscedastic_scaling():
    tau = 0.05
    for nu_ in (6, 10, 30):
        b = math.sqrt(nu.t_scale2(tau, nu_)) * np.random.default_rng(nu_).standard_t(nu_, 400_000)
        assert abs(np.var(b) / tau ** 2 - 1) < 0.03
    assert abs(nu.t_scale2(tau, 4) - tau ** 2 / 2) < 1e-15
    c = np.array([0.01, 0.02, 0.05, 0.015])
    d = nu.het_d(tau, c)
    assert abs(np.mean(d) - tau ** 2) < 1e-15 and np.allclose(d / c, d[0] / c[0])


# ---------------------------------------------------------------- mocks
def test_common_eps_and_mock_seeds(lad):
    des = _des(lad)
    P = lad["P"]
    seeds = P["nu_mock_seeds"]
    tau = 0.12
    rec = {k: nu.run_mocks(k, [0, 1], tau, des, P, lad["fns"]["reml_tau"]) for k in ("t3", "t10", "het")}
    for kind in ("t3", "t10", "het"):
        eps = np.random.default_rng(700_000 + 1).standard_normal(des["n_a"])
        b = nu.mock_b(kind, 1, tau, des, seeds)
        u = des["B"] @ eps + des["M"] @ b
        r = nu.mock_eval(u, des, P["nu_n_is_mock"], seeds["is_" + kind], 1, 0.1, lad["fns"]["reml_tau"])
        assert rec[kind]["tau_hat"][1] == r["tau_hat"] and rec[kind]["P"][1] == r["P"]
    t3 = np.random.default_rng(710_001).standard_t(3, des["n_g"]) * tau * math.sqrt(1 / 3)
    assert np.allclose(nu.mock_b("t3", 1, tau, des, seeds), t3, rtol=1e-13, atol=0)
    t10 = np.random.default_rng(720_001).standard_t(10, des["n_g"]) * tau * math.sqrt(0.8)
    assert np.allclose(nu.mock_b("t10", 1, tau, des, seeds), t10, rtol=1e-13, atol=0)
    het = np.random.default_rng(780_001).standard_normal(des["n_g"]) * np.sqrt(nu.het_d(tau, des["c_g"]))
    assert np.array_equal(nu.mock_b("het", 1, tau, des, seeds), het)


def test_mock_zero_tau_gives_one_third(lad):
    des = _des(lad)
    r = nu.mock_eval(np.zeros(des["n_g"]), des, 100, 750_000, 0, 0.1, lad["fns"]["reml_tau"])
    assert r["P"] == 1 / 3 and r["ess"] == [None] * 5 and r["at_zero"]


def test_truncation_whole_mock_rejection(lad):
    des = _des(lad)
    seeds = lad["P"]["nu_mock_seeds"]
    tau = 0.12
    # attempt 0 is the plain t_3 mock when it passes
    eps0 = np.random.default_rng(700_000 + 2).standard_normal(des["n_a"])
    b0 = nu.mock_b("t3", 2, tau, des, seeds)
    eps, b, k = nu.trunc_draw(2, tau, des, seeds, 50.0, 100)
    assert k == 0 and np.array_equal(eps, eps0) and np.array_equal(b, b0)
    # with a tight cut: the first passing attempt k >= 1 draws eps then t from default_rng(1e6 + 1000 s + k)
    cut = 2.2
    found = None
    for s in range(30):
        eps, b, k = nu.trunc_draw(s, tau, des, seeds, cut, 100)
        if k is not None and k >= 1:
            found = (s, eps, b, k)
            break
    assert found is not None
    s, eps, b, k = found
    rng = np.random.default_rng(1_000_000 + 1000 * s + k)
    e2 = rng.standard_normal(des["n_a"])
    assert np.array_equal(eps, e2) and np.allclose(b, tau * math.sqrt(1 / 3) * rng.standard_t(3, des["n_g"]),
                                                   rtol=1e-13, atol=0)
    r = des["R_eps"] @ eps + des["R_b"] @ b
    assert np.all(np.abs(r) <= cut * des["sig_hf"])
    for kk in range(1, k):                                  # the earlier attempts failed the cut
        rng = np.random.default_rng(1_000_000 + 1000 * s + kk)
        e_, b_ = rng.standard_normal(des["n_a"]), tau * math.sqrt(1 / 3) * rng.standard_t(3, des["n_g"])
        assert not nu.passes_cut(e_, b_, des, cut)
    # the attempt limit and the "truncation failed" count
    assert nu.trunc_draw(0, tau, des, seeds, 1e-6, 3) == (None, None, None)
    P = dict(lad["P"], nu_cut_sigma=1e-6, nu_cut_attempts=2)
    rec = nu.run_mocks("trunc", [0, 1, 2], tau, des, P, lad["fns"]["reml_tau"])
    assert rec["failed"] == [0, 1, 2] and rec["s"] == []
    ms = nu.mock_summary(rec, 0.02, 2)
    assert ms["n_failed"] == 3 and ms["n_rejected_attempts"] == 6


# ---------------------------------------------------------------- rules (pure)
def _est(tau, lo, hi, bound=False):
    return {"tau_hat": tau, "interval_68": [lo, hi], "at_upper_bound": bound}


def test_gate_and_label_1_order():
    assert nu.gate(_est(0.49, 0.3, "> 0.5", True), 0.02)[0] == "ν not evaluable (bound)"
    assert nu.gate(_est(0.05, "not determined", 0.1), 0.02)[0].startswith("ν not evaluable (τ̂_HF interval")
    assert nu.gate(_est(0.05, 0.0, 0.1), 0.02)[0] == nu.LBL_NO_EXCESS
    assert nu.gate(_est(0.0199, 0.01, 0.03), 0.02)[0] == nu.LBL_NO_EXCESS
    assert nu.gate(_est(0.0, 0.0, 0.02), 0.02)[0] == nu.LBL_NO_EXCESS
    assert nu.gate(_est(0.02, 0.005, 0.03), 0.02) == (None, "passed")


def test_scale_condition_and_labels():
    assert nu.scale_inside([0.05, 0.08]) is True and nu.scale_inside([0.03, 0.07]) is False
    assert nu.scale_inside([0.08, 0.2]) is False and nu.scale_inside([0.05, "> 0.5"]) is True
    # README amendment 2 (2026-11-24): an undetermined upper end counts as open, [lower end, inf)
    assert nu.scale_inside([0.05, "not determined"]) is True and nu.scale_inside([0.09, "not determined"]) is False
    c = nu.COND
    assert nu.label_from_p(0.049, True) == (nu.LBL_LIGHT + c, False)
    assert nu.label_from_p(0.951, True) == (nu.LBL_HEAVY + c, False)
    assert nu.label_from_p(0.049, False) == (nu.LBL_LIGHT + c + nu.SCALE_SUFFIX, True)
    assert nu.label_from_p(0.96, False) == (nu.LBL_HEAVY + c + nu.SCALE_SUFFIX, True)
    assert nu.label_from_p(0.05, False) == (nu.LBL_WEAK + c, False)      # no scale suffix under label 6
    assert nu.label_from_p(0.95, True) == (nu.LBL_WEAK + c, False)
    assert nu.LBL_LIGHT == "ν constrained to the light-tail side (P(ν ≤ 4) < 0.05)"
    assert nu.LBL_HEAVY == "ν constrained to the heavy-tail side (P(ν ≤ 4) > 0.95)"


def test_pass_rule_a_to_e():
    ok, parts, rec = nu.pass_rule([0.5] * 200, [0.3] * 200, [0.4] * 200)
    assert ok and parts == [] and abs(rec["delta_b"] - 0.2) < 1e-12
    t3 = [0.01] * 11 + [0.6] * 189
    assert nu.pass_rule(t3, [0.3] * 200, [0.4] * 200)[1] == ["mislabels"]
    assert nu.pass_rule([0.01] * 10 + [0.6] * 190, [0.3] * 200, [0.4] * 200)[0]
    assert nu.pass_rule([0.5] * 200, [0.96] * 11 + [0.2] * 189, [0.4] * 200)[1] == ["mislabels"]
    assert nu.pass_rule([0.4] * 200, [0.31] * 200, [0.4] * 200)[1] == ["no power at this τ_HF"]
    assert nu.pass_rule([0.5] * 200, [0.3] * 200, [0.96] * 11 + [0.4] * 189)[1] == ["heteroscedasticity"]
    assert nu.pass_rule([0.32] * 200, [0.96] * 11 + [0.3] * 189, [0.99] * 200)[1] == [
        "mislabels", "no power at this τ_HF", "heteroscedasticity"]
    ok, rec = nu.trunc_rule([0.45] * 190, [0.5] * 200, 0.2, 10)
    assert ok and rec["d"] and rec["e"] and rec["failed_ok"]
    assert not nu.trunc_rule([0.25] * 190, [0.5] * 200, 0.2, 0)[0]          # (d)
    assert not nu.trunc_rule([0.01] * 11 + [0.5] * 179, [0.5] * 200, 0.2, 0)[0]   # (e)
    assert not nu.trunc_rule([0.5] * 189, [0.5] * 200, 0.2, 11)[0]         # more than 10 failed


def test_p_int_arithmetic_from_recorded_keys():
    gtp = json.loads((HERE / "results" / "r2_re_gtp.json").read_text(encoding="utf-8"))
    pc, pm = nu.gtp_p_cal(gtp)
    flat = nu.p_int_block(nu.PRIOR_FLAT, nu.PRIOR_INV_NU, pc, pm)
    assert round(flat["prior_only"]["primary"], 4) == 0.0352 and round(flat["prior_only"]["inv_nu"], 4) == 0.0364
    assert round(flat["prior_only"]["bound"], 4) == 0.0359 and round(flat["prior_only"]["bound_inv_nu"], 4) == 0.0372
    light = nu.p_int_block([0.05, 0, 0.95, 0, 0, 0], nu.PRIOR_INV_NU, pc, pm)["primary"]
    heavy = nu.p_int_block([0, 0.95, 0, 0, 0, 0.05], nu.PRIOR_INV_NU, pc, pm)["primary"]
    assert light < 0.0324 and 0.0487 <= heavy < 0.05
    mid = nu.p_int_block([0.556, 0, 0, 0, 0, 0.444], nu.PRIOR_INV_NU, pc, pm)["primary"]
    assert abs(mid - 0.05) < 2e-4
    w = [0.1, 0.2, 0.3, 0.2, 0.1, 0.1]
    r = nu.p_int_block(w, nu.PRIOR_INV_NU, pc, pm)
    assert r["primary"] == sum(a * pc[k] for a, k in zip(w, nu.NU_KEYS))
    assert r["bound"] == sum(a * pm[k] for a, k in zip(w, nu.NU_KEYS))
    bad = json.loads(json.dumps(gtp))
    bad["refit"]["3"]["tau_obs"]["p_cal"]["p"] = 0.08
    with pytest.raises(RuntimeError, match="differ from the README"):
        nu.gtp_p_cal(bad)


def test_p_int_reading_rule():
    c = nu.COND
    assert nu.p_int_reading(nu.LBL_LIGHT + c, False, 0.03)["reading"] == "below 0.05"
    assert nu.p_int_reading(nu.LBL_LIGHT + c, False, 0.03)["statement"] == nu.READ_BELOW
    assert nu.p_int_reading(nu.LBL_HEAVY + c, False, 0.05)["reading"] == "at or above 0.05"
    assert nu.p_int_reading(nu.LBL_HEAVY + c + nu.SCALE_SUFFIX, True, 0.03)["reading"] == "not read"
    r = nu.p_int_reading(nu.LBL_WEAK + c, False, 0.03)
    assert r["reading"] == "not read" and r["reference_prior_only"] == 0.0352


# ---------------------------------------------------------------- the stages on synthetic data
def _keys(o):
    if isinstance(o, dict):
        return set(o) | set().union(*[_keys(v) for v in o.values()]) if o else set()
    if isinstance(o, list):
        return set().union(*[_keys(v) for v in o]) if o else set()
    return set()


def test_check_stage_record(lad, stages):
    rec = stages["check"]
    assert rec["stage"] == "check" and rec["outcome"] is None and rec["status"] == "known-answer check passed"
    assert rec["gate"] == "passed" and rec["stage1"]["tau_hat_HF"] >= 0.02
    assert not (_keys(rec) & set(nu.FORBIDDEN_CHECK_KEYS))           # no L(nu), weights, label or p_int
    assert all(r["ok"] for r in rec["checks"]["reduced_form"]) and len(rec["checks"]["reduced_form"]) == 3
    assert all(r["ok"] for r in rec["checks"]["pointwise"]) and len(rec["checks"]["pointwise"]) == 3
    assert rec["checks"]["row_classes"]["ok"] and rec["checks"]["grouping"]["count_check"]["ok"]
    assert rec["checks"]["design"]["n_zero_eigenvalues"] == 1
    assert rec["checks"]["r2_re_reproduction"]["mismatches"] == []
    for kind in nu.INJECTIONS:
        m = rec["mocks"][kind]
        assert len(m["P"]) == 4 and len(m["tau_hat"]) == 4 and all(len(e) == 5 for e in m["ess"])
        assert rec["mock_summary"][kind]["mean_P"] == float(np.mean(m["P"]))
    assert "frac_tau_ge_gate_proxy" in rec["mock_summary"]["t3"]
    assert rec["known_answer"]["outcome"] == "passed"
    s1 = rec["stage1"]
    assert set(s1["grouping_045"]) >= {"tau_hat", "interval_68"} and set(s1["vbase"]) >= {"tau_hat", "tau_obs"}
    assert abs(s1["ratio_to_tau_obs"] - s1["tau_hat_HF"] / shape.RECORDED_TAU_OBS) < 1e-15
    # Stage 1 is R2-RE's REML on the groups
    est = lad["run"].reml_tau(lambda t: lad["run"].reml_m2l(lad["L"], lad["y"], lad["C"], lad["rows_a"],
                                                              lad["groups"], t), 0.5, 0.01)
    assert s1["tau_hat_HF"] == est["tau_hat"] and s1["interval_68"] == est["interval_68"]
    line = nu.check_log_line(rec)
    assert line.startswith("R2-RE-NU check stage: τ̂_HF ") and "known-answer check passed" in line


def test_full_stage_record(lad, stages):
    out = stages["full"]
    assert out["checks"]["check_stage_reproduced"], out["checks"]["differences"]
    assert out["status"] == "evaluated" and len(out["stage2"]["attempts"]) == 1
    wf = nu.weights_from([out["log_L_nu"][k] for k in nu.NU_KEYS], nu.PRIOR_FLAT)
    assert [out["weights"]["flat"][k] for k in nu.NU_KEYS] == wf
    assert out["P_le4"] == wf[0] + wf[1]
    lab, suf = nu.label_from_p(out["P_le4"], out["stage1"]["scale_reference_inside_interval"])
    assert out["label"] == lab and out["scale_suffix"] == suf
    assert out["p_int"]["primary"] == sum(a * nu.P_CAL_README[k] for a, k in zip(wf, nu.NU_KEYS))
    assert set(out["sensitivities"]) == {"profile", "vbase", "grouping_045"}
    prof = out["sensitivities"]["profile"]
    assert set(prof["by_m"]) == {"0.5", "1", "2"} and prof["by_m"]["1"]["log_L"] == [out["log_L_nu"][k]
                                                                                     for k in nu.NU_KEYS]
    assert prof["by_m"]["0.5"]["seed_base"] == 770_000 and prof["by_m"]["2"]["seed_base"] == 770_100
    assert all(prof["log_L_prof"][k] == max(v["log_L"][i] for v in prof["by_m"].values())
               for i, k in enumerate(nu.NU_KEYS))
    for key in ("vbase", "grouping_045"):
        assert 0.0 <= out["sensitivities"][key]["P_le4"] <= 1.0
    s = nu.summary(out)
    assert s["label"] == out["label"] and s["p_int"] == out["p_int"]["primary"]


def test_full_stage_detects_a_changed_check_record(lad, stages):
    bad = nu.json_like(stages["check"])
    bad["mocks"]["het"]["P"][2] += 1e-12
    with pytest.MonkeyPatch.context() as mp:
        _open_mc(mp)
        out = _full(lad, bad)
    assert out["label"] == "ν not evaluable (check-stage reproduction)" and "log_L_nu" not in out
    assert any("mocks.het" in d for d in out["checks"]["differences"])


def test_full_stage_copies_a_final_check_outcome(lad, stages):
    rec = nu.json_like(stages["check"])
    rec["outcome"] = nu.LBL_NO_EXCESS
    out = _full(lad, rec)
    assert out == {"stage": "full", "settings": out["settings"], "status": "final from the check stage",
                   "label": nu.LBL_NO_EXCESS, "stage1": {k: rec["stage1"][k] for k in ("tau_hat_HF", "interval_68")},
                   "gate": "passed", "known_answer": "passed"}


def test_escalation_then_monte_carlo_label(lad, stages):
    logs = []
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(nu, "ESS_MIN", 10 ** 9)
        out = _full(lad, stages["check"], log=logs.append)
    att = out["stage2"]["attempts"]
    assert [a["n"] for a in att] == [200, 300] and [a["seed_base"] for a in att] == [730_000, 740_000]
    assert out["label"] == "ν not determinable by this method (Monte Carlo)"
    assert "p_int" not in out and "weights" not in out and "sensitivities" not in out
    assert any("escalating" in m for m in logs)


def test_undetermined_upper_end_stops_before_l(lad, stages):
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(nu, "scale_inside", lambda interval, ref=nu.SCALE_REF: None)
        _open_mc(mp)
        with pytest.raises(RuntimeError, match="not covered|does not cover"):
            _full(lad, nu.json_like(dict(stages["check"], stage1=dict(stages["check"]["stage1"],
                                                                      scale_reference_inside_interval=None))))


def test_gate_failure_and_check_failures(lad):
    lad0 = _build("run003_nu_null", tau_hf=0.0, seed=9)
    rec = _check(lad0)
    assert rec["outcome"] == nu.LBL_NO_EXCESS and "mocks" not in rec and "pointwise" not in rec["checks"]
    # R2-RE's reproduction failing is label 1, before Stage 1
    r2 = nu.run_check(lad["L"], lad["y"], lad["C"], lad["rows_a"], lad["hf"], lad["calib"], lad["P"], lad["fns"],
                      lambda m: None, lad["grid"], lad["cid"], recorded={"tau_obs": lad["rec"]["tau_obs"] + 1e-3},
                      expected=lad["exp"])
    assert r2["outcome"].startswith("ν not evaluable (R2-RE reproduction") and "stage1" not in r2
    # row classes
    r3 = nu.run_check(lad["L"], lad["y"], lad["C"], lad["rows_a"], lad["hf"], lad["calib"], lad["P"], lad["fns"],
                      lambda m: None, lad["grid"], lad["cid"], recorded=lad["rec"], expected={"n_hf": 277})
    assert r3["outcome"] == "ν not evaluable (row classes)"


def test_pointwise_failure_is_label_1(lad, monkeypatch):
    monkeypatch.setattr(nu, "pointwise_checks", lambda *a, **k: [{"s": 0, "ok": False}])
    rec = _check(lad)
    assert rec["outcome"] == "ν not evaluable (pointwise check)" and "mocks" not in rec


def test_known_answer_failure_is_label_3(lad):
    rec = _check(lad)                         # the real rules with four mocks: (b) cannot hold
    assert rec["outcome"].startswith("ν not determinable") and rec["known_answer"]["outcome"].startswith("failed")
    assert not (_keys(rec) & set(nu.FORBIDDEN_CHECK_KEYS))


# ---------------------------------------------------------------- run.main in the nu_only mode
class _Ctx:
    max_save_bytes = None

    def __init__(self, results, n_cid):
        self.results = results
        self.record_suffix = ""
        self.saved = {}
        self.logs = []
        self.http_calls = []
        self._n_cid = n_cid

    def save(self, name, obj):
        from astrolab.results import write_json
        self.saved[name] = obj
        write_json(self.results / f"{name}.json", obj)

    def log(self, msg):
        self.logs.append(msg)

    def http(self, url, label=None):
        self.http_calls.append((url, label))
        p = self.results.parent / "Pantheon+SH0ES.dat"
        p.write_text(_pantheon_text(self._n_cid), encoding="utf-8")
        return p


def _main_nu(tmp_path, monkeypatch, lad, stage, name, summary=True, log_text=""):
    run = _load(name)
    L, y, C = lad["L"], lad["y"], lad["C"]
    monkeypatch.setattr(run, "N_ROWS", len(y))
    monkeypatch.setattr(run, "load", lambda ctx: (C, L, y, np.zeros((run.N_PAR, 2))))
    monkeypatch.setattr(run, "recorded_reml_grid", lambda: list(lad["grid"]))
    monkeypatch.setattr(run, "recorded_gtp", lambda: GTP)
    monkeypatch.setattr(run, "study_log_text", lambda: log_text)
    monkeypatch.setattr(shape, "RECORDED_TAU_OBS", lad["rec"]["tau_obs"])
    monkeypatch.setattr(nu, "N_HF_EXPECTED", lad["exp"]["n_hf"])
    monkeypatch.setattr(nu, "N_ROWS_A_EXPECTED", lad["exp"]["n_rows_a"])
    monkeypatch.setattr(nu, "PREREGISTERED", dict(nu.PREREGISTERED, **SMALL))
    monkeypatch.setattr(nu, "one_thread_problems", lambda threads=None: [])
    _open_rules(monkeypatch)
    _open_mc(monkeypatch)
    for k, v in dict(SMALL, nu_check=True, nu_only=True, nu_stage=stage).items():
        monkeypatch.setitem(run.PARAMS, k, v)
    from astrolab.results import write_json
    res = tmp_path / "results"
    res.mkdir(exist_ok=True)
    old = {"params": {"a": 1}, "R2_RE_GTP": {"status": "evaluated"}, "runtime_s": 1.5}
    if summary and not (res / "summary.json").exists():
        write_json(res / "summary.json", old)
    return run, _Ctx(res, len(lad["groups"])), old


def test_main_nu_check_then_full(tmp_path, monkeypatch, lad):
    run, ctx, old = _main_nu(tmp_path, monkeypatch, lad, "check", "run003_nu_main1")
    out = run.main(ctx)
    assert ctx.record_suffix == "_nuc" and set(ctx.saved) == {"r2_re_nu_check"}
    assert ctx.http_calls == [(run.PANTHEON_DAT, "Pantheon+SH0ES.dat (CID, USED_IN_SH0ES_HF only)")]
    rec = json.loads((ctx.results / "r2_re_nu_check.json").read_text(encoding="utf-8"))
    assert rec["outcome"] is None and out["R2_RE_NU_check"]["status"] == "known-answer check passed"
    line = nu.check_log_line(rec)
    assert line in ctx.logs
    assert not (_keys(rec) & set(nu.FORBIDDEN_CHECK_KEYS))
    # the full stage refuses without the line in log.md, then runs with it
    run2, ctx2, _ = _main_nu(tmp_path, monkeypatch, lad, "full", "run003_nu_main2", log_text="nothing")
    monkeypatch.setattr(run2, "load", lambda c: pytest.fail("data loaded"))
    with pytest.raises(RuntimeError, match="check stage's line"):
        run2.main(ctx2)
    run3, ctx3, _ = _main_nu(tmp_path, monkeypatch, lad, "full", "run003_nu_main3", log_text="# log\n- " + line + "\n")
    new = run3.main(ctx3)
    assert ctx3.record_suffix == "_nu" and set(ctx3.saved) == {"r2_re_nu", "summary"}
    full = ctx3.saved["r2_re_nu"]
    assert full["checks"]["check_stage_reproduced"] and full["status"] == "evaluated"
    assert list(new) == ["params", "R2_RE_GTP", "R2_RE_NU", "runtime_s"]
    assert {k: new[k] for k in old} == old and new["R2_RE_NU"] == nu.summary(full)
    # a rerun of the full stage needs a reason present in log.md
    run4, ctx4, _ = _main_nu(tmp_path, monkeypatch, lad, "full", "run003_nu_main4", log_text=line)
    with pytest.raises(RuntimeError, match="nu_rerun_reason"):
        run4.main(ctx4)
    # the conclusion check accepts both records (the known-answer rules were opened for four mocks, so their
    # re-derivation is tested on its own below) and rejects a changed P(nu <= 4)
    tc = _load("tc003_nu", "test_conclusions.py")
    chk = {k: v for k, v in nu.json_like(rec).items() if k != "known_answer"}
    tc.check_r2_re_nu(chk, nu.json_like(full), nu.json_like(new["R2_RE_NU"]), GTP)
    with pytest.raises(AssertionError):
        tc.check_r2_re_nu(chk, dict(nu.json_like(full), P_le4=full["P_le4"] + 0.01),
                          nu.json_like(new["R2_RE_NU"]), GTP)
    with pytest.raises(AssertionError):
        tc.check_r2_re_nu(dict(chk, outcome=nu.LBL_WEAK + nu.COND), None, None, None)


def test_conclusion_check_rederives_the_known_answer_rules(stages):
    tc = _load("tc003_nu_rules", "test_conclusions.py")
    rec = nu.json_like(stages["check"])
    vals = {"t3": 0.5, "t10": 0.3, "het": 0.4, "trunc": 0.45}
    for kind, v in vals.items():
        rec["mocks"][kind]["P"] = [v] * len(rec["mocks"][kind]["P"])
        rec["mock_summary"][kind]["mean_P"] = v
    ok, parts, rule = nu.pass_rule(*(rec["mocks"][k]["P"] for k in ("t3", "t10", "het")))
    ok_t, trule = nu.trunc_rule(rec["mocks"]["trunc"]["P"], rec["mocks"]["t3"]["P"], rule["delta_b"],
                                len(rec["mocks"]["trunc"]["failed"]))
    assert ok and ok_t
    rec["known_answer"].update(rules_abc=nu.json_like(rule), rules_de=nu.json_like(trule))
    tc.check_r2_re_nu(rec, None, None, None)
    bad = json.loads(json.dumps(rec))
    bad["mocks"]["t10"]["P"] = [0.45] * len(bad["mocks"]["t10"]["P"])        # (b) now fails, outcome still None
    bad["mock_summary"]["t10"]["mean_P"] = 0.45
    with pytest.raises(AssertionError):
        tc.check_r2_re_nu(bad, None, None, None)


def test_main_nu_refusals(tmp_path, monkeypatch, lad):
    run = _load("run003_nu_refuse")
    ctx = _Ctx(tmp_path, 1)
    monkeypatch.setitem(run.PARAMS, "nu_check", True)
    with pytest.raises(ValueError, match="only standalone"):
        run.main(ctx)
    monkeypatch.setitem(run.PARAMS, "nu_check", False)
    monkeypatch.setitem(run.PARAMS, "nu_only", True)
    with pytest.raises(ValueError, match="nu_only needs nu_check"):
        run.main(ctx)
    monkeypatch.setitem(run.PARAMS, "nu_check", True)
    monkeypatch.setitem(run.PARAMS, "gtp_only", True)
    with pytest.raises(ValueError, match="cannot be combined"):
        run.main(ctx)
    monkeypatch.setitem(run.PARAMS, "gtp_only", False)
    monkeypatch.setitem(run.PARAMS, "nu_stage", "power")
    with pytest.raises(ValueError, match="nu_stage"):
        run.main(ctx)
    monkeypatch.setitem(run.PARAMS, "nu_stage", "check")
    monkeypatch.setattr(run, "load", lambda c: pytest.fail("data loaded"))
    monkeypatch.setitem(run.PARAMS, "nu_n_mocks", 20)
    with pytest.raises(RuntimeError, match=r"differ from the pre-registered values \(nu_n_mocks\)"):
        run.main(ctx)
    monkeypatch.setitem(run.PARAMS, "nu_n_mocks", 200)
    monkeypatch.setattr(shape, "thread_settings", lambda: {"env": {"OMP_NUM_THREADS": "4", "MKL_NUM_THREADS": "1",
                                                                    "OPENBLAS_NUM_THREADS": "1"}, "threadpools": None})
    with pytest.raises(RuntimeError, match="one thread"):
        run.main(ctx)
    # an exploration before the formal r2_re_nu.json is refused before any data is loaded
    ctx.max_save_bytes = 1_000_000
    monkeypatch.setattr(run, "formal_nu_done", lambda path=None: False)
    with pytest.raises(RuntimeError, match="only after the formal"):
        run.main(ctx)


def test_main_nu_full_stage_refusals(tmp_path, monkeypatch, lad, stages):
    run, ctx, _ = _main_nu(tmp_path, monkeypatch, lad, "full", "run003_nu_full_refuse", log_text="x")
    monkeypatch.setattr(run, "load", lambda c: pytest.fail("data loaded"))
    with pytest.raises(RuntimeError, match="needs results/r2_re_nu_check.json"):
        run.main(ctx)
    from astrolab.results import write_json
    write_json(ctx.results / "r2_re_nu_check.json", {"stage": "check", "status": "x"})
    with pytest.raises(RuntimeError, match="stub"):
        run.main(ctx)
    rec = nu.json_like(stages["check"])
    rec["settings"]["nu_n_is"] = 999
    write_json(ctx.results / "r2_re_nu_check.json", rec)
    with pytest.raises(RuntimeError, match="nu_n_is"):
        run.main(ctx)
    # a check-stage rerun over a formal check record needs a reason
    run2, ctx2, _ = _main_nu(tmp_path, monkeypatch, lad, "check", "run003_nu_check_rerun", log_text="x")
    with pytest.raises(RuntimeError, match="nu_rerun_reason"):
        run2.main(ctx2)


def test_full_study_run_copies_the_summary(tmp_path):
    run = _load("run003_nu_copy")
    assert run.nu_summary_from_file(tmp_path) == {"status": "not run (standalone only, README R2-RE-NU)"}
    from astrolab.results import write_json
    out = {"stage": "full", "status": "evaluated", "label": nu.LBL_WEAK + nu.COND, "P_le4": 0.4,
           "P_le4_inv_nu": 0.45, "p_int": {"primary": 0.04, "bound": 0.041}, "p_int_reading": {"reading": "not read"},
           "stage1": {"tau_hat_HF": 0.05, "interval_68": [0.03, 0.07]}}
    write_json(tmp_path / "r2_re_nu.json", out)
    assert run.nu_summary_from_file(tmp_path) == nu.summary(out)
    src = (HERE / "nu.py").read_text(encoding="utf-8").splitlines()
    assert not [x for x in src if x.strip() in ("import run",) or x.strip().startswith("from run ")]


def test_record_sizes_below_1_mb(lad):
    """A check record with 200 mocks per injection stays below 1 MB."""
    rng = np.random.default_rng(0)
    m = {k: {"s": list(range(200)), "tau_hat": rng.random(200).tolist(), "P": rng.random(200).tolist(),
             "ess": rng.random((200, 5)).tolist(), "khat": rng.random((200, 5)).tolist()} for k in nu.INJECTIONS}
    m["trunc"].update(attempt=[0] * 200, failed=[])
    size = len(json.dumps({"mocks": m, "stage1": {"main": {"grid_m2l": rng.random(51).tolist()}}}, indent=1))
    assert size < 1_000_000, size
