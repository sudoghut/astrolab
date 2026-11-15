"""Pure helpers for study 004 (wide binaries; pre-registration: README sections 1-4).

No data access here: run.py fetches through ctx.tap and passes arrays in. Every function takes its
parameters as arguments (AGENTS.md section 2: no `import run`, no module-level use of PARAMS).
"""
from __future__ import annotations

import math

import numpy as np

KAPPA = 4.740470464          # km/s per (mas/yr * kpc); v = KAPPA * mu[mas/yr] / parallax[mas]
G_SI = 6.674e-11
AU_M = 1.495978707e11
MSUN_KG = 1.98892e30
PC_AU = 206264.806


# ---------------------------------------------------------------- sky strips
def strip_plan(margin_ra_low=7.2, margin_ra_mid=30.0, margin_dec=3.3, ra_step_low=5.0,
               dec_bands_low=(-60.0, -30.0, 0.0, 30.0, 60.0), ra_step_mid=15.0):
    """Star-a regions (half-open, partitioning the sphere) with the star-b search box.

    |dec| <= 60: RA steps of ra_step_low within the given declination bands; 60-80: RA steps of
    ra_step_mid; caps |dec| > 80: one region each. Star b: the region plus margin_dec in declination
    and margin_ra_* in RA (all RA for caps). Returns a list of dicts: ra0, ra1, dec0, dec1 (star a)
    and bra0, bra1, bdec0, bdec1 (star b; bra0 > bra1 means the RA interval wraps through 0).
    """
    out = []
    nlow = int(round(360.0 / ra_step_low))
    for lo, hi in zip(dec_bands_low[:-1], dec_bands_low[1:]):
        for i in range(nlow):
            ra0, ra1 = ra_step_low * i, ra_step_low * (i + 1)
            out.append(dict(ra0=ra0, ra1=ra1, dec0=lo, dec1=hi,
                            bra0=(ra0 - margin_ra_low) % 360, bra1=(ra1 + margin_ra_low) % 360,
                            bdec0=lo - margin_dec, bdec1=hi + margin_dec))
    nmid = int(round(360.0 / ra_step_mid))
    for sgn in (1, -1):
        lo, hi = (60.0, 80.0) if sgn > 0 else (-80.0, -60.0)
        for i in range(nmid):
            ra0, ra1 = ra_step_mid * i, ra_step_mid * (i + 1)
            out.append(dict(ra0=ra0, ra1=ra1, dec0=lo, dec1=hi,
                            bra0=(ra0 - margin_ra_mid) % 360, bra1=(ra1 + margin_ra_mid) % 360,
                            bdec0=lo - margin_dec, bdec1=hi + margin_dec))
        cap = (80.0, 90.0) if sgn > 0 else (-90.0, -80.0)
        out.append(dict(ra0=0.0, ra1=360.0, dec0=cap[0], dec1=cap[1], bra0=0.0, bra1=360.0,
                        bdec0=cap[0] - margin_dec if sgn > 0 else -90.0,
                        bdec1=90.0 if sgn > 0 else cap[1] + margin_dec))
    return out


def split_region(r):
    """Split a star-a region in two along right ascension, keeping its star-b margins (README
    section 3: a region over the row cap is split and counted again)."""
    full_b = r["bra0"] == 0.0 and r["bra1"] == 360.0
    margin = 0.0 if full_b else (r["ra0"] - r["bra0"]) % 360.0
    mid = 0.5 * (r["ra0"] + r["ra1"])
    out = []
    for lo, hi in ((r["ra0"], mid), (mid, r["ra1"])):
        d = dict(r, ra0=lo, ra1=hi)
        if not full_b:
            d["bra0"], d["bra1"] = (lo - margin) % 360, (hi + margin) % 360
        out.append(d)
    return out


def ra_in(ra, lo, hi):
    """RA interval test with wrap-around (lo > hi means the interval crosses 0); [0, 360] is all."""
    ra = np.asarray(ra) % 360.0
    if lo == 0.0 and hi == 360.0:
        return np.ones_like(ra, dtype=bool)
    if lo <= hi:
        return (ra >= lo) & (ra <= hi)
    return (ra >= lo) | (ra <= hi)


def search_radius_deg(parallax_mas, radius_au=0.5 * PC_AU):
    """Angular radius (deg) of a projected radius (AU) at parallax (mas): 1 AU at 1 pc is 1 arcsec."""
    return np.asarray(radius_au) * np.asarray(parallax_mas) / 1000.0 / 3600.0


def in_region(ra, dec, r):
    """Half-open membership of star a: ra0 <= ra < ra1 and dec0 <= dec < dec1 (dec = 90 belongs to the
    north cap), so the regions partition the sphere."""
    ra = np.asarray(ra) % 360.0
    dec = np.asarray(dec)
    in_ra = (ra >= r["ra0"]) & (ra < r["ra1"])
    hi_ok = (dec < r["dec1"]) | ((r["dec1"] == 90.0) & (dec == 90.0))
    return in_ra & (dec >= r["dec0"]) & hi_ok


def region_of(ra, dec, plan):
    """Indices of the star-a regions containing (ra, dec); exactly one for every point."""
    return [k for k, r in enumerate(plan) if bool(in_region(ra, dec, r))]


def canonical_pairs(id_a, id_b):
    """Order each pair as (min, max) and drop duplicates; returns index array of kept rows."""
    a = np.minimum(id_a, id_b)
    b = np.maximum(id_a, id_b)
    seen = {}
    keep = []
    for i, (x, y) in enumerate(zip(a.tolist(), b.tolist())):
        if (x, y) not in seen:
            seen[(x, y)] = i
            keep.append(i)
    return np.array(keep, dtype=int)


# ---------------------------------------------------------------- MOND
def mls_nu(gn, a0):
    y = np.sqrt(np.asarray(gn, float) / a0)
    return 1.0 / (-np.expm1(-y))


def mls_k(gn, a0):
    """K = dln nu / dln g_N for the MLS function: -(y/2) e^-y / (1 - e^-y), y = sqrt(g_N / a0)."""
    y = np.sqrt(np.asarray(gn, float) / a0)
    return -(y / 2.0) * np.exp(-y) / (-np.expm1(-y))


def mond_boost(x, a0=1.2e-10, gne_over_a0=1.184):
    """C26 Eq. 7 velocity boost at x = r_sky / r_M (3D r = r_sky sqrt(3/2))."""
    x = np.asarray(x, float)
    gne = gne_over_a0 * a0
    gni = a0 / (1.5 * x ** 2)
    gnt = np.sqrt(gni ** 2 + gne ** 2)
    nu = mls_nu(gnt, a0)
    k = mls_k(gnt, a0)
    return np.sqrt(nu * (1.0 + (k / 3.0) * np.tanh(0.825 * gne / gni) ** 3.7))


# ---------------------------------------------------------------- stars and pairs
def mass_from_mg(mg, mg_sun=4.67, slope=0.0725, low=0.7, add=0.05):
    m = 10.0 ** (slope * (mg_sun - np.asarray(mg, float)))
    return np.where(m < low, m + add, m)


def weighted_parallax(p1, e1, p2, e2):
    """C24 Eq. A2 and its derivatives w.r.t. p1, p2 (A9, A10)."""
    w = e1 ** 2 + e2 ** 2
    pbar = (e2 ** 2 * p1 + e1 ** 2 * p2) / w
    return pbar, e2 ** 2 / w, e1 ** 2 / w


def sky_separation_au(ra1, dec1, ra2, dec2, pbar_mas):
    """Projected separation r_sky (AU) at the common distance, exact great-circle angle."""
    r1, d1, r2, d2 = map(np.radians, (ra1, dec1, ra2, dec2))
    c = np.sin(d1) * np.sin(d2) + np.cos(d1) * np.cos(d2) * np.cos(r1 - r2)
    theta = np.arccos(np.clip(c, -1.0, 1.0))
    dist_pc = 1000.0 / np.asarray(pbar_mas)
    return theta * dist_pc * PC_AU


def perspective_vsky(ra1, dec1, pmra1, pmdec1, ra2, dec2, pmra2, pmdec2, pbar, rv1, correct=True):
    """Relative sky-plane velocity (km/s) of star 2 w.r.t. star 1 at the common parallax pbar.

    With `correct`, the systemic 3D velocity of star 1 (from its proper motion, pbar and RV rv1) is
    projected onto star 2's sky plane and subtracted, removing the apparent relative motion caused
    by viewing one space velocity from two directions (perspective effect; C24 Eqs. 2-8). Returns
    (v_ra, v_dec) along star 2's local east and north.
    """
    a1, d1, a2, d2 = map(np.radians, (ra1, dec1, ra2, dec2))
    k = KAPPA / pbar
    # star-1 space velocity in equatorial Cartesian (km/s)
    e1 = np.stack([-np.sin(a1), np.cos(a1), np.zeros_like(a1)])
    n1 = np.stack([-np.sin(d1) * np.cos(a1), -np.sin(d1) * np.sin(a1), np.cos(d1)])
    r1 = np.stack([np.cos(d1) * np.cos(a1), np.cos(d1) * np.sin(a1), np.sin(d1)])
    v1 = k * pmra1 * e1 + k * pmdec1 * n1 + (rv1 if correct else 0.0) * r1
    e2 = np.stack([-np.sin(a2), np.cos(a2), np.zeros_like(a2)])
    n2 = np.stack([-np.sin(d2) * np.cos(a2), -np.sin(d2) * np.sin(a2), np.cos(d2)])
    if correct:
        exp_ra = (v1 * e2).sum(0)
        exp_dec = (v1 * n2).sum(0)
    else:
        exp_ra = k * pmra1
        exp_dec = k * pmdec1
    return k * pmra2 - exp_ra, k * pmdec2 - exp_dec


def vsky_sigma(pm1, pm2, p1, p2, e_p1, e_p2, e_pmra1, e_pmdec1, e_pmra2, e_pmdec2,
               c_ppa1, c_ppd1, c_pad1, c_ppa2, c_ppd2, c_pad2):
    """Jacobian propagation (C24 App. A) of v_sky = KAPPA/pbar * |mu2 - mu1| (perspective term's
    error neglected). pm1, pm2: (pmra, pmdec) tuples. Returns sigma(v_sky) in km/s."""
    pbar, w1, w2 = weighted_parallax(p1, e_p1, p2, e_p2)
    dra = pm2[0] - pm1[0]
    ddec = pm2[1] - pm1[1]
    vra = KAPPA / pbar * dra
    vdec = KAPPA / pbar * ddec
    v = np.hypot(vra, vdec)
    v = np.where(v > 0, v, 1e-12)
    # derivatives of v w.r.t. (p1, pmra1, pmdec1, p2, pmra2, pmdec2)
    dv_dvra = vra / v
    dv_dvdec = vdec / v
    dpbar = (-v / pbar)
    J = [dpbar * w1, -KAPPA / pbar * dv_dvra, -KAPPA / pbar * dv_dvdec,
         dpbar * w2, KAPPA / pbar * dv_dvra, KAPPA / pbar * dv_dvdec]
    var = 0.0
    for (jp, ja, jd, ep, ea, ed, cpa, cpd, cad) in [
            (J[0], J[1], J[2], e_p1, e_pmra1, e_pmdec1, c_ppa1, c_ppd1, c_pad1),
            (J[3], J[4], J[5], e_p2, e_pmra2, e_pmdec2, c_ppa2, c_ppd2, c_pad2)]:
        var = var + (jp * ep) ** 2 + (ja * ea) ** 2 + (jd * ed) ** 2 \
            + 2 * jp * ja * cpa * ep * ea + 2 * jp * jd * cpd * ep * ed + 2 * ja * jd * cad * ea * ed
    return np.sqrt(var)


def vsky_corrected_sigma(ra1, dec1, ra2, dec2, rv1, star1, star2, rel_step=1e-4):
    """sigma(v_sky) of the perspective-corrected relative velocity (README section 4.4).

    star1, star2: dicts with p, pmra, pmdec, e_p, e_pmra, e_pmdec, c_ppa, c_ppd, c_pad (scalars).
    The Jacobian of |v_sky| with respect to each star's (parallax, pmra, pmdec) is taken by central
    finite differences of the full corrected expression (common parallax and perspective term
    included); each star's 3x3 covariance comes from its errors and correlations; stars independent;
    positions and RV are treated as exact. Returns (v_sky, sigma).
    """
    def vsky(x):
        p1, a1, d1, p2, a2, d2 = x
        pbar, _, _ = weighted_parallax(p1, star1["e_p"], p2, star2["e_p"])
        vr, vd = perspective_vsky(ra1, dec1, a1, d1, ra2, dec2, a2, d2, pbar, rv1, correct=True)
        return float(np.hypot(vr, vd))

    x0 = np.array([star1["p"], star1["pmra"], star1["pmdec"], star2["p"], star2["pmra"], star2["pmdec"]], float)
    J = np.zeros(6)
    for k in range(6):
        h = rel_step * max(abs(x0[k]), 1e-3)
        xp, xm = x0.copy(), x0.copy()
        xp[k] += h
        xm[k] -= h
        J[k] = (vsky(xp) - vsky(xm)) / (2 * h)

    def cov3(s):
        e = np.array([s["e_p"], s["e_pmra"], s["e_pmdec"]], float)
        c = np.array([[1.0, s["c_ppa"], s["c_ppd"]], [s["c_ppa"], 1.0, s["c_pad"]], [s["c_ppd"], s["c_pad"], 1.0]])
        return c * np.outer(e, e)

    cov = np.zeros((6, 6))
    cov[:3, :3] = cov3(star1)
    cov[3:, 3:] = cov3(star2)
    return vsky(x0), float(np.sqrt(J @ cov @ J))


def vc_kms(mass_msun, r_au):
    """Newtonian circular speed sqrt(G M / r) in km/s."""
    return np.sqrt(G_SI * np.asarray(mass_msun) * MSUN_KG / (np.asarray(r_au) * AU_M)) / 1000.0


def r_mond_au(mass_msun, a0=1.2e-10):
    return np.sqrt(G_SI * np.asarray(mass_msun) * MSUN_KG / a0) / AU_M


# ---------------------------------------------------------------- statistics
def bin_index(x, edges):
    """edges: interior edges (increasing); returns bin number 0..len(edges)."""
    return np.searchsorted(np.asarray(edges), np.asarray(x), side="right")


def merge_outer(counts, min_count):
    """README section 2: merge the highest bin inward and the lowest bin upward until each end holds
    min_count. Returns (mapping old bin -> new bin index 0..n_final-1, evaluable); evaluable only if
    every final bin holds min_count and at least two bins remain."""
    counts = list(counts)
    n = len(counts)
    top = n - 1
    tot_top = counts[top]
    while tot_top < min_count and top > 0:
        top -= 1
        tot_top += counts[top]
    bot = 0
    tot_bot = counts[0]
    while tot_bot < min_count and bot < top - 1:
        bot += 1
        tot_bot += counts[bot]
    groups = []
    for b in range(n):
        g = 0 if b <= bot else (b - bot if b < top else top - bot)
        groups.append(g)
    finals = {}
    for b, g in enumerate(groups):
        finals[g] = finals.get(g, 0) + counts[b]
    evaluable = len(finals) >= 2 and all(v >= min_count for v in finals.values())
    return groups, evaluable


def bin_medians(vt, b, nbins):
    return np.array([np.median(vt[b == k]) if np.any(b == k) else np.nan for k in range(nbins)])


def bootstrap_cov(vt, b, nbins, n_boot, seed, min_count=15, max_redraw_frac=0.05):
    """Covariance of the bin medians over whole-sample bootstrap resamples (README section 2).

    A replicate with fewer than min_count pairs in any bin is redrawn. Returns (cov, redraw_fraction,
    valid) with valid False when more than max_redraw_frac of the draws were redrawn.
    """
    rng = np.random.default_rng(seed)
    n = len(vt)
    meds = []
    draws = 0
    while len(meds) < n_boot:
        draws += 1
        idx = rng.integers(0, n, n)
        bb = b[idx]
        if min(int(np.sum(bb == k)) for k in range(nbins)) < min_count:
            if draws > 50 * n_boot:
                break
            continue
        meds.append(bin_medians(vt[idx], bb, nbins))
    frac = 1.0 - len(meds) / draws
    meds = np.array(meds)
    cov = np.cov(meds, rowvar=False) if len(meds) > 1 else np.full((nbins, nbins), np.nan)
    return cov, frac, bool(frac <= max_redraw_frac and len(meds) == n_boot)


def mad_errors(vt, b, nbins, scale=1.0):
    out = []
    for k in range(nbins):
        v = vt[b == k]
        out.append(scale * np.median(np.abs(v - np.median(v))) / np.sqrt(len(v)))
    return np.array(out)


def gls_scale_fit(y, shape, cov, cond_max=1e8):
    """Fit y = A * shape with covariance cov; returns (A, chi2, used_diagonal, valid).

    An ill-conditioned or non-finite covariance falls back to its diagonal; the fit is invalid
    (A and chi2 NaN) unless the usable diagonal is finite and strictly positive (README section 2).
    """
    y = np.asarray(y, float)
    s = np.asarray(shape, float)
    cov = np.asarray(cov, float)
    diag = False
    if not np.all(np.isfinite(cov)) or np.linalg.cond(cov) > cond_max:
        cov = np.diag(np.diag(cov))
        diag = True
    d = np.diag(cov)
    if not (np.all(np.isfinite(d)) and np.all(d > 0) and np.all(np.isfinite(y))):
        return float("nan"), float("nan"), diag, False
    ci = np.linalg.inv(cov)
    A = float(s @ ci @ y / (s @ ci @ s))
    r = y - A * s
    return A, float(r @ ci @ r), diag, True


def compare_models(medians, x_bins, cov, a0=1.2e-10, gne_over_a0=1.184):
    """Newton (flat) vs MOND (A * b(x)); each with its own normalisation. Returns dict with 'valid'."""
    flat = np.ones_like(medians)
    shape = mond_boost(x_bins, a0, gne_over_a0)
    An, cn, dn, vn = gls_scale_fit(medians, flat, cov)
    Am, cm, dm, vm = gls_scale_fit(medians, shape, cov)
    valid = bool(vn and vm)
    d = cm - cn if valid else float("nan")
    return {"A_newton": An, "chi2_newton": cn, "A_mond": Am, "chi2_mond": cm, "dchi2": d,
            "ln_L": d / 2.0 if valid else float("nan"),
            "L": float(math.exp(min(d / 2.0, 700.0))) if valid else float("nan"),
            "used_diagonal": bool(dn or dm), "valid": valid}
