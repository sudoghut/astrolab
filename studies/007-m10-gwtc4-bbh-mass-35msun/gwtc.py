"""Event-list parsing, sample selection and toy mass-spectrum fits (README section 4).

Pure functions; tunable values are passed in as arguments (AGENTS.md section 2).
"""
import datetime
import io
import json
import re
import tarfile

import numpy as np
from scipy import optimize, stats

GPS_EPOCH = datetime.datetime(1980, 1, 6, tzinfo=datetime.timezone.utc)
LEAP_SECONDS_SINCE_GPS_EPOCH = 18      # valid from 2017-01-01 onwards (covers O4a)
NAME_RE = re.compile(r"GW(\d{6})(?:_(\d{6}))?")


# ---------------------------------------------------------------- parsing ----

def load_list(path):
    """GWOSC event-API list JSON -> {commonName: row} (latest version kept by name)."""
    with open(path, "rb") as fh:
        raw = json.loads(fh.read().decode("utf-8"))
    events = raw.get("events", raw)
    rows = {}
    for key, ev in events.items():
        name = ev.get("commonName") or key.split("-v")[0]

        def g(field):
            v = ev.get(field)
            return None if v is None else float(v)

        row = {"name": name, "key": key, "version": ev.get("version"), "far": g("far"),
               "gps": g("GPS"), "m1": g("mass_1_source"), "m1_lo": g("mass_1_source_lower"),
               "m1_hi": g("mass_1_source_upper"), "m2": g("mass_2_source"),
               "m2_lo": g("mass_2_source_lower"), "mtot": g("total_mass_source")}
        prev = rows.get(name)
        if prev is None or (row["version"] or 0) >= (prev["version"] or 0):
            rows[name] = row
    return rows


def tar_names(path, max_member_bytes=2 ** 20, max_members=1000):
    """Event names (GWyymmdd_hhmmss or GWyymmdd) found in a small tar, read in memory."""
    names, members = set(), []
    with tarfile.open(path, "r:*") as tf:
        infos = tf.getmembers()
        if len(infos) > max_members:
            raise ValueError(f"tar has {len(infos)} members")
        for info in infos:
            members.append(info.name)
            if ".." in info.name or info.name.startswith("/") or not info.isfile():
                continue
            fh = tf.extractfile(info)
            data = fh.read(max_member_bytes + 1) if fh else b""
            if len(data) > max_member_bytes:
                raise ValueError(f"member {info.name} too large")
            for m in NAME_RE.finditer(data.decode("utf-8", errors="replace")):
                names.add(m.group(0))
    return names, members


def name_to_gps(name):
    """GWyymmdd_hhmmss -> GPS seconds (UTC + leap seconds); None for date-only names."""
    m = NAME_RE.fullmatch(name)
    if not m or not m.group(2):
        return None
    dt = datetime.datetime.strptime(m.group(1) + m.group(2), "%y%m%d%H%M%S").replace(tzinfo=datetime.timezone.utc)
    return (dt - GPS_EPOCH).total_seconds() + LEAP_SECONDS_SINCE_GPS_EPOCH


# -------------------------------------------------------------- selection ----

def lower_bound(value, offset):
    if value is None or offset is None:
        return None
    return value + offset          # offsets are signed (negative)


def passes(row, far_max, m_min, mass_bound):
    """FAR and mass cuts; returns (ok, reason)."""
    if row["far"] is None or row["m1"] is None or row["m2"] is None:
        return False, "no PE or FAR"
    if row["far"] >= far_max:
        return False, f"far {row['far']:.3g} >= {far_max}"
    if mass_bound == "p90":
        b1, b2 = lower_bound(row["m1"], row["m1_lo"]), lower_bound(row["m2"], row["m2_lo"])
        if b1 is None or b2 is None:
            return False, "no mass bounds"
    else:
        b1, b2 = row["m1"], row["m2"]
    if not (b1 > m_min and b2 > m_min):
        return False, f"mass bound {min(b1, b2):.2f} <= {m_min}"
    return True, ""


def select_o4a(rows, gps_lo, gps_hi, far_max, m_min, mass_bound, exclude):
    sel, reasons = {}, {}
    for name, row in rows.items():
        if row["gps"] is None or not (gps_lo <= row["gps"] < gps_hi):
            reasons[name] = "outside O4a"
            continue
        if name in exclude:
            reasons[name] = "excluded (P26)"
            continue
        ok, why = passes(row, far_max, m_min, mass_bound)
        if ok:
            sel[name] = row
        else:
            reasons[name] = why
    return sel, reasons


def merge_lists(lists_in_precedence):
    """Union by name; earlier lists take precedence."""
    out = {}
    for rows in lists_in_precedence:
        for name, row in rows.items():
            out.setdefault(name, row)
    return out


def select_o3(merged, far_max, m_min, mass_bound):
    sel, reasons = {}, {}
    for name, row in merged.items():
        ok, why = passes(row, far_max, m_min, mass_bound)
        if ok:
            sel[name] = row
        else:
            reasons[name] = why
    return sel, reasons


# ------------------------------------------------------------- R2 and R3 ----

def vt(m, slope, m_t):
    m = np.asarray(m, dtype=float)
    if m_t is None:
        return (m / 10.0) ** slope
    return np.where(m < m_t, (m / 10.0) ** slope, (m_t / 10.0) ** slope)


def r2_prediction(lam1, slope, m_t, m_lo, m_split, m_hi, n_grid):
    grid = np.linspace(m_lo, m_hi, n_grid)
    p = grid ** (-lam1) * vt(grid, slope, m_t)
    lo = grid < m_split
    i_lo = np.trapz(np.where(lo, p, 0.0), grid)
    i_hi = np.trapz(np.where(~lo, p, 0.0), grid)
    return float(i_hi / (i_lo + i_hi))


def binom_le(k, n, f):
    return float(stats.binom.cdf(k, n, f))


def bpl(m, lam1, lam2, m_break):
    m = np.asarray(m, dtype=float)
    return np.where(m < m_break, (m / m_break) ** (-lam1), (m / m_break) ** (-lam2))


def _norm(f, grid):
    return f / np.trapz(f, grid)


def model_density(theta, kind, grid, slope, m_t):
    """Observed-frame density on the grid, normalised on [grid[0], grid[-1]]."""
    if kind == "A":
        lam1, lam2, mb = theta
        f = _norm(bpl(grid, lam1, lam2, mb), grid)
    else:
        lam1, lam2, mb, mu, sig, w = theta
        f = (1 - w) * _norm(bpl(grid, lam1, lam2, mb), grid) + w * _norm(stats.norm.pdf(grid, mu, sig), grid)
    q = f * vt(grid, slope, m_t)
    return q / np.trapz(q, grid)


def nll(theta, kind, masses, grid, slope, m_t):
    dens = model_density(theta, kind, grid, slope, m_t)
    vals = np.interp(masses, grid, dens)
    if np.any(vals <= 0) or not np.all(np.isfinite(vals)):
        return 1e30
    return float(-np.sum(np.log(vals)))


BOUNDS_A = [(-2.0, 10.0), (-2.0, 10.0), (20.0, 60.0)]
BOUNDS_B = BOUNDS_A + [(25.0, 45.0), (1.0, 10.0), (0.0, 1.0)]


def fit(kind, masses, grid, slope, m_t, n_starts, seed, extra_starts=()):
    bounds = BOUNDS_A if kind == "A" else BOUNDS_B
    rng = np.random.default_rng(seed)
    starts = [np.array([rng.uniform(lo, hi) for lo, hi in bounds]) for _ in range(n_starts)]
    starts += [np.asarray(s, dtype=float) for s in extra_starts]
    best = None
    for x0 in starts:
        res = optimize.minimize(nll, x0, args=(kind, masses, grid, slope, m_t), method="L-BFGS-B", bounds=bounds)
        if best is None or res.fun < best.fun:
            best = res
    theta = best.x.tolist()
    at_bound = [bool(np.isclose(v, lo) or np.isclose(v, hi)) for v, (lo, hi) in zip(theta, bounds)]
    return {"theta": theta, "nll": float(best.fun), "at_bound": at_bound}
