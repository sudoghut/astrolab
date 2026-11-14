# AGENTS.md · astrolab 操作手册（适用于所有编程智能体 coding agent）

这是一个由编程智能体驱动、在个人电脑上运行的天文学研究环境。开始工作前请依次阅读：

1. [`design/000-principles_*.md`](design/000-principles_agent-driven-laptop-astronomy-research.md)：设计原则，即项目的"宪法"。
2. [`STATUS.md`](STATUS.md)：当前状态与下一步。
3. [`ROADMAP.md`](ROADMAP.md)：里程碑（milestone）路线图。
4. 当前要处理的研究的 `studies/<id>/README.md` 和 `log.md`。

---

## 第一条：数据下载约束（最高优先级，不可违反）

本项目运行在存储和带宽都有限的个人电脑上，项目目录还由 Dropbox 同步。**下载大量数据是本项目最严重的错误。** 以下约束优先于任何任务目标；如果完成任务需要违反它们，**停下来问用户**。

### 1.1 数值上限

| 项目 | 上限 | 所在位置 |
|---|---|---|
| 单次 HTTP 下载 | 50 MB | `config.HTTP_MAX_BYTES` |
| 单次 TAP 查询 | 默认 50,000 行；硬上限 2,000,000 行 | `config.TAP_DEFAULT_MAX_ROWS` / `TAP_HARD_MAX_ROWS` |
| 一个研究单次运行的全部输入 | 200 MB | `config.STUDY_BUDGET_BYTES` |
| 缓存总量（cache） | 2 GB，超出按 LRU 自动清理 | `config.CACHE_LIMIT_BYTES` |
| 研究结果 `results/` | 每个文件应在 1 MB 以下，硬性警告线 5 MB | `results.RESULT_WARN_BYTES` |

LRU 指最近最少使用（Least Recently Used）的清理策略。

**未经用户明确同意，不得修改这些上限**：不改 `astrolab/config.py`，不设置 `ASTROLAB_*` 环境变量绕过它们。

### 1.2 取数只能走受守卫的通道

- 一律通过 `ctx.tap()`、`ctx.http()`（研究内）或 `astrolab.fetch.tap/http`（库内）取数。它们会做大小检查、缓存，并记录来源（provenance）。
- **禁止**用 `curl`、`wget`、`Invoke-WebRequest`、裸 `requests.get`、`astroquery` 的下载函数，或浏览器直接下载数据文件。查阅网页文档（HTML 或 arXiv 摘要页）不在此限。
- **禁止**递归或批量下载，例如 `wget -r`，或在循环中逐个下载成百上千个文件。

### 1.3 先估算，再下载

- 对于结果规模未知的查询，先在服务器端跑 `COUNT(*)`（使用 `fetch.tap_count`），确认行数后再取数据。
- 研究的 `README.md` 第 3 节"数据"表必须写出每项输入的预估行数和大小，**写完再运行**。
- 只取需要的列，不用 `SELECT *` 查大表。

### 1.4 优先在服务器端计算

能在服务器端完成的，一律在服务器端完成，只下载结果：
- 筛选：`WHERE`
- 聚合：`GROUP BY`、HEALPix 分层像素索引（Hierarchical Equal Area isoLatitude Pixelization），例如 `GAIA_HEALPIX_INDEX`
- 派生量计算：在 ADQL 里算好再下载
- 交叉匹配（cross-match）：用服务器提供的交叉匹配表

能用压缩数据产品（compressed data products）的，不用原始数据，例如论文表格、距离表、协方差矩阵、汇总后验（summary posterior）。

### 1.5 明令禁止的下载（已知的大数据陷阱）

| 不要下载 | 大小 | 替代做法 |
|---|---|---|
| Gaia 全表或批量文件（如 `cdn.gea.esac.esa.int/Gaia/gdr3/` 下的分块 CSV） | TB 级 | ADQL 服务器端查询 |
| El-Badry 2021 宽双星星表（Zenodo 4435257） | 1.8 GB | 服务器端自连接（self-join）重建样本 |
| GWTC-4.0 群体分析数据发布（Zenodo 16911562）的大文件 | 35 GB | 只取事件列表、图表包、popsummary 汇总 |
| 引力波单事件后验样本 HDF5 文件（posterior samples） | 每个数百 MB | 事件参数表，或降采样后的样本 |
| SDSS、DESI、LAMOST 的批量光谱 | GB–TB | 服务器端星表查询；单条光谱逐个按需获取 |
| 原始图像、FITS 图像立方（image cubes） | GB 级 | 不在本项目范围内 |
| JWST、HST 原始观测数据 | GB 级 | 用论文表格或高级科学产品（HLSP, High-Level Science Products）中的一维光谱 |

### 1.6 遇到上限时怎么办

收到 `TooLarge` 错误时，按顺序尝试：
1. 收窄选择条件。
2. 改为服务器端聚合。
3. 换用压缩数据产品。
4. 以上都不行时，**停下来向用户说明需求和数据量，等待同意**。

不得自行调高上限重试。如果用户同意放宽，把理由记录在研究日志 `log.md` 中。

### 1.7 存储位置

- 缓存放在系统缓存目录：`%LOCALAPPDATA%\astrolab\Cache`。
- 项目目录（Dropbox）只放代码、文档和小结果。**不往项目目录写数据文件**；`.fits`、`.h5`、`.npz` 已在 `.gitignore` 中排除，但这只是兜底，不是许可。
- 不对 Dropbox 目录做递归列举（recursive listing），例如 `ls -R` 或 `Get-ChildItem -Recurse`，因为这会触发云端文件的下载。

---

## 第二条：工作方式

- 不使用 Jupyter notebook。分析写成 `run.py`，展示写成 `web/index.html`。
- **复杂任务先写工作计划（work plan）**：
  - 放在 `design/NNN-plan_<核心内容>.md`，编号取当前最大值加 1，文件名必须表达核心内容。
  - 在 `design/README.md` 索引中登记。
  - 执行过程中，在计划文末的"执行记录"一节追加进度。
- **先写假设与判据，再跑分析**：研究的 `README.md` 第 1–4 节必须在写 `run.py` 之前完成，相当于预注册（pre-registration）。
- **术语括注英文**：设计文献与研究日志用中文书写，任何术语第一次出现时都要在括号中注明英文原文，缩写写出全称。代码与注释用英文。
- **项目保持中英双语**（见 `design/004-plan_*`）：
  - 对外说明文档（如 `README.md`）中英双语，两种语言内容对应。
  - **每个网页都要有英文/中文切换按钮，默认英文。** 一律在 `<head>` 中引用共享的 `atlas/web/i18n.js`；它自带切换按钮和隐藏样式，不依赖 `base.css`。用法：
    - 静态文字成对写成 `<span class="en">…</span><span class="zh">…</span>`。
    - 脚本生成的 HTML 用 `i18n.L(en, zh)`。
    - 纯文本场合（`textContent`、属性、`<option>`、图表标题与悬停文字）用 `i18n.t(en, zh)`，并在 `i18n.onLangChange(fn)` 中更新。
    - 中文页面标题写在 `<html data-title-zh="…">`。
  - 测试会检查每个 `web/` 下的 `.html` 是否引用了 `i18n.js`。
  - 中文字段：结论条目（claims）加 `title_zh`、`statement_zh`，`study.yaml` 加 `title_zh`、`question_zh`。新建结论或研究时必须同时填写；`claims check` 与测试会检查它们是非空字符串。网页在中文模式下显示中文字段。
  - 天体名称、星表编号、数值、单位、文献引用、代码与命令不翻译。
- **引用前先核实**：路线图中标为 [S] 或 [U] 的条目，动手前要提升到 [V]，即对照原文核实。
- **及时抽出技能（skills）**：某个研究动作第二次出现，或者步骤多、容易做错时，就把它写成技能，放在 `.claude/skills/<name>/SKILL.md`。
  - 已有技能：独立审稿（referee）、服务器端查询（server-side query）、双闸代码审查（dual-gate review）。已规划：新建研究、文献核实、出报告。
  - 技能里只写流程与检查清单；具体规则仍以本文件为准，两者不重复。

## 第三条：运行命令

需要 Python 3.11 或以上版本，在项目根目录运行。依赖见 `pyproject.toml`，安装方式：`pip install numpy scipy pandas pyarrow astropy pyvo astropy-healpix emcee platformdirs pyyaml requests pytest nsstools`。本机解释器路径若有特殊约定，写在不入库的 `CLAUDE.local.md` 或用户级配置中。Windows 的 PowerShell 中先设置 `$env:PYTHONIOENCODING='utf-8'`。

```
python -m astrolab status                 # 全局概览：研究、结论、缓存
python -m astrolab new <slug> "<title>" --level L3   # 新建研究（自动取下一个编号）
python -m astrolab run <id|编号|子串> [--refresh]     # 运行研究，产出 results/
python -m astrolab claims [list|check]    # 列出或校验结论条目
python -m astrolab atlas                  # 生成 atlas/web/data/atlas.json
python -m astrolab serve [--port 8765]    # 本地网页服务：Atlas 与各研究页面
python -m astrolab cache [info|prune|clear]
python -m pytest                          # 核心库测试 + 各研究的结论测试
```

## 第四条：目录结构

| 路径 | 内容 |
|---|---|
| `astrolab/` | 核心库（core library），只加入被研究实际用到的能力 |
| `atlas/claims/*.yaml` | 结论登记表（claims registry），字段说明见 `astrolab/claims.py` |
| `atlas/web/` | 宏观总览页；`base.css` 为所有页面共享 |
| `studies/NNN-slug/` | 每个研究问题一个文件夹，模板在 `studies/_template/` |
| `design/` | 设计文献：原则、工作计划、决策、复盘 |

单个研究文件夹的内容：

| 文件 | 作用 |
|---|---|
| `study.yaml` | 元数据：层级、状态、关联结论、足迹（footprint） |
| `README.md` | 问题、假设与判据、数据（附大小估计）、方法、结果、审稿意见、开放问题 |
| `log.md` | 研究日志（research log），按时间倒序追加 |
| `run.py` | `def main(ctx)`，用 `ctx.tap / ctx.http / ctx.save / ctx.log` |
| `test_conclusions.py` | 读取 `results/`，断言结论仍然成立 |
| `web/` | 为该问题设计的网页，读取 `../results/*.json`。形式完全按研究需要来：可以是可视化、交互式数据分析、多页面或专用工具，**不必拘泥于 Atlas 的样式或结构**；`atlas/web/base.css` 可用可不用，但必须引用 `atlas/web/i18n.js`（见第二条双语规则） |

**Atlas 与研究网页的分工**：Atlas 是总图，只负责宏观导航（各尺度的结论与研究落在哪里）。局部的研究、可视化与数据分析都在各自的 `studies/<id>/web/` 中灵活设计。

## 第五条：研究完成标准

- README 已填写完整。
- `run.py` 可以重跑。
- 测试通过。
- 网页可用。
- 关联结论条目已更新复现值（`ours`）与状态。
- `log.md` 和 `STATUS.md` 已更新。
- 已做过独立审稿（referee）：派一个子智能体（subagent），只给它代码与结果，不给我们的结论，专门找系统误差（systematics）与选择效应（selection effects）。
