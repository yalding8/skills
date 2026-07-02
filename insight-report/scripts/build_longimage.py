#!/usr/bin/env python3
"""Render a magazine-style HTML insight report to ONE continuous long PNG (长图).

This is the "long version" — a single tall, scroll-style image with NO A4 pagination,
no running header/footer, no page breaks or per-page whitespace. Best for sharing
(WeChat / Feishu / social) where readers scroll a single column.

Usage:
    python3 build_longimage.py report.config.json

Reuses the same report.config.json as build_pdf.py. For each report it emits BOTH
<src-basename>-long.png and <src-basename>-long.pdf, written into the CONFIG file's
directory (same base all config paths resolve against; preflight looks there too).
Optional config keys:
    "width":   1200      // CSS px of the magazine column viewport (default 1200)
    "scale":   2         // device pixel ratio for the PNG (default 2 = retina)
    "watermark": "Pro.uhomes.com"   // tiled diagonal watermark; "" disables
    "watermark_logo": "...svg"      // EN watermark logo override (default uhomes.com wordmark)
Per-report override keys (rarely needed):
    "long":    "custom-name.png"    // long-PNG output name (default <src-stem>-long.png)
    "longpdf": "custom-name.pdf"    // long-PDF output name (default <src-stem>-long.pdf)

Same hard-won contract as the PDF pipeline: the HTML must use `.rv` reveal blocks and
`.bar i[data-w]` bars; an injected script forces them to their final state so the static
capture renders fully. The visible page-1 lockup is `.topbar`; the legacy `.masthead`
brand bar is hidden here exactly as in print (it has no replacement in the long image,
so legacy masthead-only reports should migrate to `.topbar`).

Shared plumbing (watermark, lang detection, Chrome/CDP session, font check) lives in
scripts/_pdfcommon.py — edit it there, both build scripts pick it up.
"""
import asyncio
import base64
import json
import os
import sys
import urllib.parse

import websockets

from _pdfcommon import (SKILL_DIR, REVEAL_JS, close_chrome, close_tab, cdp_cmd,
                        data_uri_svg, is_en, launch_chrome, new_tab, wait_chrome_up,
                        wait_load, warn_if_fonts_missing, watermark_uri)

PORT = 9334  # distinct from build_pdf's 9333 so both can run


def inject(html, watermark_text, wm_logo_uri=None):
    wm_css = ""
    wm_div = ""
    if watermark_text:
        logo_for_wm = wm_logo_uri if is_en(html) else None  # EN watermark = logo + url
        uri, tw, th = watermark_uri(watermark_text, logo_for_wm)
        wm_css = (
            "#wm-long{position:absolute;top:0;left:0;width:100%;z-index:9999;"
            f"pointer-events:none;background-repeat:repeat;background-size:{tw}px {th}px;"
            f'background-image:url("{uri}")}}'
        )
        wm_div = '<div id="wm-long" aria-hidden="true"></div>'
    head = (
        "<style id='long-overrides'>"
        ".rv{opacity:1 !important;transform:none !important;transition:none !important}"
        ".bar i,.col i{transition:none !important}"
        ".masthead{display:none !important}"
        f"{wm_css}</style>"
    )
    body = (
        f"{wm_div}<script>"
        f"{REVEAL_JS}"
        "window.addEventListener('load',function(){var w=document.getElementById('wm-long');"
        "if(w){w.style.height=document.documentElement.scrollHeight+'px';}});"
        "</script>"
    )
    html = html.replace("</head>", head + "</head>", 1)
    html = html.replace("</body>", body + "</body>", 1)
    return html


def prepare(src_path, watermark_text, wm_logo_uri=None):
    with open(src_path, "r", encoding="utf-8") as f:
        html = inject(f.read(), watermark_text, wm_logo_uri)
    tmp = src_path + ".long.tmp.html"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(html)
    return tmp, "file://" + urllib.parse.quote(tmp)


async def _render_one(ws, url, out_png, out_pdf, width, scale):
    await cdp_cmd(ws, 1, "Page.enable")
    await cdp_cmd(ws, 5, "Emulation.setDeviceMetricsOverride",
                  {"width": width, "height": 1200, "deviceScaleFactor": scale, "mobile": False})
    await wait_load(ws, url)
    await asyncio.sleep(4.0)  # web fonts settle
    await warn_if_fonts_missing(ws, 8, os.path.basename(out_png))
    metrics = await cdp_cmd(ws, 6, "Page.getLayoutMetrics")
    size = metrics.get("cssContentSize") or metrics.get("contentSize")
    height = int(size["height"]) + 2
    # (a) continuous long PNG
    res = await cdp_cmd(ws, 3, "Page.captureScreenshot", {
        "format": "png", "captureBeyondViewport": True,
        "clip": {"x": 0, "y": 0, "width": width, "height": height, "scale": 1},
    })
    with open(out_png, "wb") as f:
        f.write(base64.b64decode(res["data"]))
    # (b) continuous long PDF — ONE tall page (no A4 pagination, no header/footer)
    pdf = await cdp_cmd(ws, 7, "Page.printToPDF", {
        "printBackground": True, "displayHeaderFooter": False, "preferCSSPageSize": False,
        "paperWidth": width / 96.0, "paperHeight": height / 96.0,
        "marginTop": 0, "marginBottom": 0, "marginLeft": 0, "marginRight": 0, "scale": 1,
    })
    with open(out_pdf, "wb") as f:
        f.write(base64.b64decode(pdf["data"]))
    return height


async def _run(jobs, width, scale):
    proc = launch_chrome(PORT, "cdp-long-")
    try:
        await wait_chrome_up(proc, PORT)
        for out_png, out_pdf, url in jobs:
            tab = new_tab(PORT)
            try:
                async with websockets.connect(tab["webSocketDebuggerUrl"], max_size=None) as ws:
                    h = await _render_one(ws, url, out_png, out_pdf, width, scale)
                print(f"OK  -> {out_png}  ({os.path.getsize(out_png)//1024} KB, {width}x{h}css @{scale}x)")
                print(f"OK  -> {out_pdf}  ({os.path.getsize(out_pdf)//1024} KB, single {width}x{h}css page)")
            finally:
                close_tab(PORT, tab["id"])
    finally:
        close_chrome(proc)


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: build_longimage.py <config.json>")
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
    width = int(cfg.get("width", 1200))
    scale = int(cfg.get("scale", 2))
    wm_logo_path = cfg.get("watermark_logo")
    wm_logo_path = os.path.join(base, wm_logo_path) if wm_logo_path else \
        os.path.join(SKILL_DIR, "assets", "uhomes-logo-red.svg")
    wm_logo_uri = data_uri_svg(wm_logo_path)

    jobs, tmps = [], []
    for r in cfg.get("reports", []):
        src = os.path.join(base, r["src"])
        if not os.path.isfile(src):
            sys.exit(f"ERROR: src HTML not found: {src}")
        stem = os.path.splitext(os.path.basename(r["src"]))[0]
        out_png = os.path.join(base, r.get("long", stem + "-long.png"))
        out_pdf = os.path.join(base, r.get("longpdf", stem + "-long.pdf"))
        tmp, url = prepare(src, watermark, wm_logo_uri)
        tmps.append(tmp)
        jobs.append((out_png, out_pdf, url))
    if not jobs:
        sys.exit("ERROR: config has no reports[]")
    try:
        asyncio.run(_run(jobs, width, scale))
    finally:
        for t in tmps:
            if os.path.exists(t):
                os.remove(t)


if __name__ == "__main__":
    main()
