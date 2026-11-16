# 024 · 工作计划：M3 用归一化流复现 DES Y6 与 CMB 的全参数空间差异（研究 008，R6-FLOW）

状态：执行中
创建：2026-11-16
待办：T-027（`TODO.md`）

## 1. 目标

研究 008 的 R4 用高斯近似计算全参数空间差异，结果依赖参数化（0.32–2.21σ），不能检验 D26 的 1.8σ。D26 用 tensiometer 的归一化流（normalizing flow）估计参数差异的密度。本计划在用户同意建立的独立环境（`%LOCALAPPDATA%/astrolab/venv-tf`：TensorFlow 2.21、TensorFlow Probability 0.25、tensiometer 1.1.0）中复现这一步，并作为新的判定 R6 预注册。

## 2. 范围与设计

- 预注册写在研究 008 `README.md`（及 `README.zh.md`）第 2.6 节（R6-FLOW）。参数集是我们的重建：D26 没有写明全空间包含哪些参数，我们用 R4 的六个共同采样参数（即 D26 的六个 ΛCDM 自由参数）。
- **两个环境的分工**：项目 venv 中的 `run.py` 照常经 `ctx.http` 从缓存读链（有来源记录、预算计费），只把六列、S8、Ωm 与权重写成一个临时 `.npz`，放在缓存目录的 staging 区（不写进项目目录，运行后删除）；再用子进程调用 TF 环境的解释器运行研究目录下的 `flowshift.py`（只依赖 numpy、getdist、tensiometer），结果以 JSON 返回，由 `run.py` 判定并保存到 `results/r6.json`。TF 解释器路径放在 `PARAMS["tf_python"]`；找不到时 R6 记为"无法评估（没有 TF 环境）"，其余结果不受影响。
- 不新取数据；原有 R1–R5 的结果不变（`run.py` 中 R6 是独立的一段，另有开关 `PARAMS["r6"]`）。

## 3. 环节与审查

1. 预注册附录（第 2.6 节，中英文）与本计划——双闸审查。
2. 代码：`flowshift.py`（TF 环境）、`run.py` 的 R6（数据导出、子进程、验证、判定）、`test_conclusions.py` 按规则独立复算判定；在合成高斯数据上检查流的估计（已知 n_σ）——双闸审查。
3. 正式运行、README 第 5–7 节（中英文）、`log.md`、结论条目、Wiki、独立审稿、收尾双闸、合并、发布 Wiki。

## 4. 验收标准（acceptance criteria）

- `results/r6.json` 含五次重复的 n_σ、Δ 及其区间、训练时间、tensiometer 默认设置、验证结果与判定；
- `test_conclusions.py` 由保存的数字独立复算 R6 判定；`python -m pytest` 通过（没有 TF 环境时 R6 测试跳过而不是失败）；
- README（中英文）、网页、结论条目与 Wiki 同步；`log.md`、STATUS、DONE 更新。

## 5. 执行记录

- 2026-11-16：开分支 `feat/t027-flow-full-space-shift`；核对 D26（arXiv:2601.14559v2）第 IV.1、IV.6 节与表 3、表 6；查看 tensiometer 1.1.0 的接口源代码（未对链训练任何流）；写本计划与预注册附录。
