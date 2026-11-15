# M5 Milky Way thick disc: early formation from subgiant ages

> Write sections 1–4 BEFORE writing run.py (pre-registration). Edit them later only
> with a dated note explaining the change.

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
scatter "∼0.82 ± 0.01 Gyr", called an upper limit, so that enrichment from [Fe/H] ≈ −1 to +0.5 took
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
fixed before the full catalogue is fetched (only a 5-row format trial has been seen).

### 2.0 Definitions shared by all parts

- **Catalogue columns:** Id, Age, e_Age (Gyr), [Fe/H], e_[Fe/H], [alpha/Fe], e_[alpha/Fe] (may be
  blank), JPHI (kpc km/s), MKcomb.
- **S15:** e_Age/Age < 0.15. **Full:** all rows with finite Age and e_Age > 0.
- **Early / late (XR22 eq. 1):** late if JPHI > 1500 and [α/Fe] < 0.16 ([Fe/H] < −0.5) or
  [α/Fe] < −0.16[Fe/H] + 0.08 ([Fe/H] ≥ −0.5); early otherwise. Rows with blank [α/Fe] are counted
  and excluded from every selection that uses [α/Fe]. "Above the α line" means [α/Fe] at or above
  the eq. 1 boundary.
- **Sign check:** run.py asserts that the median JPHI of the full catalogue lies in 1500–2100
  (prograde positive), that the row count is 247,104 and that Id is unique.
- **M0 (observation model).** Latent ages τ on a grid of 0.05 Gyr over [0, 20] Gyr (the YY grid edge;
  plan 019 named 0.02 Gyr, and the main R2–R4 fits are repeated at 0.02 Gyr as a check). For star i,
  g_i(A | τ) is a Gaussian in A with mean τ and width e_Age,i, truncated to [0, 20] and renormalised
  for each τ. On S15, the likelihood of star i is
  L_i = ∫ p(τ|θ) g_i(Age_i|τ) dτ / ∫ p(τ|θ) P_i(τ) dτ, with P_i(τ) = ∫ g_i(A|τ) dA from
  A = e_Age,i/0.15 to 20 (the probability that a star of true age τ passes the 15% cut, given its
  e_Age; treating e_Age as given is an approximation, stated as a limitation). On Full, the
  denominator is 1. Edge sensitivity: (i) refit without stars with Age + 2 e_Age > 20; (ii) an
  untruncated Gaussian observation model. Each verdict below is "robust" only if it holds on S15 and
  on Full.
- **Fitting.** Maximum likelihood (L-BFGS-B) from 8 starting points per model (seeded, seed 0);
  the best is kept; ties (log-likelihood within 0.01) are broken by the smaller K, then the earlier
  start. Uncertainties from the inverse Hessian (flat priors make this the large-sample posterior;
  plan 019 spoke of posterior medians, replaced here because a per-star grid likelihood for ~10⁴–10⁵
  stars is too slow for MCMC on a laptop), checked by 50 bootstrap resamples for σ_sel.

### 2.1 R1 · The 8 Gyr split (verdict)

- **Sample and bins:** S15 (and Full as the robustness check), all stars with a valid age regardless
  of [α/Fe] or JPHI, in five [Fe/H] bins of 0.2 dex: [−0.7, −0.5), [−0.5, −0.3), [−0.3, −0.1),
  [−0.1, 0.1), [0.1, 0.3).
- **Density model:** latent ages = mixture of K Gaussians (K = 1–4), each truncated to [0, 20] and
  normalised, fitted in M0; K chosen by the Bayesian information criterion (BIC). If BIC picks
  K = 4, K = 5 is also fitted and only modes present in both are counted (bins hitting the cap are
  listed).
- **Modes and valley:** density on the 0.05 Gyr grid; a peak is a local maximum whose prominence is at
  least 10% of the lower of the two peaks it separates from. The valley is the deepest local minimum
  between 5 and 11 Gyr with at least 10% of the latent mass on each side; its depth
  d = density(valley) / min(density of the highest peak on each side). No valley → d = 1.
- **Null calibration:** a skew-normal latent distribution (unimodal, non-Gaussian) is fitted to the
  bin in M0; 100 mock samples of the bin's size are drawn: latent ages from the fit, relative errors
  e/τ resampled from the bin's observed e_Age/Age, observed ages Gaussian and truncated to [0, 20],
  the S15 cut applied (for S15). The same pipeline gives d for each; d_crit = 5th percentile of the
  null d (false-positive rate 5%).
- **Power:** 100 mocks from a two-Gaussian latent model (means 5.5 and 10.5 Gyr, widths 1.2 Gyr,
  equal weights; an XR22-like separation), same error and cut procedure; power = fraction with
  d < d_crit and d ≤ 0.25. Bins with power < 80% are reported as "cannot resolve" and excluded.
- **Per bin:** "almost disjoint" if d < d_crit **and** d ≤ 0.25. Young-side upper edge = 97.5th
  percentile of the latent mass younger than the valley (a proxy we choose; XR22 give no definition).
- **Verdict:** **reproduced** if at least 3 bins are resolvable, at least 3 of them are almost
  disjoint, and the median young-side upper edge of the almost-disjoint bins lies in 6.5–9.5 Gyr.
  **Undetermined** if fewer than 3 bins are resolvable. **Not reproduced** otherwise.
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
  MIST +0.5 Gyr (XR22 Extended Data Fig. 4); [α/Fe] systematics of about 0.1 dex in LAMOST DD-Payne
  abundances (Xiang et al. 2019, arXiv:1908.09727) times XR22's sensitivity of 1–2 Gyr per 0.2 dex
  (Extended Data Fig. 4) gives ±0.5–1 Gyr; a re-analysis finds ages 12.9% younger (Chen, Sun & Ye
  2025, arXiv:2510.10092; −1.7 Gyr at 13 Gyr); [Fe/H]/Teff offsets and the parallax zero point
  (Lindegren et al. 2021, arXiv:2012.01742, about −17 to −21 μas) are listed without a propagated
  age shift because we found no verified sensitivity. The envelope is printed next to the 0.8 Gyr
  margin to the Big Bang.

### 2.3 R3/R4 · The old-disc sequence (verdicts)

- **Sample A (reproduction):** S15, [α/Fe] above the eq. 1 line, JPHI > 500, −1.2 < [Fe/H] < 0.5.
- **Model:** latent τ | [Fe/H]_i ~ N(τ̄0 + a[Fe/H]_i, σ²), truncated to [0, 20], in M0 (S15 selection
  term included). The degenerate form without truncation or selection,
  Age_i ~ N(τ̄0 + a[Fe/H]_i, σ² + e_Age,i²) (XR22's), is also fitted.
- **Verdicts on sample A (σ_sel is the scatter of the α-selected sample, a like-for-like
  reproduction of XR22's number, not the intrinsic scatter):**
  - **R4 reproduced** if σ_sel ≤ 0.92 Gyr (XR22's 0.82 plus 0.1 Gyr; XR22's 0.82 ± 0.01 is the fitted
    scatter, called an upper limit because measurement errors may be underestimated).
  - **R3 reproduced** if |a| × 1.5 dex (the span from −1 to +0.5) lies in 4.5–6.5 Gyr (XR22: "5–6
    Gyr", ±0.5 Gyr), and, as a check of the fit, a lies in −3.8 ± 0.3 Gyr/dex and τ̄0 in 9.38 ± 0.3 Gyr.
  - Each is "robust" only if it also holds on Full and in the version with a² e_[Fe/H]² added to the
    variance (which lowers σ; the unpublished age–[Fe/H] error covariance is not modelled in either
    version). The span is also reported with the sample truncated at [Fe/H] < −0.2 and < 0.
- **Intrinsic scatter (verdict):** sample B: S15, early, JPHI > 500, −1.2 < [Fe/H] < 0.5, no α cut.
  Model: mixture of the old-sequence component above (weight 1 − f) and one background component
  with a [Fe/H]-independent truncated Gaussian age distribution (mean, width, weight f), in M0.
  Recovery is checked on 50 mocks drawn from the fitted model with the real [Fe/H] and error
  distributions. If the mock bias in σ exceeds 0.1 Gyr, the verdict is **cannot determine**;
  otherwise **confirmed** if σ_int ≤ 0.92 Gyr, **not confirmed** if not.
- **Error scale, two directions (reported):** (i) the late phase (eq. 1), in 0.1 dex [Fe/H] bins
  from −0.5 to 0.3: the ratio of the observed age standard deviation to the rms e_Age is an upper
  bound on an error scale factor f (true ages also spread); (ii) from sample A, f ≤ √(1 + σ_sel²/⟨e²⟩)
  bounds the factor by which errors could be underestimated. Sample A is refitted with e_Age × f at
  the two bounds.

### 2.4 R7, R5, R6 (no verdict)

- **R7:** samples: sample A; [α/Fe] > 0.10 and [α/Fe] > 0.18 with JPHI > 500 (Miglio et al. 2021 used
  [α/Fe] > 0.1 on the APOGEE scale; the LAMOST scale may differ by about 0.1 dex); each without a
  [Fe/H] cut and with [Fe/H] < −0.2. Latent age distribution: Gaussian mixture, K = 1–4 by BIC, in M0.
  Reported: the central 95% width of the latent distribution and the largest latent fraction in any
  1.5 Gyr window (sliding on the 0.05 Gyr grid), at error scale 1 and at the two bounds of 2.3.
  Compared with Miglio et al.: 95% born within 1.52 (+0.54/−0.46) Gyr (their deconvolved
  distribution), as a qualified comparison across tracers.
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
of 2.0 and runs R1, R2, R3/R4, R7, R5, R6 with the M0 likelihood on the latent grid. Per-star kernels
g_i on the grid and the selection terms P_i are precomputed as matrices (stars × grid), so each
likelihood evaluation is a matrix–vector product. Mock samples for R1 and the R3/R4 recovery check
use their own generator, independent of the likelihood code. All tunable numbers (cuts, bins,
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
