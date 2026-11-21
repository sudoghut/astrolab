# Is the Radcliffe Wave waving? Young clusters and a Galactic oscillation

[English](#english) · [中文](#中文)

*Paper: Konietzka, Goodman, Zucker, Burkert, Alves, Foley, Swiggum, Koller, Miret-Roig 2024, "The Radcliffe Wave is oscillating", Nature 628, 62–65, doi:10.1038/s41586-024-07127-3, [arXiv:2402.12596](https://arxiv.org/abs/2402.12596). Study:
[`studies/011-m11-radcliffe-wave-oscillation`](https://github.com/sudoghut/astrolab/tree/main/studies/011-m11-radcliffe-wave-oscillation) (web page: [online](https://sudoghut.github.io/astrolab/studies/011-m11-radcliffe-wave-oscillation/web/)).
Status: planned. Last updated: 2026-11-21 (see the changelog at the end). The source of this page lives in the main repository at
[`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki); edit it there.*

*中文标题：Radcliffe 波在振荡吗？年轻星团与银河系中的竖直振荡。状态：计划中。论文：Konietzka, Goodman, Zucker, Burkert, Alves, Foley, Swiggum, Koller, Miret-Roig 2024，Nature 628, 62–65，doi:10.1038/s41586-024-07127-3，[arXiv:2402.12596](https://arxiv.org/abs/2402.12596)。研究：[`studies/011-m11-radcliffe-wave-oscillation`](https://github.com/sudoghut/astrolab/tree/main/studies/011-m11-radcliffe-wave-oscillation)（网页：[在线版](https://sudoghut.github.io/astrolab/studies/011-m11-radcliffe-wave-oscillation/web/)）。最后更新：2026-11-21（见文末"研究进展"）。本页源文件在主仓库的 [`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki) 中，请在那里修改。*

---

## English

### Part 1 · The paper in plain language

All numbers below were read from the arXiv version (arXiv:2402.12596v1, the accepted manuscript,
main text plus Methods and Extended Data); we did not compare it line by line with the typeset
Nature version. "K24" below means this paper.

#### 1.1 The question and why it matters

Our Sun sits inside a thin disc of stars and gas. Close to us (the nearest part is about 250–300
parsec (pc) away; 1 pc ≈ 3.26 light years) lies a chain of dense, star-forming gas clouds about
2.7 kiloparsec (kpc) long: Canis Major OB1, Orion, Perseus, Taurus, Cepheus, the North America
Nebula and Cygnus X. In 2020, Alves et al. (Nature 578, 237; arXiv:2001.08748) mapped the
three-dimensional positions of these clouds with 3D dust maps and found that they are not scattered:
they form a narrow, coherent line that snakes above and below the Galactic midplane like a damped
sine wave, "with an average period of about 2 kpc and a maximum amplitude of about 160 pc". They
named it the **Radcliffe Wave**.

A shape alone does not tell you whether anything is moving. A wavy rope lying on the floor and a
rope being shaken look the same in one photograph. To know whether the Radcliffe Wave is a real wave
(whose stars actually oscillate up and down through the plane, with the vertical velocities a
wave predicts at each position), one needs **velocities**, in particular the
vertical velocity v_z, perpendicular to the disc. Earlier kinematic studies with young stars
(Tu et al. 2022; Thulasidharan et al. 2022; Bobylev et al. 2022; Li & Chen 2022; Alfaro et al. 2022;
Donada & Figueras 2021) gave mixed or inconclusive answers; K24 calls them "inconclusive".

Why it matters:

- If the whole 2.7-kpc structure oscillates coherently, its motion is set by the Galaxy's vertical
  gravity, so the Wave becomes a giant "pendulum" that weighs the local disc: the midplane mass
  density, the amount of dark matter near the Sun, and the period with which the Sun itself bobs
  up and down through the disc.
- How such a structure forms (a passing satellite galaxy, gas falling in, an instability in the
  disc, supernova feedback) is open; whether it travels, stands still or drifts constrains these.
- Many of the nearest star-forming regions belong to it, so its motion is the motion of the gas that
  forms the nearby young stars, including (K24 suggests) the cluster whose supernovae blew the Local
  Bubble, the hot cavity the Sun sits in.

#### 1.2 The data

Gas clouds cannot easily be followed in three dimensions: a radio telescope measures only how fast
gas moves towards or away from us (one velocity component). Young star clusters are easier. A
cluster is a group of stars born together from the same cloud; when it is young, it still moves
with the gas it came from. The Gaia satellite measures each star's distance (from its parallax) and
its motion across the sky (proper motion); a spectrograph measures its velocity along the line of
sight (radial velocity). Averaging over the member stars of a cluster gives the cluster's position
and full 3D velocity much more precisely than for one star.

Precisely, K24 uses:

- **Young stellar clusters** (Methods, "Stellar Cluster Catalog"). Clusters from the Cantat-Gaudin
  et al. 2020 catalogue (Gaia DR2-based, keeping only good parallaxes, proper motions and radial
  velocities), plus clusters from five other catalogues (Sim et al. 2019, Hao et al. 2022, He et al.
  2022, Szilágyi et al. 2021, Liu & Pang 2019); members cross-matched with Gaia DR3; radial
  velocities from Gaia and from the APOGEE survey (SDSS DR16) to increase coverage. For each cluster:
  mean position (x, y, z) and velocity (u, v, w) in heliocentric Galactic Cartesian coordinates, with
  standard errors of the mean. Selection:
  - **ages below 30 Myr** (million years), taken from the literature, "guaranteeing" in K24's words
    that the clusters still trace the velocities of their natal clouds;
  - clusters with radial velocities above 50 km/s relative to the local standard of rest (LSR, the
    frame of a circular orbit at the Sun's position) removed as kinematic anomalies;
  - selection on the x–y plane only (top-down view): clusters within ±5 times the Wave's radius
    (47 pc, i.e. ±235 pc) of the best-fit dust model, with **no a priori cut in height z** — so the
    vertical pattern is not built in by the selection;
  - the Lacerta OB1 association is removed because it is vertically and kinematically distinct;
  - a check against the Hunt & Reffert 2023 Gaia DR3 cluster catalogue (youngest clusters only)
    reportedly has no effect.
  Velocities are converted to the LSR with the solar peculiar motion (u☉, v☉, w☉) = (10.0, 15.4, 7.8) km/s, giving (v_x, v_y, v_z).
  The number of clusters is not stated in the text; the public table (Harvard Dataverse
  doi:10.7910/DVN/XSCB9N, file `Radcliffe_Wave_stellar_clusters_Konietzka2024.tab`, 10,888 bytes,
  CC0) is described as the machine-readable table of the clusters used in K24; its columns and
  number of rows are not documented on the landing page and will be read by the study (of order 10²
  rows judging from the figures).
- **Molecular clouds**: 3D cloud positions from the Major Cloud Catalog (Zucker et al. 2019, 2020) and
  the "Tenuous Connections" catalogue of Alves et al. 2020, keeping only clouds with a radial-velocity
  measurement. Distances carry an extra systematic uncertainty of about 5%.
- **¹²CO line-of-sight velocities** (Methods, "Line-of-sight Gas Velocities"). Carbon monoxide (CO)
  emits at a radio wavelength of 2.6 mm; its Doppler shift gives the gas velocity along the line of
  sight, v_LSR. K24 uses the Dame et al. 2001 Galaxy-wide CO survey (angular resolution 0.125°,
  velocity resolution 1.3 km/s), extracts a spectrum within 0.3° of each cloud position, keeps
  |v_LSR| < 30 km/s, and fits Gaussians (Levenberg–Marquardt); 9% of clouds are dropped (outside the
  survey or no emission). Because the Wave is close and long and rises ~200 pc above the plane, lines
  of sight to different clouds point in very different directions, so a 1D velocity probes different
  mixes of v_x, v_y and v_z — including the vertical one. Public table: doi:10.7910/DVN/Q7F4PC, file
  `Radcliffe_Wave_CO_analysis_Konietzka2024.tab`, 5,286 bytes, CC0 (columns and rows to be read by
  the study).

#### 1.3 Step by step: how the authors got from data to conclusion

**Step 1 · Clusters and clouds trace the same structure.** Figure 1a shows the young clusters (blue)
lying on the same 3D sinusoid as the clouds (red), although the clusters were selected without any
cut in z. K24 concludes that the clusters were born in the Wave's clouds and can serve as tracers of
its motion. Figure 1b plots the same clusters with v_z as the third axis: the velocities also form a
wave, shifted along the structure relative to the position wave.

**Step 2 · The vertical force: an anharmonic oscillator.** For small excursions, a star near the
disc moves up and down like a mass on a spring (a harmonic oscillator) with angular frequency ν,
where ν² = 4πGρ₀ and ρ₀ is the midplane density. The Wave reaches ~220 pc, comparable to the
disc's scale height, where the restoring force weakens and the oscillation slows down, like a
pendulum swinging far from vertical. K24 writes the vertical potential as (Methods, eq. 1)

  Φ(z, r) = ½ ω₀² exp[(r☉ − r)/r₀] (z² − μ₀² z⁴),

with r☉ = 8.4 kpc, ω₀ the small-amplitude angular frequency at the Sun's radius, r₀ the radial scale
length of the density, and μ₀ is proportional to the inverse vertical scale height (z₀ = 1/(√6 μ₀)). These three numbers are not fitted to
the Wave at first: they are obtained by a χ² fit of eq. 1 to an existing Milky Way model (Allen &
Santillan 1991 with the updated parameters of Irrgang et al. 2013) over r = 7–10 kpc and |z| ≤ 300 pc:
**ω₀ = 74 km s⁻¹ kpc⁻¹, r₀ = 3.7 kpc, μ₀ = 1.3 kpc⁻¹**, implying a local density ρ₀ ≈ 0.1 M☉ pc⁻³
and scale height z₀ = 1/(√6 μ₀) = 314 pc (literature: 0.097 ± 0.013 M☉ pc⁻³ and 280 (+70/−50) pc,
McKee et al. 2015). Energy conservation then gives the period T of a cloud that rises to z_max
(eq. 2), and with the complete elliptic integral of the first kind K an analytic frequency ω(z_max, r) (eq. 3), which falls as
the amplitude grows. Because the Wave crosses different Galactocentric radii, r and z_max are
functions of the position s along the Wave, so ω = ω(s). The potential is assumed stationary; tilts,
the Galactic warp and the "radially evolving vertical waves" near the Sun (Schönrich & Dehnen 2018;
Xu et al. 2015) are argued to be negligible.

**Step 3 · The wave model.** Along its length the Wave is described by (eqs. 4–5)

  z(s, t) = ζ(s) [ B sin(ω₀t + 2πΛ(s) + φ) + (1 − B) sin(−ω₀t + 2πΛ(s) + φ) ],
  v_z(s, t) = ζ(s) ω(s) [ B cos(ω₀t + 2πΛ(s) + φ) − (1 − B) cos(−ω₀t + 2πΛ(s) + φ) ].

Here s is the distance along the Wave projected on the x–y plane (s = 0 at its start, near CMa OB1);
the baseline in the plane is a quadratic curve through three anchor points (x₀, y₀), (x₁, y₁),
(x₂, y₂); ζ(s) is the vertical envelope; Λ(s) is the cumulative phase; φ is a phase constant; t is
time (ω₀t is the present phase offset). The parameter **B mixes two waves running in opposite
directions**: B = 1 (or 0) is a pure **travelling wave**, B = 0.5 a pure **standing wave**.

- *Why the phase of z and v_z matters.* In a travelling wave, z ∝ sin(…) and v_z ∝ cos(…): the
  velocity is largest where the Wave crosses the plane and zero at the crests — a **90° phase offset**
  between position and velocity along the Wave. In a standing wave (B = 0.5) the two terms combine to
  z = ζ sin(2πΛ + φ) cos(ω₀t) and v_z = −ζω sin(2πΛ + φ) sin(ω₀t): z and v_z have the same spatial
  pattern (**zero phase offset**), and the zero crossings (nodes) never move. So the relative phase of
  the position wave and the velocity wave is the observable that distinguishes the two.
- *Travelling wave and the potential.* For a travelling wave, given the potential, the spatial shape
  fully determines v_z (amplitude times ω(s)); for a standing wave the velocity amplitude at the crests
  is not fixed by the shape. That is why the fit can predict v_z from z with no free velocity
  amplitude.
- *Wavelength that shrinks along the Wave* (eqs. 6–7): Λ(s) = s/(p − γs), so the local wavelength is
  λ(s) = (p − γs)²/p. K24 calls p "the period of the Wave" but it is a length (pc): the wavelength at
  s = 0; γ sets how fast it shrinks.
- *Damping* (eq. 9): ζ(s) = −A [1 + ((s − s₀)/δ)²]⁻¹, a Lorentzian envelope of amplitude A peaking at
  s₀ with width δ. K24 found a Lorentzian marginally better than the Gaussian of Alves et al. 2020,
  and notes that a mixture (e.g. a Voigt profile) is probably the truth but too poorly constrained.
- The vertical model has 14 parameters Θ₁ = (x₀, y₀, x₁, y₁, x₂, y₂, A, p, φ, s₀, δ, γ, ω₀t, B); the
  in-plane motion adds two, Θ₂ = (v_x,plane, v_y,plane).

**Step 4 · The fit.** For each cluster k, the "distance" to the model is a 4-vector
(x, y, z, v_z/ω₀) minus the model at the closest point s_min (eq. 12); dividing v_z by ω₀ turns it into
a length so positions and velocities count equally. The likelihood (eq. 13) uses a common scatter σ,
kernel-density weights so densely sampled regions such as Orion do not dominate, and a soft outlier
function C (a tanh truncation): a cluster is an outlier if any component c = tanh(x²) exceeds tanh(3),
which K24 describe as lying outside a 3σ radius (per component this is |x| > √3 ≈ 1.7σ; our reading). Clouds use a 3D version (eq. 11). Sampling is done with the nested-sampling code dynesty
(1000 live points), with independent priors "based on initial fits" (Extended Data Table 1), e.g.
A ~ N(215, 20) pc, p ~ N(4650, 300) pc, ln γ ~ N(0.35, 0.07), ln(δ/pc) ~ N(6.5, 0.1),
s₀ ~ N(680, 200) pc, φ ~ N(−0.09, 0.5) rad, ω₀t ~ U(−π/2, π/2), B ~ U(0, 1), in-plane velocities
~ U(−10, 10) km/s. The scatter σ is 47 pc, the "radius" of the Wave.

**Step 5 · The numbers (Extended Data Table 2; ± are 16th–84th percentiles).**

| Parameter | (3) clouds only | (4) clusters only | (5) clusters, mixture (B free) | (6) clouds + clusters | (7) clouds + clusters, ω₀ μ₀ r₀ free |
|---|---|---|---|---|---|
| A (pc) | 219.88 +18.34/−16.24 | 216.52 +11.54/−10.95 | 229.32 +13.23/−12.18 | 218.64 +13.81/−11.41 | 222.92 +13.32/−12.5 |
| p (pc) | 4773.99 +189.15/−187.63 | 4752.21 +207.28/−198.8 | 4715.14 +216.07/−214.2 | 4779.9 +195.49/−192.26 | 4749.05 +191.12/−182.03 |
| δ (pc) | 797.78 +67.28/−62.43 | 624.25 +60.19/−55.96 | 649.14 +61.95/−56.19 | 740.01 +58.78/−55.14 | 738.57 +59.33/−52.89 |
| s₀ (pc) | 482.71 +113.81/−103.35 | 673.18 +104.02/−103.13 | 662.89 +112.13/−107.4 | 544.99 +89.88/−100.53 | 517.02 +99.91/−91.41 |
| γ | 1.49 ± 0.07 | 1.4 +0.09/−0.07 | 1.4 +0.1/−0.08 | 1.46 +0.08/−0.07 | 1.46 +0.09/−0.07 |
| φ (rad) | −0.12 +0.13/−0.14 | −0.23 ± 0.16 | 0.01 +0.25/−0.23 | −0.15 ± 0.13 | −0.14 +0.13/−0.14 |
| ω₀t (rad) | – | – | −0.38 +0.19/−0.17 | – | – |
| **B** | – | – | **0.84 +0.07/−0.06** | – | – |
| ω₀ (km s⁻¹ kpc⁻¹) | – | – | – | – | 67.713 +7.677/−7.111 |
| μ₀ (kpc⁻¹) | – | – | – | – | 1.377 +0.249/−0.247 |
| r₀ (pc) | – | – | – | – | 3563.32 +513.7/−500.43 |

(The anchor points x₀…y₂ are also in the table; they agree between columns within ~1σ. The caption
says column (7) is "the same approach as in (5)", but its heading — clouds + clusters — matches (6);
we read (7) as (6) with the potential freed.) K24 states that the fits to clouds alone, clusters
alone and both together are consistent, which it takes as confirmation that clouds and young clusters
form one spatially and kinematically coherent structure. The best fit is drawn in Figure 1 (in
plain Galactic x, y, z); Extended Data Figs. 1–3 use an x–y frame rotated anticlockwise by 62° so
that their horizontal axis ("position along the Wave", about −1300 to +1500 pc with 0 near the Sun)
runs along the Wave.

Derived numbers (main text and Methods):

- **Maximum amplitude ~220 pc; mean wavelength ~2 kpc** (about 2000 pc, ranging from ~4000 pc near
  CMa OB1 to ~400 pc near Cygnus X, from eq. 7). Our check: with column (6), λ(0) = p ≈ 4.78 kpc,
  λ(0.3 kpc) ≈ 3.9 kpc, λ(2.4 kpc) ≈ 0.34 kpc, and the average of λ(s) over 0–2.4 kpc is ≈ 2.1 kpc,
  consistent with K24's description (our reading; the s-range of the data is assumed).
- **Maximum vertical velocity ~14 km/s.**
- **Travelling, not standing.** B = 0.84 (+0.07/−0.06) with a flat prior on [0, 1]. A separate fit
  with B fixed to 1 gives a log Bayes factor ΔlnZ = ln Z₂ − ln Z₁ ≈ 1 (Z₁: B = 1, Z₂: B free); K24
  says "both models are an equivalently good fit to the data, while the realization with fixed B = 1
  is slightly preferred" (that fit also fixes ω₀t = 0), concludes that "the Wave's motion is of first
  order consistent with a traveling wave", and sets B = 1 thereafter. The standing wave (B = 0.5) is excluded by a
  separate argument: for B = 0.5 the per-cluster phases φ_k = arctan(z_k ω_k / v_z,k) should be nearly
  constant along s (varying by at most ~0.03π), but they sweep the whole range −π/2 to π/2. In the
  main text this becomes "a traveling wave is strongly preferred over a standing wave", next to the
  Methods' "of first order consistent with a traveling wave".
- **Phase velocity** (the speed at which the crests appear to move, λ(s)/T(s)): from ~40 km/s near
  CMa OB1 to ~5 km/s near Cygnus X, crests moving right to left as seen from the Sun. Explaining this
  order-of-magnitude change by a change in local density would need ρ₀ to vary by at least two orders
  of magnitude, which K24 rejects; it suggests two physical processes may have shaped the Wave.
- **Outliers.** All clusters in Perseus and Taurus come out as outliers; K24 attributes this to the
  expansion of the Local and Per–Tau feedback bubbles on whose surfaces they lie. Most remaining
  outliers are in Orion, where outliers number no more than a quarter of the inliers (≤ 20% of the
  clusters).
- **Sun's height.** Freeing the Sun's height above the plane (uniform prior −10 to 25 pc) shifts A, φ
  and δ by less than a third of their 1σ errors; the other parameters by less than 10% of 1σ.
- **Plane tilt and potentials.** Tilting the plane (two extra angles), and replacing the potential by
  McMillan 2017 or galpy's MWPotential2014 (Bovy 2015), reportedly have no effect.

**Step 6 · The CO check.** Projecting the best-fit 6D model (x, y, z, v_x, v_y, v_z) onto each
cloud's line of sight, v_LSR = cos l cos b v_x + sin l cos b v_y + sin b v_z (eq. 14), gives a curve
that passes through the measured ¹²CO velocities (Extended Data Fig. 3a: v_LSR falls from ~+20 km/s
at the CMa end to ~0–2 km/s at position ≈ 0–500 pc along the rotated axis of Extended Data Fig. 3a
(not s, which starts at 0 near CMa OB1) and rises to ~+6 km/s at the far end). K24 concludes that
"our model explains the ¹²CO observations", i.e. the gas moves with the clusters. The agreement is
shown graphically; no goodness-of-fit number is given.

**Step 7 · In-plane drift.** After subtracting Galactic and differential rotation (Allen & Santillan
potential; two alternatives "no effect"), a χ² fit with a typical error of 2 km/s gives
v_x,plane = −3.9 (+2.6/−2.7) km/s and v_y,plane = 3.1 (+2.7/−2.6) km/s, i.e. 4.9 km/s (Extended
Data Fig. 2: 4.87) radially away from the Sun and 1.0 km/s (0.96) along the Wave. K24 describes this
as a solid-body drift "radially away from the Galactic Center with a velocity of around 5 km s⁻¹".
Run backwards, the drift points towards where the Upper Centaurus Lupus and Lower Centaurus Crux
clusters formed 15–16 Myr ago, whose supernovae created the Local Bubble; K24 says an exact traceback
is beyond its scope.

**Step 8 · Weighing the disc with the Wave.** Freeing ω₀, μ₀ and r₀ (column 7; 15 parameters with
B = 1) gives ω₀ = 68 (+8/−7) km s⁻¹ kpc⁻¹, μ₀ = 1.4 ± 0.2 kpc⁻¹, r₀ = 3.6 ± 0.5 kpc, consistent with
the adopted 74, 1.3 and 3.7; the evidence ratio between fixed and free potential is again
ΔlnZ ≈ 1 ("equivalently good"). With the isothermal-sheet relations ρ₀ = ω₀²/(4πG) and
z₀ = 1/(√6 μ₀) (Spitzer 1942):

- **total midplane density ρ₀ = 0.085 (+0.021/−0.017) M☉ pc⁻³**, scale height z₀ = 294 (+63/−43) pc
  (K24 cautions that z₀ above ~300 pc changes the frequency by less than the noise), surface density
  Σ₀ = 2 z₀ ρ₀ = 50.3 M☉ pc⁻²;
- subtracting the baryons (stars and gas, 0.084 ± 0.012 M☉ pc⁻³, McKee et al. 2015): **local dark
  matter density 0.001 (+0.024/−0.021) M☉ pc⁻³** for a spherical halo, consistent with zero and with
  conventional estimates at 1σ;
- **the Sun's vertical oscillation period 95 (+12/−10) Myr**, using the Sun's vertical velocity
  7.8 km/s and 2000 Monte Carlo draws; K24 compute it in the potential fitted to the Wave with the frequency parameters left free (column (7), ω₀ ≈ 68 km s⁻¹ kpc⁻¹; our reading of the Methods); so the Sun **crosses the disc every 48 (+6/−5) Myr**. The Sun's
  height (−10 to 25 pc) changes it by < 0.5 Myr; R☉ from 7.9 to 8.7 kpc has no effect. For comparison,
  baryons alone (McKee et al. 2015, Σ₀ = 47.1 M☉ pc⁻²) give 95.3 Myr, and baryons plus a dark halo of
  0.013 M☉ pc⁻³ give 88.2 Myr, both within 1σ;
- **a thin dark disc**: assuming a dark-disc scale height of 25 pc, which K24 call "comparatively
  large" (conservative, since a thinner disc of the same surface density would shorten the period
  more), and no additional dark halo (which "would only lower the upper bound further"), the 95-Myr
  period gives a surface density of 0.1 (+3.3/−3.3) M☉ pc⁻², which K24
  calls an upper bound (our reading: consistent with zero, with ~3.4 M☉ pc⁻² as the 1σ upper end).

**Back of the envelope.** (1) *Velocity amplitude.* For a small oscillation the angular frequency is
ω₀ = 74 km s⁻¹ kpc⁻¹ = 0.076 Myr⁻¹ (1 km s⁻¹ kpc⁻¹ ≈ 1/978 Myr⁻¹). At z_max = 220 pc the anharmonic
correction of eq. 3 (μ₀z_max ≈ 0.29) lowers it by ~7% to about 0.070 Myr⁻¹ at the Sun's radius
(our evaluation). Velocity amplitude = amplitude × angular frequency ≈ 220 pc × 0.070 Myr⁻¹ ≈
15 pc/Myr ≈ 15 km/s (1 pc/Myr ≈ 0.98 km/s), close to the reported ~14 km/s (the radial factor
exp[(r☉ − r)/(2r₀)] of eq. 3 and where along the Wave the amplitude peaks account for the rest; our reading). (2) *Period.* The Sun, with v_z = 7.8 km/s, rises only ~100–115 pc (our estimate). With the fitted
ω₀ = 68 km s⁻¹ kpc⁻¹ (0.0695 Myr⁻¹) and the ~2% anharmonic correction at ~115 pc, 2π/ω ≈ 92 Myr,
close to K24's 95 (+12/−10) Myr; this is our independent estimate, not K24's calculation (in the adopted ω₀ = 74 potential the Sun's period would be
≈ 83–84 Myr). (3) *Density.* ρ₀ = ω₀²/(4πG): ω₀ = 68 km s⁻¹ kpc⁻¹ =
2.2 × 10⁻¹⁵ s⁻¹ gives 5.8 × 10⁻²¹ kg m⁻³ = 0.085 M☉ pc⁻³. (4) *Phase velocity.* λ/T ≈ 4000 pc / 95 Myr
≈ 42 km/s at the CMa end and 400 pc / 90 Myr ≈ 4.4 km/s at the Cygnus end, matching ~40 and ~5 km/s.
The headline therefore comes down to this: the Wave's height (220 pc) and its vertical speeds
(~14 km/s), shifted by a quarter wavelength, are what a body oscillating in the known disc potential
should show.

#### 1.4 What they conclude, and how sure they are

- **Claims:**
  1. the Radcliffe Wave oscillates through the Galactic plane, like a travelling wave driven by the
     Galaxy's gravity, with maximum amplitude ~220 pc, mean wavelength ~2 kpc and maximum vertical
     velocity ~14 km/s; Orion, Cepheus, North America and Cygnus X move as parts of this wave;
  2. a travelling wave is "strongly preferred" over a standing one;
  3. the gas (¹²CO) moves like the young clusters;
  4. the Wave drifts radially outward (from the Galactic Centre) at ~5 km/s, supporting the idea
     that the Local Bubble's parent cluster formed in it;
  5. treated as a coherent oscillator, it measures ρ₀ = 0.085 M☉ pc⁻³, a local dark-matter density
     consistent with zero, a dark-disc bound and the Sun's vertical period of 95 Myr.
- **Caveats the authors give:** the
  damping profile is probably a mixture that the data cannot constrain; the scale height constraint is
  weak above ~300 pc; over several tens of Myr the Wave is likely affected by cloud destruction and
  phase mixing; the ripples at the Cygnus end are at the level of the dust-distance errors; Perseus
  and Taurus do not follow the Wave; the origin of the Wave remains open.
- **Points of our reading to carry into part 2** (not raised by K24 as problems):
  - "strongly preferred" (main text) versus ΔlnZ ≈ 1 and "both models are an equivalently good fit"
    (Methods). The Bayes factor compares B = 1 with B free, not travelling with standing; the
    standing wave is excluded by the phase argument (the spread of the cluster phases φ_k), and
    the posterior interval of B, 0.84 (+0.07/−0.06), lies well above 0.5 (we do not convert this
    separation into a significance: the posterior is bounded and not Gaussian). Also, with ΔlnZ = ln Z₂ − ln Z₁ ≈ +1 and Z₂ the B-free model, the stated
    preference for fixed B = 1 seems to have the opposite sign (unless the indices are swapped):
    the printed definitions and the stated preference are inconsistent, and we cannot tell which is mistaken.
    K24 report the evidence ratios (B = 1 vs B free; fixed vs free potential) as only ΔlnZ ≈ 1 and use
    them to justify B = 1 and to call the potentials equivalent. The posterior median B = 0.84 cannot
    be read as ~2σ evidence against B = 1, because the prior is truncated at 1 (a posterior bounded
    at 1 has its median below 1 even if B = 1); the relevant comparison is the B = 1 vs B-free
    evidence ratio, ΔlnZ ≈ 1. The B = 1 fit also fixes ω₀t = 0.
  - The outlier rule tanh(x²) > tanh(3) is |x| > √3 σ ≈ 1.7σ per component, although K24 call it a
    3σ radius.
  - The priors were set "based on initial fits" to the same data, and some are about as narrow as
    the posteriors (γ: prior width in ln γ of 0.07, i.e. ±0.10 in γ, posterior ±0.07–0.09; A: prior
    ±20 pc, posterior ±11–18 pc). The γ result in particular may be largely prior-driven. The r₀ prior
    N(3659, 500) pc is as wide as its column-(7) posterior 3563 (+514/−500) pc, so r₀ there is
    prior-driven. The δ prior exp(6.5) ≈ 665 ± 67 pc sits ~2σ below the clouds-only posterior 798 pc.
    The ω₀ prior ln(ω₀/(km s⁻¹ pc⁻¹)) ~ N(−2.4, 0.17) is ω₀ ≈ 91 km s⁻¹ kpc⁻¹ ~± 17%, centred ~1.2σ
    above the adopted 74 and ~1.7σ above the posterior 68 (in ln). Only the μ₀ prior ln(μ₀ pc) ~
    N(−1.346, 0.25), i.e. 0.26 pc⁻¹, cannot be interpreted as printed (our reading).
  - The fitted vertical frequency ω(s) comes from a potential fitted to an existing Milky Way model;
    the v_z prediction is therefore not independent of the potential used to weigh the disc (step 8
    frees it, with the same data).
  - The CO agreement and the cluster agreement are shown as figures without a goodness-of-fit number.
- **What would have to be true for the authors to be wrong:**
  - *The velocities are not coherent with the positions.* Zhu et al. 2024 (ApJ 971, 167 [S: volume
    from a search listing]; arXiv:2402.15346 [V abstract]) re-estimated vertical velocities, adding
    radial velocities by two routes: (i) young stars with APOGEE-2 radial velocities and Gaia DR3
    proper motions, and (ii) cloud radial velocities with the Gaia DR3 proper motions of associated
    young stellar objects (YSOs), and found that the vertical-velocity oscillations "are not synchronous with the
    vertical coordinate": instead a gradient of about 5 km s⁻¹ kpc⁻¹ in v_z along the Wave with a
    "dipole-like" pattern, which they say brings the Radcliffe Wave model "into question". If their
    v_z pattern is right, the 90° phase relation that defines K24's travelling wave would not hold.
  - *The Wave is not a solid body over an oscillation period.* Li, Zhou & Chen 2024 (arXiv:2410.14603
    [V abstract]; journal not verified) argue with 3D simulations of the local gas that Galactic shear
    and epicyclic motion stretch the Wave "to almost twice its current length" in ~45 Myr, within which
    "only half a cycle of the proposed vertical oscillation occurs", and call treating it as a solid
    body "an oversimplification". If so, a single coherent oscillation with one phase law Λ(s) (and a
    solid-body in-plane drift) is a poor description, even if local pieces move up and down.
  - *Positions and velocities give different wavelengths, or the drift is faster.* Bobylev, Ikhsanov
    & Bajkova 2025 (Astrophys. Bull. 80(2), arXiv:2503.21019 [V abstract]) analyse open clusters by
    age: the Wave is associated with clusters no older than 30 Myr (supporting K24's age cut); for the
    5.2-Myr group they find z_max = 117 ± 12 pc with wavelength 4.55 ± 0.14 kpc in position but a
    vertical-velocity amplitude 4.86 ± 0.19 km/s with wavelength 1.74 ± 0.08 kpc; for the 18.6-Myr group
    54 ± 5 pc (λ 6.30 ± 0.12 kpc) and 7.90 ± 0.16 km/s (λ 0.83 ± 0.11 kpc); radial motion away from the
    Galactic Centre at 10 pc/Myr (≈ 10 km/s, twice K24's 5 km/s); and they favour an origin in
    supernova shock waves on a ~2 kpc front. Different wavelengths in z and v_z (our reading) are not
    what a single coherent travelling wave predicts. Their method and selection differ from K24's.
  - *Outlier and selection choices drive the signal.* All Perseus and Taurus clusters are labelled
    outliers; the soft 3σ outlier model and the kernel weights decide how much each region counts. If
    the 90° phase offset depended on these choices, or on a small number of Orion and Cepheus clusters,
    the oscillation would be less secure.
  - *The age cut does not guarantee that clusters still move with their gas.* Clusters up to 30 Myr
    old have had a third of an oscillation period to separate from their natal gas; K24 relies on the
    CO check for this.

### Part 2 · The logic of the argument

#### 2.0 Map of the argument

The encoded conclusion has three parts: (1) the Wave oscillates through the Galactic plane like a
travelling wave driven by the Galactic potential (this combines the abstract, "the Radcliffe Wave
is oscillating through the Galactic plane", with the main-text p. 2 sentence that the Figure 1
fit "indicates that the Radcliffe Wave oscillates through the Galactic plane like a traveling
wave"); (2) a travelling wave is preferred over a standing wave (main text p. 2); (3) treated as a
coherent oscillator, the Wave measures the local vertical potential (midplane density) and the
Sun's vertical period (abstract). The radial drift and the Local Bubble link are discussed, not
encoded (2.6).

A. Young clusters and clouds are co-located, and the clusters were selected on the x–y plane only;
   [gap] so the clusters were born in the Wave (K24 only suggests this); being younger than 30 Myr, they still move with their
   clouds; the model also explains the ¹²CO velocities ⇒ the clusters' kinematics are the Wave's.
B. Only gravity acts, in a stationary anharmonic potential whose parameters come from an existing
   Milky Way model ⇒ for a travelling wave the shape fixes v_z. The travelling-wave (B = 1) fit to z
   and v_z is excellent, with a 90° offset.
C. The cluster phases sweep −π/2 to π/2, which a standing wave forbids ([gap] unless the spread is
   noise); the mixture fit gives B = 0.84, closer to 1 than to 0.5; [gap] both rest on a cluster v_z pattern
   that belongs to the Wave ⇒ **a travelling wave is preferred over a standing wave**; B = 1 and
   B free fit equivalently well ⇒ B = 1 is adopted.
D. With B = 1 adopted, the excellent fit, [gap] the same robust v_z pattern and [gap] one coherent
   wave despite Galactic shear ⇒ **the Wave oscillates like a travelling wave**.
E. With the potential freed, the fit gives ω₀ = 68 km s⁻¹ kpc⁻¹; the isothermal sheet turns it into
   a density; [gap] that posterior is set by the data, not by priors from initial fits ⇒ **the Wave
   weighs the local disc and gives the Sun's period**.

The order matters: the fit shown in Figure 1, which K24 reads as oscillation, is the B = 1
realisation, adopted only after the mixture fit and the evidence comparison ("implying that we can
set B = 1 in all further performed calculations"). So the oscillation claim (D) comes after the
travelling-versus-standing step (C), not before it.

How we check it: the argument is written in Lean 4
([`studies/011-m11-radcliffe-wave-oscillation/argument/Argument.lean`](https://github.com/sudoghut/astrolab/blob/main/studies/011-m11-radcliffe-wave-oscillation/argument/Argument.lean)).
Each premise is one constructor of `Field` (no axioms), labelled with its kind and its
provenance:

| Tag | Kind of premise |
|---|---|
| `OBS` | observation or measurement (with table / figure) |
| `MOD` | modelling assumption, or an inference rule the paper states |
| `STAT` | statistical inference (fit quality, model–data agreement, posterior, model comparison) |
| `NUM` | numerical result, re-computed by this repo's `run.py` (none yet: the study has no results) |
| `LIT` | result taken from other literature |
| `GAP` | premise the inference needs that neither the paper nor standard knowledge supplies |

Provenance: `[stated: "quote"]` (the paper says it, quoted from the arXiv v1 text),
`[implied]` (standard knowledge the paper relies on without writing it out, with a source),
`[reconstructed]` (our addition; exactly the `GAP` premises; literature published after K24 enters
here, because K24 cannot rely on it).

What Lean checks: that the conclusion follows from these premises (`final`) and is not trivially
true (`final_nontrivial`); that the premises can hold together (`consistent`); that no single
premise gives the conclusion alone (`alone_insufficient`); for each premise, whether it is needed
(a countermodel without it) or redundant; whether the premises the paper actually states are
enough (`stated_*`), and whether they are enough once standard knowledge is added (`explicit_*`;
`explicit_insufficient` means a real gap). What Lean does not check: the physics and statistics
inside each premise — that is what parts 1 and 3 and the study are for.

Several K24 sentences are inference rules ("we find that the Radcliffe Wave oscillates like a
traveling wave", "we can
transfer our results ... including the gas", "a traveling wave is strongly preferred", "by treating
the Wave as a coherently oscillating structure, we can ... directly measure ..."). We encode each
as an implication and, where our analysis says the step needs more, add the missing conditions as
extra antecedents; an implication with more antecedents is weaker than the quote, so the
`[stated]` label stays honest, and the missing conditions appear as separate `GAP` premises.
A hedged inference ("suggesting", "indicates") is never encoded as a stated implication, because
that would assert more than the quote: either the step becomes a `GAP` (the clusters' birth in the
Wave), or a categorical sentence of K24 for the same step is quoted instead (the Methods' "we find
that the Radcliffe Wave oscillates like a traveling wave" in place of the main text's "indicates";
the main text's "we find that a traveling wave is strongly preferred" in place of the Methods'
"The value of B closer to 1 indicates that data favors a traveling wave").

#### 2.1 Stage A · The young clusters trace the Wave

*Overview.* The Wave was found in gas (3D dust maps); its velocities come from young clusters. The
link is: clusters and clouds are in the same place although the cluster selection had no height
cut, so the clusters were born in the Wave; they are young, so they have not yet drifted away from
their clouds; and the model fitted to the clusters (with the clouds) also reproduces the gas's
line-of-sight velocities.

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `obs_coloc`: young clusters and clouds are co-located in 3D | OBS | stated: "As expected, the young clusters and star-forming molecular clouds are co-located in three dimensions." | main text p. 1, Fig. 1a |
| `mod_xy`: the clusters were selected on the x–y plane only, with no cut in height | MOD | stated: "We make a conservative selection on the x-y plane by enclosing all stellar clusters within ±5 times the radius of the Wave (47 pc) from the best fit of the dust component" | Methods, Stellar Cluster Catalog |
| `gap_born`: co-location + no height cut ⇒ the clusters were born in the Wave's clouds | GAP | reconstructed | K24 only suggests it (main text p. 1: selected "without an a priori selection criterion for height off the Galactic plane (see Methods), suggesting that the clusters' stars were born in the molecular clouds along the Radcliffe Wave") |
| `mod_age`: born in the Wave and < 30 Myr ⇒ still moving with the natal clouds | MOD | stated: "We restrict our analysis to only the youngest clusters (ages smaller than 30 Myr), guaranteeing that these associations are still tracing the velocities of the molecular clouds that served as their birthplaces." | Methods, Stellar Cluster Catalog |
| `stat_co`: the best-fit model explains the ¹²CO line-of-sight velocities (a model–data agreement) | STAT | stated: "We show in Extended Data Figure 3a that our model explains the 12CO observations" | Methods, Line-of-sight Gas Velocities |
| `mod_transfer`: tracers + CO match ⇒ clouds and clusters are one kinematically coherent structure | MOD | stated: "As a consequence, we can transfer our results from the full phase-space study of the stars to all components of the Radcliffe Wave, including the gas" | Methods, Line-of-sight Gas Velocities |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| The vertical pattern of the clusters is built in by the selection | `mod_xy`, `gap_born` | yes: selection on the x–y plane only, ±5 Wave radii from the dust model |
| The clusters were not born in the Wave but lie in front of or behind it, or are unrelated young groups aligned by chance | `obs_coloc`, `gap_born` | partly: co-location in 3D is shown, but K24 only "suggests" a common origin and gives no test of it (ages versus position, chemistry, chance alignment) |
| Clusters up to 30 Myr old have drifted away from their gas, so their v_z is not the gas's v_z | `mod_age`, `stat_co` | partly: the age cut is said to "guarantee" tracing, and the CO check is graphical and probes v_z only through the line of sight |
| Perseus, Taurus and Lacerta do not move with the Wave | (not encoded: they are removed) | yes: Lacerta excluded beforehand; all Perseus and Taurus clusters come out as outliers and are attributed to feedback bubbles |

**Inference (Lean excerpt).**

```lean
have c : v.Coherent :=
  p .mod_transfer (p .mod_age (p .gap_born (p .obs_coloc) (p .mod_xy))) (p .stat_co)
```

**Critique.** Each link is plausible, but three are qualitative. The common origin is only
suggested by K24 ("suggesting that the clusters' stars were born in the molecular clouds"), so it
enters as a gap (`gap_born`): co-location with no height cut makes it likely, but no test of it is
given. "Guaranteeing" is strong: 30 Myr is
about a third of the vertical period (~90 Myr), enough for stars and gas to separate if the gas is
pushed by feedback (which is exactly what K24 invokes for Perseus and Taurus). The CO check is the
only test with the gas, and it is a figure without a goodness-of-fit number; because each line of
sight mixes v_x, v_y and v_z, agreement in v_LSR does not by itself show that the gas has the
clusters' v_z. K24 also states that fits to clouds only, clusters only and both are consistent
(Methods, "confirming that the Radcliffe Wave is a spatially and kinematically coherent
structure"); we do not encode this as a second route, because the clouds-only fit has no
velocities.

#### 2.2 Stage B · The model and the fit

*Overview.* If only gravity acts and the vertical potential is known, each piece of the Wave
oscillates with a known frequency ω(s); for a travelling wave the spatial shape then fixes the
vertical velocities (amplitude ζ(s)ω(s), a quarter wavelength out of step with z), with no free
velocity amplitude. The potential's three parameters are not fitted to the Wave at this point:
they come from a χ² fit of eq. 1 to an existing Milky Way model. The B = 1 fit to the clusters'
(x, y, z, v_z/ω₀) together with the clouds (Figure 1; Extended Data Table 2, column (6)) is
"excellent", with the 90° offset.

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `mod_grav`: only gravity acts on the Wave vertically | MOD | stated: "We therefore model the forces acting on the Wave solely by gravity." | Methods (density contrast 10⁴ with the surrounding medium) |
| `mod_potpar`: the adopted ω₀ = 74, r₀ = 3.7, μ₀ = 1.3 are chi-square fitted to an existing Milky Way model | MOD | stated: "These parameters are adopted by comparing equation (1) with an existing model of the Galactic potential including its updated parameters" | Methods; Allen & Santillán 1991 with the parameters of Irrgang et al. 2013 (arXiv:1211.4353) |
| `mod_pot`: the vertical potential is the anharmonic oscillator of eq. 1 with those parameters | MOD | stated: "Since the Radcliffe Wave's amplitude is on the order of the Galaxy's vertical scale height, the vertical gravitational potential Φ resulting in this acceleration can be represented by an anharmonic oscillator." | Methods, eq. 1 |
| `mod_stationary`: the potential is stationary | MOD | stated: "Note that, consistent with the literature, we treat the underlying Gravitational potential as stationary." | Methods |
| `mod_shape`: gravity + known stationary potential ⇒ for a travelling wave the shape fixes v_z | MOD | stated: "For a traveling wave, the wave's spatial shape fully determines vertical velocities, assuming a gravitational potential" | main text p. 2 |
| `stat_twfit`: the travelling-wave (B = 1) model fits z and v_z, with a 90° offset | STAT | stated: "While a traveling wave provides an excellent fit to the observations, with a 90° phase offset between position (z) and velocity (vz), as evident in Figure 1" | main text p. 2; Figure 1 is the B = 1 fit (Extended Data Table 2, column (6)) |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| Non-gravitational forcing (feedback bubbles, gas pressure, magnetic fields) drives the vertical motions | `mod_grav` | partly: density contrast 10⁴; the feedback-dominated Perseus and Taurus clusters are outliers |
| A non-stationary potential (warp, tilt, radial vertical waves near the Sun) | `mod_stationary`, `mod_pot` | yes: tilt fitted (no effect), warp on longer timescales, radial waves argued negligible, three potentials tried |
| A different Milky Way model gives a different ω(s) | `mod_potpar` | yes: McMillan 2017 and MWPotential2014 reportedly have no effect; stage E frees the parameters |

**Inference (Lean excerpt).**

```lean
have z : v.VzFixed :=
  p .mod_shape (p .mod_grav) (p .mod_pot (p .mod_potpar)) (p .mod_stationary)
```

**Critique.** This stage only sets up the test; its conclusion comes in stage D. Note that the fit
quality enters as an atom: K24 calls the fit "excellent" and shows it in Figure 1, but gives no
goodness-of-fit statistic for the v_z component on its own.

#### 2.3 Stage C · Travelling, not standing; B = 1 adopted

*Overview.* K24 lets the data choose between travelling (B = 1), standing (B = 0.5) and mixtures,
fitting the clusters with B free (Extended Data Table 2, column (5)). One argument excludes a
standing wave: in a standing wave the cluster phases φ_k = arctan(z_k ω_k / v_z,k) would be almost
constant along the Wave (in the noiseless model they vary by at most ~0.03π), but they sweep the
whole range −π/2 to π/2. The mixture fit adds that B = 0.84 (+0.07/−0.06), closer to 1 than to
0.5; K24 reads this as the data favouring a travelling wave ("indicates"), and the main text states
the result categorically ("we find that a traveling wave is strongly preferred"). A fit with B fixed to 1 is then "an equivalently good fit"
(ΔlnZ ≈ 1), and B = 1 is adopted for everything that follows, including Figure 1.

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `stat_phase`: the observed phases φ_k sweep −π/2 to π/2 | STAT | stated: "In contrast, we find that the phases φk change over the whole range of -π/2 to π/2, such that B = 0.5 is inconsistent with the data." | Methods (wave model) |
| `mod_standing`: standing wave + spread not due to noise ⇒ observed phases do not sweep | MOD | stated: "From equations (4) and (5) we conclude that the phases φk should be roughly constant" | Methods (the preceding sentence assumes B = 0.5) |
| `gap_phase_noise`: the observed spread exceeds what errors and the 47 pc scatter would give for a B = 0.5 wave | GAP | reconstructed | — |
| `stat_b`: best-fit B = 0.84 (encoded as 84 hundredths) | STAT | stated: "We find a best fit value for B = 0.84." | Methods; Extended Data Table 2 column (5), clusters with B free |
| `gap_vz`: the cluster z–v_z pattern (and so the phases, the B posterior and the Figure 1 fit) is a property of the Wave, not of the sample, its radial-velocity coverage, the solar-motion zero point or the outlier and weighting choices | GAP | reconstructed | Zhu et al. 2024, arXiv:2402.15346; Bobylev et al. 2025, arXiv:2503.21019 |
| `mod_prefer`: B above 0.75 (our reading of "closer to 1") + standing excluded (+ robust v_z) ⇒ travelling preferred over standing | MOD | stated: "When fitting a mixture model that allows for superpositions of a traveling and a standing wave, we find that a traveling wave is strongly preferred over a standing wave (see Methods)." | main text p. 2 |
| `stat_bequiv`: B = 1 and B free fit equivalently well | STAT | stated: "Thus, both models are an equivalently good fit to the data, while the realization with fixed B = 1 is slightly preferred." | Methods (ΔlnZ = ln Z₂ − ln Z₁ ≈ 1) |
| `mod_b1`: travelling preferred + equivalent fits ⇒ B = 1 can be adopted | MOD | stated: "We therefore conclude that the Wave's motion is of first order consistent with a traveling wave, implying that we can set B = 1 in all further performed calculations" | Methods |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| A standing wave (fixed nodes, z and v_z in phase) | `stat_phase` + `mod_standing` + `gap_phase_noise` | yes, by the phase argument; no statistic is given for the spread |
| A standing wave whose phases look spread because, near its nodes, z and v_z are both close to zero and the phase is set by the 47 pc scatter and the v_z errors | `gap_phase_noise` | no |
| The phase spread and B = 0.84 are products of the cluster sample (outlier model, kernel weights, radial-velocity coverage, solar-motion zero point) | `gap_vz` | partly: Sun's height, tilt, potentials and a second cluster catalogue checked |
| An intermediate mixture (0.5 < B < 1) | not excluded by the encoded claim ("preferred over a standing wave") | partly: B = 1 is adopted because B = 1 and B free fit "equivalently" |

**Inference (Lean excerpt).**

```lean
have hb : v.b_x100 = 84 := p .stat_b
have ns : ¬ v.Standing := fun s => p .mod_standing s (p .gap_phase_noise) (p .stat_phase)  -- GAP
have pt : v.PreferTW := p .mod_prefer (by omega) ns (p .gap_vz)                                     -- GAP
have b1 : v.B1OK := p .mod_b1 pt (p .stat_bequiv)
```

**Critique.** Both routes use the same cluster velocities as the fit. The phases φ_k are computed
from the same z_k and v_z,k, with the same outlier model and weights, and B = 0.84 comes from the
same likelihood; so whatever threatens the v_z pattern (`gap_vz`) threatens this stage too. The
phase argument has a second weakness: the sentence K24 relies on ("the phases φk should be roughly
constant") is a property of the noiseless model, while the test is applied to observed phases.
Near a standing wave's nodes both z and v_z tend to zero, so the arctan of their ratio there is set
by the 47 pc scatter and the v_z errors and can take any value; some spread is therefore expected
even for B = 0.5, and K24 gives no statistic (no simulation of the expected spread) to show that
the observed spread exceeds it (`gap_phase_noise`). The word "strongly" has no quantitative
support in K24: the only evidence ratio reported for B, ΔlnZ ≈ 1, compares B = 1 with B free (not
travelling with standing) and is called "equivalently good"; the posterior interval of B lies well
above 0.5, but the prior is truncated at 1, so the posterior is bounded and its separation from 0.5
is not a significance. The B threshold 0.75 is our reading of "closer to 1"; any threshold between
0.5 and 0.84 gives the same result. The B = 1 step uses an evidence ratio whose printed sign
disagrees with the stated preference (part 1.4); either way the ratio is ≈ 1, so "equivalently
good" holds.

#### 2.4 Stage D · The Wave oscillates

*Overview.* With B = 1 adopted, the excellent fit with v_z fixed by the shape (stages B, C), on
tracers that are the Wave's (stage A), is read as oscillation. The main text hedges ("The fit shown
as a solid black line in Figure 1 ... indicates that the Radcliffe Wave oscillates through the
Galactic plane like a traveling wave"); the Methods state it categorically ("In the case of the
z-component, we find that the Radcliffe Wave oscillates like a traveling wave driven by the Milky
Way's gravitational acceleration"), and that is the sentence we quote.

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `gap_vz` (as in stage C) | GAP | reconstructed | Zhu et al. 2024; Bobylev et al. 2025 |
| `gap_shear`: one coherent travelling wave (one phase law Λ(s), one solid-body drift) adequately describes the Wave over the time its tracers span | GAP | reconstructed | Li, Zhou & Chen 2024, arXiv:2410.14603 |
| `mod_osc`: coherent tracers + v_z fixed by the shape + good B = 1 fit + B = 1 adopted (+ the two gaps) ⇒ the Wave oscillates like a travelling wave | MOD | stated: "In the case of the z-component, we find that the Radcliffe Wave oscillates like a traveling wave driven by the Milky Way's gravitational acceleration." | Methods, Full Spatial and Kinematic Model (main text p. 2: the fit "indicates" it) |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| A static corrugation (a frozen ripple with no vertical motion) | `stat_twfit` (v_z pattern of ~14 km/s with the predicted amplitude) | implicitly: Fig. 1b shows the v_z wave; also, under `mod_grav`, a structure 220 pc from the plane with no support cannot stay at rest |
| A standing wave, or a mixture, rather than a travelling wave | `mod_b1` (via `mod_osc`'s antecedent B = 1 adopted) | yes (stage C) |
| Vertical velocities not synchronous with the positions (v_z oscillations "not synchronous with the vertical coordinate", a dipole-like gradient along the Wave; different wavelengths in z and v_z) | `gap_vz` | no (Zhu et al. 2024 appeared on arXiv the same week as K24; Bobylev et al. 2025 later) |
| The 90° relation is driven by the outlier model (all Perseus and Taurus dropped, soft cut at √3σ per component), the kernel weights, a few Orion and Cepheus clusters, or the solar-motion zero point (w☉ = 7.8 km/s, the standard solar motion of Kerr & Lynden-Bell 1986 as cited by K24; Schönrich et al. 2010 give 7.25 km/s; subtracted from every v_z) | `gap_vz` | partly: Sun's height, tilt, potentials and a second cluster catalogue checked; outlier threshold, weights and solar motion not varied |
| Galactic shear stretches the Wave (to almost twice its length in ~45 Myr, half an oscillation cycle), so a single phase law and a solid-body drift are an oversimplification | `gap_shear` | partly: K24 notes cloud destruction and phase mixing on "several tens of Myr" and that its time-independent approximation reaches the noise after about 40 Myr, but fits a single coherent wave |

**Inference (Lean excerpt).**

```lean
have o : v.Oscillating :=
  p .mod_osc c z (p .stat_twfit) b1 (p .gap_vz) (p .gap_shear)                              -- two GAPs
```

**Critique.** The empirical content of "oscillating" is narrower than it sounds. Under
`mod_grav`, any parcel 220 pc from the plane must be moving vertically; what the data add is that
the measured v_z have the size (~14 km/s) and the quarter-wavelength shift that the known potential
predicts. That is a real test, because in the travelling-wave fit the velocity amplitude is not
free. But "like a travelling wave" rests on stage C, and two further things are not shown in K24.
(i) The v_z pattern must belong to the Wave rather than to the sample: the cluster v_z rest on Gaia
proper motions plus radial velocities that are sparse for some clusters (K24 removes clusters above
50 km/s as anomalies), on the adopted solar motion, and on a soft outlier model that removes whole
regions. Zhu et al. 2024, using APOGEE-2 stars and, separately, cloud radial velocities with YSO
proper motions, find v_z oscillations "not synchronous with the vertical coordinate" (a dipole-like
gradient of ~5 km s⁻¹ kpc⁻¹), and Bobylev et al. 2025 find different wavelengths in z and v_z.
(ii) A single coherent travelling wave is an idealisation: K24 itself says the Wave is likely
affected by phase mixing on several tens of Myr, and Li et al. 2024 argue that shear makes a
solid-body description an oversimplification over half a period. The snapshot fit can still show
that pieces of the Wave move up and down as gravity predicts; what (ii) threatens is the
"travelling wave" reading, the phase velocities and the solid-body drift. Both points are later
literature or our analysis, so they are `GAP`s.

#### 2.5 Stage E · Weighing the disc with the Wave

*Overview.* With B = 1, K24 frees the three potential parameters (ω₀, μ₀, r₀) and fits them to the
Wave (Extended Data Table 2, column (7)): ω₀ = 68 (+8/−7) km s⁻¹ kpc⁻¹, consistent with the adopted
74. The isothermal sheet turns ω₀ into a midplane density, ρ₀ = ω₀²/(4πG) = 0.085 M☉ pc⁻³;
subtracting the baryons gives a dark-matter density consistent with zero; the same potential gives
the Sun's vertical period, 95 Myr.

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `stat_omega`: with the potential freed, ω₀ = 68 (+8/−7), μ₀ = 1.4, r₀ = 3.6 kpc | STAT | stated: "We find a median value and 1σ errors (computed using the 16th, 50th and 84th percentiles of the samples) of ω0 = 68 +8 -7 km s-1 kpc-1" | Methods; Extended Data Table 2 column (7); superscripts flattened |
| `mod_sheet`: ρ₀ = ω₀²/(4πG) (isothermal sheet) | MOD | stated: "Following the vertical density model of an isothermal sheet based on a Maxwellian vertical velocity distribution, we calculate the parameters defining the Galactic mass distribution" | Methods |
| `gap_prior`: the ω₀ posterior (and so ρ₀, the dark-matter density and the Sun's period, central values and errors) is set by the Wave's data, not by priors based on initial fits | GAP | reconstructed | — |
| `mod_weigh`: oscillating + fitted ω₀ + isothermal sheet (+ the gap) ⇒ the Wave measures the local potential and the Sun's period | MOD | stated: "By treating the Radcliffe Wave as a coherently oscillating structure, we can derive its motion independently of the local Galactic mass distribution, and directly measure local properties of the Galactic potential as well as the Sun's vertical oscillation period." | Abstract |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| The fitted ω₀ reflects the prior, not the Wave | `gap_prior` | partly: K24 says it fits "without prior knowledge about the vertical gravitational potential", but its priors are "based on initial fits" |
| The data cannot distinguish the adopted potential from the fitted one | (shapes the error bars; not a separate premise) | stated: fixed and free potentials are "an equivalently good fit" (ΔlnZ ≈ 1) |
| The Wave's vertical motion is not a free oscillation (stage D fails) | `mod_weigh` needs `Oscillating` | — (inherits the gaps of stages C and D) |

**Inference (Lean excerpt).**

```lean
have w : v.Weighs := p .mod_weigh o (p .stat_omega) (p .mod_sheet) (p .gap_prior)         -- GAP
exact ⟨o, pt, w⟩
```

**Critique.** The measurement rests on stages A–D (it uses `Oscillating`), so all their gaps carry
over. Its own weak point is the prior. The ω₀ prior, ln(ω₀/(km s⁻¹ pc⁻¹)) ~ N(−2.4, 0.17), is
centred near 91 km s⁻¹ kpc⁻¹ with a width of ~17%, while the posterior has a width of ~11% and sits
~1.7σ (in ln) below the prior centre: the data pull ω₀ down and the prior pulls it up, so both the
central value and the error bar are a compromise, not the data's alone. The priors were set "based
on initial fits", presumably to the same data, which would count the data twice and make the
posteriors too narrow (r₀ is entirely prior-driven: posterior width = prior width). The fixed (74)
and free (68) potentials fit "equivalently" (ΔlnZ ≈ 1), so the data do not distinguish a 10%
change in ω₀; this is consistent with the quoted ±11%, but it means the Wave confirms the standard
potential rather than replacing it. The dark-matter density (0.001 +0.024/−0.021 M☉ pc⁻³) is a
difference of two nearly equal numbers (0.085 total and 0.084 baryons) and is consistent with both
zero and the conventional ~0.013; the Sun's period (95 Myr) is computed in the same fitted potential
and inherits its prior.

#### 2.6 The radial drift and the Local Bubble (discussed, not encoded)

K24 fits a solid-body in-plane velocity after removing Galactic rotation: v_x,plane = −3.9
(+2.6/−2.7) and v_y,plane = 3.1 (+2.7/−2.6) km/s, i.e. ~5 km/s radially away from the Galactic
Centre ("we find evidence that the Radcliffe Wave is drifting radially outward from the Galactic
Center with a velocity of 5 km s-1"). Each component is only ~1.2–1.5σ from zero, so "evidence" is
modest; the drift assumes the solid-body motion that `gap_shear` questions; and the link to the
Upper Centaurus Lupus and Lower Centaurus Crux clusters is a direction, not a traceback (K24: an
exact traceback "is beyond the scope of this work"). Bobylev et al. 2025 find ~10 km/s. Since one
file has one conclusion and this claim does not feed the oscillation, it is not encoded; part 3
can test it.

#### 2.7 What the Lean check found

1. **Headline: `explicit_insufficient`, with five gaps.** No premise is `[implied]`: everything
   that is not a gap is stated by K24 (the potential parameters enter as a stated `MOD` premise: K24's own adoption step),
   so `stated_insufficient` and `explicit_insufficient` rest on the same countermodel. The gaps
   are: the co-located clusters were born in the Wave, which K24 only suggests (`gap_born`); the
   z–v_z pattern belongs to the Wave, not to the cluster sample, its outlier treatment and
   its solar-motion zero point (`gap_vz`; questioned by Zhu et al. 2024, who find v_z oscillations
   not synchronous with the vertical coordinate, and by Bobylev et al. 2025); the observed phase
   spread exceeds what noise gives for a standing wave (`gap_phase_noise`); one coherent travelling
   wave is an adequate description despite shear (`gap_shear`; questioned by Li et al. 2024); and
   the potential fit is data-driven rather than prior-driven (`gap_prior`).
2. **Where the gaps sit: every part of the conclusion depends on gaps.** (1) and (3) need
   `gap_born` through stage A. (2), travelling rather
   than standing, needs `gap_phase_noise` and `gap_vz`, because both of its inputs (the phase
   spread and the B posterior) use the same cluster velocities and the same fit. (1), oscillation,
   comes after (2) — the Figure 1 fit is the B = 1 realisation, adopted only after the mixture
   fit — so it inherits those two gaps and adds `gap_shear`. (3), weighing the disc, uses the
   oscillation and adds `gap_prior`. "Strongly preferred" has no quantitative support in K24 (the
   only evidence ratio is ΔlnZ ≈ 1 for B = 1 against B free; the B posterior is bounded by the prior
   at 1).
3. **What each gap affects.** `gap_vz` reaches all three parts. `gap_phase_noise` concerns the one
   route that excludes a standing wave. `gap_shear` affects the travelling-wave reading and the
   drift more than the local up-and-down motion. `gap_prior` affects both the central values of
   ω₀, ρ₀, the dark-matter density and the Sun's period (the prior pulls ω₀ up) and their error
   bars.
4. **All 26 premises are needed** in this encoding; none is redundant (each sits on a single chain;
   K24's second route to coherence, the consistency of the clouds-only, clusters-only and joint
   fits, is not encoded; B = 0.84 enters as an antecedent of the stated preference, not as a second
   route excluding a standing wave).
5. **Consistency** (`consistent`) has a little weight here: `mod_standing` is negative, and the
   model needs the Wave not to be standing.
6. **How the encoding departs from the quotes.** Five stated inference rules (`mod_transfer`,
   `mod_prefer`, `mod_b1`, `mod_osc`, `mod_weigh`) and `mod_shape`, `mod_pot`, `mod_standing` carry
   extra antecedents (gaps or earlier steps), so they are weaker than their quotes; `mod_standing`
   also applies a statement about the noiseless model to observed phases, which is why it carries
   `gap_phase_noise`. No hedged sentence is encoded as a stated implication: the hedged birth step
   is a gap (`gap_born`), and for the oscillation and the travelling-wave preference we quote K24's
   categorical sentences ("we find that ..."), with the hedged versions noted. The threshold
   "B closer to 1" is our reading (above 0.75; any threshold between 0.5 and 0.84 gives the same result), used only as an antecedent.
7. **Limits.** Lean checks the logical structure under our encoding, not the dynamics or the
   statistics inside each premise; fit quality ("excellent fit") and the CO agreement are figures
   in K24 and enter as atoms.

### Part 3 · What astrolab can test or explore

This part was written before any fit (2026-11-21). It is the source of the study's pre-registration
(README sections 1–4), which fixes the exact thresholds.

When we wrote it we had looked at two things: the paper (arXiv v1, including the Methods), and the
column names, row counts and value ranges of the two public tables, read through the guarded fetch.
- The cluster table has 125 rows. Its columns are `name`, `reference`, `x, y, z, vx, vy, vz` with
  their errors (`sigma…`), `age` (in Myr, integers 0–28) and an `inlier` flag (89 inliers, 36
  outliers).
- The CO table has 79 clouds. Its columns are `x, y, z` with their spreads, `l, b, d`, and the ¹²CO
  velocity `vr` with its 16th and 84th percentiles.

No model was fitted.

**Data and cost.**
- *Data.* Two tables of 10,888 and 5,286 bytes (Harvard Dataverse, CC0), fetched with `ctx.http`.
  Nothing else is fetched.
- *Sampler.* The fits use emcee and a maximum-likelihood optimiser, both already installed. K24 used
  dynesty with 1000 live points; we do not install it.
- *Cost.* One likelihood evaluation finds the closest point on the model curve for each of about
  200 objects. On a grid of about 2000 points along s, that is a vectorised operation of about
  4 × 10⁵ distances.
  - The tests below need roughly 20–40 fits, because the robustness variants of T6 each refit two
    or three models, plus the mocks of T3 and T4.
  - We expect each fit to take minutes, and the whole run a few hours on one core.
  - The time will be measured on a short run and stated, with the exact number of fits and mocks,
    in the pre-registration.
- *Scheduling.* The run waits until no other study is running.

**What we can and cannot reproduce exactly.**
- *Not given by K24, so fixed by us:* the kernel bandwidth (K24 says only "a few percent of the
  total length of the Wave"), and how the parameters of the in-plane curve map to s. The
  pre-registration fixes both choices, and the robustness checks vary them.
- *Taken from K24:* the likelihood of eqs. 10–13, namely
  - the 4-vector (x, y, z, v_z/ω₀) for clusters and the 3-vector for clouds;
  - kernel weights that sum to the number of objects (K24: the weights "are set to sum to the number
    of" clouds, and likewise of clusters);
  - the outlier function C(x) = (Σₙ tanh(xₙ²))^½;
  - the common scatter σ = 47 pc on all components;
  - the priors of Extended Data Table 1.
- *Two features of the model that the tests must respect:*
  - With B = 1, ω₀t enters only through ω₀t + φ, so it is fixed at 0, as K24 does.
  - With B = 0.5, z = ζ sin(2πΛ + φ) cos ω₀t and v_z = −ζω sin(2πΛ + φ) sin ω₀t, so ω₀t sets the
    z and v_z amplitudes separately. A standing wave therefore has one more effective parameter
    than a travelling wave, and the two cannot be compared as if they had equal parameter counts.
  - In general, (z, v_z/ω) is a 2 × 2 matrix times (sin θ, cos θ), with θ = 2πΛ + φ, and its
    determinant is ζ²(2B − 1). Its sign, the direction of travel, cannot be changed by ζ, φ or ω₀t,
    so B and 1 − B are different waves. Locally, the standing waves (rank-1 matrices) remove one parameter from the B-free model and the travelling waves (a scale times a rotation) remove two, which sets the degrees of freedom in T3.

| Stage (Part 2) | Premise or gap | Test or exploration | How | Data | Outcome labels (thresholds fixed in the pre-registration) |
|---|---|---|---|---|---|
| B, D | `stat_twfit` | **T1 · Reproduce the fit.** Clusters only (column (4)), and clouds plus clusters (column (6)), with B = 1, ω₀t = 0, and K24's likelihood and priors | Fit with emcee. Compare medians and 16–84% intervals with Extended Data Table 2, and our inlier set with the table's flag | 16 KB | reproduced / partly reproduced / not reproduced, by how many of A, p, δ, s₀, γ, φ fall within K24's 1σ |
| C | `stat_b` | **T2 · B free** (column (5)), ω₀t free | As T1, with B ~ U(0, 1) as in K24, summarised on [0, 1] without folding. B and 1 − B are waves travelling in opposite directions, and the data can tell them apart (see above) | same | B interval compared with 0.84 (+0.07/−0.06); posterior mass above 0.95, and P(B < 0.5) as a check on the direction of travel |
| C | `mod_prefer`, "strongly" | **T3 · Travelling against standing, as nested models.** Inside the B-free model of T2, profile the likelihood at B = 0.5 and at B = 1, and compare each with the maximum over B | Maximum-likelihood fits. The priors' support is used as bounds, not their shape, except that ω₀t is treated as periodic (not clipped). MAP values are reported alongside. B = 0.5 is an interior point where ω₀t stays identified, so 2ΔlnL is referred to χ² with one degree of freedom. At B = 1, ω₀t merges into φ, so the B = 1 model removes two parameters and is referred to χ² with two degrees of freedom. Both references are checked with parametric-bootstrap mocks, from the B = 0.5 fit and from the B = 1 fit (at least 100 each, number fixed by the measured run time). The inlier sets of all fits are reported with their overlap | same | standing excluded strongly / excluded / not excluded; and, separately, pure travelling (B = 1) disfavoured / not disfavoured |
| C | `gap_phase_noise` | **T4 · Is the phase spread more than noise?** | Mocks: at least 1000 standing waves from the B = 0.5 fit of T3. Mock clusters start at the observed clusters' positions on the model. Noise: the 47 pc scatter on all four components (x, y, z and v_z/ω₀, i.e. about 3.5 km/s in v_z) plus each cluster's measurement errors; a variant instead resamples the B = 0.5 fit's own residuals. Each mock cluster's closest point (s_k, and so ω_k) is recomputed on the B = 0.5 fit's curve (also for the power mocks, the same procedure as for the data), but the global parameters are not refitted. Because the observed R uses parameters fitted to the data (the B = 0.5 fit tunes ω₀t to line the phases up) while the mocks are not refitted, the test is conservative against excluding the standing wave. Clusters: all inliers of the B = 0.5 fit, including those near nodes. Statistic: φ_k = arctan(z_k ω_k / v_z,k) has period π, so we use the circular statistic R = \|mean of e^(2iφ_k)\|. A standing wave has a constant φ_k and R near 1, and spread phases give a low R. p is the fraction of standing mocks with R at or below the observed value. Power: the same statistic on mocks from the B = 1 fit and from the B-free best fit | same | standing excluded by the phases / not excluded / undetermined (when the power at the chosen threshold is below the value fixed in the pre-registration) |
| C, D | `gap_vz` (the part these data can reach) | **T5 · A look at z and v_z that does not assume their relation.** Take the baseline and Λ(s) from the clouds-only fit (column (3), positions only, no velocities). Give each cluster s by projection onto that baseline in x–y. Clusters whose closest point is an end of the baseline are dropped and counted. The cluster set is all 125 clusters, with inlier choices varied in T6, so no velocity enters the selection. Fit z(s) and v_z(s) separately, each with its own amplitude, its own phase and its own wavelength scale k (Λ → kΛ) | Bootstrap over clusters, drawing Λ from the clouds-only posterior inside the bootstrap. The phase difference is evaluated at a stated reference s (the weighted mean s of the clusters). It is reported together with the amplitude ratio A_v/(ω A_z), with ω evaluated at the same reference s. A 90° offset alone does not make a travelling wave (any B gives 90° when ω₀t = 0); a ratio near 1 is also needed. The sign of the offset (+90° or −90°) gives the direction of travel | same | 90° offset with ratio near 1: supported (the phase-difference interval contains 90° and excludes 0° and 180°, and the ratio interval lies inside a band around 1 fixed in the pre-registration, e.g. [0.7, 1.4]) / not supported (the phase interval excludes 90°, or the ratio interval excludes 1) / undetermined (otherwise: the data are too noisy to tell). Wavelengths: consistent (the k_z/k_vz interval inside a pre-registered band around 1) / different (it excludes 1; Bobylev et al. 2025 report different wavelengths) / undetermined (otherwise) |
| C, D | `gap_vz` | **T6 · Robustness of T3, T4 and T5** | Variants: outlier rule (K24's √3σ per component, 3σ, no outlier model); no kernel weights, and two other bandwidths; w☉ = 7.8 against 7.25 km/s; Orion left out; each source catalogue (`reference`) left out in turn; only clusters with σ(v_z) below the median | same | robust (the T3, T4 and T5 labels are unchanged in every variant) / fragile (naming the variants that change them) |
| A | `stat_co` | **T7 · How much does the CO check say about v_z?** | Project the T1 model onto each cloud's line of sight (eq. 14) and compare with `vr`. The in-plane velocity comes from the clusters' v_x, v_y after removing Galactic rotation with a flat rotation curve (Oort constants). Errors come from the 16/84 columns plus an intrinsic dispersion, fitted separately for each version. Versions: the T1 model, v_z set to 0, and the B = 0.5 fit. Expected sensitivity: \|sin b\| is mostly below 0.2, so v_z contributes at most about 3 km/s to v_LSR, and "does not distinguish" is a likely outcome | 5 KB | CO prefers the travelling wave / CO does not distinguish (Δχ² between the versions) |
| E | `gap_prior` | **T8 · Is the potential set by the data?** Free ω₀, μ₀ and r₀ (column (7)), once with K24's priors and once with broad uniform priors: ω₀ 30–150 km s⁻¹ kpc⁻¹, μ₀ 0.3–3 kpc⁻¹, r₀ 1–10 kpc | Compare the ω₀ posteriors. Derive ρ₀ = ω₀²/(4πG) and the Sun's vertical period. The v_z/ω₀ divisor of the 4-vector follows the fitted ω₀ (our reading of K24); a variant fixes it at 74 | 16 KB | data-driven (posterior narrower than the prior and insensitive to it) / prior-driven / partly |

**Explorations, with no verdict.** These are the entries for chat exploration (README section 8).

- *Age and birth in the Wave* (`gap_born`, `mod_age`). Split the clusters at 10 and 20 Myr. Do
  older clusters scatter more about the T1 model in z or v_z? Separation from the gas would predict
  a scatter that grows with age. This cannot prove or disprove a common origin.
- *One coherent wave?* (`gap_shear`). Fit separate phase laws to the CMa–Orion half and the
  Cepheus–Cygnus half, and compare them with a single law. Shear acts over tens of Myr and the data
  are one snapshot, so this shows only whether one Λ(s) is adequate now, not whether it was in the
  past.
- *Radial drift* (Part 2.6). Reproduce the in-plane solid-body velocity after removing Galactic
  rotation. We would use a simple flat rotation curve with Oort constants rather than K24's
  potential, and see how the result depends on the rotation model.

**What this study cannot test.**
- *Independent velocity data.* Zhu et al. 2024 used APOGEE-2 stars, and cloud radial velocities
  combined with YSO proper motions. Bobylev et al. 2025 used a different cluster selection.
  Reaching these data would need new server-side queries, so this is left as an open question.
- *Outside this study's scope:* the physics of the Wave's origin; cloud destruction and phase
  mixing over tens of Myr; and the Local Bubble traceback.

### Glossary

| Term | Meaning |
|---|---|
| Radcliffe Wave | a ~2.7-kpc chain of dense gas clouds near the Sun, shaped like a damped sine wave (Alves et al. 2020) |
| travelling wave | a wave whose crests move; position and velocity patterns are 90° out of phase |
| standing wave | a wave with fixed nodes; position and velocity have the same spatial pattern |
| B | K24's mixing parameter: 1 (or 0) = travelling wave, 0.5 = standing wave |
| anharmonic oscillator | an oscillator whose frequency depends on amplitude (here: slower for larger excursions) |
| phase velocity | the distance a crest moves per unit time: wavelength divided by the temporal period |
| LSR | local standard of rest: the frame of a circular orbit at the Sun's position |
| ¹²CO | carbon monoxide, whose 2.6-mm line traces molecular gas and its line-of-sight velocity |
| Bayes factor, ΔlnZ | the Bayes factor is the ratio of the evidences of two models; ΔlnZ is its natural log; |ΔlnZ| ≈ 1 is a modest evidence difference, its sign (set by the convention) giving the preferred model |
| midplane density ρ₀ | total mass density (stars, gas, dark matter) in the Galactic plane near the Sun |

### Changelog

Newest first.

- 2026-11-21: part 3 drafted (eight tests T1–T8 and three explorations; the two public tables' columns and row counts read, no fit; gate-1 review: T3 recast as nested profile-likelihood tests, because with ω₀t free a standing wave has one more effective parameter; T4 noise on all four components, a circular statistic on 2φ_k and a power check; T5 takes Λ(s) from the clouds-only fit and frees each wavelength); round 2: B is not folded (B and 1 − B travel in opposite directions), B = 1 is referred to χ² with two degrees of freedom (ω₀t merges into φ there) and bootstrapped, T4 recomputes each mock's closest point, T5 reports the amplitude ratio and uses no velocity in its cluster set; round 3: T5 labels get an undetermined band, so a wide interval cannot count as support; w☉ = 7.8 km/s attributed to Kerr & Lynden-Bell 1986 as cited by K24 (was Schönrich et al. 2010).
- 2026-11-21: part 2 gate-2 review: no hedged sentence is encoded as a stated implication any more; the clusters' birth in the Wave (K24: "suggesting") is a new gap, `gap_born`; the oscillation step quotes the Methods' categorical "we find that"; the "B closer to 1 indicates" premise is folded into the stated preference; 26 premises, five gaps.
- 2026-11-21: part 2 gate-1 review: travelling versus standing now also depends on gaps (the same cluster v_z, and a phase spread that may be noise near a standing wave's nodes: new `gap_phase_noise`); the oscillation claim now comes after the B = 1 adoption (Figure 1 is the B = 1 fit); potential parameters as a `LIT` premise, the x–y selection as a premise, CO agreement tagged `STAT`; 27 premises, four gaps; Chinese term 银盘中平面密度 (midplane density).
- 2026-11-21: part 2 drafted: four stages, 24 premises checked in Lean 4; `explicit_insufficient` with three gaps (the z–v_z pattern versus Zhu et al. 2024; one coherent wave versus shear, Li et al. 2024; prior-driven potential fit); travelling versus standing closes from stated premises.
- 2026-11-21: gate-1 review: the B posterior is no longer read as evidence against a pure travelling wave (prior truncated at 1); outlier rule, priors, axes, the Sun's period estimate, the Orion outlier fraction and Zhu et al.'s data routes corrected.
- 2026-11-21: part 1 drafted (parts 2 and 3 to follow).

### Sources

- Konietzka et al. 2024, Nature 628, 62–65, doi:10.1038/s41586-024-07127-3, arXiv:2402.12596 (the
  paper studied; read in the arXiv v1 full text) [V].
- Data: Harvard Dataverse doi:10.7910/DVN/XSCB9N (clusters) and doi:10.7910/DVN/Q7F4PC (¹²CO)
  [V metadata only].
- Alves et al. 2020, Nature 578, 237, arXiv:2001.08748 [V abstract].
- Zhu et al. 2024, ApJ 971, 167, arXiv:2402.15346 [V abstract; S volume].
- Li, Zhou & Chen 2024, arXiv:2410.14603 [V abstract].
- Bobylev, Ikhsanov & Bajkova 2025, Astrophys. Bull. 80(2), arXiv:2503.21019 [V abstract].
- McKee, Parravano & Hollenbach 2015, ApJ 814, 13 (local baryons; as cited by K24).

---

## 中文

### 第一部分 · 科普详解

以下数字均读自 arXiv 版本（arXiv:2402.12596v1，即录用稿，含正文、方法（Methods）与扩展数据（Extended Data））；我们没有与 Nature 排印版逐行对照。下文"K24"指这篇论文。

#### 1.1 问题与意义

太阳位于由恒星与气体组成的薄盘中。离我们不远处（最近的部分约 250–300 秒差距（parsec, pc）；1 pc ≈ 3.26 光年）有一条约 2.7 千秒差距（kpc）长的、致密而正在形成恒星的气体云链：大犬座 OB1（CMa OB1）、猎户座（Orion）、英仙座（Perseus）、金牛座（Taurus）、仙王座（Cepheus）、北美星云（North America Nebula）与天鹅座 X（Cygnus X）。2020 年，Alves 等（Nature 578, 237；arXiv:2001.08748）用三维尘埃图（3D dust maps）测出这些云的三维位置，发现它们并非散乱分布，而是组成一条窄而连贯的线，像一条阻尼正弦波（damped sine wave）那样在银道面上下蜿蜒，"平均周期约 2 kpc，最大振幅约 160 pc"。他们称之为 **Radcliffe 波**（Radcliffe Wave）。

只看形状并不能说明它是否在运动。地上一条弯弯曲曲的绳子与一条正在被抖动的绳子，在一张照片里看起来一样。要知道 Radcliffe 波是不是真正的"波"（其中的恒星确实穿过银道面上下振荡，并且在每个位置都有波所预言的竖直速度），需要**速度**，尤其是垂直于盘面的竖直速度 v_z。早先用年轻恒星做的运动学研究（Tu 等 2022；Thulasidharan 等 2022；Bobylev 等 2022；Li & Chen 2022；Alfaro 等 2022；Donada & Figueras 2021）结论不一，K24 称之为"不确定"（inconclusive）。

为什么重要：

- 如果这条 2.7 kpc 的结构整体协调地振荡，它的运动就由银河系的竖直引力决定，于是它成了一个称量本地盘的巨大"摆"：银盘中平面密度（midplane density）、太阳附近的暗物质数量，以及太阳自身穿越银盘上下振荡的周期。
- 这样的结构如何形成（经过的卫星星系、落入的气体、盘内的不稳定性、超新星反馈（feedback））尚无定论；它是行进、驻定还是漂移，可以约束这些可能。
- 许多最近的恒星形成区都属于它，所以它的运动就是孕育附近年轻恒星的气体的运动，其中（K24 提出）也许包括那个以超新星吹出本地泡（Local Bubble，太阳所在的热空腔）的星团。

#### 1.2 数据

气体云很难在三维中追踪：射电望远镜只能测出气体朝向或背离我们的速度（一个速度分量）。年轻星团（young stellar clusters）容易些。星团是从同一块云中一起诞生的一群恒星；年轻时它仍随母云运动。Gaia 卫星测量每颗星的距离（由视差 parallax）与在天球上的运动（自行 proper motion）；光谱仪测量其视向速度（radial velocity）。对星团的成员星取平均，得到的星团位置与完整三维速度比单颗星精确得多。

具体而言，K24 用了：

- **年轻星团**（方法，"Stellar Cluster Catalog"）。来自 Cantat-Gaudin 等 2020 星表（基于 Gaia DR2，只保留质量好的视差、自行与视向速度）的星团，加上另外五个星表（Sim 等 2019、Hao 等 2022、He 等 2022、Szilágyi 等 2021、Liu & Pang 2019）的星团；成员星与 Gaia DR3 交叉匹配（cross-match）；视向速度来自 Gaia 以及 APOGEE 巡天（SDSS DR16），以提高覆盖率。每个星团给出日心银道直角坐标中的平均位置 (x, y, z) 与速度 (u, v, w)，以及平均值的标准误差。选择条件：
  - **年龄小于 30 Myr**（百万年），取自文献；按 K24 的说法，这"保证"星团仍追踪其母云的速度；
  - 去掉相对本地静止标准（local standard of rest, LSR，即太阳位置处圆轨道的参考系）视向速度大于 50 km/s 的运动学异常星团；
  - 只在 x–y 平面上选择（俯视）：距尘埃最佳拟合模型 ±5 倍波半径（47 pc，即 ±235 pc）以内的星团，**事先不对高度 z 设限**——竖直方向的图样不是由选择造成的；
  - 去掉 Lacerta OB1 星协，因为它在竖直方向与运动学上都与波不同；
  - 据称与 Hunt & Reffert 2023 的 Gaia DR3 星团表（只取最年轻的）对照，对结果没有影响。
  速度用太阳本动（solar peculiar motion）(u☉, v☉, w☉) = (10.0, 15.4, 7.8) km/s 换算到本地静止标准（LSR），得到 (v_x, v_y, v_z)。正文没有给出星团数目；公开表格（Harvard Dataverse doi:10.7910/DVN/XSCB9N，文件 `Radcliffe_Wave_stellar_clusters_Konietzka2024.tab`，10,888 字节，CC0）说明为 K24 所用星团的机器可读表；登陆页没有给出列与行数，将由研究读取（从图上看约为 10² 行）。
- **分子云**（molecular clouds）：三维云位置取自 Major Cloud Catalog（Zucker 等 2019、2020）与 Alves 等 2020 的"Tenuous Connections"星表，只保留有视向速度测量的云。距离另有约 5% 的系统不确定度。
- **¹²CO 视线速度**（方法，"Line-of-sight Gas Velocities"）。一氧化碳（CO）在 2.6 毫米的射电波段发射，其多普勒频移（Doppler shift）给出气体沿视线的速度 v_LSR。K24 用 Dame 等 2001 的全银河系 CO 巡天（角分辨率 0.125°，速度分辨率 1.3 km/s），在每个云位置 0.3° 范围内提取谱线，保留 |v_LSR| < 30 km/s，用高斯函数拟合（Levenberg–Marquardt 算法）；9% 的云被舍去（超出巡天范围或无发射）。由于波离我们近、又长、又高出银道面约 200 pc，指向不同云的视线方向差别很大，一维速度就能测到 v_x、v_y、v_z（包括竖直分量）的不同组合。公开表格：doi:10.7910/DVN/Q7F4PC，文件 `Radcliffe_Wave_CO_analysis_Konietzka2024.tab`，5,286 字节，CC0（列与行数由研究读取）。

#### 1.3 一步一步：作者如何从数据走到结论

**第 1 步 · 星团与云勾勒出同一结构。** 图 1a 显示年轻星团（蓝色）与云（红色）位于同一条三维正弦曲线上，尽管选星团时没有对 z 设限。K24 由此认为星团诞生于波中的云，可以作为其运动的示踪体（tracer）。图 1b 以 v_z 为第三个轴画出同样的星团：速度也组成一个波，并沿结构相对位置波有所错开。

**第 2 步 · 竖直方向的力：非谐振子（anharmonic oscillator）。** 振幅很小时，盘附近的恒星上下运动就像弹簧上的质量，即谐振子（harmonic oscillator），角频率为 ν，ν² = 4πGρ₀，ρ₀ 是银盘中平面的密度。波可以达到约 220 pc，与盘的标高（scale height）相当，那里回复力变弱、振荡变慢，就像摆角很大的单摆。K24 把竖直势写成（方法，式 1）

  Φ(z, r) = ½ ω₀² exp[(r☉ − r)/r₀] (z² − μ₀² z⁴)，

其中 r☉ = 8.4 kpc，ω₀ 是太阳半径处的小振幅角频率，r₀ 是密度的径向标长（scale length），μ₀ 与竖直标高的倒数成正比（z₀ = 1/(√6 μ₀)）。这三个数起初并不对波拟合，而是让式 1 在 r = 7–10 kpc、|z| ≤ 300 pc 范围内以 χ² 拟合一个现有银河系模型（Allen & Santillan 1991，参数按 Irrgang 等 2013 更新）得到：**ω₀ = 74 km s⁻¹ kpc⁻¹，r₀ = 3.7 kpc，μ₀ = 1.3 kpc⁻¹**，对应本地密度 ρ₀ ≈ 0.1 M☉ pc⁻³ 与标高 z₀ = 1/(√6 μ₀) = 314 pc（文献值：0.097 ± 0.013 M☉ pc⁻³ 与 280 (+70/−50) pc，McKee 等 2015）。由能量守恒得到上升到 z_max 的云的周期 T（式 2），借助第一类完全椭圆积分（complete elliptic integral of the first kind）K 得到解析的频率 ω(z_max, r)（式 3），振幅越大频率越低。由于波跨越不同的银心距，r 与 z_max 都是沿波位置 s 的函数，所以 ω = ω(s)。引力势被假设为稳态（stationary）；倾斜、银盘翘曲（warp）以及太阳附近"沿径向演化的竖直波"（radially evolving vertical waves；Schönrich & Dehnen 2018；Xu 等 2015）被论证为可以忽略。

**第 3 步 · 波的模型。** 沿波长度方向，波由下式描述（式 4–5）：

  z(s, t) = ζ(s) [ B sin(ω₀t + 2πΛ(s) + φ) + (1 − B) sin(−ω₀t + 2πΛ(s) + φ) ]，
  v_z(s, t) = ζ(s) ω(s) [ B cos(ω₀t + 2πΛ(s) + φ) − (1 − B) cos(−ω₀t + 2πΛ(s) + φ) ]。

其中 s 是沿波（投影到 x–y 平面）的距离（起点 s = 0，在 CMa OB1 附近）；盘面内的基线是一条过三个锚点 (x₀, y₀)、(x₁, y₁)、(x₂, y₂) 的二次曲线；ζ(s) 是竖直包络（envelope）；Λ(s) 是累积相位（cumulative phase）；φ 是相位常数；t 是时间（ω₀t 是当前的相位偏移）。参数 **B 混合两列方向相反的波**：B = 1（或 0）是纯**行波**（travelling wave），B = 0.5 是纯**驻波**（standing wave）。

- *为什么 z 与 v_z 的相位关系重要。* 在行波中 z ∝ sin(…)、v_z ∝ cos(…)：波穿过银道面的地方速度最大，波峰处速度为零——沿波方向位置与速度相差 **90° 相位**。在驻波（B = 0.5）中两项合成为 z = ζ sin(2πΛ + φ) cos(ω₀t) 与 v_z = −ζω sin(2πΛ + φ) sin(ω₀t)：z 与 v_z 的空间图样相同（**相位差为零**），零点（波节 nodes）永不移动。所以位置波与速度波的相对相位就是区分两者的观测量。
- *行波与引力势。* 对行波而言，给定引力势，空间形状就完全决定了 v_z（振幅乘以 ω(s)）；对驻波，波峰处的速度幅度不由形状决定。因此拟合可以由 z 预言 v_z，而不需要自由的速度幅度参数。
- *沿波缩短的波长*（式 6–7）：Λ(s) = s/(p − γs)，所以局部波长 λ(s) = (p − γs)²/p。K24 称 p 为"波的周期"，但它是长度（pc）：s = 0 处的波长；γ 决定波长缩短的快慢。
- *阻尼*（式 9）：ζ(s) = −A [1 + ((s − s₀)/δ)²]⁻¹，振幅为 A、峰值在 s₀、宽度为 δ 的洛伦兹（Lorentzian）包络。K24 发现洛伦兹形略好于 Alves 等 2020 的高斯形，并指出真实情况可能是两者的混合（如 Voigt 轮廓），但数据约束不了。
- 竖直模型有 14 个参数 Θ₁ = (x₀, y₀, x₁, y₁, x₂, y₂, A, p, φ, s₀, δ, γ, ω₀t, B)；盘面内运动另加两个 Θ₂ = (v_x,plane, v_y,plane)。

**第 4 步 · 拟合。** 对每个星团 k，到模型的"距离"是四维矢量 (x, y, z, v_z/ω₀) 减去模型在最近点 s_min 的值（式 12）；v_z 除以 ω₀ 把速度变成长度，让位置与速度同等重要。似然函数（likelihood，式 13）用一个共同的弥散 σ、核密度权重（kernel-density weights，让猎户座这样采样密集的区域不至于主导），以及一个软的离群函数（outlier function）C（tanh 截断）：任何一个分量 c = tanh(x²) 超过 tanh(3) 的星团算离群点，K24 称之为在 3σ 半径之外（按单个分量相当于 |x| > √3 ≈ 1.7σ；我们的理解）。云用三维版本（式 11）。用嵌套采样（nested sampling）程序 dynesty（1000 个活点）抽样，各参数先验独立，"依据初步拟合"设定（扩展数据表 1），例如 A ~ N(215, 20) pc、p ~ N(4650, 300) pc、ln γ ~ N(0.35, 0.07)、ln(δ/pc) ~ N(6.5, 0.1)、s₀ ~ N(680, 200) pc、φ ~ N(−0.09, 0.5) rad、ω₀t ~ U(−π/2, π/2)、B ~ U(0, 1)、盘面内速度 ~ U(−10, 10) km/s。弥散 σ 为 47 pc，即波的"半径"。

**第 5 步 · 数值（扩展数据表 2；± 为第 16–84 百分位）。**

| 参数 | (3) 只用云 | (4) 只用星团 | (5) 星团，混合模型（B 自由） | (6) 云 + 星团 | (7) 云 + 星团，ω₀ μ₀ r₀ 自由 |
|---|---|---|---|---|---|
| A (pc) | 219.88 +18.34/−16.24 | 216.52 +11.54/−10.95 | 229.32 +13.23/−12.18 | 218.64 +13.81/−11.41 | 222.92 +13.32/−12.5 |
| p (pc) | 4773.99 +189.15/−187.63 | 4752.21 +207.28/−198.8 | 4715.14 +216.07/−214.2 | 4779.9 +195.49/−192.26 | 4749.05 +191.12/−182.03 |
| δ (pc) | 797.78 +67.28/−62.43 | 624.25 +60.19/−55.96 | 649.14 +61.95/−56.19 | 740.01 +58.78/−55.14 | 738.57 +59.33/−52.89 |
| s₀ (pc) | 482.71 +113.81/−103.35 | 673.18 +104.02/−103.13 | 662.89 +112.13/−107.4 | 544.99 +89.88/−100.53 | 517.02 +99.91/−91.41 |
| γ | 1.49 ± 0.07 | 1.4 +0.09/−0.07 | 1.4 +0.1/−0.08 | 1.46 +0.08/−0.07 | 1.46 +0.09/−0.07 |
| φ (rad) | −0.12 +0.13/−0.14 | −0.23 ± 0.16 | 0.01 +0.25/−0.23 | −0.15 ± 0.13 | −0.14 +0.13/−0.14 |
| ω₀t (rad) | – | – | −0.38 +0.19/−0.17 | – | – |
| **B** | – | – | **0.84 +0.07/−0.06** | – | – |
| ω₀ (km s⁻¹ kpc⁻¹) | – | – | – | – | 67.713 +7.677/−7.111 |
| μ₀ (kpc⁻¹) | – | – | – | – | 1.377 +0.249/−0.247 |
| r₀ (pc) | – | – | – | – | 3563.32 +513.7/−500.43 |

（锚点 x₀…y₂ 也在表中，各列之间在约 1σ 内一致。表注说第 (7) 列"与 (5) 相同的做法"，但其列名——云 + 星团——对应 (6)；我们把 (7) 理解为放开引力势参数的 (6)。）K24 指出只用云、只用星团与两者合用的拟合相互一致，并以此确认云与年轻星团组成一个在空间与运动学上都连贯的结构。最佳拟合画在图 1 中（用普通的银道 x、y、z 坐标）；扩展数据图 1–3 则把 x–y 坐标系逆时针旋转 62°，使横轴（"沿波位置"，约 −1300 到 +1500 pc，0 在太阳附近）沿波方向。

导出的数值（正文与方法）：

- **最大振幅约 220 pc；平均波长约 2 kpc**（约 2000 pc，由式 7 得出，从 CMa OB1 附近的约 4000 pc 变到天鹅座 X 附近的约 400 pc）。我们的核对：用第 (6) 列，λ(0) = p ≈ 4.78 kpc，λ(0.3 kpc) ≈ 3.9 kpc，λ(2.4 kpc) ≈ 0.34 kpc，λ(s) 在 0–2.4 kpc 上的平均约 2.1 kpc，与 K24 的描述一致（这是我们的理解；数据的 s 范围是假设的）。
- **最大竖直速度约 14 km/s。**
- **行波而非驻波。** 在 [0, 1] 上取平坦先验时 B = 0.84 (+0.07/−0.06)。另做一个 B 固定为 1 的拟合，得对数贝叶斯因子（Bayes factor）ΔlnZ = ln Z₂ − ln Z₁ ≈ 1（Z₁：B = 1，Z₂：B 自由）；K24 写道"两个模型对数据拟合得同样好，而 B = 1 固定的实现略受偏好"（该拟合同时固定 ω₀t = 0），结论是"波的运动在一阶上与行波一致"，此后取 B = 1。驻波（B = 0.5）由另一个论证排除：若 B = 0.5，各星团的相位 φ_k = arctan(z_k ω_k / v_z,k) 沿 s 应几乎不变（变化至多约 0.03π），但实际上覆盖了 −π/2 到 π/2 的整个范围。正文中这变成"行波相对驻波受到强烈偏好"，而方法部分的说法是"在一阶上与行波一致"。
- **相速度**（phase velocity，波峰看起来移动的速度，λ(s)/T(s)）：从 CMa OB1 附近约 40 km/s 到天鹅座 X 附近约 5 km/s，从太阳看波峰从右向左移动。若要用本地密度的变化解释这一数量级的变化，ρ₀ 至少要变化两个数量级，K24 认为不可能；它提出波可能由两种物理过程共同塑造。
- **离群点。** 英仙座与金牛座的所有星团都成为离群点；K24 归因于本地泡与英仙–金牛（Per–Tau）反馈泡的膨胀，这些云位于泡的表面。其余离群点大多在猎户座，那里离群点的数目不超过内点的四分之一（≤ 星团的 20%）。
- **太阳的高度。** 放开太阳在银道面上的高度（均匀先验 −10 到 25 pc），A、φ、δ 的变化小于其 1σ 误差的三分之一，其他参数的变化小于 1σ 的 10%。
- **盘面倾斜与引力势。** 让盘面倾斜（多两个角度），以及把引力势换成 McMillan 2017 或 galpy 的 MWPotential2014（Bovy 2015），据称都没有影响。

**第 6 步 · CO 核对。** 把最佳拟合的六维模型 (x, y, z, v_x, v_y, v_z) 投影到每块云的视线方向，v_LSR = cos l cos b v_x + sin l cos b v_y + sin b v_z（式 14），得到的曲线穿过实测的 ¹²CO 速度（扩展数据图 3a：v_LSR 从 CMa 一端的约 +20 km/s 降到扩展数据图 3a 旋转后横轴上位置 ≈ 0–500 pc 处（不是 s；s 从 CMa OB1 附近的 0 起算）的约 0–2 km/s，再升到远端的约 +6 km/s）。K24 的结论是"我们的模型解释了 ¹²CO 观测"，即气体随星团一起运动。一致性只以图示给出，没有拟合优度数值。

**第 7 步 · 盘面内的漂移。** 扣除银河系自转与较差自转（Allen & Santillan 势；另两个势"没有影响"）后，以 2 km/s 的典型误差做 χ² 拟合，得 v_x,plane = −3.9 (+2.6/−2.7) km/s、v_y,plane = 3.1 (+2.7/−2.6) km/s，即沿背离太阳的径向 4.9 km/s（扩展数据图 2：4.87），沿波方向 1.0 km/s（0.96）。K24 把它描述为整体（刚体 solid-body）漂移，"以约 5 km s⁻¹ 的速度沿径向远离银心"。往回推，漂移指向 Upper Centaurus Lupus 与 Lower Centaurus Crux 星团 15–16 Myr 前形成的位置，它们的超新星吹出了本地泡；K24 说精确的回溯超出了本文范围。

**第 8 步 · 用波称量银盘。** 放开 ω₀、μ₀、r₀（第 7 列；B = 1 时共 15 个参数）得 ω₀ = 68 (+8/−7) km s⁻¹ kpc⁻¹、μ₀ = 1.4 ± 0.2 kpc⁻¹、r₀ = 3.6 ± 0.5 kpc，与采用值 74、1.3、3.7 一致；固定与放开引力势的证据比（evidence ratio）同样是 ΔlnZ ≈ 1（"同样好"）。用等温层（isothermal sheet）关系 ρ₀ = ω₀²/(4πG) 与 z₀ = 1/(√6 μ₀)（Spitzer 1942）：

- **银盘中平面总密度 ρ₀ = 0.085 (+0.021/−0.017) M☉ pc⁻³**，标高 z₀ = 294 (+63/−43) pc（K24 提醒，z₀ 超过约 300 pc 时频率的变化小于噪声），面密度 Σ₀ = 2 z₀ ρ₀ = 50.3 M☉ pc⁻²；
- 减去重子（恒星与气体，0.084 ± 0.012 M☉ pc⁻³，McKee 等 2015）：球形晕的**本地暗物质密度 0.001 (+0.024/−0.021) M☉ pc⁻³**，与零相容，并在 1σ 内与常规估计一致；
- **太阳的竖直振荡周期 95 (+12/−10) Myr**，取太阳竖直速度 7.8 km/s，用 2000 次蒙特卡罗（Monte Carlo）抽样；K24 用的是频率参数放开、对 Radcliffe 波拟合得到的引力势（第 (7) 列，ω₀ ≈ 68 km s⁻¹ kpc⁻¹；按我们对方法部分的理解）；所以太阳**每 48 (+6/−5) Myr 穿越一次银盘**。太阳的高度（−10 到 25 pc）使其改变 < 0.5 Myr；R☉ 从 7.9 到 8.7 kpc 没有影响。作为比较，只用重子（McKee 等 2015，Σ₀ = 47.1 M☉ pc⁻²）得 95.3 Myr，重子加 0.013 M☉ pc⁻³ 的暗晕得 88.2 Myr，都在 1σ 以内；
- **薄暗盘**（dark disk）：假设暗盘标高为 25 pc，K24 称之为"相对较大"（偏保守，因为面密度相同时更薄的盘会使周期更短），并且没有额外的暗晕（暗晕"只会进一步降低上限"），95 Myr 的周期给出面密度 0.1 (+3.3/−3.3) M☉ pc⁻²，K24 称之为上限（我们的理解：与零相容，1σ 上端约 3.4 M☉ pc⁻²）。

**粗略估算。** (1) *速度幅度。* 小振幅的角频率为 ω₀ = 74 km s⁻¹ kpc⁻¹ = 0.076 Myr⁻¹（1 km s⁻¹ kpc⁻¹ ≈ 1/978 Myr⁻¹）。在 z_max = 220 pc，式 3 的非谐修正（μ₀z_max ≈ 0.29）在太阳半径处使其降低约 7%，到约 0.070 Myr⁻¹（我们的计算）。速度幅度 = 振幅 × 角频率 ≈ 220 pc × 0.070 Myr⁻¹ ≈ 15 pc/Myr ≈ 15 km/s（1 pc/Myr ≈ 0.98 km/s），接近报告的约 14 km/s（其余差别来自式 3 的径向因子 exp[(r☉ − r)/(2r₀)] 以及振幅峰值沿波的位置；我们的理解）。(2) *周期。* 太阳以 v_z = 7.8 km/s 只升到约 100–115 pc（我们的估算）。用拟合得到的 ω₀ = 68 km s⁻¹ kpc⁻¹（0.0695 Myr⁻¹）以及约 115 pc 处约 2% 的非谐修正，2π/ω ≈ 92 Myr，接近 K24 的 95 (+12/−10) Myr；这是我们独立的估算，不是 K24 的计算（在采用的 ω₀ = 74 引力势中，太阳的周期约为 83–84 Myr）。(3) *密度。* ρ₀ = ω₀²/(4πG)：ω₀ = 68 km s⁻¹ kpc⁻¹ = 2.2 × 10⁻¹⁵ s⁻¹，得 5.8 × 10⁻²¹ kg m⁻³ = 0.085 M☉ pc⁻³。(4) *相速度。* λ/T 在 CMa 一端约 4000 pc / 95 Myr ≈ 42 km/s，在天鹅座一端约 400 pc / 90 Myr ≈ 4.4 km/s，与约 40 与约 5 km/s 相符。所以主要结论归结为：波的高度（220 pc）与竖直速度（约 14 km/s）错开四分之一波长，正是一个在已知银盘引力势中振荡的物体应有的表现。

#### 1.4 结论与把握程度

- **结论：**
  1. Radcliffe 波像一列由银河系引力驱动的行波那样穿越银道面振荡，最大振幅约 220 pc，平均波长约 2 kpc，最大竖直速度约 14 km/s；猎户座、仙王座、北美星云与天鹅座 X 作为这列波的一部分运动；
  2. 行波相对驻波"受到强烈偏好"；
  3. 气体（¹²CO）与年轻星团一起运动；
  4. 波以约 5 km/s 的速度沿径向向外（远离银心）漂移，支持本地泡的母星团形成于其中的设想；
  5. 把它当作连贯的振子，测得 ρ₀ = 0.085 M☉ pc⁻³、与零相容的本地暗物质密度、暗盘的上限，以及太阳 95 Myr 的竖直周期。
- **作者给出的保留：** 阻尼轮廓可能是数据约束不了的混合形；标高在约 300 pc 以上约束很弱；在几千万年的时间尺度上，波很可能受到云的瓦解与相混合（phase mixing）的影响；天鹅座一端的小起伏与尘埃距离误差相当；英仙座与金牛座不随波运动；波的起源仍未解决。
- **我们读出的、要带进第二部分的要点**（K24 并未把它们当作问题提出）：
  - 正文的"强烈偏好"与方法部分的 ΔlnZ ≈ 1、"两个模型拟合得同样好"之间的差别。贝叶斯因子比较的是 B = 1 与 B 自由，而不是行波与驻波；驻波是由相位论证以及后验 B = 0.84 (+0.07/−0.06) 在后验中远高于 0.5 排除的（区间 0.84（+0.07/−0.06）；我们不把这一距离换算成显著性：后验有界且不是高斯分布）。另外，若 ΔlnZ = ln Z₂ − ln Z₁ ≈ +1 且 Z₂ 是 B 自由的模型，所说的"B = 1 固定略受偏好"符号似乎相反（除非下标互换）：印出的定义与所述的偏好彼此矛盾，我们无法判断哪一处有误。K24 报告的证据比（B = 1 对 B 自由；固定对放开引力势）都只有 ΔlnZ ≈ 1，并用它们来论证取 B = 1、称几个引力势等价。后验中位数 B = 0.84 不能读作反对 B = 1 的约 2σ 证据，因为先验在 1 处截断（后验以 1 为界时，即使 B = 1，中位数也会低于 1）；相关的比较是 B = 1 对 B 自由的证据比 ΔlnZ ≈ 1。B = 1 的拟合同时固定了 ω₀t = 0。
  - 离群判据 tanh(x²) > tanh(3) 按单个分量是 |x| > √3 σ ≈ 1.7σ，而 K24 称之为 3σ 半径。
  - 先验是"依据初步拟合"（用同样的数据）设定的，有些与后验差不多一样窄（γ：ln γ 先验宽 0.07，即 γ 约 ±0.10，后验 ±0.07–0.09；A：先验 ±20 pc，后验 ±11–18 pc）。尤其是 γ 的结果可能主要由先验决定。r₀ 的先验 N(3659, 500) pc 与第 (7) 列的后验 3563 (+514/−500) pc 一样宽，所以那里的 r₀ 由先验决定。δ 的先验 exp(6.5) ≈ 665 ± 67 pc 比只用云的后验 798 pc 低约 2σ。ω₀ 的先验 ln(ω₀/(km s⁻¹ pc⁻¹)) ~ N(−2.4, 0.17) 即 ω₀ ≈ 91 km s⁻¹ kpc⁻¹ 约 ± 17%，中心比采用值 74 高约 1.2σ、比后验 68 高约 1.7σ（按对数）。只有 μ₀ 的先验 ln(μ₀ pc) ~ N(−1.346, 0.25)，即 0.26 pc⁻¹，按印刷的形式无法解释（我们的理解）。
  - 拟合用的竖直频率 ω(s) 来自对现有银河系模型拟合的引力势；因此 v_z 的预言并不独立于用来称量银盘的引力势（第 8 步用同样的数据把它放开）。
  - CO 的一致与星团的一致都以图示给出，没有拟合优度数值。
- **作者若是错的，需要什么成立：**
  - *速度与位置并不协调。* Zhu 等 2024（ApJ 971, 167 [S：卷号来自检索列表]；arXiv:2402.15346 [V 摘要]）重新估算了竖直速度，通过两条途径加入了视向速度：(i) 年轻恒星的 APOGEE-2 视向速度配合 Gaia DR3 自行；(ii) 云的视向速度配合相关年轻恒星天体（young stellar objects, YSOs）的 Gaia DR3 自行，发现竖直速度的振荡"与竖直坐标不同步"：沿波的 v_z 呈约 5 km s⁻¹ kpc⁻¹ 的梯度，呈"偶极状"（dipole-like）图样，他们认为这使 Radcliffe 波模型"受到质疑"。如果他们的 v_z 图样正确，定义 K24 行波的 90° 相位关系就不成立。
  - *在一个振荡周期内波不是刚体。* Li、Zhou & Chen 2024（arXiv:2410.14603 [V 摘要]；期刊未核实）用本地气体的三维模拟论证，银河系的剪切（shear）与本轮运动（epicyclic motion）会在约 45 Myr 内把波拉长到"几乎是现在长度的两倍"，而在这段时间内"所提出的竖直振荡只完成半个周期"，并称把它当作刚体是"过度简化"。若如此，用一条相位规律 Λ(s)（以及刚体式的盘面内漂移）描述的单一连贯振荡就不是好的描述，即使局部的片段在上下运动。
  - *位置与速度给出不同的波长，或漂移更快。* Bobylev、Ikhsanov & Bajkova 2025（Astrophys. Bull. 80(2)，arXiv:2503.21019 [V 摘要]）按年龄分析疏散星团：与波相关的星团不超过 30 Myr（支持 K24 的年龄截断）；对 5.2 Myr 的一组，他们得到位置振幅 z_max = 117 ± 12 pc、波长 4.55 ± 0.14 kpc，但竖直速度幅度为 4.86 ± 0.19 km/s、波长 1.74 ± 0.08 kpc；对 18.6 Myr 的一组为 54 ± 5 pc（λ 6.30 ± 0.12 kpc）与 7.90 ± 0.16 km/s（λ 0.83 ± 0.11 kpc）；远离银心的径向运动为 10 pc/Myr（≈ 10 km/s，是 K24 5 km/s 的两倍）；他们倾向于约 2 kpc 宽的超新星激波前起源。z 与 v_z 的波长不同（我们的理解）不是单一连贯行波所预言的。他们的方法与选择和 K24 不同。
  - *离群点与选择的处理造成了信号。* 英仙座与金牛座的星团全部被标为离群点；软的 3σ 离群模型与核密度权重决定了每个区域的分量。如果 90° 相位差依赖于这些选择，或依赖于少数几个猎户座与仙王座的星团，振荡就没那么可靠。
  - *年龄截断并不保证星团仍随气体运动。* 年龄可达 30 Myr 的星团已有三分之一个振荡周期的时间离开母气体；K24 依靠 CO 核对来说明这一点。

### 第二部分 · 论证逻辑

#### 2.0 论证地图

编码的结论有三部分：(1) 波像一列由银河系引力势驱动的行波那样穿越银道面振荡（这一部分合并了摘要中的"the Radcliffe Wave is oscillating through the Galactic plane"与正文第 2 页关于图 1 拟合的一句："indicates that the Radcliffe Wave oscillates through the Galactic plane like a traveling wave"）；(2) 行波相对驻波受到偏好（正文第 2 页）；(3) 把波当作连贯的振子，它测得本地竖直引力势（银盘中平面密度）与太阳的竖直周期（摘要）。径向漂移与本地泡的联系只讨论，不编码（2.6）。

A. 年轻星团与云同处一地，且星团只在 x–y 平面上选样；[缺口] 所以星团诞生于波中（K24 只是这样提示）；年龄小于 30 Myr，仍随母云运动；模型还解释了 ¹²CO 速度 ⇒ 星团的运动学就是波的运动学。
B. 只有引力作用，引力势是定常的非谐势，参数取自现有的银河系模型 ⇒ 对行波而言形状决定 v_z。行波（B = 1）对 z 与 v_z 的拟合极好，两者相差 90°。
C. 星团相位覆盖 −π/2 到 π/2，驻波不允许这样（[缺口] 除非这一分布是噪声）；混合模型拟合给出 B = 0.84，离 1 比离 0.5 近；[缺口] 两者都建立在属于波本身的星团 v_z 图样之上 ⇒ **行波相对驻波受到偏好**；B = 1 与 B 自由拟合得同样好 ⇒ 取 B = 1。
D. 取 B = 1 后，极好的拟合、[缺口] 同一个稳健的 v_z 图样，以及 [缺口] 尽管有银河系的剪切仍是一列连贯的波 ⇒ **波像行波那样振荡**。
E. 放开引力势后拟合给出 ω₀ = 68 km s⁻¹ kpc⁻¹；等温层把它换算成密度；[缺口] 这一后验由数据而不是由初步拟合定出的先验决定 ⇒ **波称量了本地银盘，并给出太阳的周期**。

顺序很重要：K24 解读为振荡的图 1 拟合是 B = 1 的实现，而 B = 1 是在混合模型拟合与证据比较之后才采用的（"implying that we can set B = 1 in all further performed calculations"）。所以振荡的结论（D）在行波与驻波的比较（C）之后，而不是之前。

检查方法：论证用 Lean 4 写成（[`studies/011-m11-radcliffe-wave-oscillation/argument/Argument.lean`](https://github.com/sudoghut/astrolab/blob/main/studies/011-m11-radcliffe-wave-oscillation/argument/Argument.lean)）。每个前提是 `Field` 的一个构造子（constructor，不用公理），标注类型与出处性质：

| 标注 | 前提类型 |
|---|---|
| `OBS` | 观测或测量（注明表或图） |
| `MOD` | 模型假设，或论文明说的推理规则 |
| `STAT` | 统计推断（拟合优度、模型与数据的一致、后验、模型比较） |
| `NUM` | 数值结果，由本仓库的 `run.py` 复算（暂无：研究还没有结果） |
| `LIT` | 取自其他文献的结果 |
| `GAP` | 推理需要、但论文与标准知识都没有提供的前提（隐含前提，gap premise） |

出处性质：`[stated: "引文"]`（论文明说，引文取自 arXiv v1 原文）、`[implied]`（论文依赖但没写出的标准知识，注明来源）、`[reconstructed]`（我们补上的，恰好是 `GAP` 前提；K24 之后发表的文献也归入此类，因为 K24 不可能依赖它）。

Lean 检查的内容：结论由这些前提推出（`final`）且不是恒真（`final_nontrivial`）；前提可以同时成立（`consistent`）；任何单个前提都推不出结论（`alone_insufficient`）；每个前提是必要的（有不含它的反例模型，countermodel）还是多余的；论文明说的前提是否足够（`stated_*`），加上标准知识后是否足够（`explicit_*`；`explicit_insufficient` 表示真正的缺口）。Lean 不检查每个前提内部的物理与统计——那是第一、三部分和研究本身的任务。

K24 有几句话是推理规则（"我们发现波像行波那样振荡"、"我们可以把结果……推广到包括气体在内的所有成分"、"行波受到强烈偏好"、"把波当作连贯振荡的结构，我们可以……直接测量……"）。我们把每一句编码为蕴涵式，并在我们的分析认为这一步还需要更多条件时，把缺少的条件作为额外的前件加进去；前件更多的蕴涵式比引文更弱，所以 `[stated]` 标注仍然如实，缺少的条件则作为单独的 `GAP` 前提出现。带保留措辞的推理（"suggesting"、"indicates"）从不编码为明说的蕴涵式，因为那会断言比引文更多的内容：要么这一步成为 `GAP`（星团诞生于波中），要么改引 K24 对同一步的明确表述（用方法部分的"we find that the Radcliffe Wave oscillates like a traveling wave"代替正文的"indicates"；用正文的"we find that a traveling wave is strongly preferred"代替方法部分的"The value of B closer to 1 indicates that data favors a traveling wave"）。

#### 2.1 环节 A · 年轻星团示踪波

*概述。* 波是在气体（三维尘埃图）中发现的；它的速度来自年轻星团。两者的联系是：尽管星团选样没有高度截断，星团与云仍在同一位置，所以星团诞生于波中；它们很年轻，还没有离开母云；而且对星团（与云一起）拟合的模型也重现了气体的视线速度。

**前提。**

| 前提（Lean 构造子） | 标注 | 出处性质 | 论文出处 |
|---|---|---|---|
| `obs_coloc`：年轻星团与云在三维中同处一地 | OBS | stated: "As expected, the young clusters and star-forming molecular clouds are co-located in three dimensions." | 正文第 1 页，图 1a |
| `mod_xy`：星团只在 x–y 平面上选样，没有高度截断 | MOD | stated: "We make a conservative selection on the x-y plane by enclosing all stellar clusters within ±5 times the radius of the Wave (47 pc) from the best fit of the dust component" | 方法，Stellar Cluster Catalog |
| `gap_born`：同处一地 + 没有高度截断 ⇒ 星团诞生于波中的云 | GAP | reconstructed | K24 只是提示（正文第 1 页：选样"without an a priori selection criterion for height off the Galactic plane (see Methods), suggesting that the clusters' stars were born in the molecular clouds along the Radcliffe Wave"） |
| `mod_age`：诞生于波中且小于 30 Myr ⇒ 仍随母云运动 | MOD | stated: "We restrict our analysis to only the youngest clusters (ages smaller than 30 Myr), guaranteeing that these associations are still tracing the velocities of the molecular clouds that served as their birthplaces." | 方法，Stellar Cluster Catalog |
| `stat_co`：最佳拟合模型解释了 ¹²CO 视线速度（模型与数据的一致） | STAT | stated: "We show in Extended Data Figure 3a that our model explains the 12CO observations" | 方法，Line-of-sight Gas Velocities |
| `mod_transfer`：示踪 + CO 相符 ⇒ 云与星团是运动学上连贯的同一结构 | MOD | stated: "As a consequence, we can transfer our results from the full phase-space study of the stars to all components of the Radcliffe Wave, including the gas" | 方法，Line-of-sight Gas Velocities |

**其他解释。**

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 星团的竖直图样是选样造成的 | `mod_xy`、`gap_born` | 是：只在 x–y 平面上选样，取尘埃模型两侧 ±5 倍波半径 |
| 星团并非诞生于波中，只是在它前方或后方，或是偶然排在一起的无关年轻星群 | `obs_coloc`、`gap_born` | 部分：表明了三维同处一地，但 K24 只是"提示"共同起源，没有给出检验（年龄与位置、化学组成、偶然排列） |
| 年龄达 30 Myr 的星团已离开其气体，其 v_z 不是气体的 v_z | `mod_age`、`stat_co` | 部分：年龄截断被说成"保证"示踪，CO 核对只有图示，且只通过视线方向探测 v_z |
| 英仙座、金牛座与蝎虎座（Lacerta）不随波运动 | （不编码：已被剔除） | 是：Lacerta 事先排除；英仙座与金牛座的星团全部成为离群点，归因于反馈泡 |

**推理（Lean 摘录）。**

```lean
have c : v.Coherent :=
  p .mod_transfer (p .mod_age (p .gap_born (p .obs_coloc) (p .mod_xy))) (p .stat_co)
```

**评述。** 每一环都说得通，但有三环是定性的。共同起源 K24 只是提示（"suggesting that the clusters' stars were born in the molecular clouds"），所以作为缺口进入（`gap_born`）：同处一地且没有高度截断使它很可能成立，但没有给出检验。"保证"一词很强：30 Myr 约为竖直周期（约 90 Myr）的三分之一，如果气体受反馈推动（K24 正是用反馈解释英仙座与金牛座），这段时间足以让恒星与气体分开。CO 核对是唯一针对气体的检验，而它是没有拟合优度数值的图；由于每条视线都混合了 v_x、v_y 与 v_z，v_LSR 相符本身并不能说明气体具有星团的 v_z。K24 还指出只用云、只用星团与两者合用的拟合相互一致（方法："confirming that the Radcliffe Wave is a spatially and kinematically coherent structure"）；我们没有把它编码为第二条路径，因为只用云的拟合没有速度信息。

#### 2.2 环节 B · 模型与拟合

*概述。* 如果只有引力作用且竖直引力势已知，波的每一段都以已知频率 ω(s) 振荡；对行波而言，空间形状就决定了竖直速度（幅度 ζ(s)ω(s)，与 z 错开四分之一波长），没有自由的速度幅度。此时引力势的三个参数并不是对波拟合的：它们来自用式 1 对现有银河系模型做的 χ² 拟合。B = 1 时对星团 (x, y, z, v_z/ω₀) 与云的联合拟合（图 1；扩展数据表 2 第 (6) 列）"极好"，并有 90° 相位差。

**前提。**

| 前提（Lean 构造子） | 标注 | 出处性质 | 论文出处 |
|---|---|---|---|
| `mod_grav`：竖直方向只有引力作用于波 | MOD | stated: "We therefore model the forces acting on the Wave solely by gravity." | 方法（与周围介质的密度比 10⁴） |
| `mod_potpar`：采用的 ω₀ = 74、r₀ = 3.7、μ₀ = 1.3 由对现有银河系模型的 χ² 拟合得出 | MOD | stated: "These parameters are adopted by comparing equation (1) with an existing model of the Galactic potential including its updated parameters" | 方法；Allen & Santillán 1991，参数取自 Irrgang 等 2013（arXiv:1211.4353） |
| `mod_pot`：竖直引力势是取这些参数的式 1 非谐振子 | MOD | stated: "Since the Radcliffe Wave's amplitude is on the order of the Galaxy's vertical scale height, the vertical gravitational potential Φ resulting in this acceleration can be represented by an anharmonic oscillator." | 方法，式 1 |
| `mod_stationary`：引力势是定常的（stationary） | MOD | stated: "Note that, consistent with the literature, we treat the underlying Gravitational potential as stationary." | 方法 |
| `mod_shape`：引力 + 已知定常引力势 ⇒ 对行波而言形状决定 v_z | MOD | stated: "For a traveling wave, the wave's spatial shape fully determines vertical velocities, assuming a gravitational potential" | 正文第 2 页 |
| `stat_twfit`：行波（B = 1）模型拟合 z 与 v_z，相差 90° | STAT | stated: "While a traveling wave provides an excellent fit to the observations, with a 90° phase offset between position (z) and velocity (vz), as evident in Figure 1" | 正文第 2 页；图 1 是 B = 1 的拟合（扩展数据表 2 第 (6) 列） |

**其他解释。**

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 非引力的驱动（反馈泡、气体压力、磁场）造成竖直运动 | `mod_grav` | 部分：密度比 10⁴；受反馈主导的英仙座与金牛座星团是离群点 |
| 非定常的引力势（翘曲、倾斜、太阳附近的径向竖直波） | `mod_stationary`、`mod_pot` | 是：拟合了倾斜（无影响），翘曲的时标更长，论证径向波可忽略，试了三个引力势 |
| 换一个银河系模型会给出不同的 ω(s) | `mod_potpar` | 是：据称 McMillan 2017 与 MWPotential2014 都没有影响；环节 E 把参数放开 |

**推理（Lean 摘录）。**

```lean
have z : v.VzFixed :=
  p .mod_shape (p .mod_grav) (p .mod_pot (p .mod_potpar)) (p .mod_stationary)
```

**评述。** 这一环节只是搭好检验；结论在环节 D 中得出。注意拟合优度是作为原子命题进入的：K24 称拟合"极好"并在图 1 中展示，但没有单独给出 v_z 分量的拟合优度统计量。

#### 2.3 环节 C · 是行波而不是驻波；取 B = 1

*概述。* K24 让数据在行波（B = 1）、驻波（B = 0.5）与混合之间选择，对星团做 B 自由的拟合（扩展数据表 2 第 (5) 列）。一个论证排除驻波：在驻波中，星团相位 φ_k = arctan(z_k ω_k / v_z,k) 沿波应几乎不变（在无噪声的模型中变化至多约 0.03π），但实际覆盖了 −π/2 到 π/2 的整个范围。混合模型拟合还给出 B = 0.84 (+0.07/−0.06)，离 1 比离 0.5 近；K24 把它读作数据偏好行波（"indicates"），正文则明确表述了结果（"we find that a traveling wave is strongly preferred"）。之后 B 固定为 1 的拟合"同样好"（ΔlnZ ≈ 1），于是此后（包括图 1）一律取 B = 1。

**前提。**

| 前提（Lean 构造子） | 标注 | 出处性质 | 论文出处 |
|---|---|---|---|
| `stat_phase`：观测到的相位 φ_k 覆盖 −π/2 到 π/2 | STAT | stated: "In contrast, we find that the phases φk change over the whole range of -π/2 to π/2, such that B = 0.5 is inconsistent with the data." | 方法（波模型） |
| `mod_standing`：驻波 + 分布不是噪声造成的 ⇒ 观测相位不会覆盖整个范围 | MOD | stated: "From equations (4) and (5) we conclude that the phases φk should be roughly constant" | 方法（前一句假设 B = 0.5） |
| `gap_phase_noise`：对 B = 0.5 的波而言，观测到的分布超过了误差与 47 pc 弥散所能造成的 | GAP | reconstructed | — |
| `stat_b`：最佳拟合 B = 0.84（编码为 84 个百分之一） | STAT | stated: "We find a best fit value for B = 0.84." | 方法；扩展数据表 2 第 (5) 列，B 自由的星团拟合 |
| `gap_vz`：星团的 z–v_z 图样（以及由此得到的相位、B 的后验与图 1 拟合）属于波本身，而不是样本、其视向速度覆盖、太阳运动零点或离群与加权的选择 | GAP | reconstructed | Zhu 等 2024，arXiv:2402.15346；Bobylev 等 2025，arXiv:2503.21019 |
| `mod_prefer`：B 大于 0.75（我们对"更接近 1"的理解）+ 排除驻波（+ 稳健的 v_z）⇒ 行波相对驻波受到偏好 | MOD | stated: "When fitting a mixture model that allows for superpositions of a traveling and a standing wave, we find that a traveling wave is strongly preferred over a standing wave (see Methods)." | 正文第 2 页 |
| `stat_bequiv`：B = 1 与 B 自由拟合得同样好 | STAT | stated: "Thus, both models are an equivalently good fit to the data, while the realization with fixed B = 1 is slightly preferred." | 方法（ΔlnZ = ln Z₂ − ln Z₁ ≈ 1） |
| `mod_b1`：偏好行波 + 拟合同样好 ⇒ 可以取 B = 1 | MOD | stated: "We therefore conclude that the Wave's motion is of first order consistent with a traveling wave, implying that we can set B = 1 in all further performed calculations" | 方法 |

**其他解释。**

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 驻波（波节固定，z 与 v_z 同相） | `stat_phase` + `mod_standing` + `gap_phase_noise` | 是，由相位论证；没有给出分布的统计量 |
| 驻波的相位看起来分散，因为在波节附近 z 与 v_z 都接近零，相位由 47 pc 弥散与 v_z 误差决定 | `gap_phase_noise` | 否 |
| 相位分布与 B = 0.84 是星团样本（离群模型、核密度权重、视向速度覆盖、太阳运动零点）的产物 | `gap_vz` | 部分：检查了太阳高度、倾斜、引力势与另一个星团星表 |
| 中间的混合（0.5 < B < 1） | 编码的说法（"相对驻波受到偏好"）不排除它 | 部分：取 B = 1 的理由是 B = 1 与 B 自由拟合得"同样好" |

**推理（Lean 摘录）。**

```lean
have hb : v.b_x100 = 84 := p .stat_b
have ns : ¬ v.Standing := fun s => p .mod_standing s (p .gap_phase_noise) (p .stat_phase)  -- GAP
have pt : v.PreferTW := p .mod_prefer (by omega) ns (p .gap_vz)                                     -- GAP
have b1 : v.B1OK := p .mod_b1 pt (p .stat_bequiv)
```

**评述。** 两条路径都用与拟合相同的星团速度。相位 φ_k 由同样的 z_k 与 v_z,k 算出，用同样的离群模型与权重；B = 0.84 来自同一个似然函数；所以凡是威胁 v_z 图样（`gap_vz`）的，也威胁这一环节。相位论证还有第二个弱点：K24 依据的那句话（"the phases φk should be roughly constant"）是无噪声模型的性质，而检验用在观测相位上。在驻波的波节附近，z 与 v_z 都趋于零，它们之比的反正切由 47 pc 弥散与 v_z 误差决定，可以取任何值；所以即使 B = 0.5 也预期会有一些分布，而 K24 没有给出统计量（也没有模拟预期的分布）来表明观测到的分布超过了它（`gap_phase_noise`）。"强烈"一词在 K24 中没有定量支持：对 B 报告的唯一证据比 ΔlnZ ≈ 1 比较的是 B = 1 与 B 自由（不是行波与驻波），并被称为"同样好"；B 的后验区间远高于 0.5，但先验在 1 处截断，后验有界，它与 0.5 的距离不是显著性。B 的阈值 0.75 是我们对"更接近 1"的理解；0.5 与 0.84 之间的任何阈值都给出同样的结果。取 B = 1 的一步用到的证据比，其印出的符号与所述的偏好不一致（第一部分 1.4）；无论哪个正确，该比值都约为 1，"同样好"成立。

#### 2.4 环节 D · 波在振荡

*概述。* 取 B = 1 后，形状决定 v_z 的极好拟合（环节 B、C），加上示踪天体就是波本身（环节 A），被解读为振荡。正文的说法带保留（"The fit shown as a solid black line in Figure 1 ... indicates that the Radcliffe Wave oscillates through the Galactic plane like a traveling wave"）；方法部分的说法是明确的（"In the case of the z-component, we find that the Radcliffe Wave oscillates like a traveling wave driven by the Milky Way's gravitational acceleration"），我们引用的是后者。

**前提。**

| 前提（Lean 构造子） | 标注 | 出处性质 | 论文出处 |
|---|---|---|---|
| `gap_vz`（同环节 C） | GAP | reconstructed | Zhu 等 2024；Bobylev 等 2025 |
| `gap_shear`：在示踪天体覆盖的时间内，一列连贯的行波（一条相位规律 Λ(s)、一个刚体漂移）是恰当的描述 | GAP | reconstructed | Li、Zhou & Chen 2024，arXiv:2410.14603 |
| `mod_osc`：连贯的示踪天体 + 形状决定 v_z + 良好的 B = 1 拟合 + 已取 B = 1（+ 两个缺口）⇒ 波像行波那样振荡 | MOD | stated: "In the case of the z-component, we find that the Radcliffe Wave oscillates like a traveling wave driven by the Milky Way's gravitational acceleration." | 方法，Full Spatial and Kinematic Model（正文第 2 页：拟合"indicates"这一点） |

**其他解释。**

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 静态褶皱（static corrugation，没有竖直运动的冻结起伏） | `stat_twfit`（约 14 km/s、幅度符合预言的 v_z 图样） | 隐含地：图 1b 显示了 v_z 波；而且在 `mod_grav` 之下，离银道面 220 pc 又没有支撑的结构不可能静止 |
| 是驻波或混合，而不是行波 | `mod_b1`（通过 `mod_osc` 的前件"已取 B = 1"） | 是（环节 C） |
| 竖直速度与位置不同步（v_z 振荡"与竖直坐标不同步"，沿波呈偶极状（dipole-like）梯度；z 与 v_z 的波长不同） | `gap_vz` | 否（Zhu 等 2024 与 K24 在同一周出现在 arXiv；Bobylev 等 2025 更晚） |
| 90° 关系由离群模型（剔除全部英仙座与金牛座、按分量 √3σ 的软截断）、核密度权重、少数猎户座与仙王座星团，或太阳运动零点（w☉ = 7.8 km/s，即 K24 引用的 Kerr & Lynden-Bell 1986 标准太阳运动；Schönrich 等 2010 给出 7.25 km/s；从每个 v_z 中扣除）造成 | `gap_vz` | 部分：检查了太阳高度、倾斜、引力势与另一个星团星表；没有改变离群阈值、权重与太阳运动 |
| 银河系的剪切把波拉长（约 45 Myr 内拉长到几乎两倍，即半个振荡周期），单一相位规律与刚体漂移是过度简化 | `gap_shear` | 部分：K24 提到在"几千万年"上云的瓦解与相混合，并指出其时间无关近似在约 40 Myr 后达到噪声水平，但仍拟合单一的连贯波 |

**推理（Lean 摘录）。**

```lean
have o : v.Oscillating :=
  p .mod_osc c z (p .stat_twfit) b1 (p .gap_vz) (p .gap_shear)                              -- two GAPs
```

**评述。** "振荡"的经验内容比听起来窄。在 `mod_grav` 之下，离银道面 220 pc 的任何一团物质都必然在竖直方向运动；数据增加的信息是：测得的 v_z 具有已知引力势所预言的大小（约 14 km/s）与四分之一波长的错位。这是真正的检验，因为在行波拟合中速度幅度不是自由参数。但"像行波那样"依赖环节 C，而且还有两件事 K24 没有表明。(i) v_z 图样必须属于波本身而不是样本：星团的 v_z 依赖 Gaia 自行加上视向速度，而有些星团的视向速度很稀少（K24 把超过 50 km/s 的星团当作异常剔除），依赖采用的太阳运动，又依赖一个会整片剔除某些区域的软离群模型。Zhu 等 2024 用 APOGEE-2 恒星、以及另外用云的视向速度配合 YSO 自行，发现 v_z 振荡"与竖直坐标不同步"（约 5 km s⁻¹ kpc⁻¹ 的偶极状梯度）；Bobylev 等 2025 发现 z 与 v_z 的波长不同。(ii) 单一的连贯行波是理想化：K24 自己说波在几千万年上很可能受相混合影响，Li 等 2024 认为剪切使刚体描述在半个周期上成为过度简化。快照拟合仍然可以表明波的各段按引力的预言上下运动；(ii) 威胁的是"行波"的解读、相速度与刚体漂移。两点都来自后来的文献或我们的分析，所以是 `GAP`。

#### 2.5 环节 E · 用波称量银盘

*概述。* 取 B = 1 后，K24 放开三个引力势参数（ω₀、μ₀、r₀），对波拟合（扩展数据表 2 第 (7) 列）：ω₀ = 68 (+8/−7) km s⁻¹ kpc⁻¹，与采用值 74 一致。等温层（isothermal sheet）把 ω₀ 换算成银盘中平面密度 ρ₀ = ω₀²/(4πG) = 0.085 M☉ pc⁻³；减去重子得到与零相容的暗物质密度；同一引力势给出太阳的竖直周期 95 Myr。

**前提。**

| 前提（Lean 构造子） | 标注 | 出处性质 | 论文出处 |
|---|---|---|---|
| `stat_omega`：放开引力势后 ω₀ = 68 (+8/−7)、μ₀ = 1.4、r₀ = 3.6 kpc | STAT | stated: "We find a median value and 1σ errors (computed using the 16th, 50th and 84th percentiles of the samples) of ω0 = 68 +8 -7 km s-1 kpc-1" | 方法；扩展数据表 2 第 (7) 列；上下标已展平 |
| `mod_sheet`：ρ₀ = ω₀²/(4πG)（等温层） | MOD | stated: "Following the vertical density model of an isothermal sheet based on a Maxwellian vertical velocity distribution, we calculate the parameters defining the Galactic mass distribution" | 方法 |
| `gap_prior`：ω₀ 的后验（以及由此得到的 ρ₀、暗物质密度与太阳周期的中心值与误差）由波的数据决定，而不是由依据初步拟合设定的先验决定 | GAP | reconstructed | — |
| `mod_weigh`：振荡 + 拟合的 ω₀ + 等温层（+ 缺口）⇒ 波测得本地引力势与太阳的周期 | MOD | stated: "By treating the Radcliffe Wave as a coherently oscillating structure, we can derive its motion independently of the local Galactic mass distribution, and directly measure local properties of the Galactic potential as well as the Sun's vertical oscillation period." | 摘要 |

**其他解释。**

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 拟合的 ω₀ 反映的是先验而不是波 | `gap_prior` | 部分：K24 说拟合"without prior knowledge about the vertical gravitational potential"，但其先验是"based on initial fits" |
| 数据无法区分采用的引力势与拟合的引力势 | （影响误差棒；不是单独的前提） | 明说：固定与放开的引力势"同样好"（ΔlnZ ≈ 1） |
| 波的竖直运动不是自由振荡（环节 D 不成立） | `mod_weigh` 需要 `Oscillating` | ——（继承环节 C 与 D 的缺口） |

**推理（Lean 摘录）。**

```lean
have w : v.Weighs := p .mod_weigh o (p .stat_omega) (p .mod_sheet) (p .gap_prior)         -- GAP
exact ⟨o, pt, w⟩
```

**评述。** 这一测量依赖环节 A–D（它用到 `Oscillating`），所以那些缺口都会传递过来。它自身的弱点是先验。ω₀ 的先验 ln(ω₀/(km s⁻¹ pc⁻¹)) ~ N(−2.4, 0.17) 中心约为 91 km s⁻¹ kpc⁻¹，宽约 17%，而后验宽约 11%，比先验中心低约 1.7σ（按对数）：数据把 ω₀ 往下拉，先验往上拉，所以中心值与误差棒都是两者的折中，不只来自数据。先验是"依据初步拟合"设定的，大概用的是同样的数据，这会把数据算两次、使后验过窄（r₀ 完全由先验决定：后验宽度等于先验宽度）。固定（74）与放开（68）的引力势拟合得"同样好"（ΔlnZ ≈ 1），所以数据分辨不出 ω₀ 10% 的变化；这与给出的 ±11% 相符，但这意味着波是在确认标准引力势，而不是取代它。暗物质密度（0.001 +0.024/−0.021 M☉ pc⁻³）是两个几乎相等的数之差（总量 0.085 与重子 0.084），既与零相容，也与常规的约 0.013 相容；太阳周期（95 Myr）在同一个拟合的引力势中算出，继承了它的先验。

#### 2.6 径向漂移与本地泡（只讨论，不编码）

K24 在扣除银河系自转后拟合一个刚体的盘面内速度：v_x,plane = −3.9 (+2.6/−2.7)、v_y,plane = 3.1 (+2.7/−2.6) km/s，即约 5 km/s 沿径向远离银心（"we find evidence that the Radcliffe Wave is drifting radially outward from the Galactic Center with a velocity of 5 km s-1"）。每个分量离零只有约 1.2–1.5σ，所以"证据"并不强；漂移假设了 `gap_shear` 所质疑的刚体运动；与 Upper Centaurus Lupus 和 Lower Centaurus Crux 星团的联系只是方向，不是回溯（K24：精确的回溯"is beyond the scope of this work"）。Bobylev 等 2025 得到约 10 km/s。由于一个文件只有一个结论，而这一说法不影响振荡的论证，所以不编码；第三部分可以检验它。

#### 2.7 Lean 检查发现的问题

1. **主要结果：`explicit_insufficient`，五个缺口。** 没有 `[implied]` 前提：凡不是缺口的前提都是 K24 明说的（引力势参数作为明说的 `MOD` 前提进入：这是 K24 自己的取参步骤），所以 `stated_insufficient` 与 `explicit_insufficient` 用的是同一个反例模型。缺口是：同处一地的星团诞生于波中，K24 只是提示（`gap_born`）；z–v_z 图样属于波本身，而不是星团样本、其离群处理与太阳运动零点（`gap_vz`；Zhu 等 2024 发现 v_z 振荡与竖直坐标不同步，Bobylev 等 2025 也提出疑问）；对驻波而言，观测到的相位分布超过了噪声所能造成的（`gap_phase_noise`）；尽管有剪切，一列连贯的行波仍是恰当的描述（`gap_shear`；Li 等 2024 对此提出质疑）；引力势的拟合由数据而不是先验决定（`gap_prior`）。
2. **缺口的位置：结论的每一部分都依赖缺口。** (1) 与 (3) 通过环节 A 需要 `gap_born`。(2) 是行波而不是驻波，需要 `gap_phase_noise` 与 `gap_vz`，因为它的两项依据（相位分布与 B 的后验）用的是同样的星团速度与同一个拟合。(1) 振荡在 (2) 之后——图 1 的拟合是 B = 1 的实现，在混合模型拟合之后才采用——所以继承这两个缺口，并加上 `gap_shear`。(3) 称量银盘用到振荡，并加上 `gap_prior`。"强烈偏好"在 K24 中没有定量支持（唯一的证据比是 B = 1 对 B 自由的 ΔlnZ ≈ 1；B 的后验受先验在 1 处截断）。
3. **各缺口影响什么。** `gap_vz` 影响全部三部分。`gap_phase_noise` 关系到排除驻波的唯一路径。`gap_shear` 对行波解读与漂移的影响大于对局部上下运动的影响。`gap_prior` 既影响 ω₀、ρ₀、暗物质密度与太阳周期的中心值（先验把 ω₀ 往上拉），也影响它们的误差棒。
4. **在这种编码下 26 个前提都是必要的**，没有多余的（每个前提都在单一链条上；K24 通向"连贯"的第二条路径，即只用云、只用星团与联合拟合的一致性，没有编码；B = 0.84 作为明说的偏好的前件进入，而不是排除驻波的第二条路径）。
5. **相容性**（`consistent`）在这里有一点分量：`mod_standing` 是否定形式，模型需要波不是驻波。
6. **编码与引文的差别。** 五条明说的推理规则（`mod_transfer`、`mod_prefer`、`mod_b1`、`mod_osc`、`mod_weigh`）以及 `mod_shape`、`mod_pot`、`mod_standing` 带有额外的前件（缺口或前面的步骤），所以比引文弱；`mod_standing` 还把关于无噪声模型的陈述用于观测相位，这正是它带有 `gap_phase_noise` 的原因。没有带保留措辞的句子被编码为明说的蕴涵式：带保留的"诞生"一步是缺口（`gap_born`），振荡与行波偏好则引用 K24 的明确表述（"we find that ..."），并注明带保留的版本。"B 更接近 1"的阈值是我们的理解（大于 0.75；0.5 与 0.84 之间的任何阈值都给出同样的结果），只作为前件使用。
7. **局限。** Lean 检查的是我们编码下的逻辑结构，不是每个前提内部的动力学或统计；拟合优度（"excellent fit"）与 CO 的一致在 K24 中只是图，作为原子命题进入。

### 第三部分 · 本项目可检验或探索的环节

本部分写于任何拟合之前（2026-11-21），是研究预注册（README 第 1–4 节）的来源，具体阈值由预注册确定。写作时我们看过的内容：论文（arXiv v1，含方法部分），以及通过受守卫的取数通道读到的两张公开表的列名、行数与取值范围。星团表有 125 行，列为 `name`、`reference`、`x, y, z, vx, vy, vz` 及其误差（`sigma…`）、`age`（百万年，0–28 的整数）与 `inlier` 标记（89 个内点（inlier），36 个离群点（outlier））；CO 表有 79 个云，列为 `x, y, z` 及其弥散、`l, b, d`，以及 ¹²CO 速度 `vr` 与其第 16/84 百分位。没有拟合任何模型。

**数据与开销。** 两张表，10,888 与 5,286 字节（Harvard Dataverse，CC0），用 `ctx.http` 获取；不取其他数据。拟合用 emcee 与最大似然（maximum likelihood）优化器，都已安装（K24 用的是 1000 个活点（live points）的 dynesty，我们不安装它）。一次似然计算要对约 200 个天体分别找模型曲线上最近的点；在沿 s 约 2000 个格点上，这是约 4 × 10⁵ 个距离的向量化运算。下面的检验大约需要 20–40 次拟合（T6 的每个稳健性变体要重新拟合两三个模型），另加 T3 与 T4 的模拟。我们预计每次拟合需要几分钟，整个运行在单核上需要几小时；在短运行中实测后，连同拟合与模拟的确切次数写进预注册。运行要等到没有其他研究在运行时进行。

**哪些能精确复现，哪些不能。** K24 没有给出核密度带宽（"a few percent of the total length of the Wave"），也没有说明平面曲线的参数如何映射为 s；我们在预注册中固定这些选择，并作为稳健性检验加以变化。似然取 K24 的式 10–13：星团用 4 维向量 (x, y, z, v_z/ω₀)，云用 3 维向量；核密度权重之和等于天体数（K24：权重"are set to sum to the number of"云，星团同样）；离群函数 C(x) = (Σₙ tanh(xₙ²))^½；所有分量共用弥散 σ = 47 pc；先验取扩展数据表 1。检验必须照顾模型的两个特点：B = 1 时 ω₀t 只以 ω₀t + φ 的形式出现，所以像 K24 一样固定为 0；B = 0.5 时 z = ζ sin(2πΛ + φ) cos ω₀t、v_z = −ζω sin(2πΛ + φ) sin ω₀t，ω₀t 分别决定 z 与 v_z 的振幅，所以驻波比行波多一个有效参数，两者不能当作参数个数相同来比较。一般地，(z, v_z/ω) 等于一个 2 × 2 矩阵乘以 (sin θ, cos θ)（θ = 2πΛ + φ），矩阵的行列式为 ζ²(2B − 1)；它的符号即传播方向，不能由 ζ、φ 或 ω₀t 改变，所以 B 与 1 − B 是不同的波。局部地看，驻波（秩为 1 的矩阵）比 B 自由的模型少一个参数，行波（缩放乘以旋转）少两个，这决定了 T3 中的自由度。

| 环节（第二部分） | 前提或缺口 | 检验或探索 | 做法 | 数据 | 结果标签（阈值在预注册中固定） |
|---|---|---|---|---|---|
| B、D | `stat_twfit` | **T1 · 复现拟合。** 只用星团（第 (4) 列）与云 + 星团（第 (6) 列），B = 1、ω₀t = 0，K24 的似然与先验 | emcee；把中位数与 16–84% 区间同扩展数据表 2 比较；把我们的内点集合同表中的标记比较 | 16 KB | 复现 / 部分复现 / 未复现，依据 A、p、δ、s₀、γ、φ 中有几个落在 K24 的 1σ 之内 |
| C | `stat_b` | **T2 · B 自由**（第 (5) 列），ω₀t 自由 | 同 T1，B ~ U(0, 1)（与 K24 相同），在 [0, 1] 上概括，不折叠；B 与 1 − B 是向相反方向传播的波，数据能把两者区分开（见上文） | 同上 | B 的区间与 0.84（+0.07/−0.06）比较；报告 B 大于 0.95 的后验质量，以及 P(B < 0.5)，用来检查传播方向 |
| C | `mod_prefer`、"strongly" | **T3 · 把行波与驻波当作嵌套模型比较。** 在 T2 的 B 自由模型中，分别在 B = 0.5 与 B = 1 处求剖面似然（profile likelihood），与对 B 取最大的似然比较 | 最大似然拟合（先验的支撑集只作为边界，不用其形状；但 ω₀t 按周期处理，不截断；同时报告最大后验（MAP）值）；B = 0.5 是内点，ω₀t 在那里仍可辨识，所以 2ΔlnL 按 1 个自由度的 χ² 分布；B = 1 时 ω₀t 并入 φ，B = 1 的模型少两个参数，所以按 2 个自由度的 χ² 分布；两个参考分布都用参数自助法（parametric bootstrap）模拟检查，分别从 B = 0.5 与 B = 1 的拟合抽取（各至少 100 个，次数按实测运行时间确定）；报告所有拟合的内点集合及其重叠 | 同上 | 强烈排除驻波 / 排除驻波 / 不排除；另外单独给出：纯行波（B = 1）受到否定 / 未受否定 |
| C | `gap_phase_noise` | **T4 · 相位的弥散是否超过噪声？** | 模拟：至少 1000 个驻波，取自 T3 中 B = 0.5 的拟合，模拟星团从观测星团在模型上的位置出发；噪声：47 pc 的弥散加在全部四个分量上（x、y、z 与 v_z/ω₀，即 v_z 上约 3.5 km/s），再加每个星团的测量误差；一个变体改为对 B = 0.5 拟合本身的残差重抽样；每个模拟星团在 B = 0.5 拟合的曲线上重新求最近点（s_k，从而 ω_k；功效模拟也如此，与对数据的做法相同），但不重新拟合全局参数；观测的 R 用的是对数据拟合的参数（B = 0.5 的拟合会调整 ω₀t 使相位对齐），而模拟不重新拟合，所以这个检验在排除驻波一方是保守的；星团：B = 0.5 拟合的全部内点，包括波节附近的；统计量：φ_k = arctan(z_k ω_k / v_z,k) 的周期是 π，所以用圆统计量 R = \|e^(2iφ_k) 的平均\|，驻波的 φ_k 恒定、R 接近 1，相位分散时 R 小；p = R 不大于观测值的驻波模拟所占比例；功效（power）：对取自 B = 1 拟合与 B 自由最佳拟合的模拟计算同一统计量 | 同上 | 相位排除驻波 / 不排除 / 无法判定（在所选阈值下的功效低于预注册中固定的数值时） |
| C、D | `gap_vz`（这批数据能触及的部分） | **T5 · 不预设 z 与 v_z 关系地看两者。** 基线与 Λ(s) 取自只用云的拟合（第 (3) 列，只有位置，没有速度）；每个星团的 s 由在 x–y 平面上向该基线投影得到，最近点落在基线端点的星团剔除并计数；星团集合为全部 125 个（内点的选择在 T6 中变化），所以选择中不含任何速度；分别拟合 z(s) 与 v_z(s)，各有自己的振幅、相位与波长缩放因子 k（Λ → kΛ） | 对星团做自助法（bootstrap），在自助法内部从只用云的拟合的后验中抽取 Λ；相位差在一个说明的参考 s（星团的加权平均 s）处计算，并与振幅比 A_v/(ω A_z) 一起报告（ω 也在该参考 s 处计算）；只有 90° 相位差不足以说明是行波（ω₀t = 0 时任何 B 都给出 90°），还要求振幅比接近 1；相位差的符号（+90° 或 −90°）给出传播方向 | 同上 | "90° 相位差且振幅比接近 1"：支持（相位差的区间包含 90° 且不包含 0° 与 180°，振幅比的区间落在预注册中固定的、围绕 1 的范围内，例如 [0.7, 1.4]）/ 不支持（相位区间不包含 90°，或振幅比的区间不包含 1）/ 无法判定（其他情况：数据噪声太大，无法分辨）。波长：一致（k_z/k_vz 的区间落在预注册的围绕 1 的范围内）/ 不同（区间不包含 1；Bobylev 等 2025 报告了不同的波长）/ 无法判定（其他情况） |
| C、D | `gap_vz` | **T6 · T3、T4 与 T5 的稳健性** | 离群规则（K24 的按分量 √3σ、3σ、不用离群模型）；不用核密度权重，以及另外两个带宽；w☉ 取 7.8 与 7.25 km/s；去掉猎户座；每次去掉一个来源星表（`reference`）；只用 σ(v_z) 低于中位数的星团 | 同上 | 稳健（所有变体中 T3、T4 与 T5 的标签都不变）/ 脆弱（列出改变标签的变体） |
| A | `stat_co` | **T7 · CO 检验对 v_z 能说明多少？** | 把 T1 的模型投影到每个云的视线方向（式 14），与 `vr` 比较；平面内速度取自星团的 v_x、v_y，用带 Oort 常数的平直自转曲线扣除银河系自转；误差取自第 16/84 百分位列，加一个内禀弥散，对每个版本分别拟合；版本为 T1 的模型、令 v_z = 0、B = 0.5 的拟合；预期灵敏度：\|sin b\| 多数小于 0.2，v_z 对 v_LSR 的贡献最多约 3 km/s，所以"无法区分"是一个很可能的结果 | 5 KB | CO 偏好行波 / CO 无法区分（各版本之间的 Δχ²） |
| E | `gap_prior` | **T8 · 引力势是否由数据决定？** 放开 ω₀、μ₀、r₀（第 (7) 列），分别用 K24 的先验与宽的均匀先验：ω₀ 30–150 km s⁻¹ kpc⁻¹、μ₀ 0.3–3 kpc⁻¹、r₀ 1–10 kpc | 比较 ω₀ 的后验；推导 ρ₀ = ω₀²/(4πG) 与太阳的竖直振荡周期；4 维向量中 v_z/ω₀ 的除数随拟合的 ω₀ 变化（我们对 K24 的理解），一个变体把它固定为 74 | 16 KB | 由数据决定（后验比先验窄且对先验不敏感）/ 由先验决定 / 部分由数据决定 |

**只做探索、不下判决**（对话探索的入口，见 README 第 8 节）：

- *年龄与在波中诞生*（`gap_born`、`mod_age`）：把星团在 10 与 20 百万年处分组；年龄较大的星团在 z 或 v_z 上相对 T1 模型的弥散是否更大？弥散随年龄增大符合"与气体分离"的预期，但不能证明或否定共同起源。
- *是一个相干的波吗？*（`gap_shear`）：对 CMa–猎户座一半与仙王座–天鹅座一半分别拟合相位律，并与单一相位律比较。剪切（shear）在数千万年上起作用，而数据只是一个快照，所以这只能说明现在用一个 Λ(s) 是否够用，不能说明过去是否如此。
- *径向漂移*（第二部分 2.6）：扣除银河系自转后复现平面内的整体速度（我们会用带 Oort 常数的简单平直自转曲线，而不是 K24 的引力势），并看它对自转模型的依赖。

**本研究不能检验的。** 独立的速度数据（Zhu 等 2024 用 APOGEE-2 恒星，以及云的视向速度配合年轻恒星体（YSO, young stellar object）的自行；Bobylev 等 2025 用了不同的星团选择）：获取它们需要新的服务器端查询，作为开放问题留待以后。波的起源物理、数千万年内云的瓦解与相混合（phase mixing），以及本地泡的回溯，不在本研究范围内。

### 术语表

| 术语 | 含义 |
|---|---|
| Radcliffe 波（Radcliffe Wave） | 太阳附近约 2.7 kpc 长、形如阻尼正弦波的致密气体云链（Alves 等 2020） |
| 行波（travelling wave） | 波峰移动的波；位置与速度图样相差 90° |
| 驻波（standing wave） | 波节固定的波；位置与速度的空间图样相同 |
| B | K24 的混合参数：1（或 0）= 行波，0.5 = 驻波 |
| 非谐振子（anharmonic oscillator） | 频率随振幅变化的振子（此处：振幅越大越慢） |
| 相速度（phase velocity） | 波峰单位时间移动的距离，即波长除以时间周期 |
| 本地静止标准（local standard of rest, LSR） | 太阳位置处圆轨道的参考系 |
| ¹²CO | 一氧化碳，其 2.6 毫米谱线示踪分子气体及其视线速度 |
| 贝叶斯因子（Bayes factor）、ΔlnZ | 贝叶斯因子是两个模型证据（evidence）之比，ΔlnZ 是它的自然对数；|ΔlnZ| ≈ 1 表示证据差别不大，偏好哪个模型由符号（取决于约定）决定 |
| 银盘中平面密度 ρ₀（midplane density） | 太阳附近银道面上的总质量密度（恒星、气体、暗物质） |

### 研究进展

按时间倒序。

- 2026-11-21：第三部分初稿（八项检验 T1–T8 与三项探索；读取了两张公开表的列与行数，未做拟合；闸门 1 审查：T3 改为嵌套模型的剖面似然检验，因为 ω₀t 自由时驻波多一个有效参数；T4 的噪声加在全部四个分量上，用 2φ_k 的圆统计量并检查功效；T5 的 Λ(s) 取自只用云的拟合，两个波长各自放开；第二轮：B 不折叠（B 与 1 − B 向相反方向传播），B = 1 按 2 个自由度的 χ² 分布（那里 ω₀t 并入 φ）并做自助法检查，T4 对每个模拟重新求最近点，T5 报告振幅比且星团选择不含速度；第三轮：T5 的标签增加"无法判定"，宽区间不能算作支持）；w☉ = 7.8 km/s 改为 K24 引用的 Kerr & Lynden-Bell 1986（原误作 Schönrich 等 2010）。
- 2026-11-21：第二部分闸门 2 审查：不再把带保留措辞的句子编码为明说的蕴涵式；星团诞生于波中（K24："suggesting"）成为新缺口 `gap_born`；振荡一步改引方法部分明确的"we find that"；"B closer to 1 indicates"前提并入明说的偏好；26 个前提、五个缺口。
- 2026-11-21：第二部分闸门 1 审查：行波相对驻波现在也依赖缺口（同样的星团 v_z，以及在驻波波节附近可能由噪声造成的相位分布：新增 `gap_phase_noise`）；振荡的结论改在取 B = 1 之后（图 1 是 B = 1 的拟合）；引力势参数作为 `LIT` 前提，x–y 选样作为前提，CO 一致改标 `STAT`；27 个前提、四个缺口；中文术语统一为"银盘中平面密度"。
- 2026-11-21：第二部分初稿：四个环节，24 个前提用 Lean 4 检查；`explicit_insufficient`，三个缺口（z–v_z 图样与 Zhu 等 2024 的矛盾；单一连贯的波与剪切，Li 等 2024；引力势拟合受先验影响）；行波相对驻波由明说的前提即可推出。
- 2026-11-21：闸门 1 审查：B 的后验不再读作反对纯行波的证据（先验在 1 处截断）；改正离群判据、先验、坐标轴、太阳周期的估算、猎户座离群比例与 Zhu 等的数据来源；补充术语英文。
- 2026-11-21：第一部分初稿（第二、三部分随后）。

### 来源

- Konietzka 等 2024，Nature 628, 62–65，doi:10.1038/s41586-024-07127-3，[arXiv:2402.12596](https://arxiv.org/abs/2402.12596)（本文研究的论文；读的是 arXiv v1 全文）[V]。
- 数据：Harvard Dataverse doi:10.7910/DVN/XSCB9N（星团）与 doi:10.7910/DVN/Q7F4PC（¹²CO）[V 仅元数据]。
- Alves 等 2020，Nature 578, 237，arXiv:2001.08748 [V 摘要]。
- Zhu 等 2024，ApJ 971, 167，arXiv:2402.15346 [V 摘要；S 卷号]。
- Li、Zhou & Chen 2024，arXiv:2410.14603 [V 摘要]。
- Bobylev、Ikhsanov & Bajkova 2025，Astrophys. Bull. 80(2)，arXiv:2503.21019 [V 摘要]。
- McKee、Parravano & Hollenbach 2015，ApJ 814, 13（本地重子；按 K24 的引用）。
