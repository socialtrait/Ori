#!/usr/bin/env python3
"""Ori v2 DOCX generator (spec: references/office.md, references/design.md).

Encodes the Ori v2 token system for Word / Google Docs. Agents import
OriDoc and compose documents from the same components the HTML templates
use: page head, title, lede, metric row, section head, body, callout (+ the
ask), table, quote, spec list, figure, chapter opener, folio, and the
meeting-minutes set (logistics, agenda, decisions, actions, smallprint).

docx is a *light* medium: Horizon canvas, Real Black ink, one Seagrass
signal per page, hairlines for structure. Horizons and dark surfaces never
appear in docx (print rule).

    python3 scripts/ori_docx.py [OUT.docx]

writes a demo exercising every component (default: $TMPDIR/ori-docx-demo.docx,
never inside the repo).
"""
import re
import sys
import tempfile
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_ROW_HEIGHT_RULE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor

# ── Ori v2 tokens (mirror tokens/ori.css; change there first) ───────
HEX = {
    "black": "1F2937",     # Real Black — primary text
    "dust": "535B65",      # secondary text
    "mist": "80868F",      # captions, labels, page numbers
    "cloud": "CCCED1",     # strong hairline
    "rule": "E3E5E8",      # default hairline
    "fog": "F1F2F4",       # panel fill
    "horizon": "FAFAFA",   # the light canvas
    "paper": "FFFFFF",
    "seagrass": "BAFE81",  # the one signal (fill under black ink)
    "dawn": "314188",
    "day": "3E6FE7",
    "day_deep": "2F5BCC",  # links / blue text on light
    "day_soft": "9DB8F5",
    "pos": "2F7A12",
    "neg": "C23B32",
    "warn": "9A6206",
}
C = {k: RGBColor.from_string(v) for k, v in HEX.items()}

FONT = "Archivo"            # SF Pro's open fallback; on Google Fonts
CODE = "JetBrains Mono"     # code only

ROOT = Path(__file__).resolve().parent.parent
LOGO = ROOT / "assets" / "logo" / "png"

LEGAL = "Confidential material. Socialtrait © 2026. All rights reserved."
LEGAL_PUBLIC = "Socialtrait © 2026"

MARGINS = {  # T, R, B, L in mm — design.md §4.4
    "one-pager": (14, 16, 12, 16),
    "long-doc": (18, 20, 14, 20),
    "report": (16, 18, 14, 18),
    "resume": (12, 14, 10, 14),
    "minutes": (16, 18, 14, 18),
}

# Print scale, design.md §3.3 (pt)
SZ = {"title": 26, "section": 15, "sub": 11, "lede": 12, "body": 9.5,
      "small": 8.5, "label": 7, "kicker": 9, "metric": 26, "folio": 6,
      "quote": 14, "callout": 10.5}

# ── OOXML child order (Word rejects out-of-order children) ──────────
_ORDER = {
    "w:rPr": ["w:rStyle", "w:rFonts", "w:b", "w:bCs", "w:i", "w:iCs",
              "w:caps", "w:smallCaps", "w:strike", "w:dstrike", "w:outline",
              "w:shadow", "w:emboss", "w:imprint", "w:noProof",
              "w:snapToGrid", "w:vanish", "w:webHidden", "w:color",
              "w:spacing", "w:w", "w:kern", "w:position", "w:sz", "w:szCs",
              "w:highlight", "w:u", "w:effect", "w:bdr", "w:shd",
              "w:fitText", "w:vertAlign", "w:rtl", "w:cs", "w:em", "w:lang"],
    "w:pPr": ["w:pStyle", "w:keepNext", "w:keepLines", "w:pageBreakBefore",
              "w:framePr", "w:widowControl", "w:numPr",
              "w:suppressLineNumbers", "w:pBdr", "w:shd", "w:tabs",
              "w:suppressAutoHyphens", "w:kinsoku", "w:wordWrap",
              "w:overflowPunct", "w:topLinePunct", "w:autoSpaceDE",
              "w:autoSpaceDN", "w:bidi", "w:adjustRightInd", "w:snapToGrid",
              "w:spacing", "w:ind", "w:contextualSpacing", "w:mirrorIndents",
              "w:suppressOverlap", "w:jc", "w:textDirection",
              "w:textAlignment", "w:textboxTightWrap", "w:outlineLvl",
              "w:divId", "w:cnfStyle", "w:rPr", "w:sectPr", "w:pPrChange"],
    "w:tcPr": ["w:cnfStyle", "w:tcW", "w:gridSpan", "w:hMerge", "w:vMerge",
               "w:tcBorders", "w:shd", "w:noWrap", "w:tcMar",
               "w:textDirection", "w:tcFitText", "w:vAlign", "w:hideMark"],
    "w:tblPr": ["w:tblStyle", "w:tblpPr", "w:tblOverlap", "w:bidiVisual",
                "w:tblStyleRowBandSize", "w:tblStyleColBandSize", "w:tblW",
                "w:jc", "w:tblCellSpacing", "w:tblInd", "w:tblBorders",
                "w:shd", "w:tblLayout", "w:tblCellMar", "w:tblLook"],
}


def _set_child(parent, tag, order_key):
    """Replace-or-insert child `tag` at its schema position; return it."""
    old = parent.find(qn(tag))
    if old is not None:
        parent.remove(old)
    el = OxmlElement(tag)
    seq = _ORDER[order_key]
    later = seq[seq.index(tag) + 1:]
    for sib in parent:
        if sib.tag in {qn(t) for t in later}:
            sib.addprevious(el)
            return el
    parent.append(el)
    return el


def _edges(parent, spec):
    """spec: {edge: (sz_eighths, hex) | None}. None → val=none."""
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        if edge not in spec:
            continue
        el = OxmlElement(f"w:{edge}")
        if spec[edge] is None:
            el.set(qn("w:val"), "nil")
        else:
            sz, color = spec[edge]
            el.set(qn("w:val"), "single")
            el.set(qn("w:sz"), str(sz))
            el.set(qn("w:space"), "0")
            el.set(qn("w:color"), color)
        parent.append(el)


HAIR = 6          # 1px ≈ 0.75pt = 6 eighths
NONE_ALL = {e: None for e in ("top", "left", "bottom", "right",
                              "insideH", "insideV")}


def _tbl_borders(table, spec):
    b = _set_child(table._tbl.tblPr, "w:tblBorders", "w:tblPr")
    _edges(b, {**NONE_ALL, **spec})


def _tbl_cell_margins(table, top=0, left=0, bottom=0, right=0):
    m = _set_child(table._tbl.tblPr, "w:tblCellMar", "w:tblPr")
    for edge, v in (("top", top), ("left", left), ("bottom", bottom),
                    ("right", right)):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:w"), str(int(v * 20)))
        el.set(qn("w:type"), "dxa")
        m.append(el)


def _tbl_fixed(table, width_emu):
    tblPr = table._tbl.tblPr
    w = _set_child(tblPr, "w:tblW", "w:tblPr")
    w.set(qn("w:w"), str(int(width_emu / 635)))   # EMU → twips
    w.set(qn("w:type"), "dxa")
    ind = _set_child(tblPr, "w:tblInd", "w:tblPr")
    ind.set(qn("w:w"), "0")
    ind.set(qn("w:type"), "dxa")
    lay = _set_child(tblPr, "w:tblLayout", "w:tblPr")
    lay.set(qn("w:type"), "fixed")
    table.autofit = False


def _cell_borders(cell, spec):
    b = _set_child(cell._tc.get_or_add_tcPr(), "w:tcBorders", "w:tcPr")
    _edges(b, spec)


def _cell_shade(cell, hex_fill):
    s = _set_child(cell._tc.get_or_add_tcPr(), "w:shd", "w:tcPr")
    s.set(qn("w:val"), "clear")
    s.set(qn("w:color"), "auto")
    s.set(qn("w:fill"), hex_fill)


def _cell_margins(cell, top=None, left=None, bottom=None, right=None):
    m = _set_child(cell._tc.get_or_add_tcPr(), "w:tcMar", "w:tcPr")
    for edge, v in (("top", top), ("left", left), ("bottom", bottom),
                    ("right", right)):
        if v is None:
            continue
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:w"), str(int(v * 20)))
        el.set(qn("w:type"), "dxa")
        m.append(el)


def _p_border(paragraph, edge, sz, color, space=4):
    pPr = paragraph._p.get_or_add_pPr()
    bdr = pPr.find(qn("w:pBdr"))
    if bdr is None:
        bdr = _set_child(pPr, "w:pBdr", "w:pPr")
    el = OxmlElement(f"w:{edge}")
    el.set(qn("w:val"), "single")
    el.set(qn("w:sz"), str(sz))
    el.set(qn("w:space"), str(space))
    el.set(qn("w:color"), color)
    # pBdr children order: top, left, bottom, right, between
    order = ["top", "left", "bottom", "right", "between"]
    for sib in bdr:
        if order.index(sib.tag.split("}")[1]) > order.index(edge):
            sib.addprevious(el)
            break
    else:
        bdr.append(el)


def _font(run, name=FONT):
    run.font.name = name
    rf = run._r.get_or_add_rPr().get_or_add_rFonts()
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(a), name)


def _tracking(run, pt):
    sp = _set_child(run._r.get_or_add_rPr(), "w:spacing", "w:rPr")
    sp.set(qn("w:val"), str(int(round(pt * 20))))


def _run_shade(run, hex_fill):
    s = _set_child(run._r.get_or_add_rPr(), "w:shd", "w:rPr")
    s.set(qn("w:val"), "clear")
    s.set(qn("w:color"), "auto")
    s.set(qn("w:fill"), hex_fill)


def _field(paragraph, instr, cached="1"):
    """PAGE / NUMPAGES field with a cached result (shown by renderers that
    don't compute fields)."""
    runs = []
    for kind in ("begin", "instr", "separate", "text", "end"):
        r = paragraph.add_run()
        if kind == "instr":
            it = OxmlElement("w:instrText")
            it.set(qn("xml:space"), "preserve")
            it.text = f" {instr} "
            r._r.append(it)
        elif kind == "text":
            r.text = cached
        else:
            fc = OxmlElement("w:fldChar")
            fc.set(qn("w:fldCharType"), kind)
            r._r.append(fc)
        runs.append(r)
    return runs


def _clear_style_tabs(style):
    pPr = style.element.get_or_add_pPr()
    tabs = pPr.find(qn("w:tabs"))
    if tabs is not None:
        pPr.remove(tabs)


_MARKUP = re.compile(r"(</?b>|</?hl>)")


# ── the document builder ─────────────────────────────────────────────
class OriDoc:
    """Ori v2 Word document.

    doc_type   → the page-head kicker (``Statement of work``)
    doc_id     → folio doc-id (``ST-SOW-007``)
    date, classification, meta → right-aligned page-head metadata
    artifact   → one-pager | long-doc | report | minutes | resume
    public     → folio legal line becomes ``Socialtrait © 2026``
    candidate  → resume only: name in the unbranded folio
    """

    def __init__(self, doc_type="Document", doc_id="ST-DOC-000", date="",
                 classification="Internal", artifact="long-doc", meta=(),
                 public=False, candidate=""):
        self.doc = Document()
        self.doc_type, self.doc_id = doc_type, doc_id
        self.artifact = artifact
        self.resume = artifact == "resume"
        self.public, self.candidate = public, candidate
        self.meta = [x for x in (*meta, date, classification) if x]

        sec = self.doc.sections[0]
        sec.page_width, sec.page_height = Mm(210), Mm(297)
        t, r, b, l = MARGINS.get(artifact, MARGINS["long-doc"])
        sec.top_margin, sec.right_margin = Mm(t), Mm(r)
        sec.bottom_margin, sec.left_margin = Mm(b), Mm(l)
        sec.header_distance = Mm(max(5, t - 9))
        sec.footer_distance = Mm(max(4, b - 8))
        self._usable = sec.page_width - sec.left_margin - sec.right_margin
        self._usable_h = sec.page_height - sec.top_margin - sec.bottom_margin

        self._base_styles()
        self._font_table()
        self._canvas()
        if not self.resume:
            self._page_head(sec.header)
        self._folio(sec.footer)
        self.doc.core_properties.author = "Socialtrait"
        self.doc.core_properties.comments = "Ori 2"

    # ── setup ──
    def _base_styles(self):
        st = self.doc.styles
        n = st["Normal"]
        n.font.name, n.font.size = FONT, Pt(SZ["body"])
        n.font.color.rgb = C["black"]
        rf = n.element.get_or_add_rPr().get_or_add_rFonts()
        for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            rf.set(qn(a), FONT)
        for a in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme",
                  "w:eastAsiaTheme"):
            if rf.get(qn(a)) is not None:
                del rf.attrib[qn(a)]
        pf = n.paragraph_format
        pf.space_before, pf.space_after = Pt(0), Pt(7)
        pf.line_spacing_rule = WD_LINE_SPACING.AT_LEAST
        pf.line_spacing = Pt(SZ["body"] * 1.5)
        for name in ("Header", "Footer"):
            _clear_style_tabs(st[name])
            st[name].paragraph_format.space_after = Pt(0)

    def _font_table(self):
        """Declare Archivo / JetBrains Mono with sans / mono PANOSE so a
        machine without them substitutes a grotesque, never a serif."""
        part = None
        for rel in self.doc.part.rels.values():
            if rel.reltype.endswith("/fontTable"):
                part = rel.target_part
        if part is None:
            return
        from lxml import etree
        root = etree.fromstring(part.blob)
        W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
        for name, panose, fam, pitch in (
                (FONT, "020B0504020202020204", "swiss", "variable"),
                (CODE, "020B0509020102050004", "modern", "fixed")):
            f = etree.SubElement(root, f"{{{W}}}font")
            f.set(f"{{{W}}}name", name)
            for tag, val in (("panose1", panose), ("charset", "00"),
                             ("family", fam), ("pitch", pitch)):
                e = etree.SubElement(f, f"{{{W}}}{tag}")
                e.set(f"{{{W}}}val", val)
        part._blob = etree.tostring(root, xml_declaration=True,
                                    encoding="UTF-8", standalone=True)

    def _canvas(self):
        """Horizon page colour (Word shows it on screen; Google Docs keeps
        it as page colour). Prints white unless background printing is on —
        accepted: print pages are light either way."""
        bg = OxmlElement("w:background")
        bg.set(qn("w:color"), HEX["horizon"])
        self.doc.element.insert(0, bg)
        settings = self.doc.settings.element
        dbs = OxmlElement("w:displayBackgroundShape")
        before = [qn(f"w:{t}") for t in (
            "writeProtection", "view", "zoom", "removePersonalInformation",
            "removeDateAndTime", "doNotDisplayPageBoundaries")]
        prev = [el for el in settings if el.tag in before]
        if prev:
            prev[-1].addnext(dbs)
        else:
            settings.insert(0, dbs)

    def _tabbed(self, p, stops):
        for pos, align in stops:
            p.paragraph_format.tab_stops.add_tab_stop(pos, align)

    def _page_head(self, header):
        """§5.1 — kicker left, quiet meta right in Mist. No rule beneath."""
        header.is_linked_to_previous = False
        p = header.paragraphs[0]
        for r in list(p.runs):
            r._r.getparent().remove(r._r)
        self._tabbed(p, [(self._usable, WD_TAB_ALIGNMENT.RIGHT)])
        self._label(p, self.doc_type, C["black"], SZ["kicker"], bold=True,
                    track=0.2)
        if self.meta:
            self._label(p, "\t" + "  ·  ".join(self.meta), C["mist"],
                        SZ["label"])

    def _folio(self, footer):
        """§5.4 — Cloud hairline, lockup left, legal line centred, doc-id
        and page X / Y right. Resumes: candidate name left, no lockup."""
        p = footer.paragraphs[0]
        pf = p.paragraph_format
        pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
        stops = [(self._usable, WD_TAB_ALIGNMENT.RIGHT)]
        if not self.resume:
            stops.insert(0, (int(self._usable / 2), WD_TAB_ALIGNMENT.CENTER))
        self._tabbed(p, stops)
        _p_border(p, "top", HAIR, HEX["cloud"], space=6)
        f, mist, black = SZ["folio"], C["mist"], C["black"]
        if self.resume:                      # unbranded: name left, X / Y
            self._label(p, self.candidate or self.doc_type, black, f,
                        track=0.25)
            self._label(p, "\t", black, f)
        else:
            lockup = LOGO / "lockup-black.png"
            if lockup.exists():
                pic = p.add_run().add_picture(str(lockup), height=Pt(9))
                pic.width = int(Pt(9) * 3148 / 480)
            legal = LEGAL_PUBLIC if self.public else LEGAL
            self._label(p, "\t" + legal, black, f, track=0.25)
            self._label(p, f"\t{self.doc_id}  ·  ", mist, f, track=0.25)
        for instr, cached in (('PAGE \\# "00"', "01"),
                              (None, None),
                              ('NUMPAGES \\# "00"', "01")):
            if instr is None:
                self._label(p, " / ", mist, f, track=0.25)
                continue
            for r in _field(p, instr, cached):
                self._style(r, f, mist, caps=True)

    # ── run helpers ──
    @staticmethod
    def _style(run, size, color, bold=False, caps=False, font=FONT):
        _font(run, font)
        run.font.size = Pt(size)
        run.font.color.rgb = color
        run.font.bold = bold
        run.font.italic = False           # italics are banned
        if caps:
            run.font.all_caps = True
        return run

    def _label(self, p, text, color, size=SZ["label"], bold=False,
               track=0.42):
        """Body 1 voice: caps, opened tracking (+.06em)."""
        r = self._style(p.add_run(text), size, color, bold=bold, caps=True)
        _tracking(r, track)
        return r

    def _rich(self, p, text, size, color, bold_color=None):
        """Markup: <b>emphasis</b> (bold, the 650 voice) and <hl>marker</hl>
        (Seagrass fill under Real Black — once per page)."""
        bold = hl = False
        for tok in _MARKUP.split(text):
            if tok in ("<b>", "</b>"):
                bold = tok == "<b>"
                continue
            if tok in ("<hl>", "</hl>"):
                hl = tok == "<hl>"
                continue
            if not tok:
                continue
            if hl:
                tok = f" {tok} "
            c = (bold_color or color) if bold else color
            if hl:
                c = C["black"]
            r = self._style(p.add_run(tok), size, c, bold=bold or hl)
            if hl:
                _run_shade(r, HEX["seagrass"])
        return p

    def _para(self, before=0, after=0, line=None, exact=False, keep=False):
        p = self.doc.add_paragraph()
        pf = p.paragraph_format
        pf.space_before, pf.space_after = Pt(before), Pt(after)
        if line:
            pf.line_spacing_rule = (WD_LINE_SPACING.EXACTLY if exact
                                    else WD_LINE_SPACING.AT_LEAST)
            pf.line_spacing = Pt(line)
        if keep:
            pf.keep_with_next = True
        return p

    def _gap(self, pt=8):
        """Spacer after a table (Word needs a paragraph between tables)."""
        p = self._para(after=0, line=pt, exact=True)
        r = p.add_run()
        r.font.size = Pt(1)
        return p

    @staticmethod
    def _cell_p(cell, first=True):
        p = cell.paragraphs[0] if first else cell.add_paragraph()
        pf = p.paragraph_format
        pf.space_before = pf.space_after = Pt(0)
        return p

    def _table(self, rows, cols, widths):
        """Fixed-layout, borderless, flush-left table. widths: fractions."""
        t = self.doc.add_table(rows=rows, cols=cols)
        _tbl_fixed(t, self._usable)
        _tbl_borders(t, {})
        _tbl_cell_margins(t)
        ws = [int(self._usable * w) for w in widths]
        for j, col in enumerate(t.columns):
            col.width = ws[j]
        for row in t.rows:
            for j, cell in enumerate(row.cells):
                cell.width = ws[j]
        return t

    # ── title block ──
    def title(self, text):
        """Doc H1 — 26pt bold, tight (design.md §3.3 Title wide)."""
        p = self._para(after=6, line=SZ["title"] * 1.08, exact=True,
                       keep=True)
        p.paragraph_format.right_indent = int(self._usable * 0.18)
        r = self._style(p.add_run(text), SZ["title"], C["black"], bold=True)
        _tracking(r, -0.4)
        self.doc.core_properties.title = text
        return p

    def lede(self, text):
        p = self._para(after=16, line=SZ["lede"] * 1.45)
        p.paragraph_format.right_indent = int(self._usable * 0.1)
        self._rich(p, text, SZ["lede"], C["dust"], bold_color=C["black"])
        return p

    # ── signature: section head ──
    def section(self, idx, eyebrow, heading):
        """§5.2 — Cloud hairline, index line (number black, topic Mist),
        then the assertion headline."""
        p = self._para(before=18, after=5, keep=True)
        _p_border(p, "top", HAIR, HEX["cloud"], space=8)
        self._label(p, f"{idx:02d}", C["black"], bold=True)
        self._label(p, "    " + eyebrow, C["mist"])
        h = self._para(after=8, line=SZ["section"] * 1.2, exact=True,
                       keep=True)
        h.paragraph_format.right_indent = int(self._usable * 0.15)
        r = self._style(h.add_run(heading), SZ["section"], C["black"],
                        bold=True)
        _tracking(r, -0.15)
        return h

    def h3(self, text):
        p = self._para(before=9, after=3, line=SZ["sub"] * 1.25, exact=True,
                       keep=True)
        self._style(p.add_run(text), SZ["sub"], C["black"], bold=True)
        return p

    def body(self, text):
        p = self._para(after=7, line=SZ["body"] * 1.5)
        self._rich(p, text, SZ["body"], C["black"])
        return p

    def bullets(self, items):
        for it in items:
            p = self.doc.add_paragraph(style="List Bullet")
            pf = p.paragraph_format
            pf.space_after = Pt(3)
            pf.line_spacing_rule = WD_LINE_SPACING.AT_LEAST
            pf.line_spacing = Pt(SZ["body"] * 1.45)
            self._rich(p, it, SZ["body"], C["black"])

    # ── metric row ──
    def metric_row(self, metrics):
        """metrics: [{label, value, unit?, note?, key?}] — 3–4 cells.
        Cloud top rule, Rule bottom rule, hairline seams; the key metric
        (``key`` or legacy ``hero``) gets the Seagrass marker."""
        n = len(metrics)
        t = self._table(3, n, [1 / n] * n)
        for i, m in enumerate(metrics):
            left = 0 if i == 0 else 11
            for row in range(3):
                # explicit per-cell edges: survive Google Docs import
                _cell_borders(t.cell(row, i), {
                    "top": (HAIR, HEX["cloud"]) if row == 0 else None,
                    "left": (HAIR, HEX["rule"]) if i else None,
                    "bottom": (HAIR, HEX["rule"]) if row == 2 else None,
                    "right": None})
                _cell_margins(t.cell(row, i), left=left, right=8,
                              top=10 if row == 0 else 0,
                              bottom=11 if row == 2 else 0)
            lp = self._cell_p(t.cell(0, i))
            lp.paragraph_format.space_after = Pt(7)
            self._label(lp, m["label"], C["mist"])
            vp = self._cell_p(t.cell(1, i))
            key = m.get("key") or m.get("hero")
            v = f" {m['value']} " if key else m["value"]
            r = self._style(vp.add_run(v), SZ["metric"], C["black"],
                            bold=True)
            _tracking(r, -0.4)
            if key:
                _run_shade(r, HEX["seagrass"])
            if m.get("unit"):
                self._style(vp.add_run(" " + m["unit"]),
                            SZ["metric"] * 0.45, C["dust"])
            np_ = self._cell_p(t.cell(2, i))
            np_.paragraph_format.space_before = Pt(5)
            self._rich(np_, m.get("note", ""), SZ["small"], C["dust"])
        self._gap(12)
        return t

    # ── callouts ──
    def callout(self, label, text, kind="insight"):
        """Fog panel + bold caps label. kind: insight (Seagrass dot) ·
        note · ask (Real Black panel, Seagrass label — once per document)
        · risk / warn (3pt semantic bar)."""
        t = self._table(1, 1, [1])
        cell = t.cell(0, 0)
        ask = kind == "ask"
        _cell_shade(cell, HEX["black"] if ask else HEX["fog"])
        _cell_margins(cell, top=11, bottom=12, left=15, right=15)
        if kind in ("risk", "warn"):
            _cell_borders(cell, {"left": (24, HEX["neg" if kind == "risk"
                                                   else "warn"])})
        lp = self._cell_p(cell)
        lp.paragraph_format.space_after = Pt(4)
        lp.paragraph_format.keep_with_next = True
        if kind == "insight":
            dot = self._style(lp.add_run("●  "), SZ["label"] + 1,
                              C["seagrass"])
            _tracking(dot, 0)
        label_color = {"ask": C["seagrass"], "risk": C["neg"],
                       "warn": C["warn"]}.get(kind, C["black"])
        self._label(lp, label, label_color, bold=True)
        bp = self._cell_p(cell, first=False)
        bp.paragraph_format.line_spacing_rule = WD_LINE_SPACING.AT_LEAST
        bp.paragraph_format.line_spacing = Pt(SZ["callout"] * 1.45)
        ink = C["horizon"] if ask else C["black"]
        self._rich(bp, text, SZ["callout"], ink)
        self._gap(12)
        return t

    def ask(self, text, label="The ask"):
        """The decision or request — Real Black panel, Seagrass label."""
        return self.callout(label, text, kind="ask")

    # ── table ──
    def table(self, headers, rows, data_cols=(), total=False, key_row=None,
              widths=None):
        """Hairline table: caps Mist header over Cloud, Rule row dividers,
        numbers right-aligned. total → last row gets a Real Black top rule
        and weight; key_row → index of one row with a 3pt Seagrass bar."""
        nc = len(headers)
        t = self._table(1 + len(rows), nc, widths or [1 / nc] * nc)
        last = len(rows) - 1
        for j, htext in enumerate(headers):
            cell = t.cell(0, j)
            _cell_borders(cell, {"bottom": (HAIR, HEX["cloud"])})
            _cell_margins(cell, bottom=5, right=0 if j == nc - 1 else 12)
            p = self._cell_p(cell)
            self._label(p, htext, C["mist"])
            if j in data_cols:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        for i, row in enumerate(rows):
            is_total = total and i == last
            is_key = key_row == i
            for j, val in enumerate(row):
                cell = t.cell(1 + i, j)
                edges = {"bottom": None if is_total else (HAIR, HEX["rule"])}
                if is_total:
                    edges["top"] = (HAIR, HEX["black"])
                if is_key and j == 0:
                    edges["left"] = (24, HEX["seagrass"])
                _cell_borders(cell, edges)
                _cell_margins(cell, top=5, bottom=5,
                              left=9 if (is_key and j == 0) else 0,
                              right=0 if j == nc - 1 else 12)
                p = self._cell_p(cell)
                if j in data_cols:
                    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                if is_total or is_key:
                    self._style(p.add_run(str(val)), 9, C["black"], bold=True)
                else:
                    self._rich(p, str(val), 9, C["black"])
        self._gap(12)
        return t

    # ── quote ──
    def quote(self, text, cite):
        """Reading-display quote: no marks, no rule, ≤ 34ch; cite caps Mist.
        Simulated personas cite as ``Maya · Simulated Gen-Z shopper``."""
        p = self._para(before=8, after=6, line=SZ["quote"] * 1.3, keep=True)
        p.paragraph_format.right_indent = int(self._usable * 0.38)
        r = self._style(p.add_run(text), SZ["quote"], C["black"])
        _tracking(r, -0.1)
        cp = self._para(after=14)
        self._label(cp, "— " + cite, C["mist"])
        return p

    # ── spec list / logistics ──
    def _spec_rows(self, t, pairs, col, label_frac_last=False):
        for i, (k, v) in enumerate(pairs):
            kc, vc = t.cell(i, col), t.cell(i, col + 1)
            for c in (kc, vc):
                edges = {"bottom": (HAIR, HEX["rule"])}
                if i == 0:
                    edges["top"] = (HAIR, HEX["cloud"])
                _cell_borders(c, edges)
                _cell_margins(c, top=5, bottom=5, right=10)
            kp = self._cell_p(kc)
            kp.paragraph_format.space_before = Pt(1)
            self._label(kp, k, C["mist"])
            self._rich(self._cell_p(vc), v, SZ["small"], C["black"])

    def kv(self, pairs, label_width=0.24):
        """Spec list (§6.7): quiet caps labels left, values right, Rule
        hairline under each row, Cloud on top."""
        t = self._table(len(pairs), 2, [label_width, 1 - label_width])
        self._spec_rows(t, pairs, 0)
        self._gap(12)
        return t

    def logistics(self, left, right):
        """Meeting logistics: two spec lists side by side."""
        rows = max(len(left), len(right))
        gap = 0.06
        t = self._table(rows, 5, [0.14, 0.33, gap, 0.14, 0.33])
        pad = lambda ps: list(ps) + [("", "")] * (rows - len(ps))
        self._spec_rows(t, pad(left), 0)
        self._spec_rows(t, pad(right), 3)
        for i in range(rows):
            _cell_borders(t.cell(i, 2), {"top": None, "bottom": None})
        for col, ps in ((0, left), (3, right)):   # no rule under padding
            for i in range(len(ps), rows):
                for c in (t.cell(i, col), t.cell(i, col + 1)):
                    _cell_borders(c, {"bottom": None})
        self._gap(12)
        return t

    # ── minutes set ──
    def agenda(self, items, label="Agenda"):
        """items: str or (text, who/timebox). Indexed hairline rows."""
        lp = self._para(before=10, after=5, keep=True)
        self._label(lp, label, C["black"], bold=True)
        t = self._table(len(items), 3, [0.07, 0.68, 0.25])
        for i, it in enumerate(items):
            text, who = (it, "") if isinstance(it, str) else it
            for j in range(3):
                c = t.cell(i, j)
                edges = {"bottom": (HAIR, HEX["rule"])}
                if i == 0:
                    edges["top"] = (HAIR, HEX["cloud"])
                _cell_borders(c, edges)
                _cell_margins(c, top=5, bottom=5, right=0 if j == 2 else 8)
            ip = self._cell_p(t.cell(i, 0))
            ip.paragraph_format.space_before = Pt(1.5)
            self._label(ip, f"{i + 1:02d}", C["black"], bold=True)
            self._rich(self._cell_p(t.cell(i, 1)), text, 9, C["black"])
            wp = self._cell_p(t.cell(i, 2))
            wp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            wp.paragraph_format.space_before = Pt(1.5)
            self._label(wp, who, C["mist"])
        self._gap(12)
        return t

    def decisions(self, items):
        """Referenceable D-ids on hairline rows."""
        t = self._table(len(items), 2, [0.07, 0.93])
        for i, item in enumerate(items):
            for j in range(2):
                c = t.cell(i, j)
                edges = {"bottom": (HAIR, HEX["rule"])}
                if i == 0:
                    edges["top"] = (HAIR, HEX["cloud"])
                _cell_borders(c, edges)
                _cell_margins(c, top=5, bottom=5, right=8)
            ip = self._cell_p(t.cell(i, 0))
            r = self._style(ip.add_run(f"D{i + 1}"), 8, C["black"], bold=True)
            _tracking(r, 0.3)
            self._rich(self._cell_p(t.cell(i, 1)), item, SZ["body"],
                       C["black"])
        self._gap(12)
        return t

    def actions(self, rows):
        """[{action, owner, due, status}] → A-id table. status: open |
        done | blocked → Fog tag with Dust / Pos / Neg ink (never Seagrass)."""
        ink = {"open": C["dust"], "done": C["pos"], "blocked": C["neg"]}
        widths = [0.07, 0.49, 0.17, 0.13, 0.14]
        t = self._table(1 + len(rows), 5, widths)
        for j, h in enumerate(["#", "Action", "Owner", "Due", "Status"]):
            c = t.cell(0, j)
            _cell_borders(c, {"bottom": (HAIR, HEX["cloud"])})
            _cell_margins(c, bottom=5, right=0 if j == 4 else 10)
            self._label(self._cell_p(c), h, C["mist"])
        for i, row in enumerate(rows, 1):
            cells = t.rows[i].cells
            for j, c in enumerate(cells):
                _cell_borders(c, {"bottom": (HAIR, HEX["rule"])})
                _cell_margins(c, top=5, bottom=5, right=0 if j == 4 else 10)
            r = self._style(self._cell_p(cells[0]).add_run(f"A{i}"), 8,
                            C["black"], bold=True)
            _tracking(r, 0.3)
            self._rich(self._cell_p(cells[1]), row["action"], 9, C["black"])
            self._style(self._cell_p(cells[2]).add_run(row["owner"]), 9,
                        C["dust"])
            self._style(self._cell_p(cells[3]).add_run(row.get("due", "TBD")),
                        9, C["dust"])
            st = row.get("status", "open").lower()
            tag = self._label(self._cell_p(cells[4]), f" {st} ",
                              ink.get(st, C["dust"]), size=6.5, track=0.3)
            _run_shade(tag, HEX["fog"])
        self._gap(12)
        return t

    def smallprint(self, text):
        """Next meeting / status / distribution — 7pt Mist, bold in Dust."""
        p = self._para(before=10, after=0, line=7 * 1.5)
        self._rich(p, text, 7, C["mist"], bold_color=C["dust"])
        return p

    # ── figure ──
    def figure(self, image_path, caption, source="", idx=None,
               width_frac=1.0):
        """Chart/figure image (rendered per design.md §7) + figcap:
        bold ``Fig 01``, one-sentence caption, source right in Mist."""
        p = self._para(before=6, after=6, keep=True)
        p.add_run().add_picture(str(image_path),
                                width=int(self._usable * width_frac))
        idx = idx if idx is not None else getattr(self, "_fig", 0) + 1
        self._fig = idx
        cp = self._para(after=12)
        self._tabbed(cp, [(self._usable, WD_TAB_ALIGNMENT.RIGHT)])
        self._style(cp.add_run(f"Fig {idx:02d}   "), SZ["small"],
                        C["black"], bold=True)
        self._style(cp.add_run(caption), SZ["small"], C["dust"])
        if source:
            self._style(cp.add_run(f"\tSource: {source}"), SZ["small"] - 0.5,
                        C["mist"])
        return p

    # ── signature: chapter opener (long docs only) ──
    def chapter(self, num, title):
        """§5.5 — a page of its own: Fog ground, giant numeral + one-word
        title bottom-left, nothing but the folio. Word can't colour a
        single page, so the Fog ground fills the text block."""
        sec = self.doc.add_section(WD_SECTION.NEW_PAGE)
        sec.header.is_linked_to_previous = False      # no page head
        hp = sec.header.paragraphs[0]
        for r in list(hp.runs):
            r._r.getparent().remove(r._r)
        t = self._table(1, 1, [1])
        cell = t.cell(0, 0)
        _cell_shade(cell, HEX["fog"])
        _cell_margins(cell, left=24, right=24, bottom=26)
        t.rows[0].height = int(self._usable_h - Pt(30))
        t.rows[0].height_rule = WD_ROW_HEIGHT_RULE.EXACTLY
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.BOTTOM
        for k, text in enumerate((f"{num:02d}" if isinstance(num, int)
                                  else str(num), title)):
            p = self._cell_p(cell, first=k == 0)
            p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
            p.paragraph_format.line_spacing = Pt(70)
            r = self._style(p.add_run(text), 72, C["black"])
            _tracking(r, -2)
        # section break paragraph: shrink it so it can't spill a blank page
        nxt = self.doc.add_section(WD_SECTION.NEW_PAGE)
        body = self.doc.element.body
        for p in body.iterchildren(qn("w:p")):
            pPr = p.find(qn("w:pPr"))
            if pPr is not None and pPr.find(qn("w:sectPr")) is not None:
                self._shrink(p)
        self._page_head(nxt.header)
        return t

    @staticmethod
    def _shrink(p):
        pPr = p.find(qn("w:pPr"))
        sp = _set_child(pPr, "w:spacing", "w:pPr")
        sp.set(qn("w:before"), "0")
        sp.set(qn("w:after"), "0")
        sp.set(qn("w:line"), "20")
        sp.set(qn("w:lineRule"), "exact")
        rpr = _set_child(pPr, "w:rPr", "w:pPr")
        sz = OxmlElement("w:sz")
        sz.set(qn("w:val"), "2")
        rpr.append(sz)

    def page_break(self):
        self.doc.add_page_break()

    def save(self, path):
        self.doc.save(str(path))
        return str(path)


# ── demo / visual regression check ──────────────────────────────────
def _demo_chart(path):
    """A §7-conformant bar chart PNG for the figure demo (Pillow)."""
    from PIL import Image, ImageDraw, ImageFont
    W_, H_ = 1800, 620
    im = Image.new("RGB", (W_, H_), "#" + HEX["horizon"])
    d = ImageDraw.Draw(im)
    font = None
    for f in ("/System/Library/Fonts/Supplemental/Arial.ttf",
              "/System/Library/Fonts/Helvetica.ttc",
              "/Library/Fonts/Arial.ttf"):
        try:
            font = ImageFont.truetype(f, 30)
            bold = ImageFont.truetype(f, 32)
            break
        except OSError:
            continue
    font = font or ImageFont.load_default()
    bold = bold if font else font
    base, top, left = 520, 60, 60
    for k in range(5):                       # gridlines, horizontal only
        y = base - k * (base - top) / 4
        d.line([(left, y), (W_ - 40, y)], fill="#" + HEX["rule"], width=2)
    d.line([(left, base), (W_ - 40, base)], fill="#" + HEX["cloud"], width=2)
    data = [("Field study", 2), ("Online panel", 4), ("Agency recall", 3),
            ("Socialtrait", 24)]
    bw, step = 190, (W_ - left - 80) / len(data)
    for i, (lab, v) in enumerate(data):
        x = left + 40 + i * step + (step - bw) / 2
        h = (base - top) * v / 24
        col = "#" + (HEX["day"] if lab == "Socialtrait" else HEX["cloud"])
        d.rounded_rectangle([x, base - max(h, 6), x + bw, base], radius=6,
                            fill=col)
        d.text((x + bw / 2, base - max(h, 6) - 14), f"{v:g}", font=bold,
               fill="#" + HEX["black"], anchor="mb")
        d.text((x + bw / 2, base + 22), lab, font=font,
               fill="#" + HEX["mist"], anchor="mt")
    im.save(path)
    return path


def demo(out):
    out = Path(out)
    d = OriDoc(doc_type="Statement of work", doc_id="ST-SOW-007",
               date="2026-10-07", classification="Client confidential",
               meta=("Arlo Foods",), artifact="long-doc")
    d.title("Audience simulation pilot — statement of work")
    d.lede("Scope, timeline, and commercial terms for the Q4 simulated-"
           "audience pilot between Socialtrait and Arlo Foods.")
    d.metric_row([
        {"label": "Studies", "value": "8", "note": "across two campaigns"},
        {"label": "Duration", "value": "10", "unit": "wks",
         "note": "kickoff to readout", "key": True},
        {"label": "Fee", "value": "$44", "unit": "k", "note": "fixed, net-30"},
        {"label": "Panel size", "value": "2,400", "note": "per study"},
    ])
    d.callout("Insight", "Simulated panels answer <b>before</b> the media "
              "decision, not three weeks after it — that is the whole "
              "commercial case for this pilot.")
    d.section(1, "Scope", "Eight simulated studies across two campaigns")
    d.body("Socialtrait will run <b>eight simulated-audience studies</b> "
           "across the client's two Q4 campaigns, covering four audience "
           "cells per study with calibrated persona models. Each study "
           "reports preference share with confidence intervals and "
           "verbatim-style persona reactions.")
    d.bullets(["Creative pre-tests for six variants per campaign",
               "Segment-level preference ranking with confidence intervals",
               "Verbatim-style persona reactions for creative iteration"])
    d.h3("Out of scope")
    d.body("Media buying, creative production, and live-panel fieldwork. "
           "Any of these can be added by change order.")
    d.section(2, "Timeline", "Kickoff to final readout in ten weeks")
    d.table(["Phase", "Deliverable", "Weeks", "Fee"],
            [["Onboard", "Data intake, persona calibration", "1–2", "$8k"],
             ["Studies", "8 studies, rolling readouts", "3–8", "$30k"],
             ["Validation", "Holdout comparison, final report", "9–10",
              "$6k"],
             ["Total", "", "10", "$44k"]],
            data_cols=(2, 3), total=True, key_row=1,
            widths=[0.2, 0.5, 0.14, 0.16])
    chart = _demo_chart(out.with_name(out.stem + "-fig01.png"))
    d.figure(chart, "Creative variants tested per campaign, by method.",
             source="Socialtrait pilots, 2026")
    d.quote("The simulation caught in four hours what our panel would have "
            "told us three weeks after launch.",
            "Dana · VP Growth, CPG pilot")
    d.kv([("Client", "Arlo Foods, Inc."),
          ("Term", "2026-10-14 → 2026-12-19"),
          ("Payment", "Fixed fee, net-30 from each invoice"),
          ("Contacts", "suraj@socialtrait.ai · ops@arlofoods.com")])
    d.callout("Risk", "Persona calibration needs the Q3 brand-tracker export "
              "by <b>October 14</b>; a late export shifts every study by "
              "the same amount.", kind="risk")
    d.callout("Watch", "Holiday media freeze from Dec 20 — final readout "
              "must land before it.", kind="warn")
    d.chapter(2, "Minutes")
    d.section(3, "Kickoff minutes", "Calibration starts Monday; two "
              "decisions, four actions")
    d.logistics([("Date", "2026-10-07, 10:00–10:45"),
                 ("Where", "Google Meet"),
                 ("Chair", "Suraj N.")],
                [("Present", "Suraj N., Dana R., Priya K., Leo M."),
                 ("Absent", "Ana T."),
                 ("Notes", "Leo M.")])
    d.agenda([("Pilot scope and success criteria", "Suraj · 15 min"),
              ("Data intake and calibration plan", "Priya · 15 min"),
              ("Readout cadence", "Dana · 10 min")])
    d.h3("Decisions")
    d.decisions(["Success = interval coverage ≥ <hl>80%</hl> on holdout "
                 "cells.",
                 "Readouts every second Thursday, 30 minutes, async-first."])
    d.h3("Actions")
    d.actions([
        {"action": "Export Q3 brand-tracker data", "owner": "Dana R.",
         "due": "Oct 14", "status": "open"},
        {"action": "Calibrate four persona cells", "owner": "Priya K.",
         "due": "Oct 21", "status": "open"},
        {"action": "Share readout template", "owner": "Suraj N.",
         "due": "Oct 9", "status": "done"},
        {"action": "Legal review of data-sharing addendum",
         "owner": "Ana T.", "due": "Oct 10", "status": "blocked"},
    ])
    d.ask("Countersign by <b>October 10</b> so persona calibration "
          "completes before the November media flight.")
    d.smallprint("<b>Next meeting:</b> 2026-10-21, 10:00. <b>Status:</b> "
                 "final. <b>Distribution:</b> pilot team, Arlo Foods "
                 "marketing.")
    return d.save(out)


def demo_resume(out):
    r = OriDoc(doc_type="Resume", artifact="resume",
               candidate="Maya Chen", classification="")
    r.title("Maya Chen")
    r.lede("Research engineer — audience simulation, causal inference, "
           "evaluation.")
    r.section(1, "Experience", "Socialtrait · Research engineer, 2024–")
    r.bullets(["Built the persona calibration pipeline used in every pilot",
               "Cut study turnaround from 19 days to <b>4 hours</b>"])
    return r.save(out)


if __name__ == "__main__":
    # demos never land in the repo: default to the system temp dir
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else (
        Path(tempfile.gettempdir()) / "ori-docx-demo.docx")
    print("wrote", demo(target))
    print("wrote", demo_resume(target.with_name(target.stem + "-resume.docx")))
