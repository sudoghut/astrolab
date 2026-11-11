# 研究日志（research log）· Gaia DR3 10 pc 普查（冒烟测试）

## 2026-11-11

创建本研究，用来验证 001 号计划的环境搭建是否端到端（end-to-end）可用。

### 第一次运行

两次表访问协议（TAP, Table Access Protocol）查询都成功了：

| 查询 | 结果 |
|---|---|
| 视差（parallax）大于 100 mas | 315 行 |
| G < 11 的亮星，按 HEALPix（Hierarchical Equal Area isoLatitude Pixelization）3 级聚合 | 约 125 万颗星在服务器端聚合（server-side aggregation）后，只返回 768 行 |

出现一个问题：HEALPix 索引的类型是 int32，`astropy_healpix` 要求 int64。已在 `run.py` 中转换类型。

### 第二次运行

- 完全命中缓存（cache），耗时 0.12 秒。
- 质量切割（quality cut）条件为 `parallax_over_error > 10` 且 `ruwe < 1.4`（RUWE, Renormalised Unit Weight Error），切割后剩 238 个天体，其中 5 pc 以内 39 个。
- 最近的五个天体：

| 天体 | 距离 |
|---|---|
| 比邻星（Proxima Centauri） | 1.302 pc |
| 巴纳德星（Barnard's Star） | 1.828 pc |
| Wolf 359 | 2.409 pc |
| Lalande 21185 | 2.546 pc |
| 第五个天体 | 2.976 pc |

  这与已知值一致。
- 半人马座 α 星 A/B（α Centauri A/B）不在样本中。它们太亮，Gaia 的天体测量（astrometry）不可靠，符合预期。
- 切向速度（tangential velocity）中位数为 34.4 km/s。

### 结论

管线（pipeline）可用。3 项结论测试（conclusion tests）全部通过。
