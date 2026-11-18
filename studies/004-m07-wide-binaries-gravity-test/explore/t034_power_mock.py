"""T-034 power pre-computation on simulated data only (README section 2.1). No data access.

Keplerian mock of the scaled relative velocity v~ (thermal eccentricities, random phase and
orientation, 0.03 Gaussian noise per sky component), calibrated by f_cal (the geometric-mean ratio
of the 2026-11-16 bootstrap errors to the mock errors at the same counts). For each design, it gives
the noise-free ("Asimov") L under Newtonian and MOND truth and, with N_MC > 0, Monte Carlo rates
using the stratified bootstrap.

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
}
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
    s = np.array([se_rel(pool, A, int(n), rng) for n in counts])
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
        if N_MC:
            d["mc"] = {t: mc(pool, c, X_R5, t, r2, N_MC, B_MC) for t in ("newton", "mond")}
        out["designs"][name] = d
        ctx.log(f"{name}: Asimov L_N, L_M = {d['asimov']}; at -25% {d['asimov_minus25pct']}")
    ctx.save("t034_power", out)
    return out
