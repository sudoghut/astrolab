"""R2-RE-N5584 (README section 2, addendum 2026-11-18, T-039): explicit treatment of host N5584.

(a) R2-RE-N5584-DROP: remove every row with a non-zero in N5584's host column from the NGC 4258-only
    system; reference fit and host step under C; R2-RE (REML, 36 groups, with interval) and the host
    step under V(tau_N); R4-N (10-host subsets of the 36 remaining hosts) under C and under V(tau_N);
    B-N (R2-RE-ROB part B on the reduced system).
(b) R2-RE-T: Student-t host effect on the full 37-host system, fitted by variational EM; plug-in
    V_T = C + sum_j (tau^2 / omega_j) h_j h_j^T; host step under V_T.

run.py passes its own functions in (`fns`); this module does not import run (AGENTS.md section 2).
"""
import time

import numpy as np
from scipy import linalg

import rob

KNOWN = "known before this addendum"
TAU_UNUSUAL = "tau_hat unusual under C (excess calibrator scatter)"
SPREAD_UNUSUAL = "the R4 excess spread is unusual under C"
SPREAD_USUAL = "the R4 spread is consistent with C"

READ_NE = "not evaluable"
READ_N5584 = "the excess calibrator scatter of R2-RE-ROB is attributable to N5584"
READ_SPREAD = "excess scatter remains without N5584"
READ_TAU = "τ excess remains without N5584"
READ_UNDET = "undetermined"

T_ROBUST = "R2-RE verdict robust to a heavy-tailed host effect"
T_DEPENDS = "R2-RE verdict depends on the host-effect distribution (heavy-tailed: {row})"
JOINT_ROBUST = ("the null result holds under both removal and down-weighting of N5584; "
                "only the hybrid τ route of R2-RE-ROB A flips")
JOINT_DEPENDS = "the verdict depends on how one host is modelled"
JOINT_NONE = "no joint reading ((b) not evaluable); (a)'s labels stand alone"


# ---------------------------------------------------------------- decision rules (pure)
def reading_a(tau_rec, spread_rec):
    """(a)'s reading from B-N's two parts, rules checked in the pre-registered order."""
    if not (tau_rec.get("status") == "evaluated" and spread_rec.get("status") == "evaluated"):
        return READ_NE
    t, s = tau_rec["label"], spread_rec["label"]
    if s == SPREAD_USUAL and t != TAU_UNUSUAL:
        return READ_N5584
    if s == SPREAD_UNUSUAL:
        return READ_SPREAD
    if s == SPREAD_USUAL and t == TAU_UNUSUAL:
        return READ_TAU
    return READ_UNDET


def label_b(row_t, row_re):
    return T_ROBUST if row_t == row_re else T_DEPENDS.format(row=row_t)


def joint_reading(b_status, b_label, z_c, z_re, tau_re, z_t):
    if b_status != "evaluated":
        return JOINT_NONE
    if b_label == T_ROBUST:
        return JOINT_ROBUST
    return (f"{JOINT_DEPENDS} (on the full 37-host system: R2 z = {z_c:.2f} under C, R2-RE z' = "
            f"{z_re:.2f} under V(tau_hat = {tau_re:.3f}), z_T = {z_t:.2f} under V_T; observed values, "
            f"not a decision rule)")


# ---------------------------------------------------------------- (b) variational EM
def vem_precompute(L, y, C, rows, groups):
    """A = X^T C^-1 X, B = X^T C^-1 Z, D = Z^T C^-1 Z, b = (X^T C^-1 y; Z^T C^-1 y) with one Cholesky
    factor of C on `rows`; X holds the columns of L non-zero on `rows` (infer.gls's kept), Z the
    indicators h_j of the row indices in groups[j] (indices into the full system)."""
    idx = np.asarray(rows)
    pos = {r: k for k, r in enumerate(idx)}
    X = L[idx]
    X = X[:, np.any(X != 0.0, axis=0)]
    Z = np.zeros((len(idx), len(groups)))
    for j, g in enumerate(groups):
        k = [pos[r] for r in g if r in pos]
        Z[k, j] = 1.0
    cf = linalg.cho_factor(C[np.ix_(idx, idx)], lower=True)
    cx, cz, cy = linalg.cho_solve(cf, X), linalg.cho_solve(cf, Z), linalg.cho_solve(cf, y[idx])
    A = X.T @ cx
    D = Z.T @ cz
    return {"A": 0.5 * (A + A.T), "B": X.T @ cz, "D": 0.5 * (D + D.T),
            "b": np.concatenate([X.T @ cy, Z.T @ cy])}


def vem(pre, nu, tau0, maxiter, tol, fix_omega=False):
    """Mean-field variational EM for u_j | w_j ~ N(0, tau^2 / w_j), w_j ~ Gamma(nu/2, rate nu/2), flat
    beta. Per iteration: P = [[A, B], [B^T, D + diag(omega)/tau^2]], m = P^-1 b, S = P^-1;
    s_j = m_u,j^2 + S_uu,jj; omega_j <- (nu + 1) / (nu + s_j / tau^2) (skipped with fix_omega: then
    this is EM for REML); tau^2 <- sum_j omega_j s_j / G with the just-updated omega. Stops when the
    largest relative change in tau^2 and in every omega_j is below tol."""
    A, B, D, b = pre["A"], pre["B"], pre["D"], pre["b"]
    p, G = A.shape[0], D.shape[0]
    P0 = np.block([[A, B], [B.T, D]])
    t2 = float(tau0) ** 2
    w = np.ones(G)
    converged, it, change = False, 0, np.inf
    eye = np.eye(p + G)
    for it in range(1, int(maxiter) + 1):
        Pm = P0.copy()
        Pm[p:, p:] += np.diag(w / t2)
        cf = linalg.cho_factor(Pm, lower=True)
        m = linalg.cho_solve(cf, b)
        S = linalg.cho_solve(cf, eye)
        s = m[p:] ** 2 + np.diag(S)[p:]
        w_new = w if fix_omega else (nu + 1.0) / (nu + s / t2)
        t2_new = float(np.sum(w_new * s) / G)
        change = max(abs(t2_new - t2) / t2, float(np.max(np.abs(w_new - w) / w)))
        t2, w = t2_new, np.array(w_new, dtype=float)
        if change < tol:
            converged = True
            break
    return {"tau": float(np.sqrt(t2)), "omega": w, "iterations": it, "converged": converged,
            "last_rel_change": float(change)}


def with_group_var(C, groups, var):
    """V = C + sum_j var_j h_j h_j^T (per-group variance; with var_j = tau^2 this is run.with_re)."""
    V = C.copy()
    for idx, v in zip(groups, var):
        if v > 0:
            V[np.ix_(idx, idx)] += v
    return V


def heavy_tail(L, y, C, rows_a, rows_s, groups, labels, re_out, c_step, P, fns, log):
    """(b) R2-RE-T on the full NGC 4258-only system (37 hosts)."""
    t0 = time.perf_counter()
    out = {"model": "u_j | w_j ~ N(0, tau^2/w_j), w_j ~ Gamma(nu/2, rate nu/2); variational EM; "
                    "plug-in V_T = C + sum_j (tau_hat^2/omega_hat_j) h_j h_j^T",
           "settings": {k: P[k] for k in ("t_nu", "t_nu_sens", "t_maxiter", "t_tol", "t_starts")}}
    if re_out.get("status") != "evaluated":
        out["status"] = "not evaluable (R2-RE not evaluable)"
        return out
    pre = vem_precompute(L, y, C, rows_a, groups)
    tau_max = P["re_tau_max"]

    # validity (1): omega fixed at 1, start tau = 0.20 -> EM for REML, reproduces R2-RE
    imp = vem(pre, P["t_nu"], 0.20, P["t_maxiter"], P["t_tol"], fix_omega=True)
    chk = {"start_tau": 0.20, "tau_em": imp["tau"], "iterations": imp["iterations"],
           "converged": imp["converged"], "tau_r2_re": re_out["tau_hat"], "z_r2_re": re_out["z"]}
    reason = None
    if not imp["converged"]:
        reason = f"not converged in {imp['iterations']} iterations"
    else:
        chk["tau_diff"] = imp["tau"] - re_out["tau_hat"]
        tau_used = 0.0 if imp["tau"] < 1e-3 else imp["tau"]
        try:
            hs_imp, _ = fns["host_step_under"](L, y, fns["with_re"](C, groups, tau_used), rows_a, rows_s)
            chk["z_em"] = hs_imp["z"]
            chk["z_diff"] = hs_imp["z"] - re_out["z"]
        except (np.linalg.LinAlgError, ValueError) as e:
            if not fns["is_fit_failure"](e):
                raise
            reason = f"host-step fit failed: {e}"
        if reason is None and abs(chk["tau_diff"]) > 1e-4:
            reason = f"tau differs from R2-RE by {chk['tau_diff']:.2e} (> 1e-4)"
        if reason is None and abs(chk["z_diff"]) > 0.005:
            reason = f"z' differs from R2-RE by {chk['z_diff']:.4f} (> 0.005)"
    chk["passed"] = reason is None
    if reason:
        chk["failure"] = reason
    out["implementation_check"] = chk
    log(f"R2-RE-T implementation check: {'passed' if reason is None else 'failed: ' + reason}")

    def one_nu(nu):
        rec = {"nu": nu, "starts": []}
        if reason is not None:
            rec["status"] = f"not evaluable (implementation check failed: {reason})"
            return rec
        fits = []
        for t0_ in P["t_starts"]:
            f = vem(pre, nu, t0_, P["t_maxiter"], P["t_tol"])
            fits.append(f)
            rec["starts"].append({"tau0": t0_, "tau_hat": f["tau"], "iterations": f["iterations"],
                                  "converged": f["converged"], "last_rel_change": f["last_rel_change"],
                                  "omega": [float(v) for v in f["omega"]]})
        if not all(f["converged"] for f in fits):
            rec["status"] = ("not evaluable (not converged; iterations "
                             + ", ".join(str(f["iterations"]) for f in fits) + ")")
            return rec
        if max(f["tau"] for f in fits) - min(f["tau"] for f in fits) > 1e-4:
            rec["status"] = "not evaluable (multiple fixed points)"
            return rec
        f = fits[0]                       # the first start's fixed point (the starts agree within 1e-4)
        tau = f["tau"]
        rec["tau_hat"] = tau
        if tau > tau_max - 1e-3:
            rec["status"] = "not evaluable (bound)"
            return rec
        at_zero = tau < 1e-3
        rec["at_zero"] = at_zero
        om = f["omega"]
        order = np.argsort(om, kind="stable")
        rec["omega_ranked"] = [{"column": int(j), "host": labels[j], "omega": float(om[j]),
                                "effective_scatter": float(tau / np.sqrt(om[j]))} for j in order]
        var = np.zeros(len(groups)) if at_zero else tau * tau / om
        V = with_group_var(C, groups, var)
        try:
            ia = np.asarray(rows_a)
            linalg.cholesky(V[np.ix_(ia, ia)], lower=True)
            hs, _ = fns["host_step_under"](L, y, V, rows_a, rows_s)
        except (np.linalg.LinAlgError, ValueError) as e:
            if not fns["is_fit_failure"](e):
                raise
            rec["status"] = f"not evaluable (fit: {e})"
            return rec
        rec.update(status="evaluated", host_step=hs, z=hs["z"],
                   row=fns["verdict"](hs["z"], hs["shift"], hs["shift_sigma"]))
        return rec

    main = one_nu(P["t_nu"])
    out["nu_main"] = main
    out["status"] = main["status"]
    if main["status"] == "evaluated":
        out["label"] = label_b(main["row"], re_out["verdict"])
        log(f"R2-RE-T nu={P['t_nu']}: evaluated")
    else:
        out["label"] = main["status"]
    sens = []
    for nu in P["t_nu_sens"]:
        r = one_nu(nu)
        if r["status"] != "evaluated":
            r["status"] = "reported, not evaluable: " + r["status"]
        sens.append(r)
    out["nu_sensitivity"] = sens
    out["joint_inputs"] = {"z_r2_c": c_step["z"], "z_r2_re": re_out["z"], "tau_r2_re": re_out["tau_hat"],
                           "z_t": main.get("z")}
    out["seconds"] = time.perf_counter() - t0
    return out


# ---------------------------------------------------------------- (a) removal
def drop_host(L, y, C, nz, cls, rows_a, rows_s, col, cchp_cols, groups, labels, host_rows, n_sn_col,
              P, fns, log):
    """(a) R2-RE-N5584-DROP."""
    t0 = time.perf_counter()
    rows_a = np.asarray(rows_a)
    rows_s = np.asarray(rows_s)
    nh = len(groups)
    if col in set(cchp_cols) or nz[rows_s, col].any():
        raise RuntimeError(f"column {col} ({labels[col]}) is in the CCHP selection: rows_s would change")
    hit = nz[rows_a, col]
    rows_n = rows_a[~hit]
    removed = rows_a[hit]
    out = {"host": labels[col], "column": int(col),
           "rows_removed": {"total": int(len(removed)), "calib_sn": int(cls["calib"][removed].sum()),
                            "cepheid": int(cls["ceph"][removed].sum()),
                            "other": int(len(removed) - cls["calib"][removed].sum() - cls["ceph"][removed].sum())},
           "rows_reduced": int(len(rows_n)), "rows_s": int(len(rows_s)), "n_hosts": nh - 1}
    groups_n = [g for k, g in enumerate(groups) if k != col]
    host_cols_n = [j for j in range(nh) if j != col]
    host_rows_n = [np.intersect1d(host_rows[j], rows_n) for j in range(len(host_rows))]
    out["host_rows_trimmed"] = [labels[j] for j in host_cols_n
                                if len(host_rows_n[j]) != len(host_rows[j])]
    any_host = nz[:, :nh].any(axis=1)
    base_n = np.array([i for i in rows_n if not any_host[i]])
    verdict = fns["verdict"]

    # reference fit and host step under C
    try:
        hs_c, res_c = fns["host_step_under"](L, y, C, rows_n, rows_s)
    except (np.linalg.LinAlgError, ValueError) as e:
        if not fns["is_fit_failure"](e):
            raise
        out["status"] = f"not evaluable (fit: {e})"
        return out
    out["c"] = {"host_step": hs_c, "z": hs_c["z"],
                "row": verdict(hs_c["z"], hs_c["shift"], hs_c["shift_sigma"]), "note": KNOWN}
    log(f"R2-RE-N5584 (a): host step under C on {len(rows_n)} rows")

    # R2-RE on the reduced system (36 groups)
    re_n = {"note": KNOWN}
    V = None
    try:
        est = fns["reml_tau"](lambda t: fns["reml_m2l"](L, y, C, rows_n, groups_n, t),
                              P["re_tau_max"], P["re_grid_step"])
    except (np.linalg.LinAlgError, ValueError) as e:
        if not fns["is_fit_failure"](e):
            raise
        re_n["status"] = f"not evaluable (fit: {e})"
        est = None
    if est is not None:
        re_n["reml"] = est
        re_n["interval_68"] = est["interval_68"]
        if est["at_upper_bound"]:
            re_n.update(status="not evaluable (bound)", tau_hat=est["tau_hat"])
        else:
            tau = 0.0 if est["at_zero"] else est["tau_hat"]
            re_n["tau_hat"] = tau
            try:
                V = fns["with_re"](C, groups_n, tau)
                hs_v, res_v = fns["host_step_under"](L, y, V, rows_n, rows_s)
                re_n.update(status="evaluated", host_step=hs_v, z=hs_v["z"],
                            verdict=verdict(hs_v["z"], hs_v["shift"], hs_v["shift_sigma"]))
            except (np.linalg.LinAlgError, ValueError) as e:
                if not fns["is_fit_failure"](e):
                    raise
                re_n["status"] = f"not evaluable (fit: {e})"
                V = None
    out["r2_re"] = re_n
    log(f"R2-RE-N5584 (a): reduced R2-RE {re_n['status']}")

    # R4-N under C
    r4n = {"status": "evaluated", "draws_requested": int(P["r4_draws"]),
           "draws": "rng.choice(36, 10, replace=False) from default_rng(r4_seed), indexing the 36 "
                    "remaining host columns in column order"}
    deltas, nsns, zs, picks = fns["r4_draws"](
        L, y, C, rows_n, res_c, hs_c["fivelogh0_37"], hs_c["sigma_37"], base_n, host_rows_n,
        np.array(host_cols_n), len(cchp_cols), int(P["r4_draws"]), P["r4_seed"], P["r4_max_minutes"],
        n_sn_col, r4n, log, "R4-N")
    if deltas:
        r4n.update(fns["r4_summary"](deltas, zs, nsns, hs_c["shift"], hs_c["z"]))
        log(f"R2-RE-N5584 (a): R4-N {r4n['draws']} draws")
    out["r4n"] = r4n
    if V is not None and picks:
        uv = {}
        fns["r2_re_r4"](uv, L, y, V, res_v, hs_v, rows_n, base_n, host_rows_n, picks)
        out["r4n_under_v"] = uv.get("r4_under_v")
        out["r4n_under_v_identity_check"] = uv.get("r4_identity_check")

    # B-N: R2-RE-ROB part B on the reduced system
    bn = rob.null_sims(L, y, C, rows_n, groups_n, re_n, picks, base_n, host_rows_n, P, fns,
                       lambda m: log("[N5584] " + m))
    tq = bn.get("tau", {})
    if tq.get("status") == "evaluated" and tq["taus"]:
        tq["sim_quantiles"] = [float(q) for q in np.percentile(tq["taus"], [5, 50, 95])]
        tq["n_at_zero"] = int(sum(1 for t in tq["taus"] if t < 1e-3))
    out["bn"] = bn
    out["reading"] = reading_a(bn.get("tau", {}), bn.get("spread", {}))
    out["status"] = "evaluated"
    out["seconds"] = time.perf_counter() - t0
    return out


def run_block(L, y, C, nz, cls, rows_a, rows_s, cchp_cols, groups, labels, host_rows, n_sn_col, re_out,
              c_step, P, fns, log, expected_col=None):
    """The whole R2-RE-N5584 block: (a), (b) and the joint reading, in that order."""
    cols = [j for j, h in enumerate(labels) if h == P["n5584_host"]]
    if len(cols) != 1:
        raise RuntimeError(f"host {P['n5584_host']} labels {len(cols)} columns, expected 1")
    col = cols[0]
    if expected_col is not None and col != expected_col:
        raise RuntimeError(f"{P['n5584_host']} is column {col}, documented as column {expected_col}")
    t0 = time.perf_counter()
    a = drop_host(L, y, C, nz, cls, rows_a, rows_s, col, cchp_cols, groups, labels, host_rows, n_sn_col,
                  P, fns, log)
    b = heavy_tail(L, y, C, rows_a, rows_s, groups, labels, re_out, c_step, P, fns, log)
    ji = b.get("joint_inputs", {})
    joint = joint_reading(b["status"], b.get("label"), ji.get("z_r2_c"), ji.get("z_r2_re"),
                          ji.get("tau_r2_re"), ji.get("z_t"))
    return {"status": "evaluated", "host": labels[col], "column": int(col),
            "headline": "R2-RE's row stays the headline; this block attaches labels",
            "drop": a, "heavy_tail": b, "joint_reading": joint, "seconds": time.perf_counter() - t0}
