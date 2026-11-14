/-
Argument of the paper, decomposed (template).

Rules: AGENTS.md section 2 (paper study, Lean). Exact specification: design/007 section 2.2.
Checked by tests/test_lean_arguments.py. Replace the EXAMPLE parts; keep FIXED BLOCK A and
FIXED BLOCK B unchanged and keep the names of the required theorems.

The EXAMPLE is illustrative only (a simplified dark-companion argument), not any paper's
actual reasoning.

Conventions (summary; the spec is authoritative)
* Vocab: atoms only. Field types: Prop, Type, Nat, Int, predicates over earlier Type fields or
  Nat/Int, or elements of earlier Type fields. Never proofs. Every field has a doc comment.
* Field: one argument-free constructor per premise. Doc comment: KIND [provenance] source.
  KIND: OBS MOD STAT NUM LIT GAP. Provenance (relative to the analysed paper):
  [stated: "verbatim quote"] / [implied] followed by its source / [reconstructed].
  GAP exactly when [reconstructed]. OBS/NUM/STAT bodies are literals (atom, negated atom,
  field-versus-literal comparison). NUM is "field op literal" and carries
  NUM[results/<file>.json:<key> <op> <value>] matching the Lean threshold up to a power of 10.
  LIT cites a bibcode or arXiv id. No top-level conjunction in a premise.
* prov and prem: one equation per constructor, no wildcard. prem and Conclusion use only Vocab
  fields, logical connectives, integer literals and comparisons; no helper definitions.
* Required theorems: final, final_nontrivial, consistent, alone_insufficient; for every premise
  c exactly one of c_needed / c_redundant; exactly one of stated_sufficient /
  stated_insufficient; exactly one of explicit_sufficient / explicit_insufficient.
* Identifiers are ASCII (h1, not h with a subscript). No string literals outside comments.
* Countermodels: a concrete Vocab plus
    by intro f hf; cases f <;> simp_all [prem]          (for c_needed)
    by intro f hf; cases f <;> simp_all [prov, prem]    (for stated_* / explicit_*)
-/

namespace Argument

-- FIXED BLOCK A (identical in every study)
inductive Prov where
  | stated
  | implied
  | reconstructed
  deriving DecidableEq
-- END FIXED BLOCK A

/-- The atoms of the argument (EXAMPLE). -/
structure Vocab where
  /-- An astrometric orbit of the visible star is detected. -/
  Orbit : Prop
  /-- The astrometric mass function, in units of 0.01 solar masses. -/
  fm_centi : Nat
  /-- The unseen companion is more massive than 3 solar masses. -/
  MassAbove3 : Prop
  /-- No light from the companion is detected. -/
  Dark : Prop
  /-- The companion is itself a close binary of two faint stars. -/
  InnerBinary : Prop
  /-- The companion is a black hole. -/
  BlackHole : Prop

/-- The premises (EXAMPLE). -/
inductive Field where
  /-- OBS [stated: "we detect a significant astrometric orbit"] Sec. 2, Table 1 -/
  | obs_orbit
  /-- NUM [stated: "the mass function is 3.4 solar masses"] Sec. 3, eq. 2 NUM[results/orbit.json:f_m_msun > 3.0] -/
  | num_fm
  /-- MOD [implied] textbook: the mass function is a lower limit on the companion mass -/
  | mod_fm_bound
  /-- OBS [stated: "no light from the companion is detected"] Sec. 4, Fig. 3 -/
  | obs_dark
  /-- MOD [stated: "a dark object above 3 solar masses is a black hole unless it is a binary"] Sec. 5 -/
  | mod_dark_massive
  /-- GAP [reconstructed] the companion is not an inner binary; the paper gives no test -/
  | gap_no_inner_binary
  deriving DecidableEq, Repr

def prov : Field → Prov
  | .obs_orbit => .stated
  | .num_fm => .stated
  | .mod_fm_bound => .implied
  | .obs_dark => .stated
  | .mod_dark_massive => .stated
  | .gap_no_inner_binary => .reconstructed

def prem : Field → Vocab → Prop
  | .obs_orbit, v => v.Orbit
  | .num_fm, v => v.fm_centi > 300
  | .mod_fm_bound, v => v.fm_centi > 300 → v.MassAbove3
  | .obs_dark, v => v.Dark
  | .mod_dark_massive, v => v.Dark → v.MassAbove3 → v.BlackHole ∨ v.InnerBinary
  | .gap_no_inner_binary, v => ¬ v.InnerBinary

/-- [stated: "the companion is a black hole"] Sec. 6 -/
def Conclusion (v : Vocab) : Prop := v.BlackHole

-- FIXED BLOCK B (identical in every study)
def Premises (v : Vocab) : Prop := ∀ f, prem f v
def Without (g : Field) (v : Vocab) : Prop := ∀ f, f ≠ g → prem f v
def Stated (v : Vocab) : Prop := ∀ f, prov f = .stated → prem f v
def Explicit (v : Vocab) : Prop := ∀ f, prov f ≠ .reconstructed → prem f v
-- END FIXED BLOCK B

/-- The paper's chain, step by step. -/
theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  have h1 : v.MassAbove3 := p .mod_fm_bound (p .num_fm)   -- Sec. 3
  have h2 := p .mod_dark_massive (p .obs_dark) h1           -- Sec. 4-5
  exact h2.resolve_right (p .gap_no_inner_binary)           -- unstated step

theorem final_nontrivial : ¬ ∀ v : Vocab, Conclusion v :=
  fun h => h ⟨False, 0, False, False, False, False⟩

/-- Weak here: the only negative premise is the GAP. -/
theorem consistent : ∃ v, Premises v :=
  ⟨⟨True, 340, True, True, False, True⟩, by intro f; cases f <;> simp [prem]⟩

theorem alone_insufficient : ∀ g, ¬ ∀ v, prem g v → Conclusion v := by
  intro g h
  cases g
  · exact h ⟨True, 0, False, False, False, False⟩ trivial
  · exact h ⟨False, 340, False, False, False, False⟩ (by simp [prem])
  · exact h ⟨False, 0, False, False, False, False⟩ (by simp [prem])
  · exact h ⟨False, 0, False, True, False, False⟩ trivial
  · exact h ⟨False, 0, False, False, False, False⟩ (fun x => x.elim)
  · exact h ⟨False, 0, False, False, False, False⟩ (fun x => x)

/-- Redundant by construction: the atom Orbit appears in no other premise nor in the
conclusion (the dependence of num_fm on the orbit is not encoded). An encoding artefact,
not a finding about the paper. -/
theorem obs_orbit_redundant : ∀ v, Without .obs_orbit v → Conclusion v := by
  intro v p
  have h1 : v.MassAbove3 := p .mod_fm_bound (by decide) (p .num_fm (by decide))
  exact (p .mod_dark_massive (by decide) (p .obs_dark (by decide)) h1).resolve_right
    (p .gap_no_inner_binary (by decide))

theorem num_fm_needed : ¬ ∀ v, Without .num_fm v → Conclusion v := fun h =>
  h ⟨True, 0, False, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem mod_fm_bound_needed : ¬ ∀ v, Without .mod_fm_bound v → Conclusion v := fun h =>
  h ⟨True, 340, False, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem obs_dark_needed : ¬ ∀ v, Without .obs_dark v → Conclusion v := fun h =>
  h ⟨True, 340, True, False, False, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem mod_dark_massive_needed : ¬ ∀ v, Without .mod_dark_massive v → Conclusion v := fun h =>
  h ⟨True, 340, True, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prem])

theorem gap_no_inner_binary_needed : ¬ ∀ v, Without .gap_no_inner_binary v → Conclusion v :=
  fun h => h ⟨True, 340, True, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prem])

/-- What the paper writes is not enough (it also relies on the textbook mass-function bound). -/
theorem stated_insufficient : ¬ ∀ v, Stated v → Conclusion v := fun h =>
  h ⟨True, 340, False, True, False, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])

/-- Even with standard knowledge the argument has a real gap: the inner-binary case. -/
theorem explicit_insufficient : ¬ ∀ v, Explicit v → Conclusion v := fun h =>
  h ⟨True, 340, True, True, True, False⟩ (by intro f hf; cases f <;> simp_all [prov, prem])

end Argument
