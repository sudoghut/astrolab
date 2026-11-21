# 研究日志（research log）· M12 Poor old heart: Gaia XP metallicities of the oldest Milky Way stars

按时间倒序追加：做了什么、发现什么、走过哪些死路（dead ends）、下一步。
术语第一次出现时，在括号中注明英文原文。

## 2026-11-21

- 数据来源与例外（exception）：论文的 XP 金属丰度样本只在 Zenodo（记录 7035809：`xp_gc_mh.csv` 98.5 MB，`xp_gc_kinematics.csv` 115.3 MB，合计 213.8 MB，CC BY 4.0）。两个文件各超过 50 MB 的单次下载上限（`HTTP_MAX_BYTES`），合计超过 200 MB 的研究预算（`STUDY_BUDGET_BYTES`）。先尝试的服务器端途径不可行：CDS TAP 主机连接超时，Andrae 等 2023 的完整星表不在 VizieR 中（只在 Zenodo 7945154，12.3 GB，不下载）。用户 2026-11-21 在对话中同意破例（原文："先做1 如果 1 不行，就做 2"）：两个文件只下载一次，放在系统缓存，不进项目目录；预注册（README 第 3 节写明文件名、大小与 MD5）完成后才下载。
- 创建研究文件夹。
- 下一步：填写 README 第 1–4 节，即问题、假设与判据（hypothesis and decision criteria）、数据、方法。
