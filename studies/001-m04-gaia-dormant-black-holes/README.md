# M4: Gaia dormant black holes - DR3 reproduction and DR4-ready screen

> Sections 1-4 were written on 2026-11-11 BEFORE run.py (pre-registration).
> Later edits to them must carry a dated note.

## 1. Question

1. Can Gaia DR3 NSS astrometric orbits alone (no RV follow-up) reproduce the
   dark-companion masses of Gaia BH1 and BH2 published by El-Badry et al. (2023a,b)?
2. Can a fully server-side screen of all DR3 astrometric orbital solutions recover
   the known dormant compact objects (BH1, BH2, and the 21 neutron-star candidates of
   El-Badry et al. 2024) while downloading only MB-scale data?
3. Is that screen ready to run on Gaia DR4 (2026-12-02) by changing one parameter?

## 2. Hypotheses and decision criteria

**R1 (BH1).** The DR3 `Orbital` solution of source 4373465352415301632 with
M1 = 0.93 +/- 0.05 Msun (El-Badry et al. 2023a, Sec. 2.1) gives M2 consistent with
the published 9.62 +/- 0.18 Msun: |M2_ours - 9.62| < 2 sigma_combined.

**R2 (BH2).** The DR3 `AstroSpectroSB1` solution of 5870569352746779008 with
M1 = 1.07 +/- 0.19 Msun (El-Badry et al. 2023b, Sec. 3.5) gives M2 consistent with
8.9 +/- 0.3 Msun at 2 sigma. *Expectation noted in advance:* the DR3 period
(1352 +/- 45 d) differs from the RV-constrained 1277 d, so a moderate offset would not
be surprising; if R2 fails we report the offset and its cause rather than tuning.

**S1 (screen size and BH recovery).** The server-side screen returns < 50,000 rows
(< 20 MB) and both BH1 and BH2 appear with M2 > 3 Msun using their published M1.

**S2 (NS-candidate recall).** At least 19 of the 21 El-Badry et al. (2024) candidates
(>= 90%) pass the server-side pre-selection (`f_M > 0.25 Msun`). Recall below this
means the pre-selection is too aggressive for DR4 and must be loosened.

**S3 (new candidates, exploratory).** The number of solutions with M2 > 3 Msun under
an M1 estimate from Gaia FLAME (`astrophysical_parameters.mass_flame`, fallback 1 Msun)
is reported with no prior expectation. Each is labelled: known (literature) / likely
spurious (quality flags) / unexplained. No discovery claim is made in this study.

**D1 (DR4 readiness).** The same code produces valid ADQL for `release="dr4"` (schema
`gaiadr4`) and runs end to end for `release="dr3"`.
*Note 2026-11-14 (design plan 008):* the check now uses the schema mapped to `dr4` in
`screen.SCHEMAS` (`gaiadr4` unless release day shows otherwise) instead of the literal name; the
meaning of D1 is unchanged. D1 is a DR3-run criterion and is "not applicable" on the DR4 run.

### DR4 addendum to section 2 (2026-11-14, written before the DR4 release; pre-registration)

Evaluated on the DR4 run only (`PARAMS["release"] = "dr4"`). The DR3 criteria above are not
changed and keep being checked against the archived DR3 results in `results/dr3/`. All DR4
criteria are computed by `run.py` (design plan 008), not by hand on the day.

**Definitions used below.**
- *Information barrier*: the release-day decisions below (astrometric types, non-validated types,
  `covariance_trusted`, the DR4 reference epoch used for `epoch_gap_yr`, and - note 2026-11-14,
  before the release - the RV-amplitude column and the DR3-DR4 cross-match table specification or
  "none published") are made from metadata and documentation only (TAP_SCHEMA, the
  server-side type tally, an aggregate query that returns only counts per type, the DR4 data model
  and release papers; no source-level row or value is inspected) and logged in `log.md`, with the
  `PARAMS` / `RELEASES` / `screen.py` change committed, before any source-level DR4 data (targets,
  controls, survivors, screen) are fetched. They cannot be revisited after such data are seen
  without being reported as a post-hoc change.
- *Astrometric types*: mechanically, the DR4 solution types for which the server-side tally
  `SELECT nss_solution_type, COUNT(*), COUNT(a_thiele_innes) ... GROUP BY nss_solution_type` shows
  Thiele-Innes constants (COUNT(a_thiele_innes) > 0); `ASTROMETRIC_TYPES["dr4"]` in `screen.py`
  (one list per release since 2026-11-14, so DR3 queries are unaffected) is set to exactly this list
  (run-book step 1).
- *Non-validated types*: `PARAMS["unvalidated_types"]`. For DR4 these are the solution types the
  DR4 documentation (data model or release papers) describes as not validated or of lower
  reliability, decided from the documentation, written into `log.md` and into `PARAMS` with a date
  before the vetting query is fetched. Changing this formal parameter is a change to this
  pre-registration and is recorded as such.
- *Resolution*: a DR3 source_id "resolves" if it is present in DR4 `gaia_source` and passes the
  identity check, or else, if DR4 publishes a DR3-DR4 cross-match (neighbourhood) table, if that
  table maps it to a DR4 source (the neighbour with the smallest angular distance; two neighbours
  within 0.1 arcsec of the same distance, or a failed identity check, mean no match); the mapped
  DR4 id is then used. Identity check: against the DR3 position and G magnitude archived for all
  109 DR3 ids the study uses (the 87 DR3 rows with M2 > 3 Msun, the 21 NS candidates, BH3 and the
  literature-labelled sources; `results/dr3/reference_ids.json`), with the DR3 position moved to the
  DR4 reference epoch using the DR4 proper motion (no propagation if DR4 has none), the offset is
  < 2 arcsec and |G_DR4 - G_DR3| < 0.3 mag. A source that does not resolve is reported as
  `unresolved`, with the reason (not found / ambiguous: several rows for the id / offset / magnitude),
  and is never counted as a
  scientific outcome. Large-amplitude variable giants can fail the magnitude check; this errs
  towards `unresolved`, and the count is reported.
- *Missing data* (note 2026-11-14, design plan 008, before the release): a FLAME value that is
  NULL, a FLAME column the release lacks, and a FLAME value that is ambiguous (several FLAME rows for
  one source) all count as absent. A missing `gaia_source` or `astrophysical_parameters` table (or
  a TAP_SCHEMA lookup that lists neither) stops the run before any source-level data are fetched:
  it needs a release-day decision, logged under the information barrier.
- *Primary solution (R-sel)*, applied per source everywhere (targets, controls, survivors, new
  candidates): among the source's solutions of astrometric type, prefer validated over
  non-validated; among those prefer `AstroSpectroSB1`, then `Orbital`, then the other types; ties
  by the highest `significance`, then the smallest |`goodness_of_fit`|, then the lexicographically
  smallest `nss_solution_type`, then the smallest `period`, then the Thiele-Innes constants A, B, F,
  G ascending (missing values sort last; rows equal on all of these are one solution), so the choice
  never depends on row order. All solutions are saved; the
  criteria use the primary.
- *Vetoes*: (i) type veto: the primary solution is of a non-validated type; (ii) RV veto: DR4
  `rv_amplitude_robust` < `PARAMS["rv_ratio_min"]` (0.5) x the min-to-max RV range predicted from
  the primary orbit (2K with cos i = (AG - BF)/a0^2, as in section 5). On DR4 the RV veto applies
  only if P < 1000 d (at least two orbits within the ~66-month DR4 baseline) and e < 0.8 (a
  short periastron spike can fall between sparse RV epochs), and the column exists; otherwise it
  is "not applicable", never a veto. A missing eccentricity means a pseudo-circular solution, for which Gaia fixes
  e = 0 (note 2026-11-14, before the release; the DR3 code already used e = 0 in this case). Even within these limits, a sparsely sampled orbit can show a
  smaller range than predicted, so an RV veto is evidence, not proof. If DR4 renames the column,
  its documented successor with the same definition is used (`RELEASES[...]["rv_amplitude_column"]`;
  a configured name absent from TAP_SCHEMA stops the run, so a typo cannot switch the veto off), decided and logged in `log.md`
  before the vetting query (like the type list); if there is none, the RV veto is not applicable.
- *Uncertainties*: the DR4 entry of `RELEASES` in `run.py` has `covariance_trusted = False` until
  the `corr_vec` parameter order is confirmed on release day (run-book step 1.5) from documentation
  only (the DR4 data model or a DPAC `nsstools` release for DR4), and the change is logged, before
  the first formal DR4 run; while it is False, R1-R3 are "not evaluable" and only central values
  are reported. If it is changed after any formal DR4 run, that earlier run is reported as well.
  After the barrier, a `corr_vec` length check on BH1 may only set it back to False (reported),
  never to True.
  `RELEASES` is part of this pre-registration: any other change to it is recorded as such.

**R1-DR4, R2-DR4.** Same rule as on DR3 (|M2_ours - M2_paper| < 2 sigma_combined), using the
primary DR4 solution of BH1 and BH2 with the M1 values of section 2. No DR4 solution or unresolved:
"not evaluable". R1b (comparison with the published DR3-only solution) is a DR3-only check and is
not evaluated on DR4.

**R3 (BH3).** If BH3 (4318465066420528000) resolves and has a DR4 solution of astrometric type,
M1 = 0.76 +/- 0.05 Msun (Gaia Collaboration, Panuzzo et al. 2024, arXiv:2404.10486v2, Table 3)
gives M2 consistent with the published 32.70 +/- 0.82 Msun: |M2_ours - 32.70| < 2 sigma_combined.
No DR4 solution: "not evaluable", not a failure.
*Expectation noted in advance:* the published mass comes from a pre-release run (NSS 4.1) of the
same pipeline on the same ~66 months of data, with a combined astrometric + RV (`AstroSpectroSB1`)
solution: f_M = 31.23 +/- 0.81 Msun, P = 4253.1 +/- 98.5 d. For an `AstroSpectroSB1` solution our
f_M = (a0/parallax)^3 / P^2 is the same quantity as their a1-based f_M (the parallax of that
solution is a0/a1), so no method offset is expected; their astrometry-only solution has f_M =
32.03 +/- 0.64 Msun, mostly because of its shorter period (4194.7 d), and would give M2 about
0.8 Msun higher. R3 is therefore a check of consistency between NSS 4.1 and the final DR4
pipeline, not an independent measurement.

**S1-DR4.** The DR4 screen returns < 50,000 rows (counted on the server first; at >= 50,000 S1-DR4
fails, the screen is not fetched, and the screen-dependent item S3-DR4 is "not evaluable" while
the rest is still computed; a tightened screen run afterwards is post-hoc and its S3 numbers are
never read as the pre-registered result), and each of BH1, BH2, BH3 that resolves and has a
DR4 solution has M2 > 3 Msun with its published M1 on its primary solution; a missing target is
listed as "not evaluable" for this part. At least 2 of the 3 targets must be evaluable for this
part to pass; with fewer, S1-DR4 is "not evaluable" (never a pass for lack of data).

**S2-DR4.** Of the 21 El-Badry et al. (2024) candidates, N_eval are those that resolve and have a
DR4 solution of astrometric type; a candidate passes if its primary solution meets the screen
cuts (astrometric type, parallax S/N > 5, f_M > 0.25 Msun; the same meaning as `in_screen` on DR3),
evaluated on the fetched solution, so S2-DR4 does not depend on fetching the screen.
Pass: N_eval >= 15 and passed >= ceil(0.9 N_eval). N_eval < 15: "not evaluable". The catalogue
recall (how many of the 21 have any DR4 solution) is reported separately. As on DR3, this test is
weak (the weakest DR3 f_M was 0.41 against a 0.25 cut).

**V-DR4 (vetoes on controls).** Controls: BH1, BH2, BH3 and the 21 NS candidates. A control is
vetoed if its primary solution is vetoed by (i) or (ii). Controls without a DR4 solution or
unresolved are listed and not counted; N_ctrl is the number counted. Pass: N_ctrl >= 15 and no
counted control is vetoed; N_ctrl < 15: "not evaluable". The number of counted controls to which
the RV veto applies is reported with it (on DR3 it was 4 of 23): below 5 the RV half of the test
is reported as weak. A vetoed control means the veto rules fail on DR4; they are reported and not
retuned.

**F-DR4 (the 51 DR3 survivors).** Each of the 51 DR3 candidates that were not known, not vetoed
and not refuted gets exactly one label, the first that applies:
1. `unresolved` (see Resolution);
2. `solution-gone`: no DR4 solution of astrometric type;
3. `type-vetoed`: the primary solution is of a non-validated type;
4. `insufficient`: the primary solution's parallax <= 0 or parallax S/N <= 5, or a missing
   period, period error or a0 (of the DR4 primary solution, or of the archived DR3 values; note
   2026-11-14, before the release);
5. `rv-vetoed`: the RV veto applies and fires;
6. `mass-below`: M2 <= 3 Msun with M1 = DR4 FLAME `mass_flame` if it is a finite number for that source (a missing column or
   a NULL value counts as absent), else the DR3 `m1_used`;
7. `period-changed`: |P_DR4 - P_DR3| >= 3 sqrt(sigma_P,DR3^2 + sigma_P,DR4^2);
8. `persists`: none of the above.
Also reported, not used for labels: P_DR4/P_DR3 (values near 0.5 or 2 flagged as possible
aliases) and a0_DR4/a0_DR3. For P_DR3 > ~1000 d (beyond the DR3 baseline) the period test is weak.
The counts per label are the result, with the number of survivors to which the RV veto applied
(28 of the 51 have P_DR3 > 1000 d, so for them `persists` rests on period and mass only). No
discovery claim: `persists` means "still a candidate".

**S3-DR4 (new candidates, exploratory).** Membership: DR4 sources with at least one screen row of
M2 > 3 Msun (FLAME M1, fallback 1 Msun) that are not one of the 87 DR3 rows with M2 > 3 Msun after
resolution. Their primary solution is chosen among all their DR4 solutions (fetched for these
sources, not only the screen rows); labels, vetoes and the reported "primary M2 > 3" count use the
primary. Their ids are saved in full (in their own result files, so each stays under 1 MB). They are checked
against literature published after DR3 (including the Gaia DR4 release papers). No prior
expectation and no discovery claim.

## 3. Data (with size estimate)

| Input | Source | Selection | Est. rows / size |
|---|---|---|---|
| BH1, BH2 full NSS rows incl. `corr_vec` | `gaiadr3.nss_two_body_orbit` (TAP gaia) | 3 source_ids | 2 rows, < 10 kB |
| BH coordinates/photometry | `gaiadr3.gaia_source` | 3 source_ids | 3 rows |
| Screen | `nss_two_body_orbit` JOIN `gaia_source` LEFT JOIN `astrophysical_parameters` | astrometric orbit types, `parallax_over_error > 5`, `f_M > 0.25` (computed in ADQL) | to be checked with COUNT first; expect 10^3-10^4 rows, < 5 MB |
| NS candidates | El-Badry et al. 2024 Table 1 (21 source_ids, M2, P) | transcribed from arXiv:2405.00089v2 HTML | 21 rows, in `ns_candidates_elbadry2024.json` |

*Note 2026-11-14 (design plan 008):* the DR3 rerun adds one input, the DR3 position and G of the
109 DR3 ids the study uses (`gaiadr3.gaia_source`, < 200 rows, < 50 kB), archived as
`reference_ids.json` for the DR4 identity check.

The DR3 table has ~443k solutions in total; we never download it. The mass
function is evaluated on the server.

### DR4 addendum to section 3 (2026-11-14, before the DR4 release)

| Input | Source | Selection | Est. rows / size |
|---|---|---|---|
| DR4 schema, tables, columns, solution types | `TAP_SCHEMA`; GROUP BY on `nss_two_body_orbit` | metadata | < 1,000 rows each |
| Resolution of DR3 ids | DR4 `gaia_source` (and the DR3-DR4 cross-match table if published) | 109 unique DR3 source_ids (87 DR3 rows with M2 > 3 incl. BH1, BH2 and the 51 survivors; 21 NS; BH3; literature-labelled) | < 300 rows |
| All solutions of the screen candidates (S3-DR4, and the veto columns of the DR4 candidate table) | DR4 `nss_two_body_orbit` JOIN `gaia_source` LEFT JOIN `astrophysical_parameters`, by id in chunks of <= 500 | sources with a screen row of M2 > 3 not already fetched as targets, controls or resolved ids | counted on the server first; expected a few x 10^3 rows. Stop rule: above 50,000 rows (~15 MB at ~300 bytes/row) S3-DR4 is "not evaluable" and nothing is fetched; no post-hoc narrowing. Bounded anyway by the screen (< 50,000 rows) times the solutions per source |
| Target, control and survivor solutions | DR4 `nss_two_body_orbit` JOIN `gaia_source` LEFT JOIN `astrophysical_parameters` | the resolved ids | < 500 rows |
| Screen | same query as DR3 on the DR4 schema | same cuts | counted on release day; DR3 gave 3,343. Above 50,000: S1-DR4 fails and is recorded first (run-book step 2) |
| DR3 reference values | `results/dr3/` (archived DR3 run: periods and their errors, a0, M1 used; `reference_ids.json` with DR3 position and G of the 109 ids, fetched in the DR3 rerun before 2026-11-25) | committed files | < 1 MB |

The release-day count and its size estimate (rows x ~300 bytes) are written into this table
before the screen is fetched. Result files stay under 1 MB (AGENTS.md section 1): the screen
points are thinned in `run.py` when the screen is large (design plan 008, section 2.4).

## 4. Method

- a0 from Thiele-Innes constants (DR3 doc eq. 7.15); for pseudo-circular solutions
  without G, use G = -AF/B (DR3 doc) via COALESCE in the screen query.
- f_M = (a0 / parallax)^3 / P_yr^2 assumes the companion is dark (photocentre =
  primary). A luminous companion shrinks the photocentre orbit, so this M2 is a
  lower bound in that case; a triple can mimic a massive dark companion.
- M2 solves M2^3 = f_M (M1 + M2)^2.
- Uncertainties (R1, R2): Monte Carlo over the full covariance of
  (parallax, A, B, F, G, P) rebuilt from `corr_vec` in the official `nsstools` order
  (verified by unit test against nsstools), and M1 ~ N(M1, sigma_M1).
- Screen: per-row central M2 with M1 from FLAME (flag when missing; flag giants by
  absolute magnitude and FLAME radius when available).

### DR4 addendum to section 4 (2026-11-14, before the DR4 release)

- Method unchanged; the release is the parameter `PARAMS["release"]` (design plan 008). The vetoes
  and the solution choice used on DR4 are defined in the section 2 addendum.
- A formal run refuses to overwrite results of another release that are not archived in
  `results/<release>/` (both directions).
- DR4 type names, the non-validated types and the `corr_vec` order (`covariance_trusted`) are
  confirmed on release day (run-book steps 1.4-1.5) and logged before the first formal DR4 run.

## 5. Results (2026-11-11)

Pre-registered criteria:

| | Result | Verdict |
|---|---|---|
| R1 | BH1: M2 = 13.3 +2.9/-2.3 Msun (DR3 astrometry only) vs 9.62 +/- 0.18 (astrometry + RV): +1.4 sigma | pass (low power, see s6) |
| R2 | BH2: M2 = 8.52 +0.61/-0.56 Msun vs 8.9 +/- 0.3: -0.6 sigma | pass |
| S1 | 3,343 rows (0.4 MB) of 169,227 astrometric solutions; with published M1, BH1 M2 = 12.8, BH2 M2 = 8.5 (> 3) | pass |
| S2 | 21/21 NS candidates pass `f_M > 0.25` (weakest f_M = 0.41) | pass (weak test, see s6) |
| S3 | 87 solutions with M2 > 3 Msun: 2 known; 5 without pre-registered labels | report |
| D1 | DR4 ADQL generated (`results/dr4_screen_query.json`); schema name to confirm on release day | pass (generation only) |

Post-hoc additions (after the referee review, NOT pre-registered; marked * on the web page):

- **R1b**: against El-Badry et al. 2023a's own *astrometry-only* solution (a0 = 3.00 +/- 0.22 mas,
  M2 = 12.8 +/- 2.0 Msun) we get a0 = 3.02 mas (+0.09 sigma) and M2 = 13.3 Msun (+0.23 sigma).
- **Predicted RV range** from the astrometric orbit (2K, with cos i = (AG - BF)/a0^2) matches
  El-Badry et al. Table E1 for all six listed sources (e.g. 167 vs 171 +/- 10, 49 vs 50 +/- 2 km/s).
- **Vetoes**: (i) non-validated `OrbitalAlternative`/`OrbitalTargetedSearch` solutions; (ii)
  `rv_amplitude_robust` < 0.5 x predicted RV range. On 23 positive controls (BH1, BH2, 21 NS):
  0 vetoed — but only 4 of the 23 have `rv_amplitude_robust`, so veto (ii) is weakly tested on positives.
- Where `rv_amplitude_robust` exists, veto (ii) agrees with the literature verdict in every case
  (vetoes 3640889032890567040, 6281177228434199296, 3664684869697065984; keeps BH2).
- After vetoes and literature: **51 unknown candidates remain, all giants and/or low-significance
  solutions; no unlabelled main-sequence host survives.** No discovery is claimed.
- 4 vetted sources carry more than one NSS solution; joins now use (source_id, nss_solution_type).
- *Note 2026-11-14 (design plan 008):* from now on a control counts as vetoed if its primary
  solution (R-sel, DR4 addendum to section 2) is vetoed, on DR3 as on DR4, instead of any of its
  rows. On DR3 this changes no number: no control row was vetoed and BH1/BH2 have one solution each.
- 0 rows are lost to NULL a0 in the server-side computation.

## 6. Referee notes (independent subagent, 2026-11-11)

Triage of the referee report (verified = checked by us against code, results or the paper text):

| # | Point | Verified | Action |
|---|---|---|---|
| 1 | Pre-registered qc labels hit both real BHs (BH1 `low-significance`, BH2 `giant`); `significance<20` never fires on OA rows | yes | Accepted as a lesson: labels must be validated on positive controls before use (now done for the vetoes). |
| 2 | FLAME M1 for giants inflates M2; a 3-4 Msun MS companion of a giant is hidden, so M2 > 3 is not a BH signature for giants | yes | Accepted limitation; giants reported as a separate class. |
| 3 | S1 as written ("published M1") was not what the code evaluated | yes | Fixed: S1 now uses published M1. |
| 4 | R1 has little power (sigma_comb ~ 2.6 Msun) and compares to the joint fit | yes | Added R1b vs the DR3-only published solution (post-hoc). |
| 5 | S2 cannot fail (weakest f_M 0.41) | yes | Accepted; recorded. The cut's DR4 suitability is not shown by S2. |
| 6 | 6281177228434199296 ruled out by RV follow-up (El-Badry+23a App. E) | yes (paper text) | Literature labels added (`data/literature_vetting.json`). |
| 7 | OA solutions mostly spurious; periods at harmonics of the 63 d precession | partly (OA statements quoted from Arenou+23 / Holl+23 by the referee; not read by us) | Post-hoc type veto, validated on controls. Period-alias veto not adopted (no validated rule). |
| 8 | No AMRF triage for triples; parallax (Eddington) bias at low S/N; P > baseline | yes | Open questions (s7). |
| 9 | D1 not evaluated; 169,227 hard-coded | yes | Fixed: D1 field + full DR4 query; count now from the server. |
| 10 | ADQL SQRT without clip could drop rows | yes | Measured: 0 rows dropped; kept as a test. |

## 7. Open questions

- DR4 release day (2026-12-02): confirm schema via TAP_SCHEMA, run the screen and the vetoes, and
  use DR4 epoch astrometry/RVs to test the 51 surviving (giant / low-significance) candidates.
- Add AMRF triage (Shahaf et al.) to separate triples and luminous companions; validate on controls.
- Propagate parallax uncertainty into f_M for the screen (Eddington bias at parallax S/N 5-20).
- A validated period-alias veto (Gaia scanning-law harmonics) for short-period solutions.
- BH2: compare with its published DR3-only solution (arXiv:2302.07880) as a tight test like R1b.
