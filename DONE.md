# DONE · 完成日志（done log）

从 [TODO.md](TODO.md) 移出的已完成（`[x]`）与已放弃（`[-]`）条目。按月分组（`## YYYY-MM`），月份与条目都按时间倒序，新条目加在当月小节最上面。规则见 `AGENTS.md` 第二条"待办清单"。

条目格式：

- 完成：`- [x] **T-NNN** 标题 · 完成 YYYY-MM-DD · PR #N · 计划 […](design/…) — 一句话结果`（先开 PR，拿到编号后补进条目再合并；`计划` 只在有 design 计划时写）
- 放弃：`- [-] **T-NNN** 标题 · 放弃 YYYY-MM-DD · 计划 […](design/…) — 放弃原因`（`计划` 同样只在有 design 计划时写）
- 标题中不要出现 ` · ` 或 ` — `；`python -m pytest` 会检查格式。

本机制建立（2026-11-14）之前完成的工作见 `git log` 与 `design/` 各计划的执行记录，不补登。

## 2026-11

- [x] **T-010** 补做：按论文立项流程为 M4 补写 Wiki 文章与 Lean 论证拆解 · 完成 2026-11-14 · PR #9 · 计划 [009](design/009-plan_m04-retrofit-wiki-article-and-lean-argument.md) — 双语 Wiki 文章 `Study-001-gaia-dormant-black-holes`（第三部分为事后补写）与 Lean 论证（`argument/`）：论文明说的前提不足（`stated_insufficient`），加上标准知识仍有缺口（`explicit_insufficient`：BH3 论文没有排除三个以上致密天体，`gap_few3`）；BH1 质量的三条路径使 8 个前提多余；经独立审稿修订（按系统设定质量阈值、BH3 的白矮星一步）
- [x] **T-011** M4：DR4 前的准备，把研究改成按数据发布参数化并预注册 DR4 判据 · 完成 2026-11-14 · PR #7 · 计划 [008](design/008-plan_m04-release-parameterisation-and-dr4-pre-registration.md) — `run.py` 按 `PARAMS`/`RELEASES` 参数化，README 中注明日期的 DR4 附录预注册了全部 DR4 判据并由代码计算；DR3 在 11-25 前重跑（数值不变，BH2 蒙特卡罗中位数差 0.004 M☉ 已说明）；网页支持 DR4/DR3 切换；运行手册按信息隔离重写
- [x] **T-003** 技能：DR4 发布日运行手册（run-book） · 完成 2026-11-14 · PR #6 — 新增技能 `gaia-dr4-release-day`（预检表列出研究中所有假定 DR3 的位置、确认模式与解类型、先计数、源编号核对、失败回退）与查询辅助脚本 `dr4_query.py` 及不联网测试；代码层面的发布参数化登记为 T-011
- [x] **T-009** 论文立项流程：Wiki 双语文章、Lean 论证检查与对话探索 · 完成 2026-11-14 · PR #5 · 计划 [007](design/007-plan_paper-to-study-workflow-wiki-article-lean-argument-and-chat-exploration.md) — 新增 `paper-study` 技能与文章模板、`AGENTS.md` 规则、Lean 论证模板与机器检查（`tests/test_lean_arguments.py`）、`python -m astrolab explore` 命令
- [x] **T-001** 建立待办清单与完成日志机制 · 完成 2026-11-14 · PR #4 · 计划 [006](design/006-plan_todo-list-and-done-log-mechanism.md) — 新增 `TODO.md`、`DONE.md`、`AGENTS.md` 规则与格式检查测试 `tests/test_todo.py`
