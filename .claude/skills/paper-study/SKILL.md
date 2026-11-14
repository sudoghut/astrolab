---
name: paper-study
description: Turn one or more papers into an astrolab study - first a bilingual wiki article (plain-language walkthrough, argument logic decomposed and checked in Lean 4, what this repo can test), then a pre-registered study with run.py and a web page, then feed the implementation back into the wiki and keep it in sync. Use when the user wants to register a paper (or a set of papers) as a study, write the wiki article for a paper, or formalise a paper's argument in Lean.
---

# From paper(s) to study

Rules live in `AGENTS.md` (data limits in section 1; to-do list, design plans, bilingual rules,
paper-study, Lean and exploration rules in section 2; completion criteria in section 5). This
skill is the order of work and the checklists. Design rationale: `design/007-plan_*`.

## 0. Register and set up

- Register one `TODO.md` item. Write a design plan if the AGENTS.md section 2 complexity rule
  says so (a paper study reviewed in stages normally qualifies). The plan holds the stages below;
  the study's pre-registration lives in its README (step 4).
- Verify the paper(s) and read the full text read-only (arXiv HTML version or the PDF page via
  web reading; never save it into the project). Record arXiv IDs, journal reference and every
  number you will rely on, marked [V] once checked; copy the verbatim quotes you will tag `[stated]`.
- Create the study folder as scaffolding only: `python -m astrolab new <slug> "<title>" --level Lx`.
  The article needs it (its Lean file lives in `argument/`, its page name uses the study number);
  the study itself - pre-registration, `run.py`, web page - still comes after the article (step 4). Fill `study.yaml`
  `papers:` (arXiv IDs), `wiki:` (page name without `.md`, e.g. `Study-012-gaia-bh3`), and the Chinese fields (`title_zh`, `question_zh`; tests reject `TODO`).
- Retrofitting an existing, already implemented study: copy `argument/`, README section 8 and
  the `papers`/`wiki` fields from `studies/_template/` by hand; write the article the same way,
  but mark part 3's table "written after implementation (post hoc)" (AGENTS.md section 2).

## 1. Wiki article, part 1 - plain-language walkthrough

Copy `wiki-article-template.md` (next to this file) to `docs/wiki/Study-NNN-<slug>.md`.
Part 1 explains the paper to a curious non-specialist IN DETAIL - not a summary. Checks:

- [ ] Question, why it matters, what was known before.
- [ ] The data: what instrument measured what, in everyday terms, then precisely, with units.
- [ ] Every `OBS`, `NUM` and `STAT` premise of part 2, and every figure or table part 2 cites,
      is explained in 1.3 with its number and how it was obtained.
- [ ] A back-of-envelope version of the headline number.
- [ ] 1.4 says what would have to be true for the authors to be wrong.
- [ ] Test: could a reader reconstruct the chain of the argument from part 1 alone?
- [ ] Several papers: one walkthrough per paper (1.3a, 1.3b, ...) plus how they combine.
- [ ] Revisit this checklist after step 2, once the premises exist.

## 2. Wiki article, part 2 - argument logic + Lean

Academic register; explain every technical term.

1. **Decompose by logic, not by the paper's sections.** Start from the conclusion(s), work
   backwards to the claims each rests on, group them into 3-7 stages.
2. **Per stage in the article:** overview; premise table (Lean constructor, kind, provenance,
   source); rival explanations table (alternative, premise that excludes it, excluded explicitly
   by the paper?); Lean excerpt (the `have` steps of `final` that belong to this stage);
   critique.
3. **Lean:** copy `studies/_template/argument/` (done by `astrolab new`) and replace the EXAMPLE
   parts of `Argument.lean`; its header comment lists the conventions and required theorems.
   Workflow:
   - write `Vocab` (atoms only, each with its operational meaning), `Field` (one premise per
     argument-free constructor, tagged), `prov`, `prem` (one claim per arm, built only from `Vocab`
     atoms and connectives), `Conclusion` (with the paper's verbatim conclusion); encode each
     `[stated]` premise no stronger than its quote;
   - prove `final` with commented `have` steps (paper location per step);
   - prove `final_nontrivial`, `consistent`, `alone_insufficient`;
   - for each premise, try a countermodel (`_needed`); if none exists, prove `_redundant` and
     report the premise as redundant (or the encoding as too coarse);
   - prove `stated_sufficient` or `stated_insufficient` (does what the paper writes suffice?) and
     `explicit_sufficient` or `explicit_insufficient` (does it suffice once standard `[implied]`
     knowledge is added?). `explicit_insufficient` means a real gap - the central finding;
   - tags: `GAP` exactly for `[reconstructed]`; an unstated textbook step is `MOD`/`LIT` `[implied]`
     with its source; a number from the paper that `run.py` does not recompute is `OBS`/`STAT`;
   - countermodels are usually one line: a concrete `Vocab` plus
     `by intro f hf; cases f <;> simp_all [prem]` for `_needed`, and `simp_all [prov, prem]` for
     `stated_*` / `explicit_*` (an unused simp argument fails `--wfail`);
   - a fact from literature published after the paper is `GAP [reconstructed]` (with its bibcode),
     not `[implied]`: the paper could not rely on it;
   - check: `python -m pytest tests/test_lean_arguments.py` (temp copy, `lake build --wfail`,
     pinned statements, axiom audit, tags, NUM bindings). Do not build inside the project.
4. **Report what Lean found** (article section 2.N): `explicit_*` and the GAPs that close the
   difference; `stated_*` and the `[implied]` background the paper relies on; each GAP (why it matters, weaker versions considered);
   redundant premises (a premise whose atoms appear nowhere else is always redundant: an artefact
   of the encoding, not a finding); rival explanations the paper leaves open; consistency (and whether it is a
   strong check here). Rank by how much the conclusion depends on each. State the limit: Lean
   checks the logical structure under our encoding, not the physics inside each premise, and with
   uninterpreted atoms "needed" means "used by this encoding".
5. Paste the key excerpts (`Field` with tags, `prem`, `final`, the `explicit_*` and `stated_*`
   theorems, and each GAP countermodel) and link the full file. The article's premise tables must match the tags.

## 3. Wiki article, part 3 - what this repo can test or explore (first version)

For each stage and rival explanation: can astrolab test or explore it, how, with which data (size estimate,
AGENTS.md section 1), the decision criterion (what result confirms or challenges the paper), and
status `testable now`, `testable after <capability or data release>`, `explorable (not decisive)`
(e.g. sensitivity to a model assumption via `PARAMS`; these feed README section 8), or
`out of scope` (reason).
Explorable rows have no decision criterion ("exploration only") and are not copied into the
README criteria. This table is the source of the pre-registration and is kept: later only its Result column and
the text after it are added to.

Then: optional sections (glossary, open questions, related papers) and the changelog with its
first entry. The Chinese half mirrors the English half.

## 4. Study: pre-register, implement, visualise

- README sections 1-4 BEFORE `run.py`, derived from part 3 (criteria copied, not re-invented).
- `run.py`: data via `ctx.tap / ctx.http`; knobs in the `PARAMS` dict, saved with the results and
  read inside `main()` (no module-level constants derived from them); values bound by `NUM`
  premises saved under stable keys.
- `test_conclusions.py`: assert the reproduced numbers.
- `web/index.html`: designed for this question (`i18n.js` required). Show the argument stages,
  which ones the repo checked, and the data behind them.

## 5. Make the study explorable via chat

Fill README section 8 from the template: the `PARAMS` knobs (meaning, safe range, cache-only or
new data), example questions, results keys. An agent answering a "what if" question:

- `python -m astrolab explore <id> --tag <topic> --set KEY=VALUE` reruns `run.py` with the
  override in memory; outputs and provenance land in `studies/<id>/explore/<date>-<topic>/`;
- for analyses `run.py` does not cover, write `studies/<id>/explore/<name>.py` with
  `def main(ctx)` (like `run.py`) and run `python -m astrolab explore <id> --tag <topic> --script explore/<name>.py`;
- estimate the data size before any knob or script that needs new data (AGENTS.md section 1);
- report the answer in chat; if it changes what we know, record it on a branch: `log.md` entry,
  wiki changelog and affected sections, and commit the script if useful.

## 6. Feed back into the wiki and keep it in sync

- Extend part 3: fill the Result column and add "what we found" with numbers and links to the
  results files. The interactive page runs locally (`python -m astrolab serve`); add a static
  figure if wiki readers need to see it.
- If results change the analysis (a `NUM` binding fails, a `GAP` turns out to matter), update
  part 2 and `Argument.lean` too.
- Every later change to the study: wiki changelog entry and updated sections in the same PR.
- The PR that first adds the article also links it from `docs/wiki/Home.md` under "Paper studies"
  in both languages, the Chinese link with the `#中文` anchor (remove "None yet." / "暂无。").
- Publishing, after the PR merges (outside Dropbox, e.g. in the scratchpad):
  `git clone https://github.com/sudoghut/astrolab.wiki.git`, copy `docs/wiki/*.md` from an
  up-to-date `main` over the clone, review `git diff`, commit, push. The wiki repo is never
  edited directly.

## 7. Close

Referee (`referee` skill; for paper studies also give the referee the quote / kind / Lean-body
table printed by the Lean test and ask whether each `[stated]` body is no stronger than its quote
and each `GAP` is honestly labelled), the AGENTS.md section 5 checklist (includes the wiki sync and the Lean
check), then move the TODO item to `DONE.md`.
