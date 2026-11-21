# M12 贫而老的核心：Gaia XP 金属丰度与银河系最老的恒星

> English: [README.md](README.md)（M12 Poor old heart: Gaia XP metallicities of the oldest Milky Way stars）。以英文 `README.md` 为准（预注册与判据的权威文本）；本文件是它的中文译本，节号与表格一一对应，英文改动时在同一个 PR 中同步修改。网页在线版：[https://sudoghut.github.io/astrolab/studies/012-m12-poor-old-heart/web/](https://sudoghut.github.io/astrolab/studies/012-m12-poor-old-heart/web/)。
>
> 第 1–4 节须在写 `run.py` 之前完成（预注册，pre-registration）；之后只能带日期注明理由地修改。

## 1. 问题

TODO：我们究竟要问什么？

## 2. 假设与判据

TODO：什么结果支持或否定假设？给出定量门槛。

## 3. 数据（附大小估计）

| 输入 | 来源（服务 / 网址） | 选择条件 | 预估行数 / 大小 |
|---|---|---|---|
| TODO | | | |

所有输入都必须是 MB 级。筛选与聚合尽量放在服务器端完成。

## 4. 方法

TODO：步骤、模型、先验、要检查的系统误差。

## 5. 结果

运行后填写。链接 `web/index.html`，并给出 `results/` 中的关键数字。

## 6. 审稿意见（referee notes）

独立审稿：选择效应、系统误差、其他解释。

## 7. 开放问题

## 8. 对话探索（exploring via chat）

编程智能体如何在不改动 `results/` 的前提下回答关于本研究的"如果……会怎样"问题（规则见 AGENTS.md 第二条）。

| 旋钮（`PARAMS`） | 含义 | 安全范围 | 只用缓存，还是需要新数据（大小）？ |
|---|---|---|---|
| TODO | | | |

- 带覆盖参数重跑：`python -m astrolab explore 012-m12-poor-old-heart --tag <topic> --set KEY=VALUE`
  （输出在 `explore/<date>-<topic>/`，不入库；从缓存运行约 N 秒）。
- `run.py` 没有覆盖的分析：在 `explore/<name>.py` 写带 `def main(ctx)` 的脚本，用
  `python -m astrolab explore 012-m12-poor-old-heart --tag <topic> --script explore/<name>.py` 运行。
- 结果文件与键：TODO（`results/<file>.json`：键——含义）。
- 示例问题：TODO（问题 -> 智能体会用的旋钮或脚本）。
- 改变认识的发现写进 `log.md`（论文研究还要写进 Wiki 文章），照常走分支。
