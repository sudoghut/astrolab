"""Offline tests for the study-004 helpers (no data access)."""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent))
import wb  # noqa: E402


def _random_sky(n, rng):
    ra = rng.uniform(0, 360, n)
    dec = np.degrees(np.arcsin(rng.uniform(-1, 1, n)))
    return ra, dec


def test_regions_partition_the_sphere():
    plan = wb.strip_plan()
    rng = np.random.default_rng(1)
    ra, dec = _random_sky(4000, rng)
    edges = [(0.0, 60.0), (15.0, -60.0), (45.0, 80.0), (359.999, -80.0), (0.0, 90.0), (0.0, -90.0)]
    pts = list(zip(ra, dec)) + edges
    for a, d in pts:
        assert len(wb.region_of(a, d, plan)) == 1, (a, d)


def _offset(ra, dec, theta_deg, pa_deg):
    """Point at angular distance theta and position angle pa from (ra, dec)."""
    r0, d0, t, p = map(np.radians, (ra, dec, theta_deg, pa_deg))
    d1 = np.arcsin(np.sin(d0) * np.cos(t) + np.cos(d0) * np.sin(t) * np.cos(p))
    r1 = r0 + np.arctan2(np.sin(p) * np.sin(t) * np.cos(d0), np.cos(t) - np.sin(d0) * np.sin(d1))
    return np.degrees(r1) % 360, np.degrees(d1)


def test_star_b_box_covers_partners():
    plan = wb.strip_plan()
    rng = np.random.default_rng(2)
    ra, dec = _random_sky(3000, rng)
    theta = wb.search_radius_deg(36.5)          # weighted parallax can reach ~36.5 mas
    for a, d in zip(ra, dec):
        k = wb.region_of(a, d, plan)[0]
        r = plan[k]
        for pa in (0, 45, 90, 135, 180, 225, 270, 315):
            b_ra, b_dec = _offset(a, d, theta, pa)
            assert r["bdec0"] <= b_dec <= r["bdec1"], (a, d, pa)
            assert bool(wb.ra_in(b_ra, r["bra0"], r["bra1"])), (a, d, pa)


def test_search_radius():
    assert wb.search_radius_deg(36.0) == pytest.approx(1.031, abs=0.001)


def test_canonical_pairs_dedupes():
    a = np.array([5, 7, 3, 9])
    b = np.array([7, 5, 9, 3])
    assert list(wb.canonical_pairs(a, b)) == [0, 2]


def test_mond_boost_limits():
    a0, ge = 1.2e-10, 1.184
    assert wb.mond_boost(1e-4, a0, ge) == pytest.approx(1.0, abs=1e-6)
    gne = ge * a0
    nu_e = wb.mls_nu(gne, a0)
    k_e = wb.mls_k(gne, a0)
    assert wb.mond_boost(1e4, a0, ge) == pytest.approx(np.sqrt(nu_e * (1 + k_e / 3)), rel=1e-6)
    assert -0.5 < float(k_e) < 0
    # about 20% faster deep in the MOND regime (C26 section 2)
    assert 1.15 < float(wb.mond_boost(1e4, a0, ge)) < 1.25


def test_mls_k_matches_numeric_derivative():
    a0 = 1.2e-10
    g = 0.7 * a0
    h = 1e-6
    num = (np.log(wb.mls_nu(g * (1 + h), a0)) - np.log(wb.mls_nu(g * (1 - h), a0))) / (2 * h)
    assert wb.mls_k(g, a0) == pytest.approx(num, rel=1e-5)


def test_mass_rule():
    assert wb.mass_from_mg(4.67) == pytest.approx(1.0)
    m = wb.mass_from_mg(9.0)
    assert m == pytest.approx(10 ** (0.0725 * (4.67 - 9.0)) + 0.05)


def test_perspective_removes_common_motion():
    # two stars sharing one space velocity show no relative sky motion after the correction
    ra1, dec1, ra2, dec2 = 30.0, 20.0, 30.3, 20.2
    plx = 10.0
    v = np.array([20.0, -15.0, 30.0])           # km/s, equatorial Cartesian

    def pm_rv(ra, dec):
        a, d = np.radians(ra), np.radians(dec)
        e = np.array([-np.sin(a), np.cos(a), 0])
        n = np.array([-np.sin(d) * np.cos(a), -np.sin(d) * np.sin(a), np.cos(d)])
        r = np.array([np.cos(d) * np.cos(a), np.cos(d) * np.sin(a), np.sin(d)])
        return v @ e * plx / wb.KAPPA, v @ n * plx / wb.KAPPA, v @ r

    pa1, pd1, rv1 = pm_rv(ra1, dec1)
    pa2, pd2, _ = pm_rv(ra2, dec2)
    vr, vd = wb.perspective_vsky(ra1, dec1, pa1, pd1, ra2, dec2, pa2, pd2, plx, rv1, correct=True)
    assert abs(vr) < 1e-9 and abs(vd) < 1e-9
    vr0, vd0 = wb.perspective_vsky(ra1, dec1, pa1, pd1, ra2, dec2, pa2, pd2, plx, rv1, correct=False)
    assert np.hypot(vr0, vd0) > 0.05            # without the correction a spurious motion appears


def test_vsky_sigma_matches_monte_carlo():
    rng = np.random.default_rng(3)
    p1, p2, ep1, ep2 = 10.0, 10.1, 0.05, 0.08
    pm1, pm2 = (50.0, -20.0), (50.6, -19.5)
    e = dict(e_pmra1=0.03, e_pmdec1=0.04, e_pmra2=0.05, e_pmdec2=0.03)
    s = wb.vsky_sigma(pm1, pm2, p1, p2, ep1, ep2, e["e_pmra1"], e["e_pmdec1"], e["e_pmra2"], e["e_pmdec2"],
                      0, 0, 0, 0, 0, 0)
    n = 40000
    P1 = p1 + ep1 * rng.normal(size=n)
    P2 = p2 + ep2 * rng.normal(size=n)
    pbar = (ep2 ** 2 * P1 + ep1 ** 2 * P2) / (ep1 ** 2 + ep2 ** 2)
    dra = (pm2[0] + e["e_pmra2"] * rng.normal(size=n)) - (pm1[0] + e["e_pmra1"] * rng.normal(size=n))
    ddec = (pm2[1] + e["e_pmdec2"] * rng.normal(size=n)) - (pm1[1] + e["e_pmdec1"] * rng.normal(size=n))
    v = wb.KAPPA / pbar * np.hypot(dra, ddec)
    assert s == pytest.approx(v.std(), rel=0.05)


def test_merge_and_bins():
    assert wb.merge_outer([100, 80, 50, 20, 10, 4], 15) == [0, 1, 2, 3, 3, 3]
    assert wb.merge_outer([100, 80, 50, 20, 12, 4], 15) == [0, 1, 2, 3, 4, 4]
    assert wb.merge_outer([100, 80, 50, 20, 30, 28], 15) == [0, 1, 2, 3, 4, 5]
    assert list(wb.bin_index([0.05, 0.2, 3.0], [0.1057, 0.2307, 0.5088, 1.0275, 2.0902])) == [0, 1, 5]


def test_gls_and_model_comparison():
    x = np.array([0.073, 0.153, 0.348, 0.744, 1.419, 3.079])
    flat = 0.5 * np.ones(6)
    cov = np.diag(np.full(6, 0.02 ** 2))
    r = wb.compare_models(flat, x, cov)
    assert r["chi2_newton"] == pytest.approx(0.0, abs=1e-12)
    assert r["dchi2"] > 0 and r["A_newton"] == pytest.approx(0.5)
    step = 0.5 * wb.mond_boost(x)
    r2 = wb.compare_models(step, x, cov)
    assert r2["chi2_mond"] == pytest.approx(0.0, abs=1e-12) and r2["dchi2"] < 0


def test_bootstrap_cov_shape():
    rng = np.random.default_rng(4)
    vt = rng.rayleigh(0.5, 600)
    b = rng.integers(0, 6, 600)
    c = wb.bootstrap_cov(vt, b, 6, 200, 0)
    assert c.shape == (6, 6) and np.all(np.diag(c) > 0)
