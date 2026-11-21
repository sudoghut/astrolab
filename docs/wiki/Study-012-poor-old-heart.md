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
"proto-Galaxy", the Milky Way's progenitor before it had a disc. Many of those stars are
expected to sit today in the deepest part of the potential well, close to the Galactic Centre, on hot
(randomly oriented, not orderly rotating) orbits. R22's introduction expects the oldest, most
metal-poor stars there to be a mix: stars from the early proto-Galactic overdensities and stars from
satellites that merged later, and it notes that the distinction between the two can blur at early
times. R22's abstract puts it as an expectation for massive disc galaxies: they
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
  coefficients + XP colours + WISE), although Appendix A.1 says "this final configuration has slightly worse performance than the best configuration", with an RMS error that
  suggests "a few more outliers" (yet that row has the best RMSE in Table 1); against about 17,000
  APOGEE stars in the target region the estimates are "≲0.1 in the median" over −2.5 < [M/H] < 0.5,
  which R22 call "not a pure cross-validation" since those stars were in the training set; against
  LAMOST, GALAH and Gaia GSP-Spec the root-mean-square difference is about 0.1 dex (Appendix A.2,
  Fig. 8) with a "slight increase in scatter towards low [M/H]"; T_eff agrees with APOGEE to a
  median of 32 K;
- extinction: the estimates stay unbiased "at a level of a few percent" up to A_K = 0.3 (about
  A_V ≈ 3 magnitudes of visual extinction).

A tree model like XGBoost cannot predict values outside the range of its training labels; R22 note it
"will not extrapolate [M/H] significantly beyond the APOGEE DR17 range", and in Section IV that "the
APOGEE training set for XGBoost only extended to [M/H]=−2.5". The paper does not state how
many training stars have [M/H] < −2 (not verified; APOGEE contains few such stars), nor a separate
error at the metal-poor end.

**The sample** (Section II.1). One query to the Gaia archive:

- sky: |b| < 30° and (l < 30° or l > 330°), a 60° × 60° box in Galactic longitude l and latitude b
  centred on the Galactic Centre (the abstract's "within 30°" means this box, not a cone);
- colour 1.0 < BP − RP < 3.5 (red, i.e. cool or reddened, stars), brightness phot_bp_mean_mag < 15.5,
  and XP spectra available (has_xp_continuous);
- distance and luminosity: `parallax < 1.` (parallax below 1 mas, milliarcsecond, i.e. further than
  about 1 kpc) and `parallax < 100.*power(10.,0.2*(0.9 - (phot_g_mean_mag - 1.5*(bp_rp-1.))))` (parallax in mas). The second condition uses a colour-corrected, approximately
  dereddened (our reading) magnitude G − 1.5(BP − RP − 1) and keeps stars brighter than about M_G = 0.9 after that
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
near [M/H] ≈ −0.6. The tail ends near [M/H] ≈ −2.5; R22 write (Section IV) that whether this is a "genuine
metallicity floor" or reflects that "the APOGEE training set for XGBoost only extended to
[M/H]=−2.5" needs follow-up. The abstract's lower bound
−2.7 is not explained in the text (not verified where it comes from).

*Back-of-envelope check.* Assume (our assumption) that d log n/d[M/H] = 1 holds exactly across the
whole interval we extrapolate over, −2 to −1. Then the number below a metallicity grows by a
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
dereddened, our reading) M_G ≈ 0.9, so the template does not match
the sample cut exactly). We could not reproduce the per-giant mass from the figures quoted: assuming half of M4's mass
lies beyond its half-mass radius, 35 giants there give about 3.5×10⁴/35 ≈ 1,000 M☉ per giant
(7×10⁴/35 = 2,000 if the whole mass is used), not 800. R22 do not give the intermediate steps, so this
is an unresolved mismatch in the quoted figures, not evidence that the conversion is wrong (our
arithmetic and assumption; the PDF and journal version not checked).

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
predates the oldest α-enhanced disk", must then have formed at τ ≳ 12.5 Gyr, "corresponding to z≳5".
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
occur". They do not claim a new component: "The results presented here are by no means a new
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
  but Appendix A.1 says "this final configuration has slightly worse performance than the best configuration" and that its RMS error suggests "a few more outliers".
- **The mass** is ≳5×10⁷ M☉ in the abstract and ≳10⁸ M☉ in the summary, and its per-giant
  conversion (800 M☉) could not be reproduced from the quoted M4 figures (an unresolved mismatch
  under our assumption of half the mass outside the half-mass radius; not evidence that it is wrong).
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

#### 2.0 Map of the argument

The encoded conclusion has four parts, all in the abstract and the summary (Section IV): (1) the
metal-poor stars ([M/H] < −1.5) in the inner Galaxy amount to at least about 5×10⁷ M☉; (2) they are
centrally concentrated, most of them within 5 kpc of the Galactic Centre; (3) they formed before the
oldest disc, at least 12.5 Gyr ago (z ≳ 5); (4) they are the most ancient proto-Galactic (in-situ)
component of the Milky Way. We quote the abstract, "This sample reveals an extensive, ancient, and
metal-poor population", for the whole; part (3) is hedged in the abstract ("most likely predate the
oldest part of the disk") and part (4) in Section IV ("All of this information fits a picture in
which this metal-poor heart of the Milky Way constitutes the most ancient proto-Galactic component of
our Galaxy").

A. The XP metallicities are precise to about 0.1 dex; [gap] the metal-poor tail is not dominated by
   metal-richer stars with underestimated [M/H]; a precise and pure selection is genuine (standard)
   ⇒ the counted metal-poor stars are real.
B. About 18,000 such stars; the globular cluster M4 gives one giant per 800 M☉; [gap] that conversion
   applies to this sample ⇒ about 2×10⁷ M☉ at face value; crowding and dust make the sample
   incomplete, and a "conservative" factor 2.5 ⇒ **at least about 5×10⁷ M☉**.
C. A spherical Gaussian fitted to the parallaxes gives σ_RGC ≈ 2.7 kpc; [gap] the fit is not distorted
   by the selection it leaves out (dust, crowding, field edge, magnitude cuts) ⇒ **most stars within
   5 kpc of the Centre**.
D. Data used by stage F: no net rotation below [M/H] = −2, rotation dominated near −1; most apocentres
   below 5 kpc; the vast majority α-enhanced.
E. The old disc's metallicity distribution drops sharply below [M/H] = −1; [gap] the metal-poor stars
   and the old disc belong to one chemically connected system; in one such system metallicity rises
   with time (standard) ⇒ the metal-poor stars predate the oldest disc; the oldest disc stars are
   ≈12.5 Gyr old ⇒ **formed ≳12.5 Gyr ago, z ≳ 5**.
F. Confinement argues against a once-distant satellite; α-enhancement argues for rapid enrichment in
   a deep potential well; [gap] together with mass, age and the rotation trend, this makes the
   population **the proto-Galaxy's in-situ core** rather than debris of an accreted galaxy.

How we check it: the argument is written in Lean 4
([`studies/012-m12-poor-old-heart/argument/Argument.lean`](https://github.com/sudoghut/astrolab/blob/main/studies/012-m12-poor-old-heart/argument/Argument.lean)).
Each premise is one constructor of `Field` (no axioms), labelled with its kind and its provenance:

| Tag | Kind of premise |
|---|---|
| `OBS` | observation or measurement (with table / figure) |
| `MOD` | modelling assumption, or an inference rule the paper states |
| `STAT` | statistical inference (fit, validation, a trend read from the data) |
| `NUM` | numerical result, re-computed by this repo's `run.py` (none yet: the study has no results) |
| `LIT` | result taken from other literature |
| `GAP` | premise the inference needs that neither the paper nor standard knowledge supplies |

Provenance: `[stated: "quote"]` (the paper says it, quoted from the arXiv HTML v1), `[implied]`
(standard knowledge the paper relies on without writing it out, with a source), `[reconstructed]`
(our addition; exactly the `GAP` premises; literature published after R22 enters here, because R22
cannot rely on it).

What Lean checks: that the conclusion follows from these premises (`final`) and is not trivially
true (`final_nontrivial`); that the premises can hold together (`consistent`); that no single premise
gives the conclusion alone (`alone_insufficient`); for each premise, whether it is needed (a
countermodel without it) or redundant; whether the premises the paper actually states are enough
(`stated_*`), and whether they are enough once standard knowledge is added (`explicit_*`;
`explicit_insufficient` means a real gap). What Lean does not check: the physics and statistics inside
each premise; that is what parts 1 and 3 and the study are for.

Encoding conventions. Stated inference rules ("this implies", "leading us to a lower limit",
"the parallax distribution implies", "it must have formed") are encoded as implications; where our
analysis says the step needs more, the missing conditions are extra antecedents, which makes the
implication weaker than the quote, and they appear as separate `GAP` premises. A hedged inference is
never encoded as a stated implication: "most likely predate" becomes a gap (`gap_onezone`) plus a
standard rule (`mod_amr`); "most likely ... not at a low-mass satellite" and "fits a picture" become
the gap `gap_proto`. "Arguing against" and "arguing for" are encoded with atoms that themselves say
"disfavoured" and "favoured". Quotes cannot contain square brackets (the test's format), so phrases
with "[M/H]" are cut before or after the bracket, and what the cut leaves out is given in the source
column. R22's numbers enter as atoms (`OBS`/`STAT`), not as numbers: the study has no results yet,
so there are no `NUM` premises.

#### 2.1 Stage A · The metal-poor tail is real

*Overview.* Everything downstream counts, maps and follows stars selected by their XP metallicity.
The selection is genuine if the estimates are precise and the tail is not filled with stars that
are really more metal-rich. R22 establish the first (validation, Appendix A) and raise the second as
an open question.

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `stat_prec`: XP [M/H] agree with APOGEE and other surveys to about 0.1 dex | STAT | stated: "a remarkably precise (≲0.1 in the median)" | Section II.3 (APOGEE stars in the training set); Appendix A.2 |
| `gap_pure`: the tail below −1.5 is not dominated by metal-richer stars with underestimated [M/H] | GAP | reconstructed | R22 asks "How pure are the XP selected samples in this regime?" (Section IV); Chen et al. 2025, arXiv:2511.18901 |
| `mod_tail`: precise + pure ⇒ the metal-poor stars are genuine | MOD | implied: standard selection logic (Ivezić et al. 2014, *Statistics, Data Mining, and Machine Learning in Astronomy*) | — |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| The tail is partly metal-richer stars scattered low by the regression (dust, crowding, low S/N) | `gap_pure` | no: the question is raised, not answered; validation below −2 is thin (GSP-Spec does not reach there; the APOGEE check uses training stars) |
| The floor near −2.5 is an artefact of the training range | (shapes the tail, not encoded) | no: R22 say it needs follow-up ("the APOGEE training set for XGBoost only extended to [M/H]=−2.5") |
| SkyMapper-style systematics (0.28 dex offset, 1 dex spread near −1.5) | `stat_prec` | yes, by comparison, attributed to SkyMapper |

**Inference (Lean excerpt).**

```lean
have t : v.TailReal := p .mod_tail (p .stat_prec) (p .gap_pure)                     -- GAP
```

**Critique.** A median precision of 0.1 dex over the bulk says little about the 1% tail. The sample
has about 100 stars above [M/H] = −1.5 for each one below; a contamination rate of 1% among stars at
−1.3 to −1 would already be a sizeable fraction of the tail. A tree regressor such as XGBoost cannot
return values below its training labels, and regression estimators in general pull extreme values
towards the bulk; both effects shape the tail, in opposite directions (fewer stars appear below
−2.5, some stars from −1.3 may appear below −1.5). Chen et al. 2025 find that ten XP metallicity
catalogues disagree on the slope of the tail below [Fe/H] = −2 (k ≈ 0.6–2.0). Purity is therefore
the first gap, and every part of the conclusion depends on it.

#### 2.2 Stage B · How many stars and how much mass

*Overview.* About 18,000 stars below −1.5 are counted (Section III.2; about 20,000 in Fig. 4 and
Section IV). A template converts luminous giants into total stellar mass: in M4, one giant with
M_G < 0.5 per 800 M☉. At face value this gives about 2×10⁷ M☉; the sample is incomplete in crowded
fields and behind dust, and a "conservative" factor 2.5 gives the lower limit ≳5×10⁷ M☉.

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `obs_count`: about 18,000 stars with [M/H] < −1.5 | OBS | stated: "that includes ∼18,000 stars" | Abstract (Section III.2; Fig. 4 and Section IV: ∼20,000) |
| `mod_m4`: in M4, one giant (M_G < 0.5) per 800 M☉ | MOD | stated: "per 800 M⊙ of total stellar population mass" | Section III.2 |
| `gap_template`: the M4 conversion applies to this sample | GAP | reconstructed | sample cut at colour-corrected M_G ≈ 0.9, not 0.5; 800 M☉ not reproduced from the quoted M4 numbers |
| `mod_face`: genuine tail + count + M4 ratio (+ template) ⇒ about 2×10⁷ M☉ at face value | MOD | stated: "At face value, this implies" | Section III.2 |
| `obs_incomplete`: XP spectra are missing in crowded fields, dust hides stars | OBS | stated: "But this does not account for the incompleteness of XP spectra in very crowded fields" | Section III.2 |
| `mod_corr`: face-value mass + incompleteness ⇒ ≳5×10⁷ M☉ | MOD | stated: "A conservative estimate of these effects is a factor of 2.5, leading us to a lower limit on the mass of" | Section III.2 |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| The count is inflated by contamination (stage A) | `mod_face` needs `TailReal` | no |
| The luminosity range or the population (age, mass function) differs from M4 | `gap_template` | no |
| The incompleteness factor is smaller than 2.5 | `mod_corr` | stated as "conservative", no derivation |

**Inference (Lean excerpt).**

```lean
have fm : v.FaceMass := p .mod_face t (p .obs_count) (p .mod_m4) (p .gap_template)  -- GAP
have m : v.Massive := p .mod_corr fm (p .obs_incomplete)
```

**Critique.** Three numbers are combined, each with a soft spot. The count differs between sections
(18,000 or 20,000). The conversion of 800 M☉ per giant does not follow from the M4 numbers quoted
(35 giants beyond the half-mass radius, 7×10⁴ M☉ in total; half of the mass beyond that radius
gives about 1,000 M☉ per giant, all of it about 2,000), and the sample includes giants fainter than
the template's M_G = 0.5 limit, which should lower the mass per counted giant; these partly
cancel and are not discussed. The factor 2.5 is called conservative without a derivation, and
the summary goes further (M* ≳ 10⁸ M☉). The lower limit is only a lower limit if the count is not
inflated by contamination: contamination and incompleteness push in opposite directions, and only
one of them is corrected. Of order 10⁷–10⁸ M☉ is robust to all of this; the factor between those is
not.

#### 2.3 Stage C · Central concentration

*Overview.* With parallax precision of about 5 for these stars, R22 do not map individual
distances. They fit a spherical Gaussian in Galactocentric radius to the parallaxes by maximum
likelihood (eq. 1) and find σ_RGC ≈ 2.7 kpc; the summary turns this into "most stars are within
5 kpc of the Galactic center".

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `mod_sph`: the 3D distribution is a spherical Gaussian in R_GC | MOD | stated: "We assume that the 3D distribution is a spherical Gaussian as a function of Galactocentric radius" | Section III.1, eq. 1 |
| `stat_sigma`: the maximum-likelihood fit gives σ_RGC ≈ 2.7 kpc | STAT | stated: "We find that the maximum likelihood of the observed parallaxes (and their uncertainties) for the" | Section III.1 (continues: "[M/H]<−1.5 stars implies an extent of σ_RGC∼2.7 kpc"; no uncertainty) |
| `gap_sel`: the fit is not distorted by the selection it leaves out | GAP | reconstructed | R22 Section IV (to be "modeled quantitatively"); Kurbatov et al. 2024, arXiv:2410.22250 |
| `mod_central`: genuine tail + model + fit (+ selection) ⇒ most stars within 5 kpc | MOD | stated: "the parallax distribution implies that most stars are within 5 kpc of the Galactic center" | Section IV (Figure 3) |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| The extent is set by the field (60° × 60° box, edge at 4.7–4.9 kpc) | `mod_sph` (eq. 1 integrates over the observed directions) | yes, in the model |
| Dust removes stars within 700 pc of the plane and the central kpc; crowding; the BP < 15.5 and luminosity cuts select by distance | `gap_sel` | no: listed as future work |
| The population is flattened or follows a power law, not a sphere | `gap_sel`, `mod_sph` | no; Kurbatov et al. 2024 find flattening ≈0.5 and an Aurora slope of −4.5 |
| Parallax zero-point errors bias σ | `stat_sigma` (0.02 mas correction) | partly |

**Inference (Lean excerpt).**

```lean
have c : v.Central := p .mod_central t (p .mod_sph) (p .stat_sigma) (p .gap_sel)    -- GAP
```

**Critique.** "Centrally concentrated" is robust in the qualitative sense: the stars' parallaxes
put most of them near the Centre, and orbits (stage D) confine them. The number σ ≈ 2.7 kpc is
fragile: it has no uncertainty, rests on a shape (sphere, Gaussian) that later work with a
selection function does not prefer, and the selection that matters most (dust near the plane,
crowding, magnitude limits that change with distance) is not in the likelihood. A selection that
removes nearby-plane and central stars and keeps distant ones at higher latitude could change σ
either way. The 5 kpc statement follows from σ ≈ 2.7 kpc (a 3D Gaussian puts 67% within 5 kpc,
part 1.3), so it inherits this gap.

#### 2.4 Stage D · Kinematics and chemistry (the data for stage F)

*Overview.* For about 1.25 million stars with RVS velocities and good parallaxes, R22 compute
orbits. The metal-poor stars are on hot orbits that stay inside about 5 kpc; the rotation
measure J_φ/J_tot rises with metallicity, from no net rotation below −2 to rotation dominated near
−1. In the APOGEE subset, the vast majority of stars below −1.5 are α-enhanced.

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `stat_norot`: no net rotation for [M/H] < −2 | STAT | stated: "show no net rotation, whereas those with" | Abstract (Section III.3: "some, albeit small, net" rotation already below −2) |
| `stat_spin`: rotation dominated near [M/H] ≈ −1 | STAT | stated: "are rotation dominated" | Abstract (J_φ/J_tot ≈ 0.3 at −1.3, III.3; 0.25 at −1.5, ≈0.9 at −0.8, IV) |
| `stat_apo`: most apocentres below 5 kpc | STAT | stated: "most stars have apocenters of less than 5 kpc" | Section IV (⟨R_apo⟩ ≈ 4 kpc, III.3) |
| `stat_alpha`: the vast majority of stars below −1.5 are α-enhanced | STAT | stated: "are distinctly α-enhanced, arguing for rapid enrichment in a deep potential well" | Section IV (APOGEE DR17 subset; the inference part is `mod_deepwell`) |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| Very metal-poor inner stars do rotate (about 40 km/s) | `stat_norot` | no; R22's own Section III.3 says "some, albeit small"; Ardern-Arentsen et al. 2024 |
| The RVS subsample (brighter, nearer) is not representative of the metal-poor population | (not encoded) | no |
| Apocentres biased by distance errors | `stat_apo` | mentioned (biased high, Section III.3), which makes "< 5 kpc" conservative |
| GSE stars passing pericentre contaminate the inner sample | (not encoded; feeds `gap_proto`) | partly: e ≥ 0.75, R_apo ≳ 10 kpc identified, not quantified |

**Critique.** These four facts are data, not inferences, and are encoded as such. Two remarks.
"No net rotation" (abstract) is stronger than the body of the paper (III.3: small rotation already
below −2); a later spectroscopic survey finds a constant ~40 km/s for very metal-poor inner stars.
For the proto-Galaxy argument a slow, non-zero rotation changes little; for a sharp "spin-up" at
one metallicity it matters (Viswanathan et al. 2025 find a gradual spin-up from −1.7 to −1.0).

#### 2.5 Stage E · Older than the disc

*Overview.* R22 measure no ages. The age argument is chemical. The old α-enhanced disc's
metallicity distribution drops sharply below [M/H] = −1, and its oldest members, near −1, are about
12.5 Gyr old (Xiang & Rix 2022). If the metal-poor heart "chemically, and therefore temporally,
predates" that disc, "it must have formed at τ≳12.5 Gyrs, corresponding to z≳5". The step from
lower metallicity to earlier formation is hedged in the abstract ("most likely predate").

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `obs_discfloor`: the old disc's metallicity distribution drops sharply below −1 | OBS | stated: "However, the old α-enhanced disk metallicity distribution function (MDF) is truncated, or at least drops sharply, below" | Section I |
| `gap_onezone`: the metal-poor stars and the old disc belong to one chemically connected system | GAP | reconstructed | R22 hedges ("most likely predate"); R22 Section I expects a mix with later-merged satellites; Ardern-Arentsen et al. 2024, arXiv:2312.03847 |
| `mod_amr`: in one system, metallicity rises with time ⇒ more metal-poor than the oldest disc means earlier | MOD | implied: one-zone chemical evolution (Tinsley 1980, 1980FCPh....5..287T) | — |
| `lit_discage`: the oldest disc stars are ≈12.5 Gyr old | LIT | stated: "appear to be ≈12.5 Gyrs old" | Section IV; ref. [96], Xiang & Rix 2022, arXiv:2203.12110 |
| `mod_ancient`: predates + disc age ⇒ formed ≳12.5 Gyr ago, z ≳ 5 | MOD | stated: "it must have formed at τ≳12.5 Gyrs, corresponding to z≳5" | Section IV (a conditional: "If much of this metal-poor heart ...") |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| Some metal-poor stars formed later in slowly enriching systems (dwarf galaxies accreted after the disc began) | `gap_onezone` | no; R22's own introduction expects such a mix |
| Inhomogeneous enrichment within the proto-Galaxy (pockets of low-metallicity gas forming stars late) | `gap_onezone` | no |
| The absolute age of the oldest disc is smaller (a different isochrone scale) | `lit_discage` | no; Chen, Sun & Ye 2025 find subgiant ages ~13% younger (see the Study 010 article) |
| "z ≳ 5" from 12.5 Gyr | `mod_ancient` | stated; in Planck 2018, 12.5 Gyr lookback is z ≈ 4.6 (part 1.3) |

**Inference (Lean excerpt).**

```lean
have pd : v.Predates := p .mod_amr (p .gap_onezone) t (p .obs_discfloor)           -- GAP
have a : v.Ancient := p .mod_ancient pd (p .lit_discage)
```

**Critique.** "Predate the oldest disk" is an inference, not an age measurement, and it needs one
chemically connected system with monotonic enrichment. That is standard for a single well-mixed gas
reservoir, but the early Milky Way was not one: R22's own introduction expects the oldest metal-poor
stars to mix early proto-Galactic pieces with satellites that merged later, and a slowly enriching
dwarf can form stars below −1.5 after the oldest disc stars at −1 formed. The argument is
statistical ("much of"), so it survives some such stars, but how many is exactly what is not known.
The 12.5 Gyr also carries the absolute-age uncertainty of the subgiant ages it comes from, and
"z ≳ 5" rounds z ≈ 4.6 up.

#### 2.6 Stage F · A proto-Galactic, in-situ core

*Overview.* Two arguments of Section IV and the kinematic trend lead to the interpretation. The
population is confined within the solar circle, tightly bound ("arguing against an origin through
accretion from a once-distant satellite"). The vast majority of its stars are α-enhanced ("arguing
for rapid enrichment in a deep potential well"), and such a mass of α-enhanced stars at such low
metallicity is "most likely" found "at the center of a (eventually) quite massive halo, not at a
low-mass satellite". With the age (stage E) and the rotation trend, "All of this information fits a
picture" of the most ancient proto-Galactic component.

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `mod_confined`: central + small apocentres ⇒ a once-distant satellite is disfavoured | MOD | stated: "arguing against an origin through accretion from a once-distant satellite" | Section IV |
| `mod_deepwell`: α-enhanced ⇒ rapid enrichment in a deep well is favoured | MOD | stated: "are distinctly α-enhanced, arguing for rapid enrichment in a deep potential well" | Section IV |
| `gap_proto`: mass + age + confinement + deep well + rotation trend ⇒ the proto-Galaxy's in-situ core | GAP | reconstructed | R22 hedges ("most likely", "fits a picture"); Heracles/Kraken/Koala "virtually indistinguishable" (III.4); Ardern-Arentsen et al. 2024 |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| Debris of a once-distant satellite (e.g. GSE) | `mod_confined` | yes (argued against); high-eccentricity GSE stars set aside |
| Debris of an early, massive accreted galaxy that sank to the centre (Heracles / Kraken / Koala) | `gap_proto` | no: chemically "virtually indistinguishable"; R22's picture "appears to obviate the need" for it, but "This does not necessarily imply that these mergers did not occur" |
| A mix: a concentrated, faster-rotating in-situ component plus a more extended, more metal-poor, slower component from smaller galaxies | `gap_proto` | no; proposed tentatively by Ardern-Arentsen et al. 2024 |
| In situ and early accreted are not separable at all | `gap_proto` | stated by R22 as a possibility (Section I: "it may be operationally impossible ...") |

**Inference (Lean excerpt).**

```lean
have nd : v.NotDistant := p .mod_confined c (p .stat_apo)
have dw : v.DeepWell := p .mod_deepwell (p .stat_alpha)
have pg : v.ProtoGal :=
  p .gap_proto m a nd dw (p .stat_norot) (p .stat_spin)                               -- GAP
exact ⟨m, c, a, pg⟩
```

**Critique.** The interpretation is a plausibility argument and R22 present it as one ("fits a
picture"). Confinement excludes a satellite that fell in from far away; it does not exclude one that
merged early and sank by dynamical friction, which is what Heracles/Kraken/Koala is proposed to be,
and R22 grant that the chemistry cannot tell the two apart. Part of the issue is definitional: if
the proto-Galaxy is built from "comparable-mass pieces" coalescing early (R22's introduction), the
line between an in-situ core and an early massive merger is a matter of mass ratio and timing. What
the data support firmly is that the population is old (in the chemical sense of stage E), centrally
concentrated, α-enhanced and kinematically hot; "proto-Galactic" is the interpretation of that
combination, and it rests on `gap_proto`.

#### 2.7 Claims discussed, not encoded

- **The internal inconsistencies** (part 1.4): counts (18,000 or 20,000 below −1.5; >4,000 or ∼5,000
  below −2; almost 100,000 or ∼70,000 below −1), sample size (1.5 to 2.1 million), mass (≳5×10⁷ or
  ≳10⁸ M☉), the Table 1 row versus the text. They do not change the logic and are not encoded; part 3
  can recount from the public files.
- **The [M/H] floor near −2.5** (Section IV) and its link to the training range: a property of the
  tail's shape, discussed under stage A.
- **The rotation trend's exact form** (J_φ/J_tot values per metallicity): encoded only as its two
  ends (no rotation below −2, rotation dominated near −1).
- **"Not a new distinct stellar component"**: R22 identify the heart with the tightly bound core of
  Belokurov & Kravtsov's Aurora; this naming is part of `gap_proto`'s interpretation.

#### 2.8 What the Lean check found

1. **Headline: `explicit_insufficient`, with five gaps.** Even with the two standard rules added
   (`mod_tail`, `mod_amr`), the conclusion does not follow without: the purity of the metal-poor tail
   (`gap_pure`), the applicability of the M4 conversion (`gap_template`), the absence of distortion by
   the unmodelled selection (`gap_sel`), one chemically connected system for the age ordering
   (`gap_onezone`) and the in-situ interpretation (`gap_proto`).
2. **`stated_insufficient`**: what R22 write is not enough even before the gaps. The argument also
   uses two standard rules it does not write out: a precise and pure selection gives genuine
   members (`mod_tail`), and in one system metallicity rises with time (`mod_amr`).
3. **Where the gaps sit.** `gap_pure` reaches all four parts (mass, concentration and age all use the
   genuine tail; the interpretation uses all three). Part (1), the mass, adds `gap_template`; part
   (2), the concentration, adds `gap_sel`; part (3), the age, adds `gap_onezone`; part (4), the
   proto-Galaxy, adds `gap_proto` and inherits every other gap. Two of the gaps (`gap_onezone`,
   `gap_proto`) are steps R22 themselves hedge ("most likely", "fits a picture"); the other three
   are steps R22 take without comment (`gap_template`) or flag as future work (`gap_pure`,
   `gap_sel`).
4. **Ranking.** `gap_pure` matters most (it reaches everything and the paper gives no number for
   it); then `gap_onezone` (the age claim is the paper's headline); `gap_proto` is largely
   interpretive; `gap_sel` affects the number σ ≈ 2.7 kpc more than the qualitative concentration;
   `gap_template` affects the mass by a factor of order 2.
5. **All 25 premises are needed** in this encoding; none is redundant (each sits on a single chain).
   The four stage D facts are needed only through the interpretive steps (`mod_confined`,
   `mod_deepwell`, `gap_proto`).
6. **Consistency** (`consistent`) is weak here: no premise is negative, so the all-true model
   satisfies them trivially.
7. **How the encoding departs from the quotes.** `mod_face`, `mod_central`, `mod_confined` and
   `mod_ancient` carry extra antecedents (weaker than the quotes). `mod_ancient` encodes a conditional
   sentence of R22 as the conditional it is. Quotes with "[M/H]" are cut before or after the bracket;
   the text left out is given in each source column. Hedged steps are gaps, not stated implications.
8. **Limits.** Lean checks the logical structure under our encoding, not the statistics inside each
   premise; the paper's numbers (counts, σ, mass, ages) enter as atoms, and "needed" means "used by
   this encoding".

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

- 2026-11-21: part 2 drafted (logic of the argument in six stages; `Argument.lean`: 25 premises,
  5 gaps, 2 implied; `stated_insufficient` and `explicit_insufficient`).
- 2026-11-21: part 1 gate-2 (Codex): no serious issues; three wording minors (R22's expected mix of
  proto-Galactic and accreted stars, the slope assumption of the count check, the 800 M☉ point as an
  unresolved mismatch).
- 2026-11-21: part 1 gate-1 review: exact parallax/luminosity query cut (colour-corrected G); Table 1
  vs text and Section II.4's 1.5 million added to the inconsistencies; section attributions of quotes
  and caveats; R22's "This does not necessarily imply that these mergers did not occur"; angle and
  redshift checks made exact; Zenodo authors and DOIs; Chen et al. wording; Chinese term glosses;
  round 2: exact Appendix A.1 quote ("slightly worse performance", "a few more outliers"), "predates",
  "our reading" for the dereddening, Section IV's training-range quote (−2.5), quote punctuation.
- 2026-11-21: part 1 drafted (plain-language walkthrough; numbers from arXiv v1, later literature
  from abstracts). Plan `design/028-plan_*`.

### Sources

- Rix et al. 2022, ApJ 941, 45, arXiv:2209.02722 (the paper studied; numbers and quotes from the arXiv HTML v1).
- Andrae, Rix, Chandra & Price-Whelan 2022, Zenodo, doi:10.5281/zenodo.7035809 (public sample; cited by R22 as ref. [85], "Rix, Chandra & Andrae"; 7035809 is presumably the concept DOI, the version v0.1 record is doi:10.5281/zenodo.7035810; landing page read 2026-11-21).
- Xiang & Rix 2022, Nature 603, 599, arXiv:2203.12110 (oldest disc age, R22's ref. [96]).
- Tinsley 1980, Fundamentals of Cosmic Physics 5, 287, 1980FCPh....5..287T; Ivezić, Connolly, VanderPlas & Gray 2014, *Statistics, Data Mining, and Machine Learning in Astronomy* (standard background of the two `[implied]` premises in part 2).
- Chen, Sun & Ye 2025, arXiv:2510.10092 (younger subgiant age scale; via the Study 010 article).
- Belokurov & Kravtsov 2022, MNRAS 514, 689, arXiv:2203.04980 (Aurora; cited by R22, not re-read here; journal reference from memory, not verified).
- Kurbatov et al. 2024, arXiv:2410.22250; Ardern-Arentsen et al. 2024, arXiv:2312.03847; Viswanathan et al. 2025, A&A 703, A183, arXiv:2411.12165; Chen et al. 2025, OJAp, arXiv:2511.18901 (later literature; abstracts read 2026-11-21).

---

## 中文

### 第一部分 · 科普详解

以下数字均取自 arXiv HTML 版（arXiv:2209.02722v1，2022 年 9 月 6 日）；我们没有与 ApJ 排版版逐行对照。下文"R22"指这篇论文。论文在不同地方对同一个量给出不同数字时，我们全部列出并注明位置。

#### 1.1 问题与意义

恒星保存着它出生时气体的化学记录。最早的恒星几乎由纯氢和氦形成；此后每一代爆发的恒星都加入更重的元素（天文学家统称为"金属"）。恒星的**金属丰度**（metallicity）[M/H] 是其金属与氢之比相对于太阳的对数：[M/H] = 0 为太阳值，−1 为十分之一，−2 为百分之一。所以极贫金属的恒星形成得很早，那时增丰还没有进行多少。

银河系最老的恒星应该在哪里？类银河系星系的宇宙学模拟（cosmological simulations）预言：最早的恒星形成于几个很早就并合成"原银河系"（proto-Galaxy，即银河系还没有盘之前的前身）的致密团块之中。预计其中许多恒星今天位于引力势（gravitational potential）阱最深处，靠近银心，处在热的（取向随机、不作有序转动的）轨道上。R22 的引言预期那里最老、最贫金属的恒星是混合的：既有来自早期原银河系高密度团块（overdensities）的星，也有来自较晚并合的卫星星系的星，并指出两者的区分在早期可能变得模糊。R22 摘要把这写成对大质量盘星系的预期：它们"should host an ancient, metal-poor, and centrally concentrated stellar population"（应当拥有一个古老、贫金属、向中心集中的恒星族群）。

2022 年之前这个族群很难看到。内银河系拥挤，被尘埃严重遮挡，而贫金属星在那里只占极小的少数（大多数核球星是富金属的）。早先的工作用窄带测光预选找到了这类恒星（例如 Arentsen 等的原初内银河系巡天（Pristine Inner Galaxy Survey, PIGS）），Belokurov 与 Kravtsov 2022 在太阳附近识别出一个古老、运动学上热、化学上独特的原位（in situ，在银河系内诞生的）族群，命名为**曙光**（Aurora），盘就从它当中演化出来。缺的是内银河系几千秒差距（千秒差距 kpc；1 kpc ≈ 3,260 光年）内一个大而均匀、带金属丰度与轨道的贫金属星样本。2022 年 6 月发布的 Gaia 第三次数据发布（Data Release 3, DR3）使之成为可能。

意义：如果存在一个大质量、向中心集中、非常古老的贫金属族群，它就是原银河系幸存下来的核心。它的质量、大小与转动约束了银河系在最初一二十亿年里如何组装，以及是否需要额外的早期并合（例如有人提出的"Heracles"/"Kraken"/"Koala"事件）来解释银心的老恒星。

#### 1.2 数据

**Gaia XP 光谱。** 除了位置、视差（距离）与运动，Gaia DR3 还发布了约 2.2 亿颗星的低分辨率光谱（据 Gaia DR3 文档，此处未重新核实），来自两个棱镜：蓝光度计（blue photometer, BP）与红光度计（red photometer, RP），合称 **XP**。它们不是通常意义上按波长列出的流量：每条光谱以一组光滑基函数的系数发布（BP 55 个、RP 55 个，共 110 个）。分辨率太低，测不了单条吸收线，但整体形状含有温度、表面重力、金属丰度与尘埃的信息。

**用机器学习得到金属丰度。** R22 没有用物理恒星模型拟合 XP 光谱，而是训练了一个梯度提升决策树模型（**XGBoost**），去预测高分辨率红外巡天 **APOGEE**（阿帕奇点天文台银河系演化实验，Apache Point Observatory Galactic Evolution Experiment，SDSS 第 17 次数据发布）对同一批星测得的金属丰度（第 II.2 节、附录 A.1）：

- 训练集："the *entire* SDSS DR17 APOGEE of giants with G_BP<15.5 (∼230,000 stars)"（G_BP < 15.5 的全部 SDSS DR17 APOGEE 巨星，约 230,000 颗），要求表面重力 log g < 3.5（只取巨星）；
- 输入：110 个 XP 系数；用 GaiaXPy 从 XP 光谱算出的合成窄带测光（Pristine、Strömgren、J-PLUS、SkyMapper 与 HST 色指数）；以及来自 ALLWISE（广域红外巡天探测器，Wide-field Infrared Survey Explorer 的星表）的红外星等 W1、W2；
- 输出：[M/H]（以及有效温度 T_eff 与 log g，发布在 Zenodo）；
- 精度：20 折交叉验证（cross-validation，表 1）对与所采用输入相符的表 1 一行（全部系数 + XP 色指数 + WISE）给出中位绝对误差 0.049 dex、均方根误差（root-mean-square error, RMSE）0.107 dex，但附录 A.1 说"this final configuration has slightly worse performance than the best configuration"（这一最终配置的表现比最好的配置略差），其 RMS 误差提示"a few more outliers"（多一些离群值）（而这一行在表 1 中 RMSE 最好）；与目标天区约 17,000 颗 APOGEE 星相比，在 −2.5 < [M/H] < 0.5 范围内"≲0.1 in the median"（中位数 ≲0.1），R22 称这"not a pure cross-validation"（不是纯粹的交叉验证），因为这些星在训练集中；与 LAMOST、GALAH 和 Gaia GSP-Spec 相比，均方根差（root-mean-square difference）约 0.1 dex（附录 A.2，图 8），"slight increase in scatter towards low [M/H]"（向低 [M/H] 弥散略有增大）；T_eff 与 APOGEE 的中位差为 32 K；
- 消光：直到 A_K = 0.3（约 A_V ≈ 3 星等的目视消光），估计值"at a level of a few percent"（在百分之几的水平上）无偏。

像 XGBoost 这样的树模型不能预测超出训练标签范围的值；R22 写道它"will not extrapolate [M/H] significantly beyond the APOGEE DR17 range"（不会显著外推到 APOGEE DR17 范围之外），并在第 IV 节写道"the APOGEE training set for XGBoost only extended to [M/H]=−2.5"（XGBoost 的 APOGEE 训练集只延伸到 [M/H] = −2.5）。论文没有说明训练集中有多少颗 [M/H] < −2 的星（未核实；APOGEE 中这类星很少），也没有单独给出贫金属端的误差。

**样本**（第 II.1 节）。对 Gaia 档案做一次查询：

- 天区：|b| < 30° 且（l < 30° 或 l > 330°），即以银心为中心、银经 l 与银纬 b 方向各 60° 的方框（摘要中的"within 30°"指这个方框，不是圆锥）；
- 颜色 1.0 < BP − RP < 3.5（偏红，即低温或受红化的星），亮度 phot_bp_mean_mag < 15.5，并且有 XP 光谱（has_xp_continuous）；
- 距离与光度：`parallax < 1.`（视差小于 1 mas（毫角秒，milliarcsecond），即远于约 1 kpc）以及 `parallax < 100.*power(10.,0.2*(0.9 - (phot_g_mean_mag - 1.5*(bp_rp-1.))))`（视差以 mas 为单位）。第二个条件用一个经颜色改正、近似消红化（dereddened；这是我们的解读）的星等 G − 1.5(BP − RP − 1)，保留改正后比约 M_G = 0.9 更亮的星（高光度巨星，包括红团簇（red clump））。

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

（引言与第 II.4 节写 150 万（"estimates for 1.5 million stars towards the Galactic center"，其中 125 万颗有轨道），Zenodo 说明也是 150 万；查询返回 210 万。）分布的形状：对数数密度随金属丰度上升，在约 −2 到 −1 之间 d log n/d[M/H] ≈ 1，在 −2 以下以及 −1 到 −0.6 之间更陡，在 [M/H] ≈ −0.6 附近达到峰值。尾巴止于 [M/H] ≈ −2.5 附近；R22 写道（第 IV 节），这是"genuine metallicity floor"（真实的金属丰度下限），还是反映了"the APOGEE training set for XGBoost only extended to [M/H]=−2.5"（XGBoost 的 APOGEE 训练集只延伸到 [M/H] = −2.5），需要后续工作。摘要的下界 −2.7 在正文中没有解释（来源未核实）。

*粗略验算。* 假设（我们的假设）d log n/d[M/H] = 1 在我们外推的整个区间（−2 到 −1）都严格成立，那么每 0.5 dex，低于某金属丰度的星数增大 10^0.5 ≈ 3.2 倍。从 −1.5 以下的 18,000 颗出发，预计 −2 以下约 5,700 颗，−1 以下约 57,000 颗。−2 以下的">4,000"符合文中所说 −2 以下更陡的下降；−1 以下的"∼70,000"接近幂律，而"近 100,000"需要从 −1.5 到 −1 增大约 5.5 倍，比 R22 对该区间描述的斜率更陡。这是我们的算术，不是 R22 的。

**第 3 步 · 它们在哪里？空间尺度**（第 III.1 节、图 2、3）。贫金属星太远，单颗星的距离不好：它们视差精度的中位数"only ϖ/σ_ϖ∼5"（只有约 5；全样本约 12；全样本中 1% 的视差为负）。所以 R22 没有逐颗把视差换成距离，而是假设一个模型（式 1）：恒星按银心距 R_GC 服从宽度为 σ_RGC 的**球对称高斯分布**（spherical Gaussian），每个方向、每个视差区间中预期的星数为 n(ϖ) = dΩ dϖ ϖ⁻⁴ ρ_Gauss(R(ϖ, l, b), σ_RGC)（ϖ⁻⁴ 把距离 1/ϖ 处的体积元换成视差区间）。用最大似然（maximum likelihood）拟合观测视差（含误差与 0.02 mas 的视差零点改正），对 [M/H] < −1.5 的星得到"an extent of σ_RGC∼2.7 kpc"（约 2.7 kpc 的尺度）。没有给出不确定度，没有尝试扁平形状，论文把尘埃、拥挤与视差误差的建模留作后续工作。

*粗略验算。* 从 8.2–8.5 kpc 处看，σ = 2.7 kpc 张角 ≈18°（精确为 17.6–18.2°，arctan(2.7 kpc/R0)）；R22 写的是 18°（第 III.1 节）。离银心 30° 的视场边缘在投影上距银心 4.7–4.9 kpc，不到 2σ，所以模型必须考虑视场边界（它通过对观测方向的 dΩ 考虑了）。σ = 2.7 kpc 的三维高斯把 47% 的星放在离银心 4 kpc 以内、67% 放在 5 kpc 以内，与总结中的"most stars are within 5 kpc of the Galactic center"（大多数星在离银心 5 kpc 以内）一致。

**第 4 步 · 质量多大？**（第 III.2 节）。计数的只是高光度巨星；它们代表多少恒星质量需要一个模板族群。R22 用球状星团（globular cluster）M4（一个古老、贫金属的星团）：其半质量半径（half-mass radius）6′ 以外约有 35 颗 M_G < 0.5 的巨星，总质量 7×10⁴ M☉，这"implies one giant (at M_G<0.5) per 800 M☉ of total stellar population mass"（意味着每 800 M☉ 的恒星总质量有一颗 M_G < 0.5 的巨星）。照此计算，[M/H] < −1.5 的星代表 M_tot ∼ 2×10⁷ M☉。拥挤与尘埃会遮住恒星，所以 R22 乘上"a conservative estimate"（保守估计）2.5 倍，给出下限 M_tot ≳ 5×10⁷ M☉（摘要与第 III.2 节）。总结更进一步："manifest dust obscuration implies a large correction"（明显的尘埃遮挡意味着很大的改正），提示 M* ≳ 10⁸ M☉。

*粗略验算。* 18,000–20,000 颗巨星 × 800 M☉ = 1.4–1.6×10⁷ M☉，取整为 2×10⁷（样本计数包括比 M_G = 0.5 暗、直到经颜色改正（近似消红化，我们的解读）的 M_G ≈ 0.9 的星，所以模板与样本截断并不完全一致）。我们无法用所引的数字复现每颗巨星对应的质量：假设 M4 一半的质量在半质量半径以外，那里的 35 颗巨星给出每颗约 3.5×10⁴/35 ≈ 1,000 M☉（若用全部质量则 7×10⁴/35 = 2,000），不是 800。R22 没有给出中间步骤，所以这是所引数字之间一个尚未解决的不符，而不是换算有误的证据（我们的算术与假设；未核对 PDF 与期刊版）。

**第 5 步 · 它们怎样运动？**（第 III.3 节、图 5、6）。大多数贫金属星处在热的偏心轨道上（偏心率（eccentricity）从约 0.1 到 0.8 几乎均匀分布），并留在内银河系（平均远心距（apocentre）⟨R_apo⟩ ≈ 4 kpc，第 III.3 节；总结第 IV 节："most stars have apocenters of less than 5 kpc"，大多数星的远心距小于 5 kpc）。另有一群 e ≥ 0.75、R_apo ≳ 10 kpc 的星被认定为正经过近心点（pericentre）的盖亚–香肠–恩克拉多斯（Gaia-Sausage-Enceladus, GSE）并合碎片；R22 没有定量估计这种混入。转动量 J_φ/J_tot 随金属丰度上升：摘要说"Stars with [M/H]<−2 show no net rotation"（[M/H] < −2 的星没有净转动），"those with [M/H]∼−1 are rotation dominated"（[M/H] ∼ −1 的星以转动为主）；第 III.3 节更谨慎（"starting already at [M/H]<−2 there is some, albeit small, net" rotation，即从 [M/H] < −2 开始就已有一些虽小的净转动），给出 [M/H] = −1.3 时 J_φ/J_tot ≈ 0.3，并在 −0.7 附近趋平；总结给出 [M/H] = −1.5 时 0.25、−0.8 时 ≈0.9。

**第 6 步 · 化学**（第 III.4 节、图 7）。对 APOGEE DR17 中的子样本，[α/Fe]、[Al/Fe] 与 [Mg/Mn]（α 元素由大质量恒星快速产生，相对于铁的丰度；以及用来区分银河系内诞生与吸积来的恒星的比值）表明：大多数低偏心率、[M/H] < −1 的星是 α 增丰（α-enhanced）的，即形成于快速增丰的气体；而在高偏心率处出现一条大远心距的低 α 序列（类似 GSE）。R22 指出这一判据"more ambiguous at low metallicity"（在低金属丰度时更含糊）。

**第 7 步 · 从金属丰度到年龄**（第 IV 节）。R22 没有测这些巨星的年龄；年龄估计"beyond the scope of this work"（超出本文范围；第 II 节）。年龄论证是化学的：最老的 α 增丰盘星在 [M/H] ∼ −1 处，"appear to be ≈12.5 Gyrs old"（看来约 12.5 Gyr）（参考文献 [96]，Xiang & Rix 2022；见本项目的[研究 010 文章](https://github.com/sudoghut/astrolab/blob/main/docs/wiki/Study-010-thick-disc-early-formation.md)）。比最老的盘更贫金属、"chemically, and therefore temporally, predates the oldest α-enhanced disk"（在化学上、因而在时间上早于最老的 α 增丰盘）的星，就必定形成于 τ ≳ 12.5 Gyr，"corresponding to z≳5"（对应 z ≳ 5）。这假设整个原银河系中金属丰度随时间单调上升。

*粗略验算。* 在 Planck 2018 宇宙学（宇宙年龄 13.79 Gyr）中，回溯时间（lookback time）12.5 Gyr 对应红移 z ≈ 4.6（大爆炸后 13 亿年）；"z≳5"略微向上取整（z = 5 对应回溯 12.62 Gyr）（我们用 astropy 的 Planck18 计算；R22 没有给出换算）。

#### 1.4 结论与把握程度

摘要：Gaia XP 数据在内银河系揭示了"an extensive, ancient, and metal-poor population"（一个延展、古老、贫金属的族群）：∼18,000 颗 −2.7 < [M/H] < −1.5 的星，代表 ≳5×10⁷ M☉ 的恒星，空间高斯尺度 σ ≈ 2.7 kpc；最贫金属的（[M/H] < −2）没有净转动，[M/H] ∼ −1 的以转动为主；"These central, metal-poor stars most likely predate the oldest part of the disk (τ_age≈12.5 Gyrs), which implies that they formed at z≳5"（这些中心的贫金属星很可能早于盘最老的部分（τ_age ≈ 12.5 Gyr），这意味着它们形成于 z ≳ 5）。总结（第 IV 节）称之为"the most ancient proto-Galactic component of our Galaxy"（我们银河系最古老的原银河系成分）；第 III.4 节把它与 Belokurov 和 Kravtsov 的"曙光"等同。总结论证：局限在太阳圆以内（R_GC < R☉）"against an origin through accretion from a once-distant satellite"（不支持来自一个曾经遥远的卫星星系的吸积起源）：如此低 [M/H] 下如此多强 α 增丰的恒星质量"are most likely to occur at the center of a (eventually) quite massive halo"（最可能出现在一个（最终）相当大质量的晕的中心），而不是低质量卫星星系中。由于所提出的 Heracles/Kraken/Koala 并合碎片与原银河系"曙光"的化学"virtually indistinguishable in all chemical spaces"（在所有化学空间中几乎无法区分），R22（第 III.4 节）认为他们的图景"appears to obviate the need for an ex-situ merger"（似乎无需这样一次异位并合），并补充："This does not necessarily imply that these mergers did not occur"（这并不一定意味着这些并合没有发生。）他们不声称发现了新成分："The results presented here are by no means a new distinct stellar component"（这里给出的结果绝不是一个新的独立恒星成分）。

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
- **表 1 与正文**：所采用配置的一行（0.049 dex、0.107 dex）在表 1 中是最好的，但附录 A.1 说"this final configuration has slightly worse performance than the best configuration"（这一最终配置的表现比最好的配置略差），且其 RMS 误差提示"a few more outliers"（多一些离群值）。
- **质量**在摘要中为 ≳5×10⁷ M☉，在总结中为 ≳10⁸ M☉；每颗巨星的换算（800 M☉）无法由所引的 M4 数字复现（在一半质量位于半质量半径以外的假设下，这是一个尚未解决的不符，不是换算有误的证据）。
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

#### 2.0 论证地图

编码的结论有四部分，摘要与总结（第 IV 节）都写到了：（1）内银河系中的贫金属星（[M/H] < −1.5）合计至少约 5×10⁷ M☉；（2）它们向中心集中，大多数在离银心 5 kpc 以内；（3）它们形成于最老的盘之前，至少 12.5 Gyr 以前（z ≳ 5）；（4）它们是银河系最古老的原银河系（原位，in situ）成分。整体引用摘要："This sample reveals an extensive, ancient, and metal-poor population"（这个样本揭示了一个延展、古老、贫金属的族群）；第（3）部分在摘要中有保留措辞（"most likely predate the oldest part of the disk"，很可能早于盘最老的部分），第（4）部分在第 IV 节中有保留措辞（"All of this information fits a picture in which this metal-poor heart of the Milky Way constitutes the most ancient proto-Galactic component of our Galaxy"，所有这些信息符合这样一幅图景：银河系这个贫金属的核心构成我们银河系最古老的原银河系成分）。

A. XP 金属丰度精确到约 0.1 dex；[缺口] 贫金属尾巴没有被 [M/H] 被低估的较富金属星主导；精确而纯净的选择是真实的（标准知识）⇒ 计数的贫金属星是真实的。
B. 约 18,000 颗这样的星；球状星团 M4 给出每 800 M☉ 一颗巨星；[缺口] 这一换算适用于本样本 ⇒ 照此计算约 2×10⁷ M☉；拥挤与尘埃使样本不完整，乘以"保守的"2.5 倍 ⇒ **至少约 5×10⁷ M☉**。
C. 用球对称高斯拟合视差得到 σ_RGC ≈ 2.7 kpc；[缺口] 拟合没有被它未建模的选择（尘埃、拥挤、视场边界、星等截断）扭曲 ⇒ **大多数星在离银心 5 kpc 以内**。
D. 供环节 F 使用的数据：[M/H] = −2 以下没有净转动，−1 附近以转动为主；大多数远心距小于 5 kpc；绝大多数 α 增丰。
E. 老盘的金属丰度分布在 [M/H] = −1 以下急剧下降；[缺口] 贫金属星与老盘属于同一个化学上相连的系统；在这样一个系统中金属丰度随时间上升（标准知识）⇒ 贫金属星早于最老的盘；最老的盘星约 12.5 Gyr ⇒ **形成于 ≳12.5 Gyr 以前，z ≳ 5**。
F. 局限在中心不支持来自曾经遥远的卫星星系；α 增丰支持在深引力势阱中快速增丰；[缺口] 再加上质量、年龄与转动趋势，这使该族群成为**原银河系的原位核心**，而不是被吸积星系的碎片。

检查方式：论证用 Lean 4 写成（[`studies/012-m12-poor-old-heart/argument/Argument.lean`](https://github.com/sudoghut/astrolab/blob/main/studies/012-m12-poor-old-heart/argument/Argument.lean)）。每个前提是 `Field` 的一个构造子（不用公理），标注类型与出处性质：

| 标签 | 前提类型 |
|---|---|
| `OBS` | 观测或测量（附表格/图） |
| `MOD` | 模型假设，或论文写出的推理规则 |
| `STAT` | 统计推断（拟合、验证、从数据读出的趋势） |
| `NUM` | 由本仓库 `run.py` 复算的数值结果（暂无：研究还没有结果） |
| `LIT` | 取自其他文献的结果 |
| `GAP` | 推理需要、但论文与标准知识都没有提供的前提（缺口） |

出处性质：`[stated: "引文"]`（论文写明，引自 arXiv HTML v1）、`[implied]`（论文依赖但没写出的标准知识，注明来源）、`[reconstructed]`（我们补上的；恰好是 `GAP` 前提；R22 之后发表的文献归入此类，因为 R22 不可能依赖它）。

Lean 检查什么：结论能否由这些前提推出（`final`）且不是恒真（`final_nontrivial`）；前提能否同时成立（`consistent`）；没有单个前提能单独给出结论（`alone_insufficient`）；每个前提是必要的（去掉它后的反例模型）还是多余的；论文实际写出的前提是否足够（`stated_*`），加上标准知识后是否足够（`explicit_*`；`explicit_insufficient` 意味着真正的缺口）。Lean 不检查什么：每个前提内部的物理与统计，这由第一、三部分与研究本身负责。

编码约定。写明的推理规则（"this implies"、"leading us to a lower limit"、"the parallax distribution implies"、"it must have formed"）编码为蕴含式；我们的分析认为这一步还需要更多条件时，把缺少的条件作为额外的前件，这使蕴含式比引文更弱，这些条件另作为 `GAP` 前提出现。带保留措辞的推理从不编码为写明的蕴含式："most likely predate" 变为一个缺口（`gap_onezone`）加一条标准规则（`mod_amr`）；"most likely ... not at a low-mass satellite" 与 "fits a picture" 变为缺口 `gap_proto`。"arguing against" 与 "arguing for" 用本身就表示"不被支持"与"被支持"的原子编码。引文不能含方括号（测试的格式要求），所以含 "[M/H]" 的短语在括号前或后截断，截掉的内容写在出处一栏。R22 的数字以原子（`OBS`/`STAT`）而不是数值进入：研究还没有结果，所以没有 `NUM` 前提。

#### 2.1 环节 A · 贫金属尾巴是真实的

*概述。* 后面的一切都是对按 XP 金属丰度选出的星做计数、作图与轨道分析。如果估计精确、而且尾巴没有被实际上更富金属的星填满，这种选择就是真实的。R22 证实了前者（验证，附录 A），把后者作为开放问题提出。

**前提。**

| 前提（Lean 构造子） | 标签 | 出处性质 | 论文出处 |
|---|---|---|---|
| `stat_prec`：XP [M/H] 与 APOGEE 及其他巡天符合到约 0.1 dex | STAT | stated: "a remarkably precise (≲0.1 in the median)" | 第 II.3 节（APOGEE 星在训练集中）；附录 A.2 |
| `gap_pure`：−1.5 以下的尾巴没有被 [M/H] 被低估的较富金属星主导 | GAP | reconstructed | R22 问"How pure are the XP selected samples in this regime?"（第 IV 节）；Chen 等 2025，arXiv:2511.18901 |
| `mod_tail`：精确 + 纯净 ⇒ 贫金属星是真实的 | MOD | implied：标准的选择逻辑（Ivezić 等 2014，*Statistics, Data Mining, and Machine Learning in Astronomy*） | — |

**竞争解释。**

| 替代解释 | 由哪个前提排除 | 论文是否明确排除？ |
|---|---|---|
| 尾巴中部分是被回归模型散射到低值的较富金属星（尘埃、拥挤、低信噪比） | `gap_pure` | 否：只提出了问题，没有回答；−2 以下的验证很薄弱（GSP-Spec 达不到那里；APOGEE 检验用的是训练星） |
| −2.5 附近的下限是训练范围造成的假象 | （影响尾巴形状，未编码） | 否：R22 说需要后续工作（"the APOGEE training set for XGBoost only extended to [M/H]=−2.5"） |
| SkyMapper 式的系统误差（−1.5 附近偏差 0.28 dex、弥散 1 dex） | `stat_prec` | 是，通过比较，归因于 SkyMapper |

**推理（Lean 摘录）。**

```lean
have t : v.TailReal := p .mod_tail (p .stat_prec) (p .gap_pure)                     -- GAP
```

**评析。** 主体的中位精度 0.1 dex 对占 1% 的尾巴说明不了多少。样本中每颗 [M/H] < −1.5 的星对应约 100 颗更富金属的星；−1.3 到 −1 之间的星只要有 1% 被估错，就已经是尾巴中相当大的一部分。XGBoost 这样的树回归模型不能给出低于训练标签的值，而一般的回归估计会把极端值拉向主体；两种效应以相反的方向塑造尾巴（−2.5 以下的星变少，−1.3 附近的一些星可能出现在 −1.5 以下）。Chen 等 2025 发现十个 XP 金属丰度星表对 [Fe/H] = −2 以下尾巴的斜率看法不一（k ≈ 0.6–2.0）。所以纯度是第一个缺口，结论的每一部分都依赖它。

#### 2.2 环节 B · 多少颗星、多少质量

*概述。* −1.5 以下计数约 18,000 颗（第 III.2 节；图 4 与第 IV 节约 20,000）。一个模板把高光度巨星换算成恒星总质量：在 M4 中，每 800 M☉ 有一颗 M_G < 0.5 的巨星。照此计算约 2×10⁷ M☉；样本在拥挤天区与尘埃后面不完整，"保守的"2.5 倍给出下限 ≳5×10⁷ M☉。

**前提。**

| 前提（Lean 构造子） | 标签 | 出处性质 | 论文出处 |
|---|---|---|---|
| `obs_count`：约 18,000 颗 [M/H] < −1.5 的星 | OBS | stated: "that includes ∼18,000 stars" | 摘要（第 III.2 节；图 4 与第 IV 节：∼20,000） |
| `mod_m4`：M4 中每 800 M☉ 一颗巨星（M_G < 0.5） | MOD | stated: "per 800 M⊙ of total stellar population mass" | 第 III.2 节 |
| `gap_template`：M4 的换算适用于本样本 | GAP | reconstructed | 样本截断在经颜色改正的 M_G ≈ 0.9，不是 0.5；800 M☉ 不能由所引的 M4 数字复现 |
| `mod_face`：真实的尾巴 + 计数 + M4 比值（+ 模板）⇒ 照此计算约 2×10⁷ M☉ | MOD | stated: "At face value, this implies" | 第 III.2 节 |
| `obs_incomplete`：拥挤天区缺少 XP 光谱，尘埃遮住恒星 | OBS | stated: "But this does not account for the incompleteness of XP spectra in very crowded fields" | 第 III.2 节 |
| `mod_corr`：照此计算的质量 + 不完整 ⇒ ≳5×10⁷ M☉ | MOD | stated: "A conservative estimate of these effects is a factor of 2.5, leading us to a lower limit on the mass of" | 第 III.2 节 |

**竞争解释。**

| 替代解释 | 由哪个前提排除 | 论文是否明确排除？ |
|---|---|---|
| 计数被污染抬高（环节 A） | `mod_face` 需要 `TailReal` | 否 |
| 光度范围或族群（年龄、质量函数）与 M4 不同 | `gap_template` | 否 |
| 不完整改正因子小于 2.5 | `mod_corr` | 称为"保守"，没有推导 |

**推理（Lean 摘录）。**

```lean
have fm : v.FaceMass := p .mod_face t (p .obs_count) (p .mod_m4) (p .gap_template)  -- GAP
have m : v.Massive := p .mod_corr fm (p .obs_incomplete)
```

**评析。** 三个数字相乘，每个都有软肋。计数在各节之间不同（18,000 或 20,000）。每颗巨星 800 M☉ 的换算不能由所引的 M4 数字推出（半质量半径以外 35 颗巨星、总质量 7×10⁴ M☉；半径以外一半质量给出每颗约 1,000 M☉，全部质量约 2,000），而样本包括比模板 M_G = 0.5 更暗的巨星，这应当降低每颗计数巨星对应的质量；两者部分抵消，论文没有讨论。2.5 倍被称为保守，没有推导，总结走得更远（M* ≳ 10⁸ M☉）。只有在计数没有被污染抬高时，下限才是下限：污染与不完整方向相反，只改正了其中之一。10⁷–10⁸ M☉ 的量级对这一切都稳健；两者之间的倍数则不然。

#### 2.3 环节 C · 向中心集中

*概述。* 这些星的视差精度约为 5，R22 不画单颗星的距离图，而是用最大似然对视差拟合一个按银心距的球对称高斯分布（式 1），得到 σ_RGC ≈ 2.7 kpc；总结把这转述为"most stars are within 5 kpc of the Galactic center"（大多数星在离银心 5 kpc 以内）。

**前提。**

| 前提（Lean 构造子） | 标签 | 出处性质 | 论文出处 |
|---|---|---|---|
| `mod_sph`：三维分布是按 R_GC 的球对称高斯 | MOD | stated: "We assume that the 3D distribution is a spherical Gaussian as a function of Galactocentric radius" | 第 III.1 节，式 1 |
| `stat_sigma`：最大似然拟合给出 σ_RGC ≈ 2.7 kpc | STAT | stated: "We find that the maximum likelihood of the observed parallaxes (and their uncertainties) for the" | 第 III.1 节（后接 "[M/H]<−1.5 stars implies an extent of σ_RGC∼2.7 kpc"；无不确定度） |
| `gap_sel`：拟合没有被它未建模的选择扭曲 | GAP | reconstructed | R22 第 IV 节（需要"modeled quantitatively"）；Kurbatov 等 2024，arXiv:2410.22250 |
| `mod_central`：真实的尾巴 + 模型 + 拟合（+ 选择）⇒ 大多数星在 5 kpc 以内 | MOD | stated: "the parallax distribution implies that most stars are within 5 kpc of the Galactic center" | 第 IV 节（图 3） |

**竞争解释。**

| 替代解释 | 由哪个前提排除 | 论文是否明确排除？ |
|---|---|---|
| 尺度由视场决定（60° × 60° 方框，边缘在 4.7–4.9 kpc） | `mod_sph`（式 1 对观测方向积分） | 是，在模型中 |
| 尘埃去掉了离盘面 700 pc 以内与中心 1 kpc 的星；拥挤；BP < 15.5 与光度截断按距离选择 | `gap_sel` | 否：列为后续工作 |
| 族群是扁的或服从幂律，不是球形 | `gap_sel`、`mod_sph` | 否；Kurbatov 等 2024 得到扁率 ≈0.5、"曙光"斜率 −4.5 |
| 视差零点误差使 σ 有偏 | `stat_sigma`（0.02 mas 改正） | 部分 |

**推理（Lean 摘录）。**

```lean
have c : v.Central := p .mod_central t (p .mod_sph) (p .stat_sigma) (p .gap_sel)    -- GAP
```

**评析。** 定性意义上的"向中心集中"是稳健的：视差把大多数星放在银心附近，轨道（环节 D）也把它们局限在那里。数字 σ ≈ 2.7 kpc 则脆弱：没有不确定度；依赖一个后来带选择函数的工作并不偏好的形状（球形、高斯）；最重要的选择（盘面附近的尘埃、拥挤、随距离变化的星等极限）不在似然中。去掉盘面附近与中心的星、保留高银纬远处星的选择，可能使 σ 向任一方向变化。5 kpc 的说法由 σ ≈ 2.7 kpc 推出（三维高斯把 67% 放在 5 kpc 以内，第一部分 1.3），所以继承这一缺口。

#### 2.4 环节 D · 运动学与化学（环节 F 的数据）

*概述。* 对约 125 万颗有 RVS 速度且视差良好的星，R22 计算了轨道。贫金属星处在留在约 5 kpc 以内的热轨道上；转动量 J_φ/J_tot 随金属丰度上升，从 −2 以下没有净转动到 −1 附近以转动为主。在 APOGEE 子样本中，−1.5 以下的星绝大多数 α 增丰。

**前提。**

| 前提（Lean 构造子） | 标签 | 出处性质 | 论文出处 |
|---|---|---|---|
| `stat_norot`：[M/H] < −2 没有净转动 | STAT | stated: "show no net rotation, whereas those with" | 摘要（第 III.3 节："some, albeit small, net" rotation，−2 以下已有一些虽小的净转动） |
| `stat_spin`：[M/H] ≈ −1 附近以转动为主 | STAT | stated: "are rotation dominated" | 摘要（J_φ/J_tot 在 −1.3 时 ≈ 0.3，III.3；−1.5 时 0.25、−0.8 时 ≈0.9，IV） |
| `stat_apo`：大多数远心距小于 5 kpc | STAT | stated: "most stars have apocenters of less than 5 kpc" | 第 IV 节（⟨R_apo⟩ ≈ 4 kpc，III.3） |
| `stat_alpha`：−1.5 以下的星绝大多数 α 增丰 | STAT | stated: "are distinctly α-enhanced, arguing for rapid enrichment in a deep potential well" | 第 IV 节（APOGEE DR17 子样本；推理部分是 `mod_deepwell`） |

**竞争解释。**

| 替代解释 | 由哪个前提排除 | 论文是否明确排除？ |
|---|---|---|
| 极贫金属的内区星确实在转动（约 40 km/s） | `stat_norot` | 否；R22 自己的第 III.3 节说"some, albeit small"；Ardern-Arentsen 等 2024 |
| RVS 子样本（更亮、更近）不能代表贫金属族群 | （未编码） | 否 |
| 远心距被距离误差影响 | `stat_apo` | 提到了（偏高，第 III.3 节），这使"< 5 kpc"偏保守 |
| 正经过近心点的 GSE 星污染内区样本 | （未编码；进入 `gap_proto`） | 部分：认出了 e ≥ 0.75、R_apo ≳ 10 kpc 的星，未定量 |

**评析。** 这四条是数据，不是推理，按数据编码。两点说明。"没有净转动"（摘要）比论文正文更强（III.3：−2 以下已有小的转动）；后来的光谱巡天发现极贫金属内区星的转动恒为约 40 km/s。对原银河系论证而言，缓慢而非零的转动影响不大；对在某一金属丰度处急剧"转快"的说法则有影响（Viswanathan 等 2025 发现从 −1.7 到 −1.0 逐渐转快）。

#### 2.5 环节 E · 比盘更老

*概述。* R22 没有测年龄，年龄论证是化学的。老的 α 增丰盘的金属丰度分布在 [M/H] = −1 以下急剧下降，其最老的成员（−1 附近）约 12.5 Gyr（Xiang & Rix 2022）。如果贫金属核心"chemically, and therefore temporally, predates"（在化学上、因而在时间上早于）这个盘，"it must have formed at τ≳12.5 Gyrs, corresponding to z≳5"（它必定形成于 τ ≳ 12.5 Gyr，对应 z ≳ 5）。从金属丰度更低到形成更早这一步，在摘要中有保留措辞（"most likely predate"）。

**前提。**

| 前提（Lean 构造子） | 标签 | 出处性质 | 论文出处 |
|---|---|---|---|
| `obs_discfloor`：老盘的金属丰度分布在 −1 以下急剧下降 | OBS | stated: "However, the old α-enhanced disk metallicity distribution function (MDF) is truncated, or at least drops sharply, below" | 第 I 节 |
| `gap_onezone`：贫金属星与老盘属于同一个化学上相连的系统 | GAP | reconstructed | R22 有保留（"most likely predate"）；R22 第 I 节预期混有较晚并合的卫星星系；Ardern-Arentsen 等 2024，arXiv:2312.03847 |
| `mod_amr`：在一个系统中金属丰度随时间上升 ⇒ 比最老的盘更贫金属意味着更早 | MOD | implied：单区化学演化（one-zone chemical evolution；Tinsley 1980，1980FCPh....5..287T） | — |
| `lit_discage`：最老的盘星约 12.5 Gyr | LIT | stated: "appear to be ≈12.5 Gyrs old" | 第 IV 节；参考文献 [96]，Xiang & Rix 2022，arXiv:2203.12110 |
| `mod_ancient`：早于盘 + 盘的年龄 ⇒ 形成于 ≳12.5 Gyr 以前，z ≳ 5 | MOD | stated: "it must have formed at τ≳12.5 Gyrs, corresponding to z≳5" | 第 IV 节（条件句："If much of this metal-poor heart ..."） |

**竞争解释。**

| 替代解释 | 由哪个前提排除 | 论文是否明确排除？ |
|---|---|---|
| 一些贫金属星较晚形成于增丰缓慢的系统（盘开始形成之后才被吸积的矮星系） | `gap_onezone` | 否；R22 自己的引言预期这种混合 |
| 原银河系内部增丰不均匀（低金属丰度气体团块较晚形成恒星） | `gap_onezone` | 否 |
| 最老的盘的绝对年龄更小（不同的等年龄线标尺） | `lit_discage` | 否；Chen, Sun & Ye 2025 发现亚巨星年龄年轻约 13%（见研究 010 的文章） |
| 由 12.5 Gyr 得到"z ≳ 5" | `mod_ancient` | 写明；在 Planck 2018 中回溯 12.5 Gyr 为 z ≈ 4.6（第一部分 1.3） |

**推理（Lean 摘录）。**

```lean
have pd : v.Predates := p .mod_amr (p .gap_onezone) t (p .obs_discfloor)           -- GAP
have a : v.Ancient := p .mod_ancient pd (p .lit_discage)
```

**评析。** "早于最老的盘"是推断，不是年龄测量，它需要一个增丰单调的、化学上相连的系统。对单个混合均匀的气体库这是标准的，但早期银河系并不是一个：R22 自己的引言预期最老的贫金属星混有早期原银河系团块与较晚并合的卫星星系，而一个增丰缓慢的矮星系可以在 −1 处最老的盘星形成之后才形成 −1.5 以下的星。论证是统计性的（"much of"，大部分），所以容许一些这样的星，但有多少正是未知的。12.5 Gyr 还带着其来源亚巨星年龄的绝对年龄不确定性，"z ≳ 5"把 z ≈ 4.6 向上取整。

#### 2.6 环节 F · 原银河系的原位核心

*概述。* 第 IV 节的两个论证与运动学趋势导向这一解释。族群局限在太阳圆以内、束缚很紧（"arguing against an origin through accretion from a once-distant satellite"，不支持来自曾经遥远的卫星星系的吸积起源）。其绝大多数星 α 增丰（"arguing for rapid enrichment in a deep potential well"，支持在深引力势阱中快速增丰），而在如此低的金属丰度下有如此多 α 增丰恒星的质量，"most likely"（最可能）出现在"at the center of a (eventually) quite massive halo, not at a low-mass satellite"（一个（最终）相当大质量的晕的中心，而不是低质量卫星星系中）。加上年龄（环节 E）与转动趋势，"All of this information fits a picture"（所有这些信息符合这样一幅图景）：最古老的原银河系成分。

**前提。**

| 前提（Lean 构造子） | 标签 | 出处性质 | 论文出处 |
|---|---|---|---|
| `mod_confined`：向中心集中 + 远心距小 ⇒ 曾经遥远的卫星星系不被支持 | MOD | stated: "arguing against an origin through accretion from a once-distant satellite" | 第 IV 节 |
| `mod_deepwell`：α 增丰 ⇒ 支持在深势阱中快速增丰 | MOD | stated: "are distinctly α-enhanced, arguing for rapid enrichment in a deep potential well" | 第 IV 节 |
| `gap_proto`：质量 + 年龄 + 局限在中心 + 深势阱 + 转动趋势 ⇒ 原银河系的原位核心 | GAP | reconstructed | R22 有保留（"most likely"、"fits a picture"）；Heracles/Kraken/Koala "virtually indistinguishable"（III.4）；Ardern-Arentsen 等 2024 |

**竞争解释。**

| 替代解释 | 由哪个前提排除 | 论文是否明确排除？ |
|---|---|---|
| 曾经遥远的卫星星系的碎片（例如 GSE） | `mod_confined` | 是（论证不支持）；高偏心率的 GSE 星被单独处理 |
| 一个早期大质量被吸积星系沉入中心的碎片（Heracles / Kraken / Koala） | `gap_proto` | 否：化学上"virtually indistinguishable"（几乎无法区分）；R22 的图景"appears to obviate the need"（似乎无需）它，但"This does not necessarily imply that these mergers did not occur"（这并不一定意味着这些并合没有发生） |
| 混合：一个集中、转得较快的原位成分，加一个更延展、更贫金属、转得更慢、来自较小星系的成分 | `gap_proto` | 否；Ardern-Arentsen 等 2024 初步提出 |
| 原位与早期吸积根本无法区分 | `gap_proto` | R22 作为一种可能写明（第 I 节："it may be operationally impossible ..."） |

**推理（Lean 摘录）。**

```lean
have nd : v.NotDistant := p .mod_confined c (p .stat_apo)
have dw : v.DeepWell := p .mod_deepwell (p .stat_alpha)
have pg : v.ProtoGal :=
  p .gap_proto m a nd dw (p .stat_norot) (p .stat_spin)                               -- GAP
exact ⟨m, c, a, pg⟩
```

**评析。** 这一解释是合理性论证，R22 也是这样呈现的（"fits a picture"）。局限在中心排除了从远处落入的卫星星系；它不排除一个很早并合、通过动力学摩擦（dynamical friction）沉入中心的星系，而这正是 Heracles/Kraken/Koala 被提出的样子，R22 也承认化学无法区分两者。部分问题在于定义：如果原银河系由很早并合的"comparable-mass pieces"（质量相当的团块）构成（R22 引言），那么原位核心与早期大质量并合之间的界线取决于质量比与时间。数据确实支持的是：这个族群是老的（在环节 E 的化学意义上）、向中心集中、α 增丰、运动学上热；"原银河系"是对这一组合的解释，依赖 `gap_proto`。

#### 2.7 讨论但未编码的结论

- **内部不一致**（第一部分 1.4）：计数（−1.5 以下 18,000 或 20,000；−2 以下 >4,000 或 ∼5,000；−1 以下近 100,000 或 ∼70,000）、样本量（150 万到 210 万）、质量（≳5×10⁷ 或 ≳10⁸ M☉）、表 1 与正文。它们不改变逻辑，没有编码；第三部分可以用公开文件重新计数。
- **−2.5 附近的 [M/H] 下限**（第 IV 节）及其与训练范围的关系：属于尾巴形状的性质，在环节 A 中讨论。
- **转动趋势的确切形式**（各金属丰度的 J_φ/J_tot 值）：只编码了两端（−2 以下无转动，−1 附近以转动为主）。
- **"Not a new distinct stellar component"**（不是一个新的独立成分）：R22 把这个核心等同于 Belokurov 与 Kravtsov 的"曙光"束缚最紧的核心；这一命名属于 `gap_proto` 的解释。

#### 2.8 Lean 检查发现的问题

1. **核心结论：`explicit_insufficient`，有五个缺口。** 即使加上两条标准规则（`mod_tail`、`mod_amr`），没有以下各条结论仍推不出：贫金属尾巴的纯度（`gap_pure`）、M4 换算的适用性（`gap_template`）、未建模的选择没有造成扭曲（`gap_sel`）、年龄排序所需的同一个化学上相连的系统（`gap_onezone`）以及原位解释（`gap_proto`）。
2. **`stated_insufficient`**：即使不计缺口，R22 写出的内容也不够。论证还用到两条它没有写出的标准规则：精确而纯净的选择给出真实成员（`mod_tail`），以及在一个系统中金属丰度随时间上升（`mod_amr`）。
3. **缺口在哪里。** `gap_pure` 影响全部四部分（质量、集中度与年龄都用到真实的尾巴；解释用到这三者）。第（1）部分质量加上 `gap_template`；第（2）部分集中度加上 `gap_sel`；第（3）部分年龄加上 `gap_onezone`；第（4）部分原银河系加上 `gap_proto` 并继承其他所有缺口。其中两个缺口（`gap_onezone`、`gap_proto`）是 R22 自己有保留的步骤（"most likely"、"fits a picture"）；另外三个是 R22 未加评论就采用的步骤（`gap_template`）或标为后续工作的步骤（`gap_pure`、`gap_sel`）。
4. **排序。** `gap_pure` 最重要（影响一切，论文没有给出任何数字）；其次是 `gap_onezone`（年龄是论文的标题结论）；`gap_proto` 主要是解释性的；`gap_sel` 对 σ ≈ 2.7 kpc 这个数字的影响大于对定性集中度的影响；`gap_template` 影响质量约 2 倍。
5. **在本编码中 25 个前提都是必要的**，没有多余的（每个都在单一链条上）。环节 D 的四条事实只通过解释性步骤（`mod_confined`、`mod_deepwell`、`gap_proto`）才是必要的。
6. **相容性**（`consistent`）在这里分量很弱：没有否定形式的前提，全真模型平凡地满足它们。
7. **编码与引文的差别。** `mod_face`、`mod_central`、`mod_confined` 与 `mod_ancient` 带有额外前件（比引文弱）。`mod_ancient` 把 R22 的一个条件句按条件句编码。含 "[M/H]" 的引文在括号前或后截断，截掉的内容写在各出处栏中。有保留的步骤是缺口，不是写明的蕴含式。
8. **局限。** Lean 检查的是在我们的编码下论证的逻辑结构，不检查每个前提内部的统计；论文的数字（计数、σ、质量、年龄）以原子进入，"必要"的意思是"本编码用到了它"。

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

- 2026-11-21：起草第二部分（六个环节的论证逻辑；`Argument.lean`：25 个前提、5 个缺口、2 条标准知识；`stated_insufficient` 与 `explicit_insufficient`）。
- 2026-11-21：第一部分闸门 2（Codex）：没有严重问题；三处措辞小问题（R22 预期的原银河系星与吸积星的混合、计数验算的斜率假设、800 M☉ 一点作为尚未解决的不符）。
- 2026-11-21：第一部分闸门 1 审查：给出视差/光度查询截断的精确表达式（经颜色改正的 G）；表 1 与正文的矛盾、第 II.4 节的 150 万加入不一致清单；引文与注意事项注明所在章节；加上 R22 的"This does not necessarily imply that these mergers did not occur"；张角与红移验算改为精确值；Zenodo 作者与 DOI；Chen 等的措辞；中文术语括注英文；第二轮：附录 A.1 的精确引文（"slightly worse performance"、"a few more outliers"）、"predates"、消红化标为"我们的解读"、第 IV 节关于训练范围（−2.5）的引文、引文标点。
- 2026-11-21：起草第一部分（科普详解；数字取自 arXiv v1，后续文献据摘要）。计划 `design/028-plan_*`。

### 来源

- Rix 等 2022，ApJ 941, 45，arXiv:2209.02722（被研究的论文；数字与引文据 arXiv HTML v1）。
- Andrae, Rix, Chandra & Price-Whelan 2022，Zenodo，doi:10.5281/zenodo.7035809（公开样本；R22 引作参考文献 [85]"Rix, Chandra & Andrae"；7035809 应是概念 DOI（concept DOI），版本 v0.1 的记录为 doi:10.5281/zenodo.7035810；2026-11-21 阅读页面）。
- Xiang & Rix 2022，Nature 603, 599，arXiv:2203.12110（最老盘的年龄，R22 的参考文献 [96]）。
- Tinsley 1980，Fundamentals of Cosmic Physics 5, 287，1980FCPh....5..287T；Ivezić, Connolly, VanderPlas & Gray 2014，*Statistics, Data Mining, and Machine Learning in Astronomy*（第二部分两条 `[implied]` 前提的标准背景）。
- Chen, Sun & Ye 2025，arXiv:2510.10092（更年轻的亚巨星年龄标尺；经研究 010 的文章）。
- Belokurov & Kravtsov 2022，MNRAS 514, 689，arXiv:2203.04980（曙光；R22 引用，此处未重读；期刊信息凭记忆，未核实）。
- Kurbatov 等 2024，arXiv:2410.22250；Ardern-Arentsen 等 2024，arXiv:2312.03847；Viswanathan 等 2025，A&A 703, A183，arXiv:2411.12165；Chen 等 2025，OJAp，arXiv:2511.18901（后续文献；2026-11-21 阅读摘要）。
