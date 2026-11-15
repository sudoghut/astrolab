/-
Argument of the paper, decomposed: DES Collaboration 2026, "Dark Energy Survey Year 6 Results:
Cosmological Constraints from Galaxy Clustering and Weak Lensing" (arXiv:2601.14559v2; "D26").

The conclusion encoded is the comparison with the primary CMB in the conclusions (Sec. VIII):
no substantial evidence for a discrepancy with the CMB, in S8 or in the full parameter space.

The chain:
  the CMB reference is the primary temperature and polarization combination of Planck 2018,
      ACT-DR6 and SPT-3G DR1, without CMB lensing
  consistency is measured by the parameter-difference probability (Sec. IV.6, eqs. 17-19)
  full-space difference 1.8 sigma; projected onto S8, 2.6 sigma (Sec. V.2, VIII)
  prior-volume (projection) effects on the fiducial posterior are below 0.5 sigma (App. B)
  [gap] below 3 sigma, in both the S8 projection and the full space, there is no substantial
      evidence for a discrepancy (an informal usage, 3 sigma as evidence, not an authoritative
      rule; D26 does not state it)
  -> no substantial evidence for a discrepancy with the CMB
  (the n_sigma below 3 criterion of Sec. IV.6 licenses combining the data sets; it is encoded
  but does not carry the conclusion, see mod_crit_redundant)

Numbers are encoded in tenths of a sigma (Nat), as the reported values rounded to one decimal;
a premise n_x10 = 18 states the reported, rounded 1.8.
Quotes follow the arXiv HTML version v2; mathematics is quoted in its LaTeX source form.

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
  /-- The CMB reference is the primary temperature and polarization likelihood combination of Planck 2018, ACT-DR6 and SPT-3G DR1, without CMB lensing. -/
  CmbPrimary : Prop
  /-- Consistency between DES and the CMB is measured by the parameter-difference probability of Sec. IV.6 (eqs. 17-19), converted to an effective number of sigma. -/
  MetricUsed : Prop
  /-- The full-parameter-space difference between DES Y6 3x2pt and the CMB, in tenths of a sigma (rounded to the nearest tenth). -/
  n_full_x10 : Nat
  /-- The difference projected onto S8, in tenths of a sigma (rounded to the nearest tenth). -/
  n_s8_x10 : Nat
  /-- DES Y6 3x2pt and the CMB agree well enough that examining their combined constraint makes sense. -/
  Combinable : Prop
  /-- Prior-volume (projection) effects on the fiducial DES posterior are small (below 0.5 sigma). -/
  ProjSmall : Prop
  /-- There is no substantial evidence for a discrepancy between DES Y6 3x2pt and the CMB, in S8 or the full parameter space. -/
  NoEvidence : Prop

/-- The premises. -/
inductive Field where
  /-- OBS [stated: "for primary temperature and polarization data, but without CMB lensing"] Sec. V.2 (Planck 2018, ACT-DR6, SPT-3G DR1) -/
  | obs_cmb
  /-- MOD [stated: "We measure consistency from the probability of a parameter difference"] Sec. IV.6, eqs. 17-19 -/
  | mod_metric
  /-- STAT [stated: "we find a full parameter space difference of 1.8"] Sec. VIII (also Sec. V.2, Table 6: PTE 0.08); encoded as the reported value, 18 tenths -/
  | stat_full
  /-- STAT [stated: "the difference increases to 2.6"] Sec. VIII (projected onto S8; also Sec. V.2); encoded as the reported value, 26 tenths -/
  | stat_s8
  /-- MOD [stated: "We set $n_{\sigma}<3$ as the criterion for different data sets agreeing well enough that it makes sense to examine their combined constraint"] Sec. IV.6; D26 states the criterion generically and applies it to the full-space number (Sec. V.2: As such, we are able to combine) -/
  | mod_crit
  /-- STAT [stated: "exhibits minor prior-volume effects of less than $0.5\sigma$ for all parameters of interest"] App. B (fiducial linear-bias 3x2pt in LCDM) -/
  | stat_proj
  /-- GAP [reconstructed] with the parameter-difference metric and small projection effects, a Gaussian-equivalent difference below 3 sigma in both the S8 projection and the full space means no substantial evidence for a discrepancy. This is the informal usage of 3 sigma as the level of evidence; it is not an authoritative rule (Lyons 2013, arXiv:1310.1284, discusses 5 sigma for discovery and argues against uniform thresholds), and D26 does not state it: its Sec. VIII sentence cites significances from about 1 to at most 3 sigma -/
  | gap_conv
  deriving DecidableEq, Repr

def prov : Field → Prov
  | .obs_cmb => .stated
  | .mod_metric => .stated
  | .stat_full => .stated
  | .stat_s8 => .stated
  | .mod_crit => .stated
  | .stat_proj => .stated
  | .gap_conv => .reconstructed

def prem : Field → Vocab → Prop
  | .obs_cmb, v => v.CmbPrimary
  | .mod_metric, v => v.MetricUsed
  | .stat_full, v => v.n_full_x10 = 18
  | .stat_s8, v => v.n_s8_x10 = 26
  | .mod_crit, v => v.n_full_x10 < 30 → v.Combinable
  | .stat_proj, v => v.ProjSmall
  | .gap_conv, v => v.MetricUsed → v.ProjSmall → v.n_s8_x10 < 30 → v.n_full_x10 < 30 → v.NoEvidence

/-- [stated: "we see no substantial evidence for a discrepancy with the CMB in either"] Sec. VIII (S8 or the full parameter space) -/
def Conclusion (v : Vocab) : Prop := v.NoEvidence

-- FIXED BLOCK B (identical in every study)
def Premises (v : Vocab) : Prop := ∀ f, prem f v
def Without (g : Field) (v : Vocab) : Prop := ∀ f, f ≠ g → prem f v
def Stated (v : Vocab) : Prop := ∀ f, prov f = .stated → prem f v
def Explicit (v : Vocab) : Prop := ∀ f, prov f ≠ .reconstructed → prem f v
-- END FIXED BLOCK B

/-- The paper's chain, step by step. -/
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  have hfull : v.n_full_x10 = 18 := p .stat_full          -- Sec. V.2, VIII: 1.8 sigma
  have hs8 : v.n_s8_x10 = 26 := p .stat_s8                -- Sec. V.2, VIII: 2.6 sigma
  exact p .gap_conv (p .mod_metric) (p .stat_proj) (by omega) (by omega)  -- GAP: 3 sigma usage

theorem final_nontrivial : ¬ ∀ v : Vocab, Conclusion v :=
  fun h => h ⟨False, False, 0, 0, False, False, False⟩

theorem consistent : ∃ v, Premises v :=
  ⟨⟨True, True, 18, 26, True, True, True⟩, by intro f; cases f <;> simp [prem]⟩

theorem alone_insufficient : ∀ g, ¬ ∀ v, prem g v → Conclusion v := by
  intro g h
  cases g
  case gap_conv => exact h ⟨False, False, 99, 99, False, False, False⟩ (by simp [prem])
  all_goals exact h ⟨True, True, 18, 26, True, True, False⟩ (by simp [prem])

theorem mod_metric_needed : ¬ ∀ v, Without .mod_metric v → Conclusion v := fun h =>
  h ⟨True, False, 18, 26, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem stat_full_needed : ¬ ∀ v, Without .stat_full v → Conclusion v := fun h =>
  h ⟨True, True, 99, 26, False, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem stat_s8_needed : ¬ ∀ v, Without .stat_s8 v → Conclusion v := fun h =>
  h ⟨True, True, 18, 99, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem stat_proj_needed : ¬ ∀ v, Without .stat_proj v → Conclusion v := fun h =>
  h ⟨True, True, 18, 26, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem gap_conv_needed : ¬ ∀ v, Without .gap_conv v → Conclusion v := fun h =>
  h ⟨True, True, 18, 26, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

/-- Redundant: which CMB combination is the reference does not enter the inference in this
encoding (its atom appears nowhere else); the reference matters for the numbers, not the logic. -/
theorem obs_cmb_redundant : ∀ v, Without .obs_cmb v → Conclusion v := by
  intro v p
  have hfull : v.n_full_x10 = 18 := p .stat_full (by decide)
  have hs8 : v.n_s8_x10 = 26 := p .stat_s8 (by decide)
  exact p .gap_conv (by decide) (p .mod_metric (by decide)) (p .stat_proj (by decide)) (by omega) (by omega)

/-- Redundant: the combination criterion of Sec. IV.6 licenses combining the data sets; it does
not carry the no-evidence conclusion. -/
theorem mod_crit_redundant : ∀ v, Without .mod_crit v → Conclusion v := by
  intro v p
  have hfull : v.n_full_x10 = 18 := p .stat_full (by decide)
  have hs8 : v.n_s8_x10 = 26 := p .stat_s8 (by decide)
  exact p .gap_conv (by decide) (p .mod_metric (by decide)) (p .stat_proj (by decide)) (by omega) (by omega)

/-- What the paper writes is not enough: it does not state the rule that turns sub-3-sigma
numbers into no substantial evidence. -/
theorem stated_insufficient : ¬ ∀ v, Stated v → Conclusion v := fun h =>
  h ⟨True, True, 18, 26, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])

/-- Standard knowledge does not supply that rule either: 3 sigma as the level of evidence is an
informal usage, not an authoritative convention. -/
theorem explicit_insufficient : ¬ ∀ v, Explicit v → Conclusion v := fun h =>
  h ⟨True, True, 18, 26, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])

end Argument
