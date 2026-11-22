"""R6-FLOW (README section 2.6): normalizing-flow parameter difference, run in the TF environment.

This module runs only in the separate environment of T-027 (TensorFlow with the legacy Keras 2 API,
tensiometer, getdist), one job per process, started by r6flow.py:

    TF_USE_LEGACY_KERAS=1 PYTHONNOUSERSITE=1 <venv-tf python> -I flowshift.py <input.npz> <config.json> <output.json> <job>

where <job> is "meta", "exact", "gate <seed>" or "case <name> <seed>" (R6), or "exact <gate>" and
"gate <gate> <seed>" for a named gate in cfg["gates"] (R6-NOMNU, README 2.7), and "shuf <variant> <seed>"
and "knn <seed>" for the Sigma m_nu column variants of R6-SHUF (README 2.8), and "ka <variant> <seed>" for
the synthetic family of R6-SHUF-KA (README 2.9). It never touches the network
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


def one_shift(diff, names, seed, est, pop_size=None, record_pop=False):
    """One repetition on equally weighted difference samples: train a flow, estimate the shift.

    pop_size None: flow_from_chain is called exactly as in R6 (tensiometer's default). Otherwise
    pop_size is passed explicitly (README 2.7). With record_pop the pop_size actually passed (None if
    none was passed), whether it was passed, and the number of trained populations are added."""
    tf = _setup()
    from getdist import MCSamples
    from tensiometer.mcmc_tension import flow as fl
    from tensiometer.synthetic_probability import synthetic_probability as sp
    tf.keras.utils.set_random_seed(seed)
    chain = MCSamples(samples=diff, names=list(names), ignore_rows=0)
    t0 = time.time()
    if pop_size is None:
        flow = sp.flow_from_chain(chain, feedback=0, plot_every=0)
    else:
        flow = sp.flow_from_chain(chain, feedback=0, plot_every=0, pop_size=int(pop_size))
    t1 = time.time()
    p, lo, up = fl.estimate_shift(flow, tol=est["tol"], max_iter=est["max_iter"], step=est["step"])
    p, lo, up = float(p), float(lo), float(up)
    s_lo, s_up = _nsigma(lo), _nsigma(up)
    at_floor = p >= 1.0
    # a NaN interval end (for example log p(0) undefined outside the flow's range) is not convergence
    converged = bool(np.isfinite(lo) and (at_floor or (np.isfinite(s_up) and s_up - s_lo <= est["tol"])))
    out = {"seed": seed, "delta": p, "delta_low": lo, "delta_up": up,
           "n_sigma": s_lo if at_floor else _nsigma(p), "lower_bound": bool(at_floor),
           "converged": converged, "train_s": round(t1 - t0, 1), "shift_s": round(time.time() - t1, 1)}
    if record_pop:
        logs = getattr(flow, "population_logs", None)
        out.update(pop_size=int(pop_size) if pop_size is not None else None,     # as passed (None: not)
                   pop_size_passed=pop_size is not None,
                   populations_trained=len(logs) if logs is not None else None)
    return out


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


# ------------------------------------------------------------------ R6-SHUF (README 2.8) ----
VARIANTS = ("none", "S", "P", "SS")


def variant_difference(xa, wa, xb, wb, n, seed, variant="none", col=None, offsets=(1000, 2000, 3000),
                       prior=(0.06, 0.6)):
    """README 2.8: the DES (xa) and CMB (xb) rows drawn exactly as resampled_difference (the same two
    rng.choice calls, in the same order, on default_rng(seed)); then only the resampled Sigma m_nu
    column `col` is changed before the difference is taken:
      "none": no change (bitwise equal to resampled_difference);
      "S":  DES column permuted with default_rng(offsets[0] + seed).permutation(n);
      "P":  DES column replaced by default_rng(offsets[1] + seed).uniform(prior[0], prior[1], n);
      "SS": as "S", and the CMB column permuted with default_rng(offsets[2] + seed).permutation(n)."""
    if variant not in VARIANTS:
        raise ValueError(f"unknown variant {variant!r}")
    rng = np.random.default_rng(seed)
    ia = rng.choice(len(wa), size=n, replace=True, p=wa / wa.sum())
    ib = rng.choice(len(wb), size=n, replace=True, p=wb / wb.sum())
    a, b = xa[ia], xb[ib]                # fancy indexing: copies, the inputs are not modified
    if variant in ("S", "SS"):
        a[:, col] = a[np.random.default_rng(offsets[0] + seed).permutation(n), col]
    elif variant == "P":
        a[:, col] = np.random.default_rng(offsets[1] + seed).uniform(prior[0], prior[1], n)
    if variant == "SS":
        b[:, col] = b[np.random.default_rng(offsets[2] + seed).permutation(n), col]
    return a - b


def knn_nsigma(x, k):
    """README 2.8 kNN estimator, as explore/t044_knn_gate_design.py: whiten with the sample mean m and
    covariance S (z = (x - m) L, L L^T = S^-1); the density proxy of a point is the distance to its
    k-th nearest neighbour among the samples; n_sigma = sqrt(2) erfinv(f), f the fraction of samples
    whose proxy distance is smaller than the origin's."""
    return knn_nsigma_multi(x, [k])[0]


def knn_nsigma_multi(x, ks):
    """knn_nsigma for several k from one tree query (the same distances as one query per k)."""
    from scipy.spatial import cKDTree
    from scipy.special import erfinv
    m = x.mean(0)
    L = np.linalg.cholesky(np.linalg.inv(np.cov(x.T)))
    z = (x - m) @ L
    z0 = (-m) @ L
    tree = cKDTree(z)
    kmax = max(ks)
    dz = tree.query(z, kmax + 1)[0]      # column 0: the sample itself (distance 0)
    d0 = np.atleast_1d(tree.query(z0[None], kmax)[0][0])   # k = 1 returns a squeezed scalar
    return [float(np.sqrt(2.0) * erfinv(np.mean(dz[:, k] < d0[k - 1]))) for k in ks]


def _shuf_arrays(inp, sc):
    d = np.load(inp, allow_pickle=False)
    cols = sc["columns"]
    xa = np.column_stack([d["des_" + c] for c in cols])    # DES 3x2pt (exported as des_<column>)
    xb = np.column_stack([d["cmb_" + c] for c in cols])    # CMB (exported as cmb_<column>)
    return xa, d["des_w"], xb, d["cmb_w"], cols.index(sc["mnu"])


# ------------------------------------------------------------------ known-answer gate ----
def synthetic(n, rng, g):
    """README 2.6 gate: a curved pair (x2 = z + curv (x1 - mu1)^2) and four box directions."""
    x1 = rng.normal(g["mu1"], 1.0, n)
    x2 = rng.normal(g["mu2"], 1.0, n) + g["curv"] * (x1 - g["mu1"]) ** 2
    boxes = [rng.uniform(lo, hi, n) - rng.normal(0.0, s, n) for lo, hi, s in g["boxes"]]
    return np.column_stack([x1, x2] + boxes)


def gate_dim(g):
    """Dimension of a synthetic gate distribution: the curved pair plus one column per box."""
    return 2 + len(g["boxes"])


def gate_names(g):
    return [f"x{i}" for i in range(gate_dim(g))]


def synthetic_exact(g):
    """Exact n_sigma of the synthetic distribution from its analytic density (README 2.6); the
    reference point 0 has the dimension implied by the box list (6-D for R6, 5-D for README 2.7)."""
    from scipy.stats import norm

    def logp(z):
        x1, x2 = z[:, 0], z[:, 1]
        out = norm.logpdf(x1, g["mu1"], 1.0) + norm.logpdf(x2 - g["curv"] * (x1 - g["mu1"]) ** 2, g["mu2"], 1.0)
        for i, (lo, hi, s) in enumerate(g["boxes"]):
            u = z[:, 2 + i]
            out = out + np.log(np.clip(norm.cdf((u - lo) / s) - norm.cdf((u - hi) / s), 1e-300, None) / (hi - lo))
        return out

    z = synthetic(g["n_exact"], np.random.default_rng(g["exact_seed"]), g)
    p = float(np.mean(logp(z) > logp(np.zeros((1, gate_dim(g))))[0]))
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


# ------------------------------------------------------------------ R6-SHUF-KA (README 2.9) ----
# The synthetic family of the known-answer test of phi: the functions of explore/t047_ka_design.py (the
# pre-registration's design script), copied with a ka_ prefix (test_r6ka.py checks identical draws and densities).
# Latent v ~ U(lo, hi); u = v - N(0, s); x1 = N(mu1 + a (v - c), 1); x2 = N(mu2, 1) + curv (x1 - mu1)^2; three boxes.
# Variants "6" (x1, x2, u, b1, b2, b3), "S" (u column permuted: u's marginal times the rest's), "5" (u dropped).

KA_NAMES6 = ["x1", "x2", "u", "b1", "b2", "b3"]
KA_U_COL = 2


def ka_nsig(p):
    from scipy.special import erfinv
    return float(np.sqrt(2) * erfinv(p))


def ka_sample(n, rng, g):
    """D6 rows; draw order v, the u noise, x1, x2, the boxes (each a full vector)."""
    lo, hi, s = g["ubox"]
    v = rng.uniform(lo, hi, n)
    u = v - rng.normal(0.0, s, n)
    x1 = rng.normal(g["mu1"] + g["a"] * (v - g["c"]), 1.0, n)
    x2 = rng.normal(g["mu2"], 1.0, n) + g["curv"] * (x1 - g["mu1"]) ** 2
    boxes = [rng.uniform(blo, bhi, n) - rng.normal(0.0, bs, n) for blo, bhi, bs in g["boxes"]]
    return np.column_stack([x1, x2, u] + boxes)


def ka_variant(z6, v, perm_rng=None):
    """The rows of variant v from the D6 rows: "6" as is; "S" the u column permuted by perm_rng; "5" u dropped."""
    if v == "6":
        return z6
    if v == "S":
        z = z6.copy()
        z[:, KA_U_COL] = z[perm_rng.permutation(len(z)), KA_U_COL]
        return z
    if v == "5":
        return np.delete(z6, KA_U_COL, axis=1)
    raise ValueError(f"unknown variant {v!r}")


def ka_names(v):
    return [n for n in KA_NAMES6 if not (v == "5" and n == "u")]


def ka_log_box(u, lo, hi, s):
    from scipy.stats import norm
    return np.log(np.clip(norm.cdf((u - lo) / s) - norm.cdf((u - hi) / s), 1e-300, None) / (hi - lo))


def ka_log_x1(x1, g):
    """marginal of x1: int U(v) N(x1; mu1 + a (v - c), 1) dv"""
    from scipy.stats import norm
    lo, hi, _ = g["ubox"]
    a = g["a"]
    if a == 0:
        return norm.logpdf(x1, g["mu1"], 1.0)
    m_lo = g["mu1"] + a * (lo - g["c"])
    m_hi = g["mu1"] + a * (hi - g["c"])
    A, B = min(m_lo, m_hi), max(m_lo, m_hi)
    return np.log(np.clip(norm.cdf(x1 - A) - norm.cdf(x1 - B), 1e-300, None) / (B - A))


def ka_log_x1u(x1, u, g):
    """int U(v) N(u; v, s) N(x1; mu1 + a (v - c), 1) dv (closed form)"""
    from scipy.stats import norm
    lo, hi, s = g["ubox"]
    a, c, mu1 = g["a"], g["c"], g["mu1"]
    if a == 0:
        return norm.logpdf(x1, mu1, 1.0) + ka_log_box(u, lo, hi, s)
    t1, p1 = u, 1.0 / s ** 2
    t2, p2 = (x1 - mu1) / a + c, a ** 2
    P = p1 + p2
    m = (p1 * t1 + p2 * t2) / P
    log_pair = norm.logpdf(t1, t2, np.sqrt(1 / p1 + 1 / p2)) - np.log(abs(a))
    sd = 1 / np.sqrt(P)
    mass = np.clip(norm.cdf((hi - m) / sd) - norm.cdf((lo - m) / sd), 1e-300, None)
    return log_pair + np.log(mass) - np.log(hi - lo)


def ka_logp(z, g, variant):
    from scipy.stats import norm
    x1, x2 = z[:, 0], z[:, 1]
    out = norm.logpdf(x2 - g["curv"] * (x1 - g["mu1"]) ** 2, g["mu2"], 1.0)
    if variant == "6":
        out = out + ka_log_x1u(x1, z[:, 2], g)
        rest = z[:, 3:]
    elif variant == "S":
        out = out + ka_log_x1(x1, g) + ka_log_box(z[:, 2], *g["ubox"])
        rest = z[:, 3:]
    else:  # "5": u dropped
        out = out + ka_log_x1(x1, g)
        rest = z[:, 2:]
    for i, (lo, hi, s) in enumerate(g["boxes"]):
        out = out + ka_log_box(rest[:, i], lo, hi, s)
    return out


def ka_exact(g, n=2_000_000, seed=999):
    """README 2.9: exact n_sigma of the three variants (D6 from default_rng(seed), DS by permuting its u column
    with default_rng(seed + 1), D5 by dropping u) and phi."""
    z6 = ka_sample(n, np.random.default_rng(seed), g)
    zS = z6.copy()
    zS[:, 2] = zS[np.random.default_rng(seed + 1).permutation(n), 2]
    z5 = np.delete(z6, 2, axis=1)
    out = {}
    for v, z in (("6", z6), ("S", zS), ("5", z5)):
        o = np.zeros((1, z.shape[1]))
        out[v] = ka_nsig(float(np.mean(ka_logp(z, g, v) > ka_logp(o, g, v)[0])))
    out["phi"] = (out["6"] - out["S"]) / (out["6"] - out["5"])
    return out


def run_job(job, inp, cfg):
    """One unit of work in its own process (so TensorFlow memory is freed when it exits):
    'meta', 'exact', ('gate', seed) or ('case', name, seed) as in R6; ('exact', gate) and
    ('gate', gate, seed) for a named gate in cfg['gates'] (README 2.7). A gate or case entry with a
    'pop_size' key (None: not passed) records the pop_size used; without the key the call is R6's.
    README 2.8: ('shuf', variant, seed) trains one flow on a Sigma m_nu column variant (pop_size not
    passed, R6's call) and ('knn', seed) gives the kNN values of all variants and of the 5-D difference."""
    if job[0] == "meta":
        import getdist
        import tensiometer
        tf = _setup()
        return {"versions": {"tensorflow": tf.__version__, "tensiometer": tensiometer.__version__,
                             "getdist": getdist.__version__, "numpy": np.__version__,
                             "legacy_keras": os.environ.get("TF_USE_LEGACY_KERAS")},
                "settings": defaults()}
    if job[0] == "exact":
        return synthetic_exact(cfg["gate"] if len(job) == 1 else cfg["gates"][job[1]])
    try:
        if job[0] == "gate":
            g, k = (cfg["gate"], int(job[1])) if len(job) == 2 else (cfg["gates"][job[1]], int(job[2]))
            x = synthetic(cfg["n"], np.random.default_rng(g["sample_seed_offset"] + k), g)
            return one_shift(x, gate_names(g), k, cfg["estimate"], g.get("pop_size"), "pop_size" in g)
        if job[0] in ("shuf", "knn"):
            sc = cfg["shuf"]
            xa, wa, xb, wb, j = _shuf_arrays(inp, sc)

            def draw(variant, k):
                return variant_difference(xa, wa, xb, wb, cfg["n"], k, variant, j, sc["offsets"], sc["prior"])
            if job[0] == "shuf":
                variant, k = job[1], int(job[2])
                out = one_shift(draw(variant, k), sc["columns"], k, cfg["estimate"], None, True)
                return {**out, "variant": variant}
            k = int(job[1])
            t0 = time.time()
            vals = {v: knn_nsigma_multi(draw(v, k), sc["knn_k"]) for v in VARIANTS}
            vals["5d"] = knn_nsigma_multi(np.delete(draw("none", k), j, axis=1), sc["knn_k"])
            return {"seed": k, "k": list(sc["knn_k"]), "n_sigma": vals, "knn_s": round(time.time() - t0, 1)}
        if job[0] == "ka":
            # README 2.9: one flow on variant job[1] ("6", "S" or "5") of the synthetic family at seed job[2];
            # the D6 rows from default_rng(offsets[0] + k), the (S) permutation from default_rng(offsets[1] + k)
            ka = cfg["ka"]
            variant, k = job[1], int(job[2])
            z6 = ka_sample(cfg["n"], np.random.default_rng(ka["offsets"][0] + k), ka["family"])
            x = ka_variant(z6, variant, np.random.default_rng(ka["offsets"][1] + k) if variant == "S" else None)
            out = one_shift(x, ka_names(variant), k, cfg["estimate"], None, True)
            return {**out, "variant": variant}
        name, k = job[1], int(job[2])
        case = cfg["cases"][name]
        cols = case["columns"]
        d = np.load(inp, allow_pickle=False)
        xa = np.column_stack([d["des_" + c] for c in cols])
        xb = np.column_stack([d["cmb_" + c] for c in cols])
        return one_shift(resampled_difference(xa, d["des_w"], xb, d["cmb_w"], cfg["n"], k), cols, k,
                         cfg["estimate"], case.get("pop_size"), "pop_size" in case)
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
