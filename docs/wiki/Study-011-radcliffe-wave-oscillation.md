# Is the Radcliffe Wave waving? Young clusters and a Galactic oscillation

[English](#english) · [中文](#中文)

*Paper: Konietzka, Goodman, Zucker, Burkert, Alves, Foley, Swiggum, Koller, Miret-Roig 2024, "The Radcliffe Wave is oscillating", Nature 628, 62–65, doi:10.1038/s41586-024-07127-3, arXiv:2402.12596. Study:
[`studies/011-m11-radcliffe-wave-oscillation`](https://github.com/sudoghut/astrolab/tree/main/studies/011-m11-radcliffe-wave-oscillation) (web page: [online](https://sudoghut.github.io/astrolab/studies/011-m11-radcliffe-wave-oscillation/web/)).
Status: planned. Last updated: 2026-11-21 (see the changelog at the end). The source of this page lives in the main repository at
[`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki); edit it there.*

*中文标题：Radcliffe 波在振荡吗？年轻星团与银河系中的竖直振荡。状态：计划中。论文：Konietzka, Goodman, Zucker, Burkert, Alves, Foley, Swiggum, Koller, Miret-Roig 2024，Nature 628, 62–65，doi:10.1038/s41586-024-07127-3，arXiv:2402.12596。研究：[`studies/011-m11-radcliffe-wave-oscillation`](https://github.com/sudoghut/astrolab/tree/main/studies/011-m11-radcliffe-wave-oscillation)（网页：[在线版](https://sudoghut.github.io/astrolab/studies/011-m11-radcliffe-wave-oscillation/web/)）。最后更新：2026-11-21（见文末"研究进展"）。本页源文件在主仓库的 [`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki) 中，请在那里修改。*

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
(something that moves up and down through the plane), one needs **velocities**, in particular the
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
  - clusters with radial LSR velocities above 50 km/s removed as kinematic anomalies;
  - selection on the x–y plane only (top-down view): clusters within ±5 times the Wave's radius
    (47 pc, i.e. ±235 pc) of the best-fit dust model, with **no a priori cut in height z** — so the
    vertical pattern is not built in by the selection;
  - the Lacerta OB1 association is removed because it is vertically and kinematically distinct;
  - a check against the Hunt & Reffert 2023 Gaia DR3 cluster catalogue (youngest clusters only)
    reportedly has no effect.
  Velocities are converted to the local standard of rest (LSR, the frame of a circular orbit at the
  Sun) with the solar peculiar motion (u☉, v☉, w☉) = (10.0, 15.4, 7.8) km/s, giving (v_x, v_y, v_z).
  The number of clusters is not stated in the text; the public table (Harvard Dataverse
  doi:10.7910/DVN/XSCB9N, file `Radcliffe_Wave_stellar_clusters_Konietzka2024.tab`, 10,888 bytes,
  CC0) has 15 columns: name, reference, x, y, z, v_x, v_y, v_z with errors, age and an inlier flag
  (row count not given in the metadata; of order 10² from the figures — to be read by the study).
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
  `Radcliffe_Wave_CO_analysis_Konietzka2024.tab`, 5,286 bytes, CC0, 13 columns (name, x, y, z,
  x/y/z spreads, l, b, d, rv, rv16, rv84).

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
length of the density, and μ₀ an inverse vertical scale height. These three numbers are not fitted to
the Wave at first: they are obtained by a χ² fit of eq. 1 to an existing Milky Way model (Allen &
Santillan 1991 with the updated parameters of Irrgang et al. 2013) over r = 7–10 kpc and |z| ≤ 300 pc:
**ω₀ = 74 km s⁻¹ kpc⁻¹, r₀ = 3.7 kpc, μ₀ = 1.3 kpc⁻¹**, implying a local density ρ₀ ≈ 0.1 M☉ pc⁻³
and scale height z₀ = 1/(√6 μ₀) = 314 pc (literature: 0.097 ± 0.013 M☉ pc⁻³ and 280 (+70/−50) pc,
McKee et al. 2015). Energy conservation then gives the period T of a cloud that rises to z_max
(eq. 2), and with an elliptic integral K an analytic frequency ω(z_max, r) (eq. 3), which falls as
the amplitude grows. Because the Wave crosses different Galactocentric radii, r and z_max are
functions of the position s along the Wave, so ω = ω(s). The potential is assumed stationary; tilts,
the Galactic warp and radial "breathing" waves are argued to be negligible.

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
function C (a tanh truncation): a cluster is an outlier if any component exceeds tanh(3), i.e. lies
beyond 3σ. Clouds use a 3D version (eq. 11). Sampling is done with the nested-sampling code dynesty
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
form one spatially and kinematically coherent structure. The best fit is drawn in Figure 1 (the
x–y frame rotated anticlockwise by 62° so that x runs along the Wave).

Derived numbers (main text and Methods):

- **Maximum amplitude ~220 pc; mean wavelength ~2 kpc** (about 2000 pc, ranging from ~4000 pc near
  CMa OB1 to ~400 pc near Cygnus X, from eq. 7). Our check: with column (6), λ(0) = p ≈ 4.78 kpc,
  λ(0.3 kpc) ≈ 3.9 kpc, λ(2.4 kpc) ≈ 0.34 kpc, and the average of λ(s) over 0–2.4 kpc is ≈ 2.1 kpc,
  consistent with K24's description (our reading; the s-range of the data is assumed).
- **Maximum vertical velocity ~14 km/s.**
- **Travelling, not standing.** B = 0.84 (+0.07/−0.06) with a flat prior on [0, 1]. A separate fit
  with B fixed to 1 gives a log Bayes factor ΔlnZ = ln Z₂ − ln Z₁ ≈ 1 (Z₁: B = 1, Z₂: B free); K24
  says "both models are an equivalently good fit to the data, while the realization with fixed B = 1
  is slightly preferred", and sets B = 1 thereafter. The standing wave (B = 0.5) is excluded by a
  separate argument: for B = 0.5 the per-cluster phases φ_k = arctan(z_k ω_k / v_z,k) should be nearly
  constant along s (varying by at most ~0.03π), but they sweep the whole range −π/2 to π/2. In the
  main text this becomes "a traveling wave is strongly preferred over a standing wave".
- **Phase velocity** (the speed at which the crests appear to move, λ(s)/T(s)): from ~40 km/s near
  CMa OB1 to ~5 km/s near Cygnus X, crests moving right to left as seen from the Sun. Explaining this
  order-of-magnitude change by a change in local density would need ρ₀ to vary by at least two orders
  of magnitude, which K24 rejects; it suggests two physical processes may have shaped the Wave.
- **Outliers.** All clusters in Perseus and Taurus come out as outliers; K24 attributes this to the
  expansion of the Local and Per–Tau feedback bubbles on whose surfaces they lie. Most remaining
  outliers are in Orion, where outliers are at most a quarter of the clusters.
- **Sun's height.** Freeing the Sun's height above the plane (uniform prior −10 to 25 pc) shifts A, φ
  and δ by less than a third of their 1σ errors; the other parameters by less than 10% of 1σ.
- **Plane tilt and potentials.** Tilting the plane (two extra angles), and replacing the potential by
  McMillan 2017 or galpy's MWPotential2014 (Bovy 2015), reportedly have no effect.

**Step 6 · The CO check.** Projecting the best-fit 6D model (x, y, z, v_x, v_y, v_z) onto each
cloud's line of sight, v_LSR = cos l cos b v_x + sin l cos b v_y + sin b v_z (eq. 14), gives a curve
that passes through the measured ¹²CO velocities (Extended Data Fig. 3a: v_LSR falls from ~+20 km/s
at the CMa end to ~0–2 km/s at s ≈ 0–500 pc and rises to ~+6 km/s at the far end). K24 concludes that
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
  7.8 km/s and 2000 Monte Carlo draws; so the Sun **crosses the disc every 48 (+6/−5) Myr**. The Sun's
  height (−10 to 25 pc) changes it by < 0.5 Myr; R☉ from 7.9 to 8.7 kpc has no effect. For comparison,
  baryons alone (McKee et al. 2015, Σ₀ = 47.1 M☉ pc⁻²) give 95.3 Myr, and baryons plus a dark halo of
  0.013 M☉ pc⁻³ give 88.2 Myr, both within 1σ;
- **a thin dark disc**: assuming a dark-disc scale height of 25 pc (a thinner disc would shorten the
  period more), the 95-Myr period gives a surface density of 0.1 (+3.3/−3.3) M☉ pc⁻², which K24
  calls an upper bound (our reading: consistent with zero, with ~3.4 M☉ pc⁻² as the 1σ upper end).

**Back of the envelope.** (1) *Velocity amplitude.* For a small oscillation the angular frequency is
ω₀ = 74 km s⁻¹ kpc⁻¹ = 0.076 Myr⁻¹ (1 km s⁻¹ kpc⁻¹ ≈ 1/978 Myr⁻¹). At z_max = 220 pc the anharmonic
correction of eq. 3 (μ₀z_max ≈ 0.29) lowers it by ~7% to about 0.070 Myr⁻¹ at the Sun's radius
(our evaluation). Velocity amplitude = amplitude × angular frequency ≈ 220 pc × 0.070 Myr⁻¹ ≈
15 pc/Myr ≈ 15 km/s (1 pc/Myr ≈ 0.98 km/s), close to the reported ~14 km/s (the radial factor
exp[(r☉ − r)/r₀] and where along the Wave the amplitude peaks account for the rest; our reading). (2) *Period.* 2π/0.070 Myr⁻¹ ≈ 90 Myr; the Sun, which with v_z = 7.8 km/s rises
only ~100–115 pc (our estimate), has a similar period: 95 Myr. (3) *Density.* ρ₀ = ω₀²/(4πG): ω₀ = 68 km s⁻¹ kpc⁻¹ =
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
- **Caveats the authors give:** the evidence ratios are only ΔlnZ ≈ 1 ("equivalently good"); the
  damping profile is probably a mixture that the data cannot constrain; the scale height constraint is
  weak above ~300 pc; over several tens of Myr the Wave is likely affected by cloud destruction and
  phase mixing; the ripples at the Cygnus end are at the level of the dust-distance errors; Perseus
  and Taurus do not follow the Wave; the origin of the Wave remains open.
- **Points of our reading to carry into part 2** (not raised by K24 as problems):
  - "strongly preferred" (main text) versus ΔlnZ ≈ 1 and "both models are an equivalently good fit"
    (Methods). The Bayes factor compares B = 1 with B free, not travelling with standing; the
    standing wave is excluded by the phase argument and by B = 0.84 (+0.07/−0.06) lying ~5σ above 0.5
    in the posterior. Also, with ΔlnZ = ln Z₂ − ln Z₁ ≈ +1 and Z₂ the B-free model, the stated
    preference for fixed B = 1 seems to have the opposite sign (unless the indices are swapped).
  - B = 0.84 is itself ~2σ below 1: a pure travelling wave is not what the mixture fit returns.
  - The priors were set "based on initial fits" to the same data, and some are about as narrow as
    the posteriors (γ: prior width in ln γ of 0.07, i.e. ±0.10 in γ, posterior ±0.07–0.09; A: prior
    ±20 pc, posterior ±11–18 pc). The γ result in particular may be largely prior-driven. The unit
    labels of the ω₀ and μ₀ priors in Extended Data Table 1 cannot be matched to the posteriors
    without guessing (our reading).
  - The fitted vertical frequency ω(s) comes from a potential fitted to an existing Milky Way model;
    the v_z prediction is therefore not independent of the potential used to weigh the disc (step 8
    frees it, with the same data).
  - The CO agreement and the cluster agreement are shown as figures without a goodness-of-fit number.
- **What would have to be true for the authors to be wrong:**
  - *The velocities are not coherent with the positions.* Zhu et al. 2024 (ApJ 971, 167 [S: volume
    from a search listing]; arXiv:2402.15346 [V abstract]) re-measured vertical velocities, adding
    radial velocities (APOGEE-2 and cloud radial velocities with young stellar objects' Gaia DR3 proper
    motions), and found that the vertical-velocity oscillations "are not synchronous with the
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

*To be written next (stages, premises, Lean 4 decomposition in
[`studies/011-m11-radcliffe-wave-oscillation/argument/Argument.lean`](https://github.com/sudoghut/astrolab/blob/main/studies/011-m11-radcliffe-wave-oscillation/argument/Argument.lean)).*

### Part 3 · What astrolab can test or explore

*To be written next (the testability table that will be the source of the pre-registration).*

### Glossary

| Term | Meaning |
|---|---|
| Radcliffe Wave | a ~2.7-kpc chain of dense gas clouds near the Sun, shaped like a damped sine wave (Alves et al. 2020) |
| travelling wave | a wave whose crests move; position and velocity patterns are 90° out of phase |
| standing wave | a wave with fixed nodes; position and velocity have the same spatial pattern |
| B | K24's mixing parameter: 1 (or 0) = travelling wave, 0.5 = standing wave |
| anharmonic oscillator | an oscillator whose frequency depends on amplitude (here: slower for larger excursions) |
| phase velocity | the speed at which crests appear to move, wavelength / period |
| LSR | local standard of rest: the frame of a circular orbit at the Sun's position |
| ¹²CO | carbon monoxide, whose 2.6-mm line traces molecular gas and its line-of-sight velocity |
| Bayes factor, ΔlnZ | ratio of the evidences of two models; ΔlnZ ≈ 1 is weak preference |
| midplane density ρ₀ | total mass density (stars, gas, dark matter) in the Galactic plane near the Sun |

### Changelog

Newest first.

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

只看形状并不能说明它是否在运动。地上一条弯弯曲曲的绳子与一条正在被抖动的绳子，在一张照片里看起来一样。要知道 Radcliffe 波是不是真正的"波"（在银道面上下运动的东西），需要**速度**，尤其是垂直于盘面的竖直速度 v_z。早先用年轻恒星做的运动学研究（Tu 等 2022；Thulasidharan 等 2022；Bobylev 等 2022；Li & Chen 2022；Alfaro 等 2022；Donada & Figueras 2021）结论不一，K24 称之为"不确定"（inconclusive）。

为什么重要：

- 如果这条 2.7 kpc 的结构整体协调地振荡，它的运动就由银河系的竖直引力决定，于是它成了一个称量本地盘的巨大"摆"：银道面中央的质量密度、太阳附近的暗物质数量，以及太阳自身穿越银盘上下振荡的周期。
- 这样的结构如何形成（经过的卫星星系、落入的气体、盘内的不稳定性、超新星反馈（feedback））尚无定论；它是行进、驻定还是漂移，可以约束这些可能。
- 许多最近的恒星形成区都属于它，所以它的运动就是孕育附近年轻恒星的气体的运动，其中（K24 提出）也许包括那个以超新星吹出本地泡（Local Bubble，太阳所在的热空腔）的星团。

#### 1.2 数据

气体云很难在三维中追踪：射电望远镜只能测出气体朝向或背离我们的速度（一个速度分量）。年轻星团（young stellar clusters）容易些。星团是从同一块云中一起诞生的一群恒星；年轻时它仍随母云运动。Gaia 卫星测量每颗星的距离（由视差 parallax）与在天球上的运动（自行 proper motion）；光谱仪测量其视向速度（radial velocity）。对星团的成员星取平均，得到的星团位置与完整三维速度比单颗星精确得多。

具体而言，K24 用了：

- **年轻星团**（方法，"Stellar Cluster Catalog"）。来自 Cantat-Gaudin 等 2020 星表（基于 Gaia DR2，只保留质量好的视差、自行与视向速度）的星团，加上另外五个星表（Sim 等 2019、Hao 等 2022、He 等 2022、Szilágyi 等 2021、Liu & Pang 2019）的星团；成员星与 Gaia DR3 交叉匹配（cross-match）；视向速度来自 Gaia 以及 APOGEE 巡天（SDSS DR16），以提高覆盖率。每个星团给出日心银道直角坐标中的平均位置 (x, y, z) 与速度 (u, v, w)，以及平均值的标准误差。选择条件：
  - **年龄小于 30 Myr**（百万年），取自文献；按 K24 的说法，这"保证"星团仍追踪其母云的速度；
  - 去掉相对本地静止标准（LSR）视向速度大于 50 km/s 的运动学异常星团；
  - 只在 x–y 平面上选择（俯视）：距尘埃最佳拟合模型 ±5 倍波半径（47 pc，即 ±235 pc）以内的星团，**事先不对高度 z 设限**——竖直方向的图样不是由选择造成的；
  - 去掉 Lacerta OB1 星协，因为它在竖直方向与运动学上都与波不同；
  - 据称与 Hunt & Reffert 2023 的 Gaia DR3 星团表（只取最年轻的）对照，对结果没有影响。
  速度用太阳本动（solar peculiar motion）(u☉, v☉, w☉) = (10.0, 15.4, 7.8) km/s 换算到本地静止标准（local standard of rest, LSR，即太阳处圆轨道的参考系），得到 (v_x, v_y, v_z)。正文没有给出星团数目；公开表格（Harvard Dataverse doi:10.7910/DVN/XSCB9N，文件 `Radcliffe_Wave_stellar_clusters_Konietzka2024.tab`，10,888 字节，CC0）有 15 列：名称、文献、x、y、z、v_x、v_y、v_z 及误差、年龄与内点标记（inlier flag）（元数据没有给出行数；从图上看约为 10² 量级——由研究读取确认）。
- **分子云**（molecular clouds）：三维云位置取自 Major Cloud Catalog（Zucker 等 2019、2020）与 Alves 等 2020 的"Tenuous Connections"星表，只保留有视向速度测量的云。距离另有约 5% 的系统不确定度。
- **¹²CO 视线速度**（方法，"Line-of-sight Gas Velocities"）。一氧化碳（CO）在 2.6 毫米的射电波段发射，其多普勒频移给出气体沿视线的速度 v_LSR。K24 用 Dame 等 2001 的全银河系 CO 巡天（角分辨率 0.125°，速度分辨率 1.3 km/s），在每个云位置 0.3° 范围内提取谱线，保留 |v_LSR| < 30 km/s，用高斯函数拟合（Levenberg–Marquardt 算法）；9% 的云被舍去（超出巡天范围或无发射）。由于波离我们近、又长、又高出银道面约 200 pc，指向不同云的视线方向差别很大，一维速度就能测到 v_x、v_y、v_z（包括竖直分量）的不同组合。公开表格：doi:10.7910/DVN/Q7F4PC，文件 `Radcliffe_Wave_CO_analysis_Konietzka2024.tab`，5,286 字节，CC0，13 列（名称、x、y、z、x/y/z 弥散、l、b、d、rv、rv16、rv84）。

#### 1.3 一步一步：作者如何从数据走到结论

**第 1 步 · 星团与云勾勒出同一结构。** 图 1a 显示年轻星团（蓝色）与云（红色）位于同一条三维正弦曲线上，尽管选星团时没有对 z 设限。K24 由此认为星团诞生于波中的云，可以作为其运动的示踪体（tracer）。图 1b 以 v_z 为第三个轴画出同样的星团：速度也组成一个波，并沿结构相对位置波有所错开。

**第 2 步 · 竖直方向的力：非谐振子。** 振幅很小时，盘附近的恒星上下运动就像弹簧上的质量（谐振子 harmonic oscillator），角频率为 ν，ν² = 4πGρ₀，ρ₀ 是银道面中央的密度。波可以达到约 220 pc，与盘的标高（scale height）相当，那里回复力变弱、振荡变慢，就像摆角很大的单摆。K24 把竖直势写成（方法，式 1）

  Φ(z, r) = ½ ω₀² exp[(r☉ − r)/r₀] (z² − μ₀² z⁴)，

其中 r☉ = 8.4 kpc，ω₀ 是太阳半径处的小振幅角频率，r₀ 是密度的径向标长（scale length），μ₀ 是竖直标高的倒数。这三个数起初并不对波拟合，而是让式 1 在 r = 7–10 kpc、|z| ≤ 300 pc 范围内以 χ² 拟合一个现有银河系模型（Allen & Santillan 1991，参数按 Irrgang 等 2013 更新）得到：**ω₀ = 74 km s⁻¹ kpc⁻¹，r₀ = 3.7 kpc，μ₀ = 1.3 kpc⁻¹**，对应本地密度 ρ₀ ≈ 0.1 M☉ pc⁻³ 与标高 z₀ = 1/(√6 μ₀) = 314 pc（文献值：0.097 ± 0.013 M☉ pc⁻³ 与 280 (+70/−50) pc，McKee 等 2015）。由能量守恒得到上升到 z_max 的云的周期 T（式 2），借助第一类椭圆积分 K 得到解析的频率 ω(z_max, r)（式 3），振幅越大频率越低。由于波跨越不同的银心距，r 与 z_max 都是沿波位置 s 的函数，所以 ω = ω(s)。引力势被假设为稳态（stationary）；倾斜、银盘翘曲（warp）与径向的"呼吸"波被论证为可以忽略。

**第 3 步 · 波的模型。** 沿波长度方向，波由下式描述（式 4–5）：

  z(s, t) = ζ(s) [ B sin(ω₀t + 2πΛ(s) + φ) + (1 − B) sin(−ω₀t + 2πΛ(s) + φ) ]，
  v_z(s, t) = ζ(s) ω(s) [ B cos(ω₀t + 2πΛ(s) + φ) − (1 − B) cos(−ω₀t + 2πΛ(s) + φ) ]。

其中 s 是沿波（投影到 x–y 平面）的距离（起点 s = 0，在 CMa OB1 附近）；盘面内的基线是一条过三个锚点 (x₀, y₀)、(x₁, y₁)、(x₂, y₂) 的二次曲线；ζ(s) 是竖直包络；Λ(s) 是累积相位；φ 是相位常数；t 是时间（ω₀t 是当前的相位偏移）。参数 **B 混合两列方向相反的波**：B = 1（或 0）是纯**行波**（travelling wave），B = 0.5 是纯**驻波**（standing wave）。

- *为什么 z 与 v_z 的相位关系重要。* 在行波中 z ∝ sin(…)、v_z ∝ cos(…)：波穿过银道面的地方速度最大，波峰处速度为零——沿波方向位置与速度相差 **90° 相位**。在驻波（B = 0.5）中两项合成为 z = ζ sin(2πΛ + φ) cos(ω₀t) 与 v_z = −ζω sin(2πΛ + φ) sin(ω₀t)：z 与 v_z 的空间图样相同（**相位差为零**），零点（波节 nodes）永不移动。所以位置波与速度波的相对相位就是区分两者的观测量。
- *行波与引力势。* 对行波而言，给定引力势，空间形状就完全决定了 v_z（振幅乘以 ω(s)）；对驻波，波峰处的速度幅度不由形状决定。因此拟合可以由 z 预言 v_z，而不需要自由的速度幅度参数。
- *沿波缩短的波长*（式 6–7）：Λ(s) = s/(p − γs)，所以局部波长 λ(s) = (p − γs)²/p。K24 称 p 为"波的周期"，但它是长度（pc）：s = 0 处的波长；γ 决定波长缩短的快慢。
- *阻尼*（式 9）：ζ(s) = −A [1 + ((s − s₀)/δ)²]⁻¹，振幅为 A、峰值在 s₀、宽度为 δ 的洛伦兹（Lorentzian）包络。K24 发现洛伦兹形略好于 Alves 等 2020 的高斯形，并指出真实情况可能是两者的混合（如 Voigt 轮廓），但数据约束不了。
- 竖直模型有 14 个参数 Θ₁ = (x₀, y₀, x₁, y₁, x₂, y₂, A, p, φ, s₀, δ, γ, ω₀t, B)；盘面内运动另加两个 Θ₂ = (v_x,plane, v_y,plane)。

**第 4 步 · 拟合。** 对每个星团 k，到模型的"距离"是四维矢量 (x, y, z, v_z/ω₀) 减去模型在最近点 s_min 的值（式 12）；v_z 除以 ω₀ 把速度变成长度，让位置与速度同等重要。似然函数（likelihood，式 13）用一个共同的弥散 σ、核密度权重（kernel-density weights，让猎户座这样采样密集的区域不至于主导），以及一个软的离群函数（outlier function）C（tanh 截断）：任何一个分量超过 tanh(3)（即在 3σ 之外）的星团算离群点。云用三维版本（式 11）。用嵌套采样（nested sampling）程序 dynesty（1000 个活点）抽样，各参数先验独立，"依据初步拟合"设定（扩展数据表 1），例如 A ~ N(215, 20) pc、p ~ N(4650, 300) pc、ln γ ~ N(0.35, 0.07)、ln(δ/pc) ~ N(6.5, 0.1)、s₀ ~ N(680, 200) pc、φ ~ N(−0.09, 0.5) rad、ω₀t ~ U(−π/2, π/2)、B ~ U(0, 1)、盘面内速度 ~ U(−10, 10) km/s。弥散 σ 为 47 pc，即波的"半径"。

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

（锚点 x₀…y₂ 也在表中，各列之间在约 1σ 内一致。表注说第 (7) 列"与 (5) 相同的做法"，但其列名——云 + 星团——对应 (6)；我们把 (7) 理解为放开引力势参数的 (6)。）K24 指出只用云、只用星团与两者合用的拟合相互一致，并以此确认云与年轻星团组成一个在空间与运动学上都连贯的结构。最佳拟合画在图 1 中（x–y 坐标系逆时针旋转 62°，使 x 沿波方向）。

导出的数值（正文与方法）：

- **最大振幅约 220 pc；平均波长约 2 kpc**（约 2000 pc，由式 7 得出，从 CMa OB1 附近的约 4000 pc 变到天鹅座 X 附近的约 400 pc）。我们的核对：用第 (6) 列，λ(0) = p ≈ 4.78 kpc，λ(0.3 kpc) ≈ 3.9 kpc，λ(2.4 kpc) ≈ 0.34 kpc，λ(s) 在 0–2.4 kpc 上的平均约 2.1 kpc，与 K24 的描述一致（这是我们的理解；数据的 s 范围是假设的）。
- **最大竖直速度约 14 km/s。**
- **行波而非驻波。** 在 [0, 1] 上取平坦先验时 B = 0.84 (+0.07/−0.06)。另做一个 B 固定为 1 的拟合，得对数贝叶斯因子（Bayes factor）ΔlnZ = ln Z₂ − ln Z₁ ≈ 1（Z₁：B = 1，Z₂：B 自由）；K24 写道"两个模型对数据拟合得同样好，而 B = 1 固定的实现略受偏好"，此后取 B = 1。驻波（B = 0.5）由另一个论证排除：若 B = 0.5，各星团的相位 φ_k = arctan(z_k ω_k / v_z,k) 沿 s 应几乎不变（变化至多约 0.03π），但实际上覆盖了 −π/2 到 π/2 的整个范围。正文中这变成"行波相对驻波受到强烈偏好"。
- **相速度**（phase velocity，波峰看起来移动的速度，λ(s)/T(s)）：从 CMa OB1 附近约 40 km/s 到天鹅座 X 附近约 5 km/s，从太阳看波峰从右向左移动。若要用本地密度的变化解释这一数量级的变化，ρ₀ 至少要变化两个数量级，K24 认为不可能；它提出波可能由两种物理过程共同塑造。
- **离群点。** 英仙座与金牛座的所有星团都成为离群点；K24 归因于本地泡与英仙–金牛（Per–Tau）反馈泡的膨胀，这些云位于泡的表面。其余离群点大多在猎户座，那里离群点至多占星团的四分之一。
- **太阳的高度。** 放开太阳在银道面上的高度（均匀先验 −10 到 25 pc），A、φ、δ 的变化小于其 1σ 误差的三分之一，其他参数的变化小于 1σ 的 10%。
- **盘面倾斜与引力势。** 让盘面倾斜（多两个角度），以及把引力势换成 McMillan 2017 或 galpy 的 MWPotential2014（Bovy 2015），据称都没有影响。

**第 6 步 · CO 核对。** 把最佳拟合的六维模型 (x, y, z, v_x, v_y, v_z) 投影到每块云的视线方向，v_LSR = cos l cos b v_x + sin l cos b v_y + sin b v_z（式 14），得到的曲线穿过实测的 ¹²CO 速度（扩展数据图 3a：v_LSR 从 CMa 一端的约 +20 km/s 降到 s ≈ 0–500 pc 处的约 0–2 km/s，再升到远端的约 +6 km/s）。K24 的结论是"我们的模型解释了 ¹²CO 观测"，即气体随星团一起运动。一致性只以图示给出，没有拟合优度数值。

**第 7 步 · 盘面内的漂移。** 扣除银河系自转与较差自转（Allen & Santillan 势；另两个势"没有影响"）后，以 2 km/s 的典型误差做 χ² 拟合，得 v_x,plane = −3.9 (+2.6/−2.7) km/s、v_y,plane = 3.1 (+2.7/−2.6) km/s，即沿背离太阳的径向 4.9 km/s（扩展数据图 2：4.87），沿波方向 1.0 km/s（0.96）。K24 把它描述为整体（刚体 solid-body）漂移，"以约 5 km s⁻¹ 的速度沿径向远离银心"。往回推，漂移指向 Upper Centaurus Lupus 与 Lower Centaurus Crux 星团 15–16 Myr 前形成的位置，它们的超新星吹出了本地泡；K24 说精确的回溯超出了本文范围。

**第 8 步 · 用波称量银盘。** 放开 ω₀、μ₀、r₀（第 7 列；B = 1 时共 15 个参数）得 ω₀ = 68 (+8/−7) km s⁻¹ kpc⁻¹、μ₀ = 1.4 ± 0.2 kpc⁻¹、r₀ = 3.6 ± 0.5 kpc，与采用值 74、1.3、3.7 一致；固定与放开引力势的证据比同样是 ΔlnZ ≈ 1（"同样好"）。用等温层（isothermal sheet）关系 ρ₀ = ω₀²/(4πG) 与 z₀ = 1/(√6 μ₀)（Spitzer 1942）：

- **银道面中央总密度 ρ₀ = 0.085 (+0.021/−0.017) M☉ pc⁻³**，标高 z₀ = 294 (+63/−43) pc（K24 提醒，z₀ 超过约 300 pc 时频率的变化小于噪声），面密度 Σ₀ = 2 z₀ ρ₀ = 50.3 M☉ pc⁻²；
- 减去重子（恒星与气体，0.084 ± 0.012 M☉ pc⁻³，McKee 等 2015）：球形晕的**本地暗物质密度 0.001 (+0.024/−0.021) M☉ pc⁻³**，与零相容，并在 1σ 内与常规估计一致；
- **太阳的竖直振荡周期 95 (+12/−10) Myr**，取太阳竖直速度 7.8 km/s，用 2000 次蒙特卡罗抽样；所以太阳**每 48 (+6/−5) Myr 穿越一次银盘**。太阳的高度（−10 到 25 pc）使其改变 < 0.5 Myr；R☉ 从 7.9 到 8.7 kpc 没有影响。作为比较，只用重子（McKee 等 2015，Σ₀ = 47.1 M☉ pc⁻²）得 95.3 Myr，重子加 0.013 M☉ pc⁻³ 的暗晕得 88.2 Myr，都在 1σ 以内；
- **薄暗盘**（dark disk）：假设暗盘标高为 25 pc（更薄的盘会使周期更短），95 Myr 的周期给出面密度 0.1 (+3.3/−3.3) M☉ pc⁻²，K24 称之为上限（我们的理解：与零相容，1σ 上端约 3.4 M☉ pc⁻²）。

**粗略估算。** (1) *速度幅度。* 小振幅的角频率为 ω₀ = 74 km s⁻¹ kpc⁻¹ = 0.076 Myr⁻¹（1 km s⁻¹ kpc⁻¹ ≈ 1/978 Myr⁻¹）。在 z_max = 220 pc，式 3 的非谐修正（μ₀z_max ≈ 0.29）在太阳半径处使其降低约 7%，到约 0.070 Myr⁻¹（我们的计算）。速度幅度 = 振幅 × 角频率 ≈ 220 pc × 0.070 Myr⁻¹ ≈ 15 pc/Myr ≈ 15 km/s（1 pc/Myr ≈ 0.98 km/s），接近报告的约 14 km/s（其余差别来自径向因子 exp[(r☉ − r)/r₀] 以及振幅峰值沿波的位置；我们的理解）。(2) *周期。* 2π/0.070 Myr⁻¹ ≈ 90 Myr；太阳以 v_z = 7.8 km/s 只升到约 100–115 pc（我们的估算），周期相近：95 Myr。(3) *密度。* ρ₀ = ω₀²/(4πG)：ω₀ = 68 km s⁻¹ kpc⁻¹ = 2.2 × 10⁻¹⁵ s⁻¹，得 5.8 × 10⁻²¹ kg m⁻³ = 0.085 M☉ pc⁻³。(4) *相速度。* λ/T 在 CMa 一端约 4000 pc / 95 Myr ≈ 42 km/s，在天鹅座一端约 400 pc / 90 Myr ≈ 4.4 km/s，与约 40 与约 5 km/s 相符。所以主要结论归结为：波的高度（220 pc）与竖直速度（约 14 km/s）错开四分之一波长，正是一个在已知银盘引力势中振荡的物体应有的表现。

#### 1.4 结论与把握程度

- **结论：**
  1. Radcliffe 波像一列由银河系引力驱动的行波那样穿越银道面振荡，最大振幅约 220 pc，平均波长约 2 kpc，最大竖直速度约 14 km/s；猎户座、仙王座、北美星云与天鹅座 X 作为这列波的一部分运动；
  2. 行波相对驻波"受到强烈偏好"；
  3. 气体（¹²CO）与年轻星团一起运动；
  4. 波以约 5 km/s 的速度沿径向向外（远离银心）漂移，支持本地泡的母星团形成于其中的设想；
  5. 把它当作连贯的振子，测得 ρ₀ = 0.085 M☉ pc⁻³、与零相容的本地暗物质密度、暗盘的上限，以及太阳 95 Myr 的竖直周期。
- **作者给出的保留：** 证据比只有 ΔlnZ ≈ 1（"同样好"）；阻尼轮廓可能是数据约束不了的混合形；标高在约 300 pc 以上约束很弱；在几千万年的时间尺度上，波很可能受到云的瓦解与相混合（phase mixing）的影响；天鹅座一端的小起伏与尘埃距离误差相当；英仙座与金牛座不随波运动；波的起源仍未解决。
- **我们读出的、要带进第二部分的要点**（K24 并未把它们当作问题提出）：
  - 正文的"强烈偏好"与方法部分的 ΔlnZ ≈ 1、"两个模型拟合得同样好"之间的差别。贝叶斯因子比较的是 B = 1 与 B 自由，而不是行波与驻波；驻波是由相位论证以及后验 B = 0.84 (+0.07/−0.06) 高出 0.5 约 5σ 排除的。另外，若 ΔlnZ = ln Z₂ − ln Z₁ ≈ +1 且 Z₂ 是 B 自由的模型，所说的"B = 1 固定略受偏好"符号似乎相反（除非下标互换）。
  - B = 0.84 本身比 1 低约 2σ：混合拟合给出的并不是纯行波。
  - 先验是"依据初步拟合"（用同样的数据）设定的，有些与后验差不多一样窄（γ：ln γ 先验宽 0.07，即 γ 约 ±0.10，后验 ±0.07–0.09；A：先验 ±20 pc，后验 ±11–18 pc）。尤其是 γ 的结果可能主要由先验决定。扩展数据表 1 中 ω₀ 与 μ₀ 先验的单位标注，不靠猜测无法与后验对上（我们的理解）。
  - 拟合用的竖直频率 ω(s) 来自对现有银河系模型拟合的引力势；因此 v_z 的预言并不独立于用来称量银盘的引力势（第 8 步用同样的数据把它放开）。
  - CO 的一致与星团的一致都以图示给出，没有拟合优度数值。
- **作者若是错的，需要什么成立：**
  - *速度与位置并不协调。* Zhu 等 2024（ApJ 971, 167 [S：卷号来自检索列表]；arXiv:2402.15346 [V 摘要]）重新测量了竖直速度，加入了视向速度（APOGEE-2，以及云的视向速度配合年轻恒星天体的 Gaia DR3 自行），发现竖直速度的振荡"与竖直坐标不同步"：沿波的 v_z 呈约 5 km s⁻¹ kpc⁻¹ 的梯度，呈"偶极状"（dipole-like）图样，他们认为这使 Radcliffe 波模型"受到质疑"。如果他们的 v_z 图样正确，定义 K24 行波的 90° 相位关系就不成立。
  - *在一个振荡周期内波不是刚体。* Li、Zhou & Chen 2024（arXiv:2410.14603 [V 摘要]；期刊未核实）用本地气体的三维模拟论证，银河系的剪切（shear）与本轮运动（epicyclic motion）会在约 45 Myr 内把波拉长到"几乎是现在长度的两倍"，而在这段时间内"所提出的竖直振荡只完成半个周期"，并称把它当作刚体是"过度简化"。若如此，用一条相位规律 Λ(s)（以及刚体式的盘面内漂移）描述的单一连贯振荡就不是好的描述，即使局部的片段在上下运动。
  - *位置与速度给出不同的波长，或漂移更快。* Bobylev、Ikhsanov & Bajkova 2025（Astrophys. Bull. 80(2)，arXiv:2503.21019 [V 摘要]）按年龄分析疏散星团：与波相关的星团不超过 30 Myr（支持 K24 的年龄截断）；对 5.2 Myr 的一组，他们得到位置振幅 z_max = 117 ± 12 pc、波长 4.55 ± 0.14 kpc，但竖直速度幅度为 4.86 ± 0.19 km/s、波长 1.74 ± 0.08 kpc；对 18.6 Myr 的一组为 54 ± 5 pc（λ 6.30 ± 0.12 kpc）与 7.90 ± 0.16 km/s（λ 0.83 ± 0.11 kpc）；远离银心的径向运动为 10 pc/Myr（≈ 10 km/s，是 K24 5 km/s 的两倍）；他们倾向于约 2 kpc 宽的超新星激波前起源。z 与 v_z 的波长不同（我们的理解）不是单一连贯行波所预言的。他们的方法与选择和 K24 不同。
  - *离群点与选择的处理造成了信号。* 英仙座与金牛座的星团全部被标为离群点；软的 3σ 离群模型与核密度权重决定了每个区域的分量。如果 90° 相位差依赖于这些选择，或依赖于少数几个猎户座与仙王座的星团，振荡就没那么可靠。
  - *年龄截断并不保证星团仍随气体运动。* 年龄可达 30 Myr 的星团已有三分之一个振荡周期的时间离开母气体；K24 依靠 CO 核对来说明这一点。

### 第二部分 · 论证逻辑

*待写（环节、前提，以及 [`studies/011-m11-radcliffe-wave-oscillation/argument/Argument.lean`](https://github.com/sudoghut/astrolab/blob/main/studies/011-m11-radcliffe-wave-oscillation/argument/Argument.lean) 中的 Lean 4 拆解）。*

### 第三部分 · 本项目可检验或探索的环节

*待写（可检验性表格，将作为预注册的来源）。*

### 术语表

| 术语 | 含义 |
|---|---|
| Radcliffe 波（Radcliffe Wave） | 太阳附近约 2.7 kpc 长、形如阻尼正弦波的致密气体云链（Alves 等 2020） |
| 行波（travelling wave） | 波峰移动的波；位置与速度图样相差 90° |
| 驻波（standing wave） | 波节固定的波；位置与速度的空间图样相同 |
| B | K24 的混合参数：1（或 0）= 行波，0.5 = 驻波 |
| 非谐振子（anharmonic oscillator） | 频率随振幅变化的振子（此处：振幅越大越慢） |
| 相速度（phase velocity） | 波峰看起来移动的速度，波长 / 周期 |
| 本地静止标准（LSR） | 太阳位置处圆轨道的参考系 |
| ¹²CO | 一氧化碳，其 2.6 毫米谱线示踪分子气体及其视线速度 |
| 贝叶斯因子（Bayes factor）、ΔlnZ | 两个模型证据（evidence）之比；ΔlnZ ≈ 1 是弱偏好 |
| 中央面密度 ρ₀（midplane density） | 太阳附近银道面上的总质量密度（恒星、气体、暗物质） |

### 研究进展

按时间倒序。

- 2026-11-21：第一部分初稿（第二、三部分随后）。

### 来源

- Konietzka 等 2024，Nature 628, 62–65，doi:10.1038/s41586-024-07127-3，arXiv:2402.12596（本文研究的论文；读的是 arXiv v1 全文）[V]。
- 数据：Harvard Dataverse doi:10.7910/DVN/XSCB9N（星团）与 doi:10.7910/DVN/Q7F4PC（¹²CO）[V 仅元数据]。
- Alves 等 2020，Nature 578, 237，arXiv:2001.08748 [V 摘要]。
- Zhu 等 2024，ApJ 971, 167，arXiv:2402.15346 [V 摘要；S 卷号]。
- Li、Zhou & Chen 2024，arXiv:2410.14603 [V 摘要]。
- Bobylev、Ikhsanov & Bajkova 2025，Astrophys. Bull. 80(2)，arXiv:2503.21019 [V 摘要]。
- McKee、Parravano & Hollenbach 2015，ApJ 814, 13（本地重子；按 K24 的引用）。
