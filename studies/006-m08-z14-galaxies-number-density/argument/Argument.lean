/-
Argument of the paper, decomposed: Naidu et al. 2026, "A Cosmic Miracle: A Remarkably Luminous
Galaxy at z_spec = 14.44 Confirmed with JWST" (OJAp 9; arXiv:2505.11263; "N26"). Context in the
wiki article: Carniani et al. 2024 (arXiv:2405.18485), Harikane et al. 2025 (arXiv:2406.18352),
Shen et al. 2023 (arXiv:2305.05679).

The conclusion encoded is the statistical sentence of Sec. 4.1, whose grammatical subject is the
LF N26 constructs to represent the pre-JWST theoretical consensus: that LF is disfavored at high
confidence by the two z = 14-15 sources. The step from that LF to the consensus itself is
discussed in the wiki article, not encoded.

The chain:
  at least two spectroscopically confirmed sources (MoM-z14, JADES-GS-z14-0) lie at z = 14-15
      with -21 < M_UV < -20 in the declared PRIMER and JOF area (388 arcmin2)
  over that area N26's constructed LF underestimates their incidence by about 200x (182x)
  [implied] Poisson mathematics: with at least two sources observed and a ratio of at least 100,
      the expected count is at most n_obs / 100 and the probability of at least n_obs sources is
      at most 2e-4 (197 ppm at n_obs = 2 and ratio 100; smaller for larger n_obs or ratio; 60 ppm
      at the stated 182, computed in results/r1.json)
  [gap] the counts in that area follow Poisson statistics about the model mean (no
      cosmic-variance excess; N26 does not discuss cosmic variance)
  [gap] the declared area is the full effective search for this bin (the fields are those where
      the detections were made; further area of comparable depth and spectroscopic follow-up
      without a detection would lower the observed density and raise the expected count)
  [gap] decision rule: a model under which the observed count has a tail probability of at most
      2e-4 is disfavored at high confidence (N26 names no test, threshold or mapping from
      probability to confidence)
  -> N26's pre-JWST LF is disfavored at high confidence

Not encoded: N26's assumption that the two sources are the only ones in the bin. Further sources
in the declared area would raise the count, so this direction cannot weaken the conclusion (the
count enters as "at least two"); the opposite direction, through the area, is gap_area.

Rules: AGENTS.md section 2 (paper study, Lean); specification: design/007 section 2.2.
Quotes follow the arXiv HTML (v2) as rendered.
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
  /-- Number of spectroscopically confirmed sources at z = 14-15 with -21 < M_UV < -20 in the declared PRIMER and JOF area. -/
  n_obs : Nat
  /-- Ratio of the observed number density to that of N26's pre-JWST LF in the same bin and area (rounded down). -/
  ratio : Nat
  /-- Poisson probability, in parts per million, of observing at least n_obs sources when the expected count is n_obs / ratio (a function of n_obs and ratio). -/
  tail_ppm : Nat
  /-- The source counts in the declared area follow Poisson statistics about the model mean (no excess field-to-field variance). -/
  PoissonOK : Prop
  /-- The declared area is the full effective search for this bin (no further area of comparable depth and follow-up without a detection). -/
  AreaFull : Prop
  /-- The redshift and magnitude bin was fixed independently of the two detections (no look-elsewhere inflation of the significance). -/
  BinPrior : Prop
  /-- N26's constructed pre-JWST LF is disfavored at high confidence by the counts. -/
  ModelDisfavored : Prop

/-- The premises. -/
inductive Field where
  /-- OBS [stated 2505.11263: "we assume MoM-z14 and JADES-GS-z14-0 are the only −21<MUV<−20 sources"] Sec. 4.1 (z = 14-15, PRIMER and JOF area); the quote is N26 counting assumption for the LF estimate; the body keeps only its observational part, that at least two such sources are spectroscopically confirmed (N26 Sec. 3, C24) -/
  | obs_count
  /-- STAT [stated 2505.11263: "Such an LF underestimates the incidence of observed sources by ≈200×"] Sec. 4.1 (182, interval +329 and -105, presumably from the Poisson uncertainty of the observed count; N26 does not say) -/
  | stat_ratio
  /-- MOD [implied] Poisson mathematics: if at least two sources are observed and the ratio is at least 100, the probability of at least n_obs sources for expected count n_obs / ratio is at most 2e-4 (the tail decreases with n_obs and with the ratio; 197 ppm at 2 and 100); textbook Poisson statistics (e.g. Gehrels 1986, ApJ 303, 336); the value at the stated 182 (60 ppm) is computed in results/r1.json -/
  | mod_poisson
  /-- GAP [reconstructed] decision rule: a model under which the observed count of at least two sources in the full effective search has a Poisson tail probability of at most 2e-4, with Poisson counts, is disfavored at high confidence; N26 gives no test, threshold or mapping from probability to confidence, so the 2e-4 cutoff is ours (significance testing in general: Wasserman 2004, All of Statistics, ch. 10) -/
  | gap_rule
  /-- GAP [reconstructed] the counts in 388 arcmin2 follow Poisson statistics about the model mean; N26 does not discuss cosmic variance, which for rare, strongly clustered halos at z ~ 14 can exceed Poisson noise (e.g. Somerville et al. 2004, ApJ 600, L171; Trenti and Stiavelli 2008, ApJ 676, 767) -/
  | gap_poisson
  /-- GAP [reconstructed] the declared area (PRIMER-COSMOS, PRIMER-UDS, JOF: the fields where the two sources were found) is the full effective search for this bin; the tail exceeds 2e-4 if the effective area is about 1.8 times larger (ratio about 100) and 1.35e-3 (one-sided 3 sigma) at about 4.8 times (ratio about 38) -/
  | gap_area
  /-- GAP [reconstructed] the bin (z = 14-15, -21 < M_UV < -20) was chosen independently of the two detections; it is drawn around them, so the tail probability of a bin chosen after the fact overstates the significance (look-elsewhere effect); added after the independent referee, 2026-11-15 -/
  | gap_bin
  deriving DecidableEq, Repr

def prov : Field → Prov
  | .obs_count => .stated
  | .stat_ratio => .stated
  | .mod_poisson => .implied
  | .gap_rule => .reconstructed
  | .gap_poisson => .reconstructed
  | .gap_area => .reconstructed
  | .gap_bin => .reconstructed

def prem : Field → Vocab → Prop
  | .obs_count, v => v.n_obs ≥ 2
  | .stat_ratio, v => v.ratio ≥ 100
  | .mod_poisson, v => v.n_obs ≥ 2 → v.ratio ≥ 100 → v.tail_ppm ≤ 200
  | .gap_rule, v =>
      v.n_obs ≥ 2 → v.ratio ≥ 100 → v.tail_ppm ≤ 200 → v.PoissonOK → v.AreaFull → v.BinPrior →
        v.ModelDisfavored
  | .gap_poisson, v => v.PoissonOK
  | .gap_area, v => v.AreaFull
  | .gap_bin, v => v.BinPrior

/-- [stated 2505.11263: "and is disfavored at high confidence"] Sec. 4.1; the subject of the sentence is Such an LF, the pre-JWST LF that N26 constructs -/
def Conclusion (v : Vocab) : Prop := v.ModelDisfavored

-- FIXED BLOCK B (identical in every study)
def Premises (v : Vocab) : Prop := ∀ f, prem f v
def Without (g : Field) (v : Vocab) : Prop := ∀ f, f ≠ g → prem f v
def Stated (v : Vocab) : Prop := ∀ f, prov f = .stated → prem f v
def Explicit (v : Vocab) : Prop := ∀ f, prov f ≠ .reconstructed → prem f v
-- END FIXED BLOCK B

/-- The paper's chain, step by step. -/
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  have h1 : v.tail_ppm ≤ 200 := p .mod_poisson (p .obs_count) (p .stat_ratio)  -- Poisson tail
  exact p .gap_rule (p .obs_count) (p .stat_ratio) h1 (p .gap_poisson) (p .gap_area)
    (p .gap_bin)  -- Sec. 4.1; GAPs

theorem final_nontrivial : ¬ ∀ v : Vocab, Conclusion v :=
  fun h => h ⟨0, 0, 0, False, False, False, False⟩

theorem consistent : ∃ v, Premises v :=
  ⟨⟨2, 182, 60, True, True, True, True⟩, by intro f; cases f <;> simp [prem]⟩

theorem alone_insufficient : ∀ g, ¬ ∀ v, prem g v → Conclusion v := by
  intro g h
  cases g
  case gap_rule => exact h ⟨0, 0, 1000, False, False, False, False⟩ (by simp [prem])
  all_goals exact h ⟨2, 182, 60, True, True, True, False⟩ (by simp [prem])

theorem obs_count_needed : ¬ ∀ v, Without .obs_count v → Conclusion v := fun h =>
  h ⟨0, 182, 60, True, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem stat_ratio_needed : ¬ ∀ v, Without .stat_ratio v → Conclusion v := fun h =>
  h ⟨2, 0, 60, True, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem mod_poisson_needed : ¬ ∀ v, Without .mod_poisson v → Conclusion v := fun h =>
  h ⟨2, 182, 1000, True, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem gap_rule_needed : ¬ ∀ v, Without .gap_rule v → Conclusion v := fun h =>
  h ⟨2, 182, 60, True, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem gap_poisson_needed : ¬ ∀ v, Without .gap_poisson v → Conclusion v := fun h =>
  h ⟨2, 182, 60, False, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem gap_area_needed : ¬ ∀ v, Without .gap_area v → Conclusion v := fun h =>
  h ⟨2, 182, 60, True, False, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem gap_bin_needed : ¬ ∀ v, Without .gap_bin v → Conclusion v := fun h =>
  h ⟨2, 182, 60, True, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prem])

/-- What the paper writes is not enough: the Poisson tail is standard background (implied), and
the decision rule, the Poisson, the area and the bin assumptions are not stated. -/
theorem stated_insufficient : ¬ ∀ v, Stated v → Conclusion v := fun h =>
  h ⟨2, 182, 1000, False, False, False, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])

/-- Even with standard knowledge the chain has four gaps: the decision rule from tail probability
to high confidence, Poisson counts (no cosmic-variance excess), the declared area being the full
effective search and a bin fixed independently of the detections. -/
theorem explicit_insufficient : ¬ ∀ v, Explicit v → Conclusion v := fun h =>
  h ⟨2, 182, 60, False, False, False, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])

end Argument
