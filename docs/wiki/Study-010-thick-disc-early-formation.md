# When did the Milky Way's disc begin? Ages of a quarter of a million subgiants

[English](#english) · [中文](#中文)

*Paper: Xiang & Rix 2022, "A time-resolved picture of our Milky Way's early formation history", Nature 603, 599, arXiv:2203.12110. Study:
[`studies/010-m05-thick-disc-subgiant-ages`](https://github.com/sudoghut/astrolab/tree/main/studies/010-m05-thick-disc-subgiant-ages) (web page: [online](https://sudoghut.github.io/astrolab/studies/010-m05-thick-disc-subgiant-ages/web/)).
Status: concluded (2026-11-16). Last updated: 2026-11-23 (see the changelog at the end). The source of this page lives in the main repository at
[`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki); edit it there.*

*中文标题：银河系的盘何时开始形成？二十五万颗亚巨星的年龄。状态：已结束（2026-11-16）。论文：Xiang & Rix 2022，Nature 603, 599，arXiv:2203.12110。研究：[`studies/010-m05-thick-disc-subgiant-ages`](https://github.com/sudoghut/astrolab/tree/main/studies/010-m05-thick-disc-subgiant-ages)（网页：[在线版](https://sudoghut.github.io/astrolab/studies/010-m05-thick-disc-subgiant-ages/web/)）。最后更新：2026-11-23（见文末"研究进展"）。本页源文件在主仓库的 [`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki) 中，请在那里修改。*

---

## English

### Part 1 · The paper in plain language

#### 1.1 The question and why it matters

The Milky Way has a thin disc, where the Sun lives and stars still form, and a thicker, older disc
whose stars move further above and below the plane and are richer in "α elements" (oxygen,
magnesium, silicon...) relative to iron. A high [α/Fe] ratio is a chemical clock: α elements come
quickly from massive stars exploding as core-collapse supernovae, while most iron comes later from
type Ia supernovae. Stars with high [α/Fe] therefore formed from gas enriched quickly, early on.

When did this old disc form, how long did it take, and how does it relate to the stellar halo and
to the big merger with a dwarf galaxy, Gaia-Sausage-Enceladus (GSE), that the Gaia satellite
revealed? Answering needs **ages** for many stars, and stellar ages are notoriously hard: for most
stars the age only weakly changes what we can observe.

#### 1.2 The data

Xiang & Rix (XR22) used **subgiants**: stars that have just exhausted hydrogen in their cores and
are crossing from the main sequence to the red-giant branch. In this short phase a star's
luminosity depends steeply on its mass, and hence its age, so luminosity plus temperature and
chemistry give a precise age. They combined:

- spectra from the LAMOST survey (Large Sky Area Multi-Object Fiber Spectroscopic Telescope; data release 7), giving temperature, metallicity [Fe/H], [α/Fe] and
  a spectroscopic absolute magnitude in the near-infrared K band;
- Gaia eDR3 parallaxes and proper motions, giving distances, a geometric absolute magnitude and,
  with LAMOST radial velocities, orbits. The orbits are summarised by **actions**; the azimuthal
  action J_φ is the angular momentum about the Galactic axis (disc stars on near-circular orbits
  near the Sun have J_φ ≈ 1800–2000 kpc km/s; halo stars have J_φ near zero or negative).

After cleaning (binary test, Gaia astrometric quality, variability, LAMOST signal-to-noise above
20, temperature below 6800 K, and cuts removing horizontal-branch stars, which also remove nearly all
stars younger than about 1.5 Gyr), **247,104 subgiants** remain. Ages come from a Bayesian fit to
**Yonsei-Yale (YY) isochrones** (model tracks of stars of one age), averaged over isochrones with
[α/Fe] = 0, 0.2 and 0.4 to match each star's α enhancement. The median age uncertainty is 7.5%; the
analysis keeps stars with relative age errors below 15%. The catalogue is public on VizieR
(J/other/Nat/603.599).

#### 1.3 Step by step: how the authors got from data to conclusion

1. **The age–metallicity plane is messy until it is split.** Plotting all stars by age and [Fe/H]
   gives a complex distribution. XR22 split the sample with quantities that are neither age nor
   [Fe/H] (their eq. 1): stars with J_φ > 1500 kpc km/s **and** low [α/Fe] (below 0.16 for
   [Fe/H] < −0.5, below −0.16[Fe/H] + 0.08 above) are the "late phase" (the thin disc); all others are
   the "early phase".
2. **Two regimes, split at 8 Gyr.** In the late phase almost all stars are younger than about 8 Gyr
   and form a "V shape" in age versus [Fe/H] (explained by radial migration). In the early phase
   almost all are older. The abstract says the plane "splits into two almost disjoint parts,
   separated at 8 Gyr".
3. **The early phase contains two sequences.** A metal-poor sequence (−2.5 < [Fe/H] < −1) is the
   halo; a metal-rich sequence ([Fe/H] ≳ −1) is the old, high-α (thick) disc. Splitting the early
   phase at J_φ = 500 kpc km/s separates them (their Fig. 3).
4. **The old disc began about 13 Gyr ago.** For early-phase stars with J_φ > 500 and
   −1.05 < [Fe/H] < −0.95 ("presumably the oldest thick disk stars"), a Gaussian fit to the age
   histogram gives a mean of 13 Gyr (the figure inset prints 13.03 Gyr, width 1.81 Gyr; Extended Data Fig. 1). With a
   13.8 Gyr old universe, this is "only 0.8 Gyr after the Big Bang".
5. **Continuous enrichment over 5–6 Gyr with a tight sequence.** Along the old-disc sequence, [Fe/H]
   rises from about −1 at 13 Gyr to +0.5 at about 7 Gyr. A model in which age at fixed [Fe/H] is a
   Gaussian around a straight line τ̄0 + a·[Fe/H] (fitted τ̄0 = 9.38 Gyr, a = −3.8 Gyr/dex), broadened
   by each star's age error and an intrinsic scatter σ_int, gives σ_int = 0.82 ± 0.01 Gyr, which XR22
   call an upper limit. With the slope, this means the [Fe/H] spread of stars born at one time is
   below 0.22 dex: the star-forming gas was well mixed.
6. **The GSE merger and a star-formation peak.** Early-phase stars with low angular momentum but
   old-disc chemistry ("splashed" disc stars, heated by the merger) appear only at ages above about
   11 Gyr; the old disc's star-formation rate (after a volume correction) peaks at about 11.2 Gyr. XR22
   conclude that the GSE merger was largely complete about 11 Gyr ago.
7. **The disc is older than the halo at the same metallicity.** At [Fe/H] ≈ −1 the old-disc sequence
   is about 2 Gyr older than the halo sequence ("Z shape").

#### 1.4 What they conclude, and how sure they are

The abstract: the old disc "started 13 Gyr ago, only 0.8 Gyr after the Big Bang"; "Most of these
stars formed 11 Gyr ago, when the Gaia-Sausage-Enceladus satellite merged with our Galaxy"; and over
the next 5–6 Gyr the Galaxy enriched continuously, by a factor of 10 in metallicity.

Caveats the paper itself discusses (Methods, Extended Data):

- **The absolute age scale.** MIST (MESA Isochrones and Stellar Tracks) isochrones give ages about 0.5 Gyr older than YY at solar α;
  ignoring α enhancement would overestimate old-star ages by up to 2 Gyr (XR22 do include it). No
  prior forces ages below 13.8 Gyr; XR22 note that ages "are consistent with the age of the universe
  at the old end".
- **Selection.** Older subgiants are fainter, so they are seen to smaller distances. XR22 check with
  a Gaia mock catalogue and a volume correction and find the selection has "negligible impact".

Other work frames the result (checked against the arXiv abstracts and full texts, 2026-11-15):

- **A nearly coeval thick disc.** Asteroseismic ages of nearly 400 α-rich red giants in the Kepler
  field (Miglio et al. 2021, arXiv:2004.14806; high α means [α/Fe] > 0.1) give a mean age of about
  11 Gyr and, after deconvolving the age errors with a hierarchical model, "95% of the population was
  born within ∼1.5 Gyr". This is in tension with 5–6 Gyr of continuous old-disc enrichment, although
  tracers (red giants with asteroseismic masses versus subgiants with isochrone ages), fields and
  definitions of "high α" differ.
- **Younger absolute ages elsewhere.** Asteroseismology of 95 red giants (Montalbán et al. 2021,
  arXiv:2006.01783) puts the start of the high-α disc "roughly ∼10 to 11.5 Gyr ago"; StarHorse ages
  (Queiroz et al. 2023, arXiv:2303.09926) give the genuine thick disc mean ages of 10.4–11.8 Gyr
  depending on the survey; the Gaia nearby-star colour–magnitude diagram (Gallart et al. 2024,
  arXiv:2402.09399, a thin-disc paper) attributes part of its age-scale difference with XR22 to the
  isochrone set.
- **The subgiant age scale itself.** A re-analysis with LAMOST DR9 parameters and different
  α-enhanced models finds ages "systematically younger than those of [Xiang & Rix 2022] by ∼12.9%"
  for 2,866 stars in common (Chen, Sun & Ye 2025, arXiv:2510.10092); at 13 Gyr that is about 1.7 Gyr.
  Wide binaries confirm XR22's *relative* age errors (12 pairs; after removing one outlier the
  scatter matches the quoted errors) but cannot test a global offset (Shariat, El-Badry &
  Bhattacharjee 2025, arXiv:2510.08675).
- **Later uses of the onset.** Feltzing, Feuillet & Bensby 2026 (arXiv:2605.20959; 319,835 LAMOST
  subgiants) find the disc spin-up at −1.25 < [Fe/H] < −0.9 with mean age 12.1 ± 2.8 Gyr; Lu et al.
  2026 (arXiv:2607.02940) argue that age errors bias the Splash older (an Eddington-like bias) and date
  the GSE merger to 10.1 ± 0.2 Gyr ago.

### Part 2 · The logic of the argument

#### 2.0 Map of the argument

We encode one claim in Lean: **the old disc started forming about 13 Gyr ago, about 0.8 Gyr after the
Big Bang.** It is the headline of the paper and of the atlas entry, and unlike the 8 Gyr split or the
σ_int bound it is an inference from survivors' ages to an event, which is where hidden steps hide.

```
 YY α-enhanced isochrone ages (mod_ages) ─┐
 bin = oldest thick-disc stars (gap_bin) ─┤
 Gaussian mean = 13 Gyr (stat_mean) ──────┤
 ages consistent with universe age ───────┼─[gap_scale]→ absolute scale accurate
   (obs_scale)                            │
 universe 13.8 Gyr (lit_universe) ────────┤
                                          └─[gap_onset]→ disc began ~13 Gyr ago, 0.8 Gyr after Big Bang
```

#### 2.1 Stage A · Ages and their absolute scale

*Summary.* The ages are model ages: a star's luminosity, temperature and composition are matched to
YY isochrones. Precision (7.5%) is not accuracy: a different isochrone set shifts every old age by a
similar amount. XR22's check of the scale is that the oldest ages are consistent with the age of the
universe.

*Premises (Lean `Field`).*
- `mod_ages` (MOD, stated, Extended Data Fig. 4): ages from YY isochrones weighted over
  [α/Fe] = 0, 0.2 and 0.4.
- `obs_scale` (OBS, stated, Methods): at the old end the ages are consistent with the age of the
  universe.
- `gap_scale` (GAP, reconstructed): this consistency establishes the absolute scale at 13 Gyr to
  better than about 0.5 Gyr, well below the 0.8 Gyr margin to the Big Bang.

*What Lean shows.* The paper states a qualitative version: the ages "seem to be reasonable as they
are consistent with the age of the universe at the old end" (XR22 impose no age prior precisely so
that stellar ages give an independent check on the age of the universe). What neither the paper nor
standard knowledge gives is the quantitative accuracy the onset needs, well below the 0.8 Gyr margin
(we take about 0.5 Gyr). Consistency with 13.8 Gyr only excludes scales far too old; a scale off by a few
tenths of a Gyr in either direction is equally consistent, and XR22's own comparison with MIST gives
0.5 Gyr; a later re-analysis finds ages 12.9% younger (about 1.7 Gyr at 13 Gyr; Chen, Sun & Ye 2025). An onset "0.8 Gyr after the Big Bang" is a difference of two numbers, 13.8 − 13.0, and is
as uncertain as the age scale.

#### 2.2 Stage B · From a mean age to an onset

*Summary.* The 13 Gyr is the mean of a Gaussian fitted to stars in one narrow metallicity bin
(−1.05 to −0.95) of the early phase with J_φ > 500. The fitted width is 1.81 Gyr, wider than the
typical age error at this age (about 1 Gyr), so the bin spans several Gyr of real ages, or contains
stars with larger errors, or both. The main text supports the onset qualitatively with Fig. 2 (the
panel-e sequence reaches [Fe/H] ≲ −1 at about 13 Gyr); Extended Data Fig. 1 is the quantitative route,
and it is the one encoded.

*Premises.*
- `gap_bin` (GAP, reconstructed): the bin holds the oldest thick-disc stars. XR22 write only
  "presumably the oldest thick disk stars"; asserting it is our step (changed 2026-11-16 after the
  referee: the earlier MOD/stated encoding was stronger than its quote).
- `stat_mean` (STAT, stated): the Gaussian mean is 13 Gyr (encoded as 130 tenths of a Gyr).
- `lit_universe` (LIT, stated, Methods: "CMB measurements of Planck (13.8 Gyr)"; XR22's ref. 19 is
  Planck 2015, arXiv:1502.01589): the universe is 13.8 Gyr old.
- `gap_onset` (GAP, reconstructed): the mean age of surviving local stars in this bin dates the start
  of disc formation.

*What Lean shows.* `gap_onset` carries four unstated steps:

1. **A mean is not a start.** If the disc started 13 Gyr ago, about half the bin is younger, so the
   mean dates the bin's typical star; read as an onset it is later than the first stars, which is
   conservative for "early". The other way round, a fitted width of 1.81 Gyr around 13.03 Gyr with
   errors of about 1 Gyr implies some true ages above 13.8 Gyr, which points back to the age scale
   (`gap_scale`).
2. **Survivors and migration.** Stars seen today within a few kpc of the Sun are survivors, some of
   which migrated outward or inward, so their ages describe where stars now are, not where the disc
   first formed.
3. **The J_φ cut does not cleanly separate components** (our reasoning): halo stars on prograde
   orbits can pass J_φ > 500 and are about 2 Gyr *younger* at this metallicity, pulling the mean
   down; old "splashed" disc stars, which XR22's Extended Data Fig. 2 shows as a low-J_φ tail at
   −1 ≲ [Fe/H] ≲ −0.4, are removed by the cut, which also pulls the mean down; the size of either effect is unknown.
4. **The observed-age mean can be biased.** The 15% relative-error cut, the faintness of old
   subgiants (a volume effect) and asymmetric errors near the 20 Gyr grid edge (with no age prior) can
   shift a mean of observed ages; age errors produce an Eddington-like bias (scatter of a truncated or steep distribution shifts its observed mean) toward older ages in a
   truncated distribution (Lu et al. 2026, arXiv:2607.02940). Our R2 tests the error-cut part.

#### 2.3 The other claims (discussed, not encoded)

- **The 8 Gyr split.** The split uses [α/Fe], which correlates with age; so "few old stars in the
  late phase and few young stars in the early phase" partly follows from the chemical cut. The
  claim that the *age–metallicity plane itself* has two almost disjoint parts needs a test of the
  density, without the split. That is our R1.
- **The 0.82 Gyr intrinsic scatter.** XR22's model adds only the age error in quadrature. Ages and
  [Fe/H] errors are correlated (the age fit uses [Fe/H]), and the sample definition of "the old
  high-α sequence" (in panel e of their Fig. 2) shapes the result: a cut on [α/Fe], which correlates
  with age at fixed [Fe/H], trims the young side and lowers σ_int. These are our R3/R4.
- **11 Gyr and the GSE.** The 11.2 Gyr peak needs the volume correction for selection, which the
  public catalogue does not carry; we can describe, not test, it.

#### 2.4 What the Lean check found

1. **Headline: `explicit_insufficient`, with three gaps.** The onset claim needs the identification of
   the bin as the oldest thick-disc stars (`gap_bin`; XR22 write "presumably"), an accurate absolute
   age scale (`gap_scale`) and the reading of a bin's mean age as the start of disc formation
   (`gap_onset`). No standard knowledge closes any of them.
2. **Ranking.** `gap_onset` matters most: it is a modelling choice the paper does not discuss, and the
   bin's fitted width (1.8 Gyr) is larger than the 0.8 Gyr margin to the Big Bang. `gap_scale` is the
   known isochrone systematic (0.5 Gyr between YY and MIST).
3. **All seven premises are needed** in this encoding; none is redundant.
4. **`stated_insufficient`** holds as well, for the same reason: no premise is merely implied (the
   age of the universe is stated in Methods), so the stated and the explicit premises coincide and
   only the three gaps are missing.
5. **Consistency** (`consistent`) is a weak check here: no premise is negative.
6. **Limits:** Lean checks the logical structure under our encoding, not the stellar physics inside
   each premise. In particular the consequent of `gap_onset` is the conclusion itself: Lean shows that
   the conclusion depends on this unstated bridge, not that the bridge holds.
7. **Deviation from the plan.** Plan 019 foresaw a NUM premise bound to an R2 result; the mean is
   encoded as XR22's stated number (STAT) instead, because the argument is the paper's, and our R2
   result is reported in part 3.

### Part 3 · What astrolab can test or explore

**Interactive page:** [open this study's web page](https://sudoghut.github.io/astrolab/studies/010-m05-thick-disc-subgiant-ages/web/) (results, figures and tables;
English/Chinese switch; updated when the site is republished).

The catalogue (VizieR J/other/Nat/603.599/table1, 247,104 rows) is fetched once through the guarded
`ctx.http` channel from the CfA VizieR mirror (the CDS TAP host is unreachable from this machine),
only the needed columns (Id, Age, e_Age, [Fe/H], e_[Fe/H], [alpha/Fe], e_[alpha/Fe], JPHI, MKcomb):
65 bytes per row measured on a 5-row trial, about 16 MB in total. The design is in
[`design/019-plan_*`](https://github.com/sudoghut/astrolab/blob/main/design/019-plan_m05-thick-disc-early-formation-subgiant-age-metallicity-sequence.md);
the decision rules are frozen in the study README sections 2–4 before any data are fetched in full.
All age fits use one observation model (M0): latent ages on the YY grid [0, 20] Gyr, each star's
measured age Gaussian around the true one with its e_Age, truncated to the grid, and, on the
15%-precision sample S15, a likelihood conditioned on selection.

| Stage / claim | Can we test or explore it? | How | Data (size) | Decision criterion | Result |
|---|---|---|---|---|---|
| Stage B: onset at 13 Gyr (R2) | testable now | Gaussian fit to observed ages in XR22's Extended Data Fig. 1 selection (early phase, J_φ > 500, −1.05 < [Fe/H] < −0.95), and the same without the early-phase filter; also the deconvolved mean (M0), the fraction of ages above 13.8 Gyr and near the 20 Gyr grid edge, and sensitivity to the J_φ cut and the error cut | catalogue (16 MB) | reproduced if the observed-age Gaussian mean is 12.5–13.5 Gyr (a tolerance for the rounded "13 Gyr") | **reproduced**: 12.93 ± 0.06 Gyr (σ 2.40); deconvolved 12.19–12.59 |
| Stage A: absolute scale (`gap_scale`) | explorable (not decisive) | envelope from literature magnitudes: MIST +0.5 Gyr, [α/Fe] error and LAMOST–APOGEE α offset through XR22's age–α sensitivity, LAMOST [Fe/H]/Teff offsets, parallax zero point | – | none - exploration only | envelope 0.7–1.1 Gyr; re-analysis −1.7 Gyr; margin to the Big Bang 0.87 Gyr |
| 8 Gyr split (R1) | testable now | without the chemical split: in five 0.2 dex [Fe/H] bins (−0.7 to +0.3), deconvolved latent age density (Gaussian mixture, K = 1–4 by the Bayesian information criterion, BIC, in M0); valley depth d between 5 and 11 Gyr; threshold d* = min(0.25, 3rd smallest null d) over two log-concave null families (skew-normal and split normal; a parametric stand-in for plan 019's non-parametric log-concave check, a labelled deviation) and two error mechanisms, 50 mocks each; power from XR22-like two-component mocks; young-side 97.5th percentile compared with 8 Gyr | catalogue (16 MB) | a bin is "almost disjoint" if a valley exists and d < d* (at most 2 of 50 null mocks pass); reproduced if ≥ 3 resolvable bins (power ≥ 80%), ≥ 3 almost disjoint, median young-side edge 6.5–9.5 Gyr; robust only if S15 and Full agree | **undetermined** (2 of 5 bins resolvable; none almost disjoint, d = 0.29–0.58) |
| Old-disc sequence: slope, 5–6 Gyr span, σ_int (R3/R4) | testable now | XR22's linear-plus-scatter model in M0 on sample A (S15, above the α line, J_φ > 500, −1.2 < [Fe/H] < 0.5): σ_sel is the scatter of this α-selected sample, a like-for-like reproduction of XR22's number, not the intrinsic-scatter test; recovery mocks under two error mechanisms; intrinsic scatter from sample B (no α cut) with a background component whose mean is linear in [Fe/H], checked with identifiability and misspecification mocks; error-scale factor f = 0.8, 1 and an upper bound from the data | catalogue | R4: \|σ_sel − 0.82\| ≤ 0.1 Gyr; R3: span \|a\| × 1.5 dex in 4.5–6.5 Gyr; robust only if each sensitivity fit passes; intrinsic: σ_int + 1.645 SE < 0.82 Gyr confirms, σ_int − 1.645 SE ≥ 0.82 does not, otherwise (or if a mock-set bias exceeds 0.1 Gyr) "cannot determine" | **cannot determine** (recovery σ bias +0.25–0.28 Gyr; span 6.0, σ_sel 2.67, σ_int 0.79) |
| Tension with Miglio et al. 2021 (R7) | explorable (qualified comparison) | deconvolved total age spread of the high-α disc: central 95% width and the largest fraction in any 1.5 Gyr window, for XR22's sample and an APOGEE-like high-α cut | catalogue | none - comparison across tracers | broad: 95% width 12.6–13.0 Gyr at f = 1 |
| Halo–disc offset at [Fe/H] ≈ −1 (R5) | explorable (plots only) | age–[Fe/H] density split by J_φ | catalogue | none | plots on the study page |
| 11 Gyr / GSE (R6) | describable, not testable | 5th and 10th percentiles of ages of low-J_φ old-disc stars; age peak without volume correction | catalogue | none - the volume correction is not public | observed-age peak 11.1 Gyr (J_φ > 500) |
| `gap_onset` itself (survivors, migration) | out of scope | needs chemical-evolution and migration models | – | – | – |

**What we found (2026-11-16).** On the published table, the 13 Gyr mean of the oldest disc bin is
reproduced on the catalogue's own age scale (12.93 Gyr), but it moves by about 1 Gyr with the isochrone
set and α scale and by 0.3–0.7 Gyr with deconvolution, while the margin to the Big Bang is 0.87 Gyr,
so `gap_scale` is the binding step. The 8 Gyr split could not be decided: in the bins the data can
resolve, the latent age density dips between the phases but not to "almost disjoint" (and a power
floor made one metal-rich bin unresolvable by construction). The old-disc sequence could not be
decided either, because our deconvolution's selection term for the 15% error cut is misspecified
under both mocked error mechanisms (found by the independent referee; post hoc); read informally,
the span (about 6 Gyr) agrees and the scatter of the α-selected sample (2.4–2.7 Gyr) is about three
times XR22's 0.82 Gyr, likely not a like-for-like comparison. A re-test is registered (T-031).
Numbers and page: the study README section 5 and the [web page (online)](https://sudoghut.github.io/astrolab/studies/010-m05-thick-disc-subgiant-ages/web/).

**Re-test with a consistent selection term (T-031, 2026-11-20).** A new pre-registration (README
section 2.5) replaced the selection term with the pass fraction measured on the catalogue as a
function of observed age, and drew the mocks' errors with the data's age dependence. The original
labels above stand as the pre-registered outcome; the re-test labels are the current reading.

- **The old-disc span is reproduced, robustly:** 6.09 Gyr over 1.5 dex (5.9–6.3 in every robustness
  fit).
- **The scatter of the α-selected sample is not reproduced:** 2.55 Gyr against 0.82.
- **The intrinsic scatter of the old sequence is confirmed below 0.82 Gyr:** 0.748 Gyr in a mixture
  with a background component. It is not robust: with errors scaled by 0.8 it can no longer be
  decided.
- **The 8 Gyr split stays undetermined.** The label hinges on one metal-poor bin. That bin's power is
  limited by mock fits that miss the valley (independent referee, post hoc). A diagnostic refit
  (T-045, exploration, post hoc) showed why: the missed mocks are local optima of the mock fits; with
  data-independent starts every mock finds its valley and the bin's power is 1.00 in all six sets
  (recorded 0.58–0.88). So the bin would be resolvable, and because no bin has an almost disjoint
  valley the reading would be "not reproduced", provided the null mocks and the other bins hold up
  under the same refit (not tested); the recorded label stays "undetermined"; the pre-registered
  rerun with better mock fits (T-049) is reported below as R1-SEL-FIT.
- **Variant without a selection term.** It agrees on the intrinsic scatter. It fails the recovery test
  for the sequence under the mocks' error generator, which is why R3/R4 carry "selection-term
  sensitive". Post hoc, the referee's evidence points to that generator as the cause (an
  inference: under the original generator the variant recovers).

**Rerun of the 8 Gyr split with better mock fits (R1-SEL-FIT, T-049, 2026-11-21).** A further
pre-registration (README section 2.6) reran R1-SEL with 8 data-independent starts per mixture size in
every mock fit. The null mocks and power mocks were included, in all bins and variants: 5,400 mocks, 5.3 h. Nothing else
changed, and the original fits reproduce every recorded mock.

- **The null mocks did not move the threshold.** No null mock's valley passes, so d* stays at its
  cap 0.25.
- **The three metal-poor bins have power 1.00 in every variant**, and the bin [−0.1, 0.1) becomes
  resolvable too (power 0.84–1.00).
- **The label is "not reproduced (robust; selection-term robust)"**, the same at the power floor
  0.20, as the pre-registration expected. Every variant has 4 of 5 bins resolvable, but none
  of them has an almost disjoint valley (data d = 0.37–0.58 against 0.25).
- **What this means.** The fits to the data show a dip between an old and a young phase at fixed [Fe/H],
  but not the near-gap the 8 Gyr split describes. This holds under the catalogue's quoted age errors
  (the power mocks use them); larger true errors could blur a near-gap into such a dip, which is not
  tested (independent referee; error-scale test T-054). The power model is the most favourable shape,
  so the label says the data do not show XR22's idealised split.
- **R1-SEL's "undetermined" stands** as that block's pre-registered outcome. R1-SEL-FIT is a rerun
  with improved mock fits, not a correction; R1-SEL's line between the two labels was set by the
  mock optimiser.
- **The metal-richest bin [0.1, 0.3) stays unresolvable** (power 0.30–0.70). Its mixtures still
  smear the generating model's sharp young edge.

**How large would the age errors have to be? (R1-ERR, T-054, 2026-11-22).** A further pre-registration
(README section 2.7) asked whether XR22's idealised split, observed with errors f times the catalogue's
quoted ones and fitted as the data are (with the quoted errors), could produce the data's dips in the
three metal-poor bins. 3,600 power mocks (f = 1.2, 1.5, 2.0, 2.81; both error mechanisms; three
variants), 4.2 h; all reproduction checks passed.

- **The label is "robust up to f = 1.5 (one bin explainable from f = 2.0: [-0.3, -0.1))".** Up to 1.5
  times the quoted errors no mock of any set reaches the data's dip depth (0 of 50 in all 36 sets): the
  blurred split still leaves valleys far deeper than the data's.
- **From about twice the quoted errors** the bin with the smallest gap, [−0.3, −0.1), no longer tells
  the two readings apart (47–50 of 50 mocks reach the data's d). At 2.81 times that bin's split is blurred
  out completely in the selection-term variants (no valley), and the bin [−0.5, −0.3) starts to reach
  in term N and Full; Full reads "sensitive at f = 2.81".
- **What this means (post hoc).** The "not reproduced" of R1-SEL-FIT does not need the quoted errors to be exact:
  XR22's idealised split would need age errors about twice as large as quoted to look like the data. At such
  scales XR22's own 0.82 Gyr width would leave no room for the extra error, and an independent check
  with 11 wide binaries found the quoted errors consistent; whether f ≈ 2 is plausible is outside this
  test. A skewed, prior-shaped error kernel remains untested.
- **A caveat from the independent referee.** The idealised split is younger than the data and its gap
  starts at 7 Gyr, while the data's dips lie at 7.5–9.8 Gyr; a split shaped more like the data could
  fill its dip at a smaller error scale, and refitting the data with larger errors deepens its dips.
  So "robust up to 1.5" is about XR22's idealised split; a calibration with the error scale in the fit
  and a data-matched split is registered (T-059).

**With the error scale in the fit (R1-ERRCAL, T-059, 2026-11-23).** The next pre-registration (README
section 2.8) asked what R1 would read if the true errors were 2.0 or 2.81 times the quoted ones and the fit
knew it: null and power mocks drawn with those errors and fitted with them (5,400 mocks, 8.1 h over three
sessions; all reproduction checks passed).

- **The label is "at f = 2.0: not reproduced; at f = 2.81: not reproduced"** in the primary variant; the two
  other variants read "reproduced" at 2.81. At twice the quoted errors the bin [−0.5, −0.3) keeps a dip far
  shallower than an almost-disjoint split's (valley depth 0.42–0.47 against 0.25). At 2.81 times it comes
  down to 0.271 in the primary variant and 0.242 / 0.232 in the others, so the variants differ by
  0.01–0.02 around the threshold.
- **What this means (post hoc).** R1-SEL-FIT's "not reproduced" holds up to about twice the quoted errors
  whether or not the fit knows the error scale. Beyond that it depends on the variant, and the test
  constrains less than its rule suggests: the null mocks never lower the threshold, and the power is
  near 1 everywhere.
- **A caveat from the independent referee.** At these error scales the data fits put a component at the
  narrowest width allowed (0.1 Gyr), and narrow peaks make dips look deeper. Mocks drawn and fitted with
  the same scale cannot see that; a check with mocks fitted at a larger scale than they were drawn with,
  and an uncertainty on the data's dip depth, are registered (T-064). The dips of the data also lie later
  (9.6–11 Gyr) than those of XR22's idealised split (8.1–9.4 Gyr).

Exploring via chat: `python -m astrolab explore 010 --tag <topic> --set key=value`
reruns any fit with changed parameters (for example the J_φ cut, the error cut or the high-α
threshold) without touching the formal results; see the study README section 8.

### Glossary

| Term | Meaning |
|---|---|
| subgiant | star just past core-hydrogen exhaustion, between the main sequence and the red-giant branch; its luminosity is a sensitive age indicator |
| isochrone | model curve of stars of one age (and composition) in temperature–luminosity space |
| [Fe/H], [α/Fe] | logarithmic iron abundance relative to the Sun; α-element-to-iron ratio relative to the Sun |
| action J_φ | azimuthal action: angular momentum about the Galactic rotation axis |
| thick / old disc | the high-[α/Fe], kinematically hotter, older disc population |
| Gaia-Sausage-Enceladus (GSE) | dwarf galaxy that merged with the Milky Way roughly 8–11 Gyr ago, building much of the inner halo |
| radial migration | stars moving to other Galactocentric radii over time while keeping near-circular orbits |
| intrinsic scatter σ_int | spread of true ages at fixed [Fe/H], after removing measurement errors |
| deconvolution | inferring a true distribution from measurements blurred by known errors |

### Open questions

- How large is the absolute age-scale uncertainty of subgiant ages at 12–14 Gyr, across isochrone
  sets and abundance scales?
- Is the old disc's 5–6 Gyr enrichment consistent with asteroseismic evidence for a nearly coeval
  high-α disc, once tracers and definitions are matched?

### Changelog

Newest first.

- 2026-11-23: R1-ERRCAL (T-059, pre-registered README 2.8): R1 calibrated at f = 2.0 and 2.81 with the
  error scale in the fit (5,400 mocks; reproduction checks passed; the first session was ended for lack of
  system memory and resumed with the user's consent). "At f = 2.0: not reproduced; at f = 2.81: not
  reproduced" (term N and Full: reproduced at 2.81, margins 0.01–0.02) (part 3 updated). Independent
  referee done; mismatched-scale check registered (T-064).

- 2026-11-22: R1-ERR (T-054, pre-registered README 2.7): error-scale power test of R1-SEL-FIT (3,600
  mocks with errors 1.2–2.81 times the quoted ones; reproduction checks passed after rerunning with the
  default thread settings). "Robust up to f = 1.5 (one bin explainable from f = 2.0: [-0.3, -0.1))";
  Full reads "sensitive at f = 2.81" (part 3 updated). Independent referee done.
- 2026-11-21: R1-SEL-FIT (T-049, pre-registered README 2.6): R1-SEL rerun with data-independent
  starts in every mock fit (5,400 mocks; all reproduction checks passed). d* stays 0.25; 4 of 5 bins
  resolvable in every variant, none almost disjoint, so "not reproduced (robust; selection-term
  robust)", also at floor 0.20. R1-SEL's "undetermined" stands as recorded (part 3 updated). Independent
  referee: no bug; the result holds under the catalogue's quoted age errors (error-scale test T-054).
- 2026-11-20: re-test R-SEL (T-031) and its independent referee: R3-SEL reproduced, robust (span
  6.09 Gyr); R4-SEL not reproduced (2.55 Gyr); intrinsic-SEL confirmed, not robust (0.748 Gyr);
  R1-SEL undetermined, hinging on one bin's mock-fit-limited power (T-045); part 3 updated.
- 2026-11-20: diagnostic refit (T-045, post hoc): the deciding bin's missed mocks are local optima of the
  mock fits; with data-independent starts its power is 1.00, so R1-SEL would read "not reproduced" if the null
  mocks and other bins hold up (not tested); pre-registered rerun registered as T-049 (part 3
  updated).
- 2026-11-16: study run and independent referee: R2 reproduced (12.93 Gyr); R1 undetermined; R3/R4
  and the intrinsic scatter cannot be determined (the S15 selection term of M0 is misspecified, found
  by the referee; re-test T-031); `mod_bin` relabelled `gap_bin` (GAP), so three gaps; part 3 results.
- 2026-11-15: gate-1 review: the age of the universe is stated by XR22 (Planck 2015), so no premise is merely implied; `gap_onset` now lists four steps, and the Extended Data Fig. 2 tail is described as splashed disc stars, not halo contamination.
- 2026-11-15: first version: parts 1–3 (pre-registration source; plan `design/019-plan_*`).

### Sources

- Xiang & Rix 2022, Nature 603, 599, arXiv:2203.12110 (the paper studied; quotes from the arXiv v1 PDF).
- Miglio et al. 2021, A&A 645, A85, arXiv:2004.14806 (asteroseismic ages of the α-rich disc).
- Montalbán et al. 2021, Nature Astronomy, arXiv:2006.01783; Queiroz et al. 2023, A&A 673, A155, arXiv:2303.09926; Gallart et al. 2024, A&A 687, A168, arXiv:2402.09399.
- Chen, Sun & Ye 2025, arXiv:2510.10092; Shariat, El-Badry & Bhattacharjee 2025, OJAp, arXiv:2510.08675 (the subgiant age scale and errors).
- Feltzing, Feuillet & Bensby 2026, arXiv:2605.20959; Lu et al. 2026, arXiv:2607.02940.
- Planck Collaboration 2016, A&A 594, A13, arXiv:1502.01589 (age of the universe, XR22's ref. 19).

---

## 中文

### 第一部分 · 科普详解

#### 1.1 问题与意义

银河系有一个薄盘（thin disc，太阳所在、至今仍在形成恒星），还有一个更厚、更老的盘：它的恒星离盘面更远，相对于铁含有更多的"α 元素"（氧、镁、硅等）。高的 [α/Fe] 是化学时钟：α 元素很快由大质量恒星的核坍缩超新星（core-collapse supernova）抛出，而大部分铁要等到较晚的 Ia 型超新星（type Ia supernova）。所以高 [α/Fe] 的恒星形成于很早、很快被增丰的气体。

这个老盘何时形成、用了多久、与恒星晕以及盖亚卫星揭示的与矮星系"盖亚–香肠–恩克拉多斯"（Gaia-Sausage-Enceladus, GSE）的大并合有什么关系？回答这些问题需要大量恒星的**年龄**，而恒星年龄出了名地难测：对大多数恒星，年龄只微弱地改变我们能观测到的量。

#### 1.2 数据

Xiang 与 Rix（下称 XR22）用的是**亚巨星**（subgiant）：刚耗尽核心氢、正从主序走向红巨星支的恒星。在这一短暂阶段，光度对质量、从而对年龄非常敏感，所以光度加上温度与化学组成就能给出精确的年龄。他们结合了：

- LAMOST 巡天（大天区面积多目标光纤光谱天文望远镜，Large Sky Area Multi-Object Fiber Spectroscopic Telescope）第 7 次数据发布的光谱：温度、金属丰度 [Fe/H]、[α/Fe]，以及近红外 K 波段的光谱绝对星等；
- Gaia eDR3 的视差与自行：距离、几何绝对星等，以及（加上 LAMOST 视向速度的）轨道。轨道用**作用量**（action）概括；方位作用量 J_φ 就是绕银河系转轴的角动量（太阳附近近圆轨道的盘星 J_φ ≈ 1800–2000 kpc km/s，晕星的 J_φ 接近零或为负）。

清洗之后（双星检验、Gaia 天体测量质量、光变、LAMOST 信噪比大于 20、温度低于 6800 K，以及去除水平支（horizontal branch）星的截断——它同时去掉了几乎所有约 1.5 Gyr 以下的星），剩下 **247,104 颗亚巨星**。年龄由**延世–耶鲁（Yonsei-Yale, YY）等年龄线**（isochrone，同一年龄的恒星模型曲线）的贝叶斯拟合得到，并按 [α/Fe] = 0、0.2、0.4 的等年龄线加权以匹配每颗星的 α 增丰。年龄误差的中位数为 7.5%；分析只用相对年龄误差低于 15% 的星。星表公开在 VizieR（J/other/Nat/603.599）。

#### 1.3 一步一步：作者如何从数据走到结论

1. **年龄–金属丰度平面在分开之前很杂乱。** 把全部恒星按年龄与 [Fe/H] 作图，分布很复杂。XR22 用既不是年龄也不是 [Fe/H] 的量分开样本（式 1）：J_φ > 1500 kpc km/s **且** [α/Fe] 低（[Fe/H] < −0.5 时低于 0.16，否则低于 −0.16[Fe/H] + 0.08）的星为"晚期"（薄盘），其余为"早期"。
2. **两个区间，在 8 Gyr 处分开。** 晚期的星几乎都年轻于约 8 Gyr，在年龄–[Fe/H] 图上呈"V 形"（由径向迁移（radial migration）解释）；早期的星几乎都更老。摘要说这个平面"splits into two almost disjoint parts, separated at 8 Gyr"。
3. **早期包含两条序列。** 贫金属序列（−2.5 < [Fe/H] < −1）是晕；富金属序列（[Fe/H] ≳ −1）是老的高 α（厚）盘。以 J_φ = 500 kpc km/s 分开早期星就能把它们分开（图 3）。
4. **老盘约 13 Gyr 前开始形成。** 对早期中 J_φ > 500、−1.05 < [Fe/H] < −0.95 的星（"presumably the oldest thick disk stars"），年龄直方图的高斯拟合给出均值 13 Gyr（图中插图印的是 13.03 Gyr、宽度 1.81 Gyr；扩展数据图 1）。宇宙年龄 13.8 Gyr，所以这是"大爆炸之后仅 0.8 Gyr"。
5. **5–6 Gyr 的持续增丰，且序列很紧。** 沿老盘序列，[Fe/H] 从 13 Gyr 时的约 −1 升到约 7 Gyr 时的 +0.5。一个模型假设给定 [Fe/H] 时年龄是围绕直线 τ̄0 + a·[Fe/H]（拟合值 τ̄0 = 9.38 Gyr、a = −3.8 Gyr/dex）的高斯，并按每颗星的年龄误差与本征弥散（intrinsic scatter）σ_int 展宽；它给出 σ_int = 0.82 ± 0.01 Gyr，XR22 称之为上限。结合斜率，同一时间诞生的恒星的 [Fe/H] 弥散小于 0.22 dex：形成恒星的气体混合得很好。
6. **GSE 并合与恒星形成峰。** 角动量低但具有老盘化学的早期星（被并合加热的"溅出"盘星）只出现在约 11 Gyr 以上；老盘的恒星形成率（经体积改正后）在约 11.2 Gyr 达到峰值。XR22 由此认为 GSE 并合约在 11 Gyr 前基本完成。
7. **同一金属丰度下盘比晕老。** 在 [Fe/H] ≈ −1，老盘序列比晕序列老约 2 Gyr（"Z 形"）。

#### 1.4 结论与把握程度

摘要：老盘"started 13 Gyr ago, only 0.8 Gyr after the Big Bang"；"Most of these stars formed 11 Gyr ago, when the Gaia-Sausage-Enceladus satellite merged with our Galaxy"；此后 5–6 Gyr 银河系持续增丰，金属丰度增加了 10 倍。

论文自己讨论的注意事项（方法部分、扩展数据）：

- **绝对年龄标尺。** 在太阳 α 配比下，MIST（MESA Isochrones and Stellar Tracks）等年龄线给出的年龄比 YY 老约 0.5 Gyr；忽略 α 增丰会把老星的年龄高估至多 2 Gyr（XR22 考虑了 α 增丰）。没有先验强制年龄低于 13.8 Gyr；XR22 指出年龄"are consistent with the age of the universe at the old end"。
- **选择效应。** 老的亚巨星更暗，所以只能在更近的距离内看到。XR22 用 Gaia 模拟星表与体积改正检查，认为选择效应"negligible impact"。

其他工作提供了背景（2026-11-15 对照 arXiv 摘要与全文核实）：

- **几乎同龄的厚盘。** 开普勒视场中近 400 颗 α 增丰红巨星的星震学（asteroseismology）年龄（Miglio et al. 2021，arXiv:2004.14806；高 α 指 [α/Fe] > 0.1）给出约 11 Gyr 的平均年龄，并在用分层模型（hierarchical model）去卷积年龄误差之后得到"95% of the population was born within ∼1.5 Gyr"。这与老盘持续 5–6 Gyr 的增丰存在张力，不过两者的示踪体（星震学质量的红巨星 vs 等年龄线年龄的亚巨星）、视场与"高 α"的定义都不同。
- **其他方法给出更年轻的绝对年龄。** 95 颗红巨星的星震学（Montalbán et al. 2021，arXiv:2006.01783）把高 α 盘的开始定在"roughly ∼10 to 11.5 Gyr ago"；StarHorse 年龄（Queiroz et al. 2023，arXiv:2303.09926）给出真正厚盘的平均年龄 10.4–11.8 Gyr（依巡天而定）；Gaia 近邻恒星的颜色–星等图（Gallart et al. 2024，arXiv:2402.09399，一篇薄盘论文）把它与 XR22 的部分年龄标尺差异归因于等年龄线的选择。
- **亚巨星年龄标尺本身。** 用 LAMOST DR9 参数与不同的 α 增丰模型重新分析，2,866 颗共同星的年龄"systematically younger than those of [Xiang & Rix 2022] by ∼12.9%"（Chen, Sun & Ye 2025，arXiv:2510.10092）；在 13 Gyr 处约为 1.7 Gyr。宽双星（wide binaries）证实了 XR22 的*相对*年龄误差（12 对，去掉一个离群对之后弥散与给出的误差一致），但不能检验整体偏移（Shariat, El-Badry & Bhattacharjee 2025，arXiv:2510.08675）。
- **后来对起点的使用。** Feltzing, Feuillet & Bensby 2026（arXiv:2605.20959；319,835 颗 LAMOST 亚巨星）发现盘的自转建立（spin-up）在 −1.25 < [Fe/H] < −0.9，平均年龄 12.1 ± 2.8 Gyr；Lu 等 2026（arXiv:2607.02940）认为年龄误差使溅出星（Splash）显得更老（类似爱丁顿偏差（Eddington bias）），把 GSE 并合定在 10.1 ± 0.2 Gyr 前。

### 第二部分 · 论证逻辑

#### 2.0 论证地图

我们在 Lean 中编码一个结论：**老盘约 13 Gyr 前、即大爆炸之后约 0.8 Gyr 开始形成。** 它是论文和 Atlas 条目的标题结论；与 8 Gyr 分界或 σ_int 上限不同，它是从幸存恒星的年龄推断一个事件，隐含的步骤正藏在这里。

```
 YY α 增丰等年龄线的年龄 (mod_ages) ─────┐
 该箱是最老的厚盘星 (gap_bin) ───────────┤
 高斯均值 = 13 Gyr (stat_mean) ──────────┤
 年龄与宇宙年龄相容 (obs_scale) ─────────┼─[gap_scale]→ 绝对标尺准确
 宇宙年龄 13.8 Gyr (lit_universe) ───────┤
                                         └─[gap_onset]→ 盘约 13 Gyr 前开始形成，大爆炸后 0.8 Gyr
```

#### 2.1 环节 A · 年龄及其绝对标尺

*概述。* 这些年龄是模型年龄：把恒星的光度、温度与组成与 YY 等年龄线匹配。精度（7.5%）不等于准确度：换一套等年龄线，所有老年龄会一起移动相近的量。XR22 对标尺的检查是：最老的年龄与宇宙年龄相容。

*前提（Lean 的 `Field`）。*
- `mod_ages`（MOD，论文明说，扩展数据图 4）：年龄来自按 [α/Fe] = 0、0.2、0.4 加权的 YY 等年龄线。
- `obs_scale`（OBS，论文明说，方法部分）：老端的年龄与宇宙年龄相容。
- `gap_scale`（GAP，我们补上的）：这种相容性确立了 13 Gyr 处的绝对标尺，误差小于约 0.5 Gyr，远小于到大爆炸的 0.8 Gyr 余量。

*Lean 的发现。* 论文写出了定性的说法：年龄"seem to be reasonable as they are consistent with the age of the universe at the old end"（XR22 不加年龄先验，正是为了让恒星年龄独立地检验宇宙年龄）。论文与标准知识都没有给出的，是起点结论所需的定量准确度：远小于 0.8 Gyr 的余量（我们取约 0.5 Gyr）。与 13.8 Gyr 相容只排除了老得太多的标尺；向任一方向偏几个 0.1 Gyr 的标尺同样相容，而 XR22 自己与 MIST 的比较就差 0.5 Gyr；后来的重新分析得到的年龄年轻 12.9%（在 13 Gyr 处约 1.7 Gyr；Chen, Sun & Ye 2025）。"大爆炸之后 0.8 Gyr"是两个数之差（13.8 − 13.0），其不确定度与年龄标尺一样大。

#### 2.2 环节 B · 从平均年龄到起点

*概述。* 13 Gyr 是对早期中 J_φ > 500、一个很窄的金属丰度箱（−1.05 到 −0.95）的星拟合高斯所得的均值。拟合宽度为 1.81 Gyr，大于这个年龄上典型的年龄误差（约 1 Gyr），所以该箱跨越数 Gyr 的真实年龄，或含有误差更大的星，或两者兼有。正文用图 2 定性地支持这个起点（e 面板的序列在约 13 Gyr 处达到 [Fe/H] ≲ −1）；扩展数据图 1 是定量的途径，编码的是它。

*前提。*
- `gap_bin`（GAP，我们补上的）：该箱是最老的厚盘星。XR22 只写了 "presumably the oldest thick disk stars"，把它断言下来是我们的一步（2026-11-16 按独立审稿修改：原来按 MOD、论文明说编码，强于引文）。
- `stat_mean`（STAT，论文明说）：高斯均值为 13 Gyr（编码为 130 个 0.1 Gyr）。
- `lit_universe`（LIT，论文明说，方法部分："CMB measurements of Planck (13.8 Gyr)"；XR22 的参考文献 19 是 Planck 2015，arXiv:1502.01589）：宇宙年龄 13.8 Gyr。
- `gap_onset`（GAP，我们补上的）：该箱中幸存的本地恒星的平均年龄标定了盘开始形成的时间。

*Lean 的发现。* `gap_onset` 承载四个没写出的步骤：

1. **均值不是起点。** 如果盘在 13 Gyr 前开始形成，该箱约一半的星更年轻，所以均值标定的是该箱的典型星；把它读作起点会晚于最早的星，这对"早"的结论是保守的。反过来，以 13.03 Gyr 为中心、宽 1.81 Gyr、误差约 1 Gyr 的分布意味着一些真实年龄超过 13.8 Gyr，这又指回年龄标尺（`gap_scale`）。
2. **幸存者与迁移。** 今天在太阳附近几 kpc 内看到的星是幸存者，其中一些向外或向内迁移过，它们的年龄描述的是恒星现在在哪里，而不是盘最先在哪里形成。
3. **J_φ 截断不能干净地分开各成分**（我们的推理）：顺行轨道的晕星可以通过 J_φ > 500，它们在这个金属丰度下约*年轻* 2 Gyr，会把均值拉低；而老的"溅出"盘星（XR22 扩展数据图 2 显示为 −1 ≲ [Fe/H] ≲ −0.4 的低 J_φ 尾巴）被截断去掉，这同样把均值拉低；两种效应的大小都不清楚。
4. **观测年龄的均值可能有偏。** 15% 相对误差截断、老亚巨星更暗（体积效应）以及 20 Gyr 网格边缘附近不对称的误差（没有年龄先验）都会移动观测年龄的均值；年龄误差会使截断后的分布向更老偏移，即类似爱丁顿偏差（Eddington-like bias）的效应（Lu et al. 2026，arXiv:2607.02940）。我们的 R2 检验其中误差截断的部分。

#### 2.3 其他结论（只讨论，不编码）

- **8 Gyr 分界。** 分群用了与年龄相关的 [α/Fe]，所以"晚期老星少、早期年轻星少"部分是化学截断的结果。要说明*年龄–金属丰度平面本身*分成两个几乎不相交的部分，需要不用分群、直接检验密度。这是我们的 R1。
- **0.82 Gyr 的本征弥散。** XR22 的模型只把年龄误差按平方和加入。年龄与 [Fe/H] 的误差相关（年龄拟合用到 [Fe/H]），而"老的高 α 序列"（其图 2 的 e 面板）的样本定义会影响结果：给定 [Fe/H] 时 [α/Fe] 与年龄相关，按 [α/Fe] 截断会削去年轻一侧、降低 σ_int。这是我们的 R3/R4。
- **11 Gyr 与 GSE。** 11.2 Gyr 的峰需要选择效应的体积改正，公开星表没有它；我们只能描述，不能检验。

#### 2.4 Lean 检查发现的问题

1. **最重要的结论：`explicit_insufficient`，有三个缺口。** 起点结论需要把该箱认定为最老的厚盘星（`gap_bin`，XR22 写的是 "presumably"）、准确的绝对年龄标尺（`gap_scale`），并把一个箱的平均年龄读作盘开始形成的时间（`gap_onset`）。没有标准知识能补上其中任何一个。
2. **排序。** `gap_onset` 最重要：它是论文没有讨论的建模选择，而该箱的拟合宽度（1.8 Gyr）大于到大爆炸的 0.8 Gyr 余量。`gap_scale` 是已知的等年龄线系统误差（YY 与 MIST 差 0.5 Gyr）。
3. **在本编码下七个前提都是必要的**，没有多余的。
4. **`stated_insufficient`** 也成立，原因相同：没有只属标准知识的前提（宇宙年龄在方法部分写明），所以论文明说的前提与显式前提相同，缺的只是三个缺口。
5. **相容性**（`consistent`）在这里是弱检查：没有否定形式的前提。
6. **局限：** Lean 检查的是在我们的编码下论证的逻辑结构，不检查每个前提内部的恒星物理。特别是 `gap_onset` 的后件就是结论本身：Lean 说明结论依赖这座没写出的桥，而不说明这座桥成立。
7. **与计划的偏离。** 计划 019 设想一个绑定 R2 结果的 NUM 前提；这里均值按 XR22 明说的数字编码（STAT），因为论证是论文的论证，我们的 R2 结果在第三部分报告。

### 第三部分 · 本项目可检验或探索的环节

**交互网页：**[打开本研究的网页](https://sudoghut.github.io/astrolab/studies/010-m05-thick-disc-subgiant-ages/web/)（结果、图与表，可切换中英文；网站重新发布时更新）。

星表（VizieR J/other/Nat/603.599/table1，247,104 行）经受守卫的 `ctx.http` 通道从 CfA 的 VizieR 镜像取一次（本机连不上 CDS 的 TAP 主机），只取所需的列（Id、Age、e_Age、[Fe/H]、e_[Fe/H]、[alpha/Fe]、e_[alpha/Fe]、JPHI、MKcomb）：5 行试取实测每行 65 字节，合计约 16 MB。设计见 [`design/019-plan_*`](https://github.com/sudoghut/astrolab/blob/main/design/019-plan_m05-thick-disc-early-formation-subgiant-age-metallicity-sequence.md)；判决规则在完整取数之前冻结于研究 README 第 2–4 节。所有年龄拟合用同一个观测模型（M0）：潜在年龄在 YY 网格 [0, 20] Gyr 上，每颗星的测量年龄以真实年龄为中心、宽度为其 e_Age 的高斯并截断到网格，在 15% 精度的样本 S15 上用以入选为条件的似然。

| 环节 / 结论 | 能否检验或探索 | 怎么做 | 数据（大小） | 判据 | 结果 |
|---|---|---|---|---|---|
| 环节 B：13 Gyr 的起点（R2） | 现在可检验 | 在 XR22 扩展数据图 1 的选择（早期、J_φ > 500、−1.05 < [Fe/H] < −0.95）以及不加早期过滤的选择中对观测年龄拟合高斯；另报告去卷积的均值（M0）、年龄超过 13.8 Gyr 与靠近 20 Gyr 网格边缘的比例，以及对 J_φ 截断与误差截断的敏感度 | 星表（16 MB） | 观测年龄的高斯均值在 12.5–13.5 Gyr 即复现（对取整的"13 Gyr"的容差） | **复现**：12.93 ± 0.06 Gyr（σ 2.40）；去卷积 12.19–12.59 |
| 环节 A：绝对标尺（`gap_scale`） | 可探索（不能判决） | 由文献幅度构成的包络：MIST +0.5 Gyr，[α/Fe] 误差与 LAMOST–APOGEE 的 α 偏移经 XR22 的年龄–α 敏感度传播，LAMOST [Fe/H]/Teff 偏移，视差零点 | – | 无，只作探索 | 包络 0.7–1.1 Gyr；重新分析 −1.7 Gyr；距大爆炸余量 0.87 Gyr |
| 8 Gyr 分界（R1） | 现在可检验 | 不用化学分群：在五个 0.2 dex 的 [Fe/H] 箱（−0.7 到 +0.3）中，用 M0 去卷积潜在年龄密度（高斯混合（Gaussian mixture），K = 1–4 按贝叶斯信息准则（Bayesian information criterion, BIC）选取）；5–11 Gyr 之间的谷深（valley depth）d；阈值 d* = min(0.25, 零模型第 3 小的 d)，取自两个对数凹（log-concave）零模型族（偏斜正态（skew-normal）与两段正态（split normal）；代替计划 019 的非参数对数凹检查，标为偏离）与两种误差机制，各 50 个模拟；检出率来自类 XR22 的两分量模拟；年轻一侧的 97.5% 分位数与 8 Gyr 比较 | 星表（16 MB） | 有谷且 d < d* 的箱为"几乎不相交"（每组零模拟至多 2/50 通过）；可分辨的箱（检出率 ≥ 80%）≥ 3 个、其中几乎不相交的 ≥ 3 个、年轻一侧上缘中位数在 6.5–9.5 Gyr 即复现；S15 与全样本一致才算稳健 | **无法判定**（5 个箱中 2 个可分辨；没有几乎不相交的箱，d = 0.29–0.58） |
| 老盘序列：斜率、5–6 Gyr 跨度、σ_int（R3/R4） | 现在可检验 | 在 M0 中对样本 A（S15、高于 α 线、J_φ > 500、−1.2 < [Fe/H] < 0.5）拟合 XR22 的线性加弥散模型：σ_sel 是这一 α 选择样本的弥散，与 XR22 的数字同类比较，不是本征弥散的检验；两种误差机制的恢复模拟；本征弥散由样本 B（不加 α 截断）与均值随 [Fe/H] 线性变化的背景分量判定，用可辨识性与误设模拟检查；误差标尺因子 f = 0.8、1 与由数据得到的上限 | 星表 | R4：\|σ_sel − 0.82\| ≤ 0.1 Gyr；R3：跨度 \|a\| × 1.5 dex 在 4.5–6.5 Gyr；每个敏感度拟合都通过才算稳健；本征：σ_int + 1.645 SE < 0.82 Gyr 为确认，σ_int − 1.645 SE ≥ 0.82 为不确认，其余（或任一组模拟偏差超过 0.1 Gyr）为"无法判定" | **无法判定**（恢复检验 σ 偏差 +0.25–0.28 Gyr；跨度 6.0，σ_sel 2.67，σ_int 0.79） |
| 与 Miglio et al. 2021 的张力（R7） | 可探索（有限定的比较） | 高 α 盘去卷积的总年龄跨度：中心 95% 宽度与任一 1.5 Gyr 窗口内的最大比例，分别用 XR22 的样本与类 APOGEE 的高 α 截断 | 星表 | 无，跨示踪体（tracer）的比较 | 很宽：f = 1 时 95% 宽度 12.6–13.0 Gyr |
| [Fe/H] ≈ −1 处晕与盘的偏移（R5） | 可探索（只作图） | 按 J_φ 分面的年龄–[Fe/H] 密度 | 星表 | 无 | 见研究网页的图 |
| 11 Gyr / GSE（R6） | 可描述，不能检验 | 低 J_φ 老盘星年龄的 5% 与 10% 分位数；未做体积改正的年龄峰 | 星表 | 无，体积改正未公开 | 观测年龄峰 11.1 Gyr（J_φ > 500） |
| `gap_onset` 本身（幸存者、迁移） | 不在范围内 | 需要化学演化与迁移模型 | – | – | – |

**我们的发现（2026-11-16）。** 在已发表的星表上，最老盘箱的 13 Gyr 均值在星表自己的年龄标尺上复现（12.93 Gyr），但它随等年龄线与 α 标尺变化约 1 Gyr、随去卷积变化 0.3–0.7 Gyr，而距大爆炸只有 0.87 Gyr 的余量，所以 `gap_scale` 是关键的一步。8 Gyr 分界无法判定：在数据能分辨的箱里，潜在年龄密度在两个阶段之间下凹，但没有到"几乎不相交"（而且功效模型（power model）的下限使一个富金属箱按构造无法分辨）。老盘序列也无法判定，因为我们去卷积中 15% 误差截断的选择项（selection term）在两种模拟误差机制下都设定错误（独立审稿（referee）发现，事后（post hoc））；非正式地看，跨度（约 6 Gyr）一致，α 选择样本的离散（2.4–2.7 Gyr）约为 XR22 的 0.82 Gyr 的三倍，可能不是同类比较。已登记重新检验（T-031）。数字与网页见研究 README 第 5 节与[网页（在线版）](https://sudoghut.github.io/astrolab/studies/010-m05-thick-disc-subgiant-ages/web/)。

**用一致的选择项重新检验（T-031，2026-11-20）。** 新的预注册（README 第 2.5 节）把选择项换成在星表上按观测年龄测得的通过比例，模拟的误差也按数据中对年龄的依赖抽取。上面的原标签作为预注册的结果保持不变；重新检验的标签是当前的解读。

- **老盘跨度复现，且稳健：** 1.5 dex 上 6.09 Gyr（各稳健性拟合中为 5.9–6.3）。
- **α 选择样本的离散未复现：** 2.55 Gyr，而 XR22 为 0.82。
- **老序列的内禀离散确认低于 0.82 Gyr：** 在带背景成分的混合模型中为 0.748 Gyr。它不稳健：误差乘以 0.8 后就无法判定。
- **8 Gyr 分界仍无法判定。** 标签取决于一个贫金属箱，而该箱的功效受限于漏掉谷的模拟拟合（独立审稿，事后）。诊断性重拟合（T-045，探索，事后）说明了原因：漏掉的模拟是模拟拟合的局部最优；用与数据无关的起点时每个模拟都找到谷，该箱六组的功效都是 1.00（记录值 0.58–0.88）。所以这个箱会是可分辨的，而没有一个箱的谷几乎不相交，只要零假设模拟与其他箱在同样的重拟合下保持不变（未检验），结论会是"未复现"；记录的标签仍是"无法判定"；用更好的模拟拟合做的预注册重跑（T-049）在下面作为 R1-SEL-FIT 报告。
- **不加选择项的变体。** 它在内禀离散上给出相同结论；在模拟的误差生成器下，它对序列的回收检验失败，所以 R3/R4 带有"对选择项敏感"。事后看，审稿的证据指向这个生成器是原因（推断：在原生成器下这个变体能够恢复）。

**用更好的模拟拟合重跑 8 Gyr 分界（R1-SEL-FIT，T-049，2026-11-21）。** 又一次预注册（README 第 2.6 节）重跑了 R1-SEL：每个模拟拟合（零假设模拟与功效模拟，所有箱与变体，共 5,400 次，5.3 小时）都对每个混合成分数加入 8 个与数据无关的起点。其余一切不变，原拟合重现了每一次记录的模拟。

- **零假设模拟没有移动阈值。** 没有零假设模拟的谷通过，所以 d* 仍在上限 0.25。
- **三个贫金属箱在每个变体中功效都是 1.00**，箱 [−0.1, 0.1) 也变为可分辨（功效 0.84–1.00）。
- **标签为"未复现（稳健；对选择项稳健）"**，功效下限 0.20 时相同，与预注册的预期一致。每个变体都是 5 个箱中 4 个可分辨，但没有一个箱的谷几乎不相交（数据 d = 0.37–0.58，阈值 0.25）。
- **这意味着什么。** 对数据的拟合显示在固定 [Fe/H] 下老、年轻两个阶段之间有下凹，但没有 8 Gyr 分界所说的近乎断开。这以星表给出的年龄误差为前提（功效模拟用的就是它们）；更大的真实误差可能把近乎断开抹成这样的下凹，这一点未检验（独立审稿；误差尺度检验 T-054）。功效模型是最有利的形状，所以这个标签说的是数据没有显示 XR22 理想化的分界。
- **R1-SEL 的"无法判定"保持不变**，作为那一部分预注册的结果。R1-SEL-FIT 是用改进的模拟拟合所做的重跑，不是更正；R1-SEL 在两个标签之间的分界是由模拟优化器决定的。
- **最富金属的箱 [0.1, 0.3) 仍不可分辨**（功效 0.30–0.70）：混合模型仍会抹平生成模型陡峭的年轻端边缘。

**年龄误差要多大才行？（R1-ERR，T-054，2026-11-22）。** 又一次预注册（README 第 2.7 节）问：XR22 理想化的分界，如果观测误差是星表给出误差的 f 倍、而拟合仍按数据的方式（用给出的误差）进行，能否在三个贫金属箱中产生数据中的下凹？3,600 个功效模拟（f = 1.2、1.5、2.0、2.81；两种误差机制；三个变体），4.2 小时；复现检查全部通过。

- **标签为"robust up to f = 1.5 (one bin explainable from f = 2.0: [-0.3, -0.1))"**（到 f = 1.5 都稳健；从 f = 2.0 起有一个箱可解释）。在给出误差的 1.5 倍以内，没有一组的任何模拟达到数据的下凹深度（全部 36 组都是 50 个中 0 个）：模糊后的分界留下的谷仍远比数据的深。
- **从约两倍的给出误差起**，间隙最小的箱 [−0.3, −0.1) 不再能区分两种解读（50 个模拟中 47–50 个达到数据的 d）。在 2.81 倍时，带选择项的变体中这个箱的分界被完全抹平（没有谷），而箱 [−0.5, −0.3) 在 N 项与 Full 中开始达到；Full 为"sensitive at f = 2.81"（在 f = 2.81 敏感）。
- **这意味着什么（事后）。** R1-SEL-FIT 的"未复现"不要求给出的误差完全准确：XR22 理想化的分界需要约为给出值两倍的年龄误差，才会看起来像数据。在这样的尺度下，XR22 自己的 0.82 Gyr 宽度没有给额外的误差留下余地，而一项用 11 对宽双星的独立检验发现给出的误差是一致的；f ≈ 2 是否可信不在本检验范围内。偏斜的、先验形状的误差核仍未检验。
- **独立审稿的保留意见。** 理想化的分界比数据年轻，其间隙从 7 Gyr 开始，而数据的下凹在 7.5–9.8 Gyr；形状更像数据的分界可能在更小的误差尺度下就填平下凹，而用更大的误差重拟合数据会让它的下凹变深。所以"到 1.5 倍都稳健"针对的是 XR22 理想化的分界；把误差尺度放进拟合、并用与数据匹配的分界做的校准已登记（T-059）。

**把误差尺度放进拟合（R1-ERRCAL，T-059，2026-11-23）。** 下一次预注册（README 第 2.8 节）问：若真实误差是给出值的 2.0 或 2.81 倍、且拟合知道这一点，R1 会读作什么？零假设与功效模拟用这样的误差生成并以之拟合（5,400 个模拟，三次会话共 8.1 小时；复现检查全部通过）。

- **主变体的标签为"at f = 2.0: not reproduced; at f = 2.81: not reproduced"**（两个 f 下都未复现）；另两个变体在 2.81 读作"复现"。在两倍的给出误差下，箱 [−0.5, −0.3) 的下凹仍远浅于几乎不相交的分界（谷深 0.42–0.47，阈值 0.25）。在 2.81 倍时，主变体降到 0.271，另两个为 0.242 / 0.232，所以各变体在阈值附近相差 0.01–0.02。
- **这意味着什么（事后）。** 无论拟合是否知道误差尺度，R1-SEL-FIT 的"未复现"在约两倍的给出误差以内都成立。超过这个尺度就取决于变体，而且这项检验的约束力比其规则看上去的要弱：零假设模拟从未降低阈值，功效处处接近 1。
- **独立审稿的保留意见。** 在这样的误差尺度下，数据拟合把一个成分放在允许的最窄宽度（0.1 Gyr），窄峰会让下凹显得更深。以同一尺度生成并拟合的模拟看不到这一点；用比生成时更大的尺度拟合模拟的检验，以及数据下凹深度的不确定度，已登记（T-064）。数据的下凹也比 XR22 理想化分界的晚（9.6–11 Gyr 对 8.1–9.4 Gyr）。

对话探索：`python -m astrolab explore 010 --tag <主题> --set 键=值` 可用改变的参数（例如 J_φ 截断、误差截断或高 α 阈值）重跑任一拟合，不影响正式结果；见研究 README 第 8 节。

### 术语表

| 术语 | 含义 |
|---|---|
| 亚巨星（subgiant） | 刚耗尽核心氢、位于主序与红巨星支之间的恒星；其光度是灵敏的年龄指标 |
| 等年龄线（isochrone） | 同一年龄（与组成）的恒星在温度–光度空间中的模型曲线 |
| [Fe/H]、[α/Fe] | 相对太阳的铁丰度（对数）；相对太阳的 α 元素与铁之比 |
| 作用量 J_φ（action） | 方位作用量：绕银河系转轴的角动量 |
| 厚盘 / 老盘（thick / old disc） | 高 [α/Fe]、运动学上更热、更老的盘族群 |
| 盖亚–香肠–恩克拉多斯（GSE） | 约 8–11 Gyr 前与银河系并合的矮星系，构成了内晕的大部分 |
| 径向迁移（radial migration） | 恒星在保持近圆轨道的同时随时间移到其他银心距 |
| 本征弥散 σ_int（intrinsic scatter） | 去掉测量误差后，给定 [Fe/H] 时真实年龄的弥散 |
| 去卷积（deconvolution） | 由被已知误差模糊的测量推断真实分布 |

### 开放问题

- 亚巨星年龄在 12–14 Gyr 处、跨等年龄线与丰度标尺的绝对标尺不确定度有多大？
- 在示踪体与定义匹配之后，老盘 5–6 Gyr 的增丰与星震学所示几乎同龄的高 α 盘是否相容？

### 研究进展

按时间倒序。

- 2026-11-23：R1-ERRCAL（T-059，预注册见 README 2.8）：把误差尺度放进拟合，在 f = 2.0 与 2.81 下校准 R1（5,400 个模拟；复现检查通过；第一次会话因系统内存不足被终止，经用户同意续跑）。"at f = 2.0: not reproduced; at f = 2.81: not reproduced"（N 项与 Full 在 2.81 复现，余量 0.01–0.02）（更新第三部分）。独立审稿已做；尺度不匹配的检验已登记（T-064）。

- 2026-11-22：R1-ERR（T-054，预注册见 README 2.7）：R1-SEL-FIT 的误差尺度功效检验（3,600 个模拟，误差为给出值的 1.2–2.81 倍；改用默认线程设置重跑后复现检查通过）。"robust up to f = 1.5 (one bin explainable from f = 2.0: [-0.3, -0.1))"；Full 为"sensitive at f = 2.81"（更新第三部分）。独立审稿已做。
- 2026-11-21：R1-SEL-FIT（T-049，预注册见 README 2.6）：在每个模拟拟合中加入与数据无关的起点重跑 R1-SEL（5,400 次模拟；重现检查全部通过）。d* 仍为 0.25；每个变体 5 个箱中 4 个可分辨，没有几乎不相交的箱，所以为"未复现（稳健；对选择项稳健）"，下限 0.20 时相同。R1-SEL 的"无法判定"按记录保持不变（更新第三部分）。独立审稿：没有错误；结论以星表给出的年龄误差为前提（误差尺度检验 T-054）。
- 2026-11-20：重新检验 R-SEL（T-031）及其独立审稿：R3-SEL 复现、稳健（跨度 6.09 Gyr）；R4-SEL 未复现（2.55 Gyr）；内禀离散-SEL 确认、不稳健（0.748 Gyr）；R1-SEL 无法判定，取决于一个功效受模拟拟合限制的箱（T-045）；更新第三部分。
- 2026-11-20：诊断性重拟合（T-045，事后）：关键箱漏掉的模拟是模拟拟合的局部最优；用与数据无关的起点时功效为 1.00，所以如果零假设模拟与其他箱保持不变（未检验），R1-SEL 会读作"未复现"；预注册重跑登记为 T-049（更新第三部分）。
- 2026-11-16：研究运行与独立审稿：R2 复现（12.93 Gyr）；R1 无法判定；R3/R4 与本征弥散无法判定（M0 的 S15 选择项设定错误，独立审稿发现；重新检验 T-031）；`mod_bin` 改为 `gap_bin`（GAP），因而有三个缺口；补上第三部分的结果。
- 2026-11-15：闸门 1 审查：宇宙年龄由 XR22 写明（Planck 2015），没有只属标准知识的前提；`gap_onset` 列出四个步骤，扩展数据图 2 的尾巴描述为溅出的盘星，而不是晕的混入。
- 2026-11-15：第一版：第一至第三部分（预注册的来源；计划 `design/019-plan_*`）。

### 来源

- Xiang & Rix 2022，Nature 603, 599，arXiv:2203.12110（被研究的论文；引文据 arXiv v1 PDF）。
- Miglio 等 2021，A&A 645, A85，arXiv:2004.14806（α 增丰盘的星震学年龄）。
- Montalbán 等 2021，Nature Astronomy，arXiv:2006.01783；Queiroz 等 2023，A&A 673, A155，arXiv:2303.09926；Gallart 等 2024，A&A 687, A168，arXiv:2402.09399。
- Chen, Sun & Ye 2025，arXiv:2510.10092；Shariat, El-Badry & Bhattacharjee 2025，OJAp，arXiv:2510.08675（亚巨星年龄标尺与误差）。
- Feltzing, Feuillet & Bensby 2026，arXiv:2605.20959；Lu 等 2026，arXiv:2607.02940。
- Planck Collaboration 2016，A&A 594, A13，arXiv:1502.01589（宇宙年龄，XR22 的参考文献 19）。
