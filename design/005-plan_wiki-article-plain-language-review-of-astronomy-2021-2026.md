# 005 · 工作计划：GitHub Wiki 双语科普综述《近五年天文学（2021–2026）》

状态：执行中
创建：2026-11-14

## 1. 目标

把对话中写成的科普综述整理成一篇中英双语的 GitHub Wiki 文章，并从 `README.md` 链接过去。文章面向非专业读者，介绍 2021–2026 年天文学的主要进展，重点放在与本项目路线图（roadmap）里程碑（milestone）M1–M10 相关的研究上。

## 2. 范围与约定

- **文章源文件入库**：GitHub Wiki 是一个独立的 git 仓库（`astrolab.wiki.git`），不经过拉取请求（PR, Pull Request）审查。因此文章源文件放在主仓库的 `docs/wiki/`，在分支上审查、合并，再原样推送到 Wiki 仓库。以主仓库中的版本为准。
- **文件**：
  - `docs/wiki/Five-Years-of-Astronomy-2021-2026.md`：正文，先英文后中文，两部分内容对应。
  - `docs/wiki/Home.md`：Wiki 首页，双语，链接到正文。
- **链接**：Wiki 页面里指向仓库文件的链接一律写成绝对网址（`https://github.com/sudoghut/astrolab/blob/main/...`），因为 Wiki 中的相对链接会解析到 Wiki 自身。
- **数字与引用**：数值和文献以 `ROADMAP.md`、`atlas/claims/*.yaml` 中的条目为准；其中只标为 [S] 的数值只用取整后的近似值（如 H0 "约 70"）。路线图里没有的数字，在文末"来源"一节列出原始文献。第 4 节（路线图之外的亮点）只做定性描述，并注明没有经过项目的文献核实流程。
- **双语规则**：天体名称、星表编号、数值、单位、文献引用不翻译；中文部分术语第一次出现时括注英文。
- **数据约束**：本任务不取任何数据，只写文档。审查者可以用网页搜索核对事实，但不下载数据文件。

## 3. 步骤

分两个环节（stage），每个环节结束做双闸审查（dual-gate review，见 `.claude/skills/dual-gate-review/SKILL.md`）。

1. **文章正文**：`docs/wiki/` 下的两个文件。审查重点：事实与数字是否准确、中英两部分是否对应、是否通俗易懂、链接是否有效。
2. **挂接与登记**：`README.md` 中英两部分各加一个链接；本计划与 `design/README.md` 索引。审查重点：链接是否正确、双语是否对应、是否符合 `AGENTS.md`。

完成后提交、推送、合并到 `main`，再把 `docs/wiki/` 推送到 Wiki 仓库。

## 4. 验收标准

- 两个环节都通过双闸审查，没有遗留的严重问题。
- 文章中的数字与 `ROADMAP.md`、结论条目一致；没有无出处的精确数字。
- `README.md` 中的链接指向 Wiki 页面，Wiki 页面能正常打开。
- `python -m pytest` 通过。

## 5. 执行记录

- 2026-11-14：建分支 `docs/wiki-astronomy-2021-2026-review`。发现 Wiki 仓库尚未初始化（`git ls-remote` 返回 not found）：GitHub 要求先在网页上创建第一页，之后才能用 git 推送。
