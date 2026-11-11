# 002 · 路线图：2022–2026 代表性结果的文献核实

- 类型：工作计划（work plan）
- 状态：完成，产出见根目录 [`ROADMAP.md`](../ROADMAP.md)
- 日期：2026-11-11
- 依据：[000 设计原则](000-principles_agent-driven-laptop-astronomy-research.md) 第 2 节

## 目标

讨论阶段凭记忆列出过一份路线图（roadmap）草案。本计划把它逐条核实，变成可以施工的 `ROADMAP.md`，要求做到：
- 出处准确，关键数值准确。
- 数据可得，且为 MB 级。
- 笔记本电脑可以复现。
- 补充可能遗漏的 2025–2026 年重要结果。

## 方法

派出两个并行的子智能体（subagent），通过网络核实文献，来源包括 arXiv、NASA 天体物理数据系统（ADS, Astrophysics Data System）、期刊页面和数据发布页面。

| 组别 | 负责的里程碑 | 领域 |
|---|---|---|
| A 组 | M1、M2、M3、M8、M9 | 宇宙学与高红移（cosmology & high redshift） |
| B 组 | M4、M5、M6、M7、M10 | 银河系、恒星、致密天体与引力波 |

每个里程碑要求输出以下内容：
- 准确引用
- 关键数值
- 数据获取方式与大小
- 笔记本可行性（feasibility）与"巧办法"
- 等级（grade）判断
- 2025–2026 年的后续进展
- 开放问题（open questions）

每项都要标注核实程度：[V] 表示已核实，[S] 表示仅来自搜索摘要，[U] 表示未核实。

## 验收标准

- 每个里程碑至少有一个已核实的原文引用（含 arXiv 号）和一个明确的数据获取地址。
- 数据量超出 MB 级的条目，必须给出压缩或服务器端方案。

## 执行记录

### 2026-11-11

- 两组子智能体完成核实。结果整理进 `ROADMAP.md`，第一条结论条目写入 `atlas/claims/`。

**最重要的发现：Gaia DR4 定于 2026-12-02 发布 [V]。**
- 距今约 3 周。
- 因此把 M4（Gaia 休眠黑洞）排到第一位，目标是在 DR4 发布前把非单星轨道（NSS, non-single-star）分析管线（pipeline）在 DR3 上做好。

**对草案的修正**

| 原草案 | 修正后 |
|---|---|
| BH3 在 DR3 中有轨道解 | 不在 DR3 中 |
| 可以直接下载宽双星（wide binary）星表 | 星表有 1.8 GB，改为在服务器端重建样本 |
| GWTC-4.0 数据可以全部下载 | 群体分析数据有 35 GB，只用小文件 |
| MoM-z14 发表于 2025 年 | 发表于 2026 年的 OJAp |
| ACT DR6 透镜 S8 = 0.840 | 无此出处，改为 0.831 ± 0.023 |

**结论等级的变化**
- DESI 的演化暗能量（evolving dark energy）迹象在 2026 年趋弱：DES-Dovekie 重新校准、Lyα 全形状（full-shape）分析都降低了其显著性。
- 宽双星之争趋向牛顿引力（Cookson et al. 2026）。

**新增并入相应里程碑的结果**
- ACT DR6 / SPT-3G D1 作为 CMB 先验（prior）
- TDCOSMO 2025 时间延迟透镜（time-delay lensing）
- eROSITA 星系团计数（cluster counts）
- Gaia 中子星（neutron star）候选体

**新增候选里程碑**
- M11：Radcliffe 波（Radcliffe Wave）
- M12：Gaia XP 金属丰度（metallicity）

**遗留**
- 仍有若干 [S] 和 [U] 项，包括部分卷页号、数据下载地址，以及 IPTA DR3 是否已发表。
- 规则：每个里程碑动手之前，先把它涉及的条目核实到 [V]。
