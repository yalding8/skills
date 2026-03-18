# Agent Skills

A personal collection of agent skills for Claude Code, Cursor, and other AI coding tools.

> My skills directory, synced automatically from `~/.claude/`.

个人 AI 编码工具 Skill 合集，从 `~/.claude/` 自动同步。

---

## Planning & Design | 规划与设计

Skills to think through problems before writing code.
在写代码之前理清思路的技能。

- **write-a-prd** — Create a PRD through user interview, codebase exploration, and module design, then submit as a GitHub issue. Use when user wants to write a PRD, create a product requirements document, or plan a new feature.
- **prd-to-issues** — Break a PRD into independently-grabbable GitHub issues using tracer-bullet vertical slices. Use when user wants to convert a PRD to issues, create implementation tickets, or break down a PRD into work items.
- **prd-to-plan** — Turn a PRD into a multi-phase implementation plan using tracer-bullet vertical slices, saved as a local Markdown file in ./plans/. Use when user wants to break down a PRD, create an implementation plan, plan phases from a PRD, or mentions "tracer bullets".
- **grill-me** — Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
- **design-an-interface** — Generate multiple radically different interface designs for a module using parallel sub-agents. Use when user wants to design an API, explore interface options, compare module shapes, or mentions "design it twice".
- **design-interface** — Generate multiple radically different interface designs for a module using parallel sub-agents. Use when user wants to design an API, explore interface options, compare module shapes, or mentions "design it twice".
- **ubiquitous-language** — Extract a DDD-style ubiquitous language glossary from the current conversation, flagging ambiguities and proposing canonical terms. Saves to UBIQUITOUS_LANGUAGE.md. Use when user wants to define domain terms, build a glossary, harden terminology, create a ubiquitous language, or mentions "domain model" or "DDD".

## Development | 开发

Skills for writing, refactoring, and fixing code.
编写、重构和修复代码的技能。

- **tdd** — Test-driven development with red-green-refactor loop. Use when user wants to build features or fix bugs using TDD, mentions "red-green-refactor", wants integration tests, or asks for test-first development.
- **triage-issue** — Triage a bug or issue by exploring the codebase to find root cause, then create a GitHub issue with a TDD-based fix plan. Use when user reports a bug, wants to file an issue, mentions "triage", or wants to investigate and plan a fix for a problem.
- **improve-codebase-architecture** — Explore a codebase to find opportunities for architectural improvement, focusing on making the codebase more testable by deepening shallow modules. Use when user wants to improve architecture, find refactoring opportunities, consolidate tightly-coupled modules, or make a codebase more AI-navigable.
- **improve-architecture** — Explore a codebase to find opportunities for architectural improvement, focusing on making the codebase more testable by deepening shallow modules. Use when user wants to improve architecture, find refactoring opportunities, consolidate tightly-coupled modules, or make a codebase more AI-navigable.
- **request-refactor-plan** — Create a detailed refactor plan with tiny commits via user interview, then file it as a GitHub issue. Use when user wants to plan a refactor, create a refactoring RFC, or break a refactor into safe incremental steps.
- **request-refactor** — Create a detailed refactor plan with tiny commits via user interview, then file it as a GitHub issue. Use when user wants to plan a refactor, create a refactoring RFC, or break a refactor into safe incremental steps.
- **migrate-to-shoehorn** — Migrate test files from `as` type assertions to @total-typescript/shoehorn. Use when user mentions shoehorn, wants to replace `as` in tests, or needs partial test data.

## Tooling & Setup | 工具与配置

- **setup-pre-commit** — Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current repo. Use when user wants to add pre-commit hooks, set up Husky, configure lint-staged, or add commit-time formatting/typechecking/testing.
- **git-guardrails-claude-code** — Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use when user wants to prevent destructive git operations, add git safety hooks, or block git push/reset in Claude Code.
- **git-guardrails** — Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use when user wants to prevent destructive git operations, add git safety hooks, or block git push/reset in Claude Code.
- **scaffold-exercises** — Create exercise directory structures with sections, problems, solutions, and explainers that pass linting. Use when user wants to scaffold exercises, create exercise stubs, or set up a new course section.
- **fix-format** — 

## Writing & Knowledge | 写作与知识

- **write-a-skill** — Create new agent skills with proper structure, progressive disclosure, and bundled resources. Use when user wants to create, write, or build a new skill.
- **edit-article** — Edit and improve articles by restructuring sections, improving clarity, and tightening prose. Use when user wants to edit, revise, or improve an article draft.
- **obsidian-vault** — Search, create, and manage notes in the Obsidian vault with wikilinks and index notes. Use when user wants to find, create, or organize notes in Obsidian.

## Frontend Design — Impeccable | 前端设计

From [Impeccable](https://github.com/pbakaus/impeccable) — design vocabulary and anti-patterns for AI-assisted frontend development.

来自 [Impeccable](https://github.com/pbakaus/impeccable) — AI 辅助前端开发的设计词汇与反模式库。

| Command | Description | 说明 |
|---------|-------------|------|
| **frontend-design** | Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications. Generates creative, polished code that avoids generic AI aesthetics. | 综合设计技能，含 7 个领域参考文件 |
| **teach-impeccable** | One-time setup that gathers design context for your project and saves it to your AI config file. Run once to establish persistent design guidelines. | 首次设置：采集项目设计上下文 |
| **audit** | Perform comprehensive audit of interface quality across accessibility, performance, theming, and responsive design. Generates detailed report of issues with severity ratings and recommendations. | 技术质量检查 — 无障碍、性能、响应式 |
| **critique** | Evaluate design effectiveness from a UX perspective. Assesses visual hierarchy, information architecture, emotional resonance, and overall design quality with actionable feedback. | UX 设计评审 — 层级、清晰度、情感共鸣 |
| **polish** | Final quality pass before shipping. Fixes alignment, spacing, consistency, and detail issues that separate good from great. | 上线前最终打磨 |
| **typeset** | Improve typography by fixing font choices, hierarchy, sizing, weight consistency, and readability. Makes text feel intentional and polished. | 修复字体选择、层级、尺寸、可读性 |
| **arrange** | Improve layout, spacing, and visual rhythm. Fixes monotonous grids, inconsistent spacing, and weak visual hierarchy to create intentional compositions. | 修复布局、间距、视觉节奏 |
| **colorize** | Add strategic color to features that are too monochromatic or lack visual interest. Makes interfaces more engaging and expressive. | 为单色界面添加战略性色彩 |
| **animate** | Review a feature and enhance it with purposeful animations, micro-interactions, and motion effects that improve usability and delight. | 添加有意义的动效和微交互 |
| **normalize** | Normalize design to match your design system and ensure consistency | 对齐设计系统标准 |
| **distill** | Strip designs to their essence by removing unnecessary complexity. Great design is simple, powerful, and clean. | 去除不必要的复杂性，提炼精华 |
| **clarify** | Improve unclear UX copy, error messages, microcopy, labels, and instructions. Makes interfaces easier to understand and use. | 改善不清晰的 UX 文案和微文案 |
| **optimize** | Improve interface performance across loading speed, rendering, animations, images, and bundle size. Makes experiences faster and smoother. | 性能优化 — 加载、渲染、包体积 |
| **harden** | Improve interface resilience through better error handling, i18n support, text overflow handling, and edge case management. Makes interfaces robust and production-ready. | 错误处理、国际化、边界情况 |
| **bolder** | Amplify safe or boring designs to make them more visually interesting and stimulating. Increases impact while maintaining usability. | 放大平淡设计的视觉冲击力 |
| **quieter** | Tone down overly bold or visually aggressive designs. Reduces intensity while maintaining design quality and impact. | 降低过于激进的设计 |
| **delight** | Add moments of joy, personality, and unexpected touches that make interfaces memorable and enjoyable to use. Elevates functional to delightful. | 添加愉悦感和个性化触点 |
| **extract** | Extract and consolidate reusable components, design tokens, and patterns into your design system. Identifies opportunities for systematic reuse and enriches your component library. | 提取为可复用组件 |
| **adapt** | Adapt designs to work across different screen sizes, devices, contexts, or platforms. Ensures consistent experience across varied environments. | 适配不同设备和场景 |
| **onboard** | Design or improve onboarding flows, empty states, and first-time user experiences. Helps users get started successfully and understand value quickly. | 设计引导流程和空状态 |
| **overdrive** | Push interfaces past conventional limits with technically ambitious implementations. Whether that's a shader, a 60fps virtual table, spring physics on a dialog, or scroll-driven reveals — make users ask "how did they do that?" | 突破常规限制的技术炫技效果 |

---

> Auto-synced from `~/.claude/` via [sync-skills.sh](https://github.com/yalding8/skills).
>
> 通过 sync-skills.sh 从 `~/.claude/` 自动同步。
