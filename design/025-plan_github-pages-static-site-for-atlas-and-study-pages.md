# 025 · 工作计划：把 Atlas 与各研究网页作为 GitHub Pages 静态网站（static site）发布

状态：完成（2026-11-16；启用 Pages 待用户决定）
创建：2026-11-16
待办：T-037（`TODO.md`）

## 1. 目标

用户提出（2026-11-16）：考虑把本项目作为 GitHub Pages 直接部署，使 Atlas 与各研究网页可以在线打开，而不必在本机运行 `python -m astrolab serve`。

## 2. 调查结果

- 所有网页都用相对路径：研究网页读取 `../results/*.json`（研究 009 还读 `../data/`），引用 `../../../atlas/web/` 中共享的 `i18n.js` 与 `base.css`；Atlas 读取 `data/atlas.json`，并以相对路径链接到 `../../studies/<id>/web/`。Plotly 来自 CDN。所以只要发布的网站保持与仓库相同的目录结构，网页无需修改。
- 需要发布的只有：`atlas/web/`，以及每个研究的 `web/`、`results/`（含子文件夹，例如研究 001 的网页在 DR4 发布后读取的 `results/dr3/`）与 `data/`（入库的小表格），按文件夹限定文件类型（`results/` 只发布 `.json`，`data/` 只发布 `.csv` 与 `.json`），2026-11-16 共 113 个文件、约 3.1 MB。不发布代码、日志、README、缓存或任何下载的原始数据；`data/` 中入库的小表格（论文表格的转录）会发布。
- 仓库是公开的；GitHub Pages 尚未启用（API 返回 404）。

## 3. 设计

- `astrolab/site.py`：`build(dest)` 按上面的范围复制文件（类型不在允许清单内或单个文件超过 5 MB 的跳过并报告；不跟随符号链接；目标文件夹不能在项目目录之内），加根目录的 `index.html`（跳转（redirect）到 `atlas/web/`）与 `.nojekyll`；`broken_links(site)` 离线检查网页中字面写出的相对链接（`src`、`href` 与 `fetch()` 的目标，去掉查询串与片段）都在网站之内且存在。运行时拼出的地址（如 `../results/${n}.json`）不在检查之内，所以 `results/` 与 `data/` 整个发布。命令：`python -m astrolab site <dest>`。
- 测试 `tests/test_site.py`：在临时目录中建网站，检查没有断链、没有 `.py` 或 `.md` 文件、大小远低于上限。
- `.github/workflows/pages.yml`（GitHub Actions 工作流，workflow）：**只能手动触发**（`workflow_dispatch`），只在 `main` 分支上运行；从入库的文件建网站，有文件被跳过或有断链（broken link）即失败，再部署到 Pages；部署权限只给部署一步；不取任何数据。
- **发布是对外公开的动作**：启用 Pages（Settings → Pages → Source: GitHub Actions）并第一次运行工作流，须由用户决定，本计划不代为执行。合并本 PR 本身不发布任何内容。

## 4. 环节与审查

1. 网站构建、测试、工作流与本计划——双闸审查。
2. 合并后由用户决定是否启用 Pages 并运行工作流；若启用，再考虑是否改为每次推送到 `main` 时自动部署。

## 5. 验收标准（acceptance criteria）

- `python -m astrolab site <dest>` 建出的网站中，字面写出的相对链接都能解析，没有文件被跳过；`python -m pytest` 通过；
- 工作流只能手动触发，不在合并时发布；
- AGENTS.md 第三条的命令列表加上 `site`。

## 6. 执行记录

- 2026-11-16：调查网页路径与发布范围；写 `astrolab/site.py`、测试与工作流；本地构建 113 个文件、3.10 MB、无断链。
- 2026-11-16：闸门 1：严重 1 条——只发布 `results/` 顶层会漏掉研究 001 在 DR4 发布日提交的 `results/dr3/`，网页会悄悄失去 DR3 视图；改为连同子文件夹发布并按文件夹限定类型。次要采纳：链接检查的覆盖范围如实写明并去掉查询串，CI 遇到被跳过的文件即失败，目标文件夹不能在项目目录内，不跟随符号链接，部署权限只给部署一步，只在 `main` 上运行，不中途取消部署，术语括注英文。
- 2026-11-16：闸门 2（Codex）三轮：第 1 轮无严重问题（次要：测试检查无跳过文件、扫描本机路径与凭据样式的字符串）；第 2 轮严重 1 条——扫描漏掉 `.css`、`.svg`、`.png`，改为扫描每个发布的文件；第 3 轮无严重、无次要问题。计划完成；是否启用 Pages 并运行工作流由用户决定。
