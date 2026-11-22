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
- **Why χ²₂ at B = 1 although B ≤ 1.** Written as the 2 × 2 matrix of section 4.4, the wave is a scale
  times a rotation (B = 1) plus an anti-conformal part of size (1 − B) in magnitude and free angle
  φ + ω₀t. Near B = 1 that part is a free 2-vector around 0, so B = 1 is an interior point of a regular
  2-parameter family, not a one-sided boundary (wiki Part 3). The χ² reference is asymptotic only, so
  every decision also requires p_boot < 0.05 from the bootstrap distribution itself.
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
  - Each power mock's R is compared with the same N₄ standing mocks, and its p uses the same
    p_boot = (1 + k)/(1 + N₄).
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

### 4.9 Amendments before any fit (2026-11-21)

These points were fixed while implementing `run.py`, before any model was fitted to the data. They
settle choices that sections 2–4.8 left open; no rule or threshold above is changed. Each was fixed
before any fit to the data.

1. **Load-check weights** (section 3). The weighted mean uses the fixed kernel weights of section 4.1.
   Inverse-variance weights are undefined because three clusters have `sigmavz` = 0.0. The three means
   found while checking the loading: kernel-weighted −2.18 km/s (the decision value), unweighted −1.44 km/s, and
   inverse-variance with a 0.05 km/s floor +1.19 km/s; all pass. Fixed before any fit to the data.
2. **Variant 1 likelihood** (section 4.6). Each component's term becomes c = 3·tanh(x²/3), so the
   likelihood is Gaussian for small residuals and the outlier boundary is |x| > 3. Fixed before any fit
   to the data.
3. **T3 refit starts** (section 4.3). For the null refit, "the generating parameters" and "the data's
   best fit" are the same point, so it uses two distinct starts (that point and one prior draw). The
   B-free fit to the data also starts from both null optima, in addition to its 20 starts, so that
   2ΔlnL ≥ 0. Fixed before any fit to the data.
4. **Number of MCMC fits** (sections 4.2, 4.7). Eight in a full run: seven in the main run, namely columns (3), (4), (5), (6), and column (7) three
   times (K24's priors, broad priors, divisor fixed at 74), plus one for variant 10 (column (3) with the
   chord-length u₁). The T7 fits are maximum-likelihood fits. Fixed before any fit to the data.
5. **Chain-length rule** (section 4.2). The post-burn length is compared with 50 times the largest
   autocorrelation time. A rerun doubles both the steps and the burn-in. Fixed before any fit to the data.
6. **T8 divisor-74 variant** (section 2, T8). It is run under K24's priors. Fixed before any fit to the
   data.
7. **Known-answer placement** (section 4.4). Each selected cluster is placed at the injected model's
   point closest to its 3-D position (x, y, z), so no velocity is used. Fixed before any fit to the data.
8. **T5 bootstrap** (section 4.4). Each resample draws from all input clusters (all 125 for the data;
   the mock set for a known-answer mock) and reapplies the end-of-grid drop and the position cut. "End
   of the grid" means the first or last valid grid point (p − γs > 0). Fixed before any fit to the data.
9. **Kernel weights in variants** (sections 4.1, 4.6). They are recomputed for each variant's data under
   K24's column-(6) medians, including subsets, the shifted v_z of variant 6 and the chord curve of
   variant 10. Fixed before any fit to the data.
10. **Point estimates.** T7 (a) uses the column-(6) maximum-likelihood fit. Θ₂ is computed from each
    version's own inliers. All 79 clouds are used in T7. T1's inlier set comes from the posterior-median
    parameters. The maximum-likelihood fit at B = 0.5 starts from the column-(5) MCMC median with B set
    to 0.5. Fixed before any fit to the data.
11. **Eq. 13 constant.** The term 3 ln(2πσ²) is kept as printed, although the distance vector has four
    components. With σ fixed it cancels in every comparison. Fixed before any fit to the data.
12. **Residual-resampling T3 variant** (section 4.3). It is kept, with full refits of 2 nulls × 100
    mocks. It adds about 3 hours, which section 4.7 did not count. Fixed before any fit to the data.
13. **Checkpoint storage** (section 4.7). Checkpoints are kept outside the project folder. For an MCMC
    fit they hold only the walkers' last state and the post-burn chain thinned by 10. The
    autocorrelation time is estimated on that thinned chain and multiplied by 10. Stored chain samples are float32. The running state is
    deleted once a chain is finished. The checkpoint folder of a formal run is deleted after all results are
    written; an exploration keeps its own folder and never touches the formal run's. Fixed before any fit to the data.
14. **Cost estimate** (section 4.7). Measured on synthetic data of the real size, one likelihood
    evaluation takes about 1.2 ms (clusters) or 1.9 ms (clusters and clouds). The projected upper bound
    for the whole run is about 16 hours on one core: T3 mocks 6.2 h, T6 8.6 h, MCMC 0.9 h. As section
    4.7 already says, the run therefore pauses at 10 hours and is resumed in a later idle period; the
    counts are unchanged. Fixed before any fit to the data.
15. **Known property of b̂.** On synthetic known-answer mocks, b̂ is biased low: its mean is 0.565 at
    B = 0.84 (target 0.68) and 0.785 at B = 1. The known-answer check may therefore fail, which makes
    the b̂ label "undetermined". The rule is unchanged. Found and recorded before any fit to the data.

### 4.10 Addendum 2026-11-21: R-CONV, the baseline convention, and T8-P, a proper ω₀ test (T-056), pre-registered before any of these fits

*Why.* The formal run (section 5) reproduced column (4) only partly (3 of 6) and did not reproduce the clouds-only
column (3) (2 of 6: inside s₀ +0.22σ and γ −0.98σ; outside A −1.40σ, p −1.41σ, δ −2.11σ, φ +3.73σ; anchors x₀ −1.50σ,
y₀ −2.08σ) or column (6). Column (3) uses cloud positions only (no velocities, no B, no outlier model), so the
difference must lie in the geometry, its conventions or the likelihood's width; the referee (section 6, points 2, 3 and
11) proposed finding the convention that reproduces column (3), then rerunning T1 and a T5 known-answer check injected
on our own fit. Separately, T8 was withdrawn because the free-ω₀ likelihood is ill-posed (section 6, point 1); its open
question asks for a likelihood in which ω₀ is identified. **Both parts are added after the formal results were seen and
are labelled post hoc throughout.**

*K24's text, rechecked (arXiv v1 PDF, Methods pp. 10–14 and Extended Data Tables 1–2, read 2026-11-21).*
- σ: "σ² is calculated as 0.5 times the standard deviation of d²_min" (after eq. 11), where d²_min = Σᵢ d²_cloud,i
  (s_min) for the clouds, said to be χ²-distributed with two degrees of freedom; this gives "a radius of the Wave of 47
  pc". For clusters "the scatter parameter σ remains the same as in the molecular cloud discussion". The notation is
  ambiguous: a single sum over clouds is one number, with no standard deviation, and the χ²₂ statement fits the squared
  3-D distance of one cloud to the curve (two components perpendicular to it), so we read d²_min as the per-cloud
  values d²_cloud,i(s_min) = Δx² + Δy² + Δz² and the standard deviation as taken over the clouds. When σ is
  evaluated (once, or at every parameter vector) is not stated, nor whether the standard deviation is weighted.
- Baseline: "a quadratic function in x and y described by three anchor points" (x₀, y₀), (x₁, y₁), (x₂, y₂); "s = 0
  pc at the beginning of the Wave (near CMa OB1)". The parametrisation of the quadratic and whether the curve extends
  past the anchors are not stated.
- Weights: a Gaussian kernel density estimate "whose bandwidth is chosen to be a few percent of the total length of the
  Wave", normalised to the number of objects; when the weights are computed is not stated.
- Priors (Extended Data Table 1): as section 4.1 uses them; in particular ln(δ/pc) ~ N(6.5, 0.1), centred on 665 pc.
- Column (7): the fourth entry of d_cluster is v_z/ω₀ (eq. 12) and eq. 13 has no ω₀ term, so K24's own free-ω₀ fit
  has the property for which our T8 was withdrawn.

*Seen before this addendum.* All of sections 5–7 and log.md, in particular every T1 number of the formal run
(`t1_t2.json`, including `col3_for_reference`: our column-(3) δ = 666 pc sits on the prior centre, against K24's 798),
every T5 and T8 number (the formal `col7_div`, divisor 74 under K24's priors: ω₀ = 71 +10/−8, half-width in ln ω₀
about 0.12, above the 0.085 limit). From gate-1 review of this addendum (no fit): at K24's published column-(3)
medians, on our formal curve, the 79 clouds give σ = 59.7 pc by "0.5 × the standard deviation of d²" (58.9 kernel-
weighted), not K24's 47; and only 1 of the 79 clouds has s < 0. No fit under any convention below has been run; no
code for this addendum exists.

*Part A, R-CONV: which convention reproduces column (3)?* Sixteen conventions, all combinations of three factors (the
first option of each is the formal run's; the index is baseline·4 + σ·2 + weights, with the options numbered 0, 1, …
in the order listed):
- **Baseline (four options).** L: the parametric Lagrange curve P(u) through the anchors at u = 0, 0.5, 1 (section
  4.1). C: the same with the middle anchor at its chord-length position (variant 10). Y: y as the quadratic function of x
  through the three anchors (requires x₀ < x₁ < x₂ or x₀ > x₁ > x₂; otherwise zero likelihood). X: x as the quadratic
  function of y through the three anchors (same monotonicity condition in y), since "a quadratic function in x and y" is
  symmetric in its wording and the Wave spans more in y than in x. In every option the curve runs from 0.2 of the
  anchor span before anchor 0 to 0.4 after anchor 2 (the formal extent; in the parameter u, x or y respectively), and s
  is the arc length in the x–y plane from anchor 0, on 2,000 grid points. The formal run's extent is kept because only 1
  of 79 clouds has s < 0 at K24's medians, so starting the curve at anchor 0 would change little.
- **σ (F / P).** F: σ = 47 pc fixed. P: at each parameter vector, σ² = 0.5 × the (unweighted) standard deviation of the
  79 clouds' squared distances d²_cloud,i(s_min) (K24's sentence read per evaluation, d²_min read as the per-cloud
  values), used in eq. 11 including its ln(2πσ²) term. P is a reading of K24's words, not a way to reach 47 pc: at
  K24's medians it gives about 60 pc on our curve (above), and a larger σ flattens the likelihood towards the priors,
  which is why the width condition below is part of the label.
- **Weights (W / R).** W: fixed, from each object's s under K24's column-(6) medians (section 4.1). R: recomputed at
  each parameter vector from that vector's s (same kernel, bandwidth 100 pc); for clusters, from the s of the 4-D
  closest point.

For each convention: the column-(3) MCMC exactly as section 4.2 (48 walkers, 6,000 steps, burn 2,000, doubling if
shorter than 50τ, then flagged), with seed (`seed`, 3000 + index); T1's column-(3) count, how many of A, p, δ, s₀, γ, φ
have their posterior median inside K24's 16–84% interval (Extended Data Table 2, column 3); the σ-scaled differences of
all 12 shape and anchor parameters; and the **width ratio**, the median over the six counted parameters of our
16–84% half-width divided by K24's. `results/rconv.json` reports all sixteen counts, differences and ratios.

*Choice of the convention (fixed now).* (i) If no convention has a count ≥ 3, Part A reads "not reproduced under any
candidate convention" and stops. (ii) Otherwise, among the conventions with a count ≥ 3 whose width ratio lies in
[2/3, 3/2], the one with the largest count is chosen; (iii) if none of the conventions with a count ≥ 3 has its width
ratio in that range, the one with the largest count among them is chosen (its label is then "partly reproduced", with
the reason). Ties are broken by the number of factors that differ from the formal run (L, F, W), fewest first, then by
the index. Labels (each says "best among these 16 candidate conventions, post hoc"):
- **"column (3) reproduced under <convention>"** if its count is ≥ 5 and its width ratio lies in [2/3, 3/2];
- **"column (3) partly reproduced under <convention>"** if its count is 3–4, or ≥ 5 with the width ratio outside
  [2/3, 3/2] (then the reason is stated);
- **"column (3) not reproduced under any candidate convention"** in case (i) (every one of the 16 counts ≤ 2); then
  Part A stops here and nothing is rerun.

*Reruns under the chosen convention (only if reproduced or partly reproduced).* σ is 47 pc for every cluster fit and
for T5 under every convention (K24 print 47 pc and say the clusters keep it; under P only the column-(3) clouds
likelihood changes). Column (4), column (5) and column (6) MCMC as section 4.2; T1 for columns (4) and (6) by section
2's rule (labels "under <convention>, post hoc"); T5 as section 4.4 (position-only cluster selection on the chosen
convention's column-(3) median curve with the √3 × 47 pc cut, 1,000 bootstrap resamples, the wavelength and b̂ rules).
Its known-answer check injects on the **same curve the analysis uses**: the chosen convention's column-(3) posterior
median (anchors and A, p, δ, s₀, γ, φ), with ω₀t from our column-(5) posterior median under that convention and B =
0.5, 0.84 and 1.0, 20 mocks per injection, 47 pc noise as in section 4.4, and the pass rule of section 2. The mock noise
(47 pc on all four components) may still make the mocks noisier than the data, so the check may again be uninformative;
the coverage and mean b̂ per injection are reported either way. These labels are reported **next to** the formal run's;
the formal labels, the overall reading and T6 stay as recorded. T3, T4, T6, T7 are not rerun.

*Part B, T8-P: ω₀ with the divisor fixed (post hoc).* The column-(7) setup (ω₀, μ₀, r₀ free) with the v_z divisor
**fixed at 74 km s⁻¹ kpc⁻¹**, under the formal run's convention (L, F, W). Then ω₀ enters only the model mean of v_z
(through the frequency ω(z_max, r) of eq. 3), and the likelihood's dependence on ω₀ is through the model alone, so the
withdrawn T8's problem (ω₀ rescaling the data's velocity component) is absent. MCMC as section 4.2 under K24's priors
(the formal `col7_div`, rerun so both chains come from this run) and under the broad priors of section 2 (new).
Section 2's T8 rule applied unchanged (half-width of the broad-prior ln ω₀ posterior against 0.085; median shift
against 0.5σ) → **"data-driven"**, **"partly data-driven"** or **"prior-driven"**, reported as T8-P (post hoc) with ρ₀
and the Sun's vertical period under both priors. Because the tanh cap lets the likelihood plateau at large ω₀, the
broad-prior posterior's distance from the 150 km s⁻¹ kpc⁻¹ bound is reported; under the broad priors only, if its
median lies within 5% of a bound's value (above 142.5 or below 31.5 km s⁻¹ kpc⁻¹), T8-P is "prior-driven (posterior
at the bound)", and this takes precedence over the width and shift rule. The withdrawn T8 stays withdrawn.

*Expected outcome (stated now).* Part A: we expect Y, X or P to move the anchors by about 100 pc; the count could reach
4–6, but P may raise it only by widening the posteriors, which the width condition catches; an even chance that column
(3) is reproduced; if so, column (4) likely reproduced, and the known-answer check more likely to pass, with b̂'s label
still likely "undetermined". Part B: the K24-prior chain already gave a half-width of about 0.12 (above 0.085), so
"data-driven" is very unlikely; "prior-driven" or "partly data-driven" is the likely label.

*Cost.* Sixteen column-(3) MCMC runs (about 0.6–1.2 ms per likelihood; with the doubling about 9–17 min each, 2.5–4.6 h
in all); the reruns about 1–1.5 h; Part B about 1 h. In all about 5–7 h single-threaded, with the formal run's pause at
`stop_after_hours` and checkpointed resume (section 4.9, item 13). Cache only, no download.

*Code checks before the formal run (synthetic data only).* Y and X give the same curve as L when the anchors are
equally spaced on a straight line; C equals variant 10's curve; s is the x–y arc length in every option; P's σ equals
47 pc within 1% for 10⁵ synthetic clouds drawn with σ = 47 pc about a known curve (K24's χ²₂ argument); R's weights
equal W's at K24's column-(6) medians; with the divisor fixed, changing ω₀ changes only the model v_z (the data vector
and the eq. 13 constant are unchanged); the tie-break order and the width condition; the T5 known-answer injection uses
the stated vector. On the real data before the formal run only the load check.

*Switch and code.* New parts `"conv"` (Part A) and `"t8p"` (Part B) in `PARAMS["parts"]`, run alone in a formal run
(the other parts' results are read, never written); results `results/rconv.json` and `results/t8p.json` (each below 1
MB), keys `R_CONV` and `T8_P` in `summary.json` (other keys byte-identical); `wave011.py` gains the C, Y and X
baselines, the P σ and the R weights as options (defaults unchanged, so the formal results reproduce), tests,
conclusion checks, a web section, section 8 knobs. None of this exists yet.

*Amendments before any R-CONV or T8-P fit (2026-11-21).* These settle implementation choices that this addendum left
open, fixed while writing the code and before any R-CONV or T8-P fit to the data; no rule, threshold or label above
changes.
1. **Seeds.** The column-(3) chain of convention i starts from the integer seed drawn first from NumPy's generator
   seeded with the sequence (`seed`, 3000 + i). Every other new chain gets its seed from (`seed`, its name) as in the
   formal run: `conv<NN>_col4`, `conv<NN>_col5`, `conv<NN>_col6` for the reruns, `t8p_k24` and `t8p_broad` for Part B.
   The K24-prior chain of Part B is therefore a new chain of the formal `col7_div` setup, not a copy of it. Walkers
   start around K24's medians of the column fitted, as in the formal run.
2. **Y and X curves.** The independent coordinate (x for Y, y for X) runs linearly in the grid parameter t, from
   t = −0.2 to 1.4 with t = 0 at anchor 0 and t = 1 at anchor 2, on 2,000 points equally spaced in t; s is the
   trapezoid integral of the analytic x–y speed, as for L. Equal coordinates of anchors (for example x₀ = x₁) count as
   not monotonic.
3. **σ under P.** The standard deviation is the population one (ddof = 0) over all clouds, unweighted. If it is zero or
   not finite, the likelihood is zero. The kernel weights (W or R) still multiply each cloud's term of eq. 11, as in
   section 4.1. In the three cluster reruns σ is 47 pc under every convention.
4. **Weights under W and R.** Under C, Y and X the fixed weights W come from each object's s on that convention's own
   curve at K24's column-(6) medians (as amendment 9 of section 4.9 does for variant 10). Under R the weights of each set
   (clusters, clouds) are recomputed from that set's own closest points (clusters 4-D with the divisor 74, clouds 3-D) and
   normalised to the number of objects in the set, as in section 4.1.
5. **Width ratio.** K24's half-width is (plus + minus)/2 as printed in Extended Data Table 2 column (3); ours is
   (p84 − p16)/2; δ and γ in linear units, as the table prints them. Both ends of [2/3, 3/2] are inside.
6. **Reruns.** T5 includes section 4.4's ω₀ = 68 sensitivity check. The known-answer injection keeps the adopted ω₀,
   μ₀ and r₀ (74 km s⁻¹ kpc⁻¹, 1.3 kpc⁻¹, 3.7 kpc) of the column-(3) fit, and each selected cluster is placed as in
   amendment 7 of section 4.9, on the injected model of the chosen convention's curve. The clusters are selected on that
   curve by the √3 × 47 pc position cut.
7. **Names in labels.** A convention is written `<baseline>-<σ>-<weights>`, for example `Y-P-W`, in the labels and in
   `rconv.json`. The rerun labels end with "under <convention>, post hoc".
8. **T8-P bound rule.** The broad-prior median of ω₀ is exp(median of ln ω₀); "within 5% of a bound" uses strict
   inequalities, median > 0.95 × 150 = 142.5 or median < 1.05 × 30 = 31.5 km s⁻¹ kpc⁻¹. ρ₀ and the Sun's period use 2,000
   posterior draws, as in T8.
9. **Standalone runs.** A formal run takes `parts = ["conv"]` or `["t8p"]` alone, R-CONV with all 16 conventions, and
   refuses to start unless `summary.json` exists and re-serialises byte-identically. It writes `rconv.json` or `t8p.json`
   (with the load check and `params`), puts `R_CONV` or `T8_P` into `summary.json` before `overall`, and keeps its
   records apart (`provenance_conv.json`, `run_info_conv.json`; `_t8p`; a paused attempt `_convpaused`, `_t8ppaused`).
   Checkpoints go to `s011_checkpoints/<conv|t8p>/<key>`, so a finished part never deletes the other's. An exploration
   may fit a subset of the conventions (`conv_indices`); then `rconv.json` says `complete_set: false` and the choice is
   over that subset.

## 5. Results

Formal run of 2026-11-21 (`results/`, page `web/index.html`). It paused at 10 h by the pre-registered
rule (section 4.9) and was resumed from its checkpoints: 36,004 s + 1,617 s, about 10.5 h in all,
single-threaded. Load check: weighted mean v_z = −2.18 km/s (limit 3), pass. All numbers below are in
`results/summary.json` unless another file is named.

**Overall reading (section 2): "mixed".** Support: T1 (column (4) partly reproduced) and T3 (standing
excluded). Do not support: T6 (fragile). Undetermined: T4 and T5.

| Test | Result | Label |
|---|---|---|
| T1 column (4) | 3 of 6 medians inside K24's 16–84%: A 214 ± 11 (K24 217), δ 605 (624), γ 1.44 (1.40) inside; p 4420 ± 200 (4752), s₀ 490 ± 90 (673), φ 0.14 ± 0.14 (−0.23) outside. Inliers vs the table's flag: 78 both, 1 ours only, 11 table only (`t1_t2.json`) | partly reproduced |
| T1 column (6) | 2 of 6 inside (A, s₀); p 4420 (4780), δ 630 (740), γ 1.38 (1.46), φ 0.12 (−0.15) outside | not reproduced |
| T2 | B = 0.84 (0.78–0.91), K24 0.84 (+0.07/−0.06); P(B > 0.95) = 0.065; P(B < 0.5) = 5×10⁻⁵; ω₀t = −0.35 (−0.53 to −0.14) | (no label) |
| T3 standing | 2ΔlnL = 20.24; mock mean m = 4.45 (d = 1), calibrated p = 0.033, p_raw = 7×10⁻⁶, p_boot = 0.0099 (0 of 100 mocks reach it) | standing excluded |
| T3 B = 1 | 2ΔlnL = 6.39; m = 3.45 (d = 2), calibrated p = 0.157, p_raw = 0.041, p_boot = 0.178 | pure travelling not disfavoured |
| T4 | R_obs = 0.377 over 75 inliers of the B = 0.5 fit; p = 0.299; power from B = 1 mocks 0.41 (B-free mocks 0.33) | undetermined (power < 0.8) |
| T5 wavelengths | k_z/k_vz = 0.75, 95% interval 0.62–4.09 (98 clusters kept) | undetermined |
| T5 b̂ | b̂ = 0.53, interval 0.39–0.61 (contains neither 0 nor 0.68); Δ = 1.07 rad, ρ = 0.71. Known-answer check **failed** at B = 1 (median mock b̂ 0.42, interval 0.04–0.76, not above 0.4), so the label is undetermined by rule | undetermined |
| T6 | 9 of 15 variants change at least one label (table below) | fragile |
| T7 | −2 ln L_max: (a) B = 1 460.0, (b) v_z = 0 449.3, (c) B = 0.5 435.8 (79 clouds); (a) is the worst of the three, by 10.6 and 24.2: the rule has one direction only, and the CO data, if anything, go against the B = 1 model | CO does not distinguish |
| T8 | ω₀ = 113 (+18/−16) km s⁻¹ kpc⁻¹ under K24's priors, 138 (+8/−15) under broad priors; broad half-width 0.089 in ln ω₀ (limit 0.085); shift −2.2σ. **Withdrawn as uninformative (post hoc, referee point 1):** with ω₀ free the likelihood is ill-posed in ω₀ (no ln ω₀ normalisation; with it, unbounded as ω₀ → 0), and in mode searches the posterior goes to a bound (broad priors) or to 117 and 4.2 km s⁻¹ kpc⁻¹ without and with the normalisation (K24's priors) | prior-driven (withdrawn) |

**T6 variants** (labels: T3 standing / T3 B = 1 / T4 / T5 wavelengths / T5 b̂; `t6.json`). The main
run's labels are the same under the full and the reduced rule: standing excluded / not disfavoured /
undetermined / undetermined / undetermined.

| Variant | Clusters | 2ΔlnL standing, B = 1 | Changed labels |
|---|---|---|---|
| 1 outlier rule 3σ | 125 | 53.5, 14.1 | T3 standing → excluded strongly; B = 1 → disfavoured (calibrated p 0.007, p_boot 0.030); T4 → not excluded by the phases (p 0.058, power 0.99) |
| 2 no outlier model | 125 | 57.6, 13.3 | T3 standing → excluded strongly |
| 3 no kernel weights | 125 | 5.4, 0.01 | T3 standing → not excluded (calibrated p 0.27) |
| 4 bandwidth 50 pc | 125 | 17.5, 5.1 | none |
| 5 bandwidth 200 pc | 125 | 24.8, 7.6 | none |
| 6 w☉ = 7.25 km/s | 125 | 20.4, 6.0 | none |
| 7 Orion left out | 67 | 1.2, 1.9 | T3 standing → not excluded (calibrated p 0.61) |
| 8 leave out Cantat-Gaudin+2020 | 88 | 12.3, 3.5 | T3 standing → not excluded (0.096) |
| 8 leave out Hao+2022 | 102 | 15.2, 4.7 | T3 standing → not excluded (0.065); T4 → not excluded by the phases (p 0.16, power 0.84) |
| 8 leave out He+2022 | 82 | 14.8, 5.9 | T3 standing → not excluded (0.068) |
| 8 leave out Liu+2019 | 120 | 18.4, 6.1 | none |
| 8 leave out Sim+2019 | 110 | 15.2, 2.7 | T3 standing → not excluded (0.064) |
| 8 leave out Castro-Ginard+2021 and Szilágyi+2021 | 123 | 20.5, 1.8 | none |
| 9 σ_vz below the median | 59 | 2.3, 1.6 | T3 standing → not excluded (0.47) |
| 10 chord anchor u₁ | 125 | 21.2, 5.7 | none |

No variant changes a T5 label (both stay undetermined; the failed main-run known-answer check makes
every variant's b̂ undetermined by rule).

**Reported alongside (not labels).**
- T3 with residual resampling instead of Gaussian mocks (section 4.3): standing p_cal 0.028 and p_boot
  0.0099 (excluded); B = 1 p_cal 0.019, p_boot 0.030 (disfavoured). The pre-registered label uses the
  Gaussian mocks. T4 with residual mocks: p = 0.84, power 0.02.
- T5 with ω₀ = 68 km s⁻¹ kpc⁻¹: b̂ = 0.56 (0.39–0.65).
- T5 known-answer coverage over all 20 mocks: 0.85 at B = 0.5 (covers 0), 0.40 at B = 0.84 (covers
  0.68), 0.00 at B = 1 (above 0.4); mean mock b̂ −0.16, 0.31, 0.39 at the three injections: b̂ is biased
  low by about 0.3–0.6 at large B, as anticipated in section 4.9. The mocks inject K24's column-(6)
  curve while the analysis uses our column-(3) curve, and are far noisier than the data, so the failed
  check says the check is not informative, not that b̂ on the data is biased by this much (section 6,
  point 3).
- T8 with the v_z/ω₀ divisor fixed at 74: ω₀ = 71 (+10/−8) km s⁻¹ kpc⁻¹, close to K24's 67.7; this
  is the only meaningful T8 number (section 6, point 1), fitted under K24's priors only (whether the
  data or the prior sets it is not tested). The free-ω₀ values of ρ₀ and the Sun's period
  in `t8.json` are not results.
- MCMC: every chain (columns 3–7, broad and divisor variants) was rerun at 12,000 steps and is still
  flagged `chain_short`: the longest autocorrelation time is 199–467 steps, so the 8,000 post-burn
  steps are 17–40 τ, below the 50 τ target. Medians are reported as they are; the T1 comparisons and
  T8 widths carry this caveat.

**What this means.** With K24's own data and model, our fit finds B ≈ 0.84 like theirs, and the
likelihood ratio prefers a travelling-type wave over a standing one in the main analysis. But that
preference rests on a minority of the clusters: leaving out the Orion region (58 clusters) or the
kernel weights removes it (2ΔlnL 1.2 and 5.4), and so does leaving out the clusters with larger v_z
errors (2.3); leaving out any of four source catalogues keeps 2ΔlnL at 12–15 but drops it below the
exclusion threshold (calibrated p 0.06–0.10). The phase-spread test (T4) has too little power to decide,
and the model-free b̂ (T5) cannot be read because the known-answer check fails at B = 1. T8's
free-ω₀ reading is withdrawn (section 6, point 1); with the divisor fixed, ω₀ = 71 km s⁻¹ kpc⁻¹, close
to K24's 67.7. The CO velocities, if anything, fit the B = 1 model worse than v_z = 0. Our column (4)
reproduction matches 3 of K24's 6 shape parameters; the wavelength p comes out about 330 pc
(1.7σ) shorter and the phase φ differs by 0.37 rad, so the remaining tests refer to our implementation.

## 6. Referee notes

### Referee of the formal run (2026-11-21)

The independent referee was a subagent. It saw README sections 1–4, the code and `results/*.json`, but
not sections 5–8, `log.md` or the wiki; it read K24's Methods to check eqs. 1–13 and ran only short
read-only inspections of the JSON. It found the labels computed as pre-registered, with no moved
goalposts, and one likelihood problem in T8. Triage (each point checked against the code and results):

| # | Point | Verified | Action |
|---|---|---|---|
| 1 | T8: with ω₀ free, the fourth component is v_z/ω₀ at fixed σ, and the likelihood has no −Σ w_k ln ω₀ normalisation, so a larger ω₀ shrinks every velocity residual at no cost; amendment 11's "cancels in every comparison" is false for T8. The free-ω₀ posteriors (113 under K24's priors, against K24's 67.7; 138 piled against the broad bound of 150) would be artefacts | yes (`wave011.py` `Model.evaluate`; `run.py` `setups`, `col7` and `col7_broad` with `divisor=None`). A post-hoc check (`explore/t8_jacobian.py`, 2026-11-21, posterior modes, not in `results/`): without the term the mode is ω₀ = 117 (K24's priors) and 150, the upper bound (broad); **with** the term it runs to 4.2 and to 30, the lower bound, because K24's truncation tanh(x²) is bounded, so a small ω₀ turns every v_z residual into a capped outlier while the normalisation keeps growing | **Accepted, post hoc (2026-11-21):** the free-ω₀ likelihood of eq. 13 with K24's bounded outlier function is ill-posed in ω₀: without the normalisation it is not a density of v_z, and with the normalisation it grows without bound as ω₀ → 0, because every v_z residual is then capped by tanh(x²) (this part is analytic). In the explored mode searches the posterior went to a bound under the broad priors in both forms, and under K24's Gaussian priors the modes are 117 without and 4.2 with the normalisation; the searches show boundary-seeking, not a proof that the formal likelihood has no finite-ω₀ information. The T8 label "prior-driven" is computed by the rule but **withdrawn as uninformative** (it reflects the likelihood's construction, not the data), and the derived ρ₀ and solar periods are not reported as results. Only the variant with the divisor fixed at 74 (ω₀ = 71 +10/−8, close to K24's 67.7) is meaningful; it was fitted under K24's priors only, so whether the data or the prior sets it is not tested. How K24 handled this is not stated in eq. 13. T8 does not enter the overall reading, which is unchanged |
| 2 | The clouds-only fit (column (3)) is not reproduced either (counted parameters outside: A −1.4σ, p −1.4σ, δ −2.1σ, φ +3.7σ; anchors x₀ −1.5σ, y₀ −2.1σ; corrected 2026-11-21, T-056 gate 1: the anchors are not among the six counted parameters; the convention search is pre-registered in section 4.10, T-056), so a geometry or convention difference sits upstream of every test (grid u ∈ [−0.2, 1.4], fixed weights, fixed σ = 47 pc); the same shift appears in columns (4) and (6); column (4) is one parameter away from "not reproduced" | yes (`t1_t2.json` `col3_for_reference`: 2 of 6 inside) | **Accepted limitation**: section 5 says T3–T5 refer to our implementation; finding the convention that reproduces column (3) is registered as an open question (section 7) |
| 3 | The T5 known-answer mocks inject K24's column-(6) medians (ω₀t = −0.38) while the analysis curve and the position cut come from our column-(3) median, which differs by ~100 pc and ~0.5 rad; the mocks are much noisier than the data (data b̂ interval 3× narrower than a typical mock's; the B = 0.84 "pass" has interval [−0.57, 0.72]) | yes (`run.py` `t5_known_answer`; `t5.json`) | **Accepted**: the check's failure means the check is not informative about the data, not that b̂ on the data is biased by the mock amount. The b̂ label would be "undetermined" anyway (lower end 0.388 < 0.4). Section 5 wording changed accordingly |
| 4 | T3 searches harder on the data than in each mock (22/20 starts against 4/2); the likelihood surface is rugged. The mock 2ΔlnL distribution is not a scaled χ²₁ (median 3.5 against 2.0 for the same mean), so p_cal = 0.033 is approximate; the empirical tail (0 of 100 mocks reach 20.2) is stronger | yes (`run.py` `t3_mocks`; `t3.json`) | **Accepted limitation** (pre-registered numbers of starts); direction of the bias unknown |
| 5 | T3's preference for travelling rests on few clusters: without the Orion box (which removes 58 of 125 clusters, far more than the Orion complex) 2ΔlnL = 1.2 and for the low-σ_vz half 2.3, against about 11 and 9.5 expected pro rata | yes (`t6.json`) | **Accepted**; stated in section 5 |
| 6 | The noise model matters: with residual resampling, pure travelling becomes "disfavoured" (p_boot 0.030) and T4's power falls to 0.02; R_obs = 0.377 is at the 30th percentile of standing mocks and the 95th of B = 1 mocks, i.e. the phases look, if anything, more like a standing wave, though the best-measured half (variant 9) gives R = 0.043, p = 0.001 | yes (`t3.json`, `t4.json`, `t6.json`) | **Accepted**; reported in section 5 (no label changes) |
| 7 | MCMC chains are 17–40 τ after the reruns (target 50 τ), τ estimated on a thinned chain; effective sample sizes ~800–1,900 are adequate for T1/T2 medians (no T1 parameter within 0.23σ of its interval edge) | yes (`t1_t2.json`, `t8.json` `chains`) | **Accepted**; disclosed in section 5 |
| 8 | T6 "fragile" follows the rule; several changes are within 1–2 Monte Carlo errors of a threshold, but variants 3, 7 and 9 (calibrated p 0.27, 0.61, 0.47) are decisive. The reduced rule cannot tell a real change from lost power in a subset | yes | **Accepted**; the label stands |
| 9 | T7: the label "does not distinguish" is right by the one-directional rule, but the CO data go against (a): the B = 1 model's −2 ln L is worse than v_z = 0 by 10.6 and than the B = 0.5 fit by 24.2 (the latter also differs in geometry and Θ₂) | yes (`t7.json`) | **Accepted**; stated in section 5 |
| 10 | Literature: Zhu et al. 2024 (arXiv:2402.15346; gas and stars oscillate out of sync), Li & Chen 2022 (arXiv:2112.08390; standing or one-way travelling both consistent), Tu et al. 2022 (arXiv:2208.06469), Alves et al. 2020 (baseline conventions) | Zhu et al. 2024 is cited in the wiki; the others unverified (IDs from the referee) | Noted |
| 11 | Most important additional test: find the convention that reproduces column (3), then rerun T1 and a T5 known-answer check injected on our own fit | – | Open question (section 7) |

## 7. Open questions

- Which convention reproduces K24's clouds-only fit (column (3))? Candidates: the curve starting at
  u = 0 rather than −0.2, σ estimated from the spread of d² as K24 describe, kernel weights recomputed at
  each parameter vector. Then rerun T1 and a T5 known-answer check injected on our own fit, so injection
  and analysis share one curve (referee, section 6, points 2, 3 and 11).
- T8 needs a likelihood that is proper in ω₀ when the v_z divisor is fitted (for example an untruncated
  velocity term, or a fixed divisor with ω₀ entering only through the frequency); as pre-registered it
  is uninformative (section 6, point 1).

## 8. Exploring via chat

How a coding agent answers "what if" questions about this study without touching `results/`
(rules: AGENTS.md section 2).

| Knob (`PARAMS`) | Meaning | Safe range | Cache only, or new data (size)? |
|---|---|---|---|
| `parts` | which tests to run (`t1t2`, `t3`, `t4`, `t5`, `t6`, `t7`, `t8`); the column-(3)–(6) chains always run | any subset | cache only (the two tables, 16 KB) |
| `parts` = `["conv"]` or `["t8p"]` | README 4.10's post-hoc R-CONV (16 column-(3) conventions, the choice, the reruns) or T8-P (ω₀ with the divisor fixed at 74); standalone: never with the other parts, which are only read | one of them (both together only in an exploration) | cache only |
| `conv_indices` | which conventions R-CONV fits (index = baseline·4 + σ·2 + weights; baseline L, C, Y, X; σ F, P; weights W, R) | any subset in an exploration; a formal run needs all 16 | cache only |
| `conv_seed_offset`, `conv_min_count`, `conv_repro_count`, `conv_width_range`, `t8p_bound_frac` | R-CONV seeds and choice rule, T8-P bound rule (pre-registered values, README 4.10) | changed only in an exploration | cache only |
| `variants` | T6 variants to run | any subset of the ten names | cache only |
| `bandwidth_pc` | kernel bandwidth of the weights (pc) | 30–300 | cache only |
| `sigma_pc` | common scatter σ of the likelihood and the mock noise (pc) | 30–80 | cache only |
| `t5_b_t`, `t5_band`, `t5_cut_sigma` | T5 b̂ threshold, wavelength band, position cut (in σ) | 0–0.9; around [0.8, 1.25]; 1–5 | cache only |
| `t5_omega0_sens_kms_kpc` | ω₀ in ω(s) for the T5 sensitivity check | 60–90 | cache only |
| `t3_mocks`, `t4_mocks`, `t5_boot`, `t5_ka_mocks` | mock and bootstrap counts (below the floors of 4.7 only for quick looks) | 10 up to the defaults | cache only |
| `mcmc_steps`, `mcmc_walkers`, `ml_starts`, `ml_nm_maxfev` | sampler and optimiser effort | shorter for quick looks | cache only |
| `t8_broad_omega0_kms_kpc`, `t8_broad_mu0_kpc`, `t8_broad_r0_pc` | T8 broad prior ranges | wider or narrower | cache only |
| `sun_vz_kms` | the Sun's vertical velocity for its period (km/s) | 7–8 | cache only |
| `stop_after_hours` | pause after this long; rerunning continues from the checkpoints (0 = no limit) | any | cache only |

- Rerun with an override: `python -m astrolab explore 011-m11-radcliffe-wave-oscillation --tag <topic> --set KEY=VALUE`
  (outputs in `explore/<date>-<topic>/`, not committed). A full run takes many hours (README 4.7), so set
  `parts` and the counts for a quick look. An exploration keeps its own checkpoints in the astrolab cache
  folder (`s011_checkpoints/explore/<date>-<topic>/<key>`) and never reads or deletes the formal run's.
  The formal run deletes its checkpoints once all results are written, so every exploration recomputes
  what it needs. At the default counts, the column-(3)–(6) chains and the three T3 maximum-likelihood
  fits always run (about 40 minutes on one core). `parts='["t5"]'` (for example with a new `t5_band`) then
  takes about 45 minutes in all, `parts='["t7"]'` about 50 minutes, and `parts='["t8"]'` (for example with
  a new `sun_vz_kms`) about 70 minutes. Rerunning the same date, tag and PARAMS resumes from the
  exploration's checkpoints; delete that folder by hand when done.
- **R-CONV and T8-P (README 4.10, post hoc).** Formal procedure: after the formal full run (its `summary.json` must
  exist), set `"parts": ["conv"]` in `PARAMS` (committed, with a line in `log.md`), run
  `python -m astrolab run 011-m11-radcliffe-wave-oscillation`, and rerun the same command after each pause at
  `stop_after_hours` until it completes (it resumes from `s011_checkpoints/conv/<key>` and deletes that folder when done);
  then the same with `["t8p"]`; then set `parts` back to the default list. Only `rconv.json` or `t8p.json`, the
  `R_CONV` or `T8_P` key of `summary.json` and the `_conv` / `_t8p` records are written. A later rerun of the full
  pipeline rewrites `summary.json` without these keys; rerun the two parts afterwards (a conclusion test fails while a
  result file exists without its key). Runtime, measured on synthetic
  data of the real size (79 clouds, 2,000 grid points) while the machine was busy: one column-(3) likelihood takes
  0.7–1.4 ms depending on the convention (L-F-W fastest; C, X and P slowest). Every formal chain was rerun with doubled
  steps, so each chain is taken as 48 × 18,000 evaluations: about 10–20 minutes per column-(3) chain, 2.7–5.4 hours for
  the sixteen; the reruns about 0.8 hours (columns (4)–(6) about 45 minutes, T5 and its known-answer check a few
  minutes); Part B about 0.7 hours. In all about 3.5–6 hours (R-CONV) plus 0.7 hours (T8-P) on one core. A quick look:
  `--set parts='["conv"]' conv_indices='[0, 9]' mcmc_steps=1500 mcmc_burn=500` (about 25 minutes with the reruns, labelled as a subset).
- Analyses `run.py` does not cover: a script `explore/<name>.py` with `def main(ctx)`, run with
  `python -m astrolab explore 011-m11-radcliffe-wave-oscillation --tag <topic> --script explore/<name>.py`.
  Existing: `explore/age_scatter.py` (wiki Part 3 exploration "Age and birth in the Wave": RMS of the z
  and v_z residuals about the clusters-only B = 1 fit, split at 10 and 20 Myr; needs `results/t3.json`);
  `explore/t8_jacobian.py` (referee check, section 6 point 1: posterior modes of ω₀ in the column-(7)
  setup with and without the −Σ w_k ln ω₀ term, under both priors; about 5 minutes; needs `results/t8.json`).
- Results files and keys (every file also stores `params`):
  - `results/t1_t2.json`: `t1` (`col4`, `col6`, `col3_for_reference`: per parameter `ours`, `k24`,
    `inside_k24_1sigma`, `sigma_scaled_difference`; `n_inside_of_6`; `label`; `inliers_vs_table_flag`),
    `t2` (`B` percentiles, `P_B_gt_0p95`, `P_B_lt_0p5`, `w0t`, `B_histogram`), `chains` (acceptance,
    autocorrelation times, `chain_short`), `plot` (model curves and cluster points for the web page).
  - `results/t3.json`: `standing_stat`, `travelling_stat` (`two_dlnL`, `d`, `p_raw`, `p_boot`, `m`,
    `se_m`, `factor`, `p_cal`, `p_cal_mcse`, `mocks_two_dlnL`), `standing`, `pure_travelling`,
    `reduced_rule_main`, `residual_resampling_variant`, `fits` (ML and MAP parameters of B = 1, B = 0.5,
    B free), `inlier_overlaps`, `clipped`.
  - `results/t4.json`: `R_obs`, `n_clusters`, `gauss` and `resid` (`p`, `p_mcse`, `power_B1`,
    `power_Bfree`, quantiles, `label`), `label`.
  - `results/t5.json`: `bhat`, `bhat_interval`, `k_ratio`, `k_ratio_interval`, `Delta` and `rho` with
    intervals, `wavelengths_label`, `bhat_label`, `sensitivity_omega0`, `known_answer` (per injection
    `median_mock_bhat`, `median_mock_interval`, `pass`, coverage, bias), counts of kept and dropped clusters.
  - `results/t6.json`: `label`, `changes`, `main_labels_full_rule`, `main_labels_reduced_rule`,
    `variants` (per variant: T3 numbers and labels, `t4`, `t5`, `labels`, `changed`).
  - `results/t7.json`: `a_col6_B1`, `b_vz_zero`, `c_B0p5` (`m2lnL`, `sigma_int`), `theta2_a`, `theta2_c`,
    `label`.
  - `results/t8.json`: `ln_omega0_k24_prior`, `ln_omega0_broad_prior`, `halfwidth_broad`,
    `median_shift_in_sigma_broad`, `label`, and for `k24_priors`, `broad_priors`, `variant_divisor_fixed`:
    `omega0_kms_kpc`, `rho0_msun_pc3`, `sun_period_myr`.
  - `results/rconv.json` (README 4.10): `conventions` (per convention: `index`, `name`, `count`, `inside`,
    `sigma_scaled_differences`, `width_ratio`, `halfwidth_ratios`, `parameters`, `sigma_P_at_median_pc`, `chain`),
    `choice` (`case`, `chosen`, `chosen_name`, `label`, `reason`), `label`, `complete_set`, `k24_column3`, `reruns`
    (`t1`, `col5`, `t5` with `known_answer` incl. `injected_vector`, `labels`, `chains`, `chain_short`).
  - `results/t8p.json` (README 4.10): `ln_omega0_k24_prior`, `ln_omega0_broad_prior`, `halfwidth_broad`,
    `median_shift_in_sigma_broad`, `broad_median_omega0_kms_kpc`, `label`, `at_bound`, `width_shift_rule_label`,
    `bound_thresholds_kms_kpc`, `distance_to_upper_bound`, `k24_priors` and `broad_priors` (`omega0_kms_kpc`,
    `rho0_msun_pc3`, `sun_period_myr`, `mu0_kpc`, `r0_pc`), `chains`.
  - `results/summary.json`: every label, `overall` (`reading`, `support`, `do_not_support`,
    `undetermined_or_not_evaluable`, `qualifier`), `load_check`, `timing`, `chain_short`; after the standalone runs also
    `R_CONV` (`label`, `case`, `chosen`, `reason`, `counts`, `width_ratios`, `reruns`, `chain_short`) and `T8_P`
    (`label`, `at_bound`, `halfwidth_broad`, `median_shift_in_sigma_broad`, `omega0_k24`, `omega0_broad`).
- Example questions:
  - "Is T5's verdict sensitive to the wavelength band?" → `--set t5_band='[0.7, 1.4]' parts='["t5"]'` (about 45 minutes).
  - "What if the Wave's scatter were 35 pc?" → `--set sigma_pc=35` (new fits; hours).
  - "Do older clusters scatter more?" → `--script explore/age_scatter.py`.
  - "How much does the Sun's period depend on its vertical velocity?" → `--set sun_vz_kms=7.25 parts='["t8"]'` (about 70 minutes; only the divisor-74 variant is meaningful, section 6 point 1).
  - "Does T8 need the ln ω₀ normalisation?" → `--script explore/t8_jacobian.py`.
  - "Which baseline, σ and weight convention reproduces K24's column (3)?" → the formal R-CONV run above (`parts=["conv"]`).
  - "Is ω₀ set by the data once the divisor is fixed?" → the formal T8-P run (`parts=["t8p"]`, about 0.7 hours).
- Findings that change what we know go into `log.md` (and, for a paper study, the wiki article)
  on a branch.
