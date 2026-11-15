# Has the S8 tension eased? DES Y6 against the CMB

[English](#english) · [中文](#中文)

*Paper: DES Collaboration (T. M. C. Abbott et al.) 2026, "Dark Energy Survey Year 6 Results: Cosmological Constraints from Galaxy Clustering and Weak Lensing", arXiv:2601.14559 (v2). Study:
[`studies/008-m03-s8-des-y6-cmb-parameter-difference`](https://github.com/sudoghut/astrolab/tree/main/studies/008-m03-s8-des-y6-cmb-parameter-difference).
Status: reproduced. Last updated: 2026-11-15 (see the changelog at the end). The source of this page lives in the main repository at
[`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki); edit it there.*

*中文标题：S8 张力减弱了吗？DES Y6 与 CMB 的比较。状态：已复现。论文：DES Collaboration（T. M. C. Abbott 等）2026，arXiv:2601.14559（v2）。研究：[`studies/008-m03-s8-des-y6-cmb-parameter-difference`](https://github.com/sudoghut/astrolab/tree/main/studies/008-m03-s8-des-y6-cmb-parameter-difference)。最后更新：2026-11-15（见文末"研究进展"）。本页源文件在主仓库的 [`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki) 中，请在那里修改。*

---

## English

### Part 1 · The paper in plain language

#### 1.1 The question and why it matters

How lumpy is the matter in the Universe today? Cosmologists measure this with one number,
**S8 = σ8 (Ωm/0.3)^0.5**. Here σ8 is the typical size of density fluctuations on scales of about
8 h⁻¹ Mpc (roughly 11 Mpc), and Ωm is the fraction of the Universe's energy density in matter. The
square-root combination is used because weak gravitational lensing, the main low-redshift probe,
measures approximately this combination (the best-constrained exponent depends on the survey: 0.617 for
DES Y6 3x2pt, D26 footnote 7).

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

DES imaged about 5,000 square degrees of the southern sky (the Y6 analysis uses about 4,300 square
degrees, with about 140 million source galaxies and 9 million lens galaxies, D26 Sec. VIII) with the Dark Energy Camera on the 4-m
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
S8–Ωm plane (2-D), and in the full parameter space, and finds **2.6σ, 2.2σ and 1.8σ** (Sec. V.2).
Table 6 gives the full-space numbers with a probability to exceed (PTE): 1.8σ (PTE 0.08) against
the CMB combination, 1.0σ (0.319) against Planck 2018 alone (DES Y3: 1.5σ). DES says 3x2pt is
most sensitive to directions like S8, so separations show up more clearly there. S8 (with the
exponent 0.5) is the conventional summary, not exactly the best-constrained direction: DES's
footnote 7 finds that σ8 (Ωm/0.3)^0.617 is best constrained, giving 0.799 (+0.011/−0.010) and
2.5σ from the CMB. In the S8–Ωm plane the difference against Planck alone fell from 1.9σ (Y3) to
1.4σ (Y6) and is 2.2σ against the combined CMB. In D26's words, from Y3 to Y6 both DES and the CMB
tightened and both shifted to higher S8, with "a slight increase in separation" as the net result.
Other DES combinations come closer to 3σ against the CMB: 3x2pt + supernovae + BAO 2.5σ
(PTE 0.012), all DES probes 2.8σ (PTE 0.006).

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
paper DES cites for it (its reference 153, Zhang et al. 2025, arXiv:2507.01386, identified from
D26's reference list; it gives 0.780 +0.029/−0.030); we use the cited paper directly.

#### 1.4 What they conclude, and how sure they are

- **Conclusion (Sec. VIII):** "we see no substantial evidence for a discrepancy with the CMB in
  either S8 or the full parameter space", with significances across weak-lensing experiments from
  about 1σ to at most 3σ. DES also notes that the field is "in a similar place as it was in
  previous years": D26 does not say the tension has gone away.
- **Strength:** the 1.8σ full-space number is free of any choice of direction; the 2.6σ is in the
  conventional S8 direction, one of three projections DES reports (plus an optimised direction
  in footnote 7, 2.5σ).
- **What would make them wrong:**
  - the metric or its numerical estimate could be off (the normalizing-flow estimate has noise
    that D26 does not quote);
  - an unrecognised systematic could shift DES S8 (lens bin 2 already had to be dropped);
  - "below 3σ" means "no evidence" only by an informal usage: 2.6σ corresponds to a two-sided
    Gaussian chance probability of about 1%. The rule D26 states is a criterion for combining, not a statement about evidence;
    the step to "no substantial evidence" rests on the informal usage of 3σ as the level of
    evidence, which D26 does not write out.

### Part 2 · The logic of the argument

#### 2.0 Map of the argument

A. The reference: the primary CMB combination (no lensing).
B. The measure: the parameter-difference probability, converted to n_σ.
C. The numbers: 1.8σ (full space) and 2.6σ (S8), with small projection effects.
D. [gap] Below 3σ, in S8 and in the full space, there is no substantial evidence (the informal
usage of 3σ as the level of evidence; not stated by D26 and not an authoritative rule).
⇒ No substantial evidence for a discrepancy with the CMB.
(D26's own rule, below 3σ the data sets agree well enough to combine, licenses combining; it
does not carry the conclusion.)

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

Numbers are encoded in tenths of a σ as natural numbers, meaning the reported values rounded to
one decimal; "18 tenths" is the reported "1.8", not a bound on the unrounded value.

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
| `stat_full`: full-space difference 1.8σ (reported, rounded) | STAT | stated: "we find a full parameter space difference of 1.8" | §VIII (also §V.2; Table 6, PTE 0.08) |
| `stat_s8`: difference projected onto S8 2.6σ (reported, rounded) | STAT | stated: "the difference increases to 2.6" | §VIII (also §V.2) |
| `stat_proj`: projection effects below 0.5σ | STAT | stated: "exhibits minor prior-volume effects of less than $0.5\sigma$ for all parameters of interest" | App. B |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| Prior-volume effects shift the DES mean enough to change the numbers | `stat_proj` | yes (App. B, Table 9: +0.17 in S8) |
| The normalizing-flow estimate is noisy | none | no; the numerical error is not quoted |

**Critique.** These are the numbers our study can recompute (part 3). D26 reports three
projections (1-D, 2-D, full space) and, in footnote 7, an optimised direction (2.5σ). Choosing
which projection to quote is a look-elsewhere question, but a correction for it could only lower
the significance, so it would not change a no-evidence conclusion; the 1.8σ full-space number
needs no such correction.

#### 2.3 Stage C · From the numbers to the conclusion

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `mod_crit`: below 3σ, the data sets agree well enough to combine | MOD | stated: "We set $n_{\sigma}<3$ as the criterion for different data sets agreeing well enough that it makes sense to examine their combined constraint" | §IV.6 (applied to the full space, §V.2) |
| `gap_conv`: below 3σ (Gaussian-equivalent n_σ, in both projections, given small projection effects) means no substantial evidence for a discrepancy | GAP | reconstructed | — |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| 2.6σ (two-sided Gaussian chance probability about 1%) is mild evidence for a discrepancy | `gap_conv` | no; D26 cites a range of significances, "from ∼1σ to ≲3σ" |

**Inference (Lean excerpt).**

```lean
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  have hfull : v.n_full_x10 = 18 := p .stat_full          -- Sec. V.2, VIII: 1.8 sigma
  have hs8 : v.n_s8_x10 = 26 := p .stat_s8                -- Sec. V.2, VIII: 2.6 sigma
  exact p .gap_conv (p .mod_metric) (p .stat_proj) (by omega) (by omega)  -- GAP: 3 sigma usage
```

**Critique.** D26 uses its own criterion only to justify combining ("As such, we are able to
combine", §V.2). The "no substantial evidence" sentence in §VIII cites a range of significances
across experiments, not that criterion. What links the numbers to the sentence is the informal
usage of 3σ as the level of "evidence". We first encoded it as standard knowledge (`[implied]`),
but no authoritative source fixes that rule: the reference usually cited, Lyons 2013
(arXiv:1310.1284), discusses 5σ as the traditional discovery criterion and argues against a
uniform threshold. So it is a gap (`[reconstructed]`). Three further reasons it is not automatic
here:

- the convention is written for the significance of one pre-specified test; here it is applied to
  a Gaussian-equivalent number from a Bayesian posterior comparison;
- it is a labelling convention: 3σ is where one starts to *claim* evidence, so falling short of it
  says the evidence is not strong enough to claim, not that the two data sets agree;
- the conclusion depends on the threshold: at 2.5σ the S8 projection (2.6σ) would fail it. (A
  neighbouring DES combination, all DES probes against the CMB, is at 2.8σ; it is not the subject
  of the conclusion, which is about 3x2pt.)

#### 2.4 What the Lean check found

1. **Headline: `explicit_insufficient`.** What D26 writes does not give its conclusion, and
   standard knowledge does not close the step either: the rule that turns sub-3σ numbers into
   "no substantial evidence" (`gap_conv`) is an informal usage, not stated by D26 and not fixed by
   an authoritative source. With that one gap filled, the conclusion follows. Its strength is
   exactly the strength of that usage (see 2.3).
2. **D26's own criterion does not carry the conclusion** (`mod_crit_redundant`). The n_σ < 3 rule
   of §IV.6 licenses combining DES with the CMB; the no-evidence statement needs the 3σ-as-evidence
   rule instead. The two use the same number, 3, for different purposes.
3. **Needed premises:** the metric, both numbers, the small projection effects and the gap
   (five `_needed` theorems). `obs_cmb` is redundant only because its atom appears nowhere else
   (an artefact of the encoding): the choice of CMB reference changes the numbers (1.0σ against
   Planck alone), not the logic.
4. **Where the conclusion is fragile.** It rests on the threshold (2.6σ is 0.4σ below it; the
   neighbouring all-probes combination, not the subject of the conclusion, is 0.2σ below it) and on the accuracy of the numerical estimate, which D26
   does not quote. Our study recomputes the 1-D and 2-D numbers to check that accuracy.
5. **Consistency** (`consistent`) is a weak check here: no premise is negative.
6. **Limits:** Lean checks the logical structure under our encoding, not the statistics inside
   each premise. Whether 3σ is the right yardstick for a discrepancy between
   cosmological data sets is a judgement the machine check cannot make.

### Part 3 · What astrolab can test or explore

The fiducial DES 3x2pt chain is 144 MB, above this project's 50 MB per-download limit; the user
approved a one-off download of this single file (2026-11-15). The CMB chain (11.8 MB) and the
cosmic-shear chain (14.9 MB) are under the limit. Other probes enter only as published summaries.

| Stage / claim | Can we test or explore it? | How | Data (size) | Decision criterion | Result |
|---|---|---|---|---|---|
| Inputs: the S8 means of the CMB (0.836 +0.012/−0.013), DES 3x2pt (0.789 ± 0.012) and DES cosmic shear (0.783 +0.019/−0.015) (R1) | testable now | weighted mean and 68% interval from each public chain | DES chains: 144 + 11.8 + 14.9 MB | each mean within a tolerance fixed in README §2 before running (planned: Monte Carlo error plus a stated allowance) | **reproduced**: 0.8357, 0.7893, 0.7834 |
| Stage B: 2.6σ (S8) and 2.2σ (S8–Ωm) (R2) | testable now | eqs. 17–19 from the two chains: weighted independent draws, pairwise differences, one kernel density estimate evaluated at the differences and at zero (split halves), n_σ = √2 erf⁻¹(Δ); convergence and bandwidth diagnostics fixed in advance | same | reproduced if within a tolerance fixed in README §2 before running (planned: Monte Carlo error plus an allowance of about ±0.15σ for D26's unquoted flow noise) | **reproduced**: 2.67σ (S8), 2.18σ (S8–Ωm) |
| Stage B: 1.8σ (full space) | explorable (not decisive) | Gaussian approximation over the shared parameters, with and without the directions dominated by the prior; no normalizing flows | same | none - exploration only | 0.89σ (6 parameters), 0.32σ (A_s, Ωm); depends on the parametrization (2.21σ in S8, Ωm); not a test of 1.8σ |
| DES cosmic shear against the CMB (R3) | explorable (not decisive; D26 quotes no number for it) | as R2, chain against chain | same | none - descriptive | 2.53σ (S8), 2.18σ (S8–Ωm) |
| Stage B: projection effects; Stage C: threshold and metric (R4) | explorable (not decisive) | shift DES by +0.17σ (Table 9) or use the MAP; compare iso-density, equal-tail and Gaussian versions of the same 1-D comparison; report where the threshold flips the classification | same | none - exploration only | 2.55σ (+0.17σ shift), 2.44σ (MAP); algorithms 2.67–2.68σ |
| Other probes against the CMB (R5) | explorable (not decisive) | each published S8 summary (split-normal) against the CMB chain; no averaging (probes are correlated and constrain different directions) | published values (kB) | none - descriptive | 0.2–1.7σ (ACT 0.18, KiDS-Legacy 1.04, eROSITA 1.51, HSC Zhang+ 2025 1.74) |
| Previous generation ("easing") | explorable (not decisive) | published S8 of DES Y3 3x2pt (0.776 ± 0.017), KiDS-1000 (0.766 +0.020/−0.014 3x2pt; 0.759 +0.024/−0.021 shear) and HSC Y3 (2023: cosmic shear 0.769 +0.031/−0.034, Li et al., arXiv:2304.00702, and 0.776 +0.032/−0.033, Dalal et al., arXiv:2304.00701; 3x2pt 0.775 +0.043/−0.038, Sugiyama et al., arXiv:2304.00705) against the same CMB chain, beside the new values | published values (kB) | none - descriptive | 1.4–3.1σ (DES Y3 2.83, KiDS-1000 2.92–3.14, HSC Y3 2023 1.44–1.93) |
| `gap_conv` (is below 3σ "no evidence"?) | out of scope | a judgement about evidence, not a computation; the study reports the numbers it is applied to and where the threshold flips the classification (R4) | – | – | – |
| DES systematics, blinding, the flow estimator itself | out of scope | needs the data vectors, simulations and the analysis pipeline | – | – | – |

**Results (added after the run, 2026-11-15; the table above keeps the pre-registered design).**
Details: [study README section 5](https://github.com/sudoghut/astrolab/blob/main/studies/008-m03-s8-des-y6-cmb-parameter-difference/README.md#5-results); page: [`web/index.html`](https://github.com/sudoghut/astrolab/blob/main/studies/008-m03-s8-des-y6-cmb-parameter-difference/web/index.html).

- **The numbers behind D26's conclusion are reproduced from the public chains.** S8 means: CMB
  0.8357, DES 3x2pt 0.7893, DES cosmic shear 0.7834, each within 0.001 of the published values. The
  parameter difference, computed directly from D26's equations 17–19 with a calibrated binned density
  estimate: **2.67σ ± 0.03 in S8** (D26: 2.6σ) and **2.18σ ± 0.03 in S8–Ωm** (D26: 2.2σ), both within
  the pre-registered tolerance (uncertainties from a bootstrap over chain rows, added after the
  referee). Prior support (Ωm, A_s) passed. The small excess over 2.6 (0.07σ) is about one bootstrap standard
  deviation.
- **How close to 3σ depends on projection effects.** Shifting DES by D26's own simulated bias
  (+0.17σ) gives 2.55σ; centring it on the MAP gives 2.44σ. So the S8 number sits between about
  2.4σ and 2.7σ: below the informal 3σ line in every variant, but by 0.3–0.6σ. Whether that is "no
  substantial evidence" is the gap `gap_conv` of part 2.
- **The full space needs the flows.** A Gaussian approximation in the sampled parameters gives
  0.89σ, and it depends on the coordinates: 0.32σ in (A_s, Ωm) but 2.21σ in (S8, Ωm), 1.48σ with S8
  in place of A_s (post hoc, after the referee). S8 is a nonlinear combination of A_s and Ωm and
  several parameters are prior-dominated in DES, so a Gaussian in sampled coordinates dilutes the
  difference. This is why D26 uses normalizing flows; no Gaussian number tests the 1.8σ.
- **"Easing", measured on one ruler.** Against the same CMB chain, the previous generation sits at
  1.4–3.1σ (DES Y3 2.83σ, KiDS-1000 2.92–3.14σ, HSC Y3 2023 1.44–1.93σ) and the other current probes
  at 0.2–1.7σ (KiDS-Legacy 1.04σ, HSC Y3 2025 1.74σ, ACT lensing 0.18σ, eROSITA 1.51σ above the CMB);
  DES Y6 3x2pt is at 2.67σ. Survey by survey: KiDS moved a lot (2.9–3.1σ to 1.0σ), DES a little
  (2.83σ to 2.67σ), HSC hardly at all (1.4–1.9σ to 1.74σ). So "easing" is mainly a KiDS result, not a
  general move of every survey. (If the older papers quote modes (most probable values) rather than
  means, KiDS-1000 3x2pt is at 2.93σ instead of 3.14σ.)

### Glossary

| Term | Meaning |
|---|---|
| S8 | σ8 (Ωm/0.3)^0.5: the amplitude of matter clustering, in a combination close to the one weak lensing constrains best |
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

- 2026-11-15: referee: bootstrap uncertainties (±0.03), the Gaussian full-space number depends on the parametrization, the step-A amendment labelled as procedural, R5 with modes.
- 2026-11-15: results: R1 and R2 reproduced (2.67σ in S8, 2.18σ in S8–Ωm); projection-effect variants 2.44–2.55σ; the Gaussian full-space approximation depends on the parametrization; against the same CMB, KiDS moved from 2.9–3.1σ to 1.0σ, DES from 2.83σ to 2.67σ, HSC hardly at all.
- 2026-11-15: gate-2 review: no authoritative source fixes "below 3σ means no evidence" (Lyons 2013 discusses 5σ and argues against uniform thresholds), so the step is a gap (`gap_conv`) again; headline `explicit_insufficient`.
- 2026-11-15: gate-1 review: the step to "no substantial evidence" is the standard 3σ convention (`[implied]`), not a gap; D26's combination criterion is redundant for the conclusion; S8 is not claimed to be pre-chosen or best-constrained (footnote 7); Table 6 PTEs; part 3 rows for the previous generation.
- 2026-11-15: first version: parts 1–3 (pre-registration source; plan `design/017-plan_*`).

### Sources

- DES Collaboration 2026, arXiv:2601.14559 (v2), the paper studied.
- Raveri & Hu 2019, PRD 99, 043506; Raveri & Doux 2021, arXiv:2105.03324: the parameter-difference metric.
- Lyons 2013, arXiv:1310.1284: the 5σ discovery criterion and why uniform thresholds are questionable.
- Wright et al. 2025, A&A 703, A158, arXiv:2503.19441 (KiDS-Legacy).
- Zhang et al. 2025, arXiv:2507.01386 (HSC Y3, the reference cited by D26 for HSC).
- Madhavacheril et al. 2024, ApJ 962, 113, arXiv:2304.05203 (ACT DR6 lensing).
- Ghirardini et al. 2024, A&A 689, A298, arXiv:2402.08458 (eROSITA clusters).
- DES Y3: arXiv:2105.13549; KiDS-1000: arXiv:2007.15632, arXiv:2007.15633 (previous generation).

---

## 中文

### 第一部分 · 科普详解

#### 1.1 问题与意义

今天宇宙中的物质有多"成团"？宇宙学家用一个数来衡量：**S8 = σ8 (Ωm/0.3)^0.5**。σ8 是约 8 h⁻¹ Mpc（约 11 Mpc）尺度上密度涨落的典型幅度，Ωm 是物质在宇宙能量密度中所占的比例。之所以用这种平方根组合，是因为低红移的主要探针弱引力透镜（weak gravitational lensing）大致测量这个组合（约束最好的指数因巡天而异：DES Y6 3x2pt 为 0.617，D26 脚注 7）。

得到 S8 有两种途径：

- **由早期宇宙预言。** 宇宙微波背景（CMB, cosmic microwave background）是大爆炸后 38 万年的宇宙。用标准模型（ΛCDM：宇宙学常数加冷暗物质）拟合 CMB 可以定下全部六个模型参数，模型随即预言到今天结构应长到多大。
- **在今天测量。** 对数亿个星系的巡天测量远处星系的光被中间物质偏折的程度（弱透镜），以及星系如何成团。

大约十年来，透镜巡天得到的 S8 比 CMB 的预言低百分之几，相差 2–3 个标准差（σ）。这就是 **S8 张力（S8 tension）**。如果它是真的，说明 ΛCDM 漏掉了什么（例如有相互作用的暗物质、行为出乎意料的中微子）；如果不是，就是统计涨落或微妙的系统误差。近来的结果更接近 CMB，人们开始说张力在"减弱"。本研究要问：对最新的暗能量巡天（DES, Dark Energy Survey）结果，这种说法在多大程度上成立。

#### 1.2 数据

DES 用智利 4 米 Blanco 望远镜上的暗能量相机，六年间拍摄了约 5000 平方度的南天（Y6 分析使用约 4300 平方度，约 1.4 亿个源星系与 900 万个透镜星系，D26 第 VIII 节）（Y6 是完整巡天）。D26 联合三种测量，因为每一种都是两点相关函数（two-point correlation function，即两个量随角距离的协变），所以叫 **3x2pt**：

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

**第 5 步 · 数字。** DES 在 S8 方向（1 维）、S8–Ωm 平面（2 维）和全参数空间比较两个后验，得到 **2.6σ、2.2σ 与 1.8σ**（第 V.2 节）。表 6 给出全空间数字及其超出概率（PTE, probability to exceed）：对 CMB 组合为 1.8σ（PTE 0.08），对单独的 Planck 2018 为 1.0σ（0.319；DES Y3 为 1.5σ）。DES 说 3x2pt 对 S8 这类方向最敏感，所以差别在那里更明显。S8（指数 0.5）是约定俗成的汇总量，并不恰好是约束最好的方向：DES 的脚注 7 发现 σ8 (Ωm/0.3)^0.617 约束最好，得到 0.799 (+0.011/−0.010)，与 CMB 相差 2.5σ。在 S8–Ωm 平面上，与单独的 Planck 相比，差别从 Y3 的 1.9σ 降到 Y6 的 1.4σ，与 CMB 组合相比为 2.2σ。按 D26 的说法，从 Y3 到 Y6，DES 与 CMB 都更紧、都移向较高的 S8，净结果是"分离略有增加"。DES 的其他组合离 3σ 更近：3x2pt + 超新星 + BAO 为 2.5σ（PTE 0.012），全部 DES 探针为 2.8σ（PTE 0.006）。

**第 6 步 · 判据。** D26 把 n_σ < 3 定为"两组数据足够一致、可以考察其联合约束"的判据（第 IV.6 节）。三个数字都低于 3，所以 DES 接着与 CMB 联合。

**第 7 步 · 对 DES 后验的检查。** 高维时，边缘均值可能被先验的形状拉离真值（"先验体积"效应，又称投影效应（projection effects））。DES 在其最佳拟合点生成无噪声的模拟数据向量，跑同样的流程，测量位移（真值 − 均值）/σ（附录 B 表 9）：基准分析中 S8 为 +0.17，所有关心的参数都低于 0.5σ。

**第 8 步 · 其他探针。** 第 VII.3 节中 DES 与 KiDS-Legacy 的宇宙剪切（S8 = 0.815 +0.016/−0.021）比较，认为与自己的宇宙剪切（0.783 +0.019/−0.015）一致。DES 引用 HSC Y3 为 0.804 ± 0.051；这个数在 DES 为它所引的论文（参考文献 153，Zhang et al. 2025，arXiv:2507.01386，由 D26 的参考文献表查得；给出 0.780 +0.029/−0.030）中找不到，我们直接用所引论文的数值。

#### 1.4 结论与把握程度

- **结论（第 VIII 节）：** 在 S8 和全参数空间上都"没有与 CMB 不一致的实质证据"，各弱透镜实验的显著性在约 1σ 到至多 3σ 之间。DES 也说整个领域"与前几年处在相似的位置"：D26 并没有说张力已经消失。
- **把握程度：** 全空间的 1.8σ 不依赖方向的选择；2.6σ 是约定俗成的 S8 方向上的数字，是 DES 报告的三种投影之一（脚注 7 另有一个优化方向，2.5σ）。
- **作者可能错在哪里：**
  - 度量或其数值估计可能有偏差（归一化流的估计有噪声，D26 没有报告）；
  - 未识别的系统误差可能移动 DES 的 S8（透镜第 2 个红移区间已经不得不去掉）；
  - "低于 3σ"等于"没有证据"只是一种非正式用法：2.6σ 对应约 1% 的双侧高斯偶然概率。D26 写下的规则是是否合并的判据，而不是关于证据的陈述；走到"没有实质证据"这一步靠的是把 3σ 当作证据门槛的非正式用法，D26 没有写出来。

### 第二部分 · 论证逻辑

#### 2.0 论证地图

A. 参照：主 CMB 组合（不含透镜）。
B. 度量：参数差异概率，换算成 n_σ。
C. 数字：1.8σ（全空间）与 2.6σ（S8），投影效应小。
D. [缺口] 在 S8 与全空间上都低于 3σ 时，没有实质证据（把 3σ 当作证据门槛的非正式用法；D26 没有写出，也不是权威规则）。
⇒ 没有与 CMB 不一致的实质证据。
（D26 自己的规则"低于 3σ 时两组数据足够一致、可以合并"是合并的许可，不承载结论。）

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

数字以十分之一个 σ 编码为自然数，指报告的、四舍五入到一位小数的值；"18 个十分之一"就是报告的"1.8"，不是对未四舍五入的值的界限。

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
| `stat_full`：全空间差异 1.8σ（报告值，已四舍五入） | STAT | stated: "we find a full parameter space difference of 1.8" | §VIII（又见 §V.2；表 6，PTE 0.08） |
| `stat_s8`：投影到 S8 的差异 2.6σ（报告值，已四舍五入） | STAT | stated: "the difference increases to 2.6" | §VIII（又见 §V.2） |
| `stat_proj`：投影效应低于 0.5σ | STAT | stated: "exhibits minor prior-volume effects of less than $0.5\sigma$ for all parameters of interest" | 附录 B |

**其他解释。**

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 先验体积效应使 DES 的均值移动到足以改变数字 | `stat_proj` | 是（附录 B 表 9：S8 为 +0.17） |
| 归一化流的估计有噪声 | 无 | 否；数值误差没有报告 |

**评述。** 这些是本研究可以复算的数字（第三部分）。D26 报告了三种投影（1 维、2 维、全空间），并在脚注 7 中给出一个优化方向（2.5σ）。引用哪种投影是多重检验（look-elsewhere）问题，但修正只会降低显著性，不会改变"没有证据"的结论；全空间的 1.8σ 不需要这种修正。

#### 2.3 环节 C · 从数字到结论

**前提。**

| 前提（Lean 构造子） | 标注 | 出处性质 | 论文出处 |
|---|---|---|---|
| `mod_crit`：低于 3σ 时两组数据足够一致、可以合并 | MOD | stated: "We set $n_{\sigma}<3$ as the criterion for different data sets agreeing well enough that it makes sense to examine their combined constraint" | §IV.6（用于全空间，§V.2） |
| `gap_conv`：低于 3σ（两种投影的高斯等效 n_σ，前提是投影效应小）即没有不一致的实质证据 | GAP | reconstructed | — |

**其他解释。**

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 2.6σ（双侧高斯偶然概率约 1%）是不一致的弱证据 | `gap_conv` | 否；D26 引用的是显著性的范围"from ∼1σ to ≲3σ" |

**推理（Lean 摘录）。**

```lean
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  have hfull : v.n_full_x10 = 18 := p .stat_full          -- Sec. V.2, VIII: 1.8 sigma
  have hs8 : v.n_s8_x10 = 26 := p .stat_s8                -- Sec. V.2, VIII: 2.6 sigma
  exact p .gap_conv (p .mod_metric) (p .stat_proj) (by omega) (by omega)  -- GAP: 3 sigma usage
```

**评述。** D26 只用它自己的判据来说明可以合并（"As such, we are able to combine"，§V.2）。§VIII 中"没有实质证据"一句引用的是各实验显著性的范围，而不是这个判据。把数字和这句话联系起来的，是把 3σ 当作"证据"门槛的非正式用法。我们起初把它编码为标准知识（`[implied]`），但没有权威来源规定这条规则：通常被引用的 Lyons 2013（arXiv:1310.1284）讨论的是作为传统发现判据的 5σ，并反对统一的阈值。所以它是缺口（`[reconstructed]`）。此外还有三点理由说明它在这里并不当然成立：

- 这个约定是为单个事先指定的检验的显著性写的；这里用于贝叶斯后验比较得出的高斯等效数字；
- 它是一种措辞约定：3σ 是开始*宣称*证据的门槛，达不到它说明证据不足以宣称，而不是说两组数据一致；
- 结论依赖阈值：阈值取 2.5σ 时 S8 投影（2.6σ）就不满足了。（相邻的 DES 组合，即全部 DES 探针对 CMB，为 2.8σ；它不是结论的对象，结论说的是 3x2pt。）

#### 2.4 Lean 检查发现的问题

1. **主要结果：`explicit_insufficient`。** D26 写出的前提推不出它的结论，标准知识也补不上这一步：把低于 3σ 的数字变成"没有实质证据"的规则（`gap_conv`）是一种非正式用法，D26 没有写出，也没有权威来源规定。补上这一个缺口后结论成立；它的强度正是这种用法的强度（见 2.3）。
2. **D26 自己的判据并不承载结论**（`mod_crit_redundant`）。§IV.6 的 n_σ < 3 规则允许 DES 与 CMB 合并；"没有证据"的陈述需要的是"3σ 才算证据"的规则。两者用了同一个数字 3，目的不同。
3. **必要的前提：** 度量、两个数字、投影效应小与缺口（五个 `_needed` 定理）。`obs_cmb` 之所以多余，只是因为它的原子命题在别处没有出现（编码的产物）：CMB 参照的选择改变的是数字（与单独的 Planck 比为 1.0σ），而不是逻辑。
4. **结论脆弱的地方。** 它依赖阈值（2.6σ 离阈值 0.4σ；不是结论对象的相邻组合，即全部探针的 2.8σ，离阈值 0.2σ），也依赖 D26 没有报告的数值估计精度。本研究复算 1 维与 2 维的数字，正是为了检查这个精度。
5. **相容性**（`consistent`）在这里是弱检查：没有否定形式的前提。
6. **局限：** Lean 检查的是我们编码下的逻辑结构，不是每个前提内部的统计。3σ 是否是衡量宇宙学数据集之间不一致的合适标尺，是机器检查无法作出的判断。

### 第三部分 · 本项目可检验或探索的环节

DES 的基准 3x2pt 链文件为 144 MB，超过本项目单次下载 50 MB 的上限；用户同意为这一个文件破例一次（2026-11-15）。CMB 链（11.8 MB）与宇宙剪切链（14.9 MB）在上限之内。其他探针只用已发表的汇总值。

| 环节 / 结论 | 能否检验或探索 | 方法 | 数据（大小） | 判据 | 结果 |
|---|---|---|---|---|---|
| 输入：CMB（0.836 +0.012/−0.013）、DES 3x2pt（0.789 ± 0.012）与 DES 宇宙剪切（0.783 +0.019/−0.015）的 S8 均值（R1） | 现在可检验 | 由每条公开链算加权均值与 68% 区间 | DES 链：144 + 11.8 + 14.9 MB | 每个均值与发表值之差在运行前于 README 第 2 节写定的容差内（计划：蒙特卡罗误差加写明的余量） | **复现**：0.8357、0.7893、0.7834 |
| 环节 B：2.6σ（S8）与 2.2σ（S8–Ωm）（R2） | 现在可检验 | 由两条链按式 17–19 计算：按权重独立抽样、逐对相减，用同一个核密度估计在差值样本与零点求值（拆分两半），n_σ = √2 erf⁻¹(Δ)；收敛与带宽诊断事先写定 | 同上 | 在运行前于 README 第 2 节写定的容差内（计划：蒙特卡罗误差加约 ±0.15σ 的余量，涵盖 D26 未报告的流噪声）→ 复现 | **复现**：2.67σ（S8）、2.18σ（S8–Ωm） |
| 环节 B：1.8σ（全空间） | 可探索（不能判决） | 对共有参数作高斯近似，包含与不含主要由先验决定的方向；不用归一化流 | 同上 | 无——仅供探索 | 0.89σ（6 个参数）、0.32σ（A_s、Ωm）；依赖参数化（S8、Ωm 上为 2.21σ）；不是对 1.8σ 的检验 |
| DES 宇宙剪切对 CMB（R3） | 可探索（不能判决；D26 没有给出对应的数字） | 同 R2，链对链 | 同上 | 无——描述 | 2.53σ（S8）、2.18σ（S8–Ωm） |
| 环节 B 的投影效应；环节 C 的阈值与度量（R4） | 可探索（不能判决） | DES 上移 +0.17σ（表 9）或改用 MAP；同一个 1 维比较的等密度、等尾与高斯三种算法；报告阈值在哪里改变分类 | 同上 | 无——仅供探索 | 2.55σ（上移 0.17σ）、2.44σ（MAP）；三种算法 2.67–2.68σ |
| 其他探针对 CMB（R5） | 可探索（不能判决） | 各已发表的 S8 汇总值（分裂正态）对 CMB 链；不做平均（探针相关，且约束的方向不同） | 发表值（kB） | 无——描述 | 0.2–1.7σ（ACT 0.18，KiDS-Legacy 1.04，eROSITA 1.51，HSC Zhang+ 2025 1.74） |
| 上一代（"减弱"） | 可探索（不能判决） | DES Y3 3x2pt（0.776 ± 0.017）、KiDS-1000（3x2pt 0.766 +0.020/−0.014；剪切 0.759 +0.024/−0.021）与 HSC Y3（2023：宇宙剪切 0.769 +0.031/−0.034，Li et al.，arXiv:2304.00702；0.776 +0.032/−0.033，Dalal et al.，arXiv:2304.00701；3x2pt 0.775 +0.043/−0.038，Sugiyama et al.，arXiv:2304.00705）发表的 S8 对同一条 CMB 链，与新值并列 | 发表值（kB） | 无——描述 | 1.4–3.1σ（DES Y3 2.83，KiDS-1000 2.92–3.14，HSC Y3 2023 1.44–1.93） |
| `gap_conv`（低于 3σ 是否等于"没有证据"） | 不在范围内 | 是关于证据的判断，不是计算；研究报告它所作用的数字，以及阈值在哪里改变分类（R4） | – | – | – |
| DES 的系统误差、盲化与流估计器本身 | 不在范围内 | 需要数据向量、模拟与分析流程 | – | – | – |

**结果（运行后补写，2026-11-15；上表保留预注册时的设计）。** 细节见 [研究 README 第 5 节](https://github.com/sudoghut/astrolab/blob/main/studies/008-m03-s8-des-y6-cmb-parameter-difference/README.md#5-results)；网页：[`web/index.html`](https://github.com/sudoghut/astrolab/blob/main/studies/008-m03-s8-des-y6-cmb-parameter-difference/web/index.html)。

- **D26 结论所依据的数字由公开链复现。** S8 均值：CMB 0.8357，DES 3x2pt 0.7893，DES 宇宙剪切 0.7834，与发表值之差都在 0.001 以内。直接按 D26 的式 17–19、用校准过的分箱密度估计（binned density estimate）计算参数差异：**S8 上 2.67σ ± 0.03**（D26：2.6σ），**S8–Ωm 上 2.18σ ± 0.03**（D26：2.2σ），都在预注册容差内（不确定度来自审稿后补做的、对链的行的自助法（bootstrap）重抽样）。先验支撑（Ωm、A_s）检验通过。比 2.6 略高的 0.07σ 约为一个自助法标准差。
- **离 3σ 多近取决于投影效应。** 按 D26 自己的模拟偏差（+0.17σ）平移 DES 得 2.55σ；以 MAP 为中心得 2.44σ。所以 S8 的数字在约 2.4σ 到 2.7σ 之间：每种变体都低于非正式的 3σ 线，但只差 0.3–0.6σ。这算不算"没有实质证据"，正是第二部分的缺口 `gap_conv`。
- **全空间需要归一化流。** 在采样参数中作高斯近似得到 0.89σ，而且它依赖坐标：(A_s, Ωm) 上 0.32σ，(S8, Ωm) 上 2.21σ，以 S8 代替 A_s 时 1.48σ（审稿后事后补做）。S8 是 A_s 与 Ωm 的非线性组合，DES 中好几个参数主要由先验决定，所以在采样坐标中作高斯近似会冲淡差别。这就是 D26 用归一化流的原因；没有哪个高斯数字能检验 1.8σ。
- **用同一把尺子量"减弱"。** 对同一条 CMB 链，上一代为 1.4–3.1σ（DES Y3 2.83σ，KiDS-1000 2.92–3.14σ，HSC Y3 2023 1.44–1.93σ），当前其他探针为 0.2–1.7σ（KiDS-Legacy 1.04σ，HSC Y3 2025 1.74σ，ACT 透镜 0.18σ，eROSITA 在 CMB 之上 1.51σ）；DES Y6 3x2pt 为 2.67σ。逐个巡天看：KiDS 移动很大（2.9–3.1σ 到 1.0σ），DES 移动很小（2.83σ 到 2.67σ），HSC 几乎没动（1.4–1.9σ 到 1.74σ）。所以"减弱"主要是 KiDS 的结果，而不是所有巡天的普遍变化。（若较早的论文给出的是众数（mode，最可能值）而不是均值，KiDS-1000 3x2pt 为 2.93σ 而不是 3.14σ。）

### 术语表

| 术语 | 含义 |
|---|---|
| S8 | σ8 (Ωm/0.3)^0.5：物质成团幅度，取接近弱透镜约束最好方向的组合 |
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

- 2026-11-15：审稿：自助法不确定度（±0.03），全空间高斯数字依赖参数化，第 A 步修订标注为程序性说明，R5 的众数读法。
- 2026-11-15：结果：R1 与 R2 复现（S8 上 2.67σ，S8–Ωm 上 2.18σ）；投影效应变体 2.44–2.55σ；全空间高斯近似依赖参数化；对同一 CMB，KiDS 由 2.9–3.1σ 变为 1.0σ，DES 由 2.83σ 变为 2.67σ，HSC 几乎没动。
- 2026-11-15：闸门 2 审查：没有权威来源规定"低于 3σ 即没有证据"（Lyons 2013 讨论 5σ 并反对统一阈值），这一步重新标为缺口（`gap_conv`）；主要结果为 `explicit_insufficient`。
- 2026-11-15：闸门 1 审查：走到"没有实质证据"的一步是标准的 3σ 约定（`[implied]`），不是缺口；D26 的合并判据对结论是多余的；不再说 S8 是事先选定或约束最好的方向（脚注 7）；表 6 的 PTE；第三部分加上一代的比较。
- 2026-11-15：第一版：第一至三部分（预注册的来源；计划 `design/017-plan_*`）。

### 来源

- DES Collaboration 2026，arXiv:2601.14559（v2），本文研究的论文。
- Raveri & Hu 2019，PRD 99, 043506；Raveri & Doux 2021，arXiv:2105.03324：参数差异度量。
- Lyons 2013，arXiv:1310.1284：5σ 的发现判据，以及统一阈值为何值得商榷。
- Wright et al. 2025，A&A 703, A158，arXiv:2503.19441（KiDS-Legacy）。
- Zhang et al. 2025，arXiv:2507.01386（HSC Y3，D26 为 HSC 所引的文献）。
- Madhavacheril et al. 2024，ApJ 962, 113，arXiv:2304.05203（ACT DR6 透镜）。
- Ghirardini et al. 2024，A&A 689, A298，arXiv:2402.08458（eROSITA 星系团）。
- DES Y3：arXiv:2105.13549；KiDS-1000：arXiv:2007.15632、arXiv:2007.15633（上一代）。
