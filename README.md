# Agent Skills

个人 AI 技能合集，适用于 Claude Code、Cursor 等 AI 编码助手。88 个技能，9 大分类。

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

---

<details>
<summary><h2 id="english-version">English Version</h2></summary>

A personal collection of 88 agent skills for Claude Code, Cursor, and other AI coding tools.

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

### Install
```bash
claude install-skill https://github.com/yalding8/skills/tree/main/<skill-name>
```

</details>

---

> 通过 [sync-skills.sh](https://github.com/yalding8/skills) 从 `~/.claude/` 自动同步。
