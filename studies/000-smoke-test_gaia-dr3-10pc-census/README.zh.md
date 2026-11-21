# 冒烟测试：Gaia DR3 的 10 pc 邻域普查

> English: [README.md](README.md)。以英文 `README.md` 为准（预注册与判据的权威文本）；本文件是它的中文译本，节号与表格一一对应，英文改动时在同一个 PR 中同步修改。 网页在线版：[https://sudoghut.github.io/astrolab/studies//web/](https://sudoghut.github.io/astrolab/studies//web/)。

## 1. 问题

整个环境能否在真实数据上端到端（end to end）跑通？这是一项工程检查（engineering check），
不是研究结果。

## 2. 假设与判据

- `parallax > 100 mas` 查询返回几百行（MB 量级），并被缓存（cache）；
  第二次运行不发出网络请求。
- 经过质量筛选（quality cut）（`parallax_over_error > 10`、`ruwe < 1.4`）之后，最近的
  天体是 Proxima Centauri（约 1.30 pc）。注意 α Cen A/B 太亮，无法得到可靠的
  Gaia 天体测量（astrometry），可能缺失。
- 在服务器端把所有 G < 11 的恒星聚合（aggregation）到 768 个 HEALPix（Hierarchical Equal Area isoLatitude Pixelization，分层等面积等纬度像素化）像素中，
  恰好返回 768 行，并且银道面（Galactic plane）清晰可见。

## 3. 数据（附大小估计）

| 输入 | 来源 | 选择条件 | 预估大小 |
|---|---|---|---|
| 近邻源 | Gaia DR3 `gaia_source`（TAP: gaia） | `parallax > 100` | 约 10² 行，< 100 kB |
| 亮星密度 | Gaia DR3 `gaia_source` | `G < 11`，按 HEALPix 第 3 级（level 3）`GROUP BY` | 768 行 |

## 4. 方法

绝对星等（absolute magnitude）`M_G = G + 5 log10(parallax / 100 mas)`；切向速度（tangential velocity）
`4.74 μ / ϖ`。不做消光改正（extinction correction）（在 10 pc 以内可以忽略）。

## 5. 结果

见 `web/index.html` 与 `results/summary.json`。
