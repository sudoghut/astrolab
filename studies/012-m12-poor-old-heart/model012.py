"""T2a/T2b of study 012: line-of-sight likelihoods, fits, profile intervals, f5, known-answer mocks
(README 4.3 and 4.4). Every tunable arrives as an argument; this module never imports run.

Conventions (README 4.1): Galactocentric frame with R0 (8.2 kpc), the Sun in the plane, x towards the
Centre; parallaxes in mas, distances in kpc; the model uses the corrected parallax
plx_corr = plx_raw + zp (zp = 0.02 mas), the cuts act on the raw parallax.
"""
from __future__ import annotations

import math
import time

import numpy as np
from scipy.optimize import minimize, minimize_scalar
from scipy.special import ndtr
from scipy.stats import chi2

MODELS = ("sph", "flat", "pow")
BOUNDS = {"sph": [(0.5, 10.0)], "flat": [(0.5, 10.0), (0.2, 1.5)],
          "pow": [(0.05, 3.0), (1.0, 8.0), (0.2, 1.5)]}
# Gaia passband extinction relative to A_V (Wang & Chen 2019, ApJ 877, 116; README 4.13 item 6)
EXT_G, EXT_BP, EXT_RP = 0.789, 1.002, 0.589
SQRT2PI = math.sqrt(2.0 * math.pi)


# ---------------------------------------------------------------------------------------------
# Geometry and grid

def gc_r2_z2(l_deg, b_deg, d, R0):
    """Squared Galactocentric radius and squared height for heliocentric (l, b, d); arrays broadcast."""
    l = np.radians(l_deg)
    b = np.radians(b_deg)
    cb = np.cos(b)
    r2 = d * d - 2.0 * d * R0 * cb * np.cos(l) + R0 * R0
    z2 = (d * np.sin(b)) ** 2
    return r2, z2


def dist_grid(dmin, dmax, k):
    d = np.geomspace(dmin, dmax, int(k))
    plx = 1.0 / d
    # trapezoid weights in parallax (|d plx|)
    w = np.zeros_like(plx)
    dp = np.abs(np.diff(plx))
    w[:-1] += 0.5 * dp
    w[1:] += 0.5 * dp
    return d, plx, w


def lum_cut(g, bp_rp):
    """R22's luminosity cut on the raw parallax (mas): plx < 100 * 10**(0.2*(0.9 - (G - 1.5(BP-RP-1))))."""
    return 100.0 * 10.0 ** (0.2 * (0.9 - (g - 1.5 * (bp_rp - 1.0))))


def cut_ii(g, bp_rp, plx_max=1.0):
    return np.minimum(plx_max, lum_cut(g, bp_rp))


# ---------------------------------------------------------------------------------------------
# Likelihood

class Lik:
    """Per-star likelihoods conditional on direction (README 4.3).

    version "i": both integrals over true distances [d1_i, dmax] (1-30 kpc), no selection term.
    version "ii": numerator and selection-weighted denominator over [dmin, dmax] (0.2-30 kpc),
    selection P(plx_raw < cut_i) = Phi((cut_i - plx + zp)/sigma_i).
    Matrices are stored as float32 (memory) and evaluated in float64 chunks.
    """

    def __init__(self, l, b, plx_raw, plx_err, g=None, bp_rp=None, *, version, k=300, R0=8.2, zp=0.02,
                 dmin=0.2, dmax=30.0, d1_i=1.0, plx_max=1.0, extra_cut=None, chunk=2048):
        self.version = version
        self.k = int(k)
        self.chunk = int(chunk)
        lo = d1_i if version == "i" else dmin
        d, plx, w = dist_grid(lo, dmax, k)
        self.d = d
        l = np.asarray(l, float)[:, None]
        b = np.asarray(b, float)[:, None]
        pc = (np.asarray(plx_raw, float) + zp)[:, None]
        s = np.asarray(plx_err, float)[:, None]
        self.n = l.shape[0]
        base = (w * plx ** -4.0)[None, :]
        self.A = np.empty((self.n, self.k), np.float32)
        self.B = np.empty((self.n, self.k), np.float32)
        self.R2 = np.empty((self.n, self.k), np.float32)
        self.Z2 = np.empty((self.n, self.k), np.float32)
        if version == "ii":
            cut = cut_ii(np.asarray(g, float), np.asarray(bp_rp, float), plx_max)
            if extra_cut is not None:
                cut = np.minimum(cut, extra_cut)
            cut = cut[:, None]
        for i0 in range(0, self.n, self.chunk):
            sl = slice(i0, i0 + self.chunk)
            r2, z2 = gc_r2_z2(l[sl], b[sl], d[None, :], R0)
            self.R2[sl] = r2
            self.Z2[sl] = z2
            self.A[sl] = base * np.exp(-0.5 * ((pc[sl] - plx[None, :]) / s[sl]) ** 2) / (SQRT2PI * s[sl])
            if version == "ii":
                self.B[sl] = base * ndtr((cut[sl] - plx[None, :] + zp) / s[sl])
            else:
                self.B[sl] = np.broadcast_to(base, (min(self.chunk, self.n - i0), self.k))
        self.nevals = 0

    def per_star(self, model, theta):
        self.nevals += 1
        out = np.empty(self.n)
        for i0 in range(0, self.n, self.chunk):
            sl = slice(i0, i0 + self.chunk)
            r2 = self.R2[sl].astype(np.float64)
            if model == "sph":
                lr = r2 * (-0.5 / theta[0] ** 2)
            else:
                q = theta[-1]
                rq = r2 + self.Z2[sl] * (1.0 / (q * q) - 1.0)
                if model == "flat":
                    lr = rq * (-0.5 / theta[0] ** 2)
                else:
                    rc, alpha = theta[0], theta[1]
                    lr = np.log(rq + rc * rc) * (-0.5 * alpha)
            m = lr.max(axis=1, keepdims=True)
            e = np.exp(lr - m)
            num = np.einsum("ij,ij->i", self.A[sl], e)
            den = np.einsum("ij,ij->i", self.B[sl], e)
            out[sl] = np.log(np.maximum(num, 1e-300)) - np.log(np.maximum(den, 1e-300))
        return out

    def lnl(self, model, theta, weights=None):
        ps = self.per_star(model, np.asarray(theta, float))
        return float(ps.sum() if weights is None else np.dot(weights, ps))


# ---------------------------------------------------------------------------------------------
# Fits

def at_bound(x, lo, hi, tol=0.05):
    return bool(x - lo < tol or hi - x < tol)


def fit_sigma(lik, weights=None, q=None, bounds=(0.5, 10.0), xatol=1e-4):
    """Brent on sigma (README 4.3): spherical, or flattened at fixed q (profile)."""
    model, mk = ("sph", lambda s: (s,)) if q is None else ("flat", lambda s: (s, q))
    r = minimize_scalar(lambda s: -lik.lnl(model, mk(s), weights), bounds=bounds, method="bounded",
                        options={"xatol": xatol})
    s = float(r.x)
    return {"sigma": s, "lnl": float(-r.fun), "at_bound": at_bound(s, *bounds), "nfev": int(r.nfev)}


def random_starts(rng, model, n):
    bd = BOUNDS[model]
    return [np.array([rng.uniform(lo, hi) for lo, hi in bd]) for _ in range(n)]


def first_start(model, sph_sigma, flat_theta=None):
    """README 4.4: the first start is the spherical sigma with q = 1; for the power law (no sigma) the
    first start is r_c = 1 kpc, alpha = 3.4, q from the flattened fit (README 4.13 item 9)."""
    if model == "flat":
        return np.array([sph_sigma, 1.0])
    q = 1.0 if flat_theta is None else float(flat_theta[1])
    return np.array([1.0, 3.4, q])


def fit_nm(lik, model, starts, weights=None, maxfev=3000):
    best = None
    nfev = 0
    bd = BOUNDS[model]
    for x0 in starts:
        x0 = np.clip(np.asarray(x0, float), [b[0] for b in bd], [b[1] for b in bd])
        r = minimize(lambda t: -lik.lnl(model, t, weights), x0, method="Nelder-Mead", bounds=bd,
                     options={"xatol": 1e-4, "fatol": 1e-4, "maxfev": maxfev})
        nfev += int(r.nfev)
        if best is None or -r.fun > best["lnl"]:
            best = {"theta": [float(v) for v in r.x], "lnl": float(-r.fun), "converged": bool(r.success)}
    best["nfev"] = nfev
    return best


def q_interval(qs, two_delta, thr=3.84):
    """README 4.4: ends by linear interpolation of 2*Delta between adjacent nodes where it crosses thr;
    more than two crossings -> [lowest, highest] with a flag; 2*Delta below thr at a grid end -> that
    end is the grid edge."""
    qs = np.asarray(qs, float)
    td = np.asarray(two_delta, float)
    order = np.argsort(qs)
    qs, td = qs[order], td[order]
    cross = []
    for j in range(len(qs) - 1):
        a, b = td[j] - thr, td[j + 1] - thr
        if a == 0:
            cross.append(qs[j])
        elif a * b < 0:
            cross.append(qs[j] + (qs[j + 1] - qs[j]) * a / (a - b))
    if td[-1] == thr:
        cross.append(qs[-1])
    below = td <= thr
    if not below.any():
        return {"lo": None, "hi": None, "crossings": len(cross), "flag": "no node within threshold"}
    lo = qs[0] if below[0] else None
    hi = qs[-1] if below[-1] else None
    inner = sorted(set(round(c, 12) for c in cross))
    if lo is None:
        lo = inner[0] if inner else float(qs[np.argmax(below)])
    if hi is None:
        hi = inner[-1] if inner else float(qs[len(qs) - 1 - np.argmax(below[::-1])])
    flag = "more than two crossings" if len(inner) > 2 else ""
    return {"lo": float(lo), "hi": float(hi), "crossings": len(inner), "flag": flag}


def profile_q(lik, flat_fit, sph_lnl, weights=None, q_min=0.2, q_max=1.5, q_step=0.05):
    """README 4.4 profile of q: grid nodes with sigma refitted, plus the Nelder-Mead node."""
    n = int(round((q_max - q_min) / q_step)) + 1
    grid = [round(q_min + i * q_step, 10) for i in range(n)]
    vals = [fit_sigma(lik, weights, q=q)["lnl"] for q in grid]
    qs = grid + [flat_fit["theta"][1]]
    ln = vals + [flat_fit["lnl"]]
    lmax = max(flat_fit["lnl"], max(vals))
    td = [2.0 * (lmax - v) for v in ln]
    iv = q_interval(qs, td)
    j1 = int(np.argmin(np.abs(np.array(grid) - 1.0)))
    return {"q_grid": grid, "lnl_grid": vals, "lnl_max": lmax, "interval": iv,
            "check_q1_minus_sph": vals[j1] - sph_lnl, "check_q1_ok": abs(vals[j1] - sph_lnl) <= 0.01}


def step1_label(two_dlnl, iv, thr=10.0, q_flat=0.8):
    if two_dlnl > thr and iv["hi"] is not None and iv["hi"] < q_flat:
        return "flattened preferred"
    if two_dlnl > thr and iv["lo"] is not None and iv["lo"] > 1.0:
        return "prolate preferred"
    return "spherical adequate"


def delta_bic(lnl_complex, lnl_simple, n, dk=1):
    return 2.0 * (lnl_complex - lnl_simple) - dk * math.log(n)


def step2_label(dbic, thr=10.0):
    return "power law preferred" if dbic > thr else "flattened Gaussian adequate"


def step1(lik, rng, sph=None, weights=None, n_starts=5, profile=True):
    """Spherical fit, flattened fit (5 starts), q profile and the step-1 label (README 4.4)."""
    sph = sph or fit_sigma(lik, weights)
    starts = [first_start("flat", sph["sigma"])] + random_starts(rng, "flat", n_starts - 1)
    flat = fit_nm(lik, "flat", starts, weights)
    out = {"sph": sph, "flat": flat, "two_dlnl": 2.0 * (flat["lnl"] - sph["lnl"])}
    if profile:
        out["profile"] = profile_q(lik, flat, sph["lnl"], weights)
        out["label"] = step1_label(out["two_dlnl"], out["profile"]["interval"])
    return out


def fit_pow(lik, rng, flat_theta, weights=None, n_starts=5):
    starts = [first_start("pow", None, flat_theta)] + random_starts(rng, "pow", n_starts - 1)
    return fit_nm(lik, "pow", starts, weights)


# ---------------------------------------------------------------------------------------------
# Fraction within 5 kpc (README 4.4)

_MU, _MUW = np.polynomial.legendre.leggauss(64)
_MU = 0.5 * (_MU + 1.0)
_MUW = 0.5 * _MUW


def f5_sph(sigma, r=5.0):
    return float(chi2.cdf((r / sigma) ** 2, 3))


def f5_flat(sigma, q, r=5.0):
    s = 1.0 - _MU ** 2 + _MU ** 2 / (q * q)
    w = _MUW * s ** -1.5
    return float(np.sum(w * chi2.cdf(r * r * s / sigma ** 2, 3)) / np.sum(w))


def f5_pow(rc, alpha, q, r=5.0, rmax=18.0, n=4000):
    rr = np.linspace(0.0, rmax, n + 1)[1:]
    dr = rmax / n
    s = 1.0 - _MU ** 2 + _MU ** 2 / (q * q)
    dens = (rr[:, None] ** 2 * s[None, :] + rc * rc) ** (-alpha / 2.0)
    shell = (dens * _MUW[None, :]).sum(axis=1) * rr ** 2 * dr
    return float(shell[rr <= r].sum() / shell.sum())


def f5_of(model, theta):
    if model == "sph":
        return f5_sph(theta[0])
    if model == "flat":
        return f5_flat(theta[0], theta[1])
    return f5_pow(*theta)


# ---------------------------------------------------------------------------------------------
# Known-answer mocks (README 4.3)

def extinction(a, b_d, b_deg, d):
    """A_G, A_BP - A_G and E(BP-RP) for A_G = a exp(-|b|/b_d) min(d, 8)/8."""
    ag = a * np.exp(-np.abs(b_deg) / b_d) * np.minimum(d, 8.0) / 8.0
    return ag, ag * (EXT_BP / EXT_G - 1.0), ag * (EXT_BP - EXT_RP) / EXT_G


class LFSample:
    """The luminosity-function stars: M' and observed colour, made intrinsic with an extinction model."""

    def __init__(self, g, bp_rp, bp, plx_raw, b_deg, zp=0.02):
        self.g = np.asarray(g, float)
        self.c = np.asarray(bp_rp, float)
        self.bpg = np.asarray(bp, float) - self.g
        pc = np.asarray(plx_raw, float) + zp
        self.mprime = self.g - 1.5 * (self.c - 1.0) + 5.0 * np.log10(pc / 100.0)
        self.d = 1.0 / pc
        self.b = np.asarray(b_deg, float)
        self.n = self.g.size

    def intrinsic(self, a, b_d):
        ag, abpg, e = extinction(a, b_d, self.b, self.d)
        mg0 = self.mprime + 1.5 * (self.c - 1.0) - ag
        return mg0, self.c - e, self.bpg - abpg


class ErrSampler:
    """Parallax errors drawn by resampling the data's sigma_plx within 0.25 mag bins of G."""

    def __init__(self, g, plx_err, width=0.25):
        g = np.asarray(g, float)
        e = np.asarray(plx_err, float)
        ok = np.isfinite(g) & np.isfinite(e) & (e > 0)
        g, e = g[ok], e[ok]
        self.w = width
        self.lo = math.floor(g.min() / width)
        idx = np.floor(g / width).astype(int) - self.lo
        self.nb = int(idx.max()) + 1
        order = np.argsort(idx, kind="stable")
        self.e = e[order]
        counts = np.bincount(idx, minlength=self.nb)
        self.start = np.concatenate([[0], np.cumsum(counts)[:-1]])
        self.count = counts
        filled = np.nonzero(counts)[0]
        near = np.abs(np.arange(self.nb)[:, None] - filled[None, :]).argmin(axis=1)
        self.use = filled[near]

    def draw(self, rng, g):
        idx = np.clip(np.floor(np.asarray(g, float) / self.w).astype(int) - self.lo, 0, self.nb - 1)
        idx = self.use[idx]
        u = rng.random(idx.size)
        return self.e[self.start[idx] + (u * self.count[idx]).astype(int)]


def draw_positions(rng, n, sigma, q, R0):
    x = rng.normal(0.0, sigma, n) + R0
    y = rng.normal(0.0, sigma, n)
    z = rng.normal(0.0, sigma * q, n)
    d = np.sqrt(x * x + y * y + z * z)
    l = np.degrees(np.arctan2(y, x))
    b = np.degrees(np.arcsin(z / d))
    return l, b, d


def apply_extra_cuts(declared, vals):
    """L6-declared cuts (README 3): {quantity: [{"side", "c"}]} applied to simulated observed values."""
    ok = np.ones(next(iter(vals.values())).size, bool)
    for qn, cuts in (declared or {}).items():
        if qn not in vals:
            continue
        v = vals[qn]
        for c in cuts:
            if c.get("c") is None:
                continue
            ok &= (v < c["c"]) if c["side"] == "upper" else (v >= c["c"])
    return ok


def simulate(rng, n_target, *, sigma, q, lf, ext, errs, R0=8.2, zp=0.02, declared=None, bmin=0.0,
             completeness=False, dlim=(0.5, 30.0), bp_max=15.5, col=(1.0, 3.5), plx_max=1.0,
             field=30.0, batch=None, max_draws=50_000_000):
    """Draw mock stars until n_target pass every cut (README 4.3 'Observed quantities' and 'Size').
    ext = (a, b_d). Returns a dict of arrays of the accepted stars (in draw order)."""
    a, b_d = ext
    mg0_all, c0_all, bpg0_all = lf.intrinsic(a, b_d)
    keep = {k: [] for k in ("l", "b", "plx", "err", "g", "bp_rp", "bp")}
    got = drawn = 0
    batch = batch or max(4 * n_target, 10_000)
    while got < n_target:
        if drawn > max_draws:
            raise RuntimeError("mock acceptance too low")
        l, b, d = draw_positions(rng, batch, sigma, q, R0)
        drawn += batch
        m = (np.abs(l) < field) & (np.abs(b) < field) & (d > dlim[0]) & (d < dlim[1]) & (np.abs(b) >= bmin)
        if completeness:   # README 4.4 false-positive mocks: c(b, d), random thinning, not in the fit
            c = 1.0 - 0.5 * np.exp(-(np.abs(b) - 5.0) / 5.0) * np.minimum(d, 8.0) / 8.0
            m &= rng.random(batch) < c
        l, b, d = l[m], b[m], d[m]
        j = rng.integers(0, lf.n, l.size)
        ag, abpg, e = extinction(a, b_d, b, d)
        mu = 5.0 * np.log10(d * 100.0)
        g = mg0_all[j] + mu + ag
        c = c0_all[j] + e
        bp = g + bpg0_all[j] + abpg
        err = errs.draw(rng, g)
        plx = 1.0 / d - zp + rng.normal(0.0, 1.0, l.size) * err
        ok = (plx < plx_max) & (plx < lum_cut(g, c)) & (bp < bp_max) & (c > col[0]) & (c < col[1])
        if declared:
            ok &= apply_extra_cuts(declared, {"parallax": plx, "parallax_over_error": plx / err, "bp": bp,
                                              "bp_rp": c, "l": l, "b": b})
        for k, v in (("l", l), ("b", b), ("plx", plx), ("err", err), ("g", g), ("bp_rp", c), ("bp", bp)):
            keep[k].append(v[ok])
        got += int(ok.sum())
    out = {k: np.concatenate(v)[:n_target] for k, v in keep.items()}
    out["drawn"] = drawn
    return out


# ---------------------------------------------------------------------------------------------
# Extinction grid (README 4.3)

B_BINS = ((0.0, 5.0), (5.0, 10.0), (10.0, 20.0), (20.0, 30.0))


def colour_stats(b_deg, bp_rp):
    ab = np.abs(np.asarray(b_deg, float))
    c = np.asarray(bp_rp, float)
    out = []
    for lo, hi in B_BINS:
        m = (ab >= lo) & (ab < hi)
        if m.sum() == 0:
            out += [np.nan, np.nan]
        else:
            out += [float(np.median(c[m])), float(np.percentile(c[m], 90))]
    return np.array(out)


def extinction_grid(data_b, data_c, *, n_target, lf, errs, a_values, bd_values, seed, sigma=2.7, R0=8.2,
                    zp=0.02, declared=None, check_time=None):
    """One mock per grid point with common random numbers (README 4.13 item 7); least sum of squared
    differences of the 8 statistics, ties to the smallest a, then the smallest b_d."""
    target = colour_stats(data_b, data_c)
    best = None
    ssd = np.full((len(a_values), len(bd_values)), np.nan)
    for i, a in enumerate(a_values):
        if check_time:
            check_time(f"extinction grid a={a:.2f}")
        for j, bd in enumerate(bd_values):
            rng = np.random.default_rng(seed)
            sim = simulate(rng, n_target, sigma=sigma, q=1.0, lf=lf, ext=(a, bd), errs=errs, R0=R0, zp=zp,
                           declared=declared)
            st = colour_stats(sim["b"], sim["bp_rp"])
            v = float(np.nansum((st - target) ** 2))
            ssd[i, j] = v
            if best is None or v < best[0] - 1e-15:
                best = (v, float(a), float(bd))
    return {"a": best[1], "b_d": best[2], "ssd": best[0], "target_stats": target.tolist(),
            "ssd_grid_min_per_a": np.nanmin(ssd, axis=1).round(6).tolist()}


# ---------------------------------------------------------------------------------------------
# Cost (README 4.10): one likelihood evaluation on synthetic stars of the real size

def synthetic_stars(rng, n):
    l = rng.uniform(-30, 30, n)
    b = rng.uniform(-30, 30, n)
    d = np.clip(rng.normal(8.2, 2.5, n), 1.2, 25)
    err = rng.uniform(0.012, 0.05, n)
    g = rng.uniform(11.0, 15.0, n)
    c = rng.uniform(1.1, 3.0, n)
    plx = 1.0 / d - 0.02 + rng.normal(0, 1, n) * err
    return l, b, np.minimum(plx, 0.99), err, g, c


def time_evaluations(n_stars, k=300, n_eval=5, seed=1):
    rng = np.random.default_rng(seed)
    l, b, plx, err, g, c = synthetic_stars(rng, n_stars)
    t0 = time.perf_counter()
    lik2 = Lik(l, b, plx, err, g, c, version="ii", k=k)
    build = time.perf_counter() - t0
    lik1 = Lik(l, b, plx, err, version="i", k=k)
    out = {"n_stars": int(n_stars), "nodes": int(k), "build_s": build}
    for name, lik, model, th in (("i_sph", lik1, "sph", (2.7,)), ("ii_sph", lik2, "sph", (2.7,)),
                                 ("ii_flat", lik2, "flat", (2.7, 0.7)), ("ii_pow", lik2, "pow", (0.5, 3.4, 0.7))):
        lik.lnl(model, th)
        t0 = time.perf_counter()
        for _ in range(n_eval):
            lik.lnl(model, th)
        out[name + "_s"] = (time.perf_counter() - t0) / n_eval
    return out


# Evaluations per fit measured on a synthetic 18,000-star mock at 300 nodes (2026-11-21): Brent on sigma
# 11-12; Nelder-Mead flattened 365 for 5 starts; power law 951 for 5 starts; q profile 306.
MEASURED_EVALS = {"evals_1p": 12, "evals_2p": 73, "evals_3p": 190, "evals_profile": 306}
PREREG_EVALS = {"evals_1p": 25, "evals_2p": 150, "evals_3p": 300, "evals_profile": 27 * 25}


def project_hours(t, *, n_boot=200, n_mocks=100, n_starts=5, evals_1p=25, evals_2p=150, evals_3p=300,
                  evals_profile=27 * 25, second_fp=False, step2=True, n_extinction=3939, mock_sim_s=0.05,
                  n_t4_runs=24, n_ref=50000, n_stars=20000):
    """Projected hours of the formal run's likelihood work from measured per-evaluation times (t, at
    n_stars), with evaluation counts per fit (README 4.10's defaults, or MEASURED_EVALS)."""
    e1, e2, e3 = t["ii_sph_s"], t["ii_flat_s"], t["ii_pow_s"]
    flat = n_starts * evals_2p * e2
    pw = n_starts * evals_3p * e3
    prof = evals_profile * e2
    sec = {"extinction_grid": n_extinction * mock_sim_s,
           "t2a": (1 + n_boot + n_mocks) * evals_1p * (t["i_sph_s"] + e1),
           "t2b_bootstrap": n_boot * (evals_1p * e1 + flat + pw),
           "t2b_mocks_fp_power": 2 * n_mocks * (evals_1p * e1 + flat + prof)}
    if step2:
        sec["t2b_step2_mocks"] = n_mocks * (evals_1p * e1 + flat + pw)
    if second_fp:
        sec["t2b_second_fp"] = n_mocks * (evals_1p * e1 + flat + prof)
    scale = n_ref / n_stars
    sec["reference_control_latitude"] = (scale * (4 * evals_1p * e1 + evals_1p * e1 + flat + pw + prof)
                                         + 2 * (evals_1p * e1 + flat + pw + prof))
    sec["t4_sigma_fits"] = n_t4_runs * evals_1p * (t["i_sph_s"] + e1)
    return {k: v / 3600.0 for k, v in sec.items()} | {"total": sum(sec.values()) / 3600.0}
