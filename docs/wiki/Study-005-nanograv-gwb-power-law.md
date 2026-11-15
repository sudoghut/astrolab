# NANOGrav 15 yr: how loud is the gravitational-wave background, and is that what black-hole binaries predict?

[English](#english) · [中文](#中文)

*Paper(s): Agazie et al. 2023, ApJL 951, L8, arXiv:2306.16213 (main paper, "L8"); Agazie et al. 2023, ApJL 952, L37, arXiv:2306.16220, erratum ApJL 1006, L67 (2026) (the SMBHB companion, "L37"); Lamb, Taylor & van Haasteren 2023, PRD 108, 103019, arXiv:2303.15442 (the refitting method); Afzal et al. 2023, ApJL 951, L11, arXiv:2306.16219 (new-physics context). Study:
[`studies/005-m09-nanograv-gwb-power-law`](https://github.com/sudoghut/astrolab/tree/main/studies/005-m09-nanograv-gwb-power-law).
Status: planned. Last updated: 2026-11-14 (see the
changelog at the end). The source of this page lives in the main repository at
[`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki); edit it there.*

*中文标题：NANOGrav 15 年：引力波背景有多强？这是黑洞双星所预言的吗？状态：计划中。论文：Agazie 等 2023, ApJL 951, L8, arXiv:2306.16213（主论文，"L8"）；Agazie 等 2023, ApJL 952, L37, arXiv:2306.16220，勘误 ApJL 1006, L67（2026）（SMBHB 姊妹论文，"L37"）；Lamb, Taylor & van Haasteren 2023, PRD 108, 103019, arXiv:2303.15442（重拟方法）；Afzal 等 2023, ApJL 951, L11, arXiv:2306.16219（新物理背景）。研究：[`studies/005-m09-nanograv-gwb-power-law`](https://github.com/sudoghut/astrolab/tree/main/studies/005-m09-nanograv-gwb-power-law)。最后更新：2026-11-14（见文末"研究进展"）。本页源文件在主仓库的 [`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki) 中，请在那里修改。*

---

## English

### Part 1 · The paper in plain language

#### 1.1 The question and why it matters

Gravitational waves are ripples in spacetime. LIGO and Virgo hear them at hundreds of hertz, from
stellar-mass black holes merging in a fraction of a second. Much heavier pairs, supermassive black
holes of 10⁸–10¹⁰ solar masses left behind when galaxies merge, orbit each other for millions of
years and radiate at nanohertz frequencies: one cycle every few years. No single pair is loud
enough to pick out yet, but the whole Universe's population of them should add up to a faint,
random "hum", a gravitational-wave background (GWB).

Theory makes two predictions about that hum. Its loudness is set by how many such binaries
there are, how massive they are and how they evolve, so measuring it constrains galaxy evolution.
And if the binaries lose energy only by gravitational radiation, on circular orbits, the hum has
a definite shape: the characteristic strain falls with frequency as f^(−2/3); equivalently the
power spectrum of timing residuals falls as f^(−γ) with γ = 13/3. A different γ, or an amplitude
far from the predictions, would hint at other physics: binaries steered by stars and gas,
eccentric orbits, or sources in the early Universe (cosmic strings, phase transitions; L11).

In June 2023 NANOGrav and other pulsar timing arrays (PTAs) reported evidence for this hum.
L8 is NANOGrav's evidence paper. This study asks two narrow questions about it: can a laptop
recover L8's numbers for the loudness (amplitude) and slope (spectral index) from NANOGrav's
published compressed data product, and how does the amplitude compare with the published
model predictions that L37 collects?

#### 1.2 The data

Millisecond pulsars are spinning neutron stars whose radio pulses arrive with clock-like
regularity. NANOGrav timed 68 of them (67 used for the GWB search) with the Arecibo, Green
Bank and VLA telescopes for up to 16 years. A passing gravitational wave stretches and squeezes
the space between Earth and each pulsar, so pulses arrive slightly early or late: the "timing
residuals", of order hundreds of nanoseconds. Over the dataset span T = 16.03 years
(L8 §II, footnote 2), the lowest frequency one can resolve is f₁ = 1/T ≈ 1.98 nHz; L8 models the
signal with the 14 lowest frequencies, f_k = k/T for k = 1…14 (about 2–28 nHz).

The key extra: a background from many sources leaves a specific pattern in how the residuals of
different pulsars correlate with each other as a function of their angular separation on the sky,
the Hellings–Downs (HD) curve. Detecting that pattern is what distinguishes a GWB from, say, a
clock error. Measuring the HD significance needs the full timing data and heavy software; this
study does not attempt it.

What this repo uses instead is a compressed product (Lamb, Taylor & van Haasteren 2023). NANOGrav
first fits a "free spectrum": at each frequency f_k, an independent power ρ_k (the root of the
timing-residual power at that frequency, in seconds), with every pulsar's own noise marginalised.
For each k the posterior of log10 ρ_k is stored as a kernel density estimate (KDE) evaluated on a
fixed grid. Multiplying these one-dimensional densities approximates the likelihood of any
spectral model (the "factorised likelihood"), so a power law can be refitted in seconds. The
product is on Zenodo: v2.0.0 (record 21844115, 2026, `ceffyl_data.zip`, 3.0 MB; fixes a
parallel-tempering sampler bug that biased the posteriors) and v1.1.0 (record 10344086, 5.3 MB).

#### 1.3 Step by step: how the authors got from data to conclusion

**(a) The power-law model.** The residual power at frequency f is
S(f) = A²/(12π²) · f_yr⁻³ · (f/f_yr)^(−γ), with f_yr = 1/yr. In free-spectrum terms
ρ_k² = S(f_k)/T (Lamb+2023, eq. 8–9). A is the strain amplitude at the reference frequency 1/yr.

*Back of the envelope.* For A = 2.4 × 10⁻¹⁵, γ = 13/3 and T = 16.03 yr,
ρ₁ ≈ 0.7 μs at 2 nHz, falling to ρ₁₄ ≈ 2 ns at 28 nHz: the signal is a slow wander of a few
hundred nanoseconds, strongest at the longest periods, which is why decade-long datasets are
needed.

**(b) The amplitude at γ = 13/3.** Fixing γ to the circular-binary value and fitting A with the HD
correlations, L8 finds A = 2.4 (+0.7/−0.6) × 10⁻¹⁵ (median, 90% credible interval). The prior
on log10 A is uniform on [−18, −14] (L8 Appendix B, Table 1).

**(c) The free spectral index.** Letting γ vary (prior uniform on [0, 7]; log10 A on [−18, −11]),
L8 finds A = 6.4 (+4.2/−2.7) × 10⁻¹⁵ and γ = 3.2 ± 0.6 (median, 5–95% quantiles). A and γ are
strongly correlated (a shallower slope and a larger amplitude at 1/yr can describe the same
low-frequency power). L8 calls the γ posterior "in moderate tension" with 13/3; Fig. 1's caption
says γ = 13/3 "is included in the 99% credible region".

**(d) The comparison with astrophysics.** L8 states (§III) that "These amplitudes are compatible
with astrophysical expectations of a GWB from inspiraling SMBHBs", and points to the companion
L37 for the detail. L37 compares the amplitude with its own population simulations
(the `holodeck` libraries, shown only as figures) and, in its Appendix A (Table A1, Fig. A1), with
published predictions from the literature (24 rows), each given as the 16th and 84th
percentiles of A_yr. Examples: Kulier et al. 1.58–2.51 × 10⁻¹⁵, McWilliams et al.
1.07–15.1 × 10⁻¹⁵ and Sesana et al. [171] 0.115–2.88 × 10⁻¹⁵ contain 2.4 × 10⁻¹⁵;
Simon 1.46–2.26 × 10⁻¹⁵ does not. In L37's words the amplitudes are within the range of some of
these model predictions but lie at the high-amplitude end. With its own populations L37 (§V)
reports that "we are able to reproduce the inferred GWB amplitude and spectral shape", while its
abstract says this needs either many parameters at the edges of expected values or a few notably
different from standard expectations. L37's 2026 erratum fixed a galaxy-mass-function bug and a sampler bug and
states that its conclusions do not change.

#### 1.4 What they conclude, and how sure they are

- **Evidence for a GWB** (HD correlations; Bayes factor 200–1000, roughly 3–4σ depending on the
  statistic): strong evidence, not a 5σ detection. Not examined here.
- **Amplitude** 2.4 × 10⁻¹⁵ at γ = 13/3 (and 6.4 × 10⁻¹⁵ with γ free), in line with SMBHB
  expectations. The abstract says "consistent with astrophysical expectations", §III says
  "These amplitudes are compatible" (both amplitudes); the discussion (§VI) adds that it is
  "toward the upper end of predictions", implying relatively high black-hole masses and binary
  fractions.
- **Spectral index** 3.2 ± 0.6, in moderate tension with 13/3, which the authors say can be
  accommodated by environmental effects, eccentricity or cosmic variance; more exotic sources
  cannot be excluded (L11 explores them).

For the amplitude claim to be wrong, one of these would have to fail: the free-spectrum and
power-law fits estimate A correctly (it could be biased by noise mismodelling or by the sampler
bug the 2026 data product fixes); and the published models that contain A are representative of
what astrophysics expects (otherwise "inside the range of some models" overstates the agreement).

### Part 2 · The logic of the argument

#### 2.0 Map of the argument

A. L8 measures A at γ = 13/3 → B. compatibility with some models, by either of two routes:
B1. A lies within the predicted range of at least one published model (L37 Table A1), or
B2. L37's own holodeck populations reproduce A → C. [gap] those models represent
"astrophysical expectations" ⇒ the γ = 13/3 amplitude is compatible with astrophysical
expectations of a GWB from SMBHBs.

How we check it: the argument is written in Lean 4
([`studies/005-m09-nanograv-gwb-power-law/argument/Argument.lean`](https://github.com/sudoghut/astrolab/blob/main/studies/005-m09-nanograv-gwb-power-law/argument/Argument.lean)).
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

Scope of the encoding: only the amplitude sentence of §III is formalised, and only in part.
"These amplitudes" there refers to both the γ = 13/3 amplitude (2.4 × 10⁻¹⁵) and the free-γ
amplitude (6.4 × 10⁻¹⁵); we encode only the first, because the published predictions are quoted
at a fixed spectral shape, so comparing them with a γ ≈ 3.2 amplitude is not like for like
(6.4 × 10⁻¹⁵ falls inside only one Table A1 range, McWilliams et al.); this reason concerns
route 1, while route 2 (the holodeck populations) is compared by L37 with the spectrum itself. The encoded conclusion is
therefore weaker than the paper's sentence. The spectral-index
statement (γ < 13/3 "can be accommodated" by mechanisms the paper does not quantify), the
statement that exotic sources cannot be excluded, and the HD significance are left out: the
first two are not precise enough to encode as a chain, and the third needs data this repo does
not use.

#### 2.1 Stage A · The amplitude measurement

**Overview.** Everything rests on the posterior for A at γ = 13/3.

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `stat_amp`: A at γ = 13/3 has been inferred, median ≈ 2.4 × 10⁻¹⁵ | STAT | stated 2306.16213: "the strain amplitude is 2.4−0.6+0.7×10−15 (median + 90% credible interval) at a reference frequency of 1 yr−1" | Abstract; §III |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| The common red process is not a GWB (e.g. unmodelled pulsar noise) | none (taken as given; the HD evidence is outside this encoding) | partly: HD Bayes factor 200–1000, not 5σ |
| The amplitude estimate is biased by the sampler | none | no (L8 predates the 2026 fix); explored by R3 (v1.1.0 vs v2.0.0) |

**Critique.** A STAT premise taken from the paper; our study recomputes it (R1) from the
compressed product, which approximates the full likelihood (Lamb+2023 found a Hellinger distance
of 0.13 for the free-spectrum refit on NANOGrav's 12.5-year data, apparently for the joint
posterior; the 1-D log10 A marginal in that case study was 0.06, and over 100 simulated
realisations the 2-D distance had a median of 0.26, 16th–84th percentile 0.17–0.40).

#### 2.2 Stage B · Compatible with some models (two routes)

**Overview.** The amplitude is compatible with at least one SMBHB-population model, either a
published prediction whose range contains it (route 1) or one of L37's holodeck populations
that reproduces it (route 2).

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `num_contain`: at least one Table A1 model's 16–84% range contains the median amplitude | NUM | stated 2306.16220: "Although the inferred GWB amplitudes are within the range of some of these model predictions"; bound to `results/r2b.json:n_models_contain_median >= 1` | L37 §V; Table A1, Fig. A1 |
| `mod_contain`: a value inside a model's 16–84% predicted range is not in tension with that model | MOD | implied (posterior predictive reasoning; Gelman et al. 2013, *Bayesian Data Analysis*, ch. 6) | – |
| `stat_holo`: some holodeck populations reproduce the inferred amplitude and spectral shape | STAT | stated 2306.16220: "we are able to reproduce the inferred GWB amplitude and spectral shape" | L37 §V |
| `mod_holo`: a population that reproduces the measured amplitude is not in tension with it | MOD | implied (Gelman et al. 2013, ch. 6); L37 compares the populations with the 15 yr spectrum, so applying this to the γ = 13/3 amplitude is our reading | – |

The quote of `num_contain` is about the inferred amplitudes (the posteriors); our binding uses the
posterior median, which is our operationalisation.

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| A lies outside every model's range | `num_contain` (route 1), `stat_holo` (route 2) | yes (L37 §V, App. A) |

**Inference (Lean excerpt).**

```lean
have h1 : v.CompatModels := p .mod_contain (p .stat_amp) (p .num_contain)  -- Sec. III; L37 Sec. V
```

**Critique.** "Within the range" of a 68% interval is a weak requirement: a model with a very wide
range (McWilliams et al., 1.07–15.1 × 10⁻¹⁵) contains almost any plausible amplitude, and at
least three Table A1 rows (Kulier et al., McWilliams et al., Sesana et al. [171]) contain
2.4 × 10⁻¹⁵, so `n_contain ≥ 1` is nearly guaranteed and discriminates weakly. Each route alone
suffices, so in the encoding each route's premises are redundant (see 2.4); our NUM test checks
route 1 only.

#### 2.3 Stage C · From some models to "expectations"

**Overview.** The paper's sentence is about astrophysical expectations, not about particular models.

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `gap_repr`: the models (published predictions or holodeck populations) that contain or reproduce A stand for astrophysical expectations in general | GAP | reconstructed | not in the paper; L37 says the amplitude needs parameters at the edges of expected values and lies at the high end |
| `mod_rule`: compatibility with representative models is compatibility with the expectations | MOD | implied (definitional unfolding of the claim; modus ponens, Enderton 2001, *A Mathematical Introduction to Logic*, ch. 1) | – |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| The containing models are the high-amplitude tail; mainstream expectations are lower | `gap_repr` | no: L37's abstract says the amplitude needs parameters at the edges of expected values; L8 §VI says "toward the upper end" |

**Inference (Lean excerpt).**

```lean
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  have h1 : v.CompatModels := p .mod_contain (p .stat_amp) (p .num_contain)  -- Sec. III; L37 Sec. V
  exact p .mod_rule h1 (p .gap_repr)  -- Sec. III; GAP
```

**Critique.** This is the weak link, and it applies to both routes. L37 §V says the populations
reproduce the amplitude "With reasonable choices of astrophysical parameters", while its abstract
says this needs many parameters at the edges of expected values (or a few notably different);
"reasonable" is not the same as "representative of expectations", so `gap_repr` stays a gap. The
abstract's "consistent with astrophysical expectations" and the discussion's "toward the upper
end of predictions" are both true only if "expectations" means "the range spanned by published
models and populations", including their high tails.

#### 2.4 What the Lean check found

1. **`explicit_insufficient`**: even with the standard background added, the chain needs `gap_repr`
   on both routes: compatibility with *some* models does not give compatibility with
   *expectations* unless those models are representative. The countermodel has every stated and
   implied premise true, `Representative` false and the conclusion false.
2. **`stated_insufficient`**: the papers state the measurement, the "within the range of some
   model predictions" fact and the holodeck reproduction; the inference steps (`mod_contain`,
   `mod_holo`, `mod_rule`) are unstated background.
3. **Needed and redundant premises.** `stat_amp`, `gap_repr` and `mod_rule` are needed. The two
   routes are alternatives, so each route's premises are redundant (`num_contain_redundant`,
   `mod_contain_redundant`, `stat_holo_redundant`, `mod_holo_redundant`): either route alone
   gives compatibility with some models. This is a finding about the argument's structure: our
   NUM check of route 1 can fail without breaking the chain, as long as route 2 holds.
4. **The encoded conclusion is narrower than the paper's sentence** (γ = 13/3 amplitude only; see
   the scope note in 2.0).
5. **Consistency** holds but is weak here: every premise is positive.
6. **Limits.** Lean checks the logical structure under our encoding. With uninterpreted atoms,
   "needed" means "used by this encoding". Whether the HD-correlated process really is a GWB, and
   whether the factorised likelihood is faithful, are outside what Lean can see.

```lean
inductive Field where
  | stat_amp      -- STAT [stated 2306.16213]
  | num_contain   -- NUM [stated 2306.16220] NUM[results/r2b.json:n_models_contain_median >= 1]
  | mod_contain   -- MOD [implied]
  | stat_holo     -- STAT [stated 2306.16220]
  | mod_holo      -- MOD [implied]
  | gap_repr      -- GAP [reconstructed]
  | mod_rule      -- MOD [implied]

theorem explicit_insufficient : ¬ ∀ v, Explicit v → Conclusion v := fun h =>
  h ⟨True, 1, True, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])
```

### Part 3 · What astrolab can test or explore

| Stage / claim | Can we test or explore it? | How | Data (size) | Decision criterion | Result |
|---|---|---|---|---|---|
| A: amplitude at γ = 13/3 (R1) | testable now | refit log10 A on the v2.0.0 KDE free spectrum, 14 lowest frequencies, factorised likelihood, L8's prior | Zenodo 21844115 `ceffyl_data.zip`, 3.0 MB | Hellinger distance between our log10 A posterior and a median-pinned two-piece normal built from L8's 5/50/95% values < 0.15: "consistent with L8's interval"; otherwise "differs" | pending |
| L8's spectral-index statement (R2) | testable now (comparison under an approximate likelihood, not a reproduction) | 2-D (log10 A, γ) posterior; q = credible level of the smallest 2-D HPD region touching γ = 13/3 | same | descriptive category (project convention): 95–99.7% "same order as L8's tension", < 95% "weaker", > 99.7% "stronger"; q itself is the result | pending |
| B1: within the range of published models (R2b) | testable now (overlap summary, not a compatibility test) | for each L37 Table A1 model: is our median inside its 16–84% range; do the ranges overlap (boundary rule and duplicate rows fixed in the pre-registration) | L37 Table A1 (paper table) | `n_models_contain_median >= 1` (Lean NUM binding); per-model results descriptive | pending |
| B2: holodeck populations reproduce A | out of scope | needs L37's population libraries and their likelihood | – | – | – |
| C: the models represent expectations (`gap_repr`) | out of scope as a test | would need a definition of what "expectations" covers; L37 itself says the high end | – | – | – |
| Sampler-bug sensitivity (R3) | explorable (not decisive) | redo R1 and R2 on v1.1.0 | Zenodo 10344086, 5.3 MB | none - exploration only, see README §8 | pending |
| Spectral shape (R4) | explorable (not decisive) | Bayes factor of a power law against a power law with a low-frequency turnover | same | none - exploration only (prior-dependent; L11 warns) | pending |
| Off-grid rule, number of frequencies | explorable (not decisive) | values below the grid floor clipped (ceffyl) vs −∞; 14 vs 30 frequencies | same | none - exploration only | pending |
| HD significance | out of scope | needs the full timing data and noise models | GB-scale | – | – |

### Glossary

| Term | Meaning |
|---|---|
| PTA (pulsar timing array) | a set of millisecond pulsars timed for years, used as a galaxy-sized detector |
| GWB (gravitational-wave background) | the summed, random signal of many unresolved sources |
| SMBHB | supermassive black-hole binary |
| Hellings–Downs curve | the expected correlation of two pulsars' residuals versus their angular separation |
| free spectrum | an independent power ρ_k at each frequency, with no assumed shape |
| KDE (kernel density estimate) | a smooth density built from samples; here tabulated on a grid of log10 ρ |
| factorised likelihood | the product of per-frequency KDE densities, approximating the full likelihood |
| Hellinger distance | a 0–1 measure of how different two probability distributions are |
| HPD (highest posterior density) region | the smallest region holding a given posterior probability |

### Open questions

- Does the 2026 sampler fix (v2.0.0) move A or γ noticeably relative to v1.1.0?
- How much does "within the range of some models" depend on including very wide model ranges?

### Changelog

Newest first.

- 2026-11-14: first version: parts 1–3 (pre-registration source; plan `design/014-plan_*`).

### Sources

- Agazie et al. 2023, ApJL 951, L8, arXiv:2306.16213 [V]
- Agazie et al. 2023, ApJL 952, L37, arXiv:2306.16220 [V]; erratum Agazie et al. 2026, ApJL 1006, L67, doi:10.3847/2041-8213/ae8764 [V]
- Lamb, Taylor & van Haasteren 2023, PRD 108, 103019, arXiv:2303.15442 [V]
- Afzal et al. 2023, ApJL 951, L11, arXiv:2306.16219; erratum ApJL 971, L27 (2024) [V]
- NANOGrav KDE free spectra: Zenodo 21844115 (v2.0.0) and 10344086 (v1.1.0) [V, record pages]
- ceffyl source: github.com/astrolamb/ceffyl, `ceffyl/Ceffyl.py` (boundary handling) [V]

---

## 中文

### 第一部分 · 科普详解

#### 1.1 问题与意义

引力波是时空的涟漪。LIGO 与 Virgo 在数百赫兹上听到它们，来源是在零点几秒内并合的恒星级黑洞。星系并合后留下的超大质量黑洞（10⁸–10¹⁰ 个太阳质量）组成的双星要重得多，它们相互绕转数百万年，辐射频率在纳赫兹：几年才一个周期。单个这样的双星目前还不足以被单独分辨，但宇宙中所有这类双星叠加起来，应该形成一种微弱、随机的"嗡嗡声"，即引力波背景（GWB, gravitational-wave background）。

理论对这种嗡嗡声有两个预言。它的响度取决于这类双星有多少、有多重、如何演化，所以测量它可以约束星系演化。如果双星只靠引力辐射损失能量、且轨道为圆，嗡嗡声有确定的形状：特征应变随频率按 f^(−2/3) 下降；等价地，计时残差的功率谱按 f^(−γ) 下降，γ = 13/3。γ 不同，或者振幅远离预言，都可能暗示别的物理：被恒星和气体驱动的双星、偏心轨道，或早期宇宙的来源（宇宙弦、相变；L11）。

2023 年 6 月，NANOGrav 与其他脉冲星计时阵（PTA, pulsar timing array）报告了这种嗡嗡声的证据。L8 是 NANOGrav 的证据论文。本研究只问两个窄问题：能否在笔记本电脑上，用 NANOGrav 公开的压缩数据产品，得回 L8 给出的响度（振幅）与斜率（谱指数）？振幅与 L37 汇总的已发表模型预言相比如何？

#### 1.2 数据

毫秒脉冲星是旋转的中子星，射电脉冲到达的规律性堪比时钟。NANOGrav 用 Arecibo、Green Bank 与 VLA 望远镜对其中 68 颗（引力波背景搜索用了 67 颗）计时，最长 16 年。经过的引力波会拉伸、压缩地球与每颗脉冲星之间的空间，使脉冲略早或略晚到达，即"计时残差"（timing residuals），量级为数百纳秒。数据跨度 T = 16.03 年（L8 第 II 节脚注 2），能分辨的最低频率为 f₁ = 1/T ≈ 1.98 nHz；L8 用最低的 14 个频率 f_k = k/T（k = 1…14，约 2–28 nHz）描述信号。

关键的一点：许多来源叠加的背景，会让不同脉冲星的残差之间的相关性随它们在天空中的角距离呈现特定的形状，即 Hellings–Downs（HD）曲线。探测到这种形状，才能把引力波背景与比如时钟误差区分开。测量 HD 显著性需要完整的计时数据和大型软件，本研究不做。

本项目用的是一个压缩产品（Lamb, Taylor & van Haasteren 2023）。NANOGrav 先拟合"自由谱"（free spectrum）：在每个频率 f_k 上有一个独立的功率 ρ_k（该频率上计时残差功率的平方根，单位为秒），每颗脉冲星自身的噪声都已边缘化。每个 k 的 log10 ρ_k 后验以核密度估计（KDE, kernel density estimate）的形式在固定网格上保存。把这些一维密度相乘，就近似得到任意谱模型的似然（"分解似然"，factorised likelihood），幂律可以在几秒内重拟。产品在 Zenodo 上：v2.0.0（记录 21844115，2026，`ceffyl_data.zip`，3.0 MB；修正了使后验产生偏差的平行回火（parallel tempering）采样器错误）与 v1.1.0（记录 10344086，5.3 MB）。

#### 1.3 一步一步：作者如何从数据走到结论

**(a) 幂律模型。** 频率 f 处的残差功率为 S(f) = A²/(12π²) · f_yr⁻³ · (f/f_yr)^(−γ)，f_yr = 1/年。用自由谱的语言，ρ_k² = S(f_k)/T（Lamb+2023 式 8–9）。A 是参考频率 1/年处的应变振幅。

*粗略估算。* A = 2.4 × 10⁻¹⁵、γ = 13/3、T = 16.03 年时，2 nHz 处 ρ₁ ≈ 0.7 μs，28 nHz 处降到 ρ₁₄ ≈ 2 ns：信号是数百纳秒量级的缓慢漂移，在最长周期上最强，所以需要十年以上的数据。

**(b) γ = 13/3 时的振幅。** 把 γ 固定为圆轨道双星的值、带 HD 相关拟合 A，L8 得到 A = 2.4（+0.7/−0.6）× 10⁻¹⁵（中位数与 90% 可信区间（credible interval））。log10 A 的先验在 [−18, −14] 上均匀（L8 附录 B 表 1）。

**(c) 自由谱指数。** 让 γ 自由变化（先验在 [0, 7] 上均匀；log10 A 在 [−18, −11] 上均匀），L8 得到 A = 6.4（+4.2/−2.7）× 10⁻¹⁵、γ = 3.2 ± 0.6（中位数与 5%–95% 分位数）。A 与 γ 强相关（较平的斜率配上 1/年处较大的振幅，可以描述同样的低频功率）。L8 称 γ 的后验与 13/3 "中等张力"（moderate tension）；图 1 的说明写 γ = 13/3 "包含在 99% 可信区域内"。

**(d) 与天体物理的比较。** L8 在第 III 节说"These amplitudes are compatible with astrophysical expectations of a GWB from inspiraling SMBHBs"，并把细节交给姊妹论文 L37。L37 把振幅与自己的群体模拟（`holodeck` 群体库，只有图）比较，并在附录 A（表 A1、图 A1）中与文献中已发表的预言（24 行）比较，每个预言给出 A_yr 的第 16 与第 84 百分位。例如：Kulier 等 1.58–2.51 × 10⁻¹⁵、McWilliams 等 1.07–15.1 × 10⁻¹⁵ 与 Sesana 等 [171] 0.115–2.88 × 10⁻¹⁵ 包含 2.4 × 10⁻¹⁵；Simon 1.46–2.26 × 10⁻¹⁵ 不包含。按 L37 的说法，振幅在一些模型预测的范围内，但位于高振幅一端。用自己的群体，L37（第 V 节）报告"we are able to reproduce the inferred GWB amplitude and spectral shape"，而它的摘要说，这需要许多参数处在预期值的边缘，或少数参数与标准预期明显不同。L37 的 2026 年勘误修正了星系质量函数的错误与采样器错误，并说结论不变。

#### 1.4 结论与把握程度

- **引力波背景的证据**（HD 相关；贝叶斯因子（Bayes factor）200–1000，按所用统计量约 3–4σ）：强证据，不是 5σ 的探测。本研究不检验。
- **振幅**：γ = 13/3 时 2.4 × 10⁻¹⁵（γ 自由时 6.4 × 10⁻¹⁵），与 SMBHB 的预期一致。摘要说"consistent with astrophysical expectations"，第 III 节说"These amplitudes are compatible"（指两个振幅）；讨论（第 VI 节）补充说它"在预测的上端"，意味着黑洞质量与双星比例相对较高。
- **谱指数**：3.2 ± 0.6，与 13/3 中等张力；作者说环境效应、偏心率或宇宙方差可以容纳它，更奇异的来源不能排除（L11 探讨了这些）。

振幅结论若要成立，以下两点都必须成立：自由谱与幂律拟合正确估计了 A（噪声模型不当或 2026 年数据产品修正的采样器错误都可能使它有偏）；包含 A 的已发表模型代表了天体物理的预期（否则"在某些模型的范围内"会夸大一致程度）。

### 第二部分 · 论证逻辑

#### 2.0 论证地图

A. L8 测得 γ = 13/3 时的 A → B. 经两条途径之一与某些模型相容：B1. A 落在至少一个已发表模型（L37 表 A1）的预测范围内；或 B2. L37 自己的 holodeck 群体再现了 A → C. [缺口] 这些模型代表"天体物理预期" ⇒ γ = 13/3 时的振幅与 SMBHB 引力波背景的天体物理预期相容。

检查方法：论证写成 Lean 4（[`studies/005-m09-nanograv-gwb-power-law/argument/Argument.lean`](https://github.com/sudoghut/astrolab/blob/main/studies/005-m09-nanograv-gwb-power-law/argument/Argument.lean)）。每个前提是 `Field` 的一个构造子（不用公理 axiom），标注类型与出处性质：

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

编码范围：只形式化第 III 节的振幅句，而且只形式化一部分。句中的"These amplitudes"同时指 γ = 13/3 的振幅（2.4 × 10⁻¹⁵）与 γ 自由时的振幅（6.4 × 10⁻¹⁵）；我们只编码前者，因为已发表的预言是在固定谱形下给出的，拿 γ ≈ 3.2 的振幅与之比较不是同类比较（6.4 × 10⁻¹⁵ 只落在表 A1 中 McWilliams 等一行的范围内）；这一理由针对途径 1，途径 2（holodeck 群体）L37 是直接与谱比较的。因此编码的结论比论文的句子弱。谱指数的陈述（γ < 13/3 "可以被"论文没有定量的机制"容纳"）、"更奇异的来源不能排除"与 HD 显著性不形式化：前两者不够精确，不能写成链条；第三者需要本项目不用的数据。

#### 2.1 环节 A · 振幅的测量

**概述。** 一切都基于 γ = 13/3 时 A 的后验。

**前提。**

| 前提（Lean 构造子） | 标签 | 出处性质 | 论文出处 |
|---|---|---|---|
| `stat_amp`：已推断出 γ = 13/3 时的 A，中位数约 2.4 × 10⁻¹⁵ | STAT | stated 2306.16213："the strain amplitude is 2.4−0.6+0.7×10−15 (median + 90% credible interval) at a reference frequency of 1 yr−1" | 摘要；第 III 节 |

**其他解释（rival explanations）。**

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 共同红噪声过程不是引力波背景（例如未建模的脉冲星噪声） | 无（视为给定；HD 证据不在本编码内） | 部分：HD 贝叶斯因子 200–1000，不到 5σ |
| 振幅估计受采样器错误影响 | 无 | 否（L8 早于 2026 年的修正）；由 R3 探索（v1.1.0 对 v2.0.0） |

**评析。** 这是取自论文的 STAT 前提；本研究用压缩产品重算它（R1）。压缩产品是完整似然的近似（Lamb+2023 在 NANOGrav 12.5 年数据上，自由谱重拟的 Hellinger 距离（Hellinger distance）为 0.13，看来是联合后验的值；该案例中 log10 A 一维边缘的距离为 0.06；在 100 次模拟实现中，二维距离的中位数为 0.26，16%–84% 范围为 0.17–0.40）。

#### 2.2 环节 B · 与某些模型相容（两条途径）

**概述。** 振幅与至少一个 SMBHB 群体模型相容：要么一个已发表预言的范围包含它（途径 1），要么 L37 的某个 holodeck 群体再现了它（途径 2）。

**前提。**

| 前提（Lean 构造子） | 标签 | 出处性质 | 论文出处 |
|---|---|---|---|
| `num_contain`：表 A1 中至少一个模型的 16%–84% 范围包含振幅中位数 | NUM | stated 2306.16220："Although the inferred GWB amplitudes are within the range of some of these model predictions"；绑定 `results/r2b.json:n_models_contain_median >= 1` | L37 第 V 节；表 A1、图 A1 |
| `mod_contain`：落在某模型 16%–84% 预测范围内的值与该模型没有张力 | MOD | implied（后验预测推理（posterior predictive reasoning）；Gelman 等 2013，*Bayesian Data Analysis*，第 6 章） | – |
| `stat_holo`：某些 holodeck 群体再现了推断的振幅与谱形 | STAT | stated 2306.16220："we are able to reproduce the inferred GWB amplitude and spectral shape" | L37 第 V 节 |
| `mod_holo`：再现了测量振幅的群体模型与它没有张力 | MOD | implied（Gelman 等 2013，第 6 章）；L37 是把群体与 15 年的谱比较，把它用于 γ = 13/3 的振幅是我们的解读 | – |

`num_contain` 的引文说的是推断的振幅（后验）；我们的绑定用后验中位数，这是我们的操作化。

**其他解释。**

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| A 落在所有模型的范围之外 | `num_contain`（途径 1）、`stat_holo`（途径 2） | 是（L37 第 V 节、附录 A） |

**推理（Lean 摘录）。**

```lean
have h1 : v.CompatModels := p .mod_contain (p .stat_amp) (p .num_contain)  -- Sec. III; L37 Sec. V
```

**评析。** "落在 68% 区间内"是很弱的要求：范围很宽的模型（McWilliams 等，1.07–15.1 × 10⁻¹⁵）几乎包含任何合理的振幅；表 A1 中至少三行（Kulier 等、McWilliams 等、Sesana 等 [171]）包含 2.4 × 10⁻¹⁵，所以 `n_contain ≥ 1` 几乎必然成立，区分力很弱。两条途径各自都足够，所以在编码中每条途径的前提都是多余的（见 2.4）；我们的 NUM 检验只检查途径 1。

#### 2.3 环节 C · 从"某些模型"到"预期"

**概述。** 论文的句子说的是天体物理预期，而不是某几个模型。

**前提。**

| 前提（Lean 构造子） | 标签 | 出处性质 | 论文出处 |
|---|---|---|---|
| `gap_repr`：包含或再现 A 的模型（已发表预言或 holodeck 群体）代表一般意义上的天体物理预期 | GAP | reconstructed | 论文没有写；L37 说这一振幅需要参数处在预期值的边缘，且位于高端 |
| `mod_rule`：与有代表性的模型相容，即与预期相容 | MOD | implied（结论的定义展开；肯定前件式（modus ponens），Enderton 2001，*A Mathematical Introduction to Logic*，第 1 章） | – |

**其他解释。**

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 包含 A 的模型是高振幅的尾部，主流预期更低 | `gap_repr` | 否：L37 的摘要说这一振幅需要参数处在预期值的边缘；L8 第 VI 节说"在预测的上端" |

**推理（Lean 摘录）。**

```lean
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  have h1 : v.CompatModels := p .mod_contain (p .stat_amp) (p .num_contain)  -- Sec. III; L37 Sec. V
  exact p .mod_rule h1 (p .gap_repr)  -- Sec. III; GAP
```

**评析。** 这是最弱的一环，而且对两条途径都适用。L37 第 V 节说群体在"With reasonable choices of astrophysical parameters"时再现了振幅，而它的摘要说这需要许多参数处在预期值的边缘（或少数参数明显不同）；"合理"不等于"代表预期"，所以 `gap_repr` 仍是缺口。摘要的"与天体物理预期一致"和讨论的"在预测的上端"，只有当"预期"指"已发表模型与群体覆盖的范围（含其高尾部）"时才同时成立。

#### 2.4 Lean 检查发现的问题

1. **`explicit_insufficient`**：即使加上标准背景知识，两条途径都仍需要 `gap_repr`：与*某些*模型相容，并不能推出与*预期*相容，除非这些模型有代表性。反例模型中所有明说与隐含的前提都成立，`Representative` 为假，结论为假。
2. **`stated_insufficient`**：论文明说了测量值、"在一些模型预测的范围内"与 holodeck 的再现；推理步骤（`mod_contain`、`mod_holo`、`mod_rule`）是没写出的背景知识。
3. **必要与多余的前提。** `stat_amp`、`gap_repr` 与 `mod_rule` 是必要的。两条途径互为替代，所以每条途径的前提都是多余的（`num_contain_redundant`、`mod_contain_redundant`、`stat_holo_redundant`、`mod_holo_redundant`）：任一途径单独就能给出与某些模型相容。这是关于论证结构的发现：只要途径 2 成立，我们对途径 1 的 NUM 检验即使失败，链条也不会断。
4. **编码的结论比论文的句子窄**（只含 γ = 13/3 的振幅；见 2.0 的范围说明）。
5. **相容性**成立，但在这里分量很弱：所有前提都是肯定命题。
6. **局限。** Lean 检查的是在我们的编码下的逻辑结构。原子命题不加解释时，"必要"指"本编码用到了它"。HD 相关的过程是否真是引力波背景、分解似然是否忠实，都在 Lean 能看到的范围之外。

```lean
inductive Field where
  | stat_amp      -- STAT [stated 2306.16213]
  | num_contain   -- NUM [stated 2306.16220] NUM[results/r2b.json:n_models_contain_median >= 1]
  | mod_contain   -- MOD [implied]
  | stat_holo     -- STAT [stated 2306.16220]
  | mod_holo      -- MOD [implied]
  | gap_repr      -- GAP [reconstructed]
  | mod_rule      -- MOD [implied]

theorem explicit_insufficient : ¬ ∀ v, Explicit v → Conclusion v := fun h =>
  h ⟨True, 1, True, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])
```

### 第三部分 · 本项目可检验或探索的环节

| 环节 / 结论 | 能否检验或探索 | 方法 | 数据（大小） | 判据 | 结果 |
|---|---|---|---|---|---|
| A：γ = 13/3 时的振幅（R1） | 现在可检验 | 在 v2.0.0 KDE 自由谱上、用最低 14 个频率、分解似然与 L8 的先验重拟 log10 A | Zenodo 21844115 `ceffyl_data.zip`，3.0 MB | 我们的 log10 A 后验与由 L8 的 5/50/95% 值构造、以中位数为界的两段半正态（median-pinned two-piece half-normal）之间的 Hellinger 距离 < 0.15："与 L8 的区间一致"；否则"不同" | 待定 |
| L8 的谱指数陈述（R2） | 现在可检验（近似似然下的比较，不是复现） | 二维 (log10 A, γ) 后验；q = 与 γ = 13/3 相交的最小二维最高后验密度（HPD, highest posterior density）区域的可信水平 | 同上 | 描述类别（本项目的约定）：95%–99.7% "与 L8 所称张力同一量级"，< 95% "更弱"，> 99.7% "更强"；结果就是 q 本身 | 待定 |
| B1：落在已发表模型的范围内（R2b） | 现在可检验（重叠摘要，不是相容性检验） | 对 L37 表 A1 的每个模型：我们的中位数是否在其 16%–84% 范围内；两个区间是否重叠（边界规则与重复行在预注册中写定） | L37 表 A1（论文表格） | `n_models_contain_median >= 1`（Lean 的 NUM 绑定）；逐个模型的结果只作描述 | 待定 |
| B2：holodeck 群体再现 A | 不在范围内 | 需要 L37 的群体库及其似然 | – | – | – |
| C：模型代表预期（`gap_repr`） | 不在检验范围内 | 需要先界定"预期"指什么；L37 自己说在高端 | – | – | – |
| 采样器错误的敏感度（R3） | 可探索（不能判决） | 在 v1.1.0 上重做 R1、R2 | Zenodo 10344086，5.3 MB | 无——仅供探索，见 README 第 8 节 | 待定 |
| 谱形（R4） | 可探索（不能判决） | 幂律对带低频转折的幂律的贝叶斯因子 | 同上 | 无——仅供探索（依赖先验；L11 有提醒） | 待定 |
| 越界规则、频率个数 | 可探索（不能判决） | 低于网格下边界取边界值（ceffyl）对 −∞；14 对 30 个频率 | 同上 | 无——仅供探索 | 待定 |
| HD 显著性 | 不在范围内 | 需要完整的计时数据与噪声模型 | GB 级 | – | – |

### 术语表

| 术语 | 含义 |
|---|---|
| PTA（pulsar timing array，脉冲星计时阵） | 一组长期计时的毫秒脉冲星，当作星系尺度的探测器 |
| GWB（gravitational-wave background，引力波背景） | 许多无法分辨的来源叠加成的随机信号 |
| SMBHB（supermassive black-hole binary） | 超大质量黑洞双星 |
| Hellings–Downs 曲线 | 两颗脉冲星残差的预期相关性随角距离的变化 |
| 自由谱（free spectrum） | 每个频率上独立的功率 ρ_k，不假定形状 |
| KDE（kernel density estimate，核密度估计） | 由样本构造的平滑密度，这里在 log10 ρ 的网格上列表 |
| 分解似然（factorised likelihood） | 各频率 KDE 密度之积，近似完整似然 |
| Hellinger 距离（Hellinger distance） | 0 到 1 之间、衡量两个概率分布差异的量 |
| HPD（highest posterior density，最高后验密度）区域 | 含给定后验概率的最小区域 |

### 开放问题

- 2026 年的采样器修正（v2.0.0）相对 v1.1.0，是否明显改变 A 或 γ？
- "在一些模型的范围内"在多大程度上依赖于范围很宽的模型？

### 研究进展

按时间倒序。

- 2026-11-14：第一版：第一至三部分（预注册的来源；计划 `design/014-plan_*`）。

### 来源

- 同英文部分。
