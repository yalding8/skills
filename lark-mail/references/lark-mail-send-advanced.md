# mail 发信进阶：send_as / 投递状态 / 撤回 / 日程邀请

> **前置条件：** 先阅读 [`../../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。
>
> 本文覆盖所有发信 shortcut（`+send` / `+reply` / `+reply-all` / `+forward` / `+draft-create`）通用的进阶能力。

## 使用公共邮箱或别名（send_as）发信

当用户需要用非主账号地址发信时，使用 `--mailbox` 指定邮箱、`--from` 指定发件人地址。

- `--mailbox` 传邮箱地址（如 `shared@example.com` 或 `me`），可通过 `accessible_mailboxes` 查询可用值
- `--from` 传发信地址（别名、邮件组等），可通过 `send_as` 查询可用值

**查询可用邮箱和发信地址：**

```bash
# 查询可访问的邮箱（主邮箱 + 公共邮箱）
lark-cli mail user_mailboxes accessible_mailboxes --params '{"user_mailbox_id":"me"}'

# 查询某个邮箱的可用发信地址（主地址、别名、邮件组）
lark-cli mail user_mailbox.settings send_as --params '{"user_mailbox_id":"me"}'
```

**公共邮箱发信：**

```bash
# --mailbox 指定公共邮箱，From 头自动使用该邮箱地址
lark-cli mail +send --mailbox shared@example.com \
  --to bob@example.com --subject '通知' --body '<p>你好</p>'
```

**别名发信：**

```bash
# --mailbox 指定所属邮箱，--from 指定别名地址
lark-cli mail +send --mailbox me --from alias@example.com \
  --to bob@example.com --subject '测试' --body '<p>你好</p>'
```

不使用公共邮箱或别名时无需指定 `--mailbox`，行为与之前一致。

## 发送后确认投递状态

**立即发送（无 `--send-time`）**：邮件发送成功后（收到 `message_id`），**必须**调用 `send_status` API 查询投递状态并向用户报告：

```bash
lark-cli mail user_mailbox.messages send_status --params '{"user_mailbox_id":"me","message_id":"<发送返回的 message_id>"}'
```

返回每个收件人的投递状态（`status`）：1=正在投递, 2=投递失败重试, 3=退信, 4=投递成功, 5=待审批, 6=审批拒绝。向用户简要报告结果，如有异常状态（退信/审批拒绝）需重点提示。

**定时发送（指定了 `--send-time`）**：定时发送不会立即产生 `message_id`，`send_status` 在定时发送成功后会返回"待发送"状态，**不建议在定时发送后立即查询**。可在预定发送时间后再查询。如需取消定时发送：

```bash
lark-cli mail user_mailbox.drafts cancel_scheduled_send --params '{"user_mailbox_id":"me","draft_id":"<draft_id>"}'
```

**取消后邮件会变回草稿**，可继续编辑或在之后重新发送。

> **定时发送注意事项**：`--send-time` 必须与 `--confirm-send` 配合使用，不能单独使用。`send_time` 为 Unix 时间戳（秒），需至少为当前时间 + 5 分钟。

## 撤回邮件

发送成功后，若响应中包含 `recall_available: true`，说明该邮件支持撤回（24 小时内已投递的邮件）。

**撤回操作：**
```bash
lark-cli mail user_mailbox.sent_messages recall --as user \
  --params '{"user_mailbox_id":"me","message_id":"<message_id>"}'
```

- 返回 `recall_status: available` 表示撤回请求已受理（异步执行）
- 返回 `recall_status: unavailable` 表示不可撤回，`recall_restriction_reason` 说明原因

**查询撤回进度：**
```bash
lark-cli mail user_mailbox.sent_messages get_recall_detail --as user \
  --params '{"user_mailbox_id":"me","message_id":"<message_id>"}'
```

- `recall_status: in_progress` — 撤回进行中，可稍后再查
- `recall_status: done` — 撤回完成，查看 `recall_result`（`all_success` / `all_fail` / `some_fail`）和每个收件人的详情

**注意：** 撤回是异步操作，`recall` 返回成功仅表示请求已受理，实际结果需通过 `get_recall_detail` 查询。若响应中无 `recall_available` 字段，说明该邮件或应用不支持撤回，不要主动提及撤回。

## 发送日程邀请邮件

在邮件中嵌入日程邀请（`text/calendar`），收件人收信后可直接接受或拒绝日程。`To`/`Cc` 收件人自动成为参会人（ATTENDEE），发件人自动成为组织者（ORGANIZER）。

```bash
# 发送带日程邀请的新邮件（先保存草稿，确认后发送）
lark-cli mail +send --as user \
    --to alice@example.com --cc bob@example.com \
    --subject '产品评审' \
    --body '<p>请参加本次产品评审会议。</p>' \
    --event-summary '产品评审' \
    --event-start '2026-05-10T14:00+08:00' \
    --event-end '2026-05-10T15:00+08:00' \
    --event-location '5F 大会议室' \
    --confirm-send
```

**参数说明：**
- `--event-summary`：日程标题，设置此参数即开启日程邀请模式，需同时设置 `--event-start` 和 `--event-end`
- `--event-start` / `--event-end`：ISO 8601 格式时间，如 `2026-05-10T14:00+08:00`
- `--event-location`：可选，日程地点

**约束：**
- `--event-*` 与 `--send-time`（定时发送）互斥，不可同时使用
- `Bcc` 收件人不会成为日程参会人；如果邮件同时包含 Bcc 和日程，后端在发送时会拒绝该请求

读取含日程邀请的邮件时，`calendar_event` 字段包含日程详情（`method`、`summary`、`start`、`end`、`organizer`、`attendees` 等）。
