---
name: gaia-dr4-release-day
description: Run-book for Gaia DR4 release day (2026-12-02) - make the release-day decisions under the information barrier (schema, solution types, non-validated types, corr_vec order, RV column, cross-match table, reference epoch), count before fetching, archive the DR3 results, run the M4 dormant-compact-object study on DR4 and close out. Use on or after DR4 release, or when preparing / rehearsing that run.
---

# Gaia DR4 release day run-book

Study: `studies/001-m04-gaia-dormant-black-holes/` (M4). The study is parameterised by release
(design plan 008): `PARAMS["release"]` in `run.py`, per-release constants in `RELEASES`, the schema in
`screen.SCHEMAS`. Every DR4 criterion is pre-registered in the study `README.md` (DR4 addendum to
sections 2-4) and computed by `run.py`; nothing is decided by hand after DR4 data are seen. The
to-do item is `T-002`.

Rules stay in `AGENTS.md` (download limits, count before fetch: section 1; branches, to-do items,
dated pre-registration changes: section 2). This file is the order of work, the decision points
and the fallbacks. ADQL how-to and archive quirks: `server-side-query` skill.

Run Python with the project interpreter (machine-specific: `CLAUDE.local.md`). Queries for the
decisions go through `dr4_query.py` next to this file. It builds every ADQL string itself (ADQL
literals do not survive shell quoting, least of all in PowerShell 5.1), sends it through
`astrolab.fetch` with `refresh=True` (no rehearsal answer is reused), and has `--print` (show the
ADQL, no network). Commands: `schemas`, `tables <schema>`, `columns <schema.table>`,
`types <schema>`, `count <release>`, `ids`, `resolve <schema>`, `archive <release>` (docstring).
`tests/test_dr4_query.py` runs them without network.

**DR4 is a new release, not a bigger DR3.** Every name below is an assumption until TAP_SCHEMA or
the DR4 documentation confirms it.

## 0. Before the day

- T-011 is done (`DONE.md`): the DR3 results in `results/` carry `release.json` = dr3,
  `reference_ids.json` (109 DR3 ids with position and G) and `period_error` in `bh_candidates`.
  The archive is offline 2026-11-25 to 12-02: no DR3 query can be redone then.
- Work on a branch with `T-002` in "进行中" and a draft PR (AGENTS.md section 2).
- Rehearse without network: `dr4_query.py <command> --print` for every command, and
  `python -m pytest`. A DR4 exploration (`python -m astrolab explore 001 --tag dr4 --set release=dr4`)
  only works once DR4 exists.
- DR3 baseline (`results/summary.json`): 3,343 screen rows of 169,227 astrometric solutions; 87 with
  M2 > 3 Msun, 2 known; 51 survivors (not known, not vetoed, not refuted); 21/21 NS recall; 0 of 23
  controls with a solution vetoed (BH3 has none in DR3).

If DR4 slips or arrives partial, stop after step 1, record what exists in `log.md` and the `T-002`
item's `备注：`, and wait.

## 1. Release-day decisions under the information barrier

README DR4 addendum, "Information barrier": these are decided from **metadata and documentation
only**, written into `log.md`, and the code change committed, **before any source-level DR4 data**
(targets, controls, survivors, screen) are fetched. Changing one afterwards is a post-hoc change and
is reported as such. Each is a one-line edit:

| Decision | Source | Where |
|---|---|---|
| DR4 schema name | `dr4_query.py schemas` | `screen.SCHEMAS["dr4"]` |
| Tables exist | `dr4_query.py tables <schema>` (names come back schema-qualified) | stop if `nss_two_body_orbit`, `gaia_source` or `astrophysical_parameters` is missing |
| Astrometric types (mechanical rule) | `dr4_query.py types <schema>`: aggregate counts only; types with `n_thiele_innes > 0` | `screen.ASTROMETRIC_TYPES["dr4"]` = exactly that list (per release: DR3 queries are unaffected) |
| Non-validated types | DR4 data model / release papers (not the data) | `PARAMS["unvalidated_types"]` (a formal parameter: dated). It is one value for whichever release runs; the DR3 value is kept in `results/dr3/summary.json` `params` |
| `corr_vec` order | DR4 data model or a DPAC `nsstools` release for DR4 | `RELEASES["dr4"]["covariance_trusted"]` = True only if confirmed; otherwise False (R1-R3 "not evaluable"). A new fitted-parameter set or order needs an `astrolab/orbits.py` change: core library, own review |
| RV amplitude column | `dr4_query.py columns <schema>.gaia_source` and the data model | `RELEASES["dr4"]["rv_amplitude_column"]`: keep, a documented successor, or `None` (RV veto not applicable). A configured name missing from TAP_SCHEMA stops the run |
| DR3-DR4 cross-match table | `dr4_query.py tables`, `columns` | `RELEASES["dr4"]["neighbourhood"]` (table, old/new id columns, distance column and its unit), or `None` if DR4 publishes no such table (then direct ids only). Before any source-level query the run checks it against TAP_SCHEMA and stops if the configured table is not listed or lacks the columns, so a wrong name cannot silently drop the fallback |
| DR4 reference epoch | data model | `RELEASES["dr4"]["epoch_gap_yr"]` = epoch - 2016.0 |

The run itself checks TAP_SCHEMA first (`run.available_columns`, `run.check_neighbourhood`): it stops
if any column its queries need, the configured RV column or the configured cross-match table is
missing, before fetching source-level data. FLAME columns may be missing (they count as absent).
`dr4_query.py resolve` fetches source-level positions: run it only after these decisions are
committed (step 3).

## 2. Count before fetching

`dr4_query.py count dr4` counts the screen (cuts from `PARAMS`) and all astrometric orbits on the
server. Write the count and the size estimate (rows x ~300 bytes) into README section 3 (DR4 table)
before the run. At >= 50,000 rows the pre-registered rule applies inside `run.py`: S1-DR4 fails,
the screen is not fetched, S3-DR4 is "not evaluable", the rest is still computed. A tightened screen
afterwards is post-hoc and is never read as the pre-registered S3 result. Raising any limit follows
AGENTS.md section 1.6.

## 3. Archive DR3, switch, check ids

1. `dr4_query.py archive dr3` (copies `results/*.json` to `results/dr3/`; refuses if `results/` is
   not DR3 or the target exists); commit `results/dr3/`. The run refuses to overwrite an
   un-archived or newer DR3 run (guard).
2. `PARAMS["release"] = "dr4"` in `run.py` (a formal parameter: dated note in `log.md`).
3. `dr4_query.py resolve <schema>`: direct ids with the identity check only (`run.py` adds the
   cross-match-table fallback for the ids that fail, so the run may resolve more). Unresolved ids are
   cross-match problems, never science results. **Step-1 settings are not changed in response to
   this output or to the run's resolution**; if one must change, it is a reported post-hoc change.

## 4. Run and check

`python -m astrolab run 001 --refresh` (`--refresh`: no cached answer from an earlier attempt).
The run writes every file of `OUTPUTS` only after all are computed and size-checked (each < 1 MB);
a failed run writes nothing.

Check `results/summary.json`:
- `dr4.resolution`: unresolved count and reasons; `neighbourhood` says whether the table was used.
- `optional_columns`, `ambiguous_flame_sources`, `sources_with_same_type_solutions`: data quirks.
- `rows_dropped_null_a0` = 0 (otherwise the screen loses rows to the server-side SQRT).
- `dr4.R`, `dr4.S1`, `dr4.S2`, `dr4.V`: verdicts `pass` / `fail` / `not evaluable`, as
  pre-registered. **A vetoed control means the veto rules fail on DR4: report it, do not retune.**
- `dr4.F.counts` (labels of the 51 DR3 survivors, `survivors_dr4.json`) and `dr4.S3`
  (`new_candidates_dr4.json`, ids in `new_candidate_ids_dr4_a/_b.json`).
- `screen_descriptive`: DR3-style counts on DR4, descriptive only.

No discovery claim comes out of this run. `persists` means "still a candidate".

## 5. When something fails

| Symptom | First response |
|---|---|
| 503 / timeouts | Expected under load; `astrolab.fetch` retries and falls back to async. Wait. |
| SystemExit "TAP_SCHEMA lists no ..." / "lacks ..." / "not in TAP_SCHEMA" | A step-1 decision is wrong or missing: fix it from metadata, log it, rerun. Nothing was written, and these stops come before any source-level query; if source-level data had already been seen (e.g. step 3.3), report the fix as post-hoc. |
| SystemExit "screen returned N distinct rows, server count n" | Server inconsistency or an unexpected join: report it; do not narrow or rewrite the screen ad hoc (that would be a post-hoc selection). |
| SystemExit "no DR3 results to compare with" | `results/dr3/` missing or not DR3: restore it from git (step 3.1). |
| SystemExit "S3 ids exceed the two id files" | Cannot happen below the 50,000-row screen bound: a bug, fix and review. |
| SystemExit "results/ holds the dr3 run, not archived" / "older" | Step 3.1 (archive, or re-archive after removing a stale `results/dr3/`). |
| `covariance_error` in `reproduction.json` | New solution type or `corr_vec` layout: R1-R3 are "not evaluable"; extending `orbits.py` is a core-library change with its own review. |
| SystemExit "result files over ... bytes" | Nothing written; the caps cover the pre-registered bounds, so this is a bug: fix it and have it reviewed. |
| ADQL parse error | Known Gaia parser quirk: nested subqueries (`server-side-query` skill). |

## 6. Close out

- `README.md`: DR4 results against the DR4 addendum criteria; `log.md`: Chinese entry (decisions of
  step 1 with their sources, counts, verdicts).
- `study.yaml` `footprint.data`: add the DR4 tables; `status` only changes if DR4 settles the questions.
- `atlas/claims/gaia-dormant-black-holes.yaml`: `ours` for BH3 if R3 is evaluable; `python -m astrolab claims check`.
- `STATUS.md`; `python -m pytest` (DR3 criteria read `results/dr3/`, DR4 ones `results/`);
  `python -m astrolab atlas`; the study page shows a DR4/DR3 switch.
- Referee the DR4 run (`referee` skill) before calling anything reproduced.
- Move `T-002` to `DONE.md` (PR number and a one-line result, AGENTS.md section 2).
