# design/ — 项目设计文献

本文件夹存放本项目自身的设计文献：设计原则、工作计划（work plan）、决策记录、复盘。
它是项目的"宪法 + 施工日志"，供人和 coding agent 共同阅读。

## 命名规则

```
NNN-<类型>_<核心内容>.md
```

- `NNN`：三位自然数编号，全局递增（000, 001, 002, ...），表示先后顺序。新文件取当前最大编号 + 1，编号永不复用。
- `<类型>`：`principles`（原则）、`plan`（工作计划）、`decision`（决策记录）、`review`（复盘/评估）。
- `<核心内容>`：用短横线连接的英文短语，必须表达文件的核心内容；禁止只叫 `work-plan`。

示例：`001-plan_environment-bootstrap-core-library-and-study-scaffold.md`

## 工作方式

- **每一个复杂任务都从写 work plan 开始**：先写计划（目标、范围、步骤、验收标准），再动手。
- 计划执行过程中，在计划文件末尾的"执行记录"一节更新进度与偏差；计划不删除，只追加。
- 计划状态写在文件头部：`草案` → `执行中` → `完成` / `搁置` / `被 NNN 取代`。

## 索引

| 编号 | 类型 | 标题 | 状态 |
|---|---|---|---|
| 000 | principles | [项目设计原则：agent 驱动的个人电脑天文学研究](000-principles_agent-driven-laptop-astronomy-research.md) | 生效 |
| 001 | plan | [环境搭建：核心库与研究文件夹骨架](001-plan_environment-bootstrap-core-library-and-study-scaffold.md) | 完成 |
| 002 | plan | [路线图：2022–2026 代表性结果的文献核实](002-plan_roadmap-literature-verification-2022-2026-landmark-results.md) | 完成 |
| 003 | plan | [M4：Gaia 休眠黑洞的 DR3 复现与 DR4 筛选管线](003-plan_m04-gaia-dormant-black-holes-dr3-reproduction-and-dr4-ready-screen.md) | 完成（DR3 部分） |
| 004 | plan | [项目双语化，网页加英中切换按钮](004-plan_bilingual-project-and-web-pages-en-zh-toggle.md) | 执行中 |

## 术语约定

本文件夹和各研究日志（research log）中，任何术语第一次出现时都要在括号中注明英文原文，缩写写出全称，例如：工作计划（work plan）、重子声学振荡（BAO, Baryon Acoustic Oscillations）。
