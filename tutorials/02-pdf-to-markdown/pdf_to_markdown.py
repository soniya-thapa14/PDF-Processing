"""
Tutorial 2 — convert a PDF into Markdown, by hand  (YOUR CODE GOES HERE)

Read the PDF from Tutorial 1 (text + a simple table + a complex, merged-cell
table) and emit Markdown that preserves reading order:

    - headings (detected by font size)   -> `#` / `##`
    - paragraphs                         -> plain text
    - the SIMPLE table                   -> a GitHub-flavored pipe table
    - the COMPLEX table                  -> a FLATTENED pipe table + a note

There is no clean way to express row/column spans in Markdown, so for the
complex table you must make a lossy, documented choice (see README): forward-fill
the merged holes and fuse the two header rows (e.g. "Q1" + "Revenue" ->
"Q1 Revenue").

Implement the functions marked TODO, then check your work with:
    uv run pytest tutorials/02-pdf-to-markdown/test_tutorial2.py

Read the README in this folder first — it walks through the three hard parts
(reading order, headings from font size, flattening a complex table).
"""

import sys
from pathlib import Path

import pdfplumber

# Tutorial 2 reads the PDF that Tutorial 1 builds. Import its generator so this
# script still works if you run it before building the PDF yourself.
_TUT1 = Path(__file__).parent.parent / "01-tables-simple-vs-complex"
sys.path.insert(0, str(_TUT1))
from generate_tables_pdf import generate  # noqa: E402

DEFAULT_PDF = _TUT1 / "tables_doc.pdf"
OUTPUT_DIR = Path(__file__).parent


# --- given helpers (use these; you don't need to change them) ----------------
def _empty(cell):
    return cell is None or str(cell).strip() == ""


def _escape(cell):
    """Markdown-escape a cell: a literal pipe would break the table layout."""
    return ("" if cell is None else str(cell)).strip().replace("|", "\\|")


# --- YOUR CODE: tables -> markdown -------------------------------------------
def table_to_markdown(rows):
    """
    Turn one extracted table grid into a Markdown pipe table (returned as a str).

    SIMPLE table  (row 0 has no holes): row 0 is the header, the rest is the body.
        | h1 | h2 |
        | --- | --- |
        | a | b |

    COMPLEX table (row 0 has a hole that row 1 fills -> two-row header):
        1. forward-fill the holes: an empty cell inherits the nearest filled cell
           to its LEFT, then (for any still-empty cell) the one ABOVE it.
        2. fuse the two header rows into one, joined by a space ("Q1 Revenue").
        3. prepend an HTML comment noting the table was flattened.
    """
    # TODO: detect simple vs complex (reuse the rule from Tutorial 1), then
    #       render. Helpers you may want to write: _render_pipe_table(header,
    #       body), _forward_fill(rows), _merge_header_rows(filled, n).
    raise NotImplementedError("TODO: render a table as Markdown")


# --- YOUR CODE: text + reading order -----------------------------------------
# Hints for the page assembly you need below:
#   - page.find_tables() gives Table objects; each has .bbox (x0, top, x1,
#     bottom) and .extract() (the grid). Use .bbox to know where the table sits.
#   - page.extract_words(extra_attrs=["size"]) gives each word an x0/x1/top/
#     bottom and a font "size". Drop words whose center is inside a table bbox.
#   - group words into lines by similar `top`; a line's font size tells you if
#     it is a heading (bigger than the most common = body size).
#   - tag every block (heading / paragraph line / table) with its `top` and sort
#     top-to-bottom to recover reading order. Compute the heading size scale ONCE
#     across the whole document, not per page.


def pdf_to_markdown(pdf_path=DEFAULT_PDF, output_path=None):
    """
    Convert the whole PDF to Markdown, write it to `<input-stem>.md` next to this
    script (unless output_path is given), and return the Markdown string.
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        if pdf_path == Path(DEFAULT_PDF):
            print(f"{pdf_path.name} not found — building it from Tutorial 1.")
            generate(pdf_path)
        else:
            raise FileNotFoundError(f"{pdf_path} not found.")
    output_path = Path(output_path) if output_path else OUTPUT_DIR / f"{pdf_path.stem}.md"

    # TODO:
    #   - open pdf_path with pdfplumber
    #   - for each page, recover (headings, paragraphs, tables) in reading order
    #     and render to Markdown (use table_to_markdown for tables)
    #   - join the pages, write to output_path, and return the string
    raise NotImplementedError("TODO: convert the PDF to Markdown")


if __name__ == "__main__":
    pdf_to_markdown(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PDF)
