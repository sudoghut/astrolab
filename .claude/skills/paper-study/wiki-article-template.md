# {{Short title of the question}}

[English](#english) · [中文](#中文)

*Paper(s): {{Author et al. YEAR, Journal Vol, page, arXiv:XXXX.XXXXX}}. Study:
[`studies/{{NNN-slug}}`](https://github.com/sudoghut/astrolab/tree/main/studies/{{NNN-slug}}).
Status: {{planned / active / reproduced / concluded / paused / abandoned}}. Last updated: {{YYYY-MM-DD}} (see the
changelog at the end). The source of this page lives in the main repository at
[`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki); edit it there.*

*中文标题：{{中文标题}}。状态：{{计划中 / 进行中 / 已复现 / 已完成 / 暂停 / 放弃}}。论文：{{作者 等 年份, 期刊 卷, 页, arXiv:XXXX.XXXXX}}。研究：[`studies/{{NNN-slug}}`](https://github.com/sudoghut/astrolab/tree/main/studies/{{NNN-slug}})。最后更新：{{YYYY-MM-DD}}（见文末"研究进展"）。本页源文件在主仓库的 [`docs/wiki/`](https://github.com/sudoghut/astrolab/tree/main/docs/wiki) 中，请在那里修改。*

<!--
Template notes (delete this comment in a real article):
- Workflow and checklists: .claude/skills/paper-study/SKILL.md. Rules: AGENTS.md section 2.
- Part 1 is plain language but DETAILED: the reader should come away knowing what was measured,
  how, which numbers came out, and why the authors believe their conclusion. No summaries.
- Parts 2 and 3 are academic; still explain each technical term at first use.
- Part 2 stages follow OUR analysis of the argument, not the paper's section order.
- Several papers: one walkthrough per paper in 1.3 (1.3a, 1.3b, ...) and a combination stage in part 2.
- Keep the premise tables in step with the doc comments in Argument.lean.
- The Chinese half mirrors the English half section by section. Object names, catalogue IDs,
  numbers, units, citations, code and Lean identifiers are not translated.
- Wiki links to repository files must be absolute https://github.com/sudoghut/astrolab/... URLs.
-->

---

## English

### Part 1 · The paper in plain language

#### 1.1 The question and why it matters

{{What were people trying to find out, what was known before, why this is hard.}}

#### 1.2 The data

{{Which instrument / survey measured what; explain the measurement in everyday terms, then
precisely. Real numbers with units.}}

#### 1.3 Step by step: how the authors got from data to conclusion

{{One subsection per real step of the paper's work, with the actual numbers and what each key
figure or table shows. Include a back-of-envelope version of the headline number.}}

#### 1.4 What they conclude, and how sure they are

{{Each claim, its strength, the authors' own caveats, and what would have to be true for the
authors to be wrong.}}

### Part 2 · The logic of the argument

#### 2.0 Map of the argument

{{The conclusion(s) and the stages they rest on, e.g. a numbered chain or a small diagram:
A. the signal is real → B. … → C. … ⇒ conclusion.}}

How we check it: the argument is written in Lean 4
([`studies/{{NNN-slug}}/argument/Argument.lean`](https://github.com/sudoghut/astrolab/blob/main/studies/{{NNN-slug}}/argument/Argument.lean)).
Each premise is one constructor of `Field` (no axioms), labelled with its kind and its
provenance:

| Tag | Kind of premise |
|---|---|
| `OBS` | observation or measurement (with table / figure) |
| `MOD` | modelling assumption |
| `STAT` | statistical inference (significance, model comparison) |
| `NUM` | numerical result, re-computed by this repo's `run.py` |
| `LIT` | result taken from other literature |
| `GAP` | premise the inference needs that neither the paper nor standard knowledge supplies |

Provenance: `[stated: "quote"]` (the paper says it, quoted; with several papers
`[stated <arXiv id>: "quote"]`), `[implied]` (standard knowledge the
paper relies on without writing it out, with a source), `[reconstructed]` (our addition; exactly
the `GAP` premises).

What Lean checks: that the conclusion follows from these premises (`final`) and is not trivially
true (`final_nontrivial`); that the premises can hold together (`consistent`); that no single
premise gives the conclusion alone (`alone_insufficient`); for each premise, whether it is needed
(a countermodel without it) or redundant; and whether the premises the paper actually states are
enough (`stated_*`), and whether they are enough once standard knowledge is added (`explicit_*`;
`explicit_insufficient` means a real gap). What Lean does not check: the physics inside
each premise — that is what parts 1 and 3 and the study are for.

#### 2.1 Stage A · {{name}}

**Overview.** {{What this stage establishes and why the rest needs it.}}

**Premises.**

| Premise (Lean constructor) | Tag | Provenance | Source in paper |
|---|---|---|---|
| {{`obs_rv`: …}} | {{OBS}} | {{stated: "…"}} | {{§2, Table 1}} |

**Rival explanations.**

| Alternative | Excluded by premise | Excluded explicitly by the paper? |
|---|---|---|
| {{…}} | {{`gap_…`}} | {{yes, §4 / no}} |

**Inference (Lean excerpt).**

```lean
{{theorem final : ∀ v, Premises v → Conclusion v := by
  intro v p
  have h1 := p .mod_… (p .obs_…)   -- §3.1
  exact …}}
```

**Critique.** {{Is each step valid? Hidden assumptions (GAP premises)? How strong is it?}}

#### 2.2 Stage B · {{name}}

{{Same structure.}}

#### 2.N What the Lean check found

{{1. Headline: `explicit_sufficient` or `explicit_insufficient` and the GAP premises that close
the difference; `stated_*` and the `[implied]` background the paper relies on.
2. Ranked list of problems: each GAP (why it matters, weaker versions considered), rival
explanations the paper leaves open, conclusions stronger than the premises.
3. Redundant premises (`…_redundant`): what they say about the paper or about our encoding (a
premise whose atoms appear nowhere else is redundant by construction).
4. Consistency (`consistent`) and whether it is a strong check here (it only bites when some
premises are negative or exclusive).
5. Limits: Lean checks the logical structure under our encoding, not the physics in each premise;
with uninterpreted atoms "needed" means "used by this encoding".}}

### Part 3 · What astrolab can test or explore

{{Retrofitted article only: "Written after implementation (post hoc); not a pre-registration."}}

| Stage / claim | Can we test or explore it? | How | Data (size) | Decision criterion | Result |
|---|---|---|---|---|---|
| {{A}} | {{testable now / after … / explorable (not decisive) / out of scope}} | {{…}} | {{…, ~N MB}} | {{confirms if …; challenges if … (explorable rows: "none - exploration only, see README §8")}} | {{pending / reproduced: … / differs: …}} |

{{Keep the table above as first written (it is the source of the pre-registration); fill the
Result column.
After implementation, add: what was actually tested, the numbers, what passed or failed, what is
still open; links to the results files. The study's interactive page runs locally with
`python -m astrolab serve`; add a static figure here if readers need to see it.}}

### Glossary

| Term | Meaning |
|---|---|
| {{…}} | {{…}} |

### Open questions

- {{…}}

### Changelog

Newest first.

- {{YYYY-MM-DD}}: {{first version: parts 1–3.}}

### Sources

- {{Author et al. YEAR, Journal Vol, page, arXiv:… [V]}}

---

## 中文

### 第一部分 · 科普详解

#### 1.1 问题与意义

{{…}}

#### 1.2 数据

{{…}}

#### 1.3 一步一步：作者如何从数据走到结论

{{论文工作的每一步一个小节，写出实际数值和每张关键图表说明了什么；附上主要数字的粗略估算。}}

#### 1.4 结论与把握程度

{{每个结论、其强度、作者自己的保留意见，以及作者若是错的，需要什么成立。}}

### 第二部分 · 论证逻辑

#### 2.0 论证地图

{{结论与它依赖的各个环节，例如编号链条或小图：A. 信号真实 → B. … → C. … ⇒ 结论。}}

检查方法：论证写成 Lean 4（[`studies/{{NNN-slug}}/argument/Argument.lean`](https://github.com/sudoghut/astrolab/blob/main/studies/{{NNN-slug}}/argument/Argument.lean)）。每个前提是 `Field` 的一个构造子（不用公理 axiom），标注类型与出处性质：

| 标签 | 前提类型 |
|---|---|
| `OBS` | 观测或测量（注明表格、图） |
| `MOD` | 模型假设 |
| `STAT` | 统计推断（显著性、模型比较） |
| `NUM` | 数值结果，由本仓库 `run.py` 复核 |
| `LIT` | 引自其他文献的结论 |
| `GAP` | 推理需要、但论文和标准知识都没有提供的前提 |

出处性质：`[stated: "引文"]`（论文明说，附原文；多篇论文时写 `[stated <arXiv 编号>: "引文"]`）、`[implied]`（论文依赖但没写出的标准知识，注明来源）、`[reconstructed]`（我们补上的，恰好就是 `GAP` 前提）。

Lean 检查什么：结论能否由这些前提推出（`final`）且并非恒真（`final_nontrivial`）；前提能否同时成立（`consistent`）；单个前提不能单独推出结论（`alone_insufficient`）；每个前提是必要的（去掉它时的反例模型）还是多余的；论文明说的前提是否足够（`stated_*`）；加上标准知识后是否足够（`explicit_*`，`explicit_insufficient` 即存在真正的缺口）。Lean 不检查每个前提内部的物理是否正确——那是第一、三部分和研究本身的任务。

#### 2.1 环节 A · {{名称}}

**概述。** {{…}}

**前提。**

| 前提（Lean 构造子） | 标签 | 出处性质 | 论文出处 |
|---|---|---|---|
| {{…}} | {{OBS}} | {{…}} | {{…}} |

**其他解释（rival explanations）。**

| 其他可能 | 由哪个前提排除 | 论文是否明确排除 |
|---|---|---|
| {{…}} | {{…}} | {{…}} |

**推理（Lean 摘录）。**

```lean
{{与英文部分相同的 Lean 代码}}
```

**评析。** {{…}}

#### 2.2 环节 B · {{名称}}

{{结构同上。}}

#### 2.N Lean 检查发现的问题

{{1. 结论：`explicit_sufficient` 还是 `explicit_insufficient`，以及补上差距的 GAP 前提；`stated_*` 与论文依赖的 `[implied]` 背景知识。
2. 按严重程度排列的问题：每个 GAP（为何重要、考虑过的更弱版本）、论文没有排除的其他解释、强于前提的结论。
3. 多余的前提（`…_redundant`）：说明它们反映的是论文还是我们的编码（原子命题在别处都不出现的前提必然多余）。
4. 相容性（`consistent`）及其在此处是否有分量（只有含否定或互斥前提时才有分量）。
5. 局限：Lean 检查的是在我们的编码下的逻辑结构，不检查每个前提内部的物理；原子命题不加解释时，"必要"指"本编码用到了它"。}}

### 第三部分 · 本项目可检验或探索的环节

{{仅限补写的文章："实现后补写（事后，post hoc），不是预注册。"}}

| 环节 / 结论 | 能否检验或探索 | 方法 | 数据（大小） | 判据 | 结果 |
|---|---|---|---|---|---|
| {{A}} | {{现在可检验 / 待…之后 / 可探索（不能判决） / 不在范围内}} | {{…}} | {{…，约 N MB}} | {{若…则支持；若…则质疑（可探索的行写"无——仅供探索，见 README 第 8 节"）}} | {{…}} |

{{保留最初的表格（即预注册来源），只填写"结果"一列；实现后补充实际检验了什么、数值、哪些通过、哪些失败、哪些仍待解决，并链接结果文件。研究的交互网页在本地用 `python -m astrolab serve` 打开，需要时在这里放静态图。}}

### 术语表

| 术语 | 含义 |
|---|---|
| {{…（English）}} | {{…}} |

### 开放问题

- {{…}}

### 研究进展

按时间倒序。

- {{YYYY-MM-DD}}：{{第一版：第一至三部分。}}

### 来源

- {{同英文部分}}
