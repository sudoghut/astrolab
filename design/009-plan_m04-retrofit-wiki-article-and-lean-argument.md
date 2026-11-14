# 009 · 工作计划：为 M4 补写 Wiki 文章与 Lean 论证拆解（论文立项流程的补做）

状态：进行中
创建：2026-11-14
待办：T-010（`TODO.md`）

## 1. 目标

M4 研究（`studies/001-m04-gaia-dormant-black-holes/`）早于论文立项流程（计划 007）完成，所以按 `paper-study` 技能"为已实现的研究补写"的要求补齐：

- 双语 Wiki 文章 `docs/wiki/Study-001-gaia-dormant-black-holes.md`：科普详解、论证逻辑与 Lean 拆解、本项目可检验或探索的环节（标明事后补写）；
- Lean 论证 `argument/Argument.lean`，通过 `tests/test_lean_arguments.py`（实际运行，不跳过）；
- `study.yaml` 的 `papers`、`wiki` 字段；`README.md` 第 8 节"对话探索（exploring via chat）"；`docs/wiki/Home.md` 中英两处链接；
- 独立审稿（referee）：附上 Lean 测试生成的"引文—类型—内容"对照表。

论文：arXiv:2209.06833（BH1）、2302.07880（BH2）、2404.10486（BH3）、2405.00089（中子星候选）。2026-11-14 用网页读取（只读）阅读 arXiv HTML 全文并摘录引文：BH1 v3、BH2 v2、BH3 v2、中子星候选 v2。

不做：不改动研究的预注册与结果（论证中的 `NUM` 前提绑定已有的 DR3 结果键）。

## 2. 设计要点

- 论证覆盖 BH1、BH2、BH3 三个系统，每个系统四个环节：视向速度验证轨道 → 质量至少 5 M☉ → 质量不在发光恒星中 → 至多两个天体加中子星最大质量 → 含有黑洞。中子星候选论文提供研究的对照样本，不在论证链条中，文章中单独说明。
- 结论编码为"每个伴星至少含有一个黑洞"，弱于论文"很可能是单个黑洞"的说法；文章写明这一点。
- `NUM`：`num_astro1` 绑定 `results/summary.json:post_hoc.R1b_bh1_vs_dr3_only_paper.m2_ours >= 5.0`。DR4 运行之后需要改为 `results/dr3/`，已写入 T-002 的备注。
- 工具链：本机安装 elan 与模板指定的 Lean 4.35.0 已获用户同意（2026-11-14）；实际约 3.3 GB（比事先估计的 300–500 MB 大得多，已告知用户），位于用户目录，不在 Dropbox 中。

## 3. 环节（每个环节过双闸审查，dual-gate review）

1. **论证与文章**：`Argument.lean`、Wiki 文章、`study.yaml`、`Home.md`、README 第 8 节。
2. **独立审稿与收尾**：审稿意见的处理记入 README 第 6 节与 `log.md`；Wiki 更新"研究进展"。合并后按技能第 6 步推送 Wiki 仓库。

## 4. 执行记录

- 2026-11-14：建分支 `feat/m4-wiki-lean-retrofit`；四篇论文的全文读取与引文摘录由网页读取子智能体完成（只读）；`Argument.lean` 通过构建与审计（`explicit_sufficient`、`stated_insufficient`，BH1 的质量有两条独立路径，相应 4 个前提为多余）。
