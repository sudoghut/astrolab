"""Offline tests of R6-SHUF-KA (README 2.9): the synthetic family (closed forms, variants, identity with the design
script), the exact values, the 'ka' job wiring, the label rules and the qualifier, the reuse of r6.json and
r6_shuf.json, the plan, the assembly and run.py's PARAMS and paths. No TensorFlow, no network, no flow training."""
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
    spec = importlib.util.spec_from_file_location(f"study008ka_{name}", path or HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


fs = _import("flowshift")
sys.path.insert(0, str(HERE))
try:
    ka = _import("r6ka")
finally:
    sys.path.remove(str(HERE))
design = _import("t047_ka_design", HERE / "explore" / "t047_ka_design.py")

FAMILY = {"mu1": 0.9, "mu2": 0.55, "curv": 0.3, "a": 2.5, "c": 1.4, "ubox": [0.05, 2.05, 0.2],
          "boxes": [[-0.6, 1.4, 0.05], [-0.6, 1.4, 0.05], [-0.6, 1.4, 0.05]]}
EXACT = {"n6": 1.8087, "S": 0.9263, "n5": 0.3652}
SEEDS = list(range(15, 25))
BAND, SMAX, EMIN = [0.40, 0.60], 0.30, 0.20


# ------------------------------------------------------------------ the family ----
def test_family_identical_to_design_script():
    """flowshift's ka_ functions are the design script's: identical draws and log densities."""
    assert design.CHOSEN == FAMILY
    a = fs.ka_sample(1000, np.random.default_rng(5), FAMILY)
    b = design.sample(1000, np.random.default_rng(5), FAMILY)
    assert a.tobytes() == b.tobytes()
    for v in ("6", "S", "5"):
        z = a if v != "5" else np.delete(a, 2, axis=1)
        assert np.array_equal(fs.ka_logp(z, FAMILY, v), design.logp(z, FAMILY, v))


def test_closed_forms_against_numerical_integration():
    design.check_density(FAMILY)                 # the design script's own check at the chosen member
    rng = np.random.default_rng(1)
    from scipy.stats import norm
    lo, hi, s = FAMILY["ubox"]
    v = np.linspace(lo, hi, 40001)
    for x1, u in fs.ka_sample(4, rng, FAMILY)[:, [0, 2]]:
        num = np.trapz(norm.pdf(u, v, s) * norm.pdf(x1, FAMILY["mu1"] + FAMILY["a"] * (v - FAMILY["c"]), 1.0), v) / (hi - lo)
        assert abs(np.log(num) - fs.ka_log_x1u(np.array([x1]), np.array([u]), FAMILY)[0]) < 1e-6
        num1 = np.trapz(norm.pdf(x1, FAMILY["mu1"] + FAMILY["a"] * (v - FAMILY["c"]), 1.0), v) / (hi - lo)
        assert abs(np.log(num1) - fs.ka_log_x1(np.array([x1]), FAMILY)[0]) < 1e-6


def test_variants_and_ds_independence():
    z6 = fs.ka_sample(200_000, np.random.default_rng(5015), FAMILY)
    zs = fs.ka_variant(z6, "S", np.random.default_rng(6015))
    z5 = fs.ka_variant(z6, "5")
    assert fs.ka_variant(z6, "6") is z6 and z5.shape == (200_000, 5) and np.array_equal(z5, np.delete(z6, 2, axis=1))
    assert np.array_equal(np.sort(zs[:, 2]), np.sort(z6[:, 2]))               # u's marginal kept
    assert np.array_equal(np.delete(zs, 2, axis=1), np.delete(z6, 2, axis=1))  # the rest unchanged
    assert abs(np.corrcoef(z6[:, 0], z6[:, 2])[0, 1] - 0.78) < 0.02            # coupled in D6
    assert abs(np.corrcoef(zs[:, 0], zs[:, 2])[0, 1]) < 0.01                   # independent after the permutation
    assert np.array_equal(zs[:, 2], z6[np.random.default_rng(6015).permutation(200_000), 2])
    assert fs.ka_names("5") == ["x1", "x2", "b1", "b2", "b3"] and fs.ka_names("S") == fs.KA_NAMES6
    with pytest.raises(ValueError):
        fs.ka_variant(z6, "P")


def test_exact_values_reproduce_the_registered_ones():
    e = ka.exact_values(FAMILY, fs)
    c = ka.exact_check(e, EXACT)
    assert c["ok"] and max(c["abs_diff"].values()) < 0.0005
    assert abs(e["phi"] - 0.6113) < 0.0005
    bad = ka.exact_check(e, dict(EXACT, S=EXACT["S"] + 0.006))
    assert not bad["ok"]


def test_run_job_ka(tmp_path, monkeypatch):
    cfg = ka.config(SEEDS, 3000, {"tol": 0.02}, FAMILY, [5000, 6000])
    seen = {}

    def fake(diff, names, seed, est, pop_size=None, record_pop=False):
        seen.update(diff=diff, names=names, seed=seed, pop_size=pop_size, record_pop=record_pop)
        return {"seed": seed, "n_sigma": 1.0, "converged": True, "lower_bound": False}

    monkeypatch.setattr(fs, "one_shift", fake)
    z6 = fs.ka_sample(3000, np.random.default_rng(5017), FAMILY)
    out = fs.run_job(["ka", "S", "17"], str(tmp_path / "unused.npz"), json.loads(json.dumps(cfg)))
    assert out["variant"] == "S" and out["seed"] == 17 and seen["pop_size"] is None and seen["record_pop"]
    assert np.array_equal(seen["diff"], fs.ka_variant(z6, "S", np.random.default_rng(6017)))
    assert seen["names"] == fs.KA_NAMES6
    fs.run_job(["ka", "5", "17"], str(tmp_path / "unused.npz"), cfg)
    assert np.array_equal(seen["diff"], np.delete(z6, 2, axis=1)) and seen["names"] == fs.ka_names("5")
    fs.run_job(["ka", "6", "17"], str(tmp_path / "unused.npz"), cfg)
    assert np.array_equal(seen["diff"], z6)
    bad = fs.run_job(["ka", "Q", "17"], str(tmp_path / "unused.npz"), cfg)
    assert "error" in bad and bad["seed"] == 17


# ------------------------------------------------------------------ rules ----
def _reps(n6, ns, n5, seeds=SEEDS, bad=None):
    out = {}
    for v, vals in (("6", n6), ("S", ns), ("5", n5)):
        out[v] = [{"seed": k, "n_sigma": vals[i], "converged": True, "lower_bound": False} for i, k in enumerate(seeds)]
    if bad:
        v, i, key, val = bad
        out[v][i][key] = val
    return out


def _vals(phi_shift=0.0, scatter=0.0):
    """n6 = 1.8, n5 = 0.4: phi_k = 0.6113 + shift + scatter * (+-1 alternating)."""
    n6 = [1.8] * 10
    n5 = [0.4] * 10
    ns = [1.8 - (0.6113 + phi_shift + scatter * (1 if i % 2 else -1)) * 1.4 for i in range(10)]
    return n6, ns, n5


def test_label_rule_order():
    n6, ns, n5 = _vals()
    assert ka.label(True, True, False, _reps(n6, ns, n5), SEEDS, 0.6113, EMIN, SMAX)[0] == ka.NE
    assert ka.label(False, True, True, _reps(n6, ns, n5), SEEDS, 0.6113, EMIN, SMAX)[0] == ka.NE
    assert ka.label(True, False, True, _reps(n6, ns, n5), SEEDS, 0.6113, EMIN, SMAX)[0] == ka.NE
    for bad in (("S", 3, "converged", False), ("5", 0, "lower_bound", True), ("6", 9, "n_sigma", float("nan"))):
        assert ka.label(True, True, True, _reps(n6, ns, n5, bad=bad), SEEDS, 0.6113, EMIN, SMAX)[0] == ka.NE
    reps = _reps(n6, ns, n5)
    reps["5"] = reps["5"][:9]
    assert ka.label(True, True, True, reps, SEEDS, 0.6113, EMIN, SMAX)[0] == ka.NE
    lab, why, _ = ka.label(True, True, True, _reps(n6, ns, [1.65] * 10), SEEDS, 0.6113, EMIN, SMAX)
    assert lab == ka.NE and "E_k" in why                                          # rule 3: E <= 0.20
    lab, why, _ = ka.label(True, True, True, _reps(*_vals(scatter=0.4)), SEEDS, 0.6113, EMIN, SMAX)
    assert lab == ka.NE and "s_b" in why                                          # rule 3: s_b > 0.30
    one = _reps([1.8], [0.95], [0.4], seeds=[15])
    assert ka.label(True, True, True, one, [15], 0.6113, EMIN, SMAX)[0] == ka.NE   # an exploration with one seed


def test_label_outcomes():
    lab, _, nums = ka.label(True, True, True, _reps(*_vals(0.10, 0.02)), SEEDS, 0.6113, EMIN, SMAX)
    assert lab.startswith(ka.OVER) and abs(nums["b_bar"] - 0.10) < 1e-9
    assert abs(nums["half_width"] - 2 * nums["s_b"] / math.sqrt(10)) < 1e-15
    lab, _, _ = ka.label(True, True, True, _reps(*_vals(-0.10, 0.02)), SEEDS, 0.6113, EMIN, SMAX)
    assert lab.startswith(ka.UNDER)
    lab, _, _ = ka.label(True, True, True, _reps(*_vals(0.01, 0.10)), SEEDS, 0.6113, EMIN, SMAX)
    assert lab.startswith(ka.NONE)


def test_qualifier_order():
    # holds: phi 0.671, s 0.037 (5 seeds); b -0.05, s_b 0.03 (10): w small, corrected 0.721
    q = ka.qualifier(0.671, 0.037, 5, -0.05, 0.03, 10, BAND)
    assert q["qualifier"] == ka.Q_HOLDS
    assert abs(q["w"] - 2 * math.sqrt(0.037 ** 2 / 5 + 0.03 ** 2 / 10)) < 1e-15
    # reverses even with a noisy test (b large): a noisy test never hides a decisive correction
    q = ka.qualifier(0.671, 0.037, 5, 0.40, 0.12, 10, BAND)
    assert q["qualifier"] == ka.Q_REVERSES and 0.671 - q["w"] < 0.60
    # holds with a noisy test and a large negative bias
    q = ka.qualifier(0.671, 0.037, 5, -0.20, 0.12, 10, BAND)
    assert q["qualifier"] == ka.Q_HOLDS
    # not decisive (noise): no-bias interval would already reach below 0.60
    q = ka.qualifier(0.671, 0.037, 5, 0.0, 0.12, 10, BAND)
    assert q["qualifier"].startswith(ka.Q_NOISY[:-1] + ": w = ")
    # not decided (bias, precise test)
    q = ka.qualifier(0.671, 0.037, 5, 0.06, 0.03, 10, BAND)
    assert q["qualifier"] == ka.Q_UNDECIDED and 0.671 - q["w"] >= 0.60


# ------------------------------------------------------------------ records, plan, assembly ----
def _shuf_file(tmp_path, label=None, phis=(0.68, 0.64, 0.71, 0.69, 0.63)):
    import r6shuf
    d = {"label": label or r6shuf.CORR,
         "quantities": {"phi": {"values": list(phis), "mean": float(np.mean(phis)), "s": float(np.std(phis, ddof=1))}},
         "flows": {"versions": {"tensorflow": "2.21.0"}, "settings": {"pop_size": 10}}}
    p = tmp_path / "r6_shuf.json"
    p.write_text(json.dumps(d), encoding="utf-8")
    return p


def test_check_shuf(tmp_path):
    sys.path.insert(0, str(HERE))
    try:
        r = ka.check_shuf(_shuf_file(tmp_path))
        assert r["ok"] and r["n"] == 5 and abs(r["phi_bar"] - 0.67) < 1e-12
        assert not ka.check_shuf(tmp_path / "missing.json")["ok"]
        assert not ka.check_shuf(_shuf_file(tmp_path, label="between the two labels (not decided)"))["ok"]
        assert not ka.check_shuf(_shuf_file(tmp_path, phis=(0.6, 0.7)))["ok"]
    finally:
        sys.path.remove(str(HERE))
    rec = HERE / "results" / "r6_shuf.json"
    if rec.exists():                                                      # the recorded file passes
        r = ka.check_shuf(rec)
        assert r["ok"] and abs(r["phi_bar"] - 0.6712464641998024) < 1e-12 and abs(r["s_phi"] - 0.036637218257397214) < 1e-12


ENV = {"versions": {"tensorflow": "2.21.0"}, "settings": {"pop_size": 10}}


def _job(calls, vals=None, env=None, crash=()):
    vals = vals or {}

    def job(*parts):
        calls.append(parts)
        if parts in crash:
            raise RuntimeError("job failed (code 1)")
        if parts[0] == "meta":
            return copy.deepcopy(env or ENV)
        v, k = parts[1], parts[2]
        return {"seed": k, "n_sigma": vals.get(v, {}).get(k, {"6": 1.8, "S": 0.95, "5": 0.4}[v]),
                "converged": True, "lower_bound": False, "variant": v}
    return job


def test_plan_order_and_env_mismatch():
    cfg = ka.config(SEEDS, 10, {"tol": 0.02}, FAMILY, [5000, 6000])
    calls = []
    res = ka.plan(_job(calls), cfg, lambda m: None, fs, expected=({**ENV, "ok": True}, {**ENV, "ok": True}))
    assert calls[0] == ("meta",)
    assert calls[1:] == [("ka", v, k) for k in SEEDS for v in ("6", "S", "5")]
    assert [r["seed"] for r in res["S"]] == SEEDS
    calls = []
    res = ka.plan(_job(calls, env={"versions": {"tensorflow": "2.20"}, "settings": {"pop_size": 10}}), cfg,
                  lambda m: None, fs, expected=({**ENV, "ok": True}, {**ENV, "ok": True}))
    assert calls == [("meta",)] and "status_runs" in res
    calls = []
    res = ka.plan(_job(calls, crash={("ka", "S", 17)}), cfg, lambda m: None, fs)
    assert res["S"][2] == {"seed": 17, "error": "subprocess failed"} and len(calls) == 31


def test_assemble(tmp_path):
    sys.path.insert(0, str(HERE))
    try:
        recs = ka.check_shuf(_shuf_file(tmp_path))
    finally:
        sys.path.remove(str(HERE))
    rec6 = {"ok": True, **ENV}
    exact = {"n6": 1.8087, "S": 0.9263, "n5": 0.3652, "phi": 0.6113}
    cfg = ka.config(SEEDS, 10, {"tol": 0.02}, FAMILY, [5000, 6000])
    res = ka.plan(_job([]), cfg, lambda m: None, fs)
    out = ka.assemble(res, rec6, recs, exact, EXACT, SEEDS, EMIN, SMAX, BAND, {"r6_ka": True})
    # phi_k = (1.8 - 0.95)/(1.4) = 0.6071 for every seed: s_b = 0 -> interval [b, b] below 0
    assert out["label"].startswith(ka.UNDER) and abs(out["numbers"]["b_bar"] - (0.85 / 1.4 - 0.6113)) < 1e-12
    assert out["summary"]["qualifier"] == out["qualifier"]["qualifier"] == ka.Q_HOLDS
    assert set(out["offsets"]) == {"6", "S", "5"} and abs(out["offsets"]["S"]["mean"] - (0.95 - 0.9263)) < 1e-12
    out2 = ka.assemble({"status": "not run (R6 or R6-SHUF record not reusable)"}, rec6, recs, exact, EXACT, SEEDS,
                       EMIN, SMAX, BAND, {})
    assert out2["label"] == ka.NE and "qualifier" not in out2
    out3 = ka.assemble(res, rec6, recs, dict(exact, S=0.95), EXACT, SEEDS, EMIN, SMAX, BAND, {})
    assert out3["label"] == ka.NE and "exact" in out3["reason"]
    res_bad = ka.plan(_job([], env={"versions": {"tensorflow": "2.20"}, "settings": {"pop_size": 10}}), cfg,
                      lambda m: None, fs)
    out4 = ka.assemble(res_bad, rec6, recs, exact, EXACT, SEEDS, EMIN, SMAX, BAND, {})
    assert out4["label"] == ka.NE and "versions" in out4["reason"]


def test_run_params_and_paths():
    src = (HERE / "run.py").read_text(encoding="utf-8")
    assert 'ctx.study.results_dir / "r6_shuf.json"' in src and 'ctx.study.results_dir / "r6_ka.json"' in src
    tree = ast.parse(src)
    saves = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and ast.unparse(n.func) == "ctx.save"
             and n.args and ast.unparse(n.args[0]) in ("'r6_shuf'", "'r6_ka'")]
    assert len(saves) == 2
    # the R6-SHUF save and its training run only when r6_shuf_retrain is true
    guard = [n for n in ast.walk(tree) if isinstance(n, ast.If) and ast.unparse(n.test) == "P['r6_shuf']"]
    assert len(guard) == 1 and any(ast.unparse(s.args[0]) == "'r6_shuf'" for b in guard[0].body
                                   for s in ast.walk(b) if isinstance(s, ast.Call) and ast.unparse(s.func) == "ctx.save")
    sys.path.insert(0, str(HERE))
    try:
        run = _import("run")
    finally:
        sys.path.remove(str(HERE))
    P = run.PARAMS
    assert P["r6_ka"] is False and P["r6_shuf_retrain"] is False and P["r6_ka_seeds"] == SEEDS
    assert P["r6_ka_family"] == FAMILY and P["r6_ka_exact"] == EXACT and P["r6_ka_seed_offsets"] == [5000, 6000]
    assert P["r6_shuf_e_min"] == EMIN and P["r6_shuf_s_max"] == SMAX and P["r6_shuf_band"] == BAND
    # TF seeds and data streams disjoint from R6, R6-NOMNU, R6-SHUF and the gates
    used_tf = set(range(0, 5)) | {10, 11, 12}
    assert not used_tf & set(SEEDS)
    used_rng = {k + o for k in range(5) for o in (0, 1000, 2000, 3000)} | {1010, 1011, 1012, 999}
    assert not used_rng & {o + k for k in SEEDS for o in (5000, 6000)}


def test_conclusion_check_on_assembled_output(tmp_path):
    """test_conclusions.check_r6_ka accepts an assembled record and rejects a changed qualifier."""
    sys.path.insert(0, str(HERE))
    try:
        recs = ka.check_shuf(_shuf_file(tmp_path))
        tc = _import("test_conclusions")
    finally:
        sys.path.remove(str(HERE))
    exact = {"n6": 1.8087, "S": 0.9263, "n5": 0.3652, "phi": 0.6113}
    cfg = ka.config(SEEDS, 10, {"tol": 0.02}, FAMILY, [5000, 6000])
    vals = {"S": {k: 0.95 + 0.02 * ((k % 3) - 1) for k in SEEDS}}
    res = ka.plan(_job([], vals=vals), cfg, lambda m: None, fs)
    out = json.loads(json.dumps(ka.assemble(res, {"ok": True, **ENV}, recs, exact, EXACT, SEEDS, EMIN, SMAX, BAND, {})))
    tc.check_r6_ka(out)
    bad = copy.deepcopy(out)
    bad["qualifier"]["qualifier"] = ka.Q_HOLDS if out["qualifier"]["qualifier"] != ka.Q_HOLDS else ka.Q_UNDECIDED
    with pytest.raises(AssertionError):
        tc.check_r6_ka(bad)


def test_draws_identical_under_the_tf_environment(tmp_path):
    """README 2.9 amendment 3: the TF environment's numpy gives the same D6 rows and (S) permutation as the project's
    (skipped when venv-tf is absent)."""
    import subprocess
    sys.path.insert(0, str(HERE))
    try:
        r6flow = _import("r6flow")
    finally:
        sys.path.remove(str(HERE))
    exe = r6flow.tf_python()
    if exe is None:
        pytest.skip("no TF environment")
    code = ("import sys, json, numpy as np; sys.path.insert(0, sys.argv[1]); import flowshift as fs; "
            "F = json.loads(sys.argv[2]); z = fs.ka_sample(2000, np.random.default_rng(5015), F); "
            "s = fs.ka_variant(z, 'S', np.random.default_rng(6015)); np.save(sys.argv[3], np.concatenate([z, s]))")
    out = tmp_path / "tf.npy"
    subprocess.run([str(exe), "-I", "-c", code, str(HERE), json.dumps(FAMILY), str(out)], check=True, timeout=300)
    z = fs.ka_sample(2000, np.random.default_rng(5015), FAMILY)
    here = np.concatenate([z, fs.ka_variant(z, "S", np.random.default_rng(6015))])
    assert np.load(out).tobytes() == here.tobytes()
