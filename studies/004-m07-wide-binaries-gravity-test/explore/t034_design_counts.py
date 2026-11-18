"""T-034 design counts (README sections 2.1 and 3). This records the server-side COUNT queries of
2026-11-18 and replays them from the cache only: it stops on any cache miss and never queries the
archive. It returns counts only, never rows of stars or pairs.

- `proxy`: pairs per x bin under C26's cuts at distance D. Both stars have parallax_over_error > 40,
  RUWE < 1.25, an RV and BP-RP. The 3-sigma rule applies, 300 AU <= r_sky <= 30 kAU at the weighted
  parallax, and the HR band with the committed c holds. Masses come from M_G. sigma(v~) < 0.1 is
  replaced by an error-only proxy: 4.74/pbar * sqrt(mean proper-motion variance) / v_c.
- `lean`: candidate pairs for query N1 (both parent at 250 pc, both with RV, <= 30 kAU).
- `stars`: parent, RV and FLAME star counts.
Each query runs in 12 declination bands of 15 deg (star b with a 1 deg margin).

Run: python -m astrolab explore 004 --tag t034-design --script explore/t034_design_counts.py
"""
EDGES = [0.1057, 0.2307, 0.5088, 1.0275, 2.0902]
C_HR = 1.590861779261529
BANDS_F = [(-90.0 + 15.0 * i, -90.0 + 15.0 * (i + 1)) for i in range(11)] + [(75.0, 90.0001)]   # proxy queries (as run)
BANDS_I = [(-90 + 15 * i, -90 + 15 * (i + 1)) for i in range(11)] + [(75, 90.0001)]       # lean queries (as run)
PROXY_D = (130, 200, 250)


def proxy_sql(D, rmin, band, poe=40.0, ruwe=1.25):
    p0 = 0.85 * 1000.0 / D
    star = (f"SELECT source_id, ra, dec, parallax, parallax_error, phot_g_mean_mag, bp_rp, pmra_error, pmdec_error "
            f"FROM gaiadr3.gaia_source WHERE parallax > {p0:.5f} AND parallax_over_error > {poe} AND ruwe < {ruwe} "
            f"AND radial_velocity IS NOT NULL AND bp_rp IS NOT NULL")
    sa = star + f" AND dec >= {band[0]} AND dec < {band[1]}"
    sb = star + f" AND dec >= {band[0] - 1.0} AND dec <= {band[1] + 1.0}"
    l1 = (f"SELECT a.parallax AS pa, a.parallax_error AS ea, b.parallax AS pb, b.parallax_error AS eb, "
          f"a.phot_g_mean_mag AS ga, b.phot_g_mean_mag AS gb, a.bp_rp AS ca, b.bp_rp AS cb, "
          f"DISTANCE(POINT(a.ra, a.dec), POINT(b.ra, b.dec)) * 3600.0 AS th, "
          f"(a.pmra_error*a.pmra_error + a.pmdec_error*a.pmdec_error + b.pmra_error*b.pmra_error + b.pmdec_error*b.pmdec_error) / 2.0 AS s2 "
          f"FROM ({sa}) AS a JOIN ({sb}) AS b "
          f"ON 1 = CONTAINS(POINT(b.ra, b.dec), CIRCLE(a.ra, a.dec, 30000.0 * a.parallax * 1.12 / 1000.0 / 3600.0)) "
          f"WHERE a.source_id < b.source_id AND ABS(a.parallax - b.parallax) < 3 * SQRT(a.parallax_error*a.parallax_error + b.parallax_error*b.parallax_error)")
    l2 = f"SELECT (eb*eb*pa + ea*ea*pb) / (ea*ea + eb*eb) AS pbar, th, s2, ga, gb, ca, cb FROM ({l1}) AS q1"
    l3 = (f"SELECT pbar, th * 1000.0 / pbar AS rsky, s2, ca, cb, ga + 5.0 * LOG10(pbar / 100.0) AS mga, "
          f"gb + 5.0 * LOG10(pbar / 100.0) AS mgb FROM ({l2}) AS q2 WHERE pbar > {1000.0 / D:.5f}")
    l4 = (f"SELECT pbar, rsky, s2, POWER(10.0, 0.0725 * (4.67 - mga)) AS ma, POWER(10.0, 0.0725 * (4.67 - mgb)) AS mb "
          f"FROM ({l3}) AS q3 WHERE rsky >= {rmin} AND rsky <= 30000.0 "
          f"AND ca > 0.5 AND ca < 3.5 AND cb > 0.5 AND cb < 3.5 AND mga > 4 AND mga < 14 AND mgb > 4 AND mgb < 14 "
          f"AND mga > 3.3 * ca + {C_HR} AND mga < 3.3 * ca + {C_HR + 0.8} AND mgb > 3.3 * cb + {C_HR} AND mgb < 3.3 * cb + {C_HR + 0.8}")
    l5 = ("SELECT rsky, s2, pbar, ma + mb + 0.05 * (ABS(0.7 - ma) + 0.7 - ma) / (2.0 * ABS(0.7 - ma)) "
          f"+ 0.05 * (ABS(0.7 - mb) + 0.7 - mb) / (2.0 * ABS(0.7 - mb)) AS m FROM ({l4}) AS q4")
    l6 = ("SELECT rsky / (7030.492 * SQRT(m)) AS x, 4.740470464 / pbar * SQRT(s2) / (29.7847 * SQRT(m / rsky)) AS sv "
          f"FROM ({l5}) AS q5")
    step = " + ".join(f"(ABS(x - {e}) + x - {e}) / (2.0 * ABS(x - {e}))" for e in EDGES)
    return (f"SELECT bin, COUNT(*) AS n FROM (SELECT FLOOR({step} + 0.5) AS bin FROM ({l6}) AS q6 WHERE sv < 0.1) AS g "
            f"GROUP BY bin ORDER BY bin")


def lean_sql(plx, band):
    star = (f"SELECT source_id, ra, dec, parallax, parallax_error FROM gaiadr3.gaia_source "
            f"WHERE parallax > {plx} AND parallax_over_error > 40 AND radial_velocity IS NOT NULL")
    sa = star + f" AND dec >= {band[0]} AND dec < {band[1]}"
    sb = star + f" AND dec >= {band[0] - 1} AND dec <= {band[1] + 1}"
    pbar = ("((b.parallax_error*b.parallax_error*a.parallax + a.parallax_error*a.parallax_error*b.parallax)"
            " / (a.parallax_error*a.parallax_error + b.parallax_error*b.parallax_error))")
    return (f"SELECT COUNT(*) AS n FROM ({sa}) AS a JOIN ({sb}) AS b ON 1 = CONTAINS(POINT(b.ra, b.dec), "
            f"CIRCLE(a.ra, a.dec, 30000.0 * a.parallax * 1.12 / 1000.0 / 3600.0)) "
            f"WHERE a.source_id < b.source_id AND ABS(a.parallax - b.parallax) < 3 * SQRT(a.parallax_error*a.parallax_error "
            f"+ b.parallax_error*b.parallax_error) AND DISTANCE(POINT(a.ra, a.dec), POINT(b.ra, b.dec)) * 3600.0 * 1000.0 / {pbar} <= 30000.0")


def star_sqls(plx):
    w = f"parallax > {plx} AND parallax_over_error > 40"
    return {"parent": f"SELECT COUNT(*) AS n FROM gaiadr3.gaia_source WHERE {w}",
            "parent_rv": f"SELECT COUNT(*) AS n FROM gaiadr3.gaia_source WHERE {w} AND radial_velocity IS NOT NULL",
            "parent_rv_flame": ("SELECT COUNT(*) AS n FROM gaiadr3.gaia_source AS g JOIN gaiadr3.astrophysical_parameters AS ap "
                                f"ON ap.source_id = g.source_id WHERE g.parallax > {plx} AND g.parallax_over_error > 40 "
                                "AND g.radial_velocity IS NOT NULL AND ap.mass_flame IS NOT NULL")}


def main(ctx):
    from astrolab import cache, fetch
    from astrolab.services import tap_url
    url = tap_url("gaia")

    def cached(q, max_rows):
        if cache.get(cache.key_for("tap", {"url": url, "adql": fetch._normalize_adql(q)}), ".parquet") is None:
            raise RuntimeError("cache miss; stop (this script never queries the archive)")
        return ctx.tap(q, "gaia", label="t034 count (cache)", max_rows=max_rows, mode="async")

    out = {"proxy": {}, "lean_pairs": {}, "stars": {}}
    for D in PROXY_D:
        tot = [0] * 6
        for band in BANDS_F:
            df = cached(proxy_sql(D, 300.0, band), 10)
            for b, n in zip(df["bin"], df["n"]):
                tot[int(round(b))] += int(n)
        out["proxy"][f"{D}pc"] = tot
    for name, plx in (("200pc", 4.3478), ("250pc", 3.4783)):
        out["lean_pairs"][name] = sum(int(cached(lean_sql(plx, b), 1)["n"].iloc[0]) for b in BANDS_I)
        out["stars"][name] = {k: int(cached(q, 1)["n"].iloc[0]) for k, q in star_sqls(plx).items()}
    ctx.log(str(out))
    ctx.save("t034_design_counts", out)
    return out
