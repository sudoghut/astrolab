/-
Argument of the paper, decomposed: Agazie et al. 2023 (NANOGrav), "The NANOGrav 15 yr Data Set:
Evidence for a Gravitational-wave Background" (ApJL 951, L8; arXiv:2306.16213). The comparison
with astrophysical models is delegated by the paper to its companion, Agazie et al. 2023
(ApJL 952, L37; arXiv:2306.16220; erratum ApJL 1006, L67, 2026), which supplies two premises.

Scope (narrower than the paper). The quoted sentence of Sec. III, "These amplitudes ...", refers
to both amplitudes of the preceding sentence: A = 2.4e-15 at gamma = 13/3 and A = 6.4e-15 with
gamma free. Only the gamma = 13/3 amplitude is formalised here: the published predictions are
quoted at a fixed spectral shape (gamma = 13/3), so comparing them with the free-gamma amplitude
is not like for like. The encoded conclusion is therefore weaker than the paper's sentence.
The spectral-index statement, the statement that more exotic sources cannot be excluded, and the
Hellings-Downs significance are not formalised (see the wiki article, part 2).

The chain (two routes to compatibility with models, then one gap):
  L8 infers the GWB amplitude at gamma = 13/3: median 2.4e-15 (90% interval 1.8e-15 to 3.1e-15)
  route 1: the 90% credible interval overlaps the 16th-84th percentile range of at least one
      published prediction (L37, Table A1); [gap] a measurement whose credible interval
      overlaps a model's predicted range is not in tension with that model (overlap is only a
      descriptive comparison, not a tension test)
  route 2: L37's own holodeck populations reproduce the inferred amplitude and spectral shape;
      [gap] applied to the gamma = 13/3 amplitude, a population that reproduces it is compatible
      with it (L37 compares the populations with its own spectra, not with this amplitude)
  [gap] the models (published predictions or holodeck populations) that overlap or reproduce the amplitude
      represent astrophysical expectations for SMBHBs (L37 itself says the amplitude needs
      parameters at the edges of expected values and lies at the high end of the predictions)
  [implied] compatibility with representative models is compatibility with the expectations
  -> the gamma = 13/3 amplitude is compatible with astrophysical expectations of a GWB from SMBHBs

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
  /-- The number of published model predictions (L37 Table A1, 16th to 84th percentile of A_yr) whose range overlaps the 90% credible interval of the amplitude (closed intervals; rows counted as listed). -/
  n_overlap : Nat
  /-- Some of the holodeck SMBHB populations of L37 reproduce the inferred GWB amplitude and spectral shape (only the amplitude part is used below). -/
  HoloRepro : Prop
  /-- The gamma = 13/3 amplitude is compatible with at least one SMBHB-population model (a published prediction or a holodeck population). -/
  CompatModels : Prop
  /-- The models that overlap or reproduce the amplitude represent the astrophysical expectations for a GWB from SMBHBs (they are not outlying or edge-of-prior models). -/
  Representative : Prop
  /-- The gamma = 13/3 amplitude is compatible with astrophysical expectations of a GWB from inspiraling SMBHBs. -/
  CompatSMBHB : Prop

/-- The premises. -/
inductive Field where
  /-- STAT [stated 2306.16213: "the strain amplitude is 2.4−0.6+0.7×10−15 (median + 90% credible interval) at a reference frequency of 1 yr−1"] Abstract; Sec. III -/
  | stat_amp
  /-- NUM [stated 2306.16220: "Although the inferred GWB amplitudes are within the range of some of these model predictions"] Sec. V; Table A1, Fig. A1 (68% ranges); within the range implies overlap, so the body is no stronger than the quote; the quote concerns the amplitudes L37 inferred (its 5-bin fits, A_yr about 2.1e-15) while the binding uses our 14-bin 90% interval, a substitution of ours NUM[results/r2b.json:n_models_overlap_ci90 >= 1] -/
  | num_overlap
  /-- GAP [reconstructed] a measurement whose 90% credible interval overlaps the 16th to 84th percentile range predicted by a model is not in tension with that model; neither paper defines a tension criterion for Table A1, and interval overlap alone is a descriptive comparison (two intervals can overlap while the distributions are in tension), so this step of route 1 is ours -/
  | gap_overlap
  /-- STAT [stated 2306.16220: "we are able to reproduce the inferred GWB amplitude and spectral shape"] Sec. V -/
  | stat_holo
  /-- GAP [reconstructed] a population model whose predicted spectra reproduce the measured spectrum is not in tension with the gamma = 13/3 amplitude; L37 compares the holodeck populations with its own 15 yr spectra (a posterior predictive check in the sense of Gelman et al. 2013, ch. 6), so applying the result to the gamma = 13/3 amplitude of L8 is our reading, and only the amplitude part of reproduce the amplitude and spectral shape is used -/
  | gap_holo
  /-- GAP [reconstructed] the models that overlap or reproduce the amplitude stand for astrophysical expectations in general; L37 (arXiv:2306.16220) says in its abstract that the amplitude needs either many parameters at the edges of expected values or a few notably different from standard expectations, and in Sec. V and App. A that it lies at the high-amplitude end of the predicted ranges; Sec. V calls the reproducing parameter choices reasonable, but reasonable is not the same as representative of expectations, so compatibility with some models does not by itself give compatibility with expectations -/
  | gap_repr
  /-- MOD [implied] inference rule: compatibility with models that represent the expectations is compatibility with the expectations (definitional unfolding of the claim; modus ponens, Enderton 2001, A Mathematical Introduction to Logic, ch. 1) -/
  | mod_rule
  deriving DecidableEq, Repr

def prov : Field → Prov
  | .stat_amp => .stated
  | .num_overlap => .stated
  | .gap_overlap => .reconstructed
  | .stat_holo => .stated
  | .gap_holo => .reconstructed
  | .gap_repr => .reconstructed
  | .mod_rule => .implied

def prem : Field → Vocab → Prop
  | .stat_amp, v => v.AmpMeasured
  | .num_overlap, v => v.n_overlap ≥ 1
  | .gap_overlap, v => v.AmpMeasured → v.n_overlap ≥ 1 → v.CompatModels
  | .stat_holo, v => v.HoloRepro
  | .gap_holo, v => v.AmpMeasured → v.HoloRepro → v.CompatModels
  | .gap_repr, v => v.Representative
  | .mod_rule, v => v.CompatModels → v.Representative → v.CompatSMBHB

/-- [stated 2306.16213: "These amplitudes are compatible with astrophysical expectations of a GWB from inspiraling SMBHBs"] Sec. III. Narrowed: the sentence covers both the gamma = 13/3 and the free-gamma amplitude; only the former is encoded (see the header). -/
def Conclusion (v : Vocab) : Prop := v.CompatSMBHB

-- FIXED BLOCK B (identical in every study)
def Premises (v : Vocab) : Prop := ∀ f, prem f v
def Without (g : Field) (v : Vocab) : Prop := ∀ f, f ≠ g → prem f v
def Stated (v : Vocab) : Prop := ∀ f, prov f = .stated → prem f v
def Explicit (v : Vocab) : Prop := ∀ f, prov f ≠ .reconstructed → prem f v
-- END FIXED BLOCK B

/-- The paper's chain, step by step (route 1; route 2 is shown in num_overlap_redundant). -/
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  have h1 : v.CompatModels := p .gap_overlap (p .stat_amp) (p .num_overlap)  -- Sec. III; L37 Sec. V, App. A
  exact p .mod_rule h1 (p .gap_repr)  -- Sec. III; GAP

theorem final_nontrivial : ¬ ∀ v : Vocab, Conclusion v :=
  fun h => h ⟨False, 0, False, False, False, False⟩

theorem consistent : ∃ v, Premises v :=
  ⟨⟨True, 1, True, True, True, True⟩, by intro f; cases f <;> simp [prem]⟩

theorem alone_insufficient : ∀ g, ¬ ∀ v, prem g v → Conclusion v := by
  intro g h
  cases g
  case mod_rule => exact h ⟨False, 0, False, False, False, False⟩ (by simp [prem])
  all_goals exact h ⟨True, 1, True, True, True, False⟩ (by simp [prem])

theorem stat_amp_needed : ¬ ∀ v, Without .stat_amp v → Conclusion v := fun h =>
  h ⟨False, 1, True, False, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

/-- Redundant: route 2 (the holodeck populations) gives compatibility with models without the
Table A1 count. Our NUM test checks route 1 only. -/
theorem num_overlap_redundant : ∀ v, Without .num_overlap v → Conclusion v := by
  intro v p
  exact p .mod_rule (by decide)
    (p .gap_holo (by decide) (p .stat_amp (by decide)) (p .stat_holo (by decide)))
    (p .gap_repr (by decide))

/-- Redundant for the same reason: route 2 does not use it. -/
theorem gap_overlap_redundant : ∀ v, Without .gap_overlap v → Conclusion v := by
  intro v p
  exact p .mod_rule (by decide)
    (p .gap_holo (by decide) (p .stat_amp (by decide)) (p .stat_holo (by decide)))
    (p .gap_repr (by decide))

/-- Redundant: route 1 (Table A1) gives compatibility with models without the holodeck result. -/
theorem stat_holo_redundant : ∀ v, Without .stat_holo v → Conclusion v := by
  intro v p
  exact p .mod_rule (by decide)
    (p .gap_overlap (by decide) (p .stat_amp (by decide)) (p .num_overlap (by decide)))
    (p .gap_repr (by decide))

/-- Redundant for the same reason: route 1 does not use it. -/
theorem gap_holo_redundant : ∀ v, Without .gap_holo v → Conclusion v := by
  intro v p
  exact p .mod_rule (by decide)
    (p .gap_overlap (by decide) (p .stat_amp (by decide)) (p .num_overlap (by decide)))
    (p .gap_repr (by decide))

theorem gap_repr_needed : ¬ ∀ v, Without .gap_repr v → Conclusion v := fun h =>
  h ⟨True, 1, True, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem mod_rule_needed : ¬ ∀ v, Without .mod_rule v → Conclusion v := fun h =>
  h ⟨True, 1, True, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

/-- What the papers write is not enough: the inference steps are standard background (implied)
or not established (route 1 overlap step, representativeness). -/
theorem stated_insufficient : ¬ ∀ v, Stated v → Conclusion v := fun h =>
  h ⟨True, 1, True, False, False, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])

/-- Even with standard knowledge the chain has a gap on both routes (route 1 also needs
gap_overlap, route 2 also needs gap_holo): compatibility with some
models (published predictions or holodeck populations) does not give compatibility with
astrophysical expectations unless those models represent the expectations (gap_repr). -/
theorem explicit_insufficient : ¬ ∀ v, Explicit v → Conclusion v := fun h =>
  h ⟨True, 1, True, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])

end Argument
