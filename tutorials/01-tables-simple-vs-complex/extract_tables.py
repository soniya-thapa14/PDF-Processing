"""
Tutorial 1, step 2 — extract the tables and tell SIMPLE from COMPLEX
(YOUR CODE GOES HERE)

`pdfplumber` always returns a RECTANGULAR grid. A merged cell shows up as the
text in its top-left corner and `None` (or "") everywhere else it covers. So
"are there holes in the interior of the grid?" is a strong signal for "merged /
complex table".

Implement the two functions marked TODO, then check your work with:
    uv run pytest tutorials/01-tables-simple-vs-complex/test_tutorial1.py

Run it directly to see your classifier on the real PDF (pass a path to use a
different file, e.g. one from ../sample_pdfs/):
    uv run python tutorials/01-tables-simple-vs-complex/extract_tables.py
"""

from pathlib import Path

import pdfplumber

from generate_tables_pdf import OUTPUT_PDF, generate


# --- given helpers (use these; you don't need to change them) ----------------
def _empty(cell):
    """A cell counts as empty if it is None or only whitespace."""
    return cell is None or str(cell).strip() == ""


def print_grid(rows, max_rows=12):
    """Pretty-print a grid so the holes (None) are easy to see."""
    for row in rows[:max_rows]:
        cells = ["·" if _empty(c) else str(c) for c in row]
        print("   | " + " | ".join(f"{c:<13}" for c in cells) + " |")
    if len(rows) > max_rows:
        print(f"   ... ({len(rows) - max_rows} more rows)")


# --- YOUR CODE ---------------------------------------------------------------
def classify_table(rows):
    """
    Return a tuple (kind, reasons) where:
        kind     is "simple" or "complex"
        reasons  is a list of short strings explaining a "complex" verdict
                 (empty list when the table is simple)

    A table is COMPLEX if any of these hold (each one is a reason string):
        - it has an interior empty cell: an empty cell that still has a filled
          cell somewhere to its right (a merge was flattened into None)
        - its rows are not all the same width
        - its header spans two rows: row 0 has an empty cell that row 1 fills
    Otherwise it is SIMPLE.
    """
    # TODO: build the `reasons` list using the rules above (use _empty()).
    #       Return ("complex", reasons) if reasons else ("simple", []).
    raise NotImplementedError("TODO: classify the table")


def extract(pdf_path=OUTPUT_PDF):
    """
    Open the PDF, pull every table with pdfplumber, classify each, print it, and
    return a list of (kind, rows). Build the default PDF first if it's missing.
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        if pdf_path == Path(OUTPUT_PDF):
            print(f"{pdf_path.name} not found — generating it first.")
            generate(pdf_path)
        else:
            raise FileNotFoundError(f"{pdf_path} not found.")

    # TODO:
    #   - open pdf_path with pdfplumber
    #   - for each page, for each table in page.extract_tables():
    #       classify it, print a header + reasons + print_grid(rows),
    #       and collect (kind, rows)
    #   - return the collected list
    raise NotImplementedError("TODO: extract and classify every table")


if __name__ == "__main__":
    import sys

    extract(sys.argv[1] if len(sys.argv) > 1 else OUTPUT_PDF)
