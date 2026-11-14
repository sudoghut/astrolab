# The Hubble tension: does the choice of calibrator galaxies explain the lower JWST values?

[English](#english) · [中文](#中文)

*Paper(s): Riess et al. 2024, "JWST Validates HST Distance Measurements: Selection of Supernova
Subsample Explains Differences in JWST Estimates of Local H0", ApJ (accepted), arXiv:2408.11770;
context: Riess et al. 2022 (R22), ApJL, doi:10.3847/2041-8213/ac5c5b, arXiv:2112.04510; Freedman et
al. 2025 (CCHP), arXiv:2408.06153. Study:
[`studies/003-m02-hubble-tension-distance-ladder`](https://github.com/sudoghut/astrolab/tree/main/studies/003-m02-hubble-tension-distance-ladder).
Status: planned. Last updated: 2026-11-14 (see the changelog at the end). The source of this page
lives in the main repository at
[`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki); edit it there.*

*中文标题：哈勃张力：校准星系的选择能否解释 JWST 给出的较低数值？状态：计划中。论文：Riess 等 2024，arXiv:2408.11770（ApJ 已接收）；背景：Riess 等 2022（R22），ApJL，doi:10.3847/2041-8213/ac5c5b，arXiv:2112.04510；Freedman 等 2025（CCHP），arXiv:2408.06153。研究：[`studies/003-m02-hubble-tension-distance-ladder`](https://github.com/sudoghut/astrolab/tree/main/studies/003-m02-hubble-tension-distance-ladder)。最后更新：2026-11-14（见文末"研究进展"）。本页源文件在主仓库的 [`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki) 中，请在那里修改。*

---

## English

### Part 1 · The paper in plain language

#### 1.1 The question and why it matters

The Hubble constant H0 is today's expansion rate of the Universe. It can be measured directly, by
measuring distances and recession speeds of nearby galaxies, or predicted from the cosmic
microwave background (CMB) using the standard model ΛCDM. The direct route gives about 73
km/s/Mpc, the prediction about 67–68 (Planck 2018: 67.4 ± 0.5; SPT-3G + ACT + Planck: 67.19 ±
0.38). If both are right, something is missing from the standard model: this is the "Hubble
tension".

The direct measurement is a *distance ladder*. Rung 1: geometric distances to a few nearby
"anchors" (parallaxes of Milky Way Cepheids, water masers orbiting the black hole in NGC 4258,
eclipsing binaries in the Large Magellanic Cloud). Rung 2: Cepheid variable stars, whose period
tells their luminosity, measured both in the anchors and in galaxies that also hosted a type Ia
supernova (SN Ia). Rung 3: SNe Ia far away in the smooth Hubble flow, where redshift gives the
expansion rate.

#### 1.2 The data

The SH0ES team (Riess et al. 2022, "R22") used Cepheids in 37 galaxies that hosted 42 SNe Ia, three
anchors, and 277 SNe Ia in the Hubble flow (0.0233 < z < 0.15). All of it fits into one system of
linear equations y = L q: about 3500 magnitudes y, a design matrix L, a covariance matrix C, and 47
unknowns q (the distance of each host, Cepheid calibration terms, the SN Ia luminosity M_B, and
5 log H0 as the last entry). R22 published y, L and C; this repo can refit them.

The Chicago-Carnegie Hubble Program (CCHP; Freedman et al. 2025) uses other stars as rung 2: the
tip of the red giant branch (TRGB) and carbon stars (JAGB). With the James Webb Space Telescope
(JWST) it observed 10 of the SN hosts (11 SNe Ia) and found lower values, 70.39 ± 1.22 (stat) ±
1.33 (sys) from 24 calibrators in total, and 68.81 (CSP SNe) or 69.29 (Pantheon+ SNe) from the 11
JWST calibrators alone.

#### 1.3 Step by step

**Step 1 — the SH0ES baseline.** R22's fit gives H0 = 73.04 ± 1.01, or ± 1.04 once the spread of 67
analysis variants is added (Eq. 10). Using only NGC 4258 as anchor gives 72.51 ± 1.54.

**Step 2 — the 2024 update and the CCHP subsample.** Riess et al. 2024 re-derived the full HST
sample (42 SNe Ia, now 4 anchors): 73.2 ± 0.9. Then they asked what the same HST Cepheid ladder
gives if one keeps only the 10 hosts CCHP chose for JWST and only NGC 4258 as anchor: 71.2, "2.0
km/s/Mpc lower than the full HST sample — simply due to the choice of SN hosts and anchor". The
table splits this into about −0.6 from the anchor and about −1.3 from the hosts.

**Step 3 — same hosts, different stars.** On the CCHP sample, JWST JAGB and HST Cepheid distances
differ by 0.047 ± 0.066 mag, i.e. agree within errors; HST and JWST Cepheids agree to within a few
hundredths of a magnitude.

**Step 4 — the conclusion.** The CCHP JWST program is about 2.5 km/s/Mpc below the full HST sample.
About 2.0 of that is expected from the choice of hosts and anchor alone; the remaining ~0.5 is well
within the ~2 km/s/Mpc uncertainty of an 11-supernova subsample. Hence the abstract: the difference
"is entirely consistent with differences in sample selection".

Back of the envelope: an 11-SN calibration with ~0.13 mag scatter per SN has an uncertainty of
0.13/√11 ≈ 0.04 mag in M_B, i.e. about 2% or 1.4 km/s/Mpc in H0 before anchor and Cepheid terms —
so a 2 km/s/Mpc swing between different 10-host subsets is not surprising.

#### 1.4 What they conclude, and how sure they are

The claim is deliberately weak: the CCHP–SH0ES difference is *consistent with* sample selection,
not proved to be caused by it. It would be wrong if (a) the 71.2 estimate (an approximation, from
M_B and a scaling formula, on 2024 data) does not hold up in a full fit, (b) the same-host
comparison hides a real TRGB/JAGB–Cepheid offset that small samples cannot detect, or (c) the
selected hosts are typical and the shift is a fluctuation that would not recur.

### Part 2 · The logic of the argument

#### 2.0 Map of the argument

A. measurements: full sample 73.2; SH0ES ladder on the CCHP hosts 71.2; observed gap ~2.5 →
B. expectation: choosing those hosts and anchor lowers H0 by ~2 →
C. same-host check: JAGB and Cepheid distances agree within errors →
D. leftover ~0.5 within the subsample error ⇒ the gap is entirely consistent with sample selection.

How we check it: the argument is written in Lean 4
([`studies/003-m02-hubble-tension-distance-ladder/argument/Argument.lean`](https://github.com/sudoghut/astrolab/blob/main/studies/003-m02-hubble-tension-distance-ladder/argument/Argument.lean)).
Each premise is one constructor of `Field` (no axioms), labelled with its kind and its provenance:

| Tag | Kind of premise |
|---|---|
| `OBS` | observation or measurement (with table / figure) |
| `MOD` | modelling assumption |
| `STAT` | statistical inference (significance, model comparison) |
| `NUM` | numerical result, re-computed by this repo's `run.py` |
| `LIT` | result taken from other literature |
| `GAP` | premise the inference needs that neither the paper nor standard knowledge supplies |

Provenance: `[stated <arXiv id>: "quote"]`, `[implied]` (standard knowledge, with a source),
`[reconstructed]` (our addition; exactly the `GAP` premises). Lean checks that the conclusion
follows (`final`), is not trivial (`final_nontrivial`), that the premises are consistent, that no
single premise suffices, which premises are needed, and whether the stated (`stated_*`) or the
explicit (`explicit_*`) premises suffice. It does not check the physics inside the premises.
H0 values are whole numbers in tenths of km/s/Mpc (73.2 → 732).

#### 2.1 Stage A–B · The selection shift

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `stat_full`: full HST sample H0 ≥ 73.1 | STAT | stated 2408.11770: "is not yet competitive with the HST set (42 SNe Ia and 4 anchors), which yields 73.2 $\pm$ 0.9" | Abstract |
| `stat_sel`: HST Cepheids on the CCHP hosts H0 ≤ 71.2 | STAT | stated 2408.11770: "a corresponding value of H ${}_{0}=71.2$" | §III.2 |
| `mod_drop`: these two → choosing the CCHP hosts and anchor lowers H0 by ~2 | MOD | stated 2408.11770: "thus 2.0 $\,\rm km\,s^{-1}\,Mpc^{-1}$ lower than the full HST sample—simply due to the choice of SN hosts and anchor" | §III.2 |

```lean
have d : v.ExpDrop := p .mod_drop (p .stat_full) (p .stat_sel)   -- Sec. III.2
```

**Critique.** The 71.2 comes from M_B = −19.32 ± 0.05 and the paper's scaling formula on 2024 data,
not from a full refit; it mixes an anchor change (~−0.6) with a host change (~−1.3). This is exactly
what this repo can recompute with R22's matrices (part 3, R2).

#### 2.2 Stage C · Same hosts, different distance indicators

| Premise | Tag | Provenance | Source |
|---|---|---|---|
| `stat_agree`: JAGB and Cepheid distances agree on the CCHP sample | STAT | stated 2408.11770: "For comparisons between JWST JAGB and HST Cepheids, we measure a difference with the CCHP JWST sample of $0.047\pm 0.066$ mag" | §III |

**Critique.** Agreement within 0.066 mag (≈ 3% in distance) cannot exclude an offset of a few
percent; the check has low power, and it is shown for JAGB, not for TRGB.

#### 2.3 Stage D · From "expected shift" to "consistent"

| Premise | Tag | Provenance | Source |
|---|---|---|---|
| `stat_gap`: observed CCHP–HST gap ≤ 3.0 | STAT | stated 2408.11770: "We show that $\Delta$ H ${}_{0}\sim$ 2.5" | Abstract |
| `mod_resid`: gap ≲ 3 and expected drop ~2 → leftover within the ~2 subsample error | MOD | implied: comparison of a difference with its standard error (Taylor 1997) | — |
| `mod_cons`: expected drop + same-host agreement + small leftover → consistent | MOD | implied: meaning of "consistent" (no significant residual) | — |

```lean
have r : v.ResidSmall := p .mod_resid (p .stat_gap) d             -- Abstract, Table 4
exact p .mod_cons d (p .stat_agree) r                             -- Abstract
```

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| A real TRGB–Cepheid offset of a few percent | `stat_agree` only within ~3% | partly: JAGB within 0.066 mag |
| The CCHP hosts are unusual, not a fluctuation | not encoded (the conclusion does not need it) | no |
| The full refit gives a smaller host shift than 71.2 suggests | `stat_sel`, `mod_drop` | no (approximation) |

#### 2.4 What the Lean check found

1. **`explicit_sufficient`**: with standard knowledge the chain closes; there is no `GAP`. This is
   because the conclusion is weak: "entirely consistent with" needs only that no part of the gap
   is significant beyond errors.
2. **`stated_insufficient`**: the comparison of the ~0.5 leftover with the subsample uncertainty
   (`mod_resid`) and the rule from that to "consistent" (`mod_cons`) are left implicit.
3. **Every premise is needed** (seven `_needed` theorems): a single route.
4. **Weak points** (ours): the 71.2 is an approximation on newer data; the same-host agreement has
   low power and covers JAGB only; "consistent with" is not "caused by". The study (part 3) tests
   the first directly.
5. **Limits**: Lean checks the structure under our encoding, not the astrophysics.

### Part 3 · What astrolab can test or explore

| Stage / claim | Can we test or explore it? | How | Data (size) | Decision criterion | Result |
|---|---|---|---|---|---|
| R1 · the SH0ES baseline | testable now | GLS fit of R22's y, L, C | C 46.5 MiB (Git LFS FITS), L 0.66 MB, y 17 kB, lstsq 0.7 kB | primary: reproduce the authors' `lstsq_results.txt` (47 parameters); secondary: 73.04 ± 1.01 (tolerances in README §2) | pending |
| R2 · stage A–B: anchor and host shifts | testable now | refit with NGC 4258 only (drop the other anchors' geometric rows), then restrict to the CCHP hosts; shifts in 5 log H0 with exact linear error propagation | same | anchor shift vs R22's −0.0158 mag; host shift: null "no shift", four-outcome table vs the paper's −0.0405 mag (README §2) | pending |
| R3 · stage C: same hosts, Cepheid vs TRGB | explorable (descriptive by default) | joint linear estimator with CCHP's JWST TRGB distances; reproduce 69.29 first | CCHP Table 3 (paper) | descriptive unless the full CCHP error budget can be mapped before data | pending |
| R4 · is the CCHP choice unusual? | explorable (descriptive) | random 10-host subsets of the 37 hosts, ΔH0 percentile | same | none — exploration only | pending |
| Cross-paper comparison | explorable (descriptive) | pairwise differences for independent pairs only (ladder vs CMB, TDCOSMO vs others) | paper numbers | none | pending |

### Glossary

| Term | Meaning |
|---|---|
| distance ladder | anchors → Cepheids (or TRGB, JAGB) → SNe Ia → Hubble flow |
| anchor | galaxy with a geometric distance (Milky Way parallaxes, NGC 4258 masers, LMC eclipsing binaries) |
| TRGB, JAGB | tip of the red giant branch; J-region asymptotic giant branch (carbon stars) |
| GLS | generalised least squares: q̂ = (LᵀC⁻¹L)⁻¹LᵀC⁻¹y |
| 5 log H0 | the ladder's last parameter; the fit is linear in it, not in H0 |

### Changelog

- 2026-11-14: first version: parts 1–3, written before implementation (T-012, plan 012).

---

## 中文

### 第一部分 · 科普详解

#### 1.1 问题与意义

哈勃常数（Hubble constant）H0 是宇宙今天的膨胀速率。它可以直接测量：测量近邻星系的距离与退行速度；也可以用宇宙微波背景（CMB, cosmic microwave background）在标准模型 ΛCDM 下预测。直接测量给出约 73 km/s/Mpc，预测约 67–68（Planck 2018：67.4 ± 0.5；SPT-3G + ACT + Planck：67.19 ± 0.38）。如果两者都对，标准模型就缺了什么：这就是"哈勃张力"（Hubble tension）。

直接测量靠距离阶梯（distance ladder）。第一级：几个近邻"锚点"（anchor）的几何距离（银河系造父变星的视差、围绕 NGC 4258 中心黑洞的水脉泽、大麦哲伦云中的食双星）。第二级：造父变星（Cepheid），其周期给出光度，在锚点和曾出现 Ia 型超新星（SN Ia）的星系中都要测量。第三级：平滑哈勃流（Hubble flow）中遥远的 Ia 型超新星，红移给出膨胀速率。

#### 1.2 数据

SH0ES 团队（Riess 等 2022，"R22"）用了 37 个曾出现 42 颗 Ia 型超新星的星系中的造父变星、三个锚点，以及哈勃流中 277 颗 Ia 型超新星（0.0233 < z < 0.15）。全部数据可以写成一个线性方程组 y = L q：约 3500 个星等 y、方程矩阵 L、协方差矩阵（covariance matrix）C 与 47 个未知数 q（每个宿主星系的距离、造父变星的标定项、超新星光度 M_B，以及最后一个 5 log H0）。R22 公开了 y、L 和 C，本项目可以重新拟合。

芝加哥—卡内基哈勃计划（CCHP, Chicago-Carnegie Hubble Program；Freedman 等 2025）在第二级用别的恒星：红巨星支顶端（TRGB, tip of the red giant branch）与碳星（JAGB, J-region asymptotic giant branch）。它用詹姆斯·韦布空间望远镜（JWST）观测了 10 个超新星宿主星系（11 颗 Ia 型超新星），得到较低的数值：全部 24 颗校准超新星给出 70.39 ± 1.22（统计）± 1.33（系统），只用 11 颗 JWST 校准超新星给出 68.81（CSP 超新星）或 69.29（Pantheon+ 超新星）。

#### 1.3 逐步讲解

**第 1 步——SH0ES 的基线。** R22 的拟合给出 H0 = 73.04 ± 1.01，加上 67 个分析变体（analysis variants）的离散后为 ± 1.04（式 10）。只用 NGC 4258 一个锚点给出 72.51 ± 1.54。

**第 2 步——2024 年的更新与 CCHP 子样本（subsample）。** Riess 等 2024 重新推导了 HST 全样本（42 颗超新星，现在有 4 个锚点）：73.2 ± 0.9。然后他们问：如果只保留 CCHP 为 JWST 选的 10 个宿主、只用 NGC 4258 作锚点，同样的 HST 造父变星阶梯给出多少？答案是 71.2，"比 HST 全样本低 2.0 km/s/Mpc——仅仅是由于超新星宿主与锚点的选择"。表中可以把它拆成锚点约 −0.6、宿主约 −1.3。

**第 3 步——同样的宿主、不同的恒星。** 在 CCHP 样本上，JWST 的 JAGB 距离与 HST 造父变星距离相差 0.047 ± 0.066 mag，即在误差内一致；HST 与 JWST 的造父变星相差在百分之几星等以内。

**第 4 步——结论。** CCHP 的 JWST 计划比 HST 全样本低约 2.5 km/s/Mpc。其中约 2.0 单靠宿主与锚点的选择就能预期；剩下约 0.5 远小于 11 颗超新星子样本约 2 km/s/Mpc 的不确定度。所以摘要说，这一差异"完全与样本选择的差异相容"。

粗估：11 颗超新星、每颗约 0.13 mag 的离散，M_B 的不确定度为 0.13/√11 ≈ 0.04 mag，即 H0 约 2%，约 1.4 km/s/Mpc（还未计锚点与造父变星项）——所以不同的 10 个宿主子样本之间相差 2 km/s/Mpc 并不奇怪。

#### 1.4 结论与把握程度

论断是刻意的弱措辞：CCHP 与 SH0ES 的差异与样本选择*相容*，而不是被证明由它造成。它可能错在：(a) 71.2（由 M_B 与一个换算公式在 2024 年数据上得到的近似）在完整拟合中站不住；(b) 同宿主比较掩盖了小样本测不出的真实 TRGB/JAGB 与造父变星的偏差；(c) 选出的宿主很典型，这一移动只是不会重现的涨落（fluctuation）。

### 第二部分 · 论证逻辑

#### 2.0 论证结构

A. 测量：全样本 73.2；SH0ES 阶梯在 CCHP 宿主上 71.2；观测差距约 2.5 →
B. 预期：选这些宿主与锚点使 H0 降低约 2 →
C. 同宿主核对：JAGB 与造父变星的距离在误差内一致 →
D. 剩余约 0.5 在子样本误差之内 ⇒ 差距完全与样本选择相容。

检查方法：论证写成 Lean 4（[`studies/003-m02-hubble-tension-distance-ladder/argument/Argument.lean`](https://github.com/sudoghut/astrolab/blob/main/studies/003-m02-hubble-tension-distance-ladder/argument/Argument.lean)）。每个前提是 `Field` 的一个构造子（不用公理），标注类型与出处性质：

| 标记 | 前提类型 |
|---|---|
| `OBS` | 观测或测量（附表或图） |
| `MOD` | 建模假设 |
| `STAT` | 统计推断（显著性、模型比较） |
| `NUM` | 本项目 `run.py` 重新计算的数值结果 |
| `LIT` | 取自其他文献的结果 |
| `GAP` | 推理需要、但论文和标准知识都没有提供的前提 |

出处性质：`[stated <arXiv 编号>: "引文"]`、`[implied]`（标准知识，注明来源）、`[reconstructed]`（我们补上的；恰好是 `GAP` 前提）。Lean 检查：结论能否推出（`final`）、不是恒真（`final_nontrivial`）、前提相容、没有单个前提单独足够、哪些前提必要，以及明说的（`stated_*`）或加上标准知识的（`explicit_*`）前提是否足够。它不检查前提内部的物理。H0 用十分之一 km/s/Mpc 为单位的整数（73.2 → 732）。

#### 2.1 环节 A–B · 选择造成的移动

| 前提（Lean 构造子） | 类型 | 出处性质 | 论文位置 |
|---|---|---|---|
| `stat_full`：HST 全样本 H0 ≥ 73.1 | STAT | stated 2408.11770："is not yet competitive with the HST set (42 SNe Ia and 4 anchors), which yields 73.2 $\pm$ 0.9" | 摘要 |
| `stat_sel`：CCHP 宿主上的 HST 造父变星 H0 ≤ 71.2 | STAT | stated 2408.11770："a corresponding value of H ${}_{0}=71.2$" | §III.2 |
| `mod_drop`：两者 → 选 CCHP 的宿主与锚点使 H0 降低约 2 | MOD | stated 2408.11770："thus 2.0 $\,\rm km\,s^{-1}\,Mpc^{-1}$ lower than the full HST sample—simply due to the choice of SN hosts and anchor" | §III.2 |

```lean
have d : v.ExpDrop := p .mod_drop (p .stat_full) (p .stat_sel)   -- Sec. III.2
```

**评析。** 71.2 来自 M_B = −19.32 ± 0.05 与论文在 2024 年数据上的换算公式，不是完整的重新拟合；它混合了锚点的改变（约 −0.6）与宿主的改变（约 −1.3）。这正是本项目能用 R22 的矩阵重新计算的（第三部分 R2）。

#### 2.2 环节 C · 同样的宿主、不同的距离指示器

| 前提 | 类型 | 出处性质 | 位置 |
|---|---|---|---|
| `stat_agree`：CCHP 样本上 JAGB 与造父变星的距离一致 | STAT | stated 2408.11770："For comparisons between JWST JAGB and HST Cepheids, we measure a difference with the CCHP JWST sample of $0.047\pm 0.066$ mag" | §III |

**评析。** 在 0.066 mag（距离约 3%）内一致，排除不了百分之几的偏差；这一核对的检验力（power）低，而且只针对 JAGB，不是 TRGB。

#### 2.3 环节 D · 从"预期的移动"到"相容"

| 前提 | 类型 | 出处性质 | 位置 |
|---|---|---|---|
| `stat_gap`：观测的 CCHP 与 HST 之差 ≤ 3.0 | STAT | stated 2408.11770："We show that $\Delta$ H ${}_{0}\sim$ 2.5" | 摘要 |
| `mod_resid`：差约 3 以内且预期降低约 2 → 剩余在约 2 的子样本误差之内 | MOD | implied：差值与其标准误的比较（Taylor 1997） | — |
| `mod_cons`：预期的移动 + 同宿主一致 + 剩余很小 → 相容 | MOD | implied："相容"的含义（没有显著的剩余） | — |

```lean
have r : v.ResidSmall := p .mod_resid (p .stat_gap) d             -- Abstract, Table 4
exact p .mod_cons d (p .stat_agree) r                             -- Abstract
```

**其他解释。**

| 其他解释 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 真实的 TRGB 与造父变星之间百分之几的偏差 | `stat_agree`，只到约 3% | 部分：JAGB 在 0.066 mag 内 |
| CCHP 的宿主本身不寻常，而不是涨落 | 未编码（结论不需要） | 否 |
| 完整重新拟合给出的宿主移动小于 71.2 所示 | `stat_sel`、`mod_drop` | 否（近似） |

#### 2.4 Lean 检查的发现

1. **`explicit_sufficient`**：加上标准知识后链条闭合，没有 `GAP`。原因是结论很弱："完全相容"只要求差距中没有超出误差的显著部分。
2. **`stated_insufficient`**：剩余约 0.5 与子样本不确定度的比较（`mod_resid`），以及由此到"相容"的规则（`mod_cons`），论文没有写出。
3. **每个前提都是必要的**（7 个 `_needed` 定理）：只有一条路径。
4. **薄弱点**（我们的判断）：71.2 是在较新数据上的近似；同宿主一致的检验力低且只针对 JAGB；"相容"不等于"由其造成"。研究（第三部分）直接检验第一点。
5. **局限**：Lean 检查的是我们编码下的结构，不是天体物理。

### 第三部分 · astrolab 能检验或探索的环节

| 环节 / 论断 | 能否检验或探索 | 方法 | 数据（大小） | 判据 | 结果 |
|---|---|---|---|---|---|
| R1 · SH0ES 的基线 | 现在可检验 | 对 R22 的 y、L、C 做广义最小二乘拟合 | C 46.5 MiB（Git LFS 的 FITS），L 0.66 MB，y 17 kB，lstsq 0.7 kB | 主要：复现作者的 `lstsq_results.txt`（47 个参数）；次要：73.04 ± 1.01（容差见 README 第 2 节） | 待定 |
| R2 · 环节 A–B：锚点与宿主的移动 | 现在可检验 | 只用 NGC 4258（去掉其他锚点的几何约束行）重拟，再限于 CCHP 宿主；在 5 log H0 中用精确的线性误差传播 | 同上 | 锚点移动对 R22 的 −0.0158 mag；宿主移动：零假设"无移动"，四种结果的判定表，对该文的 −0.0405 mag（README 第 2 节） | 待定 |
| R3 · 环节 C：同宿主上造父变星对 TRGB | 可探索（默认只作描述） | 与 CCHP 的 JWST TRGB 距离做联合线性估计；先复现 69.29 | CCHP 表 3（论文） | 只有在取数前能写出 CCHP 完整的误差预算时才作检验，否则只作描述 | 待定 |
| R4 · CCHP 的选择是否不寻常 | 可探索（只作描述） | 37 个宿主中随机 10 个的子样本，ΔH0 的百分位 | 同上 | 无——只作探索 | 待定 |
| 跨论文比较 | 可探索（只作描述） | 只对近似独立的组合给出两两之差（距离阶梯对 CMB、TDCOSMO 对其他） | 论文数字 | 无 | 待定 |

### 术语表

| 术语 | 含义 |
|---|---|
| 距离阶梯 | 锚点 → 造父变星（或 TRGB、JAGB）→ Ia 型超新星 → 哈勃流 |
| 锚点 | 有几何距离的星系（银河系视差、NGC 4258 的脉泽、LMC 的食双星） |
| TRGB、JAGB | 红巨星支顶端；J 波段渐近巨星支（碳星） |
| GLS（广义最小二乘） | q̂ = (LᵀC⁻¹L)⁻¹LᵀC⁻¹y |
| 5 log H0 | 阶梯的最后一个参数；拟合对它是线性的，对 H0 不是 |

### 研究进展

- 2026-11-14：第一版：第一至三部分，在实现之前写成（T-012，计划 012）。
