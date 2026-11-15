# Galaxies at z ≈ 14: too many, too bright, too early?

[English](#english) · [中文](#中文)

*Paper(s): Naidu et al. 2026, OJAp 9, arXiv:2505.11263 (main paper, "N26"); Carniani et al. 2024, Nature 633, 318, arXiv:2405.18485 ("C24"); Harikane et al. 2025, ApJ 980, 138, arXiv:2406.18352 ("H25"); Shen et al. 2023, MNRAS 525, 3254, arXiv:2305.05679 ("S23"). Study:
[`studies/006-m08-z14-galaxies-number-density`](https://github.com/sudoghut/astrolab/tree/main/studies/006-m08-z14-galaxies-number-density).
Status: planned. Last updated: 2026-11-15 (see the
changelog at the end). The source of this page lives in the main repository at
[`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki); edit it there.*

*中文标题：z ≈ 14 的星系：太多、太亮、太早？状态：计划中。论文：Naidu 等 2026, OJAp 9, arXiv:2505.11263（主论文，"N26"）；Carniani 等 2024, Nature 633, 318, arXiv:2405.18485（"C24"）；Harikane 等 2025, ApJ 980, 138, arXiv:2406.18352（"H25"）；Shen 等 2023, MNRAS 525, 3254, arXiv:2305.05679（"S23"）。研究：[`studies/006-m08-z14-galaxies-number-density`](https://github.com/sudoghut/astrolab/tree/main/studies/006-m08-z14-galaxies-number-density)。最后更新：2026-11-15（见文末"研究进展"）。本页源文件在主仓库的 [`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki) 中，请在那里修改。*

---

## English

### Part 1 · The paper in plain language

#### 1.1 The question and why it matters

Light from a galaxy at redshift z ≈ 14 left it when the Universe was about 290 million years old,
2% of its present age. Before the James Webb Space Telescope (JWST), models of galaxy formation
predicted that galaxies this early would be rare and faint: dark-matter halos massive enough to
host a bright galaxy had barely had time to form. JWST found many more bright galaxies at
z ≳ 10 than expected. Whether that means new physics (in cosmology or star formation) or only
that young galaxies are burstier, less dusty or more efficient at forming stars than assumed is
one of the main open questions of high-redshift astronomy.

Two galaxies anchor the very top of the redshift range. JADES-GS-z14-0 (C24) lies at
z_spec = 14.32 (later refined to 14.18 with ALMA) and has absolute UV magnitude M_UV = −20.81.
MoM-z14 (N26), found in the "Mirage or Miracle" survey, lies at z_spec = 14.44 ± 0.02 with
M_UV = −20.23 ± 0.06. Both were confirmed by spectra, not only by colours. N26 asks how common
such galaxies are and how that compares with what was expected before JWST.

#### 1.2 The data

A galaxy's *number density* in a brightness bin is the number of galaxies divided by the comoving
volume searched and by the width of the bin in magnitudes: φ = N / (V Δm), in Mpc⁻³ mag⁻¹. The
*UV luminosity function* (UV LF) is φ as a function of M_UV.

N26 counts galaxies with −21 < M_UV < −20 at z = 14–15. In the area imaged by the PRIMER and JOF
surveys, 136 arcmin² (PRIMER-COSMOS) + 243 (PRIMER-UDS) + 9 (JOF) = 388 arcmin², it assumes
MoM-z14 and JADES-GS-z14-0 are the only such sources. The comoving volume between z = 14 and 15
over that area is 462,648 Mpc³ (N26 §4.1; Planck 2018 cosmology).

#### 1.3 Step by step: how the authors got from data to conclusion

**(a) The number density.** φ = 2 / (462,648 Mpc³ × 1 mag) = 4.32 × 10⁻⁶ Mpc⁻³ mag⁻¹, i.e.
log φ = −5.36. N26 quotes −5.36 (+0.37/−0.45). Those error bars are exactly the 84% one-sided
Poisson limits for two counts (Gehrels 1986: 0.708 to 4.64 sources), although N26 does not name
the method. They include neither cosmic variance nor any completeness correction.

**(b) The pre-JWST baseline.** "To represent the pre-JWST theoretical consensus", N26 constructs a
ΛCDM UV LF in the framework of S23: halos grow at the rate dark-matter accretion sets, a
literature-averaged fraction of the inflowing gas forms stars (the star-formation efficiency, SFE),
the UV luminosity follows from the star-formation rate with a Chabrier initial mass function (IMF),
and the scatter of galaxies around the mean relation (σ_UV) is low.

**(c) The comparison.** In the same bin this LF predicts about 182 times fewer galaxies
(182, +329/−105): about 2.4 × 10⁻⁸ Mpc⁻³ mag⁻¹. N26: "Such an LF underestimates the incidence
of observed sources by ≈200×" and "is disfavored at high confidence".

*Back of the envelope.* The expected number of galaxies in the survey under the baseline is
2/182 ≈ 0.011 (the volume cancels). The Poisson probability of seeing two or more is then about
0.011²/2 ≈ 6 × 10⁻⁵, the "high confidence".

**(d) What would fix it.** N26 notes that the σ_UV needed to match the z ≈ 14–15 LF is ≈ 1.5–2 mag,
against ≈ 0.7 mag inferred out to z ≈ 9 from galaxy clustering; S23 found that σ_UV ≈ 0.75 mag
matches z ≈ 9 but ≈ 2.0 (2.5) mag is needed at z ≈ 12 (16). Other options are a higher SFE, a
top-heavy IMF, an AGN contribution, or new cosmology.

#### 1.4 What they conclude, and how sure they are

- **Detection**: two spectroscopically confirmed galaxies at z = 14–15 (established).
- **Overabundance**: φ is "> 100×" the pre-JWST consensus, and that LF "is disfavored at high
  confidence". The factor rests on two galaxies (+329/−105 on 182).
- **Interpretation**: the new generation of models built after JWST "is very much required".

For the overabundance to be wrong, one of these would have to fail: the two fields would have to
be unusually rich (cosmic variance: rare galaxies at z ≈ 14 sit in rare, strongly clustered
halos, and N26 does not discuss it); or the constructed baseline would have to underpredict what
pre-JWST models really expected. More undetected galaxies in the bin would only strengthen the
conclusion.

### Part 2 · The logic of the argument

#### 2.0 Map of the argument

A. At least two confirmed sources in the bin → B. the baseline LF predicts ≈ 182× fewer → C. the
Poisson tail probability of ≥ 2 sources is tiny → D. [gap] the counts are Poisson about the model
mean (no cosmic-variance excess) → E. so the baseline is disfavored → F. the baseline represents
the pre-JWST consensus ⇒ the pre-JWST consensus (so represented) is disfavored at high confidence.

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

Scope: the conclusion encoded is the statistical sentence of §4.1 ("is disfavored at high
confidence"), said of the constructed baseline and, through it, of the consensus it represents.
Not encoded: N26's assumption that the two sources are the only ones in the bin. More sources
would raise the count, so an incomplete census cannot weaken the conclusion; with the count
written as "at least two" the assumption is not needed.

#### 2.1 Stage A · The counts

**Overview.** The observation is a lower bound on the count in a known volume.

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `obs_count`: at least two confirmed sources at z = 14–15, −21 < M_UV < −20 | OBS | stated 2505.11263: "we assume MoM-z14 and JADES-GS-z14-0 are the only −21<MUV<−20 sources" | §4.1 |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| One of the two is a low-redshift interloper | `obs_count` (spectroscopic redshifts) | yes (spectra; C24, N26) |

**Critique.** Solid: both redshifts are spectroscopic. The census assumption ("the only")
matters for the value of φ, not for the direction of the conclusion.

#### 2.2 Stage B · The comparison and its significance

**Overview.** The baseline predicts far fewer sources; a Poisson test turns that into "disfavored".

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `stat_ratio`: observed / baseline ≥ 100 | STAT | stated 2505.11263: "Such an LF underestimates the incidence of observed sources by ≈200×" | §4.1 (182, +329/−105) |
| `num_tail`: P(N ≥ 2 \| expected 2/182) ≤ 2 × 10⁻⁴ | NUM | implied (Poisson statistics; Gehrels 1986); bound to `results/r1.json:p_tail_n26_ppm <= 200` | – |
| `mod_test`: a model with such a tail probability is disfavored at high confidence, provided the counts are Poisson | MOD | implied (significance testing; Wasserman 2004, ch. 10) | – |
| `gap_poisson`: the counts are Poisson about the model mean (no cosmic-variance excess) | GAP | reconstructed | not in the paper |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| The fields are overdense (cosmic variance) | `gap_poisson` | no: N26 does not discuss cosmic variance |
| A two-count fluctuation | `num_tail` | implicitly ("high confidence") |

**Inference (Lean excerpt).**

```lean
have h1 : v.ModelDisfavored :=
  p .mod_test (p .obs_count) (p .stat_ratio) (p .num_tail) (p .gap_poisson)  -- Sec. 4.1; GAP
```

**Critique.** The Poisson tail (≈ 6 × 10⁻⁵) is the "high confidence". It treats the expected
count as exact and the counts as Poisson. Rare bright galaxies at z ≈ 14 live in rare halos whose
clustering makes field-to-field variance larger than Poisson (Somerville et al. 2004; Trenti &
Stiavelli 2008); H25 includes such a term in its error bars, N26 does not. The tail probability
also does not depend on the survey volume, only on the ratio 182.

#### 2.3 Stage C · From the baseline to "the pre-JWST consensus"

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `mod_rep`: the constructed LF represents the pre-JWST theoretical consensus | MOD | stated 2505.11263: "To represent the pre-JWST theoretical consensus, we construct a ΛCDM UV LF" | §4.1 |
| `mod_rule`: if the representative model is disfavored, so is the consensus as represented | MOD | implied (definition of the claim; Enderton 2001, ch. 1) | – |

**Inference (Lean excerpt).**

```lean
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  have h1 : v.ModelDisfavored :=
    p .mod_test (p .obs_count) (p .stat_ratio) (p .num_tail) (p .gap_poisson)  -- Sec. 4.1; GAP
  exact p .mod_rule h1 (p .mod_rep)  -- Sec. 4.1
```

**Critique.** Whether one constructed LF "represents the consensus" is a modelling choice that N26
states openly; how much the factor 182 depends on that choice is what our study explores (R2).

#### 2.4 What the Lean check found

1. **`explicit_insufficient`**: even with standard background added, the chain needs `gap_poisson`:
   without Poisson counts (no cosmic-variance excess) the small tail probability does not make the
   model "disfavored at high confidence".
2. **`stated_insufficient`**: the paper states the count, the ratio and the representativeness; the
   significance step, its number and the inference rule are unstated background.
3. **Every premise is needed** (seven `_needed` countermodels); none is redundant.
4. **The census assumption is not needed**: the count enters only as "at least two".
5. **Consistency** holds but is weak here: every premise is positive.
6. **Limits.** Lean checks the logical structure under our encoding, not the physics inside each
   premise; with uninterpreted atoms "needed" means "used by this encoding".

```lean
inductive Field where
  | obs_count    -- OBS [stated 2505.11263]
  | stat_ratio   -- STAT [stated 2505.11263]
  | num_tail     -- NUM [implied] NUM[results/r1.json:p_tail_n26_ppm <= 200]
  | mod_test     -- MOD [implied]
  | gap_poisson  -- GAP [reconstructed]
  | mod_rep      -- MOD [stated 2505.11263]
  | mod_rule     -- MOD [implied]

theorem explicit_insufficient : ¬ ∀ v, Explicit v → Conclusion v := fun h =>
  h ⟨2, 182, 60, False, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])
```

### Part 3 · What astrolab can test or explore

| Stage / claim | Can we test or explore it? | How | Data (size) | Decision criterion | Result |
|---|---|---|---|---|---|
| A: the number density (R1) | testable now | φ = N/(V Δm) with N = 2, V = 462,648 Mpc³; Gehrels 84% Poisson limits; recompute V from 388 arcmin² and z = 14–15 (Planck 2018) | N26 §4.1 numbers (~1 KB) | reproduced if log φ within 0.01 dex and each error within 0.05 dex; volume within 5% | pending |
| B: Poisson tail under the baseline (Lean `NUM`) | testable now | P(N ≥ 2 \| μ = 2/182) | – | `p_tail_n26_ppm <= 200` | pending |
| B: an independent constant-SFE prediction (R2) | testable now (comparison, not a reproduction of N26's baseline) | Eisenstein–Hu P(k) → Sheth–Tormen halo mass function; SFR = ε(M_h) f_b Ṁ_h (Fakhouri et al. 2010); ε calibrated at z ≈ 8 by deconvolved abundance matching (σ_cal = 0.7 mag) and frozen; predict φ at z = 14–15 | pre-JWST z ≈ 8 LF parameters (paper table, ~1 KB) | φ_model(ours)/φ_model(N26 ≈ 2.4 × 10⁻⁸) within 1/3–3: "same order"; verdict conditional on the fiducial model, with robustness over a pre-declared variant grid | pending |
| D: the σ_UV needed (R3) | testable now | with the median relation fixed, solve φ_model(σ) = φ_obs (and its Poisson limits) | same | central σ reported; interval overlaps N26's ≈ 1.5–2 mag: "consistent"; conditional on R2 | pending |
| H25's z ~ 14 point (R4) | context only | H25's z ~ 14 bin contains only GS-z14-0 (shared with N26) and includes cosmic variance | H25 Table 2 | none (background) | pending |
| Model ingredients (R5) | explorable (not decisive) | halo mass function, accretion fit, calibration redshift, σ_cal, ε extrapolation, dust, completeness c | same | none - exploration only, see README §8 | pending |
| D: cosmic variance (`gap_poisson`) | explorable (not decisive) | halo-bias estimate of the field-to-field variance for two counts | same | none - exploration only | pending |
| F: the baseline represents the consensus (`mod_rep`) | out of scope as a test | would need the pre-JWST model ensemble | – | – | – |

### Glossary

| Term | Meaning |
|---|---|
| redshift z | stretching of light by cosmic expansion; z ≈ 14 means about 290 Myr after the Big Bang |
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
- How strongly does the factor 182 depend on which pre-JWST model represents the consensus?

### Changelog

Newest first.

- 2026-11-15: first version: parts 1–3 (pre-registration source; plan `design/015-plan_*`).

### Sources

- Naidu et al. 2026, OJAp 9, arXiv:2505.11263 [V]
- Carniani et al. 2024, Nature 633, 318, arXiv:2405.18485 [V]
- Harikane et al. 2025, ApJ 980, 138, arXiv:2406.18352 [V]
- Shen et al. 2023, MNRAS 525, 3254, arXiv:2305.05679 [V]
- Gehrels 1986, ApJ 303, 336 (Poisson limits)
- Eisenstein & Hu 1998, ApJ 496, 605, arXiv:astro-ph/9709112; Sheth & Tormen 1999; Fakhouri, Ma & Boylan-Kolchin 2010, MNRAS 406, 2267

---

## 中文

### 第一部分 · 科普详解

#### 1.1 问题与意义

红移 z ≈ 14 的星系发出的光，离开时宇宙只有约 2.9 亿岁，是现在年龄的 2%。在詹姆斯·韦布空间望远镜（JWST, James Webb Space Telescope）之前，星系形成模型预言这么早的星系会很稀少、很暗：足以容纳亮星系的暗物质晕（dark-matter halo）几乎还来不及形成。JWST 在 z ≳ 10 发现的亮星系比预期多得多。这究竟意味着新的物理（宇宙学或恒星形成），还是只说明年轻的星系比假设的更爆发、更少尘埃或恒星形成效率更高，是高红移天文学的主要开放问题之一。

两个星系位于红移范围的最顶端。JADES-GS-z14-0（C24）位于 z_spec = 14.32（后来用 ALMA 精化为 14.18），紫外绝对星等 M_UV = −20.81。MoM-z14（N26）在"Mirage or Miracle"巡天中发现，位于 z_spec = 14.44 ± 0.02，M_UV = −20.23 ± 0.06。两者都由光谱而不只是颜色确认。N26 问这样的星系有多常见，以及与 JWST 之前的预期相比如何。

#### 1.2 数据

某个亮度区间内星系的*数密度*（number density），是星系个数除以搜索的共动体积（comoving volume）再除以以星等计的区间宽度：φ = N / (V Δm)，单位 Mpc⁻³ mag⁻¹。*紫外光度函数*（UV LF, UV luminosity function）就是 φ 随 M_UV 的变化。

N26 统计 z = 14–15、−21 < M_UV < −20 的星系。在 PRIMER 与 JOF 巡天成像的面积内，136 arcmin²（PRIMER-COSMOS）+ 243（PRIMER-UDS）+ 9（JOF）= 388 arcmin²，它假定 MoM-z14 与 JADES-GS-z14-0 是仅有的这类源。该面积上 z = 14 到 15 之间的共动体积为 462,648 Mpc³（N26 第 4.1 节；Planck 2018 宇宙学）。

#### 1.3 一步一步：作者如何从数据走到结论

**(a) 数密度。** φ = 2 / (462,648 Mpc³ × 1 mag) = 4.32 × 10⁻⁶ Mpc⁻³ mag⁻¹，即 log φ = −5.36。N26 给出 −5.36（+0.37/−0.45）。这些误差恰好是两个计数的 84% 单侧泊松（Poisson）限（Gehrels 1986：0.708 到 4.64 个源），尽管 N26 没有写明方法。它们既不含宇宙方差（cosmic variance），也不含任何完备性改正。

**(b) JWST 之前的基准。** N26 写道"To represent the pre-JWST theoretical consensus"，按 S23 的框架构造了一个 ΛCDM 紫外光度函数：晕按暗物质吸积决定的速率增长，流入气体中按文献平均比例的部分形成恒星（恒星形成效率，SFE, star-formation efficiency），紫外光度由恒星形成率按 Chabrier 初始质量函数（IMF, initial mass function）换算，星系相对平均关系的弥散（σ_UV）较小。

**(c) 比较。** 在同一个箱里，这个光度函数预言的星系约少 182 倍（182，+329/−105）：约 2.4 × 10⁻⁸ Mpc⁻³ mag⁻¹。N26："Such an LF underestimates the incidence of observed sources by ≈200×"，并且"is disfavored at high confidence"。

*粗略估算。* 在基准模型下，巡天中预期的星系个数是 2/182 ≈ 0.011（体积相消）。看到两个或更多的泊松概率约为 0.011²/2 ≈ 6 × 10⁻⁵，这就是"高置信度"。

**(d) 什么能解释它。** N26 指出，要匹配 z ≈ 14–15 的光度函数所需的 σ_UV 约为 1.5–2 mag，而由星系成团性（clustering）推断到 z ≈ 9 的值约为 0.7 mag；S23 发现 σ_UV ≈ 0.75 mag 符合 z ≈ 9，但 z ≈ 12（16）需要约 2.0（2.5）mag。其他选项有更高的 SFE、头重型 IMF（top-heavy IMF）、活动星系核（AGN）贡献或新的宇宙学。

#### 1.4 结论与把握程度

- **探测**：两个光谱确认的 z = 14–15 星系（已确立）。
- **过多**：φ 是 JWST 之前共识的"> 100 倍"，该光度函数"is disfavored at high confidence"。这个倍数只基于两个星系（182 的区间为 +329/−105）。
- **解读**：JWST 之后建立的新一代模型"is very much required"。

过多的结论若要不成立，需要以下之一：两个视场异常富集（宇宙方差：z ≈ 14 的稀有星系位于稀有、强成团的晕中，而 N26 没有讨论它）；或者构造的基准低估了 JWST 之前的模型真正的预期。箱中若还有未探测到的星系，只会加强这一结论。

### 第二部分 · 论证逻辑

#### 2.0 论证地图

A. 箱中至少有两个确认的源 → B. 基准光度函数预言约少 182 倍 → C. 看到 ≥ 2 个源的泊松尾概率极小 → D. [缺口] 计数相对模型平均值服从泊松分布（没有宇宙方差的额外弥散）→ E. 所以基准被排除 → F. 基准代表 JWST 之前的共识 ⇒ （如此代表的）JWST 之前的共识以高置信度被排除。

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

Lean 检查什么：结论能否由这些前提推出（`final`）且并非恒真（`final_nontrivial`）；前提能否同时成立（`consistent`）；单个前提不能单独推出结论（`alone_insufficient`）；每个前提是必要的（去掉它时的反例模型）还是多余的；论文明说的前提是否足够（`stated_*`）；加上标准知识后是否足够（`explicit_*`，`explicit_insufficient` 即存在真正的缺口）。Lean 不检查每个前提内部的物理是否正确，那是第一、三部分和研究本身的任务。

编码范围：编码的结论是第 4.1 节的统计句（"is disfavored at high confidence"），说的是构造的基准，并经由它说的是它所代表的共识。没有编码 N26 关于这两个源是箱中仅有的源的假设：更多的源会增大计数，所以不完整的普查不会削弱结论；把计数写成"至少两个"，这一假设就不需要了。

#### 2.1 环节 A · 计数

**概述。** 观测是已知体积内计数的下界。

**前提。**

| 前提（Lean 构造子） | 标签 | 出处性质 | 论文出处 |
|---|---|---|---|
| `obs_count`：至少两个确认的 z = 14–15、−21 < M_UV < −20 的源 | OBS | stated 2505.11263："we assume MoM-z14 and JADES-GS-z14-0 are the only −21<MUV<−20 sources" | 第 4.1 节 |

**其他解释（rival explanations）。**

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 其中一个是低红移的混入者（interloper） | `obs_count`（光谱红移） | 是（光谱；C24、N26） |

**评析。** 很可靠：两个红移都是光谱红移。普查假设（"仅有的"）影响 φ 的数值，不影响结论的方向。

#### 2.2 环节 B · 比较及其显著性

**概述。** 基准预言的源少得多；泊松检验把它变成"被排除"。

**前提。**

| 前提（Lean 构造子） | 标签 | 出处性质 | 论文出处 |
|---|---|---|---|
| `stat_ratio`：观测 / 基准 ≥ 100 | STAT | stated 2505.11263："Such an LF underestimates the incidence of observed sources by ≈200×" | 第 4.1 节（182，+329/−105） |
| `num_tail`：P(N ≥ 2 \| 预期 2/182) ≤ 2 × 10⁻⁴ | NUM | implied（泊松统计；Gehrels 1986）；绑定 `results/r1.json:p_tail_n26_ppm <= 200` | – |
| `mod_test`：在计数服从泊松分布的前提下，尾概率如此小的模型以高置信度被排除 | MOD | implied（显著性检验；Wasserman 2004，第 10 章） | – |
| `gap_poisson`：计数相对模型平均值服从泊松分布（没有宇宙方差的额外弥散） | GAP | reconstructed | 论文没有写 |

**其他解释。**

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 视场过密（宇宙方差） | `gap_poisson` | 否：N26 没有讨论宇宙方差 |
| 两个计数的涨落 | `num_tail` | 隐含（"高置信度"） |

**推理（Lean 摘录）。**

```lean
have h1 : v.ModelDisfavored :=
  p .mod_test (p .obs_count) (p .stat_ratio) (p .num_tail) (p .gap_poisson)  -- Sec. 4.1; GAP
```

**评析。** 泊松尾概率（约 6 × 10⁻⁵）就是"高置信度"。它把预期计数当作精确值，并假定计数服从泊松分布。z ≈ 14 的稀有亮星系位于稀有晕中，这些晕的成团性使视场之间的弥散大于泊松（Somerville 等 2004；Trenti & Stiavelli 2008）；H25 的误差包含这一项，N26 没有。尾概率也与巡天体积无关，只取决于比值 182。

#### 2.3 环节 C · 从基准到"JWST 之前的共识"

**前提。**

| 前提（Lean 构造子） | 标签 | 出处性质 | 论文出处 |
|---|---|---|---|
| `mod_rep`：构造的光度函数代表 JWST 之前的理论共识 | MOD | stated 2505.11263："To represent the pre-JWST theoretical consensus, we construct a ΛCDM UV LF" | 第 4.1 节 |
| `mod_rule`：有代表性的模型被排除，则如此代表的共识也被排除 | MOD | implied（结论的定义；Enderton 2001，第 1 章） | – |

**推理（Lean 摘录）。**

```lean
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  have h1 : v.ModelDisfavored :=
    p .mod_test (p .obs_count) (p .stat_ratio) (p .num_tail) (p .gap_poisson)  -- Sec. 4.1; GAP
  exact p .mod_rule h1 (p .mod_rep)  -- Sec. 4.1
```

**评析。** 一个构造的光度函数是否"代表共识"，是 N26 公开写明的建模选择；182 倍在多大程度上取决于这一选择，是本研究要探讨的（R2）。

#### 2.4 Lean 检查发现的问题

1. **`explicit_insufficient`**：即使加上标准背景知识，链条仍需要 `gap_poisson`：计数若不服从泊松分布（存在宇宙方差的额外弥散），小的尾概率并不能使模型"以高置信度被排除"。
2. **`stated_insufficient`**：论文明说了计数、比值与代表性；显著性一步、它的数值与推断规则是没写出的背景知识。
3. **每个前提都是必要的**（七个 `_needed` 反例模型），没有多余的前提。
4. **普查假设不需要**：计数只以"至少两个"进入。
5. **相容性**成立，但在这里分量很弱：所有前提都是肯定命题。
6. **局限。** Lean 检查的是在我们的编码下的逻辑结构，不检查每个前提内部的物理；原子命题不加解释时，"必要"指"本编码用到了它"。

```lean
inductive Field where
  | obs_count    -- OBS [stated 2505.11263]
  | stat_ratio   -- STAT [stated 2505.11263]
  | num_tail     -- NUM [implied] NUM[results/r1.json:p_tail_n26_ppm <= 200]
  | mod_test     -- MOD [implied]
  | gap_poisson  -- GAP [reconstructed]
  | mod_rep      -- MOD [stated 2505.11263]
  | mod_rule     -- MOD [implied]

theorem explicit_insufficient : ¬ ∀ v, Explicit v → Conclusion v := fun h =>
  h ⟨2, 182, 60, False, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])
```

### 第三部分 · 本项目可检验或探索的环节

| 环节 / 结论 | 能否检验或探索 | 方法 | 数据（大小） | 判据 | 结果 |
|---|---|---|---|---|---|
| A：数密度（R1） | 现在可检验 | φ = N/(V Δm)，N = 2、V = 462,648 Mpc³；Gehrels 84% 泊松限；由 388 arcmin² 与 z = 14–15 复算 V（Planck 2018） | N26 第 4.1 节的数字（约 1 KB） | log φ 差 0.01 dex 以内、各误差差 0.05 dex 以内、体积差 5% 以内 → 复现 | 待定 |
| B：基准下的泊松尾概率（Lean `NUM`） | 现在可检验 | P(N ≥ 2 \| μ = 2/182) | – | `p_tail_n26_ppm <= 200` | 待定 |
| B：独立的恒定 SFE 预言（R2） | 现在可检验（比较，不是复现 N26 的基准） | Eisenstein–Hu 功率谱 → Sheth–Tormen 晕质量函数；SFR = ε(M_h) f_b Ṁ_h（Fakhouri 等 2010）；ε 在 z ≈ 8 用去卷积的丰度匹配（abundance matching，σ_cal = 0.7 mag）校准后冻结；预言 z = 14–15 的 φ | JWST 之前 z ≈ 8 光度函数的参数（论文表格，约 1 KB） | φ_model(本研究)/φ_model(N26 ≈ 2.4 × 10⁻⁸) 在 1/3–3 之间："同一量级"；判定以基准组合为条件，并报告在预先列出的变体网格上是否稳健 | 待定 |
| D：所需的 σ_UV（R3） | 现在可检验 | 固定中位数关系，解 φ_model(σ) = φ_obs（及其泊松限） | 同上 | 报告中心值；区间与 N26 的 ≈ 1.5–2 mag 重叠："一致"；以 R2 为前提 | 待定 |
| H25 的 z ~ 14 点（R4） | 只作背景 | H25 的 z ~ 14 箱只含 GS-z14-0（与 N26 共用），误差含宇宙方差 | H25 表 2 | 无（背景） | 待定 |
| 模型组成（R5） | 可探索（不能判决） | 晕质量函数、吸积拟合式、校准红移、σ_cal、ε 外推、尘埃、完备性 c | 同上 | 无——仅供探索，见 README 第 8 节 | 待定 |
| D：宇宙方差（`gap_poisson`） | 可探索（不能判决） | 用晕偏置（halo bias）估计两个计数的视场间弥散 | 同上 | 无——仅供探索 | 待定 |
| F：基准代表共识（`mod_rep`） | 不在检验范围内 | 需要 JWST 之前的模型集合 | – | – | – |

### 术语表

| 术语 | 含义 |
|---|---|
| 红移（redshift）z | 宇宙膨胀对光的拉伸；z ≈ 14 约为大爆炸后 2.9 亿年 |
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
- 182 倍在多大程度上取决于用哪个 JWST 之前的模型代表共识？

### 研究进展

按时间倒序。

- 2026-11-15：第一版：第一至三部分（预注册的来源；计划 `design/015-plan_*`）。

### 来源

- 同英文部分。
