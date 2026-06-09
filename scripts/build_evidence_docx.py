#!/usr/bin/env python3
"""Convert cd_cvra_recom_v2_evidence.md -> .docx for clinician review.

Targeted converter for the evidence paper's specific structure:
  - # / ## / ### headings
  - GitHub-flavoured tables
  - **bold** / *italic* / `code` / [text](url) inline
  - Bullet lists (-)
  - Horizontal rules (---)
  - Blockquote-style notes via paragraphs

Run:  python3 picorules-agent/scripts/build_evidence_docx.py
Output: picorules-agent/new_rules/cd_cvra_recom_v2_evidence.docx
"""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Pt, RGBColor, Cm, Inches

ROOT = Path(__file__).resolve().parents[1] / "new_rules"
SRC = ROOT / "cd_cvra_recom_v2_evidence.md"
OUT = ROOT / "cd_cvra_recom_v2_evidence.docx"

HEADER_COLOR = RGBColor(0x12, 0x2C, 0x4F)
ACCENT       = RGBColor(0x1F, 0x4F, 0x91)


# --------------------------------------------------------------- inline parsing

INLINE_RE = re.compile(
    r"(\*\*[^*]+\*\*)"     # bold
    r"|(\*[^*]+\*)"        # italic
    r"|(`[^`]+`)"          # code
    r"|(\[[^\]]+\]\([^)]+\))"  # link
)


def add_inline(paragraph, text: str):
    """Append text to paragraph, honouring inline markdown formatting."""
    if text is None:
        return
    pos = 0
    for m in INLINE_RE.finditer(text):
        if m.start() > pos:
            paragraph.add_run(text[pos : m.start()])
        token = m.group(0)
        if token.startswith("**"):
            run = paragraph.add_run(token[2:-2])
            run.bold = True
        elif token.startswith("*"):
            run = paragraph.add_run(token[1:-1])
            run.italic = True
        elif token.startswith("`"):
            run = paragraph.add_run(token[1:-1])
            run.font.name = "Consolas"
            run.font.size = Pt(9)
            run.font.color.rgb = RGBColor(0x55, 0x33, 0x66)
        elif token.startswith("["):
            link_match = re.match(r"\[([^\]]+)\]\(([^)]+)\)", token)
            if link_match:
                add_hyperlink(paragraph, link_match.group(2), link_match.group(1))
        pos = m.end()
    if pos < len(text):
        paragraph.add_run(text[pos:])


def add_hyperlink(paragraph, url: str, text: str):
    part = paragraph.part
    r_id = part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)
    new_run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    rStyle = OxmlElement("w:rStyle")
    rStyle.set(qn("w:val"), "Hyperlink")
    rPr.append(rStyle)
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "1F4F91")
    rPr.append(color)
    u = OxmlElement("w:u")
    u.set(qn("w:val"), "single")
    rPr.append(u)
    new_run.append(rPr)
    t = OxmlElement("w:t")
    t.text = text
    new_run.append(t)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)


# --------------------------------------------------------------- table helpers

def shade_cell(cell, hex_color: str):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tc_pr.append(shd)


def add_table(doc, rows: list[list[str]]):
    if not rows:
        return
    n_cols = len(rows[0])
    table = doc.add_table(rows=len(rows), cols=n_cols)
    table.style = "Light Grid Accent 1"
    table.autofit = True

    for r_idx, row in enumerate(rows):
        for c_idx, cell_text in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = ""
            p = cell.paragraphs[0]
            add_inline(p, cell_text.strip())
            for run in p.runs:
                run.font.size = Pt(9)
                if r_idx == 0:
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
            if r_idx == 0:
                shade_cell(cell, "122C4F")
            elif r_idx % 2 == 0:
                shade_cell(cell, "F2F5FA")


# --------------------------------------------------------------- markdown parser

def parse_markdown(text: str) -> list[tuple[str, object]]:
    """Tokenise the evidence paper markdown into a flat sequence of blocks.

    Returns list of (kind, payload) tuples where kind is one of:
      h1, h2, h3, p, hr, ul, table, blank
    """
    lines = text.splitlines()
    tokens: list[tuple[str, object]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip()

        if not stripped:
            tokens.append(("blank", None))
            i += 1
            continue

        if stripped.startswith("# "):
            tokens.append(("h1", stripped[2:].strip()))
            i += 1
            continue
        if stripped.startswith("## "):
            tokens.append(("h2", stripped[3:].strip()))
            i += 1
            continue
        if stripped.startswith("### "):
            tokens.append(("h3", stripped[4:].strip()))
            i += 1
            continue

        if stripped.strip() == "---":
            tokens.append(("hr", None))
            i += 1
            continue

        if stripped.lstrip().startswith("- "):
            bullets = []
            while i < len(lines) and lines[i].lstrip().startswith("- "):
                bullets.append(lines[i].lstrip()[2:].strip())
                i += 1
            tokens.append(("ul", bullets))
            continue

        if stripped.lstrip().startswith("|") and stripped.rstrip().endswith("|"):
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                row_line = lines[i].strip()
                if re.fullmatch(r"\|[\s\-:|]+\|", row_line):
                    i += 1
                    continue  # separator
                cells = [c.strip() for c in row_line.strip("|").split("|")]
                rows.append(cells)
                i += 1
            if rows:
                tokens.append(("table", rows))
            continue

        para_lines = [stripped]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].lstrip().startswith(
            ("#", "-", "|", "---")
        ):
            para_lines.append(lines[i].rstrip())
            i += 1
        tokens.append(("p", " ".join(para_lines)))
    return tokens


# --------------------------------------------------------------- docx renderer

def configure_styles(doc: Document):
    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(10)

    for level, size in [(1, 20), (2, 14), (3, 11)]:
        st = styles[f"Heading {level}"]
        st.font.name = "Calibri"
        st.font.size = Pt(size)
        st.font.bold = True
        st.font.color.rgb = HEADER_COLOR


def render(tokens, doc: Document):
    for kind, payload in tokens:
        if kind == "h1":
            p = doc.add_paragraph(payload, style="Heading 1")
            p.paragraph_format.space_before = Pt(0)
        elif kind == "h2":
            p = doc.add_paragraph(payload, style="Heading 2")
            p.paragraph_format.space_before = Pt(14)
        elif kind == "h3":
            p = doc.add_paragraph(payload, style="Heading 3")
            p.paragraph_format.space_before = Pt(8)
        elif kind == "p":
            p = doc.add_paragraph()
            add_inline(p, payload)
        elif kind == "ul":
            for item in payload:
                p = doc.add_paragraph(style="List Bullet")
                add_inline(p, item)
        elif kind == "table":
            add_table(doc, payload)
            doc.add_paragraph()  # spacer after table
        elif kind == "hr":
            p = doc.add_paragraph()
            run = p.add_run("─" * 60)
            run.font.color.rgb = RGBColor(0xCC, 0xCC, 0xCC)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        # 'blank' tokens swallowed implicitly


# --------------------------------------------------------------- main

def main():
    text = SRC.read_text()
    tokens = parse_markdown(text)

    doc = Document()
    configure_styles(doc)
    for section in doc.sections:
        section.top_margin = Cm(1.8)
        section.bottom_margin = Cm(1.8)
        section.left_margin = Cm(2.0)
        section.right_margin = Cm(2.0)
        section.page_width = Inches(11)   # landscape for wide tables
        section.page_height = Inches(8.5)
        section.orientation = 1  # WD_ORIENT.LANDSCAPE

    # Document metadata for review use
    doc.core_properties.title = "CVD risk recommendations v2 — evidence traceability"
    doc.core_properties.author = "picorules-agent"
    doc.core_properties.subject = "cd_cvra_recom_v2 evidence audit"

    render(tokens, doc)

    doc.save(OUT)
    print(f"wrote {OUT}  ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
