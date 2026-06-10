"""
Stretch exercise — build two MULTI-PAGE sample PDFs (10+ pages each)
(YOUR CODE GOES HERE)

Once your Tutorial 1 and 2 scripts work on the single-page sample, build bigger,
more realistic documents and run your code on them. These expose problems that
only appear across page boundaries (see the README in this folder).

    report_multipage.pdf       A long report: a title, many numbered sections of
                               headings + paragraphs, with the Tutorial-1 simple
                               and complex tables interspersed. Must be >= 10 pages.

    ledger_spanning_table.pdf  ONE big table (~440 rows) that continues across
                               every page, with a repeated header row
                               (LongTable + repeatRows=1) and a running page
                               header + "Page N" footer. Must be >= 10 pages.

There are no automated tests for this part — the goal is to run your extractor
and Markdown converter on these and study what breaks (split tables, repeated
headers, page furniture, the classifier's false positive on the ledger).
"""

import sys
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate  # also: LongTable, Paragraph, Spacer, TableStyle, getSampleStyleSheet

# Reuse the SIMPLE/COMPLEX table builders you wrote in Tutorial 1, so the report
# contains the very tables you already learned to extract.
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


def generate_report(output_path=REPORT_PDF, num_sections=16):
    """
    Build a multi-section report (>= 10 pages): a Title, then `num_sections`
    sections, each a Heading2 + a few BodyText paragraphs, with build_simple_table()
    and build_complex_table() dropped in every few sections. Return the path.
    """
    # TODO: assemble a Platypus `story` and doc.build() it. Generate enough
    #       paragraphs that the document is at least 10 pages.
    raise NotImplementedError("TODO: build the multi-page report")


def generate_ledger(output_path=LEDGER_PDF, n_rows=440):
    """
    Build a single long table that spans many pages (>= 10). Use a LongTable with
    repeatRows=1 so the header repeats on every page, and draw a running page
    header + "Page N" footer with onFirstPage/onLaterPages callbacks. Return path.

    Columns: Date, Txn ID, Description, Category, Debit, Credit, Balance.
    """
    # TODO: build the rows (deterministically), make a LongTable(..., repeatRows=1),
    #       and doc.build([table], onFirstPage=..., onLaterPages=...).
    raise NotImplementedError("TODO: build the page-spanning ledger")


if __name__ == "__main__":
    generate_report()
    generate_ledger()
