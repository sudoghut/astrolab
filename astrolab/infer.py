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


def minimize_multistart(fun, bounds, n_starts: int = 20, seed: int = 0, constraints=(),
                        start_ok=None, x0_extra=()):
    """Bounded multi-start minimisation (SLSQP, then Nelder-Mead polish inside the bounds).

    fun: f(x) -> float; bounds: list of (lo, hi); constraints: scipy 'ineq' dicts;
    start_ok: optional predicate for random starts (e.g. w0 + wa < 0).
    Returns (x_best, f_best, all_results) where all_results lists (f, x) per start.
    """
    rng = np.random.default_rng(seed)
    lo = np.array([b[0] for b in bounds], dtype=float)
    hi = np.array([b[1] for b in bounds], dtype=float)
    starts = [np.asarray(x, dtype=float) for x in x0_extra]
    while len(starts) < n_starts + len(x0_extra):
        x = lo + (hi - lo) * rng.random(len(bounds))
        if start_ok is None or start_ok(x):
            starts.append(x)
    results = []
    for x0 in starts:
        try:
            r = optimize.minimize(fun, x0, method="SLSQP", bounds=bounds, constraints=constraints,
                                  options={"maxiter": 500, "ftol": 1e-10})
            x = np.clip(r.x, lo, hi)
            fx = float(fun(x))
            if constraints and any(c["fun"](x) < -1e-9 for c in constraints):
                continue
            results.append((fx, x))
        except (ValueError, FloatingPointError):
            continue
    if not results:
        raise RuntimeError("no successful start")
    results.sort(key=lambda t: t[0])
    return results[0][1], results[0][0], results


def run_emcee(log_prob, p0, nwalkers: int = 32, nsteps: int = 4000, seed: int = 0,
              scatter: float = 1e-3, burn_frac: float = 0.3):
    """Affine-invariant MCMC (emcee). Returns dict with flat samples (after burn-in), the
    integrated autocorrelation times, and chain length in units of the largest tau."""
    import emcee

    rng = np.random.default_rng(seed)
    p0 = np.asarray(p0, dtype=float)
    start = p0 + scatter * np.abs(p0 + 1e-3) * rng.standard_normal((nwalkers, p0.size))
    sampler = emcee.EnsembleSampler(nwalkers, p0.size, log_prob)
    sampler.random_state = np.random.RandomState(seed).get_state()
    sampler.run_mcmc(start, nsteps, progress=False)
    tau = sampler.get_autocorr_time(quiet=True)
    burn = int(burn_frac * nsteps)
    flat = sampler.get_chain(discard=burn, flat=True)
    return {"samples": flat, "tau": tau, "n_over_tau": float(nsteps / np.max(tau)),
            "acceptance": float(np.mean(sampler.acceptance_fraction))}
