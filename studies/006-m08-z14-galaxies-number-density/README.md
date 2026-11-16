# M8 z ~ 14 galaxies: number density and the UV scatter a constant-efficiency model needs

> Sections 1-4 were written on 2026-11-15 BEFORE run.py and before any computation
> (pre-registration; derived from part 3 of the wiki article
> [Study-006](https://github.com/sudoghut/astrolab/blob/main/docs/wiki/Study-006-z14-galaxies-number-density.md)
> and design plan 015). Later edits to them must carry a dated note.

## 1. Question

Naidu et al. 2026 (OJAp 9, arXiv:2505.11263; "N26") infer, from two spectroscopically confirmed
galaxies (MoM-z14 and JADES-GS-z14-0) in 388 arcmin², a number density log φ = −5.36 (+0.37/−0.45)
Mpc⁻³ mag⁻¹ at z = 14–15, −21 < M_UV < −20, and say a pre-JWST LF they construct in the framework
of Shen et al. 2023 (arXiv:2305.05679; "S23") underestimates it by ≈ 200× (182, +329/−105) and "is
disfavored at high confidence". With numpy/scipy and paper values only:

1. **R1.** Do N = 2, V = 462,648 Mpc³ and Gehrels Poisson limits give N26's log φ and errors, and
   does the volume follow from 388 arcmin² and z = 14–15 in Planck 2018 cosmology? What is the
   Poisson tail probability of ≥ 2 sources under N26's baseline (and at a ratio of 100)?
2. **R2 (comparison, not a reproduction of N26's baseline).** What does an independent
   constant-star-formation-efficiency (SFE) halo model, calibrated on a pre-JWST z ≈ 8 LF, predict
   in the same bin, compared with N26's baseline (φ_obs/182)?
3. **R3.** With that model's median relation fixed, what UV scatter σ_UV at z = 14–15 reproduces
   φ_obs, compared with N26's "≈ 1.5–2 mag"?
4. **R4 (context).** How does H25's z ~ 14 point relate to N26's?
5. **R5 (exploration).** How do the model ingredients move R2 and R3?

The Lean argument (`argument/`) decomposes N26 §4.1. This study checks its `mod_poisson` bound
numerically (R1) and explores the gaps `gap_poisson` and `gap_area` (section 8); it does not test
`gap_rule`.

## 2. Hypotheses and decision criteria

Tolerances are fixed here and are not changed after results are seen. Each criterion reports a
verdict, the numbers, and our explanation of any failure.

**R1 (number density).**
- φ_obs = N/(V Δm) with N = 2, V = 462,648 Mpc³ (N26), Δm = 1 mag. Errors from Gehrels 1986 one-sided
  84.13% limits: λ_lo = ½ χ²_{0.1587}(2N), λ_hi = ½ χ²_{0.8413}(2N + 2). **Reproduced** if
  |log φ − (−5.36)| < 0.01 and each of the two errors is within 0.05 dex of +0.37 and −0.45.
- Volume: V' = (388 arcmin² as a solid angle) × ∫_{14}^{15} dV_c/dz/dΩ dz with astropy `Planck18`.
  **Reproduced** if |V'/462,648 − 1| < 0.05.
- Poisson tails (reported; checks the Lean `mod_poisson` bound): `p_tail_n26_ppm` = 10⁶ P(N ≥ 2 |
  μ = 2/182) and `p_tail_ratio100_ppm` = 10⁶ P(N ≥ 2 | μ = 2/100); both must be ≤ 200 for the bound
  to hold as encoded (if not, the Lean premise is false and is reported as such).
- The errors are Poisson only (no cosmic variance, no completeness); stated with the result.

**R2 (constant-SFE prediction; fiducial verdict conditional on the fiducial model).**
φ_N26 = φ_obs/182 = 2.375 × 10⁻⁸ Mpc⁻³ mag⁻¹. With φ_ours from section 4 (fiducial combination):
- **"same order as N26's baseline"** if 1/3 ≤ φ_ours/φ_N26 ≤ 3; otherwise **"higher"** or
  **"lower"** (by the factor). This is a model-to-model comparison; agreement is not a validation
  of N26's baseline.
- **Robustness:** the same verdict is computed for every combination of the variant grid
  (section 4, step 7), over the evaluable combinations only (the number not evaluable, and why, is
  reported). **"robust"** if at least 48 of the 72 combinations are evaluable and all evaluable ones
  give the same verdict as the fiducial; otherwise **"calibration-dependent"** (or **"not
  assessable"** if fewer than 48 are evaluable), with the fraction of variants per verdict and the
  envelope (min, max) of φ_ours.
- N26 does not give its baseline's σ_UV numerically ("low UV variability"), so part of any ratio
  may come from a different scatter; φ_ours at σ = 0.5 and 0.9 (the σ_cal variants) is reported
  next to the fiducial ratio.
- Reported (descriptive): P(N ≥ 2 | μ = φ_ours × V × 1 mag) for the fiducial model and its
  envelope over variants.

**R3 (required σ_UV; conditional on R2's model).**
Median relation fixed (fiducial calibration); σ at z = 14–15 varied on [0.7, 4.0] mag. Solve
φ_model(σ) = φ_obs (central value, primary result) and = φ_obs × λ_lo/2 and φ_obs × λ_hi/2 (Poisson
bounds). If φ_model(0.7) ≥ a target, that end is reported as "σ ≤ 0.7" (equality gives σ = 0.7);
if φ_model(4.0) < it, "σ > 4.0" (equality gives σ = 4.0). Censored ends enter the overlap test
as the half-open intervals they denote.
- **"consistent with N26"** if [σ(lower bound), σ(upper bound)] overlaps [1.5, 2.0] mag; otherwise
  **"different"**. Reported with the R2 verdict it is conditional on, and with the envelope of the
  central σ over the variant grid. R3 is **"robust"** if at least 48 of the 72 combinations are
  evaluable and every evaluable one gives the same overlap verdict as the fiducial; a combination is
  not evaluable if its calibration fails or φ(σ) is not monotonic on [0.7, 4.0]; censored roots
  ("σ ≤ 0.7", "σ > 4.0") are evaluable and enter the overlap test as half-open intervals; the counts
  of each case are reported.
- The roots at large σ depend on the lowest halo mass included; the verdict uses the roots at the
  fiducial floor M_min, and the roots at 10 M_min are descriptive (a verdict that would change
  under 10 M_min is reported, not substituted).
- S23's 2.0 mag (z ≈ 12) and 2.5 mag (z ≈ 16) are descriptive comparisons.

**R4 (context, no criterion).** H25 Table 2, z ~ 14 bin (13.5–15.0), M = −20.8:
Φ = 3.7 (+8.7/−3.6) × 10⁻⁵, from Robertson et al. 2023, containing only JADES-GS-z14-0 (shared with
N26), errors including cosmic variance. Reported: Φ_H25/φ_obs, and the area ratio (≈ 10 arcmin²
against 388 arcmin²).

### Addendum 2026-11-16: R2/R3-POST, calibration on binned z ≈ 8 data with errors (T-025, plan 022), pre-registered before any fit to the binned data

*Why.* The referee (section 6) found that moving any one of Bouwens et al. 2021's z ~ 8 Schechter
parameters by 1σ flips R3, and φ* − 1σ flips R2: the fiducial verdicts rest on a calibration whose
uncertainty was never propagated. This addendum calibrates on the binned luminosity function (LF)
with its errors and reports the probability of each verdict.

*Seen before this addendum.* All results in sections 5-6 (fiducial R2 "higher", ratio 9.4; R3
central σ 1.38 mag, "consistent"; the variant grids; the referee's 1σ flips; the exploration
`explore/lf_uncertainty.py`). The binned tables were read while verifying them, including Bouwens et
al. 2022's Fig. 4 (lensing points against Bouwens+21); no fit to the binned data has been made.

*Data (verified 2026-11-16 against the PDF tables).*
- Blank fields: Bouwens et al. 2021 (arXiv:2102.07775) Table 4, z ~ 8 column, all 7 rows: M_1600 =
  −21.85, −21.35, −20.85, −20.10, −19.35, −18.60, −17.60 with φ = 0.000003 ± 0.000002, 0.000012 ±
  0.000004, 0.000041 ± 0.000011, 0.000120 ± 0.000040, 0.000657 ± 0.000233, 0.001100 ± 0.000340,
  0.003020 ± 0.001140 Mpc⁻³ mag⁻¹.
- Lensing fields: Bouwens et al. 2022 (arXiv:2205.11526) Table 4 ("Binned determinations"), z ~ 8
  column, the 8 rows brighter than −15.0 mag: −18.75 0.0018 (+0.0006/−0.0006), −18.25 0.0016
  (+0.0007/−0.0007), −17.75 0.0037 (+0.0012/−0.0012), −17.25 0.0058 (+0.0023/−0.0020), −16.75 0.0063
  (+0.0040/−0.0030), −16.25 0.019 (+0.013/−0.008), −15.75 0.016 (+0.018/−0.011), −15.25 0.014
  (+0.026/−0.011). Its footnote: no magnification-map uncertainty is included, and its errors include
  a size–luminosity systematic. The fainter rows (−14.75 upper limit < 0.068 at 1σ, −14.25, −13.75,
  −13.25) are not used in the primary fit: the missing magnification uncertainty matters most there,
  the values are erratic (0.11, 0.53, 0.20) and one is a limit; they enter a sensitivity fit. (At the
  section 5 fiducial θ these magnitudes map to halo masses of about 10^9.1–10^9.7 M☉, well above the
  10⁸ M☉ floor.)
- The paper allows a 20% uncertainty in the relative normalisation of blank-field and cluster LFs
  at z ~ 8 (its §3.3.2); this enters as a nuisance factor.

*Model and likelihood.* Fiducial combination of section 4 (Sheth–Tormen, Fakhouri mean accretion,
ε extrapolation "dpl", σ_cal = 0.7 mag, z_cal = 7.9). Parameters θ = (ε₀, log10 M₁, β, γ) with flat
priors on the section 4 bounds ([10⁻⁶, 1], [9, 13], [0, 3], [0, 3]) and f (the lensing-field
normalisation factor) with a Gaussian prior N(1, 0.2) truncated to f > 0. The model φ(M_UV) is
`lf_model` at the bin centre (point evaluation; the bins' widths are 0.5 mag except where the
printed centres are 0.75-1.0 mag apart, so this is an approximation stated as such). Each point
contributes a two-piece Gaussian in φ: (φ_data − φ_model)/σ with σ the upper error if φ_model >
φ_data and the lower error otherwise; lensing-field points compare f·φ_model with the data. Stated
approximations: independent Gaussian errors (the stepwise bins may be correlated and the brightest
hold few sources); the papers' cosmology (H0 = 70, Ωm = 0.3) is not converted to Planck18 (about 10%
in φ and 0.07 mag, shared with the section 4 calibration). The blank-field and lensing points are
disjoint samples (blank fields and HFF parallels against the HFF cluster fields).

*Sampling.* Start: scipy `least_squares` on the residuals of the same likelihood plus the prior
residual (f − 1)/0.2, from (0.1, 11.5, 1.0, 0.5, f = 1), bounds the prior box and f ∈ [0.01, 3],
loss "linear", ftol = xtol = gtol = 10⁻¹⁰, max_nfev = 2000. emcee (stretch move), 32 walkers started
at the optimum plus N(0, (10⁻³ × (hi − lo))²) per parameter (for f, hi − lo = 2.99), each coordinate
reflected into its prior box; 6000 steps; the first 2000 discarded; one `np.random.default_rng(0)`
generator drives the start ball and is passed to emcee (`EnsembleSampler(..., seed=...)` from it) so
the chain is reproducible. Valid if the
post-burn length is at least 50 integrated autocorrelation times, τ from
`emcee.autocorr.integrated_time` (c = 5, tol = 0) on the post-burn chain, maximum over the five
parameters; otherwise R2/R3-POST are **not evaluable** (no step changes allowed). Fit quality: the
χ² at the optimum (15 points, 5 parameters with the f prior as one more point: 11 degrees of
freedom); if P(χ²₁₁ ≥ χ²) < 0.01 the result is labelled **"model misfit"** and the probabilities are
reported but not used as a verdict. The section 4 rms rule does not apply here.

*Propagation.* 500 posterior draws: emcee's flattened post-burn chain (step-major order, N = 4000 ×
32) at indices `np.linspace(0, N − 1, 500).round().astype(int)`. For each: R2
ratio φ_ours/φ_N26 and its section 2 verdict (factor 3), and R3's roots and overlap verdict (section 2
rules, same σ grid and censoring). A draw whose φ(σ) is not monotonic is "not evaluable" for R3.

*Decision.* For R2: P(higher), P(same order), P(lower) over the 500 draws. **"robust to the
calibration uncertainty"** if one verdict has P ≥ 0.95 (naming it); otherwise **"calibration-
uncertain"** with the probabilities. For R3 the same with P(consistent), P(different) over the
evaluable draws, which must be at least 90% of the 500 (else **not evaluable**). The section 5
fiducial verdicts stay recorded unchanged; R2/R3-POST is a sensitivity result, conditional on the
fiducial ingredients (in particular the "dpl" extrapolation of ε below the calibrated range, which
decided R3 across the section 4 variants); "robust" here means robust to the LF calibration
uncertainty only. The fraction of draws within 1% of the box width of each prior bound is reported
(for ε₀ measured in log10 ε₀ over [−6, 0], i.e. 0.06 dex; the other parameters linearly); if more
than 5% of draws sit at any bound, the result is labelled **"prior-bounded"**: the verdict stands,
with the label attached. Precedence: "not evaluable" (convergence, or R3 with fewer than 90%
evaluable draws) replaces any verdict; otherwise "model misfit" means the probabilities are reported
but not used as a verdict; "prior-bounded" is attached to whatever remains.

*Reported, not decisive.* Posterior medians and 68% intervals of θ and f; the best-fit χ² and the
number of points; the ratio and R3 central root at the posterior median θ; the same probabilities
for σ_cal = 0.5 and 0.9 (separate chains; as in section 4 step 7, the z = 14–15 σ used for R2 equals
σ_cal) and for a fit that adds the four faint lensing rows (the upper limit as a one-sided Gaussian,
1σ at 0.068), each with the same sampling, propagation and labels (the faint-row fit has 19 points,
the limit counted as one, plus the prior point, minus 5 parameters: 15 degrees of freedom).

## 3. Data (with size estimate)

| Input | Source | Selection | Est. size |
|---|---|---|---|
| N26 counts, area, volume, density, ratio | arXiv:2505.11263 §4.1 (v2) | N = 2, 388 arcmin², 462,648 Mpc³, −5.36 (+0.37/−0.45), 182 (+329/−105) | < 1 KB, in `inputs.py` |
| Pre-JWST z ≈ 8 and z ≈ 7 UV LFs | Bouwens et al. 2021, AJ 162, 47, arXiv:2102.07775, Table 5 | z ~ 8 (⟨z⟩ = 7.9): M* = −20.93, φ* = 0.09 × 10⁻³ Mpc⁻³ mag⁻¹, α = −2.23; z ~ 7 (⟨z⟩ = 6.8): M* = −21.15, φ* = 0.19 × 10⁻³ Mpc⁻³ mag⁻¹, α = −2.06 | < 1 KB |
| H25 z ~ 14 point | Harikane et al. 2025, ApJ 980, 138, Table 2 | one row | < 1 KB |
| Model constants | Planck 2018 (astropy `Planck18`: H0 = 67.66, Ωm = 0.30966, Ωb = 0.04897, σ8 = 0.8102, n_s = 0.9665); Sheth–Tormen (A = 0.3222, a = 0.707, p = 0.3, δ_c = 1.686; as in Reed et al. 2007 eq. 5); Reed et al. 2007 eq. 11–14; Fakhouri et al. 2010 eq. 2; Dekel et al. 2013 eq. 8; Madau & Dickinson 2014 eq. 10 | – | < 1 KB |

Nothing is downloaded (all values hand-transcribed and verified against the papers on
2026-11-15). Only numpy, scipy and astropy (already installed).

## 4. Method

1. **Cosmology.** astropy `Planck18`. Linear power spectrum P(k) ∝ k^{n_s} T(k)² with the
   Eisenstein & Hu 1998 transfer function including baryon oscillations (eqs. 16–24, with inputs
   from eqs. 2–7, 10–12, 14–15), Ωm = Om0, Ωb = Ob0, T_CMB = 2.7255 K; normalised to σ8 = 0.8102
   (top-hat, R = 8 h⁻¹ Mpc) at z = 0. Linear growth D(z) for flat ΛCDM (integral form, D(0) = 1).
   Units: Mpc and M☉ without h.
2. **σ(M) and halo mass function.** Top-hat σ(M, z) on a grid log10 M_h ∈ [log10 M_min, 14]
   (step 0.02), with M_min = 10⁸ M☉ (about the atomic-cooling limit, virial temperature 10⁴ K, at
   z ≈ 14; halos below it are not assumed to host galaxies),
   k integration in log k over [10⁻⁴, 10³] Mpc⁻¹ (4096 points). dn/dln M = (ρ̄_m/M) f(σ) |d ln σ/d ln M|
   with f from Sheth–Tormen (fiducial) or Reed et al. 2007 eq. 11 with n_eff from eq. 13 (variant).
3. **Galaxies.** Halo growth Ṁ_h (fiducial: Fakhouri et al. 2010 mean, 46.1 M☉/yr (M/10¹² M☉)^1.1
   (1 + 1.11 z) √(Ωm(1+z)³ + ΩΛ)); SFR = ε(M_h) f_b Ṁ_h with f_b = Ωb/Ωm; L_ν(1500 Å) = SFR / K with
   K = 0.63 × 1.15 × 10⁻²⁸ M☉ yr⁻¹ (erg s⁻¹ Hz⁻¹)⁻¹ (Madau & Dickinson 2014, Chabrier); median
   M_UV = 51.595 − 2.5 log10 L_ν (AB). Scatter: M_UV is Gaussian about the median with σ (mag).
   ε(M_h) is a double power law 2ε₀ / [(M_h/M₁)^{−β} + (M_h/M₁)^{γ}] with ε₀ ∈ [10⁻⁶, 1],
   log10 M₁ ∈ [9, 13], β ∈ [0, 3], γ ∈ [0, 3]. The median M_UV(M_h) need not be monotonic: if γ
   exceeds the growth-rate exponent (1.1 for Fakhouri, 1.0 for Dekel), the median turns over at a peak halo mass
   M_peak and fainter medians above it are allowed; the median relation, M_peak and the brightest
   median are reported at z_cal and z = 14.5. The model LF at z is
   φ(M_UV) = ∫ dn/dln M · N(M_UV; M_med(M_h, z), σ) d ln M.
4. **Calibration (deconvolved abundance matching).** At z_cal = 7.9 (fiducial; Bouwens et al. 2021
   z ~ 8 Schechter function) fit (ε₀, log10 M₁, β, γ) by least squares in log10 φ between the model
   with σ = σ_cal = 0.7 mag (fiducial) and the Schechter function on M_UV ∈ [−22.0, −17.0] in
   steps of 0.25 mag (21 points), with scipy `least_squares` from the start (0.1, 11.5, 1.0, 0.5),
   bounds as above (loss "linear", ftol = xtol = gtol = 10⁻¹⁰, max_nfev = 2000; parameters at a
   bound are allowed and reported). The fit must reach rms < 0.05 dex over the 21 points;
   otherwise R2 and R3 are **not evaluable** for that combination (reported). The calibrated
   halo-mass range is defined on the rising branch of the median relation: from the lowest M_h
   whose median M_UV at z_cal is ≤ −17 up to M_peak (or up to the M_h whose median reaches −22 if
   the median is monotonic over the range).
5. **Prediction at z = 14–15.** Same ε(M_h) (frozen), σ = 0.7 mag (fiducial), Ṁ_h at each z. φ_ours
   is the average over M_UV ∈ [−21, −20] (21 points, trapezoid) and over z ∈ [14, 15] (11 points)
   weighted by dV_c/dz (trapezoid).
6. **Required σ (R3).** As step 5 with σ varied; root-finding (brentq) on log φ(σ) − log target;
   φ(σ) is checked to be monotonic on [0.7, 4.0] (step 0.05) before solving; if not monotonic,
   R3 is not evaluable.
7. **Variant grid (R2/R3 robustness; fixed now).** Halo mass function {Sheth–Tormen, Reed et al.
   2007 eq. 11}; halo growth {Fakhouri mean, Fakhouri median (25.3 M☉/yr, (1 + 1.65 z)), Dekel et
   al. 2013 eq. 8 (below)}; calibration {z ~ 8 at z = 7.9, z ~ 7 at z = 6.8};
   σ_cal ∈ {0.5, 0.7, 0.9} mag (the z = 14–15 σ in R2 equals σ_cal); ε extrapolation {the fitted
   double power law; ε held constant below the low-mass edge of the calibrated range at its value
   there, with the fitted double power law kept above it (including above M_peak)}. Dekel et al.
   2013 eq. 8: Ṁ_h/M_h = s (1 + z)^{5/2} with s = 0.030 Gyr⁻¹ × (0.82/σ8) (their s ≃ 0.030 Gyr⁻¹
   for σ8 = 0.82 and the σ8⁻¹ scaling they state; β → 0 as in their eq. 8; Ṁ_h converted to M☉ yr⁻¹
   before it multiplies f_b).
   2 × 3 × 2 × 3 × 2 = 72 combinations. Fiducial: Sheth–Tormen, Fakhouri mean, z ~ 8, σ_cal = 0.7,
   double power law.
8. **Dust.** ε absorbs the z ≈ 8 attenuation (the calibration LF is observed); no dust evolution is
   assumed. (Exploration only: section 8.)

Checks before results: σ8 reproduced to 10⁻³ by the normalisation; the Sheth–Tormen f(σ)
integrates to 1 within 1% over ln σ⁻¹ ∈ [−20, 3] (the low-σ⁻¹ tail converges slowly; over
[−3, 3] it reaches only about 0.76); the mass function at z = 0 is compared with the
Sheth–Tormen analytic limit (descriptive).

Systematics to keep in view: the S23-type baseline of N26 is not public in detail, so R2 compares
two constructions; the z ≈ 8 calibration constrains ε only over a limited halo-mass range, and the
z = 14–15 bin needs smaller halos than at z ≈ 8 at fixed M_UV (whether their z ≈ 8 medians lie
inside the calibrated range is reported, step 4; at large σ the result depends on ε below the
calibrated range and on M_min); Poisson errors only; completeness and cosmic variance not
modelled (section 8).

## 5. Results

Run of 2026-11-15 (`python -m astrolab run 006`, 12 s, no data downloaded; page:
[`web/index.html`](web/index.html)). Checks: σ8 = 0.8102 (normalisation), Sheth–Tormen
normalisation 0.9998 over ln σ⁻¹ ∈ [−20, 3]. The pre-registered z = 0 mass-fraction comparison
(0.490 both ways) compares two forms of the same integral and is therefore not informative.

| Criterion | Result | Verdict |
|---|---|---|
| R1 number density | log φ = −5.364 (+0.365/−0.451); Gehrels 0.708–4.637 | **reproduced** (N26: −5.36 +0.37/−0.45) |
| R1 volume | 460,463 Mpc³ (ratio 0.995 to N26's 462,648) | **reproduced** |
| R1 Poisson tails (Lean `mod_poisson`) | 59.9 ppm at ratio 182; 197.4 ppm at ratio 100 | bound **holds** (≤ 200 ppm) |
| R2 constant-SFE prediction (fiducial) | φ_ours = 2.24 × 10⁻⁷ Mpc⁻³ mag⁻¹, 9.4 × N26's baseline (2.38 × 10⁻⁸); P(N ≥ 2) = 0.005 | **higher** (conditional on the fiducial model) |
| R2 robustness | 72/72 evaluable: 61 "higher", 11 "same order"; envelope 2.5–37 × N26's baseline | **calibration-dependent** |
| R3 required σ_UV (fiducial) | central 1.38 mag; Poisson bounds 1.15–1.57 mag (10 M_min: 1.38, 1.15–1.60) | **consistent with N26** (overlaps 1.5–2.0) |
| R3 robustness | 72/72 evaluable, none censored: 38 consistent, 34 different; uncensored envelope of the central σ 1.07–1.60 mag | **calibration-dependent** |
| R4 (context) | H25's z ~ 14 point is 8.6 × φ_obs; area ratio about 39 | – |

Fiducial calibration (Bouwens et al. 2021 z ~ 8, σ_cal = 0.7): ε₀ = 0.016, M₁ = 10^11.55 M☉, β = 0.21,
γ = 1.98 (no parameter at a bound), rms 0.004 dex (all 72 variants ≤ 0.015 dex). The median
relation is not monotonic (γ > 1.1): brightest median −20.64 at M_peak = 10^11.64 M☉ at z = 7.9 and
−22.15 at z = 14.5; calibrated range 10^10.24–10^11.64 M☉. At z = 14.5 halos with medians in
[−21, −20] span 10^10.70–10^12.84 M☉ (the upper part on the falling branch above M_peak), so the
pre-registered flag "inside the calibrated range" reads false; weighted by abundance, a fraction
1.000 of them is inside (the falling-branch halos are about 10⁻¹³ as abundant).

What drives the variants (ratio to N26's baseline; central σ): the scatter σ_cal (0.5: 2.5–9.4×,
1.07–1.53 mag; 0.9: 5.9–37×, 1.16–1.60 mag), the halo mass function (Sheth–Tormen 6.6–37×, Reed et
al. 2007 2.5–16×; all 11 "same order" R2 variants use Reed et al. 2007) and the extrapolation
("dpl": 2.5–19×, 1.33–1.60 mag; "const": 2.5–37×, 1.07–1.39 mag), which decides R3 ("dpl" 36/36
consistent, "const" 2/36). The growth-rate fit and the calibration redshift matter less.

Reading. The number density follows from the two sources and the stated volume. An independent
constant-SFE model, calibrated on the pre-JWST z ≈ 8 LF, predicts about 9 times more such galaxies
than N26's baseline in the fiducial set-up (2.5–37 times across the variants); with it, two sources
in the survey have a Poisson probability of about 0.5% rather than 6 × 10⁻⁵. So N26's factor of 182
depends strongly on how the pre-JWST baseline is built, but in most variants the observed density
still exceeds a constant-SFE prediction. The scatter that this model needs, about 1.4 mag (1.1–1.6
across variants), is at the low end of or below N26's 1.5–2 mag; whether it overlaps depends on the
variant. The R3 "consistent" verdict rests on the upper Poisson root (1.57 mag); the central value
is 1.38 mag.

**After the independent referee (post hoc, explorations; 2026-11-15).** Neither fiducial verdict is
stable against the uncertainty of the calibration data, which the pre-registration did not
propagate (`explore/lf_uncertainty.py`, one Bouwens et al. 2021 z ~ 8 parameter at a time by its
1σ error): φ* −1σ gives ratio 1.9 ("same order") and σ 1.70 [1.47, 1.90]; φ* +1σ gives 35 and
1.10 [0.85, 1.29] ("different"); M* ±0.28 gives 4.6–18.7 and flips R3 with the sign; α ±0.20 gives
4.1–22 and flips R3. Removing a uniform z ≈ 8 dust attenuation of 0.3 (0.5, 1.0) mag gives ratio
20 (31, 99) and σ 1.24 (1.15, 0.88) mag, R3 "different": any dust correction moves R3 away from N26.
The robust statement is therefore narrower: an independent constant-SFE model calibrated on the
pre-JWST z ≈ 8 LF predicts more z = 14–15 galaxies than N26's baseline (2.5–37× across the pre-registered variant grid, mostly > 3×; 1.9–99× including the post-hoc explorations), and the
σ_UV it needs lies around 1–2 mag, with no stable verdict on overlap with N26's 1.5–2 mag.

## 6. Referee notes

Independent referee (2026-11-15; a subagent given the code, pre-registration and results, not our
reading). It checked the physics line by line and found no code bugs. Triage:

1. **z ≈ 8 LF uncertainty not propagated (accepted; dominant).** Verified with
   `explore/lf_uncertainty.py` (section 5): ±1σ in φ*, M* or α flips R3; φ* −1σ also flips R2 (ratio 1.9, "same order"); removing z ≈ 8 dust raises the ratio (R2 stays "higher") and flips R3. The fiducial
   verdicts stand as pre-registered but are not robust to the calibration data; the follow-up is a
   calibration against binned z ≈ 8 data with errors and posterior propagation (TODO T-025).
2. **R3 is driven by halos below the calibrated range (accepted).** At σ ≈ 1.4 most of the bin's
   galaxies come from halos of 10^9.3–10^10.2 M☉, whose z ≈ 8 medians are fainter than −17; hence the
   "dpl"/"const" axis nearly decides R3. The 10 M_min test does not probe this.
3. **Halo mass function in the extreme tail (accepted limitation).** ν ≈ 5–7: a 1–2% error in σ(M)
   changes n by tens of percent; Sheth–Tormen is known to overpredict rare halos at high z (Reed
   07 lowers the ratio by 2.5–4×; all 11 "same order" variants use it).
4. **The accretion variants are nearly redundant (accepted).** After calibration the three fits
   scale almost identically from z = 7.9 to 14.5 (ratios 9.4 / 9.8 / 9.3), so that axis adds little
   independent spread; an extended-Press–Schechter rate would be a real alternative.
5. **Dust (accepted; verified).** Any z ≈ 8 dust correction moves R3 away from N26 (section 5).
6. **Non-monotonic median (harmless).** Capping γ ≤ 1.1 changes the ratio to 9.7 and σ to 1.41
   (referee's check); the bin is fed by rising-branch halos (abundance fraction inside the
   calibrated range 1.000, now reported).
7. **SFR → L_UV at low metallicity (accepted limitation).** Young, metal-poor populations have a
   1.5–2× lower K, which acts like dust removal.
8. **R3 is not like for like with N26 (accepted).** Our model starts 9.4× above N26's baseline, so
   it needs a ×19 boost where N26's needs ×182; overlap with 1.5–2 mag is not a check of N26's number.
9. **Reporting.** The z = 0 mass-fraction check compares the same integral twice (stated in
   section 5); the "inside the calibrated range" flag is misleading without the abundance weight
   (added); the R3 verdict rests on the upper Poisson root (stated). The commit that changed the
   "const" rule (49b81c7) came after the gate-1 orientation numbers; the change was structural (the
   rule was ambiguous for a non-monotonic median) but it concerns the axis that decides R3, which we
   disclose here.
10. **Lean (accepted).** A fourth gap, `gap_bin`: the bin z = 14–15, −21 < M_UV < −20 was drawn
    around the two detections (look-elsewhere effect). The other premises were checked against
    their quotes and are no stronger.

## 7. Open questions

- Propagate the z ≈ 8 LF uncertainty (binned data with errors, including faint lensing-field
  points that constrain ε at 10^9–10^10 M☉) into distributions of the R2 ratio and the σ roots
  (T-025).
- How large is cosmic variance for two sources in 388 arcmin² at z ≈ 14 (`gap_poisson`), and what is
  the full effective area (`gap_area`)?

## 8. Exploring via chat

How a coding agent answers "what if" questions about this study without touching `results/`
(rules: AGENTS.md section 2).

| Knob (`PARAMS`) | Meaning | Safe range | Cache only, or new data (size)? |
|---|---|---|---|
| `hmf` | halo mass function | `"st"`, `"reed07"` | no data |
| `accretion` | halo growth fit | `"fakhouri_mean"`, `"fakhouri_median"`, `"dekel13"` | no data |
| `cal` | calibration LF | `"bouwens21_z8"`, `"bouwens21_z7"` | no data |
| `sigma_cal` | scatter at calibration and in R2 (mag) | 0.3–1.2 | no data |
| `eps_extrap` | ε outside the calibrated range | `"dpl"`, `"const"` | no data |
| `completeness` | spectroscopic completeness c (φ_obs → φ_obs/c) | 0.1–1 | no data |
| `area_factor` | effective area / declared area (`gap_area`) | 1–10 | no data |
| (script) dust at z ≈ 8 | planned exploration script `explore/dust_z8.py` (not yet written): remove A_UV = max(0, 4.43 + 1.99 β) (Meurer et al. 1999) at z ≈ 8, with β(M_UV) from Bouwens et al. 2014 (ApJ 793, 115) transcribed and verified in the script. The exploration done so far (`explore/lf_uncertainty.py`) uses a uniform A_UV shift of the z ≈ 8 LF | – | no data |
| `m_h_min` | lowest halo mass included (M☉); values below 10⁸ include halos not assumed to host galaxies | 10⁷–10⁹ | no data |

- Rerun with an override: `python -m astrolab explore 006-m08-z14-galaxies-number-density --tag <topic> --set KEY=VALUE`
  (outputs in `explore/<date>-<topic>/`, not committed; seconds to a minute).
- Analyses `run.py` does not cover: a script `explore/<name>.py` with `def main(ctx)`, run with
  `python -m astrolab explore 006-m08-z14-galaxies-number-density --tag <topic> --script explore/<name>.py`
  (for example a halo-bias estimate of cosmic variance for `gap_poisson`).
- Results files and keys: `results/r1.json` (`log_phi`, `err_hi`, `err_lo`, `volume_mpc3`,
  `volume_ratio`, `p_tail_n26_ppm`, `p_tail_ratio100_ppm`, `verdict_density`, `verdict_volume`,
  `mod_poisson_bound_holds`); `results/r2.json` (`phi_ours`, `ratio_to_n26`, `verdict`, `robustness`,
  `variant_counts`, `envelope_phi_ours`, `envelope_p_tail`, `p_tail_ours`, `phi_ours_by_sigma`,
  `median_shape_zcal`, `median_shape_z14_5`, `checks`); `results/r3.json` (`sigma_roots`, `verdict`,
  `robustness`, `variant_counts`, `envelope_sigma_central_uncensored`, `sigma_roots_10mmin`,
  `verdict_10mmin`); `results/r4.json`; `results/variants.json` (per-combination rows);
  `results/curves.json`.
- Example questions: "what if completeness is 50%?" → `--set completeness=0.5`; "what if the
  effective area is twice as large?" → `--set area_factor=2`; "how much does the halo mass function
  matter?" → `--set hmf=reed07`.
- Findings that change what we know go into `log.md` (and the wiki article) on a branch.
