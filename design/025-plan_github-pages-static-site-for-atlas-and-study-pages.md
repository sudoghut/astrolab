# 025 · 工作计划：把 Atlas 与各研究网页作为 GitHub Pages 静态网站发布

状态：执行中
创建：2026-11-16
待办：T-037（`TODO.md`）

## 1. 目标

用户提出（2026-11-16）：考虑把本项目作为 GitHub Pages 直接部署，使 Atlas 与各研究网页可以在线打开，而不必在本机运行 `python -m astrolab serve`。

## 2. 调查结果

- 所有网页都用相对路径：研究网页读取 `../results/*.json`（研究 009 还读 `../data/`），引用 `../../../atlas/web/` 中共享的 `i18n.js` 与 `base.css`；Atlas 读取 `data/atlas.json`，并以相对路径链接到 `../../studies/<id>/web/`。Plotly 来自 CDN。所以只要发布的网站保持与仓库相同的目录结构，网页无需修改。
- 需要发布的只有：`atlas/web/`，以及每个研究的 `web/`、`results/`（顶层）与 `data/`（入库的小表格），共 113 个文件、约 3.1 MB。不发布代码、日志、README、缓存或任何数据文件。
- 仓库是公开的；GitHub Pages 尚未启用（API 返回 404）。

## 3. 设计

- `astrolab/site.py`：`build(dest)` 按上面的范围复制文件（只限网页与小结果文件的类型，单个文件超过 5 MB 跳过并报告），加根目录的 `index.html`（跳转到 `atlas/web/`）与 `.nojekyll`；`broken_links(site)` 离线检查所有静态的相对链接（`src`、`href` 与字面的 `fetch()` 目标）都在网站之内且存在。命令：`python -m astrolab site <dest>`。
- 测试 `tests/test_site.py`：在临时目录中建网站，检查没有断链、没有 `.py` 或 `.md` 文件、大小远低于上限。
- `.github/workflows/pages.yml`：**只能手动触发**（`workflow_dispatch`），从入库的文件建网站并部署到 Pages；不取任何数据。
- **发布是对外公开的动作**：启用 Pages（Settings → Pages → Source: GitHub Actions）并第一次运行工作流，须由用户决定，本计划不代为执行。合并本 PR 本身不发布任何内容。

## 4. 环节与审查

1. 网站构建、测试、工作流与本计划——双闸审查。
2. 合并后由用户决定是否启用 Pages 并运行工作流；若启用，再考虑是否改为每次推送到 `main` 时自动部署。

## 5. 验收标准（acceptance criteria）

- `python -m astrolab site <dest>` 建出的网站没有断链；`python -m pytest` 通过；
- 工作流只能手动触发，不在合并时发布；
- AGENTS.md 第三条的命令列表加上 `site`。

## 6. 执行记录

- 2026-11-16：调查网页路径与发布范围；写 `astrolab/site.py`、测试与工作流；本地构建 113 个文件、3.10 MB、无断链。
