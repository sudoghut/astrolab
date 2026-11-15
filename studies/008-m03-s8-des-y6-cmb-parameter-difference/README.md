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

Only R1 and R2 carry verdicts. All rules below are fixed before any chain is downloaded.

### 2.0 Step A: reading the chains (no statistics)

The chain formats are not documented beyond D26's `read_chains_y6.py`, which reads only the
Nautilus 3x2pt chain (Ωm in column 0, σ8 in column −7, log-weight in column −3) and a flow chain
(Ωm in column 0, σ8 in column 1, unit weights); it does not cover the CMB chain. The run therefore
has two steps. **Step A** downloads the chains and records, for each, only its format: the comment
lines (with any `#sampler=` and `##` prior-range lines), the number of columns, the header line, the
column map found by the rules below, and the row counts. It computes no statistic of any parameter.
If the rules below cannot map a chain, a dated amendment to the column mapping only (nothing else)
may be written after step A and before step B; this is the only allowed post-download change. Such
an amendment may use column names and metadata, external documentation, the column count and the
values of the first ten rows (to recognise, for example, a weight or a log-likelihood column), but
no mean, quantile or other summary of the parameters to be tested. The R1 mean test is then the
check of the mapping; a failed R1 does not allow a second remapping.
**Step B** computes everything else.

**Column rules.**
- The header is the first line that starts with a single `#` (not `##`) whose number of
  whitespace-separated fields (after the `#`) equals the number of fields in each data row.
- Names are matched case-insensitively on the part after the last `--`. Ωm: `omega_m` or `omegam`;
  σ8: `sigma_8` or `sigma8`; a stored S8: `s_8` or `s8`. Exactly one column must match each; zero
  or several matches make the chain "not mapped".
- Weights, in order of priority: `weight` (in Cobaya this is the multiplicity), then `log_weight`
  (exponentiated after subtracting its maximum); never `old_weight`. No weight column: unit weights.
- A header that lacks a needed name makes the chain "not mapped"; there is no positional fallback
  for a chain with a header. Without any header line, the three Nautilus chains (`32pt_…`,
  `12pt_…`, `shear_nla_…`) use the layout of `read_chains_y6.py`; any other chain is "not mapped".
  `read_chains_y6.py` documents this layout only for the 32pt chain; for the two ξ± chains (other
  nuisance parameters) the R1 mean test is the safeguard against a wrong column.
- Burn-in: if the `#sampler=` line names a nested sampler (nautilus, multinest, polychord) or an
  importance or flow sampler, no burn-in; if it names an MCMC sampler (metropolis, emcee, mcmc), the
  first 30% of rows are dropped; if there is no sampler line, no burn-in and this is recorded.
- Rows with a non-finite value in a used column, or zero weight, are dropped; the counts of rows with
  a non-finite value in any column and in the used columns are both reported.
- A stored S8 must agree with σ8 (Ωm/0.3)^0.5 to 1e-4 in every row, else the chain is flagged and
  the derived value is used. The effective sample size (Σw)²/Σw² is reported; below 2,000 it is
  flagged.
- A "not mapped" chain that is not fixed by the step-A amendment makes every item using it "not
  evaluable".

**Step-A amendment (2026-11-15, after step A and before step B; column mapping only).** Step A
found all three chains to be CosmoSIS Nautilus output with headers; Ωm, σ8, the stored S8 and the
log-weight were mapped by the rules above without change. Two naming facts seen only in the headers
complete the mapping: (1) the amplitude parameter is named `cosmological_parameters--a_s_1e9`
(A_s × 10⁹), which is added to the amplitude names of section 2.2; (2) CosmoSIS writes derived
parameters with an upper-case section name (for example `COSMOLOGICAL_PARAMETERS--SIGMA_12`), so
such columns count as derived in section 2.4. No statistic of any chain was computed before this
amendment.

### 2.1 R1 (verdict per chain)

Weighted mean of S8, and the 68% interval around it: the shortest interval containing the mean and
68% of the weight, found on a weighted kernel density estimate (KDE) of S8 (verdict definition);
the interval with 34% of the weight on each side of the mean is reported alongside, without verdict.
- "Reproduced" for a chain if |mean − published| ≤ 0.002 (the published means are rounded to
  0.001) **and** each interval end is within 0.003 of the published one. Published: CMB 0.836
  (+0.012/−0.013), DES 3x2pt 0.789 (+0.012/−0.012), DES ξ± 0.783 (+0.019/−0.015).
- Gates use the means only (the mean identifies the chain; the interval ends test the interval
  definition): R2 is evaluated as a reproduction only if the CMB and 3x2pt means pass; R3 uses the
  `12pt_…` chain if its mean passes, otherwise `shear_nla_…` if its mean passes (the NLA chain is
  downloaded only then), otherwise R3 is not computed.
- The weighted mean of Ωm in the 3x2pt chain is reported against 0.333, without verdict.

### 2.2 R2 (verdict for 1-D and 2-D separately)

The parameter-difference n_σ from the original chains (no truncation, no re-weighting), with the
estimator of section 4. Let s be the standard deviation of n_σ over the five seeds.
- "Reproduced" if |n_σ − published| ≤ 0.15 + 2s (published: 2.6 in S8, 2.2 in S8–Ωm; the 0.15
  allowance covers D26's unquoted normalizing-flow noise and the rounding to 0.1). Otherwise "not
  reproduced".
- "Not evaluable" if the R1 gate fails, or if s > 0.03. No rerun with other settings.
- **Prior support.** The test uses prior ranges, not where the samples fell. For each sampled
  cosmological parameter that both chains share (Ωm and the amplitude parameter, A_s or
  ln(10¹⁰A_s), when present under the same name), the prior range is taken from the chain's `##`
  lines (CosmoSIS `values.ini`) if present. If more than 1% of the DES weight lies outside the CMB
  prior range, or vice versa, R2 is "not evaluable" and the result is reported as descriptive. If no
  prior ranges are available in either header, the test is recorded as "not performed" and R2
  stays evaluable. σ8 and S8 are derived and have no prior range. As a sensitivity (no verdict), the
  1-D and 2-D n_σ are also reported after truncating both chains to the overlap of their sampled
  ranges in Ωm, with the fraction of weight dropped.
- Bandwidth variants (×0.5, ×2) and the 1-D convolution cross-check are reported; a change of more
  than 0.1σ is flagged as bandwidth-dependent and does not change the verdict.
- **Estimator calibration (done 2026-11-15, before any download, on synthetic data only).** For a
  Gaussian P(Δp) with true n_σ = 2.6 (1-D) and 2.2 (2-D), the estimator of section 4 (N = 4,000,000,
  binned, Scott bandwidth) gave, over five seeds: 1-D mean 2.5999, s = 0.0036 (bandwidth ×0.5:
  s = 0.0045; ×2: s = 0.0032); 2-D mean 2.2023, s = 0.0066 (×0.5: s = 0.0203; ×2: s = 0.0043); all
  biases below 0.008 in absolute value. Before step A, the committed `s8diff.nsigma_binned` must
  reproduce these numbers with the same seeds (each mean within 0.005, each s within a factor of
  1.5 of the value above); the rerun is logged in `log.md`. The earlier unbinned design (scipy `gaussian_kde` on a
  20,000-point fit subset, N = 400,000) gave s = 0.053 in 2-D and was replaced for that reason. The
  calibration script is `explore/estimator_calibration.py`; its test repeats a shorter version.
- Reported alongside, without verdict: the Gaussian estimate (difference of the means over the root
  sum of squared standard deviations), and the same with the weighted-KDE modes in place of the
  means.

### 2.3 R3 (descriptive)

n_σ between the ξ± chain selected by R1 and the CMB chain, 1-D and 2-D, same estimator. D26
quotes no such number; no verdict.

### 2.4 R4 (exploration, no verdict)

- **Projection effects:** shift every DES 3x2pt S8 sample by +0.17 × 0.012 = +0.00204 (D26 App. B
  Table 9: (truth − mean)/σ = +0.17, i.e. the simulated mean comes out low) and recompute the 1-D
  n_σ; expected: a smaller difference. A second variant replaces the DES mean by D26's published
  MAP (0.793): shift by +0.004. These are simulation-based or summary-based variants, not corrections.
- **Algorithm:** on the same 1-D S8 comparison, (a) iso-density (eq. 18); (b) equal-tail: p = the
  weighted probability that Δp lies on the far side of 0 from the weighted median of Δp,
  Δ_ET = 1 − 2p, n_σ = √2 erf⁻¹(Δ_ET); (c) the Gaussian estimate.
- **Threshold:** for each R2 number, the largest threshold that the number reaches (it reaches
  every threshold up to its own value), and whether that is below 3.
- **Full space (Gaussian):** over the cosmological parameters that both chains *sample*
  (identified from the `##` prior-range lines or the CosmoSIS `cosmological_parameters--` names that
  are not derived; derived columns such as σ8, S8, h0 when H0 is sampled, and any column whose
  correlation with another selected column exceeds 0.999, are excluded), the χ² = Δμᵀ (C_A + C_B)⁻¹ Δμ
  with k degrees of freedom, converted to n_σ via its probability and eq. 19. Reported twice: with
  all such parameters, and with the data-constrained ones (DES posterior variance below 0.25 of the
  variance of a uniform distribution over the DES prior range from the `##` lines). A parameter with
  a non-uniform (for example Gaussian) prior uses its prior variance in that cut instead, and is
  excluded from the second variant if that variance is not given. If the condition number of
  C_A + C_B exceeds 1e8, or the chains share no sampled parameter beyond Ωm, or no prior ranges are
  available for the second variant, the item records that and stops.

### 2.5 R5 (descriptive)

Each published S8 summary against the CMB chain, 1-D, iso-density estimator. A summary is modelled
as a split normal whose *mean* equals the published central value (the location is shifted by
−√(2/π)(σ₊ − σ₋) from the mode), with the published σ₊ and σ₋; N independent draws from it are paired
with N weighted draws from the CMB chain. Probes: KiDS-Legacy (mean 0.813 ± 0.018; the 0.76σ of its
paper is against Planck Legacy, not this CMB), HSC Y3 (Zhang et al. 2025, 0.780 +0.029/−0.030), ACT
DR6 + Planck lensing + BAO (0.831 ± 0.023), eROSITA eRASS1 (0.86 ± 0.01). Previous generation: DES
Y3 3x2pt (0.776 ± 0.017), KiDS-1000 3x2pt (0.766 +0.020/−0.014) and cosmic shear (0.759
+0.024/−0.021), HSC Y3 2023 (shear 0.769 +0.031/−0.034 and 0.776 +0.032/−0.033; 3x2pt 0.775
+0.043/−0.038). No average or joint χ²: the probes are correlated (shared footprints, the ACT
combination includes Planck lensing and BAO, eROSITA's mass calibration uses weak lensing) and S8
with exponent 0.5 is not each probe's best-constrained direction. These n_σ are a uniform
approximation and are not comparable with the significances in the probes' own papers.

## 3. Data (with size estimate)

| Input | Source (service / URL) | Selection | Est. rows / size |
|---|---|---|---|
| DES Y6 3x2pt chain `32pt_wolensbin2_lin_lcdm_DV0723_R0723.txt` | `https://desdr-server.ncsa.illinois.edu/despublic/y6a2_files/y6_key/chains_release/`, via `ctx.http` with `max_bytes = PARAMS["max_bytes_32pt"]` (150 MiB) | whole file (user-approved one-off exception, 2026-11-15) | 144,252,036 bytes; of order 10⁵ rows (about 1 kB per row of ~40 columns) |
| CMB chain `fiducial_cmb_tp_external_R1006.txt` | same, via `ctx.http` (default cap) | whole file | 11,782,940 bytes; of order 10⁴–10⁵ rows |
| DES ξ± chain `12pt_wolensbin2_lin_lcdm_DV0723_R0723.txt` | same | whole file | 14,875,711 bytes; of order 10⁴–10⁵ rows |
| fallback only: `shear_nla_wolensbin2_lcdm_DV0723_R0723.txt` | same | only if the R1 mean test fails for `12pt_…` | 10,029,183 bytes |
| Published S8 summaries | papers (R5) | in `PARAMS` | – |

Total 170,910,687 bytes (163.0 MiB), or 180,939,870 bytes (172.6 MiB) with the fallback, under the
200 MiB study budget (charged also for cached reads). The 50 MB per-download cap is exceeded only for
the 3x2pt chain, by the user's explicit one-off consent (2026-11-15, recorded in `log.md`); the cap
for that call is `PARAMS["max_bytes_32pt"]` = 150 MiB, passed for that exact URL only. The files are
cached outside Dropbox and parsed in memory; only summaries go into `results/`. Not fetched: the
2x2pt chain (128 MB), the nonlinear-bias and wCDM chains (257 MB to 4.5 GB), the fixed-neutrino-mass
chain (76 MB), any KiDS, ACT, SPT or eROSITA product.

## 4. Method

1. **Step A** (section 2.0): fetch the chains, record formats and column maps, save
   `results/formats.json`. No statistic.
2. **Step B**, R1: weighted means; a weighted Gaussian KDE of S8 on a grid of 2,000 points between
   the weighted 0.01% and 99.99% quantiles (Scott's rule with the effective sample size); the
   shortest interval containing the mean and 68% of the KDE mass, and the equal-34% interval.
   Endpoints are grid points: each candidate lower end is a grid point at or below the mean, and its
   upper end is the first grid point at which the cumulative KDE mass (trapezoidal) reaches the lower
   end's value plus 0.68; the grid spacing (range/2,000) is far below the 0.003 tolerance.
3. **R2 estimator** (D26 eqs. 17–19), for p = S8 (1-D) and p = (S8, Ωm) (2-D):
   - draw N = 4,000,000 indices from each chain independently, with probability proportional to the
     weights, with replacement; Δp_i = p_DES,i − p_CMB,i are equally weighted samples of P(Δp)
     (eq. 17);
   - whiten: z = (Δp − mean) L with L the Cholesky factor of the inverse sample covariance of Δp
     (in 1-D, division by the standard deviation); the point Δp = 0 maps to z₀;
   - binned Gaussian kernel density estimate: histogram of z on a regular grid (8,000 cells in 1-D,
     1,024 × 1,024 in 2-D) spanning, on each axis, the sample quantiles 10⁻⁶ and 1 − 10⁻⁶ extended to
     include z₀, with a margin of five bandwidths; samples outside the grid count as below the
     threshold and their number is reported; the ratio of cell size to h is recorded and the run is
     flagged if it exceeds 1/3; smoothed with
     a Gaussian filter of width h = N^(−1/(d+4)) (Scott's rule in whitened units, d = dimension);
     the density at z₀ by linear interpolation of the smoothed grid;
   - Δ = fraction of the N samples lying in cells whose smoothed density is strictly above the
     density at z₀ (eq. 18 with the binned estimate in place of the normalizing flow); n_σ =
     √2 erf⁻¹(Δ) (eq. 19); if Δ = 1 exactly, n_σ is reported as a lower bound with Δ = 1 − 1/N;
   - five seeds (0–4); mean n_σ and its standard deviation s; repeated with h × 0.5 and h × 2;
   - 1-D cross-check: P(Δp) by numerical convolution of the two weighted Gaussian KDEs of S8 (Scott's
     rule with each chain's effective sample size) on a common grid of spacing 10⁻⁴ covering the
     union of the two chains' weighted 0.01%–99.99% S8 ranges and their difference; Δ = mass of the
     grid points with density above the density at 0.
4. R3, R4 and R5 as in section 2.
5. Summaries only (means, intervals, n_σ per seed and variant, effective sample sizes, row counts,
   column maps) go to `results/*.json`, each under 1 MB.

Systematics we cannot test here: DES's own systematics and blinding, the choice of CMB likelihoods,
the accuracy of D26's normalizing flows (only bounded through the tolerance), and the
interpretation step `gap_conv` (wiki 2.3).

## 5. Results

Run 2026-11-15 (`python -m astrolab run 008`, 71 s from cache). Step A downloaded 170,910,687 bytes
in three guarded fetches; all three chains are CosmoSIS Nautilus output with headers (3x2pt: 64
columns, 115,920 rows; CMB: 18, 36,000; ξ±: 39, 19,456) and were mapped by name; one dated
column-mapping amendment (section 2.0). Page: [`web/index.html`](web/index.html). Numbers are from
`results/*.json`.

**R1 (verdict per chain): all three reproduced.**

| Chain | weighted mean S8 (published) | shortest 68% interval around the mean (published) | ESS | verdict |
|---|---|---|---|---|
| CMB | 0.8357 (0.836) | [0.8229, 0.8481] ([0.823, 0.848]) | 10,401 | reproduced |
| DES Y6 3x2pt | 0.7893 (0.789) | [0.7777, 0.8019] ([0.777, 0.801]) | 10,472 | reproduced |
| DES Y6 ξ± | 0.7834 (0.783) | [0.7671, 0.8010] ([0.768, 0.802]) | 10,061 | reproduced |

The stored S8 columns agree with σ8 (Ωm/0.3)^0.5 to 1e-4 in every row. The 3x2pt mean Ωm is
0.3328 (published 0.333). Rows dropped: zero weight (CMB 8,309; 3x2pt 13,263; ξ± 403) and non-finite
values in the used columns (677; 226; 41), as is usual for Nautilus output. The ξ± chain passed, so the NLA
fallback was not downloaded.

**R2 (verdict): both reproduced.**

| Projection | n_σ (5 seeds) | s | bandwidth ×0.5 / ×2 | D26 | tolerance 0.15 + 2s | verdict |
|---|---|---|---|---|---|---|
| S8 (1-D) | 2.674 | 0.0023 | 2.675 / 2.673 | 2.6 | 0.155 | reproduced |
| S8–Ωm (2-D) | 2.178 | 0.0112 | 2.191 / 2.172 | 2.2 | 0.172 | reproduced |

- Prior support (Ωm and A_s, from the `##` ranges): no weight of either chain lies outside the other
  chain's prior range; the test was performed and passed.
- Cross-checks (no verdict): 1-D numerical convolution 2.642; Gaussian estimate with means 2.677,
  with KDE modes 2.652; truncation to the common sampled Ωm range drops no weight
  (1-D 2.676, 2-D 2.191). No bandwidth dependence and no grid flag.
- The 1-D value lies 0.07σ above D26's 2.6, within the allowance for D26's unquoted flow noise and
  rounding.

**R3 (descriptive).** DES ξ± against the CMB: 2.53σ in S8 and 2.18σ in S8–Ωm (s = 0.004, 0.005).

**R4 (exploration, no verdict).**
- Projection effects: shifting DES S8 up by +0.00204 (Table 9) gives 2.55σ; using D26's MAP
  (+0.004) gives 2.44σ. Both directions lower the difference, as expected.
- Algorithms on the same 1-D comparison: iso-density 2.674, equal-tail 2.670, Gaussian 2.677. The 1-D
  posteriors are close to Gaussian, so the choice of algorithm does not matter here.
- Threshold: both R2 numbers are below 3; the 1-D number would be at or above a threshold of 2.67
  or lower (a threshold of 2.5 would classify it as a difference; the MAP variant would sit at 2.44).
- Full space (Gaussian approximation, not a reproduction): over the six sampled parameters both
  chains share (A_s, h, Σmν, n_s, Ωb, Ωm), χ² = 6.45 for k = 6, n_σ = 0.89; over the two
  data-constrained ones (A_s, Ωm), n_σ = 0.32. Both are far below D26's 1.8σ, and below our own
  2.18σ in the S8–Ωm plane. The reason is the shape of the posterior: S8 is a nonlinear combination
  of A_s and Ωm, so in the sampled parameters the DES posterior is curved, and a Gaussian
  approximation of it smears out the difference that is sharp in S8. This is why D26 needs
  normalizing flows for the full space; the Gaussian number is not a test of D26's 1.8σ.

**R5 (descriptive).** Published S8 summaries against the same CMB chain (split normals with the
published means; not comparable with each paper's own significance):

| Probe | S8 | n_σ vs CMB |
|---|---|---|
| ACT DR6 + Planck lensing + BAO | 0.831 ± 0.023 | 0.18 |
| KiDS-Legacy | 0.813 ± 0.018 | 1.04 |
| HSC Y3 3x2pt (Sugiyama+ 2023) | 0.775 (+0.043/−0.038) | 1.44 |
| eROSITA eRASS1 | 0.86 ± 0.01 | 1.51 |
| HSC Y3 shear (Dalal+ 2023) | 0.776 (+0.032/−0.033) | 1.71 |
| HSC Y3 (Zhang+ 2025) | 0.780 (+0.029/−0.030) | 1.74 |
| HSC Y3 shear (Li+ 2023) | 0.769 (+0.031/−0.034) | 1.93 |
| DES Y3 3x2pt | 0.776 ± 0.017 | 2.83 |
| KiDS-1000 cosmic shear | 0.759 (+0.024/−0.021) | 2.92 |
| KiDS-1000 3x2pt | 0.766 (+0.020/−0.014) | 3.14 |

The previous generation (DES Y3, KiDS-1000) sits at 2.8–3.1σ from this CMB; the current results
of other probes at 0.2–1.9σ; DES Y6 3x2pt itself at 2.67σ in S8 (R2). eROSITA lies above the CMB,
the lensing probes below it.

**Reading.** The public chains reproduce D26's inputs and its 1-D and 2-D differences: the numbers
behind the conclusion are right. Whether 2.6–2.7σ is "no substantial evidence" is the interpretation
step `gap_conv` of the wiki's Lean analysis (a 3σ-as-evidence usage, not stated by D26); the numbers
show how close it is to that line (2.67σ, and 2.44–2.55σ under D26's own projection-effect estimates).
For DES the "easing" is relative: the earlier DES Y3 result was 2.83σ from this CMB, the Y6 3x2pt
result 2.67σ, while other current probes have moved closer to the CMB.

## 6. Referee notes

Independent critique: selection effects, systematics, alternative explanations.

## 7. Open questions

## 8. Exploring via chat

How a coding agent answers "what if" questions about this study without touching `results/`
(rules: AGENTS.md section 2).

| Knob (`PARAMS`) | Meaning | Safe range | Cache only, or new data (size)? |
|---|---|---|---|
| `n_pairs` | resampled pairs per estimate | 1e6–1e7 | cache only |
| `seeds` | seeds of the estimator | any list of ≥ 2 integers | cache only |
| `bw_variants` | bandwidth factors reported beside the base | 0.25–4 | cache only |
| `proj_shift`, `map_shift` | shifts of DES S8 in R4 | ±0.01 | cache only |
| `published_nsigma`, `tol_nsigma` | R2 targets and allowance (changing them is not the registered verdict) | – | cache only |
| `probes` | R5 summaries: name -> [mean, σ₊, σ₋, reference] | any published S8 | cache only |
| `chains` | chain file names on the DES server | other files in `chains_release/` | new data: check sizes first (50 MB cap; only the 32pt chain has the user-approved exception) |

- Rerun with an override: `python -m astrolab explore 008-m03-s8-des-y6-cmb-parameter-difference --tag <topic> --set KEY=VALUE`
  (outputs in `explore/<date>-<topic>/`, not committed; about 70 s from cache).
- Analyses `run.py` does not cover: a script `explore/<name>.py` with `def main(ctx)`, run with
  `python -m astrolab explore 008-m03-s8-des-y6-cmb-parameter-difference --tag <topic> --script explore/<name>.py`.
  Existing: `explore/estimator_calibration.py` (the synthetic calibration of the estimator).
- Results files and keys: `results/formats.json` (step A: headers, column maps, row counts);
  `results/r1.json` (per chain: `mean`, `lo`, `hi`, `equal_lo`, `equal_hi`, `kde_mode`, `verdict`,
  `chain` diagnostics); `results/r2.json` (`1d`, `2d`: `n_sigma`, `s`, `per_seed`,
  `bandwidth_variants`, `verdict`; `support`; `gaussian_means`; `gaussian_modes`;
  `truncated_sensitivity`); `results/r3.json`; `results/r4.json` (`projection_shift`, `map_shift`,
  `algorithms_1d`, `threshold`, `full_space`); `results/r5.json` (per probe `n_sigma`).
- Example questions: "what if the CMB were shifted by 1σ?" -> a script that shifts the CMB samples;
  "how does KiDS-Legacy's 0.815 mode (not the mean) compare?" -> `--set` on `probes`.
- Findings that change what we know go into `log.md` (and, for a paper study, the wiki article)
  on a branch.

