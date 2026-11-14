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
example: rules/docs -> shared mechanism + data -> pages). Write the stages into the work
plan (`design/NNN-plan_*.md`) when there is one. Work on a branch (AGENTS.md / user rules).

## 1. Finish one stage

- Make the edits and run the relevant checks yourself (`python -m pytest`, render pages, ...).
- Commit the stage as a WIP commit (squash or keep later as the user prefers). This is
  required: it gives reviewers a clean diff (`git diff <base>..HEAD`).
- Before starting a reviewer, `git status --short` must be empty. If the user has unrelated
  uncommitted work, stop and ask; never stash or discard it yourself.
- Undoing reviewer changes afterwards: restore only the files `git status --short --ignored`
  shows as changed, one by one (`git checkout -- <file>`); delete files the reviewer created
  one by one. Never use `git checkout -- .`, `git reset --hard` or `git clean -fdx`.

## 2. Gate 1 - review subagents (loop)

- Spawn reviewer subagent(s) that must READ THE CODE AND THE DIFF themselves. Give them: the
  goal of the stage, the file list, the diff command, and the acceptance criteria. Do NOT
  give them your verdict or what you hope is fine.
- Ask for findings ranked serious / minor / nit, each with file:line and a concrete failure
  scenario, ending with `SERIOUS ISSUES: <n>`. Forbid editing files and fetching data.
- For larger stages use 2-3 reviewers with different lenses (correctness, behaviour/UX,
  consistency with AGENTS.md) in one message so they run in parallel.
- Afterwards run `git status --short --ignored` and undo anything a reviewer touched (step 1).
- Triage every finding yourself against the code: fix, or reject with a reason. Fix all
  serious ones. Commit the fixes (WIP) and re-run gate 1 on the new diff until it reports
  no serious issues.

## 3. Gate 2 - Codex CLI (loop)

Run Codex non-interactively from the terminal (it is a CLI, not one of our agents), in the
project root, with the PowerShell tool (Windows PowerShell 5.1, i.e. `powershell.exe`; the
template relies on 5.1 behaviour). Do not route it through Bash -> `powershell.exe` with
a `.ps1` file: Windows PowerShell 5.1 reads a BOM-less UTF-8 script in the ANSI code page and
silently corrupts Chinese text in the prompt (if you must, save the `.ps1` as UTF-8 with BOM
and pass `-C <project root>` to codex). Template:

```powershell
$OutputEncoding = [Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)  # keep Chinese intact
# Use the local proxy if it is listening; otherwise connect directly.
$c = New-Object Net.Sockets.TcpClient
try { $c.Connect('127.0.0.1', 7890); $proxy = $true } catch { $proxy = $false } finally { $c.Close() }
if ($proxy) { $env:HTTPS_PROXY = "http://127.0.0.1:7890"; $env:HTTP_PROXY = "http://127.0.0.1:7890" }
else { Remove-Item Env:HTTPS_PROXY, Env:HTTP_PROXY -ErrorAction SilentlyContinue }
Write-Output @'
<review prompt - single-quoted here-string, so $ and backticks are not expanded>
'@ | codex exec --dangerously-bypass-approvals-and-sandbox -o $out *> $log
"exit code: $LASTEXITCODE"
```

`<scratchpad>` is a placeholder: replace it with this session's scratchpad directory (or
another existing temp directory outside the project). Set `$out` first to a NEW file per
stage and round, e.g.
`$out = "<scratchpad>/codex-stage2-round1.md"; $log = "<scratchpad>/codex-stage2-round1.log"; Remove-Item $out -ErrorAction SilentlyContinue`.
(`'@ | codex ...` on the closing line is valid in PowerShell 5.1: the terminator must start at
column 0, and a pipeline may follow it.)

- `codex exec` = non-interactive; `--dangerously-bypass-approvals-and-sandbox` = no approval
  prompts. Pipe the prompt (`Write-Output ... |`) so Codex does not wait on stdin. Use a
  single-quoted here-string (closing `'@` at column 0): a double-quoted string would expand
  `$name` and turn backtick sequences such as `` `n `` into control characters.
- Proxy: the 127.0.0.1:7890 proxy is this machine's setup. When it is listening, the
  variables are required, because Node.js (which Codex runs on) ignores the Windows registry
  proxy settings. When nothing listens on that port, connect directly (no proxy variables).
  If Codex fails with a network error either way, retry once in the other mode before
  reporting the failure to the user; note which mode worked in the work-plan log.
- `-o` writes Codex's final message to a file; read the verdict from there, and only if the
  exit code is 0 and the file was written by this run (fresh name, deleted beforehand), so a
  failed run can never reuse an earlier `SERIOUS ISSUES: 0`. PowerShell 5.1 prefixes piped
  stdin with a UTF-8 BOM; Chinese still arrives intact and Codex ignores it. Start the PowerShell
  tool call with its `run_in_background: true` parameter (a review can exceed the tool's
  10-minute foreground limit); the harness notifies you when it exits. The `*> $log`
  redirect keeps codex's console output out of your context; read the log only on failure.
- The prompt must say: review only; DO NOT modify files; DO NOT run network or data-fetching
  commands (`python -m astrolab run`, downloads; AGENTS.md section 1); the stage goal; the
  diff command and file list; findings ranked serious/minor with file:line and a failure
  scenario; end with `SERIOUS ISSUES: <n>`.
- Afterwards run `git status --short --ignored`; revert anything Codex touched and remove
  files it created (as in step 1).
- Triage as in gate 1, fix serious issues (WIP commit), and re-run Codex until it reports
  none. If a fix is non-trivial, pass the changed code back through gate 1 as well.

## 4. Advance

Record in the work plan's execution log: stage name, rounds of each gate, serious issues
found and how they were fixed or why rejected. Then start the next stage at step 1.

## 5. After the last stage

A final full-diff run of both gates is optional for small changes but required if stages
interacted. Then commit / push / PR / merge as the user asked.

## Checklist: what counts as serious

Wrong results or broken behaviour, data loss, security problems, a violation of an AGENTS.md
rule (especially section 1), a regression in an existing feature, or a failing test. Style,
naming and wording preferences are minor unless they would mislead a reader or an agent.
