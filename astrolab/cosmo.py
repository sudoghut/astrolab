"""Background cosmology for BAO, supernova and compressed-CMB likelihoods (flat w0waCDM).

Units: distances in Mpc, H0 in km/s/Mpc, densities as omega = Omega h^2.
Physics follows DESI DR2 (arXiv:2503.14738, Sec. IV): photons at T_CMB = 2.7255 K,
N_eff = 3.044 with one massive neutrino (default 0.06 eV) and two massless ones, dark energy with
the CPL equation of state w(a) = w0 + wa (1 - a).

Naming: ``ombh2`` = omega_b, ``omch2`` = omega_c, ``ombc`` = omega_b + omega_c (no neutrinos),
``omm`` = omega_b + omega_c + omega_nu. The r_d fitting formula takes ``ombc``; never feed it
``omm``.

Used by studies/002-m01-desi-bao-evolving-dark-energy (design plan 010).
"""
from __future__ import annotations

from functools import lru_cache

import numpy as np
from scipy import integrate

C_KMS = 299792.458
T_CMB = 2.7255
NEFF = 3.044
KB_EV = 8.617333262e-5
# omega_gamma = (pi^2/15) (k T)^4 / (hbar^3 c^5) / rho_crit,100 ; 2.4728e-5 at T = 2.7255 K
OMEGA_GAMMA = 2.4728e-5 * (T_CMB / 2.7255) ** 4
# one massless neutrino species relative to photons, scaled so that three species give N_eff
NU_REL = 7.0 / 8.0 * (4.0 / 11.0) ** (4.0 / 3.0) * (NEFF / 3.0)
# Hu & Sugiyama (1996) z_* is calibrated by a constant factor on theta_* (see theta_star).
THETA_REF = {"ombh2": 0.022383, "omch2": 0.12011, "H0": 67.32, "theta100": 1.041085}


def omega_nu_today(mnu: float = 0.06) -> float:
    """omega_nu of the massive species today, with the 93.14 eV convention used by DESI (Eq. 7)."""
    return mnu / 93.14


def _fd_ratio(y: float) -> float:
    """Energy density of one massive neutrino species over that of a massless one, y = m / T_nu."""
    num = integrate.quad(lambda x: x * x * np.sqrt(x * x + y * y) / (np.exp(x) + 1.0),
                         0.0, 60.0 + y, limit=200)[0]
    return num / (7.0 * np.pi ** 4 / 120.0)


@lru_cache(maxsize=8)
def _nu_table(mnu: float):
    """log(a) grid and the massive-neutrino density ratio on it."""
    tnu0 = KB_EV * T_CMB * (4.0 / 11.0) ** (1.0 / 3.0)
    loga = np.linspace(np.log(1e-9), 0.0, 400)
    ratio = np.array([_fd_ratio(mnu / (tnu0 / np.exp(la))) for la in loga]) if mnu > 0 else np.ones_like(loga)
    return loga, ratio


class Background:
    """Flat w0waCDM background with photons, neutrinos (one massive) and CPL dark energy."""

    def __init__(self, H0: float, ombh2: float, omch2: float, w0: float = -1.0, wa: float = 0.0,
                 mnu: float = 0.06):
        self.H0, self.h = H0, H0 / 100.0
        self.ombh2, self.omch2, self.w0, self.wa, self.mnu = ombh2, omch2, w0, wa, mnu
        self.ombc = ombh2 + omch2
        self._loga, ratio = _nu_table(mnu)
        # massive species: density relative to photons at fixed a, times a^-4
        self._nu_mass_rel = NU_REL * ratio
        self.omnu = OMEGA_GAMMA * NU_REL * ratio[-1]            # today, from the integral
        self.omm = self.ombc + self.omnu
        self.omrad = OMEGA_GAMMA * (1.0 + 2.0 * NU_REL)          # photons + two massless species
        self.omde = self.h ** 2 - self.ombc - self.omrad - self.omnu
        self.Om = self.omm / self.h ** 2

    def E(self, a):
        """H(a) / H0."""
        a = np.asarray(a, dtype=float)
        nu = OMEGA_GAMMA * np.interp(np.log(a), self._loga, self._nu_mass_rel) / a ** 4
        de = self.omde * a ** (-3.0 * (1.0 + self.w0 + self.wa)) * np.exp(-3.0 * self.wa * (1.0 - a))
        return np.sqrt(self.ombc / a ** 3 + self.omrad / a ** 4 + nu + de) / self.h

    def comoving(self, z) -> np.ndarray:
        """Line-of-sight comoving distance D_C = D_M (flat) in Mpc; z scalar or array.

        Integrates c/H over x = ln(1+z) on a fixed grid (composite Simpson on 2048 intervals per
        unit of x; relative accuracy ~1e-9 for smooth E), then interpolates with a cubic
        Hermite rule on the cumulative integral."""
        z = np.atleast_1d(np.asarray(z, dtype=float))
        xmax = float(np.log1p(z.max())) if z.size else 0.0
        n = max(64, int(np.ceil(xmax * 2048 / 2)) * 2)
        x = np.linspace(0.0, xmax, n + 1)
        f = np.exp(x) / self.E(np.exp(-x))                 # dz/E = e^x dx / E
        cum = np.concatenate([[0.0], np.cumsum((f[:-1] + f[1:]) * 0.5 * np.diff(x))])
        # Richardson-corrected trapezoid (end correction) equals Simpson accuracy on the grid
        dfdx = np.gradient(f, x)
        cum = cum - (np.diff(x)[0] ** 2 / 12.0) * (dfdx - dfdx[0])
        xz = np.log1p(z)
        return C_KMS / self.H0 * np.interp(xz, x, cum)

    def DM(self, z):
        return self.comoving(z)

    def DH(self, z):
        z = np.asarray(z, dtype=float)
        return C_KMS / (self.H0 * self.E(1.0 / (1.0 + z)))

    def DV(self, z):
        z = np.asarray(z, dtype=float)
        return (z * self.DM(z) ** 2 * self.DH(z)) ** (1.0 / 3.0)

    def DL(self, z, zhel=None):
        z = np.asarray(z, dtype=float)
        zh = z if zhel is None else np.asarray(zhel, dtype=float)
        return (1.0 + zh) * self.DM(z)

    def rd(self) -> float:
        """Sound horizon at the drag epoch, Aubourg et al. 2015 (arXiv:1411.1074) Eq. 16 [Mpc]."""
        return rd_aubourg(self.ombc, self.ombh2, omega_nu_today(self.mnu))

    def zstar(self) -> float:
        """Photon decoupling redshift, Hu & Sugiyama 1996 fitting formula."""
        ob, om = self.ombh2, self.ombc + omega_nu_today(self.mnu)
        g1 = 0.0783 * ob ** -0.238 / (1.0 + 39.5 * ob ** 0.763)
        g2 = 0.560 / (1.0 + 21.1 * ob ** 1.81)
        return 1048.0 * (1.0 + 0.00124 * ob ** -0.738) * (1.0 + g1 * om ** g2)

    def rs(self, z: float) -> float:
        """Comoving sound horizon at redshift z [Mpc]: integral of c_s da / (a^2 H) over
        ln a from 1e-8 to 1/(1+z) on a fixed grid (trapezoid with end correction)."""
        r = 3.0 * self.ombh2 / (4.0 * OMEGA_GAMMA)
        la = np.linspace(np.log(1e-8), -np.log1p(z), 4097)
        a = np.exp(la)
        f = C_KMS / np.sqrt(3.0 * (1.0 + r * a)) / (a * self.H0 * self.E(a))   # da = a dln a
        h = la[1] - la[0]
        dfdx = np.gradient(f, la)
        # below a = 1e-8 the universe is radiation dominated (all neutrinos relativistic, R ~ 0):
        # r_s(a0) = c a0 / (sqrt(3) H0 sqrt(omega_r) / h)
        omr_all = OMEGA_GAMMA * (1.0 + 3.0 * NU_REL)
        head = C_KMS * 1e-8 / (np.sqrt(3.0) * self.H0 * np.sqrt(omr_all) / self.h)
        return float(head + np.trapz(f, la) - h * h / 12.0 * (dfdx[-1] - dfdx[0]))

    def theta_star_raw(self) -> float:
        """r_s(z_*) / D_M(z_*) with the Hu & Sugiyama z_* (uncalibrated)."""
        zs = self.zstar()
        return self.rs(zs) / float(self.DM(zs)[0])

    def theta_star(self, K: float | None = None) -> float:
        """theta_* calibrated by the constant K (default: theta_calibration())."""
        return (theta_calibration() if K is None else K) * self.theta_star_raw()


def rd_aubourg(ombc: float, ombh2: float, omnu: float) -> float:
    """Aubourg et al. 2015 Eq. 16: r_d = 55.154 exp[-72.3 (omega_nu + 0.0006)^2] /
    (omega_cb^0.25351 omega_b^0.12807) Mpc (accurate to 0.021% for N_eff = 3.046)."""
    return 55.154 * np.exp(-72.3 * (omnu + 0.0006) ** 2) / (ombc ** 0.25351 * ombh2 ** 0.12807)


@lru_cache(maxsize=1)
def theta_calibration() -> float:
    """Constant K with 100 K theta_raw = 1.041085 at the Planck 2018 best fit (Table 1, Plik)."""
    ref = Background(THETA_REF["H0"], THETA_REF["ombh2"], THETA_REF["omch2"])
    return THETA_REF["theta100"] / 100.0 / ref.theta_star_raw()


def bao_late(Om: float, hrd: float, z, w0: float = -1.0, wa: float = 0.0):
    """BAO-only distances in units of r_d for a late-time universe (matter + CPL dark energy,
    radiation neglected, neutrinos counted as matter). Returns (DM/rd, DH/rd, DV/rd); hrd in Mpc."""
    z = np.atleast_1d(np.asarray(z, dtype=float))

    def E(x):
        a = 1.0 / (1.0 + x)
        de = (1.0 - Om) * a ** (-3.0 * (1.0 + w0 + wa)) * np.exp(-3.0 * wa * (1.0 - a))
        return np.sqrt(Om / a ** 3 + de)

    scale = C_KMS / 100.0 / hrd
    dm = scale * np.array([integrate.quad(lambda x: 1.0 / E(x), 0.0, zz, epsrel=1e-9)[0] for zz in z])
    dh = scale / E(z)
    dv = (z * dm ** 2 * dh) ** (1.0 / 3.0)
    return dm, dh, dv
