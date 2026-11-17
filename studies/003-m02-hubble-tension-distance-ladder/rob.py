"""R2-RE-ROB (README section 2, addendum 2026-11-17, T-032): robustness of R2-RE.

A. Leave one host out: tau_j without host j; the label uses only the tau route (R2-RE's original
   host step under V(tau_j) over all 37 hosts' groups); the data route on the reduced system is
   reported.
B. Null simulations under C: tau_hat (400 sims, three-way Clopper-Pearson label) and R4's subset
   spread (2,000 sims over the first 1,000 R4 subsets, via precomputed linear estimator rows).

run.py passes its own functions in (`fns`); this module does not import run (AGENTS.md section 2).
"""
import time

import numpy as np
from scipy import linalg, stats


def _cp(k, n, level=0.95):
    """Two-sided equal-tailed Clopper-Pearson interval for k successes in n trials."""
    a = (1 - level) / 2
    lo = 0.0 if k == 0 else float(stats.beta.ppf(a, k, n - k + 1))
    hi = 1.0 if k == n else float(stats.beta.ppf(1 - a, k + 1, n - k))
    return lo, hi


def three_way(k, n, unusual, usual):
    lo, hi = _cp(k, n)
    if hi < 0.05:
        return unusual, (lo, hi)
    if lo > 0.05:
        return usual, (lo, hi)
    return "undetermined (Monte Carlo)", (lo, hi)


def leave_one_out(L, y, C, nz, rows_a, rows_s, cchp_cols, calib_groups, re_out, labels, P, fns, log):
    """Part A."""
    if re_out.get("status") != "evaluated":
        return {"status": "not evaluable (R2-RE not evaluable)"}
    row0 = re_out["verdict"]
    rows_a = np.asarray(rows_a)
    rows_s = np.asarray(rows_s)
    hosts, sensitive = [], []
    for j in range(len(calib_groups)):
        rec = {"column": j, "host": labels[j], "cchp": j in cchp_cols}
        keep_a = rows_a[~nz[rows_a, j]]
        groups_j = [g for k, g in enumerate(calib_groups) if k != j]
        try:
            est = fns["reml_tau"](lambda t: fns["reml_m2l"](L, y, C, keep_a, groups_j, t),
                                  P["re_tau_max"], P["re_grid_step"], interval=False)
        except (np.linalg.LinAlgError, ValueError) as e:
            if not fns["is_fit_failure"](e):
                raise
            rec["status"] = f"REML fit failed: {e}"
            hosts.append(rec)
            sensitive.append(labels[j])
            continue
        rec["tau_hat"] = est["tau_hat"]
        if est["at_upper_bound"]:
            rec["status"] = "tau at the upper bound"
            hosts.append(rec)
            sensitive.append(labels[j])
            continue
        tau = 0.0 if est["at_zero"] else est["tau_hat"]
        rec["tau_used"] = tau
        try:
            # tau route: R2-RE's original host step under V(tau_j) over all 37 hosts' groups
            hs, _ = fns["host_step_under"](L, y, fns["with_re"](C, calib_groups, tau), rows_a, rows_s)
            rec["tau_route"] = {"z": hs["z"], "shift": hs["shift"], "shift_sigma": hs["shift_sigma"],
                                "row": fns["verdict"](hs["z"], hs["shift"], hs["shift_sigma"])}
            # data route (reported): the reduced system at C and under V(tau_j)
            keep_s = rows_s[~nz[rows_s, j]]
            dr = {}
            for name, W in (("C", C), ("V", fns["with_re"](C, groups_j, tau))):
                h, _ = fns["host_step_under"](L, y, W, keep_a, keep_s)
                dr[name] = {"z": h["z"], "shift": h["shift"], "shift_sigma": h["shift_sigma"],
                            "row": fns["verdict"](h["z"], h["shift"], h["shift_sigma"])}
            if rec["cchp"]:
                dr["note"] = "changes the tested selection (9 CCHP hosts)"
            rec["data_route"] = dr
        except (np.linalg.LinAlgError, ValueError) as e:
            if not fns["is_fit_failure"](e):
                raise
            rec["status"] = f"host-step fit failed: {e}"
            hosts.append(rec)
            sensitive.append(labels[j])
            continue
        rec["status"] = "evaluated"
        if rec["tau_route"]["row"] != row0:
            sensitive.append(labels[j])
        hosts.append(rec)
        log(f"  R2-RE-ROB A {labels[j]}: tau {tau:.4f}, z {rec['tau_route']['z']:.2f}")
    taus = [h["tau_hat"] for h in hosts if "tau_hat" in h]
    zs = [h["tau_route"]["z"] for h in hosts if "tau_route" in h]
    label = ("verdict robust to single hosts' influence on tau" if not sensitive
             else "verdict sensitive to single hosts' influence on tau")
    return {"status": "evaluated", "label": label, "sensitive_hosts": sensitive, "r2_re_row": row0,
            "tau_range": [min(taus), max(taus)] if taus else None,
            "tau_route_z_range": [min(zs), max(zs)] if zs else None, "hosts": hosts}


def null_sims(L, y, C, rows_a, calib_groups, re_out, picks, base_rows, host_rows, P, fns, log):
    """Part B."""
    rows_a = np.asarray(rows_a)
    res_full = fns["fit"](L, y, C, rows_a, est=True)
    kept = res_full["kept"]
    yhat = L[np.ix_(rows_a, kept)] @ res_full["q"][kept]
    K = linalg.cholesky(C[np.ix_(rows_a, rows_a)], lower=True)

    def simulate(s):
        ys = np.array(y, dtype=float, copy=True)
        eps = np.random.default_rng(P["rob_seed_base"] + s).standard_normal(len(rows_a))
        ys[rows_a] = yhat + K @ eps
        return ys

    out = {"null": "y_s = L q_hat + K eps on the NGC 4258-only rows, under C"}

    # tau part
    if re_out.get("status") != "evaluated":
        out["tau"] = {"status": "not evaluable (R2-RE not evaluable)"}
    else:
        tau_obs = re_out["tau_hat"]
        t0 = time.perf_counter()
        taus, failed = [], 0
        for s in range(P["rob_n_tau"]):
            ys = simulate(s)
            try:
                est = fns["reml_tau"](lambda t: fns["reml_m2l"](L, ys, C, rows_a, calib_groups, t),
                                      P["re_tau_max"], P["re_grid_step"], interval=False)
                taus.append(est["tau_hat"])
            except (np.linalg.LinAlgError, ValueError) as e:
                if not fns["is_fit_failure"](e):
                    raise
                failed += 1
            if s % 50 == 49:
                log(f"  R2-RE-ROB B tau: {s + 1} sims, {time.perf_counter() - t0:.0f} s")
        n, k = len(taus), int(np.sum(np.array(taus) >= tau_obs))
        tau_rec = {"tau_obs": tau_obs, "n_sims": P["rob_n_tau"], "n_ok": n, "n_failed": failed, "k": k,
                   "taus": [round(t, 5) for t in taus]}
        if failed > P["rob_max_failed"]:
            tau_rec["status"] = "not evaluable (too many failed fits)"
        else:
            label, ci = three_way(k, n, "tau_hat unusual under C (excess calibrator scatter)",
                                  "tau_hat not unusual under C")
            tau_rec.update(status="evaluated", p=(1 + k) / (1 + n), ci95=list(ci), label=label)
        out["tau"] = tau_rec

    # spread part: linear estimator rows for the first rob_n_subsets R4 subsets
    if not picks:
        out["spread"] = {"status": "not evaluable (R4 has no draws)"}
        return out
    use = picks[:P["rob_n_subsets"]]
    rows_full = rows_a
    sa2 = float(res_full["sigma"][fns["C_H0"]]) ** 2
    M = np.zeros((len(use), len(rows_full)))
    sig = np.zeros(len(use))
    pos = {r: i for i, r in enumerate(rows_full)}
    for i, pick in enumerate(use):
        rows = np.union1d(base_rows, np.concatenate([host_rows[j] for j in pick]))
        res = fns["fit"](L, y, C, rows, est=True)
        a = fns["shift_vector"](res, rows, res_full, rows_full)
        M[i] = a[rows_full]
        sig[i] = np.sqrt(float(res["sigma"][fns["C_H0"]]) ** 2 - sa2)
        if i == 0:   # the shift vector covers only rows_a (subset rows are a subset of rows_a)
            outside = np.setdiff1d(np.flatnonzero(a), rows_full)
            if outside.size:
                raise RuntimeError("subset shift vector has weight outside rows_a")
    spread_obs = float(np.std((M @ y[rows_full]) / sig))
    sp = []
    for s in range(P["rob_n_spread"]):
        eps = np.random.default_rng(P["rob_seed_base"] + s).standard_normal(len(rows_full))
        ys = yhat + K @ eps
        sp.append(float(np.std((M @ ys) / sig)))
    k = int(np.sum(np.array(sp) >= spread_obs))
    label, ci = three_way(k, len(sp), "the R4 excess spread is unusual under C",
                          "the R4 spread is consistent with C")
    out["spread"] = {"status": "evaluated", "n_subsets": len(use), "spread_obs": spread_obs,
                     "n_sims": len(sp), "k": k, "p": (1 + k) / (1 + len(sp)), "ci95": list(ci),
                     "label": label, "sim_quantiles": [float(q) for q in np.percentile(sp, [5, 50, 95])]}
    return out
