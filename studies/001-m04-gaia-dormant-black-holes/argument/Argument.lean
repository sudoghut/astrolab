/-
Argument of the papers, decomposed: Gaia BH1 (El-Badry et al. 2023a, arXiv:2209.06833),
Gaia BH2 (El-Badry et al. 2023b, arXiv:2302.07880) and Gaia BH3 (Gaia Collaboration, Panuzzo
et al. 2024, arXiv:2404.10486). The fourth paper of this study (El-Badry et al. 2024,
arXiv:2405.00089, neutron-star candidates) supplies the study's control sample, not a step of
this argument; it is discussed in the wiki article.

One chain per system i (1 = BH1, 2 = BH2, 3 = BH3):
  follow-up RVs agree with the Gaia orbit  ->  the orbit is real
  real orbit + orbit-fit mass              ->  companion mass at least 5 Msun
  no light from a companion + that mass    ->  the mass is not in luminous stars
  at most two objects + maximum NS mass    ->  the companion contains a black hole

Rules: AGENTS.md section 2 (paper study, Lean); specification: design/007 section 2.2.
Masses are in tenths of a solar mass (Nat). Quotes follow the arXiv HTML text.
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
  /-- BH1: true companion mass, tenths of Msun. -/
  mass1 : Nat
  /-- BH1: spectra and SED show no light from a second luminous star. -/
  Faint1 : Prop
  /-- BH1: the companion mass is not carried by luminous (non-degenerate) stars. -/
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
  /-- BH2: the companion mass is not carried by luminous (non-degenerate) stars. -/
  NoStar2 : Prop
  /-- BH2: the companion consists of at most two objects. -/
  Few2 : Prop
  /-- BH2: the companion contains at least one black hole. -/
  BH2 : Prop
  /-- BH3: Gaia RVS radial velocities agree with the astrometric orbit. -/
  RVok3 : Prop
  /-- BH3: the Gaia orbital solution is real (not spurious). -/
  Orbit3 : Prop
  /-- BH3: published companion mass from the combined solution, tenths of Msun. -/
  fit3 : Nat
  /-- BH3: true companion mass, tenths of Msun. -/
  mass3 : Nat
  /-- BH3: the spectra show no second component. -/
  Faint3 : Prop
  /-- BH3: the companion mass is not carried by luminous (non-degenerate) stars. -/
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
  /-- MOD [implied] Kepler's third law: a joint orbit fit measures the companion mass when the orbit is real (textbook, e.g. Murray and Dermott 1999, Solar System Dynamics) -/
  | mod_fit1
  /-- NUM [stated 2209.06833: "12.8±2.0"] Table 1, astrometry-only block, black hole mass; recomputed from DR3 by run.py NUM[results/summary.json:post_hoc.R1b_bh1_vs_dr3_only_paper.m2_ours >= 5.0] -/
  | num_astro1
  /-- MOD [implied] Kepler's third law applied to the astrometric orbit alone gives the companion mass when the orbit is real (textbook, e.g. Murray and Dermott 1999) -/
  | mod_astro1
  /-- OBS [stated 2209.06833: "no evidence of another luminous star"] Sec. 5.1.1 -/
  | obs_faint1
  /-- MOD [stated 2209.06833: "any normal star with a mass exceeding ≈0.4 M⊙ would easily be detected in the spectrum"] Sec. 8.1 -/
  | mod_dark1
  /-- MOD [stated 2209.06833: "Scenarios involving more than two objects inside the G star's orbit are difficult to assemble and unlikely to be dynamically stable"] Sec. 8.2 -/
  | mod_few1
  /-- LIT [implied] two non-black-hole compact objects weigh less than 5 Msun: neutron-star masses stay below about 2.3 Msun, Ozel and Freire 2016, ARA&A 54, 401, arXiv:1603.02698 -/
  | lit_ns1
  /-- OBS [stated 2302.07880: "The follow-up RVs are fully consistent with the Gaia-only solution"] Sec. 3.7.1 -/
  | obs_rv2
  /-- MOD [stated 2302.07880: "it is very unlikely that the observed RVs would just happen to match the predictions of the Gaia solution if that solution were incorrect"] Sec. 4.1 -/
  | mod_rv2
  /-- STAT [stated 2302.07880: "M2 = 8.9 ± 0.3 Msun"] Sec. 3.7.3, Table 2 -/
  | stat_fit2
  /-- MOD [implied] Kepler's third law: a joint orbit fit measures the companion mass when the orbit is real (textbook, e.g. Murray and Dermott 1999) -/
  | mod_fit2
  /-- OBS [stated 2302.07880: "A companion contributing more than ≈2% of the total light at 4000-4300 Å would dilute the absorption lines beyond this value and is thus ruled out"] Sec. 3.8.1 -/
  | obs_faint2
  /-- MOD [stated 2302.07880: "a 9Msun main-sequence star would outshine the giant at all wavelengths"] Sec. 4 -/
  | mod_dark2
  /-- MOD [stated 2302.07880: "such a configuration would be difficult to assemble and would rapidly become unstable"] Sec. 4 -/
  | mod_few2
  /-- LIT [implied] two non-black-hole compact objects weigh less than 5 Msun: Ozel and Freire 2016, arXiv:1603.02698 -/
  | lit_ns2
  /-- OBS [stated 2404.10486: "Gaia radial velocities independently validate the astrometric orbit"] Abstract -/
  | obs_rv3
  /-- MOD [implied] independent radial velocities that match the astrometric orbit make a spurious solution very unlikely, El-Badry et al. 2023b, arXiv:2302.07880, Sec. 4.1 -/
  | mod_rv3
  /-- STAT [stated 2404.10486: "implies the presence of a 32.70±0.82 M⊙ BH"] Abstract, Eq. 5 -/
  | stat_fit3
  /-- MOD [implied] Kepler's third law: the combined orbit fit measures the companion mass when the orbit is real (textbook, e.g. Murray and Dermott 1999) -/
  | mod_fit3
  /-- OBS [stated 2404.10486: "The spectra do not show any sign of the presence of a second component, nor any emission line"] Appendix C -/
  | obs_faint3
  /-- MOD [stated 2404.10486: "too low by several orders of magnitude to be compatible with the hypothesis that the companion is a main sequence star"] Sec. 3 -/
  | mod_dark3
  /-- MOD [implied] more than two objects inside the orbit are hard to assemble and unstable, El-Badry et al. 2023a, arXiv:2209.06833, Sec. 8.2 -/
  | mod_few3
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
  | .obs_faint1 => .stated
  | .mod_dark1 => .stated
  | .mod_few1 => .stated
  | .lit_ns1 => .implied
  | .obs_rv2 => .stated
  | .mod_rv2 => .stated
  | .stat_fit2 => .stated
  | .mod_fit2 => .implied
  | .obs_faint2 => .stated
  | .mod_dark2 => .stated
  | .mod_few2 => .stated
  | .lit_ns2 => .implied
  | .obs_rv3 => .stated
  | .mod_rv3 => .implied
  | .stat_fit3 => .stated
  | .mod_fit3 => .implied
  | .obs_faint3 => .stated
  | .mod_dark3 => .stated
  | .mod_few3 => .implied
  | .mod_ns3 => .stated

def prem : Field → Vocab → Prop
  | .obs_rv1, v => v.RVok1
  | .mod_rv1, v => v.RVok1 → v.Orbit1
  | .stat_fit1, v => v.fit1 ≥ 90
  | .mod_fit1, v => v.Orbit1 → v.fit1 ≥ 90 → v.mass1 ≥ 50
  | .num_astro1, v => v.astro1 ≥ 50
  | .mod_astro1, v => v.Orbit1 → v.astro1 ≥ 50 → v.mass1 ≥ 50
  | .obs_faint1, v => v.Faint1
  | .mod_dark1, v => v.Faint1 → v.mass1 ≥ 50 → v.NoStar1
  | .mod_few1, v => v.Few1
  | .lit_ns1, v => v.NoStar1 → v.Few1 → v.mass1 ≥ 50 → v.BH1
  | .obs_rv2, v => v.RVok2
  | .mod_rv2, v => v.RVok2 → v.Orbit2
  | .stat_fit2, v => v.fit2 ≥ 80
  | .mod_fit2, v => v.Orbit2 → v.fit2 ≥ 80 → v.mass2 ≥ 50
  | .obs_faint2, v => v.Faint2
  | .mod_dark2, v => v.Faint2 → v.mass2 ≥ 50 → v.NoStar2
  | .mod_few2, v => v.Few2
  | .lit_ns2, v => v.NoStar2 → v.Few2 → v.mass2 ≥ 50 → v.BH2
  | .obs_rv3, v => v.RVok3
  | .mod_rv3, v => v.RVok3 → v.Orbit3
  | .stat_fit3, v => v.fit3 ≥ 300
  | .mod_fit3, v => v.Orbit3 → v.fit3 ≥ 300 → v.mass3 ≥ 50
  | .obs_faint3, v => v.Faint3
  | .mod_dark3, v => v.Faint3 → v.mass3 ≥ 50 → v.NoStar3
  | .mod_few3, v => v.Few3
  | .mod_ns3, v => v.NoStar3 → v.Few3 → v.mass3 ≥ 50 → v.BH3

/-- [stated 2209.06833: "We find no plausible astrophysical scenario that can explain the orbit and does not involve a black hole"] Abstract;
[stated 2302.07880: "the companion must be a BH, or a close binary containing a BH"] Sec. 4;
[stated 2404.10486: "Most probably, the massive dark object is a single black hole"] Sec. 4 -/
def Conclusion (v : Vocab) : Prop := v.BH1 ∧ v.BH2 ∧ v.BH3

-- FIXED BLOCK B (identical in every study)
def Premises (v : Vocab) : Prop := ∀ f, prem f v
def Without (g : Field) (v : Vocab) : Prop := ∀ f, f ≠ g → prem f v
def Stated (v : Vocab) : Prop := ∀ f, prov f = .stated → prem f v
def Explicit (v : Vocab) : Prop := ∀ f, prov f ≠ .reconstructed → prem f v
-- END FIXED BLOCK B

/-- A model in which every premise and the conclusion hold; countermodels change a few fields. -/
def full : Vocab :=
  { RVok1 := True, Orbit1 := True, fit1 := 90, astro1 := 50, mass1 := 50, Faint1 := True,
    NoStar1 := True, Few1 := True, BH1 := True,
    RVok2 := True, Orbit2 := True, fit2 := 80, mass2 := 50, Faint2 := True,
    NoStar2 := True, Few2 := True, BH2 := True,
    RVok3 := True, Orbit3 := True, fit3 := 300, mass3 := 50, Faint3 := True,
    NoStar3 := True, Few3 := True, BH3 := True }

/-- The papers' chains, step by step. -/
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  -- BH1 (El-Badry et al. 2023a)
  have o1 : v.Orbit1 := p .mod_rv1 (p .obs_rv1)                 -- Sec. 3.2, 4.2.1
  have m1 : v.mass1 ≥ 50 := p .mod_fit1 o1 (p .stat_fit1)       -- Sec. 4.1
  have n1 : v.NoStar1 := p .mod_dark1 (p .obs_faint1) m1        -- Sec. 5.1.1, 8.1
  have b1 : v.BH1 := p .lit_ns1 n1 (p .mod_few1) m1             -- Sec. 8.2 (NS mass implied)
  -- BH2 (El-Badry et al. 2023b)
  have o2 : v.Orbit2 := p .mod_rv2 (p .obs_rv2)                 -- Sec. 3.7.1, 4.1
  have m2 : v.mass2 ≥ 50 := p .mod_fit2 o2 (p .stat_fit2)       -- Sec. 3.7.3
  have n2 : v.NoStar2 := p .mod_dark2 (p .obs_faint2) m2        -- Sec. 3.8.1, 4
  have b2 : v.BH2 := p .lit_ns2 n2 (p .mod_few2) m2             -- Sec. 4 (NS mass implied)
  -- BH3 (Gaia Collaboration, Panuzzo et al. 2024)
  have o3 : v.Orbit3 := p .mod_rv3 (p .obs_rv3)                 -- Abstract (implied step)
  have m3 : v.mass3 ≥ 50 := p .mod_fit3 o3 (p .stat_fit3)       -- Eq. 5
  have n3 : v.NoStar3 := p .mod_dark3 (p .obs_faint3) m3        -- App. C, Sec. 3
  have b3 : v.BH3 := p .mod_ns3 n3 (p .mod_few3) m3             -- Sec. 3
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

-- BH1: two independent routes to the mass (joint fit; astrometry alone), so each is redundant.

theorem stat_fit1_redundant : ∀ v, Without .stat_fit1 v → Conclusion v := by
  intro v p
  have o1 : v.Orbit1 := p .mod_rv1 (by decide) (p .obs_rv1 (by decide))
  have m1 : v.mass1 ≥ 50 := p .mod_astro1 (by decide) o1 (p .num_astro1 (by decide))
  have n1 : v.NoStar1 := p .mod_dark1 (by decide) (p .obs_faint1 (by decide)) m1
  have o2 : v.Orbit2 := p .mod_rv2 (by decide) (p .obs_rv2 (by decide))
  have m2 : v.mass2 ≥ 50 := p .mod_fit2 (by decide) o2 (p .stat_fit2 (by decide))
  have n2 : v.NoStar2 := p .mod_dark2 (by decide) (p .obs_faint2 (by decide)) m2
  have o3 : v.Orbit3 := p .mod_rv3 (by decide) (p .obs_rv3 (by decide))
  have m3 : v.mass3 ≥ 50 := p .mod_fit3 (by decide) o3 (p .stat_fit3 (by decide))
  have n3 : v.NoStar3 := p .mod_dark3 (by decide) (p .obs_faint3 (by decide)) m3
  exact ⟨p .lit_ns1 (by decide) n1 (p .mod_few1 (by decide)) m1,
         p .lit_ns2 (by decide) n2 (p .mod_few2 (by decide)) m2,
         p .mod_ns3 (by decide) n3 (p .mod_few3 (by decide)) m3⟩

theorem mod_fit1_redundant : ∀ v, Without .mod_fit1 v → Conclusion v := by
  intro v p
  have o1 : v.Orbit1 := p .mod_rv1 (by decide) (p .obs_rv1 (by decide))
  have m1 : v.mass1 ≥ 50 := p .mod_astro1 (by decide) o1 (p .num_astro1 (by decide))
  have n1 : v.NoStar1 := p .mod_dark1 (by decide) (p .obs_faint1 (by decide)) m1
  have o2 : v.Orbit2 := p .mod_rv2 (by decide) (p .obs_rv2 (by decide))
  have m2 : v.mass2 ≥ 50 := p .mod_fit2 (by decide) o2 (p .stat_fit2 (by decide))
  have n2 : v.NoStar2 := p .mod_dark2 (by decide) (p .obs_faint2 (by decide)) m2
  have o3 : v.Orbit3 := p .mod_rv3 (by decide) (p .obs_rv3 (by decide))
  have m3 : v.mass3 ≥ 50 := p .mod_fit3 (by decide) o3 (p .stat_fit3 (by decide))
  have n3 : v.NoStar3 := p .mod_dark3 (by decide) (p .obs_faint3 (by decide)) m3
  exact ⟨p .lit_ns1 (by decide) n1 (p .mod_few1 (by decide)) m1,
         p .lit_ns2 (by decide) n2 (p .mod_few2 (by decide)) m2,
         p .mod_ns3 (by decide) n3 (p .mod_few3 (by decide)) m3⟩

theorem num_astro1_redundant : ∀ v, Without .num_astro1 v → Conclusion v := by
  intro v p
  have o1 : v.Orbit1 := p .mod_rv1 (by decide) (p .obs_rv1 (by decide))
  have m1 : v.mass1 ≥ 50 := p .mod_fit1 (by decide) o1 (p .stat_fit1 (by decide))
  have n1 : v.NoStar1 := p .mod_dark1 (by decide) (p .obs_faint1 (by decide)) m1
  have o2 : v.Orbit2 := p .mod_rv2 (by decide) (p .obs_rv2 (by decide))
  have m2 : v.mass2 ≥ 50 := p .mod_fit2 (by decide) o2 (p .stat_fit2 (by decide))
  have n2 : v.NoStar2 := p .mod_dark2 (by decide) (p .obs_faint2 (by decide)) m2
  have o3 : v.Orbit3 := p .mod_rv3 (by decide) (p .obs_rv3 (by decide))
  have m3 : v.mass3 ≥ 50 := p .mod_fit3 (by decide) o3 (p .stat_fit3 (by decide))
  have n3 : v.NoStar3 := p .mod_dark3 (by decide) (p .obs_faint3 (by decide)) m3
  exact ⟨p .lit_ns1 (by decide) n1 (p .mod_few1 (by decide)) m1,
         p .lit_ns2 (by decide) n2 (p .mod_few2 (by decide)) m2,
         p .mod_ns3 (by decide) n3 (p .mod_few3 (by decide)) m3⟩

theorem mod_astro1_redundant : ∀ v, Without .mod_astro1 v → Conclusion v := by
  intro v p
  have o1 : v.Orbit1 := p .mod_rv1 (by decide) (p .obs_rv1 (by decide))
  have m1 : v.mass1 ≥ 50 := p .mod_fit1 (by decide) o1 (p .stat_fit1 (by decide))
  have n1 : v.NoStar1 := p .mod_dark1 (by decide) (p .obs_faint1 (by decide)) m1
  have o2 : v.Orbit2 := p .mod_rv2 (by decide) (p .obs_rv2 (by decide))
  have m2 : v.mass2 ≥ 50 := p .mod_fit2 (by decide) o2 (p .stat_fit2 (by decide))
  have n2 : v.NoStar2 := p .mod_dark2 (by decide) (p .obs_faint2 (by decide)) m2
  have o3 : v.Orbit3 := p .mod_rv3 (by decide) (p .obs_rv3 (by decide))
  have m3 : v.mass3 ≥ 50 := p .mod_fit3 (by decide) o3 (p .stat_fit3 (by decide))
  have n3 : v.NoStar3 := p .mod_dark3 (by decide) (p .obs_faint3 (by decide)) m3
  exact ⟨p .lit_ns1 (by decide) n1 (p .mod_few1 (by decide)) m1,
         p .lit_ns2 (by decide) n2 (p .mod_few2 (by decide)) m2,
         p .mod_ns3 (by decide) n3 (p .mod_few3 (by decide)) m3⟩

-- Every other premise is needed: a countermodel breaks its system's chain at that link.

theorem obs_rv1_needed : ¬ ∀ v, Without .obs_rv1 v → Conclusion v := fun h =>
  (h { full with RVok1 := False, Orbit1 := False, mass1 := 0, NoStar1 := False, BH1 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

theorem mod_rv1_needed : ¬ ∀ v, Without .mod_rv1 v → Conclusion v := fun h =>
  (h { full with Orbit1 := False, mass1 := 0, NoStar1 := False, BH1 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

theorem obs_faint1_needed : ¬ ∀ v, Without .obs_faint1 v → Conclusion v := fun h =>
  (h { full with Faint1 := False, NoStar1 := False, BH1 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

theorem mod_dark1_needed : ¬ ∀ v, Without .mod_dark1 v → Conclusion v := fun h =>
  (h { full with NoStar1 := False, BH1 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

theorem mod_few1_needed : ¬ ∀ v, Without .mod_few1 v → Conclusion v := fun h =>
  (h { full with Few1 := False, BH1 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

theorem lit_ns1_needed : ¬ ∀ v, Without .lit_ns1 v → Conclusion v := fun h =>
  (h { full with BH1 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

theorem obs_rv2_needed : ¬ ∀ v, Without .obs_rv2 v → Conclusion v := fun h =>
  (h { full with RVok2 := False, Orbit2 := False, mass2 := 0, NoStar2 := False, BH2 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.1

theorem mod_rv2_needed : ¬ ∀ v, Without .mod_rv2 v → Conclusion v := fun h =>
  (h { full with Orbit2 := False, mass2 := 0, NoStar2 := False, BH2 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.1

theorem stat_fit2_needed : ¬ ∀ v, Without .stat_fit2 v → Conclusion v := fun h =>
  (h { full with fit2 := 0, mass2 := 0, NoStar2 := False, BH2 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.1

theorem mod_fit2_needed : ¬ ∀ v, Without .mod_fit2 v → Conclusion v := fun h =>
  (h { full with mass2 := 0, NoStar2 := False, BH2 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.1

theorem obs_faint2_needed : ¬ ∀ v, Without .obs_faint2 v → Conclusion v := fun h =>
  (h { full with Faint2 := False, NoStar2 := False, BH2 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.1

theorem mod_dark2_needed : ¬ ∀ v, Without .mod_dark2 v → Conclusion v := fun h =>
  (h { full with NoStar2 := False, BH2 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.1

theorem mod_few2_needed : ¬ ∀ v, Without .mod_few2 v → Conclusion v := fun h =>
  (h { full with Few2 := False, BH2 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.1

theorem lit_ns2_needed : ¬ ∀ v, Without .lit_ns2 v → Conclusion v := fun h =>
  (h { full with BH2 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.1

theorem obs_rv3_needed : ¬ ∀ v, Without .obs_rv3 v → Conclusion v := fun h =>
  (h { full with RVok3 := False, Orbit3 := False, mass3 := 0, NoStar3 := False, BH3 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2

theorem mod_rv3_needed : ¬ ∀ v, Without .mod_rv3 v → Conclusion v := fun h =>
  (h { full with Orbit3 := False, mass3 := 0, NoStar3 := False, BH3 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2

theorem stat_fit3_needed : ¬ ∀ v, Without .stat_fit3 v → Conclusion v := fun h =>
  (h { full with fit3 := 0, mass3 := 0, NoStar3 := False, BH3 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2

theorem mod_fit3_needed : ¬ ∀ v, Without .mod_fit3 v → Conclusion v := fun h =>
  (h { full with mass3 := 0, NoStar3 := False, BH3 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2

theorem obs_faint3_needed : ¬ ∀ v, Without .obs_faint3 v → Conclusion v := fun h =>
  (h { full with Faint3 := False, NoStar3 := False, BH3 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2

theorem mod_dark3_needed : ¬ ∀ v, Without .mod_dark3 v → Conclusion v := fun h =>
  (h { full with NoStar3 := False, BH3 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2

theorem mod_few3_needed : ¬ ∀ v, Without .mod_few3 v → Conclusion v := fun h =>
  (h { full with Few3 := False, BH3 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2

theorem mod_ns3_needed : ¬ ∀ v, Without .mod_ns3 v → Conclusion v := fun h =>
  (h { full with BH3 := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2

/-- What the papers write is not enough: they rely on the textbook mass determination (Kepler)
and on the maximum neutron-star mass, which neither BH paper states as a number. -/
theorem stated_insufficient : ¬ ∀ v, Stated v → Conclusion v := fun h =>
  (h { full with BH2 := False } (by intro f hf; cases f <;> simp_all [prov, prem, full])).2.1

/-- With standard knowledge added the argument is complete: no reconstructed (GAP) premise is
needed. Its weak points are physical (premises stated as plausibility arguments), not logical. -/
theorem explicit_sufficient : ∀ v, Explicit v → Conclusion v := by
  intro v p
  exact final v (fun f => p f (by cases f <;> decide))

end Argument
