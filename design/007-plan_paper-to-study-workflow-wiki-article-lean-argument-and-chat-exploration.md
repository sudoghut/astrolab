# 007 · 工作计划：从论文立项的研究流程——Wiki 文章、Lean 论证拆解与对话式探索

状态：完成
创建：2026-11-14
待办条目：T-009

## 1. 目标

把"一篇或几篇论文提出的问题 → 一个研究（study）"的流程固定下来，供人和编程智能体（coding agent）共用。待办清单（to-do list）与 design 文献的规范见 `AGENTS.md` 第二条与 006 号计划，这里不重复。

流程分五步：

1. **先写 Wiki 文章**（中英双语），至少三部分：
   - **第一部分 · 科普详解**：用科普方式把论文讲细，包括观点和论证细节，让读者真正了解论文做了什么、怎么做的；不写成概述。
   - **第二部分 · 论证逻辑**（学术性，专有名词要解释）：按我们对论证的分析把论文拆成若干环节（不照抄原文章节）；每个环节先概述，再用 Lean 4 拆分论证、梳理推理过程；Lean 检查中发现的错误或不严密之处要明确指出。
   - **第三部分 · 本项目可检验或探索的环节**（学术性）：哪些环节能用本仓库检验或探索、怎么做、需要多少数据。
   - 其他部分按需要设计，例如术语表（glossary）、研究进展（changelog）、开放问题。
2. **按待办清单纪律写研究计划并实现**：登记条目；研究 `README.md` 第 1–4 节预注册（pre-registration）；`run.py` 实现；`web/` 可视化。
3. **支持对话式探索**：用户可能通过与编程智能体对话来和研究互动。研究要留下让智能体接得住的入口：可调参数、离线可重跑、结果文件说明、探索记录的位置。
4. **回写 Wiki 第三部分**：根据实现过程与结果重新充实第三部分。
5. **持续同步**：研究的新变化（新结果、审稿意见、对话探索的发现、更正）都要更新到 Wiki 文章中。

## 2. 设计

### 2.1 文件与位置

| 内容 | 位置 | 说明 |
|---|---|---|
| 流程技能 | `.claude/skills/paper-study/SKILL.md` | 分步流程与检查清单；具体规则仍以 `AGENTS.md` 为准 |
| Wiki 文章模板 | `.claude/skills/paper-study/wiki-article-template.md` | 放在技能目录里，不放 `docs/wiki/`，以免被当作页面发布 |
| Wiki 文章 | `docs/wiki/Study-NNN-<slug>.md` | 与 005 号计划相同：源文件在主仓库审查，合并后推送到 Wiki 仓库 |
| Lean 论证 | `studies/NNN-slug/argument/` | 独立的 Lake（Lean 构建工具）项目：`lakefile.toml`、`lean-toolchain`、`Argument.lean` |
| 研究元数据 | `study.yaml` 新增 `papers`（arXiv 编号列表）与 `wiki`（页面名） | 让 Atlas、网页和智能体能找到论文与文章 |
| 探索 | `studies/NNN-slug/explore/` | 对话探索的脚本（入库）与输出（不入库），见 2.3 |
| 对话探索入口 | 研究 `README.md` 新增第 8 节"对话探索（exploring via chat）" | 列出可调参数、重跑命令、结果文件、探索记录方式 |

### 2.2 Lean 的用法

**原则。** 只用 Lean 4 核心库，不引入数学库 Mathlib（及其缓存，数 GB，违背 `AGENTS.md` 第一条）。本机已装 Lean 4.35.0，由工具链管理器 elan 管理；Lake 是 Lean 的构建工具。论证结构用命题逻辑与一阶逻辑即可表达。

**为什么不用全局公理（axiom）。** 闸门 1（gate 1，审查子智能体）的方法审查用实验证明：前提写成全局 `axiom` 时，智能体可以把结论本身写成一条"前提"，或者写入互相矛盾的前提，构建照样通过；全局公理也无法代入具体取值，写不出反例模型（countermodel）。

**威胁模型（threat model）。** 机器检查针对的是诚实但会出错的智能体：无心之失、省事的捷径（改标签、把结论写成前提、用 `sorry`/`admit` 糊过去、把推理藏进词项）。蓄意而精巧的规避，以及机器原理上无法判断的事（引文是否真在论文里、编码是否比原文更强、类型是否标对、`final` 是否忠实于论文结论），由双闸审查（dual-gate review）与独立审稿（referee）负责；测试会打印"引文—类型—Lean 内容"对照表供审查者核对。

**方案：按编号索引的前提（indexed premises）。** 格式以 `studies/_template/argument/Argument.lean` 为准，下面是测试据以实现的精确规格。

*文件布局*（`namespace Argument` 内，依次）：
1. 固定块 A：`inductive Prov where | stated | implied | reconstructed deriving DecidableEq`。
2. `structure Vocab`、`inductive Field`、`def prov`、`def prem`、`def Conclusion`（研究自己写）。
3. 固定块 B：
   - `def Premises (v : Vocab) : Prop := ∀ f, prem f v`
   - `def Without (g : Field) (v : Vocab) : Prop := ∀ f, f ≠ g → prem f v`
   - `def Stated (v : Vocab) : Prop := ∀ f, prov f = .stated → prem f v`
   - `def Explicit (v : Vocab) : Prop := ∀ f, prov f ≠ .reconstructed → prem f v`
4. 定理。

两个固定块在去掉注释后按词元（token）与模板逐一比较，以首个词元序列（`inductive Prov where`、`def Premises`）定位；审计另外检查 `Prov` 的结构，并用表达式相等核对四个定义。`Prov` 必须固定，否则可以另行定义 `Prov.stated` 篡改 `Stated` 的含义。

*`Vocab`*：字段类型只能是 `Prop`、`Type`、`Nat`、`Int`；`T₁ → … → Prop`，其中每个 `Tᵢ` 是前面的 `Type` 字段、`Nat` 或 `Int`；或前面某个 `Type` 字段的元素。不能是证明，也不能是携带证明的数据。每个字段有文档注释（doc comment）写明操作含义（测试检查注释存在）。

*`Field`*：无参数、无索引；每个构造子（constructor）不带参数；`deriving DecidableEq`（可加 `Repr`）。文档注释格式 `KIND [provenance] source`：
- KIND ∈ `OBS` 观测、`MOD` 模型假设、`STAT` 统计推断、`NUM` 数值结果、`LIT` 外部文献、`GAP` 隐含前提；
- provenance（出处性质，相对于被分析的论文）∈ `[stated: "引文"]`（多篇论文时 `[stated <arXiv 编号>: "引文"]`，编号须在 `study.yaml` 的 `papers:` 中；引文内不得含 `"` 与 `]`）、`[implied]`（论文依赖但没写出的标准知识，`]` 之后须有非空的来源文字：文献码 bibcode、arXiv 编号或教科书名）、`[reconstructed]`（我们补上的）；论文发表之后的文献结论属于 `[reconstructed]`（标 `GAP`，注明文献码），因为论文不可能依赖它；
- `GAP` 当且仅当 `[reconstructed]`；`GAP` 不能是 `[stated]`；
- `OBS`/`NUM`/`STAT` 的内容是"文字式"（literal）：原子、`¬` 原子或数量关系；
- `NUM` 必须带结果绑定（见下）；论文给出而本仓库不复算的数字标 `OBS` 或 `STAT`；
- `LIT` 的注释须有文献码或 arXiv 编号。

*`prov` 与 `prem`*：`prov` 对每个构造子一条等式；`prem` 对每个构造子一条等式（`| .c, v => …` 或 `match f with` 形式均可），不用通配符、不用 `if`。审计在环境中求值 `prov c`，与注释核对。

*形状文法（在展开后的项上检查）*：
- 原子：`Prop` 字段；或谓词字段作用于 `Type` 字段的元素、字面量或约束变量。
- 数量关系：`Nat`/`Int` 字段与字面量之间的 `=`、`≠`、`<`、`≤`、`>`、`≥`；在非文字式（`MOD`/`LIT`/`GAP`）中，还允许两个同类型 `Nat`/`Int` 字段之间的比较，以及两个 `Type` 元素之间的 `=`/`≠`（例如"测得质量大于中子星质量上限"、"光学源与 X 射线源是同一天体"）。
- 文字式：原子、`¬ 原子`、数量关系或其否定（`p → False` 视同 `¬ p`）。
- `prem` 与 `Conclusion` 允许出现的常量：`Vocab` 的投影；`Not And Or Iff Exists True False Eq Ne`；`LE.le LT.lt GE.ge GT.gt`；`OfNat.ofNat Neg.neg`；`Nat Int`；`instOfNatNat instOfNat instLENat instLTNat Int.instLEInt Int.instLTInt Int.instNegInt`。这是封闭清单。每个前提的内容至少含一个 `Vocab` 投影（防止通配符分支给出 `True` 之类的空前提）。不允许加法、乘法与任何辅助定义（需要算术时在 `run.py` 中算好，以放大后的整数阈值进入 Lean）。
- 每个前提的最外层不能是 `∧`。`Conclusion` 按非文字式规则检查（可含字段之间的比较），并且可以是 `∧`（论文有两个主要结论时）。约束变量（如 `∀ n : Nat`）可以出现在谓词参数与比较中。
- 审计为每个前提输出最外层联结词、是否为文字式、`NUM` 形式、越界常量与 Lean 内容，Python 据此判断。

*`NUM` 绑定*：注释中写一个或多个 `NUM[<路径>:<键> <比较> <值>]`，正则为
`NUM\[(results/[^:\]]+\.json):([A-Za-z0-9_.-]+)\s*(<=|>=|==|<|>)\s*(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\]`。绑定必须与 Lean 中的阈值一致：先把 Lean 关系规范为"字段在左"（`5 ≤ v.x` 视同 `v.x ≥ 5`），比较方向必须相同（`≥ > ≤ < =` 分别对应 `>= > <= < ==`），且绑定值等于 Lean 字面量除以 10 的某个整数次幂（0 到 9 次）；一个前提有多个绑定时每个都要满足；`NUM` 前提必须是"字段 比较 字面量"的形式（`≠` 和否定的关系不能作为 `NUM`，原子形式的数值结论标 `OBS`/`STAT`）。路径相对研究目录；键用点号表示嵌套（不支持数组下标）；值必须是 JSON 数（布尔、字符串、NaN 即失败）；`==` 的容差为 `max(1e-9·|值|, 1e-12)`；文件存在而键缺失即失败；文件不存在时，研究状态为 reproduced/concluded 则失败，否则跳过（测试输出中注明）。绑定与原子含义是否一致（"超过"对应 `>`）由审查者核对。

*定理名*：前提 `Argument.Field.c` 对应 `Argument.c_needed` 或 `Argument.c_redundant`；只考虑 `Argument` 命名空间顶层、末段以 `_needed`/`_redundant` 结尾的名字（忽略 `._proof_1`、`.match_1` 等内部名字）；对应不到前提的即失败。

*必须证明的定理*（审计把当前命名空间设为 `Argument`，以不含记号的形式书写并与 `ci.type` 做表达式相等比较；实现中逻辑常量写作 `_root_.Not`、`_root_.Exists`、`_root_.Eq`、`_root_.Ne`，防止研究文件里同名的定义遮蔽它们。确切字符串：`∀ v, Premises v → Conclusion v`；`Not (∀ v : Vocab, Conclusion v)`；`Exists (fun v => Premises v)`；`∀ g, Not (∀ v, prem g v → Conclusion v)`；`Not (∀ v, Without Field.c v → Conclusion v)` 与 `∀ v, Without Field.c v → Conclusion v`；`∀ v, Stated v → Conclusion v` 与其 `Not (…)`；`∀ v, Explicit v → Conclusion v` 与其 `Not (…)`。固定块 B 的定义体：`fun v => ∀ f, prem f v`；`fun g v => ∀ f, Ne f g → prem f v`；`fun v => ∀ f, Eq (prov f) Prov.stated → prem f v`；`fun v => ∀ f, Ne (prov f) Prov.reconstructed → prem f v`）：

| 定理 | 陈述 | 作用 |
|---|---|---|
| `final` | `∀ v, Premises v → Conclusion v` | 论证成立 |
| `final_nontrivial` | `¬ ∀ v : Vocab, Conclusion v` | 结论不是恒真 |
| `consistent` | `∃ v, Premises v` | 前提相容（只有含否定或互斥前提时才有分量） |
| `alone_insufficient` | `∀ g, ¬ ∀ v, prem g v → Conclusion v` | 任何单个前提都推不出结论：抓"把结论直接写成一条前提"（拆成两条前提的偷渡仍要靠审查）。结论本质上就是一条观测的论文（例如上限、未探测），把这一步拆成计数与统计模型，否则不适用本方法 |
| `<c>_needed` 或 `<c>_redundant`（每个前提恰好一个） | `¬ ∀ v, Without .c v → Conclusion v` / `∀ v, Without .c v → Conclusion v` | 前提必要（反例模型）或多余（证明） |
| `stated_sufficient` 或 `stated_insufficient`（恰好一个） | `∀ v, Stated v → Conclusion v` / 其否定 | 论文写出的前提是否足够；不够时说明论证依赖没写出的背景知识或缺口 |
| `explicit_sufficient` 或 `explicit_insufficient`（恰好一个） | `∀ v, Explicit v → Conclusion v` / 其否定 | 加上标准知识（`implied`）后是否足够；不够即存在真正的缺口（`GAP`），这是"论证不严密"的机器证据，也是文章最重要的单项结论 |

*篇幅*：反例模型通常一行：具体的 `Vocab` 加 `by intro f hf; cases f <;> simp_all [prem]`（`_needed`），`stated_*`/`explicit_*` 用 `simp_all [prov, prem]`（多余的 simp 参数会被 `--wfail` 当作错误）；32 个前提的实验构建约 2 秒、审计约 4 秒。

*多余的前提*：如果一个前提的原子在其他前提和结论中都没有出现，它必然多余——这是编码的产物（例如没有编码 `NUM` 对 `OBS` 的依赖），不是对论文的发现，文章要这样说明。

*局限*（文章要写明）：Lean 检查的是在我们的编码下论证结构是否成立，不检查每个前提内部的物理；原子不加解释时，"必要"的含义是"本编码用到了它"；不确定度被折算成我们选定的整数阈值；"很可能是黑洞"这类保留措辞被编码为断言；统计推断被写成演绎的判定规则。

**机器检查（`tests/test_lean_arguments.py`）的顺序。**

1. **扫描源码（构建之前；不需要 Lean，未安装 Lean 时也运行）**：`argument/` 只能有 `lakefile.toml`、`lean-toolchain`（与模板相同，按统一换行符比较，否则失败）和 `Argument.lean`；模板的工具链未安装（`elan toolchain list`）时跳过构建与审计（扫描照常运行），绝不调用 `lake` 触发下载。用理解嵌套注释的词法器（lexer）去掉注释后：不得有字符串、字符字面量、撇号、`«`、属性（`@[`、`attribute`）与任何 `#` 命令；非 ASCII 字符只允许逻辑与括号符号（`→ ← ↔ ∀ ∃ ¬ ∧ ∨ ≠ ≤ ≥ ⟨ ⟩ · × λ ▸`），因此标识符只用 ASCII；按完整的词元匹配（标识符按带点名字的每一段；`#eval` 等以 `#` 开头的命令按整个命令词元；`decide` 后接 `+native` 按相邻词元），禁止 `axiom`、`sorry`、`admit`、`native_decide`、`decide` 后接 `+native`、`debug.skipKernelTC`、`unsafe`、`implemented_by`、`extern`、`import`、`macro`、`macro_rules`、`syntax`、`declare_syntax_cat`、`notation`、`infix`/`infixl`/`infixr`、`prefix`、`postfix`、`binder_predicate`、`elab`、`elab_rules`、`#eval`、`#guard`、`#reduce`、`#exit`、`run_cmd`、`run_elab`、`run_meta`、`initialize`、`builtin_initialize`、`opaque`、`partial`、`app_unexpander`；`set_option`（全局、`in` 与战术内形式都适用）后面的选项名只能以 `linter.` 开头或恰为 `maxHeartbeats`；两个固定块与模板逐词元相同。先扫描再构建，因为 `#eval` 在构建时就会执行任意命令。
2. **构建**：复制到 Dropbox 之外的临时目录，执行 `lake build --wfail`。
3. **审计**：生成的审计文件不导入 `Argument`，运行时加载其 `.olean`，因此 `Argument` 中的宏无法改写审计；运行时加载不含记号扩展，所以固定陈述以不含记号的形式书写。审计内容：固定陈述的表达式相等；固定块的结构与定义；每个常量的公理只允许 `propext`、`Quot.sound`、`Classical.choice`；拒绝类型涉及 `Lean.*`、`IO` 的声明；`Vocab` 字段类型与文档注释；`Field` 的结构；逐个前提读取注释、求值 `prov`、展开 `prem`（展开任何末段以 `match_` 开头的匹配函数）并按形状文法输出；同样检查 `Conclusion`。输出机器可读的报告并以固定成功标记结尾，缺少标记即失败。
4. **Python 核对报告**：类型与出处性质合法且与 `prov` 一致；`GAP` ⇔ `reconstructed`；形状规则；定理名对应；`stated_*` 与 `explicit_*` 各恰好一个；`NUM` 绑定。把"引文—类型—内容"对照表写到临时目录的报告文件，路径打印在测试输出中，供审稿使用。
5. **覆盖范围**：`study.yaml` 写了 `wiki:`（页面名，如 `Study-012-x`，不带 `.md`）时，`docs/wiki/<wiki>.md` 必须存在；`papers:` 非空时，`argument/` 必须存在且不同于模板；与模板完全相同的 `argument/` 不检查。对论文研究，完成标准要求测试实际运行并通过，跳过不算。

**下载约束。** 安装或升级 Lean、改动 `lean-toolchain`、`lake update`、`lake exe cache get` 都可能触发数百 MB 的下载，需先征得用户同意。

### 2.3 对话探索

- 新增命令 `python -m astrolab explore <id> --tag <主题> [--set 键=值 ...] [--script explore/<名>.py]`：
  - 不带 `--script` 时导入 `run.py`，在内存中用 `--set` 覆盖 `PARAMS` 后运行 `main(ctx)`；带 `--script` 时运行该脚本的 `main(ctx)`；
  - `ctx` 与正式运行相同（受守卫的取数、缓存、研究预算），但输出目录改为 `studies/<id>/explore/<日期>-<主题>/`，来源记录与运行信息（含覆盖的参数）也写在那里；`results/` 不受影响；
  - `--tag` 只能由小写字母、数字和连字符组成（`[a-z0-9-]{1,40}`），`--script` 必须是 `explore/` 下的 `.py` 文件；解析后的输出目录与脚本路径必须位于 `studies/<id>/explore/` 之内，否则报错（防止路径穿越覆盖正式结果）；
  - 未知的参数名报错；值按 JSON 解析，并要求与默认值类型一致（整数可赋给浮点参数），否则报错；
  - 同一天同一主题再次运行会覆盖原目录；`run.py` 的 `main()` 与辅助模块须在调用时读取 `PARAMS`，命令把覆盖后的参数写入运行信息。
- `.gitignore` 忽略 `studies/*/explore/*/`（输出不入库，脚本可入库）；输出用完即删；探索运行时 `ctx.save` 拒绝超过 1 MB 的文件；`pytest` 不收集 `explore/` 与 `argument/`。
- 只运行探索不需要分支；把发现写进 `log.md`、Wiki 或脚本时，照常走分支与 PR。修改正式 `PARAMS` 等同于修改预注册。
- 研究 `README.md` 第 8 节列出可调参数（含义、安全范围、是否需要新数据）、示例问题、结果文件与键。

### 2.4 Wiki 文章的同步纪律

- 研究完成标准（`AGENTS.md` 第五条）加一条：Wiki 文章已与研究同步，Lean 检查通过。
- 第三部分最初的可检验性表格是预注册的来源，实现后只补充结果，不改写。
- 文章末尾的"研究进展（changelog）"按时间倒序记录每次更新。
- 只改 `docs/wiki/` 中的源文件；首页 `docs/wiki/Home.md` 的链接在同一个 PR 里加上（中英两处）；合并后按 005 号计划推送到 Wiki 仓库。

### 2.5 与待办清单的关系

- 一个论文研究在 `TODO.md` 中登记一个条目；是否写 design 计划按 `AGENTS.md` 第二条的复杂度标准判断（分环节审查的论文研究通常要写）。
- T-006（新建研究技能）保留：本任务的技能只覆盖"从论文新建研究"，不从论文出发的研究仍需另外的技能。

## 3. 步骤

分两个环节（stage），每个环节结束做双闸审查（dual-gate review）。

1. **规则与技能**：本计划、`TODO.md` 登记、`AGENTS.md`（立项流程、Lean 规则、完成标准）、`paper-study` 技能、Wiki 文章模板、`docs/wiki/Home.md` 加"论文研究"栏目。
2. **研究模板、Lean 骨架与探索命令**：`studies/_template/` 加 `argument/`（按 2.2 方案、能通过全部检查的示例）、`README.md` 第 8 节、`study.yaml` 新字段（`papers`、`wiki`）；`.gitignore`（`.lake/`、探索输出）；`pyproject.toml` 的 `norecursedirs`；`astrolab/study.py` 复制模板时跳过 `.lake/`，新增探索运行；`astrolab/cli.py` 新增 `explore` 子命令；`tests/test_lean_arguments.py`（2.2 的机器检查）与探索命令的测试；确认 `python -m astrolab new` 能正确复制。

完成后提交、开 PR、以变基合并（rebase merge）进入 `main`。

## 4. 验收标准

- 两个环节都通过双闸审查，没有遗留的严重问题。
- `python -m pytest` 通过；模板中的 Lean 项目通过检查；故意写入 `sorry`、`admit`、`axiom`、宏、改写过的固定陈述、缺少 `_needed`/`_redundant` 或错误的 `NUM` 绑定时测试失败；`explore` 命令不改动 `results/`。
- 新会话的智能体只读 `AGENTS.md` 和 `paper-study` 技能，就能从一篇论文走完整个流程。

## 5. 执行记录

- 2026-11-14：建分支 `feat/paper-study-workflow`；登记 T-009，试点任务登记为 T-010（待办池）。确认本机 Lean 4.35.0 可用。
- 2026-11-14 · 环节 1 闸门 1 第 1 轮（两名审查者：规则一致性；方法论）：共 6 个严重问题。方法审查用 Lean 实验证明全局公理方案可以"偷渡"结论、容纳矛盾前提、写不出反例模型，且 `lake build` 遇到 `sorry` 仍成功——改为 2.2 的结构体方案（相容性模型、必要性反例、出处性质、其他解释表、`NUM` 绑定、`--wfail` 与公理白名单）；对话探索可能覆盖正式结果、绕过受守卫通道——新增 2.3；工具链版本不符会触发自动下载——固定工具链并要求先征得同意。次要意见大多采纳：第三部分改为"补充"而非"重写"、首页链接在 PR 内完成、删去推送时排除 `_` 开头文件的错误说法、T-006 保留、立项时提醒填写中文字段、模板中英两半对齐、多篇论文的写法。
- 2026-11-14 · 环节 1 闸门 1 第 2 轮：8 个严重问题。方法审查再次用实验找出漏洞：只检查定理名、不检查陈述；只要求 `GAP`/`MOD` 必要，改标签即可绕过；`admit` 加关闭警告能通过 `--wfail`；宏能改写被固定的陈述，`#eval` 能在测试中执行任意命令；"原文前提"由智能体自定义。改为按编号索引的前提与固定头部、测试生成 `Check.lean` 固定陈述并审计全部常量的公理、语法黑名单与文件白名单、`alone_insufficient`/`final_nontrivial`/`stated_*`。规则审查发现探索脚本无法导入 `astrolab`、改参数探索没有可行机制、必要性规则与"多余"相矛盾：新增 `python -m astrolab explore` 命令（环节 2 实现），每个前提证明必要或多余二选一。次要意见：第三部分表格加判据列、首页链接在首个 PR 中加、写明 Wiki 推送步骤、补写已有研究时标明事后、design 计划与 README 的分工、探索输出不入库。
- 2026-11-14 · 环节 1 闸门 1 第 3 轮：7 个严重问题，均有 Lean 实验佐证：`Prov` 不在固定头部可被另行定义；`Vocab` 字段可以是证明，把推理藏起来；`Field` 构造子带默认参数可制造去不掉的隐藏前提；形状规则若按文本检查，`->`、`And`、辅助定义都能绕过；扫描若放在构建之后，`#eval` 已经执行，且朴素的去注释可被字符字面量骗过，审计文件若导入 `Argument` 会被宏改写；工具链不同时"跳过"可被利用。修订：写明威胁模型（机器检查防无心之失与捷径，蓄意规避与引文真实性由审查负责）；`Prov` 入固定头部；结构与形状在展开后的项上检查；扫描先于构建并采用"失败即关闭"（禁止字符串、`«»`，只用 ASCII）；审计文件不导入 `Argument`（审查者提供的原型已验证）；工具链不同即失败、未安装才跳过；补齐 `NUM`、`LIT` 的细则；对话探索要求在调用时读取 `PARAMS`、类型一致的覆盖、同名覆盖与用完即删；规则补入 `AGENTS.md`（读原文全文、Wiki 绝对链接、补写已有研究标明事后、跳过不算通过）。
- 2026-11-14 · 环节 1 闸门 1 第 4 轮（审查时已声明威胁模型）：3 个严重问题。数量关系与"只能用逻辑联结词"相矛盾——列出完整的常量白名单，允许 `Nat`/`Int` 字段；固定头部含 `Prov` 后无法成为一段连续代码——拆成固定块 A、B，按词元比较；"非 `stated` 的复合前提一律 `GAP`"使教科书式推理无法标为 `MOD [implied]`，并让 `stated_insufficient` 几乎必然成立——改为 `GAP` ⇔ `reconstructed`，新增固定定义 `Explicit` 与 `explicit_sufficient`/`explicit_insufficient`，区分"依赖没写出的背景知识"和"真正的缺口"。同时补齐形状文法、`NUM` 正则与容差、定理名对应、`set_option` 形式、运行时加载不含记号扩展等实现细节；`AGENTS.md` 补上"`[stated]` 内容不强于引文"、审稿时附对照表、补写已有研究时手工补齐模板文件、`papers:` 非空时必须有 `argument/`、design 计划按复杂度决定。
- 2026-11-14 · 环节 1 闸门 1 第 5 轮：规则审查 1 个严重问题——用户要求第三部分写"可检验或探索"的环节，"探索"一半在 `AGENTS.md` 与模板中丢失；已补上，并新增"可探索（不能判决）"状态，指向对话探索入口。方法审查无严重问题（按规格写出实例并通过构建与审计验证）；采纳其次要意见：两种反例写法、固定陈述的确切字符串、封闭的常量清单、字段之间的比较、`NUM` 绑定与 Lean 阈值一致、拒绝不含 `Vocab` 投影的空前提、论文之后的文献标 `GAP`、按完整词元匹配黑名单。
- 2026-11-14 · 环节 1（规则与技能）通过双闸审查：闸门 1 共 6 轮（第 1–5 轮每轮两名审查者：规则一致性、方法论；第 6 轮一名），严重问题依次为 6、8、7、3、1、0 个，修订见上面各条。闸门 2（Codex）共 3 轮，走本机代理：第 1 轮 1 个严重问题——探索命令的 `--tag` 直接拼进输出路径，可能路径穿越覆盖正式结果，已规定主题字符与路径必须留在 `explore/` 内；第 2 轮 1 个严重问题——技能在写文章前就新建研究目录，顺序看似颠倒；未改顺序，而是写明目录只是脚手架（文章的 Lean 文件在 `argument/` 中、页面名用研究编号），预注册、`run.py` 与网页仍在文章之后；第 3 轮无问题。
- 2026-11-14 · 环节 2（研究模板、Lean 骨架与探索命令）通过双闸审查：
  - 闸门 1 共 2 轮。第 1 轮两名审查者（Lean 检查；探索命令与模板）：1 个严重问题——`OBS`/`NUM`/`STAT` 的"文字式"接受了字段之间的比较和命题等式（可借 `(A ∧ B) = True` 偷渡合取）；已限定为 `Nat`/`Int` 字段（或约束变量）与整数字面量的比较。同时采纳：固定陈述改用 `_root_.` 名字防遮蔽；无 Lean 时也运行源码扫描；审计输出每个前提与结论的 Lean 内容，写入供审稿的对照表；格式错误的 JSON、旧式与带版本号的 arXiv 编号、空引文、未加引号的 arXiv 编号；自测断言拒绝原因并补充变体。探索命令：`ctx.save` 拒绝带路径的名字与保留名、写入前按实际格式检查 1 MB、覆盖参数的溢出与 NaN、字符串参数按原文、恢复 `sys.path`、脚本必须直接位于 `explore/`、运行信息记录完整参数。第 2 轮无严重问题。
  - 闸门 2（Codex）共 2 轮，走本机代理：第 1 轮 1 个严重问题——`explore/` 若是指向 `results/` 的符号链接，包含关系检查会放行；已要求解析后的 `explore/` 恰为研究目录下的真实文件夹，并加测试。第 2 轮无严重问题（次要意见：探索的来源记录不受 1 MB 上限约束，未采纳：来源记录只有元数据，规模随查询次数线性增长，远小于上限）。
  - `python -m pytest` 全部通过（模板 Lean 论证构建与审计约 30 秒）。
- 2026-11-14：T-006（新建研究技能）保留在待办池；试点 T-010（为 M4 补写文章与 Lean 拆解）留待下一步。
- 2026-11-14：开 PR #5，T-009 移入 `DONE.md`，以变基合并进入 `main`，随后把 `docs/wiki/Home.md` 推送到 Wiki 仓库。
