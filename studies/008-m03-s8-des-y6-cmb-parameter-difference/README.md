# M3 S8 tension: DES Y6 3x2pt vs CMB parameter difference and multi-probe summary

> 中文：[README.zh.md](README.zh.md)

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
6. **R6 (added 2026-11-16, section 2.6).** Does a normalizing-flow estimate over the six sampled
   ΛCDM parameters reproduce D26's full-space 1.8σ?

## 2. Hypotheses and decision criteria

Only R1 and R2 (and, added later, R6) carry verdicts. All rules below are fixed before any chain is downloaded. (Exception, dated: R6 in section 2.6 was added on 2026-11-16, after the download
and after R1–R5 were known, and is disclosed there.)

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

**Step-A amendment (2026-11-15, after step A and before step B; column mapping only).** *Procedural note (referee,
2026-11-15): section 2.0 allows an amendment only when a chain cannot be mapped; all three chains
were mapped, so this amendment, which names columns for sections 2.2 and 2.4, is outside that
scope. It was made from column names only, before any statistic, and touches no verdict; without
change (2) the R4 full-space Gaussian would have been about 1.26σ instead of 0.89σ (computed
without the correlation cut; section 6).* Step A
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

### 2.6 Addendum 2026-11-16: R6-FLOW, the full-space difference with normalizing flows (T-027, plan 024)

Written before any normalizing flow was trained on the chains; only the tensiometer source code and
synthetic data (below) were used. It adds one verdict, R6, and changes nothing above. Revised the
same day after the gate-1 review, still before any flow was trained on the chains.

**What D26 states and what it does not** (arXiv:2601.14559v2, read 2026-11-16): the full-space
number is 1.8σ for 3x2pt against the CMB (Table 6, PTE 0.08), computed with eqs. 17–19 where the
density P̂ of the parameter difference is "given by the normalizing flow model", "executed by the
tensiometer code"; the ΛCDM model has the six free parameters As, Ωm, h, Ωb, ns and Σmν, with As (not
ln As or S8) the sampled amplitude (Sec. IV.1, Table 3). D26 does not state which parameters enter
the full-space difference, the flow settings, the number of flows, or an uncertainty on 1.8σ. The
parameter set below is therefore our reconstruction.

**Known when this was written.** The iso-density Δ is not invariant under a nonlinear change of
coordinates, and the Gaussian full-space numbers of R4 and section 6 already show it: 0.89σ for the
six parameters with As, 1.48σ with S8 in place of As, 1.26–1.36σ for other sets, 0.32σ for (As, Ωm),
2.21σ for (S8, Ωm). The verdict uses As because D26 samples As; the S8 variant is reported beside it.

**Parameters.** The six parameters of the R4 full-space item ("all" variant), as mapped from the
chain headers: `cosmological_parameters--a_s_1e9`, `--h0`, `--mnu`, `--n_s`, `--omega_b`,
`--omega_m`. Same chains, rows, weights and burn-in as R2 (the DES 3x2pt and CMB chains; the R1 gate
applies).

**Prior support.** The R2 rule is applied to all six parameters: for each, the weight of each chain
outside the other chain's prior range (from the `##` lines) is computed; if it exceeds 1% for any
parameter, R6 is reported as descriptive (no verdict). Each direction is checked only where the
other chain's header gives a range; a direction without one is listed as not checked and does not
withhold the verdict (as in R2), and a parameter with no range in either header is listed as not
checkable. "Prior support fails" means that at least one checked fraction exceeds 1%; partial or
wholly unchecked support permits a verdict, as R2's "not performed" does.

**Estimator** (tensiometer 1.1.0 in the separate environment of T-027: TensorFlow 2.21 with the
legacy Keras 2 API, `TF_USE_LEGACY_KERAS=1`, which tensiometer's flows need; under Keras 3 the flow has
no trainable weights). For repetition k (seed k):
1. Seed numpy and TensorFlow with `tf.keras.utils.set_random_seed(k)` and
   `tf.config.experimental.enable_op_determinism()`.
2. Draw N = 100,000 indices from each chain independently, with probability proportional to the
   weights, with replacement (numpy `default_rng(k)`); Δθ = θ_DES − θ_CMB are equally weighted samples
   of P(Δθ), as in R2. tensiometer's `parameter_diff_chain` is not used: it pairs rows in a fixed
   cyclic order without random numbers.
3. A getdist `MCSamples(samples=Δθ, names=<the six names>, ignore_rows=0)` (default sampler, unit
   weights, no ranges given).
4. `flow_from_chain(chain, feedback=0, plot_every=0)`, all other settings tensiometer's defaults:
   an affine masked autoregressive flow, `pop_size=10` trainings of `epochs=100` each with its
   default early-stopping schedule, the best kept by validation loss (`validation_split=0.1`); the
   default settings are written into the results.
5. `estimate_shift(flow, tol=0.02, max_iter=1000, step=100000)` returns Δ and its Clopper–Pearson
   68% interval (low, up); n_σ = √2 erf⁻¹(Δ) (eq. 19). The estimate has converged if
   σ(up) − σ(low) ≤ 0.02, computed from the returned interval.
Five repetitions, seeds 0–4. n̄ = mean of the five n_σ, s = their sample standard deviation (ddof = 1).

**Known-answer gate (synthetic, run before the chains).** The calibration step of `flowshift.py`
(the study's TF-side module, run by `run.py` before any flow on the chains) uses a 6-D synthetic
difference distribution with the structures expected here, with an analytic density:
- a curved pair, like the As–Ωm ridge: x₁ ~ N(2.0, 1), x₂ = z + 0.3 (x₁ − 2.0)² with z ~ N(1.0, 1)
  (unit Jacobian, so p(x₁, x₂) = N(x₁; 2.0, 1) N(x₂ − 0.3 (x₁ − 2.0)²; 1.0, 1)); the curvature 0.3 is
  set qualitatively, not from the chains; N(m, 1) denotes a normal with mean m and standard deviation 1;
- three flat-topped box directions with 0 inside the plateau (a uniform variable on [−0.6, 1.4] minus an
  independent normal variable of width 0.05), like h, ns and Ωb;
- one box direction with 0 about one edge width inside its lower edge (a uniform variable on [−0.1, 1.9]
  minus an independent normal variable of width 0.1), like Σmν against the CMB's lower bound at 0.06 eV.
Its reference n_σ is computed by Monte Carlo from the analytic density with 2,000,000 draws
(`default_rng(999)`; sampling error about 0.001σ, negligible against the tolerances): 2,000,000
points z_i are drawn from the synthetic distribution itself, the analytic log-density log p is
evaluated exactly at each z_i and at 0 (no density estimate), Δ_ref = the fraction of z_i with
log p(z_i) > log p(0), and n_σ = √2 erf⁻¹(Δ_ref); it was not computed before this was written. "Exact value" below means this reference. The estimator above (steps 1, 3–5; the synthetic samples are
drawn fresh for each seed with `default_rng(1000 + k)`, N = 100,000) is run for seeds 10, 11, 12,
none of which was used during the design. The gate passes if the mean flow n_σ is within 0.10 of the
exact value and each of the three within 0.20; a gate repetition that fails, has not converged or is a
lower bound fails the gate (dated clarification 2026-11-16, from the stage-2 code review, before any
run). A repetition whose interval end is undefined (for example the flow density at 0 undefined) has
not converged. If it fails, R6 is "not evaluable" and no flow is
trained on the chains. The gate tests the flow's accuracy on these structures, not the 1.8 level: its
exact n_σ need not be near 1.8. Seen during the design (all with seed 0, on simpler synthetic cases, before
any flow on the chains): a single 100-epoch flow gave 0.03σ against an exact 0.003σ (a cusped,
nearly zero-shift case), 0.93σ against 0.61σ (cusped boxes with a Gaussian pair), the same with 300
epochs on 200,000 points, 1.38σ against 1.64σ (flat-topped boxes, one flow), and the default ten
trainings 1.618σ against 1.640σ on that last case; this is why the defaults are used and why the
gate exists.

**Verdict (R6).** The conditions are applied in this order; the first that applies decides:
(1) the R1 gate fails → "not evaluable"; (2) the known-answer gate fails → "not evaluable";
(3) a repetition fails, gives a non-finite n_σ or has not converged → "not evaluable"; (4) prior
support fails → "descriptive"; (5) the lower-bound rule below; (6) s > 0.07 → "not evaluable";
(7) the band rule.
- "Reproduced" if |n̄ − 1.8| ≤ 0.15 + 2s (the 0.15 allowance as in R2: D26's unquoted flow noise and
  the rounding to 0.1); otherwise "not reproduced".
- "Not evaluable" if the known-answer gate fails, if s > 0.07, if any repetition fails or returns a
  non-finite n_σ, if any estimate has not converged, or if the R1 gate fails. No rerun with other
  settings.
- If an estimate returns Δ = 1 (no flow sample below the density at 0), n_σ is recorded as a lower
  bound from the interval's lower end and counts as converged. If any repetition is a lower bound,
  n̄ and s are not used: R6 is "not reproduced" if the smallest lower bound exceeds
  1.8 + 0.15 + 0.10 = 2.05, otherwise "not evaluable".
- s ≤ 0.07 allows for the resampling noise of five repetitions; if the true spread were 0.05, s would
  exceed 0.07 by chance with probability about 0.10 (χ² with 4 degrees of freedom), an accepted risk
  of "not evaluable".

**Reported, not decisive** (same estimator, seeds 0–2, so that the run stays within a few hours):
the six-parameter flow with S8 in place of As; the two data-constrained parameters of R4 (As, Ωm), next to the binned-KDE n_σ of the same pair
computed in the same run with the R2 estimator (the only on-chain check of the curved directions);
the 1-D S8 and 2-D (S8, Ωm) flows next to this study's binned-KDE values (`r2.json` `1d.n_sigma`
2.6735 and `2d.n_sigma` 2.1777); each repetition's Δ, interval and training time; the R4 Gaussian
values beside the flow values. Like R2, R6 uses the chains as they are: no prior flow, no truncation.

**Data and environment.** No new download: the two chains are read from the cache through `ctx.http`
(the existing run, with the ξ± chain, is charged 163.0 MiB of the 200 MiB budget). The six columns,
S8 and the weights are passed to the TF environment as one temporary file in the cache staging area
(about 9 MB), written and deleted inside `try/finally`, never a cache entry; the interpreter is
resolved from `%LOCALAPPDATA%` at run time and only its availability and package versions are
saved. Expected run time about 3–4 hours (each training about 10 minutes).

**Amendment 2026-11-18 (user decision, before any secondary result was seen): iteration cap for
the reported cases.** The formal run of 2026-11-17 finished the known-answer gate (seeds 10–12), the
main case (seeds 0–4) and the S8-for-As case (seeds 0–2), then spent 20 hours on the first
constrained repetition without finishing: with `max_iter = 1000` and `step = 100000`, the estimator
may draw up to 10⁸ samples when the tension is large, and eight more reported repetitions were
queued. The user chose to stop the run and cap the reported cases. For the constrained, 1-D and 2-D
cases only, `estimate_shift` uses `max_iter = 100` (same `tol` and `step`); a repetition that does
not reach the tolerance within the cap is reported as not converged, as before. The gate, the main
case (which alone decides R6) and the S8-for-As case keep `max_iter = 1000`. Nothing of the stopped
run was opened: no job result file, no log line with a Δ or n_σ, was read. The whole R6 is rerun
from scratch (the job cache is keyed by the configuration, so earlier job files are not reused);
with fixed seeds the gate and main results are expected to be identical.

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

*Uncertainty (post hoc, referee):* s is the spread over resampling seeds only. A bootstrap over chain
rows (20 replicates) gives 2.679 ± 0.030 (1-D) and 2.189 ± 0.034 (2-D); with these the verdicts are
unchanged (|2.68 − 2.6| = 0.08 < 0.15 + 2 × 0.03).

- Prior support (Ωm and A_s, from the `##` ranges): no weight of either chain lies outside the other
  chain's prior range; the test was performed and passed.
- Cross-checks (no verdict): 1-D numerical convolution 2.642 (biased low by about 0.03: the KDE
  bandwidth of each chain broadens P(Δp); not independent support for 2.6); Gaussian estimate with means 2.677,
  with KDE modes 2.652; truncation to the common sampled Ωm range drops no weight
  (1-D 2.676, 2-D 2.191). No bandwidth dependence and no grid flag.
- The 1-D value lies 0.07σ above D26's 2.6 (outside its rounding band [2.55, 2.65), within the
  registered allowance); this is about one bootstrap standard deviation (0.03). The three estimators
  share the same chains and draws, so their agreement does not locate the difference.

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
  2.18σ in the S8–Ωm plane. The Gaussian number depends on the parametrization (post hoc,
  `explore/referee_checks.py`): (S8, Ωm) 2.21σ, (A_s, Ωm) 0.32σ; six parameters with S8 in place of
  A_s 1.48σ, six plus S8 1.36σ, six plus σ12 1.26σ. S8 is a nonlinear combination of A_s and Ωm, so
  the DES posterior is curved in the sampled parameters, and h, n_s, Σmν and Ωb are largely
  prior-dominated in DES; a Gaussian in those coordinates dilutes the difference. This is why D26
  needs normalizing flows; no Gaussian number here is a test of D26's 1.8σ.

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

If the central values are read as modes rather than means (KiDS-1000 and HSC 2023 may quote
modes; post hoc), KiDS-1000 3x2pt moves from 3.14σ to 2.93σ and KiDS-1000 shear from 2.92σ to
2.83σ; the others change by 0.1σ or less. Grouped as registered: the previous generation (DES Y3,
KiDS-1000, HSC Y3 2023) at 1.4–3.1σ from this CMB; the other current probes (KiDS-Legacy, HSC Y3
2025, ACT, eROSITA) at 0.2–1.7σ; DES Y6 3x2pt itself at 2.67σ in S8 (R2). Survey by survey, KiDS
moved a lot (2.9–3.1σ to 1.0σ), DES a little (2.83σ to 2.67σ), HSC hardly at all (1.4–1.9σ to
1.74σ). eROSITA lies above the CMB, the lensing probes below it.

**Reading.** The public chains reproduce D26's inputs and its 1-D and 2-D differences: the numbers
behind the conclusion are reproduced. Whether 2.6–2.7σ is "no substantial evidence" is the interpretation
step `gap_conv` of the wiki's Lean analysis (a 3σ-as-evidence usage, not stated by D26); the numbers
show how close it is to that line (2.67σ, and 2.44–2.55σ under D26's own projection-effect estimates).
For DES the "easing" is small: the earlier DES Y3 result was 2.83σ from this CMB, the Y6 3x2pt
result 2.67σ. Most of the easing in R5 comes from KiDS.

## 6. Referee notes

Independent referee, 2026-11-15 (subagent with the pre-registration, code and results only; it read
the cached chains with the study's own functions and downloaded nothing). Triage:

1. **R4 full-space Gaussian depends on the parametrization** (serious for interpretation, not a
   bug). *Accepted*; checked post hoc with `explore/referee_checks.py`: (S8, Ωm) 2.21σ, (A_s, Ωm)
   0.32σ, six with S8 for A_s 1.48σ. Section 5 now states that no Gaussian number tests D26's 1.8σ.
2. **The seed spread s is not the uncertainty of n_σ.** *Accepted*; a chain-row bootstrap gives
   ±0.030 (1-D) and ±0.034 (2-D), ten times s. The verdicts are unchanged; the s > 0.03 gate and the
   +2s term were close to vacuous, and the 0.15 allowance carried the tolerance. Quoted precision in
   section 5 and the wiki now uses the bootstrap.
3. **The 1-D result (2.674) lies above D26's rounding band; the convolution check is biased low.**
   *Accepted*; three estimators agree on about 2.67, so the 0.07σ is between the chains and D26's
   flow estimate; the convolution (2.64) is no longer cited as support.
4. **The step-A amendment went beyond its allowed scope.** *Accepted as a procedural point*;
   labelled in section 2.0. It used column names only, came before any statistic, and touches no
   verdict. Without the upper-case rule the full-space Gaussian would have been 1.26σ (σ12 included),
   which is item 1's parametrization dependence again.
5. **R5 mean-versus-mode convention.** *Accepted*; reading central values as modes moves KiDS-1000
   3x2pt from 3.14σ to 2.93σ and KiDS-1000 shear from 2.92σ to 2.83σ; the change is reported
   beside the registered numbers. ACT's combination shares Planck lensing with Planck primary data
   only weakly; noted.
6. **Choice of CMB combination** (a lensing-inclusive or PR4-based CMB has lower S8). *Accepted
   limitation*: the study inherits D26's CMB; R1 identifies the chain by its S8 mean only.
7. **Minor:** the Ωm truncation sensitivity is vacuous (identical priors); R5 shares seeds across
   probes; `h0` in `DERIVED` is re-admitted through the prior ranges (fragile but correct). *Accepted*;
   no change to results.
8. **Checked and fine** (by the referee): whitening, grid offsets, equal-tail side, split-normal
   construction, interval search, weighted covariances; non-finite and zero-weight rows all carry
   zero weight; ESS about 1.0 × 10⁴ per chain; cell/h 0.026 (1-D) and 0.127 (2-D).


## 7. Open questions

1. The full-space 1.8σ needs a non-Gaussian density estimate (normalizing flows, as D26); installing
   tensiometer and TensorFlow needs the user's consent.
2. How much does the S8 difference change with a lensing-inclusive or Planck-PR4-based CMB
   (D26 reports 1.0σ in full space against Planck 2018 alone)?
3. Do KiDS-1000 and HSC Y3 (2023) quote means or modes? R5 shows a 0.1–0.2σ dependence.

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
  Existing: `explore/estimator_calibration.py` (the synthetic calibration of the estimator);
  `explore/referee_checks.py` (post hoc: Gaussian by parametrization, chain-row bootstrap, R5 with modes).
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

