# 022 · 工作计划：M8 用带误差的 z ≈ 8 分箱光度函数校准恒定 SFE 模型，并给出研究 006 判定的概率

状态：执行中
创建：2026-11-16
待办：T-025（`TODO.md`）

## 1. 目标

研究 006 的独立审稿（referee）指出：Bouwens 等 2021 的 z ~ 8 舍克特（Schechter）参数任一按 1σ 移动都会使 R3 翻转，φ* 减 1σ 还会使 R2 翻转。本计划改用带误差的分箱光度函数（luminosity function, LF）——空白场（blank field）的 Bouwens 等 2021 表 4 与透镜星系团场（lensing cluster）的 Bouwens 等 2022 表 4——在似然中拟合恒定恒星形成效率（SFE, star formation efficiency）模型的参数，用 emcee 采样后验，并把后验传播到 R2 的比值与 R3 的所需 σ_UV，报告各判定的概率。全部输入是论文表格，已于 2026-11-16 对照 PDF 核实。

## 2. 范围

- 预注册写在研究 006 `README.md` 第 2 节的附录（2026-11-16，R2/R3-POST）。
- 只用基准组合（fiducial）；σ_cal = 0.5、0.9 与加入四个暗端透镜点作为报告的敏感性。
- 原来的判定不变，本检验是敏感性结果。

## 3. 环节与审查

1. 预注册附录——双闸审查（dual-gate review）。
2. 代码：`z14model.py` 的分箱似然、`run.py` 的 R2/R3-POST，结果写 `results/post.json`；`test_conclusions.py` 按规则复算——双闸审查。
3. 正式运行、README 第 5–7 节、`log.md`、结论条目、Wiki、独立审稿、收尾双闸、合并、发布 Wiki。

## 4. 验收标准（acceptance criteria）

- `results/post.json` 含链的收敛诊断、参数后验、500 次抽样的 R2/R3 判定与概率、敏感性。
- 测试按附录规则复算概率与判定；`python -m pytest` 通过。
- README、Wiki（中英）、结论条目、STATUS、DONE 同步；独立审稿已处理；收尾双闸通过。

## 5. 执行记录

- 2026-11-16：开分支 `feat/m8-lf-calibration-posterior`；对照 PDF 核实两张表（空白场 7 行，z ~ 8 的最后一行是 −17.60，−17.61 一行属于 z ~ 2；透镜场 12 行，其中一个上限）；写预注册附录，此前没有对分箱数据做过任何拟合。
