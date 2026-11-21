"""Offline unit tests of study 012's helper modules: synthetic data only, no network, no Zenodo files."""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from scipy.stats import chi2

HERE = Path(__file__).parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))


def _import(name):
    spec = importlib.util.spec_from_file_location(f"study012u_{name}", HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


M = _import("model012")
D = _import("data012")
K = _import("kin012")
S = _import("stats012")


def bright_lf(rng, n=2000, mg=-4.0):
    d = rng.uniform(2, 4, n)
    c = rng.uniform(1.2, 2.0, n)
    g = np.full(n, mg) + 5 * np.log10(d * 100)
    return M.LFSample(g, c, g + 0.45 * c, 1 / d - 0.02, rng.uniform(5, 30, n))


def errs(rng):
    return M.ErrSampler(rng.uniform(8, 16, 5000), rng.uniform(0.01, 0.05, 5000))


# ---------------------------------------------------------------------------------------------
# model012

def test_geometry():
    r2, z2 = M.gc_r2_z2(np.array([0.0]), np.array([0.0]), np.array([8.2]), 8.2)
    assert r2[0] == pytest.approx(0.0, abs=1e-12) and z2[0] == 0.0
    r2, z2 = M.gc_r2_z2(np.array([90.0]), np.array([30.0]), np.array([2.0]), 8.2)
    assert r2[0] == pytest.approx(4.0 + 8.2 ** 2) and z2[0] == pytest.approx(1.0)


def test_grid_weights_integrate():
    d, plx, w = M.dist_grid(0.2, 30.0, 300)
    assert w.sum() == pytest.approx(1 / 0.2 - 1 / 30.0)
    assert M.dist_grid(1.0, 30.0, 300)[0][0] == pytest.approx(1.0)


def test_sigma_and_shape_recovered_without_magnitude_selection():
    """With a luminous LF the magnitude limits never bind, so version (ii) must be unbiased."""
    rng = np.random.default_rng(4)
    lf, er = bright_lf(rng), errs(rng)
    sim = M.simulate(rng, 4000, sigma=2.7, q=1.0, lf=lf, ext=(0.0, 5.0), errs=er)
    assert sim["l"].size == 4000
    lik = M.Lik(sim["l"], sim["b"], sim["plx"], sim["err"], sim["g"], sim["bp_rp"], version="ii", k=200)
    f = M.fit_sigma(lik)
    assert abs(f["sigma"] - 2.7) < 0.15 and not f["at_bound"]
    s1 = M.step1(lik, rng, sph=f, n_starts=2)
    assert s1["profile"]["check_q1_ok"]
    assert s1["label"] == "spherical adequate"
    sim = M.simulate(rng, 4000, sigma=2.7, q=0.5, lf=lf, ext=(0.0, 5.0), errs=er, bmin=5.0)
    assert np.all(np.abs(sim["b"]) >= 5.0)
    lik = M.Lik(sim["l"], sim["b"], sim["plx"], sim["err"], sim["g"], sim["bp_rp"], version="ii", k=200)
    s1 = M.step1(lik, rng, n_starts=2)
    assert s1["label"] == "flattened preferred" and abs(s1["flat"]["theta"][1] - 0.5) < 0.1


def test_bootstrap_weights_equal_duplication():
    rng = np.random.default_rng(1)
    sim = M.simulate(rng, 300, sigma=2.7, q=1.0, lf=bright_lf(rng), ext=(0.0, 5.0), errs=errs(rng))
    lik = M.Lik(sim["l"], sim["b"], sim["plx"], sim["err"], sim["g"], sim["bp_rp"], version="ii", k=80)
    w = np.bincount(rng.integers(0, 300, 300), minlength=300).astype(float)
    idx = np.repeat(np.arange(300), w.astype(int))
    lik2 = M.Lik(sim["l"][idx], sim["b"][idx], sim["plx"][idx], sim["err"][idx], sim["g"][idx],
                 sim["bp_rp"][idx], version="ii", k=80)
    assert lik.lnl("flat", (2.5, 0.8), w) == pytest.approx(lik2.lnl("flat", (2.5, 0.8)), rel=1e-9)


def test_simulate_applies_every_cut():
    rng = np.random.default_rng(2)
    lf = bright_lf(rng, mg=0.0)
    declared = {"bp_rp": [{"side": "upper", "c": 1.9}], "b": [{"side": "lower", "c": -25.0}]}
    sim = M.simulate(rng, 2000, sigma=2.7, q=1.0, lf=lf, ext=(1.0, 5.0), errs=errs(rng), declared=declared)
    assert np.all(sim["plx"] < 1.0) and np.all(sim["bp"] < 15.5)
    assert np.all((sim["bp_rp"] > 1.0) & (sim["bp_rp"] < 1.9)) and np.all(sim["b"] >= -25.0)
    assert np.all(sim["plx"] < M.lum_cut(sim["g"], sim["bp_rp"]))
    assert np.all(np.abs(sim["l"]) < 30) and np.all(np.abs(sim["b"]) < 30)


def test_completeness_thins_low_latitude():
    rng = np.random.default_rng(3)
    lf, er = bright_lf(rng), errs(rng)
    a = M.simulate(rng, 5000, sigma=2.7, q=1.0, lf=lf, ext=(0.0, 5.0), errs=er, bmin=5.0)
    b = M.simulate(rng, 5000, sigma=2.7, q=1.0, lf=lf, ext=(0.0, 5.0), errs=er, bmin=5.0, completeness=True)
    assert np.mean(np.abs(b["b"]) < 8) < np.mean(np.abs(a["b"]) < 8)


def test_lf_dereddening_round_trip():
    rng = np.random.default_rng(6)
    lf = bright_lf(rng, mg=-1.0)
    mg0, c0, _ = lf.intrinsic(0.0, 5.0)
    assert np.allclose(mg0, -1.0, atol=1e-9) and np.allclose(c0, lf.c)
    mg1, c1, _ = lf.intrinsic(2.0, 5.0)
    assert np.all(mg1 <= mg0 + 1e-12) and np.all(c1 <= c0 + 1e-12)


def test_extinction_grid_finds_the_input():
    rng = np.random.default_rng(8)
    lf, er = bright_lf(rng, mg=-1.5), errs(rng)
    truth = M.simulate(np.random.default_rng(99), 3000, sigma=2.7, q=1.0, lf=lf, ext=(1.5, 6.0), errs=er)
    res = M.extinction_grid(truth["b"], truth["bp_rp"], n_target=3000, lf=lf, errs=er, a_values=[0.0, 1.5, 3.0],
                            bd_values=[2.0, 6.0, 15.0], seed=1)
    assert (res["a"], res["b_d"]) == (1.5, 6.0)


def test_err_sampler_uses_bin_and_nearest():
    es = M.ErrSampler(np.array([10.1, 10.2, 12.1]), np.array([0.01, 0.02, 0.05]))
    rng = np.random.default_rng(0)
    assert set(es.draw(rng, np.full(50, 10.15))) <= {0.01, 0.02}
    assert set(es.draw(rng, np.full(10, 11.0))) <= {0.01, 0.02, 0.05}
    assert set(es.draw(rng, np.full(10, 14.0))) == {0.05}


def test_q_interval():
    qs = np.arange(0.2, 1.51, 0.05)
    td = ((qs - 0.6) / 0.1) ** 2
    iv = M.q_interval(qs, td)
    assert iv["lo"] == pytest.approx(0.6 - 0.196, abs=0.01) and iv["hi"] == pytest.approx(0.6 + 0.196, abs=0.01)
    assert iv["flag"] == ""
    iv = M.q_interval(qs, np.zeros_like(qs))
    assert (iv["lo"], iv["hi"]) == (pytest.approx(0.2), pytest.approx(1.5))
    td = np.where(np.abs(qs - 0.8) < 0.08, 5.0, 0.0) + np.where(qs > 1.2, 10.0, 0.0)   # interior bump
    iv = M.q_interval(qs, td)
    assert iv["flag"] == "more than two crossings" and iv["lo"] == pytest.approx(0.2)
    assert 1.15 < iv["hi"] < 1.25


def test_step_labels():
    assert M.step1_label(12, {"lo": 0.4, "hi": 0.7}) == "flattened preferred"
    assert M.step1_label(12, {"lo": 1.1, "hi": 1.3}) == "prolate preferred"
    assert M.step1_label(9, {"lo": 0.4, "hi": 0.7}) == "spherical adequate"
    assert M.step1_label(12, {"lo": 0.6, "hi": 0.85}) == "spherical adequate"
    assert M.step2_label(M.delta_bic(105.0, 100.0, 1000)) == "flattened Gaussian adequate"
    assert M.step2_label(M.delta_bic(110.0, 95.0, 1000)) == "power law preferred"


def test_f5():
    assert M.f5_sph(2.7) == pytest.approx(chi2.cdf((5 / 2.7) ** 2, 3))
    assert M.f5_flat(2.7, 1.0) == pytest.approx(M.f5_sph(2.7), rel=1e-9)
    assert M.f5_flat(2.7, 0.5) > M.f5_sph(2.7)
    assert 0 < M.f5_pow(0.5, 3.4, 1.0) < M.f5_pow(0.5, 4.5, 1.0) < 1
    # power law with alpha -> 0 (uniform density): fraction = (5/18)^3
    assert M.f5_pow(0.5, 1e-9, 1.0) == pytest.approx((5 / 18) ** 3, rel=1e-3)


def test_timing_small():
    t = M.time_evaluations(200, k=50, n_eval=1)
    h = M.project_hours(t, n_stars=200)
    assert h["total"] > 0 and set(t) >= {"i_sph_s", "ii_sph_s", "ii_flat_s", "ii_pow_s"}


# ---------------------------------------------------------------------------------------------
# data012

def test_map_columns():
    m = D.map_columns(["source_id", "[M/H]", "TEFF", "phot_g_mean_mag", "bp_rp", "parallax"], D.MH_CANDIDATES,
                      D.MH_REQUIRED)
    assert m["mh"] == "[M/H]" and m["teff"] == "TEFF" and m["g"] == "phot_g_mean_mag" and m["parallax_error"] is None
    with pytest.raises(D.StopRun, match="several"):
        D.map_columns(["source_id", "mh", "feh"], D.MH_CANDIDATES, D.MH_REQUIRED)
    with pytest.raises(D.StopRun, match="no column"):
        D.map_columns(["source_id", "teff"], D.MH_CANDIDATES, D.MH_REQUIRED)


def test_duplicates():
    df = pd.DataFrame({"source_id": list(range(1000)) + [5], "mh": 0.0})
    out, rec = D.drop_duplicates(df, "x")
    assert len(out) == 999 and rec["rows_dropped"] == 2
    df = pd.DataFrame({"source_id": list(range(100)) + [5], "mh": 0.0})
    with pytest.raises(D.StopRun):
        D.drop_duplicates(df, "x")


def test_units_and_sign():
    j = pd.DataFrame({"mh": [0.0, 0.1, -2.0], "jphi": [-100.0, -200.0, 5.0], "rapo": [8.0, 9.0, 3.0]})
    assert D.check_units(j)["jphi_flipped"]
    j["rapo"] = [8000.0, 9000.0, 3.0]
    with pytest.raises(D.StopRun, match="R_apo"):
        D.check_units(j)
    j["rapo"] = 8.0
    j["jphi"] = [0.0, 0.0, 1.0]
    with pytest.raises(D.StopRun, match="J_phi"):
        D.check_units(j)


def test_detect_cuts():
    rng = np.random.default_rng(0)
    snr = rng.exponential(10.0, 200000)
    cuts, _ = D.detect_cuts(snr[snr > 5.0], -np.inf, np.inf, 0.1)
    assert cuts == [{"side": "lower", "c": pytest.approx(5.0)}]
    cuts, _ = D.detect_cuts(rng.normal(3.0, 4.0, 200000), -np.inf, np.inf, 0.1)   # smooth tails: no cut
    assert cuts == []
    b = rng.uniform(-30, 30, 100000)
    assert D.detect_cuts(b, -30, 30, 0.5)[0] == []                  # R22's own limits are not cuts
    cuts, _ = D.detect_cuts(b[np.abs(b) < 20], -30, 30, 0.5)
    assert {c["side"] for c in cuts} == {"upper", "lower"}
    assert D.detect_cuts(b[np.abs(b) > 2], -30, 30, 0.5)[0] == []   # a hole is not a cut


def test_l6_parallax_dependent():
    rng = np.random.default_rng(1)
    plx = rng.normal(0.12, 0.05, 100000)
    err = np.full(plx.size, 0.02)
    df = pd.DataFrame({"parallax": plx, "parallax_error": err})
    assert not D.l6_checks(df)["parallax_dependent_cut"]
    keep = plx / err > 5
    l6 = D.l6_checks(df[keep])
    assert l6["parallax_dependent_cut"] and "parallax_over_error" in l6["declared"]
    assert l6["snr_below_1_rule"]["declared"]


def test_t1_labels():
    c = {"lt_m2": 4500, "lt_m1p5": 18500, "m2p7_to_m1p5": 18100, "lt_m1": 95000, "total": 1_500_000}
    t = D.t1_labels(c)
    assert t["summary"] == "abstract reproduced"
    st = t["statements"]
    assert st["abstract"]["sample_differs"] and st["abstract"]["fraction_label"] == "disagrees"
    assert st["s3_lt_m2"]["count_label"] == "agrees" and st["f4_lt_m2"]["count_label"] == "disagrees"
    assert st["s3_lt_m1"]["count_label"] == "agrees" and st["s4_lt_m1"]["count_label"] == "disagrees"
    assert t["pairs"]["18,000/20,000"]["supports"] == "first"
    assert t["pairs"][">4,000/5,000"]["supports"] == "first"
    assert t["pairs"]["100,000/70,000"]["supports"] == "first"
    c["m2p7_to_m1p5"] = 18901
    assert D.t1_labels(c)["summary"] == "not reproduced"
    assert D.agrees(99999, "almost100k", 100000) and not D.agrees(100000, "almost100k", 100000)


def test_wrap_l():
    assert np.allclose(D.wrap_l([359.0, 1.0, 180.0, 181.0]), [-1.0, 1.0, 180.0, -179.0])


# ---------------------------------------------------------------------------------------------
# kin012

def test_boot_subset_size():
    rng = np.random.default_rng(0)
    ks = [K.boot_subset(rng, 1000, 100).size for _ in range(2000)]
    assert np.mean(ks) == pytest.approx(100, abs=1.0) and np.var(ks) == pytest.approx(90, rel=0.15)


def test_bins_and_logistic():
    cs = [-2.0, -1.8, -1.6, -1.4, -1.2, -1.0, -0.8, -0.6]
    j = K.bin_index(np.array([-2.1, -2.0999, -0.5, -0.5001, -1.05, -2.2]), cs, 0.2)
    assert list(j) == [0, 0, -1, 7, 5, -1]
    x = np.array(cs)
    y = K.logistic(x, 0.0, 0.8, -1.2, 0.15)
    fit = K.fit_logistic(x, y, np.full(8, 1e-4))
    assert fit["converged"] and fit["width"] == pytest.approx(2 * np.log(9) * 0.15, rel=1e-3)


def test_t3_labels():
    assert K.label_a([-0.03, 0.04]) == "no net rotation"
    assert K.label_a([0.01, 0.07]) == "net rotation"
    assert K.label_a([-0.09, -0.06]) == "net counter-rotation"
    assert K.label_a([-0.09, 0.02]) == "undetermined"
    assert K.label_b([0.55, 0.7]) == "rotation dominated" and K.label_b([0.3, 0.45]) == "not rotation dominated"
    assert K.label_c(True, [0.2, 0.35], 0.3) == "sharp"
    assert K.label_c(True, [0.45, 0.8], 0.3) == "gradual"
    assert K.label_c(True, [0.45, 0.8], 0.4) == "undetermined"
    assert K.label_c(False, [0.2, 0.3], 0.3) == "undetermined (fit failed)"


def test_t3_full_and_w0():
    rng = np.random.default_rng(3)
    mh = rng.uniform(-2.6, 0.0, 30000)
    f = np.where(mh < -1.0, 0.0, 0.8) + rng.normal(0, 0.2, mh.size)
    cs = [-2.0, -1.8, -1.6, -1.4, -1.2, -1.0, -0.8, -0.6]
    w0 = K.w0_mocks(mh, f, rng, n_mocks=5, err=0.1, centers=cs, width=0.2, n_boot=50)
    assert 0.15 < w0["w0"] < 0.5
    s = K.T3Sample(mh + rng.normal(0, 0.1, mh.size), f, cs, 0.2)     # observed [M/H] blurred by 0.1 dex
    r = K.t3_full(s, rng, 50, 100, w0["w0"])
    assert r["a_label"] == "no net rotation" and r["b_label"] == "not rotation dominated"   # bin mean 0.4 (straddles the step)
    assert r["logistic"]["converged"] and r["c_label"] in ("sharp", "undetermined")
    step = K.fit_logistic(np.array(cs), np.r_[np.zeros(5), np.full(3, 0.8)], np.full(8, 1e-4))
    assert step["at_bound"] and not step["converged"]          # a step between two bins: s at its bound


def test_t5():
    rng = np.random.default_rng(2)
    ecc = np.r_[np.full(50, 0.9), np.full(950, 0.2)]
    rapo = np.r_[np.full(50, 12.0), np.full(950, 3.0)]
    r = K.t5_fractions(ecc, rapo, rng, 500)
    assert r["g"] == pytest.approx(0.05) and r["g_label"] == "minor"
    assert r["a5_label"] == "most apocentres below 5 kpc confirmed"


# ---------------------------------------------------------------------------------------------
# stats012

def test_t2a_label_order():
    assert S.t2a_reproduction(True, 2.7, False) == S.MISSING
    assert S.t2a_reproduction(False, 2.7, True) == "not reproduced"
    assert S.t2a_reproduction(False, 2.9, False) == "reproduced"
    assert S.t2a_population(False, True, 0.5, True, [2.5, 2.6]) == "undetermined (fit at bound)"
    assert S.t2a_population(False, False, 0.15, True, [2.5, 2.6]) == "undetermined (method bias)"
    assert S.t2a_population(False, False, 0.05, True, [2.5, 2.6]) == "undetermined (unmodelled selection)"
    assert S.t2a_population(False, False, 0.05, False, [2.5, 2.6]) == "consistent with 2.7 kpc"
    assert S.t2a_population(False, False, 0.05, False, [3.1, 3.3]) == "different"
    assert S.t2a_population(False, False, 0.05, False, [2.9, 3.3]) == "undetermined"


def test_t2b_shape_and_f5():
    assert S.t2b_shape(False, False, True, "flattened preferred") == ("undetermined (checks failed)", "sph")
    assert S.t2b_shape(False, True, True, "spherical adequate") == ("spherical adequate", "sph")
    assert S.t2b_shape(False, True, True, "prolate preferred") == ("prolate preferred", "flat")
    assert S.t2b_shape(False, True, True, "flattened preferred", False, "power law preferred") == \
        ("flattened (step 2 undetermined)", "flat")
    assert S.t2b_shape(False, True, True, "flattened preferred", True, "power law preferred") == \
        ("power law preferred", "pow")
    assert S.t2b_f5("undetermined (method bias)", [0.6, 0.7]) == "undetermined (method bias)"
    assert S.t2b_f5("undetermined", [0.6, 0.7]) == "most within 5 kpc confirmed"
    assert S.t2b_f5("different", [0.3, 0.45]) == "not confirmed"


def test_t4_label():
    base = {"sigma_ii": 2.7, "a_label": "no net rotation", "b_label": "rotation dominated", "mass": 1e8}
    ok = {"sigma_ii": 2.8, "a_label": "no net rotation", "b_label": "rotation dominated", "mass": 2e8}
    assert S.t4_label(base, {"v": ok}, False) == ("robust", [])
    bad = dict(ok, sigma_ii=3.1, mass=4e8, b_label="undetermined")
    lab, broken = S.t4_label(base, {"v": bad}, False)
    assert lab == "sensitive" and set(broken) == {("v", "sigma"), ("v", "T3 (b)"), ("v", "T6 mass")}
    assert S.t4_label(base, {"v": dict(ok, sigma_ii=None)}, True)[0] == "robust"
    noise = {"sigma_ii": 2.7, "a_changed": True, "b_changed": False, "mass": 1e8}
    assert S.t4_label(base, {"n": noise}, False) == ("sensitive", [("n", "T3 (a)")])


def test_t5_labels():
    assert S.label_g([0.02, 0.08]) == "minor" and S.label_g([0.12, 0.2]) == "moderate"
    assert S.label_g([0.3, 0.4]) == "major" and S.label_g([0.08, 0.12]) == "undetermined"
    assert S.label_a5([0.3, 0.45]) == "not confirmed"


def test_readings():
    assert S.reading_reproduction("abstract reproduced", "reproduced", "no net rotation", "rotation dominated")[0] \
        == "R22's numbers reproduce from the public sample"
    assert S.reading_reproduction("abstract reproduced", "reproduced", "net rotation", "undetermined") == \
        ("not reproduced", ["T3 (a)"])
    assert S.reading_reproduction("abstract reproduced", S.MISSING, "no net rotation", "undetermined") == \
        ("partly reproduced", ["T2a", "T3 (b)"])
    good = ("consistent with 2.7 kpc", "most within 5 kpc confirmed", "robust", "moderate",
            "most apocentres below 5 kpc confirmed")
    assert S.reading_robustness(*good)[0] == "holds under our checks"
    assert S.reading_robustness("undetermined (method bias)", "undetermined (method bias)", "robust", "major",
                                "not confirmed") == ("challenged", ["T5 g", "T5 a5"])
    assert S.reading_robustness("undetermined", *good[1:])[0] == "undetermined"
