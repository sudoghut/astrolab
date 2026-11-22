"""T-047 design search (synthetic data only): a 6-D family whose Sigma-mnu-like box u is coupled to the curved pair.
Latent v ~ U(lo, hi); u = v - N(0, s); x1 = N(mu1 + a (v - c), 1); x2 = N(mu2, 1) + curv (x1 - mu1)^2 (curv about the
marginal-free centre mu1, as R6's gate); three further boxes as R6's. Exact log densities:
  D6 (x1, x2, u, b...): p(x2|x1) p(x1, u) prod p(b), with p(x1, u) = int U(v) N(u; v, s) N(x1; mu1 + a(v - c), 1) dv
  DS (u shuffled):      p(x2|x1) p(x1) p(u) prod p(b)
  D5 (u dropped):       p(x2|x1) p(x1) prod p(b)
All integrals over v are Gaussian x uniform: closed form. n_sigma = sqrt(2) erfinv(P(logp(X) > logp(0)))."""
import sys
import numpy as np
from scipy.stats import norm
from scipy.special import erfinv


def nsig(p):
    return float(np.sqrt(2) * erfinv(p))


def sample(n, rng, g):
    lo, hi, s = g["ubox"]
    v = rng.uniform(lo, hi, n)
    u = v - rng.normal(0.0, s, n)
    x1 = rng.normal(g["mu1"] + g["a"] * (v - g["c"]), 1.0, n)
    x2 = rng.normal(g["mu2"], 1.0, n) + g["curv"] * (x1 - g["mu1"]) ** 2
    boxes = [rng.uniform(blo, bhi, n) - rng.normal(0.0, bs, n) for blo, bhi, bs in g["boxes"]]
    return np.column_stack([x1, x2, u] + boxes)


def log_box(u, lo, hi, s):
    return np.log(np.clip(norm.cdf((u - lo) / s) - norm.cdf((u - hi) / s), 1e-300, None) / (hi - lo))


def log_x1(x1, g):
    """marginal of x1: int U(v) N(x1; mu1 + a (v - c), 1) dv"""
    lo, hi, _ = g["ubox"]
    a = g["a"]
    if a == 0:
        return norm.logpdf(x1, g["mu1"], 1.0)
    m_lo = g["mu1"] + a * (lo - g["c"])
    m_hi = g["mu1"] + a * (hi - g["c"])
    A, B = min(m_lo, m_hi), max(m_lo, m_hi)
    return np.log(np.clip(norm.cdf(x1 - A) - norm.cdf(x1 - B), 1e-300, None) / (B - A))


def log_x1u(x1, u, g):
    """int U(v) N(u; v, s) N(x1; mu1 + a (v - c), 1) dv (closed form)"""
    lo, hi, s = g["ubox"]
    a, c, mu1 = g["a"], g["c"], g["mu1"]
    # as a function of v: N(v; u, s^2) * N(v; (x1 - mu1)/a + c, 1/a^2) / |a|... combine precisions
    if a == 0:
        return norm.logpdf(x1, mu1, 1.0) + log_box(u, lo, hi, s)
    t1, p1 = u, 1.0 / s ** 2
    t2, p2 = (x1 - mu1) / a + c, a ** 2
    P = p1 + p2
    m = (p1 * t1 + p2 * t2) / P
    # N(v; t1, 1/p1) N(v; t2, 1/p2) = N(t1; t2, 1/p1 + 1/p2) N(v; m, 1/P); and N(x1; ...) = |a| N(v; t2, 1/a^2)... ->
    # N(x1; mu1 + a(v - c), 1) = N(v; t2, 1/a^2) / |a|
    log_pair = norm.logpdf(t1, t2, np.sqrt(1 / p1 + 1 / p2)) - np.log(abs(a))
    sd = 1 / np.sqrt(P)
    mass = np.clip(norm.cdf((hi - m) / sd) - norm.cdf((lo - m) / sd), 1e-300, None)
    return log_pair + np.log(mass) - np.log(hi - lo)


def logp(z, g, variant):
    x1, x2 = z[:, 0], z[:, 1]
    out = norm.logpdf(x2 - g["curv"] * (x1 - g["mu1"]) ** 2, g["mu2"], 1.0)
    if variant == "6":
        out = out + log_x1u(x1, z[:, 2], g)
        rest = z[:, 3:]
    elif variant == "S":
        out = out + log_x1(x1, g) + log_box(z[:, 2], *g["ubox"])
        rest = z[:, 3:]
    else:  # "5": u dropped
        out = out + log_x1(x1, g)
        rest = z[:, 2:]
    for i, (lo, hi, s) in enumerate(g["boxes"]):
        out = out + log_box(rest[:, i], lo, hi, s)
    return out


def exact(g, n=2_000_000, seed=999):
    z6 = sample(n, np.random.default_rng(seed), g)
    zS = z6.copy()
    zS[:, 2] = zS[np.random.default_rng(seed + 1).permutation(n), 2]
    z5 = np.delete(z6, 2, axis=1)
    out = {}
    for v, z in (("6", z6), ("S", zS), ("5", z5)):
        o = np.zeros((1, z.shape[1]))
        out[v] = nsig(float(np.mean(logp(z, g, v) > logp(o, g, v)[0])))
    out["phi"] = (out["6"] - out["S"]) / (out["6"] - out["5"])
    return out


def check_density(g):
    """numerical check of the closed forms: integrate over v on a grid"""
    rng = np.random.default_rng(0)
    z = sample(5, rng, g)
    lo, hi, s = g["ubox"]
    v = np.linspace(lo, hi, 20001)
    for x1, u in z[:, [0, 2]]:
        num = np.trapz(norm.pdf(u, v, s) * norm.pdf(x1, g["mu1"] + g["a"] * (v - g["c"]), 1.0), v) / (hi - lo)
        assert abs(np.log(num) - log_x1u(np.array([x1]), np.array([u]), g)[0]) < 1e-6
        num1 = np.trapz(norm.pdf(x1, g["mu1"] + g["a"] * (v - g["c"]), 1.0), v) / (hi - lo)
        assert abs(np.log(num1) - log_x1(np.array([x1]), g)[0]) < 1e-6


if __name__ == "__main__":
    base = {"mu2": 0.55, "curv": 0.3, "ubox": [-0.1, 1.9, 0.1], "c": 0.9,
            "boxes": [[-0.6, 1.4, 0.05], [-0.6, 1.4, 0.05], [-0.6, 1.4, 0.05]]}
    check_density(dict(base, mu1=1.0, a=1.5))
    print("closed forms ok")
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 300_000
    for mu1 in (0.6, 0.9, 1.2):
        for a in (1.0, 2.0, 3.0):
            for c in (0.9, 1.9):
                g = dict(base, mu1=mu1, a=a, c=c)
                e = exact(g, n=n)
                print(f"mu1 {mu1} a {a} c {c}: n6 {e['6']:.3f} nS {e['S']:.3f} n5 {e['5']:.3f} phi {e['phi']:.3f}")
