# 路线图（Roadmap）

- 来源：[002 号计划](design/002-plan_roadmap-literature-verification-2022-2026-landmark-results.md) 的文献核实（literature verification），2026-11-11
- 原则：每个里程碑（milestone）复现一个 2022–2026 年的代表性结果，借此逼出核心库的新能力，登记一个结论（claim），并留下开放问题（open questions）。

## 核实标记

| 标记 | 含义 |
|---|---|
| [V] | 已对照 arXiv、期刊或官方页面核实 |
| [S] | 仅来自搜索摘要或二手来源 |
| [U] | 未核实 |

**动手复现之前，必须把 [S] 和 [U] 项提升为 [V]。**

## 时间窗口：Gaia DR4 于 2026-12-02 发布 [V]

欧洲空间局（ESA）的 Gaia 第四次数据发布（DR4, Data Release 4）定于 **2026 年 12 月 2 日**。Gaia 数据库（archive）在 11 月 25 日至 12 月 2 日之间下线。

DR4 的内容：
- 基于 66 个月的观测数据。
- 首次发布全部历元数据（epoch data），包括天体测量（astrometry）、测光（photometry）、视向速度（radial velocity）时间序列，以及光谱。
- 包含大量非单星解（NSS, non-single-star solutions），其中有系外行星候选体（exoplanet candidates）和致密天体双星（compact-object binaries）。

**这是个人研究者少有的速度优势窗口**：如果在 DR3 上提前把管线（pipeline）做好，发布当天就能在 DR4 上运行。所以 M4 排在最前面，M7 次之。

## 里程碑总览

| 顺序 | # | 层级 | 结论 | 等级（grade） | 本地数据量 | 逼出的能力 |
|---|---|---|---|---|---|---|
| 1 | **M4** | L4 | Gaia 休眠黑洞（dormant black holes）BH1/BH2/BH3，以及中子星（neutron star）候选体 | established | kB 级 | NSS 轨道表查询、质量函数（mass function）计算、协方差（covariance）蒙特卡洛；**为 DR4 发布日准备** |
| 2 | **M1** | L0 | DESI 重子声学振荡（BAO, Baryon Acoustic Oscillations）测量；演化暗能量（evolving dark energy）迹象 | BAO 为 established；w0wa 为 hint，2026 年趋弱 | kB–MB | `cosmo` 宇宙学背景计算、似然（likelihood）框架、`infer` MCMC |
| 3 | M2 | L2 | 哈勃张力（Hubble tension）：SH0ES、CCHP 与 H0DN | tension（在校准层面有争议） | MB | 距离阶梯（distance ladder）广义最小二乘（GLS）拟合、跨论文元分析（meta-analysis） |
| 4 | M7 | L4 | 宽双星（wide binaries）引力检验，即 MOND 之争 | contested，趋向牛顿引力 | 5–20 MB（服务器端自连接） | 服务器端配对查询、前向建模（forward modelling）、污染成分建模 |
| 5 | M9 | X | 纳赫兹引力波背景（nanohertz gravitational-wave background） | 强证据（strong evidence），未达 5σ | MB | 自由谱（free spectrum）拟合、模型比较（model comparison） |
| 6 | M8 | L1 | z ≈ 14 星系的光谱确认，以及亮星系过多（bright-galaxy excess） | 探测为 established，解释为 contested | kB | 紫外光度函数（UV luminosity function）、晕质量函数（halo mass function）模型 |
| 7 | M10 | X | 双黑洞质量谱（BBH mass spectrum）结构（GWTC-4.0） | 35 M☉ 特征为 established，20 M☉ 特征为 hint | kB–MB（只用小文件） | 群体推断（population inference）、汇总量再分析 |
| 8 | M3 | L0 | S8 张力（S8 tension）减弱 | contested | kB | 多探针一致性（multi-probe consistency）元分析 |
| 9 | M6 | L3 | 银河系外区旋转曲线（rotation curve）下降 | 下降本身较一致，开普勒式解释为 contested | kB–MB | 质量模型（mass model）拟合、金斯方程（Jeans equation）系统误差 |
| 10 | M5 | L3 | 银河系厚盘（thick disk）早期形成（亚巨星年龄，subgiant ages） | established，有后续修正 | ≤ 20 MB（仅取所需列） | 外部星表与 Gaia 的交叉匹配（cross-match） |

候选里程碑：
- M11：Radcliffe 波（Radcliffe Wave）的振荡（Konietzka et al. 2024, Nature 628, 62 [V]）。细节为 [U]。
- M12：Gaia XP 光谱金属丰度（metallicity），以及银河系"贫而老的核心（poor old heart）"。全部为 [U]。

---

## 各里程碑详情

### M4 · Gaia 休眠黑洞（L4，established）

**文献** [V]
- BH1：El-Badry et al. 2023, MNRAS 518, 1057, arXiv:2209.06833
- BH2：El-Badry et al. 2023, MNRAS 521, 4323, arXiv:2302.07880
- BH3：Gaia Collaboration (Panuzzo et al.) 2024, A&A 686, L2, arXiv:2404.10486
- 中子星候选体扩展：El-Badry et al. 2024, OJAp 7, arXiv:2405.00089，从 DR3 中找出 21 个中子星候选体。

**关键数值** [V]

| 天体 | 黑洞质量 | 轨道周期 | 备注 |
|---|---|---|---|
| BH1 | 9.62 ± 0.18 M☉ | 185.6 d | |
| BH2 | 8.9 ± 0.3 M☉ | 1277 d | 偏心率（eccentricity）e ≈ 0.52 |
| BH3 | 32.70 ± 0.82 M☉ | 11.6 yr | 伴星为贫金属晕巨星（metal-poor halo giant），距离 590 pc |

**数据** [V]
- Gaia DR3 源编号（source_id）：
  - BH1：4373465352415301632
  - BH2：5870569352746779008
  - BH3：4318465066420528000
- BH1 和 BH2 在 `gaiadr3.nss_two_body_orbit` 表中有轨道解。
- **BH3 在 DR3 中没有轨道解**，它是在 DR4 预发布数据中发现的。DR4 发布之前，只能用论文表格复现。

**方法**
1. 由 Thiele–Innes 常数、视差（parallax）和周期求出光心轨道半长轴（photocentre semi-major axis）a₀，进而得到天体测量质量函数（astrometric mass function）。
2. 假设发光星（luminous star）的质量，求解暗伴星（dark companion）的质量 M₂。
3. 用 `corr_vec` 列重建相关矩阵（correlation matrix），对协方差做蒙特卡洛（Monte Carlo）采样。

整个计算只需几秒。

**开放问题**
- DR4 发布当天，对全部 NSS 轨道系统性筛选暗伴星质量大于 3 M☉ 的系统，并估计每颗恒星拥有这类伴星的比率（rate）。
- 在 DR4 轨道下，中子星与黑洞之间的质量间隙（mass gap）是否依然存在？
- 三体系统或混合光源（blend）导致假阳性（false positive）的比例有多高？

### M1 · DESI BAO 与演化暗能量（L0，hint）

**文献**
- DR1：DESI 2024 VI, JCAP 02 (2025) 021, arXiv:2404.03002 [V]
- DR2：Abdul-Karim et al. 2025, PRD 112, 083515, arXiv:2503.14738 [V]
- DR2 莱曼 α（Lyman-α）全形状（full-shape）分析：arXiv:2607.27410 (2026-07) [V]
- DES-Dovekie 超新星（SN, supernova）重新校准：Popovic et al. 2026 MNRAS, doi:10.1093/mnras/stag632, arXiv:2511.07517 [V]

**关键数值**（DR2）[V]
- 仅用 BAO，在 ΛCDM 下：Ωm = 0.2975 ± 0.0086。
- 演化暗能量模型 w0waCDM 相对 ΛCDM 的偏好程度（preference），随组合而变：

| 数据组合 | 偏好程度 |
|---|---|
| DESI + CMB | 3.1σ |
| + Pantheon+ | 2.8σ |
| + Union3 | 3.8σ |
| + DES-SN5YR | 4.2σ |

- 后续进展使信号**趋弱**：
  - Dovekie 重新校准后，DES-SN 组合（DES-Dovekie + CMB + DESI DR2）降至 3.2σ [V]。
  - Lyα 全形状分析给出 DESI+CMB 2.7σ、加超新星后 3.2σ [V]。

**数据**
- BAO 均值向量（mean vector）与协方差，kB 级：github.com/CobayaSampler/bao_data 的 `desi_bao_dr2/` 目录 [V]。
- 超新星距离模数（distance modulus）与协方差：github.com/CobayaSampler/sn_data [V]（2026-11-14 按 GitHub API 元数据核对大小：Pantheon+ 协方差 33.3 MB，Union3 约 11 kB，DES-Dovekie 6.2 MB；DES-SN5YR 协方差 53.5 MB，超过单次 50 MB 上限，不取，以 Dovekie 代替）。
- CMB 部分用压缩先验（compressed prior）：(θ*, ωb, ωbc) 的高斯近似（Gaussian approximation），均值与协方差见 DESI DR2 附录 A 式 35–36 [V]（θ* 的 6 位有效数字 0.0104103 取自 github.com/cmbant/PlanckEarlyLCDM [V]；式 35 的 ωbc 均值看来包含 ων）；论文用这一先验时给出 DESI + CMB 压缩先验的偏好为 2.4σ（Δχ² = −8.0，式 24、表 6）[V]。

**方法**
- 解析计算 D_M/r_d 和 D_H/r_d。
- 超新星似然中对绝对星等偏移做解析边缘化（analytic marginalisation）。
- 用 emcee 对 4–6 个参数采样，几分钟完成。

**开放问题**
- 信号有多少来自 w0–wa 参数化（parametrisation）？与分箱 w(z)（binned w(z)）或高斯过程（Gaussian process）重建相比如何？
- 逐一剔除某个示踪体（tracer）或某个超新星样本时，信号如何变化（leave-one-out sensitivity）？

### M2 · 哈勃张力（L2，tension）

**文献与数值**

| 测量 | H0 (km/s/Mpc) | 核实 |
|---|---|---|
| SH0ES (Riess et al. 2022, ApJL, doi:10.3847/2041-8213/ac5c5b, arXiv:2112.04510) | 73.04 ± 1.04 | [V]；卷页号 [U] |
| SH0ES HST 全样本（42 SN Ia、4 个锚点；arXiv:2408.11770 表 4） | 73.2 ± 0.9 | [V] |
| SH0ES 的 JWST 三方法合并（arXiv:2408.11770 摘要） | 72.6 ± 2.0 | [V] |
| CCHP (Freedman et al. 2025, ApJ 985, 182, arXiv:2408.06153)，TRGB 方法，24 个 SN Ia 校准 | 70.39 ± 1.22(stat) ± 1.33(sys) ± 0.70(σ_SN) | [V]（摘要；卷页号 [U]） |
| H0DN 本地距离网络（Local Distance Network, A&A 708, A166 (2026), arXiv:2510.23823） | 73.50 ± 0.81 | [V] |
| 早期宇宙：SPT-3G + ACT + Planck 组合（arXiv:2506.20707） | 67.19 ± 0.38 | [V] |
| 早期宇宙：ACT DR6（P-ACT + CMB 透镜 + DESI DR1 BAO，arXiv:2503.14452） | 68.22 ± 0.36 | [V] |
| 独立方法：TDCOSMO 2025 时间延迟透镜（time-delay lensing, A&A 704, A63 (2025), arXiv:2506.03023） | 71.6 (+3.9/−3.3) | [V] |
| SH0ES 限于 CCHP JWST 样本（10 宿主、11 SN Ia，只用 NGC 4258 锚点，近似式；arXiv:2408.11770 表 4、第 III.2 节；子样本误差待核（表 4 列含义不清，附录表 A1 为 2.0），不含 NGC 4258 的 1.1） | 71.2 | [V]（数值）；误差 [U] |

TRGB 指红巨星支顶端（Tip of the Red Giant Branch）。

**方法**
- 用 Pantheon+SH0ES 公开的设计矩阵（design matrix）做距离阶梯的广义最小二乘（GLS, Generalised Least Squares）拟合。
- 对 37 个校准宿主（calibrator hosts，含 42 颗 SN Ia）做无放回的子抽样与留一宿主（有放回的自助法（bootstrap）会复制相关的行）。

**开放问题**
- CCHP 与 SH0ES 的差异，是否主要来自校准星系样本的选择（host selection）？

### M7 · 宽双星引力检验（L4，contested，趋向牛顿引力）

**文献** [V]
- Chae 2023, ApJ 952, 128：g_obs/g_N = 1.43 ± 0.06，宣称约 10σ。
- Banik et al. 2024, MNRAS 527, 4573：α_grav = −0.021 (+0.065/−0.045)，以 16σ 排除修正牛顿动力学（MOND, Modified Newtonian Dynamics）。
- Cookson, Banik, El-Badry et al. 2026, MNRAS, arXiv:2602.24035：在最干净的样本中，牛顿引力的可能性是 MOND 的约 1500 倍。
- Chae, Lee, Hernandez et al., arXiv:2601.21728：用 36 对具有三维速度的双星，得到 γ = 1.60 (+0.24/−0.14)。该文正在修改中；去掉两个主导系统后，信号明显减弱。

**数据**
- El-Badry 等人 2021 年的宽双星星表有 **1.8 GB，不下载**。
- 改为在服务器端用 ADQL 自连接（self-join），重建 130–200 pc 以内的干净样本，约 5–20 MB。

**方法**
- 对缩放后的相对速度分布（scaled relative velocity distribution）做前向建模。
- 模型中包含三体系统（triples）、近距双星（close binaries）和偶然成对（chance alignments）等污染成分。

**开放问题**
- 在同一条管线中复现双方的样本切割，做盲化（blind）的"质量阶梯（quality ladder）"再分析。
- 用 DR4 的历元天体测量识别隐藏的近距双星（hidden close binaries）。

### M9 · 纳赫兹引力波背景（X，strong evidence）

**文献**
- NANOGrav 15 年数据：Agazie et al. 2023, ApJL 951, L8, arXiv:2306.16213 [S]
  - 振幅 A = 2.4 (+0.7/−0.6) × 10⁻¹⁵。
  - Hellings–Downs 角关联（angular correlation）显著性约 3σ。
- 其他脉冲星计时阵（PTA, Pulsar Timing Array）[V]：
  - EPTA：A&A 678, A50
  - PPTA：Reardon et al. 2023 ApJL
  - CPTA：Hellings–Downs 关联 4.6σ
- 截至 2026 年 11 月，未找到 IPTA DR3 的背景结果 [S]。

**数据**
- NANOGrav 15 年自由谱的核密度估计（KDE, Kernel Density Estimate）后验，MB 级：zenodo.org/records/10344086，使用 v1.1.0 版 [S]。

**方法**
- 用 PTArcade/ceffyl 拟合约 14 个频率点的自由谱（free spectrum）。
- 比较的模型：超大质量黑洞双星（SMBHB, Supermassive Black Hole Binaries）幂律、环境导致的谱转折（environmental turnover）、宇宙学起源模板（cosmological templates）。

### M8 · z ≈ 14 星系（L1）

**文献**
- JADES-GS-z14-0：Carniani et al. 2024, Nature 633, 318, arXiv:2405.18485，z = 14.32 [S]。
- MoM-z14：Naidu et al. 2026, OJAp 9, arXiv:2505.11263，z_spec = 14.44 ± 0.02 [S]。**修正：发表于 2026 年的 OJAp，不是 2025 年。**
- 紫外光度函数：Harikane et al. 2025 ApJ, arXiv:2406.18352 [V]。

截至 2026 年 11 月，尚未找到 z > 14.44 的光谱确认 [S]。

**方法**
- 用解析的晕质量函数，乘以恒星形成效率（star-formation efficiency），再加上紫外星等的随机弥散（UV scatter / burstiness）。
- 对论文表格中的光度函数数据点做低维 MCMC 拟合。

### M10 · GWTC-4.0 双黑洞质量谱（X）

**文献** [V]
- 引力波瞬变源目录（GWTC, Gravitational-Wave Transient Catalog）4.0：arXiv:2508.18082。
- 群体分析（population analysis）：arXiv:2508.18083, ApJL 1005, L51。
- GW231123：ApJL 993, L25。

**关键数值** [V]
- 总质量谱在 35 M☉ 以上变陡（steepening），在约 10 和 35 M☉ 处有过密（overdensity）；约 20 M☉ 处有可能的特征。
- 双黑洞局部并合率（local merger rate）为 13–26 Gpc⁻³ yr⁻¹。

**数据**
- 群体分析数据发布共 35 GB，**只取其中的小文件**：事件列表（10 kB）、图表包（8.7 MB）、popsummary 汇总。
- 事件参数表通过 GWOSC 事件 API 获取，kB 级。

### M3 · S8 张力（L0，contested）

**数值**

| 测量 | S8 | 核实 |
|---|---|---|
| KiDS-Legacy (Wright et al. 2025, A&A 703, A158) | 0.815 (+0.016/−0.021)，与 Planck 相差 0.73σ | [S] |
| DES Y6 3x2pt (arXiv:2601.14559) | 0.789 ± 0.012，在 S8 上相差 2.6σ | [V] |
| CMB（Planck+ACT+SPT） | 0.836 (+0.012/−0.013) | [V] |
| ACT DR6 透镜（ACT 与 Planck 组合） | 0.831 ± 0.023 | [S] |
| eROSITA 星系团计数（cluster counts，Ghirardini et al. 2024） | 0.86 ± 0.01 | [S] |

**修正：** 草案中的 ACT DR6 透镜值 0.840 ± 0.028 无法找到出处，已改为上表数值。

**方法**
- 在统一的 S8 定义下，比较各探针公开的后验分布与链文件（chains）。

### M6 · 银河系外区旋转曲线（L3，contested）

**文献** [V]
- Jiao et al. 2023, A&A 678, A208：19.5 kpc 到 26.5 kpc 之间旋转速度下降约 30 km/s；银河系总质量 2.06 (+0.24/−0.13) × 10¹¹ M☉。
- Ou et al. 2024, MNRAS 528, 693。
- 综述：Melchiorri & Ruchika 2026, arXiv:2608.10189，认为星流（streams）和卫星星系（satellites）等其他示踪体支持更重的暗物质晕（halo）。

**方法**
- 用论文表格中的分箱旋转曲线（binned rotation curve）做约 5 个参数的质量模型拟合。
- 显式加入金斯方程中常被忽略的交叉项（cross-term）等系统误差。

### M5 · 厚盘早期形成（L3，established）

**文献** [V]
- Xiang & Rix 2022, Nature 603, 599, arXiv:2203.12110：约 25 万颗亚巨星；厚盘约在 130 亿年前开始形成。

**数据**
- 更新版星表收录 320,028 颗亚巨星（Xiang et al. 2025），由中国国家天文数据中心（NADC）发布，DOI 10.12149/101467。具体文件大小为 [U]。
- 只下载所需的列。

---

## 已对草案做的修正

| 原草案 | 修正后 |
|---|---|
| BH3 在 DR3 中有轨道解 | 不在 DR3 中，只能用论文表格，或等 DR4 |
| 可以直接下载宽双星星表 | 1.8 GB，必须在服务器端重建样本 |
| GWTC-4.0 数据可以全部下载 | 群体分析数据有 35 GB，只用小文件 |
| MoM-z14 发表于 2025 年 | 发表于 2026 年的 OJAp |
| ACT DR6 透镜 S8 = 0.840 ± 0.028 | 无此出处，改为 0.831 ± 0.023 |
| Gaia DR4 "约 12 月" | 确认为 2026-12-02 |

建议新增并已并入相应里程碑的结果：
- ACT DR6 功率谱（power spectra）与 SPT-3G D1：作为 M1 和 M2 的现代 CMB 先验。
- TDCOSMO 2025：并入 M2。
- eROSITA 星系团计数：并入 M3。
- 中子星候选体：并入 M4。
