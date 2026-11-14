# 012 · 工作计划：M2 哈勃张力——距离阶梯的广义最小二乘复现与校准星系选择（论文研究）

状态：进行中
创建：2026-11-14
待办：T-012（`TODO.md`）

## 1. 目标

按论文立项流程（`paper-study` 技能，计划 007）把 M2 立为研究：

- 用 SH0ES（Supernovae and H0 for the Equation of State of dark energy）公开的矩阵形式数据（数据向量 y、方程矩阵 L、协方差（covariance）矩阵 C；Riess et al. 2022，下称 R22，第 2.1 节式 6）做距离阶梯（distance ladder）的广义最小二乘（GLS, Generalised Least Squares）拟合，复现作者自己的最小二乘解与论文的基线 H0；
- 检验 arXiv:2408.11770（Riess et al. 2024）的论断"超新星子样本的选择解释了 JWST 估计之间的差异"：把阶梯限制在 CCHP（Chicago-Carnegie Hubble Program）的 JWST 样本与只用 NGC 4258 一个锚点（anchor）时，H0 的变化是否与该文一致；以及 CCHP 的选择在随机宿主子样本中是否异常偏低；
- 跨论文一致性：只用论文给出的数值，描述性地比较近邻宇宙测量与早期宇宙（宇宙微波背景（CMB, Cosmic Microwave Background））的预测。

论文（2026-11-14 网页读取，只读；R22 的 arXiv HTML 转换失败，用 PDF 读取）：

| 论文 | 编号 | 期刊 | 版本 |
|---|---|---|---|
| Riess et al. 2022（R22） | arXiv:2112.04510 | ApJL，doi:10.3847/2041-8213/ac5c5b（卷页号待核） | v3 |
| Riess et al. 2024（JWST 复核） | arXiv:2408.11770 | ApJ（已接收） | v2 |
| Freedman et al. 2025（CCHP） | arXiv:2408.06153 | ApJ 985, 182（卷页号待核） | v3 |
| H0DN 合作组 2026（本地距离网络（Local Distance Network）） | arXiv:2510.23823 | A&A 708, A166 | — |
| TDCOSMO 2025（时间延迟透镜（time-delay lensing）） | arXiv:2506.03023 | A&A 704, A63 | v4 |

Lean 论证拟形式化 arXiv:2408.11770 的结论（"Selection of Supernova Subsample Explains Differences in JWST Estimates of Local H0"），以 R22 的距离阶梯为前提。

## 2. 已核实的数字

**R22（PDF 第 9–12、33 页）。** 参数向量 q = (μ0,1 … μ0,nh, ΔμN4258, M^W_H,1, ΔμLMC, μM31, b_W, M^0_B, Z_W, Δzp, 5 log H0)；"The value of H0 is derived from the final entry of q, 5 log H0"，误差取 (LᵀC⁻¹L)⁻¹ 的角元。基线：37 个造父变星（Cepheid）宿主中的 42 颗 Ia 型超新星（SN Ia），哈勃流（Hubble flow）中 0.0233 < z < 0.15 的 277 颗；χ²_dof = 1.03，N = 3445 个自由度；b_W = −3.299 ± 0.015，Z_W = −0.217 ± 0.046，M^W_H,1 = −5.894 ± 0.017，M^0_B = −19.253 ± 0.027；"H0 = 73.04 ± 1.01"（拟合），加上分析变体（analysis variants）的系统误差为 73.04 ± 1.04（式 10）；5 log H0 = 9.318 ± 0.031（含系统误差）。锚点：Gaia EDR3 视差（银河系造父变星）、NGC 4258 的脉泽（maser）、大麦哲伦云（LMC）的食双星（DEB, detached eclipsing binaries）。

**作者公开的最小二乘解**（`lstsq_results.txt`，47 行"值 误差"，无标签）：最后一行 9.32599 ± 0.028，若为 5 log H0 则 H0 ≈ 73.3，与论文的 73.04 不同；有一行为 0.00000 ± 0.000（可能是固定或全零的列）。两者的关系在环节 2 读全文时查明。

**arXiv:2408.11770 表 4（Pantheon+ SN）与第 III.2 节。** HST 全样本、4 个锚点（NGC 4258、银河系、LMC、SMC）：73.17（0.86）；全样本、只用 NGC 4258：72.54（1.54）；CCHP 选出的 11 颗 SN Ia（10 个宿主）、HST 造父变星：71.2，"thus 2.0 … lower than the full HST sample—simply due to the choice of SN hosts and anchor"，由 M^0_B = −19.32 ± 0.05 经该文式 6 的近似 5 log(H0/72.5) = M^0_B + 19.28 得到；表注：子样本误差不含 NGC 4258 距离的 1.1。由表中数字：锚点（4 个 → 只用 NGC 4258）贡献 73.17 → 72.54 = −0.6，宿主选择贡献 72.54 → 71.2 = −1.3。摘要中的"约 2.5"比较的是 CCHP 样本的 JWST 测量与 HST 全样本，与正文的 2.0（同一样本的 HST 造父变星）是不同的比较，并不矛盾。该文的数据版本晚于 R22（多了 SMC 锚点，全样本 73.17 而非 73.04）。

**CCHP（arXiv:2408.06153 v3）。** TRGB（红巨星支顶端（Tip of the Red Giant Branch））：70.39 ± 1.22 (stat) ± 1.33 (sys) ± 0.70 (σ_SN，超新星样本的误差)，24 颗 SN Ia 校准（含 NGC 1316 等没有造父变星的宿主，混合 HST 与 JWST），只用 JWST 的 TRGB 为 68.81 ± 1.79 ± 1.32；零点只用 NGC 4258；哈勃流用 CSP（Carnegie Supernova Project）与 Pantheon+。JWST 样本（表 1，10 个宿主、11 颗 SN Ia）：M101（2011fe）、NGC 1365（2012fr）、NGC 2442（2015F）、NGC 3972（2011by）、NGC 4038（2007sr）、NGC 4424（2012cg）、NGC 4536（1981B）、NGC 4639（1990N）、NGC 5643（2013aa、2017cbv）、NGC 7250（2013dy）。

**其他 H0（km/s/Mpc）。** H0DN 73.50 ± 0.81；TDCOSMO 2025（平直 ΛCDM，即含宇宙学常数的冷暗物质模型（Λ cold dark matter））71.6 (+3.9/−3.3)；Planck 2018 67.4 ± 0.5（arXiv:1807.06209）；SPT-3G + ACT + Planck 67.19 ± 0.38（arXiv:2506.20707，只用 CMB）；ACT DR6 + 透镜 + DESI DR1 重子声学振荡（BAO, baryon acoustic oscillations）68.22 ± 0.36（arXiv:2503.14452，并非只用 CMB）。

## 3. 数据与大小（AGENTS.md 第一条）

`github.com/PantheonPlusSH0ES/DataRelease/SH0ES_Data`：

| 输入 | 文件 | 大小 |
|---|---|---|
| 协方差 C（3492 × 3492，float32） | `allc_shoes_ceph_topantheonwt6.0_112221.fits`，Git 大文件存储（LFS, Large File Storage） | 46.5 MiB（48,781,440 字节，LFS 指针给出；低于 50 MiB 的单次上限） |
| 方程矩阵 L（3492 × 47） | `alll_shoes_ceph_topantheonwt6.0_112221.fits` | 0.66 MB |
| 数据向量 y | `ally_shoes_ceph_topantheonwt6.0_112221.fits` | 17 kB |
| 作者的最小二乘解 | `lstsq_results.txt` | 0.7 kB |

- 合计约 47 MB，低于研究预算 200 MB；全部经 `ctx.http` 取数。
- LFS 文件必须用 `media.githubusercontent.com/media/PantheonPlusSH0ES/DataRelease/main/SH0ES_Data/…` 的直链；`raw.githubusercontent.com` 只返回 131 字节的指针。取数后断言字节数为 48,781,440、SHA-256 等于指针中的 oid（`a42778672d25df7a559bd2949b1e412b99b2e35dd9a36895f6b38828be019172`），否则判为取数失败（含 LFS 流量限额返回的错误页）。
- FITS 数据是大端序 float32，读入后转为本机 float64 再做 Cholesky 分解，并检查 C 的条件数；内存约 100 MB。

## 4. 设计要点与判据方向（预注册写在研究 README 第 2 节，此处只列方向）

- **GLS**：q̂ = (LᵀC⁻¹L)⁻¹LᵀC⁻¹y，协方差 (LᵀC⁻¹L)⁻¹，用 Cholesky 解，不显式求逆；全零或固定的列先删去，并检验约化后的系统满秩（去掉宿主时其 μ 列变为全零，同样删去）。新增 `astrolab/infer.gls` 一个函数，不开新模块。
- **行与宿主的对应**：前 37 个参数是各宿主的距离模数（distance modulus）；把它们与 R22 的宿主距离表（表 6）比对确定列与宿主的对应；某行属于哪个宿主由它在宿主 μ 列中的非零元确定，同时作用于 M^0_B 列的行是该宿主中的超新星。子样本取 y、L 的行与 C 的行列（高斯分布的边缘分布就是 C 的子矩阵）。做不到可靠对应时，相关判据记为"不可评估"。
- **锚点**：只用 NGC 4258 一个锚点的定义按 R22 第 6.2 节的变体（去掉哪些行、是否保留其他锚点的造父变星）在环节 2 读全文后写入预注册。
- **R1（复现）**：主要目标是作者的 `lstsq_results.txt`（同一数据、同一方法，47 个参数及误差应在约 10⁻³ 内一致，是对 `infer.gls` 的精确检验）；次要目标是论文的 H0 = 73.04 ± 1.01，若与作者文件的约 73.3 不同，按环节 2 查明的原因解释，不调参数去凑。
- **R2（arXiv:2408.11770 的移动量）**：比较移动量而不是绝对值（对 R22 与 2024 年数据版本的差别更稳健）：ΔH0（锚点：全部 → 只用 NGC 4258，全样本）对 −0.6；ΔH0（宿主：全样本 → CCHP 的 10 个宿主，只用 NGC 4258）对 −1.3。容差在预注册中按数据版本差与该文式 6 近似的大小给出。
- **R3（宿主选择是否异常）**：在只用 NGC 4258 时，从 37 个宿主中无放回地随机抽 10 个宿主（共计相同的超新星数附近），每次做 GLS，得到 H0 的分布；报告 CCHP 选择所在的百分位。预注册阈值：百分位 < 5% 判为"CCHP 的宿主选择异常偏低"。这一判据回答"差异是否主要来自宿主选择"的一部分；比较对象写明是同一 10 个宿主样本上的 CCHP JWST 结果（arXiv:2408.11770 表 4 中同样本的 NIR-TRGB 70.1、JAGB 等），而不是 CCHP 24 颗超新星的 70.39。
- **探索**：留一宿主（leave-one-host-out）与无放回子抽样代替有放回的自助法（有放回会复制相关的行，使 C 奇异）。
- **跨论文比较（只作描述）**：两两差值除以 √(σa² + σb²) 只对近似独立的组合解释：距离阶梯对 CMB、TDCOSMO 对距离阶梯、TDCOSMO 对 CMB；SH0ES、H0DN、CCHP 之间共用数据，只列出朴素数值并注明"不独立、不作解释"，不做联合平均。早期宇宙的主参考取只用 CMB 的 67.19 ± 0.38，其余只作背景。TDCOSMO 的不对称误差取朝向比较对象一侧。H0DN 与 SH0ES 共用哪些数据在环节 2 读全文核实。

## 5. 环节（每个环节过双闸审查（dual-gate review））

1. **本计划与核实**（ROADMAP M2 的 [S]/[U] 项提升为 [V]）。
2. **Wiki 文章与 Lean 论证**：先用 `python -m astrolab new` 建研究目录，填 `study.yaml` 的 `papers`、`wiki`、`title_zh`、`question_zh`；读 R22 第 4–6 节（宿主表、锚点变体）与 arXiv:2408.11770 全文；查明 `lstsq_results.txt` 与论文基线的关系。
3. **预注册与 GLS 能力**：README 第 1–4 节，`infer.gls` 与不联网测试。
4. **`run.py`、结果、网页**。
5. **独立审稿与收尾**。

## 6. 执行记录

- 2026-11-14：建分支 `feat/m2-hubble-tension`，草稿 PR #12。网页读取子智能体核实第 2 节各数字；SH0ES 数据文件大小来自 GitHub 页面（协方差为 Git LFS 文件，46.5 MB）。用 GitHub API 解码文件内容的命令被自动模式拒绝，改用网页读取。
- 2026-11-14 · 环节 1 闸门 1 第 1 轮：3 个严重问题，均成立并已修改：(1) 71.2 只用 NGC 4258 一个锚点、来自近似式且基于 2024 年的数据版本，改为比较锚点与宿主两步的移动量（−0.6、−1.3）；(2) 复现 71.2 并不检验"差异主要来自宿主选择"，增加随机宿主子样本的百分位检验并写明比较对象是同一样本的 CCHP JWST 结果；(3) R1 的目标含糊：作者文件的最后一个参数约为 73.3 而论文为 73.04，改为以作者文件为主要目标、论文值为次要目标，并处理全零列。同时用本地保存的 R22 PDF 读出第 2.1 节式 6 的参数顺序与第 5 节的基线数值。次要意见采纳：宿主识别方法、LFS 直链与 SHA-256 校验、大端序 float32、有放回自助法的问题、跨论文比较只对近似独立的组合作解释、论文表、环节 2 的建目录步骤、术语补英文、"约 2.5 与 2.0"不是矛盾。
