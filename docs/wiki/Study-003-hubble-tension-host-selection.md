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
microwave background (CMB) using the standard model ΛCDM (a cosmological constant Λ plus cold dark matter). The direct route gives about 73
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

The SH0ES team (Supernovae and H0 for the Equation of State of dark energy; Riess et al. 2022, "R22") used Cepheids in 37 galaxies that hosted 42 SNe Ia, three
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
km/s/Mpc lower than the full HST sample — simply due to the choice of SN hosts and anchor". From the rows of the paper's Table 4 (73.17 → 72.54 → 71.2; our arithmetic) this is about −0.6
from the anchor and about −1.3 from the hosts; the text itself quotes ≈ 0.7 for the anchor. The 71.2
comes from M_B = −19.32 ± 0.05 through a simple scaling formula, which the paper says is accurate to
~0.01 mag compared with the full fit.

**Step 3 — same hosts, different stars.** On the CCHP hosts, JWST and HST distances to the same
galaxies agree: JWST near-infrared (NIR) TRGB minus HST Cepheid 0.032 ± 0.056 mag (10 hosts), JAGB minus Cepheid 0.047 ± 0.066 mag (7
hosts), JWST minus HST Cepheids −0.027 ± 0.10 mag (10 hosts); "The HST Cepheid and JWST distance
measurements themselves are in good agreement" (Fig. 5 caption).

**Step 4 — the conclusion.** For each subsample the paper compares the H0 from the JWST distances,
which it recalibrates itself (CCHP's distances taken at face value, H0 from the mean SN luminosity
with Pantheon+ SNe), with the value expected from HST Cepheids on the same supernovae (Table 4), and finds them "consistent with
expectations for every subsample", at or within 1σ of the differential uncertainty (about 1.5–1.8
km/s/Mpc, smaller than the full subsample error because the same SNe are used on both sides).
Hence the abstract: the ~2.5 km/s/Mpc difference between the CCHP JWST program and the full HST
sample "is entirely consistent with differences in sample selection". The ~2.5 appears only in
the abstract; the body never shows which two numbers give it. And the "JWST" values of Table 4 are
the paper's recalibration, not CCHP's own published numbers (CCHP's Pantheon+ TRGB value is 69.29,
Table 4's is 70.1). (Reading the result as "about 2.0 expected from selection plus a small
leftover" is our summary, not the paper's arithmetic.)

Back of the envelope, from the paper (§III.1): 10 CCHP SNe with an intrinsic dispersion of 0.19 mag
give a 1σ uncertainty in H0 of 2.0 km/s/Mpc, so a 2 km/s/Mpc swing between 10-host subsets is not
surprising. The paper also shows (Fig. 6) that about 5% of random 8-SN draws are as low as the CCHP
JAGB subset: unusual, but within what selection can produce.

#### 1.4 What they conclude, and how sure they are

The claim is deliberately weak: the CCHP–SH0ES difference is *consistent with* sample selection,
not proved to be caused by it, and the consistency rests on checks of modest power (distance
agreement to ~0.05–0.10 mag, H0 agreement within ~1.5 km/s/Mpc). It would be wrong if (a) the 71.2
estimate (approximation on 2024 data; subsample errors that exclude the 1.1 km/s/Mpc NGC 4258 term)
does not hold up in a full fit, or (b) the same-host comparison hides a real TRGB/JAGB–Cepheid
offset of a few percent that small samples cannot detect.

### Part 2 · The logic of the argument

#### 2.0 Map of the argument

A. measurements: full sample 73.2; SH0ES ladder on the CCHP hosts 71.2 →
B. expectation: choosing those hosts and anchor lowers H0 by ~2 →
C. same-host check: HST Cepheid and JWST (Cepheid, TRGB, JAGB) distances agree →
D. for every subsample, the JWST H0 (as recalibrated by the paper) is consistent with the HST
expectation (at or within 1σ) →
E. (our GAP) those recalibrated values stand for the CCHP program's own published H0 ⇒ the ~2.5
difference is entirely consistent with sample selection.

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
| `stat_full`: reported full HST sample H0 ≥ 73.2 (central value) | STAT | stated 2408.11770: "is not yet competitive with the HST set (42 SNe Ia and 4 anchors), which yields 73.2 $\pm$ 0.9" | Abstract |
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
| `stat_agree`: on the same hosts HST Cepheid and JWST distances agree | STAT | stated 2408.11770: "The HST Cepheid and JWST distance measurements themselves are in good agreement" | Fig. 5 caption; numbers from §II.3, Table 2 |

**Critique.** Agreement is shown for TRGB (0.032 ± 0.056 mag), JAGB (0.047 ± 0.066 mag) and Cepheids (−0.027 ±
0.10 mag on the CCHP sample), each with uncertainties of 0.05–0.10 mag (≈ 2–5% in distance): a real
offset of a few percent cannot be excluded. The check has low power.

#### 2.3 Stage D · From "within 1σ" to "consistent"

| Premise | Tag | Provenance | Source |
|---|---|---|---|
| `stat_resid`: for every subsample the recalibrated JWST H0 is consistent with the HST expectation | STAT | stated 2408.11770: "we find the values inferred using JWST are consistent with expectations for every subsample" (next sentence: at or within 1σ of these smaller uncertainties) | §III.3, Table 4 |
| `gap_same`: the CCHP JWST program, about which the conclusion speaks, is represented by those recalibrated values | GAP | reconstructed: the paper adopts CCHP's distances "at face-value" and derives H0 itself; CCHP's published values differ (69.29 vs 70.1 for Pantheon+ TRGB) and the paper does not show that the difference is immaterial | — |
| `mod_cons`: expected drop + agreement + within-1σ + same quantity → consistent | MOD | implied: meaning of "consistent" (no significant residual; Taylor 1997) | — |

```lean
exact p .mod_cons d (p .stat_agree) (p .stat_resid) (p .gap_same)  -- Sec. II.3, III.3; GAP
```

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| A real TRGB/JAGB–Cepheid offset of a few percent | `stat_agree`, only to ~0.05–0.10 mag | partly: agreement within those errors |
| The CCHP hosts are an unusual draw | not encoded (the conclusion does not need it) | yes, for the JAGB subset: ~5% of random 8-SN draws are as low (Fig. 6) |
| The full refit gives a smaller host shift than 71.2 suggests | `stat_sel`, `mod_drop` | partly: the approximation is said to be accurate to ~0.01 mag |

#### 2.4 What the Lean check found

1. **`explicit_insufficient`**: even with standard knowledge the chain has one gap, `gap_same`.
   The within-1σ comparisons the paper states are made on its own recalibration of the CCHP
   distances; the conclusion is about the CCHP program's published H0. That the two can be
   exchanged is neither stated nor standard knowledge (CCHP's Pantheon+ TRGB value is 69.29,
   Table 4's 70.1). The countermodel sets `SameQuantity := False`. This repo can probe this step
   (descriptively): R3 reproduces CCHP's 69.29 in R22's framework and compares it with the Cepheid ladder on
   the same hosts.
2. **`stated_insufficient`**: besides the gap, the rule from the facts to "consistent" (`mod_cons`)
   is left implicit; the conclusion itself is weak ("entirely consistent with").
3. **Every premise is needed** (seven `_needed` theorems): a single route. `gap_same` is the only
   reconstructed premise, which is why `explicit_insufficient` hinges on it.
4. **Consistency** (`consistent`) holds trivially: no premise is negative.
5. **Weak points** (ours): the gap above; the 71.2 is an approximation on newer data; "consistent" is backed by
   low-power checks (≈ 0.05–0.10 mag in distance, ≈ 1.5 km/s/Mpc in H0); "consistent with" is not
   "caused by". The study (part 3) tests the first directly.
6. **Limits**: Lean checks the structure under our encoding, not the astrophysics. In particular the
   atoms are uninterpreted: `mod_cons` asserts that the selection shift, the same-host agreement and
   the within-1σ comparison together imply "consistent"; whether the numbers behind those atoms
   really support them is checked by reading the paper and, for the shift, by the study (R2), not by
   Lean.

### Part 3 · What astrolab can test or explore

| Stage / claim | Can we test or explore it? | How | Data (size) | Decision criterion | Result |
|---|---|---|---|---|---|
| R1 · the SH0ES baseline | testable now | GLS fit of R22's y, L, C | C 46.5 MiB (Git LFS FITS), L 0.66 MB, y 17 kB, lstsq 0.7 kB; total about 47.2 MiB (below the 200 MB study budget) | primary: reproduce the authors' `lstsq_results.txt` (47 parameters); secondary: 73.04 ± 1.01 (tolerances in README §2) | pending |
| R2 · stage A–B: anchor and host shifts | testable now | refit with NGC 4258 only (drop the other anchors' geometric rows), then restrict to the CCHP hosts; shifts in 5 log H0 with exact linear error propagation | same | anchor shift vs R22's −0.0158 mag; host shift: null "no shift", four-outcome table vs the paper's −0.0405 mag (README §2) | pending |
| R3 · stages C and E (`gap_same`): same hosts, Cepheid vs TRGB | explorable (descriptive by default) | joint linear estimator with CCHP's JWST TRGB distances; reproduce 69.29 first | CCHP Table 3 (paper) | descriptive unless the full CCHP error budget can be mapped before data; see README §8 | pending |
| R4 · is the CCHP choice unusual? | explorable (descriptive) | random 10-host subsets of the 37 hosts, ΔH0 percentile (the paper did an 8-SN version for JAGB, Fig. 6: ~5%) | same | none — exploration only, see README §8 | pending |
| Cross-paper comparison | explorable (descriptive) | pairwise differences for independent pairs only (ladder vs CMB, TDCOSMO vs others) | paper numbers | none — see README §8 | pending |

### Glossary

| Term | Meaning |
|---|---|
| distance ladder | anchors → Cepheids (or TRGB, JAGB) → SNe Ia → Hubble flow |
| anchor | galaxy with a geometric distance (Milky Way parallaxes, NGC 4258 masers, LMC eclipsing binaries) |
| TRGB, JAGB | tip of the red giant branch; J-region asymptotic giant branch (carbon stars) |
| GLS | generalised least squares: q̂ = (LᵀC⁻¹L)⁻¹LᵀC⁻¹y |
| 5 log H0 | the ladder's last parameter; the fit is linear in it, not in H0 |

### Changelog

- 2026-11-14: first version: parts 1–3, written before implementation (T-012, plan 012); revised after
  gate-1 review (TRGB agreement included; the within-1σ comparison is stated by the paper; Fig. 6;
  GAP `gap_same`: the recalibrated JWST values versus CCHP's published H0, so `explicit_insufficient`).

---

## 中文

### 第一部分 · 科普详解

#### 1.1 问题与意义

哈勃常数（Hubble constant）H0 是宇宙今天的膨胀速率。它可以直接测量：测量近邻星系的距离与退行速度（recession velocity）；也可以用宇宙微波背景（CMB, cosmic microwave background）在标准模型 ΛCDM（宇宙学常数 Λ 加冷暗物质（cold dark matter））下预测。直接测量给出约 73 km/s/Mpc，预测约 67–68（Planck 2018：67.4 ± 0.5；SPT-3G + ACT + Planck：67.19 ± 0.38）。如果两者都对，标准模型就缺了什么：这就是"哈勃张力"（Hubble tension）。

直接测量靠距离阶梯（distance ladder）。第一级：几个近邻"锚点"（anchor）的几何距离（geometric distance）（银河系造父变星的视差、围绕 NGC 4258 中心黑洞的水脉泽、大麦哲伦云中的食双星）。第二级：造父变星（Cepheid），其周期给出光度，在锚点和曾出现 Ia 型超新星（SN Ia）的星系中都要测量。第三级：平滑哈勃流（Hubble flow）中遥远的 Ia 型超新星，红移给出膨胀速率。

#### 1.2 数据

SH0ES（Supernovae and H0 for the Equation of State of dark energy）团队（Riess 等 2022，"R22"）用了 37 个曾出现 42 颗 Ia 型超新星的星系中的造父变星、三个锚点，以及哈勃流中 277 颗 Ia 型超新星（0.0233 < z < 0.15）。全部数据可以写成一个线性方程组 y = L q：约 3500 个星等 y、方程矩阵（design matrix）L、协方差矩阵（covariance matrix）C 与 47 个未知数 q（每个宿主星系（host galaxy）的距离、造父变星的标定项、超新星光度 M_B，以及最后一个 5 log H0）。R22 公开了 y、L 和 C，本项目可以重新拟合。

芝加哥—卡内基哈勃计划（CCHP, Chicago-Carnegie Hubble Program；Freedman 等 2025）在第二级用别的恒星：红巨星支顶端（TRGB, tip of the red giant branch）与碳星（JAGB, J-region asymptotic giant branch）。它用詹姆斯·韦布空间望远镜（JWST）观测了 10 个超新星宿主星系（11 颗 Ia 型超新星），得到较低的数值：全部 24 颗校准超新星给出 70.39 ± 1.22（统计）± 1.33（系统），只用 11 颗 JWST 校准超新星给出 68.81（CSP 超新星）或 69.29（Pantheon+ 超新星）。

#### 1.3 逐步讲解

**第 1 步——SH0ES 的基线。** R22 的拟合给出 H0 = 73.04 ± 1.01，加上 67 个分析变体（analysis variants）的离散后为 ± 1.04（式 10）。只用 NGC 4258 一个锚点给出 72.51 ± 1.54。

**第 2 步——2024 年的更新与 CCHP 子样本（subsample）。** Riess 等 2024 重新推导了 HST 全样本（42 颗超新星，现在有 4 个锚点）：73.2 ± 0.9。然后他们问：如果只保留 CCHP 为 JWST 选的 10 个宿主、只用 NGC 4258 作锚点，同样的 HST 造父变星阶梯给出多少？答案是 71.2，"比 HST 全样本低 2.0 km/s/Mpc——仅仅是由于超新星宿主与锚点的选择"。按论文表 4 的各行（73.17 → 72.54 → 71.2；我们的算术）可以拆成锚点约 −0.6、宿主约 −1.3；正文给出锚点约 0.7。71.2 由 M_B = −19.32 ± 0.05 经一个简单的换算公式得到，论文说它与完整拟合相比准确到约 0.01 mag。

**第 3 步——同样的宿主、不同的恒星。** 在 CCHP 的宿主上，JWST 与 HST 对同一批星系的距离一致：JWST 近红外（near-infrared, NIR）TRGB 减 HST 造父变星 0.032 ± 0.056 mag（10 个宿主），JAGB 减造父变星 0.047 ± 0.066 mag（7 个宿主），JWST 减 HST 造父变星 −0.027 ± 0.10 mag（10 个宿主）；"HST 造父变星与 JWST 的距离测量本身良好一致"（图 5 说明）。

**第 4 步——结论。** 论文对每个子样本比较由 JWST 距离得到的 H0（由论文自己重新标定：CCHP 的距离按原值采用，H0 由 Pantheon+ 超新星的平均光度换算）与在同样超新星上由 HST 造父变星预期的数值（表 4），发现"对每个子样本都与预期相容"，在差分不确定度（differential uncertainty，约 1.5–1.8 km/s/Mpc，因两边用同样的超新星而小于子样本的总误差）的 1σ 以内。所以摘要说，CCHP 的 JWST 计划与 HST 全样本约 2.5 km/s/Mpc 的差异"完全与样本选择的差异相容"。"约 2.5"只出现在摘要里，正文没有说明由哪两个数得到。而且表 4 中的"JWST"数值是论文的重新标定，不是 CCHP 自己发表的数值（CCHP 的 Pantheon+ TRGB 为 69.29，表 4 为 70.1）。（"约 2.0 由选择预期、剩下一小部分"是我们的概括，不是论文的算术。）

粗估，取自论文（§III.1）：CCHP 的 10 颗超新星、内禀离散（intrinsic dispersion）0.19 mag，给出 H0 的 1σ 不确定度 2.0 km/s/Mpc，所以不同的 10 个宿主子样本之间相差 2 km/s/Mpc 并不奇怪。论文还表明（图 6）随机抽 8 颗超新星时约 5% 与 CCHP 的 JAGB 子样本一样低：不寻常，但在选择能造成的范围内。

#### 1.4 结论与把握程度

论断是刻意的弱措辞：CCHP 与 SH0ES 的差异与样本选择*相容*，而不是被证明由它造成，而且"相容"依靠的是检验力不高的核对（距离一致到约 0.05–0.10 mag，H0 一致到约 1.5 km/s/Mpc）。它可能错在：(a) 71.2（2024 年数据上的近似；子样本误差不含 NGC 4258 的 1.1 km/s/Mpc）在完整拟合中站不住；(b) 同宿主比较掩盖了小样本测不出的、百分之几的真实 TRGB/JAGB 与造父变星的偏差。

### 第二部分 · 论证逻辑

#### 2.0 论证结构

A. 测量：全样本 73.2；SH0ES 阶梯在 CCHP 宿主上 71.2 →
B. 预期：选这些宿主与锚点使 H0 降低约 2 →
C. 同宿主核对：HST 造父变星与 JWST（造父变星、TRGB、JAGB）的距离一致 →
D. 对每个子样本，JWST 的 H0（论文重新标定）与 HST 预期相容（在 1σ 以内）→
E. （我们补上的 GAP）这些重新标定的数值代表 CCHP 计划自己发表的 H0 ⇒ 约 2.5 的差异完全与样本选择相容。

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
| `stat_full`：HST 全样本报告的 H0 ≥ 73.2（中心值） | STAT | stated 2408.11770："is not yet competitive with the HST set (42 SNe Ia and 4 anchors), which yields 73.2 $\pm$ 0.9" | 摘要 |
| `stat_sel`：CCHP 宿主上的 HST 造父变星 H0 ≤ 71.2 | STAT | stated 2408.11770："a corresponding value of H ${}_{0}=71.2$" | §III.2 |
| `mod_drop`：两者 → 选 CCHP 的宿主与锚点使 H0 降低约 2 | MOD | stated 2408.11770："thus 2.0 $\,\rm km\,s^{-1}\,Mpc^{-1}$ lower than the full HST sample—simply due to the choice of SN hosts and anchor" | §III.2 |

```lean
have d : v.ExpDrop := p .mod_drop (p .stat_full) (p .stat_sel)   -- Sec. III.2
```

**评析。** 71.2 来自 M_B = −19.32 ± 0.05 与论文在 2024 年数据上的换算公式，不是完整的重新拟合；它混合了锚点的改变（约 −0.6）与宿主的改变（约 −1.3）。这正是本项目能用 R22 的矩阵重新计算的（第三部分 R2）。

#### 2.2 环节 C · 同样的宿主、不同的距离指示器

| 前提 | 类型 | 出处性质 | 位置 |
|---|---|---|---|
| `stat_agree`：同样的宿主上 HST 造父变星与 JWST 的距离一致 | STAT | stated 2408.11770："The HST Cepheid and JWST distance measurements themselves are in good agreement" | 图 5 说明；数字见 §II.3、表 2 |

**评析。** 一致性对 TRGB（0.032 ± 0.056 mag）、JAGB（0.047 ± 0.066 mag）与造父变星（CCHP 样本上 −0.027 ± 0.10 mag）都有展示，误差都在 0.05–0.10 mag（距离约 2–5%）：排除不了百分之几的真实偏差。这一核对的检验力（power）低。

#### 2.3 环节 D · 从"1σ 以内"到"相容"

| 前提 | 类型 | 出处性质 | 位置 |
|---|---|---|---|
| `stat_resid`：对每个子样本，重新标定的 JWST H0 与 HST 预期相容 | STAT | stated 2408.11770："we find the values inferred using JWST are consistent with expectations for every subsample"（下一句：在这些较小误差的 1σ 以内） | §III.3，表 4 |
| `gap_same`：结论所说的 CCHP JWST 计划由这些重新标定的数值代表 | GAP | reconstructed：论文按原值采用 CCHP 的距离并自己推出 H0；CCHP 发表的数值不同（Pantheon+ TRGB 69.29 对 70.1），论文没有说明这一差别无关紧要 | — |
| `mod_cons`：预期的移动 + 一致 + 1σ 以内 + 同一个量 → 相容 | MOD | implied："相容"的含义（没有显著的剩余；Taylor 1997） | — |

```lean
exact p .mod_cons d (p .stat_agree) (p .stat_resid) (p .gap_same)  -- Sec. II.3, III.3; GAP
```

**其他解释。**

| 其他解释 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 真实的 TRGB/JAGB 与造父变星之间百分之几的偏差 | `stat_agree`，只到约 0.05–0.10 mag | 部分：在这些误差内一致 |
| CCHP 的宿主是一次不寻常的抽样 | 未编码（结论不需要） | 是，针对 JAGB 子样本：随机 8 颗超新星约 5% 一样低（图 6） |
| 完整重新拟合给出的宿主移动小于 71.2 所示 | `stat_sel`、`mod_drop` | 部分：论文说近似准确到约 0.01 mag |

#### 2.4 Lean 检查的发现

1. **`explicit_insufficient`**：即使加上标准知识，链条仍有一处缺口 `gap_same`。论文写明的 1σ 以内的比较，是在它自己对 CCHP 距离的重新标定上做的；而结论针对的是 CCHP 计划发表的 H0。两者可以互换，论文没有写，也不是标准知识（CCHP 的 Pantheon+ TRGB 为 69.29，表 4 为 70.1）。反例模型令 `SameQuantity := False`。本项目可以（描述性地）探索这一步：R3 在 R22 的框架内复现 CCHP 的 69.29，并与同一批宿主上的造父变星阶梯比较。
2. **`stated_insufficient`**：除了这一缺口，由这些事实到"相容"的规则（`mod_cons`）也没有写出；结论本身很弱（"完全相容"）。
3. **每个前提都是必要的**（7 个 `_needed` 定理）：只有一条路径。`gap_same` 是唯一的补上前提，所以 `explicit_insufficient` 取决于它。
4. **相容性**（`consistent`）是平凡成立的：没有否定形式的前提。
5. **薄弱点**（我们的判断）：上述缺口；71.2 是在较新数据上的近似；"相容"依靠检验力不高的核对（距离约 0.05–0.10 mag，H0 约 1.5 km/s/Mpc）；"相容"不等于"由其造成"。研究（第三部分）直接检验第一点。
6. **局限**：Lean 检查的是我们编码下的结构，不是天体物理。特别是原子没有解释：`mod_cons` 断言选择造成的移动、同宿主的一致与 1σ 以内的比较合起来推出"相容"；这些原子背后的数字是否真的支持它们，由阅读论文以及（对移动量而言）研究的 R2 来检查，而不是 Lean。

### 第三部分 · astrolab 能检验或探索的环节

| 环节 / 论断 | 能否检验或探索 | 方法 | 数据（大小） | 判据 | 结果 |
|---|---|---|---|---|---|
| R1 · SH0ES 的基线 | 现在可检验 | 对 R22 的 y、L、C 做广义最小二乘（GLS, generalised least squares）拟合 | C 46.5 MiB（Git LFS 的 FITS），L 0.66 MB，y 17 kB，lstsq 0.7 kB；合计约 47.2 MiB（低于研究预算 200 MB） | 主要：复现作者的 `lstsq_results.txt`（47 个参数）；次要：73.04 ± 1.01（容差见 README 第 2 节） | 待定 |
| R2 · 环节 A–B：锚点与宿主的移动 | 现在可检验 | 只用 NGC 4258（去掉其他锚点的几何约束行）重拟，再限于 CCHP 宿主；在 5 log H0 中用精确的线性误差传播 | 同上 | 锚点移动对 R22 的 −0.0158 mag；宿主移动：零假设（null hypothesis）"无移动"，四种结果的判定表，对该文的 −0.0405 mag（README 第 2 节） | 待定 |
| R3 · 环节 C 与 E（`gap_same`）：同宿主上造父变星对 TRGB | 可探索（默认只作描述） | 与 CCHP 的 JWST TRGB 距离做联合线性估计；先复现 69.29 | CCHP 表 3（论文） | 只有在取数前能写出 CCHP 完整的误差预算时才作检验，否则只作描述；见 README 第 8 节 | 待定 |
| R4 · CCHP 的选择是否不寻常 | 可探索（只作描述） | 37 个宿主中随机 10 个的子样本，ΔH0 的百分位（percentile）（论文对 JAGB 做过 8 颗超新星的版本，图 6：约 5%） | 同上 | 无——只作探索，见 README 第 8 节 | 待定 |
| 跨论文比较 | 可探索（只作描述） | 只对近似独立的组合给出两两之差（距离阶梯对 CMB、TDCOSMO 对其他） | 论文数字 | 无——见 README 第 8 节 | 待定 |

### 术语表

| 术语 | 含义 |
|---|---|
| 距离阶梯 | 锚点 → 造父变星（或 TRGB、JAGB）→ Ia 型超新星 → 哈勃流 |
| 锚点 | 有几何距离的星系（银河系视差、NGC 4258 的脉泽、LMC 的食双星） |
| TRGB、JAGB | 红巨星支顶端；J 波段渐近巨星支（碳星） |
| GLS（广义最小二乘） | q̂ = (LᵀC⁻¹L)⁻¹LᵀC⁻¹y |
| 5 log H0 | 阶梯的最后一个参数；拟合对它是线性的，对 H0 不是 |

### 研究进展

- 2026-11-14：第一版：第一至三部分，在实现之前写成（T-012，计划 012）；按闸门 1 审查修订（补上 TRGB 的一致性；1σ 以内的比较论文自己写明；图 6；GAP `gap_same`：重新标定的 JWST 数值与 CCHP 发表的 H0，因而 `explicit_insufficient`）。
