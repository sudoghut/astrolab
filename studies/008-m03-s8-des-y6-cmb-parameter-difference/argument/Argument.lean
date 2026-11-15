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
  criterion: n_sigma below 3 means the data sets agree well enough to examine their combined
      constraint (Sec. IV.6)
  prior-volume (projection) effects on the fiducial posterior are below 0.5 sigma (App. B)
  [gap] data sets that pass the combination criterion in the full space, with the S8 projection
      also below 3 sigma and small projection effects, show no substantial evidence for a
      discrepancy (D26 uses the criterion only to license combining; the no-evidence sentence in
      Sec. VIII cites a range of significances, not a rule)
  -> no substantial evidence for a discrepancy with the CMB

Numbers are encoded in tenths of a sigma (Nat); a premise of the form n_x10 at most 18 is no
stronger than the reported value 1.8 (rounded to one decimal).

Rules: AGENTS.md section 2 (paper study, Lean); specification: design/007 section 2.2.
Quotes follow the arXiv HTML version v2.
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
  /-- Consistency between DES and the CMB is measured by the parameter-difference probability of Sec. IV.6 (eqs. 17-19). -/
  MetricUsed : Prop
  /-- The full-parameter-space difference between DES Y6 3x2pt and the CMB, in tenths of a sigma. -/
  n_full_x10 : Nat
  /-- The difference projected onto S8, in tenths of a sigma. -/
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
  /-- STAT [stated: "we find a full parameter space difference of 1.8"] Sec. VIII (also Sec. V.2, Table 6); encoded as at most 18 tenths -/
  | stat_full
  /-- STAT [stated: "the difference increases to 2.6"] Sec. VIII (projected onto S8; also Sec. V.2); encoded as at most 26 tenths -/
  | stat_s8
  /-- MOD [stated: "as the criterion for different data sets agreeing well enough that it makes sense to examine their combined constraint"] Sec. IV.6 (the criterion is n_sigma below 3) -/
  | mod_crit
  /-- STAT [stated: "exhibits minor prior-volume effects of less than"] App. B (0.5 sigma, fiducial linear-bias 3x2pt in LCDM) -/
  | stat_proj
  /-- GAP [reconstructed] with the primary CMB as reference and the parameter-difference metric, data sets that pass the combination criterion, whose S8 projection is also below 3 sigma and whose projection effects are small, show no substantial evidence for a discrepancy; D26 states the criterion only as a licence to combine, and its no-evidence sentence cites a range of significances (about 1 to at most 3 sigma) without stating this rule -/
  | gap_bridge
  deriving DecidableEq, Repr

def prov : Field → Prov
  | .obs_cmb => .stated
  | .mod_metric => .stated
  | .stat_full => .stated
  | .stat_s8 => .stated
  | .mod_crit => .stated
  | .stat_proj => .stated
  | .gap_bridge => .reconstructed

def prem : Field → Vocab → Prop
  | .obs_cmb, v => v.CmbPrimary
  | .mod_metric, v => v.MetricUsed
  | .stat_full, v => v.n_full_x10 ≤ 18
  | .stat_s8, v => v.n_s8_x10 ≤ 26
  | .mod_crit, v => v.n_full_x10 < 30 → v.Combinable
  | .stat_proj, v => v.ProjSmall
  | .gap_bridge, v => v.CmbPrimary → v.MetricUsed → v.Combinable → v.n_s8_x10 < 30 → v.ProjSmall → v.NoEvidence

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
  have hfull : v.n_full_x10 ≤ 18 := p .stat_full          -- Sec. V.2, VIII: 1.8 sigma
  have hs8 : v.n_s8_x10 ≤ 26 := p .stat_s8                -- Sec. V.2, VIII: 2.6 sigma
  have hcomb : v.Combinable := p .mod_crit (by omega)     -- Sec. IV.6: below 3, combinable
  exact p .gap_bridge (p .obs_cmb) (p .mod_metric) hcomb (by omega) (p .stat_proj)  -- GAP

theorem final_nontrivial : ¬ ∀ v : Vocab, Conclusion v :=
  fun h => h ⟨False, False, 0, 0, False, False, False⟩

theorem consistent : ∃ v, Premises v :=
  ⟨⟨True, True, 18, 26, True, True, True⟩, by intro f; cases f <;> simp [prem]⟩

theorem alone_insufficient : ∀ g, ¬ ∀ v, prem g v → Conclusion v := by
  intro g h
  cases g
  case gap_bridge => exact h ⟨False, False, 99, 99, False, False, False⟩ (by simp [prem])
  all_goals exact h ⟨True, True, 18, 26, True, True, False⟩ (by simp [prem])

theorem obs_cmb_needed : ¬ ∀ v, Without .obs_cmb v → Conclusion v := fun h =>
  h ⟨False, True, 18, 26, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem mod_metric_needed : ¬ ∀ v, Without .mod_metric v → Conclusion v := fun h =>
  h ⟨True, False, 18, 26, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem stat_full_needed : ¬ ∀ v, Without .stat_full v → Conclusion v := fun h =>
  h ⟨True, True, 99, 26, False, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem stat_s8_needed : ¬ ∀ v, Without .stat_s8 v → Conclusion v := fun h =>
  h ⟨True, True, 18, 99, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem mod_crit_needed : ¬ ∀ v, Without .mod_crit v → Conclusion v := fun h =>
  h ⟨True, True, 18, 26, False, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem stat_proj_needed : ¬ ∀ v, Without .stat_proj v → Conclusion v := fun h =>
  h ⟨True, True, 18, 26, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem gap_bridge_needed : ¬ ∀ v, Without .gap_bridge v → Conclusion v := fun h =>
  h ⟨True, True, 18, 26, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

/-- What the paper writes is not enough: the step from passing the combination criterion (and a
sub-3-sigma S8 projection) to no substantial evidence for a discrepancy is not stated. -/
theorem stated_insufficient : ¬ ∀ v, Stated v → Conclusion v := fun h =>
  h ⟨True, True, 18, 26, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])

/-- Standard knowledge does not close it either: below 3 sigma is a convention for combining,
not a theorem that a discrepancy is absent. -/
theorem explicit_insufficient : ¬ ∀ v, Explicit v → Conclusion v := fun h =>
  h ⟨True, True, 18, 26, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])

end Argument
