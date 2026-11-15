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

Filled after running. Link to `web/index.html` and key numbers in `results/`.

## 6. Referee notes

Independent critique: selection effects, systematics, alternative explanations.

## 7. Open questions

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
| `dust_auv_z8` | remove dust at z ≈ 8 only: A_UV = 4.43 + 1.99 β (Meurer et al. 1999) clipped at zero, A_UV = max(0, 4.43 + 1.99 β), with β(M_UV) at z ~ 8 from Bouwens et al. 2014 (ApJ 793, 115), transcribed and verified into `inputs.py` before use; scatter in β ignored; `false` = none | `true` / `false` | no data |
| `m_h_min` | lowest halo mass included (M☉); values below 10⁸ include halos not assumed to host galaxies | 10⁷–10⁹ | no data |

- Rerun with an override: `python -m astrolab explore 006-m08-z14-galaxies-number-density --tag <topic> --set KEY=VALUE`
  (outputs in `explore/<date>-<topic>/`, not committed; seconds to a minute).
- Analyses `run.py` does not cover: a script `explore/<name>.py` with `def main(ctx)`, run with
  `python -m astrolab explore 006-m08-z14-galaxies-number-density --tag <topic> --script explore/<name>.py`
  (for example a halo-bias estimate of cosmic variance for `gap_poisson`).
- Results files and keys (planned): `results/r1.json` (`log_phi`, `err_hi`, `err_lo`, `volume_mpc3`,
  `volume_ratio`, `p_tail_n26_ppm`, `p_tail_ratio100_ppm`, verdicts); `results/r2.json`
  (`phi_ours`, `ratio_to_n26`, `verdict`, `robustness`, `envelope`, `p_tail_ours`);
  `results/r3.json` (`sigma_central`, `sigma_lo`, `sigma_hi`, `verdict`, `envelope`);
  `results/r4.json`; `results/variants.json` (per-combination numbers); `results/curves.json`.
- Example questions: "what if completeness is 50%?" → `--set completeness=0.5`; "what if the
  effective area is twice as large?" → `--set area_factor=2`; "how much does the halo mass function
  matter?" → `--set hmf=reed07`.
- Findings that change what we know go into `log.md` (and the wiki article) on a branch.
