# Agent Skills

个人 AI 编码工具 Skill 合集，适用于 Claude Code、Cursor 等 AI 编码助手。

> 从 `~/.claude/` 自动同步。[English version below.](#english-version)

---

## 规划与设计

在写代码之前理清思路。

| 技能 | 说明 |
|------|------|
| **write-a-prd** | 通过用户访谈 + 代码探索创建 PRD，提交为 GitHub Issue |
| **prd-to-issues** | 将 PRD 拆分为可独立认领的 GitHub Issue（tracer-bullet 纵切） |
| **prd-to-plan** | 将 PRD 转化为多阶段实施计划，保存为本地 Markdown |
| **grill-me** | 对方案/设计进行追问式压力测试，逐一解决决策树分支 |
| **design-interface** | 并行生成多个截然不同的模块接口设计方案 |
| **ubiquitous-language** | 提取 DDD 风格的统一语言词汇表 |

## 开发

编写、重构和修复代码。

| 技能 | 说明 |
|------|------|
| **tdd** | 红-绿-重构循环的测试驱动开发 |
| **triage-issue** | 探索代码定位根因，创建含 TDD 修复方案的 GitHub Issue |
| **improve-architecture** | 发现架构改进机会，通过深化浅模块提升可测试性 |
| **request-refactor** | 通过用户访谈创建小步提交的重构方案，提交为 GitHub Issue |
| **migrate-to-shoehorn** | 将测试文件的 as 类型断言迁移为 @total-typescript/shoehorn |

## 工具与配置

| 技能 | 说明 |
|------|------|
| **setup-pre-commit** | 配置 Husky pre-commit hooks + lint-staged + 类型检查 + 测试 |
| **git-guardrails** | 设置 Claude Code hooks 拦截危险 git 命令 |
| **fix-format** | 格式修正 |
| **sync-skills** | 将已安装的 skills 同步到 GitHub 仓库 |
| **verify-blockers** | 验证阻塞项 |
| **scaffold-exercises** | 创建练习目录结构 |

## 写作与知识

| 技能 | 说明 |
|------|------|
| **write-a-skill** | 创建结构完整的新 agent skill |
| **edit-article** | 重组段落、提升清晰度、精简文字 |
| **obsidian-vault** | 搜索、创建和管理 Obsidian 笔记 |

## 前端设计 — Impeccable

来自 [Impeccable](https://github.com/pbakaus/impeccable) — AI 辅助前端开发的设计词汇与反模式库。

| 技能 | 说明 |
|------|------|
| **frontend-design** | 综合设计技能，生成高品质、有特色的前端界面 |
| **teach-impeccable** | 首次设置：采集项目设计上下文并持久化 |
| **audit** | 技术质量检查 — 无障碍、性能、响应式 |
| **critique** | UX 设计评审 — 层级、清晰度、情感共鸣 |
| **polish** | 上线前最终打磨 — 对齐、间距、一致性 |
| **typeset** | 修复字体选择、层级、尺寸、可读性 |
| **arrange** | 修复布局、间距、视觉节奏 |
| **colorize** | 为单色界面添加战略性色彩 |
| **animate** | 添加有意义的动效和微交互 |
| **normalize** | 对齐设计系统标准 |
| **distill** | 去除不必要的复杂性，提炼精华 |
| **clarify** | 改善不清晰的 UX 文案和微文案 |
| **optimize** | 性能优化 — 加载、渲染、包体积 |
| **harden** | 错误处理、国际化、边界情况 |
| **bolder** | 放大平淡设计的视觉冲击力 |
| **quieter** | 降低过于激进的设计 |
| **delight** | 添加愉悦感和个性化触点 |
| **extract** | 提取为可复用组件和设计 token |
| **adapt** | 适配不同设备和场景 |
| **onboard** | 设计引导流程和空状态 |
| **overdrive** | 突破常规限制的技术炫技效果 |

## 营销与增长

策略、内容和渠道执行。

| 技能 | 说明 |
|------|------|
| **product-marketing-context** | 建立产品定位、受众和消息框架基础文档 |
| **marketing-ideas** | 头脑风暴营销策略和增长点子 |
| **marketing-psychology** | 将心理学原理应用于营销决策 |
| **copywriting** | 撰写或重写网站营销文案 |
| **copy-editing** | 编辑和润色现有营销文案 |
| **content-strategy** | 规划内容策略、选题和发布节奏 |
| **social-content** | 创建和优化社交媒体内容 |
| **cold-email** | 撰写 B2B 冷邮件和跟进序列 |
| **email-sequence** | 设计自动化邮件序列和培育流程 |
| **paid-ads** | 付费广告策略、投放和优化 |
| **ad-creative** | 批量生成和迭代广告创意素材 |
| **launch-strategy** | 产品发布和上市策略 |
| **lead-magnets** | 设计吸引潜客的免费资源 |
| **free-tool-strategy** | 规划免费工具用于获客和 SEO |
| **competitor-alternatives** | 创建竞品对比页和替代方案页 |
| **sales-enablement** | 销售物料：pitch deck、话术、异议处理 |

## SEO

| 技能 | 说明 |
|------|------|
| **seo-audit** | 技术 SEO 审计和诊断 |
| **ai-seo** | 优化内容以出现在 AI 搜索结果中 |
| **programmatic-seo** | 模板化批量生成 SEO 页面 |
| **schema-markup** | 添加和优化结构化数据 |
| **site-architecture** | 规划网站结构、导航和 URL |

## 转化优化 (CRO)

| 技能 | 说明 |
|------|------|
| **page-cro** | 优化落地页和营销页面的转化率 |
| **signup-flow-cro** | 优化注册和账户创建流程 |
| **onboarding-cro** | 优化注册后的用户激活和留存 |
| **form-cro** | 优化表单转化率（非注册类） |
| **popup-cro** | 优化弹窗、模态框和覆盖层转化 |
| **paywall-upgrade-cro** | 优化应用内付费墙和升级引导 |
| **ab-test-setup** | 设计和实施 A/B 测试 |
| **analytics-tracking** | 实施和调试分析追踪 |

## 收入运营

| 技能 | 说明 |
|------|------|
| **pricing-strategy** | 定价决策、套餐设计和变现策略 |
| **churn-prevention** | 流失防控、取消流程和挽留机制 |
| **referral-program** | 设计推荐计划和口碑增长 |
| **revops** | 收入运营、线索生命周期和市场-销售衔接 |

## 认知与创作 — LJG

来自 [ljg-skills](https://github.com/lijigang/ljg-skills) — 认知原子、视觉铸造和工作流串联。

| 技能 | 说明 |
|------|------|
| **ljg-card** | 内容铸 PNG 卡片（长图/信息图/多卡/视觉笔记/漫画/白板） |
| **ljg-invest** | 投资分析报告 — 判断项目是否是「秩序创造机器」 |
| **ljg-learn** | 概念解剖 — 八维切割 + 顿悟压缩，输出 org-mode |
| **ljg-paper** | 论文阅读器 — 为非学术人士提取论文思想 |
| **ljg-paper-flow** | 论文流 — 读论文 → 铸卡片一气呵成 |
| **ljg-plain** | 白话引擎 — 改写到 12 岁聪明小孩也能懂 |
| **ljg-rank** | 降秩引擎 — 找出领域背后不可再少的独立生成器 |
| **ljg-roundtable** | 圆桌讨论 — 真实人物多轮辩证对话 |
| **ljg-skill-map** | 技能地图 — 扫描已安装技能渲染 ASCII 总览 |
| **ljg-travel** | 旅行研究 — 城市文化 DBA + 便携参考卡片 |
| **ljg-word** | 英语单词深度拆解（词源、核心意象、金句） |
| **ljg-word-flow** | 词卡流 — 解词 → 铸信息图一气呵成 |
| **ljg-writes** | 写作引擎 — 带观点出发，写的过程中想透 |
| **ljg-x-download** | X/Twitter 媒体下载到本地 |

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

# Agent Skills

A personal collection of agent skills for Claude Code, Cursor, and other AI coding tools.

> Auto-synced from `~/.claude/`.

### Planning & Design
| Skill | Description |
|-------|-------------|
| **write-a-prd** | Create a PRD through user interview, codebase exploration, and module design, then submit as a GitHub issue. Use when user wants to write a PRD, create a product requirements document, or plan a new feature. |
| **prd-to-issues** | Break a PRD into independently-grabbable GitHub issues using tracer-bullet vertical slices. Use when user wants to convert a PRD to issues, create implementation tickets, or break down a PRD into work items. |
| **prd-to-plan** | Turn a PRD into a multi-phase implementation plan using tracer-bullet vertical slices, saved as a local Markdown file in ./plans/. Use when user wants to break down a PRD, create an implementation plan, plan phases from a PRD, or mentions "tracer bullets". |
| **grill-me** | Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me". |
| **design-interface** | Generate multiple radically different interface designs for a module using parallel sub-agents. Use when user wants to design an API, explore interface options, compare module shapes, or mentions "design it twice". |
| **ubiquitous-language** | Extract a DDD-style ubiquitous language glossary from the current conversation, flagging ambiguities and proposing canonical terms. Saves to UBIQUITOUS_LANGUAGE.md. Use when user wants to define domain terms, build a glossary, harden terminology, create a ubiquitous language, or mentions "domain model" or "DDD". |

### Development
| Skill | Description |
|-------|-------------|
| **tdd** | Test-driven development with red-green-refactor loop. Use when user wants to build features or fix bugs using TDD, mentions "red-green-refactor", wants integration tests, or asks for test-first development. |
| **triage-issue** | Triage a bug or issue by exploring the codebase to find root cause, then create a GitHub issue with a TDD-based fix plan. Use when user reports a bug, wants to file an issue, mentions "triage", or wants to investigate and plan a fix for a problem. |
| **improve-architecture** | Explore a codebase to find opportunities for architectural improvement, focusing on making the codebase more testable by deepening shallow modules. Use when user wants to improve architecture, find refactoring opportunities, consolidate tightly-coupled modules, or make a codebase more AI-navigable. |
| **request-refactor** | Create a detailed refactor plan with tiny commits via user interview, then file it as a GitHub issue. Use when user wants to plan a refactor, create a refactoring RFC, or break a refactor into safe incremental steps. |
| **migrate-to-shoehorn** | Migrate test files from `as` type assertions to @total-typescript/shoehorn. Use when user mentions shoehorn, wants to replace `as` in tests, or needs partial test data. |

### Tooling & Setup
| Skill | Description |
|-------|-------------|
| **setup-pre-commit** | Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current repo. Use when user wants to add pre-commit hooks, set up Husky, configure lint-staged, or add commit-time formatting/typechecking/testing. |
| **git-guardrails** | Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use when user wants to prevent destructive git operations, add git safety hooks, or block git push/reset in Claude Code. |
| **fix-format** |  |
| **sync-skills** | Sync all installed skills and commands to GitHub repo yalding8/skills. Run after installing new skills. |
| **verify-blockers** |  |
| **scaffold-exercises** | Create exercise directory structures with sections, problems, solutions, and explainers that pass linting. Use when user wants to scaffold exercises, create exercise stubs, or set up a new course section. |

### Writing & Knowledge
| Skill | Description |
|-------|-------------|
| **write-a-skill** | Create new agent skills with proper structure, progressive disclosure, and bundled resources. Use when user wants to create, write, or build a new skill. |
| **edit-article** | Edit and improve articles by restructuring sections, improving clarity, and tightening prose. Use when user wants to edit, revise, or improve an article draft. |
| **obsidian-vault** | Search, create, and manage notes in the Obsidian vault with wikilinks and index notes. Use when user wants to find, create, or organize notes in Obsidian. |

### Frontend Design — Impeccable
From [Impeccable](https://github.com/pbakaus/impeccable) — design vocabulary for AI-assisted frontend development.

| Skill | Description |
|-------|-------------|
| **frontend-design** | Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications. Generates creative, polished code that avoids generic AI aesthetics. |
| **teach-impeccable** | One-time setup that gathers design context for your project and saves it to your AI config file. Run once to establish persistent design guidelines. |
| **audit** | Perform comprehensive audit of interface quality across accessibility, performance, theming, and responsive design. Generates detailed report of issues with severity ratings and recommendations. |
| **critique** | Evaluate design effectiveness from a UX perspective. Assesses visual hierarchy, information architecture, emotional resonance, and overall design quality with actionable feedback. |
| **polish** | Final quality pass before shipping. Fixes alignment, spacing, consistency, and detail issues that separate good from great. |
| **typeset** | Improve typography by fixing font choices, hierarchy, sizing, weight consistency, and readability. Makes text feel intentional and polished. |
| **arrange** | Improve layout, spacing, and visual rhythm. Fixes monotonous grids, inconsistent spacing, and weak visual hierarchy to create intentional compositions. |
| **colorize** | Add strategic color to features that are too monochromatic or lack visual interest. Makes interfaces more engaging and expressive. |
| **animate** | Review a feature and enhance it with purposeful animations, micro-interactions, and motion effects that improve usability and delight. |
| **normalize** | Normalize design to match your design system and ensure consistency |
| **distill** | Strip designs to their essence by removing unnecessary complexity. Great design is simple, powerful, and clean. |
| **clarify** | Improve unclear UX copy, error messages, microcopy, labels, and instructions. Makes interfaces easier to understand and use. |
| **optimize** | Improve interface performance across loading speed, rendering, animations, images, and bundle size. Makes experiences faster and smoother. |
| **harden** | Improve interface resilience through better error handling, i18n support, text overflow handling, and edge case management. Makes interfaces robust and production-ready. |
| **bolder** | Amplify safe or boring designs to make them more visually interesting and stimulating. Increases impact while maintaining usability. |
| **quieter** | Tone down overly bold or visually aggressive designs. Reduces intensity while maintaining design quality and impact. |
| **delight** | Add moments of joy, personality, and unexpected touches that make interfaces memorable and enjoyable to use. Elevates functional to delightful. |
| **extract** | Extract and consolidate reusable components, design tokens, and patterns into your design system. Identifies opportunities for systematic reuse and enriches your component library. |
| **adapt** | Adapt designs to work across different screen sizes, devices, contexts, or platforms. Ensures consistent experience across varied environments. |
| **onboard** | Design or improve onboarding flows, empty states, and first-time user experiences. Helps users get started successfully and understand value quickly. |
| **overdrive** | Push interfaces past conventional limits with technically ambitious implementations. Whether that's a shader, a 60fps virtual table, spring physics on a dialog, or scroll-driven reveals — make users ask "how did they do that?" |

### Marketing & Growth
| Skill | Description |
|-------|-------------|
| **product-marketing-context** | "When the user wants to create or update their product marketing context document. Also use when the user mentions 'product context,' 'marketing context,' 'set up context,' 'positioning,' 'who is my target audience,' 'describe my product,' 'ICP,' 'ideal customer profile,' or wants to avoid repeating foundational information across marketing tasks. Use this at the start of any new project before using other marketing skills — it creates `.agents/product-marketing-context.md` that all other skills reference for product, audience, and positioning context." |
| **marketing-ideas** | "When the user needs marketing ideas, inspiration, or strategies for their SaaS or software product. Also use when the user asks for 'marketing ideas,' 'growth ideas,' 'how to market,' 'marketing strategies,' 'marketing tactics,' 'ways to promote,' 'ideas to grow,' 'what else can I try,' 'I don't know how to market this,' 'brainstorm marketing,' or 'what marketing should I do.' Use this as a starting point whenever someone is stuck or looking for inspiration on how to grow. For specific channel execution, see the relevant skill (paid-ads, social-content, email-sequence, etc.)." |
| **marketing-psychology** | "When the user wants to apply psychological principles, mental models, or behavioral science to marketing. Also use when the user mentions 'psychology,' 'mental models,' 'cognitive bias,' 'persuasion,' 'behavioral science,' 'why people buy,' 'decision-making,' 'consumer behavior,' 'anchoring,' 'social proof,' 'scarcity,' 'loss aversion,' 'framing,' or 'nudge.' Use this whenever someone wants to understand or leverage how people think and make decisions in a marketing context." |
| **copywriting** | When the user wants to write, rewrite, or improve marketing copy for any page — including homepage, landing pages, pricing pages, feature pages, about pages, or product pages. Also use when the user says "write copy for," "improve this copy," "rewrite this page," "marketing copy," "headline help," "CTA copy," "value proposition," "tagline," "subheadline," "hero section copy," "above the fold," "this copy is weak," "make this more compelling," or "help me describe my product." Use this whenever someone is working on website text that needs to persuade or convert. For email copy, see email-sequence. For popup copy, see popup-cro. For editing existing copy, see copy-editing. |
| **copy-editing** | "When the user wants to edit, review, or improve existing marketing copy. Also use when the user mentions 'edit this copy,' 'review my copy,' 'copy feedback,' 'proofread,' 'polish this,' 'make this better,' 'copy sweep,' 'tighten this up,' 'this reads awkwardly,' 'clean up this text,' 'too wordy,' or 'sharpen the messaging.' Use this when the user already has copy and wants it improved rather than rewritten from scratch. For writing new copy, see copywriting." |
| **content-strategy** | When the user wants to plan a content strategy, decide what content to create, or figure out what topics to cover. Also use when the user mentions "content strategy," "what should I write about," "content ideas," "blog strategy," "topic clusters," "content planning," "editorial calendar," "content marketing," "content roadmap," "what content should I create," "blog topics," "content pillars," or "I don't know what to write." Use this whenever someone needs help deciding what content to produce, not just writing it. For writing individual pieces, see copywriting. For SEO-specific audits, see seo-audit. For social media content specifically, see social-content. |
| **social-content** | "When the user wants help creating, scheduling, or optimizing social media content for LinkedIn, Twitter/X, Instagram, TikTok, Facebook, or other platforms. Also use when the user mentions 'LinkedIn post,' 'Twitter thread,' 'social media,' 'content calendar,' 'social scheduling,' 'engagement,' 'viral content,' 'what should I post,' 'repurpose this content,' 'tweet ideas,' 'LinkedIn carousel,' 'social media strategy,' or 'grow my following.' Use this for any social media content creation, repurposing, or scheduling task. For broader content strategy, see content-strategy." |
| **cold-email** | Write B2B cold emails and follow-up sequences that get replies. Use when the user wants to write cold outreach emails, prospecting emails, cold email campaigns, sales development emails, or SDR emails. Also use when the user mentions "cold outreach," "prospecting email," "outbound email," "email to leads," "reach out to prospects," "sales email," "follow-up email sequence," "nobody's replying to my emails," or "how do I write a cold email." Covers subject lines, opening lines, body copy, CTAs, personalization, and multi-touch follow-up sequences. For warm/lifecycle email sequences, see email-sequence. For sales collateral beyond emails, see sales-enablement. |
| **email-sequence** | When the user wants to create or optimize an email sequence, drip campaign, automated email flow, or lifecycle email program. Also use when the user mentions "email sequence," "drip campaign," "nurture sequence," "onboarding emails," "welcome sequence," "re-engagement emails," "email automation," "lifecycle emails," "trigger-based emails," "email funnel," "email workflow," "what emails should I send," "welcome series," or "email cadence." Use this for any multi-email automated flow. For cold outreach emails, see cold-email. For in-app onboarding, see onboarding-cro. |
| **paid-ads** | "When the user wants help with paid advertising campaigns on Google Ads, Meta (Facebook/Instagram), LinkedIn, Twitter/X, or other ad platforms. Also use when the user mentions 'PPC,' 'paid media,' 'ROAS,' 'CPA,' 'ad campaign,' 'retargeting,' 'audience targeting,' 'Google Ads,' 'Facebook ads,' 'LinkedIn ads,' 'ad budget,' 'cost per click,' 'ad spend,' or 'should I run ads.' Use this for campaign strategy, audience targeting, bidding, and optimization. For bulk ad creative generation and iteration, see ad-creative. For landing page optimization, see page-cro." |
| **ad-creative** | "When the user wants to generate, iterate, or scale ad creative — headlines, descriptions, primary text, or full ad variations — for any paid advertising platform. Also use when the user mentions 'ad copy variations,' 'ad creative,' 'generate headlines,' 'RSA headlines,' 'bulk ad copy,' 'ad iterations,' 'creative testing,' 'ad performance optimization,' 'write me some ads,' 'Facebook ad copy,' 'Google ad headlines,' 'LinkedIn ad text,' or 'I need more ad variations.' Use this whenever someone needs to produce ad copy at scale or iterate on existing ads. For campaign strategy and targeting, see paid-ads. For landing page copy, see copywriting." |
| **launch-strategy** | "When the user wants to plan a product launch, feature announcement, or release strategy. Also use when the user mentions 'launch,' 'Product Hunt,' 'feature release,' 'announcement,' 'go-to-market,' 'beta launch,' 'early access,' 'waitlist,' 'product update,' 'how do I launch this,' 'launch checklist,' 'GTM plan,' or 'we're about to ship.' Use this whenever someone is preparing to release something publicly. For ongoing marketing after launch, see marketing-ideas." |
| **lead-magnets** | When the user wants to create, plan, or optimize a lead magnet for email capture or lead generation. Also use when the user mentions "lead magnet," "gated content," "content upgrade," "downloadable," "ebook," "cheat sheet," "checklist," "template download," "opt-in," "freebie," "PDF download," "resource library," "content offer," "email capture content," "Notion template," "spreadsheet template," or "what should I give away for emails." Use this for planning what to create and how to distribute it. For interactive tools as lead magnets, see free-tool-strategy. For writing the actual content, see copywriting. For the email sequence after capture, see email-sequence. |
| **free-tool-strategy** | When the user wants to plan, evaluate, or build a free tool for marketing purposes — lead generation, SEO value, or brand awareness. Also use when the user mentions "engineering as marketing," "free tool," "marketing tool," "calculator," "generator," "interactive tool," "lead gen tool," "build a tool for leads," "free resource," "ROI calculator," "grader tool," "audit tool," "should I build a free tool," or "tools for lead gen." Use this whenever someone wants to build something useful and give it away to attract leads or earn links. For downloadable content lead magnets (ebooks, checklists, templates), see lead-magnets. |
| **competitor-alternatives** | "When the user wants to create competitor comparison or alternative pages for SEO and sales enablement. Also use when the user mentions 'alternative page,' 'vs page,' 'competitor comparison,' 'comparison page,' '[Product] vs [Product],' '[Product] alternative,' 'competitive landing pages,' 'how do we compare to X,' 'battle card,' or 'competitor teardown.' Use this for any content that positions your product against competitors. Covers four formats: singular alternative, plural alternatives, you vs competitor, and competitor vs competitor. For sales-specific competitor docs, see sales-enablement." |
| **sales-enablement** | "When the user wants to create sales collateral, pitch decks, one-pagers, objection handling docs, or demo scripts. Also use when the user mentions 'sales deck,' 'pitch deck,' 'one-pager,' 'leave-behind,' 'objection handling,' 'deal-specific ROI analysis,' 'demo script,' 'talk track,' 'sales playbook,' 'proposal template,' 'buyer persona card,' 'help my sales team,' 'sales materials,' or 'what should I give my sales reps.' Use this for any document or asset that helps a sales team close deals. For competitor comparison pages and battle cards, see competitor-alternatives. For marketing website copy, see copywriting. For cold outreach emails, see cold-email." |

### SEO
| Skill | Description |
|-------|-------------|
| **seo-audit** | When the user wants to audit, review, or diagnose SEO issues on their site. Also use when the user mentions "SEO audit," "technical SEO," "why am I not ranking," "SEO issues," "on-page SEO," "meta tags review," "SEO health check," "my traffic dropped," "lost rankings," "not showing up in Google," "site isn't ranking," "Google update hit me," "page speed," "core web vitals," "crawl errors," or "indexing issues." Use this even if the user just says something vague like "my SEO is bad" or "help with SEO" — start with an audit. For building pages at scale to target keywords, see programmatic-seo. For adding structured data, see schema-markup. For AI search optimization, see ai-seo. |
| **ai-seo** | "When the user wants to optimize content for AI search engines, get cited by LLMs, or appear in AI-generated answers. Also use when the user mentions 'AI SEO,' 'AEO,' 'GEO,' 'LLMO,' 'answer engine optimization,' 'generative engine optimization,' 'LLM optimization,' 'AI Overviews,' 'optimize for ChatGPT,' 'optimize for Perplexity,' 'AI citations,' 'AI visibility,' 'zero-click search,' 'how do I show up in AI answers,' 'LLM mentions,' or 'optimize for Claude/Gemini.' Use this whenever someone wants their content to be cited or surfaced by AI assistants and AI search engines. For traditional technical and on-page SEO audits, see seo-audit. For structured data implementation, see schema-markup." |
| **programmatic-seo** | When the user wants to create SEO-driven pages at scale using templates and data. Also use when the user mentions "programmatic SEO," "template pages," "pages at scale," "directory pages," "location pages," "[keyword] + [city] pages," "comparison pages," "integration pages," "building many pages for SEO," "pSEO," "generate 100 pages," "data-driven pages," or "templated landing pages." Use this whenever someone wants to create many similar pages targeting different keywords or locations. For auditing existing SEO issues, see seo-audit. For content strategy planning, see content-strategy. |
| **schema-markup** | When the user wants to add, fix, or optimize schema markup and structured data on their site. Also use when the user mentions "schema markup," "structured data," "JSON-LD," "rich snippets," "schema.org," "FAQ schema," "product schema," "review schema," "breadcrumb schema," "Google rich results," "knowledge panel," "star ratings in search," or "add structured data." Use this whenever someone wants their pages to show enhanced results in Google. For broader SEO issues, see seo-audit. For AI search optimization, see ai-seo. |
| **site-architecture** | When the user wants to plan, map, or restructure their website's page hierarchy, navigation, URL structure, or internal linking. Also use when the user mentions "sitemap," "site map," "visual sitemap," "site structure," "page hierarchy," "information architecture," "IA," "navigation design," "URL structure," "breadcrumbs," "internal linking strategy," "website planning," "what pages do I need," "how should I organize my site," or "site navigation." Use this whenever someone is planning what pages a website should have and how they connect. NOT for XML sitemaps (that's technical SEO — see seo-audit). For SEO audits, see seo-audit. For structured data, see schema-markup. |

### Conversion Optimization (CRO)
| Skill | Description |
|-------|-------------|
| **page-cro** | When the user wants to optimize, improve, or increase conversions on any marketing page — including homepage, landing pages, pricing pages, feature pages, or blog posts. Also use when the user says "CRO," "conversion rate optimization," "this page isn't converting," "improve conversions," "why isn't this page working," "my landing page sucks," "nobody's converting," "low conversion rate," "bounce rate is too high," "people leave without signing up," or "this page needs work." Use this even if the user just shares a URL and asks for feedback — they probably want conversion help. For signup/registration flows, see signup-flow-cro. For post-signup activation, see onboarding-cro. For forms outside of signup, see form-cro. For popups/modals, see popup-cro. |
| **signup-flow-cro** | When the user wants to optimize signup, registration, account creation, or trial activation flows. Also use when the user mentions "signup conversions," "registration friction," "signup form optimization," "free trial signup," "reduce signup dropoff," "account creation flow," "people aren't signing up," "signup abandonment," "trial conversion rate," "nobody completes registration," "too many steps to sign up," or "simplify our signup." Use this whenever the user has a signup or registration flow that isn't performing. For post-signup onboarding, see onboarding-cro. For lead capture forms (not account creation), see form-cro. |
| **onboarding-cro** | When the user wants to optimize post-signup onboarding, user activation, first-run experience, or time-to-value. Also use when the user mentions "onboarding flow," "activation rate," "user activation," "first-run experience," "empty states," "onboarding checklist," "aha moment," "new user experience," "users aren't activating," "nobody completes setup," "low activation rate," "users sign up but don't use the product," "time to value," or "first session experience." Use this whenever users are signing up but not sticking around. For signup/registration optimization, see signup-flow-cro. For ongoing email sequences, see email-sequence. |
| **form-cro** | When the user wants to optimize any form that is NOT signup/registration — including lead capture forms, contact forms, demo request forms, application forms, survey forms, or checkout forms. Also use when the user mentions "form optimization," "lead form conversions," "form friction," "form fields," "form completion rate," "contact form," "nobody fills out our form," "form abandonment," "too many fields," "demo request form," or "lead form isn't converting." Use this for any non-signup form that captures information. For signup/registration forms, see signup-flow-cro. For popups containing forms, see popup-cro. |
| **popup-cro** | When the user wants to create or optimize popups, modals, overlays, slide-ins, or banners for conversion purposes. Also use when the user mentions "exit intent," "popup conversions," "modal optimization," "lead capture popup," "email popup," "announcement banner," "overlay," "collect emails with a popup," "exit popup," "scroll trigger," "sticky bar," or "notification bar." Use this for any overlay or interrupt-style conversion element. For forms outside of popups, see form-cro. For general page conversion optimization, see page-cro. |
| **paywall-upgrade-cro** | When the user wants to create or optimize in-app paywalls, upgrade screens, upsell modals, or feature gates. Also use when the user mentions "paywall," "upgrade screen," "upgrade modal," "upsell," "feature gate," "convert free to paid," "freemium conversion," "trial expiration screen," "limit reached screen," "plan upgrade prompt," "in-app pricing," "free users won't upgrade," "trial to paid conversion," or "how do I get users to pay." Use this for any in-product moment where you're asking users to upgrade. Distinct from public pricing pages (see page-cro) — this focuses on in-product upgrade moments where the user has already experienced value. For pricing decisions, see pricing-strategy. |
| **ab-test-setup** | When the user wants to plan, design, or implement an A/B test or experiment. Also use when the user mentions "A/B test," "split test," "experiment," "test this change," "variant copy," "multivariate test," "hypothesis," "should I test this," "which version is better," "test two versions," "statistical significance," or "how long should I run this test." Use this whenever someone is comparing two approaches and wants to measure which performs better. For tracking implementation, see analytics-tracking. For page-level conversion optimization, see page-cro. |
| **analytics-tracking** | When the user wants to set up, improve, or audit analytics tracking and measurement. Also use when the user mentions "set up tracking," "GA4," "Google Analytics," "conversion tracking," "event tracking," "UTM parameters," "tag manager," "GTM," "analytics implementation," "tracking plan," "how do I measure this," "track conversions," "attribution," "Mixpanel," "Segment," "are my events firing," or "analytics isn't working." Use this whenever someone asks how to know if something is working or wants to measure marketing results. For A/B test measurement, see ab-test-setup. |

### Revenue Operations
| Skill | Description |
|-------|-------------|
| **pricing-strategy** | "When the user wants help with pricing decisions, packaging, or monetization strategy. Also use when the user mentions 'pricing,' 'pricing tiers,' 'freemium,' 'free trial,' 'packaging,' 'price increase,' 'value metric,' 'Van Westendorp,' 'willingness to pay,' 'monetization,' 'how much should I charge,' 'my pricing is wrong,' 'pricing page,' 'annual vs monthly,' 'per seat pricing,' or 'should I offer a free plan.' Use this whenever someone is figuring out what to charge or how to structure their plans. For in-app upgrade screens, see paywall-upgrade-cro." |
| **churn-prevention** | "When the user wants to reduce churn, build cancellation flows, set up save offers, recover failed payments, or implement retention strategies. Also use when the user mentions 'churn,' 'cancel flow,' 'offboarding,' 'save offer,' 'dunning,' 'failed payment recovery,' 'win-back,' 'retention,' 'exit survey,' 'pause subscription,' 'involuntary churn,' 'people keep canceling,' 'churn rate is too high,' 'how do I keep users,' or 'customers are leaving.' Use this whenever someone is losing subscribers or wants to build systems to prevent it. For post-cancel win-back email sequences, see email-sequence. For in-app upgrade paywalls, see paywall-upgrade-cro." |
| **referral-program** | "When the user wants to create, optimize, or analyze a referral program, affiliate program, or word-of-mouth strategy. Also use when the user mentions 'referral,' 'affiliate,' 'ambassador,' 'word of mouth,' 'viral loop,' 'refer a friend,' 'partner program,' 'referral incentive,' 'how to get referrals,' 'customers referring customers,' or 'affiliate payout.' Use this whenever someone wants existing users or partners to bring in new customers. For launch-specific virality, see launch-strategy." |
| **revops** | "When the user wants help with revenue operations, lead lifecycle management, or marketing-to-sales handoff processes. Also use when the user mentions 'RevOps,' 'revenue operations,' 'lead scoring,' 'lead routing,' 'MQL,' 'SQL,' 'pipeline stages,' 'deal desk,' 'CRM automation,' 'marketing-to-sales handoff,' 'data hygiene,' 'leads aren't getting to sales,' 'pipeline management,' 'lead qualification,' or 'when should marketing hand off to sales.' Use this for anything involving the systems and processes that connect marketing to revenue. For cold outreach emails, see cold-email. For email drip campaigns, see email-sequence. For pricing decisions, see pricing-strategy." |

### Cognition & Creation — LJG
From [ljg-skills](https://github.com/lijigang/ljg-skills) — cognitive atoms, visual casting, and workflow chaining.

| Skill | Description |
|-------|-------------|
| **ljg-card** | "Content caster (铸). Transforms content into PNG visuals. Six molds: -l (default) long reading card, -i infograph, -m multi-card reading cards (1080x1440), -v visual sketchnote, -c comic (manga-style B&W), -w whiteboard (marker-style board layout). Output to ~/Downloads/. Use when user says '铸', 'cast', '做成图', '做成卡片', '做成信息图', '做成海报', '视觉笔记', 'sketchnote', '漫画', 'comic', 'manga', '白板', 'whiteboard'. Replaces ljg-cards and ljg-infograph." |
| **ljg-invest** | 投资分析, 生成一份深度投资分析报告。不做传统投资分析——核心判断是项目是否是一台「秩序创造机器」。Use when user says '投资报告', '投资分析', '分析这个项目', '写投资报告', 'investment report', 'invest analysis', or provides entrepreneur conversation records wanting investment evaluation. Also trigger when user pastes or references meeting notes, pitch decks, or founder interviews and asks for analysis. |
| **ljg-learn** | Deep concept anatomist that deconstructs any concept through 8 exploration dimensions (history, dialectics, phenomenology, linguistics, formalization, existentialism, aesthetics, meta-philosophy) and compresses insights into an epiphany. Use when user asks to explain, dissect, or deeply understand a concept, term, or idea. Triggers on '解剖概念', '概念解剖', 'explain concept', 'learn concept', '/ljg-learn'. Produces org-mode output. |
| **ljg-paper** | "Paper reader for non-academics. Takes a paper and extracts its ideas for personal use. Focuses on understanding, not academic critique. Use when user shares an arxiv link, paper URL, PDF, or asks to analyze a research paper. Trigger words: '读论文', '分析论文', 'paper', or when user shares an academic paper." |
| **ljg-paper-flow** | "Paper workflow: read papers + cast cards in one go. Takes one or more arxiv links, paper URLs, PDFs, or paper names. For each paper, runs ljg-paper (generates org analysis) then ljg-card -l (generates long reading card PNG). Use when user says '论文流', 'paper flow', '读论文并做卡片', '论文卡片', or provides multiple papers wanting both analysis and cards." |
| **ljg-plain** | "Cognitive atom: Plain (白). Rewrites any content so a smart 12-year-old groks it. Structure-free — form follows content. Use when user says '白话说', '说人话', '解释一下', 'plain', 'grok'." |
| **ljg-rank** | 给一个领域，找出背后真正撑着它的几根独立的力。十几个现象砍到不可再少的生成器——砍完能把现象一个个生回来，才算数。Use when user says '降秩', '找秩', '秩是什么', '这个领域靠什么撑着', '背后是什么', or wants to decompose any domain to its irreducible generators. |
| **ljg-roundtable** | >- |
| **ljg-skill-map** | "Skill map viewer. Scans all installed skills and renders a visual overview — name, version, description, category at a glance. Use when user says 'skills', '技能', '技能地图', 'skill map', '我有哪些技能', '看看技能', '列出技能', 'list skills'. Also trigger when user asks what skills are available or installed." |
| **ljg-travel** | "Deep travel research workflow for museums and ancient architecture. Input a city name, auto-generates structured knowledge document (org-mode) + portable reference cards (PNG). Covers historical background, museum highlights, archaeological significance, and architectural heritage. Use when user says '旅行研究', '博物馆功课', '古建功课', 'travel research', '出发前功课', or provides a city name with intent to do deep cultural travel preparation." |
| **ljg-word** | Deep-dive English word mastery tool. Deconstructs a single English word into core semantics and epiphany. Use when user asks to explain/master a specific English word. |
| **ljg-word-flow** | "Word flow: deep-dive word analysis + infograph card in one go. Takes one or more English words, runs ljg-word (generates deep semantics analysis) then ljg-card -i (generates infograph PNG). Use when user says '词卡', 'word card', 'word flow', or provides English words wanting both analysis and visual card." |
| **ljg-writes** | "写作引擎。带着一个观点出发，在写的过程中把它想透。" |
| **ljg-x-download** | "Download images and videos from X (Twitter) posts to ~/Downloads. Use when user shares an X/Twitter link and wants to save media, or says '下载', 'download', '保存图片', '保存视频', or provides a x.com/twitter.com URL with intent to download media." |

### Install
```bash
claude install-skill https://github.com/yalding8/skills/tree/main/<skill-name>
```

</details>

---

> 通过 [sync-skills.sh](https://github.com/yalding8/skills) 从 `~/.claude/` 自动同步。
