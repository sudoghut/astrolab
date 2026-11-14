# 011 · 工作计划：Atlas 的天空视图与尺度视图（研究以足迹出现在图上）

状态：进行中
创建：2026-11-14
待办：T-005（`TODO.md`）

## 1. 目标

设计原则（000 号文献第 2–3 节）把 Atlas 定为宏观的"世界地图"：每个结论（claim）与研究（study）在图上有一个位置。现在的 Atlas 只是按尺度分层（L0–L4、X）列出卡片。本计划增加两种视图：

- **尺度视图（scale view）**：一条对数距离轴（以秒差距 pc 为单位，从约 10⁻⁶ pc（约 0.2 天文单位）到约 10¹⁰ pc（可观测宇宙））。每个研究按其足迹（footprint）中的距离范围画成一段，结论跟随其研究；没有研究的结论放在所属层级的默认范围内。
- **天空视图（sky view）**：全天的莫尔韦德投影（Mollweide projection），用银道坐标（Galactic coordinates）。研究的足迹按模式显示：全天（all-sky）、巡天区域（survey，只作图例说明，不画边界）、目标天体（targets，画成点）。

研究以足迹形式出现在图上。卡片列表保留为第三种视图（默认视图不变）。

## 2. 足迹的数据模式（`study.yaml` 的 `footprint` 字段）

```yaml
footprint:
  scale: {min_pc: 100, max_pc: 3000, note: "..."}    # 距离范围（pc），min_pc < max_pc，均为正数
  sky:
    mode: all-sky | survey | targets | none          # 可组合，如 "all-sky + targets"、"survey + targets"
    survey: {name: "DESI DR2", note: "..."}           # mode 含 survey 时必填 name
    targets:                                          # mode 含 targets 时必填
      - {name: "Gaia BH1", ra: 262.17, dec: -0.58}    # 度（ICRS）；缺坐标时从 results/targets.json 按 name 取
  data: [...]                                         # 用到的数据表或文件（只作说明）
```

- 现有研究 001 的 `mode: all-sky-screen + targets` 改写为 `all-sky + targets`（含义不变：全天筛选加三个目标）。
- 坐标解析：`astrolab/claims.py` 的 `atlas_data()` 读取足迹；目标缺 ra/dec 时，从该研究 `results/targets.json`（列表，元素含 `name`、`ra`、`dec`）按名字补上；仍缺则记为未解析，页面显示在图例中而不画点。银道坐标由 astropy 在生成时换算，网页不做坐标变换。
- 校验：新增 `footprint_errors(meta)`，`python -m astrolab claims check` 与测试调用它；足迹可以缺省（研究在尺度视图中退回到层级默认范围，天空视图中不出现）。
- 层级默认范围（pc，宽松的数量级，只用于没有足迹的条目）：L0 10⁸–10¹⁰·¹⁵，L1 10⁷–10¹⁰，L2 10⁴–10⁸·⁵，L3 1–10⁵，L4 10⁻⁶–10⁴，X 全轴。

## 3. 网页设计要点

- 不引入外部库：尺度视图与天空视图都用页面内的 SVG 绘制（莫尔韦德投影用牛顿迭代解辅助角，几十行代码），保持 Atlas 轻量。
- 双语：所有文字用 `i18n.L` / `i18n.t`，切换语言时重绘。
- 点击条目跳到对应研究页面；悬停显示标题与距离范围。
- 视图切换按钮（列表 / 尺度 / 天空），默认列表；所选视图记在 `localStorage`（读写包在 try/catch 中）。

## 4. 环节（每个环节过双闸审查）

1. **数据模型**：本计划；足迹模式、`atlas_data()` 的足迹与坐标解析、`footprint_errors` 校验、研究 000/001/002 与模板的足迹字段、不联网测试；重新生成 `atlas/web/data/atlas.json`。
2. **网页视图**：`atlas/web/index.html` 的尺度视图与天空视图；用无头浏览器检查渲染。

## 5. 执行记录

- 2026-11-14：建分支 `feat/atlas-sky-scale-views`；登记 T-005 进行中。
- 2026-11-14 · 环节 1：`astrolab/claims.py` 新增足迹模式校验 `footprint_errors`、解析 `resolve_footprint`（层级默认范围、从 results/targets.json 补坐标、用 astropy 换算银道坐标）；`atlas_data()` 输出每个研究的足迹与各层级默认范围；`claims check` 同时检查足迹；研究 000、001、002 与模板加上足迹（001 的模式改写为 all-sky + targets，含义不变）；新增不联网测试 `tests/test_atlas_footprint.py`；重新生成 `atlas.json`。
