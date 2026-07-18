---
name: event-signup-form
description: 线下活动报名表单快速制作——按 B端（国际教育行业展会/海外资源推介会）与 C端（行前指导活动/好居面对面租房咨询专场）四类活动给字段模板，建表建单有章法、数据表复用不乱建 Base。当用户说新场次活动要建报名表单/收集表、香港·展会·推介会·行前会·好居面对面要报名、复用哪张表收数、把表单模板化时使用。产出止于"表单可收数+引擎可读"，播报/签到/下线闭环交给 event-broadcast-flow。
---

# 活动报名表单制作（event-signup-form）

## 分工铁律

- **本技能**：分型 → 字段模板 → 建表 → 表单配置 → 授权，止于「表单可公开收数 + dingning.ai 可读」。
- **播报/签到/问卷/enrich/下线闭环** = `event-broadcast-flow`（技能末尾显式交接，别在这里做）。
- **Base/字段/表单的具体 API 操作** = `lark-base` skill（本技能只说做什么和坑在哪）。
- **活状态**（哪些系列表在用、资源 ID）= project memory `project-2026-signup-broadcast.md` /
  `project-2026-expo-checkin.md`，动手前先读，做完更新。

## Phase 0 — 分型（先问清是哪类活动）

| 面向 | 类型 | 先例 | 模板 |
|---|---|---|---|
| B端 | 国际教育行业展会 | 沈阳 7.10 | [TEMPLATES.md](TEMPLATES.md) §B1 |
| B端 | 海外资源推介会 | （展会裁剪） | §B2 |
| C端 | 行前指导活动 | NA 系列/香港系列 | §C1 |
| C端 | 好居面对面·租房咨询专场 | 现场咨询登记表改造 | §C2 |

## Phase 1 — 一次问齐（AskUserQuestion 批量，别挤牙膏）

已知答案的跳过：①**新系列还是旧系列加场**（旧系列=场次单选加选项即完事，勿建新表）；
②场次（日期+时间+城市，进选项名）；③目的地/院校等定制项与内容偏好选项（拟稿给用户确认）；
④要不要播报+哪个群（新 key 要进服务器 .env）；⑤顾问归因/白名单 lookup 要不要；
⑥表单开放设置（默认公开可重复提交）。

## Phase 2 — 建表（硬规则）

1. **一个活动系列一张长期表**，场次做单选字段追加选项；同类型进同一 Base
   （路由见 [TEMPLATES.md](TEMPLATES.md) §Base 路由），**不新建 Base**。
2. 场次选项命名 `M月D日 HH:MM-HH:MM【城市场】`——播报模板按 `【】` 拆解，
   **改选项名须同步播报 footer 预置**（已知耦合）。
3. **电话字段用 text 不用 phone 类型**（新版表单 API 不收 phone 样式字段，沈阳踩坑）。
4. 运营列建表时一次带齐（签到勾选 checkbox + 签到人数 number + 备注），
   后续 checkin 播报 job 直接可用，不用临场补列。

## Phase 3 — 表单配置

按模板题序建题、设必填、开公开填写。**API 坑清单必读**：[TEMPLATES.md](TEMPLATES.md) §表单 API 坑。

## Phase 4 — 收尾交接（固定三步）

- [ ] dingning.ai（`cli_aa9afd3b72b9dbeb`）授 view 协作者；引擎真可读以服务器 `--dry-run` 为准
- [ ] 要播报 → 切 `event-broadcast-flow`（Phase 2 起）；给出场次选项名供 footer 预置
- [ ] memory 落档：表/表单/链接资源 ID + 各场下线日期（活动当天下线，历史漏关过 6 天）
