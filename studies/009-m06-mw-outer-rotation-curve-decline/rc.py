"""Rotation-curve physics and fits for study 009 (README sections 2 and 4).

Pure functions; tunable values are passed in as arguments (AGENTS.md section 2).
Units: kpc, km/s, Msun. G in kpc (km/s)^2 / Msun.
"""
import numpy as np
from scipy import integrate, optimize, special

G = 4.30091e-6          # kpc (km/s)^2 / Msun


# ------------------------------------------------------------ baryons ----

def disc_v2(R, M, L, H, kmax_factor=200.0, rel_tol=1e-6):
    """Midplane circular speed squared of a double-exponential disc rho = M/(4 pi H L^2) exp(-R/L - |z|/H).

    V^2 = 2 pi G Sigma0 L^2 R int_0^inf k J1(kR) / [(1 + k^2 L^2)^(3/2) (1 + k H)] dk, Sigma0 = M / (2 pi L^2).
    The integral is split at the zeros of J1(kR) up to k_max = kmax_factor / R, and k_max is doubled
    until the result changes by less than rel_tol.
    """
    sigma0 = M / (2 * np.pi * L ** 2)

    def integral(kmax):
        f = lambda k: k * special.j1(k * R) / ((1 + (k * L) ** 2) ** 1.5 * (1 + k * H))
        zeros = special.jn_zeros(1, max(1, int(kmax * R / np.pi) + 2)) / R
        edges = np.concatenate([[0.0], zeros[zeros < kmax], [kmax]])
        return sum(integrate.quad(f, a, b, limit=200)[0] for a, b in zip(edges[:-1], edges[1:]))

    kmax = kmax_factor / R
    val = integral(kmax)
    for _ in range(6):
        val2 = integral(2 * kmax)
        if abs(val2 - val) <= rel_tol * max(abs(val2), 1e-300):
            val = val2
            break
        val, kmax = val2, 2 * kmax
    else:
        raise RuntimeError(f"disc_v2 did not converge at R = {R} (L = {L}, H = {H})")
    return 2 * np.pi * G * sigma0 * L ** 2 * R * val


def freeman_v2(R, M, L):
    """Razor-thin exponential disc (Freeman 1970): V^2 = 4 pi G Sigma0 L y^2 [I0 K0 - I1 K1], y = R / 2L."""
    sigma0 = M / (2 * np.pi * L ** 2)
    y = R / (2 * L)
    return 4 * np.pi * G * sigma0 * L * y ** 2 * (special.i0(y) * special.k0(y) - special.i1(y) * special.k1(y))


def disc_mass_sphere(r, M, L, H):
    """Mass of a double-exponential disc inside a sphere of radius r (numerical; README 2.5).

    Integrates the cylinder mass at each height, 2 pi rho0 e^(-z/H) L^2 [1 - (1 + s/L) e^(-s/L)] with
    s = sqrt(r^2 - z^2), over z in units of H (u = z / H) so that thin discs are resolved.
    """
    rho0 = M / (4 * np.pi * H * L ** 2)

    def f(u):
        z = u * H
        s = np.sqrt(max(r * r - z * z, 0.0))
        return 2 * np.pi * rho0 * np.exp(-u) * L ** 2 * (1 - (1 + s / L) * np.exp(-s / L)) * H

    return 2 * integrate.quad(f, 0, min(r / H, 60.0), limit=200)[0]


def point_v2(R, M):
    return G * M / R


def hernquist_v2(R, M, rb):
    return G * M * R / (R + rb) ** 2


def baryon_v2(R, model):
    """model: dict with 'bulge' (kind, M, rb) and 'discs' [(M, L, H), ...]."""
    kind, Mb, rb = model["bulge"]
    v2 = hernquist_v2(R, Mb, rb) if kind == "hernquist" else point_v2(R, Mb)
    for M, L, H in model["discs"]:
        v2 = v2 + disc_v2(R, M, L, H)
    return v2


# --------------------------------------------------------------- halos ----

def einasto_mass(r, M0, h, inv_n):
    """M_DM(<r) = M0 n Gamma(3n) P(3n, (r/h)^(1/n)), M0 = 4 pi h^3 rho0."""
    n = 1.0 / inv_n
    a = 3 * n
    x = np.atleast_1d(np.asarray((r / h) ** inv_n, dtype=float))
    p = special.gammainc(a, x)
    with np.errstate(divide="ignore"):
        log_lower = special.gammaln(a) + np.log(p)                   # log of the lower incomplete gamma
    small = ~(p > 0)
    if np.any(small):                                                # underflow: series for large a
        xs = x[small]
        k = np.arange(400)
        terms = np.cumsum(np.log(xs[:, None]) - np.log(a + 1 + k[None, :]), axis=1)
        series = np.logaddexp.reduce(np.concatenate([np.zeros((xs.size, 1)), terms], axis=1), axis=1)
        log_lower[small] = a * np.log(xs) - xs - np.log(a) + series
    out = M0 * n * np.exp(log_lower)
    return out if np.ndim(r) else float(out[0])


def nfw_mass(r, rho_s, r_s):
    x = r / r_s
    return 4 * np.pi * rho_s * r_s ** 3 * (np.log1p(x) - x / (1 + x))


def r_vir(mass_fn, rho_cr, extra_mass=0.0, bracket=(1.0, 1e3)):
    """Radius where (M(<r) + extra_mass) / (4/3 pi r^3) = 200 rho_cr; None if no root in the bracket."""
    f = lambda r: (mass_fn(r) + extra_mass) / (4.0 / 3.0 * np.pi * r ** 3) - 200 * rho_cr
    a, b = bracket
    try:
        if f(a) * f(b) > 0:
            return None
        return optimize.brentq(f, a, b, xtol=1e-6)
    except (ValueError, FloatingPointError):
        return None


# ------------------------------------------------------------ power law ----

def powerlaw_lnpost(theta, R, V, sig, pivot, a_max, cov_inv=None, log_a=False, sample_pivot=None):
    """Posterior of V = A (R/pivot)^gamma with flat gamma in [-10, 5] and A flat on [0, a_max]
    (or log10 A flat on [0, log10 a_max] when log_a).

    Sampled coordinates (Vs, gamma) with Vs = V(sample_pivot) = A (sample_pivot/pivot)^gamma; the
    log-Jacobian of A -> Vs keeps the prior on A exactly as stated (README 2.1; reparametrisation only
    improves mixing, the posterior is unchanged).
    """
    vs, gamma = theta
    if not (-10 <= gamma <= 5) or vs <= 0:
        return -np.inf
    rs = pivot if sample_pivot is None else sample_pivot
    ratio = rs / pivot
    amp = vs * ratio ** (-gamma)
    if log_a:
        if not (1.0 <= amp <= a_max):
            return -np.inf
        log_jac = -np.log(vs)                       # flat in log A: p(Vs) = 1/A dA/dVs = 1/Vs
    else:
        if not (0.0 <= amp <= a_max):
            return -np.inf
        log_jac = -gamma * np.log(ratio)            # dA/dVs = ratio^(-gamma)
    r = V - vs * (R / rs) ** gamma
    if cov_inv is None:
        return -0.5 * np.sum((r / sig) ** 2) + log_jac
    return -0.5 * r @ cov_inv @ r + log_jac


def run_emcee(lnpost, start, args, nwalkers, nsteps, burn, seed, rel_width=1e-3, tau_factor=50):
    import emcee
    rng = np.random.default_rng(seed)
    ndim = len(start)
    p0 = start * (1 + rel_width * rng.standard_normal((nwalkers, ndim))) + 1e-6 * rng.standard_normal((nwalkers, ndim))
    sampler = emcee.EnsembleSampler(nwalkers, ndim, lnpost, args=args)
    sampler.random_state = np.random.RandomState(seed).get_state()   # seed the stretch moves
    sampler.run_mcmc(p0, nsteps, progress=False)
    chain = sampler.get_chain(discard=burn, flat=True)
    try:
        tau = float(np.max(sampler.get_autocorr_time(discard=burn, quiet=True)))
    except Exception:
        tau = float("nan")
    ok = np.isfinite(tau) and (nsteps - burn) > tau_factor * tau
    return chain, tau, bool(ok)


def s_statistic(gamma):
    med = np.median(gamma)
    return float((0 - med) / (np.percentile(gamma, 84) - med))


def one_sided_sigma(p, n_samples=None):
    """One-sided Gaussian significance of a tail probability; p = 0 gives a lower bound from 1/n_samples."""
    lower_bound = p <= 0
    if lower_bound:
        p = 1.0 / n_samples if n_samples else 1e-16
    p = min(p, 1 - 1e-16)
    return float(special.ndtri(1 - p)), bool(lower_bound)
