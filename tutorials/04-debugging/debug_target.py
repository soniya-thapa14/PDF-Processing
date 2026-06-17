"""
Tutorial 04 — Debug Target

This script contains a BUGGY chunking function. Your job is to use the VSCode
debugger to find and fix the bug.

The function `chunk_with_overlap_buggy()` is supposed to split text into chunks
of `chunk_size` characters with `overlap` characters shared between consecutive
chunks. But it has an off-by-one error that creates GAPS between chunks.

Usage:
    uv run python tutorials/04-debugging/debug_target.py
    uv run python tutorials/04-debugging/debug_target.py fixed_char
    uv run python tutorials/04-debugging/debug_target.py recursive
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "03-chunking-strategies"))

SAMPLE_TEXT = (
    "The quick brown fox jumps over the lazy dog. "
    "Pack my box with five dozen liquor jugs. "
    "How vexingly quick daft zebras jump. "
    "The five boxing wizards jump quickly. "
    "Sphinx of black quartz, judge my vow. "
    "Two driven jocks help fax my big quiz. "
    "The jay, pig, fox, zebra and my wolves quack. "
    "Jackdaws love my big sphinx of quartz. "
    "We promptly judged antique ivory buckles for the next prize. "
    "A mad boxer shot a quick, gloved jab to the jaw of his dizzy opponent. "
    "The job requires extra pluck and zeal from every young wage earner. "
    "Few quips galvanized the mock jury box. "
)


def chunk_with_overlap_buggy(text: str, chunk_size: int = 80, overlap: int = 20) -> list[str]:
    """
    Split text into fixed-size chunks with overlap.

    BUG: There's an off-by-one error in the position advancement.
    The stride should be (chunk_size - overlap) but the implementation
    has a subtle mistake. Use the debugger to find it!
    """
    chunks = []
    position = 0
    text_len = len(text)

    while position < text_len:
        end = position + chunk_size
        chunk = text[position:end]
        chunks.append(chunk)

        # BUG IS HERE: stride calculation is wrong
        # Should advance by (chunk_size - overlap) but advances by (chunk_size - overlap + 1)
        position = position + (chunk_size - overlap + 1)

    return chunks


def verify_chunks(text, chunks, overlap):
    """Verify that chunks tile the text correctly with proper overlap."""
    errors = []
    for i in range(len(chunks) - 1):
        tail = chunks[i][-overlap:]
        head = chunks[i + 1][:overlap]
        if tail != head:
            errors.append(
                f"  Chunk {i} tail: {repr(tail)}\n"
                f"  Chunk {i+1} head: {repr(head)}\n"
                f"  → Gap or misalignment at chunk boundary {i}/{i+1}"
            )
    return errors


def run_debug_target():
    """Run the buggy function and report the problem."""
    print("=" * 60)
    print("DEBUG TARGET — Find the bug!")
    print("=" * 60)
    print(f"\nInput text length: {len(SAMPLE_TEXT)} characters")
    print(f"Chunk size: 80, Overlap: 20\n")

    chunks = chunk_with_overlap_buggy(SAMPLE_TEXT, chunk_size=80, overlap=20)
    print(f"Produced {len(chunks)} chunks\n")

    errors = verify_chunks(SAMPLE_TEXT, chunks, overlap=20)

    if errors:
        print("BUG: chunks have gaps!\n")
        for err in errors[:3]:
            print(err)
            print()
        if len(errors) > 3:
            print(f"  ... and {len(errors) - 3} more errors\n")
        print("Use the debugger to find the off-by-one error in")
        print("chunk_with_overlap_buggy() and fix it.")
        print("\nHINT: Set a breakpoint on the 'position = ...' line")
        print("and watch how position advances vs where the next chunk starts.")
    else:
        print("All chunks are correct! The overlap matches perfectly.")
        print("Bug has been fixed.")


def run_strategy_demo(strategy_name):
    """Run a specific chunking strategy for debugging practice."""
    from chunking_strategies import get_all_strategies

    strategies = get_all_strategies()
    if strategy_name not in strategies:
        print(f"Unknown strategy: {strategy_name}")
        print(f"Available: {', '.join(strategies.keys())}")
        sys.exit(1)

    chunk_fn = strategies[strategy_name]
    print(f"Running strategy: {strategy_name}")
    print(f"Text length: {len(SAMPLE_TEXT)}")
    print()

    try:
        chunks = chunk_fn(SAMPLE_TEXT)
        print(f"Produced {len(chunks)} chunks:")
        for i, chunk in enumerate(chunks[:5]):
            preview = chunk[:60] if isinstance(chunk, str) else str(chunk)[:60]
            print(f"  [{i}] ({len(str(chunk))} chars) {preview}...")
    except NotImplementedError as e:
        print(f"Strategy not yet implemented: {e}")
        print("Implement it in chunking_strategies.py first!")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != "debug":
        run_strategy_demo(sys.argv[1])
    else:
        run_debug_target()
