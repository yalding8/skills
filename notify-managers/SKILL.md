---
name: notify-managers
description: 以丁宁本人飞书账号给留学事业部管理团队（9 位主管）一对一批量发消息，内置经过精确校验的姓名→open_id 名单、文档授权前置步骤和发送脚本。当用户说"发给管理团队/通知各主管/给管理层发一下/一对一发给主管们"，或要把文档/活动信息分发给主管并收集意见时使用。
---

# notify-managers — 管理团队一对一发消息

## 名单（2026-07-17 经 localized_name 精确匹配校验）

| 姓名 | open_id | 部门 |
|---|---|---|
| 王强 | ou_a9ba23e7a1b5c7a448587c326016fb4e | 苏皖团队 |
| 鲍馨柔 | ou_a4c72aed5683f05fc3f37f2096daa6c5 | 上海与浙江团队 |
| 刘雅婷 | ou_79bb8c9614b709c77d7c0a86e09f0159 | 北京与华北团队 |
| 韦刚 | ou_fa3c91bcee8321ee05bc1f717b771b5a | 留学渠道部 |
| 闫明亮 | ou_4993a9a76580073b63fea586f3c95fdc | 华南团队 |
| 张博 | ou_e49600c8d1e60d762219fad118eae8c5 | 华中与西部团队 |
| 雷宇航 | ou_7668fa6e878bed2de42fee93a37d15c8 | 金融推广部 |
| 杨传玉 | ou_40049ccb3240bc57f95911a5cac971cd | 郑州组 |
| 王金姣 | ou_fa6c7cdf203b39a32ca5104324dab136 | 天津缴费组 |

来源：`~/Projects/feishu-work-digest/pilot_roster.json` 的 `_managers_top`（9 主管汇报给丁宁）。

## 工作流

1. **确认两件事再发**（外部副作用，硬规则）：①发送范围（全部 9 人 or 子集，让用户确认）②文案全文（先展示给用户）。
2. **消息含飞书文档链接时，先授权**（否则对方点开是无权限页）：
   ```bash
   lark-cli drive +member-add --token <doc_token> --type docx --member-type openid \
     --member-id "<逗号分隔的open_id，≤10个>" --perm view --as user --yes
   ```
3. **发送**：写文案到临时文件（正文用 `{NAME}` 占位称呼），执行：
   ```bash
   bash ~/.claude/skills/notify-managers/scripts/send.sh <message_file> [姓名1 姓名2 ...]
   ```
   不带姓名参数=发全部 9 人；带姓名=只发指定子集。
4. **汇报**：逐人 ✅/❌ 结果。

## 安全规则

- `--as user`（丁宁本人名义）仅限用户明确要求本人发送的场景——本技能默认场景即是；若用户要求以机器人名义，改用 `--as bot`（dingning.ai）。
- 消息文案守异乡缴费红线（禁词/权益数字/绝对化，见 `~/Projects/uhomespay-geo/CLAUDE.md`）当内容涉及缴费业务时。
- **名单更新**：人事变动后用 `lark-cli contact +search-user --query "<姓名>" --as user` 重新解析，**必须按 `localized_name` 精确匹配**——已知陷阱：搜"雷宇航/杨传玉"会命中"郑州雷宇航组/杨传玉组"的组员（部门名含主管名），不能取第一条。
- 同步更新本文件名单表和 `scripts/send.sh` 内嵌 roster（两处都要改）。
