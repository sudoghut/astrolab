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
    anchor_ok = load("r2")["anchor_step"]["verdict"] == "reproduced"
    prefix = "" if anchor_ok else "conditional (anchor rule not validated): "
    assert h["verdict"].startswith(prefix + exp) and s["R2_host"] == h["verdict"]
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
    th = est["tau_hat"]
    for end, sgn in ((hi, 1), (lo, -1)):
        side = sorted((i for i in range(len(g)) if (g[i] - th) * sgn > 0), key=lambda i: abs(g[i] - th))
        first = next((i for i in side if v[i] >= thr), None)
        if first is None:              # no grid point beyond tau_hat reaches the threshold
            assert end == ("> 0.5" if sgn > 0 else 0.0)
            continue
        if end == "not determined":
            continue
        before = [i for i in side if abs(g[i] - th) < abs(g[first] - th)]
        inner = g[before[-1]] if before else th
        a_, b_ = sorted((inner, g[first]))
        assert a_ - 1e-9 <= end <= b_ + 1e-9          # inside the nearest crossing bracket
    assert re_["tau_hat"] == (0.0 if est["at_zero"] else est["tau_hat"])
    assert "diagnostic_errors" not in re_
    sens = re_["sensitivity_cepheid_rows"]
    assert sens["reml"]["at_upper_bound"] or "verdict_row" in sens
    # descriptive diagnostics: internal consistency
    assert re_["r4_under_v"]["draws"] == load("r4")["draws"]          # required when evaluated
    assert "loo_chi2" in re_ and "sensitivity_cepheid_rows" in re_
    for e_, m in zip(re_["interval_68"], est["m2l_at_interval"]):    # each finite end is a +1 crossing
        if isinstance(e_, float) and e_ > 0:
            assert abs(m - thr) < 1e-3
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
    import sys
    here = str(Path(__file__).parent)
    if here not in sys.path:             # run.py imports its helper module rob.py
        sys.path.insert(0, here)
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


def test_fit_failure_classification():
    """Offline: only the pre-registered fit failures make R2-RE 'not evaluable (fit)'."""
    import numpy as np
    run = _run_module()
    assert run.is_fit_failure(np.linalg.LinAlgError("x"))
    assert run.is_fit_failure(ValueError("C is not positive definite: 2-th leading minor"))
    assert run.is_fit_failure(ValueError("L^T C^-1 L is rank deficient (min/max eigenvalue 1e-20)"))
    assert not run.is_fit_failure(ValueError("y has shape (3,), expected (4,)"))
    assert not run.is_fit_failure(RuntimeError("nested-variance identity failed"))


def test_r2_re_rob_labels():
    """README section 2, addendum 2026-11-17 (R2-RE-ROB): re-derive the labels from the saved numbers."""
    from scipy import stats

    rob = load("r2_re_rob")
    if "A" not in rob:
        pytest.skip(rob.get("status", "R2-RE-ROB not run"))
    a = rob["A"]
    if a["status"] == "evaluated":
        bad = [h["host"] for h in a["hosts"]
               if h.get("status") != "evaluated" or h["tau_route"]["row"] != a["r2_re_row"]]
        assert sorted(bad) == sorted(a["sensitive_hosts"])
        assert a["label"] == ("verdict robust to single hosts' influence on tau" if not bad
                              else "verdict sensitive to single hosts' influence on tau")

    def cp(k, n):
        lo = 0.0 if k == 0 else stats.beta.ppf(0.025, k, n - k + 1)
        hi = 1.0 if k == n else stats.beta.ppf(0.975, k + 1, n - k)
        return lo, hi

    def label(k, n, unusual, usual):
        lo, hi = cp(k, n)
        return unusual if hi < 0.05 else usual if lo > 0.05 else "undetermined (Monte Carlo)"

    if a["status"] == "evaluated":                      # rows re-derived from R2's table
        ref = load("r2_re")
        for h in a["hosts"]:
            if "tau_route" in h:
                tr = h["tau_route"]
                z, d, sg = tr["z"], tr["shift"], tr["shift_sigma"]
                if z <= -2 and abs(d - ref["reference"]) <= 2 * sg + 0.02:
                    exp = "supports the paper"
                elif z <= -2:
                    exp = "different size"
                elif abs(z) < 2:
                    exp = "no host-selection effect detected"
                else:
                    exp = "raises H0"
                assert exp in tr["row"], (h["host"], tr["row"])
    t = rob["B"]["tau"]
    if t.get("status", "").startswith("not evaluable (too many"):
        assert t["n_failed"] > 20
    if t.get("status") == "evaluated":
        assert t["n_ok"] + t["n_failed"] == t["n_sims"]
        assert abs(t["p"] - (1 + t["k"]) / (1 + t["n_ok"])) < 1e-12
        k = sum(1 for x in t["taus"] if x >= t["tau_obs"] - 5e-6)   # taus saved rounded to 1e-5
        assert abs(k - t["k"]) <= sum(1 for x in t["taus"] if abs(x - t["tau_obs"]) <= 5e-6)
        assert t["n_failed"] <= 20 and t["n_ok"] == len(t["taus"])
        assert t["label"] == label(t["k"], t["n_ok"], "tau_hat unusual under C (excess calibrator scatter)",
                                   "tau_hat not unusual under C")
    s = rob["B"]["spread"]
    if s.get("status") == "evaluated":
        import math
        assert math.isfinite(s["spread_obs"])
        assert s["label"] == label(s["k"], s["n_sims"], "the R4 excess spread is unusual under C",
                                   "the R4 spread is consistent with C")
        assert abs(s["p"] - (1 + s["k"]) / (1 + s["n_sims"])) < 1e-12


def test_rob_three_way_label():
    """Offline: the Clopper-Pearson three-way rule of R2-RE-ROB."""
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    import rob

    assert rob.three_way(2, 400, "u", "n")[0] == "u"                 # clearly below 0.05
    assert rob.three_way(60, 400, "u", "n")[0] == "n"                # clearly above
    assert rob.three_way(14, 400, "u", "n")[0] == "undetermined (Monte Carlo)"
    lo, hi = rob._cp(0, 10)
    assert lo == 0.0 and 0 < hi < 1


def _row(z, d, sg, ref=-0.0405, extra=0.02):
    """R2's verdict table, written out independently of run.py."""
    if z <= -2 and abs(d - ref) <= 2 * sg + extra:
        return "host selection significantly lowers H0, by the size the paper reports (supports the paper)"
    if z <= -2:
        return "host selection significantly lowers H0, but by a different size"
    if abs(z) < 2:
        return "no host-selection effect detected in these data (does not support the paper's quantitative claim)"
    return "host selection raises H0 (contradicts the paper)"


def test_r2_re_n5584_labels():
    """README section 2, addendum 2026-11-18 (R2-RE-N5584): re-derive every label from the saved numbers
    (the R4-N percentile is taken as saved; per-draw values are not stored)."""
    from scipy import stats

    path = RESULTS / "r2_re_n5584.json"
    out = load("r2_re_n5584")
    assert path.stat().st_size < 1_000_000
    s = load("summary")["R2_RE_N5584"]
    assert s["status"] == out["status"]
    if out["status"] != "evaluated":
        pytest.skip(out["status"])
    re_ = load("r2_re")
    assert out["host"] == "N5584" and out["column"] == 26

    def label(k, n, unusual, usual):
        lo = 0.0 if k == 0 else stats.beta.ppf(0.025, k, n - k + 1)
        hi = 1.0 if k == n else stats.beta.ppf(0.975, k + 1, n - k)
        return unusual if hi < 0.05 else usual if lo > 0.05 else "undetermined (Monte Carlo)"

    # (a) removal
    a = out["drop"]
    assert a["status"] == "evaluated"
    assert a["rows_removed"]["total"] == a["rows_removed"]["calib_sn"] + a["rows_removed"]["cepheid"] \
        + a["rows_removed"]["other"] and a["rows_removed"]["calib_sn"] >= 1
    hs = a["c"]["host_step"]
    assert abs(hs["z"] - hs["shift"] / hs["shift_sigma"]) < 1e-9
    assert a["c"]["row"] == _row(hs["z"], hs["shift"], hs["shift_sigma"])
    rn = a["r2_re"]
    if rn["status"] == "evaluated":
        h = rn["host_step"]
        assert rn["verdict"] == _row(h["z"], h["shift"], h["shift_sigma"])
        assert rn["tau_hat"] == (0.0 if rn["reml"]["at_zero"] else rn["reml"]["tau_hat"])
        assert not rn["reml"]["at_upper_bound"]
    r4n = a["r4n"]
    if "percentile" in r4n:
        assert r4n["cchp_shift"] == hs["shift"]
        p = r4n["percentile"]
        assert r4n["verdict"] == ("the selection itself is systematically low" if p < 5 else
                                  "the selection itself is systematically high" if p > 95 else
                                  "consistent with random-subset fluctuations")
    t, sp = a["bn"].get("tau", {}), a["bn"].get("spread", {})
    if t.get("status") == "evaluated":
        assert t["tau_obs"] == rn["tau_hat"] and t["n_failed"] <= 20
        assert abs(t["p"] - (1 + t["k"]) / (1 + t["n_ok"])) < 1e-12
        assert t["label"] == label(t["k"], t["n_ok"], "tau_hat unusual under C (excess calibrator scatter)",
                                   "tau_hat not unusual under C")
    if sp.get("status") == "evaluated":
        assert abs(sp["p"] - (1 + sp["k"]) / (1 + sp["n_sims"])) < 1e-12
        assert sp["label"] == label(sp["k"], sp["n_sims"], "the R4 excess spread is unusual under C",
                                    "the R4 spread is consistent with C")
    if t.get("status") != "evaluated" or sp.get("status") != "evaluated":
        exp = "not evaluable"
    elif sp["label"] == "the R4 spread is consistent with C" and t["label"] != \
            "tau_hat unusual under C (excess calibrator scatter)":
        exp = "the excess calibrator scatter of R2-RE-ROB is attributable to N5584"
    elif sp["label"] == "the R4 excess spread is unusual under C":
        exp = "excess scatter remains without N5584"
    elif sp["label"] == "the R4 spread is consistent with C":
        exp = "τ excess remains without N5584"
    else:
        exp = "undetermined"
    assert a["reading"] == exp == s["drop_reading"]

    # (b) heavy-tailed host effect
    b = out["heavy_tail"]
    chk = b.get("implementation_check")
    if chk is not None:
        ok = chk["converged"] and abs(chk.get("tau_diff", 1)) <= 1e-4 and abs(chk.get("z_diff", 1)) <= 0.005
        assert chk["passed"] == ok
        if not ok:
            assert b["status"].startswith("not evaluable (implementation check failed")
    m = b.get("nu_main", {})
    assert m.get("nu", 4) == 4
    if b["status"] == "evaluated":
        st = m["starts"]
        assert len(st) == 2 and all(x["converged"] and x["iterations"] <= 10000 for x in st)
        assert abs(st[0]["tau_hat"] - st[1]["tau_hat"]) <= 1e-4
        assert 1e-3 <= m["tau_hat"] < 0.5 - 1e-3 or m["at_zero"]
        r2h = load("r2")["host_step"]
        if m["at_zero"]:
            assert m["row"] == _row(r2h["z"], r2h["shift"], r2h["shift_sigma"])
        h = m["host_step"]
        assert abs(h["z"] - h["shift"] / h["shift_sigma"]) < 1e-9
        assert m["row"] == _row(h["z"], h["shift"], h["shift_sigma"])
        om = [x["omega"] for x in m["omega_ranked"]]
        assert om == sorted(om) and len(om) == 37
        exp_b = ("R2-RE verdict robust to a heavy-tailed host effect" if m["row"] == re_["verdict"] else
                 "R2-RE verdict depends on the host-effect distribution (heavy-tailed: " + m["row"] + ")")
        assert b["label"] == exp_b == s["t_label"]
        if exp_b.startswith("R2-RE verdict robust"):
            assert out["joint_reading"] == ("the null result holds under both removal and down-weighting of "
                                            "N5584; only the hybrid τ route of R2-RE-ROB A flips")
        else:
            assert out["joint_reading"].startswith("the verdict depends on how one host is modelled")
            assert f"{m['z']:.2f}" in out["joint_reading"] and f"{re_['z']:.2f}" in out["joint_reading"]
            assert f"{r2h['z']:.2f}" in out["joint_reading"]
    else:
        assert out["joint_reading"].startswith("no joint reading")
    for r in b.get("nu_sensitivity", []):
        assert r["nu"] in (2, 10)
        if r["status"] == "evaluated":
            h = r["host_step"]
            assert r["row"] == _row(h["z"], h["shift"], h["shift_sigma"])
        else:
            assert r["status"].startswith("reported, not evaluable")


# R2-RE-SEL observed values recorded before the addendum (tau_hat_N, B-N spread_obs); README section 2
SEL_RECORDED = (0.03137144323410943, 1.0325254787240916)


def test_r2_re_sel_labels():
    """README section 2, addendum 2026-11-19 (R2-RE-SEL): re-derive the labels, the reading (rules (1)-(5)
    in order) and the reproduction checks from the saved numbers."""
    from scipy import stats

    path = RESULTS / "r2_re_sel.json"
    out = load("r2_re_sel")
    assert path.stat().st_size < 1_000_000
    s = load("summary")["R2_RE_SEL"]
    assert s["status"] == out["status"]
    ne_obs = "not evaluable (observed values differ from the recorded ones: code or data change)"
    if out["status"] == ne_obs:
        assert out["observed"]["mismatches"] and out["reading"] == s["reading"] == "not evaluable"
        return
    if out["status"] != "evaluated":
        pytest.skip(out["status"])
    assert out["host"] == "N5584"
    ob = out["observed"]
    assert ob["mismatches"] == []
    rt, rs = SEL_RECORDED
    if ob["tau_hat_N"] is not None:
        assert abs(ob["tau_hat_N"] - rt) <= 1e-6 * rt
        drop = load("r2_re_n5584")["drop"]
        assert ob["tau_hat_N"] == drop["r2_re"]["tau_hat"]
    if ob["spread_obs"] is not None:
        assert abs(ob["spread_obs"] - rs) <= 1e-9 * rs

    def label(k, n, unusual, usual):
        lo = 0.0 if k == 0 else stats.beta.ppf(0.025, k, n - k + 1)
        hi = 1.0 if k == n else stats.beta.ppf(0.975, k + 1, n - k)
        return unusual if hi < 0.05 else usual if lo > 0.05 else "undetermined (Monte Carlo)"

    chk = out["checks"]
    if "loo_maps" in chk:
        assert chk["loo_maps"]["max_rel_diff"] <= 1e-8
    t = out["tau"]
    tu, tn = "τ̂_N unusual under the selected null", "τ̂_N not unusual under the selected null"
    if t["status"] == "evaluated":
        assert chk["criterion_x_selects"]["host"] == "N5584"
        assert t["tau_obs"] == ob["tau_hat_N"]
        assert t["n_ok"] + t["n_failed"] == t["n_sims"] and t["n_failed"] <= 20 and t["n_ok"] == len(t["taus"])
        assert abs(t["p"] - (1 + t["k"]) / (1 + t["n_ok"])) < 1e-12
        near = sum(1 for x in t["taus"] if abs(x - t["tau_obs"]) <= 5e-6)   # taus saved rounded to 1e-5
        assert abs(t["k"] - sum(1 for x in t["taus"] if x >= t["tau_obs"])) <= near
        assert t["label"] == label(t["k"], t["n_ok"], tu, tn)
    elif t["status"] == "not evaluable (too many failed fits)":
        assert t["n_failed"] > 20
    for name, c in (("spread_X", "X"), ("spread_S", "S")):
        sp = out[name]
        if sp["status"] != "evaluated":
            continue
        assert sp["spread_obs"] == ob["spread_obs"]
        assert chk["spread_obs_d_host"]["rel_diff"] <= 1e-9
        assert abs(sp["p"] - (1 + sp["k"]) / (1 + sp["n_sims"])) < 1e-12
        near = sum(1 for v in sp["spreads"] if abs(v - sp["spread_obs"]) <= 5e-7)
        assert abs(sp["k"] - sum(1 for v in sp["spreads"] if v >= sp["spread_obs"])) <= near
        assert sp["label"] == label(sp["k"], sp["n_sims"],
                                    f"the 36-host spread is unusual under the selected null ({c})",
                                    f"the 36-host spread is consistent with the selected null ({c})")
        if c == "S":
            cs = chk["criterion_s"]
            assert cs["selects"]["host"] == "N5584" and cs["reproduced"]
            assert abs(cs["host_value"] - cs["expected"]) <= 0.001
        else:
            assert chk["criterion_x_selects"]["host"] == "N5584"
    # reading, rules (1)-(5) in order
    sx, ss = out["spread_X"], out["spread_S"]
    if not all(p["status"] == "evaluated" for p in (t, sx, ss)):
        exp = "not evaluable"
    else:
        cx = sx["label"] == "the 36-host spread is consistent with the selected null (X)"
        cs_ = ss["label"] == "the 36-host spread is consistent with the selected null (S)"
        ux = sx["label"] == "the 36-host spread is unusual under the selected null (X)"
        us = ss["label"] == "the 36-host spread is unusual under the selected null (S)"
        if cx and cs_ and t["label"] != tu:
            exp = ("the excess calibrator scatter of R2-RE-ROB is consistent with one outlying host, "
                   "selection included")
        elif ux or us:
            exp = ("excess scatter remains after removing the most extreme host, selection included "
                   "(criterion " + ("both" if ux and us else "X" if ux else "S") + ")")
        elif cx and cs_:
            exp = "τ excess remains after removing the most extreme host, selection included"
        else:
            exp = "undetermined"
    assert out["reading"] == exp == s["reading"]
    # the dropped-host frequencies recounted from the saved per-simulation hosts
    from collections import Counter
    sel_ = out.get("selection", {})
    host_of = {r["column"]: r["host"] for r in out.get("real_criteria", [])}
    n_sp, n_t = out["settings"]["sel_n_spread"], out["settings"]["sel_n_tau"]
    for c in ("X", "S"):
        if c in sel_:
            dr = sel_[c]["dropped"]
            assert len(dr) == max(n_sp, n_t)
            assert sel_[c]["frequency_all"] == {host_of[j]: k for j, k in sorted(Counter(dr[:n_sp]).items())}
            assert sel_[c]["frequency_first_tau"] == {host_of[j]: k for j, k in sorted(Counter(dr[:n_t]).items())}
            assert sel_[c]["n_host_all"] == sum(1 for j in dr[:n_sp] if host_of[j] == "N5584")
    if "X" in sel_ and "S" in sel_:
        assert sel_["n_same_X_S"] == sum(1 for a, b in zip(sel_["X"]["dropped"][:n_sp], sel_["S"]["dropped"][:n_sp])
                                         if a == b)
