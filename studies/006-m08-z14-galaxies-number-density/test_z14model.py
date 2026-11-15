"""Offline tests of z14model.py (no network; synthetic LFs only, not the calibration data)."""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest
from astropy.cosmology import Planck18

HERE = Path(__file__).parent


def _import(name):
    spec = importlib.util.spec_from_file_location(f"study006_{name}", HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


zm = _import("z14model")


@pytest.fixture(scope="module")
def setup():
    c = zm.cosmo_params(Planck18)
    pk = zm.LinearPower(c)
    lnM = np.log(10.0 ** np.arange(8.0, 14.0 + 1e-9, 0.02))
    return c, pk, lnM, pk.sigma_M(np.exp(lnM))


def test_cosmo_params():
    c = zm.cosmo_params(Planck18)
    assert abs(c["h"] - 0.6766) < 1e-4 and abs(c["Om"] - 0.30966) < 1e-5
    assert abs(c["sigma8"] - 0.8102) < 1e-4 and abs(c["ns"] - 0.9665) < 1e-4


def test_transfer_function(setup):
    c = setup[0]
    k = np.logspace(-5, 2, 400)
    T = zm.eisenstein_hu(k, c)
    assert abs(T[0] - 1) < 1e-3
    assert np.all(np.isfinite(T)) and T[-1] < 1e-3


def test_sigma8_normalisation(setup):
    c, pk = setup[0], setup[1]
    assert abs(pk.sigma_R(8.0 / c["h"])[0] - c["sigma8"]) < 1e-3


def test_growth():
    c = zm.cosmo_params(Planck18)
    D = zm.growth([0.0, 1.0, 14.5], c)
    assert abs(D[0] - 1) < 1e-9 and D[1] < 1
    # matter domination: D ~ a, so D(14.5) * 15.5 is nearly constant at high z
    assert abs(zm.growth(14.5, c)[0] * 15.5 / (zm.growth(20.0, c)[0] * 21.0) - 1) < 0.01


def test_st_normalisation():
    assert abs(zm.st_normalisation() - 1) < 0.01
    assert zm.st_normalisation(-3, 3) < 0.8


def test_hmf_positive_and_reed(setup):
    c, pk, lnM, sig0 = setup
    D = zm.growth(14.5, c)[0]
    st = zm.dndlnm(lnM, sig0, D, pk.rho_m(), "st")
    rd = zm.dndlnm(lnM, sig0, D, pk.rho_m(), "reed07")
    assert np.all(st > 0) and np.all(rd > 0)
    assert np.all(np.diff(st[lnM > np.log(1e10)]) < 0)
    with pytest.raises(ValueError):
        zm.dndlnm(lnM, sig0, D, pk.rho_m(), "ps")


def test_ab_zero_point_and_conversion():
    assert abs(zm.AB_ZP - 51.595) < 0.002
    # SFR 1 Msun/yr (Chabrier) -> L = 1 / (0.63 * 1.15e-28)
    c = zm.cosmo_params(Planck18)
    M = np.array([1e11])
    theta = (0.1, 11.0, 0.0, 0.0)            # eps = 0.1 exactly
    sfr = 0.1 * c["Ob"] / c["Om"] * zm.mdot_halo(M, 10.0, c, "fakhouri_mean")
    expect = zm.AB_ZP - 2.5 * np.log10(sfr / (0.63 * 1.15e-28))
    assert np.allclose(zm.muv_median(M, 10.0, c, theta, "fakhouri_mean"), expect)


def test_accretion_forms():
    c = zm.cosmo_params(Planck18)
    M = np.array([1e12])
    E = np.sqrt(c["Om"] * 3 ** 3 + 1 - c["Om"])
    assert np.isclose(zm.mdot_halo(M, 2.0, c, "fakhouri_mean")[0], 46.1 * (1 + 2.22) * E)
    assert np.isclose(zm.mdot_halo(M, 2.0, c, "fakhouri_median")[0], 25.3 * (1 + 3.30) * E)
    assert np.isclose(zm.mdot_halo(M, 2.0, c, "dekel13")[0], 1e12 * 0.030 * 0.82 / c["sigma8"] * 3 ** 2.5 / 1e9)


def test_statistics():
    lo, hi = zm.gehrels(2)
    assert abs(lo - 0.708) < 0.002 and abs(hi - 4.638) < 0.002
    assert abs(zm.poisson_tail(2, 2 / 182) * 1e6 - 59.9) < 0.2
    assert abs(zm.poisson_tail(2, 0.02) * 1e6 - 197.4) < 0.2


def test_lf_model_delta_limit(setup):
    """With tiny scatter the model LF is the abundance-matched one (number conserving)."""
    c, pk, lnM, sig0 = setup
    D = zm.growth(8.0, c)[0]
    h = zm.dndlnm(lnM, sig0, D, pk.rho_m(), "st")
    med = -2.5 * np.log10(np.exp(lnM) / 1e10) - 18.0       # monotonic toy relation
    mg = np.linspace(-26, -10, 801)
    phi = zm.lf_model(mg, lnM, h, med, 0.05)
    assert abs(np.trapz(phi, mg) / np.trapz(h, lnM) - 1) < 0.02


def test_calibration_recovers_synthetic_schechter(setup):
    """Fit a made-up Schechter LF (not the calibration data) to rms < 0.05 dex."""
    c, pk, lnM, sig0 = setup
    D = zm.growth(8.0, c)[0]
    h = zm.dndlnm(lnM, sig0, D, pk.rho_m(), "st")
    fake = {"m_star": -20.5, "phi_star": 1.0e-4, "alpha": -2.0}
    mg = np.arange(-22.0, -17.0 + 1e-9, 0.25)
    cal = zm.calibrate(lnM, h, 8.0, c, "fakhouri_mean", 0.7, fake, mg)
    assert cal["rms"] < 0.05 and len(cal["theta"]) == 4


def test_median_shape():
    M = np.logspace(8, 14, 301)
    med = -18 - 4 * np.exp(-(np.log10(M) - 11.5) ** 2)        # brightest at 1e11.5
    s = zm.median_shape(M, med, -22, -17)
    assert abs(np.log10(s["m_peak"]) - 11.5) < 0.03 and not s["monotonic"]
    assert s["m_cal_lo"] < s["m_cal_hi"] == s["m_peak"]
    mono = zm.median_shape(M, -2.5 * np.log10(M / 1e10) - 18, -22, -17)
    assert mono["monotonic"] and mono["m_cal_lo"] < mono["m_cal_hi"]


def test_eps_floor():
    c = zm.cosmo_params(Planck18)
    M = np.array([1e8, 1e9, 1e11])
    theta = (0.1, 11.0, 1.0, 0.5)
    base = zm.muv_median(M, 14.0, c, theta, "fakhouri_mean")
    fl = zm.muv_median(M, 14.0, c, theta, "fakhouri_mean", eps_floor_mass=1e9)
    assert fl[0] < base[0] and np.isclose(fl[2], base[2])


def test_verdict_helpers(monkeypatch):
    monkeypatch.syspath_prepend(str(HERE))
    run = _import("run")
    assert run.r2_verdict(2.9, 3).startswith("same") and run.r2_verdict(3.1, 3) == "higher"
    assert run.r2_verdict(0.3, 3) == "lower"
    roots = {"lower": {"value": 1.2, "censored": None}, "upper": {"value": 1.4, "censored": None}}
    assert run.r3_verdict(roots, [1.5, 2.0]) == "different"
    roots["upper"] = {"value": 4.0, "censored": "gt"}
    assert run.r3_verdict(roots, [1.5, 2.0]).startswith("consistent")
    roots = {"lower": {"value": 0.7, "censored": "le"}, "upper": {"value": 1.4, "censored": None}}
    assert run.r3_verdict(roots, [1.5, 2.0]) == "different"


def test_eh_wiggles_against_nowiggle():
    c = zm.cosmo_params(Planck18)
    k = np.logspace(-3, 1, 600)
    r = zm.eisenstein_hu(k, c) / zm.eisenstein_hu_nowiggle(k, c)
    assert np.all((r > 0.95) & (r < 1.05))
    assert abs(zm.eh_sound_horizon(c) - 150.0) < 3.0


def test_growth_against_cpt():
    c = zm.cosmo_params(Planck18)
    Om, a = c["Om"], 0.5
    Omz = Om / (Om + (1 - Om) * a ** 3)
    Olz = 1 - Omz
    g = lambda om, ol: 2.5 * om / (om ** (4 / 7) - ol + (1 + om / 2) * (1 + ol / 70))  # noqa: E731
    cpt = a * g(Omz, Olz) / g(Om, 1 - Om)
    assert abs(zm.growth(1.0, c)[0] / cpt - 1) < 0.01


def test_sigma_small_mass(setup):
    c, pk = setup[0], setup[1]
    assert 5.0 < pk.sigma_M(np.array([1e8]))[0] < 7.0


def test_reed_close_to_st_shape():
    s = np.array([0.8, 1.0, 1.2])
    r = zm.f_reed07(s, n_eff=1e6) / zm.f_st(s)
    assert np.all(np.abs(r - 1) < 0.35)    # Reed's G1/G2 bumps and c = 1.08 change ST by tens of percent
    assert np.all(np.isfinite(r))


def test_solve_sigma_and_monotonic(monkeypatch):
    monkeypatch.syspath_prepend(str(HERE))
    run = _import("run")
    sg = np.arange(0.7, 4.0 + 1e-9, 0.05)
    phi_fn = lambda s: 1e-8 * np.exp(2.0 * s)   # noqa: E731  increasing
    phis = phi_fn(sg)
    assert run.monotonic_kind(phis) == "increasing"
    assert run.monotonic_kind(phis[::-1]) == "decreasing"
    assert run.monotonic_kind(np.array([1.0, 2.0, 1.5])) == "not monotonic"
    tgt = {"central": phi_fn(2.0), "lower": phi_fn(0.5), "upper": phi_fn(4.5), "edge": phi_fn(0.7)}
    roots = run.solve_sigma(sg, phis, tgt, phi_fn)
    assert abs(roots["central"]["value"] - 2.0) < 1e-3 and roots["central"]["censored"] is None
    assert roots["lower"]["censored"] == "le" and roots["upper"]["censored"] == "gt"
    assert roots["edge"]["censored"] is None and abs(roots["edge"]["value"] - 0.7) < 1e-9


def test_robustness_rule(monkeypatch):
    monkeypatch.syspath_prepend(str(HERE))
    run = _import("run")
    rows48 = [{"r2": "higher"}] * 48
    assert run.robustness(rows48, "r2", "higher", 48) == "robust"
    assert run.robustness(rows48[:47], "r2", "higher", 48) == "not assessable"
    mixed = rows48[:47] + [{"r2": "lower"}]
    assert run.robustness(mixed, "r2", "higher", 48) == "calibration-dependent"
    assert run.robustness(rows48, "r2", "not evaluable", 48) == "not assessable"
