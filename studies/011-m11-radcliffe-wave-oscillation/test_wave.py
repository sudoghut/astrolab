"""Offline unit tests of study 011's model and statistics: synthetic data only, no network, no tables."""
import importlib.util
import math
import sys
from pathlib import Path

import numpy as np
import pytest
from scipy.integrate import quad

HERE = Path(__file__).parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))


def _import(name):
    spec = importlib.util.spec_from_file_location(f"study011_{name}", HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


W = _import("wave011")
S = _import("stats011")
F = _import("fit011")
run = _import("run")

OM0, MU0, R0 = 0.074, 1.3e-3, 3700.0


# ---------------------------------------------------------------------------------------------
# eq. 3

def test_omega_small_amplitude_limit():
    for r in (7400.0, 8400.0, 9400.0):
        w = float(W.omega_eq3(1e-3, r, OM0, MU0, R0))
        assert w == pytest.approx(OM0 * math.exp((W.R_SUN - r) / (2 * R0)), rel=1e-9)


def test_omega_anharmonic_drop_at_0p29():
    zmax = 0.29 / MU0
    drop = float(W.omega_eq3(zmax, W.R_SUN, OM0, MU0, R0)) / OM0 - 1.0
    assert -0.07 <= drop <= -0.06
    assert drop == pytest.approx(-0.75 * 0.29 ** 2, abs=0.005)       # first-order theory -6.3%


def test_omega_matches_period_integral_eq2():
    """2 pi / T with T from eq. 2 (energy conservation, numerical integral) equals eq. 3."""
    for zmax in (50.0, 150.0, 300.0, 450.0):
        phi = lambda z: 0.5 * OM0 ** 2 * (z ** 2 - MU0 ** 2 * z ** 4)
        # substitute z = zmax sin(t) to remove the endpoint singularity
        integrand = lambda t: zmax * math.cos(t) / math.sqrt(phi(zmax) - phi(zmax * math.sin(t)))
        T = 2 * math.sqrt(2) * quad(integrand, 0, math.pi / 2, limit=200)[0]
        assert 2 * math.pi / T == pytest.approx(float(W.omega_eq3(zmax, W.R_SUN, OM0, MU0, R0)), rel=1e-7)


def test_unbound_orbit_gives_zero_likelihood():
    assert np.isnan(W.omega_eq3(1.0 / math.sqrt(2) / MU0 + 1.0, W.R_SUN, OM0, MU0, R0))
    g = W.Grid(400)
    v = W.k24_vector(6, A=600.0)                     # mu0 * 600 pc = 0.78 > 1/sqrt(2)
    assert W.wave_on_grid(v, g) is None
    d = W.Data(*(np.zeros(3) for _ in range(4)), np.ones((3, 4)), np.zeros(0), np.zeros(0), np.zeros(0))
    m = W.Model(W.Setup(free=W.SHAPE_NAMES), d, g)
    assert m.loglike(m.theta_of(v)) == -np.inf
    assert m.loglike(m.theta_of(W.k24_vector(6))) > -np.inf


def test_sun_period_and_density():
    assert W.rho0(0.068) == pytest.approx(0.085, abs=0.002)
    assert 82.5 < W.sun_period_myr(0.074, MU0, R0, 7.8) < 85.0          # wiki: 83-84 Myr at 74
    assert 90.0 < W.sun_period_myr(0.068, 1.4e-3, 3600.0, 7.8) < 94.0    # wiki: ~92 Myr at 68


# ---------------------------------------------------------------------------------------------
# curve, closest point, weights, likelihood

def test_baseline_passes_through_anchors_and_s_zero():
    g = W.Grid(2001, -0.2, 1.4)
    v = W.k24_vector(6)
    x, y, s = W.baseline(v, g)
    for u, (xa, ya) in ((0.0, ("x0", "y0")), (0.5, ("x1", "y1")), (1.0, ("x2", "y2"))):
        i = int(np.argmin(abs(g.u - u)))
        assert abs(g.u[i] - u) < 1e-9
        assert x[i] == pytest.approx(v[W.IDX[xa]], abs=1e-6) and y[i] == pytest.approx(v[W.IDX[ya]], abs=1e-6)
    assert s[np.argmin(abs(g.u))] == pytest.approx(0.0, abs=1e-6)
    assert np.all(np.diff(s) > 0) and s[0] < 0
    xc, yc, sc = W.baseline(v, g, "chord")
    u1 = W.chord_u1(v)
    i = int(np.argmin(abs(g.u - u1)))
    assert xc[i] == pytest.approx(v[W.IDX["x1"]], abs=2.0)


def test_closest_point_recovery():
    g = W.Grid()
    v = W.k24_vector(6, w0t=-0.38, B=0.84)
    wv = W.wave_on_grid(v, g)
    vi = np.flatnonzero(wv["valid"])
    j = vi[np.linspace(20, len(vi) - 20, 60).astype(int)]
    d = W.Data(wv["x"][j], wv["y"][j], wv["z"][j], wv["vz"][j], np.zeros((60, 4)), wv["x"][j[:10]],
               wv["y"][j[:10]], wv["z"][j[:10]])
    m = W.Model(W.Setup(free=W.SHAPE_NAMES + ("w0t", "B"), clouds=True), d, g)
    ev = m.evaluate(v)
    assert np.array_equal(ev["cl_idx"], j)
    assert np.allclose(ev["cl_res"], 0.0, atol=1e-6) and not ev["cl_outlier"].any()
    assert np.allclose(ev["co_res"], 0.0, atol=1e-6)
    # brute force agrees with the augmented matrix product
    rng = np.random.default_rng(3)
    D = rng.normal(0, 300, (40, 4))
    M = rng.normal(0, 300, (500, 4))
    assert np.array_equal(W.closest(D, M), np.argmin(((D[:, None] - M[None]) ** 2).sum(-1), 1))


def test_outlier_rule_and_likelihood_value():
    sig = 47.0
    c, thr = W.outlier_terms(np.array([2.9, 3.1]), "k24")
    assert thr == 3.0 and np.allclose(c, np.tanh([2.9, 3.1]))
    # one cluster with residual (dx, 0, 0, 0): eq. 13 by hand
    g = W.Grid()
    v = W.k24_vector(6)
    wv = W.wave_on_grid(v, g)
    i = np.flatnonzero(wv["valid"])[700]
    for dx, out in ((1.6 * sig, False), (1.8 * sig, True)):
        # displace along z; the closest point stays the same for a small displacement relative to the curve scale
        d = W.Data(np.array([wv["x"][i]]), np.array([wv["y"][i]]), np.array([wv["z"][i] + dx]),
                   np.array([wv["vz"][i]]), np.zeros((1, 4)), np.zeros(0), np.zeros(0), np.zeros(0))
        m = W.Model(W.Setup(free=W.SHAPE_NAMES), d, g)
        ev = m.evaluate(v)
        x2 = (ev["cl_res"] / sig) ** 2
        assert ev["lnL"] == pytest.approx(-0.5 * (np.tanh(x2).sum() + 3 * math.log(2 * math.pi * sig ** 2)))
        assert bool(ev["cl_outlier"][0]) == bool(np.any(x2 > 3.0))
    assert W.outlier_terms(np.array([8.9, 9.1]), "3sigma")[1] == 9.0
    assert W.outlier_terms(np.array([100.0]), "gauss")[1] == math.inf


def test_kde_weights():
    s = np.r_[np.linspace(0, 2000, 50), np.full(50, 500.0)]
    w = W.kde_weights(s, 100.0)
    assert w.sum() == pytest.approx(len(s))
    assert w[60] < w[0]                                   # dense clump down-weighted
    assert np.allclose(W.kde_weights(s, 0.0), 1.0)


def test_canonical_mapping_keeps_the_model():
    g = W.Grid(800)
    v = W.k24_vector(5, w0t=2.5)
    wv = W.wave_on_grid(v, g)
    vi = np.flatnonzero(wv["valid"])[::40]
    d = W.Data(wv["x"][vi] + 10, wv["y"][vi], wv["z"][vi] - 20, wv["vz"][vi] + 1, np.zeros((len(vi), 4)),
               np.zeros(0), np.zeros(0), np.zeros(0))
    m = W.Model(W.Setup(free=W.SHAPE_NAMES + ("w0t", "B")), d, g)
    th = m.theta_of(v)
    thc = F.canonical(m, th)
    assert -math.pi / 2 <= thc[m.setup.free.index("w0t")] < math.pi / 2
    assert m.loglike(thc) == pytest.approx(m.loglike(th), rel=1e-12)


def test_broad_prior_jacobian():
    d = W.Data(*(np.zeros(2) for _ in range(4)), np.ones((2, 4)), np.zeros(0), np.zeros(0), np.zeros(0))
    st = W.Setup(free=("ln_omega0", "ln_mu0", "r0"), prior="broad")
    m = W.Model(st, d, W.Grid(100))
    a = m.logprior(np.array([math.log(0.06), math.log(1.0), 5000.0]))
    b = m.logprior(np.array([math.log(0.12), math.log(1.0), 5000.0]))
    assert b - a == pytest.approx(math.log(2.0))           # uniform in omega0
    assert m.logprior(np.array([math.log(0.2), 0.0, 5000.0])) == -np.inf


# ---------------------------------------------------------------------------------------------
# T5: b-hat and the phase relation

def _two_rows(B, w0t, n=400, k=1.0, phi=0.3, env=True):
    s = np.linspace(0, 2500, n)
    lam = s / (4800 - 1.4 * s)
    e = 1.0 / (1.0 + ((s - 600) / 700) ** 2) if env else np.ones(n)
    th = 2 * math.pi * k * lam + phi
    z = e * (B * np.sin(w0t + th) + (1 - B) * np.sin(-w0t + th))
    v = e * (B * np.cos(w0t + th) - (1 - B) * np.cos(-w0t + th))
    return lam, e, z, v


@pytest.mark.parametrize("B", [0.5, 0.84, 1.0, 0.2])
@pytest.mark.parametrize("w0t", [-0.38, 0.0, 0.9, -1.4])
def test_bhat_equals_2B_minus_1(B, w0t):
    lam, e, z, v = _two_rows(B, w0t)
    W1 = np.ones_like(z)
    f = S.t5_fit(lam, e, 215 * z, W1, 215 * v, W1)
    assert f["k_shared"] == pytest.approx(1.0, abs=1e-3)
    assert f["bhat"] == pytest.approx(2 * B - 1, abs=2e-3)
    if np.max(np.abs(v)) > 1e-6:          # B = 0.5 with omega0 t = 0 has v_z = 0: no k_vz
        assert f["k_ratio"] == pytest.approx(1.0, abs=2e-3)


def test_bhat_matrix_identity():
    for B in (0.5, 0.84, 1.0):
        for w in (-1.2, -0.38, 0.0, 0.7):
            # rows (A cos psi, A sin psi) of z and v_z/omega in the (sin theta, cos theta) basis
            assert S.bhat(math.cos(w), (2 * B - 1) * math.sin(w), -math.sin(w), (2 * B - 1) * math.cos(w)) == \
                pytest.approx(2 * B - 1, abs=1e-12)


def test_travelling_vs_standing_phase_relation():
    W1 = None
    lam, e, z, v = _two_rows(1.0, 0.0)
    W1 = np.ones_like(z)
    f = S.t5_fit(lam, e, z, W1, v, W1)
    assert abs(f["Delta"]) == pytest.approx(math.pi / 2, abs=1e-3)      # travelling: 90 degrees
    assert f["rho"] == pytest.approx(1.0, abs=1e-3)
    lam, e, z, v = _two_rows(0.5, 0.6)
    f = S.t5_fit(lam, e, z, W1, v, W1)
    assert min(abs(f["Delta"]), math.pi - abs(f["Delta"])) < 1e-3      # standing: 0 or 180 degrees
    assert f["bhat"] == pytest.approx(0.0, abs=1e-3)


def test_k_at_bound_flag_and_different_wavelengths():
    lam, e, z, _ = _two_rows(1.0, 0.0, k=1.0)
    _, _, _, v = _two_rows(1.0, 0.0, k=2.0)
    W1 = np.ones_like(z)
    f = S.t5_fit(lam, e, z, W1, v, W1)
    assert f["k_z"] == pytest.approx(1.0, abs=2e-3) and f["k_vz"] == pytest.approx(2.0, abs=2e-3)
    assert f["k_ratio"] == pytest.approx(0.5, abs=2e-3)
    lam, e, z, _ = _two_rows(1.0, 0.0, k=0.2)
    g = S.fit_sinusoids(lam, e, [(z, W1)])
    assert g["at_bound"]


def test_t5_pipeline_noiseless_known_answer():
    g = W.Grid()
    for B in (0.5, 1.0):
        v = W.k24_vector(6, w0t=-0.38, B=B)
        wv = W.wave_on_grid(v, g)
        vi = np.flatnonzero(wv["valid"])
        j = vi[np.linspace(150, 1300, 90).astype(int)]
        d = W.Data(wv["x"][j], wv["y"][j], wv["z"][j], wv["vz"][j], np.zeros((90, 4)), np.zeros(0), np.zeros(0),
                   np.zeros(0))
        m = W.Model(W.Setup(free=W.SHAPE_NAMES), d, g)
        x, y, z, vz = F.known_answer_vectors(m, v, d, np.random.default_rng(0), sigma=1e-9)
        assert np.allclose(z, wv["z"][j], atol=1e-6)
        cur = F.t5_curve(v, g)                          # the injected curve itself
        r = F.t5_analyse(cur, x, y, z, vz, np.zeros((90, 4)), cut=None, bandwidth=100.0)
        # omega(s) in T5 uses |zeta| of the clouds-only curve, the injection uses the same |zeta|
        assert r["fit"]["bhat"] == pytest.approx(2 * B - 1, abs=0.02)
        assert r["n_end"] == 0


# ---------------------------------------------------------------------------------------------
# T4

def test_R_standing_vs_travelling():
    s = np.linspace(0, 2500, 300)
    lam = s / (4800 - 1.4 * s)
    zeta = -200 / (1 + ((s - 600) / 700) ** 2)
    om = np.full_like(s, 0.07)
    th = 2 * math.pi * lam - 0.1
    w = 0.5
    z = zeta * np.sin(th) * math.cos(w)
    vz = -zeta * om * np.sin(th) * math.sin(w)
    assert S.circular_R(z, om, vz) == pytest.approx(1.0, abs=1e-9)
    zt, vzt = zeta * np.sin(th), zeta * om * np.cos(th)
    assert S.circular_R(zt, om, vzt) < 0.5


def test_p_boot_and_power():
    assert S.p_boot(0, 100) == pytest.approx(1 / 101)
    assert S.p_boot_ge(5.0, [1, 5, 6, 2]) == (pytest.approx(3 / 5), 2)
    assert S.p_low(0.3, [0.2, 0.3, 0.9]) == (pytest.approx(3 / 4), 2)
    st = np.linspace(0.5, 1.0, 999)
    assert S.power([0.1] * 10, st, 0.01) == 1.0
    assert S.power([0.99] * 10, st, 0.01) == 0.0


def test_calibrated_p():
    from scipy.stats import chi2
    mocks = np.array([1.0, 1.0, 1.0, 1.0])
    c = S.calibrated_p(3.84, mocks, 1)
    assert c["p_cal"] == pytest.approx(chi2.sf(3.84, 1))
    c = S.calibrated_p(3.84, np.full(10, 2.0), 1)
    assert c["p_cal"] == pytest.approx(chi2.sf(1.92, 1))
    assert S.calibrated_p(3.0, np.zeros(10), 2)["p_cal"] is None
    assert S.t3_standing_label(None, 0.1, 0.1, 0) == S.NOT_EVALUABLE


# ---------------------------------------------------------------------------------------------
# labels: edges are exclusive and every input gets exactly one label

def test_t1_labels():
    assert [S.t1_label(n) for n in range(7)] == ["not reproduced"] * 3 + ["partly reproduced"] * 2 + ["reproduced"] * 2


def test_t3_labels_edges():
    assert S.t3_standing_label(0.0009, 0.0009, 0.01, 0) == "standing excluded strongly"
    assert S.t3_standing_label(0.0009, 0.0009, 0.01, 1) == "standing excluded"       # a mock reached it
    assert S.t3_standing_label(0.001, 0.0001, 0.01, 0) == "standing excluded"        # 0.001 is not < 0.001
    assert S.t3_standing_label(0.049, 0.5, 0.049, 3) == "standing excluded"
    assert S.t3_standing_label(0.049, 0.5, 0.05, 3) == "standing not excluded"       # p_boot not < 0.05
    assert S.t3_standing_label(0.05, 0.5, 0.01, 3) == "standing not excluded"
    assert S.t3_travel_label(0.04, 0.04).startswith("pure travelling (B = 1) disfavoured")
    assert S.t3_travel_label(0.04, 0.06).endswith("not disfavoured")
    assert S.t3_standing_label_reduced(0.0009, 0.0009) == "standing excluded strongly"
    assert S.t3_standing_label_reduced(0.04, 0.5) == "standing excluded"
    assert S.t3_travel_label_reduced(0.05).endswith("not disfavoured")


def test_t4_labels_edges():
    assert S.t4_label(0.0099, 0.8) == "standing excluded by the phases"
    assert S.t4_label(0.01, 0.9) == S.UNDETERMINED
    assert S.t4_label(0.05, 0.9) == S.UNDETERMINED
    assert S.t4_label(0.0501, 0.9) == "standing not excluded by the phases"
    assert S.t4_label(0.001, 0.79) == S.UNDETERMINED
    for p in np.linspace(0, 1, 41):
        for pw in (0.0, 0.79, 0.8, 1.0):
            assert S.t4_label(p, pw) in ("standing excluded by the phases", "standing not excluded by the phases",
                                         S.UNDETERMINED)


def test_t5_labels_edges():
    assert S.wavelength_label(0.8, 1.25) == "consistent"
    assert S.wavelength_label(0.79, 1.0) == S.UNDETERMINED
    assert S.wavelength_label(1.26, 2.0) == "different" and S.wavelength_label(0.3, 0.79) == "different"
    assert S.wavelength_label(1.25, 2.0) == S.UNDETERMINED
    dom = "travelling component in K24's direction dominates"
    assert S.bhat_label(0.41, 0.9)["label"] == dom
    assert S.bhat_label(0.4, 0.9)["label"] == S.UNDETERMINED
    assert S.bhat_label(-0.2, 0.39)["label"] == "no travelling dominance in K24's direction"
    assert S.bhat_label(-0.2, 0.4)["label"] == S.UNDETERMINED
    r = S.bhat_label(-0.9, -0.5)
    assert r["label"] == "no travelling dominance in K24's direction" and r["opposite_direction"]
    assert S.bhat_label(0.5, 0.9, wavelengths="different")["label"] == "not applicable (wavelengths differ)"
    assert S.bhat_label(0.5, 0.9, known_answer_pass=False)["label"] == S.UNDETERMINED
    assert S.bhat_label(0.5, 0.9, wavelengths=S.UNDETERMINED)["caveat_wavelengths_undetermined"]


def test_t7_t8_labels():
    assert S.t7_label(100, 109, 109) == "CO prefers the travelling wave"
    assert S.t7_label(100, 108.9, 120) == "CO does not distinguish"
    assert S.t8_label(0.08, 0.17, 0.4) == "data-driven"
    assert S.t8_label(0.085, 0.17, 0.4) == "partly data-driven"         # 0.085 is not < 0.085
    assert S.t8_label(0.08, 0.17, 0.5) == "partly data-driven"
    assert S.t8_label(0.2, 0.17, -0.7) == "prior-driven"


def test_overall_reading():
    sup = S.overall_reading("partly reproduced", "standing excluded strongly", "standing excluded by the phases",
                            "travelling component in K24's direction dominates", "robust")
    assert sup["reading"].startswith("K24's travelling-wave reading is supported")
    nots = S.overall_reading("reproduced", "standing not excluded", S.UNDETERMINED,
                             "no travelling dominance in K24's direction", "fragile")
    assert nots["reading"] == "not supported"
    mixed = S.overall_reading("reproduced", "standing excluded", S.UNDETERMINED,
                              "travelling component in K24's direction dominates", "robust")
    assert mixed["reading"] == "mixed" and mixed["undetermined_or_not_evaluable"] == ["T4"]


def test_interval_helpers():
    x = np.arange(1001.0)
    lo, hi = S.interval(x)
    assert lo == pytest.approx(25.0) and hi == pytest.approx(975.0)
    assert S.quantile_mcse(x, 0.025) > 0
    lo, hi = F.circ_interval(np.r_[np.full(500, math.pi - 0.01), np.full(500, -math.pi + 0.01)])
    assert hi - lo < 0.1


# ---------------------------------------------------------------------------------------------
# run.py helpers

def test_load_check():
    w = np.ones(5)
    assert run.load_check(np.array([1.0, -2.0, 0.5, 2.0, -1.0]), w, 3.0)["passed"]
    assert not run.load_check(np.array([1.0, -2.0, 0.5, 2.0, -1.0]) - 7.8, w, 3.0)["passed"]
    assert not run.load_check(np.array([3.0, 3.0]), np.ones(2), 3.0)["passed"]      # |mean| < 3 is strict


def test_rotation_and_galactic_angles():
    vx, vy = run.rotation_lsr(np.array([0.0]), np.array([0.0]), 242.0)
    assert vx[0] == pytest.approx(0.0, abs=1e-12) and vy[0] == pytest.approx(0.0, abs=1e-12)
    l, b = run.galactic_lb(np.array([0.0, -100.0]), np.array([100.0, 0.0]), np.array([0.0, -100.0]))
    assert l[0] == pytest.approx(90.0) and l[1] == pytest.approx(180.0) and b[1] == pytest.approx(-45.0)


def test_variant_list_pools_single_catalogues():
    import pandas as pd
    refs = ["A"] * 43 + ["B"] * 37 + ["C"] * 23 + ["D"] * 15 + ["E"] * 5 + ["F", "G"]
    cl = pd.DataFrame({"reference": refs})
    vs = run.variant_list(run.PARAMS, cl)
    v8 = [v for v in vs if v[0] == "v8_leave_out"]
    assert len(v8) == 6 and ("v8_leave_out", ("F", "G")) in v8
    assert len(vs) == 15


def test_mock_noise_free_places_inliers_on_the_model():
    g = W.Grid(1000)
    v = W.k24_vector(6)
    wv = W.wave_on_grid(v, g)
    vi = np.flatnonzero(wv["valid"])[100:900:20]
    n = len(vi)
    d = W.Data(wv["x"][vi] + 5, wv["y"][vi], wv["z"][vi] + 8, wv["vz"][vi] - 0.5, np.zeros((n, 4)), np.zeros(0),
               np.zeros(0), np.zeros(0))
    m = W.Model(W.Setup(free=W.SHAPE_NAMES), d, g)
    inl = np.ones(n, bool)
    inl[0] = False
    x, y, z, vz = F.mock_vectors(m, v, d, inl, np.random.default_rng(1), sigma=0.0)
    assert x[0] == d.cx[0] and z[0] == d.cz[0]                     # outlier keeps its values
    ev = m.evaluate(v)
    assert np.allclose(z[1:], wv["z"][ev["cl_idx"][1:]])


# ---------------------------------------------------------------------------------------------
# compact checkpoints and cleanup (README 4.9, item 13)

def test_keep_mask_thinning_across_chunks():
    burn, thin, steps = 20, 10, 100
    kept = np.concatenate([np.flatnonzero(F.keep_mask(s, min(7, steps - s), burn, thin)) + s
                           for s in range(0, steps, 7)])
    assert kept.tolist() == list(range(burn, steps, thin))


class _Gauss:
    """A 3-parameter Gaussian posterior with the attributes run_mcmc uses."""

    class setup:
        free = ("a", "b", "c")

    def theta_of(self, v):
        return np.asarray(v, float)

    def scales(self):
        return np.ones(3)

    def logpost(self, th):
        return -0.5 * float(np.sum(np.asarray(th) ** 2))


def test_mcmc_checkpoint_is_compact_resumable_and_removed(tmp_path):
    store = F.Store(tmp_path, "k1")
    kw = dict(seed=5, n_walkers=8, n_steps=60, n_burn=20, chunk=7, log=lambda m: None, min_tau_mult=0.0,
              thin_keep=10)
    # stop after the first chunk, then resume
    store.stop_after_s = -1.0
    with pytest.raises(F.Paused):
        F.run_mcmc(_Gauss(), np.zeros(3), store=store, name="g", **kw)
    store.stop_after_s = None
    store.check_time = lambda where="": None
    calls = {"n": 0}
    orig_put = store.put

    def put(name, obj):
        if name.endswith("_state"):
            calls["n"] += 1
            if calls["n"] == 2:                      # interrupt mid-chain: the state stays on disk
                orig_put(name, obj)
                raise KeyboardInterrupt
        orig_put(name, obj)
    store.put = put
    with pytest.raises(KeyboardInterrupt):
        F.run_mcmc(_Gauss(), np.zeros(3), store=store, name="g", **kw)
    st = store.get("g_a_state")
    assert st["n_done"] == 14 and st["kept"].shape == (0, 8, 3)        # nothing post-burn yet
    assert "chain" not in st                                            # no full chain stored
    store.put = orig_put
    res = F.run_mcmc(_Gauss(), np.zeros(3), store=store, name="g", **kw)
    assert res["samples"].shape == (4 * 8, 3) and res["thin"] == 10     # steps 20, 30, 40, 50
    assert not store.has("g_a_state") and store.has("g_a_final")
    # same result as an uninterrupted run
    s2 = F.Store(tmp_path, "k2")
    res2 = F.run_mcmc(_Gauss(), np.zeros(3), store=s2, name="g", **kw)
    assert np.allclose(res["samples"], res2["samples"])
    assert store.size_bytes() < 50 * 1024 ** 2

    class Ctx:
        msgs = []

        def log(self, m):
            self.msgs.append(m)
    ctx = Ctx()
    assert run.finish_checkpoints(store, ctx)
    assert not (tmp_path / "k1").exists() and "removed" in ctx.msgs[-1]


def test_checkpoint_size_of_a_formal_chain_is_small(tmp_path):
    """The real storage code at the formal size (48 walkers, 15 parameters, 6000 steps, burn 2000), on a
    cheap Gaussian posterior: the running state and the final summary each stay near 1-2 MB."""
    class G15(_Gauss):
        class setup:
            free = tuple(f"p{i}" for i in range(15))

        def scales(self):
            return np.ones(15)

    store = F.Store(tmp_path, "formal")
    sizes = []
    orig_put = store.put

    def put(name, obj):
        orig_put(name, obj)
        sizes.append(store.size_bytes())
    store.put = put
    res = F.run_mcmc(G15(), np.zeros(15), seed=1, n_walkers=48, n_steps=6000, n_burn=2000, store=store, name="c",
                     chunk=500, log=lambda m: None, min_tau_mult=0.0, thin_keep=10)
    assert res["samples"].shape == (400 * 48, 15)
    assert max(sizes) < 4 * 1024 ** 2                 # state and final summary together, at their largest
    assert store.size_bytes() < 2 * 1024 ** 2         # after the chain: only the final summary
    assert not store.has("c_a_state")


def test_replace_with_retry(tmp_path, monkeypatch):
    import os as _os
    src, dst = tmp_path / "a", tmp_path / "b"
    src.write_text("x")
    calls = {"n": 0}
    real = _os.replace

    def flaky(a, b):
        calls["n"] += 1
        if calls["n"] < 3:
            raise PermissionError("locked")
        real(a, b)
    monkeypatch.setattr(F.os, "replace", flaky)
    F.replace_with_retry(src, dst, tries=5, wait=0.0)
    assert dst.read_text() == "x" and calls["n"] == 3


def test_exploration_checkpoints_are_separate(tmp_path):
    class Ctx:
        max_save_bytes = None
        results = run.HERE / "results"
    P = dict(run.PARAMS)
    assert run.is_formal_run(Ctx())
    assert run.checkpoint_root(tmp_path, P, Ctx()) == tmp_path / P["checkpoint_subdir"]

    class Ex:
        max_save_bytes = 1024 ** 2
        results = run.HERE / "explore" / "2026-11-21-topic"
    assert not run.is_formal_run(Ex())
    assert run.checkpoint_root(tmp_path, P, Ex()) == tmp_path / P["checkpoint_subdir"] / "explore" / "2026-11-21-topic"


def test_t5_select_uses_positions_only():
    g = W.Grid()
    cur = F.t5_curve(W.k24_vector(3), g)
    d = F.synthetic_clusters(g, 60, np.random.default_rng(4))
    j, end, keep = F.t5_select(cur, d.cx, d.cy, d.cz, cut=math.sqrt(3) * 47)
    j2, end2, keep2 = F.t5_select(cur, d.cx, d.cy, d.cz, cut=math.sqrt(3) * 47)
    assert np.array_equal(keep, keep2) and keep.sum() > 30 and not np.any(keep & end)
    r = F.t5_analyse(cur, d.cx, d.cy, d.cz, d.cvz + 100.0, d.csig, cut=math.sqrt(3) * 47, bandwidth=100.0)
    assert np.array_equal(r["kept_mask"], keep)             # velocities never change the selection
