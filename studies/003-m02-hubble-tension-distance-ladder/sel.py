"""R2-RE-SEL (README section 2, addendum 2026-11-19, T-042): a selection-aware null for the removal of
N5584.

Simulate the full 37-host NGC 4258-only system under C (y_s = y_hat + K eps_s, eps_s from
default_rng(sel_seed_base + s)), drop the most extreme host by a fixed criterion, and only then compute
tau_hat (criterion X) and the R4-N-style subset spread (criteria X and S) on the remaining 36 hosts.

- Criterion X: the raw leave-one-host-out chi^2 term under C (run.loo_chi2), argmax over the 37 hosts,
  ties to the lowest column; evaluated per simulation through precomputed linear maps y[rows_a] -> r_j
  and S_j^-1, which must reproduce loo_chi2 on the real y to a relative 1e-8.
- Criterion S: the spread of Delta_k / sigma_k over R2-RE-ROB part B's subsets (the first n_subsets R4
  draws on the 37-host system under C) that do not contain host j, argmin over j, ties to the lowest
  column.

run.py passes its own functions in (`fns`); this module does not import run (AGENTS.md section 2).
"""
import time
from collections import Counter

import numpy as np
from scipy import linalg

import rob

# Values recorded before the addendum (README section 2, R2-RE-SEL "Observed values" and criterion S).
RECORDED_TAU_N = 0.03137144323410943
RECORDED_SPREAD_OBS = 1.0325254787240916
TAU_N_RTOL = 1e-6
SPREAD_RTOL = 1e-9
LOO_RTOL = 1e-8
CRIT_S_EXPECTED = 1.027
CRIT_S_TOL = 0.001

UNDET_MC = "undetermined (Monte Carlo)"
TAU_UNUSUAL = "τ̂_N unusual under the selected null"
TAU_USUAL = "τ̂_N not unusual under the selected null"
SPREAD_UNUSUAL = "the 36-host spread is unusual under the selected null ({c})"
SPREAD_USUAL = "the 36-host spread is consistent with the selected null ({c})"

READ_NE = "not evaluable"
READ_CONSISTENT = ("the excess calibrator scatter of R2-RE-ROB is consistent with one outlying host, "
                   "selection included")
READ_SPREAD = ("excess scatter remains after removing the most extreme host, selection included "
               "(criterion {c})")
READ_TAU = "τ excess remains after removing the most extreme host, selection included"
READ_UNDET = "undetermined"

BLOCK_NE_OBSERVED = "not evaluable (observed values differ from the recorded ones: code or data change)"
BLOCK_NE_CONFIG = ("not evaluable (configuration: sel_n_subsets = {a} differs from rob_n_subsets = {b}; "
                   "B-N's spread_obs uses rob_n_subsets)")

SECTION5 = {
    "consistent": ("the post-hoc gloss 'consistent with one outlying host' becomes the pre-registered "
                   "reading of this test, quoted with the caveat that the tau part uses criterion X only "
                   "(its p expected to be higher than under an aligned criterion)"),
    "withdrawn": ("the gloss is withdrawn; section 5 states that the excess calibrator scatter is not "
                  "accounted for by removing the single most extreme host once that choice is simulated "
                  "('attributable to N5584' stays recorded as the outcome under the unselected null)"),
    "stays": "the gloss stays, marked post hoc, with this outcome next to it",
}


# ---------------------------------------------------------------- decision rules (pure)
def tau_label(k, n):
    return rob.three_way(k, n, TAU_UNUSUAL, TAU_USUAL)


def spread_label(k, n, crit):
    return rob.three_way(k, n, SPREAD_UNUSUAL.format(c=crit), SPREAD_USUAL.format(c=crit))


def reading(tau_rec, sx_rec, ss_rec):
    """Rules (1)-(5), checked in the pre-registered order."""
    recs = (tau_rec, sx_rec, ss_rec)
    if not all(r.get("status") == "evaluated" for r in recs):                       # (1)
        return READ_NE
    t, sx, ss = tau_rec["label"], sx_rec["label"], ss_rec["label"]
    cons_x, cons_s = sx == SPREAD_USUAL.format(c="X"), ss == SPREAD_USUAL.format(c="S")
    unu_x, unu_s = sx == SPREAD_UNUSUAL.format(c="X"), ss == SPREAD_UNUSUAL.format(c="S")
    if cons_x and cons_s and t != TAU_UNUSUAL:                                        # (2)
        return READ_CONSISTENT
    if unu_x or unu_s:                                                                # (3)
        return READ_SPREAD.format(c="both" if (unu_x and unu_s) else ("X" if unu_x else "S"))
    if cons_x and cons_s and t == TAU_UNUSUAL:                                        # (4)
        return READ_TAU
    return READ_UNDET                                                                 # (5)


def section5_action(read):
    """What the reading changes in section 5 (the text, not any label)."""
    if read == READ_CONSISTENT:
        return SECTION5["consistent"]
    if read == READ_TAU or read.startswith(READ_SPREAD.split("(criterion")[0]):
        return SECTION5["withdrawn"]
    return SECTION5["stays"]


def not_lowered(p_sel, p_bn):
    """Descriptive only: True when the selected-null p is not below B-N's (same run); None if either
    is missing."""
    if p_sel is None or p_bn is None:
        return None
    return bool(p_sel >= p_bn)


def observed_mismatches(tau_obs, spread_obs, rec_tau, rec_spread):
    """Observed values against the recorded ones (tau_hat_N relative 1e-6, spread_obs relative 1e-9);
    a value that is not available (None) is not checked."""
    bad = []
    if tau_obs is not None and not abs(tau_obs - rec_tau) <= TAU_N_RTOL * abs(rec_tau):
        bad.append(f"tau_hat_N {tau_obs!r} vs recorded {rec_tau!r}")
    if spread_obs is not None and not abs(spread_obs - rec_spread) <= SPREAD_RTOL * abs(rec_spread):
        bad.append(f"spread_obs {spread_obs!r} vs recorded {rec_spread!r}")
    return bad


def pick_max(values):
    """Criterion X's host: argmax over the 37 hosts, ties to the lowest column."""
    return int(np.argmax(values))


def pick_min(values):
    """Criterion S's host: argmin over the 37 hosts, ties to the lowest column."""
    return int(np.nanargmin(values))


# ---------------------------------------------------------------- structures
def reduced_system(nz, rows_a, d, groups, host_rows):
    """`rows_a` without every row with a non-zero in column d, as in n5584.drop_host but without its
    CCHP guard (d may be a CCHP host; the host step and rows_s are not used here)."""
    rows_a = np.asarray(rows_a)
    nh = len(groups)
    rows_n = rows_a[~nz[rows_a, d]]
    any_host = nz[:, :nh].any(axis=1)
    base_n = np.array([i for i in rows_n if not any_host[i]])
    host_rows_n = [np.intersect1d(host_rows[j], rows_n) for j in range(len(host_rows))]
    groups_n = [g for k, g in enumerate(groups) if k != d]
    host_cols_n = np.asarray([j for j in range(nh) if j != d], dtype=np.int64)
    return {"rows_n": rows_n, "base_n": base_n, "host_rows_n": host_rows_n, "groups_n": groups_n,
            "host_cols_n": host_cols_n}


def index_stream(n, seed, n_hosts, n_pick):
    """The first n index draws of R4-N's stream: rng.choice(n_hosts, n_pick, replace=False) in order
    from default_rng(seed)."""
    rng = np.random.default_rng(seed)
    return [rng.choice(n_hosts, size=n_pick, replace=False) for _ in range(n)]


def loo_maps(L, y, C, rows_a, groups, fns):
    """Criterion X's fixed maps: for host j, R_j with r_j = R_j y[rows_a] (the leave-one-host-out
    residuals of g_j from the fit under C without g_j) and S_j^-1. Stacked as one matrix R (rows in
    group order) with offsets."""
    rows_a = np.asarray(rows_a)
    n = len(rows_a)
    blocks, sinv, offs = [], [], [0]
    for g in groups:
        g = np.asarray(g)
        pg = np.searchsorted(rows_a, g)
        if np.any(pg >= n) or not np.array_equal(rows_a[np.minimum(pg, n - 1)], g):
            raise RuntimeError("a calibrator group has rows outside rows_a")
        keep = np.setdiff1d(rows_a, g)
        res = fns["fit"](L, y, C, keep, est=True)
        kept = res["kept"]
        Xg = L[np.ix_(g, kept)]
        R = np.zeros((len(g), n))
        R[np.arange(len(g)), pg] = 1.0
        R[:, np.searchsorted(rows_a, keep)] -= Xg @ res["A"]
        S = C[np.ix_(g, g)] + Xg @ res["cov"] @ Xg.T
        blocks.append(R)
        sinv.append(np.linalg.inv(S))
        offs.append(offs[-1] + len(g))
    return {"R": np.vstack(blocks), "Sinv": sinv, "offs": offs}


def crit_x_values(maps, ya):
    r = maps["R"] @ ya
    o = maps["offs"]
    return np.array([float(r[o[j]:o[j + 1]] @ maps["Sinv"][j] @ r[o[j]:o[j + 1]])
                     for j in range(len(maps["Sinv"]))])


def crit_s_values(M, sig, excl, ya):
    """spread_excl_j = numpy.std (ddof 0) of Delta_k / sigma_k over the subsets that do not contain j."""
    z = (M @ ya) / sig
    return np.array([float(np.std(z[e])) if e.any() else np.nan for e in excl])


# ---------------------------------------------------------------- the block
def _cp_share(k, n):
    lo, hi = rob._cp(k, n)
    return {"k": int(k), "n": int(n), "p": (1 + k) / (1 + n), "ci95": [lo, hi]}


def run_block(L, y, C, nz, rows_a, groups, labels, host_rows, picks, n_out, P, fns, log, n_pick=10,
              recorded_tau=RECORDED_TAU_N, recorded_spread=RECORDED_SPREAD_OBS,
              crit_s_expected=CRIT_S_EXPECTED, expected_col=None, rob_spread_obs=None):
    """The whole R2-RE-SEL block. `groups` are the 37 calibrator SN groups (calib_groups), `picks` R4's
    draws on the 37-host system, `n_out` the R2-RE-N5584 block's output from the same run, `rob_spread_obs`
    R2-RE-ROB part B's spread_obs from the same run (descriptive check of criterion S's subsets)."""
    t_block = time.perf_counter()
    rows_a = np.asarray(rows_a)
    nh = len(groups)
    cols = [j for j, h in enumerate(labels) if h == P["n5584_host"]]
    if len(cols) != 1:
        raise RuntimeError(f"host {P['n5584_host']} labels {len(cols)} columns, expected 1")
    col = cols[0]
    if expected_col is not None and col != expected_col:
        raise RuntimeError(f"{P['n5584_host']} is column {col}, documented as column {expected_col}")
    if n_out.get("column") is not None and n_out["column"] != col:
        raise RuntimeError(f"R2-RE-N5584 dropped column {n_out['column']}, this block expects {col}")
    host = labels[col]
    n_tau, n_spread, n_sub = int(P["sel_n_tau"]), int(P["sel_n_spread"]), int(P["sel_n_subsets"])
    out = {"host": host, "column": int(col),
           "headline": "R2-RE's row stays the headline; this block attaches labels",
           "null": "y_s = L q_hat + K eps_s on the NGC 4258-only rows (37 hosts), under C; the most extreme "
                   "host by criterion X or S is dropped before tau_hat and the spread are computed",
           "settings": {"eps": "numpy.random.default_rng(sel_seed_base + s).standard_normal(len(rows_a))",
                        **{k: P[k] for k in ("sel_seed_base", "sel_n_tau", "sel_n_spread", "sel_n_subsets",
                                             "sel_max_failed")},
                        "subsets_x_s_spread": "first sel_n_subsets index draws rng.choice(36, 10) of "
                                              "default_rng(r4_seed), mapped onto the 36 columns other than d",
                        "subsets_criterion_s": "the first sel_n_subsets R4 draws on 37 hosts (ROB part B's)"}}
    seconds = {}

    # ---- observed values (from the R2-RE-N5584 block of the same run)
    drop = n_out.get("drop", {})
    re_n = drop.get("r2_re", {})
    bn = drop.get("bn", {})
    bn_tau, bn_sp = bn.get("tau", {}), bn.get("spread", {})
    tau_avail = drop.get("status") == "evaluated" and re_n.get("status") == "evaluated"
    spread_avail = bn_sp.get("status") == "evaluated"
    tau_obs = re_n["tau_hat"] if tau_avail else None
    spread_obs = bn_sp["spread_obs"] if spread_avail else None
    bad = observed_mismatches(tau_obs, spread_obs, recorded_tau, recorded_spread)
    out["observed"] = {"tau_hat_N": tau_obs, "spread_obs": spread_obs, "recorded_tau_hat_N": recorded_tau,
                       "recorded_spread_obs": recorded_spread, "rtol_tau": TAU_N_RTOL,
                       "rtol_spread": SPREAD_RTOL, "mismatches": bad}
    out["bn_unselected"] = {
        "tau": {k: bn_tau.get(k) for k in ("status", "k", "n_ok", "p", "ci95", "label", "sim_quantiles",
                                           "n_at_zero")},
        "spread": {k: bn_sp.get(k) for k in ("status", "k", "n_sims", "p", "ci95", "label", "sim_quantiles")}}
    # the addendum's observed-value stop rule takes precedence over the implementation's configuration guard
    if bad:
        out.update(status=BLOCK_NE_OBSERVED, reading=READ_NE, section5=SECTION5["stays"],
                   seconds=time.perf_counter() - t_block)
        log("R2-RE-SEL: " + BLOCK_NE_OBSERVED + ": " + "; ".join(bad))
        return out
    if n_sub != int(P["rob_n_subsets"]):
        out.update(status=BLOCK_NE_CONFIG.format(a=n_sub, b=P["rob_n_subsets"]), reading=READ_NE,
                   section5=SECTION5["stays"], seconds=time.perf_counter() - t_block)
        log("R2-RE-SEL: " + out["status"])
        return out

    reasons = {"tau": [], "spread_X": [], "spread_S": []}
    if not tau_avail:
        reasons["tau"].append("R2-RE-N5584 (a) or its reduced-system R2-RE not evaluated")
    if not spread_avail:
        for k in ("spread_X", "spread_S"):
            reasons[k].append("B-N's spread part not evaluated")
    if not picks:
        reasons["spread_S"].append("R4 has no draws")

    # ---- null data under C on rows_a (the same y_hat and K as ROB)
    t0 = time.perf_counter()
    res_full = fns["fit"](L, y, C, rows_a, est=True)
    kept = res_full["kept"]
    yhat = L[np.ix_(rows_a, kept)] @ res_full["q"][kept]
    K = linalg.cholesky(C[np.ix_(rows_a, rows_a)], lower=True)
    ya_real = y[rows_a]

    def sim(s):
        eps = np.random.default_rng(P["sel_seed_base"] + s).standard_normal(len(rows_a))
        return yhat + K @ eps

    # ---- criterion X: maps, reproduction of loo_chi2 on the real y, selection of the host
    checks = {}
    maps = None
    try:
        maps = loo_maps(L, y, C, rows_a, groups, fns)
        ref = fns["loo_chi2"](L, y, C, rows_a, groups, labels)
    except (np.linalg.LinAlgError, ValueError) as e:
        if not fns["is_fit_failure"](e):
            raise
        maps = None
        for k in ("tau", "spread_X"):
            reasons[k].append(f"a leave-one-out fit under C failed: {e}")
    x_real = None
    if maps is not None:
        x_real = crit_x_values(maps, ya_real)
        x_ref = np.array([h["chi2"] for h in ref["per_host"]])
        rel = np.abs(x_real - x_ref) / np.abs(x_ref)
        checks["loo_maps"] = {"max_rel_diff": float(rel.max()), "rtol": LOO_RTOL}
        if not np.all(rel <= LOO_RTOL):
            raise RuntimeError(f"criterion X maps do not reproduce loo_chi2 (max rel diff {rel.max():.2e})")
        d_real = pick_max(x_real)
        checks["criterion_x_selects"] = {"column": d_real, "host": labels[d_real], "chi2": float(x_real[d_real])}
        if d_real != col:
            for k in ("tau", "spread_X"):
                reasons[k].append(f"criterion X does not select {host} on the real data (selects {labels[d_real]})")
    seconds["criterion_x_maps"] = time.perf_counter() - t0

    # ---- criterion S: ROB part B's subsets on 37 hosts, reference fit with all hosts
    t0 = time.perf_counter()
    MS = sigS = excl = None
    s_real = None
    if picks:
        use = picks[:n_sub]
        try:
            any_host = nz[:, :nh].any(axis=1)
            base_rows = np.array([i for i in rows_a if not any_host[i]])
            MS, sigS = rob.shift_rows(L, y, C, rows_a, res_full, use, base_rows, host_rows, fns)
        except (np.linalg.LinAlgError, ValueError) as e:
            if not fns["is_fit_failure"](e):
                raise
            MS = None
            reasons["spread_S"].append(f"fit: building criterion S's subset rows: {e}")
        if MS is not None:
            contains = np.zeros((len(use), nh), bool)
            for i, pk in enumerate(use):
                contains[i, np.asarray(pk)] = True
            excl = [~contains[:, j] for j in range(nh)]
            s_real = crit_s_values(MS, sigS, excl, ya_real)
            ds_real = pick_min(s_real)
            checks["criterion_s"] = {
                "n_subsets": len(use), "spread_37": float(np.std((MS @ ya_real) / sigS)),
                "selects": {"column": ds_real, "host": labels[ds_real], "spread_excl": float(s_real[ds_real])},
                "host_value": float(s_real[col]), "expected": crit_s_expected, "tol": CRIT_S_TOL,
                "reproduced": bool(abs(s_real[col] - crit_s_expected) <= CRIT_S_TOL)}
            sp37 = checks["criterion_s"]["spread_37"]
            checks["criterion_s"]["rob_spread_obs"] = rob_spread_obs
            checks["criterion_s"]["spread_37_matches_rob"] = (   # descriptive: the subsets are ROB's
                None if rob_spread_obs is None
                else bool(abs(sp37 - rob_spread_obs) <= SPREAD_RTOL * abs(rob_spread_obs)))
            if ds_real != col:
                reasons["spread_S"].append(f"criterion S does not select {host} on the real data "
                                           f"(selects {labels[ds_real]})")
            if not abs(s_real[col] - crit_s_expected) <= CRIT_S_TOL:
                reasons["spread_S"].append(f"criterion S reproduction: spread_excl for {host} is "
                                           f"{s_real[col]:.4f}, not {crit_s_expected} within {CRIT_S_TOL}")
    seconds["criterion_s_rows"] = time.perf_counter() - t0
    if x_real is not None or s_real is not None:
        out["real_criteria"] = [{"column": j, "host": labels[j],
                                 "loo_chi2_C": None if x_real is None else float(x_real[j]),
                                 "n_calib_rows": int(len(groups[j])),
                                 "spread_excl": None if s_real is None else float(s_real[j])} for j in range(nh)]

    # ---- the 36-host subsets: R4-N's index stream, mapped per dropped host
    stream = index_stream(n_sub, P["r4_seed"], nh - 1, n_pick)
    first = [[int(j) for j in reduced_system(nz, rows_a, col, groups, host_rows)["host_cols_n"][ix]]
             for ix in stream[:5]]
    checks["first_subsets"] = {"first_picks": first}
    bn_first = drop.get("r4n", {}).get("first_picks")
    if spread_avail and bn_first:          # no comparison when R4-N left no draws / B-N's spread not evaluated
        checks["first_subsets"]["r2_re_n5584_first_picks"] = bn_first
        if first != bn_first[:len(first)]:
            raise RuntimeError("the first subsets for d = the dropped host differ from R4-N's first_picks")
    status = {k: ("evaluated" if not v else "not evaluable (" + v[0] + ")") for k, v in reasons.items()}

    # ---- pass 1: the selected host of every simulation under each criterion
    t0 = time.perf_counter()
    n_all = max(n_tau, n_spread)
    d_x = [] if maps is not None else None
    d_s = [] if MS is not None else None
    max_x, min_s = [], []
    if d_x is not None or d_s is not None:
        for s in range(n_all):
            ya = sim(s)
            if d_x is not None:
                v = crit_x_values(maps, ya)
                d_x.append(pick_max(v))
                max_x.append(float(v.max()))
            if d_s is not None:
                v = crit_s_values(MS, sigS, excl, ya)
                d_s.append(pick_min(v))
                min_s.append(float(np.nanmin(v)))
    MS = None                                    # one large matrix at a time
    seconds["selection_pass"] = time.perf_counter() - t0

    # ---- the d = host rows and the spread_obs reproduction, before the tau part (an early stop)
    do_x, do_s = status["spread_X"] == "evaluated", status["spread_S"] == "evaluated"
    built, failed_d, cache = {}, {}, {}

    def build(d):
        tb = time.perf_counter()
        red = reduced_system(nz, rows_a, d, groups, host_rows)
        rows_n = red["rows_n"]
        picks_d = [red["host_cols_n"][ix] for ix in stream]
        res_ref = fns["fit"](L, y, C, rows_n, est=True)
        M, sig = rob.shift_rows(L, y, C, rows_n, res_ref, picks_d, red["base_n"], red["host_rows_n"], fns)
        built[d] = time.perf_counter() - tb
        return rows_n, M, sig

    if do_x or do_s:
        try:
            cache[col] = build(col)
        except (np.linalg.LinAlgError, ValueError) as e:
            if not fns["is_fit_failure"](e):
                raise
            raise RuntimeError(f"rows for {host} failed although B-N built them: {e}")
        rows_n, M, sig = cache[col]
        obs = float(np.std((M @ y[rows_n]) / sig))
        checks["spread_obs_d_host"] = {"value": obs, "spread_obs": spread_obs,
                                       "rel_diff": abs(obs - spread_obs) / abs(spread_obs)}
        if not abs(obs - spread_obs) <= SPREAD_RTOL * abs(spread_obs):
            raise RuntimeError(f"d = {host} path gives spread {obs!r}, B-N's spread_obs {spread_obs!r}")
        M = None

    # ---- tau part (criterion X)
    t0 = time.perf_counter()
    if status["tau"] == "evaluated":
        taus, failed = [], 0
        for s in range(n_tau):
            ys = np.array(y, dtype=float, copy=True)
            ys[rows_a] = sim(s)
            red = reduced_system(nz, rows_a, d_x[s], groups, host_rows)
            try:
                est = fns["reml_tau"](lambda t: fns["reml_m2l"](L, ys, C, red["rows_n"], red["groups_n"], t),
                                      P["re_tau_max"], P["re_grid_step"], interval=False)
                taus.append(est["tau_hat"])
            except (np.linalg.LinAlgError, ValueError) as e:
                if not fns["is_fit_failure"](e):
                    raise
                failed += 1
            if s % 50 == 49:
                log(f"  R2-RE-SEL tau: {s + 1} sims, {time.perf_counter() - t0:.0f} s")
        n, k = len(taus), int(np.sum(np.array(taus) >= tau_obs))
        tau_rec = {"tau_obs": tau_obs, "n_sims": n_tau, "n_ok": n, "n_failed": failed, "k": k,
                   "taus": [round(t, 5) for t in taus],
                   "sim_quantiles": [float(q) for q in np.percentile(taus, [5, 50, 95])] if taus else None,
                   "n_at_zero": int(sum(1 for t in taus if t < 1e-3))}
        if failed > P["sel_max_failed"]:
            tau_rec["status"] = "not evaluable (too many failed fits)"
        else:
            label, ci = tau_label(k, n)
            tau_rec.update(status="evaluated", p=(1 + k) / (1 + n), ci95=list(ci), label=label)
    else:
        tau_rec = {"status": status["tau"]}
    tau_rec["reasons"] = reasons["tau"]
    seconds["tau_part"] = time.perf_counter() - t0
    out["tau"] = tau_rec

    # ---- spread parts (criteria X and S): rows built once per dropped host, sims grouped by d
    t0 = time.perf_counter()
    sp_x = [None] * n_spread if do_x else None
    sp_s = [None] * n_spread if do_s else None
    need = {}
    if do_x:
        for s in range(n_spread):
            need.setdefault(d_x[s], set()).add(s)
    if do_s:
        for s in range(n_spread):
            need.setdefault(d_s[s], set()).add(s)
    if do_x or do_s:
        for d in sorted(need):
            if d in cache:                          # the d = host rows built above
                rows_n, M, sig = cache.pop(d)
            else:
                try:
                    rows_n, M, sig = build(d)
                except (np.linalg.LinAlgError, ValueError) as e:
                    if not fns["is_fit_failure"](e):
                        raise
                    failed_d[d] = str(e)
                    continue
            pos_n = np.searchsorted(rows_a, rows_n)
            for s in sorted(need[d]):
                v = float(np.std((M @ sim(s)[pos_n]) / sig))
                if do_x and d_x[s] == d:
                    sp_x[s] = v
                if do_s and d_s[s] == d:
                    sp_s[s] = v
            M = None
    cache.clear()
    seconds["spread_parts"] = time.perf_counter() - t0
    out["dropped_hosts_built"] = {"n_distinct": len(built), "hosts": [labels[d] for d in sorted(built)],
                                  "seconds_build": {labels[d]: t for d, t in sorted(built.items())},
                                  "failed": {labels[d]: e for d, e in sorted(failed_d.items())}}

    def spread_part(name, crit, dsel, vals, do):
        if not do:
            return {"status": status[name], "reasons": reasons[name]}
        fails = sorted({dsel[s] for s in range(n_spread)} & set(failed_d))
        if fails:
            return {"status": "not evaluable (fit: building the rows for dropped host "
                              + ", ".join(labels[d] for d in fails) + ")", "reasons": reasons[name]}
        k = int(np.sum(np.array(vals) >= spread_obs))
        label, ci = spread_label(k, n_spread, crit)
        return {"status": "evaluated", "criterion": crit, "spread_obs": spread_obs, "n_subsets": n_sub,
                "n_sims": n_spread, "k": k, "p": (1 + k) / (1 + n_spread), "ci95": list(ci), "label": label,
                "sim_quantiles": [float(q) for q in np.percentile(vals, [5, 50, 95])],
                "spreads": [round(v, 6) for v in vals], "reasons": reasons[name]}

    out["spread_X"] = spread_part("spread_X", "X", d_x, sp_x, do_x)
    out["spread_S"] = spread_part("spread_S", "S", d_s, sp_s, do_s)

    # ---- reported, not decisive
    sel = {}
    for name, ds in (("X", d_x), ("S", d_s)):
        if ds is None:
            continue
        sel[name] = {"dropped": ds[:n_all],
                     "frequency_all": {labels[j]: c for j, c in sorted(Counter(ds[:n_spread]).items())},
                     "frequency_first_tau": {labels[j]: c for j, c in sorted(Counter(ds[:n_tau]).items())},
                     "n_host_all": int(sum(1 for d in ds[:n_spread] if d == col)),
                     "n_host_first_tau": int(sum(1 for d in ds[:n_tau] if d == col))}
    if d_x is not None and d_s is not None:
        sel["n_same_X_S"] = int(sum(1 for a, b in zip(d_x[:n_spread], d_s[:n_spread]) if a == b))
        sel["n_same_X_S_first_tau"] = int(sum(1 for a, b in zip(d_x[:n_tau], d_s[:n_tau]) if a == b))
    out["selection"] = sel
    ext = {}
    if d_x is not None:
        mx = np.array(max_x[:n_spread])
        ext["max_loo_chi2"] = {"real_host_value": float(x_real[col]),
                               "quantiles_5_50_95": [float(q) for q in np.percentile(mx, [5, 50, 95])],
                               "values": [round(v, 4) for v in mx.tolist()],
                               **_cp_share(int(np.sum(mx >= x_real[col])), len(mx))}
    if d_s is not None:
        ms = np.array(min_s[:n_spread])
        ext["min_spread_excl"] = {"real_host_value": float(s_real[col]),
                                  "quantiles_5_50_95": [float(q) for q in np.percentile(ms, [5, 50, 95])],
                                  "values": [round(v, 5) for v in ms.tolist()],
                                  **_cp_share(int(np.sum(ms <= s_real[col])), len(ms))}
    ext["note"] = "descriptive: how extreme the host is as the most extreme of 37 under C; no label"
    out["extremeness"] = ext
    out["checks"] = checks

    read = reading(out["tau"], out["spread_X"], out["spread_S"])
    out["reading"] = read
    out["section5"] = section5_action(read)
    out["not_lowered_vs_bn"] = {
        "tau": not_lowered(out["tau"].get("p"), bn_tau.get("p")),
        "spread_X": not_lowered(out["spread_X"].get("p"), bn_sp.get("p")),
        "spread_S": not_lowered(out["spread_S"].get("p"), bn_sp.get("p")),
        "note": "descriptive: True means the selection did not lower that p value in this setup (B-N's p "
                "from the same run); it does not override rules (3) and (4)"}
    out["status"] = "evaluated"
    seconds["block"] = time.perf_counter() - t_block
    out["seconds"] = seconds
    return out


def summary(s_out):
    """Short summary for summary.json (R2_RE_SEL)."""
    if "reading" not in s_out:
        return {"status": s_out.get("status")}
    g = lambda part, key: s_out.get(part, {}).get(key)
    return {"status": s_out.get("status"), "reading": s_out["reading"],
            "tau": g("tau", "label") or g("tau", "status"), "p_tau": g("tau", "p"),
            "spread_X": g("spread_X", "label") or g("spread_X", "status"), "p_spread_X": g("spread_X", "p"),
            "spread_S": g("spread_S", "label") or g("spread_S", "status"), "p_spread_S": g("spread_S", "p")}
