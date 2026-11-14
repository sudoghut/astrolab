# DONE · 完成日志（done log）

从 [TODO.md](TODO.md) 移出的已完成（`[x]`）与已放弃（`[-]`）条目。按月分组（`## YYYY-MM`），月份与条目都按时间倒序，新条目加在当月小节最上面。规则见 `AGENTS.md` 第二条"待办清单"。

条目格式：

- 完成：`- [x] **T-NNN** 标题 · 完成 YYYY-MM-DD · PR #N · 计划 […](design/…) — 一句话结果`（先开 PR，拿到编号后补进条目再合并；`计划` 只在有 design 计划时写）
- 放弃：`- [-] **T-NNN** 标题 · 放弃 YYYY-MM-DD · 计划 […](design/…) — 放弃原因`（`计划` 同样只在有 design 计划时写）
- 标题中不要出现 ` · ` 或 ` — `；`python -m pytest` 会检查格式。

本机制建立（2026-11-14）之前完成的工作见 `git log` 与 `design/` 各计划的执行记录，不补登。

## 2026-11

- [x] **T-009** 论文立项流程：Wiki 双语文章、Lean 论证检查与对话探索 · 完成 2026-11-14 · PR #5 · 计划 [007](design/007-plan_paper-to-study-workflow-wiki-article-lean-argument-and-chat-exploration.md) — 新增 `paper-study` 技能与文章模板、`AGENTS.md` 规则、Lean 论证模板与机器检查（`tests/test_lean_arguments.py`）、`python -m astrolab explore` 命令
- [x] **T-001** 建立待办清单与完成日志机制 · 完成 2026-11-14 · PR #4 · 计划 [006](design/006-plan_todo-list-and-done-log-mechanism.md) — 新增 `TODO.md`、`DONE.md`、`AGENTS.md` 规则与格式检查测试 `tests/test_todo.py`
