#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
preflight.py — 出片前自检 (preflight lint) for insight-report HTML/PDF deliverables.

WHY THIS EXISTS
---------------
In the 2026-06 Cardiff session a whole batch of layout defects were caught only by
human eyeballing the rendered output: titles with a single orphan character on a line,
ragged A4 bottom whitespace (content jumping to the next page), billboard-sized numbers
next to a chart that already showed them, inconsistent waffle blocks, oversized footer
fine-print, and bars overflowing their track. Each of those is mechanically detectable.
This script turns those manual catches into a repeatable gate.

WHAT IT IS
----------
A *mostly static* linter: it parses the report HTML/CSS as text (regex, no DOM library)
and, when a matching PDF exists, does a light raster check via `pdftoppm -gray`
(parsing the PGM bytes with stdlib only). For each report it emits a PASS / WARN / FAIL
checklist. FAIL means "do not ship"; WARN means "human must re-review".

DESIGN CONSTRAINTS (do not break)
---------------------------------
- Python stdlib ONLY. No bs4 / lxml / Pillow / numpy.
- HTML is parsed as text. We deliberately distinguish CSS *rule definitions*
  (e.g. `.bignum{...}` in <style>, which the Cardiff report keeps for back-compat and
  is harmless) from actual *element usage* (e.g. `class="bignum"` on a real tag, which
  IS the brand-review smell). Only element usage triggers WARN.
- Raster checks are best-effort: if `pdftoppm` is missing or a PDF is absent, the raster
  checks are SKIPPED (reported as INFO), never FAIL.

USAGE
-----
    python3 preflight.py report.config.json

Reads the `reports[]` array from the config (same schema as build_pdf.py). For each
report it lints `src` (HTML, required) and, if present, the matching `out` PDF and the
`*-long.pdf` long-image PDF (looked up in the config dir — where build_longimage.py
writes — then beside the src; a per-report `longpdf` key overrides). Paths resolve
relative to the config dir. NOTE the only raster check (a4-ragged-whitespace) is
inter-page, so it applies to the A4 PDF; the single-page long PDF/PNG get static
checks only (they share the same src HTML).

Exit codes: 0 = no FAIL; 1 = at least one report has a FAIL; 2 = usage/config error
(bad args, config missing/unparsable, empty reports[]).
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

# ------------------------------------------------------------------ result model

PASS, WARN, FAIL, INFO = "PASS", "WARN", "FAIL", "INFO"

_ICON = {PASS: "✅", WARN: "⚠️ ", FAIL: "❌", INFO: "··"}


class Result:
    def __init__(self, check, level, msg):
        self.check = check
        self.level = level
        self.msg = msg

    def line(self):
        return "  {} [{}] {} — {}".format(_ICON[self.level], self.level, self.check, self.msg)


# ------------------------------------------------------------------ HTML helpers

def _strip_style_blocks(html):
    """Return (html_without_style, concatenated_css). We need the body markup with the
    <style> content removed so that CSS rule selectors like `.bignum{}` don't get
    mistaken for element class usage. HTML comments are stripped FIRST so commented-out
    markup (e.g. an old `data-w="120"` bar) can't trigger checks — a commented data-w
    used to raise a false FAIL-level bar-overflow."""
    html = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    css_parts = re.findall(r"<style[^>]*>(.*?)</style>", html, re.S | re.I)
    body_only = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.S | re.I)
    # also drop <script> blocks from the markup-class scan (they can contain class names
    # as JS strings, but those are dynamically-created, not static layout we lint here)
    body_only = re.sub(r"<script[^>]*>.*?</script>", "", body_only, flags=re.S | re.I)
    return body_only, "\n".join(css_parts)


def _has_element_class(body_html, cls):
    """True if a real element in the markup carries class `cls` (handles class lists,
    single/double quotes)."""
    pat = re.compile(r'class\s*=\s*["\']([^"\']*)["\']', re.I)
    for m in pat.finditer(body_html):
        if cls in m.group(1).split():
            return True
    return False


def _count_cjk(s):
    """Count CJK (Chinese/Japanese/Korean) characters in a string."""
    n = 0
    for ch in s:
        o = ord(ch)
        if (0x4E00 <= o <= 0x9FFF or      # CJK Unified Ideographs
                0x3400 <= o <= 0x4DBF or  # Extension A
                0x3040 <= o <= 0x30FF or  # Hiragana + Katakana
                0xAC00 <= o <= 0xD7A3 or  # Hangul syllables
                0xF900 <= o <= 0xFAFF):   # CJK compatibility
            n += 1
    return n


def _css_prop_for_selector(css, selector_regex, prop):
    """Find the value of `prop` inside the first rule whose selector matches
    selector_regex. Crude but adequate for the flat CSS these reports use.
    Returns the raw value string or None."""
    # find "selector { ... }" blocks
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css, re.S):
        sel, body = m.group(1), m.group(2)
        if re.search(selector_regex, sel):
            pm = re.search(r"(?<![\w-])" + re.escape(prop) + r"\s*:\s*([^;]+)", body, re.I)
            if pm:
                return pm.group(1).strip()
    return None


def _px_value(val):
    """Extract a px number from a CSS value like '10px' or '11.5px'. Returns float or None.
    Ignores clamp()/var()/% which we can't statically resolve."""
    if val is None:
        return None
    m = re.search(r"(-?\d+(?:\.\d+)?)\s*px", val)
    if m:
        return float(m.group(1))
    return None


# ------------------------------------------------------------------ static checks

def check_bar_overflow(body, css, out):
    """1. bar overflow: any data-w numeric > 100 -> FAIL."""
    bad = []
    for m in re.finditer(r'data-w\s*=\s*["\']?(-?\d+(?:\.\d+)?)', body):
        v = float(m.group(1))
        if v > 100:
            bad.append(v)
    if bad:
        out.append(Result("bar-overflow", FAIL,
                           "{} bar(s) have data-w > 100 (max {}); bar will overflow its track"
                           .format(len(bad), max(bad))))
    else:
        out.append(Result("bar-overflow", PASS, "all data-w values ≤ 100"))


def check_billboard_bignum(body, css, out):
    """2. billboard number: element using class="bignum" -> WARN."""
    if _has_element_class(body, "bignum"):
        out.append(Result("billboard-bignum", WARN,
                           '元素使用 class="bignum"；品牌评审建议改用 .note .fig 内联数字'
                           '（除非该页无竞争图表）'))
    else:
        out.append(Result("billboard-bignum", PASS, "no .bignum element in markup"))


def check_waffle(body, css, out):
    """3. waffle: element using class="waffle" -> WARN."""
    if _has_element_class(body, "waffle"):
        out.append(Result("waffle", WARN,
                           '元素使用 class="waffle"；品牌评审建议改用进度条 .bar-row'))
    else:
        out.append(Result("waffle", PASS, "no .waffle element in markup"))


def check_footer_fontsize(body, css, out):
    """4. footer fine-print font-size: `footer p` > 11px -> WARN."""
    val = _css_prop_for_selector(css, r"\bfooter\s+p\b", "font-size")
    px = _px_value(val)
    if px is None:
        out.append(Result("footer-fontsize", INFO,
                          "could not resolve `footer p` font-size statically (value={!r})".format(val)))
    elif px > 11:
        out.append(Result("footer-fontsize", WARN,
                          "`footer p` font-size {}px > 11px; colophon fine-print should be ~10px muted"
                          .format(px)))
    else:
        out.append(Result("footer-fontsize", PASS, "`footer p` font-size {}px ≤ 11px".format(px)))


def check_two_column_cols(body, css, out):
    """5. left/right two-column residue: `.cols` grid-template-columns has >1 track -> WARN.
    `.cols` must be a single column (stacked: chart on top, note below)."""
    val = _css_prop_for_selector(css, r"\.cols\b", "grid-template-columns")
    if val is None:
        out.append(Result("cols-single-column", INFO,
                          "no `.cols` grid-template-columns found (selector may differ)"))
        return
    tracks = _count_grid_tracks(val)
    if tracks is None:
        out.append(Result("cols-single-column", INFO,
                          "`.cols` grid-template-columns={!r}; could not count tracks".format(val)))
    elif tracks > 1:
        out.append(Result("cols-single-column", WARN,
                          "`.cols` has {} column tracks ({!r}); should be single-column stacked "
                          "(chart on top, note below), not left-right".format(tracks, val)))
    else:
        out.append(Result("cols-single-column", PASS,
                          "`.cols` is single column ({!r})".format(val)))


def _count_grid_tracks(val):
    """Count grid-template-columns track tokens. Handles 1fr / repeat(N,...) / explicit list.
    Returns int or None."""
    v = val.strip()
    # repeat(N, ...) -> N tracks (the auto-fit/auto-fill cases are responsive, treat as 1+)
    rm = re.match(r"repeat\(\s*([^,]+)\s*,", v, re.I)
    if rm:
        cnt = rm.group(1).strip()
        if cnt.isdigit():
            return int(cnt)
        # auto-fit / auto-fill collapse to a single column at narrow widths -> treat as 1
        return 1
    if v in ("none", "auto"):
        return 1
    # explicit space-separated track list, e.g. "1fr" or "auto 1fr" or "2fr 1fr"
    # strip out any function-call commas first
    tokens = [t for t in re.split(r"\s+", v) if t]
    return len(tokens) if tokens else None


def check_topbar(body, css, out):
    """6. top logo missing: no class="topbar" OR still using a visible .masthead -> WARN.
    The brand redesign requires a visible `.topbar` (page-1 logo lockup) and the legacy
    `.masthead` must be display:none."""
    has_topbar = _has_element_class(body, "topbar")
    has_masthead_el = _has_element_class(body, "masthead")
    masthead_display = _css_prop_for_selector(css, r"\.masthead\b", "display")
    masthead_hidden = (masthead_display is not None and masthead_display.strip().lower() == "none")

    problems = []
    if not has_topbar:
        problems.append('缺少 class="topbar"（page-1 logo lockup，应在 .wrap 顶部且打印可见）')
    if has_masthead_el and not masthead_hidden:
        problems.append('仍在使用可见的 .masthead（应 display:none，改用 .topbar）')
    if problems:
        out.append(Result("topbar", WARN, "; ".join(problems)))
    else:
        out.append(Result("topbar", PASS,
                          ".topbar present" + ("" if not has_masthead_el else " (.masthead hidden)")))


def check_title_orphan(body, css, out):
    """7. title orphan risk: split each <h1> by <br>; count CJK chars per fragment.
    If any fragment (especially the first) has > 9 Han chars -> WARN (narrow layout may
    wrap and produce a single-char orphan line)."""
    h1s = re.findall(r"<h1\b[^>]*>(.*?)</h1>", body, re.S | re.I)
    if not h1s:
        out.append(Result("title-orphan", INFO, "no <h1> found"))
        return
    flagged = []
    for h1 in h1s:
        # split on <br> (any form)
        frags = re.split(r"<br\s*/?>", h1, flags=re.I)
        for i, frag in enumerate(frags):
            text = re.sub(r"<[^>]+>", "", frag)  # strip inline tags like <span>
            text = re.sub(r"\s+", "", text)
            cjk = _count_cjk(text)
            if cjk > 9:
                flagged.append((i, cjk, text[:18]))
    if flagged:
        details = "; ".join("第{}行 {}汉字 “{}…”".format(i + 1, c, t) for i, c, t in flagged)
        out.append(Result("title-orphan", WARN,
                          "窄版可能折行产生孤字：{}（建议每行 ≤9 个汉字，或调整 <br> 断点）"
                          .format(details)))
    else:
        out.append(Result("title-orphan", PASS, "no <h1> fragment exceeds 9 CJK chars"))


def check_legacy_bar_colors(body, css, out):
    """8b. 4-colour discipline (brand review 2026-06-18): a `.bar` carrying a legacy
    positional colour class (sand / coral / ink) -> WARN. New content should default to
    neutral grey and opt in with semantic hl (brand) / up (green) / neg (decline-red).
    Positional/decorative colour is exactly the 'colours mean nothing' confusion that
    review flagged."""
    pat = re.compile(r'class\s*=\s*["\']([^"\']*)["\']', re.I)
    legacy = {"sand", "coral", "ink"}
    bad = 0
    for m in pat.finditer(body):
        toks = set(m.group(1).split())
        if "bar" in toks and (toks & legacy):
            bad += 1
    if bad:
        out.append(Result("bar-color-discipline", WARN,
                          '{} 个 .bar 使用了 legacy 位置色类 (sand/coral/ink)；'
                          '4 色系统要求默认中性灰,语义高亮用 hl(品牌)/up(增长绿)/neg(下降红)'
                          .format(bad)))
    else:
        out.append(Result("bar-color-discipline", PASS,
                          "no legacy positional bar colour classes (4-colour system clean)"))


def check_render_contract(body, css, out):
    """8. reveal/render contract: each class="bar" should contain <i data-w=...>;
    `.rv` must exist; `:root` must declare --paper/--coral (and other key vars).
    Missing -> WARN (PDF will render blank/animated-out)."""
    problems = []

    # every element carrying class token "bar" should be followed by an <i data-w> (horizontal
    # bars fill via the reveal script). Anchor on the .bar element itself and scan a lookahead
    # window — the old approach captured the bar-row up to the FIRST </div>, so a nested <div>
    # inside a row silently truncated the capture and missing data-w went undetected.
    # (Column charts use .col + <i data-h>, line/donut are SVG — none carry .bar, so none flagged.)
    bar_total = bar_missing = 0
    for m in re.finditer(r'<\w+[^>]*\bclass\s*=\s*["\']([^"\']*)["\'][^>]*>', body, re.I):
        if "bar" in m.group(1).split():
            bar_total += 1
            if not re.search(r"<i[^>]*\bdata-w\b", body[m.end():m.end() + 600], re.I):
                bar_missing += 1
    if bar_missing:
        problems.append("{}/{} 个 .bar 附近未发现 <i data-w=…>（打印时不会填充）"
                        .format(bar_missing, bar_total))

    # .rv must exist as an element class (the PDF script forces .rv.on visible)
    if not _has_element_class(body, "rv"):
        problems.append('未发现 class="rv" 元素（PDF reveal-forcing 依赖它，内容可能整段隐形）')

    # :root must declare the key custom properties
    root_block = ""
    rm = re.search(r":root\s*\{([^{}]*)\}", css, re.S)
    if rm:
        root_block = rm.group(1)
    # legacy palette (print-CSS overrides reference these) + the 4-colour semantic system
    # (brand review 2026-06-18); the current template declares both sets.
    required_vars = ["--paper", "--coral", "--ink", "--harbour", "--sand", "--line",
                     "--brand", "--up", "--down", "--data"]
    missing_vars = [v for v in required_vars if v not in root_block]
    if not rm:
        problems.append(":root 变量块缺失（print CSS 引用 var(--paper) 等会失效）")
    elif missing_vars:
        problems.append(":root 缺少变量 {}".format(", ".join(missing_vars)))

    if problems:
        out.append(Result("render-contract", WARN, " | ".join(problems)))
    else:
        out.append(Result("render-contract", PASS,
                          "all .bar carry <i data-w>; .rv present; :root vars complete"))


# ------------------------------------------------------------------ raster check

def _read_pgm(path):
    """Parse a binary P5 PGM. Returns (w, h, maxval, bytes) or None on failure."""
    try:
        with open(path, "rb") as f:
            data = f.read()
    except OSError:
        return None
    idx = 0

    def tok(data, idx):
        # skip whitespace and comments
        while idx < len(data):
            c = data[idx:idx + 1]
            if c.isspace():
                idx += 1
            elif c == b"#":
                while idx < len(data) and data[idx:idx + 1] not in (b"\n", b"\r"):
                    idx += 1
            else:
                break
        start = idx
        while idx < len(data) and not data[idx:idx + 1].isspace():
            idx += 1
        return data[start:idx], idx

    magic, idx = tok(data, idx)
    if magic != b"P5":
        return None
    w, idx = tok(data, idx)
    h, idx = tok(data, idx)
    mx, idx = tok(data, idx)
    idx += 1  # single whitespace separator after maxval
    try:
        w, h, mx = int(w), int(h), int(mx)
    except ValueError:
        return None
    px = data[idx:idx + w * h]
    if len(px) < w * h:
        return None
    return w, h, mx, px


def check_a4_ragged_whitespace(report, out):
    """9. A4 ragged bottom whitespace: rasterize the PDF (gray) and, for each non-last
    page, check whether the bottom region is a large near-paper void while the page
    above it has content. If so -> WARN (content jumped to the next page).

    Heuristic: split each page's content area (excluding the pure-white CDP margin
    bands) into horizontal bands. A band is "content" if its fraction of dark-ish
    pixels (brightness < 200) exceeds a small floor. If the bottom ~35% of the page is
    essentially empty (content fraction ~0) while there IS content higher up, flag it.
    """
    pdf = report.get("_pdf")
    if not pdf:
        out.append(Result("a4-ragged-whitespace", INFO, "no matching PDF found; raster check skipped"))
        return
    if not shutil.which("pdftoppm"):
        out.append(Result("a4-ragged-whitespace", INFO, "pdftoppm not installed; raster check skipped"))
        return

    tmpd = tempfile.mkdtemp(prefix="preflight_")
    prefix = os.path.join(tmpd, "p")
    try:
        r = subprocess.run(["pdftoppm", "-gray", "-r", "40", pdf, prefix],
                           capture_output=True, timeout=120)
        if r.returncode != 0:
            out.append(Result("a4-ragged-whitespace", INFO,
                              "pdftoppm failed: {}".format(r.stderr.decode("utf-8", "replace")[:120])))
            return
        pages = sorted(f for f in os.listdir(tmpd) if f.endswith(".pgm"))
        n = len(pages)
        if n <= 1:
            out.append(Result("a4-ragged-whitespace", PASS,
                              "single-page PDF; no inter-page ragging to check"))
            return

        flagged = []
        for pi, fname in enumerate(pages):
            if pi == n - 1:
                continue  # last page is allowed to be short
            parsed = _read_pgm(os.path.join(tmpd, fname))
            if not parsed:
                continue
            w, h, mx, px = parsed
            # trim left/right gutters: only look at the central 80% width (avoids edge noise)
            x0, x1 = int(w * 0.10), int(w * 0.90)
            cw = x1 - x0
            if cw <= 0:
                continue

            # per-row content fraction (dark pixels), then trim pure-white margin bands
            DARK = 200          # brightness below this = ink/content
            ROW_CONTENT = 0.004  # >0.4% dark pixels in a row => row has content
            row_dark = []
            for y in range(h):
                base = y * w
                d = 0
                for x in range(x0, x1):
                    if px[base + x] < DARK:
                        d += 1
                row_dark.append(d / cw)

            # find first & last content rows (the actual content box, excluding white margins)
            content_rows = [y for y, f in enumerate(row_dark) if f >= ROW_CONTENT]
            if not content_rows:
                continue  # genuinely blank page; not our ragged-tail case
            top, bot = content_rows[0], content_rows[-1]
            box_h = bot - top + 1
            if box_h < h * 0.25:
                # very little content overall; could be a section divider page — skip
                continue

            # how much of the page height below the last content row is empty paper?
            tail_empty = (h - 1 - bot)
            tail_frac = tail_empty / h
            if tail_frac > 0.35:
                flagged.append((pi + 1, round(tail_frac * 100)))

        if flagged:
            det = "; ".join("第{}页底部 ~{}% 留白".format(p, f) for p, f in flagged)
            out.append(Result("a4-ragged-whitespace", WARN,
                              "{}（内容跳页，疑似参差留白；请目检页面边界）".format(det)))
        else:
            out.append(Result("a4-ragged-whitespace", PASS,
                              "no non-last page has >35% empty bottom ({} pages checked)".format(n)))
    except subprocess.TimeoutExpired:
        out.append(Result("a4-ragged-whitespace", INFO, "pdftoppm timed out; raster check skipped"))
    finally:
        shutil.rmtree(tmpd, ignore_errors=True)


# ------------------------------------------------------------------ driver

def lint_report(report, cfg_dir):
    src = report.get("src")
    name = src or report.get("out") or "<unnamed>"
    results = []

    if not src:
        results.append(Result("config", FAIL, "report entry has no `src` HTML"))
        return name, results

    src_path = src if os.path.isabs(src) else os.path.join(cfg_dir, src)
    if not os.path.isfile(src_path):
        results.append(Result("config", FAIL, "src HTML not found: {}".format(src_path)))
        return name, results

    with open(src_path, "r", encoding="utf-8", errors="replace") as f:
        html = f.read()
    body, css = _strip_style_blocks(html)

    # static checks (HTML/CSS)
    check_bar_overflow(body, css, results)
    check_billboard_bignum(body, css, results)
    check_waffle(body, css, results)
    check_footer_fontsize(body, css, results)
    check_two_column_cols(body, css, results)
    check_topbar(body, css, results)
    check_title_orphan(body, css, results)
    check_legacy_bar_colors(body, css, results)
    check_render_contract(body, css, results)

    # locate matching PDF(s): the configured `out`, plus the *-long.pdf long-image PDF.
    # build_longimage.py writes long outputs into the CONFIG dir (honouring per-report
    # `long`/`longpdf` overrides), so look there first, then beside the src (legacy layouts).
    pdf_candidates = []
    out_pdf = report.get("out")
    if out_pdf:
        op = out_pdf if os.path.isabs(out_pdf) else os.path.join(cfg_dir, out_pdf)
        if os.path.isfile(op):
            pdf_candidates.append(op)
    stem = os.path.splitext(os.path.basename(src_path))[0]
    long_names = [report.get("longpdf") or (stem + "-long.pdf")]
    long_pdf = None
    for nm in long_names:
        for base in (cfg_dir, os.path.dirname(src_path)):
            p = nm if os.path.isabs(nm) else os.path.join(base, nm)
            if os.path.isfile(p):
                long_pdf = p
                break
        if long_pdf:
            break
    if long_pdf and long_pdf not in pdf_candidates:
        pdf_candidates.append(long_pdf)

    if pdf_candidates:
        # raster-check the A4 print PDF (first candidate); the long PDF is a single tall
        # page, so the inter-page whitespace check is structurally N/A there — its content
        # is already covered by the static checks on the shared src HTML.
        report["_pdf"] = pdf_candidates[0]
        check_a4_ragged_whitespace(report, results)
        for extra in pdf_candidates[1:]:
            results.append(Result("a4-ragged-whitespace", INFO,
                                  "long PDF present ({}): single tall page — inter-page check N/A; "
                                  "covered by the static checks on the same src HTML"
                                  .format(os.path.basename(extra))))
    else:
        check_a4_ragged_whitespace({}, results)  # emits the "no PDF" INFO

    return name, results


def main(argv):
    if len(argv) != 2:
        sys.stderr.write("usage: python3 preflight.py report.config.json\n")
        return 2
    cfg_path = argv[1]
    if not os.path.isfile(cfg_path):
        sys.stderr.write("config not found: {}\n".format(cfg_path))
        return 2
    try:
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    except json.JSONDecodeError as e:
        sys.stderr.write("config is not valid JSON: {} ({})\n".format(cfg_path, e))
        return 2
    cfg_dir = os.path.dirname(os.path.abspath(cfg_path))
    reports = cfg.get("reports", [])
    if not reports:
        sys.stderr.write("config has no reports[]\n")
        return 2

    any_fail = False
    print("preflight — insight-report 出片前自检")
    print("config: {}".format(os.path.abspath(cfg_path)))
    print("=" * 72)
    for report in reports:
        name, results = lint_report(report, cfg_dir)
        n_fail = sum(1 for r in results if r.level == FAIL)
        n_warn = sum(1 for r in results if r.level == WARN)
        verdict = FAIL if n_fail else (WARN if n_warn else PASS)
        print("\n▶ {}   [{} {}]".format(name, _ICON[verdict], verdict))
        if report.get("_pdf"):
            print("  (pdf: {})".format(os.path.basename(report["_pdf"])))
        for r in results:
            print(r.line())
        if n_fail:
            any_fail = True

    print("\n" + "=" * 72)
    if any_fail:
        print("RESULT: ❌ FAIL — at least one report has a blocking FAIL. Fix before shipping.")
    else:
        print("RESULT: ✅ no FAIL. Re-review every ⚠️  WARN by eye before shipping.")
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
