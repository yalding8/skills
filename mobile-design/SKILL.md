---
name: mobile-design
description: Mobile UX design guidance — touch targets, gesture design, mobile navigation patterns (tabs/drawers/bottom sheets), mobile UI components, iOS HIG / Material Design conventions, mobile accessibility, and mobile performance. Use when designing or building mobile-first web apps, native/hybrid apps (React Native, Flutter), PWAs, touch-first interfaces, gesture interactions, mobile forms/e-commerce, adapting data-heavy dashboards for mobile, or auditing mobile UX/accessibility. Boundaries — this skill owns mobile UX patterns, touch/gesture interaction, and app navigation; detailed responsive layout/breakpoint engineering belongs to the responsive-design skill; retrofitting an EXISTING design for cross-device adaptation belongs to the Impeccable adapt skill.
category: design
tags: [mobile, ux, touch, gestures, navigation, mobile-first, ios, android]
version: 1.1.0
---

# Mobile Design Skill

Mobile UX patterns, touch interactions, gesture design, mobile-first principles, app navigation, and mobile performance. Detailed material lives in `references/` — read only the file(s) relevant to the task at hand.

## Scope & Boundaries

- **This skill**: mobile UX patterns, touch/gesture design, app navigation, mobile components, platform conventions, mobile a11y & performance.
- **responsive-design skill**: in-depth responsive layout/grid/breakpoint engineering. This skill only keeps the mobile-side viewport/breakpoint quick facts needed for mobile work.
- **Impeccable `adapt` skill**: transforming an already-built design to work across devices/contexts. Use `adapt` for retrofits; use this skill when designing mobile UX from the start.

## Core Rules (use directly, no file read needed)

**Touch targets**
- Minimum: 44×44pt (iOS) / 48×48dp (Android Material) / WCAG AAA 44×44px
- Recommended: 48×48px minimum, 56×56px optimal
- Spacing between targets: ≥8px, 12–16px for frequent controls

**Thumb zones** (one-handed use)
- Easy: bottom third, center → primary actions here
- Difficult: top corners → destructive/rare actions there
- Navigation at top or bottom, never middle

**Navigation choice**
- 3–5 main sections → bottom tab bar (always show labels)
- 6+ sections / secondary features → drawer (hamburger)
- Contextual actions → bottom sheet / action sheet

**Forms & inputs**
- Input font-size ≥16px (prevents iOS auto-zoom)
- Match `inputmode`/`type` to content: email / tel / numeric / decimal / url / search
- `touch-action: manipulation` to kill double-tap zoom delay

**Platform quick numbers**
- iOS: nav bar 44pt, tab bar 49pt + safe area, system blue #007AFF, destructive red #FF3B30
- Android: app bar 56dp, bottom nav 56dp, FAB 56×56dp, 4dp spacing grid
- Safe areas: `env(safe-area-inset-top/bottom/left/right)`; viewport meta `width=device-width, initial-scale=1`

**Accessibility & performance floors**
- Contrast: 4.5:1 normal text, 3:1 large text & UI components (WCAG AA)
- Tap feedback within 0–100ms; visible `:focus-visible` outlines
- Core Web Vitals: LCP < 2.5s, FID < 100ms, CLS < 0.1
- Images: `srcset` + `loading="lazy"` + WebP fallback

## Reference Routing

| Task / question | Read |
|---|---|
| Mobile-first vs desktop-first CSS, viewport meta, safe areas (notch), breakpoints, orientation, container queries | `references/mobile-first-foundations.md` |
| Touch target sizing/spacing details, thumb-zone layout, tap feedback, swipe (swipe-to-delete, pull-to-refresh), pinch-zoom, long press, drag & drop implementations | `references/touch-and-gestures.md` |
| Tab bars, drawers/hamburger menus, bottom sheets, full-screen modals, stack navigation (incl. React Navigation setups) | `references/navigation-patterns.md` |
| Cards, iOS-style lists, mobile-optimized forms, keyboard `inputmode` table, action sheets | `references/ui-components.md` |
| iOS HIG specifics (nav/tab bar metrics, SF Pro, system colors, SwiftUI) and Material Design (app bar, FAB, elevation, Roboto, Compose) | `references/platform-conventions.md` |
| Touch-target a11y, screen reader / semantic HTML / React Native accessibility props, color contrast, focus indicators | `references/accessibility.md` |
| Responsive images, lazy loading, skeleton screens, PWA service worker caching, Core Web Vitals measurement | `references/performance.md` |
| Full worked examples: e-commerce product grid, infinite scroll, search + autocomplete, filter drawer, payment form, plus 15 more pattern summaries | `references/examples.md` |

When a task spans multiple topics (e.g., "build a mobile checkout"), read only the 2–3 most relevant files (typically touch-and-gestures + ui-components + examples), not all of them.
