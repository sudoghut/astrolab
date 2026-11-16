# 020 · 工作计划：M1 用 CAMB 核对 R2 的 θ* 标定（研究 002）

状态：执行中
创建：2026-11-16
待办：T-022（`TODO.md`）

## 1. 目标

研究 002 的独立审稿指出：R2 中压缩宇宙微波背景（CMB, Cosmic Microwave Background）先验两种解读（A：ωbc 含中微子；B：不含）的判定分歧，与 θ*（声学尺度角，angular acoustic scale）标定的误差同量级；标定常数 K 在 Planck 参考点固定，它随宇宙学参数的变化在拟合点没有测过。用户 2026-11-16 同意在项目 venv 中安装 CAMB（宇宙学线性理论代码，Code for Anisotropies in the Microwave Background；camb 2.0.5，不是数据下载）。本计划用 CAMB 的 θ* 替换拟合公式，检验 R2 的两个解读的判定是否改变。

## 2. 范围

- 只改 R2 中 CMB 先验项里的 θ*；BAO 距离、r_d、先验、起点、有效性检查与容差都不变。
- 预注册写在研究 002 `README.md` 第 2 节的附录（2026-11-16，R2-CAMB），第 4 节加一条方法说明。
- 主检验：以 Planck 参考点锚定的 CAMB θ*（只替换随宇宙学参数的变化）；次要：不缩放的 CAMB θ*。
- 原 R2 判定保持不变；本检验只增加一个敏感性结果。

## 3. 环节与审查

1. 预注册附录（README 第 2、4 节）——双闸审查。
2. 代码：`camb_theta.py`（研究目录内的辅助模块，不 `import run`）与 `run.py` 的 R2-CAMB 部分，`PARAMS["camb_check"]`；结果写 `results/r2_camb.json`；`test_conclusions.py` 按附录规则复算——双闸审查。
3. 正式运行（约 1 小时）、README 第 5–7 节、`log.md`、结论条目、Wiki 第三部分与研究进展、独立审稿（只看代码与结果）、收尾双闸、合并、发布 Wiki。

## 4. 执行记录

- 2026-11-16：开分支 `feat/m1-camb-theta-check`；速度测试：CAMB 背景计算每次约 8 ms，完整多起点拟合可行；Planck 参考点 CAMB 100θ* = 1.04116（Planck 2018 表 1 为 1.041085），这是写附录前看到的唯一 CAMB 数值。
