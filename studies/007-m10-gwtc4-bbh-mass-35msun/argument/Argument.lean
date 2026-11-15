/-
Argument of the paper, decomposed: LVK 2026, "GWTC-4.0: Population Properties of Merging Compact
Binaries" (ApJL 1005, L51; arXiv:2508.18083; "P26"). Context in the wiki article: the catalogue
paper (arXiv:2508.18082), GW231123 (arXiv:2507.08219) and independent analyses.

The conclusion encoded is the 35 Msun part of the abstract sentence "features persist at primary
masses of 10 Msun and 35 Msun", where the abstract defines the features as departures from an
otherwise power-law-like continuum. A separate theorem (overdensity_not_implied) checks whether the
stronger reading of the abstract, an over-density at 35 Msun ("We resolve multiple over- and
under-densities"), follows from the same premises.

The chain:
  a BBH sample selected by FAR < 1/yr and a 1% lower mass limit above 3 Msun (153 events)
  selection effects from search-pipeline injections via a Monte Carlo integral
  in the fiducial model, lambda2 > lambda1 (steeper above 35 Msun) at 97.7% credibility
  [gap] the parametric and weakly modeled fits, parameter-estimation systematics and residual
      noise events do not produce a spurious break near 35 Msun
  [implied] a credible change of slope in an adequate model with correct selection effects is a
      steepening of the astrophysical spectrum
  [stated] such a departure from a power-law continuum is a feature
  -> a feature at 35 Msun
  Also stated: the B-Spline model shows a local peak at 33.5 Msun; but among broken-power-law
  models the Bayes factors do not prefer a peak over a plain break, so an over-density at 35 Msun
  does not follow (overdensity_not_implied).

Rules: AGENTS.md section 2 (paper study, Lean); specification: design/007 section 2.2.
Quotes follow the published text (ApJL version, read via the arXiv PDF).
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
  /-- The BBH sample is selected by FAR < 1/yr and a 1% lower limit on both component masses above 3 Msun (153 events). -/
  Sample : Prop
  /-- The detection efficiency is estimated from search-pipeline injections through a Monte Carlo integral. -/
  SelModel : Prop
  /-- Posterior credibility, in per mille, that the spectral index above about 35 Msun exceeds the one below it. -/
  cred_pm : Nat
  /-- The population models, parameter-estimation systematics and residual noise events do not produce a spurious break near 35 Msun. -/
  ModelsOK : Prop
  /-- The astrophysical primary-mass spectrum steepens above about 35 Msun. -/
  Steepens : Prop
  /-- The primary-mass spectrum has a feature at 35 Msun (a departure from a power-law-like continuum). -/
  Feature35 : Prop
  /-- The B-Spline model shows a local peak near 33.5 Msun. -/
  BsplinePeak : Prop
  /-- Among broken-power-law models, the Bayes factors do not prefer a peak at 35 Msun over a plain break. -/
  ModelsTie : Prop
  /-- The feature at 35 Msun is an over-density (a peak), not only a break. -/
  OverDensity35 : Prop

/-- The premises. -/
inductive Field where
  /-- OBS [stated 2508.18083: "We only include events whose 1% lower limit on both component mass posteriors"] Sec. 6 (FAR below 1 per yr; 84 O4a plus 69 GWTC-3.0 events, 153 in all) -/
  | obs_sample
  /-- MOD [stated 2508.18083: "is estimated using these injections through a Monte Carlo integral"] Sec. 3.3 -/
  | mod_sel
  /-- STAT [stated 2508.18083: "at 97.7% credibility"] Sec. 6.1 (lambda2 above lambda1) -/
  | stat_steep
  /-- GAP [reconstructed] the fitted models, the parameter-estimation systematics (P26 Sec. 3.3 notes a likelihood normalisation error whose impact it expects to be negligible) and the expected noise events (about 6.7 among the 161 candidates, Sec. 3.2.1) do not produce a spurious break near 35 Msun; P26 compares models but does not test this directly -/
  | gap_model
  /-- MOD [implied] a credible change of slope in an adequate population model with correct selection effects is a steepening of the astrophysical spectrum (Bayesian inference, Gelman et al. 2013, Bayesian Data Analysis, 3rd ed., ch. 1) -/
  | mod_steep
  /-- MOD [stated 2508.18083: "These are departures from an otherwise power-law-like continuum"] Abstract (the features are departures from a power-law continuum) -/
  | mod_feature
  /-- STAT [stated 2508.18083: "which exhibits a local peak at"] Sec. 6.1 (B-Spline, 33.5 Msun) -/
  | stat_bspline
  /-- STAT [stated 2508.18083: "the Bayes factors do not show strong support for one model over another"] App. D.1 (log10 B of BP1P against BP2P is -0.06) -/
  | stat_tie
  /-- MOD [implied] an over-density claim needs the peak model to be preferred over the break model; a local peak in one flexible model with no Bayes-factor preference does not establish it (Kass and Raftery 1995, JASA 90, 773) -/
  | mod_od
  deriving DecidableEq, Repr

def prov : Field → Prov
  | .obs_sample => .stated
  | .mod_sel => .stated
  | .stat_steep => .stated
  | .gap_model => .reconstructed
  | .mod_steep => .implied
  | .mod_feature => .stated
  | .stat_bspline => .stated
  | .stat_tie => .stated
  | .mod_od => .implied

def prem : Field → Vocab → Prop
  | .obs_sample, v => v.Sample
  | .mod_sel, v => v.SelModel
  | .stat_steep, v => v.cred_pm ≥ 950
  | .gap_model, v => v.ModelsOK
  | .mod_steep, v => v.Sample → v.SelModel → v.cred_pm ≥ 950 → v.ModelsOK → v.Steepens
  | .mod_feature, v => v.Steepens → v.Feature35
  | .stat_bspline, v => v.BsplinePeak
  | .stat_tie, v => v.ModelsTie
  | .mod_od, v => v.BsplinePeak → ¬ v.ModelsTie → v.OverDensity35

/-- [stated 2508.18083: "features persist at primary masses of 10 M⊙ and 35 M⊙"] Abstract; only the 35 Msun part is encoded -/
def Conclusion (v : Vocab) : Prop := v.Feature35

-- FIXED BLOCK B (identical in every study)
def Premises (v : Vocab) : Prop := ∀ f, prem f v
def Without (g : Field) (v : Vocab) : Prop := ∀ f, f ≠ g → prem f v
def Stated (v : Vocab) : Prop := ∀ f, prov f = .stated → prem f v
def Explicit (v : Vocab) : Prop := ∀ f, prov f ≠ .reconstructed → prem f v
-- END FIXED BLOCK B

/-- The paper's chain, step by step. -/
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  have h1 : v.Steepens :=
    p .mod_steep (p .obs_sample) (p .mod_sel) (p .stat_steep) (p .gap_model)  -- Sec. 3.3, 6, 6.1; GAP
  exact p .mod_feature h1  -- Abstract

theorem final_nontrivial : ¬ ∀ v : Vocab, Conclusion v :=
  fun h => h ⟨False, False, 0, False, False, False, False, False, False⟩

theorem consistent : ∃ v, Premises v :=
  ⟨⟨True, True, 977, True, True, True, True, True, False⟩, by intro f; cases f <;> simp [prem]⟩

theorem alone_insufficient : ∀ g, ¬ ∀ v, prem g v → Conclusion v := by
  intro g h
  cases g
  case mod_steep => exact h ⟨False, False, 0, False, False, False, False, False, False⟩ (by simp [prem])
  case mod_feature => exact h ⟨False, False, 0, False, False, False, False, False, False⟩ (by simp [prem])
  case mod_od => exact h ⟨False, False, 0, False, False, False, False, False, False⟩ (by simp [prem])
  all_goals exact h ⟨True, True, 977, True, False, False, True, True, False⟩ (by simp [prem])

theorem obs_sample_needed : ¬ ∀ v, Without .obs_sample v → Conclusion v := fun h =>
  h ⟨False, True, 977, True, False, False, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem mod_sel_needed : ¬ ∀ v, Without .mod_sel v → Conclusion v := fun h =>
  h ⟨True, False, 977, True, False, False, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem stat_steep_needed : ¬ ∀ v, Without .stat_steep v → Conclusion v := fun h =>
  h ⟨True, True, 0, True, False, False, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem gap_model_needed : ¬ ∀ v, Without .gap_model v → Conclusion v := fun h =>
  h ⟨True, True, 977, False, False, False, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem mod_steep_needed : ¬ ∀ v, Without .mod_steep v → Conclusion v := fun h =>
  h ⟨True, True, 977, True, False, False, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem mod_feature_needed : ¬ ∀ v, Without .mod_feature v → Conclusion v := fun h =>
  h ⟨True, True, 977, True, True, False, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

/-- Redundant for the encoded conclusion: the B-Spline peak bears on the over-density reading
(overdensity_not_implied), not on the feature. -/
theorem stat_bspline_redundant : ∀ v, Without .stat_bspline v → Conclusion v := by
  intro v p
  exact p .mod_feature (by decide)
    (p .mod_steep (by decide) (p .obs_sample (by decide)) (p .mod_sel (by decide))
      (p .stat_steep (by decide)) (p .gap_model (by decide)))

/-- Redundant for the encoded conclusion, for the same reason. -/
theorem stat_tie_redundant : ∀ v, Without .stat_tie v → Conclusion v := by
  intro v p
  exact p .mod_feature (by decide)
    (p .mod_steep (by decide) (p .obs_sample (by decide)) (p .mod_sel (by decide))
      (p .stat_steep (by decide)) (p .gap_model (by decide)))

/-- Redundant for the encoded conclusion, for the same reason. -/
theorem mod_od_redundant : ∀ v, Without .mod_od v → Conclusion v := by
  intro v p
  exact p .mod_feature (by decide)
    (p .mod_steep (by decide) (p .obs_sample (by decide)) (p .mod_sel (by decide))
      (p .stat_steep (by decide)) (p .gap_model (by decide)))

/-- What the paper writes is not enough: the inference from a credible slope change to an
astrophysical steepening is standard background (implied), and model adequacy is not shown. -/
theorem stated_insufficient : ¬ ∀ v, Stated v → Conclusion v := fun h =>
  h ⟨True, True, 977, False, False, False, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])

/-- Even with standard knowledge the chain has a gap: the models, parameter-estimation
systematics and noise events must not produce a spurious break near 35 Msun. -/
theorem explicit_insufficient : ¬ ∀ v, Explicit v → Conclusion v := fun h =>
  h ⟨True, True, 977, False, False, False, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])

/-- The stronger reading does not follow: with every premise true (including the B-Spline peak and
the Bayes-factor tie), the feature at 35 Msun need not be an over-density. -/
theorem overdensity_not_implied : ¬ ∀ v, Premises v → v.OverDensity35 := fun h =>
  h ⟨True, True, 977, True, True, True, True, True, False⟩ (by intro f; cases f <;> simp [prem])

end Argument
