/-
Argument of the paper, decomposed: Konietzka, Goodman, Zucker, Burkert, Alves, Foley, Swiggum,
Koller, Miret-Roig 2024, "The Radcliffe Wave is oscillating" (Nature 628, 62-65;
arXiv:2402.12596; "K24").

The conclusion encoded has three parts: (1) the Radcliffe Wave oscillates through the Galactic
plane like a coherent travelling wave driven by the Galactic potential (abstract, with the
main-text p. 2 sentence on the Figure 1 fit); (2) a travelling wave is strongly preferred over a
standing wave; (3) treated as a coherent oscillator, the Wave measures the local vertical
potential (midplane density 0.085 Msun/pc3) and the Sun's vertical period (95 Myr). The radial
drift (5 km/s) and the Local Bubble link are not encoded (wiki article, section 2.6).

The chain:
  Stage A: young clusters and clouds are co-located, and the clusters were selected on the x-y
      plane only; [gap] so the clusters were born in the Wave (K24: suggesting); younger than 30 Myr, they still move with
      their clouds; the model also explains the 12CO velocities, so the cluster kinematics are the
      Wave's
  Stage B: only gravity acts; the vertical potential is an anharmonic oscillator whose parameters
      come from an existing Milky Way model (Allen and Santillan 1991, Irrgang et al. 2013), and is
      stationary; so for a travelling wave the shape fixes v_z; the travelling-wave fit to z and
      v_z is excellent, with a 90 degree offset
  Stage C: the cluster phases sweep -pi/2 to pi/2, which a standing wave forbids [gap: unless the
      spread is noise]; B = 0.84 is above 0.75 (closer to 1); [gap] both rest on a cluster v_z pattern that
      belongs to the Wave -> a travelling wave is preferred over a standing wave; B = 1 and B free
      are equivalently good -> B = 1 is adopted (the Figure 1 fit is the B = 1 realisation)
  Stage D: with B = 1 adopted (the Methods state the finding categorically), the excellent fit, [gap] the robust v_z pattern and [gap] one
      coherent wave despite Galactic shear (Li, Zhou and Chen 2024)
      -> the Wave oscillates like a travelling wave
  Stage E: with the potential freed the fit gives omega0 = 68 km/s/kpc; the isothermal sheet turns
      it into a density; [gap] the omega0 posterior is set by the Wave's data, not by priors based
      on initial fits -> the Wave measures the local potential and the Sun's period

B is encoded in hundredths (Nat): b_x100 = 84 is the reported best fit, not a bound. Quotes were
checked against the arXiv v1 PDF (accepted manuscript); sub- and superscripts are flattened
(12CO, omega0 written as in print where possible). Hedged inferences (suggesting, indicates)
are not encoded as stated implications: the step becomes a GAP, or a categorical sentence of K24
is quoted instead.

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
  /-- The young clusters (under 30 Myr) and the star-forming clouds of the Wave are co-located in 3D. -/
  CoLocated : Prop
  /-- The clusters were selected on the x-y plane only (within 5 Wave radii of the dust model), with no cut in height. -/
  NoHeightCut : Prop
  /-- The clusters' stars were born in the molecular clouds along the Wave. -/
  BornInWave : Prop
  /-- The clusters still move with the clouds they were born in, so their motions trace the Wave's kinematics. -/
  Tracer : Prop
  /-- The best-fit 6D model, projected on each cloud's line of sight, explains the measured 12CO velocities. -/
  COMatch : Prop
  /-- Clouds and young clusters form one kinematically coherent structure: the clusters' motions are the Wave's motions, gas included. -/
  Coherent : Prop
  /-- The vertical forces on the Wave are modelled by gravity alone. -/
  GravOnly : Prop
  /-- The adopted potential parameters (omega0 = 74 km/s/kpc, r0 = 3.7 kpc, mu0 = 1.3 per kpc) are chi-square fitted to an existing Milky Way model (Allen and Santillan 1991 with the parameters of Irrgang et al. 2013) at 7-10 kpc and up to 300 pc. -/
  PotParams : Prop
  /-- The vertical potential is the anharmonic oscillator of K24 eq. 1 with the adopted parameters. -/
  PotKnown : Prop
  /-- The Galactic potential is treated as stationary. -/
  Stationary : Prop
  /-- For a travelling wave, the spatial shape fixes the predicted vertical velocities (amplitude zeta times omega(s), 90 degrees out of phase with z): no free velocity amplitude. -/
  VzFixed : Prop
  /-- The travelling-wave (B = 1) model fits the clusters' z and v_z well, with a 90 degree phase offset between them (the Figure 1 fit). -/
  TWFit : Prop
  /-- The observed cluster phases phi_k = arctan(z_k omega_k / v_z,k) change over the whole range -pi/2 to pi/2 along the Wave. -/
  PhaseSpread : Prop
  /-- The observed phase spread exceeds what measurement errors and the 47 pc scatter would give for a B = 0.5 wave (near its nodes z and v_z tend to zero). -/
  PhaseNotNoise : Prop
  /-- The Wave is a standing wave (B = 0.5). -/
  Standing : Prop
  /-- Best-fit mixing parameter B of the travelling/standing mixture model, in hundredths (reported value). -/
  b_x100 : Nat
  /-- The cluster z-v_z pattern (and so the phases and the B posterior) is a property of the Wave, not of the cluster sample, its radial-velocity coverage, the solar-motion zero point or the outlier and weighting choices. -/
  VzRobust : Prop
  /-- A travelling wave is (strongly) preferred over a standing wave. -/
  PreferTW : Prop
  /-- The fits with B fixed to 1 and with B free are an equivalently good fit (Delta ln Z of about 1). -/
  BEquiv : Prop
  /-- Setting B = 1 (a pure travelling wave) in all further fits is justified. -/
  B1OK : Prop
  /-- One coherent travelling wave (one phase law Lambda(s), one solid-body drift) adequately describes the Wave over the time its tracers span, despite shear and phase mixing. -/
  SolidOK : Prop
  /-- The Radcliffe Wave oscillates through the Galactic plane like a coherent travelling wave driven by the Galactic potential. -/
  Oscillating : Prop
  /-- With omega0, mu0 and r0 free (B = 1), the fit gives omega0 = 68 +8 -7 km/s/kpc, mu0 = 1.4, r0 = 3.6 kpc. -/
  OmegaFit : Prop
  /-- The midplane density follows from omega0 by the isothermal-sheet relation rho0 = omega0 squared over 4 pi G. -/
  Sheet : Prop
  /-- The omega0 posterior (and so rho0 and the Sun's period, with their central values and errors) is set by the Wave's data, not by priors based on initial fits. -/
  DataDriven : Prop
  /-- Treated as a coherent oscillator, the Wave directly measures the local vertical potential (midplane density) and the Sun's vertical oscillation period. -/
  Weighs : Prop

/-- The premises. -/
inductive Field where
  /-- OBS [stated: "As expected, the young clusters and star-forming molecular clouds are co-located in three dimensions."] main text p. 1, Fig. 1a -/
  | obs_coloc
  /-- MOD [stated: "We make a conservative selection on the x-y plane by enclosing all stellar clusters within ±5 times the radius of the Wave (47 pc) from the best fit of the dust component"] Methods, Stellar Cluster Catalog (main text p. 1: without an a priori selection criterion for height) -/
  | mod_xy
  /-- GAP [reconstructed] co-located young clusters selected with no height cut were born in the Wave's molecular clouds. K24 only suggests this (main text p. 1: selected without an a priori selection criterion for height, suggesting that the clusters' stars were born in the molecular clouds along the Radcliffe Wave); the step from co-location to common origin is not demonstrated (no age-position or chemistry test; chance alignment of unrelated young groups not quantified) -/
  | gap_born
  /-- MOD [stated: "We restrict our analysis to only the youngest clusters (ages smaller than 30 Myr), guaranteeing that these associations are still tracing the velocities of the molecular clouds that served as their birthplaces."] Methods, Stellar Cluster Catalog -/
  | mod_age
  /-- STAT [stated: "We show in Extended Data Figure 3a that our model explains the 12CO observations"] Methods, Line-of-sight Gas Velocities (model-data agreement shown graphically; no goodness-of-fit number) -/
  | stat_co
  /-- MOD [stated: "As a consequence, we can transfer our results from the full phase-space study of the stars to all components of the Radcliffe Wave, including the gas"] Methods, Line-of-sight Gas Velocities; encoded with the extra antecedent Tracer (weaker than the quote) -/
  | mod_transfer
  /-- MOD [stated: "We therefore model the forces acting on the Wave solely by gravity."] Methods, Full Spatial and Kinematic Model (density ratio of 10^4 to the surrounding medium) -/
  | mod_grav
  /-- LIT [stated: "These parameters are adopted by comparing equation (1) with an existing model of the Galactic potential including its updated parameters"] Methods; the model is Allen and Santillan 1991 (Rev. Mex. Astron. Astrofis. 22, 255) with the updated parameters of Irrgang et al. 2013 (arXiv:1211.4353, A and A 549, A137); chi-square fit over 7-10 kpc and 0-300 pc -/
  | lit_pot
  /-- MOD [stated: "Since the Radcliffe Wave's amplitude is on the order of the Galaxy's vertical scale height, the vertical gravitational potential Φ resulting in this acceleration can be represented by an anharmonic oscillator."] Methods, eq. 1; encoded with the parameter source as antecedent -/
  | mod_pot
  /-- MOD [stated: "Note that, consistent with the literature, we treat the underlying Gravitational potential as stationary."] Methods, after eq. 3 -/
  | mod_stationary
  /-- MOD [stated: "For a traveling wave, the wave's spatial shape fully determines vertical velocities, assuming a gravitational potential"] main text p. 2 (eqs. 4-5 of Methods); encoded with the potential's assumptions as antecedents -/
  | mod_shape
  /-- STAT [stated: "While a traveling wave provides an excellent fit to the observations, with a 90° phase offset between position (z) and velocity (vz), as evident in Figure 1"] main text p. 2; the Figure 1 fit is the B = 1 realisation (Extended Data Table 2 column (6), clouds and clusters) -/
  | stat_twfit
  /-- STAT [stated: "In contrast, we find that the phases φk change over the whole range of -π/2 to π/2, such that B = 0.5 is inconsistent with the data."] Methods (wave model; no statistic is given for the spread) -/
  | stat_phase
  /-- MOD [stated: "From equations (4) and (5) we conclude that the phases φk should be roughly constant"] Methods (the preceding sentence assumes B = 0.5, a standing wave; model phases vary at most by about 0.03 pi); encoded for observed phases, with PhaseNotNoise as antecedent: the quote concerns the noiseless model, and the body applies it to observed phases, which is why PhaseNotNoise is needed -/
  | mod_standing
  /-- GAP [reconstructed] the observed phase spread exceeds what measurement errors and the Wave's 47 pc scatter would give for a B = 0.5 wave: near a standing wave's nodes both z and v_z tend to zero, so the phases there are set by noise; K24 states the noiseless model expectation and gives no statistic for the observed spread -/
  | gap_phase_noise
  /-- STAT [stated: "We find a best fit value for B = 0.84."] Methods; Extended Data Table 2 column (5), clusters with B free: 0.84 +0.07 -0.06, uniform prior on 0 to 1; encoded as the reported value 84 hundredths -/
  | stat_b
  /-- GAP [reconstructed] the clusters' mean vertical velocities (Gaia DR3 proper motions, Gaia and APOGEE radial velocities, the 50 km/s cut, the solar motion w = 7.8 km/s of Schoenrich et al. 2010 that sets every v_z zero point, the tanh outlier model that drops all Perseus and Taurus clusters, and the kernel weights) give the Wave's true z-v_z pattern, on which the phases, the B posterior and the Figure 1 fit all rest. K24 checks the Sun's height, a plane tilt, three potentials and a second cluster catalogue, but not alternative v_z derivations nor the outlier and weighting choices; Zhu et al. 2024 (arXiv:2402.15346), with APOGEE-2 stars and with cloud radial velocities plus YSO proper motions, find vertical-velocity oscillations not synchronous with the vertical coordinate (a dipole-like gradient); Bobylev, Ikhsanov and Bajkova 2025 (arXiv:2503.21019) find different wavelengths in z and v_z -/
  | gap_vz
  /-- MOD [stated: "When fitting a mixture model that allows for superpositions of a traveling and a standing wave, we find that a traveling wave is strongly preferred over a standing wave (see Methods)."] main text p. 2; encoded with B above 0.75 (our reading of closer to 1, Methods), the excluded standing wave and VzRobust as antecedents (weaker than the quote) -/
  | mod_prefer
  /-- STAT [stated: "Thus, both models are an equivalently good fit to the data, while the realization with fixed B = 1 is slightly preferred."] Methods (Delta ln Z = ln Z2 - ln Z1 of about 1, Z1 for B = 1, Z2 for B free; the printed sign and the stated preference disagree) -/
  | stat_bequiv
  /-- MOD [stated: "We therefore conclude that the Wave's motion is of first order consistent with a traveling wave, implying that we can set B = 1 in all further performed calculations"] Methods (the B = 1 fit also fixes omega0 t = 0); encoded with PreferTW as antecedent -/
  | mod_b1
  /-- GAP [reconstructed] one coherent travelling wave, with one phase law Lambda(s) and one solid-body in-plane drift, is an adequate description of the Wave over the time its tracers (up to 30 Myr old) span. K24 notes that on several tens of Myr the Wave is likely affected by cloud destruction and phase mixing (Fig. 1 caption) and that its time-independent approximation reaches the noise after about 40 Myr, but treats the Wave as a single coherent structure; Li, Zhou and Chen 2024 (arXiv:2410.14603) find that shear stretches the Wave to almost twice its length in about 45 Myr, within which only half an oscillation cycle occurs, and call the solid-body treatment an oversimplification -/
  | gap_shear
  /-- MOD [stated: "In the case of the z-component, we find that the Radcliffe Wave oscillates like a traveling wave driven by the Milky Way's gravitational acceleration."] Methods, Full Spatial and Kinematic Model (categorical; the main text p. 2 says the Figure 1 fit indicates this); the Figure 1 fit is the B = 1 realisation, so B1OK is an antecedent; encoded with the earlier steps and the two gaps as antecedents (weaker than the quote) -/
  | mod_osc
  /-- STAT [stated: "We find a median value and 1σ errors (computed using the 16th, 50th and 84th percentiles of the samples) of ω0 = 68 +8 -7 km s-1 kpc-1"] Methods, Sun's Vertical Oscillation Period (superscripts flattened; mu0 = 1.4, r0 = 3.6 kpc in the same sentence; Extended Data Table 2 column (7)) -/
  | stat_omega
  /-- MOD [stated: "Following the vertical density model of an isothermal sheet based on a Maxwellian vertical velocity distribution, we calculate the parameters defining the Galactic mass distribution"] Methods (rho0 = omega0 squared over 4 pi G, z0 = 1 over root 6 mu0) -/
  | mod_sheet
  /-- GAP [reconstructed] the omega0 posterior, and with it rho0 = 0.085 +0.021 -0.017 Msun/pc3, the dark-matter density and the Sun's 95 +12 -10 Myr period, is set by the Wave's data. K24 says it uses the pattern without prior knowledge about the vertical potential, but the priors are based on initial fits (presumably to the same data); the omega0 prior (log-normal, centred near 91 km/s/kpc, about 17 percent wide) is not much wider than the posterior (about 11 percent), which sits about 1.7 sigma (in ln) below the prior centre, and fixed (74) and free (68) potentials are an equivalently good fit (Delta ln Z of about 1) -/
  | gap_prior
  /-- MOD [stated: "By treating the Radcliffe Wave as a coherently oscillating structure, we can derive its motion independently of the local Galactic mass distribution, and directly measure local properties of the Galactic potential as well as the Sun's vertical oscillation period."] Abstract; encoded with the earlier steps and the gap as antecedents (weaker than the quote) -/
  | mod_weigh
  deriving DecidableEq, Repr

def prov : Field → Prov
  | .obs_coloc => .stated
  | .mod_xy => .stated
  | .gap_born => .reconstructed
  | .mod_age => .stated
  | .stat_co => .stated
  | .mod_transfer => .stated
  | .mod_grav => .stated
  | .lit_pot => .stated
  | .mod_pot => .stated
  | .mod_stationary => .stated
  | .mod_shape => .stated
  | .stat_twfit => .stated
  | .stat_phase => .stated
  | .mod_standing => .stated
  | .gap_phase_noise => .reconstructed
  | .stat_b => .stated
  | .gap_vz => .reconstructed
  | .mod_prefer => .stated
  | .stat_bequiv => .stated
  | .mod_b1 => .stated
  | .gap_shear => .reconstructed
  | .mod_osc => .stated
  | .stat_omega => .stated
  | .mod_sheet => .stated
  | .gap_prior => .reconstructed
  | .mod_weigh => .stated

def prem : Field → Vocab → Prop
  | .obs_coloc, v => v.CoLocated
  | .mod_xy, v => v.NoHeightCut
  | .gap_born, v => v.CoLocated → v.NoHeightCut → v.BornInWave
  | .mod_age, v => v.BornInWave → v.Tracer
  | .stat_co, v => v.COMatch
  | .mod_transfer, v => v.Tracer → v.COMatch → v.Coherent
  | .mod_grav, v => v.GravOnly
  | .lit_pot, v => v.PotParams
  | .mod_pot, v => v.PotParams → v.PotKnown
  | .mod_stationary, v => v.Stationary
  | .mod_shape, v => v.GravOnly → v.PotKnown → v.Stationary → v.VzFixed
  | .stat_twfit, v => v.TWFit
  | .stat_phase, v => v.PhaseSpread
  | .mod_standing, v => v.Standing → v.PhaseNotNoise → ¬ v.PhaseSpread
  | .gap_phase_noise, v => v.PhaseNotNoise
  | .stat_b, v => v.b_x100 = 84
  | .gap_vz, v => v.VzRobust
  | .mod_prefer, v => v.b_x100 > 75 → ¬ v.Standing → v.VzRobust → v.PreferTW
  | .stat_bequiv, v => v.BEquiv
  | .mod_b1, v => v.PreferTW → v.BEquiv → v.B1OK
  | .gap_shear, v => v.SolidOK
  | .mod_osc, v => v.Coherent → v.VzFixed → v.TWFit → v.B1OK → v.VzRobust → v.SolidOK → v.Oscillating
  | .stat_omega, v => v.OmegaFit
  | .mod_sheet, v => v.Sheet
  | .gap_prior, v => v.DataDriven
  | .mod_weigh, v => v.Oscillating → v.OmegaFit → v.Sheet → v.DataDriven → v.Weighs

/-- [stated: "Here we present evidence that the Radcliffe Wave is oscillating through the Galactic plane while also drifting radially away from the Galactic Center."] Abstract; part 1 also rests on main text p. 2 (the Figure 1 fit indicates that the Wave oscillates like a traveling wave), part 2 on main text p. 2 (strongly preferred), part 3 on the abstract (directly measure local properties of the Galactic potential as well as the Sun's vertical oscillation period); the drift is not encoded -/
def Conclusion (v : Vocab) : Prop := v.Oscillating ∧ v.PreferTW ∧ v.Weighs

-- FIXED BLOCK B (identical in every study)
def Premises (v : Vocab) : Prop := ∀ f, prem f v
def Without (g : Field) (v : Vocab) : Prop := ∀ f, f ≠ g → prem f v
def Stated (v : Vocab) : Prop := ∀ f, prov f = .stated → prem f v
def Explicit (v : Vocab) : Prop := ∀ f, prov f ≠ .reconstructed → prem f v
-- END FIXED BLOCK B

/-- A model in which every premise and the conclusion hold; countermodels change a few fields. -/
def full : Vocab :=
  { CoLocated := True, NoHeightCut := True, BornInWave := True, Tracer := True, COMatch := True,
    Coherent := True, GravOnly := True, PotParams := True, PotKnown := True, Stationary := True,
    VzFixed := True, TWFit := True, PhaseSpread := True, PhaseNotNoise := True, Standing := False,
    b_x100 := 84, VzRobust := True, PreferTW := True, BEquiv := True,
    B1OK := True, SolidOK := True, Oscillating := True, OmegaFit := True, Sheet := True,
    DataDriven := True, Weighs := True }

/-- The paper's chain, step by step. -/
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  -- Stage A: the clusters trace the Wave (main text p. 1; Methods)
  have c : v.Coherent :=
    p .mod_transfer (p .mod_age (p .gap_born (p .obs_coloc) (p .mod_xy))) (p .stat_co)
  -- Stage B: the model and the fit (main text p. 2; Methods)
  have z : v.VzFixed :=
    p .mod_shape (p .mod_grav) (p .mod_pot (p .lit_pot)) (p .mod_stationary)
  -- Stage C: travelling, not standing; B = 1 adopted (Methods)
  have hb : v.b_x100 = 84 := p .stat_b
  have ns : ¬ v.Standing := fun s => p .mod_standing s (p .gap_phase_noise) (p .stat_phase)  -- GAP
  have pt : v.PreferTW := p .mod_prefer (by omega) ns (p .gap_vz)                                     -- GAP
  have b1 : v.B1OK := p .mod_b1 pt (p .stat_bequiv)
  -- Stage D: the Wave oscillates (main text p. 2)
  have o : v.Oscillating :=
    p .mod_osc c z (p .stat_twfit) b1 (p .gap_vz) (p .gap_shear)                              -- two GAPs
  -- Stage E: weighing the disc (Methods)
  have w : v.Weighs := p .mod_weigh o (p .stat_omega) (p .mod_sheet) (p .gap_prior)         -- GAP
  exact ⟨o, pt, w⟩

theorem final_nontrivial : ¬ ∀ v : Vocab, Conclusion v :=
  fun h => (h { full with Oscillating := False }).1

theorem consistent : ∃ v, Premises v :=
  ⟨full, by intro f; cases f <;> simp [prem, full]⟩

theorem alone_insufficient : ∀ g, ¬ ∀ v, prem g v → Conclusion v := by
  intro g h
  cases g
  case mod_osc => exact (h { full with Weighs := False } (by simp [prem, full])).2.2
  all_goals exact (h { full with Oscillating := False } (by simp [prem, full])).1

-- Stage A
theorem obs_coloc_needed : ¬ ∀ v, Without .obs_coloc v → Conclusion v := fun h =>
  (h { full with CoLocated := False, BornInWave := False, Tracer := False, Coherent := False, Oscillating := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

theorem mod_xy_needed : ¬ ∀ v, Without .mod_xy v → Conclusion v := fun h =>
  (h { full with NoHeightCut := False, BornInWave := False, Tracer := False, Coherent := False, Oscillating := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

theorem gap_born_needed : ¬ ∀ v, Without .gap_born v → Conclusion v := fun h =>
  (h { full with BornInWave := False, Tracer := False, Coherent := False, Oscillating := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

theorem mod_age_needed : ¬ ∀ v, Without .mod_age v → Conclusion v := fun h =>
  (h { full with Tracer := False, Coherent := False, Oscillating := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

theorem stat_co_needed : ¬ ∀ v, Without .stat_co v → Conclusion v := fun h =>
  (h { full with COMatch := False, Coherent := False, Oscillating := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

theorem mod_transfer_needed : ¬ ∀ v, Without .mod_transfer v → Conclusion v := fun h =>
  (h { full with Coherent := False, Oscillating := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

-- Stage B
theorem mod_grav_needed : ¬ ∀ v, Without .mod_grav v → Conclusion v := fun h =>
  (h { full with GravOnly := False, VzFixed := False, Oscillating := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

theorem lit_pot_needed : ¬ ∀ v, Without .lit_pot v → Conclusion v := fun h =>
  (h { full with PotParams := False, PotKnown := False, VzFixed := False, Oscillating := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

theorem mod_pot_needed : ¬ ∀ v, Without .mod_pot v → Conclusion v := fun h =>
  (h { full with PotKnown := False, VzFixed := False, Oscillating := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

theorem mod_stationary_needed : ¬ ∀ v, Without .mod_stationary v → Conclusion v := fun h =>
  (h { full with Stationary := False, VzFixed := False, Oscillating := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

theorem mod_shape_needed : ¬ ∀ v, Without .mod_shape v → Conclusion v := fun h =>
  (h { full with VzFixed := False, Oscillating := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

theorem stat_twfit_needed : ¬ ∀ v, Without .stat_twfit v → Conclusion v := fun h =>
  (h { full with TWFit := False, Oscillating := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

-- Stage C
theorem stat_phase_needed : ¬ ∀ v, Without .stat_phase v → Conclusion v := fun h =>
  (h { full with PhaseSpread := False, Standing := True, PreferTW := False, B1OK := False, Oscillating := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.1

theorem mod_standing_needed : ¬ ∀ v, Without .mod_standing v → Conclusion v := fun h =>
  (h { full with Standing := True, PreferTW := False, B1OK := False, Oscillating := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.1

theorem gap_phase_noise_needed : ¬ ∀ v, Without .gap_phase_noise v → Conclusion v := fun h =>
  (h { full with PhaseNotNoise := False, Standing := True, PreferTW := False, B1OK := False, Oscillating := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.1

theorem stat_b_needed : ¬ ∀ v, Without .stat_b v → Conclusion v := fun h =>
  (h { full with b_x100 := 0, PreferTW := False, B1OK := False, Oscillating := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.1

theorem gap_vz_needed : ¬ ∀ v, Without .gap_vz v → Conclusion v := fun h =>
  (h { full with VzRobust := False, PreferTW := False, B1OK := False, Oscillating := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.1

theorem mod_prefer_needed : ¬ ∀ v, Without .mod_prefer v → Conclusion v := fun h =>
  (h { full with PreferTW := False, B1OK := False, Oscillating := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.1

theorem stat_bequiv_needed : ¬ ∀ v, Without .stat_bequiv v → Conclusion v := fun h =>
  (h { full with BEquiv := False, B1OK := False, Oscillating := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

theorem mod_b1_needed : ¬ ∀ v, Without .mod_b1 v → Conclusion v := fun h =>
  (h { full with B1OK := False, Oscillating := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

-- Stage D
theorem gap_shear_needed : ¬ ∀ v, Without .gap_shear v → Conclusion v := fun h =>
  (h { full with SolidOK := False, Oscillating := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

theorem mod_osc_needed : ¬ ∀ v, Without .mod_osc v → Conclusion v := fun h =>
  (h { full with Oscillating := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

-- Stage E
theorem stat_omega_needed : ¬ ∀ v, Without .stat_omega v → Conclusion v := fun h =>
  (h { full with OmegaFit := False, Weighs := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2

theorem mod_sheet_needed : ¬ ∀ v, Without .mod_sheet v → Conclusion v := fun h =>
  (h { full with Sheet := False, Weighs := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2

theorem gap_prior_needed : ¬ ∀ v, Without .gap_prior v → Conclusion v := fun h =>
  (h { full with DataDriven := False, Weighs := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2

theorem mod_weigh_needed : ¬ ∀ v, Without .mod_weigh v → Conclusion v := fun h =>
  (h { full with Weighs := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2

/-- What the paper writes is not enough: the common origin of clusters and clouds, the robustness of the v_z pattern (on which all three
parts rest), the phase spread beyond noise, the coherent-wave description and the data-driven
omega0 are not stated. -/
theorem stated_insufficient : ¬ ∀ v, Stated v → Conclusion v := fun h =>
  (h { full with VzRobust := False, PreferTW := False, B1OK := False, Oscillating := False }
    (by intro f hf; cases f <;> simp_all [prov, prem, full])).1

/-- No standard knowledge closes them (there is no implied premise): five gaps remain. -/
theorem explicit_insufficient : ¬ ∀ v, Explicit v → Conclusion v := fun h =>
  (h { full with VzRobust := False, PreferTW := False, B1OK := False, Oscillating := False }
    (by intro f hf; cases f <;> simp_all [prov, prem, full])).1

end Argument
