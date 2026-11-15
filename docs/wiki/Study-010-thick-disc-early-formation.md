# When did the Milky Way's disc begin? Ages of a quarter of a million subgiants

[English](#english) · [中文](#中文)

*Paper: Xiang & Rix 2022, "A time-resolved picture of our Milky Way's early formation history", Nature 603, 599, arXiv:2203.12110. Study:
[`studies/010-m05-thick-disc-subgiant-ages`](https://github.com/sudoghut/astrolab/tree/main/studies/010-m05-thick-disc-subgiant-ages).
Status: planned. Last updated: 2026-11-15 (see the changelog at the end). The source of this page lives in the main repository at
[`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki); edit it there.*

*中文标题：银河系的盘何时开始形成？二十五万颗亚巨星的年龄。状态：计划中。论文：Xiang & Rix 2022，Nature 603, 599，arXiv:2203.12110。研究：[`studies/010-m05-thick-disc-subgiant-ages`](https://github.com/sudoghut/astrolab/tree/main/studies/010-m05-thick-disc-subgiant-ages)。最后更新：2026-11-15（见文末"研究进展"）。本页源文件在主仓库的 [`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki) 中，请在那里修改。*

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

- spectra from the LAMOST survey (data release 7), giving temperature, metallicity [Fe/H], [α/Fe] and
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
   histogram gives a mean of 13.03 Gyr with a width of 1.81 Gyr (Extended Data Fig. 1). With a
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

- **The absolute age scale.** MIST isochrones give ages about 0.5 Gyr older than YY at solar α;
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
 bin = oldest thick-disc stars (mod_bin) ─┤
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
  better than about 0.5 Gyr.

*What Lean shows.* The step from `obs_scale` to an accurate scale is not in the paper and is not
standard knowledge. Consistency with 13.8 Gyr only excludes scales far too old; a scale off by a few
tenths of a Gyr in either direction is equally consistent, and XR22's own comparison with MIST gives
0.5 Gyr; a later re-analysis finds ages 12.9% younger (about 1.7 Gyr at 13 Gyr; Chen, Sun & Ye 2025). An onset "0.8 Gyr after the Big Bang" is a difference of two numbers, 13.8 − 13.0, and is
as uncertain as the age scale.

#### 2.2 Stage B · From a mean age to an onset

*Summary.* The 13 Gyr is the mean of a Gaussian fitted to stars in one narrow metallicity bin
(−1.05 to −0.95) of the early phase with J_φ > 500. The fitted width is 1.81 Gyr, wider than the
typical age error at this age (about 1 Gyr), so the bin spans several Gyr of real ages, or contains
stars with larger errors, or both.

*Premises.*
- `mod_bin` (MOD, stated, "presumably the oldest thick disk stars"; the hedge is encoded as an
  assertion).
- `stat_mean` (STAT, stated): the Gaussian mean is 13 Gyr (encoded as 130 tenths of a Gyr).
- `lit_universe` (LIT, implied: Planck 2018, arXiv:1807.06209): the universe is 13.8 Gyr old.
- `gap_onset` (GAP, reconstructed): the mean age of surviving local stars in this bin dates the start
  of disc formation.

*What Lean shows.* `gap_onset` carries three unstated steps: (i) a mean is not a start; if the disc
started 13 Gyr ago, half the bin is younger, so the mean dates the bin's typical star, and the
"onset" is the mean only if the bin samples just the first episode; (ii) stars seen today within a
few kpc of the Sun are survivors, some of which migrated outward or inward, so their ages describe
where stars now are, not where the disc first formed; (iii) at [Fe/H] ≈ −1 a J_φ > 500 cut can admit
halo stars (XR22's Extended Data Fig. 2 shows a low-J_φ tail in this metallicity range), which are
about 2 Gyr *younger* at this metallicity and pull the mean down, while old metal-poor stars from
other components could pull it up.

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

1. **Headline: `explicit_insufficient`, with two gaps.** The onset claim needs an accurate absolute
   age scale (`gap_scale`) and the reading of a bin's mean age as the start of disc formation
   (`gap_onset`). No standard knowledge closes either.
2. **Ranking.** `gap_onset` matters most: it is a modelling choice the paper does not discuss, and the
   bin's fitted width (1.8 Gyr) is larger than the 0.8 Gyr margin to the Big Bang. `gap_scale` is the
   known isochrone systematic (0.5 Gyr between YY and MIST).
3. **All seven premises are needed** in this encoding; none is redundant.
4. **`stated_insufficient`** holds as well: the age of the universe is only cited, and the two gaps are
   not stated.
5. **Consistency** (`consistent`) is a weak check here: no premise is negative.
6. **Limits:** Lean checks the logical structure under our encoding, not the stellar physics inside
   each premise.

### Part 3 · What astrolab can test or explore

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
| Stage B: onset at 13 Gyr (R2) | testable now | Gaussian fit to observed ages in XR22's Extended Data Fig. 1 selection (early phase, J_φ > 500, −1.05 < [Fe/H] < −0.95); also the deconvolved mean (M0), the fraction of ages above 13.8 Gyr and near the 20 Gyr grid edge, and sensitivity to the J_φ cut and the error cut | catalogue (16 MB) | reproduced if the observed-age Gaussian mean is 12.5–13.5 Gyr (a tolerance for the rounded "13 Gyr") | pending |
| Stage A: absolute scale (`gap_scale`) | explorable (not decisive) | envelope from literature magnitudes: MIST +0.5 Gyr, [α/Fe] error and LAMOST–APOGEE α offset through XR22's age–α sensitivity, LAMOST [Fe/H]/Teff offsets, parallax zero point | – | none - exploration only | pending |
| 8 Gyr split (R1) | testable now | without the chemical split: in 0.2 dex [Fe/H] bins, deconvolved age density (Gaussian mixture, K = 1–4 by BIC, M0); count modes and measure valley depth; null calibrated by simulation from a unimodal skew-normal fit; young-side upper edge compared with 8 Gyr | catalogue | "almost disjoint" threshold on valley depth fixed in the pre-registration, 5% false-positive rate | pending |
| Old-disc sequence: slope, 5–6 Gyr span, σ_int (R3/R4) | testable now | XR22's linear-plus-scatter model inside M0 on the high-α, J_φ > 500 sample (σ_sel, a reproduction of XR22's number); a background-mixture fit without the α cut for the intrinsic scatter; version with [Fe/H] errors as a bracket; error-scale checks in both directions | catalogue | σ_sel compared with 0.82 Gyr (rule fixed after checking XR22's estimator); span compared with 5–6 Gyr | pending |
| Tension with Miglio et al. 2021 (R7) | explorable (qualified comparison) | deconvolved total age spread of the high-α disc: central 95% width and the largest fraction in any 1.5 Gyr window, for XR22's sample and an APOGEE-like high-α cut | catalogue | none - comparison across tracers | pending |
| Halo–disc offset at [Fe/H] ≈ −1 (R5) | explorable (plots only) | age–[Fe/H] density split by J_φ | catalogue | none | pending |
| 11 Gyr / GSE (R6) | describable, not testable | 5th and 10th percentiles of ages of low-J_φ old-disc stars; age peak without volume correction | catalogue | none - the volume correction is not public | pending |
| `gap_onset` itself (survivors, migration) | out of scope | needs chemical-evolution and migration models | – | – | – |

Exploring via chat: once the study is implemented, `python -m astrolab explore 010 --tag <topic> --set key=value`
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

- 2026-11-15: first version: parts 1–3 (pre-registration source; plan `design/019-plan_*`).

### Sources

- Xiang & Rix 2022, Nature 603, 599, arXiv:2203.12110 (the paper studied; quotes from the arXiv v1 PDF).
- Miglio et al. 2021, A&A 645, A85, arXiv:2004.14806 (asteroseismic ages of the α-rich disc).
- Montalbán et al. 2021, Nature Astronomy, arXiv:2006.01783; Queiroz et al. 2023, A&A 673, A155, arXiv:2303.09926; Gallart et al. 2024, A&A 687, A168, arXiv:2402.09399.
- Chen, Sun & Ye 2025, arXiv:2510.10092; Shariat, El-Badry & Bhattacharjee 2025, OJAp, arXiv:2510.08675 (the subgiant age scale and errors).
- Feltzing, Feuillet & Bensby 2026, arXiv:2605.20959; Lu et al. 2026, arXiv:2607.02940.
- Planck Collaboration 2020, A&A 641, A6, arXiv:1807.06209 (age of the universe).

---

## 中文

### 第一部分 · 科普详解

#### 1.1 问题与意义

银河系有一个薄盘（thin disc，太阳所在、至今仍在形成恒星），还有一个更厚、更老的盘：它的恒星离盘面更远，相对于铁含有更多的"α 元素"（氧、镁、硅等）。高的 [α/Fe] 是化学时钟：α 元素很快由大质量恒星的核坍缩超新星（core-collapse supernova）抛出，而大部分铁要等到较晚的 Ia 型超新星（type Ia supernova）。所以高 [α/Fe] 的恒星形成于很早、很快被增丰的气体。

这个老盘何时形成、用了多久、与恒星晕以及盖亚卫星揭示的与矮星系"盖亚–香肠–恩克拉多斯"（Gaia-Sausage-Enceladus, GSE）的大并合有什么关系？回答这些问题需要大量恒星的**年龄**，而恒星年龄出了名地难测：对大多数恒星，年龄只微弱地改变我们能观测到的量。

#### 1.2 数据

Xiang 与 Rix（下称 XR22）用的是**亚巨星**（subgiant）：刚耗尽核心氢、正从主序走向红巨星支的恒星。在这一短暂阶段，光度对质量、从而对年龄非常敏感，所以光度加上温度与化学组成就能给出精确的年龄。他们结合了：

- LAMOST 巡天第 7 次数据发布的光谱：温度、金属丰度 [Fe/H]、[α/Fe]，以及近红外 K 波段的光谱绝对星等；
- Gaia eDR3 的视差与自行：距离、几何绝对星等，以及（加上 LAMOST 视向速度的）轨道。轨道用**作用量**（action）概括；方位作用量 J_φ 就是绕银河系转轴的角动量（太阳附近近圆轨道的盘星 J_φ ≈ 1800–2000 kpc km/s，晕星的 J_φ 接近零或为负）。

清洗之后（双星检验、Gaia 天体测量质量、光变、LAMOST 信噪比大于 20、温度低于 6800 K，以及去除水平支（horizontal branch）星的截断——它同时去掉了几乎所有约 1.5 Gyr 以下的星），剩下 **247,104 颗亚巨星**。年龄由**延世–耶鲁（Yonsei-Yale, YY）等年龄线**（isochrone，同一年龄的恒星模型曲线）的贝叶斯拟合得到，并按 [α/Fe] = 0、0.2、0.4 的等年龄线加权以匹配每颗星的 α 增丰。年龄误差的中位数为 7.5%；分析只用相对年龄误差低于 15% 的星。星表公开在 VizieR（J/other/Nat/603.599）。

#### 1.3 一步一步：作者如何从数据走到结论

1. **年龄–金属丰度平面在分开之前很杂乱。** 把全部恒星按年龄与 [Fe/H] 作图，分布很复杂。XR22 用既不是年龄也不是 [Fe/H] 的量分开样本（式 1）：J_φ > 1500 kpc km/s **且** [α/Fe] 低（[Fe/H] < −0.5 时低于 0.16，否则低于 −0.16[Fe/H] + 0.08）的星为"晚期"（薄盘），其余为"早期"。
2. **两个区间，在 8 Gyr 处分开。** 晚期的星几乎都年轻于约 8 Gyr，在年龄–[Fe/H] 图上呈"V 形"（由径向迁移（radial migration）解释）；早期的星几乎都更老。摘要说这个平面"splits into two almost disjoint parts, separated at 8 Gyr"。
3. **早期包含两条序列。** 贫金属序列（−2.5 < [Fe/H] < −1）是晕；富金属序列（[Fe/H] ≳ −1）是老的高 α（厚）盘。以 J_φ = 500 kpc km/s 分开早期星就能把它们分开（图 3）。
4. **老盘约 13 Gyr 前开始形成。** 对早期中 J_φ > 500、−1.05 < [Fe/H] < −0.95 的星（"presumably the oldest thick disk stars"），年龄直方图的高斯拟合给出均值 13.03 Gyr、宽度 1.81 Gyr（扩展数据图 1）。宇宙年龄 13.8 Gyr，所以这是"大爆炸之后仅 0.8 Gyr"。
5. **5–6 Gyr 的持续增丰，且序列很紧。** 沿老盘序列，[Fe/H] 从 13 Gyr 时的约 −1 升到约 7 Gyr 时的 +0.5。一个模型假设给定 [Fe/H] 时年龄是围绕直线 τ̄0 + a·[Fe/H]（拟合值 τ̄0 = 9.38 Gyr、a = −3.8 Gyr/dex）的高斯，并按每颗星的年龄误差与本征弥散（intrinsic scatter）σ_int 展宽；它给出 σ_int = 0.82 ± 0.01 Gyr，XR22 称之为上限。结合斜率，同一时间诞生的恒星的 [Fe/H] 弥散小于 0.22 dex：形成恒星的气体混合得很好。
6. **GSE 并合与恒星形成峰。** 角动量低但具有老盘化学的早期星（被并合加热的"溅出"盘星）只出现在约 11 Gyr 以上；老盘的恒星形成率（经体积改正后）在约 11.2 Gyr 达到峰值。XR22 由此认为 GSE 并合约在 11 Gyr 前基本完成。
7. **同一金属丰度下盘比晕老。** 在 [Fe/H] ≈ −1，老盘序列比晕序列老约 2 Gyr（"Z 形"）。

#### 1.4 结论与把握程度

摘要：老盘"started 13 Gyr ago, only 0.8 Gyr after the Big Bang"；"Most of these stars formed 11 Gyr ago, when the Gaia-Sausage-Enceladus satellite merged with our Galaxy"；此后 5–6 Gyr 银河系持续增丰，金属丰度增加了 10 倍。

论文自己讨论的注意事项（方法部分、扩展数据）：

- **绝对年龄标尺。** 在太阳 α 配比下，MIST 等年龄线给出的年龄比 YY 老约 0.5 Gyr；忽略 α 增丰会把老星的年龄高估至多 2 Gyr（XR22 考虑了 α 增丰）。没有先验强制年龄低于 13.8 Gyr；XR22 指出年龄"are consistent with the age of the universe at the old end"。
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
 该箱是最老的厚盘星 (mod_bin) ───────────┤
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
- `gap_scale`（GAP，我们补上的）：这种相容性确立了 13 Gyr 处的绝对标尺，误差小于约 0.5 Gyr。

*Lean 的发现。* 从 `obs_scale` 到准确的标尺这一步不在论文中，也不是标准知识。与 13.8 Gyr 相容只排除了老得太多的标尺；向任一方向偏几个 0.1 Gyr 的标尺同样相容，而 XR22 自己与 MIST 的比较就差 0.5 Gyr；后来的重新分析得到的年龄年轻 12.9%（在 13 Gyr 处约 1.7 Gyr；Chen, Sun & Ye 2025）。"大爆炸之后 0.8 Gyr"是两个数之差（13.8 − 13.0），其不确定度与年龄标尺一样大。

#### 2.2 环节 B · 从平均年龄到起点

*概述。* 13 Gyr 是对早期中 J_φ > 500、一个很窄的金属丰度箱（−1.05 到 −0.95）的星拟合高斯所得的均值。拟合宽度为 1.81 Gyr，大于这个年龄上典型的年龄误差（约 1 Gyr），所以该箱跨越数 Gyr 的真实年龄，或含有误差更大的星，或两者兼有。

*前提。*
- `mod_bin`（MOD，论文明说，"presumably the oldest thick disk stars"；保留措辞被编码为断言）。
- `stat_mean`（STAT，论文明说）：高斯均值为 13 Gyr（编码为 130 个 0.1 Gyr）。
- `lit_universe`（LIT，标准知识：Planck 2018，arXiv:1807.06209）：宇宙年龄 13.8 Gyr。
- `gap_onset`（GAP，我们补上的）：该箱中幸存的本地恒星的平均年龄标定了盘开始形成的时间。

*Lean 的发现。* `gap_onset` 承载三个没写出的步骤：(i) 均值不是起点；如果盘在 13 Gyr 前开始形成，该箱一半的星更年轻，所以均值标定的是该箱的典型星，只有当该箱只取样了第一次形成时，"起点"才等于均值；(ii) 今天在太阳附近几 kpc 内看到的星是幸存者，其中一些向外或向内迁移过，它们的年龄描述的是恒星现在在哪里，而不是盘最先在哪里形成；(iii) 在 [Fe/H] ≈ −1，J_φ > 500 的截断可能混入晕星（XR22 扩展数据图 2 显示这个金属丰度范围有低 J_φ 的尾巴），它们在这个金属丰度下约*年轻* 2 Gyr，会把均值拉低，而其他成分的老贫金属星又可能把它拉高。

#### 2.3 其他结论（只讨论，不编码）

- **8 Gyr 分界。** 分群用了与年龄相关的 [α/Fe]，所以"晚期老星少、早期年轻星少"部分是化学截断的结果。要说明*年龄–金属丰度平面本身*分成两个几乎不相交的部分，需要不用分群、直接检验密度。这是我们的 R1。
- **0.82 Gyr 的本征弥散。** XR22 的模型只把年龄误差按平方和加入。年龄与 [Fe/H] 的误差相关（年龄拟合用到 [Fe/H]），而"老的高 α 序列"（其图 2 的 e 面板）的样本定义会影响结果：给定 [Fe/H] 时 [α/Fe] 与年龄相关，按 [α/Fe] 截断会削去年轻一侧、降低 σ_int。这是我们的 R3/R4。
- **11 Gyr 与 GSE。** 11.2 Gyr 的峰需要选择效应的体积改正，公开星表没有它；我们只能描述，不能检验。

#### 2.4 Lean 检查发现的问题

1. **最重要的结论：`explicit_insufficient`，有两个缺口。** 起点结论需要准确的绝对年龄标尺（`gap_scale`），并把一个箱的平均年龄读作盘开始形成的时间（`gap_onset`）。没有标准知识能补上其中任何一个。
2. **排序。** `gap_onset` 最重要：它是论文没有讨论的建模选择，而该箱的拟合宽度（1.8 Gyr）大于到大爆炸的 0.8 Gyr 余量。`gap_scale` 是已知的等年龄线系统误差（YY 与 MIST 差 0.5 Gyr）。
3. **在本编码下七个前提都是必要的**，没有多余的。
4. **`stated_insufficient`** 也成立：宇宙年龄只是引用，两个缺口没有写出。
5. **相容性**（`consistent`）在这里是弱检查：没有否定形式的前提。
6. **局限：** Lean 检查的是在我们的编码下论证的逻辑结构，不检查每个前提内部的恒星物理。

### 第三部分 · 本项目可检验或探索的环节

星表（VizieR J/other/Nat/603.599/table1，247,104 行）经受守卫的 `ctx.http` 通道从 CfA 的 VizieR 镜像取一次（本机连不上 CDS 的 TAP 主机），只取所需的列（Id、Age、e_Age、[Fe/H]、e_[Fe/H]、[alpha/Fe]、e_[alpha/Fe]、JPHI、MKcomb）：5 行试取实测每行 65 字节，合计约 16 MB。设计见 [`design/019-plan_*`](https://github.com/sudoghut/astrolab/blob/main/design/019-plan_m05-thick-disc-early-formation-subgiant-age-metallicity-sequence.md)；判决规则在完整取数之前冻结于研究 README 第 2–4 节。所有年龄拟合用同一个观测模型（M0）：潜在年龄在 YY 网格 [0, 20] Gyr 上，每颗星的测量年龄以真实年龄为中心、宽度为其 e_Age 的高斯并截断到网格，在 15% 精度的样本 S15 上用以入选为条件的似然。

| 环节 / 结论 | 能否检验或探索 | 怎么做 | 数据（大小） | 判据 | 结果 |
|---|---|---|---|---|---|
| 环节 B：13 Gyr 的起点（R2） | 现在可检验 | 在 XR22 扩展数据图 1 的选择（早期、J_φ > 500、−1.05 < [Fe/H] < −0.95）中对观测年龄拟合高斯；另报告去卷积的均值（M0）、年龄超过 13.8 Gyr 与靠近 20 Gyr 网格边缘的比例，以及对 J_φ 截断与误差截断的敏感度 | 星表（16 MB） | 观测年龄的高斯均值在 12.5–13.5 Gyr 即复现（对取整的"13 Gyr"的容差） | 待定 |
| 环节 A：绝对标尺（`gap_scale`） | 可探索（不能判决） | 由文献幅度构成的包络：MIST +0.5 Gyr，[α/Fe] 误差与 LAMOST–APOGEE 的 α 偏移经 XR22 的年龄–α 敏感度传播，LAMOST [Fe/H]/Teff 偏移，视差零点 | – | 无，只作探索 | 待定 |
| 8 Gyr 分界（R1） | 现在可检验 | 不用化学分群：在 0.2 dex 的 [Fe/H] 箱中，用 M0 去卷积的年龄密度（高斯混合，K = 1–4 按 BIC），数众数并测量谷深；零分布由单峰偏斜正态拟合模拟标定；年轻一侧上缘与 8 Gyr 比较 | 星表 | "几乎不相交"的谷深阈值在预注册中写定，假阳性率 5% | 待定 |
| 老盘序列：斜率、5–6 Gyr 跨度、σ_int（R3/R4） | 现在可检验 | 在 M0 中、对高 α 且 J_φ > 500 的样本拟合 XR22 的线性加弥散模型（σ_sel，复现 XR22 的数字）；不加 α 截断、带背景分量的混合模型判定本征弥散；含 [Fe/H] 误差的版本作区间；两个方向的误差标尺检查 | 星表 | σ_sel 与 0.82 Gyr 比较（规则在核实 XR22 的估计量后写定）；跨度与 5–6 Gyr 比较 | 待定 |
| 与 Miglio et al. 2021 的张力（R7） | 可探索（有限定的比较） | 高 α 盘去卷积的总年龄跨度：中心 95% 宽度与任一 1.5 Gyr 窗口内的最大比例，分别用 XR22 的样本与类 APOGEE 的高 α 截断 | 星表 | 无，跨示踪体的比较 | 待定 |
| [Fe/H] ≈ −1 处晕与盘的偏移（R5） | 可探索（只作图） | 按 J_φ 分面的年龄–[Fe/H] 密度 | 星表 | 无 | 待定 |
| 11 Gyr / GSE（R6） | 可描述，不能检验 | 低 J_φ 老盘星年龄的 5% 与 10% 分位数；未做体积改正的年龄峰 | 星表 | 无，体积改正未公开 | 待定 |
| `gap_onset` 本身（幸存者、迁移） | 不在范围内 | 需要化学演化与迁移模型 | – | – | – |

对话探索：研究实现后，`python -m astrolab explore 010 --tag <主题> --set 键=值` 可用改变的参数（例如 J_φ 截断、误差截断或高 α 阈值）重跑任一拟合，不影响正式结果；见研究 README 第 8 节。

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

- 2026-11-15：第一版：第一至第三部分（预注册的来源；计划 `design/019-plan_*`）。

### 来源

- Xiang & Rix 2022，Nature 603, 599，arXiv:2203.12110（被研究的论文；引文据 arXiv v1 PDF）。
- Miglio 等 2021，A&A 645, A85，arXiv:2004.14806（α 增丰盘的星震学年龄）。
- Montalbán 等 2021，Nature Astronomy，arXiv:2006.01783；Queiroz 等 2023，A&A 673, A155，arXiv:2303.09926；Gallart 等 2024，A&A 687, A168，arXiv:2402.09399。
- Chen, Sun & Ye 2025，arXiv:2510.10092；Shariat, El-Badry & Bhattacharjee 2025，OJAp，arXiv:2510.08675（亚巨星年龄标尺与误差）。
- Feltzing, Feuillet & Bensby 2026，arXiv:2605.20959；Lu 等 2026，arXiv:2607.02940。
- Planck Collaboration 2020，A&A 641, A6，arXiv:1807.06209（宇宙年龄）。
