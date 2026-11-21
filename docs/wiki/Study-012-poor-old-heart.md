# The poor old heart of the Milky Way: metal-poor stars at the Galactic Centre

[English](#english) · [中文](#中文)

*Paper: Rix, Chandra, Andrae, Price-Whelan, Weinberg, Conroy, Fouesneau, Hogg, De Angeli, Naidu, Xiang, Ruz-Mieres 2022, "The Poor Old Heart of the Milky Way", ApJ 941, 45, doi:10.3847/1538-4357/ac9e01, [arXiv:2209.02722](https://arxiv.org/abs/2209.02722). Study:
[`studies/012-m12-poor-old-heart`](https://github.com/sudoghut/astrolab/tree/main/studies/012-m12-poor-old-heart) (web page: [online](https://sudoghut.github.io/astrolab/studies/012-m12-poor-old-heart/web/)).
Status: planned. Last updated: 2026-11-21 (see the changelog at the end). The source of this page lives in the main repository at
[`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki); edit it there.*

*中文标题：银河系贫而老的核心：银心附近的贫金属星。状态：计划中。论文：Rix, Chandra, Andrae, Price-Whelan, Weinberg, Conroy, Fouesneau, Hogg, De Angeli, Naidu, Xiang, Ruz-Mieres 2022，"The Poor Old Heart of the Milky Way"，ApJ 941, 45，doi:10.3847/1538-4357/ac9e01，[arXiv:2209.02722](https://arxiv.org/abs/2209.02722)。研究：[`studies/012-m12-poor-old-heart`](https://github.com/sudoghut/astrolab/tree/main/studies/012-m12-poor-old-heart)（网页：[在线版](https://sudoghut.github.io/astrolab/studies/012-m12-poor-old-heart/web/)）。最后更新：2026-11-21（见文末"研究进展"）。本页源文件在主仓库的 [`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki) 中，请在那里修改。*

---

## English

### Part 1 · The paper in plain language

All numbers below were read from the arXiv HTML version (arXiv:2209.02722v1, 6 September 2022);
we did not compare it line by line with the typeset ApJ version. "R22" below means this paper.
Where the paper gives different numbers for the same quantity in different places, we quote all of
them with their location.

#### 1.1 The question and why it matters

Stars keep a chemical record of the gas they were born from. The first stars formed from almost pure
hydrogen and helium; every generation of stars that exploded added heavier elements ("metals" to an
astronomer). A star's **metallicity** [M/H] is the logarithm of its metal-to-hydrogen ratio relative
to the Sun: [M/H] = 0 is solar, −1 is one tenth of solar, −2 is one hundredth. Very metal-poor
stars therefore formed early, before much enrichment had happened.

Where in the Milky Way should the oldest stars be? Cosmological simulations of galaxies like ours
predict that the first stars formed in the several dense clumps that merged early into the
"proto-Galaxy", the Milky Way's progenitor before it had a disc. Those stars should now sit in the
deepest part of the potential well, close to the Galactic Centre, on hot (randomly oriented, not
orderly rotating) orbits. R22's abstract puts it as an expectation for massive disc galaxies: they
"should host an ancient, metal-poor, and centrally concentrated stellar population".

Before 2022 this population was hard to see. The inner Galaxy is crowded and heavily obscured by
dust, and metal-poor stars are a tiny minority there (most bulge stars are metal-rich). Earlier work
found such stars with narrow-band photometric pre-selection (e.g. the Pristine Inner Galaxy Survey,
PIGS, by Arentsen et al.), and Belokurov & Kravtsov 2022 identified, in the solar neighbourhood, an
old, kinematically hot, chemically distinct in-situ (born in the Milky Way) population that they
named **Aurora**, out of which the disc emerged. What was missing was a large, uniform sample of
metal-poor stars in the inner few kiloparsecs (kpc; 1 kpc ≈ 3,260 light years) with metallicities
and orbits. Gaia Data Release 3 (DR3, June 2022) made this possible.

Why it matters: if a massive, centrally concentrated, very old, metal-poor population exists, it is
the surviving core of the proto-Galaxy. Its mass, size and rotation constrain how the Milky Way
assembled in its first billion or two years, and whether it needs extra early mergers (such as the
proposed "Heracles"/"Kraken"/"Koala" event) to explain the old stars in its centre.

#### 1.2 The data

**Gaia XP spectra.** Besides positions, parallaxes (distances) and motions, Gaia DR3 published
low-resolution spectra for about 220 million stars (Gaia DR3 documentation; not re-checked here) from two prisms, the blue photometer (BP) and
red photometer (RP), together called **XP**. They are not spectra in the usual sense of a list of
fluxes per wavelength: each is published as a set of coefficients of smooth basis functions (55 for
BP and 55 for RP, 110 in all). Their resolution is too low to measure individual absorption lines,
but the overall shape carries information on temperature, surface gravity, metallicity and dust.

**Metallicities by machine learning.** R22 did not fit physical stellar models to the XP spectra.
They trained a gradient-boosted decision-tree model (**XGBoost**) to predict the metallicity that
the high-resolution infrared survey **APOGEE** (Apache Point Observatory Galactic Evolution
Experiment, SDSS Data Release 17) measures for the same stars (Section II.2, Appendix A.1):

- training set: "the *entire* SDSS DR17 APOGEE of giants with G_BP<15.5 (∼230,000 stars)", with
  surface gravity log g < 3.5 (giants only);
- inputs: the 110 XP coefficients, synthetic narrow-band photometry computed from the XP spectra with
  GaiaXPy (Pristine, Strömgren, J-PLUS, SkyMapper and HST colours) and the infrared magnitudes W1,
  W2 from ALLWISE (the Wide-field Infrared Survey Explorer catalogue);
- outputs: [M/H] (and effective temperature T_eff and log g, released on Zenodo);
- accuracy: 20-fold cross-validation (Table 1) gives a median absolute error of 0.049 dex and a
  root-mean-square error (RMSE) of 0.107 dex for the Table 1 row matching the adopted inputs (all
  coefficients + XP colours + WISE), although Appendix A.1 says the final configuration is "slightly
  worse than the best"; against about 17,000
  APOGEE stars in the target region the estimates are "≲0.1 in the median" over −2.5 < [M/H] < 0.5,
  which R22 call "not a pure cross-validation" since those stars were in the training set; against
  LAMOST, GALAH and Gaia GSP-Spec the root-mean-square difference is about 0.1 dex (Appendix A.2,
  Fig. 8) with a "slight increase in scatter towards low [M/H]"; T_eff agrees with APOGEE to a
  median of 32 K;
- extinction: the estimates stay unbiased "at a level of a few percent" up to A_K = 0.3 (about
  A_V ≈ 3 magnitudes of visual extinction).

A tree model like XGBoost cannot predict values outside the range of its training labels; R22 note it
"will not extrapolate [M/H] significantly beyond the APOGEE DR17 range". The paper does not state how
many training stars have [M/H] < −2 (not verified; APOGEE contains few such stars), nor a separate
error at the metal-poor end.

**The sample** (Section II.1). One query to the Gaia archive:

- sky: |b| < 30° and (l < 30° or l > 330°), a 60° × 60° box in Galactic longitude l and latitude b
  centred on the Galactic Centre (the abstract's "within 30°" means this box, not a cone);
- colour 1.0 < BP − RP < 3.5 (red, i.e. cool or reddened, stars), brightness phot_bp_mean_mag < 15.5,
  and XP spectra available (has_xp_continuous);
- distance and luminosity: `parallax < 1.` (parallax below 1 mas, milliarcsecond, i.e. further than
  about 1 kpc) and `parallax < 100.*power(10.,0.2*(0.9 - (phot_g_mean_mag - 1.5*(bp_rp-1.))))` (parallax in mas). The second condition uses a colour-corrected, approximately
  dereddened magnitude G − 1.5(BP − RP − 1) and keeps stars brighter than about M_G = 0.9 after that
  correction (luminous giants, including the red clump).

This "yields 2.1 million objects". About 2% are removed as reddened hot stars using a synthetic
colour (m1) criterion. The result is "[M/H] estimates for about 2 million giants toward the inner
Galaxy, 1.58 million of which have RVS velocities, and 1.25 million have both RVS velocities and
ϖ/σ_ϖ≥5" (RVS: Gaia's Radial Velocity Spectrometer; ϖ/σ_ϖ: parallax divided by its error).

**Orbits** (Section II.4). For the 1.25 million stars with radial velocities (error δv_RVS < 5 km/s)
and good parallaxes, R22 integrate orbits in a four-component Milky Way potential (Hernquist nucleus
and bulge, approximately exponential disc with scale length 2.6 kpc and scale height 300 pc, NFW dark
halo) with circular speed 229 km/s at the Sun, and compute **actions** with the "Stäckel fudge" in
galpy. Actions are orbit labels: J_R measures radial excursions, J_z vertical excursions and J_φ the
angular momentum about the Galaxy's rotation axis. R22 use the ratio J_φ/J_tot, with
J_tot = √(J_φ² + J_R² + J_z²): close to +1 for a star on a disc-like circular orbit, near 0 for a
star with no net rotation (on average, for a non-rotating population).

**Public files.** Zenodo record 7035809 (doi:10.5281/zenodo.7035809, cited by R22, presumably the
concept DOI; version v0.1 is doi:10.5281/zenodo.7035810, 2 September
2022, CC BY 4.0, authors Andrae, Rix, Chandra, Price-Whelan): `xp_gc_mh.csv` (98.5 MB, MD5
7257c98622573a4a625571fc973859c5), "XGBOOST-inferred temperatures, surface gravities, and
metallicities for 1.5 million stars", and `xp_gc_kinematics.csv` (115.3 MB, MD5
b220c27aacff1f2f03d5a1f2b5fca147), "Galactocentric coordinates, actions, and basic orbital
parameters" for 1.2 million stars with Gaia DR3 radial velocities; 213.8 MB in all. Both exceed this
project's 50 MB single-download limit; the user agreed to an exception on 2026-11-21 (plan
[`design/028-plan_*`](https://github.com/sudoghut/astrolab/blob/main/design/028-plan_m12-poor-old-heart-paper-study.md)).
The columns of the files are not documented on the landing page; the study will read them.

#### 1.3 Step by step: how the authors got from data to conclusion

**Step 1 · Validate the metallicities** (Sections II.2–II.3, Appendix A, Figs. 1, 8, 9). Compare the
XP metallicities with APOGEE (training stars, not independent), with three independent spectroscopic
surveys (LAMOST, GALAH, GSP-Spec; about 0.1 dex scatter, GSP-Spec does not reach low metallicities)
and with SkyMapper DR2 photometric metallicities (Chiti et al.), where the agreement near
[M/H] ≈ −1.5 is poor (mean offset 0.28 dex, 68% interval of about 1 dex), which R22 attribute to the
SkyMapper estimates. The conclusion of this step is that the XP metallicities are good to about
0.1 dex, the number the abstract quotes as δ[M/H] ≲ 0.1.

**Step 2 · Count the metal-poor stars** (Section III.2, Fig. 4). The cumulative metallicity
distribution of the whole sample is the main result. The counts, as given in different places:

| Cut | Section III.2 | Fig. 4 caption | Section IV (summary) | Abstract |
|---|---|---|---|---|
| [M/H] < −2 | >4,000 | ∼5,000 | — | — |
| [M/H] < −1.5 | ∼18,000 | ∼20,000 | ∼20,000 | ∼18,000 with −2.7 < [M/H] < −1.5 |
| [M/H] < −1 | almost 100,000 | nearly 100,000 | ∼70,000 | — |
| whole sample | about 2 million (II.2) | ∼1.7 million | ∼2 million | 2 million |

(The introduction and Section II.4, "estimates for 1.5 million stars towards the Galactic center",
with orbits for 1.25 million, say 1.5 million, as does the Zenodo description; the query returned
2.1 million.)
The shape of the distribution: the logarithmic number density rises with metallicity as
d log n/d[M/H] ≈ 1 between about −2 and −1, more steeply below −2 and between −1 and −0.6, and peaks
near [M/H] ≈ −0.6. The tail ends near [M/H] ≈ −2.5; R22 write that whether this is a "genuine
metallicity floor" or reflects the APOGEE training set needs follow-up. The abstract's lower bound
−2.7 is not explained in the text (not verified where it comes from).

*Back-of-envelope check.* If d log n/d[M/H] = 1 exactly, the number below a metallicity grows by a
factor 10^0.5 ≈ 3.2 for every 0.5 dex. From 18,000 below −1.5 this predicts about 5,700 below −2 and
about 57,000 below −1. The ">4,000" below −2 fits a steeper fall-off below −2, as stated; "∼70,000"
below −1 is close to the power law, while "almost 100,000" would need a rise by a factor of about 5.5
between −1.5 and −1, steeper than the slope R22 describe for that interval. Our arithmetic, not R22's.

**Step 3 · Where are they? The spatial extent** (Section III.1, Figs. 2, 3). The metal-poor stars are
too far for good individual distances: their median parallax precision is "only ϖ/σ_ϖ∼5" (about 12
for the whole sample; 1% of the whole sample has negative parallaxes). So R22 do not convert parallaxes
to distances star by star. They assume a model (eq. 1): the stars follow a **spherical Gaussian** in
Galactocentric radius R_GC with width σ_RGC, and the expected number of stars in each direction and
parallax interval is n(ϖ) = dΩ dϖ ϖ⁻⁴ ρ_Gauss(R(ϖ, l, b), σ_RGC) (the ϖ⁻⁴ converts a volume element
at distance 1/ϖ into a parallax interval). Fitting the observed parallaxes, with their errors and a
parallax zero-point correction of 0.02 mas, by maximum likelihood gives, for the [M/H] < −1.5 stars,
"an extent of σ_RGC∼2.7 kpc". No uncertainty is quoted, no flattened shape is tried, and the paper
calls the modelling of dust, crowding and parallax errors a task for follow-up.

*Back-of-envelope checks.* σ = 2.7 kpc seen from 8.2–8.5 kpc subtends ≈18° (17.6–18.2° exactly, arctan(2.7 kpc/R0)); R22 say
18° (Section III.1). The field
edge at 30° from the Centre is 4.7–4.9 kpc away from it in projection, less than 2σ, so the model must
account for the field boundary (it does, through the dΩ over the observed directions). A 3D Gaussian
with σ = 2.7 kpc puts 47% of its stars within 4 kpc of the Centre and 67% within 5 kpc, matching the
summary's "most stars are within 5 kpc of the Galactic center".

**Step 4 · How much mass?** (Section III.2). Only luminous giants are counted; the stellar mass they
represent needs a template population. R22 use the globular cluster M4 (an old, metal-poor star
cluster): about 35 giants with M_G < 0.5 beyond its half-mass radius of 6′, and a total mass of
7×10⁴ M☉, which "implies one giant (at M_G<0.5) per 800 M☉ of total stellar population mass". At face
value the [M/H] < −1.5 stars then represent M_tot ∼ 2×10⁷ M☉. Crowding and dust hide stars, so R22
multiply by "a conservative estimate" of 2.5 and quote a lower limit M_tot ≳ 5×10⁷ M☉ (abstract and
Section III.2). The summary goes further: the "manifest dust obscuration implies a large correction"
suggesting M* ≳ 10⁸ M☉.

*Back-of-envelope check.* 18,000–20,000 giants × 800 M☉ = 1.4–1.6×10⁷ M☉, rounded to 2×10⁷ (the
sample counts include stars fainter than M_G = 0.5, down to a colour-corrected (approximately
dereddened) M_G ≈ 0.9, so the template does not match
the sample cut exactly). The per-giant mass itself does not follow from the numbers quoted: if half of
M4's mass lies beyond its half-mass radius, 35 giants there mean about 3.5×10⁴/35 ≈ 1,000 M☉ per
giant (7×10⁴/35 = 2,000 if the whole mass is used), not 800. The steps between are not given (our
arithmetic; not verified against the PDF or the journal version).

**Step 5 · How do they move?** (Section III.3, Figs. 5, 6). Most metal-poor stars have hot, eccentric
orbits (eccentricities spread nearly flat from about 0.1 to 0.8) that stay in the inner Galaxy (mean
apocentre ⟨R_apo⟩ ≈ 4 kpc, Section III.3; the summary, Section IV: "most stars have apocenters of
less than 5 kpc"). A separate group with
e ≥ 0.75 and R_apo ≳ 10 kpc is identified as stars of the Gaia-Sausage-Enceladus (GSE) merger
debris passing through pericentre; R22 do not quantify that contamination. The rotation measure
J_φ/J_tot rises with metallicity: the abstract says "Stars with [M/H]<−2 show no net rotation" and
"those with [M/H]∼−1 are rotation dominated"; Section III.3 is more cautious ("starting already at
[M/H]<−2 there is some, albeit small, net" rotation), gives J_φ/J_tot ≈ 0.3 at [M/H] = −1.3 and a
level-off near −0.7; the summary gives 0.25 at [M/H] = −1.5 and ≈0.9 at −0.8.

**Step 6 · Chemistry** (Section III.4, Fig. 7). For the subset in APOGEE DR17, [α/Fe], [Al/Fe] and
[Mg/Mn] (the abundance of α elements, made quickly by massive stars, relative to iron, and ratios used
to separate stars born in the Milky Way from accreted ones) show that most low-eccentricity stars with
[M/H] < −1 are α-enhanced, i.e. formed from rapidly enriched gas, while a low-α sequence with large
apocentres (GSE-like) appears at high eccentricity. R22 note the diagnostic is "more ambiguous at low
metallicity".

**Step 7 · From metallicity to age** (Section IV). R22 measure no ages for these giants; age
estimates are "beyond the scope of this work" (Section II). The age argument is chemical: the oldest α-enhanced
disc stars, at [M/H] ∼ −1, "appear to be ≈12.5 Gyrs old" (ref. [96], Xiang & Rix 2022; see our
[Study 010 article](https://github.com/sudoghut/astrolab/blob/main/docs/wiki/Study-010-thick-disc-early-formation.md)).
Stars that are more metal-poor than the oldest disc, and that "chemically, and therefore temporally,
predate the oldest α-enhanced disk", must then have formed at τ ≳ 12.5 Gyr, "corresponding to z≳5".
This assumes that metallicity rose monotonically in time across the whole proto-Galaxy.

*Back-of-envelope check.* In the Planck 2018 cosmology (age 13.79 Gyr), a lookback time of 12.5 Gyr
is redshift z ≈ 4.6 (1.3 Gyr after the Big Bang); "z≳5" rounds up slightly (z = 5 is 12.62 Gyr
lookback) (our calculation with astropy's Planck18; R22 do not give the conversion).

#### 1.4 What they conclude, and how sure they are

The abstract: Gaia XP data reveal "an extensive, ancient, and metal-poor population" in the inner
Galaxy: ∼18,000 stars with −2.7 < [M/H] < −1.5, representing ≳5×10⁷ M☉ of stars, with a spatial
Gaussian extent σ ≈ 2.7 kpc; the most metal-poor ([M/H] < −2) show no net rotation, those at
[M/H] ∼ −1 are rotation dominated; "These central, metal-poor stars most likely predate the oldest
part of the disk (τ_age≈12.5 Gyrs), which implies that they formed at z≳5". The summary (Section IV) calls it
"the most ancient proto-Galactic component of our Galaxy"; Section III.4 identifies it with Belokurov &
Kravtsov's Aurora. The summary argues that being confined within the solar circle (R_GC < R☉) argues
"against an origin through accretion from a once-distant satellite": such masses of strongly
α-enhanced stars at such low [M/H] "are most likely to occur at the center of a (eventually) quite
massive halo", not in a low-mass satellite. Since the chemistry of the proposed
Heracles/Kraken/Koala merger debris and of the proto-Galactic Aurora is "virtually indistinguishable
in all chemical spaces", R22 suggest (Section III.4) their picture "appears to obviate the need for an
ex-situ merger" of that kind, adding: "This does not necessarily imply that these mergers did not
occur." They do not claim a new component: "The results presented here are by no means a new
distinct stellar component".

Caveats the authors give (the summary, Section IV, calls the analysis "in many ways preliminary"):

- the spatial distribution "deserves to be modeled quantitatively, including the effects of dust
  extinction, source crowding, parallax uncertainties" (Section IV);
- dust leaves a gap at |Z| < 700 pc from the plane, where most stars are missing (Section III.2), and
  obscures the central kpc (Section III.3);
- "How pure are the XP selected samples in this regime?" (Section IV; contamination of the metal-poor
  tail by stars with wrong metallicities);
- the [M/H] floor near −2.5 may be real or an artefact of the APOGEE training range (Section IV);
- apocentres may be biased high by distance errors (Section III.3);
- the mass rests on the M4 template and a "conservative" correction (Section III.2);
- the XP information is "far from" fully exploited; forward modelling should do better (Section IV).

Points of our reading to carry into part 2:

- **Counts are internally inconsistent** (table in step 2): ∼18,000 vs ∼20,000 below −1.5; >4,000 vs
  ∼5,000 below −2; almost 100,000 vs ∼70,000 below −1; and the sample size is 1.5 (introduction,
  Section II.4), 1.7 (Fig. 4), 2 (abstract, II.2, IV) or 2.1 (query) million depending on where one looks (some of this may reflect different subsets, e.g. before and
  after cuts, but the paper does not say).
- **Table 1 vs text**: the adopted configuration's row (0.049 dex, 0.107 dex) is the best in Table 1,
  but Appendix A.1 says the final configuration is "slightly worse than the best".
- **The mass** is ≳5×10⁷ M☉ in the abstract and ≳10⁸ M☉ in the summary, and its per-giant
  conversion (800 M☉) does not follow from the quoted M4 numbers by simple arithmetic.
- **σ ≈ 2.7 kpc has no uncertainty**, rests on a spherical Gaussian (no flattening), on parallaxes
  with median precision ∼5, and on a model that does not include dust or crowding.
- **"Predate the oldest disk" is an inference, not an age measurement**: no star in the sample has an
  age. It needs a monotonic age–metallicity relation everywhere in the young Galaxy, and the
  12.5 Gyr disc age itself comes from Xiang & Rix 2022 with its own absolute-scale uncertainty
  (see the Study 010 article).
- **Metallicity systematics at low [M/H]**: XGBoost trained on APOGEE, which has few very metal-poor
  stars, cannot return values below the training range and, as regression models generally do, is
  expected to pull extreme values towards the bulk (a general property, not measured in R22); the validation at [M/H] < −2 is thin (GSP-Spec does not reach there; the APOGEE check uses
  training stars). Contamination of the tail by metal-rich stars scattered low (the sample has about
  100 stars above [M/H] = −1.5 for each one below: ∼18,000 of ∼2 million) would inflate the counts, mass and perhaps the
  measured extent.
- **"No net rotation below −2"** (abstract) versus "some, albeit small" rotation (Section III.3).

What would have to be true for the authors to be wrong:

- *The counts are inflated*: a substantial fraction of the [M/H] < −1.5 stars are metal-richer stars
  with underestimated XP metallicities (for example from dust or crowding), so the population is
  smaller and less massive. Independent spectroscopy of an XP-selected subsample would test this.
- *The extent is different*: with dust, crowding and the field boundary modelled, or a flattened
  shape allowed, the metal-poor stars might not be a compact 2.7 kpc sphere. Kurbatov et al. 2024
  (arXiv:2410.22250, "The realm of Aurora", submitted to MNRAS; abstract verified) model Gaia XP
  giants with [M/H] < −1.3 from r ∼ 1 to 18 kpc with Gaia's selection function: a single cored
  power law fits with "a vertical flattening of ∼0.5 and a slope −3.4", and a two-component model
  is better, with GSE debris and Aurora contributing roughly equally near the Sun but "Aurora
  dominates the inner halo with a steeper power-law index of −4.5". This supports a centrally
  concentrated Aurora but is flattened, not spherical (Rix is a co-author).
- *The stars are not all old or in situ*: if the inner metal-poor population mixes proto-Galactic
  stars with debris of early small satellites, "predate the disk" and "not accreted" weaken.
  Ardern-Arentsen et al. 2024 (PIGS VIII, arXiv:2312.03847, accepted to MNRAS; abstract verified),
  with spectroscopy of 13,235 stars, find that about 60% of very metal-poor ([Fe/H] < −2.0) stars stay
  within 5 kpc, that the rotation drops between [Fe/H] = −1.0 and −2.0 but is "constant for VMP stars
  (at ∼ 40 km/s)" (so very metal-poor inner stars do rotate somewhat), and tentatively propose two spheroidal
  components: a more metal-rich, concentrated, faster-rotating one (pre-disc in situ or large building
  blocks) and a more metal-poor, extended, slower one (smaller accreted galaxies).
- *The spin-up is not what it seems*: Viswanathan et al. 2025 (arXiv:2411.12165, A&A 703, A183;
  abstract verified) find with Gaia DR3 giants that the metal-poor high-α disc "gradually spins up"
  across [M/H] ∼ −1.7 to −1.0, "a slow, monotonic spin-up phase rather than a rapid, dramatic
  spin-up" at [M/H] ∼ −1.0 "as previously inferred" (whom they mean by "previously" is not stated in
  the abstract; not verified that it refers to R22). R22's rising J_φ/J_tot is compatible with a
  gradual rise; the interpretation of the transition differs.
- *The metallicity tail is shaped by the method*: Chen et al. 2025 (arXiv:2511.18901, "The dawn is
  quiet II", Open Journal of Astrophysics; abstract verified) compare ten Gaia XP metallicity
  catalogues at −3 < [Fe/H] < −2 and find a "single-slope exponential tail" in
  every catalogue but with slopes k ≈ 0.6–2.0, which they translate into very different early gas
  reservoirs (≳10⁹ M☉ for k ≈ 0.6; best fit k ≈ 1.0, 10⁸–10⁹ M☉). The spread between catalogues shows
  that the very metal-poor end of XP metallicities is catalogue dependent. Whether their sample
  covers the inner Galaxy was not checked (abstract only).

None of these papers refutes R22's main point, an ancient, metal-poor, centrally concentrated
population; they refine its shape (flattened, power law), its rotation (small, not zero, at the
lowest metallicities; gradual spin-up) and its possible accreted component.

### Part 2 · The logic of the argument

To be written next.

### Part 3 · What astrolab can test or explore

To be written next.

### Glossary

| Term | Meaning |
|---|---|
| metallicity [M/H] | logarithm of the metal-to-hydrogen ratio relative to the Sun (0 solar, −1 one tenth, −2 one hundredth) |
| [α/Fe] | α elements (O, Mg, Si...) relative to iron, relative to the Sun; high values mean rapid early enrichment |
| Gaia XP spectra | low-resolution BP/RP prism spectra of Gaia DR3, published as 2 × 55 basis-function coefficients |
| APOGEE | Apache Point Observatory Galactic Evolution Experiment, a high-resolution infrared spectroscopic survey (SDSS DR17) |
| XGBoost | gradient-boosted decision trees, a machine-learning regression method; cannot extrapolate beyond its training labels |
| parallax ϖ | apparent annual shift of a star, ϖ [mas] = 1/distance [kpc] |
| action J_R, J_z, J_φ | orbit labels: radial and vertical excursions and angular momentum about the rotation axis |
| proto-Galaxy | the Milky Way's progenitor before the disc formed, built from early-merging clumps |
| Aurora | name (Belokurov & Kravtsov 2022) for the old, kinematically hot, in-situ population that predates the disc |
| Gaia-Sausage-Enceladus (GSE) | dwarf galaxy that merged with the Milky Way about 8–11 Gyr ago |
| Heracles / Kraken / Koala | a proposed early merger whose debris would lie deep in the inner Galaxy |
| in situ / ex situ (accreted) | born in the Milky Way itself / born in another galaxy and later accreted |
| half-mass radius | radius containing half of a cluster's mass |

### Changelog

Newest first.

- 2026-11-21: part 1 gate-1 review: exact parallax/luminosity query cut (colour-corrected G); Table 1
  vs text and Section II.4's 1.5 million added to the inconsistencies; section attributions of quotes
  and caveats; R22's "This does not necessarily imply that these mergers did not occur"; angle and
  redshift checks made exact; Zenodo authors and DOIs; Chen et al. wording; Chinese term glosses.
- 2026-11-21: part 1 drafted (plain-language walkthrough; numbers from arXiv v1, later literature
  from abstracts). Plan `design/028-plan_*`.

### Sources

- Rix et al. 2022, ApJ 941, 45, arXiv:2209.02722 (the paper studied; numbers and quotes from the arXiv HTML v1).
- Andrae, Rix, Chandra & Price-Whelan 2022, Zenodo, doi:10.5281/zenodo.7035809 (public sample; cited by R22 as ref. [85], "Rix, Chandra & Andrae"; 7035809 is presumably the concept DOI, the version v0.1 record is doi:10.5281/zenodo.7035810; landing page read 2026-11-21).
- Xiang & Rix 2022, Nature 603, 599, arXiv:2203.12110 (oldest disc age, R22's ref. [96]).
- Belokurov & Kravtsov 2022, MNRAS 514, 689, arXiv:2203.04980 (Aurora; cited by R22, not re-read here; journal reference from memory, not verified).
- Kurbatov et al. 2024, arXiv:2410.22250; Ardern-Arentsen et al. 2024, arXiv:2312.03847; Viswanathan et al. 2025, A&A 703, A183, arXiv:2411.12165; Chen et al. 2025, OJAp, arXiv:2511.18901 (later literature; abstracts read 2026-11-21).

---

## 中文

### 第一部分 · 科普详解

以下数字均取自 arXiv HTML 版（arXiv:2209.02722v1，2022 年 9 月 6 日）；我们没有与 ApJ 排版版逐行对照。下文"R22"指这篇论文。论文在不同地方对同一个量给出不同数字时，我们全部列出并注明位置。

#### 1.1 问题与意义

恒星保存着它出生时气体的化学记录。最早的恒星几乎由纯氢和氦形成；此后每一代爆发的恒星都加入更重的元素（天文学家统称为"金属"）。恒星的**金属丰度**（metallicity）[M/H] 是其金属与氢之比相对于太阳的对数：[M/H] = 0 为太阳值，−1 为十分之一，−2 为百分之一。所以极贫金属的恒星形成得很早，那时增丰还没有进行多少。

银河系最老的恒星应该在哪里？类银河系星系的宇宙学模拟（cosmological simulations）预言：最早的恒星形成于几个很早就并合成"原银河系"（proto-Galaxy，即银河系还没有盘之前的前身）的致密团块之中。这些恒星现在应当位于引力势（gravitational potential）阱最深处，靠近银心，处在热的（取向随机、不作有序转动的）轨道上。R22 摘要把这写成对大质量盘星系的预期：它们"should host an ancient, metal-poor, and centrally concentrated stellar population"（应当拥有一个古老、贫金属、向中心集中的恒星族群）。

2022 年之前这个族群很难看到。内银河系拥挤，被尘埃严重遮挡，而贫金属星在那里只占极小的少数（大多数核球星是富金属的）。早先的工作用窄带测光预选找到了这类恒星（例如 Arentsen 等的原初内银河系巡天（Pristine Inner Galaxy Survey, PIGS）），Belokurov 与 Kravtsov 2022 在太阳附近识别出一个古老、运动学上热、化学上独特的原位（in situ，在银河系内诞生的）族群，命名为**曙光**（Aurora），盘就从它当中演化出来。缺的是内银河系几千秒差距（千秒差距 kpc；1 kpc ≈ 3,260 光年）内一个大而均匀、带金属丰度与轨道的贫金属星样本。2022 年 6 月发布的 Gaia 第三次数据发布（Data Release 3, DR3）使之成为可能。

意义：如果存在一个大质量、向中心集中、非常古老的贫金属族群，它就是原银河系幸存下来的核心。它的质量、大小与转动约束了银河系在最初一二十亿年里如何组装，以及是否需要额外的早期并合（例如有人提出的"Heracles"/"Kraken"/"Koala"事件）来解释银心的老恒星。

#### 1.2 数据

**Gaia XP 光谱。** 除了位置、视差（距离）与运动，Gaia DR3 还发布了约 2.2 亿颗星的低分辨率光谱（据 Gaia DR3 文档，此处未重新核实），来自两个棱镜：蓝光度计（blue photometer, BP）与红光度计（red photometer, RP），合称 **XP**。它们不是通常意义上按波长列出的流量：每条光谱以一组光滑基函数的系数发布（BP 55 个、RP 55 个，共 110 个）。分辨率太低，测不了单条吸收线，但整体形状含有温度、表面重力、金属丰度与尘埃的信息。

**用机器学习得到金属丰度。** R22 没有用物理恒星模型拟合 XP 光谱，而是训练了一个梯度提升决策树模型（**XGBoost**），去预测高分辨率红外巡天 **APOGEE**（阿帕奇点天文台银河系演化实验，Apache Point Observatory Galactic Evolution Experiment，SDSS 第 17 次数据发布）对同一批星测得的金属丰度（第 II.2 节、附录 A.1）：

- 训练集："the *entire* SDSS DR17 APOGEE of giants with G_BP<15.5 (∼230,000 stars)"（G_BP < 15.5 的全部 SDSS DR17 APOGEE 巨星，约 230,000 颗），要求表面重力 log g < 3.5（只取巨星）；
- 输入：110 个 XP 系数；用 GaiaXPy 从 XP 光谱算出的合成窄带测光（Pristine、Strömgren、J-PLUS、SkyMapper 与 HST 色指数）；以及来自 ALLWISE（广域红外巡天探测器，Wide-field Infrared Survey Explorer 的星表）的红外星等 W1、W2；
- 输出：[M/H]（以及有效温度 T_eff 与 log g，发布在 Zenodo）；
- 精度：20 折交叉验证（cross-validation，表 1）对与所采用输入相符的表 1 一行（全部系数 + XP 色指数 + WISE）给出中位绝对误差 0.049 dex、均方根误差（root-mean-square error, RMSE）0.107 dex，但附录 A.1 说最终配置"slightly worse than the best"（比最好的略差）；与目标天区约 17,000 颗 APOGEE 星相比，在 −2.5 < [M/H] < 0.5 范围内"≲0.1 in the median"（中位数 ≲0.1），R22 称这"not a pure cross-validation"（不是纯粹的交叉验证），因为这些星在训练集中；与 LAMOST、GALAH 和 Gaia GSP-Spec 相比，均方根差（root-mean-square difference）约 0.1 dex（附录 A.2，图 8），"slight increase in scatter towards low [M/H]"（向低 [M/H] 弥散略有增大）；T_eff 与 APOGEE 的中位差为 32 K；
- 消光：直到 A_K = 0.3（约 A_V ≈ 3 星等的目视消光），估计值"at a level of a few percent"（在百分之几的水平上）无偏。

像 XGBoost 这样的树模型不能预测超出训练标签范围的值；R22 写道它"will not extrapolate [M/H] significantly beyond the APOGEE DR17 range"（不会显著外推到 APOGEE DR17 范围之外）。论文没有说明训练集中有多少颗 [M/H] < −2 的星（未核实；APOGEE 中这类星很少），也没有单独给出贫金属端的误差。

**样本**（第 II.1 节）。对 Gaia 档案做一次查询：

- 天区：|b| < 30° 且（l < 30° 或 l > 330°），即以银心为中心、银经 l 与银纬 b 方向各 60° 的方框（摘要中的"within 30°"指这个方框，不是圆锥）；
- 颜色 1.0 < BP − RP < 3.5（偏红，即低温或受红化的星），亮度 phot_bp_mean_mag < 15.5，并且有 XP 光谱（has_xp_continuous）；
- 距离与光度：`parallax < 1.`（视差小于 1 mas（毫角秒，milliarcsecond），即远于约 1 kpc）以及 `parallax < 100.*power(10.,0.2*(0.9 - (phot_g_mean_mag - 1.5*(bp_rp-1.))))`（视差以 mas 为单位）。第二个条件用一个经颜色改正、近似消红化（dereddened）的星等 G − 1.5(BP − RP − 1)，保留改正后比约 M_G = 0.9 更亮的星（高光度巨星，包括红团簇（red clump））。

这"yields 2.1 million objects"（得到 210 万个天体）。约 2% 按一个合成色指数（m1）判据作为受红化的热星去除。结果是"[M/H] estimates for about 2 million giants toward the inner Galaxy, 1.58 million of which have RVS velocities, and 1.25 million have both RVS velocities and ϖ/σ_ϖ≥5"（约 200 万颗内银河系方向巨星的 [M/H] 估计，其中 158 万颗有 RVS 速度，125 万颗同时有 RVS 速度且 ϖ/σ_ϖ ≥ 5）（RVS：Gaia 的视向速度光谱仪，Radial Velocity Spectrometer；ϖ/σ_ϖ：视差除以其误差）。

**轨道**（第 II.4 节）。对 125 万颗有视向速度（误差 δv_RVS < 5 km/s）且视差良好的星，R22 在一个四分量银河系引力势中积分轨道（Hernquist 核与核球、标长 2.6 kpc 标高 300 pc 的近似指数盘、NFW 暗晕），太阳处圆周速度 229 km/s，并用 galpy 中的"Stäckel 近似"（Stäckel fudge）计算**作用量**（action）。作用量是轨道的标签：J_R 度量径向偏移，J_z 度量竖直偏移，J_φ 是绕银河系转轴的角动量。R22 用比值 J_φ/J_tot，其中 J_tot = √(J_φ² + J_R² + J_z²)：沿类盘圆轨道运动的星接近 +1，无净转动的星接近 0（对不转动的族群取平均而言）。

**公开文件。** Zenodo 记录 7035809（doi:10.5281/zenodo.7035809，R22 所引，应是概念 DOI；版本 v0.1 为 doi:10.5281/zenodo.7035810，2022 年 9 月 2 日，CC BY 4.0，作者 Andrae、Rix、Chandra、Price-Whelan）：`xp_gc_mh.csv`（98.5 MB，MD5 7257c98622573a4a625571fc973859c5），"XGBOOST-inferred temperatures, surface gravities, and metallicities for 1.5 million stars"（150 万颗星的 XGBoost 温度、表面重力与金属丰度）；`xp_gc_kinematics.csv`（115.3 MB，MD5 b220c27aacff1f2f03d5a1f2b5fca147），120 万颗有 Gaia DR3 视向速度的星的"Galactocentric coordinates, actions, and basic orbital parameters"（银心坐标、作用量与基本轨道参数）；合计 213.8 MB。两个文件都超过本项目 50 MB 的单次下载上限；用户于 2026-11-21 同意破例（计划 [`design/028-plan_*`](https://github.com/sudoghut/astrolab/blob/main/design/028-plan_m12-poor-old-heart-paper-study.md)）。文件的列在页面上没有说明，由研究读取。

#### 1.3 一步一步：作者如何从数据走到结论

**第 1 步 · 验证金属丰度**（第 II.2–II.3 节、附录 A、图 1、8、9）。把 XP 金属丰度与 APOGEE（训练星，不独立）、三个独立光谱巡天（LAMOST、GALAH、GSP-Spec；弥散约 0.1 dex，GSP-Spec 达不到低金属丰度）以及 SkyMapper DR2 测光金属丰度（Chiti 等）比较；在 [M/H] ≈ −1.5 附近与后者符合得很差（平均偏差 0.28 dex，68% 区间约 1 dex），R22 归因于 SkyMapper 的估计。这一步的结论是 XP 金属丰度精确到约 0.1 dex，即摘要所说的 δ[M/H] ≲ 0.1。

**第 2 步 · 数贫金属星**（第 III.2 节、图 4）。整个样本的累积金属丰度分布是主要结果。各处给出的计数：

| 截断 | 第 III.2 节 | 图 4 图注 | 第 IV 节（总结） | 摘要 |
|---|---|---|---|---|
| [M/H] < −2 | >4,000 | ∼5,000 | — | — |
| [M/H] < −1.5 | ∼18,000 | ∼20,000 | ∼20,000 | −2.7 < [M/H] < −1.5 的 ∼18,000 |
| [M/H] < −1 | almost 100,000（近 100,000） | nearly 100,000（近 100,000） | ∼70,000 | — |
| 全样本 | 约 200 万（II.2） | ∼170 万 | ∼200 万 | 200 万 |

（引言与第 II.4 节写 150 万（"estimates for 1.5 million stars towards the Galactic center"，其中 125 万颗有轨道），Zenodo 说明也是 150 万；查询返回 210 万。）分布的形状：对数数密度随金属丰度上升，在约 −2 到 −1 之间 d log n/d[M/H] ≈ 1，在 −2 以下以及 −1 到 −0.6 之间更陡，在 [M/H] ≈ −0.6 附近达到峰值。尾巴止于 [M/H] ≈ −2.5 附近；R22 写道，这是"genuine metallicity floor"（真实的金属丰度下限）还是反映了 APOGEE 训练集，需要后续工作。摘要的下界 −2.7 在正文中没有解释（来源未核实）。

*粗略验算。* 如果 d log n/d[M/H] 恰好为 1，那么每 0.5 dex，低于某金属丰度的星数增大 10^0.5 ≈ 3.2 倍。从 −1.5 以下的 18,000 颗出发，预计 −2 以下约 5,700 颗，−1 以下约 57,000 颗。−2 以下的">4,000"符合文中所说 −2 以下更陡的下降；−1 以下的"∼70,000"接近幂律，而"近 100,000"需要从 −1.5 到 −1 增大约 5.5 倍，比 R22 对该区间描述的斜率更陡。这是我们的算术，不是 R22 的。

**第 3 步 · 它们在哪里？空间尺度**（第 III.1 节、图 2、3）。贫金属星太远，单颗星的距离不好：它们视差精度的中位数"only ϖ/σ_ϖ∼5"（只有约 5；全样本约 12；全样本中 1% 的视差为负）。所以 R22 没有逐颗把视差换成距离，而是假设一个模型（式 1）：恒星按银心距 R_GC 服从宽度为 σ_RGC 的**球对称高斯分布**（spherical Gaussian），每个方向、每个视差区间中预期的星数为 n(ϖ) = dΩ dϖ ϖ⁻⁴ ρ_Gauss(R(ϖ, l, b), σ_RGC)（ϖ⁻⁴ 把距离 1/ϖ 处的体积元换成视差区间）。用最大似然（maximum likelihood）拟合观测视差（含误差与 0.02 mas 的视差零点改正），对 [M/H] < −1.5 的星得到"an extent of σ_RGC∼2.7 kpc"（约 2.7 kpc 的尺度）。没有给出不确定度，没有尝试扁平形状，论文把尘埃、拥挤与视差误差的建模留作后续工作。

*粗略验算。* 从 8.2–8.5 kpc 处看，σ = 2.7 kpc 张角 ≈18°（精确为 17.6–18.2°，arctan(2.7 kpc/R0)）；R22 写的是 18°（第 III.1 节）。离银心 30° 的视场边缘在投影上距银心 4.7–4.9 kpc，不到 2σ，所以模型必须考虑视场边界（它通过对观测方向的 dΩ 考虑了）。σ = 2.7 kpc 的三维高斯把 47% 的星放在离银心 4 kpc 以内、67% 放在 5 kpc 以内，与总结中的"most stars are within 5 kpc of the Galactic center"（大多数星在离银心 5 kpc 以内）一致。

**第 4 步 · 质量多大？**（第 III.2 节）。计数的只是高光度巨星；它们代表多少恒星质量需要一个模板族群。R22 用球状星团（globular cluster）M4（一个古老、贫金属的星团）：其半质量半径（half-mass radius）6′ 以外约有 35 颗 M_G < 0.5 的巨星，总质量 7×10⁴ M☉，这"implies one giant (at M_G<0.5) per 800 M☉ of total stellar population mass"（意味着每 800 M☉ 的恒星总质量有一颗 M_G < 0.5 的巨星）。照此计算，[M/H] < −1.5 的星代表 M_tot ∼ 2×10⁷ M☉。拥挤与尘埃会遮住恒星，所以 R22 乘上"a conservative estimate"（保守估计）2.5 倍，给出下限 M_tot ≳ 5×10⁷ M☉（摘要与第 III.2 节）。总结更进一步："manifest dust obscuration implies a large correction"（明显的尘埃遮挡意味着很大的改正），提示 M* ≳ 10⁸ M☉。

*粗略验算。* 18,000–20,000 颗巨星 × 800 M☉ = 1.4–1.6×10⁷ M☉，取整为 2×10⁷（样本计数包括比 M_G = 0.5 暗、直到经颜色改正（近似消红化）的 M_G ≈ 0.9 的星，所以模板与样本截断并不完全一致）。每颗巨星对应的质量本身并不能从所引的数字推出：如果 M4 一半的质量在半质量半径以外，那里的 35 颗巨星意味着每颗约 3.5×10⁴/35 ≈ 1,000 M☉（若用全部质量则 7×10⁴/35 = 2,000），不是 800。中间步骤没有给出（我们的算术；未对照 PDF 或期刊版核实）。

**第 5 步 · 它们怎样运动？**（第 III.3 节、图 5、6）。大多数贫金属星处在热的偏心轨道上（偏心率（eccentricity）从约 0.1 到 0.8 几乎均匀分布），并留在内银河系（平均远心距（apocentre）⟨R_apo⟩ ≈ 4 kpc，第 III.3 节；总结第 IV 节："most stars have apocenters of less than 5 kpc"，大多数星的远心距小于 5 kpc）。另有一群 e ≥ 0.75、R_apo ≳ 10 kpc 的星被认定为正经过近心点（pericentre）的盖亚–香肠–恩克拉多斯（Gaia-Sausage-Enceladus, GSE）并合碎片；R22 没有定量估计这种混入。转动量 J_φ/J_tot 随金属丰度上升：摘要说"Stars with [M/H]<−2 show no net rotation"（[M/H] < −2 的星没有净转动），"those with [M/H]∼−1 are rotation dominated"（[M/H] ∼ −1 的星以转动为主）；第 III.3 节更谨慎（"starting already at [M/H]<−2 there is some, albeit small, net" rotation，即从 [M/H] < −2 开始就已有一些虽小的净转动），给出 [M/H] = −1.3 时 J_φ/J_tot ≈ 0.3，并在 −0.7 附近趋平；总结给出 [M/H] = −1.5 时 0.25、−0.8 时 ≈0.9。

**第 6 步 · 化学**（第 III.4 节、图 7）。对 APOGEE DR17 中的子样本，[α/Fe]、[Al/Fe] 与 [Mg/Mn]（α 元素由大质量恒星快速产生，相对于铁的丰度；以及用来区分银河系内诞生与吸积来的恒星的比值）表明：大多数低偏心率、[M/H] < −1 的星是 α 增丰（α-enhanced）的，即形成于快速增丰的气体；而在高偏心率处出现一条大远心距的低 α 序列（类似 GSE）。R22 指出这一判据"more ambiguous at low metallicity"（在低金属丰度时更含糊）。

**第 7 步 · 从金属丰度到年龄**（第 IV 节）。R22 没有测这些巨星的年龄；年龄估计"beyond the scope of this work"（超出本文范围；第 II 节）。年龄论证是化学的：最老的 α 增丰盘星在 [M/H] ∼ −1 处，"appear to be ≈12.5 Gyrs old"（看来约 12.5 Gyr）（参考文献 [96]，Xiang & Rix 2022；见本项目的[研究 010 文章](https://github.com/sudoghut/astrolab/blob/main/docs/wiki/Study-010-thick-disc-early-formation.md)）。比最老的盘更贫金属、"chemically, and therefore temporally, predate the oldest α-enhanced disk"（在化学上、因而在时间上早于最老的 α 增丰盘）的星，就必定形成于 τ ≳ 12.5 Gyr，"corresponding to z≳5"（对应 z ≳ 5）。这假设整个原银河系中金属丰度随时间单调上升。

*粗略验算。* 在 Planck 2018 宇宙学（宇宙年龄 13.79 Gyr）中，回溯时间（lookback time）12.5 Gyr 对应红移 z ≈ 4.6（大爆炸后 13 亿年）；"z≳5"略微向上取整（z = 5 对应回溯 12.62 Gyr）（我们用 astropy 的 Planck18 计算；R22 没有给出换算）。

#### 1.4 结论与把握程度

摘要：Gaia XP 数据在内银河系揭示了"an extensive, ancient, and metal-poor population"（一个延展、古老、贫金属的族群）：∼18,000 颗 −2.7 < [M/H] < −1.5 的星，代表 ≳5×10⁷ M☉ 的恒星，空间高斯尺度 σ ≈ 2.7 kpc；最贫金属的（[M/H] < −2）没有净转动，[M/H] ∼ −1 的以转动为主；"These central, metal-poor stars most likely predate the oldest part of the disk (τ_age≈12.5 Gyrs), which implies that they formed at z≳5"（这些中心的贫金属星很可能早于盘最老的部分（τ_age ≈ 12.5 Gyr），这意味着它们形成于 z ≳ 5）。总结（第 IV 节）称之为"the most ancient proto-Galactic component of our Galaxy"（我们银河系最古老的原银河系成分）；第 III.4 节把它与 Belokurov 和 Kravtsov 的"曙光"等同。总结论证：局限在太阳圆以内（R_GC < R☉）"against an origin through accretion from a once-distant satellite"（不支持来自一个曾经遥远的卫星星系的吸积起源）：如此低 [M/H] 下如此多强 α 增丰的恒星质量"are most likely to occur at the center of a (eventually) quite massive halo"（最可能出现在一个（最终）相当大质量的晕的中心），而不是低质量卫星星系中。由于所提出的 Heracles/Kraken/Koala 并合碎片与原银河系"曙光"的化学"virtually indistinguishable in all chemical spaces"（在所有化学空间中几乎无法区分），R22（第 III.4 节）认为他们的图景"appears to obviate the need for an ex-situ merger"（似乎无需这样一次异位并合），并补充："This does not necessarily imply that these mergers did not occur."（这并不一定意味着这些并合没有发生。）他们不声称发现了新成分："The results presented here are by no means a new distinct stellar component"（这里给出的结果绝不是一个新的独立恒星成分）。

作者给出的注意事项（总结第 IV 节称分析"in many ways preliminary"，在很多方面是初步的）：

- 空间分布"deserves to be modeled quantitatively, including the effects of dust extinction, source crowding, parallax uncertainties"（值得定量建模，包括尘埃消光、源拥挤与视差误差的影响）（第 IV 节）；
- 尘埃在离盘面 |Z| < 700 pc 处留下缺口，那里大多数星缺失（第 III.2 节），并挡住了中心 1 kpc（第 III.3 节）；
- "How pure are the XP selected samples in this regime?"（在这个区间 XP 选出的样本有多纯？）（第 IV 节）即贫金属尾巴被金属丰度估错的星污染的程度；
- −2.5 附近的 [M/H] 下限可能是真实的，也可能是 APOGEE 训练范围造成的假象（第 IV 节）；
- 距离误差可能使远心距偏高（第 III.3 节）；
- 质量依赖 M4 模板和一个"保守"改正（第 III.2 节）；
- XP 的信息"far from"（远未）被充分利用；正向建模（forward modelling）应当做得更好（第 IV 节）。

我们的阅读中要带入第二部分的要点：

- **计数内部不一致**（第 2 步的表）：−1.5 以下 ∼18,000 与 ∼20,000；−2 以下 >4,000 与 ∼5,000；−1 以下近 100,000 与 ∼70,000；样本量取决于看哪里，是 150 万（引言、第 II.4 节）、170 万（图 4）、200 万（摘要、II.2、IV）或 210 万（查询）（部分可能反映不同的子样本，例如截断前后，但论文没有说明）。
- **表 1 与正文**：所采用配置的一行（0.049 dex、0.107 dex）在表 1 中是最好的，但附录 A.1 说最终配置"slightly worse than the best"（比最好的略差）。
- **质量**在摘要中为 ≳5×10⁷ M☉，在总结中为 ≳10⁸ M☉；每颗巨星的换算（800 M☉）不能由所引的 M4 数字简单算出。
- **σ ≈ 2.7 kpc 没有不确定度**，依赖球对称高斯（无扁平）、中位精度约 5 的视差，以及一个不含尘埃与拥挤的模型。
- **"早于最老的盘"是推断，不是年龄测量**：样本中没有一颗星有年龄。它需要年轻银河系各处都有单调的年龄—金属丰度关系，而 12.5 Gyr 的盘年龄本身来自 Xiang & Rix 2022，有其绝对标尺的不确定性（见研究 010 的文章）。
- **低 [M/H] 处的金属丰度系统误差**：在极贫金属星很少的 APOGEE 上训练的 XGBoost 不能给出低于训练范围的值，而且像一般的回归模型一样，预计会把极端值拉向主体（一般性质，R22 没有测量）；[M/H] < −2 处的验证很薄弱（GSP-Spec 达不到那里；APOGEE 检验用的是训练星）。如果尾巴被金属丰度被估低的富金属星污染（样本中每颗 [M/H] < −1.5 的星对应约 100 颗更富金属的星：约 200 万颗中的 ∼18,000 颗），会抬高计数、质量，也许还有测得的尺度。
- 摘要的"**−2 以下无净转动**"与第 III.3 节的"一些虽小的"转动。

作者要错，需要什么成立：

- *计数被高估*：[M/H] < −1.5 的星中有相当一部分是 XP 金属丰度被低估的较富金属星（例如由于尘埃或拥挤），这样族群更小、质量更轻。对 XP 选出的子样本做独立光谱观测可以检验。
- *尺度不同*：把尘埃、拥挤与视场边界建模，或允许扁平形状之后，贫金属星也许不是一个紧凑的 2.7 kpc 球。Kurbatov 等 2024（arXiv:2410.22250，"The realm of Aurora"，投稿 MNRAS；已核实摘要）用 Gaia 选择函数（selection function）为 r ∼ 1 到 18 kpc、[M/H] < −1.3 的 Gaia XP 巨星建模：单分量有核幂律拟合给出"a vertical flattening of ∼0.5 and a slope −3.4"（竖直扁率约 0.5、斜率 −3.4），双分量模型更好，GSE 碎片与"曙光"在太阳附近大致各占一半，但"Aurora dominates the inner halo with a steeper power-law index of −4.5"（曙光以更陡的 −4.5 幂律指数主导内晕）。这支持"曙光"向中心集中，但它是扁的，不是球形（Rix 是合作者）。
- *这些星并非都是老的或原位的*：如果内银河系贫金属族群混有早期小卫星星系的碎片，"早于盘"与"非吸积"就会减弱。Ardern-Arentsen 等 2024（PIGS VIII，arXiv:2312.03847，已被 MNRAS 接受；已核实摘要）对 13,235 颗星做了光谱观测，发现约 60% 的极贫金属（very metal-poor, VMP，[Fe/H] < −2.0）星留在 5 kpc 以内；转动在 [Fe/H] = −1.0 到 −2.0 之间下降，但"constant for VMP stars (at ∼ 40 km/s)"（对极贫金属星保持不变，约 40 km/s）（所以极贫金属的内区星确有一些转动）；并初步（tentatively）提出两个类球（spheroidal）成分：一个较富金属、更集中、转得更快（盘形成之前的原位星或大的构建块），一个较贫金属、更延展、转得更慢（较小的吸积星系）。
- *转动加速并非看上去那样*：Viswanathan 等 2025（arXiv:2411.12165，A&A 703, A183；已核实摘要）用 Gaia DR3 巨星发现，贫金属高 α 盘在 [M/H] ∼ −1.7 到 −1.0 之间"gradually spins up"（逐渐转快），"a slow, monotonic spin-up phase rather than a rapid, dramatic spin-up"（是缓慢、单调的转快阶段，而不是）在 [M/H] ∼ −1.0 处"as previously inferred"（如以前推断的）快速、剧烈的转快（摘要没有说"以前"指谁；未核实是否指 R22）。R22 上升的 J_φ/J_tot 与逐渐上升相容；对转变的解释不同。
- *金属丰度尾巴由方法塑造*：Chen 等 2025（arXiv:2511.18901，"The dawn is quiet II"，Open Journal of Astrophysics；已核实摘要）比较了十个 Gaia XP 金属丰度星表在 −3 < [Fe/H] < −2 的部分，发现每个星表都是"single-slope exponential tail"（单一斜率的指数尾巴），但斜率 k ≈ 0.6–2.0，并把它们转换成非常不同的早期气体库（k ≈ 0.6 时 ≳10⁹ M☉；最佳拟合 k ≈ 1.0，10⁸–10⁹ M☉）。星表之间的差别表明 XP 金属丰度的极贫金属端依赖于星表。他们的样本是否覆盖内银河系未核实（只读了摘要）。

这些论文都没有推翻 R22 的主要观点，即存在一个古老、贫金属、向中心集中的族群；它们细化了它的形状（扁平、幂律）、转动（在最低金属丰度处小而非零；逐渐转快）及其可能的吸积成分。

### 第二部分 · 论证逻辑

待写。

### 第三部分 · 本项目可检验或探索的环节

待写。

### 术语表

| 术语 | 含义 |
|---|---|
| 金属丰度（metallicity）[M/H] | 金属与氢之比相对于太阳的对数（0 为太阳值，−1 为十分之一，−2 为百分之一） |
| [α/Fe] | α 元素（O、Mg、Si 等）相对于铁、再相对于太阳的丰度；高值意味着早期快速增丰 |
| Gaia XP 光谱（XP spectra） | Gaia DR3 的低分辨率 BP/RP 棱镜光谱，以 2 × 55 个基函数系数发布 |
| APOGEE | 阿帕奇点天文台银河系演化实验（Apache Point Observatory Galactic Evolution Experiment），高分辨率红外光谱巡天（SDSS DR17） |
| XGBoost | 梯度提升决策树（gradient-boosted decision trees），一种机器学习回归方法；不能外推到训练标签之外 |
| 视差（parallax）ϖ | 恒星的周年视位移，ϖ [mas] = 1/距离 [kpc] |
| 作用量（action）J_R、J_z、J_φ | 轨道标签：径向与竖直偏移，以及绕转轴的角动量 |
| 原银河系（proto-Galaxy） | 盘形成之前的银河系前身，由早期并合的团块组成 |
| 曙光（Aurora） | Belokurov 与 Kravtsov 2022 对早于盘的、古老、运动学上热的原位族群的命名 |
| 盖亚–香肠–恩克拉多斯（Gaia-Sausage-Enceladus, GSE） | 约 8–11 Gyr 前与银河系并合的矮星系 |
| Heracles / Kraken / Koala | 有人提出的一次早期并合，其碎片应深藏于内银河系 |
| 原位 / 异位（吸积）（in situ / ex situ） | 在银河系内诞生 / 在别的星系诞生、后被吸积 |
| 半质量半径（half-mass radius） | 包含星团一半质量的半径 |

### 研究进展

按时间倒序。

- 2026-11-21：第一部分闸门 1 审查：给出视差/光度查询截断的精确表达式（经颜色改正的 G）；表 1 与正文的矛盾、第 II.4 节的 150 万加入不一致清单；引文与注意事项注明所在章节；加上 R22 的"This does not necessarily imply that these mergers did not occur"；张角与红移验算改为精确值；Zenodo 作者与 DOI；Chen 等的措辞；中文术语括注英文。
- 2026-11-21：起草第一部分（科普详解；数字取自 arXiv v1，后续文献据摘要）。计划 `design/028-plan_*`。

### 来源

- Rix 等 2022，ApJ 941, 45，arXiv:2209.02722（被研究的论文；数字与引文据 arXiv HTML v1）。
- Andrae, Rix, Chandra & Price-Whelan 2022，Zenodo，doi:10.5281/zenodo.7035809（公开样本；R22 引作参考文献 [85]"Rix, Chandra & Andrae"；7035809 应是概念 DOI（concept DOI），版本 v0.1 的记录为 doi:10.5281/zenodo.7035810；2026-11-21 阅读页面）。
- Xiang & Rix 2022，Nature 603, 599，arXiv:2203.12110（最老盘的年龄，R22 的参考文献 [96]）。
- Belokurov & Kravtsov 2022，MNRAS 514, 689，arXiv:2203.04980（曙光；R22 引用，此处未重读；期刊信息凭记忆，未核实）。
- Kurbatov 等 2024，arXiv:2410.22250；Ardern-Arentsen 等 2024，arXiv:2312.03847；Viswanathan 等 2025，A&A 703, A183，arXiv:2411.12165；Chen 等 2025，OJAp，arXiv:2511.18901（后续文献；2026-11-21 阅读摘要）。
