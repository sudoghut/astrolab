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
just below it. Others explain it by star clusters or by the physics of mass transfer. In GWTC-3.0
the strongly modeled Power Law + Peak fit placed a peak near 35 M☉; a break in the continuum near the
same mass was first found by Callister & Farr (2024) with a broken-power-law model.

#### 1.2 The data

GWTC-4.0 adds 128 new candidates from the first part of the fourth observing run (O4a) to the
earlier catalogues. For the black-hole population study P26 keeps binary black holes (BBHs) with a
false-alarm rate below one per year in at least one search pipeline and with both component masses
confidently above 3 M☉ (the 1% lower limit of each mass posterior, under the parameter-estimation
priors, above 3 M☉): 84 from O4a and 69 from GWTC-3.0, 153 in all. GW230529 fails the mass cut and
GW230630_070659 is excluded for data quality. Detectors see massive binaries further away than light ones, so the raw counts
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

For the 35 M☉ feature to be wrong, both the strongly and the weakly modeled routes would have to be
misled by something they share: errors in the selection function at high mass, systematic errors in
the event masses (P26 reports a likelihood normalisation error, for which it does not use the
corrected samples, and a calibration-prior error whose impact it expects to be negligible), or the expected noise events among the candidates (about 6.7 of the 161 compact-binary
candidates with FAR below one per year; a general contamination figure, not specific to 35 M☉).

### Part 2 · The logic of the argument

#### 2.0 Map of the argument

A. A selected sample of 153 BBHs → B. selection effects from injections, [gap] adequate at high mass
→ C. [gap] no spurious feature from parameter-estimation systematics or noise events → then either
D1. (strongly modeled) λ2 > λ1 at 97.7%, or D2. (weakly modeled) a B-spline local peak near 33.5 M☉
that agrees with the other flexible models ⇒ a feature at 35 M☉ (in the §6.1 sense: an over-density
or a break).

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

Scope: the conclusion encoded is the 35 M☉ part of the abstract's "features persist …", read in the
sense of §6.1 ("We identify a feature at 35 M⊙", consistent with either an over-density or a break).
The 10 M☉ peak and the 20 M☉ bump are discussed only here. Whether the 35 M☉ feature is an
over-density is discussed in 2.3, not encoded.

#### 2.1 Stage A · Sample and selection

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `obs_sample`: the analysed sample of 153 BBHs | OBS | stated 2508.18083: "which brings the total number of BBH events passing our FAR threshold to 153" | §6 |
| `mod_sel`: detection efficiency from injections | MOD | stated 2508.18083: "is estimated using these injections through a Monte Carlo integral" | §3.3 |
| `gap_sel`: that selection function is adequate at high mass | GAP | reconstructed | not tested at the relevant masses |

**Critique.** The sample can in principle be rebuilt from public lists (our R1). The selection
function needs injection files of hundreds of MB, outside this project's limits; its accuracy at
high mass is assumed, and it matters directly for a slope above 35 M☉.

#### 2.2 Stage B · Two routes to the feature

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `stat_steep`: λ2 > λ1 with credibility 97.7% (encoded as the reported value) | STAT | stated 2508.18083: "at 97.7% credibility" | §6.1 |
| `stat_bspline`: the B-spline has a local peak near 33.5 M☉ | STAT | stated 2508.18083: "which exhibits a local peak at" | §6.1 |
| `stat_weak`: it agrees with the other weakly modeled approaches | STAT | stated 2508.18083: "consistent with other models that employ a weakly modeled approach" | §6.1, App. D.4 |
| `gap_syst`: PE systematics and noise events make no spurious feature near 35 M☉ | GAP | reconstructed | not propagated in the paper |
| `gap_route1`: a credible slope change (with the above) is a feature in the §6.1 sense | GAP | reconstructed (P26 presents the slope result and then identifies a feature that may be a break, §6.1, but states no bridging rule) | not stated |
| `gap_route2`: an agreed flexible-model peak (with the above) is a feature | GAP | reconstructed (P26 says the B-Spline peak supports the over-density reading, but states no bridging rule) | not stated |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| One model shape forces a break | the second route (`stat_bspline`, `stat_weak`) | largely: strongly and weakly modeled fits agree that something lies near 35 M☉ (a break in one, a peak in the other) |
| Mass systematics or noise events near 35 M☉ | `gap_syst` | partly (errors reported, one judged negligible; not propagated) |
| Selection-function errors at high mass | `gap_sel` | no direct test |

**Inference (Lean excerpt).**

```lean
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  exact p .gap_route1 (p .obs_sample) (p .mod_sel) (p .gap_sel) (p .stat_steep)
    (p .gap_syst)  -- Sec. 3.3, 6, 6.1; GAPs
```

#### 2.3 Peak or break? (discussed, not encoded)

P26 §6.1 says the 35 M☉ feature is "consistent with either" an over-density peaking near 32.7 M☉ or a
plain break near 34.1 M☉, and that the former "is supported by the B-Spline model, which exhibits a
local peak at" 33.5 M☉. App. D.1: "the Bayes factors do not show strong support for one model over
another" (one peak against two, log10 B = −0.06), and the fiducial posterior has two modes (71% a
narrow peak, 29% close to a plain break). Whether "supported" amounts to "established" is a
judgement about evidence, not something a logical check can settle; on the Bayes factors alone the
peak is not preferred. The abstract's "We resolve multiple over- and under-densities" may refer to the
10 M☉ peak and the 20 M☉ bump; the abstract does not single out the 35 M☉ feature as an over-density.
An earlier version of our encoding contained a theorem that the over-density "does not follow"; the
gate-1 review showed it followed from our own encoding of the rule, so we removed it.

#### 2.4 What the Lean check found

1. **`explicit_insufficient`**: the chain needs the two shared gaps, an adequate selection function at
   high mass (`gap_sel`) and no spurious feature from parameter-estimation systematics or noise
   events (`gap_syst`), plus the bridging rule of at least one route (`gap_route1` or `gap_route2`):
   P26 presents the slope result and the B-spline peak and then identifies a feature, but does not
   state the rule that takes either result to a feature. (Two review rounds tried "implied" and then
   "stated" for these rules; neither fits, so they are gaps.)
2. **`stated_insufficient`**: what the paper states (sample, injections, the 97.7% slope result, the
   B-spline peak and its agreement with other flexible models) does not by itself give the feature.
3. **Two independent routes**: each route's statistical premise and bridging gap are redundant given
   the other route. Four premises are needed: the sample, the injection selection and the two shared
   gaps. Model shape is not a gap here because the two routes agree that something lies near 35 M☉
   (a break in one, a peak in the other); that each route alone suffices is our encoding, following
   §6.1's broad sense of feature, and the flexible fits carry their own smoothness priors.
4. **Consistency** holds; weak here (every premise is positive). `stated_insufficient` and
   `explicit_insufficient` share one countermodel (both gaps false); the `_needed` theorems show that
   each gap matters on its own.
5. **Limits.** Lean checks the logical structure under our encoding, not the physics.

```lean
inductive Field where
  | obs_sample    -- OBS [stated 2508.18083]
  | mod_sel       -- MOD [stated 2508.18083]
  | gap_sel       -- GAP [reconstructed]
  | stat_steep    -- STAT [stated 2508.18083]
  | stat_bspline  -- STAT [stated 2508.18083]
  | stat_weak     -- STAT [stated 2508.18083]
  | gap_syst      -- GAP [reconstructed]
  | gap_route1    -- GAP [reconstructed]
  | gap_route2    -- GAP [reconstructed]

theorem explicit_insufficient : ¬ ∀ v, Explicit v → Conclusion v := fun h =>
  h ⟨True, True, False, 977, True, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])
```

### Part 3 · What astrolab can test or explore

| Stage / claim | Can we test or explore it? | How | Data (size) | Decision criterion | Result |
|---|---|---|---|---|---|
| A: the 153-event sample (R1) | testable now | rebuild from GWOSC lists (GWTC-4.0, GWTC-1/2.1/3) with P26's cuts (FAR < 1/yr, 90% lower bound as a proxy for the 1% bound, exclusions); compare with the O4a list on Zenodo | GWOSC JSON (~0.25 MB + < 1 MB each), O4a list 10 kB | "reproduced" if the O4a events match P26's list and the counts are 84 and 69, with only pre-declared, direction-known differences; downgraded to "described" if the meaning of GWOSC's `far` cannot be confirmed (the `far` definition and the allowed number of discrepant events are fixed in the pre-registration before R1 runs) | **not reproduced** as registered: O4a 84/84 exact; O1–O3 59 of 69 ± 2 (null FARs on the GWTC-2.1 rows of the ten O1/O2 BBHs); 69 and 153 post hoc |
| Sample-level counts above and below 35 M☉ (R2) | explorable (descriptive) | median m1 counts against a single power law (λ1 = 1.7) times a toy VT(m1) with a turnover, scanning the turnover | same | none - descriptive (medians blur a break; 1-D VT is a toy) | 79 of 139 above 35 M☉ (0.57); deficit against the prediction unless VT turns over near 30 M☉ (ratio 0.69–0.80, or 1.15 at M_t = 30) |
| Steepening vs selection curvature (R3) | explorable (not decisive) | point-estimate toy fit of a broken power law, with and without a peak, scanning the VT turnover | same | none - exploration only | A steepens at 42–45 M☉ for M_t ≥ 50 (reverses at M_t = 30); a peak adds 2Δln L = 15–25 at μ = 33–40 M☉, but fits sit on bounds; with wider bounds (post hoc) the bump is at 34–39 M☉ for M_t ≤ 80 and broad and bound-limited at M_t = ∞ |
| GW231123 (R4) | descriptive | its total mass within the rebuilt sample (not P26's quantity) | same | none | 236 M☉, the heaviest of 143 (and of 153) |
| `gap_sel`, `gap_syst`, population inference | out of scope | needs posterior samples and injections (hundreds of MB to tens of GB; AGENTS.md 1.5) | – | – | – |

**Results (added after the run, 2026-11-15; the table above keeps the pre-registered design).**
Details: [study README section 5](https://github.com/sudoghut/astrolab/blob/main/studies/007-m10-gwtc4-bbh-mass-35msun/README.md#5-results); page:
[`web/index.html`](https://github.com/sudoghut/astrolab/blob/main/studies/007-m10-gwtc4-bbh-mass-35msun/web/index.html).

- **R1 is "not reproduced" by the frozen rule, and the reason is mundane.** The O4a half matches
  P26 exactly: 84 events, none missing and none extra. The O1–O3 half gives 59 instead of 69.
  - Under our registered precedence (newest catalogue first), the ten O1/O2 BBHs are taken from
    GWTC-2.1, which re-analysed their masses.
  - GWOSC stores no false-alarm rate on those re-analysed rows, while the GWTC-1 rows of the same
    events carry one.
  - Our rule "no FAR → excluded" therefore drops all ten. Taking the FAR from GWTC-1 for them (a
    labelled post-hoc exploration) gives exactly 69, and 84 + 69 = 153, P26's sample.
  - The sample can be rebuilt; the public lists just need a FAR fallback that the pre-registration
    did not foresee. The independent referee found the same cause without seeing our diagnosis.
- **R2 (counts).** 79 of 139 events lie above 35 M☉.
  - Against a single power law times a toy selection function, that is a deficit unless the
    selection stops rising near 30 M☉.
  - The low bin contains the 10 M☉ peak, and ten medians pile up just above 35 M☉, so this is
    descriptive only.
  - Single-event mass uncertainties at 30–40 M☉ are about 45% of the mass (median 90% width).
- **R3 (toy fits).** The answer depends on the toy selection function, which is what
  section 2.3 predicted.
  - A plain broken power law steepens at 42–45 M☉ when the selection keeps rising.
  - Adding a Gaussian bump improves the fit by 2Δln L = 15–25 (17–27 with the post-hoc 153 events).
  - With the registered bounds the bump fits sit on the bounds. With wider bounds (post hoc) the
    bump sits at 34–39 M☉ when the toy selection turns over by 80 M☉, but becomes a broad
    (σ ≈ 15 M☉) shoulder pressed against the 25 M☉ lower limit of the peak centre when it does not.
  - Whether "35 M☉" is a peak or a bend therefore cannot be settled without the real,
    injection-based selection function. That needs data this project does not download.
- **R4.** GW231123 (236 M☉ total) is the heaviest event in the sample by a wide margin, so its
  percentile (100) carries little information.
- **Side effect.** The first run exposed a cache bug in the core library: a `.json` download
  overwrote its own metadata file. It was fixed, with a regression test, in the same pull request.

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

- 2026-11-15: results: R1 not reproduced as registered (O4a 84/84 exact; O1–O3 59, because the GWTC-2.1 rows of the ten O1/O2 BBHs have no FAR on GWOSC; 153 post hoc); R2–R4 results; referee notes; R3 wide-bounds exploration.
- 2026-11-15: gate-2 review: the route bridging rules are neither standard knowledge nor stated in P26; they are now gaps (`gap_route1`, `gap_route2`); the slope premise encodes the reported 97.7%.
- 2026-11-15: gate-1 review: two routes (strongly and weakly modeled) with two shared gaps (`gap_sel`, `gap_syst`); the over-density theorem removed (it followed from our own rule); quotes re-sourced.
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

两个黑洞旋近（inspiral）并合时发出的引力波被 LIGO、Virgo 与 KAGRA 探测器记录下来，每个信号都给出两个黑洞的质量。事件足够多时，就可以问黑洞的质量如何分布：是平滑地铺开，还是某些质量出现得更频繁？这种分布中的特征是双星如何形成的线索。约 35 倍太阳质量（35 M☉）处的堆积从最早的目录起就有讨论；一种解释是，极大质量的恒星会因"对不稳定"（pair instability）过程损失质量或被瓦解，在约 50–60 M☉ 以上留下空缺，使黑洞堆积在其下方。另一些解释诉诸星团或质量转移的物理。在 GWTC-3.0 中，强模型化的 Power Law + Peak 拟合把峰放在约 35 M☉；连续谱在同一质量附近的折断，最早由 Callister & Farr（2024）用折断幂律模型发现。

#### 1.2 数据

GWTC-4.0 在早期目录之外加入了第四观测期前半段（O4a）的 128 个新候选体。在黑洞群体研究中，P26 保留至少一个搜索管线中误报率（FAR, false-alarm rate）低于每年一次、且两个分量质量都可靠地高于 3 M☉（在参数估计（PE, parameter estimation）先验下，每个质量后验的 1% 下限高于 3 M☉）的双黑洞（BBH）：O4a 84 个，GWTC-3.0 69 个，共 153 个。GW230529 不满足质量条件，GW230630_070659 因数据质量被排除。探测器能看到更远处的大质量双星，所以原始计数有偏；P26 用经过同样搜索管线的模拟信号（"注入"，injection）来改正，并用蒙特卡罗积分计算任意群体的探测概率。

#### 1.3 一步一步：作者如何从数据走到结论

**(a) 模型。** P26 对 153 个事件拟合两类模型："强模型化"（strongly modeled）的有固定形状（基准为 Broken Power Law + 2 Peaks：两段幂律在折断质量（break mass）处相接，再加两个高斯峰），"弱模型化"（weakly modeled）的几乎可以取任意形状（B 样条与分箱高斯过程）。每个事件的质量不确定性与选择效应都进入似然。

**(b) 35 M☉ 以上变陡。** 35 M☉ 以下连续谱按 m1^(−1.7) 下降，以上按 m1^(−4.5)。P26：λ2 > λ1"at 97.7% credibility"。

*粗略估算。* 用这两个斜率，在 70 M☉ 处每单位质量的并合率是单一幂律的 (70/35)^−(4.5−1.7) = 2^−2.8 ≈ 0.14，即很重的黑洞约少七倍。

**(c) 峰还是折断？** P26 第 6.1 节：35 M☉ 的特征"consistent with either"在折断幂律之上峰值约 32.7 M☉ 的过密，或约 34.1 M☉ 的单纯折断。弱模型化的 B 样条"exhibits a local peak at" 33.5 M☉。在含折断幂律的模型中，"the Bayes factors do not show strong support for one model over another"：一个峰对两个峰的 log10 B = −0.06，基准模型的后验有两个模态（mode）（71% 窄峰，29% 接近单纯折断）。附录 D.1：这一特征"may be an overdensity"或"could mark the onset of a decline in the merger rate"。

**(d) 其他特征。** 10 M☉ 的全局峰在各模型中都稳健；"a bump near 20 M⊙ is present in some of the weakly modeled approaches"（20 M☉ 附近的隆起（bump）），强模型化的比较不能确定（log10 B = −0.34）。局部并合率为 14–26 Gpc⁻³ yr⁻¹（两种模型 90% 区间的并集）。最重的事件 GW231123（约 137 + 101 M☉）与推断的质量谱相容。

#### 1.4 结论与把握程度

摘要："We resolve multiple over- and under-densities in the black hole mass distribution: features persist at primary masses of 10 M⊙ and 35 M⊙ with a possible third feature at 20 M⊙. These are departures from an otherwise power-law-like continuum that steepens above 35 M⊙." 变陡的可信度为 97.7%；35 M☉ 的特征是峰还是只是弯折，正文中没有定论。

35 M☉ 的特征若要不成立，强模型化与弱模型化两条途径都必须被它们共有的东西误导：高质量处选择函数的误差、事件质量的系统误差（P26 报告了一个似然归一化错误，没有使用改正后的样本，以及一个它认为影响可忽略的校准先验错误），或候选体中预期的噪声事件（FAR 低于每年一次的 161 个致密双星并合（CBC, compact binary coalescence）候选体中约 6.7 个；这是总体的污染估计，并非针对 35 M☉）。

### 第二部分 · 论证逻辑

#### 2.0 论证地图

A. 选出的 153 个 BBH 样本 → B. 由注入得到的选择效应，[缺口] 在高质量处适当 → C. [缺口] 参数估计的系统误差与噪声事件不会造成虚假的特征 → 然后经由 D1.（强模型化）λ2 > λ1 的可信度（credibility）97.7%，或 D2.（弱模型化）B 样条在约 33.5 M☉ 的局部峰、且与其他灵活模型一致 ⇒ 35 M☉ 处有特征（第 6.1 节意义上：过密或折断）。

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

编码范围：编码的结论是摘要"features persist …"中关于 35 M☉ 的部分，按第 6.1 节的意义理解（"We identify a feature at 35 M⊙"，可以是过密也可以是折断）。10 M☉ 的峰与 20 M☉ 的隆起只在这里讨论。35 M☉ 的特征是否是过密，在 2.3 中讨论，不编码。

#### 2.1 环节 A · 样本与选择

| 前提（Lean 构造子） | 标签 | 出处性质 | 论文出处 |
|---|---|---|---|
| `obs_sample`：分析的 153 个 BBH 样本 | OBS | stated 2508.18083："which brings the total number of BBH events passing our FAR threshold to 153" | 第 6 节 |
| `mod_sel`：由注入得到探测效率 | MOD | stated 2508.18083："is estimated using these injections through a Monte Carlo integral" | 第 3.3 节 |
| `gap_sel`：这一选择函数在高质量处适当 | GAP | reconstructed | 在相关质量处没有检验 |

**评析。** 样本原则上可以由公开列表重建（本研究的 R1）。选择函数需要数百 MB 的注入文件，超出本项目的上限；它在高质量处的准确性是假定的，而它直接影响 35 M☉ 以上的斜率。

#### 2.2 环节 B · 通向特征的两条途径

| 前提（Lean 构造子） | 标签 | 出处性质 | 论文出处 |
|---|---|---|---|
| `stat_steep`：λ2 > λ1 的可信度 97.7%（按报告值编码） | STAT | stated 2508.18083："at 97.7% credibility" | 第 6.1 节 |
| `stat_bspline`：B 样条在约 33.5 M☉ 有局部峰 | STAT | stated 2508.18083："which exhibits a local peak at" | 第 6.1 节 |
| `stat_weak`：它与其他弱模型化方法一致 | STAT | stated 2508.18083："consistent with other models that employ a weakly modeled approach" | 第 6.1 节、附录 D.4 |
| `gap_syst`：参数估计的系统误差与噪声事件不会在 35 M☉ 附近造成虚假的特征 | GAP | reconstructed | 论文没有传播 |
| `gap_route1`：（在上述条件下）可信的斜率变化即第 6.1 节意义上的特征 | GAP | reconstructed（P26 先给出斜率结果，再认定一个可能是折断的特征（第 6.1 节），但没有写出这一桥接规则） | 论文没有写 |
| `gap_route2`：（在上述条件下）各灵活模型一致的峰即特征 | GAP | reconstructed（P26 说 B 样条的峰支持过密的解读，但没有写出这一桥接规则） | 论文没有写 |

**其他解释（rival explanations）。**

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 某一种模型形状强加了折断 | 第二条途径（`stat_bspline`、`stat_weak`） | 大体上：强模型化与弱模型化的拟合都在约 35 M☉ 处有东西（一个是折断，一个是峰） |
| 35 M☉ 附近的质量系统误差或噪声事件 | `gap_syst` | 部分（报告了错误，其中一个判断为可忽略；没有传播） |
| 高质量处选择函数的误差 | `gap_sel` | 没有直接检验 |

**推理（Lean 摘录）。**

```lean
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  exact p .gap_route1 (p .obs_sample) (p .mod_sel) (p .gap_sel) (p .stat_steep)
    (p .gap_syst)  -- Sec. 3.3, 6, 6.1; GAPs
```

#### 2.3 峰还是折断？（只讨论，不编码）

P26 第 6.1 节说 35 M☉ 的特征"consistent with either"峰值约 32.7 M☉ 的过密或约 34.1 M☉ 的单纯折断，并说前者"is supported by the B-Spline model, which exhibits a local peak at" 33.5 M☉。附录 D.1："the Bayes factors do not show strong support for one model over another"（一个峰对两个峰的 log10 B = −0.06），基准模型的后验有两个模态（71% 窄峰，29% 接近单纯折断）。"有支持"是否等于"已确立"，是对证据的判断，逻辑检查无法裁定；仅就贝叶斯因子而言，峰并不被偏好。摘要中的"We resolve multiple over- and under-densities"可能指 10 M☉ 的峰与 20 M☉ 的隆起；摘要并没有单独说 35 M☉ 的特征是过密。我们编码的早期版本里有一条"过密推不出"的定理；闸门 1 审查指出它是由我们自己写的规则推出的，所以已删除。

#### 2.4 Lean 检查发现的问题

1. **`explicit_insufficient`**：链条需要两个共同的缺口，即高质量处的选择函数适当（`gap_sel`）、参数估计的系统误差与噪声事件不会造成虚假的特征（`gap_syst`），再加上至少一条途径的桥接规则（`gap_route1` 或 `gap_route2`）：P26 给出斜率结果与 B 样条的峰，然后认定一个特征，但没有写出从任一结果到特征的规则。（两轮审查先后尝试了 implied 与 stated 两种标注，都不合适，所以它们是缺口。）
2. **`stated_insufficient`**：论文明说的内容（样本、注入、97.7% 的斜率结果、B 样条的峰及其与其他灵活模型的一致）本身推不出特征。
3. **两条独立的途径**：有了另一条途径，每条途径的统计前提与桥接缺口都是多余的。必要的前提有四个：样本、注入的选择效应与两个共同的缺口。这里模型形状不是缺口，因为两条途径都在约 35 M☉ 处有东西（一个是折断，一个是峰）；每条途径单独就足够，是我们按第 6.1 节宽泛的"特征"含义所作的编码，而且灵活模型也有它们自己的平滑先验。
4. **相容性**成立；在这里分量较弱（所有前提都是肯定命题）。`stated_insufficient` 与 `explicit_insufficient` 共用一个反例模型（两个缺口都不成立）；各自的 `_needed` 定理表明每个缺口单独都起作用。
5. **局限。** Lean 检查的是在我们的编码下的逻辑结构，不检查物理。

```lean
inductive Field where
  | obs_sample    -- OBS [stated 2508.18083]
  | mod_sel       -- MOD [stated 2508.18083]
  | gap_sel       -- GAP [reconstructed]
  | stat_steep    -- STAT [stated 2508.18083]
  | stat_bspline  -- STAT [stated 2508.18083]
  | stat_weak     -- STAT [stated 2508.18083]
  | gap_syst      -- GAP [reconstructed]
  | gap_route1    -- GAP [reconstructed]
  | gap_route2    -- GAP [reconstructed]

theorem explicit_insufficient : ¬ ∀ v, Explicit v → Conclusion v := fun h =>
  h ⟨True, True, False, 977, True, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])
```

### 第三部分 · 本项目可检验或探索的环节

| 环节 / 结论 | 能否检验或探索 | 方法 | 数据（大小） | 判据 | 结果 |
|---|---|---|---|---|---|
| A：153 个事件的样本（R1） | 现在可检验 | 按 P26 的条件（FAR < 1/yr、以 90% 下限近似 1% 下限、排除项）由 GWOSC 列表（GWTC-4.0、GWTC-1/2.1/3）重建；与 Zenodo 上的 O4a 列表比较 | GWOSC JSON（约 0.25 MB，其余各 < 1 MB），O4a 列表 10 kB | O4a 事件与 P26 列表一致、计数为 84 与 69，只允许预先声明且方向已知的差别 → "复现"；若不能确认 GWOSC `far` 的含义则降为"描述"（`far` 的定义与允许的不一致事件数在 R1 运行前的预注册中写定） | 按预注册规则**未复现**：O4a 84/84 完全一致；O1–O3 为 59，目标 69 ± 2（十个 O1/O2 双黑洞的 GWTC-2.1 行没有 FAR）；事后为 69 与 153 |
| 35 M☉ 上下的样本计数（R2） | 可探索（描述） | 中位数 m1 的计数，与单一幂律（λ1 = 1.7）乘以带转折的玩具 VT(m1) 比较，扫描转折质量 | 同上 | 无——描述（中位数会抹平折断；一维 VT 是玩具） | 139 个中 79 个在 35 M☉ 以上（0.57）；除非 VT 在约 30 M☉ 转平，否则少于预测（比值 0.69–0.80；M_t = 30 时为 1.15） |
| 变陡对选择函数曲率的敏感度（R3） | 可探索（不能判决） | 折断幂律（加或不加峰）的点估计玩具拟合，扫描 VT 的转折 | 同上 | 无——仅供探索 | M_t ≥ 50 时 A 在 42–45 M☉ 变陡（M_t = 30 时反向）；加峰使 2Δln L 增加 15–25，μ = 33–40 M☉，但拟合落在边界；放宽边界后（事后），M_t ≤ 80 时峰在 34–39 M☉，M_t = ∞ 时变成贴着边界的宽包 |
| GW231123（R4） | 描述 | 它的总质量在重建样本中的位置（与 P26 的量不同） | 同上 | 无 | 236 M☉，143 个（以及 153 个）中最重 |
| `gap_sel`、`gap_syst`、群体推断 | 不在范围内 | 需要后验样本与注入（数百 MB 到数十 GB；AGENTS.md 1.5） | – | – | – |

**结果（运行后补写，2026-11-15；上表保留预注册时的设计）。** 细节见
[研究 README 第 5 节](https://github.com/sudoghut/astrolab/blob/main/studies/007-m10-gwtc4-bbh-mass-35msun/README.md#5-results)；网页：[`web/index.html`](https://github.com/sudoghut/astrolab/blob/main/studies/007-m10-gwtc4-bbh-mass-35msun/web/index.html)。

- **按冻结的规则，R1 为"未复现"，原因很平常。** O4a 一半与 P26 完全一致：84 个事件，不缺不多。O1–O3 一半得到 59 个而不是 69 个。
  - 按我们预注册的优先级（较新的星表优先），十个 O1/O2 双黑洞取自重新分析过质量的 GWTC-2.1。
  - GWOSC 在这些重新分析的行上没有存误报率（FAR, false alarm rate），而同一批事件在 GWTC-1 中的行有。
  - 规则"没有 FAR → 排除"于是去掉了这十个。为它们改从 GWTC-1 取 FAR（标明为事后（post hoc）探索），得到正好 69 个，84 + 69 = 153，正是 P26 的样本。
  - 样本可以重建，只是公开列表需要一条预注册没有预见到的 FAR 回退规则。独立审稿在看不到我们诊断的情况下找到了同一原因。
- **R2（计数）。** 139 个事件中有 79 个在 35 M☉ 以上。
  - 与单一幂律乘以玩具选择函数相比，除非选择效应在约 30 M☉ 就不再上升，否则高质量端偏少。
  - 低质量格包含 10 M☉ 峰，而且有十个中位数扎堆在 35 M☉ 稍上方，所以这只是描述。
  - 30–40 M☉ 处单个事件的质量不确定度约为质量的 45%（90% 宽度中位数）。
- **R3（玩具拟合）。** 答案取决于玩具选择函数，正如第 2.3 节所预料。
  - 选择效应持续上升时，普通折断幂律在 42–45 M☉ 变陡。
  - 加一个高斯包使拟合改善 2Δln L = 15–25（事后 153 个事件时为 17–27）。
  - 用预注册的边界时，加包的拟合落在边界上。放宽边界后（事后），玩具选择函数在 80 M☉ 以内转平时包位于 34–39 M☉；不转平时变成贴着峰中心 25 M☉ 下限的宽肩（σ ≈ 15 M☉）。
  - 所以"35 M☉"是峰还是弯折，没有真实的、基于注入（injection）的选择函数就无法确定，而那需要本项目不下载的数据。
- **R4。** GW231123（总质量 236 M☉）在样本中遥遥领先地最重，所以它的百分位（100）几乎没有信息量。
- **附带发现。** 第一次运行暴露了核心库的缓存缺陷：`.json` 下载会覆盖自己的元数据文件。已在同一个拉取请求（PR, pull request）中修复并加回归测试。

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

- 2026-11-15：结果：R1 按预注册规则未复现（O4a 84/84 完全一致；O1–O3 为 59，因为十个 O1/O2 双黑洞的 GWTC-2.1 行在 GWOSC 上没有 FAR；事后为 153）；R2–R4 结果；审稿意见；R3 放宽边界的探索。
- 2026-11-15：闸门 2 审查：途径的桥接规则既不是标准知识，也没有在 P26 中明说，现在是缺口（`gap_route1`、`gap_route2`）；斜率前提按报告的 97.7% 编码。
- 2026-11-15：闸门 1 审查：两条途径（强模型化与弱模型化）与两个共同的缺口（`gap_sel`、`gap_syst`）；删除过密定理（它由我们自己的规则推出）；引文改换出处。
- 2026-11-15：第一版：第一至三部分（预注册的来源；计划 `design/016-plan_*`）。

### 来源

- 同英文部分。
