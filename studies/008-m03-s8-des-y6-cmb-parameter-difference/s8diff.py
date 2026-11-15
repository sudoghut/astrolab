"""Chain parsing, summary statistics and the parameter-difference estimator (README sections 2, 4).

Pure functions; tunable values are passed in as arguments (AGENTS.md section 2).
"""
import re

import numpy as np
from scipy import ndimage, special, stats

NESTED = ("nautilus", "multinest", "polychord", "importance", "flow", "nested")
MCMC = ("metropolis", "emcee", "mcmc")
POSITIONAL = {"omega_m": 0, "sigma_8": -7, "log_weight": -3}   # read_chains_y6.py, Nautilus chains


# ------------------------------------------------------------------ chains ----

def _key(name):
    return name.split("--")[-1].lower()


def _match(names, options):
    hits = [i for i, n in enumerate(names) if _key(n) in options]
    return hits


def read_format(path, max_comment_lines=20000):
    """Step A: comment lines, header, column count and data row count; no statistics."""
    comments, header, ncols, nrows, first, ragged, n_comments = [], None, None, 0, [], 0, 0
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            s = line.strip()
            if not s:
                continue
            if s.startswith("#"):
                n_comments += 1
                if len(comments) < max_comment_lines:
                    comments.append(s)
                continue
            n = len(s.split())
            if ncols is None:
                ncols = n
            elif n != ncols:
                ragged += 1
            nrows += 1
            if len(first) < 10:
                first.append(s)
    for c in comments:
        if c.startswith("#") and not c.startswith("##"):
            fields = c[1:].split()
            if ncols is not None and len(fields) == ncols:
                header = fields
                break
    sampler, sampler_line = None, None
    for pattern in (r"#\s*sampler\s*=\s*(\S+)", r"##+\s*sampler\s*=\s*(\S+)"):
        for c in comments:
            if pattern.startswith("#\\s") and c.startswith("##"):
                continue
            m = re.match(pattern, c, re.I)
            if m:
                sampler, sampler_line = m.group(1).lower(), c
                break
        if sampler:
            break
    double = [c for c in comments if c.startswith("##")]
    return {"ncols": ncols, "nrows": nrows, "ragged_rows": ragged, "header": header, "sampler": sampler,
            "sampler_line": sampler_line, "n_comment_lines": n_comments,
            "comment_lines_truncated": n_comments > len(comments), "comment_lines": comments,
            "prior_lines": double, "first_rows": first}


def column_map(fmt, name, positional_ok):
    """README section 2.0 column rules. Returns (map, status)."""
    header = fmt["header"]
    if header is None:
        if not positional_ok:
            return None, "not mapped (no header)"
        return {"omega_m": POSITIONAL["omega_m"] % fmt["ncols"], "sigma_8": POSITIONAL["sigma_8"] % fmt["ncols"],
                "s_8": None, "weight": None, "log_weight": POSITIONAL["log_weight"] % fmt["ncols"],
                "source": "positional (read_chains_y6.py)"}, "mapped"
    om = _match(header, {"omega_m", "omegam"})
    s8g = _match(header, {"sigma_8", "sigma8"})
    s8 = _match(header, {"s_8", "s8"})
    w = _match(header, {"weight"})
    lw = _match(header, {"log_weight"})
    if len(om) != 1 or len(s8g) != 1:
        return None, f"not mapped (omega_m matches {len(om)}, sigma_8 matches {len(s8g)})"
    if len(s8) > 1 or len(w) > 1 or len(lw) > 1:
        return None, "not mapped (ambiguous S8 or weight columns)"
    cmap = {"omega_m": om[0], "sigma_8": s8g[0], "s_8": s8[0] if s8 else None,
            "weight": w[0] if w else None, "log_weight": None if w else (lw[0] if lw else None),
            "source": "header"}
    return cmap, "mapped"


def burn_in_fraction(sampler, mcmc_burn):
    if sampler is None:
        return 0.0, "no sampler line"
    if any(k in sampler for k in NESTED):
        return 0.0, "nested or importance"
    if any(k in sampler for k in MCMC):
        return mcmc_burn, "mcmc"
    return 0.0, "unrecognised sampler"


def load_chain(path, cmap, burn):
    """Load the chain, apply burn-in, drop bad rows, derive S8."""
    data = np.loadtxt(path, comments="#", ndmin=2)
    n0 = data.shape[0]
    data = data[int(np.floor(burn * n0)):]
    nonfinite_any = int(np.sum(~np.all(np.isfinite(data), axis=1)))
    om, sg = data[:, cmap["omega_m"]], data[:, cmap["sigma_8"]]
    if cmap["weight"] is not None:
        w = data[:, cmap["weight"]].astype(float)
    elif cmap["log_weight"] is not None:
        lw = data[:, cmap["log_weight"]]
        w = np.exp(lw - np.nanmax(lw[np.isfinite(lw)]))
    else:
        w = np.ones(len(data))
    used = np.column_stack([om, sg, w])
    finite = np.all(np.isfinite(used), axis=1)
    good = finite & (w > 0)
    s8 = sg * np.sqrt(om / 0.3)
    stored_ok = None
    if cmap.get("s_8") is not None:
        stored = data[:, cmap["s_8"]]
        stored_ok = bool(np.all(np.abs(stored[good] - s8[good]) < 1e-4))
    out = {"omega_m": om[good], "sigma_8": sg[good], "s8": s8[good], "w": w[good] / w[good].sum(),
           "data": data[good]}
    info = {"rows_read": n0, "rows_after_burn": int(len(data)), "nonfinite_any_column": nonfinite_any,
            "nonfinite_used_columns": int(np.sum(~finite)), "zero_weight": int(np.sum(finite & ~(w > 0))),
            "stored_s8_consistent": stored_ok,
            "ess": float(1.0 / np.sum(out["w"] ** 2))}
    return out, info


# -------------------------------------------------------------- summaries ----

def wmean(x, w):
    return float(np.sum(w * x) / np.sum(w))


def wstd(x, w):
    m = wmean(x, w)
    return float(np.sqrt(np.sum(w * (x - m) ** 2) / np.sum(w)))


def wquantile(x, w, q):
    o = np.argsort(x)
    cw = np.cumsum(w[o]) / np.sum(w)
    return np.interp(q, cw, x[o])


def wkde_grid(x, w, n_grid, qlo=1e-4, qhi=1 - 1e-4, bw_factor=1.0):
    """Weighted Gaussian KDE on a grid between weighted quantiles (Scott with the ESS)."""
    ess = 1.0 / np.sum((w / w.sum()) ** 2)
    sd = wstd(x, w)
    h = bw_factor * sd * ess ** (-1.0 / 5.0)
    lo, hi = wquantile(x, w, [qlo, qhi])
    grid = np.linspace(lo, hi, n_grid)
    hist, edges = np.histogram(x, bins=np.linspace(lo - 5 * h, hi + 5 * h, 8 * n_grid + 1), weights=w)
    dx = edges[1] - edges[0]
    dens = ndimage.gaussian_filter1d(hist.astype(float), h / dx, mode="constant")
    centres = 0.5 * (edges[1:] + edges[:-1])
    dens = np.interp(grid, centres, dens)
    dens /= np.trapezoid(dens, grid) if hasattr(np, "trapezoid") else np.trapz(dens, grid)
    return grid, dens, h


def interval_around_mean(x, w, mass, n_grid):
    """Shortest interval containing the weighted mean and `mass` of a weighted KDE; and equal-tail."""
    grid, dens, _ = wkde_grid(x, w, n_grid)
    m = wmean(x, w)
    cdf = np.concatenate([[0.0], np.cumsum(0.5 * (dens[1:] + dens[:-1]) * np.diff(grid))])
    cdf /= cdf[-1]
    best = None
    for i in range(len(grid)):
        if grid[i] > m:
            break
        target = cdf[i] + mass
        if target > 1:
            break
        j = int(np.searchsorted(cdf, target))
        if j >= len(grid) or grid[j] < m:
            continue
        width = grid[j] - grid[i]
        if best is None or width < best[0]:
            best = (width, grid[i], grid[j])
    c_m = np.interp(m, grid, cdf)
    eq = (float(np.interp(max(c_m - mass / 2, 0), cdf, grid)), float(np.interp(min(c_m + mass / 2, 1), cdf, grid)))
    mode = float(grid[np.argmax(dens)])
    return {"mean": m, "lo": float(best[1]), "hi": float(best[2]), "equal_lo": eq[0], "equal_hi": eq[1],
            "kde_mode": mode}


# ------------------------------------------------------------- estimator ----

def nsigma_binned(dp, bw_factor=1.0, n_grid_1d=8000, n_grid_2d=1024, q=1e-6):
    """Parameter-difference n_sigma (D26 eqs. 17-19) from equally weighted samples of P(dp).

    dp: array (N, d) with d = 1 or 2. Binned Gaussian KDE in whitened coordinates (README section 4).
    """
    dp = np.asarray(dp, dtype=float)
    if dp.ndim == 1:
        dp = dp[:, None]
    n, d = dp.shape
    mu = dp.mean(0)
    cov = np.atleast_2d(np.cov(dp.T))
    L = np.linalg.cholesky(np.linalg.inv(cov))
    z = (dp - mu) @ L
    z0 = (np.zeros(d) - mu) @ L
    h = bw_factor * n ** (-1.0 / (d + 4))
    ngrid = n_grid_1d if d == 1 else n_grid_2d
    lo = np.minimum(np.quantile(z, q, axis=0), z0) - 5 * h
    hi = np.maximum(np.quantile(z, 1 - q, axis=0), z0) + 5 * h
    edges = [np.linspace(lo[k], hi[k], ngrid + 1) for k in range(d)]
    H, _ = np.histogramdd(z, bins=edges)
    outside = int(n - H.sum())
    dx = np.array([(hi[k] - lo[k]) / ngrid for k in range(d)])
    dens = ndimage.gaussian_filter(H, sigma=list(h / dx), mode="constant")
    coords = [[(z0[k] - lo[k]) / dx[k] - 0.5] for k in range(d)]
    d0 = float(ndimage.map_coordinates(dens, coords, order=1)[0])
    frac = float(H[dens > d0].sum() / n)
    lower_bound = frac >= 1.0
    if lower_bound:
        frac = 1.0 - 1.0 / n
    ratio = float(np.max(dx) / h)
    return {"n_sigma": float(np.sqrt(2) * special.erfinv(frac)), "delta": frac, "lower_bound": lower_bound,
            "outside_grid": outside, "cell_over_h": ratio, "cell_flag": ratio > 1 / 3, "h": float(h)}


def draw_pairs(a, wa, b, wb, n, rng):
    """Independent weighted draws with replacement; returns a - b samples (rows of a, b are parameter vectors)."""
    ia = rng.choice(len(wa), size=n, replace=True, p=wa / wa.sum())
    ib = rng.choice(len(wb), size=n, replace=True, p=wb / wb.sum())
    return a[ia] - b[ib]


def parameter_difference(a, wa, b, wb, n, seeds, bw_factor=1.0):
    vals, extra = [], []
    for seed in seeds:
        rng = np.random.default_rng(seed)
        r = nsigma_binned(draw_pairs(a, wa, b, wb, n, rng), bw_factor=bw_factor)
        vals.append(r["n_sigma"])
        extra.append({k: r[k] for k in ("lower_bound", "outside_grid", "cell_over_h", "cell_flag")})
    return {"n_sigma": float(np.mean(vals)), "s": float(np.std(vals, ddof=1)), "per_seed": vals,
            "diagnostics": extra, "cell_flag": any(e["cell_flag"] for e in extra)}


def equal_tail(dp):
    dp = np.asarray(dp, dtype=float).ravel()
    med = np.median(dp)
    p = float(np.mean(dp <= 0)) if med > 0 else float(np.mean(dp >= 0))
    delta = 1 - 2 * p
    return {"p_far_side": p, "n_sigma": float(np.sqrt(2) * special.erfinv(max(delta, 0.0)))}


def convolution_check(xa, wa, xb, wb, spacing):
    """1-D cross-check: P(dp) by convolving the two weighted KDEs on a common grid."""
    def kde(x, w, grid):
        ess = 1.0 / np.sum((w / w.sum()) ** 2)
        h = wstd(x, w) * ess ** (-1.0 / 5.0)
        hist, edges = np.histogram(x, bins=np.append(grid - spacing / 2, grid[-1] + spacing / 2), weights=w)
        return ndimage.gaussian_filter1d(hist.astype(float), h / spacing, mode="constant")

    lo = min(wquantile(xa, wa, 1e-4), wquantile(xb, wb, 1e-4))
    hi = max(wquantile(xa, wa, 1 - 1e-4), wquantile(xb, wb, 1 - 1e-4))
    grid = np.arange(lo, hi + spacing, spacing)
    pa, pb = kde(xa, wa, grid), kde(xb, wb, grid)
    pdiff = np.convolve(pa, pb[::-1], mode="full")
    dgrid = (np.arange(len(pdiff)) - (len(grid) - 1)) * spacing
    pdiff /= pdiff.sum()
    d0 = float(np.interp(0.0, dgrid, pdiff))
    frac = float(pdiff[pdiff > d0].sum())
    return {"n_sigma": float(np.sqrt(2) * special.erfinv(min(frac, 1 - 1e-12))), "delta": frac}


def gaussian_estimate(ma, sa, mb, sb):
    return float(abs(ma - mb) / np.hypot(sa, sb))


def split_normal_draws(mean, sig_plus, sig_minus, n, rng):
    """Split normal whose mean equals `mean` (location shifted from the mode)."""
    mode = mean - np.sqrt(2 / np.pi) * (sig_plus - sig_minus)
    u = rng.uniform(size=n)
    p_minus = sig_minus / (sig_minus + sig_plus)
    z = np.abs(rng.standard_normal(n))
    return np.where(u < p_minus, mode - sig_minus * z, mode + sig_plus * z)


def full_space_gaussian(xa, wa, xb, wb, max_cond):
    """Gaussian parameter difference over columns of xa, xb (same order)."""
    ma = np.average(xa, axis=0, weights=wa)
    mb = np.average(xb, axis=0, weights=wb)
    ca = np.atleast_2d(np.cov(xa.T, aweights=wa))
    cb = np.atleast_2d(np.cov(xb.T, aweights=wb))
    c = ca + cb
    cond = float(np.linalg.cond(c))
    if cond > max_cond:
        return {"status": f"condition number {cond:.3g} > {max_cond:.0e}"}
    d = ma - mb
    chi2 = float(d @ np.linalg.solve(c, d))
    k = len(d)
    p_inside = float(stats.chi2.cdf(chi2, k))
    return {"status": "ok", "k": k, "chi2": chi2, "condition": cond,
            "n_sigma": float(np.sqrt(2) * special.erfinv(min(p_inside, 1 - 1e-15)))}
