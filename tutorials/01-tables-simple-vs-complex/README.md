# Tutorial 1 — Simple vs. complex tables

## What you'll build

1. A generator that creates a PDF containing a **simple** table and a **complex**
   table with text in between (`generate_tables_pdf.py`).
2. An extractor that pulls the tables back out and **classifies** each as simple
   or complex (`extract_tables.py`).

## The concepts

A **simple** table is a plain rectangle: one header row, every row the same
width, no merged cells. A **complex** table has **merged cells** — a header that
spans several columns, a label that spans several rows, or a header band that is
two rows tall.

Why the distinction matters: `pdfplumber` always returns a **rectangular** grid.
A merged cell shows up as the text in its top-left corner and `None` (or `""`)
in every other cell it covers. So a merged table comes back full of holes, and if
you don't notice, values silently land in the wrong column. Before you can turn a
table into Markdown (Tutorial 2) or embed it, you have to know which kind it is.

## Your task

Open the two skeleton files and implement the functions marked `# TODO`:

| File | Implement |
|------|-----------|
| `generate_tables_pdf.py` | `build_simple_table()`, `build_complex_table()`, `generate()`. The data is given (`DATA_SIMPLE` / `DATA_COMPLEX`); you write the reportlab rendering, including the `SPAN` commands for the merges. |
| `extract_tables.py` | `classify_table(rows)` and `extract()`. The docstrings spell out the exact rules and return contracts. |

Key things the skeletons tell you:
- `build_complex_table()` must add a `("SPAN", (c0,r0), (c1,r1))` for each merge:
  Region (2 rows), Country (2 rows), Q1 (2 cols), Q2 (2 cols), North America
  (2 rows), Europe (2 rows). Keep a full `GRID` so pdfplumber can find the table.
- `classify_table(rows)` returns `(kind, reasons)` — `"simple"`/`"complex"` plus
  a list of short reason strings. A table is complex if it has an **interior
  empty cell** (an empty cell with a filled one to its right), **ragged row
  widths**, or a **two-row header** (row 0 has a hole that row 1 fills).

## Run / check your work

```bash
# see your classifier on the real PDF (builds the PDF if missing):
uv run python tutorials/01-tables-simple-vs-complex/extract_tables.py

# the definition of done — make these pass:
uv run pytest tutorials/01-tables-simple-vs-complex/ -v
```

When the complex table is right, its extracted grid will show holes where the
merges are — print them with the provided `print_grid()` helper (it draws `·`
for empty cells).

## Definition of done

- [ ] `uv run pytest tutorials/01-tables-simple-vs-complex/ -v` is all green.
- [ ] You can point to the exact `SPAN` commands that create each merge and say
      whether each merges rows or columns.
- [ ] You can explain why the complex table's `Q1` value appears once and the
      cell to its right comes back as `None`.

## Stretch goals

1. Make `classify_table()` also return **where** the merges are (row/column
   indices of the holes), not just a count — Tutorial 2 needs this to flatten.
2. Add a third table that is complex in a *different* way (e.g. a single title
   cell spanning the whole top row) and confirm your classifier still catches it.
3. Try `page.extract_tables()` with different
   [table settings](https://github.com/jsvine/pdfplumber#extracting-tables)
   (`vertical_strategy`, `horizontal_strategy`). When does detection break?
