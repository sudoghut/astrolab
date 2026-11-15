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

- Rerun with an override: `python -m astrolab explore 009-m06-mw-outer-rotation-curve-decline --tag <topic> --set KEY=VALUE`
  (outputs in `explore/<date>-<topic>/`, not committed; about N s from cache).
- Analyses `run.py` does not cover: a script `explore/<name>.py` with `def main(ctx)`, run with
  `python -m astrolab explore 009-m06-mw-outer-rotation-curve-decline --tag <topic> --script explore/<name>.py`.
- Results files and keys: TODO (`results/<file>.json`: key - meaning).
- Example questions: TODO (question -> knob or script an agent would use).
- Findings that change what we know go into `log.md` (and, for a paper study, the wiki article)
  on a branch.

