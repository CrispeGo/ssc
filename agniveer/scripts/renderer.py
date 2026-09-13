# -*- coding: utf-8 -*-
"""Two-column B/W print renderer for the Physics Master Book (single-pass)."""
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
    Spacer, HRFlowable, Table, TableStyle, KeepTogether, Flowable)

FONT = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DVS", FONT + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVS-B", FONT + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVS-M", FONT + "DejaVuSansMono.ttf"))
pdfmetrics.registerFont(TTFont("DVS-MB", FONT + "DejaVuSansMono-Bold.ttf"))

BLACK = colors.black
PAGE_W, PAGE_H = A4
ML = MR = 12.5 * mm
MT = 14 * mm
MB = 12.5 * mm
COL_GAP = 5 * mm

def S(name, **kw):
    base = dict(fontName="DVS", fontSize=8.6, leading=11.2, textColor=BLACK,
                spaceBefore=0, spaceAfter=1.4, alignment=0)
    base.update(kw)
    return ParagraphStyle(name, **base)

ST = {
 "body":   S("body"),
 "bullet": S("bullet", leftIndent=9, bulletIndent=2, bulletFontName="DVS", bulletFontSize=8.6),
 "h1":     S("h1", fontName="DVS-B", fontSize=12.5, leading=14.5, spaceBefore=7, spaceAfter=2),
 "h2":     S("h2", fontName="DVS-B", fontSize=9.4, leading=11.4, spaceBefore=4.5, spaceAfter=1.4),
 "trap":   S("trap", spaceBefore=1.8),
 "corr":   S("corr", leftIndent=12, spaceBefore=0, spaceAfter=1.6),
 "formula":S("formula", fontName="DVS-M", fontSize=8.3, leading=10.6, leftIndent=9, spaceBefore=0.4, spaceAfter=0.4),
 "boxbody":S("boxbody", fontSize=8.3, leading=10.6),
 "boxbullet":S("boxbullet", fontSize=8.3, leading=10.6, leftIndent=8, bulletIndent=1, bulletFontName="DVS", bulletFontSize=8.3),
 "exq":    S("exq", fontName="DVS-B", fontSize=8.6, leading=11, spaceBefore=3, spaceAfter=0.8),
 "exw":    S("exw", leftIndent=10, spaceAfter=0.6),
 "exb":    S("exb", leftIndent=10, spaceAfter=0.6),
 "exm":    S("exm", leftIndent=10, spaceAfter=0.6),
 "exk":    S("exk", leftIndent=10, spaceAfter=3.2),
 "ext":    S("ext", leftIndent=10, spaceAfter=0.4),
 "exc":    S("exc", leftIndent=16, spaceAfter=1.2),
 "tbl":    S("tbl", fontSize=7.6, leading=9.4),
 "tblb":   S("tblb", fontName="DVS-B", fontSize=7.6, leading=9.4),
}

CHAP_STARTS = []   # (page, name) for every chapter title, in order
FIRST_FL = {}      # page -> first flowable drawn on that page

def inline(t):
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)

class ChapterTitle(Flowable):
    def __init__(self, text, name):
        super().__init__()
        self.text = text; self.name = name
        self.width = 0; self.height = 24
        self._lines = [text]
    def wrap(self, aw, ah):
        self.width = aw
        from reportlab.pdfbase.pdfmetrics import stringWidth
        words = self.text.split()
        lines = []; cur = ""
        for w in words:
            t = (cur + " " + w).strip()
            if stringWidth(t, "DVS-B", 12.5) <= aw:
                cur = t
            else:
                if cur: lines.append(cur)
                cur = w
        if cur: lines.append(cur)
        self._lines = lines
        self.height = len(lines) * 13 + 13
        return aw, self.height
    def draw(self):
        c = self.canv
        w = self.width
        c.setLineWidth(0.8); c.setStrokeColor(BLACK); c.setFillColor(BLACK)
        c.line(0, 2, w, 2)
        c.setFont("DVS-B", 12.5)
        y = self.height - 12
        for ln in self._lines:
            c.drawString(0, y, ln)
            y -= 13

class RuleBox(Flowable):
    def __init__(self, flowables, pad=4):
        super().__init__()
        self.flowables = flowables; self.pad = pad
    def wrap(self, aw, ah):
        self.width = aw
        inner = aw - 2 * self.pad
        h = 0
        for f in self.flowables:
            fw, fh = f.wrap(inner, ah)
            h += fh
        self.height = h + 2 * self.pad
        return self.width, self.height
    def draw(self):
        c = self.canv
        c.saveState()
        c.setLineWidth(0.6); c.setStrokeColor(BLACK)
        c.rect(0, 0, self.width, self.height, stroke=1, fill=0)
        y = self.height - self.pad
        for f in self.flowables:
            fw, fh = f.wrap(self.width - 2 * self.pad, self.height)
            f.drawOn(c, self.pad, y - fh)
            y -= fh
        c.restoreState()

def parse(text):
    out = []
    boxbuf = None
    exbuf = None
    ex_sol_started = [False]
    tbl = None
    def flush_ex():
        nonlocal exbuf
        if exbuf is not None:
            out.append(KeepTogether(exbuf)); exbuf = None
    def flush_box():
        nonlocal boxbuf
        if boxbuf is not None:
            out.append(KeepTogether([RuleBox(boxbuf)])); boxbuf = None
    def flush_tbl():
        nonlocal tbl
        if tbl is not None:
            data = [[Paragraph(inline(c), ST["tblb"] if i == 0 else ST["tbl"]) for c in r] for i, r in enumerate(tbl)]
            t = Table(data, hAlign="LEFT")
            t.setStyle(TableStyle([
                ("GRID", (0,0), (-1,-1), 0.4, BLACK),
                ("VALIGN", (0,0), (-1,-1), "TOP"),
                ("LEFTPADDING", (0,0), (-1,-1), 3),
                ("RIGHTPADDING", (0,0), (-1,-1), 3),
                ("TOPPADDING", (0,0), (-1,-1), 1.5),
                ("BOTTOMPADDING", (0,0), (-1,-1), 1.5),
            ]))
            out.append(KeepTogether([Spacer(1,2), t, Spacer(1,2)]))
            tbl = None
    for raw in text.split("\n"):
        line = raw.rstrip()
        if line.startswith("#") and "|" in line:
            flush_ex(); flush_box(); flush_tbl()
            numpart, title = line.split("|", 1)
            num = int(numpart.lstrip("#").strip())
            out.append(ChapterTitle("CHAPTER %02d — %s" % (num, title.strip()), "CHAPTER %02d" % num))
            continue
        if line == "---":
            flush_ex(); flush_box(); flush_tbl()
            out.append(HRFlowable(width="100%", thickness=0.5, color=BLACK, spaceBefore=2, spaceAfter=2))
            continue
        if line == "TBL":
            flush_ex(); flush_box(); flush_tbl(); tbl = []
            continue
        if line == "ENDTBL":
            flush_tbl(); continue
        if tbl is not None:
            tbl.append([c.strip() for c in line.strip("|").split("|")])
            continue
        if line == "B<":
            flush_box(); continue
        if boxbuf is not None:
            flush_ex()
            if line.startswith("-"):
                boxbuf.append(Paragraph(inline(line[1:].strip()), ST["boxbullet"], bulletText="•"))
            elif line.startswith("F>"):
                boxbuf.append(Paragraph(inline(line[2:].strip()), ST["formula"]))
            elif line.startswith("T>"):
                boxbuf.append(Paragraph("<b>TRAP:</b> " + inline(line[2:].strip()), ST["boxbody"]))
            elif line.startswith("p>"):
                boxbuf.append(Paragraph(inline(line[2:].strip()), ST["boxbody"]))
            else:
                boxbuf.append(Paragraph(inline(line), ST["boxbody"]))
            continue
        if line == "B>":
            flush_ex(); flush_tbl(); boxbuf = []
            continue
        if line.startswith("##"):
            flush_ex(); flush_box(); flush_tbl()
            out.append(Paragraph(inline(line[2:].strip()), ST["h2"]))
            continue
        if line.startswith("E>"):
            flush_ex(); flush_box(); flush_tbl()
            exbuf = [Paragraph("REAL PYQ EXAMPLE — " + inline(line[2:].strip()), ST["exq"])]
            ex_sol_started[0] = False
            continue
        if exbuf is not None:
            if line.startswith("W>"):
                exbuf.append(Paragraph("<b>What this tests:</b> " + inline(line[2:].strip()), ST["exw"])); continue
            if line.startswith("x>"):
                pre = "<b>Solution:</b> " if not ex_sol_started[0] else ""
                ex_sol_started[0] = True
                exbuf.append(Paragraph(pre + inline(line[2:].strip()), ST["exb"])); continue
            if line.startswith("M>"):
                exbuf.append(Paragraph("<b>Fast method:</b> " + inline(line[2:].strip()), ST["exm"])); continue
            if line.startswith("K>"):
                exbuf.append(Paragraph("<b>Key takeaway:</b> " + inline(line[2:].strip()), ST["exk"])); continue
            if line.startswith("T>"):
                exbuf.append(Paragraph("<b>Trap:</b> " + inline(line[2:].strip()), ST["ext"])); continue
            if line.startswith("C>"):
                exbuf.append(Paragraph("<b>Correct:</b> " + inline(line[2:].strip()), ST["exc"])); continue
            flush_ex()
        if line.startswith("T>"):
            flush_box(); flush_tbl()
            out.append(Paragraph("<b>TRAP:</b> " + inline(line[2:].strip()), ST["trap"]))
            continue
        if line.startswith("C>"):
            out.append(Paragraph("<b>CORRECT:</b> " + inline(line[2:].strip()), ST["corr"]))
            continue
        if line.startswith("F>"):
            flush_box(); flush_tbl()
            out.append(Paragraph(inline(line[2:].strip()), ST["formula"]))
            continue
        if line.startswith("-"):
            out.append(Paragraph(inline(line[1:].strip()), ST["bullet"], bulletText="•"))
            continue
        if line.strip() == "":
            continue
        out.append(Paragraph(inline(line), ST["body"]))
    flush_ex(); flush_box(); flush_tbl()
    return out

class BookDoc(BaseDocTemplate):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._seen_page = None
    def afterFlowable(self, fl):
        pg = self.canv.getPageNumber()
        if isinstance(fl, ChapterTitle):
            CHAP_STARTS.append((pg, fl.name))
        if pg != self._seen_page:
            FIRST_FL[pg] = fl
            self._seen_page = pg

def build(content_path, pdf_path):
    global CHAP_STARTS, FIRST_FL
    CHAP_STARTS = []
    FIRST_FL = {}
    text = open(content_path, encoding="utf-8").read()
    story = parse(text)

    colw = (PAGE_W - ML - MR - COL_GAP) / 2.0
    fL = Frame(ML, MB, colw, PAGE_H - MT - MB, id="L", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    fR = Frame(ML + colw + COL_GAP, MB, colw, PAGE_H - MT - MB, id="R", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

    def chapter_at_top(pg):
        first = FIRST_FL.get(pg)
        if isinstance(first, ChapterTitle):
            return first.name
        name = None
        for p, n in CHAP_STARTS:
            if p < pg:
                name = n
            else:
                break
        return name

    def onpage(canv, doc):
        canv.saveState()
        canv.setFont("DVS", 7); canv.setFillColor(BLACK)
        canv.drawString(ML, PAGE_H - MT + 4, "IAF AGNIVEERVAYU PHYSICS MASTER NOTES")
        canv.setLineWidth(0.4)
        canv.line(ML, PAGE_H - MT + 1.5, PAGE_W - MR, PAGE_H - MT + 1.5)
        midx = ML + colw + COL_GAP / 2.0
        canv.setLineWidth(0.3)
        canv.line(midx, MB, midx, PAGE_H - MT)
        canv.restoreState()

    def onpageend(canv, doc):
        pg = canv.getPageNumber()
        canv.saveState()
        cn = chapter_at_top(pg)
        footer = (cn + "  |  Page " + str(pg)) if cn else "Page " + str(pg)
        canv.setFont("DVS", 7); canv.setFillColor(BLACK)
        canv.drawRightString(PAGE_W - MR, MB - 6, footer)
        canv.setLineWidth(0.4)
        canv.line(ML, MB - 3.5, PAGE_W - MR, MB - 3.5)
        canv.restoreState()

    doc = BookDoc(pdf_path, pagesize=A4, leftMargin=ML, rightMargin=MR, topMargin=MT, bottomMargin=MB,
                  title="IAF Agniveervayu Physics Master Notes", author="Physics Master Book")
    doc.addPageTemplates([PageTemplate(id="two", frames=[fL, fR], onPage=onpage, onPageEnd=onpageend)])
    doc.build(story)
    return len(CHAP_STARTS)

if __name__ == "__main__":
    import sys
    build(sys.argv[1], sys.argv[2])
    print("built", sys.argv[2])
