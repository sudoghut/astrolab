"""Statistics and decision labels of study 011 (README sections 2, 4.3-4.6).

Pure functions: no data access, no PARAMS. Thresholds that README section 2 fixes are passed in
by run.py from PARAMS (their defaults equal the pre-registered values).
"""
from __future__ import annotations

import math

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.stats import chi2

NOT_EVALUABLE = "not evaluable"
UNDETERMINED = "undetermined"


# ---------------------------------------------------------------------------------------------
# p-values

def p_boot(k: int, n: int) -> float:
    """README section 2: p_boot = (1 + k)/(1 + N)."""
    return (1.0 + k) / (1.0 + n)


def p_boot_ge(obs: float, mocks) -> tuple[float, int]:
    """p_boot with k = number of mocks at least as large as obs."""
    m = np.asarray(mocks, float)
    k = int(np.sum(m >= obs))
    return p_boot(k, len(m)), k


def p_mcse(p: float, n: int) -> float:
    return math.sqrt(max(p * (1.0 - p), 0.0) / n) if n else float("nan")


def calibrated_p(obs: float, mocks, d: int) -> dict:
    """Bartlett-type rescaling (README section 2, T3): chi2_d p of obs * d/m, m = mean of the mocks.

    Also the Monte Carlo standard error of p, propagated from the standard error of m."""
    m_arr = np.asarray(mocks, float)
    n = len(m_arr)
    m = float(np.mean(m_arr)) if n else float("nan")
    se_m = float(np.std(m_arr, ddof=1) / math.sqrt(n)) if n > 1 else float("nan")
    out = {"m": m, "se_m": se_m, "d": d, "factor": (d / m) if m > 0 else None}
    if not (m > 0):
        out.update(p_cal=None, p_cal_mcse=None, reason="mean of the mocks' 2 dlnL is 0")
        return out
    out["p_cal"] = float(chi2.sf(obs * d / m, d))
    out["p_cal_mcse"] = calibrated_p_mcse(obs, m, se_m, d)
    return out


def calibrated_p_mcse(obs, m, se_m, d):
    if not (m > 0) or not np.isfinite(se_m):
        return None
    h = max(1e-6 * m, 1e-9)
    lo, hi = chi2.sf(obs * d / max(m - h, 1e-300), d), chi2.sf(obs * d / (m + h), d)
    return float(abs(hi - lo) / (2.0 * h) * se_m)


def p_with_factor(obs: float, factor: float | None, d: int):
    """Calibrated p using a rescaling factor d/m from another run (T6 variants 3-10)."""
    if factor is None:
        return None
    return float(chi2.sf(obs * factor, d))


def p_raw(obs: float, d: int) -> float:
    return float(chi2.sf(obs, d))


# ---------------------------------------------------------------------------------------------
# Labels (README section 2)

def t1_label(n_inside: int) -> str:
    if n_inside >= 5:
        return "reproduced"
    if n_inside >= 3:
        return "partly reproduced"
    return "not reproduced"


def t3_standing_label(p_cal, p_rawv, p_bootv, n_reach, *, strong=1e-3, alpha=0.05) -> str:
    """Full rule: strongly if p_cal and p_raw < 0.001 and no mock reaches the observed value;
    excluded if p_cal < 0.05 and p_boot < 0.05; not excluded otherwise. None p_cal -> not evaluable."""
    if p_cal is None:
        return NOT_EVALUABLE
    if p_cal < strong and p_rawv < strong and n_reach == 0:
        return "standing excluded strongly"
    if p_cal < alpha and p_bootv < alpha:
        return "standing excluded"
    return "standing not excluded"


def t3_standing_label_reduced(p_cal, p_rawv, *, strong=1e-3, alpha=0.05) -> str:
    """Reduced rule for T6 variants 3-10 (no new mocks): calibrated p and p_raw only."""
    if p_cal is None:
        return NOT_EVALUABLE
    if p_cal < strong and p_rawv < strong:
        return "standing excluded strongly"
    if p_cal < alpha:
        return "standing excluded"
    return "standing not excluded"


def t3_travel_label(p_cal, p_bootv, *, alpha=0.05) -> str:
    if p_cal is None:
        return NOT_EVALUABLE
    return ("pure travelling (B = 1) disfavoured" if (p_cal < alpha and p_bootv < alpha)
            else "pure travelling (B = 1) not disfavoured")


def t3_travel_label_reduced(p_cal, *, alpha=0.05) -> str:
    if p_cal is None:
        return NOT_EVALUABLE
    return "pure travelling (B = 1) disfavoured" if p_cal < alpha else "pure travelling (B = 1) not disfavoured"


def t4_label(p, power, *, p_excl=0.01, p_not=0.05, power_min=0.8) -> str:
    if p is None or power is None:
        return NOT_EVALUABLE
    if power < power_min:
        return UNDETERMINED
    if p < p_excl:
        return "standing excluded by the phases"
    if p > p_not:
        return "standing not excluded by the phases"
    return UNDETERMINED


def wavelength_label(lo, hi, band=(0.8, 1.25)) -> str:
    if lo is None or hi is None or not (np.isfinite(lo) and np.isfinite(hi)):
        return NOT_EVALUABLE
    if band[0] <= lo and hi <= band[1]:
        return "consistent"
    if hi < band[0] or lo > band[1]:
        return "different"
    return UNDETERMINED


def bhat_label(lo, hi, *, b_t=0.4, wavelengths="consistent", known_answer_pass=True) -> dict:
    """b-hat label; 'opposite' flags an interval entirely below -b_T (reported in addition)."""
    out = {"opposite_direction": bool(hi is not None and hi < -b_t)}
    if lo is None or hi is None or not (np.isfinite(lo) and np.isfinite(hi)):
        out["label"] = NOT_EVALUABLE
    elif wavelengths == "different":
        out["label"] = "not applicable (wavelengths differ)"
    elif not known_answer_pass:
        out["label"] = UNDETERMINED
    elif lo > b_t:
        out["label"] = "travelling component in K24's direction dominates"
    elif hi < b_t:
        out["label"] = "no travelling dominance in K24's direction"
    else:
        out["label"] = UNDETERMINED
    out["caveat_wavelengths_undetermined"] = wavelengths == UNDETERMINED
    return out


def t7_label(m2ll_a, m2ll_b, m2ll_c, margin=9.0) -> str:
    if m2ll_a + margin <= m2ll_b and m2ll_a + margin <= m2ll_c:
        return "CO prefers the travelling wave"
    return "CO does not distinguish"


def t8_label(halfwidth_broad, prior_sigma, median_shift_sigma, *, width_frac=0.5, shift_max=0.5) -> str:
    narrow = halfwidth_broad < width_frac * prior_sigma
    stable = abs(median_shift_sigma) < shift_max
    if narrow and stable:
        return "data-driven"
    if not narrow and not stable:
        return "prior-driven"
    return "partly data-driven"


# ---------------------------------------------------------------------------------------------
# README 4.10 (T-056, post hoc): R-CONV choice of the convention, T8-P

RCONV_SUFFIX = " (best among these 16 candidate conventions, post hoc)"
T8P_AT_BOUND = "prior-driven (posterior at the bound)"


def half_width(p16, p84) -> float:
    return 0.5 * (p84 - p16)


def width_ratio(ours: dict, k24: dict) -> float:
    """Median over the counted parameters of our 16-84% half-width over K24's.

    ours[name] = (p16, p84); k24[name] = (plus, minus) as printed (half-width (plus + minus)/2)."""
    r = [half_width(*ours[n]) / (0.5 * (k24[n][0] + k24[n][1])) for n in ours]
    return float(np.median(r))


def width_in(ratio, lo=2.0 / 3.0, hi=1.5) -> bool:
    return bool(ratio is not None and np.isfinite(ratio) and lo <= ratio <= hi)


def rconv_choose(rows, *, min_count=3, repro_count=5, ratio_range=(2.0 / 3.0, 1.5)) -> dict:
    """README 4.10 choice rule. rows: dicts with index, name, count, width_ratio, n_factors_differing.

    (i) no count >= 3: "not reproduced under any candidate convention", nothing chosen;
    (ii) among count >= 3 with the width ratio in [2/3, 3/2], the largest count;
    (iii) if none of those has its ratio in range, the largest count among count >= 3.
    Ties: fewest factors differing from (L, F, W), then the lowest index."""
    lo, hi = ratio_range
    cand = [r for r in rows if r["count"] >= min_count]
    if not cand:
        return {"case": "i", "chosen": None, "label": "column (3) not reproduced under any candidate convention"
                + RCONV_SUFFIX, "reason": f"every count <= {min_count - 1}", "status": "not reproduced"}
    inw = [r for r in cand if width_in(r["width_ratio"], lo, hi)]
    pool, case = (inw, "ii") if inw else (cand, "iii")
    best = min(pool, key=lambda r: (-r["count"], r["n_factors_differing"], r["index"]))
    ok_w = width_in(best["width_ratio"], lo, hi)
    reasons = []
    if best["count"] < repro_count:
        reasons.append(f"count {best['count']} of 6 (3-4)")
    if not ok_w:
        reasons.append(f"width ratio {best['width_ratio']:.3f} outside [2/3, 3/2]")
    status = "reproduced" if not reasons else "partly reproduced"
    return {"case": case, "chosen": best["index"], "chosen_name": best["name"],
            "label": f"column (3) {status} under {best['name']}" + RCONV_SUFFIX,
            "reason": "; ".join(reasons) or None, "status": status}


def t8p_label(halfwidth_broad, prior_sigma, median_shift_sigma, broad_median_omega0, bounds, *,
              bound_frac=0.05, width_frac=0.5, shift_max=0.5) -> dict:
    """README 4.10 Part B: section 2's T8 rule, except that a broad-prior median of omega0 within
    bound_frac of a bound's value (above (1 - f) hi or below (1 + f) lo) gives "prior-driven (posterior at
    the bound)", which takes precedence."""
    lo, hi = bounds
    at_bound = bool(broad_median_omega0 > (1.0 - bound_frac) * hi or broad_median_omega0 < (1.0 + bound_frac) * lo)
    rule = t8_label(halfwidth_broad, prior_sigma, median_shift_sigma, width_frac=width_frac, shift_max=shift_max)
    return {"label": T8P_AT_BOUND if at_bound else rule, "at_bound": at_bound, "width_shift_rule_label": rule,
            "bound_thresholds": [(1.0 + bound_frac) * lo, (1.0 - bound_frac) * hi]}


def overall_reading(t1_col4, t3_standing, t4, t5_bhat, t6) -> dict:
    """README section 2 'Overall reading', mechanically from the labels."""
    support = {
        "T1": t1_col4 in ("reproduced", "partly reproduced"),
        "T3": t3_standing in ("standing excluded", "standing excluded strongly"),
        "T4": t4 == "standing excluded by the phases",
        "T5": t5_bhat == "travelling component in K24's direction dominates",
        "T6": t6 == "robust",
    }
    if all(support.values()):
        reading = "K24's travelling-wave reading is supported by these data"
    elif t3_standing == "standing not excluded" and t5_bhat == "no travelling dominance in K24's direction":
        reading = "not supported"
    else:
        reading = "mixed"
    labels = {"T1": t1_col4, "T3": t3_standing, "T4": t4, "T5": t5_bhat, "T6": t6}
    groups = {"support": [], "do_not_support": [], "undetermined_or_not_evaluable": []}
    for k, ok in support.items():
        lab = labels[k]
        if ok:
            groups["support"].append(k)
        elif lab in (UNDETERMINED, NOT_EVALUABLE) or "not applicable" in str(lab):
            groups["undetermined_or_not_evaluable"].append(k)
        else:
            groups["do_not_support"].append(k)
    return {"reading": reading, "labels": labels, **groups}


# ---------------------------------------------------------------------------------------------
# T4: phases

def phase2(z, omega, vz):
    """2 phi_k with phi_k = arctan(z omega / v_z); computed with atan2 (period pi of phi removed)."""
    return 2.0 * np.arctan2(np.asarray(z) * np.asarray(omega), np.asarray(vz))


def circular_R(z, omega, vz) -> float:
    """R = |mean exp(2 i phi_k)| (README section 2, T4)."""
    a = phase2(z, omega, vz)
    if len(a) == 0:
        return float("nan")
    return float(np.hypot(np.mean(np.cos(a)), np.mean(np.sin(a))))


def p_low(r_obs, r_mocks) -> tuple[float, int]:
    """p_boot with k = number of standing mocks with R <= R_obs."""
    r = np.asarray(r_mocks, float)
    k = int(np.sum(r <= r_obs))
    return p_boot(k, len(r)), k


def power_count(r_power, r_standing, p_thr=0.01) -> tuple[int, int]:
    """Number of power mocks whose p_boot against the standing mocks is below p_thr, and their number."""
    rs = np.sort(np.asarray(r_standing, float))
    k = np.searchsorted(rs, np.asarray(r_power, float), side="right")   # number of standing R <= R_j
    p = (1.0 + k) / (1.0 + len(rs))
    return int(np.sum(p < p_thr)), int(len(p))


def power(r_power, r_standing, p_thr=0.01) -> float:
    k, n = power_count(r_power, r_standing, p_thr)
    return k / n if n else float("nan")


# ---------------------------------------------------------------------------------------------
# T5: sinusoid fits and b-hat

def bhat(az, bz, av, bv) -> float:
    """sigma_min/sigma_max of [[az, bz], [av, bv]] times the sign of its determinant (= 2B - 1).

    Rows are (A cos psi, A sin psi) of each component."""
    M = np.array([[az, bz], [av, bv]], float)
    sv = np.linalg.svd(M, compute_uv=False)
    if sv[0] <= 0:
        return float("nan")
    det = az * bv - bz * av
    return float(sv[1] / sv[0] * (1.0 if det >= 0 else -1.0))


def _trig(k, lam, env):
    k = np.atleast_1d(np.asarray(k, float))
    th = 2.0 * math.pi * k[:, None] * lam[None, :]
    return env * np.sin(th), env * np.cos(th)


def _solve_sc(S, C, y, W):
    """Weighted LSQ of y ~ a S + b C for each row of S, C; returns a, b, chi2."""
    Wr = W[None, :]
    WS, WC = Wr * S, Wr * C
    sss, scc, ssc = (WS * S).sum(1), (WC * C).sum(1), (WS * C).sum(1)
    sys_, syc, syy = WS @ y, WC @ y, float((W * y * y).sum())
    det = sss * scc - ssc * ssc
    with np.errstate(invalid="ignore", divide="ignore"):
        a = (sys_ * scc - syc * ssc) / det
        b = (syc * sss - sys_ * ssc) / det
    chi = syy - (a * sys_ + b * syc)
    chi = np.where(np.isfinite(chi), chi, np.inf)
    return a, b, chi


def _refine(grid, tot, f, k_min, k_max, k_step):
    i = int(np.argmin(tot))
    lo, hi = max(k_min, grid[i] - k_step), min(k_max, grid[i] + k_step)
    k_best, f_best = float(grid[i]), float(tot[i])
    if hi > lo:
        r = minimize_scalar(f, bounds=(lo, hi), method="bounded", options={"xatol": 1e-5})
        if r.fun < f_best:
            k_best = float(r.x)
    return k_best


def fit_sinusoids(lam, env, comps, k_min=0.3, k_max=3.0, k_step=0.01, _grid_chis=None):
    """Weighted least squares of each component y_c ~ A_c env sin(2 pi k Lambda + psi_c).

    comps: list of (y, W) with W = weight / error^2. One shared k for all components in the list.
    k from a grid k_min..k_max (step k_step), refined by a bounded scalar search within one step.
    Returns k, at_bound, and per component (a, b) = (A cos psi, A sin psi), A >= 0, chi2."""
    grid = k_grid(k_min, k_max, k_step)
    if _grid_chis is None:
        S, C = _trig(grid, lam, env)
        _grid_chis = [_solve_sc(S, C, y, W)[2] for y, W in comps]
    tot = np.sum(_grid_chis, axis=0)

    def f(k):
        S1, C1 = _trig(k, lam, env)
        return float(sum(_solve_sc(S1, C1, y, W)[2][0] for y, W in comps))

    k_best = _refine(grid, tot, f, k_min, k_max, k_step)
    S1, C1 = _trig(k_best, lam, env)
    out = {"k": k_best, "at_bound": bool(abs(k_best - k_min) < 1e-4 or abs(k_best - k_max) < 1e-4),
           "comps": []}
    for y, W in comps:
        a, b, chi = _solve_sc(S1, C1, y, W)
        out["comps"].append({"a": float(a[0]), "b": float(b[0]), "chi2": float(chi[0]),
                             "A": float(math.hypot(a[0], b[0])), "psi": float(math.atan2(b[0], a[0]))})
    return out


def k_grid(k_min, k_max, k_step):
    return np.round(np.arange(k_min, k_max + 0.5 * k_step, k_step), 10)


def t5_fit(lam, env, yz, Wz, yv, Wv, k_range=(0.3, 3.0, 0.01)):
    """The free-k fit (k_z, k_vz) and the shared-k fit; b-hat, Delta, rho from the shared fit."""
    grid = k_grid(*k_range)
    S, C = _trig(grid, lam, env)
    chi_z, chi_v = _solve_sc(S, C, yz, Wz)[2], _solve_sc(S, C, yv, Wv)[2]
    fz = fit_sinusoids(lam, env, [(yz, Wz)], *k_range, _grid_chis=[chi_z])
    fv = fit_sinusoids(lam, env, [(yv, Wv)], *k_range, _grid_chis=[chi_v])
    sh = fit_sinusoids(lam, env, [(yz, Wz), (yv, Wv)], *k_range, _grid_chis=[chi_z, chi_v])
    cz, cv = sh["comps"]
    dpsi = math.atan2(math.sin(cv["psi"] - cz["psi"]), math.cos(cv["psi"] - cz["psi"]))
    return {"k_z": fz["k"], "k_vz": fv["k"], "k_ratio": fz["k"] / fv["k"],
            "k_z_at_bound": fz["at_bound"], "k_vz_at_bound": fv["at_bound"],
            "k_shared": sh["k"], "k_shared_at_bound": sh["at_bound"],
            "bhat": bhat(cz["a"], cz["b"], cv["a"], cv["b"]),
            "Delta": dpsi, "rho": cv["A"] / cz["A"] if cz["A"] > 0 else float("nan"),
            "A_z": cz["A"], "psi_z": cz["psi"], "A_v": cv["A"], "psi_v": cv["psi"]}


# ---------------------------------------------------------------------------------------------
# Intervals and their Monte Carlo errors

def interval(x, level=0.95):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if len(x) == 0:
        return None, None
    q = (1.0 - level) / 2.0
    return float(np.quantile(x, q)), float(np.quantile(x, 1.0 - q))


def quantile_mcse(x, q):
    """Order-statistic standard error of the q-quantile: half the spread of the quantiles at
    q +- sqrt(q(1-q)/n)."""
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    n = len(x)
    if n < 2:
        return None
    dq = math.sqrt(q * (1.0 - q) / n)
    return float(0.5 * (np.quantile(x, min(q + dq, 1.0)) - np.quantile(x, max(q - dq, 0.0))))


def percentiles(x):
    x = np.asarray(x, float)
    a, b, c = np.percentile(x, [16, 50, 84])
    return {"median": float(b), "p16": float(a), "p84": float(c), "plus": float(c - b), "minus": float(b - a)}
