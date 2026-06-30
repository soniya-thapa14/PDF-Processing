"""
Tutorial 03 — Generate all 5 sample PDFs.

Each PDF has a distinct structure (40-50 pages, all vector/text-layer):
    1. zoning_ordinance.pdf    — deeply nested legal text
    2. permit_use_matrix.pdf   — dense tables with merged headers
    3. research_textbook.pdf   — pure academic prose
    4. technical_manual.pdf    — mixed layout (code, bullets, tables)
    5. financial_report.pdf    — table-heavy with commentary

Usage:
    uv run python tutorials/03-chunking-strategies/generate_pdfs.py
"""

from pathlib import Path

PDF_DIR = Path(__file__).parent / "pdfs"


def generate_all():
    """Generate all 5 sample PDFs."""
    PDF_DIR.mkdir(parents=True, exist_ok=True)

    from generate_zoning_ordinance import build_document as gen_zoning
    from generate_permit_matrix import build_pdf as gen_permit
    from generate_textbook import generate as gen_textbook
    from generate_technical_manual import main as gen_manual
    from generate_financial_report import generate as gen_financial

    generators = [
        ("zoning_ordinance.pdf", gen_zoning),
        ("permit_use_matrix.pdf", gen_permit),
        ("research_textbook.pdf", gen_textbook),
        ("technical_manual.pdf", gen_manual),
        ("financial_report.pdf", gen_financial),
    ]

    for name, gen_fn in generators:
        if (PDF_DIR / name).exists():
            print(f"  {name} already exists, skipping.")
        else:
            print(f"  Generating {name}...")
            gen_fn()
            print(f"  ✓ {name} created")

    print(f"\nAll PDFs in {PDF_DIR}/")


if __name__ == "__main__":
    generate_all()
