"""
Tutorial 1, step 1 — generate a sample PDF  (YOUR CODE GOES HERE)

Goal: build one PDF that contains, top to bottom:
    1. an intro paragraph (plain text)
    2. a SIMPLE table   — rectangular grid, one header row, no merged cells
    3. a paragraph of text in between
    4. a COMPLEX table  — merged column-group headers (Q1/Q2 each span two
                          sub-columns) AND merged row labels (a region name
                          spans two country rows)
    5. a closing paragraph

The data you must put in each table is given below (DATA_SIMPLE / DATA_COMPLEX).
Your job is to render it with reportlab. Read the README in this folder first.

Implement the three functions marked TODO, then check your work with:
    uv run pytest tutorials/01-tables-simple-vs-complex/test_tutorial1.py

Tip: do NOT call your functions at import time (no bare calls at the bottom of
the file). Only run them under `if __name__ == "__main__":`.
"""

from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import Table  # you will also want: SimpleDocTemplate, Paragraph, Spacer, TableStyle, getSampleStyleSheet

# Where this tutorial writes its sample PDF. Tutorial 2 reads the same file.
OUTPUT_PDF = Path(__file__).parent / "tables_doc.pdf"

INTRO_TEXT = (
    "Quarterly Business Review. This document mixes ordinary paragraphs with "
    "two tables. The first is a plain rectangular grid; the second uses merged "
    "header cells and merged row labels."
)
MIDDLE_TEXT = (
    "The summary table above is easy to parse: every row has the same number of "
    "filled cells and there is a single header row. The breakdown below is not."
)
CLOSING_TEXT = (
    "When this PDF becomes Markdown, the simple table maps cleanly onto a pipe "
    "table; the complex one cannot, because Markdown has no row/column spans."
)

# --- SIMPLE table: a plain rectangle, row 0 is the header --------------------
DATA_SIMPLE = [
    ["Region", "Sales", "Customers", "Growth"],
    ["North", "$18,000", "50", "45%"],
    ["South", "$14,500", "39", "5%"],
    ["East", "$7,200", "25", "15%"],
    ["West", "$5,230", "13", "8%"],
    ["Total", "$45,230", "128", "23%"],
]

# --- COMPLEX table: the empty strings mark where cells are MERGED ------------
# Row 0 + row 1 form a two-row header band. "Q1"/"Q2" each cover two columns
# (Revenue + Units). "Region"/"Country" cover both header rows. In the body,
# "North America" covers its two country rows, and so does "Europe".
DATA_COMPLEX = [
    ["Region", "Country", "Q1", "", "Q2", ""],
    ["", "", "Revenue", "Units", "Revenue", "Units"],
    ["North America", "USA", "$12,000", "120", "$13,500", "135"],
    ["", "Canada", "$8,000", "80", "$9,200", "92"],
    ["Europe", "Germany", "$10,500", "105", "$11,000", "110"],
    ["", "France", "$7,300", "73", "$7,800", "78"],
]


def build_simple_table():
    """
    Return a reportlab `Table` built from DATA_SIMPLE.

    Give it a visible GRID (pdfplumber needs the lines to detect the table) and
    make row 0 look like a header (bold). No merges here.
    """
    # TODO: create a Table(DATA_SIMPLE, colWidths=[...]) and apply a TableStyle
    #       with at least a ("GRID", ...) line. Return the Table.
    raise NotImplementedError("TODO: build the simple table")


def build_complex_table():
    """
    Return a reportlab `Table` built from DATA_COMPLEX, with the merges applied.

    Use ("SPAN", (col_start, row_start), (col_end, row_end)) in the TableStyle
    for each merged region described next to DATA_COMPLEX. Keep a full GRID.
    """
    # TODO: create a Table(DATA_COMPLEX, ...) and a TableStyle that includes a
    #       SPAN for: Region (2 rows), Country (2 rows), Q1 (2 cols),
    #       Q2 (2 cols), North America (2 rows), Europe (2 rows). Return it.
    raise NotImplementedError("TODO: build the complex table with SPANs")


def generate(output_path=OUTPUT_PDF):
    """
    Build the PDF (intro text, simple table, middle text, complex table, closing
    text) and return the path it was written to.
    """
    output_path = Path(output_path)
    # TODO: use SimpleDocTemplate + a story list of
    #       [Paragraph, Spacer, build_simple_table(), Paragraph,
    #        build_complex_table(), Paragraph], then doc.build(story).
    #       Return output_path.
    raise NotImplementedError("TODO: assemble and build the document")


if __name__ == "__main__":
    generate()
