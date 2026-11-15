/-
Argument of the paper, decomposed: Jiao, Hammer, Wang et al. 2023, "Detection of the Keplerian
decline in the Milky Way rotation curve" (A&A 678, A208; arXiv:2309.00048; "J23").

The conclusion encoded is the revised total mass (abstract): about 2 x 10^11 Msun. It rests on the
decline of the rotation curve, which is an intermediate atom of the chain:
  the rotation curve from Gaia DR3 drops by about 30 km/s between 19.5 and 26.5 kpc
  the curve is derived with the steady-state, axisymmetric Jeans equation
  a power law fitted beyond 19 kpc rejects a flat curve at 3 sigma
  [gap] steady-state axisymmetric Jeans modelling (with the estimated cross term) is accurate at
      19-26.5 kpc to better than the decline (later work, Koop et al. 2024, finds biases of 10-15%)
  [gap] with an accurate curve, a 3-sigma rejection of a flat curve detects the decline (an
      informal 3-sigma-as-evidence usage, not stated by J23)
  the dark-matter halo is a spherical Einasto profile; the baryons follow published models
  the halo is extrapolated to the virial radius (200 times the critical density)
  [gap] the Einasto shape fitted inside 26.5 kpc holds out to about 121 kpc
  [implied] the virial mass of a halo is obtained by integrating its fitted profile to the virial
      radius (standard practice)
  -> the total mass is about 2 x 10^11 Msun

Significances are encoded in tenths of a sigma (Nat), as the reported, rounded values.
Quotes follow the arXiv HTML version.

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
  /-- The curve is derived with the steady-state, axisymmetric Jeans equation. -/
  JeansUsed : Prop
  /-- Steady-state axisymmetric Jeans modelling is accurate at 19-26.5 kpc to better than the decline. -/
  JeansAccurate : Prop
  /-- Significance, in tenths of a sigma, with which a flat curve is rejected (power law beyond 19 kpc). -/
  sig_x10 : Nat
  /-- The Milky Way rotation curve declines beyond about 19 kpc (a real decline, not an artefact). -/
  Decline : Prop
  /-- The dark-matter halo is modelled as a spherical Einasto profile. -/
  Einasto : Prop
  /-- The baryonic mass distribution follows the published baryon models used. -/
  Baryons : Prop
  /-- The fitted halo is extrapolated to the virial radius. -/
  Extrapolated : Prop
  /-- The Einasto shape fitted inside 26.5 kpc holds out to the virial radius (about 121 kpc). -/
  ShapeHolds : Prop
  /-- The total (dynamical) mass of the Milky Way is about 2 x 10^11 Msun. -/
  LowMass : Prop

/-- The premises. -/
inductive Field where
  /-- OBS [stated: "the decrease in velocity between 19.5 and 26.5 kpc is approximately 30 km s-1"] Abstract (Table 3) -/
  | obs_drop
  /-- MOD [stated: "By assuming a steady state, a disc that is symmetric about its equator"] Sec. 2 (Jeans equation, Binney and Tremaine Eq. 4.222a) -/
  | mod_jeans
  /-- STAT [stated: "while a flat RC is rejected with a significance of 3σ"] Abstract (Sec. 5.3: power law beyond 19 kpc, gamma = -0.47 +- 0.15); encoded as 30 tenths -/
  | stat_flat
  /-- GAP [reconstructed] steady-state axisymmetric Jeans modelling, with J23's estimated cross term, is accurate at 19-26.5 kpc to better than the 30 km/s decline; J23 estimates the cross term (up to about 8 percent at 25.5 kpc) but does not test non-equilibrium or tracer-density truncation, which later work finds can bias the curve by 10-15 percent and fake a steep decline (Koop et al. 2024, arXiv:2405.19028) -/
  | gap_jeans
  /-- GAP [reconstructed] with the measured drop, the Jeans curve and an accurate model, a flat curve rejected at 3 sigma means the curve declines; this is the informal use of 3 sigma as evidence, which J23 does not state -/
  | gap_detect
  /-- MOD [stated: "spherical Einasto profile"] Sec. 4 (eq. 9) -/
  | mod_einasto
  /-- MOD [stated: "B2 (de Salas et al. 2019)"] Sec. 3.1 (and the E/G x CM/J/dJ models, Tables 1-2) -/
  | mod_baryons
  /-- MOD [stated: "we extrapolated the DM halo to the virial radius"] Sec. 4.3 -/
  | mod_extrap
  /-- GAP [reconstructed] the Einasto shape fitted inside 26.5 kpc holds out to about 121 kpc (a factor of 4.6 in radius); J23 does not test other halo shapes beyond the data, and stream-based masses (Koposov et al. 2023, arXiv:2211.04495; Vasiliev et al. 2021, arXiv:2009.10726) indicate more mass at 30-100 kpc -/
  | gap_shape
  /-- MOD [implied] the virial mass is the baryonic mass plus the dark mass inside the radius where the mean halo density is 200 times the critical density, obtained by integrating the fitted profile (standard halo-mass definition; e.g. Navarro, Frenk and White 1997, arXiv:astro-ph/9611107) -/
  | mod_mass
  deriving DecidableEq, Repr

def prov : Field → Prov
  | .obs_drop => .stated
  | .mod_jeans => .stated
  | .stat_flat => .stated
  | .gap_jeans => .reconstructed
  | .gap_detect => .reconstructed
  | .mod_einasto => .stated
  | .mod_baryons => .stated
  | .mod_extrap => .stated
  | .gap_shape => .reconstructed
  | .mod_mass => .implied

def prem : Field → Vocab → Prop
  | .obs_drop, v => v.Drop
  | .mod_jeans, v => v.JeansUsed
  | .stat_flat, v => v.sig_x10 = 30
  | .gap_jeans, v => v.JeansAccurate
  | .gap_detect, v => v.Drop → v.JeansUsed → v.JeansAccurate → v.sig_x10 ≥ 30 → v.Decline
  | .mod_einasto, v => v.Einasto
  | .mod_baryons, v => v.Baryons
  | .mod_extrap, v => v.Extrapolated
  | .gap_shape, v => v.ShapeHolds
  | .mod_mass, v => v.Decline → v.Einasto → v.Baryons → v.Extrapolated → v.ShapeHolds → v.LowMass

/-- [stated: "The total mass is revised downwards to 2.06"] Abstract (x 10^11 Msun, plus 0.24 minus 0.13) -/
def Conclusion (v : Vocab) : Prop := v.LowMass

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
  have hdec : v.Decline :=
    p .gap_detect (p .obs_drop) (p .mod_jeans) (p .gap_jeans) (by omega)   -- two GAPs
  exact p .mod_mass hdec (p .mod_einasto) (p .mod_baryons) (p .mod_extrap) (p .gap_shape)  -- Sec. 4.3

theorem final_nontrivial : ¬ ∀ v : Vocab, Conclusion v :=
  fun h => h ⟨False, False, False, 0, False, False, False, False, False, False⟩

theorem consistent : ∃ v, Premises v :=
  ⟨⟨True, True, True, 30, True, True, True, True, True, True⟩, by intro f; cases f <;> simp [prem]⟩

theorem alone_insufficient : ∀ g, ¬ ∀ v, prem g v → Conclusion v := by
  intro g h
  cases g
  case gap_detect => exact h ⟨False, False, False, 0, False, False, False, False, False, False⟩ (by simp [prem])
  case mod_mass => exact h ⟨False, False, False, 0, False, False, False, False, False, False⟩ (by simp [prem])
  all_goals exact h ⟨True, True, True, 30, True, True, True, True, True, False⟩ (by simp [prem])

theorem obs_drop_needed : ¬ ∀ v, Without .obs_drop v → Conclusion v := fun h =>
  h ⟨False, True, True, 30, False, True, True, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem mod_jeans_needed : ¬ ∀ v, Without .mod_jeans v → Conclusion v := fun h =>
  h ⟨True, False, True, 30, False, True, True, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem stat_flat_needed : ¬ ∀ v, Without .stat_flat v → Conclusion v := fun h =>
  h ⟨True, True, True, 0, False, True, True, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem gap_jeans_needed : ¬ ∀ v, Without .gap_jeans v → Conclusion v := fun h =>
  h ⟨True, True, False, 30, False, True, True, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem gap_detect_needed : ¬ ∀ v, Without .gap_detect v → Conclusion v := fun h =>
  h ⟨True, True, True, 30, False, True, True, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem mod_einasto_needed : ¬ ∀ v, Without .mod_einasto v → Conclusion v := fun h =>
  h ⟨True, True, True, 30, True, False, True, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem mod_baryons_needed : ¬ ∀ v, Without .mod_baryons v → Conclusion v := fun h =>
  h ⟨True, True, True, 30, True, True, False, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem mod_extrap_needed : ¬ ∀ v, Without .mod_extrap v → Conclusion v := fun h =>
  h ⟨True, True, True, 30, True, True, True, False, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem gap_shape_needed : ¬ ∀ v, Without .gap_shape v → Conclusion v := fun h =>
  h ⟨True, True, True, 30, True, True, True, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem mod_mass_needed : ¬ ∀ v, Without .mod_mass v → Conclusion v := fun h =>
  h ⟨True, True, True, 30, True, True, True, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

/-- What the paper writes is not enough: the accuracy of the Jeans curve at large radii, the step
from a 3-sigma rejection to a detected decline, the halo shape beyond the data and the standard
mass definition are not all stated. -/
theorem stated_insufficient : ¬ ∀ v, Stated v → Conclusion v := fun h =>
  h ⟨True, True, False, 30, False, True, True, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])

/-- With standard knowledge added (the mass definition), three gaps remain. -/
theorem explicit_insufficient : ¬ ∀ v, Explicit v → Conclusion v := fun h =>
  h ⟨True, True, False, 30, False, True, True, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])

end Argument
