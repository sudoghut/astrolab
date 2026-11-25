# 研究日志（research log）· M12 Poor old heart: Gaia XP metallicities of the oldest Milky Way stars

按时间倒序追加：做了什么、发现什么、走过哪些死路（dead ends）、下一步。
术语第一次出现时，在括号中注明英文原文。

## 2026-11-25（结果、审稿与收尾，T-021）

- 结果写入 README 第 5 节（中英文）。机械读法：复现"not reproduced"（T1、T3 (a)），稳健性"challenged"（T4、T5 a₅）。T1：−1.5 以下 30,589 颗，对比摘要约 18,000；T2a 版本 (i) σ̂ = 2.704 kpc [2.678, 2.730]，复现；版本 (ii) 2.713 kpc，已知答案模拟在 2.7 kpc 时恢复 2.21 kpc（偏差 −0.49 kpc），无法判定（方法偏差）；T2b 假阳性检查 0/100，形状无法判定，f₅ = 0.672 无法判定；T3 (a) 0.125 [0.089, 0.157] 有净旋转，(b) 0.542 [0.534, 0.551] 以旋转为主，(c) 宽度 1.35 dex 渐变；T4 敏感（平移 +0.1 dex 使 T3 (b) 变为不以旋转为主）；T5 g = 0.137 中等，a₅ = 0.410 未确认；T6 按 R22 的取法 6.12·10⁷ M☉。五段会话（下载并在 L2 停止；ESA 停机页面；三段完整运行合计 83,819 s）。`provenance.json`（9.9 MB）未入库，等用户决定，完整副本在 `%LOCALAPPDATA%\astrolab\Cache\s012_provenance_full\`。
- 独立审稿（referee，子智能体，只看第 1–4 节、代码、结果与 Lean 对照表）：重算全部标签与两个读法一致，没有改变标签的错误，没有改动判据。主要意见（第 6 节，事后）：T3 (a) 检验的是摘要，而 R22 第 III.3 节自己写了 −2 以下"some, albeit small, net"旋转（已逐字核对 arXiv v1）；T1 可能比较的是不同样本（图 4 图注说 R_GC < 4 kpc 的子集是"the focus of our analysis"）；T2a 的偏差决定 f₅（若真实 σ 约 3.2 kpc，f₅ 约 0.51，审稿）；T2b 的假阳性检查在 N = 30,000 时必然失败；T5 a₅ 很可能由运动学文件的选择驱动；T4 的"敏感"是阈值效应，且我们的 J_φ/J_tot 曲线低于 R22 的数字。"Gaia 补充用了 Data Lab 镜像"一点不接受：4.13 第 8 条已记录。按 σ 校准的 T2 登记为 T-069，曲线与计数定义登记为 T-070。
- Lean：审稿指出 R22 第 III.2 节明说低金属丰度部分"not severely contaminated"，所以 `gap_pure` 改为 `stat_pure`（STAT [stated]，注明是定性的论断）；`explicit_insufficient` 现在有四个缺口；`gap_template` 的注释改为只说模板对本样本的适用性是我们补上的。`tests/test_lean_arguments.py -k 012` 通过。Wiki 第二部分同步修改，第三部分补上实际结果。

## 2026-11-24

- 23:24 正式运行完成（本段 9,823 s，从检查点续跑：t2b 自助法 165–200 与其余阶段；状态 complete，检查点已按规则删除，暂停时的记录文件已由运行删除）。标签：T1 "not reproduced"（摘要比例 disagrees）；T2a 复现 "reproduced"、总体 "undetermined (method bias)"；T2b 形状 "undetermined (checks failed)"、f5 "undetermined (method bias)"；T3 (a) net rotation、(b) rotation dominated、(c) gradual（w0 0.262）；T4 "sensitive"（shift +0.1 改变 T3 (b)）；T5 g moderate、a5 "not confirmed"；T6 R22 ≥ 5e7 为真。复现读法 "not reproduced"（T1、T3 (a)），稳健性读法 "challenged"（T4、T5 a5）。其余结果文件入库；`provenance.json` 为 9.9 MB（Gaia DR3 补充查询的 235 个 source_id 列表，已是模板压缩格式），超过结果文件 1 MB 的约定，暂不入库，副本存在系统缓存目录，如何处理等用户决定。审稿与收尾随后进行。
- 20:5x 从检查点再次恢复正式运行（日志 `run012_t021_5.log`），依据是用户此前的同意（"T21 轮到之后就跑 不需要我确认"）。10:30 那一段按 `stop_after_hours` = 10 暂停在 `t2b_boot_164_K300`；之后按耗时短的先跑，先后完成了研究 010 的 T-064（16:04 结束）与研究 008 的 T-063（20:39 结束），机器上现在没有其他研究运行。PARAMS 不变。
- 00:30 从检查点恢复正式运行（日志 `run012_t021_4.log`），依据是用户 2026-11-23 的同意。研究 010 的 T-064 正式运行在 2026-11-24 00:2x 因系统内存不足被 Claude Code 停止（没有按约定自行重启，等待用户决定），所以研究 012 没有等它结束，机器上没有运行其他研究；恢复前空闲内存 8.2 GB。

## 2026-11-23

- 正式运行在第三段用完 `stop_after_hours` = 10 的时间预算后暂停（paused），停在 `t2b_boot_24_K300`；已完成 extgrid 101、t2a_mock 100、t2b_fp 100、t2b_power 100，检查点（checkpoints）在系统缓存 `s012_checkpoints/57faf48a6abc94b22d82`。用户 2026-11-23 在对话中同意从检查点恢复（原文："同意恢复"）；按一次只运行一个研究的约定，在研究 010 的 T-064 正式运行结束后再恢复。
- 正式首次运行结果：两个文件下载成功（98,513,191 与 115,266,771 字节，L1 的 MD5 都一致，放在系统缓存），运行在 L2 按预注册停止：金属丰度列名为 `mh_xgboost_rgb`，不在候选名中；并且金属丰度文件没有视差与测光（parallax、G、BP − RP、BP），只有 ra、dec、T_eff、log g 与 [M/H]。`first_download` 已改回 false。为向用户说明补充查询的规模，统计了金属丰度文件的行数与低于三个 [M/H] 值的星数（1,586,888 行；< −0.5：469,041；< −1.0：100,458；< −1.5：30,589），此外只看了列名与第一行数据。
- 用户 2026-11-23 在对话中选择完整的 Gaia DR3 TAP 补充（选项：完整补充 [M/H] < −0.5 的 469,041 颗星，约 235 次查询、约 30 MB（README 按 8 字节数值估计约 23 MB）；只补 [M/H] < −1.5；不补）。README 第 4.13 节（中英文）登记修订（amendment）：列名、补充的执行方式（含 `phot_bp_mean_mag`；l、b 由 ra、dec 计算；不做计数查询，因为每个列表至多 2,000 个不同的 `source_id`，`max_rows` 等于列表长度）、[M/H] ≥ −0.5 的星没有这些列的影响（L6 直方图与视差误差抽样改用 [M/H] < −0.5 的星）。代码 `run.gaia_addition` 与离线测试；补充须在 Gaia 档案 2026-11-25 下线之前运行。闸门 1 一轮：没有严重问题；小问题已改（补充披露 T1 的 N(< −1.5) 在运行前被看到、T4 扰动 [M/H] 的情形、ϖ/σ_ϖ < 1 比例规则、下线期间不用 `--refresh`、第 8 节的范围说明、未请求 id 的测试）。Codex 一轮：一个严重问题已改（有视差而没有测光的星在 T6 的 f_bright 中被算作暗星；现在排除并记录数目，修订第 7 项，加测试）；小问题已改（第 3 节的可选行指向 4.13、L6 比例的方向说法删去）。Codex 第二轮：一个严重问题已改（模拟的视差误差抽样只需要 G 与 σ_ϖ，原代码却同时要求 BP 与颜色，会把缺颜色的星排除；修订第 7 项写明，加测试），小问题已改（`n_no_photometry` 的范围写明）。Codex 第三轮：没有严重问题（通过双闸）；小问题已改（L2 停止信息、第 3 节行中的实际规模）。正式运行（09:20）在第一次补充查询时失败：ESA Gaia 档案已提前进入停机，TAP 返回 HTML 停机页（"ESDC Archives downtime"）而不是 VOTable。诊断：经 `astrolab.fetch.tap` 的 5 个 id 与单行查询同样失败；另用一次在 `astrolab.fetch` 之外的直接 POST 只读取了返回页面的开头以确认是停机页（没有取数据）。NOIRLab Astro Data Lab 的 Gaia DR3 镜像 `gaia_dr3.gaia_source` 可用（经 `fetch.tap`：5 个 id 39 秒，2,000 个 id 5.7 秒），改用它，修订第 8 项（中英文），再过双闸。第 8 项通过双闸（闸门 1 与 Codex 都没有严重问题）；小问题已改：第 8 项写明取代第 3、5 项的哪些部分、`n_unmatched` 预期为 0、两次镜像查询与在缓存列表上做的哨兵值检查（没有 NULL 或哨兵值）、第一个列表的来源记录带诊断注释；`gaia_addition` 的文档字符串。
- 正式首次运行（formal first run）开始：`PARAMS["first_download"]` 设为 true（只此一次，允许按 2026-11-21 的例外下载两个 Zenodo 文件，合计 213.8 MB，放在系统缓存），运行结束后立即改回 false 并提交。用户在对话中同意轮到时直接运行（原文："T21 轮到之后就跑 不需要我确认"）；运行在研究 010 的 T-059 正式运行结束后开始，机器上没有运行其他研究。`stop_after_hours` = 10（断点续跑）。

## 2026-11-21

- 实现 `run.py` 与辅助模块（`data012.py`、`model012.py`、`kin012.py`、`stats012.py`、`store012.py`），合成数据（synthetic data）上的单元测试与端到端测试，网页，README 第 8 节，以及第 4.12 节"任何拟合之前的修订"（中英文）。没有下载或读取数据文件，没有运行研究。T-021 的两个取数调用（`run.py` 的 `fetch_files`，对两个 Zenodo 文件各调用一次 `ctx.http`）带 `cap_consent`（单文件上限（cap）例外）与 `budget_consent`（研究预算（budget）例外），两者都引用 T-021 与本日志；只有 `PARAMS["first_download"]` 为真时才允许下载（`allow_download`），首次正式运行之后改回 false。计时（timing）：20,000 颗合成星、300 个节点时一次似然求值 0.075–0.13 秒；按实测的求值次数预计正式运行约 13–19 小时（按 README 第 4.10 节的次数约 23–35 小时），单核，断点续跑。
- 预注册（README 第 1–4 节，中英文）通过双闸（闸门 1 三轮、闸门 2 三轮）。写作时没有下载或打开任何数据文件。运行前提：按文件的预算例外机制（实现阶段第一项）须先通过双闸；预计运行约 24–34 小时（单核，断点续跑），正式运行前先报告实测计时。
- 数据来源与例外（exception）：论文的 XP 金属丰度样本只在 Zenodo（记录 7035809：`xp_gc_mh.csv` 98.5 MB，`xp_gc_kinematics.csv` 115.3 MB，合计 213.8 MB，CC BY 4.0）。两个文件各超过 50 MB 的单次下载上限（`HTTP_MAX_BYTES`），合计超过 200 MB 的研究预算（`STUDY_BUDGET_BYTES`）。先尝试的服务器端途径不可行：CDS TAP 主机连接超时，Andrae 等 2023 的完整星表不在 VizieR 中（只在 Zenodo 7945154，12.3 GB，不下载）。用户 2026-11-21 在对话中同意破例（原文："先做1 如果 1 不行，就做 2"）：两个文件只下载一次，放在系统缓存，不进项目目录；预注册（README 第 3 节写明文件名、大小与 MD5）完成后才下载。
- 创建研究文件夹。
- 下一步：填写 README 第 1–4 节，即问题、假设与判据（hypothesis and decision criteria）、数据、方法。
