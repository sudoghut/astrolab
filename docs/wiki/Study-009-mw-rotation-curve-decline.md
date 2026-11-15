# Is the Milky Way light? The Keplerian decline of its rotation curve

[English](#english) · [中文](#中文)

*Paper: Jiao, Hammer, Wang et al. 2023, "Detection of the Keplerian decline in the Milky Way rotation curve", A&A 678, A208, arXiv:2309.00048. Study:
[`studies/009-m06-mw-outer-rotation-curve-decline`](https://github.com/sudoghut/astrolab/tree/main/studies/009-m06-mw-outer-rotation-curve-decline).
Status: planned. Last updated: 2026-11-15 (see the changelog at the end). The source of this page lives in the main repository at
[`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki); edit it there.*

*中文标题：银河系很轻吗？其旋转曲线的开普勒式下降。状态：计划中。论文：Jiao, Hammer, Wang 等 2023，A&A 678, A208，arXiv:2309.00048。研究：[`studies/009-m06-mw-outer-rotation-curve-decline`](https://github.com/sudoghut/astrolab/tree/main/studies/009-m06-mw-outer-rotation-curve-decline)。最后更新：2026-11-15（见文末"研究进展"）。本页源文件在主仓库的 [`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki) 中，请在那里修改。*

---

## English

### Part 1 · The paper in plain language

#### 1.1 The question and why it matters

How heavy is our Galaxy? Most of its mass is thought to be dark matter, in a roughly spherical
halo that extends far beyond the stars. The classic way to weigh a galaxy is its **rotation curve**:
the speed of circular orbits as a function of distance from the centre. If orbits keep the same
speed far out (a "flat" curve), the enclosed mass keeps growing with radius, which is the textbook
signature of a dark-matter halo. If the speed falls like 1/√R (a "Keplerian" decline, as for planets
around the Sun), almost no mass is being added at those radii.

Estimates of the Milky Way's total mass range from about 0.5 to 2 × 10¹² solar masses (M☉), mostly
from tracers far out (satellite galaxies, globular clusters, stellar streams); the earlier virial
masses J23 itself cites are 7–11 × 10¹¹ M☉. J23 reports that the
rotation curve measured with Gaia data declines between about 19 and 26.5 kiloparsec (kpc) and
infers a total mass of only about 2 × 10¹¹ M☉, about 3.5–5.5 times below the earlier virial masses
J23 cites. If true, the Milky Way would
be unusually light for its stellar mass, which would matter for galaxy formation models and for
dark-matter physics.

#### 1.2 The data

The Gaia satellite measures positions, parallaxes (distances) and proper motions (motions across
the sky) for more than a billion stars, and line-of-sight velocities for about 33 million. J23 uses
a Gaia DR3 sample of disc stars analysed by Wang et al. 2023 (arXiv:2211.05668), whose distances were
corrected statistically for parallax errors (a "Lucy inversion"), out to about 27.5 kpc from the
Galactic centre (the Sun is at about 8 kpc).

Stars do not move on perfect circles: they have random motions. So the circular speed is not
measured directly; it is inferred from the stars' mean motions and their scatter with the **Jeans
equation**, which balances gravity against the "pressure" of random motions, assuming the disc is in
a steady state and is axisymmetric (the same at every azimuth).

#### 1.3 Step by step: how the authors got from data to conclusion

**Step 1 · The rotation curve.** J23 bins the stars in 1-kpc rings within 3 kpc of the plane and
applies the Jeans equation (Binney & Tremaine 2008, Eq. 4.222a). The result (Table 3) is 18 values
of the circular speed V_c from 9.5 to 26.5 kpc: about 222 km/s out to 14 kpc, then falling to 206 km/s
at 19.5 kpc and 176 km/s at 26.5 kpc, a drop of about 30 km/s over 7 kpc. Each value has one error
bar, which the paper describes as the quadrature sum of statistical and systematic errors.

**Step 2 · Systematic errors.** J23 estimates four sources: the cross term ∂⟨v_R v_z⟩/∂z of the
Jeans equation (below 2% inside 23 kpc, up to about 8% at 25.5 kpc), the scale length of the tracer
density (about 1%), a power-law instead of an exponential density (below 4%), and splitting the
sample by Galactic longitude (below 2% inside 22 kpc).

**Step 3 · Is it really declining?** J23 fits a power law V = A R^γ to the 8 bins beyond 19 kpc
(Sec. 5.3). A flat curve has γ = 0, a Keplerian one γ = −0.5. It finds γ = −0.47 ± 0.15, so γ = 0
lies 0.47/0.15 ≈ 3.1 standard deviations away (our reading; J23 does not say how it computed the
significance): "a flat RC is rejected at a 3σ significance level".
On the independent curve of Ou et al. (O24, arXiv:2303.12838) the same fit gives γ = −0.56 (+0.23/−0.22).

**Step 4 · Mass models.** J23 adds the stars and gas (seven published baryon models: B2 and six
combinations of an exponential or Gaussian triaxial bulge with three disc models) to a spherical
Einasto dark-matter halo, ρ(r) = ρ0 exp[−(r/h)^(1/n)], and fits the 18 points (Table 4). For model B2
the halo has n = 0.43 and h = 11.41 kpc: a halo whose density falls steeply at large radius.

**Step 5 · Total mass.** The fitted halo is extrapolated to the virial radius R_vir, where the mean
dark-matter density equals 200 times the critical density of the Universe (about 121 kpc), and the
"dynamical mass" is baryons plus dark matter inside R_vir. The seven models give 1.97–2.05 × 10¹¹ M☉
(mean 1.99); the O24 curve gives a mean of 2.13; the abstract's 2.06 (+0.24/−0.13) × 10¹¹ M☉ is the
average of the two curves. Using the upper ends of the O24 velocities gives at most 5.4 × 10¹¹ M☉,
which J23 calls an unsurpassable limit.

**Back of the envelope.** The mass inside radius R for a circular speed V is M ≈ V²R/G. At 26.5 kpc
with 176 km/s: M ≈ (176 km/s)² × 26.5 kpc / G ≈ 1.9 × 10¹¹ M☉. That is already the whole claimed
total: the conclusion says that almost nothing is added beyond 26.5 kpc.

#### 1.4 What they conclude, and how sure they are

- **Claims:** a Keplerian decline starting at about 19 kpc, detected "for the first time"; a flat
  curve rejected at 3σ; a total mass of about 2 × 10¹¹ M☉.
- **Caveats the authors give:** the cross term grows at large radii; the outermost bins have large
  errors; a Keplerian decline "may appear quite exceptional".
- **What would have to be true for them to be wrong:**
  - the Jeans equation in its steady-state, axisymmetric form could be biased at 20–27 kpc, where
    the disc is warped, flared and disturbed by the Sagittarius dwarf and the Large Magellanic Cloud;
    later work finds biases of 10–15% and even artificial steep declines (Koop et al. 2024,
    arXiv:2405.19028; Ou et al. 2025, arXiv:2503.05877);
  - the halo shape fitted inside 26.5 kpc may not hold out to 121 kpc: stellar streams measure more
    mass at 30–100 kpc (Koposov et al. 2023: 2.85 × 10¹¹ M☉ inside 32.4 kpc; Vasiliev et al. 2021:
    5.6 × 10¹¹ M☉ inside 100 kpc).

### Part 2 · The logic of the argument

#### 2.0 Map of the argument

The encoded conclusion is the title claim, the Keplerian decline. The total mass is obtained by a
separate fit and is discussed, not encoded, in 2.3.

A. The curve: a drop of about 30 km/s between 19.5 and 26.5 kpc, from the equilibrium Jeans equation.
B. [gap] The Jeans curve is accurate enough at those radii.
C. A flat curve rejected at 3σ, and a slope consistent with −0.5; [gap] so the decline is Keplerian.
⇒ A Keplerian decline beyond about 19 kpc.

How we check it: the argument is written in Lean 4
([`studies/009-m06-mw-outer-rotation-curve-decline/argument/Argument.lean`](https://github.com/sudoghut/astrolab/blob/main/studies/009-m06-mw-outer-rotation-curve-decline/argument/Argument.lean)).
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

#### 2.1 Stage A · The measured curve and the Jeans equation

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `obs_drop`: the curve drops by about 30 km/s from 19.5 to 26.5 kpc | OBS | stated: "the decrease in velocity between 19.5 and 26.5 kpc is approximately 30 km s-1" | Abstract, Table 3 |
| `mod_jeans`: Jeans equation for an axisymmetric potential and a disc at equilibrium | MOD | stated: "Assuming an axisymmetric MW potential and a disc at equilibrium" | Sec. 2.1 |
| `gap_jeans`: the equilibrium Jeans curve is accurate at 19–26.5 kpc to better than the decline | GAP | reconstructed | — |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| The decline is an artefact of departures from equilibrium (warp, flare, Sagittarius, LMC) or of a truncated tracer density | `gap_jeans` | partly: J23 argues for quasi-equilibrium (Sec. 2.2: the perturbations due to the radial velocity are small; Sec. 5.2: quasi-equilibrium within 30 kpc, with a discussion of the warp and Sagittarius) and estimates the cross term and the density law, but does not quantify departures from equilibrium |

**Critique.** J23 asserts equilibrium and estimates the cross term; what it does not show is that
the equilibrium Jeans curve is accurate at 19–26.5 kpc to better than the 15% decline. Later work
(published after J23, so a gap rather than standard knowledge) finds biases of 10–15% for such
modelling and shows that a truncated tracer density can fake a steep decline (Koop et al. 2024).

#### 2.2 Stage B · From a 3σ rejection to a decline

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `stat_flat`: a flat curve rejected at 3σ | STAT | stated: "while a flat RC is rejected with a significance of 3σ" | Abstract; Sec. 5.3: "a flat RC is rejected at a 3σ significance level" (γ = −0.47 ± 0.15) |
| `stat_kepler`: the slope is consistent with a Keplerian decline | STAT | stated: "This suggests that the MW RC is consistent with a Keplerian decline (γ=-0.5) at large radii" | Sec. 5.3 |
| `gap_detect`: with an accurate curve, a 3σ rejection of a flat curve and a slope consistent with −0.5 mean a Keplerian decline | GAP | reconstructed | — |

**Inference (Lean excerpt).**

```lean
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  have hsig : v.sig_x10 = 30 := p .stat_flat                     -- Abstract, Sec. 5.3
  exact p .gap_detect (p .obs_drop) (p .mod_jeans) (p .gap_jeans) (by omega) (p .stat_kepler)  -- two GAPs
```

**Critique.** The 3σ comes from γ in a two-parameter power-law fit to 8 points, with errors that
include systematics. J23 does not say how the 3σ was computed; our reading is 0.47/0.15 ≈ 3.1σ
(on the O24 curve the same ratio is 0.56/0.22 ≈ 2.5σ; J23 states the 3σ right after giving both
slopes, but the simple ratio reaches about 3σ only for its own curve). Calling it a "detection" uses
3σ as the level of evidence, and reading "consistent with −0.5" as Keplerian is a further step: the
1σ range of γ (about −0.62 to −0.32) also contains declines that are not Keplerian. Both steps are in `gap_detect`, which J23 does not state (study 008 has the same 3σ step). The
outer 4 bins have errors of 8–25 km/s, so the rejection rests mostly on 19.5–22.5 kpc.

#### 2.3 The total mass (discussed, not encoded)

J23's mass does not come from the decline test. It comes from fitting a spherical Einasto halo
(Sec. 3.2, eq. 9) plus baryon models ("considering several possible combinations of models for the
bulge and the disc presented by Iocco et al. (2015)", and the baryonic model B2 from de Salas et al.
2019) to all 18 points, then extrapolating the halo to the virial radius ("we extrapolated the DM
halo to the virial radius") and adding the baryons ("We calculated the dynamical mass as the sum of
the baryonic mass and the DM halo virial mass", Sec. 4.3). The steps that carry the mass are:

- **The fit itself.** It uses all 18 points; its result would barely change if γ were −0.3 instead
  of −0.47. J23's eq. 11 says the fit uses "the statistical uncertainty of the measurement", while
  Sec. 4.1 says "In our study, as well as in Ou et al. (2023), error bars account for systematic
  uncertainties" (Sec. 4.3 repeats this for the mass error bars), and Table 3 gives only the
  combined error. The most likely reading is that the fit used the combined errors;
  per-bin statistical errors are not published, so our fit (R2) is descriptive.
- **The extrapolation.** The data stop at 26.5 kpc; R_vir ≈ 121 kpc is 4.6 times farther. With
  n = 0.43 the Einasto halo truncates steeply, so the extrapolated mass is set largely by the
  chosen functional form. The mass the data measure is the enclosed mass at 26.5 kpc (about
  1.9 × 10¹¹ M☉ from V²R/G). Whether the fitted shape holds out to 121 kpc is not tested in J23;
  stream masses (Koposov et al. 2023: 2.85 × 10¹¹ M☉ inside 32.4 kpc; Vasiliev et al. 2021:
  5.6 × 10¹¹ M☉ inside 100 kpc) suggest more mass at 30–100 kpc.

These steps are not encoded in Lean because one file has one conclusion; they are tested in part 3
(R2, R5).

#### 2.4 What the Lean check found

1. **Headline: `explicit_insufficient`, with two gaps.** The decline needs: the equilibrium Jeans
   curve is accurate at 19–26.5 kpc (`gap_jeans`); and a 3σ rejection with a slope consistent with −0.5 counts as a detected
   Keplerian decline (`gap_detect`). No standard knowledge closes either.
2. **Ranking.** `gap_jeans` matters most: the decline (15%) is comparable to later estimates of
   Jeans biases. `gap_detect` is the same 3σ-as-evidence step found in study 008.
3. **All six premises are needed** in this encoding; none is redundant.
4. **For the mass (2.3, not encoded):** the extrapolation from 26.5 to 121 kpc is the weakest step,
   and the paper's wording on which errors the fit used is internally inconsistent.
5. **Consistency** (`consistent`) is a weak check here: no premise is negative.
6. **Limits:** Lean checks the logical structure under our encoding, not the dynamics inside each
   premise.

### Part 3 · What astrolab can test or explore

All inputs are small tables transcribed from the papers (J23 Tables 3 and 4 and the baryon
parameters; O24 Table 1; Eilers et al. 2019 Table 1), checked by two independent transcriptions;
nothing is downloaded. J23 gives no per-bin statistical errors, so (rule E0 of plan 018) R1 uses
Table 3's total errors as J23's power-law test does, and R2 is a descriptive fit, not a reproduction.

| Stage / claim | Can we test or explore it? | How | Data (size) | Decision criterion | Result |
|---|---|---|---|---|---|
| Stage B: flat rejected at 3σ (R1) | testable now | J23 eq. 13: V = A R^γ on the 8 bins beyond 19 kpc with Table 3 errors, flat prior γ ∈ [−10, 5]; statistic (0 − median γ)/(84th − 50th percentile); P(γ ≥ 0), Δχ² and leave-one-bin-out reported | J23 Table 3 (0.3 kB) | reproduced if median γ within −0.47 ± 0.05 and the statistic within 3.1 ± 0.3σ | pending |
| Stage C: masses of the six fully specified baryon models (R2) | explorable (descriptive; J23's statistical errors are not published) | Einasto + baryons fitted to Table 3 with total errors, J23's priors and R_vir definition; compared with Table 4 | J23 Tables 1, 2, 4 (5 kB) | none - descriptive (difference to Table 4 reported) | pending |
| Stage A: systematics (R3) | explorable (not decisive) | (a) constant bias: null control for γ, refits of the mass for b = ±5%, ±10%; (b) bias rising linearly from 0 at 19 kpc to b_max at 26.5 kpc, scanned 0–20%, smallest b_max that brings R1 below 2σ (an injected stress test; literature magnitudes only as context); (c) correlated outer errors | same | none - exploration only | pending |
| Other curves (R4) | explorable (descriptive) | J23 against O24 and Eilers et al. 2019 in the overlap; R1 on O24 (J23: γ = −0.56) | O24 Table 1, Eilers Table 1 (2 kB) | none - descriptive | pending |
| Stage C: extrapolation (R5) | explorable (descriptive) | M(<26.5 kpc) from the data against extrapolated M(<32.4), M(<100), M_vir; an NFW-like halo fitted for comparison; stream masses as an order-of-magnitude, cross-model comparison | as above | none - descriptive | pending |
| `gap_jeans` itself (non-equilibrium dynamics) | out of scope | needs 6-D stellar data and dynamical modelling beyond the Jeans equation | – | – | – |

### Glossary

| Term | Meaning |
|---|---|
| rotation curve | circular speed as a function of Galactocentric radius |
| Keplerian decline | V ∝ R^(−1/2), as around a point mass: no mass added at those radii |
| Jeans equation | balance of gravity and stellar "pressure" (random motions) for a steady-state system |
| cross term | ∂⟨v_R v_z⟩/∂z, the tilt of the velocity ellipsoid, often neglected in the Jeans equation |
| Einasto profile | ρ(r) = ρ0 exp[−(r/h)^(1/n)], a dark-matter density law with adjustable outer steepness |
| virial radius | radius inside which the mean dark-matter density is 200 times the critical density |
| dynamical mass | J23's term for baryons plus dark matter inside the virial radius |

### Open questions

- How large are departures from equilibrium (warp, flare, Sagittarius, LMC) at 20–27 kpc in the
  Jeans circular speed? This needs dynamical modelling beyond this repository.
- Can the extrapolated mass be made consistent with stream and satellite masses with any halo shape
  that fits the rotation curve?

### Changelog

Newest first.

- 2026-11-15: gate-1 round 2: the Keplerian shape now rests on its own stated premise (`stat_kepler`, Sec. 5.3) and on the gap.
- 2026-11-15: gate-1 review: the Lean conclusion is now the Keplerian decline (two gaps); the mass and its extrapolation are discussed in 2.3, not encoded (the mass fit does not use the decline test); quotes corrected; the error-wording inconsistency described with both sentences.
- 2026-11-15: first version: parts 1–3 (pre-registration source; plan `design/018-plan_*`).

### Sources

- Jiao et al. 2023, A&A 678, A208, arXiv:2309.00048 (the paper studied).
- Ou, Eilers, Necib, Frebel 2024, MNRAS 528, 693, arXiv:2303.12838.
- Eilers, Hogg, Rix, Ness 2019, ApJ 871, 120, arXiv:1810.09466.
- Wang, Chrobáková, López-Corredoira, Sylos Labini 2023, ApJ 942, 12, arXiv:2211.05668.
- Koop et al. 2024, A&A 692, A50, arXiv:2405.19028; Ou et al. 2025, arXiv:2503.05877 (Jeans biases).
- Koposov et al. 2023, arXiv:2211.04495; Vasiliev et al. 2021, arXiv:2009.10726 (stream masses).
- Melchiorri & Ruchika 2026, arXiv:2608.10189 (review).

---

## 中文

### 第一部分 · 科普详解

#### 1.1 问题与意义

我们的银河系有多重？一般认为它的大部分质量是暗物质，分布在一个大致球形、远远超出恒星范围的晕（halo）中。称量星系的经典方法是**旋转曲线**（rotation curve）：圆轨道速度随到中心距离的变化。如果很远处轨道速度仍保持不变（"平坦"曲线），包围质量随半径不断增长，这正是暗物质晕的教科书特征；如果速度像 1/√R 那样下降（"开普勒式"下降，就像行星绕太阳），说明在这些半径处几乎没有新增质量。

银河系总质量的估计大约在 0.5 到 2 × 10¹² 太阳质量（M☉）之间，主要来自远处的示踪体（卫星星系、球状星团、恒星星流（stellar streams））；J23 自己引用的早先的位力质量为 7–11 × 10¹¹ M☉。J23 报告说，用 Gaia 数据测得的旋转曲线在约 19 到 26.5 千秒差距（kpc）之间下降，推出总质量只有约 2 × 10¹¹ M☉，比 J23 引用的早先位力质量低约 3.5–5.5 倍。如果属实，银河系相对于其恒星质量会异常地轻，这对星系形成模型与暗物质物理都有影响。

#### 1.2 数据

Gaia 卫星测量了十多亿颗恒星的位置、视差（距离）与自行（在天球上的运动），以及约 3300 万颗恒星的视向速度。J23 用 Wang 等 2023（arXiv:2211.05668）分析过的 Gaia DR3 盘星样本，其距离已对视差误差作统计校正（"Lucy 反演"），延伸到距银心约 27.5 kpc（太阳约在 8 kpc）。

恒星并不沿完美的圆运动，而有随机运动。所以圆速度不是直接测得的，而是用**金斯方程**（Jeans equation）由恒星的平均运动与弥散推出：它在假设盘处于稳态、轴对称（各方位角相同）的前提下，让引力与随机运动的"压强"平衡。

#### 1.3 一步一步：作者如何从数据走到结论

**第 1 步 · 旋转曲线。** J23 把距银道面 3 kpc 以内的恒星按 1 kpc 的环分箱，应用金斯方程（Binney & Tremaine 2008，式 4.222a）。结果（表 3）是 9.5 到 26.5 kpc 的 18 个圆速度 V_c：14 kpc 以内约 222 km/s，然后下降到 19.5 kpc 的 206 km/s 与 26.5 kpc 的 176 km/s，在 7 kpc 内下降约 30 km/s。每个值有一个误差棒，论文称之为统计与系统误差的平方和。

**第 2 步 · 系统误差。** J23 估计了四个来源：金斯方程的交叉项（cross term）∂⟨v_R v_z⟩/∂z（23 kpc 以内小于 2%，25.5 kpc 处可达约 8%）、示踪体密度的标长（约 1%）、用幂律代替指数密度（小于 4%）、按银经把样本分开（22 kpc 以内小于 2%）。

**第 3 步 · 真的在下降吗？** J23 对 19 kpc 以外的 8 个箱拟合幂律 V = A R^γ（第 5.3 节）。平坦曲线 γ = 0，开普勒式 γ = −0.5。它得到 γ = −0.47 ± 0.15，所以 γ = 0 离它 0.47/0.15 ≈ 3.1 个标准差（这是我们的理解；J23 没有说明显著性如何算出）："平坦曲线以 3σ 的显著性水平被拒绝"。在 Ou 等（O24，arXiv:2303.12838）的独立曲线上，同样的拟合得到 γ = −0.56 (+0.23/−0.22)。

**第 4 步 · 质量模型。** J23 把恒星与气体（七个已发表的重子模型：B2，以及指数或高斯三轴核球与三种盘模型的六种组合）加上球对称的爱纳斯托（Einasto）暗物质晕 ρ(r) = ρ0 exp[−(r/h)^(1/n)]，拟合 18 个点（表 4）。对模型 B2，晕的 n = 0.43、h = 11.41 kpc：一个在大半径处密度急剧下降的晕。

**第 5 步 · 总质量。** 把拟合的晕外推到位力半径（virial radius）R_vir（暗物质平均密度等于宇宙临界密度的 200 倍处，约 121 kpc），"动力学质量"（dynamical mass）是 R_vir 以内的重子加暗物质。七个模型给出 1.97–2.05 × 10¹¹ M☉（平均 1.99）；O24 曲线的平均为 2.13；摘要的 2.06 (+0.24/−0.13) × 10¹¹ M☉ 是两条曲线的平均。用 O24 速度的上端得到至多 5.4 × 10¹¹ M☉，J23 称之为不可逾越的上限。

**粗略估算。** 圆速度 V 对应的 R 以内质量约为 M ≈ V²R/G。在 26.5 kpc 处取 176 km/s：M ≈ (176 km/s)² × 26.5 kpc / G ≈ 1.9 × 10¹¹ M☉。这已经是所声称的全部总质量：结论等于说 26.5 kpc 以外几乎没有新增质量。

#### 1.4 结论与把握程度

- **结论：** 从约 19 kpc 开始的开普勒式下降，"首次"探测到；平坦曲线以 3σ 被拒绝；总质量约 2 × 10¹¹ M☉。
- **作者给出的保留：** 交叉项在大半径处增大；最外几个箱的误差大；开普勒式下降"可能显得相当特殊"。
- **作者可能错在哪里：**
  - 稳态、轴对称形式的金斯方程在 20–27 kpc 可能有偏差，那里的盘有翘曲（warp）、外展（flare），并受人马座矮星系与大麦哲伦云扰动；后来的工作发现 10–15% 的偏差，甚至人为造成的陡降（Koop 等 2024，arXiv:2405.19028；Ou 等 2025，arXiv:2503.05877）；
  - 在 26.5 kpc 以内拟合的晕形状未必能延续到 121 kpc：恒星星流在 30–100 kpc 测得更多质量（Koposov 等 2023：32.4 kpc 以内 2.85 × 10¹¹ M☉；Vasiliev 等 2021：100 kpc 以内 5.6 × 10¹¹ M☉）。

### 第二部分 · 论证逻辑

#### 2.0 论证地图

编码的结论是标题中的说法：开普勒式下降。总质量由另一个拟合得到，在 2.3 中讨论，不编码。

A. 曲线：由平衡态金斯方程得到，19.5 到 26.5 kpc 之间下降约 30 km/s。
B. [缺口] 在这些半径处金斯曲线足够准确。
C. 平坦曲线以 3σ 被拒绝，斜率与 −0.5 相容；[缺口] 所以是开普勒式下降。
⇒ 约 19 kpc 以外的开普勒式下降。

检查方法：论证用 Lean 4 写成（[`studies/009-m06-mw-outer-rotation-curve-decline/argument/Argument.lean`](https://github.com/sudoghut/astrolab/blob/main/studies/009-m06-mw-outer-rotation-curve-decline/argument/Argument.lean)）。每个前提是 `Field` 的一个构造子（不用公理），标注类型与出处性质：

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

#### 2.1 环节 A · 测得的曲线与金斯方程

**前提。**

| 前提（Lean 构造子） | 标注 | 出处性质 | 论文出处 |
|---|---|---|---|
| `obs_drop`：曲线从 19.5 到 26.5 kpc 下降约 30 km/s | OBS | stated: "the decrease in velocity between 19.5 and 26.5 kpc is approximately 30 km s-1" | 摘要，表 3 |
| `mod_jeans`：轴对称势与平衡态盘的金斯方程 | MOD | stated: "Assuming an axisymmetric MW potential and a disc at equilibrium" | 第 2.1 节 |
| `gap_jeans`：19–26.5 kpc 的平衡态金斯曲线准确到优于下降幅度 | GAP | reconstructed | — |

**其他解释。**

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 下降是偏离平衡（翘曲、外展、人马座、大麦哲伦云）或示踪体密度截断造成的假象 | `gap_jeans` | 部分：J23 论证了准平衡（第 2.2 节：径向速度造成的扰动很小；第 5.2 节：30 kpc 以内准平衡，并讨论了翘曲与人马座），并估计了交叉项与密度规律，但没有量化偏离平衡的影响 |

**评述。** J23 断言了平衡并估计了交叉项；它没有表明平衡态金斯曲线在 19–26.5 kpc 的准确度优于 15% 的下降。后来的工作（发表于 J23 之后，所以是缺口而不是标准知识）发现这类建模的偏差可达 10–15%，并且示踪体密度截断可以造成虚假的陡降（Koop 等 2024）。

#### 2.2 环节 B · 从 3σ 拒绝到下降

**前提。**

| 前提（Lean 构造子） | 标注 | 出处性质 | 论文出处 |
|---|---|---|---|
| `stat_flat`：平坦曲线以 3σ 被拒绝 | STAT | stated: "while a flat RC is rejected with a significance of 3σ" | 摘要；第 5.3 节："a flat RC is rejected at a 3σ significance level"（γ = −0.47 ± 0.15） |
| `stat_kepler`：斜率与开普勒式下降相容 | STAT | stated: "This suggests that the MW RC is consistent with a Keplerian decline (γ=-0.5) at large radii" | 第 5.3 节 |
| `gap_detect`：曲线准确时，3σ 拒绝平坦曲线且斜率与 −0.5 相容意味着开普勒式下降 | GAP | reconstructed | — |

**推理（Lean 摘录）。**

```lean
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  have hsig : v.sig_x10 = 30 := p .stat_flat                     -- Abstract, Sec. 5.3
  exact p .gap_detect (p .obs_drop) (p .mod_jeans) (p .gap_jeans) (by omega) (p .stat_kepler)  -- two GAPs
```

**评述。** 3σ 来自对 8 个点拟合两参数幂律得到的 γ，误差已含系统误差。J23 没有说明 3σ 怎么算出；我们的理解是 0.47/0.15 ≈ 3.1σ（在 O24 曲线上同样的比值为 0.56/0.22 ≈ 2.5σ；J23 在给出两个斜率后紧接着说 3σ，但简单比值只有在它自己的曲线上才约为 3σ）。称之为"探测到"是把 3σ 当作证据门槛；把"与 −0.5 相容"读作开普勒式又是另一步：γ 的 1σ 范围（约 −0.62 到 −0.32）也包含不是开普勒式的下降。两步都在 `gap_detect` 中，J23 都没有写出（研究 008 中有同样的 3σ 一步）。外区 4 个箱的误差为 8–25 km/s，所以拒绝主要依靠 19.5–22.5 kpc。

#### 2.3 总质量（只讨论，不编码）

J23 的质量并不来自下降检验。它来自用球对称爱纳斯托晕（第 3.2 节，式 9）加重子模型（"considering several possible combinations of models for the bulge and the disc presented by Iocco et al. (2015)"，以及 de Salas 等 2019 的重子模型 B2）拟合全部 18 个点，再把晕外推到位力半径（"we extrapolated the DM halo to the virial radius"）并加上重子（"We calculated the dynamical mass as the sum of the baryonic mass and the DM halo virial mass"，第 4.3 节）。承载质量的步骤是：

- **拟合本身。** 它用全部 18 个点；即使 γ 是 −0.3 而不是 −0.47，结果也几乎不变。J23 的式 11 说拟合用的是"the statistical uncertainty of the measurement"，而第 4.1 节说"In our study, as well as in Ou et al. (2023), error bars account for systematic uncertainties"（第 4.3 节对质量误差棒重复了这一点），表 3 也只给出合成误差。最可能的理解是拟合用了合成误差；各箱的统计误差没有发表，所以我们的拟合（R2）是描述性的。
- **外推。** 数据止于 26.5 kpc；R_vir ≈ 121 kpc 远 4.6 倍。n = 0.43 的爱纳斯托晕截断很陡，所以外推的质量很大程度上由所选的函数形式决定。数据真正测量的是 26.5 kpc 以内的包围质量（由 V²R/G 得约 1.9 × 10¹¹ M☉）。拟合的形状能否延续到 121 kpc，J23 没有检验；星流的质量（Koposov 等 2023：32.4 kpc 以内 2.85 × 10¹¹ M☉；Vasiliev 等 2021：100 kpc 以内 5.6 × 10¹¹ M☉）表明 30–100 kpc 有更多质量。

这些步骤没有编码进 Lean，因为一个文件只有一个结论；它们在第三部分检验（R2、R5）。

#### 2.4 Lean 检查发现的问题

1. **主要结果：`explicit_insufficient`，两个缺口。** 下降需要：平衡态金斯曲线在 19–26.5 kpc 准确（`gap_jeans`）；3σ 拒绝加上与 −0.5 相容的斜率算作探测到开普勒式下降（`gap_detect`）。没有标准知识能补上其中任何一个。
2. **重要性排序。** `gap_jeans` 最重要：下降幅度（15%）与后来估计的金斯偏差相当。`gap_detect` 与研究 008 中"3σ 即证据"的一步相同。
3. **在这种编码下六个前提都是必要的**，没有多余的。
4. **关于质量（2.3，不编码）：** 从 26.5 kpc 外推到 121 kpc 是最弱的一步；论文关于拟合用哪种误差的措辞前后不一。
5. **相容性**（`consistent`）在这里是弱检查：没有否定形式的前提。
6. **局限：** Lean 检查的是我们编码下的逻辑结构，不是每个前提内部的动力学。

### 第三部分 · 本项目可检验或探索的环节

所有输入都是由论文抄录的小表格（J23 表 3、表 4 与重子参数；O24 表 1；Eilers 等 2019 表 1），经两次独立抄录核对；不下载任何文件。J23 没有给出各箱的统计误差，所以（计划 018 的规则 E0）R1 像 J23 的幂律检验那样用表 3 的总误差，R2 是描述性拟合而不是复现。

| 环节 / 结论 | 能否检验或探索 | 方法 | 数据（大小） | 判据 | 结果 |
|---|---|---|---|---|---|
| 环节 B：平坦以 3σ 被拒绝（R1） | 现在可检验 | J23 式 13：用表 3 误差对 19 kpc 以外的 8 个箱拟合 V = A R^γ，γ 平坦先验 [−10, 5]；统计量 (0 − γ 中位数)/(84% 分位 − 中位数)；并报告 P(γ ≥ 0)、Δχ² 与逐箱剔除 | J23 表 3（0.3 kB） | γ 中位数在 −0.47 ± 0.05 以内且统计量在 3.1 ± 0.3σ 以内 → 复现 | 待定 |
| 环节 C：六个参数完整的重子模型的质量（R2） | 可探索（描述；J23 的统计误差未发表） | 用总误差、J23 的先验与 R_vir 定义，以爱纳斯托晕加重子拟合表 3，与表 4 比较 | J23 表 1、2、4（5 kB） | 无——描述（报告与表 4 之差） | 待定 |
| 环节 A：系统误差（R3） | 可探索（不能判决） | (a) 常数偏差：γ 的零对照，b = ±5%、±10% 时重拟质量；(b) 从 19 kpc 的 0 线性增加到 26.5 kpc 的 b_max 的偏差，扫描 0–20%，找使 R1 降到 2σ 以下的最小 b_max（人为注入的压力测试，文献幅度只作背景）；(c) 外区误差相关 | 同上 | 无——仅供探索 | 待定 |
| 其他曲线（R4） | 可探索（描述） | J23 与 O24、Eilers 等 2019 在重叠区的差异；在 O24 上做 R1（J23：γ = −0.56） | O24 表 1，Eilers 表 1（2 kB） | 无——描述 | 待定 |
| 环节 C：外推（R5） | 可探索（描述） | 数据约束的 M(<26.5 kpc) 对外推的 M(<32.4)、M(<100)、M_vir；拟合类似 NFW 的晕作对比；星流质量作跨模型的量级比较 | 同上 | 无——描述 | 待定 |
| `gap_jeans` 本身（非平衡动力学） | 不在范围内 | 需要六维恒星数据与超出金斯方程的动力学建模 | – | – | – |

### 术语表

| 术语 | 含义 |
|---|---|
| 旋转曲线（rotation curve） | 圆速度随银心距的变化 |
| 开普勒式下降（Keplerian decline） | V ∝ R^(−1/2)，如同绕点质量：这些半径处没有新增质量 |
| 金斯方程（Jeans equation） | 稳态系统中引力与恒星"压强"（随机运动）的平衡 |
| 交叉项（cross term） | ∂⟨v_R v_z⟩/∂z，速度椭球的倾斜，金斯方程中常被忽略 |
| 爱纳斯托轮廓（Einasto profile） | ρ(r) = ρ0 exp[−(r/h)^(1/n)]，外区陡度可调的暗物质密度规律 |
| 位力半径（virial radius） | 其内暗物质平均密度为临界密度 200 倍的半径 |
| 动力学质量（dynamical mass） | J23 对位力半径以内重子加暗物质的称呼 |

### 开放问题

- 在 20–27 kpc，偏离平衡（翘曲、外展、人马座、大麦哲伦云）对金斯圆速度的影响有多大？这需要本仓库以外的动力学建模。
- 是否存在既能拟合旋转曲线、又使外推质量与星流和卫星星系质量相容的晕形状？

### 研究进展

按时间倒序。

- 2026-11-15：闸门 1 第 2 轮：开普勒式的形状现在依靠单独的、论文明说的前提（`stat_kepler`，第 5.3 节）与缺口。
- 2026-11-15：闸门 1 审查：Lean 的结论改为开普勒式下降（两个缺口）；质量及其外推在 2.3 中讨论，不编码（质量拟合不用下降检验）；改正引文；误差措辞的不一致引用两句原文说明。
- 2026-11-15：第一版：第一至三部分（预注册的来源；计划 `design/018-plan_*`）。

### 来源

- Jiao 等 2023，A&A 678, A208，arXiv:2309.00048（本文研究的论文）。
- Ou, Eilers, Necib, Frebel 2024，MNRAS 528, 693，arXiv:2303.12838。
- Eilers, Hogg, Rix, Ness 2019，ApJ 871, 120，arXiv:1810.09466。
- Wang, Chrobáková, López-Corredoira, Sylos Labini 2023，ApJ 942, 12，arXiv:2211.05668。
- Koop 等 2024，A&A 692, A50，arXiv:2405.19028；Ou 等 2025，arXiv:2503.05877（金斯偏差）。
- Koposov 等 2023，arXiv:2211.04495；Vasiliev 等 2021，arXiv:2009.10726（星流质量）。
- Melchiorri & Ruchika 2026，arXiv:2608.10189（综述）。
