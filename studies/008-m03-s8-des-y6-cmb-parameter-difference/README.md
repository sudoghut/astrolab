# M3 S8 tension: DES Y6 3x2pt vs CMB parameter difference and multi-probe summary

> Write sections 1–4 BEFORE writing run.py (pre-registration). Edit them later only
> with a dated note explaining the change.

## 1. Question

Paper: DES Collaboration 2026, DES Y6 3x2pt cosmology, arXiv:2601.14559 v2 ("D26"). Wiki article
(source of this pre-registration, part 3):
[Study-008-des-y6-s8-cmb](https://github.com/sudoghut/astrolab/wiki/Study-008-des-y6-s8-cmb).
Plan: `design/017-plan_*`.

D26 compares its ΛCDM 3x2pt posterior with a primary-CMB posterior (Planck 2018 + ACT-DR6 +
SPT-3G DR1, TT/TE/EE, no CMB lensing) using the parameter-difference probability (Sec. IV.6,
eqs. 17–19). It reports 2.6σ in S8, 2.2σ in the S8–Ωm plane and 1.8σ in the full parameter space,
and concludes that there is "no substantial evidence for a discrepancy" (Sec. VIII). S8 ≡ σ8 (Ωm/0.3)^0.5.

1. **R1.** Do the public DES Y6 chains reproduce the published S8 means of the CMB (0.836
   +0.012/−0.013), DES 3x2pt (0.789 +0.012/−0.012) and DES cosmic shear ξ± (0.783 +0.019/−0.015)?
2. **R2.** Do the same chains reproduce the 2.6σ (S8) and 2.2σ (S8–Ωm) DES–CMB parameter
   differences?
3. **R3 (descriptive).** What is the parameter difference between DES cosmic shear and the CMB?
4. **R4 (exploration).** How sensitive are the R2 numbers to projection effects, to the algorithm
   (iso-density, equal-tail, Gaussian), and to the threshold of 3σ; what does a Gaussian
   approximation give in the full parameter space?
5. **R5 (descriptive).** Where do the published S8 summaries of other probes, and of the
   previous generation, sit relative to the same CMB chain?

## 2. Hypotheses and decision criteria

Only R1 and R2 carry verdicts. All tolerances below are fixed before any chain is downloaded.

**Columns and S8.** Each chain is read with its header if it has one (a comment line starting with
`#` and giving one name per column). Columns are found by name: Ωm by a name ending in `omega_m`,
σ8 by a name ending in `sigma_8` or `sigma8`, the weight by `weight` (linear) or `log_weight`
(exponentiated after subtracting its maximum). If a stored S8 column exists (name ending in `s_8`
or `s8`), it must agree with σ8 (Ωm/0.3)^0.5 to 1e-4 in every row, else the chain is flagged and the
derived value is used. Without a header, the three Nautilus chains (`32pt_…`, `12pt_…`,
`shear_nla_…`) use the layout of D26's `read_chains_y6.py` (Ωm in column 0, σ8 in column −7,
log-weight in column −3), and any other chain without a header is "not evaluable". Rows with
non-finite values or zero weight are dropped and counted. A chain whose effective sample size
(Σw)²/Σw² is below 2,000 is flagged in the results.

**R1 (verdict per chain).** Weighted mean of S8 and the 68% interval around it. The interval
follows D26's "68% credible level of posterior volume around the mean": the shortest interval
containing the mean and 68% of the weight, found on a weighted kernel density estimate (KDE) of
S8. "Reproduced" for a chain if |mean − published| ≤ 0.002 (the published means are rounded to
0.001) **and** each interval end is within 0.003 of the published one. The CMB and 3x2pt chains
must both be reproduced for R2 to be evaluated as a reproduction; the 1x2pt (`12pt_…`) chain must be
reproduced for R3 to use it, otherwise `shear_nla_…` is tried with the same test, and if neither
passes R3 is not computed. R1 also reports the weighted mean of Ωm against 0.333 (3x2pt) as a
check, without a verdict.

**R2 (verdict for 1-D and 2-D separately).** The parameter-difference n_σ is computed from the
original chains (no truncation, no re-weighting) with the estimator of section 4. Let s be the
standard deviation of n_σ over the five seeds. "Reproduced" if
|n_σ − published| ≤ 0.15 + 2s (published: 2.6 in S8, 2.2 in S8–Ωm; the 0.15 allowance covers D26's
unquoted normalizing-flow noise and the rounding to 0.1). "Not reproduced" otherwise. The verdict is
"not evaluable" if R1 fails for either chain, if s > 0.03 (non-convergence), or if the prior
supports of Ωm or σ8 in the two chains differ such that more than 1% of either chain's weight lies
outside the other chain's sampled range; in that case the number is reported as descriptive. The
bandwidth variants (×0.5 and ×2) and the 1-D convolution cross-check are reported; a change of more
than 0.1σ is flagged as bandwidth-dependent but does not change the verdict.

Reported alongside, without verdicts: the Gaussian estimate (mean difference over the root sum of
squared standard deviations), with means and with MAP-like modes.

**R3 (descriptive).** n_σ between the 1x2pt chain selected by R1 and the CMB chain, 1-D and
2-D, same estimator. D26 quotes no such number; no verdict.

**R4 (exploration, no verdict).**
- Projection effects: shift every DES 3x2pt S8 sample up by 0.17 × 0.012 = +0.00204 (D26 App. B
  Table 9: (truth − mean)/σ = +0.17, i.e. the simulated mean is low) and recompute the 1-D n_σ; the
  expected change is a smaller difference. This is a simulation-calibrated bias, not a correction.
- Algorithm: on the same 1-D S8 comparison, iso-density (eq. 18), equal-tail (two-sided probability
  that Δp lies on the far side of 0 from the median, converted with eq. 19) and the Gaussian
  estimate.
- Threshold: report, for each R2 number, the largest threshold below which it would be classified
  as at or above threshold.
- Full space: Gaussian parameter difference (Δμᵀ (C_A + C_B)⁻¹ Δμ, a χ² with k degrees of freedom,
  converted to n_σ with eq. 19) over the parameters both chains share by name; twice, with all
  shared parameters and with the data-constrained ones only (those whose DES posterior variance is
  below half of the variance of a uniform distribution over the DES chain's sampled range). If the
  chains share no parameter names beyond Ωm and σ8, this item reports that and stops.

**R5 (descriptive).** Each published S8 summary (split-normal with the published asymmetric
errors) against the CMB chain, 1-D, with the iso-density estimator and a weight per sample drawn
from the split normal. Probes: KiDS-Legacy (mean 0.813 ± 0.018; the 0.76σ of its paper is against
Planck Legacy, not this CMB), HSC Y3 (Zhang et al. 2025, 0.780 +0.029/−0.030), ACT DR6 + Planck
lensing + BAO (0.831 ± 0.023), eROSITA eRASS1 (0.86 ± 0.01); previous generation: DES Y3 3x2pt
(0.776 ± 0.017), KiDS-1000 3x2pt (0.766 +0.020/−0.014) and cosmic shear (0.759 +0.024/−0.021),
HSC Y3 2023 (shear 0.769 +0.031/−0.034 and 0.776 +0.032/−0.033; 3x2pt 0.775 +0.043/−0.038). No
average or joint χ²: the probes are correlated (shared footprints, the ACT combination includes
Planck lensing and BAO, eROSITA's mass calibration uses weak lensing) and S8 with exponent 0.5 is
not each probe's best-constrained direction. These n_σ are a uniform approximation and are not
comparable with the significances in the probes' own papers.

## 3. Data (with size estimate)

| Input | Source (service / URL) | Selection | Est. rows / size |
|---|---|---|---|
| DES Y6 3x2pt chain `32pt_wolensbin2_lin_lcdm_DV0723_R0723.txt` | `https://desdr-server.ncsa.illinois.edu/despublic/y6a2_files/y6_key/chains_release/`, via `ctx.http(max_bytes=150 MiB)` | whole file (user-approved one-off exception, 2026-11-15) | 144,252,036 bytes |
| CMB chain `fiducial_cmb_tp_external_R1006.txt` | same, via `ctx.http` | whole file | 11,782,940 bytes |
| DES 1x2pt (ξ±) chain `12pt_wolensbin2_lin_lcdm_DV0723_R0723.txt` | same | whole file | 14,875,711 bytes |
| fallback only: `shear_nla_wolensbin2_lcdm_DV0723_R0723.txt` | same | only if R1 fails for `12pt_…` | 10,029,183 bytes |
| Published S8 summaries | papers (section 2, R5) | in `PARAMS` | – |

Total 170.9 MB (163.0 MiB), or 180.9 MB (172.6 MiB) with the fallback, under the 200 MiB study
budget. The 50 MB per-download cap is exceeded only by the 3x2pt chain, by the user's explicit
one-off consent (2026-11-15, recorded in `log.md`); the cap passed for that call is 150 MiB and is
used for no other URL. The chain files are cached outside Dropbox and parsed in memory; only
summaries go into `results/`. Not fetched: the 2x2pt chain (128 MB), the nonlinear-bias and wCDM
chains (257 MB to 4.5 GB), the fixed-neutrino-mass chain (76 MB), any KiDS, ACT, SPT or eROSITA
product.

## 4. Method

1. Fetch the three chains (section 3), parse them (section 2, columns), derive S8, and drop and
   count bad rows.
2. **R1:** weighted means; the 68% interval around the mean from a weighted Gaussian KDE of S8 on a
   grid of 2,000 points spanning the sample range (Scott's rule bandwidth with the effective sample
   size), shortest interval containing the mean and 68% of the KDE mass.
3. **R2 estimator** (D26 eqs. 17–19), for p = S8 (1-D) and p = (S8, Ωm) (2-D):
   - draw N = 400,000 indices from each chain independently, with probability proportional to the
     weights, with replacement; Δp_i = p_A,i − p_B,i (A = DES, B = CMB): samples of P(Δp) (eq. 17);
   - split them into two halves; fit a Gaussian KDE (scipy `gaussian_kde`, Scott's rule; in 2-D
     the samples are whitened with their covariance first) on the first half; evaluate it on the
     second half and at Δp = 0; Δ = fraction of the second half with density above the density at 0
     (eq. 18);
   - n_σ = √2 erf⁻¹(Δ) (eq. 19); if Δ = 1 exactly (no evaluation sample below the zero density),
     report n_σ as a lower bound from Δ = 1 − 1/N_half;
   - five seeds (0–4): report the mean n_σ and its standard deviation s; repeat with the bandwidth
     multiplied by 0.5 and by 2;
   - 1-D cross-check: P(Δp) by numerical convolution of the two weighted KDEs on a common grid;
     Δ = mass of the grid points with density above the density at 0.
   For speed, the KDE is evaluated on at most 50,000 points of the second half; this subsample is
   part of the seeded procedure.
4. **R3:** the same estimator, 1x2pt chain against the CMB chain.
5. **R4 and R5:** as in section 2.
6. Save summaries only (means, intervals, n_σ per seed and variant, effective sample sizes, row
   counts, column map) to `results/*.json`, each under 1 MB.

Systematics we cannot test here: DES's own systematics and blinding, the choice of CMB likelihoods,
the accuracy of D26's normalizing flows (only bounded through the tolerance), and the
interpretation step `gap_conv` (wiki 2.3).

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

- Rerun with an override: `python -m astrolab explore 008-m03-s8-des-y6-cmb-parameter-difference --tag <topic> --set KEY=VALUE`
  (outputs in `explore/<date>-<topic>/`, not committed; about N s from cache).
- Analyses `run.py` does not cover: a script `explore/<name>.py` with `def main(ctx)`, run with
  `python -m astrolab explore 008-m03-s8-des-y6-cmb-parameter-difference --tag <topic> --script explore/<name>.py`.
- Results files and keys: TODO (`results/<file>.json`: key - meaning).
- Example questions: TODO (question -> knob or script an agent would use).
- Findings that change what we know go into `log.md` (and, for a paper study, the wiki article)
  on a branch.

