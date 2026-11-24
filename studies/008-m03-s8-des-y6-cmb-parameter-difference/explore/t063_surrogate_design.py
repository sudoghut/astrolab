"""Design of R6-SHUF-KA2 (T-063, README 2.10; drafting, 2026-11-24). No flow is trained.

Builds the surrogate of the data's own 6-D DES - CMB difference: a full-covariance Gaussian mixture fitted to each
chain (the six R6 parameters, in units standardised by the DES chain's weighted mean and standard deviation), with
the number of components K in 1..8 chosen by the Bayesian information criterion (BIC), on 100,000 weighted
resampled rows of each chain (default_rng(7000) for DES, default_rng(7001) for the CMB chain). Then the exact
n_sigma of the three variants from closed-form mixture densities:
  D6: a - c, a ~ DES mixture, c ~ CMB mixture (a mixture of K_d K_c Gaussians);
  DS: DES's Sigma m_nu made independent of DES's other five (the product of its two marginal mixtures, K_d^2
      components), minus c (K_d^2 K_c Gaussians); its rows are the D6 rows with the DES Sigma m_nu column permuted,
      as R6-SHUF's (S);
  D5: Sigma m_nu dropped (the 5-D marginal of D6).
Writes the surrogate (weights, means, Cholesky factors, the standardisation) and the exact values to its output
folder. Run with:
    python -m astrolab explore 008 --tag t063-surrogate --script explore/t063_surrogate_design.py
"""
import json
import time

import numpy as np

import run
import s8diff

COLS = ["a_s_1e9", "h0", "mnu", "n_s", "omega_b", "omega_m"]      # R6's six, in R6's order
MNU = COLS.index("mnu")
K_MAX = 8
N_FIT = 100_000
FIT_SEEDS = {"des_3x2pt": 7000, "cmb": 7001}


def load(ctx, P, key):
    path = run._fetch(ctx, P, key)
    fmt = s8diff.read_format(path)
    cmap, _ = s8diff.column_map(fmt, key, key in P["positional_ok"])
    burn, _ = s8diff.burn_in_fraction(fmt["sampler"], P["mcmc_burn"])
    chain, _ = s8diff.load_chain(path, cmap, burn)
    hdr = [h.lower() for h in fmt["header"]]
    X = np.column_stack([chain["data"][:, hdr.index("cosmological_parameters--" + n)] for n in COLS])
    ok = np.all(np.isfinite(X), axis=1) & np.isfinite(chain["w"])
    w = chain["w"][ok]
    return X[ok], w / w.sum()


def fit(z, seed_label):
    from sklearn.mixture import GaussianMixture
    out = []
    for k in range(1, K_MAX + 1):
        g = GaussianMixture(k, covariance_type="full", n_init=4, max_iter=2000, tol=1e-5, reg_covar=1e-6,
                            random_state=0).fit(z)
        out.append({"k": k, "bic": float(g.bic(z)), "converged": bool(g.converged_), "gm": g})
    best = min(out, key=lambda r: r["bic"])
    return best["gm"], [{kk: r[kk] for kk in ("k", "bic", "converged")} for r in out]


def mix(g):
    return {"w": g.weights_.tolist(), "mu": g.means_.tolist(),
            "L": np.linalg.cholesky(g.covariances_).tolist()}


# ----------------------------------------------------------------- mixtures (pure numpy) ----
def sample(m, n, rng):
    """Draw order: one uniform per row for the component, then a standard normal (n, d) block."""
    w, mu, L = np.asarray(m["w"]), np.asarray(m["mu"]), np.asarray(m["L"])
    comp = np.minimum(np.searchsorted(np.cumsum(w), rng.random(n), side="right"), len(w) - 1)
    z = rng.standard_normal((n, mu.shape[1]))
    return mu[comp] + np.einsum("nij,nj->ni", L[comp], z)


def gauss_list(w, mu, cov):
    return [(float(a), np.asarray(b), np.asarray(c)) for a, b, c in zip(w, mu, cov)]


def components(md, mc, variant):
    """(weight, mean, covariance) of the difference's mixture for variant '6', 'S' or '5'."""
    wd, mud, Ld = np.asarray(md["w"]), np.asarray(md["mu"]), np.asarray(md["L"])
    wc, muc, Lc = np.asarray(mc["w"]), np.asarray(mc["mu"]), np.asarray(mc["L"])
    Cd, Cc = Ld @ np.swapaxes(Ld, 1, 2), Lc @ np.swapaxes(Lc, 1, 2)
    if variant == "S":
        rest = [j for j in range(mud.shape[1]) if j != MNU]
        a = []
        for i in range(len(wd)):
            for i2 in range(len(wd)):
                m = mud[i].copy()
                m[MNU] = mud[i2][MNU]
                C = np.zeros_like(Cd[i])
                C[np.ix_(rest, rest)] = Cd[i][np.ix_(rest, rest)]
                C[MNU, MNU] = Cd[i2][MNU, MNU]
                a.append((wd[i] * wd[i2], m, C))
    else:
        a = gauss_list(wd, mud, Cd)
    out = [(wa * wb, ma - mb, Ca + Cb) for wa, ma, Ca in a for wb, mb, Cb in gauss_list(wc, muc, Cc)]
    if variant == "5":
        keep = [j for j in range(mud.shape[1]) if j != MNU]
        out = [(w, m[keep], C[np.ix_(keep, keep)]) for w, m, C in out]
    return out


def logp(x, comps, chunk=50_000):
    """log density of the mixture at the rows of x."""
    pre = []
    for w, m, C in comps:
        L = np.linalg.cholesky(C)
        pre.append((np.log(w) - np.log(np.diag(L)).sum() - 0.5 * len(m) * np.log(2 * np.pi), m, L))
    res = np.empty(len(x))
    for s in range(0, len(x), chunk):
        xs = x[s:s + chunk]
        acc = np.empty((len(pre), len(xs)))
        for i, (c0, m, L) in enumerate(pre):
            y = np.linalg.solve(L, (xs - m).T)
            acc[i] = c0 - 0.5 * np.sum(y * y, axis=0)
        mx = acc.max(axis=0)
        res[s:s + chunk] = mx + np.log(np.exp(acc - mx).sum(axis=0))
    return res


def nsig(p):
    from scipy.special import erfinv
    return float(np.sqrt(2.0) * erfinv(p))


def rows(md, mc, n, seed, variant, perm_seed=None):
    """The variant's rows (standardised units): D6 = DES draws - CMB draws from default_rng(seed) (DES first);
    DS: the DES Sigma m_nu column permuted with default_rng(perm_seed).permutation(n) before the difference;
    D5: D6 without Sigma m_nu."""
    rng = np.random.default_rng(seed)
    a = sample(md, n, rng)
    c = sample(mc, n, rng)
    if variant == "S":
        a[:, MNU] = a[np.random.default_rng(perm_seed).permutation(n), MNU]
    d = a - c
    return np.delete(d, MNU, axis=1) if variant == "5" else d


def exact(md, mc, n=2_000_000, seed=999, perm_seed=1000):
    out = {}
    for v in ("6", "S", "5"):
        comps = components(md, mc, v)
        x = rows(md, mc, n, seed, v, perm_seed)
        l0 = logp(np.zeros((1, x.shape[1])), comps)[0]
        out[v] = nsig(float(np.mean(logp(x, comps) > l0)))
    out["phi"] = (out["6"] - out["S"]) / (out["6"] - out["5"])
    return out


def main(ctx):
    P = dict(run.PARAMS)
    t0 = time.time()
    X = {k: load(ctx, P, k) for k in ("des_3x2pt", "cmb")}
    xd, wd = X["des_3x2pt"]
    center = np.average(xd, axis=0, weights=wd)
    scale = np.sqrt(np.average((xd - center) ** 2, axis=0, weights=wd))
    mixes, bics, ess = {}, {}, {}
    for key, (x, w) in X.items():
        ess[key] = float(1.0 / np.sum(w ** 2))
        idx = np.random.default_rng(FIT_SEEDS[key]).choice(len(w), size=N_FIT, replace=True, p=w)
        z = (x[idx] - center) / scale
        g, bics[key] = fit(z, key)
        mixes[key] = mix(g)
        ctx.log(f"{key}: ESS {ess[key]:.0f}, BIC-selected K = {len(g.weights_)}")
    ex = exact(mixes["des_3x2pt"], mixes["cmb"])
    ctx.log(f"exact: n6 {ex['6']:.4f}, nS {ex['S']:.4f}, n5 {ex['5']:.4f}, phi {ex['phi']:.4f}")
    ex2 = exact(mixes["des_3x2pt"], mixes["cmb"], seed=998, perm_seed=997)
    ctx.log(f"exact (seeds 998/997): n6 {ex2['6']:.4f}, nS {ex2['S']:.4f}, n5 {ex2['5']:.4f}")
    ctx.save("t063_surrogate", {"columns": COLS, "center": center.tolist(), "scale": scale.tolist(),
                                "fit": {"n": N_FIT, "seeds": FIT_SEEDS, "k_max": K_MAX, "bic": bics, "ess": ess},
                                "mixtures": mixes, "exact": ex, "exact_check": ex2,
                                "seconds": round(time.time() - t0, 1)})
