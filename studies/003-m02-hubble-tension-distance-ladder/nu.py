"""R2-RE-NU (README section 2, addendum 2026-11-24, T-062): an outside constraint on the tail weight nu of the host
effects from the Hubble-flow (HF) supernova rows. Reported and non-decisive.

On the NGC 4258-only system (rows_a), with X the fitted columns of L there and C_a the base covariance on rows_a:
P = C_a^-1 - C_a^-1 X (X^T C_a^-1 X)^-1 X^T C_a^-1; the HF rows are grouped into SNe (connected components of
"correlation in C above 0.3"), Z is the rows_a x n_g group design, u = Z^T P y, M = Z^T P Z. With D = diag(d_g):
g(D) = log det(I + D^1/2 M D^1/2) - u^T D^1/2 (I + D^1/2 M D^1/2)^-1 D^1/2 u = -2 l_R(C + Z D Z^T) + 2 l_R(C).

Stage 1: tau_HF by R2-RE's REML (reml_m2l, reml_tau) with d_g = tau^2 and the gate (tau_hat_HF >= 0.02 and the 68%
interval's lower end above 0). Stage 2: b_g = s t_g, t_g ~ t_nu, s = tau sqrt((nu - 2) / nu);
Lambda(nu, tau) = E_w[exp(-g(diag(s^2 / w)) / 2)] by importance sampling over w (defensive mixture proposal), the
weights w(nu) ~ pi(nu) L(nu) on the grid {3, 4, 6, 10, 30, inf}, P(nu <= 4) and the labels. A known-answer check
on mocks built from C and L (t_3, t_10, heteroscedastic Gaussian, t_3 truncated at 3.5 sigma) comes first.

Two stages (README "Order and stages"): the check stage writes r2_re_nu_check.json (checks, Stage 1, the mocks; never
L(nu) on the data); the full stage recomputes the checks, Stage 1 and the first 20 mocks of each injection (they must
equal the check record), then computes L(nu), the weights, the label and p_int.

run.py passes its own functions in (`fns`); this module does not import run (AGENTS.md section 2).
"""
import math
import time

import numpy as np
from scipy import linalg, special
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

import shape

# ---------------------------------------------------------------- pre-registered values (README R2-RE-NU)
PREREGISTERED = {
    "nu_grid": [3, 4, 6, 10, 30, "inf"], "nu_tau_gate": 0.02, "nu_group_corr": 0.3, "nu_group_corr_sens": 0.45,
    "nu_q_prior_frac": 0.1, "nu_n_is": 4_000, "nu_n_is_escalate": 32_000, "nu_is_seed": 730_000,
    "nu_is_seed_escalate": 740_000, "nu_n_mocks": 200, "nu_n_is_mock": 2_000, "nu_cut_sigma": 3.5,
    "nu_cut_attempts": 100,
    "nu_mock_seeds": {"eps": 700_000, "t3": 710_000, "t10": 720_000, "het": 780_000, "trunc_joint": 1_000_000,
                      "is_t3": 750_000, "is_t10": 760_000, "is_het": 800_000, "is_trunc": 810_000},
    "nu_profile_m": [0.5, 0.75, 1, 1.5, 2], "nu_profile_seed": 770_000, "nu_vbase_seed": 820_000,
    "nu_group_sens_seed": 830_000,
}
NU_KEYS = ["3", "4", "6", "10", "30", "inf"]
FINITE_NU = [3.0, 4.0, 6.0, 10.0, 30.0]          # j = 0, ..., 4 in the seeds
PRIOR_FLAT = [1.0 / 6.0] * 6
PRIOR_INV_NU = [0.125, 0.25, 0.225, 0.20, 0.15, 0.05]    # uniform in 1/nu on [0, 1/3], cells at the midpoints
TAU_MAX, TAU_STEP = shape.TAU_MAX, shape.TAU_STEP      # reml_tau(f, 0.5, 0.01), R2-RE's grid
ZERO_TAU = 1e-3                                  # R2-RE's zero rule
SCALE_REF = 0.0767                               # the scale condition (S5): 0.0767 inside tau_hat_HF's 68% interval
TAU_OBS_RATIO = shape.RECORDED_TAU_OBS           # tau_hat_HF / tau_hat_obs (0.0766988, R2-RE)
COUNT_FRAC = 0.05                                # |n_g - n_CID| <= floor(0.05 n_CID)
N_STREAMS = 2
STREAM_DIFF_MAX = 0.1                            # |log Lambda_r=0 - log Lambda_r=1| <= 0.1
ESS_MIN = 200
KHAT_MAX = 0.7
LIGHT, HEAVY = 0.05, 0.95                        # P(nu <= 4) < 0.05 light-tail, > 0.95 heavy-tail
MAX_MISLABEL = 10                                # (a), (c), (e): at most 10 of the 200 mocks
DELTA_B_MIN = 0.10                               # (b)
MAX_TRUNC_FAILED = 10                            # more than 10 "truncation failed": selection
N_POINTWISE = 3                                  # first three t_3 mocks built in full
N_REPRO_MOCKS = 20                               # first 20 mocks of each injection recomputed by the full stage
INJECTIONS = ("t3", "t10", "het", "trunc")
N_HF_EXPECTED = 277                              # row classes: 277 Hubble-flow rows ...
N_ROWS_A_EXPECTED = 3489                         # ... all in rows_a (3,489 rows)
P_CAL_README = {"3": 0.0768, "4": 0.0504, "6": 0.0300, "10": 0.0208, "30": 0.0166, "inf": 0.0165}
P_CAL_MAX_README = {"3": 0.0783, "4": 0.0510, "6": 0.0303, "10": 0.0216, "30": 0.0178, "inf": 0.0165}
P_CAL_README_ATOL = 5e-5                         # the README quotes them to 4 decimals
PRIOR_ONLY_REF = 0.0352                          # p_int with prior weights (flat), README item 7
PANTHEON_USECOLS = ("CID", "USED_IN_SH0ES_HF")   # the only columns of Pantheon+SH0ES.dat ever read
CLOCK = time.perf_counter                        # tests may replace it

LBL_NOT_EVAL = "ν not evaluable ({})"
LBL_NO_EXCESS = "ν not evaluable (no excess scatter in the Hubble flow)"
LBL_METHOD = "ν not determinable by this method ({})"
LBL_SELECTION = "ν not determinable (selection)"
LBL_LIGHT = "ν constrained to the light-tail side (P(ν ≤ 4) < 0.05)"
LBL_HEAVY = "ν constrained to the heavy-tail side (P(ν ≤ 4) > 0.95)"
LBL_WEAK = "ν weakly constrained"
COND = " (if Hubble-flow and calibrator effects share ν)"
SCALE_SUFFIX = " (scale differs: transfer not supported)"
PART_A, PART_B, PART_C, PART_MC = "mislabels", "no power at this τ_HF", "heteroscedasticity", "Monte Carlo"
READ_BELOW = ("integrated over the Hubble-flow-informed ν, diffuse host scatter of R2-RE's size is excluded by G at "
              "the 5% level (reported, non-decisive)")
READ_ABOVE = "not excluded"
# keys the check record must never hold (README: no L(nu), weights, label or p_int computed on the data)
FORBIDDEN_CHECK_KEYS = ("L_nu", "log_L", "log_L_nu", "weights", "P_le4", "p_int", "label", "p_int_reading",
                        "stage2", "sensitivities")


def json_like(o):
    return shape.json_like(o)


def nu_key(nu):
    return shape.gtp_nu_key(nu)


def preregistered_problems(P):
    """The nu_* PARAMS that differ from the pre-registered values (a formal run refuses to start)."""
    return [k for k, v in PREREGISTERED.items() if json_like(P.get(k)) != json_like(v)]


def one_thread_problems(threads=None):
    """A formal run uses one thread (OMP/MKL/OPENBLAS_NUM_THREADS = 1)."""
    env = (threads or shape.thread_settings())["env"]
    return [f"{k}={env.get(k)!r}" for k in shape.THREAD_ENV if env.get(k) != "1"]


# ---------------------------------------------------------------- SN grouping and the CID count check (S1)
def hf_groups(C, hf_rows, thr):
    """The HF rows grouped into SNe: connected components of the graph joining two HF rows whose correlation in C
    exceeds thr. Groups hold full-system row indices (sorted), ordered by their first row."""
    idx = np.asarray(hf_rows)
    S = C[np.ix_(idx, idx)]
    d = np.sqrt(np.diag(S))
    adj = (S / np.outer(d, d)) > float(thr)
    np.fill_diagonal(adj, False)
    _, lab = connected_components(csr_matrix(adj), directed=False)
    groups = [idx[lab == k] for k in np.unique(lab)]
    groups.sort(key=lambda g: int(g[0]))
    return groups


def count_check(n_g, n_cid):
    """|n_g - n_CID| <= floor(0.05 n_CID) (main grouping only)."""
    tol = int(math.floor(COUNT_FRAC * int(n_cid)))
    return {"n_groups": int(n_g), "n_cid": int(n_cid), "tolerance": tol, "ok": bool(abs(int(n_g) - int(n_cid)) <= tol)}


def read_hf_cid_count(path, read_csv=None):
    """The number of distinct CID among the USED_IN_SH0ES_HF = 1 rows of Pantheon+SH0ES.dat. Reads the columns CID
    and USED_IN_SH0ES_HF only (usecols; no magnitude, error or residual column is ever read)."""
    if read_csv is None:
        import pandas as pd
        read_csv = pd.read_csv
    df = read_csv(path, sep=r"\s+", usecols=list(PANTHEON_USECOLS), dtype={"CID": str})
    if sorted(df.columns) != sorted(PANTHEON_USECOLS):
        raise RuntimeError(f"Pantheon+SH0ES.dat read returned columns {list(df.columns)}")
    used = df["USED_IN_SH0ES_HF"].astype(int).to_numpy() == 1
    return {"n_rows_used": int(used.sum()), "n_cid": int(df["CID"][used].nunique()),
            "columns_read": list(PANTHEON_USECOLS)}


# ---------------------------------------------------------------- the reduced form
def hf_design(L, y, Cb, rows_a, groups, fns):
    """Design-only quantities on rows_a under the base covariance Cb (y enters only y_hat and u): X (infer.gls's
    kept columns), K (lower Cholesky of Cb on rows_a), Z, P Z, M (raw and clipped), B = Z^T P K, the residual maps
    of the truncation (C_a P K and C_a P Z on the HF rows), sigma_i = sqrt(C_ii) on the HF rows, c_g. Returns
    (des, problem): problem is a label-1 reason or None."""
    rows_a = np.asarray(rows_a)
    n_a = len(rows_a)
    res = fns["fit"](L, y, Cb, rows_a)
    kept = res["kept"]
    X = L[np.ix_(rows_a, kept)]
    yhat = X @ res["q"][kept]
    gpos = shape.group_positions(rows_a, groups)
    n_g = len(groups)
    Ca = Cb[np.ix_(rows_a, rows_a)]
    try:
        K = linalg.cholesky(Ca, lower=True)
    except np.linalg.LinAlgError as e:
        return None, f"the Cholesky factor of C failed: {e}"
    Zm = np.zeros((n_a, n_g))
    for g, p in enumerate(gpos):
        Zm[p, g] = 1.0
    cf = (K, True)
    CiX = linalg.cho_solve(cf, X)
    CiZ = linalg.cho_solve(cf, Zm)
    F = X.T @ CiX
    F = 0.5 * (F + F.T)
    cfF = linalg.cho_factor(F, lower=True)
    PZ = CiZ - CiX @ linalg.cho_solve(cfF, X.T @ CiZ)
    M = Zm.T @ PZ
    M = 0.5 * (M + M.T)
    lam_raw, Q = np.linalg.eigh(M)
    thr = shape.EIG_RTOL * float(lam_raw.max())
    if np.any(lam_raw < -thr):
        raise RuntimeError(f"M has a negative eigenvalue {lam_raw.min()!r} beyond the clipping threshold: a bug")
    clipped = np.abs(lam_raw) < thr
    lam = np.where(clipped, 0.0, lam_raw)
    hf_pos = np.sort(np.concatenate(gpos))
    W1 = linalg.solve_triangular(K, X, lower=True)               # K^-1 X: (C^-1 X)^T K = W1^T
    FinvT = linalg.cho_solve(cfF, W1.T)                          # F^-1 X^T K^-T
    R_eps = K[hf_pos] - X[hf_pos] @ FinvT                        # (C_a P K) on the HF rows
    R_b = Zm[hf_pos] - X[hf_pos] @ linalg.cho_solve(cfF, CiX.T @ Zm)   # (C_a P Z) on the HF rows
    diag = np.diag(Ca)
    des = {"rows_a": rows_a, "n_a": n_a, "n_g": n_g, "kept": kept, "X": X, "yhat": yhat, "gpos": gpos, "K": K,
           "Zm": Zm, "PZ": PZ, "M": M, "lam_raw": lam_raw, "lam": lam, "Q": Q, "Mc": (Q * lam) @ Q.T,
           "n_clipped": int(clipped.sum()), "rank_M": int((~clipped).sum()), "lam_max": float(lam_raw.max()),
           "lam_min_raw": float(lam_raw.min()), "B": PZ.T @ K, "hf_pos": hf_pos, "sig_hf": np.sqrt(diag[hf_pos]),
           "R_eps": R_eps, "R_b": R_b, "c_g": np.array([float(np.mean(diag[p])) for p in gpos])}
    if des["n_clipped"] > 1:
        return des, f"design: M has {des['n_clipped']} zero eigenvalues, expected 1"
    return des, None


def u_of(y, des):
    """u = Z^T P y on rows_a."""
    return des["PZ"].T @ np.asarray(y)[des["rows_a"]]


def g_iso(tau, u, des):
    """g(tau^2 I) from the eigen-decomposition (R2-RE-G's f(tau; u))."""
    return shape.reml_f(tau, des["Q"].T @ u, des["lam"])


def g_of_d(d, u, Mc):
    """g(D) from the Cholesky factor of I + D^1/2 M D^1/2 (log det from its diagonal)."""
    sd = np.sqrt(np.asarray(d, dtype=float))
    A = Mc * np.outer(sd, sd)
    A[np.diag_indices_from(A)] += 1.0
    Lc = linalg.cholesky(A, lower=True, check_finite=False)
    z = linalg.solve_triangular(Lc, sd * u, lower=True, check_finite=False)
    return float(2.0 * np.sum(np.log(np.diag(Lc))) - z @ z)


def posterior_m(tau, u, des):
    """m_g = mu_g^2 + Sigma_gg of the Gaussian posterior of b under d_g = tau^2: Sigma = (tau^-2 I + M)^-1, mu = Sigma u."""
    Q, lam = des["Q"], des["lam"]
    inv = 1.0 / (1.0 / (float(tau) ** 2) + lam)
    mu = Q @ (inv * (Q.T @ u))
    return mu * mu + (Q * Q) @ inv


# ---------------------------------------------------------------- importance sampling (S3)
def t_scale2(tau, nu):
    """s^2 = tau^2 (nu - 2) / nu (variance tau^2)."""
    return float(tau) ** 2 * (float(nu) - 2.0) / float(nu)


def _log_gamma_pdf(w, a, rate):
    return a * np.log(rate) - special.gammaln(a) + (a - 1.0) * np.log(w) - rate * w


def proposal_draws(nu, s2, m, n, seed, q_prior):
    """w (n x n_g) from the defensive mixture q_g = q Gamma(nu/2, nu/2) + (1 - q) Gamma((nu+1)/2, (nu + m_g/s^2)/2),
    from one default_rng(seed) in a fixed order: the component indicators for all n x n_g coordinates, then the
    prior-component Gammas, then the posterior-component Gammas, each in row-major order. Returns (w, log p, log q)."""
    nu = float(nu)
    n_g = len(m)
    rng = np.random.default_rng(int(seed))
    prior = rng.random((int(n), n_g)) < float(q_prior)
    w = np.empty((int(n), n_g))
    a0, r0 = nu / 2.0, nu / 2.0
    a1 = (nu + 1.0) / 2.0
    r1 = (nu + np.asarray(m) / s2) / 2.0
    w[prior] = rng.gamma(a0, 1.0 / r0, size=int(prior.sum()))
    cols = np.nonzero(~prior)[1]
    w[~prior] = rng.gamma(a1, 1.0 / r1[cols])
    lp = _log_gamma_pdf(w, a0, r0)
    lq1 = _log_gamma_pdf(w, a1, r1[None, :])
    lq = np.logaddexp(np.log(q_prior) + lp, np.log1p(-q_prior) + lq1)
    return w, lp, lq


def is_log_weights(nu, tau, u, des, m, n, seed, q_prior):
    """log omega_i = sum_g [log Gamma(w_ig; nu/2, nu/2) - log q_g(w_ig)] - g(diag(s^2 / w_i)) / 2."""
    s2 = t_scale2(tau, nu)
    w, lp, lq = proposal_draws(nu, s2, m, n, seed, q_prior)
    Mc = des["Mc"]
    gv = np.array([g_of_d(s2 / w[i], u, Mc) for i in range(w.shape[0])])
    return np.sum(lp - lq, axis=1) - 0.5 * gv


def gpd_fit(x):
    """Zhang-Stephens estimate of the generalized Pareto shape k (and scale) of exceedances x (sorted ascending),
    with the weak prior on k of the PSIS reference implementation (Vehtari et al., arXiv:1507.02646)."""
    x = np.asarray(x, dtype=float)
    n = len(x)
    prior_bs, prior_k = 3.0, 10.0
    m_est = 30 + int(n ** 0.5)
    b = 1.0 - np.sqrt(m_est / (np.arange(1, m_est + 1) - 0.5))
    b /= prior_bs * x[int(n / 4 + 0.5) - 1]
    b += 1.0 / x[-1]
    k = np.log1p(-b[:, None] * x).mean(axis=1)
    len_scale = n * (np.log(-(b / k)) - k - 1.0)
    with np.errstate(over="ignore"):                   # overflow -> weight 0, as in the reference code
        wts = 1.0 / np.exp(len_scale - len_scale[:, None]).sum(axis=1)
    keep = wts >= 10 * np.finfo(float).eps
    wts, b = wts[keep], b[keep]
    wts /= wts.sum()
    b_post = float(np.sum(b * wts))
    k_post = float(np.log1p(-b_post * x).mean())
    sigma = -k_post / b_post
    k_post = (n * k_post + prior_k * 0.5) / (n + prior_k)
    return k_post, sigma


def psis_khat(log_w):
    """Pareto shape k_hat of the largest min(0.2 N, 3 sqrt N) weights (diagnostic only; the estimate is not smoothed)."""
    lw = np.sort(np.asarray(log_w, dtype=float))
    n = len(lw)
    m = int(math.ceil(min(0.2 * n, 3.0 * math.sqrt(n))))
    lw = lw - lw[-1]
    cut = lw[-m - 1]
    tail = lw[lw > cut]
    if len(tail) <= 4:
        return float("inf")
    x = np.sort(np.exp(tail) - np.exp(cut))
    return float(gpd_fit(x)[0])


def stream_stats(log_w):
    lw = np.asarray(log_w, dtype=float)
    lse = special.logsumexp(lw)
    return {"n": int(len(lw)), "log_lambda": float(lse - math.log(len(lw))),
            "ess": float(math.exp(2.0 * lse - special.logsumexp(2.0 * lw))), "khat": psis_khat(lw)}


def lambda_finite(nu, tau, u, des, n, seeds, q_prior):
    """log Lambda(nu, tau) over len(seeds) streams of n draws: per-stream estimate, ESS and k_hat, the accuracy check
    (two or more streams) and the pooled estimate."""
    m = posterior_m(tau, u, des)
    lws, streams = [], []
    for sd in seeds:
        lw = is_log_weights(nu, tau, u, des, m, n, sd, q_prior)
        lws.append(lw)
        streams.append(dict(stream_stats(lw), seed=int(sd)))
    pooled = np.concatenate(lws)
    out = {"nu": float(nu), "tau": float(tau), "streams": streams,
           "log_lambda": float(special.logsumexp(pooled) - math.log(len(pooled)))}
    if len(seeds) >= 2:
        diff = abs(streams[0]["log_lambda"] - streams[1]["log_lambda"])
        why = []
        if not diff <= STREAM_DIFF_MAX:
            why.append(f"stream difference {diff:.3g}")
        for r, st in enumerate(streams):
            if not st["ess"] >= ESS_MIN:
                why.append(f"ESS {st['ess']:.0f} in stream {r}")
            if not st["khat"] < KHAT_MAX:
                why.append(f"k_hat {st['khat']:.3f} in stream {r}")
        out.update(stream_diff=float(diff), ok=not why, problems=why)
    return out


def lambda_inf(tau, u, des):
    """nu = inf: log Lambda = -g(tau^2 I) / 2, exact."""
    return -0.5 * g_iso(tau, u, des)


def stage2_eval(tau, u, des, n, seed_base, q_prior):
    """log L over the grid at tau (finite nu: two streams, seeds seed_base + 10 j + r; inf exact)."""
    per = {}
    for j, nu in enumerate(FINITE_NU):
        per[nu_key(nu)] = lambda_finite(nu, tau, u, des, n, [seed_base + 10 * j + r for r in range(N_STREAMS)],
                                        q_prior)
    per["inf"] = {"nu": "inf", "tau": float(tau), "log_lambda": lambda_inf(tau, u, des), "exact": True, "ok": True}
    bad = [f"ν = {k}: " + ", ".join(per[k]["problems"]) for k in NU_KEYS[:-1] if not per[k]["ok"]]
    return {"tau": float(tau), "n": int(n), "seed_base": int(seed_base), "per_nu": per, "ok": not bad,
            "problems": bad, "log_L": [per[k]["log_lambda"] for k in NU_KEYS]}


def weights_from(log_L, prior):
    lp = np.log(np.asarray(prior, dtype=float)) + np.asarray(log_L, dtype=float)
    w = np.exp(lp - special.logsumexp(lp))
    return [float(v) for v in w]


def p_le4(weights):
    return float(weights[0] + weights[1])


def inv_nu_prior():
    """pi uniform in 1/nu on [0, 1/3]: each grid point weighted by its cell (edges at the midpoints of 1/nu)."""
    x = [1.0 / v for v in FINITE_NU] + [0.0]
    edges = [1.0 / 3.0] + [(x[i] + x[i + 1]) / 2.0 for i in range(len(x) - 1)] + [0.0]
    return [(edges[i] - edges[i + 1]) * 3.0 for i in range(len(x))]


# ---------------------------------------------------------------- labels and rules (pure)
def gate(est, tau_gate):
    """Labels 1 and 2 from Stage 1's REML record: (label or None, reason)."""
    if est["at_upper_bound"]:
        return LBL_NOT_EVAL.format("bound"), "bound"
    lo = est["interval_68"][0]
    if lo == "not determined":
        return LBL_NOT_EVAL.format("τ̂_HF interval's lower end not determined"), "lower end not determined"
    if lo == 0.0 or est["tau_hat"] < float(tau_gate):
        return LBL_NO_EXCESS, "gate"
    return None, "passed"


def scale_inside(interval, ref=SCALE_REF):
    """Whether ref lies inside the 68% interval; None when its upper end is "not determined" (not covered by the
    pre-registration: the full stage stops before L(nu))."""
    lo, hi = interval
    if isinstance(hi, str):
        if hi.startswith(">"):
            return bool(lo <= ref)
        return None
    return bool(lo <= ref <= hi)


def pass_rule(P_t3, P_t10, P_het):
    """Rules (a)-(c) on the per-mock P_s; returns (ok, failing parts, record)."""
    P_t3, P_t10, P_het = (np.asarray(a, dtype=float) for a in (P_t3, P_t10, P_het))
    heavy_t10 = int(np.sum(P_t10 > HEAVY))
    light_t3 = int(np.sum(P_t3 < LIGHT))
    heavy_het = int(np.sum(P_het > HEAVY))
    delta_b = float(np.mean(P_t3) - np.mean(P_t10))
    parts = []
    if not (heavy_t10 <= MAX_MISLABEL and light_t3 <= MAX_MISLABEL):
        parts.append(PART_A)
    if not delta_b >= DELTA_B_MIN:
        parts.append(PART_B)
    if not heavy_het <= MAX_MISLABEL:
        parts.append(PART_C)
    rec = {"heavy_in_t10": heavy_t10, "light_in_t3": light_t3, "heavy_in_het": heavy_het, "delta_b": delta_b,
           "a": not (PART_A in parts), "b": not (PART_B in parts), "c": not (PART_C in parts)}
    return not parts, parts, rec


def trunc_rule(P_trunc, P_t3, delta_b, n_failed):
    """Rules (d), (e) and the truncation-failed count on the accepted truncated mocks."""
    P_trunc = np.asarray(P_trunc, dtype=float)
    light = int(np.sum(P_trunc < LIGHT))
    diff = abs(float(np.mean(P_trunc)) - float(np.mean(P_t3))) if len(P_trunc) else float("nan")
    d_ok = bool(len(P_trunc) > 0 and diff <= delta_b)
    e_ok = bool(light <= MAX_MISLABEL)
    f_ok = bool(int(n_failed) <= MAX_TRUNC_FAILED)
    return d_ok and e_ok and f_ok, {"mean_diff": diff, "light_in_trunc": light, "n_failed": int(n_failed),
                                    "d": d_ok, "e": e_ok, "failed_ok": f_ok}


def label_from_p(P, inside):
    """Labels 4-6 with the conditional phrase and, under 4 or 5, the scale suffix; returns (label, scale_suffix)."""
    if P < LIGHT:
        base = LBL_LIGHT
    elif P > HEAVY:
        base = LBL_HEAVY
    else:
        return LBL_WEAK + COND, False
    suffix = inside is False
    return base + COND + (SCALE_SUFFIX if suffix else ""), suffix


def p_int_block(w_flat, w_inv, p_cal, p_max):
    """p_int = sum_nu w(nu) p_cal(nu, tau) at tau_hat_obs (primary) and with the maximum over the three tau (bound),
    with the flat (primary) and the 1/nu weights, next to the prior-only values."""
    pc = [float(p_cal[k]) for k in NU_KEYS]
    pm = [float(p_max[k]) for k in NU_KEYS]
    dot = lambda w, p: float(sum(a * b for a, b in zip(w, p)))
    return {"primary": dot(w_flat, pc), "inv_nu": dot(w_inv, pc), "bound": dot(w_flat, pm), "bound_inv_nu": dot(w_inv, pm),
            "bound_note": "at the three checked τ only",
            "prior_only": {"primary": dot(PRIOR_FLAT, pc), "inv_nu": dot(PRIOR_INV_NU, pc),
                           "bound": dot(PRIOR_FLAT, pm), "bound_inv_nu": dot(PRIOR_INV_NU, pm)},
            "p_cal": dict(zip(NU_KEYS, pc)), "p_cal_max_over_tau": dict(zip(NU_KEYS, pm)),
            "source": "results/r2_re_gtp.json refit.<ν>.tau_obs.p_cal.p and p_cal_max_over_tau (never recomputed)",
            "note": "a weighted average of calibrated p values, not itself a calibrated p value for a composite null; "
                    "it inherits R2-RE-GTP's caveats (three τ, coarse grid that stops at ν = 3)"}


def p_int_reading(label, scale_suffix, p):
    """Reading of p_int (primary) against 0.05: only under labels 4 and 5 without the scale suffix."""
    if label.startswith(LBL_WEAK):
        return {"reading": "not read", "reference_prior_only": PRIOR_ONLY_REF,
                "why": "label 6: the weights reflect the grid prior as much as the data"}
    if scale_suffix:
        return {"reading": "not read", "why": "scale differs: transfer not supported"}
    if p < 0.05:
        return {"reading": "below 0.05", "statement": READ_BELOW}
    return {"reading": "at or above 0.05", "statement": READ_ABOVE}


def gtp_p_cal(gtp_rec):
    """p_cal(nu, tau_hat_obs) and its maximum over the three tau from R2-RE-GTP's committed record, checked against
    the values the README quotes (an error, not a label, if they differ)."""
    if gtp_rec.get("status") != "evaluated":
        raise RuntimeError("R2-RE-NU needs R2-RE-GTP's evaluated results/r2_re_gtp.json")
    pc = {k: float(gtp_rec["refit"][k]["tau_obs"]["p_cal"]["p"]) for k in NU_KEYS}
    pm = {k: float(gtp_rec["p_cal_max_over_tau"][k]) for k in NU_KEYS}
    bad = [f"{k}: {pc[k]} vs {P_CAL_README[k]}" for k in NU_KEYS if abs(pc[k] - P_CAL_README[k]) > P_CAL_README_ATOL]
    bad += [f"max {k}: {pm[k]} vs {P_CAL_MAX_README[k]}" for k in NU_KEYS
            if abs(pm[k] - P_CAL_MAX_README[k]) > P_CAL_README_ATOL]
    if bad:
        raise RuntimeError("r2_re_gtp.json's p_cal differ from the README's values: " + "; ".join(bad))
    return pc, pm


# ---------------------------------------------------------------- mocks (known-answer check)
def eps_draw(seed_eps, s, n_a):
    return np.random.default_rng(int(seed_eps) + int(s)).standard_normal(int(n_a))


def het_d(tau, c_g):
    """d_g proportional to c_g, scaled so that the mean of d_g over the groups is tau^2."""
    c = np.asarray(c_g, dtype=float)
    return float(tau) ** 2 * c / float(np.mean(c))


def mock_b(kind, s, tau, des, seeds):
    """b_s of the t_3, t_10 and heteroscedastic injections."""
    n_g = des["n_g"]
    if kind == "t3":
        return math.sqrt(t_scale2(tau, 3)) * np.random.default_rng(seeds["t3"] + s).standard_t(3, n_g)
    if kind == "t10":
        return math.sqrt(t_scale2(tau, 10)) * np.random.default_rng(seeds["t10"] + s).standard_t(10, n_g)
    if kind == "het":
        return np.random.default_rng(seeds["het"] + s).standard_normal(n_g) * np.sqrt(het_d(tau, des["c_g"]))
    raise ValueError(kind)


def passes_cut(eps, b, des, cut):
    """The GLS residual r = C_a P (K eps + Z b) on the HF rows has no |r_i| > cut sigma_i."""
    r = des["R_eps"] @ eps + des["R_b"] @ b
    return bool(np.all(np.abs(r) <= float(cut) * des["sig_hf"]))


def trunc_draw(s, tau, des, seeds, cut, attempts):
    """Whole-mock rejection: attempt 0 is the plain t_3 mock (eps_s, t_s); attempts k = 1, ..., attempts - 1 draw eps
    (n_a values) then t (n_g values, standard_t(3)) from default_rng(trunc_joint + 1000 s + k). Returns (eps, b, k)
    of the first passing attempt, or (None, None, None)."""
    s3 = math.sqrt(t_scale2(tau, 3))
    eps = eps_draw(seeds["eps"], s, des["n_a"])
    b = mock_b("t3", s, tau, des, seeds)
    if passes_cut(eps, b, des, cut):
        return eps, b, 0
    for k in range(1, int(attempts)):
        rng = np.random.default_rng(int(seeds["trunc_joint"]) + 1000 * int(s) + k)
        eps = rng.standard_normal(des["n_a"])
        b = s3 * rng.standard_t(3, des["n_g"])
        if passes_cut(eps, b, des, cut):
            return eps, b, k
    return None, None, None


def mock_u(eps, b, des):
    """u_s = B eps_s + M b_s."""
    return des["B"] @ eps + des["M"] @ b


def mock_eval(u_s, des, n, seed_base, s, q_prior, reml_tau):
    """tau_hat_s by the reduced form, then L_s(nu) at tau_hat_s (one stream of n, seeds seed_base + 10 s + j; inf
    exact) and P_s(nu <= 4) with flat weights; tau_hat_s < 1e-3: every L_s = 1, P_s = 1/3."""
    est = shape.tau_refit(des["Q"].T @ u_s, des["lam"], reml_tau)
    t = float(est["tau_hat"])
    if est["at_zero"]:
        return {"tau_hat": t, "P": 1.0 / 3.0, "ess": [None] * 5, "khat": [None] * 5, "at_zero": True}
    m = posterior_m(t, u_s, des)
    logL, ess, kh = [], [], []
    for j, nu in enumerate(FINITE_NU):
        st = stream_stats(is_log_weights(nu, t, u_s, des, m, n, seed_base + 10 * s + j, q_prior))
        logL.append(st["log_lambda"])
        ess.append(st["ess"])
        kh.append(st["khat"])
    logL.append(lambda_inf(t, u_s, des))
    return {"tau_hat": t, "P": p_le4(weights_from(logL, PRIOR_FLAT)), "ess": ess, "khat": kh, "at_zero": False}


def run_mocks(kind, s_list, tau, des, P, reml_tau, log=None):
    """The mocks of one injection: per-mock tau_hat_s, P_s, ESS and k_hat (and for trunc the accepted attempt)."""
    seeds = P["nu_mock_seeds"]
    is_seed = seeds["is_" + kind]
    n, q = int(P["nu_n_is_mock"]), float(P["nu_q_prior_frac"])
    out = {"s": [], "tau_hat": [], "P": [], "ess": [], "khat": []}
    if kind == "trunc":
        out.update(attempt=[], failed=[])
    for s in s_list:
        s = int(s)
        if kind == "trunc":
            eps, b, k = trunc_draw(s, tau, des, seeds, P["nu_cut_sigma"], P["nu_cut_attempts"])
            if eps is None:
                out["failed"].append(s)
                continue
            out["attempt"].append(int(k))
        else:
            eps = eps_draw(seeds["eps"], s, des["n_a"])
            b = mock_b(kind, s, tau, des, seeds)
        r = mock_eval(mock_u(eps, b, des), des, n, is_seed, s, q, reml_tau)
        out["s"].append(s)
        for key in ("tau_hat", "P", "ess", "khat"):
            out[key].append(r[key])
    if log:
        log(f"  R2-RE-NU: {len(out['s'])} {kind} mocks")
    return out


def _q(a, qs=(0.05, 0.25, 0.5, 0.75, 0.95)):
    a = np.asarray([v for v in a if v is not None and np.isfinite(v)], dtype=float)
    return {str(q): (float(np.quantile(a, q)) if len(a) else None) for q in qs}


def mock_summary(rec, tau_gate, attempts=None):
    """Reported per injection: mean P_s, label counts, quantiles of P_s and tau_hat_s, the proxy fraction
    tau_hat_s >= 0.02, the fraction of mocks with ESS < 200 or k_hat >= 0.7 in any nu (M5), ESS and k_hat quantiles."""
    Ps = np.asarray(rec["P"], dtype=float)
    n = len(Ps)
    bad = [any((e is not None and e < ESS_MIN) or (k is not None and not k < KHAT_MAX) for e, k in zip(es, ks))
           for es, ks in zip(rec["ess"], rec["khat"])]
    flat_e = [e for es in rec["ess"] for e in es]
    flat_k = [k for ks in rec["khat"] for k in ks]
    out = {"n": n, "mean_P": float(Ps.mean()) if n else None,
           "n_heavy": int(np.sum(Ps > HEAVY)), "n_light": int(np.sum(Ps < LIGHT)),
           "frac_heavy": float(np.mean(Ps > HEAVY)) if n else None,
           "quantiles_P": _q(Ps), "quantiles_tau_hat": _q(rec["tau_hat"]),
           "frac_tau_ge_gate_proxy": float(np.mean(np.asarray(rec["tau_hat"]) >= float(tau_gate))) if n else None,
           "frac_tau_ge_gate_proxy_note": "proxy for passing the Stage-1 gate: the mock refits use interval=False",
           "frac_ess_or_khat_flag": float(np.mean(bad)) if n else None,
           "quantiles_ess": _q(flat_e), "quantiles_khat": _q(flat_k)}
    if "attempt" in rec:
        # rejected attempts: k before a mock accepted at attempt k, all of them for a "truncation failed" mock
        out.update(n_failed=len(rec["failed"]), failed=list(rec["failed"]),
                   n_rejected_attempts=int(sum(rec["attempt"]) + len(rec["failed"]) * int(attempts or 0)),
                   n_accepted_at_0=int(sum(1 for k in rec["attempt"] if k == 0)))
    return out


# ---------------------------------------------------------------- Stage 1 and checks
def stage1(L, y, Cb, rows_a, groups, fns, interval=True):
    """R2-RE's REML on rows_a with the HF groups (grid 0, 0.01, ..., 0.5, bounded refinement, 68% interval)."""
    est = fns["reml_tau"](lambda t: fns["reml_m2l"](L, y, Cb, rows_a, groups, t), TAU_MAX, TAU_STEP, interval=interval)
    keep = ("tau_hat", "m2l_min", "refined", "refine_error", "other_local_minima", "at_zero", "at_upper_bound",
            "interval_68", "grid_m2l", "m2l_at_interval")
    out = {k: est[k] for k in keep if k in est}
    if interval:
        out["delta_m2l_at_zero"] = float(est["grid_m2l"][0] - est["m2l_min"])
    return out


def _reproduce_r2_re(L, y, C, rows_a, calib_groups, grid_m2l, fns, tau_rec):
    """R2-RE's reproduction (R2-RE-G's tolerances): tau_hat_obs within TAU_OBS_ATOL, the recorded REML grid
    differences within GRID_ATOL. Returns (record, mismatches, tau_obs)."""
    des, problem = shape.design(L, y, C, rows_a, calib_groups, fns)
    if problem:
        return {"problem": problem}, [problem], None
    v = des["Q"].T @ (des["PZt"] @ np.asarray(y)[np.asarray(rows_a)])
    grid = np.round(np.arange(0.0, TAU_MAX + TAU_STEP / 2, TAU_STEP), 10)
    f = np.array([shape.reml_f(t, v, des["lam"]) for t in grid])
    est = shape.tau_refit(v, des["lam"], fns["reml_tau"])
    gm = np.asarray(grid_m2l, dtype=float)
    rec, bad = {"tau_hat_obs": est["tau_hat"], "recorded": float(tau_rec)}, []
    if len(gm) != len(grid):
        bad.append(f"REML grid has {len(gm)} values, expected {len(grid)}")
    else:
        dg = float(np.max(np.abs((f - f[0]) - (gm - gm[0]))))
        rec["reml_grid_max_abs_diff"] = dg
        if not dg <= shape.GRID_ATOL:
            bad.append(f"REML grid differences off by up to {dg:.3g} (tolerance {shape.GRID_ATOL:g})")
    if not abs(est["tau_hat"] - float(tau_rec)) <= shape.TAU_OBS_ATOL:
        bad.append(f"τ̂_obs {est['tau_hat']!r} vs recorded {tau_rec!r} (absolute {shape.TAU_OBS_ATOL:g})")
    rec["mismatches"] = bad
    return rec, bad, float(est["tau_hat"])


def reduced_form_check(est, u, des):
    """g(tau^2 I) against reml_m2l(tau) - reml_m2l(0) at tau = 0.01, 0.05 and tau_hat_HF (GRID_ATOL)."""
    gm = est["grid_m2l"]
    pts = [(0.01, gm[1]), (0.05, gm[5]), (est["tau_hat"], est["m2l_min"])]
    rows = []
    for t, m2l in pts:
        d = abs(g_iso(t, u, des) - (m2l - gm[0]))
        rows.append({"tau": float(t), "abs_diff": float(d), "ok": bool(d <= shape.GRID_ATOL)})
    return rows


def pointwise_checks(L, y, Cb, rows_a, groups, des, tau, P, fns, n_pw=N_POINTWISE):
    """The first t_3 mocks built in full (y_hat + K eps_s + Z b_s on rows_a): tau_hat_s from reml_m2l with the n_g
    groups against the reduced-form tau_hat_s (TAU_OBS_ATOL)."""
    seeds = P["nu_mock_seeds"]
    rows = []
    for s in range(n_pw):
        eps = eps_draw(seeds["eps"], s, des["n_a"])
        b = mock_b("t3", s, tau, des, seeds)
        t_red = shape.tau_refit(des["Q"].T @ mock_u(eps, b, des), des["lam"], fns["reml_tau"])["tau_hat"]
        y_full = np.array(y, dtype=float)
        y_full[des["rows_a"]] = des["yhat"] + des["K"] @ eps + des["Zm"] @ b
        t_full = fns["reml_tau"](lambda t: fns["reml_m2l"](L, y_full, Cb, rows_a, groups, t), TAU_MAX, TAU_STEP,
                                 interval=False)["tau_hat"]
        rows.append({"s": s, "tau_reduced": float(t_red), "tau_reml_m2l": float(t_full),
                     "ok": bool(abs(t_red - t_full) <= shape.TAU_OBS_ATOL)})
    return rows


def settings_of(P):
    return {**{k: P[k] for k in PREREGISTERED}, "threads": shape.thread_settings()}


def _core(L, y, C, rows_a, hf_rows, calib_groups, P, fns, log, grid_m2l, cid_info, recorded, expected, n_mock_cap):
    """Checks, Stage 1 and the known-answer mocks (the first n_mock_cap of each injection; None: all). Returns
    (rec, ctx): rec the check-stage record, ctx the design objects for the full stage (None after a label)."""
    t_start = CLOCK()
    rows_a = np.asarray(rows_a)
    hf_rows = np.asarray(hf_rows)
    rec = {"headline": "reported, non-decisive: no verdict, label, reading, sub-label, gloss or statement of R2 "
                       "through R2-RE-GTP changes; R2-RE's row stays the headline",
           "transfer_assumption": "the per-SN excess scatter of Hubble-flow SNe beyond C has the same tail shape ν as "
                                  "the calibrator host effects (an assumption, not a result)"}
    checks, seconds = {}, {}
    rec["checks"], rec["seconds"] = checks, seconds

    def stop(label):
        rec["outcome"] = label
        seconds["total"] = CLOCK() - t_start
        log("R2-RE-NU: " + label)
        return rec, None

    # row classes
    n_hf_exp, n_a_exp = expected.get("n_hf", N_HF_EXPECTED), expected.get("n_rows_a", N_ROWS_A_EXPECTED)
    in_a = bool(np.all(np.isin(hf_rows, rows_a)))
    checks["row_classes"] = {"n_hf": int(len(hf_rows)), "n_rows_a": int(len(rows_a)), "hf_all_in_rows_a": in_a,
                             "ok": bool(len(hf_rows) == n_hf_exp and len(rows_a) == n_a_exp and in_a)}
    if not checks["row_classes"]["ok"]:
        return stop(LBL_NOT_EVAL.format("row classes"))
    # grouping and the count check (main grouping only)
    groups = hf_groups(C, hf_rows, P["nu_group_corr"])
    groups_s = hf_groups(C, hf_rows, P["nu_group_corr_sens"])
    cc = count_check(len(groups), cid_info["n_cid"])
    checks["grouping"] = {"threshold": P["nu_group_corr"], "n_groups": len(groups),
                          "largest_group": int(max(len(g) for g in groups)), "count_check": cc,
                          "cid": cid_info,
                          "sensitivity": {"threshold": P["nu_group_corr_sens"], "n_groups": len(groups_s),
                                          "largest_group": int(max(len(g) for g in groups_s))}}
    if not cc["ok"]:
        return stop(LBL_NOT_EVAL.format("grouping count check"))
    # the design: Cholesky factor of C and M's eigenvalue rule
    t0 = CLOCK()
    try:
        des, problem = hf_design(L, y, C, rows_a, groups, fns)
    except (np.linalg.LinAlgError, ValueError) as e:
        if not fns["is_fit_failure"](e):
            raise
        des, problem = None, f"fit: {e}"
    if des is not None:
        checks["design"] = {"n_g": des["n_g"], "rank_M": des["rank_M"], "n_zero_eigenvalues": des["n_clipped"],
                            "lam_min_raw": des["lam_min_raw"], "lam_max": des["lam_max"]}
    if problem:
        return stop(LBL_NOT_EVAL.format(problem))
    # R2-RE's reproduction on the data
    rep, bad, tau_obs = _reproduce_r2_re(L, y, C, rows_a, calib_groups, grid_m2l, fns,
                                         recorded.get("tau_obs", shape.RECORDED_TAU_OBS))
    checks["r2_re_reproduction"] = rep
    seconds["design_and_reproduction"] = CLOCK() - t0
    if bad:
        return stop(LBL_NOT_EVAL.format("R2-RE reproduction: " + "; ".join(bad)))
    # Stage 1
    t0 = CLOCK()
    try:
        est = stage1(L, y, C, rows_a, groups, fns)
    except (np.linalg.LinAlgError, ValueError) as e:
        if not fns["is_fit_failure"](e):
            raise
        return stop(LBL_NOT_EVAL.format(f"fit: {e}"))
    u = u_of(y, des)
    checks["reduced_form"] = reduced_form_check(est, u, des)
    if not all(r["ok"] for r in checks["reduced_form"]):
        return stop(LBL_NOT_EVAL.format("reduced form"))
    s1 = {"main": est, "tau_hat_HF": est["tau_hat"], "interval_68": est["interval_68"],
          "ratio_to_tau_obs": est["tau_hat"] / TAU_OBS_RATIO, "tau_obs_reference": TAU_OBS_RATIO,
          "scale_reference_inside_interval": scale_inside(est["interval_68"]),
          "delta_m2l_at_zero": est["delta_m2l_at_zero"], "n_groups": len(groups)}
    # reported only: the 0.45 grouping and the V(tau_obs) base
    try:
        e045 = stage1(L, y, C, rows_a, groups_s, fns)
        s1["grouping_045"] = {"n_groups": len(groups_s), **{k: e045[k] for k in
                              ("tau_hat", "interval_68", "at_zero", "at_upper_bound", "delta_m2l_at_zero")}}
    except (np.linalg.LinAlgError, ValueError) as e:
        if not fns["is_fit_failure"](e):
            raise
        s1["grouping_045"] = {"status": f"not evaluable (fit: {e})"}
    V = fns["with_re"](C, calib_groups, tau_obs)
    try:
        ev = stage1(L, y, V, rows_a, groups, fns)
        s1["vbase"] = {"tau_obs": tau_obs, **{k: ev[k] for k in
                       ("tau_hat", "interval_68", "at_zero", "at_upper_bound", "delta_m2l_at_zero")}}
    except (np.linalg.LinAlgError, ValueError) as e:
        if not fns["is_fit_failure"](e):
            raise
        s1["vbase"] = {"tau_obs": tau_obs, "status": f"not evaluable (fit: {e})"}
    rec["stage1"] = s1
    seconds["stage1"] = CLOCK() - t0
    lab, why = gate(est, P["nu_tau_gate"])
    rec["gate"] = why
    log(f"R2-RE-NU: tau_hat_HF {est['tau_hat']:.4f} mag, 68% {est['interval_68']}; gate {why}")
    if lab:
        return stop(lab)
    tau = float(est["tau_hat"])
    # the known-answer check: pointwise first, then the mocks
    t0 = CLOCK()
    pw = pointwise_checks(L, y, C, rows_a, groups, des, tau, P, fns)
    checks["pointwise"] = pw
    seconds["pointwise"] = CLOCK() - t0
    if not all(r["ok"] for r in pw):
        return stop(LBL_NOT_EVAL.format("pointwise check"))
    n_m = int(P["nu_n_mocks"]) if n_mock_cap is None else min(int(P["nu_n_mocks"]), int(n_mock_cap))
    mocks, msum = {}, {}
    cx = {"des": des, "groups": groups, "groups_s": groups_s, "u": u, "tau": tau, "tau_obs": tau_obs, "V": V}
    t0 = CLOCK()
    if n_mock_cap is not None:
        # the full stage's recomputation: the first mocks of all four injections, no rule (it applies to all 200)
        for kind in INJECTIONS:
            mocks[kind] = run_mocks(kind, range(n_m), tau, des, P, fns["reml_tau"], log)
        rec["mocks"], rec["outcome"] = mocks, None
        seconds["mocks"] = CLOCK() - t0
        return rec, cx
    for kind in ("t3", "t10", "het"):
        mocks[kind] = run_mocks(kind, range(n_m), tau, des, P, fns["reml_tau"], log)
        msum[kind] = mock_summary(mocks[kind], P["nu_tau_gate"])
    ok, parts, rule = pass_rule(mocks["t3"]["P"], mocks["t10"]["P"], mocks["het"]["P"])
    rec["mocks"], rec["mock_summary"], rec["known_answer"] = mocks, msum, {"rules_abc": rule}
    rec["known_answer"]["frac_t3_heavy_M5"] = msum["t3"]["frac_heavy"]
    if not ok:
        seconds["mocks"] = CLOCK() - t0
        rec["known_answer"]["outcome"] = "failed (" + "; ".join(parts) + ")"
        return stop(LBL_METHOD.format("; ".join(parts)))
    mocks["trunc"] = run_mocks("trunc", range(n_m), tau, des, P, fns["reml_tau"], log)
    msum["trunc"] = mock_summary(mocks["trunc"], P["nu_tau_gate"], P["nu_cut_attempts"])
    ok_t, trule = trunc_rule(mocks["trunc"]["P"], mocks["t3"]["P"], rule["delta_b"], len(mocks["trunc"]["failed"]))
    rec["known_answer"]["rules_de"] = trule
    seconds["mocks"] = CLOCK() - t0
    if not ok_t:
        rec["known_answer"]["outcome"] = "failed (selection)"
        return stop(LBL_SELECTION)
    rec["known_answer"]["outcome"] = "passed"
    rec["outcome"] = None
    seconds["total"] = CLOCK() - t_start
    log("R2-RE-NU: known-answer check passed")
    return rec, cx


def run_check(L, y, C, rows_a, hf_rows, calib_groups, P, fns, log, grid_m2l, cid_info, recorded=None,
              expected=None):
    """The check stage: r2_re_nu_check.json's record (never L(nu) on the data)."""
    rec, _ = _core(L, y, C, rows_a, hf_rows, calib_groups, P, fns, log, grid_m2l, cid_info, recorded or {},
                   expected or {}, None)
    out = {"stage": "check", "settings": settings_of(P), **rec}
    out["status"] = "known-answer check passed" if rec.get("outcome") is None else "final: " + rec["outcome"]
    return out


def check_log_line(rec):
    """The line written into log.md (and committed) before the full stage starts."""
    s1 = rec.get("stage1", {})
    t = s1.get("tau_hat_HF")
    ts = "not computed" if t is None else f"{t:.4f} mag (68% {s1.get('interval_68')})"
    ka = rec.get("known_answer", {}).get("outcome", "not run")
    return (f"R2-RE-NU check stage: τ̂_HF {ts}; gate {rec.get('gate', 'not reached')}; known-answer check {ka}; "
            f"outcome {rec.get('outcome') or 'continue to the full stage'}")


def check_record_problems(check_rec, settings):
    """Why a check record cannot be the basis of a full stage (an error)."""
    if not isinstance(check_rec, dict) or check_rec.get("stage") != "check" or "settings" not in check_rec:
        return ["the check record is a stub or not a check-stage record"]
    cs = check_rec["settings"]
    bad = [f"{k}: check stage {json_like(cs.get(k))!r}, now {json_like(settings.get(k))!r}" for k in PREREGISTERED
           if json_like(cs.get(k)) != json_like(settings.get(k))]
    return bad + shape.thread_problems(cs.get("threads"), settings.get("threads"))


def _compare(a, b, path=""):
    """Exact comparison of two JSON-like values (after a JSON round trip); returns the differing paths."""
    a, b = json_like(a), json_like(b)
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append(f"{path}.{k}")
            else:
                out += _compare(a[k], b[k], f"{path}.{k}")
        return out
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return [path + " (length)"]
        out = []
        for i, (x, z) in enumerate(zip(a, b)):
            out += _compare(x, z, f"{path}[{i}]")
        return out
    return [] if a == b else [path]


def _first(m, n):
    """The first n mocks of one injection's record (by mock index s; trunc keeps its failed list up to s < n)."""
    keep = [i for i, s in enumerate(m["s"]) if s < n]
    out = {k: [m[k][i] for i in keep] for k in ("s", "tau_hat", "P", "ess", "khat")}
    if "attempt" in m:
        out["attempt"] = [m["attempt"][i] for i in keep]
        out["failed"] = [s for s in m["failed"] if s < n]
    return out


def sensitivity_p(tau, u, des, P, seed_base, at_zero=False):
    """P(nu <= 4) (flat; 1/nu reported) with the base N, two streams and the check (no escalation)."""
    if at_zero:
        return {"tau": float(tau), "at_zero": True, "P_le4": 1.0 / 3.0, "note": "τ̂ < 1e-3: every L = 1"}
    ev = stage2_eval(tau, u, des, int(P["nu_n_is"]), seed_base, float(P["nu_q_prior_frac"]))
    wf = weights_from(ev["log_L"], PRIOR_FLAT)
    return {"tau": float(tau), "log_L": ev["log_L"], "P_le4": p_le4(wf),
            "P_le4_inv_nu": p_le4(weights_from(ev["log_L"], PRIOR_INV_NU)), "check_ok": ev["ok"],
            "check_problems": ev["problems"], "per_nu": _per_nu_diag(ev)}


def _per_nu_diag(ev):
    return {k: {kk: v.get(kk) for kk in ("log_lambda", "stream_diff", "ok", "streams") if kk in v}
            for k, v in ev["per_nu"].items()}


def run_full(L, y, C, rows_a, hf_rows, calib_groups, P, fns, log, grid_m2l, cid_info, check_rec, gtp_rec,
             recorded=None, expected=None):
    """The full stage: recompute the checks, Stage 1 and the first 20 mocks (they must equal the check record), then
    Stage 2 (with the escalation), the weights, the label, p_int and the sensitivities."""
    t_start = CLOCK()
    out = {"stage": "full", "settings": settings_of(P)}
    if check_rec.get("outcome") is not None:
        out.update(status="final from the check stage", label=check_rec["outcome"],
                   stage1={k: check_rec.get("stage1", {}).get(k) for k in ("tau_hat_HF", "interval_68")},
                   gate=check_rec.get("gate"), known_answer=check_rec.get("known_answer", {}).get("outcome"))
        log("R2-RE-NU: " + out["label"] + " (the check stage's outcome is final)")
        return out
    p_cal, p_max = gtp_p_cal(gtp_rec)
    rec, cx = _core(L, y, C, rows_a, hf_rows, calib_groups, P, fns, log, grid_m2l, cid_info, recorded or {},
                    expected or {}, N_REPRO_MOCKS)
    # the recomputed part must equal the check record exactly
    diffs = []
    if rec.get("outcome") is not None:
        diffs.append(f"outcome {rec['outcome']!r}")
    for key in ("checks", "stage1", "gate"):
        sub = rec.get(key)
        ref = check_rec.get(key)
        if key == "checks":
            sub = {k: v for k, v in (sub or {}).items()}
            ref = {k: v for k, v in (ref or {}).items()}
        diffs += _compare(sub, ref, key)
    for kind in INJECTIONS:
        if kind not in (rec.get("mocks") or {}) or kind not in check_rec.get("mocks", {}):
            diffs.append(f"mocks.{kind} missing")
            continue
        diffs += _compare(_first(rec["mocks"][kind], N_REPRO_MOCKS), _first(check_rec["mocks"][kind], N_REPRO_MOCKS),
                          f"mocks.{kind}")
    out["checks"] = {"check_stage_reproduced": not diffs, "differences": diffs[:50]}
    if diffs:
        out.update(status="evaluated", label=LBL_NOT_EVAL.format("check-stage reproduction"))
        log("R2-RE-NU: " + out["label"])
        return out
    s1 = check_rec["stage1"]
    out["stage1"] = {k: s1[k] for k in ("tau_hat_HF", "interval_68", "ratio_to_tau_obs",
                                        "scale_reference_inside_interval", "delta_m2l_at_zero")}
    inside = s1["scale_reference_inside_interval"]
    if inside is None:
        raise RuntimeError("R2-RE-NU full stage stopped before L(ν): the upper end of τ̂_HF's 68% interval is "
                           "'not determined', a case the pre-registration's scale condition does not cover; decide and "
                           "amend the README first")
    des, u, tau = cx["des"], cx["u"], cx["tau"]
    q = float(P["nu_q_prior_frac"])
    # Stage 2 on the data, with one escalation
    t0 = CLOCK()
    attempts = [stage2_eval(tau, u, des, int(P["nu_n_is"]), int(P["nu_is_seed"]), q)]
    if not attempts[0]["ok"]:
        log("R2-RE-NU: accuracy check failed (" + "; ".join(attempts[0]["problems"]) + "); escalating")
        attempts.append(stage2_eval(tau, u, des, int(P["nu_n_is_escalate"]), int(P["nu_is_seed_escalate"]), q))
    out["stage2"] = {"attempts": [{"n": a["n"], "seed_base": a["seed_base"], "ok": a["ok"], "problems": a["problems"],
                                   "per_nu": _per_nu_diag(a)} for a in attempts]}
    out["seconds_stage2"] = CLOCK() - t0
    final = attempts[-1]
    if not final["ok"]:
        out.update(status="evaluated", label=LBL_METHOD.format(PART_MC))
        log("R2-RE-NU: " + out["label"])
        return out
    log_L = final["log_L"]
    wf, wi = weights_from(log_L, PRIOR_FLAT), weights_from(log_L, PRIOR_INV_NU)
    Pf = p_le4(wf)
    label, suffix = label_from_p(Pf, inside)
    pint = p_int_block(wf, wi, p_cal, p_max)
    out.update(status="evaluated", log_L_nu=dict(zip(NU_KEYS, log_L)), weights={"flat": dict(zip(NU_KEYS, wf)),
               "inv_nu": dict(zip(NU_KEYS, wi))}, P_le4=Pf, P_le4_inv_nu=p_le4(wi),
               P_le4_prior={"flat": 1.0 / 3.0, "inv_nu": 0.375}, label=label, scale_suffix=suffix,
               p_int=pint, p_int_reading=p_int_reading(label, suffix, pint["primary"]))
    log(f"R2-RE-NU: P(ν ≤ 4) {Pf:.4f}; {label}; p_int {pint['primary']:.4f}")
    # sensitivities (reported only, no escalation)
    t0 = CLOCK()
    sens = {}
    prof, k = {}, 0
    for m in P["nu_profile_m"]:
        if float(m) == 1.0:
            prof[f"{float(m):g}"] = {"tau": tau, "log_L": log_L, "check_ok": True, "from": "primary"}
            continue
        prof[f"{float(m):g}"] = sensitivity_p(float(m) * tau, u, des, P, int(P["nu_profile_seed"]) + 100 * k)
        prof[f"{float(m):g}"]["seed_base"] = int(P["nu_profile_seed"]) + 100 * k
        k += 1
    lp = [max(prof[key]["log_L"][i] for key in prof) for i in range(len(NU_KEYS))]
    sens["profile"] = {"by_m": prof, "log_L_prof": dict(zip(NU_KEYS, lp)),
                       "P_le4": p_le4(weights_from(lp, PRIOR_FLAT)),
                       "check_ok": all(v["check_ok"] for v in prof.values())}
    vb = check_rec["stage1"].get("vbase", {})
    if "tau_hat" in vb and not vb["at_upper_bound"]:
        desv, probv = hf_design(L, y, cx["V"], rows_a, cx["groups"], fns)
        if probv:
            sens["vbase"] = {"status": f"not evaluable ({probv})"}
        else:
            sens["vbase"] = sensitivity_p(vb["tau_hat"], u_of(y, desv), desv, P, int(P["nu_vbase_seed"]),
                                          at_zero=bool(vb["at_zero"]))
    else:
        sens["vbase"] = {"status": vb.get("status", "not evaluable (bound)")}
    g45 = check_rec["stage1"].get("grouping_045", {})
    if "tau_hat" in g45 and not g45["at_upper_bound"]:
        des45, prob45 = hf_design(L, y, C, rows_a, cx["groups_s"], fns)
        if prob45:
            sens["grouping_045"] = {"status": f"not evaluable ({prob45})"}
        else:
            sens["grouping_045"] = sensitivity_p(g45["tau_hat"], u_of(y, des45), des45, P,
                                                 int(P["nu_group_sens_seed"]), at_zero=bool(g45["at_zero"]))
    else:
        sens["grouping_045"] = {"status": g45.get("status", "not evaluable (bound)")}
    out["sensitivities"] = sens
    out["seconds"] = {"stage2": out.pop("seconds_stage2"), "sensitivities": CLOCK() - t0, "total": CLOCK() - t_start}
    return out


def summary(out):
    """Short summary for summary.json (R2_RE_NU)."""
    s = {"status": out.get("status"), "label": out.get("label")}
    for k in ("P_le4", "P_le4_inv_nu"):
        if k in out:
            s[k] = out[k]
    if "p_int" in out:
        s["p_int"] = out["p_int"]["primary"]
        s["p_int_bound"] = out["p_int"]["bound"]
        s["p_int_reading"] = out["p_int_reading"]["reading"]
    st = out.get("stage1") or {}
    if st.get("tau_hat_HF") is not None:
        s["tau_hat_HF"] = st["tau_hat_HF"]
        s["interval_68"] = st.get("interval_68")
    return s
