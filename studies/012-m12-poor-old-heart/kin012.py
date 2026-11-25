"""T3 (rotation against metallicity) and T5 (GSE and halo stars) of study 012 (README 4.5, 4.7).

Every tunable arrives as an argument; this module never imports run.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.optimize import least_squares

import stats012 as S

LN9x2 = 2.0 * math.log(9.0)


def ratio(jr, jphi, jz, flip=False):
    jphi = -np.asarray(jphi, float) if flip else np.asarray(jphi, float)
    jtot = np.sqrt(np.asarray(jr, float) ** 2 + jphi ** 2 + np.asarray(jz, float) ** 2)
    with np.errstate(invalid="ignore", divide="ignore"):
        return jphi / jtot


def boot_subset(rng, n_total, n_sub):
    """Indices into a subset of size n_sub for one bootstrap resample of all n_total stars, restricted
    to the subset: K ~ Binomial(n_total, n_sub/n_total) draws, uniform within the subset. Equal in
    distribution to resampling all stars and keeping those in the subset (README 4.12 item 11)."""
    k = rng.binomial(n_total, n_sub / n_total) if n_total > 0 else 0
    return rng.integers(0, n_sub, k) if n_sub > 0 else np.zeros(0, int)


def bin_index(mh, centers, width):
    """Bin j holds c_j - width/2 <= [M/H] < c_j + width/2; -1 outside."""
    centers = np.asarray(centers, float)
    lo = centers[0] - width / 2
    j = np.floor((np.asarray(mh, float) - lo) / width + 1e-9).astype(int)
    j[(j < 0) | (j >= len(centers))] = -1
    return j


def bin_means(j, f, nb):
    ok = j >= 0
    n = np.bincount(j[ok], minlength=nb).astype(float)
    s = np.bincount(j[ok], weights=f[ok], minlength=nb)
    with np.errstate(invalid="ignore", divide="ignore"):
        return s / n, n


def logistic(x, a, b, m, s):
    return a + (b - a) / (1.0 + np.exp(-(x - m) / s))


def fit_logistic(xc, means, var, s_bounds=(0.01, 2.0)):
    """Least squares weighted by the bins' variances (README 4.5). Bins with no stars or no variance are
    left out (README 4.12 item 12). Converged = solver success and s not at a bound."""
    xc = np.asarray(xc, float)
    ok = np.isfinite(means) & np.isfinite(var) & (var > 0)
    if ok.sum() < 5:
        return {"converged": False, "reason": "fewer than 5 usable bins", "s": None, "width": None}
    x, y, w = xc[ok], means[ok], 1.0 / np.sqrt(var[ok])
    lo_s, hi_s = s_bounds
    x0 = [float(y[:2].mean()), float(y[-2:].mean()), -1.2, 0.1]
    r = least_squares(lambda p: (logistic(x, *p) - y) * w, x0,
                      bounds=([-np.inf, -np.inf, -np.inf, lo_s], [np.inf, np.inf, np.inf, hi_s]))
    s = float(r.x[3])
    at_b = s <= lo_s * 1.001 or s >= hi_s * 0.999
    return {"converged": bool(r.success) and not at_b, "at_bound": at_b, "s": s,
            "width": LN9x2 * abs(s), "params": [float(v) for v in r.x]}


class T3Sample:
    """J_phi/J_tot and [M/H] of one T3 sample, restricted to [M/H] < -0.5 for the bootstrap."""

    def __init__(self, mh, f, centers, width):
        mh = np.asarray(mh, float)
        f = np.asarray(f, float)
        ok = np.isfinite(mh) & np.isfinite(f)
        self.n_total = int(ok.sum())
        self.centers = list(centers)
        self.width = width
        hi = centers[-1] + width / 2
        sub = ok & (mh < hi)
        self.mh = mh[sub]
        self.f = f[sub]
        self.j = bin_index(self.mh, centers, width)
        self.in_a = self.mh < -2.0
        self.in_b = (self.mh > -1.1) & (self.mh < -0.9)

    def stats(self, idx=None):
        j = self.j if idx is None else self.j[idx]
        f = self.f if idx is None else self.f[idx]
        a = self.in_a if idx is None else self.in_a[idx]
        b = self.in_b if idx is None else self.in_b[idx]
        means, n = bin_means(j, f, len(self.centers))
        return (float(f[a].mean()) if a.any() else np.nan, float(f[b].mean()) if b.any() else np.nan,
                means, n)


def label_a(iv, delta=0.05):
    lo, hi = iv
    if lo is None or not np.isfinite(lo):
        return "undetermined"
    if lo >= -delta and hi <= delta:
        return "no net rotation"
    if lo > 0:
        return "net rotation"
    if hi < 0:
        return "net counter-rotation"
    return "undetermined"


def label_b(iv, thr=0.5):
    lo, hi = iv
    if lo is None or not np.isfinite(lo):
        return "undetermined"
    if lo > thr:
        return "rotation dominated"
    if hi < thr:
        return "not rotation dominated"
    return "undetermined"


def label_c(fit_ok, iv, w0, sharp_add=0.1, gradual_min=0.4):
    if not fit_ok:
        return "undetermined (fit failed)"
    lo, hi = iv
    if lo is None or w0 is None or not np.isfinite(w0):
        return "undetermined"
    if hi < w0 + sharp_add:
        return "sharp"
    if lo > max(gradual_min, w0 + sharp_add):
        return "gradual"
    return "undetermined"


def boot_variances(sample, rng, n_boot):
    ms = np.empty((n_boot, len(sample.centers)))
    for i in range(n_boot):
        ms[i] = sample.stats(boot_subset(rng, sample.n_total, sample.mh.size))[2]
    with np.errstate(invalid="ignore"):
        return np.nanvar(ms, axis=0, ddof=1)


def t3_ab(sample, rng, n_boot, delta=0.05):
    """(a) and (b) labels only (used by T4)."""
    a = np.empty(n_boot)
    b = np.empty(n_boot)
    for i in range(n_boot):
        a[i], b[i], _, _ = sample.stats(boot_subset(rng, sample.n_total, sample.mh.size))
    iva, ivb = S.pct_interval(a), S.pct_interval(b)
    return {"a_interval": iva, "b_interval": ivb, "a_label": label_a(iva, delta), "b_label": label_b(ivb)}


def t3_full(sample, rng, n_boot1, n_boot2, w0, delta=0.05):
    """README 4.5: point estimates, pass 1 (variances), pass 2 (labelled intervals, (c) refitted)."""
    pa, pb, means, n = sample.stats()
    var = boot_variances(sample, rng, n_boot1)
    xc = np.array(sample.centers)
    fit = fit_logistic(xc, means, var)
    a = np.empty(n_boot2)
    b = np.empty(n_boot2)
    w = np.empty(n_boot2)
    n_bound = 0
    for i in range(n_boot2):
        a[i], b[i], m, _ = sample.stats(boot_subset(rng, sample.n_total, sample.mh.size))
        fb = fit_logistic(xc, m, var)
        if fb["s"] is None:
            w[i] = np.nan
        else:
            w[i] = fb["width"]
            n_bound += int(not fb["converged"])
    iva, ivb, ivc = S.pct_interval(a), S.pct_interval(b), S.pct_interval(w)
    return {"n_stars": sample.n_total, "a_mean": pa, "b_mean": pb, "a_interval": iva, "b_interval": ivb,
            "a_label": label_a(iva, delta), "b_label": label_b(ivb),
            "bins": {"centers": sample.centers, "means": means.tolist(), "n": n.tolist(),
                     "boot_var": var.tolist()},
            "logistic": fit, "width_interval": ivc, "boot_fits_at_bound_or_failed": n_bound,
            "c_label": label_c(fit["converged"], ivc, w0), "w0": w0}


def w0_mocks(mh, f, rng, *, n_mocks, err, centers, width, n_boot, step=-1.0, hi_val=0.8):
    """README 4.5 known-answer width: true step 0 -> 0.8 at [M/H] = -1.0 with the data's per-bin scatter,
    observed [M/H] blurred by N(0, err) (err a scalar or per-star array); binned and fitted as the data."""
    mh = np.asarray(mh, float)
    f = np.asarray(f, float)
    ok = np.isfinite(mh) & np.isfinite(f)
    mh, f = mh[ok], f[ok]
    err = np.broadcast_to(np.asarray(err, float), mh.shape) if np.ndim(err) == 0 else np.asarray(err, float)[ok]
    cs = np.asarray(centers, float)
    jj = bin_index(mh, cs, width)
    sd = np.array([np.std(f[jj == k], ddof=1) if np.sum(jj == k) > 1 else np.nan for k in range(len(cs))])
    filled = np.nonzero(np.isfinite(sd))[0]
    nearest = filled[np.abs(np.arange(len(cs))[:, None] - filled[None, :]).argmin(axis=1)]
    sd = sd[nearest]
    jn = np.clip(np.floor((mh - (cs[0] - width / 2)) / width).astype(int), 0, len(cs) - 1)  # nearest bin
    sig = sd[jn]
    widths, fails = [], 0
    truth = np.where(mh < step, 0.0, hi_val)
    for _ in range(n_mocks):
        fm = truth + rng.normal(0.0, 1.0, mh.size) * sig
        mo = mh + rng.normal(0.0, 1.0, mh.size) * err
        smp = T3Sample(mo, fm, centers, width)
        m = smp.stats()[2]
        var = boot_variances(smp, rng, n_boot)
        fit = fit_logistic(cs, m, var)
        if fit["s"] is None or not fit["converged"]:
            fails += 1
        widths.append(np.nan if fit["s"] is None else fit["width"])
    widths = np.array(widths)
    return {"w0": float(np.nanmedian(widths)), "n_mocks": n_mocks, "fits_failed_or_at_bound": fails,
            "width_p16_p84": [float(np.nanpercentile(widths, 16)), float(np.nanpercentile(widths, 84))]}


# ---------------------------------------------------------------------------------------------
# v_phi (reported only, README 4.5)

def vphi_from_file(df):
    if "vphi" in df:
        return df["vphi"].to_numpy(float)
    if all(c in df for c in ("x", "y", "vx", "vy")):
        x, y = df["x"].to_numpy(float), df["y"].to_numpy(float)
        with np.errstate(invalid="ignore", divide="ignore"):
            return (x * df["vy"].to_numpy(float) - y * df["vx"].to_numpy(float)) / np.hypot(x, y)
    return None


def vphi_heliocentric(df, R0, zp=0.02, vsun=(11.1, 245.0, 7.3)):
    """v_phi recomputed from heliocentric observables with astropy (z_sun = 0); None if absent."""
    need = ("ra", "dec", "parallax", "pmra", "pmdec", "rv")
    if not all(c in df for c in need):
        return None
    import astropy.units as u
    from astropy.coordinates import CartesianDifferential, Galactocentric, SkyCoord
    plx = df["parallax"].to_numpy(float) + zp
    c = SkyCoord(ra=df["ra"].to_numpy(float) * u.deg, dec=df["dec"].to_numpy(float) * u.deg,
                 distance=(1.0 / plx) * u.kpc, pm_ra_cosdec=df["pmra"].to_numpy(float) * u.mas / u.yr,
                 pm_dec=df["pmdec"].to_numpy(float) * u.mas / u.yr,
                 radial_velocity=df["rv"].to_numpy(float) * u.km / u.s)
    g = c.transform_to(Galactocentric(galcen_distance=R0 * u.kpc, z_sun=0 * u.pc,
                                      galcen_v_sun=CartesianDifferential(list(vsun) * u.km / u.s)))
    x, y = g.x.to_value(u.kpc), g.y.to_value(u.kpc)
    vx, vy = g.v_x.to_value(u.km / u.s), g.v_y.to_value(u.km / u.s)
    return -(x * vy - y * vx) / np.hypot(x, y)   # astropy frame: rotation is negative L_z


def signed_like_disc(v, metal_rich_mask):
    """Sign convention: the median of the [M/H] > -0.5 stars is positive (as L5 for J_phi)."""
    if v is None:
        return None
    med = np.nanmedian(v[metal_rich_mask]) if metal_rich_mask.any() else np.nan
    return -v if np.isfinite(med) and med < 0 else v


# ---------------------------------------------------------------------------------------------
# T5

def t5_fractions(ecc, rapo, rng, n_boot, e_min=0.75, r_gse=10.0, r_a5=5.0):
    ecc = np.asarray(ecc, float)
    rapo = np.asarray(rapo, float)
    ok = np.isfinite(ecc) & np.isfinite(rapo)
    gse = ((ecc >= e_min) & (rapo >= r_gse))[ok]
    a5 = (rapo < r_a5)[ok]
    n = gse.size
    if n == 0:
        return {"n": 0, "g_label": "undetermined", "a5_label": "undetermined"}
    gb = np.empty(n_boot)
    ab = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, n, n)
        gb[i] = gse[idx].mean()
        ab[i] = a5[idx].mean()
    ivg, iva = S.pct_interval(gb), S.pct_interval(ab)
    return {"n": int(n), "g": float(gse.mean()), "g_interval": ivg, "g_label": S.label_g(ivg),
            "a5": float(a5.mean()), "a5_interval": iva, "a5_label": S.label_a5(iva)}
