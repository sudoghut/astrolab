"""Labels and overall readings of study 012 (README section 2). Pure functions of stored numbers.

Every tunable arrives as an argument; this module never imports run.
"""
from __future__ import annotations

import math

import numpy as np

MISSING = "undetermined (data not in the files)"
GRID = "undetermined (grid not converged)"


def pct_interval(x, level=0.95):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if x.size == 0:
        return [None, None]
    a = (1.0 - level) / 2.0 * 100.0
    return [float(np.percentile(x, a)), float(np.percentile(x, 100.0 - a))]


def binom_se(k, n):
    p = k / n if n else float("nan")
    return math.sqrt(n * p * (1.0 - p)) if n else float("nan")


def median_with_se(x, rng, n_boot=1000):
    """Median and its bootstrap standard error over mocks (README 4.3)."""
    x = np.asarray(x, float)
    med = float(np.median(x))
    bs = [np.median(x[rng.integers(0, x.size, x.size)]) for _ in range(n_boot)]
    return med, float(np.std(bs, ddof=1))


# ---------------------------------------------------------------------------------------------
# T2a

def t2a_reproduction(missing, sigma_i, at_bound_i, lo=2.4, hi=3.0):
    if missing:
        return MISSING
    if at_bound_i:
        return "not reproduced"
    return "reproduced" if lo <= sigma_i <= hi else "not reproduced"


def t2a_population(missing, at_bound_ii, bias_ii, unmodelled, interval, lo=2.4, hi=3.0, bias_max=0.1,
                   grid_ok=True):
    """Order of README section 2: missing data, fit at bound, method bias, unmodelled selection, then the
    interval against 2.4-3.0 kpc. A grid check that did not converge (README 4.12 item 4) makes it
    undetermined until a dated amendment."""
    if missing:
        return MISSING
    if not grid_ok:
        return GRID
    if at_bound_ii:
        return "undetermined (fit at bound)"
    if abs(bias_ii) > bias_max:
        return "undetermined (method bias)"
    if unmodelled:
        return "undetermined (unmodelled selection)"
    a, b = interval
    if a is None:
        return "undetermined"
    if a >= lo and b <= hi:
        return "consistent with 2.7 kpc"
    if b < lo or a > hi:
        return "different"
    return "undetermined"


# ---------------------------------------------------------------------------------------------
# T2b

def check_pass(k, n=100, need=80):
    return {"passed_mocks": int(k), "n": int(n), "binomial_se": binom_se(k, n), "pass": k >= need * n / 100}


def t2b_shape(missing, fp_pass, power_pass, step1, step2_pass=None, step2=None):
    """Shape label and the model used for f5 (README section 2, T2b row).
    fp_pass: all false-positive sets passed; step1: the data's step-1 label; step2_pass: step-2 check
    (None when step 2 is not reached); step2: the data's step-2 label."""
    if missing:
        return MISSING, None
    if not (fp_pass and power_pass):
        return "undetermined (checks failed)", "sph"
    if step1 == "spherical adequate":
        return "spherical adequate", "sph"
    if step1 == "prolate preferred":
        return "prolate preferred", "flat"
    # flattened preferred: step 2
    if step2_pass is False:
        return "flattened (step 2 undetermined)", "flat"
    if step2 == "power law preferred":
        return "power law preferred", "pow"
    return "flattened Gaussian adequate", "flat"


def t2b_f5(t2a_pop_label, interval):
    """f5 label: inherits T2a (ii)'s undetermined reasons except the straddling 'undetermined'."""
    inherit = (MISSING, GRID, "undetermined (fit at bound)", "undetermined (method bias)",
               "undetermined (unmodelled selection)")
    if t2a_pop_label in inherit:
        return t2a_pop_label
    a, b = interval
    if a is None:
        return "undetermined"
    if a > 0.5:
        return "most within 5 kpc confirmed"
    if b < 0.5:
        return "not confirmed"
    return "undetermined"


# ---------------------------------------------------------------------------------------------
# T4

def t4_label(baseline, variants, sigma_skipped, sigma_max=0.3, mass_factor=3.0, grid_ok=True):
    """baseline: {"sigma_ii", "a_label", "b_label", "mass"}; variants: {name: same keys, with for the
    noise variants "a_changed", "b_changed" already decided by the 6-of-10 rule}. Returns
    (label, list of broken (variant, quantity))."""
    broken = []
    for name, v in variants.items():
        if not sigma_skipped and grid_ok:
            s0, s1 = baseline.get("sigma_ii"), v.get("sigma_ii")
            if s0 is None or s1 is None or not abs(s1 - s0) < sigma_max:
                broken.append((name, "sigma"))
        for k in ("a", "b"):
            changed = v[f"{k}_changed"] if f"{k}_changed" in v else v[f"{k}_label"] != baseline[f"{k}_label"]
            if changed:
                broken.append((name, f"T3 ({k})"))
        m0, m1 = baseline["mass"], v["mass"]
        if not (m0 > 0 and m1 > 0 and 1.0 / mass_factor < m1 / m0 < mass_factor):
            broken.append((name, "T6 mass"))
    if broken:
        return "sensitive", broken
    # the sigma condition cannot be evaluated without a converged grid (README 4.12 item 4)
    return ("robust" if grid_ok else GRID), broken


# ---------------------------------------------------------------------------------------------
# T5

def label_g(iv):
    a, b = iv
    if a is None:
        return "undetermined"
    if b < 0.10:
        return "minor"
    if a >= 0.10 and b <= 0.25:
        return "moderate"
    if a > 0.25:
        return "major"
    return "undetermined"


def label_a5(iv):
    a, b = iv
    if a is None:
        return "undetermined"
    if a > 0.5:
        return "most apocentres below 5 kpc confirmed"
    if b < 0.5:
        return "not confirmed"
    return "undetermined"


# ---------------------------------------------------------------------------------------------
# Overall readings

def reading_reproduction(t1_summary, t2a_repro, t3a, t3b):
    bad = []
    if t1_summary != "abstract reproduced":
        bad.append("T1")
    if t2a_repro == "not reproduced":
        bad.append("T2a")
    if t3a in ("net rotation", "net counter-rotation"):
        bad.append("T3 (a)")
    if t3b == "not rotation dominated":
        bad.append("T3 (b)")
    if bad:
        return "not reproduced", bad
    if (t1_summary == "abstract reproduced" and t2a_repro == "reproduced" and t3a == "no net rotation"
            and t3b == "rotation dominated"):
        return "R22's numbers reproduce from the public sample", []
    und = [n for n, ok in (("T2a", t2a_repro == "reproduced"), ("T3 (a)", t3a == "no net rotation"),
                           ("T3 (b)", t3b == "rotation dominated")) if not ok]
    return "partly reproduced", und


def reading_robustness(t2a_pop, f5, t4, g, a5):
    if (t2a_pop == "consistent with 2.7 kpc" and f5 == "most within 5 kpc confirmed" and t4 == "robust"
            and g in ("minor", "moderate") and a5 == "most apocentres below 5 kpc confirmed"):
        return "holds under our checks", []
    bad = [n for n, cond in (("T2a", t2a_pop == "different"), ("T2b f5", f5 == "not confirmed"),
                             ("T4", t4 == "sensitive"), ("T5 g", g == "major"), ("T5 a5", a5 == "not confirmed"))
           if cond]
    if bad:
        return "challenged", bad
    und = [n for n, ok in (("T2a", t2a_pop == "consistent with 2.7 kpc"),
                           ("T2b f5", f5 == "most within 5 kpc confirmed"), ("T4", t4 == "robust"),
                           ("T5 g", g in ("minor", "moderate")),
                           ("T5 a5", a5 == "most apocentres below 5 kpc confirmed")) if not ok]
    return "undetermined", und
