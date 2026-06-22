"""
Tutorial 03 — Run all chunking strategies against all PDFs.

Produces a results matrix in results/chunks/ and a summary table.

Usage:
    uv run python tutorials/03-chunking-strategies/run_all.py
"""

import json
import sys
from pathlib import Path

from chunking_strategies import get_all_strategies
from pdf_to_markdown import OUTPUT_DIR as MD_DIR, PDF_DIR, convert_all

RESULTS_DIR = Path(__file__).parent / "results" / "chunks"


def run_matrix():
    """Apply every strategy to every PDF's markdown and collect stats."""
    MD_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    md_files = sorted(MD_DIR.glob("*.md"))
    if not md_files:
        print("No Markdown files found. Converting PDFs first...")
        convert_all()
        md_files = sorted(MD_DIR.glob("*.md"))

    if not md_files:
        print("Still no Markdown files. Generate PDFs first: python generate_pdfs.py")
        sys.exit(1)

    strategies = get_all_strategies()
    summary = []

    print(f"\nRunning {len(strategies)} strategies × {len(md_files)} documents...\n")
    print(f"{'PDF':<25} {'Strategy':<20} {'Chunks':<8} {'Avg Size':<10} {'Min':<6} {'Max':<8}")
    print("-" * 80)

    for md_path in md_files:
        text = md_path.read_text(encoding="utf-8")
        pdf_name = md_path.stem

        for strat_name, chunk_fn in strategies.items():
            try:
                chunks = chunk_fn(text)
                if isinstance(chunks[0], dict):
                    chunk_records = [
                        {"chunk_id": i, **c} if "content" in c else {"chunk_id": i, "content": "", **c}
                        for i, c in enumerate(chunks)
                    ]
                else:
                    chunk_records = [{"chunk_id": i, "content": c} for i, c in enumerate(chunks)]
                chunk_texts = [c["content"] for c in chunk_records]

                sizes = [len(c) for c in chunk_texts]
                avg_size = sum(sizes) / len(sizes) if sizes else 0
                min_size = min(sizes) if sizes else 0
                max_size = max(sizes) if sizes else 0

                print(f"{pdf_name:<25} {strat_name:<20} {len(chunks):<8} {avg_size:<10.0f} {min_size:<6} {max_size:<8}")

                result = {
                    "pdf": pdf_name,
                    "strategy": strat_name,
                    "num_chunks": len(chunks),
                    "avg_size_chars": round(avg_size),
                    "min_size": min_size,
                    "max_size": max_size,
                    "sample_first_3": chunk_records[:3],
                }
                summary.append(result)

                out_file = RESULTS_DIR / f"{pdf_name}__{strat_name}.json"
                out_file.write_text(
                    json.dumps({"chunks": chunk_records, "stats": result}, indent=2),
                    encoding="utf-8",
                )

            except NotImplementedError as e:
                print(f"{pdf_name:<25} {strat_name:<20} {'SKIP':<8} (not implemented)")
            except Exception as e:
                print(f"{pdf_name:<25} {strat_name:<20} {'ERROR':<8} {e}")

    summary_path = RESULTS_DIR / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\nSummary written to {summary_path}")

    _write_summary_markdown(summary)


def _write_summary_markdown(summary):
    """Write a human-readable summary table."""
    md_path = RESULTS_DIR / "summary.md"
    lines = ["# Chunking Results Matrix\n"]
    lines.append("| PDF | Strategy | Chunks | Avg Size | Min | Max |")
    lines.append("|-----|----------|--------|----------|-----|-----|")
    for r in summary:
        lines.append(
            f"| {r['pdf']} | {r['strategy']} | {r['num_chunks']} | "
            f"{r['avg_size_chars']} | {r['min_size']} | {r['max_size']} |"
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Markdown summary: {md_path}")


if __name__ == "__main__":
    run_matrix()
