"""Factorised KDE free-spectrum likelihood and grid posteriors (README section 4).

Pure functions; every tunable value is passed in as an argument (AGENTS.md section 2).
The likelihood follows Lamb, Taylor & van Haasteren 2023 (arXiv:2303.15442, eq. 8-11) and
ceffyl's `Ceffyl.ln_likelihood` (bin lookup, below-grid clip, above-grid -inf, NaN -> -36).
"""
import io
import zipfile

import numpy as np

YEAR_S = 365.25 * 86400.0
F_YR = 1.0 / YEAR_S
NAN_LOGPDF = -36.0
MEMBERS = ("freqs.npy", "log10rhogrid.npy", "density.npy")
_trapz = getattr(np, "trapezoid", None) or np.trapz


class NotEvaluable(Exception):
    """A pre-registered structural or validity check failed (README section 2)."""


# ---------------------------------------------------------------- loading ----

def load_product(zip_path, dir_key, *, max_member_bytes, max_total_bytes, max_members):
    """Read the three arrays of the directory whose name contains `dir_key` from an untrusted zip."""
    with zipfile.ZipFile(zip_path) as zf:
        infos = zf.infolist()
        if len(infos) > max_members:
            raise NotEvaluable(f"archive lists {len(infos)} members > {max_members}")
        for info in infos:
            name = info.filename
            if ".." in name.split("/") or name.startswith("/") or "\\" in name:
                raise NotEvaluable(f"unsafe member name {name!r}")
        dirs = sorted({i.filename.rsplit("/", 1)[0] for i in infos
                       if "/" in i.filename and dir_key in i.filename.rsplit("/", 1)[0].split("/")[-1]})
        if len(dirs) != 1:
            raise NotEvaluable(f"expected exactly one directory containing {dir_key!r}, found {dirs}")
        d = dirs[0]
        total = 0
        arrays = {}
        for m in MEMBERS:
            name = f"{d}/{m}"
            try:
                with zf.open(name) as fh:
                    raw = fh.read(max_member_bytes + 1)
            except KeyError as e:
                raise NotEvaluable(f"member {name} missing") from e
            if len(raw) > max_member_bytes:
                raise NotEvaluable(f"member {name} larger than {max_member_bytes} bytes")
            total += len(raw)
            if total > max_total_bytes:
                raise NotEvaluable(f"members exceed {max_total_bytes} bytes in total")
            arrays[m] = np.load(io.BytesIO(raw), allow_pickle=False)
    return {"dir": d, "freqs": arrays["freqs.npy"], "grid": arrays["log10rhogrid.npy"],
            "density": arrays["density.npy"]}


def check_product(prod, *, n_freq_file, t_yr, freq_tol, grid_rtol):
    """Structural checks of README section 4 step 1; returns a normalised product."""
    freqs = np.asarray(prod["freqs"], dtype=float).ravel()
    grid = np.asarray(prod["grid"], dtype=float).ravel()
    dens = np.asarray(prod["density"], dtype=float)
    if freqs.size != n_freq_file:
        raise NotEvaluable(f"{freqs.size} frequencies, expected {n_freq_file}")
    if dens.ndim == 3 and dens.shape[0] == 1:
        dens = dens[0]
    if dens.ndim != 2 or dens.shape != (n_freq_file, grid.size):
        raise NotEvaluable(f"density shape {np.shape(prod['density'])} does not match "
                           f"({n_freq_file}, {grid.size})")
    if grid.size < 2:
        raise NotEvaluable("grid has fewer than 2 points")
    steps = np.diff(grid)
    db = steps.mean()
    if db <= 0 or np.max(np.abs(steps - db)) > grid_rtol * abs(db) + 1e-12:
        raise NotEvaluable("log10 rho grid is not uniform")
    t_s = 1.0 / freqs[0]
    if abs(freqs[0] * t_yr * YEAR_S - 1.0) > freq_tol:
        raise NotEvaluable(f"first frequency {freqs[0]:.4e} Hz is not 1/T for T = {t_yr} yr")
    if not np.all(np.diff(freqs) > 0):
        raise NotEvaluable("frequencies not increasing")
    dens = np.where(np.isnan(dens), NAN_LOGPDF, dens)
    return {"dir": prod["dir"], "freqs": freqs, "grid": grid, "db": float(db), "T": float(t_s),
            "density": dens, "binedges": np.append(grid - 0.5 * db, grid[-1])}


# ------------------------------------------------------------- likelihood ----

def log10rho_powerlaw(log10_a, gamma, freqs, t_s):
    """log10 rho_k for S(f) = A^2/(12 pi^2) f_yr^-3 (f/f_yr)^-gamma, rho^2 = S/T (broadcasting)."""
    log10_a = np.asarray(log10_a, dtype=float)[..., None]
    gamma = np.asarray(gamma, dtype=float)[..., None]
    lf = np.log10(freqs / F_YR)
    log10_s = (2.0 * log10_a - np.log10(12.0 * np.pi ** 2) - 3.0 * np.log10(F_YR) - gamma * lf)
    return 0.5 * (log10_s - np.log10(t_s))


def log10rho_turnover(log10_a, log10_fb, kappa, gamma, freqs, t_s):
    """Power law divided by 1 + (f_b/f)^kappa (Sampson, Cornish & McWilliams 2015)."""
    base = log10rho_powerlaw(log10_a, gamma, freqs, t_s)
    fb = 10.0 ** np.asarray(log10_fb, dtype=float)[..., None]
    kappa = np.asarray(kappa, dtype=float)[..., None]
    return base - 0.5 * np.log10(1.0 + (fb / freqs) ** kappa)


def lnlike(prod, log10rho, *, below_grid):
    """Sum over the last axis (frequencies) of the KDE log-density; K ln db is dropped."""
    k = log10rho.shape[-1]
    dens = prod["density"][:k]
    g = dens.shape[1]
    idx = np.searchsorted(prod["binedges"], log10rho, side="left") - 1
    above = idx >= g
    below = idx < 0
    idx = np.clip(idx, 0, g - 1)
    vals = dens[np.arange(k), idx]
    if below_grid == "neg_inf":
        vals = np.where(below, -np.inf, vals)
    elif below_grid != "clip":
        raise ValueError(f"below_grid must be 'clip' or 'neg_inf', not {below_grid!r}")
    vals = np.where(above, -np.inf, vals)
    return vals.sum(axis=-1)


# ---------------------------------------------------------------- 1-D grid ----

def trap_weights(n):
    w = np.ones(n)
    w[0] = w[-1] = 0.5
    return w


def axis(lo, hi, step):
    n = int(round((hi - lo) / step)) + 1
    return np.linspace(lo, hi, n)


def normalise(x, lnp):
    """Normalised density on grid x from log density (trapezoid rule)."""
    lnp = np.asarray(lnp, dtype=float)
    if not np.any(np.isfinite(lnp)):
        raise NotEvaluable("posterior is zero everywhere on the grid")
    p = np.exp(lnp - np.max(lnp))
    z = _trapz(p, x)
    if not (np.isfinite(z) and z > 0):
        raise NotEvaluable("posterior not normalisable")
    return p / z


def cdf(x, p):
    c = np.concatenate([[0.0], np.cumsum(0.5 * (p[1:] + p[:-1]) * np.diff(x))])
    return c / c[-1]


def quantiles(x, p, qs):
    c = cdf(x, p)
    return [float(np.interp(q, c, x)) for q in qs]


def edge_mass(x, p, frac):
    """Posterior mass within the outermost `frac` of the range at either end."""
    c = cdf(x, p)
    span = x[-1] - x[0]
    return float(np.interp(x[0] + frac * span, x, c) + 1.0 - np.interp(x[-1] - frac * span, x, c))


def two_piece_pdf(x, m, s_lo, s_hi):
    """Median-pinned two-piece half-normal: each side holds probability 0.5."""
    s = np.where(x < m, s_lo, s_hi)
    return np.exp(-0.5 * ((x - m) / s) ** 2) / (np.sqrt(2.0 * np.pi) * s)


def hellinger(x, p, q):
    p = p / _trapz(p, x)
    q = q / _trapz(q, x)
    bc = _trapz(np.sqrt(p * q), x)
    return float(np.sqrt(max(0.0, 1.0 - bc)))


# ------------------------------------------------------------ analyses ----

def r1(prod, *, n_freq, gamma, lo, hi, step, below_grid, l8_a, edge_frac, edge_max, h_max):
    x = axis(lo, hi, step)
    f = prod["freqs"][:n_freq]
    lnl = lnlike(prod, log10rho_powerlaw(x, np.full_like(x, gamma), f, prod["T"]), below_grid=below_grid)
    p = normalise(x, lnl)
    em = edge_mass(x, p, edge_frac)
    if em >= edge_max:
        raise NotEvaluable(f"R1 edge mass {em:.3g} >= {edge_max}")
    q05, q50, q95 = quantiles(x, p, (0.05, 0.5, 0.95))
    m = np.log10(l8_a[0])
    s_lo = (m - np.log10(l8_a[1])) / 1.645
    s_hi = (np.log10(l8_a[2]) - m) / 1.645
    ref = two_piece_pdf(x, m, s_lo, s_hi)
    h = hellinger(x, p, ref)
    return {
        "median_A": 10 ** q50, "q05_A": 10 ** q05, "q95_A": 10 ** q95,
        "log10A_median": q50, "log10A_q05": q05, "log10A_q95": q95,
        "hellinger": h, "h_max": h_max,
        "verdict": "consistent with L8's interval" if h < h_max else "differs",
        "edge_mass_log10A": em,
        "_x": x, "_p": p, "_ref": ref,
    }


def r2(prod, *, n_freq, lo_a, hi_a, lo_g, hi_g, step, below_grid, gamma_line, edge_frac, edge_max,
       chunk):
    xa = axis(lo_a, hi_a, step)
    xg = axis(lo_g, hi_g, step)
    f = prod["freqs"][:n_freq]
    lnl = np.empty((xg.size, xa.size))
    for i0 in range(0, xg.size, chunk):
        g = xg[i0:i0 + chunk]
        A, G = np.meshgrid(xa, g)
        lnl[i0:i0 + chunk] = lnlike(prod, log10rho_powerlaw(A, G, f, prod["T"]), below_grid=below_grid)
    line = lnlike(prod, log10rho_powerlaw(xa, np.full_like(xa, gamma_line), f, prod["T"]),
                  below_grid=below_grid)
    top = max(np.max(lnl), np.max(line))
    if not np.isfinite(top):
        raise NotEvaluable("R2 posterior is zero everywhere")
    p = np.exp(lnl - top)                       # uniform priors: posterior ∝ likelihood
    pline = np.exp(line - top)                  # same normalising constant
    w = p * np.outer(trap_weights(xg.size), trap_weights(xa.size)) * step * step
    z = w.sum()
    if not (np.isfinite(z) and z > 0):
        raise NotEvaluable("R2 posterior not normalisable")
    w = w / z
    pstar = float(np.max(pline))
    q = float(w[p > pstar].sum())
    q_ge = float(w[p >= pstar].sum())
    # marginal densities (trapezoid over the other axis)
    pa = (p * trap_weights(xg.size)[:, None]).sum(axis=0) * step
    pg = (p * trap_weights(xa.size)[None, :]).sum(axis=1) * step
    pa = pa / _trapz(pa, xa)
    pg = pg / _trapz(pg, xg)
    ema = edge_mass(xa, pa, edge_frac)
    emg = edge_mass(xg, pg, edge_frac)
    if ema >= edge_max or emg >= edge_max:
        raise NotEvaluable(f"R2 edge mass log10A {ema:.3g}, gamma {emg:.3g} (limit {edge_max})")
    a05, a50, a95 = quantiles(xa, pa, (0.05, 0.5, 0.95))
    g05, g50, g95 = quantiles(xg, pg, (0.05, 0.5, 0.95))
    pg_line = float(np.interp(gamma_line, xg, pg))
    hpd1 = float(np.sum((pg * trap_weights(xg.size) * step)[pg > pg_line]))
    return {
        "q_hpd_13_3": q, "q_hpd_13_3_ge": q_ge,
        "gamma_median": g50, "gamma_q05": g05, "gamma_q95": g95, "gamma_hpd1d_13_3": hpd1,
        "A_median": 10 ** a50, "A_q05": 10 ** a05, "A_q95": 10 ** a95,
        "edge_mass_log10A": ema, "edge_mass_gamma": emg,
        "_xa": xa, "_xg": xg, "_p": p / p.max() if p.max() > 0 else p,
    }


def category(q, lo, hi):
    if q < lo:
        return "weaker than L8's stated tension (descriptive category)"
    if q > hi:
        return "stronger than L8's stated tension (descriptive category)"
    return "same order as L8's stated tension (descriptive category)"


def r2b(a05, a50, a95, table):
    """Closed-interval overlap and containment against Table A1 rows (model, p16, p84)."""
    rows = []
    for model, p16, p84 in table:
        rows.append({"model": model, "p16": p16, "p84": p84,
                     "overlap_ci90": bool(a05 <= p84 and p16 <= a95),
                     "contains_median": bool(p16 <= a50 <= p84)})
    merged = {}
    for r in rows:
        merged.setdefault((r["p16"], r["p84"]), r)
    return {
        "n_rows": len(rows),
        "n_models_overlap_ci90": sum(r["overlap_ci90"] for r in rows),
        "n_models_contain_median": sum(r["contains_median"] for r in rows),
        "n_rows_merged": len(merged),
        "n_models_overlap_ci90_merged": sum(r["overlap_ci90"] for r in merged.values()),
        "n_models_contain_median_merged": sum(r["contains_median"] for r in merged.values()),
        "rows": rows,
    }


def _logsumexp(a):
    a = np.asarray(a, dtype=float)
    m = np.max(a)
    if not np.isfinite(m):
        return -np.inf
    return float(m + np.log(np.sum(np.exp(a - m))))


def r4(prod, *, n_freq, gamma, lo_a, hi_a, lo_fb, hi_fb, lo_k, hi_k, steps, below_grid, edge_frac,
       edge_max, chunk):
    sa, sf, sk = steps
    xa, xf, xk = axis(lo_a, hi_a, sa), axis(lo_fb, hi_fb, sf), axis(lo_k, hi_k, sk)
    f = prod["freqs"][:n_freq]
    lw_a, lw_f, lw_k = (np.log(trap_weights(n.size)) for n in (xa, xf, xk))
    ln_prior = -np.log(hi_a - lo_a) - np.log(hi_fb - lo_fb) - np.log(hi_k - lo_k)
    # power law
    lnl_pl = lnlike(prod, log10rho_powerlaw(xa, np.full_like(xa, gamma), f, prod["T"]), below_grid=below_grid)
    ln_z_pl = _logsumexp(lnl_pl + lw_a) + np.log(sa) - np.log(hi_a - lo_a)
    # turnover, chunked over kappa
    terms = []
    marg_a = np.full(xa.size, -np.inf)
    marg_f = np.full(xf.size, -np.inf)
    marg_k = np.full(xk.size, -np.inf)
    for i0 in range(0, xk.size, chunk):
        kk = xk[i0:i0 + chunk]
        K, F, A = np.meshgrid(kk, xf, xa, indexing="ij")
        lnl = lnlike(prod, log10rho_turnover(A, F, K, gamma, f, prod["T"]), below_grid=below_grid)
        lw = lnl + lw_k[i0:i0 + chunk, None, None] + lw_f[None, :, None] + lw_a[None, None, :]
        terms.append(_logsumexp(lw))
        marg_k[i0:i0 + chunk] = [_logsumexp(lw[j]) for j in range(kk.size)]
        marg_f = np.logaddexp(marg_f, [_logsumexp(lw[:, j]) for j in range(xf.size)])
        marg_a = np.logaddexp(marg_a, [_logsumexp(lw[:, :, j]) for j in range(xa.size)])
    ln_z_turn = _logsumexp(terms) + np.log(sa * sf * sk) + ln_prior

    def em(x, lm, w):
        p = np.exp(lm - np.max(lm) - w)     # undo trapezoid weights -> density on nodes
        return edge_mass(x, p / _trapz(p, x), edge_frac)

    ema = em(xa, marg_a, lw_a)
    if ema >= edge_max:
        raise NotEvaluable(f"R4 edge mass log10A {ema:.3g} >= {edge_max}")
    return {"ln_Z_pl": ln_z_pl, "ln_Z_turn": ln_z_turn, "ln_bf_turnover_vs_pl": ln_z_turn - ln_z_pl,
            "edge_mass_log10A": ema, "edge_mass_log10fb": em(xf, marg_f, lw_f),
            "edge_mass_kappa": em(xk, marg_k, lw_k)}
