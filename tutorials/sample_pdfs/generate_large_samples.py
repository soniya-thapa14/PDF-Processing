import sys
from pathlib import Path
from datetime import date, timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, LongTable, Paragraph, Spacer, TableStyle
from reportlab.lib.styles import getSampleStyleSheet 

_TUT1 = Path(__file__).parent.parent / "01-tables-simple-vs-complex"
sys.path.insert(0, str(_TUT1))
from generate_tables_pdf import build_complex_table, build_simple_table  # noqa: E402

HERE = Path(__file__).parent
REPORT_PDF = HERE / "report_multipage.pdf"
LEDGER_PDF = HERE / "ledger_spanning_table.pdf"

SECTION_TITLES = [
    "Executive Summary", "Market Overview", "Revenue Performance",
    "Regional Operations", "Customer Acquisition", "Product Lines",
    "Supply Chain", "Headcount and Hiring", "Research and Development",
    "Risk and Compliance", "Sustainability", "Capital Expenditure",
]

TEXT = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod "
    "tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, "
    "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo. "
    "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore "
    "eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident."
)

def generate_report(output_path=REPORT_PDF, num_sections=16):
    output_path = Path(output_path)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Annual Business Report", styles["Title"]))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("Prepared by the Analytics Team", styles["Normal"]))
    story.append(Spacer(1, 2*cm))

    for i, title in enumerate(SECTION_TITLES[:num_sections]):
        story.append(Paragraph(title, styles["Heading2"]))
        story.append(Spacer(1, 0.3*cm))

        for _ in range(4):
            story.append(Paragraph(TEXT, styles["BodyText"]))
            story.append(Spacer(1, 0.2*cm))

        if i % 3 == 1: 
            story.append(Spacer(1, 0.4*cm))
            story.append(Paragraph("Summary Table", styles['Heading3']))
            story.append(build_simple_table())
            story.append(Spacer(1, 0.4*cm))

        elif i % 3 ==2:
            story.append(Spacer(1, 0.4*cm))
            story.append(Paragraph("Regional Breakdown", styles["Heading3"]))
            story.append(build_complex_table())
            story.append(Spacer(1, 0.4*cm))

    doc = SimpleDocTemplate(
        str(output_path), pagesize = A4,
        leftMargin = 2*cm, rightMargin =2*cm,
        topMargin = 2*cm, bottomMargin = 2*cm,
    )
    doc.build(story)
    print(f"Report Written to {output_path}")
    return output_path


def generate_ledger(output_path=LEDGER_PDF, n_rows=440):
    output_path =Path(output_path)
    header = ["Date", "Txn ID", "Description", "Category", "Debit", "Credit", "Balance"]
    categories = ["Payroll", "Software", "Travel", "Marketing", "Office", "Utilities"]
    descriptions = ["Vendor payment", "Subscription renewal", "Reimbursement",
                    "Ad spend", "Office supplies", "Electricity bill"]
    
    rows =[header]
    balance = 50000.00
    start = date(2025, 1, 1)

    for i in range(n_rows):
        d = start + timedelta(days = i)
        txn_id = f"TXN{i + 1:04d}"
        desc = descriptions[i % len(descriptions)]
        cat = categories[i % len(categories)]
        if i % 3 == 0:
            debit = f"Rs{(i % 10 + 1) * 100:.2f}"
            credit = ""
            balance -= (i % 10 +1) * 100
        else:
            debit = ""
            credit = f"RS{(i % 5 + 1) *200:.2f}"
            balance += (i % 5 +1) * 200
        rows.append([str(d), txn_id, desc, cat, debit, credit, f"RS{balance:,.2f}"])

    def _draw_header_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.drawString(2*cm, A4[1] - 1.5*cm,  "Ledger Report 2025")
        canvas.drawString(A4[0] - 2*cm, 1*cm, f"page {doc.page}")
        canvas.restoreState()

    col_widths = [3*cm, 2*cm, 4*cm, 3*cm, 2*cm, 2*cm, 3*cm]
    table = LongTable(rows, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("ROWBACKGROUND", (0, 1), (-1, -1), colors.white),
    ]))

    doc = SimpleDocTemplate(
        str(output_path), pagesize = A4,
        leftMargin = 2*cm, rightMargin = 2*cm,
        topMargin = 2.5*cm, bottomMargin = 1.5*cm,
    )
    doc.build(
        [table],
        onFirstPage=_draw_header_footer,
        onLaterPages=_draw_header_footer,
    )
    print(f"Ledger written to {output_path}")
    print(output_path)


if __name__ == "__main__":
    generate_report()
    generate_ledger()