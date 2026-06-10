---
name: born-traceable
description: Use when creating a NEW project, or adding any scheduled job / cron / emitter / report generator that produces a recurring production artifact (飞书卡片, 企微推送, BI 报告, bitable 写入, 海报, 数据管道). Makes the project/job "出生即可溯源": stamps every artifact with its origin, puts the trigger in git, registers a healthcheck + REGISTRY entry for critical emitters, and verifies via reconcile. Triggers on 新建项目, 新项目, 加定时任务, 新 emitter, scheduled job, new cron, /born-traceable.
user-invokable: true
---

让一个新项目 / 新定时任务「出生即可溯源」。这是溯源契约的**创建时 push 层**。

**为什么/是什么（规格、红队、20-cap 约束）不在这里**——单一真相源是
`~/Projects/ops-deploy-kit/docs/PROVENANCE_CONTRACT.md`。本 skill 只给**动词 + 物料指针**。
读契约 §2「三机制」+ §5「验收判据」再动手。

## 先判定：这是 emitter 还是别的？

- **emitter**（产出业务产物：发群/写表/出报告/出图）→ 全套 ①②③ 适用。
- **watchdog / ci / deploy**（监控/测试/部署，不产业务物）→ 只需 ②（触发进 git），跳过 ①③，并在 REGISTRY 标 `role`。
- 一次性脚本、本地工具 → 不在契约范围，跳过。

## Checklist（逐条建 TodoWrite，按顺序做）

### ① 产物盖戳（每个 emitter，无上限）
- [ ] 拷 `~/Projects/ops-deploy-kit/templates/provenance.python.example.py`（或 `.nodejs.example.ts`）进项目，去掉 `.example`。
- [ ] 产物出口处调用 `build_provenance(script=..., repo=..., trigger=...)`，把返回串放进产物低调位置（文末行/页脚/隐藏字段）。
- [ ] **不变量验证**：故意让 git 不可用（或读模板源码确认），戳里 `源 <repo>/<script>` 必须仍在，只有 commit 降级成 `unknown`。repo/script 是入参不靠 git——别破坏。

### ② 触发进 git（每个定时任务，无上限）
- [ ] **服务器 cron**：拷 `templates/setup_cron.example.sh` → 项目 `scripts/setup_cron.sh`，改 PROJECT/RUN_USER/cron 行。写 `/etc/cron.d/<项目>`（**绝不写用户 crontab**）。规范见 `docs/CRON_SCHEDULING.md`。
- [ ] **GHA**：workflow 文件进仓（`.github/workflows/*.yml`），`on.schedule` cron 用 **UTC**（记牢 tz）。
- [ ] **external-dispatch**（Cloudflare Worker / repository_dispatch 触发 GHA）：在 REGISTRY 手填 `external-dispatch` 条目（扫描抓不到）。
- [ ] **systemd 常驻服务**：手填 REGISTRY，不进 cron 扫描。

### ③ 死人开关（仅关键 emitter，20-cap）
> 静默失败=丢钱/丢数据才建。先数名额，**别让 20-cap 当通用天花板**。
- [ ] `GET /api/v3/checks/`（key `~/.config/healthchecks/api-key`）数名额；≥19 则停下问用户取舍（合班 / self-host / 跳过）。
- [ ] 用 Management API 建 check（`unique:["slug"]` 幂等 upsert，`tz:"Asia/Shanghai"`，`grace`≥3600，`schedule` 与 cron 时刻一致）。模板见 CLAUDE.md「healthchecks.io check 由 AI 自建」。
- [ ] cron 行尾接 `&& curl -fsS -m10 --retry2 "https://hc-ping.com/$(cat <key文件>)/<slug>"`（仅成功触发）。
- [ ] ⚠️ **写了 ping ≠ check 存在**。当场建 check，绝不留「以后建」（否则死人开关一直哑）。

### ④ 登记 REGISTRY（机器字段自动，语义字段手填）
- [ ] 机器字段（trigger/schedule/tz/healthcheck/repo）跑 `python3 ~/Projects/ops-deploy-kit/scripts/registry_scan.py` 自动派生——**别手写**。
- [ ] 只手填语义字段：`name` / `output.channel` / `output.webhook_secret`（存指针不存值）/ `role` / `consumers` / `spec_doc`。schema 见 `docs/REGISTRY_SCHEMA.md`。

### ⑤ 自验（闭环这一次出生）
- [ ] 跑 `python3 ~/Projects/ops-deploy-kit/scripts/registry_reconcile.py`，确认本任务**不在 WILD**（已被登记）、healthcheck **不在 DEADMAN**（ping 不打 404）、**不在 DOWN**。
- [ ] 绿了才算「出生即可溯源」。

## 边界（别越界）
- 本 skill 是 **push 层，不验证跨时间漂移**。三个月后改了输出没人重跑——那是 `registry_reconcile.py` 定时跑（机制层）的活，**确保 reconcile 已上 cron**，否则这一层是悬空的。
- 溯源 ≠ 正确：戳能追到 commit，但不保证产物对。别把 born-traceable 当质量门。
