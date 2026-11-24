"""Offline tests of R1-ERRMM (README 2.9, T-064): synthetic data only, no network, no catalogue."""
import importlib.util
import json
import sys
import types
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))


def _import(name):
    spec = importlib.util.spec_from_file_location(f"study010mm_{name}", HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


m0 = _import("m0")
mocks = _import("mocks")
selaux = _import("selaux")
run = _import("run")
VARS = selaux.R1_VARIANTS
NAMES = ["[-0.7, -0.5)", "[-0.5, -0.3)", "[-0.3, -0.1)"]


def test_errmm_params_sets_and_key():
    P = run.PARAMS
    assert P["errmm_pairs"] == [[1.0, 2.81], [1.5, 2.81]] and P["errmm_bins"] == [0, 1, 2]
    assert P["errmm_n_mock"] == 50 and P["errmm_n_boot"] == 100 and P["errmm_boot_f"] == 2.81
    assert (P["errmm_seed_tag"], P["errmm_seed_tag_indep"], P["errmm_boot_tag"], P["errmm_boot_tag_indep"]) == \
        (64, 164, 65, 165)
    assert P["errmm_boot_max_fail"] == 5 and P["errmm_stop_h"] == 16.0 and P["parts"] == ["err"]
    assert "errmm_stop_h" in selaux.NO_KEY_PARAMS
    sets = selaux.errmm_sets(P["errmm_pairs"], P["errmm_bins"], P["mechs"])
    assert len(sets) == 72 and [s["k"] for s in sets] == list(range(72))
    nest = [(g, F, v, b, kind, m) for g, F in ((1.0, 2.81), (1.5, 2.81)) for v in VARS for b in (0, 1, 2)
            for kind in ("null_sn", "null_sp") for m in ("rtau", "rA")]
    assert [(s["g"], s["F"], s["variant"], s["bin"], s["kind"], s["mech"]) for s in sets] == nest
    assert len({s["group"] for s in sets}) == 6 and len(sets) * P["errmm_n_mock"] == 3600
    src = {"run.py": "x"}
    k0 = selaux.checkpoint_key(dict(P), src, b"d")
    assert selaux.checkpoint_key({**P, "errmm_stop_h": 30.0, "parts": ["errmm"]}, src, b"d") == k0
    assert selaux.checkpoint_key({**P, "errmm_n_boot": 10}, src, b"d") != k0


def test_errmm_parts_validation(monkeypatch):
    for bad in (["errmm", "errcal"], ["orig", "errmm"], ["errmm", "err"]):
        monkeypatch.setitem(run.PARAMS, "parts", bad)
        with pytest.raises(ValueError):
            run.main(None)


def test_errmm_streams_and_tags():
    P = dict(run.PARAMS)
    for k, j in ((0, 0), (71, 49), (12, 3)):
        a, b = run.errmm_rngs(P["seed"], P, k, j)
        assert np.array_equal(a.random(3), np.random.default_rng([P["seed"], 64, k, j]).random(3))
        assert np.array_equal(b.random(3), np.random.default_rng([P["seed"], 164, k, j]).random(3))
    rs, ro, ri = run.errmm_boot_rngs(P["seed"], P, 1, 7, "S15N")
    assert np.array_equal(rs.random(3), np.random.default_rng([P["seed"], 65, 1, 7]).random(3))
    assert np.array_equal(ro.random(3), np.random.default_rng([P["seed"], 65, 1, 7, 3]).random(3))
    assert np.array_equal(ri.random(3), np.random.default_rng([P["seed"], 165, 1, 7, 3]).random(3))
    # the resample stream is shared by the variants; the fit streams differ
    r2 = run.errmm_boot_rngs(P["seed"], P, 1, 7, "Full")
    assert np.array_equal(r2[0].random(3), np.random.default_rng([P["seed"], 65, 1, 7]).random(3))
    assert not np.array_equal(r2[1].random(3), np.random.default_rng([P["seed"], 65, 1, 7, 3]).random(3))
    run.errmm_boot_rngs(P["seed"], P, 0, 100, "S15E")              # the unresampled replicate seeds fine
    old = {P[k] for k in P if k.endswith("seed_tag") or k.endswith("seed_tag_indep")} - {64, 164}
    assert not {64, 164, 65, 165} & old


def _synthetic_D(C, variant="Full", n=3000, seed=11):
    rng = np.random.default_rng(seed)
    tau = mocks.latent_power(11.0, 0.82, 0.4, 7.0, n, rng)
    rel = rng.uniform(0.03, 0.14, n)
    A = np.clip(tau * (1 + rel * rng.standard_normal(n)), 0.2, 19.8)
    tab = run._pass_table(C.P, A, rel, None, 1)
    pools = run._pools(tab, rel)
    model = run.onedim(C, A, A * rel, variant != "Full")
    fits = run.fit_mixtures(C, model, model.cells.A, model.cells.w, C.P["kmax"], nstart=3,
                            rng=np.random.default_rng(seed + 1))
    starts = {K: th for K, (th, _) in fits.items()}
    starts[C.P["kmax"] + 1] = m0.mixture_starts(model.cells.A, model.cells.w, C.P["kmax"] + 1, 1,
                                                np.random.default_rng(seed + 2))[0]
    pm = {"mu_old": 11.0, "s_old": 0.82, "w_old": 0.4, "young": [1.5, 7.0]}
    return {"variant": variant, "_n": n, "_starts": starts, "skewnorm": [9.0, np.log(3.0), 0.0],
            "splitnorm": [9.0, np.log(3.0), np.log(2.0)], "power_models": {"primary": pm, "sens": pm}}, pools, A, A * rel


@pytest.mark.parametrize("kind", ["null_sn", "null_sp"])
def test_errmm_g_equal_F_is_r1_mock_errcal(kind):
    """README 2.9 check (b): with g = F, the same D and the same streams a part-A mock is R1-ERRCAL's."""
    C = run.Ctx(dict(run.PARAMS))
    D, pools, _, _ = _synthetic_D(C, variant="S15E")
    mk = lambda: (np.random.default_rng(5), np.random.default_rng(6))
    ref = run.r1_mock_errcal(C, D, kind, "rtau", mk(), pools, 2, 2.0)
    new = run.errmm_mock(C, D, kind, "rtau", mk(), pools, 2, 2.0, 2.0)
    assert new == ref
    for key in ("edge", "n_sig_lo", "n_sig_hi", "n_mu_lo", "n_mu_hi"):
        assert key in new


def test_errmm_g_not_F_draws_with_g_and_fits_with_F(monkeypatch):
    C = run.Ctx(dict(run.PARAMS))
    D, pools, _, _ = _synthetic_D(C)
    seen = {}
    cat0, fit0 = run.selfit_catalogue, run.selfit_fits
    monkeypatch.setattr(run, "selfit_catalogue", lambda *a, **kw: (seen.__setitem__("g", kw["f"]), cat0(*a, **kw))[1])
    monkeypatch.setattr(run, "selfit_fits", lambda *a, **kw: (seen.__setitem__("F", kw["f"]), fit0(*a, **kw))[1])
    run.errmm_mock(C, D, "null_sp", "rA", (np.random.default_rng(1), np.random.default_rng(2)), pools, 2, 1.0, 2.81)
    assert seen == {"g": 1.0, "F": 2.81}


def test_mixture_bounds():
    th = np.array([25.0, 9.0, -5.0, np.log(0.1), np.log(10.0), np.log(0.1) + 1e-7, 0.0, 0.0])
    assert run.mixture_bounds(th, 3) == {"n_sig_lo": 2, "n_sig_hi": 1, "n_mu_lo": 1, "n_mu_hi": 1}
    assert run.mixture_bounds(np.array([9.0, np.log(2.0)]), 1) == {"n_sig_lo": 0, "n_sig_hi": 0, "n_mu_lo": 0,
                                                                     "n_mu_hi": 0}


def test_errmm_resample_and_boot_fit(monkeypatch):
    rng = np.random.default_rng(0)
    idx = run.errmm_resample(50, 3, 100, np.random.default_rng([0, 65, 0, 3]))
    assert len(idx) == 50 and idx.min() >= 0 and idx.max() < 50
    assert np.array_equal(idx, np.random.default_rng([0, 65, 0, 3]).integers(0, 50, 50))
    assert np.array_equal(run.errmm_resample(50, 100, 100, rng), np.arange(50))
    C = run.Ctx(dict(run.PARAMS))
    Ap = np.array([5.0, 8.0, 10.0, -1.0, 12.0])
    Ep = np.array([0.5, 2.0, 1.0, 0.1, 0.6])          # e/A: 0.10, 0.25, 0.10, (A <= 0), 0.05
    got = {}

    def fake_fits(C_, D_, cat, par, rngs, nstart, f=1.0):
        got.update(cat=cat, par=par, D=D_, f=f)
        return {"d": 0.2, "valley": True, "k": 3, "pass_rate": 99.0}
    monkeypatch.setattr(run, "selfit_fits", fake_fits)
    r = run.errmm_boot_fit(C, {"variant": "S15E", "_starts": {}}, Ap, Ep, "S15E", (None, None), 8, 2.81)
    assert list(got["cat"]["A"]) == [5.0, 10.0, 12.0] and list(got["par"]["A"]) == list(Ap) and got["f"] == 2.81
    assert r["pass_rate"] == pytest.approx(3 / 5) and r["n"] == 3 and r["fit_fail"] is False
    r = run.errmm_boot_fit(C, {"variant": "Full", "_starts": {}}, Ap, Ep, "Full", (None, None), 8, 2.81)
    assert got["par"] is None and len(got["cat"]["A"]) == 5 and r["pass_rate"] is None

    def boom(*a, **kw):
        raise RuntimeError("K = 5 fit (i) failed and no (o) K = 5 fit exists")
    monkeypatch.setattr(run, "selfit_fits", boom)
    r = run.errmm_boot_fit(C, {"variant": "S15N", "_starts": {}}, Ap, Ep, "S15N", (None, None), 8, 2.81)
    assert r["fit_fail"] is True and r["d"] is None


def test_errmm_reading_a_table():
    ra = selaux.errmm_reading_a
    assert ra("reproduced", "reproduced") == "robust to an f mismatch"
    assert ra("reproduced", "not reproduced") == ra("reproduced", "undetermined") == "f-mismatch sensitive"
    assert ra("not reproduced", "not reproduced") == "unchanged"
    assert ra("not reproduced", "undetermined") == "power lost under the null at g"
    assert ra("reproduced", "not evaluable (generator)") is None
    with pytest.raises(ValueError):
        ra("not reproduced", "reproduced")
    assert selaux.errmm_label([(1.0, 2.81), (1.5, 2.81)], {1.0: "reproduced", 1.5: "undetermined"}) == \
        "nulls drawn at f = 1.0: reproduced; nulls drawn at f = 1.5: undetermined"
    assert selaux.errmm_label([(1.0, 2.81)], {}, reproduction_ok=False) == "not evaluable (reproduction)"


def test_errmm_reading_b_rule():
    rb = selaux.errmm_reading_b
    v = ["reproduced"] * 80 + ["not reproduced"] * 20
    assert rb(v, [False] * 100, "reproduced", 100, 5) == (0.8, "stable under resampling")
    f = [False] * 99 + [True]
    v2 = ["reproduced"] * 79 + ["not reproduced"] * 20 + [None]
    assert rb(v2, f, "reproduced", 100, 5) == (0.79, "unstable")
    assert rb(v, [True] * 6 + [False] * 94, "reproduced", 100, 5) == (None, "not evaluable (fits)")


# ---- synthetic recorded results for the evaluation and the wiring
def _rcal(P, data_d=None, verdicts=None, power_d=0.01):
    data_d = data_d or {"S15E": [0.06, 0.27, 0.16], "S15N": [0.06, 0.24, 0.14], "Full": [0.05, 0.23, 0.14]}
    verdicts = verdicts or {"S15E": "not reproduced", "S15N": "reproduced", "Full": "reproduced"}
    th4 = [5.0, 8.0, 11.0, 13.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    df = {v: [{"bin": P["r1_bins"][b], "d": data_d[v][b], "k": 4, "valley": True, "edge": [9.3, 9.4, 9.1][b],
               "valley_t": 10.0, "fits": {str(K): th4[:3 * K - 1] for K in range(1, 5)}, "k5": [0.0] * 14}
              for b in (0, 1, 2)] for v in VARS}
    per_set = [{"f": 2.81, "variant": v, "bin": b, "kind": "power", "mech": m,
                "d": [power_d] * 50, "valley": [True] * 50} for v in VARS for b in (0, 1, 2) for m in P["mechs"]]
    variants = {v: {"verdicts": {"2.0": "not reproduced", "2.81": verdicts[v]},
                    "per_f": {"2.81": {"bins": [{"bin_name": NAMES[b], "d_star": 0.25, "resolvable": True,
                                                 "d": data_d[v][b]} for b in (0, 1, 2)]}}} for v in VARS}
    return {"status": "evaluated", "params": json.loads(json.dumps(P)), "bins": [0, 1, 2],
            "data_fits": {"2.81": df}, "variants": variants, "per_set": per_set}


def _rfit():
    return {"variants": {v: {"bins": [{"d": 1.0, "resolvable": b == 3, "almost_disjoint": False, "edge": None}
                                      for b in range(5)]} for v in VARS}}


def _results(P, sets, null_rows):
    res = {}
    for s in sets:
        rows = null_rows(s)
        res[s["k"]] = [{"gen_fail": False, "d": d, "valley": v, "k": 4, "pass_rate": 0.9, "valley_t": 10.0 if v else None,
                        "i_used_k1": False, "i_used_k2": False, "i_used_k3": True, "i_used_k4": False,
                        "i_used_k5": 0, "nonmonotone": 0, "o_nonmonotone": 0, "dropped": 0, "n_sig_lo": 1,
                        "n_sig_hi": 0, "n_mu_lo": 0, "n_mu_hi": 0, "edge": 9.0} for d, v in rows]
    return res


def _evaluate_a(null_rows, power_d=0.01, verdicts=None):
    P = dict(run.PARAMS)
    sets = selaux.errmm_sets(P["errmm_pairs"], P["errmm_bins"], P["mechs"])
    rcal = _rcal(P, verdicts=verdicts, power_d=power_d)
    res = _results(P, sets, null_rows)
    pm = {(v, b): {"valid": True} for v in VARS for b in (0, 1, 2)}
    dd = {(v, b): rcal["data_fits"]["2.81"][v][b]["d"] for v in VARS for b in (0, 1, 2)}
    return run.errmm_evaluate_a(P, sets, res, {s["k"]: [1.0] * 50 for s in sets}, rcal, _rfit(), pm, dd), sets


def test_errmm_rule_a_robust_and_sensitive():
    out, _ = _evaluate_a(lambda s: [(1.0, False)] * 50)          # no null valleys: d*_mm = 0.25
    assert out["labels"]["S15N"] == "nulls drawn at f = 1.0: reproduced; nulls drawn at f = 1.5: reproduced"
    assert out["variants"]["S15N"]["readings"] == {"1.0": "robust to an f mismatch", "1.5": "robust to an f mismatch"}
    assert out["variants"]["S15E"]["readings"]["1.0"] == "unchanged"       # recorded verdict not reproduced
    # g = 1.0, bin 1: three null valleys at d = 0.20 in one set -> d*_mm = 0.20 <= data d 0.24
    rows = lambda s: ([(0.20, True)] * 3 + [(1.0, False)] * 47
                      if (s["g"], s["bin"], s["kind"], s["mech"]) == (1.0, 1, "null_sp", "rA") else [(1.0, False)] * 50)
    out, sets = _evaluate_a(rows)
    pp = out["variants"]["Full"]["per_pair"]["1.0"]
    assert pp["verdict"] == "not reproduced" and pp["reading"] == "f-mismatch sensitive"
    assert pp["bins_d_star_mm_le_data_d"] == [NAMES[1]] and pp["bins"][1]["d_star_mm"] == 0.20
    assert out["variants"]["Full"]["per_pair"]["1.5"]["reading"] == "robust to an f mismatch"
    row = next(r for r in out["per_set"] if (r["g"], r["variant"], r["bin"], r["kind"], r["mech"]) ==
               (1.0, "Full", 1, "null_sp", "rA"))
    assert row["q_s"] == 0.20 and row["frac_valley_d_lt_data"] == pytest.approx(3 / 50)
    assert row["frac_valley_d_lt_cap"] == pytest.approx(3 / 50) and row["frac_n_sig_lo"] == 1.0


def test_errmm_rule_a_power_loss_gives_undetermined():
    # d*_mm = 0.005 in bins 0 and 1: power (power mocks d = 0.01) is lost there -> 2 resolvable bins
    rows = lambda s: ([(0.005, True)] * 3 + [(1.0, False)] * 47
                      if s["g"] == 1.0 and s["bin"] in (0, 1) and s["kind"] == "null_sn" and s["mech"] == "rtau"
                      else [(1.0, False)] * 50)
    out, _ = _evaluate_a(rows)
    e = out["variants"]["S15E"]["per_pair"]["1.0"]
    assert e["verdict"] == "undetermined" and e["reading"] == "power lost under the null at g"
    assert e["bins_unresolvable"] == NAMES[:2]
    assert out["variants"]["S15N"]["per_pair"]["1.0"]["reading"] == "f-mismatch sensitive"


def test_errmm_failure_rules():
    P = dict(run.PARAMS)
    sets = selaux.errmm_sets(P["errmm_pairs"], P["errmm_bins"], P["mechs"])
    rcal = _rcal(P)
    res = _results(P, sets, lambda s: [(1.0, False)] * 50)
    k_fail = next(s["k"] for s in sets if (s["g"], s["variant"]) == (1.5, "S15N"))
    res[k_fail] = res[k_fail][:4] + [{"gen_fail": True, "d": None, "valley": None, "k": None, "pass_rate": None}]
    k_nan = next(s["k"] for s in sets if (s["g"], s["variant"]) == (1.0, "Full"))
    res[k_nan][7]["d"] = float("nan")
    pm = {(v, b): {"valid": True} for v in VARS for b in (0, 1, 2)}
    dd = {(v, b): 0.1 for v in VARS for b in (0, 1, 2)}
    out = run.errmm_evaluate_a(P, sets, res, {}, rcal, _rfit(), pm, dd)
    assert out["variants"]["S15N"]["verdicts"]["1.5"] == "not evaluable (generator)"
    assert out["variants"]["S15N"]["readings"]["1.5"] is None
    assert out["variants"]["Full"]["verdicts"]["1.0"] == "not evaluable (non-finite)"
    assert out["variants"]["Full"]["verdicts"]["1.5"] == "reproduced"
    res2 = _results(P, sets, lambda s: [(1.0, False)] * 50)
    res2[3] = res2[3][:10]
    with pytest.raises(RuntimeError):
        run.errmm_evaluate_a(P, sets, res2, {}, rcal, _rfit(), pm, dd)


def test_errmm_evaluate_b():
    P = dict(run.PARAMS, errmm_n_boot=10, errmm_boot_max_fail=1)
    rcal = _rcal(P)
    boot = {}
    for v in VARS:
        for b in (0, 1, 2):
            for j in range(11):
                d = rcal["data_fits"]["2.81"][v][b]["d"]
                if b == 1:
                    d = 0.30 if j < 3 else 0.24              # replicates 0-2 lose bin 1; the others pass it
                boot[(v, b, j)] = {"d": d, "valley": True, "k": 4, "pass_rate": 0.9, "edge": [9.3, 9.4, 9.1][b],
                                   "valley_t": 10.0, "fit_fail": False, "i_used_k3": True, "n_sig_lo": 1}
    boot[("Full", 2, 5)] = {"fit_fail": True, "d": None, "valley": None, "k": None, "pass_rate": None}
    out = run.errmm_evaluate_b(P, boot, rcal, _rfit())
    n = out["S15N"]
    assert n["replicate_verdicts"][:3] == ["not reproduced"] * 3 and n["frac_equal"] == pytest.approx(0.7)
    assert n["reading"] == "unstable" and n["unresampled_verdict"] == "reproduced" and not n["unresampled_differs"]
    assert out["Full"]["n_failed"] == 1 and out["Full"]["frac_equal"] == pytest.approx(0.6)
    assert out["S15E"]["errcal_verdict"] == "not reproduced" and out["S15E"]["frac_equal"] == pytest.approx(0.3)
    assert out["S15E"]["unresampled_differs"] and out["S15E"]["frac_equal_unresampled"] == pytest.approx(0.7)
    b1 = n["bins"][1]
    assert b1["n_used"] == 10 and b1["d_pct_16_50_84"][1] == pytest.approx(0.24) and b1["frac_n_sig_lo"] == 1.0
    boot[("Full", 1, 6)] = dict(boot[("Full", 2, 5)])
    assert run.errmm_evaluate_b(P, boot, rcal, _rfit())["Full"]["reading"] == "not evaluable (fits)"


def test_errmm_params_check():
    P = dict(run.PARAMS)
    rec = json.loads(json.dumps(dict(P, parts=["errcal"])))
    rec = {k: v for k, v in rec.items() if not k.startswith("errmm_")}
    assert run.errmm_params_ok(P, rec)
    assert not run.errmm_params_ok(P, dict(rec, kmax=5))


def test_main_errmm_wiring(tmp_path, monkeypatch):
    """main_errmm end to end on synthetic inputs (fits stubbed): a failed input check gives "not evaluable
    (reproduction)"; an exploration (2 mocks, 3 replicates) runs every set and replicate through the checkpoints
    with the README 2.9 streams and gives no label; a rerun replays the checkpoints."""
    import pandas as pd
    rng = np.random.default_rng(3)
    n = 3000
    age = rng.uniform(1.0, 14.0, n)
    rel = rng.uniform(0.03, 0.2, n)
    df = pd.DataFrame({"id": np.arange(n), "age": age, "eage": age * rel, "feh": rng.uniform(-0.69, -0.11, n),
                       "efeh": 0.05, "afe": 0.1, "eafe": 0.02, "jphi": 1800.0, "mk": 2.0})
    P = dict(run.PARAMS, n_rows=n, errmm_n_mock=2, errmm_n_boot=3, parts=["errmm"])
    monkeypatch.setattr(run, "load", lambda ctx, P_: df)
    pm = {"mu_old": 11.0, "s_old": 0.82, "w_old": 0.4, "young": [1.5, 7.0], "valid": True}
    feh = df["feh"].to_numpy()
    nbin = {b: int(((feh >= P["r1_bins"][b][0]) & (feh < P["r1_bins"][b][1])).sum()) for b in range(5)}
    rec = {"data_fits": {f"{v}_{b}": {"n": nbin[b], "skewnorm": [9.0, 0.5, 0.0], "splitnorm": [9.0, 0.5, 0.5],
                                      "power_models": {"primary": pm}} for v in VARS for b in range(5)}}
    rerr = {"companion_refits": {v: {"1.5": [{"bin": P["r1_bins"][b], "d": 0.3, "k": 4} for b in (0, 1, 2)]}
                                 for v in VARS}}
    rcal = _rcal(P)
    rcal["params"] = json.loads(json.dumps(dict(P, parts=["errcal"])))

    def fake_refit(C, df_, F, b, v, coef, f, nulls=False):
        assert nulls and f == 1.5
        return {"f": f, "variant": v, "bin": P["r1_bins"][b], "n": nbin[b], "d": 0.3, "k": 4, "valley": True,
                "skewnorm": [9.5, 0.6, 0.1], "splitnorm": [9.5, 0.6, 0.4], "_starts": {}, "_p": None}
    monkeypatch.setattr(run, "r1_data_refit", fake_refit)
    seen, seen_b = [], []

    def fake_mock(C, D, kind, mech, rngs, pools, nstart, g, F):
        seen.append((D["variant"], kind, mech, g, F, D["skewnorm"][0], float(rngs[0].random()), float(rngs[1].random())))
        return {"gen_fail": False, "d": 1.0, "valley": False, "k": 4, "pass_rate": 0.9, "valley_t": None}
    monkeypatch.setattr(run, "errmm_mock", fake_mock)

    def fake_boot(C, D, Ap, Ep, v, rngs, nstart, f):
        seen_b.append((v, len(Ap), float(Ap.sum()), f, float(rngs[0].random())))
        return {"fit_fail": False, "d": 0.1, "valley": True, "k": 4, "pass_rate": 0.9 if v != "Full" else None,
                "edge": 9.0, "valley_t": 10.0, "n": len(Ap)}
    monkeypatch.setattr(run, "errmm_boot_fit", fake_boot)
    saved = {}
    ctx = types.SimpleNamespace(save=lambda name, obj: saved.__setitem__(name, json.loads(json.dumps(obj, default=float))),
                                log=lambda m: None, record_suffix=None)
    R = {"r1_sel": rec, "r1_selfit": _rfit(), "r1_err": rerr, "r1_errcal": rcal}
    bad = json.loads(json.dumps(rerr))
    bad["companion_refits"]["S15N"]["1.5"][2]["d"] += 1e-6
    out = run.main_errmm(ctx, P, store_root=tmp_path, recorded=dict(R, r1_err=bad))
    assert ctx.record_suffix == "_errmm"
    r = saved["r1_errmm"]
    assert r["label"] == "not evaluable (reproduction)" and r["checks"]["input_and_fit_mismatches"] == ["S15N_2@f=1.5.d"]
    assert out["R1-ERRMM"] == "not evaluable (reproduction)" and not seen
    out = run.main_errmm(ctx, P, store_root=tmp_path, recorded=dict(R, r1_errcal=dict(rcal, status="stopped")))
    assert saved["r1_errmm"]["checks"]["input_and_fit_mismatches"] == ["r1_errcal.status='stopped'"]
    saved.clear()
    out = run.main_errmm(ctx, P, store_root=tmp_path, recorded=R)
    r = saved["r1_errmm"]
    assert r["status"] == "exploration (no label)" and r["label"].startswith("no label (exploration with 2")
    assert len(seen) == 144 and len(r["per_set"]) == 72 and r["seed_tags"] == [64, 164, 65, 165]
    sets = selaux.errmm_sets(P["errmm_pairs"], P["errmm_bins"], P["mechs"])
    s9 = sets[9]
    want = (np.random.default_rng([0, 64, 9, 0]).random(), np.random.default_rng([0, 164, 9, 0]).random())
    assert (s9["variant"], s9["kind"], s9["mech"], s9["g"], s9["F"]) == seen[9][:5] and seen[9][6:] == want
    assert {x[5] for x in seen if x[3] == 1.0} == {9.0} and {x[5] for x in seen if x[3] == 1.5} == {9.5}
    # part B: 3 bins x (3 + 1) replicates x 3 variants; replicate 3 (unresampled) first, the full parent
    assert len(seen_b) == 36 and all(x[3] == 2.81 for x in seen_b)
    assert seen_b[0][1] == nbin[0] and seen_b[0][2] == pytest.approx(float(age[(feh >= -0.7) & (feh < -0.5)].sum()))
    assert seen_b[0][4] == np.random.default_rng([0, 65, 0, 3, 1]).random()
    # the three variants of one replicate share the resample
    assert seen_b[3][2] == seen_b[4][2] == seen_b[5][2] and seen_b[3][2] != seen_b[0][2]
    assert r["bootstrap"]["S15N"]["reading"].startswith("no reading (exploration with 3")
    assert len(json.dumps(r)) < 1024 ** 2
    n_before = (len(seen), len(seen_b))
    run.main_errmm(ctx, P, store_root=tmp_path, recorded=R)               # replayed from the checkpoints
    assert (len(seen), len(seen_b)) == n_before
