# DESI DR2: is dark energy evolving?

[English](#english) · [中文](#中文)

*Paper(s): DESI Collaboration, Abdul-Karim et al. 2025, PRD 112, 083515, arXiv:2503.14738 (DESI DR2
BAO cosmology); Popovic et al. 2026, MNRAS, doi:10.1093/mnras/stag632, arXiv:2511.07517 (DES
supernova recalibration, "Dovekie"). Study:
[`studies/002-m01-desi-bao-evolving-dark-energy`](https://github.com/sudoghut/astrolab/tree/main/studies/002-m01-desi-bao-evolving-dark-energy).
Status: planned. Last updated: 2026-11-14 (see the changelog at the end). The source of this page
lives in the main repository at
[`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki); edit it there.*

*中文标题：DESI DR2：暗能量在演化吗？状态：计划中。论文：DESI 合作组 Abdul-Karim 等 2025, PRD 112, 083515, arXiv:2503.14738（DESI DR2 BAO 宇宙学）；Popovic 等 2026, MNRAS, doi:10.1093/mnras/stag632, arXiv:2511.07517（DES 超新星重新校准，"Dovekie"）。研究：[`studies/002-m01-desi-bao-evolving-dark-energy`](https://github.com/sudoghut/astrolab/tree/main/studies/002-m01-desi-bao-evolving-dark-energy)。最后更新：2026-11-14（见文末"研究进展"）。本页源文件在主仓库的 [`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki) 中，请在那里修改。*

---

## English

### Part 1 · The paper in plain language

#### 1.1 The question and why it matters

Since 1998 we have known that the expansion of the Universe is speeding up. The standard model of
cosmology, ΛCDM, explains this with a *cosmological constant* Λ: an energy that every cubic metre
of empty space carries, the same at all times. Its "equation of state" — the ratio of its
pressure to its energy density, written w — is exactly w = −1, forever.

Nothing forces dark energy to be a constant. If it were instead some slowly changing field, w
would drift with time. A common way to describe such a drift is two numbers: w0, the value of w
today, and wa, how fast it changes with the scale factor a of the Universe (w(a) = w0 + wa(1 − a),
the "CPL" parametrisation). ΛCDM is the single point w0 = −1, wa = 0.

The question of the paper is whether the most precise map of cosmic distances yet made still
sits at that point.

#### 1.2 The data

The **Dark Energy Spectroscopic Instrument (DESI)** on the 4-m Mayall telescope in Arizona takes
spectra of thousands of objects at once and measures their redshifts. Data Release 2 (DR2) covers
three years and more than 14 million galaxies and quasars, plus the absorption of quasar light by
intergalactic hydrogen (the Lyman-α forest).

The ruler DESI uses is the **baryon acoustic oscillation (BAO)** scale. Before the Universe was
380,000 years old, sound waves ran through the hot plasma; when the plasma turned into neutral gas
they froze, leaving a slight excess of galaxy pairs separated by a fixed distance, the *sound
horizon at the drag epoch*, r_d ≈ 147 Mpc (about 480 million light years). Measuring that
separation across the sky gives the transverse comoving distance D_M(z); measuring it along the
line of sight gives the Hubble distance D_H(z) = c/H(z). Both come out in units of r_d.

DR2 gives seven redshift bins (Table 4 of the paper), from the bright galaxy sample at
z = 0.295 to the Lyman-α forest at z = 2.33. Examples: at z = 0.510, D_M/r_d = 13.588 ± 0.167 and
D_H/r_d = 21.863 ± 0.425; at z = 2.33, D_M/r_d = 38.988 ± 0.531 and D_H/r_d = 8.632 ± 0.101. The
whole set — means and covariance — is about 3 kB of numbers.

Two further data sets enter. The **cosmic microwave background (CMB)** from Planck (with ACT
lensing) fixes the early Universe: how much matter and baryons there are and the angle the sound
horizon subtends on the sky, θ*. **Type Ia supernovae (SNe)** are standard candles that give
relative distances at z < 2; the paper uses three compilations, Pantheon+, Union3 and DES-SN5YR
(DESY5).

#### 1.3 Step by step

**Step 1 — BAO alone in ΛCDM.** Fitting only the DESI distances with ΛCDM gives a matter density
Ωm = 0.2975 ± 0.0086 and h·r_d = 101.54 ± 0.73 Mpc (Eq. 17). The fit is good: "the results are
well described by a flat ΛCDM model".

**Step 2 — the tension with the CMB.** The CMB, also within ΛCDM, prefers Ωm = 0.3169 ± 0.0065
(Table 5). The two disagree in the (Ωm, h·r_d) plane at 2.3σ ("mild", in the paper's word; 2.0σ if CMB
lensing is excluded). A
back-of-envelope check in Ωm alone: (0.3169 − 0.2975)/√(0.0086² + 0.0065²) = 0.0194/0.0108 ≈
1.8σ; the 2.3σ uses both parameters and their correlation.

**Step 3 — let w vary.** In w0waCDM the tension disappears, because a different expansion history
at low redshift lets BAO and CMB agree. For DESI + CMB the preferred values are w0 = −0.42 ± 0.21
and wa = −1.75 ± 0.58 (Eq. 25): w above −1 today, and lower in the past.

**Step 4 — how much better is the fit?** The paper compares the best (maximum a posteriori, MAP)
fits of the two models: Δχ²_MAP = χ²(w0waCDM) − χ²(ΛCDM). For DESI + CMB it is −12.5 (Table 6).
The extended model has two extra parameters, so some improvement is expected by chance alone.
Wilks' theorem says how much: if ΛCDM were true, −Δχ²_MAP would follow a χ² distribution with two
degrees of freedom. The chance of −12.5 or less is then exp(−12.5/2) = exp(−6.25) ≈ 0.0019, which
corresponds to 3.1σ for a two-sided Gaussian (Eq. 22). That is the headline number.

**Step 5 — other combinations (selected rows of Table 6).**

| Combination | Δχ²_MAP | Significance |
|---|---|---|
| DESI alone | −4.7 | 1.7σ |
| DESI + compressed CMB prior (θ*, ωb, ωbc) | −8.0 | 2.4σ |
| DESI + CMB (no lensing) | −9.7 | 2.7σ |
| DESI + CMB | −12.5 | 3.1σ |
| DESI + Pantheon+ | −4.9 | 1.7σ |
| DESI + Union3 | −10.1 | 2.7σ |
| DESI + DESY5 | −13.6 | 3.3σ |
| DESI + CMB + Pantheon+ | −10.7 | 2.8σ |
| DESI + CMB + Union3 | −17.4 | 3.8σ |
| DESI + CMB + DESY5 | −21.0 | 4.2σ |

Two rows matter for this repo. The *compressed CMB prior* replaces the full CMB likelihood by a
three-number Gaussian on θ*, ωb and ωbc (Appendix A, Eqs. 35–36); with it the preference drops to
2.4σ, because the CMB lensing likelihood "makes a sizable contribution" (§VII.3). And the rows
without CMB can be recomputed from public files of a few megabytes.

**Step 6 — the supernova recalibration (second paper).** In late 2025 (published in MNRAS in 2026) the DES supernova team
recalibrated its photometry ("Dovekie"). The DESY5 combination's preference drops from 4.2σ to
3.2σ (DES-Dovekie + CMB + DESI DR2; there the CMB is Planck + ACT + SPT), with w0 = −0.803 ± 0.054
and wa = −0.72 ± 0.21; the abstract calls the remaining preference "weak". The DESI + CMB result
itself uses no supernovae and is untouched.

#### 1.4 What they conclude, and how sure they are

The abstract's conclusion is conditional: "Unless there is an unknown systematic error associated
with one or more datasets, it is clear that ΛCDM is being challenged by the combination of DESI
BAO with other measurements and that dynamical dark energy offers a possible solution."

Caveats the authors give themselves: the significance is 3–4σ, not the 5σ usually required
(§VII.3); it depends on which supernova sample is used, which points to the calibration of nearby
against distant supernovae; the preferred models cross into "phantom" behaviour (w < −1) at
intermediate redshift, which is hard to obtain from a single scalar field; and the 3.1σ number
uses the full CMB including lensing (2.4σ with the compressed prior).

The authors would be wrong if: an unknown systematic error affects DESI BAO, the CMB or the
supernovae; the Gaussian/Wilks calibration of Δχ² overstates the significance (our `gap_regular`, part 2); or the 3σ is a
fluctuation (a 0.2% chance under the stated assumptions).

### Part 2 · The logic of the argument

#### 2.0 Map of the argument

A. the data: w0waCDM fits DESI + CMB better by Δχ²_MAP = −12.5 →
B. the statistics: nested models + Gaussian, correctly estimated errors + Wilks regularity (our GAP)
→ Wilks → 3.1σ →
C. the interpretation: a ≥ 3σ preference cannot be dismissed (ΛCDM challenged); a better fit that
relieves the BAO–CMB tension makes dynamical dark energy a possible solution
⇒ *unless there is an unknown systematic error*, ΛCDM is challenged and dynamical dark energy is a
possible solution.

How we check it: the argument is written in Lean 4
([`studies/002-m01-desi-bao-evolving-dark-energy/argument/Argument.lean`](https://github.com/sudoghut/astrolab/blob/main/studies/002-m01-desi-bao-evolving-dark-energy/argument/Argument.lean)).
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
`explicit_insufficient` means a real gap). What Lean does not check: the physics inside each
premise — that is what parts 1 and 3 and the study are for.

Encoding choices: Δχ² and significances are whole numbers in tenths (12.5 → 125, 3.1σ → 31). The
conclusion keeps the paper's condition: `Conclusion v := v.NoSys → v.Challenged ∧ v.DDE`, where
`NoSys` means no unknown systematic error in the DESI or CMB data (errors correctly estimated).
The supernova combinations are not in the chain: the headline DESI + CMB number needs none, and
the paper itself presents them as a range (2.8–4.2σ). The second paper (Dovekie) is therefore context
for part 1 and part 3, not a premise of the chain.

#### 2.1 Stage A · The data prefer w0waCDM

**Overview.** The single observational input of the chain is the size of the fit improvement.

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `stat_dchi2`: −Δχ²_MAP ≥ 12.5 for DESI + CMB | STAT | stated 2503.14738: "when including the full CMB information the $\Delta\chi^{2}_{\mathrm{MAP}}$ decreases to $-12.5$" | §VII.1, Table 6 |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| The improvement is only what two free parameters always buy | Stage B (`mod_wilks`, `mod_sig`) | yes, §VII |
| A systematic error in DESI or the CMB makes ΛCDM fit badly | not excluded: the conclusion is conditional on `NoSys` | the paper names it as the open alternative (Abstract, §VII.3) |

**Inference (Lean excerpt).**

```lean
have d : v.dchi2 ≥ 125 := p .stat_dchi2   -- Sec. VII.1, Table 6
```

**Critique.** The number is the paper's; this repo cannot recompute it, because it needs the full
Planck and ACT likelihoods. We can recompute the neighbouring numbers that use the compressed CMB
prior (−8.0) and no CMB (−4.7, −4.9, −10.1); see part 3. Δχ² is taken at the MAP, which with flat
priors is the maximum likelihood inside the prior box; the prior w0 + wa < 0 and wa > −3 matter for
the compressed-prior combination, whose posterior the paper says "is still bounded by the wa > −3
prior at the lower end".

#### 2.2 Stage B · From Δχ² to 3.1σ

**Overview.** Turning a fit improvement into a probability needs a statistical model of how large
Δχ² would be by chance if ΛCDM were true.

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `mod_nested`: ΛCDM is w0waCDM with w0 = −1, wa = 0 | MOD | stated 2503.14738: "$\Lambda$ CDM is nested within $w_{0}w_{a}$ CDM, corresponding to $w_{0}=-1$ , $w_{a}=0$" | §VII |
| `mod_gauss`: the errors are Gaussian (working assumption) | MOD | stated 2503.14738: "assuming that errors are Gaussian and correctly estimated" | §VII |
| `gap_regular`: Wilks' regularity conditions hold, so Δχ²_MAP is calibrated by χ²(2) (large-sample limit, ΛCDM point inside the prior box) | GAP | reconstructed: Wilks 1938 (1938AnMS....9...60W) gives the theorem, not its validity for this nonlinear fit; the paper neither discusses nor simulates it | — |
| `mod_wilks`: nested + Gaussian + regular + no systematics → Δχ²_MAP ~ χ²(2 dof) | MOD | stated 2503.14738: "implies that $\Delta\chi^{2}_{\mathrm{MAP}}$ should follow a $\chi^{2}$ distribution with two degrees of freedom under the assumption the null hypothesis ( $\Lambda$ CDM model) holds, and assuming that errors are Gaussian and correctly estimated" | §VII |
| `mod_sig`: Wilks + Δχ² ≤ −12.5 → 3.1σ | MOD | stated 2503.14738: "corresponding to a 3.1 $\sigma$ preference for evolving dark energy" | §VII.1 (via Eq. 22, §VII) |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| Non-Gaussian likelihood tails (the low-ℓ CMB likelihoods are not Gaussian) make large Δχ² more common than χ²(2) says | `mod_gauss` (stated assumption), `gap_regular` | no: the paper writes "assuming that errors are Gaussian" and does not discuss the calibration |
| Prior boundaries or parameter-space volume distort the Δχ² distribution | `gap_regular` | no (not discussed) |
| Underestimated errors | `NoSys` (condition of the conclusion) | yes, as the stated caveat |

**Inference (Lean excerpt).**

```lean
have w : v.WilksOK := p .mod_wilks (p .mod_nested) (p .mod_gauss) (p .gap_regular) hns
have s : v.sig ≥ 31 := p .mod_sig w d                                  -- Eq. 22
```

**Critique.** The paper states its assumption ("assuming that errors are Gaussian and correctly
estimated") and does not test it. The "correctly estimated" half is the condition `NoSys` of the
conclusion; the "Gaussian" half is the stated working assumption `mod_gauss`, which is not literally
true for the full CMB (the low-ℓ likelihoods are not Gaussian). Wilks' theorem itself does not need
Gaussian errors; it needs regularity: a large-sample limit and the null point away from prior
boundaries. The paper does not discuss this, and the textbook theorem does not show that it holds for this
nonlinear fit, so it is our `GAP` premise `gap_regular`. w0 = −1, wa = 0 is inside the prior box, so it is plausible, but no simulation of the
Δχ² distribution is reported. That is
something this repo can explore with the compressed prior (part 3).

#### 2.3 Stage C · From 3.1σ to "challenged" and "possible solution"

**Overview.** The last stage is interpretation.

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `mod_challenge`: ≥ 3σ → ΛCDM challenged | MOD | stated 2503.14738: "This level of significance is not trivially dismissed, even if it does not yet rise to the $5\sigma$ threshold" | §VII.3 |
| `mod_dde`: better fit → dynamical dark energy a possible solution | MOD | stated 2503.14738: "This tension is alleviated by dark energy with a time-evolving equation of state parametrized by $w_{0}$ and $w_{a}$ , which provides a better fit to the data" | Abstract |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| A statistical fluctuation (0.2% under the assumptions) | not excluded; `mod_challenge` only says it is "not trivially dismissed" | no: discussed but not excluded (§VII.3) |
| Another extension (curvature, neutrino mass) fits as well | not encoded | partly: no preference for curvature in ΛCDM + Ω_K (§VI) |
| The w0–wa parametrisation itself creates the preference | not encoded | partly: the paper finds the phantom crossing "rather independent of parametrization choices" |

**Inference (Lean excerpt).**

```lean
have c : v.Challenged := p .mod_challenge (by omega)   -- Sec. VII.3
have e : v.DDE := p .mod_dde d                         -- Abstract
exact ⟨c, e⟩
```

**Critique.** "Challenged" and "possible solution" are deliberately weak words, and the encoding
keeps them weak; the paper does not claim a detection. The `mod_challenge` sentence is said of the
whole range "around 3σ to over 4σ"; our threshold 3.0σ is the low end. In this encoding the `DDE` conjunct needs neither Wilks nor `NoSys`: any better fit triggers the
paper's sentence, and the threshold 12.5 is only the observed value. "Possible solution" is
backed by a better fit and by the removal of the BAO–CMB tension, but also comes with the phantom
crossing that the paper itself calls theoretically difficult for single scalar fields.

#### 2.4 What the Lean check found

```lean
theorem stated_insufficient : ¬ ∀ v, Stated v → Conclusion v := fun h =>
  (h ⟨True, True, False, True, False, 125, 0, False, True⟩
    (by intro f hf; cases f <;> simp_all [prov, prem]) trivial).1

theorem explicit_insufficient : ¬ ∀ v, Explicit v → Conclusion v := fun h =>
  (h ⟨True, True, False, True, False, 125, 0, False, True⟩
    (by intro f hf; cases f <;> simp_all [prov, prem]) trivial).1
```

1. **`explicit_insufficient`**: even with standard knowledge the chain has one real gap,
   `gap_regular`: that Δχ²_MAP is calibrated by a χ² distribution with two degrees of freedom for
   this nonlinear fit. Wilks' theorem gives this only under regularity conditions, and the paper
   neither discusses nor simulates them. The countermodel sets `Regular := False`: Wilks does not
   apply, there is no significance, and the conclusion fails. This gap is explorable here (part 3,
   "Stage B · Wilks calibration"). The paper's main caveat, unknown systematics, is not a gap of
   the encoding because the paper writes it into the conclusion ("unless there is an unknown
   systematic error"); without that condition the chain would need a second GAP "no unknown
   systematics", which no paper can supply.
2. **`stated_insufficient`**: for the same reason, what the paper writes is not enough. With no
   `[implied]` premise left, the stated and the explicit premise sets coincide; the only missing premise
   is the GAP. Gaussian
   errors, by contrast, are a stated assumption (`mod_gauss`).
3. **Every premise is needed** (eight `_needed` theorems; `mod_gauss` is needed only because we encode the
   paper's own sufficient condition for Wilks, which does not itself require Gaussian errors). There is a single route from data to
   conclusion: the Δχ², Wilks, and the two interpretive steps. This follows partly from our
   encoding choice (§2.0): the abstract's conclusion is about "DESI BAO with other measurements",
   backed by a range of 2.8–4.2σ that includes combinations below 3σ; we encode only DESI + CMB. In particular, the conclusion
   rests on one number (−12.5) computed with the full CMB likelihood including lensing; with the
   compressed CMB prior the same chain gives 2.4σ, below the 3σ of `mod_challenge`.
4. **Ranked weak points** (ours, not Lean's): (i) the condition "no unknown systematics" is where
   the debate is — the supernova range 2.8–4.2σ and the Dovekie drop to 3.2σ show how much
   calibration moves the answer; (ii) the Wilks calibration (`gap_regular`) is assumed, not simulated; (iii) the
   significance relies on CMB lensing; (iv) "possible solution" includes phantom behaviour.
5. **Consistency** (`consistent`) holds trivially here: no premise is negative.
6. **Limits**: Lean checks the structure under our encoding, not the physics in each premise.

### Part 3 · What astrolab can test or explore

| Stage / claim | Can we test or explore it? | How | Data (size) | Decision criterion | Result |
|---|---|---|---|---|---|
| R1 · Stage A input: BAO alone in ΛCDM | testable now | fit Ωm and h·r_d to the DR2 means and covariance | DESI DR2 BAO ALL, ~3 kB | reproduced if Ωm and h·r_d agree with 0.2975 ± 0.0086 and 101.54 ± 0.73 Mpc within the tolerance pre-registered in README §2 | pending |
| R2 · Stage A–B with the compressed CMB prior | testable now | MAP fits of ΛCDM and w0waCDM to DESI + (θ*, ωb, ωbc); Δχ² → σ; both readings of the prior (ωbc with and without ων) | BAO ~3 kB; prior in the code | reproduced if Δχ²_MAP is within the pre-registered tolerance of −8.0 under both readings; conditionally reproduced if under one | pending |
| R3 · Stage A–B without CMB | testable now | MAP fits for DESI, DESI + Pantheon+, DESI + Union3 | Pantheon+ 34 MB, Union3 11 kB | reproduced if Δχ²_MAP is within the pre-registered tolerance of −4.7, −4.9, −10.1 | pending |
| Stage A with the full CMB (−12.5) | out of scope | needs the full Planck and ACT likelihoods (not a compressed data product) | — | — | — |
| Stage B · Wilks calibration (`gap_regular`) | explorable (not decisive) | simulate DESI + compressed-prior data under the ΛCDM best fit, refit both models, compare the Δχ² distribution with χ²(2); this informs the gap but cannot close it, which concerns the full-CMB fit | no new data | none — exploration only, see README §8 | — |
| `NoSys` · supernova calibration | explorable (not decisive) | DESI + compressed CMB + Pantheon+ / Union3 / DES-Dovekie; compare the spread | Dovekie 6.2 MB | none — exploration only | — |
| `NoSys` · single tracers | explorable (not decisive) | leave one DESI redshift bin out | per-tracer files, ~1 kB | none — exploration only | — |
| Stage C · parametrisation | explorable (not decisive) | replace CPL by binned w(z) or other forms | no new data | none — exploration only | — |
| DES-SN5YR combinations | out of scope for now | its covariance is 53.5 MB, above the 50 MB single-download limit; Dovekie replaces it | — | — | — |

### Glossary

| Term | Meaning |
|---|---|
| BAO | baryon acoustic oscillations: a preferred separation between galaxies, set by sound waves in the early Universe |
| r_d | the sound horizon at the drag epoch, the BAO ruler length (≈ 147 Mpc) |
| D_M, D_H | transverse comoving distance and Hubble distance c/H(z) |
| ΛCDM | the standard model: cosmological constant plus cold dark matter |
| w0, wa | equation of state of dark energy today and its rate of change (CPL parametrisation) |
| Δχ²_MAP | difference of the best-fit χ² of two models (MAP: maximum a posteriori) |
| Wilks' theorem | for nested models, twice the log-likelihood ratio follows a χ² distribution with as many degrees of freedom as extra parameters, when the simpler model is true |
| compressed CMB prior | a Gaussian on a few early-Universe numbers (θ*, ωb, ωbc) that stands in for the full CMB likelihood |
| phantom | w < −1: dark energy whose density grows as the Universe expands |

### Changelog

- 2026-11-14: first version: parts 1–3, written before implementation (T-004, plan 010); revised after
  gate-1 review (Gaussian errors are a stated assumption; Wilks regularity added as the GAP `gap_regular`, so `explicit_insufficient`).

---

## 中文

### 第一部分 · 科普详解

#### 1.1 问题与意义

1998 年起我们知道宇宙在加速膨胀。标准宇宙学模型 ΛCDM 用宇宙学常数（cosmological constant）Λ 解释这一点：每立方米真空都带有同样的能量，任何时候都不变。它的物态方程（equation of state）——压强与能量密度之比，记作 w——恒等于 −1。

没有什么规定暗能量必须是常数。如果它是某种缓慢变化的场，w 就会随时间漂移。描述这种漂移的常见方式是两个数：w0 是今天的 w，wa 是它随宇宙尺度因子（scale factor）a 变化的快慢（w(a) = w0 + wa(1 − a)，称为 CPL 参数化）。ΛCDM 就是 w0 = −1、wa = 0 这一个点。

论文的问题是：迄今最精确的宇宙距离图，是否仍然落在这个点上。

#### 1.2 数据

**暗能量光谱仪（DESI, Dark Energy Spectroscopic Instrument）** 装在亚利桑那州 4 米 Mayall 望远镜上，一次可拍几千个天体的光谱并测出红移。第二次数据发布（DR2）包含三年的观测、超过 1400 万个星系和类星体，以及类星体光被星系际氢吸收形成的莱曼 α 森林（Lyman-α forest）。

DESI 用的尺子是 **重子声学振荡（BAO, baryon acoustic oscillations）** 的尺度。宇宙诞生后 38 万年之前，声波在炽热的等离子体中传播；等离子体变成中性气体时声波冻结，留下一个固定间距上星系对略多的痕迹，这个间距就是拖曳时期的声视界（sound horizon at the drag epoch）r_d ≈ 147 Mpc（约 4.8 亿光年）。在天空方向测这个间距，得到横向共动距离（transverse comoving distance）D_M(z)；沿视线方向测，得到哈勃距离（Hubble distance）D_H(z) = c/H(z)。两者都以 r_d 为单位。

DR2 给出 7 个红移区间（论文表 4），从 z = 0.295 的亮星系样本到 z = 2.33 的莱曼 α 森林。例如 z = 0.510 处 D_M/r_d = 13.588 ± 0.167、D_H/r_d = 21.863 ± 0.425；z = 2.33 处 D_M/r_d = 38.988 ± 0.531、D_H/r_d = 8.632 ± 0.101。全部均值与协方差（covariance）约 3 kB。

另外两组数据也参与。**宇宙微波背景（CMB, cosmic microwave background）**（Planck 加 ACT 透镜）确定早期宇宙：物质与重子的多少，以及声视界在天空上张开的角度 θ*。**Ia 型超新星（SNe）** 是标准烛光，给出 z < 2 的相对距离；论文用三个汇编：Pantheon+、Union3 和 DES-SN5YR（DESY5）。

#### 1.3 逐步讲解

**第 1 步——只用 BAO，在 ΛCDM 中。** 只拟合 DESI 的距离，得到物质密度 Ωm = 0.2975 ± 0.0086、h·r_d = 101.54 ± 0.73 Mpc（式 17）。拟合很好："结果可以很好地由平直 ΛCDM 模型描述"。

**第 2 步——与 CMB 的张力（tension）。** CMB 在 ΛCDM 中偏好 Ωm = 0.3169 ± 0.0065（表 5）。两者在 (Ωm, h·r_d) 平面上相差 2.3σ（论文称为"温和的"；不含 CMB 透镜时为 2.0σ）。只看 Ωm 的粗估：(0.3169 − 0.2975)/√(0.0086² + 0.0065²) = 0.0194/0.0108 ≈ 1.8σ；2.3σ 用了两个参数及其相关性。

**第 3 步——让 w 变化。** 在 w0waCDM 中张力消失：低红移处不同的膨胀历史让 BAO 与 CMB 一致。DESI + CMB 偏好 w0 = −0.42 ± 0.21、wa = −1.75 ± 0.58（式 25）：今天 w 高于 −1，过去更低。

**第 4 步——拟合好了多少？** 论文比较两个模型的最佳拟合（最大后验，MAP, maximum a posteriori）：Δχ²_MAP = χ²(w0waCDM) − χ²(ΛCDM)。DESI + CMB 为 −12.5（表 6）。扩展模型多两个参数，单靠运气也会改善一些。威尔克斯定理（Wilks' theorem）给出改善多少才算意外：若 ΛCDM 为真，−Δχ²_MAP 服从 2 个自由度的 χ² 分布。得到 −12.5 或更小的概率为 exp(−12.5/2) = exp(−6.25) ≈ 0.0019，对应双侧高斯的 3.1σ（式 22）。这就是标题数字。

**第 5 步——其他组合（表 6 的部分行）。**

| 组合 | Δχ²_MAP | 显著性（significance） |
|---|---|---|
| 只用 DESI | −4.7 | 1.7σ |
| DESI + 压缩 CMB 先验 (θ*, ωb, ωbc) | −8.0 | 2.4σ |
| DESI + CMB（不含透镜） | −9.7 | 2.7σ |
| DESI + CMB | −12.5 | 3.1σ |
| DESI + Pantheon+ | −4.9 | 1.7σ |
| DESI + Union3 | −10.1 | 2.7σ |
| DESI + DESY5 | −13.6 | 3.3σ |
| DESI + CMB + Pantheon+ | −10.7 | 2.8σ |
| DESI + CMB + Union3 | −17.4 | 3.8σ |
| DESI + CMB + DESY5 | −21.0 | 4.2σ |

有两行对本项目重要。**压缩 CMB 先验（compressed CMB prior）** 用 θ*、ωb、ωbc 三个数的高斯分布代替完整的 CMB 似然（附录 A，式 35–36）；用它时偏好降到 2.4σ，因为 CMB 透镜似然"贡献相当大"（§VII.3）。不含 CMB 的几行可以用几 MB 的公开文件重算。

**第 6 步——超新星重新校准（第二篇论文）。** 2025 年底（2026 年发表于 MNRAS）DES 超新星团队重新校准了测光（"Dovekie"）。DESY5 组合的偏好由 4.2σ 降到 3.2σ（DES-Dovekie + CMB + DESI DR2，其中 CMB 是 Planck + ACT + SPT），w0 = −0.803 ± 0.054、wa = −0.72 ± 0.21；摘要称剩下的偏好"较弱"。DESI + CMB 的结果本身不用超新星，不受影响。

#### 1.4 结论与把握程度

摘要的结论是有条件的："除非一个或多个数据集存在未知的系统误差，否则显然 ΛCDM 正受到 DESI BAO 与其他测量组合的挑战，而动力学暗能量（dynamical dark energy）提供了一种可能的解释。"

作者自己给出的保留：显著性是 3–4σ，不是通常要求的 5σ（§VII.3）；它取决于用哪个超新星样本，说明近处与远处超新星的相对校准很关键；偏好的模型在中等红移进入"幽灵"（phantom）区域（w < −1），单个标量场很难做到；3.1σ 用了包括透镜在内的完整 CMB（用压缩先验时为 2.4σ）。

作者可能错在：DESI BAO、CMB 或超新星存在未知系统误差；Δχ² 的高斯/威尔克斯校准高估了显著性（即第二部分的 `gap_regular`）；或者 3σ 只是涨落（在上述假设下概率 0.2%）。

### 第二部分 · 论证逻辑

#### 2.0 论证结构

A. 数据：w0waCDM 对 DESI + CMB 的拟合好 Δχ²_MAP = −12.5 →
B. 统计：模型嵌套（nested）+ 误差高斯且估计正确 + 威尔克斯正则性（我们补上的 GAP）→ 威尔克斯定理 → 3.1σ →
C. 解释：≥ 3σ 的偏好不能轻易忽略（ΛCDM 受到挑战）；拟合更好且消除 BAO–CMB 张力，使动力学暗能量成为可能的解释
⇒ *除非存在未知系统误差*，ΛCDM 受到挑战，动力学暗能量是一种可能的解释。

检查方法：论证写成 Lean 4（[`studies/002-m01-desi-bao-evolving-dark-energy/argument/Argument.lean`](https://github.com/sudoghut/astrolab/blob/main/studies/002-m01-desi-bao-evolving-dark-energy/argument/Argument.lean)）。每个前提是 `Field` 的一个构造子（不用公理），标注类型与出处性质：

| 标记 | 前提类型 |
|---|---|
| `OBS` | 观测或测量（附表或图） |
| `MOD` | 建模假设 |
| `STAT` | 统计推断（显著性、模型比较） |
| `NUM` | 本项目 `run.py` 重新计算的数值结果 |
| `LIT` | 取自其他文献的结果 |
| `GAP` | 推理需要、但论文和标准知识都没有提供的前提 |

出处性质：`[stated <arXiv 编号>: "引文"]`（论文明说，附引文）、`[implied]`（论文依赖但没写出的标准知识，注明来源）、`[reconstructed]`（我们补上的；恰好是 `GAP` 前提）。

Lean 检查：结论能否由这些前提推出（`final`），且不是恒真（`final_nontrivial`）；前提能否同时成立（`consistent`）；没有任何单个前提单独推出结论（`alone_insufficient`）；每个前提是必要的（去掉它有反例模型（countermodel））还是多余的；论文实际写出的前提是否足够（`stated_*`），加上标准知识后是否足够（`explicit_*`；`explicit_insufficient` 表示真正的缺口）。Lean 不检查：每个前提内部的物理——那是第一、三部分和研究本身的任务。

编码选择：Δχ² 与显著性用十分之一为单位的整数（12.5 → 125，3.1σ → 31）。结论保留论文的条件：`Conclusion v := v.NoSys → v.Challenged ∧ v.DDE`，`NoSys` 表示 DESI 或 CMB 数据中没有未知系统误差（误差估计正确）。超新星组合不在链条中：DESI + CMB 的标题数字不需要超新星，论文本身也只给出范围（2.8–4.2σ）。因此第二篇论文（Dovekie）是第一、三部分的背景，不是链条的前提。

#### 2.1 环节 A · 数据偏好 w0waCDM

**概述。** 链条唯一的观测输入是拟合改善的大小。

**前提。**

| 前提（Lean 构造子） | 类型 | 出处性质 | 论文位置 |
|---|---|---|---|
| `stat_dchi2`：DESI + CMB 的 −Δχ²_MAP ≥ 12.5 | STAT | stated 2503.14738："when including the full CMB information the $\Delta\chi^{2}_{\mathrm{MAP}}$ decreases to $-12.5$" | §VII.1，表 6 |

**其他解释。**

| 其他解释 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 改善只是两个自由参数总能带来的 | 环节 B（`mod_wilks`、`mod_sig`） | 是，§VII |
| DESI 或 CMB 的系统误差让 ΛCDM 拟合变差 | 不排除：结论以 `NoSys` 为条件 | 论文把它列为尚未排除的可能（摘要、§VII.3） |

**推理（Lean 摘录）。**

```lean
have d : v.dchi2 ≥ 125 := p .stat_dchi2   -- Sec. VII.1, Table 6
```

**评析。** 这个数字来自论文；本项目无法重算，因为需要完整的 Planck 与 ACT 似然。我们能重算相邻的几个数：用压缩 CMB 先验的 −8.0，以及不含 CMB 的 −4.7、−4.9、−10.1（见第三部分）。Δχ² 取在 MAP，平直先验下就是先验范围内的最大似然；对压缩先验的组合，w0 + wa < 0 与 wa > −3 的先验有影响：论文说这一组合的后验"在下端仍受 wa > −3 的先验限制"。

#### 2.2 环节 B · 从 Δχ² 到 3.1σ

**概述。** 把拟合改善变成概率，需要一个统计模型：若 ΛCDM 为真，Δχ² 靠运气会有多大。

**前提。**

| 前提（Lean 构造子） | 类型 | 出处性质 | 论文位置 |
|---|---|---|---|
| `mod_nested`：ΛCDM 是 w0 = −1、wa = 0 的 w0waCDM | MOD | stated 2503.14738："$\Lambda$ CDM is nested within $w_{0}w_{a}$ CDM, corresponding to $w_{0}=-1$ , $w_{a}=0$" | §VII |
| `mod_gauss`：误差是高斯的（工作假设） | MOD | stated 2503.14738："assuming that errors are Gaussian and correctly estimated" | §VII |
| `gap_regular`：威尔克斯定理的正则性（regularity）条件成立，所以 Δχ²_MAP 按 χ²(2) 校准（大样本极限，ΛCDM 点在先验范围内部） | GAP | reconstructed：Wilks 1938（1938AnMS....9...60W）给出定理，但不说明它对这一非线性拟合成立；论文既没有讨论也没有模拟 | — |
| `mod_wilks`：嵌套 + 高斯 + 正则 + 无系统误差 → Δχ²_MAP 服从 χ²（2 个自由度） | MOD | stated 2503.14738："implies that $\Delta\chi^{2}_{\mathrm{MAP}}$ should follow a $\chi^{2}$ distribution with two degrees of freedom under the assumption the null hypothesis ( $\Lambda$ CDM model) holds, and assuming that errors are Gaussian and correctly estimated" | §VII |
| `mod_sig`：威尔克斯 + Δχ² ≤ −12.5 → 3.1σ | MOD | stated 2503.14738："corresponding to a 3.1 $\sigma$ preference for evolving dark energy" | §VII.1（经 §VII 的式 22） |

**其他解释。**

| 其他解释 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 似然（likelihood）的非高斯尾部（低 ℓ 的 CMB 似然不是高斯的）让大的 Δχ² 比 χ²(2) 更常见 | `mod_gauss`（明说的假设）、`gap_regular` | 否：论文写的是"假设误差是高斯的"，没有讨论校准 |
| 先验边界或参数空间体积扭曲 Δχ² 的分布 | `gap_regular` | 否（没有讨论） |
| 误差被低估 | `NoSys`（结论的条件） | 是，作为明说的保留 |

**推理（Lean 摘录）。**

```lean
have w : v.WilksOK := p .mod_wilks (p .mod_nested) (p .mod_gauss) (p .gap_regular) hns
have s : v.sig ≥ 31 := p .mod_sig w d                                  -- Eq. 22
```

**评析。** 论文写明了它的假设（"假设误差是高斯的且估计正确"），没有检验。"估计正确"这一半是结论的条件 `NoSys`；"高斯"这一半是明说的工作假设 `mod_gauss`，对完整 CMB 并不严格成立（低 ℓ 的似然不是高斯的）。威尔克斯定理本身并不需要高斯误差，需要的是正则性：大样本极限（渐近，asymptotic），且零假设点远离先验边界。论文没有讨论这一点，教科书定理也不说明它对这一非线性拟合成立，所以它是我们补上的 `GAP` 前提 `gap_regular`。w0 = −1、wa = 0 在先验范围内部，所以大致合理，但论文没有报告 Δχ² 分布的模拟。本项目可以用压缩先验探索这一点（第三部分）。

#### 2.3 环节 C · 从 3.1σ 到"受到挑战"与"可能的解释"

**概述。** 最后一个环节是解释。

**前提。**

| 前提（Lean 构造子） | 类型 | 出处性质 | 论文位置 |
|---|---|---|---|
| `mod_challenge`：≥ 3σ → ΛCDM 受到挑战 | MOD | stated 2503.14738："This level of significance is not trivially dismissed, even if it does not yet rise to the $5\sigma$ threshold" | §VII.3 |
| `mod_dde`：拟合更好 → 动力学暗能量是可能的解释 | MOD | stated 2503.14738："This tension is alleviated by dark energy with a time-evolving equation of state parametrized by $w_{0}$ and $w_{a}$ , which provides a better fit to the data" | 摘要 |

**其他解释。**

| 其他解释 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 统计涨落（在上述假设下概率 0.2%） | 不排除；`mod_challenge` 只说"不能轻易忽略" | 否：讨论了但没有排除（§VII.3） |
| 另一种扩展（曲率、中微子质量）拟合得同样好 | 未编码 | 部分：ΛCDM + Ω_K 中曲率没有显著偏好（§VI） |
| w0–wa 参数化本身造成偏好 | 未编码 | 部分：论文认为幽灵穿越"相当独立于参数化的选择" |

**推理（Lean 摘录）。**

```lean
have c : v.Challenged := p .mod_challenge (by omega)   -- Sec. VII.3
have e : v.DDE := p .mod_dde d                         -- Abstract
exact ⟨c, e⟩
```

**评析。** "受到挑战"与"可能的解释"是刻意的弱措辞，编码也保持了这种弱度；论文没有宣称探测到。`mod_challenge` 那句话针对的是"约 3σ 到 4σ 以上"整个范围；我们的阈值 3.0σ 是下端。在本编码中 `DDE` 这一半既不需要威尔克斯定理也不需要 `NoSys`：任何更好的拟合都触发论文的那句话，阈值 12.5 只是观测值。"可能的解释"有更好的拟合和张力的消除作支持，但也伴随论文自己承认对单个标量场在理论上很困难的幽灵穿越。

#### 2.4 Lean 检查的发现

```lean
theorem stated_insufficient : ¬ ∀ v, Stated v → Conclusion v := fun h =>
  (h ⟨True, True, False, True, False, 125, 0, False, True⟩
    (by intro f hf; cases f <;> simp_all [prov, prem]) trivial).1

theorem explicit_insufficient : ¬ ∀ v, Explicit v → Conclusion v := fun h =>
  (h ⟨True, True, False, True, False, 125, 0, False, True⟩
    (by intro f hf; cases f <;> simp_all [prov, prem]) trivial).1
```

1. **`explicit_insufficient`**：即使加上标准知识，链条仍有一处真正的缺口 `gap_regular`：对这一非线性拟合，Δχ²_MAP 按 2 个自由度的 χ² 分布校准。威尔克斯定理只在正则性条件下给出这一点，论文既没有讨论也没有模拟。反例模型令 `Regular := False`：威尔克斯定理不适用，没有显著性，结论不成立。这个缺口在本项目可以探索（第三部分"环节 B · 威尔克斯校准"）。论文的主要保留——未知系统误差——不是编码中的缺口，因为论文把它写进了结论（"除非存在未知系统误差"）；去掉这个条件，链条就需要第二个"没有未知系统误差"的 GAP，而这是任何论文都无法提供的。
2. **`stated_insufficient`**：同样的原因，论文写出的内容不够。由于没有 `[implied]` 前提，明说的前提集合与加上标准知识后的集合相同；唯一缺少的前提就是这个 GAP。高斯误差则是论文明说的假设（`mod_gauss`）。
3. **每个前提都是必要的**（8 个 `_needed` 定理；`mod_gauss` 之所以必要，只是因为我们编码了论文自己给出的威尔克斯定理的充分条件，而该定理本身并不要求高斯误差）。从数据到结论只有一条路径：Δχ²、威尔克斯定理与两个解释步骤。这部分是我们编码选择的结果（§2.0）：摘要的结论针对"DESI BAO 与其他测量的组合"，依据的是 2.8–4.2σ 的范围，其中包括低于 3σ 的组合；我们只编码了 DESI + CMB。特别是，结论依赖一个用包括透镜在内的完整 CMB 似然算出的数（−12.5）；用压缩 CMB 先验时同一链条给出 2.4σ，低于 `mod_challenge` 的 3σ。
4. **按重要性排序的薄弱点**（我们的判断，不是 Lean 的）：(i) "没有未知系统误差"这一条件正是争论所在——超新星给出的 2.8–4.2σ 范围和 Dovekie 降到 3.2σ，说明校准对答案影响很大；(ii) 威尔克斯校准（`gap_regular`）是假设的，没有模拟；(iii) 显著性依赖 CMB 透镜；(iv) "可能的解释"包含幽灵行为。
5. **相容性**（`consistent`）在这里是平凡成立的：没有否定形式的前提。
6. **局限**：Lean 检查的是我们编码下的逻辑结构，不是每个前提内部的物理。

### 第三部分 · astrolab 能检验或探索的环节

| 环节 / 论断 | 能否检验或探索 | 方法 | 数据（大小） | 判据 | 结果 |
|---|---|---|---|---|---|
| R1 · 环节 A 的输入：只用 BAO 的 ΛCDM | 现在可检验 | 用 DR2 均值与协方差拟合 Ωm 与 h·r_d | DESI DR2 BAO ALL，约 3 kB | Ωm 与 h·r_d 在 README 第 2 节预注册的容差内与 0.2975 ± 0.0086、101.54 ± 0.73 Mpc 一致即为复现 | 待定 |
| R2 · 用压缩 CMB 先验的环节 A–B | 现在可检验 | 对 DESI + (θ*, ωb, ωbc) 做 ΛCDM 与 w0waCDM 的 MAP 拟合；Δχ² → σ；先验的两种解读（ωbc 含与不含 ων） | BAO 约 3 kB；先验写在代码中 | 两种解读下 Δχ²_MAP 都在 −8.0 的预注册容差内为复现；只有一种为有条件复现 | 待定 |
| R3 · 不含 CMB 的环节 A–B | 现在可检验 | DESI、DESI + Pantheon+、DESI + Union3 的 MAP 拟合 | Pantheon+ 34 MB，Union3 11 kB | Δχ²_MAP 在 −4.7、−4.9、−10.1 的预注册容差内为复现 | 待定 |
| 用完整 CMB 的环节 A（−12.5） | 不在范围内 | 需要完整的 Planck 与 ACT 似然（不是压缩数据产品） | — | — | — |
| 环节 B · 威尔克斯校准（`gap_regular`） | 可探索（不作判决） | 在 ΛCDM 最佳拟合下模拟 DESI + 压缩先验数据，重拟两个模型，把 Δχ² 分布与 χ²(2) 比较；这能为该缺口提供信息，但不能填补它，因为缺口针对的是完整 CMB 的拟合 | 不需新数据 | 无——只作探索，见 README §8 | — |
| `NoSys` · 超新星校准 | 可探索（不作判决） | DESI + 压缩 CMB + Pantheon+ / Union3 / DES-Dovekie，比较离散程度 | Dovekie 6.2 MB | 无——只作探索 | — |
| `NoSys` · 单个示踪体（tracer） | 可探索（不作判决） | 逐一去掉 DESI 的一个红移区间 | 分示踪体文件约 1 kB | 无——只作探索 | — |
| 环节 C · 参数化 | 可探索（不作判决） | 把 CPL 换成分箱 w(z) 或其他形式 | 不需新数据 | 无——只作探索 | — |
| DES-SN5YR 的组合 | 暂不在范围内 | 其协方差 53.5 MB，超过单次 50 MB 上限；以 Dovekie 代替 | — | — | — |

### 术语表

| 术语 | 含义 |
|---|---|
| BAO | 重子声学振荡：由早期宇宙声波确定的星系间优选间距 |
| r_d | 拖曳时期的声视界，即 BAO 尺子的长度（约 147 Mpc） |
| D_M、D_H | 横向共动距离与哈勃距离 c/H(z) |
| ΛCDM | 标准模型：宇宙学常数加冷暗物质 |
| w0、wa | 暗能量今天的物态方程及其变化率（CPL 参数化） |
| Δχ²_MAP | 两个模型最佳拟合 χ² 之差（MAP：最大后验） |
| 威尔克斯定理 | 对嵌套模型，若较简单的模型为真，两倍对数似然比服从自由度等于多出参数个数的 χ² 分布 |
| 压缩 CMB 先验 | 用少数几个早期宇宙参数（θ*、ωb、ωbc）的高斯分布代替完整的 CMB 似然 |
| 幽灵（phantom） | w < −1：密度随宇宙膨胀而增大的暗能量 |

### 研究进展

- 2026-11-14：第一版：第一至三部分，在实现之前写成（T-004，计划 010）；按闸门 1 审查修订（高斯误差是明说的假设；威尔克斯正则性作为 GAP `gap_regular` 补上，因而 `explicit_insufficient`）。
