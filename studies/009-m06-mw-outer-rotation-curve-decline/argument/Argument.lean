/-
Argument of the paper, decomposed: Jiao, Hammer, Wang et al. 2023, "Detection of the Keplerian
decline in the Milky Way rotation curve" (A&A 678, A208; arXiv:2309.00048; "J23").

The conclusion encoded is the title claim: a Keplerian decline of the rotation curve beyond about
19 kpc. The total mass (abstract: revised downwards to 2.06 x 10^11 Msun) is not encoded: J23 obtains
it from an Einasto-plus-baryon fit to all 18 points, which does not use the decline test; that
step and its extrapolation to the virial radius are discussed in the wiki article (section 2.3).

The chain:
  the rotation curve from Gaia DR3 drops by about 30 km/s between 19.5 and 26.5 kpc
  the curve is derived with the Jeans equation for an axisymmetric potential and a disc at
      equilibrium
  a power law fitted beyond 19 kpc rejects a flat curve at 3 sigma
  [gap] the equilibrium Jeans curve (with J23's estimated cross term) is accurate at 19-26.5 kpc
      to better than the decline; J23 argues for quasi-equilibrium but does not quantify
      departures from it (later work, Koop et al. 2024, finds biases of 10-15 percent)
  [gap] with an accurate curve, a 3-sigma rejection of a flat curve detects the decline (the
      informal use of 3 sigma as evidence, not stated by J23)
  -> a Keplerian decline beyond about 19 kpc

Significances are encoded in tenths of a sigma (Nat): sig_x10 = 30 states the reported, rounded
3 sigma, not a bound on an unrounded value. Quotes follow the arXiv HTML version.

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
  /-- The measured rotation curve drops by about 30 km/s between 19.5 and 26.5 kpc. -/
  Drop : Prop
  /-- The curve is derived with the Jeans equation for an axisymmetric potential and a disc at equilibrium. -/
  JeansUsed : Prop
  /-- The equilibrium Jeans curve is accurate at 19-26.5 kpc to better than the decline. -/
  JeansAccurate : Prop
  /-- Significance, in tenths of a sigma (reported, rounded), with which a flat curve is rejected by a power law beyond 19 kpc. -/
  sig_x10 : Nat
  /-- The Milky Way rotation curve declines in a Keplerian way beyond about 19 kpc (a real decline, not an artefact). -/
  Decline : Prop

/-- The premises. -/
inductive Field where
  /-- OBS [stated: "the decrease in velocity between 19.5 and 26.5 kpc is approximately 30 km s-1"] Abstract (Table 3) -/
  | obs_drop
  /-- MOD [stated: "Assuming an axisymmetric MW potential and a disc at equilibrium"] Sec. 2.1 (Jeans equation, Binney and Tremaine Eq. 4.222a) -/
  | mod_jeans
  /-- STAT [stated: "while a flat RC is rejected with a significance of 3σ"] Abstract (Sec. 5.3: power law beyond 19 kpc, gamma = -0.47 +- 0.15); encoded as the reported, rounded 30 tenths -/
  | stat_flat
  /-- GAP [reconstructed] the equilibrium Jeans curve, with J23's estimated cross term (up to about 8 percent at 25.5 kpc), is accurate at 19-26.5 kpc to better than the 30 km/s (15 percent) decline. J23 argues for quasi-equilibrium (Sec. 2.2: perturbations from the radial velocity component are small; Sec. 5.2: quasi-equilibrium within 30 kpc) but does not quantify departures from it; later work finds that such modelling can be biased by 10-15 percent and that a truncated tracer density can fake a steep decline (Koop et al. 2024, arXiv:2405.19028) -/
  | gap_jeans
  /-- GAP [reconstructed] with the measured drop, the Jeans curve and an accurate model, a flat curve rejected at 3 sigma means the curve declines; this is the informal use of 3 sigma as evidence, which J23 does not state -/
  | gap_detect
  deriving DecidableEq, Repr

def prov : Field → Prov
  | .obs_drop => .stated
  | .mod_jeans => .stated
  | .stat_flat => .stated
  | .gap_jeans => .reconstructed
  | .gap_detect => .reconstructed

def prem : Field → Vocab → Prop
  | .obs_drop, v => v.Drop
  | .mod_jeans, v => v.JeansUsed
  | .stat_flat, v => v.sig_x10 = 30
  | .gap_jeans, v => v.JeansAccurate
  | .gap_detect, v => v.Drop → v.JeansUsed → v.JeansAccurate → v.sig_x10 ≥ 30 → v.Decline

/-- [stated: "We identify, for the first time, a Keplerian decline of the RC"] Abstract (starting at about 19 kpc) -/
def Conclusion (v : Vocab) : Prop := v.Decline

-- FIXED BLOCK B (identical in every study)
def Premises (v : Vocab) : Prop := ∀ f, prem f v
def Without (g : Field) (v : Vocab) : Prop := ∀ f, f ≠ g → prem f v
def Stated (v : Vocab) : Prop := ∀ f, prov f = .stated → prem f v
def Explicit (v : Vocab) : Prop := ∀ f, prov f ≠ .reconstructed → prem f v
-- END FIXED BLOCK B

/-- The paper's chain, step by step. -/
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  have hsig : v.sig_x10 = 30 := p .stat_flat                     -- Abstract, Sec. 5.3
  exact p .gap_detect (p .obs_drop) (p .mod_jeans) (p .gap_jeans) (by omega)   -- two GAPs

theorem final_nontrivial : ¬ ∀ v : Vocab, Conclusion v :=
  fun h => h ⟨False, False, False, 0, False⟩

theorem consistent : ∃ v, Premises v :=
  ⟨⟨True, True, True, 30, True⟩, by intro f; cases f <;> simp [prem]⟩

theorem alone_insufficient : ∀ g, ¬ ∀ v, prem g v → Conclusion v := by
  intro g h
  cases g
  case gap_detect => exact h ⟨False, False, False, 0, False⟩ (by simp [prem])
  all_goals exact h ⟨True, True, True, 30, False⟩ (by simp [prem])

theorem obs_drop_needed : ¬ ∀ v, Without .obs_drop v → Conclusion v := fun h =>
  h ⟨False, True, True, 30, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem mod_jeans_needed : ¬ ∀ v, Without .mod_jeans v → Conclusion v := fun h =>
  h ⟨True, False, True, 30, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem stat_flat_needed : ¬ ∀ v, Without .stat_flat v → Conclusion v := fun h =>
  h ⟨True, True, True, 0, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem gap_jeans_needed : ¬ ∀ v, Without .gap_jeans v → Conclusion v := fun h =>
  h ⟨True, True, False, 30, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem gap_detect_needed : ¬ ∀ v, Without .gap_detect v → Conclusion v := fun h =>
  h ⟨True, True, True, 30, False⟩ (by intro f hf; cases f <;> simp_all [prem])

/-- What the paper writes is not enough: the accuracy of the equilibrium Jeans curve at large radii
and the step from a 3-sigma rejection to a detected decline are not stated. -/
theorem stated_insufficient : ¬ ∀ v, Stated v → Conclusion v := fun h =>
  h ⟨True, True, False, 30, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])

/-- No standard knowledge closes either step: two gaps remain. -/
theorem explicit_insufficient : ¬ ∀ v, Explicit v → Conclusion v := fun h =>
  h ⟨True, True, False, 30, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])

end Argument
