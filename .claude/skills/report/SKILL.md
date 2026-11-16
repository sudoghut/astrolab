---
name: report
description: Write a report on one study or on the state of the project for a human reader - what was asked, what the pre-registered criteria said, what the results are (numbers traced to results files and provenance), negative and undetermined outcomes, amendments and post-hoc items, referee caveats and open questions - without new analysis. Use when the user asks for a report, summary, write-up or briefing of a study, a milestone or the project.
---

# Report (study or project)

Rules live in `AGENTS.md` (pre-registration, bilingual text and exploration in section 2;
completion criteria in section 5); principles in `design/000-principles_*` (provenance,
negative results recorded). This skill is the order of work and the checklist. A report adds no
analysis: a question the results do not answer goes to chat exploration or a new TODO item.

## 1. Scope and freshness

- Agree the scope: one study, a milestone, or the whole project; the reader (the user, a
  colleague, the wiki); the language (chat follows the user; a document others read follows the
  bilingual rules).
- Study: check the results are current. `results/run_info.json` `finished_at` is later than the
  last commit to `run.py` and its helpers (`git log -1 --format=%cI -- <files>`); otherwise say so
  in the report, or rerun only if the user asks (a formal run can take hours).
- `python -m pytest studies/<id>` (conclusion tests; for a paper study also
  `tests/test_lean_arguments.py`) and `python -m astrolab claims check`; report failures, do not
  hide them.
- Project: `python -m astrolab status`, `STATUS.md`, `TODO.md`/`DONE.md`,
  `python -m astrolab claims list`.

## 2. Gather (sources, in this order)

- `README.md` sections 1-4 (question, criteria as frozen, with dated amendments), 5 (results),
  6 (referee notes), 7 (open questions); `study.yaml` (status, claims).
- `results/*.json`: every number in the report comes from here, with its uncertainty and the
  file and key it came from (e.g. `r2.json: primary.mu`). Do not round away the uncertainty or
  quote a number that is only in prose.
- `results/provenance.json` (inputs: request, data version or label, `retrieved_at`, `sha256`,
  bytes) and `run_info.json` (when, how long).
- Linked claims in `atlas/claims/`: `reproduction.quantities` (paper versus ours), `grade`.
- `log.md` for dead ends and decisions; the wiki article (part 3) for paper studies.

## 3. Write

For a study, in this order:

1. Question (one sentence) and the data (inputs, sizes, data release).
2. Per criterion: the rule as pre-registered, the number, the verdict as the code produced it
   ("reproduced", "not reproduced", "cannot determine" are all results), and the sensitivity
   checks named in advance.
3. Paper versus ours, where a claim lists quantities.
4. Everything decided after seeing data: dated amendments and post-hoc analyses, labelled as such.
5. Referee points and accepted limitations; what would change the conclusion.
6. Open questions; how to reproduce (`python -m astrolab run <id>`) and explore (README section 8).

For a project report: one line per study (status, headline verdict, date), blocked items with the
reason, upcoming dates, and the TODO items next in line.

Checks before handing over: every number traced to a results key; no verdict stronger than its
rule; negative and undetermined outcomes included; post-hoc items labelled; no data or paper files
written to the project.

## 4. Deliver

- Default: in chat. A report meant to be kept goes where it will be maintained: the study README
  or the wiki article (on a branch, through a PR), not a new file elsewhere in the project.
- If the user wants a standalone document, write it outside the project directory (or publish it
  with the agent's own tools) and say where it is.
