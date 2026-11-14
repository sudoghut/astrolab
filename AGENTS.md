# AGENTS.md · astrolab 操作手册（适用于所有编程智能体 coding agent）

这是一个由编程智能体驱动、在个人电脑上运行的天文学研究环境。开始工作前请依次阅读：

1. [`design/000-principles_*.md`](design/000-principles_agent-driven-laptop-astronomy-research.md)：设计原则，即项目的"宪法"。
2. [`STATUS.md`](STATUS.md)：当前状态与时间点。
3. [`TODO.md`](TODO.md)：待办清单（to-do list），要做的事与优先级。
4. [`ROADMAP.md`](ROADMAP.md)：里程碑（milestone）路线图。
5. 当前要处理的研究的 `studies/<id>/README.md` 和 `log.md`。

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
- **分支与合并**：所有改动（包括只改 `TODO.md`/`DONE.md` 的）都在功能分支（feature branch）上做，通过拉取请求（PR, Pull Request）以变基合并（rebase merge）进入 `main`，保持线性历史；不直接提交到 `main`。
- **待办清单（to-do list）**：`TODO.md` 是唯一的任务清单，`DONE.md` 是完成日志（done log）。条目格式见两个文件开头，设计见 `design/006-plan_*`。
  - **先登记再动手**：任何要做的独立任务先写进 `TODO.md`：马上做的放"进行中（Doing）"；排定的按优先级插入"下一步（Next）"；暂不排序的放"待办池（Backlog）"末尾。当前条目内部的小步骤写在它的 `计划：`/`备注：` 子条目里，不另开编号。研究自身的开放问题留在该研究 `README.md` 的"开放问题"一节，排上日程时再登记到 `TODO.md`。只登记、不开工时，随当前分支提交；手上没有分支时，开一个 `chore/todo-<内容>` 小分支走 PR。
  - **编号**：`T-NNN`（三位数字），取 `TODO.md` 与 `DONE.md` 中最大编号加 1，永不复用。两个分支撞号时，先合入 `main` 的保留，后合入的改号，并同步修改 `来源 T-NNN` 与计划中的引用。
  - **按复杂度写计划**：改动多个模块、新增核心库能力或需要分环节审查的，写工作计划（见下一条），条目只放链接；其余任务在条目下用 `计划：` 写几行步骤，然后开工。研究的预注册写在该研究的 `README.md` 中，不因此单独写 design 计划。
  - **开工**：把条目移到"进行中"，写上分支名，尽早推送分支并开草稿 PR（draft PR），让别的会话看得见。分支上的 `TODO.md` 改动要合并后才出现在 `main`，所以开工或分配编号之前，先看未合并的分支与 PR 是否已在做这件事或用了这个编号（`gh pr list`；各分支上用过的编号可用 `git grep -h -o "T-[0-9]\{3\}" $(git for-each-ref --format="%(refname)" refs/heads refs/remotes) -- TODO.md DONE.md` 查看）。
  - **不属于当前分支的问题不顺手修**：工作中发现的其他问题登记到"待办池"末尾，写明 `来源 T-NNN`，然后回到当前任务。
  - **完成或放弃**：在同一个分支里（被放弃的分支除外，见下条）把条目从 `TODO.md` 删除，加到 `DONE.md` 当月小节（`## YYYY-MM`，没有就在最上面新建）；条目按日期倒序，变基（rebase）遇到冲突时按日期重排。完成写 `[x]`、日期、PR 编号和一句结果（先开 PR，拿到编号后补进条目再合并），复杂任务再加计划链接；一个任务分多个 PR 时，条目留在"进行中"直到最后一个 PR，写最后的 PR 编号；放弃写 `[-]`、日期和原因。
  - **放弃或暂停一个分支**：删除分支之前，用一个小 PR 把它的状态落到 `main`：本分支的条目移入 `DONE.md` 标 `[-]` 并写原因，或者（暂停时）放回"下一步"/"待办池"并在 `备注：` 里写明进度；分支上新登记的其他条目一并带过去，不随分支丢失。
  - **整理**：每次改 `TODO.md` 时顺手看一眼待办池：失效的标 `[-]` 移走，变重要的提到"下一步"。
  - `STATUS.md` 不再列待办，只记全局状态与时间点；`python -m pytest` 会检查两个文件的格式与编号。
- **复杂任务先写工作计划（work plan）**：
  - 放在 `design/NNN-plan_<核心内容>.md`，编号取当前最大值加 1，文件名必须表达核心内容。
  - 在 `design/README.md` 索引中登记。
  - 执行过程中，在计划文末的"执行记录"一节追加进度。
- **从论文立项（paper study）**：一篇或几篇论文提出的问题要立为研究时，按 `paper-study` 技能的顺序做，设计与 Lean 方法见 `design/007-plan_*`：
  - **读原文**：可以用网页读取（只读）阅读论文全文，例如 arXiv 的 HTML 版或 PDF 页面，用于核实数字与摘录引文；不把论文文件保存到项目目录。
  - **先写 Wiki 文章**：`docs/wiki/Study-NNN-<slug>.md`，中英双语，指向仓库文件的链接一律用 `https://github.com/sudoghut/astrolab/...` 绝对网址；至少三部分：
    1. 科普详解：把论文的观点和论证细节讲清楚，不写成概述；
    2. 论证逻辑（学术性，专有名词要解释）：按我们对论证的分析拆成若干环节，不照抄原文章节；每个环节先概述，再用 Lean 4 拆分推理，并如实报告 Lean 检查发现的错误或不严密之处；
    3. 本项目可检验或探索的环节：能否检验或探索、怎么做、数据量多大；不能给出判决但可以探索的（例如结论对某个模型假设的敏感度），指向对话探索的入口。
    其他部分（术语表、开放问题、研究进展 changelog 等）按需要添加。为已经实现的研究补写文章时，第三部分标明"实现后补写（事后，post hoc）"，不作为预注册，并手工从模板补上 `argument/`、`README.md` 第 8 节与 `study.yaml` 的 `papers`、`wiki` 字段。
  - **Lean 论证**放在 `studies/<id>/argument/`，格式以模板 `studies/_template/argument/Argument.lean` 为准，`python -m pytest`（`tests/test_lean_arguments.py`）会检查。机器检查针对无心之失和省事的捷径；引文是否真实、编码是否忠实于原文、类型是否标对，由审查（双闸审查与独立审稿）负责。
    - 只用 Lean 4 核心库：不写 `require`，不引入 Mathlib 等外部包（数 GB，违背第一条）。`argument/` 中只放 `lakefile.toml`、`lean-toolchain`（两者都与模板相同，否则测试失败）和 `Argument.lean`；模板指定的工具链（toolchain）未安装时测试跳过而不是下载。安装或升级 Lean、改动 `lean-toolchain`、运行 `lake update` 或 `lake exe cache get` 都要先征得用户同意。
    - 结构：不写 `axiom`；词项（term）是结构体（structure）`Vocab` 的字段，只能是 `Prop`、`Type`、`Nat`/`Int` 数量、以前面的 `Type` 字段或 `Nat`/`Int` 为参数的谓词（predicate），或前面 `Type` 字段的元素，不能是证明；结论本质上就是一条观测的论文（如上限、未探测）要把这一步拆成计数与统计模型，否则不适用本方法；前提是归纳类型（inductive type）`Field` 的无参数构造子（constructor），内容写在 `prem` 中（每个构造子一条等式）；模板的两段固定代码（`Prov`；`Premises`、`Without`、`Stated`、`Explicit`）不得改动。`prem` 与 `Conclusion` 只能用 `Vocab` 的字段、逻辑联结词、整数字面量与比较（完整清单见 `design/007-plan_*` 第 2.2 节），不能引用自定义的辅助定义；任何前提都不在最外层用 `∧` 合并多条断言。
    - 标注：每个前提注明类型 `OBS`/`MOD`/`STAT`/`NUM`/`LIT`/`GAP` 与出处性质，出处性质相对于被分析的论文：论文明说 `[stated: "引文"]`（多篇论文时写 `[stated <arXiv 编号>: "引文"]`，编号须列在 `study.yaml` 的 `papers:` 中；引文内不能含 `"` 与 `]`）、论文依赖但没写出的标准知识 `[implied]`（须注明来源：文献码 bibcode、arXiv 编号或教科书）、我们补上的 `[reconstructed]`（论文发表之后的文献结论也属此类）。`LIT` 的注释须有文献码或 arXiv 编号。`GAP`（隐含前提，gap premise）当且仅当出处性质为 `reconstructed`。`OBS`/`NUM`/`STAT` 的内容只能是单个原子命题、其否定或数量关系；`NUM` 必须带结果绑定，论文给出而本仓库不复算的数字标 `OBS` 或 `STAT`。`[stated]` 前提的 Lean 内容不得强于引文。`Conclusion` 附上论文结论的原文引文。
    - 必须证明（陈述由测试固定，不能改写）：最终结论 `final`；结论并非恒真 `final_nontrivial`；前提相容 `consistent`；任何单个前提都推不出结论 `alone_insufficient`；每个前提要么必要（`<前提>_needed`，反例模型）要么多余（`<前提>_redundant`）；论文明说的前提是否足以推出结论（`stated_sufficient` 或 `stated_insufficient`：需要论文没写出的背景知识）；加上标准知识后是否足够（`explicit_sufficient` 或 `explicit_insufficient`：存在真正的缺口，即"论证不严密"的机器证据）。
    - 禁止：`sorry`、`admit`、`native_decide`、`decide +native`、`debug.skipKernelTC`、`unsafe`、`implemented_by`、`extern`，以及 `import`、宏与语法扩展（`macro`、`syntax`、`notation` 等）、`#eval`、`#guard`、`run_cmd`、`initialize`、`opaque`、`partial` 等（完整清单见 `design/007-plan_*` 第 2.2 节，按完整的标识符词元匹配，`initial_mass` 之类的名字不受影响）；注释以外不得出现字符串、字符字面量、撇号（`h'` 之类的名字）、`«»` 引号、属性（`@[...]`、`attribute`）和任何 `#` 命令；标识符只用 ASCII（`h1` 而不是 `h₁`）；`set_option` 只允许 `linter.*` 与 `maxHeartbeats`。测试先扫描源码再构建，再用不导入该模块的审计文件检查固定陈述、结构与形状，并审计每个常量的公理（只允许 `propext`、`Quot.sound`、`Classical.choice`）。
    - 数值不在 Lean 里算：`NUM` 前提用 `NUM[results/<文件>.json:<键> <比较> <值>]` 绑定到 `run.py` 的结果（路径相对研究目录，键用点号表示嵌套，比较为 `<`、`<=`、`>`、`>=`、`==`，`==` 的容差为 `max(1e-9·|值|, 1e-12)`），由测试核对，并核对绑定与 Lean 中的阈值一致；研究状态为 reproduced 或 concluded 时结果文件与键必须存在。
    - 只在 Dropbox 之外构建：测试会把 `argument/` 复制到临时目录执行 `lake build --wfail`。不要在项目目录里运行 `lake build` 或用编辑器打开 Lean 文件（都会在 Dropbox 中生成 `.lake/`）。与模板完全相同的 `argument/`（非论文研究未删除的示例）不检查；但 `study.yaml` 的 `papers:` 非空时，`argument/` 必须存在且不同于模板。
  - **预注册与实现**（待办条目在动手前已登记；按第二条的复杂度标准决定是否写 design 计划，分环节审查的论文研究通常要写，至少在条目下写 `计划：`）：研究的预注册（问题、判据、数据、方法）写在研究 `README.md` 第 1–4 节，由 Wiki 第三部分导出，然后实现 `run.py` 与网页。`run.py` 把可调参数集中在文件开头的 `PARAMS` 字典里，并随结果一起保存；`main()` 在调用时读取 `PARAMS` 并把取值作为参数传给辅助模块，不在导入时据此计算模块级常量，辅助模块也不自行 `import run`（否则探索时的覆盖不生效）。`README.md` 第 8 节写明对话探索（exploring via chat）的入口，方便用户通过与编程智能体对话来探索研究。
  - **对话探索不改动正式结果**：用 `python -m astrolab explore <id> --tag <主题> [--set 键=值 ...] [--script explore/<名>.py]` 运行：它在内存中覆盖 `PARAMS`（或运行 `explore/` 下带 `main(ctx)` 的脚本），取数仍走受守卫的通道与研究预算，输出（含来源记录）写到 `studies/<id>/explore/<日期>-<主题>/`，不碰 `results/`（主题只能用小写字母、数字和连字符，脚本必须在 `explore/` 下，命令会拒绝越出 `explore/` 的路径）。同一天同一主题再次运行会覆盖原目录。探索输出不入库、每个文件不超过 1 MB，用完即删；探索脚本直接放在 `explore/` 下，可以入库（`explore/` 的子目录一律视为输出，不入库）。只运行探索不需要分支；把发现写进 `log.md`、Wiki 或脚本时，照常走分支与 PR。修改正式 `PARAMS` 等同于修改预注册，要写明日期与理由。
  - **回写并保持同步**：实现后在 Wiki 第三部分补充实际结果（保留原来的可检验性表格，不改写成事后选择的样子）；之后研究的任何新变化（新结果、审稿意见、改变认识的对话探索发现、更正）都在同一个 PR 里更新 Wiki 文章及其"研究进展"一节，首次加入文章的 PR 同时在 `docs/wiki/Home.md` 中英两处登记链接。Wiki 仓库不经过审查，只改 `docs/wiki/` 中的源文件，合并后再推送（步骤见 `paper-study` 技能）。
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
  - 中文字段：结论条目（claims）加 `title_zh`、`statement_zh`，`study.yaml` 加 `title_zh`、`question_zh`。新建结论或研究时必须同时填写；`python -m astrolab claims check` 与测试会检查它们含有中文、且不是模板占位符（`TODO…`）。网页在中文模式下显示中文字段。
  - 天体名称、星表编号、数值、单位、文献引用、代码与命令不翻译。
- **引用前先核实**：路线图中标为 [S] 或 [U] 的条目，动手前要提升到 [V]，即对照原文核实。
- **及时抽出技能（skills）**：某个研究动作第二次出现，或者步骤多、容易做错时，就把它写成技能，放在 `.claude/skills/<name>/SKILL.md`。
  - 已有技能：独立审稿（referee）、服务器端查询（server-side query）、双闸代码审查（dual-gate review）、从论文立项（paper-study）。待抽出的技能登记在 `TODO.md`。
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
| `TODO.md` / `DONE.md` | 待办清单与完成日志（见第二条） |
| `docs/wiki/` | Wiki 页面的源文件（含论文研究文章 `Study-NNN-<slug>.md`），合并后推送到 Wiki 仓库 |

单个研究文件夹的内容：

| 文件 | 作用 |
|---|---|
| `study.yaml` | 元数据：层级、状态、关联结论、足迹（footprint） |
| `README.md` | 问题、假设与判据、数据（附大小估计）、方法、结果、审稿意见、开放问题、对话探索入口（第 8 节） |
| `log.md` | 研究日志（research log），按时间倒序追加 |
| `run.py` | `def main(ctx)`，用 `ctx.tap / ctx.http / ctx.save / ctx.log` |
| `test_conclusions.py` | 读取 `results/`，断言结论仍然成立 |
| `argument/` | 论文研究的 Lean 4 论证拆解（Lake 项目，Lake 是 Lean 的构建工具；入口 `Argument.lean`）；非论文研究可删除 |
| `explore/` | 对话探索：脚本可入库；`<日期>-<主题>/` 输出不入库（见第二条），不影响 `results/` |
| `web/` | 为该问题设计的网页，读取 `../results/*.json`。形式完全按研究需要来：可以是可视化、交互式数据分析、多页面或专用工具，**不必拘泥于 Atlas 的样式或结构**；`atlas/web/base.css` 可用可不用，但必须引用 `atlas/web/i18n.js`（见第二条双语规则） |

**Atlas 与研究网页的分工**：Atlas 是总图，只负责宏观导航（各尺度的结论与研究落在哪里）。局部的研究、可视化与数据分析都在各自的 `studies/<id>/web/` 中灵活设计。

## 第五条：研究完成标准

- README 已填写完整。
- `run.py` 可以重跑。
- 测试通过。
- 网页可用。
- 关联结论条目已更新复现值（`ours`）与状态。
- `log.md` 和 `STATUS.md` 已更新；`TODO.md` 中的条目已移入 `DONE.md`。
- 论文研究：Wiki 文章已与研究同步（第三部分反映实际结果，研究进展已记录），`tests/test_lean_arguments.py` 对该研究实际运行并通过（跳过不算通过）。
- 已做过独立审稿（referee）：派一个子智能体（subagent），只给它代码与结果，不给我们的结论，专门找系统误差（systematics）与选择效应（selection effects）。论文研究另给它 Lean 测试生成的"引文—类型—内容"对照表，核对每个 `[stated]` 前提不强于引文、`GAP` 标注如实。
