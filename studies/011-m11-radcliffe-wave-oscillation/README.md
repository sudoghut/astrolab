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
maps each to a premise or gap of the Lean decomposition (`argument/Argument.lean`).

This section and sections 2–4 were written on 2026-11-21, before any model was fitted. Before that
date, our only contact with the data was reading the two tables' column names, row counts and value
ranges, and the value counts of the cluster table's `reference` and `inlier` columns (wiki Part 3).
- `inlier`: 89 inliers and 36 outliers.
- `reference`: 7 source catalogues, with 43, 37, 23, 15, 5, 1 and 1 clusters.

## 2. Hypothesis and decision criteria

The hypothesis under test is K24's reading: the young clusters' z and v_z follow one travelling wave
in the adopted Galactic potential (B near 1), not a standing wave (B = 0.5).

**Conventions.**
- Posterior intervals are central 68% (16th–84th percentiles). Bootstrap intervals are 95%, unless
  stated otherwise.
- "K24 1σ" means the asymmetric 16–84% interval printed in their Extended Data Table 2.
- A bootstrap p-value from N mocks, k of which are at least as extreme as the data, is
  p_boot = (1 + k)/(1 + N).
- Each test has its own label. A test that cannot be evaluated is reported as "not evaluable", with
  the reason.

| Test | Quantity | Labels (decision rules) |
|---|---|---|
| **T1** reproduce | our posterior medians of A, p, δ, s₀, γ, φ, for column (4) (clusters, B = 1) and column (6) (clouds + clusters, B = 1) | per column: **reproduced** if at least 5 of the 6 medians fall inside K24's 16–84% interval; **partly reproduced** if 3–4; **not reproduced** if at most 2. Also reported: the anchor points, σ-scaled differences, and the overlap of our inlier set with the table's `inlier` flag |
| **T2** B free | posterior of B (column (5) setup, ω₀t free), on [0, 1], unfolded | reported, no label: median and 16–84%, compared with 0.84 (+0.07/−0.06); P(B > 0.95); P(B < 0.5) |
| **T3** nested likelihood ratios | 2ΔlnL between the B-free maximum and the profile at B = 0.5 (reference χ²₁), and at B = 1 with ω₀t = 0, where ω₀t merges into φ (reference χ²₂). Each is calibrated by N mocks from the null fit (section 4.3). The calibrated p is the χ² p-value of 2ΔlnL × (d / m), where d is the reference degrees of freedom and m the mean 2ΔlnL of the mocks (a Bartlett-type rescaling); if m = 0 the calibrated p is not evaluable. We also report p_raw (uncalibrated χ²), p_boot, and the inlier sets of all fits with their overlaps | **standing excluded strongly** if the calibrated p and p_raw are both below 0.001 and no mock reaches the observed 2ΔlnL. **standing excluded** if not "strongly", the calibrated p is below 0.05 and p_boot is below 0.05. **standing not excluded** otherwise. **pure travelling (B = 1) disfavoured** if its calibrated p is below 0.05 and its p_boot is below 0.05; **not disfavoured** otherwise |
| **T4** phase spread | R = \|mean of exp(2iφ_k)\| over the inliers of the B = 0.5 fit. p = p_boot over N₄ standing mocks with R ≤ R_obs. Power = fraction of N₄ mocks drawn from the B = 1 fit with p < 0.01; the same is reported for mocks from the B-free fit | **standing excluded by the phases** if p < 0.01 and power ≥ 0.8; **not excluded** if p > 0.05 and power ≥ 0.8; **undetermined** otherwise (including power < 0.8) |
| **T5** z and v_z without assuming their relation | b̂ (estimate of 2B − 1, sign = K24's direction of travel), from the shared-k fit. k_z/k_vz, from the free-k fit. Both with 95% bootstrap intervals | **Wavelengths:** **consistent** if the k_z/k_vz interval lies inside [0.8, 1.25]; **different** if it lies entirely outside; **undetermined** otherwise. **b̂** (b_T = 0.4, i.e. B = 0.7): **travelling component in K24's direction dominates** if the interval is entirely above 0.4; **no travelling dominance in K24's direction** if entirely below 0.4; **undetermined** otherwise. An interval entirely below −0.4 is also reported as travelling the opposite way. b̂ is **not applicable** if the wavelengths are "different"; when they are "undetermined", b̂ is reported with that caveat. Also reported: Δ = ψ_v − ψ_z, ρ = A_v/A_z, and whether the b̂ interval contains 0 (standing) and 0.68 (K24). **Known-answer check** (section 4.4): it passes if, at each injection, the median mock (the 10th of the 20 when ranked by b̂) has an interval covering 0 at B = 0.5, covering 0.68 at B = 0.84, and lying entirely above 0.4 at B = 1. If it fails, the b̂ label is **undetermined** and the bias is reported; in T6 a failed main-run check makes every variant's b̂ label undetermined too. Coverage over all mocks is reported as well |
| **T6** robustness | five labels under each variant of section 4.6, computed as specified there: T3 standing, T3 pure travelling, T4, T5 wavelengths, T5 b̂. Each variant label is compared with the main run's label computed by the same rule (section 4.6); the main run's full-rule labels are reported separately. Each change is reported with the Monte Carlo standard error of the p-value or interval end that crossed a threshold (for variants 3–10, the calibrated p's error is propagated from the standard error of m) | **robust** if no variant changes any of the five labels; **fragile** otherwise, naming the variants and labels that change. A change into or out of "undetermined" or "not evaluable" counts as a change |
| **T7** CO | −2 ln L_max of the ¹²CO velocities for three versions, each with its own fitted intrinsic dispersion (the likelihood includes the Σ ln(e² + σ_int²) term): (a) the column-(6) B = 1 model; (b) the same with v_z = 0; (c) a column-(6)-setup fit with B = 0.5 and ω₀t free | **CO prefers the travelling wave** if (a)'s −2 ln L_max is lower than both (b) and (c) by at least 9; **CO does not distinguish** otherwise. v_z contributes at most ~3 km/s to v_LSR, so "does not distinguish" is likely |
| **T8** potential | ω₀ posterior with ω₀, μ₀ and r₀ free (column (7) setup), under K24's priors and under broad uniform priors (ω₀ 30–150 km s⁻¹ kpc⁻¹, μ₀ 0.3–3 kpc⁻¹, r₀ 1–10 kpc). All widths and shifts are in ln ω₀ | **data-driven** if, under the broad priors, the posterior 16–84% half-width is below half of K24's prior σ (0.085), and the medians under the two priors differ by less than 0.5σ (σ: half the 16–84% width of the broad-prior posterior). **prior-driven** if neither holds; **partly data-driven** otherwise. Reported under both priors: ρ₀ = ω₀²/(4πG) and the Sun's vertical period. Reported as a variant: the v_z/ω₀ divisor fixed at 74 |

**Overall reading.** It is formed mechanically from the labels:
- **"K24's travelling-wave reading is supported by these data"** if all of these hold:
  - T1 is reproduced or partly reproduced for column (4);
  - T3 gives standing excluded or excluded strongly;
  - T4 gives standing excluded by the phases;
  - T5 gives travelling component dominates;
  - T6 is robust.
- **"not supported"** if T3 gives standing not excluded and T5 gives no travelling dominance.
- **"mixed"** otherwise, listing which tests support, which do not, and which are undetermined or not evaluable.

T7 and T8 are reported separately and do not enter the overall reading.

**What would change our mind about the method.** If T1 is "not reproduced" for both columns, the
remaining tests are still run and reported, but labelled "on our reproduction, which does not match
K24's fit". The README then says that the overall reading refers to our implementation of the model,
not to K24's.

## 3. Data (with size estimate)

| Input | Source (service / URL) | Selection | Est. rows / size |
|---|---|---|---|
| K24 young-cluster table `Radcliffe_Wave_stellar_clusters_Konietzka2024.tab` | Harvard Dataverse doi:10.7910/DVN/XSCB9N, file id 7211931, via `ctx.http` (`https://dataverse.harvard.edu/api/access/datafile/7211931`) | all rows | 125 rows, 10,888 bytes |
| K24 ¹²CO cloud table `Radcliffe_Wave_CO_analysis_Konietzka2024.tab` | Harvard Dataverse doi:10.7910/DVN/Q7F4PC, file id 7211929, via `ctx.http` | all rows | 79 rows, 5,286 bytes |

The two tables come to about 16 KB, far below the 200 MB study budget. Nothing else is fetched.

**Column meanings, as we take them.**
- *Clusters:*
  - `x, y, z`: heliocentric Galactic Cartesian positions (pc), used as given, with no offset for the
    Sun's height (as in K24).
  - `vx, vy, vz`: velocities relative to the local standard of rest (LSR, km/s), after K24's
    solar-motion correction (10.0, 15.4, 7.8) km/s, i.e. v_LSR = v_helio + (u☉, v☉, w☉).
  - `sigma*`: their standard errors. `age`: in Myr. `inlier`: K24's flag.
- *Clouds:* `x, y, z` (pc), `l, b` (deg), `d` (pc), and `vr`, the ¹²CO LSR velocity, with its
  percentiles `vr16` and `vr84`.

**Load check.** The weighted mean v_z of the clusters must satisfy |mean v_z| < 3 km/s (a heliocentric
table would give about −7.8). If it fails, the run stops before any fit, and the reading is fixed by a
dated amendment.

## 4. Method

### 4.1 Model (K24 eqs. 1–13)

- **Potential.** Φ(z, r) = ½ ω₀² exp[(r☉ − r)/r₀] (z² − μ₀² z⁴), with r☉ = 8.4 kpc and the adopted
  ω₀ = 74 km s⁻¹ kpc⁻¹, r₀ = 3.7 kpc, μ₀ = 1.3 kpc⁻¹ (freed only in T8).
- **Frequency ω(z_max, r).** From eq. 3, with z_max = |ζ(s)| as in K24.
  - The argument of the complete elliptic integral is checked against eq. 3 when implemented.
  - Unit tests check that ω → ω₀ exp[(r☉ − r)/(2r₀)] as z_max → 0, and that ω falls by 6–7% at
    μ₀ z_max = 0.29 (first-order theory gives −(3/4)μ₀² z_max² ≈ −6.3%).
  - Where μ₀ z_max ≥ 1/√2 the orbit is unbound, and the likelihood is zero.
- **Galactocentric radius.** r(s) = √((r☉ − x(s))² + y(s)²), with x pointing towards the Galactic
  Centre.
- **Baseline in the plane.** The quadratic Lagrange curve P(u) through the anchor points (x₀, y₀) at
  u = 0, (x₁, y₁) at u = 0.5 and (x₂, y₂) at u = 1.
  - It is evaluated on 2000 points for u in [−0.2, 1.4]. The curve extends past the third anchor
    because K24's model continues towards Cygnus X.
  - s is the arc length from u = 0, negative for u < 0.
  - A variant places the middle anchor at its chord-length position (section 4.6).
- **Wave shape.**
  - Λ(s) = s/(p − γs) (eq. 6), used only on grid points with p − γs > 0. Other grid points are
    excluded from the closest-point search.
  - ζ(s) = −A [1 + ((s − s₀)/δ)²]⁻¹ (eq. 9).
  - z(s) and v_z(s) follow eqs. 4–5.
- **Distance vectors.** For a cluster, d = (x, y, z, v_z/ω₀) − the model at the closest grid point.
  v_z/ω₀ is in pc, with ω₀ = 74 (or the fitted ω₀ in T8). A cloud uses the 3-vector (x, y, z).
- **Likelihood.** Eq. 13 for clusters and eq. 11 for clouds. σ = 47 pc is fixed. The outlier function
  is C(d/σ) = (Σₙ tanh((dₙ/σ)²))^½. A cluster is an outlier if, for any component,
  tanh((dₙ/σ)²) > tanh(3), i.e. |dₙ|/σ > √3 (K24's rule).
- **Kernel weights.** A Gaussian kernel density in s, with bandwidth 100 pc (about 3–4% of the Wave's
  length).
  - Each object's weight is inversely proportional to the density at its s, normalised to sum to the
    number of objects in its set.
  - The weights are computed once, from each object's s under K24's Extended Data Table 2
    column-(6) medians, and held fixed during sampling. Fixed weights also keep the likelihoods of
    T3 nested.
- **Priors.** Extended Data Table 1, with three readings of ours:
  - **ω₀t:** U(−π/2, π/2) in MCMC. In maximum-likelihood fits it is periodic (section 4.3).
  - **μ₀:** the printed ln(μ₀ pc) ~ N(−1.346, 0.25) gives μ₀ ≈ 0.26 pc⁻¹, which is not physical. We
    read it as ln(μ₀ · kpc) ~ N(ln 1.3, 0.25), centred on the adopted 1.3 kpc⁻¹. Note that
    −1.346 ≈ ln(ln 1.3) = −1.339, which suggests a double logarithm in the printed value.
  - **ω₀:** ln(ω₀ km⁻¹ s pc) ~ N(−2.4, 0.17) is used as printed (ω₀ ≈ 91 km s⁻¹ kpc⁻¹).

### 4.2 Fits

- **Sampler (T1, T2, T8).** emcee with 48 walkers and 6000 steps, discarding the first 2000. The
  acceptance fraction and autocorrelation time are reported.
  - If the chain is shorter than 50 autocorrelation times, it is rerun with twice the steps.
  - If it is still short, the fit is used and flagged as "chain short" in the results.
- **Maximum-likelihood fits.** The best of 20 starts: the MCMC median plus 19 prior draws. Nelder–Mead
  then L-BFGS-B, within the priors' support. MAP values are reported alongside.
- **Fit setups:**
  - Column (3): clouds only, B = 1, ω₀t = 0.
  - Column (4): clusters only, B = 1, ω₀t = 0.
  - Column (5): clusters only, B and ω₀t free.
  - Column (6): clouds + clusters, B = 1, ω₀t = 0.
  - Column (7): as (6), with ω₀, μ₀ and r₀ free.
  - For T7 only: column-(6) setup with B = 0.5 and ω₀t free.
- **Order.**
  1. Load check.
  2. Column (3).
  3. T5 known-answer check (needs only K24's published values and the clouds-only posterior; no
     cluster has been fitted yet). The load check has already read the clusters' v_z, a known
     departure from wiki Part 3's "before the data are read"; it fits nothing.
  4. All other fits.

### 4.3 T3 and T4

- **T3 fits.** The likelihood is profiled over all other parameters at B = 0.5, and at B = 1 with
  ω₀t = 0. In the B-free maximum, ω₀t is periodic on (−π, π].
- **T3 mocks.** A mock is drawn from the fitted null model (the B = 0.5 fit, or the B = 1 fit).
  - Every inlier of the null fit is placed at the model point closest to it, (x, y, z, v_z), plus
    Gaussian noise: σ = 47 pc on all four components (in v_z, 47 pc × ω₀ ≈ 3.5 km/s), plus the
    cluster's measurement errors (`sigmax`, `sigmay`, `sigmaz`, `sigmavz`) added in quadrature.
  - The null fit's outliers keep their observed values.
  - Both models are refitted on every mock, using 3 starts: the generating parameters, the data's best
    fit, and one prior draw. The B-free refit always also starts from the refitted null optimum, so
    that 2ΔlnL ≥ 0; any negative value is clipped to 0 and counted.
  - N = 100 mocks per null. A reported variant draws the noise by resampling the null fit's residual
    vectors.
- **T4 mocks.** These use the same clusters: the inliers of the B = 0.5 fit, identified by index; the
  outlier rule is not reapplied.
  - Standing mocks are drawn from the B = 0.5 fit as in T3. Power mocks are drawn from the B = 1 fit
    (and, reported, from the B-free fit).
  - In all mocks, closest points (s_k, and so ω_k) are recomputed on the B = 0.5 fit's curve, without
    refitting: the same procedure as for the data.
  - In φ_k = arctan(z_k ω_k / v_z,k), z is in pc, ω in km s⁻¹ pc⁻¹ and v_z in km/s.
  - N₄ = 1000 mocks each. A reported variant uses residual resampling.

### 4.4 T5

- **Baseline, Λ(s) and s.** They come from the column-(3) clouds-only posterior. Each cluster's s is
  its projection onto the baseline in x–y. Clusters whose closest point is an end of the grid are
  dropped and counted.
- **Cluster set, using positions only.** A cluster is kept if each of its x, y and z residuals from
  the clouds-only model at its closest point is below √3 × 47 pc. Variants use 3σ, or all 125
  clusters (section 4.6).
- **Fit form.** Each component is fitted as A·ζ̃(s)·sin(2πkΛ(s) + ψ), with A ≥ 0 and k in [0.3, 3].
  - ζ̃ is the clouds-only envelope shape divided by its peak.
  - v_z is divided by ω(s), using the clouds-only envelope as z_max.
  - Weighted least squares, with the kernel weights of section 4.1 (recomputed on these s). The errors
    are the measurement errors and the 47 pc scatter added in quadrature.
  - k is found on a grid from 0.3 to 3 in steps of 0.01, then refined. A k at a bound is reported.
- **Two fits.** The free-k fit (separate k_z and k_vz) and the shared-k fit (one k).
- **b̂.** The ratio σ_min/σ_max of the singular values of
  [[A_z cos ψ_z, A_z sin ψ_z], [A_v cos ψ_v, A_v sin ψ_v]], times the sign of its determinant. In
  K24's model this equals 2B − 1 for any ω₀t. Reported as a sensitivity check: b̂ with ω₀ = 68 in ω(s).
- **Bootstrap.** 1000 resamples of the clusters. Each resample also draws one full sample of the
  clouds-only posterior (anchors included) and re-projects s.
- **Known-answer check.**
  - The mocks are generated on K24's column-(6) model: Extended Data Table 2 medians, with
    ω₀t = −0.38 (column (5)), at the selected clusters' positions, and with the noise of T3.
  - They are analysed exactly as the data, using the clouds-only posterior, including the √3 × 47 pc
    position cut.
  - 20 mocks per injection, at B = 0.5, 0.84 and 1.

### 4.5 T7

- **Line-of-sight velocity.** We project the model 3D velocity at each cloud's closest point onto the
  line of sight (eq. 14).
- **In-plane part.** Galactic rotation from a flat rotation curve, relative to the LSR (V_c = 242 km/s,
  the value K24 quote for their adopted potential; r☉ = 8.4 kpc), plus a solid-body velocity Θ₂. Θ₂ is
  the kernel-weighted mean residual (v_x, v_y) of the column-(6) inlier clusters after subtracting
  rotation.
- **Errors.** Each cloud's error is (vr84 − vr16)/2. The intrinsic dispersion is fitted for each
  version by maximum likelihood.

### 4.6 Robustness variants (T6)

**How labels are computed in each variant.**
- *T3, variants 1 and 2 (the likelihood changes):* new mocks, 2 nulls × 100, and the full rule of
  section 2. Compared with the main run's full-rule labels.
- *T3, variants 3–10 (same likelihood, reweighted or subset data, or a different curve):* the
  variant's maximum-likelihood fits, calibrated with the main run's rescaling factor d/m. No new mocks
  are drawn, so a reduced rule applies: "excluded strongly" uses the calibrated p and p_raw only, and
  "excluded" (and B = 1 "disfavoured") uses the calibrated p only. Compared with the main run's labels
  recomputed by the same reduced rule.
- *T4:* 1000 new mocks. Under variant 2 there is no inlier set, so T4 uses all clusters kept after the
  end-of-grid cut on the B = 0.5 fit's grid; in variant 2's T3 mocks every cluster is an inlier and is re-drawn.
- *T5:* 1000 bootstrap resamples. The T5 known-answer check is not repeated. Under variant 10, the
  clouds-only posterior is refitted with the new u₁.

**Variants.**
1. Outlier rule at 3σ per component instead of √3σ. In T5, the position-only cut at 3σ.
2. No outlier model: a plain Gaussian likelihood. In T5, all 125 clusters.
3. No kernel weights (T3, T4, T5).
4. Kernel bandwidth 50 pc.
5. Kernel bandwidth 200 pc.
6. Solar motion w☉ = 7.25 km/s instead of 7.8. Every v_z shifts by −0.55 km/s.
7. Orion left out: clusters with 180 < l < 220 deg and −25 < b < −5 deg, with l and b computed from
   x, y and z. This is a fixed box, defined here.
8. Leave out each `reference` catalogue in turn. The two catalogues with a single cluster each are
   pooled into one leave-out, because removing one cluster cannot change a fit measurably. That gives
   6 leave-outs.
9. Only clusters with `sigmavz` below the median.
10. Middle anchor of the baseline at its chord-length position, u₁ = d₀₁/(d₀₁ + d₁₂), instead of 0.5.

### 4.7 Cost and order

- **Work in the main run.**
  - 5 MCMC fits plus the T7 fit.
  - About 10 maximum-likelihood fits.
  - T3: 2 nulls × 100 mocks × 2 refits.
  - T4: 3 × 1000 mock evaluations, without refits.
  - T5: 1000 least-squares bootstrap fits, plus the known-answer check (60 mocks × 1000 resamples
    each).
- **Work in T6.** 15 variants (9 single-change variants, the 6 leave-outs counted separately). Each
  variant needs about 3 maximum-likelihood fits plus T4 and T5 at the counts above. Variants 1 and 2
  also need 2 × 100 T3 mocks with refits; variant 10 also needs one clouds-only MCMC.
- **Expected run time.** A rough estimate is 4–10 hours on one core; a short timing run measures it
  before the formal run.
- **Floors.** These counts are minimums and will not be reduced: 100 mocks per T3 null, 1000 T4 mocks,
  20 mocks per T5 injection, 1000 bootstrap resamples.
- **If the projected time exceeds 10 hours,** the run is checkpointed and continued in later idle
  periods. The counts stay as they are.
- **Scheduling.** The formal run waits until no other study is running.
- **Results files** (`results/`): `t1_t2.json`, `t3.json`, `t4.json`, `t5.json`, `t6.json`,
  `t7.json`, `t8.json`, `summary.json`. Each stays below 1 MB, with chains thinned or summarised.

### 4.8 Systematics we know about but do not test

- **Independent velocity data** (Zhu et al. 2024; Bobylev et al. 2025): out of scope (open question).
- **Our choices where K24 is not specific.** These are the kernel bandwidth, the curve
  parametrisation, the closest-point grid and our reading of the μ₀ prior. T6 covers the first two.
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

