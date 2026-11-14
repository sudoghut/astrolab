# 研究日志（research log）· M4：Gaia 休眠黑洞

按时间倒序追加。

## 2026-11-14

### 论证的独立审稿（argument referee）与修订（T-010，设计计划 009 环节 2）

独立审稿子智能体只看到三篇论文、`argument/Argument.lean` 与 Lean 测试生成的"引文—类型—内容"对照表，不看我们的文章。2 个严重问题，均成立：

- **统一的 5 M☉ 阈值让引文承担了它们没有说的内容**：BH2、BH3 的句子讲的是 8.9 与 32.7 M☉ 的伴星，BH1 摘要写的是严格的"> 5"。改为按系统设定阈值（BH1 `> 5`、BH2 `≥ 8.0`、BH3 `≥ 30` M☉），NUM 绑定改为 `> 5.0`。
- **`mod_ns3` 强于引文**：BH3 的句子只排除中子星，没有排除白矮星。`mod_ns3` 改为推出新原子 `NoNS3`，新增 `lit_wd3`（LIT [implied]，钱德拉塞卡极限（Chandrasekhar limit））完成到 BH3 的一步。

次要意见采纳：`mod_fit3` 改为 [implied]（论文给出方法，没有给出从估计值到下限的一步）；文章写明 BH1 三条质量路径都依赖同一批后续视向速度，"多余"不等于对视向速度数据出问题也稳健；写明 `num_astro1` 是多余前提、绑定的是低显著性 DR3 解的中位数；`Faint2` 的说明收窄到蓝端约 2% 的限制；BH3 结论改用摘要原文；`lit_ns1` 注明中子星最大质量约 2.3–2.5 M☉，且不考虑奇异致密天体。

双闸审查中又补了两处：`lit_wd3` 加上前件 `NoStar3`（否则一颗 30 M☉ 的普通恒星就是反例）；`mod_dark2` 改为 [implied]，因为引文只说 9 M☉ 的单星。

修订后的 Lean 结论：`explicit_insufficient`（GAP `gap_few3`）、`stated_insufficient`，BH1 质量路径的 8 个前提为多余。审稿表见 `README.md` 第 6b 节。

### 为 DR4 做准备：按数据发布参数化与 DR4 预注册（T-011，设计计划 008）

**预注册（pre-registration）**：`README.md` 第 2–4 节加入注明日期的 DR4 附录，写于 DR4 发布之前。要点如下。

- **信息隔离（information barrier）**：发布日要做几项决定——天体测量类型、非验证类型、`corr_vec` 顺序、RV 列、交叉匹配表、参考历元。这些决定只凭元数据与文档做出，记入本日志并提交之后，才取任何单个源的 DR4 数据。
- **主解规则（R-sel）**：逐源统一使用，并列规则一直排到 Thiele-Innes 常数，选择结果与行序无关。
- **BH3 的判据 R3**：M1 = 0.76 ± 0.05 M☉，比较值 32.70 ± 0.82 M☉，均取自 Panuzzo et al. 2024 并对照 arXiv 全文核实。
- **S1/S2/V 在 DR4 上的含义**：都有最小样本量，样本不足时判为"不可评估"，不会空洞地通过。
- **F-DR4**：51 个 DR3 幸存候选（survivors）各得到 8 个有序标签之一。
- **S3-DR4**：新候选设有先计数的停止规则。

**代码**：

- `run.py` 加入 `PARAMS` 与 `RELEASES`，所有 DR4 判据都由代码计算；
- 新增纯函数模块 `selection.py`，以及不联网的测试 `test_selection.py`、`test_dr4_criteria.py`、`test_run_guard.py`；
- 保护机制：结果先存档再切换发布，每个结果文件小于 1 MB，全部算完才写出；
- 发布日的辅助脚本 `dr4_query.py` 加入 `archive` 命令。

**DR3 重跑**（在 2026-11-25 数据库下线之前）：

- **新增**：`reference_ids.json`（109 个 DR3 编号的位置与星等），以及 `bh_candidates` 中的 `period_error`。
- **数值不变**：除下一条外，DR3 的预注册与事后数值全部不变。
- **例外**：BH2 的蒙特卡罗（Monte Carlo）中位数由 8.521 变为 8.517 M☉（−0.575σ → −0.581σ），判定不变。原因是 BH2 所用协方差（covariance）块的条件数（condition number）约 1.8e7，新环境的 LAPACK 给出另一种等价分解；变化约为一个中位数标准误（standard error of the median，约 0.005 M☉）。
- **结论**：DR3 的蒙特卡罗数值不能在不同机器之间逐位复现。

**环境**：本机用户目录里的 numpy 2 与 Anaconda 的 astropy 不兼容。为此在 `%LOCALAPPDATA%\astrolab\venv` 建了虚拟环境，用法写在不入库的 `CLAUDE.local.md`。

**DR4 演练（rehearsal）**：在暂存目录（scratchpad）中把 DR4 的模式（schema）临时指向 DR3 数据，跑通整条 DR4 路径。结果符合预期：

- 109/109 个编号解析成功；
- R1–R3 不可评估（协方差未确认可信），S1、S2、V 通过；
- 51 个幸存候选全部为 `persists`，S3 为 0。

**审查中抓到的真错误**（修复前代码从未在 DR4 上运行，所以没有造成实际影响）：

- 有一个编号未解析时，pandas 把 19 位的 Gaia 编号转成 float64，所有编号都会被悄悄改错；
- 去重让服务器的行序决定保留哪个解；
- 未经计数的候选取数绕过了 S3 的停止规则；
- 有几个文件可能超过 1 MB 的上限。

**网页**：`web/index.html` 按 `summary.release` 显示 DR3 或 DR4 的判据；`results/dr3/` 存在时提供 DR4/DR3 切换。

**双闸审查（dual-gate review）**：三个环节都已通过，过程见计划 008 的执行记录。

## 2026-11-11

### 准备工作

**确定数据结构**
- 用表访问协议（TAP, Table Access Protocol）查询 `TAP_SCHEMA`，取得 `nss_two_body_orbit` 的列说明。说明中只写了"`bit_index` 是对上面各字段的掩码（mask）"。`TAP_SCHEMA` 返回的列顺序并不可靠，例如 ra、dec 排在了最后，所以无法据此确定参数顺序。
- 让网页读取子智能体（subagent）阅读官方文档，再以 Gaia 数据处理与分析联盟（DPAC, Data Processing and Analysis Consortium）的官方包 `nsstools` 源码为准，确定了相关矩阵（correlation matrix）`corr_vec` 的参数顺序：
  - `Orbital` 解：ra, dec, parallax, pmra, pmdec, A, B, F, G, e, P, T
  - `AstroSpectroSB1` 解：在 e, P, T 之前加入 C, H, γ
  - 存储方式：上三角，按列优先（column-major）
- **死路（dead end）**：文档子智能体曾经推断"把参数列表倒过来读就是比特顺序"，这个推断与官方实现不符。教训是 packed 字段的顺序只能以官方实现为准，并且要写单元测试（unit test）。现在 `tests/test_orbits.py` 会逐元素对照 `nsstools`。
- 实测：BH1 是 12 参数的 `Orbital` 解，`corr_vec` 长 66；BH2 是 15 参数的 `AstroSpectroSB1` 解，`corr_vec` 长 105。所以 `corr_vec` 只覆盖拟合了的参数。BH3 在 DR3 的轨道表中确实没有解。

**服务器端查询的两个坑**
1. Gaia 的 `/sync` 端点间歇性返回 HTTP 503。在核心库 `fetch` 中加入了退避重试（backoff retry），并在必要时自动改用异步（async）端点。
2. 把质量函数（mass function）整个内联进 WHERE 子句会解析失败。逐项探测后发现，每个函数单独都能用，于是改成嵌套子查询（nested subqueries），逐层计算 a₀ 和 f_M。

以上两点已经写进技能 `.claude/skills/server-side-query/SKILL.md`。

**先计数，再下载**
- DR3 共有 169,227 个天体测量轨道解（astrometric orbital solutions）。
- 预注册（pre-registered）切割：f_M > 0.25 M☉，视差信噪比（parallax S/N）> 5。满足条件的有 3,343 个，在服务器端完成计算后下载。
- 作为对照：f_M > 0.1 时有 22,512 个。

### 结果（对照 README 中的预注册判据）

| 判据 | 结果 | 结论 |
|---|---|---|
| R1：BH1 | 只用 DR3 天体测量，M₂ = 13.3 (+2.9/−2.3) M☉；论文值 9.62 ± 0.18，偏差 +1.4σ | 通过 |
| R2：BH2 | M₂ = 8.52 (+0.61/−0.56) M☉；论文值 8.9 ± 0.3，偏差 −0.6σ | 通过 |
| S1：筛选规模与已知黑洞 | 3,343 行，结果文件约 0.4 MB；BH1、BH2 都在 M₂ > 3 的候选中 | 通过 |
| S2：中子星候选召回率 | 21/21，召回率（recall）100%；它们的 f_M 最小为 0.41 | 通过 |
| S3：M₂ > 3 的候选（探索性） | 87 个，其中已知 2 个，无质量标记的未知天体 5 个 | 待审稿 |
| D1：DR4 就绪 | 完整的 DR4 查询保存在 `results/dr4_screen_query.json` | 通过 |

R1 的补充说明：
- BH1 的 DR3 解中，Thiele–Innes 常数 G 的误差很大（±0.55 mas），所以只用天体测量时质量的不确定度大。
- 论文值结合了视向速度（radial velocity）随访，因而精度高得多。

S3 中 5 个无标记的未知天体：
- 4 个是 `OrbitalAlternative` 解，周期 20–90 d，给出 30–130 M☉ 这种物理上不合理的质量。这类解是 Gaia 为"有问题的源"提供的备选模型。不过它们没有被我们的预注册标记覆盖，**如果要排除，只能作为事后（post-hoc）标记，并注明理由**。
- 1 个是 Gaia DR3 6281177228434199296：`Orbital` 解，P = 154 d，距离 233 pc，类太阳主序星，M₂ ≈ 12 M☉。它的形态与 BH1 相似。我对它有"文献中做过随访、结论是假解"的模糊印象，但**没有核实之前不下任何结论**，已交给审稿子智能体查证。

### 独立审稿（referee）之后

审稿人找出了 10 个问题。我们逐条核对了代码、结果或论文原文，分类处理的明细见 README 第 6 节。最重要的几条如下。

**1. 预注册的质量标记（quality labels）本身没有经过验证**
- 这套标记把 BH1 标成了"低显著性（low-significance）"，把 BH2 标成了"巨星（giant）"。也就是说，如果盲目使用，两个真黑洞都会被当成可疑对象排除掉。
- 教训：**任何否决规则（veto）在使用之前，都必须先在已知的正样本（positive controls）上验证**，确认不会误杀真天体。

**2. S1 的执行与预注册不一致**
- README 中写的是"用论文中的 M₁"，代码里实际用的却是 FLAME 质量。
- 已改为按预注册的写法计算。两个黑洞的结论不变：BH1 M₂ = 12.8，BH2 M₂ = 8.5，都大于 3 M☉。

**3. R1 的检验力（statistical power）太弱**
- 合并误差约 2.6 M☉，即使代码有 40% 的误差也能通过。
- 事后（post-hoc）补充了 R1b：与 El-Badry 等人论文中**只用天体测量的解**比较。结果是 a₀ 偏差 0.09σ，M₂ 偏差 0.23σ，吻合得很好。

**4. 文献核实**
- 6281177228434199296 已在 El-Badry et al. 2023a 附录 E 中被视向速度随访排除。这一点我们对照论文原文核实过，不是只听审稿人转述。

**事后否决规则与验证**
- 规则 (i)：排除未经验证的 `OrbitalAlternative` 和 `OrbitalTargetedSearch` 解。
- 规则 (ii)：如果观测到的视向速度幅度 `rv_amplitude_robust` 小于轨道预测幅度的一半，则否决。预测的视向速度全幅为 2K，其中轨道倾角（inclination）由 cos i = (AG − BF)/a₀² 求出。
- **公式验证**：我们预测的幅度与论文表 E1 中 6 个源的值全部吻合，例如 167 对 171 ± 10、49 对 50 ± 2 km/s。
- **正样本验证**：23 个已知天体（BH1、BH2 和 21 个中子星候选）一个都没有被否决。不过其中只有 4 个有视向速度幅度数据，所以规则 (ii) 在正样本上的检验还偏弱。
- **与文献一致**：凡是有视向速度数据的源，规则 (ii) 的判定都与文献结论一致。

**否决之后的结果**
- 剩下 51 个未知候选，全部是巨星或低显著性的解，**没有一个是没有任何标记的主序星宿主**。不宣称任何发现。

**新发现的数据特性**
- 同一个天体可以有多条 NSS 解。关联表格时必须以（source_id, nss_solution_type）为键。

**页面检查**
- 用 `node --check` 检查网页脚本，发现一个变量重复声明（`labels`），已修复。
- 页面还没有在浏览器中做视觉检查。

### 结论

- BH1、BH2 只用 DR3 的复现成立。
- 服务器端筛选和否决规则已在正样本与文献上得到验证，可以用于 DR4。
- BH3 要等 DR4 才能复现，因此结论条目状态设为 `partial`。
