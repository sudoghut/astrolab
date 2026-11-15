# M6 Milky Way outer rotation curve: Keplerian decline, mass and systematics

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

