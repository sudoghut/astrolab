# 研究日志（research log）· Wide binaries: Newton or MOND at low acceleration?

按时间倒序追加：做了什么、发现什么、走过哪些死路（dead ends）、下一步。
术语第一次出现时，在括号中注明英文原文。

## 2026-11-16

- 第 A 步取数（不含速度列）完成：339 个区域，A1 194,157 对候选，A2 548,804 颗有邻居的星（README 第 3 节估计"可能不超过 200,000"，仍在硬上限之内），A3 157,692 颗 FLAME（Gaia DR3 的恒星参数流水线 Final Luminosity Age Mass Estimator）质量。第 A 步按每行 600 B 的保守估计累计 142.2 MB（实际下载 38.7 MB），第 B 步 B1 在剩余约 67 MB 内取数。过程中 Gaia 存档停机约 28 小时；恢复后先因会话 cookie 失效（HTTP 401）、再因缓存的线程竞争（race condition）失败，核心库已修复（计划 013 执行记录）。`results/provenance.json` 为 2.7 MB，超过每个结果文件 1 MB 的建议值（未超过 5 MB 警告线），压缩来源记录登记为 T-033。
- 赫罗图（HR, Hertzsprung–Russell）常数 c = 1.5909（0.05 窗口内 2081 颗星），带日期写入 `PARAMS["hr_c"]` 与 README 第 4.5 节。
- 不用速度的逐箱计数（探索脚本 `explore/occupancy_step_a.py`）：x 箱依次为 3、371、407、204、162、223 对，每箱都是第 B 步的上限；最终的合并由第 B 步的计数按同一规则决定（按这些计数，最低箱会并入相邻箱）。这些计数比 C26 图 8 偏向更大的 x，是系统误差中已列出的 x 约定问题在不用速度时的迹象；没有因此改动任何箱边界、x 的定义或合并规则。逐项截断：配对 194,157 → 去群（degrouping）37,381 → 距离 30,213 → r_sky 6,777 → RUWE（重归一化单位权误差，Renormalised Unit Weight Error）4,457 → 赫罗图带 1,370。
- 下一步：提交后运行第 B 步。

## 2026-11-14

- 创建研究文件夹。
- 下一步：填写 README 第 1–4 节，即问题、假设与判据（hypothesis and decision criteria）、数据、方法。
