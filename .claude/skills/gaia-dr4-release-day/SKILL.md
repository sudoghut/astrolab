---
name: gaia-dr4-release-day
description: Run-book for Gaia DR4 release day (2026-12-02) - preflight the M4 study for DR4, confirm the DR4 schema, columns and solution types via TAP_SCHEMA, count before fetching, re-run the dormant-compact-object screen and its vetoes on DR4, and follow up the surviving DR3 candidates. Use on or after DR4 release, or when preparing / rehearsing that run.
---

# Gaia DR4 release day run-book

Study: `studies/001-m04-gaia-dormant-black-holes/` (M4). Its DR3 run is `reproduced`. The open
questions this run answers are in that study's `README.md` section 7; the to-do item is `T-002`.

Rules stay in `AGENTS.md` (download limits and the order count -> estimate -> fetch in section 1;
pre-registration, branches, to-do items in section 2). This file is only the order of work, the
decision points and the fallbacks. ADQL how-to and archive quirks: `server-side-query` skill.

**DR4 is a new release, not a bigger DR3.** Every table name, column name and solution type the
study uses is an assumption until TAP_SCHEMA confirms it.

Queries go through `dr4_query.py` next to this file. It builds every ADQL string itself (ADQL
literals contain quotes that do not survive shell quoting, least of all in PowerShell 5.1), sends it
through `astrolab.fetch`, and always uses `refresh=True`, so an answer cached during a rehearsal
is not served again on release day. Add `--print` to see the ADQL without touching the network.
Run from the project root (in PowerShell set `$env:PYTHONIOENCODING='utf-8'` first):

```
python .claude/skills/gaia-dr4-release-day/dr4_query.py <command> [arg] [--print]
```

Commands: `schemas`, `tables <schema>`, `columns <schema.table>`, `types <schema>`,
`count <release>`, `ids`, `resolve <schema>`, `followup <schema>` (see the script's docstring).
The helper reads `TARGETS`, the cuts and the `data/` files from the study, so it follows code
changes; `tests/test_dr4_query.py` runs every command with `--print` and fails if a renamed
key, moved file or changed id count breaks it (it does not check each id or column).

## 0. Preflight (before 2026-11-25, while the archive is still up)

The study is not yet a one-parameter switch. `T-011` makes it one; check that `DONE.md` lists it
as done (`[x]`). If not, every site in this table must be changed by hand on the day, and each one
has a failure mode:

| Site | Current DR3 assumption | Failure if left |
|---|---|---|
| `screen.py` `SCHEMAS` | `"dr4": "gaiadr4"` (unconfirmed) | every query fails if the schema name differs |
| `run.py` `RELEASE` | `"dr3"` | runs DR3 again |
| `run.py` `release="Gaia DR3"` in `reproduce_targets`, `run_screen`, `ns_recall`, `vet` | provenance label | results claim DR3 as their source |
| `run.py` `TARGETS["Gaia BH3"]` | `m1: None, m1_err: None` | **`TypeError` in `reproduce_targets` as soon as BH3 has an orbit** (`rng.normal(None, ...)`), before anything is saved |
| `run.py` `main()` `controls` | BH1, BH2 only | BH3 is never checked as a positive control; adding it makes `controls_checked` 24, but `test_post_hoc_vetoes_keep_all_positive_controls` asserts 23 |
| `run.py` `reproduce_targets` | `rows.iloc[0]` | a target with more than one DR4 solution silently uses whichever row the server returns first |
| `data/ns_candidates_elbadry2024.json`, `data/literature_vetting.json`, the 51 DR3 survivors in `results/bh_candidates.json` | DR3 source_ids | an id that changed in DR4 reads as a science result: a lost NS control lowers S2 recall, a lost refuted source loses its label, a lost survivor looks like "solution gone" |
| `run.py` `UNVALIDATED_TYPES` | DR3 type names, exact match | if DR4 renames the families, `veto_type` silently never fires and the survivor count is inflated |
| `run.py` result keys `period_dr3_d`, `gaia_dr3`, status `"no DR3 orbital solution ..."`; `D1_dr4_query_ok` literal `gaiadr4` | DR3 names | DR4 numbers stored under DR3 keys |
| `results/` | overwritten in place by `python -m astrolab run 001` | the committed DR3 reproduction is replaced, and every DR3 assertion in `test_conclusions.py` is evaluated on DR4 numbers (`test_bh3_has_no_dr3_orbit` must then fail) |
| `test_conclusions.py` | DR3 criteria; `test_D1_dr4_query_generated` checks the literal `gaiadr4` | pytest red at close-out |
| `.claude/skills/gaia-dr4-release-day/dr4_query.py` | `TARGETS[...]["gaia_dr3"]`, `results/` (or `results/dr3/`) with `summary.json` `release == "dr3"` | refuses to run, or reads moved files; `tests/test_dr4_query.py` catches it |
| `web/index.html` | "DR3" labels, `P<sub>DR3</sub>`, the literal 169,227, `REPRO_STATUS_ZH` | page shows DR4 numbers under DR3 labels |
| `study.yaml` `footprint.data` | `gaiadr3.*` | Atlas footprint names the wrong release |

**Pre-register the DR4 run before it happens** (AGENTS.md section 2): `README.md` sections 1-4 get
a dated DR4 addendum written before 2026-12-02, at least:

- R3 (BH3): M1 and its error from Gaia Collaboration, Panuzzo et al. 2024 (arXiv:2404.10486),
  verified against the paper text; the comparison value 32.70 +/- 0.82 Msun; the pass rule.
- What S1 (< 50,000 rows), S2 (>= 19/21 NS recall) and the veto checks mean on DR4.
- What decides each of the 51 DR3 survivors (step 5).
- README section 3: the DR4 inputs with "to be counted on release day" and the decision table of
  step 2, so the size estimate is written before the fetch.

Rehearsal (safe, no network): `python -c "import sys; sys.path.insert(0,'studies/001-m04-gaia-dormant-black-holes'); from screen import screen_adql; print(screen_adql('dr4'))"`.
The DR3 run stored the same string in `results/dr4_screen_query.json` (until `T-011` changes the
results layout). `dr4_query.py <command> --print` rehearses every query below. A full rehearsal through
`python -m astrolab explore` needs a `PARAMS` dict in `run.py` (also `T-011`).

DR3 baseline to compare against (`results/summary.json`): 3,343 screen rows of 169,227 astrometric
solutions; 87 with M2 > 3 Msun, 2 known; 51 survivors (not known, not vetoed, not refuted - all
giant and/or low-significance); 5 unknown with no pre-registered label (`S3_unflagged_unknown_preregistered_labels`);
21/21 NS recall, weakest f_M 0.41; 0 of 23 positive controls vetoed.

If DR4 slips or arrives partial (e.g. NSS tables later than `gaia_source`), stop after step 1, record
what exists in `log.md` and the `T-002` item's `备注：`, and wait.

## 1. Confirm the schema

Release-day load is expected: use `mode='async'`, retry patiently, no parallel query storms.

1. Schema: `dr4_query.py schemas`. If the DR4 schema is not `gaiadr4`, fix `SCHEMAS` in
   `screen.py` now (step 2 builds its count from it), and the other schema rows of the preflight
   table before step 3.
2. Tables: `dr4_query.py tables <schema>` - `nss_two_body_orbit`, `gaia_source`,
   `astrophysical_parameters` (Gaia returns schema-qualified names, e.g. `gaiadr4.gaia_source`).
3. Columns: `dr4_query.py columns <schema>.<table>` for each table.
   Check every column the code selects - read them from the code, not from a list here:
   `ERR_PARAMS` and the two SELECTs in `reproduce_targets`, `vet` in `run.py`; `_COLS` and the
   SELECTs in `screen.py`. Write the confirmed mapping into `log.md` before fetching data.
4. Solution types: `dr4_query.py types <schema>` (a server-side aggregate, a handful of rows).
   Compare with **both** `ASTROMETRIC_TYPES` (`screen.py`) and `UNVALIDATED_TYPES` (`run.py`):
   - a new astrometric type not in `ASTROMETRIC_TYPES` is silently excluded from the screen;
   - a renamed non-validated family makes `veto_type` silently stop firing;
   - `orbits.solution_parameters` raises `ValueError` on any type other than `Orbital`,
     `AstroSpectroSB1`, or a name containing `OrbitalAlternative` / `OrbitalTargetedSearch` (three
     `corr_vec` orders: `Orbital`; the alternative / targeted-search families; `AstroSpectroSB1`), so BH1/BH2/BH3 with a new type crash `reproduce_targets`.
   Decide each new type explicitly, record the decision in `log.md`, and state it in the results.
5. `corr_vec`: the DR3 order follows DPAC `nsstools` (`astrolab/orbits.py`). `tests/test_orbits.py`
   checks it only when `nsstools` is installed (otherwise it skips). A changed parameter count fails
   loudly (`orbits.covariance` raises on a length mismatch); a same-length reordering corrupts the
   Monte Carlo masses silently. Check the DR4 data-model documentation and the `bit_index` /
   `corr_vec` length on BH1 before trusting any DR4 uncertainty. If the order cannot be confirmed,
   report central values only and say why.

## 2. Count before fetching

`dr4_query.py count dr4` counts the screen and the denominator (all astrometric orbits) on the
server, using `SCHEMAS` from `screen.py` and the cuts `FM_MIN`, `PLX_SNR_MIN` from `run.py`
(a tightened cut goes into `run.py` first, so the count and the run cannot disagree).
Size estimate: rows x ~300 bytes, conservative for the ~30 columns fetched (DR3: 3,343 rows gave
0.4 MB of results JSON). Write count and estimate into
README section 3 before running.

| Screen count | Action |
|---|---|
| < 50,000 | proceed |
| >= 50,000 | **pre-registered S1 fails on DR4: record that first.** Then, as a dated post-hoc step, tighten the selection (higher `f_M` or parallax S/N cut - fewer columns does not help, the limit is rows), re-count, and report both. Raising `max_rows` or any limit follows AGENTS.md section 1.6. |

## 3. Switch and protect the DR3 results

- Apply the preflight table (or confirm `T-011` did).
- Keep the DR3 results as committed files, not memory: the DR3 `results/` is in git on `main`.
  Unless `T-011` already separates results by release, copy it to `results/dr3/` (small JSON,
  ~0.5 MB) and commit before the DR4 run, and point the DR3 assertions of `test_conclusions.py`
  there. Never edit DR3 assertions to make them pass on DR4 numbers.
- `dr4_query.py resolve <schema>`: one `IN (...)` query checks that every DR3 id the study is
  keyed on (3 BHs, 21 NS controls, 6 literature-labelled, 51 survivors; `dr4_query.py ids` lists
  them) exists in DR4 `gaia_source`, and lists their DR4 NSS solutions (more than one for a
  target: decide which one R1-R3 use, preflight row). **Any missing id is a cross-match problem,
  resolved before S2 or step 5 are computed**, never a science result. Use the DR3-DR4
  neighbourhood / cross-match table if DR4 publishes one.

## 4. Run and check

`python -m astrolab run 001 --refresh`. The cache key is the query text, so without `--refresh`
a DR4 answer cached by an earlier attempt (e.g. before an archive reload or erratum) would be
reused silently; every query of this run is a DR4 query, so refreshing re-fetches nothing else.
Then, in order:

1. The run finished. An over-size result raises `TooLarge` out of `ctx.tap` (it is never silently
   truncated); go back to step 2. **After any failed run, restore `results/` from git** (or from
   `results/dr3/`): `main()` saves files as it goes, so a crash leaves a DR3/DR4 mixture whose
   `provenance.json` and `run_info.json` still describe the DR3 run.
2. `rows_dropped_null_a0` is 0 (as in DR3). Non-zero: the screen loses rows to the `SQRT`.
3. Positive controls (`results/vetting_controls.json`: BH1, BH2, 21 NS candidates; BH3 once added, preflight row) all
   `vetoed: false`. **If any is vetoed, the veto rules fail on DR4: report it, do not retune them
   to let the controls through.**
4. `candidates_vetoed_type` > 0, or an explained 0 (step 1.4). A silent 0 is a finding to
   investigate, not a pass.
5. S2 recall >= 19/21; below that the pre-selection is too aggressive for DR4 (its pre-registered
   meaning). Loosen only as a labelled post-hoc step, re-counting first.
6. R3 (BH3) against its pre-registered rule.

Mass direction, for interpreting rows without FLAME masses: M2 rises with M1 in
M2^3 = f_M (M1 + M2)^2, so the fallback M1 = 1 Msun underestimates M2 for hosts heavier than
1 Msun and overestimates it for lighter ones.

## 5. Interpret against DR3

Report DR3 and DR4 side by side: screen rows, M2 > 3 candidates, known, vetoed (by rule),
refuted by literature, survivors. Then the 51 DR3 survivors. For each, from DR4:

- does the orbital solution still exist with a consistent period and `a0`?
- is there now an RV amplitude (`rv_amplitude_robust` or its DR4 successor)? Veto (ii) was weakly
  tested in DR3 (4 of 23 controls had it); DR4 RVs make it a real test.
- did the solution type or significance change?

Get these as **one server-side query**: `dr4_query.py followup <schema>` (orbit and RV summary
for the 51 ids, `source_id IN (...)`; check its column names against step 1.3 first). Aggregate any
epoch quantity on the server (`server-side-query` skill). Per-source epoch
time-series are a last resort: count and size them first, never in a loop over the list
(AGENTS.md section 1.2), and stop at summary parameters if they are large.

No discovery claim comes out of this run. A surviving candidate is a candidate.

## 6. When something fails

| Symptom | First response |
|---|---|
| 503 / timeouts | Expected under load. `astrolab.fetch` retries with backoff and falls back to async. Wait. |
| Schema or table name differs | Every schema row of the preflight table: `SCHEMAS`, the D1 literal, `test_D1_dr4_query_generated`, `study.yaml` footprint. |
| S2 recall drops, or a survivor's solution "vanished" | First `dr4_query.py resolve`: a changed source_id, not a science result. |
| Column missing or renamed | Patch the code for that column; record in `log.md`. A missing `mass_flame` makes every row use M1 = 1 Msun: flag it (step 4 note on direction). |
| `TypeError` in `reproduce_targets` | BH3 `m1` is still `None` (preflight). |
| `ValueError` from `orbits` | New solution type or changed `corr_vec` length (step 1.4-1.5). |
| ADQL parse error | Known Gaia parser quirk: nested subqueries (`server-side-query` skill). |
| Count over 50,000 | Step 2 table. |
| Positive control vetoed | Report as a veto failure on DR4; do not retune. |

If the run cannot be completed, leave the branch readable and record progress in the `T-002`
item's `备注：` before pausing.

## 7. Close out

- `README.md`: DR4 results against the pre-registered DR4 criteria; any change to a cut or veto
  dated and marked post-hoc. `log.md`: Chinese entry with schema, counts, type decisions.
- `study.yaml` `footprint.data`; `status` changes only if DR4 settles the questions.
- `atlas/claims/gaia-dormant-black-holes.yaml`: `ours` for BH3, status; `python -m astrolab claims check`.
- Web page: labels show the release of the numbers they sit on (preflight row).
- `STATUS.md` time-point row; `python -m pytest`; `python -m astrolab atlas`; page renders.
- Referee the DR4 run (`referee` skill) before calling anything reproduced.
- Move `T-002` to `DONE.md` (with the PR number and a one-line result, AGENTS.md section 2).
