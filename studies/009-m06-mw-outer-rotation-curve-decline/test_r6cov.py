"""Offline tests of r6cov.py (README 2.6, R6-COV) on synthetic inputs only (no fit of Table 3 with the
new covariances)."""
import sys
from pathlib import Path

import numpy as np
import pytest
from scipy import integrate

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import r6cov  # noqa: E402
import rc  # noqa: E402

R = np.arange(9.5, 27.0, 1.0)
V = np.linspace(222.0, 176.0, len(R))
SIG = np.linspace(3.0, 20.0, len(R))


@pytest.mark.parametrize("kind", [("se", 2.0), ("se", 8.0), ("global", None)])
def test_kernel_cov_diagonal_and_pd(kind):
    for f in (0.0, 0.5, 0.99):
        C = r6cov.make_cov(kind, f, R, V, SIG)
        assert np.allclose(np.diag(C), SIG ** 2)
        assert np.all(np.linalg.eigvalsh(C) > 0)
    assert r6cov.max_corr_fraction(kind, 0.7, V, SIG) == 0.7


def test_fractional_cov():
    c = 0.99 * np.min(SIG / V)
    C = r6cov.make_cov(("fractional", None), c, R, V, SIG)
    assert np.allclose(np.diag(C), SIG ** 2) and np.all(np.linalg.eigvalsh(C) > 0)
    assert np.isclose(C[0, 5], c ** 2 * V[0] * V[5])
    assert r6cov.max_corr_fraction(("fractional", None), c, V, SIG) == pytest.approx(np.max(c ** 2 * V ** 2 / SIG ** 2))


def test_lcdm_conversion_matches_direct_integration():
    for lrho2, lr2 in ((6.0, np.log10(20.0)), (3.0, 0.0), (10.0, np.log10(300.0))):
        m = r6cov.mass_fn("lcdm", [lrho2, lr2])
        rho2, r2, a = 10 ** lrho2, 10 ** lr2, r6cov.ALPHA_LCDM
        rho = lambda r: rho2 * np.exp(-(2 / a) * ((r / r2) ** a - 1))
        for r in (9.5, 26.5, 100.0):
            direct = integrate.quad(lambda s: 4 * np.pi * s ** 2 * rho(s), 0, r, limit=400, epsabs=0, epsrel=1e-10)[0]
            assert m(r) == pytest.approx(direct, rel=1e-6)


def test_calibrate_smallest_crossing_and_failures():
    grid = np.round(np.arange(100) * 0.01, 2)
    res = r6cov.calibrate(lambda f: 20 * f, grid, 15.0, 1e-4)  # monotone: root 0.75
    assert res["status"] == "calibrated" and res["value"] == pytest.approx(0.75, abs=2e-4)
    curve = lambda f: 1.3 + 80 * f if f < 0.2 else (5.0 if f < 0.6 else 16.0)   # crosses at 0.17125, dips, rises
    res = r6cov.calibrate(curve, grid, 15.0, 1e-4)
    assert res["value"] == pytest.approx(0.17125, abs=2e-4)                     # the smallest crossing
    assert r6cov.calibrate(lambda f: 1.0, grid, 15.0, 1e-4)["status"] == "not calibratable"
    skip = lambda f: None if abs(f - 0.3) < 1e-9 else 20 * f      # a failed grid point away from the crossing
    assert r6cov.calibrate(skip, grid, 15.0, 1e-4)["status"] == "calibrated"
    below = lambda f: None if abs(f - 0.74) < 1e-9 else 20 * f    # the point just below the crossing failed
    assert r6cov.calibrate(below, grid, 15.0, 1e-4)["status"] == "not evaluable"


def test_powerlaw_profile_recovers_slope():
    Ro = np.arange(19.5, 27.0, 1.0)
    Vo = 1000.0 * Ro ** -0.45
    C = np.diag(np.full(len(Ro), 4.0))
    t = r6cov.powerlaw_tests(Ro, Vo, C)
    assert t["gamma_min"] == pytest.approx(-0.45, abs=1e-5) and t["chi2_min"] == pytest.approx(0, abs=1e-6)
    assert t["t1_evaluable"] and t["dchi2_flat"] > 0 and t["D_K"] > 0 and t["D_02"] > 0
    assert t["pref_kepler"] == pytest.approx(t["D_02"] - t["D_K"])


def test_fit_halo_recovers_synthetic_einasto():
    model_x = [np.log10(3.7e11), 12.0, 2.4]
    vb2 = np.full(len(R), 150.0 ** 2)
    Vs = np.sqrt(vb2 + rc.G * r6cov.mass_fn("einasto", model_x)(R) / R)
    cho = r6cov.linalg.cho_factor(np.diag(SIG ** 2))
    fit = r6cov.fit_halo("einasto", R, Vs, vb2, cho)
    assert fit["converged"] and fit["chi2"] < 1e-6


def test_labels_and_high_f_order():
    flags = {"a": False, "b": False, "c": False, "d": True, "e": True}
    v = {"a": 3.5, "b": 3.2, "c": 3.1, "d": 2.5, "e": None}
    assert r6cov.label("t1", v, flags) == "kernel-dependent (high-f)"     # all: >= 2; unflagged: >= 3
    v["d"] = 3.4
    assert r6cov.label("t1", v, flags) == "flat rejected at >= 3 sigma"
    flags2 = {"a": True, "b": True, "c": False, "d": False, "e": True}
    assert r6cov.label("t1", {"a": 1.0, "b": 1.5, "c": 1.2, "d": None, "e": None}, flags2) == \
        "flat not rejected at 2 sigma (only with high-f covariances)"
    assert r6cov.label("t2", {"a": 5, "b": None, "c": None, "d": None, "e": 6}, {}) == "not evaluable"
    assert r6cov.label("t2", {"a": 5, "b": -5, "c": 1}, {}) == "kernel-dependent"
    assert r6cov.label("t2", {"a": 1, "b": -3, "c": 2}, {}) == "not distinguished"
    assert r6cov.label("t3", {"a": 4.5, "b": 8.9, "c": 5}, {}) == "mildly disfavoured"
    assert r6cov.label("t3", {"a": -1.0, "b": 3.9, "c": 0}, {}) == "not disfavoured"
    assert r6cov.label("t3", {"a": 3.0, "b": 9.5, "c": 12}, {}) == "kernel-dependent"
