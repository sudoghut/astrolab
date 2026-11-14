# TODO · 待办清单（to-do list）

所有要做的事先登记在这里再动手。规则见 `AGENTS.md` 第二条"待办清单"，设计见 [006 号计划](design/006-plan_todo-list-and-done-log-mechanism.md)。完成或放弃的条目移到 [DONE.md](DONE.md)。

条目格式：`- [ ] **T-NNN** 标题 · 登记 YYYY-MM-DD`（`NNN` 为三位数字，不足补零；标题中不要出现 ` · ` 或 ` — `），后面按需加 `· 截止 YYYY-MM-DD`、`· 分支 名称`、`· 计划 […](design/…)`、`· 前置 T-NNN`、`· 来源 T-NNN`（多个编号用 `、` 分隔）；简单任务在子条目 `计划：` 里写步骤，进度与说明写在 `备注：` 里。新编号取 `TODO.md` 与 `DONE.md` 中最大编号加 1，永不复用。

## 进行中（Doing）

- [ ] **T-004** M1：DESI BAO 复现，引入 `cosmo` 与 `infer` 模块 · 登记 2026-11-14 · 分支 feat/m1-desi-bao · 计划 [010](design/010-plan_m01-desi-dr2-bao-evolving-dark-energy-cosmo-infer.md)
  - 备注：论文研究，按 `paper-study` 技能分 5 个环节（见计划 010）；环节 1（计划与核实）、环节 2（Wiki 文章与 Lean）已过双闸审查；环节 3（预注册与核心模块）已过双闸审查；环节 4（run.py、结果、网页）进行中。

## 下一步（Next）

按优先级排序，最重要的在最上面。

- [ ] **T-002** M4：Gaia DR4 发布日运行 · 登记 2026-11-14 · 截止 2026-12-02 · 前置 T-003、T-011
  - 计划：按技能 `gaia-dr4-release-day` 执行（确认模式与解类型、先计数、存档 DR3 结果、`PARAMS["release"] = "dr4"`、`--refresh` 运行），判据见研究 `README.md` 第 2–4 节的 DR4 附录（R1–R3、S1/S2-DR4、V-DR4、51 个幸存候选的 F-DR4 标签、S3-DR4）。Gaia 数据库 2026-11-25 至 12-02 下线，期间不做 DR3 查询。
  - 备注：DR4 运行后 `results/` 不再有 DR3 的 `post_hoc.R1b_*`，届时把 `argument/Argument.lean` 中 `num_astro1` 的绑定路径改为 `results/dr3/summary.json`，并且与 DR4 的 `results/` 放在同一个 PR 里，否则研究状态为 reproduced 时 Lean 测试会失败（来源 T-010）。
- [ ] **T-005** Atlas 导航：天空视图与尺度视图，研究以足迹（footprint）形式出现在图上 · 登记 2026-11-14
  - 计划：复杂任务，先写 design 计划；新视图遵守双语规则。
- [ ] **T-012** M2：哈勃张力（SH0ES、CCHP、H0DN）的距离阶梯复现与跨论文元分析 · 登记 2026-11-14
  - 计划：按论文立项流程（`paper-study` 技能）：先把 ROADMAP 中本里程碑的 [S]/[U] 项核实为 [V]，写双语 Wiki 文章与 Lean 论证拆解，再预注册、实现 `run.py` 与网页；复杂度达到第二条标准时先写 design 计划。论文：Riess et al. 2022 arXiv:2112.04510（卷页号 [U]）、SH0ES 的 JWST 复核 arXiv:2408.11770、Freedman et al. 2025 arXiv:2408.06153 [S]、H0DN arXiv:2510.23823 [S]、TDCOSMO 2025 arXiv:2506.03023 [S]。能力：距离阶梯广义最小二乘（GLS）拟合、对校准星系的自助法（bootstrap）。数据为公开的 Pantheon+SH0ES 设计矩阵与协方差及论文表格，MB 级。
- [ ] **T-013** M7：宽双星引力检验（MOND 之争） · 登记 2026-11-14
  - 计划：按论文立项流程（`paper-study` 技能）：先把 ROADMAP 中本里程碑的 [S]/[U] 项核实为 [V]，写双语 Wiki 文章与 Lean 论证拆解，再预注册、实现 `run.py` 与网页；复杂度达到第二条标准时先写 design 计划。论文：Cookson, Banik, El-Badry et al. 2026 arXiv:2602.24035；Chae et al. arXiv:2601.21728（修改中）。能力：服务器端自连接配对、前向建模、污染成分建模。数据 5–20 MB，必须服务器端自连接，不下载 El-Badry 2021 星表（AGENTS.md 1.5）。
- [ ] **T-014** M9：纳赫兹引力波背景（NANOGrav 15 年数据） · 登记 2026-11-14
  - 计划：按论文立项流程（`paper-study` 技能）：先把 ROADMAP 中本里程碑的 [S]/[U] 项核实为 [V]，写双语 Wiki 文章与 Lean 论证拆解，再预注册、实现 `run.py` 与网页；复杂度达到第二条标准时先写 design 计划。论文：Agazie et al. 2023 arXiv:2306.16213 [S]。数据：zenodo.org/records/10344086 v1.1.0 [S] 中公开的汇总量（自由谱、后验摘要），MB 级。能力：自由谱拟合、模型比较。
- [ ] **T-015** M8：z ≈ 14 星系的光谱确认与亮星系过多 · 登记 2026-11-14
  - 计划：按论文立项流程（`paper-study` 技能）：先把 ROADMAP 中本里程碑的 [S]/[U] 项核实为 [V]，写双语 Wiki 文章与 Lean 论证拆解，再预注册、实现 `run.py` 与网页；复杂度达到第二条标准时先写 design 计划。论文：Carniani et al. 2024 arXiv:2405.18485 [S]、Naidu et al. 2026 arXiv:2505.11263 [S]、Harikane et al. 2025 arXiv:2406.18352。能力：紫外光度函数、晕质量函数模型。数据为论文表格，kB 级。
- [ ] **T-016** M10：GWTC-4.0 双黑洞质量谱结构 · 登记 2026-11-14
  - 计划：按论文立项流程（`paper-study` 技能）：先把 ROADMAP 中本里程碑的 [S]/[U] 项核实为 [V]，写双语 Wiki 文章与 Lean 论证拆解，再预注册、实现 `run.py` 与网页；复杂度达到第二条标准时先写 design 计划。论文：GWTC-4.0 arXiv:2508.18082、群体分析 arXiv:2508.18083。能力：群体推断、汇总量再分析。只取事件列表（GWOSC 事件接口，kB 级）、图表包（约 8.7 MB）与 popsummary，禁止下载 35 GB 数据发布的大文件与单事件后验（AGENTS.md 1.5）。
- [ ] **T-017** M3：S8 张力减弱的多探针一致性 · 登记 2026-11-14
  - 计划：按论文立项流程（`paper-study` 技能）：先把 ROADMAP 中本里程碑的 [S]/[U] 项核实为 [V]，写双语 Wiki 文章与 Lean 论证拆解，再预注册、实现 `run.py` 与网页；复杂度达到第二条标准时先写 design 计划。论文：DES Y6 3x2pt arXiv:2601.14559 及 ROADMAP 所列其他探针。能力：多探针一致性元分析。数据为各探针公开的后验与链文件（chains）：下载前先按 AGENTS.md 第一条核对大小，能用汇总值时不取链文件。
- [ ] **T-018** M6：银河系外区旋转曲线下降 · 登记 2026-11-14
  - 计划：按论文立项流程（`paper-study` 技能）：先把 ROADMAP 中本里程碑的 [S]/[U] 项核实为 [V]，写双语 Wiki 文章与 Lean 论证拆解，再预注册、实现 `run.py` 与网页；复杂度达到第二条标准时先写 design 计划。论文：ROADMAP M6 所列，以及综述 Melchiorri & Ruchika 2026 arXiv:2608.10189。能力：质量模型拟合、金斯方程（Jeans equation）系统误差。数据 kB–MB。
- [ ] **T-019** M5：银河系厚盘早期形成（亚巨星年龄） · 登记 2026-11-14
  - 计划：按论文立项流程（`paper-study` 技能）：先把 ROADMAP 中本里程碑的 [S]/[U] 项核实为 [V]，写双语 Wiki 文章与 Lean 论证拆解，再预注册、实现 `run.py` 与网页；复杂度达到第二条标准时先写 design 计划。论文：Xiang & Rix 2022 arXiv:2203.12110 及 2025 年的更新星表（320,028 颗亚巨星，NADC，DOI 10.12149/101467）。能力：外部星表与 Gaia 的交叉匹配，只取所需列，预计不超过 20 MB；NADC 文件的实际大小为 [U]，取数前先核实（AGENTS.md 1.3）。

## 待办池（Backlog）

未排序，暂不安排的事都放这里，新条目加在末尾。工作中发现、但不属于当前分支的问题也登记在这里，并写明 `来源 T-NNN`；其他条目不必写来源。

- [ ] **T-006** 技能：新建研究（new study） · 登记 2026-11-14
- [ ] **T-007** 技能：文献核实（literature verification） · 登记 2026-11-14
- [ ] **T-008** 技能：出报告（report） · 登记 2026-11-14
- [ ] **T-020** 候选 M11：Radcliffe 波的振荡 · 登记 2026-11-14
  - 计划：论文：Konietzka et al. 2024, Nature 628, 62 [V]；细节为 [U]，立项前先核实。
- [ ] **T-021** 候选 M12：Gaia XP 光谱金属丰度与银河系贫而老的核心 · 登记 2026-11-14
  - 计划：全部为 [U]：立项前先确定论文并核实。
- [ ] **T-022** M1：在 R2 的拟合点用 CAMB 核对 θ* 标定，判断压缩 CMB 先验的 ωbc 约定 · 登记 2026-11-14 · 来源 T-004
  - 备注：需要先征得用户同意安装 CAMB（pip 包，非数据）；独立审稿指出 R2 两种解读的分歧可能落在 θ* 标定的宇宙学依赖之内。
