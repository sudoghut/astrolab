# 研究日志（research log）· M12 Poor old heart: Gaia XP metallicities of the oldest Milky Way stars

按时间倒序追加：做了什么、发现什么、走过哪些死路（dead ends）、下一步。
术语第一次出现时，在括号中注明英文原文。

## 2026-11-21

- 实现 `run.py` 与辅助模块（`data012.py`、`model012.py`、`kin012.py`、`stats012.py`、`store012.py`），合成数据（synthetic data）上的单元测试与端到端测试，网页，README 第 8 节，以及第 4.12 节"任何拟合之前的修订"（中英文）。没有下载或读取数据文件，没有运行研究。T-021 的两个取数调用（`run.py` 的 `fetch_files`，对两个 Zenodo 文件各调用一次 `ctx.http`）带 `cap_consent`（单文件上限（cap）例外）与 `budget_consent`（研究预算（budget）例外），两者都引用 T-021 与本日志；只有 `PARAMS["first_download"]` 为真时才允许下载（`allow_download`），首次正式运行之后改回 false。计时（timing）：20,000 颗合成星、300 个节点时一次似然求值 0.075–0.13 秒；按实测的求值次数预计正式运行约 13–19 小时（按 README 第 4.10 节的次数约 23–35 小时），单核，断点续跑。
- 预注册（README 第 1–4 节，中英文）通过双闸（闸门 1 三轮、闸门 2 三轮）。写作时没有下载或打开任何数据文件。运行前提：按文件的预算例外机制（实现阶段第一项）须先通过双闸；预计运行约 24–34 小时（单核，断点续跑），正式运行前先报告实测计时。
- 数据来源与例外（exception）：论文的 XP 金属丰度样本只在 Zenodo（记录 7035809：`xp_gc_mh.csv` 98.5 MB，`xp_gc_kinematics.csv` 115.3 MB，合计 213.8 MB，CC BY 4.0）。两个文件各超过 50 MB 的单次下载上限（`HTTP_MAX_BYTES`），合计超过 200 MB 的研究预算（`STUDY_BUDGET_BYTES`）。先尝试的服务器端途径不可行：CDS TAP 主机连接超时，Andrae 等 2023 的完整星表不在 VizieR 中（只在 Zenodo 7945154，12.3 GB，不下载）。用户 2026-11-21 在对话中同意破例（原文："先做1 如果 1 不行，就做 2"）：两个文件只下载一次，放在系统缓存，不进项目目录；预注册（README 第 3 节写明文件名、大小与 MD5）完成后才下载。
- 创建研究文件夹。
- 下一步：填写 README 第 1–4 节，即问题、假设与判据（hypothesis and decision criteria）、数据、方法。
