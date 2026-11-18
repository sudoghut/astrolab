"""R6-NOMNU (README section 2.7, T-040): the full-space difference without Sigma m_nu, and pop_size = 1.

Project-environment side. The flows run through r6flow.run_jobs (the same job folder, caching and
cleanup as R6) with plan() below; flowshift.py does the TensorFlow work. This module also checks the
recorded results/r6.json for reuse (R6 is not retrained), applies the label rules 1-6 and the pop_size
comparison, and assembles results/r6_nomnu.json. It does not import run.py; run.py passes PARAMS in.
"""
import json
import math
from pathlib import Path

import numpy as np

# README 2.7: what the recorded r6.json must show to be reused (a check of a file, not a tunable)
R6_EXPECT = {"seeds": [0, 1, 2, 3, 4], "n_bar": 1.69853, "s": 0.0977, "decimals": 4}
EDGE_BOX = 3            # README 2.7: the 5-D gate drops boxes[3] = [-0.1, 1.9, 0.1] (the Sigma m_nu-like edge)
DROPPED = "mnu"

NE = "not evaluable"
MAINLY = "the full-space shift is mainly the Σmν direction"
NOT_MAINLY = "not mainly Σmν: the other directions carry most of the shift"
PARTLY = "partly the Σmν direction"
BETWEEN = "between the two adjacent labels (not decided)"


def _num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


# ------------------------------------------------------------------ reuse of R6 ----
def check_r6(path):
    """README 2.7 reuse path: load the recorded r6.json and check it exactly as written. Returns
    {"ok": True, ...R6 numbers} or {"ok": False, "reason": ...}. Never writes."""
    path = Path(path)
    if not path.exists():
        return {"ok": False, "reason": "results/r6.json missing"}
    try:
        r6 = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        return {"ok": False, "reason": f"results/r6.json unreadable ({type(exc).__name__})"}
    flows = r6.get("flows") if isinstance(r6, dict) else None
    if not isinstance(flows, dict) or flows.get("complete") is not True:
        return {"ok": False, "reason": "r6.json: flows.complete is not true"}
    gate = flows.get("gate")
    if not isinstance(gate, dict) or gate.get("passed") is not True:
        return {"ok": False, "reason": "r6.json: flows.gate.passed is not true"}
    main = flows.get("main")
    reps = main.get("repetitions") if isinstance(main, dict) else None
    if not isinstance(reps, list) or not all(isinstance(r, dict) for r in reps) \
            or [r.get("seed") for r in reps] != R6_EXPECT["seeds"]:
        return {"ok": False, "reason": "r6.json: flows.main does not hold five repetitions for seeds 0-4"}
    if not all(_num(r.get("n_sigma")) for r in reps):
        return {"ok": False, "reason": "r6.json: a flows.main repetition is not finite"}
    d = R6_EXPECT["decimals"]
    n_bar, s = main.get("n_bar"), main.get("s")
    if not _num(n_bar) or round(n_bar, d) != round(R6_EXPECT["n_bar"], d):
        return {"ok": False, "reason": f"r6.json: flows.main.n_bar is not {R6_EXPECT['n_bar']} to {d} decimals"}
    if not _num(s) or round(s, d) != round(R6_EXPECT["s"], d):
        return {"ok": False, "reason": f"r6.json: flows.main.s is not {R6_EXPECT['s']} to {d} decimals"}
    exact = (gate.get("exact") or {}).get("n_sigma")
    return {"ok": True, "n_bar": n_bar, "s": s, "repetitions": reps,
            "per_seed": {int(r["seed"]): r["n_sigma"] for r in reps},
            "parameters": main.get("parameters"), "gate_exact": exact,
            "gate_mean": gate.get("mean"), "verdict": r6.get("verdict"), "reason": r6.get("reason")}


# ------------------------------------------------------------------ configuration ----
def gate5(gate6):
    """README 2.7: R6's synthetic gate without the edge box boxes[3]; same generators, so the 5-D
    rows equal R6's first five columns."""
    boxes = [list(b) for b in gate6["boxes"]]
    dropped = boxes.pop(EDGE_BOX)
    return {**gate6, "boxes": boxes}, dropped


def gate_settings(gate6):
    """The gate configuration saved with the results (README 2.7: 5-D gate = R6's without boxes[3])."""
    g5, dropped = gate5(gate6)
    return {"gate5": g5, "gate6": gate6, "dropped_box_index": EDGE_BOX, "dropped_box": dropped}


def config(short, seeds, n, estimate, gate6, pop1):
    """Job configuration for r6flow.run_jobs. 'pop_size': None = not passed (tensiometer's default,
    as in R6) but recorded; 1 = passed explicitly."""
    five = [c for c in short if c != DROPPED]
    g5, _ = gate5(gate6)
    gates = {"g5": {**g5, "pop_size": None}}
    cases = {"nomnu": {"columns": five, "seeds": list(seeds), "pop_size": None}}
    if pop1:
        gates["g5_pop1"] = {**g5, "pop_size": 1}
        gates["g6_pop1"] = {**gate6, "pop_size": 1}
        cases["nomnu_pop1"] = {"columns": five, "seeds": list(seeds), "pop_size": 1}
        cases["main_pop1"] = {"columns": list(short), "seeds": list(seeds), "pop_size": 1}
    return {"n": n, "estimate": estimate, "gates": gates, "cases": cases}


def plan(job, cfg, log, flowshift):
    """README 2.7 runs in order: (a) 5-D gate, default; (b) 5-D chains, default, only if (a) passed;
    (c) 5-D and 6-D gates with pop_size = 1; (d) 5-D and 6-D chains with pop_size = 1 (descriptive;
    (c) does not gate (d))."""
    gates, cases = cfg["gates"], cfg["cases"]

    def run(descriptive, *parts):
        """A crashed subprocess in a descriptive job ((c), (d)) is recorded as a failed repetition;
        in (a) and (b) it propagates (run_jobs then reports "not evaluable")."""
        if not descriptive:
            return job(*parts)
        try:
            return job(*parts)
        except RuntimeError:
            return {"seed": parts[-1], "error": "subprocess failed"}

    def gate(name, exact, descriptive=False):
        reps = []
        for k in gates[name]["seeds"]:
            r = run(descriptive, "gate", name, k)
            reps.append(r)
            log(f"  {name} seed {k}: {r.get('n_sigma', r.get('error'))} (exact {exact['n_sigma']:.4f})")
        return flowshift.gate_summary(exact, reps, gates[name])

    def case(name, descriptive=False):
        log(f"case {name}: {cases[name]['columns']}")
        reps = []
        for k in cases[name]["seeds"]:
            r = run(descriptive, "case", name, k)
            reps.append(r)
            log(f"  {name} seed {k}: {r.get('n_sigma', r.get('error'))}")
        return flowshift.case_summary(reps, cases[name]["columns"])

    res = job("meta")
    exact5 = job("exact", "g5")
    res["gate5"] = gate("g5", exact5)                                   # (a)
    if res["gate5"]["passed"]:
        res["nomnu"] = case("nomnu")                                    # (b)
    else:
        res["nomnu"] = {"status": "not run (5-D known-answer gate failed)"}
    if "g5_pop1" in gates:
        res["gate5_pop1"] = gate("g5_pop1", exact5, True)               # (c), descriptive
        exact6 = run(True, "exact", "g6_pop1")
        res["gate6_pop1"] = (gate("g6_pop1", exact6, True) if "error" not in exact6
                             else {"status": "not run (6-D exact job failed)", "passed": False})
        res["nomnu_pop1"] = case("nomnu_pop1", True)                    # (d), descriptive
        res["main_pop1"] = case("main_pop1", True)
    return res


# ------------------------------------------------------------------ rules ----
def label(reps, gate_r1, gate5_passed, bands, s_max):
    """README 2.7 label rules 1-5, in order (rule 6 is a flag, see assemble). Returns
    (label, reason, numbers)."""
    lo_b, hi_b = bands
    if not gate_r1:
        return NE, "R1 gate failed", {}
    if not gate5_passed:
        return NE, "5-D known-answer gate failed", {}
    if not reps or any("error" in r or not _num(r.get("n_sigma")) for r in reps):
        return NE, "a default 5-D repetition failed or gave a non-finite n_sigma", {}
    if not all(r.get("converged") for r in reps):
        return NE, "a default 5-D estimate did not converge", {}
    vals = [float(r["n_sigma"]) for r in reps]
    if any(r.get("lower_bound") for r in reps):                         # rule 3
        low = min(vals)
        if low >= hi_b:
            return NOT_MAINLY, f"lower bound present; minimum {low:.4f} >= {hi_b}", {"minimum": low}
        return NE, f"lower bound present; minimum {low:.4f} < {hi_b}", {"minimum": low}
    n_bar = float(np.mean(vals))
    s = float(np.std(vals, ddof=1))
    nums = {"n_bar": n_bar, "s": s}
    if s > s_max:                                                       # rule 4
        return NE, f"s5 = {s:.4f} > {s_max}", nums
    half = 2.0 * s / math.sqrt(len(vals))                               # rule 5
    lo, hi = n_bar - half, n_bar + half
    nums.update(half_width=half, interval=[lo, hi])
    if hi <= lo_b:
        return MAINLY, f"I = [{lo:.4f}, {hi:.4f}] within (-inf, {lo_b}]", nums
    if lo >= hi_b:
        return NOT_MAINLY, f"I = [{lo:.4f}, {hi:.4f}] within [{hi_b}, inf)", nums
    if lo > lo_b and hi < hi_b:
        return PARTLY, f"I = [{lo:.4f}, {hi:.4f}] within ({lo_b}, {hi_b})", nums
    return BETWEEN, f"I = [{lo:.4f}, {hi:.4f}] straddles {lo_b if lo <= lo_b else hi_b}", nums


def _values(reps):
    """n_sigma of every repetition if all are finite and none is a lower bound, else None."""
    if not reps or any("error" in r or not _num(r.get("n_sigma")) or r.get("lower_bound") for r in reps):
        return None
    return [float(r["n_sigma"]) for r in reps]


def paired(reps_a, reps_b):
    """Per-seed differences a_k - b_k for seeds where both are finite."""
    a = {r.get("seed"): r.get("n_sigma") for r in reps_a or [] if "error" not in r}   # failed: skipped
    b = {r.get("seed"): r.get("n_sigma") for r in reps_b or [] if "error" not in r}
    diff = {str(k): float(a[k] - b[k]) for k in sorted(set(a) & set(b), key=str)
            if _num(a[k]) and _num(b[k])}
    vals = list(diff.values())
    return {"per_seed": diff, "mean": float(np.mean(vals)) if vals else None,
            "s": float(np.std(vals, ddof=1)) if len(vals) > 1 else None}


def pop_compare(reps10, reps1, f_crit):
    """README 2.7 pop_size comparison (descriptive): variance ratio larger/smaller against
    F_0.95(4, 4) (two-sided 10%), means by |n1 - n10| > 2 sqrt(s1^2/5 + s10^2/5) (a heuristic), and the
    paired per-seed differences n1_k - n10_k."""
    out = {"failed_pop1": [r.get("seed") for r in reps1 or []
                           if "error" in r or not _num(r.get("n_sigma"))],
           "paired_pop1_minus_default": paired(reps1, reps10)}
    v10, v1 = _values(reps10), _values(reps1)
    if v10 is None or v1 is None or len(v10) < 2 or len(v1) < 2:
        out["status"] = "not computed (a repetition failed, is non-finite or is a lower bound)"
        return out
    m10, s10 = float(np.mean(v10)), float(np.std(v10, ddof=1))
    m1, s1 = float(np.mean(v1)), float(np.std(v1, ddof=1))
    big, small = max(s1 ** 2, s10 ** 2), min(s1 ** 2, s10 ** 2)
    ratio = big / small if small > 0 else (1.0 if big == 0 else None)   # None: unbounded
    thr = 2.0 * math.sqrt(s1 ** 2 / len(v1) + s10 ** 2 / len(v10))
    out.update(n_bar_default=m10, s_default=s10, n_bar_pop1=m1, s_pop1=s1, variance_ratio=ratio,
               f_crit=f_crit, mean_difference=m1 - m10, mean_threshold=thr,
               all_converged=all(r.get("converged") for r in list(reps1) + list(reps10)),
               spread=("spreads differ" if ratio is None or ratio > f_crit
                       else "no detectable difference in spread with five repetitions"),
               means=("means differ" if abs(m1 - m10) > thr
                      else "means do not differ by the heuristic"))
    return out


def _case_reps(res, name):
    c = res.get(name)
    return c.get("repetitions") if isinstance(c, dict) else None


def assemble(res, rec, gate_r1, bands, s_max, s_flag, f_crit, settings):
    """results/r6_nomnu.json: the label, the pop_size comparison and everything README 2.7 reports."""
    out = {"settings": settings, "dropped": DROPPED,
           "r6_reused": {"path": "results/r6.json", "ok": bool(rec.get("ok")), "reason": rec.get("reason")},
           "r6": {k: rec.get(k) for k in ("n_bar", "s", "per_seed", "parameters", "gate_exact", "gate_mean",
                                          "verdict", "reason")}}
    if not rec.get("ok"):
        out.update(label=NE, reason=rec.get("reason"), flows={"status": "not run (R6 record not reusable)"})
        return _summary(out)
    out["flows"] = res
    if "status" in res:
        out.update(label=NE, reason=res["status"])
        return _summary(out)
    g5 = res["gate5"]
    reps5 = _case_reps(res, "nomnu")
    lab, why, nums = label(reps5 or [], gate_r1, bool(g5.get("passed")), bands, s_max)
    out.update(label=lab, reason=why, numbers=nums)
    if "s" in nums:
        out["s5_within_r6_s_max"] = {"value": nums["s"] <= s_flag, "threshold": s_flag,
                                     "note": "flag only (rule 6); does not decide the label"}
    out["paired_6d_minus_5d"] = {"default": paired(rec.get("repetitions"), reps5),
                                 "pop1": paired(_case_reps(res, "main_pop1"), _case_reps(res, "nomnu_pop1"))}
    if "main_pop1" in res:
        out["pop_size_comparison"] = {
            "5d": (pop_compare(reps5, _case_reps(res, "nomnu_pop1"), f_crit) if reps5
                   else {"status": "not computed (default 5-D case not run)"}),
            "6d": pop_compare(rec.get("repetitions"), _case_reps(res, "main_pop1"), f_crit)}
        g6 = res.get("gate6_pop1", {}).get("exact", {}).get("n_sigma")
        out["gate6_exact_recomputed"] = {"value": g6, "recorded": rec.get("gate_exact"),
                                         "equal": g6 is not None and g6 == rec.get("gate_exact")}
    out["gate_note"] = "gate5 decides (rule 1); gate5_pop1 and gate6_pop1 are reported and do not gate (d)"
    return _summary(out)


def _summary(out):
    nums = out.get("numbers") or {}
    out["summary"] = {"label": out["label"], "reason": out["reason"], "n_bar5": nums.get("n_bar"),
                      "s5": nums.get("s"), "interval": nums.get("interval"),
                      "n_bar6_r6": out["r6"].get("n_bar"), "r6_reused": out["r6_reused"]}
    return out
