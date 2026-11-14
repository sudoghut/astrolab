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

Stars much heavier than the Sun end their lives as black holes, so the Milky Way should contain about a
hundred million stellar-mass black holes. Almost all the ones we know, however, were found because they
are *feeding*: a companion star spills gas onto the black hole, the gas heats up and glows in X-rays.
Feeding black holes are rare and probably not typical. A black hole that sits quietly next to an ordinary
star, with nothing falling onto it, emits nothing at all. Such "dormant" black holes should be far more
common, but they can only be found by their gravity: the visible star moves in an orbit around something
that cannot be seen.

Before 2022, every claimed dormant black hole around a normal star had later been explained another way
(most often a second, fainter star that had been overlooked). The question these papers answer is: can a
star's own motion, measured precisely enough, prove that its invisible partner is a black hole?

#### 1.2 The data

The European Space Agency's Gaia satellite measures the positions of about two billion stars, again and
again, for years. A star in a binary does not move in a straight line across the sky; it traces a small
ellipse around the binary's centre of mass. Gaia's third data release (DR3, June 2022) included, for the
first time, fitted orbits for about 440,000 binaries (the "non-single-star" or NSS catalogue). For an
*astrometric* orbit the fit gives the size of the star's ellipse on the sky (the semi-major axis a0, in
milliarcseconds), the period P, the shape (eccentricity e) and the orientation, through four numbers called
the Thiele-Innes constants. With the star's distance (from its parallax ϖ) the angular size becomes a
physical size in astronomical units.

From the orbit's size and period alone, Kepler's third law gives the *astrometric mass function*,
f_M = (a0/ϖ)³ / P², in solar masses (with P in years). If the companion is dark, f_M equals
M2³ / (M1 + M2)², where M1 is the visible star's mass and M2 the companion's. With M1 known from the star's
colour and brightness, M2 follows.

The papers then added spectroscopy. A spectrograph measures the star's radial velocity (RV), its speed
towards or away from us, through the Doppler shift of its absorption lines. RVs give an independent view
of the same orbit; on their own they give the *spectroscopic mass function*, which sets a minimum companion
mass whatever the orbit's tilt. Spectra also show whether a second star contributes light: a second star
would add its own lines, or dilute the visible star's lines.

#### 1.3 Step by step: how the authors got from data to conclusion

##### 1.3a Gaia BH1 (El-Badry et al. 2023a)

1. **A candidate from Gaia.** Among DR3 astrometric orbits, one Sun-like star at 480 pc (G = 13.8 mag) had
   an orbit of about 186 days, with a0 = 3.00 ± 0.22 mas; Gaia's astrometry alone implies a dark companion
   of 12.8 ± 2.0 Msun. Its solution "just narrowly passes" the DR3 cut on parallax precision for its period
   (§9), and Gaia's observations covered only about half of the orbit, so it needed checking.
2. **RV follow-up.** The authors took 39 spectra over four months with six spectrographs (MagE, GMOS,
   X-shooter, HIRES, FEROS, ESI), plus two archival LAMOST spectra. The RVs "span most of the orbit's
   predicted dynamic range and broadly validate the Gaia solution". On their own, without Gaia, "the
   spectroscopic orbit alone sets a minimum companion mass of M2 > 5 M⊙" (abstract, using the G star's mass from its SED); for any visible-star mass the RVs still
   require at least about 4 Msun (§4.3).
3. **Masses.** The visible star's mass, M1 = 0.93 ± 0.05 Msun, comes from fitting its spectral energy
   distribution (SED) and comparing with stellar evolution models. A joint fit of the Gaia astrometry and
   the RVs gives P = 185.59 ± 0.05 d, e = 0.451 ± 0.005 and **M2 = 9.62 ± 0.18 Msun**, consistent with the
   astrometry-only value at the 1.6σ level.
4. **No light from the companion.** The spectra show "no evidence of another luminous star". A companion
   adding only continuum light could provide at most about 10% of the light; the spectral-matching method
   detects companions above about 3% of the light 90% of the time. "Any normal star with a mass exceeding
   ≈0.4 M⊙ would easily be detected", and spectra from the UV to the infrared with GALEX and WISE
   photometry "rule out pathological companions that are hot and small or cool and large". A 5 Msun star
   would be about 500 times more luminous than the whole system.
5. **What else could it be?** Not a normal star (too faint). Not a white dwarf or neutron star (far too
   heavy). Not a group of compact objects: "Scenarios involving more than two objects inside the G star's
   orbit are difficult to assemble and unlikely to be dynamically stable." One or two compact objects
   without a black hole cannot reach several solar masses. What remains is a single black hole, or a pair
   containing one.

*Back of the envelope.* a0 = 3.0 mas at ϖ = 2.08 mas gives a1 ≈ 1.44 au; P = 0.509 yr gives
f_M ≈ 1.44³/0.509² ≈ 11.6 Msun. With M1 ≈ 1 Msun, M2³ = 11.6 (1 + M2)² gives M2 ≈ 13 Msun: of order ten
solar masses, in an object that gives no light.

##### 1.3b Gaia BH2 (El-Badry et al. 2023b)

1. **A candidate with an AstroSpectroSB1 solution.** A red giant (G = 12.3) at 1.16 kpc had a joint
   astrometric and spectroscopic Gaia solution with P = 1352 ± 45 d and an astrometric mass function of
   6.7 ± 0.5 Msun, implying M2 ≈ 8.4 Msun for M1 = 1 Msun.
2. **RV follow-up.** 48 RVs (43 FEROS, 5 UVES) over seven months. "The follow-up RVs are fully consistent
   with the Gaia-only solution." The joint fit gives P = 1276.7 ± 0.6 d and e = 0.518. The Gaia archive
   period (1352 ± 45 d) differs from it by 1.6σ, and the authors' own Gaia-only refit gives 1300 ± 26 d;
   they attribute the difference to their model requiring the spectroscopic and astrometric orbits to share
   the same size (a0 = a1), which the Gaia pipeline does not enforce.
3. **Masses.** M1 = 1.07 ± 0.19 Msun from the giant's temperature and radius with stellar tracks;
   **M2 = 8.9 ± 0.3 Msun** from the joint fit, at an inclination of about 35°. If the orbit were seen
   edge-on instead, the minimum mass would be 2.6 Msun, which the paper notes is still too heavy for a
   white dwarf or neutron star.
4. **No light.** The deepest absorption lines reach about 2% of the continuum, so a companion giving more
   than about 2–3% of the light at 4000 Å would have diluted them; the UV is faint. "A 9Msun main-sequence
   star would outshine the giant at all wavelengths", and "one or more red giant companions would outshine
   the giant in the optical".
5. **What else?** As for BH1, a compact-object cluster "would be difficult to assemble and would rapidly
   become unstable"; the mass "is too large to be a neutron star or white dwarf, or any plausible
   combination of white dwarfs, neutron stars, and faint stars". The conclusion is explicitly conditional:
   "if the Gaia astrometric solution is correct, the companion must be a BH, or a close binary containing a
   BH". The authors argue that a wrong Gaia solution is very unlikely because the independent RVs match its
   predictions. Elsewhere (§6.1) they note that of six candidates from the same astrometric cuts, four
   turned out to have spurious Gaia solutions.

##### 1.3c Gaia BH3 (Gaia Collaboration, Panuzzo et al. 2024)

Found during validation of pre-release Gaia DR4 data (a preliminary pipeline run called NSS 4.1): an old,
metal-poor giant with M1 = 0.76 ± 0.05 Msun in an 11.6-year orbit (P = 4253 ± 99 d, e = 0.73). Gaia's own
RVs "independently validate the astrometric orbit", and the team called a ground-based confirmation
"indispensable to discard the possibility of a spurious solution": UVES, HERMES and SOPHIE radial
velocities agree with the prediction "within 0.5 km s-1", which "confirms the reality and accuracy of the
orbital solution". The combined solution gives a mass function of 31.2 ± 0.8 Msun and
**M2 = 32.70 ± 0.82 Msun**. The spectra "do not show any sign of the presence of a second component", the
observed luminosity is "too low by several orders of magnitude" for a main-sequence companion or a close
pair of them, and the mass is "too large for one neutron star or two neutron stars in a close orbit".
"Although the single BH is the simplest explanation, the hypothesis of an inner binary of two BHs cannot be
excluded." It is the most massive stellar black hole known in the Galaxy.

##### 1.3d Neutron-star candidates (El-Badry et al. 2024)

The same method, pushed to lower companion masses: 21 Sun-like stars in wide orbits (P ≈ 190–1050 d)
whose companions weigh 1.26–1.90 Msun, too much for any normal star or close pair of stars given the light
limits, confirmed with about 300 RVs. The simplest interpretation is neutron stars, though ultramassive
white dwarfs and tight white-dwarf pairs cannot be fully excluded. For this repository the 21 objects
matter as *known positive controls*: a screen for dark companions should recover them.

#### 1.4 What they conclude, and how sure they are

- BH1 and BH2: dark companions of 9.6 and 8.9 Msun that contain at least one black hole; the simplest
  reading is a single black hole. The papers are confident about the mass and the darkness; the
  identification as a black hole rests on no other dark object of that mass being plausible.
- BH3: a 33 Msun dark companion; a single black hole is the simplest explanation, from preliminary data.
- For the authors to be wrong, one of these would have to fail: the orbit is spurious (for BH1 the RVs
  alone already give more than 5 Msun; for BH2 the conclusion is stated conditionally; for BH3 ground-based
  RVs confirm it); or the dark mass is a stable group of three or more neutron stars or white dwarfs
  (argued implausible by BH1 and BH2, not discussed by BH3, not excluded by data).

### Part 2 · The logic of the argument

#### 2.0 Map of the argument

For each system i (1 = BH1, 2 = BH2, 3 = BH3) the same chain:

A. the follow-up RVs agree with the Gaia orbit → the orbit is real;
B. a real orbit and its fitted mass → the companion weighs more than 5 Msun for BH1, at least 8.0 Msun for BH2 and
   at least 30 Msun for BH3 (BH1 also has two routes that do
   not need the joint fit: Gaia's astrometry alone, and the RVs alone);
C. no light, with that mass → no main-sequence star carries the mass → no luminous star of any kind does;
D. at most two objects, and the white-dwarf and neutron-star mass limits → the companion contains a black
   hole.

Conclusion: BH1 ∧ BH2 ∧ BH3 (each companion contains at least one black hole). This is weaker than "a single
black hole", and it matches each paper's own hedged conclusion.

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

Provenance: `[stated <arXiv id>: "quote"]` (the paper says it, quoted), `[implied]` (standard knowledge the
paper relies on without writing it out, with a source), `[reconstructed]` (our addition; exactly the `GAP`
premises).

What Lean checks: that the conclusion follows from these premises (`final`) and is not trivially true
(`final_nontrivial`); that the premises can hold together (`consistent`); that no single premise gives the
conclusion alone (`alone_insufficient`); for each premise, whether it is needed (a countermodel without it)
or redundant; whether the premises the papers actually state are enough (`stated_*`); and whether they are
enough once standard knowledge is added (`explicit_*`; `explicit_insufficient` means a real gap). What Lean
does not check: the physics inside each premise.

Masses are in tenths of a solar mass (whole numbers): `mass1 > 50`, `mass2 ≥ 80`, `mass3 ≥ 300`. The
thresholds are chosen so that each quoted sentence speaks about masses in that range (the BH2 and BH3 sentences
are about the 8.9 and 32.7 Msun companions); BH1 uses the strict "> 5" of its abstract, because two neutron
stars near the maximum neutron-star mass (about 2.2–2.3 Msun, up to about 2.5 allowing for uncertainty) could
reach 5.0. Hedged
sentences ("very unlikely", "unlikely to be dynamically stable") are encoded as plain assertions; each such
premise is named in its stage.

#### 2.1 Stage A · The orbit is real

**Overview.** The joint-fit masses come from the orbit. If Gaia's orbital solution were an artefact, those
masses would mean nothing. The papers settle this with independent radial velocities.

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| `obs_rv1`: BH1 RVs agree with the Gaia orbit | OBS | stated 2209.06833: "The follow-up RVs span most of the orbit's predicted dynamic range and broadly validate the Gaia solution" | §3.2 |
| `mod_rv1`: agreeing RVs → orbit real | MOD | stated 2209.06833: "a catastrophic problem with the astrometric solution is firmly ruled out by the RVs" | §4.2.1 |
| `obs_rv2`: BH2 RVs agree | OBS | stated 2302.07880: "The follow-up RVs are fully consistent with the Gaia-only solution" | §3.7.1 |
| `mod_rv2`: agreeing RVs → orbit real (hedged: "very unlikely") | MOD | stated 2302.07880: "it is very unlikely that the observed RVs would just happen to match the predictions of the Gaia solution if that solution were incorrect" | §4.1 |
| `obs_rv3`: BH3 ground-based RVs agree | OBS | stated 2404.10486: "they are in agreement with the predicted radial velocity within 0.5 km s-1" | §2.3 |
| `mod_rv3`: agreeing RVs → orbit real | MOD | stated 2404.10486: "This result confirms the reality and accuracy of the orbital solution derived from Gaia data" | §2.3 |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| Spurious Gaia solution (BH1) | `mod_rv1`, and independently the RV-only mass (stage B) | yes, §4.2.1, §4.3 |
| Spurious Gaia solution (BH2) | `mod_rv2` | argued unlikely, §4.1; the conclusion is stated conditionally, §4 |
| Spurious solution (BH3) | `mod_rv3` | yes, §2.3 (ground-based RVs) |

**Inference (Lean excerpt).**

```lean
have o1 : v.Orbit1 := p .mod_rv1 (p .obs_rv1)   -- Sec. 3.2, 4.2.1
```

**Critique.** For BH1 this stage is not even needed (2.5). For BH2 the RVs cover a small part of the
1277-day orbit, and the paper's own base rate is sobering (four of six similar candidates had spurious
solutions); the paper keeps its conclusion conditional on the Gaia solution. For BH3 the ground-based RVs
are a direct check of the predicted velocities.

#### 2.2 Stage B · The companion is heavy (> 5, ≥ 8.0, ≥ 30 Msun)

**Overview.** Kepler's third law turns orbit size and period into mass. The papers quote joint-fit masses;
for BH1 there are two further routes: Gaia's astrometry alone (which still needs the orbit to be real), and
the RVs alone, which give a minimum mass for any inclination and do not need the Gaia orbit at all.

**Premises.**

| Premise | Tag | Provenance | Source |
|---|---|---|---|
| `stat_fit1`: fit1 ≥ 9.0 Msun | STAT | stated 2209.06833: "We infer an unseen companion mass M2=9.62±0.18" | §4.1, Table 1 |
| `mod_fit1`: real orbit + fit → mass > 5 | MOD | implied: Kepler's third law with a dark companion, and 9.62 ± 0.18 being far above 5 (textbook, e.g. Murray and Dermott 1999) | — |
| `num_astro1`: astrometry-only mass > 5.0 Msun | NUM | stated 2209.06833: "12.8±2.0" (Table 1, astrometry-only block); recomputed by `run.py` (posterior median), bound to `results/summary.json:post_hoc.R1b_bh1_vs_dr3_only_paper.m2_ours > 5.0` | Table 1 |
| `mod_astro1`: real orbit + astrometric mass → mass > 5 | MOD | implied: Kepler's third law with a dark companion | — |
| `stat_rvmin1`: RV-only minimum mass > 5.0 Msun | STAT | stated 2209.06833: "The spectroscopic orbit alone sets a minimum companion mass of M2 > 5 M⊙" | Abstract, §4.3 |
| `mod_rvmin1`: RV minimum → mass > 5 | MOD | implied: the spectroscopic mass function is a lower limit for any inclination (textbook, e.g. Hilditch 2001) | — |
| `stat_fit2`: fit2 ≥ 8.0 Msun | STAT | stated 2302.07880: "M2 = 8.9 ± 0.3 Msun" | §3.7.3 |
| `mod_fit2`: real orbit + fit → mass ≥ 8.0 | MOD | implied: Kepler's third law with a dark companion and the reported uncertainty | — |
| `stat_fit3`: fit3 ≥ 30.0 Msun | STAT | stated 2404.10486: "implies the presence of a 32.70±0.82 M⊙ BH" | Abstract, Eq. 5 |
| `mod_fit3`: real orbit + fit → mass ≥ 30 | MOD | implied: Kepler's third law with a dark companion and the reported uncertainty; the paper gives the method (Eqs. 2, 5) | §2.2–2.3 |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly? |
|---|---|---|
| The visible star's mass M1 is badly wrong | `stat_fit*` (M2 depends only weakly on M1 here) | yes (BH1 §4.1 prior; BH2 §3.5, §3.5.1 stripped giant disfavoured) |
| Inclination wrong (orbit nearer edge-on) | BH1: `stat_rvmin1` (inclination-free); BH2, BH3: `stat_fit*` | BH2 §4: the edge-on minimum is 2.6 Msun, which our 8.0 Msun threshold does not cover |

**Inference (Lean excerpt).**

```lean
have m1 : v.mass1 > 50 := p .mod_fit1 o1 (p .stat_fit1)   -- Sec. 4.1
```

**Critique.** The BH2 and BH3 thresholds sit about 3σ below the measured values (8.9 ± 0.3 against 8.0;
32.70 ± 0.82 against 30); BH1 uses the RV-only "> 5", far below the joint-fit 9.62 ± 0.18. BH1's RV-only route needs no Gaia orbit but does use the G star's mass from its SED: with no M1 at all the bound is about 4 Msun (§4.3), and 4 Msun would no longer exclude two neutron stars (2 × 2.2 = 4.4). The `mod_fit*`
premises carry more than Kepler: the dark-companion assumption (no light in the photocentre fit) and the
step from a published estimate with its error to a bound on the true mass. For BH2 the 8.0 Msun bound rests
on the Gaia inclination; the paper's inclination-free fallback (2.6 Msun, still above white-dwarf and
neutron-star masses) would need a different stage D and is not encoded.

#### 2.3 Stage C · The mass is not in luminous stars

**Overview.** A star of several solar masses is hundreds of times brighter than the systems observed; the
spectra would show it. The papers' sentences speak first of main-sequence (normal) stars; other luminous
stars are a separate step.

**Premises.**

| Premise | Tag | Provenance | Source |
|---|---|---|---|
| `obs_faint1` | OBS | stated 2209.06833: "no evidence of another luminous star" | §5.1.1 |
| `mod_dark1`: faint + mass > 5 → no normal star carries it | MOD | stated 2209.06833: "any normal star with a mass exceeding ≈0.4 M⊙ would easily be detected in the spectrum" | §8.1 |
| `mod_other1`: … nor any other luminous star | MOD | stated 2209.06833: "This and the GALEX + WISE photometry allow us to rule out pathological companions that are hot and small or cool and large" | §5.1.1 |
| `obs_faint2` | OBS | stated 2302.07880: "A companion contributing more than ≈2% of the total light at 4000-4300 Å would dilute the absorption lines beyond this value and is thus ruled out" | §3.8.1 |
| `mod_dark2`: faint + mass ≥ 8.0 → no main-sequence star (nor a pair) | MOD | implied: mass–luminosity relation (Kippenhahn, Weigert and Weiss 2012); the paper says it for one 9 Msun star: "a 9Msun main-sequence star would outshine the giant at all wavelengths" | §4 |
| `mod_other2` | MOD | implied: non-main-sequence stars of several solar masses are at least as luminous (textbook); the paper states it for red giants ("But one or more red giant companions would outshine the giant in the optical", §4) and limits hot companions with the UV (§3.3) | — |
| `obs_faint3` | OBS | stated 2404.10486: "The spectra do not show any sign of the presence of a second component, nor any emission line" | App. C |
| `mod_dark3` | MOD | stated 2404.10486: "too low by several orders of magnitude to be compatible with the hypothesis that the companion is a main sequence star or even two main sequence stars in a close orbit" | §3 |
| `mod_other3` | MOD | implied: non-main-sequence stars of several solar masses are at least as luminous (textbook, e.g. Kippenhahn, Weigert and Weiss 2012) | — |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly? |
|---|---|---|
| A massive main-sequence star | `mod_dark*` | yes, all three |
| An inner pair of ordinary stars | `mod_dark1`, `mod_dark3` | BH1 (each star > 0.4 Msun would show); BH2 (§4, for the 2.6 Msun case); BH3 yes |
| A giant companion | `mod_other*` | BH2 yes (red giants); BH1 via "cool and large"; BH3 no (textbook step) |
| A rapidly rotating hot star (broad, shallow lines) | `mod_other*`, `obs_faint*` | BH1 rules out "hot and small" companions with UV-to-IR data; BH2 notes rotating secondaries are harder to detect and uses the UV |

**Inference (Lean excerpt).**

```lean
have s1 : v.NoMS1 := p .mod_dark1 (p .obs_faint1) m1      -- Sec. 5.1.1, 8.1
have n1 : v.NoStar1 := p .mod_other1 (p .obs_faint1) s1   -- Sec. 5.1.1
```

**Critique.** Splitting the step keeps each quoted premise no stronger than its sentence. For BH1 the 0.4 Msun limit also covers pairs: two normal stars carrying 5 Msun would include one above 2.5 Msun. The BH3 paper
discusses only main-sequence stars; the extension to other luminous stars is standard stellar physics.

#### 2.4 Stage D · A black hole is required

**Overview.** Once the mass is dark and above these thresholds, the remaining non-black-hole options are white
dwarfs (below 1.4 Msun each) and neutron stars (below about 2.2–2.3 Msun each, 2.5 allowing for uncertainty). One or two of them cannot
exceed 5 Msun (BH1's strict bound), let alone 8 or 30; three or more would be needed. This uses the
measured and equation-of-state maximum neutron-star mass: the causality bound (about 3 Msun; Kalogera and
Baym 1996) would let two neutron stars exceed 5 Msun, so BH1's RV-only route depends on the former.

**Premises.**

| Premise | Tag | Provenance | Source |
|---|---|---|---|
| `mod_few1`: at most two objects (hedged: "unlikely to be dynamically stable") | MOD | stated 2209.06833: "Scenarios involving more than two objects inside the G star's orbit are difficult to assemble and unlikely to be dynamically stable" | §8.2 |
| `lit_ns1`: dark, at most two, > 5 Msun → black hole (no exotic compact objects) | LIT | implied: Chandrasekhar 1931 (white dwarfs); Özel and Freire 2016, arXiv:1603.02698; Rezzolla et al. 2018, arXiv:1711.00314 (neutron stars) | — |
| `mod_few2` (hedged: "difficult to assemble") | MOD | stated 2302.07880: "such a configuration would be difficult to assemble and would rapidly become unstable" | §4 |
| `mod_ns2` | MOD | stated 2302.07880: "is too large to be a neutron star or white dwarf, or any plausible combination of white dwarfs, neutron stars, and faint stars" | §7 item 4 |
| `gap_few3`: at most two objects (BH3) | GAP | reconstructed: the BH3 paper does not discuss three or more compact objects (the argument exists in BH1 §8.2) | — |
| `mod_ns3`: … → neither one nor two neutron stars | MOD | stated 2404.10486: "The estimated mass is also too large for one neutron star or two neutron stars in a close orbit" | §3 |
| `lit_wd3`: no luminous star, no neutron stars, at most two, ≥ 30 Msun → black hole (white dwarfs, white dwarf + neutron star) | LIT | implied: Chandrasekhar 1931; Özel and Freire 2016 | — |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly? |
|---|---|---|
| A single neutron star or white dwarf | `lit_ns1`, `mod_ns2`, `mod_ns3`, `lit_wd3` | yes (BH1 §8.1 names "the maximum neutron star mass" without a number; BH2 §4, §7; BH3 §3) |
| Two compact objects without a black hole | `lit_ns1`, `mod_ns2`, `mod_ns3`, `lit_wd3` | BH2 yes; BH3 for neutron stars only (white dwarfs: textbook step); BH1 implicitly |
| Three or more neutron stars / white dwarfs | `mod_few1`, `mod_few2`, `gap_few3` | BH1, BH2: argued unstable, not excluded by data; BH3: not discussed |
| An inner pair containing a black hole | — | not a rival: the conclusion is "contains a black hole" |

**Inference (Lean excerpt).**

```lean
have b1 : v.BH1 := p .lit_ns1 n1 (p .mod_few1) m1   -- Sec. 8.2 (mass limits implied)
have k3 : v.NoNS3 := p .mod_ns3 n3 (p .gap_few3) m3  -- Sec. 3 (three or more: not discussed)
have b3 : v.BH3 := p .lit_wd3 n3 k3 (p .gap_few3) m3  -- white dwarfs: textbook step
exact ⟨b1, b2, b3⟩
```

**Critique.** The BH1 paper never gives the white-dwarf or neutron-star mass limits as numbers; they are
textbook (`[implied]`). The BH3 paper lists the remaining possibilities as a single black hole, two black
holes, or a black hole plus another compact object, without arguing away three or more compact objects:
that step is our `GAP`. For BH2, `mod_ns2` ("any plausible combination") already covers three or more objects, so it overlaps `mod_few2`; the encoding keeps both.

#### 2.5 What the Lean check found

1. **`explicit_insufficient`: one real gap.** Even with standard knowledge added, the BH3 conclusion
   needs `gap_few3`: the BH3 paper does not exclude three or more non-black-hole compact objects. The
   BH1 and BH2 papers do argue it (as a plausibility statement), so the gap is specific to BH3 and could
   be closed by citing their argument. For a 33 Msun companion it would take more than a dozen neutron
   stars, so the gap is small in practice, but it is a missing step.
2. **`stated_insufficient`.** What the papers write needs textbook knowledge: the Kepler mass relations and
   the step from a published estimate to a bound (`mod_fit*`; BH3 gives its equations but not this step), the inclination-free lower limit from the RV mass function,
   the white-dwarf and neutron-star mass limits for BH1 and the white-dwarf limit for BH3 (`lit_wd3`), the mass–luminosity scaling from the 9 Msun star BH2 names down to 8.0 Msun (`mod_dark2`), and, for BH2 (beyond red giants) and BH3, the
   luminosity of non-main-sequence stars.
3. **BH1 is over-determined.** `obs_rv1`, `mod_rv1`, `stat_fit1`, `mod_fit1`, `num_astro1`, `mod_astro1`,
   `stat_rvmin1` and `mod_rvmin1` are each redundant: the RV-only minimum mass gives stage B without the
   Gaia orbit, and the joint fit gives it without the RV-only bound. This matches the BH1 paper's own
   claim that the RVs require a black-hole-mass companion even without the astrometry. The joint-fit and
   astrometry-only routes are not independent of each other (both need the Gaia orbit); the RV-only route
   is independent of the Gaia orbit. But all three rest on the same follow-up RVs (the joint fit uses them,
   the Gaia orbit is validated by them, the RV-only bound is them): "redundant" means robust to dropping any
   one premise, not robust to a problem in the RV data, and not "Gaia DR3 alone suffices".
4. **Where the argument is weak is physics.** The decisive premises are hedged sentences encoded as
   assertions: `mod_rv2` ("very unlikely"), `mod_few1` and `mod_few2` ("difficult to assemble", "unlikely
   to be dynamically stable"). For BH2 the conclusion is conditional on the Gaia solution in the paper
   itself, and the 8.0 Msun bound depends on the Gaia inclination.
5. **`num_astro1` is a weak link to our results.** It is redundant, so our reproduction failing could not
   change any Lean verdict; and it is bound to the posterior median of our DR3-only mass (13.3 Msun), not a
   lower bound (the 16th percentile, about 11, is stored in a list the binding cannot address). Our DR3
   solution for BH1 is also flagged low-significance by our own labels, and DR3 errors near G ≈ 13.8 are
   underestimated by about 30% (BH1 §4.3.2), which widens the lower tail.
6. **Consistency.** `consistent` holds, but it is a weak check here: there are no negative premises.
7. **Limits.** Lean checks the logical structure under our encoding, not the physics in each premise.
   Uncertainties are folded into integer thresholds (> 5, 9.0, 8.0, 30 Msun); the neutron-star candidate
   paper (1.3d) is not part of the chain.

### Part 3 · What astrolab can test or explore

*Written after implementation (post hoc); not a pre-registration.* The study's actual pre-registration is in
its [README](https://github.com/sudoghut/astrolab/blob/main/studies/001-m04-gaia-dormant-black-holes/README.md)
(sections 1–4, with a DR4 addendum written before the DR4 release).

| Stage / claim | Can we test or explore it? | How | Data (size) | Decision criterion | Result |
|---|---|---|---|---|---|
| B: BH1 mass from Gaia DR3 alone | testable now | Monte Carlo over the full DR3 covariance, M1 = 0.93 | 2 NSS rows, < 10 kB | within 2σ of the published mass | reproduced: 13.3 (+2.9/−2.3) Msun, +1.4σ from 9.62; +0.23σ from the paper's astrometry-only 12.8 |
| B: BH2 mass from Gaia DR3 alone | testable now | same, M1 = 1.07 | as above | within 2σ | reproduced: 8.52 (+0.61/−0.56) Msun, −0.6σ |
| A: is the orbit real? (RV prediction) | testable now (partial) | predicted RV range from the astrometric orbit vs Gaia's `rv_amplitude_robust` | in the vetting query | matches the published RV ranges | reproduced for the six sources in El-Badry et al. 2023a Table E1 |
| Recovery of known dark companions | testable now | server-side screen of all DR3 astrometric orbits (f_M > 0.25 Msun) | 3,343 rows, 0.4 MB | ≥ 19 of the 21 neutron-star candidates recovered | 21/21 (weak test) |
| B for BH3 | testable after Gaia DR4 (2026-12-02) | pre-registered R3 | DR4 query, counted first | within 2σ of 32.70 Msun | pending |
| C: luminosity limits | out of scope | needs spectra | — | — | — |
| D: stability of three or more compact objects | explorable (not decisive) | n-body integrations or literature | — | none - exploration only | not started |

What we found so far: Gaia DR3 alone reproduces the BH1 and BH2 masses, the screen recovers the known dark
companions, and our vetoes leave 51 unexplained candidates in DR3, all giants or low-significance solutions,
so no new dormant black hole around a main-sequence star. The interactive page runs locally with
`python -m astrolab serve`.

### Glossary

| Term | Meaning |
|---|---|
| Astrometry | Measuring positions of stars on the sky. |
| Astrometric mass function f_M | (a0/ϖ)³/P²: what Kepler's law gives from the visible star's orbit alone. |
| Spectroscopic mass function | The same from the RV orbit; a lower limit on the companion mass for any inclination. |
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

- 2026-11-14: first version: parts 1–3, written after the DR3 implementation (T-010); revised after the
  independent referee (per-system mass thresholds, white-dwarf step for BH3, notes on shared RV dependence and
  the weak NUM binding).

### Sources

- El-Badry et al. 2023a, MNRAS 518, 1057, arXiv:2209.06833 (read: v3) [V]
- El-Badry et al. 2023b, MNRAS 521, 4323, arXiv:2302.07880 (read: v2) [V]
- Gaia Collaboration, Panuzzo et al. 2024, A&A 686, L2, arXiv:2404.10486 (read: v2) [V]
- El-Badry et al. 2024, OJAp 7, arXiv:2405.00089 (read: v2) [V]
- Kalogera and Baym 1996, ApJ 470, L61, arXiv:astro-ph/9608059 (causality bound on neutron-star mass);
  Rezzolla, Most and Weih 2018, ApJL 852, L25, arXiv:1711.00314 (maximum neutron-star mass).
- Chandrasekhar 1931, ApJ 74, 81 (white-dwarf maximum mass); Özel and Freire 2016, ARA&A 54, 401,
  arXiv:1603.02698 (neutron-star masses)

---

## 中文

### 第一部分 · 科普详解

#### 1.1 问题与意义

比太阳重得多的恒星，死后会变成黑洞，所以银河系里应该有约一亿个恒星级黑洞。可是我们知道的黑洞几乎都是因为它在"进食"才被发现的：伴星把气体倒向黑洞，气体被加热，发出 X 射线。进食的黑洞很少，也未必有代表性。一个安静地待在普通恒星旁边、没有东西落进去的黑洞，什么也不发出。这样的"休眠"黑洞应该多得多，但只能通过引力发现：可见的恒星绕着一个看不见的东西运动。

2022 年以前，所有声称在普通恒星旁边发现的休眠黑洞，后来都有了别的解释（最常见的是漏掉了一颗更暗的恒星）。这几篇论文回答的问题是：只要把一颗恒星自身的运动测得足够准，能不能证明它看不见的伙伴是黑洞？

#### 1.2 数据

欧洲空间局的 Gaia 卫星多年来反复测量约二十亿颗恒星的位置。双星中的一颗星在天空上不走直线，而是绕着双星的质心画一个小椭圆。Gaia 第三次数据发布（DR3，2022 年 6 月）首次给出约 44 万个双星的拟合轨道（"非单星"星表，NSS）。对天体测量轨道，拟合给出恒星在天空上的椭圆大小（半长轴 a0，单位毫角秒）、周期 P、形状（偏心率 e）和方向，方向由四个称为 Thiele-Innes 常数的数表示。再结合由视差 ϖ 得到的距离，角大小就变成以天文单位计的实际大小。

只凭轨道大小和周期，开普勒第三定律就给出天体测量质量函数 f_M = (a0/ϖ)³ / P²（P 以年计，结果以太阳质量计）。如果伴星不发光，f_M 等于 M2³ / (M1 + M2)²，M1 是可见星的质量，M2 是伴星的质量。由恒星的颜色和亮度知道 M1，就能求出 M2。

论文接着用光谱观测。光谱仪通过吸收线的多普勒位移测量恒星的视向速度（radial velocity, RV），即朝向或离开我们的速度。视向速度从另一个角度看同一个轨道；单独使用时给出光谱质量函数（spectroscopic mass function），无论轨道倾角如何都给出伴星质量的下限。光谱还能看出有没有第二颗星在发光：第二颗星会带来自己的谱线，或者冲淡可见星的谱线。

#### 1.3 一步一步：作者如何从数据走到结论

##### 1.3a Gaia BH1（El-Badry 等 2023a）

1. **Gaia 给出的候选。** 在 DR3 的天体测量轨道中，一颗距离 480 pc、G = 13.8 星等的类太阳恒星有约 186 天的轨道，a0 = 3.00 ± 0.22 毫角秒；只用 Gaia 天体测量，暗伴星质量为 12.8 ± 2.0 M☉。它的解刚好越过 DR3 按周期设定的视差精度门槛（§9），而 Gaia 的观测只覆盖了约半个轨道，所以需要核查。
2. **视向速度后续观测。** 作者在四个月里用六台光谱仪（MagE、GMOS、X-shooter、HIRES、FEROS、ESI）拍了 39 条光谱，另有两条 LAMOST 存档光谱。视向速度覆盖了轨道预期变化范围的大部分，并大体证实了 Gaia 的解。不用 Gaia，单凭光谱轨道就给出伴星质量下限 M2 > 5 M☉（摘要，用到由 SED 得到的 G 型星质量）；无论可见星质量多少，视向速度仍要求至少约 4 M☉（§4.3）。
3. **质量。** 可见星质量 M1 = 0.93 ± 0.05 M☉，来自对其光谱能量分布（SED）的拟合与恒星演化模型的比较。Gaia 天体测量与视向速度联合拟合给出 P = 185.59 ± 0.05 天、e = 0.451 ± 0.005、**M2 = 9.62 ± 0.18 M☉**，与只用天体测量的结果在 1.6σ 水平上一致。
4. **伴星不发光。** 光谱里"没有另一颗发光恒星的迹象"。只贡献连续谱的伴星最多提供约 10% 的光；论文所用的光谱匹配方法对贡献超过约 3% 光的伴星有 90% 的探测率。任何质量超过约 0.4 M☉ 的普通恒星都会在光谱中轻易被看到；从紫外到红外的光谱，加上 GALEX 与 WISE 的测光，排除了"热而小或冷而大"的异常伴星。一颗 5 M☉ 的恒星会比整个系统亮约 500 倍。
5. **还可能是什么？** 不是普通恒星（太暗）。不是白矮星或中子星（太重）。不是一群致密天体：轨道内有两个以上天体的情形难以形成，也不太可能动力学稳定。一两个不含黑洞的致密天体到不了几个太阳质量。剩下的只有单个黑洞，或含有黑洞的一对天体。

*粗略估算。* a0 = 3.0 毫角秒、ϖ = 2.08 毫角秒，得 a1 ≈ 1.44 au；P = 0.509 年，得 f_M ≈ 1.44³/0.509² ≈ 11.6 M☉。取 M1 ≈ 1 M☉，解 M2³ = 11.6 (1 + M2)² 得 M2 ≈ 13 M☉：一个不发光的天体，质量在十倍太阳质量的量级。

##### 1.3b Gaia BH2（El-Badry 等 2023b）

1. **带天体测量加光谱联合解的候选。** 一颗距离 1.16 kpc、G = 12.3 的红巨星有 Gaia 天体测量与光谱联合解（AstroSpectroSB1），P = 1352 ± 45 天，天体测量质量函数 6.7 ± 0.5 M☉，取 M1 = 1 M☉ 时 M2 ≈ 8.4 M☉。
2. **视向速度后续观测。** 七个月内 48 个视向速度（FEROS 43 个、UVES 5 个）。后续视向速度与只用 Gaia 的解完全一致。联合拟合给出 P = 1276.7 ± 0.6 天、e = 0.518。Gaia 档案中的周期（1352 ± 45 天）与之相差 1.6σ，作者自己只用 Gaia 重新拟合得到 1300 ± 26 天；他们把差别归因于自己的模型要求光谱轨道和天体测量轨道大小一致（a0 = a1），而 Gaia 流程没有这样做。
3. **质量。** 由巨星的温度和半径配合演化轨迹得到 M1 = 1.07 ± 0.19 M☉；联合拟合给出 **M2 = 8.9 ± 0.3 M☉**，轨道倾角约 35°。如果轨道其实接近侧向，最小质量是 2.6 M☉，论文指出这对白矮星或中子星仍然太重。
4. **不发光。** 最深的吸收线降到连续谱的约 2%，所以在 4000 Å 处贡献超过约 2–3% 光的伴星会把它们冲淡；紫外也很暗。一颗 9 M☉ 的主序星会在所有波段都比巨星亮，一颗或多颗红巨星伴星会在光学波段比可见星亮。
5. **还可能是什么？** 与 BH1 相同：一群致密天体难以形成，而且很快会变得不稳定；这个质量对中子星或白矮星，或白矮星、中子星与暗星的任何合理组合都太大。结论是有条件的：如果 Gaia 天体测量解是正确的，伴星必定是黑洞，或含有黑洞的密近双星。作者认为 Gaia 解出错的可能性很小，因为独立的视向速度符合它的预测。论文另一处（§6.1）指出，同样筛选条件下的六个候选中，有四个的 Gaia 解后来证明是虚假的。

##### 1.3c Gaia BH3（Gaia 合作组 Panuzzo 等 2024）

在验证 Gaia DR4 预发布数据（一次称为 NSS 4.1 的初步流程运行）时发现：一颗年老、贫金属的巨星，M1 = 0.76 ± 0.05 M☉，轨道周期 11.6 年（P = 4253 ± 99 天，e = 0.73）。Gaia 自己的视向速度独立证实了天体测量轨道，团队还认为地面观测的确认对排除虚假解"不可或缺"：UVES、HERMES 与 SOPHIE 测得的视向速度与预测值相差在 0.5 km/s 以内，证实了 Gaia 轨道解的真实性与准确性。联合解给出质量函数 31.2 ± 0.8 M☉、**M2 = 32.70 ± 0.82 M☉**。光谱没有显示第二个成分的任何迹象，观测到的光度比一颗主序伴星（甚至一对密近主序星）应有的低几个数量级，这个质量对一颗中子星或一对密近中子星都太大。作者认为单个黑洞是最简单的解释，但不能排除内部是一对黑洞。它是银河系已知质量最大的恒星级黑洞。

##### 1.3d 中子星候选（El-Badry 等 2024）

同样的方法推向更低的伴星质量：21 颗处于宽轨道（P ≈ 190–1050 天）的类太阳恒星，伴星质量 1.26–1.90 M☉；在光度限制下，这对任何普通恒星或密近恒星对都太重；用约 300 个视向速度证实。最简单的解释是中子星，但不能完全排除超大质量白矮星和密近双白矮星。对本项目而言，这 21 个天体是已知的正样本对照：寻找暗伴星的筛选应当能把它们找回来。

#### 1.4 结论与把握程度

- BH1 与 BH2：9.6 和 8.9 M☉ 的暗伴星，至少含有一个黑洞；最简单的解读是单个黑洞。论文对质量和不发光很有把握；认定为黑洞依赖于没有其他这种质量的暗天体说得通。
- BH3：33 M☉ 的暗伴星；单个黑洞是最简单的解释，数据是初步的。
- 作者若是错的，需要以下之一成立：轨道是虚假的（BH1 单凭视向速度已给出 5 M☉ 以上；BH2 的结论本来就是条件句；BH3 由地面视向速度证实）；或者暗质量是由三颗以上中子星或白矮星组成的稳定群体（BH1、BH2 论证为不合理，BH3 没有讨论，数据都没有排除）。

### 第二部分 · 论证逻辑

#### 2.0 论证地图

对每个系统 i（1 = BH1，2 = BH2，3 = BH3），都是同样的链条：

A. 后续视向速度与 Gaia 轨道一致 → 轨道是真实的；
B. 真实的轨道和拟合质量 → 伴星质量：BH1 大于 5 M☉，BH2 至少 8.0 M☉，BH3 至少 30 M☉（BH1 另有两条不需要联合拟合的路径：只用 Gaia 天体测量，以及只用视向速度）；
C. 没有光，加上这个质量 → 没有主序星承载这些质量 → 也没有任何其他发光恒星承载；
D. 至多两个天体，加上白矮星与中子星的质量上限 → 伴星含有黑洞。

结论：BH1 ∧ BH2 ∧ BH3（每个伴星都至少含有一个黑洞）。这弱于"单个黑洞"，与各篇论文自己留有余地的结论相符。

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

Lean 检查什么：结论能否由这些前提推出（`final`）且并非恒真（`final_nontrivial`）；前提能否同时成立（`consistent`）；单个前提不能单独推出结论（`alone_insufficient`）；每个前提是必要的（去掉它时的反例模型）还是多余的；论文明说的前提是否足够（`stated_*`）；加上标准知识后是否足够（`explicit_*`，`explicit_insufficient` 即存在真正的缺口）。Lean 不检查每个前提内部的物理是否正确。

质量以十分之一太阳质量为单位（整数）：`mass1 > 50`、`mass2 ≥ 80`、`mass3 ≥ 300`。阈值的选择使每条引文讲的都是这一范围内的质量（BH2、BH3 的句子讲的是 8.9 与 32.7 M☉ 的伴星）；BH1 用摘要中严格的"> 5"，因为两颗接近中子星最大质量（约 2.2–2.3 M☉，考虑不确定度可到约 2.5）的中子星可以达到 5.0。留有余地的句子（"可能性很小"、"不太可能动力学稳定"）被编码为断言；每个这样的前提都在所属环节中点名。

#### 2.1 环节 A · 轨道是真实的

**概述。** 联合拟合的质量来自轨道。如果 Gaia 的轨道解是假象，这些质量就没有意义。论文用独立的视向速度解决这一点。

**前提。**

| 前提（Lean 构造子） | 标签 | 出处性质 | 论文出处 |
|---|---|---|---|
| `obs_rv1`：BH1 的视向速度与 Gaia 轨道一致 | OBS | stated 2209.06833："The follow-up RVs span most of the orbit's predicted dynamic range and broadly validate the Gaia solution" | §3.2 |
| `mod_rv1`：一致的视向速度 → 轨道真实 | MOD | stated 2209.06833："a catastrophic problem with the astrometric solution is firmly ruled out by the RVs" | §4.2.1 |
| `obs_rv2`：BH2 的视向速度一致 | OBS | stated 2302.07880："The follow-up RVs are fully consistent with the Gaia-only solution" | §3.7.1 |
| `mod_rv2`：一致的视向速度 → 轨道真实（留有余地："very unlikely"） | MOD | stated 2302.07880："it is very unlikely that the observed RVs would just happen to match the predictions of the Gaia solution if that solution were incorrect" | §4.1 |
| `obs_rv3`：BH3 的地面视向速度一致 | OBS | stated 2404.10486："they are in agreement with the predicted radial velocity within 0.5 km s-1" | §2.3 |
| `mod_rv3`：一致的视向速度 → 轨道真实 | MOD | stated 2404.10486："This result confirms the reality and accuracy of the orbital solution derived from Gaia data" | §2.3 |

**其他解释（rival explanations）。**

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| Gaia 解是虚假的（BH1） | `mod_rv1`，以及独立的、只用视向速度的质量（环节 B） | 是，§4.2.1、§4.3 |
| Gaia 解是虚假的（BH2） | `mod_rv2` | 论证为可能性很小，§4.1；结论以条件句表述，§4 |
| 虚假解（BH3） | `mod_rv3` | 是，§2.3（地面视向速度） |

**推理（Lean 摘录）。**

```lean
have o1 : v.Orbit1 := p .mod_rv1 (p .obs_rv1)   -- Sec. 3.2, 4.2.1
```

**评析。** 对 BH1，这个环节其实不需要（见 2.5）。对 BH2，视向速度只覆盖 1277 天轨道的一小段，论文自己给出的基础比率也令人警醒（六个类似候选中有四个是虚假解）；论文因此把结论写成以 Gaia 解正确为条件。对 BH3，地面视向速度直接检验了预测的速度。

#### 2.2 环节 B · 伴星质量大（> 5、≥ 8.0、≥ 30 M☉）

**概述。** 开普勒第三定律把轨道大小和周期变成质量。论文给出联合拟合的质量；BH1 还有两条路径：只用 Gaia 天体测量（仍需要轨道真实），以及只用视向速度（给出任意倾角下的最小质量，完全不需要 Gaia 轨道）。

**前提。**

| 前提 | 标签 | 出处性质 | 出处 |
|---|---|---|---|
| `stat_fit1`：fit1 ≥ 9.0 M☉ | STAT | stated 2209.06833："We infer an unseen companion mass M2=9.62±0.18" | §4.1，表 1 |
| `mod_fit1`：真实轨道 + 拟合 → 质量 > 5 | MOD | implied：开普勒第三定律加暗伴星假设，以及 9.62 ± 0.18 远高于 5（教科书，如 Murray 与 Dermott 1999） | — |
| `num_astro1`：只用天体测量的质量 > 5.0 M☉ | NUM | stated 2209.06833："12.8±2.0"（表 1，只用天体测量的一栏）；由 `run.py` 复算（后验中位数），绑定 `results/summary.json:post_hoc.R1b_bh1_vs_dr3_only_paper.m2_ours > 5.0` | 表 1 |
| `mod_astro1`：真实轨道 + 天体测量质量 → 质量 > 5 | MOD | implied：开普勒第三定律加暗伴星假设 | — |
| `stat_rvmin1`：只用视向速度的最小质量 > 5.0 M☉ | STAT | stated 2209.06833："The spectroscopic orbit alone sets a minimum companion mass of M2 > 5 M⊙" | 摘要，§4.3 |
| `mod_rvmin1`：视向速度最小质量 → 质量 > 5 | MOD | implied：光谱质量函数在任何倾角下都是下限（教科书，如 Hilditch 2001） | — |
| `stat_fit2`：fit2 ≥ 8.0 M☉ | STAT | stated 2302.07880："M2 = 8.9 ± 0.3 Msun" | §3.7.3 |
| `mod_fit2`：真实轨道 + 拟合 → 质量 ≥ 8.0 | MOD | implied：开普勒第三定律加暗伴星假设与给出的不确定度 | — |
| `stat_fit3`：fit3 ≥ 30.0 M☉ | STAT | stated 2404.10486："implies the presence of a 32.70±0.82 M⊙ BH" | 摘要，式 5 |
| `mod_fit3`：真实轨道 + 拟合 → 质量 ≥ 30 | MOD | implied：开普勒第三定律加暗伴星假设与给出的不确定度；论文给出了方法（式 2、5） | §2.2–2.3 |

**其他解释。**

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 可见星质量 M1 严重偏差 | `stat_fit*`（这里 M2 对 M1 依赖很弱） | 是（BH1 §4.1 先验；BH2 §3.5，§3.5.1 不支持剥离巨星） |
| 倾角估错（轨道更接近侧向） | BH1：`stat_rvmin1`（与倾角无关）；BH2、BH3：`stat_fit*` | BH2 §4：侧向时最小质量 2.6 M☉，我们 8.0 M☉ 的阈值不覆盖这一情形 |

**推理（Lean 摘录）。**

```lean
have m1 : v.mass1 > 50 := p .mod_fit1 o1 (p .stat_fit1)   -- Sec. 4.1
```

**评析。** BH2、BH3 的阈值比测量值低约 3σ（8.9 ± 0.3 对 8.0；32.70 ± 0.82 对 30）；BH1 用只靠视向速度的"> 5"，远低于联合拟合的 9.62 ± 0.18。BH1 只用视向速度的路径不需要 Gaia 轨道，但用到了由 SED 得到的 G 型星质量：完全不用 M1 时下限约为 4 M☉（§4.3），而 4 M☉ 已不足以排除两颗中子星（2 × 2.2 = 4.4）。`mod_fit*` 前提不只是开普勒定律：还包含暗伴星假设（光心拟合中伴星不发光），以及从带误差的发表值到真实质量下限的一步。对 BH2，8.0 M☉ 的下限依赖 Gaia 的倾角；论文给出的、与倾角无关的退路（2.6 M☉，仍高于白矮星和中子星质量）需要另一个环节 D，本编码没有包含。

#### 2.3 环节 C · 这些质量不在发光恒星中

**概述。** 几倍太阳质量的恒星比观测到的系统亮几百倍，光谱里会看到它。论文的句子首先讲主序（普通）恒星；其他发光恒星是单独的一步。

**前提。**

| 前提 | 标签 | 出处性质 | 出处 |
|---|---|---|---|
| `obs_faint1` | OBS | stated 2209.06833："no evidence of another luminous star" | §5.1.1 |
| `mod_dark1`：不发光 + 质量 > 5 → 没有普通恒星承载 | MOD | stated 2209.06833："any normal star with a mass exceeding ≈0.4 M⊙ would easily be detected in the spectrum" | §8.1 |
| `mod_other1`：……也没有其他发光恒星 | MOD | stated 2209.06833："This and the GALEX + WISE photometry allow us to rule out pathological companions that are hot and small or cool and large" | §5.1.1 |
| `obs_faint2` | OBS | stated 2302.07880："A companion contributing more than ≈2% of the total light at 4000-4300 Å would dilute the absorption lines beyond this value and is thus ruled out" | §3.8.1 |
| `mod_dark2`：不发光 + 质量 ≥ 8.0 → 没有主序星（也没有一对主序星） | MOD | implied：质光关系（mass–luminosity relation；Kippenhahn、Weigert 与 Weiss 2012）；论文对一颗 9 M☉ 的恒星明说："a 9Msun main-sequence star would outshine the giant at all wavelengths" | §4 |
| `mod_other2` | MOD | implied：几个太阳质量的非主序恒星至少同样明亮（教科书）；论文对红巨星明确说明（"But one or more red giant companions would outshine the giant in the optical"，§4），并用紫外限制热的伴星（§3.3） | — |
| `obs_faint3` | OBS | stated 2404.10486："The spectra do not show any sign of the presence of a second component, nor any emission line" | 附录 C |
| `mod_dark3` | MOD | stated 2404.10486："too low by several orders of magnitude to be compatible with the hypothesis that the companion is a main sequence star or even two main sequence stars in a close orbit" | §3 |
| `mod_other3` | MOD | implied：几个太阳质量的非主序恒星至少与同质量主序星一样亮（教科书，如 Kippenhahn、Weigert 与 Weiss 2012） | — |

**其他解释。**

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 一颗大质量主序星 | `mod_dark*` | 是，三篇都排除 |
| 一对普通恒星 | `mod_dark1`、`mod_dark3` | BH1（每颗 > 0.4 M☉ 都会显现）；BH2（§4，针对 2.6 M☉ 的情形）；BH3 是 |
| 一颗巨星伴星 | `mod_other*` | BH2 是（红巨星）；BH1 通过"冷而大"；BH3 否（教科书步骤） |
| 快速自转的热星（谱线宽而浅） | `mod_other*`、`obs_faint*` | BH1 用紫外到红外数据排除"热而小"的伴星；BH2 指出自转快的伴星较难探测，并用紫外加以限制 |

**推理（Lean 摘录）。**

```lean
have s1 : v.NoMS1 := p .mod_dark1 (p .obs_faint1) m1      -- Sec. 5.1.1, 8.1
have n1 : v.NoStar1 := p .mod_other1 (p .obs_faint1) s1   -- Sec. 5.1.1
```

**评析。** 把这一步拆开，使每条引用的前提都不强于原句。对 BH1，0.4 M☉ 的限制也覆盖一对恒星：两颗普通恒星合计 5 M☉ 时，其中必有一颗超过 2.5 M☉。BH3 论文只讨论了主序星；推广到其他发光恒星属于标准的恒星物理。

#### 2.4 环节 D · 必须有黑洞

**概述。** 一旦确定这些质量不发光且超过上述阈值，剩下的非黑洞选项是白矮星（每颗低于 1.4 M☉）和中子星（每颗低于约 2.2–2.3 M☉，考虑不确定度为 2.5）。一颗或两颗都不能超过 5 M☉（BH1 的严格下限），更到不了 8 或 30 M☉，需要三颗以上。这里用的是观测与物态方程（equation of state）给出的中子星最大质量；按因果性上限（约 3 M☉；Kalogera 与 Baym 1996），两颗中子星可以超过 5 M☉，所以 BH1 只用视向速度的路径依赖前者。

**前提。**

| 前提 | 标签 | 出处性质 | 出处 |
|---|---|---|---|
| `mod_few1`：至多两个天体（留有余地："unlikely to be dynamically stable"） | MOD | stated 2209.06833："Scenarios involving more than two objects inside the G star's orbit are difficult to assemble and unlikely to be dynamically stable" | §8.2 |
| `lit_ns1`：不发光、至多两个、> 5 M☉ → 黑洞（没有奇异致密天体） | LIT | implied：Chandrasekhar 1931（白矮星）；Özel 与 Freire 2016，arXiv:1603.02698；Rezzolla 等 2018，arXiv:1711.00314（中子星） | — |
| `mod_few2`（留有余地："difficult to assemble"） | MOD | stated 2302.07880："such a configuration would be difficult to assemble and would rapidly become unstable" | §4 |
| `mod_ns2` | MOD | stated 2302.07880："is too large to be a neutron star or white dwarf, or any plausible combination of white dwarfs, neutron stars, and faint stars" | §7 第 4 条 |
| `gap_few3`：至多两个天体（BH3） | GAP | reconstructed：BH3 论文没有讨论三个以上致密天体（这一论证见 BH1 §8.2） | — |
| `mod_ns3`：…… → 既不是一颗也不是两颗中子星 | MOD | stated 2404.10486："The estimated mass is also too large for one neutron star or two neutron stars in a close orbit" | §3 |
| `lit_wd3`：没有发光恒星、没有中子星、至多两个、≥ 30 M☉ → 黑洞（白矮星、白矮星加中子星） | LIT | implied：Chandrasekhar 1931；Özel 与 Freire 2016 | — |

**其他解释。**

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| 单颗中子星或白矮星 | `lit_ns1`、`mod_ns2`、`mod_ns3`、`lit_wd3` | 是（BH1 §8.1 提到"中子星最大质量"但未给数值；BH2 §4、§7；BH3 §3） |
| 两个不含黑洞的致密天体 | `lit_ns1`、`mod_ns2`、`mod_ns3`、`lit_wd3` | BH2 明确；BH3 只针对中子星（白矮星为教科书步骤）；BH1 隐含 |
| 三个或更多中子星或白矮星 | `mod_few1`、`mod_few2`、`gap_few3` | BH1、BH2：论证为不稳定，但未被数据排除；BH3：未讨论 |
| 内部是含黑洞的一对天体 | — | 不构成反驳：结论是"含有黑洞" |

**推理（Lean 摘录）。**

```lean
have b1 : v.BH1 := p .lit_ns1 n1 (p .mod_few1) m1   -- Sec. 8.2 (mass limits implied)
have k3 : v.NoNS3 := p .mod_ns3 n3 (p .gap_few3) m3  -- Sec. 3 (three or more: not discussed)
have b3 : v.BH3 := p .lit_wd3 n3 k3 (p .gap_few3) m3  -- white dwarfs: textbook step
exact ⟨b1, b2, b3⟩
```

**评析。** BH1 论文从未给出白矮星或中子星质量上限的数值；它们属于教科书知识（`[implied]`）。BH3 论文把剩下的可能列为单个黑洞、两个黑洞、或一个黑洞加另一个致密天体，没有论证排除三个以上的致密天体：这一步是我们的 `GAP`。对 BH2，`mod_ns2`（"任何合理组合"）本身已涵盖三个以上天体，与 `mod_few2` 有重叠；本编码两者都保留。

#### 2.5 Lean 检查发现的问题

1. **`explicit_insufficient`：一个真正的缺口。** 即使加上标准知识，BH3 的结论仍需要 `gap_few3`：BH3 论文没有排除三个以上不含黑洞的致密天体。BH1 和 BH2 论文论证了这一点（作为合理性陈述），所以缺口只在 BH3，引用它们的论证即可补上。对 33 M☉ 的伴星需要十几颗中子星，所以实际影响很小，但它确实是缺失的一步。
2. **`stated_insufficient`。** 论文写出的内容需要教科书知识补充：开普勒质量关系以及从发表值到下限的一步（`mod_fit*`；BH3 给出了方程，但没有这一步）、光谱质量函数给出的与倾角无关的下限、BH1 所需的白矮星与中子星质量上限、BH3 所需的白矮星质量上限（`lit_wd3`）、从 BH2 点名的 9 M☉ 恒星推到 8.0 M☉ 的质光关系（`mod_dark2`），以及 BH2（红巨星之外）与 BH3 所需的非主序恒星的光度。
3. **BH1 是超定的。** `obs_rv1`、`mod_rv1`、`stat_fit1`、`mod_fit1`、`num_astro1`、`mod_astro1`、`stat_rvmin1` 与 `mod_rvmin1` 各自都是多余的：只用视向速度的最小质量不需要 Gaia 轨道就能给出环节 B，联合拟合不需要视向速度下限也能给出。这与 BH1 论文自己的说法一致：即使不用天体测量，视向速度也要求一个黑洞质量的伴星。联合拟合与只用天体测量的两条路径彼此并不独立（都需要 Gaia 轨道）；只用视向速度的路径独立于 Gaia 轨道。但三条路径都依赖同一批后续视向速度（联合拟合用到它们，Gaia 轨道由它们验证，视向速度下限就是它们本身）："多余"的意思是去掉任何一条前提都不影响结论，而不是对视向速度数据本身出问题也稳健，更不是"只用 Gaia DR3 就够"。
4. **薄弱之处在物理。** 起决定作用的前提是被编码为断言的、留有余地的句子：`mod_rv2`（"very unlikely"）、`mod_few1` 与 `mod_few2`（"difficult to assemble"、"unlikely to be dynamically stable"）。BH2 论文本身就把结论写成以 Gaia 解为条件，而且 8.0 M☉ 的下限依赖 Gaia 的倾角。
5. **`num_astro1` 与本项目结果的联系较弱。** 它是多余的前提，所以即使我们的复现失败，也不会改变任何 Lean 结论；它绑定的是我们只用 DR3 的质量的后验中位数（13.3 M☉），而不是下界（第 16 百分位约 11，存在列表里，绑定无法寻址）。我们自己的标签还把 BH1 的 DR3 解标为低显著性，而 G ≈ 13.8 附近 DR3 的误差被低估约 30%（BH1 §4.3.2），这会使下侧尾部更宽。
6. **相容性。** `consistent` 成立，但这里分量不大：没有否定形式的前提。
7. **局限。** Lean 检查的是在我们的编码下的逻辑结构，不检查每个前提内部的物理。不确定度被折算成整数阈值（> 5、9.0、8.0、30 M☉）；中子星候选论文（1.3d）不在链条中。

### 第三部分 · 本项目可检验或探索的环节

*实现后补写（事后，post hoc），不是预注册。* 研究真正的预注册在它的 [README](https://github.com/sudoghut/astrolab/blob/main/studies/001-m04-gaia-dormant-black-holes/README.md) 中（第 1–4 节，另有 DR4 发布前写好的 DR4 附录）。

| 环节 / 结论 | 能否检验或探索 | 方法 | 数据（大小） | 判据 | 结果 |
|---|---|---|---|---|---|
| B：只用 Gaia DR3 求 BH1 质量 | 现在可检验 | 对 DR3 完整协方差做蒙特卡罗，M1 = 0.93 | 2 行 NSS，< 10 kB | 与已发表质量相差 2σ 以内 | 已复现：13.3 (+2.9/−2.3) M☉，与 9.62 相差 +1.4σ；与论文只用天体测量的 12.8 相差 +0.23σ |
| B：只用 Gaia DR3 求 BH2 质量 | 现在可检验 | 同上，M1 = 1.07 | 同上 | 2σ 以内 | 已复现：8.52 (+0.61/−0.56) M☉，−0.6σ |
| A：轨道是否真实（视向速度预测） | 现在可检验（部分） | 由天体测量轨道预测视向速度变化幅度，与 Gaia 的 `rv_amplitude_robust` 比较 | 在否决规则的查询中 | 与已发表的视向速度幅度一致 | El-Badry 等 2023a 表 E1 中的六个源全部复现 |
| 找回已知暗伴星 | 现在可检验 | 在服务器端筛选全部 DR3 天体测量轨道（f_M > 0.25 M☉） | 3,343 行，0.4 MB | 21 个中子星候选中至少找回 19 个 | 21/21（检验偏弱） |
| BH3 的 B | 待 Gaia DR4（2026-12-02） | 预注册的 R3 | DR4 查询，先计数 | 与 32.70 M☉ 相差 2σ 以内 | 待定 |
| C：光度限制 | 不在范围内 | 需要光谱 | — | — | — |
| D：三个以上致密天体的稳定性 | 可探索（不能判决） | n 体模拟或文献 | — | 无——仅供探索 | 尚未开始 |

目前的发现：只用 Gaia DR3 就能复现 BH1 与 BH2 的质量；筛选能找回已知的暗伴星；我们的否决规则在 DR3 中留下 51 个未解释的候选，全部是巨星或低显著性的解，所以没有发现主序星旁边的新休眠黑洞。交互网页在本地用 `python -m astrolab serve` 打开。

### 术语表

| 术语 | 含义 |
|---|---|
| 天体测量（astrometry） | 测量恒星在天空上的位置。 |
| 天体测量质量函数 f_M（astrometric mass function） | (a0/ϖ)³/P²：只凭可见星的轨道由开普勒定律得到的量。 |
| 光谱质量函数（spectroscopic mass function） | 由视向速度轨道得到的同类量；在任何倾角下都是伴星质量的下限。 |
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

- 2026-11-14：第一版：第一至三部分，在 DR3 实现之后补写（T-010）；按独立审稿意见修订（按系统设定质量阈值、BH3 的白矮星一步、三条质量路径共用视向速度的说明、NUM 绑定较弱的说明）。

### 来源

- El-Badry 等 2023a, MNRAS 518, 1057, arXiv:2209.06833（阅读版本 v3）[V]
- El-Badry 等 2023b, MNRAS 521, 4323, arXiv:2302.07880（阅读版本 v2）[V]
- Gaia 合作组 Panuzzo 等 2024, A&A 686, L2, arXiv:2404.10486（阅读版本 v2）[V]
- El-Badry 等 2024, OJAp 7, arXiv:2405.00089（阅读版本 v2）[V]
- Kalogera 与 Baym 1996, ApJ 470, L61, arXiv:astro-ph/9608059（中子星质量的因果性上限）；Rezzolla、Most 与 Weih 2018, ApJL 852, L25, arXiv:1711.00314（中子星最大质量）。
- Chandrasekhar 1931, ApJ 74, 81（白矮星最大质量）；Özel 与 Freire 2016, ARA&A 54, 401, arXiv:1603.02698（中子星质量）
