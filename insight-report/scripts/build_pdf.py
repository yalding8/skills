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

Requires: macOS Google Chrome + Python `websockets` (pip install websockets).
"""
import asyncio
import base64
import json
import os
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request

import websockets

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 9333

# --- print geometry (inches) — slim header/footer bands top & bottom ---
PAPER_W, PAPER_H = 8.27, 11.69          # A4
M_TOP, M_BOTTOM, M_SIDE = 0.5, 0.5, 0.47
PAD = "47px"                            # ~12mm side inset so header/footer rules align with body
FONT = "'Helvetica Neue', Arial, 'PingFang SC', 'Microsoft YaHei', sans-serif"
RULE = "#ccbfa8"
MUTE = "#7c8a90"


def data_uri_svg(path):
    with open(path, "rb") as f:
        return "data:image/svg+xml;base64," + base64.b64encode(f.read()).decode("ascii")


def _is_en(html):
    import re
    m = re.search(r'<html[^>]*\blang="([^"]+)"', html[:1000], re.I)
    return bool(m) and m.group(1).lower().startswith("en")


def watermark_uri(text, logo_uri=None):
    """Tiled diagonal watermark. Returns (data_uri, tile_w, tile_h).

    EN variant (logo_uri given) = the uhomes.com wordmark above the url text
    (brand request 2026-06: EN watermark = English logo + pro.uhomes.com).
    Default = text-only tile (used for CN)."""
    if logo_uri:
        # logo wordmark (viewBox 1600x600 ≈ 2.67:1) faint, with url text below
        svg = (
            "<svg xmlns='http://www.w3.org/2000/svg' "
            "xmlns:xlink='http://www.w3.org/1999/xlink' width='360' height='230'>"
            "<g transform='rotate(-28 180 115)' opacity='0.085'>"
            f"<image xlink:href='{logo_uri}' x='66' y='62' width='168' height='63'/>"
            f"<text x='86' y='150' font-family='Montserrat, Helvetica, Arial, sans-serif' "
            f"font-size='16' font-weight='600' fill='#1f5d7a' letter-spacing='1'>{text}</text>"
            "</g></svg>"
        )
        return "data:image/svg+xml," + urllib.parse.quote(svg), 360, 230
    svg = (
        "<svg xmlns='http://www.w3.org/2000/svg' width='340' height='200'>"
        "<text x='10' y='120' transform='rotate(-28 170 100)' "
        "font-family='Montserrat, Helvetica, Arial, sans-serif' font-size='24' "
        f"font-weight='600' fill='#1f5d7a' fill-opacity='0.075' letter-spacing='1'>{text}</text></svg>"
    )
    return "data:image/svg+xml," + urllib.parse.quote(svg), 340, 200


def header_tpl(title, brand):
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
  .note,.note p,.bignum,.pq,.waffle,.legend,.act,.stats .cell,.ch-head p.sub,.deck{{break-inside:avoid}}
  .chart .ct,.chart .cn2{{break-after:avoid}}
  .ch-head{{break-after:avoid;break-inside:avoid}}
  h1,h2,h3,h4{{break-after:avoid}}
}}
{wm}
</style>
"""


BODY_INJECT = """
<div id="wm-pro" aria-hidden="true"></div>
<script>
(function(){
  document.querySelectorAll('.rv').forEach(function(el){el.classList.add('on');});
  document.querySelectorAll('.bar i').forEach(function(b){
    if(b.dataset && b.dataset.w){b.style.width=b.dataset.w+'%';}
  });
})();
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
    logo_for_wm = wm_logo_uri if _is_en(html) else None  # EN watermark = logo + url
    html = html.replace("</head>", head_inject(watermark_text, logo_for_wm) + "</head>", 1)
    html = html.replace("</body>", BODY_INJECT + "</body>", 1)
    tmp = src_path + ".print.tmp.html"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(html)
    return tmp, "file://" + urllib.parse.quote(tmp)


async def _cmd(ws, _id, method, params=None):
    await ws.send(json.dumps({"id": _id, "method": method, "params": params or {}}))
    while True:
        m = json.loads(await ws.recv())
        if m.get("id") == _id:
            if "error" in m:
                raise RuntimeError(f"{method}: {m['error']}")
            return m.get("result", {})


async def _render_one(ws, url, out_path, params):
    await _cmd(ws, 1, "Page.enable")
    await ws.send(json.dumps({"id": 2, "method": "Page.navigate", "params": {"url": url}}))
    while True:
        m = json.loads(await ws.recv())
        if m.get("method") == "Page.loadEventFired":
            break
    await asyncio.sleep(4.0)  # let web fonts settle
    res = await _cmd(ws, 3, "Page.printToPDF", params)
    with open(out_path, "wb") as f:
        f.write(base64.b64decode(res["data"]))


def _new_tab():
    req = urllib.request.Request(f"http://127.0.0.1:{PORT}/json/new?about:blank", method="PUT")
    return json.loads(urllib.request.urlopen(req, timeout=10).read())


def _close_tab(tid):
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/close/{tid}", timeout=10).read()
    except Exception:
        pass


async def _run(jobs):
    udd = tempfile.mkdtemp(prefix="cdp-chrome-")
    proc = subprocess.Popen(
        [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox", "--no-first-run",
         "--no-default-browser-check", f"--remote-debugging-port={PORT}",
         "--remote-allow-origins=*", f"--user-data-dir={udd}", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        for _ in range(100):
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=1).read()
                break
            except Exception:
                await asyncio.sleep(0.1)
        for out_path, url, params in jobs:
            tab = _new_tab()
            try:
                async with websockets.connect(tab["webSocketDebuggerUrl"], max_size=None) as ws:
                    await _render_one(ws, url, out_path, params)
                print(f"OK  -> {out_path}  ({os.path.getsize(out_path) // 1024} KB)")
            finally:
                _close_tab(tab["id"])
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except Exception:
            proc.kill()


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: build_pdf.py <config.json>")
    cfg_path = os.path.abspath(sys.argv[1])
    base = os.path.dirname(cfg_path)
    with open(cfg_path, encoding="utf-8") as f:
        cfg = json.load(f)

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
    for r in cfg["reports"]:
        src = os.path.join(base, r["src"])
        out = os.path.join(base, r["out"])
        tmp, url = prepare(src, watermark, wm_logo_uri)
        tmps.append(tmp)
        jobs.append((out, url, pdf_params(r, logo_uri)))
    try:
        asyncio.run(_run(jobs))
    finally:
        for t in tmps:
            if os.path.exists(t):
                os.remove(t)


if __name__ == "__main__":
    main()
