"""R2-RE-D (README section 2, addendum 2026-11-21, T-048): one outlying host or diffuse host scatter.

Three data models for the excess calibrator scatter of the 37-host NGC 4258-only system are compared by
how often each produces data as "one-outlier-like" as observed:
- C: y_s = y_hat + K_C eps_s (no excess);
- V(tau), tau = 0.05, 0.077, 0.105 mag: K from with_re(C, calib_groups, tau) (diffuse host scatter);
- O(delta_hat): y_C,s + delta_hat h, h the indicator of N5584's calibrator rows (one offset host);
  reported variants O(delta_hat - sigma_delta), O(delta_hat) + V(tau_hat_N), O_any(delta_hat).
eps_s = default_rng(d_seed_base + s).standard_normal(len(rows_a)), the same for every model.

Statistics (identical on data and simulations; the shift rows and sigma_k always come from fits under C):
- spread_37: numpy.std of Delta_k / sigma_k over the first n_subsets R4 subsets (R2-RE-ROB part B);
- d': criterion S of R2-RE-SEL (argmin_j spread_excl_j, ties to the lowest column);
- spread_36: the R2-RE-SEL spread for dropped host d' (36-host reference refit, R4-N's index stream);
- D = spread_37 - spread_36 (exact); D_proxy = spread_37 - min_j spread_excl_j (reported);
- J: the quadrant count {spread_37 >= x, spread_36 <= x} estimated on half A (s even), calibrated on half
  B (s odd): p_J = (1 + #{i in B: count_i <= count_obs}) / (1 + n_B).

run.py passes its own functions in (`fns`); this module does not import run (AGENTS.md section 2).
"""
import json
import time
from collections import Counter

import numpy as np
from scipy import linalg, stats

import rob
import sel

# Values recorded before the addendum (README section 2, R2-RE-D "Seen before" and rule (1)).
RECORDED_SPREAD_37 = 1.3070929081086322       # R2-RE-ROB part B spread_obs
RECORDED_SPREAD_36 = sel.RECORDED_SPREAD_OBS   # 1.0325254787240916, B-N spread_obs
SPREAD_RTOL = 1e-9
CRIT_S_EXPECTED = sel.CRIT_S_EXPECTED          # 1.027
CRIT_S_TOL = sel.CRIT_S_TOL                    # 0.001
RECORDED_DELTA = 0.33634                       # delta_hat, GLS coefficient of h under C on rows_a (as registered)
DELTA_ATOL = 5e-6                              # absolute: the precision at which delta_hat was recorded
RECORDED_TAU_N = sel.RECORDED_TAU_N            # 0.03137144323410943
TAU_N_RTOL = 1e-6
KDE_SEED_BASE = 300_000                        # bootstrap resample b: default_rng(300_000 + b)
PAIR_DECIMALS = 4                              # per-simulation pairs saved rounded to 4 decimals
TIE_PAIR = 5e-5                                # tests: pairs this close are rounding ties
TIE_D = 1.5e-4                                 # tests: D this close to D_obs is a rounding tie
CHUNK = 500                                    # simulations generated at a time

UNDET_MC = "undetermined (Monte Carlo)"
EXCL = "excluded ({s})"
NOT_EXCL = "not excluded ({s})"

READ_NE = "not evaluable"
READ_ONE = "the {n} tested diffuse models {models} excluded by J; one offset host not excluded"
QUAL_BOTH = "(both statistics)"
QUAL_J = "(joint statistic only; D does not exclude τ = {taus})"
READ_DIFFUSE = "tested diffuse model(s) not excluded (τ = {taus})"
READ_NEITHER = "neither one offset host nor diffuse scatter reproduces the observed spreads"
READ_UNDET = "undetermined"

BLOCK_NE_OBSERVED = "not evaluable (observed values differ from the recorded ones: code or data change)"

SECTION5 = {
    "one": ("the R2-RE-SEL post-hoc bullet ('points towards one outlying host but does not show it') is "
            "replaced by this pre-registered reading, quoted with the caveats: δ̂ fitted on the same data, N5584 "
            "identified post hoc, J's quadrant anchored at a point chosen after seeing the data (calibrated, "
            "but chosen post hoc), C taken as correct (R2-RE-SEL referee point 5){joint}"),
    "diffuse": ("section 5 states that the data do not distinguish one outlying host from host-level scatter "
                "of R2-RE's size; R2-RE-SEL's reading stays, glossed 'consistent with C after removing one host, "
                "and not distinguished from diffuse scatter'"),
    "neither": ("section 5 states that neither model reproduces both spreads, and the 'one outlying host' "
                "gloss is marked unsupported"),
    "stays": "the post-hoc bullet stays as it is, with this outcome next to it",
}
NUMBER_WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}


# ---------------------------------------------------------------- names
def vkey(tau):
    """Model key of V(tau): V050, V077, V105."""
    return "V%03d" % int(round(tau * 1000))


def fmt_taus(taus):
    return ", ".join(f"{t:g}" for t in taus)


def model_keys(taus):
    """The eight models in the pre-registered order (C, the V(tau), O and the reported variants)."""
    return ["C"] + [vkey(t) for t in taus] + ["O", "Olo", "OVN", "Oany"]


def decisive_keys(taus):
    return [vkey(t) for t in taus] + ["O"]


# ---------------------------------------------------------------- labels and reading (pure)
def stat_label(k, n, stat):
    """Three-way Clopper-Pearson label for statistic D or J (rob.three_way)."""
    return rob.three_way(k, n, EXCL.format(s=stat), NOT_EXCL.format(s=stat))


def reading(models, taus):
    """Rules (1)-(5), checked in the pre-registered order. `models` maps a model key to its record
    (status, D.label, J.label); only the decisive models V(tau) and O enter."""
    vk = [vkey(t) for t in taus]
    if not all(models.get(k, {}).get("status") == "evaluated" for k in vk + ["O"]):         # (1)
        return READ_NE
    J = lambda k: models[k]["J"]["label"]
    D = lambda k: models[k]["D"]["label"]
    v_excl_j = all(J(k) == EXCL.format(s="J") for k in vk)
    if v_excl_j and J("O") == NOT_EXCL.format(s="J") and D("O") == NOT_EXCL.format(s="D"):     # (2)
        not_d = [t for t, k in zip(taus, vk) if D(k) != EXCL.format(s="D")]
        qual = QUAL_BOTH if not not_d else QUAL_J.format(taus=fmt_taus(not_d))
        return READ_ONE.format(n=NUMBER_WORDS.get(len(vk), str(len(vk))),
                               models=", ".join(f"V({t:g})" for t in taus)) + " " + qual
    not_j = [t for t, k in zip(taus, vk) if J(k) == NOT_EXCL.format(s="J")]
    if not_j:                                                                                 # (3)
        return READ_DIFFUSE.format(taus=fmt_taus(not_j))
    if v_excl_j and (J("O") == EXCL.format(s="J") or D("O") == EXCL.format(s="D")):           # (4)
        return READ_NEITHER
    return READ_UNDET                                                                         # (5)


def section5_action(read):
    """What the reading changes in section 5 (the text, not any earlier label)."""
    if read.endswith("; one offset host not excluded " + QUAL_BOTH):
        return SECTION5["one"].format(joint="")
    if "; one offset host not excluded (joint statistic only" in read:
        return SECTION5["one"].format(joint=", and 'joint statistic only'")
    if read.startswith("tested diffuse model(s) not excluded"):
        return SECTION5["diffuse"]
    if read == READ_NEITHER:
        return SECTION5["neither"]
    return SECTION5["stays"]


def observed_mismatches(obs, rec):
    """Rule (1)'s observed-value checks: spread_37 and spread_36 (relative 1e-9), criterion S selecting the
    host with spread_excl within 0.001 of the expected value, delta_hat (absolute 5e-6, its recorded precision)."""
    bad = []
    for key in ("spread_37", "spread_36"):
        if not abs(obs[key] - rec[key]) <= SPREAD_RTOL * abs(rec[key]):
            bad.append(f"{key} {obs[key]!r} vs recorded {rec[key]!r} (relative {SPREAD_RTOL:g})")
    if not abs(obs["delta_hat"] - rec["delta_hat"]) <= DELTA_ATOL:
        bad.append(f"delta_hat {obs['delta_hat']!r} vs recorded {rec['delta_hat']!r} (absolute {DELTA_ATOL:g})")
    if not obs["crit_s_selects_host"]:
        bad.append(f"criterion S selects {obs['crit_s_selected']}, not {obs['host']}")
    if not abs(obs["crit_s_host_value"] - rec["crit_s"]) <= CRIT_S_TOL:
        bad.append(f"criterion S spread_excl for {obs['host']} {obs['crit_s_host_value']!r}, "
                   f"not {rec['crit_s']} within {CRIT_S_TOL}")
    return bad


# ---------------------------------------------------------------- statistics (pure)
def quadrant_counts(points, ref, chunk=500):
    """For each point x: #{r in ref: r[0] >= x[0] and r[1] <= x[1]} (the quadrant 'high spread_37, low
    spread_36'), as integers."""
    points = np.asarray(points, dtype=float).reshape(-1, 2)
    ref = np.asarray(ref, dtype=float).reshape(-1, 2)
    out = np.zeros(len(points), dtype=np.int64)
    for i in range(0, len(points), chunk):
        p = points[i:i + chunk]
        out[i:i + chunk] = np.sum((ref[None, :, 0] >= p[:, None, 0]) & (ref[None, :, 1] <= p[:, None, 1]), axis=1)
    return out


def j_stat(pairs, obs):
    """Calibrated quadrant statistic J: half A = even simulation index, half B = odd. Returns the half-B
    counts, the count at the observed point, k_J = #{i in B: count_i <= count_obs}, n_A, n_B."""
    pairs = np.asarray(pairs, dtype=float)
    a, b = pairs[0::2], pairs[1::2]
    counts_b = quadrant_counts(b, a)
    c_obs = int(quadrant_counts(np.asarray(obs, dtype=float)[None, :], a)[0])
    k = int(np.sum(counts_b <= c_obs))
    return {"counts_b": counts_b, "count_obs": c_obs, "k": k, "n_A": int(len(a)), "n_B": int(len(b))}


def d_stat(d_sims, d_obs):
    d_sims = np.asarray(d_sims, dtype=float)
    return int(np.sum(d_sims >= d_obs)), int(len(d_sims))


def crit_s_batch(Z, excl):
    """sel.crit_s_values for a block of simulations: Z holds Delta_k / sigma_k (subsets x simulations);
    returns spread_excl (hosts x simulations), NaN for a host in every subset."""
    out = np.full((len(excl), Z.shape[1]), np.nan)
    for j, e in enumerate(excl):
        if e.any():
            out[j] = np.std(Z[e], axis=0)
    return out


def _share(k, n):
    lo, hi = rob._cp(k, n)
    return {"k": int(k), "n": int(n), "share": k / n if n else None, "ci95": [lo, hi]}


def kde_ratio(num, den, x, factor_scale=1.0):
    """Density ratio num/den at x from scipy.stats.gaussian_kde (Scott bandwidth, scaled by factor_scale).
    num, den: (n,) for one dimension or (n, 2) for two. None when the denominator density is 0."""
    num = np.asarray(num, dtype=float)
    den = np.asarray(den, dtype=float)
    pts = lambda a: a.T if a.ndim == 2 else a
    xx = np.asarray(x, dtype=float).reshape(-1, 1) if num.ndim == 2 else np.atleast_1d(float(x))
    try:
        kn, kd = stats.gaussian_kde(pts(num)), stats.gaussian_kde(pts(den))
        if factor_scale != 1.0:
            kn = stats.gaussian_kde(pts(num), bw_method=kn.factor * factor_scale)
            kd = stats.gaussian_kde(pts(den), bw_method=kd.factor * factor_scale)
    except np.linalg.LinAlgError:       # a degenerate (singular) resample: the ratio is undefined
        return None
    fn, fd = float(kn(xx)[0]), float(kd(xx)[0])
    return None if fd == 0.0 else fn / fd


def kde_report(num, den, x, n_boot, seed_base=KDE_SEED_BASE):
    """Point ratio, 68% interval from n_boot paired bootstrap resamples (one index draw per resample from
    default_rng(seed_base + b), applied to both models' simulations: the eps_s are common), and the ratio
    with the bandwidth halved. Reported only; no label uses it."""
    num = np.asarray(num, dtype=float)
    den = np.asarray(den, dtype=float)
    n = len(num)
    boot = []
    for b in range(int(n_boot)):
        idx = np.random.default_rng(seed_base + b).integers(0, n, n)
        boot.append(kde_ratio(num[idx], den[idx], x))
    fin = [r for r in boot if r is not None]
    return {"ratio": kde_ratio(num, den, x), "ratio_half_bandwidth": kde_ratio(num, den, x, 0.5),
            "boot_68": [float(q) for q in np.percentile(fin, [16, 84])] if fin else None,
            "n_boot": int(n_boot), "n_boot_undefined": int(len(boot) - len(fin))}


# ---------------------------------------------------------------- models
def eps_block(seed_base, s_list, n):
    """eps_s = default_rng(seed_base + s).standard_normal(n), one column per s (common to every model)."""
    E = np.empty((n, len(s_list)))
    for i, s in enumerate(s_list):
        E[:, i] = np.random.default_rng(seed_base + int(s)).standard_normal(n)
    return E


def offset_hosts(seed_base, n_sims, n_hosts):
    """O_any's offset host of simulation s: default_rng(seed_base + s).integers(0, n_hosts)."""
    return np.array([int(np.random.default_rng(seed_base + s).integers(0, n_hosts)) for s in range(n_sims)],
                    dtype=np.int64)


def model_y(spec, K, yhat, E, s_list, gpos, any_hosts=None):
    """y on rows_a for the simulations s_list (columns of E): y_hat + K eps_s, plus the model's offset on the
    calibrator rows of one host (positions gpos[host] in rows_a)."""
    Y = yhat[:, None] + K @ E
    if spec["delta"] is not None:
        if spec["offset"] == "any":
            hosts = any_hosts[np.asarray(s_list, dtype=np.int64)]
            for i, h in enumerate(hosts):
                Y[gpos[h], i] += spec["delta"]
        else:
            Y[gpos[spec["offset"]], :] += spec["delta"]
    return Y


def model_specs(taus, col, delta, sigma_delta, tau_n):
    """The eight models: covariance (tau of the random effect, 0 for C), offset (host column, 'any' or None)
    and delta. tau_n None: O(delta_hat) + V(tau_hat_N) is not run."""
    sp = {"C": {"tau": 0.0, "offset": None, "delta": None, "decisive": False,
                "description": "C: y_hat + K_C eps_s"}}
    for t in taus:
        sp[vkey(t)] = {"tau": float(t), "offset": None, "delta": None, "decisive": True,
                       "description": f"V({t:g}): K from with_re(C, calib_groups, {t:g})"}
    sp["O"] = {"tau": 0.0, "offset": col, "delta": delta, "decisive": True,
               "description": "O(δ̂): y_C,s + δ̂ h (N5584's calibrator rows)"}
    sp["Olo"] = {"tau": 0.0, "offset": col, "delta": delta - sigma_delta, "decisive": False,
                 "description": "O(δ̂ − σ_δ): y_C,s + (δ̂ − σ_δ) h"}
    sp["OVN"] = {"tau": tau_n, "offset": col, "delta": delta, "decisive": False,
                 "description": "O(δ̂) + V(τ̂_N): N5584 offset and τ̂_N on all 37 hosts"}
    sp["Oany"] = {"tau": 0.0, "offset": "any", "delta": delta, "decisive": False,
                  "description": "O_any(δ̂): the offset on a host drawn uniformly from the 37 in each simulation"}
    return sp


def fit_delta(L, y, C, rows_a, h_rows, fns):
    """delta_hat and sigma_delta: the GLS coefficient of the indicator of h_rows, fitted with L under C on
    rows_a (L with one extra column)."""
    h = np.zeros((L.shape[0], 1))
    h[np.asarray(h_rows), 0] = 1.0
    res = fns["fit"](np.hstack([L, h]), y, C, rows_a)
    return float(res["q"][-1]), float(res["sigma"][-1])


# ---------------------------------------------------------------- the block
def run_block(L, y, C, nz, rows_a, groups, labels, host_rows, picks, P, fns, log, n_pick=10, tau_n=None,
              expected_col=None, recorded=None, rob_spread_obs=None):
    """The whole R2-RE-D block. `groups` are the 37 calibrator SN groups (calib_groups), `picks` R4's draws
    on the 37-host system (at least the first rob_n_subsets), `tau_n` tau_hat_N from the R2-RE-N5584 block of
    the same run (None: computed here, as in the standalone mode). `recorded` overrides the recorded values
    (tests only). Returns (out, sims): sims maps each model key to its per-simulation record."""
    t_block = time.perf_counter()
    rows_a = np.asarray(rows_a)
    nh = len(groups)
    cols = [j for j, h in enumerate(labels) if h == P["n5584_host"]]
    if len(cols) != 1:
        raise RuntimeError(f"host {P['n5584_host']} labels {len(cols)} columns, expected 1")
    col = cols[0]
    if expected_col is not None and col != expected_col:
        raise RuntimeError(f"{P['n5584_host']} is column {col}, documented as column {expected_col}")
    host = labels[col]
    rec = {"spread_37": RECORDED_SPREAD_37, "spread_36": RECORDED_SPREAD_36, "crit_s": CRIT_S_EXPECTED,
           "delta_hat": RECORDED_DELTA, "tau_n": RECORDED_TAU_N}
    rec.update(recorded or {})
    taus = [float(t) for t in P["d_taus"]]
    n_sims, n_sub = int(P["d_n_sims"]), int(P["rob_n_subsets"])
    keys = model_keys(taus)
    out = {"host": host, "column": int(col),
           "headline": "R2-RE's row stays the headline; this block attaches labels to R2-RE-SEL's reading",
           "settings": {"eps": "numpy.random.default_rng(d_seed_base + s).standard_normal(len(rows_a)), "
                               "the same eps_s for every model",
                        "offset_host_any": "numpy.random.default_rng(d_host_seed_base + s).integers(0, 37)",
                        "kde_bootstrap": "numpy.random.default_rng(300_000 + b).integers(0, n, n), one index "
                                         "draw per resample applied to both models",
                        **{k: P[k] for k in ("d_seed_base", "d_n_sims", "d_taus", "d_host_seed_base",
                                             "d_kde_boot", "d_only", "rob_n_subsets", "r4_seed", "n5584_host")},
                        "n_pick": int(n_pick),
                        "subsets_37": "the first rob_n_subsets R4 draws on 37 hosts (ROB part B's)",
                        "subsets_36": "the first rob_n_subsets index draws rng.choice(36, 10) of default_rng(r4_seed), "
                                      "mapped onto the 36 columns other than d'",
                        "half_A": "s even", "half_B": "s odd", "pair_decimals": PAIR_DECIMALS},
           "recorded": rec, "model_keys": keys, "decisive": decisive_keys(taus)}
    seconds = {}
    checks = {}

    def stop(status, extra=None):
        out.update(status=status, reading=READ_NE, section5=SECTION5["stays"], checks=checks)
        if extra:
            out.update(extra)
        seconds["block"] = time.perf_counter() - t_block
        out["seconds"] = seconds
        log("R2-RE-D: " + status)
        return out, {k: {"model": k, "status": status} for k in keys}

    # ---- rule (1): empty index streams
    stream = sel.index_stream(n_sub, P["r4_seed"], nh - 1, n_pick)
    if not picks or n_sub <= 0:
        return stop("not evaluable (empty index stream: R4 has no draws)")
    if not stream:
        return stop("not evaluable (empty index stream: R4-N)")
    if len(picks) < n_sub or len(stream) < n_sub:
        return stop("not evaluable (index stream shorter than rob_n_subsets)")
    use = picks[:n_sub]

    # ---- fit under C on rows_a, delta_hat, the 37-host shift rows (criterion S)
    t0 = time.perf_counter()
    try:
        res_full = fns["fit"](L, y, C, rows_a, est=True)
    except (np.linalg.LinAlgError, ValueError) as e:
        if not fns["is_fit_failure"](e):
            raise
        return stop(f"not evaluable (fit: the reference fit under C on rows_a: {e})")
    kept = res_full["kept"]
    yhat = L[np.ix_(rows_a, kept)] @ res_full["q"][kept]
    ya_real = y[rows_a]
    n_a = len(rows_a)
    gpos = []
    for g in groups:
        g = np.asarray(g)
        pg = np.searchsorted(rows_a, g)
        if np.any(pg >= n_a) or not np.array_equal(rows_a[np.minimum(pg, n_a - 1)], g):
            raise RuntimeError("a calibrator group has rows outside rows_a")
        gpos.append(pg)
    try:
        delta, sigma_delta = fit_delta(L, y, C, rows_a, groups[col], fns)
    except (np.linalg.LinAlgError, ValueError) as e:
        if not fns["is_fit_failure"](e):
            raise
        return stop(f"not evaluable (fit: δ̂: {e})")
    seconds["delta_fit"] = time.perf_counter() - t0
    t0 = time.perf_counter()
    any_host = nz[:, :nh].any(axis=1)
    base_rows = np.array([i for i in rows_a if not any_host[i]])
    try:
        M37, sig37 = rob.shift_rows(L, y, C, rows_a, res_full, use, base_rows, host_rows, fns)
    except (np.linalg.LinAlgError, ValueError) as e:
        if not fns["is_fit_failure"](e):
            raise
        return stop(f"not evaluable (fit: building the 37-host shift rows: {e})")
    contains = np.zeros((len(use), nh), bool)
    for i, pk in enumerate(use):
        contains[i, np.asarray(pk)] = True
    excl = [~contains[:, j] for j in range(nh)]
    seconds["rows_37"] = time.perf_counter() - t0

    # ---- the reduced systems' rows (built once, shared by every model)
    built = {}

    def build(d):
        tb = time.perf_counter()
        red = sel.reduced_system(nz, rows_a, d, groups, host_rows)
        rows_n = red["rows_n"]
        picks_d = [red["host_cols_n"][ix] for ix in stream]
        res_ref = fns["fit"](L, y, C, rows_n, est=True)
        M, sig = rob.shift_rows(L, y, C, rows_n, res_ref, picks_d, red["base_n"], red["host_rows_n"], fns)
        built[d] = time.perf_counter() - tb
        return np.searchsorted(rows_a, rows_n), M, sig, red

    # ---- observed values (rule (1))
    t0 = time.perf_counter()
    sp37_obs = float(np.std((M37 @ ya_real) / sig37))
    s_real = sel.crit_s_values(M37, sig37, excl, ya_real)
    d_real = sel.pick_min(s_real)
    try:
        cache = {col: build(col)}
    except (np.linalg.LinAlgError, ValueError) as e:
        if not fns["is_fit_failure"](e):
            raise
        return stop(f"not evaluable (fit: building the rows of the reduced system without {host}: {e})")
    pos_c, Mc, sigc, red_c = cache[col]
    sp36_obs = float(np.std((Mc @ ya_real[pos_c]) / sigc))
    d_obs = sp37_obs - sp36_obs
    dproxy_obs = sp37_obs - float(np.nanmin(s_real))
    obs = {"spread_37": sp37_obs, "spread_36": sp36_obs, "D": d_obs, "D_proxy": dproxy_obs,
           "delta_hat": delta, "sigma_delta": sigma_delta, "delta_over_sigma": delta / sigma_delta,
           "host": host, "crit_s_selected": labels[d_real], "crit_s_selects_host": bool(d_real == col),
           "crit_s_host_value": float(s_real[col]), "crit_s_min": float(np.nanmin(s_real)),
           "n_calib_rows_host": int(len(groups[col])), "calib_rows_host": [int(r) for r in groups[col]]}
    bad = observed_mismatches(obs, rec)
    obs["mismatches"] = bad
    out["observed"] = obs
    out["real_spread_excl"] = [{"column": j, "host": labels[j],
                                "spread_excl": None if np.isnan(s_real[j]) else float(s_real[j])}
                               for j in range(nh)]
    checks["spread_37_matches_rob"] = (None if rob_spread_obs is None else
                                       bool(abs(sp37_obs - rob_spread_obs) <= SPREAD_RTOL * abs(rob_spread_obs)))
    checks["first_subsets_36"] = [[int(j) for j in red_c["host_cols_n"][ix]] for ix in stream[:5]]
    seconds["observed"] = time.perf_counter() - t0
    if bad:
        return stop(BLOCK_NE_OBSERVED)

    # ---- tau_hat_N (O(delta_hat) + V(tau_hat_N), reported only)
    t0 = time.perf_counter()
    tn = {"source": "R2-RE-N5584 block of the same run" if tau_n is not None else
          "REML on the reduced system without the host (computed in this block)"}
    if tau_n is None:
        try:
            est = fns["reml_tau"](lambda t: fns["reml_m2l"](L, y, C, red_c["rows_n"], red_c["groups_n"], t),
                                  P["re_tau_max"], P["re_grid_step"], interval=False)
            if est["at_upper_bound"]:
                tn["status"] = "not run (τ̂_N at the upper bound)"
            else:
                tau_n = 0.0 if est["at_zero"] else est["tau_hat"]
        except (np.linalg.LinAlgError, ValueError) as e:
            if not fns["is_fit_failure"](e):
                raise
            tn["status"] = f"not run (τ̂_N REML fit failed: {e})"
    tn["tau_hat_N"] = tau_n
    tn["recorded"] = rec["tau_n"]
    if tau_n is not None and not abs(tau_n - rec["tau_n"]) <= TAU_N_RTOL * abs(rec["tau_n"]):
        tn["status"] = f"not run (τ̂_N {tau_n!r} does not reproduce the recorded {rec['tau_n']!r})"
    tn.setdefault("status", "reproduced")
    out["tau_hat_N"] = tn
    seconds["tau_hat_N"] = time.perf_counter() - t0
    specs = model_specs(taus, col, delta, sigma_delta, tau_n if tn["status"] == "reproduced" else None)

    # ---- model status and Cholesky factors (one per covariance, shared)
    t0 = time.perf_counter()
    status = {k: "evaluated" for k in keys}
    if tn["status"] != "reproduced":
        status["OVN"] = tn["status"]
    factors, fail_f = {}, {}
    for k in keys:
        if status[k] != "evaluated":
            continue
        tau = specs[k]["tau"]
        if tau in factors or tau in fail_f:
            continue
        try:
            V = C if tau == 0.0 else fns["with_re"](C, groups, tau)
            factors[tau] = linalg.cholesky(V[np.ix_(rows_a, rows_a)], lower=True)
            V = None
        except np.linalg.LinAlgError as e:
            fail_f[tau] = str(e)
    for k in keys:
        if status[k] == "evaluated" and specs[k]["tau"] in fail_f:
            status[k] = f"not evaluable (Cholesky factor failed: {fail_f[specs[k]['tau']]})"
    run_keys = [k for k in keys if status[k] == "evaluated"]
    any_hosts = offset_hosts(P["d_host_seed_base"], n_sims, nh)
    seconds["cholesky"] = time.perf_counter() - t0

    # ---- pass 1: spread_37, criterion S (d'), D_proxy for every model
    t0 = time.perf_counter()
    sp37 = {k: np.empty(n_sims) for k in run_keys}
    dsel = {k: np.empty(n_sims, dtype=np.int64) for k in run_keys}
    dprox = {k: np.empty(n_sims) for k in run_keys}
    for c0 in range(0, n_sims, CHUNK):
        s_list = np.arange(c0, min(c0 + CHUNK, n_sims))
        E = eps_block(P["d_seed_base"], s_list, n_a)
        for k in run_keys:
            Y = model_y(specs[k], factors[specs[k]["tau"]], yhat, E, s_list, gpos, any_hosts)
            Z = (M37 @ Y) / sig37[:, None]
            sp37[k][s_list] = Z.std(axis=0)
            cs = crit_s_batch(Z, excl)
            dsel[k][s_list] = [sel.pick_min(cs[:, i]) for i in range(cs.shape[1])]
            dprox[k][s_list] = sp37[k][s_list] - np.nanmin(cs, axis=0)
        if c0 % 2000 == 0:
            log(f"  R2-RE-D pass 1: {c0 + len(s_list)} of {n_sims} per model, {time.perf_counter() - t0:.0f} s")
    M37 = None
    seconds["pass_1"] = time.perf_counter() - t0

    # ---- pass 2: spread_36 for d', the rows built once per dropped host, simulations grouped by d'
    t0 = time.perf_counter()
    sp36 = {k: np.full(n_sims, np.nan) for k in run_keys}
    need = sorted({int(d) for k in run_keys for d in dsel[k]})
    failed_d = {}
    for d in need:
        if d in cache:
            pos_n, M, sig, _ = cache.pop(d)
        else:
            try:
                pos_n, M, sig, _ = build(d)
            except (np.linalg.LinAlgError, ValueError) as e:
                if not fns["is_fit_failure"](e):
                    raise
                failed_d[d] = str(e)
                continue
        s_union = np.flatnonzero(np.any([dsel[k] == d for k in run_keys], axis=0))
        for c0 in range(0, len(s_union), CHUNK):
            s_list = s_union[c0:c0 + CHUNK]
            E = eps_block(P["d_seed_base"], s_list, n_a)
            for k in run_keys:
                m = dsel[k][s_list] == d
                if not m.any():
                    continue
                Y = model_y(specs[k], factors[specs[k]["tau"]], yhat, E[:, m], s_list[m], gpos, any_hosts)
                sp36[k][s_list[m]] = np.std((M @ Y[pos_n]) / sig[:, None], axis=0)
        M = None
        log(f"  R2-RE-D pass 2: dropped host {labels[d]} ({time.perf_counter() - t0:.0f} s)")
    cache.clear()
    factors.clear()
    seconds["pass_2"] = time.perf_counter() - t0
    out["dropped_hosts_built"] = {"n_distinct": len(built), "hosts": [labels[d] for d in sorted(built)],
                                  "seconds_build": {labels[d]: t for d, t in sorted(built.items())},
                                  "failed": {labels[d]: e for d, e in sorted(failed_d.items())}}
    for k in run_keys:
        fails = sorted(set(int(d) for d in dsel[k]) & set(failed_d))
        if fails:
            status[k] = ("not evaluable (fit: building the rows for dropped host "
                         + ", ".join(labels[d] for d in fails) + ")")

    # ---- statistics, labels
    t0 = time.perf_counter()
    obs_pt = np.array([sp37_obs, sp36_obs])
    models, sims = {}, {}
    for k in keys:
        mrec = {"description": specs[k]["description"], "decisive": specs[k]["decisive"], "status": status[k]}
        if specs[k]["delta"] is not None:
            mrec["delta"] = specs[k]["delta"]
        if specs[k]["tau"] is not None:
            mrec["tau"] = specs[k]["tau"]
        if status[k] != "evaluated":
            models[k] = mrec
            sims[k] = {"model": k, "status": status[k]}
            continue
        a, b = sp37[k], sp36[k]
        dd = a - b
        pairs = np.column_stack([a, b])
        kd, nd = d_stat(dd, d_obs)
        lab_d, ci_d = stat_label(kd, nd, "D")
        js = j_stat(pairs, obs_pt)
        lab_j, ci_j = stat_label(js["k"], js["n_B"], "J")
        kq = int(np.sum((a >= sp37_obs) & (b <= sp36_obs)))
        freq = Counter(int(d) for d in dsel[k])
        mrec.update({
            "D": {"obs": d_obs, "k": kd, "n": nd, "p": (1 + kd) / (1 + nd), "ci95": list(ci_d), "label": lab_d},
            "J": {"k": js["k"], "n_B": js["n_B"], "n_A": js["n_A"], "count_obs": js["count_obs"],
                  "t_obs": js["count_obs"] / js["n_A"], "p": (1 + js["k"]) / (1 + js["n_B"]), "ci95": list(ci_j),
                  "label": lab_j},
            "Q_raw": {**_share(kq, n_sims), "note": "raw quadrant probability at the observed point over all "
                                                    "simulations; descriptive only, not a p value"},
            "quantiles_5_50_95": {"spread_37": [float(q) for q in np.percentile(a, [5, 50, 95])],
                                  "spread_36": [float(q) for q in np.percentile(b, [5, 50, 95])],
                                  "D": [float(q) for q in np.percentile(dd, [5, 50, 95])]},
            "P_spread_37_ge_obs": _share(int(np.sum(a >= sp37_obs)), n_sims),
            "P_spread_36_le_obs": _share(int(np.sum(b <= sp36_obs)), n_sims),
            "D_proxy": {"obs": dproxy_obs, **_share(int(np.sum(dprox[k] >= dproxy_obs)), n_sims),
                        "p": (1 + int(np.sum(dprox[k] >= dproxy_obs))) / (1 + n_sims)},
            "selected": {"frequency": {labels[j]: c for j, c in sorted(freq.items())},
                         "n_host": int(freq.get(col, 0))},
        })
        srec = {"model": k, "status": "evaluated", "n": n_sims, "seed_base": int(P["d_seed_base"]),
                "obs": [sp37_obs, sp36_obs], "D_obs": d_obs,
                "pairs": [[round(float(x), PAIR_DECIMALS), round(float(z), PAIR_DECIMALS)] for x, z in pairs],
                "dropped": [int(d) for d in dsel[k]], "n_A": js["n_A"], "n_B": js["n_B"],
                "half_b_counts": [int(c) for c in js["counts_b"]], "count_obs": js["count_obs"]}
        if specs[k]["offset"] == "any":
            mrec["selected"]["n_offset_host"] = int(np.sum(dsel[k] == any_hosts))
            srec["offset_host"] = [int(h) for h in any_hosts]
        models[k] = mrec
        sims[k] = srec
    out["models"] = models
    seconds["statistics"] = time.perf_counter() - t0

    # ---- KDE density ratios of O(delta_hat) to each V(tau) and to C at the observed point (reported)
    t0 = time.perf_counter()
    kde = {"note": "reported, not decisive: tail densities depend on the bandwidth, so no label uses them"}
    if models["O"]["status"] == "evaluated":
        num2, num1 = np.column_stack([sp37["O"], sp36["O"]]), sp37["O"] - sp36["O"]
        for k in [vkey(t) for t in taus] + ["C"]:
            if models[k]["status"] != "evaluated":
                continue
            kde[f"O_over_{k}"] = {
                "2d": kde_report(num2, np.column_stack([sp37[k], sp36[k]]), obs_pt, P["d_kde_boot"]),
                "1d_D": kde_report(num1, sp37[k] - sp36[k], d_obs, P["d_kde_boot"])}
    out["kde"] = kde
    seconds["kde"] = time.perf_counter() - t0

    read = reading(models, taus)
    out.update(status="evaluated", reading=read, section5=section5_action(read), checks=checks)
    seconds["block"] = time.perf_counter() - t_block
    out["seconds"] = seconds
    log(f"R2-RE-D: {read}")
    return out, sims


def summary(d_out):
    """Short summary for summary.json (R2_RE_D)."""
    if "models" not in d_out:
        return {"status": d_out.get("status"), "reading": d_out.get("reading")}
    m = {}
    for k, r in d_out["models"].items():
        if r.get("status") != "evaluated":
            m[k] = {"status": r.get("status")}
        else:
            m[k] = {"D": r["D"]["label"], "p_D": r["D"]["p"], "J": r["J"]["label"], "p_J": r["J"]["p"]}
    return {"status": d_out.get("status"), "reading": d_out.get("reading"), "models": m}


def summary_with_key(old_text, key, value, before="runtime_s"):
    """summary.json with only `key` set to `value` (standalone mode). Every other key keeps its serialised
    bytes: refuses (RuntimeError) when the existing file does not re-serialise to itself. An existing key is
    replaced in place; a new one goes before `before` (as in a full run) or at the end."""
    from astrolab.results import to_jsonable
    dump = lambda o: json.dumps(to_jsonable(o), indent=1, ensure_ascii=False)
    old = json.loads(old_text)
    if not isinstance(old, dict) or dump(old) != old_text:
        raise RuntimeError("summary.json does not re-serialise byte-identically; refusing to update it")
    new = {}
    for k, v in old.items():
        if k == before and key not in old:
            new[key] = value
        new[k] = value if k == key else v
    if key not in new:
        new[key] = value
    for k in old:                       # the other keys' serialised values are unchanged
        if k != key and dump(new[k]) != dump(old[k]):
            raise RuntimeError(f"summary.json key {k} would change")
    return new
