# NANOGrav 15 yr: how loud is the gravitational-wave background, and is that what black-hole binaries predict?

[English](#english) · [中文](#中文)

*Paper(s): Agazie et al. 2023, ApJL 951, L8, arXiv:2306.16213 (main paper, "L8"); Agazie et al. 2023, ApJL 952, L37, arXiv:2306.16220, erratum ApJL 1006, L67 (2026) (the SMBHB companion, "L37"); Lamb, Taylor & van Haasteren 2023, PRD 108, 103019, arXiv:2303.15442 (the refitting method); Afzal et al. 2023, ApJL 951, L11, arXiv:2306.16219 (new-physics context). Study:
[`studies/005-m09-nanograv-gwb-power-law`](https://github.com/sudoghut/astrolab/tree/main/studies/005-m09-nanograv-gwb-power-law).
Status: reproduced. Last updated: 2026-11-15 (see the
changelog at the end). The source of this page lives in the main repository at
[`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki); edit it there.*

*中文标题：NANOGrav 15 年：引力波背景有多强？这是黑洞双星所预言的吗？状态：已复现。论文：Agazie 等 2023, ApJL 951, L8, arXiv:2306.16213（主论文，"L8"）；Agazie 等 2023, ApJL 952, L37, arXiv:2306.16220，勘误 ApJL 1006, L67（2026）（SMBHB 姊妹论文，"L37"）；Lamb, Taylor & van Haasteren 2023, PRD 108, 103019, arXiv:2303.15442（重拟方法）；Afzal 等 2023, ApJL 951, L11, arXiv:2306.16219（新物理背景）。研究：[`studies/005-m09-nanograv-gwb-power-law`](https://github.com/sudoghut/astrolab/tree/main/studies/005-m09-nanograv-gwb-power-law)。最后更新：2026-11-15（见文末"研究进展"）。本页源文件在主仓库的 [`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki) 中，请在那里修改。*

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
bug the 2026 data product fixes); and the published models compatible with A are representative of
what astrophysics expects (otherwise "inside the range of some models" overstates the agreement).

### Part 2 · The logic of the argument

#### 2.0 Map of the argument

A. L8 measures A at γ = 13/3 → B. compatibility with some models, by either of two routes:
B1. the 90% credible interval of A overlaps the predicted range of at least one published model (L37 Table A1), or
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
published prediction whose range overlaps its 90% credible interval (route 1) or one of L37's holodeck populations
that reproduces it (route 2).

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `num_overlap`: at least one Table A1 model's 16–84% range overlaps the 90% credible interval of A | NUM | stated 2306.16220: "Although the inferred GWB amplitudes are within the range of some of these model predictions"; bound to `results/r2b.json:n_models_overlap_ci90 >= 1` | L37 §V; Table A1, Fig. A1 |
| `gap_overlap`: a measurement whose 90% credible interval overlaps a model's 16–84% predicted range is not in tension with that model | GAP | reconstructed (neither paper defines a tension criterion for Table A1; overlap is only a descriptive comparison) | – |
| `stat_holo`: some holodeck populations reproduce the inferred amplitude and spectral shape (only the amplitude part is used) | STAT | stated 2306.16220: "we are able to reproduce the inferred GWB amplitude and spectral shape" | L37 §V |
| `gap_holo`: a population whose predicted spectra reproduce the measured spectrum is not in tension with the γ = 13/3 amplitude | GAP | reconstructed (L37 compares the populations with its own spectra, a posterior predictive check in the sense of Gelman et al. 2013, ch. 6; applying it to L8's γ = 13/3 amplitude is our reading; relabelled from MOD after the referee, 2026-11-15) | – |

The quote of `num_overlap` is about the inferred amplitudes (the posteriors). A posterior within a
range overlaps it, so the overlap count is no stronger than the quote; whether the median itself
lies inside a range (a stronger statement) is reported only descriptively.

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| No listed prediction overlaps the inferred amplitude (the narrower claim; a descriptive result, not a compatibility test) | `num_overlap` (route 1), `stat_holo` (route 2) | yes, in this narrower sense (L37 §V, App. A) |

**Inference (Lean excerpt).**

```lean
have h1 : v.CompatModels := p .gap_overlap (p .stat_amp) (p .num_overlap)  -- Sec. III; L37 Sec. V
```

**Critique.** "Within the range" of a 68% interval is a weak requirement: a model with a very wide
range (McWilliams et al., 1.07–15.1 × 10⁻¹⁵) contains almost any plausible amplitude, and at
least three Table A1 rows (Kulier et al., McWilliams et al., Sesana et al. [171]) contain
2.4 × 10⁻¹⁵, so `n_overlap ≥ 1` is nearly guaranteed and discriminates weakly. Each route alone
suffices, so in the encoding each route's premises are redundant (see 2.4); our NUM test checks
route 1 only. Route 1 also needs a step neither paper supplies: that overlap of the intervals means
no tension (`gap_overlap`); overlap is a description, and two intervals can overlap while the
distributions are in tension.

#### 2.3 Stage C · From some models to "expectations"

**Overview.** The paper's sentence is about astrophysical expectations, not about particular models.

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `gap_repr`: the models (published predictions or holodeck populations) that overlap or reproduce A stand for astrophysical expectations in general | GAP | reconstructed | not in the paper; L37 says the amplitude needs parameters at the edges of expected values and lies at the high end |
| `mod_rule`: compatibility with representative models is compatibility with the expectations | MOD | implied (definitional unfolding of the claim; modus ponens, Enderton 2001, *A Mathematical Introduction to Logic*, ch. 1) | – |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| The containing models are the high-amplitude tail; mainstream expectations are lower | not excluded; this is the gap (`gap_repr`) | no: L37's abstract says the amplitude needs parameters at the edges of expected values; L8 §VI says "toward the upper end" |

**Inference (Lean excerpt).**

```lean
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  have h1 : v.CompatModels := p .gap_overlap (p .stat_amp) (p .num_overlap)  -- Sec. III; L37 Sec. V
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
   model predictions" fact and the holodeck reproduction; `mod_rule` is unstated background, and
   each route has a gap of its own (`gap_overlap` on route 1, `gap_holo` on route 2).
3. **Needed and redundant premises.** `stat_amp`, `gap_repr` and `mod_rule` are needed. The two
   routes are alternatives, so each route's premises are redundant (`num_overlap_redundant`,
   `gap_overlap_redundant`, `stat_holo_redundant`, `gap_holo_redundant`): either route alone
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
  | num_overlap   -- NUM [stated 2306.16220] NUM[results/r2b.json:n_models_overlap_ci90 >= 1]
  | gap_overlap   -- GAP [reconstructed]
  | stat_holo     -- STAT [stated 2306.16220]
  | gap_holo      -- GAP [reconstructed]
  | gap_repr      -- GAP [reconstructed]
  | mod_rule      -- MOD [implied]

theorem explicit_insufficient : ¬ ∀ v, Explicit v → Conclusion v := fun h =>
  h ⟨True, 1, True, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])
```

### Part 3 · What astrolab can test or explore

| Stage / claim | Can we test or explore it? | How | Data (size) | Decision criterion | Result |
|---|---|---|---|---|---|
| A: amplitude at γ = 13/3 (R1) | testable now | refit log10 A on the v2.0.0 KDE free spectrum, 14 lowest frequencies, factorised likelihood, L8's prior | Zenodo 21844115 `ceffyl_data.zip`, 3.0 MB | Hellinger distance between our log10 A posterior and a median-pinned two-piece normal built from L8's 5/50/95% values < 0.15: "consistent with L8's interval"; otherwise "differs" | **consistent with L8's interval**: A = 2.31 [1.82, 2.92] × 10⁻¹⁵, H = 0.099 |
| L8's spectral-index statement (R2) | testable now (comparison under an approximate likelihood, not a reproduction) | 2-D (log10 A, γ) posterior; q = credible level of the smallest 2-D HPD region touching γ = 13/3 | same | descriptive category (project convention): 95–99.7% "same order as L8's tension", < 95% "weaker", > 99.7% "stronger"; q itself is the result | q = 0.979: same order as L8's stated tension (descriptive category); γ = 3.25 [2.65, 3.89] |
| B1: within the range of published models (R2b) | testable now (overlap summary, not a compatibility test) | for each L37 Table A1 model: does its 16–84% range overlap our 90% credible interval; is our median inside it; closed intervals (an endpoint equal to the other range's endpoint counts as overlap); Table A1 rows counted as listed (24 rows; the two identical rows, Rasskazov & Merritt and Dvorkin & Barausse, count separately), with the count after merging identical rows reported alongside | L37 Table A1 (paper table, 24 rows, ~1 KB, transcribed by hand) | `n_models_overlap_ci90 >= 1` (Lean NUM binding); the median count and per-model results descriptive | 8 of 24 rows overlap (binding holds); 5 contain the median |
| B2: holodeck populations reproduce A | out of scope | needs L37's population libraries and their likelihood | – | – | – |
| C: the models represent expectations (`gap_repr`) | out of scope as a test | would need a definition of what "expectations" covers; L37 itself says the high end | – | – | – |
| Sampler-bug sensitivity (R3) | explorable (not decisive) | redo R1 and R2 on v1.1.0 | Zenodo 10344086, 5.3 MB | none - exploration only, see README §8 | pre-registered rule: not evaluable (two matching directories); post hoc with the exact directory: A −8%, γ +0.17 in v2.0.0 |
| Spectral shape (R4) | explorable (not decisive) | Bayes factor of a power law against a power law with a low-frequency turnover | same | none - exploration only (prior-dependent; L11 warns) | ln BF = 2.37 (turnover vs γ = 13/3 power law; prior-dependent) |
| Off-grid rule, number of frequencies | explorable (not decisive) | values below the grid floor clipped (ceffyl) vs −∞; 14 vs 30 frequencies | same | none - exploration only | post hoc: K = 30 H 0.093, q 0.993; K = 5 H 0.243, q 0.92; off-grid rule and grid range no effect |
| HD significance | out of scope | needs the full timing data and noise models | GB-scale | – | – |

#### What we found (2026-11-15)

On NANOGrav's 2026 KDE free spectrum (v2.0.0), the laptop refit lands on L8's numbers under L8's fiducial DMX noise model (see the referee caveats below). At
γ = 13/3 the amplitude is A = 2.31 [1.82, 2.92] × 10⁻¹⁵ (median, 5–95%) against L8's
2.4 [1.8, 3.1] × 10⁻¹⁵; the Hellinger distance to the pre-registered reference is 0.099 (threshold
0.15). With γ free, A = 6.33 × 10⁻¹⁵ and γ = 3.25 [2.65, 3.89] against L8's 6.4 × 10⁻¹⁵ and
3.2 ± 0.6. The smallest 2-D HPD region that touches γ = 13/3 holds q = 0.979 of the posterior, the
same order as L8's "within the 99% region" (under our approximate, factorised likelihood).
Eight of the 24 Table A1 ranges overlap our 90% interval, so the `NUM` premise of route 1 holds;
five contain our median. These numbers do not touch the three gaps (route 2 is not tested): whether a holodeck reproduction applies to this amplitude (`gap_holo`), whether an overlap means "no
tension" (`gap_overlap`) and whether those models represent "astrophysical expectations"
(`gap_repr`).

The pre-registered comparison with the 2023 product (R3) could not be evaluated: its archive holds
two directories matching our rule (the second uses a different noise model). Reading the exact
directory instead (post hoc) shows the 2026 sampler fix lowering A at γ = 13/3 by about 8%
(2.52 → 2.31 × 10⁻¹⁵) and raising γ by about 0.17. A low-frequency turnover is mildly preferred
over the γ = 13/3 power law (ln Bayes factor 2.37), a prior-dependent, descriptive number.

Results: [`r1.json`](https://github.com/sudoghut/astrolab/blob/main/studies/005-m09-nanograv-gwb-power-law/results/r1.json), [`r2.json`](https://github.com/sudoghut/astrolab/blob/main/studies/005-m09-nanograv-gwb-power-law/results/r2.json), [`r2b.json`](https://github.com/sudoghut/astrolab/blob/main/studies/005-m09-nanograv-gwb-power-law/results/r2b.json),
[`r3.json`](https://github.com/sudoghut/astrolab/blob/main/studies/005-m09-nanograv-gwb-power-law/results/r3.json), [`r4.json`](https://github.com/sudoghut/astrolab/blob/main/studies/005-m09-nanograv-gwb-power-law/results/r4.json). The interactive page runs locally with
`python -m astrolab serve`.

**After the independent referee (2026-11-15; post hoc, explorations only).** Three caveats change how
these numbers should be read:

- **The noise model dominates.** On the v1.1.0 free spectrum fitted with a Gaussian-process model
  of dispersion-measure variations (DMGP) instead of L8's fiducial DMX model, R1 gives
  A = 2.19 × 10⁻¹⁵ with H = 0.312 ("differs"), R2 gives q = 0.62 and γ = 3.75 [3.13, 4.43], and
  R4 gives ln BF = 0.99. L8 §V.1 itself notes that DMGP shifts γ towards 13/3. Our agreement with
  L8 is therefore conditional on the DMX noise model, which is the one L8's headline numbers use.
- **The size of the approximation error is better read from v1.1.0.** L8's numbers come from the
  2023 chains, whose like-for-like product is v1.1.0: there H = 0.143, just under the 0.15
  threshold. The smaller v2.0.0 distance (0.099) may partly reflect the 2026 product's own changes.
- **R4 is mostly a preference for γ < 13/3, not for a turnover.** A free-γ power law against the
  γ = 13/3 power law gives ln BF = 1.76; the turnover adds only 0.61 over the free-γ power law.
  L8 Appendix E calls the turnover Bayes factor (1.46, under CURN, common uncorrelated red noise, with γ free) inconclusive.

Number of frequencies: with all 30, H = 0.093 and q = 0.993; with only 5, H = 0.243 and q = 0.92.
L8 uses 14. The KDE grid range and the off-grid rule make no difference (checked by the referee).

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

- 2026-11-16: a blind pre-registered DMX-versus-DMGP comparison (T-024) is not possible: the v2.0.0
  product has no DMGP free spectrum and the only one (v1.1.0) was already explored post hoc; the
  noise-model caveat above stays a post-hoc result.
- 2026-11-15: independent referee: noise-model (DMGP), data-version and R4 caveats added after "What we found"; `mod_holo` relabelled as GAP `gap_holo`; `num_overlap` notes the substitution of our 14-bin interval for L37's own amplitudes.
- 2026-11-15: results: Part 3 result column and "What we found" (R1 consistent, q = 0.979, R2b binding holds, R3 not evaluable as pre-registered with a post-hoc comparison, R4 ln BF 2.37).
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

振幅结论若要成立，以下两点都必须成立：自由谱与幂律拟合正确估计了 A（噪声模型不当或 2026 年数据产品修正的采样器错误都可能使它有偏）；与 A 相容的已发表模型代表了天体物理的预期（否则"在某些模型的范围内"会夸大一致程度）。

### 第二部分 · 论证逻辑

#### 2.0 论证地图

A. L8 测得 γ = 13/3 时的 A → B. 经两条途径之一与某些模型相容：B1. A 的 90% 可信区间与至少一个已发表模型（L37 表 A1）的预测范围重叠；或 B2. L37 自己的 holodeck 群体再现了 A → C. [缺口] 这些模型代表"天体物理预期" ⇒ γ = 13/3 时的振幅与 SMBHB 引力波背景的天体物理预期相容。

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

**概述。** 振幅与至少一个 SMBHB 群体模型相容：要么一个已发表预言的范围与它的 90% 可信区间重叠（途径 1），要么 L37 的某个 holodeck 群体再现了它（途径 2）。

**前提。**

| 前提（Lean 构造子） | 标签 | 出处性质 | 论文出处 |
|---|---|---|---|
| `num_overlap`：表 A1 中至少一个模型的 16%–84% 范围与 A 的 90% 可信区间重叠 | NUM | stated 2306.16220："Although the inferred GWB amplitudes are within the range of some of these model predictions"；绑定 `results/r2b.json:n_models_overlap_ci90 >= 1` | L37 第 V 节；表 A1、图 A1 |
| `gap_overlap`：90% 可信区间与某模型 16%–84% 预测范围重叠的测量与该模型没有张力 | GAP | reconstructed（两篇论文都没有为表 A1 定义张力判据；区间重叠只是描述性比较） | – |
| `stat_holo`：某些 holodeck 群体再现了推断的振幅与谱形（只用到振幅部分） | STAT | stated 2306.16220："we are able to reproduce the inferred GWB amplitude and spectral shape" | L37 第 V 节 |
| `gap_holo`：预测谱再现了测量谱的群体模型与 γ = 13/3 的振幅没有张力 | GAP | reconstructed（L37 把群体与它自己的谱比较，即 Gelman 等 2013 第 6 章意义上的后验预测检验（posterior predictive check）；把它用于 L8 的 γ = 13/3 振幅是我们的解读；审稿后由 MOD 改标，2026-11-15） | – |

`num_overlap` 的引文说的是推断的振幅（后验）。后验落在某范围内必然与它重叠，所以重叠计数不强于引文；中位数本身是否落在范围内（更强的说法）只作描述。

**其他解释。**

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 没有任何列出的预言与推断的振幅重叠（较窄的说法；描述性结果，不是相容性检验） | `num_overlap`（途径 1）、`stat_holo`（途径 2） | 是，在这一较窄的意义上（L37 第 V 节、附录 A） |

**推理（Lean 摘录）。**

```lean
have h1 : v.CompatModels := p .gap_overlap (p .stat_amp) (p .num_overlap)  -- Sec. III; L37 Sec. V
```

**评析。** "落在 68% 区间内"是很弱的要求：范围很宽的模型（McWilliams 等，1.07–15.1 × 10⁻¹⁵）几乎包含任何合理的振幅；表 A1 中至少三行（Kulier 等、McWilliams 等、Sesana 等 [171]）包含 2.4 × 10⁻¹⁵，所以 `n_overlap ≥ 1` 几乎必然成立，区分力很弱。两条途径各自都足够，所以在编码中每条途径的前提都是多余的（见 2.4）；我们的 NUM 检验只检查途径 1。途径 1 还需要一步两篇论文都没有提供的推理：区间重叠即没有张力（`gap_overlap`）；重叠只是描述，两个区间可以重叠而分布之间仍有张力。

#### 2.3 环节 C · 从"某些模型"到"预期"

**概述。** 论文的句子说的是天体物理预期，而不是某几个模型。

**前提。**

| 前提（Lean 构造子） | 标签 | 出处性质 | 论文出处 |
|---|---|---|---|
| `gap_repr`：与 A 重叠或再现 A 的模型（已发表预言或 holodeck 群体）代表一般意义上的天体物理预期 | GAP | reconstructed | 论文没有写；L37 说这一振幅需要参数处在预期值的边缘，且位于高端 |
| `mod_rule`：与有代表性的模型相容，即与预期相容 | MOD | implied（结论的定义展开；肯定前件式（modus ponens），Enderton 2001，*A Mathematical Introduction to Logic*，第 1 章） | – |

**其他解释。**

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 包含 A 的模型是高振幅的尾部，主流预期更低 | 未排除；这正是缺口（`gap_repr`） | 否：L37 的摘要说这一振幅需要参数处在预期值的边缘；L8 第 VI 节说"在预测的上端" |

**推理（Lean 摘录）。**

```lean
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  have h1 : v.CompatModels := p .gap_overlap (p .stat_amp) (p .num_overlap)  -- Sec. III; L37 Sec. V
  exact p .mod_rule h1 (p .gap_repr)  -- Sec. III; GAP
```

**评析。** 这是最弱的一环，而且对两条途径都适用。L37 第 V 节说群体在"With reasonable choices of astrophysical parameters"时再现了振幅，而它的摘要说这需要许多参数处在预期值的边缘（或少数参数明显不同）；"合理"不等于"代表预期"，所以 `gap_repr` 仍是缺口。摘要的"与天体物理预期一致"和讨论的"在预测的上端"，只有当"预期"指"已发表模型与群体覆盖的范围（含其高尾部）"时才同时成立。

#### 2.4 Lean 检查发现的问题

1. **`explicit_insufficient`**：即使加上标准背景知识，两条途径都仍需要 `gap_repr`：与*某些*模型相容，并不能推出与*预期*相容，除非这些模型有代表性。反例模型中所有明说与隐含的前提都成立，`Representative` 为假，结论为假。
2. **`stated_insufficient`**：论文明说了测量值、"在一些模型预测的范围内"与 holodeck 的再现；`mod_rule` 是没写出的背景知识，每条途径各有一个缺口（途径 1 的 `gap_overlap`、途径 2 的 `gap_holo`）。
3. **必要与多余的前提。** `stat_amp`、`gap_repr` 与 `mod_rule` 是必要的。两条途径互为替代，所以每条途径的前提都是多余的（`num_overlap_redundant`、`gap_overlap_redundant`、`stat_holo_redundant`、`gap_holo_redundant`）：任一途径单独就能给出与某些模型相容。这是关于论证结构的发现：只要途径 2 成立，我们对途径 1 的 NUM 检验即使失败，链条也不会断。
4. **编码的结论比论文的句子窄**（只含 γ = 13/3 的振幅；见 2.0 的范围说明）。
5. **相容性**成立，但在这里分量很弱：所有前提都是肯定命题。
6. **局限。** Lean 检查的是在我们的编码下的逻辑结构。原子命题不加解释时，"必要"指"本编码用到了它"。HD 相关的过程是否真是引力波背景、分解似然是否忠实，都在 Lean 能看到的范围之外。

```lean
inductive Field where
  | stat_amp      -- STAT [stated 2306.16213]
  | num_overlap   -- NUM [stated 2306.16220] NUM[results/r2b.json:n_models_overlap_ci90 >= 1]
  | gap_overlap   -- GAP [reconstructed]
  | stat_holo     -- STAT [stated 2306.16220]
  | gap_holo      -- GAP [reconstructed]
  | gap_repr      -- GAP [reconstructed]
  | mod_rule      -- MOD [implied]

theorem explicit_insufficient : ¬ ∀ v, Explicit v → Conclusion v := fun h =>
  h ⟨True, 1, True, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])
```

### 第三部分 · 本项目可检验或探索的环节

| 环节 / 结论 | 能否检验或探索 | 方法 | 数据（大小） | 判据 | 结果 |
|---|---|---|---|---|---|
| A：γ = 13/3 时的振幅（R1） | 现在可检验 | 在 v2.0.0 KDE 自由谱上、用最低 14 个频率、分解似然与 L8 的先验重拟 log10 A | Zenodo 21844115 `ceffyl_data.zip`，3.0 MB | 我们的 log10 A 后验与由 L8 的 5/50/95% 值构造、以中位数为界的两段半正态（median-pinned two-piece half-normal）之间的 Hellinger 距离 < 0.15："与 L8 的区间一致"；否则"不同" | **与 L8 的区间一致**：A = 2.31 [1.82, 2.92] × 10⁻¹⁵，H = 0.099 |
| L8 的谱指数陈述（R2） | 现在可检验（近似似然下的比较，不是复现） | 二维 (log10 A, γ) 后验；q = 与 γ = 13/3 相交的最小二维最高后验密度（HPD, highest posterior density）区域的可信水平 | 同上 | 描述类别（本项目的约定）：95%–99.7% "与 L8 所称张力同一量级"，< 95% "更弱"，> 99.7% "更强"；结果就是 q 本身 | q = 0.979：与 L8 所称张力同一量级（描述类别）；γ = 3.25 [2.65, 3.89] |
| B1：落在已发表模型的范围内（R2b） | 现在可检验（重叠摘要，不是相容性检验） | 对 L37 表 A1 的每个模型：其 16%–84% 范围是否与我们的 90% 可信区间重叠；我们的中位数是否在其中；闭区间（端点相等算重叠）；表 A1 的行按原样计数（24 行；两行数值相同的 Rasskazov & Merritt 与 Dvorkin & Barausse 分别计数），同时报告合并相同行后的计数 | L37 表 A1（论文表格，24 行，约 1 KB，手工抄入） | `n_models_overlap_ci90 >= 1`（Lean 的 NUM 绑定）；中位数计数与逐个模型的结果只作描述 | 24 行中 8 行重叠（绑定成立）；5 行包含中位数 |
| B2：holodeck 群体再现 A | 不在范围内 | 需要 L37 的群体库及其似然 | – | – | – |
| C：模型代表预期（`gap_repr`） | 不在检验范围内 | 需要先界定"预期"指什么；L37 自己说在高端 | – | – | – |
| 采样器错误的敏感度（R3） | 可探索（不能判决） | 在 v1.1.0 上重做 R1、R2 | Zenodo 10344086，5.3 MB | 无——仅供探索，见 README 第 8 节 | 预注册规则：不可评估（两个目录匹配）；事后用精确目录：v2.0.0 中 A 降低 8%、γ 升高 0.17 |
| 谱形（R4） | 可探索（不能判决） | 幂律对带低频转折的幂律的贝叶斯因子 | 同上 | 无——仅供探索（依赖先验；L11 有提醒） | ln BF = 2.37（转折对 γ = 13/3 幂律；依赖先验） |
| 越界规则、频率个数 | 可探索（不能判决） | 低于网格下边界取边界值（ceffyl）对 −∞；14 对 30 个频率 | 同上 | 无——仅供探索 | 事后：K = 30 时 H 0.093、q 0.993；K = 5 时 H 0.243、q 0.92；越界规则与网格范围没有影响 |
| HD 显著性 | 不在范围内 | 需要完整的计时数据与噪声模型 | GB 级 | – | – |

#### 我们的发现（2026-11-15）

在 NANOGrav 2026 年的 KDE 自由谱（v2.0.0）上，在 L8 基准的 DMX 噪声模型下，本机重拟得到了 L8 的数字（见下文审稿后的保留意见）。γ = 13/3 时振幅 A = 2.31 [1.82, 2.92] × 10⁻¹⁵（中位数与 5%–95%），L8 为 2.4 [1.8, 3.1] × 10⁻¹⁵；与预注册参考分布的 Hellinger 距离为 0.099（门槛 0.15）。γ 自由时 A = 6.33 × 10⁻¹⁵、γ = 3.25 [2.65, 3.89]，L8 为 6.4 × 10⁻¹⁵ 与 3.2 ± 0.6。与 γ = 13/3 相交的最小二维 HPD 区域含后验的 q = 0.979，与 L8 的"在 99% 区域内"同一量级（在我们的近似分解似然下）。表 A1 的 24 个范围中有 8 个与我们的 90% 区间重叠，所以途径 1 的 `NUM` 前提成立；5 个包含我们的中位数。这些数字不触及三个缺口（途径 2 未检验）：holodeck 的再现能否用于这一振幅（`gap_holo`）、重叠是否意味着"没有张力"（`gap_overlap`），以及这些模型是否代表"天体物理预期"（`gap_repr`）。

与 2023 年产品的预注册比较（R3）不可评估：其压缩包里有两个目录符合我们的规则（另一个用不同的噪声模型）。事后改读精确目录可见，2026 年的采样器修正使 γ = 13/3 时的 A 降低约 8%（2.52 → 2.31 × 10⁻¹⁵），γ 升高约 0.17。低频转折相对 γ = 13/3 幂律略受偏好（ln 贝叶斯因子 2.37），这是依赖先验的描述性数字。

结果：[`r1.json`](https://github.com/sudoghut/astrolab/blob/main/studies/005-m09-nanograv-gwb-power-law/results/r1.json)、[`r2.json`](https://github.com/sudoghut/astrolab/blob/main/studies/005-m09-nanograv-gwb-power-law/results/r2.json)、[`r2b.json`](https://github.com/sudoghut/astrolab/blob/main/studies/005-m09-nanograv-gwb-power-law/results/r2b.json)、[`r3.json`](https://github.com/sudoghut/astrolab/blob/main/studies/005-m09-nanograv-gwb-power-law/results/r3.json)、[`r4.json`](https://github.com/sudoghut/astrolab/blob/main/studies/005-m09-nanograv-gwb-power-law/results/r4.json)。交互网页在本地用 `python -m astrolab serve` 打开。

**独立审稿之后（2026-11-15；事后，仅为探索）。** 三条保留意见改变了对这些数字的解读：

- **噪声模型占主导。** 在 v1.1.0 中用色散量（dispersion measure）变化的高斯过程模型（DMGP）而不是 L8 基准的 DMX 模型拟合的自由谱上，R1 得 A = 2.19 × 10⁻¹⁵、H = 0.312（"不同"），R2 得 q = 0.62、γ = 3.75 [3.13, 4.43]，R4 得 ln BF = 0.99。L8 第 V.1 节自己也指出 DMGP 会把 γ 推向 13/3。所以我们与 L8 的一致以 DMX 噪声模型为条件，而 L8 的主要数字用的正是它。
- **近似误差的大小更应以 v1.1.0 为准。** L8 的数字来自 2023 年的链，与之同期的产品是 v1.1.0：那里 H = 0.143，刚好低于 0.15。v2.0.0 上较小的距离（0.099）可能部分来自 2026 年产品自身的变化。
- **R4 主要反映 γ < 13/3 的偏好，而不是转折。** 自由 γ 幂律对 γ = 13/3 幂律的 ln BF = 1.76；转折相对自由 γ 幂律只多 0.61。L8 附录 E 称（在 CURN，即无相关的共同红噪声（common uncorrelated red noise）、γ 自由的模型下）转折贝叶斯因子 1.46 不确定。

频率个数：用全部 30 个时 H = 0.093、q = 0.993；只用 5 个时 H = 0.243、q = 0.92。L8 用 14 个。KDE 网格范围与越界规则没有影响（审稿人核对过）。

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

- 2026-11-16：无法做盲的、预注册的 DMX 与 DMGP 比较（T-024）：v2.0.0 数据产品没有 DMGP 自由谱，唯一的一个（v1.1.0）已经做过事后探索；上面关于噪声模型的保留意见仍是事后结果。
- 2026-11-15：独立审稿：在"我们的发现"之后补上噪声模型（DMGP）、数据版本与 R4 的保留意见；`mod_holo` 改标为 GAP `gap_holo`；`num_overlap` 注明以我们的 14 频率区间替代 L37 自己的振幅。
- 2026-11-15：结果：第三部分"结果"一列与"我们的发现"（R1 一致，q = 0.979，R2b 绑定成立，R3 按预注册不可评估、另有事后比较，R4 ln BF 2.37）。
- 2026-11-14：第一版：第一至三部分（预注册的来源；计划 `design/014-plan_*`）。

### 来源

- 同英文部分。
