# 003 · M4：Gaia 休眠黑洞的 DR3 复现，以及为 DR4 准备的筛选管线

- 类型：工作计划（work plan）
- 状态：完成（DR3 部分）；DR4 发布日任务见执行记录末尾
- 日期：2026-11-11
- 依据：[`ROADMAP.md`](../ROADMAP.md) 中的 M4；[000 设计原则](000-principles_agent-driven-laptop-astronomy-research.md)
- 截止：2026-11-25。这一天 Gaia 数据库（archive）下线，12-02 发布 DR4（第四次数据发布，Data Release 4）。

## 目标

1. **复现（reproduce）**：只用 Gaia DR3 的非单星（NSS, non-single-star）天体测量轨道解（astrometric orbital solution），求出 Gaia BH1 和 BH2 的暗伴星（dark companion）质量，并与论文值比较。
2. **筛选（screen）**：在服务器端（server-side）对 DR3 的全部天体测量轨道解计算质量函数（mass function），找出暗伴星候选体（dark-companion candidates），并检验能否找回已知的黑洞和中子星（neutron star）候选体。
3. **为 DR4 准备（DR4-ready）**：把筛选写成以数据发布版本为参数的管线（pipeline），12-02 当天只需改一个参数即可运行。

**不在本计划内**：视向速度（radial velocity）随访数据的联合拟合；BH3 的轨道复现（DR3 中没有它的轨道解，只登记论文值）。

## 物理与方法

**光心轨道半长轴（photocentre semi-major axis）a₀**

由 Thiele–Innes 常数（Thiele–Innes constants）A、B、F、G（单位 mas）计算：

- u = (A² + B² + F² + G²) / 2
- v = AG − BF
- a₀ = √(u + √(u² − v²))

**天体测量质量函数（astrometric mass function）**

- 暗伴星不发光，所以光心轨道就是发光星（luminous star）的轨道：a₁ = a₀ / ϖ（单位 AU，ϖ 为视差 parallax）。
- f_M = a₁³ / P² = M₂³ / (M₁ + M₂)²（单位：M☉；P 以年为单位）。
- 给定发光星质量 M₁，解三次方程得到 M₂。

**误差传播（error propagation）**

- 用 `corr_vec` 列重建相关矩阵（correlation matrix），对 (ϖ, A, B, F, G, P) 做多元高斯（multivariate Gaussian）蒙特卡洛（Monte Carlo）采样。
- 参数顺序由 `bit_index` 决定，必须先从官方文档或 `TAP_SCHEMA` 中核实。

**筛选的巧办法**

- f_M 可以完全在 ADQL 中计算，它只用到 `SQRT` 和 `POWER`。
- 服务器在约 17 万条天体测量轨道解上算完 f_M，只返回超过阈值的几百行。
- 对比方案：下载全表需要约 20 MB，而且不必要。

## 步骤

1. **核实数据结构**：查询 `TAP_SCHEMA.columns`，取得 `nss_two_body_orbit` 的列说明，确认 `bit_index` 和 `corr_vec` 的参数顺序，以及 Thiele–Innes 常数的单位。
2. **核实文献数值**：BH1、BH2 的发光星质量 M₁ 和黑洞质量 M₂，以及 El-Badry et al. 2024 列出的 21 个中子星候选体的 source_id，都要提升到 [V]。
3. **建研究文件夹** `studies/001-m04-gaia-dormant-black-holes/`：先写 README 第 1–4 节（预注册 pre-registration），并在 `study.yaml` 中写入足迹（footprint）字段，供后续 Atlas 使用。
4. **实现**：
   - `run.py`：取数、复现计算和筛选。
   - 通用的 Thiele–Innes 与质量函数计算放进核心库的新模块 `astrolab/orbits.py`，并配单元测试（unit test）。
5. **审稿（referee）**：派一个独立的子智能体（subagent），只给代码与结果，专门检查系统误差（systematics），例如假阳性（false positive）的来源：三体系统（triples）、光心稀释（photocentre dilution）、轨道解拟合质量。
6. **可视化**：研究网页显示复现值与论文值的对比、质量函数分布图、候选体表格。
7. **登记与收尾**：更新结论条目 `gaia-dormant-black-holes.yaml`、`STATUS.md` 和研究日志。

## 验收标准

- BH1、BH2 的 M₂ 复现值与论文值之差在合并误差的 2σ 以内；如果不在，要给出能说清楚的原因。
- 服务器端筛选只返回 MB 级数据，并且在候选体中找回 BH1 和 BH2。
- 报告找回了多少个已知中子星候选体（召回率，recall）。
- 发布版本作为参数；用 `release=dr3` 完整跑通，且 `release=dr4` 的查询能够生成。
- 测试全部通过，结论条目更新为 `reproduced` 或 `partial`。

## 风险

- `corr_vec` 的参数顺序可能理解错。对策：在 BH1 上把 Monte Carlo 误差与直接误差传播对比，并与论文对照。
- DR4 的表名和列名可能改变。对策：查询模板集中在一处；发布当天先查 `TAP_SCHEMA`，确认后再运行。

## 执行记录

### 2026-11-11

- 计划写成，开始执行。

**步骤 1：核实数据结构**
- 官方 `nsstools` 源码确定了相关矩阵 `corr_vec` 的参数顺序。文档子智能体的推断是错的，已经用官方实现替代，并写了对照测试。

**步骤 2：核实文献数值**
- BH1、BH2 的发光星质量 M₁、黑洞质量 M₂，以及 21 个中子星候选的源编号，都已对照 arXiv 全文核实。

**步骤 3–4：实现**
- 新增核心模块 `astrolab/orbits.py`。
- 研究位于 `studies/001`。
- 核心库新增三项能力：研究输入总预算、`ctx.count()` 先计数、TAP 查询失败时退避重试并回退到异步端点。
- 新增 `AGENTS.md`（数据下载约束），以及两个技能：`referee` 和 `server-side-query`。

**步骤 5：审稿**
- 审稿报告共 10 条，逐条核对和分类处理，见研究 README 第 6 节。
- 新增的检验都标为事后（post-hoc）：R1b、视向速度否决规则、解类型否决规则。每条否决规则都在 23 个正样本上验证过。

**步骤 6：网页**
- 已完成；脚本语法用 node 检查过。

**步骤 7：登记**
- 结论条目状态改为 `partial`：BH1、BH2 已复现；BH3 要等 DR4。

**验收**
- 测试 35 项全部通过。
- R1、R2、S1、S2、D1 全部通过。
- 数据量：查询服务器上的 16.9 万条解，只下载约 0.5 MB。

**遗留到 DR4 发布日（12-02）**
1. 用 `TAP_SCHEMA` 确认 DR4 的表名和列名。
2. 运行 `release="dr4"`。
3. 用 DR4 的历元数据检验剩下的 51 个候选。

另外，三体系统分诊（AMRF triage）和视差偏差处理列为开放问题。

- **状态：完成**（DR3 部分）。
