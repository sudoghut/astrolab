# DONE · 完成日志（done log）

从 [TODO.md](TODO.md) 移出的已完成（`[x]`）与已放弃（`[-]`）条目。按月分组（`## YYYY-MM`），月份与条目都按时间倒序，新条目加在当月小节最上面。规则见 `AGENTS.md` 第二条"待办清单"。

条目格式：

- 完成：`- [x] **T-NNN** 标题 · 完成 YYYY-MM-DD · PR #N · 计划 […](design/…) — 一句话结果`（先开 PR，拿到编号后补进条目再合并；`计划` 只在有 design 计划时写）
- 放弃：`- [-] **T-NNN** 标题 · 放弃 YYYY-MM-DD · 计划 […](design/…) — 放弃原因`（`计划` 同样只在有 design 计划时写）
- 标题中不要出现 ` · ` 或 ` — `；`python -m pytest` 会检查格式。

本机制建立（2026-11-14）之前完成的工作见 `git log` 与 `design/` 各计划的执行记录，不补登。

## 2026-11

- [x] **T-015** M8：z ≈ 14 星系的光谱确认与亮星系过多 · 完成 2026-11-15 · PR #15 · 计划 [015](design/015-plan_m08-z14-galaxies-number-density-and-required-uv-scatter.md) — 研究 006 已复现：Naidu 等 2026 的 z = 14–15 数密度（log φ = −5.36）与体积由两个源复现；独立的恒定 SFE 晕模型（z ≈ 8 校准）预言为 N26 基准的 9.4 倍（72 个变体 2.5–37 倍，依赖校准），所需 σ_UV 1.38 mag（1.07–1.60）；独立审稿指出 z ≈ 8 光度函数的 1σ 不确定性或少量尘埃就使两个判定翻转（后续 T-025）；Wiki 文章与 Lean 论证（四个缺口：判决规则、宇宙方差、有效面积、围绕探测选取的箱）
- [x] **T-014** M9：纳赫兹引力波背景（NANOGrav 15 年数据） · 完成 2026-11-15 · PR #14 · 计划 [014](design/014-plan_m09-nanograv-free-spectrum-power-law-and-spectral-index.md) — 研究 005 已复现：在 KDE 自由谱 v2.0.0 上本机重拟，γ = 13/3 时 A = 2.31 [1.82, 2.92] × 10⁻¹⁵（与 L8 的区间一致，Hellinger 0.099），自由拟合 γ = 3.25、A = 6.33 × 10⁻¹⁵，γ = 13/3 的 HPD 水平 q = 0.979（与 L8 所称张力同一量级）；表 A1 中 8 个预言与 90% 区间重叠（Lean 绑定成立）；v1.1.0 按预注册规则不可评估；独立审稿指出结论以 DMX 噪声模型为条件（DMGP 上 q = 0.62，T-024），R4 的 ln BF 2.37 主要来自 γ < 13/3 的偏好；Wiki 文章与 Lean 论证（两条途径，`gap_overlap`、`gap_holo`、`gap_repr` 三个缺口）
- [x] **T-012** M2：哈勃张力（SH0ES、CCHP、H0DN）的距离阶梯复现与跨论文元分析 · 完成 2026-11-14 · PR #12 · 计划 [012](design/012-plan_m02-hubble-tension-distance-ladder-gls-and-host-selection.md) — 研究 003 已结束：对 SH0ES 公开矩阵的 GLS 复现 R22 印出的基线（73.04，χ²/自由度 1.031；作者的 lstsq 文件是另一个拟合）；锚点一步复现；L 的列不按表 6 排列，预注册的宿主一步、R3、R4 不可评估，数据之后修订标注后宿主一步为 −0.073 ± 0.033 mag（−2.2σ，按随机子样本的离散约 1.7σ，边缘显著，后续检验 T-023），同宿主上造父变星与 TRGB 一致（d = +0.010 ± 0.048 mag），CCHP 的选择位于随机子样本第 5.7 百分位；Wiki 文章与 Lean 论证（`gap_rule` 为补上的推理规则）；新增 `infer.gls`
- [x] **T-005** Atlas 导航：天空视图与尺度视图，研究以足迹（footprint）形式出现在图上 · 完成 2026-11-14 · PR #11 · 计划 [011](design/011-plan_atlas-sky-and-scale-views-from-study-footprints.md) — `study.yaml` 的足迹模式（校验、坐标解析、银道坐标换算）进入 `atlas.json`；Atlas 增加尺度视图（对数距离轴）与天空视图（银道莫尔韦德投影），页面内 SVG、双语；研究 000–002 有了足迹
- [x] **T-004** M1：DESI BAO 复现，引入 `cosmo` 与 `infer` 模块 · 完成 2026-11-14 · PR #10 · 计划 [010](design/010-plan_m01-desi-dr2-bao-evolving-dark-energy-cosmo-infer.md) — 研究 002 已复现：只用 BAO 的 Ωm、h·r_d 与不含 CMB 的三个 Δχ²（−4.65、−4.86、−10.03）复现；压缩 CMB 先验的 Δχ² 只在 ωbc 不含 ων 的解读下复现（−8.01 对 −6.59，有条件复现），分歧可能落在 θ* 标定误差之内（T-022）；Wiki 文章与 Lean 论证（`explicit_insufficient`：威尔克斯校准为缺口）；新增核心模块 `cosmo`、`infer`
- [x] **T-010** 补做：按论文立项流程为 M4 补写 Wiki 文章与 Lean 论证拆解 · 完成 2026-11-14 · PR #9 · 计划 [009](design/009-plan_m04-retrofit-wiki-article-and-lean-argument.md) — 双语 Wiki 文章 `Study-001-gaia-dormant-black-holes`（第三部分为事后补写）与 Lean 论证（`argument/`）：论文明说的前提不足（`stated_insufficient`），加上标准知识仍有缺口（`explicit_insufficient`：BH3 论文没有排除三个以上致密天体，`gap_few3`）；BH1 质量的三条路径使 8 个前提多余；经独立审稿修订（按系统设定质量阈值、BH3 的白矮星一步）
- [x] **T-011** M4：DR4 前的准备，把研究改成按数据发布参数化并预注册 DR4 判据 · 完成 2026-11-14 · PR #7 · 计划 [008](design/008-plan_m04-release-parameterisation-and-dr4-pre-registration.md) — `run.py` 按 `PARAMS`/`RELEASES` 参数化，README 中注明日期的 DR4 附录预注册了全部 DR4 判据并由代码计算；DR3 在 11-25 前重跑（数值不变，BH2 蒙特卡罗中位数差 0.004 M☉ 已说明）；网页支持 DR4/DR3 切换；运行手册按信息隔离重写
- [x] **T-003** 技能：DR4 发布日运行手册（run-book） · 完成 2026-11-14 · PR #6 — 新增技能 `gaia-dr4-release-day`（预检表列出研究中所有假定 DR3 的位置、确认模式与解类型、先计数、源编号核对、失败回退）与查询辅助脚本 `dr4_query.py` 及不联网测试；代码层面的发布参数化登记为 T-011
- [x] **T-009** 论文立项流程：Wiki 双语文章、Lean 论证检查与对话探索 · 完成 2026-11-14 · PR #5 · 计划 [007](design/007-plan_paper-to-study-workflow-wiki-article-lean-argument-and-chat-exploration.md) — 新增 `paper-study` 技能与文章模板、`AGENTS.md` 规则、Lean 论证模板与机器检查（`tests/test_lean_arguments.py`）、`python -m astrolab explore` 命令
- [x] **T-001** 建立待办清单与完成日志机制 · 完成 2026-11-14 · PR #4 · 计划 [006](design/006-plan_todo-list-and-done-log-mechanism.md) — 新增 `TODO.md`、`DONE.md`、`AGENTS.md` 规则与格式检查测试 `tests/test_todo.py`
