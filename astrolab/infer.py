"""Small inference toolkit: Gaussian likelihoods, analytic marginalisation, MAP fits, MCMC.

Used by studies/002-m01-desi-bao-evolving-dark-energy (design plan 010). Pure functions; no data
access (fetching stays in astrolab.fetch).
"""
from __future__ import annotations

import numpy as np
from scipy import optimize, stats


def gaussian_chi2(resid, cinv) -> float:
    """r^T C^-1 r."""
    r = np.asarray(resid, dtype=float)
    return float(r @ cinv @ r)


def chi2_marg_offset(delta, cinv) -> float:
    """chi2 analytically marginalised over a constant additive offset (flat prior), e.g. the
    supernova absolute magnitude: delta^T C^-1 delta - (1^T C^-1 delta)^2 / (1^T C^-1 1).
    (The constant log-determinant term of the marginalisation is dropped.)"""
    d = np.asarray(delta, dtype=float)
    cd = cinv @ d
    c1 = cinv.sum(axis=1)
    return float(d @ cd - (c1 @ d) ** 2 / c1.sum())


def sigma_from_dchi2(dchi2: float, dof: int = 2) -> float:
    """Gaussian-equivalent two-sided significance of an improvement -dchi2 (dchi2 <= 0) for a
    chi2 distribution with ``dof`` degrees of freedom (DESI DR2 Eq. 22)."""
    x = max(-float(dchi2), 0.0)
    p = stats.chi2.sf(x, dof)
    return float(stats.norm.isf(p / 2.0))


PENALTY = 1e30


def minimize_multistart(fun, bounds, n_starts: int = 20, seed: int = 0, constraint=None,
                        x0_extra=(), agree_tol: float = 0.01, n_polish: int = 2,
                        xatol: float = 1e-7, fatol: float = 1e-6, maxfev: int = 4000):
    """Bounded multi-start minimisation that is robust to bad parameter scaling and NaNs.

    The search runs in unit-scaled coordinates u in [0, 1]^n (x = lo + (hi - lo) u) with the
    derivative-free Nelder-Mead method; points outside the box, points violating
    ``constraint(x) >= 0`` (e.g. -(w0 + wa)) and non-finite objective values get a large penalty,
    so they can never be returned as the optimum. Each start is polished by ``n_polish`` restarts
    from its own end point. ``x0_extra`` are added as starts (e.g. the nested-model optimum).

    Returns a dict: x, f, n_agree (starts within ``agree_tol`` of the best f), n_ok (finite starts),
    and all (sorted list of (f, x)).
    """
    lo = np.array([b[0] for b in bounds], dtype=float)
    hi = np.array([b[1] for b in bounds], dtype=float)
    span = hi - lo

    def feasible(x):
        return constraint is None or constraint(x) >= 0.0

    def g(u):
        if np.any(u < 0.0) or np.any(u > 1.0):
            return PENALTY
        x = lo + span * u
        if not feasible(x):
            return PENALTY
        try:
            with np.errstate(invalid="ignore", divide="ignore", over="ignore"):
                f = float(fun(x))
        except (ValueError, FloatingPointError, ZeroDivisionError, OverflowError):
            return PENALTY
        return f if np.isfinite(f) else PENALTY

    rng = np.random.default_rng(seed)
    starts = [(np.asarray(x, dtype=float) - lo) / span for x in x0_extra]
    tries = 0
    while len(starts) < n_starts + len(x0_extra) and tries < 1000 * n_starts:
        tries += 1
        u = rng.random(len(bounds))
        if g(u) < PENALTY:
            starts.append(u)
    results = []
    opts = {"xatol": xatol, "fatol": fatol, "maxfev": maxfev, "adaptive": True}
    for u0 in starts:
        u0 = np.clip(u0, 0.0, 1.0)
        r = optimize.minimize(g, u0, method="Nelder-Mead", options=opts)
        for _ in range(n_polish):
            r = optimize.minimize(g, r.x, method="Nelder-Mead", options=opts)
        if r.fun < PENALTY:
            results.append((float(r.fun), lo + span * r.x))
    if not results:
        raise RuntimeError("no start reached a finite, feasible point")
    results.sort(key=lambda t: t[0])
    best_f, best_x = results[0]
    n_agree = sum(1 for f, _ in results if f - best_f <= agree_tol)
    return {"x": best_x, "f": best_f, "n_agree": n_agree, "n_ok": len(results), "all": results}


def run_emcee(log_prob, p0, nwalkers: int = 32, nsteps: int = 4000, seed: int = 0,
              scatter: float = 1e-3, burn_frac: float = 0.3):
    """Affine-invariant MCMC (emcee). Returns dict with flat samples (after burn-in), the
    integrated autocorrelation times, and chain length in units of the largest tau."""
    import emcee

    rng = np.random.default_rng(seed)
    p0 = np.asarray(p0, dtype=float)
    start = p0 + scatter * np.abs(p0 + 1e-3) * rng.standard_normal((nwalkers, p0.size))
    if not all(np.isfinite(log_prob(w)) for w in start):
        raise ValueError("initial walkers have non-finite log_prob; start closer to the optimum")
    sampler = emcee.EnsembleSampler(nwalkers, p0.size, log_prob)
    sampler.random_state = np.random.RandomState(seed).get_state()
    sampler.run_mcmc(start, nsteps, progress=False)
    burn = int(burn_frac * nsteps)
    chain = sampler.get_chain(discard=burn)
    tau = emcee.autocorr.integrated_time(chain, quiet=True)
    flat = chain.reshape(-1, p0.size)
    return {"samples": flat, "tau": tau, "n_over_tau": float((nsteps - burn) / np.max(tau)),
            "acceptance": float(np.mean(sampler.acceptance_fraction))}
