"""M0 observation model and maximum-likelihood fits (README section 2.0).

Latent ages are piecewise constant on cells of a grid over [0, tmax]. A star (or a compressed cell
of stars) with observed age A and error e has a kernel K_c = P(A | latent cell c), Gaussian in A,
truncated to [0, tmax] and renormalised for each latent age; on S15 a selection term P_c = P(pass
the 15% cut | latent cell c) divides the likelihood. Nothing here reads PARAMS: every setting is an
argument.

Selection modes of the S15 denominator (README 2.0 and 2.5, SEL-1): "cut" (the 2.0 term, a fixed
error and the cut A >= e / 0.15), "emp" (term E: an empirical pass fraction pi per pass bin of the
observed age, per [Fe/H] slice, from pass_table) and "none" (term N: denominator 1).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import sparse
from scipy.optimize import minimize
from scipy.special import ndtr
from scipy.stats import skewnorm

SQ2PI = np.sqrt(2.0 * np.pi)


def phi(z):
    return np.exp(-0.5 * z * z) / SQ2PI


def ndiff(a, b):
    """Phi(b) - Phi(a) for a <= b, computed in the lower tail to avoid cancellation."""
    return np.where(a > 0, ndtr(-a) - ndtr(-b), ndtr(b) - ndtr(a))


# --------------------------------------------------------------------------------------------
# grid, cells, kernels
# --------------------------------------------------------------------------------------------
@dataclass
class Grid:
    step: float = 0.05
    tmax: float = 20.0

    def __post_init__(self):
        n = int(round(self.tmax / self.step))
        self.edges = np.linspace(0.0, self.tmax, n + 1)
        self.lo = self.edges[:-1]
        self.hi = self.edges[1:]
        self.mid = 0.5 * (self.lo + self.hi)
        self.n = n


@dataclass
class Cells:
    """Compressed data: observed age A, error e, weight w (star count), S15 threshold thr (or None),
    group index g (for [Fe/H]-dependent models) with group [Fe/H] fe and [Fe/H] error efe."""
    A: np.ndarray
    e: np.ndarray
    w: np.ndarray
    thr: np.ndarray | None = None
    g: np.ndarray | None = None
    fe: np.ndarray | None = None
    efe: np.ndarray | None = None
    sl: np.ndarray | None = None        # [Fe/H] slice index per cell (term E); None = one slice

    @property
    def nstar(self):
        return float(self.w.sum())


def compress(age, eage, *, s15, step_a=0.05, nclass=20, feh=None, efeh=None, feh_step=0.05,
             nefe=5, cut=0.15, none=False, sl=None):
    """Group stars into cells (README 2.0, Compression). none=True keeps one cell per star with its
    own error. On S15 every cell gets the threshold e_rep / cut. sl (per-star slice index, term E
    only) is added as the last cell key, so no cell mixes two [Fe/H] slices; with sl=None the cells
    are exactly those of README 2.0."""
    age = np.asarray(age, float)
    eage = np.asarray(eage, float)
    if none:
        A, e, w = age, eage, np.ones_like(age)
        thr = e / cut if s15 else None
        g = fe = efe = None
        if feh is not None:
            feh = np.asarray(feh, float)
            keys = [np.floor(feh / feh_step).astype(np.int64)]
            if efeh is not None:
                eq = np.quantile(efeh, np.linspace(0, 1, nefe + 1))
                keys.append(np.clip(np.searchsorted(eq, efeh, side="right") - 1, 0, nefe - 1))
            guniq, g = np.unique(np.stack(keys, 1), axis=0, return_inverse=True)
            g = g.ravel()
            cnt = np.bincount(g, minlength=len(guniq))
            fe = np.bincount(g, weights=feh, minlength=len(guniq)) / cnt
            efe = np.zeros(len(guniq))
            if efeh is not None:
                efe = np.array([np.median(np.asarray(efeh)[g == k]) for k in range(len(guniq))])
        return Cells(A, e, w, thr, g, fe, efe, None if sl is None else np.asarray(sl, np.int64))
    r = eage / age
    qs = np.quantile(r, np.linspace(0, 1, nclass + 1))
    cls = np.clip(np.searchsorted(qs, r, side="right") - 1, 0, nclass - 1)
    rmed = np.array([np.median(r[cls == k]) if np.any(cls == k) else np.nan for k in range(nclass)])
    ai = np.floor(age / step_a).astype(np.int64)
    keys = [ai, cls]
    if feh is not None:
        fi = np.floor(np.asarray(feh, float) / feh_step).astype(np.int64)
        keys.append(fi)
        if efeh is not None:
            eq = np.quantile(efeh, np.linspace(0, 1, nefe + 1))
            ei = np.clip(np.searchsorted(eq, efeh, side="right") - 1, 0, nefe - 1)
            keys.append(ei)
    if sl is not None:
        keys.append(np.asarray(sl, np.int64))
    K = np.stack(keys, 1)
    uniq, inv, counts = np.unique(K, axis=0, return_inverse=True, return_counts=True)
    inv = inv.ravel()
    A = (uniq[:, 0] + 0.5) * step_a
    e = rmed[uniq[:, 1]] * A
    w = counts.astype(float)
    thr = e / cut if s15 else None
    g = fe = efe = None
    if feh is not None:
        gkeys = uniq[:, 2:]
        guniq, ginv = np.unique(gkeys, axis=0, return_inverse=True)
        g = ginv.ravel()
        fe = np.zeros(len(guniq))
        efe = np.zeros(len(guniq))
        fsum = np.bincount(inv, weights=np.asarray(feh, float), minlength=len(uniq))
        # group [Fe/H] = mean over its stars; group error = median e_[Fe/H] of its stars
        star_g = g[inv]
        fe = np.bincount(star_g, weights=np.asarray(feh, float), minlength=len(guniq)) / np.bincount(star_g, minlength=len(guniq))
        if efeh is not None:
            efe = np.array([np.median(np.asarray(efeh)[star_g == k]) for k in range(len(guniq))])
        del fsum
    csl = None if sl is None else uniq[:, -1].astype(np.int64)
    return Cells(A, e, w, thr, g, fe, efe, csl)


def kernels(grid: Grid, cells: Cells, *, f=1.0, truncate=True, dtype=np.float64, sel="cut", ptab=None):
    """K (n x C): observed-age density given each latent cell (cell-integrated); P (n x C) or None:
    probability of passing the S15 cut given each latent cell. Cells without an S15 threshold (Full)
    have no P in every mode. sel: "cut" (README 2.0), "emp" (term E, ptab from pass_coefs) or
    "none" (term N, P = None)."""
    if sel not in ("cut", "emp", "none"):
        raise ValueError(f"unknown selection mode {sel!r}")
    e = (f * cells.e)[:, None]
    A = cells.A[:, None]
    K = ndiff((grid.lo - A) / e, (grid.hi - A) / e) / grid.step
    Z = None
    if truncate:
        Z = ndiff((0.0 - grid.mid) / e, (grid.tmax - grid.mid) / e)
        K = K / Z
    P = None
    if cells.thr is not None and sel == "emp":
        P = _emp_term(grid, cells, e, Z, ptab, truncate).astype(dtype)
    elif cells.thr is not None and sel == "cut":
        thr = cells.thr[:, None]
        if truncate:
            P = ndiff((thr - grid.mid) / e, (grid.tmax - grid.mid) / e) / Z
        else:
            P = ndtr(-(thr - grid.mid) / e)
        P = P.astype(dtype)
    return K.astype(dtype), P


def _emp_term(grid, cells, e, Z, ptab, truncate):
    """Term E (README 2.5, SEL-1): P_i(c) = sum_b pi_{s,b} [Phi((u_b - m_c)/e_i) - Phi((l_b - m_c)/e_i)]
    / Z_i(c), accumulated edge by edge as sum_j c[s, j] Phi((U_j - m_c)/e_i) over the union edges U
    of all slices (c from pass_coefs; one temporary of the size of P). Truncated: the outer edges are
    0 and tmax and Z is the kernel's truncation normaliser. Untruncated: the outer bins extend to
    -inf and +inf (their Phi terms are 0 and 1) and Z = 1."""
    if ptab is None:
        raise ValueError("selection mode 'emp' needs ptab (pass_coefs of the pass tables)")
    U, coef, pi_last = ptab["U"], ptab["c"], ptab["pi_last"]
    if not (abs(U[0]) < 1e-9 and abs(U[-1] - grid.tmax) < 1e-9):
        raise ValueError("pass-bin edges must run from 0 to tmax")
    n = len(cells.A)
    sl = np.zeros(n, np.int64) if cells.sl is None else np.asarray(cells.sl, np.int64)
    if n and (sl.min() < 0 or sl.max() >= coef.shape[0]):
        raise ValueError("cell slice index outside the pass tables")
    P = np.zeros((n, grid.n))
    tmp = np.empty((n, grid.n))
    js = range(len(U)) if truncate else range(1, len(U) - 1)
    for j in js:
        cj = coef[sl, j]
        if not np.any(cj):
            continue
        np.subtract(U[j], grid.mid[None, :], out=tmp)
        np.divide(tmp, e, out=tmp)
        ndtr(tmp, out=tmp)
        np.multiply(tmp, cj[:, None], out=tmp)
        P += tmp
    del tmp
    if truncate:
        P /= Z
    else:
        P += pi_last[sl][:, None]
    np.clip(P, 0.0, 1.0, out=P)        # rounding of the edge sum
    return P


# --------------------------------------------------------------------------------------------
# pass tables (README 2.5, SEL-0)
# --------------------------------------------------------------------------------------------
def merge_bins(counts, n_min):
    """SEL-0 merge rule: walk from the youngest bin upward, accumulating consecutive bins until the
    group's count is >= n_min, then close it; a last group with fewer than n_min is merged into the
    previous closed group (or, if there is none, the slice is one group). Returns [first, last]
    bin indices of each group."""
    groups = []
    start, acc = 0, 0
    nb = len(counts)
    for i, c in enumerate(counts):
        acc += int(c)
        if acc >= n_min:
            groups.append([start, i])
            start, acc = i + 1, 0
    if start < nb:
        if groups:
            groups[-1][1] = nb - 1
        else:
            groups.append([0, nb - 1])
    return groups


def pass_table(age, relerr, sl=None, *, nslice=1, width=1.0, tmax=20.0, n_min=200, cut=0.15):
    """Pass tables of a parent set (README 2.5, SEL-0). Parent rows need Age > 0 and a finite
    relative error (others are dropped and counted in n_dropped). Observed-age bins [k w, (k + 1) w),
    Age >= tmax in the last bin, merged per slice by merge_bins; pi = parent stars with
    relerr < cut / parent stars. Returns one dict per slice: edges, n, n_pass, pi (lists), n_parent,
    n_dropped, and pools (index arrays into the input, one per pass bin; not JSON)."""
    age = np.asarray(age, float)
    relerr = np.asarray(relerr, float)
    sl = np.zeros(len(age), np.int64) if sl is None else np.asarray(sl, np.int64)
    ok = np.isfinite(age) & (age > 0) & np.isfinite(relerr)
    nb = int(round(tmax / width))
    k = np.full(len(age), -1, np.int64)
    k[ok] = np.clip(np.floor(age[ok] / width).astype(np.int64), 0, nb - 1)
    passed = relerr < cut
    out = []
    for s in range(nslice):
        ms = ok & (sl == s)
        cnt = np.bincount(k[ms], minlength=nb)
        groups = merge_bins(cnt, n_min)
        gi = np.empty(nb, np.int64)
        for b, (a0, a1) in enumerate(groups):
            gi[a0:a1 + 1] = b
        edges = [g[0] * width for g in groups] + [float(tmax)]
        star_g = np.full(len(age), -1, np.int64)
        star_g[ms] = gi[k[ms]]
        pools = [np.flatnonzero(star_g == b) for b in range(len(groups))]
        n = [int(len(p)) for p in pools]
        npass = [int(passed[p].sum()) for p in pools]
        pi = [npass[b] / n[b] if n[b] > 0 else 0.0 for b in range(len(groups))]
        out.append({"edges": [float(x) for x in edges], "n": n, "n_pass": npass, "pi": pi,
                    "n_parent": int(ms.sum()), "n_dropped": int(((~ok) & (sl == s)).sum()),
                    "pools": pools})
    return out


def table_json(tables):
    """JSON-safe copy of pass tables (without the pools)."""
    return [{k: v for k, v in t.items() if k != "pools"} for t in tables]


def pass_coefs(tables):
    """Edge coefficients of term E for kernels(sel="emp"): the union U of all slices' edges and,
    per slice s, c[s, j] = pi_s(bin left of U_j) - pi_s(bin right of U_j) (0 beyond the outer
    edges), so that sum_b pi_b [Phi(u_b) - Phi(l_b)] = sum_j c[s, j] Phi(U_j); pi_last = pi of the
    oldest bin (the untruncated variant's constant)."""
    U = np.unique(np.round(np.concatenate([np.asarray(t["edges"], float) for t in tables]), 9))
    S, J = len(tables), len(U) - 1
    piu = np.zeros((S, J))
    mids = 0.5 * (U[:-1] + U[1:])
    for s, t in enumerate(tables):
        ed = np.asarray(t["edges"], float)
        b = np.clip(np.searchsorted(ed, mids, side="right") - 1, 0, len(t["pi"]) - 1)
        piu[s] = np.asarray(t["pi"], float)[b]
    ext = np.concatenate([np.zeros((S, 1)), piu, np.zeros((S, 1))], axis=1)
    coef = ext[:, :-1] - ext[:, 1:]            # c_j = pi_{j-1} - pi_j, j = 0..J
    return {"U": U, "c": coef, "pi_last": piu[:, -1].copy()}


# --------------------------------------------------------------------------------------------
# latent distributions on the grid (cell probabilities) and their derivatives
# --------------------------------------------------------------------------------------------
def tn_cells(grid: Grid, mu, s):
    """Truncated normal on [0, tmax]: cell probabilities q and dq/dmu, dq/ds.
    mu, s: arrays of shape (m, 1) (or scalars); returns arrays (m, C)."""
    mu = np.atleast_2d(np.asarray(mu, float).reshape(-1, 1))
    s = np.atleast_2d(np.asarray(s, float).reshape(-1, 1))
    zl = (grid.lo - mu) / s
    zu = (grid.hi - mu) / s
    a = (0.0 - mu) / s
    b = (grid.tmax - mu) / s
    num = ndiff(zl, zu)
    Z = np.maximum(ndiff(a, b), 1e-300)
    q = num / Z
    dnum_dmu = -(phi(zu) - phi(zl)) / s
    dZ_dmu = -(phi(b) - phi(a)) / s
    dnum_ds = -(phi(zu) * zu - phi(zl) * zl) / s
    dZ_ds = -(phi(b) * b - phi(a) * a) / s
    dq_dmu = (dnum_dmu - q * dZ_dmu) / Z
    dq_ds = (dnum_ds - q * dZ_ds) / Z
    return q, dq_dmu, dq_ds


def mix_unpack(theta, K):
    mu = theta[:K]
    s = np.exp(theta[K:2 * K])
    eta = np.concatenate([[0.0], theta[2 * K:3 * K - 1]])
    w = np.exp(eta - eta.max())
    w /= w.sum()
    return mu, s, w


def mix_cells(grid, theta, K, grad=False):
    mu, s, w = mix_unpack(theta, K)
    q, dmu, ds = tn_cells(grid, mu, s)
    p = w @ q
    if not grad:
        return p
    # dp/dtheta: (ntheta, C)
    J = np.zeros((3 * K - 1, grid.n))
    J[:K] = w[:, None] * dmu
    J[K:2 * K] = (w * s)[:, None] * ds
    for j in range(1, K):
        J[2 * K + j - 1] = w[j] * (q[j] - p)
    return p, J


MIN_GRID_MASS = 1e-10


def _cells_from_cdf_sf(c, sf):
    """Cell probabilities on the grid from the CDF and survival function at the edges, each cell
    taken from the tail where it is not a difference of numbers near 1; renormalised over the
    grid. A distribution with less than MIN_GRID_MASS on the grid returns zeros (the likelihood
    floor then penalises it) rather than renormalised rounding noise."""
    upper = c[:-1] > 0.5
    d = np.where(upper, sf[:-1] - sf[1:], c[1:] - c[:-1])
    d = np.maximum(d, 0.0)
    Z = d.sum()
    if not Z > MIN_GRID_MASS:
        return np.zeros_like(d)
    return d / Z


def skewnorm_cells(grid, theta):
    loc, logsc, alpha = theta
    sc = np.exp(logsc)
    return _cells_from_cdf_sf(skewnorm.cdf(grid.edges, alpha, loc, sc), skewnorm.sf(grid.edges, alpha, loc, sc))


def splitnorm_cdf(x, m, s1, s2):
    x = np.asarray(x, float)
    out = np.where(x < m, 2 * s1 / (s1 + s2) * ndtr((x - m) / s1),
                   s1 / (s1 + s2) + 2 * s2 / (s1 + s2) * (ndtr((x - m) / s2) - 0.5))
    return out


def splitnorm_sf(x, m, s1, s2):
    x = np.asarray(x, float)
    return np.where(x < m, 1.0 - 2 * s1 / (s1 + s2) * ndtr((x - m) / s1),
                    2 * s2 / (s1 + s2) * ndtr(-(x - m) / s2))


def splitnorm_cells(grid, theta):
    m, l1, l2 = theta
    s1, s2 = np.exp(l1), np.exp(l2)
    return _cells_from_cdf_sf(splitnorm_cdf(grid.edges, m, s1, s2), splitnorm_sf(grid.edges, m, s1, s2))


TINY = 1e-300


def floored_terms(w, num, den=None):
    """Weighted log-likelihood sum_i w_i [log num_i - log den_i] with a floor, and the per-row
    derivative factors (d ll / d num_i, d ll / d den_i).

    A row whose term sits on the floor is constant in the parameters (zero derivative). If the
    selection probability den_i is on the floor, the row gets the floor value log(TINY) and no
    den correction: otherwise num and den would both be floored and the term would be exactly 0,
    a spurious optimum for latent distributions with no mass on the grid."""
    numc = np.maximum(num, TINY)
    sn = np.where(num > TINY, w / numc, 0.0)
    if den is None:
        return float(w @ np.log(numc)), sn, None
    ok = den > TINY
    denc = np.maximum(den, TINY)
    terms = np.where(ok, np.log(numc) - np.log(denc), np.log(TINY))
    sn = np.where(ok, sn, 0.0)
    sd = np.where(ok & (num > TINY), w / denc, 0.0)
    return float(w @ terms), sn, sd


# --------------------------------------------------------------------------------------------
# 1-D likelihood (one latent distribution for all cells)
# --------------------------------------------------------------------------------------------
class OneD:
    def __init__(self, grid, cells, *, f=1.0, truncate=True, dtype=np.float64, sel="cut", ptab=None):
        self.grid = grid
        self.cells = cells
        self.K, self.P = kernels(grid, cells, f=f, truncate=truncate, dtype=dtype, sel=sel, ptab=ptab)
        self.w = cells.w

    def ll_p(self, p, grad=False):
        p = np.maximum(p, 0.0)
        num = self.K @ p
        den = self.P @ p if self.P is not None else None
        ll, sn, sd = floored_terms(self.w, num, den)
        if not grad:
            return ll
        g = self.K.T @ sn
        if sd is not None:
            g = g - self.P.T @ sd
        return ll, g

    # ---- Gaussian mixtures (analytic gradient)
    def mix_negll(self, theta, K):
        p, J = mix_cells(self.grid, theta, K, grad=True)
        ll, g = self.ll_p(p, grad=True)
        return -ll, -(J @ g)

    def fit_mixture(self, K, starts):
        bounds = [(-5.0, 25.0)] * K + [(np.log(0.1), np.log(10.0))] * K + [(-12.0, 12.0)] * (K - 1)
        best = None
        for th0 in starts:
            th0 = np.clip(th0, [b[0] for b in bounds], [b[1] for b in bounds])
            r = minimize(self.mix_negll, th0, args=(K,), jac=True, method="L-BFGS-B", bounds=bounds)
            if not np.isfinite(r.fun):
                continue
            if _better(r, best):
                best = r
        if best is None:
            raise RuntimeError("all optimiser starts gave a non-finite objective")
        return best

    # ---- parametric unimodal nulls (numerical gradient; three parameters)
    def fit_param(self, cellfun, starts, bounds):
        def nll(th):
            return -self.ll_p(cellfun(self.grid, th))
        best = None
        for th0 in starts:
            r = minimize(nll, th0, method="L-BFGS-B", bounds=bounds)
            if not np.isfinite(r.fun):
                continue
            if _better(r, best):
                best = r
        if best is None:
            raise RuntimeError("all optimiser starts gave a non-finite objective")
        return best


def mixture_starts(ages, weights, K, nstart, rng):
    """README 2.0: means at the (j + 0.5)/K weighted quantiles, widths 1.5 Gyr, equal weights,
    plus nstart - 1 seeded perturbations."""
    order = np.argsort(ages)
    cw = np.cumsum(weights[order]) / weights.sum()
    mus = np.array([ages[order][np.searchsorted(cw, (j + 0.5) / K)] for j in range(K)])
    base = np.concatenate([mus, np.full(K, np.log(1.5)), np.zeros(K - 1)])
    out = [base]
    for _ in range(nstart - 1):
        out.append(base + np.concatenate([rng.normal(0, 1.0, K), rng.normal(0, 0.3, K), rng.normal(0, 0.5, K - 1)]))
    return out


def _better(r, best):
    """Start selection (README 2.0): the lower objective wins, ties within 0.01 keep the earlier
    start. Convergence is not used for selection (L-BFGS-B often reports a line-search stop at a
    flat optimum); the chosen result's .success is recorded by the callers instead."""
    return best is None or r.fun < best.fun - 0.01


def perturb(theta, n, rng, scale=0.2):
    return [theta] + [theta + rng.normal(0, scale, len(theta)) for _ in range(n)]


def bic(nll, k, n):
    return 2.0 * nll + k * np.log(n)


# --------------------------------------------------------------------------------------------
# density shape: peaks, valley, depth (README 2.1)
# --------------------------------------------------------------------------------------------
def _local_extrema(y):
    """Indices of local maxima and minima of y, plateaus represented by their centre."""
    n = len(y)
    # compress plateaus
    idx = [0]
    for i in range(1, n):
        if y[i] != y[idx[-1]]:
            idx.append(i)
    starts = np.array(idx)
    ends = np.append(starts[1:] - 1, n - 1)
    vals = y[starts]
    maxima, minima = [], []
    for k in range(len(vals)):
        left = vals[k - 1] if k > 0 else -np.inf
        right = vals[k + 1] if k < len(vals) - 1 else -np.inf
        c = (starts[k] + ends[k]) // 2
        if vals[k] > left and vals[k] > right:
            maxima.append(c)
        lft = vals[k - 1] if k > 0 else np.inf
        rgt = vals[k + 1] if k < len(vals) - 1 else np.inf
        if vals[k] < lft and vals[k] < rgt:
            minima.append(c)
    return maxima, minima


def peaks(dens, prom=0.10):
    """Local maxima that survive the prominence rule: between two adjacent peaks, the lower one is
    dropped if (lower peak - minimum between them) < prom x lower peak; repeated until stable."""
    pk, _ = _local_extrema(dens)
    pk = list(pk)
    changed = True
    while changed and len(pk) > 1:
        changed = False
        worst, worst_k = None, None
        for k in range(len(pk) - 1):
            i, j = pk[k], pk[k + 1]
            m = dens[i:j + 1].min()
            low = min(dens[i], dens[j])
            if low <= 0 or (low - m) < prom * low:
                rel = (low - m) / low if low > 0 else -1
                if worst is None or rel < worst:
                    worst, worst_k = rel, k
        if worst_k is not None:
            i, j = pk[worst_k], pk[worst_k + 1]
            pk.pop(worst_k if dens[i] < dens[j] else worst_k + 1)
            changed = True
    return pk


def valley(grid, p, *, lo=5.0, hi=11.0, side_mass=0.10, prom=0.10, keep_peaks=None):
    """Deepest valley between lo and hi with at least side_mass of latent mass on each side.
    Returns dict with d (1 if no valley), position, edge (97.5th percentile of the mass younger than
    the valley), peak positions."""
    dens = p / grid.step
    pk = peaks(dens, prom)
    if keep_peaks is not None:
        pk = [i for i in pk if keep_peaks(grid.mid[i])]
    cum = np.cumsum(p)
    best = None
    for k in range(len(pk) - 1):
        i, j = pk[k], pk[k + 1]
        v = i + int(np.argmin(dens[i:j + 1]))
        t = grid.mid[v]
        if not (lo <= t <= hi):
            continue
        if cum[v] < side_mass or 1 - cum[v] < side_mass:
            continue
        left = dens[pk[:k + 1]].max()
        right = dens[pk[k + 1:]].max()
        d = dens[v] / min(left, right)
        if best is None or d < best["d"]:
            best = {"d": float(d), "t": float(t), "v": v}
    out = {"peaks": [float(grid.mid[i]) for i in pk], "nmodes": len(pk)}
    if best is None:
        out.update({"d": 1.0, "t": None, "edge": None, "valley": False})
        return out
    v = best["v"]
    young = p[:v]
    cy = np.cumsum(young) / max(young.sum(), 1e-300)
    edge = float(grid.mid[np.searchsorted(cy, 0.975)])
    out.update({"d": best["d"], "t": best["t"], "edge": edge, "valley": True})
    return out


def quantile_cells(grid, p, qs):
    if not p.sum() > 0:
        return [float("nan")] * len(qs)
    c = np.cumsum(p) / p.sum()
    return [float(grid.mid[min(np.searchsorted(c, q), grid.n - 1)]) for q in qs]


def max_window(grid, p, width):
    n = int(round(width / grid.step))
    if not p.sum() > 0:
        return float("nan")
    c = np.concatenate([[0.0], np.cumsum(p)])
    return float((c[n:] - c[:-n]).max() / p.sum())


# --------------------------------------------------------------------------------------------
# [Fe/H]-dependent models (R3/R4): grouped latent distributions
# --------------------------------------------------------------------------------------------
class Grouped:
    """Cells with group index g; latent distribution of group k is a truncated normal (old
    sequence), optionally mixed with a background truncated normal. Analytic gradients."""

    def __init__(self, grid, cells, *, f=1.0, truncate=True, feh_err=False, dtype=np.float64, sel="cut",
                 ptab=None):
        self.grid = grid
        self.c = cells
        self.K, self.P = kernels(grid, cells, f=f, truncate=truncate, dtype=dtype, sel=sel, ptab=ptab)
        self.w = cells.w.astype(float)
        self.g = cells.g
        self.fe = cells.fe
        self.efe2 = (cells.efe ** 2) if feh_err else np.zeros_like(cells.fe)
        self.G = len(self.fe)
        # sparse group-indicator matrix (G x n). A cumulative-sum-and-difference group sum loses
        # all precision after rows with very large w / num (outlying stars), so sum exactly.
        n = len(self.g)
        self.S = sparse.csr_matrix((np.ones(n), (self.g, np.arange(n))), shape=(self.G, n))

    def _sum_by_group(self, M):
        return np.asarray(self.S @ M)

    def _ll_q(self, Q):
        """Q: (G x C) latent cell probabilities per group. Returns ll and dll/dQ (G x C)."""
        # float64 throughout: in float32 the latent probabilities of outlying cells underflow and
        # w / num overflows (inf * 0 = nan). Where a likelihood term sits on its floor it is constant
        # in the parameters, so its gradient contribution is zero (consistent with the value).
        Qr = Q[self.g]
        num = (self.K * Qr).sum(1, dtype=np.float64)
        den = (self.P * Qr).sum(1, dtype=np.float64) if self.P is not None else None
        ll, sn, sd = floored_terms(self.w, num, den)
        Gm = self.K * sn[:, None]
        if sd is not None:
            Gm = Gm - self.P * sd[:, None]
        return ll, self._sum_by_group(Gm)

    def seq_negll(self, th):
        t0, a, ls = th
        s0 = np.exp(ls)
        s = np.sqrt(s0 ** 2 + a ** 2 * self.efe2)
        mu = t0 + a * self.fe
        q, dmu, ds = tn_cells(self.grid, mu, s)
        ll, G = self._ll_q(q)
        gmu = (G * dmu).sum(1)
        gs = (G * ds).sum(1)
        ds_da = np.where(s > 0, a * self.efe2 / s, 0.0)
        ds_dls = s0 ** 2 / s
        grad = np.array([gmu.sum(), (gmu * self.fe).sum() + (gs * ds_da).sum(), (gs * ds_dls).sum()])
        return -ll, -grad

    def fit_seq(self, starts):
        bounds = [(0.0, 20.0), (-15.0, 5.0), (np.log(0.01), np.log(10.0))]
        best = None
        for th0 in starts:
            r = minimize(self.seq_negll, th0, jac=True, method="L-BFGS-B", bounds=bounds)
            if not np.isfinite(r.fun):
                continue
            if _better(r, best):
                best = r
        if best is None:
            raise RuntimeError("all optimiser starts gave a non-finite objective")
        return best

    def mix_negll(self, th):
        t0, a, ls, b0, b1, lsb, eta = th
        s0 = np.exp(ls)
        s = np.sqrt(s0 ** 2 + a ** 2 * self.efe2)
        sb = np.exp(lsb)
        fb = 1.0 / (1.0 + np.exp(-eta))
        q1, d1m, d1s = tn_cells(self.grid, t0 + a * self.fe, s)
        q2, d2m, d2s = tn_cells(self.grid, b0 + b1 * self.fe, np.full_like(self.fe, sb))
        Q = (1 - fb) * q1 + fb * q2
        ll, G = self._ll_q(Q)
        g1m = (1 - fb) * (G * d1m).sum(1)
        g1s = (1 - fb) * (G * d1s).sum(1)
        g2m = fb * (G * d2m).sum(1)
        g2s = fb * (G * d2s).sum(1)
        ds_da = np.where(s > 0, a * self.efe2 / s, 0.0)
        grad = np.array([
            g1m.sum(), (g1m * self.fe).sum() + (g1s * ds_da).sum(), (g1s * s0 ** 2 / s).sum(),
            g2m.sum(), (g2m * self.fe).sum(), g2s.sum() * sb,
            (G * (q2 - q1)).sum() * fb * (1 - fb)])
        return -ll, -grad

    def fit_mix(self, starts):
        bounds = [(0.0, 20.0), (-15.0, 5.0), (np.log(0.01), np.log(10.0)),
                  (-5.0, 25.0), (-15.0, 15.0), (np.log(0.1), np.log(10.0)), (-8.0, 8.0)]
        best = None
        for th0 in starts:
            r = minimize(self.mix_negll, th0, jac=True, method="L-BFGS-B", bounds=bounds)
            if not np.isfinite(r.fun):
                continue
            if _better(r, best):
                best = r
        if best is None:
            raise RuntimeError("all optimiser starts gave a non-finite objective")
        return best


def hessian_se(fun_grad, theta, h=1e-4):
    """Standard errors from a central-difference Hessian of the gradient (fun_grad returns
    (value, gradient) of the negative log-likelihood)."""
    n = len(theta)
    H = np.zeros((n, n))
    for i in range(n):
        dt = np.zeros(n)
        dt[i] = h * max(1.0, abs(theta[i]))
        gp = fun_grad(theta + dt)[1]
        gm = fun_grad(theta - dt)[1]
        H[i] = (gp - gm) / (2 * dt[i])
    H = 0.5 * (H + H.T)
    try:
        cov = np.linalg.inv(H)
        se = np.sqrt(np.clip(np.diag(cov), 0, None))
    except np.linalg.LinAlgError:
        cov = None
        se = np.full(n, np.nan)
    return se, cov
