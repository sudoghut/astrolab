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
- **Known limitations.** No full CMB likelihood; θ* via a calibrated fitting formula, not CAMB
  (installing CAMB needs the user's consent and is not planned); the Wilks calibration
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
  θ* at the fit points (T-022, needs the user's consent to install CAMB) would show whether R2
  depends on the convention at all; only a primary source can say which convention DESI used.

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
sections 1-4 unchanged since commit 88cdacb, before the data were first used).

## 7. Open questions

- The ωbc convention of the compressed prior (Eq. 35): which quantity does the paper's code compare
  with it? A primary source (the authors' Cobaya configuration or the definition in the
  compression paper, ref. [111]) would say which convention DESI used; a CAMB check of θ* at the fit points (T-022; installing CAMB
  needs the user's consent, which README section 4 did not plan) would show whether R2 depends on it.
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
