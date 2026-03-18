# Agent Skills

A collection of agent skills that extend capabilities across planning, development, tooling, and frontend design.

## Planning & Design

These skills help you think through problems before writing code.

- **write-a-prd** — Create a PRD through an interactive interview, codebase exploration, and module design. Filed as a GitHub issue.
  > 通过交互式访谈、代码库探索和模块设计，生成 PRD 并提交为 GitHub issue。
- **prd-to-issues** — Break a PRD into independently-grabbable GitHub issues using vertical slices.
  > 将 PRD 拆解为可独立认领的垂直切片 GitHub issue。
- **prd-to-plan** — Turn a PRD into a multi-phase implementation plan saved as a local Markdown file.
  > 将 PRD 转化为多阶段实施计划，保存为本地 Markdown 文件。
- **grill-me** — Get relentlessly interviewed about a plan or design until every branch of the decision tree is resolved.
  > 对你的设计方案进行压力测试式追问，直到每个决策分支都被解决。
- **design-an-interface** — Generate multiple radically different interface designs using parallel sub-agents, then compare.
  > 并行生成多种截然不同的接口设计方案，对比后选出最优解。
- **design-interface** — Similar to design-an-interface with a streamlined workflow for quick interface exploration.
  > 精简版接口设计探索，适合快速原型场景。
- **ubiquitous-language** — Extract a DDD-style ubiquitous language glossary from the current conversation.
  > 从当前对话中提取 DDD 风格的统一语言词汇表。

## Development

These skills help you write, refactor, and fix code.

- **tdd** — Test-driven development with a red-green-refactor loop. Builds features or fixes bugs one vertical slice at a time.
  > 测试驱动开发：红-绿-重构循环，每次只做一个垂直切片。
- **triage-issue** — Investigate a bug by exploring the codebase, identify the root cause, and file a GitHub issue with a TDD-based fix plan.
  > 自动排查 bug 根因，生成带 TDD 修复计划的 GitHub issue。
- **improve-codebase-architecture** / **improve-architecture** — Explore a codebase for architectural improvement opportunities, focusing on deepening shallow modules and improving testability.
  > 扫描代码库的架构薄弱点，提出"深模块"重构方案并创建 RFC issue。
- **request-refactor-plan** / **request-refactor** — Create a detailed refactor plan with tiny commits via user interview, then file as a GitHub issue.
  > 通过访谈制定细粒度重构计划（小步提交），提交为 GitHub issue。
- **migrate-to-shoehorn** — Migrate test files from `as` type assertions to `@total-typescript/shoehorn`.
  > 将测试文件中的 `as` 类型断言迁移为 shoehorn 的 `fromPartial()`。

## Tooling & Setup

- **setup-pre-commit** — Set up Husky pre-commit hooks with lint-staged, Prettier, type checking, and tests.
  > 一键配置 Husky 预提交钩子 + lint-staged + Prettier。
- **git-guardrails-claude-code** / **git-guardrails** — Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, etc.) before they execute.
  > 配置 Claude Code 钩子，在执行前拦截危险 git 命令。
- **scaffold-exercises** — Create exercise directory structures with sections, problems, solutions, and explainers.
  > 生成课程练习目录结构（题目/解答/讲解）。
- **fix-format** — Auto-fix formatting issues in code files.
  > 自动修复代码格式问题。

## Writing & Knowledge

- **write-a-skill** — Create new skills with proper structure, progressive disclosure, and bundled resources.
  > 创建新的 agent skill，包含正确的文件结构和渐进式指令。
- **edit-article** — Edit and improve articles by restructuring sections, improving clarity, and tightening prose.
  > 编辑文章：重组段落、提升清晰度、精简表达。
- **obsidian-vault** — Search, create, and manage notes in an Obsidian vault with wikilinks and index notes.
  > 在 Obsidian 笔记库中搜索、创建和管理笔记。

## Frontend Design (Impeccable)

From [Impeccable](https://github.com/pbakaus/impeccable) — design vocabulary and anti-patterns for AI-assisted frontend development.

| Command | Description |
|---------|-------------|
| **frontend-design** | Comprehensive design skill with 7 domain references (typography, color, spatial, motion, interaction, responsive, UX writing) |
| **teach-impeccable** | One-time setup: gather design context and save to config |
| **audit** | Technical quality checks — a11y, performance, responsive |
| **critique** | UX design review — hierarchy, clarity, emotional resonance |
| **polish** | Final quality pass before shipping |
| **typeset** | Fix font choices, hierarchy, sizing, readability |
| **arrange** | Fix layout, spacing, visual rhythm |
| **colorize** | Add strategic color to monochromatic interfaces |
| **animate** | Add purposeful motion and micro-interactions |
| **normalize** | Align with design system standards |
| **distill** | Strip to essence — remove unnecessary complexity |
| **clarify** | Improve unclear UX copy and microcopy |
| **optimize** | Performance improvements (loading, rendering, bundle) |
| **harden** | Error handling, i18n, edge cases |
| **bolder** | Amplify safe/boring designs |
| **quieter** | Tone down overly bold designs |
| **delight** | Add moments of joy and personality |
| **extract** | Pull into reusable components |
| **adapt** | Adapt for different devices and contexts |
| **onboard** | Design onboarding flows and empty states |
| **overdrive** | Push past conventional limits with ambitious effects |
