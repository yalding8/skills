# Insight Report — Reference

## Pre-registration (Stage 1)

Lock these into the report file BEFORE looking at results; do not edit after opening the box:

- **Question / hypothesis** — the one decision this report informs.
- **Primary metric** — the single number that answers it (+ how it's computed).
- **Window** — exact date range; for survey data the fielding window, for DB the `created_at` range.
- **Threshold / success criteria** — what counts as up/down/flat, stated numerically.
- **Cohort 口径** — who's in/out (sample frame or SQL filter), pinned exactly.

Two independent waves (e.g. self-fill + interview) using different scales beat one wave — report
the crossing range, not a single point estimate.

## Cohort & data discipline (Stages 2–3)

- **Show raw data before any conclusion.** Run the actual SQL / tally; never state a headcount,
  causal mechanism, or "the difference is reasonable" without query evidence. AnalyticDB has read
  inconsistency — re-query key numbers.
- **Annotate every quantified claim**: `[已核实]` (re-checked, with evidence) / `[AI 估算]`
  (not verified). Never present an estimate as a precise measurement.
- **Batch-import artifacts**: survey/event data often lands in DB in delayed batches (~D+4).
  Watch for "single rep / single hour / same destination ≥N rows" and treat as a batch event —
  strip from the organic baseline and attribute separately.
- **Credibility note**: AI "multi-agent review" ≠ independent expert cross-check; same model shares
  blind spots. Put a credibility disclaimer at the top of AI-generated reports.

## HTML render contract (Stage 4)

The PDF script (`scripts/build_pdf.py`) injects overrides + a reveal-forcing script that depend on
these hooks. The HTML **must** use them or the static PDF renders blank/animated-out:

| Hook | Purpose |
|---|---|
| `class="rv"` on every animated/reveal block | script adds `.on` to force it visible in PDF |
| `<span class="bar"><i data-w="46.7"></i></span>` | script sets `i.style.width` from `data-w` so bars fill |
| `:root` CSS vars `--paper --ink --coral --harbour --sand --line` | print CSS references `var(--paper)` etc. |
| `.masthead` (page-1 brand bar) | hidden in print; the CDP running header replaces it |
| `section.ch` + `.ch-head` (number + `h2`) | section unit; header kept with its content, never orphaned |
| `.cols` (2-col grid: charts left, note right) | forced back to 2 columns in print |
| `.stats` (stat strip), `.bignum`, `.note`, `.pq` (pull-quote), `.waffle`, `.legend` | kept intact across page breaks |
| `footer` (dark colophon block at the end) | kept intact; gets extra bottom compression |

Design system: brand fonts (阿里普惠体 / Montserrat via `@font-face` + Google Fonts `@import`);
warm paper palette; numbered chapters; each exhibit has a title (`.ct`/`.cn2`) + source line.
Reuse the Crazy Thursday Sydney report HTML as a worked example
(`share/sydney-2026/sydney-insight-2026-*.html`).

## PDF pipeline (Stage 5)

### Config schema

```json
{
  "watermark": "Pro.uhomes.com",          // "" to disable
  "logo": "assets/uhomes-logo-red.svg",    // optional; default = skill's bundled red wordmark
  "reports": [
    { "src": "report-cn.html", "out": "Report-CN.pdf", "title": "<header left>", "brand": "<header right>" }
  ]
}
```

Paths resolve relative to the config file's directory. Run:
`python3 <skill>/scripts/build_pdf.py report.config.json`

### Why it's built this way (do not "simplify" these away)

- **Header/footer via Chrome DevTools Protocol templates, not CSS `position:fixed`.** Chrome
  CLIPS fixed elements to the content box, so a fixed footer collides with body text (the logo
  lands on top of the last chart row) or, with a negative offset, vanishes off-page. CDP
  header/footer templates render in the reserved page MARGIN and reserve their own space.
- **Logo = small bottom-LEFT corner mark + page numbers bottom-right; running header = title left /
  brand right.** A big centered footer logo reads as a PowerPoint banner; pro reports
  (McKinsey/BCG/Goldman) use a quiet corner mark + consistent running header for cross-page
  continuity. ~13px logo, muted 7.5px header/footer text.
- **Flow layout, not one-section-per-page.** Sections are unequal length; one-per-page leaves
  ragged whitespace (the exact complaint to avoid). Break rules keep single bars and section
  titles intact (`break-inside`/`break-after: avoid`) but do NOT force whole charts atomic —
  atomic charts orphan the tail into a near-empty closing page. A chart may continue across a
  page between two bars; it is never split mid-bar.
- **Margins** A4, ~12.7mm top/bottom (slim header/footer bands), ~12mm sides. Body compressed to
  14.5px / 1.64 line-height for print density without cramping.

### Dependencies & gotchas

- macOS Google Chrome at the hard-coded path; Python `websockets` (`pip install websockets`).
- The script launches headless Chrome with `--remote-debugging-port=9333`; if a stale instance
  lingers, `pkill -f "remote-debugging-port=9333"` before re-running.
- It waits 4s after load for web fonts (PuHuiTi/Montserrat) to settle — networked fonts need this.
- `websockets.connect(max_size=None)` is required: printToPDF returns multi-MB base64.
- **Always verify visually**: `pdftoppm -png -r 90 out.pdf /tmp/p` then inspect page boundaries —
  page count alone hides collisions, orphan headers, and split bars.

## Push & archive

- Report file: `docs/ANALYSIS_YYYY-MM-DD_<topic>.md` with credibility disclaimer + `[已核实]`
  annotations; update the README report index.
- Lark push: `--as bot` (dingning.ai) unless the user asks for personal identity. Sync to Feishu
  Wiki with the feishu-wiki skill.
