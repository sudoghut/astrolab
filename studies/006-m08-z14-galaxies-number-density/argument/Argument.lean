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
  [implied] the expected count is then n_obs / 182 and the Poisson probability of at least two
      sources is below 2e-4 (our computation)
  [gap] the counts in that area follow Poisson statistics about the model mean (no
      cosmic-variance excess; N26 does not discuss cosmic variance)
  [gap] the declared area is the full effective search for this bin (the fields are those where
      the detections were made; further area of comparable depth and spectroscopic follow-up
      without a detection would lower the observed density and raise the expected count)
  [implied] a model under which the observed count has such a small tail probability is
      disfavored at high confidence
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
  /-- Poisson probability, in parts per million, of observing at least n_obs sources when the expected count is n_obs / ratio. -/
  tail_ppm : Nat
  /-- The source counts in the declared area follow Poisson statistics about the model mean (no excess field-to-field variance). -/
  PoissonOK : Prop
  /-- The declared area is the full effective search for this bin (no further area of comparable depth and follow-up without a detection). -/
  AreaFull : Prop
  /-- N26's constructed pre-JWST LF is disfavored at high confidence by the counts. -/
  ModelDisfavored : Prop

/-- The premises. -/
inductive Field where
  /-- OBS [stated 2505.11263: "we assume MoM-z14 and JADES-GS-z14-0 are the only −21<MUV<−20 sources"] Sec. 4.1 (z = 14-15, PRIMER and JOF area); the spectroscopic confirmations are N26 Sec. 3 and C24; the body uses only that there are at least two -/
  | obs_count
  /-- STAT [stated 2505.11263: "Such an LF underestimates the incidence of observed sources by ≈200×"] Sec. 4.1 (182, interval +329 and -105, presumably from the Poisson uncertainty of the observed count; N26 does not say) -/
  | stat_ratio
  /-- NUM [implied] Poisson tail P(N >= 2) for expected count 2/182 in the declared area; textbook Poisson statistics (e.g. Gehrels 1986, ApJ 303, 336) NUM[results/r1.json:p_tail_n26_ppm <= 200] -/
  | num_tail
  /-- MOD [implied] a model under which the observed count of at least two sources in the full effective search has a Poisson tail probability of at most 2e-4, with Poisson counts, is disfavored at high confidence (significance testing, Wasserman 2004, All of Statistics, ch. 10) -/
  | mod_test
  /-- GAP [reconstructed] the counts in 388 arcmin2 follow Poisson statistics about the model mean; N26 does not discuss cosmic variance, which for rare, strongly clustered halos at z ~ 14 can exceed Poisson noise (e.g. Somerville et al. 2004, ApJ 600, L171; Trenti and Stiavelli 2008, ApJ 676, 767) -/
  | gap_poisson
  /-- GAP [reconstructed] the declared area (PRIMER-COSMOS, PRIMER-UDS, JOF: the fields where the two sources were found) is the full effective search for this bin; the tail exceeds 2e-4 if the effective area is about 1.8 times larger (ratio about 100) and 1.35e-3 (one-sided 3 sigma) at about 4.8 times (ratio about 38) -/
  | gap_area
  deriving DecidableEq, Repr

def prov : Field → Prov
  | .obs_count => .stated
  | .stat_ratio => .stated
  | .num_tail => .implied
  | .mod_test => .implied
  | .gap_poisson => .reconstructed
  | .gap_area => .reconstructed

def prem : Field → Vocab → Prop
  | .obs_count, v => v.n_obs ≥ 2
  | .stat_ratio, v => v.ratio ≥ 100
  | .num_tail, v => v.tail_ppm ≤ 200
  | .mod_test, v =>
      v.n_obs ≥ 2 → v.ratio ≥ 100 → v.tail_ppm ≤ 200 → v.PoissonOK → v.AreaFull → v.ModelDisfavored
  | .gap_poisson, v => v.PoissonOK
  | .gap_area, v => v.AreaFull

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
  exact p .mod_test (p .obs_count) (p .stat_ratio) (p .num_tail) (p .gap_poisson)
    (p .gap_area)  -- Sec. 4.1; two GAPs

theorem final_nontrivial : ¬ ∀ v : Vocab, Conclusion v :=
  fun h => h ⟨0, 0, 0, False, False, False⟩

theorem consistent : ∃ v, Premises v :=
  ⟨⟨2, 182, 60, True, True, True⟩, by intro f; cases f <;> simp [prem]⟩

theorem alone_insufficient : ∀ g, ¬ ∀ v, prem g v → Conclusion v := by
  intro g h
  cases g
  case mod_test => exact h ⟨0, 0, 1000, False, False, False⟩ (by simp [prem])
  all_goals exact h ⟨2, 182, 60, True, True, False⟩ (by simp [prem])

theorem obs_count_needed : ¬ ∀ v, Without .obs_count v → Conclusion v := fun h =>
  h ⟨0, 182, 60, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem stat_ratio_needed : ¬ ∀ v, Without .stat_ratio v → Conclusion v := fun h =>
  h ⟨2, 0, 60, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem num_tail_needed : ¬ ∀ v, Without .num_tail v → Conclusion v := fun h =>
  h ⟨2, 182, 1000, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem mod_test_needed : ¬ ∀ v, Without .mod_test v → Conclusion v := fun h =>
  h ⟨2, 182, 60, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem gap_poisson_needed : ¬ ∀ v, Without .gap_poisson v → Conclusion v := fun h =>
  h ⟨2, 182, 60, False, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem gap_area_needed : ¬ ∀ v, Without .gap_area v → Conclusion v := fun h =>
  h ⟨2, 182, 60, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prem])

/-- What the paper writes is not enough: the significance step is standard background (implied),
and the Poisson and area assumptions are not stated. -/
theorem stated_insufficient : ¬ ∀ v, Stated v → Conclusion v := fun h =>
  h ⟨2, 182, 1000, False, False, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])

/-- Even with standard knowledge the chain has two gaps: Poisson counts (no cosmic-variance
excess) and the declared area being the full effective search. -/
theorem explicit_insufficient : ¬ ∀ v, Explicit v → Conclusion v := fun h =>
  h ⟨2, 182, 60, False, False, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])

end Argument
