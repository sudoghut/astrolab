"""Offline tests for astrolab.cosmo and astrolab.infer (design plan 010)."""
import numpy as np
import pytest

from astrolab import cosmo, infer

PLANCK_BF = dict(H0=67.32, ombh2=0.022383, omch2=0.12011)   # Planck 2018 VI Table 1, Plik best fit


def test_theta_calibration_reproduces_reference():
    b = cosmo.Background(**PLANCK_BF)
    assert 100 * b.theta_star() == pytest.approx(1.041085, abs=1e-9)
    K = cosmo.theta_calibration()
    assert 1.0 < K < 1.003          # the fitting-formula z_* sits ~2 above CAMB's (plan 010)


def test_theta_second_point_sanity():
    # CamSpec posterior means of the same table: 100 theta_* = 1.04106 +- 0.00031
    b = cosmo.Background(67.39, 0.02229, 0.1197)
    assert abs(100 * b.theta_star() - 1.04106) < 2.57e-4    # within one compressed-prior sigma


def test_rd_against_planck_best_fit():
    # Planck r_drag = 147.049 Mpc (N_eff = 3.046); Aubourg Eq. 16 is good to ~0.02%
    assert cosmo.Background(**PLANCK_BF).rd() == pytest.approx(147.049, rel=3e-4)


def test_matter_density_and_neutrinos():
    b = cosmo.Background(**PLANCK_BF)
    assert b.Om == pytest.approx(0.3158, abs=2e-4)                 # Planck best fit Omega_m
    assert b.omnu == pytest.approx(cosmo.omega_nu_today(), rel=0.01)
    assert b.ombc == pytest.approx(0.022383 + 0.12011)


def test_lcdm_limit_and_low_z():
    b = cosmo.Background(70.0, 0.022, 0.12)
    z = 1e-3
    assert float(b.DM(z)[0]) == pytest.approx(cosmo.C_KMS / 70.0 * z, rel=2e-3)
    assert float(b.E(1.0)) == pytest.approx(1.0, abs=1e-12)          # flatness closes the budget


def test_bao_late_matches_full_background():
    b = cosmo.Background(67.32, 0.022383, 0.12011, w0=-0.8, wa=-0.5)
    dm, dh, _ = cosmo.bao_late(b.Om, b.h * b.rd(), [0.5, 2.33], w0=-0.8, wa=-0.5)
    assert dm == pytest.approx(b.DM([0.5, 2.33]) / b.rd(), rel=1e-3)   # radiation neglected
    assert dh == pytest.approx(b.DH(np.array([0.5, 2.33])) / b.rd(), rel=1e-3)


def test_w0wa_changes_distances():
    a = cosmo.bao_late(0.3, 100.0, [1.0])[0][0]
    b = cosmo.bao_late(0.3, 100.0, [1.0], w0=-0.5, wa=-1.5)[0][0]
    assert a != pytest.approx(b, rel=1e-3)


def test_sigma_from_dchi2_matches_paper():
    assert infer.sigma_from_dchi2(-12.5) == pytest.approx(3.1, abs=0.05)
    assert infer.sigma_from_dchi2(-8.0) == pytest.approx(2.4, abs=0.05)
    assert infer.sigma_from_dchi2(-21.0) == pytest.approx(4.2, abs=0.05)
    assert infer.sigma_from_dchi2(0.5) == 0.0


def test_marginalised_offset_matches_brute_force():
    rng = np.random.default_rng(1)
    n = 6
    a = rng.normal(size=(n, n))
    cov = a @ a.T + n * np.eye(n)
    cinv = np.linalg.inv(cov)
    d = rng.normal(size=n) + 0.7
    best = min(infer.gaussian_chi2(d - m, cinv) for m in np.linspace(-3, 3, 60001))
    assert infer.chi2_marg_offset(d, cinv) == pytest.approx(best, abs=1e-6)


def test_multistart_respects_constraint():
    cons = lambda x: -(x[0] + x[1]) - 1e-9                        # w0 + wa < 0
    f = lambda x: (x[0] + 0.5) ** 2 + (x[1] + 0.5) ** 2          # minimum at w0 + wa = -1
    r = infer.minimize_multistart(f, [(-3, 1), (-3, 2)], n_starts=5, constraint=cons)
    assert r["f"] == pytest.approx(0.0, abs=1e-8) and r["x"].sum() < 0
    g = lambda x: (x[0] - 0.5) ** 2 + (x[1] - 0.5) ** 2           # unconstrained minimum excluded
    r = infer.minimize_multistart(g, [(-3, 1), (-3, 2)], n_starts=5, constraint=cons)
    assert r["x"].sum() == pytest.approx(0.0, abs=1e-5) and r["f"] == pytest.approx(0.5, abs=1e-4)
    assert r["x"].sum() < 0


def test_multistart_badly_scaled():
    # mimics the compressed-CMB problem: a tight constraint on a combination of a parameter of
    # order 70 and one of order 0.02, inside wide bounds
    f = lambda x: ((x[0] * x[1] - 1.5) / 1e-5) ** 2 + ((x[1] - 0.02) / 1e-4) ** 2
    r = infer.minimize_multistart(f, [(20, 100), (0.005, 0.1)], n_starts=10, seed=3)
    assert r["f"] < 1e-6
    assert r["x"] == pytest.approx([75.0, 0.02], rel=1e-5)
    assert r["n_agree"] >= 3


def test_multistart_ignores_nan_and_nests():
    f = lambda x: np.nan if x[0] < 0 else (x[0] - 0.3) ** 2
    r = infer.minimize_multistart(f, [(-1, 1)], n_starts=5, x0_extra=[[-0.9]])
    assert np.isfinite(r["f"]) and r["x"][0] == pytest.approx(0.3, abs=1e-5)
    # the nested optimum as a start guarantees chi2(extended) <= chi2(nested)
    h = lambda x: (x[0] - 1.0) ** 2 + 0.1 * (x[1] ** 2 - 1.0) ** 2   # nested model: x[1] = 0
    nested = 0.1
    r = infer.minimize_multistart(h, [(-3, 3), (-3, 3)], n_starts=3, x0_extra=[[1.0, 0.0]])
    assert r["f"] <= nested + 1e-9


def test_dm_at_zero():
    b = cosmo.Background(70.0, 0.022, 0.12)
    assert b.DM(0.0)[0] == 0.0
    assert np.all(np.isfinite(b.DM([0.0, 0.5])))


def test_multistart_reports_nonconvergence():
    # an evaluation cap far too small: no start converges, and this is reported
    f = lambda x: sum((xi - 0.1 * i) ** 2 for i, xi in enumerate(x))
    r = infer.minimize_multistart(f, [(-1, 1)] * 5, n_starts=3, maxfev=10, n_polish=0)
    assert r["converged"] is False and r["n_conv"] == 0 and r["n_agree"] == 0
    assert r["x"] is None and r["f"] is None
    r = infer.minimize_multistart(f, [(-1, 1)] * 5, n_starts=3)
    assert r["converged"] and r["n_agree"] >= 3 and r["x_spread"] < 1e-3


# ---- infer.gls (design plan 012) -------------------------------------------------------------

def _gls_problem(seed=1, n=60, p=5):
    rng = np.random.default_rng(seed)
    L = rng.normal(size=(n, p))
    M = rng.normal(size=(n, n))
    C = M @ M.T / n + 0.5 * np.eye(n)
    q_true = rng.normal(size=p)
    y = L @ q_true + np.linalg.cholesky(C) @ rng.normal(size=n)
    return L, y, C


def test_gls_matches_explicit_formula():
    L, y, C = _gls_problem()
    Ci = np.linalg.inv(C)
    cov = np.linalg.inv(L.T @ Ci @ L)
    q = cov @ L.T @ Ci @ y
    out = infer.gls(L, y, C, return_estimator=True)
    assert np.allclose(out["q"], q, atol=1e-10)
    assert np.allclose(out["cov"], cov, atol=1e-10)
    assert np.allclose(out["A"] @ y, q, atol=1e-10)
    r = y - L @ q
    assert out["chi2"] == pytest.approx(r @ Ci @ r, rel=1e-10)
    assert out["dof"] == L.shape[0] - L.shape[1]


def test_gls_ordinary_least_squares_limit():
    L, y, _ = _gls_problem(seed=2)
    out = infer.gls(L, y, 4.0 * np.eye(len(y)))
    q_ols = np.linalg.lstsq(L, y, rcond=None)[0]
    assert np.allclose(out["q"], q_ols, atol=1e-10)
    assert np.allclose(out["sigma"] ** 2, 4.0 * np.diag(np.linalg.inv(L.T @ L)), rtol=1e-10)


def test_gls_drops_zero_columns_and_reuses_factor():
    from scipy import linalg
    L, y, C = _gls_problem(seed=3)
    L0 = np.insert(L, 2, 0.0, axis=1)                  # a host whose rows were removed
    full = infer.gls(L, y, C)
    out = infer.gls(L0, y, c_factor=linalg.cho_factor(C, lower=True))
    assert list(out["kept"]) == [0, 1, 3, 4, 5]
    assert np.isnan(out["q"][2]) and np.isnan(out["sigma"][2])
    assert np.allclose(np.delete(out["q"], 2), full["q"], atol=1e-10)


def test_gls_rejects_rank_deficiency_and_bad_shapes():
    L, y, C = _gls_problem(seed=4)
    Lbad = L.copy()
    Lbad[:, 1] = 2.0 * Lbad[:, 0]
    with pytest.raises(ValueError, match="rank deficient"):
        infer.gls(Lbad, y, C)
    with pytest.raises(ValueError):
        infer.gls(L, y[:-1], C)
    with pytest.raises(ValueError):
        infer.gls(L, y)


def test_gls_subset_shift_variance_is_exact():
    # Delta = e^T (A_sub S - A_full) y has variance a^T C a; check against Monte Carlo
    L, _, C = _gls_problem(seed=5, n=40, p=3)
    rows = np.arange(0, 40, 2)
    full = infer.gls(L, np.zeros(40), C, return_estimator=True)
    sub = infer.gls(L[rows], np.zeros(len(rows)), C[np.ix_(rows, rows)], return_estimator=True)
    S = np.zeros((len(rows), 40))
    S[np.arange(len(rows)), rows] = 1.0
    a = (sub["A"] @ S - full["A"])[-1]
    var = a @ C @ a
    rng = np.random.default_rng(0)
    ys = (np.linalg.cholesky(C) @ rng.normal(size=(40, 20000))).T
    deltas = ys @ a
    assert deltas.var() == pytest.approx(var, rel=0.05)
    assert var > 0
    # a is the right vector: it maps y to the difference of the two estimates ...
    y = ys[0]
    q_sub = infer.gls(L[rows], y[rows], C[np.ix_(rows, rows)])["q"][-1]
    q_full = infer.gls(L, y, C)["q"][-1]
    assert a @ y == pytest.approx(q_sub - q_full, abs=1e-10)
    # ... and for nested GLS with the same C, Var(difference) = Var(sub) - Var(full)
    assert var == pytest.approx(sub["sigma"][-1] ** 2 - full["sigma"][-1] ** 2, rel=1e-8)


def test_gls_checks_factor_shape():
    from scipy import linalg
    L, y, C = _gls_problem(seed=6)
    with pytest.raises(ValueError, match="c_factor"):
        infer.gls(L[:-1], y[:-1], c_factor=linalg.cho_factor(C, lower=True))
