# M1: DESI DR2 BAO and evolving dark energy

> Sections 1-4 were written on 2026-11-14 BEFORE run.py and before any data were fetched
> (pre-registration; derived from part 3 of the wiki article
> [Study-002](https://github.com/sudoghut/astrolab/blob/main/docs/wiki/Study-002-desi-bao-evolving-dark-energy.md)
> and design plan 010). Later edits to them must carry a dated note.

## 1. Question

1. Do the public DESI DR2 BAO distances (mean vector and covariance) reproduce the paper's
   BAO-only ΛCDM constraints (Ωm, h·r_d; DESI Collaboration 2025, arXiv:2503.14738, Eq. 17)
   with this repo's own background code?
2. With the paper's compressed CMB prior on (θ*, ωb, ωbc) (Appendix A, Eqs. 35-36), how much
   better does w0waCDM fit than ΛCDM (Δχ²_MAP; the paper reports −8.0, 2.4σ, Table 6), under
   both readings of the prior's ωbc mean (section 2, R2)?
3. Without CMB, do DESI alone and DESI combined with Pantheon+ or Union3 supernovae reproduce
   the paper's Δχ²_MAP (−4.7, −4.9, −10.1; Table 6)?

The full-CMB numbers (−12.5, 3.1σ, and the CMB + SN rows) are out of scope: they need the full
Planck and ACT likelihoods. DES-SN5YR is out of scope: its covariance (53.5 MB) exceeds the 50 MB
single-download limit.

## 2. Hypotheses and decision criteria

Common definitions.
- Δχ²_MAP = χ²_min(w0waCDM) − χ²_min(ΛCDM), each minimum found by bounded multi-start
  optimisation inside the paper's priors (w0 ∈ [−3, 1], wa ∈ [−3, 2], w0 + wa < 0; flat priors,
  so the MAP is the constrained maximum likelihood; w0 + wa < 0 is enforced as
  w0 + wa ≤ −10⁻⁹). Significance: N such that the two-sided
  Gaussian tail equals the χ²(2 dof) tail at −Δχ²_MAP (paper Eq. 22).
- Tolerances are fixed here, before any result, and are the same for every reading and combination.
  Error budget behind the Δχ² tolerance of 1.0 (written before any result): the paper rounds
  Δχ² to 0.1 (±0.05); optimiser convergence is required to 0.01 (fit validity below); r_d from the
  Aubourg formula is good to 0.02% against CAMB, which at the DESI precision (~0.3% on the
  combined BAO scale) moves χ² by well under 0.1; the BAO-only approximation (radiation neglected,
  ~5×10⁻⁴ in E(z) at z = 2.33) moves χ² by ~0.1 at most; the θ* calibration K is the largest
  unknown, bounded only by the reported K check (section 2, last item), and the remainder of the
  allowance (~0.7) is assigned to it and to CAMB-versus-fitting-formula differences in z*. For R1
  the tolerance of 0.3σ covers the same implementation differences on a nearly Gaussian
  two-parameter posterior.
- **Fit validity (required before any criterion is evaluated).** Every w0waCDM fit is also started
  from its nested ΛCDM optimum (w0 = −1, wa = 0) and from the paper's reported point (the paper's
  w0, wa posterior means for that combination, Table 5 / Eqs. 23-24, other parameters from the
  ΛCDM optimum), so
  χ²_min(w0waCDM) ≤ χ²_min(ΛCDM) + 10⁻³ must hold; and at least 3 starts must agree on each minimum
  within 0.01, counting only converged starts (a start converges when its final Nelder-Mead run
  meets the tolerances within the evaluation limit; agreement is in χ², and the largest parameter
  distance among the agreeing starts, `x_spread` in units of the prior width, is reported but not
  required, since degenerate directions are expected). `n_conv`, `n_agree`, `x_spread` and `n_ok` are
  saved with every fit. A fit that fails either check is reported as a failed fit (not as a result) and is
  investigated before anything else.
- Each criterion is reported as **reproduced** or **not reproduced**; R2 also has
  **conditionally reproduced** (below). A failure is reported with its size and our best
  explanation; tolerances are not changed afterwards.

**R1 (BAO only, ΛCDM).** Fitting the DESI DR2 BAO (ALL tracers) with flat ΛCDM, sampling Ωm and
h·r_d (flat priors Ωm ∈ [0.01, 0.99], h·r_d ∈ [50, 150] Mpc): |Ωm − 0.2975| ≤ 0.0026 (0.3σ) and |h·r_d − 101.54 Mpc| ≤ 0.22 Mpc (0.3σ), using the
posterior means; and our 1σ errors (half-width of the central 68% marginal interval of the
 emcee samples, the paper's convention) within 20% of 0.0086 and 0.73 Mpc. *Expectation:* same data,
nearly Gaussian posterior, so this should pass; a failure points to the distance code.

**R2 (DESI + compressed CMB prior).** |Δχ²_MAP − (−8.0)| ≤ 1.0, evaluated separately under
- reading A (`R2.reading_A_with_nu`): the Eq. 35 ωbc mean constrains ωb + ωc + ων
  (indirect numerical evidence, plan 010 section 2), and
- reading B (`R2.reading_B_without_nu`): it constrains ωb + ωc (the paper's definition next to Eq. 2).

Overall: both pass → reproduced; exactly one passes → conditionally reproduced (naming the
reading; the result depends on the prior's parameter definition); neither → not reproduced.
We do not choose a reading by which one hits −8.0. Secondary, reported but not decisive: the
w0, wa posterior means against −0.43 ± 0.22 and −1.72 ± 0.64 (Eq. 24); they depend on the
sampling parameters through the Jacobian (section 4).

**R3 (no CMB).** For each of DESI alone (target −4.7), DESI + Pantheon+ (−4.9) and
DESI + Union3 (−10.1): |Δχ²_MAP − target| ≤ 1.0. R3 is reproduced if all three pass; the three
are also reported individually.

**K check (not a reproduction criterion; reported).** The θ* calibration factor K is fixed at
the Planck 2018 reference point (section 4) and treated as a constant. Reported: the shift of
Δχ²_MAP in R2 when K is changed by ±1 prior σ of θ*, and the deviation of our 100θ* at a second
reference point (sanity check only).

## 3. Data (with size estimate)

File sizes from GitHub API metadata (no download), 2026-11-14. All fetched through `ctx.http`
into the system cache (not the project folder). Total required input about 34 MB (33.9 MB, almost all the Pantheon+ covariance), below the
200 MB study budget; every file is below the 50 MB single-download limit.

| Input | Source (service / URL) | Selection | Est. rows / size |
|---|---|---|---|
| DESI DR2 BAO mean | `raw.githubusercontent.com/CobayaSampler/bao_data/master/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_mean.txt` | all 7 tracers | 13 rows, 0.5 kB |
| DESI DR2 BAO covariance | same folder, `desi_gaussian_bao_ALL_GCcomb_cov.txt` | | 13 × 13, 2.5 kB |
| Pantheon+ distances | `raw.githubusercontent.com/CobayaSampler/sn_data/master/PantheonPlus/Pantheon+SH0ES.dat` | zHD > 0.01 | 1701 rows in the file (fewer after the cut), 0.58 MB |
| Pantheon+ covariance | same folder, `Pantheon+SH0ES_STAT+SYS.cov` | submatrix for zHD > 0.01 | 1701², 33.3 MB |
| Union3 | `raw.githubusercontent.com/CobayaSampler/sn_data/master/Union3/lcparam_full.txt` and `.../Union3/mag_covmat.txt` | all nodes | about 22 binned nodes, 1.6 kB + 9.2 kB |
| Compressed CMB prior | paper Appendix A, Eqs. 35-36 (θ* mean to 6 digits from `cmbant/PlanckEarlyLCDM`) | in the code | 3 numbers + 3 × 3 |

Exploration only (README section 8): DES-Dovekie (`DES-Dovekie_HD.csv` 0.11 MB,
`covtot_inv_000.npz` 6.2 MB) and the per-tracer DESI files (about 1.2 kB).

## 4. Method

- **Background (`astrolab/cosmo.py`, new core module).** Flat w0waCDM with CPL dark energy;
  photons (T_CMB = 2.7255 K), N_eff = 3.044 with one massive neutrino of 0.06 eV (Fermi-Dirac
  density integral) and two massless; distances D_M, D_H, D_V by numerical integration.
  Variable names keep ωb + ωc (`ombc`) and ωb + ωc + ων (`omm`) apart.
- **BAO only (R1, R3).** Parameters Ωm (including neutrinos) and h·r_d; at z ≤ 2.33 neutrinos
  are treated as matter and radiation is neglected (relative error in E(z) about 5×10⁻⁴).
- **r_d (R2).** Aubourg et al. 2015 (arXiv:1411.1074) Eq. 16 fitting formula (inputs ω_cb and ων
  separately); formula checked against the source before use; cross-checked against the paper's
  Eq. 2 and a sound-speed integral (order of magnitude only).
- **θ* (R2).** θ* = r_s(z*)/D_M(z*), z* from Hu & Sugiyama 1996, r_s by numerical integration,
  multiplied by a constant K fixed so that 100θ* = 1.041085 at the Planck 2018 best-fit point
  (Planck 2018 VI, arXiv:1807.06209, Table 1, Plik best fit: ωb = 0.022383, ωc = 0.12011,
  H0 = 67.32; one code at one exact point). The prototype needed K ≈ 1 + 1.3×10⁻³ (plan 010
  section 4). Sanity check at a second point (reported only): the CamSpec column of the same
  table (posterior means 0.02229, 0.1197, 67.39; 100θ* = 1.04106). The same best-fit point checks
  the r_d formula against r_drag = 147.049 Mpc (Planck uses N_eff = 3.046).
- **CMB prior (R2).** Gaussian in (θ*, ωb, ωbc) with the Eq. 36 covariance and mean
  (0.0104103, 0.02223, 0.14208); ωbc compared to ωb + ωc + ων (reading A, with ων = Σmν/93.14 eV
  as in the paper's Eq. 7) or ωb + ωc (reading B). The BAO distances in R2 use the full background
  (radiation and neutrinos included), not the late-time approximation of R1 and R3.
  Sampling parameters: H0, ωb, ωc (+ w0, wa) with flat priors H0 ∈ [20, 100],
  ωb ∈ [0.005, 0.1], ωc ∈ [0.001, 0.99].
- **Supernovae (R3).** χ² with the absolute magnitude marginalised analytically:
  χ² = ΔᵀC⁻¹Δ − (1ᵀC⁻¹Δ)²/(1ᵀC⁻¹1). Pantheon+: zHD > 0.01, covariance submatrix before
  inversion, D_L with zHD and the (1+zHEL) factor, column `m_b_corr` (not `MU_SH0ES`). Union3: the
  binned nodes with `mag_covmat.txt`, following the Cobaya likelihood's column conventions
  (checked against its `.dataset` file before use; Cobaya reads only `zcmb` and `mb` and sets
  zhel = zcmb).
- **Fits (`astrolab/infer.py`, new core module).** Bounded multi-start optimisation for χ²_min:
  at least 20 random starts plus the nested ΛCDM optimum and the paper's point, Nelder-Mead in
  unit-scaled coordinates with polish restarts; non-finite values and points outside the priors
  are rejected (validity checks in section 2); emcee for posterior means (R1, R2 secondary),
  with convergence checked by the integrated autocorrelation time (post-burn chains at least
  50 τ); posterior means are reported with their Monte Carlo error σ/√N_eff.
- **Tests.** Offline unit tests for `cosmo` (limits, Planck reference point, K) and `infer`
  (analytic marginalisation against a brute-force grid, Δχ² → σ conversion: 12.5 → 3.1σ,
  8.0 → 2.4σ).
- **Known limitations.** No full CMB likelihood; θ* via a calibrated fitting formula, not CAMB
  (installing CAMB needs the user's consent and is not planned); the Wilks calibration
  (wiki `gap_regular`) is assumed here as in the paper and only explored (section 8).

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

- Rerun with an override: `python -m astrolab explore 002-m01-desi-bao-evolving-dark-energy --tag <topic> --set KEY=VALUE`
  (outputs in `explore/<date>-<topic>/`, not committed; about N s from cache).
- Analyses `run.py` does not cover: a script `explore/<name>.py` with `def main(ctx)`, run with
  `python -m astrolab explore 002-m01-desi-bao-evolving-dark-energy --tag <topic> --script explore/<name>.py`.
- Results files and keys: TODO (`results/<file>.json`: key - meaning).
- Example questions: TODO (question -> knob or script an agent would use).
- Findings that change what we know go into `log.md` (and, for a paper study, the wiki article)
  on a branch.

