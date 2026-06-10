"""
Tutorial 2 — make these tests pass.

    uv run pytest tutorials/02-pdf-to-markdown/test_tutorial2.py -v

They check the contract described in the README: simple tables become clean pipe
tables, complex tables get flattened (headers fused, merged labels filled), and a
whole PDF round-trips into ordered Markdown.
"""

from pdf_to_markdown import pdf_to_markdown, table_to_markdown


def test_simple_table_to_markdown():
    rows = [["A", "B"], ["1", "2"], ["3", "4"]]
    md = table_to_markdown(rows)
    lines = [ln for ln in md.strip().splitlines() if ln.strip()]
    assert lines[0] == "| A | B |", "row 0 should be the header"
    # second line is the separator: only pipes, dashes, spaces
    assert set(lines[1]) <= set("| -"), "missing the |---| separator row"
    assert "| 1 | 2 |" in md and "| 3 | 4 |" in md


def test_complex_table_is_flattened():
    rows = [
        ["Region", "Country", "Q1", "", "Q2", ""],
        ["", "", "Revenue", "Units", "Revenue", "Units"],
        ["North America", "USA", "1", "2", "3", "4"],
        ["", "Canada", "5", "6", "7", "8"],
    ]
    md = table_to_markdown(rows)
    assert "Q1 Revenue" in md, "the two header rows should be fused with a space"
    assert "Q2 Units" in md
    # the merged region label should be forward-filled onto the Canada row
    assert md.count("North America") >= 2


def test_pdf_to_markdown_end_to_end(tmp_path):
    md = pdf_to_markdown(output_path=tmp_path / "out.md")
    assert md.lstrip().startswith("#"), "the document should open with a heading"
    assert "| ---" in md, "expected at least one GitHub-flavored pipe table"
    # content from both tables should be present
    assert "Sales" in md, "simple table content missing"
    assert "Country" in md, "complex table content missing"
    assert (tmp_path / "out.md").exists()
