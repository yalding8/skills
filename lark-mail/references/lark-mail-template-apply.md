# mail 邮件模板套用（`--template-id` 合并规则）

> **前置条件：** 先阅读 [`../../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。
>
> 模板的创建 / 更新见 [`lark-mail-template-create.md`](./lark-mail-template-create.md) / [`lark-mail-template-update.md`](./lark-mail-template-update.md)。本文讲发信类 shortcut 通过 `--template-id <id>` 套用模板时的合并规则。

> **跟仓库 `assets/templates/` 的区别**：本文讲的是**飞书 OAPI 的个人邮件模板系统**（用户邮箱里的"我的模板"），可在飞书客户端管理；"仓库内置 HTML 模板库"（`assets/templates/`）是 lark-cli 仓库里预制的飞书原生 HTML 文件，可供写信参考。

## 套用模板（5 个发信 shortcut）

`+send` / `+draft-create` / `+reply` / `+reply-all` / `+forward` 均支持 `--template-id <id>`。`--template-id` 必须是**十进制整数字符串**。

合并规则（与 `lark/desktop` 对齐）：

| # | 场景 | 合并策略 |
|---|------|----------|
| Q1 to/cc/bcc | 全部 5 个 shortcut | 用户 `--to/--cc/--bcc` 先覆盖草稿原有值，再与模板 tos/ccs/bccs **无去重追加** |
| Q2 subject | `+send` / `+draft-create` | 用户 `--subject` > 草稿 subject > 模板 subject |
|  | `+reply` / `+reply-all` / `+forward` | 用户 `--subject` 覆盖自动 Re:/Fw:；否则保持 Re:/Fw: + 原邮件 subject。**模板 subject 被忽略**（保留会话线索） |
| Q3 body | `+send` / `+draft-create` | 空草稿 body → 用模板；非空 HTML → `draftBody + <br><br> + tplContent`；非空 plain-text → `\n\n` 拼接 |
|  | `+reply` / `+reply-all` / `+forward` | 模板内容注入 `<blockquote>` 之前；无 blockquote 则追加；plain-text 模板走 emlbuilder plain-text 追加 |
| Q4 附件 | 全部 5 个 shortcut | 模板 inline（SMALL）由 CLI 走 `user_mailbox.template.attachments.download_url` 下载后以 MIME part 注入；SMALL 非 inline 同样注入；LARGE（`attachment_type=2`）不下载，只把 `file_key` 放到 `X-Lms-Large-Attachment-Ids` header 让服务端渲染下载卡片 |
| Q5 cid 冲突 | inline 图片 | cid 由 UUID v4 生成（碰撞概率 ~ 2^-122），不显式检测 |

**Warning**：`+reply` / `+reply-all` + 模板且模板自带 tos/ccs/bccs 时，CLI 在 stderr 打印：`warning: template to/cc/bcc are appended without de-duplication; you may see repeated recipients. Use --to/--cc/--bcc to override, or run +template-update to clear template addresses.`

**size 约束**：单模板 `template_content` ≤ 3 MB；`body + inline + SMALL` 累计 ≤ 25 MB（超过则该批次剩余非 inline 附件切换为 LARGE；inline 不能切换）。

## 模板管理

- [`+template-create`](./lark-mail-template-create.md) — 创建新模板。`--name` 必填；正文通过 `--template-content` 或 `--template-content-file` 二选一；支持 HTML 内嵌图片自动上传到 Drive。
- [`+template-update`](./lark-mail-template-update.md) — 全量替换式更新（**后端无乐观锁，last-write-wins**）。支持 `--inspect`（只读 projection）/ `--print-patch-template`（patch 骨架）/ `--patch-file`（结构化 patch）/ 扁平 `--set-*` flag。
- 列表 / 获取 / 删除 走原生 API：`lark-cli mail user_mailbox.templates {list|get|delete} ...`。
