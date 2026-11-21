# M11 Radcliffe Wave: is the young-cluster wave oscillating?

> 中文：[README.zh.md](README.zh.md) · Web page online: [https://sudoghut.github.io/astrolab/studies/011-m11-radcliffe-wave-oscillation/web/](https://sudoghut.github.io/astrolab/studies/011-m11-radcliffe-wave-oscillation/web/)

> Write sections 1–4 BEFORE writing run.py (pre-registration). Edit them later only
> with a dated note explaining the change.

## 1. Question

Konietzka et al. 2024 (Nature 628, 62; arXiv:2402.12596; "K24") fit a damped-wave model to the
positions and vertical velocities of young clusters (and the positions of molecular clouds) along the
Radcliffe Wave. They conclude that the Wave oscillates through the Galactic plane like a travelling
wave, that a travelling wave is "strongly preferred" over a standing one, and that the fitted
oscillation frequency measures the local midplane density and the Sun's vertical period.

Using only K24's two public tables, we ask:

1. Does their published fit reproduce? (T1, T2)
2. How strongly do the data prefer a travelling wave over a standing wave, judged by tests that do not
   share the weaknesses identified in our argument analysis? (T3, T4, T5)
3. Do the answers survive reasonable changes of the analysis choices? (T6)
4. How much do the ¹²CO velocities say about vertical motion? (T7)
5. Is the fitted vertical frequency set by the data or by the priors? (T8)

The tests are derived from Part 3 of the wiki article
([Study-011](https://github.com/sudoghut/astrolab/wiki/Study-011-radcliffe-wave-oscillation)), which
maps each to a premise or gap of the Lean decomposition (`argument/Argument.lean`). This section and
sections 2–4 were written on 2026-11-21, before any model was fitted. The only contact with the data
before that date was reading the two tables' column names, row counts and value ranges (wiki Part 3).

## 2. Hypothesis and decision criteria

The hypothesis under test is K24's reading: the young clusters' z and v_z follow one travelling wave
in the adopted Galactic potential (B near 1), not a standing wave (B = 0.5).

All intervals are central 68% (16th–84th percentiles) for posteriors, and 95% for bootstrap
intervals, unless stated otherwise. "K24 1σ" means the asymmetric 16–84% interval printed in their
Extended Data Table 2. Each test has its own label, and a test that cannot be evaluated is reported as
"not evaluable" with the reason.

| Test | Quantity | Labels (decision rules) |
|---|---|---|
| **T1** reproduce | our posterior medians of A, p, δ, s₀, γ, φ, for column (4) (clusters, B = 1) and column (6) (clouds + clusters, B = 1) | per column: **reproduced** if at least 5 of the 6 medians fall inside K24's 16–84% interval; **partly reproduced** if 3–4; **not reproduced** if at most 2. Also reported: the anchor points, σ-scaled differences, and the overlap of our inlier set with the table's `inlier` flag |
| **T2** B free | posterior of B (column (5) setup, ω₀t free), on [0, 1], unfolded | reported, no label: median and 16–84%, compared with 0.84 (+0.07/−0.06); P(B > 0.95); P(B < 0.5) |
| **T3** nested likelihood ratios | maximum likelihood of the B-free model, and the profiles at B = 0.5 and at B = 1 (ω₀t = 0, which there merges into φ); 2ΔlnL | **standing**: p from χ²₁, checked by the parametric bootstrap (100 mocks from the B = 0.5 fit; if the bootstrap p and the χ²₁ p fall on different sides of a threshold, the bootstrap p is used): **standing excluded strongly** p < 0.001; **standing excluded** 0.001 ≤ p < 0.05; **standing not excluded** p ≥ 0.05. With 100 mocks, a bootstrap p is resolved only down to 0.01; p < 0.001 is then decided by χ²₁ only if no mock exceeds the observed 2ΔlnL. **pure travelling (B = 1)**: p from χ²₂, checked likewise with 100 mocks from the B = 1 fit: **disfavoured** if p < 0.05, else **not disfavoured** |
| **T4** phase spread | R = \|mean of exp(2iφ_k)\| over the inliers of the B = 0.5 fit, φ_k = arctan(z_k ω_k / v_z,k); p = fraction of 1000 standing mocks with R ≤ R_obs; power = fraction of 1000 mocks from the B = 1 fit (and, reported, from the B-free fit) with p < 0.01 | **standing excluded by the phases** if p < 0.01 and power ≥ 0.8; **not excluded** if p > 0.05 and power ≥ 0.8; **undetermined** otherwise (including power < 0.8) |
| **T5** z and v_z without assuming their relation | b̂ (estimate of 2B − 1, sign = K24's direction of travel) from the shared-k fit; k_z/k_vz from the free-k fit; 95% bootstrap intervals (1000 resamples, Λ drawn from the clouds-only posterior) | **wavelengths**: **consistent** if the k_z/k_vz interval lies inside [0.8, 1.25]; **different** if it lies entirely outside; **undetermined** otherwise. **b̂** (b_T = 0.4, i.e. B = 0.7): **travelling component in K24's direction dominates** if the interval is entirely above 0.4; **no travelling dominance in K24's direction** if entirely below 0.4; **undetermined** otherwise; an interval entirely below −0.4 is reported as travelling the opposite way. **Not applicable** if the wavelengths are "different". The known-answer check (20 mocks per injection at B = 0.5, 0.84 and 1; the mock with the median b̂ at each injection) passes if its interval covers 0 at B = 0.5 and 0.68 at B = 0.84, and lies entirely above 0.4 at B = 1; if it fails, the b̂ label is **undetermined** and the bias is reported |
| **T6** robustness | labels of T3 (standing), T4 and T5 (b̂) under each variant of section 4.6 | **robust** if no variant changes any of the three labels; **fragile** otherwise, naming the variants and labels that change. Changes into or out of "undetermined" or "not evaluable" count as changes |
| **T7** CO | χ² of the ¹²CO velocities for three versions (T1 column-(6) model; the same with v_z = 0; the B = 0.5 fit), each with its own fitted intrinsic dispersion | **CO prefers the travelling wave** if the T1 version's χ² is lower than both others by at least 9; **CO does not distinguish** otherwise. (Expected: v_z contributes at most ~3 km/s to v_LSR, so "does not distinguish" is likely) |
| **T8** potential | ω₀ posterior with ω₀, μ₀, r₀ free (column (7) setup), under K24's priors and under broad uniform priors (ω₀ 30–150 km s⁻¹ kpc⁻¹, μ₀ 0.3–3 kpc⁻¹, r₀ 1–10 kpc) | **data-driven** if, under the broad priors, the ω₀ posterior's 16–84% half-width is below half of K24's prior half-width (in ln ω₀: 0.085) and the medians under the two priors differ by less than 0.5σ (σ: half the 16–84% width of the broad-prior posterior); **prior-driven** if neither holds; **partly data-driven** otherwise. Reported: ρ₀ = ω₀²/(4πG) and the Sun's vertical period under both priors |

**Overall reading.** It is formed mechanically from the labels:

- **"K24's travelling-wave reading is supported by these data"** if all of the following hold:
  - T1 is reproduced or partly reproduced for column (4);
  - T3 gives standing excluded or excluded strongly;
  - T4 gives standing excluded by the phases;
  - T5 gives the travelling component dominates;
  - T6 is robust.
- **"not supported"** if T3 gives standing not excluded and T5 gives no travelling dominance.
- **"mixed"** otherwise, listing which tests support and which do not.

T7 and T8 are reported separately; they do not enter the overall reading.

**What would change our mind about the method.** If T1 is "not reproduced" for both columns, the
remaining tests are still run and reported, but labelled "on our reproduction, which does not match
K24's fit". The README then says that the overall reading refers to our implementation of the model,
not to K24's.

## 3. Data (with size estimate)

| Input | Source (service / URL) | Selection | Est. rows / size |
|---|---|---|---|
| K24 young-cluster table `Radcliffe_Wave_stellar_clusters_Konietzka2024.tab` | Harvard Dataverse doi:10.7910/DVN/XSCB9N, file id 7211931, via `ctx.http` (`https://dataverse.harvard.edu/api/access/datafile/7211931`) | all rows | 125 rows, 10,888 bytes |
| K24 ¹²CO cloud table `Radcliffe_Wave_CO_analysis_Konietzka2024.tab` | Harvard Dataverse doi:10.7910/DVN/Q7F4PC, file id 7211929, via `ctx.http` | all rows | 79 rows, 5,286 bytes |

That is about 16 KB in total, far below the 200 MB study budget. Nothing else is fetched. The column meanings are taken
as follows: `x, y, z` heliocentric Galactic Cartesian positions (pc); `vx, vy, vz` velocities relative
to the LSR (km/s) after K24's solar-motion correction (10.0, 15.4, 7.8) km/s; `sigma*` their standard
errors; `age` (Myr); `inlier` K24's flag. For the clouds: `x, y, z` (pc), `l, b` (deg), `d` (pc), `vr`
the ¹²CO LSR velocity with percentiles `vr16`, `vr84`. These readings are checked when the tables are
loaded (`run.py` records the checks): the mean v_z of the clusters should be near zero in the LSR frame,
and |v_z| < 30 km/s.

## 4. Method

### 4.1 Model (K24 eqs. 1–13)

- **Potential.** Φ(z, r) = ½ ω₀² exp[(r☉ − r)/r₀] (z² − μ₀² z⁴), with r☉ = 8.4 kpc. The adopted
  values are ω₀ = 74 km s⁻¹ kpc⁻¹, r₀ = 3.7 kpc and μ₀ = 1.3 kpc⁻¹, free only in T8.
- **Frequency.** ω(z_max, r) is taken from eq. 3, with the complete elliptic integral from
  `scipy.special.ellipk` (in its parameter-m convention, m = k²). We use z_max = |ζ(s)|, as K24 does.
- **Galactocentric radius.** r(s) = √((r☉ − x(s))² + y(s)²), in heliocentric Galactic coordinates
  with x towards the Galactic Centre.
- **Baseline in the plane.** It is the quadratic Lagrange curve P(u) through the anchor points:
  (x₀, y₀) at u = 0, (x₁, y₁) at u = 0.5, and (x₂, y₂) at u = 1.
  - It is evaluated on 2000 points for u in [−0.2, 1.4].
  - s is the arc length from u = 0, negative for u < 0.
  - The anchors' priors are those of Extended Data Table 1, and the curve extends past the third
    anchor because K24's model continues towards Cygnus X.
- **Shape along the Wave.**
  - Phase: Λ(s) = s/(p − γs) (eq. 6), on the grid where p − γs > 0. Grid points with p − γs ≤ 0
    are excluded from the closest-point search.
  - Envelope: ζ(s) = −A [1 + ((s − s₀)/δ)²]⁻¹ (eq. 9).
- **Waves.** z(s) and v_z(s) follow eqs. 4–5.
- **Distance vectors.** Clusters use d = (x, y, z, v_z/ω₀) − model at the closest grid point, with
  v_z/ω₀ in pc (ω₀ = 74, or the fitted ω₀ in T8). Clouds use the 3-vector.
- **Likelihood.** Eq. 13 for clusters and eq. 11 for clouds, with σ = 47 pc fixed and the outlier
  function C(d/σ) = (Σₙ tanh((dₙ/σ)²))^½.
  - A cluster is an outlier if any component has |dₙ|/σ > √3, that is, if tanh((dₙ/σ)²) > tanh(3)
    for some n (K24's rule).
- **Kernel weights.** A Gaussian kernel density in s with bandwidth 100 pc, about 3–4% of the
  Wave's length. Each object's weight is inversely proportional to the density at its s, normalised
  to sum to the number of objects in its set. The weights are computed once, from the s of each
  object at K24's column-(6) best fit, and held fixed during sampling.
- **Priors.** Extended Data Table 1, with three interpretations of our own:
  - **ω₀t.** U(−π/2, π/2) in MCMC. In maximum-likelihood fits ω₀t is periodic (section 4.3).
  - **μ₀.** The printed ln(μ₀ pc) ~ N(−1.346, 0.25) gives μ₀ ≈ 0.26 pc⁻¹, which is not physical. We
    read it as ln(μ₀ · kpc) ~ N(ln 1.3, 0.25), centred on the adopted 1.3 kpc⁻¹.
  - **ω₀.** ln(ω₀ km⁻¹ s pc) ~ N(−2.4, 0.17) is used as printed: ω₀ ≈ 91 km s⁻¹ kpc⁻¹.

### 4.2 Fits

- **Sampler (T1, T2, T8).** emcee with 48 walkers and 6000 steps, discarding the first 2000. We
  report the acceptance fraction and the autocorrelation time. If the chain is shorter than 50
  autocorrelation times, the fit is flagged and run again with twice the steps.
- **Maximum-likelihood fits (T3; the fits used by T4–T7).** Each fit starts from the best of 20
  starts: the MCMC median plus 19 draws from the prior. The optimiser is Nelder–Mead followed by
  L-BFGS-B, and the priors' support is used as bounds. MAP values are reported alongside.
- **The fits and their setups:**
  - **Column (3):** clouds only, B = 1, ω₀t = 0.
  - **Column (4):** clusters only, B = 1, ω₀t = 0.
  - **Column (5):** clusters only, B and ω₀t free.
  - **Column (6):** clouds and clusters, B = 1, ω₀t = 0.
  - **Column (7):** as (6), with ω₀, μ₀ and r₀ free.

### 4.3 T3 and T4

- **T3.**
  - We profile over all other parameters at B = 0.5, and at B = 1 with ω₀t = 0. The B-free maximum
    has ω₀t periodic on (−π, π].
  - For the bootstrap, each mock draws the data from the fitted null model. That model is the fit's
    z and v_z at each cluster's closest point, plus Gaussian noise of σ = 47 pc on all four
    components and the cluster's measurement errors on z and v_z. Both models are refitted on every
    mock.
- **T4.**
  - The mocks keep the observed clusters' model positions from the B = 0.5 fit and add the same
    noise as in T3.
  - Each mock cluster's closest point is recomputed on the B = 0.5 fit's curve, without refitting.
  - A variant draws the noise by resampling that fit's residual vectors.

### 4.4 T5

- **Baseline and Λ(s).** They come from the column-(3) clouds-only posterior. Each cluster's s is
  its projection onto the baseline in x–y. Clusters whose closest point is an end of the grid are
  dropped and counted.
- **The two fits.** They use all 125 clusters (the variants of T6 apply). Each component is fitted
  as A·ζ̃(s)·sin(2πkΛ(s) + ψ), with A ≥ 0 and k in [0.3, 3], by weighted least squares with the
  measurement errors and the 47 pc scatter added in quadrature. ζ̃ is the clouds-only envelope shape
  divided by its peak.
  - **Free-k fit:** k_z and k_vz are fitted separately.
  - **Shared-k fit:** a single k is fitted for both components.
- **b̂.** It is the ratio σ_min/σ_max of the singular values of [[A_z cos ψ_z, A_z sin ψ_z],
  [A_v cos ψ_v, A_v sin ψ_v]], with the sign of the matrix's determinant. In K24's model this equals
  2B − 1 for any ω₀t. v_z is divided by ω(s), evaluated with the clouds-only envelope as z_max.
- **Bootstrap.** 1000 resamples of the clusters, each with Λ drawn from the clouds-only posterior.
- **Known-answer check.** It runs before the data are fitted. For each injection, 20 mocks are drawn
  at the clusters' s with B = 0.5, 0.84 and 1, using ω₀t from the B-free fit and the other parameters
  from the column-(6) fit, with the noise of T3.

### 4.5 T7

- **Velocity of each cloud's closest point.** We project the model 3D velocity at each cloud's
  closest point onto the line of sight (eq. 14). The in-plane part is Galactic rotation from a flat
  rotation curve. It uses V_c = 242 km/s, the value K24 quotes for its adopted potential, and
  r☉ = 8.4 kpc, taken relative to the LSR. To that we add the solid-body in-plane velocity Θ₂, the
  kernel-weighted mean residual (v_x, v_y) of the T1 column-(6) inlier clusters after subtracting
  rotation.
- **Errors.** Each cloud's error is (vr84 − vr16)/2. The intrinsic dispersion is fitted for each
  version by maximum likelihood.

### 4.6 Robustness variants (T6)

Each variant reruns T3, T4 and T5. A variant that changes the inlier rule also changes it inside T3
and T4.

1. Outlier rule at 3σ per component, instead of √3σ.
2. No outlier model: a plain Gaussian likelihood.
3. No kernel weights.
4. Kernel bandwidth of 50 pc.
5. Kernel bandwidth of 200 pc.
6. Solar motion w☉ = 7.25 km/s instead of 7.8. Every v_z is shifted by +0.55 km/s.
7. Orion left out. These are the clusters whose `name` or `reference` marks them as Orion members;
   if the table does not identify them, the clusters with 180 < l < 220 deg and −25 < b < −5 deg are
   used instead, a box defined here before the data are read.
8. Leave out each `reference` catalogue in turn. There are 7 references; those with fewer than 5
   clusters are pooled into one leave-out.
9. Only clusters with sigmavz below the median.

### 4.7 Cost and order

- **Number of fits.** About 25–40 maximum-likelihood fits, 5 MCMC fits, and the mocks: 200 refits
  in T3, 2000 evaluations in T4, and 1000 bootstrap fits per T5 run.
- **Expected run time.** A few hours on one core. If a short timing run shows the total would exceed
  10 hours, the mock counts are reduced before the formal run. The reduction is recorded as a dated
  amendment, and never made after seeing a test result.
- **Order.** The formal run waits until no other study is running. The known-answer check of T5 runs
  first.
- **Results files** (`results/`): `t1_t2.json`, `t3.json`, `t4.json`, `t5.json`, `t6.json`,
  `t7.json`, `t8.json` and `summary.json`. Each file is below 1 MB, so chains are thinned or
  summarised.

### 4.8 Systematics we know about but do not test

- **Independent velocity data** (Zhu et al. 2024; Bobylev et al. 2025): out of scope (open question).
- **Our choices where K24 is not specific:** the kernel bandwidth, the curve parametrisation, the
  closest-point grid, and the μ₀ prior reading. T6 covers part of this.
- **The table's `inlier` flag** comes from K24's final fit. We do not use it for selection, only for
  comparison.

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

- Rerun with an override: `python -m astrolab explore 011-m11-radcliffe-wave-oscillation --tag <topic> --set KEY=VALUE`
  (outputs in `explore/<date>-<topic>/`, not committed; about N s from cache).
- Analyses `run.py` does not cover: a script `explore/<name>.py` with `def main(ctx)`, run with
  `python -m astrolab explore 011-m11-radcliffe-wave-oscillation --tag <topic> --script explore/<name>.py`.
- Results files and keys: TODO (`results/<file>.json`: key - meaning).
- Example questions: TODO (question -> knob or script an agent would use).
- Findings that change what we know go into `log.md` (and, for a paper study, the wiki article)
  on a branch.

