# 000 · 项目设计原则：agent 驱动的个人电脑天文学研究

- 类型：原则（principles）
- 状态：生效
- 日期：2026-11-11（同日补充第 4 节术语规则）
- 来源：与用户的设计讨论（原始提示见 `/prompts.md`）

## 0. 项目是什么

这是一个面向**真正研究产出**的实验：只依靠编程智能体（coding agent）和一台资源有限的个人电脑，能否进行并推动真正的天文学研究。

知识按 Google Map 的思路组织：
- 初始状态是一个**粗粒度（coarse-grained）的整个宇宙的宏观模型**，相当于世界地图，细节可以模糊。
- 当某个局部需要研究或验证时，**按需补充细节（on-demand detail）**。
- 目标是可验证、可延续、可拓展、可深入，并能复制到同类研究。

## 1. 四条基本原则

### 原则一：个人电脑能跑，不烧硬件

本地只处理 **MB 级**数据，单次运算以**分钟**计。以下不在范围内：
- GB 级下载
- 大规模数值模拟（numerical simulation）
- 原始图像处理（raw image processing）
- 完整的宇宙微波背景（CMB, Cosmic Microwave Background）管线（pipeline）
- 完整的弱引力透镜（weak gravitational lensing）管线

遇到"重"问题，用巧办法：
1. **服务器端计算（server-side computation）**：用天文数据查询语言（ADQL, Astronomical Data Query Language）通过表访问协议（TAP, Table Access Protocol）在数据中心完成筛选、聚合和交叉匹配（cross-match），只下载结果。聚合可以按分层等面积像素化（HEALPix, Hierarchical Equal Area isoLatitude Pixelization）索引分组（`GROUP BY`）。
2. **压缩数据产品（compressed data products）**：例如重子声学振荡（BAO, Baryon Acoustic Oscillations）距离表、压缩似然（compressed likelihood）、距离模数（distance modulus）表、事件参数表、论文表格。
3. **低维推断（low-dimensional inference）**：对少量参数做马尔可夫链蒙特卡洛（MCMC, Markov Chain Monte Carlo）或嵌套采样（nested sampling）。
4. **精选小样本加物理洞察**，代替大样本的暴力计算（brute force）。

缓存（cache）放在**系统缓存目录（system cache directory）**：
- 由 `platformdirs` 确定，在 Windows 上为 `%LOCALAPPDATA%\astrolab\Cache`。
- 有容量上限，可以随时清空重建。
- **绝不放进 Dropbox 同步的项目目录。**

### 原则二：核心库加每个问题一个文件夹，不用 notebook

- `astrolab/` 是小而稳定的核心 Python 库（core library），只加入真正被研究用到的能力。
- 每个研究问题是 `studies/` 下的一个文件夹（study folder），包含：
  - 问题说明
  - 可复现的命令行入口（command-line entry point）
  - 小体积结果
  - **为该问题专门设计的可视化网页（visualization page）**
  - 研究日志（research log）
- 计算与展示分离：脚本产出 `results/*.json`，网页只读这些结果。
- **总览图（Atlas）只是总图**，负责宏观导航。研究网页按实际需要灵活设计，可以做可视化，也可以做交互式数据分析（interactive data analysis），不必拘泥于 Atlas 的形式（2026-11-11 用户补充）。
- 不使用 Jupyter notebook。

### 原则三：面向真正的研究产物

每个结论（claim）都有**等级（grade）**：

| 等级 | 含义 |
|---|---|
| `established` | 已坐实 |
| `tension` | 存在张力 |
| `hint` | 初步迹象 |
| `contested` | 有争议 |
| `refuted` | 被否定 |

另外三条要求：
- **先写假设与判据（hypothesis and decision criteria），再跑分析**，类似预注册（pre-registration）。负面结果（negative result）同样记录。
- 每个数字都能追溯到查询语句、数据版本和获取时间，即来源记录（provenance）。
- 设立独立的审稿人（referee）环节，专门检查系统误差（systematics）和选择效应（selection effects），防止确认偏差（confirmation bias）。

### 原则四：coding agent 是主要的研究与交互方式

项目首先是**写给 agent 读和用的**：
- `CLAUDE.md` 是操作手册。
- `STATUS.md`、各研究的 `README.md` 与 `log.md` 是跨会话（cross-session）的工作记忆。

核心库按 agent 的使用方式设计：
- **命令行优先，输出紧凑**：给摘要，不给整表。
- **先估算再下载**：超过上限即拒绝，并提示收窄查询。

结论复现写成 `pytest` 测试，"结论是否仍成立"可以运行、可以判定。反复出现的研究动作固化为 agent 技能（skill），包括新建研究、文献调研、审稿、复核和出报告。

人负责提出问题、判断方向，并在网页上审阅结果。agent 负责文献、查询、代码、分析、作图、日志与自我质疑。

## 2. 路线图原则：以代表性结果驱动环境搭建

环境不按功能模块搭建，而是**按 2022–2026 年顶刊中最重要、能坐实、能用公开数据验证的结果**排出路线图（roadmap）。每个里程碑（milestone）包括四步：

1. 复现（reproduce）一个代表性结果，借此逼出核心库需要的新能力。
2. 把结论登记进总览图（Atlas），即宏观"世界地图"上的一个坐标，并附上复现值与原文值的对比。
3. 写成测试，持续验证。
4. 留下"开放问题（open questions）"清单，作为真正研究的起点。

入选标准：
- 来自顶刊或大型合作组（collaboration）的正式发布。
- 数据公开，复现所需数据为 MB 级。
- 笔记本电脑上分钟级可复现。
- 等级明确：以 `established` 为地基，少量 `contested` 作为研究前沿（research frontier）。
- 整体覆盖从宇宙学到恒星的不同尺度。

## 3. 尺度分层（"缩放级别"）

| 层级 | 内容 |
|---|---|
| L0 | 宇宙背景：宇宙学参数（cosmological parameters）、膨胀史（expansion history）、CMB |
| L1 | 大尺度结构（large-scale structure）与高红移（high redshift）：BAO、星系分布、早期星系 |
| L2 | 近邻宇宙（local universe）：本星系群（Local Group）、距离阶梯（distance ladder）、哈勃常数（Hubble constant, H0） |
| L3 | 银河系（Milky Way）：结构、运动学（kinematics）、并合史（merger history）、暗物质（dark matter） |
| L4 | 恒星与行星：单星、双星（binary stars）、致密天体（compact objects）、系外行星（exoplanets） |
| X  | 横向（cross-cutting）：时域（time domain）、引力波（gravitational waves）、暂现源（transients） |

空间索引统一使用 HEALPix。

## 4. 语言与术语约定

- 设计文献（design documents）和研究日志（research log）用中文书写。
- **其中出现的任何术语，第一次出现时都要在括号中注明英文原文**，例如：重子声学振荡（BAO, Baryon Acoustic Oscillations）、选择效应（selection effects）。缩写要写出全称。
- 同一文档中术语再次出现时，可以只用中文或缩写。
- 代码、注释、网页、结论条目（claims）使用英文，便于将来发表与工具兼容。
