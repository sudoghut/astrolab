# M4：Gaia 休眠黑洞——DR3 复现与面向 DR4 的筛选

> English: [README.md](README.md)。以英文 `README.md` 为准（预注册与判据的权威文本）；本文件是它的中文译本，节号与表格一一对应，英文改动时在同一个 PR 中同步修改。 网页在线版：[https://sudoghut.github.io/astrolab/studies//web/](https://sudoghut.github.io/astrolab/studies//web/)。

> 第 1–4 节写于 2026-11-11，在 run.py 之前（预注册，pre-registration）。
> 此后对这几节的修改必须附带注明日期的说明。

## 1. 问题

1. 仅凭 Gaia DR3 NSS（Non-Single Stars，非单星）天体测量轨道（astrometric orbits）（不做视向速度（RV, radial velocity）后续观测），能否复现
   El-Badry et al. (2023a,b) 发表的 Gaia BH1 与 BH2 暗伴星（dark companion）质量？
2. 对全部 DR3 天体测量轨道解做完全在服务器端的筛选（screen），能否找回
   已知的休眠致密天体（dormant compact objects）（BH1、BH2，以及 El-Badry et al. 2024 的 21 个中子星候选体（neutron-star candidates）），
   同时只下载 MB 量级的数据？
3. 这一筛选能否只改一个参数，就在 Gaia DR4（2026-12-02）上运行？

## 2. 假设与判据

**R1（BH1）。** 源 4373465352415301632 的 DR3 `Orbital` 解，取
M1 = 0.93 +/- 0.05 Msun（El-Badry et al. 2023a, Sec. 2.1），给出的 M2 与
发表值 9.62 +/- 0.18 Msun 相符：|M2_ours - 9.62| < 2 sigma_combined。

**R2（BH2）。** 源 5870569352746779008 的 DR3 `AstroSpectroSB1` 解，取
M1 = 1.07 +/- 0.19 Msun（El-Badry et al. 2023b, Sec. 3.5），给出的 M2 在 2 sigma 内与
8.9 +/- 0.3 Msun 相符。*事先记下的预期：* DR3 周期
（1352 +/- 45 d）与视向速度约束的 1277 d 不同，所以出现中等程度的偏差并不
意外；如果 R2 不通过，我们报告偏差及其原因，而不是调参。

**S1（筛选规模与黑洞找回）。** 服务器端筛选返回 < 50,000 行
（< 20 MB），并且用各自发表的 M1 时，BH1 与 BH2 都以 M2 > 3 Msun 出现。

**S2（中子星候选体召回率，recall）。** El-Badry et al. (2024) 的 21 个候选体中至少 19 个
（>= 90%）通过服务器端预选（pre-selection）（`f_M > 0.25 Msun`）。召回率低于此值
意味着预选对 DR4 来说过于激进，必须放宽。

**S3（新候选体，探索性）。** 以 Gaia FLAME（`astrophysical_parameters.mass_flame`，缺失时取 1 Msun）
估计 M1 时 M2 > 3 Msun 的解的数目，不带先验预期地报告。每个解都打上标签：已知（文献）/ 可能
虚假（质量标志，quality flags）/ 无法解释。本研究不作任何发现声明（discovery claim）。

**D1（DR4 就绪，DR4 readiness）。** 同一套代码对 `release="dr4"`（schema
`gaiadr4`）生成有效的 ADQL（Astronomical Data Query Language，天文数据查询语言），并对 `release="dr3"` 端到端运行。
*说明 2026-11-14（设计计划 008）：* 现在的检查使用 `screen.SCHEMAS` 中映射到 `dr4` 的 schema
（除非发布日显示另有名称，否则为 `gaiadr4`），而不是写死的名字；D1 的
含义不变。D1 是 DR3 运行的判据，在 DR4 运行中为"不适用"。

### 第 2 节的 DR4 补充（2026-11-14，写于 DR4 发布之前；预注册）

只在 DR4 运行（`PARAMS["release"] = "dr4"`）上评估。上面的 DR3 判据不
改变，继续对照 `results/dr3/` 中归档的 DR3 结果检查。所有 DR4
判据都由 `run.py` 计算（设计计划 008），不在发布当天手工计算。

**下文使用的定义。**
- *信息屏障（information barrier）*：下面的发布日决定（天体测量类型、未验证类型、
  `covariance_trusted`、用于 `epoch_gap_yr` 的 DR4 参考历元（reference epoch），以及——说明 2026-11-14，
  发布之前——视向速度幅度列和 DR3-DR4 交叉匹配（cross-match）表的说明，或
  "未发布"）只根据元数据和文档作出（TAP_SCHEMA、
  服务器端的类型计数、只返回每种类型计数的聚合查询、DR4 数据模型
  与发布论文；不查看任何源级（source-level）的行或数值），记录在 `log.md` 中，并在
  获取任何源级 DR4 数据（目标、对照、幸存者（survivors）、筛选）之前提交
  `PARAMS` / `RELEASES` / `screen.py` 的改动。看到这些数据之后再改动这些决定，
  必须作为事后（post-hoc）改动报告。
- *天体测量类型（astrometric types）*：机械地定义为服务器端计数
  `SELECT nss_solution_type, COUNT(*), COUNT(a_thiele_innes) ... GROUP BY nss_solution_type` 中
  带有 Thiele-Innes 常数（COUNT(a_thiele_innes) > 0）的 DR4 解类型；`screen.py` 中的 `ASTROMETRIC_TYPES["dr4"]`
  （自 2026-11-14 起每个发布版本一份列表，因此 DR3 查询不受影响）恰好设为这份列表
  （运行手册第 1 步）。
- *未验证类型（non-validated types）*：`PARAMS["unvalidated_types"]`。对 DR4 而言，指
  DR4 文档（数据模型或发布论文）描述为未经验证或可靠性较低的解类型，
  根据文档决定，在获取审核（vetting）查询之前写入 `log.md` 和 `PARAMS` 并注明日期。
  改动这个正式参数就是改动本预注册，并按此记录。
- *解析（resolution）*：一个 DR3 source_id "可解析"，是指它出现在 DR4 `gaia_source` 中且通过
  身份核对；否则，如果 DR4 发布了 DR3-DR4 交叉匹配（邻域，neighbourhood）表，且该表
  把它映射到某个 DR4 源（取角距离最小的邻居；两个邻居的角距离相差不超过 0.1 arcsec，
  或身份核对失败，都视为无匹配），则也算可解析；此时使用映射得到的
  DR4 id。身份核对：对照为本研究用到的全部 109 个 DR3 id（87 个 M2 > 3 Msun 的 DR3 行、
  21 个中子星候选体、BH3 和带文献标签的源；`results/dr3/reference_ids.json`）归档的 DR3 位置和 G 星等，
  把 DR3 位置用 DR4 自行（proper motion）推算到 DR4 参考历元（DR4 没有自行时不推算），
  偏差 < 2 arcsec 且 |G_DR4 - G_DR3| < 0.3 mag。不可解析的源报告为
  `unresolved`（未解析），并写明原因（未找到 / 有歧义：同一 id 有多行 / 位置偏差 / 星等），
  并且永远不计为
  科学结果。大幅度变星巨星（variable giants）可能通不过星等核对；这种偏差倾向于
  `unresolved`，并报告其数目。
- *缺失数据*（说明 2026-11-14，设计计划 008，发布之前）：FLAME 值为
  NULL、发布版本缺少 FLAME 列、以及 FLAME 值有歧义（同一源有多行
  FLAME）都算作缺失。缺少 `gaia_source` 或 `astrophysical_parameters` 表（或
  TAP_SCHEMA 查询两者都未列出）时，在获取任何源级数据之前停止运行：
  这需要一个在信息屏障下记录的发布日决定。
- *主解（primary solution）（R-sel）*，对每个源处处适用（目标、对照、幸存者、新
  候选体）：在该源的天体测量类型解中，已验证优先于
  未验证；其中 `AstroSpectroSB1` 优先，其次 `Orbital`，再次其他类型；平局时
  依次取 `significance` 最高者、|`goodness_of_fit`| 最小者、字典序
  最小的 `nss_solution_type`、最小的 `period`、再按 Thiele-Innes 常数 A、B、F、
  G 升序（缺失值排在最后；这些量全部相同的行视为同一个解），因此选择
  从不依赖行的顺序。所有解都会保存；
  判据使用主解。
- *否决（vetoes）*：(i) 类型否决：主解属于未验证类型；(ii) 视向速度否决：DR4
  `rv_amplitude_robust` < `PARAMS["rv_ratio_min"]`（0.5）x 由主轨道预测的
  视向速度最小到最大范围（2K，其中 cos i = (AG - BF)/a0^2，与第 5 节相同）。在 DR4 上，视向速度否决只在
  P < 1000 d（在约 66 个月的 DR4 基线（baseline）内至少两个轨道周期）且 e < 0.8（短暂的
  近星点尖峰可能落在稀疏的视向速度历元之间）、并且该列存在时才适用；否则
  为"不适用"，绝不算否决。偏心率缺失意味着伪圆（pseudo-circular）解，Gaia 对其固定
  e = 0（说明 2026-11-14，发布之前；DR3 代码在这种情况下已经使用 e = 0）。即便在这些限制之内，采样稀疏的轨道也可能显示
  比预测更小的范围，所以视向速度否决是证据，不是证明。如果 DR4 给该列改名，
  就使用其文档中定义相同的后继列（`RELEASES[...]["rv_amplitude_column"]`；
  配置的列名不在 TAP_SCHEMA 中时停止运行，以免拼写错误把否决关掉），在审核查询之前
  决定并记录在 `log.md` 中（与类型列表一样）；如果没有后继列，视向速度否决不适用。
- *不确定度（uncertainties）*：`run.py` 中 `RELEASES` 的 DR4 条目在发布日
  只凭文档（DR4 数据模型，或 DPAC（Data Processing and Analysis Consortium，数据处理与分析联盟）面向 DR4 发布的 `nsstools`）
  确认 `corr_vec` 参数顺序（运行手册第 1.5 步）之前，`covariance_trusted = False`，并在
  第一次正式 DR4 运行之前记录这一改动；为 False 期间，R1-R3 为"无法评估"，只报告
  中心值。如果在任何一次正式 DR4 运行之后才改动它，较早那次运行也一并报告。
  信息屏障之后，对 BH1 的 `corr_vec` 长度检查只能把它改回 False（并报告），
  绝不能改为 True。
  `RELEASES` 是本预注册的一部分：对它的任何其他改动都按此记录。

**R1-DR4、R2-DR4。** 规则与 DR3 相同（|M2_ours - M2_paper| < 2 sigma_combined），使用
BH1 与 BH2 的 DR4 主解和第 2 节的 M1 值。没有 DR4 解或未解析：
"无法评估"。R1b（与已发表的仅 DR3 解比较）是只针对 DR3 的检查，
不在 DR4 上评估。

**R3（BH3）。** 如果 BH3（4318465066420528000）可解析且有天体测量类型的 DR4 解，
M1 = 0.76 +/- 0.05 Msun（Gaia Collaboration, Panuzzo et al. 2024, arXiv:2404.10486v2, Table 3）
给出的 M2 与发表值 32.70 +/- 0.82 Msun 相符：|M2_ours - 32.70| < 2 sigma_combined。
没有 DR4 解："无法评估"，不算失败。
*事先记下的预期：* 发表的质量来自同一流水线（pipeline）在相同约 66 个月数据上的
发布前运行（NSS 4.1），使用天体测量 + 视向速度联合（`AstroSpectroSB1`）
解：f_M = 31.23 +/- 0.81 Msun，P = 4253.1 +/- 98.5 d。对 `AstroSpectroSB1` 解而言，我们的
f_M = (a0/parallax)^3 / P^2 与他们基于 a1 的 f_M 是同一个量（该解的视差为 a0/a1），
因此不预期有方法上的偏差；他们的仅天体测量解给出 f_M =
32.03 +/- 0.64 Msun，主要由于周期较短（4194.7 d），会使 M2 高出约
0.8 Msun。因此 R3 是检验 NSS 4.1 与最终 DR4 流水线之间的一致性，
不是一次独立测量。

**S1-DR4。** DR4 筛选返回 < 50,000 行（先在服务器端计数；>= 50,000 时 S1-DR4
不通过，不获取筛选结果，依赖筛选的 S3-DR4 为"无法评估"，其余照常
计算；此后再跑的收紧筛选属于事后，其 S3 数字
绝不作为预注册结果解读），并且 BH1、BH2、BH3 中每个可解析且有
DR4 解的目标，用其发表的 M1 在主解上得到 M2 > 3 Msun；缺失的目标在这一部分中
列为"无法评估"。这一部分要通过，3 个目标中至少 2 个必须可评估；少于 2 个时，S1-DR4 为"无法评估"（绝不因缺数据而算通过）。

**S2-DR4。** 在 El-Badry et al. (2024) 的 21 个候选体中，N_eval 是可解析且有
天体测量类型 DR4 解的那些；候选体的主解满足筛选
切割（天体测量类型、视差信噪比（S/N, signal-to-noise ratio）> 5、f_M > 0.25 Msun；含义与 DR3 上的 `in_screen` 相同）即算通过，
在获取的解上评估，因此 S2-DR4 不依赖于获取筛选结果。
通过：N_eval >= 15 且通过数 >= ceil(0.9 N_eval)。N_eval < 15："无法评估"。星表
召回率（21 个中有多少有任何 DR4 解）单独报告。与 DR3 一样，这项检验
很弱（DR3 上最弱的 f_M 为 0.41，切割为 0.25）。

**V-DR4（对照上的否决）。** 对照（controls）：BH1、BH2、BH3 与 21 个中子星候选体。对照的主解
被 (i) 或 (ii) 否决时，该对照即被否决。没有 DR4 解或
未解析的对照列出但不计数；N_ctrl 是计入的数目。通过：N_ctrl >= 15 且计入的对照
无一被否决；N_ctrl < 15："无法评估"。同时报告视向速度否决适用的计入对照数目
（DR3 上为 23 个中的 4 个）：少于 5 时，检验的视向速度部分
报告为弱。对照被否决意味着否决规则在 DR4 上失效；予以报告，不
重新调参。

**F-DR4（51 个 DR3 幸存者）。** 51 个既非已知、未被否决、
也未被驳倒的 DR3 候选体，每个恰好得到一个标签，取第一个适用者：
1. `unresolved`（见"解析"）；
2. `solution-gone`：没有天体测量类型的 DR4 解；
3. `type-vetoed`：主解属于未验证类型；
4. `insufficient`：主解的视差 <= 0 或视差信噪比 <= 5，或缺少
   周期、周期误差或 a0（DR4 主解的，或归档 DR3 值的；说明
   2026-11-14，发布之前）；
5. `rv-vetoed`：视向速度否决适用且触发；
6. `mass-below`：M2 <= 3 Msun，其中 M1 = DR4 FLAME `mass_flame`（若对该源是有限数值；缺列或
   NULL 值算作缺失），否则取 DR3 的 `m1_used`；
7. `period-changed`：|P_DR4 - P_DR3| >= 3 sqrt(sigma_P,DR3^2 + sigma_P,DR4^2)；
8. `persists`：以上都不符合。
另外报告、但不用于打标签的：P_DR4/P_DR3（接近 0.5 或 2 的值标记为可能的
混叠（aliases））与 a0_DR4/a0_DR3。P_DR3 > ~1000 d（超出 DR3 基线）时周期检验很弱。
结果是各标签的计数，以及视向速度否决适用的幸存者数目
（51 个中有 28 个 P_DR3 > 1000 d，对它们来说 `persists` 只依赖周期和质量）。不作
发现声明：`persists` 的意思是"仍是候选体"。

**S3-DR4（新候选体，探索性）。** 成员资格：至少有一条
M2 > 3 Msun（FLAME M1，缺失时取 1 Msun）筛选行、且解析之后不属于 87 个 M2 > 3 Msun 的 DR3 行的 DR4 源。
它们的主解在其全部 DR4 解中选择（为这些源专门获取，不只是筛选行）；
标签、否决和报告的"主解 M2 > 3"计数都使用
主解。它们的 id 完整保存（放在各自的结果文件中，使每个文件都在 1 MB 以下）。对照
DR3 之后发表的文献（包括 Gaia DR4 发布论文）核查它们。没有先验
预期，也不作发现声明。

## 3. 数据（附大小估计）

| 输入 | 来源 | 选择条件 | 预估行数 / 大小 |
|---|---|---|---|
| BH1、BH2 的完整 NSS 行，含 `corr_vec` | `gaiadr3.nss_two_body_orbit`（TAP gaia） | 3 个 source_id | 2 行，< 10 kB |
| 黑洞坐标/测光 | `gaiadr3.gaia_source` | 3 个 source_id | 3 行 |
| 筛选 | `nss_two_body_orbit` JOIN `gaia_source` LEFT JOIN `astrophysical_parameters` | 天体测量轨道类型，`parallax_over_error > 5`，`f_M > 0.25`（在 ADQL 中计算） | 先用 COUNT 核对；预计 10^3-10^4 行，< 5 MB |
| 中子星候选体 | El-Badry et al. 2024 Table 1（21 个 source_id、M2、P） | 从 arXiv:2405.00089v2 HTML 版转录 | 21 行，在 `ns_candidates_elbadry2024.json` 中 |

*说明 2026-11-14（设计计划 008）：* DR3 重跑增加一项输入，即本研究用到的
109 个 DR3 id 的 DR3 位置和 G（`gaiadr3.gaia_source`，< 200 行，< 50 kB），归档为
`reference_ids.json`，用于 DR4 身份核对。

DR3 表共有约 443k 个解；我们从不下载它。质量
函数（mass function）在服务器端计算。

### 第 3 节的 DR4 补充（2026-11-14，DR4 发布之前）

| 输入 | 来源 | 选择条件 | 预估行数 / 大小 |
|---|---|---|---|
| DR4 的 schema、表、列、解类型 | `TAP_SCHEMA`；对 `nss_two_body_orbit` 做 GROUP BY | 元数据 | 每项 < 1,000 行 |
| DR3 id 的解析 | DR4 `gaia_source`（以及已发布时的 DR3-DR4 交叉匹配表） | 109 个不重复的 DR3 source_id（87 个 M2 > 3 的 DR3 行，含 BH1、BH2 与 51 个幸存者；21 个中子星；BH3；带文献标签的源） | < 300 行 |
| 筛选候选体的全部解（S3-DR4，以及 DR4 候选体表的否决列） | DR4 `nss_two_body_orbit` JOIN `gaia_source` LEFT JOIN `astrophysical_parameters`，按 id 分块，每块 <= 500 | 有 M2 > 3 筛选行、且尚未作为目标、对照或已解析 id 获取过的源 | 先在服务器端计数；预计几 x 10^3 行。停止规则：超过 50,000 行（约 15 MB，按每行约 300 字节）时 S3-DR4 为"无法评估"，什么也不获取；不做事后收窄。无论如何其上限为筛选行数（< 50,000 行）乘以每个源的解数 |
| 目标、对照与幸存者的解 | DR4 `nss_two_body_orbit` JOIN `gaia_source` LEFT JOIN `astrophysical_parameters` | 已解析的 id | < 500 行 |
| 筛选 | 与 DR3 相同的查询，用于 DR4 schema | 相同的切割 | 发布日计数；DR3 为 3,343。超过 50,000：S1-DR4 不通过并首先记录（运行手册第 2 步） |
| DR3 参考值 | `results/dr3/`（归档的 DR3 运行：周期及其误差、a0、所用 M1；`reference_ids.json` 含 109 个 id 的 DR3 位置和 G，在 2026-11-25 之前的 DR3 重跑中获取） | 已提交的文件 | < 1 MB |

发布日的计数及其大小估计（行数 x 约 300 字节）在获取筛选结果之前
写入此表。结果文件保持在 1 MB 以下（AGENTS.md 第 1 节）：筛选很大时，
`run.py` 会对筛选点做抽稀（设计计划 008，第 2.4 节）。

## 4. 方法

- 由 Thiele-Innes 常数求 a0（DR3 文档式 7.15）；对于没有 G 的伪圆解，
  在筛选查询中通过 COALESCE 使用 G = -AF/B（DR3 文档）。
- f_M = (a0 / parallax)^3 / P_yr^2 假定伴星是暗的（光心（photocentre）=
  主星）。发光的伴星会缩小光心轨道，因此在那种情况下这个 M2 是
  下限；三体系统（triple）可以伪装成大质量暗伴星。
- M2 由 M2^3 = f_M (M1 + M2)^2 求解。
- 不确定度（R1、R2）：对由 `corr_vec` 按官方 `nsstools` 顺序重建的
  (parallax, A, B, F, G, P) 完整协方差（covariance）做蒙特卡罗（Monte Carlo）抽样
  （已用单元测试对照 nsstools 核实），并取 M1 ~ N(M1, sigma_M1)。
- 筛选：逐行计算 M2 中心值，M1 取自 FLAME（缺失时标记；有条件时用
  绝对星等和 FLAME 半径标记巨星）。

### 第 4 节的 DR4 补充（2026-11-14，DR4 发布之前）

- 方法不变；发布版本是参数 `PARAMS["release"]`（设计计划 008）。DR4 上使用的否决
  和解的选择在第 2 节补充中定义。
- 正式运行拒绝覆盖另一发布版本未归档在
  `results/<release>/` 中的结果（两个方向都如此）。
- DR4 类型名称、未验证类型和 `corr_vec` 顺序（`covariance_trusted`）在
  发布日确认（运行手册第 1.4-1.5 步），并在第一次正式 DR4 运行之前记录。

## 5. 结果（2026-11-11）

预注册判据：

| | 结果 | 判定 |
|---|---|---|
| R1 | BH1：M2 = 13.3 +2.9/-2.3 Msun（仅 DR3 天体测量）对比 9.62 +/- 0.18（天体测量 + 视向速度）：+1.4 sigma | 通过（检验功效低，见 s6） |
| R2 | BH2：M2 = 8.52 +0.61/-0.56 Msun 对比 8.9 +/- 0.3：-0.6 sigma | 通过 |
| S1 | 169,227 个天体测量解中的 3,343 行（0.4 MB）；用发表的 M1，BH1 M2 = 12.8，BH2 M2 = 8.5（> 3） | 通过 |
| S2 | 21/21 个中子星候选体通过 `f_M > 0.25`（最弱 f_M = 0.41） | 通过（弱检验，见 s6） |
| S3 | 87 个 M2 > 3 Msun 的解：2 个已知；5 个没有预注册标签 | 报告 |
| D1 | 已生成 DR4 ADQL（`results/dr4_screen_query.json`）；schema 名称待发布日确认 | 通过（仅生成） |

事后补充（在独立审稿之后，**不是**预注册的；在网页上以 * 标记）：

- **R1b**：对照 El-Badry et al. 2023a 自己的*仅天体测量*解（a0 = 3.00 +/- 0.22 mas，
  M2 = 12.8 +/- 2.0 Msun），我们得到 a0 = 3.02 mas（+0.09 sigma）和 M2 = 13.3 Msun（+0.23 sigma）。
- 由天体测量轨道得到的**预测视向速度范围**（2K，其中 cos i = (AG - BF)/a0^2）与
  El-Badry et al. Table E1 中列出的全部六个源相符（例如 167 对比 171 +/- 10，49 对比 50 +/- 2 km/s）。
- **否决**：(i) 未验证的 `OrbitalAlternative`/`OrbitalTargetedSearch` 解；(ii)
  `rv_amplitude_robust` < 0.5 x 预测视向速度范围。在 23 个阳性对照（positive controls）（BH1、BH2、21 个中子星）上：
  0 个被否决——但 23 个中只有 4 个有 `rv_amplitude_robust`，所以否决 (ii) 在阳性样本上的检验很弱。
- 在有 `rv_amplitude_robust` 的情况下，否决 (ii) 在每一例中都与文献结论一致
  （否决 3640889032890567040、6281177228434199296、3664684869697065984；保留 BH2）。
- 经过否决与文献比对之后：**剩下 51 个未知候选体，全部是巨星和/或低显著性
  解；没有未加标签的主序（main-sequence）宿主星幸存。** 不声称任何发现。
- 4 个经审核的源有不止一个 NSS 解；现在的连接（join）使用 (source_id, nss_solution_type)。
- *说明 2026-11-14（设计计划 008）：* 从现在起，对照的主解
  （R-sel，第 2 节的 DR4 补充）被否决时才算该对照被否决，DR3 与 DR4 一样，而不是它的任何一行
  被否决即算。在 DR3 上这不改变任何数字：没有对照行被否决，BH1/BH2 各只有一个解。
- 服务器端计算中因 a0 为 NULL 丢失的行为 0。

## 6. 审稿意见（独立子智能体，2026-11-11）

审稿报告的处置（triage）（已核实 = 我们对照代码、结果或论文原文检查过）：

| # | 要点 | 已核实 | 处理 |
|---|---|---|---|
| 1 | 预注册的质量控制（qc）标签打中了两个真实黑洞（BH1 `low-significance`，BH2 `giant`）；`significance<20` 在 OA 行上从不触发 | 是 | 作为教训接受：标签在使用前必须在阳性对照上验证（现已对否决这样做）。 |
| 2 | 对巨星用 FLAME M1 会高估 M2；巨星的 3-4 Msun 主序伴星会被掩盖，所以对巨星而言 M2 > 3 不是黑洞特征 | 是 | 作为局限接受；巨星单独作为一类报告。 |
| 3 | 按书面写法的 S1（"发表的 M1"）不是代码实际评估的内容 | 是 | 已修正：S1 现在使用发表的 M1。 |
| 4 | R1 功效很低（sigma_comb ~ 2.6 Msun），且比较对象是联合拟合 | 是 | 增加 R1b，对照已发表的仅 DR3 解（事后）。 |
| 5 | S2 不可能不通过（最弱 f_M 0.41） | 是 | 接受；已记录。S2 不能说明该切割适合 DR4。 |
| 6 | 6281177228434199296 已被视向速度后续观测排除（El-Badry+23a App. E） | 是（论文原文） | 已加入文献标签（`data/literature_vetting.json`）。 |
| 7 | OA 解大多是虚假的；周期位于 63 d 进动（precession）的谐波上 | 部分（OA 的说法由审稿人引自 Arenou+23 / Holl+23；我们未读原文） | 事后加入类型否决，已在对照上验证。未采用周期混叠否决（没有经过验证的规则）。 |
| 8 | 没有针对三体系统的 AMRF（astrometric mass ratio function，天体测量质量比函数）处置；低信噪比下的视差（Eddington）偏差；P > 基线 | 是 | 列入开放问题（s7）。 |
| 9 | D1 未评估；169,227 写死在代码中 | 是 | 已修正：D1 字段 + 完整的 DR4 查询；计数现在来自服务器。 |
| 10 | 不加截断的 ADQL SQRT 可能丢行 | 是 | 已测量：丢失 0 行；保留为一项测试。 |

### 6b. 论证审稿（Lean 论证与 Wiki 文章，2026-11-14，T-010）

一个独立子智能体看了三篇论文、`argument/Argument.lean` 以及来自 `tests/test_lean_arguments.py` 的引文—类型—内容对照表，
没有看我们的文章。处置：

| # | 要点 | 已核实 | 处理 |
|---|---|---|---|
| 1 | 共用一个阈值"质量 >= 5 Msun"，使 BH2 与 BH3 的引文（关于约 8.9 和 32.7 Msun 的伴星）承载了它们并未讨论的质量的断言；BH1 的摘要写的是"> 5" | 是 | 按系统分设阈值：BH1 `> 5`、BH2 `>= 8.0`、BH3 `>= 30` Msun；NUM 绑定现为 `> 5.0`。 |
| 2 | `mod_ns3` 强于其引文：BH3 那句话只排除了中子星，没有排除白矮星 | 是 | `mod_ns3` 现在的结论是 `NoNS3`；新增 `lit_wd3`（LIT [implied]，钱德拉塞卡极限（Chandrasekhar limit））把它推到 BH3。 |
| 3 | `mod_fit3` [stated] 涵盖的是方法，而不是从估计值到界限的那一步 | 是 | `mod_fit3` 改为 [implied]，与 `mod_fit1`/`mod_fit2` 一样。 |
| 4 | BH1 质量的几条"多余"路径都依赖同一批后续视向速度 | 是 | 文章说明：多余性是指对去掉单个前提的稳健性，而不是对视向速度数据本身问题的稳健性。 |
| 5 | `num_astro1` 是多余的，并且绑定的是一个低显著性 DR3 解的中位数 | 是 | 已在文章中说明；没有任何 Lean 判定依赖于它。 |
| 5b | （来自对修正的审查）`lit_wd3` 缺少 `NoStar3`；`mod_dark2` 的引文只提到一颗 9 Msun 的单星 | 是 | `lit_wd3` 加上 `NoStar3`；`mod_dark2` 改为 [implied]（质光关系，mass-luminosity relation）。 |
| 6 | 次要措辞（`Faint2` 的范围、BH3 结论的引文、`lit_ns1` 中子星最大质量 2.3-2.5 Msun） | 是 | 已修正。 |

修正后的判定：`explicit_insufficient`（GAP `gap_few3`）、`stated_insufficient`，8 个 BH1 质量路径
前提为多余。

## 7. 开放问题

- DR4 发布日（2026-12-02）：通过 TAP_SCHEMA 确认 schema，运行筛选与否决，并
  用 DR4 历元天体测量/视向速度检验 51 个幸存（巨星 / 低显著性）候选体。
- 加入 AMRF 处置（Shahaf et al.），区分三体系统与发光伴星；在对照上验证。
- 在筛选中把视差不确定度传递到 f_M（视差信噪比 5-20 时的 Eddington 偏差）。
- 为短周期解建立经过验证的周期混叠否决（Gaia 扫描规律（scanning law）的谐波）。
- BH2：与其已发表的仅 DR3 解（arXiv:2302.07880）比较，作为类似 R1b 的严格检验。

## 8. 对话探索

编程智能体如何在不碰 `results/` 的前提下回答关于本研究的"如果……会怎样"问题
（规则：AGENTS.md 第 2 节）。添加于 2026-11-14（T-010，实现之后）。

| 旋钮（`PARAMS`） | 含义 | 安全范围 | 只用缓存，还是需要新数据（大小）？ |
|---|---|---|---|
| `release` | Gaia 数据发布版本（`dr3`；发布后的 `dr4`） | `dr3`、`dr4` | `dr4`：新查询（运行手册 `gaia-dr4-release-day`，先计数） |
| `fm_min` | 天体测量质量函数的服务器端切割 [Msun] | 0.1-1.0 | 新的筛选与审核查询；0.1 给出 22,512 行（约 3 MB，见 log.md），先计数 |
| `plx_snr_min` | 视差信噪比切割 | 3-20 | 新的筛选与审核查询；先计数 |
| `m2_bh_min` | 筛选行成为候选体的 M2 下限 [Msun] | 2-10 | 新的审核查询（候选体 id 列表改变），数据量小 |
| `rv_ratio_min` | 视向速度否决阈值（观测 / 预测视向速度范围） | 0.2-1.0 | 只用缓存 |
| `unvalidated_types` | 作为未验证而否决的解类型 | `screen.ASTROMETRIC_TYPES[release]` 的任意子集（DR3：Orbital、AstroSpectroSB1、OrbitalTargetedSearch(Validated)、OrbitalAlternative(Validated)） | 只用缓存 |

- 带覆盖值重跑：`python -m astrolab explore 001 --tag <topic> --set KEY=VALUE`
  （输出在 `explore/<date>-<topic>/`，不入库；从缓存运行只需几秒）。列表以 JSON 传入，
  例如在 bash 中 `--set 'unvalidated_types=["OrbitalAlternative"]'`。
- `run.py` 未涵盖的分析：写一个带 `def main(ctx)` 的脚本 `explore/<name>.py`，用
  `python -m astrolab explore 001 --tag <topic> --script explore/<name>.py` 运行。
- 结果文件与键（每次运行都写出全部文件；不适用于某个发布版本的文件只含
  简短的占位内容）：`summary.json`（`R1_BH1`、`R2_BH2`、`S1_*`、`S2_*`、`S3_*`、`post_hoc`；在 DR4 上还有
  `dr4`、`screen_descriptive`），`reproduction.json` 与 `targets.json`（三个黑洞），
  `bh_candidates.json`（M2 > 3 Msun 的行，带标签与否决），`screen_points.json`、`ns_recall.json`、
  `vetting_controls.json`、`reference_ids.json` 与 `dr4_screen_query.json`（DR3 运行），
  `survivors_dr4.json`、`new_candidates_dr4.json`、`new_candidate_ids_dr4_a/_b.json`（DR4 运行），
  `release.json`。
- 示例问题：
  - "如果视向速度否决更严格，会剩下多少候选体？" -> `--set rv_ratio_min=0.8`（只用缓存）。
  - "收紧预选后还能找回中子星候选体吗？" -> `--set fm_min=0.5`（先计数）。
  - "5 Msun 的阈值会留下哪些 DR3 候选体？" -> `--set m2_bh_min=5.0`（小规模新查询）。
- 改变我们认识的发现写进 `log.md` 和 Wiki 文章
  （[Study-001-gaia-dormant-black-holes](https://github.com/sudoghut/astrolab/wiki/Study-001-gaia-dormant-black-holes)），
  在分支上进行。
