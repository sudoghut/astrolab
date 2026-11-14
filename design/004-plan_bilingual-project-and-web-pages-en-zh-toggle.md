# 004 · 工作计划：项目双语化，网页加英中切换按钮

状态：执行中
创建：2026-11-14

## 1. 目标

把"项目保持中英双语"写成规则，并让所有网页（Atlas 总览页、各研究页面、研究模板）都有英文/中文切换按钮，默认英文。

## 2. 规则（写入 `AGENTS.md` 第二条）

- **对外文档双语**：`README.md` 这类面向读者的说明保持中英双语，两种语言内容对应。
- **网页双语**：每个网页（`atlas/web/`、`studies/*/web/`）都要有英/中切换按钮，默认英文；语言选择在页面之间保持。
- **结构化文本双语**：结论条目（claims）和 `study.yaml` 的标题与陈述可加 `*_zh` 字段（`title_zh`、`statement_zh`、`question_zh`），网页在中文模式下优先显示，缺失时回退英文。
- **不翻译的内容**：天体名称、星表编号、数值、单位、文献引用、代码与命令保持原样。
- **不变的约定**：设计文献与研究日志仍用中文（术语括注英文），代码与注释仍用英文。

## 3. 实现方案

共享机制，避免每个页面各写一套：

- `atlas/web/i18n.js`：
  - 语言状态：`?lang=zh|en` 优先，其次本地存储（localStorage，读写包在 try/catch 中），默认 `en`。
  - 在页面右上角插入切换按钮；切换时设置 `<html data-lang>` 与 `lang` 属性，更新 `<title>`，并通知页面注册的回调（用于 Plotly 图表标题等无法用 CSS 切换的文本）。
  - 提供 `L(en, zh)`：生成两种语言的 `<span>`，由 CSS 显示其中一种；提供 `t(en, zh)`：按当前语言返回纯文本（图表用）；提供 `pick(obj, field)`：取 `field_zh`，缺失回退 `field`。
- `atlas/web/base.css`：`[data-lang="en"] .zh`、`[data-lang="zh"] .en` 隐藏规则，以及按钮样式。
- 静态文字用 `<span class="en">…</span><span class="zh">…</span>` 成对书写；动态生成的文字用 `L()`。这样切换语言不需要重绘，表格筛选等交互状态不会丢失。
- `astrolab/claims.py`：在文档字符串中登记可选 `*_zh` 字段；`atlas_data()` 透传研究的 `title_zh`、`question_zh`。
- 测试：`tests/test_core.py` 新增一项，检查每个 `web/index.html` 都引用了 `i18n.js`，让规则可被自动检查。

## 4. 步骤

分三个环节（stage），每个环节结束都做双闸审查（dual-gate review，见 `.claude/skills/dual-gate-review/SKILL.md`）：先由审查子智能体（review subagent）反复审查到没有严重问题，再由 Codex 命令行反复审查到没有严重问题，才进入下一环节。

1. **规则与文档**：本计划、`design/README.md` 索引、`AGENTS.md` 双语规则、双闸审查技能。
2. **双语机制与数据**：`atlas/web/i18n.js`、`base.css` 样式；`claims.py` 透传与校验中文字段；10 条结论条目与 2 个研究补中文字段，模板 `study.yaml` 加中文字段；新增测试。
3. **网页改造**：Atlas 页面、研究 000 与 001 页面、研究模板；重新生成 `atlas.json`；用无头浏览器（headless browser）分别检查英文与中文两种模式。

全部通过后提交、推送、合并。

## 5. 验收标准

- 所有页面默认英文；点击按钮切换到中文，刷新或跳转到其他页面后保持中文。
- 中文模式下，页面说明、表头、判据、图表坐标轴与标题都显示中文；数据值不变。
- 切换语言不重置候选表的筛选状态。
- `python -m pytest` 全部通过，`python -m astrolab claims check` 无错误。

## 6. 执行记录

- 2026-11-14：计划创建，分支 `feat/bilingual-web-pages`。
