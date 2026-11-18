"""Offline tests of the R-SEL code (README 2.5, T-031): synthetic data only, no network, no catalogue."""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pytest
from scipy.special import ndtr

HERE = Path(__file__).parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))


def _import(name):
    spec = importlib.util.spec_from_file_location(f"study010_{name}", HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


m0 = _import("m0")
mocks = _import("mocks")
selaux = _import("selaux")
run = _import("run")


# ---------------------------------------------------------------------------------------------
# SEL-0 merge rule and pass tables
# ---------------------------------------------------------------------------------------------
@pytest.mark.parametrize("counts, groups", [
    ([300] * 4, [[0, 0], [1, 1], [2, 2], [3, 3]]),            # every bin large enough
    ([100, 150, 300, 50, 50], [[0, 1], [2, 4]]),              # young bins accumulate; short last merged back
    ([10, 20, 30, 40], [[0, 3]]),                             # under n_min in all: one group
    ([200, 200], [[0, 0], [1, 1]]),                           # last group closes exactly at the end
    ([250, 0, 0], [[0, 2]]),                                  # empty old bins join the last closed group
    ([0, 0, 199, 1, 5], [[0, 4]]),                            # first group closes at bin 3, last (5) merged
])
def test_merge_rule(counts, groups):
    assert m0.merge_bins(counts, 200) == groups


def test_pass_table_bins_drop_and_pools():
    rng = np.random.default_rng(1)
    age = np.concatenate([rng.uniform(0.01, 20, 3000), [20.0, 0.0, -1.0, np.nan]])
    rel = np.concatenate([rng.uniform(0.02, 0.3, 3000), [0.1, 0.1, 0.1, 0.1]])
    sl = np.concatenate([np.repeat([0, 1], 1500), [1, 0, 0, 1]])
    tabs = m0.pass_table(age, rel, sl, nslice=2, n_min=200)
    assert tabs[0]["n_dropped"] == 2 and tabs[1]["n_dropped"] == 1
    for s, t in enumerate(tabs):
        assert t["edges"][0] == 0.0 and t["edges"][-1] == 20.0
        assert sum(t["n"]) == t["n_parent"]
        assert all(n >= 200 for n in t["n"])
        for b, ix in enumerate(t["pools"]):
            assert np.all(sl[ix] == s)
            assert np.all((age[ix] >= t["edges"][b]) & ((age[ix] < t["edges"][b + 1]) | (age[ix] == 20.0)))
            assert t["n_pass"][b] == int((rel[ix] < 0.15).sum())
            assert t["pi"][b] == pytest.approx(t["n_pass"][b] / t["n"][b])
    assert len(np.flatnonzero(age == 20.0)) == 1
    i20 = int(np.flatnonzero(age == 20.0)[0])
    assert any(i20 in ix for ix in tabs[1]["pools"][-1:])        # Age = 20 in the last pass bin
    assert m0.table_json(tabs)[0].get("pools") is None
    json.dumps(m0.table_json(tabs))


# ---------------------------------------------------------------------------------------------
# SEL-1 term E
# ---------------------------------------------------------------------------------------------
def _tables():
    return [{"edges": [0.0, 3.0, 7.0, 12.0, 20.0], "pi": [0.2, 0.5, 0.8, 0.6]},
            {"edges": [0.0, 5.0, 9.0, 20.0], "pi": [0.3, 0.9, 0.4]}]


def _cells(n=60, seed=2):
    rng = np.random.default_rng(seed)
    A = rng.uniform(0.5, 19.5, n)
    e = A * rng.uniform(0.03, 0.14, n)
    return m0.Cells(A, e, np.ones(n), e / 0.15, sl=rng.integers(0, 2, n))


@pytest.mark.parametrize("truncate", [True, False])
def test_term_e_matches_direct_sum(truncate):
    grid = m0.Grid(0.05, 20.0)
    cells = _cells()
    tabs = _tables()
    _, P = m0.kernels(grid, cells, truncate=truncate, sel="emp", ptab=m0.pass_coefs(tabs))
    e = cells.e[:, None]
    ref = np.zeros_like(P)
    for i in range(len(cells.A)):
        t = tabs[cells.sl[i]]
        ed = np.array(t["edges"], float)
        if not truncate:
            ed[0], ed[-1] = -np.inf, np.inf
        for b, pi in enumerate(t["pi"]):
            ref[i] += pi * (ndtr((ed[b + 1] - grid.mid) / e[i]) - ndtr((ed[b] - grid.mid) / e[i]))
    if truncate:
        ref /= ndtr((20.0 - grid.mid) / e) - ndtr((0.0 - grid.mid) / e)
    assert np.allclose(P, ref, rtol=1e-10, atol=1e-13)


def test_full_cells_have_no_denominator_in_any_mode():
    grid = m0.Grid(0.05, 20.0)
    c = _cells()
    c.thr = None
    for sel in ("cut", "emp", "none"):
        assert m0.kernels(grid, c, sel=sel, ptab=m0.pass_coefs(_tables()))[1] is None
    c2 = _cells()
    assert m0.kernels(grid, c2, sel="none")[1] is None
    with pytest.raises(ValueError):
        m0.kernels(grid, c2, sel="bogus")


def _synthetic_s15(n=4000, seed=3):
    rng = np.random.default_rng(seed)
    tau = np.clip(rng.normal(10.0, 2.0, n), 0.2, 19.8)
    r = rng.uniform(0.03, 0.14, n)
    A = np.clip(tau + r * tau * rng.standard_normal(n), 0.05, 19.95)
    return A, r * A


def test_constant_pi_gives_term_n_optimum():
    grid = m0.Grid(0.05, 20.0)
    A, e = _synthetic_s15()
    cells = m0.compress(A, e, s15=True)
    const = [{"edges": [0.0, 4.0, 8.0, 13.0, 20.0], "pi": [0.6] * 4}]
    for trunc in (True, False):
        mE = m0.OneD(grid, cells, sel="emp", ptab=m0.pass_coefs(const), truncate=trunc)
        mN = m0.OneD(grid, cells, sel="none", truncate=trunc)
        starts = m0.mixture_starts(cells.A, cells.w, 1, 3, np.random.default_rng(0))
        rE, rN = mE.fit_mixture(1, starts), mN.fit_mixture(1, starts)
        assert np.allclose(rE.x, rN.x, atol=1e-4)
        assert rE.fun - rN.fun == pytest.approx(cells.nstar * np.log(0.6), rel=1e-6)
    # grouped (sequence) model with three slices, all at the same constant pi
    rng = np.random.default_rng(4)
    feh = rng.uniform(-1.1, 0.4, len(A))
    sl = np.digitize(feh, [-0.6, 0.0])
    cg = m0.compress(A, e, s15=True, feh=feh, sl=sl)
    gE = m0.Grouped(grid, cg, sel="emp", ptab=m0.pass_coefs(const * 3))
    gN = m0.Grouped(grid, cg, sel="none")
    th0 = [np.array([9.0, -2.0, np.log(1.5)])]
    assert np.allclose(gE.fit_seq(th0).x, gN.fit_seq(th0).x, atol=1e-4)


def _kernels_ref(grid, cells, *, f=1.0, truncate=True, dtype=np.float64):
    """The README 2.0 kernels() as frozen before T-031 (reference for the 'cut' mode)."""
    e = (f * cells.e)[:, None]
    A = cells.A[:, None]
    K = m0.ndiff((grid.lo - A) / e, (grid.hi - A) / e) / grid.step
    if truncate:
        Z = m0.ndiff((0.0 - grid.mid) / e, (grid.tmax - grid.mid) / e)
        K = K / Z
    P = None
    if cells.thr is not None:
        thr = cells.thr[:, None]
        if truncate:
            P = m0.ndiff((thr - grid.mid) / e, (grid.tmax - grid.mid) / e) / Z
        else:
            P = ndtr(-(thr - grid.mid) / e)
        P = P.astype(dtype)
    return K.astype(dtype), P


@pytest.mark.parametrize("truncate", [True, False])
@pytest.mark.parametrize("f", [1.0, 0.8])
def test_cut_mode_unchanged(truncate, f):
    grid = m0.Grid(0.05, 20.0)
    A, e = _synthetic_s15(1500)
    feh = np.random.default_rng(5).uniform(-1.1, 0.4, len(A))
    cells = m0.compress(A, e, s15=True, feh=feh)
    K, P = m0.kernels(grid, cells, f=f, truncate=truncate)
    K0, P0 = _kernels_ref(grid, cells, f=f, truncate=truncate)
    assert np.array_equal(K, K0) and np.array_equal(P, P0)
    # the slice key changes nothing when no cell straddles a slice boundary
    c2 = m0.compress(A, e, s15=True, feh=feh, sl=np.digitize(feh, [-0.6, 0.0]))
    for a, b in ((cells.A, c2.A), (cells.e, c2.e), (cells.w, c2.w), (cells.g, c2.g), (cells.fe, c2.fe)):
        assert np.array_equal(a, b)
    g = m0.Grouped(grid, cells)
    th = np.array([9.0, -2.5, np.log(1.4)])
    v, gr = g.seq_negll(th)
    assert np.isfinite(v) and np.all(np.isfinite(gr))


# ---------------------------------------------------------------------------------------------
# SEL-2 generator
# ---------------------------------------------------------------------------------------------
def test_pools_pass_fraction_equals_pi_and_mock_pass_rate_under_rA():
    rng = np.random.default_rng(6)
    n = 6000
    age = rng.uniform(0.1, 19.9, n)
    rel = np.where(age < 8, rng.uniform(0.05, 0.4, n), rng.uniform(0.02, 0.2, n))
    tab = m0.pass_table(age, rel, None, nslice=1, n_min=200)
    edges, pools = [tab[0]["edges"]], [[rel[ix] for ix in tab[0]["pools"]]]
    for b, pool in enumerate(pools[0]):           # by construction
        assert np.mean(pool < 0.15) == pytest.approx(tab[0]["pi"][b], abs=1e-12)
    b = 3
    lo, hi = tab[0]["edges"][b], tab[0]["edges"][b + 1]
    target = 4000

    def draw(k):
        tau = rng.uniform(lo, hi, k)
        sl = np.zeros(k, np.int64)
        return {"tau": tau, "r": mocks.draw_r_keyed(tau, sl, edges, pools, rng), "sl": sl}
    cat, par = mocks.catalogue_sel(draw, target, "rA", rng, s15=True)
    rate = target / len(par["A"])
    pi = tab[0]["pi"][b]
    assert abs(rate - pi) < 5 * np.sqrt(pi * (1 - pi) / len(par["A"])) + 1e-3
    # mock parent: ends at the star completing the target count; sample = the parent's passing stars
    assert par["pass"][-1] and int(par["pass"].sum()) == target and len(cat["A"]) == target
    assert np.all(cat["e"] / cat["A"] < 0.15)
    assert np.all((par["A"] > 0) & (par["A"] < 20))


def test_catalogue_sel_without_cut_and_keyed_r_slices():
    rng = np.random.default_rng(7)
    edges = [[0.0, 10.0, 20.0], [0.0, 20.0]]
    pools = [[np.array([0.01]), np.array([0.02])], [np.array([0.05])]]
    tau = np.array([1.0, 15.0, 3.0, 19.0])
    sl = np.array([0, 0, 1, 1])
    assert np.allclose(mocks.draw_r_keyed(tau, sl, edges, pools, rng), [0.01, 0.02, 0.05, 0.05])
    cat, par = mocks.catalogue_sel(lambda k: {"tau": np.full(k, 5.0), "r": np.full(k, 0.3)}, 100, "rtau", rng,
                                   s15=False)
    assert par is None and len(cat["A"]) == 100
    with pytest.raises(RuntimeError):
        mocks.draw_r_keyed(tau, np.array([0, 0, 2, 2]), edges, pools, rng)


# ---------------------------------------------------------------------------------------------
# SEL-8 seed nest
# ---------------------------------------------------------------------------------------------
def test_seed_nest():
    sets = selaux.sel_sets(5, ["rtau", "rA"], [2, 3, 4])
    assert [s["k"] for s in sets] == list(range(124))
    count = lambda f: sum(1 for s in sets if f(s))
    assert count(lambda s: s["tag"] == "R1" and s["floor"] == "primary") == 90
    assert [s["k"] for s in sets if s["tag"] == "A_rec"] == [90, 91, 92, 93]
    assert [s["k"] for s in sets if s["tag"] == "B"] == list(range(94, 102))
    assert [s["k"] for s in sets if s["tag"] == "diag"] == [102, 103, 104, 105]
    assert [s["k"] for s in sets if s.get("floor") == "sens"] == list(range(106, 124))
    assert count(lambda s: s["group"] == "R1") == 108 and count(lambda s: s["group"] == "AB") == 12
    assert count(lambda s: s["group"] == "diag") == 4
    s = sets[30]
    assert (s["variant"], s["bin"], s["kind"], s["mech"]) == ("S15N", 0, "null_sn", "rtau")
    s = sets[89]
    assert (s["variant"], s["bin"], s["kind"], s["mech"]) == ("Full", 4, "power", "rA")
    assert (sets[94]["term"], sets[94]["kind"], sets[94]["mech"]) == ("E", "id", "rtau")
    assert (sets[101]["term"], sets[101]["kind"], sets[101]["mech"]) == ("N", "mis", "rA")
    assert (sets[106]["variant"], sets[106]["bin"], sets[106]["mech"]) == ("S15E", 2, "rtau")
    assert (sets[123]["variant"], sets[123]["bin"], sets[123]["mech"]) == ("Full", 4, "rA")
    a = selaux.mock_rng(0, 31, 17, 3).random(5)
    assert np.array_equal(a, np.random.default_rng([0, 31, 17, 3]).random(5))
    assert not np.array_equal(a, selaux.mock_rng(0, 31, 17, 4).random(5))


# ---------------------------------------------------------------------------------------------
# SEL-3 edge loop
# ---------------------------------------------------------------------------------------------
def test_edge_loop_cases():
    assert selaux.candidate_edges(7.0, 0.5, 2.0) == [7.0, 6.5, 6.0, 5.5, 5.0, 4.5, 4.0, 3.5, 3.0, 2.5, 2.0]
    ok = selaux.edge_loop(lambda e: (True, 0.05))
    assert ok["valid"] and ok["edge"] == 7.0
    none = selaux.edge_loop(lambda e: (False, 1.0))
    assert not none["valid"] and none["edge"] == 7.0 and len(none["trace"]) == 1
    step = selaux.edge_loop(lambda e: (True, 0.15 if e > 6.75 else 0.04))
    assert step["valid"] and step["edge"] == 6.5 and step["true_d"] == 0.04
    lost = selaux.edge_loop(lambda e: (e > 5.75, 0.3 if e > 5.75 else 1.0))
    assert not lost["valid"] and lost["edge"] == 6.0 and lost["true_d"] == 0.3
    floor = selaux.edge_loop(lambda e: (True, 0.5))
    assert not floor["valid"] and floor["edge"] == 2.0 and len(floor["trace"]) == 11


def test_power_models_on_the_grid():
    """README SEL-3 offline check on the generating models (the raw fractions quoted there)."""
    C = run.Ctx(dict(run.PARAMS))
    pm = run.r1_power_model_sel(C, 0.0, 0.094, 0.12)               # bin [-0.1, 0.1), S15
    assert pm["valid"] and pm["young"][1] == 7.0 and pm["true_d"] <= 0.02 and pm["w_old"] == 0.12
    pm = run.r1_power_model_sel(C, 0.2, 0.121, 0.12)               # bin [0.1, 0.3)
    assert pm["valid"] and pm["young"][1] == 6.5 and pm["true_d"] <= 0.1
    assert pm["edge_trace"][0][2] > 0.1
    pm = run.r1_power_model_sel(C, 0.0, 0.094, 0.10)               # the 2.1 floor: no valley at all
    assert not pm["valid"] and pm["young"][1] == 7.0 and pm["true_d"] == 1.0
    for fc, raw in ((-0.6, 0.415), (-0.4, 0.296), (-0.2, 0.153)):
        for floor in (0.12, 0.20):
            assert run.r1_power_model_sel(C, fc, raw, floor)["valid"]


# ---------------------------------------------------------------------------------------------
# labels, projection, checkpoints
# ---------------------------------------------------------------------------------------------
def test_label_rules():
    lab = selaux.r1_label("not reproduced", "not reproduced", "undetermined")
    assert lab["bare"] == "not reproduced" and not lab["robust"]
    assert lab["label"] == "not reproduced (not robust; selection-term robust)"
    assert selaux.r1_label("undetermined", "reproduced", "undetermined")["selection_term"] == "selection-term sensitive"
    assert selaux.primacy(True, True) == ("S15", False)
    assert selaux.primacy(True, False) == ("S15", True)
    assert selaux.primacy(False, True) == ("Full", False)
    assert selaux.primacy(False, False) == (None, False)
    assert selaux.r34_bare(None, (4.5, 6.5), 0.82, 0.1) == ("cannot determine", "cannot determine")
    assert selaux.r34_bare({"span": 6.0, "sigma": 0.9}, (4.5, 6.5), 0.82, 0.1) == ("reproduced", "reproduced")
    assert selaux.r34_bare({"span": 6.6, "sigma": 0.95}, (4.5, 6.5), 0.82, 0.1) == ("not reproduced", "not reproduced")
    assert selaux.with_robust("reproduced", False) == "reproduced, not robust"
    assert selaux.with_robust("not reproduced", False) == "not reproduced"
    ib = lambda s, se, b: selaux.intrinsic_bare(s, se, b, 0.1, 1.645, 0.82)
    assert ib(0.5, 0.05, [0.05, -0.02]) == "confirmed"
    assert ib(0.5, 0.05, [0.11]) == "cannot determine"
    assert ib(1.2, 0.05, [0.0]) == "not confirmed"
    assert ib(0.8, 0.05, [0.0]) == "cannot determine"
    bins = [{"resolvable": True, "almost_disjoint": True, "edge": e} for e in (7.0, 8.0, 9.0)]
    assert selaux.r1_verdict(bins) == ("reproduced", 8.0)
    assert selaux.r1_verdict(bins[:2]) == ("undetermined", None)
    assert selaux.r1_verdict(bins[:2] + [{"resolvable": True, "almost_disjoint": False, "edge": None}])[0] == "not reproduced"


def test_qualifiers_compare_bare_categories():
    cd, cdse = "cannot determine", "cannot determine (non-finite standard error)"
    assert selaux.category(cdse) == cd and selaux.category("reproduced") == "reproduced"
    assert selaux.category(selaux.NONFINITE) == cd
    assert selaux.selterm(cd, cdse) == "selection-term robust"
    assert selaux.selterm("confirmed", cdse) == "selection-term sensitive"
    assert selaux.same_category(cd, cdse, selaux.NONFINITE)
    lab = selaux.r1_label(selaux.NONFINITE, "undetermined", "cannot determine")
    assert lab["robust"] and lab["selection_term"] == "selection-term sensitive"
    assert lab["bare"] == selaux.NONFINITE                     # the parenthetical is kept for display


def test_r1_decide_rank():
    P = dict(run.PARAMS)
    D = {"shape": {"valley": True, "d": 0.2, "edge": 8.0, "t": 7.0}}
    null = [{"d": d, "valley": True} for d in (0.05, 0.1, 0.15)] + [{"d": 1.0, "valley": False}] * 47
    res = {(k, m): null for k in ("null_sn", "null_sp") for m in P["mechs"]}
    res.update({("power", m): [{"d": 0.01, "valley": True}] * 50 for m in P["mechs"]})
    dec = run.r1_decide(P, D, res, 50, qrank=3)
    assert dec["d_star"] == 0.15 and dec["almost_disjoint"] is False and dec["resolvable"]
    assert run.r1_decide(P, D, res, 50, qrank=2)["d_star"] == 0.1


def test_projection():
    st = {0: {"group": "R1", "times": [2.0] * 4}, 1: {"group": "R1", "times": [5.0]},
          2: {"group": "AB", "times": [10.0]}, 3: {"group": "AB", "times": [8.0, 9.0]}}
    # R1 has a finished set (mean 2 s): set 1 has 3 left -> 6 s; AB has none: first-mock times
    assert selaux.projection_h(3600.0, st, 4) == pytest.approx((3600 + 3 * 2.0 + 3 * 10.0 + 2 * 8.0) / 3600)


def test_mock_store_stop_and_consent(tmp_path):
    st = selaux.MockStore(tmp_path, "abc")
    assert st.get(1, 0) is None
    st.put(1, 0, {"d": 0.5}, 2.0)
    assert st.get(1, 0)["result"] == {"d": 0.5}
    (st.dir / "k002_j00.json").write_text("{broken", encoding="utf-8")
    assert st.get(2, 0) is None and not (st.dir / "k002_j00.json").exists()
    with pytest.raises(RuntimeError):
        selaux.MockStore(tmp_path, "abc")                          # locked by the first run
    st.stop({"projection_h": 17.0})
    with pytest.raises(selaux.StopRun):
        selaux.MockStore(tmp_path, "abc")                          # stopped: needs consent
    (st.dir / "resume_consent.txt").write_text("2026-11-18 user consent (log.md)", encoding="utf-8")
    st2 = selaux.MockStore(tmp_path, "abc")
    assert st2.resumed and st2.get(1, 0)["result"] == {"d": 0.5}
    assert st2.elapsed_s() >= 0.0
    assert not (st2.dir / "resume_consent.txt").exists()          # consent is used once
    assert st2.limit_h is None and st2.resumes()[0]["limit_h"] is None
    st2.finish()
    assert not st2.dir.exists()


def test_checkpoint_key_ignores_stop_limit_and_parts():
    text = (HERE / "run.py").read_text(encoding="utf-8")
    assert '"sel_stop_h": 16.0' in text
    edited = text.replace('"sel_stop_h": 16.0', '"sel_stop_h": 24.0').replace('"parts": ["sel"]', '"parts": ["orig", "sel"]')
    assert selaux.strip_params(edited) == selaux.strip_params(text)
    assert selaux.strip_params(text.replace("def main_sel(", "def main_sel_x(")) != selaux.strip_params(text)
    P = dict(run.PARAMS)
    src = {"run.py": selaux.strip_params(text), "m0.py": "x"}
    k0 = selaux.checkpoint_key(P, src, b"data")
    assert selaux.checkpoint_key({**P, "sel_stop_h": 24.0, "parts": ["orig"]}, src, b"data") == k0
    assert selaux.checkpoint_key({**P, "sel_n_mock": 49}, src, b"data") != k0
    assert selaux.checkpoint_key(P, src, b"other") != k0
    assert selaux.checkpoint_key(P, {**src, "m0.py": "y"}, b"data") != k0
    crlf = {k: v.replace("\n", "\r\n") for k, v in src.items()}
    assert selaux.checkpoint_key(P, crlf, b"data") == k0


def test_resume_with_raised_limit_continues_from_checkpoints(tmp_path):
    sets = [{"k": k, "group": g} for k, g in enumerate(["R1", "R1", "AB"])]
    calls = []

    def run_one(s, rng):
        calls.append(s["k"])
        return {"d": float(rng.random()), "valley": True, "k": 2, "pass_rate": None}
    mk = lambda k, j: selaux.mock_rng(0, 31, k, j)
    st = selaux.MockStore(tmp_path, "key")
    with pytest.raises(selaux.StopRun):
        selaux.run_mock_sets(sets, 4, st, run_one, mk, 1e-12, log=lambda m: None)
    assert sorted(calls) == [0, 1, 2]                      # stopped after the first-mock pass
    with pytest.raises(selaux.StopRun):                     # no consent yet
        selaux.MockStore(tmp_path, "key")
    (st.dir / "resume_consent.txt").write_text("user consent 2026-11-18 (log.md)\nlimit_h = 24\n", encoding="utf-8")
    st2 = selaux.MockStore(tmp_path, "key")
    assert st2.resumed and st2.limit_h == 24.0 and st2.resumes()[-1]["limit_h"] == 24.0
    calls.clear()
    res, state, log = selaux.run_mock_sets(sets, 4, st2, run_one, mk, 1e-12, log=lambda m: None)
    assert sorted(calls) == [0, 0, 0, 1, 1, 1, 2, 2, 2]    # only the mocks not yet checkpointed
    assert all(p["limit_h"] == 24.0 for p in log) and log[-1]["mocks_left"] == 0
    for s in sets:                                          # identical to an uninterrupted run
        assert [r["d"] for r in res[s["k"]]] == [float(mk(s["k"], j).random()) for j in range(4)]
    st2.release()
    st3 = selaux.MockStore(tmp_path, "key")                 # the limit stays for the rest of the run
    assert st3.limit_h == 24.0 and not st3.resumed
    st3.release()


def test_nonfinite_results_are_counted():
    assert selaux.nonfinite({"sigma": float("nan"), "a": 1.0})
    assert selaux.nonfinite({"d": float("inf")})
    assert not selaux.nonfinite({"d": 0.3, "valley": True, "k": 2, "pass_rate": None})
    assert selaux._jsonable_result({"x": np.float64("nan"), "v": np.bool_(True), "k": np.int64(3)})["k"] == 3
