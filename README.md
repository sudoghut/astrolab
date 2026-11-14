# astrolab

[English](#english) · [中文](#中文)

---

## English

**Agent-driven astronomy research on a personal laptop.**

An open experiment: can a coding agent plus one laptop (MB-scale data, minute-scale
compute) do and advance real astronomical research using public survey data
(Gaia, SDSS, DESI, LIGO/Virgo/KAGRA, pulsar timing arrays, ...)?

### How it works

- **Coarse map first, detail on demand.** The [Atlas](atlas/) is a coarse, scale-ordered map of
  the universe (cosmology → large-scale structure → local universe → Milky Way → stars, plus
  cross-cutting time-domain/GW). Each landmark result is a graded *claim*
  (`established` / `tension` / `hint` / `contested` / `refuted`).
- **One folder per question.** Each study in [`studies/`](studies/) has a pre-registered
  README (question, hypothesis, decision criteria written *before* the code), a re-runnable
  `run.py`, small JSON results with full provenance, tests asserting its conclusions, and a web
  page designed freely for that question (the Atlas is only the overview map).
- **Laptop-scale by construction.** Heavy lifting happens on public servers via ADQL/TAP
  (filtering, aggregation, derived quantities computed server-side). The core library refuses
  oversized downloads, caches in the system cache directory, and records where every number came from.
- **Roadmap = landmark results.** The environment grows by reproducing important, verifiable
  2022–2026 results ([ROADMAP.md](ROADMAP.md)); each reproduction adds library capability and
  leaves open questions for new research.
- **Agents first.** [AGENTS.md](AGENTS.md) is the operating manual for coding agents (data-download
  limits come first). Reusable research workflows live in [`.claude/skills/`](.claude/skills/),
  e.g. independent referee review. No notebooks.

### Status

| Study | Result |
|---|---|
| [000 · smoke test](studies/000-smoke-test_gaia-dr3-10pc-census/) | Gaia DR3 10 pc census; pipeline check |
| [001 · M4 Gaia dormant black holes](studies/001-m04-gaia-dormant-black-holes/) | Gaia BH1/BH2 masses reproduced from DR3 astrometry alone; server-side screen of all 169,227 DR3 astrometric orbits (~0.5 MB downloaded); referee-reviewed; vetoes validated on 23 positive controls; ready for Gaia DR4 (2026-12-02) |

See [STATUS.md](STATUS.md) and the design documents in [`design/`](design/) (in Chinese).

### Background reading

- [Five Years of Astronomy (2021–2026): A Plain-Language Review](https://github.com/sudoghut/astrolab/wiki/Five-Years-of-Astronomy-2021-2026)
  (wiki, English and Chinese): what changed in astronomy over the last five years, with the
  emphasis on the results this project reproduces. Source: [`docs/wiki/`](docs/wiki/).

### Quick start

```bash
pip install numpy scipy pandas pyarrow astropy pyvo astropy-healpix emcee platformdirs pyyaml requests pytest nsstools
python -m astrolab status          # studies, claims, cache
python -m astrolab run 001         # re-run a study (cached after the first run)
python -m pytest                   # library tests + each study's conclusion tests
python -m astrolab serve           # Atlas and study pages at http://127.0.0.1:8765/atlas/web/
```

### License

[MIT](LICENSE). Data products remain under the terms of their original providers
(ESA Gaia, DESI, LVK, NANOGrav, ...); this repository stores only small derived results.

---

## 中文

**在个人电脑上、由编程智能体（coding agent）驱动的天文学研究。**

这是一个开放的实验：只依靠编程智能体和一台个人电脑（本地数据为 MB 级，单次运算以分钟计），
能否基于公开巡天数据（Gaia、SDSS、DESI、LIGO/Virgo/KAGRA、脉冲星计时阵 Pulsar Timing Arrays 等）
进行并推动真正的天文学研究？

### 工作方式

- **先有粗粒度的总图，细节按需补充。** [总览图（Atlas）](atlas/)按尺度排列整个宇宙：
  宇宙学、大尺度结构（large-scale structure）、近邻宇宙、银河系、恒星，另加时域与引力波（gravitational waves）等横向主题。
  每个代表性结果都是一个带等级的结论（claim），等级分为：已坐实（established）、张力（tension）、
  迹象（hint）、有争议（contested）、被否定（refuted）。
- **每个问题一个文件夹。** [`studies/`](studies/) 下的每个研究都包含以下内容：
  - 预注册（pre-registration）的 README：问题、假设和判据都在写代码**之前**定好；
  - 可以重跑的 `run.py`；
  - 带完整来源记录（provenance）的小体积 JSON 结果；
  - 断言结论仍然成立的测试；
  - 为该问题自由设计的网页。Atlas 只是总图，研究网页不必拘泥于它的形式。
- **从设计上就控制在个人电脑的规模。** 繁重的计算交给公开服务器，通过 ADQL/TAP 在服务器端完成筛选、
  聚合和派生量计算。核心库会拒绝超限下载，缓存（cache）放在系统缓存目录，并记录每个数字的来源。
- **路线图（roadmap）由代表性结果构成。** 环境的成长方式是复现 2022–2026 年重要且可验证的结果（见 [ROADMAP.md](ROADMAP.md)）。
  每完成一次复现，核心库就增加相应能力，同时留下可供新研究的开放问题（open questions）。
- **以智能体为先。** [AGENTS.md](AGENTS.md) 是写给编程智能体的操作手册，第一条就是数据下载约束。
  可复用的研究流程放在 [`.claude/skills/`](.claude/skills/)，例如独立审稿（referee review）。本项目不使用 notebook。

### 进展

| 研究 | 结果 |
|---|---|
| [000 · 冒烟测试（smoke test）](studies/000-smoke-test_gaia-dr3-10pc-census/) | Gaia DR3 中 10 pc 以内的天体普查；用于检查整条管线（pipeline） |
| [001 · M4 Gaia 休眠黑洞（dormant black holes）](studies/001-m04-gaia-dormant-black-holes/) | 只用 DR3 天体测量（astrometry）就复现了 Gaia BH1、BH2 的质量；在服务器端筛选了 DR3 全部 169,227 个天体测量轨道解，只下载约 0.5 MB；经过独立审稿；否决规则（veto）在 23 个已知正样本（positive controls）上验证无误；已为 Gaia DR4（2026-12-02 发布）准备就绪 |

详见 [STATUS.md](STATUS.md)，以及 [`design/`](design/) 中的设计文献。

### 背景阅读

- [近五年天文学（2021–2026）：科普综述](https://github.com/sudoghut/astrolab/wiki/Five-Years-of-Astronomy-2021-2026#中文)
  （Wiki，中英双语）：用浅显的语言介绍近五年天文学的主要进展，重点是本项目复现的成果。源文件：[`docs/wiki/`](docs/wiki/)。

### 快速开始

```bash
pip install numpy scipy pandas pyarrow astropy pyvo astropy-healpix emcee platformdirs pyyaml requests pytest nsstools
python -m astrolab status          # 查看研究、结论和缓存
python -m astrolab run 001         # 重跑某个研究（第一次运行后即命中缓存）
python -m pytest                   # 运行核心库测试和各研究的结论测试
python -m astrolab serve           # 本地浏览 Atlas 与研究网页：http://127.0.0.1:8765/atlas/web/
```

### 许可证

代码采用 [MIT](LICENSE) 许可证。数据产品仍遵循其原始提供方的条款（ESA Gaia、DESI、LVK、NANOGrav 等），
本仓库只保存体积很小的派生结果。
