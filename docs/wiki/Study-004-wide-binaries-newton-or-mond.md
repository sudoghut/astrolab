# Wide binaries: Newton or MOND at low acceleration?

[English](#english) · [中文](#中文)

*Paper(s): Cookson, Banik, El-Badry, Sutherland, Penoyre, Pittordis and Clarke 2026, "A Quality
Framework for Testing Gravity with Wide Binaries: No Evidence for MOND", MNRAS, arXiv:2602.24035
(C26); context: Banik et al. 2024, MNRAS 527, 4573, arXiv:2311.03436 (B24); Chae 2023, ApJ 952,
128, arXiv:2305.04613 (C23); Cookson 2024, MNRAS 533, 110, doi:10.1093/mnras/stae1820,
arXiv:2408.13618 (C24). Study:
[`studies/004-m07-wide-binaries-gravity-test`](https://github.com/sudoghut/astrolab/tree/main/studies/004-m07-wide-binaries-gravity-test) (web page: [online](https://sudoghut.github.io/astrolab/studies/004-m07-wide-binaries-gravity-test/web/)).
Status: concluded (2026-11-16). Last updated: 2026-11-20 (see the changelog at the end). The source of this page
lives in the main repository at
[`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki); edit it there.*

*中文标题：宽双星：低加速度下是牛顿引力还是 MOND？状态：已结束（2026-11-16）。论文：Cookson、Banik、El-Badry 等 2026（C26），arXiv:2602.24035（MNRAS）；背景：Banik 等 2024（B24），MNRAS 527, 4573，arXiv:2311.03436；Chae 2023（C23），ApJ 952, 128，arXiv:2305.04613；Cookson 2024（C24），MNRAS 533, 110，arXiv:2408.13618。研究：[`studies/004-m07-wide-binaries-gravity-test`](https://github.com/sudoghut/astrolab/tree/main/studies/004-m07-wide-binaries-gravity-test)（网页：[在线版](https://sudoghut.github.io/astrolab/studies/004-m07-wide-binaries-gravity-test/web/)）。最后更新：2026-11-20（见文末"研究进展"）。本页源文件在主仓库的 [`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki) 中，请在那里修改。*

---

## English

### Part 1 · The paper in plain language

#### 1.1 The question and why it matters

Galaxies rotate too fast at their edges for the gravity of their visible stars and gas. The
standard explanation is dark matter. An alternative, MOND (Milgromian dynamics), changes the law
of gravity itself: below an acceleration a0 ≈ 1.2 × 10⁻¹⁰ m/s² (about one hundred-billionth of
Earth's surface gravity), gravity falls off more slowly than Newton's inverse square.

Wide binaries are pairs of stars that orbit each other thousands of astronomical units (AU, the
Earth–Sun distance) apart. Beyond a few thousand AU their mutual acceleration drops below a0, so
they probe exactly the regime where MOND and Newton disagree, without any dark matter in play.
For a solar-mass pair the crossover, the MOND radius r_M = √(GM/a0), is about 7,000 AU. In the
Solar neighbourhood the Galaxy's own pull (the external field effect) caps MOND's boost: binaries
well beyond r_M should orbit about 20% faster than Newton predicts, and no faster.

Since 2023 the test has been contested. Chae (C23) reported gravity about 1.4 times stronger than
Newtonian at low acceleration (g_obs/g_N = 1.43 ± 0.06 at g_N ≈ 10^−10.15 m/s²; the paper's "10σ" combines
this with a smaller deviation, δ = 0.034 ± 0.007, at g_N ≈ 10^−8.91 m/s², both in the same direction); Banik et al. (B24) excluded MOND
at 16σ from about 8,600 binaries within 250 pc. C26 asks why careful groups disagree, writes a
quality checklist, and applies it to the cleanest sample they can build.

#### 1.2 The data

The European Space Agency's Gaia satellite measured positions, distances (from parallax, the
small annual shift of a star against the background) and motions across the sky (proper motions)
for more than a billion stars (Data Release 3, DR3). For pairs of stars at the same distance and
moving together, the difference in their proper motions times their distance gives v_sky, their
relative speed in the plane of the sky (in km/s). Their separation on the sky gives r_sky (in kAU,
thousands of AU). Their brightness gives their masses, through a mass–luminosity relation.

The key number is the scaled velocity ṽ = v_sky / √(GM/r_sky): the measured speed divided by the
Newtonian circular speed at the observed separation (C26 Eq. 9). Because orbits are tilted and
eccentric and we only see two of three dimensions, ṽ is spread out (Newtonian bound orbits have
ṽ < √2), but its typical value should not depend on separation in Newtonian gravity. In MOND it
should step up by about 20% for r_sky beyond r_M.

C26's sample (all from Gaia DR3; C26 §3–4, C24 §2):
- stars with parallax error below 2.5% (catalogue "C25"), distance within 130 pc, separation
  1–30 kAU;
- RUWE (renormalised unit weight error, a measure of how well a single-star model fits the
  astrometry) below 1.25 for both stars, to reject hidden close companions that wobble the star;
- both stars on a band of the main sequence in the colour–magnitude diagram (0.5 < BP−RP < 3.5,
  4 < M_G < 14), rejecting white dwarfs and over-luminous stars that may hide a companion;
- radial velocities (RV, speed along the line of sight) for both stars, differing by less than
  10 km/s; ṽ uncertainty below 0.1; ṽ ≤ 2.5;
- "degrouping": a pair is dropped if either star has any other star within 100 kAU, including
  faint stars with poor data, to reject triples and moving groups;
- the two stars are placed at a common distance, and a perspective ("spherical projection")
  correction removes the apparent motion that the pair's motion along the line of sight creates
  across a curved sky.

#### 1.3 Step by step: how the authors got from data to conclusion

**Step 1 — the prediction.** C26 Eq. 7 gives MOND's boost to the circular speed, including the
Galactic external field (g_N,e = 1.184 a0): the median ṽ should rise by about 20% from
r_sky/r_M ≪ 1 to r_sky/r_M ≳ 1. The Newtonian prediction is flat; its level (about 0.5) depends
on the unknown eccentricity distribution, so both models get a free normalisation.

**Step 2 — the sample.** With all cuts, C26 Table 3 lists N = 1421 pairs for ṽ ≤ 2.5 and 1216 for
the cleanest variant (ṽ ≤ 1.5 and ipd_frac_multi_peak = 0, a Gaia flag for marginally resolved
companions). The per-bin counts printed in their Figure 8 (368, 228, 144, 99, 33, 28; the numbers appear
only in the figure image) add up to 900, which the paper does not reconcile with 1421. Possible
explanations: Figure 8 may show a different cut or sample, or the six bins may not cover the whole
r_sky/r_M range.

**Step 3 — the measurement.** The pairs are split into six bins of r_sky/r_M (bin medians 0.073,
0.153, 0.348, 0.744, 1.419, 3.079; Table 2; edges not given). In each bin the median ṽ is taken,
with uncertainty "MAD/√N" (§4.2.1; MAD is the median absolute deviation). §4.1.5 also defines a
Gaussian-equivalent σ = 1.4826 MAD; the formula §4.2.1 states is MAD/√N with the raw MAD; the
scaled version (1.4826 MAD/√N) is considered below only as a hypothetical alternative. The medians are flat; Figure 8 draws
the fitted Newtonian normalisation at 0.489.

**Step 4 — the comparison.** A χ² fit of each model, with the normalisation free, gives (Table 3):

| Filter | N | χ² Newton | χ² MOND | Newton preferred by |
|---|---|---|---|---|
| ṽ ≤ 2.5 | 1421 | 2.48 | 15.10 | 548× |
| ṽ ≤ 2 | 1417 | 2.33 | 14.90 | 535× |
| ṽ ≤ 1.5 | 1408 | 1.92 | 15.49 | 883× |
| ṽ ≤ 1.5 and ipd = 0 | 1216 | 1.46 | 16.09 | 1501× |

The preference is the likelihood ratio exp(Δχ²/2). Back of the envelope: a 20% step on a median
of 0.49 is 0.10. The bins are very unequal: Figure 8 shows 368, 228, 144, 99, 33 and 28 pairs
(read from the figure image), so the two outer bins, where the step should be, have error bars of
about ±0.06–0.075, so an expected MOND offset of 0.10 in either of them alone would be only about
1.4–1.7σ (an illustration of the expected sensitivity, not a measured residual); the constraint
comes from all bins together, with the inner bins fixing the shared normalisation.

**Step 5 — robustness (§7.2–7.3).** Extending to 150 pc makes MOND 12× more likely; adding the ipd cut at
150 pc restores Newton (88×). Dropping the perspective correction raises the outer-bin median ṽ by
about 0.15 (§7.2). C26 reads these as contamination and projection effects that can mimic MOND.

#### 1.4 What they conclude, and how sure they are

"There is no observational evidence for MOND-induced velocity boosts in wide binaries", and
"Newtonian gravity is up to 1500× more likely than MOND for our cleanest sample" (abstract). For
them to be wrong, either the cleaned sample would have to hide a real MOND step behind a
separation-dependent change in eccentricities or hidden companions (which C26 explicitly assumes
away, §5), or their quoted errors would have to be too small, inflating Δχ². The 130-pc choice
also matters: at 150 pc without the ipd cut, the preference flips.

#### 1.5 The two context papers

**B24 (Banik et al. 2024).** Built its own sample from Gaia (not the El-Badry catalogue): stars
within 250 pc, G < 17, |b| > 15°, per-star astrometric-quality and extinction cuts, an RV for at
least one star, ṽ error below 0.1 (scaled at large ṽ); 8,611 pairs with r_sky = 2–30 kAU. Instead
of medians it forward-models the full (r_sky, ṽ) distribution with a mixture of bound binaries
(gravity interpolated by α_grav: 0 = Newton, 1 = MOND), undetected close companions (fitted
fraction about 63%) and chance alignments (about 2%; B24 Table 3), and finds α_grav = −0.021 (+0.065/−0.045):
MOND excluded at 16σ.

**C23 (Chae 2023).** Took about 26,600 pairs within 200 pc from the El-Badry, Rix and Heintz 2021
catalogue (chance-alignment probability below 1%, main-sequence pairs), estimated masses from
magnitudes, deprojected the sky velocities by Monte Carlo with eccentricities from Hwang et al.
2022 (C23 §III), and calibrated the close-binary fraction on the high-acceleration bin (C23
§IV.2). It reports g_obs/g_N = 1.43 ± 0.06 at g_N ≈ 10^−10.15 m/s² (about 10σ when combined with a
second deviation at higher acceleration). C26's checklist (Table 4) scores it 8 of 17 and "not
valid".

### Part 2 · The logic of the argument

#### 2.0 Map of the argument

A. MOND predicts a ~20% step in the median ṽ beyond r_M →
B. the 130 pc sample is high-purity, and eccentricities and hidden companions do not vary with
separation →
C. the observed median ṽ is flat, and Δχ² is about 12–16 →
D. (our GAP: the per-bin median errors are not underestimated) →
E. (standard likelihood-ratio reasoning) ⇒ Newton is up to 1500× more likely than MOND.

How we check it: the argument is written in Lean 4
([`studies/004-m07-wide-binaries-gravity-test/argument/Argument.lean`](https://github.com/sudoghut/astrolab/blob/main/studies/004-m07-wide-binaries-gravity-test/argument/Argument.lean)).
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
explicit (`explicit_*`) premises suffice. It does not check the physics inside the premises: the
atoms are uninterpreted propositions.

We encode the quantitative conclusion ("up to 1500× more likely"), not the qualitative "no
evidence for MOND": a flat profile is no evidence for MOND whatever the errors, but the size of
the preference depends on them.

#### 2.1 Stage A–B · Prediction and sample

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `mod_step`: MOND predicts a ~20% faster orbit beyond r_M | MOD | stated 2602.24035: "should orbit each other 20% faster than the Newtonian expectation if their separation exceeds" | §8 (cites Eq. 3); step shape Eq. 7, Fig. 8 caption |
| `stat_pure`: the 130 pc sample is high-purity | STAT | stated 2602.24035: "we compile a high-purity sample of WBs within 130 pc" | Abstract |
| `mod_notrend`: eccentricities and hidden close binaries do not vary with separation | MOD | stated 2602.24035: "Our conclusion assumes that the WB eccentricity distribution and the incidence of undetected CBs do not vary with the WB separation" | §5 |

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| hidden close binaries inflate ṽ more at large separation | `stat_pure`, `mod_notrend` | partly: cuts plus the assumption; argued unlikely to *cancel* a MOND step (§5) |
| a different eccentricity distribution mimics or hides the step | `mod_notrend` | assumed; B24 Figs. 15–16 cited |
| projection effects | `stat_pure` (the correction is part of the pipeline) | yes, §4.1.6 |

**Critique.** "High-purity" is argued through the checklist, not measured; the 150-pc flip shows
the result depends on how far out the sample goes. The sample-size discrepancy (1421 in Table 3,
about 900 in Figure 8's bins) is unexplained.

#### 2.2 Stage C–E · From flat medians to "1500×"

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `stat_flat`: the median ṽ shows no 20% step | STAT | stated 2602.24035: "does not exhibit the 20% enhancement expected from MOND and is consistent with Newtonian gravity across all separations" | Abstract |
| `stat_lr`: Δχ² is about 12–16 | STAT | stated 2602.24035: "The $\Delta\chi^{2}$ of about $12-16$ implies a likelihood ratio" | §5, Table 3 |
| `gap_err`: the per-bin median errors are not underestimated | GAP | reconstructed: the paper gives the median's uncertainty as MAD/√N (§4.2.1) (the stated formula; §4.1.5 separately defines σ = 1.4826 MAD, considered as a hypothetical alternative); the asymptotic standard error of a median is 1/(2 f(m) √N) (Cramér 1946, Mathematical Methods of Statistics, §28.5), which for a Gaussian is 1.86 MAD/√N, or 1.2533 times 1.4826 MAD/√N; under either reading the paper does not show its errors are calibrated for the actual ṽ distribution | — |
| `mod_lr`: under a Gaussian error model, calibrated errors and a large Δχ² give a valid likelihood ratio (the Gaussian model is a further assumption, not covered by `gap_err`) | MOD | implied: likelihood-ratio reasoning (Wasserman 2004, ch. 10) | — |
| `mod_rule`: flat, unbiased data with a valid, large likelihood ratio disfavour the step model | MOD | implied: likelihood-ratio reasoning (Wasserman 2004, ch. 10) | — |

```lean
have lr : v.LRValid := p .mod_lr (p .gap_err) (p .stat_lr)  -- Sec. 4.2.1, 5 (Table 3); GAP
exact p .mod_rule (p .stat_flat) (p .mod_step) (p .stat_pure) (p .mod_notrend) lr  -- Abstract, Sec. 5, 8
```

**Critique.** The large-sample standard error of a median is 1/(2 f(m) √N), where f(m) is the
probability density at the median; MAD/√N equals it only if f(m)·MAD = 0.5. For example shapes the
true error would be larger by a factor of 1.44 (Laplace), 1.86 (Gaussian), 2.0 (uniform) or 2.08
(exponential); whether any of these describes the ṽ distribution in each bin is not known, so
these are illustrations, not evidence that C26's errors are too small. Two readings of the paper,
taking the Gaussian factor as an example:
- if Table 3 used MAD/√N (§4.2.1 says so), with the Gaussian factor every χ² shrinks by about 3.45:
  Δχ² 12.6 → 3.7 (likelihood ratio about 6, not 548) and, for the cleanest row, 14.6 → 4.2 (about
  8, not 1501);
- if it used 1.4826 MAD/√N (the σ of §4.1.5), the factor 1.2533 remains: Δχ² 12.6 → 8.0 (about 55)
  and 14.6 → 9.3 (about 105).

Either way the stated ratio needs errors the paper does not justify. Counter-evidence: the Newton
χ² values are already small (2.48 and 1.46 for 5 degrees of freedom); with errors 1.86 times larger
they would be about 0.7 and 0.4, a suspiciously good fit (p ≈ 0.98–0.995), which weakly suggests
the errors are not underestimated by that much. A flat profile would still give no evidence for
MOND; only the size of the preference is at stake. This repo tests it directly with a bootstrap
(part 3, R2).

#### 2.3 What the Lean check found

1. **`explicit_insufficient`**: even with standard knowledge the chain needs `gap_err`, that the
   per-bin errors are not underestimated. It enters through the statistical link `mod_lr`
   (calibrated errors and a large Δχ² give a valid likelihood ratio), separately from the
   interpretation step `mod_rule`. The paper states its error formula but does not show it is
   calibrated; the standard formula for a median's error differs from MAD/√N unless the
   distribution has a particular shape, and the small Newton χ² is weak counter-evidence (2.2).
   What this does and does not show: the two implied steps are our encoding of the paper's
   implicit reasoning, so the verdict says that, on this reading, the stated likelihood ratio
   needs an error calibration the paper does not supply; it does not show the errors are wrong.
   That is an empirical question, tested by R2.
2. **`stated_insufficient`**: besides the gap, the two inference steps are standard
   likelihood-ratio reasoning (`mod_lr`, `mod_rule`, implied).
3. **Every premise is needed** (eight `_needed` theorems): a single route.
4. **Consistency** (`consistent`) holds trivially: no premise is negative, and `mod_rule` is an
   implication.
5. **Weak points** (ours): the error calibration (`gap_err`); the assumption of no separation
   trends (`mod_notrend`); the distance limit (150 pc flips the result); the N = 1421 versus
   ~900 discrepancy; bin edges not published.
6. **Limits**: Lean checks the structure of our encoding, not the physics or the numbers behind
   the atoms.

### Part 3 · What astrolab can test or explore

| Stage / claim | Can we test or explore it? | How | Data (size) | Decision criterion | Result |
|---|---|---|---|---|---|
| R1 · the sample and the median profile (stages B–C) | testable now | rebuild C26's sample with Gaia DR3 server-side self-joins (no 1.8 GB El-Badry catalogue), same cuts, median ṽ in six bins | candidate pairs and per-star neighbour counts, provisionally 10–40 MB (counts first; plan 013) | N within ±20% of 1421 / 1216; per-bin comparison with Fig. 8 diagnostic only (including which error formula reproduces Fig. 8's error bars, about ±0.013 at N = 368); overall median vs 0.489 | **different sample**: N = 639 vs 1421 (per x bin 3, 215, 232, 109, 56, 24 vs 368, 228, 144, 99, 33, 28); A = 0.499 vs 0.489 |
| R2 · `gap_err` and stage D–E: does Δχ² survive calibrated errors? | testable now | same χ² comparison with a whole-sample bootstrap covariance of the six medians (primary; five after the pre-registered merge of a sparse bin, as happened in the run) and C26's MAD/√N (reproduction column) | same | relative likelihood ≥ 100 → Newton preferred (agrees with C26); between 1/100 and 100 → cannot distinguish; ≤ 1/100 → MOND preferred | **cannot distinguish**: L = 0.49 (bootstrap errors); L = 1.7 × 10⁻⁵ with MAD/√N; noise-free Newtonian data would give only L = 6.2 (no power; referee, post hoc) |
| R3 · stage B: robustness of "high-purity" | explorable (descriptive) | switch C26's choices off one at a time (projection correction, HR cut, 150/200 pc, parallax S/N > 100, ipd = 0, degrouping) | same | none — exploration only, see README §8 | most variants cannot distinguish (L 0.13–1.2); 6 of 14 invalid (more than 5% of bootstrap replicates redrawn) |
| R4 · B24 cuts | explorable (descriptive) | median profile with B24's 250 pc, G < 17 selection | larger query (count first) | none — exploration only | not run |

The Gaia archive is offline 2026-11-25 to 12-02, so data are fetched and cached before then;
velocity columns are fetched only after the study's pre-registration is committed (plan 013).

**What we found (2026-11-16).** The server-side rebuild gives 639 pairs, less than half of C26's 1421:
relative to C26's Fig. 8 counts, almost all of the shortfall is C26's lowest x bin, which its stated
1 kAU floor cannot populate.
With the pre-registered bootstrap errors the test cannot distinguish Newton from MOND (L = 0.49), but
the independent referee found (post hoc) that the test had no power: noise-free Newtonian data would give only L = 6.2. With C26's MAD/√N
errors (the formula C26 states) the same medians give L = 1.7 × 10⁻⁵ (MOND), so on our sample the error convention decides the
outcome, the numerical form of `gap_err`. After the independent referee (post hoc): with the r_sky
floor at 300 AU the sample (1250 pairs) matches C26's bins much better, and the likelihood ratio swings
by orders of magnitude with the HR cut and the degrouping (196 Newton to 4.5 × 10⁻⁴ MOND). A
pre-registered re-test is registered (T-034). Numbers and page: the study README section 5 and
`web/index.html`.

**Update 2026-11-18, R5 (T-034, pre-registered): not run.** The enlarged design (d < 250 pc, r_sky ≥
300 AU) had a velocity-free power gate (G1b) applied before any velocity was fetched. It failed:
after the velocity-free cuts the counts were 53% of the design prediction, giving a predicted
likelihood ratio of 68 under Newtonian truth (needed ≥ 100) and 0.028 under MOND truth (needed ≤
0.01), so the velocities were never fetched and R5 gives no verdict. The independent referee (post
hoc, verified by us) traced the shortfall to degrouping: C26's relaxed neighbour rule keeps 44% of
pairs at 130 pc but 23% at 250 pc; pairs at 300–1,000 AU survive only 11% at 150–250 pc, and
survival falls steeply towards the Galactic plane (to 2% at |b| < 10°). The parallax window that
defines a "neighbour" deepens with distance, so this points to chance neighbours rather than real
triples (an inference; the direct test is T-043). The rule most likely does not scale beyond about 130–150 pc;
larger published samples (Banik et al. 2024, arXiv:2311.03436; El-Badry et al. 2021,
arXiv:2101.05282) model or estimate contamination instead. A chance-neighbour measurement is
registered (T-043). Numbers: [`results/r5.json`](https://github.com/sudoghut/astrolab/blob/main/studies/004-m07-wide-binaries-gravity-test/results/r5.json).

**Update 2026-11-20, chance neighbours (T-043, exploration, post hoc).** We counted, for every star of
the R5 candidate pairs with parents beyond 29.9 pc, the neighbours that the relaxed rule would find around a position shifted 2°
in declination: such a circle holds no real companion, so its count is the chance-neighbour rate at
the same depth. The fraction of pairs whose two shifted circles are both empty matches the observed
survival closely: 0.47 against 0.42 at 29.9–130 pc, 0.24 against 0.22 at 130–150 pc, 0.11 against
0.10 at 150–250 pc, with the same fall towards the Galactic plane, and real extra neighbours per star
(3.8–6.0) match the shifted count (4.1–5.7). So the degrouping loss is close to a chance-only
expectation, which supports the referee's inference that it is mostly chance neighbours; the
remainder, about 12% of the expected survival at 29.9–130 pc and 6% beyond, is a proxy difference
(not a bound) that may hold losses to real triples and moving groups but also shift bias and noise. A larger sample would need a
degrouping rule that allows for chance neighbours, and so a new pre-registration. Numbers in the
study README, section 5 (script
[`explore/t043_shifted_neighbours.py`](https://github.com/sudoghut/astrolab/blob/main/studies/004-m07-wide-binaries-gravity-test/explore/t043_shifted_neighbours.py)).

### Glossary

| Term | Meaning |
|---|---|
| MOND | Milgromian dynamics: gravity is boosted below the acceleration scale a0 ≈ 1.2 × 10⁻¹⁰ m/s² |
| MOND radius r_M | √(GM/a0): the separation at which a binary's internal acceleration equals a0 (~7 kAU for 1 M☉) |
| external field effect | in MOND, the Galaxy's own gravity limits the boost a binary can get (~20% in velocity here) |
| ṽ (scaled velocity) | sky-plane relative velocity divided by the Newtonian circular speed at the projected separation |
| RUWE | Gaia's renormalised unit weight error; values above ~1.25 suggest an unseen companion |
| degrouping | removing pairs that share a star with another pair or have a third star nearby |
| MAD | median absolute deviation; 1.4826 MAD estimates a Gaussian σ |
| likelihood ratio | exp(Δχ²/2): how much better one model explains the data than another |

### Open questions

- Which median-error formula fed Table 3, and why do the Figure 8 bin counts (900, read from the
  figure image) differ from N = 1421?
- Does a MOND-like rise appear in any reasonable variant (R3), and is it step-like or a steady
  rise (C26 argues systematics give a steady rise)?

### Changelog

- 2026-11-20: T-043 (exploration, post hoc): a 2° shifted field shows that the relaxed degrouping
  loss is close to a chance-only expectation, so mostly chance neighbours (observed survival 0.42 / 0.22 / 0.10 against 0.47 / 0.24
  / 0.11 expected from chance alone in the three shells) (part 3 update).
- 2026-11-18: R5 (T-034): pre-registered power gate G1b failed (L_N* 68 < 100), velocities not
  fetched, R5 not run; referee (post hoc): relaxed degrouping keeps 23% of pairs at 250 pc (44% at
  130 pc), pointing to chance neighbours (inference; direct test T-043); T-043 registered (part 3 update).
- 2026-11-16: study run (steps A and B) and independent referee: different sample (639 pairs), cannot
  distinguish (L = 0.49) with no power; post-hoc r_sky 300 AU exploration; T-034 registered; part 3 results.
- 2026-11-14: first version: parts 1–3, written before implementation (T-013, plan 013).

### Sources

- Cookson et al. 2026, arXiv:2602.24035 (HTML read 2026-11-14).
- Cookson 2024, arXiv:2408.13618 (PDF read 2026-11-14), MNRAS 533, 110.
- Banik et al. 2024, arXiv:2311.03436; Chae 2023, arXiv:2305.04613; Chae et al. 2026,
  arXiv:2601.21728 (abstract-level context).

---

## 中文

### 第一部分 · 科普详解

#### 1.1 问题与意义

星系边缘的旋转速度太快，光靠看得见的恒星和气体的引力解释不了。标准的解释是暗物质（dark matter）。另一种解释是 MOND（Milgromian dynamics，米尔格罗姆动力学），它修改引力定律本身：当加速度低于 a0 ≈ 1.2 × 10⁻¹⁰ m/s²（约为地表重力的一千亿分之一）时，引力衰减得比牛顿的平方反比律慢。

宽双星（wide binaries）是相隔数千个天文单位（AU, astronomical unit，日地距离）互相绕转的两颗恒星。间距超过几千 AU 时，它们之间的加速度低于 a0，正好落在 MOND 与牛顿引力分歧的区域，而且不牵涉暗物质。对一个太阳质量的双星，分界点即 MOND 半径（MOND radius）r_M = √(GM/a0)，约 7,000 AU。在太阳附近，银河系本身的引力（外场效应（external field effect））限制了 MOND 的增强：远在 r_M 之外的双星，轨道速度应比牛顿预期快约 20%，不会更快。

2023 年以来这一检验争议不断。Chae（C23）报告低加速度下的引力约为牛顿的 1.4 倍（在 g_N ≈ 10^−10.15 m/s² 处 g_obs/g_N = 1.43 ± 0.06；论文的"10σ"是把它与 g_N ≈ 10^−8.91 m/s² 处较小的偏差 δ = 0.034 ± 0.007 合起来，两者方向相同）；Banik 等（B24）用 250 pc 以内约 8,600 对双星以 16σ 排除 MOND。C26 追问为什么认真的团队会得出相反结论，写出一份质量清单，并用它建立尽可能干净的样本。

#### 1.2 数据

欧洲空间局（ESA, European Space Agency）的 Gaia 卫星（名字原为 Global Astrometric Interferometer for Astrophysics 的缩写）为十亿多颗恒星测量了位置、距离（由视差（parallax），即恒星相对背景的周年微小位移）和天球上的运动（自行（proper motion））（第三次数据发布，DR3）。对距离相同、一起运动的两颗星，两者自行之差乘以距离，就是它们在天球平面内的相对速度 v_sky（km/s）；天球上的间距给出 r_sky（kAU，千天文单位）；亮度经质光关系（mass–luminosity relation）给出质量。

关键量是缩放速度（scaled velocity）ṽ = v_sky / √(GM/r_sky)：测得的速度除以该间距上的牛顿圆周速度（C26 式 9）。由于轨道倾斜、有偏心率（eccentricity），而我们只看到三维中的两维，ṽ 是一个分布（牛顿束缚轨道的 ṽ < √2），但在牛顿引力中它的典型值不应随间距变化；在 MOND 中，r_sky 超过 r_M 时它应升高约 20%。

C26 的样本（全部来自 Gaia DR3；C26 第 3–4 节，C24 第 2 节）：
- 视差误差小于 2.5% 的恒星（星表"C25"，即 catalogue with parallax error ≤ 2.5%），距离 130 pc 以内，间距 1–30 kAU；
- 两颗星的 RUWE（renormalised unit weight error，单星模型拟合天体测量数据的好坏）都小于 1.25，以排除使恒星摆动的隐藏近伴星；
- 两颗星都位于颜色—星等图（colour–magnitude diagram）主序（main sequence）上的一条带内（0.5 < BP−RP < 3.5，4 < M_G < 14），排除白矮星与可能藏有伴星的过亮恒星；
- 两颗星都有视向速度（RV, radial velocity），相差小于 10 km/s；ṽ 的误差小于 0.1；ṽ ≤ 2.5；
- "去群"（degrouping）：任一颗星在 100 kAU 以内还有其他恒星（包括数据很差的暗星）时，整对去掉，以排除三合星（triple）与移动星群（moving group）；
- 两颗星放在同一个距离上，并做透视修正（perspective correction，即"球面投影"修正），去掉双星沿视线的运动在弯曲天球上造成的表观运动。

#### 1.3 一步一步：作者如何从数据走到结论

**第 1 步——预测。** C26 式 7 给出 MOND 对圆周速度的增强（含银河系外场 g_N,e = 1.184 a0）：中位数 ṽ 应从 r_sky/r_M ≪ 1 到 r_sky/r_M ≳ 1 升高约 20%。牛顿的预测是平的；其高度（约 0.5）取决于未知的偏心率分布，所以两个模型都有一个自由的归一化（normalisation）。

**第 2 步——样本。** 加上全部切割后，C26 表 3 给出 ṽ ≤ 2.5 时 N = 1421 对，最干净的变体（ṽ ≤ 1.5 且 ipd_frac_multi_peak = 0，即图像参数测定中出现多峰的比例（image parameter determination multi-peak fraction），Gaia 用它标记边缘可分辨的伴星）为 1216 对。他们图 8 中印出的各箱数目（368、228、144、99、33、28，这些数字只出现在图中）加起来为 900，论文没有说明它与 1421 的差别。可能的解释：图 8 用的是不同的切割或样本，或者六个箱没有覆盖全部 r_sky/r_M 范围。

**第 3 步——测量。** 双星按 r_sky/r_M 分成六个箱（各箱中位数 0.073、0.153、0.348、0.744、1.419、3.079；表 2；没有给出边界）。每箱取 ṽ 的中位数，误差为"MAD/√N"（第 4.2.1 节；MAD 是中位数绝对偏差（median absolute deviation））。第 4.1.5 节还定义了高斯等效的 σ = 1.4826 MAD；第 4.2.1 节写明的公式是用原始 MAD 的 MAD/√N；乘过系数的版本（1.4826 MAD/√N）下面只作为假设的另一种可能讨论。各箱中位数平坦；图 8 把拟合的牛顿归一化画在 0.489。

**第 4 步——比较。** 每个模型在归一化自由时做 χ² 拟合，得到（表 3）：

| 切割 | N | 牛顿 χ² | MOND χ² | 牛顿受偏好倍数 |
|---|---|---|---|---|
| ṽ ≤ 2.5 | 1421 | 2.48 | 15.10 | 548× |
| ṽ ≤ 2 | 1417 | 2.33 | 14.90 | 535× |
| ṽ ≤ 1.5 | 1408 | 1.92 | 15.49 | 883× |
| ṽ ≤ 1.5 且 ipd = 0 | 1216 | 1.46 | 16.09 | 1501× |

偏好倍数是似然比（likelihood ratio）exp(Δχ²/2)。粗估：在 0.49 的中位数上升高 20% 就是 0.10。各箱的双星数很不均匀：图 8 中为 368、228、144、99、33、28 对（从图上读出），所以最该出现台阶的两个外侧箱误差约 ±0.06–0.075，预期的 0.10 的 MOND 偏移在其中任何一箱单独只有约 1.4–1.7σ（这是对预期灵敏度的示意，不是测得的残差）；约束来自所有箱的合力，内侧几箱确定共同的归一化（normalisation）。

**第 5 步——稳健性（第 7.2–7.3 节）。** 扩展到 150 pc 时 MOND 受偏好约 12 倍；在 150 pc 加上 ipd 切割后牛顿恢复受偏好（88 倍）。不做透视修正会使外侧箱的中位数 ṽ 升高约 0.15（第 7.2 节）。C26 把这些解读为能模仿 MOND 的污染与投影效应。

#### 1.4 结论与把握程度

"宽双星中没有 MOND 引起的速度增强的观测证据"，以及"在我们最干净的样本中，牛顿引力的可能性最高为 MOND 的 1500 倍"（摘要）。要让他们错，要么干净样本中有随间距变化的偏心率或隐藏伴星恰好掩盖了真实的 MOND 台阶（C26 明确假设没有这种变化，第 5 节），要么他们给出的误差太小、夸大了 Δχ²。130 pc 的选择也很关键：在 150 pc、不加 ipd 切割时，偏好会翻转。

#### 1.5 两篇背景论文

**B24（Banik 等 2024）。** 自己从 Gaia 建样本（不用 El-Badry 星表）：250 pc 以内、G < 17、|b| > 15° 的恒星，逐星的天体测量质量与消光切割，至少一颗星有视向速度，ṽ 误差小于 0.1（ṽ 大时放宽）；r_sky = 2–30 kAU 的 8,611 对。它不用中位数，而是对整个 (r_sky, ṽ) 分布做前向建模：束缚双星（引力由 α_grav 插值：0 为牛顿，1 为 MOND）、未探测到的近伴星（拟合比例约 63%）与偶然成对（约 2%；B24 表 3）的混合，得到 α_grav = −0.021（+0.065/−0.045）：以 16σ 排除 MOND。

**C23（Chae 2023）。** 从 El-Badry、Rix 与 Heintz 2021 星表中取 200 pc 以内约 26,600 对（偶然成对概率小于 1%，主序对），由星等估计质量，用 Hwang 等 2022 的偏心率以蒙特卡罗方法对天球速度去投影（C23 第 III 节），并用高加速度箱标定近伴星比例（C23 第 IV.2 节）。它报告在 g_N ≈ 10^−10.15 m/s² 处 g_obs/g_N = 1.43 ± 0.06（与较高加速度处的另一偏差合起来约 10σ）。C26 的清单（表 4）给它 17 分中的 8 分，评为"无效"。

### 第二部分 · 论证逻辑

#### 2.0 论证地图

A. MOND 预测 r_M 以外中位数 ṽ 升高约 20% →
B. 130 pc 样本纯度高，偏心率与隐藏伴星不随间距变化 →
C. 观测到的中位数 ṽ 平坦，Δχ² 约为 12–16 →
D. （我们补上的 GAP：各箱中位数的误差没有被低估）→
E. （标准的似然比推理）⇒ 牛顿的可能性最高为 MOND 的 1500 倍。

检查方法：论证写成 Lean 4（[`studies/004-m07-wide-binaries-gravity-test/argument/Argument.lean`](https://github.com/sudoghut/astrolab/blob/main/studies/004-m07-wide-binaries-gravity-test/argument/Argument.lean)）。每个前提是 `Field` 的一个构造子（constructor）（不用公理），标明类型与出处性质：

| 标签 | 前提类型 |
|---|---|
| `OBS` | 观测或测量（注明表格、图） |
| `MOD` | 模型假设 |
| `STAT` | 统计推断（显著性、模型比较） |
| `NUM` | 数值结果，由本仓库 `run.py` 复核 |
| `LIT` | 引自其他文献的结论 |
| `GAP` | 推理需要、但论文和标准知识都没有提供的前提 |

出处性质：`[stated <arXiv 编号>: "引文"]`、`[implied]`（标准知识，注明来源）、`[reconstructed]`（我们补上的，恰好是 `GAP` 前提）。Lean 检查结论能推出（`final`）、不是恒真（`final_nontrivial`）、前提相容、任何单个前提都不够、哪些前提必要，以及论文明说的（`stated_*`）或加上标准知识的（`explicit_*`）前提是否足够。它不检查前提里的物理：原子命题（atom）不作解释。

我们编码的是定量结论（"最高 1500 倍"），而不是定性的"没有 MOND 的证据"：无论误差如何，平坦的曲线都不是 MOND 的证据，但偏好的大小取决于误差。

#### 2.1 环节 A–B · 预测与样本

| 前提（Lean 构造子） | 标签 | 出处性质 | 论文出处 |
|---|---|---|---|
| `mod_step`：MOND 预测 r_M 以外轨道快约 20% | MOD | stated 2602.24035："should orbit each other 20% faster than the Newtonian expectation if their separation exceeds" | 第 8 节（引式 3）；台阶形状见式 7 与图 8 说明 |
| `stat_pure`：130 pc 样本纯度高 | STAT | stated 2602.24035："we compile a high-purity sample of WBs within 130 pc" | 摘要 |
| `mod_notrend`：偏心率与隐藏近伴星不随间距变化 | MOD | stated 2602.24035："Our conclusion assumes that the WB eccentricity distribution and the incidence of undetected CBs do not vary with the WB separation" | 第 5 节 |

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 隐藏近伴星在大间距处更多地抬高 ṽ | `stat_pure`、`mod_notrend` | 部分：切割加假设；论证它不太可能恰好*抵消* MOND 台阶（第 5 节） |
| 不同的偏心率分布模仿或掩盖台阶 | `mod_notrend` | 假设；引 B24 图 15–16 |
| 投影效应 | `stat_pure`（修正是管线的一部分） | 是，第 4.1.6 节 |

**评论。** "纯度高"是用清单论证的，不是测出来的；150 pc 时偏好翻转说明结果依赖样本延伸多远。样本数的差别（表 3 为 1421，图 8 各箱合计约 900）没有解释。

#### 2.2 环节 C–E · 从平坦的中位数到"1500 倍"

| 前提（Lean 构造子） | 标签 | 出处性质 | 论文出处 |
|---|---|---|---|
| `stat_flat`：中位数 ṽ 没有 20% 的台阶 | STAT | stated 2602.24035："does not exhibit the 20% enhancement expected from MOND and is consistent with Newtonian gravity across all separations" | 摘要 |
| `stat_lr`：Δχ² 约为 12–16 | STAT | stated 2602.24035："The $\Delta\chi^{2}$ of about $12-16$ implies a likelihood ratio" | 第 5 节，表 3 |
| `gap_err`：各箱中位数的误差没有被低估 | GAP | reconstructed：论文把中位数的误差写成 MAD/√N（第 4.2.1 节），（论文写明的公式；第 4.1.5 节另外定义了 σ = 1.4826 MAD，作为假设的另一种可能）；中位数的渐近标准误为 1/(2 f(m) √N)（Cramér 1946，Mathematical Methods of Statistics，第 28.5 节），对高斯分布为 1.86 MAD/√N，即 1.4826 MAD/√N 的 1.2533 倍；无论哪种读法，论文都没有说明它的误差对实际的 ṽ 分布是标定正确的 | — |
| `mod_lr`：在高斯误差模型下，误差标定正确且 Δχ² 大时，似然比是有效的（高斯模型是另一个假设，不在 `gap_err` 之内） | MOD | implied：似然比推理（Wasserman 2004，第 10 章） | — |
| `mod_rule`：平坦、无偏的数据加上有效且大的似然比不支持台阶模型 | MOD | implied：似然比推理（Wasserman 2004，第 10 章） | — |

```lean
have lr : v.LRValid := p .mod_lr (p .gap_err) (p .stat_lr)  -- Sec. 4.2.1, 5 (Table 3); GAP
exact p .mod_rule (p .stat_flat) (p .mod_step) (p .stat_pure) (p .mod_notrend) lr  -- Abstract, Sec. 5, 8
```

**评论。** 大样本下中位数的标准误为 1/(2 f(m) √N)，f(m) 是中位数处的概率密度；只有 f(m)·MAD = 0.5 时它才等于 MAD/√N。以几种分布为例，真实误差会大 1.44 倍（拉普拉斯分布）、1.86 倍（高斯分布）、2.0 倍（均匀分布）或 2.08 倍（指数分布）；各箱 ṽ 的分布是否像其中任何一种并不知道，所以这些只是示例，不是 C26 误差偏小的证据。以高斯的倍数为例，对论文有两种读法：
- 如果表 3 用的是 MAD/√N（第 4.2.1 节如此写），按高斯的倍数，每个 χ² 缩小约 3.45 倍：Δχ² 12.6 → 3.7（似然比约 6，而不是 548），最干净的一行 14.6 → 4.2（约 8，而不是 1501）；
- 如果用的是 1.4826 MAD/√N（第 4.1.5 节的 σ），仍差 1.2533 倍：Δχ² 12.6 → 8.0（约 55），14.6 → 9.3（约 105）。

无论哪种读法，论文给出的倍数都依赖它没有论证的误差。反面证据：牛顿模型的 χ² 本来就小（5 个自由度下 2.48 与 1.46）；误差放大 1.86 倍后约为 0.7 与 0.4，拟合好得可疑（p ≈ 0.98–0.995），这弱地提示误差并没有被低估那么多。平坦的曲线仍然不是 MOND 的证据；受影响的只是偏好的大小。本项目用自助法（bootstrap）直接检验（第三部分 R2）。

#### 2.3 Lean 检查的发现

1. **`explicit_insufficient`**：即使加上标准知识，链条仍需要 `gap_err`，即各箱误差没有被低估。它经由统计连接 `mod_lr`（误差标定正确且 Δχ² 大时似然比有效）进入，与解释一步 `mod_rule` 分开。论文写出了误差公式，但没有说明它是标定正确的；除非分布具有特定形状，中位数误差的标准公式与 MAD/√N 不同，而牛顿模型的小 χ² 是弱的反面证据（2.2）。这能说明什么、不能说明什么：两个 implied 的推理步骤是我们对论文隐含推理的编码，所以这一结论说的是：按这种理解，论文给出的似然比需要一个论文没有提供的误差标定；它并不说明误差是错的，那是一个经验问题，由 R2 检验。
2. **`stated_insufficient`**：除这一缺口外，两个推理步骤是标准的似然比推理（`mod_lr`、`mod_rule`，implied）。
3. **每个前提都是必要的**（8 个 `_needed` 定理）：只有一条路径。
4. **相容性**（`consistent`）平凡成立：没有否定形式的前提，`mod_rule` 是一个蕴涵。
5. **薄弱点**（我们的判断）：误差标定（`gap_err`）；没有随间距变化的假设（`mod_notrend`）；距离上限（150 pc 时结果翻转）；N = 1421 与约 900 的差别；没有发表分箱边界。
6. **局限**：Lean 检查的是我们编码的结构，不是原子背后的物理或数字。

### 第三部分 · astrolab 能检验或探索的环节

| 环节 / 论断 | 能否检验或探索 | 方法 | 数据（大小） | 判据 | 结果 |
|---|---|---|---|---|---|
| R1 · 样本与中位数曲线（环节 B–C） | 现在可检验 | 用 Gaia DR3 服务器端自连接（self-join）重建 C26 的样本（不下载 1.8 GB 的 El-Badry 星表），同样的切割，六个箱的中位数 ṽ | 候选对与逐星的邻居计数，暂估 10–40 MB（先计数；计划 013） | N 在 1421 / 1216 的 ±20% 以内；逐箱与图 8 的比较只作诊断（包括哪个误差公式能复现图 8 的误差棒，N = 368 时约 ±0.013）；总体中位数对 0.489 | **样本不同**：N = 639，C26 为 1421（各 x 箱 3、215、232、109、56、24 对 368、228、144、99、33、28）；A = 0.499，C26 为 0.489 |
| R2 · `gap_err` 与环节 D–E：误差标定正确时 Δχ² 是否仍成立 | 现在可检验 | 同样的 χ² 比较，主要误差为对全体双星整体自助法得到的六个中位数的协方差（预注册规则把稀疏箱合并后为五个，实际运行即如此），C26 的 MAD/√N 作复现栏 | 同上 | 相对似然 ≥ 100 → 牛顿受偏好（与 C26 一致）；在 1/100 与 100 之间 → 不能区分；≤ 1/100 → MOND 受偏好 | **无法区分**：L = 0.49（自助法误差）；用 MAD/√N 时 L = 1.7 × 10⁻⁵；无噪声的牛顿数据也只给出 L = 6.2（没有功效；审稿发现，事后） |
| R3 · 环节 B："纯度高"的稳健性 | 可探索（只作描述） | 逐项关闭 C26 的选择（透视修正、HR 切割、150/200 pc、视差信噪比 > 100、ipd = 0、去群） | 同上 | 无——只作探索，见 README 第 8 节 | 多数变体无法区分（L 0.13–1.2）；14 个中 6 个拟合无效（超过 5% 的自助法样本需要重抽） |
| R4 · B24 的切割 | 可探索（只作描述） | 用 B24 的 250 pc、G < 17 选择的中位数曲线 | 更大的查询（先计数） | 无——只作探索 | 未运行 |

Gaia 档案 2026-11-25 至 12-02 下线，所以在此之前取数并缓存；速度列只在研究的预注册提交之后才取（计划 013）。

**我们的发现（2026-11-16）。** 服务器端重建得到 639 对，不到 C26 的 1421 的一半；与 C26 图 8 的计数相比，不足几乎全在 C26 最低的 x 箱，而 C26 所说的 1 kAU 下限填不满这个箱。按预注册的自助法（bootstrap）误差，检验无法区分牛顿与 MOND（L = 0.49），但独立审稿事后发现检验本身没有功效（power）：无噪声的牛顿数据也只给出 L = 6.2。用 C26 的 MAD/√N 误差时，同样的中位数给出 L = 1.7 × 10⁻⁵（偏向 MOND），所以在我们的样本上结果取决于误差约定——这正是 `gap_err` 的数值形式。独立审稿之后（事后，post hoc）：把 r_sky 下限降到 300 AU，样本（1250 对）与 C26 各箱更接近，而似然比随赫罗图截断与去群相差几个数量级（从偏向牛顿的 196 到偏向 MOND 的 4.5 × 10⁻⁴）。已登记预注册的重新检验（T-034）。数字与网页见研究 README 第 5 节与 `web/index.html`。

**2026-11-18 更新，R5（T-034，预注册）：未运行。** 扩大样本的设计（d < 250 pc，r_sky ≥ 300 AU）在获取任何速度之前先用不含速度的功效门槛（G1b）检查。结果不通过：经过不用速度的截断后，计数只有设计预测的 53%，牛顿真值下预测的似然比为 68（要求 ≥ 100），MOND 真值下为 0.028（要求 ≤ 0.01），所以速度从未获取，R5 不给判决。独立审稿（事后，我们已复核）把不足追溯到去群：C26 的宽松邻居规则在 130 pc 保留 44% 的星对，在 250 pc 只保留 23%；300–1,000 AU 的星对在 150–250 pc 只存活 11%，而且越靠近银道面存活率越低（|b| < 10° 时降到 2%）。定义"邻居"的视差窗口随距离加深，所以这指向偶然邻居而不是真正的三合星（推断，直接检验为 T-043）。这一规则很可能在约 130–150 pc 以外不再适用；已发表的更大样本（Banik et al. 2024，arXiv:2311.03436；El-Badry et al. 2021，arXiv:2101.05282）是对污染建模或估计。已登记偶然邻居率的测量（T-043）。数字见 [`results/r5.json`](https://github.com/sudoghut/astrolab/blob/main/studies/004-m07-wide-binaries-gravity-test/results/r5.json)。

**2026-11-20 更新，偶然邻居（T-043，探索，事后）。** 对 R5 候选星对中母星在 29.9 pc 以外的每颗星，我们计数宽松规则在赤纬平移 2° 的位置周围会找到的邻居：这样的圆内没有真实伴星，所以它的计数就是同样深度下的偶然邻居率。两颗星的平移圆都为空的星对比例与观测存活率非常接近：29.9–130 pc 0.47 对 0.42，130–150 pc 0.24 对 0.22，150–250 pc 0.11 对 0.10，向银道面的下降也一样；每颗星的额外真实邻居（3.8–6.0）与平移计数（4.1–5.7）相当。所以去群损失接近只有偶然邻居时的预期，支持审稿的推断，即损失大部分来自偶然邻居；剩余部分约为 29.9–130 pc 预期存活率的 12%，更远处 6%，是代理差值（不是上限），可能包含真正的三合星与移动星群造成的损失，也可能包含平移偏差与噪声。更大的样本需要一种考虑偶然邻居的去群规则，因而需要新的预注册。数字见研究 README 第 5 节（脚本 [`explore/t043_shifted_neighbours.py`](https://github.com/sudoghut/astrolab/blob/main/studies/004-m07-wide-binaries-gravity-test/explore/t043_shifted_neighbours.py)）。

### 术语表

| 术语 | 含义 |
|---|---|
| MOND | 米尔格罗姆动力学：加速度低于 a0 ≈ 1.2 × 10⁻¹⁰ m/s² 时引力增强 |
| MOND 半径 r_M | √(GM/a0)：双星内部加速度等于 a0 时的间距（1 M☉ 约 7 kAU） |
| 外场效应 | 在 MOND 中，银河系本身的引力限制了双星能得到的增强（此处速度约 20%） |
| ṽ（缩放速度） | 天球平面内的相对速度除以投影间距上的牛顿圆周速度 |
| RUWE | Gaia 的重归一化单位权重误差（renormalised unit weight error）；大于约 1.25 提示有看不见的伴星 |
| 去群（degrouping） | 去掉与另一对共用一颗星、或附近有第三颗星的双星 |
| MAD | 中位数绝对偏差（median absolute deviation）；1.4826 MAD 估计高斯分布的 σ |
| 似然比 | exp(Δχ²/2)：一个模型比另一个模型更能解释数据的倍数 |

### 开放问题

- 表 3 用的是哪个中位数误差公式？图 8 各箱的数目（900，从图上读出）为什么与 N = 1421 不同？
- 在任何合理的变体（R3）中是否出现类似 MOND 的上升？它是台阶式的还是持续上升的（C26 认为系统误差会造成持续上升）？

### 研究进展

- 2026-11-20：T-043（探索，事后）：赤纬平移 2° 的视场表明宽松去群的损失接近只有偶然邻居时的预期，即大部分来自偶然邻居（三个壳层的观测存活率 0.42 / 0.22 / 0.10，仅由偶然邻居预期 0.47 / 0.24 / 0.11）（第三部分更新）。
- 2026-11-18：R5（T-034）：预注册的功效门槛 G1b 不通过（L_N* 68 < 100），未取速度，R5 未运行；审稿（事后）：宽松去群在 250 pc 只保留 23% 的星对（130 pc 为 44%），指向偶然邻居（推断，直接检验为 T-043）；登记 T-043（第三部分更新）。
- 2026-11-16：研究运行（第 A、B 步）与独立审稿：样本不同（639 对），无法区分（L = 0.49）且检验没有功效；事后的 r_sky 300 AU 探索；登记 T-034；补上第三部分的结果。
- 2026-11-14：第一版：第一至三部分，在实现之前写成（T-013，计划 013）。

### 来源

- Cookson 等 2026，arXiv:2602.24035（2026-11-14 读 HTML 版）。
- Cookson 2024，arXiv:2408.13618（2026-11-14 读 PDF），MNRAS 533, 110。
- Banik 等 2024，arXiv:2311.03436；Chae 2023，arXiv:2305.04613；Chae 等 2026，arXiv:2601.21728（摘要层面的背景）。
