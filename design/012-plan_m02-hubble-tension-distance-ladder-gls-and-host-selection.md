# 012 · 工作计划：M2 哈勃张力——距离阶梯的广义最小二乘复现与校准星系选择（论文研究）

状态：进行中
创建：2026-11-14
待办：T-012（`TODO.md`）

## 1. 目标

按论文立项流程（`paper-study` 技能，计划 007）把 M2 立为研究：

- 用 SH0ES 公开的矩阵形式数据（数据向量 y、方程矩阵 L、协方差 C；Riess et al. 2022，下称 R22，第 2.1 节式 6）做距离阶梯（distance ladder）的广义最小二乘（GLS, Generalised Least Squares）拟合，复现 R22 的基线 H0；
- 检验"SH0ES 与 CCHP（Chicago-Carnegie Hubble Program）的差异主要来自超新星校准星系（calibrator host）的选择"：把 SH0ES 的造父变星（Cepheid）阶梯限制在 CCHP 的 JWST 样本（10 个宿主星系、11 颗 Ia 型超新星（SN Ia））上重新拟合，与 Riess et al. 2024（arXiv:2408.11770）给出的 71.2 比较；
- 对校准星系做自助法（bootstrap）重采样，看 H0 对宿主样本的敏感度（只作探索）；
- 跨论文的一致性元分析（meta-analysis）：近邻宇宙测量（SH0ES、CCHP、H0DN、TDCOSMO）与早期宇宙（CMB）的张力（tension）统计量，只用论文给出的数值。

## 2. 已核实的数字（2026-11-14，网页读取，只读）

| 测量 | H0 (km/s/Mpc) | 出处 |
|---|---|---|
| SH0ES R22 基线（造父变星—超新星） | 73.04 ± 1.04（含系统误差） | arXiv:2112.04510 摘要；DOI 10.3847/2041-8213/ac5c5b（ApJL；卷页号待从 DOI 页核实） |
| SH0ES HST 全样本（42 SN Ia，4 个锚点（anchor）） | 73.2 ± 0.9（表 4：73.17） | arXiv:2408.11770 摘要、表 4 |
| SH0ES 限于 CCHP JWST 样本（10 宿主、11 SN Ia，HST 造父变星） | 71.2（比全样本低 2.0，"simply due to the choice of SN hosts and anchor"） | arXiv:2408.11770 第 III.2 节、表 4（表注：子样本误差不含 NGC 4258 的 1.1） |
| CCHP，TRGB | 70.39 ± 1.22 (stat) ± 1.33 (sys) ± 0.70 (σ_SN)，24 个 SN Ia 校准 | arXiv:2408.06153 摘要（v3） |
| H0DN 本地距离网络 | 73.50 ± 0.81 | arXiv:2510.23823 摘要；A&A 708, A166 (2026) |
| TDCOSMO 2025（平直 ΛCDM） | 71.6 (+3.9/−3.3) | arXiv:2506.03023 摘要；A&A 704, A63 (2025) |
| Planck 2018（base-ΛCDM） | 67.4 ± 0.5 | arXiv:1807.06209 摘要；A&A 641, A6 (2020) |
| ACT DR6 + Planck/ACT 透镜 + DESI DR1 BAO | 68.22 ± 0.36 | arXiv:2503.14452 摘要（并非只用 CMB） |
| SPT-3G + ACT + Planck | 67.19 ± 0.38 | arXiv:2506.20707 摘要 |

- CCHP JWST 样本（arXiv:2408.06153 表 1）：M101（SN 2011fe）、NGC 1365（2012fr）、NGC 2442（2015F）、NGC 3972（2011by）、NGC 4038（2007sr）、NGC 4424（2012cg）、NGC 4536（1981B）、NGC 4639（1990N）、NGC 5643（2013aa、2017cbv）、NGC 7250（2013dy）。
- 尚未核实（环节 2 读 R22 全文时解决）：R22 式 6 中参数向量 q 的顺序（哪一个是 5 log H0）、宿主与校准超新星的个数、只含统计误差的 H0；CCHP 24 颗校准超新星的完整名单；arXiv:2408.11770 摘要中的"约 2.5"与正文"2.0"的出入。

## 3. 数据与大小（AGENTS.md 第一条）

`github.com/PantheonPlusSH0ES/DataRelease/SH0ES_Data`（GitHub 页面与 API 元数据，2026-11-14）：

| 输入 | 文件 | 大小 |
|---|---|---|
| 协方差 C | `allc_shoes_ceph_topantheonwt6.0_112221.fits`（Git LFS） | 46.5 MB（低于单次 50 MB 上限） |
| 方程矩阵 L | `alll_shoes_ceph_topantheonwt6.0_112221.fits` | 0.66 MB |
| 数据向量 y | `ally_shoes_ceph_topantheonwt6.0_112221.fits` | 17 kB |

合计约 47 MB，低于研究预算 200 MB；经 `ctx.http` 取数（LFS 文件走 `media.githubusercontent.com` 的直链，取数前先用 HEAD 核对大小），缓存在系统缓存目录。其余数字取自论文。

## 4. 设计要点

- **GLS**：q̂ = (Lᵀ C⁻¹ L)⁻¹ Lᵀ C⁻¹ y，协方差 (Lᵀ C⁻¹ L)⁻¹；用 Cholesky 分解解，不显式求逆。H0 由 q 中的 5 log H0 分量换算（参数位置在环节 2 从 R22 原文确定并写入预注册，取数前完成）。README 提到的斜率偏置（初始斜率 −3.285 已扣除）不影响 H0。
- **CCHP 子样本**：从 L 中只保留指定宿主的行与对应参数，其余结构不变；宿主的识别需要 y/L 的行标签——若 FITS 文件不带标签，用 R22 的表与 GitHub 上的说明文件建立对应，并在预注册中写明方法。做不到可靠对应时，该判据记为"不可评估"。
- **元分析**：两两张力 (H0,a − H0,b)/√(σa² + σb²)，近邻测量的加权平均与 χ²；论文之间共用数据（如 SH0ES 与 H0DN 共用造父变星）时不当作独立，只报告两两张力，不做联合平均（或注明）。
- 新增核心能力很少（GLS 一个函数，放入 `astrolab/infer.py`），不单独开模块。

## 5. 环节（每个环节过双闸审查（dual-gate review））

1. **本计划与核实**（ROADMAP M2 的 [S]/[U] 项提升为 [V]）。
2. **Wiki 文章与 Lean 论证**（读 R22 全文，确定参数顺序等待核实项）。
3. **预注册与 GLS 能力**：README 第 1–4 节，`infer.gls` 与不联网测试。
4. **`run.py`、结果、网页**。
5. **独立审稿与收尾**。

## 6. 执行记录

- 2026-11-14：建分支 `feat/m2-hubble-tension`，草稿 PR #12。网页读取子智能体核实第 2 节各数字；SH0ES 数据文件大小来自 GitHub 页面（协方差为 Git LFS 文件，46.5 MB）。用 GitHub API 解码文件内容的命令被自动模式拒绝，改用网页读取。
