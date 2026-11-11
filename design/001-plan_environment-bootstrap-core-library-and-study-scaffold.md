# 001 · 环境搭建：核心库与研究文件夹骨架

- 类型：工作计划（work plan）
- 状态：完成
- 日期：2026-11-11
- 依据：[000 设计原则](000-principles_agent-driven-laptop-astronomy-research.md)

## 目标

搭出最小可用的研究环境：
- agent 能读懂的操作手册
- 核心库（core library）的最小能力：取数、缓存（cache）、来源记录（provenance）、结果导出、研究调度
- 研究文件夹模板（study template）
- 总览图（Atlas）骨架

然后用一个真实的小研究做端到端（end-to-end）测试。

**不在本计划内**：
- 宇宙学计算（`cosmo`）和统计推断（`infer`, statistical inference）等能力，留给路线图里程碑（milestone）M1 按需引入。
- agent 技能（skill / slash command），留给后续计划。

## 范围与产物

```
astro/
├── CLAUDE.md              # agent 操作手册
├── STATUS.md              # 全局研究状态
├── ROADMAP.md             # 路线图（由 002 号计划产出）
├── pyproject.toml         # 依赖与 pytest 配置（不安装本包，从项目根目录运行）
├── .gitignore
├── astrolab/
│   ├── __main__.py / cli.py   # python -m astrolab <command>
│   ├── config.py          # 项目路径、系统缓存目录、容量与行数上限
│   ├── cache.py           # 内容寻址缓存（content-addressed cache），键 = 查询哈希；容量上限 + LRU 清理
│   ├── provenance.py      # 来源记录：服务、查询、数据版本、时间、哈希、行数
│   ├── fetch.py           # http() 带大小检查；tap() 带行数上限，超限拒绝
│   ├── services.py        # 已知 TAP 服务登记（Gaia、VizieR、NOIRLab Data Lab、MAST、IRSA…）
│   ├── results.py         # 结果写成 JSON（处理 numpy 类型）、紧凑摘要打印
│   ├── study.py           # 研究发现、新建（模板）、运行（调用 run.py 的 main(ctx)）
│   └── claims.py          # 结论条目（claim）加载与校验，生成 Atlas 数据
├── atlas/
│   ├── claims/            # *.yaml 结论条目
│   └── web/               # 宏观总览页 + 共享样式 base.css
├── studies/
│   ├── _template/         # 新研究模板
│   └── 000-smoke-test_gaia-dr3-10pc-census/   # 端到端冒烟研究
└── tests/
```

LRU 指最近最少使用（Least Recently Used）的清理策略。TAP 指表访问协议（Table Access Protocol）。

## 关键设计决定

1. **不用 `pip install` 安装本项目**：从项目根目录用 `python -m astrolab` 运行；pytest 通过 `pythonpath = ["."]` 找到包。这样可以避免往 anaconda 写入指向 Dropbox 的链接。
2. **命令行用 `argparse`**，不引入额外依赖；输出控制在几十行以内。
3. **取数守卫（fetch guard）**：
   - 每次 TAP 查询有行数上限，默认 50,000 行，可以显式放宽，但不能超过硬上限。
   - 结果超限直接报错（`TooLarge`），并提示改用服务器端聚合（server-side aggregation）或收窄条件。超限结果绝不静默截断。
   - HTTP 下载先读 `Content-Length`，超过 50 MB 默认上限即拒绝。
4. **缓存**：
   - 位置：`platformdirs.user_cache_dir("astrolab")`；可用 `ASTROLAB_CACHE_DIR` 环境变量覆盖。
   - 格式：表格存 Parquet，元数据存 JSON。
   - 容量：总上限默认 2 GB，超出时按 LRU 清理。
5. **网页**：
   - 浏览器禁止从 `file://` 读取本地 JSON，因此提供 `python -m astrolab serve`，即一个以项目为根目录的本地 HTTP 服务器。
   - 页面通过相对路径读取 `../results/*.json`。
   - 可视化库按页面需要从 CDN（内容分发网络，Content Delivery Network）引入，并固定版本号。
6. **研究文件夹命名**：`NNN-<slug>`，与设计文献同样的编号思路。
7. **新增依赖**：
   - `pyvo`：TAP 客户端。
   - `astropy-healpix`：HEALPix 计算。`healpy` 在 Windows 上没有官方 wheel 安装包，所以不用它。
   - `emcee`：MCMC 采样器，为 M1 预备。
8. **测试收集**：pytest 同时收集 `tests/` 和各研究文件夹中的 `test_*.py`。使用 `--import-mode=importlib`，避免各研究中的同名测试文件冲突。

## 步骤

1. 安装依赖。
2. 写 `pyproject.toml`、`.gitignore`、`CLAUDE.md`、`STATUS.md`。
3. 写核心库各模块。
4. 写研究模板与 Atlas 骨架（含示例结论条目）。
5. 写冒烟研究（smoke test）：Gaia DR3 中视差（parallax）大于 100 mas、即 10 pc 以内的天体普查（census），以及服务器端聚合的全天亮星密度图。
6. 写测试：缓存、来源记录、结果导出、结论校验、研究发现，全部离线可跑。
7. 运行测试与冒烟研究，确认网页可用。

## 验收标准

- `python -m pytest` 全部通过。
- `python -m astrolab run 000` 成功，第二次运行命中缓存、不再联网。
- `results/` 中有结果 JSON 和来源记录。
- `python -m astrolab serve` 之后，能在浏览器中打开研究网页与 Atlas 页面。
- `python -m astrolab status` 输出简洁的全局状态。

## 执行记录

### 2026-11-11

- 计划写成，开始执行。
- 安装 pyvo 1.10.0、astropy-healpix 2.0.1、emcee 3.1.6。
- 核心库、模板、Atlas、冒烟研究、测试全部写成。
- **第一次运行冒烟研究**：两次 Gaia 查询均成功。`parallax > 100` 返回 315 行；服务器端把约 125 万颗 G < 11 的亮星聚合成 768 个像素，只返回这 768 行。
  - 问题：Gaia 返回的 HEALPix 索引是 int32，而 `astropy_healpix` 要求 int64。
  - 修复：在 `run.py` 中转换类型。
- **第二次运行**：0.12 秒，完全命中缓存。
  - 质量切割（quality cut）后剩 238 个天体。
  - 最近的天体依次是比邻星（Proxima Centauri）1.302 pc、巴纳德星（Barnard's Star）1.828 pc，与已知值一致。
- **资源占用**：缓存 0.05 MB，位于 `%LOCALAPPDATA%\astrolab\Cache`；结果文件共 60 kB。
- **测试**：13 项全部通过（10 项核心库测试 + 3 项冒烟研究结论测试）。
- 环境中的 `pytest_freezegun` 插件会产生弃用警告（deprecation warning），已在 pytest 配置中用 `-p no:freezegun` 禁用。
- 用户追加约定：设计文献与研究日志中的术语必须括注英文原文。已写入 000 号原则第 4 节，并按此改写了现有设计文献。
