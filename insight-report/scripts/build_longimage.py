#!/usr/bin/env python3
"""Render a magazine-style HTML insight report to ONE continuous long PNG (长图).

This is the "long version" — a single tall, scroll-style image with NO A4 pagination,
no running header/footer, no page breaks or per-page whitespace. Best for sharing
(WeChat / Feishu / social) where readers scroll a single column.

Usage:
    python3 build_longimage.py report.config.json

Reuses the same report.config.json as build_pdf.py. For each report it emits
<src-basename>-long.png next to the HTML. Optional config keys:
    "width":   1200      // CSS px of the magazine column viewport (default 1200)
    "scale":   2         // device pixel ratio for crispness (default 2 = retina)
    "watermark": "Pro.uhomes.com"   // tiled diagonal watermark; "" disables

Same hard-won contract as the PDF pipeline: the HTML must use `.rv` reveal blocks and
`.bar i[data-w]` bars; an injected script forces them to their final state so the static
capture renders fully. The page-1 `.topbar` logo stays visible (no masthead hiding here).
"""
import asyncio
import base64
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request

import websockets

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 9334  # distinct from build_pdf's 9333 so both can run


def watermark_uri(text):
    svg = (
        "<svg xmlns='http://www.w3.org/2000/svg' width='340' height='200'>"
        "<text x='10' y='120' transform='rotate(-28 170 100)' "
        "font-family='Montserrat, Helvetica, Arial, sans-serif' font-size='24' "
        f"font-weight='600' fill='#1f5d7a' fill-opacity='0.075' letter-spacing='1'>{text}</text></svg>"
    )
    return "data:image/svg+xml," + urllib.parse.quote(svg)


def inject(html, watermark_text):
    wm_css = ""
    wm_div = ""
    if watermark_text:
        wm_css = (
            "#wm-long{position:absolute;top:0;left:0;width:100%;z-index:9999;"
            "pointer-events:none;background-repeat:repeat;background-size:340px 200px;"
            f'background-image:url("{watermark_uri(watermark_text)}")}}'
        )
        wm_div = '<div id="wm-long" aria-hidden="true"></div>'
    head = (
        "<style id='long-overrides'>"
        ".rv{opacity:1 !important;transform:none !important;transition:none !important}"
        ".bar i{transition:none !important}"
        ".masthead{display:none !important}"
        f"{wm_css}</style>"
    )
    body = (
        f"{wm_div}<script>"
        "document.querySelectorAll('.rv').forEach(function(e){e.classList.add('on');});"
        "document.querySelectorAll('.bar i').forEach(function(b){"
        "if(b.dataset&&b.dataset.w){b.style.width=b.dataset.w+'%';}});"
        "window.addEventListener('load',function(){var w=document.getElementById('wm-long');"
        "if(w){w.style.height=document.documentElement.scrollHeight+'px';}});"
        "</script>"
    )
    html = html.replace("</head>", head + "</head>", 1)
    html = html.replace("</body>", body + "</body>", 1)
    return html


def prepare(src_path, watermark_text):
    with open(src_path, "r", encoding="utf-8") as f:
        html = inject(f.read(), watermark_text)
    tmp = src_path + ".long.tmp.html"
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


async def _render_one(ws, url, out_path, width, scale):
    await _cmd(ws, 1, "Page.enable")
    await _cmd(ws, 5, "Emulation.setDeviceMetricsOverride",
              {"width": width, "height": 1200, "deviceScaleFactor": scale, "mobile": False})
    await ws.send(json.dumps({"id": 2, "method": "Page.navigate", "params": {"url": url}}))
    while True:
        m = json.loads(await ws.recv())
        if m.get("method") == "Page.loadEventFired":
            break
    await asyncio.sleep(4.0)  # web fonts settle
    metrics = await _cmd(ws, 6, "Page.getLayoutMetrics")
    size = metrics.get("cssContentSize") or metrics.get("contentSize")
    height = int(size["height"]) + 2
    res = await _cmd(ws, 3, "Page.captureScreenshot", {
        "format": "png", "captureBeyondViewport": True,
        "clip": {"x": 0, "y": 0, "width": width, "height": height, "scale": 1},
    })
    with open(out_path, "wb") as f:
        f.write(base64.b64decode(res["data"]))
    return height


async def _run(jobs, width, scale):
    import tempfile
    udd = tempfile.mkdtemp(prefix="cdp-long-")
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
        for out_path, url in jobs:
            req = urllib.request.Request(f"http://127.0.0.1:{PORT}/json/new?about:blank", method="PUT")
            tab = json.loads(urllib.request.urlopen(req, timeout=10).read())
            try:
                async with websockets.connect(tab["webSocketDebuggerUrl"], max_size=None) as ws:
                    h = await _render_one(ws, url, out_path, width, scale)
                print(f"OK  -> {out_path}  ({os.path.getsize(out_path)//1024} KB, {width}x{h}css @{scale}x)")
            finally:
                try:
                    urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/close/{tab['id']}", timeout=10).read()
                except Exception:
                    pass
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except Exception:
            proc.kill()


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: build_longimage.py <config.json>")
    cfg_path = os.path.abspath(sys.argv[1])
    base = os.path.dirname(cfg_path)
    with open(cfg_path, encoding="utf-8") as f:
        cfg = json.load(f)
    watermark = cfg.get("watermark", "Pro.uhomes.com")
    width = int(cfg.get("width", 1200))
    scale = int(cfg.get("scale", 2))

    jobs, tmps = [], []
    for r in cfg["reports"]:
        src = os.path.join(base, r["src"])
        stem = os.path.splitext(os.path.basename(r["src"]))[0]
        out = os.path.join(base, r.get("long", stem + "-long.png"))
        tmp, url = prepare(src, watermark)
        tmps.append(tmp)
        jobs.append((out, url))
    try:
        asyncio.run(_run(jobs, width, scale))
    finally:
        for t in tmps:
            if os.path.exists(t):
                os.remove(t)


if __name__ == "__main__":
    main()
