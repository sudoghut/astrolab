/-
Argument of the paper, decomposed: LVK 2026, "GWTC-4.0: Population Properties of Merging Compact
Binaries" (ApJL 1005, L51; arXiv:2508.18083; "P26"). Context in the wiki article: the catalogue
paper (arXiv:2508.18082), GW231123 (arXiv:2507.08219) and independent analyses.

The conclusion encoded is the 35 Msun part of the abstract sentence "features persist at primary
masses of 10 Msun and 35 Msun", read in the sense of Sec. 6.1 ("We identify a feature at 35"):
a feature that may be either an over-density or a break in a broken power law. Whether the feature
is an over-density is discussed in the wiki article, not encoded: P26 says the peak reading is
supported by the B-Spline model while the Bayes factors do not strongly prefer it, and whether
supported amounts to established is a judgement, not something a machine check adds.

The chain has two routes to the feature, with two gaps shared by both:
  a BBH sample selected by FAR < 1/yr and a 1% lower mass limit above 3 Msun (153 events)
  selection effects from search-pipeline injections via a Monte Carlo integral
  [gap] the selection function is adequate at high mass
  [gap] parameter-estimation systematics and residual noise events do not make a spurious
      feature near 35 Msun
  route 1 (strongly modeled): lambda2 > lambda1 at 97.7% credibility
  route 2 (weakly modeled): the B-Spline shows a local peak near 33.5 Msun, consistent with the
      other weakly modeled approaches
  [gap] either route, with the sample, selection and systematics as above, gives a feature at
      35 Msun in the Sec. 6.1 sense (P26 asserts the feature after presenting both results but does
      not state the bridging rule)
  -> a feature at 35 Msun

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
  /-- The analysed BBH sample: the events passing the FAR threshold and the mass cut, 153 in all. -/
  Sample : Prop
  /-- The detection efficiency is estimated from search-pipeline injections through a Monte Carlo integral. -/
  SelUsed : Prop
  /-- The selection function so estimated is adequate at high mass (above about 30 Msun). -/
  SelOK : Prop
  /-- Posterior credibility, in per mille, that the spectral index above about 35 Msun exceeds the one below it (fiducial strongly modeled fit). -/
  cred_pm : Nat
  /-- The B-Spline (weakly modeled) fit shows a local peak near 33.5 Msun. -/
  BsplinePeak : Prop
  /-- The B-Spline result is consistent with the other weakly modeled approaches. -/
  WeakAgree : Prop
  /-- Parameter-estimation systematics and residual noise events do not make a spurious feature near 35 Msun. -/
  SystOK : Prop
  /-- The primary-mass spectrum has a feature at 35 Msun in the sense of P26 Sec. 6.1 (an over-density or a break). -/
  Feature35 : Prop

/-- The premises. -/
inductive Field where
  /-- OBS [stated 2508.18083: "which brings the total number of BBH events passing our FAR threshold to 153"] Sec. 6 (with the mass cut on the 1% lower limits) -/
  | obs_sample
  /-- MOD [stated 2508.18083: "is estimated using these injections through a Monte Carlo integral"] Sec. 3.3 -/
  | mod_sel
  /-- GAP [reconstructed] the injection-based selection function is adequate at high mass; P26 does not test this at the masses that matter for the 35 Msun feature -/
  | gap_sel
  /-- STAT [stated 2508.18083: "at 97.7% credibility"] Sec. 6.1 (subject: the index above 35 Msun exceeds the one below; the body, at least 97.7 percent, is no stronger than the reported value) -/
  | stat_steep
  /-- STAT [stated 2508.18083: "which exhibits a local peak at"] Sec. 6.1 (B-Spline, 33.5 Msun) -/
  | stat_bspline
  /-- STAT [stated 2508.18083: "consistent with other models that employ a weakly modeled approach"] Sec. 6.1, App. D.4 -/
  | stat_weak
  /-- GAP [reconstructed] parameter-estimation systematics and residual noise events (about 6.7 expected among the 161 candidates with FAR below 1 per yr, Sec. 3.2.1) do not make a spurious feature near 35 Msun; P26 does not propagate either into the mass spectrum -/
  | gap_syst
  /-- GAP [reconstructed] route 1: with the sample, an adequate selection function and no spurious systematics, the credible slope change is a feature at 35 Msun in the Sec. 6.1 sense; P26 presents the slope result and then identifies a feature, which it says may be a break (Sec. 6.1: or (ii) a broken power law with break), but does not state this bridging rule -/
  | gap_route1
  /-- GAP [reconstructed] route 2: under the same conditions, a local peak in a flexible model that agrees with the other flexible models is a feature at 35 Msun; P26 says the B-Spline peak supports the over-density reading (Sec. 6.1) but does not state this bridging rule -/
  | gap_route2
  deriving DecidableEq, Repr

def prov : Field → Prov
  | .obs_sample => .stated
  | .mod_sel => .stated
  | .gap_sel => .reconstructed
  | .stat_steep => .stated
  | .stat_bspline => .stated
  | .stat_weak => .stated
  | .gap_syst => .reconstructed
  | .gap_route1 => .reconstructed
  | .gap_route2 => .reconstructed

def prem : Field → Vocab → Prop
  | .obs_sample, v => v.Sample
  | .mod_sel, v => v.SelUsed
  | .gap_sel, v => v.SelOK
  | .stat_steep, v => v.cred_pm ≥ 977
  | .stat_bspline, v => v.BsplinePeak
  | .stat_weak, v => v.WeakAgree
  | .gap_syst, v => v.SystOK
  | .gap_route1, v => v.Sample → v.SelUsed → v.SelOK → v.cred_pm ≥ 977 → v.SystOK → v.Feature35
  | .gap_route2, v => v.Sample → v.SelUsed → v.SelOK → v.BsplinePeak → v.WeakAgree → v.SystOK → v.Feature35

/-- [stated 2508.18083: "features persist at primary masses of 10 M⊙ and 35 M⊙"] Abstract; only the 35 Msun part is encoded, in the Sec. 6.1 sense (We identify a feature at 35 M⊙, an over-density or a break) -/
def Conclusion (v : Vocab) : Prop := v.Feature35

-- FIXED BLOCK B (identical in every study)
def Premises (v : Vocab) : Prop := ∀ f, prem f v
def Without (g : Field) (v : Vocab) : Prop := ∀ f, f ≠ g → prem f v
def Stated (v : Vocab) : Prop := ∀ f, prov f = .stated → prem f v
def Explicit (v : Vocab) : Prop := ∀ f, prov f ≠ .reconstructed → prem f v
-- END FIXED BLOCK B

/-- The paper's chain, step by step (route 1; route 2 is shown in the _redundant proofs). -/
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  exact p .gap_route1 (p .obs_sample) (p .mod_sel) (p .gap_sel) (p .stat_steep)
    (p .gap_syst)  -- Sec. 3.3, 6, 6.1; two GAPs

theorem final_nontrivial : ¬ ∀ v : Vocab, Conclusion v :=
  fun h => h ⟨False, False, False, 0, False, False, False, False⟩

theorem consistent : ∃ v, Premises v :=
  ⟨⟨True, True, True, 977, True, True, True, True⟩, by intro f; cases f <;> simp [prem]⟩

theorem alone_insufficient : ∀ g, ¬ ∀ v, prem g v → Conclusion v := by
  intro g h
  cases g
  case gap_route1 => exact h ⟨False, False, False, 0, False, False, False, False⟩ (by simp [prem])
  case gap_route2 => exact h ⟨False, False, False, 0, False, False, False, False⟩ (by simp [prem])
  all_goals exact h ⟨True, True, True, 977, True, True, True, False⟩ (by simp [prem])

theorem obs_sample_needed : ¬ ∀ v, Without .obs_sample v → Conclusion v := fun h =>
  h ⟨False, True, True, 977, True, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem mod_sel_needed : ¬ ∀ v, Without .mod_sel v → Conclusion v := fun h =>
  h ⟨True, False, True, 977, True, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem gap_sel_needed : ¬ ∀ v, Without .gap_sel v → Conclusion v := fun h =>
  h ⟨True, True, False, 977, True, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem gap_syst_needed : ¬ ∀ v, Without .gap_syst v → Conclusion v := fun h =>
  h ⟨True, True, True, 977, True, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prem])

/-- Redundant: route 2 (weakly modeled) gives the feature without the slope credibility. -/
theorem stat_steep_redundant : ∀ v, Without .stat_steep v → Conclusion v := by
  intro v p
  exact p .gap_route2 (by decide) (p .obs_sample (by decide)) (p .mod_sel (by decide))
    (p .gap_sel (by decide)) (p .stat_bspline (by decide)) (p .stat_weak (by decide))
    (p .gap_syst (by decide))

/-- Redundant for the same reason. -/
theorem gap_route1_redundant : ∀ v, Without .gap_route1 v → Conclusion v := by
  intro v p
  exact p .gap_route2 (by decide) (p .obs_sample (by decide)) (p .mod_sel (by decide))
    (p .gap_sel (by decide)) (p .stat_bspline (by decide)) (p .stat_weak (by decide))
    (p .gap_syst (by decide))

/-- Redundant: route 1 (strongly modeled) gives the feature without the B-Spline peak. -/
theorem stat_bspline_redundant : ∀ v, Without .stat_bspline v → Conclusion v := by
  intro v p
  exact p .gap_route1 (by decide) (p .obs_sample (by decide)) (p .mod_sel (by decide))
    (p .gap_sel (by decide)) (p .stat_steep (by decide)) (p .gap_syst (by decide))

/-- Redundant for the same reason. -/
theorem stat_weak_redundant : ∀ v, Without .stat_weak v → Conclusion v := by
  intro v p
  exact p .gap_route1 (by decide) (p .obs_sample (by decide)) (p .mod_sel (by decide))
    (p .gap_sel (by decide)) (p .stat_steep (by decide)) (p .gap_syst (by decide))

/-- Redundant for the same reason. -/
theorem gap_route2_redundant : ∀ v, Without .gap_route2 v → Conclusion v := by
  intro v p
  exact p .gap_route1 (by decide) (p .obs_sample (by decide)) (p .mod_sel (by decide))
    (p .gap_sel (by decide)) (p .stat_steep (by decide)) (p .gap_syst (by decide))

/-- What the paper writes is not enough: the bridging rules of both routes, the high-mass selection
and the systematics are not established. -/
theorem stated_insufficient : ¬ ∀ v, Stated v → Conclusion v := fun h =>
  h ⟨True, True, False, 977, True, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])

/-- Even with standard knowledge the chain needs the two shared gaps (an adequate high-mass
selection function; no spurious feature from systematics or noise events) and the bridging rule of
at least one route. -/
theorem explicit_insufficient : ¬ ∀ v, Explicit v → Conclusion v := fun h =>
  h ⟨True, True, False, 977, True, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])

end Argument
