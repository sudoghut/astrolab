/-
Argument of the paper, decomposed: Xiang and Rix 2022, "A time-resolved picture of our Milky Way's
early formation history" (Nature 603, 599; arXiv:2203.12110; "XR22").

The conclusion encoded is the abstract's onset claim: the formation of the old (thick) disc started
about 13 Gyr ago, only 0.8 Gyr after the Big Bang. The other claims (the split at 8 Gyr, the
star-formation peak near the Gaia-Sausage-Enceladus merger, enrichment over 5 to 6 Gyr, the 0.82 Gyr
age dispersion) are discussed in the wiki article and tested by the study, not encoded here.

The chain:
  ages come from Bayesian fits to alpha-enhanced Yonsei-Yale (YY) isochrones
  early-phase stars with J_phi above 500 kpc km/s and [Fe/H] between -1.05 and -0.95 are
      presumably the oldest thick-disc stars
  a Gaussian fit to their ages gives a mean of 13 Gyr (Extended Data Fig. 1)
  at the old end the YY ages are consistent with the age of the universe
  the universe is 13.8 Gyr old (Planck 2018)
  [gap] consistency with the age of the universe establishes the absolute YY age scale at 13 Gyr
      to better than about 0.5 Gyr (it only rules out ages far above 13.8 Gyr; MIST isochrones give
      ages 0.5 Gyr older, XR22 Extended Data Fig. 4)
  [gap] the mean age of the surviving local stars in that bin dates the start of disc formation
      (the mean of a 1.8 Gyr wide distribution is not an onset; survivors and radial migration;
      halo contamination of the bin)
  -> the old disc started forming about 13 Gyr ago, about 0.8 Gyr after the Big Bang

Ages are encoded in tenths of a Gyr (Nat): mean_x10 = 130 states the reported, rounded 13 Gyr (the
figure inset shows 13.03). The 0.8 Gyr enters only through the comparison of the two ages; Lean has
no arithmetic here. Quotes follow the arXiv v1 PDF.

Rules: AGENTS.md section 2 (paper study, Lean); specification: design/007 section 2.2.
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
  /-- Ages come from Bayesian fits to alpha-enhanced YY isochrones (weighted over [alpha/Fe] = 0, 0.2, 0.4). -/
  AgesYY : Prop
  /-- Early-phase stars with J_phi above 500 kpc km/s and [Fe/H] between -1.05 and -0.95 are the oldest thick-disc stars. -/
  OldestBin : Prop
  /-- Mean age of a Gaussian fitted to the ages of that bin, in tenths of a Gyr (reported, rounded). -/
  mean_x10 : Nat
  /-- At the old end the YY ages are consistent with the age of the universe. -/
  ScaleConsistent : Prop
  /-- The absolute YY age scale at about 13 Gyr is accurate to better than about 0.5 Gyr. -/
  ScaleAccurate : Prop
  /-- Age of the universe, in tenths of a Gyr. -/
  universe_x10 : Nat
  /-- The old (thick) disc of the Milky Way started forming about 13 Gyr ago, about 0.8 Gyr after the Big Bang. -/
  Onset : Prop

/-- The premises. -/
inductive Field where
  /-- MOD [stated: "We adopt the YY isochrones, and take the weighted-mean ages from isochrones with"] Extended Data Fig. 4 ([alpha/Fe] = 0, 0.2 and 0.4; Methods: Bayesian age estimation) -/
  | mod_ages
  /-- MOD [stated: "presumably the oldest thick disk stars"] Extended Data Fig. 1 (early phase, J_phi above 500 kpc km/s, -1.05 to -0.95 in [Fe/H]); the hedge is encoded as an assertion -/
  | mod_bin
  /-- STAT [stated: "A Gaussian fit to the distribution (red curve) yields a mean age of 13 Gyr"] Extended Data Fig. 1 (inset: mean 13.03, sigma 1.81); encoded as the reported, rounded 130 tenths -/
  | stat_mean
  /-- OBS [stated: "they are consistent with the age of the universe at the old end"] Methods (Ages from the YY isochrones seem to be reasonable; Figure 2) -/
  | obs_scale
  /-- LIT [implied] age of the universe 13.8 Gyr: Planck Collaboration 2020, A&A 641, A6, arXiv:1807.06209 (XR22 cites a reference, ref. 19, for 0.8 Gyr after the Big Bang) -/
  | lit_universe
  /-- GAP [reconstructed] consistency with the age of the universe establishes the absolute YY age scale at 13 Gyr to better than about 0.5 Gyr. It only rules out ages far above 13.8 Gyr: XR22 imposes no age prior, MIST isochrones give ages 0.5 Gyr older (Extended Data Fig. 4), and a scale older or younger by a few tenths of a Gyr would remain consistent with 13.8 Gyr; a later re-analysis finds ages younger by 12.9 percent (Chen, Sun and Ye 2025, arXiv:2510.10092) -/
  | gap_scale
  /-- GAP [reconstructed] with these ages, the mean age of the surviving local stars in the most metal-poor old-disc bin dates the start of disc formation. XR22 does not argue this step: the mean of a distribution 1.8 Gyr wide is not its onset, the stars observed near the Sun are survivors that may have migrated, and the bin may contain halo stars (XR22 Extended Data Fig. 2 shows a low J_phi tail at these metallicities) -/
  | gap_onset
  deriving DecidableEq, Repr

def prov : Field → Prov
  | .mod_ages => .stated
  | .mod_bin => .stated
  | .stat_mean => .stated
  | .obs_scale => .stated
  | .lit_universe => .implied
  | .gap_scale => .reconstructed
  | .gap_onset => .reconstructed

def prem : Field → Vocab → Prop
  | .mod_ages, v => v.AgesYY
  | .mod_bin, v => v.OldestBin
  | .stat_mean, v => v.mean_x10 = 130
  | .obs_scale, v => v.ScaleConsistent
  | .lit_universe, v => v.universe_x10 = 138
  | .gap_scale, v => v.ScaleConsistent → v.ScaleAccurate
  | .gap_onset, v => v.AgesYY → v.ScaleAccurate → v.OldestBin → v.mean_x10 = 130 → v.universe_x10 > v.mean_x10 → v.Onset

/-- [stated: "the formation of the Galactic old (thick) disk started 13 Gyr ago, only 0.8 Gyr after the Big Bang"] Abstract -/
def Conclusion (v : Vocab) : Prop := v.Onset

-- FIXED BLOCK B (identical in every study)
def Premises (v : Vocab) : Prop := ∀ f, prem f v
def Without (g : Field) (v : Vocab) : Prop := ∀ f, f ≠ g → prem f v
def Stated (v : Vocab) : Prop := ∀ f, prov f = .stated → prem f v
def Explicit (v : Vocab) : Prop := ∀ f, prov f ≠ .reconstructed → prem f v
-- END FIXED BLOCK B

/-- The paper's chain, step by step. -/
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  have hm : v.mean_x10 = 130 := p .stat_mean                    -- Extended Data Fig. 1
  have hu : v.universe_x10 = 138 := p .lit_universe             -- Planck 2018
  have hs : v.ScaleAccurate := p .gap_scale (p .obs_scale)       -- GAP: age scale
  exact p .gap_onset (p .mod_ages) hs (p .mod_bin) hm (by omega)  -- GAP: mean as onset

theorem final_nontrivial : ¬ ∀ v : Vocab, Conclusion v :=
  fun h => h ⟨False, False, 0, False, False, 0, False⟩

theorem consistent : ∃ v, Premises v :=
  ⟨⟨True, True, 130, True, True, 138, True⟩, by intro f; cases f <;> simp [prem]⟩

theorem alone_insufficient : ∀ g, ¬ ∀ v, prem g v → Conclusion v := by
  intro g h
  cases g
  case gap_onset => exact h ⟨False, False, 0, False, False, 0, False⟩ (by simp [prem])
  all_goals exact h ⟨True, True, 130, True, True, 138, False⟩ (by simp [prem])

theorem mod_ages_needed : ¬ ∀ v, Without .mod_ages v → Conclusion v := fun h =>
  h ⟨False, True, 130, True, True, 138, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem mod_bin_needed : ¬ ∀ v, Without .mod_bin v → Conclusion v := fun h =>
  h ⟨True, False, 130, True, True, 138, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem stat_mean_needed : ¬ ∀ v, Without .stat_mean v → Conclusion v := fun h =>
  h ⟨True, True, 0, True, True, 138, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem obs_scale_needed : ¬ ∀ v, Without .obs_scale v → Conclusion v := fun h =>
  h ⟨True, True, 130, False, False, 138, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem lit_universe_needed : ¬ ∀ v, Without .lit_universe v → Conclusion v := fun h =>
  h ⟨True, True, 130, True, True, 0, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem gap_scale_needed : ¬ ∀ v, Without .gap_scale v → Conclusion v := fun h =>
  h ⟨True, True, 130, True, False, 138, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem gap_onset_needed : ¬ ∀ v, Without .gap_onset v → Conclusion v := fun h =>
  h ⟨True, True, 130, True, True, 138, False⟩ (by intro f hf; cases f <;> simp_all [prem])

/-- What the paper writes is not enough: the accuracy of the absolute age scale and the step from a
mean age to an onset are not stated, and the age of the universe is only cited. -/
theorem stated_insufficient : ¬ ∀ v, Stated v → Conclusion v := fun h =>
  h ⟨True, True, 130, True, False, 138, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])

/-- Standard knowledge (the age of the universe) does not close the argument: two gaps remain. -/
theorem explicit_insufficient : ¬ ∀ v, Explicit v → Conclusion v := fun h =>
  h ⟨True, True, 130, True, False, 138, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])

end Argument
