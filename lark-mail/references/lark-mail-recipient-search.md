# mail 收件人搜索：查找邮箱地址

> **前置条件：** 先阅读 [`../../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

当需要查找收件人邮箱地址时，使用联系人搜索接口。支持多种搜索方式，如：
- **按人名搜索**：如"给张三发邮件" → query="张三"
- **按邮箱关键词搜索**：如"发到 larkmail 的邮箱" → query="@larkmail"
- **按群名搜索**：如"发给项目群" → query="项目群"

```bash
lark-cli mail multi_entity search --as user --data '{"query":"<关键词>"}'
```

搜索结果包含多种实体类型：

| `type` 值 | `tag` 示例 | 说明 |
|-----------|-----------|------|
| `user` / `chatter` | `chatter` | 个人用户 |
| `enterprise_mail_group` | `mail_group` | 企业邮件组 |
| `chat` / `group` | `chat_group_tenant` / `chat_group_normal` | 群聊（有群邮件地址） |
| `external_contact` | `external_contact` | 外部联系人 |

**处理规则：**
1. 从结果中筛选有 `email` 字段的条目
2. 无论匹配数量多少，都必须列出候选项供用户确认后再使用（搜索是模糊匹配，单条结果不代表精确命中）。展示尽可能多的字段帮助用户区分：
   ```text
   找到以下匹配"张三"的结果：
   1. 张三 <zhangsan@example.com>
      类型：user | 部门：研发团队
   ---
   找到多个匹配"组"的结果，请选择：
   1. 团队邮件组 <team@example.com>
      类型：enterprise_mail_group | 标签：mail_group
   2. 项目群 <project@example.com>
      类型：chat | 成员数：50 | 标签：chat_group_normal
   3. 张群 <zhangqun@example.com>
      类型：user | 部门：研发团队 | 备注名：张群同学
   ```
   可用字段：`name`（名称）、`email`（邮箱）、`department`（部门）、`tag`（标签）、`display_name`（备注名）、`type`（实体类型）、`member_count`（成员数，群类型时展示）。字段为空时省略。
3. 若无匹配，告知用户未找到，建议换关键词或直接提供邮箱地址
4. 用户确认后，将 `email` 传入 compose shortcut 的 `--to` / `--cc` / `--bcc` 参数

**注意：** 用户直接提供完整邮箱地址时不需要搜索，直接使用即可。
