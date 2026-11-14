# Dormant black holes in Gaia astrometric orbits

[English](#english) · [中文](#中文)

*Paper(s): El-Badry et al. 2023a, MNRAS 518, 1057, arXiv:2209.06833 (Gaia BH1); El-Badry et al. 2023b,
MNRAS 521, 4323, arXiv:2302.07880 (Gaia BH2); Gaia Collaboration, Panuzzo et al. 2024, A&A 686, L2,
arXiv:2404.10486 (Gaia BH3); El-Badry et al. 2024, OJAp 7, arXiv:2405.00089 (neutron-star candidates).
Study: [`studies/001-m04-gaia-dormant-black-holes`](https://github.com/sudoghut/astrolab/tree/main/studies/001-m04-gaia-dormant-black-holes).
Status: reproduced (Gaia DR3). Last updated: 2026-11-14 (see the changelog at the end). The source of this
page lives in the main repository at [`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki); edit it there.*

*中文标题：Gaia 天体测量轨道中的休眠黑洞。状态：已复现（Gaia DR3）。论文：El-Badry 等 2023a, MNRAS 518, 1057, arXiv:2209.06833（Gaia BH1）；El-Badry 等 2023b, MNRAS 521, 4323, arXiv:2302.07880（Gaia BH2）；Gaia 合作组 Panuzzo 等 2024, A&A 686, L2, arXiv:2404.10486（Gaia BH3）；El-Badry 等 2024, OJAp 7, arXiv:2405.00089（中子星候选）。研究：[`studies/001-m04-gaia-dormant-black-holes`](https://github.com/sudoghut/astrolab/tree/main/studies/001-m04-gaia-dormant-black-holes)。最后更新：2026-11-14（见文末"研究进展"）。本页源文件在主仓库的 [`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki) 中，请在那里修改。*

---

## English

### Part 1 · The papers in plain language

#### 1.1 The question and why it matters

Stars much heavier than the Sun end their lives as black holes. The Milky Way should therefore contain
about a hundred million stellar-mass black holes. Almost all the ones we know, however, were found
because they are *feeding*: a companion star spills gas onto the black hole, the gas heats up and glows
in X-rays. Feeding black holes are rare and probably not typical. A black hole that sits quietly next
to an ordinary star, with nothing falling onto it, emits nothing at all. Such "dormant" black holes
should be far more common, but they can only be found by their gravity: the visible star moves in an
orbit around something that cannot be seen.

Before 2022, every claimed dormant black hole around a normal star had later been explained another
way (most often a second, fainter star that had been overlooked). The question these papers answer is:
can a star's own motion, measured precisely enough, prove that its invisible partner is a black hole?

#### 1.2 The data

The European Space Agency's Gaia satellite measures the positions of about two billion stars, again and
again, for years. A star in a binary does not move in a straight line across the sky; it traces a small
ellipse around the binary's centre of mass. Gaia's third data release (DR3, June 2022) included, for the
first time, fitted orbits for about 440,000 binaries (the "non-single-star" or NSS catalogue). For an
*astrometric* orbit the fit gives the size of the star's ellipse on the sky (the semi-major axis a0, in
milliarcseconds), the period P, the shape (eccentricity e) and the orientation, through four numbers
called the Thiele-Innes constants. With the star's distance (from its parallax ϖ) the angular size
becomes a physical size in astronomical units.

From the orbit's size and period alone, Kepler's third law gives the *astrometric mass function*,
f_M = (a0/ϖ)³ / P², in solar masses (with P in years). If the companion is dark, f_M equals
M2³ / (M1 + M2)², where M1 is the visible star's mass and M2 the companion's. With M1 known from the
star's colour and brightness, M2 follows.

The papers then added ground-based spectroscopy. A spectrograph measures the star's radial velocity
(RV), its speed towards or away from us, through the Doppler shift of its absorption lines. RVs give an
independent view of the same orbit. Spectra also show whether a second star contributes light: a second
star would add its own lines, or dilute the visible star's lines.

#### 1.3 Step by step: how the authors got from data to conclusion

##### 1.3a Gaia BH1 (El-Badry et al. 2023a)

1. **A candidate from Gaia.** Among DR3 astrometric orbits, one Sun-like star at 480 pc (G = 13.8 mag)
   had an orbit of about 186 days, with a0 = 3.00 ± 0.22 mas, implying a dark companion of about 10 Msun.
   It only just passed Gaia's quality thresholds, and Gaia's observations covered only about half of the
   orbit, so the solution needed checking.
2. **RV follow-up.** The authors took 39 spectra over four months with six spectrographs (MagE, GMOS,
   X-shooter, HIRES, FEROS, ESI), plus two archival LAMOST spectra. The RVs "span most of the orbit's
   predicted dynamic range and broadly validate the Gaia solution". Even ignoring Gaia entirely, the RVs
   alone require a companion of at least about 4 Msun.
3. **Masses.** The visible star's mass, M1 = 0.93 ± 0.05 Msun, comes from fitting its spectral energy
   distribution (SED) and comparing with stellar evolution models. A joint fit of the Gaia astrometry
   and the RVs gives P = 185.59 ± 0.05 d, e = 0.451 ± 0.005 and **M2 = 9.62 ± 0.18 Msun**. Gaia's
   astrometry alone gives 12.8 ± 2.0 Msun, consistent at the 1.6σ level.
4. **No light from the companion.** The spectra show "no evidence of another luminous star"; a
   companion contributing pure continuum light could provide at most about 10% of the light, and a
   companion with its own lines more than about 3% would have been detected. The authors note that "any
   normal star with a mass exceeding ≈0.4 M⊙ would easily be detected in the spectrum". A 10 Msun star
   would be hundreds of times brighter than the whole system.
5. **What else could it be?** Not a normal star (too faint). Not a white dwarf or neutron star (far too
   heavy). Not a group of compact objects: "Scenarios involving more than two objects inside the G star's
   orbit are difficult to assemble and unlikely to be dynamically stable." Two compact objects without a
   black hole cannot reach 10 Msun. What remains is a single black hole, or a pair containing one.

*Back of the envelope.* a0 = 3.0 mas at ϖ = 2.08 mas gives a1 ≈ 1.44 au; P = 0.509 yr gives
f_M ≈ 1.44³/0.509² ≈ 11 Msun. With M1 ≈ 1 Msun, M2³ = 11 (1 + M2)² gives M2 ≈ 13 Msun: of order ten
solar masses, in an object that gives no light.

##### 1.3b Gaia BH2 (El-Badry et al. 2023b)

1. **A candidate with an AstroSpectroSB1 solution.** A red giant (G = 12.3) at 1.16 kpc had a joint
   astrometric and spectroscopic Gaia solution with P = 1352 ± 45 d and an astrometric mass function of
   6.7 ± 0.5 Msun, implying M2 ≈ 8.4 Msun for M1 = 1 Msun.
2. **RV follow-up.** 48 RVs (43 FEROS, 5 UVES) over seven months. "The follow-up RVs are fully
   consistent with the Gaia-only solution." The joint fit gives P = 1276.7 ± 0.6 d and e = 0.518; the
   Gaia-only period differs at the 1.6σ level, which the authors attribute to how the Gaia pipeline
   links the spectroscopic and astrometric parts of the orbit.
3. **Masses.** M1 = 1.07 ± 0.19 Msun from the giant's temperature and radius with stellar tracks;
   **M2 = 8.9 ± 0.3 Msun** from the joint fit, at an inclination of about 35°.
4. **No light.** The deepest absorption lines reach about 2% of the continuum, so a companion giving
   more than about 2–3% of the light at 4000 Å would have diluted them. The UV is faint. "A 9Msun
   main-sequence star would outshine the giant at all wavelengths."
5. **What else?** As for BH1: a compact-object cluster "would be difficult to assemble and would rapidly
   become unstable". The conclusion is explicitly conditional: "if the Gaia astrometric solution is
   correct, the companion must be a BH, or a close binary containing a BH". The authors argue that a
   wrong Gaia solution is very unlikely because the independent RVs match its predictions.

##### 1.3c Gaia BH3 (Gaia Collaboration, Panuzzo et al. 2024)

Found during validation of pre-release Gaia DR4 data (a preliminary pipeline run called NSS 4.1): an
old, metal-poor giant with M1 = 0.76 ± 0.05 Msun in an 11.6-year orbit (P = 4253 ± 99 d, e = 0.73).
Gaia's own RVs "independently validate the astrometric orbit". The combined solution gives a mass
function of 31.2 ± 0.8 Msun and **M2 = 32.70 ± 0.82 Msun**. The spectra "do not show any sign of the
presence of a second component", and the observed luminosity is "too low by several orders of magnitude"
for a main-sequence companion; the mass is "too large for one neutron star or two neutron stars in a
close orbit". The authors conclude that "most probably" it is a single black hole, the most massive
stellar black hole known in the Galaxy, while noting that an inner pair of black holes cannot be excluded.

##### 1.3d Neutron-star candidates (El-Badry et al. 2024)

The same method, pushed to lower companion masses: 21 Sun-like stars in wide orbits (P ≈ 190–1050 d)
whose companions weigh 1.26–1.90 Msun, too much for any normal star or close pair of stars given the
light limits, confirmed with about 300 RVs. The simplest interpretation is neutron stars, though
ultramassive white dwarfs and tight white-dwarf pairs cannot be fully excluded. For this repository the
21 objects matter as *known positive controls*: a screen for dark companions should recover them.

#### 1.4 What they conclude, and how sure they are

- BH1 and BH2: dark companions of 9.6 and 8.9 Msun that contain at least one black hole; the simplest
  reading is a single black hole. The papers are confident about the mass and the darkness; the
  identification as a black hole rests on (a) the orbit being real, (b) no other dark object of that
  mass being plausible.
- BH3: a 33 Msun dark companion, "most probably" a single black hole, from preliminary data.
- For the authors to be wrong, one of these would have to fail: the Gaia orbit is spurious (ruled out for
  BH1 by the RVs; argued very unlikely for BH2; for BH3 Gaia's own RVs); the visible star's mass is badly
  off (it changes M2 only modestly); or the dark mass is a stable group of several neutron stars or white
  dwarfs (argued implausible, not excluded by data).

### Part 2 · The logic of the argument

#### 2.0 Map of the argument

For each system i (1 = BH1, 2 = BH2, 3 = BH3) the same four-link chain:

A. the follow-up RVs agree with the Gaia orbit → the orbit is real;
B. a real orbit and its fitted mass → the companion weighs at least 5 Msun;
C. no light from a companion, with that mass → the mass is not in luminous stars;
D. at most two objects, and the maximum neutron-star mass → the companion contains a black hole.

Conclusion: BH1 ∧ BH2 ∧ BH3 (each companion contains at least one black hole).

How we check it: the argument is written in Lean 4
([`studies/001-m04-gaia-dormant-black-holes/argument/Argument.lean`](https://github.com/sudoghut/astrolab/blob/main/studies/001-m04-gaia-dormant-black-holes/argument/Argument.lean)).
Each premise is one constructor of `Field` (no axioms), labelled with its kind and its provenance:

| Tag | Kind of premise |
|---|---|
| `OBS` | observation or measurement (with table / figure) |
| `MOD` | modelling assumption |
| `STAT` | statistical inference (significance, model comparison) |
| `NUM` | numerical result, re-computed by this repo's `run.py` |
| `LIT` | result taken from other literature |
| `GAP` | premise the inference needs that neither the paper nor standard knowledge supplies |

Provenance: `[stated <arXiv id>: "quote"]` (the paper says it, quoted), `[implied]` (standard knowledge
the paper relies on without writing it out, with a source), `[reconstructed]` (our addition; exactly the
`GAP` premises).

What Lean checks: that the conclusion follows from these premises (`final`) and is not trivially true
(`final_nontrivial`); that the premises can hold together (`consistent`); that no single premise gives the
conclusion alone (`alone_insufficient`); for each premise, whether it is needed (a countermodel without
it) or redundant; whether the premises the papers actually state are enough (`stated_*`); and whether they
are enough once standard knowledge is added (`explicit_*`). What Lean does not check: the physics inside
each premise.

Masses are in tenths of a solar mass (whole numbers), so "at least 5 Msun" is `mass ≥ 50`.

#### 2.1 Stage A · The orbit is real

**Overview.** Every mass in the argument comes from the orbit. If Gaia's orbital solution were an
artefact, nothing else would follow. The papers settle this with independent radial velocities.

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `obs_rv1`: BH1 RVs agree with the Gaia orbit | OBS | stated 2209.06833: "The follow-up RVs span most of the orbit's predicted dynamic range and broadly validate the Gaia solution" | §3.2 |
| `mod_rv1`: agreeing RVs → orbit real | MOD | stated 2209.06833: "a catastrophic problem with the astrometric solution is firmly ruled out by the RVs" | §4.2.1 |
| `obs_rv2`: BH2 RVs agree | OBS | stated 2302.07880: "The follow-up RVs are fully consistent with the Gaia-only solution" | §3.7.1 |
| `mod_rv2`: agreeing RVs → orbit real | MOD | stated 2302.07880: "it is very unlikely that the observed RVs would just happen to match the predictions of the Gaia solution if that solution were incorrect" | §4.1 |
| `obs_rv3`: BH3 Gaia RVs agree | OBS | stated 2404.10486: "Gaia radial velocities independently validate the astrometric orbit" | Abstract |
| `mod_rv3`: agreeing RVs → orbit real | MOD | implied: El-Badry et al. 2023b, arXiv:2302.07880 §4.1 | — |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| Spurious Gaia solution (BH1) | `mod_rv1` | yes, §4.2.1 |
| Spurious Gaia solution (BH2) | `mod_rv2` | argued unlikely, §4.1; the conclusion is stated conditionally |
| Spurious solution (BH3) | `mod_rv3` | not argued for this source beyond the abstract sentence |

**Inference (Lean excerpt).**

```lean
have o1 : v.Orbit1 := p .mod_rv1 (p .obs_rv1)   -- Sec. 3.2, 4.2.1
```

**Critique.** For BH1 the step is strong: the RVs alone already require a > 4 Msun companion. For BH2
the RVs cover a small part of the 1277-day orbit, and the paper's own base rate is sobering (of six
candidates from the same cuts, four turned out to have spurious Gaia solutions); the paper therefore
states its conclusion "if the Gaia astrometric solution is correct". For BH3 the validation is internal to
Gaia; we mark the step as standard knowledge borrowed from the BH2 paper.

#### 2.2 Stage B · The companion weighs at least 5 Msun

**Overview.** Kepler's third law turns orbit size and period into mass. The papers quote joint-fit
masses; for BH1, Gaia's astrometry alone gives a second, independent route.

**Premises.**

| Premise | Tag | Provenance | Source |
|---|---|---|---|
| `stat_fit1`: fit1 ≥ 9.0 Msun | STAT | stated 2209.06833: "We infer an unseen companion mass M2=9.62±0.18" | §4.1, Table 1 |
| `mod_fit1`: real orbit + fit → mass ≥ 5 | MOD | implied: Kepler's third law (textbook, e.g. Murray and Dermott 1999) | — |
| `num_astro1`: astrometry-only mass ≥ 5.0 Msun | NUM | stated 2209.06833: "12.8±2.0" (Table 1, astrometry-only block); recomputed by `run.py`, bound to `results/summary.json:post_hoc.R1b_bh1_vs_dr3_only_paper.m2_ours >= 5.0` | Table 1 |
| `mod_astro1`: real orbit + astrometric mass → mass ≥ 5 | MOD | implied: Kepler's third law | — |
| `stat_fit2`: fit2 ≥ 8.0 Msun | STAT | stated 2302.07880: "M2 = 8.9 ± 0.3 Msun" | §3.7.3 |
| `mod_fit2` | MOD | implied: Kepler's third law | — |
| `stat_fit3`: fit3 ≥ 30.0 Msun | STAT | stated 2404.10486: "implies the presence of a 32.70±0.82 M⊙ BH" | Abstract, Eq. 5 |
| `mod_fit3` | MOD | implied: Kepler's third law | — |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly? |
|---|---|---|
| The visible star's mass M1 is badly wrong | `stat_fit*` (M2 depends only weakly on M1 here) | yes (BH1 §4.1 prior; BH2 §3.5, §3.5.1 stripped giant disfavoured) |
| Orbit seen nearly edge-on, inclination wrong | `stat_fit*` | BH2: the minimum mass for an edge-on orbit is still 2.6 Msun, §4 |

**Inference (Lean excerpt).**

```lean
have m1 : v.mass1 ≥ 50 := p .mod_fit1 o1 (p .stat_fit1)   -- Sec. 4.1
```

**Critique.** The thresholds are far below the measured values (9.6, 8.9, 32.7 against 5.0), so the
step does not depend on fine details of the uncertainties. For BH1 the mass is over-determined: Lean
finds both routes redundant (2.N).

#### 2.3 Stage C · The mass is not in luminous stars

**Overview.** A star of several solar masses is hundreds of times brighter than the systems observed;
the spectra would show it.

**Premises.**

| Premise | Tag | Provenance | Source |
|---|---|---|---|
| `obs_faint1` | OBS | stated 2209.06833: "no evidence of another luminous star" | §5.1.1 |
| `mod_dark1`: faint + mass ≥ 5 → not luminous stars | MOD | stated 2209.06833: "any normal star with a mass exceeding ≈0.4 M⊙ would easily be detected in the spectrum" | §8.1 |
| `obs_faint2` | OBS | stated 2302.07880: "A companion contributing more than ≈2% of the total light at 4000-4300 Å would dilute the absorption lines beyond this value and is thus ruled out" | §3.8.1 |
| `mod_dark2` | MOD | stated 2302.07880: "a 9Msun main-sequence star would outshine the giant at all wavelengths" | §4 |
| `obs_faint3` | OBS | stated 2404.10486: "The spectra do not show any sign of the presence of a second component, nor any emission line" | App. C |
| `mod_dark3` | MOD | stated 2404.10486: "too low by several orders of magnitude to be compatible with the hypothesis that the companion is a main sequence star" | §3 |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly? |
|---|---|---|
| A massive main-sequence star | `mod_dark*` | yes, all three |
| An inner pair of ordinary stars | `mod_dark*` | yes for BH1, BH2 (each still far too bright); BH3 mentions "two main sequence stars" |
| A giant companion | `mod_dark2` | BH2: "one or more red giant companions would outshine the giant in the optical" |
| A rapidly rotating hot star (broad, shallow lines) | `obs_faint*` | partly: BH1 rules out "hot and small or cool and large" companions with UV-to-IR spectra; BH2 notes rotating secondaries are harder to detect and uses the UV |

**Inference (Lean excerpt).**

```lean
have n1 : v.NoStar1 := p .mod_dark1 (p .obs_faint1) m1   -- Sec. 5.1.1, 8.1
```

**Critique.** The quoted BH2 and BH3 sentences speak about main-sequence stars; our atom `NoStar` covers
all luminous stars, so for those two papers the premise leans on the neighbouring sentences (giants for
BH2, "two main sequence stars" for BH3). A reviewer should check that the encoding is not stronger than
the papers here.

#### 2.4 Stage D · A black hole is required

**Overview.** Once the mass is dark and at least 5 Msun, the remaining non-black-hole options are
white dwarfs (below 1.4 Msun each) and neutron stars (below about 2.3 Msun each). One or two of them
cannot reach 5 Msun; three or more would be needed.

**Premises.**

| Premise | Tag | Provenance | Source |
|---|---|---|---|
| `mod_few1`: at most two objects | MOD | stated 2209.06833: "Scenarios involving more than two objects inside the G star's orbit are difficult to assemble and unlikely to be dynamically stable" | §8.2 |
| `lit_ns1`: dark, at most two, ≥ 5 Msun → black hole | LIT | implied: maximum neutron-star mass, Özel and Freire 2016, arXiv:1603.02698 | — |
| `mod_few2` | MOD | stated 2302.07880: "such a configuration would be difficult to assemble and would rapidly become unstable" | §4 |
| `lit_ns2` | LIT | implied: Özel and Freire 2016 | — |
| `mod_few3` | MOD | implied: El-Badry et al. 2023a, arXiv:2209.06833 §8.2 | — |
| `mod_ns3` | MOD | stated 2404.10486: "The estimated mass is also too large for one neutron star or two neutron stars in a close orbit" | §3 |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly? |
|---|---|---|
| A single neutron star or white dwarf | `lit_ns*`, `mod_ns3` | yes (BH1 §8.1 names the maximum neutron-star mass without a number; BH2 §4; BH3 §3) |
| Two compact objects without a black hole | `lit_ns*`, `mod_ns3` | BH3 yes; BH1/BH2 implicitly |
| Three or more neutron stars / white dwarfs | `mod_few*` | BH1, BH2: argued unstable, not excluded by data; BH3: not discussed (we borrow the BH1 argument) |
| An inner pair containing a black hole | — | not a rival: the conclusion is "contains a black hole" |

**Inference (Lean excerpt).**

```lean
have b1 : v.BH1 := p .lit_ns1 n1 (p .mod_few1) m1   -- Sec. 8.2 (NS mass implied)
exact ⟨b1, b2, b3⟩
```

**Critique.** Neither BH paper states the maximum neutron-star mass as a number; BH1 names "the maximum
neutron star mass" in passing. The step is textbook, so we tag it `[implied]`. The exclusion of three or
more compact objects is a plausibility argument (assembly, stability), stated by BH1 and BH2 and not
discussed by BH3.

#### 2.5 What the Lean check found

1. **`explicit_sufficient` holds; `stated_insufficient` holds.** With standard knowledge added, the
   argument is complete: no `GAP` premise was needed. What the papers write is not quite enough on its
   own: they rely on Kepler's law for the mass (`mod_fit*`, `mod_astro1`), on the maximum neutron-star
   mass (`lit_ns1`, `lit_ns2`, never given as a number), and, for BH3, on two steps argued in the earlier
   papers (`mod_rv3`, `mod_few3`).
2. **Where the argument is weak is physics, not logic.** The decisive premises are stated as
   plausibility arguments and encoded as assertions: that RVs matching the orbit make a spurious
   solution negligible (`mod_rv2`; the BH2 paper itself keeps its conclusion conditional), and that
   three or more compact objects would be unstable (`mod_few*`). Lean cannot weigh these; it shows
   that the conclusion stands or falls with them.
3. **Redundant premises.** `stat_fit1`, `mod_fit1`, `num_astro1` and `mod_astro1` are each redundant:
   BH1's mass has two independent routes (joint fit; astrometry alone). Removing either still leaves the
   conclusion. This is a real feature of the BH1 case, not an artefact: our repository's DR3-only
   recomputation (13.3 Msun) alone is enough for stage B.
4. **Consistency.** `consistent` holds, but it is a weak check here: there are no negative premises.
5. **Limits.** Lean checks the logical structure under our encoding, not the physics in each premise.
   Uncertainties are folded into chosen integer thresholds (5 Msun, 9.0, 8.0, 30.0); "very likely" and
   "most probably" are encoded as assertions; the neutron-star candidate paper (1.3d) is not part of the
   chain.

### Part 3 · What astrolab can test or explore

*Written after implementation (post hoc); not a pre-registration.* The study's actual pre-registration
is in its [README](https://github.com/sudoghut/astrolab/blob/main/studies/001-m04-gaia-dormant-black-holes/README.md)
(sections 1–4, with a DR4 addendum written before the DR4 release).

| Stage / claim | Can we test or explore it? | How | Data (size) | Decision criterion | Result |
|---|---|---|---|---|---|
| B: BH1 mass from Gaia DR3 alone | testable now | Monte Carlo over the full DR3 covariance, M1 = 0.93 | 2 NSS rows, < 10 kB | within 2σ of the published mass | reproduced: 13.3 (+2.9/−2.3) Msun, +1.4σ from 9.62; +0.23σ from the paper's astrometry-only 12.8 |
| B: BH2 mass from Gaia DR3 alone | testable now | same, M1 = 1.07 | as above | within 2σ | reproduced: 8.52 (+0.61/−0.56) Msun, −0.6σ |
| A: is the orbit real? (RV prediction) | testable now (partial) | predicted RV range from the astrometric orbit vs Gaia's `rv_amplitude_robust` | in the vetting query | matches the published RV ranges | reproduced for the six sources in El-Badry et al. 2023a Table E1 |
| Recovery of known dark companions | testable now | server-side screen of all DR3 astrometric orbits (f_M > 0.25 Msun) | 3,343 rows, 0.4 MB | ≥ 19 of the 21 neutron-star candidates recovered | 21/21 (weak test) |
| B, C for BH3 | testable after Gaia DR4 (2026-12-02) | pre-registered R3 | DR4 query, counted first | within 2σ of 32.70 Msun | pending |
| C: luminosity limits | out of scope | needs spectra | — | — | — |
| D: stability of multiple compact objects | explorable (not decisive) | n-body or literature | — | none - exploration only | not started |

What we found so far: Gaia DR3 alone reproduces the BH1 and BH2 masses, the screen recovers the known
dark companions, and our vetoes leave 51 unexplained candidates in DR3, all giants or low-significance
solutions, so no new dormant black hole around a main-sequence star. The interactive page runs locally
with `python -m astrolab serve`.

### Glossary

| Term | Meaning |
|---|---|
| Astrometry | Measuring positions of stars on the sky. |
| Astrometric mass function f_M | (a0/ϖ)³/P²: what Kepler's law gives from the visible star's orbit alone. |
| Radial velocity (RV) | A star's speed along the line of sight, from the Doppler shift of its lines. |
| SED | Spectral energy distribution: brightness across wavelengths. |
| NSS | Gaia's non-single-star catalogue (fitted binary orbits). |
| Thiele-Innes constants | Four numbers that encode an orbit's size and orientation on the sky. |
| Countermodel | An assignment of the atoms in which all premises but one hold and the conclusion fails. |

### Open questions

- How often are Gaia astrometric orbits of this kind spurious, as a function of quality cuts? (The BH2
  paper's base rate: four of six.)
- Can DR4 epoch astrometry and RVs decide the 51 DR3 candidates the vetoes leave open?
- Are inner pairs (black hole + black hole, black hole + compact object) detectable by small RV
  perturbations, as the BH3 paper suggests (about 0.2 km/s)?

### Changelog

Newest first.

- 2026-11-14: first version: parts 1–3, written after the DR3 implementation (T-010).

### Sources

- El-Badry et al. 2023a, MNRAS 518, 1057, arXiv:2209.06833 (read: v3) [V]
- El-Badry et al. 2023b, MNRAS 521, 4323, arXiv:2302.07880 (read: v2) [V]
- Gaia Collaboration, Panuzzo et al. 2024, A&A 686, L2, arXiv:2404.10486 (read: v2) [V]
- El-Badry et al. 2024, OJAp 7, arXiv:2405.00089 (read: v2) [V]
- Özel and Freire 2016, ARA&A 54, 401, arXiv:1603.02698 (maximum neutron-star mass)

---

## 中文

### 第一部分 · 科普详解

#### 1.1 问题与意义

比太阳重得多的恒星，死后会变成黑洞，所以银河系里应该有约一亿个恒星级黑洞。可是我们知道的黑洞几乎都是因为它在"进食"才被发现的：伴星把气体倒向黑洞，气体被加热，发出 X 射线。进食的黑洞很少，也未必有代表性。一个安静地待在普通恒星旁边、没有东西落进去的黑洞，什么也不发出。这样的"休眠"黑洞应该多得多，但只能通过引力发现：可见的恒星绕着一个看不见的东西运动。

2022 年以前，所有声称在普通恒星旁边发现的休眠黑洞，后来都有了别的解释（最常见的是漏掉了一颗更暗的恒星）。这几篇论文回答的问题是：只要把一颗恒星自身的运动测得足够准，能不能证明它看不见的伙伴是黑洞？

#### 1.2 数据

欧洲空间局的 Gaia 卫星多年来反复测量约二十亿颗恒星的位置。双星中的一颗星在天空上不走直线，而是绕着双星的质心画一个小椭圆。Gaia 第三次数据发布（DR3，2022 年 6 月）首次给出约 44 万个双星的拟合轨道（"非单星"星表，NSS）。对天体测量轨道，拟合给出恒星在天空上的椭圆大小（半长轴 a0，单位毫角秒）、周期 P、形状（偏心率 e）和方向，方向由四个称为 Thiele-Innes 常数的数表示。再结合由视差 ϖ 得到的距离，角大小就变成以天文单位计的实际大小。

只凭轨道大小和周期，开普勒第三定律就给出天体测量质量函数 f_M = (a0/ϖ)³ / P²（P 以年计，结果以太阳质量计）。如果伴星不发光，f_M 等于 M2³ / (M1 + M2)²，M1 是可见星的质量，M2 是伴星的质量。由恒星的颜色和亮度知道 M1，就能求出 M2。

论文接着用地面光谱仪观测。光谱仪通过吸收线的多普勒位移测量恒星的视向速度（radial velocity, RV），即朝向或离开我们的速度。视向速度从另一个角度看同一个轨道。光谱还能看出有没有第二颗星在发光：第二颗星会带来自己的谱线，或者冲淡可见星的谱线。

#### 1.3 一步一步：作者如何从数据走到结论

##### 1.3a Gaia BH1（El-Badry 等 2023a）

1. **Gaia 给出的候选。** 在 DR3 的天体测量轨道中，一颗距离 480 pc、G = 13.8 星等的类太阳恒星有约 186 天的轨道，a0 = 3.00 ± 0.22 毫角秒，意味着伴星约 10 倍太阳质量且不发光。它刚好越过 Gaia 的质量门槛，而 Gaia 的观测只覆盖了约半个轨道，所以这个解需要核查。
2. **视向速度后续观测。** 作者在四个月里用六台光谱仪（MagE、GMOS、X-shooter、HIRES、FEROS、ESI）拍了 39 条光谱，另有两条 LAMOST 存档光谱。视向速度覆盖了轨道预期变化范围的大部分，并大体证实了 Gaia 的解。即使完全不用 Gaia，单凭视向速度也要求伴星至少约 4 倍太阳质量。
3. **质量。** 可见星质量 M1 = 0.93 ± 0.05 M☉，来自对其光谱能量分布（SED）的拟合与恒星演化模型的比较。Gaia 天体测量与视向速度联合拟合给出 P = 185.59 ± 0.05 天、e = 0.451 ± 0.005、**M2 = 9.62 ± 0.18 M☉**。只用 Gaia 天体测量得到 12.8 ± 2.0 M☉，两者在 1.6σ 水平上一致。
4. **伴星不发光。** 光谱里"没有另一颗发光恒星的迹象"；只贡献连续谱的伴星最多提供约 10% 的光，带有自己谱线的伴星超过约 3% 就会被发现。作者指出，任何质量超过约 0.4 M☉ 的普通恒星都会在光谱中轻易被看到；一颗 10 M☉ 的恒星会比整个系统亮几百倍。
5. **还可能是什么？** 不是普通恒星（太暗）。不是白矮星或中子星（太重）。不是一群致密天体：轨道内有两个以上天体的情形难以形成，也不太可能动力学稳定。两个不含黑洞的致密天体到不了 10 M☉。剩下的只有单个黑洞，或含有黑洞的一对天体。

*粗略估算。* a0 = 3.0 毫角秒、ϖ = 2.08 毫角秒，得 a1 ≈ 1.44 au；P = 0.509 年，得 f_M ≈ 1.44³/0.509² ≈ 11 M☉。取 M1 ≈ 1 M☉，解 M2³ = 11 (1 + M2)² 得 M2 ≈ 13 M☉：一个不发光的天体，质量在十倍太阳质量的量级。

##### 1.3b Gaia BH2（El-Badry 等 2023b）

1. **带天体测量加光谱联合解的候选。** 一颗距离 1.16 kpc、G = 12.3 的红巨星有 Gaia 天体测量与光谱联合解（AstroSpectroSB1），P = 1352 ± 45 天，天体测量质量函数 6.7 ± 0.5 M☉，取 M1 = 1 M☉ 时 M2 ≈ 8.4 M☉。
2. **视向速度后续观测。** 七个月内 48 个视向速度（FEROS 43 个、UVES 5 个）。后续视向速度与只用 Gaia 的解完全一致。联合拟合给出 P = 1276.7 ± 0.6 天、e = 0.518；Gaia 单独给出的周期相差 1.6σ，作者归因于 Gaia 流程把轨道的光谱部分和天体测量部分联系起来的方式。
3. **质量。** 由巨星的温度和半径配合演化轨迹得到 M1 = 1.07 ± 0.19 M☉；联合拟合给出 **M2 = 8.9 ± 0.3 M☉**，轨道倾角约 35°。
4. **不发光。** 最深的吸收线降到连续谱的约 2%，所以在 4000 Å 处贡献超过约 2–3% 光的伴星会把它们冲淡；紫外也很暗。一颗 9 M☉ 的主序星会在所有波段都比巨星亮。
5. **还可能是什么？** 与 BH1 相同：一群致密天体难以形成，而且很快会变得不稳定。结论是有条件的：如果 Gaia 天体测量解是正确的，伴星必定是黑洞，或含有黑洞的密近双星。作者认为 Gaia 解出错的可能性很小，因为独立的视向速度符合它的预测。

##### 1.3c Gaia BH3（Gaia 合作组 Panuzzo 等 2024）

在验证 Gaia DR4 预发布数据（一次称为 NSS 4.1 的初步流程运行）时发现：一颗年老、贫金属的巨星，M1 = 0.76 ± 0.05 M☉，轨道周期 11.6 年（P = 4253 ± 99 天，e = 0.73）。Gaia 自己的视向速度独立证实了天体测量轨道。联合解给出质量函数 31.2 ± 0.8 M☉、**M2 = 32.70 ± 0.82 M☉**。光谱没有显示第二个成分的任何迹象，观测到的光度比主序伴星应有的低几个数量级；这个质量对一颗中子星或一对密近中子星都太大。作者的结论是它"很可能"是单个黑洞，是银河系已知质量最大的恒星级黑洞，同时指出不能排除内部是一对黑洞。

##### 1.3d 中子星候选（El-Badry 等 2024）

同样的方法推向更低的伴星质量：21 颗处于宽轨道（P ≈ 190–1050 天）的类太阳恒星，伴星质量 1.26–1.90 M☉；在光度限制下，这对任何普通恒星或密近恒星对都太重；用约 300 个视向速度证实。最简单的解释是中子星，但不能完全排除超大质量白矮星和密近双白矮星。对本项目而言，这 21 个天体是已知的正样本对照：寻找暗伴星的筛选应当能把它们找回来。

#### 1.4 结论与把握程度

- BH1 与 BH2：9.6 和 8.9 M☉ 的暗伴星，至少含有一个黑洞；最简单的解读是单个黑洞。论文对质量和不发光很有把握；认定为黑洞依赖于 (a) 轨道是真实的，(b) 没有其他这种质量的暗天体说得通。
- BH3：33 M☉ 的暗伴星，"很可能"是单个黑洞，数据是初步的。
- 作者若是错的，需要以下之一成立：Gaia 轨道是虚假的（BH1 被视向速度排除；BH2 论证为可能性很小；BH3 由 Gaia 自己的视向速度检验）；可见星质量严重偏差（这只会适度改变 M2）；或者暗质量是由多颗中子星或白矮星组成的稳定群体（论证为不合理，但没有被数据排除）。

### 第二部分 · 论证逻辑

#### 2.0 论证地图

对每个系统 i（1 = BH1，2 = BH2，3 = BH3），都是同样的四环链条：

A. 后续视向速度与 Gaia 轨道一致 → 轨道是真实的；
B. 真实的轨道和拟合质量 → 伴星至少 5 M☉；
C. 没有伴星的光，加上这个质量 → 这些质量不在发光恒星中；
D. 至多两个天体，加上中子星最大质量 → 伴星含有黑洞。

结论：BH1 ∧ BH2 ∧ BH3（每个伴星都至少含有一个黑洞）。

检查方法：论证写成 Lean 4（[`studies/001-m04-gaia-dormant-black-holes/argument/Argument.lean`](https://github.com/sudoghut/astrolab/blob/main/studies/001-m04-gaia-dormant-black-holes/argument/Argument.lean)）。每个前提是 `Field` 的一个构造子（不用公理 axiom），标注类型与出处性质：

| 标签 | 前提类型 |
|---|---|
| `OBS` | 观测或测量（注明表格、图） |
| `MOD` | 模型假设 |
| `STAT` | 统计推断（显著性、模型比较） |
| `NUM` | 数值结果，由本仓库 `run.py` 复核 |
| `LIT` | 引自其他文献的结论 |
| `GAP` | 推理需要、但论文和标准知识都没有提供的前提 |

出处性质：`[stated <arXiv 编号>: "引文"]`（论文明说，附原文）、`[implied]`（论文依赖但没写出的标准知识，注明来源）、`[reconstructed]`（我们补上的，恰好就是 `GAP` 前提）。

Lean 检查什么：结论能否由这些前提推出（`final`）且并非恒真（`final_nontrivial`）；前提能否同时成立（`consistent`）；单个前提不能单独推出结论（`alone_insufficient`）；每个前提是必要的（去掉它时的反例模型）还是多余的；论文明说的前提是否足够（`stated_*`）；加上标准知识后是否足够（`explicit_*`）。Lean 不检查每个前提内部的物理是否正确。

质量以十分之一太阳质量为单位（整数），所以"至少 5 M☉"写作 `mass ≥ 50`。

#### 2.1 环节 A · 轨道是真实的

**概述。** 论证中的所有质量都来自轨道。如果 Gaia 的轨道解是假象，后面什么都推不出来。论文用独立的视向速度解决这一点。

**前提。**

| 前提（Lean 构造子） | 标签 | 出处性质 | 论文出处 |
|---|---|---|---|
| `obs_rv1`：BH1 的视向速度与 Gaia 轨道一致 | OBS | stated 2209.06833："The follow-up RVs span most of the orbit's predicted dynamic range and broadly validate the Gaia solution" | §3.2 |
| `mod_rv1`：一致的视向速度 → 轨道真实 | MOD | stated 2209.06833："a catastrophic problem with the astrometric solution is firmly ruled out by the RVs" | §4.2.1 |
| `obs_rv2`：BH2 的视向速度一致 | OBS | stated 2302.07880："The follow-up RVs are fully consistent with the Gaia-only solution" | §3.7.1 |
| `mod_rv2`：一致的视向速度 → 轨道真实 | MOD | stated 2302.07880："it is very unlikely that the observed RVs would just happen to match the predictions of the Gaia solution if that solution were incorrect" | §4.1 |
| `obs_rv3`：BH3 的 Gaia 视向速度一致 | OBS | stated 2404.10486："Gaia radial velocities independently validate the astrometric orbit" | 摘要 |
| `mod_rv3`：一致的视向速度 → 轨道真实 | MOD | implied：El-Badry 等 2023b，arXiv:2302.07880 §4.1 | — |

**其他解释（rival explanations）。**

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| Gaia 解是虚假的（BH1） | `mod_rv1` | 是，§4.2.1 |
| Gaia 解是虚假的（BH2） | `mod_rv2` | 论证为可能性很小，§4.1；结论以条件句表述 |
| 虚假解（BH3） | `mod_rv3` | 除摘要那句话外，没有针对这颗星的论证 |

**推理（Lean 摘录）。**

```lean
have o1 : v.Orbit1 := p .mod_rv1 (p .obs_rv1)   -- Sec. 3.2, 4.2.1
```

**评析。** 对 BH1 这一步很强：单凭视向速度已要求伴星 > 4 M☉。对 BH2，视向速度只覆盖 1277 天轨道的一小段，论文自己给出的基础比率也令人警醒（同样筛选条件下的六个候选中，有四个的 Gaia 解后来证明是虚假的），所以论文把结论写成"如果 Gaia 天体测量解是正确的"。对 BH3，检验在 Gaia 内部完成；我们把这一步标为借自 BH2 论文的标准知识。

#### 2.2 环节 B · 伴星至少 5 M☉

**概述。** 开普勒第三定律把轨道大小和周期变成质量。论文给出联合拟合的质量；对 BH1，只用 Gaia 天体测量给出第二条独立的路径。

**前提。**

| 前提 | 标签 | 出处性质 | 出处 |
|---|---|---|---|
| `stat_fit1`：fit1 ≥ 9.0 M☉ | STAT | stated 2209.06833："We infer an unseen companion mass M2=9.62±0.18" | §4.1，表 1 |
| `mod_fit1`：真实轨道 + 拟合 → 质量 ≥ 5 | MOD | implied：开普勒第三定律（教科书，如 Murray 与 Dermott 1999） | — |
| `num_astro1`：只用天体测量的质量 ≥ 5.0 M☉ | NUM | stated 2209.06833："12.8±2.0"（表 1，只用天体测量的一栏）；由 `run.py` 复算，绑定 `results/summary.json:post_hoc.R1b_bh1_vs_dr3_only_paper.m2_ours >= 5.0` | 表 1 |
| `mod_astro1`：真实轨道 + 天体测量质量 → 质量 ≥ 5 | MOD | implied：开普勒第三定律 | — |
| `stat_fit2`：fit2 ≥ 8.0 M☉ | STAT | stated 2302.07880："M2 = 8.9 ± 0.3 Msun" | §3.7.3 |
| `mod_fit2` | MOD | implied：开普勒第三定律 | — |
| `stat_fit3`：fit3 ≥ 30.0 M☉ | STAT | stated 2404.10486："implies the presence of a 32.70±0.82 M⊙ BH" | 摘要，式 5 |
| `mod_fit3` | MOD | implied：开普勒第三定律 | — |

**其他解释。**

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 可见星质量 M1 严重偏差 | `stat_fit*`（这里 M2 对 M1 依赖很弱） | 是（BH1 §4.1 先验；BH2 §3.5，§3.5.1 不支持剥离巨星） |
| 轨道接近侧向、倾角估错 | `stat_fit*` | BH2：侧向轨道的最小质量仍有 2.6 M☉，§4 |

**推理（Lean 摘录）。**

```lean
have m1 : v.mass1 ≥ 50 := p .mod_fit1 o1 (p .stat_fit1)   -- Sec. 4.1
```

**评析。** 阈值远低于测量值（9.6、8.9、32.7 对 5.0），所以这一步不依赖不确定度的细节。对 BH1，质量是"超定"的：Lean 发现两条路径各自都是多余的（见 2.5）。

#### 2.3 环节 C · 这些质量不在发光恒星中

**概述。** 几倍太阳质量的恒星比观测到的系统亮几百倍，光谱里会看到它。

**前提。**

| 前提 | 标签 | 出处性质 | 出处 |
|---|---|---|---|
| `obs_faint1` | OBS | stated 2209.06833："no evidence of another luminous star" | §5.1.1 |
| `mod_dark1`：不发光 + 质量 ≥ 5 → 不在发光恒星中 | MOD | stated 2209.06833："any normal star with a mass exceeding ≈0.4 M⊙ would easily be detected in the spectrum" | §8.1 |
| `obs_faint2` | OBS | stated 2302.07880："A companion contributing more than ≈2% of the total light at 4000-4300 Å would dilute the absorption lines beyond this value and is thus ruled out" | §3.8.1 |
| `mod_dark2` | MOD | stated 2302.07880："a 9Msun main-sequence star would outshine the giant at all wavelengths" | §4 |
| `obs_faint3` | OBS | stated 2404.10486："The spectra do not show any sign of the presence of a second component, nor any emission line" | 附录 C |
| `mod_dark3` | MOD | stated 2404.10486："too low by several orders of magnitude to be compatible with the hypothesis that the companion is a main sequence star" | §3 |

**其他解释。**

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 一颗大质量主序星 | `mod_dark*` | 是，三篇都排除 |
| 一对普通恒星 | `mod_dark*` | BH1、BH2 是（仍然太亮）；BH3 提到"两颗主序星" |
| 一颗巨星伴星 | `mod_dark2` | BH2：一颗或多颗红巨星伴星会在光学波段比可见星亮 |
| 快速自转的热星（谱线宽而浅） | `obs_faint*` | 部分：BH1 用紫外到红外光谱排除"热而小或冷而大"的伴星；BH2 指出自转快的伴星较难探测，并用紫外加以限制 |

**推理（Lean 摘录）。**

```lean
have n1 : v.NoStar1 := p .mod_dark1 (p .obs_faint1) m1   -- Sec. 5.1.1, 8.1
```

**评析。** BH2 与 BH3 所引的句子讲的是主序星；我们的原子 `NoStar` 涵盖所有发光恒星，所以对这两篇论文，这条前提还依赖相邻的句子（BH2 关于巨星，BH3 关于"两颗主序星"）。审稿人应核对此处编码是否强于原文。

#### 2.4 环节 D · 必须有黑洞

**概述。** 一旦确定这些质量不发光且至少 5 M☉，剩下的非黑洞选项是白矮星（每颗低于 1.4 M☉）和中子星（每颗低于约 2.3 M☉）。一颗或两颗都到不了 5 M☉，需要三颗以上。

**前提。**

| 前提 | 标签 | 出处性质 | 出处 |
|---|---|---|---|
| `mod_few1`：至多两个天体 | MOD | stated 2209.06833："Scenarios involving more than two objects inside the G star's orbit are difficult to assemble and unlikely to be dynamically stable" | §8.2 |
| `lit_ns1`：不发光、至多两个、≥ 5 M☉ → 黑洞 | LIT | implied：中子星最大质量，Özel 与 Freire 2016，arXiv:1603.02698 | — |
| `mod_few2` | MOD | stated 2302.07880："such a configuration would be difficult to assemble and would rapidly become unstable" | §4 |
| `lit_ns2` | LIT | implied：Özel 与 Freire 2016 | — |
| `mod_few3` | MOD | implied：El-Badry 等 2023a，arXiv:2209.06833 §8.2 | — |
| `mod_ns3` | MOD | stated 2404.10486："The estimated mass is also too large for one neutron star or two neutron stars in a close orbit" | §3 |

**其他解释。**

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 单颗中子星或白矮星 | `lit_ns*`、`mod_ns3` | 是（BH1 §8.1 提到中子星最大质量但未给数值；BH2 §4；BH3 §3） |
| 两个不含黑洞的致密天体 | `lit_ns*`、`mod_ns3` | BH3 明确；BH1、BH2 隐含 |
| 三个或更多中子星或白矮星 | `mod_few*` | BH1、BH2：论证为不稳定，但未被数据排除；BH3：未讨论（我们借用 BH1 的论证） |
| 内部是含黑洞的一对天体 | — | 不构成反驳：结论是"含有黑洞" |

**推理（Lean 摘录）。**

```lean
have b1 : v.BH1 := p .lit_ns1 n1 (p .mod_few1) m1   -- Sec. 8.2 (NS mass implied)
exact ⟨b1, b2, b3⟩
```

**评析。** 两篇 BH 论文都没有给出中子星最大质量的数值；BH1 只是顺带提到"中子星最大质量"。这一步属于教科书知识，所以我们标为 `[implied]`。排除三个以上致密天体靠的是合理性论证（难以形成、不稳定），BH1 与 BH2 明说了，BH3 没有讨论。

#### 2.5 Lean 检查发现的问题

1. **`explicit_sufficient` 成立；`stated_insufficient` 成立。** 加上标准知识后论证完整，不需要任何 `GAP` 前提。论文写出的内容本身还不够：它们依赖开普勒定律求质量（`mod_fit*`、`mod_astro1`），依赖中子星最大质量（`lit_ns1`、`lit_ns2`，从未给出数值），BH3 还依赖前两篇论文中论证过的两步（`mod_rv3`、`mod_few3`）。
2. **薄弱之处在物理，不在逻辑。** 起决定作用的前提是以合理性论证写出、被编码为断言的：视向速度符合轨道就足以排除虚假解（`mod_rv2`；BH2 论文自己也把结论写成条件句），以及三个以上致密天体会不稳定（`mod_few*`）。Lean 无法衡量这些前提的分量，只能表明结论随它们成立或不成立。
3. **多余的前提。** `stat_fit1`、`mod_fit1`、`num_astro1` 与 `mod_astro1` 各自都是多余的：BH1 的质量有两条独立路径（联合拟合；只用天体测量），去掉任何一条结论仍然成立。这是 BH1 的真实特点，不是编码的产物：本仓库只用 DR3 复算的质量（13.3 M☉）单独就足以支撑环节 B。
4. **相容性。** `consistent` 成立，但这里分量不大：没有否定形式的前提。
5. **局限。** Lean 检查的是在我们的编码下的逻辑结构，不检查每个前提内部的物理。不确定度被折算成选定的整数阈值（5、9.0、8.0、30.0 M☉）；"很可能"被编码为断言；中子星候选论文（1.3d）不在链条中。

### 第三部分 · 本项目可检验或探索的环节

*实现后补写（事后，post hoc），不是预注册。* 研究真正的预注册在它的 [README](https://github.com/sudoghut/astrolab/blob/main/studies/001-m04-gaia-dormant-black-holes/README.md) 中（第 1–4 节，另有 DR4 发布前写好的 DR4 附录）。

| 环节 / 结论 | 能否检验或探索 | 方法 | 数据（大小） | 判据 | 结果 |
|---|---|---|---|---|---|
| B：只用 Gaia DR3 求 BH1 质量 | 现在可检验 | 对 DR3 完整协方差做蒙特卡罗，M1 = 0.93 | 2 行 NSS，< 10 kB | 与已发表质量相差 2σ 以内 | 已复现：13.3 (+2.9/−2.3) M☉，与 9.62 相差 +1.4σ；与论文只用天体测量的 12.8 相差 +0.23σ |
| B：只用 Gaia DR3 求 BH2 质量 | 现在可检验 | 同上，M1 = 1.07 | 同上 | 2σ 以内 | 已复现：8.52 (+0.61/−0.56) M☉，−0.6σ |
| A：轨道是否真实（视向速度预测） | 现在可检验（部分） | 由天体测量轨道预测视向速度变化幅度，与 Gaia 的 `rv_amplitude_robust` 比较 | 在否决规则的查询中 | 与已发表的视向速度幅度一致 | El-Badry 等 2023a 表 E1 中的六个源全部复现 |
| 找回已知暗伴星 | 现在可检验 | 在服务器端筛选全部 DR3 天体测量轨道（f_M > 0.25 M☉） | 3,343 行，0.4 MB | 21 个中子星候选中至少找回 19 个 | 21/21（检验偏弱） |
| BH3 的 B、C | 待 Gaia DR4（2026-12-02） | 预注册的 R3 | DR4 查询，先计数 | 与 32.70 M☉ 相差 2σ 以内 | 待定 |
| C：光度限制 | 不在范围内 | 需要光谱 | — | — | — |
| D：多个致密天体的稳定性 | 可探索（不能判决） | n 体模拟或文献 | — | 无——仅供探索 | 尚未开始 |

目前的发现：只用 Gaia DR3 就能复现 BH1 与 BH2 的质量；筛选能找回已知的暗伴星；我们的否决规则在 DR3 中留下 51 个未解释的候选，全部是巨星或低显著性的解，所以没有发现主序星旁边的新休眠黑洞。交互网页在本地用 `python -m astrolab serve` 打开。

### 术语表

| 术语 | 含义 |
|---|---|
| 天体测量（astrometry） | 测量恒星在天空上的位置。 |
| 天体测量质量函数 f_M（astrometric mass function） | (a0/ϖ)³/P²：只凭可见星的轨道由开普勒定律得到的量。 |
| 视向速度（radial velocity, RV） | 恒星沿视线方向的速度，由谱线的多普勒位移测得。 |
| 光谱能量分布（SED） | 恒星在各波段的亮度。 |
| 非单星星表（NSS） | Gaia 的双星轨道拟合星表。 |
| Thiele-Innes 常数 | 描述轨道在天空上大小与方向的四个数。 |
| 反例模型（countermodel） | 对原子命题的一种取值，使除某一条外的所有前提都成立而结论不成立。 |

### 开放问题

- 这类 Gaia 天体测量轨道虚假的比例有多高，与质量筛选条件有什么关系？（BH2 论文的基础比率：六个中有四个。）
- DR4 的历元天体测量与视向速度，能否判定否决规则在 DR3 中留下的 51 个候选？
- 内部的天体对（黑洞 + 黑洞，黑洞 + 致密天体）能否像 BH3 论文建议的那样，通过约 0.2 km/s 的视向速度微扰探测到？

### 研究进展

按时间倒序。

- 2026-11-14：第一版：第一至三部分，在 DR3 实现之后补写（T-010）。

### 来源

- El-Badry 等 2023a, MNRAS 518, 1057, arXiv:2209.06833（阅读版本 v3）[V]
- El-Badry 等 2023b, MNRAS 521, 4323, arXiv:2302.07880（阅读版本 v2）[V]
- Gaia 合作组 Panuzzo 等 2024, A&A 686, L2, arXiv:2404.10486（阅读版本 v2）[V]
- El-Badry 等 2024, OJAp 7, arXiv:2405.00089（阅读版本 v2）[V]
- Özel 与 Freire 2016, ARA&A 54, 401, arXiv:1603.02698（中子星最大质量）
