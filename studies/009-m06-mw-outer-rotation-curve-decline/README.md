# M6 Milky Way outer rotation curve: Keplerian decline, mass and systematics

> 中文：[README.zh.md](README.zh.md)

> Write sections 1–4 BEFORE writing run.py (pre-registration). Edit them later only
> with a dated note explaining the change.

## 1. Question

Paper: Jiao, Hammer, Wang et al. 2023, A&A 678, A208, arXiv:2309.00048 ("J23"). Wiki article (the
source of this pre-registration, part 3):
[Study-009-mw-rotation-curve-decline](https://github.com/sudoghut/astrolab/wiki/Study-009-mw-rotation-curve-decline).
Plan: `design/018-plan_*` (rule E0 on error conventions).

J23 derives the Milky Way rotation curve from Gaia DR3 with the equilibrium Jeans equation (Table 3:
18 bins, 9.5–26.5 kpc), reports that a power law fitted beyond 19 kpc rejects a flat curve at 3σ and
is consistent with a Keplerian decline (γ = −0.47 ± 0.15, Sec. 5.3), and, from Einasto-plus-baryon
fits extrapolated to the virial radius, a total mass of about 2 × 10¹¹ M☉ (Table 4).

1. **R1.** Does J23 Table 3 reproduce γ = −0.47 ± 0.15 and the 3σ rejection of a flat curve?
2. **R2 (descriptive).** What dynamical masses do the six fully specified baryon models give when
   fitted to Table 3 with J23's halo, priors and definitions, compared with Table 4?
3. **R3 (exploration).** How sensitive are γ and the masses to coherent, radius-dependent biases of
   the size discussed in the literature?
4. **R4 (descriptive).** How do the J23, Ou et al. 2024 (O24) and Eilers et al. 2019 (E19) curves
   compare, and what does R1 give on O24?
5. **R5 (descriptive).** How much of the mass is measured (inside 26.5 kpc) and how much
   extrapolated, and how does the extrapolation depend on the halo shape?

## 2. Hypotheses and decision criteria

Only R1 carries a verdict. All rules are fixed before any fit is run. Inputs are the transcribed
tables in `data/` (two independent transcriptions, identical digit for digit).

**E0 · Error conventions.** J23 publishes no per-bin statistical errors; Table 3's σ is the combined
statistical and systematic error (Sec. 2.2.5; Sec. 4.1: "error bars account for systematic
uncertainties"). R1 follows J23's power-law test, which uses these combined errors (Fig. 10). R2
uses them too and is therefore descriptive, not a reproduction (eq. 11 speaks of statistical errors,
which are not published).

### 2.1 R1 (verdict)

Fit V(R) = A (R / 1 kpc)^γ to the 8 bins of Table 3 with R > 19 kpc (19.5–26.5 kpc), Gaussian
likelihood with the Table 3 σ as independent errors, flat priors γ ∈ [−10, 5] and A ∈ [0, 10⁵] km/s
(J23 eq. 13 states the flat γ prior; it gives no prior or units for A, and a flat A with R in kpc is
our most literal reading; the upper bound on A truncates γ near −2, far from the data). MCMC with
emcee: 32 walkers started in a Gaussian ball (relative width 10⁻³) around the least-squares
optimum, 6,000 steps, 1,000 burn-in, seed 0; the run must have more than 50 autocorrelation times
after burn-in, otherwise the steps are doubled (once).
- Statistic S = (0 − median γ) / (84th percentile − median), the like-for-like counterpart of J23's
  0.47/0.15.
- **Reproduced** if the median γ lies in −0.47 ± 0.05 **and** S lies in 3.1 ± 0.3. Otherwise **not
  reproduced**.
- **Reading, fixed in advance:** "reproduced" means that J23's numbers follow from the published
  table under a flat prior on A at a 1 kpc pivot, not that the data alone reject a flat curve at
  3σ or more. A reviewer's check while this section was being written (a grid marginalisation on
  `data/j23_table3.csv`, 2026-11-15) found that the likelihood alone prefers γ ≈ −0.40 ± 0.15 and
  that the flat-A prior at a 1 kpc pivot shifts the γ marginal by about −0.07 (a prior-volume
  effect); the verdict rule above was not changed after that check, and the sensitivity runs below
  were added to report it.
- Reported alongside, without verdict: (i) A log-uniform on [1, 10⁵] km/s; (ii) a flat A on [0, 10³] km/s with
  the pivot R_p at the inverse-variance-weighted mean radius of the 8 bins (computed from the table,
  about 22.9 kpc), V = A (R/R_p)^γ; both with the same walker start rule as R1; for each, median
  γ and S. Also P(γ ≥ 0) as a one-sided Gaussian significance; Δχ² between the best flat fit and the
  best power law (one degree of freedom); the leave-one-bin-out S for each of the 8 bins; the 1σ
  interval of γ and whether it contains −0.5.
- Monte Carlo check: rerun with seed 1; if the medians of γ differ by more than 0.01, double the steps
  (once) and report both.

### 2.2 R2 (descriptive)

For each of the six fully specified baryon models (E dJ, E J, E CM, G dJ, G J, G CM) and for B2
(seven fits; parameters in `data/j23_baryons.csv`):
- Discs (thin, thick; for B2 also the cold and warm dust and the H₂ and HI discs of de Salas et al.
  2019, HI as an untruncated double exponential, as de Salas evaluate it, with M = 8.2 × 10⁹ M☉ taken as the total mass of the untruncated disc): ρ = M/(4π H L²)
  exp(−R/L − |z|/H) (J23 eq. 8). Midplane circular speed of each disc:
  V²(R) = 2πG Σ₀ L² R ∫₀^∞ k J₁(kR) / [(1 + k²L²)^(3/2) (1 + kH)] dk, with Σ₀ = 2ρ₀H = M/(2πL²).
  The integral is computed with scipy `quad` on [0, k_max] split at the zeros of J₁(kR), with
  k_max = 200/R and a convergence check (doubling k_max changes V² by less than 10⁻⁶ relative); a
  unit test checks that H → 0 reproduces the Freeman thin-disc formula.
- Bulges: the triaxial E and G bulges as point masses, V² = G M_b / R (at R ≥ 9.5 kpc their enclosed
  fraction exceeds 0.998); the B2 Hernquist bulge with its exact speed, V² = G M_b R / (R + r_b)²
  (r_b = 0.70 kpc; only 87% of its mass lies inside 9.5 kpc).
- Halo: Einasto ρ(r) = ρ0 exp[−(r/h)^(1/n)], M0 = 4π h³ ρ0, enclosed mass
  M_DM(<r) = M0 · n · Γ(3n) · P(3n, (r/h)^(1/n)) (P the regularised lower incomplete gamma function;
  logarithms via `gammaln`). Sampled parameters M0, h and 1/n with **flat priors as J23**:
  M0 ∈ [10¹⁰, 10¹⁴] M☉, h ∈ [0, 20] kpc, 1/n ∈ [0, 5] (a log-uniform M0 is reported as a labelled
  variant for model E dJ). MCMC as in R1 (start around the least-squares optimum), 18 points of
  Table 3, combined errors.
- R_vir and M_dyn: **primary**, J23's stated definition, the radius where the mean dark-matter
  density inside r is 200 ρ_cr (ρ_cr = 1.34 × 10⁻⁷ M☉/pc³ = 134 M☉/kpc³); **secondary**, the mean
  total density (dark matter plus all of M_bar, which is essentially all enclosed at these radii) equal
  to 200 ρ_cr. Posterior samples with no root in the bracket [1, 10³] kpc are counted and reported,
  and the bracket is widened to [1, 10⁴] kpc for them; any still without a root are flagged, not
  dropped silently. M_dyn = M_bar + M_DM(<R_vir) (J23
  Sec. 4.3), M_bar from J23 Table 4. M_dyn and R_vir are computed per posterior sample and summarised
  by the median and 68% interval. Predicted before fitting (from the Table 4 medians, reviewer's
  check): the primary definition gives R_vir ≈ 107 kpc, the secondary ≈ 121 kpc, J23 quotes 121.03
  (+1.80/−1.23) kpc (Sec. 4.3); M_dyn changes by below about 1% between the two, because the halo has
  converged.
- Reported: per model, medians and 68% intervals of M_dyn (both definitions), R_vir (both), n, h,
  M0; differences to Table 4 (M_dyn TW column) and to 121.03 kpc; the mean of the six E/G models
  against the mean of their six Table 4 values, and B2 against 2.05 × 10¹¹ M☉.

### 2.3 R3 (exploration, no verdict)

In every case below both V and σ of the affected bins are divided by (1 − b) (a multiplicative bias
scales the errors too).
- (a) **Constant bias, null control:** b constant. Expected Δγ = 0 exactly; reported as a check. For
  the masses: R2 refitted (model E dJ, primary definition) for b = −0.10, −0.05, +0.05, +0.10.
- (b) **Outer ramp (stress test):** b(R) = 0 for R ≤ 19 kpc, rising linearly to b_max at 26.5 kpc
  (b > 0: observed velocities biased low); b_max from 0 to 0.20 in steps of 0.005; R1 refitted at each
  step (32 walkers, 1,000 burn-in, 2,000 kept steps, seed 0); reported: S(b_max), whether it is
  monotonic, and the first grid value with S < 2 (with the R1 sensitivity runs (i) and (ii) repeated
  at that value). This is an injected stress test, not a robustness verdict; literature bias
  magnitudes (Koop et al. 2024: 10–15%; Ou et al. 2025: 5–20%) are context only.
- (c) **Secondary cases:** the errors of the 8 R1 bins enlarged in quadrature by 5%, 10% and 15% of V
  (double-counting the systematics already in Table 3, labelled as such); and correlated errors in the
  4 bins at R ≥ 23.5 kpc, C_ij = ρ σ_i σ_j with ρ = 0.5 and 0.99, with the full covariance in the
  likelihood; S for each.

### 2.4 R4 (descriptive)

- Overlap: the J23 radii that lie inside the other curve's own range (no extrapolation: for E19,
  9.5–24.5 kpc; for O24, 9.5–26.5 kpc). The other curve's velocity and error are interpolated
  linearly to J23's radii; asymmetric errors are symmetrised as their mean. Difference in units of
  √(σ_J23² + σ_other²). J23's σ includes systematics, O24's and E19's do not (E19's separate 2–5%
  is not added); O24 has sparse bins near 22.7–25 kpc, which interpolation smooths over.
- R1 on O24: the 11 bins with R > 19 kpc (19.22–27.31 kpc), symmetrised errors, the same prior,
  pivot and sensitivity runs as R1; J23's −0.56 (+0.23/−0.22) is compared approximately (J23 does not
  say which O24 bins it used).
- R2 on O24, descriptive: the seven models fitted to O24's bins with R ≥ 9.5 kpc (where the bulge
  approximations hold) with symmetrised errors, compared approximately with Table 4's O23 column (J23
  does not say which O24 bins its fits used). We cannot tell which errors J23 used for O24 (J23 Sec. 4.1 says that
  error bars account for systematic uncertainties in both studies, while O24 publishes no
  systematic-error column), so differences are reported, not judged.

### 2.5 R5 (descriptive)

- For model E dJ (primary R_vir definition): the model-free V²R/G at 26.5 kpc; the enclosed mass
  M(<26.5 kpc) inside a sphere (disc mass inside the sphere by numerical integration, plus the bulge,
  plus the halo); and the extrapolated M(<32.4 kpc), M(<100 kpc) and M_vir (= M_dyn, baryons plus dark matter
  inside R_vir, both R_vir definitions), each with its 68% interval.
- The same for an NFW halo, ρ = ρ_s / [(r/r_s)(1 + r/r_s)²], with E dJ baryons, log-uniform priors
  ρ_s ∈ [10⁴, 10¹⁰] M☉/kpc³ and r_s ∈ [1, 100] kpc, fitted to the same 18 points with the same
  likelihood as R2 (independent Gaussian errors, Table 3's combined σ; MCMC as in R2), with the same R_vir
  rules.
- Order-of-magnitude, cross-model comparison with stream masses: Koposov et al. 2023, (2.85 ± 0.10) ×
  10¹¹ M☉ inside 32.4 kpc; Vasiliev et al. 2021, (5.6 ± 0.4) × 10¹¹ M☉ inside 100 kpc (a model with a
  possibly non-spherical halo and the LMC; not the same mass definition).

### 2.6 R6-COV (addendum 2026-11-17, T-028), pre-registered before any fit with a correlated covariance

Revised the same day after the gate-1 review, still before any such fit.

*Why.* The referee and the post-hoc check (sections 5 and 6) found that Table 3's errors are unlikely
to be independent (best-fit Einasto χ² = 1.30 for 15 degrees of freedom); a χ² this low can also
come from an overestimated error scale, so the χ² alone does not establish correlation. Either way the
independent-error significances are mis-scaled. R6-COV is a sensitivity analysis conditioned on the
chosen χ² target, not a determination of the covariance. *Seen before this addendum:* all R1–R5 results, including the
R3(c) case ρ = 0.99 (S = 6.07, an artefact of a near-singular covariance); the post-hoc χ² values
(Einasto 1.30, NFW 21.1, power law beyond 19 kpc 0.47 for 6); and the referee's numbers in section 6
(with ad-hoc correlated kernels whose forms and amplitudes were not recorded: likelihood-only flat
rejection 2.3–3.7σ, Einasto over NFW Δχ² 11–29; with independent errors: χ² 23.2, 21.0, 15.3, 7.65
for 1/n fixed at 0.17, 0.25, 0.5, 1, and the start-radius results of item 6). No fit with the
covariances below has been run; the gate-1 reviewer computed only kernel eigenvalues.

*Source facts (J23, arXiv HTML read 2026-11-17).* Sec. 2.2.5, Eq. 4 adds the cross-term, scale-length,
density-profile and sample-split systematics in quadrature, and that total, combined with the
statistical errors, "has been adopted to calculate error bars in Figure 2"; the Fig. 4 caption puts
the total systematic "at the 2% level up to R = 22.5 kpc", rising beyond (Sec. 2.2.1: cross-term up to
~8% at 25.5 kpc). Table 3's caption does not state its composition (the Fig. 5 caption says the error
bars include systematics). Table 3's σ/V is 1.35–1.57% at 9.5–13.5 kpc, comparable to that stated
systematic level, so the split of σ into statistical and systematic parts cannot be determined, and
the inner σ is probably mostly systematic. J23 give no per-bin statistical errors. The original
T-028 note (amplitudes from J23 and Koop et al. 2024 added to a statistical part) is therefore not
followed: adding any positive-semidefinite variance on top of σ_i (at fixed residuals) only lowers
χ² further (already 1.30 for 15), so reaching
χ² ≈ degrees of freedom needs correlation within the existing variance. We keep σ_i as the total
error of each bin (our reading of the Sec. 2.2.5 text and the Fig. 5 caption; Table 3's caption is
silent) and only add correlations.

*Covariance family.* Five covariances, each with Table 3's σ_i² on the diagonal:
- four of the form C_ij = σ_i σ_j [(1 − f) δ_ij + f K_ij], f ∈ [0, 0.99], with K the squared-exponential
  K_ij = exp[−(R_i − R_j)²/(2ℓ²)] for ℓ = 2, 4 and 8 kpc (ℓ = 2 kpc is about two bins; 7 kpc is the
  length of the R1 range), or the global K_ij = 1. The correlated error of bin i is then √f · σ_i, so the
  correlated part is shaped like σ itself, which is dominated by the 23.5, 25.5 and 26.5 kpc bins
  (12.95, 19.58, 24.68 km/s against about 4 km/s elsewhere): on the 8 outer bins the global kernel acts
  like an outer ramp, partly degenerate with γ, and favours a weaker flat rejection; the ℓ = 4 and 8 kpc
  kernels less so;
- the fractional kernel, a truly coherent fractional offset: C = diag(σ_i² − c² V_i²) + c² V Vᵀ with
  c ∈ [0, 0.99 · min_i(σ_i/V_i)] (min σ/V = 1.35%, at 10.5 kpc).
No kernel is primary; the family (bin scale, intermediate, range scale, global, and a strictly
fractional offset) was chosen to span the plausible correlation lengths, not tuned to any fit.

*Calibration.* For each covariance the free parameter (f, or c) is set so that the best-fit free
Einasto model (baryons E dJ, the 18 points) has χ² = rᵀC⁻¹r = 15, its degrees of freedom. χ²(f) need
not be monotonic, so: evaluate χ² on the grid f = 0, 0.01, …, 0.99 (c = k · c_max/99, k = 0, …, 99, c_max = 0.99 · min σ/V),
refitting the Einasto model at each point; take the smallest grid value at which χ² ≥ 15 and bisect
inside the cell below it (stop when hi − lo ≤ 10⁻⁴ × the full parameter range, i.e. 0.99 for f or c_max for c;
refitting at each trial): starting from
lo = the grid point below (χ² < 15) and hi = the first crossing (χ² ≥ 15), each midpoint replaces hi if
its χ² ≥ 15 and lo otherwise, and the result is the final (lo + hi)/2 (if χ² crosses 15 more than once
inside one 0.01 cell, this picks one of those crossings; accepted); report the whole
curve. If χ² < 15 on the whole grid, the covariance is "not calibratable": reported at the top of its
range but excluded from the labels. If an Einasto refit fails the convergence rule below at a grid
point, that point is skipped (the first crossing is the first successful grid point with χ² ≥ 15; a skipped
point could hide an earlier crossing, a blind spot reported through the curve); if the grid point just below the
first crossing failed, or a refit fails during the bisection, the covariance is "not evaluable". Also reported, without labels: the same tests at the smallest grid-and-bisection values
with χ² ≥ 15 − √30 and ≥ 15 + √30 (√30 = √(2 · 15) is the standard deviation of a χ² with 15 degrees of freedom; each threshold
found by the same first-upward-crossing procedure as the target), where they exist,
and χ²_min/6 of the profiled 8-bin power law (T1; 8 bins minus A and γ) at the calibrated value (f is calibrated on 18 points, the
power law uses 8). Known biases: calibrating on Einasto makes Einasto fit by construction (T3 is
relative to it). **High-f flag:** at large f the χ² is dominated by small-eigenvalue (bin-to-bin
difference) directions, the artefact seen in R3(c); a covariance is flagged "high-f" if its largest
per-bin correlated fraction exceeds 0.9 at the calibrated value (f itself for the four kernels;
max_i c²V_i²/σ_i² for the fractional one). Order: (1) the label from all calibrated, evaluable
covariances (at least 3 needed, else "not evaluable"); (2) the label from the unflagged ones among those usable covariances alone (with at least 3 of them it
always exists);
if fewer than 3 are unflagged, the label of (1) is reported with the qualifier "(only with high-f
covariances)"; otherwise, if (1) and (2) differ, the label is "kernel-dependent (high-f)", and if they
agree it stands.

*Fits.*
- T1 and T2 (8 bins beyond 19 kpc, sub-block of C): the power law V = A (R/1 kpc)^γ is linear in A, so
  for each γ the amplitude is the generalised-least-squares (GLS) solution and χ²(γ) is the profile;
  χ²(γ) is evaluated on γ ∈ [−3, 1] in steps of 0.001 and its minimum refined by bounded Brent
  minimisation on [γ_(k−1), γ_(k+1)] around the grid minimum γ_k (at an edge, [γ_k, γ_(k±1)]), where
  γ values with A ≤ 0 count as χ² = +∞; the reported minimum is the smaller of the grid and Brent
  values; Brent uses xatol 10⁻⁷ in γ (scipy `minimize_scalar`, method "bounded"); A must be positive (a γ with A ≤ 0 is excluded). The flat model is γ = 0 of the same profile. If the minimum lies at γ = −3 or 1, it is
reported as at the edge and used as is; if γ = 0, −0.2 or −0.5 is excluded (A ≤ 0), T1 or T2 is "not
evaluable" for that covariance.
- Halo fits (18 points, E dJ baryons): free Einasto in R2's parametrisation and bounds (M0, h, 1/n;
  the fitted coordinates are log10 M0, h, 1/n); NFW in R5's (log10 ρ_s, log10 r_s); the ΛCDM-like
  Einasto with 1/n = 0.17 fixed in (log10 ρ₋₂, log10 r₋₂), ρ₋₂ ∈ [10³, 10¹⁰] M☉/kpc³, r₋₂ ∈ [1, 300]
  kpc, converted by h = r₋₂ (0.17/2)^(1/0.17) and ρ0 = ρ₋₂ e^(2/0.17), M0 = 4π h³ ρ0 (R2's bounds on
  M0 and h do not apply to it: a ΛCDM-like halo has M0 far below 10¹⁰ M☉). Nelder–Mead in those
  coordinates (maxiter 20,000, xatol 10⁻⁸, fatol 10⁻¹⁰; χ² = 10³⁰ outside the bounds) from 20 starts
  drawn uniformly in the fitted coordinates themselves (log10 M0 ∈ [10, 14], h ∈ [0, 20], 1/n ∈ [0, 5];
  log10 ρ_s ∈ [4, 10], log10 r_s ∈ [0, 2]; log10 ρ₋₂ ∈ [3, 10], log10 r₋₂ ∈ [0, log10 300]) with a
  fresh `default_rng(0)` created once per fit (one model at one covariance value) and then used for
  its 20 starts in turn (start by start, each coordinate in the order listed drawn with
  `rng.uniform(lo, hi)`), plus one fixed extra start: the starts used for R2 and R5
  (free Einasto M0 = 3.7 × 10¹¹ M☉, h = 12 kpc, 1/n = 2.4; NFW log10 ρ_s = 7.0, log10 r_s = 1.2) and,
  for the ΛCDM-like model, ρ₋₂ = 10⁶ M☉/kpc³, r₋₂ = 20 kpc. The best fit is
  the minimum over all 21 starts; it counts as converged if at least 3 starts that terminate successfully (the optimiser's own success
flag; a run stopped by maxiter does not count) reach within 0.01 in χ² (absolute) of
  that minimum (the minimum is taken over the successful runs with χ² < 10³⁰; none → "not evaluable") (an optimum on a bound is allowed and reported); otherwise the test is "not evaluable" for that covariance. Whether the free Einasto
  optimum lies at a bound is reported.

*Tests at each calibrated covariance.*
- **T1, flat rejection.** Δχ²_flat = χ²(γ = 0) − min χ²(γ); significance √Δχ²_flat (one degree of
  freedom, likelihood only).
- **T2, Keplerian versus γ = −0.2.** D_K = χ²(−0.5) − min χ², D_02 = χ²(−0.2) − min χ²; preference
  D_02 − D_K (positive favours Keplerian).
- **T3, halo shape.** Δχ²_NFW = χ²_NFW − χ²_Einasto and Δχ²_ΛCDM = χ²_ΛCDM − χ²_Einasto (positive: worse than the free
Einasto), and the best-fit M_vir of each
  (primary R_vir definition of section 2.2, plus E dJ's M_bar; reported only). NFW is not nested in
  Einasto, so the thresholds below are conventional evidence levels, not exact 2σ/3σ; nor is the
ΛCDM-like model nested in the bounded free Einasto (R2's bounds exclude 1/n = 0.17 halos), so Δχ²_ΛCDM
can be negative (it then falls in the lowest band).

*Labels, fixed now. Each of T1, T2, T3-NFW and T3-ΛCDM has its own set of usable covariances
(calibrated, and that test evaluable there: T1/T2 need their profile points, T3 needs both its halo
fits converged); at least 3 of the 5 are needed for that test, otherwise "not evaluable"; then the
high-f rule above, applied per test.*
- T1: every covariance √Δχ²_flat ≥ 3 → **"flat rejected at ≥ 3σ"**; every one ≥ 2 and not all ≥ 3 →
  **"flat rejected at ≥ 2σ"**; every one < 2 → **"flat not rejected at 2σ"**; otherwise
  **"kernel-dependent"**.
- T2: every D_02 − D_K ≥ 4 → **"Keplerian favoured over γ = −0.2"**; every one ≤ −4 → **"γ = −0.2
  favoured over Keplerian"**; every |D_02 − D_K| < 4 → **"not distinguished"**; otherwise
  **"kernel-dependent"**.
- T3, separately for NFW and ΛCDM-like: Δχ² in the bands Δχ² < 4, 4 ≤ Δχ² < 9, Δχ² ≥ 9; all covariances in one band →
  **"not disfavoured"**, **"mildly disfavoured"**, **"disfavoured"** respectively; otherwise
  **"kernel-dependent"**.

*Reading.* R6-COV replaces none of the R1–R5 results; it states which readings of section 5 (the
decline's significance, "Keplerian", the preference for a truncated halo) survive once the errors are
allowed to be correlated by an amount that makes the Einasto χ² equal its degrees of freedom. The
kernels are assumptions; the true covariance is not established. For contrast (reported, no label):
T1 and T2 with independent errors rescaled by the factor that makes the Einasto χ² = 15
(σ_i → σ_i · √(1.30/15) with the exact f = 0 χ²), the overestimated-scale reading.

*Runtime.* Some thousands of halo fits of 18 points (100 grid points × 5 covariances with 21 starts
each, plus the bisections), estimated 30–90 minutes; no data downloaded; results in
`results/r6.json`. Switch: `PARAMS["r6_check"]`.

## 3. Data (with size estimate)

| Input | Source (service / URL) | Selection | Est. rows / size |
|---|---|---|---|
| J23 Table 3 | arXiv:2309.00048 HTML, transcribed twice independently | all | 18 rows, 0.3 kB |
| J23 Table 4 | same | all | 8 rows, 1.2 kB |
| J23 baryon parameters (Tables 1–2, Sec. 3.1) | same | all | 45 rows, 2.5 kB |
| O24 Table 1 | arXiv:2303.12838 HTML | all | 37 rows, 1.0 kB |
| E19 Table 1 | arXiv:1810.09466 (ar5iv HTML) | all | 38 rows, 0.9 kB |

No download: all inputs are in `data/` (6 kB in total). Nothing is fetched at run time.

## 4. Method

1. Read the CSVs; check the row counts (18, 8, 37, 38), that Table 3 matches the 206.25 and 175.68
   km/s quoted for 19.5 and 26.5 kpc, and that the component masses of each baryon model sum to its
   Table 4 M_bar (to 0.005 × 10¹¹ M☉).
2. R1: emcee as in section 2.1; Δχ² with scipy optimisation; leave-one-bin-out.
3. R2: as section 2.2; R_vir by root finding (brentq on [1, 10³] kpc).
4. R3–R5 as in sections 2.3–2.5.
5. Summaries only (medians, intervals, statistics, per-bin tables) go to `results/*.json`, each under
   1 MB.

Not tested here: departures from equilibrium themselves (`gap_jeans` in the Lean argument), J23's
systematic error budget, the Gaia sample and its distances.

## 5. Results

Run 2026-11-15 (`python -m astrolab run 009`, 399 s; no downloads). All MCMC runs converged (more than
50 autocorrelation times after burn-in). Page: [`web/index.html`](web/index.html). Numbers from
`results/*.json`; post-hoc items are labelled.

**R1 (verdict): reproduced, under the stated reading.** On the 8 bins beyond 19 kpc with J23's
literal priors (flat γ, flat A at a 1 kpc pivot): median γ = −0.466 (16–84%: −0.614 to −0.318),
S = 3.15 (J23: −0.47 ± 0.15, 3σ); seed-1 check −0.465, S = 3.17. As fixed in advance, this means
J23's numbers follow from the published table under that prior, **not** that the data alone reject a
flat curve at 3σ:
- log-uniform A: γ = −0.402, S = 2.70; flat A at the data's own pivot (21.5 kpc; the
  pre-registration's "about 22.9 kpc" was an arithmetic slip, the rule computes it from the table):
  γ = −0.401, S = 2.72; Δχ² flat versus power law = 7.20 (2.68σ, best γ = −0.397). About 0.45σ of the
  "3σ" comes from the prior on A.
- Leave-one-bin-out (flat A): S between 2.74 and 3.23; the 1σ interval of γ contains −0.5.

**R2 (descriptive).** Einasto plus baryons fitted to the 18 points with Table 3's combined errors:

| Model | M_dyn ours (10¹¹ M☉) | Table 4 | n | R_vir DM-only / total (kpc) |
|---|---|---|---|---|
| E dJ | 1.969 | 1.97 | 0.40 | 106.7 / 120.6 |
| E J | 1.970 | 1.97 | 0.41 | 106.8 / 120.6 |
| E CM | 1.972 | 1.97 | 0.44 | 107.2 / 120.7 |
| G dJ | 1.970 | 1.98 | 0.43 | 107.5 / 120.6 |
| G J | 1.980 | 1.98 | 0.45 | 107.9 / 120.8 |
| G CM | 1.976 | 1.99 | 0.47 | 108.1 / 120.7 |
| B2 | 2.039 | 2.05 | 0.41 | 108.2 / 122.0 |

The six-model mean is 1.973 against Table 4's 1.977. J23's masses are reproduced to within 0.7% using
the combined errors, which supports reading its fit as using them (despite eq. 11). R_vir: J23's
121.03 kpc matches the **total-density** definition (120.6–122.0 kpc), not the dark-matter-only
definition its text states (≈107 kpc), as predicted before fitting; M_dyn is identical under both,
because the fitted halo has converged (n ≈ 0.4: the density falls by a factor of about 10⁻⁷ from
20 to 40 kpc). A log-uniform M0 prior gives 1.975 × 10¹¹ (E dJ). On O24's curve (R ≥ 9.5 kpc,
statistical errors) the seven models give 2.12–2.18 × 10¹¹ against Table 4's O23 column 2.07–2.19.

**R3 (exploration, no verdict).**
- (a) Constant bias: γ unchanged (−0.464 to −0.470, null control passed); M_dyn(E dJ) = 1.61, 1.77,
  2.20, 2.46 × 10¹¹ M☉ for b = −0.10, −0.05, +0.05, +0.10.
- (b) Outer ramp (stress test): S falls monotonically; it drops below 2 at **b_max = 0.06** (a bias
  rising to 6% at 26.5 kpc, about 11 km/s there and 4.0 km/s at 21.5 kpc, smaller than Table 3's
  errors). At that point the log-A and pivot runs give S ≈ 1.5. For context only: Koop et al. 2024
  report Jeans biases of 10–15%, Ou et al. 2025 5–20%.
- (c) Errors enlarged in quadrature by 5/10/15% of V: S = 2.54, 2.38, 2.67 with the flat-A prior, but
  (referee, section 6) the flat-A median γ runs away to −0.69, −1.04, −1.39 and a log-uniform A gives
  S = 1.70, 1.14, 0.81: the prior effect grows with the errors; this case is not evidence of
  robustness. Correlated outer errors: ρ = 0.5 gives S = 2.85; ρ = 0.99 gives 6.07, an artefact of a
  near-singular covariance that pins the differences between the outer bins, not a stronger decline.

**R4 (descriptive).** J23 against O24 (18 radii): χ² = 16.9, the largest pulls at 9.5–12.5 kpc
(−2.5 to −1.0σ, J23 lower); against E19 (16 radii): χ² = 8.2. R1 on O24's 11 bins beyond 19 kpc
(statistical errors only): γ = −0.408, S = 5.4 (log-A 5.3, pivot 5.3, Δχ² 27.6). J23 reports
γ = −0.56 (+0.23/−0.22) for O24, three times wider, so J23 must have used larger errors or other bins
for O24. The three curves share Gaia-based kinematics and equilibrium modelling, so their agreement is
not independent confirmation.

**R5 (descriptive).** E dJ baryons:

| Mass (10¹¹ M☉) | Einasto | NFW |
|---|---|---|
| V²R/G at 26.5 kpc (model-free) | 1.90 | 1.90 |
| M(<26.5 kpc) | 1.97 | 2.33 |
| M(<32.4 kpc) | 1.97 | 2.69 |
| M(<100 kpc) | 1.97 | 5.35 |
| M_vir (DM-only / total R_vir) | 1.97 / 1.97 | 7.05 / 7.16 |

With n ≈ 0.4 the Einasto halo stops growing beyond about 30 kpc: 99.8% of the total M_vir (baryons
plus halo) lies inside 26.5 kpc. The total mass is therefore the measured enclosed mass plus the assumption that the halo
ends there. Stream masses (cross-model, order of magnitude): Koposov et al. 2023 M(<32.4) = 2.85 ±
0.10 is far above the Einasto value and close to NFW's; Vasiliev et al. 2021 M(<100) = 5.6 ± 0.4
likewise.

*Post hoc (2026-11-15, `explore/halo_fit_quality.py`):* best-fit χ² on the 18 points is 1.30 for
Einasto (15 degrees of freedom; p ≈ 10⁻⁶ for being so small) and 21.1 for NFW (16 degrees of freedom,
p ≈ 0.18). The Einasto fit is too good: Table 3's errors cannot be independent per-bin errors (they
include smooth, correlated systematics), so every significance above that treats them as independent,
including R1's, is mis-scaled. Under that same independent-error scaling NFW looks acceptable
(p ≈ 0.18), but the data prefer Einasto by Δχ² ≈ 20, a preference that the referee finds survives
correlated-error kernels (Δχ² 11–29); if the errors were rescaled to make Einasto's χ² equal its
degrees of freedom, NFW would be strongly rejected under that rescaling; since the correct
covariance is unknown (T-028), NFW is disfavoured, not excluded.

**Reading.**
1. *The decline* is reproduced as J23 computed it, but its 3σ depends on the prior on A (2.7σ from the
   likelihood) and on correlated errors that the analysis treats as independent; a 6% outer bias
   would remove it.
2. *"Keplerian"* rests on the 1σ interval of γ containing −0.5; that interval also contains clearly
   non-Keplerian declines.
3. *The total mass* of about 2 × 10¹¹ M☉ is reproduced to 0.7%, but it is the enclosed mass at 26.5 kpc
   (1.90 × 10¹¹ from V²R/G) plus a halo shape that ends just beyond the data. The data prefer that
   truncated shape (Δχ² ≈ 20 over NFW), but an NFW (Navarro–Frenk–White) halo, disfavoured (11–29 under the referee's correlated-error kernels) but not excluded, gives 7 × 10¹¹ M☉ and
   agrees with the stream masses; which shape is right is what T-028 tests.

## 6. Referee notes

Independent referee, 2026-11-15 (subagent with the pre-registration, code, data and results only; it
ran checks with the study's own modules; no downloads). Triage:

1. **Table 3's errors cannot be independent** (the most serious point). Best-fit χ² = 1.30 for 15
   degrees of freedom (Einasto) and 0.47 for 6 (power law beyond 19 kpc). *Accepted*; confirmed post
   hoc (`explore/halo_fit_quality.py`) and stated in section 5. All significances that treat the σ as
   independent are mis-scaled; with ad-hoc correlated kernels the referee finds a likelihood-only flat
   rejection of 2.3–3.7σ. The proper test (a physically motivated full covariance) is registered as
   T-028.
2. **The 3σ is partly a prior effect.** *Accepted*; already fixed in the pre-registration and
   reported (likelihood alone 2.7σ; log-A and pivot runs 2.70 and 2.72). The referee adds that under
   the quadrature cases the flat-A median runs to γ = −0.69, −1.04, −1.39, while log-A gives S = 1.70,
   1.14, 0.81: R3(c) is not evidence of robustness (section 5 says so).
3. **The total mass is set by the halo shape.** *Accepted*. The fitted Einasto halo (1/n ≈ 2.5) has a
   density slope of −8.7 at 20 kpc and −17 at 26.5 kpc; 99.8% of M_vir lies inside 26.5 kpc. With
   1/n fixed at 0.17 (ΛCDM-like), 0.25, 0.5 and 1 the referee finds χ² = 23.2, 21.0, 15.3, 7.65 and
   M_vir = 8.1, 5.7, 3.3, 2.3 × 10¹¹ M☉.
4. **NFW is acceptable on its own** (χ² = 21.1 for 16, p = 0.18); its rejection relative to Einasto
   (Δχ² ≈ 20) relies on independent errors; the Einasto preference survives the referee's correlated
   kernels (Δχ² 11–29). *Accepted*; NFW M_vir = 7.1 × 10¹¹, close to Eilers et al. 2019's NFW value
   (recalled by the referee, unverified).
5. **Stream masses** favour NFW (within 1.6σ and 0.6σ) over the truncated Einasto (about 9σ low).
   *Accepted*, as a cross-model, order-of-magnitude comparison.
6. **Start radius and leverage.** Likelihood-only: R > 14 kpc gives γ = −0.30 ± 0.04 (flat rejected
   at 6.7σ, Keplerian rejected); R > 16 kpc γ = −0.34 ± 0.07; R > 19 kpc −0.40 ± 0.15; R > 21 kpc
   −0.44 ± 0.30 (1.5σ). Dropping the 19.5 or 24.5 kpc bin gives 2.05σ or 2.2σ. *Accepted*: the
   decline is robust to the start radius (under independent errors); "Keplerian" depends on the
   19 kpc cut.
7. **O24 errors.** J23's quoted O24 width is three times ours; the curves share systematics.
   *Accepted*; section 5.
8. **Minor:** the pre-registered "about 22.9 kpc" pivot is 21.5 kpc as computed by the rule
   (arithmetic slip, not a change); the two M_dyn definitions give identical numbers because the
   halo has converged; the leave-one-out runs use the scan length (not fixed by the pre-registration).
   *Accepted*.
9. **Checked and fine:** disc rotation and sphere mass, Einasto (including the underflow series), NFW
   and R_vir, the reparametrised posterior's Jacobians, seeding, B2 mass sum.


## 7. Open questions

1. Under a physically motivated full covariance for Table 3 (statistical plus smooth systematic
   components), what are the likelihood-only flat rejection, the Keplerian-versus-γ = −0.2
   distinction, and the Einasto-versus-NFW-versus-ΛCDM-like preference? (T-028)
2. How large are departures from equilibrium at 20–27 kpc (warp, flare, Sagittarius, LMC)? Beyond
   this repository.
3. Can any halo shape fit the rotation curve and the stream masses together?

## 8. Exploring via chat

How a coding agent answers "what if" questions about this study without touching `results/`
(rules: AGENTS.md section 2).

| Knob (`PARAMS`) | Meaning | Safe range | Cache only, or new data (size)? |
|---|---|---|---|
| `r_min_powerlaw` | inner radius of the power-law fit (kpc) | 12–22 | none needed (local tables) |
| `a_max`, `a_max_pivot` | upper bounds of the A prior | 10³–10⁶ | none needed |
| `bmax_grid`, `ramp_start` | bias-ramp grid and its start radius | 0–0.3; 15–22 kpc | none needed |
| `corr_rho`, `corr_r_min` | correlated-error cases | 0–0.95; 19–25 kpc | none needed |
| `models` | baryon models fitted | any of the seven | none needed |
| `nfw_rhos_range`, `nfw_rs_range` | NFW priors | wide | none needed |

- Rerun with an override: `python -m astrolab explore 009-m06-mw-outer-rotation-curve-decline --tag <topic> --set KEY=VALUE`
  (outputs in `explore/<date>-<topic>/`, not committed; about 7 minutes for a full run).
- Analyses `run.py` does not cover: a script `explore/<name>.py` with `def main(ctx)`. Existing:
  `explore/halo_fit_quality.py` (post hoc: best-fit χ² of Einasto and NFW).
- Results files and keys: `results/r1.json` (`base`: `median_gamma`, `S`, `p16`, `p84`; `verdict`;
  `sensitivity_log_a`; `sensitivity_pivot`; `delta_chi2`; `leave_one_out`); `results/r2.json`
  (`models`: per model `mdyn_dm`, `mdyn_tot`, `rvir_dm`, `rvir_tot`, `n`, `h`, `M0`, `table4_mdyn`;
  `six_mean`); `results/r3.json` (`constant_gamma`, `constant_mass_EdJ`, `ramp`, `quadrature`,
  `correlated`); `results/r4.json` (`diff_O24`, `diff_E19`, `r1_on_O24`, `r2_on_O24`);
  `results/r5.json` (`einasto_EdJ`, `nfw_EdJ`, `v2r_over_G_26.5`).
- Example questions: "what if the power law starts at 16 kpc?" → `--set r_min_powerlaw=16`; "how does a
  ΛCDM-like halo extrapolate?" → a script fixing 1/n = 0.17.
- Findings that change what we know go into `log.md` (and, for a paper study, the wiki article)
  on a branch.

