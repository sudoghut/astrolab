"""ADQL builders for study 004 (README section 3). Pure string functions; run.py executes them through
ctx.count / ctx.tap. Star a is restricted to a half-open region, star b to that region's search box.
"""
from __future__ import annotations

DEG_PER_PC_PER_MAS = 1.0 / 1000.0 * 180.0 / 3.141592653589793 * 1.0   # theta[deg] = r[pc] * plx[mas] / 1000 * 180/pi
PAIR_PC = 0.5


def _ra_clause(col, lo, hi, half_open=False):
    if lo == 0.0 and hi == 360.0:
        return "1=1"
    upper = "<" if half_open else "<="
    if lo <= hi:
        return f"({col} >= {lo} AND {col} {upper} {hi})"
    return f"({col} >= {lo} OR {col} {upper} {hi})"


def _dec_clause(col, lo, hi, half_open=False):
    if half_open and hi < 90.0:
        return f"({col} >= {lo} AND {col} < {hi})"
    return f"({col} >= {lo} AND {col} <= {hi})"


def star_a_where(region, parent, near=False, near_plx=100.0):
    w = [parent, _ra_clause("ra", region["ra0"], region["ra1"], True),
         _dec_clause("dec", region["dec0"], region["dec1"], True)]
    w.append(f"parallax >= {near_plx}" if near else f"parallax < {near_plx}")
    return " AND ".join(w)


def star_b_where(region, b_filter, near=False):
    if near:
        return b_filter
    return " AND ".join([b_filter, _ra_clause("ra", region["bra0"], region["bra1"]),
                         _dec_clause("dec", region["bdec0"], region["bdec1"])])


DEGROUP_PC = 100000.0 / 206264.806     # C26 section 3.2.1: 100 kAU


def pair_conditions(vcap_kms=None, radius_pc=PAIR_PC):
    """WHERE conditions on the joined subqueries a, b (pbar: weighted parallax)."""
    pbar = ("((b.parallax_error*b.parallax_error*a.parallax + a.parallax_error*a.parallax_error*b.parallax)"
            " / (a.parallax_error*a.parallax_error + b.parallax_error*b.parallax_error))")
    conds = [
        "ABS(a.parallax - b.parallax) < 3 * SQRT(a.parallax_error*a.parallax_error"
        " + b.parallax_error*b.parallax_error)",
        f"DISTANCE(POINT(a.ra, a.dec), POINT(b.ra, b.dec)) * 3.141592653589793 / 180.0 * 1000.0 / {pbar}"
        f" <= {radius_pc}",
    ]
    if vcap_kms is not None:
        conds.append(f"4.740470464 * SQRT((a.pmra - b.pmra)*(a.pmra - b.pmra) + (a.pmdec - b.pmdec)*(a.pmdec - b.pmdec))"
                     f" / {pbar} < {vcap_kms}")
    return conds


def _circle(factor=1.12, radius_pc=PAIR_PC):
    # search circle at least as large as the exact rule: pbar <= ~1.11 a.parallax under the 3-sigma rule
    return f"CIRCLE(a.ra, a.dec, {radius_pc} * a.parallax * {factor} / 1000.0 * 180.0 / 3.141592653589793)"


A_COLS = ["source_id", "ra", "dec", "parallax", "parallax_error", "phot_g_mean_mag", "bp_rp", "ruwe",
          "ipd_frac_multi_peak", "rv_method_used"]
B1_COLS = ["source_id", "pmra", "pmdec", "pmra_error", "pmdec_error", "parallax_pmra_corr",
           "parallax_pmdec_corr", "pmra_pmdec_corr", "radial_velocity", "radial_velocity_error"]
NEED_COLS = ["source_id", "ra", "dec", "parallax", "parallax_error", "pmra", "pmdec"]


def _sub(where, cols, alias):
    return f"(SELECT {', '.join(cols)} FROM gaiadr3.gaia_source WHERE {where}) AS {alias}"


def pair_query(region, parent, vcap_kms, select, near=False, extra_where=()):
    """A1/B1 pair query; `select` is the SELECT list ('COUNT(*) AS n' for counts)."""
    cols = sorted(set(A_COLS) | ({"pmra", "pmdec"} if vcap_kms is not None else set())
                  | (set(B1_COLS) if "radial_velocity" in select or any("radial_velocity" in e for e in extra_where)
                     else set()))
    a = _sub(star_a_where(region, parent, near), cols, "a")
    b = _sub(star_b_where(region, parent, near), cols, "b")
    conds = ["a.source_id < b.source_id"] + pair_conditions(vcap_kms) + list(extra_where)
    # a.source_id < b.source_id would lose pairs whose lower id lies in the margin; the margin star
    # is then 'a' in its own region, so each pair is still found exactly once over all regions.
    return (f"SELECT {select} FROM {a} JOIN {b} "
            f"ON 1 = CONTAINS(POINT(b.ra, b.dec), {_circle()}) "
            f"WHERE {' AND '.join(conds)}")


def a1_select():
    out = []
    for s in ("a", "b"):
        out += [f"{s}.{c} AS {c}_{s}" for c in A_COLS]
    return ", ".join(out)


def b1_select():
    out = ["a.source_id AS source_id_a", "b.source_id AS source_id_b"]
    for s in ("a", "b"):
        out += [f"{s}.{c} AS {c}_{s}" for c in B1_COLS if c != "source_id"]
    return ", ".join(out)


def b1_extra(rsky_max_kau=30.0):
    pbar = ("((b.parallax_error*b.parallax_error*a.parallax + a.parallax_error*a.parallax_error*b.parallax)"
            " / (a.parallax_error*a.parallax_error + b.parallax_error*b.parallax_error))")
    return [f"DISTANCE(POINT(a.ra, a.dec), POINT(b.ra, b.dec)) * 3.141592653589793 / 180.0 * 1000.0 / {pbar}"
            f" * 206.264806 <= {rsky_max_kau}",
            "a.radial_velocity IS NOT NULL", "b.radial_velocity IS NOT NULL"]


def neighbour_query(region, parent, neighbour, select, near=False):
    """A2: per parent star in the region, count neighbours (both orientations, no velocity rule)."""
    cols = ["source_id", "ra", "dec", "parallax", "parallax_error"]
    a = _sub(star_a_where(region, parent, near), cols, "a")
    b = _sub(star_b_where(region, neighbour, near), cols, "b")
    conds = ["a.source_id <> b.source_id"] + pair_conditions(None, DEGROUP_PC)
    inner = (f"SELECT a.source_id AS source_id, COUNT(*) AS n, MIN(b.source_id) AS first_neighbour "
             f"FROM {a} JOIN {b} ON 1 = CONTAINS(POINT(b.ra, b.dec), {_circle(radius_pc=DEGROUP_PC)}) "
             f"WHERE {' AND '.join(conds)} GROUP BY a.source_id")
    if select == "count":
        return f"SELECT COUNT(*) AS n FROM ({inner}) AS g"
    return inner


def flame_query(region, parent, select, near=False):
    """A3: FLAME masses of the region's parent stars (velocity-free)."""
    sub = f"(SELECT source_id FROM gaiadr3.gaia_source WHERE {star_a_where(region, parent, near)}) AS g"
    inner = (f"FROM {sub} JOIN gaiadr3.astrophysical_parameters AS ap ON ap.source_id = g.source_id "
             f"WHERE ap.mass_flame IS NOT NULL")
    if select == "count":
        return f"SELECT COUNT(*) AS n {inner}"
    return f"SELECT g.source_id AS source_id, ap.mass_flame AS mass_flame {inner}"
