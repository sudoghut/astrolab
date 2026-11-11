# Smoke test: Gaia DR3 census of the 10 pc neighbourhood

## 1. Question

Does the environment work end to end on real data? This is an engineering check,
not a research result.

## 2. Hypothesis and decision criteria

- The `parallax > 100 mas` query returns a few hundred rows (MB-scale) and is cached;
  a second run makes no network request.
- After a quality cut (`parallax_over_error > 10`, `ruwe < 1.4`), the nearest
  object is Proxima Centauri (~1.30 pc). Note that α Cen A/B are too bright for
  reliable Gaia astrometry and may be missing.
- Server-side aggregation of all G < 11 stars into 768 HEALPix pixels returns
  exactly 768 rows, and the Galactic plane is clearly visible.

## 3. Data (with size estimate)

| Input | Source | Selection | Est. size |
|---|---|---|---|
| Nearby sources | Gaia DR3 `gaia_source` (TAP: gaia) | `parallax > 100` | ~10² rows, < 100 kB |
| Bright-star density | Gaia DR3 `gaia_source` | `G < 11`, `GROUP BY` HEALPix level 3 | 768 rows |

## 4. Method

Absolute magnitude `M_G = G + 5 log10(parallax / 100 mas)`; tangential velocity
`4.74 μ / ϖ`. No extinction correction (negligible within 10 pc).

## 5. Results

See `web/index.html` and `results/summary.json`.
