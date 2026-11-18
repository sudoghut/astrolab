"""Offline tests of R6-NOMNU (README 2.7): label rules, pop_size comparison, reuse of r6.json, the
dimension-general gate and the job plans. No TensorFlow, no network, no flow training."""
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


def _import(name):
    spec = importlib.util.spec_from_file_location(f"study008_{name}", HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


nm = _import("r6nomnu")
fs = _import("flowshift")

GATE6 = {"mu1": 2.0, "mu2": 1.0, "curv": 0.3,
         "boxes": [[-0.6, 1.4, 0.05], [-0.6, 1.4, 0.05], [-0.6, 1.4, 0.05], [-0.1, 1.9, 0.1]],
         "n_exact": 2_000_000, "exact_seed": 999, "seeds": [10, 11, 12], "sample_seed_offset": 1000,
         "tol_mean": 0.10, "tol_each": 0.20}
BANDS, SMAX = [1.00, 1.40], 0.15


def _reps(vals, lower=(), conv=True):
    return [{"seed": k, "n_sigma": v, "lower_bound": k in lower, "converged": conv} for k, v in enumerate(vals)]


# ------------------------------------------------------------------ label rules ----
def test_label_rule_order_and_bands():
    good = _reps([1.2, 1.21, 1.19, 1.2, 1.2])
    assert nm.label(good, False, True, BANDS, SMAX)[0] == nm.NE                    # rule 1 (R1)
    assert nm.label(good, True, False, BANDS, SMAX)[0] == nm.NE                    # rule 1 (5-D gate)
    bad = good[:4] + [{"seed": 4, "error": "x"}]
    assert nm.label(bad, True, True, BANDS, SMAX)[0] == nm.NE                      # rule 2 (failed)
    assert nm.label(_reps([1.2, None, 1.2, 1.2, 1.2]), True, True, BANDS, SMAX)[0] == nm.NE
    assert nm.label(_reps([1.2] * 5, conv=False), True, True, BANDS, SMAX)[0] == nm.NE
    # rule 3: a lower bound; the minimum over all five decides
    assert nm.label(_reps([1.5, 2.0, 1.45, 1.6, 1.4], lower={1}), True, True, BANDS, SMAX)[0] == nm.NOT_MAINLY
    assert nm.label(_reps([1.5, 2.0, 1.39, 1.6, 1.5], lower={1}), True, True, BANDS, SMAX)[0] == nm.NE
    # rule 3 precedes rule 4 (a huge spread does not matter when a bound is present)
    assert nm.label(_reps([1.5, 9.0, 1.45, 1.6, 1.4], lower={1}), True, True, BANDS, SMAX)[0] == nm.NOT_MAINLY
    # rule 4
    lab, why, nums = nm.label(_reps([1.0, 1.4, 1.2, 1.6, 0.8]), True, True, BANDS, SMAX)
    assert lab == nm.NE and nums["s"] > SMAX
    # rule 5
    assert nm.label(_reps([0.80, 0.82, 0.78, 0.81, 0.79]), True, True, BANDS, SMAX)[0] == nm.MAINLY
    assert nm.label(_reps([1.60, 1.62, 1.58, 1.61, 1.59]), True, True, BANDS, SMAX)[0] == nm.NOT_MAINLY
    assert nm.label(good, True, True, BANDS, SMAX)[0] == nm.PARTLY
    assert nm.label(_reps([1.00, 1.02, 0.98, 1.01, 0.99]), True, True, BANDS, SMAX)[0] == nm.BETWEEN
    assert nm.label(_reps([1.40, 1.42, 1.38, 1.41, 1.39]), True, True, BANDS, SMAX)[0] == nm.BETWEEN


def test_label_interval_unrounded_and_half_open_edges():
    vals = [1.31, 1.12, 1.25, 1.18, 1.29]
    lab, _, nums = nm.label(_reps(vals), True, True, BANDS, SMAX)
    s = float(np.std(vals, ddof=1))
    assert nums["s"] == pytest.approx(s) and nums["half_width"] == pytest.approx(2 * s / math.sqrt(5))
    # I touching 1.00 from below is inside (-inf, 1.00]; touching 1.40 from above is inside [1.40, inf)
    zero = _reps([1.0] * 5)
    assert nm.label(zero, True, True, BANDS, SMAX)[0] == nm.MAINLY
    assert nm.label(_reps([1.4] * 5), True, True, BANDS, SMAX)[0] == nm.NOT_MAINLY


# ------------------------------------------------------------------ pop_size comparison ----
def test_pop_compare():
    r10 = _reps([1.86, 1.64, 1.72, 1.61, 1.67])
    same = nm.pop_compare(r10, _reps([1.80, 1.66, 1.70, 1.60, 1.70]), 6.39)
    assert same["spread"].startswith("no detectable") and same["means"].startswith("means do not")
    wide = nm.pop_compare(r10, _reps([2.6, 1.0, 1.7, 2.2, 1.2]), 6.39)
    assert wide["variance_ratio"] > 6.39 and wide["spread"] == "spreads differ"
    shifted = nm.pop_compare(r10, _reps([1.30, 1.32, 1.28, 1.31, 1.29]), 6.39)
    assert shifted["means"] == "means differ"
    assert shifted["paired_pop1_minus_default"]["per_seed"]["0"] == pytest.approx(1.30 - 1.86)
    failed = nm.pop_compare(r10, r10[:4] + [{"seed": 4, "error": "x"}], 6.39)
    assert failed["status"].startswith("not computed") and failed["failed_pop1"] == [4]


# ------------------------------------------------------------------ reuse of r6.json ----
def _r6(tmp_path, mutate=None):
    src = HERE / "results" / "r6.json"
    if not src.exists():
        pytest.skip("results/r6.json not present")
    d = json.loads(src.read_text(encoding="utf-8"))
    if mutate:
        mutate(d)
    p = tmp_path / "r6.json"
    p.write_text(json.dumps(d), encoding="utf-8")
    return p


def test_check_r6_recorded_and_tampered(tmp_path):
    ok = nm.check_r6(_r6(tmp_path))
    assert ok["ok"] and sorted(ok["per_seed"]) == [0, 1, 2, 3, 4] and round(ok["n_bar"], 4) == 1.6985
    assert not nm.check_r6(tmp_path / "missing.json")["ok"]

    def setter(path, value):
        def f(d):
            o = d
            for k in path[:-1]:
                o = o[k]
            o[path[-1]] = value
        return f

    tampered = [
        setter(["flows", "complete"], False),
        setter(["flows", "gate", "passed"], False),
        setter(["flows", "main", "n_bar"], 1.6987),
        setter(["flows", "main", "s"], 0.0979),
        lambda d: d["flows"]["main"]["repetitions"].pop(),
        lambda d: d["flows"]["main"]["repetitions"][2].update(n_sigma=None),
        lambda d: d["flows"]["main"]["repetitions"][0].update(seed=7),
        lambda d: d["flows"].pop("main"),
    ]
    for i, m in enumerate(tampered):
        sub = tmp_path / str(i)
        sub.mkdir()
        assert not nm.check_r6(_r6(sub, m))["ok"], i
    bad = tmp_path / "bad"
    bad.mkdir()
    (bad / "r6.json").write_text("{not json", encoding="utf-8")
    assert not nm.check_r6(bad / "r6.json")["ok"]


def test_run_reuse_path_never_writes_or_trains_r6():
    """With r6_retrain False, run.py neither calls R6's training nor saves r6.json: every such call
    sits inside the `if P["r6_retrain"]:` block (static check of run.py)."""
    src = (HERE / "run.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    guard = [n for n in ast.walk(tree) if isinstance(n, ast.If) and ast.unparse(n.test) == "P['r6_retrain']"]
    assert len(guard) == 1
    inside = {id(n) for stmt in guard[0].body for n in ast.walk(stmt)}
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)]
    sensitive = [c for c in calls if ast.unparse(c.func) in ("r6flow.run_flows", "r6flow.verdict")
                 or (ast.unparse(c.func) == "ctx.save" and c.args and ast.unparse(c.args[0]) == "'r6'")]
    assert len(sensitive) == 3 and all(id(c) in inside for c in sensitive)
    sys.path.insert(0, str(HERE))
    try:
        run = _import("run")
    finally:
        sys.path.remove(str(HERE))
    P = run.PARAMS
    assert P["r6_retrain"] is False and P["r6_nomnu"] is True and P["r6_pop1"] is True
    assert P["r6_nomnu_seeds"] == [0, 1, 2, 3, 4] and P["r6_nomnu_s_max"] == 0.15
    assert P["r6_nomnu_bands"] == [1.00, 1.40]


# ------------------------------------------------------------------ gate generalisation ----
def _old_exact(g):
    """flowshift.synthetic_exact as recorded for R6 (6-D reference point hard-coded)."""
    from scipy.stats import norm

    def logp(z):
        x1, x2 = z[:, 0], z[:, 1]
        out = norm.logpdf(x1, g["mu1"], 1.0) + norm.logpdf(x2 - g["curv"] * (x1 - g["mu1"]) ** 2, g["mu2"], 1.0)
        for i, (lo, hi, s) in enumerate(g["boxes"]):
            u = z[:, 2 + i]
            out = out + np.log(np.clip(norm.cdf((u - lo) / s) - norm.cdf((u - hi) / s), 1e-300, None) / (hi - lo))
        return out

    z = fs.synthetic(g["n_exact"], np.random.default_rng(g["exact_seed"]), g)
    p = float(np.mean(logp(z) > logp(np.zeros((1, 6)))[0]))
    return {"delta": p, "n_sigma": fs._nsigma(p)}


def test_gate_generalisation():
    small6 = {**GATE6, "n_exact": 20_000, "exact_seed": 5}      # not the formal 2,000,000 / seed 999
    assert fs.synthetic_exact(small6) == _old_exact(small6)
    assert fs.gate_names(small6) == [f"x{i}" for i in range(6)]
    g5, dropped = nm.gate5(GATE6)
    assert dropped == [-0.1, 1.9, 0.1] and len(g5["boxes"]) == 3 and len(GATE6["boxes"]) == 4
    assert fs.gate_dim(g5) == 5 and fs.gate_names(g5) == [f"x{i}" for i in range(5)]
    # same generators: the 5-D rows are R6's first five columns
    x6 = fs.synthetic(1000, np.random.default_rng(1010), GATE6)
    x5 = fs.synthetic(1000, np.random.default_rng(1010), g5)
    assert x5.shape == (1000, 5) and np.array_equal(x5, x6[:, :5])
    small5 = {**g5, "n_exact": 20_000, "exact_seed": 5}
    r5 = fs.synthetic_exact(small5)                                # 5-D reference point (6-D would fail)
    assert 0 < r5["delta"] < 1 and math.isfinite(r5["n_sigma"])


# ------------------------------------------------------------------ configuration and plans ----
SHORT = ["a_s_1e9", "h0", "mnu", "n_s", "omega_b", "omega_m"]


def test_config():
    g6 = copy.deepcopy(GATE6)
    cfg = nm.config(SHORT, [0, 1, 2, 3, 4], 100_000, {"tol": 0.02}, g6, True)
    assert g6 == GATE6                                             # PARAMS not mutated
    assert cfg["cases"]["nomnu"]["columns"] == ["a_s_1e9", "h0", "n_s", "omega_b", "omega_m"]
    assert cfg["cases"]["main_pop1"]["columns"] == SHORT
    assert cfg["cases"]["nomnu"]["pop_size"] is None and cfg["cases"]["nomnu_pop1"]["pop_size"] == 1
    assert len(cfg["gates"]["g5"]["boxes"]) == 3 and len(cfg["gates"]["g6_pop1"]["boxes"]) == 4
    assert cfg["gates"]["g5"]["pop_size"] is None and cfg["gates"]["g6_pop1"]["pop_size"] == 1
    assert set(nm.config(SHORT, [0], 1, {}, GATE6, False)["cases"]) == {"nomnu"}


def _fake_job(calls, gate_val):
    def job(*parts):
        calls.append(parts)
        if parts[0] == "meta":
            return {"versions": {}, "settings": {}}
        if parts[0] == "exact":
            return {"delta": 0.9, "n_sigma": 2.0}
        return {"seed": parts[-1], "n_sigma": gate_val if parts[0] == "gate" else 1.2,
                "lower_bound": False, "converged": True}
    return job


@pytest.mark.parametrize("gate_val", [2.0, 3.0])
def test_nomnu_plan_order_and_gate_failure(gate_val):
    cfg = nm.config(SHORT, [0, 1, 2, 3, 4], 10, {}, GATE6, True)
    calls = []
    res = nm.plan(_fake_job(calls, gate_val), cfg, lambda m: None, fs)
    names = [c[1] if len(c) > 1 else c[0] for c in calls]
    assert res["gate5"]["passed"] is (gate_val == 2.0)
    order = ["meta", "g5", "g5", "g5", "g5"]
    if gate_val == 2.0:
        order += ["nomnu"] * 5
    else:
        assert res["nomnu"]["status"].startswith("not run")
    order += ["g5_pop1"] * 3 + ["g6_pop1"] * 4 + ["nomnu_pop1"] * 5 + ["main_pop1"] * 5
    assert names == order
    out = nm.assemble(fs.finite(res), {"ok": True, "repetitions": _reps([1.86, 1.64, 1.72, 1.61, 1.67]),
                                       "n_bar": 1.7, "gate_exact": 2.0}, True, BANDS, SMAX, 0.07, 6.39, {})
    assert out["label"] == (nm.PARTLY if gate_val == 2.0 else nm.NE)
    assert out["pop_size_comparison"]["6d"]["means"] == "means differ"
    assert out["gate6_exact_recomputed"]["equal"] is True
    assert len(json.dumps(out)) < 1024 ** 2


def test_r6_plan_job_sequence_unchanged():
    """R6's job order through the refactored run_jobs plan equals the recorded run's order."""
    rf = _import("r6flow")
    cases = {"main": {"columns": SHORT, "seeds": [0, 1, 2, 3, 4]},
             "flow_2d": {"columns": ["s8", "omega_m"], "seeds": [0, 1, 2]}}
    calls = []
    res = rf._r6_plan(_fake_job(calls, 2.0), {"gate": GATE6, "cases": cases}, lambda m: None, fs)
    assert calls == ([("meta",), ("exact",)] + [("gate", k) for k in (10, 11, 12)]
                     + [("case", "main", k) for k in range(5)] + [("case", "flow_2d", k) for k in range(3)])
    assert res["gate"]["passed"] and res["main"]["n_bar"] == pytest.approx(1.2)


def test_flowshift_r6_jobs_do_not_record_pop_size():
    """R6 job configs (no 'pop_size' key) keep R6's call and result keys."""
    src = (HERE / "flowshift.py").read_text(encoding="utf-8")
    assert "sp.flow_from_chain(chain, feedback=0, plot_every=0)\n" in src
    assert '"pop_size" in g' in src and '"pop_size" in case' in src


@pytest.mark.parametrize("vals5, pop_vals, gate_val", [
    ([1.2, 1.25, 1.15, 1.22, 1.18], [1.3, 1.1, 1.2, 1.25, 1.15], 2.0),     # partly; spreads similar
    ([0.8, 0.82, 0.78, 0.81, 0.79], [2.6, 1.0, 1.7, 2.2, 1.2], 2.0),       # mainly; spreads differ
    ([1.2] * 5, [1.2] * 5, 3.0),                                          # 5-D gate fails
])
def test_conclusion_test_on_assembled_output(tmp_path, monkeypatch, vals5, pop_vals, gate_val):
    """The conclusion test in test_conclusions.py agrees with assemble() on synthetic flow results."""
    for name in ("r6", "r2"):
        src = HERE / "results" / f"{name}.json"
        if not src.exists():
            pytest.skip(f"results/{name}.json not present")
        (tmp_path / src.name).write_bytes(src.read_bytes())
    r6 = json.loads((tmp_path / "r6.json").read_text(encoding="utf-8"))
    short = [n.split("--")[-1] for n in r6["flows"]["main"]["parameters"]]
    exact6 = r6["flows"]["gate"]["exact"]
    cfg = nm.config(short, [0, 1, 2, 3, 4], 10, {}, GATE6, True)

    def job(*parts):
        if parts[0] == "meta":
            return {"versions": {}, "settings": {}}
        if parts[0] == "exact":
            return exact6 if parts[1] == "g6_pop1" else {"delta": 0.9, "n_sigma": 2.0}
        k = parts[-1]
        rec = {"seed": k, "lower_bound": False, "converged": True, "delta": 0.5}
        if parts[0] == "gate":
            g = cfg["gates"][parts[1]]
            v = exact6["n_sigma"] if parts[1] == "g6_pop1" else gate_val
            return {**rec, "n_sigma": v, "pop_size": g["pop_size"] or 10, "pop_size_passed": g["pop_size"] is not None}
        c = cfg["cases"][parts[1]]
        v = {"nomnu": vals5, "nomnu_pop1": pop_vals, "main_pop1": pop_vals}[parts[1]][k]
        return {**rec, "n_sigma": v, "pop_size": c["pop_size"] or 10, "pop_size_passed": c["pop_size"] is not None}

    res = fs.finite(nm.plan(job, cfg, lambda m: None, fs))
    rec = nm.check_r6(tmp_path / "r6.json")
    out = nm.assemble(res, rec, True, BANDS, SMAX, 0.07, 6.39, {})
    out.update(parameters=short, parameters_match_r6=True)
    (tmp_path / "r6_nomnu.json").write_text(json.dumps(fs.finite(out)), encoding="utf-8")
    tc = _import("test_conclusions")
    monkeypatch.setattr(tc, "RESULTS", tmp_path)
    tc.test_r6_nomnu_label_rule()
    # a tampered label must fail the conclusion test
    out["label"] = nm.BETWEEN if out["label"] != nm.BETWEEN else nm.PARTLY
    (tmp_path / "r6_nomnu.json").write_text(json.dumps(fs.finite(out)), encoding="utf-8")
    with pytest.raises(AssertionError):
        tc.test_r6_nomnu_label_rule()
