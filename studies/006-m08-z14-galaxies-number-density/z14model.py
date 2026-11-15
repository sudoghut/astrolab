"""Halo model for the z ~ 14 UV luminosity function (README section 4).

Pure functions; every tunable value is passed in as an argument (AGENTS.md section 2).
Units: Mpc and M_sun without h; k in Mpc^-1.
"""
import numpy as np
from scipy import integrate, optimize, special, stats

RHO_CRIT_H2 = 2.775e11          # M_sun Mpc^-3 per h^2
DELTA_C = 1.686
ST = {"A": 0.3222, "a": 0.707, "p": 0.3}
REED_C = 1.08
K_UV_SALPETER = 1.15e-28        # M_sun/yr per erg/s/Hz (Madau & Dickinson 2014, eq. 10)
CHABRIER_FACTOR = 0.63          # SFR_Chabrier = 0.63 SFR_Salpeter (MD14)
PC_CM = 3.0856775814913673e18
AB_ZP = 2.5 * np.log10(4.0 * np.pi * (10.0 * PC_CM) ** 2) - 48.60   # M_UV = AB_ZP - 2.5 log10 L_nu
YR_PER_GYR = 1.0e9


# ------------------------------------------------------------ cosmology ----

def cosmo_params(cosmo):
    """Numbers used here from an astropy cosmology (Planck18)."""
    meta = getattr(cosmo, "meta", {}) or {}
    return {"h": cosmo.H0.value / 100.0, "Om": float(cosmo.Om0), "Ob": float(cosmo.Ob0),
            "Tcmb": float(cosmo.Tcmb0.value), "ns": float(meta.get("n", 0.9665)),
            "sigma8": float(meta.get("sigma8", 0.8102))}


def eisenstein_hu(k, c):
    """Eisenstein & Hu 1998 transfer function with baryon oscillations (eqs. 2-24); k in Mpc^-1."""
    k = np.asarray(k, dtype=float)
    h, Om, Ob = c["h"], c["Om"], c["Ob"]
    Oc = Om - Ob
    theta = c["Tcmb"] / 2.7
    wm, wb = Om * h * h, Ob * h * h
    fb, fc = Ob / Om, Oc / Om
    z_eq = 2.50e4 * wm * theta ** -4                                   # eq. 2
    k_eq = 7.46e-2 * wm * theta ** -2                                  # eq. 3
    b1 = 0.313 * wm ** -0.419 * (1 + 0.607 * wm ** 0.674)              # eq. 4
    b2 = 0.238 * wm ** 0.223
    z_d = 1291 * wm ** 0.251 / (1 + 0.659 * wm ** 0.828) * (1 + b1 * wb ** b2)

    def R(z):                                                          # eq. 5
        return 31.5 * wb * theta ** -4 * (z / 1.0e3) ** -1

    R_d, R_eq = R(z_d), R(z_eq)
    s = (2.0 / (3.0 * k_eq) * np.sqrt(6.0 / R_eq)                       # eq. 6
         * np.log((np.sqrt(1 + R_d) + np.sqrt(R_d + R_eq)) / (1 + np.sqrt(R_eq))))
    k_silk = 1.6 * wb ** 0.52 * wm ** 0.73 * (1 + (10.4 * wm) ** -0.95)  # eq. 7
    q = k / (13.41 * k_eq)                                             # eq. 10
    a1 = (46.9 * wm) ** 0.670 * (1 + (32.1 * wm) ** -0.532)            # eq. 11
    a2 = (12.0 * wm) ** 0.424 * (1 + (45.0 * wm) ** -0.582)
    alpha_c = a1 ** -fb * a2 ** (-fb ** 3)
    bb1 = 0.944 / (1 + (458 * wm) ** -0.708)                           # eq. 12
    bb2 = (0.395 * wm) ** -0.0266
    beta_c = 1.0 / (1 + bb1 * (fc ** bb2 - 1))

    def t0(alpha, beta):                                               # eqs. 19-20
        L = np.log(np.e + 1.8 * beta * q)
        C = 14.2 / alpha + 386.0 / (1 + 69.9 * q ** 1.08)
        return L / (L + C * q * q)

    f = 1.0 / (1 + (k * s / 5.4) ** 4)                                 # eq. 18
    T_c = f * t0(1.0, beta_c) + (1 - f) * t0(alpha_c, beta_c)          # eq. 17
    y = (1 + z_eq) / (1 + z_d)                                         # eq. 15
    G = y * (-6 * np.sqrt(1 + y) + (2 + 3 * y) * np.log((np.sqrt(1 + y) + 1) / (np.sqrt(1 + y) - 1)))
    alpha_b = 2.07 * k_eq * s * (1 + R_d) ** -0.75 * G                 # eq. 14
    beta_node = 8.41 * wm ** 0.435                                     # eq. 23
    ks = k * s
    with np.errstate(divide="ignore", invalid="ignore"):
        s_tilde = s / (1 + (beta_node / ks) ** 3) ** (1.0 / 3.0)       # eq. 22
    beta_b = 0.5 + fb + (3 - 2 * fb) * np.sqrt((17.2 * wm) ** 2 + 1)   # eq. 24
    x = k * s_tilde
    j0 = np.where(x > 1e-8, np.sin(x) / np.where(x > 1e-8, x, 1.0), 1.0)
    with np.errstate(divide="ignore", over="ignore"):
        T_b = (t0(1.0, 1.0) / (1 + (ks / 5.2) ** 2)
               + alpha_b / (1 + (beta_b / ks) ** 3) * np.exp(-(k / k_silk) ** 1.4)) * j0   # eq. 21
    return fb * T_b + fc * T_c                                         # eq. 16


def growth(z, c):
    """Linear growth factor D(z)/D(0) for flat LCDM (integral form)."""
    Om = c["Om"]
    Ol = 1.0 - Om

    def E(a):
        return np.sqrt(Om / a ** 3 + Ol)

    def D_un(a):
        val, _ = integrate.quad(lambda x: 1.0 / (x * E(x)) ** 3, 0.0, a, limit=200)
        return 2.5 * Om * E(a) * val

    z = np.atleast_1d(np.asarray(z, dtype=float))
    d0 = D_un(1.0)
    return np.array([D_un(1.0 / (1 + zi)) / d0 for zi in z])


def tophat(x):
    x = np.asarray(x, dtype=float)
    small = x < 1e-3
    xs = np.where(small, 1.0, x)
    w = 3.0 * (np.sin(xs) - xs * np.cos(xs)) / xs ** 3
    return np.where(small, 1.0 - x * x / 10.0, w)


class LinearPower:
    """P(k) normalised to sigma8 at z = 0; sigma(M) at z = 0."""

    def __init__(self, c, n_k=4096, k_min=1e-4, k_max=1e3):
        self.c = c
        self.lnk = np.linspace(np.log(k_min), np.log(k_max), n_k)
        self.k = np.exp(self.lnk)
        T = eisenstein_hu(self.k, c)
        self.p_un = self.k ** c["ns"] * T * T
        r8 = 8.0 / c["h"]
        self.norm = c["sigma8"] ** 2 / self._sig2(r8, self.p_un)

    def _sig2(self, R, p):
        integrand = self.k ** 3 * p * tophat(self.k * R) ** 2 / (2 * np.pi ** 2)
        return np.trapz(integrand, self.lnk)

    def sigma_R(self, R):
        R = np.atleast_1d(R)
        return np.sqrt(np.array([self._sig2(r, self.p_un) for r in R]) * self.norm)

    def rho_m(self):
        return self.c["Om"] * RHO_CRIT_H2 * self.c["h"] ** 2

    def sigma_M(self, M):
        R = (3.0 * np.asarray(M) / (4.0 * np.pi * self.rho_m())) ** (1.0 / 3.0)
        return self.sigma_R(R)


# --------------------------------------------------------- mass functions ----

def f_st(sigma):
    A, a, p = ST["A"], ST["a"], ST["p"]
    nu2 = (DELTA_C / sigma) ** 2
    return A * np.sqrt(2 * a / np.pi) * (1 + (1.0 / (a * nu2)) ** p) * np.sqrt(nu2) * np.exp(-a * nu2 / 2)


def f_reed07(sigma, n_eff):
    """Reed et al. 2007 eq. 11."""
    A, a, p = ST["A"], ST["a"], ST["p"]
    ls = np.log(1.0 / sigma)
    G1 = np.exp(-(ls - 0.4) ** 2 / (2 * 0.6 ** 2))
    G2 = np.exp(-(ls - 0.75) ** 2 / (2 * 0.2 ** 2))
    x = DELTA_C / sigma
    return (A * np.sqrt(2 * a / np.pi) * (1 + (sigma ** 2 / (a * DELTA_C ** 2)) ** p + 0.6 * G1 + 0.4 * G2)
            * x * np.exp(-REED_C * a * DELTA_C ** 2 / (2 * sigma ** 2) - 0.03 / (n_eff + 3) ** 2 * x ** 0.6))


def dndlnm(lnM, sig0, D, rho_m, hmf):
    """dn/dlnM [Mpc^-3] on the lnM grid, given sigma(M, z=0) and the growth factor D."""
    sigma = sig0 * D
    dlnsig_dlnm = np.gradient(np.log(sigma), lnM)
    if hmf == "st":
        f = f_st(sigma)
    elif hmf == "reed07":
        n_eff = 6.0 * (-dlnsig_dlnm) - 3.0                       # Reed eq. 13
        f = f_reed07(sigma, n_eff)
    else:
        raise ValueError(f"unknown hmf {hmf!r}")
    return rho_m / np.exp(lnM) * f * np.abs(dlnsig_dlnm)


def st_normalisation(lo=-20.0, hi=3.0, n=20001):
    x = np.linspace(lo, hi, n)                                   # x = ln sigma^-1
    return float(np.trapz(f_st(np.exp(-x)), x))


# --------------------------------------------------------------- galaxies ----

def mdot_halo(M, z, c, kind):
    """Total (dark matter) halo growth rate [M_sun/yr]."""
    Om = c["Om"]
    E = np.sqrt(Om * (1 + z) ** 3 + 1 - Om)
    if kind == "fakhouri_mean":
        return 46.1 * (M / 1e12) ** 1.1 * (1 + 1.11 * z) * E
    if kind == "fakhouri_median":
        return 25.3 * (M / 1e12) ** 1.1 * (1 + 1.65 * z) * E
    if kind == "dekel13":
        s = 0.030 * (0.82 / c["sigma8"]) / YR_PER_GYR
        return M * s * (1 + z) ** 2.5
    raise ValueError(f"unknown accretion {kind!r}")


def eps_dpl(M, theta):
    eps0, logm1, beta, gamma = theta
    x = M / 10.0 ** logm1
    return 2.0 * eps0 / (x ** -beta + x ** gamma)


def muv_median(M, z, c, theta, accretion, eps_floor_mass=None):
    """Median M_UV for halos of mass M at redshift z."""
    eps = eps_dpl(M, theta)
    if eps_floor_mass is not None:
        eps = np.where(M < eps_floor_mass, eps_dpl(np.asarray(eps_floor_mass), theta), eps)
    sfr = eps * (c["Ob"] / c["Om"]) * mdot_halo(M, z, c, accretion)
    k_uv = CHABRIER_FACTOR * K_UV_SALPETER
    lnu = np.maximum(sfr, 1e-300) / k_uv
    return AB_ZP - 2.5 * np.log10(lnu)


def lf_model(muv, lnM, hmf_vals, med, sigma):
    """phi(M_UV) = int dn/dlnM N(M_UV; med(M), sigma) dlnM."""
    muv = np.atleast_1d(muv)
    kern = stats.norm.pdf(muv[:, None], loc=med[None, :], scale=sigma)
    return np.trapz(hmf_vals[None, :] * kern, lnM, axis=1)


def schechter_mag(M, m_star, phi_star, alpha):
    x = 10.0 ** (0.4 * (m_star - M))
    return 0.4 * np.log(10) * phi_star * x ** (alpha + 1) * np.exp(-x)


# ------------------------------------------------------------ calibration ----

def calibrate(lnM, hmf_cal, z_cal, c, accretion, sigma_cal, lf, m_grid,
              start=(0.1, 11.5, 1.0, 0.5)):
    """Deconvolved abundance matching: fit the DPL efficiency (README section 4, step 4)."""
    M = np.exp(lnM)
    target = np.log10(schechter_mag(m_grid, lf["m_star"], lf["phi_star"], lf["alpha"]))

    def resid(theta):
        med = muv_median(M, z_cal, c, theta, accretion)
        phi = lf_model(m_grid, lnM, hmf_cal, med, sigma_cal)
        return np.log10(np.maximum(phi, 1e-300)) - target

    lo = [1e-6, 9.0, 0.0, 0.0]
    hi = [1.0, 13.0, 3.0, 3.0]
    res = optimize.least_squares(resid, np.array(start), bounds=(lo, hi), loss="linear",
                                 ftol=1e-10, xtol=1e-10, gtol=1e-10, max_nfev=2000)
    r = resid(res.x)
    at_bound = [bool(np.isclose(v, l) or np.isclose(v, h)) for v, l, h in zip(res.x, lo, hi)]
    return {"theta": res.x.tolist(), "rms": float(np.sqrt(np.mean(r ** 2))), "success": bool(res.success),
            "at_bound": at_bound, "residuals": r.tolist()}


def median_shape(M, med, bright=-22.0, faint=-17.0):
    """Peak (brightest median) and the calibrated range on the rising branch."""
    i_peak = int(np.argmin(med))
    monotonic = i_peak == len(M) - 1
    rising = np.arange(i_peak + 1)
    ok = rising[med[rising] <= faint]
    m_lo = float(M[ok[0]]) if ok.size else None
    if monotonic:
        bright_ok = rising[med[rising] <= bright]
        m_hi = float(M[bright_ok[0]]) if bright_ok.size else float(M[-1])
    else:
        m_hi = float(M[i_peak])
    return {"m_peak": float(M[i_peak]), "brightest_median": float(med[i_peak]), "monotonic": monotonic,
            "m_cal_lo": m_lo, "m_cal_hi": m_hi}


# ------------------------------------------------------------- prediction ----

def bin_average(lnM, hmf_by_z, med_by_z, sigma, dvdz, m_lo, m_hi, n_m=21):
    """phi averaged over the magnitude bin and over z with dV/dz weights (README step 5)."""
    mg = np.linspace(m_lo, m_hi, n_m)
    per_z = np.array([np.trapz(lf_model(mg, lnM, h, md, sigma), mg) / (m_hi - m_lo)
                      for h, md in zip(hmf_by_z, med_by_z)])
    return float(np.trapz(per_z * dvdz, dx=1.0) / np.trapz(dvdz, dx=1.0)), per_z


# -------------------------------------------------------------- statistics ----

def gehrels(n, cl_lo=0.1587, cl_hi=0.8413):
    lo = 0.5 * stats.chi2.ppf(cl_lo, 2 * n) if n > 0 else 0.0
    hi = 0.5 * stats.chi2.ppf(cl_hi, 2 * n + 2)
    return float(lo), float(hi)


def poisson_tail(n, mu):
    """P(N >= n | mu)."""
    return float(special.gammainc(n, mu)) if n > 0 else 1.0
