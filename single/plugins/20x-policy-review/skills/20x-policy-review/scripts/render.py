#!/usr/bin/env python3
"""Render a skill's deliverable to Word or Excel for the client.

The Markdown and JSON files stay the source of truth. Render after the SME Validate
step, so the client copy matches the validated source.

  render.py docx REPORT.md OUT.docx    Markdown (front matter, headings, paragraphs,
                                       bullets, numbered lists, tables, bold, code) to Word
  render.py xlsx TABLES.json OUT.xlsx  {"title": ..., "sheets": [{"name", "columns", "rows"}]}
                                       to an Excel workbook, one sheet per table

Front matter at the top of the Markdown (between two lines of ---) becomes the
document control table on the first page. Needs python-docx and openpyxl:
  pip install python-docx openpyxl
"""
import json
import re
import sys
from pathlib import Path

DRAFT_MARK = "Draft: pending SME validation"
LABELS = {"frmr_version": "FRMR version", "sme_validation": "SME validation", "class": "Class",
          "prepared_by": "Prepared by", "client": "Client", "date": "Date"}


def parse_front_matter(text: str):
    meta = {}
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            for line in text[4:end].splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip().strip('"')
            text = text[end + 4:].lstrip("\n")
    return meta, text


def add_runs(par, text: str):
    """Add text to a paragraph, honouring **bold** and `code`."""
    for part in re.split(r"(\*\*[^*]+\*\*|`[^`]+`)", text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            par.add_run(part[2:-2]).bold = True
        elif part.startswith("`") and part.endswith("`"):
            r = par.add_run(part[1:-1])
            r.font.name = "Consolas"
        else:
            par.add_run(re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", part))


def shade(cell, fill="D9E2F3"):
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)


def to_docx(src: Path, out: Path):
    from docx import Document
    from docx.shared import Pt, RGBColor

    meta, body = parse_front_matter(src.read_text(encoding="utf-8"))
    doc = Document()
    from docx.enum.section import WD_ORIENT
    from docx.shared import Inches
    sec = doc.sections[0]
    if meta.get("orientation", "landscape") == "landscape":
        sec.orientation = WD_ORIENT.LANDSCAPE
        sec.page_width, sec.page_height = sec.page_height, sec.page_width
    for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, side, Inches(0.8))
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(11)

    if meta.get("title"):
        doc.add_heading(meta["title"], level=0)
    status = meta.get("sme_validation", DRAFT_MARK)
    if status.lower().startswith("draft") or status == DRAFT_MARK:
        p = doc.add_paragraph()
        r = p.add_run(DRAFT_MARK.upper())
        r.bold = True
        r.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)
    if meta:
        t = doc.add_table(rows=0, cols=2)
        t.style = "Table Grid"
        for k, v in meta.items():
            if k == "title":
                continue
            row = t.add_row().cells
            row[0].text = LABELS.get(k, k.replace("_", " ").capitalize())
            row[1].text = v
        doc.add_paragraph()

    lines = body.splitlines()
    i = 0
    in_code = False
    code_buf = []
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("```"):
            if in_code:
                p = doc.add_paragraph()
                r = p.add_run("\n".join(code_buf))
                r.font.name = "Consolas"
                r.font.size = Pt(9)
                code_buf = []
            in_code = not in_code
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)", line)
        if m and len(m.group(1)) == 1 and m.group(2).strip() == meta.get("title"):
            i += 1
            continue
        if m:
            doc.add_heading(m.group(2).strip(), level=min(len(m.group(1)), 4))
            i += 1
            continue
        if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|$", lines[i + 1].strip()):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                if not re.match(r"^\|[\s:|-]+\|$", lines[i].strip()):
                    cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                    rows.append(cells)
                i += 1
            ncol = max(len(r) for r in rows)
            t = doc.add_table(rows=0, cols=ncol)
            t.style = "Table Grid"
            for ri, cells in enumerate(rows):
                rc = t.add_row().cells
                for ci in range(ncol):
                    par = rc[ci].paragraphs[0]
                    add_runs(par, cells[ci] if ci < len(cells) else "")
                    for run in par.runs:
                        run.font.size = Pt(9)
                        if ri == 0:
                            run.bold = True
                    if ri == 0:
                        shade(rc[ci])
            doc.add_paragraph()
            continue
        m = re.match(r"^\s*[-*]\s+(.*)", line)
        if m:
            add_runs(doc.add_paragraph(style="List Bullet"), m.group(1))
            i += 1
            continue
        m = re.match(r"^\s*\d+\.\s+(.*)", line)
        if m:
            add_runs(doc.add_paragraph(style="List Number"), m.group(1))
            i += 1
            continue
        if line.startswith(">"):
            p = doc.add_paragraph()
            add_runs(p, line.lstrip("> "))
            for run in p.runs:
                run.italic = True
            i += 1
            continue
        if line.strip():
            para = [line.strip()]
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r"^(#|\||\s*[-*]\s|\s*\d+\.\s|>|```)", lines[i]):
                para.append(lines[i].strip())
                i += 1
            add_runs(doc.add_paragraph(), " ".join(para))
            continue
        i += 1
    doc.save(out)


def to_xlsx(src: Path, out: Path):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter

    data = json.loads(src.read_text(encoding="utf-8"))
    wb = Workbook()
    wb.remove(wb.active)
    status = data.get("sme_validation", DRAFT_MARK)
    about = wb.create_sheet("About")
    about.append([data.get("title", src.stem)])
    about["A1"].font = Font(bold=True, size=14)
    about.append(["SME validation", status])
    for k in ("client", "class", "frmr_version", "prepared_by", "date"):
        if k in data:
            about.append([k.replace("_", " ").capitalize(), str(data[k])])
    about.column_dimensions["A"].width = 22
    about.column_dimensions["B"].width = 80
    head_fill = PatternFill("solid", fgColor="1F3864")
    for sheet in data["sheets"]:
        ws = wb.create_sheet(sheet["name"][:31])
        ws.append(sheet["columns"])
        for c in ws[1]:
            c.font = Font(bold=True, color="FFFFFF")
            c.fill = head_fill
            c.alignment = Alignment(wrap_text=True, vertical="top")
        for row in sheet["rows"]:
            ws.append(["; ".join(map(str, v)) if isinstance(v, list) else v for v in row])
        for ci, col in enumerate(sheet["columns"], 1):
            longest = max([len(str(col))] + [len(str(r[ci - 1])) if ci - 1 < len(r) else 0 for r in sheet["rows"]])
            ws.column_dimensions[get_column_letter(ci)].width = min(max(12, longest + 2), 60)
        for row in ws.iter_rows(min_row=2):
            for c in row:
                c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions
    wb.save(out)


def main(argv=None):
    a = argv or sys.argv[1:]
    if a[:1] in (["-h"], ["--help"]):
        print(__doc__)
        return
    if len(a) != 3 or a[0] not in ("docx", "xlsx"):
        sys.exit(__doc__)
    src, out = Path(a[1]), Path(a[2])
    (to_docx if a[0] == "docx" else to_xlsx)(src, out)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
