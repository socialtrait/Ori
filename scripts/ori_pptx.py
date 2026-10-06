#!/usr/bin/env python3
"""Ori v2 PPTX generator (spec: references/office.md, references/design.md).

Mirrors the v2 slide system on a 13.333×7.5in (1280×720px @96dpi) canvas:

  cover      Dawn horizon, centred white lockup over a centred title
  evidence   Horizon #FAFAFA: kicker, assertion title, evidence, takeaway
  statement  Real Black (or Twilight / any horizon): one big sentence
  chapter    Fog: giant numeral + one-word title bottom-left (decks ≥ 12)
  close      Dusk horizon + one Seagrass signal chip (the CTA)

Every slide closes with the folio: Cloud hairline, lockup bottom-left,
legal line centred, page number right. One Seagrass signal per slide —
the generator tracks it and demotes a second one to Real Black.

    python3 scripts/ori_pptx.py [OUT.pptx]

writes a demo exercising every component (default: $TMPDIR/ori-pptx-demo.pptx,
never inside the repo).
"""
import re
import sys
import tempfile
from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import (XL_CHART_TYPE, XL_LABEL_POSITION,
                             XL_LEGEND_POSITION, XL_MARKER_STYLE,
                             XL_TICK_LABEL_POSITION, XL_TICK_MARK)
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

# ── Ori v2 tokens (mirror tokens/ori.css; change there first) ───────
HEX = {
    "black": "1F2937", "dust": "535B65", "mist": "80868F",
    "cloud": "CCCED1", "rule": "E3E5E8", "fog": "F1F2F4",
    "horizon": "FAFAFA", "paper": "FFFFFF", "seagrass": "BAFE81",
    "dawn": "314188", "day": "3E6FE7", "day_deep": "2F5BCC",
    "day_soft": "9DB8F5", "day_wash": "EAF0FD", "dusk": "2A2759",
    "twilight": "070B2F", "pos": "2F7A12", "neg": "C23B32",
    "warn": "9A6206",
}
C = {k: RGBColor.from_string(v) for k, v in HEX.items()}
SERIES = [C["day"], C["dawn"], C["day_soft"], C["cloud"]]   # §7, on light

FONT = "Archivo"
CODE = "JetBrains Mono"

ROOT = Path(__file__).resolve().parent.parent
LOGO = ROOT / "assets" / "logo" / "png"
HORIZON = ROOT / "assets" / "horizon"
LOCKUP_RATIO = 3148 / 480

LEGAL = "Confidential material. Socialtrait © 2026. All rights reserved."
LEGAL_PUBLIC = "Socialtrait © 2026"

W, H = Inches(13.333), Inches(7.5)


def px(v):
    """Template px (1280×720 canvas) → EMU."""
    return Emu(int(round(v * 914400 / 96)))


def pt(v_px):
    """Template px → pt (1px = .75pt)."""
    return v_px * 0.75


# Slide geometry (design.md §4.4: padding 56 72 40)
PAD_T, PAD_X, PAD_B = 56, 72, 40
CW_PX = 1280 - 2 * PAD_X                  # 1136
MX, CW = px(PAD_X), px(CW_PX)
FOLIO_Y = 720 - PAD_B - 26                # hairline y (px)
TAKE_Y = FOLIO_Y - 74                     # takeaway hairline y (px)
BODY_Y = 236                              # evidence body starts (px)

# Slide type scale, design.md §3.3 "Slides 1280×720" (px)
SZ = {"display": 76, "statement": 60, "title": 44, "section": 26,
      "sub": 20, "lede": 20, "body": 18, "small": 15, "label": 12,
      "kicker": 14, "metric": 56, "folio": 9, "chapter": 150}

# Surfaces: background + ink set
SURF = {
    "light":    dict(bg=HEX["horizon"], ink=C["black"], ink2=C["dust"],
                     ink3=C["mist"], rule=C["cloud"], rule_alpha=None,
                     logo="lockup-black.png"),
    "fog":      dict(bg=HEX["fog"], ink=C["black"], ink2=C["dust"],
                     ink3=C["mist"], rule=C["cloud"], rule_alpha=None,
                     logo="lockup-black.png"),
    "black":    dict(bg=HEX["black"], ink=C["horizon"], ink2=C["cloud"],
                     ink3=C["cloud"], rule=C["horizon"], rule_alpha=18,
                     logo="lockup-white.png"),
}
for _h in ("dawn", "dusk", "twilight"):
    SURF[_h] = dict(SURF["black"], bg=HEX[_h], image=f"horizon-{_h}.jpg")
SURF["day"] = dict(bg=HEX["day"], ink=C["black"], ink2=C["black"],
                   ink3=C["black"], rule=C["black"], rule_alpha=25,
                   logo="lockup-black.png", image="horizon-day.jpg")

_MARKUP = re.compile(r"(</?b>)")


# ── low-level XML helpers ────────────────────────────────────────────
_PANOSE = {FONT: ("020B0504020202020204", "34"),     # swiss, variable
           CODE: ("020B0509020102050004", "49")}     # modern, fixed


def _font(run, name=FONT):
    """Typeface on latin/ea/cs + PANOSE/pitch so a machine without the
    font substitutes a grotesque, never a serif."""
    run.font.name = name
    rPr = run._r.get_or_add_rPr()
    latin = rPr.find(qn("a:latin"))
    if name in _PANOSE and latin is not None:
        latin.set("panose", _PANOSE[name][0])
        latin.set("pitchFamily", _PANOSE[name][1])
        latin.set("charset", "0")
    for tag in ("a:ea", "a:cs"):
        el = rPr.find(qn(tag))
        if el is None:
            el = etree.SubElement(rPr, qn(tag))
        el.set("typeface", name)


def _alpha(fill_fore_color_xml_parent, pct):
    """Add <a:alpha> to the srgbClr under a solidFill element."""
    clr = fill_fore_color_xml_parent.find(".//" + qn("a:srgbClr"))
    a = etree.SubElement(clr, qn("a:alpha"))
    a.set("val", str(int(pct * 1000)))


def _no_shadow(shape):
    spPr = shape._element.spPr
    if spPr.find(qn("a:effectLst")) is None:
        etree.SubElement(spPr, qn("a:effectLst"))


def _glow(shape, hex_color, radius_px=18, alpha=55):
    spPr = shape._element.spPr
    eff = spPr.find(qn("a:effectLst"))
    if eff is None:
        eff = etree.SubElement(spPr, qn("a:effectLst"))
    g = etree.SubElement(eff, qn("a:glow"))
    g.set("rad", str(int(px(radius_px))))
    clr = etree.SubElement(g, qn("a:srgbClr"))
    clr.set("val", hex_color)
    a = etree.SubElement(clr, qn("a:alpha"))
    a.set("val", str(alpha * 1000))


class OriDeck:
    """Ori v2 deck.

    occasion        → right-hand meta on every slide (``Q4 review``)
    date, classification → cover meta
    doc_id          → folio prefix (``ST-DECK-012 · 03 / 08``)
    public          → legal line becomes ``Socialtrait © 2026``
    """

    def __init__(self, occasion="Deck", date="", classification="",
                 doc_id="", public=False):
        self.prs = Presentation()
        self.prs.slide_width, self.prs.slide_height = W, H
        self.blank = self.prs.slide_layouts[6]
        self.occasion, self.date = occasion, date
        self.classification, self.doc_id = classification, doc_id
        self.public = public
        self.n = 0
        self._signal = set()        # slide ids that already carry Seagrass
        self._surface = {}          # slide id → surface key
        self._fig = 0

    # ── primitives ──
    def _slide(self, surface="light"):
        s = self.prs.slides.add_slide(self.blank)
        sf = SURF[surface]
        s.background.fill.solid()
        s.background.fill.fore_color.rgb = RGBColor.from_string(sf["bg"])
        if sf.get("image"):
            self._horizon(s, sf["image"])
        self.n += 1
        self._surface[s.slide_id] = surface
        return s

    def _horizon(self, s, name):
        """Full-bleed Solar Horizon photo, cropped to 16:9 from the top so
        the luminous horizon band at the bottom is kept."""
        path = HORIZON / name
        if not path.exists():
            return
        pic = s.shapes.add_picture(str(path), 0, 0, W, H)
        excess = 1 - (2880 / 2048) / (1280 / 720)        # ≈ .209 of height
        pic.crop_top, pic.crop_bottom = excess * .78, excess * .22
        return pic

    def _sf(self, s):
        return SURF[self._surface[s.slide_id]]

    def _use_signal(self, s):
        """True if this slide may still spend its one Seagrass signal."""
        if s.slide_id in self._signal:
            return False
        self._signal.add(s.slide_id)
        return True

    def _rect(self, s, x, y, w, h, fill, radius_px=0, alpha=None):
        shape = MSO_SHAPE.ROUNDED_RECTANGLE if radius_px else MSO_SHAPE.RECTANGLE
        r = s.shapes.add_shape(shape, x, y, w, h)
        if radius_px:
            r.adjustments[0] = min(.5, px(radius_px) / min(w, h))
        r.fill.solid()
        r.fill.fore_color.rgb = fill
        if alpha is not None:
            _alpha(r._element.spPr.find(qn("a:solidFill")), alpha)
        r.line.fill.background()
        _no_shadow(r)
        return r

    def _hair(self, s, x, y_px, w, color, alpha=None, weight_px=1,
              vertical=False):
        """1px hairline at template y (px) — a true line, so it survives
        every renderer and stays editable as a rule in Slides."""
        y = px(y_px)
        x2, y2 = (x, y + w) if vertical else (x + w, y)
        ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x, y, x2, y2)
        ln.line.color.rgb = color
        ln.line.width = Pt(pt(weight_px))
        if alpha is not None:
            _alpha(ln._element.spPr.find(qn("a:ln")), alpha)
        return ln

    def _dot(self, s, x, y, d_px, fill, ring=None):
        o = s.shapes.add_shape(MSO_SHAPE.OVAL, x, y, px(d_px), px(d_px))
        o.fill.solid()
        o.fill.fore_color.rgb = fill
        if ring is not None:
            o.line.color.rgb = ring
            o.line.width = Pt(.75)
        else:
            o.line.fill.background()
        _no_shadow(o)
        return o

    def _style_run(self, r, size_px, color, bold=False, caps=False,
                   track=0.0, font=FONT):
        _font(r, font)
        r.font.size = Pt(pt(size_px))
        r.font.color.rgb = color
        r.font.bold = bold
        r.font.italic = False
        if track:
            r._r.get_or_add_rPr().set("spc", str(int(track * 100)))
        if caps:
            r._r.get_or_add_rPr().set("cap", "all")
        return r

    def _text(self, s, x, y, w, h, paras, align=PP_ALIGN.LEFT,
              anchor=MSO_ANCHOR.TOP, line=None, space_after=0):
        """paras: list of paragraphs; each a list of run tuples
        (text, size_px, color, bold=False, caps=False, track_pt=0)."""
        tb = s.shapes.add_textbox(x, y, w, h)
        tf = tb.text_frame
        tf.word_wrap = True
        tf.auto_size = None
        tf.margin_left = tf.margin_right = 0
        tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = anchor
        if paras and not isinstance(paras[0], list):
            paras = [paras]
        for i, para in enumerate(paras):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = align
            if line:
                p.line_spacing = line
            p.space_after = Pt(space_after)
            for run in para:
                text, size, color, *rest = run
                bold = rest[0] if len(rest) > 0 else False
                caps = rest[1] if len(rest) > 1 else False
                track = rest[2] if len(rest) > 2 else 0
                r = p.add_run()
                r.text = text
                self._style_run(r, size, color, bold, caps, track)
        return tb

    def _rich_runs(self, text, size, color, bold_color=None):
        """<b>…</b> markup → run tuples."""
        out, bold = [], False
        for tok in _MARKUP.split(text):
            if tok in ("<b>", "</b>"):
                bold = tok == "<b>"
                continue
            if tok:
                out.append((tok, size, (bold_color or color) if bold
                            else color, bold))
        return out

    # ── chrome: page head + folio ──
    def _page_head(self, s, kicker, idx=None, meta=None):
        """§5.1 — bold caps kicker top-left; quiet meta right."""
        sf = self._sf(s)
        runs = []
        if idx is not None:
            runs.append((f"{idx:02d}", SZ["kicker"], sf["ink3"], True, True,
                         .3))
            runs.append(("    ", SZ["kicker"], sf["ink"], True))
        runs.append((kicker, SZ["kicker"], sf["ink"], True, True, .3))
        self._text(s, MX, px(PAD_T), px(760), px(22), runs)
        meta = self.occasion if meta is None else meta
        if meta:
            self._text(s, MX + CW - px(420), px(PAD_T + 2), px(420), px(20),
                       [(meta, SZ["label"], sf["ink3"], False, True, .6)],
                       align=PP_ALIGN.RIGHT)

    def _folio(self, s):
        """§5.4 — hairline, lockup left, legal centre, page number right."""
        sf = self._sf(s)
        self._hair(s, MX, FOLIO_Y, CW, sf["rule"], alpha=sf["rule_alpha"])
        logo = LOGO / sf["logo"]
        lh = 14
        if logo.exists():
            s.shapes.add_picture(str(logo), MX, px(FOLIO_Y + 12),
                                 height=px(lh))
        legal = LEGAL_PUBLIC if self.public else LEGAL
        self._text(s, MX + px(240), px(FOLIO_Y + 14), CW - px(480), px(14),
                   [(legal, SZ["folio"], sf["ink"], False, True, .35)],
                   align=PP_ALIGN.CENTER)
        num = f"{self.n:02d} / NN"
        if self.doc_id:
            num = f"{self.doc_id}  ·  {num}"
        self._text(s, MX + CW - px(240), px(FOLIO_Y + 14), px(240), px(14),
                   [(num, SZ["folio"], sf["ink3"], False, True, .35)],
                   align=PP_ALIGN.RIGHT)

    # ── slide archetypes ──
    def cover(self, eyebrow, title, lede="", presenter="", bg="dawn"):
        """Horizon cover: centred lockup over a centred display title."""
        s = self._slide(bg)
        sf = self._sf(s)
        meta = "  ·  ".join(x for x in (self.date, self.classification) if x)
        self._page_head(s, eyebrow, meta=meta)
        lh = 38
        lw = lh * LOCKUP_RATIO
        logo = LOGO / sf["logo"]
        if logo.exists():
            s.shapes.add_picture(str(logo), px((1280 - lw) / 2), px(168),
                                 height=px(lh))
        self._text(s, px(120), px(250), px(1040), px(190),
                   [(title, SZ["display"], sf["ink"], True, False, -1.2)],
                   align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP, line=0.98)
        if lede:
            self._text(s, px(240), px(456), px(800), px(64),
                       [(lede, SZ["lede"], sf["ink2"])],
                       align=PP_ALIGN.CENTER, line=1.3)
        if presenter:
            self._text(s, px(240), px(540), px(800), px(20),
                       [(presenter, SZ["label"], sf["ink2"], True, True,
                         .6)], align=PP_ALIGN.CENTER)
        self._folio(s)
        return s

    def evidence(self, idx, section, title, context_stat=None,
                 context_kicker=None):
        """Light evidence slide. context_stat: (label, value, unit);
        context_kicker: one quiet sentence beside the title."""
        s = self._slide("light")
        self._page_head(s, section, idx=idx)
        side = context_stat or context_kicker
        tw = 860 if side else CW_PX
        self._text(s, MX, px(98), px(tw), px(120),
                   [(title, SZ["title"], C["black"], True, False, -.6)],
                   line=1.02)
        cx, cw = MX + px(900), px(CW_PX - 900)
        if context_stat:
            label, value, unit = context_stat
            self._text(s, cx, px(104), cw, px(18),
                       [(label, SZ["label"], C["mist"], False, True, .6)])
            self._text(s, cx, px(126), cw, px(56),
                       [(value, 40, C["black"], True, False, -.6),
                        (f" {unit}" if unit else "", 18, C["dust"])])
        elif context_kicker:
            self._text(s, cx, px(108), cw, px(100),
                       [(context_kicker, SZ["small"], C["dust"])], line=1.35)
        self._folio(s)
        return s

    def statement(self, idx, section, title, lede="", bg="black"):
        """A dark moment: one sentence at statement size. bg: black (flat
        Real Black) · twilight · dawn · dusk · day."""
        s = self._slide(bg)
        sf = self._sf(s)
        self._page_head(s, section, idx=idx)
        self._text(s, MX, px(190), px(1020), px(250),
                   [(title, SZ["statement"], sf["ink"], True, False, -1)],
                   anchor=MSO_ANCHOR.BOTTOM, line=1.0)
        if lede:
            self._text(s, MX, px(462), px(720), px(90),
                       [(lede, SZ["lede"], sf["ink2"])], line=1.35)
        self._folio(s)
        return s

    def chapter(self, num, title):
        """§5.5 — Fog page, giant numeral + one-word title bottom-left,
        nothing else but the folio. Decks of ≥ 12 slides, max 4."""
        s = self._slide("fog")
        n = f"{num:02d}" if isinstance(num, int) else str(num)
        size = SZ["chapter"]
        self._text(s, MX - px(6), px(FOLIO_Y - 40 - 2 * size * .98),
                   px(1100), px(2 * size),
                   [[(n, size, C["black"], False, False, -3)],
                    [(title, size, C["black"], False, False, -3)]],
                   anchor=MSO_ANCHOR.BOTTOM, line=0.92)
        self._folio(s)
        return s

    def close(self, eyebrow, title, lede="", contact="", cta=None,
              bg="dusk"):
        """Horizon close + one Seagrass signal chip (the CTA)."""
        s = self._slide(bg)
        sf = self._sf(s)
        self._page_head(s, eyebrow)
        self._text(s, MX, px(150), px(1000), px(220),
                   [(title, SZ["statement"], sf["ink"], True, False, -1)],
                   anchor=MSO_ANCHOR.BOTTOM, line=1.0)
        if lede:
            self._text(s, MX, px(390), px(720), px(64),
                       [(lede, SZ["lede"], sf["ink2"])], line=1.35)
        chip = cta or contact
        if chip:
            self.signal(s, chip, MX, px(486))
            if cta and contact:
                self._text(s, MX, px(560), px(600), px(22),
                           [(contact, SZ["small"], sf["ink2"])])
        self._folio(s)
        return s

    # ── signals ──
    def signal(self, s, text, x, y, size=17):
        """Seagrass chip (rounded 12px, glow) with Real Black ink. Counts as
        the slide's one signal; a second request renders a ghost chip."""
        w = px(len(text) * size * .56 + 44)
        h = px(size * 1.3 + 26)
        live = self._use_signal(s)
        r = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
        r.adjustments[0] = px(12) / h
        if live:
            r.fill.solid()
            r.fill.fore_color.rgb = C["seagrass"]
            r.line.fill.background()
            _no_shadow(r)
            _glow(r, HEX["seagrass"], 16, 45)
            ink = C["black"]
        else:
            r.fill.background()
            r.line.color.rgb = self._sf(s)["ink2"]
            r.line.width = Pt(.75)
            _no_shadow(r)
            ink = self._sf(s)["ink"]
        tf = r.text_frame
        tf.margin_left = tf.margin_right = px(22)
        tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.word_wrap = False
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        self._style_run(p.add_run(), size, ink, bold=True)
        p.runs[0].text = text
        return r

    def takeaway(self, s, text, label="Takeaway"):
        """Pinned above the folio: hairline, dot, bold caps label, one
        sentence. The dot is Seagrass unless the slide already spent its
        signal (then Real Black)."""
        self._hair(s, MX, TAKE_Y, CW, C["cloud"])
        dot_fill = C["seagrass"] if self._use_signal(s) else C["black"]
        ring = C["black"] if dot_fill == C["seagrass"] else None
        self._dot(s, MX, px(TAKE_Y + 25), 9, dot_fill, ring=ring)
        self._text(s, MX + px(20), px(TAKE_Y + 22), px(150), px(16),
                   [(label, SZ["label"], C["black"], True, True, .6)])
        self._text(s, MX + px(180), px(TAKE_Y + 17), CW - px(180), px(48),
                   [self._rich_runs(text, SZ["sub"], C["black"])], line=1.2)

    # ── evidence bodies ──
    def metric_row(self, s, metrics, y=None, x=None, w=None):
        """Spec-sheet row: Cloud top rule, Rule bottom rule, hairline
        seams. metrics: [{label, value, unit?, note?, key?}] — exactly one
        ``key`` (legacy ``hero``) gets the Seagrass marker."""
        y = BODY_Y + 24 if y is None else y
        x = MX if x is None else x
        w = CW if w is None else w
        n, hgt = len(metrics), 176
        cw = int(w / n)
        self._hair(s, x, y, w, C["cloud"])
        self._hair(s, x, y + hgt, w, C["rule"])
        for i, m in enumerate(metrics):
            cx = x + i * cw
            pad = 0 if i == 0 else px(22)
            if i:
                self._hair(s, cx, y, px(hgt), C["rule"], vertical=True)
            tx, tw = cx + pad, cw - pad - px(16)
            self._text(s, tx, px(y + 20), tw, px(18),
                       [(m["label"], SZ["label"], C["mist"], False, True,
                         .6)])
            key = (m.get("key") or m.get("hero")) and self._use_signal(s)
            runs = [(m["value"], SZ["metric"], C["black"], True, False,
                     -1)]
            if m.get("unit"):
                runs.append((" " + m["unit"], SZ["metric"] * .45,
                             C["dust"], False))
            if key:                     # marker = rounded Seagrass fill
                est = (len(m["value"]) * SZ["metric"] * .64 +
                       len(m.get("unit", "")) * SZ["metric"] * .45 * .6 +
                       (8 if m.get("unit") else 0) + 18)
                mk = self._rect(s, tx - px(8), px(y + 48), px(est), px(68),
                                C["seagrass"], radius_px=4)
                mk.text_frame.text = ""
            self._text(s, tx, px(y + 50), tw + px(8), px(66), runs,
                       anchor=MSO_ANCHOR.MIDDLE)
            if m.get("note"):
                self._text(s, tx, px(y + 128), tw, px(40),
                           [self._rich_runs(m["note"], SZ["small"],
                                            C["dust"], C["black"])],
                           line=1.25)

    def bullets(self, s, items, x=None, y=None, w=None, size=SZ["body"]):
        """Hanging-indent bullets (Mist dot), Real Black text, <b> markup."""
        x = MX if x is None else x
        y = BODY_Y + 24 if y is None else y
        tb = s.shapes.add_textbox(x, px(y), w or px(1000),
                                  px(TAKE_Y - 24 - y))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = 0
        for i, item in enumerate(items):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.line_spacing, p.space_after = 1.3, Pt(pt(12))
            pPr = p._p.get_or_add_pPr()
            pPr.set("marL", str(int(px(22))))
            pPr.set("indent", str(-int(px(22))))
            bc = etree.SubElement(pPr, qn("a:buClr"))
            etree.SubElement(bc, qn("a:srgbClr")).set("val", HEX["mist"])
            etree.SubElement(pPr, qn("a:buFont")).set("typeface", "Arial")
            etree.SubElement(pPr, qn("a:buChar")).set("char", "•")
            for text, sz, color, bold in self._rich_runs(item, size,
                                                         C["black"]):
                r = p.add_run()
                r.text = text
                self._style_run(r, sz, color, bold)
        return tb

    def quote(self, s, text, cite, x=None, y=None, w=None):
        """Reading-display quote: no marks, no rule; cite caps Mist."""
        x = MX if x is None else x
        y = BODY_Y + 24 if y is None else y
        w = w or px(760)
        self._text(s, x, px(y), w, px(150),
                   [(text, 32, C["black"], False, False, -.3)], line=1.22)
        self._text(s, x, px(y + 160), w, px(18),
                   [("— " + cite, SZ["label"], C["mist"], False, True, .6)])

    def table(self, s, headers, rows, data_cols=(), x=None, y=None,
              w=None, col_widths=None, total=False, key_row=None):
        """Hairline table: caps Mist header over Cloud, Rule dividers,
        numbers right-aligned; total → Real Black top rule + bold;
        key_row → 3px Seagrass bar (counts as the slide's signal)."""
        x = MX if x is None else x
        y = BODY_Y + 24 if y is None else y
        w = w or CW
        nr, nc = len(rows) + 1, len(headers)
        row_h = 44
        gf = s.shapes.add_table(nr, nc, x, px(y), w, px(row_h * nr))
        tbl = gf.table
        tblPr = tbl._tbl.tblPr
        for a in ("firstRow", "bandRow"):
            tblPr.set(a, "0")
        sid = tblPr.find(qn("a:tableStyleId"))
        if sid is None:
            sid = etree.SubElement(tblPr, qn("a:tableStyleId"))
        sid.text = "{2D5ABB26-0587-4C30-8999-92F81FD0307C}"  # no style
        widths = col_widths or [1 / nc] * nc
        for j, f in enumerate(widths):
            tbl.columns[j].width = int(w * f)
        key = key_row is not None and self._use_signal(s)
        last = len(rows) - 1
        for i in range(nr):
            tbl.rows[i].height = px(row_h if i else 34)
            for j in range(nc):
                cell = tbl.cell(i, j)
                cell.margin_left = px(12) if (key and i - 1 == key_row
                                              and j == 0) else 0
                cell.margin_right = 0 if j == nc - 1 else px(16)
                cell.margin_top = cell.margin_bottom = px(6)
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                is_total = total and i - 1 == last
                is_key = key and i - 1 == key_row
                if i == 0:
                    edges = {"B": (HEX["cloud"], 1)}
                else:
                    edges = {"B": (HEX["rule"], 1)}
                    if is_total:
                        edges = {"T": (HEX["black"], 1)}
                    if is_key and j == 0:
                        edges["L"] = (HEX["seagrass"], 3)
                self._cell_lines(cell, edges)
                tf = cell.text_frame
                p = tf.paragraphs[0]
                p.alignment = PP_ALIGN.RIGHT if j in data_cols else \
                    PP_ALIGN.LEFT
                if i == 0:
                    r = p.add_run()
                    r.text = headers[j]
                    self._style_run(r, SZ["label"], C["mist"], False, True,
                                    .6)
                else:
                    for text, sz, color, bold in self._rich_runs(
                            str(rows[i - 1][j]), SZ["small"] + 1,
                            C["black"]):
                        r = p.add_run()
                        r.text = text
                        self._style_run(r, sz, color,
                                        bold or is_total or is_key)
        return gf

    @staticmethod
    def _cell_lines(cell, edges):
        """edges: {L|R|T|B: (hex, width_px)}; all others → no line."""
        tcPr = cell._tc.get_or_add_tcPr()
        for el in list(tcPr):
            if el.tag in {qn(f"a:ln{e}") for e in "LRTB"}:
                tcPr.remove(el)
        first_fill = None
        for el in tcPr:
            first_fill = el
            break
        for e in "LRTB":
            ln = etree.Element(qn(f"a:ln{e}"))
            if e in edges:
                color, wpx = edges[e]
                ln.set("w", str(int(px(wpx))))
                sf = etree.SubElement(ln, qn("a:solidFill"))
                etree.SubElement(sf, qn("a:srgbClr")).set("val", color)
            else:
                ln.set("w", "0")
                etree.SubElement(ln, qn("a:noFill"))
            if first_fill is not None:
                first_fill.addprevious(ln)
            else:
                tcPr.append(ln)
        if tcPr.find(qn("a:noFill")) is None and \
                tcPr.find(qn("a:solidFill")) is None:
            etree.SubElement(tcPr, qn("a:noFill"))

    # ── charts (native, editable in Slides) ──
    def _style_axes(self, chart, value_fmt=None, show_value_axis=True):
        ca, va = chart.category_axis, chart.value_axis
        for ax in (ca, va):
            ax.tick_labels.font.size = Pt(pt(13))
            ax.tick_labels.font.name = FONT
            ax.tick_labels.font.color.rgb = C["mist"]
            ax.major_tick_mark = XL_TICK_MARK.NONE
            ax.minor_tick_mark = XL_TICK_MARK.NONE
        ca.format.line.color.rgb = C["cloud"]            # baseline
        ca.format.line.width = Pt(.75)
        va.format.line.fill.background()                 # no value spine
        va.has_major_gridlines = True
        va.major_gridlines.format.line.color.rgb = C["rule"]
        va.major_gridlines.format.line.width = Pt(.75)
        if value_fmt:
            va.tick_labels.number_format = value_fmt
            va.tick_labels.number_format_is_linked = False
        if not show_value_axis:
            va.tick_label_position = XL_TICK_LABEL_POSITION.NONE

    def _legend(self, chart, n):
        chart.has_legend = n > 1
        if chart.has_legend:
            chart.legend.position = XL_LEGEND_POSITION.TOP
            chart.legend.include_in_layout = False
            chart.legend.font.size = Pt(pt(13))
            chart.legend.font.name = FONT
            chart.legend.font.color.rgb = C["dust"]

    def bar_chart(self, s, categories, series, x=None, y=None, w=None,
                  h=None, highlight=None, horizontal=False,
                  number_format='0'):
        """series: [(name, [values])]. Multi-series → Day, Dawn, Day-soft,
        Cloud. Single series + highlight=i → bar i in Day, rest Cloud."""
        data = CategoryChartData(number_format=number_format)
        data.categories = categories
        for name, vals in series:
            data.add_series(name, vals)
        kind = (XL_CHART_TYPE.BAR_CLUSTERED if horizontal
                else XL_CHART_TYPE.COLUMN_CLUSTERED)
        gf = s.shapes.add_chart(
            kind, MX if x is None else x, px(BODY_Y + 16 if y is None else y),
            w or px(620), h or px(TAKE_Y - 40 - (BODY_Y + 16)), data)
        chart = gf.chart
        chart.has_title = False
        self._chart_frame(chart)
        plot = chart.plots[0]
        plot.gap_width = 80                       # gap ≥ 40% of bar width
        plot.overlap = -10 if len(series) > 1 else 0
        plot.vary_by_categories = False
        plot.has_data_labels = True
        dl = plot.data_labels
        dl.font.size = Pt(pt(13))
        dl.font.bold = True
        dl.font.name = FONT
        dl.font.color.rgb = C["black"]
        dl.number_format = number_format
        dl.number_format_is_linked = False
        dl.position = XL_LABEL_POSITION.OUTSIDE_END
        for i, srs in enumerate(chart.series):
            srs.format.fill.solid()
            if len(series) == 1 and highlight is not None:
                srs.format.fill.fore_color.rgb = C["cloud"]
                pnt = srs.points[highlight]
                pnt.format.fill.solid()
                pnt.format.fill.fore_color.rgb = C["day"]
            else:
                srs.format.fill.fore_color.rgb = SERIES[i % len(SERIES)]
            srs.format.line.fill.background()
        self._style_axes(chart, show_value_axis=False)
        chart.value_axis.has_major_gridlines = not horizontal
        self._legend(chart, len(series))
        return gf

    def line_chart(self, s, categories, series, x=None, y=None, w=None,
                   h=None, highlight=0, number_format='0', value_range=None):
        """Lines 2.5px; highlight series in Day, others step down the ramp.
        Direct labels (series name + last value) at the line ends replace
        the legend (≤ 3 series); end-point dot on the highlight series."""
        data = CategoryChartData(number_format=number_format)
        data.categories = categories
        for name, vals in series:
            data.add_series(name, vals)
        gf = s.shapes.add_chart(
            XL_CHART_TYPE.LINE, MX if x is None else x,
            px(BODY_Y + 16 if y is None else y), w or px(620),
            h or px(TAKE_Y - 40 - (BODY_Y + 16)), data)
        chart = gf.chart
        chart.has_title = False
        self._chart_frame(chart)
        rest = [C["dawn"], C["day_soft"], C["cloud"]]
        k = 0
        for i, srs in enumerate(chart.series):
            srs.smooth = False
            ln = srs.format.line
            ln.width = Pt(pt(2.5))
            hi = i == highlight
            if hi:
                color = C["day"]
            else:
                color, k = rest[k % len(rest)], k + 1
            ln.color.rgb = color
            srs.marker.style = XL_MARKER_STYLE.NONE
            end = srs.points[len(categories) - 1]
            if hi:
                end.marker.style = XL_MARKER_STYLE.CIRCLE
                end.marker.size = 7
                end.marker.format.fill.solid()
                end.marker.format.fill.fore_color.rgb = C["day"]
                end.marker.format.line.color.rgb = C["horizon"]
                end.marker.format.line.width = Pt(1.5)
            dl = end.data_label
            dl.position = XL_LABEL_POSITION.RIGHT
            dl.font.size = Pt(pt(13))
            dl.font.bold = hi
            dl.font.name = FONT
            dl.font.color.rgb = C["black"] if hi else C["dust"]
            dLbl = dl._get_or_add_dLbl()
            for tag in ("c:showVal", "c:showSerName"):
                el = dLbl.find(qn(tag))
                if el is not None:
                    el.set("val", "1")
            sep = etree.SubElement(dLbl, qn("c:separator"))
            sep.text = "  "
            ext = dLbl.find(qn("c:extLst"))
            if ext is not None:
                ext.addprevious(sep)
        self._style_axes(chart, value_fmt=number_format)
        if value_range:
            chart.value_axis.minimum_scale = value_range[0]
            chart.value_axis.maximum_scale = value_range[1]
        chart.has_legend = False
        # leave room on the right for the direct labels
        pa = chart._chartSpace.chart.plotArea
        lay = pa.find(qn("c:layout"))
        if lay is None:
            lay = etree.Element(qn("c:layout"))
            pa.insert(0, lay)
        ml = etree.SubElement(lay, qn("c:manualLayout"))
        for tag, val in (("c:layoutTarget", "inner"), ("c:xMode", "edge"),
                         ("c:yMode", "edge"), ("c:x", "0.07"),
                         ("c:y", "0.05"), ("c:w", "0.68"), ("c:h", "0.82")):
            etree.SubElement(ml, qn(tag)).set("val", val)
        return gf

    def _chart_frame(self, chart):
        """Transparent chart + plot area, no border, Archivo text."""
        cs = chart._chartSpace
        chart.font.name = FONT
        chart.font.size = Pt(pt(13))
        chart.font.color.rgb = C["mist"]
        for parent, after in ((cs, cs.find(qn("c:chart"))),
                              (cs.chart.plotArea, None)):
            spPr = parent.find(qn("c:spPr"))
            if spPr is None:
                spPr = etree.Element(qn("c:spPr"))
                if after is not None:
                    after.addnext(spPr)
                else:
                    ext = parent.find(qn("c:extLst"))
                    (ext.addprevious(spPr) if ext is not None
                     else parent.append(spPr))
            etree.SubElement(spPr, qn("a:noFill"))
            ln = etree.SubElement(spPr, qn("a:ln"))
            etree.SubElement(ln, qn("a:noFill"))

    def donut_chart(self, s, categories, values, center_value="",
                    center_label="", x=None, y=None, d=None,
                    highlight=0):
        """Ring, ≤ 5 segments; highlight segment Day, rest down the ramp;
        metric centred in the display cut."""
        data = CategoryChartData(number_format='0')
        data.categories = categories
        data.add_series("share", values)
        d = d or px(300)
        x = MX if x is None else x
        y = px(BODY_Y + 20 if y is None else y)
        gf = s.shapes.add_chart(XL_CHART_TYPE.DOUGHNUT, x, y, d, d, data)
        chart = gf.chart
        chart.has_title = False
        chart.has_legend = False
        self._chart_frame(chart)
        ramp = [C["day"], C["dawn"], C["day_soft"], C["cloud"], C["rule"]]
        order = [highlight] + [i for i in range(len(values))
                               if i != highlight]
        srs = chart.plots[0].series[0]
        for rank, i in enumerate(order):
            p = srs.points[i]
            p.format.fill.solid()
            p.format.fill.fore_color.rgb = ramp[rank % len(ramp)]
            p.format.line.color.rgb = C["horizon"]
            p.format.line.width = Pt(1.5)
        dn = chart.plots[0]._element
        hole = dn.find(qn("c:holeSize"))
        if hole is None:
            hole = etree.SubElement(dn, qn("c:holeSize"))
        hole.set("val", "72")
        if center_value:
            self._text(s, x, y + int(d / 2) - px(40), d, px(52),
                       [(center_value, 44, C["black"], True, False, -.6)],
                       align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        if center_label:
            self._text(s, x + px(50), y + int(d / 2) + px(14), d - px(100),
                       px(18), [(center_label, SZ["label"], C["mist"],
                                 False, True, .6)], align=PP_ALIGN.CENTER)
        return gf

    def legend_list(self, s, items, x, y, w=px(360)):
        """Direct labels for a donut: [(color_key, label, value)]."""
        for i, (ck, label, value) in enumerate(items):
            yy = y + i * 40
            self._dot(s, x, px(yy + 6), 10, C[ck])
            self._text(s, x + px(22), px(yy), w - px(70), px(24),
                       [(label, SZ["small"] + 1, C["black"])])
            self._text(s, x + w - px(48), px(yy), px(48), px(24),
                       [(value, SZ["small"] + 1, C["black"], True)],
                       align=PP_ALIGN.RIGHT)
            self._hair(s, x, yy + 32, w, C["rule"])

    def figcap(self, s, caption, source="", x=None, y=None, w=None,
               idx=None):
        """Bold ``Fig 01`` + one-sentence caption; source right, Mist."""
        x = MX if x is None else x
        w = w or px(620)
        y = TAKE_Y - 34 if y is None else y
        self._fig = idx if idx is not None else self._fig + 1
        self._text(s, x, px(y), w, px(18),
                   [(f"Fig {self._fig:02d}   ", 13, C["black"], True),
                    (caption, 13, C["dust"])])
        if source:
            self._text(s, x, px(y), w, px(18),
                       [(f"Source: {source}", 12, C["mist"])],
                       align=PP_ALIGN.RIGHT)

    # ── save ──
    def save(self, path):
        total = f"{self.n:02d}"
        for slide in self.prs.slides:
            for shape in slide.shapes:
                if shape.has_text_frame and "/ NN" in shape.text_frame.text:
                    for p in shape.text_frame.paragraphs:
                        for r in p.runs:
                            r.text = r.text.replace("NN", total)
        self.prs.core_properties.author = "Socialtrait"
        self.prs.core_properties.comments = "Ori 2"
        self.prs.save(str(path))
        return str(path)


# ── demo / visual regression check ──────────────────────────────────
def demo(out):
    d = OriDeck(occasion="Q4 pilot review", date="2026-10-07",
                classification="Confidential", doc_id="ST-DECK-012")
    d.prs.core_properties.title = "Simulation predicted the market"
    d.cover("Pilot results", "Simulation predicted the market. Three "
            "times out of three.",
            "Q4 audience-simulation pilot results and the case for a "
            "ten-account expansion.", "Suraj N. · Socialtrait")

    s = d.evidence(1, "Headline numbers", "Three pilots, one pattern: the "
                   "simulation called every winner",
                   context_kicker="Enterprise pilots across CPG, fintech, "
                   "and retail — 12 audience cells, Jul–Sep 2026.")
    d.metric_row(s, [
        {"label": "Prediction accuracy", "value": "87", "unit": "%",
         "note": "interval coverage 11/12 cells", "key": True},
        {"label": "Time to insight", "value": "4", "unit": "hrs",
         "note": "panels took 19 days median"},
        {"label": "Media saved", "value": "$340", "unit": "k",
         "note": "one flagged creative, one pilot"},
    ])
    d.takeaway(s, "Simulation is accurate enough to gate media spend "
               "<b>today</b>.")

    s = d.evidence(2, "Speed", "Answers land inside the campaign cycle, "
                   "not after it",
                   context_stat=("Median time to insight", "4", "hrs"))
    d.bar_chart(s, ["Field study", "Online panel", "Agency recall",
                    "Socialtrait"],
                [("Variants tested per campaign", [2, 4, 3, 24])],
                highlight=3, w=px(640), h=px(270))
    d.figcap(s, "Creative variants tested per campaign.", "pilots, 2026",
             w=px(640), y=TAKE_Y - 36)
    d.bullets(s, ["Nine-day median creative iteration at pilot clients",
                  "Panels answer <b>after</b> the decision; simulation "
                  "answers before",
                  "Same-day re-tests after every creative revision"],
              x=MX + px(700), w=px(436), size=17)
    d.takeaway(s, "Research finally moves at the speed the campaign "
               "already does.")

    d.chapter(2, "Evidence")

    s = d.evidence(3, "Accuracy over time", "Accuracy held as the panel "
                   "scaled from one to twelve cells")
    d.line_chart(s, ["Jul", "Aug", "Sep", "Oct"],
                 [("Simulation", [78, 83, 85, 87]),
                  ("Online panel", [74, 75, 73, 74])], w=px(640),
                 h=px(270), value_range=(60, 95))
    d.figcap(s, "Interval coverage by month, %.", "pilot holdouts",
             w=px(640), y=TAKE_Y - 36)
    d.donut_chart(s, ["CPG", "Fintech", "Retail"], [6, 4, 2],
                  center_value="12", center_label="Cells",
                  x=MX + px(700), y=BODY_Y + 16, d=px(250))
    d.legend_list(s, [("day", "CPG", "6"), ("dawn", "Fintech", "4"),
                      ("day_soft", "Retail", "2")],
                  MX + px(976), BODY_Y + 76, w=px(160))
    d.takeaway(s, "More cells did not dilute accuracy — the model "
               "generalises.")

    s = d.evidence(4, "Economics", "The expansion pays back inside one "
                   "quarter")
    d.table(s, ["Account", "Studies", "Fee", "Media at risk"],
            [["Arlo Foods", "8", "$44k", "$1.2M"],
             ["Northwind Bank", "6", "$36k", "$0.9M"],
             ["Ten-account plan", "64", "$380k", "$9.6M"],
             ["Total", "78", "$460k", "$11.7M"]],
            data_cols=(1, 2, 3), col_widths=[.4, .16, .2, .24],
            total=True, key_row=2, w=px(760))
    d.quote(s, "We stopped arguing about creative and started testing it.",
            "Dana · VP Growth, CPG pilot", x=MX + px(820), w=px(316),
            y=BODY_Y + 24)
    d.takeaway(s, "Fee is under 4% of the media it protects.")

    d.statement(5, "The point", "Simulation is not a cheaper panel. It is "
                "an earlier one.", "Decisions move upstream of the media "
                "flight — that is the product.")
    d.statement(6, "Twilight variant", "The model is the moat; the panel "
                "is the proof.", bg="twilight")
    d.close("Decision requested", "Expand the pilot. Ten accounts, this "
            "quarter.", "Approval needed by October 18 · detail in "
            "ST-OP-014.", contact="suraj@socialtrait.ai",
            cta="Approve the ten-account expansion")
    return d.save(out)


if __name__ == "__main__":
    # demos never land in the repo: default to the system temp dir
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else (
        Path(tempfile.gettempdir()) / "ori-pptx-demo.pptx")
    print("wrote", demo(target))
