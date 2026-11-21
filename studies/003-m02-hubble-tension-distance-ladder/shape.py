"""R2-RE-G (README section 2, addendum 2026-11-21, T-055): a composite shape test of one offset host against
diffuse host scatter.

On the NGC 4258-only system (rows_a), with X the columns of L fitted there and C_a = C on rows_a:
P = C_a^-1 - C_a^-1 X (X^T C_a^-1 X)^-1 X^T C_a^-1, Z = (h_1, ..., h_37) the hosts' calibrator SN indicators,
M = Z^T P Z, u = Z^T P y, z_j = u_j / sqrt(M_jj) (the one-extra-column GLS t statistic of host j),
G = max_j z_j^2 / sum_j z_j^2. z = W y with W = diag(M_jj^-1/2) Z^T P (W X = 0).

Under V(tau) = C + tau^2 Z Z^T: u ~ N(0, M + tau^2 M^2); R2-RE's -2 l_R(tau) - (-2 l_R(0)) equals
f(tau; u) = sum_i [log(1 + tau^2 lam_i) - tau^2 v_i^2 / (1 + tau^2 lam_i)], M = Q diag(lam) Q^T, v = Q^T u
(eigenvalues with |lam| < 1e-10 max lam set to 0). tau_hat = R2-RE's reml_tau applied to f.
Test of one data vector: k = #{i: G_i^in(tau_hat) >= G} over N_in exact inner draws z_i = diag(M_jj^-1/2) Q
diag(sqrt(lam (1 + tau_hat^2 lam))) e_i, e_i the rows of one fixed matrix (default_rng(g_inner_seed)),
p_boot = (1 + k) / (1 + N_in), label rob.three_way(k, N_in, "excluded", "not excluded").

Two stages (README): the power stage writes power, size and curve (no G_obs, no z_j of other hosts, no sum of
z^2); the full stage recomputes it (its counts must equal the power record's) and then computes G_obs, p_G
and the reading.

run.py passes its own functions in (`fns`); this module does not import run (AGENTS.md section 2).
"""
import hashlib
import json
import os
import time
from pathlib import Path

import numpy as np
from scipy import linalg

import onehost
import rob
import sel

# ---------------------------------------------------------------- recorded values and tolerances (rule (1))
RECORDED_TAU_OBS = 0.07669875579792439        # R2-RE tau_hat (r2_re.json)
TAU_OBS_ATOL = 2e-5                           # absolute: twice the optimiser's xatol
GRID_ATOL = 1e-5                              # f(tau_i) - f(0) vs grid_m2l_i - grid_m2l_0, absolute
RECORDED_DELTA = onehost.RECORDED_DELTA       # 0.33634 (R2-RE-D)
DELTA_ATOL = onehost.DELTA_ATOL               # 5e-6 absolute
RECORDED_SIGMA_DELTA = 0.09251604267299487    # R2-RE-D sigma_delta
RECORDED_Z_OBS = 3.6354437025541553           # R2-RE-D delta_hat / sigma_delta
REL_TOL = 1e-6                                # sigma_delta and z_obs, relative
RECORDED_TAU_N = sel.RECORDED_TAU_N           # 0.03137144323410943 (R2-RE-N5584)
REML_GRID_SOURCE = "results/r2_re.json reml.grid_m2l (R2-RE, 51 values at tau = 0, 0.01, ..., 0.50 mag)"
TAU_MAX, TAU_STEP = 0.5, 0.01                 # reml_tau(f, 0.5, 0.01, interval=False)
Z_ATOL = 1e-8                                 # W y against one-column GLS fits
POINT_TAU_ATOL = 2e-5                         # reduced-form tau_hat against reml_tau on reml_m2l
N_POINTWISE = 3                               # first simulations of VHAT and OANY checked in full
EIG_RTOL = 1e-10                              # |lam| < 1e-10 max lam -> 0
G_DECIMALS, TAU_DECIMALS = 5, 6               # per-simulation files
TIE_G = 1e-5                                  # tests: |G_s - G_obs| <= 1e-5 is a rounding tie
TIME_SIMS = 1000                              # runtime guard: the first 1,000 VHAT simulations are timed
CHUNK = 500                                   # simulations generated at a time
CLOCK = time.perf_counter                     # tests may replace it

EXCL, NOT_EXCL = "excluded", "not excluded"
UNDET_MC = "undetermined (Monte Carlo)"
READ_UNDERPOWERED = "undetermined (underpowered)"
SUB_LABEL = "diffuse excluded; test underpowered against the σ-matched alternative"
READ_PREFERRED = "one offset host preferred over diffuse scatter"
READ_NOT_EXCL = "diffuse scatter not excluded"
READ_UNDET_MC = "undetermined (Monte Carlo)"
NE_RUNTIME = "not evaluated (runtime)"
RUNTIME = "runtime"                           # the rule-(1) reason of the runtime guard

SECTION5 = {
    "preferred": ("section 5 states that, with τ refitted in every simulation and the host chosen inside the "
                  "statistic, the concentration of the calibrator offsets in one host is unusual under diffuse "
                  "host scatter of the fitted size; R2-RE-D's reading stays recorded, glossed 'a powered composite "
                  "shape test prefers one offset host (R2-RE-G)', with the caveats that G's form was proposed after "
                  "the data were seen and that C is taken as correct"),
    "not_excluded": ("section 5 states that G does not exclude diffuse scatter with τ = 0.05, 0.077 or 0.105, with "
                     "a test that would have found a σ-matched single outlier in at least 80% of cases, both on C "
                     "and on V(τ̂_N); R2-RE-D's gloss 'not distinguished' becomes 'diffuse scatter not excluded by a "
                     "powered shape test', with the reverse check next to it"),
    "none": ("section 5 states that no powered shape test separates the two pictures on these data, quoting the "
             "power, the size and the smallest curve z with power ≥ 0.8 (if any); R2-RE-D's reading and gloss stay"),
}

# keys the power stage must never write (README: no G_obs, no sum of z^2, no z_j of other hosts)
FORBIDDEN_POWER_KEYS = ("G_obs", "j_hat_obs", "sum_z2", "hosts_observed", "p_G", "p_G_fixed", "p_dbl", "p_rev",
                        "reading", "sub_label", "observed")


# settings the full stage must share with the power stage (g_only and g_stage differ between them by design)
STAGE_SETTING_KEYS = ("g_seed_base", "g_host_seed_base", "g_inner_seed", "g_n_sims", "g_n_inner", "g_power_min",
                      "g_z_curve", "g_taus_rep", "g_max_minutes", "g_min_sims", "n5584_host", "threads")
THREAD_ENV = ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS")


def thread_settings():
    """The BLAS / OpenMP thread settings of this process (environment and, when threadpoolctl is available, the
    loaded thread pools): the full stage must run with the power stage's settings (README amendment 2026-11-21)."""
    out = {"env": {k: os.environ.get(k) for k in THREAD_ENV}}
    try:
        import threadpoolctl
        out["threadpools"] = sorted([[str(i.get("internal_api")), int(i.get("num_threads"))]
                                     for i in threadpoolctl.threadpool_info()])
    except ImportError:
        out["threadpools"] = None
    return out


STUDY_DIR = Path(__file__).parent


def formal_g_done(path=None):
    """True once the formal full stage's results/r2_re_g.json is committed in the study folder: status "evaluated"
    or an `observed` record (G on the data computed). Until then only the two standalone stages may run (README
    amendment 2026-11-21, gate 1)."""
    path = STUDY_DIR / "results" / "r2_re_g.json" if path is None else Path(path)
    if not path.exists():
        return False
    rec = json.loads(path.read_text(encoding="utf-8"))
    return rec.get("status") == "evaluated" or "observed" in rec


def formal_outcome(path):
    """True when `path` holds a full-stage outcome (any status, rule (1) included), not a "not run" record."""
    path = Path(path)
    if not path.exists():
        return False
    rec = json.loads(path.read_text(encoding="utf-8"))
    return rec.get("stage") == "full" and "settings" in rec


def study_log_text():
    """The study's log.md (the power line must be present there before the formal full stage)."""
    path = STUDY_DIR / "log.md"
    return path.read_text(encoding="utf-8") if path.exists() else ""


def stage_settings(P):
    """The settings a power record must share with the full stage, as they read back from JSON."""
    return json_like({**{k: P[k] for k in STAGE_SETTING_KEYS if k != "threads"}, "threads": thread_settings()})


def thread_problems(a, b):
    """Thread settings differ: the environment strictly; the thread pools only for an internal_api present in both
    records (which BLAS libraries are loaded can depend on what ran before the snapshot)."""
    a, b = a or {}, b or {}
    out = []
    if a.get("env") != b.get("env"):
        out.append(f"threads env: power stage {a.get('env')!r}, now {b.get('env')!r}")
    pa, pb = {}, {}
    for d, rec in ((pa, a), (pb, b)):
        for api, n in rec.get("threadpools") or []:
            d.setdefault(api, set()).add(int(n))
    for api in sorted(set(pa) & set(pb)):
        if pa[api] != pb[api]:
            out.append(f"threads {api}: power stage {sorted(pa[api])}, now {sorted(pb[api])}")
    return out


def power_record_problems(power_rec, settings):
    """Why a power record cannot be the basis of a full stage (an error, not rule (1)): a stub ("not run" or
    not a power-stage record) or settings that differ from this run's (threads: thread_problems)."""
    if (not isinstance(power_rec, dict) or power_rec.get("stage") != "power" or "settings" not in power_rec
            or str(power_rec.get("status", "")).startswith("not run")):
        st = power_rec.get("status") if isinstance(power_rec, dict) else None
        return [f"the power record is a stub or not a power-stage record (status {st!r})"]
    ps = power_rec["settings"]
    bad = [f"{k}: power stage {ps.get(k)!r}, now {settings.get(k)!r}" for k in STAGE_SETTING_KEYS
           if k != "threads" and ps.get(k) != settings.get(k)]
    return bad + thread_problems(ps.get("threads"), settings.get("threads"))


# ---------------------------------------------------------------- names
def vkey(tau):
    return onehost.vkey(tau)


def zkey(z):
    """Power-curve key: Z250, Z300, ..."""
    return "Z%03d" % int(round(z * 100))


def sim_keys(taus_rep):
    """The eight models with per-simulation files, in the order they run (VHAT first: the runtime guard)."""
    return ["VHAT"] + [vkey(t) for t in taus_rep] + ["C", "OANY", "OANYLO", "OANYVN", "O"]


def set_keys(taus_rep, z_curve):
    """The 13 sets: the eight models and the power curve."""
    return sim_keys(taus_rep) + [zkey(z) for z in z_curve]


def size_keys(taus_rep):
    return ["VHAT"] + [vkey(t) for t in taus_rep]


POWER_KEYS = ["OANY", "OANYVN"]


def fmt_tau(t):
    return f"{t:.4g}"


def model_specs(taus_rep, z_curve, tau_obs, tau_n, z_obs, delta, col):
    """Covariance (tau of the random effect; 0 is C), offset (None, 'any' or a host column) and its size
    (z_alt for the sigma-matched offsets, delta for O)."""
    sp = {"VHAT": {"tau": float(tau_obs), "offset": None, "decisive": True,
                   "description": "V(τ̂_obs): diffuse host scatter at the fitted τ (size at τ̂_obs)"}}
    for t in taus_rep:
        sp[vkey(t)] = {"tau": float(t), "offset": None, "decisive": True,
                       "description": f"V({t:g}): diffuse host scatter (size at τ = {t:g})"}
    sp["C"] = {"tau": 0.0, "offset": None, "decisive": False, "description": "C: no excess scatter (reported)"}
    sp["OANY"] = {"tau": 0.0, "offset": "any", "z_alt": float(z_obs), "decisive": True,
                  "description": "O_any on C: one host drawn uniformly, σ-matched offset z_obs σ_δ,k"}
    sp["OANYLO"] = {"tau": 0.0, "offset": "any", "z_alt": float(z_obs) - 1.0, "decisive": False,
                    "description": "O_any on C with z_obs − 1 (reported)"}
    sp["OANYVN"] = {"tau": float(tau_n), "offset": "any", "z_alt": float(z_obs), "decisive": True,
                    "description": "O_any on V(τ̂_N): one σ-matched offset host plus a small diffuse term"}
    sp["O"] = {"tau": 0.0, "offset": int(col), "delta": float(delta), "decisive": False,
               "description": "O(δ̂): δ̂ on N5584's calibrator rows, on C (reported)"}
    for z in z_curve:
        sp[zkey(z)] = {"tau": 0.0, "offset": "any", "z_alt": float(z), "decisive": False, "curve": True,
                       "description": f"power curve: O_any on C with z_alt = {z:g}"}
    return sp


# ---------------------------------------------------------------- labels and reading (pure)
def p_label(k, n_in):
    """rob.three_way(k, N_in, 'excluded', 'not excluded'): (label, Clopper-Pearson interval of k / N_in)."""
    return rob.three_way(int(k), int(n_in), EXCL, NOT_EXCL)


def p_boot(k, n_in):
    return (1 + int(k)) / (1 + int(n_in))


def rule1_status(reasons):
    """The status of rule (1) from its reasons ('runtime' -> 'not evaluated (runtime)')."""
    if RUNTIME in reasons:
        return NE_RUNTIME
    return "not evaluable (" + "; ".join(reasons) + ")"


def reading(reasons, power, pg_label, power_min=0.8):
    """Rules (1)-(5) in order; returns (reading, sub_label). reasons: rule (1)'s list (empty: rule (1) does
    not apply); power: min(R_OANY, R_OANYVN) (point estimates); pg_label: p_G's three-way label."""
    if reasons:                                                    # (1)
        return rule1_status(reasons), None
    if power < power_min:                                          # (2)
        return READ_UNDERPOWERED, (SUB_LABEL if pg_label == EXCL else None)
    if pg_label == EXCL:                                           # (3)
        return READ_PREFERRED, None
    if pg_label == NOT_EXCL:                                       # (4)
        return READ_NOT_EXCL, None
    return READ_UNDET_MC, None                                     # (5)


def section5_action(read):
    if read == READ_PREFERRED:
        return SECTION5["preferred"]
    if read == READ_NOT_EXCL:
        return SECTION5["not_excluded"]
    return SECTION5["none"]


def anti_conservative(models, taus_rep):
    """Rule (1): the 95% Clopper-Pearson interval of the rejection rate entirely above 0.05 under VHAT or a
    V(tau) of taus_rep; returns the list of those tau (VHAT as its tau)."""
    out = []
    for k in size_keys(taus_rep):
        m = models.get(k, {})
        if m.get("status") == "evaluated" and m["ci95"][0] > 0.05:
            out.append(m["tau"])
    return out


def guard_n(per_sim, n_req, n_sets, max_minutes, min_sims):
    """Runtime guard: (n, projected minutes, reduced). n None: even min_sims does not fit."""
    proj = per_sim * n_req * n_sets / 60.0
    if proj <= max_minutes:
        return int(n_req), proj, False
    new = int(max_minutes * 60.0 / (per_sim * n_sets)) // 1000 * 1000
    new = min(new, int(n_req))
    if new < min_sims:
        return None, proj, True
    return new, proj, True


def smallest_z(curve, power_min):
    ok = [c["z_alt"] for c in curve if c.get("rate") is not None and c["rate"] >= power_min]
    return min(ok) if ok else None


# ---------------------------------------------------------------- the algebra
def g_stat(z):
    """G = max z^2 / sum z^2 and its argmax (ties to the lowest column); z (..., n_hosts)."""
    z2 = np.square(z)
    j = np.argmax(z2, axis=-1)
    return np.take_along_axis(z2, np.expand_dims(j, -1), -1)[..., 0] / z2.sum(axis=-1), j


def reml_f(tau, v, lam):
    """f(tau; u) = sum_i [log(1 + tau^2 lam_i) - tau^2 v_i^2 / (1 + tau^2 lam_i)] (clipped lam)."""
    t2 = float(tau) * float(tau)
    d = 1.0 + t2 * lam
    return float(np.sum(np.log(d) - t2 * v * v / d))


def tau_refit(v, lam, reml_tau):
    """R2-RE's estimator applied to the reduced form."""
    return reml_tau(lambda t: reml_f(t, v, lam), TAU_MAX, TAU_STEP, interval=False)


def inner_matrix(tau, des):
    """A with z_i = A e_i ~ N(0, D (M + tau^2 M^2) D), D = diag(M_jj^-1/2)."""
    lam = des["lam"]
    s = np.sqrt(lam * (1.0 + tau * tau * lam))
    return des["DQ"] * s[None, :]


def inner_k(G, tau, des, E_in):
    """k = #{i: G_i^in(tau) >= G} over the fixed inner matrix E_in (N_in x n_hosts)."""
    Zi = E_in @ inner_matrix(tau, des).T
    np.square(Zi, out=Zi)
    Gi = Zi.max(axis=1) / Zi.sum(axis=1)
    return int(np.count_nonzero(Gi >= G))


def inner_draws(seed, n_in, n_hosts):
    return np.random.default_rng(seed).standard_normal((int(n_in), int(n_hosts)))


def group_positions(rows_a, groups):
    rows_a = np.asarray(rows_a)
    n_a = len(rows_a)
    gpos = []
    for g in groups:
        g = np.asarray(g)
        pg = np.searchsorted(rows_a, g)
        if np.any(pg >= n_a) or not np.array_equal(rows_a[np.minimum(pg, n_a - 1)], g):
            raise RuntimeError("a calibrator group has rows outside rows_a")
        gpos.append(pg)
    return gpos


def design(L, y, C, rows_a, groups, fns):
    """Everything that depends on the design only (plus y_hat for the pointwise checks): the fit under C on
    rows_a (kept columns, y_hat), C_a's lower Cholesky factor, P Z, M, W, the clipped eigen-decomposition of
    M. Returns (des, problem): problem is a rule-(1) reason or None. Fit failures raise (the caller decides)."""
    rows_a = np.asarray(rows_a)
    res = fns["fit"](L, y, C, rows_a)
    kept = res["kept"]
    X = L[np.ix_(rows_a, kept)]
    yhat = X @ res["q"][kept]
    gpos = group_positions(rows_a, groups)
    n_a, nh = len(rows_a), len(groups)
    try:
        Kc = linalg.cholesky(C[np.ix_(rows_a, rows_a)], lower=True)
    except np.linalg.LinAlgError as e:
        return None, f"the Cholesky factor of C failed: {e}"
    Zm = np.zeros((n_a, nh))
    for j, p in enumerate(gpos):
        Zm[p, j] = 1.0
    cf = (Kc, True)
    CiX = linalg.cho_solve(cf, X)
    CiZ = linalg.cho_solve(cf, Zm)
    F = X.T @ CiX
    F = 0.5 * (F + F.T)
    cfF = linalg.cho_factor(F, lower=True)
    PZ = CiZ - CiX @ linalg.cho_solve(cfF, X.T @ CiZ)
    M = Zm.T @ PZ
    M = 0.5 * (M + M.T)
    mjj = np.diag(M).copy()
    if not np.all(mjj > 0):
        return None, "some M_jj ≤ 0 (hosts " + ", ".join(str(j) for j in np.flatnonzero(~(mjj > 0))) + ")"
    dinv = 1.0 / np.sqrt(mjj)
    W = PZ.T * dinv[:, None]
    lam, Q = np.linalg.eigh(M)
    thr = EIG_RTOL * float(lam.max())
    if np.any(lam < -thr):
        raise RuntimeError(f"M has a negative eigenvalue {lam.min()!r} beyond the clipping threshold: a bug")
    clipped = np.abs(lam) < thr
    lam = np.where(clipped, 0.0, lam)
    des = {"kept": kept, "X": X, "yhat": yhat, "gpos": gpos, "Kc": Kc, "W": W, "PZt": PZ.T.copy(), "M": M,
           "mjj": mjj, "dinv": dinv, "sqrt_m": np.sqrt(mjj), "lam": lam, "Q": Q, "DQ": dinv[:, None] * Q,
           "WH": W @ Zm, "n_clipped": int(clipped.sum()), "rank_M": int((~clipped).sum()),
           "lam_max": float(lam.max()), "lam_min_raw": float(np.linalg.eigvalsh(M)[0]),
           "n_a": n_a, "n_hosts": nh, "p": int(len(kept))}
    return des, None


def v_of_z(z, des):
    """v = Q^T u with u = diag(sqrt(M_jj)) z."""
    return des["Q"].T @ (z * des["sqrt_m"])


def offset_z(spec, k_host, des):
    """W (delta h_k): the offset's term in z (sigma-matched: delta = z_alt M_kk^-1/2)."""
    if spec["offset"] is None:
        return 0.0
    if spec["offset"] == "any":
        return spec["z_alt"] * des["dinv"][k_host] * des["WH"][:, k_host]
    return spec["delta"] * des["WH"][:, spec["offset"]]


def offset_y(spec, k_host, des):
    """The offset on rows_a (for the pointwise checks): delta on host k's calibrator rows."""
    off = np.zeros(des["n_a"])
    if spec["offset"] is None:
        return off
    if spec["offset"] == "any":
        off[des["gpos"][k_host]] = spec["z_alt"] * des["dinv"][k_host]
    else:
        off[des["gpos"][spec["offset"]]] = spec["delta"]
    return off


def one_column_z(L, y_full, C, rows_a, groups, fns):
    """The 37 one-column GLS fits: delta_j, sigma_j (onehost.fit_delta)."""
    out = [onehost.fit_delta(L, y_full, C, rows_a, g, fns) for g in groups]
    d = np.array([a for a, _ in out])
    s = np.array([b for _, b in out])
    return d, s


# ---------------------------------------------------------------- simulations
def simulate(spec, B, des, E_in, seed_base, s_lo, s_hi, any_hosts, reml_tau, n_in):
    """Outer simulations s_lo..s_hi-1 of one model: z_s = B eps_s (+ offset), G_s, j_s, tau_s (refitted),
    k_s (inner draws at tau_s; tau_s < 1e-3 counts as zero)."""
    n = s_hi - s_lo
    G = np.empty(n)
    J = np.empty(n, dtype=np.int64)
    T = np.empty(n)
    K = np.empty(n, dtype=np.int64)
    Z0 = np.empty(n, dtype=bool)
    UB = np.empty(n, dtype=bool)
    for c0 in range(s_lo, s_hi, CHUNK):
        s_list = np.arange(c0, min(c0 + CHUNK, s_hi))
        E = onehost.eps_block(seed_base, s_list, des["n_a"])
        Zc = (B @ E).T
        for i, s in enumerate(s_list):
            z = Zc[i]
            if spec["offset"] is not None:
                z = z + offset_z(spec, int(any_hosts[s]) if spec["offset"] == "any" else None, des)
            g, j = g_stat(z)
            est = tau_refit(v_of_z(z, des), des["lam"], reml_tau)
            t_in = 0.0 if est["at_zero"] else est["tau_hat"]
            r = s - s_lo
            G[r], J[r], T[r], Z0[r], UB[r] = float(g), int(j), est["tau_hat"], est["at_zero"], est["at_upper_bound"]
            K[r] = inner_k(float(g), t_in, des, E_in)
    return {"G": G, "j": J, "tau": T, "k": K, "at_zero": Z0, "at_bound": UB}


def _cat(parts):
    return {k: np.concatenate([p[k] for p in parts]) for k in parts[0]}


def k_digest(k):
    return hashlib.sha256(np.asarray(k, dtype="<i8").tobytes()).hexdigest()


def model_record(key, spec, arr, n_in, any_hosts, labels_cache):
    n = len(arr["k"])
    labs = []
    for k in arr["k"]:
        k = int(k)
        if k not in labels_cache:
            labels_cache[k] = p_label(k, n_in)[0]
        labs.append(labels_cache[k])
    n_ex = sum(1 for x in labs if x == EXCL)
    n_ne = sum(1 for x in labs if x == NOT_EXCL)
    lo, hi = rob._cp(n_ex, n)
    rec = {"description": spec["description"], "decisive": spec["decisive"], "status": "evaluated",
           "tau": spec["tau"], "offset": spec["offset"], "n": int(n), "n_excluded": int(n_ex),
           "n_not_excluded": int(n_ne), "n_undetermined": int(n - n_ex - n_ne), "rate": n_ex / n,
           "ci95": [lo, hi],
           "quantiles_5_50_95": {"G": [float(q) for q in np.percentile(arr["G"], [5, 50, 95])],
                                 "tau_hat": [float(q) for q in np.percentile(arr["tau"], [5, 50, 95])]},
           "n_tau_zero": int(arr["at_zero"].sum()), "n_tau_bound": int(arr["at_bound"].sum()),
           "k_sha256": k_digest(arr["k"])}
    if "z_alt" in spec:
        rec["z_alt"] = spec["z_alt"]
    if "delta" in spec:
        rec["delta"] = spec["delta"]
    if spec["offset"] == "any":
        rec["n_jhat_is_offset_host"] = int(np.sum(arr["j"] == any_hosts[:n]))
    elif spec["offset"] is not None:
        rec["n_jhat_is_offset_host"] = int(np.sum(arr["j"] == spec["offset"]))
    return rec


def sims_file(key, spec, arr, P, any_hosts):
    n = len(arr["k"])
    out = {"model": key, "status": "evaluated", "n": int(n), "seed_base": int(P["g_seed_base"]),
           "n_inner": int(P["g_n_inner"]), "inner_seed": int(P["g_inner_seed"]),
           "G": [round(float(g), G_DECIMALS) for g in arr["G"]],
           "tau_hat": [round(float(t), TAU_DECIMALS) for t in arr["tau"]],
           "k": [int(k) for k in arr["k"]], "j_hat": [int(j) for j in arr["j"]]}
    if spec["offset"] == "any":
        out["host_seed_base"] = int(P["g_host_seed_base"])
        out["offset_host"] = [int(h) for h in any_hosts[:n]]
    return out


# ---------------------------------------------------------------- the block
def run_stage(stage, L, y, C, rows_a, groups, labels, P, fns, log, grid_m2l, power_rec=None,
              grid_source=REML_GRID_SOURCE, expected_col=None, recorded=None):
    """One stage of R2-RE-G. stage "power": returns (power_record, None). stage "full": needs power_rec (the
    power stage's record) and returns (out, sims), sims mapping the eight model keys to their per-simulation
    records. `recorded` overrides the recorded values (tests only)."""
    if stage not in ("power", "full"):
        raise ValueError(f"g_stage must be 'power' or 'full', not {stage!r}")
    if stage == "full" and power_rec is None:
        raise ValueError("the full stage needs the power stage's record")
    t_block = CLOCK()
    rows_a = np.asarray(rows_a)
    nh = len(groups)
    taus_rep = [float(t) for t in P["g_taus_rep"]]
    z_curve = [float(z) for z in P["g_z_curve"]]
    skeys, keys = sim_keys(taus_rep), set_keys(taus_rep, z_curve)
    n_in = int(P["g_n_inner"])
    cols = [j for j, h in enumerate(labels) if h == P["n5584_host"]]
    if len(cols) != 1:
        raise RuntimeError(f"host {P['n5584_host']} labels {len(cols)} columns, expected 1")
    col = cols[0]
    if expected_col is not None and col != expected_col:
        raise RuntimeError(f"{P['n5584_host']} is column {col}, documented as column {expected_col}")
    rec = {"tau_obs": RECORDED_TAU_OBS, "delta_hat": RECORDED_DELTA, "sigma_delta": RECORDED_SIGMA_DELTA,
           "z_obs": RECORDED_Z_OBS, "tau_n": RECORDED_TAU_N}
    rec.update(recorded or {})
    out = {"stage": stage, "host": labels[col], "column": int(col),
           "headline": "R2-RE's row stays the headline; this block attaches a label to R2-RE-D's reading",
           "settings": {"eps": "numpy.random.default_rng(g_seed_base + s).standard_normal(len(rows_a)), the same "
                               "eps_s for every model",
                        "offset_host_any": "numpy.random.default_rng(g_host_seed_base + s).integers(0, 37), shared "
                                           "by every O_any variant",
                        "inner": "numpy.random.default_rng(g_inner_seed).standard_normal((g_n_inner, 37)), one "
                                 "fixed matrix for every evaluation",
                        **{k: P[k] for k in ("g_seed_base", "g_host_seed_base", "g_inner_seed", "g_n_sims",
                                             "g_n_inner", "g_power_min", "g_z_curve", "g_taus_rep",
                                             "g_max_minutes", "g_min_sims", "g_only", "g_stage", "n5584_host")},
                        "threads": thread_settings(),
                        "reml": f"reml_tau(f, {TAU_MAX}, {TAU_STEP}, interval=False); τ̂ < 1e-3 counts as zero",
                        "eig_rtol": EIG_RTOL, "reml_grid_source": grid_source},
           "recorded": rec, "set_keys": keys, "sim_keys": skeys, "decisive": [k for k in keys if k in
                                                                               size_keys(taus_rep) + POWER_KEYS]}
    seconds, checks, reasons = {}, {}, []

    def finish(models=None):
        out["checks"] = checks
        out["rule1"] = list(reasons)
        out["status"] = rule1_status(reasons) if reasons else "evaluated"
        if models is not None:
            out["models"] = models
        seconds["block"] = CLOCK() - t_block
        out["seconds"] = seconds
        return out

    def stop():
        finish()
        log("R2-RE-G (" + stage + "): " + out["status"])
        if stage == "power":
            return out, None
        out.update(reading=out["status"], sub_label=None, section5=SECTION5["none"])
        return out, {k: {"model": k, "status": out["status"]} for k in skeys}

    if stage == "full":
        bad_rec = power_record_problems(power_rec, json_like(out["settings"]))
        if bad_rec:
            raise RuntimeError("R2-RE-G full stage refused: " + "; ".join(bad_rec))
        # the gate holds for any caller (also an explore/ script): G on the data only after the formal full stage,
        # or for the formal full stage itself, whose power line must be present in log.md
        if not (formal_g_done() or power_log_line(power_rec) in study_log_text()):
            raise RuntimeError("R2-RE-G full stage refused: the power record's line (shape.power_log_line) is not "
                               "present in log.md and the formal results/r2_re_g.json does not exist yet")
    if stage == "full" and power_rec.get("status") == NE_RUNTIME:
        reasons.append(RUNTIME)
        checks["power_record_status"] = power_rec.get("status")
        return stop()
    if stage == "full" and not power_rec.get("n_sims"):
        # the power stage stopped before its simulations (rule (1)): nothing to reproduce, the same rule applies
        reasons.extend(power_rec.get("rule1") or [f"the power stage was not evaluated ({power_rec.get('status')})"])
        checks["power_record_status"] = power_rec.get("status")
        return stop()

    # ---- design
    t0 = CLOCK()
    try:
        des, problem = design(L, y, C, rows_a, groups, fns)
    except (np.linalg.LinAlgError, ValueError) as e:
        if not fns["is_fit_failure"](e):
            raise
        reasons.append(f"fit: the design under C on rows_a: {e}")
        return stop()
    if problem:
        reasons.append(problem)
        return stop()
    out["design"] = {"n_rows": des["n_a"], "n_hosts": nh, "n_columns_X": des["p"], "rank_M": des["rank_M"],
                     "n_eigenvalues_clipped": des["n_clipped"], "lambda_max": des["lam_max"],
                     "lambda_min_unclipped": des["lam_min_raw"], "M_jj_min": float(des["mjj"].min()),
                     "joint_rank": des["p"] + des["rank_M"], "joint_columns": des["p"] + nh,
                     "sigma_delta_j": [float(s) for s in des["dinv"]],
                     "W_X_max_abs": float(np.max(np.abs(des["W"] @ des["X"])))}
    seconds["design"] = CLOCK() - t0

    # ---- reproduction checks that use only recorded data values (both stages)
    t0 = CLOCK()
    ya = y[rows_a]
    try:
        delta, sigma_delta = onehost.fit_delta(L, y, C, rows_a, groups[col], fns)
    except (np.linalg.LinAlgError, ValueError) as e:
        if not fns["is_fit_failure"](e):
            raise
        reasons.append(f"fit: δ̂: {e}")
        return stop()
    z_obs = delta / sigma_delta
    v_obs = des["Q"].T @ (des["PZt"] @ ya)        # u_obs = Z^T P y, used only through v: no z_j formed, nothing stored
    grid = np.round(np.arange(0.0, TAU_MAX + TAU_STEP / 2, TAU_STEP), 10)
    f_grid = np.array([reml_f(t, v_obs, des["lam"]) for t in grid])
    est_obs = tau_refit(v_obs, des["lam"], fns["reml_tau"])
    v_obs = None
    tau_obs = est_obs["tau_hat"]
    gm = np.asarray(grid_m2l, dtype=float)
    repro = {"reml_grid_n": int(len(gm)), "tau_hat_obs": tau_obs, "tau_hat_obs_refined": est_obs["refined"],
             "tau_hat_obs_at_zero": est_obs["at_zero"], "tau_hat_obs_at_upper_bound": est_obs["at_upper_bound"],
             "delta_hat": delta, "sigma_delta": sigma_delta, "z_obs": z_obs,
             "sigma_delta_from_M_rel_diff": abs(des["dinv"][col] - sigma_delta) / sigma_delta}
    bad = []
    if len(gm) != len(grid):
        bad.append(f"REML grid has {len(gm)} values, expected {len(grid)}")
    else:
        dg = np.abs((f_grid - f_grid[0]) - (gm - gm[0]))
        repro["reml_grid_max_abs_diff"] = float(dg.max())
        if not dg.max() <= GRID_ATOL:
            bad.append(f"REML grid differences off by up to {dg.max():.3g} (tolerance {GRID_ATOL:g})")
    if not abs(tau_obs - rec["tau_obs"]) <= TAU_OBS_ATOL:
        bad.append(f"τ̂_obs {tau_obs!r} vs recorded {rec['tau_obs']!r} (absolute {TAU_OBS_ATOL:g})")
    if not abs(delta - rec["delta_hat"]) <= DELTA_ATOL:
        bad.append(f"δ̂ {delta!r} vs recorded {rec['delta_hat']!r} (absolute {DELTA_ATOL:g})")
    if not abs(sigma_delta - rec["sigma_delta"]) <= REL_TOL * abs(rec["sigma_delta"]):
        bad.append(f"σ_δ {sigma_delta!r} vs recorded {rec['sigma_delta']!r} (relative {REL_TOL:g})")
    if not abs(z_obs - rec["z_obs"]) <= REL_TOL * abs(rec["z_obs"]):
        bad.append(f"z_obs {z_obs!r} vs recorded {rec['z_obs']!r} (relative {REL_TOL:g})")
    repro["mismatches"] = bad
    checks["reproduction"] = repro
    seconds["reproduction"] = CLOCK() - t0
    if bad:
        reasons.append("reproduction check failed: " + "; ".join(bad))
        return stop()
    if est_obs["at_upper_bound"]:
        reasons.append("τ̂_obs at the upper bound")
        return stop()
    log(f"R2-RE-G ({stage}): reproduced τ̂_obs {tau_obs:.6f}, δ̂ {delta:.6f}, σ_δ {sigma_delta:.6f}, "
        f"z_obs {z_obs:.6f}; rank M {des['rank_M']} of {nh}")

    # ---- models, Cholesky factors and B = W K (one factor at a time)
    t0 = CLOCK()
    specs = model_specs(taus_rep, z_curve, tau_obs, rec["tau_n"], z_obs, delta, col)
    n_req = int(P["g_n_sims"]) if stage == "power" else int(power_rec["n_sims"])
    n_pw = min(N_POINTWISE, n_req)
    point_taus = {specs["VHAT"]["tau"], specs["OANY"]["tau"]}
    eps_pw = onehost.eps_block(P["g_seed_base"], np.arange(n_pw), des["n_a"])
    Bs, KE, fail = {}, {}, {}
    for tau in dict.fromkeys(specs[k]["tau"] for k in keys):
        try:
            if tau == 0.0:
                K = des["Kc"]
            else:
                V = fns["with_re"](C, groups, tau)
                K = linalg.cholesky(V[np.ix_(rows_a, rows_a)], lower=True)
                V = None
        except np.linalg.LinAlgError as e:
            fail[tau] = str(e)
            continue
        Bs[tau] = des["W"] @ K
        if tau in point_taus:
            KE[tau] = K @ eps_pw
        K = None
    status = {k: "evaluated" if specs[k]["tau"] not in fail else
              f"not evaluable (Cholesky factor failed: {fail[specs[k]['tau']]})" for k in keys}
    checks["cholesky_failed"] = {fmt_tau(t): e for t, e in fail.items()}
    if fail:
        reasons.append("the Cholesky factor of " + ", ".join("C" if t == 0.0 else f"V({fmt_tau(t)})" for t in fail)
                       + " failed")
    seconds["factors"] = CLOCK() - t0
    if fail:
        return stop()

    E_in = inner_draws(P["g_inner_seed"], n_in, nh)
    any_hosts = onehost.offset_hosts(P["g_host_seed_base"], n_req, nh)

    # ---- pointwise checks: the first simulations of VHAT and OANY built in full
    t0 = CLOCK()
    pw = []
    for key in ("VHAT", "OANY"):
        sp = specs[key]
        for s in range(n_pw):
            kh = int(any_hosts[s]) if sp["offset"] == "any" else None
            z_red = Bs[sp["tau"]] @ eps_pw[:, s] + offset_z(sp, kh, des)
            y_full = np.array(y, dtype=float)
            y_full[rows_a] = des["yhat"] + KE[sp["tau"]][:, s] + offset_y(sp, kh, des)
            d, sd = one_column_z(L, y_full, C, rows_a, groups, fns)
            dz = float(np.max(np.abs(d / sd - z_red)))
            t_red = tau_refit(v_of_z(z_red, des), des["lam"], fns["reml_tau"])["tau_hat"]
            t_full = fns["reml_tau"](lambda t: fns["reml_m2l"](L, y_full, C, rows_a, groups, t), TAU_MAX, TAU_STEP,
                                     interval=False)["tau_hat"]
            pw.append({"model": key, "s": s, "offset_host": kh, "max_abs_dz": dz, "tau_reduced": t_red,
                       "tau_reml_m2l": t_full, "ok": bool(dz <= Z_ATOL and abs(t_red - t_full) <= POINT_TAU_ATOL)})
    checks["pointwise"] = pw
    seconds["pointwise"] = CLOCK() - t0
    if not all(p["ok"] for p in pw):
        reasons.append("pointwise check failed (" + ", ".join(f"{p['model']} s={p['s']}" for p in pw if not p["ok"])
                       + ")")
        return stop()

    # ---- outer simulations, VHAT first (runtime guard in the power stage)
    run_keys = [k for k in keys if status[k] == "evaluated"]
    arrs, seconds_m = {}, {}
    t0 = CLOCK()
    n_time = min(TIME_SIMS, n_req)
    first = simulate(specs["VHAT"], Bs[specs["VHAT"]["tau"]], des, E_in, P["g_seed_base"], 0, n_time, any_hosts,
                     fns["reml_tau"], n_in)
    per = (CLOCK() - t0) / max(n_time, 1)
    if stage == "power":
        n, proj, reduced = guard_n(per, n_req, len(run_keys), float(P["g_max_minutes"]), int(P["g_min_sims"]))
        out["runtime_guard"] = {"timed_sims": n_time, "seconds_per_sim": per, "n_sets": len(run_keys),
                                "n_requested": n_req, "projected_minutes": proj, "max_minutes": P["g_max_minutes"],
                                "min_sims": P["g_min_sims"], "reduced": reduced, "n": n}
        if n is None:
            reasons.append(RUNTIME)
            out["n_sims"] = None
            return stop()
        if reduced:
            log(f"R2-RE-G (power): projected {proj:.0f} min; n reduced from {n_req} to {n}")
    else:
        n = n_req
        out["runtime_guard"] = {"from_power_stage": power_rec.get("runtime_guard"), "seconds_per_sim": per}
    out["n_sims"] = int(n)
    parts = [first] if n >= n_time else [{k: v[:n] for k, v in first.items()}]
    if n > n_time:
        parts.append(simulate(specs["VHAT"], Bs[specs["VHAT"]["tau"]], des, E_in, P["g_seed_base"], n_time, n,
                              any_hosts, fns["reml_tau"], n_in))
    arrs["VHAT"] = _cat(parts)
    seconds_m["VHAT"] = CLOCK() - t0
    log(f"  R2-RE-G ({stage}): VHAT {n} simulations, {seconds_m['VHAT']:.0f} s")
    for key in run_keys:
        if key == "VHAT":
            continue
        t1 = CLOCK()
        sp = specs[key]
        arrs[key] = simulate(sp, Bs[sp["tau"]], des, E_in, P["g_seed_base"], 0, n, any_hosts, fns["reml_tau"], n_in)
        seconds_m[key] = CLOCK() - t1
        log(f"  R2-RE-G ({stage}): {key} {n} simulations, {seconds_m[key]:.0f} s")
    seconds["simulations"] = seconds_m
    Bs.clear()

    # ---- per-model records, power, size, curve
    cache = {}
    models = {}
    for k in keys:
        if status[k] != "evaluated":
            models[k] = {"description": specs[k]["description"], "decisive": specs[k]["decisive"],
                         "status": status[k], "tau": specs[k]["tau"]}
            continue
        models[k] = model_record(k, specs[k], arrs[k], n_in, any_hosts, cache)
    r_any, r_vn = models["OANY"]["rate"], models["OANYVN"]["rate"]
    power = min(r_any, r_vn)
    sz = {k: models[k]["rate"] for k in size_keys(taus_rep)}
    out["power"] = {"R_OANY": r_any, "R_OANYVN": r_vn, "power": power, "power_min": float(P["g_power_min"]),
                    "powered": bool(power >= float(P["g_power_min"]))}
    out["size"] = {**{f"R_{k}": v for k, v in sz.items()}, "size": max(sz.values()),
                   "taus": {k: models[k]["tau"] for k in size_keys(taus_rep)},
                   "note": "checked at τ = 0.05, τ̂_obs and 0.105 only; no monotonicity in τ is assumed"}
    curve = [{"key": zkey(z), "z_alt": z, "n_excluded": models[zkey(z)].get("n_excluded"),
              "rate": models[zkey(z)].get("rate"), "ci95": models[zkey(z)].get("ci95")} for z in z_curve]
    out["curve"] = curve
    out["curve_with_oany"] = sorted(curve + [{"key": k, "z_alt": models[k]["z_alt"], "n_excluded":
                                              models[k]["n_excluded"], "rate": models[k]["rate"],
                                              "ci95": models[k]["ci95"]} for k in ("OANYLO", "OANY")],
                                    key=lambda c: c["z_alt"])
    out["smallest_z_alt_power_08"] = smallest_z(curve, float(P["g_power_min"]))
    ac = anti_conservative(models, taus_rep)
    if ac:
        reasons.append("anti-conservative at τ = " + ", ".join(fmt_tau(t) for t in ac))
    if stage == "full":
        mism = []
        pm = power_rec.get("models", {})
        if int(power_rec.get("n_sims") or -1) != n:
            mism.append(f"n {n} vs power stage {power_rec.get('n_sims')}")
        for k in keys:
            a, b = models[k].get("n_excluded"), pm.get(k, {}).get("n_excluded")
            if a != b:
                mism.append(f"{k}: {a} vs power stage {b}")
        checks["power_stage_counts_reproduced"] = not mism
        checks["power_stage_count_mismatches"] = mism
        checks["power_stage_k_sha256_equal"] = {k: models[k].get("k_sha256") == pm.get(k, {}).get("k_sha256")
                                                for k in keys}
        if mism:
            reasons.insert(0, "the full stage does not reproduce the power stage's counts")
    seconds["records"] = CLOCK() - t0
    log(f"R2-RE-G ({stage}): power min(R_OANY {r_any:.4f}, R_OANYVN {r_vn:.4f}) = {power:.4f}; size max "
        + ", ".join(f"R_{k} {v:.4f}" for k, v in sz.items()) + "; curve "
        + ", ".join(f"z {c['z_alt']:g}: {c['rate']:.4f}" for c in curve if c["rate"] is not None))

    if stage == "power":
        finish(models)
        return out, None

    # ---- full stage: G_obs and the reading (only after the power stage's counts are reproduced)
    out["models"] = models
    sims = {k: sims_file(k, specs[k], arrs[k], P, any_hosts) for k in skeys}
    if any(r != RUNTIME and not r.startswith("anti-conservative") for r in reasons):
        finish(models)
        out.update(reading=out["status"], sub_label=None, section5=SECTION5["none"])
        log("R2-RE-G (full): " + out["status"])
        return out, sims
    t0 = CLOCK()
    try:
        d_j, s_j = one_column_z(L, y, C, rows_a, groups, fns)
    except (np.linalg.LinAlgError, ValueError) as e:
        if not fns["is_fit_failure"](e):
            raise
        reasons.insert(0, f"fit: the one-column fits on the real data: {e}")
        finish(models)
        out.update(reading=out["status"], sub_label=None, section5=SECTION5["none"])
        return out, sims
    z_w = des["W"] @ ya
    z_fit = d_j / s_j
    dz = float(np.max(np.abs(z_w - z_fit)))
    checks["real_W_y_vs_one_column_fits"] = {"max_abs_dz": dz, "ok": bool(dz <= Z_ATOL)}
    seconds["one_column_fits"] = CLOCK() - t0
    if not dz <= Z_ATOL:
        reasons.insert(0, f"reproduction check failed: W y against the one-column GLS fits (max |Δz| {dz:.3g})")
        finish(models)
        out.update(reading=out["status"], sub_label=None, section5=SECTION5["none"])
        return out, sims
    t0 = CLOCK()
    g_obs, j_obs = g_stat(z_w)
    g_obs, j_obs = float(g_obs), int(j_obs)
    t_in = 0.0 if est_obs["at_zero"] else tau_obs
    k_obs = inner_k(g_obs, t_in, des, E_in)
    lab, ci = p_label(k_obs, n_in)
    p_g = {"k": k_obs, "n_inner": n_in, "p": p_boot(k_obs, n_in), "ci95": list(ci), "label": lab, "tau": tau_obs}
    fixed = {}
    for key, t in [(vkey(t), t) for t in taus_rep] + [("C", 0.0)]:
        kf = inner_k(g_obs, t, des, E_in)
        lf, cf_ = p_label(kf, n_in)
        fixed[key] = {"tau": t, "k": kf, "p": p_boot(kf, n_in), "ci95": list(cf_), "label": lf}
    kv = arrs["VHAT"]["k"]
    n_dbl = int(np.sum(kv <= k_obs))
    p_dbl = {"count": n_dbl, "n": int(n), "p": (1 + n_dbl) / (1 + n), "ci95": list(rob._cp(n_dbl, n)),
             "note": "#{s in VHAT: p_boot,s <= p_G}, i.e. k_s <= k_obs"}
    p_rev = {}
    for key in ("OANY", "O"):
        c = int(np.sum(arrs[key]["G"] <= g_obs))
        p_rev[key] = {"count": c, "n": int(n), "p": (1 + c) / (1 + n), "ci95": list(rob._cp(c, n))}
    ss = float(np.sum(z_w * z_w))
    out["observed"] = {"G_obs": g_obs, "j_hat_obs": j_obs, "host_j_hat": labels[j_obs], "z_j_hat": float(z_w[j_obs]),
                       "sum_z2": ss, "tau_hat_obs": tau_obs,
                       "hosts_observed": [{"column": j, "host": labels[j], "z": float(z_w[j]), "z_fit": float(z_fit[j]),
                                           "delta_hat": float(d_j[j]), "sigma_delta": float(s_j[j])}
                                          for j in range(nh)]}
    out["p_G"] = p_g
    out["p_G_fixed"] = fixed
    out["p_dbl"] = p_dbl
    out["p_rev"] = p_rev
    try:
        fns["fit"](np.hstack([L, np.column_stack([np.isin(np.arange(L.shape[0]), g) for g in groups]).astype(float)]),
                   y, C, rows_a)
        jf = "fitted (full column rank)"
    except (np.linalg.LinAlgError, ValueError) as e:
        if not fns["is_fit_failure"](e):
            raise
        jf = f"not fitted: {e}"
    out["joint_fit"] = {"attempt": jf, "rank": des["p"] + des["rank_M"], "n_columns": des["p"] + nh,
                        "note": "the joint fit with all 37 offsets is attempted once and reported; not used"}
    seconds["observed"] = CLOCK() - t0
    read, sub = reading(reasons, power, lab, float(P["g_power_min"]))
    finish(models)
    out.update(reading=read, sub_label=sub, section5=section5_action(read))
    log(f"R2-RE-G (full): G_obs {g_obs:.5f} (ĵ {labels[j_obs]}), p_G {p_g['p']:.4f} ({lab}); reading: {read}"
        + (f" [{sub}]" if sub else ""))
    return out, sims


def json_like(o):
    """o as it reads back from JSON (tuples become lists), for comparing settings with a saved record."""
    import json
    from astrolab.results import to_jsonable
    return json.loads(json.dumps(to_jsonable(o)))


def summary(g_out):
    """Short summary for summary.json (R2_RE_G)."""
    out = {"status": g_out.get("status"), "reading": g_out.get("reading")}
    if g_out.get("sub_label"):
        out["sub_label"] = g_out["sub_label"]
    if "power" in g_out:
        out.update(power=g_out["power"]["power"], size=g_out["size"]["size"], n_sims=g_out.get("n_sims"),
                   smallest_z_alt_power_08=g_out.get("smallest_z_alt_power_08"))
    if "p_G" in g_out:
        out.update(G_obs=g_out["observed"]["G_obs"], host_j_hat=g_out["observed"]["host_j_hat"],
                   p_G=g_out["p_G"]["p"], p_G_label=g_out["p_G"]["label"])
    return out


def power_log_line(p_out):
    """One line for log.md after the power stage (power, size, curve; nothing that uses G_obs)."""
    if "power" not in p_out:
        return f"R2-RE-G power stage: {p_out.get('status')}"
    pw, sz = p_out["power"], p_out["size"]
    return (f"R2-RE-G power stage (n = {p_out['n_sims']}): power = min(R_OANY {pw['R_OANY']:.4f}, R_OANYVN "
            f"{pw['R_OANYVN']:.4f}) = {pw['power']:.4f} ({'powered' if pw['powered'] else 'underpowered'}); size = "
            + ", ".join(f"{k} {v:.4f}" for k, v in sz.items() if k.startswith("R_")) + f" (max {sz['size']:.4f}); "
            + "curve " + ", ".join(f"z {c['z_alt']:g}: {c['rate']:.4f}" for c in p_out["curve"]
                                   if c["rate"] is not None)
            + f"; smallest z with power ≥ 0.8: {p_out['smallest_z_alt_power_08']}; status {p_out['status']}")
