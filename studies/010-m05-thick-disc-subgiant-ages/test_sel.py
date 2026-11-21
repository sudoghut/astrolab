"""Offline tests of the R-SEL code (README 2.5, T-031): synthetic data only, no network, no catalogue."""
import importlib.util
import json
import os
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
    edited = text.replace('"sel_stop_h": 16.0', '"sel_stop_h": 24.0').replace('"parts": ["err"]', '"parts": ["orig", "sel"]')
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


def test_write_retries_a_refused_replace(tmp_path, monkeypatch):
    real = os.replace
    fails = {"n": 3}

    def flaky(src, dst):
        if fails["n"] > 0:
            fails["n"] -= 1
            raise PermissionError(5, "Access is denied")
        return real(src, dst)
    monkeypatch.setattr(selaux.os, "replace", flaky)
    p = tmp_path / "x.json"
    selaux.MockStore._write(p, {"a": 1}, pause=0.0)
    assert json.loads(p.read_text(encoding="utf-8")) == {"a": 1} and fails["n"] == 0
    fails["n"] = 10                                          # a refusal that persists is raised
    with pytest.raises(PermissionError):
        selaux.MockStore._write(p, {"a": 2}, tries=4, pause=0.0)
    assert fails["n"] == 6                                   # exactly 4 attempts
    assert json.loads(p.read_text(encoding="utf-8")) == {"a": 1}
    assert not list(tmp_path.glob("*.tmp"))                  # the temporary file is removed
    monkeypatch.setattr(selaux.os, "replace", lambda s, t: (_ for _ in ()).throw(OSError(22, "other")))
    with pytest.raises(OSError):                             # other errors: not retried, temp removed
        selaux.MockStore._write(p, {"a": 3}, pause=0.0)
    assert not list(tmp_path.glob("*.tmp"))
    monkeypatch.setattr(selaux.os, "replace", real)
    selaux.MockStore._write(p, {"a": 4}, tries=0)            # tries <= 0 still writes once
    assert json.loads(p.read_text(encoding="utf-8")) == {"a": 4}


def test_resume_does_not_count_checkpointed_mocks_as_left(tmp_path):
    sets = [{"k": k, "group": g} for k, g in enumerate(["R1", "R1", "AB"])]
    mk = lambda k, j: selaux.mock_rng(0, 31, k, j)
    st = selaux.MockStore(tmp_path, "key")
    for s in sets:                                          # an earlier session checkpointed sets 0 and 2
        if s["k"] != 1:
            for j in range(4):
                st.put(s["k"], j, {"d": float(mk(s["k"], j).random())}, 100.0)
    st.release()
    st2 = selaux.MockStore(tmp_path, "key")
    calls = []

    def run_one(s, rng):
        calls.append(s["k"])
        return {"d": float(rng.random())}
    res, state, log = selaux.run_mock_sets(sets, 4, st2, run_one, mk, 1e6, log=lambda m: None)
    first = log[0]                                          # after the first-mock pass
    assert first["mocks_done"] == 3 and first["mocks_checkpointed_not_replayed"] == 6
    assert first["mocks_left"] == 3                          # only set 1's mocks 1-3
    el = first["elapsed_h"] * 3600
    # set 1 (R1) uses the finished R1 set 0 (100 s per mock): 3 x 100 s; nothing else is left
    assert first["projection_h"] == pytest.approx((el + 3 * 100.0) / 3600, abs=1e-6)
    assert sorted(calls) == [1, 1, 1, 1]
    assert log[-1]["mocks_left"] == 0
    for s in sets:
        assert [r["d"] for r in res[s["k"]]] == [float(mk(s["k"], j).random()) for j in range(4)]
    st2.release()


def _seed_sessions(st, sets, mk, skip, seconds):
    for s in sets:
        for j in range(4):
            if (s["k"], j) not in skip:
                st.put(s["k"], j, {"d": float(mk(s["k"], j).random())}, seconds)


def test_resume_stop_rule_counts_only_mocks_without_checkpoint(tmp_path):
    sets = [{"k": k, "group": "R1"} for k in range(3)]
    mk = lambda k, j: selaux.mock_rng(0, 31, k, j)
    run_one = lambda s, rng: {"d": float(rng.random())}
    # (a) all mocks checkpointed, elapsed already above the limit: nothing is left, so no stop
    st = selaux.MockStore(tmp_path, "a")
    _seed_sessions(st, sets, mk, set(), 1.0)
    (st.sessions / "old.json").write_text(json.dumps({"seconds": 7200.0}), encoding="utf-8")
    st.release()
    st = selaux.MockStore(tmp_path, "a")
    res, _, log = selaux.run_mock_sets(sets, 4, st, run_one, mk, 1.0, log=lambda m: None)
    assert log[0]["mocks_left"] == 0 and log[0]["projection_h"] > 1.0
    st.release()
    # (b) one mock without a checkpoint: the old count (8 replays + 1 left) x 1000 s would be ~2.5 h,
    # the corrected one ~0.3 h; a 1 h limit must not stop
    st = selaux.MockStore(tmp_path, "b")
    _seed_sessions(st, sets, mk, {(2, 3)}, 1000.0)
    st.release()
    st = selaux.MockStore(tmp_path, "b")
    res, _, log = selaux.run_mock_sets(sets, 4, st, run_one, mk, 1.0, log=lambda m: None)
    assert log[0]["mocks_left"] == 1 and log[0]["projection_h"] < 0.5
    st.release()
    # (c) the same with a limit below one mock's time: the run stops before the uncomputed mock
    st = selaux.MockStore(tmp_path, "c")
    _seed_sessions(st, sets, mk, {(2, 3)}, 1000.0)
    st.release()
    st = selaux.MockStore(tmp_path, "c")
    with pytest.raises(selaux.StopRun):
        selaux.run_mock_sets(sets, 4, st, run_one, mk, 0.1, log=lambda m: None)
    info = json.loads((st.dir / "stopped.json").read_text(encoding="utf-8"))
    assert info["mocks_left"] == 1 and info["mocks_checkpointed"] == 11


def test_damaged_checkpoint_counts_as_left_and_is_recomputed(tmp_path):
    sets = [{"k": 0, "group": "R1"}]
    mk = lambda k, j: selaux.mock_rng(0, 31, k, j)
    st = selaux.MockStore(tmp_path, "key")
    _seed_sessions(st, sets, mk, set(), 1.0)
    (st.dir / "k000_j02.json").write_text("{", encoding="utf-8")
    st.release()
    st = selaux.MockStore(tmp_path, "key")
    calls = []
    run_one = lambda s, rng: calls.append(1) or {"d": float(rng.random())}
    res, _, log = selaux.run_mock_sets(sets, 4, st, run_one, mk, 1e6, log=lambda m: None)
    assert log[0]["mocks_left"] == 1 and len(calls) == 1
    assert [r["d"] for r in res[0]] == [float(mk(0, j).random()) for j in range(4)]
    st.release()


def test_nonfinite_results_are_counted():
    assert selaux.nonfinite({"sigma": float("nan"), "a": 1.0})
    assert selaux.nonfinite({"d": float("inf")})
    assert not selaux.nonfinite({"d": 0.3, "valley": True, "k": 2, "pass_rate": None})
    assert selaux._jsonable_result({"x": np.float64("nan"), "v": np.bool_(True), "k": np.int64(3)})["k"] == 3


# ---------------------------------------------------------------------------------------------
# R1-SEL-FIT (README 2.6, T-049)
# ---------------------------------------------------------------------------------------------
def test_selfit_helpers_and_sets():
    assert selaux.better_fit(10.0, 9.99) == "o"            # within the 0.01 tie rule: keep (o)
    assert selaux.better_fit(10.0, 9.98) == "i"
    assert selaux.better_fit(10.0, float("nan")) == "o"    # a non-finite (i) is never selected
    assert selaux.better_fit(10.0, None) == "o"
    assert selaux.nonmonotone_k({1: 5.0, 2: 6.0, 3: 4.0, 4: 4.005}) == [2]
    assert selaux.nonmonotone_k({1: 5.0, 2: 4.0, 3: 3.0}) == []
    P = run.PARAMS
    sets = selaux.selfit_sets(len(P["r1_bins"]), P["mechs"], P["sel_floor_sens_bins"])
    assert [s["k"] for s in sets] == list(range(90)) + list(range(106, 124))
    assert all(s["tag"] == "R1" for s in sets) and len(sets) * P["sel_n_mock"] == 5400
    assert P["selfit_seed_tag"] == 45 and P["selfit_nstart"] == 8 and P["selfit_stop_h"] == 12.0
    assert "selfit_stop_h" in selaux.NO_KEY_PARAMS


def test_parts_validation(monkeypatch):
    for bad in (["selfit", "sel"], ["orig", "selfit"], ["x"], []):
        monkeypatch.setitem(run.PARAMS, "parts", bad)
        with pytest.raises(ValueError):
            run.main(None)


def _synthetic_D(C, variant="Full", n=3000, seed=11):
    """A small R1 data-fit dict for one synthetic bin (power model of README 2.1 with old weight 0.4)."""
    rng = np.random.default_rng(seed)
    tau = mocks.latent_power(11.0, 0.82, 0.4, 7.0, n, rng)
    rel = rng.uniform(0.03, 0.14, n)
    A = tau * (1 + rel * rng.standard_normal(n))
    A = np.clip(A, 0.2, 19.8)
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
            "splitnorm": [9.0, np.log(3.0), np.log(2.0)], "power_models": {"primary": pm, "sens": pm}}, pools


@pytest.mark.parametrize("kind", ["power", "null_sn"])
def test_selfit_path_o_reproduces_r1_mock_sel(kind):
    """README 2.6: fit (o) of r1_mock_selfit is r1_mock_sel on the same SEL-8 stream (the (i) stream is
    separate), and the chosen fit is never worse than (o) for any K."""
    C = run.Ctx(dict(run.PARAMS))
    D, pools = _synthetic_D(C)
    ref = run.r1_mock_sel(C, D, kind, "rA", "primary", np.random.default_rng(5), pools)
    new = run.r1_mock_selfit(C, D, kind, "rA", "primary", (np.random.default_rng(5), np.random.default_rng(6)),
                             pools, 8)
    assert new["o_d"] == ref["d"] and new["o_valley"] == ref["valley"] and new["o_k"] == ref["k"]
    assert all(isinstance(new[f"i_used_k{K}"], bool) for K in range(1, 5)) and new["i_used_k5"] in (-1, 0, 1)
    # a different (i) stream does not change (o)
    other = run.r1_mock_selfit(C, D, kind, "rA", "primary", (np.random.default_rng(5), np.random.default_rng(7)),
                               pools, 8)
    assert other["o_d"] == new["o_d"] and other["o_k"] == new["o_k"]


def test_selfit_mock_check_flags_differences():
    rec = {"variants": {v: {"bins": [{"mocks": {"power_rA": {"k": 5, "d": [0.1, 1.0], "valley": [True, False]}}}]}
                        for v in selaux.R1_VARIANTS},
           "floor_sensitivity": {v: {"bins": []} for v in selaux.R1_VARIANTS}}
    sets = [{"k": 5}]
    ok = {5: [{"o_d": 0.1, "o_valley": True}, {"o_d": 1.0, "o_valley": False}]}
    assert run.selfit_mock_check(ok, sets, rec)[0] == []
    bad = {5: [{"o_d": 0.1 + 2e-9, "o_valley": True}, {"o_d": 1.0, "o_valley": True}]}
    assert run.selfit_mock_check(bad, sets, rec)[0] == [[5, 0], [5, 1]]
    assert run.selfit_mock_check({6: ok[5]}, [{"k": 6}], rec)[0] == [[6, 0], [6, 1]]   # no record counts as a difference


def test_r1_sel_bins_rederives_recorded_r1_sel():
    """The refactored decision function (shared by R1-SEL and R1-SEL-FIT) re-derives the recorded R1-SEL
    powers, d*, resolvability and verdicts from the recorded mock d values."""
    path = HERE / "results" / "r1_sel.json"
    if not path.exists():
        pytest.skip("results/r1_sel.json not present")
    rec = json.loads(path.read_text(encoding="utf-8"))
    P = dict(run.PARAMS)
    nbins, mechs, sens = len(P["r1_bins"]), P["mechs"], list(P["sel_floor_sens_bins"])
    sets = selaux.selfit_sets(nbins, mechs, sens)
    _, recmock = run.selfit_mock_check({}, [], rec)
    results = {s["k"]: [{"d": d, "valley": v, "pass_rate": 0.9} for d, v in zip(recmock[s["k"]]["d"], recmock[s["k"]]["valley"])]
               for s in sets}
    nf = {s["k"]: 0 for s in sets}
    kof = {("R1", s["variant"], s["bin"], None, s["kind"], s["mech"], s["floor"]): s["k"] for s in sets}
    r1d = {}
    for v in selaux.R1_VARIANTS:
        for b in range(nbins):
            B, F_ = rec["variants"][v]["bins"][b], rec["data_fits"][f"{v}_{b}"]
            r1d[(v, b)] = {"shape": {"d": B["d"], "edge": B["edge"], "t": B["valley_t"], "k": B["k"], "cap": B["cap"],
                                     "valley": B["valley"], "peaks": B["peaks"]},
                           "power_models": F_["power_models"], "bin": B["bin"], "n": B["n"], "bic": B["bic"]}
    data_frac = {f"R1_{b}": None for b in range(nbins)}
    for floor, src in (("primary", "variants"), ("sens", "floor_sensitivity")):
        for v in selaux.R1_VARIANTS:
            out = run.r1_sel_bins(P, r1d, results, kof, nf, data_frac, v, floor, nbins, mechs, sens, P["sel_n_mock"])
            want = rec[src][v]
            assert out["verdict"] == want["verdict"]
            for got, w in zip(out["bins"], want["bins"]):
                assert got["power"] == w["power"] and got["d_star"] == w["d_star"]
                assert got["resolvable"] == w["resolvable"] and got["almost_disjoint"] == w["almost_disjoint"]


def test_selfit_mock_through_run_mock_sets(tmp_path):
    """End to end through the checkpointing runner: tuple make_rng, a JSON-storable result, and the
    replay from the checkpoint equals the first computation (README 2.6)."""
    C = run.Ctx(dict(run.PARAMS))
    D, pools = _synthetic_D(C)
    sets = [{"k": 4, "group": "R1", "kind": "power", "mech": "rtau", "floor": "primary"}]
    run_one = lambda s, rngs: run.r1_mock_selfit(C, D, s["kind"], s["mech"], s["floor"], rngs, pools, 8)
    make_rng = lambda k, j: (np.random.default_rng([0, 31, k, j]), np.random.default_rng([0, 45, k, j]))
    st = selaux.MockStore(tmp_path, "k1")
    res, state, _ = selaux.run_mock_sets(sets, 1, st, run_one, make_rng, 12.0, log=lambda m: None)
    st.release()
    r = res[4][0]
    assert set(r) >= {"d", "valley", "k", "o_d", "o_valley", "o_k", "i_used_k1", "i_used_k5", "o_nonmonotone"}
    assert r["i_used_k5"] in (-1, 0, 1) and not selaux.nonfinite(r)
    st2 = selaux.MockStore(tmp_path, "k1")
    res2, _, _ = selaux.run_mock_sets(sets, 1, st2, lambda s, g: (_ for _ in ()).throw(AssertionError("recomputed")),
                                      make_rng, 12.0, log=lambda m: None)
    st2.release()
    assert res2[4][0] == r


# ---------------------------------------------------------------------------------------------
# R1-ERR (README 2.7, T-054)
# ---------------------------------------------------------------------------------------------
from scipy.stats import kstest  # noqa: E402


def _observe_ref(tau, r, mech, rng, tmax=20.0):
    """mocks.observe as it was before R1-ERR (commit f0a8455), for the f = 1 identity test."""
    tau = np.asarray(tau, float)
    r = np.asarray(r, float)
    A = np.full(len(tau), np.nan)
    todo = np.arange(len(tau))
    for _ in range(200):
        if len(todo) == 0:
            break
        z = rng.standard_normal(len(todo))
        if mech == "rtau":
            a = tau[todo] + r[todo] * tau[todo] * z
        else:
            den = 1.0 - r[todo] * z
            a = np.where(den > 0, tau[todo] / np.where(den > 0, den, 1.0), np.nan)
        ok = np.isfinite(a) & (a > 0) & (a < tmax)
        A[todo[ok]] = a[ok]
        todo = todo[~ok]
    keep = np.isfinite(A)
    tau, r, A = tau[keep], r[keep], A[keep]
    e = r * tau if mech == "rtau" else r * A
    return A, e, keep


def _catalogue_sel_ref(draw_rows, n_target, mech, rng, *, s15, cut=0.15, tmax=20.0, batch=None):
    """mocks.catalogue_sel as it was before R1-ERR (commit f0a8455)."""
    out = {}
    have = 0
    for _ in range(mocks.MAX_ROUNDS):
        if have >= n_target:
            break
        m = batch or max(2 * (n_target - have), 1024)
        rows = draw_rows(m)
        A, e, keep = _observe_ref(rows["tau"], rows["r"], mech, rng, tmax)
        new = {"A": A, "e": e}
        for k, v in rows.items():
            new[k] = np.asarray(v)[keep]
        new["pass"] = (e / A < cut) if s15 else np.ones(len(A), bool)
        for k, v in new.items():
            out[k] = np.concatenate([out[k], v]) if k in out else v
        have = int(out["pass"].sum())
    if have < n_target:
        raise RuntimeError("selection rate too low")
    last = int(np.flatnonzero(out["pass"])[n_target - 1])
    parent = {k: v[:last + 1] for k, v in out.items()}
    sample = {k: v[parent["pass"]] for k, v in parent.items() if k != "pass"}
    return sample, (parent if s15 else None)


@pytest.mark.parametrize("f", [1.2, 2.0, 2.81])
def test_observe_f_scales_the_deviate_under_rtau(f):
    """README 2.7 test (i): e = r tau, no truncation in effect: std of (A - tau) / e is f."""
    n, tau, r = 200_000, 10.0, 0.05                   # f r tau <= 1.4 Gyr: 0 and 20 are >= 7 sigma away
    A, e, keep = mocks.observe(np.full(n, tau), np.full(n, r), "rtau", np.random.default_rng(1), f=f)
    assert keep.all()
    x = (A - tau) / e
    assert np.all(e == r * tau)                       # the catalogue error is unchanged
    assert abs(x.std() - f) < 4 * f / np.sqrt(2 * n)
    assert abs(x.mean()) < 4 * f / np.sqrt(n)


@pytest.mark.parametrize("f", [1.2, 1.5, 2.81])
def test_observe_f_scales_the_deviate_under_rA(f):
    """README 2.7 test (ii): e = r A, at fixed tau: 1 - tau / A = f r z passes a KS test against N(0, (f r)^2)."""
    n, tau, r = 100_000, 10.0, 0.04                  # A < 20 needs f r z < 0.5: z < 4.4 at f = 2.81
    A, e, keep = mocks.observe(np.full(n, tau), np.full(n, r), "rA", np.random.default_rng(2), f=f)
    assert keep.all() and np.allclose(e, r * A, rtol=0, atol=0)
    assert kstest(1 - tau / A, "norm", args=(0.0, f * r)).pvalue > 0.01
    # a wrong scale is rejected (the test has power)
    assert kstest(1 - tau / A, "norm", args=(0.0, r)).pvalue < 1e-6


@pytest.mark.parametrize("mech", ["rtau", "rA"])
def test_f1_generator_is_bit_identical(mech):
    """README 2.7 test (iii): at f = 1, observe and catalogue_sel return exactly the arrays of the code
    before R1-ERR for the same stream (default f and an explicit f = 1.0)."""
    rng0 = np.random.default_rng(3)
    tau = np.concatenate([rng0.uniform(0.3, 19.0, 3000), [0.05, 19.9, 19.99]])   # some stars need redraws
    r = rng0.uniform(0.02, 0.6, len(tau))
    ref = _observe_ref(tau, r, mech, np.random.default_rng(4))
    for kw in ({}, {"f": 1.0}, {"f": 1}):
        new = mocks.observe(tau, r, mech, np.random.default_rng(4), **kw)
        for a, b in zip(ref, new):
            assert np.array_equal(a, b)

    def make_draw(rng):
        def draw(m):
            t = mocks.latent_power(11.0, 0.82, 0.3, 7.0, m, rng)
            return {"tau": t, "r": rng.uniform(0.02, 0.3, m), "sl": np.zeros(m, np.int64)}
        return draw
    for s15 in (True, False):
        g1, g2 = np.random.default_rng(5), np.random.default_rng(5)
        sa, pa = _catalogue_sel_ref(make_draw(g1), 2000, mech, g1, s15=s15)
        stats = {}
        sb, pb = mocks.catalogue_sel(make_draw(g2), 2000, mech, g2, s15=s15, f=1.0, stats=stats)
        assert set(sa) == set(sb)
        assert all(np.array_equal(sa[k], sb[k]) for k in sa)
        assert (pa is None) == (pb is None)
        if pa is not None:
            assert all(np.array_equal(pa[k], pb[k]) for k in pa)
        assert g1.random() == g2.random()            # same stream position afterwards
        assert stats["drawn"] >= len(sb["A"]) and stats["dropped"] >= 0


def test_redraw_limit_drops_are_counted():
    """Stars that do not reach (0, tmax) in 200 draws are dropped by observe; catalogue_sel counts them
    over all its draws (README 2.7, reported per set)."""
    def draw(m):
        return {"tau": np.full(m, 19.999), "r": np.full(m, 1000.0)}   # a draw lands in (0, 20) with p ~ 1e-3
    stats = {}
    sample, parent = mocks.catalogue_sel(draw, 50, "rtau", np.random.default_rng(8), s15=False, stats=stats)
    assert parent is None and len(sample["A"]) == 50
    assert stats["dropped"] > 0 and stats["drawn"] - stats["dropped"] >= 50
    _, _, keep = mocks.observe(np.full(2000, 19.999), np.full(2000, 1000.0), "rtau", np.random.default_rng(9))
    assert 0 < (~keep).sum() < 2000


def test_err_params_sets_and_key():
    P = run.PARAMS
    assert P["err_f"] == [1.2, 1.5, 2.0, 2.81] and P["err_bins"] == [0, 1, 2] and P["err_n_mock"] == 50
    assert P["err_reach_frac"] == 0.05 and P["err_min_bins"] == 2
    assert P["err_seed_tag"] == 54 and P["err_seed_tag_indep"] == 154 and P["err_stop_h"] == 16.0
    assert "err_stop_h" in selaux.NO_KEY_PARAMS and "parts" in selaux.NO_KEY_PARAMS
    sets = selaux.err_sets(P["err_f"], P["err_bins"], P["mechs"])
    assert len(sets) == 72 and [s["k"] for s in sets] == list(range(72))
    nest = [(f, v, b, m) for f in P["err_f"] for v in ("S15E", "S15N", "Full") for b in (0, 1, 2) for m in ("rtau", "rA")]
    assert [(s["f"], s["variant"], s["bin"], s["mech"]) for s in sets] == nest
    assert len({s["group"] for s in sets}) == 12                     # (variant, f) projection groups
    assert all(s["kind"] == "power" and s["floor"] == "primary" for s in sets)
    src = {"run.py": "x"}
    k0 = selaux.checkpoint_key(dict(P), src, b"d")
    assert selaux.checkpoint_key({**P, "err_stop_h": 30.0, "parts": ["orig"]}, src, b"d") == k0
    assert selaux.checkpoint_key({**P, "err_f": [1.2]}, src, b"d") != k0
    text = (HERE / "run.py").read_text(encoding="utf-8")
    assert selaux.strip_params(text.replace('"err_stop_h": 16.0', '"err_stop_h": 20.0')) == selaux.strip_params(text)


def test_err_parts_validation(monkeypatch):
    for bad in (["err", "selfit"], ["orig", "err"], ["sel", "err"]):
        monkeypatch.setitem(run.PARAMS, "parts", bad)
        with pytest.raises(ValueError):
            run.main(None)


def test_clopper_pearson_and_counts():
    lo, hi = selaux.clopper_pearson(0, 50)
    assert lo == 0.0 and hi == pytest.approx(0.0711, abs=5e-4)
    lo, hi = selaux.clopper_pearson(3, 50)
    assert lo == pytest.approx(0.0125, abs=5e-4) and hi == pytest.approx(0.1655, abs=5e-4)
    assert selaux.clopper_pearson(50, 50)[1] == 1.0
    # a mock without a valley (d = 1 sentinel) is never in n_reach
    assert selaux.err_counts([1.0, 0.5, 0.3, None], [False, True, True, None], 0.4) == (1, 1)
    assert selaux.err_counts([0.4], [True], 0.4) == (1, 0)                    # d >= data d counts
    assert not selaux.err_explainable({"rtau": 2, "rA": 2}, 50, 0.05)
    assert selaux.err_explainable({"rtau": 0, "rA": 3}, 50, 0.05)              # one mechanism suffices
    assert not selaux.err_explainable({"rtau": 24, "rA": 0}, 50, 0.5)
    assert selaux.err_explainable({"rtau": 25, "rA": 0}, 50, 0.5)


LAD = [1.2, 1.5, 2.0, 2.81]
NAMES = {f: [] for f in LAD}


@pytest.mark.parametrize("E, cut_f, kw, want", [
    # 1-3: the "not evaluable" cases, in order of precedence
    ({f: 0 for f in LAD}, None, {"reproduction_ok": False, "nonfinite": True}, "not evaluable (reproduction)"),
    ({f: 0 for f in LAD}, 1.2, {"nonfinite": True}, "not evaluable (non-finite)"),
    ({1.2: None, 1.5: None, 2.0: None, 2.81: None}, 1.2, {}, "not evaluable (infeasible)"),
    # 4: sensitive at the smallest feasible f with E >= 2
    ({1.2: 0, 1.5: 0, 2.0: 2, 2.81: 3}, None, {}, "sensitive at f = 2.0"),
    ({1.2: 1, 1.5: 2, 2.0: 1, 2.81: 3}, None, {}, "sensitive at f = 1.5"),
    ({1.2: 0, 1.5: 2, 2.0: None, 2.81: None}, 2.0, {}, "sensitive at f = 1.5"),   # no ladder-end qualifier
    # 5: robust, with the qualifiers
    ({f: 0 for f in LAD}, None, {}, "robust up to f = 2.81"),
    ({1.2: 0, 1.5: 0, 2.0: 1, 2.81: 1}, None, {}, "robust up to f = 1.5 (one bin explainable from f = 2.0: [-0.3, -0.1))"),
    ({1.2: 1, 1.5: 0, 2.0: 0, 2.81: 1}, None, {}, "robust up to f = 1.0 (one bin explainable from f = 1.2: [-0.3, -0.1))"),
    ({1.2: 0, 1.5: 0, 2.0: None, 2.81: None}, 2.0, {}, "robust up to f = 1.5 (ladder ends at f = 1.5)"),
    ({1.2: 0, 1.5: 1, 2.0: None, 2.81: None}, 2.0, {},
     "robust up to f = 1.2 (one bin explainable from f = 1.5: [-0.3, -0.1); ladder ends at f = 1.5)"),
    ({1.2: 0, 1.5: 0, 2.0: 0, 2.81: None}, 2.81, {}, "robust up to f = 2.0 (ladder ends at f = 2.0)"),
])
def test_err_label_cases(E, cut_f, kw, want):
    names = {f: (["[-0.3, -0.1)"] if E.get(f) == 1 else []) for f in LAD}
    lab = selaux.err_label(LAD, E, cut_f, names, **kw)
    assert lab["label"] == want


def test_err_label_details():
    lab = selaux.err_label(LAD, {1.2: 0, 1.5: 1, 2.0: 2, 2.81: 3}, None, {1.5: ["a"], 2.0: ["a", "b"]})
    assert lab["case"] == 4 and lab["Y"] == 2.0 and lab["W3"] == 2.81
    assert lab["all_bins_explainable_from"] == "all three bins explainable from f = 2.81"
    lab = selaux.err_label(LAD, {1.2: 0, 1.5: 1, 2.0: 1, 2.81: 1}, None, {1.5: ["a"], 2.0: ["b"], 2.81: ["a"]})
    assert lab["case"] == 5 and lab["X"] == 1.2 and lab["Z"] == 1.5 and lab["Z_bins"] == ["a", "b"] and lab["W3"] is None
    # variant labels (S15 term N / Full): an f with a generator failure is named and skipped
    lab = selaux.err_label(LAD, {1.2: 0, 1.5: None, 2.0: 0, 2.81: 0}, None, NAMES, not_evaluable=[1.5])
    assert lab["label"] == "robust up to f = 2.81 (not evaluable at f = 1.5)"
    lab = selaux.err_label(LAD, {1.2: None, 1.5: 2, 2.0: 0, 2.81: 0}, None, NAMES, not_evaluable=[1.2])
    assert lab["label"] == "sensitive at f = 1.5 (not evaluable at f = 1.2)"


def _fake_rfit(nbins=5, d_data=(0.41, 0.58, 0.50, 1.0, 1.0)):
    def mk(k):
        return {"k": k, "d": [0.01] * 50, "valley": [True] * 50}
    out = {"variants": {}}
    for i, v in enumerate(selaux.R1_VARIANTS):
        out["variants"][v] = {"bins": [{"d": d_data[b], "resolvable": b < 3, "almost_disjoint": False, "edge": None,
                                        "power_model": {"valid": True},
                                        "mocks": {"power_rtau": mk(30 * i + 6 * b + 4), "power_rA": mk(30 * i + 6 * b + 5)}}
                                       for b in range(nbins)]}
    return out


def _fake_results(sets, reach, fail=None, nmock=50):
    """reach(s) -> number of mocks with a valley and d = 0.9 (>= every data d); the rest have a valley and
    d = 0.01, except 5 without a valley. fail(s) -> index of the mock with a generator failure, or None."""
    res = {}
    for s in sets:
        n = reach(s)
        rr = []
        for j in range(nmock):
            if fail is not None and fail(s) == j:
                rr.append({"gen_fail": True, "d": None, "valley": None, "k": None, "pass_rate": None,
                           "dropped": 0, "drawn": 10})
                continue
            d, v = (0.9, True) if j < n else ((1.0, False) if j >= nmock - 5 else (0.01, True))
            rr.append({"gen_fail": False, "d": d, "valley": v, "k": 3, "pass_rate": 0.9, "dropped": 0, "drawn": 4000,
                       "i_used_k1": False, "i_used_k2": True, "i_used_k3": False, "i_used_k4": False, "i_used_k5": -1,
                       "nonmonotone": 0, "o_nonmonotone": 1, "age_p5": 5.0, "age_p50": 9.0, "age_p95": 13.0})
        res[s["k"]] = rr
    return res


def _evaluate(reach, fail=None, cut_from=None):
    P = dict(run.PARAMS)
    sets = selaux.err_sets(P["err_f"], P["err_bins"], P["mechs"])
    res = _fake_results(sets, reach, fail)
    if cut_from is not None:                           # sets the runner would not have finished
        for s in sets:
            if s["f"] >= cut_from[0] and s["k"] > cut_from[1]:
                res[s["k"]] = []
    times = {s["k"]: [1.0] * len(res[s["k"]]) for s in sets}
    return run.err_evaluate(P, sets, res, times, _fake_rfit(), {}, {"R1_0": 0.8, "R1_1": 0.8, "R1_2": 0.8})


def test_err_evaluate_robust_and_sensitive():
    out = _evaluate(lambda s: 0)
    assert out["label"]["label"] == "robust up to f = 2.81" and out["cut_f"] is None
    assert out["f1_row"]["S15E"]["E"] == 0
    ps = out["per_set"][0]
    assert ps["n_reach"] == 0 and ps["n_novalley"] == 5 and ps["n_d_ge_data_incl_novalley"] == 5
    assert ps["frac_valley"] == 0.9 and ps["power_at_d_cap"] == 0.9 and ps["k_chosen"]["3"] == 50
    assert ps["d_pct_5_50_80_95"][1] == 0.01 and ps["mean_pass_rate"] == 0.9 and ps["data_pass_frac"] == 0.8
    assert out["variants"]["S15E"]["per_f"]["1.2"]["r1_verdict_at_f"] == "not reproduced"
    # 3 of 50 under one mechanism in bins 1 and 2 from f = 2.0 on: sensitive at 2.0
    out = _evaluate(lambda s: 3 if (s["f"] >= 2.0 and s["bin"] > 0 and s["mech"] == "rA") else 2)
    assert out["label"]["label"] == "sensitive at f = 2.0"
    assert out["variants"]["S15E"]["per_f"]["2.0"]["explainable_bins"] == ["[-0.5, -0.3)", "[-0.3, -0.1)"]
    assert out["label_median_rule"]["label"] == "robust up to f = 2.81"
    # median rule: 25 of 50 needed
    out = _evaluate(lambda s: 25 if (s["f"] >= 1.5 and s["bin"] == 2) else 0)
    assert out["label"]["label"].startswith("robust up to f = 1.2 (one bin explainable from f = 1.5: [-0.3, -0.1)")
    assert out["label_median_rule"]["label"] == out["label"]["label"]
    # a power below 0.8 under one mechanism makes the bin not resolvable in the R1 verdict at f
    out = _evaluate(lambda s: 45 if s["bin"] == 0 and s["mech"] == "rA" else 0)
    assert out["variants"]["S15E"]["per_f"]["1.2"]["r1_verdict_at_f"] == "undetermined"


def test_err_evaluate_feasibility():
    # a generator failure in an S15E set at f = 2.0 cuts the ladder there
    fail = lambda s: 7 if (s["variant"] == "S15E" and s["f"] == 2.0 and s["bin"] == 1 and s["mech"] == "rtau") else None
    out = _evaluate(lambda s: 0, fail, cut_from=(2.0, 39))
    assert out["cut_f"] == 2.0 and out["feasible"] == {"1.2": True, "1.5": True, "2.0": False, "2.81": False}
    assert out["label"]["label"] == "robust up to f = 1.5 (ladder ends at f = 1.5)"
    assert out["variants"]["S15N"]["per_f"]["2.0"]["status"] == "not feasible"
    # a failure at f = 1.2 in S15E: not evaluable (infeasible)
    out = _evaluate(lambda s: 0, lambda s: 0 if s["k"] == 0 else None, cut_from=(1.2, 0))
    assert out["label"]["label"] == "not evaluable (infeasible)"
    # a failure in a term N set does not cut: that variant is not evaluable at f, the primary is unchanged
    out = _evaluate(lambda s: 0, lambda s: 3 if (s["variant"] == "S15N" and s["f"] == 1.5 and s["k"] % 6 == 0) else None)
    assert out["cut_f"] is None and out["label"]["label"] == "robust up to f = 2.81"
    assert out["variants"]["S15N"]["per_f"]["1.5"]["status"] == "not evaluable at f"
    assert out["variants"]["S15N"]["label"]["label"] == "robust up to f = 2.81 (not evaluable at f = 1.5)"
    # an incomplete set at a feasible f is an error, not a label
    with pytest.raises(RuntimeError):
        _evaluate(lambda s: 0, cut_from=(2.81, 70))
    # non-finite results in a set used for the label
    P = dict(run.PARAMS)
    sets = selaux.err_sets(P["err_f"], P["err_bins"], P["mechs"])
    res = _fake_results(sets, lambda s: 0)
    res[3][4]["d"] = float("nan")
    out = run.err_evaluate(P, sets, res, {}, _fake_rfit(), {}, {})
    assert out["label"]["label"] == "not evaluable (non-finite)"


def test_run_mock_sets_cut_stops_larger_f(tmp_path):
    """README 2.7 feasibility: after a generator failure in an S15E set, no set at that f or a larger one
    is run; earlier sets are complete; a replay from the checkpoints makes the same cut."""
    sets = selaux.err_sets([1.2, 1.5, 2.0], [0], ["rtau"])         # 9 sets: k = 3 is S15E at f = 1.5
    calls = []

    def run_one(s, rng):
        calls.append(s["k"])
        j = len([c for c in calls if c == s["k"]]) - 1
        if s["k"] == 3 and j == 2:
            return {"gen_fail": True, "d": None, "valley": None, "k": None, "pass_rate": None}
        return {"gen_fail": False, "d": 0.01, "valley": True, "k": 3, "pass_rate": None}
    mk = lambda k, j: selaux.mock_rng(0, 54, k, j)
    st = selaux.MockStore(tmp_path, "cut")
    res, state, log = selaux.run_mock_sets(sets, 5, st, run_one, mk, 16.0, log=lambda m: None, cut=run.err_cut)
    st.release()
    assert [len(res[k]) for k in range(9)] == [5, 5, 5, 3, 1, 1, 1, 1, 1]
    assert log[-1]["mocks_left"] == 0
    st2 = selaux.MockStore(tmp_path, "cut")
    res2, _, _ = selaux.run_mock_sets(sets, 5, st2, lambda s, g: (_ for _ in ()).throw(AssertionError("recomputed")),
                                      mk, 16.0, log=lambda m: None, cut=run.err_cut)
    st2.release()
    assert res2 == res
    # a failure in a term N set does not cut
    calls.clear()

    def run_n(s, rng):
        calls.append(s["k"])
        return {"gen_fail": s["k"] == 4, "d": None if s["k"] == 4 else 0.01, "valley": None, "k": None, "pass_rate": None}
    st3 = selaux.MockStore(tmp_path, "cut2")
    res3, _, _ = selaux.run_mock_sets(sets, 3, st3, run_n, mk, 16.0, log=lambda m: None, cut=run.err_cut)
    st3.release()
    assert all(len(res3[k]) == 3 for k in range(9))


def test_r1_mock_err_f1_equals_selfit_and_generator_failure(monkeypatch):
    C = run.Ctx(dict(run.PARAMS))
    D, pools = _synthetic_D(C)
    ref = run.r1_mock_selfit(C, D, "power", "rtau", "primary", (np.random.default_rng(5), np.random.default_rng(6)), pools, 8)
    new = run.r1_mock_err(C, D, "rtau", (np.random.default_rng(5), np.random.default_rng(6)), pools, 8, 1.0)
    assert {k: new[k] for k in ref} == ref and new["gen_fail"] is False
    assert new["drawn"] >= D["_n"] and new["dropped"] >= 0 and new["age_p5"] < new["age_p50"] < new["age_p95"]
    assert selaux._jsonable_result(new) == new and not selaux.nonfinite(new)
    big = run.r1_mock_err(C, D, "rA", (np.random.default_rng(5), np.random.default_rng(6)), pools, 8, 2.81)
    assert big["gen_fail"] is False and big["age_p95"] - big["age_p5"] > 0

    def boom(*a, **k):
        raise RuntimeError("catalogue_sel: selection rate too low")
    monkeypatch.setattr(run.mocks, "catalogue_sel", boom)
    bad = run.r1_mock_err(C, D, "rtau", (np.random.default_rng(5), np.random.default_rng(6)), pools, 8, 2.0)
    assert bad["gen_fail"] is True and bad["d"] is None and selaux._jsonable_result(bad) == bad


def test_err_generator_check_flags_differences():
    P = dict(run.PARAMS)
    rfit = _fake_rfit()
    rec = lambda v, b, mech, k: {"d": 0.01, "valley": True, "gen_fail": False}
    g = run.err_generator_check(P, rfit, rec)
    assert g["n"] == 18 and g["mismatches"] == []
    assert [r["k"] for r in g["rows"][:2]] == [4, 5]               # R1-SEL-FIT set numbers (SEL-8)
    off = lambda v, b, mech, k: {"d": 0.01 + (2e-9 if (v, b, mech) == ("Full", 2, "rA") else 0), "valley": True}
    assert run.err_generator_check(P, rfit, off)["mismatches"] == [["Full", 2, "rA"]]
    gf = lambda v, b, mech, k: {"gen_fail": True, "d": None, "valley": None}
    assert len(run.err_generator_check(P, rfit, gf)["mismatches"]) == 18
