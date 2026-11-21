# 研究日志（research log）· M11 Radcliffe Wave: is the young-cluster wave oscillating?

按时间倒序追加：做了什么、发现什么、走过哪些死路（dead ends）、下一步。
术语第一次出现时，在括号中注明英文原文。

## 2026-11-21

- 预注册（pre-registration，README 第 1–4 节，中英文）通过双闸审查：闸门 1 三轮（子智能体），闸门 2 两轮（Codex）。主要修改：T3 的自助法 p 值与 Bartlett 型校准（calibration）的定义；模拟次数设下限，超时则断点续跑；已知答案检验（known-answer check）改用 K24 印出的参数；T5 只按位置选择星团；T6 检查全部五个标签并按相同规则比较；T7 改为比较 −2 ln L_max。Codex 认为 B = 1 处应按单边边界处理，我们以矩阵形式的论证驳回（B = 1 是正则二参数族的内点），理由写入第 4.3 节，Codex 第二轮同意。
- 预注册之前接触数据的范围（已在 README 第 1 节披露）：经受守卫的 `fetch.http` 读取两张表的列名、行数、取值范围，以及星团表 `reference` 与 `inlier` 两列的计数；没有拟合任何模型。为此给 `fetch.http` 加了通用的客户端名（User-Agent），因为 Harvard Dataverse 拒绝 Python 默认的客户端名（403）。
- Wiki 第三部分（可检验环节）通过双闸：闸门 1 六轮，闸门 2 三轮；Codex 一条关于 b̂ 依赖 ω₀t 的意见经数值检验驳回。
- 下一步：实现 `run.py`、结论测试、网页与第 8 节，走双闸；正式运行要等 T-049 的运行结束。
- 创建研究文件夹。
- 下一步：填写 README 第 1–4 节，即问题、假设与判据（hypothesis and decision criteria）、数据、方法。
