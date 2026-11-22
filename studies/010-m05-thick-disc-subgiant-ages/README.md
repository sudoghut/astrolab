# M5 Milky Way thick disc: early formation from subgiant ages

> 中文：[README.zh.md](README.zh.md) · Web page online: [https://sudoghut.github.io/astrolab/studies/010-m05-thick-disc-subgiant-ages/web/](https://sudoghut.github.io/astrolab/studies/010-m05-thick-disc-subgiant-ages/web/)

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
  *Amendment (2026-11-15, after the smoke test, before the formal run; numerical, no criterion
  changed):* the R1 **data** fits (K = 1–4 and the K = 5 mode-matching fit) use 40 starts instead
  of 8 (`PARAMS["nstart_r1_data"]`), each bin with its own seeded random stream. Reason: a
  start-convergence check (5 seeds × 8 starts and 2 seeds × 40 starts per bin) found that with 8
  starts 3 of the 10 bins sometimes stopped in a worse local optimum (higher NLL by about 140–580)
  or missed a mode in the K = 5 fit, changing that bin's d (e.g. 0.454 vs 1.000); with 40 starts
  all seeds agreed. Disclosure: the smoke test had already shown the R1 data d values of both
  start settings; the change selects the higher-likelihood fit, as the 2.0 rule already intends,
  and is not chosen by its effect on d. Mock fits are unchanged (data fit + 2 perturbations).
  The same 40 starts are used for the other 1-D mixture data fits (R7 and the background slices
  that generate the sample-B misspecification mocks), and the sample-B f = 0.8 and f_max data fits
  use the 8 starts of this rule plus the f = 1 optimum (code review, same date). Mock fits draw
  their start perturbations from their own mock set's random stream.
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
- *Clarifications (2026-11-15, code review, before the formal run; the rules above did not cover
  these cases):* (i) if only the e = r·τ mechanism breaks the tolerance, S15 stays primary as
  stated and the result carries the flag "e = r·τ recovery failed"; (ii) when Full is primary, its
  robustness set is Full's own variants (a² e_[Fe/H]² added; for R3 also f = 0.8 and f_max refitted
  on Full), since the S15 verdicts are then declared not robust.
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

### 2.5 R-SEL (addendum 2026-11-17, T-031), pre-registered before any fit with the new selection term

This addendum registers a **re-test** of R1, the R3/R4 recovery and verdicts, and the sample-B
intrinsic scatter under an S15 selection term consistent with the error mechanisms of the mocks.
It does not change sections 2.0–2.4 or the verdicts recorded in section 5; those stay as the
outcome of the original pre-registration. Everything not restated here follows 2.0–2.3 unchanged.
The re-test labels carry the suffix "-SEL" (R1-SEL, R3-SEL, R4-SEL, intrinsic-SEL).

- **Why.** (1) M0's S15 term (2.0) is P_i(τ) = ∫ g_i(A|τ) dA over A ≥ e_Age,i/0.15, i.e. it treats the
  error as fixed and makes the pass probability rise with τ. In both mocked mechanisms the relative
  error r is drawn independently of τ, and then the cut does not depend on τ: under e = r·A it is
  the cut r < 0.15; under e = r·τ, e/A = r/(1 + r z) with z the standard-normal deviate, again
  independent of τ. The term therefore over-weights young latent ages and inflates widths; the
  referee's synthetic check gave a σ bias of +0.31/+0.29 Gyr with the term and −0.02/−0.03 Gyr
  without it (section 6, point 1), matching our recovery bias (+0.28/+0.25 Gyr) and the sample-B
  biases (+0.13 to +0.18 Gyr). (2) In the data, however, r is not independent of age: the
  Full-sample correlation of e_Age/Age with Age is +0.16 (`summary.json`, `checks.corr_relerr_age`),
  so the pass fraction may genuinely depend on age, and mocks that draw r independently of τ do not
  test that case. (3) R1's power model floors the old weight at 10%, which cannot pass the 10%
  side-mass rule (section 6, point 2). (4) The original run used 30 mocks per set (budget fallback),
  and R1's line between "undetermined" and "not reproduced" sits on that Monte Carlo noise (point 4).

- **Seen before this addendum (disclosure).** Everything in sections 5–7 and in `log.md`, in
  particular: all recorded verdicts; the R1 data d values, K, edges and powers of every bin under
  the old term (S15 d = 0.295, 0.454, 0.492, 1, 1; Full d = 0.386, 0.579, 0.479, 1, 1) and the
  power-model raw old weights (S15 0.415, 0.296, 0.153, 0.094, 0.121; Full 0.427, 0.308, 0.160,
  0.097, 0.122); the sample-A fits under
  the old term (S15: τ̄0 = 8.07, a = −4.00, σ = 2.67, span 6.00; Full: 8.70, −4.01, 2.58, 6.01) and
  every sample-A variant (span 5.7–6.2, σ_sel 2.4–2.7); the recovery biases; sample B's
  σ_int = 0.79 ± 0.02 Gyr with f_bg = 0.53 and its mock biases; the deconvolved R2 means (12.19 S15,
  12.59 Full); f_max = 2.81; R7 widths; corr(e/A, Age) = +0.16 and the median relative error
  0.075; the referee's synthetic-check numbers; the smoke-test diagnosis (log 2026-11-15) and the
  timings (smoke projection 4.6 h and formal projection 4.29 h at 50 per set; 2.55 h for the 30-per-set
  mock stage; total run 3.53 h). **Not seen:** any pass-fraction table P_pass (defined below) on the
  data, and any fit, mock or likelihood value with either new term. Because the old-term results are
  known, the re-test is not blind to the data: a term that removes the upward σ bias is expected to
  lower σ_sel and σ_int (σ_int = 0.79 is already below 0.82), so an "intrinsic-SEL confirmed" label
  is foreseeable in direction. Further foreseeable directions: (i) Full's R1 data fits are
  unchanged by the re-test (denominator 1, same random streams), with d = 0.386, 0.579, 0.479, 1, 1,
  all above the cap 0.25, so R1-SEL cannot be "reproduced, robust", and more resolvable bins push
  R1-SEL towards "not reproduced"; (ii) the Full sample-A fit is unchanged (span 6.01, inside the R3
  band; σ = 2.58, failing R4), so R4-SEL cannot be "reproduced, robust", and "R4-SEL not
  reproduced" is foreseeable from σ_sel ≈ 2.67 minus a bias of about 0.25 Gyr; (iii) R3-SEL's Full
  span is inside its band. The rules below were chosen from the mechanism argument and the
  referee's points, not from their expected effect on any label.

- **SEL-0 Parent sets and the pass table.**
  - *Parent* Π of an analysis sample = the same selection on Full (valid rows) without the S15 cut:
    R1 bin b on S15 → Full ∩ bin b; sample A → Full ∩ above the α line ∩ JPHI > 500 ∩ [Fe/H] window
    (`selA_full`); sample B → Full ∩ early ∩ JPHI > 500 ∩ window (`selB_full`); Fig. 2e → Full ∩ early
    ∩ window; R2 deconvolved → the R2 primary selection on Full.
  - *[Fe/H] slices:* for samples A, B and Fig. 2e, the three slices of 2.3 ([−1.2, −0.6), [−0.6, 0.0),
    [0.0, 0.5)), assigned by lo ≤ [Fe/H] < hi; for R1 bins and R2 the whole sample is one slice.
  - *Age bins:* observed-age bins of 1 Gyr, [k, k + 1) for k = 0…19, with Age = 20 in the last bin.
    Within each slice, bins are merged deterministically: walk from the youngest bin upward,
    accumulating consecutive bins into a group until its parent count is ≥ n_min = 200, then close
    the group; if the last (oldest) group ends with fewer than 200 parent stars, merge it into the
    previous closed group (if there is none, the slice is one group). The merged groups are the
    *pass bins* of that slice.
  - *Pass fraction:* π_s,b = (number of parent stars of slice s in pass bin b with e_Age/Age < 0.15) /
    (number of parent stars of slice s in pass bin b); parent rows have Age > 0 (Full requires finite
    Age and e_Age > 0; a row with Age ≤ 0 has no relative error and is excluded from Π). No smoothing: P_pass,s(A) = π_s,b for A in
    pass bin b, piecewise constant in observed age. (A bin that contains an S15 star has π > 0
    because S15 ⊂ Π.) The tables are written to the results with their counts.

- **SEL-1 Selection terms in M0.** Numerators are unchanged (2.0, including compression: each cell's
  error e = class-median r × cell-centre Age, times f in the f-variants). Only the S15 denominator
  changes; on Full the denominator stays 1.
  - *Primary, term E (empirical, age-dependent):* for cell i in slice s,
    P_i(c) = Σ_b π_s,b · [Φ((u_b − m_c)/e_i) − Φ((l_b − m_c)/e_i)] / Z_i(c), where c is a latent cell
    with midpoint m_c, (l_b, u_b) are the pass-bin edges (in the truncated model the first bin starts at 0 and the last
    ends at 20, the range of g_i), e_i = f·e of the cell, and Z_i(c) is the
    same truncation normaliser over [0, 20] as in `m0.kernels` (midpoint convention, as the old
    term). The likelihood of cell i is ∫ p(τ|θ) g_i(Age_i|τ) dτ / Σ_c p_c(θ) P_i(c), i.e. the
    denominator ∫ p(τ|θ) ∫ g_i(A|τ) P_pass(A) dA dτ. In the untruncated variant Z = 1 and the first
    and last pass bins extend to −∞ and +∞. The floor rules of `m0.floored_terms` apply unchanged.
    Rationale and assumption: term E assumes P(pass | A, τ) = P_pass(A), i.e. given the observed
    age, passing S15 does not depend further on the latent age. Then
    p(A, pass | θ) = p(A|θ)·P_pass(A); the factor P_pass(Age_i) in the numerator does not depend on θ
    and drops, leaving this denominator. In the mocks (r keyed by τ, SEL-2) this assumption is
    violated to second order (the pass probability depends on τ through r and, under e = r·τ, on z),
    and the mocks measure the effect. Using the star's own kernel g_i (rather than a
    population-averaged one) keeps the code structure of 2.0; it is a first-order approximation (the
    selected stars' errors are smaller than their parents'), also measured by the mocks, and it
    reduces to term N when π is flat.
  - *Secondary, term N (none):* denominator 1 on S15. This is the limit for r independent of τ under
    both mocked mechanisms away from the age range's ends (the pass probability is then a constant and
    drops out); it is not exact under e = r·τ, where the numerator's shape changes slightly and, near
    0 and 20 Gyr, truncating observed ages to (0, 20) makes the pass probability depend on τ; the mocks
    measure both effects.
  - The old term of 2.0 is not fitted again in the re-test (its results are in section 5).
  - Verdicts use term E. Term N is a sensitivity: each -SEL label is also computed with term N, by the
    same rules and with its own mocks, and the label is reported as "selection-term robust" if the
    two bare labels agree (the verdict without its robustness qualifiers) and "selection-term
    sensitive" otherwise. Term N never replaces term E for a label.

- **SEL-2 Mock generator (all re-test mock sets).** As 2.1/2.3 except how r is drawn and how the
  mock's own term is built.
  - *r with the data's age dependence:* each mock star first gets its latent age τ (and [Fe/H] where
    relevant, as in 2.3: resampled from the parent Π of the sample, or from the background slice for
    misspecification background stars); its r is then drawn uniformly with replacement from the
    parent stars of the same slice whose observed Age lies in the pass bin (data edges, SEL-0) that
    contains τ (the pools are the data parent's pass bins, each with at least 200 stars by the merge
    rule, so no pool is empty; catalogue ages lie in [0, 20], and mock stars are kept only with observed
    ages in (0, 20), so every observed age has a pass bin in every variant). The observed age and
    catalogue error follow under each mechanism as in `mocks.observe`
    (e = r·τ or e = r·A). Keying by τ, not by the star's observed age, avoids a circular draw; under
    e = r·A the true pass probability of a star of latent age τ is then exactly π_s,b(τ), while under
    e = r·τ it differs (the cut depends on z), so the two mechanisms test term E under two
    misspecifications (a conservative test).
    This replaces the joint resampling of ([Fe/H], r) rows (sample A and identifiability mocks) and
    the slice pools of the misspecification mocks; old-sequence and background stars use the same
    rule.
  - *Mock parent and mock term:* the generator keeps every drawn star with an observed age in
    (0, 20) in draw order; the mock parent is that sequence up to and including the star that
    completes the target S15 count, i.e. the number of S15 stars of the data sample being mocked (for
    S15 mock sets); later draws of the same batch are discarded. The mock's term E is built from the mock
    parent by the SEL-0 procedure (merging recomputed on the mock parent counts), so the mocks test
    the whole procedure, including the estimation of π. Full mock sets (R1 on Full) need no parent.
  - *Generating models:* the data fits of the term under test (term E mocks from the term-E data fits,
    term N mocks from the term-N data fits); R1 null and power models as in 2.1 with SEL-3's changes;
    the misspecification background fits (Full, denominator 1) as in 2.3, refitted with the same
    40-start rule.
  - *Diagnostic (no verdict):* the sample-A recovery is also run with the original generator (r drawn
    with [Fe/H] from the parent rows, independent of τ), under both mechanisms and both terms
    (4 sets), to check the referee's synthetic result on the real sample.

- **SEL-3 R1-SEL.** Rules of 2.1 unchanged (bins, mixtures K = 1–4 with the K = 5 rule, 40 starts for
  data fits, mock fits from the data fit + 2 perturbations, valley and side-mass rule, two null
  families × two mechanisms, d* = min(0.25, q_1…q_4) with q_s the 3rd smallest null d of 50, strict
  d < d*, power ≥ 80% under both mechanisms, verdict rule), with three variants: S15 with term E
  (primary), S15 with term N, and Full (denominator 1; changes only through SEL-2 mocks, the power
  floor and the mock count). Changes:
  - *Power floor:* the old weight is max(raw fraction, **0.12**) instead of max(raw, 0.10). Reason,
    from the rule's arithmetic only: the floor exists "so that the valley rule can apply" (2.1); with
    weight w the generating model's old-side mass is w·(1 − ε), with ε the old component's tail below
    the valley, and the 10% side-mass rule needs w·(1 − ε) ≥ 0.10. For the power models' young edges
    (6.5–7 Gyr) and old means (8.6–11.7 Gyr), ε ≤ 3%, so w ≥ 0.103 is needed; 0.12 is the next round
    value with a small margin. With 0.12 only the bin [−0.1, 0.1) is raised (seen raw fractions:
    S15 0.094, Full 0.097); all other bins keep their raw fractions.
  - *Floor sensitivity (fixed in advance, no label change):* R1-SEL's per-bin power and the verdict
    are also computed with a floor of 0.20 (which also raises [−0.3, −0.1) and [0.1, 0.3)) and
    reported next to the primary; the R1-SEL label is the one at 0.12. The null sets and d* are
    shared; new power sets are run only where the generating model changes: bins [−0.3, −0.1),
    [−0.1, 0.1) and [0.1, 0.3) in each of the three variants × two mechanisms = 18 sets of 50
    (900 mocks), numbered after the 106 main sets (SEL-8).
  - *Edge loop:* the young edge starts at 7.0 Gyr and is lowered in 0.5 Gyr steps (candidate edges 7.0, 6.5, …, 2.0 Gyr;
    the valley and d of each generating model are evaluated on the 0.05 Gyr latent grid) only while the generating model **has a valley** with true d > 0.1. If at 7.0 Gyr the
    generating model has no valley (d = 1, e.g. by the side-mass rule), the edge is not moved. If a
    valley exists at 7.0 Gyr with d > 0.1 but disappears at a lower edge, the last edge that had a
    valley is kept (and reported). The loop stops at the first edge with a valley and d ≤ 0.1, which
    is then the power model. If the loop ends without a valley with d ≤ 0.1 (either case above, or 2.0 Gyr
    reached), the bin's power model is flagged "power model invalid" and the bin is "cannot resolve"
    by construction (reported separately from low-power bins). (The original loop treated "no
    valley" as "d too large" and walked [−0.1, 0.1) down to 2.0 Gyr.) Checked offline on the
    generating models only (m0.tn_cells and m0.valley on the 0.05 Gyr grid, no data, using the seen
    raw fractions): with the 0.12 floor every bin of S15 and Full has a valley at 7.025 Gyr with
    true d ≤ 0.02 at edge 7.0 (old-side mass ≥ 0.118), except [0.1, 0.3), whose d = 0.151 at
    7.0 Gyr becomes 0.038 at 6.5 Gyr (as in the original run); the same holds at the 0.20 floor.
    The true d values are printed by run.py.
  - *Mocks:* 50 per set, SEL-2 generator, S15 term-E and term-N mocks fitted with the term under test.
  - *Labels:* R1-SEL = the 2.1 verdict on S15 term E. "Robust" as in 2.1 if Full gives the same
    verdict; "selection-term robust" if S15 term N gives the same bare verdict.

- **SEL-4 R3-SEL / R4-SEL.** Sample A fitted with term E (primary) and term N, same model, starts and
  Hessian errors as 2.3. f_max is recomputed by the 2.0 definition with σ_sel from the term-E fit
  (f_ii); f_i is unchanged (late-phase ratios do not depend on the term). Recovery: 50 mocks per
  mechanism per term (SEL-2 generator, generating values = that term's fit), tolerance per mechanism
  |bias σ| ≤ 0.1 Gyr and |bias a| ≤ 0.2 Gyr/dex with the Monte Carlo uncertainty and the
  "near tolerance" flag, and the 2.3 rules and clarifications for primacy: if e = r·A passes, S15
  (term E) is primary (with the flag if only e = r·τ fails); if only e = r·τ passes, the Full fit is
  primary and its own robustness set applies; if both fail, R3-SEL and R4-SEL are **cannot determine**.
  Verdict rules unchanged (R3: |a| × 1.5 in 4.5–6.5 Gyr; R4: |σ_sel − 0.82| ≤ 0.1 Gyr at f = 1).
  Robustness sets as 2.3, with every S15 fit using term E (Full; a² e_[Fe/H]² added; for R3 also
  f = 0.8 and the recomputed f_max). The same procedure with term N gives the term-N labels for the
  selection-term qualifier; for term N's own robustness set, f_max is recomputed from term N's
  σ_sel, and the f-refits use term N. The qualifier compares the bare labels. The span truncated at [Fe/H] < −0.2 and < 0, the edge-drop, untruncated,
  0.02 Gyr grid, 40-class and no-compression fits are repeated with term E and reported without
  verdict; the 50 bootstrap resamples of σ_sel are run for term E only.

- **SEL-5 intrinsic-SEL.** Sample B's mixture (2.3) fitted with term E (primary) and term N (8 starts
  around the same term's sample-A fit; the f-variants add, as in 2.0, sample B's own f = 1 optimum
  under the same term).
  Identifiability and misspecification mocks: 50 per mechanism per term (8 sets), SEL-2 generator.
  Rules unchanged: cannot determine if |bias| > 0.1 Gyr in any of the term's four sets; otherwise SE
  = max(Hessian SE, s.d. of recovered σ_int over the term's identifiability mocks of both mechanisms)
  and confirmed if σ_int + 1.645 SE < 0.82, not confirmed if σ_int − 1.645 SE ≥ 0.82, cannot
  determine otherwise; "robust" if f = 0.8 and the recomputed f_max give the same label (both refits
  with term E); "selection-term robust" if term N gives the same bare label (term N's own f-refits
  use term N and f_max recomputed from term N's sample-A σ_sel).

- **SEL-6 Reported without verdict.** The pass tables (counts, π per slice and bin); the R2
  deconvolved latent Gaussian (S15 term E and term N, next to 12.19 and 12.59); the Fig. 2e fit with
  term E; the SEL-2 diagnostic; per set, the mean pass rate of the mocks against the data's S15
  fraction of the parent. R2's verdict (observed ages, no selection term) and R7 are not re-run.

- **SEL-7 Sensitivity variants (data fits only, no mocks, no verdict).** Term E with (i) pass bins of
  0.5 Gyr (same merge rule, n_min = 200) and (ii) one slice for samples A and B (no [Fe/H] split), for
  sample A (σ_sel, span) and sample B (σ_int). Reported next to the primary values.

- **SEL-8 Mock count, seeds, budget, runtime and memory.**
  - *Mock count:* 50 per set, with **no reduced fallback** (the 4 h / 30-mock rule of 2.1 does not
    apply to the re-test). R1 q_s is the 3rd smallest of 50.
  - *Sets:* R1: 3 variants × 5 bins × 6 sets = 90; sample A recovery: 2 terms × 2 mechanisms = 4;
    sample B: 2 kinds × 2 mechanisms × 2 terms = 8; SEL-2 diagnostic: 4. In all 106 main sets,
    5,300 mocks, plus the 18 floor-sensitivity power sets (900 mocks).
  - *Seeds:* sets are numbered k = 0, 1, … in this loop nest (outermost first): R1 sets: variant
    (S15-E, S15-N, Full) > bin (in order) > kind (null_sn, null_sp, power) > mechanism (rtau, rA),
    k = 0–89; then sample-A recovery: term (E, N) > mechanism, k = 90–93; then sample B: term (E, N) >
    kind (identifiability, misspecification) > mechanism, k = 94–101; then the SEL-2 diagnostic:
    term (E, N) > mechanism, k = 102–105 (106 sets); then the floor-0.20 power sets of SEL-3:
    variant > bin (the three listed there, in order) > mechanism, k = 106–123. Mock j (j = 0…49) of set k uses its own
    stream `default_rng([seed, 31, k, j])`; data fits keep the 2.0 streams, with R1 sample codes
    0 = S15 term E, 1 = Full, 2 = S15 term N. Per-mock streams make an interrupted run resumable with
    identical results.
  - *Runtime estimate:* the original 66 sets averaged about 4.7 s per mock (projection 4.29 h for
    3,300 mocks; 2.55 h for the 1,914 mocks after the 66 timing mocks, which are not included).
    Splitting that average between R1 (60 sets) and samples A/B
    (6 sets) is not recorded; a consistent range is 3.5–4.5 s per R1 mock and 7–17 s per A/B mock.
    Term E adds one pass table and one P matrix per mock: about 21 Gaussian-CDF evaluations per
    (cell, latent cell) pair, < 0.1 s for 1-D R1 cells and about 1–3 s for the grouped samples. Hence:
    R1 4,500 mocks ≈ 4.4–5.6 h; floor-sensitivity 900 mocks ≈ 0.9–1.1 h; A/B 800 mocks ≈ 1.9–4.5 h;
    mocks in all ≈ 7.2–11.2 h; data fits
    (R1 15 bin-variants at 40 starts, samples A/B with both terms and their variants, bootstrap)
    ≈ 1–1.5 h (the original non-mock stage took about 1 h including R7). Total ≈ 8.2–12.7 h, run in the
    background on an otherwise idle machine (no other study's run at the same time; recorded in
    `log.md`). run.py times the first mock of every set and prints the projection; the check is
    repeated after every completed set, with projection = elapsed + Σ over remaining sets of (their mocks × the mean time per
    mock of finished sets of the same kind: R1, sample A/B, diagnostic; a kind not yet started uses the
    initial first-mock estimate of its sets); whenever it exceeds 16 h, run.py stops before the remaining mocks and the user is
    asked (mock counts are never reduced; resuming needs the user's explicit consent, recorded in
    `log.md`, and the same check, on total elapsed time across sessions, continues after resuming); every finished mock is already checkpointed, so a stop keeps
    all completed mocks, including those of a partly finished set, and a resumed run continues from them;
    no -SEL label is computed until every set has its 50 mocks.
  - *Memory:* the grouped likelihoods hold K and P (cells × 400 latent cells, float64) plus about
    four temporaries of the same size in `_ll_q`; sample B (≈ 79,000 S15 stars, tens of thousands of
    cells) needs about 1 GB at peak, the no-compression checks about 1.5 GB. Term E does not add a
    persistent array (it replaces P) and needs one extra temporary while P is built (accumulated
    edge by edge). Models are released after each fit, mocks run in one process, sequentially, and the
    run logs the peak working set per stage; the first formal run was stopped for low memory
    (log 2026-11-16), which is why the run must not share the machine.
  - Mock results are checkpointed per mock in the system cache directory (not the project
    directory), keyed by the PARAMS and code version, so a stopped run resumes.

- **SEL-9 Relation to the recorded verdicts and reporting.** The section 5 verdicts (R1 undetermined,
  R3/R4 and intrinsic scatter cannot determine) are the outcome of the original pre-registration and
  stay as recorded. The -SEL labels are reported in a new results subsection "Re-test with a
  consistent selection term (T-031)", next to (not replacing) them, each with its qualifiers
  (robust / not robust; selection-term robust / sensitive) and with term-N values side by side. The
  claim entries and wiki report both: the original labels as the pre-registered outcome and the
  -SEL labels as the current reading. A -SEL label that differs from the recorded one is not
  described as correcting it. Results go to new files (`r1_sel.json`, `r34_sel.json`, `sel.json`);
  `r1.json`, `r34.json` and `summary.json` are not overwritten.

- **SEL-10 Limitations.** P_pass is a function of observed age estimated on the parent, which is
  itself selected (catalogue cuts, 2.0); it absorbs any dependence of r on age that comes from the
  error mechanism itself (under e = r·τ with r independent of τ, stars scattered to older A pass more
  often, so π can rise with A without a true τ dependence): the e = r·τ mocks test exactly this.
  Keying r by τ in the mocks approximates the data's dependence on observed age. The star's own
  kernel is used in the denominator. The R1 power floor makes the power model of bin [−0.1, 0.1)
  slightly richer in old stars (0.12) than its α-selected fraction (0.094 S15, 0.097 Full). Mock fits still start from the data fit with
  3 starts (section 6, point 5).

### 2.6 R1-SEL-FIT (addendum 2026-11-20, T-049), pre-registered before any mock fit with the new starts

This addendum registers a rerun of R1-SEL (2.5, SEL-3) in which every mock fit also uses
data-independent starts. It changes nothing else in 2.0–2.5 and no recorded label; the label it
produces is called R1-SEL-FIT.

- **Why.** The T-045 diagnostic (section 5.1, post hoc) regenerated the six power sets of bin
  [−0.7, −0.5) and found that the mocks without a valley are local optima of the mock fits: the
  original fits (the data fit's parameters plus 2 perturbations, 2.0 "Fitting" and SEL-3) gave an NLL that rises from some
  K to K + 1 in 27–38 of 50 mocks per set, which the global optima of nested models cannot do; with 8
  data-independent starts per K the bin's power was 1.00 in all six sets (recorded 0.58–0.88). The
  null sets and the other bins were not refitted, so whether R1-SEL's line between "undetermined"
  and "not reproduced" moves is open.

- **Seen before this addendum (disclosure).** Everything in sections 5–7 and `log.md`, in particular:
  the R1-SEL results of every bin and variant (data d: S15 term E 0.410, 0.579, 0.502, 1, 1; term N
  0.367, 0.580, 0.482, 1, 1; Full 0.386, 0.579, 0.479, 1, 1; d* = 0.25 (the cap) everywhere; no
  valley in any of the 3,000 null mocks; powers per bin and mechanism as in section 5.1; verdicts
  undetermined / not reproduced / undetermined); the recorded d values of every power mock (in the
  two resolvable bins up to 0.04 and 0.14); and the T-045 refit of bin [−0.7, −0.5)'s power sets
  (power 1.00 in all six, K = 3 or 4, 95th percentile of d at most 0.017). No null set and no other bin has been fitted
  with the new starts.

- **What changes (mock fits only).** In every R1 mock fit (null and power sets, all five bins, all
  three variants, primary and floor-0.20 power sets), for each K = 1–4 the fit is done twice on the
  same catalogue and model: (o) exactly as in SEL-3 (`run.fit_mixtures` from the data fit's
  parameters with 2 perturbations, then `run.shape_from_fits`, on the SEL-8 stream of the mock); (i)
  from 8 data-independent starts per K (`m0.mixture_starts` on the mock's compressed cells,
  `model.cells.A` and `model.cells.w`: the 2.0 quantile start plus 7 seeded perturbations) on a
  separate stream, consumed in the order K = 1, 2, 3, 4, then 5, `default_rng([seed, 45, k, j])` (the T-045 stream, so the
  power sets of bin [−0.7, −0.5) repeat T-045's fits). For each K the fit used is (i) if its NLL is
  lower than (o)'s by more than 0.01 (the tie rule of 2.0's start selection), else (o); a
  non-finite (i) NLL is never selected, and the existing non-finite-mock rule (`selaux.nonfinite`)
  applies unchanged. K is chosen by
  BIC on these fits. If K = 4 is chosen, K = 5 is fitted from 8 data-independent starts on stream (i)
  and compared in the same way with (o)'s K = 5 fit when (o) chose K = 4 (otherwise the (i) fit is
  used; deliberately, to repeat T-045, the data fit's K = 5 parameters are not added as a start in
  that case); the 2.1 mode-matching rule then applies. The catalogue (drawn before any fit) and (o) are
  unchanged, so (o) must reproduce the recorded R1-SEL d and valley flag of every mock.
- **Unchanged.** Data fits (40 starts, the 2.0 streams), power models (primary floor 0.12 and the
  0.20 sensitivity), null families, mock generator (SEL-2), set numbering and mock streams (SEL-8),
  50 mocks per set (90 main sets and 18 floor-sensitivity sets, 5,400 mocks), the d* rule, strict
  d < d*, power ≥ 80% under both mechanisms, the 2.1 verdict rule and the SEL-3 labels and
  qualifiers. R1-SEL-FIT = the 2.1 verdict on S15 term E with the new mock fits; "robust" if Full gives
  the same verdict; "selection-term robust" if S15 term N gives the same bare verdict; the floor-0.20
  verdict (with the d* of the new null fits, the null sets being shared as in SEL-3) is reported next
  to it without changing it.
- **Checks (a failure makes R1-SEL-FIT "not evaluable (reproduction)", reported and investigated
  before anything else).** Every data fit equals `r1_sel.json`: `data_fits.<variant>_<bin>` (the
  K = 1–4 mixture parameters, the skew-normal and split-normal parameters and both power models) and
  `variants.<variant>.bins[bin]` (d and K), each number within an absolute 10⁻⁹; for every mock, (o)'s
  d equals the recorded value within an absolute 10⁻⁹ and its valley flag is the same.
- **Reported (no verdict).** Per set: power or false-positive rate, q_s and d* under the new fits next
  to the recorded ones; the number of mocks whose valley flag or pass changes; the number of mocks
  whose (o) NLL rises with K and whose new NLL does; the K chosen under (o) and under the new fits;
  the time per mock.
- **What the outcome can be (stated now).** The data fits do not change, so no bin can become
  almost disjoint (data d ≥ 0.367 against d* ≤ 0.25; the metal-rich bins have no valley), and
  "reproduced" is impossible. The question is only whether at least three bins are resolvable
  ("not reproduced") or fewer ("undetermined"). Expected: bin [−0.7, −0.5) resolvable in all three
  variants (T-045). The open part is the null sets: better fits may find valleys in some null mocks
  and lower d* below its cap; bins [−0.5, −0.3) and [−0.3, −0.1) stay resolvable if, under each
  mechanism, at least 40 of their 50 new power mocks have a valley with d < d* (under the original
  fits all have a valley and all d ≤ 0.04 and ≤ 0.14). The metal-rich bins may gain
  power if their power mocks' fits improve; they cannot become almost disjoint. Our expectation is
  "not reproduced" in all three variants, which would make R1-SEL-FIT "not reproduced (robust;
  selection-term robust)".
- **Runtime and machine.** T-045 measured about 4.2 s per mock for S15 term E and about 2.4 s for
  term N and Full, both fits included (its run log; `sel.json` gives 1.27 s per R1 mock for the original
  fit alone): 5,400 mocks ≈ 4.5–5 h, plus the 15 R1 data fits (≈ 25 min) and the pass tables; no data download, cache only. The run is started only on an otherwise idle
  machine (the R-SEL mock stage peaked at a 6.26 GB working set, log 2026-11-20). Checkpoints per mock in the system cache (`s010_selfit_mocks`), keyed by PARAMS and code;
  the SEL-8 projection rule applies with a stop at 12 h (resuming needs the user's consent, recorded
  in `log.md`); no label is computed until every set has its 50 mocks.
- **Reporting.** Results in a new file `r1_selfit.json`; `r1_sel.json` and the recorded R1 and
  R1-SEL labels are not overwritten. Section 5 reports R1-SEL-FIT next to R1-SEL as the rerun with
  improved mock fits, not as a correction of it; the claim and the wiki report both.
- **Code (none exists yet).** A new part `"selfit"` in `PARAMS["parts"]` runs only this rerun (pass
  tables of the R1 bins, R1 data fits, the 108 R1 sets); `PARAMS["selfit_seed_tag"] = 45`,
  `PARAMS["selfit_nstart"] = 8`, `PARAMS["selfit_stop_h"] = 12`; the checkpoint key leaves out
  `selfit_stop_h` and `parts`, as `_sel_key` leaves out `sel_stop_h` and `parts`.

### 2.7 R1-ERR (addendum 2026-11-21, T-054), pre-registered before any mock with scaled errors

This addendum registers an error-scale power test of R1-SEL-FIT (2.6). It changes nothing in
2.0–2.6 and no recorded label: R1, R1-SEL and R1-SEL-FIT keep their labels. R1-ERR produces a label
of its own, which says how far R1-SEL-FIT's label depends on the age-error scale. It is not a verdict
on XR22's claim.

- **Why.** R1-SEL-FIT reads "not reproduced". Its three metal-poor bins are resolvable (power 1.00),
  and their data valleys (d = 0.367–0.580) lie far above d* = 0.25. Its power mocks draw observed ages
  with the catalogue's quoted errors and fit them with the same errors (f = 1). If XR22's true age
  errors are larger than quoted, the f = 1 fit under-deconvolves a nearly disjoint latent split and
  partly fills its valley, and the R1-SEL-FIT power sets cannot see this (referee of 2026-11-21,
  section 6, points 1 and 9). R1-ERR asks: if the true errors are f × e_Age, does XR22's idealised
  split, fitted exactly as R1-SEL-FIT fits it, reach the data's d in the metal-poor bins? The split
  is the primary power model of 2.1 and SEL-3, with true d < 0.001 in these bins.

- **Seen before this addendum (disclosure).** Everything in sections 5–7 and `log.md`, in particular:
  - the R1-SEL-FIT results (section 5.2): data d of the metal-poor bins (S15 term E 0.410, 0.579,
    0.502; term N 0.367, 0.580, 0.482; Full 0.386, 0.579, 0.479) and d = 1 in the metal-rich bins;
    d* = 0.25 in every set; power 1.00 in all 18 primary power sets of the metal-poor bins, whose
    fitted d never exceeds 0.073 (95th percentiles at most 0.017, 0.011 and 0.069 by bin, over the
    variants), with K = 3 or 4;
  - the generating models of these bins (old weight 0.415, 0.296, 0.153 on S15 and 0.427, 0.308,
    0.160 on Full; old mean 11.66, 10.90, 10.14 Gyr; old width 0.82 Gyr; young component uniform on
    1.5–7.0 Gyr);
  - the time per mock in these bins (S15 term E null 6.55 s and power 3.07 s; term N power 1.99 s;
    Full power 2.39 s; `r1_selfit.json` `per_set`);
  - the error-scale values and fits: f_max = 2.81 (2.0), recomputed as 2.70 (term E) and 2.65
    (term N) in R-SEL; the sample-A, sample-B and R7 fits at f = 0.8 and f_max (other samples).

  **Not seen:** any R1 mock drawn with f ≠ 1, and any R1 data fit at f ≠ 1. While drafting this
  addendum we made only the rough estimate given under "What the outcome can be", by hand, and the
  binomial error rates of the decision rule (below); nothing else was computed.

- **What changes (mock generator only).** New power sets for the three metal-poor bins
  [−0.7, −0.5), [−0.5, −0.3) and [−0.3, −0.1), drawn with true errors f·e. In `mocks.observe` the
  standard-normal deviate z is multiplied by f and the catalogue error stays as it is: under
  e = r·τ, A = τ + f·r·τ·z and e = r·τ; under e = r·A, A = τ / (1 − f·r·z) and e = r·A (so
  A − τ = f·r·A·z = f·e·z). The rest of the SEL-2 generator is unchanged: r keyed by τ from the bin's
  data pass-bin pools, observed ages kept in (0, 20) by redrawing z, the S15 cut on the catalogue
  e/A, the mock parent and the mock's own term E. At f = 1 the generator is the existing one, draw
  for draw.
  - *Ladder:* f ∈ {1.2, 1.5, 2.0, 2.81}. 2.81 is f_max of 2.0 (`r34.json`, `error_scale.f_max`).
    R-SEL's recomputed values (2.70 and 2.65) lie between 2.0 and 2.81, so the ladder brackets them.
    f_max is a heuristic upper value, not a supported error scale (2.0; section 7). f = 1 is
    R1-SEL-FIT itself and is not rerun.
  - *Generating models:* the primary power models (floor 0.12) of each bin and variant, as recorded
    in `r1_sel.json` (data fits at f = 1), the same at every f. The floor-0.20 power models are not
    used; among the metal-poor bins only [−0.3, −0.1) has one, and its power equalled the primary
    one in R1-SEL-FIT.
  - *No null sets, and d* is not recomputed.* The label compares power mocks with the data's d, not
    with d*, so d* enters no R1-ERR rule. Null mocks drawn from the f = 1 unimodal fits and blurred by
    f would also not be the right null for "true errors f × e_Age" (that null would be fitted at f),
    and they would cost about two thirds of the run. The reference threshold stays R1-SEL-FIT's
    d* = 0.25 (the cap; no null mock of the metal-poor bins had a valley).
  - *Fits:* every mock is fitted with f = 1 exactly as in R1-SEL-FIT (2.6). Fit (o) starts from the
    data fit plus 2 perturbations, and fit (i) from 8 data-independent starts per K. Per K the
    better-fit rule applies (tie 0.01), then BIC and the K = 5 rule. Valley and d are found on the
    0.05 Gyr grid, with the variant's own selection term (S15 term E built from the mock parent;
    term N; Full with denominator 1).
  - *Sets:* for each f, 3 variants × 3 bins × 2 mechanisms = 18 power sets; 72 sets in all, 50 mocks
    each (3,600 mocks), with no reduced fallback.
  - *Numbering and streams:* sets are numbered k = 0…71 in the loop nest f (ladder order) > variant
    (S15E, S15N, Full) > bin > mechanism (rtau, rA). Mock j of set k draws its catalogue and fit (o)
    from `default_rng([seed, 54, k, j])` and fit (i) from `default_rng([seed, 154, k, j])`, consumed
    as in 2.6. No other stream uses tags 54 and 154 (SEL-8 uses 31, R1-SEL-FIT 45, the data fits
    `[seed, 1000 + b, …]`).

- **Decision rules (fixed now).** For variant v, bin b, scale f and mechanism m, n_reach is the
  number of the 50 power mocks that have a valley and whose fitted d ≥ d_data(v, b), the R1-SEL-FIT
  data d of that bin and variant (`r1_selfit.json` `variants.<v>.bins[b].d`). Mocks without a valley
  (d = 1 is a sentinel, not a dip) are not in n_reach; they are counted separately as n_novalley and
  reported. A blurred split that shows no dip at all does not reproduce the data's dip.
  *Amendment (2026-11-21, Codex review, before any R1-ERR mock):* the first draft counted mocks
  without a valley in n_reach, which would inflate it; changed to the definition above.
  - *Per bin:* "explainable at f" if n_reach / 50 ≥ 0.05 (at least 3 of 50) under at least one
    mechanism, otherwise "not explainable at f". Equivalently, at least 3 mocks have a valley and,
    among the mocks with a valley, the 3rd largest d is ≥ the data d.
  - *Why this rule and not the median.* The question is whether the data's d is consistent with an
    idealised split blurred by f, not whether it is typical of one. A one-sided 5% tail is the usual
    consistency criterion, and it mirrors the construction of d* (at most 2 of 50 null mocks pass).
    The valley-aware median rule (n_reach ≥ 25 of 50: at least half of the mocks have a valley with d ≥ data
    d) asks for typicality and would call a bin "not
    explainable" more easily, which favours the recorded label. It is reported (labels computed with
    it by the same structure) but not used. "At least one mechanism" is also the side less favourable
    to the recorded label: R1 needs power under both mechanisms, so a dip that either mechanism
    produces counts as explained.
  - *Precision (computed now from the binomial distribution, 50 mocks per mechanism, the two
    mechanisms treated as independent).* If the true fraction of mocks that have a valley with d ≥ data d is 2%
    under both mechanisms, a bin is called explainable with probability 0.15; if it is 5%, the call
    is missed with probability 0.29; at 10% it is missed with probability 0.01. "Not explainable" and
    "robust up to f = X" are therefore 50-mock estimates, not bounds; every n_reach / 50 is reported
    with its 95% Clopper–Pearson interval (for 0 of 50: 0–0.071; for 3 of 50: 0.013–0.165).
  - *E(f)* is the number of the three metal-poor bins explainable at f in S15 term E (primary). At
    f = 1, E = 0 from the R1-SEL-FIT record (every power mock d ≤ 0.073 against data d ≥ 0.410); it is
    computed from the per-mock d of `r1_selfit.json` and reported as the f = 1 row.
  - *Feasibility:* an f is "not feasible" if the generator fails (a `RuntimeError` of
    `mocks.catalogue_sel` or of the latent sampler) in one of the S15 term E power sets of that f,
    the sets used for the label. The ladder is cut there: no set at that f or a larger one is run
    after the failure, and those f values are reported as not feasible. A generator failure in a
    term N or Full set is reported for that set and does not cut the ladder; that variant's
    reported label at that f is "not evaluable at f".
  - *Label R1-ERR (exactly one of):*
    1. "not evaluable (reproduction)" if a check below fails;
    2. otherwise "not evaluable (non-finite)" if any set used for the label has a non-finite mock
       result (`selaux.nonfinite` on d, valley, k and pass_rate);
    3. otherwise "not evaluable (infeasible)" if f = 1.2 is not feasible;
    4. otherwise "sensitive at f = Y", with Y the smallest feasible ladder f where E(f) ≥ 2;
    5. otherwise "robust up to f = X", with X the largest feasible ladder f such that E(f′) = 0 for
       every feasible f′ ≤ f (X = 1 if E(1.2) = 1). It carries the qualifier "one bin explainable
       from f = Z" (Z the smallest feasible f with E(f) = 1, with the bin or bins named) when there
       is one, and "ladder ends at f = F_end" (F_end the largest feasible f) when the feasibility rule
       cuts the ladder.

    Cases 4 and 5 cover every remaining outcome, since either some feasible f has E(f) ≥ 2 or none
    has.
  - *Why two of three bins.* R1 (2.1) reads "reproduced" only with at least 3 almost-disjoint bins,
    and the metal-rich bins show no valley in the data. The recorded "not reproduced" could therefore
    turn only if all three metal-poor bins were compatible with an almost-disjoint split. "Sensitive"
    is set earlier, at two bins: each bin's call rests on one set of 50 mocks per mechanism, and two
    compatible bins already make the recorded reading insecure. The smallest f with E(f) = 3 ("all
    three bins explainable from f = W3") is reported next to the label.

- **Unchanged.** The data fits (40 starts, the 2.0 streams; they must equal `r1_sel.json`); the power
  models; the pass tables and r pools; R1-SEL-FIT's fit procedure; the valley rule; d* (R1-SEL-FIT's
  0.25); and every recorded label. R1-ERR computes no R1 verdict. The metal-rich bins are not run:
  their data show no valley, and R1-SEL-FIT's verdict does not rest on them (three metal-poor bins
  with power 1.00 already give it). The kernel stays Gaussian. The prior-shaped skewed kernel that
  T-054 lists as optional is not registered, because no specification of the shapes of XR22's age
  posteriors is available here; it stays an open question.

- **Checks (a failure makes R1-ERR "not evaluable (reproduction)", reported and investigated before
  anything else).** (a) The 9 data fits of the metal-poor bins (3 variants) equal `r1_sel.json` by
  the check of 2.6 (absolute 10⁻⁹). (b) Generator at f = 1: mock j = 0 of each of the 18 primary
  power sets of the metal-poor bins, regenerated by the new code at f = 1 on R1-SEL-FIT's streams
  (tags 31 and 45, with R1-SEL-FIT's set numbers), gives the recorded d and valley flag
  (`r1_selfit.json` `variants.<v>.bins[b].mocks.power_<mech>`, absolute 10⁻⁹).

- **Reported (no verdict).**
  - *Per set:* the 5th, 50th, 80th and 95th percentiles of the fitted d; n_reach with its 95%
    Clopper–Pearson interval; n_novalley; descriptively, the number of all mocks with d ≥ data d
    including those without a valley (n_reach + n_novalley); the fraction with a valley; the power at d* = 0.25 (a valley and d < 0.25); the K chosen; how often
    (i) was used; the number of mocks whose NLL rises with K; the mean pass rate of the mocks against
    the data's S15 fraction of the parent; the 5th, 50th and 95th percentiles of the observed ages
    (median over mocks) against the data bin's; the number of stars dropped by the redraw limit of
    `mocks.observe` (200 draws); generator failures; the time per mock.
  - *Per f:* the labels of S15 term N and Full by the same rules, next to the primary (they do not
    qualify it); the median-rule labels; and the 2.1 verdict R1 would read at f with the power at f
    against d* = 0.25.
  - *Companion data refit:* the 9 metal-poor data bins (3 variants) are refitted at each ladder f
    (`run.onedim` with f; 40 starts on the stream `default_rng([seed, 1000 + b, code, 50,
    round(100·f)])`; K = 1–4 by BIC and the K = 5 rule). Reported: d, K, valley, and whether
    d < 0.25. This shows what the data would give if the true errors were f × e_Age and the fit knew
    it. It is not decisive, because no mock calibration is done at that f.

- **What the outcome can be (stated now).** At f = 1, E = 0 (R1-SEL-FIT). The recovered d of the
  power mocks should rise with f, because the f = 1 fit leaves a residual blur of about
  √(f² − 1) × e. With e ≈ 0.8 Gyr at 10–11 Gyr (median relative error 0.075), that is about 0.5,
  0.9, 1.4 and 2.1 Gyr at f = 1.2, 1.5, 2.0 and 2.81. The gaps between the young edge (7.0 Gyr) and
  the old means are 4.7, 3.9 and 3.1 Gyr in the three bins, with an old width of 0.82 Gyr. A rough
  estimate by hand puts the recovered d below 0.37 at f ≤ 1.5 in every bin and leaves f = 2.0 and
  2.81 open, with bin [−0.3, −0.1) (the smallest gap) the first to reach. So "robust up to f = 1.5",
  "robust up to f = 2.0 / 2.81" and "sensitive at f = 2.0 / 2.81" are all foreseeable; "sensitive at
  f = 1.2 or 1.5" would contradict the estimate.
  - *Reading:* "robust up to f = X" means that XR22's idealised split, blurred by Gaussian errors up
    to X times the quoted ones (under either mechanism), does not produce the data's dips (within the
    precision above). "Sensitive at f = Y" means that R1-SEL-FIT's "not reproduced" holds only if the
    true errors are below about Y times the quoted ones. Neither shows that the split exists or that
    it does not.
  - *The generating model is "a 0.82 Gyr split blurred by f".* XR22's 0.82 Gyr width was deconvolved
    with the quoted errors. Under errors f times larger their own deconvolution would give a narrower
    old sequence, and at f ≳ 1.4 (√(f² − 1) × 0.8 Gyr ≳ 0.82 Gyr) the quoted width leaves no room for
    the added error variance, so a 0.82 Gyr intrinsic width is no longer consistent with XR22's own
    numbers. The mocks keep 0.82 Gyr at every f. That is the side less favourable to the recorded
    label: a wider old component fills the valley more easily.
  - *Plausibility of f is outside R1-ERR.* The only independent check cited here (Shariat, El-Badry
    & Bhattacharjee 2025, 11 wide pairs) finds the quoted errors consistent but does not exclude
    modest misestimates, and f_max is a heuristic upper value. At large f the mocks' observed ages
    may be wider than the data's; the reported percentiles show this, but it does not enter the rule.

- **Runtime and machine.** From R1-SEL-FIT's measured times in these bins (the overall mean of
  3.53 s per mock would give 3.5 h):

  | Sets | Sets (4 f values) | Mocks | s per mock (R1-SEL-FIT) | Hours |
  |---|---|---|---|---|
  | S15 term E power | 24 | 1,200 | 3.07 | 1.02 |
  | S15 term N power | 24 | 1,200 | 1.99 | 0.66 |
  | Full power | 24 | 1,200 | 2.39 | 0.80 |
  | Total | 72 | 3,600 | – | 2.48 |

  Larger f widens the mocks and may lengthen draws and fits; allowing up to 1.5 times gives
  2.5–3.7 h of mocks. Add the 9 data fits (about 15 min; 2.6 took about 25 min for 15), the 36
  companion refits (about 1 h) and check (b) (18 mocks, about 1 min): about 4–5 h in all. No data
  download, cache only. The run is started only on an otherwise idle machine (the R-SEL mock stage
  peaked at a 6.26 GB working set). Checkpoints per mock go to the system cache (`s010_err_mocks`),
  keyed by PARAMS and code. The SEL-8 projection rule applies with a stop at 16 h, well above the
  estimate (resuming needs the user's consent, recorded in `log.md`). Its projection groups are the
  (variant, f) pairs, so that slower sets at large f are not projected from faster ones: each group
  projects from its own first-mock times until one of its own sets has finished, then from its
  finished sets. No label is computed until every set that the rules run has its 50 mocks.

- **Reporting.** Results go to a new file `r1_err.json`, with `provenance_err.json` and
  `run_info_err.json`. `r1_sel.json` and `r1_selfit.json` are read, never written, and no recorded
  label changes. Section 5 reports R1-ERR in a new subsection after 5.2. The claim, the root tables,
  `STATUS.md` and the wiki give R1-ERR's label next to R1-SEL-FIT's as its error-scale qualifier
  ("not reproduced under the quoted errors; R1-ERR: robust up to f = X" or "sensitive at f = Y"),
  not as a correction of it.

- **Code (none exists yet).** A new part `"err"` in `PARAMS["parts"]` runs only this test, alone (it
  reads `r1_sel.json` and `r1_selfit.json`): pass tables of the metal-poor bins, their 9 data fits,
  check (b), the 72 sets and the companion refits. New PARAMS: `err_f = [1.2, 1.5, 2.0, 2.81]`,
  `err_bins = [0, 1, 2]`, `err_n_mock = 50`, `err_reach_frac = 0.05`, `err_min_bins = 2`,
  `err_seed_tag = 54`, `err_seed_tag_indep = 154`, `err_stop_h = 16`. `mocks.observe` and
  `mocks.catalogue_sel` get a keyword `f = 1.0` that scales only the deviate, and the R1-SEL-FIT
  mock function passes f through. The checkpoint key leaves out `parts` and `err_stop_h` (added to
  `selaux.NO_KEY_PARAMS`).
  - *Offline unit tests of the generator (no data):* with fixed τ and r, a large draw and no
    truncation in effect (τ and errors far from 0 and 20), (i) under e = r·τ the standard deviation
    of (A − τ)/e is f within its sampling error, and (ii) under e = r·A, at fixed τ, 1 − τ/A
    (which equals f·r·z) passes a Kolmogorov–Smirnov test against N(0, (f·r)²); (iii) at f = 1 `observe` and
    `catalogue_sel` return exactly the arrays of the current code for the same stream.

- **Amendments before any R1-ERR mock (2026-11-21)** (implementation choices, T-054; no rule above changes):
  1. *Generator failure.* A `RuntimeError` raised inside the mock's `mocks.catalogue_sel` call (which
     includes the latent sampler and the keyed r draw) is a generator failure; the mock is checkpointed
     with `gen_fail` and no d. A `RuntimeError` of the fits is not a generator failure and stops the run,
     as in R1-SEL-FIT. After a failure in an S15 term E set, no further mock of that set or of any set at
     that f or a larger one is run (mocks such sets ran before the failure are kept and reported); those
     sets leave the runtime projection. A failure in a term N or Full set does not stop that set.
  2. *Reported labels of S15 term N and Full.* An f at which the variant had a generator failure is left
     out of that variant's rules (as an infeasible f is) and named in the qualifier "not evaluable at
     f = …"; X ends there, as at a cut (X is the largest f below it with E = 0 at every smaller f), while
     Y, Z and W3 are taken over the variant's evaluable f values; the "ladder ends" qualifier follows the
     primary ladder.
  3. *Label text.* f is written as `str(float(f))` (1.0, 1.2, 1.5, 2.0, 2.81); bins as "[-0.3, -0.1)".
     The bins named after "one bin explainable from f = Z:" are all bins explainable at any feasible f
     with E(f) = 1, in bin order. "All three bins explainable from f = W3" is a separate field.
  4. *Reported items.* The d percentiles are over all mocks of a set (a mock without a valley has d = 1),
     as in R1-SEL-FIT's `per_set`, and also over the mocks with a valley. Stars dropped by the redraw
     limit are counted over every draw of the mock's catalogue call, including draws discarded after the
     parent closes. The f = 1 row counts n_reach in each variant from `r1_selfit.json`'s per-mock d with
     the same 3-of-50 rule. The 2.1 verdict "R1 would read at f" takes, for the three R1-ERR bins,
     resolvable = power at 0.25 ≥ 0.80 under both mechanisms and a valid power model, and takes the data
     d, the almost-disjoint flags and the two metal-rich bins (not run) from R1-SEL-FIT. The median rule
     uses the same "at least one mechanism" structure with n_reach ≥ 25.
  5. *Order and records.* Check (b) runs before the checkpoint folder is opened and its 18 mocks are
     not checkpointed; the 36 companion refits run after the 72 sets, are not checkpointed and are not
     in the projection; their stream uses the literal 50 as written above. With `err_n_mock` ≠ 50 (an
     exploration) no label is given, as in 2.6. The committed `PARAMS["parts"]` is `["err"]`.
- **Note after the first formal attempt (2026-11-21; no rule changes, no formal R1-ERR mock had run).** The first
  formal run, single-threaded (`OMP_NUM_THREADS`, `MKL_NUM_THREADS`, `OPENBLAS_NUM_THREADS` = 1), stopped
  at check (a) as "not evaluable (reproduction)": d and K of the 9 data fits matched, but the skew-normal
  and split-normal fits (and two K fits) differed from `r1_sel.json` by more than 10⁻⁹. Investigated as
  this section requires: an exploration with the default thread settings passed check (a) and check (b)
  (18 of 18). It then computed 10 R1-ERR power mocks (set 0 to 9, mock 0), which were not inspected, and
  was stopped; its checkpoints and output were deleted. The runs that wrote `r1_sel.json` and
  `r1_selfit.json` did not record their thread settings; that they used the default (multi-threaded)
  settings is inferred from this reproduction. The cause is inferred to be the thread count (presumably
  small floating-point differences amplified by the optimiser), not the code or the data. The formal run is therefore repeated with the default thread settings; `r1_err.json`
  now records them (`threads`, with the CPU count); every session of the run must use the same settings,
  and multi-threaded results need not be bitwise reproducible on another machine. The exploration also
  showed that an exploration wrote R1-ERR mock checkpoints into the formal folder; they now go to
  `s010_err_mocks_explore/<date>-<tag>`.

### 2.8 R1-ERRCAL (addendum 2026-11-22, T-059), pre-registered before any mock fitted with f ≠ 1

This addendum registers a calibration of R1 under enlarged age errors, with the error scale in the fit. It changes
nothing in 2.0–2.7 and no recorded label: R1, R1-SEL, R1-SEL-FIT and R1-ERR keep their labels. R1-ERRCAL gives, for
each of two error scales, the 2.1 verdict R1 would read if the true errors were f × e_Age **and the fit knew it**. It
is reported next to R1-SEL-FIT and R1-ERR as a further qualifier, not as a verdict on XR22's claim.

- **Why.** R1-ERR (2.7, section 5.3) fitted every mock with f = 1. Its companion data refits, fitted with f, give
  much smaller valley depths at f = 2.0 and 2.81 (S15 term E 0.078, 0.465, 0.227 and 0.057, 0.271, 0.160; term N and
  Full below 0.25 in all three metal-poor bins at 2.81), but no mock calibration was done at those f, so they decide
  nothing. Its referee (section 6, R1-ERR point 8) named this as the most important additional test: draw the null
  and power mocks with f·e, fit them with f, and read the 2.1 verdict at each f. The referee also asked for a power
  model built from the data's fit at f and matched to the observed ages, and for a comparison of valley positions.
  **The data-matched power model is omitted:** 2.1 defines power against XR22's idealised split, and R1-ERRCAL keeps
  R1-SEL-FIT's primary power model so that "resolvable" means the same as in R1-SEL-FIT. Its direction is stated: the
  idealised split has a wide gap (young edge 7.0 Gyr, old means 10.1–11.7 Gyr), while a split shaped like the data's
  fits at f (valleys at 9.6–11 Gyr, more stars at 7–10 Gyr; R1-ERR referee point 1) would be harder to resolve, so
  keeping the idealised split makes "resolvable" easier and moves outcomes towards "not reproduced" rather than
  "undetermined". Valley positions are reported (below).

- **Seen before this addendum (disclosure).** Everything in sections 5–7 and `log.md`, in particular all R1-ERR
  results: the per-set d of every mock (fitted with f = 1), the labels, the 36 companion data refits at f = 1.2, 1.5,
  2.0, 2.81 (d, K, valley age) and the observed-age percentiles. **Not seen:** any mock fitted with f ≠ 1, any null fit
  (skew-normal or split-normal) with f ≠ 1, and any d* at f ≠ 1.

- **Scales and bins.** f ∈ {2.0, 2.81} (the two R1-ERR values at which the companion refits turned; f_max = 2.81 is a
  heuristic upper value, see 2.0), in this order. The three metal-poor bins [−0.7, −0.5), [−0.5, −0.3), [−0.3, −0.1) in the three
  variants (S15 term E, primary; term N; Full), in the order S15E, S15N, Full as in R1-ERR. The metal-rich bins are
  not run (their data show no valley at f = 1; that a fit with f could create one is not tested here).

- **Data fits at f.** For each variant, bin and f: the K = 1–4 mixtures by `run.onedim` with f (40 starts on the
  stream `default_rng([seed, 1000 + b, code, 50, round(100·f)])`, R1-ERR's companion refits; K by BIC and the K = 5
  rule; `run.r1_data_refit`), which must reproduce R1-ERR's `companion_refits` d and K within 10⁻⁹ (check a); then
  the two unimodal null families (skew-normal, split-normal) fitted with f exactly as the 2.1 data fit does with f = 1
  (8 starts each: 3 deterministic + 5 seeded perturbations of the first, bounds as recorded, the variant's selection
  term), their perturbations drawn from the same stream after the mixture fits. Valley, d, valley age and the
  young-side edge (97.5th percentile of the latent mass younger than the valley) from the K fit as in 2.1.
  `run.r1_data_refit` is extended, not replaced: the mixture fits and K are computed first, exactly as now, so check
  (a) holds, and the null fits follow on the same stream.

- **Mocks.** For each (f, variant, bin): four null sets (skew-normal and split-normal at f × the two error mechanisms)
  and two power sets (the primary power model of R1-SEL-FIT, floor 0.12, as recorded in `r1_sel.json`, × the two
  mechanisms); 50 mocks each; 2 × 3 × 3 × 6 = 108 sets, 5,400 mocks. Catalogues by R1-ERR's generator with true errors
  f·e (2.7: only the deviate is scaled; the catalogue error and the S15 cut on e/A as recorded). Every mock is fitted
  **with f** (the kernels of `m0` at f), by R1-SEL-FIT's procedure (2.6: fit (o) from the data fit at f plus 2
  perturbations, fit (i) from 8 data-independent starts per K, the better-fit rule with tie 0.01, BIC, the K = 5 rule
  and the 2.1 mode-matching rule). Sets are numbered k = 0…107 in the loop nest f > variant > bin > set (null
  skew-normal e = r·τ, e = r·A, split-normal e = r·τ, e = r·A, power e = r·τ, e = r·A); mock j of set k draws its
  catalogue and fit (o) from `default_rng([seed, 59, k, j])` and fit (i) from `default_rng([seed, 159, k, j])`. Tags 59
  and 159 are used by no other stream.

- **Decision rules (fixed now), per f and variant.** d*(f) = min(0.25, q₁, …, q₄) per bin as in 2.1 (q_s the 3rd
  smallest null d of set s, ties counted; 0.25 if fewer than 3 mocks of the set have a valley); a bin is resolvable if
  its power (a valley and d < d*(f)) is ≥ 0.80 under both mechanisms; almost disjoint if the data fit at f has a
  valley with d < d*(f). Verdict at f: the 2.1 rule on all five bins, with the three metal-poor bins from R1-ERRCAL
  at f and the two metal-rich bins taken from R1-SEL-FIT (resolvable or not, and not almost disjoint, as their data
  show no valley), as R1-ERR's amendment 4 does for "the 2.1 verdict R1 would read at f"; the metal-rich bins are not
  calibrated at f, which is stated with the verdict. So **"reproduced at f"** if at least three bins are resolvable, at
  least three of them almost disjoint (only the metal-poor bins can be) and the median young-side edge of the almost-
  disjoint bins lies in 6.5–9.5 Gyr; **"undetermined at f"** if fewer than three bins are resolvable; **"not
  reproduced at f"** otherwise.
  - *Label R1-ERRCAL* (S15 term E, primary): "at f = 2.0: <verdict>; at f = 2.81: <verdict>". The whole label is
    replaced by "not evaluable (reproduction)" if check (a) fails. Per f and variant, the verdict is replaced by "not
    evaluable (non-finite)" if any mock of that variant's sets at that f has a non-finite result (`selaux.nonfinite`), and by "not evaluable
    (generator)" if the generator fails (a `RuntimeError` of `mocks.catalogue_sel` or of the latent sampler) in one of
    its sets at that f; the failing mock is checkpointed with `gen_fail`, no further mock of that f and variant is run, and
    the other f is unaffected. Term N and Full give the same label, reported next to it.
  - *Reading (fixed now).* "Reproduced at f" means: if the true errors were f times the quoted ones, the data's dips,
    deconvolved with those errors, are as deep as an almost-disjoint split, and the test could see such a split.
    "Not reproduced at f" keeps R1-SEL-FIT's reading at that scale. Neither says that f is plausible; R1-ERR's
    plausibility notes (2.7) and the f_max caveat apply.

- **Reported (no verdict).** Per set: the d percentiles (5, 50, 80, 95), the fraction with a valley, q_s, power at d*,
  the K chosen, how often (i) was used, the number whose NLL rises with K, the time per mock; the median valley age of
  the mocks with a valley against the data fit's valley age at f (the valley position the referee asked for); the
  null fits' parameters at f.

- **What the outcome can be (stated now).** At f = 2.0, S15 term E's bin [−0.5, −0.3) has data d = 0.465 at f, above
  any d* ≤ 0.25, so "reproduced at 2.0" is impossible in term E; "not reproduced at 2.0" if at least two of the three
  metal-poor bins stay resolvable ([−0.1, 0.1), resolvable in R1-SEL-FIT, counts as the third). At f = 2.81, term E's bin [−0.5, −0.3) has d = 0.271, also above 0.25: "reproduced at 2.81" is impossible
  in term E too, so **the primary label can only read "not reproduced" or "undetermined" at each f**. Term N and Full
  cannot read "reproduced at 2.0" either (their bin [−0.5, −0.3) has d = 0.430 and 0.421 at 2.0); at 2.81 (all three
  bins below 0.25: 0.063, 0.242, 0.145 and 0.054, 0.232, 0.142) they can read "reproduced at 2.81" only if each bin's
  d* (per bin, as in 2.1) exceeds that bin's data d: in bin [−0.5, −0.3) every q_s above 0.242 / 0.232, and in the
  other two bins every q_s above their data d, i.e. d* stays near its cap, the power holds and the edges fall in
  6.5–9.5 Gyr. Term E's bin [−0.7, −0.5) has its data valley at 10.975 Gyr at 2.81, at the edge of 2.1's 5–11 Gyr
  window. The open parts: deconvolving mocks with large f may create valleys in unimodal null mocks
  (lowering d*), and larger f may reduce power. Our guess: term E "not reproduced at 2.0; not reproduced at 2.81",
  term N and Full split between "reproduced" and "not reproduced" at 2.81 (if one metal-poor bin loses power or its
  d* falls below the data's d, the alternative is "not reproduced"; "undetermined" needs two bins to lose power).

- **Unchanged.** The power models (R1-SEL-FIT's primary, true d ≤ 0.02), the generator (R1-ERR's at f), the fit
  procedure (R1-SEL-FIT's, with f), the valley rule, the 2.1 verdict rule, and every recorded label. No R1 verdict at
  f = 1 is recomputed.

- **Runtime and machine.** R1-ERR's mocks took 4.01 s on average (5.76 s term E, 3.1 s term N and Full) with f = 1
  fits; R1-SEL-FIT's null mocks were slower (term E 6.55 s). Fits with f use the same kernels at a different width.
  Estimate: 5,400 mocks ≈ 6–8 h, plus the data and null fits (about 30 min), on an otherwise idle machine, with the
  default thread settings recorded as in R1-ERR (`threads`). Checkpoints per mock in the system cache
  (`s010_errcal_mocks`, explorations under `s010_errcal_mocks_explore/<date>-<tag>`), keyed by PARAMS and code; the
  SEL-8 projection rule with groups per (f, variant) and a stop at 16 h (resuming needs the user's consent). No label is
  computed until every set has its 50 mocks. Cache only, no download.

- **Reporting.** `r1_errcal.json`, `provenance_errcal.json`, `run_info_errcal.json`; `r1_sel.json`, `r1_selfit.json`
  and `r1_err.json` are read, never written. Section 5 reports R1-ERRCAL in a new subsection after 5.3; the claim, the
  root tables, `STATUS.md` and the wiki give it next to R1-SEL-FIT's and R1-ERR's labels.

- **Code (none exists yet).** A new part `"errcal"` in `PARAMS["parts"]` runs only this calibration, alone; PARAMS
  `errcal_f = [2.0, 2.81]`, `errcal_bins = [0, 1, 2]`, `errcal_n_mock = 50`, `errcal_seed_tag = 59`,
  `errcal_seed_tag_indep = 159`, `errcal_stop_h = 16`; the checkpoint key leaves out `parts` and `errcal_stop_h`.
  Offline tests: a mock fitted with f equals the model's likelihood at f; f = 1 reproduces R1-SEL-FIT's fit path; the
  set numbering and streams; the verdict rule on synthetic set results.

- **Amendments before any R1-ERRCAL mock (2026-11-22)** (implementation choices, T-059; no rule above changes):
  1. *Power models and data.* The primary power models (floor 0.12) are read from `r1_sel.json`
     (`data_fits.<variant>_<bin>.power_models.primary`); the f = 1 data fits are not rerun (R1-ERR refitted
     and checked them; JSON keeps the floats exactly). Each data fit at f must have the star count recorded
     in `r1_sel.json` for that bin and variant; a difference stops the run as a code error (no label).
  2. *Check (a).* For each f, variant and bin, d (absolute 10⁻⁹) and K of the data fit at f are compared
     with `r1_err.json` `companion_refits.<variant>.<f>` (matched by bin); a missing record counts as a
     mismatch. The mismatches are listed in `checks.data_fit_mismatches`; with any mismatch no mock is run
     and the labels of all three variants read "not evaluable (reproduction)".
  3. *Null fits at f.* The null-fit code of the 2.1 data fit is moved, unchanged, into one function
     (`run.r1_null_fits`) used by both the f = 1 fit (`r1_data_sel`) and the fit at f; at f it runs on the
     model built with f, after the K = 1–4 fits and (if K = 4 is chosen) the K = 5 fit, on the same stream.
  4. *Starts of fit (o).* The data fit at f's mixture per K (and its K = 5 fit when it chose K = 4). When the
     data fit at f did not fit K = 5, a mock's (o) K = 5 fit uses 3 starts from the mock's own data, exactly
     as R1-SEL-FIT does when its data fit had no K = 5 fit.
  5. *What "fitted with f" scales.* The model's kernel width and the selection term are computed with f·e
     (`m0.kernels` with f, as in R1-ERR's companion refits): for S15 term E the pass table is built from the
     mock parent's catalogue e/A, as in 2.6, and its terms are integrated with width f·e. The S15 cut, the
     cell compression and the catalogue error stay the quoted e (as in the generator, 2.7).
  6. *Order of the failure rules.* Per f and variant, "not evaluable (generator)" is checked first, then
     "not evaluable (non-finite)" (`selaux.nonfinite` on d, valley, k and pass_rate, the fields the rules use,
     as in 2.6 and 2.7). Mocks of a failing f and variant that ran before the failure are kept and reported.
     A set that is incomplete without a generator failure stops the evaluation with an error.
  7. *Resolvable* also needs a valid power model, as in R1-SEL-FIT (`r1_sel_bins`); every primary power model
     of the three bins is valid in `r1_sel.json`. The metal-rich bins enter the verdict with R1-SEL-FIT's
     `resolvable` (primary floor), `almost_disjoint` false and their recorded edge.
  8. *Label text.* f is written as `str(float(f))` (2.0, 2.81) and the verdict as "reproduced",
     "not reproduced" or "undetermined": "at f = 2.0: not reproduced; at f = 2.81: undetermined". With
     `errcal_n_mock` ≠ 50 (an exploration) no label is given, as in 2.6 and 2.7 (`computed_labels_not_used`).
  9. *Reported items.* Per set: the per-mock d and valley flags, d percentiles over all mocks and over mocks
     with a valley, the fraction with a valley, q_s and the pass fraction at d* (null sets), the power at d*
     (power sets), K chosen, use of (i), NLL rising with K, the mean pass rate, stars dropped by the redraw
     limit, and the mean time per mock. Valley ages: the mock fit result now also carries the valley age
     (`valley_t`, an added field that changes no number of R1-SEL-FIT or R1-ERR); per set only the median over
     mocks with a valley is stored (`median_valley_t_mocks`), next to the data fit's at f (`data_valley_t`).
     The data fits at f (d, K, valley, edge, peaks, BIC, fits per K, null parameters and convergence) are in
     `data_fits.<f>.<variant>[bin]`.
  10. *Order and records.* The 18 data fits run before any mock, are not checkpointed and are repeated on a
      resume (about 30 min). The run uses the default thread settings, recorded in `threads` as in R1-ERR.

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

## 5. Results (2026-11-16)

Run of 2026-11-16 (`python -m astrolab run 010`, 3.53 h; catalogue from the cache). Page:
[`web/index.html`](web/index.html) (`python -m astrolab serve`); numbers in `results/*.json`.
**Mock budget:** the projection at 50 mocks per set was 4.29 h > 4 h, so by the pre-registered rule
every mock set used 30 (R1 q_s = 2nd smallest null d). The projection was inflated by another
study's run on the same machine at the time (our scheduling); the reduced mode is the
pre-registered fallback and was applied as written.

| Criterion | Ours | Rule | Verdict |
|---|---|---|---|
| R1 8 Gyr split, S15 | resolvable bins 2 of 5; almost disjoint 0 | ≥ 3 resolvable, ≥ 3 almost disjoint, median edge 6.5–9.5 Gyr | **undetermined** |
| R1 8 Gyr split, Full | resolvable bins 2 of 5; almost disjoint 0 | same | **undetermined** (robust: same as S15) |
| R2 13 Gyr mean (observed ages, ED Fig. 1 selection) | μ = 12.93 ± 0.06 Gyr, σ = 2.40 ± 0.04 Gyr, n = 1891 | μ in 12.5–13.5 Gyr | **reproduced** |
| R3 sequence span | 6.00 Gyr over 1.5 dex (sample A) | 4.5–6.5 Gyr, if recovery passes | **cannot determine** (recovery failed) |
| R4 sequence scatter | σ = 2.67 Gyr (sample A) | \|σ − 0.82\| ≤ 0.1, if recovery passes | **cannot determine** (recovery failed) |
| Intrinsic scatter (sample B) | σ_int = 0.79 ± 0.02 Gyr | needs \|mock bias\| ≤ 0.1 | **cannot determine** (mock bias +0.13 to +0.18) |

- **R1.** S15 bins [−0.7, −0.5) and [−0.5, −0.3) are resolvable (power 1.00/1.00 and 1.00/0.97 under
  the two error mechanisms) but their valleys are shallow (d = 0.29 and 0.45 against d* = 0.25);
  [−0.3, −0.1) has d = 0.49 but power 0; the two metal-rich bins show no valley (d = 1) and power 0.
  Full: [−0.5, −0.3) and [−0.3, −0.1) resolvable (d = 0.58, 0.48), [−0.7, −0.5) power 0.67. No null
  mock of any set had a valley below 0.25 (all realised false-positive rates 0), so d* stayed at its
  cap 0.25. Young-side edges where a valley exists: 8.6–9.4 Gyr (S15), 7.3–9.5 Gyr (Full). In words:
  where the data can resolve a split, the latent age density dips between the old and young phases
  but not to "almost disjoint"; for the metal-rich bins the error model cannot resolve one at all.
- **R2.** The observed-age Gaussian for old, metal-poor (−1.05 to −0.95), high-J_φ disc stars gives
  12.93 Gyr, inside the tolerance; XR22's width 1.81 Gyr against our 2.40 Gyr (no verdict).
  Sensitivity: no early-phase filter 12.67, Full 12.76, J_φ > 300 / 700: 12.92 / 12.90, error cuts 10% /
  20%: 12.81 / 12.87; the deconvolved latent mean is lower: 12.19 (S15) and 12.59 (Full). 33% of the
  observed ages exceed 13.8 Gyr and 0.7% exceed 18 Gyr. Age-scale envelope (literature, not
  recomputed): ±0.7–1.1 Gyr in quadrature, and a whole-pipeline re-analysis 1.7 Gyr younger, against a
  0.87 Gyr margin to the Big Bang. So the 13 Gyr number is reproduced on the catalogue's own age scale,
  and is sensitive at the ~1 Gyr level to the scale and to deconvolution.
- **R3/R4.** The sample-A fit (τ̄0 = 8.07 Gyr, a = −4.00 Gyr/dex, σ = 2.67 Gyr; span 6.00 Gyr) would put
  R3 inside its band and R4 far outside, but neither verdict applies: in mocks drawn from that model,
  M0 recovers σ with a bias of +0.28 Gyr (e = r·τ) and +0.25 Gyr (e = r·A), beyond the 0.1 Gyr
  tolerance, so the pre-registered rule gives "cannot determine" for both. The cause was diagnosed
  before the run (log 2026-11-15): with the S15 cut, M0's selection term treats the error as fixed
  while under e = r·τ the cut does not depend on τ (section 7). XR22 Fig. 2e's own selection gives
  span 6.83 Gyr and σ = 2.71 Gyr.
- **Intrinsic scatter.** Sample B's two-component fit gives σ_int = 0.79 ± 0.02 Gyr (close to XR22's
  0.82), but its mock biases (+0.13 to +0.18 Gyr in all four sets) exceed 0.1, so "cannot determine".
- **R5 (descriptive).** Of late-phase stars 23.6% have observed ages above 8 Gyr, and 19.4% of
  early-phase stars are younger than 8 Gyr (XR22 Fig. 2 split by eq. 1).
- **R6 (descriptive).** Early stars with −1.0 < [Fe/H] < −0.4: 5th/10th percentiles of observed age
  7.38 ± 0.39 / 9.54 ± 0.16 Gyr for J_φ < 500 (n = 1956) and 6.09 ± 0.04 / 7.68 ± 0.04 Gyr for J_φ > 500
  (n = 41828); peak of the observed age distribution for J_φ > 500 at 11.1 Gyr.
- **R7 (descriptive, across tracers).** The latent age distributions of old high-α samples are broad:
  at f = 1 the central 95% width is 12.6–13.0 Gyr and the largest fraction in any 1.5 Gyr window is
  0.24–0.38; only at f_max = 2.81 and for [α/Fe] > 0.18 with [Fe/H] < −0.2 does it reach 0.80 (width
  9.7 Gyr). This is far from Miglio et al.'s 95% within 1.52 Gyr, but the two use different tracers,
  scales and deconvolutions; with the recovery bias above, our latent widths are upper-biased.
- **Reading after the referee (post hoc, 2026-11-16; the verdicts above stand as pre-registered).**
  (1) M0's S15 selection term is misspecified under *both* mocked error mechanisms, not only e = r·τ:
  with r independent of τ the cut e/A < 0.15 does not depend on τ under either mechanism (under
  e = r·A it is a cut on r alone), so the term pushes latent ages younger and wider; the referee's
  synthetic check reproduces the +0.3 Gyr σ bias with the term and recovers σ within 0.03 Gyr
  without it. This, not the data, is what makes R3/R4 and the intrinsic scatter undeterminable, and
  it is why S15 and Full differ (deconvolved R2 12.19 vs 12.59; τ̄0 8.07 vs 8.70). The README 2.0
  statement that compression "encodes errors that scale with the observed age" is therefore wrong
  (correction noted here; the frozen text is left as it was). (2) The R1 power model floors the old
  weight at 10%, which can never pass the 10% side-mass rule, so bin [−0.1, 0.1) was unresolvable by
  construction (generating model with young edge 2.0 Gyr, true d = 1). (3) Substantively: no
  resolvable R1 bin is almost disjoint (d = 0.29–0.58 against 0.25), so with one more resolvable bin
  R1 would read "not reproduced" rather than "undetermined"; R3's span is 5.7–6.2 Gyr in every
  sample-A variant (inside 4.5–6.5; XR22 Fig. 2e's own selection gives 6.83); R4's σ_sel is 2.4–2.7 Gyr in every variant, about three times XR22's 0.82,
  so the comparison is probably not like for like (XR22's fit likely includes an outlier or
  background component, as our sample-B mixture does). A re-test with a selection term consistent
  with the mock mechanisms and a corrected power floor needs a new pre-registration (T-031).

### 5.1 Re-test with a consistent selection term (R-SEL, T-031; run 2026-11-19/20)

Pre-registered in section 2.5 (2026-11-17). Run with `"parts": ["sel"]` (`python -m astrolab run 010`)
from 2026-11-19 00:03 to 2026-11-20 04:13 on an otherwise idle machine. The run was interrupted
four times: Claude Code reaped it once under system memory pressure, a stale lock file stopped one
resume, and Windows briefly refused a file replace twice. It also stopped itself once under the 16 h
projection rule, whose projection counted checkpointed mocks not yet replayed as remaining work. Each
resume continued from the per-mock checkpoints with the user's explicit consent (`log.md`); the last
ran under a 20 h limit, through an uncommitted wrapper that only retries the refused file replace.
Both causes were fixed in the code afterwards (T-046, 2026-11-20; section 8).
Per-mock seeds make the numbers independent of the interruptions.

The run took 10.05 h of elapsed time over five sessions. This is the time the SEL-8 limit counts,
and each session refits the data and replays the checkpoints. The 6,200 mocks (124 sets of 50, with
no reduced fallback) took 5.97 h of compute (the sum of the per-mock fit times as checkpointed), against the
estimate of 7.2–11.2 h. The final session's data fits took about 0.73 h, against SEL-8's 1–1.5 h.
Peak working set: 6.26 GB in the mock stage and 3.47 GB in the data fits, well above SEL-8's estimate of about 1–1.5 GB. The estimate was wrong; the cause was not
investigated (the memory reap of 2026-11-19 happened under this load).

New files: `r1_sel.json`, `r34_sel.json` and `sel.json`. `r1.json`, `r34.json` and `summary.json`
are unchanged. The original run's `run_info.json` and `provenance.json` were copied to `orig_*.json`
before being overwritten. The Full sample-A fits reproduce the recorded ones exactly (τ̄0 = 8.70,
a = −4.01, σ = 2.58, span 6.01), and so do Full's R1 data d values (0.386, 0.579, 0.479, 1, 1), as
SEL-9 expects. The table below gives the -SEL labels next to the recorded ones; the recorded
verdicts above stand (SEL-9).

| Label | Term E (primary) | Term N (sensitivity) | -SEL label | Recorded (section 5) |
|---|---|---|---|---|
| R1-SEL | 2 of 5 bins resolvable, 0 almost disjoint (Full: same) | 3 of 5 resolvable, 0 almost disjoint → not reproduced | **undetermined** (robust; selection-term sensitive) | undetermined |
| R3-SEL | span 6.09 Gyr (a = −4.06 ± 0.04 Gyr/dex); robustness fits 5.93–6.25; recovery passes | recovery fails → cannot determine | **reproduced, robust**; selection-term sensitive | cannot determine |
| R4-SEL | σ_sel = 2.55 ± 0.01 Gyr against 0.82 ± 0.1 | cannot determine | **not reproduced**; selection-term sensitive | cannot determine |
| intrinsic-SEL | σ_int = 0.748 Gyr, SE 0.0098 → 0.764 < 0.82; f = 0.8 refit 0.814 → cannot determine | 0.717, SE 0.0085; confirmed at f = 1, 0.8, f_max | **confirmed, not robust**; selection-term robust | cannot determine |

- **R1-SEL.**
  - **Data and calibration.** With term E, S15's data d values are 0.410, 0.579 and 0.502, plus d = 1
    (no valley) in the two metal-rich bins. The old term gave 0.295, 0.454 and 0.492. Term N gives
    0.367, 0.580 and 0.482. In every set no null mock had a valley below 0.25, so d* stayed at its
    cap 0.25.
  - **Bins [−0.5, −0.3) and [−0.3, −0.1).** Resolvable in all three variants (power 1.00).
  - **Bin [−0.7, −0.5) decides the label.** Its power is 0.80 / 0.58 under e = r·τ / e = r·A with
    term E (Monte Carlo ±0.06–0.07), 0.70 / 0.74 on Full, and 0.88 / 0.88 with term N. Only term N
    reaches 80% under both mechanisms, and its third resolvable bin turns term N's verdict into
    "not reproduced". No bin in any variant is almost disjoint (d = 0.37–0.58 against 0.25), so the
    line between "undetermined" and "not reproduced" is this one bin's power.
  - **Metal-rich bins and power models.** The metal-rich bins have no valley in the data and power 0.
    Every power model is valid: true d ≤ 0.04, with young edge 7.0 Gyr (6.5 Gyr for [0.1, 0.3)), as
    checked before the run.
  - **Floor 0.20 sensitivity.** Same verdict in all three variants. The power models of [−0.3, −0.1) and [0.1, 0.3) change but
    their power does not; only [−0.1, 0.1)'s power changes, to
    0.04 / 0.06 (term E), 0.60–0.68 (term N) and 0.36–0.52 (Full), and its data d is 1 anyway.
- **R3-SEL / R4-SEL.**
  - **Recovery and primacy.** Term E's recovery passes under both mechanisms (σ bias −0.051 / −0.066
    Gyr, a bias +0.090 / +0.072 Gyr/dex, none near tolerance), so S15 term E is primary. Term N's
    recovery fails under both (σ bias −0.142 / −0.168), so term N gives "cannot determine" for R3 and
    R4. That is why both labels are "selection-term sensitive": the qualifier reflects term N's
    failed recovery, not a contrary term-N verdict.
  - **Sample A fit and robustness.** Sample A with term E: τ̄0 = 8.72 ± 0.02 Gyr, a = −4.06 ± 0.04
    Gyr/dex, σ_sel = 2.55 ± 0.01 Gyr (bootstrap s.d. 0.009), span 6.09 Gyr; the old term gave 8.07,
    −4.00, 2.67 and 6.00. The R3 robustness fits span 6.01 (Full), 6.25 (a² e_[Fe/H]² added), 6.13
    (f = 0.8) and 5.93 (f_max = 2.70, recomputed from term E's σ_sel), all inside 4.5–6.5. R4's set
    gives σ_sel = 2.58 (Full) and 2.50.
  - **Extra term-E fits (no verdict).** Spans 5.69 ([Fe/H] < −0.2), 6.26 (< 0), 5.81 (edge-drop) and
    6.08–6.09 (untruncated, 0.02 Gyr grid, 40 classes, no compression), with σ_sel 2.47–2.57.
  - **Fig. 2e with term E (no verdict).** τ̄0 = 8.14, a = −4.69, σ = 2.57, span 7.03 Gyr (XR22: 9.38,
    −3.8, 0.82, "5–6 Gyr").
- **Intrinsic-SEL.**
  - **Term E fit.** Sample B gives σ_int = 0.748 ± 0.009 Gyr (f_bg = 0.44). The four mock biases are
    −0.003 and −0.016 (identifiability) and +0.067 and +0.049 (misspecification), all within 0.1. With
    SE = 0.0098 (the s.d. over the identifiability mocks), 0.748 + 1.645 SE = 0.764 < 0.82, so the
    label is confirmed.
  - **Error-scale refits.** At f = 0.8 the refit gives 0.814, and 0.814 ± 1.645 SE straddles 0.82, so
    "cannot determine". At f_max = 2.70 it gives 0.170, confirmed. The label is therefore "not
    robust".
  - **Term N.** It gives 0.717 at f = 1, 0.780 at f = 0.8 and 0.159 at f_max: confirmed, robust. The
    bare labels agree, so intrinsic-SEL is selection-term robust.
- **Reported without verdict (SEL-6, SEL-7).**
  - **Pass tables.** The pass fraction π depends on observed age, not monotonically: 0.54–1.00 across slices and
    bins. In the metal-poor slice it rises from about 0.6 in the youngest bin to about 1.0 in the oldest. The data's S15 fraction of each parent is 0.83–0.95.
  - **Mock pass rates.** The mocks' mean pass rate is within −0.053 to +0.025 of the data's, and the
    R1 S15 mocks pass up to 5 points less often than the data.
  - **R2 deconvolved latent Gaussian.** μ = 12.61 Gyr with term E and 12.73 with term N (σ = 2.24 /
    2.21), against 12.19 with the old term on S15 and 12.59 on Full.
  - **SEL-2 diagnostic (original generator, r independent of τ).** σ bias +0.025 / +0.022 with term E
    and −0.014 / −0.024 with term N, and |a bias| ≤ 0.071. With age-independent errors both new
    terms recover σ. Term N fails only when the mocks carry the data's age dependence of r.
  - **SEL-7 variants.** 0.5 Gyr pass bins: σ_sel 2.55, span 6.09, σ_int 0.752. One slice: 2.53, 6.39,
    0.741.
- **Reading after the referee (post hoc, 2026-11-20; the -SEL labels above stand as pre-registered).**
  1. **R1-SEL's undetermined / not-reproduced line.** It is the power of bin [−0.7, −0.5), and that
     power is limited by mock fits that find no valley.
     - Power mocks of this bin that find a valley always find a deep one (median d 0.008–0.027). The
       misses are mocks without a valley: 10 and 21 of 50 for term E, 6 and 6 for term N, 15 and 13
       for Full.
     - BIC chose K = 1 in 2 and 4 of the term-E mocks (term N 0 and 3, Full 4 and 1). Each mock has
       40,000–46,000 stars drawn from a two-component model, so a converged K = 2 fit would not be
       expected to lose to K = 1 on BIC. Our inference is that the K ≥ 2 fits failed (a local optimum
       or a non-finite likelihood); the checkpoints store only the chosen K.
     - Mock fits start only from the data fit and 2 perturbations (rule of 2.0; point 5 of the
       original referee).
     - The label therefore measures the mock optimiser as much as the data. If this bin were
       resolvable, all three variants would read "not reproduced": no bin is almost disjoint (data
       d = 0.37–0.58, while power mocks in the two resolvable bins give d ≈ 0.03–0.06).
     - A diagnostic rerun of this bin with data-independent starts is registered (T-045; done, below:
       the misses are local optima of the mock fits).
     - The metal-rich bins have power 0 because K ≤ 4 Gaussians smear the generating model's uniform
       young edge: their power mocks give d ≈ 0.29–0.48 against a true 0.016–0.04. That is a limit
       of the density model, not of the data.
  2. **Term N's failed recovery and the R3/R4 qualifier.** The evidence points to the SEL-2
     generator as the cause of term N's failure (an inference: the original generator also differs by
     drawing r jointly with [Fe/H]).
     - The τ-keyed r pools are binned in observed age, so their pass fractions already contain the age
       dependence created by the errors themselves (SEL-10).
     - The recovery mocks pass 1.2–1.9 points less often than the data (term E 0.843 / 0.849, term N
       0.844 / 0.850, against 0.862),
       while the original generator matches the data (0.856 / 0.862) and term N recovers under it
       (σ bias −0.014 / −0.024).
     - So "selection-term sensitive" on R3/R4 records which generator is adopted, not a contrary
       result. Term N's span (6.19) lies in the R3 band, and its σ_sel (2.49) fails R4.
  3. **Term E's assumption.** SEL-1 calls the violation of term E's assumption under e = r·τ "second
     order". At fixed A, e/A depends on τ through z, so the violation is first order (corrected here;
     the frozen text is left as it was). Term E recovers within tolerance under both mechanisms
     anyway.
  4. **Intrinsic-SEL's margin.** The margin to 0.82 (0.072 Gyr) is comparable to:
     - the f = 0.8 shift (+0.065),
     - the misspecification mock biases (+0.049 / +0.067), and
     - the term E–N difference (−0.03).

     f_max drives σ_int to 0.17, so only the f = 0.8 refit can break the label. By linear
     interpolation, "confirmed" holds for f ≳ 0.83, a bound nothing here fixes. All mocks keep a
     Gaussian old component.

- **Diagnostic refit of the deciding bin (T-045; exploration, post hoc, 2026-11-20; the -SEL labels
  above stand).** Script `explore/t045_r1sel_power_refit.py` (about 20 min, cache only). It rebuilt bin
  [−0.7, −0.5)'s data fits (identical to `r1_sel.json`: d, K and all mixture parameters, difference 0)
  and regenerated its six power sets with the SEL-8 streams; the original mock fits reproduce every
  recorded d and valley flag (300 of 300) and every checkpointed K. It then refitted each catalogue with
  data-independent starts (the 2.0 quantile starts, 8 per K, K = 1–5, own stream) and kept, for each K,
  the better of the two fits.

  | Variant, mechanism | Power, recorded | Mocks without a valley | NLL rises with K (original fits) | Power, better fits | d of better fits, 95th percentile |
  |---|---|---|---|---|---|
  | S15 term E, e = r·τ | 0.80 | 10 | 29 of 50 | 1.00 | 0.017 |
  | S15 term E, e = r·A | 0.58 | 21 | 27 | 1.00 | 0.015 |
  | S15 term N, e = r·τ | 0.88 | 6 | 38 | 1.00 | 0.009 |
  | S15 term N, e = r·A | 0.88 | 6 | 37 | 1.00 | 0.009 |
  | Full, e = r·τ | 0.70 | 15 | 37 | 1.00 | 0.009 |
  | Full, e = r·A | 0.74 | 13 | 35 | 1.00 | 0.009 |

  - **The misses are local optima of the mock fits.** In 27–38 of 50 mocks per set the original fits'
    NLL rises from some K to K + 1, which the global optima of nested models cannot do, so the original fits missed those optima; with the independent starts
    it never does (0 of 300), and the better fits never do either. Every missed mock has a K ≥ 2 fit
    whose NLL the independent starts lower by at least 1,500. L-BFGS-B reported success for every fit,
    so the convergence flag does not detect these optima.
  - **With the better fits** BIC chooses K = 3 in 43–47 of 50 mocks and K = 4 in the rest (never K = 1
    or 2), every mock has a valley, and no mock that passed under the original fits fails. Power is
    1.00 in all six sets. It stays at or above 0.80 unless refitted null sets lower d* below 0.016 (the
    largest 80th percentile of d over the sets); the original fits found no valley in any of the bin's
    200 null mocks per variant, but those fits used the same optimiser, so this is not shown.
  - **What this means for R1-SEL (post hoc; the pre-registered label stands).** With converged mock fits
    bin [−0.7, −0.5) would be resolvable in all three variants. Each variant would then have three
    resolvable bins and none almost disjoint (data d = 0.37–0.58 against d* ≤ 0.25), which the 2.1 rule
    reads as "not reproduced". So the lost power of bin [−0.7, −0.5) is an artefact of the mock optimiser, as the
    referee inferred, and R1-SEL would read "not reproduced" if the null sets and the other resolvable
    bins hold up under the same refit. That is not tested here: better null fits could find valleys and
    lower d* from its cap 0.25, and the two other resolvable bins are more exposed to that than bin [−0.7, −0.5)
    (their recorded power mocks reach d = 0.03–0.14; power 1.00 at d* = 0.25); the metal-rich bins'
    power 0, attributed above to the density model, may also be partly optimiser-limited. A pre-registered rerun of R1-SEL with
    data-independent starts in every mock fit is registered as T-049 (done 2026-11-21, section 5.2:
    d* stayed at its cap (bin [0.1, 0.3)'s null sets gained 5 valleys, none passing) and the
    metal-poor bins held up, and R1-SEL-FIT reads "not reproduced (robust;
    selection-term robust)").

### 5.2 R1-SEL-FIT: R1-SEL rerun with data-independent starts in every mock fit (T-049; run 2026-11-20/21)

Pre-registered in section 2.6 (2026-11-20). Run with `"parts": ["selfit"]` (`python -m astrolab run 010`)
on an otherwise idle machine. The first session started on the evening of 2026-11-20. The 15 R1 data
fits passed the check. After the first set (k = 0, the S15 term-E skew-normal null set of bin
[−0.7, −0.5), about 10.9 s per mock) the projection was 16.17 h against the 12 h limit. The run
therefore stopped at 19:25 under the SEL-8 rule, with 157 mocks checkpointed
(`mocks.resumes[0].stopped`). On 2026-11-21 the user consented to resume with a 24 h limit (`log.md`;
`mocks.resumes[0].consent`, `mocks.stop_limit_h`); the number of mocks did not change. The resumed
session started at 03:12 and finished at 08:13 local time (13:13 UTC, `run_info_selfit.json`).

The stop rule counted 5.30 h of elapsed time over both sessions (`mocks.elapsed_h_total`); the resumed
session ran 5.11 h, data fits included (`runtime_h`). The 5,400 mocks (108 sets of 50: 90 main sets
and 18 floor-0.20 sets) took 5.29 h of fit time, against 2.6's estimate of 4.5–5 h. That is 3.53 s per
mock on average (`per_set[].mean_s_per_mock`):
- by variant, 4.67 s for S15 term E, 2.80 s for term N and 3.11 s for Full (T-045: about 4.2 and 2.4 s);
- by kind, 4.08 s for null mocks, and 2.62 s and 3.20 s for power mocks at floors 0.12 and 0.20.

Per-mock seeds make the numbers independent of the stop.

New files: `r1_selfit.json`, `provenance_selfit.json` and `run_info_selfit.json`. `r1_sel.json` and
every recorded label are unchanged. R1-SEL-FIT is a rerun of R1-SEL with improved mock fits, not a
correction of it: R1-SEL's label in section 5.1 stands as that block's pre-registered outcome.

- **Checks (2.6): all passed.** The 15 R1 data fits equal `r1_sel.json` within 10⁻⁹
  (`data_fit_mismatches` is empty). Fit (o) reproduces the recorded d and valley flag of all 5,400
  mocks (`mock_reproduction`: 0 mismatches). No mock had a non-finite likelihood (`nonfinite` is
  empty).
- **Label: R1-SEL-FIT is "not reproduced (robust; selection-term robust)"** (`label`), the outcome 2.6
  stated as expected. Every variant has 4 of 5 bins resolvable and none almost disjoint (data
  d = 0.367–0.580 against d* = 0.25), so the 2.1 rule gives "not reproduced" (`variants.<v>.verdict`).
  Full gives the same verdict (robust), and so does S15 term N (selection-term robust). This holds under the catalogue's quoted age errors: the power mocks are drawn and fitted with them (f = 1), so a nearly disjoint latent split blurred by larger true errors is not excluded (referee, section 6, point 1; error-scale test T-054, section 5.3: robust up to 1.5 times the quoted errors); and the power model is the most favourable shape, so the label means the data do not show XR22's idealised split (point 2).
- **Floor 0.20.** The label is the same (`label_floor_sensitivity`), with 4 of 5 bins resolvable in
  each variant (`floor_sensitivity.<v>`).
- **The verdict does not depend on the metal-rich bins.** The three metal-poor bins have power 1.00 in
  every variant, which already gives three resolvable bins.

| Variant | Resolvable bins, R1-SEL → R1-SEL-FIT | Almost disjoint | Verdict, R1-SEL → R1-SEL-FIT |
|---|---|---|---|
| S15 term E (primary) | 2 → 4 | 0 → 0 | undetermined → **not reproduced** |
| S15 term N | 3 → 4 | 0 → 0 | not reproduced → **not reproduced** |
| Full | 2 → 4 | 0 → 0 | undetermined → **not reproduced** |
| Label | – | – | undetermined (robust; selection-term sensitive) → **not reproduced (robust; selection-term robust)** |

Per bin, R1-SEL (`recorded_r1_sel`) next to R1-SEL-FIT (`variants.<v>.bins[i]`). Power is given under
e = r·τ / e = r·A. The FPR is the largest realised false-positive rate over the four null sets. The
data d values do not change (data fits unchanged); d = 1 means no valley.

| Variant | Bin [Fe/H] | Data d | Power, R1-SEL | Power, R1-SEL-FIT | FPR / q_s / d*, R1-SEL → R1-SEL-FIT | Resolvable, R1-SEL → R1-SEL-FIT |
|---|---|---|---|---|---|---|
| S15 term E | [−0.7, −0.5) | 0.410 | 0.80 / 0.58 | 1.00 / 1.00 | 0 / 0.25 / 0.25 → same | no → **yes** |
| S15 term E | [−0.5, −0.3) | 0.579 | 1.00 / 1.00 | 1.00 / 1.00 | 0 / 0.25 / 0.25 → same | yes → yes |
| S15 term E | [−0.3, −0.1) | 0.502 | 1.00 / 1.00 | 1.00 / 1.00 | 0 / 0.25 / 0.25 → same | yes → yes |
| S15 term E | [−0.1, 0.1) | 1 | 0 / 0 | 0.84 / 0.92 | 0 / 0.25 / 0.25 → same | no → **yes** |
| S15 term E | [0.1, 0.3) | 1 | 0 / 0 | 0.36 / 0.32 | 0 / 0.25 / 0.25 → same | no → no |
| S15 term N | [−0.7, −0.5) | 0.367 | 0.88 / 0.88 | 1.00 / 1.00 | 0 / 0.25 / 0.25 → same | yes → yes |
| S15 term N | [−0.5, −0.3) | 0.580 | 1.00 / 1.00 | 1.00 / 1.00 | 0 / 0.25 / 0.25 → same | yes → yes |
| S15 term N | [−0.3, −0.1) | 0.482 | 1.00 / 1.00 | 1.00 / 1.00 | 0 / 0.25 / 0.25 → same | yes → yes |
| S15 term N | [−0.1, 0.1) | 1 | 0 / 0 | 1.00 / 1.00 | 0 / 0.25 / 0.25 → same | no → **yes** |
| S15 term N | [0.1, 0.3) | 1 | 0 / 0 | 0.50 / 0.56 | 0 / 0.25 / 0.25 → same | no → no |
| Full | [−0.7, −0.5) | 0.386 | 0.70 / 0.74 | 1.00 / 1.00 | 0 / 0.25 / 0.25 → same | no → **yes** |
| Full | [−0.5, −0.3) | 0.579 | 1.00 / 1.00 | 1.00 / 1.00 | 0 / 0.25 / 0.25 → same | yes → yes |
| Full | [−0.3, −0.1) | 0.479 | 1.00 / 1.00 | 1.00 / 1.00 | 0 / 0.25 / 0.25 → same | yes → yes |
| Full | [−0.1, 0.1) | 1 | 0 / 0 | 0.98 / 0.98 | 0 / 0.25 / 0.25 → same | no → **yes** |
| Full | [0.1, 0.3) | 1 | 0 / 0 | 0.44 / 0.36 | 0 / 0.25 / 0.25 → same | no → no |

Floor-0.20 power sets. Only three bins have their own power model at floor 0.20; the null sets, d*
and the other bins are shared with the primary. R1-SEL is from `r1_sel.json` `floor_sensitivity`,
R1-SEL-FIT from `floor_sensitivity.<v>.bins[i]`. In R1-SEL the three verdicts at floor 0.20 were the
same as at floor 0.12.

| Variant | Bin [Fe/H] | Power, R1-SEL | Power, R1-SEL-FIT |
|---|---|---|---|
| S15 term E | [−0.3, −0.1) | 1.00 / 1.00 | 1.00 / 1.00 |
| S15 term E | [−0.1, 0.1) | 0.04 / 0.06 | 1.00 / 1.00 |
| S15 term E | [0.1, 0.3) | 0 / 0 | 0.34 / 0.30 |
| S15 term N | [−0.3, −0.1) | 1.00 / 1.00 | 1.00 / 1.00 |
| S15 term N | [−0.1, 0.1) | 0.68 / 0.60 | 1.00 / 1.00 |
| S15 term N | [0.1, 0.3) | 0 / 0 | 0.70 / 0.70 |
| Full | [−0.3, −0.1) | 1.00 / 1.00 | 1.00 / 1.00 |
| Full | [−0.1, 0.1) | 0.52 / 0.36 | 1.00 / 1.00 |
| Full | [0.1, 0.3) | 0 / 0 | 0.60 / 0.44 |

- **Reported without verdict (2.6, from `per_set`).**
  - **Valley flag changes: 334 of 5,400 mocks, all gains.** No mock lost a valley.
    - Null mocks: 5, all in bin [0.1, 0.3) (S15 term E 2, term N 1, Full 2). None of these valleys
      passes, so every FPR stays 0 and d* stays at its cap.
    - Primary power mocks: 306 (bin [−0.7, −0.5) 71, [−0.1, 0.1) 56, [0.1, 0.3) 179).
    - Floor-0.20 power mocks: 23.
  - **Pass changes: 825 mocks, all gains.** In every power set the new power minus the recorded
    power equals the number of changes. By kind: null 0, primary power 484 (bins [−0.7, −0.5) 71,
    [−0.1, 0.1) 286, [0.1, 0.3) 127), floor-0.20 power 341.
  - **NLL rising with K (K = 1–4).** Under (o) the NLL rises in 1,748 of 5,400 mocks: 509 null (508
    of them in bin [0.1, 0.3)), 737 primary power and 502 floor-0.20 power. Under the new fits it
    rises in 1: one null mock of Full, bin [0.1, 0.3), split-normal null, e = r·A (set k = 87).
  - **K chosen by BIC.** Under (o), K = 1 / 2 / 3 / 4 in 47 / 720 / 1,760 / 2,873 mocks. Under the
    new fits, 0 / 524 / 798 / 4,078.
    - Every power mock of the four bins above [−0.7, −0.5) now chooses K = 4.
    - In bin [−0.7, −0.5)'s power mocks, K = 3 in 273 of 300 and K = 4 in 27.
    - The null mocks of bin [0.1, 0.3) chose K = 2 in 599 of 600 under (o). Under the new fits they
      choose K = 2 in 524, K = 3 in 73 and K = 4 in 3.
  - **Bin [−0.7, −0.5) repeats T-045.** Its six power sets give the same K counts (K = 3 in 43–47 of
    50) and the same 95th percentiles of d (0.017, 0.015, 0.009, 0.009, 0.009, 0.009) as the
    diagnostic, as the shared stream intends.
  - **d of the new power mocks** (range of the set medians, and the largest 95th percentile;
    `d_new_quantiles_5_50_80_95`, both floors):
    - [−0.5, −0.3): 0.003–0.009, at most 0.011.
    - [−0.3, −0.1): 0.038–0.059, at most 0.069. R1-SEL's power mocks reached 0.14.
    - [−0.1, 0.1): 0.183–0.224, at most 0.259.
    - [0.1, 0.3): 0.234–0.275, at most 0.326.
    - The true d of the metal-rich power models is 0.016 and 0.038.
- **Reading (post hoc, 2026-11-21; no verdict).**
  - With converged mock fits, the null sets did not move d*, and the metal-poor bins kept or gained
    power. So R1-SEL's line between "undetermined" and "not reproduced" (section 5.1) was set by the
    mock optimiser, as the T-045 diagnostic suggested. With better mock fits all three variants read
    "not reproduced": the valleys present in the fits to the data (d = 0.37–0.58) are far from almost
    disjoint, under the quoted age errors (see the label bullet above).
  - Section 5.1 attributed the metal-rich bins' power 0 to the density model. That was only partly
    right. With better fits, bin [−0.1, 0.1) is resolvable in every variant, at both floors. In bin
    [0.1, 0.3) the power mocks still give median d ≈ 0.23–0.28 against a true 0.038, so its power stays
    at 0.30–0.70: the K ≤ 4 Gaussian smearing remains there.
  - The resolvability of bin [−0.1, 0.1) at floor 0.12 is narrow for S15 term E (power 0.84 under
    e = r·τ). This does not affect the verdict.

### 5.3 R1-ERR: error-scale power test of R1-SEL-FIT (T-054; run 2026-11-21/22)

Pre-registered in section 2.7 (2026-11-21). Run with `"parts": ["err"]` (`python -m astrolab run 010`) on
an otherwise idle machine with the default thread settings (`threads`; the first, single-threaded
attempt is described at the end of 2.7). One session, no stop: 4.21 h in all (`runtime_h`), of which
the 3,600 mocks took 4.02 h (`mocks.elapsed_h_total`, against 2.7's 2.5–3.7 h), the projection staying at
3.9–4.1 h against the 16 h limit. That is 4.01 s per mock on average: 5.76 s for S15 term E, 3.15 s for
term N and 3.12 s for Full; 3.68, 4.00, 4.10 and 4.26 s at f = 1.2, 1.5, 2.0 and 2.81
(`per_set[].mean_s_per_mock`). Cache only, no download.

New files: `r1_err.json`, `provenance_err.json` and `run_info_err.json`. `r1_sel.json`, `r1_selfit.json`
and every recorded label are unchanged; R1-ERR gives no R1 verdict.

- **Checks (2.7): all passed.** (a) The 9 data fits of the metal-poor bins equal `r1_sel.json` within
  10⁻⁹ (`checks.data_fit_mismatches` is empty). (b) The generator at f = 1 reproduces the recorded d and
  valley flag of all 18 R1-SEL-FIT mocks (`checks.generator_f1`: 18 of 18). Every f is feasible (no
  generator failure in any set), no set has a non-finite result, and no star was dropped by the redraw
  limit (`per_set[].dropped_by_redraw_limit` = 0 everywhere).
- **Label: R1-ERR is "robust up to f = 1.5 (one bin explainable from f = 2.0: [-0.3, -0.1))"**
  (`label`, case 5). In S15 term E, E(1.2) = E(1.5) = 0, E(2.0) = 1 (bin [−0.3, −0.1)) and
  E(2.81) = 0 (`variants.S15E.per_f`), so no f has E ≥ 2 and X = 1.5. The median rule gives the same
  label (`label_median_rule`). The outcome is one of those 2.7 listed as foreseeable ("robust up to
  f = 1.5"), and the hand estimate there (recovered d below 0.37 at f ≤ 1.5, bin [−0.3, −0.1) first to
  reach) held.
- **Reported labels (they do not qualify the primary).** S15 term N: "robust up to f = 1.5 (one bin
  explainable from f = 2.0: [-0.3, -0.1), [-0.5, -0.3))" (bin [−0.3, −0.1) at f = 2.0, bin
  [−0.5, −0.3) at f = 2.81). Full: **"sensitive at f = 2.81"**: at f = 2.81 bin [−0.5, −0.3) reaches in
  3 of 50 mocks (e = r·τ, exactly the threshold; 95% interval 0.013–0.165) and bin [−0.3, −0.1) in 35 of
  50 (e = r·τ). By the median rule both read "robust up to f = 1.5 (one bin explainable from f = 2.0:
  [-0.3, -0.1))".

Per bin in S15 term E: data d (R1-SEL-FIT), the median fitted d of the 50 power mocks under e = r·τ / e = r·A
(`per_set[].d_pct_5_50_80_95`, 50th), and n_reach of 50 under each mechanism. A median of 1 means that no
mock had a valley.

| Bin | Data d | f = 1.2 | f = 1.5 | f = 2.0 | f = 2.81 |
|---|---|---|---|---|---|
| [−0.7, −0.5) | 0.410 | 0.028 / 0.025; 0, 0 | 0.052 / 0.053; 0, 0 | 0.141 / 0.147; 0, 0 | 0.357 / 0.381; 0, 0 |
| [−0.5, −0.3) | 0.579 | 0.027 / 0.025; 0, 0 | 0.092 / 0.086; 0, 0 | 0.286 / 0.222; 0, 0 | 0.471 / 0.494; 1, 0 (3 without a valley) |
| [−0.3, −0.1) | 0.502 | 0.112 / 0.117; 0, 0 | 0.252 / 0.256; 0, 0 | 0.614 / 0.688; **50, 50** | 1 / 1; 0, 0 (all 50 without a valley) |
| E(f) | – | 0 | 0 | 1 | 0 |

- **The ladder is not monotone in bin [−0.3, −0.1).** At f = 2.0 every mock's valley is shallower than
  the data's (d 0.54–0.76). At f = 2.81 the blurred split has no valley at all in S15 (all 200 mocks of
  term E and term N; Full: 50 of 50 under e = r·A, 15 of 50 under e = r·τ). A dip that is
  not there does not reproduce the data's dip, so 2.7 counts these mocks out of n_reach; this is why
  E(2.81) = 0 in S15 term E. X is defined over every f′ ≤ f, so E(2.81) = 0 does not raise X above 1.5.
  So in term E bin [−0.3, −0.1) is explainable at f = 2.0 only, although the pre-registered qualifier
  reads "from f = 2.0". That term E reads "robust" and Full "sensitive at f = 2.81" rests on bin
  [−0.5, −0.3) reaching in 1 against 3 of 50 mocks, within the 50-mock precision of 2.7 (referee, point 2).
- **Other per-set numbers.** n_reach is 0 of 50 (95% interval 0–0.071) in every set at f ≤ 1.5. The fit
  chose K = 4 in every mock at f ≥ 1.5 (K = 3 in some mocks of bin [−0.7, −0.5) at f = 1.2). No mock's NLL rises
  with K after the better-fit rule (`nonmonotone` = 0); under fit (o) alone it does in 1,020 of 3,600
  (`o_nonmonotone`), so the data-independent starts mattered here as in 2.6. The mean pass rates of the
  S15 mocks (0.83–0.94) track the data's S15 fractions (0.872, 0.909, 0.935), a little lower at larger f.
- **The power model is younger than the data.** The mocks' median observed age is 6.3–6.6, 5.4–5.5 and
  4.7–4.8 Gyr in the three bins, against the data's 8.85, 7.43 and 6.02 Gyr; their 5th percentile is
  about 1.8–2.0 Gyr against 2.4–4.2 Gyr (`age_pct_5_50_95_median_over_mocks`, `data_age_pct_5_50_95`).
  The idealised split puts more weight in its young uniform component than the data have. Their
  95th percentile reaches the data's at f = 2.0 in the two lower bins (14.5 against 14.3 Gyr; 12.73
  against 12.72 Gyr) and passes it at f = 2.81 there (15.4, 13.4 Gyr); in bin [−0.3, −0.1) it stays at or
  below the data's (11.2 against 11.27 Gyr). This is reported, not part of any rule.
- **The 2.1 verdict R1 would read at f** (`variants.<v>.per_f.<f>.r1_verdict_at_f`; power at d* = 0.25
  in the R1-ERR bins, the rest from R1-SEL-FIT): "not reproduced" in every variant at f = 1.2 and 1.5. At f = 2.0 it is "undetermined" in S15 term E, where bin [−0.3, −0.1) loses its
  power at 0.25 (0.00) and bin [−0.5, −0.3) keeps 0.28 / 0.80, and "not reproduced" in term N and Full.
  At f = 2.81 it is "undetermined" in every variant.
- **Companion data refit (not decisive).** Refitting the data bins with f × e_Age lowers their d: in
  S15 term E 0.342 / 0.574 / 0.417 at f = 1.2, 0.246 / 0.546 / 0.348 at 1.5, 0.078 / 0.465 / 0.227 at
  2.0 and 0.057 / 0.271 / 0.160 at 2.81 (`companion_refits`; K = 4 and a valley in every refit). So if the
  true errors were twice the quoted ones and the fit knew it, two of the three bins would show a valley
  below d* = 0.25, and at f = 2.81 all three would in term N and Full. Without a mock calibration at that
  f this does not show an almost-disjoint split.
- **Reading (post hoc, 2026-11-22; no verdict).**
  - R1-SEL-FIT's "not reproduced" does not rest on the quoted errors being exact. If the true errors are
    up to 1.5 times the quoted ones, XR22's idealised split, fitted as the data are fitted, leaves valleys
    far deeper than the data's in all three metal-poor bins (n_reach 0 of 50 in all 36 sets), under both
    error mechanisms and in all three variants.
  - At about twice the quoted errors, the bin with the smallest gap, [−0.3, −0.1), no longer separates
    the two readings: the blurred split reaches the data's d there. At 2.81 the two other bins come
    close (term N and Full reach in [−0.5, −0.3)). At these scales 2.7 already noted that XR22's own
    0.82 Gyr width would leave no room for the added error variance (f ≳ 1.4), and the mocks' observed
    ages are wider than the data's. f_max = 2.81 is a heuristic upper value, not a supported scale.
  - So the remaining room for XR22's idealised split is an age error about twice as large as quoted.
    Whether that is plausible is outside R1-ERR (2.7; Shariat, El-Badry & Bhattacharjee 2025, 11 wide
    pairs, find the quoted errors consistent).
  - This is a statement about XR22's idealised split, not about every split (referee, point 1). The
    power model is younger than the data and its gap starts at the 7.0 Gyr young edge, while the data's
    valleys lie at 7.5–9.8 Gyr; n_reach compares depth, not position. A split with more stars at 7–10 Gyr
    could fill its valley at a smaller f. The companion refits point the same way: with f in the fit the
    data's valleys deepen (below 0.25 in all three bins of term N and Full at f = 2.81, at 9.6–10.9 Gyr),
    so R1-SEL-FIT's "not reproduced" plausibly needs f ≲ 2 (referee, point 3). Neither is calibrated; a
    test with f in the likelihood and a data-matched power model is registered as T-059.

## 6. Referee notes

Independent referee, 2026-11-16 (a subagent that saw README sections 1-4, the code, the results, the
Lean argument and its quote / kind / body table, not sections 5-8; it ran offline synthetic checks).
Triage:

| # | Point | Verified | Action |
|---|---|---|---|
| 1 | M0's S15 selection term is wrong under both mocked mechanisms (with r independent of τ the cut does not depend on τ); it drives the σ recovery bias (+0.28/+0.25), the sample-B bias and the S15/Full differences; the README 2.0 rationale for e = r·A is wrong | yes: the algebra of the cut under both mechanisms; our pre-run diagnosis found the same for r·τ; the referee's synthetic check (σ bias +0.31/+0.29 with the term, −0.02/−0.03 without) | **Accepted.** Verdicts stand as pre-registered ("cannot determine"); post-hoc reading in section 5; the 2.0 rationale corrected there; re-test registered as T-031. |
| 2 | R1 power floor of 10% can never pass the 10% side-mass rule; bin [−0.1, 0.1) unresolvable by construction | yes: `run.py` power model with `m0.valley`'s side-mass test; saved generating model young edge 2.0 Gyr, true d = 1 | **Accepted** (a flaw of the pre-registered specification, implemented as written); verdict stands; noted in section 5; fix in T-031. |
| 3 | R4's "cannot determine" hides a large discrepancy (σ_sel 2.4–2.7 in all variants vs 0.82); R3's span is stably inside its band | yes (results) | **Accepted**; substantive reading reported in section 5 next to the formal labels. |
| 4 | R1's undetermined/not-reproduced line sits on Monte Carlo noise (Full bin 0 power 20/30) from the 30-mock fallback | yes | **Accepted**; open question (rerun at 50 per set). |
| 5 | Mock fits start from the data fit (3 starts) while data fits use 40 | yes | **Accepted limitation**; noted. |
| 6 | r drawn independently of τ in all mocks while corr(e/A, Age) = +0.16 in the data; f_max = 2.81 is not a usable error scale; latent peaks pile up at the 20 Gyr edge in metal-rich bins | partly (correlation not recomputed by us; the rest from results) | **Accepted limitations**; noted in section 7. |
| 7 | R2's ML Gaussian on all stars is not exactly XR22's inset fit (σ 2.40 vs 1.81; 33% above 13.8 Gyr) | yes | **Accepted**; the verdict stands; section 5 states the sensitivity. |
| 8 | Lean: `mod_bin` encoded XR22's hedged "presumably the oldest thick disk stars" as an assertion tagged stated, stronger than its quote; `mod_ages`' quote is a fragment | yes | **Fixed**: relabelled `gap_bin`, GAP [reconstructed]; Lean test passes (now three gaps). `mod_ages`: minor, docstring kept (the Lean body is only an atom). |
| 9 | Literature on young α-rich stars (Chiappini et al. 2015, Martig et al. 2015; IDs given by the referee, unverified) | no | Noted as context for sample A's young tail; not used. |
| 10 | Most important additional test: rerun R3/R4 recovery, sample B and R1 bin [−0.3, −0.1) with a selection term consistent with the mocks, and fix the power floor | – | Registered as T-031 (new pre-registration). |

### Referee of the re-test (R-SEL, 2026-11-20)

The independent referee was a subagent. It saw README sections 1–4, the code, the three new results
files and the per-mock checkpoints, but not sections 5–8 or `log.md`. Because another study was
running, it made only short single-threaded checks. It recomputed every -SEL label from the saved
numbers and found each one as the rules give. Triage:

| # | Point | Verified | Action |
|---|---|---|---|
| 1 | R1-SEL's label, including its "selection-term sensitive", hinges on bin [−0.7, −0.5). That bin's power is lost to mock fits without a valley, including K = 1 chosen by BIC on 40,000+ stars drawn from a two-component model (failed K ≥ 2 fits, inferred). With that bin resolvable, every variant would read "not reproduced". | Yes, from the checkpoints: K = 1 in 2 and 4 of 50 mocks for term E (term N 0/3, Full 4/1); mocks without a valley were 10/21 (term E), 6/6 (term N) and 15/13 (Full); mocks with a valley have median d 0.008–0.027. | **Accepted** as a limitation of the mock fits; the rule was applied as written. Post-hoc reading in section 5.1. A diagnostic rerun with data-independent starts is registered (T-045). |
| 2 | Term N's recovery failure is built into the τ-keyed generator, whose pools are binned in observed age, so R3/R4's "selection-term sensitive" carries no data information. In some sets the mock pass rates do not match the data. | Yes. Recovery mocks pass 0.843/0.849 (term E) and 0.844/0.850 (term N) against the data's 0.862. Under the original generator they pass 0.856/0.862 and term N's bias is −0.014/−0.024. Sample-B misspecification mocks pass 0.903–0.908 against 0.883. | **Accepted**; section 5.1, reading 2. |
| 3 | Term E's assumption is violated to first order under e = r·τ, not to second order as SEL-1 says. Catalogue errors that depend on Teff or M_K at fixed A are not mocked. The 17–20 Gyr pass bin, after a dip at 14–16 Gyr, looks like the grid-edge pile-up (the edge-drop fit gives σ_sel 2.47 and span 5.81). | The wording point: yes, from the algebra. The rest: from the results. | **Accepted**. Wording corrected in section 5.1, reading 3; the untested error dependence and the edge effect are noted in section 7. |
| 4 | Intrinsic-SEL's margin (0.072 Gyr) is smaller than the systematics: the f = 0.8 shift (+0.065), the misspecification bias (+0.05/+0.07) and the term difference (−0.03). The f_max check is one-sided. The old component is Gaussian in all mocks. Old-sequence mock stars draw [Fe/H] from the whole sample-B parent. | Yes, from the results and run.py's draw. | **Accepted**; section 5.1, reading 4; section 7. |
| 5 | R4-SEL carries no "robust" qualifier, while R1-SEL's "undetermined" does. | Yes. | **Rejected** as a defect. Section 2.3 attaches "robust / not robust" only to "reproduced" for R3/R4 (`selaux.with_robust`), while 2.1's R1 robustness applies to any verdict; both are as pre-registered. |
| 6 | The 16 h stop fired, and the limit was raised to 20 h with consent. | Yes. | Disclosed in section 5.1 and `log.md`. |
| 7 | Literature: Silva Aguirre et al. 2018 (arXiv:1710.09847) find that high- and low-α ages overlap; Miglio et al. 2021 (arXiv:2004.14806). | No; the IDs are the referee's and were not verified by us. | Noted as context; not used. |
| 8 | Most important additional test: rerun bin [−0.7, −0.5)'s power sets with data-independent starts, recording the NLL and convergence for each K. | – | Registered as T-045 (a diagnostic; it does not change the label). |

### Referee of R1-SEL-FIT (2026-11-21)

The independent referee was a subagent. It saw README sections 2.0–2.6, the code of the block and the
two results files (`r1_selfit.json`, `r1_sel.json`), but not sections 5–8 or `log.md`. It ran only
short single-threaded inspections of the JSON. It found no bug that changes d, d*, power, a verdict or
the label, and found every rule of 2.6 evaluated as written. Triage:

| # | Point | Verified | Action |
|---|---|---|---|
| 1 | The power mocks draw and fit ages with the catalogue's quoted errors (f = 1, Gaussian kernel). If XR22's true errors are larger or have prior-shaped tails, a nearly disjoint latent distribution would be under-deconvolved and its valley partly filled to the observed d ≈ 0.4–0.6, which the power sets cannot see; 2.6 has no error-scale sensitivity for R1 | yes (`run.py` power-mock generator; 2.0/2.3 vary f only for R3/R4) | **Accepted limitation**: the label reads "not reproduced under the catalogue's quoted age errors"; section 5.2, the root tables and the wiki say so. The test the referee proposes is registered as T-054 |
| 2 | The power model is the most favourable shape (hard-edged uniform young component plus a narrow old Gaussian, true d ≤ 0.02), and the fitted d of a K ≤ 4 Gaussian mixture is smoothed upward (bins 3–4: true d ≤ 0.04 recovered at ≈ 0.19–0.33); a softer split could fail the 0.25 cap. Data fits sit at K = 4 in every bin | yes (`r1_selfit.json` per-set d quantiles, K counts) | **Accepted limitation**: "not reproduced" means the data do not show XR22's idealised split, not that the phases overlap |
| 3 | Choosing between fit (o) and the data-independent fit by NLL (tie 0.01) could bias null and power sets differently | yes: the rule is the same in both; bins [−0.7, 0.1) still have 0 valleys in every null set, so d* stays at the pre-registered cap and is not set by the mocks; any false-valley inflation would have lowered d* (towards "undetermined") | **Rejected** as a bias of the obtained label |
| 4 | Precision of 50 mocks: bin [−0.1, 0.1) term E power 0.84 (rtau) is indistinguishable from 0.80 | yes | **Accepted**; that bin is not needed for the label: bins [−0.7, −0.5), [−0.5, −0.3), [−0.3, −0.1) are 50/50 in all 18 primary power sets of the three metal-poor bins (and in the 6 floor-0.20 sets of bin [−0.3, −0.1)) with d far below 0.25 |
| 5 | The non-monotone count covers K = 1–4 only (T-045 also counted K = 5); one Full null mock (set 87, bin [0.1, 0.3)) is still non-monotone after the better fit, so the new fits are not guaranteed global optima | yes (`run.py`, comment discloses it) | **Accepted**; reported in section 5.2 |
| 6 | All-star R1 bins mix young α-rich stars, accreted or halo stars and migrators, and subgiant selection multiplies the latent distribution by a smooth function of age | – | **Accepted** as a limit of the 2.1 design (interpretation, not validity of the test) |
| 7 | The run stopped early by the projection rule (first projection 16.2 h, actual 5.3 h; slow early sets suggest machine contention) and was resumed | yes: consent recorded in `log.md` (2026-11-21) | No action; results are deterministic |
| 8 | Literature: Shariat, El-Badry & Bhattacharjee 2025 (arXiv:2510.08675; 11 wide pairs do not exclude f > 1) and Chen, Sun & Ye 2025 (arXiv:2510.10092; age-scale shift) bear on point 1; young α-rich stars (Chiappini et al. 2015, Martig et al. 2015) and Kepler/APOKASC age distributions (Silva Aguirre et al. 2018, Miglio et al. 2021) on point 6 | the two 2025 papers are cited in this README; the others unverified (IDs given by the referee) | Noted; not used |
| 9 | Most important additional test: an error-scale power test for R1 (mocks drawn with f·e_Age, f ∈ {1.2, 1.5, 2.0, f_max}, fitted with f = 1), or more cheaply refit the data bins at several f | – | Registered as T-054 |

### Referee of R1-ERR (2026-11-22)

The independent referee was a subagent. It saw README sections 2.0, 2.6 and 2.7, the code of the block,
the tests and the three results files (`r1_err.json`, `r1_selfit.json`, `r1_sel.json`), but not sections
5–8 or `log.md`. It made only short inspections of the JSON. It found no bug and found every rule of 2.7
applied as written, with the label following from the per-set numbers. Triage:

| # | Point | Verified | Action |
|---|---|---|---|
| 1 | The generating model does not look like the data at any f: the mocks are 1.3–2.5 Gyr younger in median observed age, because the power model puts 57–85% of the stars uniformly on 1.5–7 Gyr; the data's valleys sit at 9.8, 7.5 and 9.3 Gyr while the mocks' gap starts at the 7.0 Gyr young edge, and n_reach compares depth only, not position. A split with more stars at 7–10 Gyr could fill the valley at a smaller f, so the true threshold could lie below 2.0 | yes (`age_pct_5_50_95_median_over_mocks`, `r1_sel.json` power models, `r1_selfit.json` `valley_t`) | **Accepted limitation** (as point 2 of the R1-SEL-FIT referee): R1-ERR's label is about XR22's idealised split, not about every split; stated in section 5.3's reading; see point 8 |
| 2 | The primary label at f = 2.81 hangs on the no-valley rule and on binomial noise: bin [−0.3, −0.1) has no valley in 50 of 50 mocks (so E(2.81) = 0 in term E), and primary and Full differ by 1 against 3 of 50 in bin [−0.5, −0.3), within the stated precision. "Explainable from f = 2.0" suggests the bin stays explainable at larger f, which it does not in term E. The ladder does not sample 2.0–2.81 | yes | **Accepted**: the label text is the pre-registered one and stands; section 5.3 states that bin [−0.3, −0.1) is explainable at f = 2.0 only in term E and loses its valley at 2.81, and that "sensitive at f = 2.81" (Full) against "robust" (term E) is within 50-mock precision. X = 1.5 does not depend on f = 2.81 |
| 3 | The companion refits point to sensitivity: with f in the likelihood the data's d falls below 0.25 in all three metal-poor bins of term N and Full at f = 2.81, with valleys moving to 9.6–11 Gyr; read together, R1-SEL-FIT's "not reproduced" plausibly needs f ≲ 2 | yes (`companion_refits`, valley ages 9.6–10.9 Gyr at 2.81) | **Accepted** as a reading, not a verdict (no mock calibration at that f, as 2.7 states); section 5.3 says so |
| 4 | The mocks' 95th percentile of observed age matches the data only at f ≈ 2.0 (two lower bins) or 2.81 (top bin); at f = 1.2 the mocks are too narrow on the old side, so either the old width exceeds 0.82 Gyr or f > 1 | yes | **Accepted** as a diagnostic, not a bound; reported in section 5.3 |
| 5 | Under e = r·τ the S15 pass rate falls with f (bin [−0.7, −0.5) 0.861 → 0.828 against the data's 0.872), and the fitter receives e = r·τ from the true age (inherited from SEL-2) | yes | **Accepted limitation**; no effect on the label (it holds under both mechanisms) |
| 6 | Code and rules: f scales only the deviate, e unchanged, no star dropped; `err_counts`, `err_explainable`, `err_label` match 2.7 and its amendments; checks passed; no moved goalposts | – | No action |
| 7 | Literature: Shariat, El-Badry & Bhattacharjee 2025 (arXiv:2510.08675) find XR22's quoted errors consistent with 11 wide pairs, which disfavours a random-error f much above 1.5, but pairs share [Fe/H] and model systematics and cannot see age-scale distortions that depend on age or [Fe/H]; other photometric subgiant and giant ages underestimate their errors by 2–5× | the 2025 paper is cited in 2.7; the "2–5×" statement is from the referee's search snippet, not verified | Noted; not used |
| 8 | Most important additional test: calibrate R1 at f = 2.0 and 2.81 with f in the likelihood (null and power mocks drawn with f·e and fitted with f), with a power model built from the data's f-deconvolved fit and matched to the observed-age marginal, comparing valley position as well as d | – | Registered as T-059 (backlog) |

## 7. Open questions

- **A selection term consistent with the error mechanism (T-031, done).** Re-tested in section 5.1
  with an empirical age-dependent pass fraction (term E), a corrected power floor and r keyed by
  age. The -SEL labels are reported there next to the original ones.
- **R1-SEL's deciding bin (T-045, done as a diagnostic).** The power of bin [−0.7, −0.5) was lost to
  local optima of the mock fits; with data-independent starts it is 1.00 in all six sets, so R1-SEL
  would read "not reproduced" if the null sets and the other resolvable bins hold up under the same
  refit (section 5.1, post hoc; not tested). A pre-registered rerun of
  R1-SEL with such starts in every mock fit, null sets and all bins included, is T-049.
  **Closed by R1-SEL-FIT (T-049, 2026-11-21, section 5.2).** The null sets kept d* at its cap 0.25
  (no null mock passed), the three metal-poor bins have power 1.00 in every variant, and bin
  [−0.1, 0.1) became resolvable too. R1-SEL-FIT reads "not reproduced (robust; selection-term
  robust)", at both floors, under the catalogue's quoted age errors. R1-SEL's "undetermined" stands as
  its own pre-registered outcome.
- **Error scale of R1 (T-054).** R1's power mocks are drawn and fitted with the catalogue's quoted
  age errors (f = 1), so whether a nearly disjoint latent split blurred by larger true errors would
  look like the data's dip is untested (referee, section 6). An error-scale power test (mocks drawn
  with f·e_Age, f ∈ {1.2, 1.5, 2.0, f_max}, fitted with f = 1) is registered as T-054.
  **Closed by R1-ERR (T-054, 2026-11-22, section 5.3).** R1-ERR reads "robust up to f = 1.5 (one bin
  explainable from f = 2.0: [-0.3, -0.1))": up to 1.5 times the quoted errors the blurred split leaves
  valleys far deeper than the data's in all three metal-poor bins; from about twice the quoted errors
  bin [−0.3, −0.1) no longer separates the readings (Full reads "sensitive at f = 2.81"). A
  prior-shaped (skewed) error kernel stays untested, since no specification of XR22's age-posterior
  shapes is available here.
- **Which error generator is right.** Open points from section 5.1, readings 2–4:
  - Term N fails recovery only under the τ-keyed generator, whose pools carry the age dependence
    of the pass fraction that the errors themselves create.
  - Catalogue errors that depend on Teff or M_K at fixed observed age are not mocked.
  - The intrinsic-SEL label holds only for an error scale f ≳ 0.83, which nothing here bounds.
  - An old component with tails heavier than Gaussian was not tested.
- **Limitations noted by the referee.** Mock fits start from the data fit with 3 starts while data
  fits use 40; f_max = 2.81 (dominated by the true late-phase age spread and by σ_sel) is not a
  usable error scale; latent peaks pile up at the 20 Gyr grid edge in metal-rich bins, which affects
  BIC and the K cap. For R1, R1-SEL-FIT (section 5.2) adds 8 data-independent starts per K to
  every mock fit.
- **R1 power.** Metal-rich bins have no power under the pre-registered generating model (one by
  construction, section 5); a model with a sharper young edge, or ages from a different pipeline,
  would be needed to resolve them. With better mock fits (R1-SEL-FIT, section 5.2), bin [−0.1, 0.1)
  is resolvable (power 0.84–1.00). Bin [0.1, 0.3) is not (power 0.30–0.70; its power mocks give
  median d ≈ 0.23–0.28 against a true 0.038), so the density-model limit remains there.
- **Absolute age scale.** The 13 Gyr mean moves by ~1 Gyr with the isochrone grid and α scale, and the
  deconvolved mean is 0.3–0.7 Gyr lower; an independent age scale (e.g. Chen, Sun & Ye 2025) on the
  same stars would show whether the onset epoch survives.
- **Mock budget (done in the re-test).** R-SEL used 50 mocks per set. The R1 line still sits on
  one bin's power (section 5.1). In R1-SEL-FIT it does not: three bins have power 1.00 in every
  variant (section 5.2).

## 8. Exploring via chat

How a coding agent answers "what if" questions about this study without touching `results/`
(rules: AGENTS.md section 2). All knobs below reuse the cached catalogue (about 16 MB, fetched once).

| Knob (`PARAMS`) | Meaning | Safe range | Cache only, or new data (size)? |
|---|---|---|---|
| `cut` | S15 relative-error cut e_Age/Age | 0.10–0.20 | cache only |
| `r1_bins` | [Fe/H] bins of R1 | 0.1–0.3 dex wide, within −1 to 0.4 | cache only |
| `valley_lo`, `valley_hi` | age range searched for the R1 valley (Gyr) | 4–12 | cache only |
| `kmax` | largest mixture size for R1/R7 | 3–5 | cache only |
| `nstart`, `nstart_r1_data` | optimiser starts (models; 1-D mixture data fits) | 8–80 | cache only |
| `n_mock` | mocks per set (R1 calibration, recovery) | 2–50 (2 for a quick run; verdicts need the full count) | cache only |
| `seq_feh`, `seq_jphi` | [Fe/H] window and J_φ cut of samples A/B | −1.5 to 0.5; 0–1000 | cache only |
| `r2_feh`, `r2_jphi` | R2 sample window and J_φ cut | ±0.1 dex around −1; 0–1000 | cache only |
| `f_min` | error-scale sensitivity value | 0.6–1.0 | cache only |
| `grid_step` | latent grid step (Gyr) | 0.02–0.1 | cache only |
| `parts` | which pipeline runs: `["orig"]` (sections 2.0–2.4; `r1/r2/r34/r56/r7/summary.json`) and/or `["sel"]` (section 2.5 R-SEL; `r1_sel/r34_sel/sel.json`), or `["selfit"]` alone (section 2.6 R1-SEL-FIT; `r1_selfit.json`, records `provenance_selfit.json`, `run_info_selfit.json`; reads `r1_sel.json`), or `["err"]` alone (section 2.7 R1-ERR; `r1_err.json`, records `provenance_err.json`, `run_info_err.json`; reads `r1_sel.json` and `r1_selfit.json`), or `["errcal"]` alone (section 2.8 R1-ERRCAL; `r1_errcal.json`, records `provenance_errcal.json`, `run_info_errcal.json`; reads `r1_sel.json`, `r1_selfit.json` and `r1_err.json`); the committed value is `["err"]` (T-054) | either or both of orig/sel; selfit alone; err alone; errcal alone | cache only |
| `selfit_seed_tag`, `selfit_nstart`, `selfit_stop_h` | R1-SEL-FIT: stream tag of the data-independent starts, starts per K, stop limit (h) | 45 and 8 are pre-registered; 12 h | cache only |
| `err_f`, `err_bins`, `err_n_mock` | R1-ERR (section 2.7): error-scale ladder, R1 bins run, mocks per set | pre-registered [1.2, 1.5, 2.0, 2.81], [0, 1, 2], 50 (2 for a quick run; the label needs 50) | cache only |
| `err_reach_frac`, `err_min_bins` | R1-ERR: fraction of mocks reaching the data d that makes a bin explainable; bins needed for "sensitive" | 0.05 and 2 are pre-registered | cache only |
| `err_seed_tag`, `err_seed_tag_indep`, `err_stop_h` | R1-ERR: stream tags of the catalogue and fit (o), and of fit (i); stop limit (h) | 54 and 154 are pre-registered; 16 h | cache only |
| `errcal_f`, `errcal_bins`, `errcal_n_mock` | R1-ERRCAL (section 2.8): error scales (fitted with f), R1 bins run, mocks per set | pre-registered [2.0, 2.81], [0, 1, 2], 50 (2 for a quick run; the label needs 50) | cache only |
| `errcal_seed_tag`, `errcal_seed_tag_indep`, `errcal_stop_h` | R1-ERRCAL: stream tags of the catalogue and fit (o), and of fit (i); stop limit (h) | 59 and 159 are pre-registered; 16 h | cache only |
| `sel_n_mock` | R-SEL mocks per set (verdicts need 50) | 2–50 | cache only |
| `sel_power_floor`, `sel_power_floor_sens` | R1-SEL power-model floor and its sensitivity value | 0.10–0.30 | cache only |
| `sel_pass_width`, `sel_n_min` | pass-bin width (Gyr) and minimum parent count per pass bin (SEL-0) | 0.5–2; 100–500 | cache only |

- Exploration checkpoints: since 2026-11-22 (T-058) R-SEL and R1-SEL-FIT explorations, like R1-ERR's
  since T-054, keep their mock checkpoints under a sibling root (`s010_sel_mocks_explore`,
  `s010_selfit_mocks_explore`, `s010_err_mocks_explore`, each under `<date>-<tag>`; R1-ERRCAL's under
  `s010_errcal_mocks_explore`, T-059), never in the formal folders, so pruning exploration checkpoints cannot touch the formal ones.
- Rerun with an override: `python -m astrolab explore 010-m05-thick-disc-subgiant-ages --tag <topic> --set KEY=VALUE`
  (outputs in `explore/<date>-<topic>/`, not committed). The original pipeline needs
  `--set 'parts=["orig"]'`; without mocks
  (`--set n_mock=2 --set n_mock_reduced=2 --set n_boot=2 --set n_boot_r6=5`) it takes about 30 min,
  and the full calibration about 5 h. The R-SEL pipeline (the default) takes about 0.75 h of data fits
  plus mocks (`--set sel_n_mock=2` for a quick run; at 50 per set the mocks took 6 h of compute and
  the interrupted run 10 h in all). Its mocks are
  checkpointed in the cache under a key of the code and PARAMS, so an override starts a new folder
  (an exploration's folders sit under a separate root, see the item above);
  it needs about 6 GB of memory at peak (section 5.1). Since 2026-11-20 (T-046, after the R-SEL
  run; the code change gives a new checkpoint key) a refused file replace is retried for about 25 s
  before the run stops, and on a resume the projection counts mocks already checkpointed as
  finished, with their recorded times, instead of as remaining work (`selaux.run_mock_sets`; in the
  log of projections `mocks_left` now counts only mocks without a checkpoint, and
  `mocks_checkpointed_not_replayed` is new).
- Analyses `run.py` does not cover: a script `explore/<name>.py` with `def main(ctx)`, run with
  `python -m astrolab explore 010-m05-thick-disc-subgiant-ages --tag <topic> --script explore/<name>.py`.
  Existing: `explore/t045_r1sel_power_refit.py` (T-045: refit of bin [−0.7, −0.5)'s R1-SEL power mocks
  with data-independent starts, about 20 min).
  A script can `import run` and reuse `run.load`, `run.flags`, `run.onedim`, `run.grouped`,
  `run.fit_mixtures`, `run.fit_seq` and `m0`/`mocks` (see the execution log of `design/019-plan_*` for examples of
  convergence and recovery checks).
- Results files and keys: `summary.json` (all verdicts, key numbers, mock budget, `params`);
  `r1.json` (`bins.<sample>[i]`: d, d_star, power, edge, resolvable, almost_disjoint; `verdict`;
  `latent_density`, `grid_mid`); `r2.json` (`primary`, `sensitivity`, `checks`, `envelope`, `verdict`);
  `r34.json` (`sampleA`, `sampleA_sensitivity`, `fig2e`, `sampleB`, `recovery`, `sampleB_mock_bias`,
  `error_scale`, `primary`, `verdict`); `r56.json` (age–[Fe/H] histograms, cross-fractions, R6
  percentiles); `r7.json` (`rows`: median, 95% width, largest fraction within 1.5 Gyr).
  R-SEL: `r1_sel.json` (`variants.<S15E|S15N|Full>.bins[i]` and `.verdict`; `floor_sensitivity`;
  `label`; `data_fits` with the power models); `r34_sel.json` (`terms.<E|N>`: `sampleA`, `recovery`,
  `R3`, `R4`, `robustness_fits`, `error_scale`; `intrinsic.<E|N>`; `sampleA_extra_E`; `fig2e_E`;
  `shared_full_fits`; `labels`); `sel.json` (`pass_tables`, `data_pass_frac`, `r2_deconvolved`,
  `sel7`, `diagnostic`, `mock_pass_rates`, `mocks` with the runtime projections, `labels`,
  `memory_peak_mb`). R1-SEL-FIT: `r1_selfit.json` (`status`, `label`, `label_floor_sensitivity`,
  `variants`, `floor_sensitivity` as in `r1_sel.json`; `recorded_r1_sel`; `per_set` (valley counts,
  K chosen, NLL rising with K over K = 1–4 under (o) and under the new fits, how often (i) was used per K,
  changes in valley and pass, time per mock); `data_fit_mismatches`,
  `mock_reproduction`; `mocks` with the projections). The R1-SEL-FIT run (the committed default) takes
  about 5 h of mocks plus about 25 min of data fits, on an otherwise idle machine. The formal run took
  5.29 h of mock fit time, 3.53 s per mock, and 5.30 h of elapsed time with one stop and a resume
  (section 5.2). Its 12 h stop rule fired after the first set, whose mocks are the slowest (10.9 s each),
  so a rerun needs either a higher `selfit_stop_h` or a resume with consent.
  R1-ERR: `r1_err.json` (`status`; `label` (S15 term E: `label`, `case`, `X`, `Y`, `Z`, `Z_bins`,
  `F_end`, `W3`, `all_bins_explainable_from`) and `label_median_rule`; `checks` (`data_fit_mismatches`,
  `generator_f1`); `ladder`, `bins`, `data_d`, `cut_f`, `feasible`; `f1_row` (n_reach at f = 1 from
  `r1_selfit.json`); `variants.<S15E|S15N|Full>` with `label`, `label_median_rule` and `per_f.<f>`
  (`status`, `E`, `explainable_bins`, per-bin `n_reach`, `n_novalley`, `power_at_d_cap`,
  `r1_verdict_at_f`); `per_set` (per-mock `d` and `valley`, `n_reach` with `n_reach_cp95`, `n_novalley`,
  `n_d_ge_data_incl_novalley`, d percentiles over all mocks and over mocks with a valley, power at 0.25,
  K chosen, use of (i), NLL rising with K, pass rate, observed-age percentiles against the data's, stars
  dropped by the redraw limit, generator failures, time per mock); `companion_refits.<variant>.<f>`;
  `mocks` with the projections). The R1-ERR run (the committed default) is estimated at 4–5 h on an
  otherwise idle machine (section 2.7); its checkpoints are in the cache folder `s010_err_mocks`.
  `--set err_n_mock=2` gives no label and still takes about 1.3 h: the 9 data fits, check (b) and the 36
  companion data refits run in full, and only the mock sets shrink.
- R1-ERRCAL (section 2.8): the formal run is `"parts": ["errcal"]` (run alone; the committed default stays
  `["err"]`), with the default thread settings (recorded in `threads`), on an otherwise idle machine: about
  30 min of data fits at f plus 5,400 mocks, about 6–8 h in all. Checkpoints go to the cache folder
  `s010_errcal_mocks` (explorations: `s010_errcal_mocks_explore/<date>-<tag>`). It writes `r1_errcal.json`
  (`status`; `label` (S15 term E) and `labels.<variant>`; `checks.data_fit_mismatches`; `data_fits.<f>.<variant>`
  with the null parameters at f; `power_models`; `variants.<variant>` with `verdicts` and `per_f.<f>` (`status`,
  `verdict`, `median_edge`, per-bin `d_star`, `q`, `power`, `fpr`, `resolvable`, `almost_disjoint`, and the
  metal-rich bins from `r1_selfit.json`); `per_set`; `mocks` with the projections) and the records
  `provenance_errcal.json`, `run_info_errcal.json`. `--set errcal_n_mock=2` gives no label and takes about
  1 h (the 18 data fits run in full).
- Example questions: "Does the R1 valley survive a stricter error cut?" → `--set cut=0.10`.
  "Is the 13 Gyr mean sensitive to the J_φ cut?" → `--set r2_jphi=300` (R2 also reports 300 and 700).
  "What if the selection term conditioned on relative error instead of e?" → an `explore/` script
  (a post hoc question, see section 7).
- Findings that change what we know go into `log.md` (and the wiki article) on a branch.
