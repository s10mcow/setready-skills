#!/usr/bin/env python3
"""Render a SetReady skill report as a PDF.

    python3 report.py report.json report.pdf

Needs reportlab (pip install reportlab). The skill's references/report.md says what goes in
report.json. The shape:

    {
      "title": "Land deal summary",
      "subtitle": "Address or parcel, county, state",
      "meta": [["Date", "2026-11-18"], ["Goal", "Sell the land and home together"]],
      "sections": [
        {"kind": "flags", "title": "Red flags", "tone": "red", "tile": true,
         "empty": "None found in this conversation.",
         "items": [{"title": "...", "detail": "...", "status": "Red flag",
                    "evidence": "...", "who": "..."}]},
        {"kind": "table", "title": "Open questions", "tone": "amber", "tile": true,
         "columns": ["Question", "Who answers it", "Why it matters"], "widths": [45, 25, 30],
         "rows": [["...", "...", "..."]]},
        {"kind": "table", "title": "Budget", "columns": ["Line", "Amount", "Source", "Who quotes it"],
         "align": ["left", "right", "left", "left"], "rows": [...], "total": ["Total", "$1", "", ""]},
        {"kind": "table", "title": "What was looked up", "status_column": 1, ...},
        {"kind": "list", "title": "Settled", "tone": "green", "tile": true, "items": ["..."]},
        {"kind": "text", "title": "Next step", "callout": true, "paragraphs": ["..."]}
      ],
      "footer": "Not a survey ... advice.",
      "closing": ["Made with ...", "a link"]
    }

Text may use **bold**, [label](link) and bare links. Keep every fact and its status exactly
as the user confirmed it; this script only lays it out.
"""

import json
import re
import sys
from xml.sax.saxutils import escape

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.pdfbase.pdfmetrics import stringWidth
    from reportlab.pdfgen import canvas as pdfcanvas
    from reportlab.platypus import (
        BaseDocTemplate,
        CondPageBreak,
        Flowable,
        Frame,
        KeepTogether,
        PageTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle,
    )
except ImportError:
    sys.exit("reportlab is missing. Install it with: pip install reportlab")

INK = colors.HexColor("#171717")
BODY = colors.HexColor("#4d4d4d")
MUTE = colors.HexColor("#888888")
HAIR = colors.HexColor("#ebebeb")
HAIR_STRONG = colors.HexColor("#a1a1a1")
SOFT = colors.HexColor("#fafafa")
LINK = "#0070f3"

# Each tone: the strong colour for text and bars, and a pale tint for backgrounds.
TONES = {
    "red": (colors.HexColor("#c62828"), colors.HexColor("#fdf3f3")),
    "amber": (colors.HexColor("#b45309"), colors.HexColor("#fff8ec")),
    "green": (colors.HexColor("#15803d"), colors.HexColor("#f1f9f3")),
    "neutral": (INK, SOFT),
}

PAGE_W, PAGE_H = letter
MARGIN_X = 0.75 * inch
CONTENT_W = PAGE_W - 2 * MARGIN_X


def style(name, font="Helvetica", size=9.5, leading=None, color=BODY, **extra):
    return ParagraphStyle(name, fontName=font, fontSize=size, leading=leading or size * 1.38, textColor=color, **extra)


S = {
    "title": style("title", "Helvetica-Bold", 23, 27, INK, spaceAfter=4),
    "subtitle": style("subtitle", size=11, leading=15, color=BODY),
    "h2": style("h2", "Helvetica-Bold", 12.5, 16, INK, spaceBefore=16, spaceAfter=7),
    "body": style("body"),
    "cell": style("cell", size=8.8, leading=12),
    "cell_bold": style("cell_bold", "Helvetica-Bold", 8.8, 12, INK),
    "head": style("head", "Helvetica-Bold", 7, 9, MUTE),
    "label": style("label", "Helvetica-Bold", 6.8, 9, MUTE),
    "meta_value": style("meta_value", "Helvetica-Bold", 9.5, 12.5, INK),
    "flag_title": style("flag_title", "Helvetica-Bold", 10, 13.5, INK),
    "flag_detail": style("flag_detail", size=9, leading=12.8),
    "small": style("small", size=8.3, leading=11.5),
    "tile_number": style("tile_number", "Helvetica-Bold", 22, 24, INK),
    "tile_label": style("tile_label", "Helvetica-Bold", 7.5, 10, MUTE),
    "closing": style("closing", size=8.5, leading=12, color=MUTE),
}

# Standard PDF fonts only cover Windows-1252, so swap the few symbols agents like to use.
SWAPS = {"→": "->", "←": "<-", "≤": "<=", "≥": ">=", "✓": "", "✔": "", "≈": "~"}
LINK_RE = re.compile(r"\[([^\]]+)\]\(((?:https?)://[^)\s]+)\)|((?:https?)://[^\s<]*[^\s<.,;:)\]])")


def clean(value):
    text = str(value if value is not None else "")
    for old, new in SWAPS.items():
        text = text.replace(old, new)
    return text.encode("cp1252", "replace").decode("cp1252")


def inline(text):
    """Escape plain text and turn **bold** into markup."""
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escape(text))


def rich(value):
    text = clean(value)
    out, pos = [], 0
    for match in LINK_RE.finditer(text):
        out.append(inline(text[pos:match.start()]))
        label, url, bare = match.groups()
        href = url or bare
        out.append('<a href="%s" color="%s">%s</a>' % (escape(href, {'"': "&quot;"}), LINK, escape(label or bare)))
        pos = match.end()
    out.append(inline(text[pos:]))
    return "".join(out)


def para(value, st):
    return Paragraph(rich(value), st)


def tone_of(name):
    return TONES.get(name or "neutral", TONES["neutral"])


STATUS_WORDS = [("red flag", "red"), ("unverified", "amber"), ("verified", "green"), ("settled", "green"), ("open", "amber")]


def status_para(text, st):
    """Colour the status word (Verified, Unverified, Red flag, Settled, Open) and leave the rest plain."""
    text = clean(text).strip()
    for word, tone in STATUS_WORDS:
        if text.lower().startswith(word):
            strong = tone_of(tone)[0].hexval()[2:]
            head, rest = text[:len(word)], text[len(word):]
            return Paragraph('<font color="#%s"><b>%s</b></font>%s' % (strong, escape(head), rich(rest)), st)
    return para(text, st)


def heading(section, count=None, keep=0):
    """A section heading that moves to the next page unless `keep` points of what follows fit under it."""
    text = rich(section.get("title", ""))
    if count is not None:
        text += '  <font color="#888888" size="10">%d</font>' % count
    return [CondPageBreak(keep + 40), Paragraph(text, S["h2"])]


def lead_height(flowable, rows=2):
    """Height of a flowable's first rows, so its heading never ends a page alone."""
    _, height = flowable.wrap(CONTENT_W, PAGE_H)
    row_heights = getattr(flowable, "_rowHeights", None)
    return sum(row_heights[:rows]) if row_heights else height


def meta_block(pairs):
    if not pairs:
        return []
    per_row = 3
    cells, rows = [], []
    for label, value in pairs:
        cells.append([para(str(label).upper(), S["label"]), para(value, S["meta_value"])])
    for i in range(0, len(cells), per_row):
        row = cells[i:i + per_row]
        rows.append(row + [""] * (per_row - len(row)))
    table = Table(rows, colWidths=[CONTENT_W / per_row] * per_row)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SOFT),
        ("BOX", (0, 0), (-1, -1), 0.6, HAIR),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return [Spacer(1, 10), table]


def section_count(section):
    kind = section.get("kind")
    if kind in ("flags", "list"):
        return len(section.get("items") or [])
    if kind == "table":
        return len(section.get("rows") or [])
    return None


def tiles(sections):
    chosen = [s for s in sections if s.get("tile") and section_count(s) is not None]
    if not chosen:
        return []
    gap = 8
    width = (CONTENT_W - gap * (len(chosen) - 1)) / len(chosen)
    cells, widths, commands = [], [], []
    for index, section in enumerate(chosen):
        strong, tint = tone_of(section.get("tone"))
        number = Paragraph('<font color="#%s">%d</font>' % (strong.hexval()[2:], section_count(section)), S["tile_number"])
        cells.append([number, para(section.get("title", "").upper(), S["tile_label"])])
        widths.append(width)
        col = len(cells) - 1
        commands += [("BACKGROUND", (col, 0), (col, 0), tint), ("LINEBEFORE", (col, 0), (col, 0), 3, strong)]
        if index < len(chosen) - 1:
            cells.append("")
            widths.append(gap)
    table = Table([cells], colWidths=widths)
    table.setStyle(TableStyle(commands + [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 11),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    return [Spacer(1, 10), table]


def flags_block(section):
    items = section.get("items") or []
    strong, tint = tone_of(section.get("tone") or "red")
    if not items:
        return heading(section, 0) + [para(section.get("empty", "None."), S["body"])]
    out, cards = [], []
    inner_w = CONTENT_W - 26
    for item in items:
        status = clean(item.get("status") or "").strip()
        if status.lower().startswith("red flag"):
            status = status[len("red flag"):].strip(" ()-:;,")
            status = status[:1].upper() + status[1:]
        top = Table(
            [[para(item.get("title", ""), S["flag_title"]), status_para(status, style("st", "Helvetica-Bold", 7.5, 10, MUTE, alignment=2))]],
            colWidths=[inner_w * 0.74, inner_w * 0.26],
        )
        top.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
        parts = [top]
        if item.get("detail"):
            parts += [Spacer(1, 3), para(item["detail"], S["flag_detail"])]
        facts = []
        if item.get("evidence"):
            facts.append([para("EVIDENCE", S["label"]), para(item["evidence"], S["small"])])
        if item.get("who"):
            facts.append([para("WHO CAN CONFIRM OR CLEAR IT", S["label"]), para(item["who"], style("who", "Helvetica-Bold", 8.3, 11.5, INK))])
        if facts:
            row = Table([[f for f in facts]], colWidths=[inner_w * 0.6, inner_w * 0.4][:len(facts)] if len(facts) == 2 else [inner_w])
            row.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 8), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            parts += [Spacer(1, 6), row]
        card = Table([[parts]], colWidths=[CONTENT_W])
        card.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), tint),
            ("LINEBEFORE", (0, 0), (0, -1), 3, strong),
            ("LEFTPADDING", (0, 0), (-1, -1), 13),
            ("RIGHTPADDING", (0, 0), (-1, -1), 13),
            ("TOPPADDING", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ]))
        cards.append(card)
        out += [card, Spacer(1, 6)]
    return heading(section, len(items), lead_height(cards[0])) + out


def table_block(section):
    columns = section.get("columns") or []
    rows = section.get("rows") or []
    count = len(rows) if section.get("count", True) else None
    if not rows:
        return heading(section, count) + [para(section.get("empty", "None."), S["body"])]
    n = len(columns)
    weights = section.get("widths") or [1] * n
    total_weight = float(sum(weights))
    widths = [CONTENT_W * w / total_weight for w in weights]
    align = section.get("align") or ["left"] * n
    status_cols = section.get("status_column")
    status_cols = set(status_cols if isinstance(status_cols, list) else [status_cols] if status_cols is not None else [])

    def cell(value, col, st):
        if align[col] == "right":
            st = ParagraphStyle(st.name + "r", parent=st, alignment=2)
        if col in status_cols:
            return status_para(value, st)
        return para(value, st)

    data = [[para(str(c).upper(), ParagraphStyle("h", parent=S["head"], alignment=2 if align[i] == "right" else 0)) for i, c in enumerate(columns)]]
    for row in rows:
        row = list(row) + [""] * (n - len(row))
        data.append([cell(v, i, S["cell"]) for i, v in enumerate(row[:n])])
    total = section.get("total")
    if total:
        total = list(total) + [""] * (n - len(total))
        data.append([cell(v, i, S["cell_bold"]) for i, v in enumerate(total[:n])])
    table = Table(data, colWidths=widths, repeatRows=1)
    commands = [
        ("BACKGROUND", (0, 0), (-1, 0), SOFT),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, HAIR_STRONG),
        ("LINEBELOW", (0, 1), (-1, -1), 0.5, HAIR),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    if len(data) > 2:
        commands.append(("NOSPLIT", (0, 0), (-1, 1)))
    if total:
        commands += [("LINEABOVE", (0, -1), (-1, -1), 0.9, INK), ("LINEBELOW", (0, -1), (-1, -1), 0, colors.white)]
        commands.append(("NOSPLIT", (0, -3 if len(data) > 3 else 0), (-1, -1)))
    table.setStyle(TableStyle(commands))
    return heading(section, count, lead_height(table)) + [table]


class Check(Flowable):
    """A tick drawn as lines, so it shows in every PDF viewer."""

    def __init__(self, color, line_height):
        super().__init__()
        self.color = color
        self.width = 12
        self.height = line_height

    def draw(self):
        base = self.height - 9.5
        c = self.canv
        c.setStrokeColor(self.color)
        c.setLineWidth(1.5)
        c.setLineCap(1)
        c.setLineJoin(1)
        path = c.beginPath()
        path.moveTo(0.6, base + 3.4)
        path.lineTo(3.0, base + 0.6)
        path.lineTo(7.8, base + 6.8)
        c.drawPath(path, stroke=1, fill=0)


def list_block(section):
    items = section.get("items") or []
    if not items:
        return heading(section, 0) + [para(section.get("empty", "None."), S["body"])]
    strong = tone_of(section.get("tone") or "green")[0]
    data = [[Check(strong, S["body"].leading), para(item, S["body"])] for item in items]
    table = Table(data, colWidths=[16, CONTENT_W - 16])
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, HAIR),
    ]))
    return heading(section, len(items), lead_height(table)) + [table]


def text_block(section):
    paragraphs = [para(p, S["body"]) for p in section.get("paragraphs") or []]
    if not section.get("callout"):
        out = heading(section, keep=lead_height(paragraphs[0]) if paragraphs else 0)
        for p in paragraphs:
            out += [p, Spacer(1, 5)]
        return out
    parts = []
    for p in paragraphs:
        parts += [p, Spacer(1, 5)]
    box = Table([[parts[:-1]]], colWidths=[CONTENT_W])
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SOFT),
        ("BOX", (0, 0), (-1, -1), 0.6, HAIR),
        ("LINEBEFORE", (0, 0), (0, -1), 3, INK),
        ("LEFTPADDING", (0, 0), (-1, -1), 13),
        ("RIGHTPADDING", (0, 0), (-1, -1), 13),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    return heading(section, keep=lead_height(box)) + [box]


BLOCKS = {"flags": flags_block, "table": table_block, "list": list_block, "text": text_block}


def make_canvas(title, footer):
    class ReportCanvas(pdfcanvas.Canvas):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._pages = []

        def showPage(self):
            self._pages.append(dict(self.__dict__))
            self._startPage()

        def save(self):
            total = len(self._pages)
            for state in self._pages:
                self.__dict__.update(state)
                self._chrome(total)
                super().showPage()
            super().save()

        def _chrome(self, total):
            top = PAGE_H - 0.5 * inch
            self.setFillColor(INK)
            self.setFont("Helvetica-Bold", 8.5)
            self.drawString(MARGIN_X, top, "SETREADY", charSpace=1.4)
            self.setFillColor(MUTE)
            self.setFont("Helvetica", 7.8)
            room = CONTENT_W - 90
            text = clean(title) if self._pageNumber > 1 else "setready.us"
            while text and stringWidth(text, "Helvetica", 7.8) > room:
                text = text[:-2].rstrip() + "\u2026"
            self.drawRightString(PAGE_W - MARGIN_X, top, text)
            self.setStrokeColor(HAIR)
            self.setLineWidth(0.6)
            self.line(MARGIN_X, top - 7, PAGE_W - MARGIN_X, top - 7)
            bottom = 0.5 * inch
            self.line(MARGIN_X, bottom + 11, PAGE_W - MARGIN_X, bottom + 11)
            self.setFont("Helvetica", 7.3)
            self.drawString(MARGIN_X, bottom, clean(footer))
            self.drawRightString(PAGE_W - MARGIN_X, bottom, "Page %d of %d" % (self._pageNumber, total))

    return ReportCanvas


def build(data, out_path):
    for key in ("title", "sections"):
        if key not in data:
            sys.exit('report.json needs "%s"' % key)
    sections = data["sections"]
    for section in sections:
        if section.get("kind") not in BLOCKS:
            sys.exit('Unknown section kind "%s"; use flags, table, list or text' % section.get("kind"))

    story = [para(data["title"], S["title"])]
    if data.get("subtitle"):
        story.append(para(data["subtitle"], S["subtitle"]))
    story += meta_block(data.get("meta") or [])
    story += tiles(sections)
    blocks = [BLOCKS[section["kind"]](section) for section in sections]
    for block in blocks[:-1]:
        story += block
    last = blocks[-1] if blocks else []
    closing = data.get("closing") or []
    if closing:
        # The closing travels with the last section, heading and all, so neither sits alone on a page.
        rule = Table([[""]], colWidths=[CONTENT_W], rowHeights=[1], style=[("LINEABOVE", (0, 0), (-1, -1), 0.6, HAIR)])
        body = [f for f in last if not isinstance(f, CondPageBreak)]
        story.append(KeepTogether(body + [Spacer(1, 18), rule, Spacer(1, 6)] + [para(line, S["closing"]) for line in closing]))
    else:
        story += last

    running = data["title"] + (" \u00b7 " + data["subtitle"] if data.get("subtitle") else "")
    doc = BaseDocTemplate(
        out_path,
        pagesize=letter,
        leftMargin=MARGIN_X,
        rightMargin=MARGIN_X,
        topMargin=0.85 * inch,
        bottomMargin=0.85 * inch,
        title=clean(data["title"]),
        author="SetReady agent skill",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="body", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="page", frames=[frame])])
    doc.build(story, canvasmaker=make_canvas(running, data.get("footer", "")))


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python3 report.py report.json report.pdf")
    with open(sys.argv[1], encoding="utf-8") as handle:
        data = json.load(handle)
    build(data, sys.argv[2])
    print("Wrote " + sys.argv[2])


if __name__ == "__main__":
    main()
