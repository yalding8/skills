---
name: event-broadcast-flow
description: 线下活动（行前会/分享会/展会）的报名-问卷-签到播报全流程编排，基于 feishu-broadcast 引擎既有模式。当用户提到新场次活动要上播报、报名播报、签到播报、行前问卷播报、活动结束下线、复用旧表单办新场次、或客户画像 enrich（订房/注册核验）时使用。核心价值：开场一次问齐全部决策点（避免多轮沟通）、指路抄哪个既有模式（避免重新发明）、上线前核验与会后下线闭环（避免漏关/漏开）。
---

# 活动播报全流程（feishu-broadcast）

## 分工铁律（先读这个）

- **机制 SSOT = repo README**（`~/Projects/feishu-broadcast/README.md`）：触发规则、
  filter 语义、state/seed/重开语义、防护机制。**本 skill 不复制机制，只指路**。
- **活状态 = project memory**（`project-2026-signup-broadcast.md`）：哪些 job 在跑、
  资源 ID、下线日期。做任何事前先读它，做完更新它。
- **本 skill = 流程编排**：问什么、抄什么、核什么、关什么。

## Phase 0 — 判定意图

| 用户在说 | 走 |
|---|---|
| 新场次要上报名/签到/问卷播报 | Phase 1 → 5 |
| 复用旧表单/旧表办新场次 | **高危**：旧 job 可能已 disabled → 读 [PATTERNS.md](PATTERNS.md) §重开 |
| 活动结束了 | Phase 5 下线闭环（当天做，历史上漏关过 6 天） |
| 查客户订房/注册/画像回写 | [PATTERNS.md](PATTERNS.md) §enrich |

## Phase 1 — 一次问齐决策点（AskUserQuestion 批量，别挤牙膏）

已知答案的跳过，其余**一轮问完**，每项给推荐默认：

1. **数据源**：新建 Base+表单，还是复用哪张表？（复用→触发列/身份键沿用先例）
2. **播报类型**：报名 / 签到 / 会前问卷，各要哪几个？
3. **Sink 群**：新群 or 复用哪个 webhook key？（key 名查 memory；新 key 要进服务器 .env）
4. **口径**：footer 统计范围（单场次 filter / 全场次累计）；签到人数=现场实数（默认）
5. **banner 色**：每城一色不重复（已用：🔴北 🔵沪 🟡广 🟢深 🟠郑）
6. **测试行处理**：物理删 / 必填题放行闸 / filter 拦（默认放行闸，别删别人数据）
7. **下线日期**：活动日 + 谁触发（默认活动当天晚上，建提醒）
8. **enrich 要不要**：订房/注册核验列（默认要，边际成本≈0）

## Phase 2 — 建 job：抄模式，别发明

查 [PATTERNS.md](PATTERNS.md) 模式索引表 → 复制对应 yaml + 模板 + 测试改参数。
命名：`<类型>-<城市拼音>-<MMDD>.yaml`、模板 `<类型>_<城市缩写><MMDD>_*.j2`。
**表单/表新接入先确认 dingning.ai 有读权限**（sheet 源还要查 app 的 sheet scope，见 README）。

## Phase 3 — 上线前核验（一条都不能跳）

- [ ] 触发列**预勾/预填行扫描**：`签到勾选==true` 带场次 filter 查一遍，非零先让现场取消
- [ ] **积压量预估**：新 job 首跑会补播多少条？说给用户听
- [ ] `pytest -q` 全绿 + `--once --dry-run --job <name>` 本地过
- [ ] .env 是否要加 key？（能复用就零改动）
- [ ] 复用表多 job 并行时：state 按 job 名隔离，确认身份键一致

## Phase 4 — 部署与验收

服务器 = dingning，**JumpServer 跳板**（本地 ssh 不通，给用户三行粘贴命令）：
`git pull` → `sudo systemctl restart feishu-broadcast` → `journalctl -u feishu-broadcast -n 30 --no-pager`
判据：job loaded 行 / 预期补播 sent N entries / 零 ERROR·DISABLED / 无意外 sent。

## Phase 5 — 会后下线闭环（活动当天！）

- [ ] 签到+问卷 job 设 `disabled: true`（PR），报名 job 看后续场次
- [ ] footer 预置场次摘除 / filter 换下一场（如 contains:上海）
- [ ] enrich：最后一场后 `launchctl unload` + REGISTRY 摘条目
- [ ] 无人值守时建一次性 cloud routine 开下线 PR（先例：retire-signup-2026-na）
- [ ] memory 更新：下线日期落档
