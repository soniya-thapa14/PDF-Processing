"""
Tutorial 03 — PDF to Markdown converter for chunking pipeline.

Converts each PDF in pdfs/ to Markdown, preserving:
- Headings (detected by font size)
- Paragraphs (body text)
- Tables (as GitHub-flavored pipe tables)
- Reading order (reconstructed from page geometry)

Reuses the approach from Tutorial 02 but generalized for any PDF.

Usage:
    uv run python tutorials/03-chunking-strategies/pdf_to_markdown.py
"""

import sys
from pathlib import Path

import pdfplumber
from collections import Counter


PDF_DIR = Path(__file__).parent / "pdfs"
OUTPUT_DIR = Path(__file__).parent / "results" / "markdown"


def _empty(cell):
    return cell is None or str(cell).strip() == ""


def _escape(cell):
    return ("" if cell is None else str(cell)).strip().replace("|", "\\|")


def _render_pipe_table(header, body):
    sep = ["---"] * len(header)
    lines = []
    lines.append("| " + " | ".join(_escape(c) for c in header) + " |")
    lines.append("| " + " | ".join(sep) + " |")
    for row in body:
        lines.append("| " + " | ".join(_escape(c) for c in row) + " |")
    return "\n".join(lines)


def _forward_fill(rows):
    filled = []
    for row in rows:
        new_row = list(row)
        for i, cell in enumerate(new_row):
            if _empty(cell) and i > 0:
                new_row[i] = new_row[i - 1]
        filled.append(new_row)

    if filled:
        for col in range(len(filled[0])):
            for row_i in range(1, len(filled)):
                if col < len(filled[row_i]) and _empty(filled[row_i][col]):
                    filled[row_i][col] = filled[row_i - 1][col]
    return filled


def _merged_header_rows(filled_rows, n=2):
    header = []
    for col in range(len(filled_rows[0])):
        parts = []
        seen = set()
        for row_i in range(min(n, len(filled_rows))):
            val = (filled_rows[row_i][col] or "").strip()
            if val and val not in seen:
                parts.append(val)
                seen.add(val)
        header.append(" ".join(parts))
    return header


def table_to_markdown(rows):
    if not rows or not rows[0]:
        return ""

    is_complex = False
    if len(rows) >= 2:
        for col in range(min(len(rows[0]), len(rows[1]))):
            if _empty(rows[0][col]) and not _empty(rows[1][col]):
                is_complex = True
                break

    if not is_complex:
        header = [c or "" for c in rows[0]]
        body = rows[1:]
        return _render_pipe_table(header, body)
    else:
        filled = _forward_fill(rows)
        header = _merged_header_rows(filled, n=2)
        body = filled[2:]
        note = "<!-- complex table: merged cells flattened, two-row header fused -->\n"
        return note + _render_pipe_table(header, body)


def pdf_to_markdown(pdf_path, output_path=None):
    """Convert a single PDF to Markdown. Returns the markdown string."""
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"{pdf_path} not found.")

    if output_path is None:
        output_path = OUTPUT_DIR / f"{pdf_path.stem}.md"
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    sizes = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for word in page.extract_words(extra_attrs=["size"]):
                sizes.append(round(word["size"], 1))

    if not sizes:
        output_path.write_text("", encoding="utf-8")
        return ""

    body_size = Counter(sizes).most_common(1)[0][0]

    blocks = []
    page_height = 10000

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            page_offset = page_num * page_height

            table_objects = page.find_tables()
            table_bboxes = [t.bbox for t in table_objects]

            def _inside_table(word):
                wx = (word["x0"] + word["x1"]) / 2
                wy = (word["top"] + word["bottom"]) / 2
                return any(
                    x0 <= wx <= x1 and t <= wy <= b
                    for x0, t, x1, b in table_bboxes
                )

            words = [
                w for w in page.extract_words(extra_attrs=["size"])
                if not _inside_table(w)
            ]

            lines = []
            for word in sorted(words, key=lambda w: (round(w["top"]), w["x0"])):
                placed = False
                for line in lines:
                    if abs(line["top"] - word["top"]) < 2:
                        line["words"].append(word)
                        placed = True
                        break
                if not placed:
                    lines.append({"top": word["top"], "words": [word]})

            para_lines = []
            para_top = None

            for line in sorted(lines, key=lambda l: l["top"]):
                text = " ".join(
                    w["text"] for w in sorted(line["words"], key=lambda w: w["x0"])
                )
                size = round(line["words"][0]["size"], 1)

                if size > body_size + 3:
                    if para_lines:
                        blocks.append({"top": page_offset + para_top, "md": " ".join(para_lines)})
                        para_lines = []
                        para_top = None
                    blocks.append({"top": page_offset + line["top"], "md": f"# {text}"})
                    continue

                elif size > body_size + 1:
                    if para_lines:
                        blocks.append({"top": page_offset + para_top, "md": " ".join(para_lines)})
                        para_lines = []
                        para_top = None
                    blocks.append({"top": page_offset + line["top"], "md": f"## {text}"})
                    continue

                if para_top is None:
                    para_top = line["top"]
                para_lines.append(text)

            if para_lines:
                blocks.append({"top": page_offset + para_top, "md": " ".join(para_lines)})

            for t in table_objects:
                rows = t.extract()
                md = table_to_markdown(rows)
                if md:
                    blocks.append({"top": page_offset + t.bbox[1], "md": md})

    blocks.sort(key=lambda b: b["top"])
    markdown = "\n\n".join(b["md"] for b in blocks)

    output_path.write_text(markdown, encoding="utf-8")
    print(f"  {pdf_path.name} → {output_path.name} ({len(blocks)} blocks)")
    return markdown


def convert_all():
    """Convert all PDFs in the pdfs/ directory to Markdown."""
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    if not pdfs:
        print(f"No PDFs found in {PDF_DIR}. Run generate_pdfs.py first.")
        return

    print(f"Converting {len(pdfs)} PDFs to Markdown...")
    for pdf_path in pdfs:
        pdf_to_markdown(pdf_path)
    print(f"Done. Markdown files in {OUTPUT_DIR}/")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        pdf_to_markdown(sys.argv[1])
    else:
        convert_all()
