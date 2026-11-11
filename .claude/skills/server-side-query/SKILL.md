---
name: server-side-query
description: Write and run ADQL/TAP queries that keep downloads MB-scale - count first, compute derived quantities and aggregates on the server, and work around archive parser quirks. Use whenever a study needs catalog data from Gaia, VizieR, NOIRLab Data Lab, MAST, IRSA or the Exoplanet Archive.
---

# Server-side query workflow

Rules live in AGENTS.md section 1 (limits, forbidden downloads). This is the how-to.

## Steps

1. **Find the columns** instead of guessing: query `tap_schema.columns` for the table
   (`SELECT column_name, unit, description FROM tap_schema.columns WHERE table_name = '<schema.table>'`).
   Column ORDER from TAP_SCHEMA is not reliable; for packed fields (e.g. Gaia `corr_vec`) find the
   official definition (data-model docs or the mission's own package) and add a unit test.
2. **Count first** for any selection of unknown size: `ctx.count("<table> WHERE ...")` or
   `fetch.tap_count(...)`. Write the estimate into README section 3 before fetching.
3. **Push work to the server**: filters in WHERE, aggregates with GROUP BY (Gaia: `GAIA_HEALPIX_INDEX(level, source_id)`),
   derived quantities computed in the SELECT, joins to companion tables (e.g. `gaia_source`,
   `astrophysical_parameters`) on the server. Select only needed columns, never `SELECT *` on big tables.
4. **Fetch through the guard**: `ctx.tap(adql, service, label=..., release=..., max_rows=...)`.
   Use `mode="async"` for queries that may run > ~30 s.

## Known quirks (add new ones here)

- Gaia archive: a long inlined expression in WHERE can fail to parse ("Encountered POWER") even
  though each function works alone. Fix: nested subqueries - compute in inner SELECTs, filter in
  the outer WHERE (`SELECT ... FROM (SELECT ... ) AS q WHERE q.x > ...`). See
  `studies/001-m04-gaia-dormant-black-holes/screen.py`.
- Gaia archive: intermittent HTTP 503 on `/sync`; `astrolab.fetch` retries with backoff and falls
  back to async automatically.
- Gaia HEALPix indices come back as int32; cast to int64 before `astropy_healpix`.
- Gaia DR3 NSS: `corr_vec` covers only fitted parameters, ordered as in DPAC `nsstools`
  (`astrolab/orbits.py`); pseudo-circular orbits omit G (use G = -AF/B).
- pandas: a column named `flags` collides with `DataFrame.flags`; rename derived label columns.
