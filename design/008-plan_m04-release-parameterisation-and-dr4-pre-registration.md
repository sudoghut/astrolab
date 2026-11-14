# 008 · 工作计划：M4 按数据发布参数化（release parameterisation）与 DR4 预注册

状态：进行中
创建：2026-11-14
待办：T-011（`TODO.md`）；前置于 T-002（DR4 发布日运行）

## 1. 目标

Gaia DR4 于 2026-12-02 发布，Gaia 数据库（archive）在 2026-11-25 至 12-02 下线。M4 研究（`studies/001-m04-gaia-dormant-black-holes/`）目前只能靠改代码切到 DR4，运行手册（run-book，技能 `gaia-dr4-release-day`）的预检表列出了十几处假定 DR3 的地方。本计划在数据库下线前做两件事：

1. **把研究改成按数据发布参数化**，使发布日只剩确认与运行；
2. **在发布前写好 DR4 的预注册（pre-registration）**：见研究 `README.md` 第 2–4 节的 DR4 附录。附录里的每条判据都由 `run.py` 计算，发布日不靠手算。

发布日仍需人工确认的事（不能提前做）：
- DR4 的模式名（schema）：必要时改 `screen.SCHEMAS`；
- 解类型（solution type）：`ASTROMETRIC_TYPES` 与 `PARAMS["unvalidated_types"]`；
- 相关矩阵（correlation matrix）`corr_vec` 的参数顺序：DR4 若出现新的解类型或新顺序，要改 `astrolab/orbits.py`，这是核心库改动，届时另走审查；
- DR3 编号在 DR4 中能否找到。

之后依次：用 `dr4_query.py archive-dr3` 存档 DR3 结果（archive）；把 `PARAMS["release"]` 改为 `"dr4"`；`python -m astrolab run 001 --refresh`。

不做：
- 不改核心库（`astrolab/`）；
- 不改筛选的物理方法；
- 不改 DR3 的预注册判据；
- 不在 DR4 发布前对 DR4 下任何结论。

**时间约束**：环节 2 的 DR3 重跑会发出新的查询（缓存键是查询文本，查询一变就要联网），必须在 2026-11-25 之前完成；数据库下线期间无法重做。T-011 的截止日期定为 11-24。

## 2. 设计

### 2.1 参数（`PARAMS`）与固定的发布表

按 `AGENTS.md` 第二条，`run.py` 开头放 `PARAMS` 字典。`main()` 调用时读取，作为参数传给各函数，并随结果保存在 `summary.json` 的 `params` 中：

| 键 | DR3 取值 | 含义 |
|---|---|---|
| `release` | `"dr3"` | `screen.SCHEMAS` 的键 |
| `fm_min` | 0.25 | 服务器端预选的质量函数（mass function）下限 [M☉] |
| `plx_snr_min` | 5.0 | 视差信噪比（parallax S/N）下限 |
| `m2_bh_min` | 3.0 | 候选黑洞的伴星质量（companion mass）下限 [M☉] |
| `rv_ratio_min` | 0.5 | 视向速度（RV, radial velocity）否决规则（veto）的比值下限 |
| `unvalidated_types` | `["OrbitalAlternative", "OrbitalTargetedSearch"]` | 类型否决规则；DR4 的取值按预注册的规则在发布日确定 |

另设一张不属于可调参数的发布表 `RELEASES`，属于预注册内容：

| 发布 | 来源标签（provenance label） | RV 否决的适用条件 | `covariance_trusted` |
|---|---|---|---|
| `dr3` | `"Gaia DR3"` | 无限制（保持 DR3 的事后规则不变） | True（`nsstools` 顺序，已测试） |
| `dr4` | `"Gaia DR4"` | P < 1000 d 且 e < 0.8 | False，发布日确认顺序后改为 True 并记入 `log.md` |

`RELEASES` 的其他改动等同于修改预注册。

`TARGETS`（论文给出的数值）仍是常量。BH3 的 M1 = 0.76 ± 0.05 M☉，取自 Gaia Collaboration, Panuzzo et al. 2024（arXiv:2404.10486v2，表 3），已核实 [V]。

### 2.2 标签、键名与 DR3 专属检查

- 结果中的键名去掉发布名：
  - `period_dr3_d` → `period_d`，`period_dr3_err_d` → `period_err_d`；
  - `targets.json`、`reproduction.json` 中的 `gaia_dr3` → `source_id`；
  - 输入表 `data/*.json` 中的 `gaia_dr3` 保留，那确实是论文给出的 DR3 编号。
- 状态文字改为 `"no <label> orbital solution"`。`test_bh3_has_no_dr3_orbit` 相应修改。
- D1 与 `dr4_screen_query.json` 只属于 DR3 运行：
  - D1 改为检查 `screen.SCHEMAS["dr4"]`，不再写死 `gaiadr4`，在 `README.md` 加注日期；
  - R1b 只在 DR3 运行时计算；
  - 在 DR4 运行中，这几项都记为"不适用（not applicable）"。
- `bh_candidates.json` 增加 `period_error`，供 F-DR4 的周期检验使用。这必须在 DR3 重跑时加入。
- DR3 重跑新增 `reference_ids.json`：研究用到的 109 个 DR3 编号（87 个 M2 > 3 的 DR3 行、21 个中子星候选、BH3、文献标注的源）的 DR3 位置与 G 星等，供 DR4 的身份核对（identity check）。这需要一次小查询（< 200 行），也必须在 11-25 前完成。

### 2.3 主解（primary solution）、对照与 DR4 判据的计算

- 主解规则 R-sel 写成一个函数，对目标、对照、幸存候选（survivors）、新候选统一使用。所有解都保存，判据只用主解。
- 正样本对照（positive controls）加入 BH3：
  - 对照"被否决"按主解判断；
  - 没有解或找不到编号的对照单独列出，不计入；
  - DR3 中 BH3 没有轨道解，所以 `controls_checked` 在 DR3 仍是 23，新增的 `controls_without_solution` 为 `[BH3]`。
- DR3 运行时，`main()` 保持 DR3 的全部输出与判据。
- DR4 运行时（`release != "dr3"`），`main()` 额外计算 DR4 附录中的各项：
  - **编号解析（resolution）**：一次 `IN (...)` 查询 DR4 `gaia_source`（含 ra、dec、自行、G），按 README 的规则做身份核对，`unresolved` 记下原因。若 DR4 发布 DR3–DR4 交叉匹配表（neighbourhood table），按表回退的代码在发布日表名与列确定后再写，并单独过审查；在此之前只有"直接编号 + 身份核对"一条路径；
  - **判据**：R1–R3、S1-DR4、S2-DR4、V-DR4，以及 F-DR4 的 51 个标签；
  - **新候选**（new candidates）S3-DR4：对有 M2 > 3 筛选行的源，另发一个"全部解"查询，按编号分块（每块 ≤ 500 个），列包括解类型、Thiele-Innes 常数、周期及误差、偏心率、视差及误差、`significance`、`goodness_of_fit`、`gaia_source` 的 RV 列与 FLAME 质量，在全部解中选主解。不复用 `vet`（它缺这些列，且 `max_rows` 只有 2,000）；先在服务器端计数（同一编号列表上的 `COUNT(*)`），超过 50,000 行时 S3-DR4 记为"不可评估"，不取数，也不事后收窄选择，研究的 200 MB 预算因此不会被这一步突破；
  - S2-DR4 用目标、对照与幸存候选的解查询（README 第 3 节附录的第三行）中 21 个中子星候选的主解判断是否满足筛选条件，不依赖筛选结果；
  - 先在服务器端计数：≥ 50,000 时记 S1-DR4 失败，不取筛选结果，S3-DR4 与 `screen_points` 记为"不可评估"，其余判据（包括 S2-DR4）照常计算。
  - DR3 参考值（reference values）读自 `results/dr3/`（周期及其误差、a0、所用 M1、`reference_ids.json`）；还没存档时，若 `results/` 的发布是 DR3，就读 `results/`（与测试相同的回退），所以存档前的对话探索也能运行；
  - 结果写入 `summary.json` 的 `dr4` 小节，以及 `survivors_dr4.json`。
- RV 否决的适用条件按 `RELEASES` 中的条件判断（DR4：P < 1000 d 且 e < 0.8），并要求该列存在。

### 2.4 结果按发布分开，文件大小

- `results/` 存放当前发布的正式运行结果。`release.json`（只含发布名）标记运行所属的发布，与其他文件一起在最后写出（见下文"保存前统一检查"），不在运行开始时写。
- 存档：`dr4_query.py archive <release>` 把 `results/*.json` 复制到 `results/<release>/`。它不联网；`results/` 的发布与参数不符、或目标目录已存在时拒绝执行。
- 保护（双向）：正式运行（不是对话探索，以 `ctx.results == ctx.study.results_dir` 判断）如果要写的发布与 `results/release.json` 记录的不同，而后者还没存档到 `results/<旧发布>/`，就拒绝运行。缺少 `release.json` 时按 `summary.json` 的 `release` 判断。
- 所有结果算完后才写文件，所以取数阶段失败不会留下半个目录；写文件阶段本身失败（如磁盘错误）时，恢复办法是对 `results/` 做 `git restore`，并删除其中新出现的未入库文件（运行手册第 4 步），不是再跑一次旧发布。
- `test_conclusions.py`：
  - DR3 判据读 `results/dr3/`（存在时），否则读 `results/`（其发布为 DR3 时）；
  - DR4 判据只在 `results/` 的发布为 DR4 时检查，否则跳过。
- 文件大小（每个结果文件 < 1 MB，`AGENTS.md` 第一条）：
  - `screen_points.json` 硬上限 5,000 行：保留 M2 > 3 M☉ 的全部行（至多 2,000 行，超出时按 M2 从大到小取前 2,000），其余按固定随机种子抽样（sampling）补足到 5,000，并记录总行数与抽样标记。DR3 的 3,343 行不受影响；
  - `bh_candidates.json` 硬上限 2,500 行（约 0.9 MB），超出时按 M2 从大到小保留，并记录总数；F-DR4 与 S3-DR4 的计数在截断之前算好；
  - 所有结果先算完，保存前统一检查大小，超出 1 MB 则在任何文件写出之前报错，不留下写了一半的目录。

### 2.5 对话探索（exploring via chat）

有了 `PARAMS`，就可以用 `python -m astrolab explore 001 --tag <主题> --set release=dr4` 演练。探索输出每个文件不超过 1 MB，2.4 节的抽样保证 `screen_points` 不超标。在 DR4 发布前，演练会因为模式不存在而失败，这是预期结果；发布前的演练只用 `dr4_query.py --print`。

### 2.6 网页、运行手册与其他文件（环节 3）

- **网页**：
  - 标签随 `summary.release` 变化；
  - 页面说明中的 169,227 改为读取 `astrometric_solutions_total`；
  - `results/dr3/` 存在时，提供 DR3/DR4 切换，保证 DR3 复现结果（研究状态 `reproduced` 的依据）仍可查看。
- **运行手册与 `dr4_query.py`**：
  - 预检表改为"已由 T-011 处理"的核对清单；
  - 第 0、2、3、4、5 步与失败表中提到旧常量、BH3 TypeError、手工复制、手工判定幸存候选的地方，全部改为新机制。第 5 步改为直接读 F-DR4 结果；
  - 第 1 步：第 1.3 步要核对的列加入新的解析、全部解与 FLAME 查询；第 1.4 步改为"非验证类型按 DR4 文档决定并记入 `log.md`、`PARAMS`"（README 的预注册规则）；
  - `dr4_query.py types` 增加 `COUNT(a_thiele_innes)` 一列，用来按 README 的机械规则确定天体测量类型；运行手册写明信息隔离（information barrier）：三项发布日决定只凭元数据与文档，记入 `log.md` 并提交后，才取任何单个源的 DR4 数据；
  - `dr4_query.py` 读 `PARAMS`，新增 `archive <release>`；`followup` 删除（F-DR4 已在 `run.py` 中）；`resolve` 保留为运行前的检查，但改为调用 `run.py` 的解析与身份核对函数，保证与正式运行的结果一致。`dr4_query.py` 导入 `run` 是技能脚本，不是研究的辅助模块，`AGENTS.md` 中"辅助模块不 `import run`"的规则针对的是后者（覆盖 `PARAMS` 后不生效的问题），这里只读取，不受影响；
  - 发布日要在 `study.yaml` 的 `footprint.data` 中加入 DR4 表名，运行手册保留这一步。
- **日志与状态**：`log.md` 与 `STATUS.md`。

## 3. 环节（每个环节过双闸审查，dual-gate review）

1. **计划与 DR4 预注册**：本文件；研究 `README.md` 第 2–4 节注明日期的 DR4 附录与 D1 注记；`TODO.md`。
2. **代码**（`run.py` 中的新判据都配不联网的单元测试）：
   - `run.py`（2.1–2.4）、`test_conclusions.py`、`dr4_query.py` 与测试；
   - 重跑 DR3（11-25 之前），核对 DR3 数值与改动前一致；
   - 用人工构造的 DR4 形状数据做不联网的单元测试，检验 R-sel、F-DR4 标签与 S2-DR4 的计数规则。
3. **网页与文档**：2.6 节。

## 4. 执行记录

- 2026-11-14：建分支 `feat/m4-release-parameterise`。核实 BH3 的文献数值（Panuzzo et al. 2024，arXiv v2）：
  - M⋆ = 0.76 ± 0.05 M☉（表 3）；
  - M_BH = 32.70 ± 0.82 M☉（摘要与式 5）；
  - 联合解 `AstroSpectroSB1`（表 2）：P = 4253.1 ± 98.5 d，e = 0.7291 ± 0.0048，f_M = 31.23 ± 0.81 M☉；
  - 纯天体测量解 f_M = 32.03 ± 0.64 M☉；
  - 数据来自 DR4 之前的预发布 NSS 4.1 运行。
- 2026-11-14 · 环节 1 闸门 1（gate 1）第 1 轮：两位审查者（科学、规则与可行性）共 6 个严重问题，全部成立，已修改：
  - S2-DR4 固定计数遇上可变分母，改为 N_eval ≥ 15 且 ≥ 90%；
  - 主解规则对对照、幸存候选含糊，标签 `type-vetoed` 不可达，改为逐源统一的 R-sel，对照按主解判否决；
  - `persists` 缺 DR3 周期误差与 DR4 FLAME 质量，2.2 节保存 `period_error`，查询加入 `astrophysical_parameters`；
  - 长周期的 RV 否决可能因采样窗口误判，DR4 上限定 P < 2000 d；
  - DR4 判据在代码计划中没有位置，补 2.3 节；
  - DR4 规模的 `screen_points` 超过 1 MB，补 2.4 节的抽样。
  
  次要意见同时采纳：
  - 修正 R3 的预期推理（`AstroSpectroSB1` 的 a0/ϖ 等于 a1，没有方法偏差）；
  - 补 corr_vec 无法确认时的处理、交叉匹配后再判 `unresolved`、S3-DR4、类型否决名单的事先规则、D1 注记、R1b 只用于 DR3、双向保护、11-25 时限、运行手册需要更新的全部位置、术语括注英文。
- 2026-11-14 · 环节 1 闸门 1 第 2 轮：科学审查者无严重问题；规则审查者 1 个严重问题，成立：`screen_points` 的抽样规则保留 M2 > 1 的全部行，而 DR3 中 97.6% 的行 M2 > 1，等于没有上限，改为硬上限 5,000 行。同轮次要意见全部采纳：
  - 交叉匹配取最近邻居，并按归档的 DR3 位置与星等做身份核对；
  - RV 否决限于 P < 1000 d 且 e < 0.8；
  - V-DR4 要求至少 15 个计入的对照；
  - S1-DR4 中缺失的目标记为不可评估；超过 50,000 行时不中断其余判据；
  - `covariance_trusted` 开关；
  - `archive <release>` 与 `git restore` 恢复；
  - S3-DR4 在全部解中选主解；
  - 存档前回退读 `results/`；
  - 保存前统一检查大小；
  - 运行手册第 1 步列入更新；
  - DR3 对照规则改为按主解，加注日期；
  - 术语括注英文。
- 2026-11-14 · 环节 1 闸门 1 第 3 轮：两位审查者都没有严重问题，闸门 1 通过。同轮次要意见全部采纳，都是为了不在看到 DR4 数据后留下选择余地：
  - `covariance_trusted` 只能凭文档、在第一次正式运行前改；
  - S3-DR4 的入选看筛选行，标签看主解，编号全量保存；
  - 解析与参考值扩大到全部 109 个 DR3 编号；
  - 身份核对的边界情况：无自行、并列容差、记录原因；
  - 报告 RV 否决适用的幸存候选数；
  - "全部解"查询单独写，列名明确，并补进 README 第 3 节；
  - 交叉匹配表回退在发布日另行审查；
  - `release.json` 改为最后写出；
  - `resolve` 与正式运行共用函数；
  - S2-DR4 不依赖筛选结果；
  - DR3 新输入注明于 DR3 第 3 节。
- 2026-11-14 · 环节 1 闸门 2（Codex，只读沙箱）第 1 轮：2 个严重问题。
  - S1-DR4 在三个目标都不可评估时会空洞地通过。已成立并修改：至少 2 个目标可评估才能通过，否则记为"不可评估"。
  - 解类型与协方差的认定是发布日的选择。部分成立：DR4 的表结构无法预知，这一点本身避免不了。已改为：
    - 天体测量类型按机械规则确定：类型统计中有 Thiele-Innes 常数的类型；
    - 加上信息隔离：三项决定只凭元数据与文档，记录并提交后才取单个源的数据，之后再改一律记为事后修改。
  - 次要意见（变星巨星可能被判为 `unresolved`）不改：README 已写明，并会报告计数。
- 2026-11-14 · 环节 1 闸门 2 第 2 轮：
  - 1 个严重问题，成立：计划写 ≥ 50,000 时 S2-DR4 不可评估，README 写它不依赖筛选结果，两处矛盾。已统一为 README 的写法：S2-DR4 用对照的解查询，照常计算。
  - 次要意见采纳：README 写明类型统计是只返回聚合数的元数据查询，信息隔离之前不看任何单个源的行。
- 2026-11-14 · 环节 1 闸门 2 第 3 轮：2 个严重问题，都在运行手册里，原定在环节 3 更新，因与新预注册直接矛盾而提前修改。
  - 运行手册的 S2 仍按 19/21 判定，已改为 README 的 N_eval 规则。
  - 运行手册把 BH1 的 `corr_vec` 长度检查放在信息隔离之前。已改为 `covariance_trusted` 只凭文档决定；隔离之后的长度检查只能把它改回 False，不能改成 True。README 同步写明。
- 2026-11-14 · 环节 1 闸门 2 第 4 轮：1 个严重问题，成立：R-sel 没有最终的并列规则，选择可能取决于行的顺序。已补上：再按类型名的字典序，再按周期从小到大，缺失值排在最后。次要意见采纳：FLAME 质量为 NULL 时视为缺失。
- 2026-11-14 · 环节 1 闸门 2 第 5 轮：1 个严重问题，成立：S3 的"全部解"查询没有强制上限。已加入先计数的停止规则：超过 50,000 行时 S3-DR4 不可评估，不取数（约 15 MB，在 200 MB 研究预算之内）。
- 2026-11-14 · 环节 1 闸门 2 第 6 轮：无严重问题，无次要问题。**环节 1 通过双闸审查**：闸门 1 共 3 轮（严重问题 6 → 1 → 0），闸门 2 共 6 轮（2 → 1 → 2 → 1 → 1 → 0）。
