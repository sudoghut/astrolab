"""R-DIAG of study 011 (README 4.11, T-061, post hoc): the input sample, per-object terms, K24's published
curve, and the labels and reading of the addendum.

Pure functions only: every tunable arrives as an argument (run.py passes PARAMS values); this module never
imports run.
"""
from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

import fit011 as F
import wave011 as W

# README 4.11 Part B: the name map from the named 12CO rows to the Zucker et al. 2020 names (fixed there).
NAME_MAP = {n: n for n in ("CB29", "CMa_OB1", "Cam", "Cepheus", "CygnusX", "IC5146", "L1228", "L1228D", "L1251",
                           "L1265", "L1333", "L1617", "L1622", "L977", "L988", "Lacerta", "Orion", "Orion_Lam",
                           "Polaris", "S106")}
NAME_MAP.update({"MonR2": "Mon_R2", "Mon_R2": "Mon_R2", "NorthAmerica": "North_America",
                 "NorthAmericaNebula": "North_America", "NorthernCoalsack": "Northern_Coalsack"})

T1_KEYS = ("A", "p", "delta", "s0", "gamma", "phi")
SHAPE_PHYS = ("x0", "y0", "x1", "y1", "x2", "y2", "A", "p", "delta", "s0", "gamma", "phi")


# ---------------------------------------------------------------------------------------------
# Part B: the membership rule

def membership(rows, sightlines, *, k=3.0, floor=5.0, name_map=None):
    """README 4.11 Part B membership rule.

    rows: list of dicts (in 12CO table order) with name, p = (x, y, z) and sig = (xspread, yspread, zspread).
    sightlines: dict with arrays name, x, y, z (the Zucker table; index = row number).
    Tolerance t_a = k max(sig_a, floor); candidates: sightlines of the mapped name within t_a on every axis. A
    sightline that is a candidate of several rows goes to the row with the smaller max_a |x_a - p_a| / t_a
    (compared exactly; ties to the row listed first). Gate: a row whose candidates all went to other rows is
    absorbed (dropped); otherwise it passes if it keeps >= 1 sightline whose mean lies within max(sig_a, floor)
    of p on every axis, else it falls back to its own 12CO point (no candidates, or the mean outside).
    Returns one record per row: candidates, kept, status (pass | fallback | absorbed), absorbed_by, reason, and
    absorbed_rows (the rows it absorbed). A row absorbed by a row that then falls back leaves no point in S; the
    fallback row lists it under absorbed_rows. floor must be > 0 (a zero spread would give a zero tolerance and
    undefined scores)."""
    if not (math.isfinite(k) and k > 0):
        raise ValueError(f"the membership factor k must be finite and > 0 (got {k!r})")
    if not floor > 0:
        raise ValueError(f"the membership floor must be > 0 (got {floor!r})")
    name_map = NAME_MAP if name_map is None else name_map
    sx = np.column_stack([np.asarray(sightlines["x"], float), np.asarray(sightlines["y"], float),
                          np.asarray(sightlines["z"], float)])
    snames = np.asarray(sightlines["name"]).astype(str)
    cands, scores = [], []
    for r in rows:
        p = np.asarray(r["p"], float)
        sig = np.asarray(r["sig"], float)
        tol = k * np.maximum(sig, floor)
        idx = np.flatnonzero(snames == name_map[r["name"]])
        dev = np.abs(sx[idx] - p)
        ok = np.all(dev <= tol, axis=1)
        idx = idx[ok]
        cands.append([int(j) for j in idx])
        scores.append({int(j): float(np.max(dev[m] / tol)) for j, m in zip(idx, np.flatnonzero(ok))})
    owner = {}
    for i in range(len(rows)):                       # table order; strict < keeps the first row on a tie
        for j in cands[i]:
            if j not in owner or scores[i][j] < scores[owner[j]][j]:
                owner[j] = i
    out = []
    for i, r in enumerate(rows):
        kept = [j for j in cands[i] if owner[j] == i]
        rec = {"name": r["name"], "mapped": name_map[r["name"]], "p": [float(a) for a in r["p"]],
               "sig": [float(a) for a in r["sig"]], "candidates": cands[i], "kept": kept,
               "absorbed_by": None, "reason": None, "absorbed_rows": []}
        if not cands[i]:
            rec.update(status="fallback", reason="no candidates")
        elif not kept:
            by = sorted({owner[j] for j in cands[i]})
            rec.update(status="absorbed", absorbed_by=[rows[b]["name"] for b in by],
                       reason="absorbed by " + ", ".join(rows[b]["name"] for b in by))
        else:
            mean = sx[kept].mean(axis=0)
            gate = np.maximum(np.asarray(r["sig"], float), floor)
            if np.all(np.abs(mean - np.asarray(r["p"], float)) <= gate):
                rec["status"] = "pass"
            else:
                rec.update(status="fallback", reason="mean of the kept sightlines outside max(spread, floor)")
        out.append(rec)
    for rec in out:                                  # README 4.11 amendment 3: who absorbed whom
        for b in rec["absorbed_by"] or []:
            out[[r["name"] for r in rows].index(b)]["absorbed_rows"].append(rec["name"])
    return out


def build_samples(co_named, zucker, bridging, members, *, pt_names=("Perseus", "Taurus"), name_map=None):
    """S (the passing rows' kept sightlines, the fallback rows' own points, the bridging sightlines), S_all (all
    Zucker sightlines of the mapped names plus the bridging sightlines) and S+PT (S plus all sightlines of
    pt_names). Each sample: dict with x, y, z arrays and per point `source` and `row` (12CO row or None)."""
    name_map = NAME_MAP if name_map is None else name_map
    zx, zy, zz = (np.asarray(zucker[a], float) for a in ("x", "y", "z"))
    zn = np.asarray(zucker["name"]).astype(str)
    bx, by, bz = (np.asarray(bridging[a], float) for a in ("x", "y", "z"))
    bn = [str(n) for n in bridging["name"]]

    def sample(pts):
        return {"x": np.array([p[2] for p in pts], float), "y": np.array([p[3] for p in pts], float),
                "z": np.array([p[4] for p in pts], float), "source": [p[0] for p in pts], "row": [p[1] for p in pts],
                "id": [p[5] for p in pts]}

    pts = []
    for rec, row in zip(members, co_named):
        if rec["status"] == "pass":
            pts += [("zucker", rec["name"], zx[j], zy[j], zz[j], int(j)) for j in rec["kept"]]
        elif rec["status"] == "fallback":
            pts.append(("12co", rec["name"], float(row["p"][0]), float(row["p"][1]), float(row["p"][2]), rec["name"]))
    bridges = [("bridging", None, bx[i], by[i], bz[i], bn[i]) for i in range(len(bn))]
    s = sample(pts + bridges)
    mapped = set(name_map.values())
    alls = [("zucker", None, zx[j], zy[j], zz[j], int(j)) for j in range(len(zn)) if zn[j] in mapped]
    s_all = sample(alls + bridges)
    pt = [("zucker_pt", None, zx[j], zy[j], zz[j], int(j)) for j in range(len(zn)) if zn[j] in set(pt_names)]
    s_pt = sample(pts + bridges + pt)
    return {"S": s, "S_all": s_all, "S+PT": s_pt}


def consistency_table(members, zucker, w_s=None, s_rows=None, w79=None):
    """README 4.11 Part B consistency table: per named row the candidates and kept sightlines, the mean of the kept
    sightlines minus p, per axis their population SD (ddof 0) over the row's spread (None when the spread is 0),
    the status; with w_s / s_rows (S's weights and each S point's row) the summed weight of the row's points in S,
    next to the row's weight in the 79-row fit (w79: name -> weight)."""
    sx = np.column_stack([np.asarray(zucker[a], float) for a in ("x", "y", "z")])
    out = []
    for rec in members:
        kept = rec["kept"]
        row = {"name": rec["name"], "mapped": rec["mapped"], "n_candidates": len(rec["candidates"]),
               "n_kept": len(kept), "status": rec["status"], "reason": rec["reason"], "absorbed_by": rec["absorbed_by"],
               "absorbed_rows": list(rec.get("absorbed_rows", [])),
               "mean_minus_p": None, "sd_over_spread": None}
        if kept:
            pts = sx[kept]
            row["mean_minus_p"] = [float(a) for a in pts.mean(axis=0) - np.asarray(rec["p"], float)]
            sd = pts.std(axis=0)
            row["sd_over_spread"] = [float(sd[a] / rec["sig"][a]) if rec["sig"][a] > 0 else None for a in range(3)]
        if w_s is not None:
            row["summed_weight_in_S"] = float(sum(w for w, r in zip(w_s, s_rows) if r == rec["name"]))
            row["weight_in_79_row_fit"] = None if w79 is None else float(w79[rec["name"]])
        out.append(row)
    return out


# ---------------------------------------------------------------------------------------------
# Part A: per-object terms

def object_terms(model: W.Model, v):
    """Clouds-only model (sigma fixed): per object s, weight, d^2 and t_i = w_i d_i^2 / (2 sigma^2), with lnL and
    the constant sum_i w_i ln(2 pi sigma^2), so that sum_i t_i = -lnL - constant."""
    if model.setup.sigma_mode != "fixed" or model.setup.clusters or not model.setup.clouds:
        raise ValueError("object_terms needs the clouds-only setup with sigma fixed")
    ev = model.evaluate(v)
    if ev is None:
        return None
    d2 = (ev["co_res"] ** 2).sum(1)
    sig = model.setup.sigma
    w = np.asarray(model.w_co, float)
    t = w * d2 / (2.0 * sig * sig)
    return {"s": ev["wave"]["s"][ev["co_idx"]], "w": w, "d2": d2, "t": t, "lnL": float(ev["lnL"]),
            "constant": float(np.sum(w * math.log(2.0 * math.pi * sig * sig)))}


def top_contributors(names, delta, named_mask, n=10):
    """The n objects with the largest Delta_i, the share of sum max(Delta_i, 0) they carry, and the sums over the
    named rows and the bridges."""
    delta = np.asarray(delta, float)
    named_mask = np.asarray(named_mask, bool)
    order = np.argsort(-delta, kind="stable")[:n]
    pos = np.maximum(delta, 0.0)
    tot = float(pos.sum())
    return {"top": [{"name": str(names[i]), "delta": float(delta[i])} for i in order],
            "share_of_positive_sum": (float(pos[order].sum()) / tot) if tot > 0 else None,
            "positive_sum": tot, "sum_named": float(delta[named_mask].sum()),
            "sum_bridges": float(delta[~named_mask].sum()), "sum_all": float(delta.sum())}


# ---------------------------------------------------------------------------------------------
# Part C: K24's published curve

def curve_compare(curve, pub):
    """Nearest valid grid point of `curve` (dict x, y, z, vz, s over the valid grid points only, in order) for each
    published point pub (n, 4: x, y, z, vz), in x-y and in 3-D. A point whose nearest point is the first or last
    grid point is flagged (end_xy, end_3d)."""
    C2 = np.column_stack([curve["x"], curve["y"]])
    C3 = np.column_stack([curve["x"], curve["y"], curve["z"]])
    pub = np.asarray(pub, float)
    jx = W.closest(pub[:, :2], C2)
    j3 = W.closest(pub[:, :3], C3)
    n = len(C2)
    return {"j_xy": jx, "d_xy": np.hypot(*(pub[:, :2] - C2[jx]).T), "end_xy": (jx == 0) | (jx == n - 1),
            "j_3d": j3, "d_3d": np.sqrt(((pub[:, :3] - C3[j3]) ** 2).sum(1)), "end_3d": (j3 == 0) | (j3 == n - 1),
            "dvz": np.abs(pub[:, 3] - np.asarray(curve["vz"], float)[j3]), "s_xy": np.asarray(curve["s"])[jx],
            "s_3d": np.asarray(curve["s"])[j3]}


def _dist_stats(d):
    d = np.asarray(d, float)
    if len(d) == 0:
        return {"median": None, "p95": None, "max": None}
    return {"median": float(np.percentile(d, 50)), "p95": float(np.percentile(d, 95)), "max": float(np.max(d))}


def curve_label(median_xy, p95_xy, n_excl_xy, n_total, *, match_median=5.0, match_p95=15.0, approx_median=20.0,
                excl_frac=0.10):
    if median_xy is not None and median_xy <= match_median and p95_xy <= match_p95:
        lab = "matches K24's published curve"
    elif median_xy is not None and median_xy <= approx_median:
        lab = "approximately matches"
    else:
        lab = "differs from K24's published curve"
    if n_excl_xy > excl_frac * n_total:
        lab += f" (more than {round(100.0 * excl_frac, 6):g}% of the points lie beyond our curve's ends)"
    return lab


def curve_summary(cmp, *, match_median=5.0, match_p95=15.0, approx_median=20.0, excl_frac=0.10):
    """Part C (i) numbers and label from curve_compare's output."""
    kx, k3 = ~cmp["end_xy"], ~cmp["end_3d"]
    n = len(kx)
    sx, s3 = _dist_stats(cmp["d_xy"][kx]), _dist_stats(cmp["d_3d"][k3])
    lab = curve_label(sx["median"], sx["p95"], int((~kx).sum()), n, match_median=match_median, match_p95=match_p95,
                      approx_median=approx_median, excl_frac=excl_frac)
    return {"n_points": n, "n_excluded_xy": int((~kx).sum()), "n_excluded_3d": int((~k3).sum()),
            "xy": sx, "3d": s3,
            "median_abs_dvz_3d": float(np.median(cmp["dvz"][k3])) if k3.any() else None,
            "first_point": {"s_xy": float(cmp["s_xy"][0]), "s_3d": float(cmp["s_3d"][0]),
                            "end_xy": bool(cmp["end_xy"][0]), "end_3d": bool(cmp["end_3d"][0])},
            "last_point": {"s_xy": float(cmp["s_xy"][-1]), "s_3d": float(cmp["s_3d"][-1]),
                           "end_xy": bool(cmp["end_xy"][-1]), "end_3d": bool(cmp["end_3d"][-1])},
            "label": lab}


def valid_curve(wv):
    vi = np.flatnonzero(wv["valid"])
    return {k: wv[k][vi] for k in ("x", "y", "z", "vz", "s")}


def lsq_model(grid, start_vec, *, c_bounds, c_scale, u1_mode="half"):
    """A Model holding the Part C (ii) parameters (12 shape and anchor parameters plus s_origin; B = 1, w0t = 0)."""
    empty = np.zeros(0)
    data = W.Data(cx=empty, cy=empty, cz=empty, cvz=empty, csig=np.zeros((0, 4)), ox=empty, oy=empty, oz=empty)
    v = np.array(start_vec, float)
    v[W.IDX["B"]] = 1.0
    v[W.IDX["w0t"]] = 0.0
    st = W.Setup(free=W.SHAPE_NAMES + ("s_origin",), clusters=False, clouds=False, u1_mode=u1_mode,
                 uniform={"s_origin": tuple(c_bounds)}, scales={"s_origin": float(c_scale)})
    return W.Model(st, data, grid, base=v)


def curve_ssd(model: W.Model, theta, pts3):
    """Sum over pts3 of the squared 3-D distance to the nearest valid grid point of the curve at theta; None if
    the vector gives no usable curve."""
    wv = W.wave_on_grid(model.full(theta), model.grid, model.setup.u1_mode)
    if wv is None:
        return None
    vi = np.flatnonzero(wv["valid"])
    M = np.column_stack([wv["x"], wv["y"], wv["z"]])[vi]
    j = W.closest(pts3, M)
    return float(((pts3 - M[j]) ** 2).sum())


def curve_lsq(model: W.Model, pts3, *, nm_maxfev, lbfgs_maxfun):
    """README 4.11 Part C (ii): least squares of our curve to the kept published points (equal weights), one start
    (the model's base vector, c = 0 there), fit011.optimise's Nelder-Mead and L-BFGS-B; c bounded by its flat
    prior, the rest unbounded; a vector with no usable curve scores 1e12."""
    pts3 = np.asarray(pts3, float)

    def obj(th):
        v = curve_ssd(model, th, pts3)
        return -np.inf if v is None else -v

    start = model.theta_of(model.base)
    bounds = [tuple(model.setup.uniform[n]) if n in model.setup.uniform else (None, None) for n in model.setup.free]
    ssd0 = curve_ssd(model, start, pts3)
    r = F.optimise(model, start, nm_maxfev=nm_maxfev, lbfgs_maxfun=lbfgs_maxfun, objective=obj, bounds=bounds)
    ssd = -r["value"]
    v = model.full(r["theta"])
    return {"theta": r["theta"], "vector": v, "ssd": ssd, "rms_pc": math.sqrt(ssd / len(pts3)),
            "rms_start_pc": None if ssd0 is None else math.sqrt(ssd0 / len(pts3)), "n_eval": r["n_eval"],
            "n_points": int(len(pts3))}


def sigma_scaled(value, ref):
    """(value - median) / plus if above, / minus if below (ref = (median, plus, minus))."""
    med, plus, minus = ref
    d = value - med
    return d / plus if d > 0 else (d / minus if minus > 0 else float("nan"))


# ---------------------------------------------------------------------------------------------
# Labels and the reading

def d6_m6(diffs):
    """D6 = sum of |sigma-scaled differences| of A, p, delta, s0, gamma, phi; M6 the largest, with its name."""
    a = {k: abs(float(diffs[k])) for k in T1_KEYS}
    name = max(T1_KEYS, key=lambda k: a[k])
    return float(sum(a.values())), a[name], name


def _frac(x):
    """2/3 for 0.666..., 3/2 for 1.5 (the registered wording of the width range)."""
    return str(Fraction(float(x)).limit_denominator(1000))


def fit_status(count, ratio, *, repro_count=5, min_count=3, ratio_range=(2.0 / 3.0, 1.5)):
    """R-CONV's thresholds (README 4.10) applied to one fit: (status, reason)."""
    lo, hi = ratio_range
    ok_w = ratio is not None and bool(np.isfinite(ratio)) and lo <= ratio <= hi
    if count < min_count:
        return "not reproduced", None
    reasons = []
    if count < repro_count:
        reasons.append(f"count {count} of 6 ({min_count}-{repro_count - 1})")
    if not ok_w:
        reasons.append(f"width ratio {ratio:.3f} outside [{_frac(lo)}, {_frac(hi)}]")
    return ("reproduced", None) if not reasons else ("partly reproduced", "; ".join(reasons))


def fit_label(status, what):
    return f"column (3) {status} {what}, post hoc"


def c_reading(halfwidth, max_halfwidth=100.0):
    """README 4.11 Part D: c is data-driven if c-ref's 16-84% half-width of c is at most max_halfwidth."""
    return "data-driven" if halfwidth <= max_halfwidth else "prior-dominated"


def step(status, d6, m6, *, d6_max, m6_max):
    """2: reproduced; 1: partly reproduced with D6 <= d6_max and M6 <= m6_max; 0 otherwise."""
    if status == "reproduced":
        return 2
    if status == "partly reproduced" and d6 <= d6_max and m6 <= m6_max:
        return 1
    return 0


READING_S2 = ("column (3) is reproduced with the reconstructed sightline sample: the difference is consistent with "
              "the input sample")
READING_S1 = "the reconstructed sightline sample accounts for part of the column-(3) difference"
READING_D2 = "the column-(3) difference comes from the origin of s or the Sun's height"
READING_D1 = "the origin of s or the Sun's height accounts for part of the column-(3) difference"
READING_NONE = "the column-(3) difference remains unexplained (input sample, origin and the Sun's height tested)"


def reading(s_fit, c_fit, z_fit, c_driven, *, d6_max, m6_max, c_name="the origin of s free",
            z_name="z☉ = 20.8 pc"):
    """README 4.11 reading. Each *_fit: dict with status, D6, M6. c counts only if c_driven ("data-driven").
    Part D takes whichever of (c) and (z☉) reaches the higher step, naming it (both on a tie)."""
    st = step(s_fit["status"], s_fit["D6"], s_fit["M6"], d6_max=d6_max, m6_max=m6_max)
    if st == 2:
        return {"reading": READING_S2, "from": "S", "variants": []}
    if st == 1:
        return {"reading": READING_S1, "from": "S", "variants": []}
    steps = {c_name: step(c_fit["status"], c_fit["D6"], c_fit["M6"], d6_max=d6_max, m6_max=m6_max)
             if c_driven == "data-driven" else 0,
             z_name: step(z_fit["status"], z_fit["D6"], z_fit["M6"], d6_max=d6_max, m6_max=m6_max)}
    best = max(steps.values())
    if best == 0:
        return {"reading": READING_NONE, "from": None, "variants": []}
    names = [k for k in (c_name, z_name) if steps[k] == best]
    base = READING_D2 if best == 2 else READING_D1
    tag = "variant" if len(names) == 1 else "variants"
    return {"reading": f"{base} ({tag}: {' and '.join(names)})", "from": "D", "variants": names}
