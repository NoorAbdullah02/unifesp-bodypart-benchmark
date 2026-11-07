"""Build submission/manuscript.docx from MANUSCRIPT_v2.md + results/paper_tables.md + figures/.  uv run --with python-docx python build_docx.py"""
import re, os
from docx import Document
from docx.shared import Pt, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
md = open("MANUSCRIPT_v2.md", encoding="utf-8").read()
tables_md = open("results/paper_tables.md", encoding="utf-8").read()
doc = Document()
for s in doc.sections: s.left_margin = s.right_margin = Cm(2.2); s.top_margin = s.bottom_margin = Cm(2.2)
st = doc.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(11)
def runs(p, text):
    for part in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)", text):
        if not part: continue
        if part.startswith("**"): r = p.add_run(part[2:-2]); r.bold = True
        elif part.startswith("*") and len(part) > 2: r = p.add_run(part[1:-1]); r.italic = True
        elif part.startswith("`"): r = p.add_run(part[1:-1]); r.font.name = "Consolas"
        else: p.add_run(part)
# ---- split the manuscript: body (up to Figures) and figure list
body, _, figs = md.partition("## Figures (files in")
body = body.split("\n---\n", 1)[1] if "\n---\n" in body else body       # drop the working-status header
title = "How reliable are radiograph body-part classifiers? A leakage-controlled, cross-dataset benchmark with reliability and label-quality analysis on public data"
h = doc.add_heading(title, 0); h.alignment = WD_ALIGN_PARAGRAPH.LEFT
p = doc.add_paragraph(); r = p.add_run("[Author names, affiliations, corresponding author, ORCID - to be completed]"); r.italic = True
for line in body.split("\n"):
    line = line.rstrip()
    if not line.strip() or line.strip() == "---": continue
    if line.startswith("[[FIG|"):
        _, num, fn, cap = line.strip("[]").split("|", 3)
        png = "figures/" + fn.replace(".pdf", ".png")
        if os.path.exists(png):
            doc.add_picture(png, width=Inches(3.6 if fn.endswith("1.png") or "gradcam" in fn else 6.0)); doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            q = doc.add_paragraph(); rr = q.add_run("Fig. %s. " % num); rr.bold = True; q.add_run(cap)
        continue
    if line.startswith("## "): doc.add_heading(re.sub(r"^## \d* ?", "", line) if False else line[3:], 1)
    elif line.startswith("### "): doc.add_heading(line[4:], 2)
    elif re.match(r"^\* ", line): runs(doc.add_paragraph(style="List Bullet"), line[2:])
    elif re.match(r"^\d+\. ", line): runs(doc.add_paragraph(style="List Number"), re.sub(r"^\d+\. ", "", line))
    else: runs(doc.add_paragraph(), line)
# ---- tables
doc.add_page_break(); doc.add_heading("Tables", 1)
for block in re.split(r"\n(?=## Table )", tables_md):
    if not block.startswith("## Table"): continue
    lines = block.strip().split("\n"); doc.add_paragraph().add_run(lines[0][3:]).bold = True
    rows = [l for l in lines if l.startswith("|") and not re.match(r"^\|[-| ]+\|$", l)]
    cells = [[c.strip() for c in r.strip("|").split("|")] for r in rows]
    t = doc.add_table(rows=len(cells), cols=len(cells[0])); t.style = "Light Grid Accent 1"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(cells):
        for j, c in enumerate(row[:len(cells[0])]):
            cell = t.cell(i, j); cell.text = ""; pr = cell.paragraphs[0]; rr = pr.add_run(c); rr.font.size = Pt(8); rr.bold = (i == 0)
    for l in lines:
        if l.startswith("_") and l.endswith("_"): q = doc.add_paragraph(); rr = q.add_run(l.strip("_")); rr.italic = True; rr.font.size = Pt(8)
    doc.add_paragraph()
doc.save("submission/manuscript.docx"); print("wrote submission/manuscript.docx")
