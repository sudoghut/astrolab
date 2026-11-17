"""R6-COV (README section 2.6, addendum 2026-11-17, T-028): the rotation-curve tests under correlated
covariances that keep Table 3's sigma on the diagonal and are calibrated so that the best-fit Einasto
chi^2 equals its degrees of freedom. Helper module: does not import run; callers pass every value."""
import numpy as np
from scipy import linalg, optimize

import rc

ALPHA_LCDM = 0.17          # 1/n of the LCDM-like Einasto halo


# ------------------------------------------------------------------ covariances ----

def kernel_corr(R, kind):
    """Unit-diagonal correlation kernel: ("se", ell) squared exponential, or ("global", None)."""
    name, ell = kind
    d = R[:, None] - R[None, :]
    if name == "global":
        return np.ones_like(d)
    return np.exp(-d ** 2 / (2.0 * ell ** 2))


def cov_kernel(sig, K, f):
    return np.outer(sig, sig) * ((1.0 - f) * np.eye(len(sig)) + f * K)


def cov_fractional(V, sig, c):
    return np.diag(sig ** 2 - c ** 2 * V ** 2) + c ** 2 * np.outer(V, V)


def max_corr_fraction(kind, value, V, sig):
    """Largest per-bin correlated fraction of the variance (the high-f flag's quantity)."""
    if kind[0] == "fractional":
        return float(np.max(value ** 2 * V ** 2 / sig ** 2))
    return float(value)


def make_cov(kind, value, R, V, sig):
    if kind[0] == "fractional":
        return cov_fractional(V, sig, value)
    return cov_kernel(sig, kernel_corr(R, kind), value)


def chi2(resid, cho):
    return float(resid @ linalg.cho_solve(cho, resid))


# ------------------------------------------------------------------ halo models ----

# Fixed by the pre-registration (README 2.6), deliberately not PARAMS knobs: changing them changes R6-COV.
HALO_BOUNDS = {
    # coordinates: free Einasto (log10 M0, h, 1/n) with R2's bounds; NFW (log10 rho_s, log10 r_s) with R5's;
    # LCDM-like Einasto (log10 rho_-2, log10 r_-2) with 1/n = 0.17
    "einasto": [(10.0, 14.0), (0.0, 20.0), (0.0, 5.0)],
    "nfw": [(4.0, 10.0), (0.0, 2.0)],
    "lcdm": [(3.0, 10.0), (0.0, float(np.log10(300.0)))],
}
EXTRA_START = {"einasto": [np.log10(3.7e11), 12.0, 2.4], "nfw": [7.0, 1.2], "lcdm": [6.0, np.log10(20.0)]}


def lcdm_params(lrho2, lr2, alpha=ALPHA_LCDM):
    """(rho_-2, r_-2) -> (M0, h, 1/n) of J23's Einasto form rho0 exp[-(r/h)^alpha]."""
    r2 = 10.0 ** lr2
    h = r2 * (alpha / 2.0) ** (1.0 / alpha)
    rho0 = 10.0 ** lrho2 * np.exp(2.0 / alpha)
    return 4.0 * np.pi * h ** 3 * rho0, h, alpha


def mass_fn(kind, x):
    if kind == "einasto":
        return lambda r: rc.einasto_mass(r, 10.0 ** x[0], x[1], x[2])
    if kind == "nfw":
        return lambda r: rc.nfw_mass(r, 10.0 ** x[0], 10.0 ** x[1])
    m0, h, inv_n = lcdm_params(x[0], x[1])
    return lambda r: rc.einasto_mass(r, m0, h, inv_n)


def in_bounds(kind, x):
    b = HALO_BOUNDS[kind]
    if kind == "einasto":        # R2: h in (0, 20], 1/n in (0, 5]
        return b[0][0] <= x[0] <= b[0][1] and 0.0 < x[1] <= b[1][1] and 0.0 < x[2] <= b[2][1]
    return all(lo <= v <= hi for v, (lo, hi) in zip(x, b))


def halo_chi2(kind, x, R, V, vb2, cho):
    if not in_bounds(kind, x):
        return 1e30
    with np.errstate(all="ignore"):
        v2 = vb2 + rc.G * mass_fn(kind, x)(R) / R
    if not np.all(np.isfinite(v2)) or np.any(v2 <= 0):
        return 1e30
    return chi2(V - np.sqrt(v2), cho)


def fit_halo(kind, R, V, vb2, cho, n_starts=20, seed=0, agree_tol=0.01):
    """README 2.6 fits: Nelder-Mead from n_starts uniform starts (fresh default_rng(seed)) plus the extra
    start; best = minimum over all; converged if at least 3 successfully terminated starts lie within
    agree_tol of it."""
    rng = np.random.default_rng(seed)
    b = HALO_BOUNDS[kind]
    starts = [np.array([rng.uniform(lo, hi) for lo, hi in b]) for _ in range(n_starts)]
    starts.append(np.array(EXTRA_START[kind], dtype=float))
    f = lambda x: halo_chi2(kind, x, R, V, vb2, cho)
    res = [optimize.minimize(f, s, method="Nelder-Mead",
                             options={"maxiter": 20000, "xatol": 1e-8, "fatol": 1e-10}) for s in starts]
    vals = np.array([r.fun for r in res])
    ok = np.array([bool(r.success) for r in res]) & (vals < 1e29)
    if not ok.any():
        return {"chi2": float(np.min(vals)), "x": [float(v) for v in res[int(np.argmin(vals))].x], "n_agree": 0,
                "converged": False, "at_bound": []}
    k = int(np.flatnonzero(ok)[np.argmin(vals[ok])])            # minimum over successful runs (README 2.6)
    n_agree = int(np.sum(ok & (vals <= vals[k] + agree_tol)))
    x = res[k].x
    at_bound = []
    for j, (lo, hi) in enumerate(b):
        if np.isclose(x[j], lo, atol=1e-6 * (hi - lo)) or np.isclose(x[j], hi, atol=1e-6 * (hi - lo)):
            at_bound.append(j)
    return {"chi2": float(vals[k]), "x": [float(v) for v in x], "n_agree": n_agree,
            "converged": bool(n_agree >= 3), "at_bound": at_bound}


def m_vir(kind, x, m_bar, rho_cr):
    """Primary R_vir (dark matter only, section 2.2) and M_vir = M_bar + M_DM(<R_vir)."""
    mf = mass_fn(kind, x)
    rv = rc.r_vir(mf, rho_cr, 0.0)
    if rv is None:
        rv = rc.r_vir(mf, rho_cr, 0.0, bracket=(1.0, 1e4))
    return {"r_vir": rv, "m_vir": None if rv is None else float(m_bar + mf(rv))}


# ------------------------------------------------------------------ power-law profile ----

def gls_profile(R, V, C, gamma):
    """chi^2 at fixed gamma with the GLS amplitude (pivot 1 kpc); None if A <= 0."""
    cho = linalg.cho_factor(C)
    x = R ** gamma
    cx = linalg.cho_solve(cho, x)
    a = float(cx @ V / (cx @ x))
    if a <= 0:
        return None, a
    r = V - a * x
    return chi2(r, cho), a


def powerlaw_tests(R, V, C, lo=-3.0, hi=1.0, step=0.001):
    """T1 and T2 from the profile chi^2(gamma) (README 2.6)."""
    grid = np.round(np.arange(lo, hi + step / 2, step), 6)
    vals = []
    for g in grid:
        c, _ = gls_profile(R, V, C, g)
        vals.append(np.inf if c is None else c)
    vals = np.array(vals)
    k = int(np.argmin(vals))
    a, b = grid[max(k - 1, 0)], grid[min(k + 1, len(grid) - 1)]
    def fn(g):
        c, _ = gls_profile(R, V, C, g)
        return np.inf if c is None else c
    ref = optimize.minimize_scalar(fn, bounds=(a, b), method="bounded", options={"xatol": 1e-7})
    gmin, cmin = (float(ref.x), float(ref.fun)) if ref.fun <= vals[k] else (float(grid[k]), float(vals[k]))
    edge = bool(k == 0 or k == len(grid) - 1)
    out = {"gamma_min": gmin, "chi2_min": cmin, "at_edge": edge, "n_bins": int(len(R)),
           "chi2_per_dof": cmin / (len(R) - 2)}
    pts = {}
    for name, g in (("flat", 0.0), ("kepler", -0.5), ("g02", -0.2)):
        c, _ = gls_profile(R, V, C, g)
        pts[name] = c
    if any(v is None for v in pts.values()):
        out.update({"t1_evaluable": pts["flat"] is not None,
                    "t2_evaluable": pts["kepler"] is not None and pts["g02"] is not None})
    else:
        out.update({"t1_evaluable": True, "t2_evaluable": True})
    if out["t1_evaluable"]:
        d = max(pts["flat"] - cmin, 0.0)
        out["dchi2_flat"] = float(d)
        out["sigma_flat"] = float(np.sqrt(d))
    if out["t2_evaluable"]:
        out["D_K"] = float(pts["kepler"] - cmin)
        out["D_02"] = float(pts["g02"] - cmin)
        out["pref_kepler"] = out["D_02"] - out["D_K"]
    return out


# ------------------------------------------------------------------ calibration ----

def calibrate(chi2_at, grid, target, tol):
    """Smallest grid value with chi2 >= target, then bisection in the cell below (README 2.6).
    chi2_at(v) -> chi2 or None (fit not converged). Returns dict with status, value and the curve."""
    curve = [(float(v), chi2_at(v)) for v in grid]
    valid = [(v, c) for v, c in curve if c is not None]
    k = next((i for i, (v, c) in enumerate(curve) if c is not None and c >= target), None)
    if k is None:
        return {"status": "not calibratable", "value": float(grid[-1]), "curve": curve}
    if k == 0:      # chi2 >= target already at the bottom of the range (not covered by README 2.6; unreachable here)
        return {"status": "calibrated", "value": float(grid[0]), "curve": curve}
    lo, hi = float(grid[k - 1]), float(grid[k])
    if curve[k - 1][1] is None:
        return {"status": "not evaluable", "value": None, "curve": curve}
    width = tol * (float(grid[-1]) - float(grid[0]))
    while hi - lo > width:
        mid = 0.5 * (lo + hi)
        c = chi2_at(mid)
        if c is None:
            return {"status": "not evaluable", "value": None, "curve": curve}
        if c >= target:
            hi = mid
        else:
            lo = mid
    return {"status": "calibrated", "value": 0.5 * (lo + hi), "curve": curve}


# ------------------------------------------------------------------ labels ----

def _t1(v):
    if all(x >= 3 for x in v):
        return "flat rejected at >= 3 sigma"
    if all(x >= 2 for x in v):
        return "flat rejected at >= 2 sigma"
    if all(x < 2 for x in v):
        return "flat not rejected at 2 sigma"
    return "kernel-dependent"


def _t2(v):
    if all(x >= 4 for x in v):
        return "Keplerian favoured over gamma = -0.2"
    if all(x <= -4 for x in v):
        return "gamma = -0.2 favoured over Keplerian"
    if all(abs(x) < 4 for x in v):
        return "not distinguished"
    return "kernel-dependent"


def _t3(v):
    band = {("not disfavoured" if x < 4 else "mildly disfavoured" if x < 9 else "disfavoured") for x in v}
    return band.pop() if len(band) == 1 else "kernel-dependent"


RULES = {"t1": _t1, "t2": _t2, "t3": _t3}


def label(test, values, flags, min_n=3):
    """values: {cov: number or None (not evaluable / not calibratable)}; flags: {cov: high-f bool}.
    README 2.6 order: all usable covariances (>= min_n), then the unflagged ones."""
    rule = RULES[test]
    use = {k: v for k, v in values.items() if v is not None}
    if len(use) < min_n:
        return "not evaluable"
    lab_all = rule(list(use.values()))
    unflagged = [v for k, v in use.items() if not flags.get(k)]
    if len(unflagged) < min_n:
        return lab_all + " (only with high-f covariances)"
    lab_unf = rule(unflagged)
    return lab_all if lab_all == lab_unf else "kernel-dependent (high-f)"
