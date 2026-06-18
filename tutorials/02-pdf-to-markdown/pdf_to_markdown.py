
import sys
from pathlib import Path

import pdfplumber

_TUT1 = Path(__file__).parent.parent /"01-tables-simple-vs-complex"
sys.path.insert(0, str(_TUT1))
from generate_tables_pdf import generate  # noqa: E402

DEFAULT_PDF = _TUT1 / "tables_doc.pdf"
OUTPUT_DIR = Path(__file__).parent


def _empty(cell):
    return cell is None or str(cell).strip() == ""


def _escape(cell):
    """Markdown-escape a cell: a literal pipe would break the table layout."""
    return ("" if cell is None else str(cell)).strip().replace("|", "\\|")


def _render_pipe_table(header, body):
    sep = ["---"] * len(header)
    lines =[]
    lines.append("| " + " | ".join(_escape(c) for c in header) + " |")
    lines.append("| " + " | ".join(sep) + " |")
    for row in body:
        lines.append("| " + " | ".join(_escape(c) for c in row) + " |")
    return "\n".join(lines)

def _forward_fill(rows):
    filled =[]
    for row in rows:
        new_row = list(row)
        for i, cell in enumerate(new_row):
            if _empty(cell) and i > 0:
                new_row[i] = new_row[i-1]
        filled.append(new_row)

    for col in range(len(filled[0])):
        for row_i in range(1, len(filled)):
            if _empty(filled[row_i][col]):
                filled[row_i][col] = filled[row_i-1][col]
    return filled

def _merged_header_rows(filled_rows, n = 2):
    header =[]
    for col in range(len(filled_rows[0])):
        parts =[]
        seen = set()
        for row_i in range(n):
            val = (filled_rows[row_i][col] or "").strip()
            if val and val not in seen:
                parts.append(val)
                seen.add(val)
        header.append(" ".join(parts))
    return header

def table_to_markdown(rows):
    is_complex = False
    if len(rows) >= 2:
        for col in range(min(len(rows[0]), len(rows[1]))):
            if _empty(rows[0][col]) and not _empty(rows[1][col]):
                is_complex = True
                break
    
    if not is_complex:
        header = [ c or "" for c in rows[0]]
        body = rows[1:]
        return _render_pipe_table(header, body)
    else:
        filled = _forward_fill(rows)
        header = _merged_header_rows(filled, n=2)
        body =  filled[2:]
        note = "<!-- complex table: merged cells flattened, two-row header fused -->\n"

    return note + _render_pipe_table(header, body)
    

def pdf_to_markdown(pdf_path=DEFAULT_PDF, output_path=None):

    pdf_path = Path("pdf_path")
    if not pdf_path.exists():
        if pdf_path == Path(DEFAULT_PDF):
            print(f"{pdf_path.name} not found — building it from Tutorial 1.")
            generate(pdf_path)
        else:
            raise FileNotFoundError(f"{pdf_path} not found.")
    output_path = Path(output_path) if output_path else OUTPUT_DIR / f"{pdf_path.stem}.md"

    sizes = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for word in page.extract_words(extra_attrs = ["size"]):
                sizes.append(round(word["size"], 1))

    from collections import Counter
    body_size = Counter(sizes).most_common(1)[0][0]

    blocks =[]

    # Larger than any realistic PDF page height (in points)
    virtual_page_height = 10000
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            page_offset = page_num * virtual_page_height

            table_objects = page.find_tables()
            table_bboxes = [t.bbox for t in table_objects]

            def _inside_table(word):
                wx = (word["x0"] + word["x1"]) / 2 
                wy = (word["top"] + word["bottom"]) / 2 
                return any (
                    x0 <= wx <= x1 and t <= wy <= b
                    for x0, t, x1, b in table_bboxes
                ) 
            
            words = [w for w in page.extract_words(extra_attrs = ["size"])
                     if not _inside_table(w)]
            
            lines = []
            for word in sorted(words, key =lambda w: (round(w["top"]), w["x0"])):
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

            for line in sorted(lines, key = lambda l: l["top"]):
                text = " ".join(w["text"] for w in sorted(line["words"], key= lambda w: w["x0"]))
                size =round(line["words"][0]['size'], 1)

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
                blocks.append({"top": page_offset + t.bbox[1], "md":md})
    
    blocks.sort(key = lambda b: b["top"])
    markdown = "\n\n".join(b["md"] for b in blocks)
    
    output_path.write_text(markdown, encoding="utf-8")
    print(f"Written to {output_path}")
    return markdown

if __name__ == "__main__":
    pdf_to_markdown(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PDF)
