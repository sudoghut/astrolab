/-
Argument of the paper, decomposed: Agazie et al. 2023 (NANOGrav), "The NANOGrav 15 yr Data Set:
Evidence for a Gravitational-wave Background" (ApJL 951, L8; arXiv:2306.16213). The comparison
with astrophysical models is delegated by the paper to its companion, Agazie et al. 2023
(ApJL 952, L37; arXiv:2306.16220; erratum ApJL 1006, L67, 2026), which supplies the LIT premise.

The conclusion encoded is the amplitude sentence of Sec. III. The spectral-index statement, the
statement that more exotic sources cannot be excluded, and the Hellings-Downs significance are
not formalised (see the wiki article, part 2).

The chain:
  L8 infers the GWB amplitude at gamma = 13/3: median 2.4e-15 (90% interval 1.8e-15 to 3.1e-15)
  the amplitude lies within the predicted range of at least one published model (L37, Table A1)
  [implied] a value inside a model's predicted range is compatible with that model
  [gap] the models that contain it represent astrophysical expectations for SMBHBs
      (L37 itself places the amplitude at the high end of the predictions)
  [implied] compatibility with representative models is compatibility with the expectations
  -> the amplitude is compatible with astrophysical expectations of a GWB from SMBHBs

Rules: AGENTS.md section 2 (paper study, Lean); specification: design/007 section 2.2.
Quotes follow the arXiv HTML text as rendered (math flattened to text).
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
  /-- The GWB strain amplitude at 1/yr for gamma = 13/3 under the Hellings-Downs model has been inferred, with a posterior median near 2.4e-15. -/
  AmpMeasured : Prop
  /-- The number of published model predictions (L37 Table A1, 16th to 84th percentile of A_yr) whose range contains the median amplitude. -/
  n_contain : Nat
  /-- The amplitude is compatible with at least one published SMBHB-population prediction. -/
  CompatModels : Prop
  /-- The published predictions that contain the amplitude represent the astrophysical expectations for a GWB from SMBHBs (they are not outlying models). -/
  Representative : Prop
  /-- The amplitude is compatible with astrophysical expectations of a GWB from inspiraling SMBHBs. -/
  CompatSMBHB : Prop

/-- The premises. -/
inductive Field where
  /-- STAT [stated 2306.16213: "the strain amplitude is 2.4−0.6+0.7×10−15 (median + 90% credible interval) at a reference frequency of 1 yr−1"] Abstract; Sec. III -/
  | stat_amp
  /-- NUM [stated 2306.16220: "Although the inferred GWB amplitudes are within the range of some of these model predictions"] Sec. V; Table A1, Fig. A1 (68% ranges) NUM[results/r2b.json:n_models_contain_median >= 1] -/
  | num_contain
  /-- MOD [implied] a measured value inside the 16th to 84th percentile range predicted by a model is not in tension with that model (posterior predictive reasoning, Gelman et al. 2013, Bayesian Data Analysis, 3rd ed., ch. 6) -/
  | mod_contain
  /-- GAP [reconstructed] the models whose ranges contain the amplitude stand for astrophysical expectations in general; L37 (arXiv:2306.16220, Sec. V and App. A) says the amplitude lies at the high-amplitude end of the predicted ranges, and its abstract says it needs parameters at the edges of expected values, so compatibility with some models does not by itself give compatibility with expectations -/
  | gap_repr
  /-- MOD [implied] inference rule: compatibility with models that represent the expectations is compatibility with the expectations (definition of the claim; Gelman et al. 2013, ch. 6) -/
  | mod_rule
  deriving DecidableEq, Repr

def prov : Field → Prov
  | .stat_amp => .stated
  | .num_contain => .stated
  | .mod_contain => .implied
  | .gap_repr => .reconstructed
  | .mod_rule => .implied

def prem : Field → Vocab → Prop
  | .stat_amp, v => v.AmpMeasured
  | .num_contain, v => v.n_contain ≥ 1
  | .mod_contain, v => v.AmpMeasured → v.n_contain ≥ 1 → v.CompatModels
  | .gap_repr, v => v.Representative
  | .mod_rule, v => v.CompatModels → v.Representative → v.CompatSMBHB

/-- [stated 2306.16213: "These amplitudes are compatible with astrophysical expectations of a GWB from inspiraling SMBHBs"] Sec. III -/
def Conclusion (v : Vocab) : Prop := v.CompatSMBHB

-- FIXED BLOCK B (identical in every study)
def Premises (v : Vocab) : Prop := ∀ f, prem f v
def Without (g : Field) (v : Vocab) : Prop := ∀ f, f ≠ g → prem f v
def Stated (v : Vocab) : Prop := ∀ f, prov f = .stated → prem f v
def Explicit (v : Vocab) : Prop := ∀ f, prov f ≠ .reconstructed → prem f v
-- END FIXED BLOCK B

/-- The paper's chain, step by step. -/
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  have h1 : v.CompatModels := p .mod_contain (p .stat_amp) (p .num_contain)  -- Sec. III; L37 Sec. V
  exact p .mod_rule h1 (p .gap_repr)  -- Sec. III; GAP

theorem final_nontrivial : ¬ ∀ v : Vocab, Conclusion v :=
  fun h => h ⟨False, 0, False, False, False⟩

theorem consistent : ∃ v, Premises v :=
  ⟨⟨True, 1, True, True, True⟩, by intro f; cases f <;> simp [prem]⟩

theorem alone_insufficient : ∀ g, ¬ ∀ v, prem g v → Conclusion v := by
  intro g h
  cases g
  case mod_rule => exact h ⟨False, 0, False, False, False⟩ (by simp [prem])
  all_goals exact h ⟨True, 1, True, True, False⟩ (by simp [prem])

theorem stat_amp_needed : ¬ ∀ v, Without .stat_amp v → Conclusion v := fun h =>
  h ⟨False, 1, False, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem num_contain_needed : ¬ ∀ v, Without .num_contain v → Conclusion v := fun h =>
  h ⟨True, 0, False, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem mod_contain_needed : ¬ ∀ v, Without .mod_contain v → Conclusion v := fun h =>
  h ⟨True, 1, False, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem gap_repr_needed : ¬ ∀ v, Without .gap_repr v → Conclusion v := fun h =>
  h ⟨True, 1, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem mod_rule_needed : ¬ ∀ v, Without .mod_rule v → Conclusion v := fun h =>
  h ⟨True, 1, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

/-- What the papers write is not enough: both inference steps are standard background (implied),
and representativeness is not established. -/
theorem stated_insufficient : ¬ ∀ v, Stated v → Conclusion v := fun h =>
  h ⟨True, 1, False, False, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])

/-- Even with standard knowledge the chain has a gap: compatibility with some published models
does not give compatibility with astrophysical expectations unless those models represent the
expectations (gap_repr), and L37 places the amplitude at the high end of the predictions. -/
theorem explicit_insufficient : ¬ ∀ v, Explicit v → Conclusion v := fun h =>
  h ⟨True, 1, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])

end Argument
