"""R6-SHUF-KA (README section 2.9, T-047 flow part): a known-answer test of R6-SHUF's phi.

Project-environment side (no TensorFlow). The flows run through r6flow.run_jobs (job folder, caching and cleanup
as R6) with plan() below; flowshift.py's 'ka' jobs train one flow on one variant ("6", "S", "5") of the synthetic
family at one seed. The exact values are recomputed here with flowshift.ka_exact (numpy/scipy only). This module
checks the recorded results/r6.json and results/r6_shuf.json (read, never written), applies the label rules 1-4 and
the qualifier of R6-SHUF, and assembles results/r6_ka.json. It does not import run.py; run.py passes PARAMS in.
"""
import json
import math
from pathlib import Path

import numpy as np

import r6shuf

VARIANTS = ("6", "S", "5")
EXACT_TOL = 0.005                       # README 2.9 rule 1: recomputed exact values within 0.005
EXACT_SEED = 999                        # D6 draws for the exact values; DS permutation default_rng(1000)
EXACT_N = 2_000_000

NE = "not evaluable"
OVER = "flows overestimate φ"
UNDER = "flows underestimate φ"
NONE = "no bias of φ detected"
Q_HOLDS = "R6-SHUF's label holds after the known-answer correction"
Q_REVERSES = "R6-SHUF's label reverses after the known-answer correction"
Q_NOISY = "known-answer correction not decisive (test too noisy)"
Q_UNDECIDED = "R6-SHUF's label is not decided after the known-answer correction"
_good = r6shuf._good
_num = r6shuf._num


# ------------------------------------------------------------------ records ----
def check_shuf(path):
    """README 2.9: the recorded results/r6_shuf.json must exist with its recorded label and give the unrounded
    phi mean and s over five seeds (quantities.phi.mean, .s). Never writes."""
    path = Path(path)
    if not path.exists():
        return {"ok": False, "reason": "results/r6_shuf.json missing"}
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        return {"ok": False, "reason": f"results/r6_shuf.json unreadable ({type(exc).__name__})"}
    if d.get("label") != r6shuf.CORR:
        return {"ok": False, "reason": f"results/r6_shuf.json label differs from the recorded one ({d.get('label')!r})"}
    phi = (d.get("quantities") or {}).get("phi") or {}
    vals = phi.get("values")
    if not (isinstance(vals, list) and len(vals) == 5 and _num(phi.get("mean")) and _num(phi.get("s"))):
        return {"ok": False, "reason": "results/r6_shuf.json has no phi mean and s over five seeds"}
    if not (all(_num(v) for v in vals) and abs(float(np.mean(vals)) - phi["mean"]) <= 1e-12
            and abs(float(np.std(vals, ddof=1)) - phi["s"]) <= 1e-12):
        return {"ok": False, "reason": "results/r6_shuf.json: phi mean or s does not match its five values"}
    fl = d.get("flows") or {}
    return {"ok": True, "phi_bar": float(phi["mean"]), "s_phi": float(phi["s"]), "n": len(vals),
            "label": d["label"], "versions": fl.get("versions"), "settings": fl.get("settings")}


def env_matches(res, rec6, recs):
    """README 2.9 rule 1: the run's versions and flow settings equal those recorded in r6.json and r6_shuf.json."""
    run = {"versions": res.get("versions"), "settings": res.get("settings")}
    out = {"run": run, "equal_r6": run == {"versions": rec6.get("versions"), "settings": rec6.get("settings")},
           "equal_r6_shuf": run == {"versions": recs.get("versions"), "settings": recs.get("settings")}}
    present = all(isinstance(x.get(key), dict) and x.get(key) for x in (run, rec6, recs)
                  for key in ("versions", "settings"))
    out["ok"] = bool(present and out["equal_r6"] and out["equal_r6_shuf"])
    return out


# ------------------------------------------------------------------ configuration, exact values, plan ----
def config(seeds, n, estimate, family, offsets):
    """Job configuration for r6flow.run_jobs (no 'pop_size' anywhere: flow_from_chain is called as in R6)."""
    return {"n": n, "estimate": estimate,
            "ka": {"seeds": list(seeds), "family": family, "offsets": list(offsets)}}


def exact_values(family, flowshift):
    """README 2.9: the exact values recomputed with the design script's code (flowshift.ka_exact)."""
    e = flowshift.ka_exact(family, n=EXACT_N, seed=EXACT_SEED)
    return {"n6": e["6"], "S": e["S"], "n5": e["5"], "phi": e["phi"]}


def exact_check(exact, registered):
    diffs = {k: abs(exact[k] - registered[k]) for k in ("n6", "S", "n5")}
    return {"recomputed": exact, "registered": registered, "abs_diff": diffs, "tolerance": EXACT_TOL,
            "ok": all(v <= EXACT_TOL for v in diffs.values())}


def plan(job, cfg, log, flowshift, expected=None):
    """README 2.9 order: the environment (meta); if it differs from the records (expected = (rec6, recs)), nothing
    is trained (rule 1 decides); else for each seed the three variants "6", "S", "5"."""
    ka = cfg["ka"]

    def one(*parts):
        try:
            return job(*parts)
        except RuntimeError:
            return {"seed": parts[-1], "error": "subprocess failed"}

    res = job("meta")
    if expected is not None and not env_matches(res, *expected)["ok"]:
        res["status_runs"] = "not run (versions or flow settings differ from the recorded ones)"
        return res
    for v in VARIANTS:
        res[v] = []
    for k in ka["seeds"]:
        for v in VARIANTS:
            r = one("ka", v, k)
            res[v].append(r)
            log(f"  R6-SHUF-KA seed {k} variant {v}: {r.get('n_sigma', r.get('error'))}")
    return res


# ------------------------------------------------------------------ rules ----
def _stats(v):
    v = [float(x) for x in v]
    return {"values": v, "mean": float(np.mean(v)) if v else None,
            "s": float(np.std(v, ddof=1)) if len(v) > 1 else None}


def label(env_ok, exact_ok, recs_ok, reps, seeds, phi_exact, e_min, s_max):
    """README 2.9 label rules 1-4, in order. reps: variant -> repetition list. Returns (label, reason, numbers)."""
    if not recs_ok:
        return NE, "results/r6_shuf.json missing or its label differs from the recorded one", {}
    if not env_ok:
        return NE, "versions or flow settings differ from the recorded ones", {}
    if not exact_ok:
        return NE, f"a recomputed exact value differs from the registered one by more than {EXACT_TOL}", {}
    for v in VARIANTS:                                                          # rule 2
        r = reps.get(v)
        if not r or [x.get("seed") for x in r] != list(seeds) or not all(_good(x) for x in r):
            return NE, f"a ({v}) training failed, is non-finite, has not converged or is a lower bound", {}
    if len(seeds) < 2:
        return NE, "fewer than two seeds (s_b undefined)", {}
    n = {v: {int(x["seed"]): float(x["n_sigma"]) for x in reps[v]} for v in VARIANTS}
    e = {k: n["6"][k] - n["5"][k] for k in seeds}
    if any(x <= e_min for x in e.values()):                                     # rule 3
        return NE, f"an E_k <= {e_min} (min {min(e.values()):.4f})", {"E": e}
    phi = {k: (n["6"][k] - n["S"][k]) / e[k] for k in seeds}
    b = [phi[k] - phi_exact for k in seeds]
    m, s = float(np.mean(b)), float(np.std(b, ddof=1))
    nums = {"E": e, "phi": phi, "b_bar": m, "s_b": s}
    if s > s_max:
        return NE, f"s_b = {s:.4f} > {s_max}", nums
    half = 2.0 * s / math.sqrt(len(b))                                          # rule 4
    lo, hi = m - half, m + half
    nums.update(half_width=half, interval_b=[lo, hi])
    if lo > 0:
        return f"{OVER} (bias {m:+.3f})", f"I_b = [{lo:.4f}, {hi:.4f}] within (0, inf)", nums
    if hi < 0:
        return f"{UNDER} (bias {m:+.3f})", f"I_b = [{lo:.4f}, {hi:.4f}] within (-inf, 0)", nums
    return f"{NONE} (I_b = [{lo:.3f}, {hi:.3f}])", f"I_b = [{lo:.4f}, {hi:.4f}] contains 0", nums


def qualifier(phi_r6, s_r6, n_r6, b_bar, s_b, n_b, band):
    """README 2.9 qualifier of R6-SHUF: w = 2 sqrt(s_R6^2/n_R6 + s_b^2/n_b), I_corr = (phi_R6 - b_bar) +- w; holds,
    reverses, then (phi_R6 - w < hi_band: test too noisy), else not decided."""
    lo_b, hi_b = band
    w = 2.0 * math.sqrt(s_r6 ** 2 / n_r6 + s_b ** 2 / n_b)
    c = phi_r6 - b_bar
    lo, hi = c - w, c + w
    out = {"w": w, "phi_corrected": c, "interval": [lo, hi], "phi_r6": phi_r6, "s_r6": s_r6, "n_r6": n_r6}
    if lo >= hi_b:
        out["qualifier"] = Q_HOLDS
    elif hi <= lo_b:
        out["qualifier"] = Q_REVERSES
    elif phi_r6 - w < hi_b:
        out["qualifier"] = f"{Q_NOISY[:-1]}: w = {w:.3f})"
    else:
        out["qualifier"] = Q_UNDECIDED
    return out


def assemble(res, rec6, recs, exact, registered, seeds, e_min, s_max, band, settings):
    """results/r6_ka.json: the label, the qualifier and everything README 2.9 reports."""
    out = {"settings": settings,
           "records": {"r6": {"path": "results/r6.json", "ok": bool(rec6.get("ok")), "reason": rec6.get("reason"),
                              **{k: rec6.get(k) for k in ("versions", "settings")}},
                       "r6_shuf": {"path": "results/r6_shuf.json", **recs}},
           "flows": res}
    ex = exact_check(exact, registered) if exact else {"ok": False, "reason": "not computed"}
    out["exact"] = ex
    if "status" in res:
        out.update(label=NE, reason=res["status"])
        return _summary(out)
    env = env_matches(res, rec6, recs) if rec6.get("ok") and recs.get("ok") else {"ok": False}
    out["environment"] = env
    reps = {v: res.get(v) for v in VARIANTS}
    phi_exact = ex["recomputed"]["phi"] if ex.get("recomputed") else None
    lab, why, nums = label(bool(env.get("ok")), bool(ex.get("ok")), bool(recs.get("ok") and rec6.get("ok")), reps,
                           seeds, phi_exact if phi_exact is not None else float("nan"), e_min, s_max)
    out.update(label=lab, reason=why, numbers=nums)
    if lab != NE and "b_bar" in nums:
        out["qualifier"] = qualifier(recs["phi_bar"], recs["s_phi"], recs["n"], nums["b_bar"], nums["s_b"],
                                     len(seeds), band)
    # descriptive: per-variant mean offsets from the exact values, whatever the label
    per = {v: {int(x["seed"]): float(x["n_sigma"]) for x in (reps.get(v) or []) if _good(x)} for v in VARIANTS}
    key = {"6": "n6", "S": "S", "5": "n5"}
    if ex.get("recomputed"):
        out["offsets"] = {v: _stats([x - ex["recomputed"][key[v]] for x in per[v].values()]) for v in VARIANTS}
    out["per_seed"] = {str(k): {v: per[v].get(k) for v in VARIANTS} for k in seeds}
    return _summary(out)


def _summary(out):
    nums = out.get("numbers") or {}
    q = out.get("qualifier") or {}
    out["summary"] = {"label": out["label"], "reason": out["reason"], "b_bar": nums.get("b_bar"),
                      "s_b": nums.get("s_b"), "interval_b": nums.get("interval_b"),
                      "qualifier": q.get("qualifier"), "w": q.get("w"), "interval_corrected": q.get("interval")}
    return out
