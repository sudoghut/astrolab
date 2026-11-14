# 011 · 工作计划：Atlas 的天空视图与尺度视图（研究以足迹出现在图上）

状态：完成
创建：2026-11-14
待办：T-005（`TODO.md`）

## 1. 目标

设计原则（000 号文献第 2–3 节）把 Atlas 定为宏观的"世界地图"：每个结论（claim）与研究（study）在图上有一个位置。现在的 Atlas 只是按尺度分层（L0–L4、X）列出卡片。本计划增加两种视图：

- **尺度视图（scale view）**：一条对数距离轴，横轴是**研究对象到观测者的距离**（宇宙学研究用共动距离（comoving distance）），不是系统本身的大小；以秒差距（parsec, pc）为单位，从约 10⁻⁶ pc（约 0.2 天文单位（astronomical unit, AU））到约 10¹⁰·¹⁵ pc（约 1.4×10¹⁰ pc，可观测宇宙（observable universe）的共动半径，也是到 CMB 的距离）。每个研究按其足迹（footprint）中的距离范围画成一段，结论跟随其研究；没有研究的结论放在所属层级的默认范围内。
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
      - {name: "Gaia BH1", ra: 262.17, dec: -0.58}    # 度（国际天球参考系（International Celestial Reference System, ICRS））；缺坐标时从 results/targets.json 按 name 取
  data: [...]                                         # 用到的数据表或文件（只作说明）
```

- 现有研究 001 的 `mode: all-sky-screen + targets` 改写为 `all-sky + targets`（含义不变：全天筛选加三个目标）。
- 坐标解析：`astrolab/claims.py` 的 `atlas_data()` 读取足迹；目标缺 ra/dec 时，从该研究 `results/targets.json`（列表，元素含 `name`、`ra`、`dec`）按名字补上；仍缺则记为未解析，页面显示在图例中而不画点。银道坐标由 astropy 在生成时换算，网页不做坐标变换。
- 校验：新增 `footprint_errors(meta)`（数值须有限；坐标须在 0 ≤ ra < 360、−90 ≤ dec ≤ 90 度；`none` 不能与其他模式组合；模式不含 targets 时不得给出目标），`python -m astrolab claims check` 与测试调用它；足迹可以缺省（研究在尺度视图中退回到层级默认范围，天空视图中不出现）；足迹不合格时 `atlas_data()` 同样退回到默认值，不会中断生成。
- 层级默认范围（pc，宽松的数量级，只用于没有足迹的条目）：L0 10⁸–10¹⁰·¹⁵，L1 10⁷–10¹⁰，L2 10⁴–10⁸·⁵，L3 1–10⁵，L4 10⁻⁶–10⁴，X 全轴。

## 3. 网页设计要点

- 不引入外部库：尺度视图与天空视图都用页面内的可缩放矢量图形（SVG, Scalable Vector Graphics）绘制（莫尔韦德投影用牛顿迭代（Newton's method）解辅助角（auxiliary angle），几十行代码），保持 Atlas 轻量。
- 双语：所有文字用 `i18n.L` / `i18n.t`，切换语言时重绘。
- 点击条目跳到对应研究页面；悬停显示标题与距离范围。
- 视图切换按钮（列表 / 尺度 / 天空），默认列表；所选视图记在 `localStorage`（读写包在 try/catch 中）。

## 4. 环节（每个环节过双闸审查（dual-gate review））

1. **数据模型**：本计划；足迹模式、`atlas_data()` 的足迹与坐标解析、`footprint_errors` 校验、研究 000/001/002 与模板的足迹字段、不联网测试；重新生成 `atlas/web/data/atlas.json`。
2. **网页视图**：`atlas/web/index.html` 的尺度视图与天空视图；用无头浏览器（headless browser）检查渲染。

## 5. 执行记录

- 2026-11-14：建分支 `feat/atlas-sky-scale-views`；登记 T-005 进行中。
- 2026-11-14 · 环节 1：`astrolab/claims.py` 新增足迹模式校验 `footprint_errors`、解析 `resolve_footprint`（层级默认范围、从 results/targets.json 补坐标、用 astropy 换算银道坐标）；`atlas_data()` 输出每个研究的足迹与各层级默认范围；`claims check` 同时检查足迹；研究 000、001、002 与模板加上足迹（001 的模式改写为 all-sky + targets，含义不变）；新增不联网测试 `tests/test_atlas_footprint.py`；重新生成 `atlas.json`。
- 2026-11-14 · 环节 1 闸门 1 第 1 轮：无严重问题。次要意见采纳：校验通过但会让 `resolve_footprint` 崩溃的输入（ra/dec 为空、越界或非数值，`targets` 不是列表，`max_pc` 为无穷）改为在校验中拒绝，且不合格的足迹在生成时退回默认值；`none` 不能与其他模式组合、模式不得重复、模式不含 targets 时不得给目标；研究 002 的距离说明写全；计划写明横轴是到观测者的距离、上限约 10¹⁰·¹⁵ pc，术语补英文；测试补上这些情形、YAML 指数写法与研究 001 的目标解析；模板注明可从 targets.json 取坐标。
- 2026-11-14 · 环节 1 闸门 2（Codex）第 1 轮：4 个严重问题，均成立并已修改：`survey` 不是映射、目标名不是文字、整数过大（`float` 溢出）、`note`/`survey` 中的非文字值（如 YAML 日期）都能通过校验却让生成崩溃或写不出合法 JSON；改为在校验中拒绝（`survey` 须为带文字 `name` 的映射，目标名须为非空文字，`note` 须为文字，溢出视为非数值），并加测试确认通过校验的足迹都能序列化。次要意见：研究 002 的范围合并了 BAO 与 CMB 距离，说明已写明；层级默认范围在视图中以虚线与"层级默认范围"标注（环节 2）。
- 2026-11-14 · 环节 1 闸门 2 第 2 轮：1 个严重问题，采纳：`survey` 的额外键（如日期、NaN）会原样输出；改为只输出校验过的 `name` 与 `note`。次要意见采纳：results/targets.json 中名字不是文字的条目跳过；研究 002 的距离说明写明是 BAO 与 CMB 合并、并不连续的范围。加测试。
- 2026-11-14 · 环节 1 闸门 2 第 3 轮：无严重问题，**环节 1 通过双闸审查**（闸门 1：1 轮，0；闸门 2：3 轮，4 → 1 → 0）。次要意见采纳：空的模式（如 "" 或 " + "）不再被默默接受。
- 2026-11-14 · 环节 2：`atlas/web/index.html` 增加视图切换（列表 / 尺度 / 天空，默认列表，所选视图存于 localStorage）。尺度视图：对数距离轴 10⁻⁶·⁵–10¹⁰·⁶ pc，研究为实心条、结论为按等级着色的空心条（取其研究的范围，否则为层级默认范围，虚线），标出 1 AU、1 pc、银河系盘、1 Mpc、1 Gpc、CMB。天空视图：银道坐标莫尔韦德投影，l 向左增大，研究目标画为红点，全天足迹、巡天区域与缺坐标的目标列在图例中。全部用页面内 SVG 绘制，双语，切换语言时重绘。无头浏览器截图检查两种视图。
- 2026-11-14 · 环节 2 闸门 1 第 1 轮：无严重问题（投影用独立数值核对，双语、转义、暗色模式均通过）。次要意见采纳：窄屏时图表横向滚动而不缩小文字；颜色改为 CSS 变量，主题切换时随之改变；SVG 改用 role=group，视图按钮组加 aria-label；绘图失败时提示重新生成 atlas.json；层级代码转义；纬线路径不再折返。未改：足迹的 note 只有英文（数据模型没有 note_zh，以后需要时再加）；标签可能超出图边（现有数据不会发生）。
- 2026-11-14 · 环节 2 闸门 2（Codex）第 1 轮：无严重问题，**环节 2 通过双闸审查**（闸门 1：1 轮，0；闸门 2：1 轮，0）。次要意见采纳：等级颜色经固定白名单映射；足迹字段缺失时逐条退回默认值。未改：巡天说明只有英文（已知局限，见闸门 1 记录）。**计划完成。**
