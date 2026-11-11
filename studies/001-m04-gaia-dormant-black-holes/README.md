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

## 3. Data (with size estimate)

| Input | Source | Selection | Est. rows / size |
|---|---|---|---|
| BH1, BH2 full NSS rows incl. `corr_vec` | `gaiadr3.nss_two_body_orbit` (TAP gaia) | 3 source_ids | 2 rows, < 10 kB |
| BH coordinates/photometry | `gaiadr3.gaia_source` | 3 source_ids | 3 rows |
| Screen | `nss_two_body_orbit` JOIN `gaia_source` LEFT JOIN `astrophysical_parameters` | astrometric orbit types, `parallax_over_error > 5`, `f_M > 0.25` (computed in ADQL) | to be checked with COUNT first; expect 10^3-10^4 rows, < 5 MB |
| NS candidates | El-Badry et al. 2024 Table 1 (21 source_ids, M2, P) | transcribed from arXiv:2405.00089v2 HTML | 21 rows, in `ns_candidates_elbadry2024.json` |

The DR3 table has ~443k solutions in total; we never download it. The mass
function is evaluated on the server.

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
