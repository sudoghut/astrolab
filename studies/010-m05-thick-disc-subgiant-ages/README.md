# M5 Milky Way thick disc: early formation from subgiant ages

> Write sections 1–4 BEFORE writing run.py (pre-registration). Edit them later only
> with a dated note explaining the change.

**Frozen 2026-11-15** after dual-gate review (gate 1: 3 rounds; Codex: 9 rounds; history in
`design/019-plan_*` section 6). Only a 5-row format trial of the catalogue had been seen.

## 1. Question

Paper: Xiang & Rix 2022, Nature 603, 599, arXiv:2203.12110 ("XR22"). Wiki article (the source of
this pre-registration, part 3):
[Study-010-thick-disc-early-formation](https://github.com/sudoghut/astrolab/wiki/Study-010-thick-disc-early-formation).
Plan: `design/019-plan_*` (section 4 is the design; quotes and numbers verified against the arXiv v1
PDF, including the Extended Data figures).

XR22 derive ages for 247,104 LAMOST/Gaia subgiants (α-enhanced Yonsei-Yale isochrones) and claim:
the age–[Fe/H] plane "splits into two almost disjoint parts, separated at 8 Gyr"; the old (thick)
disc "started 13 Gyr ago, only 0.8 Gyr after the Big Bang" (Extended Data Fig. 1: Gaussian mean
13.03 Gyr, width 1.81 Gyr, for early-phase stars with J_φ > 500 kpc km/s and −1.05 < [Fe/H] < −0.95);
the old-disc sequence follows τ̄ = τ̄0 + a[Fe/H] with τ̄0 = 9.38 Gyr, a = −3.8 Gyr/dex and intrinsic
scatter of 0.82 ± 0.01 Gyr (main text: "less than 0.82±0.01 Gyr"), called an upper limit, so that enrichment from [Fe/H] ≈ −1 to +0.5 took
5–6 Gyr; most old-disc stars formed about 11 Gyr ago, at the time of the GSE merger.

1. **R1.** Without a chemical split, does the age distribution at fixed [Fe/H] show two almost
   disjoint parts, with the young part ending near 8 Gyr?
2. **R2.** Does the catalogue reproduce the 13 Gyr Gaussian mean of Extended Data Fig. 1, and how
   does it depend on selection, the error cut and the age scale?
3. **R3/R4.** Does XR22's linear-plus-scatter model reproduce τ̄0, a, the 5–6 Gyr span and the 0.82 Gyr
   scatter on the α-selected sample (σ_sel), and is the intrinsic scatter of the old sequence below
   0.82 Gyr when the α cut is replaced by a background component?
4. **R7 (descriptive).** What total (deconvolved) age spread does the high-α disc have, compared with
   the asteroseismic "95% of the population was born within ∼1.5 Gyr" (Miglio et al. 2021)?
5. **R5, R6 (descriptive).** Plots of the halo–disc offset at [Fe/H] ≈ −1; age percentiles of
   low-J_φ ("splashed") old-disc stars.

## 2. Hypotheses and decision criteria

R1, R2 and R3/R4 carry verdicts; R7, R5, R6 and the age-scale envelope do not. All rules below are
fixed before the full catalogue is fetched (only a 5-row format trial has been seen). Where a
threshold is computed from the data (R1's null quantile), the procedure, not the number, is fixed in
advance.

### 2.0 Definitions shared by all parts

- **Catalogue columns:** Id, Age, e_Age (Gyr), [Fe/H], e_[Fe/H], [alpha/Fe], e_[alpha/Fe] (may be
  blank), JPHI (kpc km/s), MKcomb.
- **S15:** e_Age/Age < 0.15. **Full:** all rows with finite Age and e_Age > 0. Full is not
  selection-free: XR22's catalogue cuts (M_K, Teff, the 20 Gyr isochrone boundary) are themselves
  age-dependent.
- **Early / late (XR22 eq. 1):** late if JPHI > 1500 and [α/Fe] < 0.16 ([Fe/H] < −0.5) or
  [α/Fe] < −0.16[Fe/H] + 0.08 ([Fe/H] ≥ −0.5); early otherwise. Rows with blank [α/Fe] are counted
  and excluded from every selection that uses [α/Fe]. "Above the α line" means [α/Fe] at or above
  the eq. 1 boundary.
- **Checks:** run.py asserts that the row count is 247,104, that Id is unique and that the median
  JPHI of the full catalogue lies in 1500–2100 (prograde positive). It reports the Full-sample
  correlation of e_Age/Age with Age (diagnostic for the error mechanism, see M0).
- **M0 (observation model).** Latent ages τ are piecewise constant on cells of 0.05 Gyr over [0, 20]
  Gyr (the YY grid edge). For star i, g_i(A | τ) is a Gaussian in A with mean τ and width e_Age,i,
  truncated to [0, 20] and renormalised for each τ; the kernel of each latent cell is integrated over
  the cell (differences of Gaussian CDFs), so narrow kernels of young stars are not under-sampled.
  On S15 the likelihood of star i is L_i = ∫ p(τ|θ) g_i(Age_i|τ) dτ / ∫ p(τ|θ) P_i(τ) dτ, with
  P_i(τ) = ∫ g_i(A|τ) dA from A = e_Age,i/0.15 to 20 (the probability that a star of true age τ
  passes the 15% cut, given its e_Age). On Full the denominator is 1.
  - *Deviation from plan 019 (0.02 Gyr grid):* 0.05 Gyr cells with cell-integrated kernels, because
    the R1 calibration needs about 10³ fits; the main R2 and R3/R4 fits and the R1 fit of the bin
    [−0.3, −0.1) are repeated at 0.02 Gyr (float32, in chunks) as a check.
  - *Compression:* since L_i depends only on (Age_i, e_Age,i), stars are grouped into cells of
    0.05 Gyr in Age and 20 quantile classes of the relative error r = e_Age/Age (per sample or bin),
    and the likelihood is a weighted sum over occupied cells (for the R3/R4 models, also 0.05 dex in
    [Fe/H]). Each cell uses e = (class median r) × (cell-centre Age); on S15 every class median is
    below 0.15, so every cell passes its own cut; the selection term of a star then uses its class's
    r rather than its own (an approximation, stated as a limitation; the cut boundary is at r = 0.15
    for every star, so no star is assigned zero probability). This encodes errors that scale
    with the observed age (the e = r·A mechanism of 2.1) in the real-data fits; the mocks test both
    mechanisms against it.
  - *Limitations:* treating e_Age as given is an approximation (if errors scale with the age
    estimate, S15 is a cut on relative precision and P_i is misspecified; tested below); catalogue
    ages are isochrone posterior summaries shaped by the prior and the grid edge, not Gaussian
    measurements.
  - *Compression check:* the R2 deconvolved fit and the R3/R4 sample-A fit (S15 and Full) are
    repeated with 40 classes and without compression (one cell per star, each star's own e_Age in
    both numerator and selection term); changes are reported.
  - *Edge sensitivity:* (i) refit without stars with Age + 2 e_Age > 20; (ii) an untruncated Gaussian
    observation model. Each verdict below is "robust" only if it holds on S15 and on Full.
- **Fitting.** Maximum likelihood (L-BFGS-B, analytic gradients for the mixtures) from 8 starts per
  model: for a K-component mixture, means at the (j + 0.5)/K quantiles of the observed ages with
  widths 1.5 Gyr and equal weights, plus 7 starts perturbing these (seeded, seed 0); the highest
  likelihood is kept, ties (within 0.01) broken by the earlier start. K is then chosen by BIC.
  Mock fits start from the corresponding data fit (for R1, the bin's data-fit mixture for each K;
  for R3/R4, the fitted parameters) plus 2 seeded perturbations. Uncertainties from a
  finite-difference Hessian at the optimum (flat priors make this the large-sample posterior; plan
  019 spoke of posterior medians, replaced because the grid likelihood is too slow for MCMC at this
  sample size), checked by 50 bootstrap resamples for σ_sel.
- **Error-scale factor f.** If true errors are f × e_Age, two heuristic upper values are computed
  (heuristic because they rest on approximations, not on a full forward model): (i) in the late
  phase (eq. 1), in 0.1 dex [Fe/H] bins from −0.5 to 0.3, using only stars with Age − 2e_Age > 0 and
  Age + 2e_Age < 20 (so that truncation at the grid edges does not reduce the variance), the ratio
  of the observed age standard deviation to the rms e_Age (true ages also spread, so f lies below
  it); (ii) from sample A, √(1 + σ_sel²/⟨e²⟩), where σ_sel is the M0 fit, which models the
  truncation. f_max = min(i, ii), used as a sensitivity value, not as a proven bound. No data here bound f from below; a fixed f_min = 0.8 is used
  (wide binaries find XR22's errors consistent with the scatter of 11 pairs, Shariat, El-Badry &
  Bhattacharjee 2025, arXiv:2510.08675, which does not exclude modest overestimates). Sensitivity
  runs use f ∈ {0.8, 1, f_max}; f = 0.8 is a chosen sensitivity value, not a data-supported lower
  bound, and robustness at f = 0.8 is read in that light.

### 2.1 R1 · The 8 Gyr split (verdict)

- **Sample and bins:** S15 (and Full, calibrated separately) with a valid age, regardless of [α/Fe]
  or JPHI, in five [Fe/H] bins of 0.2 dex: [−0.7, −0.5), [−0.5, −0.3), [−0.3, −0.1), [−0.1, 0.1),
  [0.1, 0.3).
- **Density model:** latent ages = mixture of K Gaussians (K = 1–4), each truncated to [0, 20] and
  normalised, fitted in M0; K by BIC. If BIC picks K = 4, K = 5 is also fitted; a mode counts only if
  a mode within 0.5 Gyr exists in both fits, and d and the edge are taken from the K = 4 fit. Bins
  hitting the cap are listed. Mocks follow the same rule.
- **Modes and valley:** density on the cell grid; a peak is a local maximum with prominence at least
  10% of the lower of the two peaks it separates. The valley is the deepest local minimum between 5
  and 11 Gyr with at least 10% of the latent mass on each side; depth d = density(valley) /
  min(highest peak on each side). No valley → d = 1.
- **Mocks (both null and power):** latent ages drawn from the generating model; relative errors
  r = e/Age resampled from the bin's **Full** sample; two error mechanisms, e = r·τ (errors scale
  with the true age) and e = r·A (errors scale with the observed age, computed iteratively from the
  draw); observed ages Gaussian around τ, truncated to [0, 20]; for S15 the cut e/A < 0.15 is applied
  and draws continue until the bin's observed count is reached. Null and power results are reported
  per mechanism; the bin counts as resolvable only if power ≥ 80% under both (a strict d* lowers the
  power and makes the bin "cannot resolve" rather than failing it).
- **Null and threshold (calibrated jointly with the decision rule):** two unimodal, log-concave,
  non-Gaussian latent families, each fitted to the bin in M0: a skew-normal and a two-piece (split)
  normal (different widths on each side of the mode). 50 mocks per family and error mechanism (four
  null sets). The decision rule is "a valley exists and d < d*" (strict), with
  d* = min(0.25, q_1, …, q_4), where q_s is the 3rd smallest null d of set s, counting ties (q_s = 0.25
  if fewer than 3 mocks of set s have a valley). Because the inequality is strict, mocks tied at q_s
  do not pass, so in every null set at most 2 of 50 mocks (about 5%; binomial uncertainty about ±3%)
  pass the rule, ties included; d* ≤ 0.25 always. The realised false-positive rate of
  each set at d* is reported. *Deviation from plan 019:* the plan asked for a log-concave sensitivity
  check; a non-parametric log-concave deconvolution with truncation and the S15 term is not practical
  here, so a second parametric log-concave family is used and enters the threshold.
- **Power:** per bin, a two-component latent model built from XR22's numbers: an old component
  N(τ̄0 + a·[Fe/H]_centre, 0.82²) with τ̄0 = 9.38, a = −3.8 (8.6 Gyr at +0.2, 11.7 Gyr at −0.6), and a
  young component uniform from 1.5 Gyr to 7 Gyr (XR22's late phase, ending before 8 Gyr), with
  the old weight equal to the fraction of the bin's stars that are early with JPHI > 500 and above
  the α line (minimum 10%, so that the valley rule can apply). The true d of each generating model
  is computed and printed with the old weight; where it exceeds 0.1, the young edge is moved down by
  0.5 Gyr steps until it is ≤ 0.1 (expected only for [0.1, 0.3), to 6.5 Gyr). The edge is not moved
  further if mock power is low (for example because the Gaussian fit smooths the uniform edge); the
  generating models are recorded. 50 mocks; power = fraction passing the same rule
  (a valley and d < d*). Bins with power < 80% are "cannot resolve" and excluded.
- **Recorded per bin:** q_s of each null set, d*, the realised false-positive rates and the power.
- **Per bin:** "almost disjoint" if a valley exists and d < d*. Young-side upper edge = 97.5th
  percentile of the latent mass younger than the valley (our proxy; XR22 give no definition).
- **Verdict:** **reproduced** if at least 3 bins are resolvable, at least 3 of them are almost
  disjoint, and the median young-side upper edge of the almost-disjoint bins lies in 6.5–9.5 Gyr.
  **Undetermined** if fewer than 3 bins are resolvable. **Not reproduced** otherwise.
- **Budget (all mock sets: R1, the R3/R4 recovery, sample B):** R1 has, per bin and sample, 4 null
  sets and 2 power sets of 50 mocks (300 mocks; 3,000 over 5 bins and 2 samples). run.py runs the
  first mock of every set, takes the projected total as the sum over sets of (number of mocks × time
  of that set's first mock) and prints it (the projection covers the mock sets only; the robustness refits are timed and
  reported separately). Sequence: if the total exceeds 4 h, every mock set drops to 30
  (R1 q_s = 2nd smallest with the same strict rule, at most 1 of 30, a nominal 3.3%); the total is then re-projected with 30 per set, and if it still exceeds 8 h, run.py runs in the background
  and the elapsed time is reported. The counts used are written to the results.
- Reported without verdict: the eq. 1 cross-fractions (late stars older than 8 Gyr; early stars
  younger than 8 Gyr), as a descriptive reproduction of XR22 Fig. 2.

### 2.2 R2 · The 13 Gyr mean (verdict)

- **Primary selection (Extended Data Fig. 1):** S15, early (eq. 1), JPHI > 500, −1.05 < [Fe/H] < −0.95.
- **Statistic:** maximum-likelihood Gaussian fitted to the observed ages (no deconvolution; this is
  what the figure inset does), mean μ and width σ with errors.
- **Verdict:** **reproduced** if μ lies in 12.5–13.5 Gyr (a tolerance for the rounded "13 Gyr", not
  an error bar of the paper). Otherwise **not reproduced**. σ is compared with 1.81 Gyr without
  verdict.
- **Sensitivity, reported without verdict:** no early-phase filter; Full instead of S15; JPHI cuts 300
  and 700; error cuts 10% and 20%; the deconvolved latent Gaussian mean in M0 (with the S15
  selection term); the fractions of observed ages above 13.8 Gyr and above 18 Gyr.
- **Age-scale envelope (exploration, no verdict), magnitudes from the literature, not recomputed:**
  isochrone set, MIST +0.5 Gyr (XR22 Extended Data Fig. 4); [α/Fe] systematics of about 0.1 dex in
  LAMOST DD-Payne abundances (Xiang et al. 2019, arXiv:1908.09727) times XR22's sensitivity of 1–2 Gyr
  per 0.2 dex gives ±0.5–1 Gyr; these two are listed and added in quadrature (0.7–1.1 Gyr). Shown
  separately, not added (it overlaps both): a whole-pipeline re-analysis with ages 12.9% younger
  (Chen, Sun & Ye 2025, arXiv:2510.10092; −1.7 Gyr at 13 Gyr). Listed without a propagated age shift
  (no verified sensitivity found): LAMOST [Fe/H]/Teff offsets and the parallax zero point (Lindegren
  et al. 2021, arXiv:2012.01742, about −17 to −21 μas). The envelope is printed next to the 0.8 Gyr
  margin to the Big Bang.

### 2.3 R3/R4 · The old-disc sequence (verdicts)

- **[Fe/H] window:** −1.2 < [Fe/H] < 0.5 for samples A, B and 2e: XR22's sequence runs from
  [Fe/H] ≲ −1 to 0.5, and the halo is "predominately [Fe/H] < −1.2".
- **Sample A (reproduction):** S15, [α/Fe] above the eq. 1 line, JPHI > 500.
- **Model:** latent τ | [Fe/H]_i ~ N(τ̄0 + a[Fe/H]_i, σ²), truncated to [0, 20], in M0 (S15 selection
  term included). The degenerate form without truncation or selection,
  Age_i ~ N(τ̄0 + a[Fe/H]_i, σ² + e_Age,i²) (XR22's), is also fitted.
- **Recovery (before the verdicts are read):** 50 mocks with the real [Fe/H] and e_Age/Age of
  sample A's Full parent, generated from the fitted (τ̄0, a, σ) under both error mechanisms of 2.1,
  with the S15 cut applied. Tolerance: per mechanism, |bias| ≤ 0.1 Gyr in σ and ≤ 0.2 Gyr/dex in a, where bias = mean over
  the 50 mocks of (recovered − generating value); its Monte Carlo uncertainty (standard deviation
  / √n) is reported, and a bias within one such uncertainty of the tolerance is flagged "near
  tolerance" in the results (the rule itself is unchanged). If the e = r·A
  mechanism breaks the tolerance, the S15 verdicts are reported as not robust and the Full fits
  become primary; if the e = r·τ mechanism also breaks it, R3 and R4 are **cannot determine**.
- **R4 (verdict, on σ_sel = the M0 σ of sample A at f = 1):** **reproduced** if |σ_sel − 0.82| ≤ 0.1 Gyr.
  This is the tentative rule of plan 019, frozen without XR22's supplement, which could not be
  accessed. σ_sel is the scatter of an α-selected sample (the α cut trims the young side at fixed
  [Fe/H] and lowers it), not the intrinsic scatter.
- **R3 (verdict):** **reproduced** if |a| × 1.5 dex (the span from −1 to +0.5) lies in 4.5–6.5 Gyr
  (XR22: "5–6 Gyr", ±0.5 Gyr). τ̄0 and a are reported against 9.38 and −3.8 without verdict (XR22's
  values come from all of Fig. 2e, so the like-for-like comparison is the Fig. 2e fit below).
- Each verdict is "robust" only if every one of these fits meets the same criterion individually:
  Full, and the version with a² e_[Fe/H]² added to the variance (which lowers σ; the unpublished
  age–[Fe/H] error covariance is not modelled in either version); for R3 also f = 0.8 and f_max. The
  spans of all these fits are reported side by side. A primary pass with any failing sensitivity fit
  is reported as "reproduced, not robust". Recovery failures act as stated above (Full
  primary if only the e = r·A mechanism fails; R3 and R4 "cannot determine" if both fail). R4 checks XR22's number under XR22's error scale,
  and rescaling the errors moves σ_sel almost one for one (at f_max it tends to 0 by construction),
  so σ_sel at f = 0.8 and f_max is reported without entering R4's robustness. The span is also reported with the sample truncated at
  [Fe/H] < −0.2 and < 0.
- **Fig. 2e fit (no verdict):** S15, early, any JPHI, same model; τ̄0, a and σ compared with XR22's.
- **Intrinsic scatter (verdict):** sample B: S15, early, JPHI > 500, no α cut. Model: mixture of the
  old-sequence component above (weight 1 − f_b) and a background component with a truncated Gaussian
  age distribution whose mean is linear in [Fe/H] (b0 + b1[Fe/H]) with width s, in M0.
  - Identifiability mocks: 50 per error mechanism from the fitted model. Misspecification mocks: 50 per error mechanism in which the
    background follows the empirical background population instead of the fitted Gaussian: the Full
    early stars with JPHI > 500 below the α line are split into three [Fe/H] slices (−1.2 to −0.6,
    −0.6 to 0, 0 to 0.5); in each, a latent age mixture (K = 1–4 by BIC) is fitted in M0; mock
    background stars take [Fe/H] resampled from the slice and latent ages from its fit. Old-sequence
    stars take [Fe/H] resampled from sample B and latent ages from the fitted old component. Each mock
    star then gets a relative error resampled from the Full stars of its [Fe/H] slice, an observed
    age under each error mechanism, truncation to [0, 20] and the S15 cut, in the fitted proportions.
  - Bias of a mock set = mean over its mocks of (recovered σ_int − generating σ_int), signed. There
    are four sets (identifiability and misspecification, each under both error mechanisms). If
    |bias| > 0.1 Gyr in any set, the verdict is **cannot determine** (bias uncertainties reported and
    flagged as for sample A);
    otherwise, with SE = the larger of the Hessian standard error of σ_int and the standard
    deviation of recovered σ_int across the identifiability mocks (both mechanisms), **confirmed** if
    σ_int + 1.645 SE < 0.82 Gyr (plan 019's criterion, with a one-sided 95% margin), **not confirmed**
    if σ_int − 1.645 SE ≥ 0.82 Gyr, and **cannot determine** otherwise (too imprecise to decide).
  - The physical claim depends on the error scale: the fit is repeated at f = 0.8 and f_max, and the
    verdict is "robust" only if all three give the same verdict.

### 2.4 R7, R5, R6 (no verdict)

- **R7:** samples (all S15, early, JPHI > 500): sample A; [α/Fe] > 0.10; [α/Fe] > 0.18 (Miglio et al.
  2021 used [α/Fe] > 0.1 on the APOGEE scale; the LAMOST scale may differ by about 0.1 dex); each
  without a [Fe/H] cut and with [Fe/H] < −0.2. Latent age distribution: Gaussian mixture, K = 1–4 by
  BIC, in M0. Reported: the central 95% width of the latent distribution and the largest latent
  fraction in any 1.5 Gyr window (sliding on the cell grid), at f = 0.8, 1 and f_max. Compared with
  Miglio et al.: 95% born within 1.52 (+0.54/−0.46) Gyr (their deconvolved distribution), as a
  qualified comparison across tracers.
- **R5:** age–[Fe/H] density plots of early stars split at JPHI = 500.
- **R6:** 5th and 10th percentiles (with 200 bootstrap resamples) of observed ages of early stars with
  −1.0 < [Fe/H] < −0.4, for JPHI < 500 and for JPHI > 500; the peak of the observed age distribution
  of early stars with JPHI > 500 (no volume correction; claim 3 is not testable here).

## 3. Data (with size estimate)

| Input | Source (service / URL) | Selection | Est. rows / size |
|---|---|---|---|
| XR22 subgiant catalogue | VizieR J/other/Nat/603.599/table1 via the CfA mirror ASU interface (`vizier.cfa.harvard.edu/viz-bin/asu-tsv`), guarded `ctx.http`, cached | all rows; columns Id, Age, e_Age, [Fe/H], e_[Fe/H], [alpha/Fe], e_[alpha/Fe], JPHI, MKcomb | 247,104 rows; measured 65 bytes/row on a 5-row trial (2026-11-15) → about 16 MB plus a 3 kB header (cap 50 MB; study budget 200 MB) |

The CDS TAP host (tapvizier.cds.unistra.fr) times out from this machine. The 2024 updated catalogue
(320,028 subgiants, NADC) returned 403 and is not used. No other data; comparison numbers are in
`PARAMS`.

## 4. Method

`run.py` fetches the catalogue once, checks it (row count, unique Id, JPHI sign), defines the samples
of 2.0 and runs R1, R2, R3/R4, R7, R5, R6 with the M0 likelihood on the latent grid. Kernels and
selection terms are precomputed for the occupied (Age, e_Age) cells (about 10³–10⁴ per sample, cells ×
400 latent cells), so each likelihood evaluation is a weighted matrix–vector product; kernels stay in
memory and are never written to the project directory. Mock samples for R1 and the recovery checks
use their own generator, independent of the likelihood code. Analytic gradients are used for the
mixtures and the R3/R4 models. Cost estimate: one R1 evaluation about 1–3 ms, one R3/R4 evaluation
about 10–20 ms (cells are nearly one per star); a fit takes a few hundred evaluations. R1 calibration
is 3,000 mocks × about 12–15 fits (K and starts) × 0.3–1 s, about 3–12 h; the R3/R4 and sample-B mocks
(sample A: 50 per error mechanism, 100; sample B: 50 identifiability and 50 misspecification mocks
per mechanism, 200; 300 in all, × 3 starts × about 300 evaluations) add about 3–5 h, plus the robustness refits. The budget
rule of 2.1 therefore probably applies (30 mocks per set, about 60% of these times) and possibly the
background rule. This exceeds the minutes-scale runs of other studies; it is a one-off calibration,
cached results are reused by `explore`, and the main fits (without mocks) take minutes. The Monte Carlo uncertainty of every mock-based rate is written to the
results. All tunable numbers (cuts, bins,
grid, K range, mock counts, thresholds, seeds) are in `PARAMS`, saved with the results. Results go to
`results/` as small JSON files (no per-star output). A web page shows the age–[Fe/H] densities, the
R1 bin densities with valleys, the R2 histogram and fits, the R3/R4 sequence and the R7 spreads.

## 5. Results

Filled after running. Link to `web/index.html` and key numbers in `results/`.

## 6. Referee notes

Independent critique: selection effects, systematics, alternative explanations.

## 7. Open questions

## 8. Exploring via chat

How a coding agent answers "what if" questions about this study without touching `results/`
(rules: AGENTS.md section 2).

| Knob (`PARAMS`) | Meaning | Safe range | Cache only, or new data (size)? |
|---|---|---|---|
| TODO | | | |

- Rerun with an override: `python -m astrolab explore 010-m05-thick-disc-subgiant-ages --tag <topic> --set KEY=VALUE`
  (outputs in `explore/<date>-<topic>/`, not committed; about N s from cache).
- Analyses `run.py` does not cover: a script `explore/<name>.py` with `def main(ctx)`, run with
  `python -m astrolab explore 010-m05-thick-disc-subgiant-ages --tag <topic> --script explore/<name>.py`.
- Results files and keys: TODO (`results/<file>.json`: key - meaning).
- Example questions: TODO (question -> knob or script an agent would use).
- Findings that change what we know go into `log.md` (and, for a paper study, the wiki article)
  on a branch.
