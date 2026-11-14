---
name: dual-gate-review
description: Dual-gate code review - after each small stage of a code change, first loop review subagents until no serious issues remain, then loop the Codex CLI (a separate model, run as a terminal command) until no serious issues remain, and only then move to the next stage. Use when the user asks for "双闸 review" / dual-gate review, or for any multi-stage change they want independently reviewed before commit.
---

# Dual-gate review (双闸 review)

Two independent gates per stage. Gate 1 is our own review subagents; gate 2 is Codex, a
different model run from the terminal, so its blind spots differ from ours. A stage passes
only when BOTH gates report no serious issues. Then, and only then, start the next stage.

## 0. Split the work into small stages

Before coding, cut the change into stages that can each be reviewed on their own (for
example: rules/docs + shared mechanism -> pages -> content/data). Write the stages into the
work plan (`design/NNN-plan_*.md`) when there is one. Work on a branch, never on `main`.

## 1. Finish one stage

Make the edits, run the relevant checks yourself (`python -m pytest`, render pages, etc.).
Note the exact file list and the diff range for this stage (`git diff` against the stage's
starting point; stage files with `git add` or commit a WIP so later stages have a clean base).

## 2. Gate 1 - review subagents (loop)

- Spawn reviewer subagent(s) that must READ THE CODE AND THE DIFF themselves. Give them: the
  goal of the stage, the file list, how to see the diff (`git diff <base>`), and the
  acceptance criteria. Do NOT give them your verdict or what you hope is fine.
- Ask for findings ranked by severity (serious / minor / nit), each with file:line and a
  concrete failure scenario. Forbid editing files.
- For larger stages use 2-3 reviewers with different lenses (correctness, UX/behaviour,
  consistency with AGENTS.md rules) in one message so they run in parallel.
- Triage every finding yourself against the code: fix / reject with reason. Fix serious ones.
- Re-run gate 1 on the updated diff until no serious issues remain.

## 3. Gate 2 - Codex CLI (loop)

Run Codex non-interactively from the terminal (it is a CLI, not one of our agents). On this
Windows machine, from the PowerShell tool (call `powershell.exe` when shelling out):

```powershell
$env:HTTPS_PROXY = "http://127.0.0.1:7890"; $env:HTTP_PROXY = "http://127.0.0.1:7890"
Write-Output "<review prompt>" | codex exec --dangerously-bypass-approvals-and-sandbox
```

- `codex exec` = non-interactive; `--dangerously-bypass-approvals-and-sandbox` = no approval
  prompts. Pipe the prompt with `Write-Output "..." |` so Codex does not wait on stdin.
- The proxy variables are required: Node.js (which Codex runs on) ignores the Windows
  registry proxy settings.
- The prompt states: review only, DO NOT modify any files; the stage goal; the diff command
  (`git diff <base>`) and file list; report findings ranked serious/minor with file:line and
  a failure scenario; end with an explicit line `SERIOUS ISSUES: <n>`.
- Run it in the project root; allow a long timeout (10 min). After it finishes, check
  `git status` to confirm Codex changed nothing; revert anything it touched.
- Triage as in gate 1, fix serious issues, and re-run Codex until it reports none. If a fix
  is non-trivial, pass the changed code back through gate 1 as well.

## 4. Advance

Record in the work plan's execution log: stage name, rounds of each gate, serious issues
found and how they were fixed or why rejected. Then start the next stage at step 1.

## 5. After the last stage

Final full-diff run of both gates is optional for small changes but required if stages
interacted. Then commit / push / PR / merge as the user asked.

## What counts as serious

Wrong results or broken behaviour, data loss, security problems, a violation of an AGENTS.md
rule (especially section 1 data limits), a regression in an existing feature, or a failing
test. Style, naming and wording preferences are minor unless they mislead readers.
