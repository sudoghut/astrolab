"""T-043 (post hoc, exploration; no verdict): the chance-neighbour rate of the relaxed degrouping rule,
measured with shifted positions and without velocities.

For every R5 parent RV star that belongs to an N1 pair (README 2.1), the N2 neighbour query is repeated
with the star's position moved by SHIFT_DEG in declination (towards the equator; RA, parallax and
parallax error unchanged). Neighbours found around the shifted position, with the same selection,
100 kAU radius and 3-sigma parallax rule, are unrelated to the star: their number is the chance
neighbour count at that distance and sky density. Per pair, "both stars have no shifted neighbour" is a
shifted-field proxy for the survival expected if degrouping removed pairs only through chance
neighbours (it does not identify which real neighbours are chance alignments); it is compared with
the observed relaxed-rule survival (N2: both stars' only neighbour is the partner), by distance shell
and Galactic latitude.

Data: N1 and N2 are the R5 queries of 2026-11-18 (cache hits when still cached). The shifted query is
new: per region, a server count first (split in RA above the caps, as section 3), then the rows
(source_id, n), about 40 bytes per parent star with at least one shifted neighbour (about 100 s per
query on the archive). Parents within 29.9 pc (parallax >= 33.4 mas) are excluded on the server:
beyond it the shifted and true 100 kAU circles are disjoint and the shifted circle stays inside the
region's star-b box; the near-star region (d < 10 pc) is not queried. A region whose N1, N2 or shifted
query fails is recorded and skipped, and a pair is used only if both stars lie in regions
whose queries all worked (a pair's star b can lie in another region's margin).

Run: python -m astrolab explore 004 --tag t043-shift --script explore/t043_shifted_neighbours.py
"""
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd

import queries as Q
import r5
import run
import wb

SHIFT_DEG = 2.0                 # circle (<= 1.24 deg beyond 25 pc) + shift < the 3.3 deg declination margin
PLX_MAX = 33.4                  # parents beyond 29.9 pc: the exact 100 kAU neighbourhoods (radius <= 1.0 deg) of the
                                # true and shifted positions are disjoint (the 1.12x search circles may overlap)
SHELLS = [(29.9, 130.0), (130.0, 150.0), (150.0, 250.0)]
CUMULATIVE = [130.0, 150.0, 250.0]  # the referee's cumulative bins (d < 130, 150, 250 pc; beyond 29.9 pc)
LAT_BINS = [(0.0, 10.0), (10.0, 40.0), (40.0, 90.0)]
SEP_BINS = [(300.0, 1000.0), (1000.0, 30000.0)]
WORKERS = 4                     # archive-bound threads; local CPU use is small
BYTES_ROW = 40
REGION_LIMIT = None             # smoke tests only: the first N regions


def shift_for(region):
    """Declination shift towards the equator (no wrap through a pole)."""
    return -SHIFT_DEG if region["dec0"] >= 0.0 else SHIFT_DEG


def shifted_query(region, near_b, select, shift):
    """N2 (restricted to N1 members) with star a's position moved by `shift` degrees in declination."""
    cols = ["source_id", "ra", "dec", "parallax", "parallax_error"]
    aw = Q.star_a_where(region, r5.PARENT_RV, False) + f" AND parallax < {PLX_MAX}" + \
        f" AND source_id IN ({r5.member_subquery(region, False, near_b)})"
    a = Q._sub(aw, cols, "a")
    b = Q._sub(Q.star_b_where(region, r5.NEIGHBOUR, False), cols, "b")
    pbar = ("((b.parallax_error*b.parallax_error*a.parallax + a.parallax_error*a.parallax_error*b.parallax)"
            " / (a.parallax_error*a.parallax_error + b.parallax_error*b.parallax_error))")
    dec = f"(a.dec + ({shift}))"
    conds = ["a.source_id <> b.source_id",
             "ABS(a.parallax - b.parallax) < 3 * SQRT(a.parallax_error*a.parallax_error"
             " + b.parallax_error*b.parallax_error)",
             f"DISTANCE(POINT(a.ra, {dec}), POINT(b.ra, b.dec)) * 3.141592653589793 / 180.0 * 1000.0 / {pbar}"
             f" <= {Q.DEGROUP_PC}"]
    circ = (f"CIRCLE(a.ra, {dec}, {Q.DEGROUP_PC} * a.parallax * 1.12 / 1000.0 * 180.0 / 3.141592653589793)")
    inner = (f"SELECT a.source_id AS source_id, COUNT(*) AS n FROM {a} JOIN {b} "
             f"ON 1 = CONTAINS(POINT(b.ra, b.dec), {circ}) WHERE {' AND '.join(conds)} GROUP BY a.source_id")
    return f"SELECT COUNT(*) AS n FROM ({inner}) AS g" if select == "count" else inner


def in_regions(regs, ra, dec, plx):
    """True where a star lies in one of the (non-near) regions as star a: half-open RA and declination
    boxes (declination closed at +90), parallax below the near-star limit (queries.star_a_where)."""
    ra, dec, plx = np.asarray(ra, float), np.asarray(dec, float), np.asarray(plx, float)
    hit = np.zeros(len(ra), bool)
    for g in regs:
        if g["ra0"] == 0.0 and g["ra1"] == 360.0:
            m_ra = np.ones(len(ra), bool)
        elif g["ra0"] <= g["ra1"]:
            m_ra = (ra >= g["ra0"]) & (ra < g["ra1"])
        else:
            m_ra = (ra >= g["ra0"]) | (ra < g["ra1"])
        m_dec = (dec >= g["dec0"]) & ((dec < g["dec1"]) if g["dec1"] < 90.0 else (dec <= g["dec1"]))
        hit |= m_ra & m_dec
    return hit & (plx < 100.0)


def galactic_b(ra, dec):
    from astropy.coordinates import SkyCoord
    import astropy.units as u
    return SkyCoord(ra=np.asarray(ra) * u.deg, dec=np.asarray(dec) * u.deg, frame="icrs").galactic.b.deg


def summarise(pairs, mask):
    sub = pairs[mask]
    n = int(len(sub))
    if n == 0:
        return {"pairs": 0}
    return {"pairs": n,
            "observed_survival": float(sub["survives"].mean()),
            "no_shifted_neighbour_fraction": float(sub["no_chance"].mean()),   # shifted-field proxy
            "mean_extra_real_neighbours_per_star": float(np.mean(np.r_[sub["extra_a"], sub["extra_b"]])),
            "mean_chance_neighbours_per_star": float(np.mean(np.r_[sub["chance_a"], sub["chance_b"]])),
            "frac_stars_with_chance_neighbour": float(np.mean(np.r_[sub["chance_a"], sub["chance_b"]] > 0))}


def main(ctx):
    P = dict(run.PARAMS)
    R = {k: P[k] for k in P if k.startswith("r5_")}
    nb = P["near_b"]
    budget = run.Budget(float(P["budget_bytes"]))
    regions = [(name, r) for name, r, near in run._regions(P) if not near]
    if REGION_LIMIT:
        regions = regions[:REGION_LIMIT]

    def one(item):
        name, r = item
        try:
            _, d1 = run._r5_region(ctx, P, "N1", name, r, False, budget,
                                   lambda rr, nn, sel: r5.n1_query(rr, nn, nb, sel), R["r5_bytes_n1"])
            _, d2, _ = run._r5_with_fallback(
                ctx, P, "N2", name, r, False, budget,
                lambda rr, nn, sel: r5.neighbour_query(rr, nn, nb, r5.NEIGHBOUR, sel, True),
                lambda rr, nn, sel: r5.neighbour_query(rr, nn, nb, r5.NEIGHBOUR, sel, False), R["r5_bytes_n2"])
        except run._stops():
            raise
        except Exception as e:  # noqa: BLE001 - N1/N2 not obtained: record the region as failed
            if not (run._archive_error(e) or isinstance(e, run.DataNotObtained)):
                raise
            return name, None, None, None, f"N1/N2 {type(e).__name__}: {str(e)[:200]}"
        build = lambda rr, nn, sel: shifted_query(rr, nb, sel, shift_for(rr))
        try:
            _, d3 = run._r5_region(ctx, P, "T043", name, r, False, budget, build, BYTES_ROW)   # count first
            err = None
        except run._stops():
            raise
        except Exception as e:  # noqa: BLE001 - archive refusal or timeout: record and skip
            if not run._archive_error(e):
                raise                     # a code defect or count mismatch stops the run
            d3, err = None, f"{type(e).__name__}: {str(e)[:200]}"
        return name, d1, d2, d3, err

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        out = list(ex.map(one, regions))
    failed = {name: err for name, _, _, _, err in out if err}
    ok_names = {name for name, _, _, _, err in out if not err}
    # a pair is used only if both stars lie in regions whose queries all worked (a pair's star b can lie
    # in another region's margin, and that region may have failed); a star without an N2 row there has
    # no true neighbour (not survival) and one without a shifted row no shifted neighbour
    ok_regions = [r for name, r in regions if name in ok_names]
    ctx.log(f"regions: {len(out)}; shifted query failed in {len(failed)}: {dict(list(failed.items())[:3])}")

    n1 = pd.concat([d1 for name, d1, _, _, _ in out if name in ok_names and len(d1)], ignore_index=True)
    n2 = pd.concat([d2 for name, _, d2, _, _ in out if name in ok_names and len(d2)], ignore_index=True)
    sh = [d3 for name, _, _, d3, _ in out if name in ok_names and d3 is not None and len(d3)]
    sh = pd.concat(sh, ignore_index=True) if sh else pd.DataFrame({"source_id": [], "n": []})
    for name, df in (("N2", n2), ("shifted", sh)):
        if df["source_id"].duplicated().any():
            raise RuntimeError(f"{name} table has duplicate source_id rows; stop")

    n1 = n1.iloc[wb.canonical_pairs(n1["source_id_a"].to_numpy(), n1["source_id_b"].to_numpy())].reset_index(drop=True)
    pb, _, _ = wb.weighted_parallax(n1["parallax_a"].values, n1["parallax_error_a"].values,
                                    n1["parallax_b"].values, n1["parallax_error_b"].values)
    n1 = n1.assign(pbar=pb, rsky=wb.sky_separation_au(n1["ra_a"].values, n1["dec_a"].values,
                                                      n1["ra_b"].values, n1["dec_b"].values, pb))
    # R5's velocity-free server cuts (N4): pbar > 4 mas, r_sky >= 300 AU, RUWE < 1.25; and beyond 29.9 pc
    cut = ((n1["pbar"] > 4.0) & (n1["rsky"] >= 300.0) & (n1["ruwe_a"] < 1.25) & (n1["ruwe_b"] < 1.25)
           & (n1["parallax_a"] < PLX_MAX) & (n1["parallax_b"] < PLX_MAX))
    pairs = n1[cut].copy()
    both_ok = (in_regions(ok_regions, pairs["ra_a"].values, pairs["dec_a"].values, pairs["parallax_a"].values)
               & in_regions(ok_regions, pairs["ra_b"].values, pairs["dec_b"].values, pairs["parallax_b"].values))
    dropped_failed = int((~both_ok).sum())
    pairs = pairs[both_ok].copy()
    real = {int(s): (int(n), int(f)) for s, n, f in zip(n2["source_id"], n2["n"], n2["first_neighbour"])}
    chance = {int(s): int(n) for s, n in zip(sh["source_id"], sh["n"])}
    ia, ib = pairs["source_id_a"].astype("int64").to_numpy(), pairs["source_id_b"].astype("int64").to_numpy()

    def single(s, partner):
        v = real.get(int(s))
        return v is not None and v[0] == 1 and v[1] == int(partner)
    pairs["survives"] = [single(p, q) and single(q, p) for p, q in zip(ia, ib)]
    pairs["extra_a"] = [max(real.get(int(p), (0, 0))[0] - 1, 0) for p in ia]
    pairs["extra_b"] = [max(real.get(int(q), (0, 0))[0] - 1, 0) for q in ib]
    pairs["chance_a"] = [chance.get(int(p), 0) for p in ia]
    pairs["chance_b"] = [chance.get(int(q), 0) for q in ib]
    pairs["no_chance"] = (pairs["chance_a"] == 0) & (pairs["chance_b"] == 0)
    pairs["d"] = 1000.0 / pairs["pbar"]
    pairs["absb"] = np.abs(galactic_b(pairs["ra_a"].values, pairs["dec_a"].values))

    res = {"settings": {"shift_deg": SHIFT_DEG, "plx_max": PLX_MAX, "shells_pc": SHELLS, "lat_bins_deg": LAT_BINS,
                        "sep_bins_au": SEP_BINS, "neighbour": r5.NEIGHBOUR, "parent": r5.PARENT_RV,
                        "degroup_pc": Q.DEGROUP_PC},
           "regions": len(out), "failed_regions": failed, "pairs_total": int(len(pairs)),
           "n_shifted_rows": int(len(sh)), "pairs_dropped_not_in_ok_regions": dropped_failed,
           "note": ("latitude bins use star a's true (unshifted) position; per-star means count a star once per pair it belongs to; the declination shift moves |b| by "
                    "up to 2 deg and its direction depends on the region (pairs straddling dec 0 get opposite "
                    "shifts); the shifted field also samples moving groups wider than 2 deg as 'chance'"),
           "cumulative": {}, "by_shell": {}, "by_shell_lat": {}, "by_shell_sep": {}}
    for hi in CUMULATIVE:
        res["cumulative"][f"29.9-{hi:g}"] = summarise(pairs, pairs["d"] < hi)
    for lo, hi in SHELLS:
        m = (pairs["d"] >= lo) & (pairs["d"] < hi)
        key = f"{lo:g}-{hi:g}"
        res["by_shell"][key] = summarise(pairs, m)
        for blo, bhi in LAT_BINS:
            res["by_shell_lat"][f"{key}|b{blo:g}-{bhi:g}"] = summarise(
                pairs, m & (pairs["absb"] >= blo) & (pairs["absb"] < bhi))
        for slo, shi in SEP_BINS:
            res["by_shell_sep"][f"{key}|s{slo:g}-{shi:g}"] = summarise(
                pairs, m & (pairs["rsky"] >= slo) & (pairs["rsky"] < shi))
        ctx.log(f"{key} pc: {res['by_shell'][key]}")
    ctx.save("t043_shifted_neighbours", res)
    return res
