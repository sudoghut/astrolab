"""Offline tests of rc.py (analytic limits and synthetic data; no study data, no network)."""
import importlib.util
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent


def _import(name):
    spec = importlib.util.spec_from_file_location(f"study009_{name}", HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


rc = _import("rc")


def test_thin_disc_limit_matches_freeman():
    for R in (2.0, 9.5, 20.0, 26.5):
        thin = rc.disc_v2(R, 4e10, 2.6, 1e-4)
        assert abs(thin / rc.freeman_v2(R, 4e10, 2.6) - 1) < 2e-3


def test_thick_disc_lowers_midplane_speed_inside():
    assert rc.disc_v2(5.0, 4e10, 2.6, 0.9) < rc.disc_v2(5.0, 4e10, 2.6, 0.25)


def test_disc_far_field_is_point_mass():
    v2 = rc.disc_v2(200.0, 4e10, 2.6, 0.3)
    assert abs(v2 / rc.point_v2(200.0, 4e10) - 1) < 5e-3


def test_hernquist_and_point():
    assert np.isclose(rc.hernquist_v2(9.5, 1.55e10, 0.7) / rc.point_v2(9.5, 1.55e10), (9.5 / 10.2) ** 2)


def test_einasto_total_mass_and_profile():
    M0, h, inv_n = 3.7e11, 11.4, 1 / 0.43
    n = 1 / inv_n
    total = rc.einasto_mass(1e6, M0, h, inv_n)
    from scipy import special
    assert np.isclose(total, M0 * n * special.gamma(3 * n), rtol=1e-6)
    # numerical integral of rho = rho0 exp(-(r/h)^(1/n)) agrees
    from scipy import integrate
    rho0 = M0 / (4 * np.pi * h ** 3)
    m = integrate.quad(lambda r: 4 * np.pi * r ** 2 * rho0 * np.exp(-(r / h) ** inv_n), 0, 30)[0]
    assert np.isclose(rc.einasto_mass(30.0, M0, h, inv_n), m, rtol=1e-6)


def test_rvir_root():
    rho_cr = 134.0
    m = lambda r: rc.nfw_mass(r, 1e7, 20.0)
    rv = rc.r_vir(m, rho_cr)
    assert rv is not None
    assert np.isclose(m(rv) / (4 / 3 * np.pi * rv ** 3), 200 * rho_cr, rtol=1e-6)
    assert rc.r_vir(lambda r: 0 * r, rho_cr) is None


def test_powerlaw_fit_recovers_slope():
    rng = np.random.default_rng(3)
    R = np.arange(19.5, 27, 1.0)
    V = 1000 * R ** -0.5 + rng.normal(0, 2, R.size)
    sig = np.full(R.size, 2.0)
    start = np.array([1000.0, -0.5])
    chain, tau, ok = rc.run_emcee(rc.powerlaw_lnpost, start, (R, V, sig, 1.0, 1e5), 32, 3000, 500, 0)
    g = chain[:, 1]
    assert abs(np.median(g) + 0.5) < 0.1 and rc.s_statistic(g) > 3


def test_one_sided_sigma():
    assert np.isclose(rc.one_sided_sigma(0.0013499), 3.0, atol=1e-3)


def test_disc_mass_sphere_limits():
    M, L, H = 4e10, 2.6, 0.3
    assert rc.disc_mass_sphere(500.0, M, L, H) / M > 0.999
    # thin-disc limit: M(<r) -> M [1 - (1 + r/L) exp(-r/L)]
    r = 8.0
    thin = M * (1 - (1 + r / L) * np.exp(-r / L))
    assert abs(rc.disc_mass_sphere(r, M, L, 1e-4) / thin - 1) < 1e-3
