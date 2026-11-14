/-
Argument of the paper, decomposed: DESI DR2 BAO cosmology (DESI Collaboration, Abdul-Karim et al.
2025, PRD 112, 083515, arXiv:2503.14738). The DES-Dovekie recalibration (Popovic et al. 2026,
arXiv:2511.07517) bears on the supernova combinations, which are not part of this chain (the
headline DESI + CMB result needs no supernovae); it is discussed in the wiki article.

The chain (conclusion is conditional, as in the paper: unless there is an unknown systematic error):
  w0waCDM improves the DESI + CMB fit by Delta chi2_MAP = -12.5
  LCDM is nested in w0waCDM, likelihoods Gaussian, errors correctly estimated
      -> Wilks: Delta chi2_MAP follows chi2 with 2 degrees of freedom under LCDM
  -> 3.1 sigma preference
  -> a preference of about 3 sigma or more is not trivially dismissed: LCDM is challenged
  better fit that relieves the BAO-CMB tension -> dynamical dark energy is a possible solution

Rules: AGENTS.md section 2 (paper study, Lean); specification: design/007 section 2.2.
Delta chi2 and significances are in tenths (Nat): 12.5 is 125, 3.1 sigma is 31.
Quotes follow the arXiv HTML text (v3), with math in its LaTeX source form.
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
  /-- No unknown systematic error in the DESI BAO or CMB data: errors correctly estimated. -/
  NoSys : Prop
  /-- The likelihoods are Gaussian in the data (BAO distances, compressed or full CMB). -/
  Gaussian : Prop
  /-- LCDM is the special case w0 = -1, wa = 0 of w0waCDM (nested models). -/
  Nested : Prop
  /-- Under LCDM, Delta chi2_MAP follows a chi2 distribution with two degrees of freedom. -/
  WilksOK : Prop
  /-- Minus Delta chi2_MAP (w0waCDM minus LCDM) for DESI + CMB, in tenths. -/
  dchi2 : Nat
  /-- Significance of the preference for w0waCDM over LCDM (DESI + CMB), in tenths of sigma. -/
  sig : Nat
  /-- LCDM is challenged: the preference cannot be trivially dismissed as a fluctuation. -/
  Challenged : Prop
  /-- Dynamical dark energy offers a possible solution (better fit, relieves the BAO-CMB tension). -/
  DDE : Prop

/-- The premises. -/
inductive Field where
  /-- STAT [stated 2503.14738: "when including the full CMB information the $\Delta\chi^{2}_{\mathrm{MAP}}$ decreases to $-12.5$"] Sec. VII.1, Table 6 -/
  | stat_dchi2
  /-- MOD [stated 2503.14738: "CDM is nested within $w_{0}w_{a}$ CDM"] Sec. VII -/
  | mod_nested
  /-- MOD [implied] the BAO and compressed-CMB likelihoods are Gaussian by construction (DESI DR2 BAO likelihood files, arXiv:2503.14739; Planck high-l CamSpec likelihood, Efstathiou and Gratton 2021, arXiv:1910.00483) -/
  | mod_gauss
  /-- MOD [stated 2503.14738: "implies that $\Delta\chi^{2}_{\mathrm{MAP}}$ should follow a $\chi^{2}$ distribution with two degrees of freedom under the assumption the null hypothesis"] Sec. VII (Wilks theorem; the paper adds: assuming that errors are Gaussian and correctly estimated) -/
  | mod_wilks
  /-- MOD [stated 2503.14738: "corresponding to a 3.1 $\sigma$ preference for evolving dark energy"] Sec. VII.1, Eq. 22 -/
  | mod_sig
  /-- MOD [stated 2503.14738: "This level of significance is not trivially dismissed, even if it does not yet rise to the $5\sigma$ threshold"] Sec. VII.3 (said of about 3 sigma to over 4 sigma) -/
  | mod_challenge
  /-- MOD [stated 2503.14738: "This tension is alleviated by dark energy with a time-evolving equation of state parametrized by $w_{0}$ and $w_{a}$ , which provides a better fit to the data"] Abstract -/
  | mod_dde
  deriving DecidableEq, Repr

def prov : Field → Prov
  | .stat_dchi2 => .stated
  | .mod_nested => .stated
  | .mod_gauss => .implied
  | .mod_wilks => .stated
  | .mod_sig => .stated
  | .mod_challenge => .stated
  | .mod_dde => .stated

def prem : Field → Vocab → Prop
  | .stat_dchi2, v => v.dchi2 ≥ 125
  | .mod_nested, v => v.Nested
  | .mod_gauss, v => v.Gaussian
  | .mod_wilks, v => v.Nested → v.Gaussian → v.NoSys → v.WilksOK
  | .mod_sig, v => v.WilksOK → v.dchi2 ≥ 125 → v.sig ≥ 31
  | .mod_challenge, v => v.sig ≥ 30 → v.Challenged
  | .mod_dde, v => v.dchi2 ≥ 125 → v.DDE

/-- [stated 2503.14738: "Unless there is an unknown systematic error associated with one or more datasets, it is clear that $\Lambda$ CDM is being challenged by the combination of DESI BAO with other measurements and that dynamical dark energy offers a possible solution"] Abstract -/
def Conclusion (v : Vocab) : Prop := v.NoSys → v.Challenged ∧ v.DDE

-- FIXED BLOCK B (identical in every study)
def Premises (v : Vocab) : Prop := ∀ f, prem f v
def Without (g : Field) (v : Vocab) : Prop := ∀ f, f ≠ g → prem f v
def Stated (v : Vocab) : Prop := ∀ f, prov f = .stated → prem f v
def Explicit (v : Vocab) : Prop := ∀ f, prov f ≠ .reconstructed → prem f v
-- END FIXED BLOCK B

/-- The paper's chain, step by step. -/
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p hns
  have w : v.WilksOK := p .mod_wilks (p .mod_nested) (p .mod_gauss) hns  -- Sec. VII
  have d : v.dchi2 ≥ 125 := p .stat_dchi2                                -- Sec. VII.1, Table 6
  have s : v.sig ≥ 31 := p .mod_sig w d                                  -- Eq. 22
  have c : v.Challenged := p .mod_challenge (by omega)                   -- Sec. VII.3
  have e : v.DDE := p .mod_dde d                                         -- Abstract
  exact ⟨c, e⟩

theorem final_nontrivial : ¬ ∀ v : Vocab, Conclusion v :=
  fun h => (h ⟨True, False, False, False, 0, 0, False, False⟩ trivial).1

theorem consistent : ∃ v, Premises v :=
  ⟨⟨True, True, True, True, 125, 31, True, True⟩, by intro f; cases f <;> simp [prem]⟩

theorem alone_insufficient : ∀ g, ¬ ∀ v, prem g v → Conclusion v := by
  intro g h
  cases g
  case mod_wilks =>
    exact (h ⟨True, False, False, False, 0, 0, False, False⟩ (by simp [prem]) trivial).1
  case mod_dde =>
    exact (h ⟨True, False, False, False, 0, 0, False, False⟩ (by simp [prem]) trivial).1
  all_goals exact (h ⟨True, True, True, False, 125, 0, False, False⟩ (by simp [prem]) trivial).1

theorem stat_dchi2_needed : ¬ ∀ v, Without .stat_dchi2 v → Conclusion v := fun h =>
  (h ⟨True, True, True, True, 0, 0, False, False⟩
    (by intro f hf; cases f <;> simp_all [prem]) trivial).1

theorem mod_nested_needed : ¬ ∀ v, Without .mod_nested v → Conclusion v := fun h =>
  (h ⟨True, True, False, False, 125, 0, False, True⟩
    (by intro f hf; cases f <;> simp_all [prem]) trivial).1

theorem mod_gauss_needed : ¬ ∀ v, Without .mod_gauss v → Conclusion v := fun h =>
  (h ⟨True, False, True, False, 125, 0, False, True⟩
    (by intro f hf; cases f <;> simp_all [prem]) trivial).1

theorem mod_wilks_needed : ¬ ∀ v, Without .mod_wilks v → Conclusion v := fun h =>
  (h ⟨True, True, True, False, 125, 0, False, True⟩
    (by intro f hf; cases f <;> simp_all [prem]) trivial).1

theorem mod_sig_needed : ¬ ∀ v, Without .mod_sig v → Conclusion v := fun h =>
  (h ⟨True, True, True, True, 125, 0, False, True⟩
    (by intro f hf; cases f <;> simp_all [prem]) trivial).1

theorem mod_challenge_needed : ¬ ∀ v, Without .mod_challenge v → Conclusion v := fun h =>
  (h ⟨True, True, True, True, 125, 31, False, True⟩
    (by intro f hf; cases f <;> simp_all [prem]) trivial).1

theorem mod_dde_needed : ¬ ∀ v, Without .mod_dde v → Conclusion v := fun h =>
  (h ⟨True, True, True, True, 125, 31, True, False⟩
    (by intro f hf; cases f <;> simp_all [prem]) trivial).2

/-- What the paper writes is not enough: Wilks needs Gaussian likelihoods, which the paper
assumes ("assuming that errors are Gaussian") but does not assert. -/
theorem stated_insufficient : ¬ ∀ v, Stated v → Conclusion v := fun h =>
  (h ⟨True, False, True, False, 125, 0, False, True⟩
    (by intro f hf; cases f <;> simp_all [prov, prem]) trivial).1

/-- With standard knowledge the chain closes: no reconstructed premise is needed. The
conclusion is conditional on the absence of unknown systematics, as the paper says. -/
theorem explicit_sufficient : ∀ v, Explicit v → Conclusion v := fun v p =>
  final v (fun f => p f (by cases f <;> decide))

end Argument
