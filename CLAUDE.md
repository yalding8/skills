# Skills 仓库规则

## 项目概述
个人 Claude Code / Cursor / AI 编码工具的 Skill 合集，从 `~/.claude/` 自动同步。

## 同步机制
- 源：`~/.claude/skills/`（技能目录）+ `~/.claude/commands/`（命令文件）
- 目标：本仓库各子目录，每个 skill 一个文件夹，入口为 `SKILL.md`
- 脚本：`~/.claude/scripts/sync-skills.sh`
- 触发：手动 `/sync-skills` 或安装新 skill 后执行

## README 规则
- **默认中文版本**，英文版本以折叠 `<details>` 形式附在底部
- 同步脚本自动生成 README，手动编辑会被覆盖
- 所有 skill 必须归类到对应分组中

## Skill 分类体系
> 与 `sync-skills.sh` 中的分类数组保持一致；改分类时先改脚本，再回写本节。

1. **规划与设计** — PRD、拆分、评审、接口设计
2. **开发** — TDD、重构、架构改进、小程序开发
3. **工具与效率** — Git hooks、pre-commit、溯源、IPFS 发布、Obsidian
4. **前端设计 (Impeccable)** — 21 个设计词汇技能
5. **前端工程** — 移动端、响应式、Web 性能、平台能力门禁
6. **Cloudflare 开发** — Workers、Wrangler、Durable Objects、Agents/Sandbox SDK
7. **认知与写作** — ljg 思维工具、写作引擎、技能编写
8. **视觉铸造** — ljg 卡片、归藏社交卡片/PPT
9. **营销与增长** — 文案、广告、邮件、社媒、公众号发布
10. **SEO 与搜索** — 审计、AI SEO、结构化数据、站点架构
11. **转化与变现** — CRO、定价、流失防控、推荐计划、RevOps
12. **飞书 Lark** — lark-* 全家桶（文档、表格、消息、日历、审批等）
13. **企业微信 WeCom** — wecomcli-* 系列
14. **业务工作流** — insight-report、interview-copilot 等业务专用流程

共享库（如 `_feishu-core`，无 SKILL.md）不列入 README 分类表。

## 命名规范
- 目录名 = skill 名，全小写 kebab-case
- 不创建重复 skill（如同时存在 `foo` 和 `foo-plan`，只保留活跃的那个）
- 已废弃的 skill 在同步时自动清理

## 提交规范
- 同步脚本自动提交，消息格式：`Sync skills from ~/.claude/ (YYYY-MM-DD)`
- 手动改动使用常规 commit message
