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
1. **规划与设计** — PRD、拆分、评审、接口设计
2. **开发** — TDD、重构、架构改进、问题诊断
3. **工具与配置** — Git hooks、pre-commit、格式化
4. **写作与知识** — 技能编写、文章编辑、Obsidian
5. **前端设计 (Impeccable)** — 21 个设计词汇技能
6. **营销与增长** — 文案、SEO、广告、邮件、社媒
7. **转化优化 (CRO)** — 页面、表单、注册、弹窗、定价
8. **收入运营** — 销售赋能、流失防控、推荐计划、RevOps

## 命名规范
- 目录名 = skill 名，全小写 kebab-case
- 不创建重复 skill（如同时存在 `foo` 和 `foo-plan`，只保留活跃的那个）
- 已废弃的 skill 在同步时自动清理

## 提交规范
- 同步脚本自动提交，消息格式：`Sync skills from ~/.claude/ (YYYY-MM-DD)`
- 手动改动使用常规 commit message
