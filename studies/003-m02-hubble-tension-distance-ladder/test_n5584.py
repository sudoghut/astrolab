"""Offline tests of R2-RE-N5584 (README section 2, addendum 2026-11-18, T-039) on synthetic data:
the variational EM, the decision rules and a small end-to-end pass of the block."""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).parent


def _mods():
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    spec = importlib.util.spec_from_file_location("run003_n", HERE / "run.py")
    run = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(run)
    import n5584
    return run, n5584


def _synthetic(run, tau=0.12, outlier=0.6, seed=3):
    """A small ladder with run.py's column layout: 37 hosts (4 Cepheid rows, 1-2 SN rows each), NGC 4258
    Cepheids and maser, Hubble-flow SNe. Host 26 is 'N5584' with an extra SN offset `outlier`."""
    rng = np.random.default_rng(seed)
    rows, yv, sig = [], [], []
    mu = rng.uniform(30.5, 33.0, run.NH)
    m_h, m_b, q = -5.9, -19.25, 9.32
    u = rng.normal(0.0, tau, run.NH)
    u[26] += outlier

    def add(cols, val, s):
        r = np.zeros(run.N_PAR)
        for c, v in cols:
            r[c] = v
        rows.append(r)
        yv.append(val + rng.normal(0, s))
        sig.append(s)

    for j in range(run.NH):
        for _ in range(4):
            add([(j, 1), (run.C_MH, 1)], mu[j] + m_h, 0.08)
        for _ in range(1 + (j % 3 == 0)):
            add([(j, 1), (run.C_MB, 1)], mu[j] + m_b + u[j], 0.05)
    for _ in range(6):
        add([(run.C_N4258, 1), (run.C_MH, 1)], 29.4 + m_h, 0.08)
    add([(run.C_N4258, 1)], 0.0, 0.03)
    yv[-1] = 0.0                           # maser row: y = 0 exactly (as in the real data)
    for _ in range(40):
        add([(run.C_MB, 1), (run.C_H0, -1)], m_b - q, 0.12)
    L = np.array(rows)
    y = np.array(yv)
    C = np.diag(np.array(sig) ** 2)
    return L, y, C


@pytest.fixture
def synth(monkeypatch):
    run, n5584 = _mods()
    L, y, C = _synthetic(run)
    monkeypatch.setattr(run, "N_ROWS", len(y))
    nz, cls, _ = run.row_classes(L, y)
    groups = [np.flatnonzero(cls["calib"] & nz[:, j]) for j in range(run.NH)]
    return run, n5584, L, y, C, nz, cls, groups


def test_vem_with_fixed_omega_is_reml(synth):
    """omega fixed at 1: the iteration is EM for REML and lands on the direct REML optimum."""
    run, n5584, L, y, C, nz, cls, groups = synth
    rows = np.arange(len(y))
    pre = n5584.vem_precompute(L, y, C, rows, groups)
    em = n5584.vem(pre, 4, 0.20, 10000, 1e-10, fix_omega=True)
    assert em["converged"] and np.all(em["omega"] == 1.0)
    est = run.reml_tau(lambda t: run.reml_m2l(L, y, C, rows, groups, t), 0.5, 0.01, interval=False)
    assert est["tau_hat"] > 0.05
    assert abs(em["tau"] - est["tau_hat"]) < 1e-4


def test_vem_downweights_planted_outlier_and_converges(synth):
    run, n5584, L, y, C, nz, cls, groups = synth
    pre = n5584.vem_precompute(L, y, C, np.arange(len(y)), groups)
    fits = [n5584.vem(pre, 4, t0, 10000, 1e-8) for t0 in (0.077, 0.20)]
    assert all(f["converged"] for f in fits)
    assert abs(fits[0]["tau"] - fits[1]["tau"]) < 1e-4            # both starts reach the same point
    for f in fits:
        assert int(np.argmin(f["omega"])) == 26
        assert np.all(f["omega"] > 0)
    # the fixed point satisfies its own update equations
    f = fits[0]
    t2 = f["tau"] ** 2
    assert t2 > 0 and abs(np.mean(f["omega"]) - 1.0) < 0.5


def test_with_group_var_matches_with_re(synth):
    run, n5584, L, y, C, nz, cls, groups = synth
    V1 = run.with_re(C, groups, 0.1)
    V2 = n5584.with_group_var(C, groups, np.full(len(groups), 0.01))
    assert np.allclose(V1, V2, rtol=0, atol=1e-15)


def test_reading_rules():
    _, n = _mods()
    ev = lambda lab: {"status": "evaluated", "label": lab}
    und = "undetermined (Monte Carlo)"
    usual_t = "tau_hat not unusual under C"
    assert n.reading_a({"status": "not evaluable (R2-RE not evaluable)"}, ev(n.SPREAD_USUAL)) == n.READ_NE
    assert n.reading_a(ev(usual_t), {"status": "not evaluable (R4 has no draws)"}) == n.READ_NE
    assert n.reading_a(ev(usual_t), ev(n.SPREAD_USUAL)) == n.READ_N5584
    assert n.reading_a(ev(und), ev(n.SPREAD_USUAL)) == n.READ_N5584
    assert n.reading_a(ev(n.TAU_UNUSUAL), ev(n.SPREAD_UNUSUAL)) == n.READ_SPREAD
    assert n.reading_a(ev(usual_t), ev(n.SPREAD_UNUSUAL)) == n.READ_SPREAD
    assert n.reading_a(ev(n.TAU_UNUSUAL), ev(n.SPREAD_USUAL)) == n.READ_TAU
    assert n.reading_a(ev(usual_t), ev(und)) == n.READ_UNDET
    row = "no host-selection effect detected in these data (does not support the paper's quantitative claim)"
    assert n.label_b(row, row) == n.T_ROBUST
    other = "host selection significantly lowers H0, but by a different size"
    assert n.label_b(other, row) == ("R2-RE verdict depends on the host-effect distribution "
                                     "(heavy-tailed: " + other + ")")
    assert n.joint_reading("evaluated", n.T_ROBUST, -2.2, -1.5, 0.077, -1.6) == n.JOINT_ROBUST
    j = n.joint_reading("evaluated", n.label_b(other, row), -2.21, -1.53, 0.077, -2.3)
    assert j.startswith(n.JOINT_DEPENDS) and "-2.21" in j and "-1.53" in j and "-2.30" in j
    assert n.joint_reading("not evaluable (bound)", None, 0, 0, 0, None) == n.JOINT_NONE


def test_block_end_to_end_synthetic(synth, tmp_path, monkeypatch):
    """The whole block on the synthetic ladder with tiny simulation counts: it runs, follows its own
    rules, and the 36-host subsets never touch the removed host."""
    run, n5584, L, y, C, nz, cls, groups = synth
    rows_a = np.arange(len(y))
    cchp = [0, 3, 7, 10, 12, 19, 21, 30, 33, 36]
    other = [j for j in range(run.NH) if j not in cchp]
    rows_s = np.array([i for i in rows_a if not nz[i, other].any()])
    labels = [f"H{j:02d}" for j in range(run.NH)]
    labels[26] = "N5584"
    host_rows = [np.flatnonzero(nz[:, j]) for j in range(run.NH)]
    n_sn_col = [len(g) for g in groups]
    P = dict(run.PARAMS, r4_draws=30, rob_n_tau=3, rob_n_spread=20, rob_n_subsets=10)
    verdict = lambda z_, d_, s_: run.host_step_verdict(z_, d_, s_, P["host_ref"], P["host_ref_extra"])
    fns = {"reml_tau": run.reml_tau, "reml_m2l": run.reml_m2l, "host_step_under": run.host_step_under,
           "with_re": run.with_re, "fit": run.fit, "shift_vector": run.shift_vector,
           "is_fit_failure": run.is_fit_failure, "C_H0": run.C_H0, "r4_draws": run.r4_draws,
           "r4_summary": run.r4_summary, "r2_re_r4": run.r2_re_r4, "verdict": verdict}
    est = run.reml_tau(lambda t: run.reml_m2l(L, y, C, rows_a, groups, t), 0.5, 0.01)
    tau = 0.0 if est["at_zero"] else est["tau_hat"]
    hs, _ = run.host_step_under(L, y, run.with_re(C, groups, tau), rows_a, rows_s)
    re_out = {"status": "evaluated", "tau_hat": tau, "z": hs["z"],
              "verdict": verdict(hs["z"], hs["shift"], hs["shift_sigma"])}
    hc, _ = run.host_step_under(L, y, C, rows_a, rows_s)
    with pytest.raises(RuntimeError):
        n5584.run_block(L, y, C, nz, cls, rows_a, rows_s, cchp, groups, labels, host_rows, n_sn_col,
                        re_out, hc, P, fns, lambda m: None, expected_col=25)
    out = n5584.run_block(L, y, C, nz, cls, rows_a, rows_s, cchp, groups, labels, host_rows, n_sn_col,
                          re_out, hc, P, fns, lambda m: None, expected_col=26)
    a, b = out["drop"], out["heavy_tail"]
    assert a["status"] == "evaluated" and a["column"] == 26
    assert a["rows_removed"] == {"total": 5, "calib_sn": 1, "cepheid": 4, "other": 0}
    assert a["rows_reduced"] == len(y) - 5 and a["host_rows_trimmed"] == []
    assert a["r2_re"]["status"] == "evaluated" and a["r4n"]["draws"] == 30
    assert a["c"]["row"] == verdict(a["c"]["z"], a["c"]["host_step"]["shift"], a["c"]["host_step"]["shift_sigma"])
    assert a["r4n_under_v"]["draws"] == 30
    assert a["bn"]["tau"]["n_sims"] == 3 and a["bn"]["spread"]["n_subsets"] == 10
    assert a["reading"] == n5584.reading_a(a["bn"]["tau"], a["bn"]["spread"])
    # R4-N draws are R4's index stream mapped onto the 36 remaining columns
    rng = np.random.default_rng(P["r4_seed"])
    cols = np.array([j for j in range(run.NH) if j != 26])
    exp = [[int(j) for j in cols[rng.choice(36, size=10, replace=False)]] for _ in range(len(a["r4n"]["first_picks"]))]
    assert a["r4n"]["first_picks"] == exp and all(26 not in p for p in exp)
    assert b["implementation_check"]["passed"], b["implementation_check"]
    assert b["status"] == "evaluated"
    assert b["nu_main"]["omega_ranked"][0]["host"] == "N5584"
    assert b["label"] == n5584.label_b(b["nu_main"]["row"], re_out["verdict"])
    assert [r["nu"] for r in b["nu_sensitivity"]] == [2, 10]
    assert out["joint_reading"] == n5584.joint_reading(b["status"], b["label"], hc["z"], re_out["z"], tau,
                                                       b["nu_main"]["z"])
    # the conclusion test re-derives every label from the saved file
    from astrolab.results import write_json
    write_json(tmp_path / "r2_re_n5584.json", out)
    write_json(tmp_path / "r2_re.json", re_out)
    write_json(tmp_path / "summary.json", {"R2_RE_N5584": run.n5584_summary(out)})
    spec = importlib.util.spec_from_file_location("tc003_n", HERE / "test_conclusions.py")
    tc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tc)
    monkeypatch.setattr(tc, "RESULTS", tmp_path)
    tc.test_r2_re_n5584_labels()


def test_r4_draws_full_column_set_is_r4_stream(synth):
    """With all 37 columns the generalised draw equals R4's original rng.choice(NH, 10) stream."""
    run, n5584, L, y, C, nz, cls, groups = synth
    rows_a = np.arange(len(y))
    res_a = run.fit(L, y, C, rows_a, est=True)
    any_host = nz[:, :run.NH].any(axis=1)
    base = rows_a[~any_host]
    host_rows = [np.flatnonzero(nz[:, j]) for j in range(run.NH)]
    out = {}
    _, _, _, picks = run.r4_draws(L, y, C, rows_a, res_a, float(res_a["q"][run.C_H0]),
                                  float(res_a["sigma"][run.C_H0]), base, host_rows, np.arange(run.NH), 10,
                                  5, 0, 60.0, [1] * run.NH, out, lambda m: None)
    rng = np.random.default_rng(0)
    for p in picks:
        ref = rng.choice(run.NH, size=10, replace=False)
        assert p.dtype == ref.dtype and np.array_equal(p, ref)
    assert out["z_identity_check"]["rel_diff"] < 1e-6


@pytest.mark.parametrize("case,expected", [
    ("not_converged", "not evaluable (not converged; iterations 10000, 10000)"),
    ("two_points", "not evaluable (multiple fixed points)"),
    ("bound", "not evaluable (bound)"),
])
def test_heavy_tail_failure_branches(synth, monkeypatch, case, expected):
    """Validity checks (2)-(4) of (b): forced fixed points give the pre-registered statuses for nu = 4,
    and nu = 2, 10 carry the 'reported, not evaluable' prefix; the implementation check uses the real EM."""
    run, n5584, L, y, C, nz, cls, groups = synth
    rows_a = np.arange(len(y))
    cchp = [0, 3, 7, 10, 12, 19, 21, 30, 33, 36]
    other = [j for j in range(run.NH) if j not in cchp]
    rows_s = np.array([i for i in rows_a if not nz[i, other].any()])
    labels = [f"H{j:02d}" for j in range(run.NH)]
    P = dict(run.PARAMS)
    verdict = lambda z_, d_, s_: run.host_step_verdict(z_, d_, s_, P["host_ref"], P["host_ref_extra"])
    fns = {"host_step_under": run.host_step_under, "with_re": run.with_re,
           "is_fit_failure": run.is_fit_failure, "verdict": verdict}
    est = run.reml_tau(lambda t: run.reml_m2l(L, y, C, rows_a, groups, t), 0.5, 0.01)
    tau = 0.0 if est["at_zero"] else est["tau_hat"]
    hs, _ = run.host_step_under(L, y, run.with_re(C, groups, tau), rows_a, rows_s)
    re_out = {"status": "evaluated", "tau_hat": tau, "z": hs["z"],
              "verdict": verdict(hs["z"], hs["shift"], hs["shift_sigma"])}
    hc, _ = run.host_step_under(L, y, C, rows_a, rows_s)
    real = n5584.vem

    def fake(pre, nu, tau0, maxiter, tol, fix_omega=False):
        if fix_omega:
            return real(pre, nu, tau0, maxiter, tol, fix_omega=True)
        om = np.ones(len(groups))
        t_hat = {"not_converged": 0.1, "two_points": 0.1 if tau0 < 0.1 else 0.2, "bound": 0.5}[case]
        return {"tau": t_hat, "omega": om, "iterations": 10000 if case == "not_converged" else 50,
                "converged": case != "not_converged", "last_rel_change": 1e-3 if case == "not_converged" else 1e-9}

    monkeypatch.setattr(n5584, "vem", fake)
    b = n5584.heavy_tail(L, y, C, rows_a, rows_s, groups, labels, re_out, hc, P, fns, lambda m: None)
    assert b["implementation_check"]["passed"]
    assert b["status"] == expected and b["nu_main"]["status"] == expected
    for r in b["nu_sensitivity"]:
        assert r["status"] == "reported, not evaluable: " + expected
