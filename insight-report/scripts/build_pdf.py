#!/usr/bin/env python3
"""Render magazine-style HTML insight reports to watermarked, print-ready PDFs.

Config-driven, reusable across reports. Usage:

    python3 build_pdf.py report.config.json

Config schema (paths are resolved relative to the config file's directory):

    {
      "watermark": "Pro.uhomes.com",          // optional; "" disables the watermark
      "watermark_logo": "assets/...svg",       // optional; EN watermark logo (default uhomes.com)
      "logo": "assets/uhomes-logo-red.svg",    // optional; default = this skill's red wordmark
      "reports": [
        {
          "src":   "report-cn.html",           // input HTML (required)
          "out":   "Report-CN.pdf",            // output PDF (required)
          "title": "悉尼留学市场观察 · 2026",   // running-header left  (report title)
          "brand": "异乡好居　渠道调研洞察"      // running-header right (brand / series)
        },
        { "src": "report-en.html", "out": "Report-EN.pdf",
          "title": "Sydney Student Housing Market · 2026", "brand": "uhomes.com　Channel Insights" }
      ]
    }

HARD-WON DESIGN DECISIONS baked in (do not "simplify" away):
- Header/footer are rendered via Chrome DevTools Protocol footerTemplate/headerTemplate,
  NOT a CSS position:fixed bar. Chrome CLIPS fixed elements to the content box, so a fixed
  footer either collides with body text or vanishes off-page. CDP templates live in the
  reserved page MARGIN and reserve their own space -> never collide.
- Footer logo is a SMALL bottom-LEFT corner mark (a quiet brand mark, not a centered banner)
  + page numbers bottom-right. Running HEADER on every page (title left / brand right) gives
  cross-page continuity so interior pages aren't naked.
- Flow layout (continuous), NOT one-section-per-page: sections of unequal length would leave
  big ragged whitespace if each got its own page. Break rules keep single bars / section
  titles intact (never split mid-bar, never orphan a heading) without forcing whole charts
  atomic (which orphans the tail into a near-empty closing page).
- The HTML must use the reveal/animation contract (see REFERENCE.md): every animated block
  has class `rv`; every animated bar is `.bar i[data-w="N"]`. An injected script forces them
  to their final state so the static PDF renders fully.

Shared plumbing (watermark, lang detection, Chrome/CDP session, font check) lives in
scripts/_pdfcommon.py — edit it there, both build scripts pick it up.

Requires: macOS Google Chrome + Python `websockets` (pip install websockets).
"""
import asyncio
import base64
import json
import os
import sys
import urllib.parse

import websockets

from _pdfcommon import (SKILL_DIR, REVEAL_JS, close_chrome, close_tab, cdp_cmd,
                        data_uri_svg, esc, is_en, launch_chrome, new_tab,
                        wait_chrome_up, wait_load, warn_if_fonts_missing, watermark_uri)

PORT = 9333

# --- print geometry (inches) — slim header/footer bands top & bottom ---
PAPER_W, PAPER_H = 8.27, 11.69          # A4
M_TOP, M_BOTTOM, M_SIDE = 0.5, 0.5, 0.47
PAD = "47px"                            # ~12mm side inset so header/footer rules align with body
FONT = "'Helvetica Neue', Arial, 'PingFang SC', 'Microsoft YaHei', sans-serif"
RULE = "#ccbfa8"
MUTE = "#7c8a90"


def header_tpl(title, brand):
    title, brand = esc(title), esc(brand)
    return (
        f'<div style="width:100%;box-sizing:border-box;padding:0 {PAD};font-family:{FONT};'
        f'-webkit-print-color-adjust:exact;">'
        f'<div style="border-bottom:0.75px solid {RULE};padding-bottom:5px;position:relative;'
        f'font-size:7.5px;letter-spacing:0.6px;color:{MUTE};">'
        f'<span style="font-weight:600;">{title}</span>'
        f'<span style="position:absolute;right:0;top:0;">{brand}</span>'
        "</div></div>"
    )


def footer_tpl(logo_uri):
    return (
        f'<div style="width:100%;box-sizing:border-box;padding:0 {PAD};font-family:{FONT};'
        f'-webkit-print-color-adjust:exact;">'
        f'<div style="border-top:0.75px solid {RULE};padding-top:6px;position:relative;height:16px;">'
        f'<img src="{logo_uri}" style="height:13px;width:auto;position:absolute;left:0;top:6px;">'
        f'<span style="position:absolute;right:0;top:7px;font-size:7.5px;letter-spacing:1px;color:{MUTE};">'
        '<span class="pageNumber"></span>&nbsp;/&nbsp;<span class="totalPages"></span></span>'
        "</div></div>"
    )


def head_inject(watermark_text, wm_logo_uri=None):
    wm = ""
    if watermark_text:
        uri, tw, th = watermark_uri(watermark_text, wm_logo_uri)
        wm = (
            f'#wm-pro{{position:fixed;inset:0;z-index:9999;pointer-events:none;'
            f'background-image:url("{uri}");'
            f"background-repeat:repeat;background-size:{tw}px {th}px}}"
        )
    return f"""
<style id="pdf-overrides">
.rv{{opacity:1 !important;transform:none !important;transition:none !important}}
.bar i,.col i{{transition:none !important}}
.masthead{{display:none !important}}   /* CDP running header replaces the page-1 masthead */
@media print{{
  html,body{{-webkit-print-color-adjust:exact;print-color-adjust:exact;background:var(--paper) !important}}
  body{{font-size:14.5px !important;line-height:1.64 !important}}
  .hero{{padding:6px 0 14px !important}}
  section.ch{{padding:18px 0 !important;break-inside:auto}}
  .stats{{margin:16px 0 18px !important}}
  .pq{{margin:16px auto !important}} .pq blockquote{{font-size:19px !important}}
  .acts .act{{padding:9px 0 !important}} .act h3{{margin-bottom:4px !important}}
  footer{{margin-top:8px !important;padding:22px 0 !important;break-inside:avoid}}
  footer p{{margin-top:8px !important;font-size:10px !important;line-height:1.7 !important}}
  /* stacked layout: charts on top, note below (no left-right split) */
  .cols{{grid-template-columns:1fr !important;gap:22px !important}}
  .stats{{grid-template-columns:repeat(4,1fr) !important}}
  .hero .meta{{grid-template-columns:repeat(4,1fr) !important}}
  /* flow cross-page handling: never split a bar mid-row, never orphan a heading,
     keep every text block (note/paragraph/card) intact across page breaks */
  .bar-row{{break-inside:avoid}}
  /* new chart variants are atomic units — never split a column chart / line / donut across pages */
  .col-chart,.linechart,.donut-chart{{break-inside:avoid}}
  .note,.note p,.bignum,.pq,.waffle,.legend,.donut-legend,.act,.stats .cell,.ch-head p.sub,.deck{{break-inside:avoid}}
  .chart .ct,.chart .cn2{{break-after:avoid}}
  .ch-head{{break-after:avoid;break-inside:avoid}}
  h1,h2,h3,h4{{break-after:avoid}}
}}
{wm}
</style>
"""


BODY_INJECT = f"""
<div id="wm-pro" aria-hidden="true"></div>
<script>
(function(){{{REVEAL_JS}}})();
</script>
"""


def pdf_params(meta, logo_uri):
    return {
        "printBackground": True, "displayHeaderFooter": True,
        "headerTemplate": header_tpl(meta.get("title", ""), meta.get("brand", "")),
        "footerTemplate": footer_tpl(logo_uri),
        "paperWidth": PAPER_W, "paperHeight": PAPER_H,
        "marginTop": M_TOP, "marginBottom": M_BOTTOM, "marginLeft": M_SIDE, "marginRight": M_SIDE,
        "preferCSSPageSize": False, "scale": 1,
    }


def prepare(src_path, watermark_text, wm_logo_uri=None):
    with open(src_path, "r", encoding="utf-8") as f:
        html = f.read()
    logo_for_wm = wm_logo_uri if is_en(html) else None  # EN watermark = logo + url
    html = html.replace("</head>", head_inject(watermark_text, logo_for_wm) + "</head>", 1)
    html = html.replace("</body>", BODY_INJECT + "</body>", 1)
    tmp = src_path + ".print.tmp.html"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(html)
    return tmp, "file://" + urllib.parse.quote(tmp)


async def _render_one(ws, url, out_path, params):
    await cdp_cmd(ws, 1, "Page.enable")
    await wait_load(ws, url)
    await asyncio.sleep(4.0)  # let web fonts settle
    await warn_if_fonts_missing(ws, 8, os.path.basename(out_path))
    res = await cdp_cmd(ws, 3, "Page.printToPDF", params)
    with open(out_path, "wb") as f:
        f.write(base64.b64decode(res["data"]))


async def _run(jobs):
    proc = launch_chrome(PORT, "cdp-chrome-")
    try:
        await wait_chrome_up(proc, PORT)
        for out_path, url, params in jobs:
            tab = new_tab(PORT)
            try:
                async with websockets.connect(tab["webSocketDebuggerUrl"], max_size=None) as ws:
                    await _render_one(ws, url, out_path, params)
                print(f"OK  -> {out_path}  ({os.path.getsize(out_path) // 1024} KB)")
            finally:
                close_tab(PORT, tab["id"])
    finally:
        close_chrome(proc)


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: build_pdf.py <config.json>")
    cfg_path = os.path.abspath(sys.argv[1])
    base = os.path.dirname(cfg_path)
    try:
        with open(cfg_path, encoding="utf-8") as f:
            cfg = json.load(f)
    except FileNotFoundError:
        sys.exit(f"ERROR: config not found: {cfg_path}")
    except json.JSONDecodeError as e:
        sys.exit(f"ERROR: config is not valid JSON: {cfg_path} ({e})")

    watermark = cfg.get("watermark", "Pro.uhomes.com")
    logo_path = cfg.get("logo")
    logo_path = os.path.join(base, logo_path) if logo_path else \
        os.path.join(SKILL_DIR, "assets", "uhomes-logo-red.svg")
    logo_uri = data_uri_svg(logo_path)
    # watermark logo (EN only): uhomes.com English wordmark, faint + tiled
    wm_logo_path = cfg.get("watermark_logo")
    wm_logo_path = os.path.join(base, wm_logo_path) if wm_logo_path else \
        os.path.join(SKILL_DIR, "assets", "uhomes-logo-red.svg")
    wm_logo_uri = data_uri_svg(wm_logo_path)

    jobs, tmps = [], []
    for r in cfg.get("reports", []):
        src = os.path.join(base, r["src"])
        if not os.path.isfile(src):
            sys.exit(f"ERROR: src HTML not found: {src}")
        out = os.path.join(base, r["out"])
        tmp, url = prepare(src, watermark, wm_logo_uri)
        tmps.append(tmp)
        jobs.append((out, url, pdf_params(r, logo_uri)))
    if not jobs:
        sys.exit("ERROR: config has no reports[]")
    try:
        asyncio.run(_run(jobs))
    finally:
        for t in tmps:
            if os.path.exists(t):
                os.remove(t)


if __name__ == "__main__":
    main()
