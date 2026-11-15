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
likelihood with the Table 3 σ as independent errors, flat priors γ ∈ [−10, 5] and A ∈ [0, 10⁵] km/s,
sampled with a Markov chain Monte Carlo (MCMC, emcee: 32 walkers, 6,000 steps, 1,000 burn-in,
seed 0).
- Statistic S = (0 − median γ) / (84th percentile − median), the like-for-like counterpart of J23's
  0.47/0.15.
- **Reproduced** if the median γ lies in −0.47 ± 0.05 **and** S lies in 3.1 ± 0.3. Otherwise **not
  reproduced**.
- Reported alongside, without verdict: P(γ ≥ 0) converted to a one-sided Gaussian significance;
  Δχ² between the best flat fit (γ = 0) and the best power law, converted with one degree of freedom;
  the leave-one-bin-out S for each of the 8 bins; the 1σ interval of γ and whether it contains −0.5.
- Monte Carlo check: rerun with seed 1; if the two medians of γ differ by more than 0.01, double the
  steps (once) and report both runs.

### 2.2 R2 (descriptive)

For each of the six fully specified baryon models (E dJ, E J, E CM, G dJ, G J, G CM; parameters in
`data/j23_baryons.csv`):
- Baryons: thin and thick discs ρ = M/(4π H L²) exp(−R/L − |z|/H) (J23 eq. 8), circular speed from the
  midplane radial force computed numerically (Bessel-function integral for the double exponential);
  the triaxial bulge as a point mass, V² = G M_b / R (all bins have R ≥ 9.5 kpc, where the bulge is
  well inside).
- Halo: Einasto ρ(r) = ρ0 exp[−(r/h)^(1/n)] with M0 = 4π h³ ρ0, enclosed mass analytic (incomplete
  gamma function); priors as J23: M0 ∈ [10¹⁰, 10¹⁴] M☉ (log-uniform), h ∈ [0, 20] kpc,
  1/n ∈ [0, 5]; MCMC as in R1 (seed 0); 18 points of Table 3, combined errors.
- R_vir: where the mean dark-matter density inside r is 200 ρ_cr, ρ_cr = 1.34 × 10⁻⁷ M☉/pc³;
  M_dyn = M_bar + M_DM(<R_vir) (J23 Sec. 4.3), with M_bar from J23 Table 4.
- Reported: median and 68% interval of M_dyn, R_vir, n, h, M0 per model, the difference to Table 4,
  and the six-model mean against the mean of the six Table 4 values. B2 is not fitted (its gas and
  dust parameters are not in J23).

### 2.3 R3 (exploration, no verdict)

- (a) **Constant bias, null control:** V_true = V_obs / (1 − b) with b constant. Expected Δγ = 0
  exactly (absorbed by A); reported as a check. For the masses: R2 refitted (model E dJ only) for
  b = −0.10, −0.05, +0.05, +0.10.
- (b) **Outer ramp (stress test):** b(R) = 0 for R ≤ 19 kpc, rising linearly to b_max at 26.5 kpc,
  V_true = V_obs / (1 − b(R)) (observed velocities biased low); b_max from 0 to 0.20 in steps of 0.005;
  R1 refitted at each step (MCMC as in R1 with 2,000 steps after burn-in, seed 0); reported: S as a
  function of b_max and the smallest b_max with S < 2. This is an injected stress test, not a
  robustness verdict; literature bias magnitudes (Koop et al. 2024: 10–15%; Ou et al. 2025: 5–20%)
  are given as context only.
- (c) **Secondary cases:** the outer errors enlarged in quadrature by 5%, 10% and 15% of V
  (double-counting the systematics already in Table 3, labelled as such); and correlated errors in the
  4 bins at R ≥ 23.5 kpc, C_ij = ρ σ_i σ_j with ρ = 0.5 and 0.99; S reported for each.

### 2.4 R4 (descriptive)

- Differences between the curves in the overlap (J23 against O24 and E19, after linear interpolation
  of O24 and E19 to J23's radii; asymmetric errors symmetrised as their mean), in units of the
  combined error.
- R1 on O24: bins with R > 19 kpc, symmetrised errors, same statistic; J23 reports γ = −0.56
  (+0.23/−0.22) on this curve.

### 2.5 R5 (descriptive)

- For model E dJ: the enclosed mass M(<26.5 kpc) (baryons plus halo, spherical) and the extrapolated
  M(<32.4 kpc), M(<100 kpc) and M_vir, each with its 68% interval.
- The same for an NFW halo, ρ = ρ_s / [(r/r_s)(1 + r/r_s)²], with log-uniform priors on ρ_s and r_s
  (r_s ∈ [1, 100] kpc), fitted to the same 18 points.
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

1. Read the CSVs; check the row counts (18, 8, 37, 38) and that Table 3 matches the 206.25 and 175.68
   km/s quoted for 19.5 and 26.5 kpc.
2. R1: emcee as in section 2.1; Δχ² with scipy optimisation; leave-one-bin-out.
3. R2: baryonic circular speed from the discs by numerical integration (scipy `quad` of the
   Bessel-function expression for the midplane radial force of a double-exponential disc), plus the
   bulge point mass; Einasto enclosed mass via the regularised lower incomplete gamma function;
   R_vir by root finding; emcee as in R1.
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

