/-
Argument of the papers, decomposed: Gaia BH1 (El-Badry et al. 2023a, arXiv:2209.06833),
Gaia BH2 (El-Badry et al. 2023b, arXiv:2302.07880) and Gaia BH3 (Gaia Collaboration, Panuzzo
et al. 2024, arXiv:2404.10486). The fourth paper of this study (El-Badry et al. 2024,
arXiv:2405.00089, neutron-star candidates) supplies the study's control sample, not a step of
this argument; it is discussed in the wiki article.

One chain per system i (1 = BH1, 2 = BH2, 3 = BH3):
  follow-up RVs agree with the Gaia orbit  ->  the orbit is real
  real orbit + orbit-fit mass              ->  companion mass at least 5 Msun
      (BH1 also: the RV orbit alone gives a minimum mass above 5 Msun, without the Gaia orbit)
  no light + that mass                     ->  no main-sequence star carries the mass
  ... and no other luminous star either    ->  the mass is not in luminous stars
  at most two objects + compact-object mass limits -> the companion contains a black hole

Rules: AGENTS.md section 2 (paper study, Lean); specification: design/007 section 2.2.
Masses are in tenths of a solar mass (Nat). Quotes follow the arXiv HTML text (math rendered as
plain text). Hedged statements (very unlikely, unlikely to be stable) are encoded as assertions.
-/

namespace Argument

-- FIXED BLOCK A (identical in every study)
inductive Prov where
  | stated
  | implied
  | reconstructed
  deriving DecidableEq
-- END FIXED BLOCK A

/-- The atoms of the argument. -/
structure Vocab where
  /-- BH1: follow-up radial velocities agree with the Gaia DR3 astrometric orbit. -/
  RVok1 : Prop
  /-- BH1: the Gaia orbital solution is real (not spurious). -/
  Orbit1 : Prop
  /-- BH1: published companion mass from the joint astrometry plus RV fit, tenths of Msun. -/
  fit1 : Nat
  /-- BH1: companion mass from the Gaia DR3 astrometry alone, tenths of Msun. -/
  astro1 : Nat
  /-- BH1: minimum companion mass from the RV orbit alone (any inclination, M1 from the SED), tenths of Msun. -/
  rvmin1 : Nat
  /-- BH1: true companion mass, tenths of Msun. -/
  mass1 : Nat
  /-- BH1: spectra and SED show no light from a second luminous star. -/
  Faint1 : Prop
  /-- BH1: no main-sequence (normal) star carries the companion mass. -/
  NoMS1 : Prop
  /-- BH1: the companion mass is not carried by luminous (non-degenerate) stars of any kind. -/
  NoStar1 : Prop
  /-- BH1: the companion consists of at most two objects. -/
  Few1 : Prop
  /-- BH1: the companion contains at least one black hole. -/
  BH1 : Prop
  /-- BH2: follow-up radial velocities agree with the Gaia DR3 orbit. -/
  RVok2 : Prop
  /-- BH2: the Gaia orbital solution is real (not spurious). -/
  Orbit2 : Prop
  /-- BH2: published companion mass from the joint fit, tenths of Msun. -/
  fit2 : Nat
  /-- BH2: true companion mass, tenths of Msun. -/
  mass2 : Nat
  /-- BH2: spectra, SED and UV show no light from a second luminous star. -/
  Faint2 : Prop
  /-- BH2: no main-sequence star (nor a close pair of them) carries the companion mass. -/
  NoMS2 : Prop
  /-- BH2: the companion mass is not carried by luminous (non-degenerate) stars of any kind. -/
  NoStar2 : Prop
  /-- BH2: the companion consists of at most two objects. -/
  Few2 : Prop
  /-- BH2: the companion contains at least one black hole. -/
  BH2 : Prop
  /-- BH3: ground-based radial velocities agree with the predicted orbit. -/
  RVok3 : Prop
  /-- BH3: the Gaia orbital solution is real (not spurious). -/
  Orbit3 : Prop
  /-- BH3: published companion mass from the combined solution, tenths of Msun. -/
  fit3 : Nat
  /-- BH3: true companion mass, tenths of Msun. -/
  mass3 : Nat
  /-- BH3: the spectra show no second component. -/
  Faint3 : Prop
  /-- BH3: no main-sequence star (nor a close pair of them) carries the companion mass. -/
  NoMS3 : Prop
  /-- BH3: the companion mass is not carried by luminous (non-degenerate) stars of any kind. -/
  NoStar3 : Prop
  /-- BH3: the companion consists of at most two objects. -/
  Few3 : Prop
  /-- BH3: the companion contains at least one black hole. -/
  BH3 : Prop

/-- The premises. -/
inductive Field where
  /-- OBS [stated 2209.06833: "The follow-up RVs span most of the orbit's predicted dynamic range and broadly validate the Gaia solution"] Sec. 3.2 -/
  | obs_rv1
  /-- MOD [stated 2209.06833: "a catastrophic problem with the astrometric solution is firmly ruled out by the RVs"] Sec. 4.2.1 -/
  | mod_rv1
  /-- STAT [stated 2209.06833: "We infer an unseen companion mass M2=9.62±0.18"] Sec. 4.1, Table 1 -/
  | stat_fit1
  /-- MOD [implied] mass from the joint orbit fit: Kepler's third law with a dark companion (zero flux ratio), and a 9.62 ± 0.18 estimate being well above 5 Msun (textbook, e.g. Murray and Dermott 1999, Solar System Dynamics) -/
  | mod_fit1
  /-- NUM [stated 2209.06833: "12.8±2.0"] Table 1, astrometry-only block, black hole mass; recomputed from DR3 by run.py (posterior median) NUM[results/summary.json:post_hoc.R1b_bh1_vs_dr3_only_paper.m2_ours >= 5.0] -/
  | num_astro1
  /-- MOD [implied] mass from the astrometric orbit alone: Kepler's third law with a dark companion (textbook, e.g. Murray and Dermott 1999) -/
  | mod_astro1
  /-- STAT [stated 2209.06833: "The spectroscopic orbit alone sets a minimum companion mass of M2 > 5 M⊙"] Abstract; Sec. 4.3 -/
  | stat_rvmin1
  /-- MOD [implied] the spectroscopic mass function gives a lower limit on the companion mass for any inclination, given the luminous-star mass M1 = 0.93 Msun from the SED (textbook, e.g. Hilditch 2001, An Introduction to Close Binary Stars); with no M1 at all the bound is about 4 Msun (Sec. 4.3) -/
  | mod_rvmin1
  /-- OBS [stated 2209.06833: "no evidence of another luminous star"] Sec. 5.1.1 -/
  | obs_faint1
  /-- MOD [stated 2209.06833: "any normal star with a mass exceeding ≈0.4 M⊙ would easily be detected in the spectrum"] Sec. 8.1 -/
  | mod_dark1
  /-- MOD [stated 2209.06833: "This and the GALEX + WISE photometry allow us to rule out pathological companions that are hot and small or cool and large"] Sec. 5.1.1 -/
  | mod_other1
  /-- MOD [stated 2209.06833: "Scenarios involving more than two objects inside the G star's orbit are difficult to assemble and unlikely to be dynamically stable"] Sec. 8.2 -/
  | mod_few1
  /-- LIT [implied] one or two compact objects without a black hole weigh less than 5 Msun: white dwarfs below the Chandrasekhar mass (Chandrasekhar 1931, 1931ApJ....74...81C), neutron stars below about 2.3 Msun (Ozel and Freire 2016, arXiv:1603.02698) -/
  | lit_ns1
  /-- OBS [stated 2302.07880: "The follow-up RVs are fully consistent with the Gaia-only solution"] Sec. 3.7.1 -/
  | obs_rv2
  /-- MOD [stated 2302.07880: "it is very unlikely that the observed RVs would just happen to match the predictions of the Gaia solution if that solution were incorrect"] Sec. 4.1 -/
  | mod_rv2
  /-- STAT [stated 2302.07880: "M2 = 8.9 ± 0.3 Msun"] Sec. 3.7.3, Table 2 -/
  | stat_fit2
  /-- MOD [implied] mass from the joint orbit fit: Kepler's third law with a dark companion and the reported uncertainty (textbook, e.g. Murray and Dermott 1999) -/
  | mod_fit2
  /-- OBS [stated 2302.07880: "A companion contributing more than ≈2% of the total light at 4000-4300 Å would dilute the absorption lines beyond this value and is thus ruled out"] Sec. 3.8.1 -/
  | obs_faint2
  /-- MOD [stated 2302.07880: "a 9Msun main-sequence star would outshine the giant at all wavelengths"] Sec. 4 -/
  | mod_dark2
  /-- MOD [implied] non-main-sequence stars of several solar masses are at least as luminous as main-sequence stars of that mass (textbook, e.g. Kippenhahn, Weigert and Weiss 2012); the BH2 paper states it for red giants (Sec. 4) and limits hot companions with the UV (Sec. 3.3) -/
  | mod_other2
  /-- MOD [stated 2302.07880: "such a configuration would be difficult to assemble and would rapidly become unstable"] Sec. 4 -/
  | mod_few2
  /-- MOD [stated 2302.07880: "is too large to be a neutron star or white dwarf, or any plausible combination of white dwarfs, neutron stars, and faint stars"] Sec. 7, item 4 -/
  | mod_ns2
  /-- OBS [stated 2404.10486: "they are in agreement with the predicted radial velocity within 0.5 km s-1"] Sec. 2.3 -/
  | obs_rv3
  /-- MOD [stated 2404.10486: "This result confirms the reality and accuracy of the orbital solution derived from Gaia data"] Sec. 2.3 -/
  | mod_rv3
  /-- STAT [stated 2404.10486: "implies the presence of a 32.70±0.82 M⊙ BH"] Abstract, Eq. 5 -/
  | stat_fit3
  /-- MOD [stated 2404.10486: "can be used to solve for the mass of the dark companion"] Sec. 2.2-2.3 (Eqs. 2, 5); the step from the published 32.70 ± 0.82 to a bound of 5 Msun is the same textbook step as in mod_fit1 -/
  | mod_fit3
  /-- OBS [stated 2404.10486: "The spectra do not show any sign of the presence of a second component, nor any emission line"] Appendix C -/
  | obs_faint3
  /-- MOD [stated 2404.10486: "too low by several orders of magnitude to be compatible with the hypothesis that the companion is a main sequence star or even two main sequence stars in a close orbit"] Sec. 3 -/
  | mod_dark3
  /-- MOD [implied] non-degenerate stars of several solar masses in later phases (giants, stripped stars) are at least as luminous as main-sequence stars of that mass (textbook, e.g. Kippenhahn, Weigert and Weiss 2012, Stellar Structure and Evolution) -/
  | mod_other3
  /-- GAP [reconstructed] three or more compact objects inside the orbit are excluded; the BH3 paper does not discuss them (the argument exists in El-Badry et al. 2023a, arXiv:2209.06833, Sec. 8.2) -/
  | gap_few3
  /-- MOD [stated 2404.10486: "The estimated mass is also too large for one neutron star or two neutron stars in a close orbit"] Sec. 3 -/
  | mod_ns3
  deriving DecidableEq, Repr

def prov : Field → Prov
  | .obs_rv1 => .stated
  | .mod_rv1 => .stated
  | .stat_fit1 => .stated
  | .mod_fit1 => .implied
  | .num_astro1 => .stated
  | .mod_astro1 => .implied
  | .stat_rvmin1 => .stated
  | .mod_rvmin1 => .implied
  | .obs_faint1 => .stated
  | .mod_dark1 => .stated
  | .mod_other1 => .stated
  | .mod_few1 => .stated
  | .lit_ns1 => .implied
  | .obs_rv2 => .stated
  | .mod_rv2 => .stated
  | .stat_fit2 => .stated
  | .mod_fit2 => .implied
  | .obs_faint2 => .stated
  | .mod_dark2 => .stated
  | .mod_other2 => .implied
  | .mod_few2 => .stated
  | .mod_ns2 => .stated
  | .obs_rv3 => .stated
  | .mod_rv3 => .stated
  | .stat_fit3 => .stated
  | .mod_fit3 => .stated
  | .obs_faint3 => .stated
  | .mod_dark3 => .stated
  | .mod_other3 => .implied
  | .gap_few3 => .reconstructed
  | .mod_ns3 => .stated

def prem : Field → Vocab → Prop
  | .obs_rv1, v => v.RVok1
  | .mod_rv1, v => v.RVok1 → v.Orbit1
  | .stat_fit1, v => v.fit1 ≥ 90
  | .mod_fit1, v => v.Orbit1 → v.fit1 ≥ 90 → v.mass1 ≥ 50
  | .num_astro1, v => v.astro1 ≥ 50
  | .mod_astro1, v => v.Orbit1 → v.astro1 ≥ 50 → v.mass1 ≥ 50
  | .stat_rvmin1, v => v.rvmin1 ≥ 50
  | .mod_rvmin1, v => v.rvmin1 ≥ 50 → v.mass1 ≥ 50
  | .obs_faint1, v => v.Faint1
  | .mod_dark1, v => v.Faint1 → v.mass1 ≥ 50 → v.NoMS1
  | .mod_other1, v => v.Faint1 → v.NoMS1 → v.NoStar1
  | .mod_few1, v => v.Few1
  | .lit_ns1, v => v.NoStar1 → v.Few1 → v.mass1 ≥ 50 → v.BH1
  | .obs_rv2, v => v.RVok2
  | .mod_rv2, v => v.RVok2 → v.Orbit2
  | .stat_fit2, v => v.fit2 ≥ 80
  | .mod_fit2, v => v.Orbit2 → v.fit2 ≥ 80 → v.mass2 ≥ 50
  | .obs_faint2, v => v.Faint2
  | .mod_dark2, v => v.Faint2 → v.mass2 ≥ 50 → v.NoMS2
  | .mod_other2, v => v.Faint2 → v.NoMS2 → v.NoStar2
  | .mod_few2, v => v.Few2
  | .mod_ns2, v => v.NoStar2 → v.Few2 → v.mass2 ≥ 50 → v.BH2
  | .obs_rv3, v => v.RVok3
  | .mod_rv3, v => v.RVok3 → v.Orbit3
  | .stat_fit3, v => v.fit3 ≥ 300
  | .mod_fit3, v => v.Orbit3 → v.fit3 ≥ 300 → v.mass3 ≥ 50
  | .obs_faint3, v => v.Faint3
  | .mod_dark3, v => v.Faint3 → v.mass3 ≥ 50 → v.NoMS3
  | .mod_other3, v => v.Faint3 → v.NoMS3 → v.NoStar3
  | .gap_few3, v => v.Few3
  | .mod_ns3, v => v.NoStar3 → v.Few3 → v.mass3 ≥ 50 → v.BH3

/-- [stated 2209.06833: "We find no plausible astrophysical scenario that can explain the orbit and does not involve a black hole"] Abstract;
[stated 2302.07880: "We conclude that if the Gaia astrometric solution is correct, the companion must be a BH, or a close binary containing a BH"] Sec. 4;
[stated 2404.10486: "Although the single BH is the simplest explanation, the hypothesis of an inner binary of two BHs cannot be excluded"] Sec. 3 -/
def Conclusion (v : Vocab) : Prop := v.BH1 ∧ v.BH2 ∧ v.BH3

-- FIXED BLOCK B (identical in every study)
def Premises (v : Vocab) : Prop := ∀ f, prem f v
def Without (g : Field) (v : Vocab) : Prop := ∀ f, f ≠ g → prem f v
def Stated (v : Vocab) : Prop := ∀ f, prov f = .stated → prem f v
def Explicit (v : Vocab) : Prop := ∀ f, prov f ≠ .reconstructed → prem f v
-- END FIXED BLOCK B

/-- A model in which every premise and the conclusion hold; countermodels change a few fields. -/
def full : Vocab :=
  { RVok1 := True, Orbit1 := True, fit1 := 90, astro1 := 50, rvmin1 := 50, mass1 := 50,
    Faint1 := True, NoMS1 := True, NoStar1 := True, Few1 := True, BH1 := True,
    RVok2 := True, Orbit2 := True, fit2 := 80, mass2 := 50, Faint2 := True,
    NoMS2 := True, NoStar2 := True, Few2 := True, BH2 := True,
    RVok3 := True, Orbit3 := True, fit3 := 300, mass3 := 50, Faint3 := True,
    NoMS3 := True, NoStar3 := True, Few3 := True, BH3 := True }

/-- The papers' chains, step by step. -/
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  -- BH1 (El-Badry et al. 2023a)
  have o1 : v.Orbit1 := p .mod_rv1 (p .obs_rv1)                 -- Sec. 3.2, 4.2.1
  have m1 : v.mass1 ≥ 50 := p .mod_fit1 o1 (p .stat_fit1)       -- Sec. 4.1
  have s1 : v.NoMS1 := p .mod_dark1 (p .obs_faint1) m1          -- Sec. 5.1.1, 8.1
  have n1 : v.NoStar1 := p .mod_other1 (p .obs_faint1) s1       -- Sec. 5.1.1
  have b1 : v.BH1 := p .lit_ns1 n1 (p .mod_few1) m1             -- Sec. 8.2 (mass limits implied)
  -- BH2 (El-Badry et al. 2023b)
  have o2 : v.Orbit2 := p .mod_rv2 (p .obs_rv2)                 -- Sec. 3.7.1, 4.1
  have m2 : v.mass2 ≥ 50 := p .mod_fit2 o2 (p .stat_fit2)       -- Sec. 3.7.3
  have s2 : v.NoMS2 := p .mod_dark2 (p .obs_faint2) m2          -- Sec. 3.8.1, 4
  have n2 : v.NoStar2 := p .mod_other2 (p .obs_faint2) s2       -- Sec. 4
  have b2 : v.BH2 := p .mod_ns2 n2 (p .mod_few2) m2             -- Sec. 4, 7
  -- BH3 (Gaia Collaboration, Panuzzo et al. 2024)
  have o3 : v.Orbit3 := p .mod_rv3 (p .obs_rv3)                 -- Sec. 2.3
  have m3 : v.mass3 ≥ 50 := p .mod_fit3 o3 (p .stat_fit3)       -- Sec. 2.2, Eq. 5
  have s3 : v.NoMS3 := p .mod_dark3 (p .obs_faint3) m3          -- App. C, Sec. 3
  have n3 : v.NoStar3 := p .mod_other3 (p .obs_faint3) s3       -- textbook step
  have b3 : v.BH3 := p .mod_ns3 n3 (p .gap_few3) m3             -- Sec. 3 (three or more: not discussed)
  exact ⟨b1, b2, b3⟩

theorem final_nontrivial : ¬ ∀ v : Vocab, Conclusion v :=
  fun h => (h { full with BH1 := False }).1

theorem consistent : ∃ v, Premises v :=
  ⟨full, by intro f; cases f <;> simp [prem, full]⟩

theorem alone_insufficient : ∀ g, ¬ ∀ v, prem g v → Conclusion v := by
  intro g h
  cases g
  case mod_ns3 => exact (h { full with BH1 := False } (by simp [prem, full])).1
  all_goals exact (h { full with BH3 := False } (by simp [prem, full])).2.2

/-- The premises that give BH1's mass (three routes: joint fit, astrometry alone, RVs alone). -/
def massRoute1 : Field → Bool
  | .obs_rv1 => true
  | .mod_rv1 => true
  | .stat_fit1 => true
  | .mod_fit1 => true
  | .num_astro1 => true
  | .mod_astro1 => true
  | .stat_rvmin1 => true
  | .mod_rvmin1 => true
  | _ => false

/-- Everything after BH1's mass step, given that mass and every premise outside the mass routes. -/
theorem tail (v : Vocab) (q : ∀ f, massRoute1 f = false → prem f v) (m1 : v.mass1 ≥ 50) :
    Conclusion v := by
  have s1 : v.NoMS1 := q .mod_dark1 rfl (q .obs_faint1 rfl) m1
  have n1 : v.NoStar1 := q .mod_other1 rfl (q .obs_faint1 rfl) s1
  have o2 : v.Orbit2 := q .mod_rv2 rfl (q .obs_rv2 rfl)
  have m2 : v.mass2 ≥ 50 := q .mod_fit2 rfl o2 (q .stat_fit2 rfl)
  have s2 : v.NoMS2 := q .mod_dark2 rfl (q .obs_faint2 rfl) m2
  have n2 : v.NoStar2 := q .mod_other2 rfl (q .obs_faint2 rfl) s2
  have o3 : v.Orbit3 := q .mod_rv3 rfl (q .obs_rv3 rfl)
  have m3 : v.mass3 ≥ 50 := q .mod_fit3 rfl o3 (q .stat_fit3 rfl)
  have s3 : v.NoMS3 := q .mod_dark3 rfl (q .obs_faint3 rfl) m3
  have n3 : v.NoStar3 := q .mod_other3 rfl (q .obs_faint3 rfl) s3
  exact ⟨q .lit_ns1 rfl n1 (q .mod_few1 rfl) m1,
         q .mod_ns2 rfl n2 (q .mod_few2 rfl) m2,
         q .mod_ns3 rfl n3 (q .gap_few3 rfl) m3⟩

-- BH1's mass is over-determined: each route premise is redundant.

theorem obs_rv1_redundant : ∀ v, Without .obs_rv1 v → Conclusion v := fun v p =>
  tail v (fun f hf => p f (by intro e; subst e; simp [massRoute1] at hf))
    (p .mod_rvmin1 (by decide) (p .stat_rvmin1 (by decide)))

theorem mod_rv1_redundant : ∀ v, Without .mod_rv1 v → Conclusion v := fun v p =>
  tail v (fun f hf => p f (by intro e; subst e; simp [massRoute1] at hf))
    (p .mod_rvmin1 (by decide) (p .stat_rvmin1 (by decide)))

theorem stat_fit1_redundant : ∀ v, Without .stat_fit1 v → Conclusion v := fun v p =>
  tail v (fun f hf => p f (by intro e; subst e; simp [massRoute1] at hf))
    (p .mod_rvmin1 (by decide) (p .stat_rvmin1 (by decide)))

theorem mod_fit1_redundant : ∀ v, Without .mod_fit1 v → Conclusion v := fun v p =>
  tail v (fun f hf => p f (by intro e; subst e; simp [massRoute1] at hf))
    (p .mod_rvmin1 (by decide) (p .stat_rvmin1 (by decide)))

theorem num_astro1_redundant : ∀ v, Without .num_astro1 v → Conclusion v := fun v p =>
  tail v (fun f hf => p f (by intro e; subst e; simp [massRoute1] at hf))
    (p .mod_rvmin1 (by decide) (p .stat_rvmin1 (by decide)))

theorem mod_astro1_redundant : ∀ v, Without .mod_astro1 v → Conclusion v := fun v p =>
  tail v (fun f hf => p f (by intro e; subst e; simp [massRoute1] at hf))
    (p .mod_rvmin1 (by decide) (p .stat_rvmin1 (by decide)))

theorem stat_rvmin1_redundant : ∀ v, Without .stat_rvmin1 v → Conclusion v := fun v p =>
  tail v (fun f hf => p f (by intro e; subst e; simp [massRoute1] at hf))
    (p .mod_fit1 (by decide) (p .mod_rv1 (by decide) (p .obs_rv1 (by decide))) (p .stat_fit1 (by decide)))

theorem mod_rvmin1_redundant : ∀ v, Without .mod_rvmin1 v → Conclusion v := fun v p =>
  tail v (fun f hf => p f (by intro e; subst e; simp [massRoute1] at hf))
    (p .mod_fit1 (by decide) (p .mod_rv1 (by decide) (p .obs_rv1 (by decide))) (p .stat_fit1 (by decide)))

-- Every other premise is needed: a countermodel breaks its system's chain at that link.

theorem obs_faint1_needed : ¬ ∀ v, Without .obs_faint1 v → Conclusion v := fun h =>
  (h { full with Faint1 := False, NoMS1 := False, NoStar1 := False, BH1 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

theorem mod_dark1_needed : ¬ ∀ v, Without .mod_dark1 v → Conclusion v := fun h =>
  (h { full with NoMS1 := False, NoStar1 := False, BH1 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

theorem mod_other1_needed : ¬ ∀ v, Without .mod_other1 v → Conclusion v := fun h =>
  (h { full with NoStar1 := False, BH1 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

theorem mod_few1_needed : ¬ ∀ v, Without .mod_few1 v → Conclusion v := fun h =>
  (h { full with Few1 := False, BH1 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

theorem lit_ns1_needed : ¬ ∀ v, Without .lit_ns1 v → Conclusion v := fun h =>
  (h { full with BH1 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

theorem obs_rv2_needed : ¬ ∀ v, Without .obs_rv2 v → Conclusion v := fun h =>
  (h { full with RVok2 := False, Orbit2 := False, mass2 := 0, NoMS2 := False, NoStar2 := False, BH2 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.1

theorem mod_rv2_needed : ¬ ∀ v, Without .mod_rv2 v → Conclusion v := fun h =>
  (h { full with Orbit2 := False, mass2 := 0, NoMS2 := False, NoStar2 := False, BH2 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.1

theorem stat_fit2_needed : ¬ ∀ v, Without .stat_fit2 v → Conclusion v := fun h =>
  (h { full with fit2 := 0, mass2 := 0, NoMS2 := False, NoStar2 := False, BH2 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.1

theorem mod_fit2_needed : ¬ ∀ v, Without .mod_fit2 v → Conclusion v := fun h =>
  (h { full with mass2 := 0, NoMS2 := False, NoStar2 := False, BH2 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.1

theorem obs_faint2_needed : ¬ ∀ v, Without .obs_faint2 v → Conclusion v := fun h =>
  (h { full with Faint2 := False, NoMS2 := False, NoStar2 := False, BH2 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.1

theorem mod_dark2_needed : ¬ ∀ v, Without .mod_dark2 v → Conclusion v := fun h =>
  (h { full with NoMS2 := False, NoStar2 := False, BH2 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.1

theorem mod_other2_needed : ¬ ∀ v, Without .mod_other2 v → Conclusion v := fun h =>
  (h { full with NoStar2 := False, BH2 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.1

theorem mod_few2_needed : ¬ ∀ v, Without .mod_few2 v → Conclusion v := fun h =>
  (h { full with Few2 := False, BH2 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.1

theorem mod_ns2_needed : ¬ ∀ v, Without .mod_ns2 v → Conclusion v := fun h =>
  (h { full with BH2 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.1

theorem obs_rv3_needed : ¬ ∀ v, Without .obs_rv3 v → Conclusion v := fun h =>
  (h { full with RVok3 := False, Orbit3 := False, mass3 := 0, NoMS3 := False, NoStar3 := False, BH3 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2

theorem mod_rv3_needed : ¬ ∀ v, Without .mod_rv3 v → Conclusion v := fun h =>
  (h { full with Orbit3 := False, mass3 := 0, NoMS3 := False, NoStar3 := False, BH3 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2

theorem stat_fit3_needed : ¬ ∀ v, Without .stat_fit3 v → Conclusion v := fun h =>
  (h { full with fit3 := 0, mass3 := 0, NoMS3 := False, NoStar3 := False, BH3 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2

theorem mod_fit3_needed : ¬ ∀ v, Without .mod_fit3 v → Conclusion v := fun h =>
  (h { full with mass3 := 0, NoMS3 := False, NoStar3 := False, BH3 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2

theorem obs_faint3_needed : ¬ ∀ v, Without .obs_faint3 v → Conclusion v := fun h =>
  (h { full with Faint3 := False, NoMS3 := False, NoStar3 := False, BH3 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2

theorem mod_dark3_needed : ¬ ∀ v, Without .mod_dark3 v → Conclusion v := fun h =>
  (h { full with NoMS3 := False, NoStar3 := False, BH3 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2

theorem mod_other3_needed : ¬ ∀ v, Without .mod_other3 v → Conclusion v := fun h =>
  (h { full with NoStar3 := False, BH3 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2

theorem gap_few3_needed : ¬ ∀ v, Without .gap_few3 v → Conclusion v := fun h =>
  (h { full with Few3 := False, BH3 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2

theorem mod_ns3_needed : ¬ ∀ v, Without .mod_ns3 v → Conclusion v := fun h =>
  (h { full with BH3 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2

/-- What the papers write is not enough: they rely on textbook mass determinations, on the
white-dwarf and neutron-star mass limits (BH1 never gives them as numbers) and, for BH3, on the
luminosity of non-main-sequence stars. -/
theorem stated_insufficient : ¬ ∀ v, Stated v → Conclusion v := fun h =>
  (h { full with BH1 := False } (by intro f hf; cases f <;> simp_all [prov, prem, full])).1

/-- Even with standard knowledge the argument has a gap: the BH3 paper does not exclude three or
more compact objects. The BH1 and BH2 papers argue it (as a plausibility statement). -/
theorem explicit_insufficient : ¬ ∀ v, Explicit v → Conclusion v := fun h =>
  (h { full with Few3 := False, BH3 := False }
    (by intro f hf; cases f <;> simp_all [prov, prem, full])).2.2

end Argument
