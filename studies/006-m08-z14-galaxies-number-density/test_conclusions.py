"""Assertions that this study's results are complete and internally consistent, read from results/.

Run the study first: python -m astrolab run 006-m08-z14-galaxies-number-density
These check that each pre-registered criterion (README section 2) was evaluated as written.
"""
import json
import math
from pathlib import Path

import pytest

RESULTS = Path(__file__).parent / "results"


def load(name):
    path = RESULTS / f"{name}.json"
    if not path.exists():
        pytest.skip(f"{path.name} missing; run the study first")
    return json.loads(path.read_text(encoding="utf-8"))


def test_r1_verdicts_follow_tolerances():
    r1 = load("r1")
    ok = abs(r1["log_phi"] + 5.36) < 0.01 and abs(r1["err_hi"] - 0.37) < 0.05 and abs(r1["err_lo"] - 0.45) < 0.05
    assert r1["verdict_density"] == ("reproduced" if ok else "not reproduced")
    assert r1["verdict_volume"] == ("reproduced" if abs(r1["volume_ratio"] - 1) < 0.05 else "not reproduced")
    assert r1["mod_poisson_bound_holds"] == (r1["p_tail_n26_ppm"] <= 200 and r1["p_tail_ratio100_ppm"] <= 200)


def test_r2_verdict_follows_ratio():
    r2 = load("r2")
    if r2.get("verdict") == "not evaluable":
        pytest.skip(r2.get("reason"))
    ratio = r2["ratio_to_n26"]
    want = "same order as N26's baseline" if 1 / 3 <= ratio <= 3 else ("higher" if ratio > 3 else "lower")
    assert r2["verdict"] == want
    assert r2["robustness"] in ("robust", "calibration-dependent", "not assessable")
    assert r2["variant_counts"]["total"] == 72


def _overlap(roots, target):
    lo, hi = roots["lower"], roots["upper"]
    a = float("-inf") if lo["censored"] == "le" else lo["value"]
    b = float("inf") if hi["censored"] == "gt" else hi["value"]
    return "consistent with N26" if (a <= target[1] and b >= target[0]) else "different"


def test_r3_verdict_and_roots():
    r3 = load("r3")
    if r3.get("verdict") == "not evaluable":
        pytest.skip(r3.get("reason"))
    roots = r3["sigma_roots"]
    assert roots["upper"]["value"] >= roots["central"]["value"] >= roots["lower"]["value"]
    assert r3["verdict"] == _overlap(roots, r3["target"])


def _robust(rows, key, fid, n_min=48):
    if fid in (None, "not evaluable") or len(rows) < n_min:
        return "not assessable"
    return "robust" if all(r[key] == fid for r in rows) else "calibration-dependent"


def test_robustness_rederived():
    r2, r3, var = load("r2"), load("r3"), load("variants")
    rows = var["rows"]
    if not rows:
        pytest.skip("variants not run")
    ev = [v for v in rows if v["evaluable"]]
    assert r2["robustness"] == _robust(ev, "r2", r2.get("verdict"))
    ev3 = [v for v in ev if v.get("r3_evaluable")]
    assert r3["robustness"] == _robust(ev3, "r3", r3.get("verdict"))
    for v in ev3:
        assert v["r3"] == _overlap(v["sigma_roots"], r3["target"])


def test_result_files_small():
    for path in RESULTS.glob("*.json"):
        assert path.stat().st_size < 1024 ** 2, path.name


def _post_label(probs, n_eff, thr=0.95):
    best = max(probs, key=probs.get)
    p = probs[best]
    se = (p * (1 - p) / n_eff) ** 0.5
    if p - 2 * se >= thr:
        return f"robust to the calibration uncertainty ({best})"
    return "calibration-uncertain (borderline)" if p >= thr else "calibration-uncertain"


def test_r23_post_rules():
    """R2/R3-POST (README section 2, addendum 2026-11-16): probabilities, Monte Carlo rule, labels and
    their precedence recomputed from the saved per-draw verdicts."""
    post = load("post")
    for name, fit in post.items():
        r2v, r3v = fit["r2_verdicts"], fit["r3_verdicts"]
        n = len(r2v)
        assert n == 500 and len(r3v) == n and len(fit["ratios"]) == n and len(fit["r3_roots"]) == n, name
        for ratio, v in zip(fit["ratios"], r2v):
            exp = "same order as N26's baseline" if 1 / 3 <= ratio <= 3 else ("higher" if ratio > 3 else "lower")
            assert v == exp
        p2 = {k: r2v.count(k) / n for k in ("higher", "same order as N26's baseline", "lower")}
        assert p2 == fit["r2_probabilities"] and abs(sum(p2.values()) - 1) < 1e-12
        for roots, v in zip(fit["r3_roots"], r3v):     # R3 verdicts re-derived from each draw's roots
            if roots is None:
                assert v == "not evaluable"
                continue
            lo, hi = roots["lower"], roots["upper"]
            a = float("-inf") if lo["censored"] == "le" else lo["value"]
            b = float("inf") if hi["censored"] == "gt" else hi["value"]
            assert v == ("consistent with N26" if (a <= 2.0 and b >= 1.5) else "different")
        ev3 = [v for v in r3v if v != "not evaluable"]
        n_eff_chain = 32 * fit["n_post_steps"] / max(fit["tau"])
        assert abs(fit["n_eff"] - min(n, n_eff_chain)) < 1e-6
        assert fit["converged"] == (fit["n_post_steps"] >= 50 * max(fit["tau"]))
        bounded = any(max(b["lower"], b["upper"]) > 0.05 for b in fit["bound_fractions"].values())
        assert fit["prior_bounded"] == bounded

        fq = fit["lsq"]["n_bootstrap_failed"] <= 20 and fit["lsq"]["n_bootstrap"] > 0
        assert fit["lsq"]["fit_quality_determined"] == fq
        assert fit["lsq"]["n_bootstrap"] + fit["lsq"]["n_bootstrap_failed"] == 200

        def label(probs, evaluable, n_draws):
            if not fit["lsq"]["success"] or not fit["converged"] or not evaluable:
                return "not evaluable"
            lab = _post_label(probs, min(n_draws, n_eff_chain))
            if fq and fit["lsq"]["p_bootstrap"] < 0.01:
                lab = "model misfit (probabilities reported, not a verdict)"
            return lab + ("; prior-bounded" if bounded else "")
        assert fit["r2_label"] == label(p2, True, n), name
        if not ev3:
            assert fit["r3_label"] == "not evaluable", name
        if ev3:
            p3 = {k: ev3.count(k) / len(ev3) for k in ("consistent with N26", "different")}
            assert p3 == fit["r3_probabilities"]
            assert fit["r3_label"] == label(p3, len(ev3) >= 0.9 * n, len(ev3)), name
    s = load("summary")
    assert s["R2_post"]["r2_label"] == post["primary"]["r2_label"]
    assert s["R2_post"]["r2_probabilities"] == post["primary"]["r2_probabilities"]
    assert s["R3_post"]["r3_probabilities"] == post["primary"]["r3_probabilities"]
    assert s["R3_post"]["r3_label"] == post["primary"]["r3_label"]


def test_r3_post2_rules():
    """R3-POST2 (README section 2, addendum 2026-11-17): six-parameter fit with sigma_cal sampled;
    probabilities, labels, the sigma_cal identifiability label and the per-bin counts recomputed."""
    fit = load("post2")
    r2v, r3v, sig = fit["r2_verdicts"], fit["r3_verdicts"], fit["sigma_cal_draws"]
    n = len(r2v)
    assert n == 500 and len(r3v) == n and len(sig) == n and len(fit["r3_roots"]) == n
    assert [r[1] for r in fit["poisson_rows"]] == [2, 9]
    assert len(fit["tau"]) == 6 and set(fit["bound_fractions"]) == {"eps0", "log_m1", "beta", "gamma", "f",
                                                                     "sigma_cal"}
    assert all(0.3 <= s <= 1.2 for s in sig) and all(-1.0 <= g <= 3.0 for g in fit["gamma_draws"])
    for ratio, v in zip(fit["ratios"], r2v):
        exp = "same order as N26's baseline" if 1 / 3 <= ratio <= 3 else ("higher" if ratio > 3 else "lower")
        assert v == exp
    for roots, v in zip(fit["r3_roots"], r3v):
        if roots is None:
            assert v == "not evaluable"
            continue
        lo, hi = roots["lower"], roots["upper"]
        a = float("-inf") if lo["censored"] == "le" else lo["value"]
        b = float("inf") if hi["censored"] == "gt" else hi["value"]
        assert v == ("consistent with N26" if (a <= 2.0 and b >= 1.5) else "different")
    p2 = {k: r2v.count(k) / n for k in ("higher", "same order as N26's baseline", "lower")}
    assert p2 == fit["r2_probabilities"]
    ev3 = [v for v in r3v if v != "not evaluable"]
    assert all(t is not None for t in fit["tau"])
    n_eff_chain = 32 * fit["n_post_steps"] / max(fit["tau"])
    assert fit["converged"] == (fit["n_post_steps"] >= 50 * max(fit["tau"]))
    draws = fit["draws"]
    assert len(draws) == n and [d[5] for d in draws] == sig and [d[3] for d in draws] == fit["gamma_draws"]
    box = {"eps0": (-6.0, 0.0), "log_m1": (9.0, 13.0), "beta": (0.0, 3.0), "gamma": (-1.0, 3.0),
           "f": (0.01, 3.0), "sigma_cal": (0.3, 1.2)}
    lo_box = [1e-6, 9.0, 0.0, -1.0, 0.01, 0.3]
    hi_box = [1.0, 13.0, 3.0, 3.0, 3.0, 1.2]
    assert all(lo_box[j] <= d[j] <= hi_box[j] for d in draws for j in range(6))
    for j, (name, (lo, hi)) in enumerate(box.items()):    # bound fractions re-derived from the draws
        x = [math.log10(d[j]) if name == "eps0" else d[j] for d in draws]
        w = 0.01 * (hi - lo)
        assert fit["bound_fractions"][name]["lower"] == pytest.approx(sum(v <= lo + w for v in x) / n)
        assert fit["bound_fractions"][name]["upper"] == pytest.approx(sum(v >= hi - w for v in x) / n)
    bounded = any(max(b["lower"], b["upper"]) > 0.05 for b in fit["bound_fractions"].values())
    assert fit["prior_bounded"] == bounded
    q = fit["posterior"]["sigma_cal"]
    width = q["p84"] - q["p16"]
    assert abs(fit["sigma_cal_68_width"] - width) < 1e-12
    assert fit["sigma_cal_prior_dominated"] == (width > 0.6 * 0.9)
    tag = "; sigma_cal prior-dominated" if fit["sigma_cal_prior_dominated"] else ""
    fq = fit["lsq"]["n_bootstrap_failed"] <= 20 and fit["lsq"]["n_bootstrap"] > 0
    assert fit["lsq"]["fit_quality_determined"] == fq
    assert fit["lsq"]["n_bootstrap"] + fit["lsq"]["n_bootstrap_failed"] == 200

    def label(probs, evaluable, n_draws):
        if not fit["lsq"]["success"] or not fit["converged"] or not evaluable:
            return "not evaluable" + tag
        lab = _post_label(probs, min(n_draws, n_eff_chain))
        if fq and fit["lsq"]["p_bootstrap"] < 0.01:
            lab = "model misfit (probabilities reported, not a verdict)"
        return lab + ("; prior-bounded" if bounded else "") + tag
    assert fit["r2_label"] == label(p2, True, n)
    if ev3:
        p3 = {k: ev3.count(k) / len(ev3) for k in ("consistent with N26", "different")}
        assert p3 == fit["r3_probabilities"]
        assert fit["r3_label"] == label(p3, len(ev3) >= 0.9 * n, len(ev3))
    else:
        assert fit["r3_label"] == "not evaluable" + tag
    assert fit["fraction_gamma_negative"] == sum(g < 0 for g in fit["gamma_draws"]) / n
    bins = fit["r3_by_sigma_cal_bin"]
    assert len(bins) == 9 and sum(b["n_draws"] for b in bins) == n
    for b in bins:
        lo, hi = b["sigma_cal"]
        sel = [v for v, s in zip(r3v, sig) if lo <= s < hi or (hi == bins[-1]["sigma_cal"][1] and s == hi)]
        ev = [v for v in sel if v != "not evaluable"]
        assert b["n_draws"] == len(sel)
        assert b["p_r3_consistent"] == ((ev.count("consistent with N26") / len(ev)) if ev else None)
    s = load("summary")
    assert s["R3_post2"]["r3_label"] == fit["r3_label"] and s["R3_post2"]["r2_label"] == fit["r2_label"]
