"""Assertions that this study's conclusions still hold, read from results/.

Run the study first: python -m astrolab run 003-m02-hubble-tension-distance-ladder
"""
import json
from pathlib import Path

import pytest

RESULTS = Path(__file__).parent / "results"


def load(name):
    path = RESULTS / f"{name}.json"
    if not path.exists():
        pytest.skip(f"{path.name} missing; run the study first")
    return json.loads(path.read_text(encoding="utf-8"))


def test_summary_exists():
    assert load("summary")


def test_r1_printed_baseline_reproduced():
    r1 = load("r1")
    assert abs(r1["fivelogh0"] - 9.318) < 0.001          # R22: H0 = 73.04
    assert abs(r1["chi2_dof"] - 1.03) < 0.005
    assert r1["verdict"] == "not reproduced"              # the public lstsq file is a different fit


def test_r2_anchor_step_reproduced():
    a = load("r2")["anchor_step"]
    assert a["verdict"] == "reproduced"
    assert abs(a["shift"] - (-0.0158)) <= 0.005


def test_r2_host_step_amended():
    h = load("r2")["host_step"]
    assert h["preregistered_verdict"] == "not evaluable (host identification)"
    assert "amended" in h["status"]
    assert h["z"] <= -2 and abs(h["shift"] - (-0.0405)) <= 2 * h["shift_sigma"] + 0.02
    assert abs(h["shift_check_ay"] - h["shift"]) < 1e-8
    assert abs(h["nested_var_check"] - h["shift_sigma"] ** 2) < 1e-8


def test_host_labelling_unique_cchp_set():
    i = load("host_identification")
    assert i["matching_found"] and not i["alt_changes_cchp_set"]


def test_r3_same_hosts_agree():
    r3 = load("r3")
    assert r3["cchp_match"] == "matched"
    assert abs(r3["d"]) < 2 * r3["sigma_d"]


def test_r4_descriptive():
    r4 = load("r4")
    assert r4["draws"] >= 2000 and 0 <= r4["percentile"] <= 100


def test_r2_re_rule_and_headline():
    """R2-RE (README section 2, addendum 2026-11-16): verdict row recomputed from the saved numbers
    with R2's table, and the headline rule (R2-RE's row is the public host-step verdict)."""
    re_ = load("r2_re")
    s = load("summary")
    h = load("r2")["host_step"]
    assert re_["status"] in ("evaluated", "not run", "not evaluable (bound)") or         re_["status"].startswith("not evaluable (fit")
    if re_["status"] != "evaluated":
        assert s["R2_host_headline_source"] == "R2 (C errors) with qualification; R2-RE " + re_["status"]
        assert h["verdict"] == h["qualified_verdict"]
        if "reml" in re_ and re_["reml"]["at_upper_bound"]:
            assert re_["status"] == "not evaluable (bound)"
        return
    est = re_["reml"]
    assert min(est["grid_m2l"]) >= est["m2l_min"] - 1e-9            # tau_hat is at least the grid minimum
    assert not est["at_upper_bound"]
    hs = re_["host_step"]
    assert abs(hs["z"] - hs["shift"] / hs["shift_sigma"]) < 1e-9
    assert abs(hs["nested_var_check"] - hs["shift_sigma"] ** 2) < 1e-8 * hs["shift_sigma"] ** 2 + 1e-12
    z, d, sh = hs["z"], hs["shift"], hs["shift_sigma"]
    if z <= -2 and abs(d - (-0.0405)) <= 2 * sh + 0.02:
        exp = "host selection significantly lowers H0, by the size the paper reports (supports the paper)"
    elif z <= -2:
        exp = "host selection significantly lowers H0, but by a different size"
    elif abs(z) < 2:
        exp = "no host-selection effect detected in these data (does not support the paper's quantitative claim)"
    else:
        exp = "host selection raises H0 (contradicts the paper)"
    assert re_["verdict"] == exp
    assert h["verdict"].startswith(exp) and s["R2_host"] == h["verdict"]
    assert s["R2_host_headline_source"] == "R2-RE"
    # R2 with C errors stays recorded
    assert h["criterion_outcome"].startswith("host selection significantly lowers H0")
    lo, hi = re_["interval_68"]
    assert not isinstance(lo, float) or lo <= re_["tau_hat"]
    assert not isinstance(hi, float) or hi >= re_["tau_hat"]
    # independent recomputation of the pre-registered search rules from the saved grid
    g, v = est["grid"], est["grid_m2l"]
    k = min(range(len(g)), key=lambda i: v[i])
    assert g[max(k - 1, 0)] - 1e-12 <= est["tau_hat"] <= g[min(k + 1, len(g) - 1)] + 1e-12
    assert est["m2l_min"] <= v[k] + 1e-12
    thr = est["m2l_min"] + 1.0
    if isinstance(hi, float):           # nearest crossing above: first grid point >= thr beyond tau_hat
        j = next(i for i in range(len(g)) if g[i] > est["tau_hat"] and v[i] >= thr)
        assert g[j - 1] - 1e-9 <= hi <= g[j] + 1e-9 or (j - 1 == k and est["tau_hat"] <= hi <= g[j] + 1e-9)
    elif hi == "> 0.5":
        assert all(v[i] < thr for i in range(len(g)) if g[i] > est["tau_hat"])
    if isinstance(lo, float) and lo > 0:
        j = max(i for i in range(len(g)) if g[i] < est["tau_hat"] and v[i] >= thr)
        assert g[j] - 1e-9 <= lo <= g[j + 1] + 1e-9
    elif lo == 0.0:
        assert all(v[i] < thr for i in range(len(g)) if g[i] < est["tau_hat"])
    assert re_["tau_hat"] == (0.0 if est["at_zero"] else est["tau_hat"])
    # descriptive diagnostics: internal consistency
    if "r4_under_v" in re_:
        assert re_["r4_under_v"]["draws"] == load("r4")["draws"]
    if "loo_chi2" in re_:
        for w in ("C", "V"):
            lc = re_["loo_chi2"][w]
            assert abs(lc["chi2"] - sum(x["chi2"] for x in lc["per_host"])) < 1e-6
            assert lc["n_rows"] == sum(x["n_rows"] for x in lc["per_host"]) and len(lc["per_host"]) == 37
    # grid points inside a determined interval lie within min + 1 of the REML minimum
    if isinstance(lo, float) and isinstance(hi, float):
        for t, v in zip(est["grid"], est["grid_m2l"]):
            if lo + 1e-9 < t < hi - 1e-9:
                assert v <= est["m2l_min"] + 1.0 + 1e-6


def _run_module():
    import importlib.util
    spec = importlib.util.spec_from_file_location("run003", Path(__file__).parent / "run.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_reml_objective_matches_error_contrast_likelihood():
    """Offline, synthetic: reml_m2l equals -2 log of the error-contrast likelihood (K^T y with
    K^T X = 0) up to a tau-independent constant."""
    import numpy as np
    from scipy import linalg

    run = _run_module()
    rng = np.random.default_rng(1)
    n, p = 40, 4
    L = np.zeros((n, p))
    L[:, 0] = np.linspace(-1.0, 1.0, n)
    L[:20, 1] = 1.0
    L[20:, 2] = 1.0
    L[:, 3] = rng.normal(size=n)
    A = rng.normal(size=(n, n))
    C = A @ A.T / n + np.eye(n)
    y = rng.normal(size=n)
    groups = [np.arange(0, 5), np.arange(20, 26)]
    rows = np.arange(n)
    K = linalg.null_space(L.T)
    diffs = []
    for tau in (0.0, 0.1, 0.4):
        V = run.with_re(C, groups, tau)
        S = K.T @ V @ K
        z = K.T @ y
        brute = np.linalg.slogdet(S)[1] + z @ np.linalg.solve(S, z)
        diffs.append(run.reml_m2l(L, y, C, rows, groups, tau) - brute)
    assert np.ptp(diffs) < 1e-8


def test_reml_tau_grid_refinement_and_interval():
    """Offline: on a parabola with minimum 0.2 and curvature giving +1 at +-0.05, the estimate and
    the nearest crossings are recovered; flat and increasing profiles hit the documented edges."""
    run = _run_module()
    par = run.reml_tau(lambda t: ((t - 0.2) / 0.05) ** 2, 0.5, 0.01)
    assert abs(par["tau_hat"] - 0.2) < 1e-4 and not par["at_zero"] and not par["at_upper_bound"]
    assert abs(par["interval_68"][0] - 0.15) < 1e-5 and abs(par["interval_68"][1] - 0.25) < 1e-5
    inc = run.reml_tau(lambda t: 100 * t, 0.5, 0.01)
    assert inc["at_zero"] and inc["interval_68"][0] == 0.0 and abs(inc["interval_68"][1] - 0.01) < 1e-6
    flat = run.reml_tau(lambda t: 0.0 * t, 0.5, 0.01)
    assert flat["interval_68"][1] == "> 0.5"
    dec = run.reml_tau(lambda t: -t, 0.5, 0.01)
    assert dec["at_upper_bound"]
