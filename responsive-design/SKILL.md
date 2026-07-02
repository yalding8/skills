---
name: responsive-design
description: Mobile-first responsive layout engineering — fluid layouts, breakpoint/media-query strategy, container queries, flexbox and CSS grid, viewport units, clamp()/min()/max(), responsive images (srcset/picture), plus performance and accessibility for cross-device CSS. Use when building or fixing layouts that must adapt across screen sizes — responsive pages, card grids, navigation, forms, tables, dashboards, galleries — or when choosing breakpoints, CSS units, or image loading strategy. Boundaries — this skill owns layout technique (fluid layout, media queries, flexbox/grid, responsive images); mobile UX patterns, touch targets, gestures, and app navigation belong to the mobile-design skill.
category: frontend
tags: [css, responsive, mobile-first, flexbox, grid, media-queries]
version: 1.1.0
---

# Responsive Design Skill

Router file. Core decision rules below are self-sufficient for common cases; read a `references/*.md` file only when you need the full technique or a copy-paste pattern.

## Core Decision Rules (use directly, no file read needed)

**Always mobile-first**: write base styles for mobile, enhance upward with `min-width` queries. Never desktop-first with `max-width` overrides.

**Standard breakpoints** (adjust to content, not devices):

| Breakpoint | Target |
|---|---|
| (base, no query) | Mobile 320px+ |
| `min-width: 480px` | Large mobile |
| `min-width: 768px` | Tablet |
| `min-width: 1024px` | Desktop |
| `min-width: 1280px` | Wide desktop |
| `min-width: 1536px` | Ultra-wide |

**Unit selection**:
- Font sizes → `rem` (respects user settings); fluid type → `clamp(min, vw-based, max)`, e.g. `clamp(1.5rem, 4vw + 1rem, 3rem)`
- Spacing/padding → `rem` or `clamp()`, e.g. `clamp(1rem, 5vw, 3rem)`
- Container widths → `%` / `100%` + `max-width` px cap
- Full-height sections → `100dvh` (not `100vh`, which breaks under mobile browser chrome); `svh`/`lvh` for explicit small/large viewport
- Media query thresholds → `em` preferred (zoom-safe) or `px`

**Layout technique choice**:
- One-dimensional (row OR column, nav bars, toolbars) → Flexbox
- Two-dimensional (rows AND columns, page shells, card grids) → CSS Grid
- Auto-responsive grid without media queries → `grid-template-columns: repeat(auto-fit, minmax(250px, 1fr))`
- Component that adapts to its container (not the viewport) → container queries (`container-type: inline-size` + `@container`)

**Responsive images**: same image, multiple sizes → `srcset` + `sizes`; different crops/formats per breakpoint (art direction) → `<picture>`; always set `width`/`height` (or `aspect-ratio`) to prevent CLS; below-the-fold → `loading="lazy"`.

**Non-negotiables**: touch targets ≥ 44×44px; body text ≥ 16px on mobile; `<meta name="viewport" content="width=device-width, initial-scale=1">`; test at 320px width and with 200% text zoom.

## Routing Table — what to read for which problem

| Problem | Read |
|---|---|
| Mobile-first philosophy, breakpoint strategy in depth, fluid container/grid/typography patterns | `references/core-concepts.md` |
| Flexbox patterns (responsive nav, flexible cards, sidebar) and CSS Grid (auto-fit minmax, named areas, gallery with spans) | `references/flexbox-grid.md` |
| Advanced media queries (orientation, hover/pointer, prefers-reduced-motion/color-scheme, print) and container queries | `references/media-queries.md` |
| `srcset`/`sizes`, `<picture>` art direction, WebP fallbacks, responsive background images | `references/responsive-images.md` |
| Viewport units (vw/vh/dvh/svh/lvh, mobile pitfalls) and modern functions: clamp(), min(), max(), aspect-ratio | `references/units-and-functions.md` |
| Critical CSS, lazy loading, performance budget; touch targets, readable text, focus indicators; testing checklist, common pitfalls, tools/docs links | `references/performance-accessibility.md` |
| Full-page layout examples: Holy Grail, Dashboard, Magazine, Sidebar with toggle, Footer | `references/examples-page-layouts.md` |
| Component examples: Card Grid, Navigation (hamburger→horizontal), Hero, Masonry, Feature Grid, Image Gallery | `references/examples-components.md` |
| Data-dense examples: Form, Table (stacked-card mobile pattern), Pricing Table, Timeline | `references/examples-forms-data.md` |

When implementing a concrete UI, prefer starting from the closest example file, then consult technique files for the pieces you need to change.
