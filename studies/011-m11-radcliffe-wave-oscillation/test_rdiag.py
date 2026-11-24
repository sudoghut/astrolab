"""Code checks of README 4.11 (R-DIAG, T-061) before the run: synthetic data only, except the sample counts on
the real tables (read from the astrolab cache; skipped when they are not cached, never downloaded)."""
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

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
F = _import("fit011")
D = _import("diag011")
run = _import("run")


def _syn_data(n_cl=125, n_co=79, seed=11):
    """As test_wave._syn_data: synthetic clusters (K24 column (6)) and clouds (K24 column-(3) curve)."""
    g = W.Grid()
    d = F.synthetic_clusters(g, n_cl, np.random.default_rng(seed))
    wv = W.wave_on_grid(W.k24_vector(3), g)
    vi = np.flatnonzero(wv["valid"])
    r = np.random.default_rng(seed + 1)
    k = r.choice(vi[150:1500], n_co)
    return g, W.Data(d.cx, d.cy, d.cz, d.cvz, d.csig, wv["x"][k] + r.normal(0, 47, n_co),
                     wv["y"][k] + r.normal(0, 47, n_co), wv["z"][k] + r.normal(0, 47, n_co))


def _c_setup(P, cref=False):
    base = run.setups(P)["col3"]
    uni = {"s_origin": tuple(P["rdiag_c_prior_pc"])}
    if cref:
        uni["s0"] = tuple(P["rdiag_cref_s0_prior_pc"])
    return run.replace(base, free=W.SHAPE_NAMES + ("s_origin",), uniform=uni,
                       scales={"s_origin": P["rdiag_c_scale_pc"]})


# ---------------------------------------------------------------------------------------------
# the origin shift

def test_c_zero_and_no_z_change_reproduce_the_formal_likelihood_to_the_bit():
    """-834.095003579991: the formal column-(3) value on these synthetic clouds (commit e15b38f)."""
    g, d = _syn_data()
    wc, wo = W.fixed_weights(d, g, 100.0)
    P = dict(run.PARAMS)
    formal = W.Model(W.Setup(free=W.SHAPE_NAMES, clusters=False, clouds=True), d, g, wc, wo)
    v = W.k24_vector(3)
    assert formal.loglike(formal.theta_of(v)) == -834.095003579991
    mc = W.Model(_c_setup(P), d, g, None, wo)
    assert v[W.IDX["s_origin"]] == 0.0 and mc.theta_of(v)[-1] == 0.0
    assert mc.loglike(mc.theta_of(v)) == -834.095003579991
    assert W.Model(run.replace(run.setups(P)["col3"], s_origin=0.0), d, g, None, wo).loglike(formal.theta_of(v)) \
        == -834.095003579991
    a, b = W.wave_on_grid(v, g), W.wave_on_grid(mc.full(mc.theta_of(v)), g)
    for k in ("x", "y", "z", "vz", "s", "zeta", "valid", "Lambda", "omega"):
        assert np.array_equal(a[k], b[k], equal_nan=k != "valid")
    # the Part D models on the 79 rows: (c) and c-ref at c = 0 equal the formal value; z_sun shifts z only
    dm = run.diag_models_d(P, d, g, wo)
    assert dm["c"].loglike(dm["c"].theta_of(v)) == -834.095003579991
    assert np.array_equal(dm["zsun"].data.oz, d.oz + 20.8) and np.array_equal(dm["zsun"].data.ox, d.ox)
    assert dm["cref"].setup.uniform["s0"] == (-1000.0, 3000.0)
    # physical() keeps the keys written before README 4.11
    assert "s_origin" not in W.physical(v) and W.NAMES[-1] == "s_origin" and len(W.NAMES) == 18


def test_shifted_zeta_with_s0_minus_c_reproduces_the_formal_zeta():
    g = W.Grid()
    v = W.k24_vector(3)
    a = W.wave_on_grid(v, g)
    for c in (-250.0, -37.5, 120.0, 390.0):
        v2 = v.copy()
        v2[W.IDX["s_origin"]] = c
        v2[W.IDX["s0"]] = v[W.IDX["s0"]] - c
        b = W.wave_on_grid(v2, g)
        assert np.allclose(b["zeta"], a["zeta"], rtol=1e-12, atol=1e-9)
        assert np.array_equal(b["s"], a["s"])                       # s itself is not shifted
        sm = a["s"] - c
        p, gam = v[W.IDX["p"]], math.exp(v[W.IDX["ln_gamma"]])
        assert np.array_equal(b["valid"], p - gam * sm > 0)           # validity uses s' = s - c
        lam = np.where(b["valid"], sm / (p - gam * sm), np.nan)
        assert np.allclose(b["Lambda"], lam, equal_nan=True, rtol=1e-13)
        assert not np.allclose(b["Lambda"][b["valid"] & a["valid"]], a["Lambda"][b["valid"] & a["valid"]])


def test_origin_prior_scales_and_flat_s0():
    g, d = _syn_data(n_cl=5, n_co=30)
    P = dict(run.PARAMS)
    m = W.Model(_c_setup(P), d, g)
    f = W.Model(run.setups(P)["col3"], d, g)
    th = m.theta_of(W.k24_vector(3))
    lp0 = f.logprior(f.theta_of(W.k24_vector(3)))
    for c, ok in ((-400.0, True), (399.9, True), (400.0, True), (-400.01, False), (401.0, False)):
        th[-1] = c
        assert (m.logprior(th) == lp0) if ok else (m.logprior(th) == -np.inf)
    assert m.scales()[-1] == 100.0 and np.array_equal(m.scales()[:-1], f.scales())
    draws = np.array([m.prior_draw(np.random.default_rng(i))[-1] for i in range(200)])
    assert draws.min() >= -400 and draws.max() <= 400 and draws.std() > 150
    # walkers: ball 0.05 x 100 pc around c = 0
    w = F.init_walkers(m, W.k24_vector(3), 48, np.random.default_rng(1))
    assert abs(w[:, -1].mean()) < 3 and 3 < w[:, -1].std() < 7
    # c-ref: s0 flat in U(-1000, 3000), its walker scale still the prior sigma (200 pc)
    r = W.Model(_c_setup(P, cref=True), d, g)
    t = r.theta_of(W.k24_vector(3))
    i = r.setup.free.index("s0")
    vals = []
    for s0 in (-1000.0, 0.0, 680.0, 2999.0):
        t[i] = s0
        vals.append(r.logprior(t))
    assert len(set(vals)) == 1 and np.isfinite(vals[0])
    t[i] = 3000.5
    assert r.logprior(t) == -np.inf
    assert r.scales()[i] == 200.0
    with pytest.raises(ValueError):
        W.Model(W.Setup(free=W.SHAPE_NAMES + ("s_origin",), clusters=False, clouds=True), d, g)
    with pytest.raises(ValueError):
        W.Model(W.Setup(free=W.SHAPE_NAMES + ("s_origin",), clusters=False, clouds=True,
                        uniform={"s_origin": (-400, 400)}), d, g)


# ---------------------------------------------------------------------------------------------
# Part A

def test_object_terms_sum_to_minus_lnl_minus_the_constant():
    g, d = _syn_data()
    _, wo = W.fixed_weights(d, g, 100.0)
    m = W.Model(W.Setup(free=W.SHAPE_NAMES, clusters=False, clouds=True), d, g, None, wo)
    for v in (W.k24_vector(3), W.k24_vector(6)):
        tm = D.object_terms(m, v)
        assert tm["t"].sum() == pytest.approx(-tm["lnL"] - tm["constant"], rel=1e-12)
        assert tm["constant"] == pytest.approx(wo.sum() * math.log(2 * math.pi * 47.0 ** 2), rel=1e-12)
        assert np.all(tm["t"] >= 0) and len(tm["s"]) == d.n_clouds


def test_top_contributors():
    names = [f"o{i}" for i in range(12)]
    delta = np.array([5.0, -1.0, 3.0, 0.5, 0, 0, 0, 0, 0, 0, 0, 1.5])
    named = np.array([True] * 6 + [False] * 6)
    r = D.top_contributors(names, delta, named, n=2)
    assert [t["name"] for t in r["top"]] == ["o0", "o2"]
    assert r["share_of_positive_sum"] == pytest.approx(8.0 / 10.0)
    assert r["sum_named"] == pytest.approx(7.5) and r["sum_bridges"] == pytest.approx(1.5)


def test_part_a_starts_and_terms(monkeypatch):
    """21 starts: v_K, v_P, then 19 prior draws from rng_for(seed, 'ml_rdiag_map'); log posterior objective."""
    g, d = _syn_data()
    _, wo = W.fixed_weights(d, g, 100.0)
    P = dict(run.PARAMS)
    m = W.Model(run.setups(P)["col3"], d, g, None, wo)
    seen = []

    def fake(model, st, *, nm_maxfev, lbfgs_maxfun, objective="like", bounds=None):
        seen.append((np.array(st), objective))
        return {"theta": np.array(st), "value": model.logpost(st), "n_eval": 1}

    monkeypatch.setattr(run.F, "optimise", fake)
    vP = W.k24_vector(3, A=200.0)

    class Ctx:
        log = staticmethod(lambda m: None)

    names = [f"c{i}" for i in range(d.n_clouds)]
    named = np.arange(d.n_clouds) < 25
    out = run.diag_part_a(P, F.NullStore(), m, vP, names, named, Ctx())
    assert len(seen) == 21 and all(o == "post" for _, o in seen)
    assert np.array_equal(seen[0][0], m.theta_of(W.k24_vector(3))) and np.array_equal(seen[1][0], m.theta_of(vP))
    rng = run.rng_for(P["seed"], "ml_rdiag_map")
    for st, _ in seen[2:]:
        assert np.array_equal(st, m.prior_draw(rng))
    best = max(seen, key=lambda s: m.logpost(s[0]))[0]
    assert out["vectors"]["M"]["ln_posterior"] == pytest.approx(m.logpost(best))
    for k in ("K", "P", "M"):
        a = out["vectors"][k]
        assert a["sum_terms"] == pytest.approx(-a["lnL"] - a["constant"], rel=1e-12)
    tK = np.array([o["t_K"] for o in out["objects"]])
    tP = np.array([o["t_P"] for o in out["objects"]])
    assert out["comparisons"]["K_minus_P"]["sum_all"] == pytest.approx(float((tK - tP).sum()))
    assert len(out["comparisons"]["K_minus_M"]["top"]) == 10


# ---------------------------------------------------------------------------------------------
# Part B: the membership rule

def _rows(spec):
    return [{"name": n, "p": p, "sig": s} for n, p, s in spec]


def _sl(spec):
    return {"name": [n for n, *_ in spec], "x": [x for _, x, _, _ in spec], "y": [y for _, _, y, _ in spec],
            "z": [z for *_, z in spec]}


NMAP = {"A": "X", "B": "X", "C": "X", "F": "Y", "G": "Z"}


def test_membership_rule_on_synthetic_rows():
    rows = _rows([("A", (0, 0, 0), (20, 20, 20)), ("B", (50, 0, 0), (10, 10, 10)), ("C", (3, 0, 0), (0, 0, 0)),
                  ("F", (500, 0, 0), (10, 10, 10)), ("G", (0, 0, 0), (0, 0, 0))])
    sl = _sl([("X", 2, 0, 0), ("X", 20, 0, 0), ("X", 30, 0, 0), ("X", 25, 0, 0), ("X", 52, 0, 0),
              ("Y", 0, 0, 0), ("Z", 12, 0, 0), ("Z", 10, 0, 0), ("Perseus", 9, 9, 9)])
    m = {r["name"]: r for r in D.membership(rows, sl, k=3.0, floor=5.0, name_map=NMAP)}
    # sightlines 1-3 are candidates of A and B and go to the smaller max |dx|/t (A: 20/60, 30/60, 25/60 vs B:
    # 30/30, 20/30, 25/30); sightline 0 is a candidate of A (2/60) and C (1/15) and goes to A
    assert m["A"]["candidates"] == [0, 1, 2, 3, 4] and m["A"]["kept"] == [0, 1, 2, 3]
    assert m["A"]["status"] == "pass"                       # mean x 19.25 <= max(20, 5)
    assert m["B"]["candidates"] == [1, 2, 3, 4] and m["B"]["kept"] == [4] and m["B"]["status"] == "pass"
    assert m["C"]["candidates"] == [0] and m["C"]["status"] == "absorbed" and m["C"]["absorbed_by"] == ["A"]
    assert m["F"]["status"] == "fallback" and m["F"]["reason"] == "no candidates"
    assert m["G"]["kept"] == [6, 7] and m["G"]["status"] == "fallback"     # mean 11 > max(0, 5)
    sam = D.build_samples(rows, sl, _sl([("Bridge_1", 1, 1, 1), ("Bridge_2", 2, 2, 2)]),
                          [m[r["name"]] for r in rows], pt_names=("Perseus",), name_map=NMAP)
    assert len(sam["S"]["x"]) == 4 + 1 + 1 + 1 + 2          # A's 4, B's 1, F and G as their own points, 2 bridges
    assert sam["S"]["source"].count("12co") == 2 and sam["S"]["row"][:5] == ["A"] * 4 + ["B"]
    assert len(sam["S_all"]["x"]) == 5 + 1 + 2 + 2 and len(sam["S+PT"]["x"]) == len(sam["S"]["x"]) + 1
    tab = {r["name"]: r for r in D.consistency_table([m[r["name"]] for r in rows], sl,
                                                     w_s=np.ones(9), s_rows=sam["S"]["row"],
                                                     w79={r["name"]: 1.0 for r in rows})}
    assert tab["A"]["mean_minus_p"][0] == pytest.approx(19.25) and tab["G"]["sd_over_spread"] == [None] * 3
    assert tab["A"]["sd_over_spread"][0] == pytest.approx(np.std([2, 20, 30, 25]) / 20)
    assert tab["A"]["summed_weight_in_S"] == 4.0 and tab["C"]["summed_weight_in_S"] == 0.0
    assert tab["G"]["summed_weight_in_S"] == 1.0 and tab["F"]["n_candidates"] == 0


def test_membership_exact_ties_go_to_the_row_listed_first():
    sl = _sl([("X", 10, 0, 0)])
    for order in (("A", "B"), ("B", "A")):
        pos = {"A": (0, 0, 0), "B": (20, 0, 0)}
        rows = _rows([(n, pos[n], (10, 10, 10)) for n in order])
        m = D.membership(rows, sl, name_map=NMAP)
        assert m[0]["kept"] == [0] and m[1]["status"] == "absorbed" and m[1]["absorbed_by"] == [order[0]]


def _cached_ctx():
    from astrolab import cache

    class Ctx:
        def http(self, url, label=None):
            e = cache.get(cache.key_for("http", {"url": url}), ".bin")
            if e is None:
                pytest.skip(f"{url} not in the astrolab cache (this test never downloads)")
            return e.payload

        def log(self, m):
            pass
    return Ctx()


def test_samples_on_the_real_tables():
    ctx = _cached_ctx()
    P = dict(run.PARAMS)
    _, co, _ = run.load_tables(ctx)
    tabs = run.load_diag_tables(ctx)
    assert tabs["rows"] == {"zucker": 326, "bridging": 54, "curve": 1500}
    inp = run.diag_inputs(P, co, tabs, ctx)
    assert inp["n_points"] == {"S": 149, "S_all": 169, "S+PT": 177}
    assert inp["n_kept_sightlines"] == 95 and inp["fallback_rows"] == []
    assert inp["absorbed_rows"] == {"NorthAmericaNebula": ["NorthAmerica"]}
    assert inp["n_named_rows"] == 25 and inp["bridge_rows_max_abs_diff_pc"] <= 1.0
    with pytest.raises(RuntimeError):
        run.diag_inputs(dict(P, rdiag_s_all_n=170), co, tabs, ctx)
    with pytest.raises(RuntimeError):
        run.diag_inputs(dict(P, rdiag_pt_n=27), co, tabs, ctx)


# ---------------------------------------------------------------------------------------------
# Part C

def _line(n=501):
    x = np.linspace(0.0, 1000.0, n)
    return {"x": x, "y": np.zeros(n), "z": np.zeros(n), "vz": np.zeros(n), "s": x.copy()}


def test_curve_distance_zero_known_displacement_and_grid_ends():
    cur = _line()
    own = np.column_stack([cur["x"], cur["y"], cur["z"], cur["vz"]])
    c = D.curve_compare(cur, own)
    assert np.all(c["d_xy"] == 0) and np.all(c["d_3d"] == 0) and np.all(c["dvz"] == 0)
    assert np.flatnonzero(c["end_xy"]).tolist() == [0, 500] == np.flatnonzero(c["end_3d"]).tolist()
    pub = np.array([[300.0, 5.0, 7.0, 2.0], [700.0, -3.0, 4.0, -1.0], [-50.0, 0, 0, 0], [1100.0, 1.0, 0, 0]])
    c = D.curve_compare(cur, pub)
    assert c["d_xy"][:2] == pytest.approx([5.0, 3.0]) and c["d_3d"][:2] == pytest.approx([math.sqrt(74), 5.0])
    assert c["dvz"][:2] == pytest.approx([2.0, 1.0]) and c["s_xy"][:2] == pytest.approx([300.0, 700.0])
    assert c["end_xy"].tolist() == [False, False, True, True] == c["end_3d"].tolist()
    s = D.curve_summary(c)
    assert s["n_excluded_xy"] == 2 and s["xy"]["median"] == pytest.approx(4.0)
    assert s["label"] == "matches K24's published curve (more than 10% of the points lie beyond our curve's ends)"
    # our model curve against itself
    wv = W.wave_on_grid(W.k24_vector(6), W.Grid())
    cur = D.valid_curve(wv)
    c = D.curve_compare(cur, np.column_stack([cur["x"], cur["y"], cur["z"], cur["vz"]])[5:-5])
    assert np.all(c["d_3d"] == 0) and not c["end_xy"].any() and not c["end_3d"].any()


def test_curve_label_edges():
    assert D.curve_label(5.0, 15.0, 0, 1500) == "matches K24's published curve"
    assert D.curve_label(5.0, 15.1, 0, 1500) == "approximately matches"
    assert D.curve_label(20.0, 99.0, 150, 1500) == "approximately matches"
    assert D.curve_label(20.01, 30.0, 151, 1500) == ("differs from K24's published curve (more than 10% of the "
                                                     "points lie beyond our curve's ends)")


def test_least_squares_recovers_a_synthetic_vector_with_c():
    g = W.Grid(400)
    truth = W.k24_vector(6, s_origin=60.0)
    truth[W.IDX["x1"]] += 15.0
    truth[W.IDX["s0"]] += 40.0
    truth[W.IDX["A"]] += 10.0
    cur = D.valid_curve(W.wave_on_grid(truth, g))
    n = len(cur["x"])
    k = np.arange(int(0.05 * n), int(0.95 * n), 2)
    pts = np.column_stack([cur["x"], cur["y"], cur["z"]])[k]
    m = D.lsq_model(g, W.k24_vector(6), c_bounds=(-400.0, 400.0), c_scale=100.0)
    assert m.scales()[-1] == 100.0 and m.base[W.IDX["B"]] == 1.0 and m.base[W.IDX["w0t"]] == 0.0
    r = D.curve_lsq(m, pts, nm_maxfev=6000, lbfgs_maxfun=3000)
    assert r["rms_start_pc"] > 5.0 and r["rms_pc"] < 1.0
    assert -400.0 <= r["vector"][W.IDX["s_origin"]] <= 400.0


# ---------------------------------------------------------------------------------------------
# labels and the reading

def test_d6_m6_and_fit_status():
    diffs = {"A": -1.0, "p": 2.0, "delta": -0.5, "s0": 0.1, "gamma": 0.2, "phi": 3.5, "x0": 99.0}
    d6, m6, name = D.d6_m6(diffs)
    assert d6 == pytest.approx(7.3) and m6 == 3.5 and name == "phi"
    assert D.fit_status(5, 1.0) == ("reproduced", None)
    assert D.fit_status(6, 2 / 3) == ("reproduced", None) and D.fit_status(5, 1.5)[0] == "reproduced"
    assert D.fit_status(5, 1.51) == ("partly reproduced", "width ratio 1.510 outside [2/3, 3/2]")
    assert D.fit_status(3, 1.0) == ("partly reproduced", "count 3 of 6 (3-4)")
    assert D.fit_status(4, 0.5)[0] == "partly reproduced"
    assert D.fit_status(2, 1.0) == ("not reproduced", None)
    assert D.fit_label("partly reproduced", "with sample S") == "column (3) partly reproduced with sample S, post hoc"


def test_c_reading_and_reading_rule():
    assert D.c_reading(100.0) == "data-driven" and D.c_reading(100.01) == "prior-dominated"
    kw = dict(d6_max=8.781, m6_max=3.192)
    fit = lambda st, d6=5.0, m6=2.0: {"status": st, "D6": d6, "M6": m6}
    nr = fit("not reproduced", 12.0, 4.0)
    assert D.reading(fit("reproduced", 20.0, 9.0), nr, nr, "data-driven", **kw)["reading"] == D.READING_S2
    assert D.reading(fit("partly reproduced", 8.781, 3.192), nr, nr, "data-driven", **kw)["reading"] == D.READING_S1
    # S partly reproduced but D6 or M6 above the threshold: go on to Part D
    s_far = fit("partly reproduced", 8.79, 3.0)
    assert D.reading(s_far, nr, nr, "data-driven", **kw)["reading"] == D.READING_NONE
    assert D.reading(fit("partly reproduced", 8.0, 3.2), nr, nr, "data-driven", **kw)["reading"] == D.READING_NONE
    r = D.reading(s_far, fit("reproduced"), fit("partly reproduced"), "data-driven", **kw)
    assert r["reading"] == D.READING_D2 + " (variant: the origin of s free)"
    r = D.reading(s_far, fit("reproduced"), fit("partly reproduced"), "prior-dominated", **kw)
    assert r["reading"] == D.READING_D1 + " (variant: z☉ = 20.8 pc)"           # (c) counts only if data-driven
    r = D.reading(s_far, fit("partly reproduced"), fit("partly reproduced"), "data-driven", **kw)
    assert r["reading"] == D.READING_D1 + " (variants: the origin of s free and z☉ = 20.8 pc)"
    r = D.reading(nr, fit("reproduced"), fit("reproduced"), "data-driven", **kw)
    assert r["reading"] == D.READING_D2 + " (variants: the origin of s free and z☉ = 20.8 pc)"
    assert D.reading(nr, fit("partly reproduced", 9.0), nr, "data-driven", **kw)["reading"] == D.READING_NONE


def test_formal_reference_from_rconv(tmp_path):
    P = dict(run.PARAMS)
    with pytest.raises(RuntimeError):
        run.diag_formal_reference(P, tmp_path / "rconv.json")
    k = W.K24_TABLE2[3]
    par = {n: {"median": k[n][0] + 1.0} for n in ("x0", "y0", "x1", "y1", "x2", "y2", "A", "p", "s0", "phi",
                                                   "delta", "gamma")}
    diffs = {"A": -1.40, "p": -1.41, "delta": -2.11, "s0": 0.22, "gamma": -0.98, "phi": 3.73, "x0": -1.5}
    (tmp_path / "rconv.json").write_text(json.dumps({"conventions": [
        {"index": 0, "name": "L-F-W", "count": 2, "width_ratio": 1.18, "sigma_scaled_differences": diffs,
         "parameters": par}]}), encoding="utf-8")
    fr = run.diag_formal_reference(P, tmp_path / "rconv.json")
    assert fr["count"] == 2 and fr["D6"] == pytest.approx(9.85) and fr["M6"] == 3.73 and fr["M6_parameter"] == "phi"
    v = fr["v_P"]
    assert v[W.IDX["A"]] == k["A"][0] + 1 and v[W.IDX["ln_delta"]] == pytest.approx(math.log(k["delta"][0] + 1))
    assert v[W.IDX["B"]] == 1.0 and v[W.IDX["w0t"]] == 0.0 and v[W.IDX["s_origin"]] == 0.0
    assert P["rdiag_d6_max"] == 8.781 and P["rdiag_m6_max"] == 3.192


def test_formal_rconv_numbers_if_present():
    p = HERE / "results" / "rconv.json"
    if not p.exists():
        pytest.skip("results/rconv.json missing")
    fr = run.diag_formal_reference(dict(run.PARAMS), p)
    assert fr["count"] == 2 and round(fr["D6"], 3) == 9.781 and round(fr["M6"], 3) == 3.692
    assert fr["M6_parameter"] == "phi"
    assert run.PARAMS["rdiag_d6_max"] == round(fr["D6"] - 1.0, 3) and run.PARAMS["rdiag_m6_max"] == round(fr["M6"] - 0.5, 3)


def test_chain_seeds_follow_the_mcmc_rule(monkeypatch):
    P = dict(run.PARAMS)
    got = {}
    monkeypatch.setattr(run.F, "run_mcmc", lambda model, c, *, seed, name, **kw: got.update({name: seed}))

    class Ctx:
        log = staticmethod(lambda m: None)

    g, d = _syn_data(n_cl=5, n_co=20)
    m = W.Model(run.setups(P)["col3"], d, g)
    for nm in ("rdiag_S", "rdiag_Sall", "rdiag_SPT", "rdiag_c", "rdiag_cref", "rdiag_zsun"):
        run.mcmc(P, None, nm, m, W.k24_vector(3), Ctx())
        assert got["mcmc_" + nm] == int(run.rng_for(P["seed"], "mcmc_" + nm).integers(2 ** 31))


def test_diag_is_a_standalone_part():
    P = dict(run.PARAMS)
    run.check_standalone(P, {"diag"}, True)
    run.check_standalone(P, {"diag", "conv"}, False)
    with pytest.raises(ValueError):
        run.check_standalone(P, {"diag", "t8p"}, True)
    with pytest.raises(ValueError):
        run.check_standalone(P, {"diag", "t5"}, False)
    assert run.standalone_tag({"diag"}) == "diag" and run.STANDALONE_KEYS["diag"] == ("rdiag", "R_DIAG")
    assert "diag" not in run.PARAMS["parts"]
    old = {"status": "complete", "R_CONV": {}, "T8_P": {}, "overall": {}, "params": {}}
    new = run.summary_with_key(run._dump(old), "R_DIAG", {"reading": "x"})
    assert list(new) == ["status", "R_CONV", "T8_P", "R_DIAG", "overall", "params"]
