# M1: DESI DR2 BAO and evolving dark energy

> 中文：[README.zh.md](README.zh.md)

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
- **Fit validity (required before any criterion is evaluated).** Every fit, the ΛCDM baseline
  included, must pass the convergence and agreement rule below. Every w0waCDM fit is also started
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
The R1 chains must have post-burn length ≥ 50 integrated autocorrelation times τ (largest over
parameters); the Monte Carlo error of each mean is σ/√N_eff with
N_eff = walkers × post-burn steps / τ, and must be below 0.05σ.

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

**K check (diagnostic only; reported, never used to change a tolerance).** The θ* calibration factor K is fixed at
the Planck 2018 reference point (section 4) and treated as a constant. Reported: the shift of
Δχ²_MAP in R2 when K is changed by ±1 prior σ of θ*, and the deviation of our 100θ* at a second
reference point (sanity check only).

### Addendum 2026-11-16: R2-CAMB (T-022, plan 020), pre-registered before any CAMB value at a fit point

*Why.* The referee (section 6, point 1) found that the R2 split between readings A and B is of
the size of the θ* calibration error, and that the cosmology dependence of the calibration
between the Planck reference point and the R2 fit points was unmeasured. The user consented on
2026-11-16 to installing CAMB (`camb` 2.0.5 in the project venv; not a data download).

*Seen before this addendum.* The 2026-11-14 results (section 5). From a speed test, CAMB with the
settings below at two points only: the Planck reference point (100θ* = 1.04116, against 1.041085
in Planck 2018 Table 1, i.e. +7.5×10⁻⁵ or +0.29 prior σ of 100θ*) and the same point with
w0 = −0.8, wa = −0.5 (100θ* = 1.04711; r_drag 147.06 Mpc at both); the formula θ* was not evaluated at the second
point, so no formula–CAMB difference away from the reference point was seen. Implication known when the
variants were chosen: absolute CAMB θ* is a constant +0.29σ above the anchored one, and section 5
shows a higher θ* moves reading A towards −8 (K + 1σ: −6.98), so the raw variant is expected to
move A by about −0.1 relative to the anchored one. For this reason both variants enter the
conclusion below.

*Question.* Do the R2 verdicts of readings A and B change when θ* comes from CAMB instead of the
calibrated fitting formula?

*What changes.* Only θ* in the CMB-prior term of χ²_R2, in the MAP fits; the R2 secondary
posterior chains (MCMC) are not rerun. BAO distances, r_d (Aubourg formula), the prior mean and
covariance, both readings (reading A keeps ων = Σmν/93.14 eV; CAMB's own ων differs by ~10⁻⁶ in
ωbc, negligible and deliberately not "fixed"), bounds, starts (`n_starts` random starts with
seed `PARAMS["seed"]` as in R2, the nested ΛCDM optimum, the paper point), validity checks and the
tolerance stay as pre-registered in this section. The existing feasibility check (Ω_DE ≤ 0 or
non-finite → χ² = ∞) runs before any CAMB call, so the feasible region is the same as in R2.

- **θ*_CAMB.** camb 2.0.5 (version saved with the results), all `CAMBparams` at the package
  defaults except: `set_cosmology(H0=H0, ombh2=ombh2, omch2=omch2, mnu=PARAMS["mnu"],
  num_massive_neutrinos=1, nnu=3.044, TCMB=2.7255, YHe=None)` (helium from CAMB's BBN default; degenerate hierarchy;
  Recfast recombination; default accuracy) and `set_dark_energy(w=w0, wa=wa,
  dark_energy_model="ppf")`; `camb.get_background`, θ* = `thetastar`/100 from
  `get_derived_params()`. The recombination class and BBN predictor are saved with the results.
- **Anchored variant (primary for the referee's question).** θ* = K_C · θ*_CAMB with the constant
  K_C fixed so that 100θ* = 1.041085 at the Planck reference point of section 4 (ωb = 0.022383,
  ωc = 0.12011, H0 = 67.32, Σmν = `PARAMS["mnu"]`, w0 = −1, wa = 0), same CAMB settings. It keeps the
  original anchor and replaces only the cosmology dependence of the calibration.
- **Raw variant.** θ* = θ*_CAMB unscaled: current-CAMB absolute θ* (as current Cobaya + CAMB would
  compute it), not "Planck's θ*" (Planck 2018 used an older CAMB and N_eff = 3.046).
- **Rule.** For each variant, the R2 rule of this section unchanged: per reading
  |Δχ²_MAP − (−8.0)| ≤ 1.0, overall from the two readings as above.
- **Conclusion for T-022.**
  - "R2 robust to the θ* calibration" only if both variants give the same per-reading verdicts as
    the 2026-11-14 run (A not reproduced, B reproduced).
  - "R2 depends on the cosmology dependence of the θ* calibration" if the anchored variant changes
    a per-reading verdict (naming the reading).
  - "R2 depends on the absolute θ* calibration (anchor)" if only the raw variant changes one.
  - "Inconclusive" for a variant with a failed fit (validity checks). Precedence: a variant whose
    fits are all valid is evaluated by its own bullet above, even if the other variant is
    inconclusive; the "robust" label needs both variants valid. Allowed afterwards:
    documented, dated bug fixes only; no change of CAMB accuracy settings, starts or tolerance.
  The 2026-11-14 R2 verdict stays the recorded verdict in every case (it was pre-registered);
  this addendum adds a sensitivity result and its interpretation, it does not replace R2.
- **Diagnostics (reported only).** At the optima of each reading and model: 100θ* from the formula
  (K) minus from CAMB anchored, in prior σ of 100θ*; the ratio of the Aubourg r_d to CAMB's
  `rdrag`; the shift of Δχ² per reading between the formula and each CAMB variant; the number of
  trial points rejected by the feasibility check and, separately, by CAMB errors (χ² = ∞).

### Addendum 2026-11-17: R2-CAMB-RD (T-030), pre-registered before any fit by us with CAMB's r_drag

*Why.* The R2-CAMB referee (section 6, point 2) noted that R2-CAMB kept the Aubourg et al. 2015
r_d formula, so the check was not fully CAMB-consistent. T-030 also asked which quantity DESI's code
compared with the Eq. 35 ωbc mean. *Primary-source search, 2026-11-17 (pages read only):* the
arXiv HTML of the paper (Appendix A was not reachable in the fetched text), the prior's source
`cmbant/PlanckEarlyLCDM` (README and both Cobaya yaml files: the Gaussian input parameters are
`thetastar`, `ombh2`, `omch2`, with `mnu` fixed at 0.06 in the chains) and `CobayaSampler/bao_data`
(BAO mean and covariance files only). DESI's configuration for the compressed prior was not found in
these sources; not yet checked: the full text of Appendix A (PDF), the compression reference [111]
and any DESI chain release with its input files. So the question stays open here. A Cobaya run with
the source's `gaussian_mixture` would constrain ωb + ωc against 0.14143, which for Σmν = 0.06 eV
equals reading A (0.14208 − 0.06/93.14 = 0.141436), with Cobaya's `thetastar`, CAMB's absolute θ*:
so of the variants below, raw-RD with reading A is closest to the source's own configuration.
*Seen before this addendum:* all R2 and R2-CAMB results and both referee tables (sections 5 and 6;
among them: BAO distances from `Background` agree with CAMB to better than 8×10⁻⁶ at the optima, and
the raw/anchored offset comes mainly from N_eff 3.044 vs 3.046), the diagnostic Aubourg r_d / CAMB r_drag = 0.99971–0.99972 at every optimum, and the
referee's own refit with CAMB's r_drag and the formula θ* (Δχ² −6.48 for A, −7.90 for B, about +0.10;
not rerun by us). So the expected outcome is no change of verdict.

*Question.* Do the per-reading R2 verdicts change when both θ* and r_d come from CAMB?

*What changes.* Relative to R2-CAMB, only the sound horizon in the BAO term: r_d = CAMB's `rdrag`
from the same `camb.get_background` call that gives θ* (same settings, `camb_theta.py`). The BAO
distances D_M, D_H stay from `astrolab.cosmo.Background` (as in R2 and R2-CAMB). Two variants, as in
R2-CAMB: **anchored-RD** (θ* = K_C · θ*_CAMB, the R2-CAMB K_C) and **raw-RD** (θ* = θ*_CAMB). Everything
r_d is not scaled in either variant (K_C multiplies θ* only); a non-finite θ* or `rdrag` rejects the
point and is counted, as a non-finite θ* in R2-CAMB. The CAMB call now precedes the BAO term, so the
rejection tallies are not comparable with R2-CAMB's; the pre-CAMB feasibility check and the bounds are
unchanged (CAMB errors can still reject points, as in R2-CAMB). The shift
"against R2-CAMB's same variant" uses R2-CAMB rerun in the same run. Everything
else (readings A and B with ων = Σmν/93.14 eV, prior mean and covariance, bounds, starts, seed,
feasibility check before any CAMB call, CAMB-error rejection, validity checks, tolerance) as in
R2-CAMB. No MCMC.

*Rule, fixed now.* For each variant the R2 rule unchanged (per reading |Δχ²_MAP − (−8.0)| ≤ 1.0).
- "R2 robust to the r_d formula" only if both variants are valid and keep the recorded per-reading
  verdicts (A not reproduced, B reproduced).
- "R2 depends on the r_d formula (reading X)" if a valid variant changes a per-reading verdict
  (attributable to r_d, since both R2-CAMB variants kept the recorded verdicts).
- "Inconclusive (variant: failed fit)" for a variant with a failed fit; a valid variant is still
  evaluated by its own rule, and "robust" needs both valid.
The 2026-11-14 R2 verdict stays the recorded verdict in every case; this is a sensitivity result.
Reported: Δχ²_MAP per reading and variant, its shift against R2-CAMB's same variant, and the gap of
reading A to −8.0. Allowed afterwards: documented, dated bug fixes only.

*Runtime.* The full run reruns R1–R3, R2-CAMB and adds these fits: about 2 hours in total (the last
full run took 5,259 s); no data downloaded. Switch: `PARAMS["camb_rd_check"]` (needs `camb_check`).

## 3. Data (with size estimate)

File sizes from GitHub API metadata (no download), 2026-11-14. All fetched through `ctx.http`
into the system cache (not the project folder). Total required input about 34 MB (33.9 MB, almost all the Pantheon+ covariance), below the
200 MB study budget; every file is below the 50 MB single-download limit.

| Input | Source (service / URL) | Selection | Est. rows / size |
|---|---|---|---|
| DESI DR2 BAO mean | `raw.githubusercontent.com/CobayaSampler/bao_data/master/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_mean.txt` | all 7 tracers | 13 rows, 0.5 kB |
| DESI DR2 BAO covariance | `raw.githubusercontent.com/CobayaSampler/bao_data/master/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_cov.txt` | | 13 × 13, 2.5 kB |
| Pantheon+ distances | `raw.githubusercontent.com/CobayaSampler/sn_data/master/PantheonPlus/Pantheon+SH0ES.dat` | zHD > 0.01 | 1701 rows in the file (fewer after the cut), 0.58 MB |
| Pantheon+ covariance | `raw.githubusercontent.com/CobayaSampler/sn_data/master/PantheonPlus/Pantheon+SH0ES_STAT+SYS.cov` | submatrix for zHD > 0.01 | 1701², 33.3 MB |
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
- **θ* from CAMB (addendum 2026-11-16).** Needs `camb` (not in the base install line; set
  `camb_check` to false without it). R2-CAMB in section 2; code in `camb_theta.py`, results
  in `results/r2_camb.json`; switched by `PARAMS["camb_check"]` (CAMB must be installed).
- **Known limitations.** No full CMB likelihood; θ* via a calibrated fitting formula, not CAMB
  in R2 itself (CAMB enters only in the R2-CAMB sensitivity check, addendum 2026-11-16); the Wilks calibration
  (wiki `gap_regular`) is assumed here as in the paper and only explored (section 8).

## 5. Results (2026-11-14)

Run of 2026-11-14 (`python -m astrolab run 002`, final run 1717 s; inputs 33.9 MB from the cache). Page:
[`web/index.html`](web/index.html) (`python -m astrolab serve`). Numbers: `results/summary.json`.
Every fit passed the pre-registered validity checks (converged; at least 3 starts agree within
0.01; χ²(w0waCDM) ≤ χ²(ΛCDM) + 10⁻³; Pantheon+ uses 1590 SNe after zHD > 0.01).

| Criterion | Ours | Paper | Verdict |
|---|---|---|---|
| R1 Ωm (BAO only, ΛCDM) | 0.2979 ± 0.0086 (+0.05σ) | 0.2975 ± 0.0086 | reproduced |
| R1 h·r_d [Mpc] | 101.52 ± 0.73 (−0.03σ) | 101.54 ± 0.73 | reproduced |
| R2 reading A (ωbc mean = ωb + ωc + ων) | Δχ² = −6.59 (2.1σ) | −8.0 (2.4σ) | not reproduced |
| R2 reading B (ωbc mean = ωb + ωc) | Δχ² = −8.01 (2.4σ) | −8.0 (2.4σ) | reproduced |
| R2 overall | | | **conditionally reproduced (reading B)** |
| R3 DESI alone | −4.65 (1.7σ) | −4.7 (1.7σ) | reproduced |
| R3 DESI + Pantheon+ | −4.86 (1.7σ) | −4.9 (1.7σ) | reproduced |
| R3 DESI + Union3 | −10.03 (2.7σ) | −10.1 (2.7σ) | reproduced |

- R1 chain: post-burn length 99 τ, Monte Carlo error 0.02σ.
- R2 secondary (posterior means, reading B): w0 = −0.437 ± 0.226, wa = −1.69 ± 0.66, against
  −0.43 ± 0.22 and −1.72 ± 0.64 (Eq. 24); reading A gives −0.48 ± 0.23 and −1.55 ± 0.66.
- K check (diagnostic): K = 1.001141; shifting K by ±1 prior σ of θ* moves Δχ² by about ±0.4
  (A: −6.98 / −6.21; B: −8.44 / −7.59): a constant shift of K does not close the 1.4 difference,
  but the cosmology dependence of K at the fit points is not measured (see the finding below). Second reference point: Δ(100θ*) = 3.8×10⁻⁵ (0.15 prior σ).
- **Finding, with its limit.** Reading B reproduces Δχ² and the posterior means; reading A misses
  by 1.4. The verdict is recorded as pre-registered (conditionally reproduced, reading B) and
  readings are not switched post hoc. But the split is not robust (referee, section 6): the θ*
  calibration moves Δχ² by about 0.4 per prior σ of θ*, and its cosmology dependence between the
  reference point and the fit points (ωc 0.117-0.120) is unmeasured and could plausibly reach ~1σ,
  enough for reading A to pass. Nor is reading B cleanly "the paper's convention": the text defines
  ωbc = ωb + ωc, but Eq. 2 normalises ωbc to 0.1432, which equals Planck's ωm including the
  0.06 eV neutrino. We therefore do not conclude which convention DESI's prior uses; a CAMB check of
  θ* at the fit points (T-022, needs the user's consent to install CAMB; consent given 2026-11-16,
  see the R2-CAMB addendum in section 2) would show whether R2 depends on the convention at all; only a primary source can say which convention DESI used.

### R2-CAMB (addendum 2026-11-16, T-022)

Run of 2026-11-16 (`python -m astrolab run 002`, 5259 s, camb 2.0.5; R1, R2, R3 and the K check
reproduce the 2026-11-14 numbers exactly). Numbers: `results/r2_camb.json`.

| Variant | Reading A: Δχ²_MAP (shift vs formula) | Reading B: Δχ²_MAP (shift) | Verdicts |
|---|---|---|---|
| formula, K (2026-11-14) | −6.59 | −8.01 | A not reproduced, B reproduced |
| CAMB anchored (K_C = 0.999928) | −6.59 (−0.007) | −8.01 (−0.002) | A not reproduced, B reproduced |
| CAMB raw (100θ* at reference 1.041160) | −6.71 (−0.119) | −8.13 (−0.125) | A not reproduced, B reproduced |

- **Conclusion (pre-registered rule): R2 robust to the θ* calibration.** Both variants are valid
  (every fit converged, ≥ 3 starts agree, nesting holds) and keep the per-reading verdicts.
- Diagnostics: at all twelve optima (formula, anchored, raw × readings × models) the calibrated
  formula's 100θ* differs from anchored CAMB by −0.012 to −0.048 prior σ, so the cosmology dependence
  of K between the reference point and the fit points is about 20 times smaller than the ~1σ the
  referee considered plausible. The Aubourg r_d is 0.99971–0.99972 of CAMB's r_drag at every optimum
  (r_d was not part of the check). Rejected trial points per fit: 32–60 infeasible (mostly random
  start draws) and one CAMB error in each ΛCDM fit (`CAMBError`), none non-finite.
- As expected from the disclosure in section 2, the raw variant moves both readings by about −0.12;
  reading A stays 0.29 outside the tolerance.
- **What this changes.** The R2 split between readings A and B is not an artefact of the θ*
  calibration: R2 really depends on the ωbc convention of the compressed prior. The recorded R2
  verdict is unchanged.
- **Source of the prior (referee 2026-11-16, verified by us; post hoc).** The prior's source,
  `cmbant/PlanckEarlyLCDM` README (read 2026-11-16): Cobaya `gaussian_mixture` with `input_params: ['thetastar', 'ombh2', 'omch2']`, means `[1.04103e-2, 0.02223, 0.1192]`, transformed to (θ*, ωb, ωb + ωc) reproduces DESI's Eq. 36 covariance to every printed
  digit and its θ* and ωb means, but gives ωb + ωc = 0.14143, while Eq. 35 prints 0.14208; the
  difference 0.00065 is ων for 0.06 eV (0.53σ of ωbc). So **reading A is the faithful version of
  the source prior** and reading B is that prior with its ωbc mean shifted by +0.53σ. Taken with
  Eq. 2 (section 6, point 2), the evidence now favours A. Under A our Δχ² is −6.59 (formula), −6.59
  (CAMB anchored), −6.71 (CAMB raw), and the referee estimates about +0.1 more with CAMB's r_drag in
  place of the Aubourg r_d: about −6.6 against the paper's −8.0. The pre-registered verdict stays
  "conditionally reproduced (reading B)", but B's match may be a coincidence or may reflect how
  DESI's code applied the mean; we cannot tell without DESI's likelihood configuration (T-030).

### R2-CAMB-RD (addendum 2026-11-17, T-030)

Run of 2026-11-18 (`python -m astrolab run 002`, 5189 s, camb 2.0.5; R1, R2, R3, the K check and
R2-CAMB reproduce the earlier numbers exactly). Both θ* and r_d from CAMB (`rdrag` from the same
`get_background` call). Numbers: `results/r2_camb.json`.

| Variant | Reading A: Δχ²_MAP (shift vs R2-CAMB; vs formula) | Reading B: Δχ²_MAP (shift vs R2-CAMB; vs formula) | Verdicts |
|---|---|---|---|
| CAMB anchored-RD | −6.49 (+0.103; +0.096) | −7.90 (+0.107; +0.105) | A not reproduced, B reproduced |
| CAMB raw-RD | −6.60 (+0.102; −0.016) | −8.03 (+0.106; −0.019) | A not reproduced, B reproduced |

- **Conclusion (pre-registered rule): R2 robust to the r_d formula.** Both variants are valid (every
  fit converged, 16–20 starts agree, nesting holds) and keep the per-reading verdicts. Rejected trial
  points per fit: 33 infeasible and one CAMB error in each ΛCDM fit, 48–49 infeasible in each
  w0waCDM fit, none non-finite.
- CAMB's r_drag moves Δχ² by about +0.10 in every reading and variant, as the R2-CAMB referee
  estimated (−6.48 for A, −7.90 for B with the formula θ*, against our anchored-RD −6.49, −7.90 with
  the anchored θ*; the two θ* differ by less than 0.01 in Δχ²).
  After the referee (section 6): this is a constant rescale, the Aubourg r_d being 0.99971–0.99972
  of CAMB's r_drag at every optimum (referee's offline script; at the Planck reference point about
  −0.020% is the formula's own error and −0.007% is N_eff 3.044 vs 3.046, the rest varies with
  cosmology), and it moves both readings alike, so it cannot explain the A/B split. For raw-RD the shift
  against the formula (−0.016, −0.019) is θ* (about −0.12) and r_d (about +0.10) cancelling.
- Gap of reading A to the paper's −8.0: 1.51 (anchored-RD) and 1.40 (raw-RD). Raw-RD with reading A
  is the variant closest to how a current Cobaya + CAMB run would evaluate the prior (section 2; it
  uses N_eff = 3.044, while the prior's chains probably used 3.046): **−6.60**.
- **What this changes.** Nothing in the verdicts ("robust" in the narrow sense that the
  formula-vs-CAMB difference in r_d is too small to matter): with θ* and r_d both from CAMB, reading A still
  gives about −6.5 to −6.6, and only reading B matches −8.0. The question of which quantity DESI's
  code compared with the Eq. 35 mean stays open (the primary-source search of 2026-11-17 did not
  find DESI's configuration; section 2), and so does, under A, the remaining ~1.4 in Δχ².

## 6. Referee notes (independent subagent, 2026-11-14)

The referee saw only README sections 1-4, the code, the results, the Lean argument with its
quote / kind / body table, and the paper. Triage (verified = checked by us against code, results or
the paper):

| # | Point | Verified | Action |
|---|---|---|---|
| 1 | The R2 A/B split is of the size of the θ* calibration error: K ± 1σ moves Δχ² by ~0.4; at K + 1σ reading A misses the tolerance by only 0.02; the cosmology dependence of K at the fit points is unmeasured (second point already 0.15σ off at Δωc = 4×10⁻⁴) | yes | Accepted limitation; interpretation softened (section 5); CAMB check registered as T-022 (needs user consent). The test no longer asserts the K-check values, only their validity. |
| 2 | Eq. 2 normalises ωbc to 0.1432 = Planck ωm including ων, so the paper itself points to reading A; B is not cleanly "the paper's definition" | yes (0.02236 + 0.1202 + 0.00064 = 0.1432) | Accepted; wording changed in README, log, wiki, claim. |
| 3 | DESI-alone w0wa MAP sits near the wa = −3 prior edge (wa = −2.72); Δχ² and its Wilks calibration depend on the prior box | yes | Same box as the paper, so the reproduction stands; noted under `gap_regular` (wiki) and open questions. |
| 4 | Wilks calibration untested anywhere (all σ from χ²(2)) | yes | Open question (section 7): null-hypothesis mocks; this is the wiki's GAP `gap_regular`. |
| 5 | Extra start for DESI alone uses the paper's 68% upper limit wa = −1.34, not a posterior mean | yes | Harmless (a start only); noted here. |
| 6 | N_eff = walkers × steps / τ is optimistic for emcee | yes | R1 margin is large (MC error 0.02σ vs 0.05σ limit); accepted. |
| 7 | 10 Pantheon+ calibrators survive zHD > 0.01; Cobaya likely keeps them too (match −4.86 vs −4.9) | partly (count verified; Cobaya not checked offline) | Accepted limitation: Cobaya's exact cut was not verified; we keep the pre-registered cut. |
| 8 | K-check fits used 10 starts, not ≥ 20 | yes | Fixed (20 starts) and rerun. |
| 9 | Lean: `mod_sig` generalises one quoted value by monotonicity of Eq. 22; `Challenged` is named from "not trivially dismissed"; `gap_regular` could mention prior truncation | yes | Docstrings and wiki notes added; no change of verdicts. |

No code bug that changes a verdict was found; criteria were applied as pre-registered (README
sections 1-4 unchanged since commit 88cdacb, before the data were first used; as of 2026-11-14,
before the R2-CAMB addendum of 2026-11-16).

### Referee, R2-CAMB (independent subagent, 2026-11-16)

The referee saw README sections 1-4 (with the R2-CAMB addendum), the code and the results, not
sections 5-7; it ran small offline checks with camb.

| # | Point | Verified | Action |
|---|---|---|---|
| 1 | The prior's source (`cmbant/PlanckEarlyLCDM` README (read 2026-11-16): Cobaya `gaussian_mixture` with `input_params: ['thetastar', 'ombh2', 'omch2']`, means `[1.04103e-2, 0.02223, 0.1192]`) transforms to Eq. 36 exactly, but its ωb + ωc mean is 0.14143, not 0.14208; the difference is ων (0.00065). Reading A is the source prior; B shifts the mean by +0.53σ | yes: read the README ourselves and recomputed the transformation (covariance −1.19288, −94.0008, 1488.417 ×10⁻⁹) | Accepted; interpretation in section 5 and wiki revised (post hoc, labelled). Which quantity DESI's code compared with 0.14208 needs DESI's likelihood configuration: registered as T-030. Verdict unchanged. |
| 2 | R2-CAMB keeps the Aubourg r_d; with CAMB's r_drag the formula-θ* Δχ² becomes −6.48 (A), −7.90 (B), i.e. about +0.10 | partly: our diagnostics give Aubourg/CAMB = 0.99971 at every optimum, consistent; the refit is the referee's, not rerun by us | Accepted limitation; outside the pre-registered check; a fully CAMB-consistent rerun goes with T-030. |
| 3 | BAO distances from `cosmo.Background` agree with CAMB to < 8×10⁻⁶ at the R2 optima | not rerun | Noted; no action. |
| 4 | The raw/anchored offset (+0.29σ) is almost all N_eff 3.044 vs 3.046 (CAMB with 3.046 gives 1.041089 at the reference); raw is probably closer to how the prior's θ* was computed, so the formula R2 carries a −0.29σ θ* bias from its anchor | partly (consistent with the disclosure; the 3.046 value not rerun) | Accepted: both variants already decide the conclusion; raw shifts Δχ² by −0.12 and changes no verdict. |
| 5 | Low power: a verdict flip needed a ~0.5σ cosmology-dependent θ* error; the check measures ≤ 0.05σ. It shows the calibration is fine, not why A is 1.4 off | yes | Accepted; stated in section 5. |
| 6 | Rules applied as pre-registered; the one pre-run change of the addendum made it stricter | yes | None. |
| 7 | If the anchored variant is invalid and raw flips, the code says "depends on the absolute θ* calibration" | yes | Rejected: this is the pre-registered precedence (a valid variant is evaluated by its own rule); it did not occur. |

### Referee, R2-CAMB-RD (independent subagent, 2026-11-18)

A subagent given README sections 1–4, the section 6 tables, the code and the results files (not
section 5); small offline checks with the cached DESI files, no fits rerun. No bug that changes a
label; the json supports the conclusion. Triage:

| # | Point | Verified | Action |
|---|---|---|---|
| 1 | The code matches the addendum (r_d = `rdrag` from the same `get_background` call, K_C scales θ* only, rejections counted, the shift against R2-CAMB from the same run, the labels); χ² recomputed at all 8 saved RD optima matches the json exactly | yes (rerun of the referee's script: difference 0 at every optimum) | None. |
| 2 | The +0.10 shift is a constant r_d rescale (numbers from the referee's offline script, not saved in `results/`): Aubourg / CAMB = 0.999712–0.999720 at every optimum; swapping r_d at fixed parameters gives Δχ² +0.103 (anchored-RD, A) before any refit, +0.103 after | yes | Stated in section 5. |
| 3 | Where the 0.029% comes from: at the Planck reference point CAMB `rdrag` is 147.059 Mpc with N_eff = 3.044 and 147.049 with 3.046 (Planck's published 147.049), the formula 147.020; so about −0.020% is the formula's own error and −0.007% is N_eff. "Anchored-RD" is a hybrid: θ* is anchored to the Planck reference, r_d is not (as pre-registered) | yes | Stated in section 5. |
| 4 | Neutrinos: CAMB's ων at Σmν = 0.06 eV is 6.449 × 10⁻⁴ against 6.442 × 10⁻⁴ from Σmν/93.14 (0.018 prior σ of ωbc); Σmν is fixed, so no Σmν–r_d degeneracy propagates | yes | None. |
| 5 | r_d enters both readings alike (+0.103 / +0.107 anchored-RD), so it cannot explain the A/B split; the check had low power (flipping A needed about −0.4, B about ±0.9) and tests only the formula-vs-CAMB rescale, not r_d systematics in general | yes (the shifts) | **Accepted**; section 5 reads "robust" in this narrow sense. |
| 6 | For the RD variants `dchi2_shift_vs_formula` mixes two changes: raw-RD's −0.016 is θ* (−0.12) plus r_d (+0.10) cancelling | yes | Section 5 leads with the shift against R2-CAMB and states the decomposition. |
| 7 | No r_d diagnostics are saved at the RD optima (not required by the addendum) | yes | None; the ratios in item 2 are recorded here. |
| 8 | Rejection tallies as expected (one CAMB error per ΛCDM fit, none non-finite) | yes | None. |
| 9 | "Raw-RD with reading A is closest to the source's configuration" is only partly true: raw-RD uses N_eff = 3.044 and CAMB 2.0.5, while the prior's chains probably used 3.046 (the R2-CAMB raw offset) | partly (the N_eff difference yes; the chains' setting is the referee's inference) | **Accepted**; section 5 says "closest to how a current Cobaya + CAMB run would evaluate the prior". |

## 7. Open questions

- The ωbc convention of the compressed prior (Eq. 35): which quantity does the paper's code compare
  with it? A primary source (the authors' Cobaya configuration or the definition in the
  compression paper, ref. [111]) would say which convention DESI used; a CAMB check of θ* at the fit points (T-022; installing CAMB
  needs the user's consent, which README section 4 did not plan; consent given 2026-11-16,
  R2-CAMB addendum in section 2) would show whether R2 depends on it. Answered 2026-11-16: the
  split is robust to the θ* calibration (section 5, R2-CAMB), so R2 does depend on the convention.
  The prior's source chain matches reading A (section 5, referee; post hoc); what remains is which quantity
  DESI's code compared with the 0.14208 mean, and, if A, where the remaining ~1.4 in Δχ² comes
  from (T-030). R2-CAMB-RD (2026-11-18) ruled out the r_d formula as the source: with θ* and r_d
  from CAMB, reading A gives −6.49 to −6.60. The primary sources not yet checked are Appendix A of
  the paper (PDF), ref. [111] and any DESI chain release with its input files.
- Wilks calibration (wiki `gap_regular`): simulate the Δχ² distribution under the ΛCDM best fit
  for DESI + compressed CMB and compare with χ²(2).
- Leave-one-tracer-out sensitivity of Δχ² (`drop_z`), and DES-Dovekie as a third SN sample.
- Prior edge: the DESI-alone w0waCDM MAP sits at wa = −2.72, near the wa = −3 prior bound, so its
  Δχ² and its Wilks calibration depend on the prior box (same box as the paper).

## 8. Exploring via chat

How a coding agent answers "what if" questions about this study without touching `results/`
(rules: AGENTS.md section 2).

| Knob (`PARAMS`) | Meaning | Safe range | Cache only, or new data (size)? |
|---|---|---|---|
| `drop_z` | list of BAO effective redshifts to leave out (leave-one-tracer-out) | values from the mean file: 0.295, 0.51, 0.706, 0.934, 1.321, 1.484, 2.33 | cache only |
| `sn_zmin` | Pantheon+ minimum zHD | 0.01-0.1 | cache only |
| `mnu` | neutrino mass sum [eV], one massive state | 0.06-0.3 | cache only |
| `n_starts` | random starts per fit | ≥ 10 (fewer weakens the validity check) | cache only |
| `r2_mcmc`, `k_check` | run the R2 posterior chains / the K check | true, false (false: much faster) | cache only |
| `camb_check` | run the R2-CAMB check (addendum 2026-11-16); needs `camb` installed (not in the base install line) | true, false (false: much faster, no camb needed) | cache only |
| `camb_rd_check` | also run R2-CAMB-RD (addendum 2026-11-17: r_d from CAMB's `rdrag`); needs `camb_check` | true, false | cache only |
| `r1_steps`, `r2_steps` | chain lengths | ≥ 4000 / ≥ 6000 for the pre-registered precision | cache only |

- Rerun with an override: `python -m astrolab explore 002 --tag <topic> --set KEY=VALUE`
  (outputs in `explore/<date>-<topic>/`, not committed; about 1.5 min with
  `--set r2_mcmc=false --set k_check=false`, about 25 min with everything). A list is passed as
  JSON, e.g. in bash `--set 'drop_z=[2.33]'`.
- Analyses `run.py` does not cover: a script `explore/<name>.py` with `def main(ctx)`, run with
  `python -m astrolab explore 002 --tag <topic> --script explore/<name>.py` (e.g. a Wilks
  simulation, or DES-Dovekie: `sn_data/master/DES-Dovekie/DES-Dovekie_HD.csv` 0.11 MB and
  `covtot_inv_000.npz` 6.2 MB through `ctx.http`).
- Results files and keys (`results/summary.json`): `R1` (`posterior.Om`, `posterior.hrd`,
  `checks`, `verdict`), `R2` (`reading_A_with_nu`, `reading_B_without_nu`: `dchi2`, `sigma`,
  `lcdm`, `w0wa`, `posterior`, `verdict`; `overall`, `K`, `K_check`), `R3` (`desi`,
  `desi_pantheonplus`, `desi_union3`: `dchi2`, `sigma`, `verdict`; `overall`), `params`, `targets`.
- Example questions:
  - "Does the preference survive without the Lyman-α point?" -> `--set 'drop_z=[2.33]' --set r2_mcmc=false --set k_check=false`.
  - "What if the neutrino mass were 0.1 eV?" -> `--set mnu=0.1`.
  - "Is Δχ² really χ²(2)-distributed here?" -> a simulation script in `explore/`.
- Findings that change what we know go into `log.md` (and the wiki article) on a branch.
