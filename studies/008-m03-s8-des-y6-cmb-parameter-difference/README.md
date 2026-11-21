# M3 S8 tension: DES Y6 3x2pt vs CMB parameter difference and multi-probe summary

> 中文：[README.zh.md](README.zh.md) · Web page online: [https://sudoghut.github.io/astrolab/studies//web/](https://sudoghut.github.io/astrolab/studies//web/)

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
4. `flow_from_chain(chain, feedback=0, plot_every=0)`, all other settings tensiometer's defaults
   (*dated clarification 2026-11-18, from the referee, after the run: in tensiometer 1.1.0 the ten
   "trainings" are warm restarts: populations 2–10 continue from the previous population's weights,
   only the optimiser restarts; the settings are unchanged*):
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
the 1-D S8 (not run, see the amendment of 2026-11-18) and 2-D (S8, Ωm) flows next to this study's binned-KDE values (`r2.json` `1d.n_sigma`
2.6735 and `2d.n_sigma` 2.1777); each repetition's Δ, interval and training time; the R4 Gaussian
values beside the flow values. Like R2, R6 uses the chains as they are: no prior flow, no truncation.

**Data and environment.** No new download: the two chains are read from the cache through `ctx.http`
(the existing run, with the ξ± chain, is charged 163.0 MiB of the 200 MiB budget). The six columns,
S8 and the weights are passed to the TF environment as one temporary file in the cache staging area
(about 9 MB), written and deleted inside `try/finally`, never a cache entry; the interpreter is
resolved from `%LOCALAPPDATA%` at run time and only its availability and package versions are
saved. Expected run time about 3–4 hours (each training about 10 minutes).

**Amendment 2026-11-18 (after a stalled run, before any secondary result was seen): the 1-D flow is
not run.** The formal run of 2026-11-17 finished the known-answer gate (seeds 10–12), the main case
(seeds 0–4), the S8-for-As case and the constrained case (seeds 0–2 each; about 4–13 minutes per
repetition), then ran for 20 hours on the first 1-D repetition (S8 alone) without finishing and was
stopped. Diagnosis on synthetic data only: with tensiometer's default settings a 2-D flow trains in
seconds, but a 1-D flow never starts training, because tensiometer 1.1.0's
`trainable_bijectors.min_var_permutations` draws random permutations until it finds one different
from the identity, and in one dimension the identity is the only permutation, so the loop never
ends. The 1-D flow is therefore not run and is reported as "not run (tensiometer 1.1.0 does not
support a 1-D flow with its default settings)"; the binned-KDE 1-D value (`r2.json` `1d.n_sigma`)
stays the reference. Nothing else changes (all other cases keep `max_iter = 1000`). Nothing of the
stopped run was opened: no job result file and no log line with a Δ or n_σ was read; its job folder
was deleted. The whole R6 is rerun from scratch (the job cache is keyed by the configuration);
with fixed seeds the gate and main results are expected to be identical. (A first version of this
amendment, the same day, wrongly blamed the iteration cap of the constrained case and capped the
reported cases at 100 iterations; that was withdrawn before any run.)

### 2.7 Addendum 2026-11-18: R6-NOMNU, the full-space difference without Σmν (T-040)

Written after R6 and its referee review, before any flow without Σmν or with `pop_size = 1` was
trained on the chains. It changes nothing above; R6's recorded verdict, "not evaluable", stays as
recorded, and R6 itself is not retrained: with the new key `"r6_retrain": False`, run.py loads the
recorded `results/r6.json`, checks that it is complete (`flows.complete` true, `flows.gate.passed`
true, five repetitions in `flows.main` for seeds 0–4, each finite, `flows.main.n_bar` = 1.69853 and
`flows.main.s` = 0.0977, both to 4 decimals), does not call R6's training and does not rewrite `r6.json`,
and passes n̄₆ and the per-seed n₆,k to R6-NOMNU; if the file is missing or does not pass these checks,
R6-NOMNU is "not evaluable". This reuse path, the `pop_size` argument and a gate whose dimension follows
its box count (the current `flowshift` gate helpers assume six dimensions) are code to be written at the
code stage; none exists yet.

*Why.* R6 gave 1.61–1.86σ for the six-parameter difference; the referee found, post hoc, that Σmν alone
gives 1.74σ (section 6). Removing Σmν tests whether the full-space number is carried by that prior-edge
direction. Separately, tensiometer's ten "populations" turned out to be warm restarts of one
initialisation (section 2.6 step 4), so whether they help is open. In tensiometer 1.1.0
(`synthetic_probability.py`), `flow_from_chain(chain, **kwargs)` passes its keyword arguments to both
the callback and `global_train`, whose loop `while ind <= pop_size` skips already-built layers, recompiles
a fresh Adam optimiser, trains up to 100 epochs per round with the default early-stopping scheduler and
keeps the weights with the lowest final validation loss: `pop_size = 1` is one initialisation trained
once, without warm restarts or selection.

*Seen before this addendum.*
- R6 main case, seeds 0–4 (A_s, h, Σmν, n_s, Ωb, Ωm): 1.857, 1.643, 1.719, 1.605, 1.669; n̄₆ = 1.699,
  s = 0.098; R6 gate s = 0.135 over seeds 10–12, exact value 2.371; S8-for-A_s case 1.714; (A_s, Ωm)
  flow 0.401 (binned KDE 0.381); (S8, Ωm) flow 2.143; Gaussian full space 0.89σ (six parameters) and
  0.32σ for (A_s, Ωm).
- 1-D binned-KDE differences (`explore/referee_r6_marginals.py`, one seed): Σmν 1.737σ, the other five
  0.21–0.89σ each; pairs (Σmν, A_s) 1.27σ, (Σmν, Ωm) 0.99σ. Σmν means: CMB 0.122 ± 0.056 (against the
  0.06 eV edge), DES 0.384 ± 0.147. Prior support passed for all six parameters. Each R6 training took
  about 12.5 min (6-D) or 5 min (2-D).
- *Predictability, both ways.* The marginals and the (A_s, Ωm) flow point to a low 5-D value ("mainly
  Σmν"). A Gaussian χ² bookkeeping on recorded numbers only (done while drafting this addendum) points
  higher. Mapping: n_σ ↔ χ² by equal tail probability, two-sided Gaussian n_σ against χ² with k degrees
  of freedom (k = 6 for six parameters, 5 for five, 1 for one). Then 1.699σ in 6-D corresponds to an
  effective χ² ≈ 11.0; Σmν's own 1.737² ≈ 3.0 is 27.5% of it; if
  Σmν carried exactly that share, the 5-D value would be about 1.41σ, and about 1.94σ if it carried
  nothing. The bookkeeping assumes independent Gaussian directions, while (Σmν, A_s) is 1.27σ. The
  band edges below come from it. Also seen: all other entries of `results/r6.json` and section 6 (among
  them the gate repetitions 2.374, 2.273, 2.541; the S8-for-A_s spread 0.041; P(ΔΣmν > 0) = 0.935; the
  referee's own 1.742σ; and the referee's note that the `ranges` prior bijector depends on the seed).

*Question.* Is the DES − CMB difference in (A_s, h, Ωb, n_s, Ωm) clearly smaller than in the six
parameters? Separately, does `pop_size = 1` change n̄ or s relative to the default?

*Method.*
- Data and estimator as R6: same chains, rows, weights, burn-in and R1 gate; section 2.6 steps 1–5
  (N = 100,000, `estimate_shift(tol=0.02, max_iter=1000, step=100000)`); the only change is dropping the
  `mnu` column: the 5-D arrays are taken from the 6-D column set (same finite-row mask), then `mnu` is
  dropped. Seeds 0–4; with the same seed the 5-D resampled rows are R6's 6-D rows, so the comparison is
  paired. R6's prior-support result (all six passed) applies to the five kept parameters and is not
  re-applied.
- Flow settings: R6's defaults, only the dimension changes; for the comparison
  `flow_from_chain(..., pop_size=1)` with everything else unchanged. The `pop_size` actually passed is
  recorded (not the signature default).
- Known-answer gate (5-D): R6's synthetic distribution without the edge box `boxes[3]` = [−0.1, 1.9,
  0.1] (the curved pair plus the three flat boxes; since `synthetic()` draws x₁, x₂ and then the boxes in
  order, with the same generators the 5-D gate rows are R6's first five columns); its exact n_σ by the same Monte Carlo (2,000,000 draws, `default_rng(999)`), not
  computed before this was written; seeds 10–12, R6's tolerances (mean within 0.10, each within 0.20);
  run before the chains with default settings; if it fails, the default 5-D case is "not evaluable" and
  (b) is not run, while (c) and (d) still run (descriptive only). The R6 6-D gate is kept as recorded.
- Runs: (a) 5-D gate, default; (b) 5-D chains, default, seeds 0–4; (c) 5-D and 6-D gates with
  `pop_size = 1`, seeds 10–12; (d) 5-D and 6-D chains with `pop_size = 1`, seeds 0–4. Baseline n̄₆ is
  R6's recorded 1.699 (seeds 0–4).

*Label for R6-NOMNU, fixed now* (a reading of the full-space number, not a verdict on D26; rules in
order, the first that applies decides):
1. R1 gate or 5-D gate fails → "not evaluable".
2. A default 5-D repetition fails, is non-finite or has not converged → "not evaluable".
3. If any repetition is a lower bound, n̄₅ is not used: "not mainly Σmν" if the minimum over all five
   repetitions (finite values and bounds) is ≥ 1.40, otherwise "not evaluable".
4. s₅ > 0.15 → "not evaluable". With s₅ ≤ 0.15 the half-width 2s₅/√5 ≤ 0.134 < 0.20, so I can never
   straddle both edges; the risk of "not evaluable" here is P(s > 0.15) ≈ 0.06 if the true σ = 0.10 and
   ≈ 0.29 if it is 0.135.
5. Otherwise the interval I = n̄₅ ± 2 s₅/√5 (unrounded values, s with ddof = 1; about 88% coverage with
   4 degrees of freedom) decides: I ⊂ (−∞, 1.00] → **"the full-space shift is mainly the Σmν
   direction"** (at least 0.70 below n̄₆; with the mapping above, 1.00σ in 5-D is χ² = 5.89 against 10.97,
   at least 46% of the effective χ² lost); I ⊂ [1.40, ∞) → **"not mainly Σmν: the other directions carry most of the shift"** (1.41σ is the value
   expected if Σmν carried only its own 1-D share); I ⊂ (1.00, 1.40) → "partly the Σmν
   direction"; otherwise (I straddles 1.00 or 1.40) → "between the two adjacent
   labels (not decided)".
6. s₅ ≤ 0.07 (R6's stability threshold) is reported as a flag and does not decide the label. Reason:
   these bands are 0.4σ wide, whereas R6 needed ±0.15 around 1.8, and R6's measured spreads (0.098;
   gate 0.135) show that 0.07 as a decisive rule would make "not evaluable" the likely outcome.

*`pop_size` comparison (descriptive, no label),* per dimension: "spreads differ" only if the variance
ratio (larger over smaller) exceeds F₀.₉₅(4, 4) = 6.39 (s ratio > 2.53; a two-sided 10% test), otherwise "no detectable difference in spread with
five repetitions"; "means differ" if |n̄₁ − n̄₁₀| > 2√(s₁²/5 + s₁₀²/5) (a descriptive heuristic, not a calibrated
test; the paired per-seed differences are also reported). The `pop_size = 1` gate results are
reported but do not gate (d); a failed `pop_size = 1` repetition is reported as failed.

*Reported.* Per seed: Δ, interval, n_σ, training time and the `pop_size` used; paired differences
n₆,k − n₅,k for both settings; both 5-D gate exact values; the R6 numbers beside the new ones.

*Runtime.* From R6 (10,583 s; chain trainings 746–759 s in 6-D, 308–315 s in 2-D; gate trainings 769–807 s):
5-D default about 650 s × 8 ≈ 1.5 h; `pop_size = 1` not measured (R6's 750 s ÷ 10 rounds is a lower guess;
round 1 may be the longest), guessed ≤ 1 h for 16 trainings; about 2.5 h in venv-tf (`TF_USE_LEGACY_KERAS=1`), scheduled apart from other CPU runs; no data
downloaded (chains from the cache). PARAMS: `"r6_nomnu": True`, `"r6_nomnu_seeds": [0, 1, 2, 3, 4]`,
`"r6_nomnu_s_max": 0.15`, `"r6_nomnu_bands": [1.00, 1.40]`, `"r6_pop1": True`, `"r6_retrain": False`; output
`results/r6_nomnu.json`.

### 2.8 Addendum 2026-11-19: R6-SHUF, what Σmν adds to the full-space difference (T-044)

Written after R6-NOMNU and its referee review, before any flow was trained on a shuffled or
prior-replaced Σmν column. It changes nothing above; the R6 and R6-NOMNU labels stay as recorded, and
neither is retrained. The per-seed values are read from the recorded files:
- n₆,k from `results/r6.json` with section 2.6/2.7's checks (`flows.complete` and `flows.gate.passed`
  true; `flows.main` repetitions for seeds 0–4, each finite, converged and not a lower bound;
  `flows.main.n_bar` = 1.6985 and `flows.main.s` = 0.0977 to 4 decimals);
- n₅,k from `results/r6_nomnu.json`, default case only (`flows.complete` and `flows.gate5.passed`
  true; `flows.nomnu` repetitions for seeds 0–4, each finite, converged and not a lower bound;
  `flows.nomnu.n_bar` = 0.5236 and `flows.nomnu.s` = 0.0402 to 4 decimals; not the `pop_size = 1`
  cases).
If either file is missing or fails these checks, R6-SHUF is "not evaluable".

*Why.* R6-NOMNU found that without Σmν the difference is 0.52σ, against 1.70σ in six parameters. Its
referee (section 6) showed with a k-nearest-neighbour (kNN) density estimate that shuffling DES's Σmν
column, which keeps its marginal and breaks its correlations with the other DES parameters, lowers the
6-D value from 1.270/1.572σ to 0.781/0.795σ (k = 20/100), and that drawing DES's Σmν from its prior
lowers it to 0.690/0.608σ. The kNN estimator is not calibrated: on R6's synthetic gate distributions
(a design check run while drafting this addendum, synthetic data only, seeds 10–12, N = 100,000; the
script is added as `explore/t044_knn_gate_design.py` in the same change) it gives 2.03–2.24σ against the exact 2.371 (6-D)
and 2.02–2.16σ against 2.386 (5-D), 0.13–0.37σ low at k = 20, 50 and 100. This addendum therefore uses
R6's flows, the estimator that passed the gate; kNN is reported beside them as descriptive.

*Seen before this addendum.* Everything in sections 5–6 (R6, R6-NOMNU and both referee tables),
including the kNN numbers above, the Gaussian conditional χ² of Σmν given the other five (4.35 against
its marginal 2.74), DES's Σmν 0.384 ± 0.147 against the uniform prior's 0.330 ± 0.156, and the 1-D
difference with DES's Σmν drawn from the prior (1.05σ). From the kNN numbers, with the kNN 5-D value
(0.556/0.466) in place of n₅, the quantities defined below would be φ ≈ 0.68, ψ ≈ 0.13, ρ ≈ 0.19 at
k = 20 and φ ≈ 0.70, ψ ≈ 0.17, ρ ≈ 0.13 at k = 100; the expected label is therefore "mainly through
DES-side correlations". No flow has been trained on a shuffled or prior-replaced column. The prior
range was read from the cached chains' headers while drafting: both the DES 3x2pt and the CMB chain
give `mnu = 0.06 0.0773062 0.6` in their `[cosmological_parameters]` values section and no Σmν entry
in a priors section, i.e. a uniform prior on [0.06, 0.6] eV (the CosmoSIS default within the values
range).

*Question.* Of what Σmν adds to the 6-D DES − CMB difference over the 5-D one, what fraction disappears
when Σmν's correlations with the other **DES** parameters are broken (the CMB chain's own Σmν
correlations are kept)?

*Method.*
- Data, rows, weights, burn-in, the R1 gate, N = 100,000, the flow settings (tensiometer defaults,
  `pop_size` not passed) and `estimate_shift(tol=0.02, max_iter=1000, step=100000)` exactly as R6
  (section 2.6); 6-D parameters (A_s, h, Σmν, n_s, Ωb, Ωm); seeds 0–4; TensorFlow seeded with k as in
  R6.
- For seed k the DES and CMB rows are drawn exactly as in R6's `resampled_difference`: the same two
  `rng.choice` calls, in the same order, on `default_rng(k)`; a unit test checks that with no column
  change the difference is bitwise equal to `resampled_difference`. So every variant is paired with R6
  and R6-NOMNU at the same seed. Then only resampled Σmν columns are changed, before the difference is
  taken:
  - **(S) DES shuffled:** the N resampled DES Σmν values are permuted with
    `numpy.random.default_rng(1000 + k).permutation(N)` (DES's weighted Σmν marginal is kept; its
    pairing with the other DES parameters is broken);
  - **(P) DES prior:** the N resampled DES Σmν values are replaced by `default_rng(2000 + k).uniform(0.06,
    0.6, N)` (DES's marginal and correlations both replaced by the prior);
  - **(SS) both shuffled, descriptive:** as (S), and the N resampled CMB Σmν values are permuted with
    `default_rng(3000 + k).permutation(N)` (both chains' Σmν correlations broken; no label).
  All other columns are unchanged. Flows are trained on the resulting 6-D differences, giving n_S,k,
  n_P,k and n_SS,k. The same differences, and the 5-D difference without Σmν at the same seed,
  are also passed to the kNN estimator, reported only: each sample x is whitened with the sample mean m
  and covariance Σ (z = (x − m)L with LLᵀ = Σ⁻¹), the density proxy of a point is its distance to its
  k-th nearest neighbour among the samples (k = 20 and 100), and n_σ = √2 erf⁻¹(f) with f the fraction
  of samples whose proxy distance is smaller than the origin's (as in `explore/t044_knn_gate_design.py`);
  it is computed in venv-tf on the arrays the flows are trained on.
- Environment: the run records the versions and flow settings as R6 does; they must equal those in
  both recorded files (`flows.versions`: tensorflow 2.21.0, tensiometer 1.1.0, getdist 1.7.7, numpy
  2.5.5, legacy_keras 1; and `flows.settings`), otherwise R6-SHUF is "not evaluable" (rule 1).
  Determinism check, reported only: R6 seed 0 is retrained once through the new draw path with no
  column change (so it checks that path as well as TensorFlow determinism; a new job folder is used,
  no earlier result can be picked up) and its n_σ is compared with the recorded 1.8569; if they differ
  by more than 0.02, the result carries the flag "cross-run pairing approximate" and φ̄ is still read.
- Low-shift known-answer gate (6-D, run first, default settings): R6's 6-D synthetic distribution
  (section 2.6, `flowshift.synthetic`) with the curved pair moved to μ₁ = 1.1, μ₂ = 0.55 (curvature
  and the four boxes unchanged); its exact n_σ, by R6's Monte Carlo (2,000,000 draws,
  `default_rng(999)`), is 0.8601, computed while drafting this revision (synthetic data only; the
  candidates tried were (μ₁, μ₂) = (0.5–1.3, 0–0.65), exact 0.28–1.14, and 1.1/0.55 was chosen as the
  value nearest the expected range of n_S); seeds 10–12, R6's tolerances (mean within 0.10, each within
  0.20). R6's recorded 6-D gate (exact 2.371) stays as the high-shift check. The low-shift gate tests one
  point (0.86) inside the expected range of n_S and n_P (0.6–1.0) in 6-D, on a synthetic distribution,
  not the whole range or the shuffled and prior-replaced distributions themselves; n₅ (0.52, 5-D) is recorded and not re-gated. R6's design notes
  and the R6-NOMNU referee (item 5) show flows biased high at small shifts; the low-shift gate bounds
  that bias at 0.86 in 6-D, and any remaining bias moves φ in a direction not known in advance.

*Quantities, per seed k* (all from flows, paired): E_k = n₆,k − n₅,k (what Σmν adds);
φ_k = (n₆,k − n_S,k) / E_k (the fraction removed by breaking Σmν's DES-side correlations);
ψ_k = (n_S,k − n_P,k) / E_k (DES's own Σmν marginal against its prior);
ρ_k = (n_P,k − n₅,k) / E_k (what remains with DES's Σmν at its prior: the CMB chain's Σmν, including
its CMB-side correlations, against the prior, the effect of the sixth dimension itself, and any
residual). φ_k + ψ_k + ρ_k = 1 identically; the split depends on the order chosen (shuffle, then prior)
and is not a unique decomposition. φ_k can lie outside [0, 1] (above 1 if n_S,k < n₅,k, below 0 if
n_S,k > n₆,k); the rules below cover both. Means and s (ddof = 1) over the five seeds; φ is also
reported on the χ²-equivalent scale (descriptive): φ_χ²,k = (χ²₆,k − χ²_S,k)/(χ²₆,k − χ²₅,k), each χ² from
its n_σ by section 2.7's mapping (k = 6 degrees of freedom for n₆ and n_S, 5 for n₅).

*Label for R6-SHUF, fixed now* (a reading of the 6-D number, not a verdict on D26; rules in order, the
first that applies decides):
1. R1 gate fails, the R6 or R6-NOMNU records fail their checks, or the versions or flow settings differ
   from the recorded ones → "not evaluable".
2. The low-shift gate fails (a repetition failed, non-finite, not converged or a lower bound, or the
   tolerances missed) → "not evaluable (low-shift gate)"; the variants are still run and reported as
   descriptive only.
3. Any (S) or (P) repetition fails, is non-finite, has not converged or is a lower bound → "not
   evaluable". ((SS) and the determinism check do not decide.)
4. Any E_k ≤ 0.20 → "not evaluable" (the ratio is unstable; the recorded E_k are 1.03–1.38).
5. s_φ > 0.30 → "not evaluable". (Expected s_φ: each flow value scatters by about 0.1σ in 6-D, so
   n₆,k − n_S,k scatters by about 0.14 and φ_k by about 0.12 for E ≈ 1.2.)
6. Otherwise the interval I_φ = φ̄ ± 2 s_φ/√5 (unrounded values) decides: I_φ ⊂ [0.60, ∞) → **"what Σmν
   adds is mainly through its correlations with the other DES parameters"**; I_φ ⊂ (−∞, 0.40] →
   **"what Σmν adds is mainly not through its DES-side correlations (the Σmν direction itself,
   including the CMB side and the prior)"**; otherwise (I_φ reaches into (0.40, 0.60)) → "between the
   two labels (not decided)". Why a band and not 0.50: s_φ measures training and resampling scatter
   only, not the chains' own finite-sample noise, which section 6 (item 2) puts at about ±0.03 per n_σ
   (chain-row bootstrap, R2); the variants share the same rows, so that noise is largely common to
   n₆, n_S and n₅, and even uncorrelated it would move φ by about √2 × 0.03 / 1.2 ≈ 0.035. The
   ±0.10 band around 0.50 is about three times that (a heuristic, not a derived uncertainty of φ).

*Reported, descriptive.* Per seed n_S,k, n_P,k, n_SS,k, Δ, intervals, training times; E_k, φ_k, ψ_k,
ρ_k with means and s; n̄_S, n̄_P, n̄_SS with s; the kNN values of all variants; the determinism check;
the low-shift gate's repetitions and exact value. ψ̄, ρ̄, (SS) and kNN get no label.

*Runtime.* R6's 6-D chain trainings took 745–759 s and its gate trainings 769–807 s; 19 trainings (the
3 low-shift gate trainings, 5 × S, P, SS and the determinism check) ≈ 4.0 h in venv-tf (`TF_USE_LEGACY_KERAS=1`, through the project venv's subprocess as for R6),
run after study 010's T-031 run has finished (that run requires an otherwise idle machine); no data
downloaded (chains from the cache). PARAMS: `"r6_shuf": True`, `"r6_shuf_seeds": [0, 1, 2, 3, 4]`,
`"r6_shuf_s_max": 0.30`, `"r6_shuf_e_min": 0.20`, `"r6_shuf_band": [0.40, 0.60]`,
`"r6_shuf_gate": {"mu1": 1.1, "mu2": 0.55, "exact": 0.8601}`,
`"r6_shuf_seed_offsets": [1000, 2000, 3000]`, `"r6_shuf_prior": [0.06, 0.6]`, `"r6_shuf_knn_k": [20, 100]`;
output `results/r6_shuf.json`. R1–R5 run as usual (seconds). R6 and R6-NOMNU are not retrained and
their result files are read, not rewritten: R6 through the existing `"r6_retrain": False` path; for
R6-NOMNU a new key `"r6_nomnu_retrain": False` skips all of its runs (a)–(d), including the
`pop_size = 1` cases, whatever `"r6_nomnu"` and `"r6_pop1"` say, and checks and reads
`results/r6_nomnu.json` instead. This reuse path, the column variants and the kNN report are code to
be written at the code stage; none exists yet.

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

**R6-FLOW (verdict, addendum 2026-11-16, section 2.6): not evaluable.** Run of 2026-11-18
(`python -m astrolab run 008`, 10,583 s; tensiometer 1.1.0, TensorFlow 2.21.0, legacy Keras; all
earlier results reproduce exactly, only timing and provenance fields changed). Numbers from
`results/r6.json`; every repetition converged, none was a lower bound; each training took
about 12.5 minutes (6-D) or 5 minutes (2-D).

| Case | n_σ per seed | n̄ | s | reference |
|---|---|---|---|---|
| Known-answer gate (synthetic 6-D; seeds 10–12) | 2.374, 2.273, 2.541 | 2.396 | – | exact 2.371: mean within 0.10, each within 0.20, **passed** |
| **Main: (A_s, h, Σmν, n_s, Ωb, Ωm), seeds 0–4** | 1.857, 1.643, 1.719, 1.605, 1.669 | **1.699** | **0.098** | D26 1.8; Gaussian 0.887 |
| S8 in place of A_s (seeds 0–2) | 1.749, 1.670, 1.722 | 1.714 | 0.041 | Gaussian 1.48 |
| (A_s, Ωm) (seeds 0–2) | 0.396, 0.405, 0.401 | 0.401 | 0.004 | binned KDE, same run, 0.381; Gaussian 0.323 |
| (S8, Ωm) (seeds 0–2) | 2.158, 2.126, 2.144 | 2.143 | 0.016 | binned KDE (R2) 2.178 |
| 1-D flow in S8 | not run (amendment 2026-11-18) | – | – | binned KDE (R2) 2.674 |

- **Verdict.** Conditions (1)–(5) of section 2.6 do not apply: the R1 gate and the known-answer gate
  passed, all five repetitions converged with finite n_σ, prior support passed (no weight of either
  chain outside the other's prior range for any of the six parameters), and no repetition is a lower
  bound. Condition (6) applies: s = 0.098 > 0.07, so R6 is **not evaluable**, and the band rule is not
  applied. No rerun with other settings, as registered.
- **Descriptive (not a verdict).** The five main-case values span 1.61–1.86σ around D26's single
  1.8σ; their mean, 1.70, lies 0.10 below it. Training noise is the limiting factor: one flow
  training moves n_σ by about 0.1σ (s = 0.098 on the chains; the three gate values scatter by 0.13
  on the synthetic case), so a single flow number such as D26's 1.8σ carries a training uncertainty
  of about this size, which D26 does not quote.
- **Parametrization (descriptive).** Unlike the Gaussian approximation of R4 (0.89σ with A_s,
  1.48σ with S8), the flow gives nearly the same value in both parametrizations (seeds 0–2: 1.740
  with A_s, 1.714 with S8). On the two planes where both estimators exist, flow and binned KDE agree
  within 0.04σ ((A_s, Ωm) 0.401 against 0.381; (S8, Ωm) 2.143 against 2.178).
- *Post hoc remark (2026-11-18, not a change of rule):* section 2.6 accepted a 10% chance of "not
  evaluable" if the true spread were 0.05; the observed spreads (s = 0.098 on the chains, s = 0.135
  over the three gate seeds) suggest a true spread of about 0.1, for which s > 0.07 is the likely
  outcome. The 0.07 threshold was set from the design runs without a measured spread; this is recorded, the label
  stands.

**Reading.** The public chains reproduce D26's inputs and its 1-D and 2-D differences: the numbers
behind the conclusion are reproduced. Whether 2.6–2.7σ is "no substantial evidence" is the interpretation
step `gap_conv` of the wiki's Lean analysis (a 3σ-as-evidence usage, not stated by D26); the numbers
show how close it is to that line (2.67σ, and 2.44–2.55σ under D26's own projection-effect estimates).
For DES the "easing" is small: the earlier DES Y3 result was 2.83σ from this CMB, the Y6 3x2pt
result 2.67σ. Most of the easing in R5 comes from KiDS.

- **Full space (R6, added 2026-11-18).** The flow estimate of the six-parameter difference is
  1.6–1.9σ over five trainings (mean 1.70), around D26's 1.8σ, but its training scatter (0.1σ)
  exceeds the registered stability limit, so R6 gives no verdict. The full-space number is not
  reproduced or refuted; it is bracketed.
- **Post hoc (referee, 2026-11-18; section 6): the full-space number may be mostly Σmν.** The CMB
  chain's Σmν sits against the shared prior edge at 0.06 eV (0.122 ± 0.056) while DES is
  prior-dominated (0.384 ± 0.147); Σmν alone gives a 1-D difference of 1.74σ, the other five
  parameters 0.21–0.89σ each (`explore/referee_r6_marginals.py`). If the 6-D number is carried by this prior-edge direction, D26's 1.8σ
  (and our 1.6–1.9σ) would say little about a disagreement in the data-constrained directions,
  where the flow gives 0.40σ for (A_s, Ωm). A 1-D marginal does not decide the 6-D number; the
  pre-registered test is T-040 (a 5-D flow without Σmν).

**R6-NOMNU (addendum 2026-11-18, section 2.7, T-040): the full-space shift is mainly the Σmν
direction.** Run of 2026-11-18 (`python -m astrolab run 008`, 7,098 s; R1–R5 unchanged; R6 reused from
the recorded `results/r6.json`, checks passed, not retrained; numbers in `results/r6_nomnu.json`).

| Run | n_σ per seed | n̄ | s | Outcome |
|---|---|---|---|---|
| (a) 5-D gate, default (seeds 10–12) | 2.401, 2.331, 2.452 | 2.395 | – | exact 2.386: **passed** |
| (b) 5-D chains (A_s, h, n_s, Ωb, Ωm), default (seeds 0–4) | 0.478, 0.551, 0.518, 0.576, 0.494 | **0.524** | 0.040 | I = [0.488, 0.560] ⊂ (−∞, 1.00] |
| R6, 6-D chains, default (recorded) | 1.857, 1.643, 1.719, 1.605, 1.669 | 1.699 | 0.098 | – |
| (c) 5-D gate, `pop_size = 1` | 2.253, 2.215, 2.328 | 2.265 | – | exact 2.386: failed (mean 0.12 low; reported only) |
| (c) 6-D gate, `pop_size = 1` | 2.372, 2.376, 2.529 | 2.425 | – | exact 2.371: passed (reported only) |
| (d) 5-D chains, `pop_size = 1` | 0.408, 0.464, 0.509, 0.479, 0.434 | 0.459 | 0.039 | – |
| (d) 6-D chains, `pop_size = 1` | 1.803, 1.823, 1.655, 1.832, 1.626 | 1.748 | 0.099 | – |

- **Label (pre-registered, rule 5): "the full-space shift is mainly the Σmν direction".** Rules 1–4
  do not apply (R1 and the 5-D gate pass; every repetition finite and converged; no lower bound;
  s₅ = 0.040 ≤ 0.15). Flag (rule 6): s₅ ≤ 0.07. Paired per seed, n₆ − n₅ = 1.38, 1.09, 1.20, 1.03,
  1.17 (mean 1.17).
- **What it means.** Without Σmν the DES − CMB difference in the other five parameters is about 0.5σ;
  with the pre-registered mapping that is an effective χ² of 3.65 against 10.97 for 1.699σ in 6-D,
  so about two thirds of the full-space difference goes with Σmν, the direction in which the CMB
  chain sits against the 0.06 eV prior edge. D26's full-space 1.8σ (and R6's 1.6–1.9σ) therefore
  mostly goes with Σmν; in the other five parameters the difference is about 0.5σ (h, n_s and Ωb are
  themselves largely prior-dominated in DES; in the data-constrained pair (A_s, Ωm) the R6 flow gives
  0.40σ). Section 2.7 had both predictions on record: the
  marginals and the (A_s, Ωm) flow pointed low; the Gaussian χ² bookkeeping (1.41σ if Σmν carried
  only its 1-D share) pointed higher. The outcome lies below the lower band edge (1.00) and far below the
  bookkeeping's 1.41σ, so the bookkeeping's independence assumption does not hold here.
- **`pop_size` comparison (descriptive, no label).** Training time per flow falls from about 670–
  705 s (5-D) and 746–759 s (6-D, R6) to 71–83 s. Spread: variance ratios 1.05 (5-D) and 1.03 (6-D), "no detectable difference in
  spread with five repetitions" in both. Means: 5-D "means differ" (n̄ 0.459 against 0.524; the
  difference 0.065 exceeds the heuristic threshold 0.050; paired per-seed differences −0.070,
  −0.087, −0.009, −0.097, −0.060); 6-D "means do not differ by the heuristic" (1.748 against 1.699;
  threshold 0.124). The `pop_size = 1` 5-D gate is 0.12 low against its exact value, outside R6's
  tolerance, so with one population the flow underestimates the known-answer case in 5-D; the
  restarts of the default appear to help there (three gate seeds and five paired chain seeds). Neither run changes the label.
- **Post hoc (referee, 2026-11-18; section 6): Σmν together with its correlations, and partly the
  prior.** The label stands, but "the Σmν direction" is narrower than what the checks show. In the
  Gaussian approximation Σmν adds a conditional χ² of 4.35 given the other five, more than its
  marginal 2.74. A k-nearest-neighbour (kNN) density estimate of the 6-D difference gives 1.27/1.57σ
  (k = 20/100) on the real chains, 0.78/0.80σ with DES's Σmν column shuffled (its marginal kept, its
  correlations with the other parameters broken) and 0.69/0.61σ with DES's Σmν drawn from the uniform
  prior [0.06, 0.6] eV. So most of what Σmν adds to the 6-D number comes from it jointly with its DES correlations
  (probably the A_s–Σmν degeneracy; an inference), and the near-equality of the 1-D Σmν value
  (1.74σ) and the 6-D flow value (1.70σ) is largely a coincidence (an inference). DES's Σmν is close
  to its prior (0.384 ± 0.147, against the prior's 0.330 ± 0.156); with DES's Σmν replaced by the prior the 1-D
  difference is still 1.05σ, i.e. about 1σ of the 1-D "shift" is the CMB chain at the prior edge
  against the DES prior. Shuffling keeps that placement but still removes most of what Σmν adds over the 5-D value (about
  70% at k = 20 and 100), so the placement is the smaller part and the correlations the larger. The 5-D value (0.52σ; kNN
  0.56/0.47σ, Gaussian 0.21σ) is therefore less affected by the Σmν prior edge; it is not a
  data-constrained number either (h, n_s and Ωb are largely prior-dominated in DES; (A_s, Ωm) 0.40σ). Dropping Σmν here means
  marginalising over it; conditioning on a fixed Σmν (DES's fixed-mass chain, 76 MB, above the
  50 MB per-download cap) would answer a different question and is not done. A pre-registered
  shuffle and prior-replacement check is registered as T-044.

**R6-SHUF (addendum 2026-11-19, section 2.8, T-044): what Σmν adds is mainly through its
correlations with the other DES parameters.** Run of 2026-11-20 (`python -m astrolab run 008`,
04:13–08:18, 14,707 s against the estimated 4.0 h; no other study run on the machine; R1–R5
unchanged; R6 and R6-NOMNU read from their recorded files, checks passed, not retrained; numbers in
`results/r6_shuf.json`). Each flow training took 754–776 s, except the first gate training (523 s).

| Run | n_σ per seed | n̄ | s | Outcome |
|---|---|---|---|---|
| Low-shift gate, 6-D synthetic (seeds 10–12) | 0.839, 0.689, 0.969 | 0.832 | – | exact 0.8601: **passed** (mean 0.028 low; largest single deviation 0.171, seed 11) |
| (S) DES Σmν shuffled (seeds 0–4) | 0.914, 0.949, 0.862, 0.893, 0.929 | **0.909** | 0.033 | – |
| (P) DES Σmν from the prior | 0.526, 0.617, 0.497, 0.528, 0.594 | 0.552 | 0.051 | – |
| (SS) both chains' Σmν shuffled (descriptive) | 0.907, 0.918, 0.841, 0.919, 0.962 | 0.909 | 0.044 | – |
| R6, 6-D (recorded) | 1.857, 1.643, 1.719, 1.605, 1.669 | 1.699 | 0.098 | – |
| R6-NOMNU, 5-D (recorded) | 0.478, 0.551, 0.518, 0.576, 0.494 | 0.524 | 0.040 | – |
| Determinism check (R6 seed 0 through the new draw path) | 1.857 | – | – | recorded 1.8569; difference 0.000 |

- **Label (pre-registered, rule 6): "what Σmν adds is mainly through its correlations with the other
  DES parameters".** Rules 1–5 do not apply: R1 passes; the versions and flow settings equal both
  recorded files; the low-shift gate passes; every (S) and (P) repetition is finite, converged and not
  a lower bound; E_k = 1.379, 1.091, 1.201, 1.029, 1.174 (all > 0.20); s_φ = 0.037 ≤ 0.30. φ_k =
  0.684, 0.636, 0.714, 0.692, 0.630; φ̄ = 0.671, I_φ = [0.638, 0.704] ⊂ [0.60, ∞). No flag (the
  determinism difference is 0.000 ≤ 0.02: R6 seed 0 is reproduced exactly; the other seeds and
  R6-NOMNU use the same draw path, which a unit test checks).
- **The rest of the split (descriptive).** ψ̄ = 0.306 (s 0.029; 0.28–0.35 per seed) and ρ̄ = 0.023
  (s 0.055; −0.047 to 0.085). On the χ² scale φ_χ² = 0.601 (0.56–0.64). Read in the registered order
  (shuffle, then prior; the split is not unique): of the 1.17σ that Σmν adds over the 5-D value, about
  two thirds goes when DES's Σmν is decoupled from DES's other parameters, about a third when DES's
  own Σmν marginal is then replaced by the prior, and almost nothing remains: with DES's Σmν at its
  prior the 6-D value (0.552) is within 0.03σ of the 5-D value (0.524).
- **(SS) agrees with (S)** (0.909 both; paired per-seed differences −0.031 to +0.034): shuffling the CMB
  chain's Σmν as well changes nothing visible (descriptive).
- **What it means.** Section 6 found that DES's Σmν against the CMB, with DES's Σmν drawn from the
  prior, still differs by 1.05σ in 1-D, because the CMB chain sits at the 0.06 eV prior edge. In six
  dimensions, what remains with DES's Σmν at its prior is only about 0.03σ over the 5-D value
  (n̄_P − n̄₅ = 0.029σ; ρ̄ = 0.023 of E).
  ρ̄ lumps together the CMB chain's Σmν against the prior, the sixth dimension itself and any residual,
  and does not separate them; nothing in it is of the size of the 1-D 1.05σ (a reading of ρ̄; n_P and
  n₅ are not gated). By the registered label (near the edge of the gates' calibration; see the post
  hoc item below), what Σmν adds to the full-space number comes mostly from how DES's Σmν co-varies with its other parameters (which
  parameters is not tested here; the referee's A_s–Σmν degeneracy remains an inference), and about a
  third from DES's Σmν marginal (0.384 ± 0.147) differing from its prior (0.330 ± 0.156). Combined
  with R6-NOMNU: the 5-D value without Σmν is about 0.5σ, and the 6-D value (R6 1.6–1.9σ, around D26's
  1.8σ) exceeds it by E ≈ 1.17σ, of which about two thirds goes with DES's own Σmν correlations and
  a small remainder (ρ̄) is left once DES's Σmν is at its prior. Section 2.8 expected this label from the kNN numbers
  (φ ≈ 0.68/0.70); its expected ψ (0.13/0.17) and ρ (0.19/0.13) were not borne out.
- **kNN, descriptive (not calibrated, section 2.8).** Means over the five seeds, k = 20/100: real
  1.247/1.527, (S) 0.917/0.871, (P) 0.699/0.538, (SS) 0.946/0.869, 5-D 0.533/0.501. From these means
  φ would be 0.46 at k = 20 and 0.64 at k = 100. Per seed, φ is 0.58–0.70 at k = 100 (in line with
  the flows) but 0.12–0.89 at k = 20, where the real-chain value scatters from 1.07 to 1.43 between
  seeds. So kNN at k = 100 agrees with the flow label and kNN at k = 20 does not; section 2.8's kNN
  expectation (φ ≈ 0.68 at k = 20) rested on one seed. The kNN values are not used for the label.
- **Limits.** The low-shift gate checks one point (0.86) in 6-D, on a synthetic distribution; it
  passes, but one of its three trainings was 0.17 low, so a single flow training at this level may
  be off by up to about 0.2σ (from three trainings; an inference). n_S (0.91) is close to the gated point and n₆ (1.70) lies between it
  and R6's gate (2.371); n₅ (0.52, 5-D) and n_P (0.55) lie below both, where R6's design notes found
  flows biased high, and are not gated. A high bias in n₅ shrinks E and raises φ; a high bias in n_P
  raises ρ and lowers ψ, not φ. The seed scatter s_φ excludes the chains' own finite-sample noise;
  section 2.8's band allows for about 0.035 of it, and I_φ's lower end is 0.038 above 0.60.
- **Post hoc (referee, 2026-11-20; section 6): the label is robust to training scatter but sits near
  the edge of what the gates certify.** s_φ (0.037, against the 0.12 expected in section 2.8) is
  small partly by construction: n_S and n₅ vary little between seeds, and φ moves by only about 0.28
  per unit of n₆, the noisiest input. The gates bound a mean bias only to about ±0.1σ. Correcting
  each input by its own gate's mean offset (n₆ by R6's gate, +0.025; n₅ by the 5-D gate, +0.009; n_S
  by the low-shift gate, −0.028) gives φ̄ = 0.635 and I_φ = [0.601, 0.669], still above 0.60 but by
  0.001 (our recomputation; a post hoc check, not a rule, and the gate offsets are themselves noisy:
  the low-shift gate's three trainings scatter by s = 0.14). If n_S were biased low by about 0.045σ
  relative to n₆ (the low-shift gate reads 0.028 low), or n₅ biased high by about 0.075σ (the
  direction R6's design notes found for flows at small shifts), the label would become "between". Shuffling replaces the joint
  distribution of Σmν and the other DES parameters by the product of their marginals, so φ measures
  what that change does to the difference; it does not show which DES parameters carry the
  correlation, or whether DES's low-Σmν region moves them away from the CMB. A known-answer test of φ
  itself and a check of DES's conditional means in Σmν bins are registered as T-047.

**Conditional means in Σmν bins (exploration, post hoc, 2026-11-20, T-047 first part; no flow).**
Script `explore/t047_conditional_means.py` (cache only, about a minute, single-threaded). Both
chains are binned in Σmν at the DES chain's weighted quintiles (edges 0.239, 0.359, 0.452, 0.529 eV;
outer bins open); in each bin the weighted mean and standard deviation of each other parameter are
compared, offset = (DES − CMB) / √(σ_DES² + σ_CMB²) of the conditional distributions, and the 2-D
offset in (A_s, Ωm) uses the summed conditional covariances (Gaussian approximation, χ² with 2
degrees of freedom expressed as a two-sided n_σ).

| Σmν bin (eV) | CMB weight (ESS) | Ωm | h | Ωb | n_s | A_s | (A_s, Ωm) 2-D |
|---|---|---|---|---|---|---|---|
| < 0.239 | 0.953 (9,882) | −0.21 | +0.01 | −0.54 | −0.56 | −0.67 | 0.33 |
| 0.239–0.359 | 0.044 (474) | −0.78 | +0.32 | −0.88 | −0.40 | −0.75 | 0.78 |
| 0.359–0.452 | 0.003 (38) | −1.07 | +0.57 | −1.13 | −0.26 | −0.81 | 1.05 |
| 0.452–0.529 | 0.001 (23) | −1.30 | +0.77 | −1.24 | −0.20 | −0.99 | 1.37 |
| ≥ 0.529 | 0.000 (13) | −1.53 | +0.99 | −1.41 | −0.26 | −1.24 | 1.80 |
| marginal (no binning) | – | +0.34 | +0.10 | −0.56 | −0.45 | −0.75 | 0.32 |

Each DES bin holds 0.20 of the weight (effective sample size, ESS, 1,862–2,393). Linear ties of Σmν
to the other five parameters, DES / CMB: multiple R² 0.867 / 0.926; partial correlations Ωm
+0.93 / −0.80, h +0.92 / −0.73, Ωb −0.86 / +0.79, n_s +0.39 / +0.30, A_s +0.78 / +0.09; pairwise
correlations Ωm +0.39 / +0.76, h +0.06 / −0.80, Ωb +0.00 / +0.83, n_s +0.05 / −0.18, A_s
−0.07 / +0.18.

- **Reading (descriptive).** In the DES chain a linear regression of Σmν on all five other
  parameters has R² = 0.87, with large partial correlations (conditional linear associations) with
  Ωm, h, Ωb and A_s, although the pairwise correlations are small except with Ωm (+0.39). So the
  pairwise correlations do not describe Σmν's linear ties, and shuffling DES's Σmν breaks a joint
  relation with the other parameters rather than one pair; which parameters matter for φ is not
  shown. In the lowest Σmν bin, where 95% of the CMB weight lies, the conditional mean offsets of Ωm
  and A_s and the Gaussian 2-D (A_s, Ωm) offset are similar to, or smaller than, their marginal
  counterparts (Ωm −0.21 against +0.34; A_s −0.67 against −0.75; in raw units Ωm −0.0048 against
  +0.0092, A_s −0.126 against −0.138 in 10⁻⁹; 2-D 0.33σ against 0.32σ). This compares means and a
  Gaussian summary, not the full conditional distributions, and says nothing causal. The Ωm, h, Ωb,
  A_s and 2-D offsets grow in size with Σmν (n_s does not). Across the bins the CMB's conditional means of Ωm, h and Ωb change more than
  DES's (Ωm: CMB 0.322 → 0.384, DES 0.318 → 0.344; h: 0.668 → 0.625 against 0.669 → 0.680; Ωb:
  0.0503 → 0.0572 against about 0.0458 throughout); for A_s both change (DES 1.993 → 1.949, CMB
  2.119 → 2.170). That the CMB's shifts follow its geometric degeneracy is an interpretation, not
  measured here. Above 0.36 eV the offsets compare DES with a CMB tail of ESS 13–38, so those rows
  are poorly determined. The sign change of the Ωm offset between the bins and the marginal is a
  mixture effect: the CMB weight sits in the lowest bin, the DES weight is spread over all five.
- **Limits.** Conditional means and covariances, per parameter and for one pair, not the 6-D
  difference; φ (a 6-D, partly non-linear quantity) cannot be read off them, and these numbers are
  not a check of φ = 0.67. One binning (quintiles of DES); no error bars (the ESS per bin is given).
  Bin offsets use conditional standard deviations and the marginal row marginal ones (the low-bin
  comparison holds in raw units too, above). The known-answer test of φ (T-047's flow part) needs a
  TensorFlow environment, which was removed after T-044 and is reinstalled only with the user's
  consent. Exploration output was deleted after these numbers were copied.

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

### Referee, R6-FLOW (independent subagent, 2026-11-18)

The referee saw README sections 1–4, the code and the results, not sections 5–8 or the log; it ran
short offline checks from the cache and read tensiometer's source. Triage:

| # | Point | Verified | Action |
|---|---|---|---|
| 1 | **The full-space number may be mostly the Σmν direction.** The CMB chain has Σmν = 0.122 ± 0.056, against the shared prior edge at 0.06; DES has 0.384 ± 0.147, prior-dominated over 0.06–0.6. The 1-D difference in Σmν alone, with the study's binned estimator, is 1.74σ (P(ΔΣmν > 0) = 0.935); the other five 1-D differences are 0.21–0.89σ, and the pairs (Σmν, A_s) and (Σmν, Ωm) 1.27σ and 0.99σ. The prior-support check cannot see this: both chains share the same prior ranges | yes: we reran the referee's cache-only script (3 s; its chain labels were swapped, corrected by row count): Σmν 1.742σ; then rewrote it with the study's own loaders as `explore/referee_r6_marginals.py` (one seed, 400,000 draws), which gives the numbers quoted here (Σmν 1.737σ) | **Accepted** (post hoc, 2026-11-18). Section 5 reading extended; the R6 label stands. A 1-D marginal does not decide the 6-D number, so this is suggestive, not shown. The decisive test (a 5-D flow without Σmν) is registered as T-040. |
| 2 | **`pop_size = 10` is not ten independent initialisations.** tensiometer 1.1.0's `global_train` skips layers that are already built (the model is built at initialisation), so populations 2–10 continue from the previous population's weights; only the optimiser and learning-rate schedule restart. Section 2.6 step 4 ("ten trainings … the best kept") describes the settings, not what the code does | yes: `synthetic_probability.py` lines 1051–1063 (the loop that skips built layers) and the referee's 3-population test (population 2 starts at population 1's final weights) | **Accepted** (dated clarification in section 2.6 step 4, 2026-11-18): each repetition is one initialisation trained in up to ten successive rounds; the seed spread is single-initialisation spread. The settings were tensiometer's defaults as registered; the verdict is unchanged. A `pop_size = 1` comparison is part of T-040. |
| 3 | The known-answer gate already showed a spread (s = 0.135 over seeds 10–12) about twice the registered limit 0.07, whose justification assumed a true spread of 0.05; "not evaluable" was predictable from the gate | yes (results) | Accepted; already in the post hoc remark of section 5, the gate spread added there. |
| 4 | The Clopper–Pearson "convergence" measures only the Monte Carlo sampling of one fixed flow (half-width about 0.0008 in Δ, 30–50 times smaller than the seed spread); the saved intervals are not uncertainties of n_σ | yes | Accepted; noted (section 5 does not quote them). |
| 5 | Smaller: the Monte Carlo error of the gate reference is about 0.002σ, not 0.001σ; the `ranges` prior bijector takes each repetition's range from that sample's minimum and maximum, so it varies with the seed; `main` and `s8_for_as` use the same resampling seeds (paired, not independent); with ESS about 10⁴ per chain, 100,000 draws repeat rows, so validation rows duplicate training rows | yes | Accepted as limitations; none changes the label. The paired seeds make the A_s/S8 comparison (1.740 against 1.714) a paired one. |
| 6 | The verdict order, the independent re-derivation in `test_conclusions.py`, the lower-bound handling and the analytic gate density are correct; the s ≤ 0.07 rule withheld a verdict that the band alone would have called "reproduced" (0.10 from 1.8, within 0.345), so it is not a moved goalpost; the amendment of 2026-11-18 is consistent with the results | – | None. |
| 7 | Literature (unverified, the referee's memory): Raveri & Doux 2021 (arXiv:2105.03324, flow-based shifts); Raveri & Hu 2019 (arXiv:1806.04649); Lemos et al. 2021 (arXiv:2012.09554); Raveri, Zacharegkas & Hu 2020 (arXiv:1912.04880, prior-dominated directions). D26's PTE 0.08 corresponds to 1.75σ | no | Context for T-040; to be raised to [V] before use. |


### Referee, R6-NOMNU (independent subagent, 2026-11-18)

The referee saw README sections 1–4, the code and the results, not sections 5–8 or the log; it was
limited to short single-threaded checks on the cached chains (no flow training), because study 010's
run was using the machine. We reran its scripts and reproduced every number below. Triage:

| # | Point | Verified | Action |
|---|---|---|---|
| 1 | The label re-derives from the saved numbers (n̄₅ 0.52363, s₅ 0.04021, I = [0.4877, 0.5596]; rules 1–4 do not apply); the 5-D column drop, seed pairing, gate construction, `pop_size` passing, rule order and comparison are correct | yes | None. |
| 2 | Σmν contributes jointly with its correlations: Gaussian conditional χ² 4.35 against marginal 2.74; kNN 6-D 1.27/1.57σ real, 0.78/0.80σ with DES Σmν shuffled, 0.69/0.61σ with DES Σmν from its prior; the 1.41σ band edge (Σmν's own 1-D share) has no firm basis | yes (our rerun) | **Accepted** (post hoc, section 5): the label is read as "Σmν together with its correlations"; the band edges were already reported as resting on a failed independence assumption. Label unchanged. |
| 3 | DES Σmν is close to prior-dominated (0.384 ± 0.147 against 0.330 ± 0.156; histogram rising to 0.6 eV); the CMB has 13% of its weight below 0.07 eV; with DES Σmν from the prior the 1-D difference is 1.05σ against 1.74σ | yes | **Accepted**: about 1σ of the 1-D Σmν shift is prior placement; the 5-D number is less affected by the Σmν prior edge (section 5), though h, n_s and Ωb are themselves largely prior-dominated in DES. |
| 4 | Marginalising over Σmν is not the only way to drop it; conditioning (DES's fixed-Σmν chain, 76 MB) answers a different question | yes (size from the pre-registration's chain list) | Accepted; section 5 states that the question is the marginal one; the conditional chain exceeds the 50 MB cap and would need the user's consent; not registered. |
| 5 | The gate tests Δ ≈ 0.98, not the result's regime (Δ ≈ 0.40); the design notes show flows biased high at small shifts, so 0.52 is if anything high; kNN 0.56/0.47 agrees, Gaussian 0.21 is lower | yes | Accepted limitation; the label (I ⊂ (−∞, 1.00]) is robust to a downward bias. |
| 6 | `pop_size = 1` underfits: lower in all five 5-D seeds (paired mean −0.065, s 0.034), fails the 5-D gate, passes the 6-D gate; the restarts reduce bias, not spread (s ≈ 0.04 in 5-D, 0.10 in 6-D for both) | yes | Accepted; the unpaired "means" heuristic is as pre-registered, the paired differences are reported in section 5. |
| 7 | On success `results/r6_nomnu.json` `r6_reused.reason` holds R6's own verdict reason ("s = 0.0977 > 0.07"), which reads like a failure reason | yes (`r6nomnu.py`) | Noted here: `r6_reused.ok` is the reuse outcome; `reason` is R6's recorded reason. Not changed (would need a rerun). |
| 8 | The reuse check does not test that `n_bar` and `s` agree with the per-seed values | yes | Accepted limitation (low risk: the file is checked against recorded values to 4 decimals). |
| 9 | Literature (from memory, not verified by the referee or us): Raveri & Hu 2019 (arXiv:1806.04649), Raveri, Zacharegkas & Hu 2020 (arXiv:1912.04880), Raveri & Doux 2021 (arXiv:2105.03324), Lemos et al. 2021 (arXiv:2012.09554), Krause et al. 2021 (arXiv:2105.13548) | no | Context only; not used; to be verified before any use. |
| 10 | Most important next test: the shuffle and prior-replacement check, pre-registered, with a non-flow estimator on the 6-D and (Σmν, A_s, Ωm) differences (minutes of CPU) | – | Registered as T-044. |

### Referee, R6-SHUF (independent subagent, 2026-11-20)

The referee saw README sections 1–4, the code, the results and the run log, not sections 5–8 or
`log.md`; it was limited to short single-threaded checks (no flow training) because study 003's run
was using the machine. Triage:

| # | Point | Verified | Action |
|---|---|---|---|
| 1 | The label re-derives from the saved numbers (φ_k 0.684, 0.636, 0.714, 0.692, 0.630; φ̄ 0.6712, s_φ 0.0366, I_φ = [0.6385, 0.7040]); rules applied in order (`r6shuf.py`); the variants change only the Σmν column(s) after R6's two `rng.choice` calls (`flowshift.py`); the determinism check reproduces R6 seed 0 exactly; the recomputed low-shift exact value is 0.86006 | yes (our recomputation; determinism difference 0.0) | None. |
| 2 | **The margin is smaller than what the gates certify.** With each input corrected by its gate's mean offset (+0.025, +0.009, −0.028), φ̄ = 0.635 and I_φ = [0.601, 0.669]; n_S biased low by about 0.045σ relative to n₆, or n₅ biased high by about 0.075σ, would give "between". n₅ was gated only at 2.39 | yes (our recomputation gives the same numbers) | **Accepted** (post hoc, section 5): the label stands as registered; it is reported as robust to training scatter but near the edge of the calibration. Known-answer test of φ registered as T-047. |
| 3 | The low-shift gate's three trainings scatter by s ≈ 0.14 (0.839, 0.689, 0.969), four times the chain variants' s (0.033); it bounds a mean bias only loosely | yes | Accepted limitation (section 5). |
| 4 | s_φ is small partly by construction: ∂φ/∂n₆ ≈ 0.28, and n_S and n₅ vary little, so the noisiest input (n₆, s = 0.098) is damped; the 0.037 is not unusual precision | yes ((n̄_S − n̄₅)/Ē² = 0.28) | Accepted (section 5). |
| 5 | The low-shift gate reuses R6's gate seeds (10–12) and `sample_seed_offset` (1000), so its draws are R6's gate draws with the curved pair moved, not an independent realisation | yes (`PARAMS["r6_gate"]`, `results/r6_shuf.json` `settings.gate_low`) | Accepted; noted here. As registered (section 2.8 uses R6's gate distribution and seeds). |
| 6 | kNN in the run: φ = 0.64 at k = 100 (0.58–0.70 per seed) but 0.45 at k = 20 (mean of the per-seed values, 0.12–0.89; 0.46 from the means); section 2.8's kNN expectation at k = 20 rested on one seed | yes | Accepted (section 5 states it). kNN stays descriptive. |
| 7 | Shuffling replaces the joint distribution by the product of marginals; φ measures what that does to the difference, not which DES parameters carry the correlation or whether low Σmν moves DES away from the CMB | – | Accepted (section 5); the label's wording is kept. A no-flow check of DES's conditional (A_s, Ωm) means in Σmν bins is part of T-047. |
| 8 | (SS) ≈ (S) and (P) ≈ n₅, so the "shuffle, then prior" order shows no artefact; the (P) range equals both chains' header range; shuffling keeps the Σmν range the flow's `ranges` bijector sees | yes | None. |
| 9 | Process: the low-shift gate point was chosen near the expected n_S, which came from kNN numbers already seen | yes (section 2.8 states it) | Already on record in section 2.8; a calibration point, not a decision threshold. |
| 10 | Literature: Raveri & Doux 2021 (arXiv:2105.03324) report flow/KDE shift estimators agreeing with the exact tension within about 0.5σ in difficult cases, usually 0.2σ or better (the referee's web search; not checked by us); Lemos et al. 2021 (arXiv:2012.09554, not read) | no | Context only; not used. |
| 11 | Most important next test: a known-answer test of φ itself (a synthetic family in which the Σmν-like box is correlated with the curved pair on the "DES" side, exact n₆, n_S and n₅ known; recover φ within about 0.05 with the same pipeline), and first, without flows, DES's conditional (A_s, Ωm) means in Σmν bins against the CMB | – | Registered as T-047. |

## 7. Open questions

1. The full-space 1.8σ: R6 (2026-11-18) brackets it at 1.6–1.9σ but is not evaluable because one flow
   training scatters by about 0.1σ. A verdict would need a new, pre-registered estimator whose
   scatter is measured first (for example the mean of more trainings, or a flow ensemble).
   R6-NOMNU (2026-11-18) shows that most of it goes with Σmν (0.52σ without Σmν), and the referee's
   checks that this is Σmν jointly with its DES correlations and partly the prior shape (section 6;
   pre-registered check T-044), so a verdict on the data-constrained pair (A_s, Ωm) (R6 flow 0.40σ)
   matters more than a sharper 6-D number. R6-SHUF's pre-registered label (T-044, 2026-11-20) is that
   the Σmν part is mainly DES's own Σmν correlations (φ̄ = 0.67); R6-SHUF itself does not show which DES parameters carry them.
   Its referee (post hoc) found the label near the edge of what the gates certify (bias-corrected
   I_φ = [0.601, 0.669]); a known-answer test of φ is registered as T-047. Its no-flow first part
   (conditional means, 2026-11-20, post hoc; section 5) finds DES's Σmν tied linearly to the other
   five parameters jointly (R² = 0.87), not to one of them, and in the lowest Σmν bin (A_s, Ωm) mean
   offsets similar to the marginal ones (descriptive; not a test of φ).
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
| `r6_retrain`, `r6_nomnu_retrain` | `False`: R6 / R6-NOMNU are not retrained; the recorded `results/r6.json` / `results/r6_nomnu.json` are checked and reused (README 2.7, 2.8) | keep `False` (`True` retrains for hours) | cache only |
| `r6_shuf` | run R6-SHUF (README 2.8): flows on DES's Σmν column shuffled (S), drawn from the prior (P) and both chains shuffled (SS) | `False` skips it (about 4 h of flows in venv-tf); it defaults to `True` and its job folder is deleted after a finished run, so pass `--set r6_shuf=False` when exploring other keys, or every run retrains | cache only |
| `r6_shuf_seeds`, `r6_shuf_seed_offsets` | R6-SHUF seeds k (paired with R6 and R6-NOMNU) and the offsets of the (S), (P), (SS) generators | the registered `[0..4]`, `[1000, 2000, 3000]` | cache only |
| `r6_shuf_s_max`, `r6_shuf_e_min`, `r6_shuf_band` | R6-SHUF label rules 4–6 (changing them is not the registered label) | – | cache only |
| `r6_shuf_gate` | low-shift gate: curved-pair means and the recorded exact n_σ | – | cache only |
| `r6_shuf_prior`, `r6_shuf_knn_k` | Σmν prior range used by (P); k of the descriptive kNN values | prior from the chain headers; k 10–200 | cache only |

- Rerun with an override: `python -m astrolab explore 008-m03-s8-des-y6-cmb-parameter-difference --tag <topic> --set KEY=VALUE`
  (outputs in `explore/<date>-<topic>/`, not committed; about 70 s from cache with `--set r6_shuf=False`).
- Analyses `run.py` does not cover: a script `explore/<name>.py` with `def main(ctx)`, run with
  `python -m astrolab explore 008-m03-s8-des-y6-cmb-parameter-difference --tag <topic> --script explore/<name>.py`.
  Existing: `explore/estimator_calibration.py` (the synthetic calibration of the estimator);
  `explore/referee_checks.py` (post hoc: Gaussian by parametrization, chain-row bootstrap, R5 with modes).
- Results files and keys: `results/formats.json` (step A: headers, column maps, row counts);
  `results/r1.json` (per chain: `mean`, `lo`, `hi`, `equal_lo`, `equal_hi`, `kde_mode`, `verdict`,
  `chain` diagnostics); `results/r2.json` (`1d`, `2d`: `n_sigma`, `s`, `per_seed`,
  `bandwidth_variants`, `verdict`; `support`; `gaussian_means`; `gaussian_modes`;
  `truncated_sensitivity`); `results/r3.json`; `results/r4.json` (`projection_shift`, `map_shift`,
  `algorithms_1d`, `threshold`, `full_space`); `results/r5.json` (per probe `n_sigma`);
  `results/r6_shuf.json` (R6-SHUF: `label`, `reason`, `numbers` (`phi_bar`, `s_phi`, `interval`),
  `quantities` (per seed E, φ, ψ, ρ, φ_χ²), `means`, `flows` (`gate_low`, `S`, `P`, `SS`,
  `determinism`), `knn`, `records`, `environment`, `flags`).
- Example questions: "what if the CMB were shifted by 1σ?" -> a script that shifts the CMB samples;
  "how does KiDS-Legacy's 0.815 mode (not the mean) compare?" -> `--set` on `probes`.
- Findings that change what we know go into `log.md` (and, for a paper study, the wiki article)
  on a branch.

