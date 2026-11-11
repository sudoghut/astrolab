# CLAUDE.md

本项目的完整操作手册在 `AGENTS.md`，所有编程智能体（coding agent）共用一份。下面这行把它导入：

@AGENTS.md

## 对 Claude Code 的补充

- **数据下载约束（`AGENTS.md` 第一条）优先于任何任务目标。** 需要突破上限时，停下来问用户；不要自行修改 `astrolab/config.py` 中的上限，也不要设置 `ASTROLAB_*` 环境变量绕过它们。
- 不要用 Bash 或 PowerShell 的 `curl`、`wget`、`Invoke-WebRequest` 下载数据文件；取数只走 `astrolab.fetch`。
- 文献核实可以用网页搜索与网页读取，但只读页面，不下载数据文件。
