# 模式索引：新场景抄哪个（全部在 ~/Projects/feishu-broadcast）

> 每个模式都有跑过生产的 yaml + 模板 + 测试三件套。抄最近的先例改参数，别从零写。

## 报名播报（new_row）

| 场景 | 抄 | 要点 |
|---|---|---|
| 新报名表，字段自定 | `jobs.d/signup-2026-na.yaml` + `signup_na_*.j2` | 长场次串拆「城市场 · 日期」；footer 预置恒显（0 组照列，选项名与模板耦合） |
| 表里有遗留测试行 | `jobs.d/checkin-shenyang-0710.yaml` 的 trigger | **必填题当放行闸**：column+nonempty，正式提交必触发、遗留行永不触发，不删别人数据 |

## 签到播报（cell_change checkbox）

| 场景 | 抄 | 要点 |
|---|---|---|
| bitable + checkbox 签到 | `jobs.d/checkin-beijing-0718.yaml` + `checkin_bj0718_*.j2` | 勾「签到勾选」+填「签到人数」（现场实数口径）；interval 15s；famcount 封顶 |
| 同表多场次 | 同上 sink filter | `contains:<城市>` 圈触发行+footer 分母；banner 每城一色 |
| sheet 源 | `jobs.d/checkin-nanjing-0613.yaml` | ⚠️ 先确认引擎 app 有 sheets scope（6.13 郑南事故） |

## 会前问卷播报

抄 `jobs.d/survey-preevent-0711.yaml` + `survey_*.j2`。未订房=热线索标 🔥；
回收中途追加题→模板 `{% if %}` 整行隐藏（≠恒显示，语义见 README）。

## §重开：复用旧表单办新场次（本 skill 诞生的直接原因）

**症状**：表单链接带新 prefill 复发出去了，但 job 早已 `disabled: true` → 新填报静默积压。
**动作**：
1. 移除 `disabled`，**job 名保持不变**（沿用 state，旧记录不重发，新记录自动补播）
2. sink 加/换 `filter: contains:<新场次>`——旧场次行"fired 未 sent"永久挂起，不误播；
   footer 只算新场次
3. 下一场次再换 filter；全结束才 disable
先例：PR #40 重开 survey-preevent-0711；语义测试 `tests/test_survey_0718_reopen_job.py`

## §enrich：客户画像回写（订房/注册核验）

抄 `scripts/enrich_us_booking.py`（改查询条件/字段名即可）：
- 链路 `uhz_customer.phone → stat_rent_order_business`（宽表有 country/status/公寓名；
  **宽表 mobile 是脱敏的**，必须经 uhz_customer 明文 phone 关联）
- 注册核验与订房同链路零成本；分层价值：注册未订=现场转化优先
- 幂等逐行 diff；异常手机号容错**必须带响的计数**（WARN 行）
- 回写字段带溯源戳；跑 Mac launchd（`setup_launchd_enrich.sh`；launchd PATH 无
  node/lark-cli，plist 注入 fnm bin）。**迁服务器路径**：dingning 走 VPC 可直连 ADB，
  卡点只是 bot 对 Base 只读——升可编辑+.env 配凭证即可迁 cron
- 新 emitter 必过 born-traceable（REGISTRY 手填 launchd 条目）

## 已知坑速查（血的教训，部署前扫一眼）

- bitable 表头必须取字段 schema，空列会被 records API 省略（README 防护机制节）
- checkbox：True→"1"/False→"0"，truthy 恰好只认勾选（有单测锁死）
- 场次选项从表单删除后，老记录该字段**显示为空**→ filter 拦不住的场景要重查
- 手机号 entry 一律脱敏（前3****后4）；姓名换行 `replace("\n"," / ")`
- 新加 sink 到已上线 job：先 stop→seed→start，否则积压灌群（README 冷启动节）
- lark-cli `--as bot` 读表报 99991672 是 CLI quirk，引擎读权限以服务器 dry-run 为准
- 部署完必须看 journalctl 验收，"没报错"≠"跑对了"——对着 Phase 4 判据逐条勾
