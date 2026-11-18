"""T-034 power pre-computation on simulated data only (README section 2.1). No data access.

Keplerian mock of the scaled relative velocity v~ (thermal eccentricities, random phase and
orientation, 0.03 Gaussian noise per sky component). Its scatter about the median is multiplied by
the fixed f_cal = 1.227 everywhere (main path, g1b(), Monte Carlo and G2). f_cal was derived once as
the geometric-mean ratio of the 2026-11-16 bootstrap errors to the mock errors at the same counts;
main() recomputes that ratio only as a check ("f_cal_check") and does not use it.

The default run regenerates every number of README section 2.1 (about 1 h on a laptop):
- noise-free ("Asimov") L under Newtonian and MOND truth for each design, and with counts -25%;
- the Monte Carlo rates for the R5 design (N_MC = 1000, B = 1000);
- the symmetric-G2 and verdict rates for R5 and R5 -25% (N_G2 = 1000, B = 1000).
Every computation starts from a fresh generator with a fixed seed: Asimov SEED_MC (the same as
g1b()), Monte Carlo SEED_MCRUN, G2 SEED_G2.

G1b: g1b_pipeline() takes the x values of the pairs that survive G1b step 1 (the cuts, done in
run.py) and performs steps 2-5. g1b_counts() covers steps 2-3 and g1b() steps 4-5.

Run: python -m astrolab explore 004 --tag t034-power --script explore/t034_power_mock.py
"""
import numpy as np

import wb

SEED_POOL, N_POOL, NOISE, ALPHA_E = 20261117, 2_000_000, 0.03, 1.0
SEEN_ERR = np.array([0.0274, 0.0306, 0.0529, 0.0381, 0.0931])     # 2026-11-16 bootstrap errors
SEEN_A, SEEN_COUNTS = 0.4988, [218, 232, 109, 56, 24]
SEEN_X = [0.167, 0.328, 0.707, 1.31, 2.7]
X_R5 = [0.063, 0.155, 0.328, 0.707, 1.31, 2.7]
DESIGNS = {                                           # predicted final counts per x bin (README 2.1)
    "130pc_relaxed": [543, 286, 232, 109, 56, 24],
    "200pc_relaxed": [1112, 672, 542, 251, 154, 56],
    "250pc_relaxed_R5": [1408, 988, 789, 375, 220, 72],
    "150pc_relaxed": [637, 337, 272, 127, 66, 28],
    "150pc_c25": [1180, 678, 483, 245, 143, 61],
    "shell_150_250pc": [771, 651, 517, 248, 154, 44],      # R5 minus the predicted d < 150 pc counts
}
F_CAL_FIXED = 1.227                                   # fixed by README 2.1 for every table and G1b
N_SE, SEED_MC = 20000, 20261118                       # Asimov: replicate medians per bin; seed (= g1b)
N_MC, B_MC, SEED_MCRUN = 1000, 1000, 20261120         # Monte Carlo table (R5 design)
N_G2, B_G2, SEED_G2 = 1000, 1000, 20261121            # G2 table (R5 and R5 -25%)
EDGES = [0.1057, 0.2307, 0.5088, 1.0275, 2.0902]


def kepler_vt(n, rng, alpha=ALPHA_E, noise=NOISE):
    e = rng.random(n) ** (1.0 / (alpha + 1.0))
    m = rng.random(n) * 2 * np.pi
    E = m.copy()
    for _ in range(60):
        E = E - (E - e * np.sin(E) - m) / (1 - e * np.cos(E))
    x, y = np.cos(E) - e, np.sqrt(1 - e ** 2) * np.sin(E)
    r = 1 - e * np.cos(E)
    vx, vy = -np.sin(E) / r, np.sqrt(1 - e ** 2) * np.cos(E) / r
    q = rng.normal(size=(n, 4))
    q /= np.linalg.norm(q, axis=1)[:, None]
    w, a, b, c = q.T
    R = np.array([[1 - 2 * (b * b + c * c), 2 * (a * b - c * w), 2 * (a * c + b * w)],
                  [2 * (a * b + c * w), 1 - 2 * (a * a + c * c), 2 * (b * c - a * w)]])
    P = np.einsum("ijn,jn->in", R[:, :2, :], np.stack([x, y]))
    V = np.einsum("ijn,jn->in", R[:, :2, :], np.stack([vx, vy]))
    rsky = np.hypot(P[0], P[1])
    s = np.sqrt(rsky)
    return np.hypot(V[0] * s + rng.normal(0, noise, n), V[1] * s + rng.normal(0, noise, n))


def se_rel(pool, A, n, rng, reps=N_SE):
    return float(np.std([np.median(pool[rng.integers(0, len(pool), n)]) for _ in range(reps)]) / A)


def asimov(pool, A, counts, xm, rng):
    s = np.array([se_rel(pool, A, int(np.floor(n + 0.5)), rng) for n in counts])
    xm = np.asarray(xm, float)
    b = wb.mond_boost(xm)
    LN = wb.compare_models(A * np.ones(len(xm)), xm, np.diag((A * s) ** 2))["L"]
    LM = wb.compare_models(A * b, xm, np.diag((A * s * b) ** 2))["L"]
    return float(LN), float(LM)


def mc(pool, counts, xm, truth, rng, R, B):
    xm = np.asarray(xm, float)
    b = wb.mond_boost(xm) if truth == "mond" else np.ones(len(xm))
    Ls = []
    for _ in range(R):
        vs = [pool[rng.integers(0, len(pool), n)] * bj for n, bj in zip(counts, b)]
        med = np.array([np.median(v) for v in vs])
        s = np.array([np.std(np.median(v[rng.integers(0, len(v), (B, len(v)))], axis=1), ddof=1) for v in vs])
        Ls.append(wb.compare_models(med, xm, np.diag(s ** 2))["L"])
    Ls = np.array(Ls)
    return {"median_L": float(np.median(Ls)), **{f"P(L>={t})": float(np.mean(Ls >= t)) for t in (10, 100)},
            **{f"P(L<={t})": float(np.mean(Ls <= t)) for t in (0.1, 0.01)}}


def calibrated_pool():
    raw = kepler_vt(N_POOL, np.random.default_rng(SEED_POOL))
    A = float(np.median(raw))
    return A + F_CAL_FIXED * (raw - A), A


G1B_FACTORS = np.array([0.969, 0.937, 0.953, 0.899, 0.809, 0.521])


def g1b_counts(raw_counts, min_count=15):
    """README 2.1 G1b steps 2-3: scale the six velocity-free bin counts by G1B_FACTORS, round to the
    nearest integer (halves up), then apply the 15-pair outer merge to the rounded counts.
    Returns (final counts, old-bin -> final-bin mapping, evaluable)."""
    scaled = np.floor(np.asarray(raw_counts, float) * G1B_FACTORS + 0.5).astype(int)
    mapping, evaluable = wb.merge_outer(scaled.tolist(), min_count)
    final = [int(sum(scaled[k] for k in range(len(scaled)) if mapping[k] == g)) for g in range(max(mapping) + 1)]
    return final, mapping, evaluable


def g1b(final_counts, x_medians):
    """README 2.1 G1b steps 4-5: (L_N*, L_M*, passes) for the final counts from g1b_counts() and the
    observed velocity-free x medians of the final bins; pool from SEED_POOL with f_cal = 1.227, one
    fresh generator SEED_MC, bins in increasing x."""
    pool, A = calibrated_pool()
    LN, LM = asimov(pool, A, final_counts, x_medians, np.random.default_rng(SEED_MC))
    return LN, LM, bool(LN >= 100 and LM <= 0.01)


def g1b_pipeline(x_pairs, edges=EDGES, min_count=15):
    """README 2.1 G1b steps 2-5, given the velocity-free x of every pair that survives step 1:
    raw counts per bin, scaling and rounding, the 15-pair merge, the observed median x of each final
    bin, then g1b(). Returns a dict with the counts, mapping, medians, L_N*, L_M* and the result."""
    x_pairs = np.asarray(x_pairs, float)
    b = wb.bin_index(x_pairs, edges)
    raw = [int(np.sum(b == k)) for k in range(len(edges) + 1)]
    final, mapping, evaluable = g1b_counts(raw, min_count)
    if not evaluable:
        return {"raw": raw, "final": final, "evaluable": False, "passes": False}
    fb = np.array([mapping[k] for k in b])
    xmed = [float(np.median(x_pairs[fb == g])) for g in range(len(final))]
    LN, LM, ok = g1b(final, xmed)
    return {"raw": raw, "final": final, "mapping": mapping, "x_medians": xmed, "L_N": LN, "L_M": LM,
            "evaluable": True, "passes": ok}


def g2_symmetric(med, s, x):
    """README 2.1 G2: relative errors r = s/m; Newton truth A_N with errors A_N r; MOND truth
    A_M b(x) with errors A_M b(x) r; A_N, A_M the GLS fits to the observed medians."""
    x = np.asarray(x, float)
    b = wb.mond_boost(x)
    f = wb.compare_models(med, x, np.diag(s ** 2))
    An, Am, r = f["A_newton"], f["A_mond"], s / med
    LN = wb.compare_models(An * np.ones(len(x)), x, np.diag((An * r) ** 2))["L"]
    LM = wb.compare_models(Am * b, x, np.diag((Am * b * r) ** 2))["L"]
    return f["L"], float(LN), float(LM), bool(LN >= 100 and LM <= 0.01)


def g2_rates(pool, counts, x, truth, R, B, seed):
    rng = np.random.default_rng(seed)
    x = np.asarray(x, float)
    bb = wb.mond_boost(x) if truth == "mond" else np.ones(len(x))
    L, ok = [], []
    for _ in range(R):
        vs = [pool[rng.integers(0, len(pool), n)] * bj for n, bj in zip(counts, bb)]
        med = np.array([np.median(v) for v in vs])
        s = np.array([np.std(np.median(v[rng.integers(0, len(v), (B, len(v)))], axis=1), ddof=1) for v in vs])
        l, _, _, g = g2_symmetric(med, s, x)
        L.append(l)
        ok.append(g)
    L, ok = np.array(L), np.array(ok)
    return {"P_G2_pass": float(ok.mean()), "P_pass_L>=100": float(np.mean(ok & (L >= 100))),
            "P_pass_L<=0.01": float(np.mean(ok & (L <= 0.01))),
            "P_pass_between": float(np.mean(ok & (L > 0.01) & (L < 100)))}


def main(ctx):
    pool, A = calibrated_pool()
    raw = A + (pool - A) / F_CAL_FIXED                  # the uncalibrated pool, for the f_cal check only
    rc = np.random.default_rng(SEED_MC)
    mock_rel = np.array([se_rel(raw, A, n, rc) for n in SEEN_COUNTS])
    out = {"A_mock": A, "f_cal_used": F_CAL_FIXED,
           "f_cal_check": float(np.exp(np.mean(np.log((SEEN_ERR / SEEN_A) / mock_rel)))),
           "check_seen_errors_L": float(wb.compare_models(SEEN_A * np.ones(5), np.array(SEEN_X),
                                                          np.diag(SEEN_ERR ** 2))["L"]),
           "check_old_design_L": asimov(pool, A, SEEN_COUNTS, SEEN_X, np.random.default_rng(SEED_MC)),
           "designs": {}}
    for name, c in DESIGNS.items():
        c75 = [int(np.floor(0.75 * n + 0.5)) for n in c]
        d = {"counts": c, "asimov": asimov(pool, A, c, X_R5, np.random.default_rng(SEED_MC)),
             "counts_minus25pct": c75,
             "asimov_minus25pct": asimov(pool, A, c75, X_R5, np.random.default_rng(SEED_MC))}
        if name == "250pc_relaxed_R5":
            if N_MC:
                d["mc"] = {t: mc(pool, c, X_R5, t, np.random.default_rng(SEED_MCRUN), N_MC, B_MC)
                           for t in ("newton", "mond")}
            if N_G2:
                d["g2"] = {t: g2_rates(pool, c, X_R5, t, N_G2, B_G2, SEED_G2) for t in ("newton", "mond")}
                d["g2_minus25pct"] = {t: g2_rates(pool, c75, X_R5, t, N_G2, B_G2, SEED_G2)
                                      for t in ("newton", "mond")}
        out["designs"][name] = d
        ctx.log(f"{name}: Asimov L_N, L_M = {d['asimov']}; at -25% {d['asimov_minus25pct']}")
    ctx.save("t034_power", out)
    return out
