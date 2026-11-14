# 008 · 工作计划：M4 按数据发布参数化（release parameterisation）与 DR4 预注册

状态：进行中
创建：2026-11-14
待办：T-011（`TODO.md`）；前置于 T-002（DR4 发布日运行）

## 1. 目标

Gaia DR4 于 2026-12-02 发布，Gaia 数据库（archive）在 2026-11-25 至 12-02 下线。M4 研究（`studies/001-m04-gaia-dormant-black-holes/`）目前只能"改代码"切到 DR4，运行手册（run-book，技能 `gaia-dr4-release-day`）的预检表列出了十几处假定 DR3 的地方。本计划在数据库下线前把它们改掉，使发布日只需：

1. 确认模式（schema）与解类型（solution type），必要时改 `screen.SCHEMAS`；
2. 存档 DR3 结果；
3. 把 `PARAMS["release"]` 改为 `"dr4"`（或 `python -m astrolab explore 001 --set release=dr4` 先试）；
4. `python -m astrolab run 001 --refresh`。

同时，**在发布前写好 DR4 的预注册（pre-registration）**：BH3 的判据 R3、S1/S2/否决规则（veto）在 DR4 上的含义、DR3 剩下的 51 个候选怎样判定。

不做：不改核心库（`astrolab/`）；不改筛选的物理方法；不在 DR4 发布前对 DR4 下任何结论。

## 2. 设计

### 2.1 参数（`PARAMS`）

按 `AGENTS.md` 第二条，`run.py` 开头放 `PARAMS` 字典，`main()` 调用时读取并作为参数传给各函数，随结果保存在 `summary.json` 的 `params` 中：

| 键 | DR3 取值 | 含义 |
|---|---|---|
| `release` | `"dr3"` | `screen.SCHEMAS` 的键；决定模式名与来源标签（provenance label） |
| `fm_min` | 0.25 | 服务器端预选的质量函数（mass function）下限 [M☉] |
| `plx_snr_min` | 5.0 | 视差信噪比下限 |
| `m2_bh_min` | 3.0 | 候选黑洞的伴星质量下限 [M☉] |
| `rv_ratio_min` | 0.5 | 视向速度（RV, radial velocity）否决规则的比值下限 |
| `unvalidated_types` | `["OrbitalAlternative", "OrbitalTargetedSearch"]` | 类型否决规则（DR4 上按发布日确认的类型名修改，并在 `log.md` 记录） |

`TARGETS`（论文给出的数值）仍是常量，不属于可调参数。

### 2.2 与发布有关的标签和键名

- 来源标签：`{"dr3": "Gaia DR3", "dr4": "Gaia DR4"}[release]`。
- 结果键名去掉发布名：`period_dr3_d` → `period_d`，`period_dr3_err_d` → `period_err_d`；`targets.json`、`reproduction.json` 中的 `gaia_dr3` → `source_id`（输入表 `data/*.json` 中的 `gaia_dr3` 保留：那确实是论文给出的 DR3 编号）。
- 状态文字：`"no {label} orbital solution"`；DR3 下 BH3 仍为预期的"无解"。
- `D1_dr4_query_ok` 改为检查 `screen.SCHEMAS["dr4"]`，不再写死 `gaiadr4`。

### 2.3 BH3 与多解

- BH3 的 M1 = 0.76 ± 0.05 M☉，取自 Gaia Collaboration, Panuzzo et al. 2024（arXiv:2404.10486v2，表 3，"M⋆ [M⊙] | 0.76±0.05"），2026-11-14 对照 arXiv HTML 全文核实 [V]。
- BH3 加入正样本对照（positive controls）。DR3 中 BH3 没有轨道解，所以 `controls_checked` 在 DR3 仍是 23；新增 `controls_without_solution`（DR3 为 BH3）。
- 一个目标有多个轨道解时，全部计算并保存；判据所用的"主解"按预注册规则选取（第 3 节 R-sel）。

### 2.4 结果按发布分开

- `results/` 存放当前 `PARAMS["release"]` 的正式运行结果；发布日在切换前把 DR3 结果复制到 `results/dr3/` 并提交（`dr4_query.py archive-dr3`）。
- 保护：正式运行（不是对话探索）在 `release != "dr3"`、而 `results/` 仍是 DR3 结果且 `results/dr3/` 不存在时**拒绝运行**，防止覆盖 DR3 复现记录。
- `test_conclusions.py`：DR3 判据读 `results/dr3/`（存在时）或 `results/`（其 `release` 为 `dr3` 时）；DR4 判据只在 `results/summary.json` 的 `release` 为 `dr4` 时检查，否则跳过。
- 网页读 `../results/`，标签随 `summary.release` 变化；页面标题里的 169,227 改为读 `astrometric_solutions_total`。

### 2.5 辅助脚本与运行手册

`dr4_query.py` 改为读 `PARAMS`，新增 `archive-dr3` 命令；运行手册的预检表改为"已由 T-011 处理"的核对清单，只保留发布日仍需人工确认的项目。

## 3. 环节（每个环节过双闸审查）

1. **计划与 DR4 预注册**：本文件；研究 `README.md` 第 2–4 节加注日期的 DR4 附录；`TODO.md` 把 T-011 移入"进行中"。
2. **代码**：`run.py`（`PARAMS`、标签、键名、BH3、对照、多解、保护）、`test_conclusions.py`、`dr4_query.py` 与测试；用缓存重跑 DR3，核对数值与改动前一致。
3. **网页与文档**：`web/index.html` 标签；运行手册预检表；`log.md`、`STATUS.md`；收尾。

## 4. 执行记录

- 2026-11-14：建分支 `feat/m4-release-parameterise`；核实 BH3 文献数值（Panuzzo et al. 2024 arXiv v2：M⋆ = 0.76 ± 0.05 M☉，表 3；M_BH = 32.70 ± 0.82 M☉，摘要与式 5；P = 4253.1 ± 98.5 d，e = 0.7291 ± 0.0048，联合解 `AstroSpectroSB1`，表 2；数据为 DR4 之前的预发布 NSS 4.1 运行）。
