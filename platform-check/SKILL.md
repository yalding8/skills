---
name: platform-check
description: Prevent AI from reimplementing platform-native capabilities when modifying UI code. Enforces three gates — read design spec before coding, check platform mechanisms before building, request human screenshot verification after changes. Use when modifying UI pages (WXML/WXSS/JSX/CSS), adding interactive features (share, navigation, refresh, auth), or when user says "check platform", "design check", "UI review".
---

# Platform Check

Stop. Before writing any UI code, pass three gates.

## Gate 1: Read the Design Spec

**Before modifying any page's WXML/WXSS/HTML/CSS:**

1. Check if a `.pen` design file exists for this project
2. If yes → use MCP Pencil `batch_get` to read the exact frame for this page
3. Extract precise values: padding, gap, cornerRadius, fontSize, fontWeight, fill colors, shadow
4. Write CSS using these extracted values — not from memory or guesswork

**If no design file exists:** ask the user for design reference before proceeding.

**Never:** guess spacing, colors, or layout. Every visual value must trace to a source.

## Gate 2: Check Platform Capabilities

**Before implementing any interactive feature, ask:**

> "Does the platform already provide this?"

### WeChat Mini Program Native Capabilities

| Feature | Platform Mechanism | Do NOT Build |
|---------|-------------------|-------------|
| Share/Forward | `onShareAppMessage` + right-corner "···" menu | Custom share buttons on page |
| Share to Moments | `onShareTimeline` lifecycle | Custom "share to moments" button |
| Pull-to-refresh | `enablePullDownRefresh` + `onPullDownRefresh` | Custom pull-to-refresh UI |
| Back navigation | Native nav bar back arrow | Custom back button (unless `navigationStyle: "custom"`) |
| Page scroll | Pages scroll natively | `scroll-view` wrapping entire page |
| Image preview | `wx.previewImage` | Custom image viewer/lightbox |
| Copy to clipboard | `wx.setClipboardData` | Custom copy UI |
| Phone call | `wx.makePhoneCall` | Custom phone dialer |
| Location | `wx.openLocation` / `wx.chooseLocation` | Custom map picker |
| Loading toast | `wx.showLoading` / `wx.showToast` | Custom loading overlay (for simple cases) |

**Rule:** If the platform has it, use it. Only build custom UI when the platform mechanism is genuinely insufficient AND the user explicitly approves.

### Adding Other Platforms

This table is extensible. For Web, React Native, Flutter — maintain an equivalent table in CLAUDE.md.

## Gate 3: Verify with Human

**After modifying any visual code:**

1. State what was changed and why
2. List what is **machine-verified**: lint passed, tests passed, no compile errors
3. List what **needs human verification**: visual appearance, spacing, interaction feel
4. Ask: "Please check the page in devtools/device and confirm the visual result. Specifically verify: [list 2-3 concrete checkpoints]"

**Never say:**
- "已修复 ✅" for visual changes (you cannot see the result)
- "效果已对齐设计稿" (you cannot compare visually)

**Instead say:**
- "代码已更新。⚠️ 请在开发者工具中确认：1) 分享按钮样式 2) 筛选标签颜色 3) 卡片间距"

## Quick Reference

```
Before coding  → Gate 1 (read design) + Gate 2 (check platform)
After coding   → Gate 3 (human verification)
```

Three questions to ask yourself:
1. "Am I building something the platform already has?"
2. "Did I read the actual design values or am I guessing?"
3. "Can I verify this visually, or do I need the human to check?"
