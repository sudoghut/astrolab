# {{TITLE}}

> Write sections 1–4 BEFORE writing run.py (pre-registration). Edit them later only
> with a dated note explaining the change.

## 1. Question

TODO: what exactly are we asking?

## 2. Hypothesis and decision criteria

TODO: what result would support / refute the hypothesis? Quantitative thresholds.

## 3. Data (with size estimate)

| Input | Source (service / URL) | Selection | Est. rows / size |
|---|---|---|---|
| TODO | | | |

All inputs must be MB-scale. Push filtering and aggregation to the server.

## 4. Method

TODO: steps, model, priors, systematics to check.

## 5. Results

Filled after running. Link to `web/index.html` and key numbers in `results/`.

## 6. Referee notes

Independent critique: selection effects, systematics, alternative explanations.

## 7. Open questions

## 8. Exploring via chat

How a coding agent answers "what if" questions about this study without touching `results/`
(rules: AGENTS.md section 2).

| Knob (`PARAMS`) | Meaning | Safe range | Cache only, or new data (size)? |
|---|---|---|---|
| TODO | | | |

- Rerun with an override: `python -m astrolab explore {{ID}} --tag <topic> --set KEY=VALUE`
  (outputs in `explore/<date>-<topic>/`, not committed; about N s from cache).
- Analyses `run.py` does not cover: a script `explore/<name>.py` with `def main(ctx)`, run with
  `python -m astrolab explore {{ID}} --tag <topic> --script explore/<name>.py`.
- Results files and keys: TODO (`results/<file>.json`: key - meaning).
- Example questions: TODO (question -> knob or script an agent would use).
- Findings that change what we know go into `log.md` (and, for a paper study, the wiki article)
  on a branch.

