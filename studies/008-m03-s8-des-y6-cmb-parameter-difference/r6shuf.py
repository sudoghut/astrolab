"""R6-SHUF (README section 2.8, T-044): what Sigma m_nu adds to the full-space difference.

Project-environment side (no TensorFlow). The flows run through r6flow.run_jobs (job folder, caching
and cleanup as R6) with plan() below; flowshift.py does the TensorFlow work (variant_difference,
knn_nsigma_multi, the low-shift gate through its named-gate jobs). This module checks the recorded
results/r6.json and results/r6_nomnu.json for reuse (neither is retrained or rewritten), compares the
environment with both, applies the label rules 1-6 and assembles results/r6_shuf.json. It does not
import run.py; run.py passes PARAMS in.
"""
import json
import math
from pathlib import Path

import numpy as np

# README 2.8: what the recorded files must show to be reused (checks of files, not tunables)
R6_EXPECT = {"seeds": [0, 1, 2, 3, 4], "n_bar": 1.6985, "s": 0.0977, "decimals": 4}
NOMNU_EXPECT = {"seeds": [0, 1, 2, 3, 4], "n_bar": 0.5236, "s": 0.0402, "decimals": 4}
MNU = "mnu"
DET_SEED = 0            # README 2.8 determinism check: R6 seed 0, no column change
DET_TOL = 0.02          # |n - recorded| > 0.02 -> flag "cross-run pairing approximate"
EXACT_DECIMALS = 4      # the recorded low-shift exact value 0.8601 is given to 4 decimals

NE = "not evaluable"
NE_GATE = "not evaluable (low-shift gate)"
CORR = "what Σmν adds is mainly through its correlations with the other DES parameters"
NOT_CORR = ("what Σmν adds is mainly not through its DES-side correlations (the Σmν direction itself, "
            "including the CMB side and the prior)")
BETWEEN = "between the two labels (not decided)"
FLAG_DET = "cross-run pairing approximate"


def _num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def _good(r):
    """A repetition that is finite, converged and not a lower bound."""
    return (isinstance(r, dict) and "error" not in r and _num(r.get("n_sigma"))
            and r.get("converged") is True and not r.get("lower_bound"))


# ------------------------------------------------------------------ reuse of the records ----
def _load(path, name):
    path = Path(path)
    if not path.exists():
        return None, f"results/{name} missing"
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        return None, f"results/{name} unreadable ({type(exc).__name__})"
    if not isinstance(d, dict) or not isinstance(d.get("flows"), dict):
        return None, f"{name}: no flows"
    return d, None


def _check_case(name, flows, gate_key, case_key, expect):
    if flows.get("complete") is not True:
        return f"{name}: flows.complete is not true"
    gate = flows.get(gate_key)
    if not isinstance(gate, dict) or gate.get("passed") is not True:
        return f"{name}: flows.{gate_key}.passed is not true"
    case = flows.get(case_key)
    reps = case.get("repetitions") if isinstance(case, dict) else None
    if not isinstance(reps, list) or not all(isinstance(r, dict) for r in reps) \
            or [r.get("seed") for r in reps] != expect["seeds"]:
        return f"{name}: flows.{case_key} does not hold five repetitions for seeds 0-4"
    if not all(_good(r) for r in reps):
        return f"{name}: a flows.{case_key} repetition is not finite, not converged or a lower bound"
    d = expect["decimals"]
    for key in ("n_bar", "s"):
        v = case.get(key)
        if not _num(v) or round(v, d) != round(expect[key], d):
            return f"{name}: flows.{case_key}.{key} is not {expect[key]} to {d} decimals"
    return None


def _env(flows):
    return {"versions": flows.get("versions"), "settings": flows.get("settings")}


def check_r6(path):
    """README 2.8: the recorded r6.json, checked as section 2.6/2.7 and 2.8 name it (also converged and
    not a lower bound). Returns {"ok": True, "per_seed": {k: n6_k}, ...} or {"ok": False, "reason"}.
    Never writes."""
    d, why = _load(path, "r6.json")
    if d is None:
        return {"ok": False, "reason": why}
    why = _check_case("r6.json", d["flows"], "gate", "main", R6_EXPECT)
    if why:
        return {"ok": False, "reason": why}
    main = d["flows"]["main"]
    return {"ok": True, "n_bar": main["n_bar"], "s": main["s"],
            "per_seed": {int(r["seed"]): float(r["n_sigma"]) for r in main["repetitions"]},
            "parameters": main.get("parameters"), "gate_exact": (d["flows"]["gate"].get("exact") or {}).get("n_sigma"),
            "verdict": d.get("verdict"), **_env(d["flows"])}


def check_nomnu(path):
    """README 2.8: the recorded r6_nomnu.json, default case only (flows.complete, flows.gate5.passed,
    flows.nomnu seeds 0-4 finite, converged, not lower bounds, n_bar 0.5236 and s 0.0402 to 4 decimals;
    not the pop_size = 1 cases). Never writes."""
    d, why = _load(path, "r6_nomnu.json")
    if d is None:
        return {"ok": False, "reason": why}
    why = _check_case("r6_nomnu.json", d["flows"], "gate5", "nomnu", NOMNU_EXPECT)
    if why:
        return {"ok": False, "reason": why}
    case = d["flows"]["nomnu"]
    return {"ok": True, "n_bar": case["n_bar"], "s": case["s"],
            "per_seed": {int(r["seed"]): float(r["n_sigma"]) for r in case["repetitions"]},
            "parameters": d.get("parameters"), "parameters5": case.get("parameters"),
            "label": d.get("label"), **_env(d["flows"])}


def env_matches(res, rec6, rec5):
    """README 2.8 rule 1: the run's versions and flow settings equal those in both recorded files."""
    run = {"versions": res.get("versions"), "settings": res.get("settings")}
    out = {"run": run, "equal_r6": run == {"versions": rec6.get("versions"), "settings": rec6.get("settings")},
           "equal_r6_nomnu": run == {"versions": rec5.get("versions"), "settings": rec5.get("settings")}}
    out["ok"] = bool(run["versions"] is not None and out["equal_r6"] and out["equal_r6_nomnu"])
    return out


# ------------------------------------------------------------------ configuration and plan ----
def low_gate(gate6, gate_param):
    """README 2.8: R6's 6-D synthetic distribution with the curved pair moved to (mu1, mu2); curvature,
    boxes, exact draws, seeds and tolerances unchanged."""
    return {**gate6, "mu1": gate_param["mu1"], "mu2": gate_param["mu2"]}


def config(short, seeds, n, estimate, gate6, gate_param, offsets, prior, knn_k):
    """Job configuration for r6flow.run_jobs. No 'pop_size' key anywhere: flow_from_chain is called as in
    R6 (tensiometer's defaults)."""
    if MNU not in short:
        raise ValueError("no Sigma m_nu column")
    return {"n": n, "estimate": estimate, "gates": {"low": low_gate(gate6, gate_param)},
            "shuf": {"columns": list(short), "mnu": MNU, "seeds": list(seeds), "offsets": list(offsets),
                     "prior": list(prior), "knn_k": list(knn_k), "det_seed": DET_SEED}}


def plan(job, cfg, log, flowshift, expected=None):
    """README 2.8 order: the environment (meta), the low-shift gate (exact value, seeds 10-12), then (S),
    (P), (SS) for each seed and the determinism job; (S) and (P) also run if the low-shift gate failed
    (descriptive). Then the kNN values (descriptive). If `expected` = (rec6, rec5) is given and the
    environment differs from it, nothing is trained (rule 1 would decide "not evaluable" anyway)."""
    sc = cfg["shuf"]

    def descriptive(*parts):
        try:
            return job(*parts)
        except RuntimeError:
            return {"seed": parts[-1], "error": "subprocess failed"}

    res = job("meta")
    if expected is not None and not env_matches(res, *expected)["ok"]:
        res["status_runs"] = "not run (versions or flow settings differ from the recorded ones)"
        return res
    exact = job("exact", "low")
    reps = []
    for k in cfg["gates"]["low"]["seeds"]:
        # a crashed gate repetition counts as failed (README 2.8 rule 2), so the variants still run
        r = descriptive("gate", "low", k)
        reps.append(r)
        log(f"  low-shift gate seed {k}: {r.get('n_sigma', r.get('error'))} (exact {exact['n_sigma']:.4f})")
    res["gate_low"] = flowshift.gate_summary(exact, reps, cfg["gates"]["low"])
    for variant in ("S", "P", "SS"):
        log(f"variant {variant}: seeds {sc['seeds']}")
        vreps = []
        for k in sc["seeds"]:
            r = descriptive("shuf", variant, k) if variant == "SS" else job("shuf", variant, k)
            vreps.append(r)
            log(f"  {variant} seed {k}: {r.get('n_sigma', r.get('error'))}")
        res[variant] = flowshift.case_summary(vreps, sc["columns"])
    res["determinism"] = descriptive("shuf", "none", sc["det_seed"])
    log(f"  determinism (seed {sc['det_seed']}, no change): {res['determinism'].get('n_sigma')}")
    res["knn"] = [descriptive("knn", k) for k in sc["seeds"]]
    return res


# ------------------------------------------------------------------ quantities and rules ----
def chi2_equiv(n_sigma, dof):
    """README 2.7 mapping: the chi^2 with `dof` degrees of freedom whose upper-tail probability equals the
    two-sided Gaussian tail probability of n_sigma."""
    from scipy.special import erfc
    from scipy.stats import chi2
    return float(chi2.isf(erfc(n_sigma / math.sqrt(2.0)), dof))


def _stats(v):
    v = [float(x) for x in v]
    return {"values": v, "mean": float(np.mean(v)) if v else None,
            "s": float(np.std(v, ddof=1)) if len(v) > 1 else None}


def quantities(n6, n5, ns, np_):
    """README 2.8, per seed (dicts seed -> n_sigma): E, phi, psi, rho and phi on the chi^2 scale
    (6 dof for n6 and n_S, 5 for n5). E_k <= 0 gives None ratios for that seed."""
    seeds = sorted(set(n6) & set(n5) & set(ns) & set(np_))
    per = {}
    for k in seeds:
        e = n6[k] - n5[k]
        row = {"E": e}
        if e != 0:
            row.update(phi=(n6[k] - ns[k]) / e, psi=(ns[k] - np_[k]) / e, rho=(np_[k] - n5[k]) / e)
        c6, cs, c5 = chi2_equiv(n6[k], 6), chi2_equiv(ns[k], 6), chi2_equiv(n5[k], 5)
        row["chi2"] = {"n6": c6, "S": cs, "n5": c5}
        row["phi_chi2"] = (c6 - cs) / (c6 - c5) if c6 != c5 else None
        per[str(k)] = row
    out = {"seeds": seeds, "per_seed": per}
    for q in ("E", "phi", "psi", "rho", "phi_chi2"):
        vals = [per[str(k)].get(q) for k in seeds]
        out[q] = _stats(vals) if vals and all(_num(x) for x in vals) else None
    return out


def _per_seed(reps):
    return {int(r["seed"]): float(r["n_sigma"]) for r in reps or [] if _good(r)}


def label(gate_r1, records_ok, env_ok, gate_low_passed, reps_s, reps_p, n6, n5, seeds, e_min, s_max, band):
    """README 2.8 label rules 1-6, in order. reps_*: repetition lists; n6, n5: seed -> n_sigma from the
    records. Returns (label, reason, numbers)."""
    lo_b, hi_b = band
    if not gate_r1:
        return NE, "R1 gate failed", {}
    if not records_ok or not all(k in n6 and k in n5 for k in seeds):
        return NE, "the R6 or R6-NOMNU record failed its checks", {}
    if not env_ok:
        return NE, "versions or flow settings differ from the recorded ones", {}
    if not gate_low_passed:                                                   # rule 2
        return NE_GATE, "low-shift known-answer gate failed (variants descriptive only)", {}
    for name, reps in (("S", reps_s), ("P", reps_p)):                          # rule 3
        if not reps or [r.get("seed") for r in reps] != list(seeds) or not all(_good(r) for r in reps):
            return NE, f"a ({name}) repetition failed, is non-finite, has not converged or is a lower bound", {}
    ns, np_ = _per_seed(reps_s), _per_seed(reps_p)
    e = {k: n6[k] - n5[k] for k in seeds}
    if any(v <= e_min for v in e.values()):                                    # rule 4
        return NE, f"an E_k <= {e_min} (min {min(e.values()):.4f})", {"E": e}
    phi = [(n6[k] - ns[k]) / e[k] for k in seeds]
    m, s = float(np.mean(phi)), float(np.std(phi, ddof=1))
    nums = {"phi_bar": m, "s_phi": s}
    if s > s_max:                                                              # rule 5
        return NE, f"s_phi = {s:.4f} > {s_max}", nums
    half = 2.0 * s / math.sqrt(len(phi))                                       # rule 6
    lo, hi = m - half, m + half
    nums.update(half_width=half, interval=[lo, hi])
    if lo >= hi_b:
        return CORR, f"I_phi = [{lo:.4f}, {hi:.4f}] within [{hi_b}, inf)", nums
    if hi <= lo_b:
        return NOT_CORR, f"I_phi = [{lo:.4f}, {hi:.4f}] within (-inf, {lo_b}]", nums
    return BETWEEN, f"I_phi = [{lo:.4f}, {hi:.4f}] reaches into ({lo_b}, {hi_b})", nums


def determinism(rep, rec6):
    """README 2.8 determinism check (reported only): seed 0 through the new draw path, no column change,
    against the recorded R6 seed-0 value."""
    ref = (rec6.get("per_seed") or {}).get(DET_SEED)
    out = {"seed": DET_SEED, "recorded": ref, "tolerance": DET_TOL, "repetition": rep}
    if not isinstance(rep, dict) or not _num(rep.get("n_sigma")) or not _num(ref):
        out.update(difference=None, flag=None, status="not available (failed or no record)")
        return out
    diff = float(rep["n_sigma"]) - float(ref)
    out.update(difference=diff, flag=FLAG_DET if abs(diff) > DET_TOL else None)
    return out


def _case_reps(res, name):
    c = res.get(name)
    return c.get("repetitions") if isinstance(c, dict) else None


def _knn_table(knn):
    """seed -> variant -> [k values] from the kNN jobs (descriptive)."""
    out = {}
    for r in knn or []:
        if isinstance(r, dict):
            out[str(r.get("seed"))] = r.get("n_sigma") if "error" not in r else {"error": r["error"]}
    return out


def assemble(res, rec6, rec5, gate_r1, seeds, e_min, s_max, band, gate_param, settings):
    """results/r6_shuf.json: the label and everything README 2.8 reports."""
    records_ok = bool(rec6.get("ok") and rec5.get("ok"))
    out = {"settings": settings,
           "records": {"r6": {"path": "results/r6.json", "ok": bool(rec6.get("ok")), "reason": rec6.get("reason"),
                              **{k: rec6.get(k) for k in ("n_bar", "s", "per_seed", "parameters", "versions",
                                                          "settings")}},
                       "r6_nomnu": {"path": "results/r6_nomnu.json", "ok": bool(rec5.get("ok")),
                                    "reason": rec5.get("reason"),
                                    **{k: rec5.get(k) for k in ("n_bar", "s", "per_seed", "parameters",
                                                                "versions", "settings")}}},
           "flows": res}
    if not records_ok:
        out.update(label=NE, reason=rec6.get("reason") if not rec6.get("ok") else rec5.get("reason"))
        return _summary(out)
    if "status" in res:
        out.update(label=NE, reason=res["status"])
        return _summary(out)
    env = env_matches(res, rec6, rec5)
    out["environment"] = env
    n6, n5 = rec6["per_seed"], rec5["per_seed"]
    if not env["ok"] or "gate_low" not in res:
        out.update(label=NE, reason="versions or flow settings differ from the recorded ones")
        return _summary(out)
    g = res["gate_low"]
    rec_exact = gate_param["exact"]
    new_exact = (g.get("exact") or {}).get("n_sigma")
    out["gate_low_exact"] = {"recomputed": new_exact, "recorded": rec_exact,
                             "equal_to_4_decimals": _num(new_exact)
                             and round(new_exact, EXACT_DECIMALS) == round(rec_exact, EXACT_DECIMALS)}
    reps_s, reps_p = _case_reps(res, "S"), _case_reps(res, "P")
    lab, why, nums = label(gate_r1, records_ok, True, bool(g.get("passed")), reps_s, reps_p, n6, n5, seeds,
                           e_min, s_max, band)
    out.update(label=lab, reason=why, numbers=nums)
    # descriptive: everything that can be computed, whatever the label
    out["means"] = {v: {"n_bar": (res.get(v) or {}).get("n_bar"), "s": (res.get(v) or {}).get("s")}
                    for v in ("S", "P", "SS")}
    out["quantities"] = quantities(n6, n5, _per_seed(reps_s), _per_seed(reps_p))
    out["paired_minus_r6"] = {v: {str(k): n - n6[k] for k, n in _per_seed(_case_reps(res, v)).items() if k in n6}
                              for v in ("S", "P", "SS")}
    out["determinism"] = determinism(res.get("determinism"), rec6)
    out["flags"] = [out["determinism"]["flag"]] if out["determinism"].get("flag") else []
    out["knn"] = {"k": settings.get("r6_shuf_knn_k") if isinstance(settings, dict) else None,
                  "per_seed": _knn_table(res.get("knn")),
                  "note": "descriptive; the kNN estimator is not calibrated (README 2.8)"}
    return _summary(out)


def _summary(out):
    nums = out.get("numbers") or {}
    q = out.get("quantities") or {}
    out["summary"] = {"label": out["label"], "reason": out["reason"], "phi_bar": nums.get("phi_bar"),
                      "s_phi": nums.get("s_phi"), "interval": nums.get("interval"),
                      "psi_bar": (q.get("psi") or {}).get("mean"), "rho_bar": (q.get("rho") or {}).get("mean"),
                      "flags": out.get("flags", []),
                      "records_ok": {"r6": out["records"]["r6"]["ok"], "r6_nomnu": out["records"]["r6_nomnu"]["ok"]}}
    return out
