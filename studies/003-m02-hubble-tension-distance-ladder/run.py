"""M2: Hubble tension, SH0ES distance ladder and host selection (pre-registration: README 1-4).

Run with:      python -m astrolab run 003-m02-hubble-tension-distance-ladder
Explore with:  python -m astrolab explore 003-m02-hubble-tension-distance-ladder --tag <topic> --set KEY=VALUE

R1  GLS of the public SH0ES y, L, C (Riess et al. 2022, Eq. 6) against the authors' lstsq_results.txt.
R2  Anchor step (all anchors -> NGC 4258 only) and host step (37 hosts -> the 10 CCHP hosts), in
    5 log H0 with exact variances a^T C a; the host step is the test of arXiv:2408.11770.
R3  Same 10 hosts: SH0ES Cepheid ladder vs CCHP JWST TRGB distances (descriptive).
R4  Random 10-host subsets (descriptive).
Cross-paper comparison of published H0 values (descriptive).
"""
import hashlib
import json
import time
from pathlib import Path

import numpy as np
from scipy import linalg, optimize

from astrolab import infer

import n5584
import onehost
import rob
import sel
import shape

# Tunable knobs (AGENTS.md section 2). Read inside main() and passed on as arguments.
PARAMS = {
    "cchp_hosts": ["M101", "N1365", "N2442", "N3972", "N4038", "N4424", "N4536", "N4639",
                   "N5643", "N7250"],
    "r4_draws": 10000,
    "r4_seed": 0,
    "r4_max_minutes": 60.0,
    "sn_match_tol": 0.15,       # mag, check (ii)
    "trgb_tip_sys": 0.025,      # mag, NGC 4258 TRGB tip measurement (CCHP section X)
    # pre-registered tolerances (README section 2)
    "tol_r1": 1e-3,
    "anchor_target": -0.0158, "anchor_tol": 0.005,
    "anchor_sigma_target": 0.0461, "anchor_sigma_frac": 0.15,
    "host_ref": -0.0405, "host_ref_extra": 0.02,
    "cchp_target_5logh0": 9.2034, "cchp_match_tol": 0.02,
    # R2-RE (README section 2, addendum 2026-11-16): host-level random effect, REML
    "re_check": True, "re_tau_max": 0.5, "re_grid_step": 0.01,
    # R2-RE-ROB (README section 2, addendum 2026-11-17, T-032)
    "rob_check": True, "rob_n_tau": 400, "rob_n_spread": 2000, "rob_n_subsets": 1000,
    "rob_seed_base": 10_000, "rob_max_failed": 20,
    # R2-RE-N5584 (README section 2, addendum 2026-11-18, T-039): (a) removal, (b) Student-t host effect
    "n5584_check": True, "n5584_host": "N5584",
    "t_nu": 4, "t_nu_sens": [2, 10], "t_maxiter": 10000, "t_tol": 1e-8, "t_starts": [0.077, 0.20],
    # R2-RE-SEL (README section 2, addendum 2026-11-19, T-042): selection-aware null for dropping N5584
    "sel_check": True, "sel_seed_base": 20_000, "sel_n_tau": 400, "sel_n_spread": 2000,
    "sel_n_subsets": 1000, "sel_max_failed": 20,
    # R2-RE-D (README section 2, addendum 2026-11-21, T-048): one outlying host or diffuse host scatter.
    # d_only: standalone mode (only this block; writes r2_re_d*.json and summary.json's R2_RE_D key)
    "d_check": True, "d_seed_base": 100_000, "d_n_sims": 10_000, "d_taus": [0.05, 0.077, 0.105],
    "d_host_seed_base": 200_000, "d_kde_boot": 200, "d_only": False,
    # R2-RE-G (README section 2, addendum 2026-11-21, T-055): composite shape test of one offset host against
    # diffuse host scatter. g_check stays false until the formal stages (README amendment 2026-11-21); g_only:
    # standalone mode; g_stage "power" (writes only r2_re_g_power.json) then "full" (README section 8)
    "g_check": False, "g_seed_base": 400_000, "g_host_seed_base": 500_000, "g_inner_seed": 600_000,
    "g_n_sims": 10_000, "g_n_inner": 20_000, "g_power_min": 0.8, "g_z_curve": [2.5, 3.0, 4.0, 4.5, 5.0],
    "g_taus_rep": [0.05, 0.105], "g_max_minutes": 120, "g_min_sims": 5_000, "g_only": False, "g_stage": "full",
    "g_rerun_reason": "",       # a g_only full stage after a formal outcome needs a reason, also present in log.md
    # R2-RE-GT (README section 2, addendum 2026-11-21, T-057): the shape test G against heavy-tailed (Student-t)
    # diffuse host scatter. gt_check stays false until the formal stages; gt_only: standalone mode; gt_stage
    # "power" (writes only r2_re_gt_power.json) then "full" (README section 8). Reuses g_seed_base (eps_s),
    # g_host_seed_base (O_any's host), g_inner_seed (E_in) and g_taus_rep (T050, T105, the fixed-tau sensitivities)
    "gt_check": False, "gt_only": False, "gt_stage": "full", "gt_seed_base": 410_000, "gt_inner_seed": 610_000,
    "gt_inner_seeds_rep": [611_000, 612_000], "gt_nu": 4, "gt_nu_rep": [3, 10], "gt_n_sims": 10_000,
    "gt_n_inner": 20_000, "gt_power_min": 0.8, "gt_max_minutes": 120, "gt_min_sims": 5_000,
    "gt_rerun_reason": "",      # a gt_only full stage after a formal outcome needs a reason, also present in log.md
    # R2-RE-GTP (README section 2, addendum 2026-11-22, T-060): a reported, non-decisive profile of R2-RE-GT over nu
    # and tau; runs only standalone (gtp_check and gtp_only true for the formal run, back to false afterwards).
    # Reuses gt_* (nu = 4, the inner seeds of nu = 3 and 10) and g_* (eps_s, E_in) from R2-RE-GT and R2-RE-G
    "gtp_check": False, "gtp_only": False, "gtp_nus": [3, 4, 6, 10, 30, "inf"],
    "gtp_t_seeds": {3: 430_000, 6: 440_000, 10: 450_000, 30: 460_000},
    "gtp_inner_seeds": {6: 613_000, 30: 614_000}, "gtp_n_sims": 10_000,
    "gtp_rerun_reason": "",     # a formal rerun after a formal outcome needs a reason, also present in log.md
}

DR = "PantheonPlusSH0ES/DataRelease/main/SH0ES_Data/"
RAW = "https://raw.githubusercontent.com/" + DR
MEDIA = "https://media.githubusercontent.com/media/" + DR
F_C = "allc_shoes_ceph_topantheonwt6.0_112221.fits"
F_L = "alll_shoes_ceph_topantheonwt6.0_112221.fits"
F_Y = "ally_shoes_ceph_topantheonwt6.0_112221.fits"
F_Q = "lstsq_results.txt"
C_BYTES = 48_781_440
C_SHA256 = "a42778672d25df7a559bd2949b1e412b99b2e35dd9a36895f6b38828be019172"
N_ROWS, N_PAR = 3492, 47

# parameter columns (README section 4)
NH = 37
C_N4258, C_MH, C_LMC, C_M31, C_BW, C_MB, C_ZW, C_X, C_ZP, C_H0 = range(37, 47)
PAR_NAMES = None  # filled in main from HOSTS
N5584_COLUMN = 26  # N5584's column under the amended host labelling (host_identification.json)

# R22 Table 6 (arXiv:2112.04510, PDF p. 30): host, SN, m0_B, sigma, mu_Ceph(a), sigma(a)
TABLE6 = [
    ("M101", "2011fe", 9.7800, 0.115, 29.193, 0.039),
    ("M1337", "2006D", 13.655, 0.106, 32.922, 0.124),
    ("N0105", "2007A", 15.250, 0.133, 34.531, 0.253),
    ("N0691", "2005W", 13.602, 0.139, 32.846, 0.109),
    ("N0976", "1999dq", 14.250, 0.103, 33.719, 0.151),
    ("N1015", "2009ig", 13.350, 0.094, 32.570, 0.075),
    ("N1309", "2002fk", 13.209, 0.082, 32.546, 0.060),
    ("N1365", "2012fr", 11.900, 0.092, 31.379, 0.057),
    ("N1448", "2001el", 12.254, 0.136, 31.290, 0.037),
    ("N1448", "2021pit", 11.752, 0.200, 31.290, 0.037),
    ("N1559", "2005df", 12.141, 0.086, 31.501, 0.062),
    ("N2442", "2015F", 12.234, 0.082, 31.457, 0.065),
    ("N2525", "2018gv", 12.728, 0.074, 32.067, 0.100),
    ("N2608", "2001bg", 13.443, 0.166, 32.629, 0.155),
    ("N3021", "1995al", 13.114, 0.116, 32.474, 0.160),
    ("N3147", "2021hpr", 13.843, 0.159, 33.044, 0.165),
    ("N3147", "1997bq", 13.821, 0.141, 33.044, 0.165),
    ("N3147", "2008fv", 13.936, 0.200, 33.044, 0.165),
    ("N3254", "2019np", 13.201, 0.074, 32.332, 0.077),
    ("N3370", "1994ae", 12.937, 0.082, 32.123, 0.052),
    ("N3447", "2012ht", 12.736, 0.089, 31.939, 0.035),
    ("N3583", "ASASSN-15so", 13.509, 0.093, 32.808, 0.081),
    ("N3972", "2011by", 12.548, 0.094, 31.644, 0.090),
    ("N3982", "1998aq", 12.252, 0.078, 31.724, 0.072),
    ("N4038", "2007sr", 12.409, 0.106, 31.615, 0.117),
    ("N4424", "2012cg", 11.487, 0.192, 30.856, 0.130),
    ("N4536", "1981B", 11.551, 0.133, 30.838, 0.051),
    ("N4639", "1990N", 12.454, 0.124, 31.818, 0.085),
    ("N4680", "1997bp", 13.173, 0.205, 32.606, 0.208),
    ("N5468", "1999cp", 13.880, 0.080, 33.120, 0.075),
    ("N5468", "2002cr", 13.993, 0.072, 33.120, 0.075),
    ("N5584", "2007af", 12.804, 0.079, 31.775, 0.053),
    ("N5643", "2013aa", 11.252, 0.079, 30.569, 0.050),
    ("N5643", "2017cbv", 11.208, 0.074, 30.569, 0.050),
    ("N5728", "2009Y", 13.514, 0.115, 33.116, 0.207),
    ("N5861", "2017erp", 12.945, 0.107, 32.232, 0.101),
    ("N5917", "2005cf", 13.079, 0.095, 32.363, 0.122),
    ("N7250", "2013dy", 12.283, 0.178, 31.628, 0.126),
    ("N7329", "2006bh", 14.030, 0.079, 33.274, 0.116),
    ("N7541", "1998dh", 13.418, 0.128, 32.504, 0.121),
    ("N7678", "2002dp", 14.090, 0.093, 33.196, 0.155),
    ("U9391", "2003du", 13.525, 0.084, 32.849, 0.068),
]
# R22 Table 3 (PDF p. 22, read from the rendered table), Cepheids in the fit per SN host.
# The column sums to 2149; the printed "SN Total" 2150 is inconsistent with it, while
# 2149 + 443 + 55 + 339 + 143 = 3129 matches the printed "Total All".
TABLE3_FIT = {
    "M101": 259, "M1337": 15, "N0105": 8, "N0691": 28, "N0976": 33, "N1015": 18,
    "N1309": 53, "N1365": 45, "N1448": 73, "N1559": 110, "N2442": 177, "N2525": 73,
    "N2608": 22, "N3021": 16, "N3147": 27, "N3254": 48, "N3370": 73, "N3447": 101,
    "N3583": 54, "N3972": 52, "N3982": 27, "N4038": 29, "N4424": 9, "N4536": 40,
    "N4639": 30, "N4680": 11, "N5468": 93, "N5584": 165, "N5643": 251, "N5728": 20,
    "N5861": 41, "N5917": 14, "N7250": 21, "N7329": 31, "N7541": 33, "N7678": 16,
    "U9391": 33,
}
TABLE3_SUM = 2149
# CCHP Table 2 (arXiv:2408.06153 v3): JWST TRGB distance modulus and sigma_T per host
CCHP_TRGB = {
    "M101": (29.151, 0.042), "N1365": (31.366, 0.069), "N2442": (31.646, 0.097),
    "N3972": (31.747, 0.068), "N4038": (31.645, 0.078), "N4424": (30.926, 0.030),
    "N4536": (30.923, 0.052), "N4639": (31.774, 0.073), "N5643": (30.643, 0.071),
    "N7250": (31.629, 0.047),
}
CCHP_CSP_H0 = 68.81
# Published H0 values for the cross-paper comparison (plan 012, section 2): value, -err, +err
PUBLISHED = [
    {"name": "SH0ES R22 baseline", "arxiv": "2112.04510", "h0": 73.04, "lo": 1.04, "hi": 1.04, "group": "ladder"},
    {"name": "SH0ES + JWST (Riess et al. 2024), full HST sample", "arxiv": "2408.11770", "h0": 73.17, "lo": 0.86, "hi": 0.86, "group": "ladder"},
    {"name": "H0DN local distance network", "arxiv": "2510.23823", "h0": 73.50, "lo": 0.81, "hi": 0.81, "group": "ladder"},
    {"name": "CCHP TRGB (24 calibrators)", "arxiv": "2408.06153", "h0": 70.39, "lo": 1.94, "hi": 1.94, "group": "ladder",
     "note": "1.22 stat, 1.33 sys, 0.70 sigma_SN in quadrature"},
    {"name": "TDCOSMO 2025 (flat LCDM)", "arxiv": "2506.03023", "h0": 71.6, "lo": 3.3, "hi": 3.9, "group": "lensing"},
    {"name": "Planck 2018", "arxiv": "1807.06209", "h0": 67.4, "lo": 0.5, "hi": 0.5, "group": "cmb"},
    {"name": "SPT-3G + ACT + Planck (CMB only)", "arxiv": "2506.20707", "h0": 67.19, "lo": 0.38, "hi": 0.38, "group": "cmb"},
]


# ---------------------------------------------------------------- data
def _fetch_fits(ctx, name, label):
    path = ctx.http(RAW + name, label=label)
    head = path.read_bytes()[:64]
    if head.startswith(b"version https://git-lfs"):
        ctx.log(f"{name}: raw URL returned an LFS pointer; fetching the media URL")
        path = ctx.http(MEDIA + name, label=label + " (LFS)")
    return path


def _read_fits(path):
    from astropy.io import fits
    with fits.open(path, memmap=False) as hdul:
        for hdu in hdul:
            if hdu.data is not None:
                return np.asarray(hdu.data, dtype=np.float64)
    raise ValueError(f"no data in {path}")


def load(ctx):
    cpath = ctx.http(MEDIA + F_C, label="SH0ES C (LFS)")
    size = cpath.stat().st_size
    sha = hashlib.sha256(cpath.read_bytes()).hexdigest()
    if size != C_BYTES or sha != C_SHA256:
        raise RuntimeError(f"C download failed checks: {size} bytes, sha256 {sha}")
    C = _read_fits(cpath)
    L = _read_fits(_fetch_fits(ctx, F_L, "SH0ES L"))
    y = _read_fits(_fetch_fits(ctx, F_Y, "SH0ES y")).ravel()
    if L.shape == (N_PAR, N_ROWS):
        L = L.T
    if C.shape != (N_ROWS, N_ROWS) or L.shape != (N_ROWS, N_PAR) or y.shape != (N_ROWS,):
        raise RuntimeError(f"unexpected shapes C {C.shape}, L {L.shape}, y {y.shape}")
    qtxt = ctx.http(RAW + F_Q, label="SH0ES lstsq_results").read_text(encoding="utf-8")
    rows = []
    for line in qtxt.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            try:
                rows.append((float(parts[0]), float(parts[1])))
            except ValueError:
                continue
    lsq = np.array(rows)
    if lsq.shape != (N_PAR, 2):
        raise RuntimeError(f"lstsq_results.txt has {lsq.shape[0]} numeric rows, expected {N_PAR}")
    return C, L, y, lsq


# ---------------------------------------------------------------- structure
def row_classes(L, y):
    nz = L != 0.0
    nhost = nz[:, :NH].sum(axis=1)
    single = nz.sum(axis=1) == 1
    calib = nz[:, C_MB] & (nhost == 1)
    hflow = nz[:, C_MB] & nz[:, C_H0] & (nhost == 0)
    ceph = nz[:, C_MH] & ~nz[:, C_MB] & ~single
    cls = {
        "calib": calib, "hflow": hflow, "single": single, "ceph": ceph,
        "ceph_host": ceph & (nhost == 1),
        "maser": single & nz[:, C_N4258], "lmc": single & nz[:, C_LMC],
        "mw": single & nz[:, C_MH], "zp": single & nz[:, C_ZP],
    }
    known = calib | hflow | single | ceph
    counts = {k: int(v.sum()) for k, v in cls.items()}
    counts["other"] = int((~known).sum())
    counts["total"] = int(len(y))
    return nz, cls, counts


def anchor_rows(nz, cls, y):
    """Rows of the NGC 4258-only system (README section 4) and its structural checks."""
    lmc, mw, maser = np.flatnonzero(cls["lmc"]), np.flatnonzero(cls["mw"]), np.flatnonzero(cls["maser"])
    checks = {
        "lmc_rows": lmc.tolist(), "mw_rows": mw.tolist(), "maser_rows": maser.tolist(),
        "lmc_ok": len(lmc) == 1 and all(abs(y[i]) < 1e-9 for i in lmc),
        "mw_ok": len(mw) == 2 and all(abs(y[i] + 5.85) <= 0.2 for i in mw),
        "maser_ok": len(maser) == 1 and all(abs(y[i]) < 1e-9 for i in maser),
        "mw_y": [float(y[i]) for i in mw],
    }
    checks["ok"] = bool(checks["lmc_ok"] and checks["mw_ok"] and checks["maser_ok"])
    keep = np.ones(len(y), bool)
    keep[lmc] = False
    keep[mw] = False
    return np.flatnonzero(keep), checks


def host_compat(nz, cls, y, mu_fit, hosts, tol, mean_mode=False):
    """Compatibility matrix compat[j, h]: column j passes checks (ii)-(iv) for host label h.

    mean_mode (amendment, README dated note): check (ii) compares the mean of the column's SN
    rows with the mean of the host's Table 6 m0_B (Table 6 note d: a simple average over surveys).
    """
    sn = {}
    for h, s, mb, smb, mua, sa in TABLE6:
        sn.setdefault(h, {"mb": [], "mua": mua, "sa": sa})["mb"].append(mb)
    calib = cls["calib"]
    ncep = np.array([int((cls["ceph_host"] & nz[:, j]).sum()) for j in range(NH)])
    rows_y = [y[calib & nz[:, j]] for j in range(NH)]
    comp = np.zeros((NH, NH), bool)
    detail = {"ii": np.zeros((NH, NH), bool), "iii": np.zeros((NH, NH), bool),
              "iv": np.zeros((NH, NH), bool)}
    for j in range(NH):
        for k, h in enumerate(hosts):
            mbs = np.array(sn[h]["mb"])
            ry = rows_y[j]
            if mean_mode:
                ii = len(ry) > 0 and abs(float(np.mean(ry)) - float(np.mean(mbs))) <= tol
            else:
                ii = (len(ry) > 0 and all(np.min(np.abs(mbs - v)) <= tol for v in ry)
                      and all(np.min(np.abs(ry - m)) <= tol for m in mbs))
            iii = abs(mu_fit[j] - sn[h]["mua"]) <= 3 * sn[h]["sa"] + 0.02
            iv = abs(ncep[j] - TABLE3_FIT[h]) <= 2
            detail["ii"][j, k], detail["iii"][j, k], detail["iv"][j, k] = ii, iii, iv
            comp[j, k] = ii and iii and iv
    return comp, detail, ncep, rows_y, sn


def assignment_alternatives(comp):
    """Every compatible off-diagonal edge that belongs to another perfect matching (any cycle)."""
    alts = []
    cost0 = np.where(comp, 0.0, 1.0)
    for j, h in zip(*np.nonzero(comp & ~np.eye(len(comp), dtype=bool))):
        cost = cost0.copy()
        cost[j, :] = 1.0
        cost[:, h] = 1.0
        cost[j, h] = 0.0
        r, c = optimize.linear_sum_assignment(cost)
        if cost[r, c].sum() == 0:
            perm = np.empty(len(comp), int)
            perm[r] = c
            alts.append({"col": int(j), "label": int(h), "perm": perm.tolist()})
    return alts


# ---------------------------------------------------------------- estimators
def fit(L, y, C, rows, est=False):
    idx = np.asarray(rows)
    return infer.gls(L[idx], y[idx], C[np.ix_(idx, idx)], return_estimator=est)


def kpos(res, col):
    kept = res["kept"]
    i = int(np.searchsorted(kept, col))
    if i >= len(kept) or kept[i] != col:
        raise RuntimeError(f"column {col} not fitted")
    return i


def shift_vector(res_sub, rows_sub, res_full, rows_full, col=C_H0):
    a = np.zeros(N_ROWS)
    a[rows_sub] += res_sub["A"][kpos(res_sub, col)]
    a[rows_full] -= res_full["A"][kpos(res_full, col)]
    return a


# ---------------------------------------------------------------- R4 (README section 2)
def r4_draws(L, y, C, rows_a, res_a, qa, sa, base_rows, host_rows, host_cols, n_pick, draws, seed,
             max_minutes, n_sn_col, out, log, name="R4"):
    """R4's draw loop with its runtime guard: `draws` subsets of `n_pick` hosts drawn with
    default_rng(seed).choice(len(host_cols), n_pick, replace=False), indexing `host_cols` in order
    (R4: all 37 columns, so the index is the column; R4-N: the 36 columns without N5584). Each subset
    is refitted under C and compared with the reference fit `res_a` on `rows_a` (5 log H0 qa, sigma
    sa). Writes z_identity_check, seconds_per_draw, draws_reduced_from and a runtime status into
    `out`; returns deltas, nsns, zs, picks (picks hold column indices)."""
    rng = np.random.default_rng(seed)
    cols = np.asarray(host_cols, dtype=np.int64)   # the dtype of rng.choice, as in the original loop
    deltas, nsns, zs, picks = [], [], [], []
    t1 = time.perf_counter()
    i = 0
    while i < draws:
        pick = cols[rng.choice(len(cols), size=n_pick, replace=False)]
        picks.append(pick)
        rows = np.union1d(base_rows, np.concatenate([host_rows[j] for j in pick]))
        res = fit(L, y, C, rows, est=(i == 0))
        deltas.append(float(res["q"][C_H0]) - qa)
        # nested GLS with the same C: the full fit is efficient (BLUE) for a superset of the
        # data, so Cov(full, sub) = Var(full) and Var(sub - full) = sigma_sub^2 - sigma_full^2
        # (Hausman-type identity; checked exactly on R2's host step and on the first draw here)
        if i == 0:
            a1 = shift_vector(res, rows, res_a, rows_a)
            exact = float(a1 @ C @ a1)
            nested = float(res["sigma"][C_H0]) ** 2 - sa ** 2
            out["z_identity_check"] = {"exact_aCa": exact, "nested": nested,
                                       "rel_diff": abs(exact - nested) / exact}
            if abs(exact - nested) > 1e-6 * exact:
                raise RuntimeError(f"nested-variance identity failed: {exact} vs {nested}")
        zs.append(deltas[-1] / np.sqrt(max(float(res["sigma"][C_H0]) ** 2 - sa ** 2, 1e-30)))
        nsns.append(int(sum(n_sn_col[j] for j in pick)))
        i += 1
        if i == 100:
            per = (time.perf_counter() - t1) / 100
            proj = per * draws / 60
            out["seconds_per_draw"] = per
            if proj > max_minutes:
                new = int(max_minutes * 60 / per) // 1000 * 1000
                if new < 2000:
                    out["status"] = "not evaluated (runtime)"
                    deltas, nsns, zs, picks = [], [], [], []
                    break
                out["draws_reduced_from"] = draws
                draws = new
                log(f"{name}: projected {proj:.0f} min; draws reduced to {draws}")
    return deltas, nsns, zs, picks


def r4_summary(deltas, zs, nsns, d_h, z):
    """R4's reported numbers and its pre-registered 5/95 percentile rule for the CCHP shift d_h."""
    dl = np.array(deltas)
    pct = float(100.0 * np.mean(dl <= d_h))
    if pct < 5:
        rv = "the selection itself is systematically low"
    elif pct > 95:
        rv = "the selection itself is systematically high"
    else:
        rv = "consistent with random-subset fluctuations"
    qs_ = np.percentile(dl, [2.5, 5, 16, 50, 84, 95, 97.5])
    hist, edges = np.histogram(dl, bins=60)
    return {"draws": len(dl), "cchp_shift": d_h, "percentile": pct, "verdict": rv,
            "quantiles": dict(zip(["p2.5", "p5", "p16", "p50", "p84", "p95", "p97.5"],
                                  [float(x) for x in qs_])),
            "mean": float(dl.mean()), "std": float(dl.std()),
            "hist_counts": hist.tolist(), "hist_edges": [float(e) for e in edges],
            "n_sn_mean": float(np.mean(nsns)),
            # added after the first results (gate-1 review; descriptive): each draw's
            # shift in units of its own C-propagated sigma, and where the CCHP z sits
            "z_quantiles": dict(zip(["p2.5", "p5", "p16", "p50", "p84", "p95", "p97.5"],
                                    [float(x) for x in np.percentile(zs, [2.5, 5, 16, 50, 84, 95, 97.5])])),
            "z_std": float(np.std(zs)), "cchp_z": z,
            "z_percentile": float(100.0 * np.mean(np.array(zs) <= z)),
            "shift_by_n_sn": {str(n): float(np.mean(dl[np.array(nsns) == n]))
                              for n in sorted(set(nsns))}}


# ---------------------------------------------------------------- R2-RE (addendum 2026-11-16)
_FIT_FAILURES = ("is not positive definite", "rank deficient")


def is_fit_failure(exc):
    """The pre-registered 'not evaluable (fit)' cases: V not positive definite or a rank-deficient
    normal matrix (numpy LinAlgError, or infer.gls's ValueError for those two cases). Any other
    error is a bug and propagates."""
    return isinstance(exc, np.linalg.LinAlgError) or (
        isinstance(exc, ValueError) and any(m in str(exc) for m in _FIT_FAILURES))


def with_re(C, groups, tau):
    """V = C + tau^2 sum_j h_j h_j^T (h_j: indicator of the row indices in groups[j])."""
    V = C.copy()
    if tau > 0:
        t2 = tau * tau
        for idx in groups:
            V[np.ix_(idx, idx)] += t2
    return V


def reml_m2l(L, y, C, rows, groups, tau):
    """-2 x restricted log-likelihood (up to a constant) of the GLS model on `rows` with
    V(tau) = C + tau^2 sum_j h_j h_j^T; groups hold row indices into the full system."""
    idx = np.asarray(rows)
    pos = {r: k for k, r in enumerate(idx)}
    V = C[np.ix_(idx, idx)].copy()
    if tau > 0:
        for g in groups:
            k = np.array([pos[r] for r in g if r in pos])
            if k.size:
                V[np.ix_(k, k)] += tau * tau
    X = L[idx]
    X = X[:, np.any(X != 0.0, axis=0)]
    cf = linalg.cho_factor(V, lower=True)
    logdet_v = 2.0 * np.sum(np.log(np.diag(cf[0])))
    vix = linalg.cho_solve(cf, X)
    viy = linalg.cho_solve(cf, y[idx])
    F = X.T @ vix
    cfF = linalg.cho_factor(F, lower=True)
    logdet_f = 2.0 * np.sum(np.log(np.diag(cfF[0])))
    q = linalg.cho_solve(cfF, X.T @ viy)
    r = y[idx] - X @ q
    return float(logdet_v + logdet_f + r @ linalg.cho_solve(cf, r))


def reml_tau(f, tau_max, step, interval=True):
    """Grid then bounded refinement around the grid's global minimum; 68% interval from the
    crossing of min + 1 nearest to tau_hat on each side (README section 2, R2-RE)."""
    grid = np.round(np.arange(0.0, tau_max + step / 2, step), 10)
    vals = np.array([f(t) for t in grid])
    k = int(np.argmin(vals))
    local = [float(grid[i]) for i in range(len(grid)) if i != k
             and (i == 0 or vals[i] < vals[i - 1]) and (i == len(grid) - 1 or vals[i] < vals[i + 1])]
    lo, hi = grid[max(k - 1, 0)], grid[min(k + 1, len(grid) - 1)]
    tau_hat, f_hat, refined, refine_error = float(grid[k]), float(vals[k]), False, None
    try:
        r = optimize.minimize_scalar(f, bounds=(lo, hi), method="bounded", options={"xatol": 1e-5})
        if r.success and r.fun < f_hat:
            tau_hat, f_hat, refined = float(r.x), float(r.fun), True
        elif not r.success:
            refine_error = f"not converged: {r.message}"
    except np.linalg.LinAlgError as e:   # numerical failure: keep the grid minimum (pre-registered);
        refine_error = f"{type(e).__name__}: {e}"   # anything else is a bug and propagates

    def crossing(direction):
        """Nearest crossing of min + 1 on one side of tau_hat: scan the grid points beyond tau_hat
        outward to the first one at or above the threshold; brentq between it and the previous
        point on that side (tau_hat itself when there is none in between)."""
        g = lambda t: f(t) - f_hat - 1.0
        side = [i for i in range(len(grid)) if (grid[i] - tau_hat) * direction > 0]
        side.sort(key=lambda i: abs(grid[i] - tau_hat))
        inner = tau_hat
        for i in side:
            if vals[i] - f_hat - 1.0 >= 0:
                a, b = sorted((inner, float(grid[i])))
                ga, gb = g(a), g(b)          # errors from the objective itself propagate
                if ga == 0.0 or gb == 0.0:
                    return a if ga == 0.0 else b
                if np.sign(ga) == np.sign(gb):
                    return "not determined"            # no sign change in the bracket
                root, info = optimize.brentq(g, a, b, xtol=1e-6, full_output=True, disp=False)
                return float(root) if info.converged else "not determined"
            inner = float(grid[i])
        return 0.0 if direction < 0 else "> %.1f" % tau_max

    if not interval:                     # R2-RE-ROB: tau_hat only (README addendum 2026-11-17)
        return {"tau_hat": tau_hat, "m2l_min": f_hat, "refined": refined, "refine_error": refine_error,
                "other_local_minima": local, "at_zero": tau_hat < 1e-3,
                "at_upper_bound": tau_hat > tau_max - 1e-3}
    ends = [crossing(-1), crossing(+1)]
    return {"tau_hat": tau_hat, "m2l_min": f_hat, "refined": refined, "refine_error": refine_error,
            "m2l_at_interval": [float(f(e)) if isinstance(e, float) else None for e in ends],
            "grid": [float(t) for t in grid], "grid_m2l": [float(v) for v in vals],
            "other_local_minima": local, "interval_68": ends,
            "at_zero": tau_hat < 1e-3, "at_upper_bound": tau_hat > tau_max - 1e-3}


def host_step_verdict(z, d_h, s_h, ref, extra):
    """R2's pre-registered verdict table (README section 2)."""
    if z <= -2 and abs(d_h - ref) <= 2 * s_h + extra:
        return "host selection significantly lowers H0, by the size the paper reports (supports the paper)"
    if z <= -2:
        return "host selection significantly lowers H0, but by a different size"
    if abs(z) < 2:
        return "no host-selection effect detected in these data (does not support the paper's quantitative claim)"
    return "host selection raises H0 (contradicts the paper)"


def host_step_under(L, y, V, rows_a, rows_s):
    """R2's host step with covariance V; exact shift variance a^T V a and the nested identity."""
    res_a = fit(L, y, V, rows_a, est=True)
    res_s = fit(L, y, V, rows_s, est=True)
    d_h = float(res_s["q"][C_H0] - res_a["q"][C_H0])
    a = shift_vector(res_s, rows_s, res_a, rows_a)
    var = float(a @ V @ a)
    nested = float(res_s["sigma"][C_H0] ** 2 - res_a["sigma"][C_H0] ** 2)
    if abs(var - nested) > 1e-6 * var:
        raise RuntimeError(f"nested-variance identity failed under V: {var} vs {nested}")
    s_h = float(np.sqrt(var))
    return {"shift": d_h, "shift_sigma": s_h, "z": d_h / s_h, "nested_var_check": nested,
            "fivelogh0_37": float(res_a["q"][C_H0]), "sigma_37": float(res_a["sigma"][C_H0]),
            "fivelogh0_cchp": float(res_s["q"][C_H0]), "h0_shift_kms": to_h0(float(res_s["q"][C_H0]))
            - to_h0(float(res_a["q"][C_H0]))}, res_a


def loo_chi2(L, y, W, rows_a, groups, labels):
    """Host-level chi^2 of the leave-one-host-out calibrator-SN residuals (README R2-RE)."""
    total, n, per = 0.0, 0, []
    rows_a = np.asarray(rows_a)
    for g in groups:
        g = np.asarray(g)
        keep = np.setdiff1d(rows_a, g)
        res = fit(L, y, W, keep)
        kept = res["kept"]
        Xg = L[np.ix_(g, kept)]
        r = y[g] - Xg @ res["q"][kept]
        S = W[np.ix_(g, g)] + Xg @ res["cov"] @ Xg.T
        c = float(r @ np.linalg.solve(S, r))
        per.append({"host": labels[len(per)], "chi2": c, "n_rows": int(len(g))})
        total += c
        n += len(g)
    return {"chi2": total, "n_rows": n, "per_host": per}


def to_h0(q):
    return float(10 ** (q / 5.0))


def r2_re(ctx, P, C, L, y, nz, cls, rows_a, rows_s, base_rows, host_rows, picks, c_step, anchor_status,
          labels):
    """R2-RE (README section 2, addendum 2026-11-16)."""
    t0 = time.perf_counter()
    calib_groups = [np.flatnonzero(cls["calib"] & nz[:, j]) for j in range(NH)]
    ceph_groups = [np.flatnonzero(cls["ceph_host"] & nz[:, j]) for j in range(NH)]
    out = {"model": "V = C + tau^2 sum_j h_j h_j^T over each host's calibrator SN rows",
           "n_calib_rows_per_host": [int(len(g)) for g in calib_groups]}

    def estimate(groups):
        return reml_tau(lambda t: reml_m2l(L, y, C, rows_a, groups, t), P["re_tau_max"], P["re_grid_step"])

    try:
        est = estimate(calib_groups)
    except (np.linalg.LinAlgError, ValueError) as e:
        if not is_fit_failure(e):
            raise
        out.update(status=f"not evaluable (fit: {e})", anchor_status=anchor_status)
        return out
    out["reml"] = est
    ctx.log(f"R2-RE: tau_hat {est['tau_hat']:.4f} mag, 68% {est['interval_68']}, "
            f"refined {est['refined']}, other local minima {est['other_local_minima']}")
    if est["at_upper_bound"]:
        out.update(status="not evaluable (bound)", tau_hat=est["tau_hat"], interval_68=est["interval_68"],
                   anchor_status=anchor_status)
        return out
    tau = 0.0 if est["at_zero"] else est["tau_hat"]
    try:
        V = with_re(C, calib_groups, tau)
        hs, res_aV = host_step_under(L, y, V, rows_a, rows_s)
    except (np.linalg.LinAlgError, ValueError) as e:   # pre-registered fit failures only
        if not is_fit_failure(e):
            raise
        out.update(status=f"not evaluable (fit: {e})", tau_hat=tau, anchor_status=anchor_status)
        return out
    v = host_step_verdict(hs["z"], hs["shift"], hs["shift_sigma"], P["host_ref"], P["host_ref_extra"])
    out.update(status="evaluated", anchor_status=anchor_status, tau_hat=tau, interval_68=est["interval_68"],
               host_step=hs, z=hs["z"], verdict=v, reference=P["host_ref"],
               reference_tol=2 * hs["shift_sigma"] + P["host_ref_extra"], c_errors=c_step)
    ctx.log(f"R2-RE host step: {hs['shift']:+.4f} +- {hs['shift_sigma']:.4f} (z {hs['z']:.2f}) -> {v}")

    # reported, not decisive; any failure here is a bug and stops the run (nothing is swallowed)
    hi = est["interval_68"][1]
    if isinstance(hi, float):
        hs_hi, _ = host_step_under(L, y, with_re(C, calib_groups, hi), rows_a, rows_s)
        out["at_interval_upper"] = {"tau": hi, "z": hs_hi["z"], "shift": hs_hi["shift"],
                                    "shift_sigma": hs_hi["shift_sigma"]}
    est_c = estimate(ceph_groups)
    sens = {"reml": {k: est_c[k] for k in ("tau_hat", "interval_68", "refined", "other_local_minima",
                                            "at_zero", "at_upper_bound")}}
    if not est_c["at_upper_bound"]:
        tc = 0.0 if est_c["at_zero"] else est_c["tau_hat"]
        hs_c, _ = host_step_under(L, y, with_re(C, ceph_groups, tc), rows_a, rows_s)
        sens.update(host_step=hs_c, verdict_row=host_step_verdict(
            hs_c["z"], hs_c["shift"], hs_c["shift_sigma"], P["host_ref"], P["host_ref_extra"]))
    out["sensitivity_cepheid_rows"] = sens
    r2_re_r4(out, L, y, V, res_aV, hs, rows_a, base_rows, host_rows, picks)
    out["loo_chi2"] = {"C": loo_chi2(L, y, C, rows_a, calib_groups, labels),
                       "V": loo_chi2(L, y, V, rows_a, calib_groups, labels),
                       "note": "predicted from the fit without the host's SN rows; the cross-covariance "
                               "of those rows with the kept rows is ignored (README definition), so the "
                               "comparison with chi^2(n) is approximate"}
    out["seconds"] = time.perf_counter() - t0
    ctx.log(f"R2-RE diagnostics: R4 under V z spread {out['r4_under_v']['z_std']:.3f}; "
            f"LOO chi2 C {out['loo_chi2']['C']['chi2']:.1f}, V {out['loo_chi2']['V']['chi2']:.1f}")
    return out


def r2_re_r4(out, L, y, V, res_aV, hs, rows_a, base_rows, host_rows, picks):
    """R4 under V: the same draws as R4; the full system fitted once under V (in host_step_under)."""
    qa_v, sa_v = hs["fivelogh0_37"], hs["sigma_37"]
    zs, deltas = [], []
    for i, pick in enumerate(picks):
        rows = np.union1d(base_rows, np.concatenate([host_rows[j] for j in pick]))
        res = fit(L, y, V, rows, est=(i == 0))
        dl = float(res["q"][C_H0]) - qa_v
        var = float(res["sigma"][C_H0]) ** 2 - sa_v ** 2
        if i == 0:
            a1 = shift_vector(res, rows, res_aV, rows_a)
            exact = float(a1 @ V @ a1)
            if abs(exact - var) > 1e-6 * exact:
                raise RuntimeError(f"nested-variance identity failed under V on draw 0: {exact} vs {var}")
            out["r4_identity_check"] = {"exact_aVa": exact, "nested": var}
        deltas.append(dl)
        if not var > 0:                  # the nested identity guarantees var > 0: anything else is a bug
            raise RuntimeError(f"non-positive nested variance under V on draw {i}: {var}")
        zs.append(dl / np.sqrt(var))
    if zs:
        zs_a = np.array(zs)
        out["r4_under_v"] = {"draws": len(zs), "z_std": float(zs_a.std()), "z_mean": float(zs_a.mean()),
                             "cchp_z": hs["z"], "z_percentile": float(100.0 * np.mean(zs_a <= hs["z"])),
                             "shift_percentile": float(100.0 * np.mean(np.array(deltas) <= hs["shift"]))}


def n5584_summary(n_out):
    """Short summary of R2-RE-N5584 for summary.json."""
    if n_out.get("status") != "evaluated":
        return {"status": n_out.get("status")}
    a, b = n_out["drop"], n_out["heavy_tail"]
    bn = a.get("bn", {})
    return {"status": "evaluated",
            "drop_reading": a.get("reading", a.get("status")),
            "drop_tau_hat": a.get("r2_re", {}).get("tau_hat"),
            "drop_R4N_verdict": a.get("r4n", {}).get("verdict", a.get("r4n", {}).get("status")),
            "drop_BN_tau": bn.get("tau", {}).get("label", bn.get("tau", {}).get("status")),
            "drop_BN_spread": bn.get("spread", {}).get("label", bn.get("spread", {}).get("status")),
            "t_status": b.get("status"), "t_label": b.get("label"),
            "t_tau_hat": b.get("nu_main", {}).get("tau_hat"), "t_z": b.get("nu_main", {}).get("z"),
            "joint_reading": n_out["joint_reading"]}


# ---------------------------------------------------------------- main
def save_d(ctx, d_out, sims):
    """R2-RE-D's files: r2_re_d.json and one r2_re_d_sims_<model>.json per model (always all of them, so no
    stale file survives)."""
    ctx.save("r2_re_d", d_out)
    for k, v in sims.items():
        ctx.save(f"r2_re_d_sims_{k}", v)


def run_d(ctx, P, L, y, C, nz, cls, rows_a, col_host, ident, n_pick, picks=None, tau_n=None, rob_spread_obs=None):
    """The R2-RE-D block (README section 2, addendum 2026-11-21). picks None: R4's draws regenerated from
    R4's index stream (standalone mode; R4's loop draws rng.choice(37, 10) from default_rng(r4_seed) in order)."""
    keys = onehost.model_keys([float(t) for t in P["d_taus"]])
    if not ident["host_step_evaluable"]:
        st = "not evaluable (host step not evaluable)"
        return {"status": st, "reading": "not evaluable"}, {k: {"model": k, "status": st} for k in keys}
    calib_groups = [np.flatnonzero(cls["calib"] & nz[:, j]) for j in range(NH)]
    host_rows = [np.flatnonzero(nz[:, j]) for j in range(NH)]
    if picks is None:
        picks = sel.index_stream(int(P["rob_n_subsets"]), P["r4_seed"], NH, n_pick)
    fns_d = {"reml_tau": reml_tau, "reml_m2l": reml_m2l, "fit": fit, "shift_vector": shift_vector,
             "with_re": with_re, "is_fit_failure": is_fit_failure, "C_H0": C_H0}
    return onehost.run_block(L, y, C, nz, rows_a, calib_groups, col_host[:NH], host_rows, picks, P, fns_d,
                             ctx.log, n_pick=n_pick, tau_n=tau_n,
                             expected_col=N5584_COLUMN if P["n5584_host"] == "N5584" else None,
                             rob_spread_obs=rob_spread_obs)


def save_g(ctx, g_out, sims):
    """R2-RE-G's full-stage files: r2_re_g.json and the eight r2_re_g_sims_<model>.json (always all of them)."""
    ctx.save("r2_re_g", g_out)
    for k, v in sims.items():
        ctx.save(f"r2_re_g_sims_{k}", v)


def recorded_reml_grid():
    """R2-RE's saved REML grid (README R2-RE-G: the reproduction check's source), read from the committed
    results next to this file (also in an exploration, whose ctx.results is another folder)."""
    path = Path(__file__).parent / "results" / "r2_re.json"
    if not path.exists():
        raise RuntimeError("g_only needs results/r2_re.json (R2-RE's REML grid): run the full study first")
    return json.loads(path.read_text(encoding="utf-8"))["reml"]["grid_m2l"]


def formal_g_done(path=None):
    """shape.formal_g_done: the formal full stage's results/r2_re_g.json exists (README amendment 2026-11-21)."""
    return shape.formal_g_done(path)


def study_log_text():
    """The study's log.md (shape.study_log_text)."""
    return shape.study_log_text()


def save_g_stubs(ctx, P, status):
    """A full study run whose R2-RE-G block does not run (g_check = false, or R2-RE / the host step not
    evaluable): write its records only where no R2-RE-G file exists, so a formal result is never overwritten.
    Returns the record whose summary goes into summary.json (the existing r2_re_g.json when there is one)."""
    p_out, _ = g_not_run(P, status, "power")
    g_out, sims = g_not_run(P, status, "full")
    files = {"r2_re_g_power": p_out, "r2_re_g": g_out, **{f"r2_re_g_sims_{k}": v for k, v in sims.items()}}
    for name, obj in files.items():
        if not (ctx.results / f"{name}.json").exists():
            ctx.save(name, obj)
    path = ctx.results / "r2_re_g.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else g_out


def g_not_run(P, status, stage):
    keys = shape.sim_keys([float(t) for t in P["g_taus_rep"]])
    out = {"stage": stage, "status": status}
    if stage == "full":
        out["reading"] = status if status.startswith("not evaluable") else None
    return out, {k: {"model": k, "status": status} for k in keys}


def run_g(ctx, P, L, y, C, nz, cls, rows_a, col_host, ident, stage, grid_m2l, power_rec=None,
          grid_source=shape.REML_GRID_SOURCE, recorded=None):
    """One stage of the R2-RE-G block (README section 2, addendum 2026-11-21, T-055). Returns (out, sims);
    sims is None in the power stage."""
    if not ident["host_step_evaluable"]:
        out, sims = g_not_run(P, "not evaluable (host step not evaluable)", stage)
        return out, (sims if stage == "full" else None)
    calib_groups = [np.flatnonzero(cls["calib"] & nz[:, j]) for j in range(NH)]
    fns_g = {"reml_tau": reml_tau, "reml_m2l": reml_m2l, "fit": fit, "with_re": with_re,
             "is_fit_failure": is_fit_failure}
    return shape.run_stage(stage, L, y, C, rows_a, calib_groups, col_host[:NH], P, fns_g, ctx.log, grid_m2l,
                           power_rec=power_rec, grid_source=grid_source,
                           expected_col=N5584_COLUMN if P["n5584_host"] == "N5584" else None, recorded=recorded)


def run_g_both(ctx, P, L, y, C, nz, cls, rows_a, col_host, ident, grid_m2l, grid_source, save_power):
    """Both stages in one process (a full study run, or an exploration without a power record): the power
    record is saved and logged before the full stage computes G_obs."""
    p_out, _ = run_g(ctx, P, L, y, C, nz, cls, rows_a, col_host, ident, "power", grid_m2l, grid_source=grid_source)
    save_power(p_out)
    ctx.log(shape.power_log_line(p_out))
    return run_g(ctx, P, L, y, C, nz, cls, rows_a, col_host, ident, "full", grid_m2l, power_rec=p_out,
                 grid_source=grid_source)


# ---------------------------------------------------------------- R2-RE-GT (addendum 2026-11-21, T-057)
def save_gt(ctx, gt_out, sims):
    """R2-RE-GT's full-stage files: r2_re_gt.json and the seven r2_re_gt_sims_<model>.json (always all of them)."""
    ctx.save("r2_re_gt", gt_out)
    for k, v in sims.items():
        ctx.save(f"r2_re_gt_sims_{k}", v)


def formal_gt_done(path=None):
    """shape.gt_formal_done: the formal full stage's results/r2_re_gt.json exists (README R2-RE-GT)."""
    return shape.gt_formal_done(path)


def recorded_g_sims(P):
    """R2-RE-G's committed r2_re_g_sims_<model>.json for VHAT, OANY, OANYVN (the reproduction reference) and
    R2-RE-G's thread settings (shape.read_g_sims)."""
    return shape.read_g_sims(P)


def gt_not_run(P, status, stage):
    keys = shape.gt_sim_keys([float(t) for t in P["g_taus_rep"]])
    out = {"stage": stage, "status": status}
    if stage == "full":
        out["reading"] = status if status.startswith("not evaluable") else None
    return out, {k: {"model": k, "status": status} for k in keys}


def save_gt_stubs(ctx, P, status):
    """A full study run whose R2-RE-GT block does not run: write its records only where no R2-RE-GT file exists, so
    a formal result is never overwritten. Returns the record whose summary goes into summary.json."""
    p_out, _ = gt_not_run(P, status, "power")
    gt_out, sims = gt_not_run(P, status, "full")
    files = {"r2_re_gt_power": p_out, "r2_re_gt": gt_out, **{f"r2_re_gt_sims_{k}": v for k, v in sims.items()}}
    for name, obj in files.items():
        if not (ctx.results / f"{name}.json").exists():
            ctx.save(name, obj)
    path = ctx.results / "r2_re_gt.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else gt_out


def run_gt(ctx, P, L, y, C, nz, cls, rows_a, col_host, ident, stage, grid_m2l, g_saved, power_rec=None,
           grid_source=shape.GT_REML_GRID_SOURCE, recorded=None):
    """One stage of the R2-RE-GT block (README section 2, addendum 2026-11-21, T-057). Returns (out, sims); sims is
    None in the power stage."""
    if not ident["host_step_evaluable"]:
        out, sims = gt_not_run(P, "not evaluable (host step not evaluable)", stage)
        return out, (sims if stage == "full" else None)
    calib_groups = [np.flatnonzero(cls["calib"] & nz[:, j]) for j in range(NH)]
    fns_g = {"reml_tau": reml_tau, "reml_m2l": reml_m2l, "fit": fit, "with_re": with_re,
             "is_fit_failure": is_fit_failure}
    return shape.run_gt_stage(stage, L, y, C, rows_a, calib_groups, col_host[:NH], P, fns_g, ctx.log, grid_m2l,
                              g_saved, power_rec=power_rec, grid_source=grid_source,
                              expected_col=N5584_COLUMN if P["n5584_host"] == "N5584" else None, recorded=recorded)


def run_gt_both(ctx, P, L, y, C, nz, cls, rows_a, col_host, ident, grid_m2l, grid_source, g_saved, save_power):
    """Both stages in one process (a full study run, or an exploration without a power record, both only after the
    formal full stage): the power record is saved and logged before the full stage computes p_T,obs."""
    p_out, _ = run_gt(ctx, P, L, y, C, nz, cls, rows_a, col_host, ident, "power", grid_m2l, g_saved,
                      grid_source=grid_source)
    save_power(p_out)
    ctx.log(shape.gt_power_log_line(p_out))
    return run_gt(ctx, P, L, y, C, nz, cls, rows_a, col_host, ident, "full", grid_m2l, g_saved, power_rec=p_out,
                  grid_source=grid_source)


# ---------------------------------------------------------------- R2-RE-GTP (addendum 2026-11-22, T-060)
GTP_REUSED_FILES = {nk: ("r2_re_gt_sims_" if nk == "4" else "r2_re_g_sims_", keys)
                    for nk, keys in shape.GTP_REUSED_SETS.items()}


def formal_gtp_done(path=None):
    """The formal results/r2_re_gtp.json exists (any formal outcome)."""
    return shape.formal_outcome(shape.STUDY_DIR / "results" / "r2_re_gtp.json" if path is None else path)


def gtp_preflight(ctx, P):
    """The checks of a gtp_only run before any data is loaded. Returns (gt_rec, g_rec, reused_k): R2-RE-GT's and
    R2-RE-G's committed records and the k_s of their reused simulations (always read from this study's committed
    results/, also in an exploration)."""
    if not P["gtp_check"]:
        raise ValueError("gtp_only needs gtp_check = true")
    exploring = getattr(ctx, "max_save_bytes", None) is not None
    if not exploring:
        # a formal run uses the pre-registered grid, streams and counts (README R2-RE-GTP)
        bad = [k for k, v in shape.GTP_PREREGISTERED.items()
               if shape.json_like(P[k]) != shape.json_like(v)]
        if bad:
            raise RuntimeError("R2-RE-GTP formal run refused: PARAMS differ from the pre-registered values (" +
                               ", ".join(bad) + ")")
    if exploring and not formal_gtp_done():
        raise RuntimeError("an exploration may run R2-RE-GTP only after the formal results/r2_re_gtp.json is committed "
                           "(README section 8)")
    res = shape.STUDY_DIR / "results"
    if not formal_gt_done(res / "r2_re_gt.json"):
        raise RuntimeError("R2-RE-GTP needs R2-RE-GT's formal results/r2_re_gt.json")
    gt_rec = json.loads((res / "r2_re_gt.json").read_text(encoding="utf-8"))
    g_rec = json.loads((res / "r2_re_g.json").read_text(encoding="utf-8"))
    if g_rec.get("status") != "evaluated" or "p_G" not in g_rec:
        raise RuntimeError("R2-RE-GTP needs R2-RE-G's evaluated results/r2_re_g.json (with p_G)")
    reused = {}
    for nk, (prefix, keys) in GTP_REUSED_FILES.items():
        reused[nk] = {}
        for tk, key in keys.items():
            f = json.loads((res / f"{prefix}{key}.json").read_text(encoding="utf-8"))
            if f.get("status") != "evaluated" or len(f.get("k", [])) != int(P["gtp_n_sims"]):
                raise RuntimeError(f"{prefix}{key}.json: not an evaluated record of {P['gtp_n_sims']} simulations")
            reused[nk][tk] = np.asarray(f["k"], dtype=np.int64)
    if gt_rec.get("settings", {}).get("threads") != shape.thread_settings() and not exploring:
        raise RuntimeError("R2-RE-GTP refused: the thread settings differ from R2-RE-GT's formal run (its recorded k "
                           "would not be reproduced bit for bit)")
    sum_path = ctx.results / "summary.json"
    if sum_path.exists():
        onehost.summary_with_key(sum_path.read_text(encoding="utf-8"), "R2_RE_GTP", None)
    elif not exploring:
        raise RuntimeError("gtp_only updates summary.json's R2_RE_GTP key: run the full study first")
    if not exploring:
        why = P["gtp_rerun_reason"]
        if formal_gtp_done(ctx.results / "r2_re_gtp.json") and not (
                isinstance(why, str) and why.strip() and why in study_log_text()):
            raise RuntimeError("results/r2_re_gtp.json already holds a formal R2-RE-GTP outcome: a rerun needs PARAMS "
                               "gtp_rerun_reason, a non-empty text also present in log.md")
    return gt_rec, g_rec, reused


def run_gtp_only(ctx, P, L, y, C, nz, cls, col_host, ident, pre):
    """The standalone R2-RE-GTP block after host identification: r2_re_gtp.json, the 12 new
    r2_re_gtp_sims_<nu>_<tau>.json and summary.json's R2_RE_GTP key."""
    gt_rec, g_rec, reused = pre
    if not ident["host_step_evaluable"]:
        out = {"stage": "full", "status": "not evaluable (host step not evaluable)",
               "settings": {"nus": [shape.gtp_nu_key(v) for v in P["gtp_nus"]], "threads": shape.thread_settings()}}
        sims = {}
    else:
        rows_a, _ = anchor_rows(nz, cls, y)
        calib_groups = [np.flatnonzero(cls["calib"] & nz[:, j]) for j in range(NH)]
        fns_g = {"reml_tau": reml_tau, "reml_m2l": reml_m2l, "fit": fit, "with_re": with_re,
                 "is_fit_failure": is_fit_failure}
        out, sims = shape.run_gtp(L, y, C, rows_a, calib_groups, col_host[:NH], P, fns_g, ctx.log,
                                  recorded_reml_grid(), gt_rec, g_rec, reused)
    sum_path = ctx.results / "summary.json"
    new = (onehost.summary_with_key(sum_path.read_text(encoding="utf-8"), "R2_RE_GTP", shape.gtp_summary(out))
           if sum_path.exists() else {"R2_RE_GTP": shape.gtp_summary(out)})
    ctx.save("r2_re_gtp", out)
    for k, v in sims.items():
        ctx.save(f"r2_re_gtp_sims_{k}", v)
    ctx.save("summary", new)
    return new


def gtp_summary_from_file(results):
    """summary.json's R2_RE_GTP in a full study run (R2-RE-GTP runs only standalone): from r2_re_gtp.json if present."""
    path = Path(results) / "r2_re_gtp.json"
    if path.exists():
        return shape.gtp_summary(json.loads(path.read_text(encoding="utf-8")))
    return {"status": "not run (standalone only, README R2-RE-GTP)"}


def gt_preflight(ctx, P):
    """The checks of a gt_only run before any data is loaded (README R2-RE-GT: R2-RE-G's safeguards). Returns
    (g_saved, power_rec): R2-RE-G's saved simulations and, for a formal full stage, the power record."""
    if not P["gt_check"]:
        raise ValueError("gt_only needs gt_check = true")
    if P["gt_stage"] not in ("power", "full"):
        raise ValueError(f"gt_stage must be 'power' or 'full', not {P['gt_stage']!r}")
    exploring = getattr(ctx, "max_save_bytes", None) is not None
    full = P["gt_stage"] == "full"
    if full and exploring and not formal_gt_done():
        raise RuntimeError("an exploration may run only gt_stage = 'power' until the formal full stage's "
                           "results/r2_re_gt.json is committed (README section 8)")
    g_saved, g_threads = recorded_g_sims(P)
    if not exploring:
        # R2-RE-G's saved G_s and tau_s are reproduced exactly only with its thread settings
        bad = shape.thread_problems(g_threads, shape.thread_settings()) if g_threads is not None else []
        if bad:
            raise RuntimeError("R2-RE-GT refused: the thread settings differ from R2-RE-G's formal run ("
                               + "; ".join(bad) + "); its saved simulations would not be reproduced bit for bit")
    power_rec = None
    if full:
        sum_path = ctx.results / "summary.json"
        if sum_path.exists():
            onehost.summary_with_key(sum_path.read_text(encoding="utf-8"), "R2_RE_GT", None)
        elif not exploring:
            raise RuntimeError("gt_only updates summary.json's R2_RE_GT key: run the full study first")
        pw_path = ctx.results / "r2_re_gt_power.json"
        if not exploring:
            # the first formal outcome stands: a rerun needs a reason, present in log.md before it starts
            why = P["gt_rerun_reason"]
            if shape.formal_outcome(ctx.results / "r2_re_gt.json") and not (
                    isinstance(why, str) and why.strip() and why in study_log_text()):
                raise RuntimeError("results/r2_re_gt.json already holds a formal R2-RE-GT outcome: a rerun needs "
                                   "PARAMS gt_rerun_reason, a non-empty text also present in log.md")
            if not pw_path.exists():
                raise RuntimeError("the full stage needs results/r2_re_gt_power.json: run gt_stage = 'power' "
                                   "first and commit its power line to log.md")
            power_rec = json.loads(pw_path.read_text(encoding="utf-8"))
            bad = shape.gt_power_record_problems(power_rec, shape.gt_stage_settings(P))
            if bad:
                raise RuntimeError("R2-RE-GT full stage refused: " + "; ".join(bad))
            if shape.gt_power_log_line(power_rec) not in study_log_text():
                raise RuntimeError("R2-RE-GT full stage refused: the power stage's line (shape.gt_power_log_line) "
                                   "is not present in log.md; add it (and commit it) first (README section 8)")
    return g_saved, power_rec


def run_gt_only(ctx, P, L, y, C, nz, cls, col_host, ident, g_saved):
    """The standalone R2-RE-GT stage(s) after host identification."""
    rows_a, _ = anchor_rows(nz, cls, y)
    grid, src = recorded_reml_grid(), shape.GT_REML_GRID_SOURCE + " (committed file, standalone mode)"
    if P["gt_stage"] == "power":
        p_out, _ = run_gt(ctx, P, L, y, C, nz, cls, rows_a, col_host, ident, "power", grid, g_saved,
                          grid_source=src)
        ctx.save("r2_re_gt_power", p_out)
        ctx.log(shape.gt_power_log_line(p_out))
        return {"R2_RE_GT_power": {k: p_out.get(k) for k in ("status", "n_sims", "power", "size", "reported")}}
    pw_path = ctx.results / "r2_re_gt_power.json"
    if pw_path.exists():
        power_rec = json.loads(pw_path.read_text(encoding="utf-8"))
        gt_out, sims = run_gt(ctx, P, L, y, C, nz, cls, rows_a, col_host, ident, "full", grid, g_saved,
                              power_rec=power_rec, grid_source=src)
    else:               # an exploration (empty folder) after the formal full stage: both stages in this process
        gt_out, sims = run_gt_both(ctx, P, L, y, C, nz, cls, rows_a, col_host, ident, grid, src, g_saved,
                                   lambda o: ctx.save("r2_re_gt_power", o))
    sum_path = ctx.results / "summary.json"
    new = (onehost.summary_with_key(sum_path.read_text(encoding="utf-8"), "R2_RE_GT", shape.gt_summary(gt_out))
           if sum_path.exists() else {"R2_RE_GT": shape.gt_summary(gt_out)})
    save_gt(ctx, gt_out, sims)         # only after the summary check passed: no half-written result
    ctx.save("summary", new)
    return new


def main(ctx):
    P = dict(PARAMS)
    t0 = time.perf_counter()
    d_only = bool(P["d_only"])
    g_only = bool(P["g_only"])
    gt_only = bool(P["gt_only"])
    gtp_only = bool(P["gtp_only"])
    if gtp_only and (d_only or g_only or gt_only):
        raise ValueError("gtp_only cannot be combined with d_only, g_only or gt_only")
    if P["gtp_check"] and not gtp_only:
        raise ValueError("R2-RE-GTP runs only standalone: gtp_check = true needs gtp_only = true (README section 8)")
    gtp_pre = None
    if gtp_only:
        # standalone R2-RE-GTP (README section 2, addendum 2026-11-22, T-060): r2_re_gtp*.json and summary.json's
        # R2_RE_GTP key (records provenance_gtpp / run_info_gtpp)
        ctx.record_suffix = "_gtpp"
        gtp_pre = gtp_preflight(ctx, P)
    if d_only and g_only:
        raise ValueError("d_only and g_only cannot both be true")
    if gt_only and (d_only or g_only):
        raise ValueError("gt_only cannot be combined with d_only or g_only")
    g_saved_gt = None
    if gt_only:
        # standalone R2-RE-GT (README section 2, addendum 2026-11-21, T-057): power stage -> r2_re_gt_power.json
        # (records provenance_gtp / run_info_gtp) only; full stage -> r2_re_gt*.json and summary.json's R2_RE_GT key
        ctx.record_suffix = "_gtp" if P["gt_stage"] == "power" else "_gt"
        g_saved_gt, _ = gt_preflight(ctx, P)
    if P["gt_check"] and not (gt_only or d_only or g_only) and not formal_gt_done():
        raise RuntimeError("gt_check = true outside gt_only would compute p_T on the data before the formal two-stage "
                           "R2-RE-GT run: run gt_only = true with gt_stage = 'power', then 'full', or set gt_check = "
                           "false (README section 8)")
    if P["gt_check"] and not (gt_only or d_only or g_only):
        # a full study run with gt_check (after the formal stages): the same safeguards, before any data is loaded
        # (gate-1 review of the code, 2026-11-21): the first formal outcome stands, and R2-RE-G's committed
        # simulations are the reproduction reference (read now, so a missing file fails before hours of work)
        why = P["gt_rerun_reason"]
        if (getattr(ctx, "max_save_bytes", None) is None and shape.formal_outcome(ctx.results / "r2_re_gt.json")
                and not (isinstance(why, str) and why.strip() and why in study_log_text())):
            raise RuntimeError("results/r2_re_gt.json already holds a formal R2-RE-GT outcome: a full run with "
                               "gt_check = true reruns it and needs PARAMS gt_rerun_reason, also present in log.md")
        g_saved_gt = recorded_g_sims(P)[0]
    if g_only:
        # standalone R2-RE-G (README section 2, addendum 2026-11-21, T-055): power stage -> r2_re_g_power.json
        # (records provenance_gp / run_info_gp) only; full stage -> r2_re_g*.json and summary.json's R2_RE_G key
        if not P["g_check"]:
            raise ValueError("g_only needs g_check = true")
        if P["g_stage"] not in ("power", "full"):
            raise ValueError(f"g_stage must be 'power' or 'full', not {P['g_stage']!r}")
        ctx.record_suffix = "_gp" if P["g_stage"] == "power" else "_g"
        if P["g_stage"] == "full" and getattr(ctx, "max_save_bytes", None) is not None and not formal_g_done():
            raise RuntimeError("an exploration may run only g_stage = 'power' until the formal full stage's "
                               "results/r2_re_g.json is committed (README section 8)")
        if P["g_stage"] == "full":
            sum_path = ctx.results / "summary.json"
            if sum_path.exists():
                onehost.summary_with_key(sum_path.read_text(encoding="utf-8"), "R2_RE_G", None)
            elif getattr(ctx, "max_save_bytes", None) is None:
                raise RuntimeError("g_only updates summary.json's R2_RE_G key: run the full study first")
            pw_path = ctx.results / "r2_re_g_power.json"
            if getattr(ctx, "max_save_bytes", None) is None:
                # the first formal outcome stands: a rerun needs a reason, present in log.md before it starts
                why = P["g_rerun_reason"]
                if shape.formal_outcome(ctx.results / "r2_re_g.json") and not (
                        isinstance(why, str) and why.strip() and why in study_log_text()):
                    raise RuntimeError("results/r2_re_g.json already holds a formal R2-RE-G outcome: a rerun needs "
                                       "PARAMS g_rerun_reason, a non-empty text also present in log.md")
                if not pw_path.exists():
                    raise RuntimeError("the full stage needs results/r2_re_g_power.json: run g_stage = 'power' "
                                       "first and commit its power to log.md")
                power_rec = json.loads(pw_path.read_text(encoding="utf-8"))
                bad = shape.power_record_problems(power_rec, shape.stage_settings(P))
                if bad:
                    raise RuntimeError("R2-RE-G full stage refused: " + "; ".join(bad))
                if shape.power_log_line(power_rec) not in study_log_text():
                    raise RuntimeError("R2-RE-G full stage refused: the power stage's line (shape.power_log_line) "
                                       "is not present in log.md; add it (and commit it) first (README section 8)")
    if P["g_check"] and not g_only and not d_only and not gt_only and not formal_g_done():
        raise RuntimeError("g_check = true outside g_only would compute G on the data before the formal two-stage "
                           "R2-RE-G run: run g_only = true with g_stage = 'power', then 'full', or set g_check = false "
                           "(README section 8)")
    if d_only:
        # standalone R2-RE-D (README section 2, addendum 2026-11-21): its own provenance_d/run_info_d, no
        # other results file written; summary.json must exist and re-serialise to itself (checked first)
        if not P["d_check"]:
            raise ValueError("d_only needs d_check = true")
        ctx.record_suffix = "_d"
        sum_path = ctx.results / "summary.json"
        if sum_path.exists():
            onehost.summary_with_key(sum_path.read_text(encoding="utf-8"), "R2_RE_D", None)
        elif getattr(ctx, "max_save_bytes", None) is None:      # an exploration starts from an empty folder
            raise RuntimeError("d_only updates summary.json's R2_RE_D key: run the full study first")
    save = (lambda name, obj: None) if (d_only or g_only or gt_only or gtp_only) else ctx.save
    C, L, y, lsq = load(ctx)
    hosts = [h for h, *_ in TABLE6]
    hosts = list(dict.fromkeys(hosts))
    assert len(hosts) == NH and sum(TABLE3_FIT.values()) == TABLE3_SUM
    par_names = hosts + ["dmu_N4258", "M_H1_W", "dmu_LMC", "mu_M31", "b_W", "M0_B", "Z_W",
                         "extra", "zp", "5logH0"]
    nz, cls, counts = row_classes(L, y)
    ctx.log(f"row classes: {counts}")
    validity = {"row_counts": counts, "notes": []}

    # ---- baseline and R1
    cf = linalg.cho_factor(C, lower=True)
    base = infer.gls(L, y, c_factor=cf)
    full_rows = np.arange(N_ROWS)
    dq = base["q"] - lsq[:, 0]
    ds = base["sigma"] - lsq[:, 1]
    unfit = np.isnan(base["q"])
    dq[unfit] = np.abs(lsq[unfit, 0])
    ds[unfit] = np.abs(lsq[unfit, 1])
    worst = int(np.argmax(np.maximum(np.abs(dq), np.abs(ds))))
    r1_ok = bool(np.all(np.abs(dq) <= P["tol_r1"]) and np.all(np.abs(ds) <= P["tol_r1"]))
    q46 = float(base["q"][C_H0])
    r1 = {
        "verdict": "reproduced" if r1_ok else "not reproduced",
        "max_abs_dq": float(np.max(np.abs(dq))), "max_abs_dsigma": float(np.max(np.abs(ds))),
        "worst_param": par_names[worst], "unfitted_columns": [par_names[i] for i in np.flatnonzero(unfit)],
        "params": [{"name": par_names[i], "q": None if unfit[i] else float(base["q"][i]),
                    "sigma": None if unfit[i] else float(base["sigma"][i]),
                    "file_q": float(lsq[i, 0]), "file_sigma": float(lsq[i, 1])} for i in range(N_PAR)],
        "chi2": base["chi2"], "dof": base["dof"], "chi2_dof": base["chi2"] / base["dof"],
        "fivelogh0": q46, "sigma_fivelogh0": float(base["sigma"][C_H0]), "h0": to_h0(q46),
        "secondary": {"r22_fivelogh0": 9.318, "r22_h0": 73.04, "diff_mag": q46 - 9.318},
    }
    ctx.log(f"R1: {r1['verdict']} (max |dq| {r1['max_abs_dq']:.2e}, worst {r1['worst_param']}); "
            f"5logH0 {q46:.5f} -> H0 {r1['h0']:.2f}")
    save("r1", r1)

    # ---- host identification (checks i-v)
    mu_fit = base["q"][:NH]
    comp, detail, ncep, rows_y, sn = host_compat(nz, cls, y, mu_fit, hosts, P["sn_match_tol"])
    n_calib_host = [int(len(r)) for r in rows_y]
    i_ok = counts["calib"] == 77 and min(n_calib_host) >= 1
    diag = np.diag(comp)
    ident = {
        "i_calib_rows": counts["calib"], "i_ok": bool(i_ok),
        "ii_ok": bool(np.all(np.diag(detail["ii"]))), "iii_ok": bool(np.all(np.diag(detail["iii"]))),
        "iv_ok": bool(np.all(np.diag(detail["iv"]))),
        "ceph_host_rows": counts["ceph_host"], "ceph_host_expected": [TABLE3_SUM - 37, TABLE3_SUM + 37],
        "per_host": [{"host": h, "calib_rows": n_calib_host[j], "rows_y": [round(float(v), 3) for v in rows_y[j]],
                      "table6_mb": sn[h]["mb"], "mu_fit": float(mu_fit[j]), "mu_ceph_a": sn[h]["mua"],
                      "sigma_a": sn[h]["sa"], "dmu_over_sigma": float((mu_fit[j] - sn[h]["mua"]) / sn[h]["sa"]),
                      "ceph_rows": int(ncep[j]), "table3_fit": TABLE3_FIT[h],
                      "ii": bool(detail["ii"][j, j]), "iii": bool(detail["iii"][j, j]),
                      "iv": bool(detail["iv"][j, j])} for j, h in enumerate(hosts)],
    }
    ceph_ok = TABLE3_SUM - 37 <= counts["ceph_host"] <= TABLE3_SUM + 37
    id_ok = bool(i_ok and diag.all() and ceph_ok)
    # Pre-registered labelling: column j = Table 6 host j. If it fails, the pre-registered verdicts
    # of R2's host step, R3 and R4 are "not evaluable". AMENDMENT (2026-11-14, after the first run;
    # README dated note): label the columns by the perfect matching of the compatibility graph
    # (checks ii-iv), accepted only if it exists and no alternative matching changes the CCHP set.
    mode = "pre-registered" if id_ok else "amended (post-data labelling)"
    if id_ok:
        match = np.arange(NH)
    else:
        comp, detail_m, _, _, _ = host_compat(nz, cls, y, mu_fit, hosts, P["sn_match_tol"], mean_mode=True)
        # cost: 1 for an incompatible edge; ties among compatible edges are broken by the
        # structural distance |mu_fit - mu_Ceph(a)| / sigma(a), scaled to stay far below 1
        dist = np.array([[abs(mu_fit[j] - sn[h]["mua"]) / sn[h]["sa"] for h in hosts] for j in range(NH)])
        cost = np.where(comp, 1e-3 * dist / max(dist.max(), 1.0), 1.0)
        r_, c_ = optimize.linear_sum_assignment(cost)
        match = np.empty(NH, int)
        match[r_] = c_
        ident["amended_check_ii_mean_mode"] = True
        if not (i_ok and ceph_ok and comp[np.arange(NH), match].all()):
            match = None
    if match is not None:
        comp_m = comp[:, match]                 # identity = the chosen labelling
        alts = assignment_alternatives(comp_m)
        col_host = [hosts[match[j]] for j in range(NH)]
    else:
        alts, col_host = [], list(hosts)
    cchp = [j for j in range(NH) if col_host[j] in P["cchp_hosts"]]
    cset = set(cchp)
    changes_set, cchp_perm = False, False
    for a in alts:
        perm = a["perm"]
        new_cchp_cols = {j for j in range(NH) if perm[j] in cset}
        if new_cchp_cols != cset:
            changes_set = True
        elif any(perm[j] != j for j in cset):
            cchp_perm = True
    evaluable = bool(match is not None and len(cchp) == len(P["cchp_hosts"]) and not changes_set)
    ident.update({"compatible_edges_not_chosen": [] if match is None else
                  [[j, hosts[h]] for j, h in zip(*np.nonzero(comp)) if h != match[j]],
                  "ok": id_ok, "preregistered_labelling_ok": id_ok, "mode": mode,
                  "matching_found": match is not None,
                  "column_labels": col_host,
                  "relabelled": [{"column": j, "table6_order_label": hosts[j], "label": col_host[j]}
                                 for j in range(NH) if col_host[j] != hosts[j]],
                  "alternatives": len(alts), "alt_changes_cchp_set": changes_set,
                  "alt_permutes_cchp_only": cchp_perm,
                  "host_step_evaluable": evaluable})
    if match is not None:
        ident["per_column_under_labels"] = [
            {"column": j, "label": col_host[j], "rows_y": [round(float(v), 3) for v in rows_y[j]],
             "table6_mb": sn[col_host[j]]["mb"], "mu_fit": float(mu_fit[j]),
             "mu_ceph_a": sn[col_host[j]]["mua"],
             "dmu_over_sigma": float((mu_fit[j] - sn[col_host[j]]["mua"]) / sn[col_host[j]]["sa"]),
             "ceph_rows": int(ncep[j]), "table3_fit": TABLE3_FIT[col_host[j]]} for j in range(NH)]
    ctx.log(f"host identification: pre-registered ok={id_ok}; mode={mode}; matching={match is not None}; "
            f"alternatives={len(alts)}, changes CCHP set={changes_set}")
    save("host_identification", ident)
    for i_, prm in enumerate(r1["params"][:NH]):
        prm["column_label"] = col_host[i_]
    r1["worst_param_label"] = col_host[worst] if worst < NH else par_names[worst]
    r1["note"] = ("params[].name is the Table 6-order name of the column; column_label is the host "
                  "it holds (host_identification.json)")
    save("r1", r1)
    validity["host_identification_ok"] = id_ok
    validity["host_labelling_mode"] = mode

    if d_only:              # standalone R2-RE-D: rows_a, the R4 / R4-N index streams, the block
        rows_a, _ = anchor_rows(nz, cls, y)
        d_out, sims = run_d(ctx, P, L, y, C, nz, cls, rows_a, col_host, ident,
                            n_pick=len([j for j in range(NH) if col_host[j] in P["cchp_hosts"]]))
        sum_path = ctx.results / "summary.json"
        new = (onehost.summary_with_key(sum_path.read_text(encoding="utf-8"), "R2_RE_D", onehost.summary(d_out))
               if sum_path.exists() else {"R2_RE_D": onehost.summary(d_out)})
        save_d(ctx, d_out, sims)       # only after the summary check passed: no half-written result
        ctx.save("summary", new)
        return new

    if g_only:              # standalone R2-RE-G: rows_a and one stage of the block
        rows_a, _ = anchor_rows(nz, cls, y)
        grid, src = recorded_reml_grid(), shape.REML_GRID_SOURCE + " (committed file, standalone mode)"
        if P["g_stage"] == "power":
            p_out, _ = run_g(ctx, P, L, y, C, nz, cls, rows_a, col_host, ident, "power", grid, grid_source=src)
            ctx.save("r2_re_g_power", p_out)
            ctx.log(shape.power_log_line(p_out))
            return {"R2_RE_G_power": {k: p_out.get(k) for k in ("status", "n_sims", "power", "size",
                                                                 "smallest_z_alt_power_08")}}
        pw_path = ctx.results / "r2_re_g_power.json"
        if pw_path.exists():
            power_rec = json.loads(pw_path.read_text(encoding="utf-8"))
            g_out, sims = run_g(ctx, P, L, y, C, nz, cls, rows_a, col_host, ident, "full", grid, power_rec=power_rec,
                                grid_source=src)
        else:               # an exploration (empty folder): both stages in this process
            g_out, sims = run_g_both(ctx, P, L, y, C, nz, cls, rows_a, col_host, ident, grid, src,
                                     lambda o: ctx.save("r2_re_g_power", o))
        sum_path = ctx.results / "summary.json"
        new = (onehost.summary_with_key(sum_path.read_text(encoding="utf-8"), "R2_RE_G", shape.summary(g_out))
               if sum_path.exists() else {"R2_RE_G": shape.summary(g_out)})
        save_g(ctx, g_out, sims)       # only after the summary check passed: no half-written result
        ctx.save("summary", new)
        return new

    if gt_only:             # standalone R2-RE-GT: rows_a and one stage of the block
        return run_gt_only(ctx, P, L, y, C, nz, cls, col_host, ident, g_saved_gt)
    if gtp_only:            # standalone R2-RE-GTP
        return run_gtp_only(ctx, P, L, y, C, nz, cls, col_host, ident, gtp_pre)

    # ---- R2 anchor step
    rows_a, achk = anchor_rows(nz, cls, y)
    res_a = fit(L, y, C, rows_a, est=True)
    res_b = infer.gls(L, y, c_factor=cf, return_estimator=True)
    qa = float(res_a["q"][C_H0])
    sa = float(res_a["sigma"][C_H0])
    d_a = qa - q46
    a_vec = shift_vector(res_a, rows_a, res_b, full_rows)
    var_a = float(a_vec @ C @ a_vec)
    anchor_repro = bool(achk["ok"] and abs(d_a - P["anchor_target"]) <= P["anchor_tol"]
                        and abs(sa / P["anchor_sigma_target"] - 1) <= P["anchor_sigma_frac"])
    r2a = {"structural": achk, "fivelogh0": qa, "sigma": sa, "h0": to_h0(qa), "shift": d_a,
           "shift_sigma": float(np.sqrt(max(var_a, 0.0))), "shift_check_ay": float(a_vec @ y),
           "target": P["anchor_target"], "sigma_target": P["anchor_sigma_target"],
           "secondary_2024": 5 * np.log10(72.54 / 73.17),
           "verdict": "reproduced" if anchor_repro else "not reproduced"}
    ctx.log(f"R2 anchor: shift {d_a:+.4f} (target -0.0158), sigma {sa:.4f} (target 0.0461) -> {r2a['verdict']}")

    # ---- R2 host step
    other_hosts = [j for j in range(NH) if j not in cset]
    drop = nz[:, other_hosts].any(axis=1)
    rows_s = np.array([i for i in rows_a if not drop[i]])
    res_s = fit(L, y, C, rows_s, est=True)
    qs = float(res_s["q"][C_H0])
    d_h = qs - qa
    a_h = shift_vector(res_s, rows_s, res_a, rows_a)
    var_h = float(a_h @ C @ a_h)
    s_h = float(np.sqrt(var_h))
    z = d_h / s_h
    ref, extra = P["host_ref"], P["host_ref_extra"]
    if z <= -2 and abs(d_h - ref) <= 2 * s_h + extra:
        v = "host selection significantly lowers H0, by the size the paper reports (supports the paper)"
    elif z <= -2:
        v = "host selection significantly lowers H0, but by a different size"
    elif abs(z) < 2:
        v = "no host-selection effect detected in these data (does not support the paper's quantitative claim)"
    else:
        v = "host selection raises H0 (contradicts the paper)"
    if not ident["host_step_evaluable"]:
        v = "not evaluable (host identification)"
        status = "not evaluable (host identification)"
    elif not anchor_repro:
        status = "conditional (anchor rule not validated)"
    else:
        status = "evaluated"
    if mode != "pre-registered":
        status += "; " + mode
    r2h = {"rows": int(len(rows_s)), "fivelogh0": qs, "sigma": float(res_s["sigma"][C_H0]), "h0": to_h0(qs),
           "shift": d_h, "shift_sigma": s_h, "z": z, "shift_check_ay": float(a_h @ y),
           "nested_var_check": float(res_s["sigma"][C_H0] ** 2 - sa ** 2),
           "reference": ref, "reference_tol": 2 * s_h + extra,
           "h0_shift_kms": to_h0(qs) - to_h0(qa), "verdict": v, "status": status,
           "preregistered_verdict": v if mode == "pre-registered" else "not evaluable (host identification)",
           "labelling_mode": mode}
    ctx.log(f"R2 host: shift {d_h:+.4f} +- {s_h:.4f} (z {z:+.2f}); {v}; {status}")
    ctx.save("r2", {"anchor_step": r2a, "host_step": r2h})

    # ---- R3 (descriptive)
    r3 = {"status": "evaluated", "labelling_mode": mode}
    m_rows = np.flatnonzero(cls["maser"])
    n4258_ceph = cls["ceph"] & nz[:, C_N4258]
    cvals = np.unique(L[n4258_ceph, C_N4258])
    if not ident["host_step_evaluable"] or len(m_rows) != 1 or len(cvals) != 1 or abs(abs(cvals[0]) - 1) > 1e-12 \
            or abs(abs(L[m_rows[0], C_N4258]) - 1) > 1e-12:
        r3["status"] = "not evaluable"
    else:
        m = int(m_rows[0])
        k, c = float(L[m, C_N4258]), float(cvals[0])
        sm2 = float(C[m, m])
        t = np.array([CCHP_TRGB[col_host[j]][0] for j in cchp])
        st = np.array([CCHP_TRGB[col_host[j]][1] for j in cchp])

        def cchp_side(zp_terms):
            Ct = np.diag(st ** 2) + ((P["trgb_tip_sys"] ** 2 + sm2) if zp_terms else 0.0)
            cross = k * c * sm2 if zp_terms else 0.0
            cep_drop = cls["ceph"] & nz[:, cchp].any(axis=1)
            rows_c = np.array([i for i in rows_s if not cep_drop[i]])
            nc = len(rows_c)
            Lt = np.zeros((len(cchp), N_PAR))
            Lt[np.arange(len(cchp)), cchp] = 1.0
            Lz = np.vstack([L[rows_c], Lt])
            yz = np.concatenate([y[rows_c], t])
            Cz = np.zeros((nc + len(cchp),) * 2)
            Cz[:nc, :nc] = C[np.ix_(rows_c, rows_c)]
            Cz[nc:, nc:] = Ct
            mp = int(np.searchsorted(rows_c, m))
            assert rows_c[mp] == m
            Cz[mp, nc:] = cross
            Cz[nc:, mp] = cross
            res = infer.gls(Lz, yz, Cz, return_estimator=True)
            return res, rows_c, Ct, cross

        def contrast(res_c, rows_c, Ct, cross, col_s, t_coef):
            """b = b_S - b_C over z = (y, t); returns value and sigma via Cov(z)."""
            by = np.zeros(N_ROWS)
            by[rows_s] += res_s["A"][kpos(res_s, col_s)]
            bt = np.array(t_coef, float)
            if res_c is not None:
                row = res_c["A"][kpos(res_c, C_H0)]
                by[rows_c] -= row[:len(rows_c)]
                bt = bt - row[len(rows_c):]
            val = float(by @ y + bt @ t)
            var = float(by @ C @ by + bt @ Ct @ bt + 2 * by[m] * cross * bt.sum())
            return val, var, by, bt

        res_c, rows_c, Ct, cross = cchp_side(True)
        qc = float(res_c["q"][C_H0])
        d, var_d, _, _ = contrast(res_c, rows_c, Ct, cross, C_H0, np.zeros(len(cchp)))
        # per-host delta mu: mu_S,i (SH0ES host-step fit) - t_i
        B_y = np.zeros((len(cchp), N_ROWS))
        B_t = -np.eye(len(cchp))
        for r, j in enumerate(cchp):
            B_y[r, rows_s] = res_s["A"][kpos(res_s, j)]
        dmu = B_y @ y + B_t @ t
        cross_term = np.outer(B_y[:, m] * cross, B_t.sum(axis=1))
        cov_dmu = B_y @ C @ B_y.T + B_t @ Ct @ B_t.T + cross_term + cross_term.T
        chi2 = float(dmu @ np.linalg.solve(cov_dmu, dmu))
        res_c0, rows_c0, Ct0, cross0 = cchp_side(False)
        d0, var_d0, _, _ = contrast(res_c0, rows_c0, Ct0, cross0, C_H0, np.zeros(len(cchp)))
        r3.update({
            "k": k, "c": c, "maser_var": sm2,
            "cchp_side_fivelogh0": qc, "cchp_side_h0": to_h0(qc),
            "cchp_target_fivelogh0": P["cchp_target_5logh0"], "cchp_target_h0": 69.29,
            "cchp_match": "matched" if abs(qc - P["cchp_target_5logh0"]) <= P["cchp_match_tol"] else "not matched",
            "cchp_diff_mag": qc - P["cchp_target_5logh0"],
            "d": d, "sigma_d": float(np.sqrt(var_d)), "d_check": qs - qc,
            "d_kms_illustrative": to_h0(qs) - to_h0(qc),
            "per_host": [{"host": col_host[j], "mu_ceph": float(res_s["q"][j]), "mu_trgb": float(t[r]),
                          "dmu": float(dmu[r]), "sigma": float(np.sqrt(cov_dmu[r, r]))}
                         for r, j in enumerate(cchp)],
            "dmu_chi2": chi2, "dmu_dof": len(cchp),
            "dmu_weighted_mean": float(np.sum(np.linalg.solve(cov_dmu, dmu)) / np.sum(np.linalg.solve(cov_dmu, np.ones(len(cchp))))),
            "sensitivity_no_zp_terms": {"cchp_side_fivelogh0": float(res_c0["q"][C_H0]), "d": d0,
                                        "sigma_d": float(np.sqrt(var_d0))},
            "sensitivity_csp": {"cchp_h0": CCHP_CSP_H0, "d": qs - 5 * np.log10(CCHP_CSP_H0)},
        })
        ctx.log(f"R3: CCHP side H0 {to_h0(qc):.2f} ({r3['cchp_match']}); d {d:+.4f} +- {np.sqrt(var_d):.4f}; "
                f"per-host chi2 {chi2:.1f}/{len(cchp)}")
    ctx.save("r3", r3)

    # ---- R4 (descriptive)
    host_rows = [np.flatnonzero(nz[:, j]) for j in range(NH)]
    any_host = nz[:, :NH].any(axis=1)
    base_rows = np.array([i for i in rows_a if not any_host[i]])
    n_sn = {h: len(sn[h]["mb"]) for h in hosts}
    n_sn_col = [n_sn[col_host[j]] for j in range(NH)]
    draws = int(P["r4_draws"])
    deltas, nsns, zs, picks = [], [], [], []
    r4 = {"status": "evaluated", "draws_requested": draws, "labelling_mode": mode}
    if not ident["host_step_evaluable"]:
        r4["status"] = "not evaluable"
    else:
        deltas, nsns, zs, picks = r4_draws(L, y, C, rows_a, res_a, qa, sa, base_rows, host_rows,
                                           np.arange(NH), len(cchp), draws, P["r4_seed"],
                                           P["r4_max_minutes"], n_sn_col, r4, ctx.log, "R4")
        if deltas:
            r4.update(r4_summary(deltas, zs, nsns, d_h, z))
            ctx.log(f"R4: CCHP shift at percentile {r4['percentile']:.1f} of {r4['draws']} draws -> {r4['verdict']}")
    ctx.save("r4", r4)

    # ---- R2-RE (README section 2, addendum 2026-11-16): host-level random effect
    re = {"status": "not run"}
    if P["re_check"] and ident["host_step_evaluable"]:
        re = r2_re(ctx, P, C, L, y, nz, cls, rows_a, rows_s, base_rows, host_rows, picks,
                   {"shift": d_h, "shift_sigma": s_h, "z": z}, status, col_host[:NH])
    ctx.save("r2_re", re)                 # always written, so no stale file survives

    # ---- R2-RE-ROB (README section 2, addendum 2026-11-17, T-032): descriptive labels for R2-RE
    rob_out = {"status": "not run (PARAMS)"}
    if P["rob_check"] and not (P["re_check"] and ident["host_step_evaluable"]):
        rob_out = {"A": {"status": "not evaluable (R2-RE not evaluable)"},
                   "B": {"tau": {"status": "not evaluable (R2-RE not evaluable)"},
                         "spread": {"status": "not evaluable (R4 has no draws)" if not picks
                                    else "not evaluable (host step not evaluable)"}}}
    if P["rob_check"] and P["re_check"] and ident["host_step_evaluable"]:
        calib_groups = [np.flatnonzero(cls["calib"] & nz[:, j]) for j in range(NH)]
        fns = {"reml_tau": reml_tau, "reml_m2l": reml_m2l, "host_step_under": host_step_under,
               "with_re": with_re, "fit": fit, "shift_vector": shift_vector, "is_fit_failure": is_fit_failure,
               "C_H0": C_H0,
               "verdict": lambda z_, d_, s_: host_step_verdict(z_, d_, s_, P["host_ref"], P["host_ref_extra"])}
        t_rob = time.perf_counter()
        rob_out = {"A": rob.leave_one_out(L, y, C, nz, rows_a, rows_s, set(cset), calib_groups, re,
                                          col_host[:NH], P, fns, ctx.log),
                   "B": rob.null_sims(L, y, C, rows_a, calib_groups, re, picks, base_rows, host_rows,
                                      P, fns, ctx.log)}
        rob_out["seconds"] = time.perf_counter() - t_rob
        ctx.log(f"R2-RE-ROB: A {rob_out['A'].get('label', rob_out['A']['status'])}; "
                f"B tau {rob_out['B'].get('tau', {}).get('label')}; "
                f"B spread {rob_out['B'].get('spread', {}).get('label')}")
    ctx.save("r2_re_rob", rob_out)

    # ---- R2-RE-N5584 (README section 2, addendum 2026-11-18, T-039): runs after, and in addition to,
    # the R2-RE-ROB block, under the same condition (R2-RE run and the host step evaluable)
    n_out = {"status": "not run (PARAMS)"}
    if P["n5584_check"] and not (P["re_check"] and ident["host_step_evaluable"]):
        n_out = {"status": "not evaluable (R2-RE not run or host step not evaluable)"}
    if P["n5584_check"] and P["re_check"] and ident["host_step_evaluable"]:
        calib_groups = [np.flatnonzero(cls["calib"] & nz[:, j]) for j in range(NH)]
        fns_n = {"reml_tau": reml_tau, "reml_m2l": reml_m2l, "host_step_under": host_step_under,
                 "with_re": with_re, "fit": fit, "shift_vector": shift_vector, "is_fit_failure": is_fit_failure,
                 "C_H0": C_H0, "r4_draws": r4_draws, "r4_summary": r4_summary, "r2_re_r4": r2_re_r4,
                 "verdict": lambda z_, d_, s_: host_step_verdict(z_, d_, s_, P["host_ref"], P["host_ref_extra"])}
        n_out = n5584.run_block(L, y, C, nz, cls, rows_a, rows_s, sorted(cset), calib_groups, col_host[:NH],
                                host_rows, n_sn_col, re, {"shift": d_h, "shift_sigma": s_h, "z": z}, P, fns_n,
                                ctx.log, expected_col=N5584_COLUMN if P["n5584_host"] == "N5584" else None)
        ctx.log(f"R2-RE-N5584: (a) {n_out['drop'].get('reading', n_out['drop']['status'])}; "
                f"(b) {n_out['heavy_tail'].get('label')}")
    ctx.save("r2_re_n5584", n_out)

    # ---- R2-RE-SEL (README section 2, addendum 2026-11-19, T-042): runs after the R2-RE-N5584 block and
    # only when that block runs (the same condition: R2-RE run and the host step evaluable)
    sel_out = {"status": "not run (PARAMS)"}
    if P["sel_check"] and not P["n5584_check"]:
        sel_out = {"status": "not run (the R2-RE-N5584 block is not run)"}
    elif P["sel_check"] and not (P["re_check"] and ident["host_step_evaluable"]):
        sel_out = {"status": "not evaluable (R2-RE not run or host step not evaluable)"}
    elif P["sel_check"]:
        calib_groups = [np.flatnonzero(cls["calib"] & nz[:, j]) for j in range(NH)]
        fns_s = {"reml_tau": reml_tau, "reml_m2l": reml_m2l, "fit": fit, "shift_vector": shift_vector,
                 "is_fit_failure": is_fit_failure, "loo_chi2": loo_chi2, "C_H0": C_H0}
        sel_out = sel.run_block(L, y, C, nz, rows_a, calib_groups, col_host[:NH], host_rows, picks, n_out, P,
                                fns_s, ctx.log, n_pick=len(cset),
                                expected_col=N5584_COLUMN if P["n5584_host"] == "N5584" else None,
                                rob_spread_obs=rob_out.get("B", {}).get("spread", {}).get("spread_obs"))
        ctx.log(f"R2-RE-SEL: {sel_out.get('reading', sel_out['status'])}")
    ctx.save("r2_re_sel", sel_out)

    # ---- R2-RE-D (README section 2, addendum 2026-11-21, T-048): runs after the R2-RE-SEL block, under the
    # condition of the R2-RE-N5584 block (that block run, R2-RE run and the host step evaluable); tau_hat_N
    # from that block when it was evaluated, else computed in the block
    keys_d = onehost.model_keys([float(t) for t in P["d_taus"]])
    if not P["d_check"]:
        st = "not run (PARAMS)"
        d_out, sims_d = {"status": st}, {k: {"model": k, "status": st} for k in keys_d}
    elif not P["n5584_check"]:
        st = "not run (the R2-RE-N5584 block is not run)"
        d_out, sims_d = {"status": st}, {k: {"model": k, "status": st} for k in keys_d}
    elif not (P["re_check"] and ident["host_step_evaluable"]):
        st = "not evaluable (R2-RE not run or host step not evaluable)"
        d_out, sims_d = {"status": st, "reading": "not evaluable"}, {k: {"model": k, "status": st} for k in keys_d}
    else:
        rn = n_out.get("drop", {}).get("r2_re", {}) if n_out.get("status") == "evaluated" else {}
        d_out, sims_d = run_d(ctx, P, L, y, C, nz, cls, rows_a, col_host, ident, n_pick=len(cset), picks=picks,
                              tau_n=rn.get("tau_hat") if rn.get("status") == "evaluated" else None,
                              rob_spread_obs=rob_out.get("B", {}).get("spread", {}).get("spread_obs"))
    save_d(ctx, d_out, sims_d)

    # ---- R2-RE-G (README section 2, addendum 2026-11-21, T-055): runs after the R2-RE-D block, under the
    # condition R2-RE run and the host step evaluable; both stages in this process, the power record saved and
    # logged before G_obs is computed; R2-RE's REML grid from this run
    sims_g = None
    if not P["g_check"]:
        g_out = save_g_stubs(ctx, P, "not run (PARAMS)")
    elif not (P["re_check"] and ident["host_step_evaluable"]) or re.get("status") != "evaluated":
        g_out = save_g_stubs(ctx, P, "not evaluable (R2-RE not run or host step not evaluable)")
    else:
        g_out, sims_g = run_g_both(ctx, P, L, y, C, nz, cls, rows_a, col_host, ident, re["reml"]["grid_m2l"],
                                   "R2-RE's REML grid of the same run (r2_re.json reml.grid_m2l)",
                                   lambda o: ctx.save("r2_re_g_power", o))
    if sims_g is not None:
        save_g(ctx, g_out, sims_g)

    # ---- R2-RE-GT (README section 2, addendum 2026-11-21, T-057): runs after the R2-RE-G block under the same
    # condition (only after its formal full stage, see main's gate); R2-RE-G's committed simulation files are the
    # reproduction reference (read in main before any data is loaded)
    sims_gt = None
    if not P["gt_check"]:
        gt_out = save_gt_stubs(ctx, P, "not run (PARAMS)")
    elif not (P["re_check"] and ident["host_step_evaluable"]) or re.get("status") != "evaluated":
        gt_out = save_gt_stubs(ctx, P, "not evaluable (R2-RE not run or host step not evaluable)")
    else:
        g_saved_gt = g_saved_gt if g_saved_gt is not None else recorded_g_sims(P)[0]   # committed files
        gt_out, sims_gt = run_gt_both(ctx, P, L, y, C, nz, cls, rows_a, col_host, ident, re["reml"]["grid_m2l"],
                                      "R2-RE's REML grid of the same run (r2_re.json reml.grid_m2l)", g_saved_gt,
                                      lambda o: ctx.save("r2_re_gt_power", o))
    if sims_gt is not None:
        save_gt(ctx, gt_out, sims_gt)

    # One canonical qualified verdict for the host step (gate-2 review): states the labelling mode
    # and, when R4 ran, the empirical (random-subset) scale next to the C-propagated significance.
    qual = []
    if mode != "pre-registered":
        qual.append("post-data host labelling, with identification check (ii) changed to compare means")
    if r4.get("z_std"):
        qual.append(f"{z:.1f} sigma uses C-propagated errors; on the random-subset scale "
                    f"(Delta/sigma spread {r4['z_std']:.2f}, itself uncertain) about "
                    f"{z / r4['z_std']:.1f} sigma (post-hoc Delta/sigma percentile "
                    f"{r4['z_percentile']:.1f}; pre-registered R4 Delta percentile {r4['percentile']:.1f}); "
                    f"with sigma inflated by that spread the verdict table would give 'no host-selection "
                    f"effect detected'")
    r2h["qualified_verdict"] = v + (" [" + "; ".join(qual) + "]" if qual and ident["host_step_evaluable"] else "")
    # the public verdict is the qualified one; the bare row of the verdict table is kept, labelled
    r2h["criterion_outcome"] = r2h.pop("verdict")
    r2h["verdict"] = r2h["qualified_verdict"]
    # R2-RE headline rule (addendum 2026-11-16): when R2-RE is evaluable its verdict row is the public
    # host-step verdict; R2 (C errors) stays recorded; the inflated-sigma text becomes descriptive
    if re.get("status") == "evaluated":
        r2h["descriptive_inflated_sigma"] = r2h["qualified_verdict"]
        tags = ["R2-RE: host-level random effect, pre-registered 2026-11-16",
                "post-data host labelling" if mode != "pre-registered" else "pre-registered labelling"]
        prefix = "" if anchor_repro else "conditional (anchor rule not validated): "
        r2h["verdict"] = prefix + re["verdict"] + " [" + "; ".join(tags) + "]"
        r2h["headline_source"] = "R2-RE"
    else:
        r2h["headline_source"] = "R2 (C errors) with qualification; R2-RE " + re.get("status", "not run")
    ctx.save("r2", {"anchor_step": r2a, "host_step": r2h})

    # ---- cross-paper comparison (descriptive)
    def pair(a, b):
        hi_a = a["hi"] if b["h0"] > a["h0"] else a["lo"]
        hi_b = b["hi"] if a["h0"] > b["h0"] else b["lo"]
        return (a["h0"] - b["h0"]) / np.hypot(hi_a, hi_b)
    pubs = {p["name"]: p for p in PUBLISHED}
    cmb = pubs["SPT-3G + ACT + Planck (CMB only)"]
    ladder = pubs["SH0ES R22 baseline"]
    lens = pubs["TDCOSMO 2025 (flat LCDM)"]
    cross = {
        "values": PUBLISHED,
        "interpreted_pairs": [
            {"pair": "SH0ES R22 vs CMB-only", "nsigma": float(pair(ladder, cmb))},
            {"pair": "TDCOSMO vs SH0ES R22", "nsigma": float(pair(lens, ladder))},
            {"pair": "TDCOSMO vs CMB-only", "nsigma": float(pair(lens, cmb))},
            {"pair": "CCHP TRGB vs CMB-only", "nsigma": float(pair(pubs["CCHP TRGB (24 calibrators)"], cmb))},
        ],
        "not_independent": ["SH0ES R22", "SH0ES + JWST 2024", "H0DN", "CCHP"],
        "note": "SH0ES, H0DN and CCHP share data; listed, not interpreted, not averaged.",
    }
    ctx.save("cross_paper", cross)

    summary = {
        "params": P,
        "validity": validity,
        "R1": r1["verdict"], "R1_h0": r1["h0"],
        "R2_anchor": r2a["verdict"], "R2_anchor_shift": d_a,
        "R2_host": r2h["verdict"], "R2_host_headline_source": r2h["headline_source"],
        "R2_RE": {k: re.get(k) for k in ("status", "verdict", "tau_hat", "interval_68", "z")},
        "R2_host_status": r2h["status"],
        "R2_host_preregistered": r2h["preregistered_verdict"], "host_labelling_mode": mode,
        "R2_host_shift": d_h, "R2_host_sigma": s_h, "R2_host_z": z,
        "R3_cchp_match": r3.get("cchp_match"), "R3_d": r3.get("d"), "R3_sigma_d": r3.get("sigma_d"),
        "R4_percentile": r4.get("percentile"), "R4_verdict": r4.get("verdict", r4["status"]),
        "R2_RE_N5584": n5584_summary(n_out),
        "R2_RE_SEL": sel.summary(sel_out),
        "R2_RE_D": onehost.summary(d_out),
        "R2_RE_G": shape.summary(g_out),
        "R2_RE_GT": shape.gt_summary(gt_out),
        "R2_RE_GTP": gtp_summary_from_file(ctx.results),
        "runtime_s": time.perf_counter() - t0,
    }
    ctx.save("summary", summary)
    return summary
