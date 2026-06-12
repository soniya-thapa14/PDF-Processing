from pathlib import Path
import pdfplumber
from generate_tables_pdf import OUTPUT_PDF, generate


def _empty(cell):
    """A cell counts as empty if it is None or only whitespace."""
    return cell is None or str(cell).strip() == ""


def print_grid(rows, max_rows=12):
    for row in rows[:max_rows]:
        cells = ["·" if _empty(c) else str(c) for c in row]
        print("   | " + " | ".join(f"{c:<13}" for c in cells) + " |")
    if len(rows) > max_rows:
        print(f"   ... ({len(rows) - max_rows} more rows)")

def classify_table(rows):
    reasons = []
    width = [len(row) for row in rows]
    if len(set(width)) > 1:
        reasons.append("rows have uneven widths")
    
    found = False
    for row in rows:
        for i, cell in enumerate(row):
            if _empty(cell) and any(not _empty(row[j]) for j in range(i+1, len(row))):
                reasons.append("interior empty cell")
                found = True
                break
        if found:
            break
    
    if len(rows) >=2:
        for col in range(min(len(rows[0]), len(rows[1]))):
            if _empty(rows[0][col]) and not _empty(rows[1][0]):
                reasons.append("two-row header")
                break
    return ("complex", reasons) if reasons else ("simple", [])
    


def extract(pdf_path=OUTPUT_PDF):
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        if pdf_path == Path(OUTPUT_PDF):
            print(f"{pdf_path.name} not found — generating it first.")
            generate(pdf_path)
        else:
            raise FileNotFoundError(f"{pdf_path} not found.")

    results = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start =1):
            for table_num, rows in enumerate(page.extract_tables(), start=1):
                kind, reasons = classify_table(rows)
                print(f"\n--- Page {page_num}, Table {table_num}: {kind.upper()} ---")
                if reasons:
                    for r in reasons:
                        print(f" Reasons : {r}")
                print_grid(rows)
                results.append((kind, rows))
    return results

if __name__ == "__main__":
    import sys

    extract(sys.argv[1] if len(sys.argv) > 1 else OUTPUT_PDF)
