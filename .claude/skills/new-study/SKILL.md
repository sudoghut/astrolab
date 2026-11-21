---
name: new-study
description: Start a new astrolab study that is not driven by a paper's argument (a census, a reproduction of a catalogue number, a pipeline check) - register it, scaffold the folder, pre-register question, criteria, data and method with a size estimate, then implement run.py, conclusion tests, web page and chat exploration, and close it out. Use when the user asks to open, create or set up a new study; for a study built around one or more papers use the paper-study skill instead.
---

# New study (non-paper)

Rules live in `AGENTS.md` (data limits in section 1; to-do list, branches, bilingual rules,
pre-registration and exploration in section 2; commands in section 3; folder layout in section 4;
completion criteria in section 5). This skill is the order of work and the checklists.

Paper or not? If the question is "does this paper's argument hold" (its claims, quotes, premises),
use `paper-study`: it adds the wiki article and the Lean argument before the pre-registration.

## 0. Register and set up

- Register one `TODO.md` item (check `gh pr list` and the T-numbers on other branches first) and
  move it to Doing with the branch name. Write a design plan only if the section 2 complexity rule
  says so (several modules, new core-library capability, staged review).
- Branch, push early, open a draft PR.
- Raise the milestone's [S]/[U] roadmap items to [V] before starting, and other items before the
  step that relies on them (`literature-verification` skill).
- Scaffold: `python -m astrolab new <slug> "<title>" --level Lx` (picks the next number). Then:
  - `study.yaml`: `title_zh`, `question_zh` (tests reject `TODO`), `claims:`, `milestone:`;
    leave `papers: []` and `wiki: null`; fill the `footprint` block (required: scale, sky mode, data; `claims check` fails without it; targets with sourced coordinates where the study has named objects, each with a one-line `note`/`note_zh` (or a shared `target_note`/`target_note_zh`) on its role and result, shown on the Atlas sky);
  - delete `argument/` (only paper studies need it; an unchanged template copy is not checked);
  - the Chinese title in `web/index.html` (both `data-title-zh` and the `<h1>` span).

## 1. Pre-register (README sections 1-4, before any `run.py`)

Write `README.md` in English and keep `README.zh.md` (the Chinese companion, from the template) in step:
same section numbers and tables, updated in the same PR (AGENTS.md bilingual rule).

- **Question**: one precise question; the same sentence as `study.yaml` `question`.
- **Criteria**: for each result a quantitative rule fixed now (threshold, interval, or a
  calibration that fixes the threshold, e.g. from mocks), and what the study reports when the
  rule cannot be applied ("cannot determine"). Name the primary sample and the sensitivity checks
  in advance.
- **Data**: one row per input with service, selection, estimated rows and size. Count first
  (`ctx.count` in a study, `fetch.tap_count` in the library; `server-side-query` skill); compute aggregates and derived columns on the
  server; prefer compressed products. If an estimate or a `TooLarge` error exceeds the limits
  (section 1.1), follow section 1.6 in its order; ask the user only at its last step.
- **Method**: model, likelihood, priors, systematics to check, random seeds.
- Commit the pre-registration with its date before writing code. Later edits are dated
  amendments with a reason (state whether results had been seen).

## 2. Implement

- `run.py`: `def main(ctx)`; data only via `ctx.tap / ctx.http`; knobs in `PARAMS`, read inside
  `main()` and passed to helper modules as arguments (no module-level constants from them, no
  `import run` in helpers); save `PARAMS` with the results; each `results/*.json` under 1 MB.
- Smoke-run with a reduced setting through `python -m astrolab explore <id> --tag smoke --set ...`
  (does not touch `results/`; delete the output afterwards), then the formal
  `python -m astrolab run <id>`.
- `test_conclusions.py`: recompute each verdict from the saved numbers by the pre-registered rule,
  rather than hard-coding the outcome; skip cleanly when `results/` is missing.
- `web/index.html`: designed for this question, reading `../results/*.json`; must load
  `atlas/web/i18n.js` (English default, en/zh switch), and keep the template's "On the sky" box
  (`<section id="skylinks" hidden>` and `atlas/web/skylinks.js`; a test checks it). Check it with `python -m astrolab serve`.
- If the plan calls for staged review (section 2 complexity rule), review each stage with the
  `dual-gate-review` skill before moving on.

## 3. Make it explorable via chat (README section 8)

Table of `PARAMS` knobs (meaning, safe range, cache only or new data with size), the `explore`
commands for `--set` and `--script explore/<name>.py`, the results files and keys, and two or
three example questions. Exploration never edits `results/`.

## 4. Write up and close

- README section 5 (results with numbers and links), section 7 (open questions, including any
  post-hoc ideas, labelled as such), languages per the AGENTS.md section 2 bilingual rules; a
  `log.md` entry in Chinese with English terms in
  parentheses, newest entry on top.
- `referee` skill (a subagent that sees only code and results, AGENTS.md section 5) before
  marking anything reproduced or concluded; triage every point into README section 6 and `log.md`.
- Then the status: in each linked claim in `atlas/claims/`, `reproduction.study` (this study's
  id), `reproduction.quantities[].ours` and `reproduction.status` (vocabulary in `astrolab/claims.py`) plus the Chinese fields; the
  study's own `status` in `study.yaml` (a different vocabulary); `python -m astrolab claims check`;
  `python -m astrolab atlas` and commit `atlas/web/data/atlas.json` (`serve` also rewrites it).
- The study's row in the root `README.md` status tables (English "Status" and Chinese "进展") and
  in the `STATUS.md` study table: added in the PR that creates the study, and updated in every later
  PR that changes its results, verdicts or status (AGENTS.md section 2, "总表保持同步").
- After merging, the online site (https://sudoghut.github.io/astrolab/) still shows the old page until
  the Pages workflow runs again (AGENTS.md section 3): ask the user, then `gh workflow run pages.yml --ref main`.
- `python -m pytest` passes; `STATUS.md` updated; move the TODO item to `DONE.md` with the PR
  number; if the plan uses staged review, a final `dual-gate-review` of the whole diff; mark the
  PR ready and rebase-merge.
