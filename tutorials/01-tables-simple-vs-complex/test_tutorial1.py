"""
Tutorial 1 — make these tests pass.

    uv run pytest tutorials/01-tables-simple-vs-complex/test_tutorial1.py -v

They check the contract described in the README: a generator that builds a PDF
with one simple and one complex table, and a classifier that can tell them apart.
"""

from pathlib import Path

from reportlab.platypus import Table

from extract_tables import classify_table, extract
from generate_tables_pdf import build_complex_table, build_simple_table, generate


def test_generate_creates_a_real_pdf(tmp_path):
    out = generate(tmp_path / "doc.pdf")
    assert Path(out).exists(), "generate() should write a PDF and return its path"
    assert Path(out).stat().st_size > 1000, "the PDF looks empty"


def test_builders_return_reportlab_tables():
    assert isinstance(build_simple_table(), Table)
    assert isinstance(build_complex_table(), Table)


def test_classify_simple_table():
    rows = [
        ["Region", "Sales", "Customers"],
        ["North", "$1", "5"],
        ["South", "$2", "9"],
    ]
    kind, reasons = classify_table(rows)
    assert kind == "simple"
    assert reasons == []


def test_classify_complex_table():
    rows = [
        ["Region", "Country", "Q1", "", "Q2", ""],
        ["", "", "Revenue", "Units", "Revenue", "Units"],
        ["North America", "USA", "1", "2", "3", "4"],
        ["", "Canada", "5", "6", "7", "8"],
    ]
    kind, reasons = classify_table(rows)
    assert kind == "complex"
    assert reasons, "a complex verdict should come with at least one reason"


def test_extract_finds_one_simple_and_one_complex():
    tables = extract()  # builds the sample PDF if missing
    kinds = sorted(kind for kind, _rows in tables)
    assert kinds == ["complex", "simple"], f"expected one of each, got {kinds}"
