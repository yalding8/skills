#!/usr/bin/env python3
"""
build_report.py — render a magazine-style insight HTML from a content JSON + shared template.

Goal: ONE template + per-language content JSON. No more hand-maintaining two ~430-line
HTML files whose CSS drifts apart. Edit content.<lang>.json, rebuild, done.

Pure Python stdlib only (string.Template). No jinja2 / no external deps.

USAGE
    python3 build_report.py content.cn.json [-o cardiff-insight-2026-cn.html]
    python3 build_report.py content.en.json          # output defaults to content json's "output"

The content JSON's top-level "output" key names the HTML file (relative to the JSON's dir),
or pass -o to override.

----------------------------------------------------------------------------------------
BAR HELPER (the core convenience)
----------------------------------------------------------------------------------------
A chart's "bars" is a list of rows. Each row:
    {"label": "2021 峰", "value": 746, "style": "coral", "hl": true}

The helper computes the visual bar width (data-w, a 0..~95 number the IO script animates to)
and the printed value text. Three modes, set per-chart via "mode":

  mode = "scale"   (DEFAULT)
        data-w = value / max(values) * scale   (scale defaults to 95)
        Use for raw magnitudes (deal counts, etc.) so the biggest bar ≈ 95% wide.
        Printed value = value (or "value_text" if you want a custom label like "474").

  mode = "percent"
        data-w = value  (the value IS already a 0..100 width)
        Printed value = "{value}%"  (override with value_text)
        Use for shares that literally sum to 100 (e.g. 47% / 40% / 13%).

  mode = "raw_w"
        You supply "w" per row explicitly; helper does no math.
        Printed value taken from "value_text" (or value).
        Use to reproduce hand-tuned widths 1:1 (e.g. YoY-% charts where bar length is a
        manual visual encoding decoupled from the printed %, like the country/peer charts).

NEGATIVE VALUES: any row whose numeric value < 0 (or w resolves < 0) gets width 0,
the row gets class "neg" (val turns coral), and the printed value keeps its minus sign.
You can also force red-negative styling with "neg": true.

Per-row keys:
    label       (str, required)   right-aligned text left of the bar
    value       (number)          the datum; drives math + default printed text
    value_text  (str, optional)   override the printed value cell (e.g. "+22%", "2.0万")
    w           (number, optional) explicit data-w; required for mode raw_w
    hl          (bool, optional)  THE highlighted row — brand-colour fill (#FF5A5F),
                                  bold label. Use for the subject (Cardiff / UK). One per chart.
    up          (bool, optional)  growth-green fill (positive emphasis)
    neg         (bool, optional)  decline: red value; width 0 (normal bars) or left-extending
                                  (diverging bars). Auto when value < 0.
    style       (str, optional)   DEPRECATED legacy bar class "coral"|"sand"|"ink".
                                  Don't use in new content — default is neutral grey; opt in
                                  with hl/up/neg. (Brand review 2026-06-18: 4-colour system —
                                  brand / growth-green / decline-red / neutral-grey ONLY.)

----------------------------------------------------------------------------------------
CHART VARIANTS  ("variant" on a chart block; default "bar")
----------------------------------------------------------------------------------------
  "bar"     (default)  horizontal bars (mode scale/percent/raw_w as above).
            Add "diverging": true to render signed data around a centre zero-axis
            (positive right / negative LEFT in decline-red) — use when negatives must SHOW.
  "column"  vertical columns (time comparison). bars:[{label,value,hl?/up?/down?}].
            Default grey, highlight ONE with hl. "scale" caps the tallest (default 92).
  "line"    trend line over time. bars:[{label,value,hl?/down?,value_text?}] (treated as
            ordered points). Marks each point; hl point = brand, down point = red.
  "donut"   share/proportion. bars:[{label,value,hl?,value_text?}]; highlighted slice =
            brand, rest = neutral greys. Optional "center":{value,label} in the hole.

----------------------------------------------------------------------------------------
CONTENT JSON SHAPE  (see templates/content.example.json for an annotated copy)
----------------------------------------------------------------------------------------
{
  "lang": "cn" | "en",          # picks the built-in style preset
  "output": "report-cn.html",
  "style": { ... optional CSS overrides on top of the preset ... },
  "head": { meta_description, og_title, og_description, page_title, lang_attr?, keywords? },
  "topbar": { logo_src, logo_alt, issue (may contain <br>) },
  "hero": { kicker, h1 (may contain <br>/<span class=accent>), deck,
            meta: [ {b, span}, x4 ] },
  "stats": [ {b, span, tone?} x4 ],   # tone: "pos"|"neg"|"neutral" override; default auto by +/− sign of b (unsigned keeps positional color)
  "chapters": [
     { "num": "01", "h2": "...", "sub": "...",
       "blocks": [ <block>, ... ],
       "pull_quote": { "quote": "...", "cite": "..." }   # optional, after blocks
     }, ...
  ],
  "footer": { brand, note (may contain <code>), tag }
}

A <block> is one of:
  {"type":"chart", "ct":"title", "cn2":"subtitle", "mode":"scale|percent|raw_w",
   "scale":95, "bars":[ ... ]}
  {"type":"note", "h4":"...", "ps":[ "para html", ... ], "fig":"−58%", "style":"..."}
       # "fig" (optional) prepends an inline .fig number to the FIRST paragraph
       # "style" (optional) raw inline style on the .note div (e.g. "margin-top:6px")
  {"type":"acts", "items":[ {"h3":"...<em>...</em>", "p":"..."}, ... ]}
  {"type":"group", "blocks":[ ... ]}   # wraps children in a bare <div> (matches the
       # original's nested column wrappers; purely structural, no visual effect)
"""
import argparse
import json
import os
import sys
from string import Template

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(HERE, "..", "templates", "report.template.html")

# ----------------------------------------------------------------------------------------
# Built-in per-language style presets (these are the CSS values that differ CN vs EN,
# extracted 1:1 from the two finished Cardiff reports).
# ----------------------------------------------------------------------------------------
PRESET_CN = {
    "font_face": (
        "@font-face{font-family:'Alibaba PuHuiTi 3.0';src:url('https://puhuiti.oss-cn-hangzhou.aliyuncs.com/AlibabaPuHuiTi-3/AlibabaPuHuiTi_3_55_Regular/AlibabaPuHuiTi_3_55_Regular.woff2') format('woff2');font-weight:400;font-display:swap}\n"
        "@font-face{font-family:'Alibaba PuHuiTi 3.0';src:url('https://puhuiti.oss-cn-hangzhou.aliyuncs.com/AlibabaPuHuiTi-3/AlibabaPuHuiTi_3_85_Bold/AlibabaPuHuiTi_3_85_Bold.woff2') format('woff2');font-weight:700;font-display:swap}\n"
        "@font-face{font-family:'Alibaba PuHuiTi 3.0';src:url('https://puhuiti.oss-cn-hangzhou.aliyuncs.com/AlibabaPuHuiTi-3/AlibabaPuHuiTi_3_65_Medium/AlibabaPuHuiTi_3_65_Medium.woff2') format('woff2');font-weight:500;font-display:swap}"
    ),
    "montserrat_import": "https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,600;0,800;1,400&display=swap",
    "font_body": "'Alibaba PuHuiTi 3.0','PingFang SC','Microsoft YaHei',sans-serif",
    "body_line_height": "1.85",
    "topbar_issue_ls": ".26em",
    "hero_h1_size": "clamp(38px,7vw,76px)",
    "hero_h1_lh": "1.14",
    "hero_h1_weight": "700",
    "hero_h1_ls": ".01em",
    "hero_h1_maxw": "13em",
    "hero_deck_maxw": "36em",
    "hero_meta_ls": ".08em",
    "stats_span_lh": "1.6",
    "ch_h2_size": "clamp(24px,3.4vw,38px)",
    "ch_h2_weight": "700",
    "ch_h2_lh": "1.3",
    "ch_sub_maxw": "38em",
    "chart_ct_size": "13px",
    "chart_ct_ls": ".12em",
    "chart_ct_weight": "500",
    "chart_ct_tt": "",
    "bar_lab_min": "96px",
    "bar_lab_max": "9em",
    "bar_lab_size": "13.5px",
    "col_h": "230px",
    "legend_size": "13.5px",
    "note_h4_size": "14px",
    "note_h4_ls": ".18em",
    "note_h4_tt": "",
    "note_p_size": "14.5px",
    "note_p_maxw": "52em",
    "pq_maxw": "760px",
    "pq_quote": "「",
    "pq_quote_top": "-8px",
    "pq_quote_size": "clamp(40px,6vw,64px)",
    "pq_quote_weight": "700",
    "pq_bq_size": "clamp(19px,2.6vw,27px)",
    "pq_bq_lh": "1.7",
    "pq_cite_size": "13px",
    "pq_cite_ls": ".1em",
    "pq_cite_prefix": "—— ",
    "bignum_span_size": "15px",
    "bignum_span_maxw": "16em",
    "bignum_span_lh": "1.6",
    "act_h3_weight": "700",
    "act_p_size": "14.5px",
    "act_p_maxw": "42em",
    "footer_brand_weight": "700",
    "footer_p_maxw": "60em",
    "footer_tag_ls": ".3em",
}

PRESET_EN = {
    "font_face": (
        "@font-face{font-family:'Alibaba PuHuiTi 3.0';src:url('https://puhuiti.oss-cn-hangzhou.aliyuncs.com/AlibabaPuHuiTi-3/AlibabaPuHuiTi_3_55_Regular/AlibabaPuHuiTi_3_55_Regular.woff2') format('woff2');font-weight:400;font-display:swap}\n"
        "@font-face{font-family:'Alibaba PuHuiTi 3.0';src:url('https://puhuiti.oss-cn-hangzhou.aliyuncs.com/AlibabaPuHuiTi-3/AlibabaPuHuiTi_3_85_Bold/AlibabaPuHuiTi_3_85_Bold.woff2') format('woff2');font-weight:700;font-display:swap}"
    ),
    "montserrat_import": "https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,500;0,600;0,800;1,400&display=swap",
    "font_body": "'Montserrat','Helvetica Neue',Arial,sans-serif",
    "body_line_height": "1.7",
    "topbar_issue_ls": ".22em",
    "hero_h1_size": "clamp(36px,6.4vw,70px)",
    "hero_h1_lh": "1.12",
    "hero_h1_weight": "800",
    "hero_h1_ls": "-.01em",
    "hero_h1_maxw": "15em",
    "hero_deck_maxw": "40em",
    "hero_meta_ls": ".04em",
    "stats_span_lh": "1.55",
    "ch_h2_size": "clamp(23px,3.2vw,36px)",
    "ch_h2_weight": "800",
    "ch_h2_lh": "1.25",
    "ch_sub_maxw": "42em",
    "chart_ct_size": "12.5px",
    "chart_ct_ls": ".1em",
    "chart_ct_weight": "600",
    "chart_ct_tt": ";text-transform:uppercase",
    "bar_lab_min": "110px",
    "bar_lab_max": "11em",
    "bar_lab_size": "13px",
    "col_h": "240px",
    "legend_size": "13px",
    "note_h4_size": "13px",
    "note_h4_ls": ".14em",
    "note_h4_tt": ";text-transform:uppercase",
    "note_p_size": "14px",
    "note_p_maxw": "56em",
    "pq_maxw": "780px",
    "pq_quote": "\\201C",
    "pq_quote_top": "6px",
    "pq_quote_size": "clamp(56px,8vw,90px)",
    "pq_quote_weight": "800",
    "pq_bq_size": "clamp(18px,2.4vw,25px)",
    "pq_bq_lh": "1.55",
    "pq_cite_size": "12.5px",
    "pq_cite_ls": ".06em",
    "pq_cite_prefix": "— ",
    "bignum_span_size": "14.5px",
    "bignum_span_maxw": "17em",
    "bignum_span_lh": "1.5",
    "act_h3_weight": "800",
    "act_p_size": "14px",
    "act_p_maxw": "44em",
    "footer_brand_weight": "800",
    "footer_p_maxw": "64em",
    "footer_tag_ls": ".28em",
}

PRESETS = {"cn": PRESET_CN, "en": PRESET_EN}


def fmt_w(x):
    """Format a width number the way the originals do: trailing-zero-trimmed, but keep
    a single decimal when present (e.g. 95.0, 16.5, 47, 14.6)."""
    if isinstance(x, int):
        return str(x)
    f = float(x)
    if f == int(f):
        # originals print 2021/03/etc peak as 95.0 (one decimal) for scaled charts but
        # whole numbers (47) for percent charts. We mirror the source by keeping ints
        # int and floats float; callers that need "95.0" pass 95.0 literally in JSON.
        # json.load gives int for 95 and float for 95.0, so distinguish via repr.
        return str(f)
    # strip trailing zeros but keep at least one decimal
    s = ("%.4f" % f).rstrip("0").rstrip(".")
    return s


def is_negative(value, w):
    if w is not None:
        try:
            return float(w) < 0
        except (TypeError, ValueError):
            return False
    if value is not None:
        try:
            return float(value) < 0
        except (TypeError, ValueError):
            return False
    return False


def render_bars(chart):
    mode = chart.get("mode", "scale")
    scale = chart.get("scale", 95)
    bars = chart["bars"]

    # precompute max for scale mode (ignore negatives)
    if mode == "scale":
        vals = [float(b["value"]) for b in bars if b.get("value") is not None and float(b["value"]) > 0]
        mx = max(vals) if vals else 1.0

    rows = []
    for b in bars:
        label = b["label"]
        value = b.get("value")
        value_text = b.get("value_text")
        explicit_w = b.get("w")
        bstyle = b.get("style", "")
        hl = b.get("hl", False)
        up_flag = b.get("up", False)
        neg_flag = b.get("neg", False)

        neg = neg_flag or is_negative(value, explicit_w)

        # compute width
        if mode == "raw_w":
            if explicit_w is None:
                raise ValueError("mode raw_w requires 'w' on every bar (label=%r)" % label)
            w = float(explicit_w)
        elif mode == "percent":
            w = float(explicit_w) if explicit_w is not None else float(value)
        else:  # scale
            if explicit_w is not None:
                w = float(explicit_w)
            else:
                v = float(value) if value is not None else 0.0
                w = (v / mx * scale) if v > 0 else 0.0

        zeroed = bool(neg or w < 0)
        if zeroed:
            w = 0.0

        # printed value cell
        if value_text is not None:
            vtxt = value_text
        elif mode == "percent":
            vtxt = "%s%%" % fmt_w(value)
        else:
            vtxt = fmt_w(value)

        # width string (data-w):
        #   - zeroed rows  -> "0"
        #   - explicit w   -> echo exactly as authored (int stays int, 95.0 stays 95.0)
        #   - computed     -> one decimal (matches the source aesthetic, e.g. 60.4)
        if zeroed:
            wtxt = "0"
        elif explicit_w is not None:
            wtxt = fmt_w(explicit_w)
        elif mode == "percent":
            # percent shares are authored as ints (47/40/13) -> bare int width
            wtxt = str(int(w)) if w == int(w) else ("%.1f" % w)
        else:
            wtxt = "%.1f" % w

        cls = ["bar-row"]
        if hl:
            cls.append("hl")
        if up_flag:
            cls.append("up")
        if neg:
            cls.append("neg")
        # bar fill class drives colour: default (no class) = neutral grey;
        # hl = brand highlight, up = growth green (decline is zeroed-width here, so its
        # fill is moot — the red value cell carries the signal via .bar-row.neg)
        barcls = "bar"
        if hl:
            barcls += " hl"
        elif up_flag:
            barcls += " up"
        if bstyle:
            barcls += " " + bstyle

        rows.append(
            '        <div class="%s"><span class="lab">%s</span>'
            '<span class="%s"><i data-w="%s"></i></span>'
            '<b class="val">%s</b></div>'
            % (" ".join(cls), label, barcls, wtxt, vtxt)
        )
    return "\n".join(rows)


def render_diverging_bars(chart):
    """Signed horizontal bars around a centre zero-axis: positive extends right (neutral
    grey / brand if hl), negative extends LEFT in decline-red. Use for YoY where some
    values are negative and must be SHOWN (not zeroed). Width is half-track relative
    (max ~47% of the full bar, leaving a margin), scaled by max(|value|)."""
    bars = chart["bars"]
    scale = chart.get("scale", 47)
    vals = [abs(float(b["value"])) for b in bars if b.get("value") is not None]
    mx = max(vals) if vals else 1.0
    rows = []
    for b in bars:
        label = b["label"]
        value = b.get("value")
        value_text = b.get("value_text")
        hl = b.get("hl", False)
        v = float(value) if value is not None else 0.0
        neg = (v < 0) or b.get("neg", False)
        w = (abs(v) / mx * scale) if mx else 0.0
        vtxt = value_text if value_text is not None else fmt_w(value)
        cls = ["bar-row", "div"]
        if hl:
            cls.append("hl")
        elif b.get("up"):
            cls.append("up")
        if neg:
            cls.append("neg")
        barcls = "bar div"
        if hl:
            barcls += " hl"
        elif b.get("up"):
            barcls += " up"
        icls = ' class="neg"' if neg else ""
        rows.append(
            '        <div class="%s"><span class="lab">%s</span>'
            '<span class="%s"><span class="track left"></span><span class="track"></span>'
            '<i%s data-w="%.1f"></i></span>'
            '<b class="val">%s</b></div>'
            % (" ".join(cls), label, barcls, icls, w, vtxt)
        )
    return "\n".join(rows)


def render_column(chart):
    """Vertical columns (time comparison). Default fill = neutral grey; opt-in hl=brand /
    up=green / down=red. Heights scaled to max positive value."""
    bars = chart["bars"]
    scale = chart.get("scale", 92)
    vals = [float(b["value"]) for b in bars
            if b.get("value") is not None and float(b["value"]) > 0]
    mx = max(vals) if vals else 1.0
    cols = []
    for b in bars:
        label = b["label"]
        value = b.get("value")
        value_text = b.get("value_text")
        v = float(value) if value is not None else 0.0
        h = (v / mx * scale) if v > 0 else 0.0
        vtxt = value_text if value_text is not None else fmt_w(value)
        cls = ["col"]
        if b.get("hl"):
            cls.append("hl")
        elif b.get("down") or v < 0:
            cls.append("down")
        elif b.get("up"):
            cls.append("up")
        cols.append(
            '          <div class="%s"><span class="colval">%s</span>'
            '<i data-h="%.1f"></i><span class="collab">%s</span></div>'
            % (" ".join(cls), vtxt, h, label)
        )
    return '        <div class="col-chart">\n%s\n        </div>' % "\n".join(cols)


def render_line(chart):
    """Trend line (one metric over time). Neutral ink line + faint brand area; each point a
    dot (neutral; hl=brand, down=red). Static SVG (renders 1:1 in print; the .rv wrapper
    still fades it in on screen)."""
    pts = chart["bars"]
    if not pts:
        return '        <div class="linechart"></div>'
    vals = [float(p["value"]) for p in pts]
    mx, mn = max(vals), min(vals)
    span = (mx - mn) if mx > mn else 1.0
    W, H = 760.0, 300.0
    padL = padR = 20.0
    padT, padB = 36.0, 36.0
    n = len(pts)
    yb = H - padB

    def X(i):
        return padL + (W - padL - padR) * (i / (n - 1) if n > 1 else 0.5)

    def Y(v):
        return padT + (H - padT - padB) * (1 - (v - mn) / span)

    coords = [(X(i), Y(float(p["value"]))) for i, p in enumerate(pts)]
    line_d = "M" + " L".join("%.1f %.1f" % (x, y) for x, y in coords)
    area_d = ("M%.1f %.1f " % (coords[0][0], yb)
              + "".join("L%.1f %.1f " % (x, y) for x, y in coords)
              + "L%.1f %.1f Z" % (coords[-1][0], yb))

    svg = ['      <div class="linechart">',
           '        <svg viewBox="0 0 %g %g" preserveAspectRatio="xMidYMid meet" '
           'xmlns="http://www.w3.org/2000/svg">' % (W, H),
           '          <line class="lc-base" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'
           % (padL, yb, W - padR, yb),
           '          <path class="lc-area" d="%s"/>' % area_d,
           '          <path class="lc-line" d="%s"/>' % line_d]
    for i, p in enumerate(pts):
        x, y = coords[i]
        tone = "hl" if p.get("hl") else ("down" if p.get("down") else ("up" if p.get("up") else ""))
        dotcls = "lc-dot" + ((" " + tone) if tone else "")
        valcls = "lc-val" + ((" " + tone) if tone else "")
        vtxt = p.get("value_text", fmt_w(p.get("value")))
        vy = y - 12 if y > padT + 16 else y + 22
        svg.append('          <circle class="%s" cx="%.1f" cy="%.1f" r="4.5"/>' % (dotcls, x, y))
        svg.append('          <text class="%s" x="%.1f" y="%.1f">%s</text>' % (valcls, x, vy, vtxt))
        svg.append('          <text class="lc-lab" x="%.1f" y="%.1f">%s</text>'
                   % (x, yb + 20, p["label"]))
    svg.append('        </svg>')
    svg.append('      </div>')
    return "\n".join(svg)


def render_donut(chart):
    """Share / proportion donut. The highlighted slice = brand; the rest = neutral greys.
    Optional center={value,label}. Legend lists every slice with its value."""
    slices = chart["bars"]
    total = sum(float(s["value"]) for s in slices) or 1.0
    cx = cy = 80.0
    r = 58.0
    sw = 26.0
    import math
    C = 2 * math.pi * r
    greys = ["var(--data)", "var(--data-soft)", "var(--ink-soft)"]
    acc = 0.0
    arcs = []
    legend = []
    gi = 0
    for s in slices:
        v = float(s["value"])
        frac = v / total
        seg = frac * C
        if s.get("hl"):
            color = "var(--brand)"
        elif s.get("down"):
            color = "var(--down)"
        elif s.get("up"):
            color = "var(--up)"
        else:
            color = greys[gi % len(greys)]
            gi += 1
        arcs.append(
            '          <circle cx="%g" cy="%g" r="%g" fill="none" stroke="%s" '
            'stroke-width="%g" stroke-dasharray="%.2f %.2f" stroke-dashoffset="%.2f" '
            'transform="rotate(-90 %g %g)"/>'
            % (cx, cy, r, color, sw, seg, C - seg, -acc, cx, cy))
        acc += seg
        vtxt = s.get("value_text", "%s%%" % fmt_w(v))
        legend.append(
            '          <li><i style="background:%s"></i>'
            '<span class="dn-lab">%s</span><b>%s</b></li>' % (color, s["label"], vtxt))

    center = chart.get("center")
    center_svg = ""
    if center:
        center_svg = (
            '          <text class="dn-center-v" x="%g" y="%g">%s</text>'
            '          <text class="dn-center-l" x="%g" y="%g">%s</text>'
            % (cx, cy + 2, center.get("value", ""), cx, cy + 20, center.get("label", "")))

    return (
        '      <div class="donut-chart">\n'
        '        <svg viewBox="0 0 160 160" xmlns="http://www.w3.org/2000/svg">\n'
        '%s\n%s        </svg>\n'
        '        <ul class="donut-legend">\n%s\n        </ul>\n'
        '      </div>'
        % ("\n".join(arcs), (center_svg + "\n") if center_svg else "", "\n".join(legend)))


def render_chart(block):
    ct = block.get("ct", "")
    cn2 = block.get("cn2", "")
    variant = block.get("variant", "bar")
    if variant == "column":
        body = render_column(block)
    elif variant == "line":
        body = render_line(block)
    elif variant in ("donut", "pie"):
        body = render_donut(block)
    elif block.get("diverging"):
        body = render_diverging_bars(block)
    else:
        body = render_bars(block)
    parts = ['      <div class="chart rv">']
    if ct:
        parts.append('        <div class="ct">%s</div>' % ct)
    if cn2:
        parts.append('        <div class="cn2">%s</div>' % cn2)
    parts.append(body)
    parts.append("      </div>")
    return "\n".join(parts)


def render_note(block):
    h4 = block.get("h4", "")
    ps = block.get("ps", [])
    fig = block.get("fig")
    style = block.get("style")
    style_attr = ' style="%s"' % style if style else ""
    parts = ['        <div class="note rv"%s>' % style_attr]
    if h4:
        parts.append('          <h4>%s</h4>' % h4)
    for i, p in enumerate(ps):
        if i == 0 and fig:
            parts.append('          <p><span class="fig">%s</span>%s</p>' % (fig, p))
        else:
            parts.append('          <p>%s</p>' % p)
    parts.append("        </div>")
    return "\n".join(parts)


def render_acts(block):
    parts = ['    <div class="acts">']
    for it in block["items"]:
        parts.append('      <div class="act rv">')
        parts.append('        <div>')
        parts.append('          <h3>%s</h3>' % it["h3"])
        parts.append('          <p>%s</p>' % it["p"])
        parts.append('        </div>')
        parts.append('      </div>')
    parts.append("    </div>")
    return "\n".join(parts)


def render_block(block):
    t = block["type"]
    if t == "chart":
        return render_chart(block)
    if t == "note":
        return render_note(block)
    if t == "acts":
        return render_acts(block)
    if t == "group":
        inner = "\n".join(render_block(b) for b in block["blocks"])
        return "      <div>\n%s\n      </div>" % inner
    raise ValueError("unknown block type: %r" % t)


def render_pull_quote(pq):
    return (
        '    <div class="pq rv">\n'
        '      <blockquote>%s</blockquote>\n'
        '      <cite>%s</cite>\n'
        '    </div>' % (pq["quote"], pq["cite"])
    )


def render_chapter(ch):
    parts = ['  <section class="ch">']
    parts.append('    <div class="ch-head rv">')
    parts.append('      <div class="ch-num">%s</div>' % ch["num"])
    parts.append('      <div>')
    parts.append('        <h2>%s</h2>' % ch["h2"])
    if ch.get("sub"):
        parts.append('        <p class="sub">%s</p>' % ch["sub"])
    parts.append('      </div>')
    parts.append('    </div>')

    blocks = ch.get("blocks", [])
    # An "acts" chapter has its acts at section level (no .cols wrapper); chart/note
    # chapters wrap their blocks in .cols.
    if blocks and all(b["type"] == "acts" for b in blocks):
        for b in blocks:
            parts.append(render_block(b))
    elif blocks:
        parts.append('    <div class="cols">')
        for b in blocks:
            parts.append(render_block(b))
        parts.append('    </div>')

    if ch.get("pull_quote"):
        parts.append(render_pull_quote(ch["pull_quote"]))

    parts.append('  </section>')
    return "\n".join(parts)


def render_meta_cells(meta):
    out = []
    for m in meta:
        out.append('      <div><b>%s</b><span>%s</span></div>' % (m["b"], m["span"]))
    return "\n".join(out)


def render_stat_cells(stats):
    out = []
    for s in stats:
        b = s["b"]
        tone = s.get("tone")  # optional explicit override: "pos" | "neg" | "neutral"
        first = b.lstrip()[:1]
        is_sign = first in ("+", "−", "-")
        if tone is None:
            # auto by sign: leading + → rise(green), leading − / - → fall(red),
            # otherwise no class → falls back to the positional nth-child color.
            if first == "+":
                tone = "pos"
            elif first in ("−", "-"):
                tone = "neg"
            else:
                tone = ""
        cls = ' class="%s"' % tone if tone else ""
        # Wrap a leading +/− in <span class="sgn">: Montserrat draws U+2212 as a wide
        # bar that visually outweighs the compact +, so render the sign as a small,
        # raised affix to balance the pair. Unsigned numbers are emitted as-is.
        if is_sign:
            stripped = b.lstrip()
            lead = b[:len(b) - len(stripped)]  # preserve rare leading whitespace
            disp = '%s<span class="sgn">%s</span>%s' % (lead, stripped[0], stripped[1:])
        else:
            disp = b
        out.append('    <div class="cell"><b%s>%s</b><span>%s</span></div>' % (cls, disp, s["span"]))
    return "\n".join(out)


ASSETS_DIR = os.path.join(HERE, "..", "assets")


def _img_data_uri(path):
    """Read an image file → a base64 data: URI so the HTML is self-contained (no sibling
    asset to ship). Returns None if the file is missing (caller falls back to a plain src)."""
    import base64
    if not path or not os.path.isfile(path):
        return None
    ext = os.path.splitext(path)[1].lower()
    mime = {".svg": "image/svg+xml", ".png": "image/png",
            ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}.get(ext, "image/svg+xml")
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return "data:%s;base64,%s" % (mime, b64)


def _logo_img(cls, asset_path, alt, fallback_src):
    """Emit an <img>; embed the asset as a data URI when present (self-contained HTML),
    else fall back to a relative src (which then MUST be shipped alongside the HTML)."""
    uri = _img_data_uri(asset_path)
    return '<img class="%s" src="%s" alt="%s">' % (cls, uri or fallback_src, alt)


def build_logo_html(lang, topbar, json_dir):
    """Topbar logo by rule (assets embedded as data URIs → HTML is self-contained):
    - EN report → uhomes.com wordmark only (uhomes-logo-red.svg)
    - CN report → 3-brand combined logo 异乡好居+异乡缴费+异乡人才 (uhomes-cn-combined-logo.svg)
    Content can override: topbar.logo_html (full custom HTML, used verbatim) or topbar.logo_src
    (single img relative to the content JSON, for university/apartment report-type logos)."""
    if topbar.get("logo_html"):
        return topbar["logo_html"]
    if topbar.get("logo_src"):
        src = topbar["logo_src"]
        alt = topbar.get("logo_alt", "uhomes.com")
        return _logo_img("logo", os.path.join(json_dir, src), alt, src)
    if lang == "cn":
        return _logo_img("logo logo-combined",
                         os.path.join(ASSETS_DIR, "uhomes-cn-combined-logo.svg"),
                         "异乡好居 异乡缴费 异乡人才", "uhomes-cn-combined-logo.svg")
    return _logo_img("logo logo-uhomes",
                     os.path.join(ASSETS_DIR, "uhomes-logo-red.svg"),
                     "uhomes.com", "uhomes-logo-red.svg")


def build(content, json_dir):
    lang = content.get("lang", "cn")
    if lang not in PRESETS:
        raise ValueError("lang must be 'cn' or 'en', got %r" % lang)
    style = dict(PRESETS[lang])
    style.update(content.get("style", {}))  # allow per-report overrides

    head = content["head"]
    topbar = content["topbar"]
    hero = content["hero"]
    footer = content["footer"]

    mapping = dict(style)
    mapping.update({
        "lang": head.get("lang_attr", "zh-CN" if lang == "cn" else "en"),
        "meta_description": head["meta_description"],
        "keywords": head.get("keywords", ""),  # optional: comma-separated SEO/social tags
        "og_title": head["og_title"],
        "og_description": head["og_description"],
        "page_title": head["page_title"],
        "logo_html": build_logo_html(lang, topbar, json_dir),
        "issue": topbar["issue"],
        "kicker": hero["kicker"],
        "h1": hero["h1"],
        "deck": hero["deck"],
        "meta_cells": render_meta_cells(hero["meta"]),
        "stat_cells": render_stat_cells(content["stats"]),
        "chapters": "\n\n".join(render_chapter(c) for c in content["chapters"]),
        "footer_brand": footer["brand"],
        "footer_note": footer["note"],
        "footer_tag": footer["tag"],
    })

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        tpl = Template(f.read())
    return tpl.substitute(mapping)


def main():
    ap = argparse.ArgumentParser(description="Render insight HTML from content JSON + template.")
    ap.add_argument("content", help="path to content.<lang>.json")
    ap.add_argument("-o", "--output", help="output HTML path (default: JSON's 'output' key)")
    args = ap.parse_args()

    with open(args.content, "r", encoding="utf-8") as f:
        content = json.load(f)

    json_dir = os.path.dirname(os.path.abspath(args.content))
    html = build(content, json_dir)

    out = args.output or content.get("output")
    if not out:
        print("ERROR: no output path (-o or 'output' key in JSON)", file=sys.stderr)
        sys.exit(1)
    if not os.path.isabs(out):
        out = os.path.join(json_dir, out)

    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote %s (%d bytes)" % (out, len(html.encode("utf-8"))))


if __name__ == "__main__":
    main()
