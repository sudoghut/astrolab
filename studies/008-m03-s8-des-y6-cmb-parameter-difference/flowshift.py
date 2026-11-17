"""R6-FLOW (README section 2.6): normalizing-flow parameter difference, run in the TF environment.

This module runs only in the separate environment of T-027 (TensorFlow with the legacy Keras 2 API,
tensiometer, getdist), one job per process, started by r6flow.py:

    TF_USE_LEGACY_KERAS=1 PYTHONNOUSERSITE=1 <venv-tf python> -I flowshift.py <input.npz> <config.json> <output.json> <job>

where <job> is "meta", "exact", "gate <seed>" or "case <name> <seed>". It never touches the network
or the project folder: it reads the job folder's input.npz (the chains' columns and weights) and
writes one JSON file atomically. The pure helpers (gate_summary, case_summary, finite) are also
used by r6flow.py in the project environment. Order (README 2.6): the known-answer gate first; only
if it passes, the chains.
"""
import inspect
import json
import os
import sys
import time

import numpy as np


def _setup():
    os.environ.setdefault("MPLBACKEND", "Agg")
    import tensorflow as tf
    tf.config.experimental.enable_op_determinism()
    return tf


def _nsigma(p):
    from scipy.special import erfinv
    return float(np.sqrt(2.0) * erfinv(p)) if p < 1 else float("inf")


def defaults():
    """The tensiometer settings used (its defaults apart from feedback and plotting)."""
    from tensiometer.synthetic_probability import synthetic_probability as sp
    init = inspect.signature(sp.FlowCallback.__init__).parameters
    glob = inspect.signature(sp.FlowCallback.global_train).parameters
    train = inspect.signature(sp.FlowCallback.train).parameters
    keep = ("prior_bijector", "apply_rescaling", "trainable_bijector", "validation_split")
    out = {k: init[k].default for k in keep}
    out.update(pop_size=glob["pop_size"].default, epochs=train["epochs"].default,
               feedback=0, plot_every=0)
    return out


def one_shift(diff, names, seed, est):
    """One repetition on equally weighted difference samples: train a flow, estimate the shift."""
    tf = _setup()
    from getdist import MCSamples
    from tensiometer.mcmc_tension import flow as fl
    from tensiometer.synthetic_probability import synthetic_probability as sp
    tf.keras.utils.set_random_seed(seed)
    chain = MCSamples(samples=diff, names=list(names), ignore_rows=0)
    t0 = time.time()
    flow = sp.flow_from_chain(chain, feedback=0, plot_every=0)
    t1 = time.time()
    p, lo, up = fl.estimate_shift(flow, tol=est["tol"], max_iter=est["max_iter"], step=est["step"])
    p, lo, up = float(p), float(lo), float(up)
    s_lo, s_up = _nsigma(lo), _nsigma(up)
    at_floor = p >= 1.0
    # a NaN interval end (for example log p(0) undefined outside the flow's range) is not convergence
    converged = bool(np.isfinite(lo) and (at_floor or (np.isfinite(s_up) and s_up - s_lo <= est["tol"])))
    return {"seed": seed, "delta": p, "delta_low": lo, "delta_up": up,
            "n_sigma": s_lo if at_floor else _nsigma(p), "lower_bound": bool(at_floor),
            "converged": converged, "train_s": round(t1 - t0, 1), "shift_s": round(time.time() - t1, 1)}


def _clean(msg):
    """An exception message without local paths (README 2.6: only availability and versions saved)."""
    import re
    return re.sub(r"[A-Za-z]:[\\/][^\s'\"]*|/(?:home|Users)/[^\s'\"]*", "<path>", msg)[:300]


def resampled_difference(xa, wa, xb, wb, n, seed):
    """README 2.6 step 2: weighted independent draws from each chain; equally weighted differences."""
    rng = np.random.default_rng(seed)
    ia = rng.choice(len(wa), size=n, replace=True, p=wa / wa.sum())
    ib = rng.choice(len(wb), size=n, replace=True, p=wb / wb.sum())
    return xa[ia] - xb[ib]


# ------------------------------------------------------------------ known-answer gate ----
def synthetic(n, rng, g):
    """README 2.6 gate: a curved pair (x2 = z + curv (x1 - mu1)^2) and four box directions."""
    x1 = rng.normal(g["mu1"], 1.0, n)
    x2 = rng.normal(g["mu2"], 1.0, n) + g["curv"] * (x1 - g["mu1"]) ** 2
    boxes = [rng.uniform(lo, hi, n) - rng.normal(0.0, s, n) for lo, hi, s in g["boxes"]]
    return np.column_stack([x1, x2] + boxes)


def synthetic_exact(g):
    """Exact n_sigma of the synthetic distribution from its analytic density (README 2.6)."""
    from scipy.stats import norm

    def logp(z):
        x1, x2 = z[:, 0], z[:, 1]
        out = norm.logpdf(x1, g["mu1"], 1.0) + norm.logpdf(x2 - g["curv"] * (x1 - g["mu1"]) ** 2, g["mu2"], 1.0)
        for i, (lo, hi, s) in enumerate(g["boxes"]):
            u = z[:, 2 + i]
            out = out + np.log(np.clip(norm.cdf((u - lo) / s) - norm.cdf((u - hi) / s), 1e-300, None) / (hi - lo))
        return out

    z = synthetic(g["n_exact"], np.random.default_rng(g["exact_seed"]), g)
    p = float(np.mean(logp(z) > logp(np.zeros((1, 6)))[0]))
    return {"delta": p, "n_sigma": _nsigma(p)}


def gate_summary(exact, reps, g):
    """README 2.6 gate rule from the exact value and the three repetitions (no TensorFlow needed)."""
    vals = [r.get("n_sigma") for r in reps]
    ok = all(v is not None and np.isfinite(v) and r.get("converged") and not r.get("lower_bound")
             for v, r in zip(vals, reps))
    mean = float(np.mean(vals)) if ok else None
    passed = bool(ok and abs(mean - exact["n_sigma"]) <= g["tol_mean"]
                  and all(abs(v - exact["n_sigma"]) <= g["tol_each"] for v in vals))
    return {"exact": exact, "repetitions": reps, "mean": mean, "passed": passed,
            "rule": f"mean within {g['tol_mean']} and each within {g['tol_each']} of the exact n_sigma"}


def case_summary(reps, cols):
    good = [r["n_sigma"] for r in reps if r.get("n_sigma") is not None and np.isfinite(r["n_sigma"])]
    return {"parameters": list(cols), "repetitions": reps,
            "n_bar": float(np.mean(good)) if good else None,
            "s": float(np.std(good, ddof=1)) if len(good) > 1 else None}


def finite(o):
    """Strict JSON: NaN and infinities become null."""
    if isinstance(o, dict):
        return {k: finite(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [finite(v) for v in o]
    if isinstance(o, (float, np.floating)):
        return float(o) if np.isfinite(o) else None
    if isinstance(o, np.integer):
        return int(o)
    return o


def run_job(job, inp, cfg):
    """One unit of work in its own process (so TensorFlow memory is freed when it exits):
    'meta', 'exact', ('gate', seed) or ('case', name, seed)."""
    if job[0] == "meta":
        import getdist
        import tensiometer
        tf = _setup()
        return {"versions": {"tensorflow": tf.__version__, "tensiometer": tensiometer.__version__,
                             "getdist": getdist.__version__, "numpy": np.__version__,
                             "legacy_keras": os.environ.get("TF_USE_LEGACY_KERAS")},
                "settings": defaults()}
    if job[0] == "exact":
        return synthetic_exact(cfg["gate"])
    names6 = [f"x{i}" for i in range(6)]
    try:
        if job[0] == "gate":
            g, k = cfg["gate"], int(job[1])
            x = synthetic(cfg["n"], np.random.default_rng(g["sample_seed_offset"] + k), g)
            return one_shift(x, names6, k, cfg["estimate"])
        name, k = job[1], int(job[2])
        cols = cfg["cases"][name]["columns"]
        d = np.load(inp, allow_pickle=False)
        xa = np.column_stack([d["des_" + c] for c in cols])
        xb = np.column_stack([d["cmb_" + c] for c in cols])
        return one_shift(resampled_difference(xa, d["des_w"], xb, d["cmb_w"], cfg["n"], k), cols, k,
                         cfg["estimate"])
    except Exception as exc:             # recorded; the verdict rule handles failures
        return {"seed": int(job[-1]), "error": _clean(f"{type(exc).__name__}: {exc}")}


def main(argv):
    """flowshift.py <input.npz> <config.json> <output.json> <job...>; writes one job's JSON."""
    inp, cfg_path, out_path = argv[1:4]
    job = argv[4:]
    cfg = json.loads(open(cfg_path, encoding="utf-8").read())
    res = run_job(job, inp, cfg)
    tmp = out_path + ".part"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(finite(res), fh, indent=1, allow_nan=False)
    os.replace(tmp, out_path)


if __name__ == "__main__":
    main(sys.argv)
