---
name: insight-report
description: End-to-end pipeline for uhomes market-research / channel insight reports — frame a hypothesis, organize a survey, analyze the data, produce a magazine-style bilingual HTML report, and export a watermarked, print-ready PDF with a professional running header/footer. Use when the user wants to create a market insight or 调研/洞察 report, turn survey or DB data into a report, build an HTML insight page, or export a branded watermarked PDF — triggers include "insight", "洞察", "调研报告", "市场调研", "出一份报告", "加水印 PDF", "insight 报告".
---

# Insight Report

Produces a uhomes-branded insight report across five stages. Stages 1–3 are methodology
(do them with the user); stages 4–5 are deterministic and scripted.

## The five stages

1. **命题 (Frame)** — lock the question, the metric, the window, and the decision it informs
   BEFORE seeing data. Write the pre-registration block into the report file. See REFERENCE.md
   §Pre-registration. Don't change metrics/thresholds after opening the box.
2. **组织调研 (Field)** — define the sample frame and fielding window. Data comes from a 飞书/Lark
   survey (问卷/forms) and/or a DB cohort. If DB, pin the exact cohort 口径 (SQL) and show raw
   rows first. See REFERENCE.md §Cohort & data discipline.
3. **输出报告 (Analyze & write)** — run real SQL / tally before stating any number; show raw data,
   then conclusions. Annotate every quantified claim `[已核实]`/`[AI 估算]`. Write findings as a
   tight narrative (chapters + exhibits), bilingual (CN + EN) when for external sharing.
4. **产生 HTML (Design)** — DO NOT hand-write two ~430-line HTML files. The layout lives in ONE
   shared template; content/data live in `content.<lang>.json`. Edit the JSON, then generate:
   ```bash
   python3 ~/.claude/skills/insight-report/scripts/build_report.py content.cn.json   # → CN html
   python3 ~/.claude/skills/insight-report/scripts/build_report.py content.en.json   # → EN html
   ```
   `lang: "cn"|"en"` picks the whole typographic preset (CN=阿里普惠体, EN=Montserrat) — no CSS
   edits needed. Change layout → edit `templates/report.template.html` (both languages benefit);
   change copy/data → edit the JSON only. The output conforms to the **render contract** (`.rv`
   reveal blocks; `.bar i[data-w]` bars; `section.ch`/`.ch-head`/`.cols`/`.stats`/`.pq`). See
   REFERENCE.md §Templated authoring + §HTML render contract. (Bar widths come from the helper —
   never hand-compute `data-w`; give raw values, see REFERENCE §Bar helper.)
5. **自检 + 输出 (Preflight + Export)** — decide the output form FIRST (default 长版本 for
   external sharing; A4 only for formal print), then build, then **gate on preflight**:

   - **长版本 / continuous** (DEFAULT — one tall page, NO A4 pagination/header/footer/whitespace):
     ```bash
     python3 ~/.claude/skills/insight-report/scripts/build_longimage.py report.config.json
     ```
     Emits BOTH `<src>-long.png` (raster 长图) AND `<src>-long.pdf` (single-page vector PDF). Keys:
     `width` (default 1200), `scale` (PNG DPR, default 2), shares `watermark`.
   - **A4 PDF** (paginated, watermark + running header/footer) — formal/print only:
     ```bash
     python3 ~/.claude/skills/insight-report/scripts/build_pdf.py report.config.json
     ```
   - **Preflight gate (mandatory before shipping)** — static + raster lint; FAIL blocks output:
     ```bash
     python3 ~/.claude/skills/insight-report/scripts/preflight.py report.config.json
     ```
     **FAIL must be zero; re-review every ⚠️ WARN by eye.** See §Preflight gate below.
   - Then **verify visually** — rasterize (`pdftoppm -png`) and eyeball; never declare done from
     page count alone. To deliver into Feishu, see REFERENCE §Feishu delivery.

## Stage 5 quick start

Create `report.config.json` next to the HTML files (paths relative to the config):

```json
{
  "watermark": "Pro.uhomes.com",
  "reports": [
    { "src": "report-cn.html", "out": "Report-CN.pdf",
      "title": "悉尼留学市场观察 · 2026", "brand": "异乡好居　渠道调研洞察" },
    { "src": "report-en.html", "out": "Report-EN.pdf",
      "title": "Sydney Student Housing Market · 2026", "brand": "uhomes.com　Channel Insights" }
  ]
}
```

Then run the script. Output: each PDF gets a tiled diagonal watermark, a running header
(title left / brand right) and footer (small uhomes.com wordmark bottom-left + page numbers)
on **every** page. After building, **verify visually** — rasterize pages (`pdftoppm -png`) and
eyeball the boundaries; do not declare done from the page count alone.

## Preflight gate (出片前自检 — mandatory门禁)

Before exporting/shipping, run preflight on the report config — this is a hard gate:

```bash
python3 ~/.claude/skills/insight-report/scripts/preflight.py report.config.json
```

- **FAIL must be zero** (`bar-overflow`: any `data-w > 100`). Non-zero exit = do not ship, fix first.
- **Every ⚠️ WARN must be eyeballed** — WARN ≠ ignorable; it's "machine can't be sure, human must judge."
  WARNs map to defects this skill historically shipped only because a human caught them:
  `billboard-bignum` (big number → `.note .fig` inline) · `waffle` (→ `.bar-row`) · `footer-fontsize`
  (~10px) · `cols-single-column` (must be stacked) · `topbar` (visible; legacy `.masthead`
  display:none) · `title-orphan` (`<h1>` fragments ≤9 CJK chars) · `render-contract` (`.bar`>`<i data-w>`,
  `.rv`, `:root` vars) · `a4-ragged-whitespace` (non-last page >35% empty bottom = content jumped).
- Order: build PDF/long → run preflight (raster checks need the PDF present) → FAIL=0 + WARN reviewed
  → only then push/archive. Report "preflight FAIL=0, N WARN reviewed" in the delivery summary.

## Conventions (always)

- Brand fonts: 中文 阿里普惠体 (Alibaba PuHuiTi) / 英文 Montserrat.
- **Templated authoring (not hand-written HTML).** One `templates/report.template.html` + per-language
  `content.<lang>.json` → `build_report.py`. Edit layout once (template), copy/data in JSON. Never
  maintain two parallel HTML files by hand. See REFERENCE.md §Templated authoring + §Bar helper.
- **Layout (brand review 2026-06): stacked not boxed.** Single-column `.cols` (chart on top, note
  below — never left-right); no heavy boxed stat strip; footer source/disclaimer at ~10px; every
  text block atomic across pages. See REFERENCE.md §Design rules.
- **Stat strip = semantic color by sign (auto).** `+`→green, `−`→red, unsigned→positional fallback;
  override with `"tone"`. Don't mix a signed delta with a bare ratio (`"7 / 8"`) — rewrite as big
  count `"7"` + denominator in the span. Leading +/− auto-balanced via `.sgn`. See REFERENCE §Design
  rules 6–7.
- **Logo wordmark is tight-cropped** (`logo-uhomes`, 18px); if a wordmark looks tiny, crop the SVG
  viewBox, don't inflate CSS height. `head.keywords` → meta tags; `footer.brand` takes raw HTML so
  brand names can be clickable links (live in HTML/PDF, not PNG). See REFERENCE §Logo strategy +
  §content JSON extras.
- **Generated HTML is self-contained** — the logo is embedded as a `data:` URI, so handoff = ship the
  single `.html` (no separate logo file). Fonts still load from CDN (online needed). See REFERENCE
  §Self-contained HTML.
- **Logo by language (auto)**: EN report → **uhomes.com only** (`uhomes-logo-red.svg`); CN report →
  **3-brand combined logo 异乡好居 ｜ 异乡缴费 ｜ 异乡人才** (`uhomes-cn-combined-logo.svg`).
  `build_report.py` picks this from `lang` — leave `content.topbar` as just `issue`. Override per
  report-type (university/apartment) via `content.topbar.logo_src`. See REFERENCE.md §Logo strategy.
- **Watermark by language (auto)**: EN report → faint **uhomes.com wordmark + `watermark` url text**
  tiled; CN report → **text-only** tile. Both build scripts detect `lang` from the HTML. See
  REFERENCE.md §PDF pipeline config schema.
- Pre-register before results; show raw data before conclusions; annotate AI-estimated numbers.
- Archive the report as `docs/ANALYSIS_YYYY-MM-DD_<topic>.md` and update the README index.

See **[REFERENCE.md](REFERENCE.md)** for the render contract, pre-registration template, cohort
discipline, the PDF config schema, and the design decisions behind the PDF pipeline.
