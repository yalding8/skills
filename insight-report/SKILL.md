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
4. **产生 HTML (Design)** — build the report as a magazine-style HTML page that conforms to the
   **render contract** (brand fonts; `.rv` reveal blocks; `.bar i[data-w]` bars; `section.ch` /
   `.ch-head` / `.cols` / `.stats` / `.pq` structure). The PDF script depends on these hooks.
   See REFERENCE.md §HTML render contract. Produce one HTML per language.
5. **输出 (Export)** — two output modes from the SAME `report.config.json`:

   - **A4 PDF** (paginated, watermark + running header/footer) — for formal/print:
     ```bash
     python3 ~/.claude/skills/insight-report/scripts/build_pdf.py report.config.json
     ```
   - **长图 / long PNG** (one continuous scroll image, NO pagination, NO per-page
     header/footer/whitespace) — for WeChat / Feishu / social sharing:
     ```bash
     python3 ~/.claude/skills/insight-report/scripts/build_longimage.py report.config.json
     ```
     Emits `<src>-long.png` per report. Optional config keys: `width` (col px, default 1200),
     `scale` (DPR, default 2), shares `watermark`. **Default to the long PNG when the user wants
     a "长版本" / continuous report rather than A4 pages.**

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

## Conventions (always)

- Brand fonts: 中文 阿里普惠体 (Alibaba PuHuiTi) / 英文 Montserrat.
- **Layout (brand review 2026-06): stacked not boxed.** Single-column `.cols` (chart on top, note
  below — never left-right); no heavy boxed stat strip; footer source/disclaimer at ~10px; every
  text block atomic across pages. See REFERENCE.md §Design rules.
- **Logo by report type**: top `.topbar` logo = uhomes own (city report) / the university's logo
  (university report) / the apartment brand's logo (apartment report); footer corner mark always
  uhomes. See REFERENCE.md §Logo strategy. Bundled: `assets/uhomes-logo-red.svg` (+ white variant).
- Pre-register before results; show raw data before conclusions; annotate AI-estimated numbers.
- Archive the report as `docs/ANALYSIS_YYYY-MM-DD_<topic>.md` and update the README index.

See **[REFERENCE.md](REFERENCE.md)** for the render contract, pre-registration template, cohort
discipline, the PDF config schema, and the design decisions behind the PDF pipeline.
