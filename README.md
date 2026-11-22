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

The Atlas and every study's web page are online at [sudoghut.github.io/astrolab](https://sudoghut.github.io/astrolab/)
(published from `main` by a manually triggered workflow; locally: `python -m astrolab serve`).
Each study's page is at `https://sudoghut.github.io/astrolab/studies/<id>/web/`.

| Study | Result |
|---|---|
| [000 · smoke test](studies/000-smoke-test_gaia-dr3-10pc-census/) | Gaia DR3 10 pc census; pipeline check |
| [001 · M4 Gaia dormant black holes](studies/001-m04-gaia-dormant-black-holes/) | Gaia BH1/BH2 masses reproduced from DR3 astrometry alone; server-side screen of all 169,227 DR3 astrometric orbits (~0.5 MB downloaded); referee-reviewed; vetoes validated on 23 positive controls; ready for Gaia DR4 (2026-12-02) |
| [002 · M1 DESI BAO and evolving dark energy](studies/002-m01-desi-bao-evolving-dark-energy/) | BAO-only and no-CMB combinations reproduced; the compressed-CMB-prior result reproduced conditionally (reading B; post hoc, DESI's public chain configuration supports it, the likelihood source is not public), robust in a narrow sense to the θ* calibration and the r_d formula |
| [003 · M2 Hubble tension: SH0ES ladder and host selection](studies/003-m02-hubble-tension-distance-ladder/) | R22's printed fit reproduced (H0 73.04; the pre-registered 47-parameter target was a different fit, not reproduced); restricting the ladder to the CCHP hosts (post-data host labelling) lowers H0 by about 2 km/s/Mpc, not significant once a host-level random effect is modelled; the excess calibrator scatter is consistent with one outlying host (N5584), also with that choice simulated, but a pre-registered comparison does not distinguish it from host-level scatter spread over all hosts (R2-RE-D: diffuse models with τ = 0.077 and 0.105 mag not excluded, an underpowered null with about 50% power against a single offset host); Cepheids and TRGB agree on the same hosts; referee-reviewed |
| [004 · M7 wide binaries: Newton or MOND](studies/004-m07-wide-binaries-gravity-test/) | C26's sample rebuilt server-side (639 pairs against C26's 1,421; not the same sample); with bootstrap errors the test cannot tell Newton from MOND and has no power (referee, post hoc); with C26's stated error formula it leans to MOND; the extended sample failed its pre-registered power gate and was not run; a shifted-field exploration (post hoc) shows the relaxed degrouping loss is mostly chance neighbours |
| [005 · M9 NANOGrav 15-yr background](studies/005-m09-nanograv-gwb-power-law/) | power-law amplitude within NANOGrav's interval and spectral-index tension of the same order (descriptive) under the DMX noise model; clearly different under the DMGP noise model (post hoc) |
| [006 · M8 galaxies at z ≈ 14](studies/006-m08-z14-galaxies-number-density/) | number density reproduced; the constant-efficiency prediction lies above N26's baseline robustly, while whether the UV scatter it needs (about 1–2 mag) matches N26's depends on the calibration of the z ≈ 8 luminosity function (undetermined, prior-dominated) |
| [007 · M10 GWTC-4.0 binary black hole masses](studies/007-m10-gwtc4-bbh-mass-35msun/) | O4a event sample reproduced (84 of 84); the full sample is not reproduced as registered (O1–O3 59 of 69 by the rule; 69 with a post-hoc FAR fallback); the 35 M☉ local peak depends on the selection-function model (exploration) |
| [008 · M3 S8: DES Y6 against the CMB](studies/008-m03-s8-des-y6-cmb-parameter-difference/) | parameter difference reproduced (S8 2.67σ, S8–Ωm 2.18σ); the full 6-D difference from a normalizing flow (1.70σ) is descriptive only (training scatter above the registered limit, no verdict); it comes mostly from the Σmν direction (0.52σ without it) and from Σmν's correlations with the other DES parameters |
| [009 · M6 Milky Way outer rotation curve](studies/009-m06-mw-outer-rotation-curve-decline/) | J23's power law and mass reproduced under their assumptions; part of the 3σ comes from the prior and the errors are not independent; with correlated errors a flat curve is rejected at ≥ 2σ (high-f covariances only; about 3–5σ over the squared-exponential kernels, post-hoc reading), a Keplerian decline cannot be told apart from a shallower one, and NFW is disfavoured |
| [010 · M5 thick disc from subgiant ages](studies/010-m05-thick-disc-subgiant-ages/) | the 13 Gyr mean reproduced (12.93 Gyr); with a consistent selection term the old-disc span is reproduced (6.09 Gyr) but its scatter is not (2.55 against 0.82 Gyr), both sensitive to the choice of selection term (the original verdicts, "cannot determine", stay recorded); the intrinsic scatter is confirmed below 0.82 Gyr but not robust; the 8 Gyr split: the recorded R1-SEL label stays "undetermined"; the pre-registered rerun with improved mock fits (R1-SEL-FIT, T-049) gives "not reproduced (robust; selection-term robust)": four of five metallicity bins resolvable, none almost disjoint, under the catalogue's quoted age errors and an idealised split model (larger errors untested, T-054) |
| [011 · M11 Radcliffe Wave oscillation](studies/011-m11-radcliffe-wave-oscillation/) | mixed: K24's B = 0.84 reproduced and the standing wave excluded in the main fit, but not robustly (the preference vanishes without the Orion region or without kernel weights, and drops below the exclusion threshold without one of four source catalogues); the phase spread and the model-free b̂ are undetermined; the cluster fit is partly reproduced (3 of 6 shape parameters), the clouds-only and column-(6) fits are not, so the tests refer to our implementation; the CO velocities do not favour the travelling wave; the free-ω₀ potential test is withdrawn (likelihood degenerate in ω₀; T-056) |

See [STATUS.md](STATUS.md), the to-do list [TODO.md](TODO.md) (finished items move to [DONE.md](DONE.md)), and the design documents in [`design/`](design/) (all in Chinese).

### Background reading

- [Five Years of Astronomy (2021–2026): A Plain-Language Review](https://github.com/sudoghut/astrolab/wiki/Five-Years-of-Astronomy-2021-2026)
  (wiki, English and Chinese): what changed in astronomy over the last five years, with the
  emphasis on the results this project sets out to reproduce. Source: [`docs/wiki/`](docs/wiki/).

### Quick start

```bash
pip install numpy scipy pandas pyarrow astropy pyvo astropy-healpix emcee platformdirs pyyaml requests pytest nsstools
python -m astrolab status          # studies, claims, cache
python -m astrolab run 001         # re-run a study (cached after the first run)
python -m pytest                   # library tests + each study's conclusion tests
python -m astrolab serve           # Atlas and study pages at http://127.0.0.1:8765/atlas/web/
```

### Configuration

- **Data limits** live in `astrolab/config.py` (per download, per TAP query, per study run, cache size).
  They are deliberate guards (AGENTS.md section 1); do not raise them or set `ASTROLAB_*` overrides
  without a recorded reason.
- **Cache**: the system cache directory (`%LOCALAPPDATA%\astrolab\Cache` on Windows), never the
  project folder. `python -m astrolab cache [info|prune|clear]`.
- **Gaia archive login (optional).** Anonymous jobs on the ESA Gaia archive stop after 60 s; a free
  Gaia archive account gets much longer limits. astrolab finds credentials in this order:
  1. environment variables `GAIA_USERNAME` and `GAIA_PASSWORD`;
  2. a `.env` file at the project root: copy `.env.example` to `.env` and fill in both lines. `.env`
     is git-ignored. If the project folder is synced (e.g. Dropbox), the file is synced too; use the
     environment variables instead if that matters;
  3. otherwise `python -m astrolab gaia-login` asks interactively (password not echoed).

  The password is never stored by astrolab: only the session cookie returned by the archive is kept,
  in `%LOCALAPPDATA%\astrolab\gaia_session.json` (outside the project). With credentials configured
  and no cookie yet, Gaia queries log in once automatically. `python -m astrolab gaia-logout` ends the
  session and deletes the cookie. The cookie works like a password while the session lasts: on Windows the
  file inherits the user-only permissions of the profile folder (`chmod` has no effect there).

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

Atlas 与每个研究的网页在线发布于 [sudoghut.github.io/astrolab](https://sudoghut.github.io/astrolab/)（由手动触发的工作流从 `main` 发布；本地浏览用 `python -m astrolab serve`）。每个研究的网页在 `https://sudoghut.github.io/astrolab/studies/<id>/web/`。

| 研究 | 结果 |
|---|---|
| [000 · 冒烟测试（smoke test）](studies/000-smoke-test_gaia-dr3-10pc-census/) | Gaia DR3 中 10 pc 以内的天体普查；用于检查整条管线（pipeline） |
| [001 · M4 Gaia 休眠黑洞（dormant black holes）](studies/001-m04-gaia-dormant-black-holes/) | 只用 DR3 天体测量（astrometry）就复现了 Gaia BH1、BH2 的质量；在服务器端筛选了 DR3 全部 169,227 个天体测量轨道解，只下载约 0.5 MB；经过独立审稿；否决规则（veto）在 23 个已知正样本（positive controls）上验证无误；已为 Gaia DR4（2026-12-02 发布）准备就绪 |
| [002 · M1 DESI 重子声学振荡（Baryon Acoustic Oscillations, BAO）与演化暗能量](studies/002-m01-desi-bao-evolving-dark-energy/) | 只用 BAO 与不含宇宙微波背景（CMB, Cosmic Microwave Background）的组合已复现；压缩 CMB 先验的结果为有条件复现（解读 B；事后，DESI 公开的链配置支持这一解读，似然源码不公开），在较窄的意义上对 θ* 标定与 r_d 公式稳健 |
| [003 · M2 哈勃张力：SH0ES 距离阶梯与宿主选择](studies/003-m02-hubble-tension-distance-ladder/) | 复现 R22 印出的拟合（H0 73.04；预注册的 47 参数目标是另一个拟合，未复现）；把阶梯限于 CCHP 宿主（数据之后的宿主标注）使 H0 降低约 2 km/s/Mpc，加入宿主级随机效应（random effect）后不显著；多出的定标星（calibrator）离散与一个离群宿主（outlying host）N5584 相容，把这一选择放进模拟后也是如此，但预注册的比较不能把它与分布在所有宿主上的宿主级离散区分开（R2-RE-D：τ = 0.077 与 0.105 mag 的分散模型未被排除，对单个偏移宿主的功效只有约 50%，是功效不足的零结果）；同宿主上造父变星（Cepheids）与红巨星支顶端（TRGB, Tip of the Red Giant Branch）一致；经过独立审稿 |
| [004 · M7 宽双星：牛顿还是 MOND（Modified Newtonian Dynamics，修正牛顿动力学）](studies/004-m07-wide-binaries-gravity-test/) | 在服务器端重建 C26 的样本（639 对，C26 为 1,421 对；样本不同）；自助法（bootstrap）误差下检验无法区分牛顿与 MOND，且没有功效（审稿，事后）；用 C26 写明的误差公式时偏向 MOND；扩大样本未通过预注册的功效门槛，没有运行；平移视场（shifted field）的探索（事后）表明宽松去群（relaxed degrouping）的损失大部分来自偶然邻居（chance neighbours） |
| [005 · M9 NANOGrav 15 年引力波背景](studies/005-m09-nanograv-gwb-power-law/) | 在 DMX 噪声模型（逐段色散量，dispersion measure）下，幂律（power law）振幅在 NANOGrav 的区间内，谱指数（spectral index）张力为同一量级（描述性）；在 DMGP 噪声模型（色散量的高斯过程，Gaussian process）下差别明显（事后） |
| [006 · M8 z ≈ 14 星系](studies/006-m08-z14-galaxies-number-density/) | 数密度复现；恒定效率模型的预言稳健地高于 N26 的基准，而它所需的紫外弥散（UV scatter，约 1–2 mag）是否与 N26 相符，取决于 z ≈ 8 光度函数（luminosity function）的校准（无法判定，由先验主导） |
| [007 · M10 GWTC-4.0 双黑洞质量](studies/007-m10-gwtc4-bbh-mass-35msun/) | O4a 事件样本复现（84/84）；完整样本按注册的规则未复现（O1–O3 按规则 59/69；事后用误报率（FAR, false alarm rate）替代规则为 69）；35 M☉ 局部峰依赖选择函数（selection function）模型（探索） |
| [008 · M3 S8：DES Y6 与 CMB](studies/008-m03-s8-des-y6-cmb-parameter-difference/) | 参数差异复现（S8 2.67σ，S8–Ωm 2.18σ）；归一化流（normalizing flow）给出的完整 6 维差异（1.70σ）只作描述（训练离散超过预注册上限，没有判定）；它主要来自 Σmν 方向（不含 Σmν 时 0.52σ）以及 Σmν 与其他 DES 参数的相关 |
| [009 · M6 银河系外区旋转曲线](studies/009-m06-mw-outer-rotation-curve-decline/) | 在 J23 的假设下复现其幂律与质量；3σ 部分来自先验，误差也不独立；在相关误差下平坦曲线在 ≥ 2σ 被拒绝（只在高 f 协方差下；在平方指数核下约 3–5σ，事后解读），开普勒式下降与较缓的下降无法区分，NFW（Navarro–Frenk–White）晕不被看好 |
| [010 · M5 由亚巨星年龄看厚盘](studies/010-m05-thick-disc-subgiant-ages/) | 复现 13 Gyr 均值（12.93 Gyr）；用一致的选择项（selection term）后，老盘序列的跨度复现（6.09 Gyr），其弥散未复现（2.55 Gyr，论文 0.82 Gyr），两者都对选择项的取法敏感（原判定"无法确定"保留）；内禀离散（intrinsic scatter）确认低于 0.82 Gyr，但不稳健；8 Gyr 分界：记录的 R1-SEL 标签"无法判定"保留；改进模拟拟合的预注册重跑（R1-SEL-FIT，T-049）给出"未复现（稳健；选择项稳健）"：五个金属丰度箱中四个可分辨，没有一个近乎分离，前提是星表给出的年龄误差与理想化的分界模型（更大的误差未检验，T-054） |
| [011 · M11 Radcliffe 波的振荡](studies/011-m11-radcliffe-wave-oscillation/) | 混合（mixed）：复现 K24 的 B = 0.84，主拟合排除了驻波，但不稳健（去掉猎户座区域或去掉核权重，偏好就消失；去掉四个来源星表中的任何一个，则降到排除阈值以下）；相位离散与不依赖模型的 b̂ 无法判定；星团拟合部分复现（6 个形状参数中 3 个），只用云的拟合与第 (6) 列未复现，所以各检验针对我们的实现；CO 速度不偏好行波；ω₀ 自由的引力势检验撤回（似然对 ω₀ 退化（degenerate）；T-056） |

详见 [STATUS.md](STATUS.md)、待办清单（to-do list）[TODO.md](TODO.md)（完成的条目移入 [DONE.md](DONE.md)），以及 [`design/`](design/) 中的设计文献。

### 背景阅读

- [近五年天文学（2021–2026）：科普综述](https://github.com/sudoghut/astrolab/wiki/Five-Years-of-Astronomy-2021-2026#中文)
  （Wiki，中英双语）：用浅显的语言介绍近五年天文学的主要进展，重点是本项目计划复现的成果。源文件：[`docs/wiki/`](docs/wiki/)。

### 快速开始

```bash
pip install numpy scipy pandas pyarrow astropy pyvo astropy-healpix emcee platformdirs pyyaml requests pytest nsstools
python -m astrolab status          # 查看研究、结论和缓存
python -m astrolab run 001         # 重跑某个研究（第一次运行后即命中缓存）
python -m pytest                   # 运行核心库测试和各研究的结论测试
python -m astrolab serve           # 本地浏览 Atlas 与研究网页：http://127.0.0.1:8765/atlas/web/
```

### 配置

- **数据上限**写在 `astrolab/config.py` 中（单次下载、单次 TAP 查询、单次研究运行、缓存总量）。它们是有意设置的保护（AGENTS.md 第一条）；没有记录理由时不要调高，也不要用 `ASTROLAB_*` 环境变量绕过。
- **缓存**放在系统缓存目录（Windows 上为 `%LOCALAPPDATA%\astrolab\Cache`），从不放在项目目录。命令：`python -m astrolab cache [info|prune|clear]`。
- **Gaia 档案登录（可选）。** ESA Gaia 档案对匿名作业限制执行 60 秒；免费注册的 Gaia 档案账号限制宽得多。astrolab 按以下顺序寻找凭据：
  1. 环境变量 `GAIA_USERNAME` 与 `GAIA_PASSWORD`；
  2. 项目根目录下的 `.env` 文件：把 `.env.example` 复制为 `.env` 并填写两行。`.env` 不受 git 追踪；若项目目录被同步（例如 Dropbox），这个文件也会被同步，介意时请改用环境变量；
  3. 都没有时，`python -m astrolab gaia-login` 以交互方式询问（密码不回显）。

  astrolab 从不保存密码，只保存档案返回的会话 cookie，位置是 `%LOCALAPPDATA%\astrolab\gaia_session.json`（项目目录之外）。配置了凭据而还没有 cookie 时，Gaia 查询会自动登录一次。`python -m astrolab gaia-logout` 结束会话并删除 cookie。会话有效期间 cookie 相当于密码：在 Windows 上，文件继承用户配置文件夹只限本人访问的权限（`chmod` 在那里不起作用）。

### 许可证

代码采用 [MIT](LICENSE) 许可证。数据产品仍遵循其原始提供方的条款（ESA Gaia、DESI、LVK、NANOGrav 等），
本仓库只保存体积很小的派生结果。
