---
name: referee
description: Run an independent referee review of a study in studies/ - spawn a subagent that sees only the code, pre-registration and results (not our conclusions) and hunts for systematics, selection effects, bugs and literature that contradicts or explains the results. Use before marking any study reproduced/concluded, or when a result looks surprising.
---

# Independent referee review

Goal: an adversarial read that is NOT anchored on our interpretation (AGENTS.md, section 5).

## Steps

1. Identify the study folder `studies/<id>/`. Make sure `results/` is current (`python -m astrolab run <id>`).
2. Spawn ONE subagent (general-purpose; it needs web search for literature) with a prompt that:
   - points it to: `README.md` sections 1-4 (pre-registration), `run.py` and helper modules, the
     relevant `astrolab/*.py` modules, `results/*.json`, `data/` inputs;
   - does NOT include our summary of what the results mean, nor which answer we hope for;
   - asks for: (a) code/physics bugs with file:line, (b) systematics and selection effects that
     could produce or hide the result, (c) whether each pre-registered criterion was evaluated
     honestly (no moved goalposts), (d) literature that already explains specific results or
     candidates (cite arXiv IDs; mark unverified), (e) the single most important additional test;
   - forbids downloading data files (AGENTS.md section 1) and forbids editing files;
   - asks for a ranked list, most serious first, each with a concrete failure scenario.
3. Triage every point yourself: verify against the code/results; classify as fixed / accepted
   limitation / rejected (with reason). Do not accept or reject wholesale.
4. Record in `README.md` section 6 "Referee notes" (English) and summarise in `log.md`
   (Chinese, terms with English in parentheses). Post-hoc changes to criteria or flags must be
   labelled post-hoc with date and reason.
