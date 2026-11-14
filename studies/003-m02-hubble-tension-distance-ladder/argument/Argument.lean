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
  observed: CCHP JWST program lower than the full HST sample by about 2.5
  on the same CCHP hosts, JWST JAGB and HST Cepheid distances agree within errors
  -> the leftover (about 0.5) is within the subsample uncertainty (about 2)
  -> the 2.5 difference is entirely consistent with differences in sample selection

Rules: AGENTS.md section 2 (paper study, Lean); specification: design/007 section 2.2.
H0 values and differences are in tenths of km/s/Mpc (Nat): 73.2 is 732, 2.5 is 25.
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
  /-- H0 from the full HST sample (42 SNe Ia, 4 anchors), tenths of km/s/Mpc. -/
  h_full : Nat
  /-- H0 from HST Cepheids on the 10 CCHP-selected hosts (11 SNe Ia), NGC 4258 anchor, tenths. -/
  h_sel : Nat
  /-- Observed H0 difference between the CCHP JWST program and the full HST sample, tenths. -/
  h_gap : Nat
  /-- Choosing the CCHP hosts and anchor is expected to lower H0 by about 2 km/s/Mpc. -/
  ExpDrop : Prop
  /-- On the CCHP JWST sample, JWST JAGB and HST Cepheid distances agree within their errors. -/
  AgreeJAGB : Prop
  /-- The part of the observed difference not expected from selection is within the subsample uncertainty. -/
  ResidSmall : Prop
  /-- The observed difference is entirely consistent with differences in sample selection. -/
  ConsSel : Prop

/-- The premises. -/
inductive Field where
  /-- STAT [stated 2408.11770: "is not yet competitive with the HST set (42 SNe Ia and 4 anchors), which yields 73.2 $\pm$ 0.9"] Abstract -/
  | stat_full
  /-- STAT [stated 2408.11770: "a corresponding value of H ${}_{0}=71.2$"] Sec. III.2 (HST Cepheids on the CCHP-selected hosts) -/
  | stat_sel
  /-- STAT [stated 2408.11770: "We show that $\Delta$ H ${}_{0}\sim$ 2.5"] Abstract (CCHP JWST program versus the full HST sample; about 2.5, encoded as at most 3.0) -/
  | stat_gap
  /-- MOD [stated 2408.11770: "thus 2.0 $\,\rm km\,s^{-1}\,Mpc^{-1}$ lower than the full HST sample—simply due to the choice of SN hosts and anchor"] Sec. III.2 -/
  | mod_drop
  /-- STAT [stated 2408.11770: "For comparisons between JWST JAGB and HST Cepheids, we measure a difference with the CCHP JWST sample of $0.047\pm 0.066$ mag"] Sec. III -/
  | stat_agree
  /-- MOD [implied] a leftover of at most about 1 km/s/Mpc (observed about 2.5 minus expected about 2.0) is within the uncertainty of an 11-SN subsample H0 (about 2 km/s/Mpc, the paper Table 4); comparison of a difference with its standard error (e.g. Taylor 1997, An Introduction to Error Analysis) -/
  | mod_resid
  /-- MOD [implied] inference rule: if the selection is expected to produce the shift, the same-host distances agree, and the leftover is within errors, the observed difference is consistent with selection (consistency means no part is significant beyond errors; same textbook) -/
  | mod_cons
  deriving DecidableEq, Repr

def prov : Field → Prov
  | .stat_full => .stated
  | .stat_sel => .stated
  | .stat_gap => .stated
  | .mod_drop => .stated
  | .stat_agree => .stated
  | .mod_resid => .implied
  | .mod_cons => .implied

def prem : Field → Vocab → Prop
  | .stat_full, v => v.h_full ≥ 731
  | .stat_sel, v => v.h_sel ≤ 712
  | .stat_gap, v => v.h_gap ≤ 30
  | .mod_drop, v => v.h_full ≥ 731 → v.h_sel ≤ 712 → v.ExpDrop
  | .stat_agree, v => v.AgreeJAGB
  | .mod_resid, v => v.h_gap ≤ 30 → v.ExpDrop → v.ResidSmall
  | .mod_cons, v => v.ExpDrop → v.AgreeJAGB → v.ResidSmall → v.ConsSel

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
  have d : v.ExpDrop := p .mod_drop (p .stat_full) (p .stat_sel)   -- Sec. III.2
  have r : v.ResidSmall := p .mod_resid (p .stat_gap) d             -- Abstract, Table 4
  exact p .mod_cons d (p .stat_agree) r                             -- Abstract

theorem final_nontrivial : ¬ ∀ v : Vocab, Conclusion v :=
  fun h => h ⟨0, 0, 0, False, False, False, False⟩

theorem consistent : ∃ v, Premises v :=
  ⟨⟨731, 712, 25, True, True, True, True⟩, by intro f; cases f <;> simp [prem]⟩

theorem alone_insufficient : ∀ g, ¬ ∀ v, prem g v → Conclusion v := by
  intro g h
  cases g
  case mod_drop => exact h ⟨0, 999, 99, False, False, False, False⟩ (by simp [prem])
  case mod_resid => exact h ⟨0, 999, 99, False, False, False, False⟩ (by simp [prem])
  case mod_cons => exact h ⟨0, 999, 99, False, False, False, False⟩ (by simp [prem])
  all_goals exact h ⟨731, 712, 25, False, True, False, False⟩ (by simp [prem])

theorem stat_full_needed : ¬ ∀ v, Without .stat_full v → Conclusion v := fun h =>
  h ⟨0, 712, 25, False, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem stat_sel_needed : ¬ ∀ v, Without .stat_sel v → Conclusion v := fun h =>
  h ⟨731, 999, 25, False, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem stat_gap_needed : ¬ ∀ v, Without .stat_gap v → Conclusion v := fun h =>
  h ⟨731, 712, 99, True, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem mod_drop_needed : ¬ ∀ v, Without .mod_drop v → Conclusion v := fun h =>
  h ⟨731, 712, 25, False, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem stat_agree_needed : ¬ ∀ v, Without .stat_agree v → Conclusion v := fun h =>
  h ⟨731, 712, 25, True, False, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem mod_resid_needed : ¬ ∀ v, Without .mod_resid v → Conclusion v := fun h =>
  h ⟨731, 712, 25, True, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem mod_cons_needed : ¬ ∀ v, Without .mod_cons v → Conclusion v := fun h =>
  h ⟨731, 712, 25, True, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

/-- What the paper writes is not enough: the comparison of the leftover with the subsample
uncertainty and the rule from that to "consistent" are left implicit. -/
theorem stated_insufficient : ¬ ∀ v, Stated v → Conclusion v := fun h =>
  h ⟨731, 712, 25, True, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])

/-- With standard knowledge the chain closes: no reconstructed premise is needed. The conclusion
is a weak one ("consistent with"), which an absence of significant residuals suffices for. -/
theorem explicit_sufficient : ∀ v, Explicit v → Conclusion v := fun v p =>
  final v (fun f => p f (by cases f <;> decide))

end Argument
