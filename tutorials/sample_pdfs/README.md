# Stretch — multi-page sample PDFs (10+ pages)

The single-page `tables_doc.pdf` is enough to learn the core ideas, but real
documents are long and messy. Once Tutorials 1 and 2 pass their tests, build
these two **10+ page** documents and run your code on them. They expose problems
that only appear across page boundaries.

## Your task

Implement the two functions marked `# TODO` in `generate_large_samples.py`:

| Function | Build |
|----------|-------|
| `generate_report()` | A long report (**>= 10 pages**): a title, many numbered sections of heading + paragraphs, with your Tutorial-1 `build_simple_table()` / `build_complex_table()` dropped in every few sections. |
| `generate_ledger()` | **One** transaction table (~440 rows) that continues across every page (**>= 10 pages**): use a `LongTable` with `repeatRows=1` so the header repeats, and draw a running page header + `Page N` footer via the `onFirstPage` / `onLaterPages` callbacks. |

```bash
uv run python tutorials/sample_pdfs/generate_large_samples.py
# then run your Tutorial 1 / 2 code against the results:
uv run python tutorials/01-tables-simple-vs-complex/extract_tables.py \
    tutorials/sample_pdfs/report_multipage.pdf
uv run python tutorials/02-pdf-to-markdown/pdf_to_markdown.py \
    tutorials/sample_pdfs/ledger_spanning_table.pdf
```

(Confirm each PDF is at least 10 pages — e.g. open it, or count with PyMuPDF:
`import fitz; fitz.open(path).page_count`.)

## What to look for (write down what you find)

These are the lessons — run your own code and observe them:

1. **A table split by a page break becomes two tables.** A complex table that
   straddles a page boundary is detected as a header band on one page and a
   separate body on the next. How would you stitch them back together?

2. **A spanning table becomes one table per page.** The ledger is one logical
   table, but extraction returns ~11 — one slice per page, each repeating the
   header row.

3. **Page furniture pollutes the text.** The running header and the `Page N`
   footer are drawn on every page, so they appear in the extracted text on every
   page. Real pipelines strip headers/footers by position before parsing.

4. **Your classifier gives a false positive on the ledger.** Tutorial 1's rule
   says "interior empty cell -> merged cell," but each transaction has *either* a
   Debit *or* a Credit, leaving the other blank. Those legitimate blanks make the
   classifier call the ledger COMPLEX even though it has no merges. A blank *data*
   cell and a *merge* hole look identical to the simple rule.

5. **Heading scale must be document-wide.** If you computed the font-size scale
   per page in Tutorial 2, a section heading on a page without the title turns
   into `#`. Did yours? Fix it to use a document-wide scale.

## Stretch-of-the-stretch

1. **Stitch split tables** that continue across a page break into one.
2. **Strip page furniture** (top/bottom margin band) before building paragraphs.
3. **Fix the false positive** so the ledger is classified SIMPLE — distinguish a
   blank *data* cell from a *merge* hole by looking at *where* the blanks are.
4. **Reassemble the ledger** into a single Markdown table (one header, all rows).
