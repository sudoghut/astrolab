# Galaxies at z ≈ 14: too many, too bright, too early?

[English](#english) · [中文](#中文)

*Paper(s): Naidu et al. 2026, OJAp 9, arXiv:2505.11263 (main paper, "N26"); Carniani et al. 2024, Nature 633, 318, arXiv:2405.18485 ("C24"); Harikane et al. 2025, ApJ 980, 138, arXiv:2406.18352 ("H25"); Shen et al. 2023, MNRAS 525, 3254, arXiv:2305.05679 ("S23"). Study:
[`studies/006-m08-z14-galaxies-number-density`](https://github.com/sudoghut/astrolab/tree/main/studies/006-m08-z14-galaxies-number-density).
Status: reproduced. Last updated: 2026-11-15 (see the
changelog at the end). The source of this page lives in the main repository at
[`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki); edit it there.*

*中文标题：z ≈ 14 的星系：太多、太亮、太早？状态：已复现。论文：Naidu 等 2026, OJAp 9, arXiv:2505.11263（主论文，"N26"）；Carniani 等 2024, Nature 633, 318, arXiv:2405.18485（"C24"）；Harikane 等 2025, ApJ 980, 138, arXiv:2406.18352（"H25"）；Shen 等 2023, MNRAS 525, 3254, arXiv:2305.05679（"S23"）。研究：[`studies/006-m08-z14-galaxies-number-density`](https://github.com/sudoghut/astrolab/tree/main/studies/006-m08-z14-galaxies-number-density)。最后更新：2026-11-15（见文末"研究进展"）。本页源文件在主仓库的 [`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki) 中，请在那里修改。*

---

## English

### Part 1 · The paper in plain language

#### 1.1 The question and why it matters

Light from a galaxy at redshift z ≈ 14 left it when the Universe was about 280 million years old (N26; the exact age depends on the cosmology),
2% of its present age. Before the James Webb Space Telescope (JWST), models of galaxy formation
predicted that galaxies this early would be rare and faint: dark-matter halos massive enough to
host a bright galaxy had barely had time to form. JWST found many more bright galaxies at
z ≳ 10 than expected. Whether that means new physics (in cosmology or star formation) or only
that young galaxies are burstier, less dusty or more efficient at forming stars than assumed is
one of the main open questions of high-redshift astronomy.

Two galaxies anchor the very top of the redshift range. JADES-GS-z14-0 (C24) lies at
z_spec = 14.32 (refined to 14.18 from the ALMA [O III] 88 µm line; Schouws et al. 2024, Carniani
et al. 2025) and has absolute UV magnitude M_UV = −20.81. MoM-z14 (N26), found in the "Mirage or
Miracle" survey, lies at z_spec = 14.44 ± 0.02 with M_UV = −20.23 ± 0.06. Both were confirmed by
spectra, not only by colours. N26 asks how common such galaxies are and how that compares with
what was expected before JWST.

#### 1.2 The data

A galaxy's *number density* in a brightness bin is the number of galaxies divided by the comoving
volume searched and by the width of the bin in magnitudes: φ = N / (V Δm), in Mpc⁻³ mag⁻¹. The
*UV luminosity function* (UV LF) is φ as a function of M_UV.

N26 counts galaxies with −21 < M_UV < −20 at z = 14–15. In the area imaged by the PRIMER and JOF
surveys, 136 arcmin² (PRIMER-COSMOS) + 243 (PRIMER-UDS) + 9 (JOF) = 388 arcmin², it assumes
MoM-z14 and JADES-GS-z14-0 are the only such sources. The comoving volume between z = 14 and 15
over that area is 462,648 Mpc³ (N26 §4.1; Planck 2018 cosmology). These are the fields in which
the two galaxies were found.

#### 1.3 Step by step: how the authors got from data to conclusion

**(a) The number density.** φ = 2 / (462,648 Mpc³ × 1 mag) = 4.32 × 10⁻⁶ Mpc⁻³ mag⁻¹, i.e.
log φ = −5.36. N26 quotes −5.36 (+0.37/−0.45). Those error bars are exactly the 84% one-sided
Poisson limits for two counts (Gehrels 1986: 0.708 to 4.64 sources), although N26 does not name
the method. They include neither cosmic variance nor any completeness correction. N26 notes that
this value agrees well with photometric luminosity functions at z ≈ 14–15.

**(b) The pre-JWST baseline.** "To represent the pre-JWST theoretical consensus", N26 constructs a
ΛCDM UV LF in the framework of S23: halos grow at the rate dark-matter accretion sets, a
literature-averaged fraction of the inflowing gas forms stars (the star-formation efficiency, SFE),
the UV luminosity follows from the star-formation rate with a Chabrier initial mass function (IMF),
and the scatter of galaxies around the mean relation (σ_UV) is low.

**(c) The comparison.** In the same bin and area this LF predicts about 182 times fewer galaxies
(182, +329/−105): about 2.4 × 10⁻⁸ Mpc⁻³ mag⁻¹. N26: "Such an LF underestimates the incidence
of observed sources by ≈200×" and "is disfavored at high confidence". The interval on 182 presumably
comes from the Poisson uncertainty of the observed count (N26 does not say; it mirrors the interval on φ, with the signs
swapped: +0.45/−0.37 dex against +0.37/−0.45 dex, which we flag rather than resolve).

*Back of the envelope (our reading; N26 gives no number for "high confidence").* Over the declared
area the expected number of galaxies under the baseline is 2/182 ≈ 0.011. The Poisson probability
of seeing two or more is then about 0.011²/2 ≈ 6 × 10⁻⁵. Using the lower end of the ratio
interval (77×) instead would count the Poisson uncertainty of the observed count twice, since the
test already treats the count as data.

**(d) What would fix it.** N26 notes that the σ_UV needed to match the z ≈ 14–15 LF is ≈ 1.5–2 mag,
against ≈ 0.7 mag inferred out to z ≈ 9 from galaxy clustering; S23 found that σ_UV ≈ 0.75 mag
matches z ≈ 9 but ≈ 2.0 (2.5) mag is needed at z ≈ 12 (16). Other options are a higher SFE, a
top-heavy IMF, an AGN contribution, or new cosmology.

#### 1.4 What they conclude, and how sure they are

- **Detection**: two spectroscopically confirmed galaxies at z = 14–15 (established).
- **Overabundance**: the constructed pre-JWST LF underestimates the sources by ≈ 200× and "is
  disfavored at high confidence" (§4.1); the Summary speaks of a ">100× over-abundance". The factor
  rests on two galaxies.
- **Interpretation**: the new generation of models built after JWST "is very much required".

For the overabundance to be wrong, one of these would have to fail: the two fields would have to
be unusually rich (cosmic variance: rare galaxies at z ≈ 14 sit in rare, strongly clustered
halos, and N26 does not discuss it); the declared area would have to understate the effective
search (if comparable area with spectroscopic follow-up and no detection belongs in the census,
the observed density falls and the expected count rises; about 1.8 times more area already moves
the Poisson tail above 2 × 10⁻⁴); or the constructed baseline would have to underpredict what
pre-JWST models really expected. More undetected galaxies within the declared area would only
strengthen the conclusion.

### Part 2 · The logic of the argument

#### 2.0 Map of the argument

A. At least two confirmed sources in the bin and declared area → B. the constructed pre-JWST LF
predicts ≈ 182× fewer there → C. the Poisson tail probability of ≥ 2 sources is tiny → D. [gap]
the counts are Poisson about the model mean (no cosmic-variance excess) and E. [gap] the declared
area is the full effective search → F. [gap] a decision rule maps the tail probability to "high
confidence" ⇒ that LF is disfavored at high confidence.

How we check it: the argument is written in Lean 4
([`studies/006-m08-z14-galaxies-number-density/argument/Argument.lean`](https://github.com/sudoghut/astrolab/blob/main/studies/006-m08-z14-galaxies-number-density/argument/Argument.lean)).
Each premise is one constructor of `Field` (no axioms), labelled with its kind and its
provenance:

| Tag | Kind of premise |
|---|---|
| `OBS` | observation or measurement (with table / figure) |
| `MOD` | modelling assumption |
| `STAT` | statistical inference (significance, model comparison) |
| `NUM` | numerical result, re-computed by this repo's `run.py` |
| `LIT` | result taken from other literature |
| `GAP` | premise the inference needs that neither the paper nor standard knowledge supplies |

Provenance: `[stated <arXiv id>: "quote"]` (the paper says it, quoted), `[implied]` (standard
knowledge the paper relies on without writing it out, with a source), `[reconstructed]` (our
addition; exactly the `GAP` premises).

What Lean checks: that the conclusion follows from these premises (`final`) and is not trivially
true (`final_nontrivial`); that the premises can hold together (`consistent`); that no single
premise gives the conclusion alone (`alone_insufficient`); for each premise, whether it is needed
(a countermodel without it) or redundant; and whether the premises the paper actually states are
enough (`stated_*`), and whether they are enough once standard knowledge is added (`explicit_*`;
`explicit_insufficient` means a real gap). What Lean does not check: the physics inside
each premise; that is what parts 1 and 3 and the study are for.

Scope: the conclusion encoded is the statistical sentence of §4.1, whose grammatical subject is
"Such an LF", the pre-JWST LF N26 constructs. Whether that LF stands for "the pre-JWST consensus"
is N26's stated modelling choice ("To represent the pre-JWST theoretical consensus, we construct a
ΛCDM UV LF"); that step is discussed in 2.3, not encoded. N26's assumption that the two sources are
the only ones in the bin enters only as "at least two": further sources within the declared area
would strengthen the conclusion. The opposite direction runs through the area, and is a gap.

#### 2.1 Stage A · The counts

**Overview.** The observation is a lower bound on the count in the declared area.

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `obs_count`: at least two confirmed sources at z = 14–15, −21 < M_UV < −20 | OBS | stated 2505.11263: "we assume MoM-z14 and JADES-GS-z14-0 are the only −21<MUV<−20 sources" (N26's counting assumption for the LF estimate; we keep only its observational part, at least two confirmed) | §4.1 (confirmations: N26 §3, C24) |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| One of the two is a low-redshift interloper | `obs_count` (spectroscopic redshifts) | yes (spectra; C24, N26) |

**Critique.** Solid: both redshifts are spectroscopic.

#### 2.2 Stage B · The comparison and its significance

**Overview.** The baseline predicts far fewer sources over the declared area; a Poisson test turns
that into "disfavored".

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `stat_ratio`: observed / baseline ≥ 100 | STAT | stated 2505.11263: "Such an LF underestimates the incidence of observed sources by ≈200×" | §4.1 (182, +329/−105) |
| `mod_poisson`: with ≥ 2 observed and ratio ≥ 100, P(N ≥ n_obs \| expected n_obs/ratio) ≤ 2 × 10⁻⁴ | MOD | implied (Poisson mathematics; Gehrels 1986): 197 ppm at 2 and 100, smaller for larger values; 60 ppm at the stated 182 (computed in `results/r1.json`) | – |
| `gap_rule`: decision rule: with Poisson counts over the full effective search, a model with a tail probability ≤ 2 × 10⁻⁴ is disfavored at high confidence | GAP | reconstructed (N26 names no test, threshold or mapping from probability to confidence; the 2 × 10⁻⁴ cutoff is ours) | not in the paper |
| `gap_poisson`: the counts are Poisson about the model mean (no cosmic-variance excess) | GAP | reconstructed | not in the paper |
| `gap_area`: the declared area is the full effective search for this bin | GAP | reconstructed | not in the paper |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| The fields are overdense (cosmic variance) | `gap_poisson` | no: N26 does not discuss cosmic variance |
| Further comparable area without detections belongs in the census | `gap_area` | no |
| A two-count fluctuation | `mod_poisson`, `gap_rule` | no test given: "high confidence" signals a claimed inference but specifies neither the count model nor the test |

**Inference (Lean excerpt).**

```lean
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  have h1 : v.tail_ppm ≤ 200 := p .mod_poisson (p .obs_count) (p .stat_ratio)  -- Poisson tail
  exact p .gap_rule (p .obs_count) (p .stat_ratio) h1 (p .gap_poisson) (p .gap_area)  -- Sec. 4.1; GAP
```

**Critique.** The Poisson tail (≈ 6 × 10⁻⁵) is our reading of "high confidence". It treats the
expected count as exact and the counts as Poisson. Rare bright galaxies at z ≈ 14 live in rare halos
whose clustering makes field-to-field variance larger than Poisson (Somerville et al. 2004; Trenti &
Stiavelli 2008); H25 includes such a term in its error bars, N26 does not. The expected count
2/182 holds for the declared area, chosen where the detections were made. The margin is thin: the
tail reaches 2 × 10⁻⁴ at a ratio of about 100 (about 1.8 times more effective area) and the
one-sided 3σ level, 1.35 × 10⁻³, at a ratio of about 38 (about 4.8 times more area).

#### 2.3 From the constructed LF to "the pre-JWST consensus" (not encoded)

N26 builds one LF "to represent the pre-JWST theoretical consensus" and the abstract says the
density is ">100× larger … than pre-JWST consensus models". Whether one constructed LF stands for
the consensus is a modelling choice that N26 states openly; how much the factor 182 depends on it is
what our study explores (R2). We did not encode this step: with the quote's subject being "Such an
LF", the encoded conclusion is about that LF.

#### 2.4 What the Lean check found

1. **`explicit_insufficient`**: even with standard background added, the chain needs three gaps:
   a decision rule from tail probability to "high confidence" (`gap_rule`; N26 names no test or
   threshold), Poisson counts with no cosmic-variance excess (`gap_poisson`) and the declared area
   being the full effective search (`gap_area`). None is discussed in N26 §4.
2. **`stated_insufficient`**: the paper states the count and the ratio; the Poisson tail bound is
   unstated background (implied), the decision rule is not stated at all.
3. **Every premise is needed** (six `_needed` countermodels); none is redundant. The Poisson tail is
   tied to the count and the ratio by `mod_poisson` (after Codex review: a free-standing number
   would not have connected them).
4. **The census assumption cuts both ways**: through the count it can only strengthen the
   conclusion (further sources inside the declared area enter as "at least two"); through the area it can weaken it (more searched
   area without detections, `gap_area`).
5. **Consistency** holds but is weak here: every premise is positive.
6. **Limits.** Lean checks the logical structure under our encoding, not the physics inside each
   premise; with uninterpreted atoms "needed" means "used by this encoding".

```lean
inductive Field where
  | obs_count    -- OBS [stated 2505.11263]
  | stat_ratio   -- STAT [stated 2505.11263]
  | mod_poisson  -- MOD [implied] (Poisson tail bound)
  | gap_rule     -- GAP [reconstructed]
  | gap_poisson  -- GAP [reconstructed]
  | gap_area     -- GAP [reconstructed]

theorem explicit_insufficient : ¬ ∀ v, Explicit v → Conclusion v := fun h =>
  h ⟨2, 182, 60, False, False, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])
```

### Part 3 · What astrolab can test or explore

| Stage / claim | Can we test or explore it? | How | Data (size) | Decision criterion | Result |
|---|---|---|---|---|---|
| A: the number density (R1) | testable now | φ = N/(V Δm) with N = 2, V = 462,648 Mpc³; Gehrels 84% Poisson limits; recompute V from 388 arcmin² and z = 14–15 (Planck 2018) | N26 §4.1 numbers (~1 KB) | reproduced if log φ within 0.01 dex and each error within 0.05 dex; volume within 5% | **reproduced**: log φ = −5.364 (+0.365/−0.451); V = 460,463 Mpc³ (−0.5%) |
| B: Poisson tail under the baseline (checks the Lean `mod_poisson` bound numerically) | testable now | P(N ≥ 2 \| μ = 2/182), and at ratio 100 | – | tail at 182 and at 100 both ≤ 200 ppm (reported as `p_tail_n26_ppm`, `p_tail_ratio100_ppm`) | 59.9 ppm at 182, 197.4 ppm at 100: bound holds |
| B: an independent constant-SFE prediction (R2) | testable now (comparison, not a reproduction of N26's baseline) | Eisenstein–Hu P(k) → Sheth–Tormen halo mass function; SFR = ε(M_h) f_b Ṁ_h (Fakhouri et al. 2010); ε calibrated at z ≈ 8 by deconvolved abundance matching (σ_cal = 0.7 mag) and frozen; predict φ at z = 14–15 | pre-JWST z ≈ 8 LF parameters (paper table, ~1 KB) | φ_model(ours)/φ_model(N26 ≈ 2.4 × 10⁻⁸) within 1/3–3: "same order"; verdict conditional on the fiducial model, with robustness over a pre-declared variant grid | **higher**: 9.4× N26's baseline (fiducial); **calibration-dependent** (61 higher, 11 same order of 72; 2.5–37×) |
| D: the σ_UV needed (R3) | testable now | with the median relation fixed, solve φ_model(σ) = φ_obs (and its Poisson limits) | same | central σ reported; interval overlaps N26's ≈ 1.5–2 mag: "consistent"; conditional on R2 | **consistent with N26**: 1.38 mag (1.15–1.57); **calibration-dependent** (38 consistent, 34 different; 1.07–1.60 mag) |
| H25's z ~ 14 point (R4) | context only | H25's z ~ 14 bin contains only GS-z14-0 (shared with N26) and includes cosmic variance | H25 Table 2 | none (background) | H25 is 8.6× φ_obs (shared object, ≈ 39× smaller area) |
| Model ingredients (R5) | explorable (not decisive) | halo mass function, accretion fit, calibration redshift, σ_cal, ε extrapolation, dust, completeness c | same | none - exploration only, see README §8 | σ_cal and the ε extrapolation drive the variant spread (see What we found) |
| D: cosmic variance (`gap_poisson`) | explorable (not decisive) | halo-bias estimate of the field-to-field variance for two counts | same | none - exploration only | not yet explored |
| E: effective area (`gap_area`) | explorable (not decisive) | tail probability as a function of the effective area (ratio): crosses 2 × 10⁻⁴ at ≈ 1.8× (ratio ≈ 99) and 1.35 × 10⁻³ at ≈ 4.8× (ratio ≈ 38) the declared area (these are properties of the Poisson tail, reported for orientation, not decision thresholds) | – | none - exploration only | not yet explored |
| The baseline represents the consensus (2.3) | out of scope as a test | would need the pre-JWST model ensemble | – | – | – |

#### What we found (2026-11-15)

The number density follows from the two sources and N26's volume: log φ = −5.364 (+0.365/−0.451)
with Gehrels Poisson limits, and the volume recomputed from 388 arcmin² in Planck 2018 is within
0.5%. Under N26's baseline the Poisson probability of two or more sources is 6 × 10⁻⁵ (2 × 10⁻⁴ at a
ratio of 100), so the bound used in the Lean argument holds.

An independent constant star-formation-efficiency model, calibrated on the pre-JWST z ≈ 8 LF of
Bouwens et al. 2021 and frozen, predicts φ = 2.2 × 10⁻⁷ Mpc⁻³ mag⁻¹ in the same bin: 9.4 times N26's
baseline (the observed density is then about 19 times this prediction, and two sources have a
Poisson probability of about 0.5%). Across 72 pre-declared variants the factor ranges from 2.5 to 37
(61 "higher", 11 "same order"), so the verdict is calibration-dependent. The largest effects are the
scatter assumed at calibration and how the efficiency is extended to small halos. With the median
relation fixed, the scatter that reproduces the observed density is σ_UV ≈ 1.4 mag (1.15–1.57 within
the Poisson range; 1.07–1.60 across variants): at the low end of, or just below, N26's 1.5–2 mag,
and above the ≈ 0.7 mag inferred to z ≈ 9. The three gaps of the argument (decision rule, cosmic
variance, effective area) are untouched by these numbers.

Results: [`r1.json`](https://github.com/sudoghut/astrolab/blob/main/studies/006-m08-z14-galaxies-number-density/results/r1.json), [`r2.json`](https://github.com/sudoghut/astrolab/blob/main/studies/006-m08-z14-galaxies-number-density/results/r2.json), [`r3.json`](https://github.com/sudoghut/astrolab/blob/main/studies/006-m08-z14-galaxies-number-density/results/r3.json),
[`variants.json`](https://github.com/sudoghut/astrolab/blob/main/studies/006-m08-z14-galaxies-number-density/results/variants.json). The interactive page runs locally with `python -m astrolab serve`.

### Glossary

| Term | Meaning |
|---|---|
| redshift z | stretching of light by cosmic expansion; z ≈ 14 means about 280 Myr after the Big Bang |
| M_UV | absolute magnitude in the rest-frame ultraviolet (more negative = brighter) |
| UV luminosity function (UV LF) | number density of galaxies per magnitude as a function of M_UV |
| comoving volume | volume with the expansion of the Universe factored out |
| halo mass function | number density of dark-matter halos per unit mass |
| star-formation efficiency (SFE, ε) | fraction of the inflowing baryons that turn into stars |
| σ_UV | scatter, in magnitudes, of galaxies' UV brightness at fixed halo mass |
| abundance matching | linking galaxies to halos by matching their cumulative number densities |
| cosmic variance | extra field-to-field scatter in counts caused by large-scale structure |
| Poisson tail probability | the chance of seeing at least the observed count if counts are Poisson with a given mean |

### Open questions

- How much does cosmic variance for two rare objects in 388 arcmin² weaken "high confidence"?
- What is the full effective area searched for z = 14–15 sources at this depth with spectroscopic
  follow-up (for example the rest of JADES GOODS-S, CEERS, NGDEEP)?
- How strongly does the factor 182 depend on which pre-JWST model represents the consensus?

### Changelog

Newest first.

- 2026-11-15: results: Part 3 result column and "What we found" (R1 reproduced; R2 higher, calibration-dependent; R3 consistent, calibration-dependent).
- 2026-11-15: gate-2 review, round 2: the step from tail probability to "high confidence" is our decision rule, now GAP `gap_rule` (three gaps); age at z ≈ 14 aligned with N26 (280 Myr).
- 2026-11-15: gate-2 review: the Poisson tail is now a bound tied to the count and the ratio (`mod_poisson`), not a free-standing number; `obs_count` labelled as N26's counting assumption, observational part kept.
- 2026-11-15: gate-1 review: the area dependence made explicit (`gap_area`; the volume does not
  "cancel"); the encoded conclusion is about the LF N26 constructs (the step to "the consensus" is
  discussed, not encoded).
- 2026-11-15: first version: parts 1–3 (pre-registration source; plan `design/015-plan_*`).

### Sources

- Naidu et al. 2026, OJAp 9, arXiv:2505.11263 [V]
- Carniani et al. 2024, Nature 633, 318, arXiv:2405.18485 [V]
- Harikane et al. 2025, ApJ 980, 138, arXiv:2406.18352 [V]
- Shen et al. 2023, MNRAS 525, 3254, arXiv:2305.05679 [V]
- Schouws et al. 2024; Carniani et al. 2025 (ALMA [O III] redshift of JADES-GS-z14-0, z = 14.18; cited by N26)
- Gehrels 1986, ApJ 303, 336 (Poisson limits)
- Somerville et al. 2004, ApJ 600, L171; Trenti & Stiavelli 2008, ApJ 676, 767 (cosmic variance)
- Wasserman 2004, *All of Statistics*, ch. 10 (significance testing)
- Eisenstein & Hu 1998, ApJ 496, 605, arXiv:astro-ph/9709112; Sheth & Tormen 1999; Fakhouri, Ma & Boylan-Kolchin 2010, MNRAS 406, 2267

---

## 中文

### 第一部分 · 科普详解

#### 1.1 问题与意义

红移 z ≈ 14 的星系发出的光，离开时宇宙只有约 2.8 亿岁（N26；确切年龄取决于宇宙学参数），是现在年龄的 2%。在詹姆斯·韦布空间望远镜（JWST, James Webb Space Telescope）之前，星系形成模型预言这么早的星系会很稀少、很暗：足以容纳亮星系的暗物质晕（dark-matter halo）几乎还来不及形成。JWST 在 z ≳ 10 发现的亮星系比预期多得多。这究竟意味着新的物理（宇宙学或恒星形成），还是只说明年轻的星系比假设的更爆发、更少尘埃或恒星形成效率更高，是高红移天文学的主要开放问题之一。

两个星系位于红移范围的最顶端。JADES-GS-z14-0（C24）位于 z_spec = 14.32（后来由 ALMA 的 [O III] 88 µm 谱线精化为 14.18；Schouws 等 2024、Carniani 等 2025），紫外绝对星等 M_UV = −20.81。MoM-z14（N26）在"Mirage or Miracle"巡天中发现，位于 z_spec = 14.44 ± 0.02，M_UV = −20.23 ± 0.06。两者都由光谱而不只是颜色确认。N26 问这样的星系有多常见，以及与 JWST 之前的预期相比如何。

#### 1.2 数据

某个亮度区间内星系的*数密度*（number density），是星系个数除以搜索的共动体积（comoving volume）再除以以星等计的区间宽度：φ = N / (V Δm)，单位 Mpc⁻³ mag⁻¹。*紫外光度函数*（UV LF, UV luminosity function）就是 φ 随 M_UV 的变化。

N26 统计 z = 14–15、−21 < M_UV < −20 的星系。在 PRIMER 与 JOF 巡天成像的面积内，136 arcmin²（PRIMER-COSMOS）+ 243（PRIMER-UDS）+ 9（JOF）= 388 arcmin²，它假定 MoM-z14 与 JADES-GS-z14-0 是仅有的这类源。该面积上 z = 14 到 15 之间的共动体积为 462,648 Mpc³（N26 第 4.1 节；Planck 2018 宇宙学）。这些正是发现这两个星系的视场。

#### 1.3 一步一步：作者如何从数据走到结论

**(a) 数密度。** φ = 2 / (462,648 Mpc³ × 1 mag) = 4.32 × 10⁻⁶ Mpc⁻³ mag⁻¹，即 log φ = −5.36。N26 给出 −5.36（+0.37/−0.45）。这些误差恰好是两个计数的 84% 单侧泊松（Poisson）限（Gehrels 1986：0.708 到 4.64 个源），尽管 N26 没有写明方法。它们既不含宇宙方差（cosmic variance），也不含任何完备性改正。N26 指出这一数值与 z ≈ 14–15 的测光光度函数很一致。

**(b) JWST 之前的基准。** N26 写道"To represent the pre-JWST theoretical consensus"，按 S23 的框架构造了一个 ΛCDM 紫外光度函数：晕按暗物质吸积决定的速率增长，流入气体中按文献平均比例的部分形成恒星（恒星形成效率，SFE, star-formation efficiency），紫外光度由恒星形成率按 Chabrier 初始质量函数（IMF, initial mass function）换算，星系相对平均关系的弥散（σ_UV）较小。

**(c) 比较。** 在同一个箱与面积里，这个光度函数预言的星系约少 182 倍（182，+329/−105）：约 2.4 × 10⁻⁸ Mpc⁻³ mag⁻¹。N26："Such an LF underestimates the incidence of observed sources by ≈200×"，并且"is disfavored at high confidence"。182 的区间大概来自观测计数的泊松不确定性（N26 没有说明；它与 φ 的区间互为镜像、正负号对调：+0.45/−0.37 dex 对 +0.37/−0.45 dex，我们只指出而不解决这一点）。

*粗略估算（我们的解读；N26 没有给出"高置信度"的数值）。* 在所述面积上，基准模型下预期的星系个数是 2/182 ≈ 0.011。看到两个或更多的泊松概率约为 0.011²/2 ≈ 6 × 10⁻⁵。若改用比值区间的下端（77 倍），会把观测计数的泊松不确定性计算两次，因为检验已经把计数当作数据。

**(d) 什么能解释它。** N26 指出，要匹配 z ≈ 14–15 的光度函数所需的 σ_UV 约为 1.5–2 mag，而由星系成团性（clustering）推断到 z ≈ 9 的值约为 0.7 mag；S23 发现 σ_UV ≈ 0.75 mag 符合 z ≈ 9，但 z ≈ 12（16）需要约 2.0（2.5）mag。其他选项有更高的 SFE、头重型 IMF（top-heavy IMF）、活动星系核（AGN）贡献或新的宇宙学。

#### 1.4 结论与把握程度

- **探测**：两个光谱确认的 z = 14–15 星系（已确立）。
- **过多**：构造的 JWST 之前的光度函数把源的数目低估了约 200 倍，并且"is disfavored at high confidence"（第 4.1 节）；总结部分说">100× over-abundance"。这个倍数只基于两个星系。
- **解读**：JWST 之后建立的新一代模型"is very much required"。

过多的结论若要不成立，需要以下之一：两个视场异常富集（宇宙方差：z ≈ 14 的稀有星系位于稀有、强成团的晕中，而 N26 没有讨论它）；所述面积低估了实际的有效搜索（若有同等深度、做过光谱跟进而没有探测的面积应计入普查（census），观测数密度就会下降、预期计数就会上升；有效面积只要大约 1.8 倍，泊松尾概率就超过 2 × 10⁻⁴）；或者构造的基准低估了 JWST 之前的模型真正的预期。所述面积内若还有未探测到的星系，只会加强这一结论。

### 第二部分 · 论证逻辑

#### 2.0 论证地图

A. 箱与所述面积内至少有两个确认的源 → B. 构造的 JWST 之前的光度函数在该面积上预言约少 182 倍 → C. 看到 ≥ 2 个源的泊松尾概率极小 → D. [缺口] 计数相对模型平均值服从泊松分布（没有宇宙方差的额外弥散），且 E. [缺口] 所述面积就是完整的有效搜索 → F. [缺口] 一条判决规则把尾概率对应到"高置信度" ⇒ 该光度函数以高置信度被排除。

检查方法：论证写成 Lean 4（[`studies/006-m08-z14-galaxies-number-density/argument/Argument.lean`](https://github.com/sudoghut/astrolab/blob/main/studies/006-m08-z14-galaxies-number-density/argument/Argument.lean)）。每个前提是 `Field` 的一个构造子（不用公理 axiom），标注类型与出处性质：

| 标签 | 前提类型 |
|---|---|
| `OBS` | 观测或测量（注明表格、图） |
| `MOD` | 模型假设 |
| `STAT` | 统计推断（显著性、模型比较） |
| `NUM` | 数值结果，由本仓库 `run.py` 复核 |
| `LIT` | 引自其他文献的结论 |
| `GAP` | 推理需要、但论文和标准知识都没有提供的前提 |

出处性质：`[stated <arXiv 编号>: "引文"]`（论文明说，附原文）、`[implied]`（论文依赖但没写出的标准知识，注明来源）、`[reconstructed]`（我们补上的，恰好就是 `GAP` 前提）。

Lean 检查什么：结论能否由这些前提推出（`final`）且并非恒真（`final_nontrivial`）；前提能否同时成立（`consistent`）；单个前提不能单独推出结论（`alone_insufficient`）；每个前提是必要的（去掉它时的反例模型（countermodel））还是多余的；论文明说的前提是否足够（`stated_*`）；加上标准知识后是否足够（`explicit_*`，`explicit_insufficient` 即存在真正的缺口）。Lean 不检查每个前提内部的物理是否正确，那是第一、三部分和研究本身的任务。

编码范围：编码的结论是第 4.1 节的统计句，其语法主语是"Such an LF"，即 N26 构造的 JWST 之前的光度函数。该光度函数是否代表"JWST 之前的共识"，是 N26 明说的建模选择（"To represent the pre-JWST theoretical consensus, we construct a ΛCDM UV LF"）；这一步在 2.3 中讨论，没有编码。N26 关于这两个源是箱中仅有的源的假设只以"至少两个"进入：所述面积内若还有更多的源，只会加强结论。相反的方向经由面积起作用，是一个缺口。

#### 2.1 环节 A · 计数

**概述。** 观测是所述面积内计数的下界。

**前提。**

| 前提（Lean 构造子） | 标签 | 出处性质 | 论文出处 |
|---|---|---|---|
| `obs_count`：至少两个确认的 z = 14–15、−21 < M_UV < −20 的源 | OBS | stated 2505.11263："we assume MoM-z14 and JADES-GS-z14-0 are the only −21<MUV<−20 sources"（这是 N26 估计光度函数时的计数假设；我们只保留其观测部分：至少两个已确认） | 第 4.1 节（光谱确认：N26 第 3 节、C24） |

**其他解释（rival explanations）。**

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 其中一个是低红移的混入者（interloper） | `obs_count`（光谱红移） | 是（光谱；C24、N26） |

**评析。** 很可靠：两个红移都是光谱红移。

#### 2.2 环节 B · 比较及其显著性

**概述。** 基准在所述面积上预言的源少得多；泊松检验把它变成"被排除"。

**前提。**

| 前提（Lean 构造子） | 标签 | 出处性质 | 论文出处 |
|---|---|---|---|
| `stat_ratio`：观测 / 基准 ≥ 100 | STAT | stated 2505.11263："Such an LF underestimates the incidence of observed sources by ≈200×" | 第 4.1 节（182，+329/−105） |
| `mod_poisson`：观测 ≥ 2 且比值 ≥ 100 时，P(N ≥ n_obs \| 预期 n_obs/比值) ≤ 2 × 10⁻⁴ | MOD | implied（泊松数学；Gehrels 1986）：2 与 100 时为 197 ppm，数值更大时更小；按所述的 182 为 60 ppm（在 `results/r1.json` 中计算） | – |
| `gap_rule`：判决规则：在完整的有效搜索上计数服从泊松分布时，尾概率 ≤ 2 × 10⁻⁴ 的模型以高置信度被排除 | GAP | reconstructed（N26 没有给出检验、门槛或从概率到置信度的对应；2 × 10⁻⁴ 的门槛是我们定的；显著性检验（significance testing）一般见 Wasserman 2004，第 10 章） | 论文没有写 |
| `gap_poisson`：计数相对模型平均值服从泊松分布（没有宇宙方差的额外弥散） | GAP | reconstructed | 论文没有写 |
| `gap_area`：所述面积就是这一箱的完整有效搜索 | GAP | reconstructed | 论文没有写 |

**其他解释。**

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 视场过密（宇宙方差） | `gap_poisson` | 否：N26 没有讨论宇宙方差 |
| 还有同等条件、没有探测的面积应计入普查 | `gap_area` | 否 |
| 两个计数的涨落 | `mod_poisson`、`gap_rule` | 没有给出检验："高置信度"表明作者作了推断，但没有说明计数模型或检验方法 |

**推理（Lean 摘录）。**

```lean
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  have h1 : v.tail_ppm ≤ 200 := p .mod_poisson (p .obs_count) (p .stat_ratio)  -- Poisson tail
  exact p .gap_rule (p .obs_count) (p .stat_ratio) h1 (p .gap_poisson) (p .gap_area)  -- Sec. 4.1; GAP
```

**评析。** 泊松尾概率（约 6 × 10⁻⁵）是我们对"高置信度"的解读。它把预期计数当作精确值，并假定计数服从泊松分布。z ≈ 14 的稀有亮星系位于稀有晕中，这些晕的成团性使视场之间的弥散大于泊松（Somerville 等 2004；Trenti & Stiavelli 2008）；H25 的误差包含这一项，N26 没有。预期计数 2/182 只对所述面积成立，而该面积是在有探测的地方选的。余量很小：比值约 100（有效面积约 1.8 倍）时尾概率达到 2 × 10⁻⁴，比值约 38（约 4.8 倍面积）时达到单侧 3σ 的 1.35 × 10⁻³。

#### 2.3 从构造的光度函数到"JWST 之前的共识"（未编码）

N26 构造了一个光度函数"to represent the pre-JWST theoretical consensus"，摘要说数密度比"pre-JWST consensus models"大 100 倍以上。一个构造的光度函数是否代表共识，是 N26 公开写明的建模选择；182 倍在多大程度上取决于这一选择，是本研究要探讨的（R2）。我们没有编码这一步：引文的主语是"Such an LF"，所以编码的结论说的是这个光度函数。

#### 2.4 Lean 检查发现的问题

1. **`explicit_insufficient`**：即使加上标准背景知识，链条仍需要三个缺口：从尾概率到"高置信度"的判决规则（`gap_rule`；N26 没有给出检验或门槛）、计数服从泊松分布且没有宇宙方差的额外弥散（`gap_poisson`），以及所述面积就是完整的有效搜索（`gap_area`）。N26 第 4 节都没有讨论它们。
2. **`stated_insufficient`**：论文明说了计数与比值；泊松尾概率的界是没写出的背景知识（implied），判决规则则完全没有写出。
3. **每个前提都是必要的**（六个 `_needed` 反例模型），没有多余的前提。泊松尾概率经由 `mod_poisson` 与计数和比值相连（Codex 审查后改：单独的数值无法把它们连起来）。
4. **普查假设在两个方向上起作用**：经由计数，只会加强结论（所述面积内更多的源以"至少两个"进入）；经由面积，可能削弱结论（搜索了更多面积却没有探测，`gap_area`）。
5. **相容性**成立，但在这里分量很弱：所有前提都是肯定命题。
6. **局限。** Lean 检查的是在我们的编码下的逻辑结构，不检查每个前提内部的物理；原子命题不加解释时，"必要"指"本编码用到了它"。

```lean
inductive Field where
  | obs_count    -- OBS [stated 2505.11263]
  | stat_ratio   -- STAT [stated 2505.11263]
  | mod_poisson  -- MOD [implied] (Poisson tail bound)
  | gap_rule     -- GAP [reconstructed]
  | gap_poisson  -- GAP [reconstructed]
  | gap_area     -- GAP [reconstructed]

theorem explicit_insufficient : ¬ ∀ v, Explicit v → Conclusion v := fun h =>
  h ⟨2, 182, 60, False, False, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])
```

### 第三部分 · 本项目可检验或探索的环节

| 环节 / 结论 | 能否检验或探索 | 方法 | 数据（大小） | 判据 | 结果 |
|---|---|---|---|---|---|
| A：数密度（R1） | 现在可检验 | φ = N/(V Δm)，N = 2、V = 462,648 Mpc³；Gehrels 84% 泊松限；由 388 arcmin² 与 z = 14–15 复算 V（Planck 2018） | N26 第 4.1 节的数字（约 1 KB） | log φ 差 0.01 dex 以内、各误差差 0.05 dex 以内、体积差 5% 以内 → 复现 | **复现**：log φ = −5.364（+0.365/−0.451）；V = 460,463 Mpc³（−0.5%） |
| B：基准下的泊松尾概率（数值核对 Lean 的 `mod_poisson` 界） | 现在可检验 | P(N ≥ 2 \| μ = 2/182)，以及比值 100 时 | – | 182 与 100 时的尾概率都 ≤ 200 ppm（报告为 `p_tail_n26_ppm`、`p_tail_ratio100_ppm`） | 182 时 59.9 ppm、100 时 197.4 ppm：界成立 |
| B：独立的恒定 SFE 预言（R2） | 现在可检验（比较，不是复现 N26 的基准） | Eisenstein–Hu 功率谱 → Sheth–Tormen 晕质量函数；SFR = ε(M_h) f_b Ṁ_h（Fakhouri 等 2010）；ε 在 z ≈ 8 用去卷积的丰度匹配（abundance matching，σ_cal = 0.7 mag）校准后冻结；预言 z = 14–15 的 φ | JWST 之前 z ≈ 8 光度函数的参数（论文表格，约 1 KB） | φ_model(本研究)/φ_model(N26 ≈ 2.4 × 10⁻⁸) 在 1/3–3 之间："同一量级"；判定以基准组合为条件，并报告在预先列出的变体网格上是否稳健 | **更高**：基准组合为 N26 基准的 9.4 倍；**依赖校准**（72 个中 61 个更高、11 个同一量级；2.5–37 倍） |
| D：所需的 σ_UV（R3） | 现在可检验 | 固定中位数关系，解 φ_model(σ) = φ_obs（及其泊松限） | 同上 | 报告中心值；区间与 N26 的 ≈ 1.5–2 mag 重叠："一致"；以 R2 为前提 | **与 N26 一致**：1.38 mag（1.15–1.57）；**依赖校准**（38 个一致、34 个不同；1.07–1.60 mag） |
| H25 的 z ~ 14 点（R4） | 只作背景 | H25 的 z ~ 14 箱只含 GS-z14-0（与 N26 共用），误差含宇宙方差 | H25 表 2 | 无（背景） | H25 为 φ_obs 的 8.6 倍（共用天体，面积约小 39 倍） |
| 模型组成（R5） | 可探索（不能判决） | 晕质量函数、吸积拟合式、校准红移、σ_cal、ε 外推、尘埃、完备性 c | 同上 | 无——仅供探索，见 README 第 8 节 | σ_cal 与 ε 外推方式决定变体之间的差别（见"我们的发现"） |
| D：宇宙方差（`gap_poisson`） | 可探索（不能判决） | 用晕偏置（halo bias）估计两个计数的视场间弥散 | 同上 | 无——仅供探索 | 尚未探索 |
| E：有效面积（`gap_area`） | 可探索（不能判决） | 尾概率随有效面积（比值）的变化：约为所述面积的 1.8 倍（比值约 99）时越过 2 × 10⁻⁴，约 4.8 倍（比值约 38）时越过 1.35 × 10⁻³（这是泊松尾概率本身的性质，用于参照，不是判决门槛） | – | 无——仅供探索 | 尚未探索 |
| 基准代表共识（2.3） | 不在检验范围内 | 需要 JWST 之前的模型集合 | – | – | – |

#### 我们的发现（2026-11-15）

数密度由两个源与 N26 的体积得出：用 Gehrels 泊松限，log φ = −5.364（+0.365/−0.451）；由 388 arcmin² 在 Planck 2018 下复算的体积相差不到 0.5%。在 N26 的基准下，看到两个或更多源的泊松概率为 6 × 10⁻⁵（比值为 100 时为 2 × 10⁻⁴），所以 Lean 论证中用到的界成立。

一个独立的恒定恒星形成效率模型，用 Bouwens 等 2021 的 JWST 之前 z ≈ 8 光度函数校准后冻结，在同一箱中预言 φ = 2.2 × 10⁻⁷ Mpc⁻³ mag⁻¹：为 N26 基准的 9.4 倍（观测数密度约为这一预言的 19 倍，看到两个源的泊松概率约 0.5%）。在 72 个预先列出的变体中，这个倍数从 2.5 到 37（61 个"更高"、11 个"同一量级"），所以判定依赖校准。影响最大的是校准时假定的弥散，以及效率如何外推到小晕。固定中位数关系时，再现观测数密度所需的弥散为 σ_UV ≈ 1.4 mag（泊松范围内 1.15–1.57；各变体 1.07–1.60）：位于 N26 的 1.5–2 mag 的低端或略低，并高于推断到 z ≈ 9 的约 0.7 mag。论证的三个缺口（判决规则、宇宙方差、有效面积）不受这些数字影响。

结果：[`r1.json`](https://github.com/sudoghut/astrolab/blob/main/studies/006-m08-z14-galaxies-number-density/results/r1.json)、[`r2.json`](https://github.com/sudoghut/astrolab/blob/main/studies/006-m08-z14-galaxies-number-density/results/r2.json)、[`r3.json`](https://github.com/sudoghut/astrolab/blob/main/studies/006-m08-z14-galaxies-number-density/results/r3.json)、[`variants.json`](https://github.com/sudoghut/astrolab/blob/main/studies/006-m08-z14-galaxies-number-density/results/variants.json)。交互网页在本地用 `python -m astrolab serve` 打开。

### 术语表

| 术语 | 含义 |
|---|---|
| 红移（redshift）z | 宇宙膨胀对光的拉伸；z ≈ 14 约为大爆炸后 2.8 亿年 |
| M_UV | 静止系紫外的绝对星等（越负越亮） |
| 紫外光度函数（UV LF） | 每星等的星系数密度随 M_UV 的变化 |
| 共动体积（comoving volume） | 扣除宇宙膨胀后的体积 |
| 晕质量函数（halo mass function） | 单位质量的暗物质晕数密度 |
| 恒星形成效率（SFE, ε） | 流入的重子中转变为恒星的比例 |
| σ_UV | 在固定晕质量下，星系紫外亮度以星等计的弥散 |
| 丰度匹配（abundance matching） | 通过匹配累计数密度把星系与晕对应起来 |
| 宇宙方差（cosmic variance） | 大尺度结构造成的视场之间计数的额外弥散 |
| 泊松尾概率（Poisson tail probability） | 若计数服从给定平均值的泊松分布，看到至少观测计数的概率 |

### 开放问题

- 对 388 arcmin² 中的两个稀有天体，宇宙方差在多大程度上削弱"高置信度"？
- 在这一深度、做过光谱跟进的 z = 14–15 源的完整有效搜索面积是多少（例如 JADES GOODS-S 的其余部分、CEERS、NGDEEP）？
- 182 倍在多大程度上取决于用哪个 JWST 之前的模型代表共识？

### 研究进展

按时间倒序。

- 2026-11-15：结果：第三部分"结果"一列与"我们的发现"（R1 复现；R2 更高、依赖校准；R3 一致、依赖校准）。
- 2026-11-15：闸门 2 审查第 2 轮：从尾概率到"高置信度"的一步是我们定的判决规则，改为 GAP `gap_rule`（三个缺口）；z ≈ 14 的宇宙年龄按 N26 改为 2.8 亿年。
- 2026-11-15：闸门 2 审查：泊松尾概率改为与计数和比值相连的界（`mod_poisson`），不再是单独的数值；`obs_count` 注明是 N26 的计数假设，只保留观测部分。
- 2026-11-15：闸门 1 审查：写明面积的依赖（`gap_area`；体积并不"相消"）；编码的结论说的是 N26 构造的光度函数（到"共识"的一步只讨论、不编码）。
- 2026-11-15：第一版：第一至三部分（预注册的来源；计划 `design/015-plan_*`）。

### 来源

- 同英文部分。
