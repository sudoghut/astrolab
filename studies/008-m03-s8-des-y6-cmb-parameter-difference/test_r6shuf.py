"""Offline tests of R6-SHUF (README 2.8): the column-variant draw, the kNN estimator, the label rules,
the reuse of r6.json and r6_nomnu.json, the job plan and the conclusion test. No TensorFlow, no network,
no flow training."""
import ast
import copy
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).parent


def _import(name, path=None):
    spec = importlib.util.spec_from_file_location(f"study008_{name}", path or HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


rs = _import("r6shuf")
fs = _import("flowshift")

GATE6 = {"mu1": 2.0, "mu2": 1.0, "curv": 0.3,
         "boxes": [[-0.6, 1.4, 0.05], [-0.6, 1.4, 0.05], [-0.6, 1.4, 0.05], [-0.1, 1.9, 0.1]],
         "n_exact": 2_000_000, "exact_seed": 999, "seeds": [10, 11, 12], "sample_seed_offset": 1000,
         "tol_mean": 0.10, "tol_each": 0.20}
GATE_P = {"mu1": 1.1, "mu2": 0.55, "exact": 0.8601}
SHORT = ["a_s_1e9", "h0", "mnu", "n_s", "omega_b", "omega_m"]
SEEDS = [0, 1, 2, 3, 4]
BAND, SMAX, EMIN = [0.40, 0.60], 0.30, 0.20
N6 = {0: 1.857, 1: 1.643, 2: 1.719, 3: 1.605, 4: 1.669}
N5 = {0: 0.478, 1: 0.52, 2: 0.55, 3: 0.53, 4: 0.54}


def test_no_tensorflow_on_import():
    assert "tensorflow" not in sys.modules


# ------------------------------------------------------------------ variant draw ----
def _chains(rng, na=500, nb=700):
    xa = rng.normal(size=(na, 6)) + np.arange(6)
    xb = rng.normal(size=(nb, 6)) - np.arange(6)
    xa[:, 2] = rng.uniform(0.06, 0.6, na)
    xb[:, 2] = rng.uniform(0.06, 0.2, nb)
    return xa, rng.uniform(0.1, 1.0, na), xb, rng.uniform(0.1, 1.0, nb)


@pytest.mark.parametrize("seed", [0, 3, 17])
def test_variant_none_is_resampled_difference_bitwise(seed):
    xa, wa, xb, wb = _chains(np.random.default_rng(1))
    a0, b0 = xa.copy(), xb.copy()
    ref = fs.resampled_difference(xa, wa, xb, wb, 4000, seed)
    new = fs.variant_difference(xa, wa, xb, wb, 4000, seed, "none", 2)
    assert new.tobytes() == ref.tobytes() and new.dtype == ref.dtype and new.shape == ref.shape
    for v in ("S", "P", "SS"):
        fs.variant_difference(xa, wa, xb, wb, 4000, seed, v, 2)
    assert np.array_equal(xa, a0) and np.array_equal(xb, b0)          # inputs untouched


def _draws(seed, n=3000):
    """The resampled DES rows (CMB set to zero) and CMB rows (DES set to zero) for one seed."""
    xa, wa, xb, wb = _chains(np.random.default_rng(2))
    za, zb = np.zeros_like(xa), np.zeros_like(xb)
    des = {v: fs.variant_difference(xa, wa, zb, wb, n, seed, v, 2) for v in fs.VARIANTS}
    cmb = {v: -fs.variant_difference(za, wa, xb, wb, n, seed, v, 2) for v in fs.VARIANTS}
    return des, cmb


def test_variant_columns():
    k, n = 2, 3000
    des, cmb = _draws(k, n)
    others = [0, 1, 3, 4, 5]
    # (S): the DES mnu multiset is kept, the pairing is the stated permutation; other columns unchanged
    perm = np.random.default_rng(1000 + k).permutation(n)
    assert np.array_equal(np.sort(des["S"][:, 2]), np.sort(des["none"][:, 2]))
    assert np.array_equal(des["S"][:, 2], des["none"][perm, 2])
    assert not np.array_equal(des["S"][:, 2], des["none"][:, 2])
    assert np.array_equal(des["S"][:, others], des["none"][:, others])
    assert np.array_equal(cmb["S"], cmb["none"])                         # CMB untouched in (S)
    # (P): the DES mnu column is the stated uniform draw on the prior
    assert np.array_equal(des["P"][:, 2], np.random.default_rng(2000 + k).uniform(0.06, 0.6, n))
    assert np.array_equal(des["P"][:, others], des["none"][:, others])
    assert np.array_equal(cmb["P"][:, others], cmb["none"][:, others])   # (DES is zero here: column 2 is P - CMB)
    xa, wa, xb, wb = _chains(np.random.default_rng(2))
    full = fs.variant_difference(xa, wa, xb, wb, n, k, "P", 2)
    assert np.array_equal(full[:, 2], des["P"][:, 2] - cmb["none"][:, 2])   # CMB mnu unchanged in (P)
    # (SS): (S) on DES plus the CMB mnu column permuted with default_rng(3000 + k)
    pc = np.random.default_rng(3000 + k).permutation(n)
    assert np.array_equal(des["SS"], des["S"])
    assert np.array_equal(cmb["SS"][:, 2], cmb["none"][pc, 2])
    assert np.array_equal(np.sort(cmb["SS"][:, 2]), np.sort(cmb["none"][:, 2]))
    assert np.array_equal(cmb["SS"][:, others], cmb["none"][:, others])
    with pytest.raises(ValueError):
        fs.variant_difference(*_chains(np.random.default_rng(2)), 10, 0, "X", 2)


def test_knn_matches_design_script():
    sys.path.insert(0, str(HERE))
    try:
        ex = _import("t044_knn", HERE / "explore" / "t044_knn_gate_design.py")
    finally:
        sys.path.remove(str(HERE))
    x = fs.synthetic(3000, np.random.default_rng(1010), {**GATE6, "mu1": 1.1, "mu2": 0.55})
    multi = fs.knn_nsigma_multi(x, [20, 100])
    assert multi == [ex.knn_nsigma(x, 20), ex.knn_nsigma(x, 100)]
    assert fs.knn_nsigma(x, 20) == multi[0]


def test_run_job_shuf_and_knn(tmp_path, monkeypatch):
    """The TF-side job wiring: DES/CMB and the mnu column from the exported names (one_shift faked)."""
    xa, wa, xb, wb = _chains(np.random.default_rng(3), 400, 300)
    arrays = {f"des_{c}": xa[:, i] for i, c in enumerate(SHORT)}
    arrays.update({f"cmb_{c}": xb[:, i] for i, c in enumerate(SHORT)}, des_w=wa, cmb_w=wb,
                  des_s8=xa[:, 0], cmb_s8=xb[:, 0])
    inp = tmp_path / "input.npz"
    np.savez(inp, **arrays)
    cfg = rs.config(SHORT, SEEDS, 2000, {"tol": 0.02}, GATE6, GATE_P, [1000, 2000, 3000], [0.06, 0.6], [20, 100])
    seen = {}

    def fake(diff, names, seed, est, pop_size=None, record_pop=False):
        seen.update(diff=diff, names=names, pop_size=pop_size, record_pop=record_pop)
        return {"seed": seed, "n_sigma": 1.0, "converged": True, "lower_bound": False}

    monkeypatch.setattr(fs, "one_shift", fake)
    out = fs.run_job(["shuf", "P", "4"], str(inp), cfg)
    assert out["variant"] == "P" and out["seed"] == 4
    assert np.array_equal(seen["diff"], fs.variant_difference(xa, wa, xb, wb, 2000, 4, "P", 2))
    assert seen["names"] == SHORT and seen["pop_size"] is None
    out = fs.run_job(["shuf", "none", "0"], str(inp), cfg)
    assert seen["diff"].tobytes() == fs.resampled_difference(xa, wa, xb, wb, 2000, 0).tobytes()
    k = fs.run_job(["knn", "1"], str(inp), cfg)
    assert set(k["n_sigma"]) == {"none", "S", "P", "SS", "5d"} and k["k"] == [20, 100]
    five = np.delete(fs.variant_difference(xa, wa, xb, wb, 2000, 1, "none", 2), 2, axis=1)
    assert k["n_sigma"]["5d"] == fs.knn_nsigma_multi(five, [20, 100])
    assert k["n_sigma"]["S"] == fs.knn_nsigma_multi(fs.variant_difference(xa, wa, xb, wb, 2000, 1, "S", 2), [20, 100])


# ------------------------------------------------------------------ gate and mapping ----
def test_low_gate_exact_value():
    """README 2.8: the low-shift gate's exact n_sigma (2,000,000 draws, default_rng(999)) is 0.8601."""
    g = rs.low_gate(GATE6, GATE_P)
    assert {k: v for k, v in g.items() if k not in ("mu1", "mu2")} == \
        {k: v for k, v in GATE6.items() if k not in ("mu1", "mu2")}
    assert round(fs.synthetic_exact(g)["n_sigma"], 4) == 0.8601


def test_chi2_mapping_matches_section_2_7():
    assert rs.chi2_equiv(1.699, 6) == pytest.approx(10.97, abs=0.01)
    assert rs.chi2_equiv(1.00, 5) == pytest.approx(5.89, abs=0.01)
    assert rs.chi2_equiv(1.737, 1) == pytest.approx(1.737 ** 2, rel=1e-6)


# ------------------------------------------------------------------ rules ----
def _reps(vals, lower=(), conv=True, seeds=SEEDS):
    return [{"seed": k, "n_sigma": v, "lower_bound": k in lower, "converged": conv} for k, v in zip(seeds, vals)]


def _ns_for_phi(phis):
    """n_S,k that give the stated phi_k with N6, N5."""
    return [N6[k] - p * (N6[k] - N5[k]) for k, p in zip(SEEDS, phis)]


def _label(reps_s, reps_p=None, gate_r1=True, rec=True, env=True, gate=True, n6=N6, n5=N5):
    reps_p = reps_p if reps_p is not None else _reps([0.7] * 5)
    return rs.label(gate_r1, rec, env, gate, reps_s, reps_p, n6, n5, SEEDS, EMIN, SMAX, BAND)


def test_label_rule_order():
    good = _reps(_ns_for_phi([0.70, 0.72, 0.68, 0.71, 0.69]))
    assert _label(good)[0] == rs.CORR
    assert _label(good, gate_r1=False)[0] == rs.NE                                  # rule 1
    assert _label(good, rec=False)[0] == rs.NE
    assert _label(good, env=False)[0] == rs.NE
    assert _label(good, gate=False)[0] == rs.NE_GATE                               # rule 2
    assert _label(good, gate_r1=False, gate=False)[0] == rs.NE                     # 1 before 2
    for bad in (good[:4] + [{"seed": 4, "error": "x"}], good[:4],
                _reps([1.0, None, 1.0, 1.0, 1.0]), _reps([1.0, float("nan"), 1.0, 1.0, 1.0]),
                _reps([1.0] * 5, conv=False), _reps([1.0] * 5, lower={2}),
                _reps([1.0] * 5, seeds=[0, 1, 2, 3, 5])):
        assert _label(bad)[0] == rs.NE                                             # rule 3 (S)
        assert _label(good, bad)[0] == rs.NE                                       # rule 3 (P)
    assert _label(_reps([1.0] * 5, lower={2}), gate=False)[0] == rs.NE_GATE        # 2 before 3
    n5_small = {**N5, 3: N6[3] - 0.20}                                             # rule 4: E = 0.20
    lab, why, nums = _label(good, n5=n5_small)
    assert lab == rs.NE and "E_k" in why
    n5_ok = {**N5, 3: N6[3] - 0.2001}
    ok = _reps([N6[k] - 0.7 * (N6[k] - n5_ok[k]) for k in SEEDS])          # phi = 0.7 with this n5
    assert rs.label(True, True, True, True, ok, _reps([0.7] * 5), N6, n5_ok, SEEDS, EMIN, SMAX, BAND)[0] == rs.CORR
    lab, why, nums = _label(_reps(_ns_for_phi([0.1, 0.9, 0.5, 1.2, -0.2])))      # rule 5
    assert lab == rs.NE and nums["s_phi"] > SMAX


def test_label_bands_and_edges():
    assert _label(_reps(_ns_for_phi([0.2, 0.22, 0.18, 0.21, 0.19])))[0] == rs.NOT_CORR
    assert _label(_reps(_ns_for_phi([0.5, 0.52, 0.48, 0.51, 0.49])))[0] == rs.BETWEEN
    assert _label(_reps(_ns_for_phi([0.62, 0.66, 0.56, 0.64, 0.58])))[0] == rs.BETWEEN  # lower end < 0.60
    # closed band edges, with exactly representable phi (E_k = 1, n6 = 2, n5 = 1) and zero spread
    n6e, n5e = {k: 2.0 for k in SEEDS}, {k: 1.0 for k in SEEDS}
    p1 = _reps([1.0] * 5)

    def lab(ns, band):
        return rs.label(True, True, True, True, _reps(ns), p1, n6e, n5e, SEEDS, EMIN, SMAX, band)[0]
    assert lab([1.5] * 5, BAND) == rs.BETWEEN                                   # phi = 0.5
    assert lab([1.375] * 5, [0.375, 0.625]) == rs.CORR                          # phi = 0.625 = upper edge
    assert lab([1.625] * 5, [0.375, 0.625]) == rs.NOT_CORR                      # phi = 0.375 = lower edge
    assert lab([1.375] * 5, [0.375, 0.6250001]) == rs.BETWEEN                   # just inside the band
    # rule 5 is s_phi > s_max: s_phi equal to s_max does not decide
    ns = [1.0, 2.0, 1.5, 1.5, 1.5]
    s_phi = float(np.std([2.0 - v for v in ns], ddof=1))
    assert rs.label(True, True, True, True, _reps(ns), p1, n6e, n5e, SEEDS, EMIN, s_phi, BAND)[0] == rs.BETWEEN
    assert rs.label(True, True, True, True, _reps(ns), p1, n6e, n5e, SEEDS, EMIN, s_phi * 0.999, BAND)[0] == rs.NE


def test_interval_definition():
    phis = [0.71, 0.55, 0.83, 0.64, 0.77]
    _, _, nums = _label(_reps(_ns_for_phi(phis)))
    s = float(np.std(phis, ddof=1))
    assert nums["phi_bar"] == pytest.approx(np.mean(phis)) and nums["s_phi"] == pytest.approx(s)
    assert nums["half_width"] == pytest.approx(2 * s / math.sqrt(5))


def test_quantities_sum_to_one_and_chi2_scale():
    ns = dict(zip(SEEDS, _ns_for_phi([0.7, 0.6, 0.8, 1.2, -0.1])))
    np_ = {k: v - 0.15 for k, v in ns.items()}
    q = rs.quantities(N6, N5, ns, np_)
    for k in SEEDS:
        row = q["per_seed"][str(k)]
        assert row["phi"] + row["psi"] + row["rho"] == pytest.approx(1.0, abs=1e-12)
        assert row["E"] == pytest.approx(N6[k] - N5[k])
        c = row["chi2"]
        assert c["n6"] == pytest.approx(rs.chi2_equiv(N6[k], 6)) and c["n5"] == pytest.approx(rs.chi2_equiv(N5[k], 5))
        assert row["phi_chi2"] == pytest.approx((c["n6"] - c["S"]) / (c["n6"] - c["n5"]))
    assert q["phi"]["mean"] == pytest.approx(np.mean([0.7, 0.6, 0.8, 1.2, -0.1]))
    assert q["phi"]["s"] == pytest.approx(np.std([0.7, 0.6, 0.8, 1.2, -0.1], ddof=1))


def test_determinism_flag():
    rec = {"per_seed": {0: 1.8568675521248896}}
    assert rs.determinism({"n_sigma": 1.8568675521248896}, rec)["flag"] is None
    assert rs.determinism({"n_sigma": 1.87}, rec)["flag"] is None
    assert rs.determinism({"n_sigma": 1.88}, rec)["flag"] == rs.FLAG_DET
    assert rs.determinism({"n_sigma": 1.83}, rec)["flag"] == rs.FLAG_DET
    assert rs.determinism({"seed": 0, "error": "x"}, rec)["flag"] is None


# ------------------------------------------------------------------ reuse of the records ----
def _copy(tmp_path, name, mutate=None):
    src = HERE / "results" / name
    if not src.exists():
        pytest.skip(f"results/{name} not present")
    d = json.loads(src.read_text(encoding="utf-8"))
    if mutate:
        mutate(d)
    tmp_path.mkdir(parents=True, exist_ok=True)
    p = tmp_path / name
    p.write_text(json.dumps(d), encoding="utf-8")
    return p


def _set(path, value):
    def f(d):
        o = d
        for k in path[:-1]:
            o = o[k]
        o[path[-1]] = value
    return f


def test_check_records_recorded_and_tampered(tmp_path):
    ok6 = rs.check_r6(_copy(tmp_path, "r6.json"))
    ok5 = rs.check_nomnu(_copy(tmp_path, "r6_nomnu.json"))
    assert ok6["ok"] and sorted(ok6["per_seed"]) == SEEDS and ok6["parameters"] == SHORT
    assert ok5["ok"] and sorted(ok5["per_seed"]) == SEEDS and ok5["parameters"] == SHORT
    assert ok6["versions"] == ok5["versions"] and ok6["settings"] == ok5["settings"]
    assert not rs.check_r6(tmp_path / "missing" / "r6.json")["ok"]
    assert not rs.check_nomnu(tmp_path / "missing" / "r6_nomnu.json")["ok"]
    t6 = [_set(["flows", "complete"], False), _set(["flows", "gate", "passed"], False),
          _set(["flows", "main", "n_bar"], 1.6987), _set(["flows", "main", "s"], 0.0979),
          lambda d: d["flows"]["main"]["repetitions"].pop(),
          lambda d: d["flows"]["main"]["repetitions"][2].update(n_sigma=None),
          lambda d: d["flows"]["main"]["repetitions"][2].update(converged=False),
          lambda d: d["flows"]["main"]["repetitions"][2].update(lower_bound=True),
          lambda d: d["flows"]["main"]["repetitions"][0].update(seed=7),
          lambda d: d["flows"].pop("main")]
    for i, m in enumerate(t6):
        assert not rs.check_r6(_copy(tmp_path / f"r6_{i}", "r6.json", m))["ok"], i
    t5 = [_set(["flows", "complete"], False), _set(["flows", "gate5", "passed"], False),
          _set(["flows", "nomnu", "n_bar"], 0.5238), _set(["flows", "nomnu", "s"], 0.0404),
          lambda d: d["flows"]["nomnu"]["repetitions"].pop(),
          lambda d: d["flows"]["nomnu"]["repetitions"][1].update(n_sigma=float("inf")),
          lambda d: d["flows"]["nomnu"]["repetitions"][1].update(converged=False),
          lambda d: d["flows"]["nomnu"]["repetitions"][1].update(lower_bound=True),
          lambda d: d["flows"]["nomnu"]["repetitions"][1].update(error="x"),
          lambda d: d["flows"].pop("nomnu")]
    for i, m in enumerate(t5):
        assert not rs.check_nomnu(_copy(tmp_path / f"r5_{i}", "r6_nomnu.json", m))["ok"], i
    bad = tmp_path / "bad"
    bad.mkdir()
    (bad / "r6_nomnu.json").write_text("{not json", encoding="utf-8")
    assert not rs.check_nomnu(bad / "r6_nomnu.json")["ok"]


def test_env_matches():
    env = {"versions": {"tensorflow": "2.21.0"}, "settings": {"pop_size": 10}}
    assert rs.env_matches(env, env, env)["ok"]
    assert not rs.env_matches({**env, "versions": {"tensorflow": "2.22.0"}}, env, env)["ok"]
    assert not rs.env_matches(env, env, {**env, "settings": {"pop_size": 1}})["ok"]
    assert not rs.env_matches({}, {}, {})["ok"]


# ------------------------------------------------------------------ run.py ----
def test_run_params_and_reuse_paths():
    src = (HERE / "run.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    guard = [n for n in ast.walk(tree) if isinstance(n, ast.If)
             and ast.unparse(n.test) == "P['r6_nomnu_retrain'] and P['r6_nomnu']"]
    assert len(guard) == 1
    inside = {id(n) for stmt in guard[0].body for n in ast.walk(stmt)}
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)]
    sensitive = [c for c in calls if (ast.unparse(c.func) == "r6flow.run_jobs" and "r6nomnu.plan" in ast.unparse(c))
                 or (ast.unparse(c.func) == "ctx.save" and c.args and ast.unparse(c.args[0]) == "'r6_nomnu'")]
    assert len(sensitive) == 2 and all(id(c) in inside for c in sensitive)
    assert 'ctx.study.results_dir / "r6_nomnu.json"' in src
    sys.path.insert(0, str(HERE))
    try:
        run = _import("run")
    finally:
        sys.path.remove(str(HERE))
    P = run.PARAMS
    assert P["r6_shuf"] is True and P["r6_nomnu_retrain"] is False and P["r6_retrain"] is False
    assert P["r6_shuf_seeds"] == SEEDS and P["r6_shuf_s_max"] == 0.30 and P["r6_shuf_e_min"] == 0.20
    assert P["r6_shuf_band"] == [0.40, 0.60] and P["r6_shuf_gate"] == GATE_P
    assert P["r6_shuf_seed_offsets"] == [1000, 2000, 3000] and P["r6_shuf_prior"] == [0.06, 0.6]
    assert P["r6_shuf_knn_k"] == [20, 100]
    assert P["r6_gate"] == GATE6


# ------------------------------------------------------------------ plan and assembly ----
def _fake_job(calls, gate_val, vals=None, env=None, crash=()):
    vals = vals or {}

    def job(*parts):
        calls.append(parts)
        if parts in crash:
            raise RuntimeError("job failed (code 1)")
        if parts[0] == "meta":
            return copy.deepcopy(env) if env else {"versions": {"tensorflow": "2.21.0"}, "settings": {"pop_size": 10}}
        if parts[0] == "exact":
            return {"delta": 0.61, "n_sigma": 0.8601}
        if parts[0] == "knn":
            return {"seed": parts[1], "k": [20, 100], "n_sigma": {v: [0.5, 0.6] for v in ("none", "S", "P", "SS", "5d")}}
        k = parts[-1]
        rec = {"seed": k, "lower_bound": False, "converged": True, "delta": 0.5}
        if parts[0] == "gate":
            return {**rec, "n_sigma": gate_val}
        return {**rec, "n_sigma": vals.get(parts[1], {}).get(k, 1.0), "variant": parts[1],
                "pop_size": None, "pop_size_passed": False}
    return job


def _cfg():
    return rs.config(SHORT, SEEDS, 10, {"tol": 0.02}, GATE6, GATE_P, [1000, 2000, 3000], [0.06, 0.6], [20, 100])


@pytest.mark.parametrize("gate_val", [0.86, 1.2])
def test_plan_order(gate_val):
    calls = []
    res = rs.plan(_fake_job(calls, gate_val), _cfg(), lambda m: None, fs)
    expected = [("meta",), ("exact", "low")] + [("gate", "low", k) for k in (10, 11, 12)]
    for v in ("S", "P", "SS"):                     # also run when the low-shift gate fails (rule 2)
        expected += [("shuf", v, k) for k in SEEDS]
    expected += [("shuf", "none", 0)] + [("knn", k) for k in SEEDS]
    assert calls == expected
    assert res["gate_low"]["passed"] is (gate_val == 0.86)
    assert all("pop_size" not in g for g in _cfg()["gates"].values())


def test_plan_env_mismatch_trains_nothing():
    calls = []
    rec = {"versions": {"tensorflow": "2.21.0"}, "settings": {"pop_size": 10}}
    other = {"versions": {"tensorflow": "2.22.0"}, "settings": {"pop_size": 10}}
    res = rs.plan(_fake_job(calls, 0.86, env=other), _cfg(), lambda m: None, fs, expected=(rec, rec))
    assert calls == [("meta",)] and "gate_low" not in res
    out = rs.assemble(fs.finite(res), {"ok": True, "per_seed": N6, **rec}, {"ok": True, "per_seed": N5, **rec},
                      True, SEEDS, EMIN, SMAX, BAND, GATE_P, {})
    assert out["label"] == rs.NE and "differ" in out["reason"]


def test_descriptive_crashes():
    calls = []
    res = rs.plan(_fake_job(calls, 0.86, crash={("shuf", "SS", 2), ("shuf", "none", 0), ("knn", 1)}),
                  _cfg(), lambda m: None, fs)
    assert res["SS"]["repetitions"][2] == {"seed": 2, "error": "subprocess failed"}
    assert res["determinism"]["error"] == "subprocess failed" and res["knn"][1]["error"] == "subprocess failed"


def test_s_p_crash_recorded_and_plan_continues():
    calls = []
    res = rs.plan(_fake_job(calls, 0.86, crash={("shuf", "P", 3)}), _cfg(), lambda m: None, fs)
    assert res["P"]["repetitions"][3] == {"seed": 3, "error": "subprocess failed"}
    assert ("shuf", "SS", 4) in calls and ("shuf", "none", 0) in calls and ("knn", 4) in calls
    rec = {"versions": {"tensorflow": "2.21.0"}, "settings": {"pop_size": 10}}
    out = rs.assemble(fs.finite(res), {"ok": True, "per_seed": N6, **rec}, {"ok": True, "per_seed": N5, **rec},
                      True, SEEDS, EMIN, SMAX, BAND, GATE_P, {})
    assert out["label"] == rs.NE and "(P)" in out["reason"]


def test_env_requires_settings_present():
    rec = {"versions": {"tensorflow": "2.21.0"}, "settings": None}
    res = {"versions": {"tensorflow": "2.21.0"}, "settings": None}
    assert rs.env_matches(res, rec, rec)["ok"] is False
    full = {"versions": {"tensorflow": "2.21.0"}, "settings": {"pop_size": 10}}
    assert rs.env_matches(dict(full), full, full)["ok"] is True


def test_assemble_not_reusable():
    out = rs.assemble({}, {"ok": False, "reason": "results/r6.json missing"}, {"ok": True}, True, SEEDS, EMIN,
                      SMAX, BAND, GATE_P, {})
    assert out["label"] == rs.NE and out["reason"] == "results/r6.json missing"
    assert out["summary"]["records_ok"] == {"r6": False, "r6_nomnu": True}


@pytest.mark.parametrize("phis, gate_val, det", [
    ([0.70, 0.72, 0.68, 0.71, 0.69], 0.86, 1.8569),     # mainly through DES-side correlations
    ([0.20, 0.25, 0.15, 0.22, 0.18], 0.86, 1.90),       # mainly not; determinism flagged
    ([0.50, 0.55, 0.45, 0.52, 0.48], 0.86, 1.8569),     # between
    ([0.70, 0.72, 0.68, 0.71, 0.69], 1.20, 1.8569),     # low-shift gate fails
    ([0.1, 0.9, 0.5, 1.2, -0.2], 0.86, 1.8569),         # s_phi > 0.30
])
def test_conclusion_test_on_assembled_output(tmp_path, monkeypatch, phis, gate_val, det):
    """test_conclusions.test_r6_shuf_label_rule agrees with assemble() on synthetic flow results built on
    the recorded R6 and R6-NOMNU files; a tampered label fails it."""
    for name in ("r6", "r6_nomnu", "r2"):
        src = HERE / "results" / f"{name}.json"
        if not src.exists():
            pytest.skip(f"results/{name}.json not present")
        (tmp_path / src.name).write_bytes(src.read_bytes())
    rec6, rec5 = rs.check_r6(tmp_path / "r6.json"), rs.check_nomnu(tmp_path / "r6_nomnu.json")
    assert rec6["ok"] and rec5["ok"]
    n6, n5 = rec6["per_seed"], rec5["per_seed"]
    ns = {k: n6[k] - p * (n6[k] - n5[k]) for k, p in zip(SEEDS, phis)}
    env = {"versions": rec6["versions"], "settings": rec6["settings"]}
    vals = {"S": ns, "P": {k: v - 0.2 for k, v in ns.items()}, "SS": {k: v - 0.1 for k, v in ns.items()},
            "none": {0: det}}
    nomnu = json.loads((tmp_path / "r6_nomnu.json").read_text(encoding="utf-8"))
    gate6 = nomnu["settings"]["gates"]["gate6"]
    cfg = rs.config(SHORT, SEEDS, 10, {"tol": 0.02}, gate6, GATE_P, [1000, 2000, 3000], [0.06, 0.6], [20, 100])
    res = fs.finite(rs.plan(_fake_job([], gate_val, vals, env), cfg, lambda m: None, fs, expected=(rec6, rec5)))
    res["complete"] = True
    settings = {"r6_shuf_gate": GATE_P, "r6_shuf_knn_k": [20, 100], "gate_low": rs.low_gate(gate6, GATE_P)}
    out = rs.assemble(res, rec6, rec5, True, SEEDS, EMIN, SMAX, BAND, GATE_P, settings)
    out["parameters"] = SHORT
    expected = {0: rs.CORR, 1: rs.NOT_CORR, 2: rs.BETWEEN}
    if gate_val != 0.86:
        assert out["label"] == rs.NE_GATE
    elif max(phis) > 1:
        assert out["label"] == rs.NE and "s_phi" in out["reason"]
    else:
        assert out["label"] == expected[[[0.70, 0.72, 0.68, 0.71, 0.69], [0.20, 0.25, 0.15, 0.22, 0.18],
                                          [0.50, 0.55, 0.45, 0.52, 0.48]].index(phis)]
    assert out["gate_low_exact"]["equal_to_4_decimals"] is True
    assert out["determinism"]["flag"] == (rs.FLAG_DET if det == 1.90 else None)
    assert len(json.dumps(fs.finite(out))) < 1024 ** 2
    (tmp_path / "r6_shuf.json").write_text(json.dumps(fs.finite(out)), encoding="utf-8")
    tc = _import("test_conclusions")
    monkeypatch.setattr(tc, "RESULTS", tmp_path)
    tc.test_r6_shuf_label_rule()
    out["label"] = rs.BETWEEN if out["label"] != rs.BETWEEN else rs.CORR
    (tmp_path / "r6_shuf.json").write_text(json.dumps(fs.finite(out)), encoding="utf-8")
    with pytest.raises(AssertionError):
        tc.test_r6_shuf_label_rule()
