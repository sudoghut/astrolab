/-
Argument of the paper, decomposed: Cookson, Banik, El-Badry, Sutherland, Penoyre, Pittordis and
Clarke 2026, "A Quality Framework for Testing Gravity with Wide Binaries: No Evidence for MOND"
(arXiv:2602.24035, MNRAS). Banik et al. 2024 (arXiv:2311.03436) and Chae 2023 (arXiv:2305.04613)
supply context in the wiki article; the chain below is the 2026 paper's own.

The chain (the conclusion encoded is the quantitative one, "up to 1500x more likely"):
  MOND predicts wide binaries beyond the MOND radius orbit about 20% faster (a step in the median
      scaled velocity against r_sky / r_M)
  the paper compiles a high-purity sample within 130 pc
  in that sample the median scaled velocity is flat across r_sky / r_M (no 20% step)
  the paper assumes the eccentricity distribution and the undetected close-binary incidence do
      not vary with separation
  chi-square fits with per-bin median errors give a large Delta chi2 (about 12-16)
  [gap] the per-bin median errors are correctly calibrated (not underestimated)
  -> Newtonian gravity is up to 1500x more likely than MOND

Rules: AGENTS.md section 2 (paper study, Lean); specification: design/007 section 2.2.
Quotes follow the arXiv HTML text, with math in its LaTeX source form.
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
  /-- The median scaled relative velocity of the cleaned sample shows no 20% step with r_sky / r_M. -/
  Flat : Prop
  /-- MOND predicts that wide binaries beyond the MOND radius orbit about 20% faster than Newtonian (a step in the median scaled velocity). -/
  MondStep : Prop
  /-- The 130 pc sample is of high purity (contaminants such as close binaries and flybys largely removed). -/
  Pure : Prop
  /-- The eccentricity distribution and the incidence of undetected close binaries do not vary with separation. -/
  NoTrend : Prop
  /-- The chi-square comparison gives a large Delta chi2 between MOND and Newton (about 12 to 16). -/
  LRBig : Prop
  /-- The per-bin uncertainties of the median scaled velocity used in the chi-square are not underestimated. -/
  ErrCal : Prop
  /-- Newtonian gravity is strongly favoured over MOND (likelihood ratio of order 1000). -/
  NewtonStrong : Prop

/-- The premises. -/
inductive Field where
  /-- STAT [stated 2602.24035: "does not exhibit the 20% enhancement expected from MOND and is consistent with Newtonian gravity across all separations"] Abstract -/
  | stat_flat
  /-- MOD [stated 2602.24035: "should orbit each other 20% faster than the Newtonian expectation if their separation exceeds"] Sec. 8 (cites Eq. 3); step shape Eq. 7 -/
  | mod_step
  /-- STAT [stated 2602.24035: "we compile a high-purity sample of WBs within 130 pc"] Abstract -/
  | stat_pure
  /-- MOD [stated 2602.24035: "Our conclusion assumes that the WB eccentricity distribution and the incidence of undetected CBs do not vary with the WB separation"] Sec. 5 -/
  | mod_notrend
  /-- STAT [stated 2602.24035: "The $\Delta\chi^{2}$ of about $12-16$ implies a likelihood ratio"] Sec. 5 (Table 3) -/
  | stat_lr
  /-- GAP [reconstructed] the per-bin median errors are calibrated; the paper takes the uncertainty of the median as MAD / sqrt(N) (Sec. 4.2.1), while the standard error of a median is 1/(2 f(m) sqrt(N)), about 1.4 to 2.1 MAD / sqrt(N) for plausible shapes (1.86 for a Gaussian; Kendall and Stuart, The Advanced Theory of Statistics, Vol. 1); the study tests this with a bootstrap (R2) -/
  | gap_err
  /-- MOD [implied] standard model comparison: a model predicting a step is disfavoured when unbiased, calibrated data are flat and Delta chi2 is large (likelihood-ratio reasoning, e.g. Wasserman 2004, All of Statistics, ch. 10) -/
  | mod_rule
  deriving DecidableEq, Repr

def prov : Field → Prov
  | .stat_flat => .stated
  | .mod_step => .stated
  | .stat_pure => .stated
  | .mod_notrend => .stated
  | .stat_lr => .stated
  | .gap_err => .reconstructed
  | .mod_rule => .implied

def prem : Field → Vocab → Prop
  | .stat_flat, v => v.Flat
  | .mod_step, v => v.MondStep
  | .stat_pure, v => v.Pure
  | .mod_notrend, v => v.NoTrend
  | .stat_lr, v => v.LRBig
  | .gap_err, v => v.ErrCal
  | .mod_rule, v => v.Flat → v.MondStep → v.Pure → v.NoTrend → v.ErrCal → v.LRBig → v.NewtonStrong

/-- [stated 2602.24035: "Newtonian gravity is up to $1500\times$ more likely than MOND for our cleanest sample"] Abstract -/
def Conclusion (v : Vocab) : Prop := v.NewtonStrong

-- FIXED BLOCK B (identical in every study)
def Premises (v : Vocab) : Prop := ∀ f, prem f v
def Without (g : Field) (v : Vocab) : Prop := ∀ f, f ≠ g → prem f v
def Stated (v : Vocab) : Prop := ∀ f, prov f = .stated → prem f v
def Explicit (v : Vocab) : Prop := ∀ f, prov f ≠ .reconstructed → prem f v
-- END FIXED BLOCK B

/-- The paper's chain, step by step. -/
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  exact p .mod_rule (p .stat_flat) (p .mod_step) (p .stat_pure) (p .mod_notrend) (p .gap_err)
    (p .stat_lr)  -- Abstract, Sec. 4.2.1, 5, 8; GAP

theorem final_nontrivial : ¬ ∀ v : Vocab, Conclusion v :=
  fun h => h ⟨False, False, False, False, False, False, False⟩

theorem consistent : ∃ v, Premises v :=
  ⟨⟨True, True, True, True, True, True, True⟩, by intro f; cases f <;> simp [prem]⟩

theorem alone_insufficient : ∀ g, ¬ ∀ v, prem g v → Conclusion v := by
  intro g h
  cases g
  case mod_rule => exact h ⟨False, False, False, False, False, False, False⟩ (by simp [prem])
  all_goals exact h ⟨True, True, True, True, True, True, False⟩ (by simp [prem])

theorem stat_flat_needed : ¬ ∀ v, Without .stat_flat v → Conclusion v := fun h =>
  h ⟨False, True, True, True, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem mod_step_needed : ¬ ∀ v, Without .mod_step v → Conclusion v := fun h =>
  h ⟨True, False, True, True, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem stat_pure_needed : ¬ ∀ v, Without .stat_pure v → Conclusion v := fun h =>
  h ⟨True, True, False, True, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem mod_notrend_needed : ¬ ∀ v, Without .mod_notrend v → Conclusion v := fun h =>
  h ⟨True, True, True, False, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem stat_lr_needed : ¬ ∀ v, Without .stat_lr v → Conclusion v := fun h =>
  h ⟨True, True, True, True, False, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem gap_err_needed : ¬ ∀ v, Without .gap_err v → Conclusion v := fun h =>
  h ⟨True, True, True, True, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem mod_rule_needed : ¬ ∀ v, Without .mod_rule v → Conclusion v := fun h =>
  h ⟨True, True, True, True, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

/-- What the paper writes is not enough: the inference rule is standard background (implied), and
the calibration of the per-bin median errors is not established. -/
theorem stated_insufficient : ¬ ∀ v, Stated v → Conclusion v := fun h =>
  h ⟨True, True, True, True, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])

/-- Even with standard knowledge the chain has a gap: the per-bin median errors must not be
underestimated for Delta chi2 to carry the stated likelihood ratio (gap_err). -/
theorem explicit_insufficient : ¬ ∀ v, Explicit v → Conclusion v := fun h =>
  h ⟨True, True, True, True, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])

end Argument
