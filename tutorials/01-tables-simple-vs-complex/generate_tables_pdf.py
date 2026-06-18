from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import Table, SimpleDocTemplate, Paragraph, Spacer, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

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
DATA_SIMPLE = [
    ["Region", "Sales", "Customers", "Growth"],
    ["North", "$18,000", "50", "45%"],
    ["South", "$14,500", "39", "5%"],
    ["East", "$7,200", "25", "15%"],
    ["West", "$5,230", "13", "8%"],
    ["Total", "$45,230", "128", "23%"],
]

DATA_COMPLEX = [
    ["Region", "Country", "Q1", "", "Q2", ""],
    ["", "", "Revenue", "Units", "Revenue", "Units"],
    ["North America", "USA", "$12,000", "120", "$13,500", "135"],
    ["", "Canada", "$8,000", "80", "$9,200", "92"],
    ["Europe", "Germany", "$10,500", "105", "$11,000", "110"],
    ["", "France", "$7,300", "73", "$7,800", "78"],
]


def build_simple_table():
    col_widths = [3.5*cm, 3*cm, 3*cm, 3*cm]
    t = Table(DATA_SIMPLE, colWidths= col_widths)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
    ]))
    return t


def build_complex_table():
    col_widths = [3.5*cm, 2.5*cm, 2.5*cm, 2*cm, 2.5*cm, 2*cm]
    t = Table(DATA_COMPLEX, colWidths= col_widths)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, 0), (-1, 1), colors.lightgrey),
        ("FONTNAME", (0, 0), (-1, 1), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        # header merges
        ("SPAN", (0, 0), (0, 1)),
        ("SPAN", (1, 0), (1, 1)),
        ("SPAN", (2, 0), (3, 0)),
        ("SPAN", (4, 0), (5, 0)),
        
        #body row
        ("SPAN", (0, 2), (0, 3)),   
        ("SPAN", (0, 4), (0, 5)),
    ]))
    return t


def generate(output_path=OUTPUT_PDF):
    output_path = Path(output_path)
    styles = getSampleStyleSheet()
    normal = styles["Normal"]

    doc = SimpleDocTemplate(str(output_path), pagesize = A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)

    story = [

        Paragraph(INTRO_TEXT, styles["Heading1"]),
        Spacer(1, 0.5*cm),
        build_simple_table(),
        Spacer(1, 0.5*cm),
        Paragraph(MIDDLE_TEXT, normal),
        Spacer(1, 0.5*cm),
        build_complex_table(),
        Spacer(1, 0.5*cm),
        Paragraph(CLOSING_TEXT, normal)
    ]
    doc.build(story)
    return output_path



if __name__ == "__main__":
    generate()
