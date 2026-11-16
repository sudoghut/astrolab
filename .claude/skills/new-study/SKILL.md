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
- Verify every number you will compare against (roadmap [S]/[U] items to [V]) by reading the
  source read-only; record what was verified where.
- Scaffold: `python -m astrolab new <slug> "<title>" --level Lx` (picks the next number). Then:
  - `study.yaml`: `title_zh`, `question_zh` (tests reject `TODO`), `claims:`, `milestone:`;
    leave `papers: []` and `wiki: null`; fill or delete the `footprint` block;
  - delete `argument/` (only paper studies keep it);
  - the Chinese title in `web/index.html` (both `data-title-zh` and the `<h1>` span).

## 1. Pre-register (README sections 1-4, before any `run.py`)

- **Question**: one precise question; the same sentence as `study.yaml` `question`.
- **Criteria**: for each result a quantitative rule fixed now (threshold, interval, or a
  calibration that fixes the threshold, e.g. from mocks), and what the study reports when the
  rule cannot be applied ("cannot determine"). Name the primary sample and the sensitivity checks
  in advance.
- **Data**: one row per input with service, selection, estimated rows and size. Count first
  (`fetch.tap_count`, `server-side-query` skill); compute aggregates and derived columns on the
  server; prefer compressed products. Stop and ask if anything is over 50 MB per download or
  200 MB per run (section 1.6).
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
  `atlas/web/i18n.js` (English default, en/zh switch). Check it with `python -m astrolab serve`.
- Review each stage with the `dual-gate-review` skill before moving on.

## 3. Make it explorable via chat (README section 8)

Table of `PARAMS` knobs (meaning, safe range, cache only or new data with size), the `explore`
commands for `--set` and `--script explore/<name>.py`, the results files and keys, and two or
three example questions. Exploration never edits `results/`.

## 4. Write up and close

- README section 5 (results with numbers and links), section 7 (open questions, including any
  post-hoc ideas, labelled as such); `log.md` entry in Chinese with English terms in parentheses.
- Linked claims in `atlas/claims/`: `ours`, `status`, and the Chinese fields; `study.yaml`
  `status`; `python -m astrolab claims check`; regenerate `atlas/web/data/atlas.json` if the
  Atlas changed (`python -m astrolab atlas`).
- `referee` skill; triage every point into README section 6 and `log.md`.
- `python -m pytest` passes; `STATUS.md` updated; move the TODO item to `DONE.md` with the PR
  number; close-out review; mark the PR ready and rebase-merge.
