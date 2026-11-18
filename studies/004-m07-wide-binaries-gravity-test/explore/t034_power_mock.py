"""T-034 power pre-computation on simulated data only (README section 2.1). No data access.

Keplerian mock of the scaled relative velocity v~ (thermal eccentricities, random phase and
orientation, 0.03 Gaussian noise per sky component), calibrated by f_cal (the geometric-mean ratio
of the 2026-11-16 bootstrap errors to the mock errors at the same counts). For each design, it gives
the noise-free ("Asimov") L under Newtonian and MOND truth and, with N_MC > 0, Monte Carlo rates
using the stratified bootstrap. `g1b()` is the pre-registered G1b evaluation (fixed f_cal, fresh
generator); `g2_rates()` simulates the symmetric G2 rule and the verdict rates (N_G2 > 0).

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
    "150pc_c25": [1180, 678, 483, 245, 143, 61],
    "shell_150_250pc": [771, 651, 517, 248, 154, 44],      # R5 minus the predicted d < 150 pc counts
}
F_CAL_FIXED = 1.227                                   # f_cal fixed by README 2.1 for G1b
N_G2, B_G2, SEED_G2 = 0, 1000, 20261121               # set N_G2 = 1000 to repeat the G2 table
N_SE, N_MC, B_MC, SEED_MC = 20000, 0, 1000, 20261118  # set N_MC = 1000 to repeat the MC table


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
    rng = np.random.default_rng(SEED_POOL)
    raw = kepler_vt(N_POOL, rng)
    A = float(np.median(raw))
    r2 = np.random.default_rng(SEED_MC)
    mock_rel = np.array([se_rel(raw, A, n, r2) for n in SEEN_COUNTS])
    f_cal = float(np.exp(np.mean(np.log((SEEN_ERR / SEEN_A) / mock_rel))))
    pool = A + f_cal * (raw - A)
    out = {"A_mock": A, "f_cal": f_cal,
           "check_seen_errors_L": float(wb.compare_models(SEEN_A * np.ones(5), np.array(SEEN_X),
                                                          np.diag(SEEN_ERR ** 2))["L"]),
           "check_old_design_L": asimov(pool, A, SEEN_COUNTS, SEEN_X, r2), "designs": {}}
    for name, c in DESIGNS.items():
        d = {"counts": c, "asimov": asimov(pool, A, c, X_R5, r2),
             "asimov_minus25pct": asimov(pool, A, [int(round(0.75 * n)) for n in c], X_R5, r2)}
        if N_G2:
            pool2, _ = calibrated_pool()
            d["g2"] = {t: g2_rates(pool2, c, X_R5, t, N_G2, B_G2, SEED_G2) for t in ("newton", "mond")}
        if N_MC:
            d["mc"] = {t: mc(pool, c, X_R5, t, r2, N_MC, B_MC) for t in ("newton", "mond")}
        out["designs"][name] = d
        ctx.log(f"{name}: Asimov L_N, L_M = {d['asimov']}; at -25% {d['asimov_minus25pct']}")
    ctx.save("t034_power", out)
    return out
