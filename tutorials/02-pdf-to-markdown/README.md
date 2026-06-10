# Tutorial 2 — PDF → Markdown

## What you'll build

A converter (`pdf_to_markdown.py`) that reads a PDF and emits clean **Markdown**:

- reconstruct **reading order** from page geometry (PDFs don't store it);
- detect **headings** from font size (`#` / `##`);
- turn a **simple** table into a GitHub-flavored pipe table;
- handle a **complex** (merged-cell) table — which Markdown can't represent
  exactly, so you make a lossy choice on purpose.

This builds on Tutorial 1: it reads the same `tables_doc.pdf`.

## Why it matters

Markdown is the format most downstream tools want — clean to chunk, embed, store
in a vector DB, and feed to an LLM. But a PDF stores only *where* things are
drawn, not *what* they are. There is no "paragraph" object and no "this comes
before that." You rebuild all of that from coordinates. Doing it by hand once is
the fastest way to understand what every "PDF-to-Markdown" library does under the
hood — and where it quietly loses information.

## The three hard parts (what your code has to do)

1. **Reading order.** `pdfplumber` gives you text and tables *separately*. Each
   word (`extract_words`) and each table (`find_tables`, which has a `.bbox`) has
   a vertical position. Drop words that fall inside a table's bbox, tag every
   block with its `top`, and sort top-to-bottom.

2. **Headings from font size.** `extract_words(extra_attrs=["size"])` gives each
   word its size. The most common size is body text; anything bigger is a
   heading. Rank the bigger sizes so the largest becomes `#`, the next `##`.
   Compute this scale **once across the whole document**, not per page — or a
   heading on a page without the title gets mistaken for the biggest text.

3. **Tables** (`table_to_markdown(rows)`):
   - *simple* → row 0 is the header, the rest is the body → a pipe table.
   - *complex* → Markdown has **no row/column spans**, so: **forward-fill** the
     merged holes (inherit from the left, then from above), **fuse** the two
     header rows (`Q1` + `Revenue` → `Q1 Revenue`), and prepend an HTML-comment
     **note** that the table was flattened. This is lossy on purpose — that's the
     lesson.

## Your task

Implement the functions marked `# TODO` in `pdf_to_markdown.py`
(`table_to_markdown` and `pdf_to_markdown`, plus any helpers you need). The
docstrings and the hint block in the file spell out the contracts.

## Run / check your work

```bash
# convert the Tutorial-1 PDF (writes tables_doc.md next to the script):
uv run python tutorials/02-pdf-to-markdown/pdf_to_markdown.py

# the definition of done — make these pass:
uv run pytest tutorials/02-pdf-to-markdown/ -v
```

Your output should look like this (paste it into a Markdown previewer to check):

```markdown
# Quarterly Business Review

Quarterly Business Review. This document mixes ordinary paragraphs ...

## Summary by Region

| Region | Sales | Customers | Growth |
| --- | --- | --- | --- |
| North | $18,000 | 50 | 45% |
...

## Regional Breakdown by Quarter

<!-- NOTE: this table had merged cells; Markdown can't express spans ... -->
| Region | Country | Q1 Revenue | Q1 Units | Q2 Revenue | Q2 Units |
| --- | --- | --- | --- | --- | --- |
| North America | USA | $12,000 | 120 | $13,500 | 135 |
| North America | Canada | $8,000 | 80 | $9,200 | 92 |
...
```

## Definition of done

- [ ] `uv run pytest tutorials/02-pdf-to-markdown/ -v` is all green.
- [ ] You can explain how your code decides heading vs. paragraph, and how it
      keeps the tables in the right order relative to the text.
- [ ] You can point to the exact lines that make the complex table lossy and name
      one piece of information that is lost.

## Stretch goals

1. **Compare to a library.** `uv add pymupdf4llm`, then
   `pymupdf4llm.to_markdown("tables_doc.pdf")`. Diff its output against yours.
2. **Raster path.** The root `raster.pdf` is a scan — `pdfplumber` finds no text.
   Wire in the OCR step from `pdf_extraction.py` so a scanned PDF can become
   Markdown too. What structure is lost when there's no text layer?
3. **Bigger documents.** Run your converter on the 10+ page samples in
   [`../sample_pdfs/`](../sample_pdfs/) and see what breaks.
4. **Toward embeddings.** Split the Markdown into chunks (e.g. by heading) — the
   input a vector store wants. What's a good chunk boundary for prose + tables?
