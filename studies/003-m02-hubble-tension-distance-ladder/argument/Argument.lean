/-
Argument of the paper, decomposed: Riess et al. 2024, "JWST Validates HST Distance Measurements:
Selection of Supernova Subsample Explains Differences in JWST Estimates of Local H0"
(arXiv:2408.11770, ApJ accepted). The distance-ladder framework is that of Riess et al. 2022
(arXiv:2112.04510); the CCHP numbers come from Freedman et al. 2025 (arXiv:2408.06153). Those two
papers supply context in the wiki article; the chain below is the 2024 paper's own.

The chain (the conclusion is deliberately weak: "entirely consistent with"):
  full HST sample (42 SNe Ia, 4 anchors): H0 = 73.2
  the same HST Cepheid ladder on the CCHP-selected hosts, NGC 4258 anchor: H0 = 71.2
      -> choosing those hosts and that anchor is expected to lower H0 by about 2
  on the same hosts, HST Cepheid and JWST distances agree (TRGB and JAGB within errors)
  for every subsample, the JWST-inferred H0 (the paper's own calibration of the CCHP distances)
      is consistent with the HST expectation (at or within 1 sigma)
  F24's own reported three-method combination (70) is near the HST expectation for the subsample
      (~70.8 +- 2.3)
  -> the CCHP-vs-HST difference (about 2.5) is entirely consistent with sample selection

Rules: AGENTS.md section 2 (paper study, Lean); specification: design/007 section 2.2.
H0 values are in tenths of km/s/Mpc (Nat): 73.2 is 732.
Quotes follow the arXiv HTML text (v2), with math in its LaTeX source form.
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
  /-- Reported central value of H0 from the full HST sample (42 SNe Ia, 4 anchors), tenths of km/s/Mpc (premises bound it from below at that central value). -/
  h_full : Nat
  /-- Reported central value of H0 from HST Cepheids on the 10 CCHP-selected hosts (11 SNe Ia), NGC 4258 anchor, tenths. -/
  h_sel : Nat
  /-- The paper attributes the about 2 km/s/Mpc lower H0 on the CCHP-selected sample to the choice of SN hosts and anchor. -/
  ExpDrop : Prop
  /-- On the same hosts, HST Cepheid and JWST (Cepheid, TRGB, JAGB) distances agree within errors. -/
  AgreeSameHost : Prop
  /-- For every subsample, the H0 from the JWST distances, as recalibrated by the paper (Table 4), is consistent with the HST expectation on the same SNe (at or within 1 sigma, Sec. III.3). -/
  ResidSmall : Prop
  /-- CCHP's own reported three-method combined H0 for the subsample (F24) is near the HST expectation for that subsample. -/
  F24Near : Prop
  /-- The CCHP-vs-HST difference is entirely consistent with differences in sample selection. -/
  ConsSel : Prop

/-- The premises. -/
inductive Field where
  /-- STAT [stated 2408.11770: "is not yet competitive with the HST set (42 SNe Ia and 4 anchors), which yields 73.2 $\pm$ 0.9"] Abstract -/
  | stat_full
  /-- STAT [stated 2408.11770: "a corresponding value of H ${}_{0}=71.2$"] Sec. III.2 (HST Cepheids on the CCHP-selected hosts, NGC 4258 anchor) -/
  | stat_sel
  /-- STAT [stated 2408.11770: "thus 2.0 $\,\rm km\,s^{-1}\,Mpc^{-1}$ lower than the full HST sample—simply due to the choice of SN hosts and anchor"] Sec. III.2 -/
  | stat_drop
  /-- STAT [stated 2408.11770: "The HST Cepheid and JWST distance measurements themselves are in good agreement"] Fig. 5 caption; the numbers are in Sec. II.3, Table 2 (TRGB 0.032, JAGB 0.047, Cepheids -0.027 mag; uncertainties 0.05-0.10 mag) -/
  | stat_agree
  /-- STAT [stated 2408.11770: "we find the values inferred using JWST are consistent with expectations for every subsample"] Sec. III.3 (next sentence: at or within 1 sigma of these smaller uncertainties, i.e. between HST and JWST excluding SNe; Table 4) -/
  | stat_resid
  /-- STAT [stated 2408.11770: "For the combination of these three methods, F24 reports $70$ $\,\rm km\,s^{-1}\,Mpc^{-1}$ , near the HST -expected value of $\sim$ 70.8 $\pm 2.3$"] Sec. III.2 (also: F24's JWST Cepheids about 72 and NIR-TRGB near the HST-expected about 71) -/
  | stat_f24
  /-- GAP [reconstructed] our reading of the paper's inference: the two reported values, the attribution of their difference to selection, agreement on the same hosts, a within-1 sigma comparison, and the right quantity together make the difference entirely consistent with selection; the paper states the conclusion but not this rule, and no textbook supplies it (a standard definition of consistency within errors, e.g. Taylor 1997, covers only the last comparison) -/
  | gap_rule
  deriving DecidableEq, Repr

def prov : Field → Prov
  | .stat_full => .stated
  | .stat_sel => .stated
  | .stat_drop => .stated
  | .stat_agree => .stated
  | .stat_resid => .stated
  | .stat_f24 => .stated
  | .gap_rule => .reconstructed

def prem : Field → Vocab → Prop
  | .stat_full, v => v.h_full ≥ 732
  | .stat_sel, v => v.h_sel ≤ 712
  | .stat_drop, v => v.ExpDrop
  | .stat_agree, v => v.AgreeSameHost
  | .stat_resid, v => v.ResidSmall
  | .stat_f24, v => v.F24Near
  | .gap_rule, v => v.h_full ≥ 732 → v.h_sel ≤ 712 → v.ExpDrop → v.AgreeSameHost → v.ResidSmall → v.F24Near → v.ConsSel

/-- [stated 2408.11770: "between the CCHP JWST program and the full HST sample is entirely consistent with differences in sample selection"] Abstract -/
def Conclusion (v : Vocab) : Prop := v.ConsSel

-- FIXED BLOCK B (identical in every study)
def Premises (v : Vocab) : Prop := ∀ f, prem f v
def Without (g : Field) (v : Vocab) : Prop := ∀ f, f ≠ g → prem f v
def Stated (v : Vocab) : Prop := ∀ f, prov f = .stated → prem f v
def Explicit (v : Vocab) : Prop := ∀ f, prov f ≠ .reconstructed → prem f v
-- END FIXED BLOCK B

/-- The paper's chain, step by step. -/
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  exact p .gap_rule (p .stat_full) (p .stat_sel) (p .stat_drop) (p .stat_agree) (p .stat_resid)
    (p .stat_f24)  -- Abstract, Sec. II.3, III.2-3; GAP

theorem final_nontrivial : ¬ ∀ v : Vocab, Conclusion v :=
  fun h => h ⟨0, 0, False, False, False, False, False⟩

theorem consistent : ∃ v, Premises v :=
  ⟨⟨732, 712, True, True, True, True, True⟩, by intro f; cases f <;> simp [prem]⟩

theorem alone_insufficient : ∀ g, ¬ ∀ v, prem g v → Conclusion v := by
  intro g h
  cases g
  case gap_rule => exact h ⟨0, 999, False, False, False, False, False⟩ (by simp [prem])
  all_goals exact h ⟨732, 712, True, True, True, True, False⟩ (by simp [prem])

theorem stat_full_needed : ¬ ∀ v, Without .stat_full v → Conclusion v := fun h =>
  h ⟨0, 712, True, True, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem stat_sel_needed : ¬ ∀ v, Without .stat_sel v → Conclusion v := fun h =>
  h ⟨732, 999, True, True, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem stat_drop_needed : ¬ ∀ v, Without .stat_drop v → Conclusion v := fun h =>
  h ⟨732, 712, False, True, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem stat_agree_needed : ¬ ∀ v, Without .stat_agree v → Conclusion v := fun h =>
  h ⟨732, 712, True, False, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem stat_resid_needed : ¬ ∀ v, Without .stat_resid v → Conclusion v := fun h =>
  h ⟨732, 712, True, True, False, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem stat_f24_needed : ¬ ∀ v, Without .stat_f24 v → Conclusion v := fun h =>
  h ⟨732, 712, True, True, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem gap_rule_needed : ¬ ∀ v, Without .gap_rule v → Conclusion v := fun h =>
  h ⟨732, 712, True, True, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

/-- What the paper writes is not enough: the rule from the facts to "consistent" (gap_rule, our
reading) is not stated. -/
theorem stated_insufficient : ¬ ∀ v, Stated v → Conclusion v := fun h =>
  h ⟨732, 712, True, True, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])

/-- Consequence of the encoding, not evidence of a defect: the paper leaves its inference rule
implicit, and we encode it as the reconstructed premise gap_rule, whose consequent is the
conclusion; without it the stated facts do not entail the conclusion. -/
theorem explicit_insufficient : ¬ ∀ v, Explicit v → Conclusion v := fun h =>
  h ⟨732, 712, True, True, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])

end Argument
