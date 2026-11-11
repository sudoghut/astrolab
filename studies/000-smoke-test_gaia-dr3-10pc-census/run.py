"""Smoke test: Gaia DR3 census of the 10 pc neighbourhood + server-side all-sky density.

Exercises the whole pipeline: guarded TAP queries, caching, provenance,
server-side aggregation, results JSON, and the study web page.

Run with:  python -m astrolab run 000
"""
import numpy as np
from astropy import units as u
from astropy_healpix import HEALPix

NEARBY_ADQL = """
SELECT source_id, ra, dec, l, b, parallax, parallax_over_error, pmra, pmdec,
       radial_velocity, phot_g_mean_mag, bp_rp, ruwe
FROM gaiadr3.gaia_source
WHERE parallax > 100
"""

# Server-side aggregation: ~1e6 bright stars -> 768 numbers (HEALPix level 3).
# In gaia_source, source_id // 2^35 is the level-12 nested HEALPix index;
# dividing by 4^(12-3) more gives level 3.
DENSITY_LEVEL = 3
DENSITY_ADQL = f"""
SELECT GAIA_HEALPIX_INDEX({DENSITY_LEVEL}, source_id) AS hpx, COUNT(*) AS n
FROM gaiadr3.gaia_source
WHERE phot_g_mean_mag < 11
GROUP BY hpx
"""


def main(ctx):
    near = ctx.tap(NEARBY_ADQL, "gaia", label="parallax>100mas", release="Gaia DR3", max_rows=5000)

    # Quality cut: the raw parallax>100 selection contains spurious solutions.
    good = near[(near.parallax_over_error > 10) & (near.ruwe < 1.4)].copy()
    good["dist_pc"] = 1000.0 / good.parallax
    good["abs_g"] = good.phot_g_mean_mag + 5 * np.log10(good.parallax / 100.0)
    good["v_tan_kms"] = 4.74047 * np.hypot(good.pmra, good.pmdec) / good.parallax

    dens = ctx.tap(DENSITY_ADQL, "gaia", label="healpix3 density G<11", release="Gaia DR3",
                   max_rows=1000, mode="async")
    hp = HEALPix(nside=2**DENSITY_LEVEL, order="nested")
    lon, lat = hp.healpix_to_lonlat(dens.hpx.to_numpy().astype(np.int64))
    density = {
        "level": DENSITY_LEVEL,
        "pixel_area_deg2": float(hp.pixel_area.to_value(u.deg**2)),
        "ra": np.round(lon.to_value(u.deg), 3),
        "dec": np.round(lat.to_value(u.deg), 3),
        "n": dens.n.to_numpy(),
    }
    ctx.save("density_healpix3", density)

    cols = ["source_id", "ra", "dec", "dist_pc", "abs_g", "bp_rp", "v_tan_kms", "radial_velocity", "phot_g_mean_mag"]
    ctx.save("nearby", good[cols].round(4).sort_values("dist_pc"))

    nearest = good.nsmallest(5, "dist_pc")
    summary = {
        "raw_rows": len(near),
        "after_quality_cut": len(good),
        "within_5pc": int((good.dist_pc < 5).sum()),
        "nearest_5": [
            {"source_id": str(r.source_id), "dist_pc": round(r.dist_pc, 3), "G": round(r.phot_g_mean_mag, 2)}
            for r in nearest.itertuples()
        ],
        "median_v_tan_kms": round(float(good.v_tan_kms.median()), 1),
        "bright_stars_G_lt_11": int(dens.n.sum()),
        "density_pixels": len(dens),
    }
    ctx.save("summary", summary)
    return summary
