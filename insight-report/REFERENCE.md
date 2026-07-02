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

## Templated authoring (Stage 4)

The report is NOT two hand-maintained HTML files. Layout lives in one shared template; content/data
live in per-language JSON. This kills the "edit the same fix twice in CN and EN" error class.

**Three steps:**
1. **Edit `content.<lang>.json`** (text, chart values, chapters). `lang: "cn"|"en"` selects the whole
   typographic preset (CN=阿里普惠体, EN=Montserrat) — no CSS edits.
2. **Generate**: `python3 scripts/build_report.py content.cn.json` (EN likewise). The renderer reads
   `templates/report.template.html` + the built-in CN/EN presets and emits HTML 1:1 with the design.
3. **Export**: `build_longimage.py` (长图/长 PDF, default) or `build_pdf.py` (A4) as usual.

Change layout → edit `templates/report.template.html` or a preset once, both languages benefit.
Change copy/data → edit only the relevant `content.<lang>.json`. Output name = JSON `output` key (or `-o`).
Starter: `templates/content.example.json` (delete its `__*` comment keys in a real file).

### Self-contained HTML (handoff to ops)

`build_report.py` **embeds the topbar logo as a base64 `data:` URI**, so the generated HTML has NO
local asset dependency — ship the single `.html` and the logo renders anywhere (verified by rendering
in an empty dir). Custom `topbar.logo_src` is embedded too (read relative to the content JSON); a
missing file degrades to a plain relative `src` (then it MUST be shipped alongside). **History:**
before this, the HTML referenced `uhomes-logo-red.svg` by relative path → "sent only the HTML, logo
disappeared" on every handoff. Fixed by mechanism, not by "remember to attach the file."

⚠️ **Fonts are still CDN-loaded** (Montserrat via Google Fonts, 阿里普惠体 via Aliyun OSS). The page
needs internet for brand fonts; offline/air-gapped servers fall back to system fonts (layout intact,
typeface differs). If a deploy target is intranet-only, embed the woff2 as `@font-face` data URIs too.

### content JSON — head & footer extras

- **`head.keywords`** (optional): comma-separated SEO/social tags → `<meta name="keywords">`. Omit
  → empty meta (back-compatible; old reports build unchanged).
- **`footer.brand` is injected as RAW HTML** (not escaped) — so brand segments can be clickable links:
  `"<a href=\"https://www.uhomes.com\" target=\"_blank\" rel=\"noopener\">uhomes.com</a>　·　…"`.
  Links inherit color + have no underline (`footer .f-brand a`), and survive as clickable `/URI`
  annotations in the A4 PDF and long PDF (NOT in the long **PNG** — it's a flat raster). EN brand line
  is `uhomes.com · UhomesPay · Uhomesjobs` → `www.uhomes.com` / `uhomespay.com` / `uhomesjobs.com`.

### Bar helper (never hand-compute `data-w`)

Each chart carries `"bars": [...]`; each row `{label, value, ...}`. The helper computes bar widths:

- `mode: "scale"` (default) — `data-w = value / max * scale` (scale default 95); for raw magnitudes
  (deal counts etc.), tallest bar ≈95% wide.
- `mode: "percent"` — `data-w = value`, prints `N%`; for shares that sum to 100 (progress bars).
- `mode: "raw_w"` — you give `w` + `value_text`; helper does no math; for YoY charts where bar length
  is a hand-tuned visual code decoupled from the printed % (country / peer-city exhibits).
- Row keys: `label`(req) / `value` / `value_text`(override printed value, e.g. `+22%`) / `w`(explicit
  width — **raw_w only**; in scale/percent it bypasses the math and the builder WARNs) /
  `style`(`""|coral|sand|ink`, deprecated) / `hl`(highlight row) / `neg`(force negative style).
  **Any value<0 or w<0 → width 0, value printed red `.neg`, minus sign kept.** The builder also
  WARNs on any resulting `data-w > 100` (preflight FAILs on it).

## HTML render contract (Stage 4 output)

`build_report.py` produces this; `build_pdf.py`/`build_longimage.py` inject overrides + a
reveal-forcing script that depend on these hooks. The HTML **must** use them or the static
PDF/PNG renders blank/animated-out:

| Hook | Purpose |
|---|---|
| `class="rv"` on every animated/reveal block | script adds `.on` to force it visible in PDF |
| `<span class="bar"><i data-w="46.7"></i></span>` | script sets `i.style.width` from `data-w` so bars fill |
| `:root` CSS vars — legacy `--paper --ink --coral --harbour --sand --line` AND 4-colour `--brand --up --down --data` | print CSS references `var(--paper)` etc.; the 4-colour system drives chart semantics; preflight requires both sets |
| `.topbar` (page-1 logo lockup) | **visible in print** — holds the report-type logo + issue/date; see logo strategy below |
| `.masthead` (legacy brand bar) | hidden in print; kept only for backward-compat (use `.topbar` instead) |
| `section.ch` + `.ch-head` (number + `h2`) | section unit; header kept with its content, never orphaned |
| `.cols` (**single-column stacked** grid: charts on top, note below) | forced to 1 column in print — **never left-right** |
| `<div class="col-chart">` + `.col` w/ `<i data-h="N">` | vertical-column chart; reveal script sets `i.style.height` from `data-h` (mirrors `.bar i[data-w]`) — must be present or columns render flat in print |
| `.linechart svg` / `.donut-chart svg` | line & donut charts are **static SVG** (final values baked in); they need no data attr, only the `.rv` wrapper to fade in — they render 1:1 in print |
| `.bar.div` (diverging) holds `.track` spans + `<i data-w>` (and `<i class="neg" data-w>` for left) | signed bars around a centre axis; the `<i data-w>` still drives fill width |
| `.stats .cell` (now a **light card**), `.note`, `.note p`, `.pq`, `.legend`, `.donut-legend`, `.col-chart`, `.linechart`, `.donut-chart`, `.act`, `.deck`, `.note .fig` | every text block / chart kept intact across page breaks (no split mid-page) |
| ~~`.bignum`~~ / ~~`.waffle`~~ (DEPRECATED) | brand review 2026-06 retired both — use `.note .fig` inline figure instead of billboard `.bignum`; use `.bar-row` progress bars instead of `.waffle` grid. CSS kept for back-compat only; preflight WARNs if used |
| `footer` (dark colophon block at the end) | kept intact; source/disclaimer at **10px** (small, muted — not body size) |

### Design rules (updated per brand review 2026-06-18)

0. **4-COLOUR SEMANTIC SYSTEM (the governing rule).** Colour encodes data; it never decorates. There
   are exactly four data roles, defined as `:root` vars:
   - `--brand` **#FF5A5F** (uhomes 品牌色) — structural accents: logo, chapter numbers, h1 accent,
     note border, AND **the one highlighted/subject bar** in any comparison chart.
   - `--up` (增长绿) — positive / rising values only.
   - `--down` **#c8102e** (下降红, deeper than brand) — negative / falling values only.
   - `--data` (普通数据灰) — the DEFAULT fill for every non-highlighted bar/column/slice.
   Charts default to `--data`; you opt into meaning with row keys `hl` (→brand), `up` (→green),
   `neg` (→red, auto when value<0). The legacy positional classes `style:"coral"/"sand"/"ink"` are
   DEPRECATED — preflight `bar-color-discipline` WARNs on them. The whole point: a reader must be able
   to tell what a colour MEANS. (Origin: the positional green/amber/red/ink rainbow carried no meaning
   and brand flagged it as "colours are confusing, nobody knows what they represent.")
1. **Light cards, not a heavy box.** The stat strip is now light cards (soft white fill, `border-radius`,
   hairline `var(--line)` border, `gap`) — approved 2026-06-18. The earlier "no boxes at all" rule was
   about the *heavy 2px segmented* strip that read as chopped-up and broke across pages; that is still
   banned. A clean light card with `break-inside:avoid` is fine and is what brand asked for.
2. **Stacked, not side-by-side.** `.cols` is a single column: each exhibit is a full-width chart
   followed by its note **below** it. No left-chart / right-note two-column layout.
3. **Footer fine print is small.** Source + disclaimer in `footer p` at ~10px, muted color —
   it is a colophon, not body copy.
4. **Every text block is atomic across pages.** `.note`, `.note p`, `.bignum`, `.pq`, `.act`,
   `.deck`, stat cells carry `break-inside:avoid` so a paragraph never splits across a page.
5. **No billboard numbers next to a chart that already shows them.** A 100px `.bignum` beside a
   bar chart of the same data reads as abrupt and redundant. Integrate the figure as a moderate
   inline lead (`.note .fig`, ~26–38px coral) inside the note instead. Reserve big numbers for a
   page with no competing chart.
6. **Stat cards = icon badge + semantic colour (designer mockup, 2026-06-18).** Each `.stats .cell`
   renders: a coloured **circular icon badge** (`.ic`), the big number, a bold title (`.cap` ← `span`),
   and a muted subtitle (`.sub` ← `sub`). Colour is SEMANTIC by sign: leading `+` → `--up` green
   `.pos`, leading `−`/`-` → `--down` red `.neg`, **unsigned** → neutral ink (the old `nth-child`
   positional rainbow was REMOVED — it was the meaningless-colour problem). The badge glyph auto-picks
   `up`/`down`/`bars` by tone; override with `"icon":"up|down|bars|globe|flat"`. Override colour with
   `"tone":"pos"|"neg"|"neutral"` — e.g. a *bad absolute* stat like a rank `#17` (no sign) → `"neg"`
   to render it red, matching the mockup. A trailing `%` is auto-wrapped in `.u` (shrunk unit).
   **Never mix a signed delta with a bare ratio in the same strip** — rewrite `"7 / 8"` as a big count
   `"7"` with the denominator in the subtitle, else the fraction reads ambiguously next to `+9.3 / −5.6`.
7. **Leading +/− is auto-wrapped in `<span class="sgn">`** and rendered as a small raised affix
   (`.neg .sgn` shrinks harder). Montserrat draws U+2212 as a wide bar that visually outweighs the
   compact `+`; the affix balances the pair. Automatic — keep using the real minus `−` (U+2212), not
   a hyphen, in JSON.

### Chart variants (added 2026-06-18 — pick the form that fits the question)

A `chart` block takes an optional `"variant"` (default `"bar"`). Match the chart type to what the
exhibit is arguing — brand review called out using horizontal bars for everything:

| variant | use for | data shape | colour |
|---|---|---|---|
| `"line"` | a **trend** over time | `bars:[{label,value,hl?,down?,up?}]` (ordered points) | ink line + faint brand area; per-point dot — `hl`=brand, `down`=red, `up`=green, else neutral |
| `"donut"` (alias `"pie"`) | a **share / proportion** | `bars:[{label,value,hl?,up?,down?}]`; optional `center:{value,label}` | highlighted slice=brand, `up`/`down` tint a slice green/red, rest=neutral greys |
| `"column"` | a **time comparison** (few periods) | `bars:[{label,value,hl?/up?/down?}]` | default grey + ONE `hl` (subject) — "全灰，只突出一条红色" |
| `"bar"` (default) | a **ranking** | `bars:[…]` with `mode` scale/percent/raw_w | default grey + ONE `hl`; legacy `style` deprecated |
| `"bar"` + `"diverging":true` | a ranking **with negatives** | `bars:[{label,value (signed numeric),value_text}]` | + right (grey/`hl`), − **left in `--down` red** around a centre axis |

Diverging requires real numeric `value` (it computes left/right from `max(|value|)`); use `value_text`
for the printed label (`"+101%"`, `"−16%"`). The earlier behaviour (zeroing a negative bar to width 0)
HID the decline — diverging is the fix for "negatives must show". Column charts reveal via `<i data-h>`
(the build scripts force height the same way they force `.bar i[data-w]` width); line/donut are static
SVG. Worked examples: the Cardiff report — 01 line, 02 donut, 03 column, 04 bar, 05 diverging.

### Logo strategy

**Primary rule — by language** (handled automatically by `build_report.py`, no config needed):

| Version | `.topbar` logo |
|---|---|
| **EN** report (`lang: "en"`) | **uhomes.com wordmark ONLY** (`assets/uhomes-logo-red.svg`) |
| **CN** report (`lang: "cn"`) | **3-brand combined logo 异乡好居 ｜ 异乡缴费 ｜ 异乡人才** — single official asset `assets/uhomes-cn-combined-logo.svg` (`.logo-combined`, height 26px, wide ~13:1) |

The generator picks this from `lang`; leave `content.topbar` with just `issue` (no `logo_src`).

**Override — by report type** (set `content.topbar.logo_src` — plus optional `logo_alt` for its
alt text — or `logo_html` to override the rule; for single-school / property reports the footer
corner mark stays uhomes):
- **University** deep-dive → that university's logo (`logo_src`) + "× uhomes".
- **Apartment / property** → that apartment brand's logo + "× uhomes".

`.topbar` stays visible in print (unlike `.masthead`). The CDP running header (thin text
title/brand) still repeats on interior pages for continuity. Assets: `uhomes-logo-red.svg`
(uhomes.com), `uhomes-cn-combined-logo.svg` (三品牌组合标), + white variants for dark backgrounds.

**Wordmark sizing (do not "fix" by inflating the box).** `uhomes-logo-red.svg` is **tight-cropped**
(`viewBox="98 214 1404 172"`) — the original Adobe export had `viewBox="0 0 1600 600"` with ~74%
vertical whitespace, so at `height:34px` the visible ink was only ~7px (smaller than the 11px issue
text). The EN wordmark therefore renders with class `logo logo-uhomes` sized `height:18px`; generic
`.logo` stays `34px` for square / custom single-image logos (`logo_src`). If a wordmark looks tiny,
the fix is **crop the SVG viewBox to the ink bounds**, not bump the CSS height (which just adds dead
space). ⚠️ The white variant `uhomes-logo-white.svg` still has the old padding — crop its viewBox the
same way before using it as a topbar wordmark.

Design system: brand fonts (阿里普惠体 / Montserrat via `@font-face` + Google Fonts `@import`);
warm paper palette; numbered chapters; each exhibit has a title (`.ct`/`.cn2`) + source line.
**Canonical worked example: the Cardiff report** (`~/Projects/uhomes-insights/cardiff-2026/
cardiff-insight-2026-*.html`) — it embodies all the rules above. (The older Sydney report predates
the stacked/de-boxed redesign.)

## PDF pipeline (Stage 5)

### Config schema

```json
{
  "watermark": "Pro.uhomes.com",          // "" to disable; tiled diagonal text
  "logo": "assets/uhomes-logo-red.svg",    // optional; footer corner mark; default = skill's red wordmark (build_pdf only)
  "watermark_logo": "assets/uhomes-logo-red.svg", // optional; EN watermark logo; default = uhomes.com wordmark
  "width": 1200,                           // optional; long-image viewport CSS px (build_longimage only)
  "scale": 2,                              // optional; long-PNG device pixel ratio (build_longimage only)
  "reports": [
    { "src": "report-cn.html",             // input HTML (both scripts)
      "out": "Report-CN.pdf",              // A4 PDF output (build_pdf only)
      "title": "<header left>", "brand": "<header right>",   // running header (build_pdf only)
      "long": "custom-long.png", "longpdf": "custom-long.pdf" } // optional name overrides (build_longimage only)
  ]
}
```

One config drives both scripts; each reads its own keys (annotated above) and ignores the rest.
Long outputs default to `<src-stem>-long.png/pdf` in the config dir. Paths resolve relative to
the config file's directory. Run:
`python3 <skill>/scripts/build_pdf.py report.config.json`

**Watermark is language-aware** (brand request 2026-06, both `build_pdf.py` and `build_longimage.py`):
- **EN report** (`<html lang="en">`) → tile = the **uhomes.com English wordmark** (`watermark_logo`,
  faint ~8.5% opacity) **above** the `watermark` url text — i.e. "English logo + pro.uhomes.com".
- **CN report** (any non-`en` lang) → tile = **text-only** (`watermark` string), no logo.

Detection is automatic from the HTML `lang` attr (double/single/unquoted accepted, scanned in the
first 4000 chars); no per-report config needed. Override the watermark logo via the top-level
`watermark_logo` key. ⚠️ A stale `head.lang_attr` in the content JSON (e.g. `zh-CN` left in an EN
copy) defeats this — leave `lang_attr` out and let `lang` derive it.

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
- Shared plumbing (watermark SVG, lang detection, Chrome/CDP session, escaping, brand-font check)
  lives in `scripts/_pdfcommon.py` — both build scripts import it; edit watermark/lang behaviour
  there once. The scripts print a `WARN` when the CDN brand fonts fail to load (offline builds
  silently fell back to system fonts before).
- The script launches headless Chrome with `--remote-debugging-port=9333`; if a stale instance
  lingers, `pkill -f "remote-debugging-port=9333"` before re-running.
- It waits 4s after load for web fonts (PuHuiTi/Montserrat) to settle — networked fonts need this.
- `websockets.connect(max_size=None)` is required: printToPDF returns multi-MB base64.
- **Always verify visually**: `pdftoppm -png -r 90 out.pdf /tmp/p` then inspect page boundaries —
  page count alone hides collisions, orphan headers, and split bars.

## Push & archive

- Report file: `docs/ANALYSIS_YYYY-MM-DD_<topic>.md` with credibility disclaimer + `[已核实]`
  annotations; update the README report index.
- Lark push: `--as bot` (dingning.ai) unless the user asks for personal identity.

### Feishu delivery (长图/长 PDF into a Wiki doc)

- `feishu-wiki/push.py <md>` imports a Markdown report → a Wiki **docx**. **CAUTION: md import does
  NOT carry local images/attachments** — a `![](local.png)` will not appear. The pushed doc is
  text/tables only.
- To put the 长图 cover + 长 PDF attachment INTO the Wiki doc, after pushing run:
  ```bash
  python3 ~/.claude/skills/feishu-wiki/push.py --embed <wiki_url> --image <cover-long.png> --file <report-long.pdf>
  ```
  It inserts a docx image block (top) + file block via the docx blocks API.
- **Requires the app to have `docx:document` (user-identity) scope.** Without it `--embed` fails
  gracefully with the fix steps (open scope → republish → `--login` re-auth). `push.py --status`
  now预检 this scope and reports "图片嵌入能力 ✓/✗". If unavailable, fall back to dragging the
  files into the doc by hand, or deliver the 长图/长 PDF via Lark IM (first-class file upload).
