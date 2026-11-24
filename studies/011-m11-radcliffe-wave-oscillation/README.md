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
| *Added 2026-11-24 (section 4.11, T-061, R-DIAG only):* Zucker et al. 2020 Table A.1 `Handbook_Distances_Zucker2020.dat` | Harvard Dataverse doi:10.7910/DVN/07L7YZ, file id 4361456, via `ctx.http` | all rows | 326 rows, 55,870 bytes |
| *Added 2026-11-24 (R-DIAG):* Alves et al. 2020 bridging sightlines `Bridging_Sightlines_Alves_2020.dat` | doi:10.7910/DVN/K16GQX, file id 4361453, via `ctx.http` | all rows | 54 rows, 9,894 bytes |
| *Added 2026-11-24 (R-DIAG):* K24 best-fit model curve `Radcliffe_Wave_best_fit_model_Konietzka2024.tab` | doi:10.7910/DVN/F98QHY, file id 8954305, via `ctx.http` | all rows | 1,500 rows, 47,253 bytes |

The two tables come to about 16 KB, far below the 200 MB study budget. Nothing else is fetched, except the three files
added on 2026-11-24 for R-DIAG (section 4.11; 113,017 bytes, about 129 KB with the two tables).

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

### 4.11 Addendum 2026-11-24: R-DIAG, where the column-(3) difference comes from (T-061), pre-registered before any of these fits

*Why.* R-CONV (section 5.1) found that none of 16 conventions reproduces column (3): all give the same two parameters
inside and four outside, so the cause is common to them. Its referee (section 6, points 1, 2 and 9) proposed a per-cloud
diagnostic at K24's column-(3) medians against our best point, and refits with the origin of s shifted and with the Sun
20.8 pc above the midplane, and asked whether our 79 clouds are K24's sample. **Everything in this addendum is post
hoc**: it is added after the formal, R-CONV and T8-P results were seen.

*K24's text and the public data, rechecked (2026-11-24; K24 read in the arXiv PDF, Methods pp. 10–18 and Extended
Data Figs. 1–3).*
- "Modeling the Spatial Molecular Cloud Distribution": the cloud component is "described by the corresponding 3D cloud
  positions from the Major Cloud Catalog and the Tenuous Connections Catalog", keeping "only those molecular clouds for
  which we can obtain a radial velocity measurement". "Line-of-sight Gas Velocities": a ¹²CO spectrum is computed "for
  each set of spatial cloud coordinates"; "nine percent of the clouds" have no usable ¹²CO and are excluded; for Extended
  Data Fig. 3a the measurements of a single cloud are combined "into a single data point". That figure's caption says
  the Perseus and Taurus clouds, which K24 identified as outliers, are not shown. K24 print no count of the clouds in the
  column-(3) fit; in their Extended Data Fig. 1 the clouds appear as many more points than 79.
- The Major Cloud Catalog is Zucker et al. 2020 Table A.1 (Harvard Dataverse doi:10.7910/DVN/07L7YZ, file
  `Handbook_Distances_Zucker2020.dat`, id 4361456, 55,870 bytes, CC0): 326 sightlines in 94 named clouds, one row per
  sightline with name, l, b, distance percentiles and x, y, z. The Tenuous Connections Catalog is Alves et al. 2020's
  bridging sightlines (doi:10.7910/DVN/K16GQX, `Bridging_Sightlines_Alves_2020.dat`, id 4361453, 9,894 bytes, CC0): 54
  sightlines with the same columns.
- Our 79-row ¹²CO table has columns name, x, y, z, xspread, yspread, zspread, l, b, d, vr, vr16, vr84. Its rows are the
  54 bridging sightlines (they agree with the bridging table within 1 pc) and 25 rows named after 23 major clouds;
  `MonR2` and `Mon_R2` are two rows at different positions, as are `NorthAmerica` and `NorthAmericaNebula`; Perseus and
  Taurus are absent. A named row is often **not** the mean of all the Zucker sightlines of that name (gate-1 review of
  this addendum, below): it looks like the mean of a subset. So our column-(3) fit used one point per named row, where
  K24's fit most likely used one point per sightline of that subset. This is our reading; K24 do not say it in these
  words, and no public list of the subsets was found.
- K24's best-fit model curve is public (doi:10.7910/DVN/F98QHY, `Radcliffe_Wave_best_fit_model_Konietzka2024.tab`, id
  8954305, 47,253 bytes, CC0): 1,500 points with x, y, z (pc) and v_z (km/s). The Dataverse description says the model
  was applied to the cloud and cluster observations, so the curve is most likely the column-(6) fit (column (7) is
  possible); whether it is the median, the maximum or another point of the posterior is not stated.
- Bennett & Bovy 2019 (MNRAS 482, 1417; arXiv:1809.03507) measure the Sun's height above the local midplane as
  z☉ = 20.8 ± 0.3 pc. K24 (Methods, cluster fit) refit with z☉ free in U(−10, 25) pc and found shifts below a third of
  the 1σ uncertainties of A, φ and δ, so we expect little from this variant.

*Seen before this addendum.* All of sections 5–7 and log.md. On 2026-11-24:
- An exploration (`explore/t061_inputs.py`, output not committed) fetched the three new files and printed their row and
  column counts, the header and first two rows of each, and the names. The first row of K24's published curve, (x, y) =
  (−994.6, −930.4) pc, lies about 194 pc in x–y from K24's column-(6) anchor 0 (simple arithmetic, not done at the
  time), so where K24's curve starts was visible. The per-cloud sightline counts (115 mapped, Perseus 18, Taurus 10)
  came from a second listing of the Zucker names with their counts (an uncommitted one-off script).
- The gate-1 review of this addendum compared each named ¹²CO row with its mapped sightlines (positions only, no model):
  Cepheus's row (spread 19/12/14 pc) lies far from the mean of its 28 sightlines (only 10 are within 30 pc); Polaris's
  mean is 54 pc off in z; `MonR2` (spread 0) is one sightline of `Mon_R2`'s 6; the two North America rows are different
  subsets of its 10 sightlines; Cygnus X, Orion, IC5146 and the single-sightline rows match. In round 1, with a
  stricter check than the rule below (each sightline counted once per row, and the SD compared as well), it found 103
  sightlines at k = 3 (89 at k = 2), with MonR2, NorthAmerica and Orion_Lam mismatched. In round 2 it applied the final
  rule below to the tables (positions only): 95 distinct sightlines kept, every row passing the gate except
  `NorthAmericaNebula`, whose candidates all go to `NorthAmerica` (absorbed); so S has 95 + 54 = 149 points. It also
  computed, at K24's column-(3) medians and with the model only, the grid's s range (−291 to 4,042 pc) and
  the Λ pole p/γ = 3,204 pc.
- No sightline was compared with a model curve, the published curve was not compared with our model, and nothing was
  fitted.

*Part A, per-object diagnostic on the 79 (descriptive).* The formal column-(3) setup (L-F-W, σ = 47 pc, the formal fixed
weights). Three parameter vectors: K24's column-(3) medians v_K (the free parameters from Extended Data Table 2, B = 1,
ω₀t = 0); our formal L-F-W posterior medians v_P (`rconv.json`, convention 0); and our maximum a posteriori point v_M
(section 4.2's optimiser, Nelder–Mead then L-BFGS-B, with the log posterior as objective from every start; the best of
21 starts: v_K, v_P and 19 prior draws from `rng_for(seed, "ml_rdiag_map")`). At each: ln L, ln prior, ln posterior and σ_P (section 4.10); for each object its
name, s, weight, d² and term tᵢ = wᵢ dᵢ²/(2σ²). Reported for both comparisons Δᵢ = tᵢ(v_K) − tᵢ(v_M) and Δᵢ = tᵢ(v_K) −
tᵢ(v_P): the ten objects with the largest Δᵢ, the share of Σ max(Δᵢ, 0) they carry, and the sums over the 25 named rows
and the 54 bridges. No label (the share has no calibrated reference).

*Part B, the input sample (R-SAMP).* Positions from each table's x, y, z columns (heliocentric Galactic Cartesian, as in
our ¹²CO table). The name map, fixed now: CB29, CMa_OB1, Cam, Cepheus, CygnusX, IC5146, L1228, L1228D, L1251, L1265,
L1333, L1617, L1622, L977, L988, Lacerta, Orion, Orion_Lam, Polaris, S106 to the same Zucker name; `MonR2` and `Mon_R2`
to `Mon_R2`; `NorthAmerica` and `NorthAmericaNebula` to `North_America`; `NorthernCoalsack` to `Northern_Coalsack`.
- **S, the reconstructed sample (primary).** For a named row r with position p_r and spreads σ_r,a (a = x, y, z), the
  tolerance is t_r,a = 3 max(σ_r,a, 5 pc). The candidates of r are the sightlines of its mapped name with |x_a − p_r,a| ≤
  t_r,a on every axis. A sightline that is a candidate of two rows goes to the row with the smaller maxₐ |x_a −
  p_r,a|/t_r,a, compared as computed in double precision with no tolerance (exact ties to the row listed first in the
¹²CO table). **Gate per row:** a row that had candidates but keeps
  none because all of them went to another row is **absorbed** by that row: it is dropped and listed ("absorbed by
  <row>"). Every other row passes if it keeps at least one sightline and the mean of its sightlines lies within
  max(σ_r,a, 5 pc) of p_r on every axis; a row that fails (no candidates at all, or the mean outside) enters S as its own
  single ¹²CO point (a "fallback row", listed). S is the passing rows' sightlines, the fallback rows' points and the 54
  bridging sightlines (from the bridging table). On the real tables the rule gives 95 sightlines, no fallback row and
  one absorbed row (`NorthAmericaNebula` by `NorthAmerica`), so S has 149 points (gate-1 round 2, disclosed above); the
  run recomputes and reports it.
- **S_all** (reported): every distinct Zucker sightline of the mapped names (115; the Zucker table has no bridging
  sightlines, so nothing is duplicated) plus the 54 bridging sightlines, 169 points.
- **S+PT** (reported): S plus all Perseus (18) and Taurus (10) sightlines (177 points), which K24 may have kept in the
  spatial fit.
- **Consistency table** (reported): for each named row, the number of its candidates and kept sightlines, the mean of the
  kept sightlines minus p_r and, per axis, their population standard deviation (ddof = 0) divided by σ_r,a (not defined
  when σ_r,a = 0), pass or fallback; and, under S, the summed kernel
  weight of each row's points next to that row's weight in the 79-row fit.

*Fits.* For S, S_all and S+PT the column-(3) MCMC exactly as section 4.2 (L-F-W, σ = 47 pc fixed, B = 1, ω₀t = 0), with
kernel weights from each point's s on the formal curve at K24's column-(6) medians (bandwidth 100 pc, normalised to the
sample size, as section 4.1). Chain seeds by the `mcmc` rule of `run.py` with the names `rdiag_S`, `rdiag_Sall`,
`rdiag_SPT` (the integer drawn from `rng_for(seed, "mcmc_<name>")`). Walkers are placed as in the formal run
(`fit011.init_walkers`): K24's column-(3) medians plus 0.05 × each parameter's scale (its prior σ; 100 pc for c in Part D)
× a standard normal draw from the chain's seed, redrawn until the log posterior is finite (at most 200 × 48 draws, else
the run stops); the same for every chain of this addendum. For each: T1's column-(3) count (how many of A, p, δ, s₀, γ, φ have their posterior median inside K24's 16–84% interval), the
σ-scaled differences of the 12 shape and anchor parameters, D₆ = the sum of the absolute σ-scaled differences of A, p,
δ, s₀, γ and φ (all six, whether inside or not) and M₆ = the largest of these six, the width ratio (section 4.10, amendment 5), σ_P at the posterior median (reported, not
used), and the label by R-CONV's thresholds: **"column (3) reproduced with sample <S | S_all | S+PT>"** if the count is
≥ 5 and the width ratio lies in [2/3, 3/2]; **"column (3) partly reproduced with sample <…>"** if the count is 3–4, or
≥ 5 with the width ratio outside that range; **"column (3) not reproduced with sample <…>"** if the count is ≤ 2. Each
label ends with "post hoc". The formal L-F-W fit (`rconv.json`, convention 0) has count 2, D₆ = 9.781 and M₆ = 3.692
(φ).

*Part C, K24's published curve (R-CURVE).* (i) Our model curve at K24's column-(6) medians (the formal L baseline, grid
and extent, B = 1, ω₀t = 0, divisor 74): for each of the 1,500 published points, the nearest valid grid point of our
curve in x–y (the projection depends only on the anchors and the baseline convention) and in 3-D. A point whose nearest
point is the first or last valid grid point (as in section 4.9, item 8) is excluded, separately for the x–y and the 3-D
nearest point; both counts are reported. Reported for the rest: median, 95th percentile and maximum of the x–y and
3-D distances, the median absolute v_z difference at the 3-D nearest point, and our s of the published curve's first and
last points (percentiles by `numpy.percentile` with its default linear interpolation). Label (from the x–y
distances): **"matches K24's published curve"** if the median is ≤ 5 pc and the 95th
percentile ≤ 15 pc; **"approximately matches"** if the median is ≤ 20 pc; otherwise **"differs from K24's published
curve"**; if more than 10% of the 1,500 points are excluded in x–y, the label is followed by "(more than 10% of the
points lie beyond our curve's ends)". The 3-D numbers are reported next to it (z depends on which posterior point was
published). (ii) A
least-squares fit of our curve to the published points: the 12 shape and anchor parameters plus the origin shift c
(below), B = 1 and ω₀t = 0, minimising the sum over the published points (ends excluded as in (i)) of the squared 3-D
distance to our curve, each kept point with equal weight (the 3-D exclusion set of (i), fixed during the fit). At every evaluation each kept point is
matched to its nearest valid grid point of that evaluation's curve (2,000 points, validity p − γs′ > 0); a vector with no
usable curve scores 10¹². One start, K24's column-(6) medians with c = 0, then `fit011.optimise`'s Nelder–Mead (initial
steps 0.5 × each parameter's scale, 100 pc for c) and L-BFGS-B; the anchors, A, p, s₀ and φ are unbounded, δ and γ are
fitted as ln δ and ln γ (unbounded), and c is bounded to [−400, 400] pc. Reported: the fitted parameters, c, their differences from K24's column-(6) medians in K24's σ,
and the RMS distance; read in section 5, without a label.

*Part D, conventions R-CONV did not vary (R-ORIG).* On the 79 ¹²CO rows, the formal column-(3) setup with one change
each:
- **(c)** the origin of s as a free parameter c: s′ = s − c replaces s wherever s enters the model (Λ, ζ, and the
  validity mask p − γs′ > 0), with c ~ U(−400, 400) pc and the other priors unchanged (s₀ is then measured from the
  shifted origin, as K24's s₀ is from theirs). Because ζ depends only on s₀ + c, c enters the fit only through Λ, where it is constrained jointly with p, γ and
  the anchors [post hoc 2026-11-24: wrong, see section 6, R-DIAG referee point 1]; the posterior correlations of c with s₀, p and γ are reported. The
  grid, the curve's extent and the fixed weights (computed as in the formal run, with c = 0) are unchanged; c < −291 pc
  puts the origin before the grid's start, which is allowed. Walkers start around c = 0 with a ball scale of 100 pc.
  Because the data fix s₀ + c near the envelope's peak (about 500 pc in our fit), the N(680, 200) prior on s₀ induces a
  prior on c of roughly N(−180, 200) pc. So a reference chain **(c-ref)** is run with the same setup but s₀ flat in
  U(−1,000, 3,000) pc, and c is read as **"data-driven"** if c-ref's 16–84% half-width of c is at most 100 pc (a chosen
  threshold: about half the width of that induced prior, and well below the 272 pc of U(−400, 400) itself), otherwise as **"prior-dominated"**; both chains' c posteriors are reported. c-ref's count and labels are not
  reported or used (it is not a third variant); its walkers start as in (c), around K24's column-(3) medians with c = 0.
- **(z☉)** every cloud's z increased by 20.8 pc (the model has no free vertical offset, so A and φ absorb it).
MCMC as section 4.2 (13 free parameters for (c) and c-ref), seeds by the `mcmc` rule with the names `rdiag_c`,
`rdiag_cref` and `rdiag_zsun`;
count, differences, D₆, M₆, width ratio and labels as in Part B ("… with the origin free / with z☉ = 20.8 pc, post
hoc"); for (c) also the posterior of c.

*Reading (post hoc, fixed now; uses S, not S_all or S+PT).*
- **"column (3) is reproduced with the reconstructed sightline sample: the difference is consistent with the input
  sample"** if S's label is "reproduced";
- otherwise **"the reconstructed sightline sample accounts for part of the column-(3) difference"** if S's label is
  "partly reproduced"
  and S's D₆ ≤ 8.781 and its M₆ ≤ 3.192 (the formal fit's 9.781 and 3.692 less margins of 1 and 0.5, for the seed and
  chain-length noise: the 16 R-CONV conventions moved φ by about ±0.6σ);
- otherwise the same two steps for Part D, taking whichever of (c) and (z☉) reaches the higher step (both named on a
  tie), where (c) counts only if c is "data-driven": **"the column-(3) difference comes from the origin of s or the Sun's
  height"** or **"the origin of s or the Sun's height accounts for part of the column-(3) difference"** (naming the
  variant);
- otherwise **"the column-(3) difference remains unexplained (input sample, origin and the Sun's height tested)"**.
S is our reconstruction (K24's subsets are not public), so the first two readings are evidence that the sample matters,
not proof that K24 used S. S_all, S+PT, Part A and Part C are reported next to it and do not enter it. Nothing else is rerun: the formal labels, the
overall reading, T6, R-CONV and T8-P stay as recorded; if S reproduces column (3), rerunning columns (4) and (6) and T5
with sightlines is a separate, later decision.

*Expected outcome (stated now).* Under S, Orion (Orion 17 and Orion_Lam up to 7 sightlines), Cygnus X (13) and the kept
part of Cepheus get more weight than one row each, unless the kernel weights compensate (they largely do when a row's
sightlines lie within about 100 pc in s; the consistency table shows it); we expect S to move the anchors and φ, with an
even chance of at least a partial reproduction. Part C most likely "matches" or "approximately matches". Part D: z☉
changes little (K24's own test); under (c) the s₀ prior pulls c towards about −180 pc, close to the −194 pc offset of
K24's published first point, so a c near −200 pc from the main chain alone would mean little (hence c-ref; we expect
"prior-dominated"); s₀ shifts with c, so the count is unlikely to reach 3.

*Data and cost.* Three new files of 55,870, 9,894 and 47,253 bytes (113,017 in all) via `ctx.http`, far below the
budget; added to section 3. Part A a few minutes; Part B three column-(3) chains on 149, 169 and 177 points (about 2–2.3
times the 79-row cost per evaluation, so about 20–45 minutes each with the doubling); Part C a few minutes; Part D three
chains of 10–25 minutes. In all about 2–3.5 hours on one core, with the pause and checkpointed
resume of section 4.9, item 13. Run alone, after the other studies' runs.

*Code checks before the run (synthetic data only, except the counts).* The name map and the membership rule on synthetic
rows and sightlines (a sightline inside two rows, an absorbed row, a row that falls back, ties); on the real tables S
has 149 points, S_all 169 and S+PT 177; with c = 0 and no z change the formal likelihood is reproduced to the bit; the shifted ζ with s₀′ = s₀ −
c reproduces the formal ζ to round-off; the per-object terms sum to −ln L minus the constant; the curve-distance code
returns 0 for a curve against itself and the right distance for a curve displaced by a known vector, and flags grid ends;
the least-squares fit recovers a synthetic vector (with c) from its own curve to under 1 pc RMS.

*Switch and code.* A new part `"diag"` in `PARAMS["parts"]`, standalone like `"conv"` (section 4.10, amendment 9): it
refuses to start unless `summary.json` exists and re-serialises byte-identically, writes `results/rdiag.json` (below 1 MB)
with the load check and `params`, and puts `R_DIAG` into `summary.json` before `overall`; records `_diag` and
`_diagpaused`; checkpoints in `s011_checkpoints/diag/<key>`. `wave011.py` gains the origin shift as a setup option
(default 0, so all other results reproduce). Tests, conclusion checks, a web section and section 8 knobs. None of this
exists yet.

*Amendments and disclosure while writing the code (2026-11-24, before the formal R-DIAG run).* No rule, threshold or
label above changes.
1. **Seen before the formal run.** While checking the code on the real inputs, a smoke check printed Part C (i) (x–y
   median 0.80 pc, 95th percentile 1.30 pc, label "matches"; 3-D median 66 pc) and ln L at v_K and v_P (−913.88 and
   −805.51). A data-path exploration with chains far too short to read (32 walkers, 200 steps; output and checkpoints
   deleted) printed preliminary labels: S "reproduced" (count 5), S_all and S+PT "partly reproduced", (c) "reproduced"
   with c ≈ −196 pc and a c-ref half-width of 92 pc, (z☉) "not reproduced". The formal run replaces all of these; they
   are disclosed because they were seen.
2. **(z☉) weights.** The fixed weights of the (z☉) fit are recomputed by the formal rule from the shifted clouds, as
   amendment 9 of section 4.9 does for variants (largest change 0.106 against the 79-row weights; recorded as
   `weights_max_abs_change`). For (c) and c-ref they are the formal weights, as stated above. The addendum did not
   say which weights (z☉) uses; this recomputation is a choice made when writing the code.
3. **Membership edge cases.** A row whose candidates went to several other rows is listed as absorbed by all of them; a
   fallback row's own sightlines stay out of S (they are not handed to another row). A row absorbed by a row that then
   falls back leaves no point in S at all; it is recorded under the fallback row (`absorbed_rows` in the consistency
   table, `absorbed_into_fallback` in `rdiag.json`). None of these cases occurs on the real tables.
4. **Part A's ln prior** is the same unnormalised Gaussian log prior as the log posterior's; Part C (ii)'s bound on c is
   the prior range of (c), [−400, 400] pc.
5. **Cost.** One column-(3) likelihood takes about 0.73 ms on the 79 rows and 1.05–1.12 ms on S (about 1.5 times, not
   2–2.3); the run should take about 1.5–2 hours.


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

### 5.1 R-CONV and T8-P (post hoc, addendum 4.10, T-056; runs 2026-11-22)

Two standalone runs with the formal run's settings (`parts` ["conv"], then ["t8p"], set back to the default
afterwards), single-threaded, cache only: R-CONV 9,167 s (2.5 h), T8-P 1,910 s (32 min). Load check passed (weighted
mean v_z −2.18 km/s). Numbers: `results/rconv.json`, `results/t8p.json`, `summary.json` keys `R_CONV` and `T8_P`. Both
are post hoc; the formal labels, the overall reading and T6 stay as recorded.

**R-CONV: "column (3) not reproduced under any candidate convention (best among these 16 candidate conventions, post
hoc)"** (case (i) of the choice rule: every count ≤ 2). So Part A stops here and nothing is rerun (no column-(4)/(6) refit, no T5
known-answer check on our own curve). In all 16 conventions the same two parameters are inside K24's 16–84% interval
(s₀ and γ) and the same four outside, with nearly the same σ-scaled differences:

| Parameter | Range of (ours − K24)/σ over the 16 conventions | Formal run (L-F-W) |
|---|---|---|
| A | −1.42 to −1.14 | −1.39 |
| p | −1.71 to −1.41 | −1.44 |
| δ | −2.14 to −1.87 | −2.09 |
| s₀ | −0.43 to +0.36 (inside) | +0.17 |
| γ | −0.99 to −0.52 (inside) | −0.99 |
| φ | +2.91 to +4.06 | +3.69 |
| x₀ | −1.70 to −1.10 | −1.47 |
| y₀ | −2.30 to −1.93 | −2.07 |

- **Width ratios** 1.07–1.20 (our 16–84% half-widths 7–20% wider than K24's), inside [2/3, 3/2] in every convention;
  P (σ from the spread of d²) gives the slightly narrower posteriors (1.07–1.12) than F (1.17–1.20). Under P, σ at
  our own posterior median is 42–44 pc, close to K24's 47 (not the 60 pc found at K24's medians on our curve, section
  4.10).
- **Chains:** in every convention the post-burn chain (8,000 steps after the doubling) is shorter than 50τ (τ_max
  176–217), so every column-(3) fit carries the pre-registered "chain short" flag.
- The baseline (L, C, Y, X), σ (F, P) and weights (W, R) move the anchors by at most about 0.6σ (x₀) and the shape
  parameters by at most about 1.2σ (φ): none of these conventions accounts for the column-(3) difference.

**T8-P: "prior-driven" (post hoc)**, with the divisor fixed at 74 km s⁻¹ kpc⁻¹ and the formal convention. The broad-prior
posterior of ln ω₀ has a half-width of 0.172 (limit 0.085) and its median is 1.15 broad-posterior half-widths from the K24-prior
median (limit 0.5); the broad-prior median, 58.6 km s⁻¹ kpc⁻¹, is not at a bound (16th percentile 49, far from the
31.5 threshold; no draw above 142.5). Both chains were flagged short after the doubling: τ_max 389 (K24) and 499
(broad), so the 8,000 post-burn steps are only 16–21τ; the widths and medians carry that Monte Carlo uncertainty.

| Prior | ω₀ (km s⁻¹ kpc⁻¹) | ρ₀ (M☉ pc⁻³) | Sun's vertical period (Myr) |
|---|---|---|---|
| K24's (ln(ω₀ km⁻¹ s pc) ~ N(−2.4, 0.17), centred on 91) | 71 (+9/−8) | 0.094 (+0.026/−0.020) | 88 (+12/−10) |
| broad | 59 (+12/−10) | 0.064 (+0.028/−0.019) | 107 (+22/−17) |

**Reading (post hoc).** (1) The column-(3) difference is not a matter of the baseline, the σ convention or the weights:
all sixteen readings of K24's Methods give the same two inside and four outside, with δ about 2σ shorter, φ 3–4σ
larger and the first anchor about 2σ lower in y; the addendum's expectation that Y, X or P would move the anchors by
about 100 pc was wrong (at most about 35 pc). The cause is common to all sixteen: the data, the likelihood, or a
convention none of them varies (the origin of s and the form of Λ(s), section 6). K24 fit "only those molecular clouds
for which we can obtain a radial velocity measurement", which is our 79-cloud sample's definition; whether the clouds
and their positions are the same is not checked here (T-061). (2) With ω₀ entering only through the model, the data
constrain ln ω₀ to about ±0.17 (about ±19%), as tightly as K24's prior and far more than the broad prior (about ±0.49),
and under the broad priors prefer 59 km s⁻¹ kpc⁻¹; K24's prior (centred on 91) pulls the median up to 71. So prior and data are
comparable, and K24's 67.7 sits between them. The broad width is inflated by the ω₀–r₀–μ₀ freedom (r₀ stays at about
its prior width), and with B = 1 and ω₀t = 0 fixed ω₀ effectively measures the clusters' A_v/A_z ratio, which a
partly standing component or the tanh outlier truncation would bias; it is not a clean measure of the midplane
density. The withdrawn T8 stays withdrawn.

### 5.2 R-DIAG (post hoc, addendum 4.11, T-061; run 2026-11-24)

A standalone run (`parts` ["diag"], commit ed915e7; set back to the default with the results, commit 028fc1f), threads
not limited, cache only: 6,617 s (1.8 h). Load check passed (weighted mean v_z −2.18 km/s). Samples as registered: S 149
points (95 sightlines, no fallback row, NorthAmericaNebula absorbed by NorthAmerica), S_all 169, S+PT 177. Numbers:
`results/rdiag.json`, `summary.json` key `R_DIAG`. All post hoc; the formal labels, the overall reading, T6 and R-CONV
stay as recorded.

**Reading (by the rule of section 4.11): "the reconstructed sightline sample accounts for part of the column-(3)
difference"** (from S: D₆ 7.659 ≤ 8.781 and M₆ 2.674 ≤ 3.192). Part of this gain may come from the larger total kernel
weight of S rather than from the sample itself (section 6, point 3; a control is registered as T-065).

| Fit | Points | Count (inside) | D₆ | M₆ | Width ratio | Label |
|---|---|---|---|---|---|---|
| formal L-F-W (R-CONV, for reference) | 79 | 2 (s₀, γ) | 9.781 | 3.692 (φ) | 1.18 | not reproduced |
| S | 149 | 3 (δ, s₀, γ) | 7.659 | 2.674 (φ) | 1.07 | partly reproduced |
| S_all (reported only) | 169 | 3 (A, s₀, γ) | 7.159 | 3.256 (p) | 1.01 | partly reproduced |
| S+PT | 177 | 4 (A, δ, s₀, γ) | 4.738 | 1.724 (φ) | 1.05 | partly reproduced |
| (c) origin free | 79 | 3 (A, p, s₀) | 6.516 | 1.866 (δ) | 1.21 | partly reproduced by the rule; **withdrawn as uninformative** (section 6, point 1) |
| (z☉) +20.8 pc | 79 | 1 (p) | 17.598 | 8.503 (φ) | 0.98 | not reproduced |

- **Part B.** With S, δ moves from −2.1σ to −0.4σ; among S and S+PT, A comes inside only with S+PT (−0.5σ; −1.4σ in S); φ stays
  outside (+2.7σ in S, +1.7σ in S+PT, against +3.7σ formally) and the first anchor stays about −1.7σ / −2.4σ off in x₀ /
  y₀. The anchors slide along the curve with the origin (section 6, point 2), so their σ-differences are not read as
  geometry differences. S_all has σ_P = 130 pc at its median (a few far sightlines dominate the uncapped d²
  dispersion); it is reported only, as registered.
- **Part A.** At K24's column-(3) medians our 79-row ln L is 108.9 lower than at our MAP point (ln posterior −807.57
  from 21 starts). The 54 bridging sightlines carry 77.4 of this and the named rows 31.5; the largest single terms are
  four bridging sightlines near l ≈ 222°, b ≈ −6° (4.2–4.7 each), IC5146 (4.5) and S106 (3.7). The bridging rows are
  the same in S, so S does not touch most of the per-object difference.
- **Part C.** Our curve at K24's column-(6) medians **matches K24's published curve**: x–y distance median 0.80 pc, 95th
  percentile 1.30 pc (maximum 2.26 pc), no point excluded at our curve's ends; in 3-D the median is 66 pc (the
  published z depends on which posterior point K24 drew). The least-squares fit of our curve to the published points
  reaches an RMS of 0.68 pc (from 70.2 pc). Because the origin c is degenerate with p, γ, φ and s₀ (section 6, point 1),
  only this RMS is read, not the fitted parameters or c.
- **Part D.** (c): c = −245 (+140/−101) pc; the reference chain c-ref (s₀ flat) gives −216 (+152/−121) pc, half-width
  137 pc > 100 pc, so c is **"prior-dominated"**. Part D does not enter the reading (S already reached the second reading; c was also
  prior-dominated). Post hoc (referee): c is exactly
  degenerate with p, γ, φ and s₀ (the curve, ζ and the validity mask are unchanged under p′ = (p + γc)²/p, γ′ = γ(p +
  γc)/p, φ′ = φ − 2πc/(p + γc), s₀′ = s₀ + c), so the likelihood is flat in c and c is set by the priors alone: c-ref
  could not have been "data-driven", and section 4.11's statement that c "is constrained jointly with p, γ and the
  anchors" was wrong. The (c) label is computed by the rule but withdrawn as uninformative. By the referee's
  computation (not saved), no single c brings p, γ, φ and s₀ inside together, so the origin of s does not account for
  the difference. (z☉): with z shifted by +20.8 pc and the weights recomputed (largest change 0.106) the fit moves
  further away (φ +8.5σ); the model has no free z offset, so a large change is expected and says little.
- **Chains.** Every chain was rerun by the rule at twice the length (6,000 → 12,000 steps, burn-in 2,000 → 4,000) and every one still carries the "chain
  short" flag (τ_max 180–244, 8,000 post-burn steps, 33–44τ). With about 1,500 independent samples per chain the
  medians' Monte Carlo error is about 0.03 posterior σ, far below the margins of S (1.12 in D₆, 0.52 in M₆).
- **Seen before the run.** The short-chain exploration disclosed in section 4.11 (amendment 1) had printed S
  "reproduced" (count 5) and (c) "reproduced" with a c-ref half-width of 92 pc; the formal run gives S count 3 and a
  c-ref half-width of 137 pc. The formal numbers replace the exploration's.

**Reading (post hoc).** With K24's per-sightline cloud positions (S), column (3) moves from 2 to 3 of 6 parameters
inside K24's ranges (4 with the Perseus and Taurus points), and D₆ from 9.8 to 7.7 (4.7), mostly through the envelope
width δ; the phase φ and the first anchor stay off. So the input sample is part of the column-(3) difference, but not
all of it, and part of the gain may be the larger total weight of 149 points against the priors (T-065). The origin of
s cannot explain the rest (it is exactly degenerate), and a fixed z☉ shift makes it worse. Most of the per-object
difference at K24's medians sits in the 54 bridging sightlines, which S does not change.

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

### Referee of R-CONV and T8-P (2026-11-22)

The independent referee was a subagent. It saw README sections 1–4 (with 4.10 and its amendments), `wave011.py`,
`stats011.py`, the conv and t8p parts of `run.py`, and the results files, not sections 5–7; it did not evaluate the
likelihood on the data. It found no bug in the four baselines, P, R, the count, the width ratio, the choice rule or the
T8-P likelihood, and found both labels applied as written. Triage:

| # | Point | Verified | Action |
|---|---|---|---|
| 1 | The difference is common to all 16 conventions (they agree to about 0.3σ), so it comes from the data or the likelihood, not the baseline. At K24's medians σ_P on our curve is 59.7 pc against 42–44 pc at ours, which with σ = 47 pc costs of order 60 in ln L, far more than the priors gain: K24's column-(3) point is strongly disfavoured by our 79 clouds. The referee suggests the 79-cloud CO table may not be K24's column-(3) sample (about 9% of clouds were dropped in the CO analysis) | the agreement and the σ_P values: yes (`rconv.json`); the ln L estimate is the referee's, not computed by us. K24's Methods ("Modeling the Spatial Molecular Cloud Distribution", read 2026-11-22) say they "include in our analysis only those molecular clouds for which we can obtain a radial velocity measurement", i.e. the clouds with a CO velocity, which is what our 79 are; K24 do not print the count there | **Accepted** that the cause is common to all conventions (section 5.1 reading); **not accepted** as shown that the samples differ (K24's own selection is the clouds with velocities). A per-cloud diagnostic is registered (T-061) |
| 2 | The origin of s and the form of Λ(s) = s/(p − γs) were not varied: an origin shift is not absorbed by s₀ and moves φ, p and γ together, which is the observed pattern (φ +3–4σ, p −1.5σ, γ −0.9σ). The addendum argued from cloud coverage, not from the model | yes (all conventions put s = 0 at anchor 0; K24: "s = 0 pc at the beginning of the Wave (near CMa OB1)") | **Accepted** as a gap of R-CONV's set of conventions; part of T-061 |
| 3 | Held fixed everywhere: no z offset of the Sun (as K24), the ln(2πσ²) constant of eq. 11 (matters only under P), priors centred near K24's results (which attenuate our offsets) | yes | **Accepted** as limitations; listed in section 7 (with T-061) |
| 4 | The "chain short" flags do not matter for the labels: about 1,800 independent samples per chain, sixteen chains with different seeds agree to 0.1–0.3σ, all started at K24's medians and moved away; T8-P's margins are large | yes (τ_max 176–217 for R-CONV; 389 and 499 for T8-P) | Noted in section 5.1 |
| 5 | T8-P's "prior-driven" follows the rule, but the reading needs care: the data constrain ln ω₀ about as well as K24's prior (0.17 against 0.17), far better than the broad prior (about 0.49 for a prior uniform in ω₀); under K24's prior (centred on 91) the median moves from 59 to 71. The broad width is inflated by the ω₀–r₀–μ₀ freedom (r₀ essentially at its prior width). With B = 1 and ω₀t = 0 fixed, ω₀ measures the clusters' A_v/A_z ratio, which a partly standing component or the outlier truncation bias | yes (`t8p.json`; K24's prior ln(ω₀ km⁻¹ s pc) ~ N(−2.4, 0.17), section 4.1) | **Accepted**: section 5.1's reading reworded ("prior and data comparable; K24's value pulled up by its prior") with these caveats |
| 6 | No serious bug; minor: P is not a proper likelihood (σ depends on the residuals) | yes | Noted; harmless here (P ≈ F) |
| 7 | The addendum's expectation (Y, X or P would move the anchors by about 100 pc) was wrong | yes (at most about 0.6σ ≈ 35 pc in x₀) | Stated in section 5.1 |
| 8 | Literature: Alves et al. 2020 (arXiv:2001.08748), Zucker et al. 2020 (arXiv:2001.00591), Edenhofer et al. 2024 (arXiv:2308.01295), Zhu et al. 2024 (arXiv:2402.15346), Li & Chen 2022 (arXiv:2112.08390), McKee et al. 2015 (arXiv:1509.05334) | Alves et al. 2020 is cited in the wiki; the others are the referee's IDs, not verified | Noted; not used |
| 9 | Most important additional test: on the 79 clouds, ln L and the per-cloud d² at K24's column-(3) medians against our MAP (L-F-W); then refits with the origin of s shifted by ±200 pc and with z + 20.8 pc | – | Registered as T-061 |

### Referee of R-DIAG (2026-11-24)

The independent referee was a subagent. It saw README sections 1–4 (with 4.11 and its amendments), `diag011.py`,
`wave011.py`, `fit011.py`, the diag part of `run.py`, `test_rdiag.py` and `results/rdiag.json`, not sections 5–7 or
log.md. It ran `test_rdiag.py` (21 passed) and recomputed every label from `rdiag.json`: all match the rules of section
4.11, with no threshold moved. Triage:

| # | Point | Verified | Action |
|---|---|---|---|
| 1 | The origin c is exactly degenerate: Λ(s) is a Möbius function of s, and p′ = (p + γc)²/p, γ′ = γ(p + γc)/p, φ′ = φ − 2πc/(p + γc), s₀′ = s₀ + c give the same curve, ζ and validity mask for any c (numerically 1e−7 pc at c = −245). The likelihood is flat in c, its posterior comes from the priors on p, γ, φ, s₀, c-ref could never be "data-driven", and Part C (ii)'s parameters are one point of a flat valley | yes (analytic, from `wave011.wave_on_grid`: ζ depends on s − c − s₀, and p − γ(s − c) = (p′ − γ′s)·p/(p + γc)) | **Accepted, post hoc (2026-11-24):** the (c) label is computed by the rule but withdrawn as uninformative; section 4.11's "constrained jointly" is wrong; only the RMS of Part C (ii) is read. The reading is unchanged (Part D does not enter it: S already reached the second reading; c was also prior-dominated). By the referee's computation (not saved), no single c brings p, γ, φ and s₀ inside together |
| 2 | Anchor 0 is nearly degenerate with the origin too: our anchor 0 lies on K24's curve about 128 pc before theirs along it, so the x₀/y₀ offsets are mostly a slide along the curve | the referee's computation | **Accepted:** anchor σ-differences are not read as geometry differences (section 5.2) |
| 3 | Kernel weights are normalised to the number of points, so S carries a total weight of 149 against 79 at fixed σ; the likelihood weighs about 1.9 times more against tight priors, and the main gain (δ) may come from data weight rather than the sample | yes (section 4.11, Part B; README 4.1) | **Accepted limitation:** the reading is qualified in section 5.2; a weight control (the 79-row chain with every weight × 149/79) is registered as T-065 |
| 4 | Part A: the bridging sightlines carry 77.4 of the 108.9 between K24's medians and our MAP point, and they are the same in S | yes (`rdiag.json` `part_a`) | **Accepted;** stated in section 5.2 |
| 5 | S_all has σ_P = 130 pc at its median; far sightlines dominate, so its p (−3.3σ) is not interpretable | yes | Noted; S_all is reported only, as registered |
| 6 | (z☉) shifts the data by +20.8 pc with no free offset in the model, so a large change (φ +8.5σ) was expected | yes | Noted in section 5.2 |
| 7 | Every chain is flagged short (τ_max 180–244, 33–44τ), but about 1,500 independent samples give a Monte Carlo error of about 0.03σ, far below the margins (1.12 in D₆, 0.52 in M₆) | yes | Noted; the labels are unaffected |
| 8 | c-ref reaches towards the −400 pc bound (16th percentile −337), so its half-width (137 pc) is truncated by the bound | yes | Noted; "prior-dominated" holds, conservatively |
| 9 | Literature: Zucker et al. 2020 (arXiv:2001.00591), Alves et al. 2020 (arXiv:2001.08748), Edenhofer et al. 2024 (arXiv:2308.01295); none explains the φ/δ difference directly | – | Noted |
| 10 | Most important additional test: the weight control of point 3 | – | Registered as T-065 |

## 7. Open questions

- Which convention reproduces K24's clouds-only fit (column (3))? Candidates: the curve starting at
  u = 0 rather than −0.2, σ estimated from the spread of d² as K24 describe, kernel weights recomputed at
  each parameter vector. Then rerun T1 and a T5 known-answer check injected on our own fit, so injection
  and analysis share one curve (referee, section 6, points 2, 3 and 11). **Answered by R-CONV (2026-11-22, T-056,
  section 5.1): none of 16 conventions** (baselines L, C, Y, X; σ fixed or from the spread of d²; fixed or
  recomputed weights) reproduces column (3); all give the same two inside and four outside. Still open: the origin of
  s and the form of Λ(s), a z offset of the Sun, and whether our 79 clouds and their positions are K24's (a per-cloud
  diagnostic at K24's medians, T-061); also held fixed in all conventions: the ln(2πσ²) constant of eq. 11 (it matters
  only under P) and priors centred near K24's results, which attenuate our offsets. **Partly answered by R-DIAG
  (2026-11-24, T-061, section 5.2):** with the reconstructed per-sightline sample column (3) is partly reproduced (3 of
  6; 4 with Perseus and Taurus), while φ and the first anchor stay off; the origin of s cannot help (it is exactly
  degenerate with p, γ, φ and s₀), and a fixed z☉ shift makes it worse. Still open: whether the gain comes from the
  sample or from its larger total kernel weight (T-065), and the 54 bridging sightlines, which carry most of the
  per-object difference at K24's medians.
- T8 needs a likelihood that is proper in ω₀ when the v_z divisor is fitted (for example an untruncated
  velocity term, or a fixed divisor with ω₀ entering only through the frequency); as pre-registered it
  is uninformative (section 6, point 1). **Answered by T8-P (2026-11-22, T-056, section 5.1):** with the divisor
  fixed, the data constrain ln ω₀ about as tightly as K24's prior and prefer 59 km s⁻¹ kpc⁻¹; the label is
  "prior-driven" (half-width 0.172 against 0.085), and K24's 67.7 lies between prior and data.

## 8. Exploring via chat

How a coding agent answers "what if" questions about this study without touching `results/`
(rules: AGENTS.md section 2).

| Knob (`PARAMS`) | Meaning | Safe range | Cache only, or new data (size)? |
|---|---|---|---|
| `parts` | which tests to run (`t1t2`, `t3`, `t4`, `t5`, `t6`, `t7`, `t8`); the column-(3)–(6) chains always run | any subset | cache only (the two tables, 16 KB; `["diag"]` also reads the three R-DIAG files of section 3, 113,017 bytes) |
| `parts` = `["conv"]` or `["t8p"]` | README 4.10's post-hoc R-CONV (16 column-(3) conventions, the choice, the reruns) or T8-P (ω₀ with the divisor fixed at 74); standalone: never with the other parts, which are only read | one of them (both together only in an exploration) | cache only |
| `parts` = `["diag"]` | README 4.11's post-hoc R-DIAG (Part A per-cloud terms, Part B the reconstructed sightline sample S with S_all and S+PT, Part C K24's published curve, Part D the origin of s free with c-ref and z☉ = 20.8 pc, the reading); standalone like `conv` | alone in a formal run; with `conv` / `t8p` only in an exploration | the two tables plus the three R-DIAG files (Zucker 2020, Alves 2020 bridging sightlines, K24's curve; 113,017 bytes via `ctx.http`, cached after the first run); needs `results/rconv.json` |
| `rdiag_member_k`, `rdiag_member_floor_pc`, `rdiag_pt_names`, `rdiag_s_all_n`, `rdiag_pt_n` | R-DIAG Part B: tolerance k max(spread, floor) per axis (3, 5 pc), the gate max(spread, floor), the names added in S+PT, and the stop checks (S_all = 169, S+PT − S = 28) | k 2–4, floor > 0 (up to 20 pc) in an exploration; k and the floor change only S, so the stop checks still pass (only a change to `rdiag_pt_names` changes S+PT − S and then needs a new `rdiag_pt_n`) | cache only |
| `rdiag_map_prior_draws`, `rdiag_top_n`, `rdiag_c_prior_pc`, `rdiag_c_scale_pc`, `rdiag_cref_s0_prior_pc`, `rdiag_c_halfwidth_max_pc`, `rdiag_zsun_pc`, `rdiag_d6_max`, `rdiag_m6_max`, `rdiag_curve_*` | R-DIAG Parts A, C, D and the reading: MAP starts (2 + 19), the ten largest Δᵢ, c ~ U(−400, 400) pc (also Part C's bound on c) with scale 100 pc, c-ref's flat s₀ U(−1,000, 3,000), the data-driven limit 100 pc, z☉ 20.8 pc, D₆ ≤ 8.781 and M₆ ≤ 3.192, the curve-label thresholds 5 / 15 / 20 pc and 10% (pre-registered values, README 4.11) | changed only in an exploration | cache only |
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
- **R-DIAG (README 4.11, post hoc).** Formal procedure: after R-CONV (`results/rconv.json` and `summary.json` must exist), set
  `"parts": ["diag"]` in `PARAMS` (committed, with a line in `log.md`), run `python -m astrolab run 011-m11-radcliffe-wave-oscillation`,
  rerun after each pause at `stop_after_hours` until it completes (it resumes from `s011_checkpoints/diag/<key>` and deletes that
  folder when done), then set `parts` back to the default list. Only `rdiag.json`, the `R_DIAG` key of `summary.json` and the `_diag`
  records are written (`_diagpaused` while paused). The run stops before any fit unless S_all has 169 points and S+PT 28 more than S;
  the formal L-F-W numbers (count 2, D₆ 9.781, M₆ 3.692) and v_P are read from `rconv.json` convention 0 at run time. Runtime,
  measured on the real inputs while the machine was busy: one column-(3) likelihood takes about 0.73 ms on the 79 rows and 1.05–1.12 ms
  on S (149 points); the Part C distance sum about 9 ms. Taking each chain as 48 × 18,000 evaluations (doubled steps): S, S_all and S+PT
  about 16–19 minutes each, (c), c-ref and (z☉) about 11–12 minutes each; the MAP (21 starts) about 2 minutes; the Part C fit about
  1–2 minutes. In all about 1.5–2 hours on one core. A data-path check: `--set parts='["diag"]' mcmc_steps=200 mcmc_burn=100
  mcmc_walkers=32 ml_nm_maxfev=300 ml_lbfgs_maxfun=100 rdiag_map_prior_draws=2` (about 1 minute; the chains are far too short to read).
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
    (`label`, `at_bound`, `halfwidth_broad`, `median_shift_in_sigma_broad`, `omega0_k24`, `omega0_broad`); after R-DIAG also
    `R_DIAG` (`reading`, `labels`, `n_points`, `counts`, `D6`, `c_median_pc`, `c_ref_halfwidth_pc`, `chain_short`).
  - `results/rdiag.json` (README 4.11): `reading`, `reading_detail`, `labels` (`S`, `S_all`, `S+PT`, `c`, `zsun`, `c_reading`,
    `curve`), `formal_reference` (rconv.json convention 0: `count`, `D6`, `M6`, thresholds), `v_P`, `part_a` (`vectors` K, P, M with
    lnL, ln prior, ln posterior, σ_P; `map`; `comparisons` `K_minus_M` and `K_minus_P` with `top`, `share_of_positive_sum`,
    `sum_named`, `sum_bridges`; `objects` per cloud s, weight, d², tᵢ at each vector), `part_b` (`samples` with their points and
    weights, `consistency_table`, `fallback_rows`, `absorbed_rows`, `fits` per sample: `count`, `inside`, `sigma_scaled_differences`,
    `D6`, `M6`, `width_ratio`, `parameters`, `sigma_P_at_median_pc`, `status`, `label`, `chain`), `part_c` (`comparison`: x–y and 3-D
    distance statistics, exclusions, first and last points, `label`; `lsq_fit`: parameters, `c_pc`, σ-scaled differences from K24's
    column (6), `rms_pc`), `part_d` (`c` with `c_posterior` incl. correlations, `zsun` with `weights_max_abs_change`, `c_ref`,
    `c_reading`), `timing`, `chain_short`.
- Example questions:
  - "Is T5's verdict sensitive to the wavelength band?" → `--set t5_band='[0.7, 1.4]' parts='["t5"]'` (about 45 minutes).
  - "What if the Wave's scatter were 35 pc?" → `--set sigma_pc=35` (new fits; hours).
  - "Do older clusters scatter more?" → `--script explore/age_scatter.py`.
  - "How much does the Sun's period depend on its vertical velocity?" → `--set sun_vz_kms=7.25 parts='["t8"]'` (about 70 minutes; only the divisor-74 variant is meaningful, section 6 point 1).
  - "Does T8 need the ln ω₀ normalisation?" → `--script explore/t8_jacobian.py`.
  - "Which baseline, σ and weight convention reproduces K24's column (3)?" → the formal R-CONV run above (`parts=["conv"]`).
  - "Is ω₀ set by the data once the divisor is fixed?" → the formal T8-P run (`parts=["t8p"]`, about 0.7 hours).
  - "Does column (3) depend on the input sample, the origin of s or the Sun's height?" → the formal R-DIAG run (`parts=["diag"]`,
    about 1.5–2 hours); "what if the membership tolerance were k = 2?" → `--set parts='["diag"]' rdiag_member_k=2` (S changes; S_all
    and S+PT − S do not, so the stop checks still pass).
- Findings that change what we know go into `log.md` (and, for a paper study, the wiki article)
  on a branch.
