#!/usr/bin/env python3
"""Shared plumbing for build_pdf.py / build_longimage.py.

Everything here used to be duplicated verbatim in both scripts (~100 lines), which is
exactly how the two watermark/lang implementations would eventually drift apart. Both
build scripts import from this module; edit watermark/lang/Chrome behaviour HERE only.

Contents:
- CHROME / SKILL_DIR constants
- data_uri_svg()          — embed an SVG file as a base64 data: URI
- is_en()                 — language detection from the <html lang> attribute
- watermark_uri()         — the tiled diagonal watermark SVG (EN logo+text / CN text-only)
- esc()                   — HTML/XML escaping for user-supplied strings (title/brand/watermark)
- REVEAL_JS               — forces .rv/.bar i[data-w]/.col i[data-h] to final state
- launch_chrome()/close_chrome()/new_tab()/close_tab() — headless-Chrome session helpers
  with FRIENDLY errors (missing Chrome binary, port not coming up) instead of raw tracebacks
- cdp_cmd()/wait_load()   — CDP request/response + load-event wait, both with timeouts
  (a hung navigation used to hang the script forever)
- warn_if_fonts_missing() — after the font-settle sleep, checks document.fonts for the
  brand faces (PuHuiTi/Montserrat) and prints a WARNING when the CDN didn't deliver them;
  silent fallback to system fonts used to be invisible.
"""
import asyncio
import base64
import html as _html
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def esc(s):
    """Escape &<>\" for safe interpolation into HTML templates / SVG text nodes.
    Unescaped user strings (a title containing '&' or '<') used to break the CDP
    header template or make the watermark SVG unparsable (watermark silently gone)."""
    return _html.escape(str(s), quote=True)


def data_uri_svg(path):
    with open(path, "rb") as f:
        return "data:image/svg+xml;base64," + base64.b64encode(f.read()).decode("ascii")


def is_en(html_text):
    """True if the report HTML declares an English lang. Reads the <html ... lang=...>
    attribute; accepts double/single/no quotes and scans the first 4000 chars (a long
    comment/preamble before <html> used to silently defeat the 1000-char window and
    give an EN report the CN text-only watermark)."""
    m = re.search(r"<html[^>]*\blang\s*=\s*[\"']?([A-Za-z-]+)", html_text[:4000], re.I)
    return bool(m) and m.group(1).lower().startswith("en")


def watermark_uri(text, logo_uri=None):
    """Tiled diagonal watermark. Returns (data_uri, tile_w, tile_h).

    EN variant (logo_uri given) = the uhomes.com wordmark above the url text
    (brand request 2026-06: EN watermark = English logo + pro.uhomes.com).
    Default = text-only tile (used for CN)."""
    text = esc(text)
    if logo_uri:
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


REVEAL_JS = (
    "document.querySelectorAll('.rv').forEach(function(e){e.classList.add('on');});"
    "document.querySelectorAll('.bar i').forEach(function(b){"
    "if(b.dataset&&b.dataset.w){b.style.width=b.dataset.w+'%';}});"
    "document.querySelectorAll('.col i').forEach(function(b){"
    "if(b.dataset&&b.dataset.h){b.style.height=b.dataset.h+'%';}});"
)


# ------------------------------------------------------------------ Chrome session

def launch_chrome(port, udd_prefix):
    """Start headless Chrome with a CDP port and wait for it to answer.
    Exits with a readable message when the binary is missing or the port never
    comes up (previously: 10s silent wait, then a bare URLError from _new_tab)."""
    if not os.path.exists(CHROME):
        sys.exit("ERROR: Google Chrome not found at {!r} — this pipeline renders via "
                 "headless Chrome (macOS). Install Chrome or fix the CHROME path in "
                 "scripts/_pdfcommon.py.".format(CHROME))
    udd = tempfile.mkdtemp(prefix=udd_prefix)
    proc = subprocess.Popen(
        [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox", "--no-first-run",
         "--no-default-browser-check", f"--remote-debugging-port={port}",
         "--remote-allow-origins=*", f"--user-data-dir={udd}", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    return proc


async def wait_chrome_up(proc, port, timeout_s=15):
    deadline = asyncio.get_event_loop().time() + timeout_s
    while asyncio.get_event_loop().time() < deadline:
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=1).read()
            return
        except Exception:
            await asyncio.sleep(0.1)
    close_chrome(proc)
    sys.exit("ERROR: headless Chrome did not come up on port {} within {}s. A stale "
             "instance may hold the port — try: pkill -f \"remote-debugging-port={}\""
             .format(port, timeout_s, port))


def close_chrome(proc):
    proc.terminate()
    try:
        proc.wait(timeout=10)
    except Exception:
        proc.kill()


def new_tab(port):
    req = urllib.request.Request(f"http://127.0.0.1:{port}/json/new?about:blank", method="PUT")
    return json.loads(urllib.request.urlopen(req, timeout=10).read())


def close_tab(port, tid):
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{port}/json/close/{tid}", timeout=10).read()
    except Exception:
        pass


# ------------------------------------------------------------------ CDP helpers

async def cdp_cmd(ws, _id, method, params=None, timeout_s=120):
    await ws.send(json.dumps({"id": _id, "method": method, "params": params or {}}))
    deadline = asyncio.get_event_loop().time() + timeout_s
    while True:
        remain = deadline - asyncio.get_event_loop().time()
        if remain <= 0:
            raise RuntimeError(f"{method}: no CDP response within {timeout_s}s")
        m = json.loads(await asyncio.wait_for(ws.recv(), timeout=remain))
        if m.get("id") == _id:
            if "error" in m:
                raise RuntimeError(f"{method}: {m['error']}")
            return m.get("result", {})


async def wait_load(ws, url, timeout_s=60):
    """Navigate and block until Page.loadEventFired — WITH a timeout. The unbounded
    recv loop this replaces hung the whole script forever on a stuck navigation."""
    await ws.send(json.dumps({"id": 2, "method": "Page.navigate", "params": {"url": url}}))
    deadline = asyncio.get_event_loop().time() + timeout_s
    while True:
        remain = deadline - asyncio.get_event_loop().time()
        if remain <= 0:
            raise RuntimeError(f"page load timed out after {timeout_s}s: {url}")
        m = json.loads(await asyncio.wait_for(ws.recv(), timeout=remain))
        if m.get("method") == "Page.loadEventFired":
            return


async def warn_if_fonts_missing(ws, _id, label):
    """After the font-settle sleep, verify the brand webfonts actually loaded.
    Fonts come from CDNs (Google Fonts / Aliyun OSS); offline they silently fall back
    to system faces and nobody notices until brand review does. Best-effort: any
    evaluation failure is ignored (never blocks the build)."""
    js = ("(function(){try{if(!document.fonts)return 'unknown';"
          "var ok=false;document.fonts.forEach(function(f){"
          "if(f.status==='loaded'&&/Montserrat|PuHuiTi/i.test(f.family))ok=true;});"
          "return ok?'ok':'missing';}catch(e){return 'unknown';}})()")
    try:
        res = await cdp_cmd(ws, _id, "Runtime.evaluate",
                            {"expression": js, "returnByValue": True}, timeout_s=10)
        if res.get("result", {}).get("value") == "missing":
            sys.stderr.write("WARN [{}]: brand webfonts (PuHuiTi/Montserrat) did NOT load "
                             "— CDN unreachable? Output uses system-font fallback; "
                             "re-run with network before shipping.\n".format(label))
    except Exception:
        pass
