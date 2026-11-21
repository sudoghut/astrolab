/-
Argument of the paper, decomposed: Rix, Chandra, Andrae, Price-Whelan, Weinberg, Conroy,
Fouesneau, Hogg, De Angeli, Naidu, Xiang, Ruz-Mieres 2022, "The Poor Old Heart of the Milky Way"
(ApJ 941, 45; arXiv:2209.02722; "R22").

The conclusion encoded has four parts: (1) the metal-poor stars (XP [M/H] below -1.5) in the inner
Galaxy amount to at least about 5e7 solar masses; (2) they are centrally concentrated, most within
5 kpc of the Galactic Centre; (3) they formed before the oldest disc, at least 12.5 Gyr ago
(z of about 5 or more); (4) they are the most ancient proto-Galactic (in-situ) component of the
Milky Way. The abstract and the summary (Section IV) state all four; the abstract hedges (3)
("most likely predate") and Section IV hedges (4) ("fits a picture in which").

The chain:
  Stage A: the XP metallicities are precise to about 0.1 dex; [gap] the metal-poor tail is not
      dominated by metal-richer stars with underestimated [M/H] (R22 asks how pure it is); a
      precise and pure selection is genuine (standard) -> the counted metal-poor stars are real
  Stage B: about 18,000 such stars; M4 gives one giant per 800 Msun; [gap] that conversion applies
      to this sample -> about 2e7 Msun at face value; crowding and dust make the sample incomplete,
      a conservative factor 2.5 -> at least about 5e7 Msun
  Stage C: a spherical Gaussian fitted to the parallaxes gives sigma of about 2.7 kpc; [gap] the
      fit is not distorted by the unmodelled selection (dust, crowding, field edge, magnitude cut)
      -> most stars within 5 kpc of the Centre
  Stage D: no net rotation below -2, rotation dominated near -1; most apocentres below 5 kpc;
      the vast majority alpha-enhanced (data feeding stage F)
  Stage E: the old disc's metallicity distribution drops sharply below -1; [gap] the metal-poor
      stars and the old disc belong to one chemically connected system; within one such system
      metallicity rises with time (standard) -> the metal-poor stars predate the oldest disc;
      the oldest disc stars are about 12.5 Gyr old -> formed at least 12.5 Gyr ago, z of about 5
      or more
  Stage F: confinement argues against a once-distant satellite; alpha-enhancement argues
      for rapid enrichment in a deep potential well; [gap] together with mass, age and kinematics
      this makes the population the proto-Galaxy's in-situ core

Hedged sentences are not encoded as stated implications: "most likely predate" becomes the gap
gap_onezone plus the standard rule mod_amr; "most likely ... not at a low-mass satellite" and
"fits a picture" become the gap gap_proto. The paper's "arguing against" and "arguing for" are
encoded with atoms that themselves say disfavoured / favoured. Quotes are from the arXiv HTML v1;
quotes cannot contain square brackets, so phrases with [M/H] are cut before or after the bracket,
and LaTeX subscripts are flattened.

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
  /-- The XGBoost XP metallicities agree with APOGEE (and with LAMOST, GALAH, GSP-Spec) to about 0.1 dex. -/
  Precise : Prop
  /-- The XP-selected metal-poor tail ([M/H] below -1.5) is not dominated by metal-richer stars whose XP [M/H] is underestimated (by dust, crowding, the training range or the regression's behaviour at the edge of its labels). -/
  Pure : Prop
  /-- The stars with XP [M/H] below -1.5 are genuinely metal-poor, so counts and maps of them describe a real metal-poor population. -/
  TailReal : Prop
  /-- The sample contains about 18,000 stars with XP [M/H] below -1.5 (abstract; about 20,000 in Fig. 4 and Section IV). -/
  CountMP : Prop
  /-- In the template globular cluster M4 there is one giant with M_G below 0.5 per 800 Msun of total stellar mass. -/
  M4Ratio : Prop
  /-- The M4 giant-to-mass conversion applies to the counted sample (same luminosity range as the sample cut, representative age and mass function, and the 800 Msun follows from the M4 numbers used). -/
  TemplateOK : Prop
  /-- At face value the stars with [M/H] below -1.5 represent about 2e7 Msun. -/
  FaceMass : Prop
  /-- The sample is incomplete: XP spectra are missing in very crowded fields and dust extinction hides stars. -/
  Incomplete : Prop
  /-- The stellar mass of the metal-poor ([M/H] below -1.5) population in the inner Galaxy is at least about 5e7 Msun. -/
  Massive : Prop
  /-- The 3D distribution of the metal-poor stars is modelled as a spherical Gaussian in Galactocentric radius. -/
  SphGauss : Prop
  /-- The maximum-likelihood fit of that model to the observed parallaxes (with errors) gives sigma_RGC of about 2.7 kpc. -/
  SigmaFit : Prop
  /-- The fitted extent is not distorted by the selection the model leaves out (dust gap at small heights, crowding, the 60 by 60 degree field, the BP and luminosity cuts). -/
  SelOK : Prop
  /-- The metal-poor population is centrally concentrated: most of its stars are within 5 kpc of the Galactic Centre. -/
  Central : Prop
  /-- Stars with [M/H] below -2 show no net rotation. -/
  NoRotVMP : Prop
  /-- Stars with [M/H] near -1 are rotation dominated. -/
  RotRich : Prop
  /-- Most of the metal-poor stars have orbital apocentres below 5 kpc. -/
  ApoSmall : Prop
  /-- The vast majority of stars with [M/H] below -1.5 (APOGEE subset) are distinctly alpha-enhanced. -/
  AlphaEnh : Prop
  /-- The metallicity distribution of the old alpha-enhanced disc is truncated, or drops sharply, below [M/H] = -1. -/
  DiscFloor : Prop
  /-- The inner-Galaxy metal-poor stars and the old disc formed in one chemically connected system with a single, monotonic enrichment history (no fragment that enriched more slowly and formed its metal-poor stars later). -/
  OneSystem : Prop
  /-- The metal-poor stars formed before the oldest part of the disc. -/
  Predates : Prop
  /-- The oldest alpha-enhanced disc stars (near [M/H] = -1) are about 12.5 Gyr old. -/
  DiscAge : Prop
  /-- The metal-poor population formed at least 12.5 Gyr ago, at z of about 5 or more. -/
  Ancient : Prop
  /-- An origin by accretion from a once-distant satellite is disfavoured. -/
  NotDistant : Prop
  /-- Rapid enrichment in a deep potential well is favoured. -/
  DeepWell : Prop
  /-- The metal-poor heart is the most ancient proto-Galactic (in-situ) component of the Milky Way. -/
  ProtoGal : Prop

/-- The premises. -/
inductive Field where
  /-- STAT [stated: "a remarkably precise (≲0.1 in the median)"] Section II.3 (against about 17,000 APOGEE stars that were in the training set; Appendix A.2: about 0.1 dex against LAMOST, GALAH, GSP-Spec, with a slight increase in scatter towards low [M/H]) -/
  | stat_prec
  /-- GAP [reconstructed] the XP-selected tail below [M/H] = -1.5 is pure enough: R22 asks how pure the XP selected samples in this regime are (Section IV) and gives no contamination estimate; the sample has about 100 stars above -1.5 for each one below, the APOGEE training set only extended to -2.5, and Chen et al. 2025 (arXiv:2511.18901) find that ten Gaia XP metallicity catalogues give metal-poor tails with slopes from about 0.6 to 2.0 -/
  | gap_pure
  /-- MOD [implied] standard selection logic: stars selected by an estimated quantity below a cut are genuine members when the estimator is precise and the contamination is small (Ivezic, Connolly, VanderPlas and Gray 2014, Statistics, Data Mining, and Machine Learning in Astronomy, Princeton University Press) -/
  | mod_tail
  /-- OBS [stated: "that includes ∼18,000 stars"] Abstract (with -2.7 to -1.5 in [M/H]; Section III.2 also about 18,000, Fig. 4 and Section IV about 20,000) -/
  | obs_count
  /-- MOD [stated: "per 800 M⊙ of total stellar population mass"] Section III.2 (about 35 giants with M_G below 0.5 beyond M4 half-mass radius, M4 total mass 7e4 Msun) -/
  | mod_m4
  /-- GAP [reconstructed] the M4 conversion applies to the sample: the sample cut keeps stars to a colour-corrected M_G of about 0.9, not 0.5; M4 age and mass function stand for the whole population; and the 800 Msun per giant does not follow from the quoted M4 numbers by our arithmetic (35 giants beyond the half-mass radius and half of 7e4 Msun give about 1,000) -/
  | gap_template
  /-- MOD [stated: "At face value, this implies"] Section III.2 (continues: about 2e7 Msun for [M/H] below -1.5); encoded with the genuine tail and the template as extra antecedents (weaker than the quote) -/
  | mod_face
  /-- OBS [stated: "But this does not account for the incompleteness of XP spectra in very crowded fields"] Section III.2 (the sentence continues: nor for the far-reaching effects of dust extinction) -/
  | obs_incomplete
  /-- MOD [stated: "A conservative estimate of these effects is a factor of 2.5, leading us to a lower limit on the mass of"] Section III.2 (continues: about 5e7 Msun for [M/H] below -1.5; the summary, Section IV, suggests 1e8 Msun or more) -/
  | mod_corr
  /-- MOD [stated: "We assume that the 3D distribution is a spherical Gaussian as a function of Galactocentric radius"] Section III.1, eq. 1 -/
  | mod_sph
  /-- STAT [stated: "We find that the maximum likelihood of the observed parallaxes (and their uncertainties) for the"] Section III.1 (continues: [M/H] below -1.5 stars implies an extent of sigma_RGC of about 2.7 kpc; no uncertainty quoted; parallax zero point 0.02 mas) -/
  | stat_sigma
  /-- GAP [reconstructed] the fitted extent is not distorted by the selection the model omits: R22 says the distribution deserves to be modeled quantitatively including dust extinction, crowding and parallax uncertainties (Section IV), and dust removes most stars at heights below 700 pc (Section III.2); Kurbatov et al. 2024 (arXiv:2410.22250), modelling Gaia XP giants with [M/H] below -1.3 with the Gaia selection function, find a flattened (about 0.5) cored power law, with an Aurora component of slope -4.5 dominating the inner halo -/
  | gap_sel
  /-- MOD [stated: "the parallax distribution implies that most stars are within 5 kpc of the Galactic center"] Section IV (Figure 3); encoded with the genuine tail, the model, the fit and the selection as antecedents (weaker than the quote) -/
  | mod_central
  /-- STAT [stated: "show no net rotation, whereas those with"] Abstract (the subject is stars with [M/H] below -2; Section III.3 says instead that some, albeit small, net rotation starts already below -2; Ardern-Arentsen et al. 2024, arXiv:2312.03847, find about 40 km/s for very metal-poor inner stars) -/
  | stat_norot
  /-- STAT [stated: "are rotation dominated"] Abstract (the subject is stars with [M/H] near -1; J_phi/J_tot about 0.3 at -1.3 in Section III.3, 0.25 at -1.5 and about 0.9 at -0.8 in Section IV) -/
  | stat_spin
  /-- STAT [stated: "most stars have apocenters of less than 5 kpc"] Section IV (mean apocentre about 4 kpc, Section III.3; orbits for the RVS subsample) -/
  | stat_apo
  /-- STAT [stated: "are distinctly α-enhanced, arguing for rapid enrichment in a deep potential well"] Section IV (subject: the vast majority of stars with [M/H] below -1.5, APOGEE DR17 subset); the body encodes only the observation, the inference is mod_deepwell -/
  | stat_alpha
  /-- OBS [stated: "However, the old α-enhanced disk metallicity distribution function (MDF) is truncated, or at least drops sharply, below"] Section I (continues: [M/H] = -1) -/
  | obs_discfloor
  /-- GAP [reconstructed] the metal-poor stars and the old disc belong to one chemically connected system with a monotonic enrichment history; R22 itself expects the oldest metal-poor stars to mix early proto-Galactic pieces and later-merged satellites (Section I), and Ardern-Arentsen et al. 2024 (arXiv:2312.03847) propose a more metal-poor, more extended component from smaller accreted galaxies; a slowly enriching fragment can form [M/H] below -1.5 stars after the oldest disc stars at -1. R22 hedges the step: most likely predate (abstract) -/
  | gap_onezone
  /-- MOD [implied] one-zone chemical evolution: within a single well-mixed system metallicity rises monotonically with time, so stars more metal-poor than the oldest disc stars formed earlier (Tinsley 1980, Fundamentals of Cosmic Physics 5, 287, bibcode 1980FCPh....5..287T) -/
  | mod_amr
  /-- LIT [stated: "appear to be ≈12.5 Gyrs old"] Section IV (subject: the oldest alpha-enhanced disc members, at [M/H] near -1); R22 ref. 96, Xiang and Rix 2022, Nature 603, 599, arXiv:2203.12110 -/
  | lit_discage
  /-- MOD [stated: "it must have formed at τ≳12.5 Gyrs, corresponding to z≳5"] Section IV (conditional: if much of this metal-poor heart chemically, and therefore temporally, predates the oldest alpha-enhanced disk); encoded with the disc age as antecedent -/
  | mod_ancient
  /-- MOD [stated: "arguing against an origin through accretion from a once-distant satellite"] Section IV (subject: much of this population is confined within the solar circle, tightly bound); encoded with the central concentration and the small apocentres as antecedents; the atom says disfavoured, as the quote does -/
  | mod_confined
  /-- MOD [stated: "are distinctly α-enhanced, arguing for rapid enrichment in a deep potential well"] Section IV; the atom says favoured, as the quote does -/
  | mod_deepwell
  /-- GAP [reconstructed] mass, age, confinement, a deep well and the rotation trend make the population the proto-Galaxy in-situ core rather than debris of an early accreted galaxy. R22 hedges both steps: such stars are most likely to occur at the center of a (eventually) quite massive halo, not at a low-mass satellite (Section IV), and the information fits a picture in which the heart constitutes the most ancient proto-Galactic component (Section IV); the proposed Heracles/Kraken/Koala debris is virtually indistinguishable in all chemical spaces (Section III.4), early in-situ and accreted stars may be operationally impossible to separate (Section I), and Ardern-Arentsen et al. 2024 (arXiv:2312.03847) attribute a more metal-poor, extended component to smaller accreted galaxies -/
  | gap_proto
  deriving DecidableEq, Repr

def prov : Field → Prov
  | .stat_prec => .stated
  | .gap_pure => .reconstructed
  | .mod_tail => .implied
  | .obs_count => .stated
  | .mod_m4 => .stated
  | .gap_template => .reconstructed
  | .mod_face => .stated
  | .obs_incomplete => .stated
  | .mod_corr => .stated
  | .mod_sph => .stated
  | .stat_sigma => .stated
  | .gap_sel => .reconstructed
  | .mod_central => .stated
  | .stat_norot => .stated
  | .stat_spin => .stated
  | .stat_apo => .stated
  | .stat_alpha => .stated
  | .obs_discfloor => .stated
  | .gap_onezone => .reconstructed
  | .mod_amr => .implied
  | .lit_discage => .stated
  | .mod_ancient => .stated
  | .mod_confined => .stated
  | .mod_deepwell => .stated
  | .gap_proto => .reconstructed

def prem : Field → Vocab → Prop
  | .stat_prec, v => v.Precise
  | .gap_pure, v => v.Pure
  | .mod_tail, v => v.Precise → v.Pure → v.TailReal
  | .obs_count, v => v.CountMP
  | .mod_m4, v => v.M4Ratio
  | .gap_template, v => v.TemplateOK
  | .mod_face, v => v.TailReal → v.CountMP → v.M4Ratio → v.TemplateOK → v.FaceMass
  | .obs_incomplete, v => v.Incomplete
  | .mod_corr, v => v.FaceMass → v.Incomplete → v.Massive
  | .mod_sph, v => v.SphGauss
  | .stat_sigma, v => v.SigmaFit
  | .gap_sel, v => v.SelOK
  | .mod_central, v => v.TailReal → v.SphGauss → v.SigmaFit → v.SelOK → v.Central
  | .stat_norot, v => v.NoRotVMP
  | .stat_spin, v => v.RotRich
  | .stat_apo, v => v.ApoSmall
  | .stat_alpha, v => v.AlphaEnh
  | .obs_discfloor, v => v.DiscFloor
  | .gap_onezone, v => v.OneSystem
  | .mod_amr, v => v.OneSystem → v.TailReal → v.DiscFloor → v.Predates
  | .lit_discage, v => v.DiscAge
  | .mod_ancient, v => v.Predates → v.DiscAge → v.Ancient
  | .mod_confined, v => v.Central → v.ApoSmall → v.NotDistant
  | .mod_deepwell, v => v.AlphaEnh → v.DeepWell
  | .gap_proto, v =>
      v.Massive → v.Ancient → v.NotDistant → v.DeepWell → v.NoRotVMP → v.RotRich → v.ProtoGal

/-- [stated: "This sample reveals an extensive, ancient, and metal-poor population"] Abstract (continues: that includes about 18,000 stars, a stellar mass of at least about 5e7 Msun, a Gaussian extent of about 2.7 kpc; these central, metal-poor stars most likely predate the oldest part of the disk, about 12.5 Gyr, so formed at z of about 5 or more); part 4 rests on Section IV: All of this information fits a picture in which this metal-poor heart of the Milky Way constitutes the most ancient proto-Galactic component of our Galaxy -/
def Conclusion (v : Vocab) : Prop := v.Massive ∧ v.Central ∧ v.Ancient ∧ v.ProtoGal

-- FIXED BLOCK B (identical in every study)
def Premises (v : Vocab) : Prop := ∀ f, prem f v
def Without (g : Field) (v : Vocab) : Prop := ∀ f, f ≠ g → prem f v
def Stated (v : Vocab) : Prop := ∀ f, prov f = .stated → prem f v
def Explicit (v : Vocab) : Prop := ∀ f, prov f ≠ .reconstructed → prem f v
-- END FIXED BLOCK B

/-- A model in which every premise and the conclusion hold; countermodels change a few fields. -/
def full : Vocab :=
  { Precise := True, Pure := True, TailReal := True, CountMP := True, M4Ratio := True,
    TemplateOK := True, FaceMass := True, Incomplete := True, Massive := True,
    SphGauss := True, SigmaFit := True, SelOK := True, Central := True,
    NoRotVMP := True, RotRich := True, ApoSmall := True, AlphaEnh := True,
    DiscFloor := True, OneSystem := True, Predates := True, DiscAge := True, Ancient := True,
    NotDistant := True, DeepWell := True, ProtoGal := True }

/-- The paper's chain, step by step. -/
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  -- Stage A: the metal-poor tail is real (Section II.3; Appendix A)
  have t : v.TailReal := p .mod_tail (p .stat_prec) (p .gap_pure)                     -- GAP
  -- Stage B: counts and mass (Section III.2)
  have fm : v.FaceMass := p .mod_face t (p .obs_count) (p .mod_m4) (p .gap_template)  -- GAP
  have m : v.Massive := p .mod_corr fm (p .obs_incomplete)
  -- Stage C: central concentration (Section III.1; Section IV)
  have c : v.Central := p .mod_central t (p .mod_sph) (p .stat_sigma) (p .gap_sel)    -- GAP
  -- Stage E: age; predates the oldest disc, so at least 12.5 Gyr old (Sections I, IV)
  have pd : v.Predates := p .mod_amr (p .gap_onezone) t (p .obs_discfloor)           -- GAP
  have a : v.Ancient := p .mod_ancient pd (p .lit_discage)
  -- Stage F: origin, with the stage D data (Sections III.3, III.4, IV)
  have nd : v.NotDistant := p .mod_confined c (p .stat_apo)
  have dw : v.DeepWell := p .mod_deepwell (p .stat_alpha)
  have pg : v.ProtoGal :=
    p .gap_proto m a nd dw (p .stat_norot) (p .stat_spin)                               -- GAP
  exact ⟨m, c, a, pg⟩

theorem final_nontrivial : ¬ ∀ v : Vocab, Conclusion v :=
  fun h => (h { full with Massive := False }).1

theorem consistent : ∃ v, Premises v :=
  ⟨full, by intro f; cases f <;> simp [prem, full]⟩

theorem alone_insufficient : ∀ g, ¬ ∀ v, prem g v → Conclusion v := by
  intro g h
  cases g
  case gap_proto => exact (h { full with Massive := False } (by simp [prem, full])).1
  all_goals exact (h { full with ProtoGal := False } (by simp [prem, full])).2.2.2

-- Stage A
theorem stat_prec_needed : ¬ ∀ v, Without .stat_prec v → Conclusion v := fun h =>
  (h { full with Precise := False, TailReal := False, FaceMass := False, Massive := False,
                   Central := False, Predates := False, Ancient := False, NotDistant := False, ProtoGal := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

theorem gap_pure_needed : ¬ ∀ v, Without .gap_pure v → Conclusion v := fun h =>
  (h { full with Pure := False, TailReal := False, FaceMass := False, Massive := False,
                   Central := False, Predates := False, Ancient := False, NotDistant := False, ProtoGal := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

theorem mod_tail_needed : ¬ ∀ v, Without .mod_tail v → Conclusion v := fun h =>
  (h { full with TailReal := False, FaceMass := False, Massive := False,
                   Central := False, Predates := False, Ancient := False, NotDistant := False, ProtoGal := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

-- Stage B
theorem obs_count_needed : ¬ ∀ v, Without .obs_count v → Conclusion v := fun h =>
  (h { full with CountMP := False, FaceMass := False, Massive := False, ProtoGal := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

theorem mod_m4_needed : ¬ ∀ v, Without .mod_m4 v → Conclusion v := fun h =>
  (h { full with M4Ratio := False, FaceMass := False, Massive := False, ProtoGal := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

theorem gap_template_needed : ¬ ∀ v, Without .gap_template v → Conclusion v := fun h =>
  (h { full with TemplateOK := False, FaceMass := False, Massive := False, ProtoGal := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

theorem mod_face_needed : ¬ ∀ v, Without .mod_face v → Conclusion v := fun h =>
  (h { full with FaceMass := False, Massive := False, ProtoGal := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

theorem obs_incomplete_needed : ¬ ∀ v, Without .obs_incomplete v → Conclusion v := fun h =>
  (h { full with Incomplete := False, Massive := False, ProtoGal := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

theorem mod_corr_needed : ¬ ∀ v, Without .mod_corr v → Conclusion v := fun h =>
  (h { full with Massive := False, ProtoGal := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).1

-- Stage C
theorem mod_sph_needed : ¬ ∀ v, Without .mod_sph v → Conclusion v := fun h =>
  (h { full with SphGauss := False, Central := False, NotDistant := False, ProtoGal := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.1

theorem stat_sigma_needed : ¬ ∀ v, Without .stat_sigma v → Conclusion v := fun h =>
  (h { full with SigmaFit := False, Central := False, NotDistant := False, ProtoGal := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.1

theorem gap_sel_needed : ¬ ∀ v, Without .gap_sel v → Conclusion v := fun h =>
  (h { full with SelOK := False, Central := False, NotDistant := False, ProtoGal := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.1

theorem mod_central_needed : ¬ ∀ v, Without .mod_central v → Conclusion v := fun h =>
  (h { full with Central := False, NotDistant := False, ProtoGal := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.1

-- Stage D
theorem stat_norot_needed : ¬ ∀ v, Without .stat_norot v → Conclusion v := fun h =>
  (h { full with NoRotVMP := False, ProtoGal := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2.2

theorem stat_spin_needed : ¬ ∀ v, Without .stat_spin v → Conclusion v := fun h =>
  (h { full with RotRich := False, ProtoGal := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2.2

theorem stat_apo_needed : ¬ ∀ v, Without .stat_apo v → Conclusion v := fun h =>
  (h { full with ApoSmall := False, NotDistant := False, ProtoGal := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2.2

theorem stat_alpha_needed : ¬ ∀ v, Without .stat_alpha v → Conclusion v := fun h =>
  (h { full with AlphaEnh := False, DeepWell := False, ProtoGal := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2.2

-- Stage E: age
theorem obs_discfloor_needed : ¬ ∀ v, Without .obs_discfloor v → Conclusion v := fun h =>
  (h { full with DiscFloor := False, Predates := False, Ancient := False, ProtoGal := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2.1

theorem gap_onezone_needed : ¬ ∀ v, Without .gap_onezone v → Conclusion v := fun h =>
  (h { full with OneSystem := False, Predates := False, Ancient := False, ProtoGal := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2.1

theorem mod_amr_needed : ¬ ∀ v, Without .mod_amr v → Conclusion v := fun h =>
  (h { full with Predates := False, Ancient := False, ProtoGal := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2.1

theorem lit_discage_needed : ¬ ∀ v, Without .lit_discage v → Conclusion v := fun h =>
  (h { full with DiscAge := False, Ancient := False, ProtoGal := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2.1

theorem mod_ancient_needed : ¬ ∀ v, Without .mod_ancient v → Conclusion v := fun h =>
  (h { full with Ancient := False, ProtoGal := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2.1

-- Stage F: origin
theorem mod_confined_needed : ¬ ∀ v, Without .mod_confined v → Conclusion v := fun h =>
  (h { full with NotDistant := False, ProtoGal := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2.2

theorem mod_deepwell_needed : ¬ ∀ v, Without .mod_deepwell v → Conclusion v := fun h =>
  (h { full with DeepWell := False, ProtoGal := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2.2

theorem gap_proto_needed : ¬ ∀ v, Without .gap_proto v → Conclusion v := fun h =>
  (h { full with ProtoGal := False }
    (by intro f hf; cases f <;> simp_all [prem, full])).2.2.2

/-- What the paper writes is not enough: besides the gaps, it relies on two standard rules it
does not write out (a precise and pure selection is genuine; metallicity rises with time in one
system). -/
theorem stated_insufficient : ¬ ∀ v, Stated v → Conclusion v := fun h =>
  (h { full with TailReal := False, FaceMass := False, Massive := False,
                   Central := False, Predates := False, Ancient := False, NotDistant := False, ProtoGal := False }
    (by intro f hf; cases f <;> simp_all [prov, prem, full])).1

/-- Standard knowledge does not close the argument: five gaps remain. -/
theorem explicit_insufficient : ¬ ∀ v, Explicit v → Conclusion v := fun h =>
  (h { full with Pure := False, TailReal := False, FaceMass := False, Massive := False,
                   Central := False, Predates := False, Ancient := False, NotDistant := False, ProtoGal := False }
    (by intro f hf; cases f <;> simp_all [prov, prem, full])).1

end Argument
