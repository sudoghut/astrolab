/-
Argument of the paper, decomposed: DESI DR2 BAO cosmology (DESI Collaboration, Abdul-Karim et al.
2025, PRD 112, 083515, arXiv:2503.14738). The DES-Dovekie recalibration (Popovic et al. 2026,
arXiv:2511.07517) bears on the supernova combinations, which are not part of this chain (the
headline DESI + CMB result needs no supernovae); it is discussed in the wiki article.

The chain (conclusion is conditional, as in the paper: unless there is an unknown systematic error):
  w0waCDM improves the DESI + CMB fit by Delta chi2_MAP = -12.5
  LCDM is nested in w0waCDM, errors Gaussian and correctly estimated (assumed by the paper),
  asymptotic regularity (null point inside the prior box)
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
  /-- The errors are Gaussian (the working assumption of the paper for the Wilks step). -/
  Gaussian : Prop
  /-- Wilks regularity holds: large-sample limit, LCDM point inside the prior box, smooth likelihood. -/
  Regular : Prop
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
  /-- MOD [stated 2503.14738: "$\Lambda$ CDM is nested within $w_{0}w_{a}$ CDM, corresponding to $w_{0}=-1$ , $w_{a}=0$"] Sec. VII -/
  | mod_nested
  /-- MOD [stated 2503.14738: "assuming that errors are Gaussian and correctly estimated"] Sec. VII (adopted as a working assumption; the correctly-estimated half is the condition NoSys of the conclusion) -/
  | mod_gauss
  /-- MOD [implied] the regularity conditions of Wilks theorem hold for this fit: asymptotic (large-sample) limit and the LCDM point w0 = -1, wa = 0 inside the prior box w0 in [-3, 1], wa in [-3, 2], w0 + wa < 0 (Wilks 1938, Ann. Math. Statist. 9, 60, doi:10.1214/aoms/1177732360); the paper does not discuss them, and the full CMB likelihood is not Gaussian at low l -/
  | mod_regular
  /-- MOD [stated 2503.14738: "implies that $\Delta\chi^{2}_{\mathrm{MAP}}$ should follow a $\chi^{2}$ distribution with two degrees of freedom under the assumption the null hypothesis ( $\Lambda$ CDM model) holds, and assuming that errors are Gaussian and correctly estimated"] Sec. VII (Wilks theorem) -/
  | mod_wilks
  /-- MOD [stated 2503.14738: "corresponding to a 3.1 $\sigma$ preference for evolving dark energy"] Sec. VII.1 (via Eq. 22, Sec. VII) -/
  | mod_sig
  /-- MOD [stated 2503.14738: "This level of significance is not trivially dismissed, even if it does not yet rise to the $5\sigma$ threshold"] Sec. VII.3 (said of about 3 sigma to over 4 sigma) -/
  | mod_challenge
  /-- MOD [stated 2503.14738: "This tension is alleviated by dark energy with a time-evolving equation of state parametrized by $w_{0}$ and $w_{a}$ , which provides a better fit to the data"] Abstract -/
  | mod_dde
  deriving DecidableEq, Repr

def prov : Field → Prov
  | .stat_dchi2 => .stated
  | .mod_nested => .stated
  | .mod_gauss => .stated
  | .mod_regular => .implied
  | .mod_wilks => .stated
  | .mod_sig => .stated
  | .mod_challenge => .stated
  | .mod_dde => .stated

def prem : Field → Vocab → Prop
  | .stat_dchi2, v => v.dchi2 ≥ 125
  | .mod_nested, v => v.Nested
  | .mod_gauss, v => v.Gaussian
  | .mod_regular, v => v.Regular
  | .mod_wilks, v => v.Nested → v.Gaussian → v.Regular → v.NoSys → v.WilksOK
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
  have w : v.WilksOK := p .mod_wilks (p .mod_nested) (p .mod_gauss) (p .mod_regular) hns
  have d : v.dchi2 ≥ 125 := p .stat_dchi2                                -- Sec. VII.1, Table 6
  have s : v.sig ≥ 31 := p .mod_sig w d                                  -- Eq. 22
  have c : v.Challenged := p .mod_challenge (by omega)                   -- Sec. VII.3
  have e : v.DDE := p .mod_dde d                                         -- Abstract
  exact ⟨c, e⟩

theorem final_nontrivial : ¬ ∀ v : Vocab, Conclusion v :=
  fun h => (h ⟨True, False, False, False, False, 0, 0, False, False⟩ trivial).1

theorem consistent : ∃ v, Premises v :=
  ⟨⟨True, True, True, True, True, 125, 31, True, True⟩, by intro f; cases f <;> simp [prem]⟩

theorem alone_insufficient : ∀ g, ¬ ∀ v, prem g v → Conclusion v := by
  intro g h
  cases g
  case mod_wilks =>
    exact (h ⟨True, False, False, False, False, 0, 0, False, False⟩ (by simp [prem]) trivial).1
  case mod_dde =>
    exact (h ⟨True, False, False, False, False, 0, 0, False, False⟩ (by simp [prem]) trivial).1
  all_goals exact (h ⟨True, True, True, True, False, 125, 0, False, False⟩ (by simp [prem]) trivial).1

theorem stat_dchi2_needed : ¬ ∀ v, Without .stat_dchi2 v → Conclusion v := fun h =>
  (h ⟨True, True, True, True, True, 0, 0, False, False⟩
    (by intro f hf; cases f <;> simp_all [prem]) trivial).1

theorem mod_nested_needed : ¬ ∀ v, Without .mod_nested v → Conclusion v := fun h =>
  (h ⟨True, True, True, False, False, 125, 0, False, True⟩
    (by intro f hf; cases f <;> simp_all [prem]) trivial).1

theorem mod_gauss_needed : ¬ ∀ v, Without .mod_gauss v → Conclusion v := fun h =>
  (h ⟨True, False, True, True, False, 125, 0, False, True⟩
    (by intro f hf; cases f <;> simp_all [prem]) trivial).1

theorem mod_regular_needed : ¬ ∀ v, Without .mod_regular v → Conclusion v := fun h =>
  (h ⟨True, True, False, True, False, 125, 0, False, True⟩
    (by intro f hf; cases f <;> simp_all [prem]) trivial).1

theorem mod_wilks_needed : ¬ ∀ v, Without .mod_wilks v → Conclusion v := fun h =>
  (h ⟨True, True, True, True, False, 125, 0, False, True⟩
    (by intro f hf; cases f <;> simp_all [prem]) trivial).1

theorem mod_sig_needed : ¬ ∀ v, Without .mod_sig v → Conclusion v := fun h =>
  (h ⟨True, True, True, True, True, 125, 0, False, True⟩
    (by intro f hf; cases f <;> simp_all [prem]) trivial).1

theorem mod_challenge_needed : ¬ ∀ v, Without .mod_challenge v → Conclusion v := fun h =>
  (h ⟨True, True, True, True, True, 125, 31, False, True⟩
    (by intro f hf; cases f <;> simp_all [prem]) trivial).1

theorem mod_dde_needed : ¬ ∀ v, Without .mod_dde v → Conclusion v := fun h =>
  (h ⟨True, True, True, True, True, 125, 31, True, False⟩
    (by intro f hf; cases f <;> simp_all [prem]) trivial).2

/-- What the paper writes is not enough: Wilks theorem also needs its regularity conditions
(asymptotic limit, null point inside the prior box), which the paper does not discuss. -/
theorem stated_insufficient : ¬ ∀ v, Stated v → Conclusion v := fun h =>
  (h ⟨True, True, False, True, False, 125, 0, False, True⟩
    (by intro f hf; cases f <;> simp_all [prov, prem]) trivial).1

/-- With standard knowledge the chain closes: no reconstructed premise is needed. The
conclusion is conditional on the absence of unknown systematics, as the paper says. -/
theorem explicit_sufficient : ∀ v, Explicit v → Conclusion v := fun v p =>
  final v (fun f => p f (by cases f <;> decide))

end Argument
