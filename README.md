# Agent Skills

个人 AI 技能合集，适用于 Claude Code、Cursor 等 AI 编码助手。151 个技能，14 大分类。

> 从 `~/.claude/` 自动同步 · [English version](#english-version)

---

## 规划与设计

在写代码之前理清思路。

| 技能 | 说明 |
|------|------|
| [write-a-prd](./write-a-prd) | 通过用户访谈 + 代码探索创建 PRD，提交为 GitHub Issue |
| [prd-to-issues](./prd-to-issues) | 将 PRD 拆分为可独立认领的 GitHub Issue（tracer-bullet 纵切） |
| [prd-to-plan](./prd-to-plan) | 将 PRD 转化为多阶段实施计划，保存为本地 Markdown |
| [grill-me](./grill-me) | 对方案/设计进行追问式压力测试，逐一解决决策树分支 |
| [design-interface](./design-interface) | 并行生成多个截然不同的模块接口设计方案 |
| [ubiquitous-language](./ubiquitous-language) | 提取 DDD 风格的统一语言词汇表 |

## 开发

编写、重构和修复代码。

| 技能 | 说明 |
|------|------|
| [tdd](./tdd) | 红-绿-重构循环的测试驱动开发 |
| [triage-issue](./triage-issue) | 探索代码定位根因，创建含 TDD 修复方案的 GitHub Issue |
| [improve-architecture](./improve-architecture) | 发现架构改进机会，通过深化浅模块提升可测试性 |
| [request-refactor](./request-refactor) | 通过用户访谈创建小步提交的重构方案，提交为 GitHub Issue |
| [migrate-to-shoehorn](./migrate-to-shoehorn) | 将测试文件的 as 类型断言迁移为 @total-typescript/shoehorn |
| [miniprogram-development](./miniprogram-development) | 微信小程序开发 — 构建、调试、预览、发布、云开发 |

## 工具与效率

开发环境、知识管理和实用工具。

| 技能 | 说明 |
|------|------|
| [setup-pre-commit](./setup-pre-commit) | 配置 Husky pre-commit hooks + lint-staged + 类型检查 + 测试 |
| [git-guardrails](./git-guardrails) | 设置 Claude Code hooks 拦截危险 git 命令 |
| [fix-format](./fix-format) | 格式修正 |
| [sync-skills](./sync-skills) | 将已安装的 skills 同步到 GitHub 仓库 |
| [verify-blockers](./verify-blockers) | 验证阻塞项 |
| [scaffold-exercises](./scaffold-exercises) | 创建练习目录结构 |
| [obsidian-vault](./obsidian-vault) | 搜索、创建和管理 Obsidian 笔记 |
| [ljg-skill-map](./ljg-skill-map) | 技能地图 — 扫描已安装技能渲染 ASCII 总览 |
| [ljg-x-download](./ljg-x-download) | X/Twitter 媒体下载到本地 |
| [born-traceable](./born-traceable) | 新项目/定时任务出生即可溯源 — 产物盖戳 + 触发进 git + 死人开关 |
| [update-readme](./update-readme) | 扫描 git 历史更新 README，保持现有格式 |
| [publish-artifact](./publish-artifact) | 发布 HTML/附件/目录到私有 IPFS Cluster，返回不可变分享链接 |
| [kubo-deploy-e2e](./kubo-deploy-e2e) | 私有 IPFS Cluster（Kubo）部署链路端到端测试 — 单机 3 节点 compose |
| [kubo-publish-e2e](./kubo-publish-e2e) | Agent 发布链路端到端测试 — 经 token 写入口发布 HTML 到 IPFS Cluster |

## 前端设计 — Impeccable

来自 [Impeccable](https://github.com/pbakaus/impeccable) — AI 辅助前端开发的设计词汇与反模式库。

| 技能 | 说明 |
|------|------|
| [frontend-design](./frontend-design) | 综合设计技能，生成高品质、有特色的前端界面 |
| [teach-impeccable](./teach-impeccable) | 首次设置：采集项目设计上下文并持久化 |
| [audit](./audit) | 技术质量检查 — 无障碍、性能、响应式 |
| [critique](./critique) | UX 设计评审 — 层级、清晰度、情感共鸣 |
| [polish](./polish) | 上线前最终打磨 — 对齐、间距、一致性 |
| [typeset](./typeset) | 修复字体选择、层级、尺寸、可读性 |
| [arrange](./arrange) | 修复布局、间距、视觉节奏 |
| [colorize](./colorize) | 为单色界面添加战略性色彩 |
| [animate](./animate) | 添加有意义的动效和微交互 |
| [normalize](./normalize) | 对齐设计系统标准 |
| [distill](./distill) | 去除不必要的复杂性，提炼精华 |
| [clarify](./clarify) | 改善不清晰的 UX 文案和微文案 |
| [optimize](./optimize) | 性能优化 — 加载、渲染、包体积 |
| [harden](./harden) | 错误处理、国际化、边界情况 |
| [bolder](./bolder) | 放大平淡设计的视觉冲击力 |
| [quieter](./quieter) | 降低过于激进的设计 |
| [delight](./delight) | 添加愉悦感和个性化触点 |
| [extract](./extract) | 提取为可复用组件和设计 token |
| [adapt](./adapt) | 适配不同设备和场景 |
| [onboard](./onboard) | 设计引导流程和空状态 |
| [overdrive](./overdrive) | 突破常规限制的技术炫技效果 |

## 前端工程

移动端、响应式与性能。

| 技能 | 说明 |
|------|------|
| [mobile-design](./mobile-design) | 移动端 UX 模式、触控交互、手势设计与移动优先原则 |
| [responsive-design](./responsive-design) | 移动优先响应式设计 — 流式布局、媒体查询、flexbox/grid |
| [web-perf](./web-perf) | 用 Chrome DevTools 分析 Web 性能，度量 Core Web Vitals |
| [platform-check](./platform-check) | 防止 AI 重复实现平台原生能力 — 改 UI 前三道门禁 |

## Cloudflare 开发

Workers 生态：部署、状态、沙箱、Agent、邮件。

| 技能 | 说明 |
|------|------|
| [cloudflare](./cloudflare) | Cloudflare 开发总纲 — Workers、Pages、R2、KV 等产品选型与集成 |
| [wrangler](./wrangler) | Wrangler CLI — Cloudflare Workers 项目配置与部署 |
| [workers-best-practices](./workers-best-practices) | Cloudflare Workers 最佳实践 |
| [durable-objects](./durable-objects) | Durable Objects — 有状态协调、RPC、SQLite、告警、WebSocket |
| [agents-sdk](./agents-sdk) | 用 Agents SDK 在 Cloudflare Workers 上构建 AI Agent |
| [sandbox-sdk](./sandbox-sdk) | Sandbox SDK — 安全沙箱代码执行、代码解释器、CI/CD |
| [cloudflare-email-service](./cloudflare-email-service) | Cloudflare Email Service 收发事务邮件 |

## 认知与写作

思维工具和写作引擎。部分来自 [ljg-skills](https://github.com/lijigang/ljg-skills)。

| 技能 | 说明 |
|------|------|
| [ljg-learn](./ljg-learn) | 概念解剖 — 八维切割 + 顿悟压缩 |
| [ljg-rank](./ljg-rank) | 降秩引擎 — 找出领域背后不可再少的独立生成器 |
| [ljg-roundtable](./ljg-roundtable) | 圆桌讨论 — 真实人物多轮辩证对话 |
| [ljg-invest](./ljg-invest) | 投资分析 — 判断项目是否是「秩序创造机器」 |
| [ljg-writes](./ljg-writes) | 写作引擎 — 带观点出发，写的过程中想透 |
| [ljg-plain](./ljg-plain) | 白话引擎 — 改写到 12 岁聪明小孩也能懂 |
| [ljg-word](./ljg-word) | 英语单词深度拆解（词源、核心意象、金句） |
| [write-a-skill](./write-a-skill) | 创建结构完整的新 agent skill |
| [edit-article](./edit-article) | 重组段落、提升清晰度、精简文字 |

## 视觉铸造

将内容铸成可分享的视觉产物。来自 [ljg-skills](https://github.com/lijigang/ljg-skills)。

| 技能 | 说明 |
|------|------|
| [ljg-card](./ljg-card) | 内容铸 PNG 卡片（长图/信息图/多卡/视觉笔记/漫画/白板） |
| [ljg-paper](./ljg-paper) | 论文阅读器 — 为非学术人士提取论文思想 |
| [ljg-paper-flow](./ljg-paper-flow) | 论文流 — 读论文 → 铸卡片一气呵成 |
| [ljg-word-flow](./ljg-word-flow) | 词卡流 — 解词 → 铸信息图一气呵成 |
| [ljg-travel](./ljg-travel) | 旅行研究 — 城市文化 DBA + 便携参考卡片 |
| [guizang-social-card-skill](./guizang-social-card-skill) | 归藏风格社交卡片 — 小红书图文套图 + 公众号封面对 |
| [guizang-ppt-skill](./guizang-ppt-skill) | 归藏风格 PPT/幻灯片生成 |

## 营销与增长

策略、内容和渠道执行。

| 技能 | 说明 |
|------|------|
| [product-marketing-context](./product-marketing-context) | 建立产品定位、受众和消息框架基础文档 |
| [marketing-ideas](./marketing-ideas) | 头脑风暴营销策略和增长点子 |
| [marketing-psychology](./marketing-psychology) | 将心理学原理应用于营销决策 |
| [copywriting](./copywriting) | 撰写或重写网站营销文案 |
| [copy-editing](./copy-editing) | 编辑和润色现有营销文案 |
| [content-strategy](./content-strategy) | 规划内容策略、选题和发布节奏 |
| [social-content](./social-content) | 创建和优化社交媒体内容 |
| [cold-email](./cold-email) | 撰写 B2B 冷邮件和跟进序列 |
| [email-sequence](./email-sequence) | 设计自动化邮件序列和培育流程 |
| [paid-ads](./paid-ads) | 付费广告策略、投放和优化 |
| [ad-creative](./ad-creative) | 批量生成和迭代广告创意素材 |
| [launch-strategy](./launch-strategy) | 产品发布和上市策略 |
| [lead-magnets](./lead-magnets) | 设计吸引潜客的免费资源 |
| [free-tool-strategy](./free-tool-strategy) | 规划免费工具用于获客和 SEO |
| [competitor-alternatives](./competitor-alternatives) | 创建竞品对比页和替代方案页 |
| [sales-enablement](./sales-enablement) | 销售物料：pitch deck、话术、异议处理 |
| [baoyu-markdown-to-html](./baoyu-markdown-to-html) | Markdown 转微信公众号友好 HTML |
| [baoyu-post-to-wechat](./baoyu-post-to-wechat) | 发布文章/贴图到微信公众号（API 或 Chrome CDP） |

## SEO 与搜索

| 技能 | 说明 |
|------|------|
| [seo-audit](./seo-audit) | 技术 SEO 审计和诊断 |
| [ai-seo](./ai-seo) | 优化内容以出现在 AI 搜索结果中 |
| [programmatic-seo](./programmatic-seo) | 模板化批量生成 SEO 页面 |
| [schema-markup](./schema-markup) | 添加和优化结构化数据 |
| [site-architecture](./site-architecture) | 规划网站结构、导航和 URL |

## 转化与变现

从页面优化到定价策略的全链路转化。

| 技能 | 说明 |
|------|------|
| [page-cro](./page-cro) | 优化落地页和营销页面的转化率 |
| [signup-flow-cro](./signup-flow-cro) | 优化注册和账户创建流程 |
| [onboarding-cro](./onboarding-cro) | 优化注册后的用户激活和留存 |
| [form-cro](./form-cro) | 优化表单转化率（非注册类） |
| [popup-cro](./popup-cro) | 优化弹窗、模态框和覆盖层转化 |
| [paywall-upgrade-cro](./paywall-upgrade-cro) | 优化应用内付费墙和升级引导 |
| [ab-test-setup](./ab-test-setup) | 设计和实施 A/B 测试 |
| [analytics-tracking](./analytics-tracking) | 实施和调试分析追踪 |
| [pricing-strategy](./pricing-strategy) | 定价决策、套餐设计和变现策略 |
| [churn-prevention](./churn-prevention) | 流失防控、取消流程和挽留机制 |
| [referral-program](./referral-program) | 设计推荐计划和口碑增长 |
| [revops](./revops) | 收入运营、线索生命周期和市场-销售衔接 |

## 飞书 Lark

飞书开放平台全家桶：文档、表格、消息、日历、审批、知识库。

| 技能 | 说明 |
|------|------|
| [lark-base](./lark-base) | 飞书多维表格 — 建表、字段、记录、视图、公式、仪表盘、权限 |
| [lark-doc](./lark-doc) | 飞书云文档 — 读取、创建、编辑 Docx/Wiki 文档 |
| [lark-sheets](./lark-sheets) | 飞书电子表格 — 单元格读写、公式、图表、透视表、批量更新 |
| [lark-drive](./lark-drive) | 飞书云空间 — 上传下载、目录管理、格式导入 |
| [lark-wiki](./lark-wiki) | 飞书知识库 — 空间、节点、成员管理 |
| [lark-im](./lark-im) | 飞书即时通讯 — 收发消息、群管理、文件、加急 |
| [lark-mail](./lark-mail) | 飞书邮箱 — 邮件收发与管理 |
| [lark-calendar](./lark-calendar) | 飞书日历 — 日程、忙闲查询、会议室预定 |
| [lark-task](./lark-task) | 飞书任务 — 待办创建与管理 |
| [lark-contact](./lark-contact) | 飞书通讯录 — 姓名/邮箱与 open_id 互查 |
| [lark-approval](./lark-approval) | 飞书审批流程查询与操作 |
| [lark-attendance](./lark-attendance) | 飞书考勤 — 打卡记录与假勤管理 |
| [lark-okr](./lark-okr) | 飞书 OKR 查询与管理 |
| [lark-minutes](./lark-minutes) | 飞书妙记 — 会议纪要查询与导出 |
| [lark-note](./lark-note) | 飞书小记管理 |
| [lark-vc](./lark-vc) | 飞书视频会议 — 会议记录查询 |
| [lark-vc-agent](./lark-vc-agent) | 飞书视频会议 Agent 工作流 |
| [lark-whiteboard](./lark-whiteboard) | 飞书画板读取与操作 |
| [lark-slides](./lark-slides) | 飞书幻灯片创建与编辑 |
| [lark-markdown](./lark-markdown) | 飞书 Markdown 文件 — 查看、创建、编辑、patch、diff |
| [lark-event](./lark-event) | 飞书事件订阅管理 |
| [lark-apps](./lark-apps) | 妙搭（Miaoda/Spark）应用开发与托管 — HTML 发布、本地/云端全栈开发 |
| [lark-shared](./lark-shared) | lark-* skills 共享认证与工具库 |
| [lark-openapi-explorer](./lark-openapi-explorer) | 从官方文档挖掘未封装的飞书原生 OpenAPI |
| [lark-skill-maker](./lark-skill-maker) | 脚手架生成新的 lark-* skill |
| [lark-workflow-meeting-summary](./lark-workflow-meeting-summary) | 工作流：会议纪要自动生成 |
| [lark-workflow-standup-report](./lark-workflow-standup-report) | 工作流：站会日报自动生成 |
| [feishu-wiki](./feishu-wiki) | 本地 Markdown 推送到飞书知识库并转 Docs 格式 |

## 企业微信 WeCom

基于 wecom-cli 的企业微信操作。

| 技能 | 说明 |
|------|------|
| [wecomcli-get-msg](./wecomcli-get-msg) | 企微：读取消息 |
| [wecomcli-lookup-contact](./wecomcli-lookup-contact) | 企微：查找联系人 |
| [wecomcli-create-meeting](./wecomcli-create-meeting) | 企微：创建会议 |
| [wecomcli-edit-meeting](./wecomcli-edit-meeting) | 企微：修改会议 |
| [wecomcli-get-meeting](./wecomcli-get-meeting) | 企微：查询会议 |
| [wecomcli-get-todo-list](./wecomcli-get-todo-list) | 企微：待办列表 |
| [wecomcli-get-todo-detail](./wecomcli-get-todo-detail) | 企微：待办详情 |
| [wecomcli-edit-todo](./wecomcli-edit-todo) | 企微：编辑待办 |
| [wecomcli-manage-doc](./wecomcli-manage-doc) | 企微：文档管理 |
| [wecomcli-manage-schedule](./wecomcli-manage-schedule) | 企微：日程管理 |
| [wecomcli-manage-smartsheet-data](./wecomcli-manage-smartsheet-data) | 企微：智能表格数据操作 |
| [wecomcli-manage-smartsheet-schema](./wecomcli-manage-smartsheet-schema) | 企微：智能表格结构管理 |

## 业务工作流

特定业务场景的端到端流程。

| 技能 | 说明 |
|------|------|
| [insight-report](./insight-report) | uhomes 市场调研/渠道洞察报告全流程 — 问卷、分析、双语 HTML、水印 PDF |
| [interview-copilot](./interview-copilot) | 终面副驾 — 简历评估、定制问题、现场记录、录用决策与存档 |

---

## 安装

```bash
# 安装单个 skill
claude install-skill https://github.com/yalding8/skills/tree/main/<skill-name>

# 例：安装 TDD 技能
claude install-skill https://github.com/yalding8/skills/tree/main/tdd
```

## 同步

```bash
# 在 Claude Code 中运行
/sync-skills
```

同步脚本在推送前自动执行凭证扫描门禁，检出疑似密钥即中止。

## 维护记录

- [AUDIT_2026-07-02_SKILLS_INVENTORY](./docs/AUDIT_2026-07-02_SKILLS_INVENTORY.md)

---

<details>
<summary><h2 id="english-version">English Version</h2></summary>

A personal collection of agent skills for Claude Code, Cursor, and other AI coding tools.

> Auto-synced from `~/.claude/`.

### Planning & Design
| Skill | Description |
|-------|-------------|
| [write-a-prd](./write-a-prd) | Create a PRD through user interview and codebase exploration, submit as GitHub Issue |
| [prd-to-issues](./prd-to-issues) | Break a PRD into independently-grabbable GitHub Issues using tracer-bullet slices |
| [prd-to-plan](./prd-to-plan) | Turn a PRD into a multi-phase implementation plan saved as local Markdown |
| [grill-me](./grill-me) | Stress-test a plan or design through relentless questioning |
| [design-interface](./design-interface) | Generate multiple radically different interface designs using parallel agents |
| [ubiquitous-language](./ubiquitous-language) | Extract a DDD-style ubiquitous language glossary |

### Development
| Skill | Description |
|-------|-------------|
| [tdd](./tdd) | Test-driven development with red-green-refactor loop |
| [triage-issue](./triage-issue) | Explore codebase to find root cause, create GitHub Issue with TDD fix plan |
| [improve-architecture](./improve-architecture) | Find architectural improvements by deepening shallow modules |
| [request-refactor](./request-refactor) | Create a detailed refactor plan with tiny commits via user interview |
| [migrate-to-shoehorn](./migrate-to-shoehorn) | Migrate test files from `as` assertions to @total-typescript/shoehorn |
| [miniprogram-development](./miniprogram-development) | WeChat Mini Program development — build, debug, preview, publish, CloudBase |

### Tooling & Productivity
| Skill | Description |
|-------|-------------|
| [setup-pre-commit](./setup-pre-commit) | Set up Husky pre-commit hooks with lint-staged, type checking, and tests |
| [git-guardrails](./git-guardrails) | Set up Claude Code hooks to block dangerous git commands |
| [fix-format](./fix-format) | Format correction |
| [sync-skills](./sync-skills) | Sync all installed skills and commands to GitHub |
| [verify-blockers](./verify-blockers) | Verify blockers |
| [scaffold-exercises](./scaffold-exercises) | Create exercise directory structures with sections and solutions |
| [obsidian-vault](./obsidian-vault) | Search, create, and manage notes in Obsidian vault |
| [ljg-skill-map](./ljg-skill-map) | Scan installed skills and render ASCII visual overview |
| [ljg-x-download](./ljg-x-download) | Download images and videos from X/Twitter posts |
| [born-traceable](./born-traceable) | Make new projects and scheduled jobs traceable from birth — stamps, git triggers, dead-man switches |
| [update-readme](./update-readme) | Update README.md from recent code changes, keeping existing format |
| [publish-artifact](./publish-artifact) | Publish HTML, attachments, or directories to a private IPFS Cluster for immutable share links |
| [kubo-deploy-e2e](./kubo-deploy-e2e) | E2E test/demo for private IPFS Cluster (Kubo) deployment — 3-node docker-compose |
| [kubo-publish-e2e](./kubo-publish-e2e) | E2E test/demo for the agent publish pipeline to a private IPFS Cluster |

### Frontend Design — Impeccable
From [Impeccable](https://github.com/pbakaus/impeccable) — design vocabulary for AI-assisted frontend development.

| Skill | Description |
|-------|-------------|
| [frontend-design](./frontend-design) | Create distinctive, production-grade frontend interfaces |
| [teach-impeccable](./teach-impeccable) | One-time setup: gather design context for your project |
| [audit](./audit) | Comprehensive audit across accessibility, performance, and responsive design |
| [critique](./critique) | UX design review — hierarchy, clarity, emotional resonance |
| [polish](./polish) | Final quality pass — alignment, spacing, consistency |
| [typeset](./typeset) | Fix font choices, hierarchy, sizing, readability |
| [arrange](./arrange) | Fix layout, spacing, and visual rhythm |
| [colorize](./colorize) | Add strategic color to monochromatic interfaces |
| [animate](./animate) | Add purposeful animations and micro-interactions |
| [normalize](./normalize) | Align to design system standards |
| [distill](./distill) | Strip unnecessary complexity, extract essence |
| [clarify](./clarify) | Improve unclear UX copy and microcopy |
| [optimize](./optimize) | Performance optimization — loading, rendering, bundle size |
| [harden](./harden) | Error handling, i18n, edge cases |
| [bolder](./bolder) | Amplify visual impact of safe designs |
| [quieter](./quieter) | Tone down overly aggressive designs |
| [delight](./delight) | Add moments of joy and personality |
| [extract](./extract) | Extract reusable components and design tokens |
| [adapt](./adapt) | Adapt designs across devices and contexts |
| [onboard](./onboard) | Design onboarding flows and empty states |
| [overdrive](./overdrive) | Push past conventional limits with ambitious implementations |

### Frontend Engineering
| Skill | Description |
|-------|-------------|
| [mobile-design](./mobile-design) | Mobile UX patterns, touch interactions, gestures, mobile-first principles |
| [responsive-design](./responsive-design) | Mobile-first responsive design — fluid layouts, media queries, flexbox, grid |
| [web-perf](./web-perf) | Analyze web performance via Chrome DevTools MCP, measure Core Web Vitals |
| [platform-check](./platform-check) | Prevent AI from reimplementing platform-native capabilities — three gates before UI changes |

### Cloudflare Development
| Skill | Description |
|-------|-------------|
| [cloudflare](./cloudflare) | Cloudflare development overview — Workers, Pages, R2, KV, product selection |
| [wrangler](./wrangler) | Wrangler CLI for Cloudflare Workers configuration and deployment |
| [workers-best-practices](./workers-best-practices) | Cloudflare Workers best practices |
| [durable-objects](./durable-objects) | Durable Objects — stateful coordination, RPC, SQLite, alarms, WebSockets |
| [agents-sdk](./agents-sdk) | Build AI agents on Cloudflare Workers with the Agents SDK |
| [sandbox-sdk](./sandbox-sdk) | Sandbox SDK — secure sandboxed code execution, interpreters, CI/CD |
| [cloudflare-email-service](./cloudflare-email-service) | Send and receive transactional email with Cloudflare Email Service |

### Cognition & Writing
Thinking tools and writing engines. Partially from [ljg-skills](https://github.com/lijigang/ljg-skills).

| Skill | Description |
|-------|-------------|
| [ljg-learn](./ljg-learn) | Concept anatomy — 8-dimensional deconstruction + epiphany compression |
| [ljg-rank](./ljg-rank) | Rank reduction — find irreducible generators behind any domain |
| [ljg-roundtable](./ljg-roundtable) | Structured roundtable with real historical/contemporary figures |
| [ljg-invest](./ljg-invest) | Investment analysis — is the project an "order-creation machine"? |
| [ljg-writes](./ljg-writes) | Writing engine — start with a thesis, think it through by writing |
| [ljg-plain](./ljg-plain) | Plain language engine — rewrite so a smart 12-year-old gets it |
| [ljg-word](./ljg-word) | Deep English word mastery (etymology, core imagery, epiphany) |
| [write-a-skill](./write-a-skill) | Create a well-structured new agent skill |
| [edit-article](./edit-article) | Restructure paragraphs, improve clarity, tighten prose |

### Visual Casting
Cast content into shareable visual artifacts. From [ljg-skills](https://github.com/lijigang/ljg-skills).

| Skill | Description |
|-------|-------------|
| [ljg-card](./ljg-card) | Cast content into PNG visuals (6 molds: long/infograph/multi/sketch/comic/whiteboard) |
| [ljg-paper](./ljg-paper) | Paper reader — extract ideas for non-academics |
| [ljg-paper-flow](./ljg-paper-flow) | Paper workflow: read paper → cast card in one go |
| [ljg-word-flow](./ljg-word-flow) | Word flow: deep-dive analysis → infograph card in one go |
| [ljg-travel](./ljg-travel) | Deep travel research with org-mode docs + portable reference cards |
| [guizang-social-card-skill](./guizang-social-card-skill) | Guizang-style social card sets and WeChat official account cover pairs |
| [guizang-ppt-skill](./guizang-ppt-skill) | Guizang-style presentation deck generation |

### Marketing & Growth
| Skill | Description |
|-------|-------------|
| [product-marketing-context](./product-marketing-context) | Establish product positioning, audience, and messaging framework |
| [marketing-ideas](./marketing-ideas) | Brainstorm marketing strategies and growth ideas |
| [marketing-psychology](./marketing-psychology) | Apply psychological principles to marketing decisions |
| [copywriting](./copywriting) | Write or rewrite marketing copy for any page |
| [copy-editing](./copy-editing) | Edit and polish existing marketing copy |
| [content-strategy](./content-strategy) | Plan content strategy, topics, and publishing cadence |
| [social-content](./social-content) | Create and optimize social media content |
| [cold-email](./cold-email) | Write B2B cold emails and follow-up sequences |
| [email-sequence](./email-sequence) | Design automated email sequences and nurture flows |
| [paid-ads](./paid-ads) | Paid advertising strategy, targeting, and optimization |
| [ad-creative](./ad-creative) | Generate and iterate ad creative at scale |
| [launch-strategy](./launch-strategy) | Product launch and go-to-market strategy |
| [lead-magnets](./lead-magnets) | Design free resources for lead generation |
| [free-tool-strategy](./free-tool-strategy) | Plan free tools for lead gen and SEO value |
| [competitor-alternatives](./competitor-alternatives) | Create competitor comparison and alternative pages |
| [sales-enablement](./sales-enablement) | Sales collateral: pitch decks, talk tracks, objection handling |
| [baoyu-markdown-to-html](./baoyu-markdown-to-html) | Convert Markdown to WeChat-friendly HTML |
| [baoyu-post-to-wechat](./baoyu-post-to-wechat) | Post articles and image-text to WeChat Official Account (API or Chrome CDP) |

### SEO
| Skill | Description |
|-------|-------------|
| [seo-audit](./seo-audit) | Technical SEO audit and diagnosis |
| [ai-seo](./ai-seo) | Optimize content for AI search engines and LLM citations |
| [programmatic-seo](./programmatic-seo) | Generate SEO pages at scale using templates |
| [schema-markup](./schema-markup) | Add and optimize structured data markup |
| [site-architecture](./site-architecture) | Plan website structure, navigation, and URLs |

### Conversion & Revenue
| Skill | Description |
|-------|-------------|
| [page-cro](./page-cro) | Optimize landing page and marketing page conversions |
| [signup-flow-cro](./signup-flow-cro) | Optimize signup and account creation flows |
| [onboarding-cro](./onboarding-cro) | Optimize post-signup activation and retention |
| [form-cro](./form-cro) | Optimize form conversion rates (non-signup) |
| [popup-cro](./popup-cro) | Optimize popup, modal, and overlay conversions |
| [paywall-upgrade-cro](./paywall-upgrade-cro) | Optimize in-app paywalls and upgrade prompts |
| [ab-test-setup](./ab-test-setup) | Design and implement A/B tests |
| [analytics-tracking](./analytics-tracking) | Implement and debug analytics tracking |
| [pricing-strategy](./pricing-strategy) | Pricing decisions, packaging, and monetization |
| [churn-prevention](./churn-prevention) | Churn prevention, cancellation flows, and save offers |
| [referral-program](./referral-program) | Design referral programs and word-of-mouth growth |
| [revops](./revops) | Revenue operations, lead lifecycle, marketing-sales handoff |

### Feishu Lark
| Skill | Description |
|-------|-------------|
| [lark-base](./lark-base) | Feishu Base (bitable) — tables, fields, records, views, formulas, dashboards |
| [lark-doc](./lark-doc) | Feishu Docs — read, create, edit cloud documents |
| [lark-sheets](./lark-sheets) | Feishu Sheets — cells, formulas, charts, pivot tables, batch updates |
| [lark-drive](./lark-drive) | Feishu Drive — upload/download, folders, file import |
| [lark-wiki](./lark-wiki) | Feishu Wiki — spaces, nodes, member management |
| [lark-im](./lark-im) | Feishu IM — messages, groups, files, urgent pings |
| [lark-mail](./lark-mail) | Feishu Mail — send and manage email |
| [lark-calendar](./lark-calendar) | Feishu Calendar — events, free/busy, meeting rooms |
| [lark-task](./lark-task) | Feishu Tasks — create and manage todos |
| [lark-contact](./lark-contact) | Feishu contacts — resolve names/emails to open_id and back |
| [lark-approval](./lark-approval) | Feishu approval workflows |
| [lark-attendance](./lark-attendance) | Feishu attendance records and leave management |
| [lark-okr](./lark-okr) | Feishu OKR queries and management |
| [lark-minutes](./lark-minutes) | Feishu Minutes — meeting transcripts |
| [lark-note](./lark-note) | Feishu notes management |
| [lark-vc](./lark-vc) | Feishu video conferencing records |
| [lark-vc-agent](./lark-vc-agent) | Feishu VC agent workflows |
| [lark-whiteboard](./lark-whiteboard) | Feishu Whiteboard reading and operations |
| [lark-slides](./lark-slides) | Feishu Slides creation and editing |
| [lark-markdown](./lark-markdown) | Feishu Markdown files — view, create, edit, patch, diff |
| [lark-event](./lark-event) | Feishu event subscriptions |
| [lark-apps](./lark-apps) | Miaoda (Spark) app development and hosting — HTML publishing, local/cloud full-stack dev |
| [lark-shared](./lark-shared) | Shared auth and utilities for lark-* skills |
| [lark-openapi-explorer](./lark-openapi-explorer) | Explore native Feishu OpenAPIs beyond the CLI wrappers |
| [lark-skill-maker](./lark-skill-maker) | Scaffold new lark-* skills |
| [lark-workflow-meeting-summary](./lark-workflow-meeting-summary) | Workflow: automated meeting summaries |
| [lark-workflow-standup-report](./lark-workflow-standup-report) | Workflow: automated standup reports |
| [feishu-wiki](./feishu-wiki) | Push local Markdown to Feishu Wiki as native Docs |

### WeCom
| Skill | Description |
|-------|-------------|
| [wecomcli-get-msg](./wecomcli-get-msg) | WeCom: read messages |
| [wecomcli-lookup-contact](./wecomcli-lookup-contact) | WeCom: look up contacts |
| [wecomcli-create-meeting](./wecomcli-create-meeting) | WeCom: create meetings |
| [wecomcli-edit-meeting](./wecomcli-edit-meeting) | WeCom: edit meetings |
| [wecomcli-get-meeting](./wecomcli-get-meeting) | WeCom: get meeting info |
| [wecomcli-get-todo-list](./wecomcli-get-todo-list) | WeCom: list todos |
| [wecomcli-get-todo-detail](./wecomcli-get-todo-detail) | WeCom: todo details |
| [wecomcli-edit-todo](./wecomcli-edit-todo) | WeCom: edit todos |
| [wecomcli-manage-doc](./wecomcli-manage-doc) | WeCom: manage docs |
| [wecomcli-manage-schedule](./wecomcli-manage-schedule) | WeCom: manage schedules |
| [wecomcli-manage-smartsheet-data](./wecomcli-manage-smartsheet-data) | WeCom: smartsheet data operations |
| [wecomcli-manage-smartsheet-schema](./wecomcli-manage-smartsheet-schema) | WeCom: smartsheet schema management |

### Business Workflows
| Skill | Description |
|-------|-------------|
| [insight-report](./insight-report) | End-to-end uhomes market-research insight reports with watermarked PDF export |
| [interview-copilot](./interview-copilot) | Final-round interview copilot — resume evaluation, custom questions, hire decisions |

### Install
```bash
claude install-skill https://github.com/yalding8/skills/tree/main/<skill-name>
```

</details>

---

> 通过 [sync-skills.sh](https://github.com/yalding8/skills) 从 `~/.claude/` 自动同步。
