"""Offline tests of R6-SHUF-KA2 (README 2.10): the surrogate (committed file and hash, mixture densities, variants,
identity with the design script), the exact values, the 'ka2' job wiring, the label rules, the qualifier, the
comparison with R6-SHUF-KA, the reuse of the recorded files, the plan, the assembly and run.py's PARAMS and paths.
No TensorFlow, no network, no flow training."""
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
    spec = importlib.util.spec_from_file_location(f"study008ka2_{name}", path or HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


fs = _import("flowshift")
sys.path.insert(0, str(HERE))
try:
    ka2 = _import("r6ka2")
    design = _import("t063_surrogate_design", HERE / "explore" / "t063_surrogate_design.py")
finally:
    sys.path.remove(str(HERE))

SHA = "ba050dc4b15c945c2185398c21b97d0c8116208afc872bd71c842592323aff76"
EXACT = {"n6": 1.3768, "S": 0.6678, "n5": 0.3341}
SEEDS = list(range(25, 35))
BAND, SMAX, EMIN = [0.40, 0.60], 0.30, 0.20
SUR = ka2.load_surrogate(HERE / "surrogate_t063.json", SHA)
MD, MC = SUR["mixtures"]["des_3x2pt"], SUR["mixtures"]["cmb"]
PHI_EXACT = (1.3768 - 0.6678) / (1.3768 - 0.3341)


def _small():
    """A small mixture pair (2 DES and 2 CMB components, 6-D) for fast density checks."""
    rng = np.random.default_rng(3)

    def mx(k):
        L = []
        for _ in range(k):
            a = rng.normal(size=(6, 6)) * 0.3
            L.append(np.linalg.cholesky(a @ a.T + np.eye(6) * 0.5).tolist())
        w = rng.uniform(0.3, 1.0, k)
        return {"w": (w / w.sum()).tolist(), "mu": rng.normal(size=(k, 6)).tolist(), "L": L}
    return mx(2), mx(2)


# ------------------------------------------------------------------ the surrogate ----
def test_committed_surrogate_and_hash(tmp_path):
    assert SUR["ok"] and SUR["sha256"] == SHA
    assert SUR["columns"] == ["a_s_1e9", "h0", "mnu", "n_s", "omega_b", "omega_m"] and SUR["columns"][fs.SUR_MNU] == "mnu"
    for key in ("des_3x2pt", "cmb"):
        m = SUR["mixtures"][key]
        assert len(m["w"]) == 8 and abs(sum(m["w"]) - 1) < 1e-9 and np.asarray(m["L"]).shape == (8, 6, 6)
    raw = (HERE / "surrogate_t063.json").read_bytes().replace(b"\r\n", b"\n")
    crlf = tmp_path / "crlf.json"
    crlf.write_bytes(raw.replace(b"\n", b"\r\n"))
    assert ka2.file_sha256(crlf) == SHA                                   # a CRLF checkout gives the same hash
    changed = tmp_path / "changed.json"
    changed.write_bytes(raw.replace(b'"w"', b'"w" ', 1))
    assert not ka2.load_surrogate(changed, SHA)["ok"]
    assert not ka2.load_surrogate(tmp_path / "missing.json", SHA)["ok"]
    d = json.loads(raw)
    assert d["exact_design"]["6"] == pytest.approx(1.3768, abs=5e-5) and d["fit"]["seeds"] == design.FIT_SEEDS


def test_functions_identical_to_design_script():
    """flowshift's sur_ functions are the design script's: identical draws, components and log densities."""
    for v in ("6", "S", "5"):
        a = fs.sur_rows(MD, MC, 3000, 8025, v, 9025)
        b = design.rows(MD, MC, 3000, 8025, v, 9025)
        assert a.tobytes() == b.tobytes()
    a = fs.sur_sample(MD, 500, np.random.default_rng(1))
    assert a.tobytes() == design.sample(MD, 500, np.random.default_rng(1)).tobytes()
    md, mc = _small()
    for v in ("6", "S", "5"):
        x = fs.sur_rows(md, mc, 400, 2, v, 3)
        assert np.array_equal(fs.sur_logp(x, fs.sur_components(md, mc, v)), design.logp(x, design.components(md, mc, v)))
    assert fs.SUR_MNU == design.MNU


def test_mixture_density_against_direct_sum():
    from scipy.stats import multivariate_normal as mvn
    md, mc = _small()
    for v, ncomp in (("6", 4), ("S", 8), ("5", 4)):
        comps = fs.sur_components(md, mc, v)
        assert len(comps) == ncomp and abs(sum(c[0] for c in comps) - 1) < 1e-12
        x = fs.sur_rows(md, mc, 50, 4, v, 5)
        direct = np.log(sum(w * mvn(m, C).pdf(x) for w, m, C in comps))
        assert np.allclose(fs.sur_logp(x, comps, chunk=7), direct, atol=1e-10)
    # the committed surrogate: 64, 512 and 64 components
    assert [len(fs.sur_components(MD, MC, v)) for v in ("6", "S", "5")] == [64, 512, 64]


def test_ds_is_the_product_of_des_marginals():
    """DS = DES's Sigma m_nu marginal x its five-parameter marginal, convolved with the full CMB mixture: its
    marginal without Sigma m_nu is D5's, its Sigma m_nu marginal is D6's, and with one DES component it is D6."""
    from scipy.stats import multivariate_normal as mvn
    md, mc = _small()
    x5 = fs.sur_rows(md, mc, 40, 6, "5", 7)
    ds = fs.sur_components(md, mc, "S")
    keep = [j for j in range(6) if j != fs.SUR_MNU]
    marg = np.log(sum(w * mvn(m[keep], C[np.ix_(keep, keep)]).pdf(x5) for w, m, C in ds))
    assert np.allclose(marg, fs.sur_logp(x5, fs.sur_components(md, mc, "5")), atol=1e-10)
    u = np.linspace(-4, 4, 21)
    j = fs.SUR_MNU
    from scipy.stats import norm
    m_s = sum(w * norm(m[j], math.sqrt(C[j, j])).pdf(u) for w, m, C in ds)
    m_6 = sum(w * norm(m[j], math.sqrt(C[j, j])).pdf(u) for w, m, C in fs.sur_components(md, mc, "6"))
    assert np.allclose(m_s, m_6, atol=1e-12)
    one = {"w": [1.0], "mu": md["mu"][:1], "L": md["L"][:1]}
    x = fs.sur_rows(one, mc, 30, 8, "6", 9)
    c6, cs = fs.sur_components(one, mc, "6"), fs.sur_components(one, mc, "S")
    C = np.asarray(one["L"][0]) @ np.asarray(one["L"][0]).T
    rest = keep
    Cb = np.zeros_like(C)
    Cb[np.ix_(rest, rest)] = C[np.ix_(rest, rest)]
    Cb[j, j] = C[j, j]
    assert all(np.allclose(a[2] - b[2], C - Cb) for a, b in zip(c6, cs))      # only the DES cross terms differ


def test_ds_rows_have_the_product_distribution():
    """With one Gaussian component per chain the DS rows' covariance is blockdiag(Sigma_DES) + Sigma_CMB."""
    rng = np.random.default_rng(11)
    a = rng.normal(size=(6, 6))
    Cd = a @ a.T + np.eye(6)
    Cc = np.eye(6) * 0.3
    md = {"w": [1.0], "mu": [[0.0] * 6], "L": [np.linalg.cholesky(Cd).tolist()]}
    mc = {"w": [1.0], "mu": [[0.5] * 6], "L": [np.linalg.cholesky(Cc).tolist()]}
    x = fs.sur_rows(md, mc, 400_000, 1, "S", 2)
    j = fs.SUR_MNU
    expect = Cd.copy()
    expect[j, :] = 0
    expect[:, j] = 0
    expect[j, j] = Cd[j, j]
    expect += Cc
    assert np.allclose(np.cov(x.T), expect, atol=0.03 * np.diag(expect).max())
    off = np.delete(np.cov(x.T)[j], j)
    assert np.allclose(off, np.delete(Cc[j], j), atol=0.03 * np.diag(expect).max())   # DES cross terms gone
    x6 = fs.sur_rows(md, mc, 400_000, 1, "6", 2)
    xs = fs.sur_rows(md, mc, 400_000, 1, "S", 2)
    assert np.array_equal(np.delete(x6, j, axis=1), np.delete(xs, j, axis=1))           # the rest unchanged
    with pytest.raises(ValueError):
        fs.sur_rows(md, mc, 10, 1, "P", 2)


def test_exact_values_reproduce_the_registered_ones():
    """The formal computation (2,000,000 rows) reproduces the registered values bit for bit with the design
    output; here a 200,000-row version checks the code path and agrees within its Monte Carlo error."""
    e = ka2.exact_values(SUR, fs, n=200_000)
    assert abs(e["n6"] - EXACT["n6"]) < 0.01 and abs(e["S"] - EXACT["S"]) < 0.01 and abs(e["n5"] - EXACT["n5"]) < 0.01
    c = ka2.exact_check({"n6": 1.3768, "S": 0.6678, "n5": 0.3341, "phi": PHI_EXACT}, EXACT)
    assert c["ok"]
    assert not ka2.exact_check({"n6": 1.3768, "S": 0.6738, "n5": 0.3341, "phi": PHI_EXACT}, EXACT)["ok"]


def test_run_job_ka2(tmp_path, monkeypatch):
    cfg = json.loads(json.dumps(ka2.config(SEEDS, 3000, {"tol": 0.02}, SUR, [8000, 9000])))
    seen = {}

    def fake(diff, names, seed, est, pop_size=None, record_pop=False):
        seen.update(diff=diff, names=names, seed=seed, pop_size=pop_size, record_pop=record_pop)
        return {"seed": seed, "n_sigma": 1.0, "converged": True, "lower_bound": False}

    monkeypatch.setattr(fs, "one_shift", fake)
    scale = np.asarray(SUR["scale"])
    out = fs.run_job(["ka2", "S", "27"], str(tmp_path / "unused.npz"), cfg)
    assert out["variant"] == "S" and out["seed"] == 27 and seen["pop_size"] is None and seen["record_pop"]
    assert np.array_equal(seen["diff"], fs.sur_rows(MD, MC, 3000, 8027, "S", 9027) * scale)
    assert seen["names"] == SUR["columns"]
    fs.run_job(["ka2", "5", "27"], str(tmp_path / "unused.npz"), cfg)
    assert np.array_equal(seen["diff"], fs.sur_rows(MD, MC, 3000, 8027, "5") * np.delete(scale, fs.SUR_MNU))
    assert seen["names"] == ["a_s_1e9", "h0", "n_s", "omega_b", "omega_m"]
    fs.run_job(["ka2", "6", "27"], str(tmp_path / "unused.npz"), cfg)
    d6 = seen["diff"]
    assert np.array_equal(d6, fs.sur_rows(MD, MC, 3000, 8027, "6") * scale)
    # D6 = (DES block - CMB block) from default_rng(8000 + k), times the scale
    rng = np.random.default_rng(8027)
    a, c = fs.sur_sample(MD, 3000, rng), fs.sur_sample(MC, 3000, rng)
    assert np.allclose(d6, (a - c) * scale, rtol=0, atol=1e-12)
    bad = fs.run_job(["ka2", "Q", "27"], str(tmp_path / "unused.npz"), cfg)
    assert "error" in bad and bad["seed"] == 27


# ------------------------------------------------------------------ rules ----
def _reps(n6, ns, n5, seeds=SEEDS, bad=None):
    out = {}
    for v, vals in (("6", n6), ("S", ns), ("5", n5)):
        out[v] = [{"seed": k, "n_sigma": vals[i], "converged": True, "lower_bound": False, "train_s": 500.0}
                  for i, k in enumerate(seeds)]
    if bad:
        v, i, key, val = bad
        out[v][i][key] = val
    return out


def _vals(phi_shift=0.0, scatter=0.0):
    """n6 = 1.38, n5 = 0.33: phi_k = phi_exact + shift + scatter * (+-1 alternating)."""
    n6, n5 = [1.38] * 10, [0.33] * 10
    ns = [1.38 - (PHI_EXACT + phi_shift + scatter * (1 if i % 2 else -1)) * 1.05 for i in range(10)]
    return n6, ns, n5


def _lab(reps, flags=(True, True, True, True), seeds=SEEDS):
    return ka2.label(*flags, reps, seeds, PHI_EXACT, EMIN, SMAX)


def test_label_rule_order():
    good = _reps(*_vals())
    for i in range(4):
        flags = [True] * 4
        flags[i] = False
        assert _lab(good, tuple(flags))[0] == ka2.NE
    for bad in (("S", 3, "converged", False), ("5", 0, "lower_bound", True), ("6", 9, "n_sigma", float("nan"))):
        assert _lab(_reps(*_vals(), bad=bad))[0] == ka2.NE
    reps = _reps(*_vals())
    reps["5"] = reps["5"][:9]
    assert _lab(reps)[0] == ka2.NE
    reps = _reps(*_vals())
    reps["S"][2] = {"seed": 27, "error": "subprocess failed (RuntimeError)"}
    assert _lab(reps)[0] == ka2.NE
    lab, why, _ = _lab(_reps(*_vals()[:2], [1.2] * 10))
    assert lab == ka2.NE and "E_k" in why
    lab, why, _ = _lab(_reps(*_vals(scatter=0.4)))
    assert lab == ka2.NE and "s_b" in why
    assert _lab(_reps([1.38], [0.67], [0.33], seeds=[25]), seeds=[25])[0] == ka2.NE


def test_label_outcomes():
    lab, _, nums = _lab(_reps(*_vals(0.10, 0.02)))
    assert lab.startswith(ka2.OVER) and abs(nums["b_bar"] - 0.10) < 1e-9
    assert abs(nums["half_width"] - 2 * nums["s_b"] / math.sqrt(10)) < 1e-15
    assert nums["t_quantile"] == pytest.approx(2.2622, abs=1e-4)
    assert nums["interval_b_t"][1] - nums["b_bar"] == pytest.approx(nums["t_quantile"] * nums["s_b"] / math.sqrt(10))
    assert _lab(_reps(*_vals(-0.10, 0.02)))[0].startswith(ka2.UNDER)
    lab, _, nums = _lab(_reps(*_vals(0.01, 0.10)))
    assert lab.startswith(ka2.NONE) and lab.endswith(f"[{nums['interval_b'][0]:.3f}, {nums['interval_b'][1]:.3f}])")


def test_qualifier_order():
    q = ka2.qualifier(0.671, 0.037, 5, -0.05, 0.03, 10, BAND)
    assert q["qualifier"] == ka2.Q_HOLDS and abs(q["w"] - 2 * math.sqrt(0.037 ** 2 / 5 + 0.03 ** 2 / 10)) < 1e-15
    q = ka2.qualifier(0.671, 0.037, 5, 0.40, 0.12, 10, BAND)
    assert q["qualifier"] == ka2.Q_REVERSES and 0.671 - q["w"] < 0.60
    assert ka2.qualifier(0.671, 0.037, 5, -0.20, 0.12, 10, BAND)["qualifier"] == ka2.Q_HOLDS
    assert ka2.qualifier(0.671, 0.037, 5, 0.0, 0.12, 10, BAND)["qualifier"].startswith(ka2.Q_NOISY[:-1] + ": w = ")
    q = ka2.qualifier(0.671, 0.037, 5, 0.06, 0.03, 10, BAND)
    assert q["qualifier"] == ka2.Q_UNDECIDED and 0.671 - q["w"] >= 0.60


def test_comparison():
    rk = {"ok": True, "b_bar": 0.0197, "s_b": 0.040, "n": 10}
    c = ka2.comparison(0.03, 0.05, 10, rk)
    sig = math.sqrt(0.05 ** 2 / 10 + 0.04 ** 2 / 10)
    assert c["reading"].startswith(ka2.C_NONE) and abs(c["sigma"] - sig) < 1e-15 and abs(c["delta_b"] - 0.0103) < 1e-12
    assert ka2.comparison(0.0197 + 2.01 * sig, 0.05, 10, rk)["reading"].startswith(ka2.C_DIFF)
    assert ka2.comparison(0.0197 - 2.01 * sig, 0.05, 10, rk)["reading"].startswith(ka2.C_DIFF)
    assert ka2.comparison(0.03, 0.05, 10, {"ok": False, "reason": "x"})["reading"] == ka2.NE


# ------------------------------------------------------------------ records, plan, assembly ----
def _shuf_file(tmp_path, phis=(0.68, 0.64, 0.71, 0.69, 0.63)):
    import r6shuf
    d = {"label": r6shuf.CORR,
         "quantities": {"phi": {"values": list(phis), "mean": float(np.mean(phis)), "s": float(np.std(phis, ddof=1))}},
         "flows": {"versions": {"tensorflow": "2.21.0"}, "settings": {"pop_size": 10}}}
    p = tmp_path / "r6_shuf.json"
    p.write_text(json.dumps(d), encoding="utf-8")
    return p


def _ka_file(tmp_path, label=None, b=0.0197, s=0.040):
    d = {"label": label or ka2.KA_LABEL, "numbers": {"b_bar": b, "s_b": s}, "settings": {"r6_ka_seeds": list(range(15, 25))},
         "flows": {"versions": {"tensorflow": "2.21.0"}, "settings": {"pop_size": 10}},
         "offsets": {"6": {"mean": -0.073}, "S": {"mean": -0.116}, "5": {"mean": -0.098}}}
    p = tmp_path / "r6_ka.json"
    p.write_text(json.dumps(d), encoding="utf-8")
    return p


def test_check_ka(tmp_path):
    r = ka2.check_ka(_ka_file(tmp_path))
    assert r["ok"] and r["n"] == 10 and r["b_bar"] == 0.0197 and r["offsets"]["S"] == -0.116
    assert not ka2.check_ka(tmp_path / "missing.json")["ok"]
    assert not ka2.check_ka(_ka_file(tmp_path, label="flows overestimate φ (bias +0.050)"))["ok"]
    rec = HERE / "results" / "r6_ka.json"
    if rec.exists():                                                      # the recorded file passes
        r = ka2.check_ka(rec)
        assert r["ok"] and r["b_bar"] == pytest.approx(0.019736336171276514, abs=1e-15) and r["n"] == 10


ENV = {"versions": {"tensorflow": "2.21.0"}, "settings": {"pop_size": 10}}


def _job(calls, vals=None, env=None, crash=()):
    vals = vals or {}

    def job(*parts):
        calls.append(parts)
        if parts in crash:
            raise OSError("job failed")
        if parts[0] == "meta":
            return copy.deepcopy(env or ENV)
        v, k = parts[1], parts[2]
        return {"seed": k, "n_sigma": vals.get(v, {}).get(k, {"6": 1.38, "S": 0.68, "5": 0.33}[v]),
                "converged": True, "lower_bound": False, "variant": v, "train_s": 600.0}
    return job


def _cfg():
    return ka2.config(SEEDS, 10, {"tol": 0.02}, SUR, [8000, 9000])


def test_plan_order_and_env_mismatch():
    calls = []
    res = ka2.plan(_job(calls), _cfg(), lambda m: None, fs, expected=({**ENV, "ok": True}, {**ENV, "ok": True}))
    assert calls[0] == ("meta",) and calls[1:] == [("ka2", v, k) for k in SEEDS for v in ("6", "S", "5")]
    calls = []
    res = ka2.plan(_job(calls, env={"versions": {"tensorflow": "2.20"}, "settings": {"pop_size": 10}}), _cfg(),
                   lambda m: None, fs, expected=({**ENV, "ok": True}, {**ENV, "ok": True}))
    assert calls == [("meta",)] and "status_runs" in res
    calls = []
    res = ka2.plan(_job(calls, crash={("ka2", "S", 27)}), _cfg(), lambda m: None, fs)
    assert res["S"][2]["seed"] == 27 and "error" in res["S"][2] and len(calls) == 31   # any exception is recorded


def _recs(tmp_path):
    sys.path.insert(0, str(HERE))
    try:
        return ka2.check_shuf(_shuf_file(tmp_path)), ka2.check_ka(_ka_file(tmp_path))
    finally:
        sys.path.remove(str(HERE))


def test_assemble(tmp_path):
    recs, rk = _recs(tmp_path)
    rec6 = {"ok": True, **ENV}
    exact = {**EXACT, "phi": PHI_EXACT}
    res = ka2.plan(_job([]), _cfg(), lambda m: None, fs)
    out = ka2.assemble(res, rec6, recs, rk, SUR, exact, EXACT, SEEDS, EMIN, SMAX, BAND, {"r6_ka2": True})
    b = (1.38 - 0.68) / (1.38 - 0.33) - PHI_EXACT
    assert out["label"].startswith(ka2.UNDER if b < 0 else ka2.OVER) and abs(out["numbers"]["b_bar"] - b) < 1e-12
    assert out["summary"]["qualifier"] == out["qualifier"]["qualifier"]
    assert out["summary"]["comparison"] == out["comparison"]["reading"]
    assert out["environment"]["equal_r6_ka"] is True and out["offsets_ka"]["S"] == -0.116
    assert abs(out["offsets"]["S"]["mean"] - (0.68 - 0.6678)) < 1e-12 and out["times_s"]["6"] == [600.0] * 10
    # rule 1: missing r6_ka.json only makes the comparison not evaluable
    out1 = ka2.assemble(res, rec6, recs, {"ok": False, "reason": "results/r6_ka.json missing"}, SUR, exact, EXACT,
                        SEEDS, EMIN, SMAX, BAND, {})
    assert out1["label"] == out["label"] and out1["comparison"]["reading"] == ka2.NE
    out2 = ka2.assemble({"status": "not run (x)"}, rec6, recs, rk, SUR, exact, EXACT, SEEDS, EMIN, SMAX, BAND, {})
    assert out2["label"] == ka2.NE and "qualifier" not in out2 and "comparison" not in out2
    out3 = ka2.assemble(res, rec6, recs, rk, SUR, dict(exact, S=0.68), EXACT, SEEDS, EMIN, SMAX, BAND, {})
    assert out3["label"] == ka2.NE and "exact" in out3["reason"]
    out4 = ka2.assemble(res, rec6, recs, rk, {"ok": False, "reason": "hash"}, exact, EXACT, SEEDS, EMIN, SMAX, BAND, {})
    assert out4["label"] == ka2.NE and "surrogate" in out4["reason"]
    res_bad = ka2.plan(_job([], env={"versions": {"tensorflow": "2.20"}, "settings": {"pop_size": 10}}), _cfg(),
                       lambda m: None, fs)
    out5 = ka2.assemble(res_bad, rec6, recs, rk, SUR, exact, EXACT, SEEDS, EMIN, SMAX, BAND, {})
    assert out5["label"] == ka2.NE and "versions" in out5["reason"]
    assert len(json.dumps(out)) < 100_000                                  # results file far below 1 MB


def test_conclusion_check_on_assembled_output(tmp_path):
    """test_conclusions.check_r6_ka2 accepts an assembled record and rejects changed readings."""
    recs, rk = _recs(tmp_path)
    sys.path.insert(0, str(HERE))
    try:
        tc = _import("test_conclusions")
    finally:
        sys.path.remove(str(HERE))
    exact = {**EXACT, "phi": PHI_EXACT}
    vals = {"S": {k: 0.68 + 0.02 * ((k % 3) - 1) for k in SEEDS}}
    res = ka2.plan(_job([], vals=vals), _cfg(), lambda m: None, fs)
    out = json.loads(json.dumps(ka2.assemble(res, {"ok": True, **ENV}, recs, rk, SUR, exact, EXACT, SEEDS, EMIN, SMAX,
                                             BAND, {})))
    tc.check_r6_ka2(out)
    bad = copy.deepcopy(out)
    bad["qualifier"]["qualifier"] = ka2.Q_UNDECIDED if out["qualifier"]["qualifier"] != ka2.Q_UNDECIDED else ka2.Q_HOLDS
    with pytest.raises(AssertionError):
        tc.check_r6_ka2(bad)
    bad = copy.deepcopy(out)
    bad["comparison"]["reading"] = ka2.C_DIFF + " (Δb = +0.000)"
    with pytest.raises(AssertionError):
        tc.check_r6_ka2(bad)


def test_run_params_and_paths():
    src = (HERE / "run.py").read_text(encoding="utf-8")
    assert 'ctx.study.results_dir / "r6_ka.json"' in src and 'ctx.study.results_dir / "r6_ka2.json"' in src
    tree = ast.parse(src)
    saves = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and ast.unparse(n.func) == "ctx.save"
             and n.args and ast.unparse(n.args[0]) == "'r6_ka2'"]
    assert len(saves) == 1
    sys.path.insert(0, str(HERE))
    try:
        run = _import("run")
    finally:
        sys.path.remove(str(HERE))
    P = run.PARAMS
    assert P["r6_ka2"] is False and P["r6_ka"] is False and P["r6_ka2_seeds"] == SEEDS
    assert P["r6_ka2_exact"] == EXACT and P["r6_ka2_seed_offsets"] == [8000, 9000] and P["r6_ka2_sha256"] == SHA
    assert P["r6_ka2_file"] == "surrogate_t063.json"
    used_tf = set(range(0, 5)) | {10, 11, 12} | set(range(15, 25))
    assert not used_tf & set(SEEDS)
    used_rng = ({k + o for k in range(5) for o in (0, 1000, 2000, 3000)} | {1010, 1011, 1012, 999, 1000, 7000, 7001}
                | {o + k for k in range(15, 25) for o in (5000, 6000)})
    assert not used_rng & {o + k for k in SEEDS for o in (8000, 9000)}


def test_draws_identical_under_the_tf_environment(tmp_path):
    """README 2.10: the TF environment's numpy gives bit-identical generator streams and the same mapped rows
    (within 1e-12) as the project's (skipped when venv-tf is absent)."""
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
            "c = json.loads(open(sys.argv[2], encoding='utf-8').read()); "
            "r = np.random.default_rng(8025); u = r.random(1000); z = r.standard_normal((1000, 6)); "
            "p = np.random.default_rng(9025).permutation(2000); "
            "rows = [fs.sur_train_rows(c, 2000, v, 25) for v in ('6', 'S', '5')]; "
            "np.savez(sys.argv[3], u=u, z=z, p=p, r6=rows[0], rS=rows[1], r5=rows[2])")
    cfgp = tmp_path / "cfg.json"
    cfgp.write_text(json.dumps(_cfg()["ka2"]), encoding="utf-8")
    out = tmp_path / "tf.npz"
    subprocess.run([str(exe), "-I", "-c", code, str(HERE), str(cfgp), str(out)], check=True, timeout=300)
    d = np.load(out)
    r = np.random.default_rng(8025)
    assert d["u"].tobytes() == r.random(1000).tobytes() and d["z"].tobytes() == r.standard_normal((1000, 6)).tobytes()
    assert np.array_equal(d["p"], np.random.default_rng(9025).permutation(2000))
    for v in ("6", "S", "5"):
        assert np.allclose(d["r" + v], fs.sur_train_rows(_cfg()["ka2"], 2000, v, 25), rtol=0, atol=1e-12)
