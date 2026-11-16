"""Mock catalogues for the R1 calibration and the R3/R4 recovery checks (README 2.1, 2.3).

Deliberately independent of the likelihood code in m0.py: latent ages are drawn by rejection
sampling from the generating distributions, observed ages are drawn star by star, and the S15 cut
is applied to the drawn catalogue values. Nothing here reads PARAMS.
"""
from __future__ import annotations

import numpy as np
from scipy.stats import skewnorm


MAX_ROUNDS = 1000


def _trunc(draw, n, rng, tmax):
    out = np.empty(0)
    for _ in range(MAX_ROUNDS):
        if len(out) >= n:
            return out[:n]
        x = draw(max(2 * (n - len(out)), 256))
        out = np.concatenate([out, x[(x > 0) & (x < tmax)]])
    if len(out) >= n:
        return out[:n]
    raise RuntimeError(f"latent sampler: acceptance too low in (0, {tmax}) ({len(out)} of {n})")


def latent_normal(mu, s, n, rng, tmax=20.0):
    return _trunc(lambda m: rng.normal(mu, s, m), n, rng, tmax)


def latent_mixture(mu, s, w, n, rng, tmax=20.0):
    k = rng.choice(len(w), size=n, p=w)
    out = np.empty(n)
    for j in range(len(w)):
        idx = np.flatnonzero(k == j)
        if len(idx):
            out[idx] = latent_normal(mu[j], s[j], len(idx), rng, tmax)
    return out


def latent_skewnorm(loc, scale, alpha, n, rng, tmax=20.0):
    return _trunc(lambda m: skewnorm.rvs(alpha, loc, scale, size=m, random_state=rng), n, rng, tmax)


def latent_split(m, s1, s2, n, rng, tmax=20.0):
    def draw(k):
        left = rng.random(k) < s1 / (s1 + s2)
        z = np.abs(rng.normal(size=k))
        return np.where(left, m - s1 * z, m + s2 * z)
    return _trunc(draw, n, rng, tmax)


def latent_power(mu_old, s_old, w_old, edge, n, rng, lo=1.5, tmax=20.0):
    old = rng.random(n) < w_old
    out = rng.uniform(lo, edge, n)
    k = int(old.sum())
    if k:
        out[old] = latent_normal(mu_old, s_old, k, rng, tmax)
    return out


def observe(tau, r, mech, rng, tmax=20.0):
    """Observed ages and catalogue errors: mech 'rtau' (e = r tau) or 'rA' (e = r A). Draws are
    repeated for a star until its observed age lies in (0, tmax)."""
    tau = np.asarray(tau, float)
    r = np.asarray(r, float)
    A = np.full(len(tau), np.nan)
    todo = np.arange(len(tau))
    for _ in range(200):
        if len(todo) == 0:
            break
        z = rng.standard_normal(len(todo))
        if mech == "rtau":
            a = tau[todo] + r[todo] * tau[todo] * z
        else:
            den = 1.0 - r[todo] * z
            a = np.where(den > 0, tau[todo] / np.where(den > 0, den, 1.0), np.nan)
        ok = np.isfinite(a) & (a > 0) & (a < tmax)
        A[todo[ok]] = a[ok]
        todo = todo[~ok]
    keep = np.isfinite(A)
    tau, r, A = tau[keep], r[keep], A[keep]
    e = r * tau if mech == "rtau" else r * A
    return A, e, keep


def catalogue(draw_rows, n_target, mech, rng, *, s15, cut=0.15, tmax=20.0, batch=None):
    """Draw stars until n_target pass the selection. draw_rows(m) returns a dict with at least
    'tau' and 'r' (arrays of length m) and optionally other per-star arrays (e.g. 'feh').
    Returns a dict with 'A', 'e' and the other arrays of the selected stars."""
    out = {}
    have = 0
    for _ in range(MAX_ROUNDS):
        if have >= n_target:
            break
        m = batch or max(2 * (n_target - have), 1024)
        rows = draw_rows(m)
        A, e, keep = observe(rows["tau"], rows["r"], mech, rng, tmax)
        sel = (e / A < cut) if s15 else np.ones(len(A), bool)
        new = {"A": A[sel], "e": e[sel]}
        for k, v in rows.items():
            if k not in ("tau", "r"):
                new[k] = np.asarray(v)[keep][sel]
        new["tau"] = np.asarray(rows["tau"])[keep][sel]
        for k, v in new.items():
            out[k] = np.concatenate([out[k], v]) if k in out else v
        have = len(out["A"])
    if have < n_target:
        raise RuntimeError(f"catalogue: selection rate too low ({have} of {n_target})")
    return {k: v[:n_target] for k, v in out.items()}
