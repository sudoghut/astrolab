# STATUS · 全局研究状态

更新于 2026-11-11

## 当前阶段

M4 的 DR3 部分已完成并经过独立审稿（referee）。下一步：在 Gaia DR4 发布日运行 M4；其余时间推进 M1。

## 研究

| 研究 | 层级 | 状态 | 说明 |
|---|---|---|---|
| `000-smoke-test_gaia-dr3-10pc-census` | L3 | active | 冒烟测试（smoke test），管线端到端可用 |
| `001-m04-gaia-dormant-black-holes` | L4 | reproduced（DR3） | BH1、BH2 只用 DR3 复现成立；服务器端筛选与否决规则已在正样本上验证；DR4 查询已就绪 |

## 时间点

| 日期 | 事件 | 要做的事 |
|---|---|---|
| 2026-11-25 | Gaia 数据库下线 | 此前不需要再做 DR3 查询，所需结果都已缓存 |
| **2026-12-02** | **Gaia DR4 发布** | 见 M4 README 第 7 节：用 `TAP_SCHEMA` 确认表名，运行 `release="dr4"`，检验剩下的 51 个候选 |

## 下一步（按优先级）

1. **M1 · DESI BAO**：先写工作计划（work plan），再引入 `cosmo` 和 `infer` 两个模块。
2. **Atlas 导航**：天空视图和尺度视图，研究以足迹（footprint）形式出现在图上。需要先写 004 号或之后编号的计划。
3. **技能（skills）**：已有 `referee` 和 `server-side-query`；待抽出的有新建研究、文献核实、DR4 发布日运行手册。

## 待用户决定

- 是否初始化 git 版本库？是否推送到 GitHub？
