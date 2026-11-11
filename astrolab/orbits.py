"""Astrometric binary orbits from Gaia non-single-star (NSS) solutions.

- Thiele-Innes -> photocentre semi-major axis a0 (Gaia DR3 documentation,
  chapter 7.2.5, eq. 7.15): u = (A^2+B^2+F^2+G^2)/2, v = AG - BF,
  a0 = sqrt(u + sqrt(u^2 - v^2)).
- Astrometric mass function for a DARK companion (photocentre = primary):
  f_M = (a0/parallax)^3 / P_yr^2 = M2^3 / (M1 + M2)^2   [Msun].
- Covariance from ``corr_vec``: parameter order per ``nss_solution_type`` as in
  the official Gaia DPAC package ``nsstools`` (classes.py, _fields/covmat);
  upper triangle, column-major; parameters with non-finite errors are not fitted.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

DAYS_PER_YEAR = 365.25

_BASE = ["ra", "dec", "parallax", "pmra", "pmdec",
         "a_thiele_innes", "b_thiele_innes", "f_thiele_innes", "g_thiele_innes",
         "c_thiele_innes", "h_thiele_innes"]


def solution_parameters(solution_type: str) -> list[str]:
    """Full candidate parameter list (before dropping unfitted ones), nsstools order."""
    if solution_type == "Orbital":
        return _BASE + ["eccentricity", "period", "t_periastron"]
    if "OrbitalAlternative" in solution_type or "OrbitalTargetedSearch" in solution_type:
        return _BASE + ["period", "eccentricity", "t_periastron"]
    if solution_type == "AstroSpectroSB1":
        return _BASE + ["center_of_mass_velocity", "eccentricity", "period", "t_periastron"]
    raise ValueError(f"not an astrometric-orbit solution type: {solution_type!r}")


def fitted_parameters(row: pd.Series) -> list[str]:
    names = solution_parameters(row["nss_solution_type"])
    return [n for n in names if np.isfinite(row.get(f"{n}_error", np.nan))]


def covariance(row: pd.Series) -> tuple[list[str], np.ndarray]:
    """Covariance matrix of the fitted parameters of one NSS solution row."""
    names = fitted_parameters(row)
    errs = np.array([row[f"{n}_error"] for n in names], dtype=float)
    corr = np.asarray(row["corr_vec"], dtype=float)
    corr = corr[np.isfinite(corr)]
    n = len(names)
    if len(corr) != n * (n - 1) // 2:
        raise ValueError(f"corr_vec has {len(corr)} entries, expected {n * (n - 1) // 2} for {n} params")
    cov = np.diag(errs**2)
    k = 0
    for j in range(n):
        for i in range(j):
            cov[i, j] = cov[j, i] = corr[k] * errs[i] * errs[j]
            k += 1
    return names, cov


def a0_mas(A, B, F, G):
    """Photocentre semi-major axis [mas] from Thiele-Innes constants [mas]."""
    A, B, F, G = map(np.asarray, (A, B, F, G))
    u = 0.5 * (A**2 + B**2 + F**2 + G**2)
    v = A * G - B * F
    return np.sqrt(u + np.sqrt(np.clip(u**2 - v**2, 0, None)))


def mass_function(a0, parallax, period_days):
    """Astrometric mass function [Msun] assuming a dark companion."""
    a1_au = np.asarray(a0) / np.asarray(parallax)
    p_yr = np.asarray(period_days) / DAYS_PER_YEAR
    return a1_au**3 / p_yr**2


def companion_mass(f_m, m1):
    """Solve M2^3 = f (M1 + M2)^2 for M2 > 0 (vectorised Newton; unique positive root)."""
    f_m, m1 = np.broadcast_arrays(np.asarray(f_m, float), np.asarray(m1, float))
    # Upper bound on the root: if M2 >= M1 then (M1+M2)^2 <= 4 M2^2, so M2 <= 4f; hence
    # root <= max(M1, 4f). h(x) = x^3 - f(M1+x)^2 is convex for x > f/3 and the root
    # exceeds f, so Newton started above the root decreases monotonically onto it.
    m2 = np.maximum(m1, 4 * np.maximum(f_m, 0)) + 1e-6
    for _ in range(60):
        g = m2**3 - f_m * (m1 + m2) ** 2
        dg = 3 * m2**2 - 2 * f_m * (m1 + m2)
        step = g / dg
        m2 = m2 - step
        if np.all(np.abs(step) < 1e-10 * np.maximum(m2, 1e-6)):
            break
    return m2


def sample_companion_mass(row: pd.Series, m1, m1_err=0.0, n=20000, seed=0):
    """Monte Carlo M2 using the full NSS covariance (parallax, A, B, F, G, period) and M1 ~ N(m1, m1_err).

    Note: when g_thiele_innes is not fitted (pseudo-circular orbits) this is not handled.
    """
    names, cov = covariance(row)
    need = ["parallax", "a_thiele_innes", "b_thiele_innes", "f_thiele_innes", "g_thiele_innes", "period"]
    missing = [p for p in need if p not in names]
    if missing:
        raise ValueError(f"parameters not fitted: {missing}")
    idx = [names.index(p) for p in need]
    mean = np.array([row[p] for p in need], dtype=float)
    rng = np.random.default_rng(seed)
    s = rng.multivariate_normal(mean, cov[np.ix_(idx, idx)], size=n)
    plx, A, B, F, G, P = s.T
    a0 = a0_mas(A, B, F, G)
    fm = mass_function(a0, plx, P)
    m1s = np.clip(rng.normal(m1, m1_err, n), 0.05, None)
    return {"a0_mas": a0, "f_m": fm, "m2": companion_mass(fm, m1s), "parallax": plx, "period": P}
