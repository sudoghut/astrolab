"""Konietzka et al. 2024 (K24) damped-wave model of the Radcliffe Wave (README section 4.1).

Units: lengths in pc, velocities in km/s, frequencies in km s^-1 pc^-1 (74 km/s/kpc = 0.074).
No module-level state derives from run.py's PARAMS: every tunable is passed in as an argument.

Equations (K24 Methods, checked against arXiv:2402.12596v1):
  eq. 1  Phi(z, r) = 1/2 w0^2 exp[(r_sun - r)/r0] (z^2 - mu0^2 z^4)
  eq. 3  w(z_max, r) = pi/2 w0 exp[(r_sun - r)/(2 r0)] (1 - mu0^2 z_max^2)^0.5
                       / K( mu0 z_max (1 - mu0^2 z_max^2)^-0.5 )
         K's argument is the modulus k; scipy's ellipk takes the parameter m = k^2.
  eqs. 4-5 z and v_z; eq. 6 Lambda(s) = s/(p - gamma s); eq. 9 zeta(s) = -A/[1 + ((s - s0)/delta)^2]
  eq. 11 clouds:   ln L = -sum_i w_i [ d_i^2/(2 sigma^2) + ln(2 pi sigma^2) ]
  eq. 13 clusters: ln L = -1/2 sum_k w_k [ C(d_k/sigma)^2 + 3 ln(2 pi sigma^2) ],
         C(x) = (sum_n tanh(x_n^2))^0.5; outlier if any tanh(x_n^2) > tanh(3), i.e. |x_n| > sqrt(3).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field, replace

import numpy as np
from scipy.special import ellipk

R_SUN = 8400.0                     # pc (K24)
OMEGA0_ADOPTED = 0.074             # km/s/pc (74 km/s/kpc)
MU0_ADOPTED_KPC = 1.3              # kpc^-1
R0_ADOPTED = 3700.0                # pc
G_PC = 4.300917e-3                 # pc (km/s)^2 / Msun
PC_PER_KMS_MYR = 0.977792          # 1 pc / (km/s) in Myr

# Parameter vector (internal): lengths in pc, ln_delta = ln(delta/pc), ln_gamma = ln(gamma),
# ln_omega0 = ln(omega0 / (km/s/pc)), ln_mu0 = ln(mu0 / kpc^-1), r0 in pc.
NAMES = ("x0", "y0", "x1", "y1", "x2", "y2", "A", "p", "ln_delta", "s0", "ln_gamma", "phi",
         "w0t", "B", "ln_omega0", "ln_mu0", "r0")
IDX = {n: i for i, n in enumerate(NAMES)}
SHAPE_NAMES = ("x0", "y0", "x1", "y1", "x2", "y2", "A", "p", "ln_delta", "s0", "ln_gamma", "phi")

# Extended Data Table 1 (priors). Gaussian (mean, sd) on the internal parameter. Our readings
# (README 4.1): ln_mu0 ~ N(ln 1.3, 0.25) in kpc^-1; ln(omega0 km^-1 s pc) ~ N(-2.4, 0.17) as printed.
PRIOR_GAUSS = {
    "x0": (-850.0, 100.0), "y0": (-790.0, 100.0), "x1": (-255.0, 100.0), "y1": (23.0, 100.0),
    "x2": (313.0, 100.0), "y2": (1368.0, 100.0), "p": (4650.0, 300.0), "A": (215.0, 20.0),
    "ln_delta": (6.5, 0.1), "s0": (680.0, 200.0), "ln_gamma": (0.35, 0.07), "phi": (-0.09, 0.5),
    "ln_omega0": (-2.4, 0.17), "ln_mu0": (math.log(1.3), 0.25), "r0": (3659.0, 500.0),
}
W0T_PRIOR = (-math.pi / 2, math.pi / 2)
B_PRIOR = (0.0, 1.0)
# T8 broad priors, uniform in the physical parameter (README section 2, T8)
BROAD = {"omega0": (0.030, 0.150), "mu0_kpc": (0.3, 3.0), "r0": (1000.0, 10000.0)}

# Extended Data Table 2: median, +err, -err (16-84%) per column. delta and gamma are linear here.
K24_TABLE2 = {
    3: {"x0": (-853.13, 51.12, 57.35), "y0": (-797.19, 48.74, 48.78), "x1": (-276.15, 45.72, 47.33),
        "y1": (18.27, 89.0, 88.02), "x2": (289.05, 28.05, 27.1), "y2": (1386.24, 80.67, 79.49),
        "p": (4773.99, 189.15, 187.63), "A": (219.88, 18.34, 16.24), "delta": (797.78, 67.28, 62.43),
        "s0": (482.71, 113.81, 103.35), "gamma": (1.49, 0.07, 0.07), "phi": (-0.12, 0.13, 0.14)},
    4: {"x0": (-822.51, 49.83, 51.82), "y0": (-804.87, 64.26, 60.12), "x1": (-289.51, 49.9, 48.11),
        "y1": (42.29, 87.38, 85.05), "x2": (329.57, 49.93, 46.41), "y2": (1365.38, 93.43, 89.69),
        "p": (4752.21, 207.28, 198.8), "A": (216.52, 11.54, 10.95), "delta": (624.25, 60.19, 55.96),
        "s0": (673.18, 104.02, 103.13), "gamma": (1.4, 0.09, 0.07), "phi": (-0.23, 0.16, 0.16)},
    5: {"x0": (-833.83, 49.57, 57.1), "y0": (-826.53, 63.65, 61.06), "x1": (-284.02, 50.64, 50.65),
        "y1": (25.84, 88.24, 83.4), "x2": (317.16, 51.18, 45.58), "y2": (1377.48, 91.07, 96.67),
        "p": (4715.14, 216.07, 214.2), "A": (229.32, 13.23, 12.18), "delta": (649.14, 61.95, 56.19),
        "s0": (662.89, 112.13, 107.4), "gamma": (1.4, 0.1, 0.08), "phi": (0.01, 0.25, 0.23),
        "w0t": (-0.38, 0.19, 0.17), "B": (0.84, 0.07, 0.06)},
    6: {"x0": (-852.99, 51.66, 54.91), "y0": (-807.94, 54.01, 50.29), "x1": (-275.13, 43.85, 46.1),
        "y1": (30.48, 84.66, 86.94), "x2": (293.84, 30.25, 26.96), "y2": (1387.37, 85.95, 75.5),
        "p": (4779.9, 195.49, 192.26), "A": (218.64, 13.81, 11.41), "delta": (740.01, 58.78, 55.14),
        "s0": (544.99, 89.88, 100.53), "gamma": (1.46, 0.08, 0.07), "phi": (-0.15, 0.13, 0.13)},
    7: {"x0": (-844.31, 49.13, 54.15), "y0": (-797.55, 49.32, 54.25), "x1": (-276.51, 42.69, 42.98),
        "y1": (29.03, 81.8, 81.52), "x2": (291.68, 32.72, 27.41), "y2": (1379.77, 91.24, 73.37),
        "p": (4749.05, 191.12, 182.03), "A": (222.92, 13.32, 12.5), "delta": (738.57, 59.33, 52.89),
        "s0": (517.02, 99.91, 91.41), "gamma": (1.46, 0.09, 0.07), "phi": (-0.14, 0.13, 0.14),
        "omega0": (0.067713, 0.007677, 0.007111), "mu0_kpc": (1.377, 0.249, 0.247),
        "r0": (3563.32, 513.7, 500.43)},
}


def k24_vector(col: int, **over) -> np.ndarray:
    """Full internal parameter vector at K24's Extended Data Table 2 medians of a column."""
    t = K24_TABLE2[col]
    v = default_vector()
    for n in ("x0", "y0", "x1", "y1", "x2", "y2", "A", "p", "s0", "phi"):
        v[IDX[n]] = t[n][0]
    v[IDX["ln_delta"]] = math.log(t["delta"][0])
    v[IDX["ln_gamma"]] = math.log(t["gamma"][0])
    if "w0t" in t:
        v[IDX["w0t"]] = t["w0t"][0]
        v[IDX["B"]] = t["B"][0]
    if "omega0" in t:
        v[IDX["ln_omega0"]] = math.log(t["omega0"][0])
        v[IDX["ln_mu0"]] = math.log(t["mu0_kpc"][0])
        v[IDX["r0"]] = t["r0"][0]
    for k, val in over.items():
        v[IDX[k]] = val
    return v


def default_vector() -> np.ndarray:
    v = np.zeros(len(NAMES))
    v[IDX["B"]] = 1.0
    v[IDX["ln_omega0"]] = math.log(OMEGA0_ADOPTED)
    v[IDX["ln_mu0"]] = math.log(MU0_ADOPTED_KPC)
    v[IDX["r0"]] = R0_ADOPTED
    return v


def physical(v: np.ndarray) -> dict:
    """Readable values: delta, gamma, omega0 (km/s/kpc), mu0 (kpc^-1) instead of their logs."""
    d = {n: float(v[IDX[n]]) for n in NAMES}
    d["delta"] = math.exp(d.pop("ln_delta"))
    d["gamma"] = math.exp(d.pop("ln_gamma"))
    d["omega0_kms_kpc"] = 1000.0 * math.exp(d.pop("ln_omega0"))
    d["mu0_kpc"] = math.exp(d.pop("ln_mu0"))
    return d


# ---------------------------------------------------------------------------------------------
# Frequency (eq. 3) and the Sun's vertical period

def omega_eq3(zmax, r, omega0, mu0_pc, r0):
    """Anharmonic angular frequency (km/s/pc). NaN where mu0 z_max >= 1/sqrt(2) (unbound)."""
    zmax = np.asarray(zmax, float)
    a = (mu0_pc * zmax) ** 2
    with np.errstate(invalid="ignore", divide="ignore"):
        m = a / (1.0 - a)                               # k^2, k = mu0 zmax / sqrt(1 - mu0^2 zmax^2)
        w = (0.5 * math.pi) * omega0 * np.exp((R_SUN - np.asarray(r, float)) / (2.0 * r0)) \
            * np.sqrt(1.0 - a) / ellipk(m)
    return np.where(a < 0.5, w, np.nan)


def sun_zmax(vz, omega0, mu0_pc):
    """Height reached by a body with vertical velocity vz at z = 0, r = r_sun (energy conservation)."""
    disc = 1.0 - 4.0 * (mu0_pc * vz / omega0) ** 2
    if disc <= 0:
        return float("nan")
    return math.sqrt((1.0 - math.sqrt(disc)) / (2.0 * mu0_pc ** 2))


def sun_period_myr(omega0, mu0_pc, r0, vz_sun=7.8):
    zm = sun_zmax(vz_sun, omega0, mu0_pc)
    w = float(omega_eq3(zm, R_SUN, omega0, mu0_pc, r0))
    return 2.0 * math.pi / w * PC_PER_KMS_MYR


def rho0(omega0):
    """Midplane density omega0^2/(4 pi G) in Msun/pc^3 (omega0 in km/s/pc)."""
    return omega0 ** 2 / (4.0 * math.pi * G_PC)


# ---------------------------------------------------------------------------------------------
# Baseline curve and model on the grid

@dataclass
class Grid:
    n: int = 2000
    u_min: float = -0.2
    u_max: float = 1.4

    def __post_init__(self):
        self.u = np.linspace(self.u_min, self.u_max, self.n)


def chord_u1(v):
    p0 = np.array([v[IDX["x0"]], v[IDX["y0"]]])
    p1 = np.array([v[IDX["x1"]], v[IDX["y1"]]])
    p2 = np.array([v[IDX["x2"]], v[IDX["y2"]]])
    d01, d12 = np.linalg.norm(p1 - p0), np.linalg.norm(p2 - p1)
    return float(d01 / (d01 + d12))


# Baseline options of README 4.10 (R-CONV). The internal mode strings flow through every function that
# takes `u1_mode`: "half" (L, the formal curve), "chord" (C, variant 10), "y_of_x" (Y), "x_of_y" (X).
BASELINE_MODE = {"L": "half", "C": "chord", "Y": "y_of_x", "X": "x_of_y"}
CONV_BASELINES = ("L", "C", "Y", "X")
CONV_SIGMAS = ("F", "P")          # F: sigma fixed (47 pc); P: sigma^2 = 0.5 std(d^2) per evaluation
CONV_WEIGHTS = ("W", "R")         # W: fixed at K24 column-(6) medians; R: recomputed per evaluation


def convention(index: int) -> dict:
    """README 4.10: index = baseline*4 + sigma*2 + weights, options numbered in the listed order."""
    index = int(index)
    if not 0 <= index < 16:
        raise ValueError(f"convention index {index} outside 0..15")
    b, s, w = index // 4, (index // 2) % 2, index % 2
    name = f"{CONV_BASELINES[b]}-{CONV_SIGMAS[s]}-{CONV_WEIGHTS[w]}"
    return {"index": index, "name": name, "baseline": CONV_BASELINES[b], "sigma": CONV_SIGMAS[s],
            "weights": CONV_WEIGHTS[w], "u1_mode": BASELINE_MODE[CONV_BASELINES[b]],
            "sigma_mode": "per_eval" if s else "fixed", "weights_mode": "recompute" if w else "fixed",
            "n_factors_differing": int(b != 0) + int(s != 0) + int(w != 0)}


def _baseline_function(v, grid: Grid, mode: str):
    """README 4.10 Y / X: the dependent coordinate as the quadratic (Lagrange) function of the other one
    through the three anchors. The independent coordinate runs linearly in the grid parameter, a(t) = a0 +
    t (a2 - a0) for t in [u_min, u_max] (the formal extent: 0.2 of the anchor span before anchor 0, 0.4
    after anchor 2). Needs a0 < a1 < a2 or a0 > a1 > a2, else None (zero likelihood). s is the x-y arc
    length from anchor 0 (t = 0)."""
    X = (v[IDX["x0"]], v[IDX["x1"]], v[IDX["x2"]])
    Y = (v[IDX["y0"]], v[IDX["y1"]], v[IDX["y2"]])
    a, b = (X, Y) if mode == "y_of_x" else (Y, X)
    a0, a1, a2 = a
    if not ((a0 < a1 < a2) or (a0 > a1 > a2)):
        return None
    t = grid.u
    q = a0 + t * (a2 - a0)
    d0, d1, d2 = (a0 - a1) * (a0 - a2), (a1 - a0) * (a1 - a2), (a2 - a0) * (a2 - a1)
    f = b[0] * (q - a1) * (q - a2) / d0 + b[1] * (q - a0) * (q - a2) / d1 + b[2] * (q - a0) * (q - a1) / d2
    df = b[0] * (2.0 * q - a1 - a2) / d0 + b[1] * (2.0 * q - a0 - a2) / d1 + b[2] * (2.0 * q - a0 - a1) / d2
    speed = abs(a2 - a0) * np.sqrt(1.0 + df * df)
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (speed[1:] + speed[:-1]) * np.diff(t))])
    s = cum - np.interp(0.0, t, cum)                  # s = 0 at anchor 0, negative before it
    return (q, f, s) if mode == "y_of_x" else (f, q, s)


def baseline(v, grid: Grid, u1_mode: str = "half"):
    """Quadratic Lagrange curve through the anchors at u = 0, u1, 1 ("half": u1 = 0.5; "chord": the
    chord-length u1), or y(x) / x(y) for "y_of_x" / "x_of_y" (README 4.10); returns x, y, s on the grid."""
    if u1_mode in ("y_of_x", "x_of_y"):
        return _baseline_function(v, grid, u1_mode)
    if u1_mode not in ("half", "chord"):
        raise ValueError(f"unknown baseline mode {u1_mode!r}")
    u = grid.u
    u1 = 0.5 if u1_mode == "half" else chord_u1(v)
    if not (0.0 < u1 < 1.0):
        return None
    l0 = (u - u1) * (u - 1.0) / u1
    l1 = u * (u - 1.0) / (u1 * (u1 - 1.0))
    l2 = u * (u - u1) / (1.0 - u1)
    d0 = (2.0 * u - u1 - 1.0) / u1
    d1 = (2.0 * u - 1.0) / (u1 * (u1 - 1.0))
    d2 = (2.0 * u - u1) / (1.0 - u1)
    X = np.array([v[IDX["x0"]], v[IDX["x1"]], v[IDX["x2"]]])
    Y = np.array([v[IDX["y0"]], v[IDX["y1"]], v[IDX["y2"]]])
    x = l0 * X[0] + l1 * X[1] + l2 * X[2]
    y = l0 * Y[0] + l1 * Y[1] + l2 * Y[2]
    speed = np.hypot(d0 * X[0] + d1 * X[1] + d2 * X[2], d0 * Y[0] + d1 * Y[1] + d2 * Y[2])
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (speed[1:] + speed[:-1]) * np.diff(u))])
    s = cum - np.interp(0.0, u, cum)                  # s = 0 at u = 0, negative for u < 0
    return x, y, s


def wave_on_grid(v, grid: Grid, u1_mode: str = "half"):
    """Model curve: dict with x, y, z, vz, omega, s, Lambda, zeta, valid mask; None if unusable.

    Grid points with p - gamma s <= 0 are excluded (valid False). Unbound (mu0 z_max >= 1/sqrt 2)
    on any valid point -> None (zero likelihood, README 4.1)."""
    if not np.all(np.isfinite(v)) or np.any(np.abs(v[[IDX["ln_delta"], IDX["ln_gamma"], IDX["ln_omega0"],
                                                       IDX["ln_mu0"]]]) > 30.0):
        return None
    b = baseline(v, grid, u1_mode)
    if b is None:
        return None
    x, y, s = b
    p, gamma = v[IDX["p"]], math.exp(v[IDX["ln_gamma"]])
    den = p - gamma * s
    valid = den > 0
    if valid.sum() < 3:
        return None
    lam = np.where(valid, s / np.where(valid, den, 1.0), np.nan)
    A, s0, delta = v[IDX["A"]], v[IDX["s0"]], math.exp(v[IDX["ln_delta"]])
    zeta = -A / (1.0 + ((s - s0) / delta) ** 2)
    omega0 = math.exp(v[IDX["ln_omega0"]])
    mu0 = math.exp(v[IDX["ln_mu0"]]) * 1e-3
    r = np.hypot(R_SUN - x, y)
    om = omega_eq3(np.abs(zeta), r, omega0, mu0, v[IDX["r0"]])
    if np.any(np.isnan(om[valid])):
        return None
    theta = 2.0 * math.pi * lam + v[IDX["phi"]]
    w0t, B = v[IDX["w0t"]], v[IDX["B"]]
    z = zeta * (B * np.sin(w0t + theta) + (1.0 - B) * np.sin(-w0t + theta))
    vz = zeta * om * (B * np.cos(w0t + theta) - (1.0 - B) * np.cos(-w0t + theta))
    return {"x": x, "y": y, "z": z, "vz": vz, "omega": om, "s": s, "Lambda": lam, "zeta": zeta,
            "valid": valid, "omega0": omega0}


def closest(D, M):
    """Index (into M's rows) of the closest row of M for each row of D (Euclidean)."""
    # |D - M|^2 = |D|^2 + (|M|^2 - 2 D.M); the first term does not change the argmin, and the
    # second is one matrix product with an augmented column.
    Ma = np.column_stack([-2.0 * M, (M * M).sum(1)])
    Da = np.column_stack([D, np.ones(len(D))])
    if len(D) > CLOSEST_CHUNK:          # large synthetic tests only (data and mocks have < 200 rows)
        return np.concatenate([np.argmin(Da[i:i + CLOSEST_CHUNK] @ Ma.T, axis=1)
                               for i in range(0, len(D), CLOSEST_CHUNK)])
    return np.argmin(Da @ Ma.T, axis=1)


CLOSEST_CHUNK = 5000


def kde_weights(s, bandwidth):
    """Inverse Gaussian-kernel density in s, normalised to sum to len(s); ones if bandwidth <= 0."""
    s = np.asarray(s, float)
    n = len(s)
    if n == 0:
        return s.copy()
    if bandwidth is None or bandwidth <= 0:
        return np.ones(n)
    dens = np.exp(-0.5 * ((s[:, None] - s[None, :]) / bandwidth) ** 2).sum(1)
    w = 1.0 / dens
    return w * n / w.sum()


def outlier_terms(x2, mode):
    """Per-component truncation c_n(x^2) and the outlier threshold on x^2 (README 4.1, 4.6)."""
    if mode == "k24":
        return np.tanh(x2), 3.0
    if mode == "3sigma":                              # variant 1: a tanh(x^2/a), a = 3 (outlier |x| > 3)
        return 3.0 * np.tanh(x2 / 3.0), 9.0
    if mode == "gauss":                               # variant 2: plain Gaussian, no outliers
        return x2, math.inf
    raise ValueError(mode)


# ---------------------------------------------------------------------------------------------
# Data, setups and the likelihood

@dataclass
class Data:
    """Clusters (positions pc, LSR velocities km/s, errors) and clouds (positions pc)."""
    cx: np.ndarray
    cy: np.ndarray
    cz: np.ndarray
    cvz: np.ndarray
    csig: np.ndarray          # (N, 4): sigmax, sigmay, sigmaz, sigmavz (km/s)
    ox: np.ndarray
    oy: np.ndarray
    oz: np.ndarray

    @property
    def n_clusters(self):
        return len(self.cx)

    @property
    def n_clouds(self):
        return len(self.ox)

    def cluster_subset(self, mask):
        m = np.asarray(mask)
        return replace(self, cx=self.cx[m], cy=self.cy[m], cz=self.cz[m], cvz=self.cvz[m],
                       csig=self.csig[m])

    def with_cluster_vz(self, vz):
        return replace(self, cvz=np.asarray(vz, float))

    def with_clusters(self, x, y, z, vz):
        return replace(self, cx=np.asarray(x, float), cy=np.asarray(y, float),
                       cz=np.asarray(z, float), cvz=np.asarray(vz, float))


@dataclass
class Setup:
    free: tuple
    fixed: dict = field(default_factory=dict)     # name -> value, overrides the base vector
    clusters: bool = True
    clouds: bool = False
    divisor: float | None = OMEGA0_ADOPTED        # None: v_z/omega0 uses the fitted omega0 (T8)
    prior: str = "k24"                            # k24 | broad (T8)
    outlier: str = "k24"                          # k24 | 3sigma | gauss
    u1_mode: str = "half"                         # half | chord (variant 10) | y_of_x | x_of_y (README 4.10)
    sigma: float = 47.0
    broad: dict | None = None                     # T8 broad bounds (default BROAD)
    sigma_mode: str = "fixed"                     # fixed | per_eval (README 4.10 P; clouds-only fits only)
    weights_mode: str = "fixed"                   # fixed | recompute (README 4.10 R; needs `bandwidth`)
    bandwidth: float | None = None                # kernel bandwidth (pc) for weights_mode = recompute


class Model:
    """Likelihood of one fit setup on fixed data with fixed kernel weights."""

    def __init__(self, setup: Setup, data: Data, grid: Grid, w_clusters=None, w_clouds=None,
                 base=None):
        self.setup = setup
        self.data = data
        self.grid = grid
        self.base = default_vector() if base is None else np.array(base, float)
        for k, val in setup.fixed.items():
            self.base[IDX[k]] = val
        self.free_idx = np.array([IDX[n] for n in setup.free], int)
        self.w_cl = np.ones(data.n_clusters) if w_clusters is None else np.asarray(w_clusters, float)
        self.w_co = np.ones(data.n_clouds) if w_clouds is None else np.asarray(w_clouds, float)
        self.D3o = np.column_stack([data.ox, data.oy, data.oz]) if setup.clouds else None
        s2 = setup.sigma ** 2
        self.const_cl = 3.0 * math.log(2.0 * math.pi * s2)
        self.const_co = math.log(2.0 * math.pi * s2)
        self.broad = setup.broad or BROAD
        if setup.sigma_mode not in ("fixed", "per_eval"):
            raise ValueError(f"unknown sigma_mode {setup.sigma_mode!r}")
        if setup.sigma_mode == "per_eval" and setup.clusters:
            raise ValueError("sigma_mode 'per_eval' applies to the clouds-only column (3) only (README 4.10)")
        if setup.weights_mode not in ("fixed", "recompute"):
            raise ValueError(f"unknown weights_mode {setup.weights_mode!r}")
        if setup.weights_mode == "recompute" and setup.bandwidth is None:
            raise ValueError("weights_mode 'recompute' needs the kernel bandwidth")

    # parameter vectors ---------------------------------------------------------------------
    def full(self, theta):
        v = self.base.copy()
        v[self.free_idx] = theta
        return v

    def theta_of(self, v):
        return np.asarray(v, float)[self.free_idx].copy()

    def divisor(self, v):
        return self.setup.divisor if self.setup.divisor is not None else math.exp(v[IDX["ln_omega0"]])

    def cluster_vectors(self, v):
        d = self.data
        return np.column_stack([d.cx, d.cy, d.cz, d.cvz / self.divisor(v)])

    def model_vectors(self, wv, v):
        return np.column_stack([wv["x"], wv["y"], wv["z"], wv["vz"] / self.divisor(v)])

    # likelihood ------------------------------------------------------------------------------
    def evaluate(self, v):
        """Everything about one parameter vector: lnL parts, closest indices, residuals, outliers."""
        wv = wave_on_grid(v, self.grid, self.setup.u1_mode)
        if wv is None:
            return None
        valid_idx = np.flatnonzero(wv["valid"])
        out = {"wave": wv, "valid_idx": valid_idx, "lnL": 0.0}
        sig = self.setup.sigma
        if self.setup.clusters and self.data.n_clusters:
            M = self.model_vectors(wv, v)[valid_idx]
            D = self.cluster_vectors(v)
            j = closest(D, M)
            res = D - M[j]
            x2 = (res / sig) ** 2
            c, thr = outlier_terms(x2, self.setup.outlier)
            w_cl = self.w_cl
            if self.setup.weights_mode == "recompute":     # README 4.10 R: from the 4-D closest points' s
                w_cl = kde_weights(wv["s"][valid_idx[j]], self.setup.bandwidth)
                out["w_cl"] = w_cl
            lnl = -0.5 * float(np.sum(w_cl * (c.sum(1) + self.const_cl)))
            out.update(cl_idx=valid_idx[j], cl_res=res, cl_outlier=np.any(x2 > thr, axis=1), lnL_cl=lnl)
            out["lnL"] += lnl
        if self.setup.clouds and self.data.n_clouds:
            M3 = np.column_stack([wv["x"], wv["y"], wv["z"]])[valid_idx]
            j = closest(self.D3o, M3)
            res = self.D3o - M3[j]
            d2 = (res * res).sum(1)
            w_co = self.w_co
            if self.setup.weights_mode == "recompute":     # README 4.10 R: from the 3-D closest points' s
                w_co = kde_weights(wv["s"][valid_idx[j]], self.setup.bandwidth)
                out["w_co"] = w_co
            if self.setup.sigma_mode == "per_eval":
                # README 4.10 P: sigma^2 = 0.5 x the unweighted standard deviation (ddof 0) of the clouds'
                # squared 3-D distances d^2_cloud,i(s_min), at this parameter vector, in eq. 11 incl. ln(2 pi sigma^2)
                s2 = 0.5 * float(np.std(d2))
                if not (np.isfinite(s2) and s2 > 0.0):
                    return None
                lnl = -float(np.sum(w_co * (d2 / (2.0 * s2) + math.log(2.0 * math.pi * s2))))
                out["sigma_eval"] = math.sqrt(s2)
            else:
                lnl = -float(np.sum(w_co * (d2 / (2.0 * sig * sig) + self.const_co)))
            out.update(co_idx=valid_idx[j], co_res=res, lnL_co=lnl)
            out["lnL"] += lnl
        return out

    def loglike(self, theta):
        v = self.full(theta)
        if self.setup.prior == "broad" and not self._in_broad(v):
            return -np.inf
        e = self.evaluate(v)
        return -np.inf if e is None else e["lnL"]

    def _in_broad(self, v):
        om = math.exp(v[IDX["ln_omega0"]])
        mu = math.exp(v[IDX["ln_mu0"]])
        r0 = v[IDX["r0"]]
        return (self.broad["omega0"][0] <= om <= self.broad["omega0"][1] and self.broad["mu0_kpc"][0] <= mu <= self.broad["mu0_kpc"][1]
                and self.broad["r0"][0] <= r0 <= self.broad["r0"][1])

    def logprior(self, theta):
        lp = 0.0
        for name, val in zip(self.setup.free, theta):
            if name == "w0t":
                if not (W0T_PRIOR[0] <= val <= W0T_PRIOR[1]):
                    return -np.inf
            elif name == "B":
                if not (B_PRIOR[0] <= val <= B_PRIOR[1]):
                    return -np.inf
            elif self.setup.prior == "broad" and name in ("ln_omega0", "ln_mu0", "r0"):
                if name == "ln_omega0":
                    om = math.exp(val)
                    if not (self.broad["omega0"][0] <= om <= self.broad["omega0"][1]):
                        return -np.inf
                    lp += val                       # uniform in omega0 -> Jacobian d omega0/d ln omega0
                elif name == "ln_mu0":
                    mu = math.exp(val)
                    if not (self.broad["mu0_kpc"][0] <= mu <= self.broad["mu0_kpc"][1]):
                        return -np.inf
                    lp += val
                else:
                    if not (self.broad["r0"][0] <= val <= self.broad["r0"][1]):
                        return -np.inf
            else:
                m, s = PRIOR_GAUSS[name]
                lp += -0.5 * ((val - m) / s) ** 2
        return lp

    def logpost(self, theta):
        lp = self.logprior(theta)
        if not np.isfinite(lp):
            return -np.inf
        ll = self.loglike(theta)
        return lp + ll if np.isfinite(ll) else -np.inf

    def prior_draw(self, rng, w0t_range=W0T_PRIOR):
        th = np.empty(len(self.setup.free))
        for i, name in enumerate(self.setup.free):
            if name == "w0t":
                th[i] = rng.uniform(*w0t_range)
            elif name == "B":
                th[i] = rng.uniform(*B_PRIOR)
            elif self.setup.prior == "broad" and name == "ln_omega0":
                th[i] = math.log(rng.uniform(*self.broad["omega0"]))
            elif self.setup.prior == "broad" and name == "ln_mu0":
                th[i] = math.log(rng.uniform(*self.broad["mu0_kpc"]))
            elif self.setup.prior == "broad" and name == "r0":
                th[i] = rng.uniform(*self.broad["r0"])
            else:
                m, s = PRIOR_GAUSS[name]
                th[i] = rng.normal(m, s)
        return th

    def scales(self):
        """A step size per free parameter (for simplices and walker balls)."""
        out = []
        for name in self.setup.free:
            if name == "w0t":
                out.append(0.3)
            elif name == "B":
                out.append(0.1)
            elif self.setup.prior == "broad" and name in ("ln_omega0", "ln_mu0"):
                out.append(0.3)
            elif self.setup.prior == "broad" and name == "r0":
                out.append(1000.0)
            else:
                out.append(PRIOR_GAUSS[name][1])
        return np.array(out)

    def clone(self, **kw):
        """Same setup with other data / weights (kw: data, w_clusters, w_clouds, setup)."""
        return Model(kw.get("setup", self.setup), kw.get("data", self.data), self.grid,
                     kw.get("w_clusters", self.w_cl), kw.get("w_clouds", self.w_co), self.base)


def wrap_pi(a):
    """Wrap to (-pi, pi]."""
    return -((-np.asarray(a, float) + math.pi) % (2.0 * math.pi) - math.pi)


def object_s(v, data: Data, grid: Grid, divisor=OMEGA0_ADOPTED, u1_mode="half"):
    """s of each cluster (4-D closest point) and cloud (3-D) under parameter vector v."""
    wv = wave_on_grid(v, grid, u1_mode)
    if wv is None:
        raise ValueError("parameter vector gives no usable model curve")
    vi = np.flatnonzero(wv["valid"])
    M4 = np.column_stack([wv["x"], wv["y"], wv["z"], wv["vz"] / divisor])[vi]
    D4 = np.column_stack([data.cx, data.cy, data.cz, data.cvz / divisor])
    s_cl = wv["s"][vi[closest(D4, M4)]] if data.n_clusters else np.zeros(0)
    if data.n_clouds:
        D3 = np.column_stack([data.ox, data.oy, data.oz])
        s_co = wv["s"][vi[closest(D3, M4[:, :3])]]
    else:
        s_co = np.zeros(0)
    return s_cl, s_co


def fixed_weights(data: Data, grid: Grid, bandwidth, u1_mode="half"):
    """README 4.1: weights from each object's s under K24's column-(6) medians, held fixed."""
    s_cl, s_co = object_s(k24_vector(6), data, grid, OMEGA0_ADOPTED, u1_mode)
    return kde_weights(s_cl, bandwidth), kde_weights(s_co, bandwidth)
