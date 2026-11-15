# Has the S8 tension eased? DES Y6 against the CMB

[English](#english) · [中文](#中文)

*Paper: DES Collaboration (T. M. C. Abbott et al.) 2026, "Dark Energy Survey Year 6 Results: Cosmological Constraints from Galaxy Clustering and Weak Lensing", arXiv:2601.14559 (v2; accepted in PRD). Study:
[`studies/008-m03-s8-des-y6-cmb-parameter-difference`](https://github.com/sudoghut/astrolab/tree/main/studies/008-m03-s8-des-y6-cmb-parameter-difference).
Status: planned. Last updated: 2026-11-15 (see the changelog at the end). The source of this page lives in the main repository at
[`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki); edit it there.*

*中文标题：S8 张力减弱了吗？DES Y6 与 CMB 的比较。状态：计划中。论文：DES Collaboration（T. M. C. Abbott 等）2026，arXiv:2601.14559（v2，已被 PRD 接收）。研究：[`studies/008-m03-s8-des-y6-cmb-parameter-difference`](https://github.com/sudoghut/astrolab/tree/main/studies/008-m03-s8-des-y6-cmb-parameter-difference)。最后更新：2026-11-15（见文末"研究进展"）。本页源文件在主仓库的 [`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki) 中，请在那里修改。*

---

## English

### Part 1 · The paper in plain language

#### 1.1 The question and why it matters

How lumpy is the matter in the Universe today? Cosmologists measure this with one number,
**S8 = σ8 (Ωm/0.3)^0.5**. Here σ8 is the typical size of density fluctuations on scales of about
8 h⁻¹ Mpc (roughly 11 Mpc), and Ωm is the fraction of the Universe's energy density in matter. The
square-root combination is used because weak gravitational lensing, the main low-redshift probe,
measures almost exactly this combination.

There are two ways to get S8:

- **Predict it from the early Universe.** The cosmic microwave background (CMB) shows the
  Universe 380,000 years after the Big Bang. Fitting the standard model (ΛCDM: a cosmological
  constant plus cold dark matter) to the CMB fixes all six model parameters, and the model then
  predicts how much structure should have grown by today.
- **Measure it today.** Surveys of hundreds of millions of galaxies measure how light from distant
  galaxies is bent by the matter in between (weak lensing), and how galaxies cluster.

For about a decade, lensing surveys found S8 a few percent lower than the CMB predicts, at 2–3
standard deviations (σ). This is the **S8 tension**. If real, it would mean ΛCDM is missing
something (for example dark matter that interacts, or massive neutrinos behaving unexpectedly). If
not, it is a statistical fluctuation or a subtle systematic error. Recent results have tended to
come out closer to the CMB, and people have started to say the tension is "easing". This study
asks how far that statement holds for the newest Dark Energy Survey (DES) result.

#### 1.2 The data

DES imaged about 5,000 square degrees of the southern sky with the Dark Energy Camera on the 4-m
Blanco telescope in Chile, over six years (Y6 is the full survey). D26 combines three measurements,
called **3x2pt** because each is a two-point correlation function (a measurement of how two
quantities co-vary with angular separation):

1. **Cosmic shear (ξ±):** the shapes of more than a hundred million background galaxies are slightly
   stretched by lensing; the correlation of these distortions measures the projected matter.
2. **Galaxy–galaxy lensing (γt):** the stretching of background galaxies around foreground
   ("lens") galaxies, which measures the matter around those galaxies.
3. **Galaxy clustering (w(θ)):** how lens galaxies cluster with each other.

The CMB comparison is a combination of three experiments' temperature and polarization power
spectra: Planck 2018 (ℓ from 2 to 1000 in TT, 30 to 600 in TE and EE, plus low-ℓ EE), ACT DR6
(ℓ 600–8500) and SPT-3G DR1 (TT 400–3000, TE/EE 400–4000). ℓ is the multipole number: a higher ℓ
means smaller angular scales. DES deliberately leaves out CMB lensing, which would not be
independent of DES's own lensing.

#### 1.3 Step by step: how the authors got from data to conclusion

**Step 1 · The DES measurement.** DES fits ΛCDM to the 3x2pt data (with lens bin 2 removed after
pre-agreed unblinding tests failed). The analysis was blinded: the authors could not see the
cosmological results until the pipeline was fixed. The fiducial result (Sec. V.1, eq. 21) is
S8 = 0.789 ± 0.012 and Ωm = 0.333 (+0.023/−0.028). D26 reports the posterior **mean** with a 68%
credible interval, and the maximum a posteriori (MAP) value in parentheses (0.793 for S8).

**Step 2 · The CMB prediction.** Running the same model on the CMB combination gives
S8 = 0.836 (+0.012/−0.013) (Table 4).

**Step 3 · Back of the envelope.** The two S8 values differ by 0.836 − 0.789 = 0.047. If both
were Gaussian and independent, the uncertainty of the difference would be
√(0.012² + 0.0125²) ≈ 0.017, so the difference is about 0.047/0.017 ≈ **2.7σ**.

**Step 4 · The proper metric.** D26 does not use the back-of-envelope number. It uses the
**parameter-difference probability** (Sec. IV.6; Raveri & Hu 2019; Raveri & Doux 2021):

- the distribution of the difference Δp between two independent posteriors is the
  cross-correlation integral P(Δp) = ∫ P(p|A) P(p − Δp|B) dp (eq. 17);
- Δ is the probability mass of P(Δp) inside the contour of equal density that passes through
  Δp = 0, the point of no shift (eq. 18);
- Δ is turned into an "effective number of σ", n_σ = √2 erf⁻¹(Δ) (eq. 19): the number of standard
  deviations a Gaussian event with the same probability would have.

In many dimensions DES estimates the densities with **normalizing flows** (a machine-learning
density estimator) in the tensiometer code.

**Step 5 · The numbers.** DES compares the two posteriors in the S8 direction (1-D), in the
S8–Ωm plane (2-D), and in the full parameter space, and finds **2.6σ, 2.2σ and 1.8σ** (Sec. V.2;
Table 6). The S8 direction is the one 3x2pt measures best, so a separation shows up most
clearly there. Against Planck 2018 alone the full-space difference is 1.0σ (DES Y3: 1.5σ).
The 2-D difference against Planck alone fell from 1.9σ (Y3) to 1.4σ (Y6), but rose to 2.2σ
against the combined CMB, because the combined CMB is tighter and prefers a slightly higher S8.

**Step 6 · The decision rule.** D26 sets n_σ < 3 as "the criterion for different data sets
agreeing well enough that it makes sense to examine their combined constraint" (Sec. IV.6). All
three numbers are below 3, so DES goes on to combine with the CMB.

**Step 7 · Checks on the DES posterior.** In many dimensions, marginal means can be pulled away
from the truth by the shape of the prior ("prior-volume" or projection effects). DES ran its
pipeline on a noiseless simulated data vector at its best-fit point and measured the shift
(truth − mean)/σ (App. B, Table 9): +0.17 for S8 in the fiducial analysis, below 0.5σ for all
parameters of interest.

**Step 8 · Other probes.** In Sec. VII.3 DES compares itself with KiDS-Legacy cosmic shear
(S8 = 0.815 +0.016/−0.021) and finds them consistent with its own cosmic shear
(0.783 +0.019/−0.015). It quotes HSC Y3 as 0.804 ± 0.051. That number does not appear in the
paper DES cites (Zhang et al. 2025, arXiv:2507.01386, which gives 0.780 +0.029/−0.030); we use
the cited paper directly.

#### 1.4 What they conclude, and how sure they are

- **Conclusion (Sec. VIII):** "we see no substantial evidence for a discrepancy with the CMB in
  either S8 or the full parameter space", with significances across weak-lensing experiments from
  about 1σ to at most 3σ. DES also notes that the field is "in a similar place as it was in
  previous years": D26 does not say the tension has gone away.
- **Strength:** the 1.8σ full-space number is free of any choice of direction; the 2.6σ is in the
  direction DES chose a priori as its best-measured one.
- **What would make them wrong:**
  - the metric or its numerical estimate could be off (the normalizing-flow estimate has noise
    that D26 does not quote);
  - an unrecognised systematic could shift DES S8 (lens bin 2 already had to be dropped);
  - "below 3σ" may not mean "no evidence": 2.6σ corresponds to a chance probability of about
    1%, which many would call mild evidence. The rule D26 states is a criterion for combining, not
    a statement about evidence.

### Part 2 · The logic of the argument

#### 2.0 Map of the argument

A. The reference: the primary CMB combination (no lensing).
B. The measure: the parameter-difference probability, converted to n_σ.
C. The numbers: 1.8σ (full space) and 2.6σ (S8), with small projection effects.
D. The rule: below 3σ, the data sets agree well enough to combine.
E. [gap] Combinable, with the S8 projection also below 3σ ⇒ no substantial evidence for a
discrepancy.
⇒ No substantial evidence for a discrepancy with the CMB.

How we check it: the argument is written in Lean 4
([`studies/008-m03-s8-des-y6-cmb-parameter-difference/argument/Argument.lean`](https://github.com/sudoghut/astrolab/blob/main/studies/008-m03-s8-des-y6-cmb-parameter-difference/argument/Argument.lean)).
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

Provenance: `[stated: "quote"]` (the paper says it, quoted), `[implied]` (standard knowledge the
paper relies on without writing it out, with a source), `[reconstructed]` (our addition; exactly
the `GAP` premises).

What Lean checks: that the conclusion follows from these premises (`final`) and is not trivially
true (`final_nontrivial`); that the premises can hold together (`consistent`); that no single
premise gives the conclusion alone (`alone_insufficient`); for each premise, whether it is needed
(a countermodel without it) or redundant; and whether the premises the paper actually states are
enough (`stated_*`), and whether they are enough once standard knowledge is added (`explicit_*`;
`explicit_insufficient` means a real gap). What Lean does not check: the physics inside each
premise — that is what parts 1 and 3 and the study are for.

Numbers are encoded in tenths of a σ as natural numbers; "at most 18 tenths" is no stronger than
the reported, rounded "1.8".

#### 2.1 Stage A · Reference and measure

**Overview.** The comparison needs a fixed reference (which CMB) and a fixed way of turning two
posteriors into one number.

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `obs_cmb`: the CMB reference is Planck 2018 + ACT-DR6 + SPT-3G DR1 primary TT/TE/EE, no CMB lensing | OBS | stated: "for primary temperature and polarization data, but without CMB lensing" | §V.2 |
| `mod_metric`: consistency is measured by the parameter-difference probability | MOD | stated: "We measure consistency from the probability of a parameter difference" | §IV.6, eqs. 17–19 |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| A different CMB reference (Planck alone) gives a different answer (1.0σ) | `obs_cmb` fixes the reference | yes, both are reported (§V.2) |
| A different metric (Gaussian difference, Bayes-factor or evidence ratio) gives a different number | `mod_metric` | no; D26 uses one metric |

**Critique.** The reference matters: against Planck alone the full-space number is 1.0σ, against
the combination 1.8σ. The conclusion is about "the CMB" in the sense of the combination.

#### 2.2 Stage B · The numbers and their reliability

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `stat_full`: full-space difference at most 1.8σ | STAT | stated: "we find a full parameter space difference of 1.8" | §VIII (also §V.2, Table 6) |
| `stat_s8`: difference projected onto S8 at most 2.6σ | STAT | stated: "the difference increases to 2.6" | §VIII (also §V.2) |
| `stat_proj`: projection effects below 0.5σ | STAT | stated: "exhibits minor prior-volume effects of less than" | App. B |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| Prior-volume effects shift the DES mean enough to change the numbers | `stat_proj` | yes (App. B, Table 9: +0.17 in S8) |
| The normalizing-flow estimate is noisy | none | no; the numerical error is not quoted |

**Critique.** These are the numbers our study can recompute (part 3). The 2.6σ is in a direction
chosen before the comparison (the best-measured one), so a trials correction is arguable either
way; the 1.8σ full-space number needs none.

#### 2.3 Stage C · From the numbers to the conclusion

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `mod_crit`: below 3σ (full space), the data sets agree well enough to combine | MOD | stated: "as the criterion for different data sets agreeing well enough that it makes sense to examine their combined constraint" | §IV.6 |
| `gap_bridge`: with the reference and metric above, combinable data sets whose S8 projection is also below 3σ and whose projection effects are small show no substantial evidence for a discrepancy | GAP | reconstructed | — |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| 2.6σ (chance probability about 1%) is mild evidence for a discrepancy, even if combining is allowed | `gap_bridge` | no |

**Inference (Lean excerpt).**

```lean
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  have hfull : v.n_full_x10 ≤ 18 := p .stat_full          -- Sec. V.2, VIII: 1.8 sigma
  have hs8 : v.n_s8_x10 ≤ 26 := p .stat_s8                -- Sec. V.2, VIII: 2.6 sigma
  have hcomb : v.Combinable := p .mod_crit (by omega)     -- Sec. IV.6: below 3, combinable
  exact p .gap_bridge (p .obs_cmb) (p .mod_metric) hcomb (by omega) (p .stat_proj)  -- GAP
```

**Critique.** D26 uses its criterion only to justify combining ("As such, we are able to
combine", §V.2). The "no substantial evidence" sentence in §VIII cites a range of significances
across experiments, not the criterion. The step between the two is ours.

#### 2.4 What the Lean check found

1. **Headline: `explicit_insufficient`.** Even with standard statistical knowledge, the
   premises do not give the conclusion without `gap_bridge`. A sub-3σ difference is a convention
   for combining data, not a theorem that no discrepancy exists. `stated_insufficient` holds for
   the same reason. No `[implied]` premise was needed.
2. **Every premise is needed** in this encoding (seven `_needed` theorems); none is redundant.
   With uninterpreted atoms, "needed" means "used by this encoding": for example `stat_proj` is
   needed because we put small projection effects into the bridge.
3. **Where the conclusion is fragile.** It depends on the threshold. All reported numbers are
   below 3σ, so it survives any of D26's three projections, but with a threshold of 2.5σ the S8
   projection would fail. It also depends on the reference (Planck alone gives 1.0σ) and on the
   accuracy of the numerical estimate, which D26 does not quote.
4. **Consistency** (`consistent`) is a weak check here: no premise is negative.
5. **Limits:** Lean checks the logical structure under our encoding, not the statistics inside
   each premise. Whether 2.6σ is "substantial" is a judgement; the machine check only shows that
   the paper does not supply a rule for it.

### Part 3 · What astrolab can test or explore

The fiducial DES 3x2pt chain is 144 MB, above this project's 50 MB per-download limit; the user
approved a one-off download of this single file (2026-11-15). The CMB chain (11.8 MB) and the
cosmic-shear chain (14.9 MB) are under the limit. Other probes enter only as published summaries.

| Stage / claim | Can we test or explore it? | How | Data (size) | Decision criterion | Result |
|---|---|---|---|---|---|
| Inputs: the S8 means of the CMB (0.836 +0.012/−0.013), DES 3x2pt (0.789 ± 0.012) and DES cosmic shear (0.783 +0.019/−0.015) (R1) | testable now | weighted mean and 68% interval from each public chain | DES chains: 144 + 11.8 + 14.9 MB | each mean within a pre-registered tolerance of the published value | pending |
| Stage B: 2.6σ (S8) and 2.2σ (S8–Ωm) (R2) | testable now | eqs. 17–19 from the two chains: weighted independent draws, pairwise differences, one kernel density estimate evaluated at the differences and at zero (split halves), n_σ = √2 erf⁻¹(Δ); convergence and bandwidth diagnostics fixed in advance | same | reproduced if within the pre-registered tolerance (Monte Carlo error plus a stated allowance) | pending |
| Stage B: 1.8σ (full space) | explorable (not decisive) | Gaussian approximation over the shared parameters, with and without the directions dominated by the prior; no normalizing flows | same | none - exploration only | pending |
| DES cosmic shear against the CMB (R3) | testable now (if R1 confirms the chain) | as R2, chain against chain | same | none unless D26 quotes a number - descriptive | pending |
| Stage B: projection effects; Stage C: threshold and metric (R4) | explorable (not decisive) | shift DES by +0.17σ (Table 9) or use the MAP; compare iso-density, equal-tail and Gaussian versions of the same 1-D comparison; report where the threshold flips the classification | same | none - exploration only | pending |
| Other probes against the CMB (R5) | explorable (not decisive) | each published S8 summary (split-normal) against the CMB chain; no averaging (probes are correlated and constrain different directions) | published values (kB) | none - descriptive | pending |
| `gap_bridge` (is below 3σ "no evidence"?) | out of scope | a judgement about evidence, not a computation; the study reports the numbers that feed it | – | – | – |
| DES systematics, blinding, the flow estimator itself | out of scope | needs the data vectors, simulations and the analysis pipeline | – | – | – |

### Glossary

| Term | Meaning |
|---|---|
| S8 | σ8 (Ωm/0.3)^0.5: the amplitude of matter clustering, in the combination weak lensing measures best |
| σ8 | rms amplitude of linear matter fluctuations in spheres of 8 h⁻¹ Mpc today |
| Ωm | matter density as a fraction of the critical density |
| 3x2pt | the joint analysis of cosmic shear, galaxy–galaxy lensing and galaxy clustering |
| parameter-difference probability | probability mass of the distribution of the difference of two posteriors inside the iso-density contour through zero shift |
| n_σ | √2 erf⁻¹(Δ): the Gaussian-equivalent number of standard deviations of a probability Δ |
| normalizing flow | a neural-network density estimator used to evaluate posterior densities in many dimensions |
| prior-volume (projection) effect | a shift of marginal means caused by the prior volume of the other parameters, not by the data |
| MAP | maximum a posteriori: the parameter values with the highest posterior density |
| blinding | hiding the cosmological results from the analysts until the analysis choices are fixed |

### Open questions

- Is the full-space 1.8σ reproducible without normalizing flows (it would need the flow
  machinery, a separate installation)?
- How much do the published S8 values of other probes move when re-analysed with matched choices
  (D26 §VII.3 plots published chains, not a matched re-analysis)?

### Changelog

Newest first.

- 2026-11-15: first version: parts 1–3 (pre-registration source; plan `design/017-plan_*`).

### Sources

- DES Collaboration 2026, arXiv:2601.14559 (v2), the paper studied.
- Raveri & Hu 2019, PRD 99, 043506; Raveri & Doux 2021, arXiv:2105.03324: the parameter-difference metric.
- Wright et al. 2025, A&A 703, A158, arXiv:2503.19441 (KiDS-Legacy).
- Zhang et al. 2025, arXiv:2507.01386 (HSC Y3, the reference cited by D26 for HSC).
- Madhavacheril et al. 2024, ApJ 962, 113, arXiv:2304.05203 (ACT DR6 lensing).
- Ghirardini et al. 2024, A&A 689, A298, arXiv:2402.08458 (eROSITA clusters).
- DES Y3: arXiv:2105.13549; KiDS-1000: arXiv:2007.15632, arXiv:2007.15633 (previous generation).

---

## 中文

### 第一部分 · 科普详解

#### 1.1 问题与意义

今天宇宙中的物质有多"成团"？宇宙学家用一个数来衡量：**S8 = σ8 (Ωm/0.3)^0.5**。σ8 是约 8 h⁻¹ Mpc（约 11 Mpc）尺度上密度涨落的典型幅度，Ωm 是物质在宇宙能量密度中所占的比例。之所以用这种平方根组合，是因为低红移的主要探针弱引力透镜（weak gravitational lensing）几乎正好测量这个组合。

得到 S8 有两种途径：

- **由早期宇宙预言。** 宇宙微波背景（CMB, cosmic microwave background）是大爆炸后 38 万年的宇宙。用标准模型（ΛCDM：宇宙学常数加冷暗物质）拟合 CMB 可以定下全部六个模型参数，模型随即预言到今天结构应长到多大。
- **在今天测量。** 对数亿个星系的巡天测量远处星系的光被中间物质偏折的程度（弱透镜），以及星系如何成团。

大约十年来，透镜巡天得到的 S8 比 CMB 的预言低百分之几，相差 2–3 个标准差（σ）。这就是 **S8 张力（S8 tension）**。如果它是真的，说明 ΛCDM 漏掉了什么（例如有相互作用的暗物质、行为出乎意料的中微子）；如果不是，就是统计涨落或微妙的系统误差。近来的结果更接近 CMB，人们开始说张力在"减弱"。本研究要问：对最新的暗能量巡天（DES, Dark Energy Survey）结果，这种说法在多大程度上成立。

#### 1.2 数据

DES 用智利 4 米 Blanco 望远镜上的暗能量相机，六年间拍摄了约 5000 平方度的南天（Y6 是完整巡天）。D26 联合三种测量，因为每一种都是两点相关函数（two-point correlation function，即两个量随角距离的协变），所以叫 **3x2pt**：

1. **宇宙剪切（cosmic shear，ξ±）：** 上亿个背景星系的形状被透镜轻微拉伸；这些畸变的相关性测量投影的物质分布。
2. **星系–星系透镜（galaxy–galaxy lensing，γt）：** 前景（"透镜"）星系周围背景星系的拉伸，测量这些星系周围的物质。
3. **星系成团（galaxy clustering，w(θ)）：** 透镜星系彼此之间如何成团。

用来比较的 CMB 是三个实验温度与偏振功率谱的组合：Planck 2018（TT 的 ℓ 从 2 到 1000，TE 与 EE 从 30 到 600，另加低 ℓ 的 EE）、ACT DR6（ℓ 600–8500）与 SPT-3G DR1（TT 400–3000，TE/EE 400–4000）。ℓ 是多极矩（multipole）序号，越大对应越小的角尺度。DES 有意不用 CMB 透镜，因为它与 DES 自己的透镜测量并不独立。

#### 1.3 一步一步：作者如何从数据走到结论

**第 1 步 · DES 的测量。** DES 用 ΛCDM 拟合 3x2pt 数据（预先约定的揭盲检验没有通过后，去掉了透镜第 2 个红移区间）。分析是盲化（blinding）的：在流程定下来之前，作者看不到宇宙学结果。基准结果（第 V.1 节式 21）为 S8 = 0.789 ± 0.012，Ωm = 0.333 (+0.023/−0.028)。D26 报告后验**均值**与 68% 可信区间，括号中是最大后验（MAP, maximum a posteriori）值（S8 为 0.793）。

**第 2 步 · CMB 的预言。** 用同一模型拟合 CMB 组合，得到 S8 = 0.836 (+0.012/−0.013)（表 4）。

**第 3 步 · 粗略估算。** 两个 S8 相差 0.836 − 0.789 = 0.047。如果两者都是独立的高斯分布，差值的不确定度约为 √(0.012² + 0.0125²) ≈ 0.017，差别约为 0.047/0.017 ≈ **2.7σ**。

**第 4 步 · 正式的度量。** D26 不用粗略估算，而用**参数差异概率（parameter-difference probability）**（第 IV.6 节；Raveri & Hu 2019；Raveri & Doux 2021）：

- 两个独立后验之差 Δp 的分布是交叉相关积分 P(Δp) = ∫ P(p|A) P(p − Δp|B) dp（式 17）；
- Δ 是 P(Δp) 在经过 Δp = 0（没有位移的点）的等密度线以内的概率（式 18）；
- 把 Δ 换算成"等效标准差数" n_σ = √2 erf⁻¹(Δ)（式 19）：同样概率的高斯事件对应的标准差个数。

在高维时，DES 用 tensiometer 代码中的**归一化流（normalizing flow，一种机器学习的密度估计器）**估计密度。

**第 5 步 · 数字。** DES 在 S8 方向（1 维）、S8–Ωm 平面（2 维）和全参数空间比较两个后验，得到 **2.6σ、2.2σ 与 1.8σ**（第 V.2 节，表 6）。S8 方向是 3x2pt 测得最好的方向，所以差别在那里最明显。与单独的 Planck 2018 相比，全空间差别为 1.0σ（DES Y3 为 1.5σ）。与单独的 Planck 比，2 维差别从 Y3 的 1.9σ 降到 Y6 的 1.4σ；但与 CMB 组合比则升到 2.2σ，因为组合的 CMB 更紧、偏好稍高的 S8。

**第 6 步 · 判据。** D26 把 n_σ < 3 定为"两组数据足够一致、可以考察其联合约束"的判据（第 IV.6 节）。三个数字都低于 3，所以 DES 接着与 CMB 联合。

**第 7 步 · 对 DES 后验的检查。** 高维时，边缘均值可能被先验的形状拉离真值（"先验体积"效应，又称投影效应（projection effects））。DES 在其最佳拟合点生成无噪声的模拟数据向量，跑同样的流程，测量位移（真值 − 均值）/σ（附录 B 表 9）：基准分析中 S8 为 +0.17，所有关心的参数都低于 0.5σ。

**第 8 步 · 其他探针。** 第 VII.3 节中 DES 与 KiDS-Legacy 的宇宙剪切（S8 = 0.815 +0.016/−0.021）比较，认为与自己的宇宙剪切（0.783 +0.019/−0.015）一致。DES 引用 HSC Y3 为 0.804 ± 0.051；这个数在 DES 所引的论文（Zhang et al. 2025，arXiv:2507.01386，给出 0.780 +0.029/−0.030）中找不到，我们直接用所引论文的数值。

#### 1.4 结论与把握程度

- **结论（第 VIII 节）：** 在 S8 和全参数空间上都"没有与 CMB 不一致的实质证据"，各弱透镜实验的显著性在约 1σ 到至多 3σ 之间。DES 也说整个领域"与前几年处在相似的位置"：D26 并没有说张力已经消失。
- **把握程度：** 全空间的 1.8σ 不依赖方向的选择；2.6σ 是 DES 事先选定的、测得最好的方向上的数字。
- **作者可能错在哪里：**
  - 度量或其数值估计可能有偏差（归一化流的估计有噪声，D26 没有报告）；
  - 未识别的系统误差可能移动 DES 的 S8（透镜第 2 个红移区间已经不得不去掉）；
  - "低于 3σ"未必等于"没有证据"：2.6σ 对应约 1% 的偶然概率，很多人会称之为弱证据。D26 写下的规则是是否合并的判据，而不是关于证据的陈述。

### 第二部分 · 论证逻辑

#### 2.0 论证地图

A. 参照：主 CMB 组合（不含透镜）。
B. 度量：参数差异概率，换算成 n_σ。
C. 数字：1.8σ（全空间）与 2.6σ（S8），投影效应小。
D. 规则：低于 3σ 时两组数据足够一致、可以合并。
E. [缺口] 可以合并，且 S8 投影也低于 3σ ⇒ 没有不一致的实质证据。
⇒ 没有与 CMB 不一致的实质证据。

检查方法：论证用 Lean 4 写成（[`studies/008-m03-s8-des-y6-cmb-parameter-difference/argument/Argument.lean`](https://github.com/sudoghut/astrolab/blob/main/studies/008-m03-s8-des-y6-cmb-parameter-difference/argument/Argument.lean)）。每个前提是 `Field` 的一个构造子（不用公理），标注类型与出处性质：

| 标注 | 前提类型 |
|---|---|
| `OBS` | 观测或测量（注明表或图） |
| `MOD` | 模型假设 |
| `STAT` | 统计推断（显著性、模型比较） |
| `NUM` | 数值结果，由本仓库的 `run.py` 复算 |
| `LIT` | 取自其他文献的结果 |
| `GAP` | 推理需要、但论文与标准知识都没有提供的前提 |

出处性质：`[stated: "引文"]`（论文明说，附引文）、`[implied]`（论文依赖但没写出的标准知识，注明来源）、`[reconstructed]`（我们补上的，恰好是 `GAP` 前提）。

Lean 检查的内容：结论由这些前提推出（`final`）且不是恒真（`final_nontrivial`）；前提可以同时成立（`consistent`）；任何单个前提都推不出结论（`alone_insufficient`）；每个前提是必要的（有不含它的反例模型）还是多余的；论文明说的前提是否足够（`stated_*`），加上标准知识后是否足够（`explicit_*`；`explicit_insufficient` 表示真正的缺口）。Lean 不检查每个前提内部的物理——那是第一、三部分和研究本身的任务。

数字以十分之一个 σ 编码为自然数；"至多 18 个十分之一"不强于报告的、已四舍五入的"1.8"。

#### 2.1 环节 A · 参照与度量

**概述。** 比较需要固定的参照（哪一个 CMB）与固定的、把两个后验变成一个数的方法。

**前提。**

| 前提（Lean 构造子） | 标注 | 出处性质 | 论文出处 |
|---|---|---|---|
| `obs_cmb`：CMB 参照是 Planck 2018 + ACT-DR6 + SPT-3G DR1 的主 TT/TE/EE，不含 CMB 透镜 | OBS | stated: "for primary temperature and polarization data, but without CMB lensing" | §V.2 |
| `mod_metric`：一致性由参数差异概率度量 | MOD | stated: "We measure consistency from the probability of a parameter difference" | §IV.6，式 17–19 |

**其他解释。**

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 换一个 CMB 参照（单独的 Planck）会得到不同答案（1.0σ） | `obs_cmb` 固定了参照 | 是，两者都报告了（§V.2） |
| 换一种度量（高斯差异、贝叶斯因子或证据比）会得到不同的数 | `mod_metric` | 否；D26 只用一种度量 |

**评述。** 参照很重要：与单独的 Planck 比，全空间为 1.0σ；与组合比为 1.8σ。结论说的"CMB"是指组合。

#### 2.2 环节 B · 数字及其可靠性

**前提。**

| 前提（Lean 构造子） | 标注 | 出处性质 | 论文出处 |
|---|---|---|---|
| `stat_full`：全空间差异至多 1.8σ | STAT | stated: "we find a full parameter space difference of 1.8" | §VIII（又见 §V.2、表 6） |
| `stat_s8`：投影到 S8 的差异至多 2.6σ | STAT | stated: "the difference increases to 2.6" | §VIII（又见 §V.2） |
| `stat_proj`：投影效应低于 0.5σ | STAT | stated: "exhibits minor prior-volume effects of less than" | 附录 B |

**其他解释。**

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 先验体积效应使 DES 的均值移动到足以改变数字 | `stat_proj` | 是（附录 B 表 9：S8 为 +0.17） |
| 归一化流的估计有噪声 | 无 | 否；数值误差没有报告 |

**评述。** 这些是本研究可以复算的数字（第三部分）。2.6σ 是在比较之前选定的方向（测得最好的方向）上的数字，是否要做试验次数修正两种看法都有；全空间的 1.8σ 不需要。

#### 2.3 环节 C · 从数字到结论

**前提。**

| 前提（Lean 构造子） | 标注 | 出处性质 | 论文出处 |
|---|---|---|---|
| `mod_crit`：（全空间）低于 3σ 时两组数据足够一致、可以合并 | MOD | stated: "as the criterion for different data sets agreeing well enough that it makes sense to examine their combined constraint" | §IV.6 |
| `gap_bridge`：在上述参照与度量下，可以合并、S8 投影也低于 3σ 且投影效应小的数据，没有不一致的实质证据 | GAP | reconstructed | — |

**其他解释。**

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 即使允许合并，2.6σ（偶然概率约 1%）也是不一致的弱证据 | `gap_bridge` | 否 |

**推理（Lean 摘录）。**

```lean
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  have hfull : v.n_full_x10 ≤ 18 := p .stat_full          -- Sec. V.2, VIII: 1.8 sigma
  have hs8 : v.n_s8_x10 ≤ 26 := p .stat_s8                -- Sec. V.2, VIII: 2.6 sigma
  have hcomb : v.Combinable := p .mod_crit (by omega)     -- Sec. IV.6: below 3, combinable
  exact p .gap_bridge (p .obs_cmb) (p .mod_metric) hcomb (by omega) (p .stat_proj)  -- GAP
```

**评述。** D26 只用它的判据来说明可以合并（"As such, we are able to combine"，§V.2）。§VIII 中"没有实质证据"一句引用的是各实验显著性的范围，而不是这个判据。两者之间的这一步是我们补上的。

#### 2.4 Lean 检查发现的问题

1. **主要结果：`explicit_insufficient`。** 即使加上标准的统计知识，没有 `gap_bridge` 这些前提也推不出结论。低于 3σ 是合并数据的约定，而不是"不存在不一致"的定理。`stated_insufficient` 因同样的原因成立。不需要任何 `[implied]` 前提。
2. **在这种编码下每个前提都是必要的**（七个 `_needed` 定理），没有多余的。对未解释的原子命题而言，"必要"指"被这种编码用到"：例如 `stat_proj` 之所以必要，是因为我们把"投影效应小"放进了桥接规则。
3. **结论脆弱的地方。** 它依赖阈值：报告的数字都低于 3σ，所以在 D26 的三种投影下都成立；但阈值若取 2.5σ，S8 投影就不满足了。它也依赖参照（单独的 Planck 给出 1.0σ），以及 D26 没有报告的数值估计精度。
4. **相容性**（`consistent`）在这里是弱检查：没有否定形式的前提。
5. **局限：** Lean 检查的是我们编码下的逻辑结构，不是每个前提内部的统计。2.6σ 算不算"实质"是判断问题；机器检查只表明论文没有给出这个判断的规则。

### 第三部分 · 本项目可检验或探索的环节

DES 的基准 3x2pt 链文件为 144 MB，超过本项目单次下载 50 MB 的上限；用户同意为这一个文件破例一次（2026-11-15）。CMB 链（11.8 MB）与宇宙剪切链（14.9 MB）在上限之内。其他探针只用已发表的汇总值。

| 环节 / 结论 | 能否检验或探索 | 方法 | 数据（大小） | 判据 | 结果 |
|---|---|---|---|---|---|
| 输入：CMB（0.836 +0.012/−0.013）、DES 3x2pt（0.789 ± 0.012）与 DES 宇宙剪切（0.783 +0.019/−0.015）的 S8 均值（R1） | 现在可检验 | 由每条公开链算加权均值与 68% 区间 | DES 链：144 + 11.8 + 14.9 MB | 每个均值与发表值之差在预注册容差内 | 待定 |
| 环节 B：2.6σ（S8）与 2.2σ（S8–Ωm）（R2） | 现在可检验 | 由两条链按式 17–19 计算：按权重独立抽样、逐对相减，用同一个核密度估计在差值样本与零点求值（拆分两半），n_σ = √2 erf⁻¹(Δ)；收敛与带宽诊断事先写定 | 同上 | 在预注册容差（蒙特卡罗误差加写明的余量）内 → 复现 | 待定 |
| 环节 B：1.8σ（全空间） | 可探索（不能判决） | 对共有参数作高斯近似，包含与不含主要由先验决定的方向；不用归一化流 | 同上 | 无——仅供探索 | 待定 |
| DES 宇宙剪切对 CMB（R3） | 现在可检验（若 R1 确认该链） | 同 R2，链对链 | 同上 | 除非 D26 给出数字，否则无——描述 | 待定 |
| 环节 B 的投影效应；环节 C 的阈值与度量（R4） | 可探索（不能判决） | DES 上移 +0.17σ（表 9）或改用 MAP；同一个 1 维比较的等密度、等尾与高斯三种算法；报告阈值在哪里改变分类 | 同上 | 无——仅供探索 | 待定 |
| 其他探针对 CMB（R5） | 可探索（不能判决） | 各已发表的 S8 汇总值（分裂正态）对 CMB 链；不做平均（探针相关，且约束的方向不同） | 发表值（kB） | 无——描述 | 待定 |
| `gap_bridge`（低于 3σ 是否等于"没有证据"） | 不在范围内 | 是关于证据的判断，不是计算；研究只报告它所依据的数字 | – | – | – |
| DES 的系统误差、盲化与流估计器本身 | 不在范围内 | 需要数据向量、模拟与分析流程 | – | – | – |

### 术语表

| 术语 | 含义 |
|---|---|
| S8 | σ8 (Ωm/0.3)^0.5：物质成团幅度，取弱透镜测得最好的组合 |
| σ8 | 今天 8 h⁻¹ Mpc 球内线性物质涨落的均方根幅度 |
| Ωm | 物质密度与临界密度之比 |
| 3x2pt | 宇宙剪切、星系–星系透镜与星系成团的联合分析 |
| 参数差异概率（parameter-difference probability） | 两个后验之差的分布在经过零位移的等密度线以内的概率 |
| n_σ | √2 erf⁻¹(Δ)：概率 Δ 对应的高斯等效标准差数 |
| 归一化流（normalizing flow） | 用于在高维中计算后验密度的神经网络密度估计器 |
| 先验体积（投影）效应（prior-volume / projection effect） | 由其他参数的先验体积而不是数据造成的边缘均值位移 |
| MAP | 最大后验：后验密度最高的参数值 |
| 盲化（blinding） | 在分析选择定下之前对分析者隐藏宇宙学结果 |

### 开放问题

- 不用归一化流，全空间的 1.8σ 能否复现（需要流的工具，要另行安装）？
- 其他探针发表的 S8 在统一选择下重新分析会移动多少（D26 §VII.3 画的是各巡天发表的链，不是统一的重新分析）？

### 研究进展

按时间倒序。

- 2026-11-15：第一版：第一至三部分（预注册的来源；计划 `design/017-plan_*`）。

### 来源

- DES Collaboration 2026，arXiv:2601.14559（v2），本文研究的论文。
- Raveri & Hu 2019，PRD 99, 043506；Raveri & Doux 2021，arXiv:2105.03324：参数差异度量。
- Wright et al. 2025，A&A 703, A158，arXiv:2503.19441（KiDS-Legacy）。
- Zhang et al. 2025，arXiv:2507.01386（HSC Y3，D26 为 HSC 所引的文献）。
- Madhavacheril et al. 2024，ApJ 962, 113，arXiv:2304.05203（ACT DR6 透镜）。
- Ghirardini et al. 2024，A&A 689, A298，arXiv:2402.08458（eROSITA 星系团）。
- DES Y3：arXiv:2105.13549；KiDS-1000：arXiv:2007.15632、arXiv:2007.15633（上一代）。
