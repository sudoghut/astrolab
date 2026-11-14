---
name: gaia-dr4-release-day
description: Run-book for Gaia DR4 release day (2026-12-02) - confirm the DR4 schema and columns via TAP_SCHEMA, count before fetching, re-run the M4 dormant-compact-object screen and its vetoes on DR4, and follow up the surviving DR3 candidates with DR4 epoch data. Use on or after DR4 release, or when preparing / rehearsing that run.
---

# Gaia DR4 release day run-book

Study: `studies/001-m04-gaia-dormant-black-holes/` (M4). Its DR3 run is `reproduced`; the
screen is written to be release-parameterised (`screen.py`). The open questions this run
answers are in that study's `README.md` section 7; the to-do item is `T-002`.

Rules stay in `AGENTS.md` - in particular section 1 (download limits, count before fetch,
server-side first). This file is only the order of work, the decision points and the
fallbacks. ADQL how-to and archive quirks: `server-side-query` skill.

**DR4 is a new release, not a bigger DR3.** Every table name, column name and solution type
below is an assumption until TAP_SCHEMA confirms it. Confirm first, then run.

## 0. Before the day

- The Gaia archive is offline 2026-11-25 to 2026-12-02. Do not plan DR3 queries in that
  window; the DR3 results needed for comparison are already in `results/`.
- Work on a branch, with `T-002` moved to "进行中" in `TODO.md` and a draft PR open
  (AGENTS.md section 2).
- Rehearsal (safe before release): `python -c "import sys; sys.path.insert(0,'studies/001-m04-gaia-dormant-black-holes'); from screen import screen_adql; print(screen_adql('dr4'))"`
  prints the DR4 query without touching the network. The same string is already stored in
  `results/dr4_screen_query.json` from the DR3 run.
- Record the DR3 baseline numbers you will compare against (from `results/summary.json`):
  3,343 screen rows, 87 candidates with M2 > 3 Msun, 51 unexplained survivors after vetoes,
  21/21 NS-candidate recall.

## 1. Confirm the schema (no assumptions)

Expect release-day load; use `mode="async"` and retry rather than hammering `/sync`.

1. Schemas: `SELECT schema_name FROM tap_schema.schemas` - confirm the DR4 schema name.
   `screen.py` assumes `gaiadr4` (`SCHEMAS = {"dr3": "gaiadr3", "dr4": "gaiadr4"}`). If it
   differs, change that mapping only - nothing else in the study hard-codes a schema.
2. Tables: `SELECT table_name FROM tap_schema.tables WHERE schema_name = '<dr4 schema>'` -
   confirm `nss_two_body_orbit`, `gaia_source`, `astrophysical_parameters` exist under those
   names.
3. Columns, per table: `SELECT column_name, unit, description FROM tap_schema.columns WHERE table_name = '<schema>.<table>'`.
   Check every column the study uses:
   - `nss_two_body_orbit`: `source_id`, `nss_solution_type`, `period`, `period_error`,
     `eccentricity`, `parallax`, `parallax_error`, `significance`, `goodness_of_fit`, `flags`,
     `a_thiele_innes`, `b_thiele_innes`, `f_thiele_innes`, `g_thiele_innes`, `c_thiele_innes`,
     `h_thiele_innes`, `center_of_mass_velocity`, `t_periastron`, their `_error` twins,
     `bit_index`, `corr_vec`.
   - `gaia_source`: `ra`, `dec`, `l`, `b`, `parallax`, `phot_g_mean_mag`, `bp_rp`, `ruwe`,
     `rv_amplitude_robust`, `rv_nb_transits`.
   - `astrophysical_parameters`: `mass_flame`, `mass_flame_lower`, `mass_flame_upper`,
     `radius_flame`.
   Write the confirmed list into the study `log.md` before fetching anything.
4. Solution types: `SELECT nss_solution_type, COUNT(*) FROM <schema>.nss_two_body_orbit GROUP BY nss_solution_type`
   (server-side aggregate, a handful of rows). Compare with `ASTROMETRIC_TYPES` in
   `screen.py`. DR4 may rename types, drop the `OrbitalAlternative` /
   `OrbitalTargetedSearch` families, or add new astrometric ones. **A new type that is not
   in `ASTROMETRIC_TYPES` is silently excluded from the screen** - decide explicitly for each
   new type whether it is an astrometric orbit, record the decision in `log.md`, and say so
   in the results.
5. `corr_vec`: the DR3 parameter order comes from DPAC `nsstools` (`astrolab/orbits.py`,
   unit-tested in `tests/test_orbits.py`). If DR4 changes the fitted-parameter set or the
   packing, the Monte Carlo masses (R1/R2) are wrong in a way no test catches. Check the DR4
   data-model documentation and the `bit_index` / `corr_vec` lengths on a known source before
   trusting any DR4 uncertainty. If the order cannot be confirmed, report DR4 central values
   only and mark the uncertainties as DR3-order-assumed.

## 2. Count before fetching

```
python -c "import sys; sys.path.insert(0,'studies/001-m04-gaia-dormant-black-holes'); \
  from screen import screen_from_where; print(screen_from_where('dr4'))"
```

Run that `FROM ... WHERE ...` through `fetch.tap_count` (or `ctx.count`). Also count the
whole astrometric-orbit table (`... WHERE a_thiele_innes IS NOT NULL`) for the denominator.

Decision on the count:

| Screen rows | Action |
|---|---|
| < 50,000 | proceed as written (DR3 gave 3,343) |
| 50,000 - 200,000 | do not raise `max_rows` blindly. First tighten: raise `f_M` or the parallax S/N cut, or drop columns. Record the tightened cut as a dated, post-hoc change in `README.md` and `log.md`. |
| > 200,000 or > 50 MB estimated | stop and ask the user (AGENTS.md section 1.6). Do not edit `config.py` or set `ASTROLAB_*`. |

Estimate size as rows x ~130 bytes/row (DR3: 3,343 rows -> 0.4 MB) and check it against
`STUDY_BUDGET_BYTES` (200 MB per run) together with everything else this run fetches.

## 3. Switch the study to DR4

The release is not yet a single parameter. Change, in `studies/001-m04-gaia-dormant-black-holes/run.py`:

- `RELEASE = "dr3"` -> `"dr4"`;
- the provenance labels `release="Gaia DR3"` in `reproduce_targets`, `run_screen`,
  `ns_recall` and `vet` -> `"Gaia DR4"` (they are provenance strings, not logic, but a wrong
  label makes the results file lie about its source);
- `TARGETS[...]["gaia_dr3"]` keys: DR4 source_ids are expected to be stable for these sources,
  but confirm BH1/BH2/BH3 resolve in `<schema>.gaia_source` before interpreting an empty result
  as "no DR4 solution". A missing row is a cross-match problem, not a science result.
- `D1_dr4_query_ok` in `summary` checks for the literal `FROM gaiadr4.nss_two_body_orbit`;
  if the schema name differed in step 1, that check and `SCHEMAS` move together.

Keep the DR3 results: copy `results/` to `results_dr3/` (not committed) or run DR4 on the
branch only, so the comparison in step 5 is against a file, not a memory.

Expected, and fine: BH3 now has an orbital solution in DR4 (it had none in DR3) - that is a
new positive control, not a bug.

## 4. Run

`python -m astrolab run 001` (add `--refresh` only if a cached DR3 answer would otherwise be
reused for an identical query string; the DR4 queries differ by schema, so normally no).

Then check, in order:

1. `assert len(df) == n` in `run_screen` passed (download matches the server-side count).
2. `rows_dropped_null_a0` is 0, as in DR3; a non-zero value means the `SQRT` clip issue is
   live in DR4 and the screen is losing rows.
3. Positive controls are not vetoed: `results/vetting_controls.json` - BH1, BH2 and the 21
   El-Badry et al. (2024) NS candidates must all have `vetoed: false`. **If any control is
   vetoed, the veto rules do not transfer to DR4: report them as failed, do not retune them
   to let the controls through.**
4. S2 recall of the 21 NS candidates. In DR3 the weakest `f_M` was 0.41 against a 0.25 cut;
   if DR4 recall drops below 19/21, the pre-selection is too aggressive for DR4 (that is the
   pre-registered meaning of S2) - report it, loosen the cut only as a labelled post-hoc step,
   and re-count first.
5. `test_conclusions.py`: it asserts the DR3 numbers. Do not edit it to match DR4 in the same
   step as the run. Either keep it pinned to the archived DR3 results, or add DR4 assertions
   alongside - decided deliberately and written up, never silently.

## 5. Interpret against DR3

Report, with DR3 and DR4 side by side: screen rows, candidates with M2 > 3 Msun, how many are
known, how many are vetoed and by which rule, and how many survive unexplained. Then the
specific DR3 follow-up (README section 7): the **51 surviving DR3 candidates** (all giants
and/or low-significance solutions). For each, use DR4 to decide:

- does the DR4 orbital solution still exist, and with a consistent period and `a0`?
- does DR4 epoch radial velocity give an RV amplitude where DR3 had none? The `veto_rv` rule
  was only weakly tested in DR3 (4 of 23 controls had `rv_amplitude_robust`); DR4 epoch RVs
  are what makes it a real test.
- does DR4 epoch astrometry change the solution type or the significance?

Fetch epoch data **only for this short list**, source by source, never in bulk: epoch
time-series for tens of thousands of sources is exactly the kind of download AGENTS.md
section 1.5 forbids. Count and size-check the epoch query before running it; if per-source
epoch tables are large, stop at the summary parameters.

No discovery claim comes out of this run on its own. A surviving candidate is a candidate.

## 6. When something fails

| Symptom | First response |
|---|---|
| Archive down / 503 / timeouts on release day | Expected under load. `astrolab.fetch` already retries with backoff and falls back to async. Wait and retry; do not open parallel query storms. |
| DR4 schema or table name differs | Fix `SCHEMAS` in `screen.py` (step 1.1); nothing else should need touching. |
| A column is missing or renamed in DR4 | Patch `screen.py` / `run.py` for that column and say so in `log.md`. If it is `mass_flame`, the screen falls back to M1 = 1 Msun, which inflates M2 for giants - flag it loudly rather than quietly. |
| ADQL parse error on the nested query | Known Gaia parser quirk; see the `server-side-query` skill (nested subqueries, not inlined expressions). Test each function alone. |
| `corr_vec` order unconfirmed | Central values only; uncertainties withheld (step 1.5). |
| Count over budget | Step 2 table. Ask the user before raising any limit. |
| Positive controls vetoed | Report as a failure of the veto rules on DR4; do not retune. |

If the day's run cannot be completed, leave the branch in a readable state and record the
progress in the `T-002` item's `备注:` before pausing (AGENTS.md section 2).

## 7. Close out

- `README.md`: new section with the DR4 results against the pre-registered criteria; every
  change to a criterion, cut or veto dated and marked post-hoc.
- `log.md`: Chinese entry, newest first, with the confirmed schema, counts, and decisions on
  new solution types.
- `study.yaml`: `footprint.data` gains the DR4 tables; `status` only changes if the DR4 run
  actually settles the study's questions.
- `atlas/claims/*.yaml`: update `ours` and the status for `gaia-dormant-black-holes`.
- `STATUS.md`: the DR4 time-point row is done; state what DR4 changed.
- `python -m pytest` passes; `python -m astrolab atlas`; the study page still renders.
- Referee the DR4 run (`referee` skill) before calling anything reproduced.
- Move `T-002` to `DONE.md` with the PR number and a one-line result.
