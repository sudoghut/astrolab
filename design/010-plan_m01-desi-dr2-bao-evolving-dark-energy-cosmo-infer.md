# 010 · 工作计划：M1 DESI DR2 重子声学振荡与演化暗能量（论文研究；新增核心模块 `cosmo` 与 `infer`）

状态：进行中
创建：2026-11-14
待办：T-004（`TODO.md`）

## 1. 目标

按论文立项流程（`paper-study` 技能，计划 007）把 M1 立为研究：

- 复现 DESI DR2 只用重子声学振荡（BAO, Baryon Acoustic Oscillations）时 ΛCDM 下的 Ωm 与 h·r_d；
- 复现 DESI DR2 加压缩宇宙微波背景（CMB, Cosmic Microwave Background）先验时，演化暗能量模型 w0waCDM 相对 ΛCDM 的偏好（Δχ²_MAP 与等效显著性）；
- 加入超新星（SN, supernova）样本（Pantheon+、Union3、DES-Dovekie），看偏好程度如何随样本变化，并与论文给出的数值对比；
- 为此新增两个核心模块：`astrolab/cosmo.py`（平直宇宙背景演化与 BAO、超新星、CMB 声学尺度可观测量）与 `astrolab/infer.py`（高斯似然、解析边缘化、最大后验（MAP, maximum a posteriori）寻优、emcee 采样、Δχ² 与显著性换算）。

论文：

| 论文 | 编号 | 核实 |
|---|---|---|
| DESI DR2 BAO 宇宙学结果（Abdul-Karim et al. 2025, PRD 112, 083515） | arXiv:2503.14738（读 v3 HTML 全文，含附录 A） | [V] 2026-11-14 |
| DES 超新星 Dovekie 重新校准（Popovic et al. 2026, MNRAS, doi:10.1093/mnras/stag632） | arXiv:2511.07517（读 v3 摘要） | [V] 2026-11-14 |
| DESI DR2 莱曼 α 全形状分析 | arXiv:2607.27410 | [V]（ROADMAP） |

## 2. 已核实的数字（2026-11-14）

- 只用 BAO，ΛCDM：Ωm = 0.2975 ± 0.0086，h·r_d = 101.54 ± 0.73 Mpc，相关系数 −0.92（式 17）。
- 压缩 CMB 先验（附录 A，式 35–36）：均值 (θ*, ωb, ωbc) = (0.01041, 0.02223, 0.14208)；协方差 10⁻⁹ × [[0.006621, 0.12444, −1.1929], [0.12444, 21.344, −94.001], [−1.1929, −94.001, 1488.4]]。来自 Planck PR4 CamSpec 的早期宇宙压缩（Lemos & Lewis 2023，arXiv:2302.12911），已对 ISW 与透镜效应边缘化。
- w0waCDM（表 5、表 6）：
  - DESI + (θ*, ωb, ωbc)_CMB：w0 = −0.43 ± 0.22，wa = −1.72 ± 0.64，Δχ²_MAP = −8.0（2.4σ）（式 24）。**这是本项目能直接复现的组合。**
  - DESI + 完整 CMB：−12.5（3.1σ）；+ Pantheon+：−10.7（2.8σ）；+ Union3：−17.4（3.8σ）；+ DESY5：−21.0（4.2σ）。
  - 不含 CMB：DESI −4.7（1.7σ）；DESI + Pantheon+ −4.9（1.7σ）；DESI + Union3 −10.1（2.7σ）；DESI + DESY5 −13.6（3.3σ）。
  - 显著性换算：2 个自由度的 χ² 分布的累积概率，换算为一维高斯的双侧 Nσ（式 22）。
  - 先验：w0 ∈ U[−3, 1]，wa ∈ U[−3, 2]，并要求 w0 + wa < 0。
- 物理假设：Neff = 3.044，Σmν = 0.06 eV（一个有质量本征态），平直宇宙；r_d 的近似式（式 2）：147.05 Mpc × (ωb/0.02236)^−0.13 × (ωbc/0.1432)^−0.23 × (Neff/3.04)^−0.1。
- Dovekie：DES-Dovekie + CMB + DESI DR2 的偏好为 3.2σ（DES-SN5YR 为 4.2σ）；w0 = −0.803 ± 0.054，wa = −0.72 ± 0.21。

## 3. 数据与大小（AGENTS.md 第一条）

文件大小来自 GitHub API 的元数据（不下载），2026-11-14：

| 输入 | 来源 | 大小 |
|---|---|---|
| DESI DR2 BAO 均值与协方差（ALL） | `CobayaSampler/bao_data/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_{mean,cov}.txt` | 0.5 kB + 2.5 kB |
| DESI DR2 分示踪体（tracer）文件（留一法探索用） | 同目录，8 组 | 共约 10 kB |
| Pantheon+ | `CobayaSampler/sn_data/PantheonPlus/`：`Pantheon+SH0ES.dat`、`Pantheon+SH0ES_STAT+SYS.cov` | 0.58 MB + 33.3 MB |
| Union3 | `sn_data/Union3/`：`lcparam_full.txt`、`mag_covmat.txt` | 2 kB + 9 kB |
| DES-Dovekie | `sn_data/DES-Dovekie/`：`DES-Dovekie_HD.csv`、`covtot_inv_000.npz` | 0.11 MB + 6.2 MB |
| **不取**：DES-SN5YR 协方差 `covsys_000.txt` | `sn_data/DESY5/` | **53.5 MB，超过单次 50 MB 上限**；Dovekie 是它重新校准后的版本，以 Dovekie 代替 |

合计约 40 MB，低于研究预算 200 MB；全部经 `ctx.http` 取数并缓存在系统缓存目录，不写入项目目录。CMB 部分只用附录 A 的 3 维高斯先验（写在代码里，不取数）。

## 4. 设计要点

- **`cosmo`**：平直 w0waCDM 背景（CPL 参数化 w(a) = w0 + wa(1 − a)），含光子、三种中微子（两种无质量、一种 0.06 eV 有质量，用数值积分求有质量中微子的能量密度）；D_M、D_H、D_V；r_d（近似式 2，并用声速积分交叉核对）；θ* = r_s(z*)/D_M(z*)，z* 用 Hu & Sugiyama 1996 的拟合公式。精度验收：用 Planck 2018 最佳拟合点（ωb = 0.02237，ωc = 0.1200，H0 = 67.36）复算 100θ* 并与 1.04110 比较，差异须小于 CMB 先验 σ 的 0.3 倍；否则改用对 θ* 的经验修正并在预注册中写明。
- **`infer`**：高斯似然；超新星绝对星等的解析边缘化；MAP 用多起点的 scipy 寻优；后验用 emcee；Δχ²_MAP → Nσ（2 个自由度）。
- **复现判据**（预注册写在研究 README 第 2 节，此处只列方向）：R1 只用 BAO 的 Ωm 与 h·r_d；R2 DESI + 压缩 CMB 的 Δχ²_MAP、w0、wa；R3 加超新星后偏好程度的排序（Union3 > Pantheon+；Dovekie 低于 DESY5 的 4.2σ），因为论文的 +SN 数值用的是完整 CMB，我们只用压缩先验，判据只比较方向与大致数值，容差在预注册中写明。
- **探索**（对话探索入口）：逐一剔除示踪体（留一法）、换超新星样本、换 w(z) 参数化。

## 5. 环节（每个环节过双闸审查）

1. **本计划与 ROADMAP 核实**（[S] → [V]）。
2. **Wiki 文章与 Lean 论证**：`docs/wiki/Study-002-desi-bao-evolving-dark-energy.md`（第一至三部分），`studies/002-…/argument/`。
3. **预注册与核心模块**：研究 README 第 1–4 节；`astrolab/cosmo.py`、`astrolab/infer.py` 及不联网测试（含 θ* 精度验收）。
4. **`run.py`、结果、网页**：取数、运行、`test_conclusions.py`、`web/index.html`、结论条目（claim）。
5. **独立审稿与收尾**：审稿、Wiki 第三部分回写、README 第 8 节、STATUS、DONE。

## 6. 执行记录

- 2026-11-14：建分支 `feat/m1-desi-bao`，草稿 PR #10。核实：Dovekie（arXiv:2511.07517 v3 摘要：3.2σ，由 4.2σ 降低，MNRAS 2026）；`CobayaSampler/sn_data` 目录与文件大小（GitHub API 元数据）；DESI DR2 正文表 4–6、式 2、14–28 与附录 A 式 35–36（arXiv HTML v3，网页读取子智能体与无头浏览器只读读取，未保存到项目目录）。发现 DES-SN5YR 协方差 53.5 MB 超过单次下载上限，以 Dovekie 代替。
