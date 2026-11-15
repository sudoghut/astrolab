# Black-hole masses in GWTC-4.0: a peak at 35 M☉, or just a bend?

[English](#english) · [中文](#中文)

*Paper(s): LVK 2026, "GWTC-4.0: Population Properties of Merging Compact Binaries", ApJL 1005, L51, arXiv:2508.18083 (main paper, "P26"); GWTC-4.0 catalogue, ApJL 1004, arXiv:2508.18082 ("C26"); GW231123, ApJL 993, L25, arXiv:2507.08219. Study:
[`studies/007-m10-gwtc4-bbh-mass-35msun`](https://github.com/sudoghut/astrolab/tree/main/studies/007-m10-gwtc4-bbh-mass-35msun).
Status: planned. Last updated: 2026-11-15 (see the
changelog at the end). The source of this page lives in the main repository at
[`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki); edit it there.*

*中文标题：GWTC-4.0 中的黑洞质量：35 M☉ 处是一个峰，还是只是一处弯折？状态：计划中。论文：LVK 2026，"GWTC-4.0: Population Properties of Merging Compact Binaries"，ApJL 1005, L51, arXiv:2508.18083（主论文，"P26"）；GWTC-4.0 目录，ApJL 1004, arXiv:2508.18082（"C26"）；GW231123，ApJL 993, L25, arXiv:2507.08219。研究：[`studies/007-m10-gwtc4-bbh-mass-35msun`](https://github.com/sudoghut/astrolab/tree/main/studies/007-m10-gwtc4-bbh-mass-35msun)。最后更新：2026-11-15（见文末"研究进展"）。本页源文件在主仓库的 [`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki) 中，请在那里修改。*

---

## English

### Part 1 · The paper in plain language

#### 1.1 The question and why it matters

When two black holes spiral together and merge, the gravitational waves they emit are recorded by
the LIGO, Virgo and KAGRA detectors. Each signal reveals the masses of the two black holes. With
enough events one can ask how black-hole masses are distributed: are they spread smoothly, or do
some masses occur more often than others? Features in that distribution are clues to how the
binaries formed. A pile-up near 35 times the Sun's mass (35 M☉) has been discussed since the first
catalogues; one explanation is that very massive stars shed mass or are disrupted by the
"pair-instability" process, which would leave a gap above roughly 50–60 M☉ and pile black holes up
just below it. Others explain it by star clusters or by the physics of mass transfer.

#### 1.2 The data

GWTC-4.0 adds 128 new candidates from the first part of the fourth observing run (O4a) to the
earlier catalogues. For the black-hole population study P26 keeps binary black holes (BBHs) with a
false-alarm rate below one per year in at least one search pipeline and with both component masses
confidently above 3 M☉ (the 1% lower limit of each mass above 3 M☉): 84 from O4a and 69 from
GWTC-3.0, 153 in all. Detectors see massive binaries further away than light ones, so the raw counts
are biased; P26 corrects for this with simulated signals ("injections") put through the same search
pipelines, from which the detection probability for any population is computed by a Monte Carlo
integral.

#### 1.3 Step by step: how the authors got from data to conclusion

**(a) Models.** P26 fits two kinds of models to the 153 events: "strongly modeled" ones with a fixed
shape (the fiducial Broken Power Law + 2 Peaks: two power laws joined at a break mass, plus two
Gaussian peaks) and "weakly modeled" ones that can take almost any shape (a B-spline and a binned
Gaussian process). Each event's mass uncertainty and the selection effects enter the likelihood.

**(b) Steepening above 35 M☉.** Below 35 M☉ the continuum falls as m1^(−1.7); above it as
m1^(−4.5). P26: λ2 > λ1 "at 97.7% credibility".

*Back of the envelope.* With these slopes, at 70 M☉ the merger rate per unit mass is
(70/35)^−(4.5−1.7) = 2^−2.8 ≈ 0.14 of what a single power law would give, about seven times fewer
very massive black holes.

**(c) Peak or break?** P26 §6.1: the 35 M☉ feature is "consistent with either" an over-density
peaking near 32.7 M☉ on top of a broken power law, or a plain break near 34.1 M☉. The weakly modeled
B-spline "exhibits a local peak at" 33.5 M☉. Among models with a broken power law, "the Bayes
factors do not show strong support for one model over another": one peak against two peaks gives
log10 B = −0.06, and the fiducial posterior has two modes (71% a narrow peak, 29% close to a plain
break). Appendix D.1: the feature "may be an overdensity … or could mark the onset of a decline in
the merger rate".

**(d) Other features.** A global peak at 10 M☉ is robust across models; "a bump near 20 M⊙ is
present in some of the weakly modeled approaches", while the strongly modeled comparison cannot
decide (log10 B = −0.34). The local merger rate is 14–26 Gpc⁻³ yr⁻¹ (the union of two models' 90%
intervals). The heaviest event, GW231123 (about 137 + 101 M☉), is consistent with the inferred
spectrum.

#### 1.4 What they conclude, and how sure they are

The abstract: "We resolve multiple over- and under-densities in the black hole mass distribution:
features persist at primary masses of 10 M⊙ and 35 M⊙ with a possible third feature at 20 M⊙. These
are departures from an otherwise power-law-like continuum that steepens above 35 M⊙." The steepening
is credible at 97.7%; whether the 35 M☉ feature is a peak or only a bend is left open in the body.

For the 35 M☉ feature to be wrong, the slope change would have to be produced by the modelling: an
inadequate model shape, systematic errors in the event masses (P26 notes a likelihood normalisation
error it expects to be negligible), the expected noise events among the candidates (about 6.7 of 161
compact-binary candidates), or errors in the selection function at high mass.

### Part 2 · The logic of the argument

#### 2.0 Map of the argument

A. A selected sample of 153 BBHs → B. selection effects from injections → C. λ2 > λ1 at 97.7% →
D. [gap] the models and systematics do not produce a spurious break → E. so the spectrum steepens →
F. a departure from a power-law continuum is a feature ⇒ a feature at 35 M☉. Separately: the B-spline
peak and the Bayes-factor tie do not establish an over-density.

How we check it: the argument is written in Lean 4
([`studies/007-m10-gwtc4-bbh-mass-35msun/argument/Argument.lean`](https://github.com/sudoghut/astrolab/blob/main/studies/007-m10-gwtc4-bbh-mass-35msun/argument/Argument.lean)).
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

Scope: the conclusion encoded is the 35 M☉ part of the abstract's "features persist …"; the 10 M☉
peak and the 20 M☉ bump are discussed only here. An extra theorem, `overdensity_not_implied`, checks
the stronger reading "over-density at 35 M☉".

#### 2.1 Stage A · Sample and selection

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `obs_sample`: the 153-event BBH sample with the stated cuts | OBS | stated 2508.18083: "We only include events whose 1% lower limit on both component mass posteriors" | §6 |
| `mod_sel`: detection efficiency from injections | MOD | stated 2508.18083: "is estimated using these injections through a Monte Carlo integral" | §3.3 |

**Critique.** The sample is reproducible in principle from public lists (our R1); the selection
function needs injection files of hundreds of MB, outside this project's limits.

#### 2.2 Stage B · From a slope change to a feature

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `stat_steep`: λ2 > λ1 with credibility ≥ 95% | STAT | stated 2508.18083: "at 97.7% credibility" | §6.1 |
| `gap_model`: models, PE systematics and noise events do not make a spurious break near 35 M☉ | GAP | reconstructed | not tested in the paper |
| `mod_steep`: a credible slope change in an adequate model with correct selection is an astrophysical steepening | MOD | implied (Bayesian inference; Gelman et al. 2013, ch. 1) | – |
| `mod_feature`: such a departure from a power-law continuum is a feature | MOD | stated 2508.18083: "These are departures from an otherwise power-law-like continuum" | Abstract |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| The model shape forces a break | `gap_model` | partly: weakly modeled fits agree |
| Mass systematics or noise events near 35 M☉ | `gap_model` | partly (likelihood error "negligible"; contamination estimated, not propagated) |
| Selection-function errors at high mass | `mod_sel` | no direct test |

**Inference (Lean excerpt).**

```lean
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  have h1 : v.Steepens :=
    p .mod_steep (p .obs_sample) (p .mod_sel) (p .stat_steep) (p .gap_model)  -- Sec. 3.3, 6, 6.1; GAP
  exact p .mod_feature h1  -- Abstract
```

#### 2.3 Stage C · Peak or break

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `stat_bspline`: the B-spline has a local peak near 33.5 M☉ | STAT | stated 2508.18083: "which exhibits a local peak at" | §6.1 |
| `stat_tie`: Bayes factors do not prefer peak over break | STAT | stated 2508.18083: "the Bayes factors do not show strong support for one model over another" | App. D.1 (log10 B = −0.06) |
| `mod_od`: an over-density claim needs the peak model to be preferred | MOD | implied (Kass & Raftery 1995) | – |

```lean
theorem overdensity_not_implied : ¬ ∀ v, Premises v → v.OverDensity35 := fun h =>
  h ⟨True, True, 977, True, True, True, True, True, False⟩ (by intro f; cases f <;> simp [prem])
```

**Critique.** "Feature" in the abstract is safe as "departure from a power law"; the abstract's
framing "over- and under-densities" is stronger than the body supports at 35 M☉.

#### 2.4 What the Lean check found

1. **`explicit_insufficient`**: the feature needs `gap_model`, that no part of the modelling (model
   shape, PE systematics, noise events) creates a spurious break near 35 M☉.
2. **`stated_insufficient`**: the stated premises omit the step from a credible slope change to an
   astrophysical steepening (standard Bayesian reading).
3. **`overdensity_not_implied`**: with every premise true, including the B-spline peak, the
   over-density reading does not follow, because the Bayes factors tie.
4. **Redundant premises**: `stat_bspline`, `stat_tie` and `mod_od` are redundant for the encoded
   conclusion; they matter only for the over-density reading (item 3). Six premises are needed.
5. **Consistency** holds; weak here (only `mod_od` contains a negation).
6. **Limits.** Lean checks the logical structure under our encoding, not the physics.

### Part 3 · What astrolab can test or explore

| Stage / claim | Can we test or explore it? | How | Data (size) | Decision criterion | Result |
|---|---|---|---|---|---|
| A: the 153-event sample (R1) | testable now | rebuild from GWOSC lists (GWTC-4.0, GWTC-1/2.1/3) with P26's cuts (FAR < 1/yr, 90% lower bound as a proxy for the 1% bound, exclusions); compare with the O4a list on Zenodo | GWOSC JSON (~0.25 MB + < 1 MB each), O4a list 10 kB | "reproduced" if the O4a events match P26's list and the counts are 84 and 69, with only pre-declared, direction-known differences; downgraded to "described" if the meaning of GWOSC's `far` cannot be confirmed | pending |
| Sample-level counts above and below 35 M☉ (R2) | explorable (descriptive) | median m1 counts against a single power law (λ1 = 1.7) times a toy VT(m1) with a turnover, scanning the turnover | same | none - descriptive (medians blur a break; 1-D VT is a toy) | pending |
| Steepening vs selection curvature (R3) | explorable (not decisive) | point-estimate toy fit of a broken power law, with and without a peak, scanning the VT turnover | same | none - exploration only | pending |
| GW231123 (R4) | descriptive | its total mass within the rebuilt sample (not P26's quantity) | same | none | pending |
| `gap_model`, selection function, population inference | out of scope | needs posterior samples and injections (hundreds of MB to tens of GB; AGENTS.md 1.5) | – | – | – |

### Glossary

| Term | Meaning |
|---|---|
| BBH | binary black hole |
| primary mass m1 | the mass of the heavier black hole |
| FAR (false-alarm rate) | how often noise alone would produce a signal at least as loud |
| injections | simulated signals added to detector data to measure detection probability |
| selection effects | the bias of a detected sample towards events that are easier to see |
| power law, spectral index λ | dR/dm1 ∝ m1^(−λ); a larger λ is a steeper fall |
| Bayes factor B | ratio of the evidence for two models; log10 B near 0 means no preference |
| pair instability | a process in very massive stars that may prevent black holes of about 50–130 M☉ forming |

### Open questions

- Is the 35 M☉ feature a peak or a break? (P26 leaves it open.)
- How sensitive is the steepening to the high-mass selection function?

### Changelog

Newest first.

- 2026-11-15: first version: parts 1–3 (pre-registration source; plan `design/016-plan_*`).

### Sources

- LVK 2026, ApJL 1005, L51, arXiv:2508.18083 [V]
- LVK 2026 (GWTC-4.0), ApJL 1004, arXiv:2508.18082 [V]
- LVK 2025 (GW231123), ApJL 993, L25, arXiv:2507.08219 [V]
- Tiwari 2026, arXiv:2510.25579; Tenorio et al. 2025, arXiv:2509.19466; Sridhar, Ray & Kalogera, arXiv:2511.22093 (context)
- Kass & Raftery 1995, JASA 90, 773; Gelman et al. 2013, *Bayesian Data Analysis*

---

## 中文

### 第一部分 · 科普详解

#### 1.1 问题与意义

两个黑洞旋近并合时发出的引力波被 LIGO、Virgo 与 KAGRA 探测器记录下来，每个信号都给出两个黑洞的质量。事件足够多时，就可以问黑洞的质量如何分布：是平滑地铺开，还是某些质量出现得更频繁？这种分布中的特征是双星如何形成的线索。约 35 倍太阳质量（35 M☉）处的堆积从最早的目录起就有讨论；一种解释是，极大质量的恒星会因"对不稳定"（pair instability）过程损失质量或被瓦解，在约 50–60 M☉ 以上留下空缺，使黑洞堆积在其下方。另一些解释诉诸星团或质量转移的物理。

#### 1.2 数据

GWTC-4.0 在早期目录之外加入了第四观测期前半段（O4a）的 128 个新候选体。在黑洞群体研究中，P26 保留至少一个搜索管线中误报率（FAR, false-alarm rate）低于每年一次、且两个分量质量都可靠地高于 3 M☉（每个质量的 1% 下限高于 3 M☉）的双黑洞（BBH）：O4a 84 个，GWTC-3.0 69 个，共 153 个。探测器能看到更远处的大质量双星，所以原始计数有偏；P26 用经过同样搜索管线的模拟信号（"注入"，injection）来改正，并用蒙特卡罗积分计算任意群体的探测概率。

#### 1.3 一步一步：作者如何从数据走到结论

**(a) 模型。** P26 对 153 个事件拟合两类模型："强模型化"的有固定形状（基准为 Broken Power Law + 2 Peaks：两段幂律在折断质量处相接，再加两个高斯峰），"弱模型化"的几乎可以取任意形状（B 样条与分箱高斯过程）。每个事件的质量不确定性与选择效应都进入似然。

**(b) 35 M☉ 以上变陡。** 35 M☉ 以下连续谱按 m1^(−1.7) 下降，以上按 m1^(−4.5)。P26：λ2 > λ1"at 97.7% credibility"。

*粗略估算。* 用这两个斜率，在 70 M☉ 处每单位质量的并合率是单一幂律的 (70/35)^−(4.5−1.7) = 2^−2.8 ≈ 0.14，即很重的黑洞约少七倍。

**(c) 峰还是折断？** P26 第 6.1 节：35 M☉ 的特征"consistent with either"在折断幂律之上峰值约 32.7 M☉ 的过密，或约 34.1 M☉ 的单纯折断。弱模型化的 B 样条"exhibits a local peak at" 33.5 M☉。在含折断幂律的模型中，"the Bayes factors do not show strong support for one model over another"：一个峰对两个峰的 log10 B = −0.06，基准模型的后验有两个模态（71% 窄峰，29% 接近单纯折断）。附录 D.1：这一特征"may be an overdensity"或"could mark the onset of a decline in the merger rate"。

**(d) 其他特征。** 10 M☉ 的全局峰在各模型中都稳健；"a bump near 20 M⊙ is present in some of the weakly modeled approaches"，强模型化的比较不能确定（log10 B = −0.34）。局部并合率为 14–26 Gpc⁻³ yr⁻¹（两种模型 90% 区间的并集）。最重的事件 GW231123（约 137 + 101 M☉）与推断的质量谱相容。

#### 1.4 结论与把握程度

摘要："We resolve multiple over- and under-densities in the black hole mass distribution: features persist at primary masses of 10 M⊙ and 35 M⊙ with a possible third feature at 20 M⊙. These are departures from an otherwise power-law-like continuum that steepens above 35 M⊙." 变陡的可信度为 97.7%；35 M☉ 的特征是峰还是只是弯折，正文中没有定论。

35 M☉ 的特征若要不成立，斜率的变化必须是建模造成的：模型形状不当、事件质量的系统误差（P26 指出一个它认为影响可忽略的似然归一化错误）、候选体中预期的噪声事件（161 个致密双星候选体中约 6.7 个），或高质量处选择函数的误差。

### 第二部分 · 论证逻辑

#### 2.0 论证地图

A. 选出的 153 个 BBH 样本 → B. 由注入得到的选择效应 → C. λ2 > λ1 的可信度 97.7% → D. [缺口] 模型与系统误差不会造成虚假的折断 → E. 所以质量谱变陡 → F. 偏离幂律连续谱即为特征 ⇒ 35 M☉ 处有特征。另外：B 样条的峰与贝叶斯因子的平局不能确立过密。

检查方法：论证写成 Lean 4（[`studies/007-m10-gwtc4-bbh-mass-35msun/argument/Argument.lean`](https://github.com/sudoghut/astrolab/blob/main/studies/007-m10-gwtc4-bbh-mass-35msun/argument/Argument.lean)）。每个前提是 `Field` 的一个构造子（不用公理 axiom），标注类型与出处性质：

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

编码范围：编码的结论是摘要"features persist …"中关于 35 M☉ 的部分；10 M☉ 的峰与 20 M☉ 的隆起只在这里讨论。另一条定理 `overdensity_not_implied` 检查更强的解读"35 M☉ 处有过密"。

#### 2.1 环节 A · 样本与选择

| 前提（Lean 构造子） | 标签 | 出处性质 | 论文出处 |
|---|---|---|---|
| `obs_sample`：按所述条件选出的 153 个 BBH 样本 | OBS | stated 2508.18083："We only include events whose 1% lower limit on both component mass posteriors" | 第 6 节 |
| `mod_sel`：由注入得到探测效率 | MOD | stated 2508.18083："is estimated using these injections through a Monte Carlo integral" | 第 3.3 节 |

**评析。** 样本原则上可以由公开列表重建（本研究的 R1）；选择函数需要数百 MB 的注入文件，超出本项目的上限。

#### 2.2 环节 B · 从斜率变化到特征

| 前提（Lean 构造子） | 标签 | 出处性质 | 论文出处 |
|---|---|---|---|
| `stat_steep`：λ2 > λ1 的可信度 ≥ 95% | STAT | stated 2508.18083："at 97.7% credibility" | 第 6.1 节 |
| `gap_model`：模型、参数估计的系统误差与噪声事件不会在 35 M☉ 附近造成虚假的折断 | GAP | reconstructed | 论文没有检验 |
| `mod_steep`：在适当的模型与正确的选择效应下，可信的斜率变化就是天体物理上的变陡 | MOD | implied（贝叶斯推断（Bayesian inference）；Gelman 等 2013，第 1 章） | – |
| `mod_feature`：这样偏离幂律连续谱即为特征 | MOD | stated 2508.18083："These are departures from an otherwise power-law-like continuum" | 摘要 |

**其他解释（rival explanations）。**

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 模型形状强加了折断 | `gap_model` | 部分：弱模型化拟合一致 |
| 35 M☉ 附近的质量系统误差或噪声事件 | `gap_model` | 部分（似然错误"可忽略"；污染有估计但未传播） |
| 高质量处选择函数的误差 | `mod_sel` | 没有直接检验 |

**推理（Lean 摘录）。**

```lean
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  have h1 : v.Steepens :=
    p .mod_steep (p .obs_sample) (p .mod_sel) (p .stat_steep) (p .gap_model)  -- Sec. 3.3, 6, 6.1; GAP
  exact p .mod_feature h1  -- Abstract
```

#### 2.3 环节 C · 峰还是折断

| 前提（Lean 构造子） | 标签 | 出处性质 | 论文出处 |
|---|---|---|---|
| `stat_bspline`：B 样条在约 33.5 M☉ 有局部峰 | STAT | stated 2508.18083："which exhibits a local peak at" | 第 6.1 节 |
| `stat_tie`：贝叶斯因子不偏好峰而非折断 | STAT | stated 2508.18083："the Bayes factors do not show strong support for one model over another" | 附录 D.1（log10 B = −0.06） |
| `mod_od`：主张过密需要峰模型被偏好 | MOD | implied（Kass & Raftery 1995） | – |

```lean
theorem overdensity_not_implied : ¬ ∀ v, Premises v → v.OverDensity35 := fun h =>
  h ⟨True, True, 977, True, True, True, True, True, False⟩ (by intro f; cases f <;> simp [prem])
```

**评析。** 摘要中的"特征"作为"偏离幂律"是稳妥的；摘要"over- and under-densities"的说法对 35 M☉ 而言强于正文所支持的。

#### 2.4 Lean 检查发现的问题

1. **`explicit_insufficient`**：特征需要 `gap_model`，即建模的任何部分（模型形状、参数估计的系统误差、噪声事件）都不会在 35 M☉ 附近造成虚假的折断。
2. **`stated_insufficient`**：论文明说的前提缺少从可信的斜率变化到天体物理上变陡的一步（标准的贝叶斯解读）。
3. **`overdensity_not_implied`**：即使所有前提都成立（包括 B 样条的峰），由于贝叶斯因子平局，过密的解读也推不出来。
4. **多余的前提**：`stat_bspline`、`stat_tie` 与 `mod_od` 对编码的结论是多余的，它们只与过密的解读有关（第 3 条）。六个前提是必要的。
5. **相容性**成立；在这里分量较弱（只有 `mod_od` 含否定）。
6. **局限。** Lean 检查的是在我们的编码下的逻辑结构，不检查物理。

### 第三部分 · 本项目可检验或探索的环节

| 环节 / 结论 | 能否检验或探索 | 方法 | 数据（大小） | 判据 | 结果 |
|---|---|---|---|---|---|
| A：153 个事件的样本（R1） | 现在可检验 | 按 P26 的条件（FAR < 1/yr、以 90% 下限近似 1% 下限、排除项）由 GWOSC 列表（GWTC-4.0、GWTC-1/2.1/3）重建；与 Zenodo 上的 O4a 列表比较 | GWOSC JSON（约 0.25 MB，其余各 < 1 MB），O4a 列表 10 kB | O4a 事件与 P26 列表一致、计数为 84 与 69，只允许预先声明且方向已知的差别 → "复现"；若不能确认 GWOSC `far` 的含义则降为"描述" | 待定 |
| 35 M☉ 上下的样本计数（R2） | 可探索（描述） | 中位数 m1 的计数，与单一幂律（λ1 = 1.7）乘以带转折的玩具 VT(m1) 比较，扫描转折质量 | 同上 | 无——描述（中位数会抹平折断；一维 VT 是玩具） | 待定 |
| 变陡对选择函数曲率的敏感度（R3） | 可探索（不能判决） | 折断幂律（加或不加峰）的点估计玩具拟合，扫描 VT 的转折 | 同上 | 无——仅供探索 | 待定 |
| GW231123（R4） | 描述 | 它的总质量在重建样本中的位置（与 P26 的量不同） | 同上 | 无 | 待定 |
| `gap_model`、选择函数、群体推断 | 不在范围内 | 需要后验样本与注入（数百 MB 到数十 GB；AGENTS.md 1.5） | – | – | – |

### 术语表

| 术语 | 含义 |
|---|---|
| BBH | 双黑洞（binary black hole） |
| 主质量（primary mass）m1 | 较重黑洞的质量 |
| 误报率（FAR） | 仅由噪声产生至少同样响的信号的频率 |
| 注入（injection） | 加入探测器数据、用来测量探测概率的模拟信号 |
| 选择效应（selection effects） | 探测样本偏向容易看到的事件 |
| 幂律与谱指数（spectral index）λ | dR/dm1 ∝ m1^(−λ)；λ 越大下降越陡 |
| 贝叶斯因子（Bayes factor）B | 两个模型证据之比；log10 B 接近 0 表示没有偏好 |
| 对不稳定（pair instability） | 极大质量恒星中的一种过程，可能使约 50–130 M☉ 的黑洞无法形成 |

### 开放问题

- 35 M☉ 的特征是峰还是折断？（P26 没有定论。）
- 变陡对高质量处的选择函数有多敏感？

### 研究进展

按时间倒序。

- 2026-11-15：第一版：第一至三部分（预注册的来源；计划 `design/016-plan_*`）。

### 来源

- 同英文部分。
