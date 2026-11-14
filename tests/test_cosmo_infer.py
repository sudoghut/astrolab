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
