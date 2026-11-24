"""R6-SHUF-KA2 (README section 2.10, T-063): a known-answer test of R6-SHUF's phi on a surrogate of the data.

Project-environment side (no TensorFlow). The flows run through r6flow.run_jobs (job folder, caching and cleanup as
R6) with plan() below; flowshift.py's 'ka2' jobs train one flow on one variant ("6", "S", "5") of the surrogate
(surrogate_t063.json, Gaussian mixtures fitted to the two chains) at one seed. The exact values are recomputed here
with flowshift.sur_exact (numpy/scipy only). This module checks the committed surrogate's hash and the recorded
results/r6.json, results/r6_shuf.json and results/r6_ka.json (read, never written), applies the label rules 1-4, the
qualifier of R6-SHUF and the comparison with R6-SHUF-KA, and assembles results/r6_ka2.json. It does not import run.py;
run.py passes PARAMS in.
"""
import hashlib
import json
import math
from pathlib import Path

import numpy as np

import r6ka
import r6shuf

VARIANTS = ("6", "S", "5")
EXACT_TOL = 0.005                       # README 2.10 rule 1: recomputed exact values within 0.005
EXACT_SEED, EXACT_PERM_SEED = 999, 1000
EXACT_N = 2_000_000
KA_LABEL = "no bias of φ detected (I_b = [-0.006, 0.045])"      # R6-SHUF-KA's recorded label (README 2.10)

NE = "not evaluable"
OVER = "flows overestimate φ on the surrogate"
UNDER = "flows underestimate φ on the surrogate"
NONE = "no bias of φ detected on the surrogate"
Q_HOLDS = "R6-SHUF's label holds after the surrogate correction"
Q_REVERSES = "R6-SHUF's label reverses after the surrogate correction"
Q_NOISY = "surrogate correction not decisive (test too noisy)"
Q_UNDECIDED = "R6-SHUF's label is not decided after the surrogate correction"
C_DIFF = "the bias of φ differs between the family and the surrogate"
C_NONE = "no difference in the bias of φ detected between the family and the surrogate"
_good = r6shuf._good
_num = r6shuf._num
check_shuf = r6ka.check_shuf
env_matches = r6ka.env_matches


# ------------------------------------------------------------------ inputs ----
def file_sha256(path):
    """SHA-256 of the file's bytes with \\n line endings (README 2.10; a CRLF checkout gives the same hash)."""
    return hashlib.sha256(Path(path).read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def load_surrogate(path, sha256):
    """The committed surrogate and whether its hash is the registered one (rule 1). Never refits."""
    path = Path(path)
    if not path.exists():
        return {"ok": False, "reason": f"{path.name} missing"}
    h = file_sha256(path)
    if h != sha256:
        return {"ok": False, "reason": f"{path.name} hash {h} differs from the registered one", "sha256": h}
    d = json.loads(path.read_text(encoding="utf-8"))
    return {"ok": True, "sha256": h, "columns": d["columns"], "scale": d["scale"], "mixtures": d["mixtures"]}


def check_ka(path):
    """README 2.10 comparison input: results/r6_ka.json with its recorded label; b_bar and s_b from numbers.b_bar
    and numbers.s_b over its seeds. Never writes."""
    path = Path(path)
    if not path.exists():
        return {"ok": False, "reason": "results/r6_ka.json missing"}
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        return {"ok": False, "reason": f"results/r6_ka.json unreadable ({type(exc).__name__})"}
    if d.get("label") != KA_LABEL:
        return {"ok": False, "reason": f"results/r6_ka.json label differs from the recorded one ({d.get('label')!r})"}
    nums = d.get("numbers") or {}
    seeds = (d.get("settings") or {}).get("r6_ka_seeds")
    if not (_num(nums.get("b_bar")) and _num(nums.get("s_b")) and isinstance(seeds, list) and len(seeds) > 1):
        return {"ok": False, "reason": "results/r6_ka.json has no b_bar, s_b and seeds"}
    fl = d.get("flows") or {}
    off = d.get("offsets") or {}
    return {"ok": True, "b_bar": float(nums["b_bar"]), "s_b": float(nums["s_b"]), "n": len(seeds),
            "label": d["label"], "versions": fl.get("versions"), "settings": fl.get("settings"),
            "offsets": {v: (off.get(v) or {}).get("mean") for v in VARIANTS}}


# ------------------------------------------------------------------ configuration, exact values, plan ----
def config(seeds, n, estimate, sur, offsets):
    """Job configuration for r6flow.run_jobs (no 'pop_size': flow_from_chain is called as in R6)."""
    return {"n": n, "estimate": estimate,
            "ka2": {"seeds": list(seeds), "columns": list(sur["columns"]), "scale": list(sur["scale"]),
                    "mixtures": sur["mixtures"], "offsets": list(offsets)}}


def exact_values(sur, flowshift, n=EXACT_N):
    """README 2.10: the exact values recomputed from the committed surrogate with the design script's code."""
    mx = sur["mixtures"]
    e = flowshift.sur_exact(mx["des_3x2pt"], mx["cmb"], n=n, seed=EXACT_SEED, perm_seed=EXACT_PERM_SEED)
    return {"n6": e["6"], "S": e["S"], "n5": e["5"], "phi": e["phi"]}


exact_check = r6ka.exact_check


def plan(job, cfg, log, flowshift, expected=None):
    """README 2.10 order: the environment (meta); if it differs from the records (expected = (rec6, recs)), nothing
    is trained (rule 1 decides); else for each seed the three variants "6", "S", "5". A crashed job of any kind is
    recorded as failed (rule 2)."""
    ka2 = cfg["ka2"]

    def one(*parts):
        try:
            return job(*parts)
        except Exception as exc:                                  # noqa: BLE001 (README 2.10 rule 2)
            return {"seed": parts[-1], "error": f"subprocess failed ({type(exc).__name__})"}

    res = job("meta")
    if expected is not None and not env_matches(res, *expected)["ok"]:
        res["status_runs"] = "not run (versions or flow settings differ from the recorded ones)"
        return res
    for v in VARIANTS:
        res[v] = []
    for k in ka2["seeds"]:
        for v in VARIANTS:
            r = one("ka2", v, k)
            res[v].append(r)
            log(f"  R6-SHUF-KA2 seed {k} variant {v}: {r.get('n_sigma', r.get('error'))}")
    return res


# ------------------------------------------------------------------ rules ----
def label(env_ok, sur_ok, exact_ok, recs_ok, reps, seeds, phi_exact, e_min, s_max):
    """README 2.10 label rules 1-4, in order. Returns (label, reason, numbers)."""
    if not env_ok:
        return NE, "versions or flow settings differ from the recorded ones", {}
    if not sur_ok:
        return NE, "surrogate_t063.json missing or its hash differs from the registered one", {}
    if not exact_ok:
        return NE, f"a recomputed exact value differs from the registered one by more than {EXACT_TOL}", {}
    if not recs_ok:
        return NE, "results/r6_shuf.json missing or its label differs from the recorded one", {}
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
    nums = {"E": e, "phi": phi, "b": b, "b_bar": m, "s_b": s}
    if s > s_max:
        return NE, f"s_b = {s:.4f} > {s_max}", nums
    half = 2.0 * s / math.sqrt(len(b))                                          # rule 4
    lo, hi = m - half, m + half
    nums.update(half_width=half, interval_b=[lo, hi])
    from scipy.stats import t as student_t                                     # descriptive: t quantile
    tq = float(student_t.ppf(0.975, len(b) - 1))
    nums.update(t_quantile=tq, interval_b_t=[m - tq * s / math.sqrt(len(b)), m + tq * s / math.sqrt(len(b))])
    if lo > 0:
        return f"{OVER} (bias {m:+.3f})", f"I_b = [{lo:.4f}, {hi:.4f}] within (0, inf)", nums
    if hi < 0:
        return f"{UNDER} (bias {m:+.3f})", f"I_b = [{lo:.4f}, {hi:.4f}] within (-inf, 0)", nums
    return f"{NONE} (I_b = [{lo:.3f}, {hi:.3f}])", f"I_b = [{lo:.4f}, {hi:.4f}] contains 0", nums


def qualifier(phi_r6, s_r6, n_r6, b_bar, s_b, n_b, band):
    """README 2.10 qualifier of R6-SHUF (section 2.9's with this test's b_bar and s_b)."""
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


def comparison(b_bar, s_b, n_b, rec_ka):
    """README 2.10 comparison with R6-SHUF-KA: delta_b = b_bar - b_bar_KA, sigma = sqrt(s_b^2/n + s_KA^2/n_KA)."""
    if not rec_ka.get("ok"):
        return {"reading": NE, "reason": rec_ka.get("reason")}
    d = b_bar - rec_ka["b_bar"]
    sig = math.sqrt(s_b ** 2 / n_b + rec_ka["s_b"] ** 2 / rec_ka["n"])
    out = {"delta_b": d, "sigma": sig, "b_bar_ka": rec_ka["b_bar"], "s_b_ka": rec_ka["s_b"], "n_ka": rec_ka["n"]}
    if abs(d) > 2 * sig:
        out["reading"] = f"{C_DIFF} (Δb = {d:+.3f})"
    else:
        out["reading"] = f"{C_NONE} (Δb = {d:+.3f} ± {sig:.3f})"
    return out


def assemble(res, rec6, recs, rec_ka, sur, exact, registered, seeds, e_min, s_max, band, settings):
    """results/r6_ka2.json: the label, the qualifier, the comparison and everything README 2.10 reports."""
    out = {"settings": settings,
           "surrogate": {k: sur.get(k) for k in ("ok", "reason", "sha256", "columns")},
           "records": {"r6": {"path": "results/r6.json", "ok": bool(rec6.get("ok")), "reason": rec6.get("reason"),
                              **{k: rec6.get(k) for k in ("versions", "settings")}},
                       "r6_shuf": {"path": "results/r6_shuf.json", **recs},
                       "r6_ka": {"path": "results/r6_ka.json", **rec_ka}},
           "flows": res}
    ex = exact_check(exact, registered) if exact else {"ok": False, "reason": "not computed"}
    out["exact"] = ex
    if "status" in res:
        out.update(label=NE, reason=res["status"])
        return _summary(out)
    env = env_matches(res, rec6, recs) if rec6.get("ok") and recs.get("ok") else {"ok": False}
    if rec_ka.get("ok"):                                       # reported against R6-SHUF-KA's, not a rule
        env["equal_r6_ka"] = env.get("run") == {"versions": rec_ka.get("versions"), "settings": rec_ka.get("settings")}
    out["environment"] = env
    reps = {v: res.get(v) for v in VARIANTS}
    phi_exact = ex["recomputed"]["phi"] if ex.get("recomputed") else float("nan")
    lab, why, nums = label(bool(env.get("ok")), bool(sur.get("ok")), bool(ex.get("ok")),
                           bool(recs.get("ok") and rec6.get("ok")), reps, seeds, phi_exact, e_min, s_max)
    out.update(label=lab, reason=why, numbers=nums)
    if lab != NE and "b_bar" in nums:
        out["qualifier"] = qualifier(recs["phi_bar"], recs["s_phi"], recs["n"], nums["b_bar"], nums["s_b"],
                                     len(seeds), band)
        out["comparison"] = comparison(nums["b_bar"], nums["s_b"], len(seeds), rec_ka)
    # descriptive: per-variant mean offsets from the exact values, whatever the label, next to R6-SHUF-KA's
    per = {v: {int(x["seed"]): float(x["n_sigma"]) for x in (reps.get(v) or []) if _good(x)} for v in VARIANTS}
    key = {"6": "n6", "S": "S", "5": "n5"}
    if ex.get("recomputed"):
        out["offsets"] = {v: r6ka._stats([x - ex["recomputed"][key[v]] for x in per[v].values()]) for v in VARIANTS}
        if rec_ka.get("ok"):
            out["offsets_ka"] = rec_ka["offsets"]
    out["per_seed"] = {str(k): {v: per[v].get(k) for v in VARIANTS} for k in seeds}
    out["times_s"] = {v: [x.get("train_s") for x in (reps.get(v) or [])] for v in VARIANTS}
    return _summary(out)


def _summary(out):
    nums = out.get("numbers") or {}
    q = out.get("qualifier") or {}
    c = out.get("comparison") or {}
    out["summary"] = {"label": out["label"], "reason": out["reason"], "b_bar": nums.get("b_bar"),
                      "s_b": nums.get("s_b"), "interval_b": nums.get("interval_b"),
                      "qualifier": q.get("qualifier"), "w": q.get("w"), "interval_corrected": q.get("interval"),
                      "comparison": c.get("reading"), "delta_b": c.get("delta_b"), "sigma_delta": c.get("sigma")}
    return out
