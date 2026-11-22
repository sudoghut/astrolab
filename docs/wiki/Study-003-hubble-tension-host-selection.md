# The Hubble tension: does the choice of calibrator galaxies explain the lower JWST values?

[English](#english) · [中文](#中文)

*Paper(s): Riess et al. 2024, "JWST Validates HST Distance Measurements: Selection of Supernova
Subsample Explains Differences in JWST Estimates of Local H0", ApJ (accepted), arXiv:2408.11770;
context: Riess et al. 2022 (R22), ApJL, doi:10.3847/2041-8213/ac5c5b, arXiv:2112.04510; Freedman et
al. 2025 (CCHP), arXiv:2408.06153. Study:
[`studies/003-m02-hubble-tension-distance-ladder`](https://github.com/sudoghut/astrolab/tree/main/studies/003-m02-hubble-tension-distance-ladder) (web page: [online](https://sudoghut.github.io/astrolab/studies/003-m02-hubble-tension-distance-ladder/web/)).
Status: concluded (referee done). Last updated: 2026-11-20 (see the changelog at the end). The source of this page
lives in the main repository at
[`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki); edit it there.*

*中文标题：哈勃张力：校准星系的选择能否解释 JWST 给出的较低数值？状态：已结束（已做独立审稿）。论文：Riess 等 2024，arXiv:2408.11770（ApJ 已接收）；背景：Riess 等 2022（R22），ApJL，doi:10.3847/2041-8213/ac5c5b，arXiv:2112.04510；Freedman 等 2025（CCHP），arXiv:2408.06153。研究：[`studies/003-m02-hubble-tension-distance-ladder`](https://github.com/sudoghut/astrolab/tree/main/studies/003-m02-hubble-tension-distance-ladder)（网页：[在线版](https://sudoghut.github.io/astrolab/studies/003-m02-hubble-tension-distance-ladder/web/)）。最后更新：2026-11-20（见文末"研究进展"）。本页源文件在主仓库的 [`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki) 中，请在那里修改。*

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
1.33 (sys) ± 0.70 (σ_SN, supernova sample) from 24 calibrators in total (HST and JWST data), and, from the JWST TRGB distances to the 11 JWST-observed calibrators alone, 68.81 (with CSP
Hubble-flow SNe) or 69.29 (with Pantheon+ SNe).

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
the abstract; the body never shows which two numbers give it. The "JWST" values of Table 4 are the
paper's recalibration of CCHP's distances, but the paper also compares CCHP's own reported values:
"For the combination of these three methods, F24 reports 70 km/s/Mpc, near the HST-expected value
of ∼70.8 ± 2.3" (§III.2). (Reading the result as "about 2.0 expected from selection plus a small
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
E. CCHP's own reported three-method combined value (2024 version) is near the HST expectation for the
subsample →
F. (our GAP: the inference rule) ⇒ the ~2.5 difference is entirely consistent with sample selection.

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

Provenance: `[stated <arXiv id>: "quote"]`, `[implied]` (standard knowledge, with a source; no
premise in this argument uses it), `[reconstructed]` (our addition; exactly the `GAP` premises). Lean checks that the conclusion
follows (`final`), is not trivial (`final_nontrivial`), that the premises are consistent, that no
single premise suffices, which premises are needed, and whether the stated (`stated_*`) or the
explicit (`explicit_*`) premises suffice. It does not check the physics inside the premises.
H0 values are whole numbers in tenths of km/s/Mpc (73.2 → 732).

#### 2.1 Stage A–B · The selection shift

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `stat_full`: reported full HST sample H0 ≥ 73.2 (a lower bound at the reported central value) | STAT | stated 2408.11770: "is not yet competitive with the HST set (42 SNe Ia and 4 anchors), which yields 73.2 $\pm$ 0.9" | Abstract |
| `stat_sel`: HST Cepheids on the CCHP hosts H0 ≤ 71.2 (an upper bound at the reported central value; both values are deliberately encoded as weak bounds) | STAT | stated 2408.11770: "a corresponding value of H ${}_{0}=71.2$" | §III.2 |
| `stat_drop`: the paper attributes the 2.0 lower value to the choice of hosts and anchor (the paper's stated inference; Lean takes it as given and does not derive the shift from the two numbers) | STAT | stated 2408.11770: "thus 2.0 $\,\rm km\,s^{-1}\,Mpc^{-1}$ lower than the full HST sample—simply due to the choice of SN hosts and anchor" | §III.2 |

```lean
-- stat_full, stat_sel, stat_drop are atoms; they are combined only in gap_rule (2.3)
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
| `stat_f24`: CCHP's own reported three-method combined value is near the HST expectation for the subsample | STAT | stated 2408.11770: "For the combination of these three methods, F24 reports $70$ $\,\rm km\,s^{-1}\,Mpc^{-1}$ , near the HST -expected value of $\sim$ 70.8 $\pm 2.3$" | §III.2 |
| `gap_rule`: the two values + their attributed drop + agreement + within-1σ + CCHP's combined value near → consistent | GAP | reconstructed: our reading of the paper's inference; the paper states only the conclusion, and a textbook definition of consistency within errors (Taylor 1997) covers only the last comparison | — |

```lean
exact p .gap_rule (p .stat_full) (p .stat_sel) (p .stat_drop) (p .stat_agree) (p .stat_resid)
  (p .stat_f24)  -- Abstract, Sec. II.3, III.2-3; GAP
```

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| A real TRGB/JAGB–Cepheid offset of a few percent | `stat_agree`, only to ~0.05–0.10 mag | partly: agreement within those errors |
| The CCHP hosts are an unusual draw | not encoded (the conclusion does not need it) | yes, for the JAGB subset: ~5% of random 8-SN draws are as low (Fig. 6) |
| The full refit gives a smaller host shift than 71.2 suggests | `stat_sel`, `stat_drop` | partly: the paper says its approximation matches its own full fit to ~0.01 mag, which does not show that a full fit on R22's public matrices gives the same shift (R2 checks this) |

#### 2.4 What the Lean check found

1. **`explicit_insufficient` is a consequence of our encoding, not evidence of a defect.** The
   paper states its facts and its conclusion but leaves the inference rule between them implicit;
   we encode that rule as the reconstructed premise `gap_rule`, whose consequent is the
   conclusion itself, so removing it necessarily breaks the chain. The verdict records only that
   the rule is unstated. The informative part is elsewhere: every input the rule needs is stated
   by the paper, including that CCHP's own reported three-method combination (not only the paper's
   recalibration) is near the HST expectation (`stat_f24`). A different reading of "consistent"
   would be a different encoding.
2. **`stated_insufficient`**: for the same reason; the conclusion itself is weak ("entirely
   consistent with").
3. **Every premise is needed** (seven `_needed` theorems): a single route. Context, not a gap: the
   paper's Table 4 recalibration and CCHP's later published values differ somewhat (CCHP's 2025
   Pantheon+ TRGB value 69.29 against Table 4's 70.1); R3 explores this descriptively.
4. **Consistency** (`consistent`) holds trivially: no premise is negative.
5. **Weak points** (ours): the gap above; the 71.2 is an approximation on newer data; "consistent" is backed by
   low-power checks (≈ 0.05–0.10 mag in distance, ≈ 1.5 km/s/Mpc in H0); "consistent with" is not
   "caused by". The study (part 3) does not test the inference rule; it tests the size and
   significance of the host-selection shift (R2) that the rule takes as input, and explores the
   rest descriptively (R3, R4).
6. **Limits**: Lean checks the structure under our encoding, not the astrophysics. In particular the
   atoms are uninterpreted: `gap_rule` asserts that the selection shift, the same-host agreement and
   the within-1σ comparison together imply "consistent"; whether the numbers behind those atoms
   really support them is checked by reading the paper and, for the shift, by the study (R2), not by
   Lean.

### Part 3 · What astrolab can test or explore

**Interactive page:** [open this study's web page](https://sudoghut.github.io/astrolab/studies/003-m02-hubble-tension-distance-ladder/web/) (results, figures and tables;
English/Chinese switch; updated when the site is republished).

| Stage / claim | Can we test or explore it? | How | Data (size) | Decision criterion | Result |
|---|---|---|---|---|---|
| R1 · the SH0ES baseline | testable now | GLS fit of R22's y, L, C | C 46.5 MiB (Git LFS FITS), L 0.66 MB, y 17 kB, lstsq 0.7 kB; total about 47.2 MiB (below the 200 MB study budget) | primary: reproduce the authors' `lstsq_results.txt` (47 parameters); secondary: 73.04 ± 1.01 (tolerances in README §2) | not reproduced against the file (it is a different fit, about 73.3); our fit matches the printed baseline, 73.04, χ²/dof 1.031 |
| R2 · stage A–B: anchor and host shifts | testable now | refit with NGC 4258 only (drop the other anchors' geometric rows), then restrict to the CCHP hosts; shifts in 5 log H0 with exact linear error propagation | same | anchor shift vs R22's −0.0158 mag; host shift: null "no shift", four-outcome table vs −0.0405 mag (our conversion of the paper's 72.54 → 71.2 to 5 log H0; README §2) | anchor shift reproduced (−0.0184, σ 0.0461); host shift −0.073 ± 0.033 mag (−2.2σ) under a post-data host labelling, pre-registered verdict "not evaluable"; R2-RE (2026-11-16): −0.062 ± 0.040 mag (z = −1.53), not detected; see 3.1 |
| R3 · stages C and E: same hosts, Cepheid vs TRGB | explorable (descriptive by default) | joint linear estimator with CCHP's JWST TRGB distances; first reproduce CCHP's TRGB + Pantheon+ value 69.29 (not the paper's recalibrated Table 4 value 70.1) | CCHP Table 3 (paper) | descriptive unless the full CCHP error budget can be mapped before data; see README §8 | CCHP side 69.70 against 69.29 (matched); same hosts: d = +0.010 ± 0.048 mag |
| R4 · is the CCHP choice unusual? | explorable (descriptive) | random 10-host subsets of the 37 hosts, ΔH0 percentile (the paper did an 8-SN version for JAGB, Fig. 6: ~5%) | same | none — exploration only, see README §8 | CCHP choice at the 5.7th percentile (4.7th in Δ/σ) |
| Cross-paper comparison | explorable (descriptive) | pairwise differences for independent pairs only (ladder vs CMB, TDCOSMO vs others) | paper numbers | none — see README §8 | ladder vs CMB-only 5.3σ; TDCOSMO vs ladder −0.4σ; TDCOSMO vs CMB-only 1.3σ |


#### 3.1 Results (after implementation)

The table above keeps the plan as written before implementation; the "Result" column and this
section were added after the run (study README section 5; [web page](https://sudoghut.github.io/astrolab/studies/003-m02-hubble-tension-distance-ladder/web/)).

- **The public matrices reproduce R22's printed fit** (H0 = 73.04, χ²/dof 1.031). The authors'
  `lstsq_results.txt`, our pre-registered primary target, is a different fit (about 73.3).
- **A deviation from the pre-registration.** The columns of the public equation matrix are not in
  the order of R22's host table, so the pre-registered host identification failed and the host
  step (R2), R3 and R4 are, as pre-registered, *not evaluable*. After the first run we relabelled
  the columns using only supernova magnitudes, Cepheid counts and host distances; the CCHP set is
  then unique. Everything below rests on that post-data labelling.
- **The host step (stage A–B).** Restricting the NGC 4258-only ladder to the 10 CCHP hosts moves
  5 log H0 by −0.073 ± 0.033 mag (H0 72.4 → 70.0), −2.2σ with the covariance-propagated error.
  That passes the pre-registered "significant, and the size the paper reports" row, but our shift
  is 1.8 times the paper's −1.3 km/s/Mpc and agrees only within a wide tolerance. Random 10-host
  subsets scatter more than the covariance predicts (the ratio Δ/σ spreads by 1.33), and on that
  empirical scale the CCHP choice is about 1.7σ low (4.7th–5.7th percentile): a low but not
  exceptional draw. With errors inflated by that factor the pre-registered table would read "no
  host-selection effect detected"; the independent referee made this its main point, and a test
  with a host-level random effect is registered for later (T-023).
- **Update 2026-11-16, R2-RE (T-023, pre-registered addendum): no host-selection effect detected.**
  A host-level random effect estimated by restricted maximum likelihood (REML) is 0.077 mag
  (68% interval 0.048–0.105); it removes the excess random-subset scatter (spread of Δ/σ 1.33 → 1.005). With it
  the CCHP host shift is −0.062 ± 0.040 mag (z = −1.53), and the unchanged pre-registered table gives
  "no host-selection effect detected", which is now the headline host-step verdict (the 2026-11-14
  verdict stays recorded). The shift keeps its sign and size (about −2 km/s/Mpc); its significance
  does not survive. The independent referee (post hoc) found no bug but stressed how soft this null is:
  z crosses −2 already at τ ≈ 0.03 mag (the referee's estimate), the evidence for τ > 0 is modest (p ≈ 0.03), τ̂ may rest on a
  few non-CCHP hosts, and the rule was fixed knowing the first result; so the honest summary is a
  shift of about −2 km/s/Mpc at 1.5σ–2.2σ. A leave-one-host-out check is registered (T-032). Numbers: [`results/r2_re.json`](https://github.com/sudoghut/astrolab/blob/main/studies/003-m02-hubble-tension-distance-ladder/results/r2_re.json).
- **Update 2026-11-18, R2-RE-ROB (T-032, pre-registered addendum): the null rests on one host.**
  Leaving out single hosts, the verdict changes only without [N5584](https://sudoghut.github.io/astrolab/atlas/web/?view=sky&focus=NGC%205584&study=003-m02-hubble-tension-distance-ladder) (τ̂ falls to 0.031 and the
  full-data host step gives z' = −2.04, "supports the paper"); the pre-registered label is
  "verdict sensitive to single hosts' influence on τ̂ (N5584)". Under the null of no host-level
  scatter, τ̂ = 0.077 is not clearly unusual (p = 0.07, "undetermined"), but R4's 1.33 spread is
  (p = 0.02). The independent referee (post hoc, verified by us) showed that N5584, one supernova
  (2007af), carries all three signals: over random subsets without it the spread is 1.03 (p = 0.33; an approximate post-hoc check, N5584 staying in the reference fit),
  and without its rows the host step is "no effect" under either covariance (z = −1.63, −1.50). The
  headline stays "no host-selection effect detected"; an explicit, pre-registered treatment of N5584
  is registered (T-039). Numbers: [`results/r2_re_rob.json`](https://github.com/sudoghut/astrolab/blob/main/studies/003-m02-hubble-tension-distance-ladder/results/r2_re_rob.json).
- **Update 2026-11-18, R2-RE-N5584 (T-039, pre-registered addendum): one outlying host, and the null
  holds either way.** Removing N5584 completely (36 hosts) leaves calibrator scatter that the
  covariance C allows (null simulations: p = 0.34 for τ̂, 0.36 for the random-subset spread; label
  "attributable to N5584", read post hoc as consistent with one outlying host, since the null does not
  include choosing the most extreme host; T-042), and the CCHP selection sits at the 8.5th percentile of random 10-host
  subsets. Keeping N5584 but giving every host a heavy-tailed (Student-t, ν = 4) offset down-weights
  only N5584 (weight 0.39) and gives z = −1.38: "no host-selection effect detected" under both
  treatments. The referee (post hoc, verified by us) found that the variational fit overestimates τ
  (exact Student-t likelihood: about 0.055 rather than 0.075) and that z varies by about ±0.3 with the
  method, never reaching −2; that the null does not account for choosing the most extreme host
  (registered as T-042); and that the data cannot tell whether N5584's SN or its Cepheids are off,
  although the literature (an independent Cepheid reanalysis, arXiv:2102.12489) favours the SN.
  Numbers: [`results/r2_re_n5584.json`](https://github.com/sudoghut/astrolab/blob/main/studies/003-m02-hubble-tension-distance-ladder/results/r2_re_n5584.json).
- **Update 2026-11-20, R2-RE-SEL (T-042, pre-registered addendum): consistent with one outlying host, with the
  selection simulated.** The null simulations of the update above did not include how N5584 was found:
  as the most extreme of 37 hosts. This test simulates all 37 hosts under C, drops the most extreme one
  in each simulation by a fixed criterion that picks N5584 on the real data (X: the largest
  leave-one-host-out χ² term; S: the smallest random-subset spread without the host), and only then
  measures the scatter of the other 36. The real 36-host scatter is still ordinary: p = 0.24 for τ̂
  (criterion X; 0.34 without the selection) and p = 0.24 and 0.14 for the random-subset spread (X and
  S; 0.36 without). The pre-registered reading is "the excess calibrator scatter is consistent with one
  outlying host, selection included", so the earlier post-hoc gloss is now a pre-registered result,
  with the caveat that the τ part has no criterion aligned with τ̂. Descriptively, a largest
  leave-one-out term as big as N5584's occurs in 11% of null simulations. The referee (post hoc,
  verified by us) found no bug but pointed out that "consistent" only means the 36 remaining hosts do
  not reject C: the test has little power against host scatter spread over all hosts (with a proxy
  statistic it rejects such scatter in 21–45% of simulations). A statistic chosen afterwards, how much
  the spread drops when the selected host is removed, is rare under C (0.6% of simulations) and less
  rare under diffuse scatter (2–4%): it points towards one outlying host, but no single-outlier model
  was simulated; a pre-registered comparison is registered as T-048. The headline ("no
  host-selection effect detected") is unchanged. Numbers:
  [`results/r2_re_sel.json`](https://github.com/sudoghut/astrolab/blob/main/studies/003-m02-hubble-tension-distance-ladder/results/r2_re_sel.json).
- **Update 2026-11-21, R2-RE-D (T-048, pre-registered addendum): one outlying host and diffuse host
  scatter are not distinguished.** This test compares three pictures of the excess calibrator scatter:
  none (C), host-level scatter spread over all 37 hosts (a random effect with τ = 0.05, 0.077 or 0.105
  mag, R2-RE's estimate and the ends of its 68% interval), and one host, N5584, offset by δ̂ = 0.34 mag
  with everything else under C. Each model is simulated 10,000 times and judged by two statistics: the
  drop D of the random-subset spread when the most extreme host is removed (real data 1.307 → 1.033,
  D = 0.275), and a joint statistic J asking how often a model gives a 37-host spread as high together
  with a post-removal spread as low, calibrated so that it is a valid p value (the raw probability of
  that "quadrant" is not one: for the diffuse models here it is more than ten times smaller). Results: the smallest diffuse model
  (τ = 0.05) is excluded by both statistics (p 0.016 and 0.039), but the two larger ones are not
  excluded by J (p = 0.080 and 0.068); the one-host model is not excluded either (p 0.52 and 0.68), as
  it largely must be, since δ̂ was fitted to these data. The pre-registered reading is "tested diffuse
  model(s) not excluded (τ = 0.077, 0.105)": the data are consistent with either picture and cannot tell
  one outlying host from host scatter of R2-RE's size. "Not excluded" means consistent at the 5% level;
  it is evidence neither for diffuse scatter nor against a single outlier. Density ratios at the observed
  point favour the one-host model by factors of about 2–10, but they are not decisive (the offset is
  fitted, and tail densities depend on the smoothing). The headline ("no host-selection effect
  detected") is unchanged; deciding between the two pictures needs information beyond these spreads,
  such as an independent distance to N5584, or the composite shape test registered as T-055. The
  referee (post hoc, verified) found that the comparison has only about 50% power against its own
  one-host alternative and that V(0.05)'s exclusion by J depends on how J is calibrated: "not excluded"
  is an underpowered null result, not evidence for diffuse scatter. Numbers:
  [`results/r2_re_d.json`](https://github.com/sudoghut/astrolab/blob/main/studies/003-m02-hubble-tension-distance-ladder/results/r2_re_d.json).
- **Update 2026-11-21, R2-RE-G (T-055, pre-registered addendum): a composite shape test is
  underpowered.** The statistic G is the share of the largest host offset in the sum of all 37
  squared host-offset z-scores, so the most extreme host is picked inside the statistic; each
  simulation refits the diffuse scatter τ. Its power against one σ-matched offset host was fixed and
  committed before G was read on the data: 0.49, below the required 0.8, so the pre-registered
  reading is "undetermined (underpowered)". On the data G = 0.305 (N5584 carries 30% of the total),
  which is unusual under Gaussian diffuse scatter of the fitted size (p = 0.016) and typical of one
  offset host; this sub-label is not independent of R2-RE-D, and heavy-tailed diffuse scatter was not
  simulated (independent referee; T-057). The headline is unchanged. Numbers in
  [`results/r2_re_g.json`](https://github.com/sudoghut/astrolab/blob/main/studies/003-m02-hubble-tension-distance-ladder/results/r2_re_g.json).
- **Update 2026-11-22, R2-RE-GT (T-057, pre-registered addendum): heavy tails leave it open.** The
  same statistic G was calibrated against diffuse host scatter whose host effects follow a heavy-tailed
  Student-t distribution (ν = 4, the same variance as R2-RE's random effect), so that one large host
  effect is more common than under a Gaussian. Power against one σ-matched offset host, fixed before
  the data's p value: 0.32, so again "undetermined (underpowered)". On the data p = 0.052, with a
  Monte Carlo interval (0.049–0.056) that contains 0.05: undetermined. Lighter or heavier tails, or a
  smaller or larger scatter, move p across 0.05 (0.021 to 0.092), so whether R2-RE-G's exclusion of
  Gaussian scatter rests on Gaussian tails alone is not decided by these data. A profile over the tail weight
  (R2-RE-GTP, T-060, 2026-11-22) makes this precise: with the test calibrated at each tail weight, diffuse scatter is
  excluded (p ≤ 0.031) for host effects from the Gaussian down to Student-t with 6 degrees of freedom, sits on the 0.05
  boundary at 4 and is not excluded at 3. One value of G cannot tell which tail is right. The headline is
  unchanged. Numbers in
  [`results/r2_re_gt.json`](https://github.com/sudoghut/astrolab/blob/main/studies/003-m02-hubble-tension-distance-ladder/results/r2_re_gt.json).
- **Same hosts, two indicators (stages C and E).** Putting CCHP's JWST TRGB distances in place
  of the Cepheids on the same 10 hosts gives 69.70, close to CCHP's own 69.29; the SH0ES and CCHP
  ladders on those hosts differ by +0.010 ± 0.048 mag (0.3 km/s/Mpc), and no host deviates by
  more than 1.2σ.
- **What this means for the argument.** The inputs of `gap_rule` that this repo can recompute
  hold in R22's data: the selected hosts give a lower H0 than the full sample, and on those hosts
  Cepheids and TRGB agree. The rule itself (that this makes the difference "entirely" a matter of
  selection) is not tested, and the selection effect is at most about 2σ and not significant once a
  host-level random effect is modelled (R2-RE, below).

### Glossary

| Term | Meaning |
|---|---|
| distance ladder | anchors → Cepheids (or TRGB, JAGB) → SNe Ia → Hubble flow |
| anchor | galaxy with a geometric distance (Milky Way parallaxes, NGC 4258 masers, LMC eclipsing binaries) |
| TRGB, JAGB | tip of the red giant branch; J-region asymptotic giant branch (carbon stars) |
| GLS | generalised least squares: q̂ = (LᵀC⁻¹L)⁻¹LᵀC⁻¹y |
| 5 log H0 | the ladder's last parameter; the fit is linear in it, not in H0 |

### Changelog

- 2026-11-22: R2-RE-GTP (T-060): profile of R2-RE-GT over the tail weight and scale; model-limited; calibrated p ≤ 0.031 for ν ≥ 6, 0.05 at ν = 4, 0.08 at ν = 3; part 3 updated; independent referee done.
- 2026-11-22: R2-RE-GT (T-057): G under a Student-t (ν = 4) diffuse null with τ refitted; power 0.32 fixed before the p value, so "undetermined (underpowered)"; p_T,obs = 0.052 (Monte Carlo interval contains 0.05), sub-label "t₄ diffuse undetermined (Monte Carlo)"; part 3 updated. Independent referee done.
- 2026-11-21: R2-RE-G (T-055): composite shape test G with τ refitted, power fixed before reading G: 0.49, so "undetermined (underpowered)"; G = 0.305 at N5584, Gaussian diffuse scatter excluded (p 0.016), not independently of R2-RE-D; referee: no bug, heavy-tailed diffuse null registered as T-057; headline unchanged (part 3 updated).
- 2026-11-21: R2-RE-D (T-048): C, diffuse host scatter V(τ) and a single N5584 offset compared with
  the spread drop D and a calibrated joint statistic J; V(0.05) excluded, V(0.077) and V(0.105) not
  excluded by J (p 0.080, 0.068), the one-host model not excluded (p 0.68, by construction): one outlying
  host and diffuse scatter are not distinguished; referee (post hoc): underpowered (about 50% against
  a single offset host), V(0.05)'s J exclusion not firm, composite shape test registered as T-055;
  headline unchanged (part 3 update).
- 2026-11-20: R2-RE-SEL (T-042): selection-aware null; with the choice of the most extreme host
  simulated, the 36-host scatter is still ordinary (p 0.24, 0.24, 0.14): consistent with one outlying
  host, selection included; referee (post hoc): low power against diffuse scatter, a post-hoc
  spread-drop statistic points towards one host (no single-outlier model simulated), T-048 registered
  (part 3 update).
- 2026-11-18: R2-RE-N5584 (T-039): N5584 removed or down-weighted; the null holds under both;
  referee (post hoc): variational τ biased high, z method spread about ±0.3, selection-aware null
  registered as T-042 (part 3 update).
- 2026-11-18: R2-RE-ROB (T-032): leave-one-host-out and null simulations; the null is sensitive to
  N5584, which (referee, post hoc) carries every signal; T-039 registered (part 3 update).
- 2026-11-16: R2-RE (T-023, plan 021): host-level random effect (REML 0.077 mag); the host step
  becomes "no host-selection effect detected" (z = −1.53), now the headline (part 3 update).
- 2026-11-14: independent referee: the host step's significance depends on the error scale (about 1.7σ with the random-subset scatter, where the pre-registered table would read no effect); R3's per-host distances include each host's own SNe; Lean gloss of `ResidSmall` clarified; follow-up test T-023 registered.
- 2026-11-14: results added after implementation (Part 3 "Result" column and section 3.1): R22's printed fit reproduced; host step −0.073 ± 0.033 mag under a post-data host labelling (pre-registered verdict: not evaluable); same-host Cepheid–TRGB agreement; the CCHP choice is a low but ordinary draw.
- 2026-11-14: first version: parts 1–3, written before implementation (T-012, plan 012); revised after
  review (gate 1: TRGB agreement included; the within-1σ comparison is stated by the paper; Fig. 6;
  GAP `stat_f24`: the recalibrated JWST values versus CCHP's published H0, so `explicit_insufficient`;
  gate 2: reported central value 73.2, and the limits of what Lean shows about `gap_rule`).

---

## 中文

### 第一部分 · 科普详解

#### 1.1 问题与意义

哈勃常数（Hubble constant）H0 是宇宙今天的膨胀速率。它可以直接测量：测量近邻星系的距离与退行速度（recession velocity）；也可以用宇宙微波背景（CMB, cosmic microwave background）在标准模型 ΛCDM（宇宙学常数 Λ 加冷暗物质（cold dark matter））下预测。直接测量给出约 73 km/s/Mpc，预测约 67–68（Planck 2018：67.4 ± 0.5；SPT-3G + ACT + Planck：67.19 ± 0.38）。如果两者都对，标准模型就缺了什么：这就是"哈勃张力"（Hubble tension）。

直接测量靠距离阶梯（distance ladder）。第一级：几个近邻"锚点"（anchor）的几何距离（geometric distance）（银河系造父变星的视差、围绕 NGC 4258 中心黑洞的水脉泽、大麦哲伦云中的食双星）。第二级：造父变星（Cepheid），其周期给出光度，在锚点和曾出现 Ia 型超新星（SN Ia）的星系中都要测量。第三级：平滑哈勃流（Hubble flow）中遥远的 Ia 型超新星，红移给出膨胀速率。

#### 1.2 数据

SH0ES（Supernovae and H0 for the Equation of State of dark energy）团队（Riess 等 2022，"R22"）用了 37 个曾出现 42 颗 Ia 型超新星的星系中的造父变星、三个锚点，以及哈勃流中 277 颗 Ia 型超新星（0.0233 < z < 0.15）。全部数据可以写成一个线性方程组 y = L q：约 3500 个星等 y、方程矩阵（design matrix）L、协方差矩阵（covariance matrix）C 与 47 个未知数 q（每个宿主星系（host galaxy）的距离、造父变星的标定项、超新星光度 M_B，以及最后一个 5 log H0）。R22 公开了 y、L 和 C，本项目可以重新拟合。

芝加哥—卡内基哈勃计划（CCHP, Chicago-Carnegie Hubble Program；Freedman 等 2025）在第二级用别的恒星：红巨星支顶端（TRGB, tip of the red giant branch）与碳星（JAGB, J-region asymptotic giant branch）。它用詹姆斯·韦布空间望远镜（JWST）观测了 10 个超新星宿主星系（11 颗 Ia 型超新星），得到较低的数值：全部 24 颗校准超新星给出 70.39 ± 1.22（统计）± 1.33（系统）± 0.70（σ_SN，超新星样本），24 颗校准超新星包括 HST 与 JWST 的数据；只用 JWST 观测的 11 颗校准超新星的 TRGB 距离给出 68.81（哈勃流用 CSP 超新星）或 69.29（用 Pantheon+ 超新星）。

#### 1.3 逐步讲解

**第 1 步——SH0ES 的基线。** R22 的拟合给出 H0 = 73.04 ± 1.01，加上 67 个分析变体（analysis variants）的离散后为 ± 1.04（式 10）。只用 NGC 4258 一个锚点给出 72.51 ± 1.54。

**第 2 步——2024 年的更新与 CCHP 子样本（subsample）。** Riess 等 2024 重新推导了 HST 全样本（42 颗超新星，现在有 4 个锚点）：73.2 ± 0.9。然后他们问：如果只保留 CCHP 为 JWST 选的 10 个宿主、只用 NGC 4258 作锚点，同样的 HST 造父变星阶梯给出多少？答案是 71.2，"比 HST 全样本低 2.0 km/s/Mpc——仅仅是由于超新星宿主与锚点的选择"。按论文表 4 的各行（73.17 → 72.54 → 71.2；我们的算术）可以拆成锚点约 −0.6、宿主约 −1.3；正文给出锚点约 0.7。71.2 由 M_B = −19.32 ± 0.05 经一个简单的换算公式得到，论文说它与完整拟合相比准确到约 0.01 mag。

**第 3 步——同样的宿主、不同的恒星。** 在 CCHP 的宿主上，JWST 与 HST 对同一批星系的距离一致：JWST 近红外（near-infrared, NIR）TRGB 减 HST 造父变星 0.032 ± 0.056 mag（10 个宿主），JAGB 减造父变星 0.047 ± 0.066 mag（7 个宿主），JWST 减 HST 造父变星 −0.027 ± 0.10 mag（10 个宿主）；"HST 造父变星与 JWST 的距离测量本身良好一致"（图 5 说明）。

**第 4 步——结论。** 论文对每个子样本比较由 JWST 距离得到的 H0（由论文自己重新标定：CCHP 的距离按原值采用，H0 由 Pantheon+ 超新星的平均光度换算）与在同样超新星上由 HST 造父变星预期的数值（表 4），发现"对每个子样本都与预期相容"，在差分不确定度（differential uncertainty，约 1.5–1.8 km/s/Mpc，因两边用同样的超新星而小于子样本的总误差）的 1σ 以内。所以摘要说，CCHP 的 JWST 计划与 HST 全样本约 2.5 km/s/Mpc 的差异"完全与样本选择的差异相容"。"约 2.5"只出现在摘要里，正文没有说明由哪两个数得到。表 4 中的"JWST"数值是论文对 CCHP 距离的重新标定，但论文也比较了 CCHP 自己报告的数值："三种方法合并，F24 给出 70 km/s/Mpc，接近 HST 预期的约 70.8 ± 2.3"（§III.2）。（"约 2.0 由选择预期、剩下一小部分"是我们的概括，不是论文的算术。）

粗估，取自论文（§III.1）：CCHP 的 10 颗超新星、内禀离散（intrinsic dispersion）0.19 mag，给出 H0 的 1σ 不确定度 2.0 km/s/Mpc，所以不同的 10 个宿主子样本之间相差 2 km/s/Mpc 并不奇怪。论文还表明（图 6）随机抽 8 颗超新星时约 5% 与 CCHP 的 JAGB 子样本一样低：不寻常，但在选择能造成的范围内。

#### 1.4 结论与把握程度

论断是刻意的弱措辞：CCHP 与 SH0ES 的差异与样本选择*相容*，而不是被证明由它造成，而且"相容"依靠的是检验力不高的核对（距离一致到约 0.05–0.10 mag，H0 一致到约 1.5 km/s/Mpc）。它可能错在：(a) 71.2（2024 年数据上的近似；子样本误差不含 NGC 4258 的 1.1 km/s/Mpc）在完整拟合中站不住；(b) 同宿主比较掩盖了小样本测不出的、百分之几的真实 TRGB/JAGB 与造父变星的偏差。

### 第二部分 · 论证逻辑

#### 2.0 论证结构

A. 测量：全样本 73.2；SH0ES 阶梯在 CCHP 宿主上 71.2 →
B. 预期：选这些宿主与锚点使 H0 降低约 2 →
C. 同宿主核对：HST 造父变星与 JWST（造父变星、TRGB、JAGB）的距离一致 →
D. 对每个子样本，JWST 的 H0（论文重新标定）与 HST 预期相容（在 1σ 以内）→
E. CCHP 自己报告的三种方法合并值（2024 年版本）接近该子样本的 HST 预期 →
F. （我们补上的 GAP：推理规则）⇒ 约 2.5 的差异完全与样本选择相容。

检查方法：论证写成 Lean 4（[`studies/003-m02-hubble-tension-distance-ladder/argument/Argument.lean`](https://github.com/sudoghut/astrolab/blob/main/studies/003-m02-hubble-tension-distance-ladder/argument/Argument.lean)）。每个前提是 `Field` 的一个构造子（constructor）（不用公理），标注类型与出处性质：

| 标记 | 前提类型 |
|---|---|
| `OBS` | 观测或测量（附表或图） |
| `MOD` | 建模假设 |
| `STAT` | 统计推断（显著性、模型比较） |
| `NUM` | 本项目 `run.py` 重新计算的数值结果 |
| `LIT` | 取自其他文献的结果 |
| `GAP` | 推理需要、但论文和标准知识都没有提供的前提 |

出处性质：`[stated <arXiv 编号>: "引文"]`、`[implied]`（标准知识，注明来源；本论证没有用到）、`[reconstructed]`（我们补上的；恰好是 `GAP` 前提）。Lean 检查：结论能否推出（`final`）、不是恒真（`final_nontrivial`）、前提相容、没有单个前提单独足够、哪些前提必要，以及明说的（`stated_*`）或加上标准知识的（`explicit_*`）前提是否足够。它不检查前提内部的物理。H0 用十分之一 km/s/Mpc 为单位的整数（73.2 → 732）。

#### 2.1 环节 A–B · 选择造成的移动

| 前提（Lean 构造子） | 类型 | 出处性质 | 论文位置 |
|---|---|---|---|
| `stat_full`：HST 全样本报告的 H0 ≥ 73.2（在报告的中心值处取下界） | STAT | stated 2408.11770："is not yet competitive with the HST set (42 SNe Ia and 4 anchors), which yields 73.2 $\pm$ 0.9" | 摘要 |
| `stat_sel`：CCHP 宿主上的 HST 造父变星 H0 ≤ 71.2（在报告的中心值处取上界；两个数值都有意编码为弱的界） | STAT | stated 2408.11770："a corresponding value of H ${}_{0}=71.2$" | §III.2 |
| `stat_drop`：论文把低 2.0 归因于宿主与锚点的选择（论文明说的推断；Lean 把它当作给定，不由两个数推出这一移动） | STAT | stated 2408.11770："thus 2.0 $\,\rm km\,s^{-1}\,Mpc^{-1}$ lower than the full HST sample—simply due to the choice of SN hosts and anchor" | §III.2 |

```lean
-- stat_full, stat_sel, stat_drop are atoms; they are combined only in gap_rule (2.3)
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
| `stat_f24`：CCHP 自己报告的三种方法合并值接近该子样本的 HST 预期 | STAT | stated 2408.11770："For the combination of these three methods, F24 reports $70$ $\,\rm km\,s^{-1}\,Mpc^{-1}$ , near the HST -expected value of $\sim$ 70.8 $\pm 2.3$" | §III.2 |
| `gap_rule`：两个数值 + 论文归因的降低 + 一致 + 1σ 以内 + CCHP 合并值接近 → 相容 | GAP | reconstructed：我们对论文推理的理解；论文只写出结论，教科书中"误差内相容"的定义（Taylor 1997）只涵盖最后一项比较 | — |

```lean
exact p .gap_rule (p .stat_full) (p .stat_sel) (p .stat_drop) (p .stat_agree) (p .stat_resid)
  (p .stat_f24)  -- Abstract, Sec. II.3, III.2-3; GAP
```

**其他解释。**

| 其他解释 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 真实的 TRGB/JAGB 与造父变星之间百分之几的偏差 | `stat_agree`，只到约 0.05–0.10 mag | 部分：在这些误差内一致 |
| CCHP 的宿主是一次不寻常的抽样 | 未编码（结论不需要） | 是，针对 JAGB 子样本：随机 8 颗超新星约 5% 一样低（图 6） |
| 完整重新拟合给出的宿主移动小于 71.2 所示 | `stat_sel`、`stat_drop` | 部分：论文说其近似与它自己的完整拟合相差约 0.01 mag，但这并不说明对 R22 公开矩阵的完整拟合给出同样的移动（R2 检验这一点） |

#### 2.4 Lean 检查的发现

1. **`explicit_insufficient` 是编码方式的结果，不是论证有缺陷的证据。** 论文写出了事实与结论，但两者之间的推理规则没有写出；我们把它编码为补上的前提 `gap_rule`，其结论就是论文的结论本身，所以去掉它链条必然断开。这一结论只记录了"规则没有写出"。有信息量的是另一点：这一规则需要的每个输入论文都写明了，包括 CCHP 自己报告的三种方法合并值（而不只是论文的重新标定）接近 HST 预期（`stat_f24`）。对"相容"的另一种理解会是另一种编码。
2. **`stated_insufficient`**：原因相同；结论本身很弱（"完全相容"）。
3. **每个前提都是必要的**（7 个 `_needed` 定理）：只有一条路径。背景而非缺口：论文表 4 的重新标定与 CCHP 后来发表的数值有些差别（CCHP 2025 年的 Pantheon+ TRGB 为 69.29，表 4 为 70.1）；R3 对此作描述性探索。
4. **相容性**（`consistent`）是平凡成立的：没有否定形式的前提。
5. **薄弱点**（我们的判断）：上述缺口；71.2 是在较新数据上的近似；"相容"依靠检验力不高的核对（距离约 0.05–0.10 mag，H0 约 1.5 km/s/Mpc）；"相容"不等于"由其造成"。研究（第三部分）不检验这一推理规则；它检验规则的输入之一，即宿主选择造成的移动的大小与显著性（R2），其余只作描述性探索（R3、R4）。
6. **局限**：Lean 检查的是我们编码下的结构，不是天体物理。特别是原子没有解释：`gap_rule` 断言选择造成的移动、同宿主的一致与 1σ 以内的比较合起来推出"相容"；这些原子背后的数字是否真的支持它们，由阅读论文以及（对移动量而言）研究的 R2 来检查，而不是 Lean。

### 第三部分 · astrolab 能检验或探索的环节

**交互网页：**[打开本研究的网页](https://sudoghut.github.io/astrolab/studies/003-m02-hubble-tension-distance-ladder/web/)（结果、图与表，可切换中英文；网站重新发布时更新）。

| 环节 / 论断 | 能否检验或探索 | 方法 | 数据（大小） | 判据 | 结果 |
|---|---|---|---|---|---|
| R1 · SH0ES 的基线 | 现在可检验 | 对 R22 的 y、L、C 做广义最小二乘（GLS, generalised least squares）拟合 | C 46.5 MiB（Git LFS 的 FITS），L 0.66 MB，y 17 kB，lstsq 0.7 kB；合计约 47.2 MiB（低于研究预算 200 MB） | 主要：复现作者的 `lstsq_results.txt`（47 个参数）；次要：73.04 ± 1.01（容差见 README 第 2 节） | 对作者文件未复现（那是另一个拟合，约 73.3）；我们的拟合与印出的基线一致，73.04，χ²/自由度 1.031 |
| R2 · 环节 A–B：锚点与宿主的移动 | 现在可检验 | 只用 NGC 4258（去掉其他锚点的几何约束行）重拟，再限于 CCHP 宿主；在 5 log H0 中用精确的线性误差传播（linear error propagation） | 同上 | 锚点移动对 R22 的 −0.0158 mag；宿主移动：零假设（null hypothesis）"无移动"，四种结果的判定表，对 −0.0405 mag（我们把该文的 72.54 → 71.2 换算到 5 log H0；README 第 2 节） | 锚点移动复现（−0.0184，σ 0.0461）；宿主移动在数据之后的宿主标注下为 −0.073 ± 0.033 mag（−2.2σ），预注册判定为"不可评估"；R2-RE（2026-11-16）：−0.062 ± 0.040 mag（z = −1.53），未检出；见 3.1 |
| R3 · 环节 C 与 E：同宿主上造父变星对 TRGB | 可探索（默认只作描述） | 与 CCHP 的 JWST TRGB 距离做联合线性估计；先复现 CCHP 的 TRGB + Pantheon+ 数值 69.29（不是论文重新标定的表 4 数值 70.1） | CCHP 表 3（论文） | 只有在取数前能写出 CCHP 完整的误差预算时才作检验，否则只作描述；见 README 第 8 节 | CCHP 一侧 69.70 对 69.29（一致）；同宿主 d = +0.010 ± 0.048 mag |
| R4 · CCHP 的选择是否不寻常 | 可探索（只作描述） | 37 个宿主中随机 10 个的子样本，ΔH0 的百分位（percentile）（论文对 JAGB 做过 8 颗超新星的版本，图 6：约 5%） | 同上 | 无——只作探索，见 README 第 8 节 | CCHP 的选择位于第 5.7 百分位（按 Δ/σ 为第 4.7） |
| 跨论文比较 | 可探索（只作描述） | 只对近似独立的组合给出两两之差（距离阶梯对 CMB、TDCOSMO 对其他） | 论文数字 | 无——见 README 第 8 节 | 距离阶梯对只用 CMB 5.3σ；TDCOSMO 对距离阶梯 −0.4σ；TDCOSMO 对只用 CMB 1.3σ |


#### 3.1 结果（实现之后）

上表保留实现之前写下的计划；"结果"一栏与本节在运行之后加入（研究 README 第 5 节；[网页](https://sudoghut.github.io/astrolab/studies/003-m02-hubble-tension-distance-ladder/web/)）。

- **公开矩阵复现了 R22 印出的拟合**（H0 = 73.04，χ²/自由度 1.031）。我们预注册的主要目标，即作者的 `lstsq_results.txt`，是另一个拟合（约 73.3）。
- **偏离预注册。** 公开的方程矩阵的列不是按 R22 宿主表的顺序排列的，所以预注册的宿主识别失败，宿主一步（R2）、R3 与 R4 按预注册为*不可评估*。第一次运行之后，我们只用超新星星等、造父变星数目与宿主距离重新标注各列；这样 CCHP 宿主集合是唯一确定的。下面的结果都依赖这一数据之后的标注。
- **宿主一步（环节 A–B）。** 把只用 NGC 4258 的阶梯限于 10 个 CCHP 宿主，5 log H0 移动 −0.073 ± 0.033 mag（H0 72.4 → 70.0），按协方差传播的误差为 −2.2σ。这符合预注册判定表中"显著，且大小与该文一致"一行，但我们的移动是论文的 −1.3 km/s/Mpc 的 1.8 倍，只在宽的容差内一致。随机 10 宿主子样本的离散大于协方差的预期（Δ/σ 的离散为 1.33），在这一经验尺度上 CCHP 的选择约低 1.7σ（第 4.7–5.7 百分位）：偏低，但不算异常。按这一倍数膨胀误差后，预注册判定表会给出"未检测到宿主选择的效应"；独立审稿把这一点列为最主要的意见，带逐宿主随机效应（random effect）的检验已登记待做（T-023）。
- **2026-11-20 更新，R2-RE-SEL（T-042，预注册附录）：把选择放进模拟后，仍与一个离群宿主相容。** 上一条更新中的零假设模拟没有包含 [N5584](https://sudoghut.github.io/astrolab/atlas/web/?view=sky&focus=NGC%205584&study=003-m02-hubble-tension-distance-ladder) 是怎样被找出来的：它是 37 个宿主中最极端的一个。本检验在 C 下模拟全部 37 个宿主，每次按一个固定准则去掉最极端的宿主（这个准则在真实数据上选出 N5584；X：留一宿主 χ² 项最大；S：不含该宿主的随机子样本离散最小），然后才测量其余 36 个宿主的离散。真实的 36 宿主离散仍是普通的：τ̂ 的 p = 0.24（准则 X；不考虑选择时 0.34），随机子样本离散的 p = 0.24 与 0.14（X 与 S；不考虑选择时 0.36）。预注册解读为"计入选择后，多出的校准离散与一个离群宿主相容"，所以先前的事后说法现在是预注册的结果，附一条限定：τ 部分没有与 τ̂ 对应的准则。描述性地，零假设模拟中有 11% 的最大留一项与 N5584 的一样大。独立审稿（事后，我们已复核）没有发现错误，但指出"相符"只表示其余 36 个宿主不拒绝 C：这个检验对分散在所有宿主上的离散功效很低（用代理统计量，只在 21–45% 的模拟中拒绝）。一个事后选择的统计量，即去掉选出的宿主时离散下降多少，在 C 下少见（0.6% 的模拟），在分散离散下没那么少见（2–4%）：它指向一个离群宿主，但没有模拟单个离群者的模型；预注册的比较登记为 T-048。标题判定（"未检出宿主选择效应"）不变。数字见 [`results/r2_re_sel.json`](https://github.com/sudoghut/astrolab/blob/main/studies/003-m02-hubble-tension-distance-ladder/results/r2_re_sel.json)。
- **2026-11-21 更新，R2-RE-D（T-048，预注册附录）：无法区分一个离群宿主与分散的宿主离散。** 本检验比较对多出的定标星离散的三种图景：没有额外离散（C）、分布在全部 37 个宿主上的宿主层级离散（随机效应 τ = 0.05、0.077 或 0.105 mag，即 R2-RE 的估计值及其 68% 区间两端），以及只有一个宿主 N5584 偏移 δ̂ = 0.34 mag、其余都按 C。每个模型模拟 10,000 次，用两个统计量判断：去掉最极端宿主时随机子样本离散的下降量 D（真实数据 1.307 → 1.033，D = 0.275），以及联合统计量 J：模型多常给出同样高的 37 宿主离散、同时去掉一个宿主后同样低的离散；J 经过校准，是有效的 p 值（这个"象限"的原始概率不是 p 值，对这里的分散模型小了十倍以上）。结果：最小的分散模型（τ = 0.05）被两个统计量都排除（p 0.016 与 0.039），但两个较大的分散模型没有被 J 排除（p = 0.080 与 0.068）；单宿主模型也没有被排除（p 0.52 与 0.68），这在很大程度上是必然的，因为 δ̂ 是在这些数据上拟合的。预注册解读为"所检验的分散模型未被排除（τ = 0.077、0.105）"：数据与两种图景都相容，不能区分一个离群宿主与 R2-RE 大小的宿主离散。"未排除"指在 5% 水平上相容，既不是支持分散离散的证据，也不是反对单个离群者的证据。观测点处的密度比偏向单宿主模型约 2–10 倍，但不起决定作用（偏移是拟合的，尾部密度取决于平滑程度）。标题判定（"未检出宿主选择效应"）不变；要在两种图景间作出判断，需要这些离散之外的信息，例如 N5584 的独立距离，或登记为 T-055 的复合形状检验。独立审稿（事后，已复核）发现这一比较对它自己的单宿主备择只有约 50% 的功效，J 对 V(0.05) 的排除取决于 J 的校准方式："未排除"是功效不足的零结果，不是支持分散离散的证据。数字见 [`results/r2_re_d.json`](https://github.com/sudoghut/astrolab/blob/main/studies/003-m02-hubble-tension-distance-ladder/results/r2_re_d.json)。
- **2026-11-21 更新，R2-RE-G（T-055，预注册附录）：复合形状检验功效不足。** 统计量 G 是最大的宿主偏移在全部 37 个宿主偏移 z 值平方和中所占的比例，所以最极端的宿主是在统计量内部挑出的；每次模拟都重新拟合分散离散 τ。它对一个 σ 匹配的偏移宿主的功效在读取数据上的 G 之前就已固定并提交：0.49，低于要求的 0.8，所以预注册解读为"无法判定（功效不足）"。数据上 G = 0.305（N5584 占总和的 30%），在拟合大小的高斯分散离散下不寻常（p = 0.016），在一个偏移宿主下则很典型；这个子标签不独立于 R2-RE-D，而且没有模拟重尾的分散离散（独立审稿；T-057）。标题判定不变。数字见 [`results/r2_re_g.json`](https://github.com/sudoghut/astrolab/blob/main/studies/003-m02-hubble-tension-distance-ladder/results/r2_re_g.json)。
- **2026-11-22 更新，R2-RE-GT（T-057，预注册附录）：重尾下仍未判定。** 同一统计量 G 在宿主效应服从重尾 Student-t 分布（ν = 4，方差与 R2-RE 的随机效应相同）的分散宿主离散下校准，这样一个大的宿主效应比高斯下更常见。对一个 σ 匹配的偏移宿主的功效在计算数据的 p 值之前固定：0.32，所以仍是"无法判定（功效不足）"。数据上 p = 0.052，其蒙特卡洛区间（0.049–0.056）包含 0.05：无法判定。更轻或更重的尾部、更小或更大的离散都会让 p 跨过 0.05（0.021 到 0.092），所以 R2-RE-G 对高斯离散的排除是否只依赖高斯尾部，这些数据没有判定。在尾部权重上作的剖面（R2-RE-GTP，T-060，2026-11-22）把这一点说得更具体：在每个尾部权重下分别校准检验，宿主效应从高斯到 6 个自由度的 Student-t，分散离散都被排除（p ≤ 0.031），4 个自由度时落在 0.05 的边界上，3 个自由度时不排除。一个 G 值无法判断哪种尾部是对的。标题判定不变。数字见 [`results/r2_re_gt.json`](https://github.com/sudoghut/astrolab/blob/main/studies/003-m02-hubble-tension-distance-ladder/results/r2_re_gt.json)。
- **同样的宿主、两种指示器（环节 C 与 E）。** 在同样 10 个宿主上用 CCHP 的 JWST TRGB 距离代替造父变星，得到 69.70，与 CCHP 自己的 69.29 接近；这些宿主上 SH0ES 与 CCHP 两个阶梯相差 +0.010 ± 0.048 mag（0.3 km/s/Mpc），没有宿主偏离超过 1.2σ。
- **对论证的意义。** 本项目能重算的 `gap_rule` 输入在 R22 的数据中成立：选出的宿主给出比全样本低的 H0，而在这些宿主上造父变星与 TRGB 一致。规则本身（因此差异"完全"是选择造成的）没有被检验，而选择效应至多约 2σ，加入宿主级随机效应后不显著（R2-RE，下一条）。
- **2026-11-16 更新，R2-RE（T-023，预注册附录）：未检出宿主选择效应。** 用限制最大似然（REML, restricted maximum likelihood）估计的宿主级随机效应（random effect）为 0.077 mag（68% 区间 0.048–0.105），它消除了随机子样本多出来的离散（Δ/σ 的离散 1.33 → 1.005）。计入它之后，CCHP 宿主一步为 −0.062 ± 0.040 mag（z = −1.53），不变的预注册判定表给出"未检出宿主选择效应"，现在是宿主一步的标题判定（2026-11-14 的判定保留记录）。移动的方向与大小（约 −2 km/s/Mpc）不变，不成立的是显著性。独立审稿（事后）没有发现错误，但强调这个"未检出"很软：τ ≈ 0.03 mag 时 z 就越过 −2（审稿的估计），τ > 0 的证据不强（p ≈ 0.03），τ̂ 可能由少数非 CCHP 宿主决定，而且规则是在已知第一次结果后定的；所以如实的概括是约 −2 km/s/Mpc 的移动，显著性 1.5σ–2.2σ。逐一剔除宿主的检验已登记（T-032）。数字见 [`results/r2_re.json`](https://github.com/sudoghut/astrolab/blob/main/studies/003-m02-hubble-tension-distance-ladder/results/r2_re.json)。
- **2026-11-18 更新，R2-RE-ROB（T-032，预注册附录）：零结果依赖一个宿主。** 逐一剔除宿主时，只有去掉 N5584 时判定改变（τ̂ 降到 0.031，用全部数据的宿主一步给出 z' = −2.04，"支持论文"）；预注册标签为"判定对单个宿主对 τ̂ 的影响敏感（N5584）"。在没有宿主层面离散的零假设下，τ̂ = 0.077 并不明显不寻常（p = 0.07，"无法判定"），但 R4 的 1.33 离散不寻常（p = 0.02）。独立审稿（事后，我们已复核）表明一颗超新星（N5584 中的 2007af）承载了全部三个信号：在不含它的随机子样本上离散为 1.03（p = 0.33；近似的事后检查，N5584 仍在参照拟合中），去掉它的行后宿主一步在两种协方差下都是"无效应"（z = −1.63、−1.50）。标题判定仍为"未检出宿主选择效应"；对 N5584 的明确、预注册处理已登记（T-039）。数字见 [`results/r2_re_rob.json`](https://github.com/sudoghut/astrolab/blob/main/studies/003-m02-hubble-tension-distance-ladder/results/r2_re_rob.json)。
- **2026-11-18 更新，R2-RE-N5584（T-039，预注册附录）：一个离群宿主，零结果两种处理下都成立。** 完全去掉 N5584（36 个宿主）后，定标星的离散在协方差 C 允许的范围内（零假设模拟：τ̂ 的 p = 0.34，随机子样本离散的 p = 0.36；标签"可归因于 N5584"；由于零假设没有包含选出最极端宿主这一步，事后读作"与一个离群宿主相容"，T-042），CCHP 的选择位于随机 10 宿主子样本的第 8.5 百分位。保留 N5584、给每个宿主重尾（Student-t，ν = 4）偏移时，只有 N5584 被降权（权重 0.39），z = −1.38：两种处理下都是"未检出宿主选择效应"。独立审稿（事后，我们已复核）发现：变分拟合高估了 τ（精确 Student-t 似然约 0.055 而非 0.075），z 随方法变化约 ±0.3，但从未达到 −2；零假设没有计入"选出最极端宿主"这一步（登记 T-042）；数据不能说明是 N5584 的超新星还是造父变星有偏，但文献（独立的造父变星再分析，arXiv:2102.12489）倾向于超新星一侧。数字见 [`results/r2_re_n5584.json`](https://github.com/sudoghut/astrolab/blob/main/studies/003-m02-hubble-tension-distance-ladder/results/r2_re_n5584.json)。

### 术语表

| 术语 | 含义 |
|---|---|
| 距离阶梯 | 锚点 → 造父变星（或 TRGB、JAGB）→ Ia 型超新星 → 哈勃流 |
| 锚点 | 有几何距离的星系（银河系视差、NGC 4258 的脉泽、LMC 的食双星） |
| TRGB、JAGB | 红巨星支顶端（tip of the red giant branch）；J 波段渐近巨星支（J-region asymptotic giant branch，碳星） |
| GLS（广义最小二乘） | q̂ = (LᵀC⁻¹L)⁻¹LᵀC⁻¹y |
| 5 log H0 | 阶梯的最后一个参数；拟合对它是线性的，对 H0 不是 |

### 研究进展

- 2026-11-22：R2-RE-GTP（T-060）：R2-RE-GT 在尾部权重与尺度上的剖面；受模型限制；校准 p 在 ν ≥ 6 时 ≤ 0.031，ν = 4 时 0.05，ν = 3 时 0.08；更新第三部分；独立审稿已做。
- 2026-11-22：R2-RE-GT（T-057）：G 在 Student-t（ν = 4）分散零假设下校准，重新拟合 τ；功效 0.32 在 p 值之前固定，所以"无法判定（功效不足）"；p_T,obs = 0.052（蒙特卡洛区间包含 0.05），子标签"t₄ 分散：无法判定（蒙特卡洛）"；更新第三部分。独立审稿已做。
- 2026-11-21：R2-RE-G（T-055）：重新拟合 τ 的复合形状检验 G，功效在读取 G 前固定：0.49，所以"无法判定（功效不足）"；G = 0.305（N5584），高斯分散离散被排除（p 0.016），但不独立于 R2-RE-D；审稿：没有错误，重尾分散零假设登记为 T-057；标题判定不变（第三部分更新）。
- 2026-11-21：R2-RE-D（T-048）：用离散下降量 D 与校准后的联合统计量 J 比较 C、分散的宿主离散 V(τ) 与单独 N5584 偏移；V(0.05) 被排除，V(0.077) 与 V(0.105) 未被 J 排除（p 0.080、0.068），单宿主模型未被排除（p 0.68，构造使然）：无法区分一个离群宿主与分散离散；审稿（事后）：功效不足（对单个偏移宿主约 50%），J 对 V(0.05) 的排除不牢靠，登记复合形状检验 T-055；标题判定不变（第三部分更新）。
- 2026-11-20：R2-RE-SEL（T-042）：考虑选择的零假设；把选出最极端宿主这一步放进模拟后，36 个宿主的离散仍是普通的（p 0.24、0.24、0.14）：计入选择后与一个离群宿主相容；审稿（事后）：对分散离散功效低，事后的离散下降统计量指向一个宿主（未模拟单个离群者的模型），登记 T-048（第三部分更新）。
- 2026-11-18：R2-RE-N5584（T-039）：去掉或降权 N5584，零结果都成立；审稿（事后）：变分 τ 偏高，z 的方法离散约 ±0.3，考虑选择的零假设登记为 T-042（第三部分更新）。
- 2026-11-18：R2-RE-ROB（T-032）：逐一剔除宿主与零假设模拟；零结果对 N5584 敏感，而（审稿，事后）它承载了全部信号；登记 T-039（第三部分更新）。
- 2026-11-16：R2-RE（T-023，计划 021）：宿主级随机效应（REML，0.077 mag）；宿主一步变为"未检出宿主选择效应"（z = −1.53），成为标题判定（第三部分更新）。
- 2026-11-14：独立审稿：宿主一步的显著性取决于误差尺度（按随机子样本的离散约 1.7σ，此时预注册判定表会给出没有效应）；R3 的逐宿主距离含本宿主的超新星；澄清 `ResidSmall` 的 Lean 说明；登记后续检验 T-023。
- 2026-11-14：实现之后加入结果（第三部分"结果"一栏与 3.1 节）：复现 R22 印出的拟合；在数据之后的宿主标注下宿主移动为 −0.073 ± 0.033 mag（预注册判定：不可评估）；同宿主上造父变星与 TRGB 一致；CCHP 的选择偏低但不异常。
- 2026-11-14：第一版：第一至三部分，在实现之前写成（T-012，计划 012）；按审查修订（闸门 1：补上 TRGB 的一致性；1σ 以内的比较论文自己写明；图 6；GAP `stat_f24`：重新标定的 JWST 数值与 CCHP 发表的 H0，因而 `explicit_insufficient`；闸门 2：报告的中心值 73.2，以及 Lean 对 `gap_rule` 能说明什么）。
