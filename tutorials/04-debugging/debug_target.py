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
    """Retrieval-augmented generation systems depend heavily on how source documents are split into chunks before being embedded and indexed.

A chunking strategy that ignores natural document structure can fracture sentences mid-thought, which degrades retrieval quality. This is why recursive splitting tries multiple separators in order of preference, falling back only when the larger units are still too big.

The recursive approach first tries to split on paragraph breaks. If a paragraph is still too large for the target chunk size, it falls back to splitting on single newlines. Should that still not be enough, it tries splitting on sentence boundaries marked by a period followed by a space.

Only as a last resort does the algorithm fall back to splitting on whitespace between words, and if even that fails to produce small enough pieces, it resorts to a hard character-level cut with no regard for word boundaries at all. Each fallback represents a loss of semantic coherence in exchange for guaranteeing the chunk size constraint is respected.

Consider a single sentence so long that no whitespace appears within a reasonable distance such as a dense run of numbers or an unbroken identifier string the splitter has no safe place to cut and must fall through every separator tier before reaching the final character level fallback which simply slices the text into fixed size windows regardless of meaning. The final paragraph in this sample exists purely to pad the overall length toward two thousand characters so that a chunk size of three hundred forces multiple levels of recursion to occur, giving the debugger something substantial to step through across several separator tiers. A few extra sentences are added here at the end simply to reach the target length without changing the structural shape of the document, since paragraph and sentence boundaries are what actually drive the recursive splitting behavior under inspection. This sentence repeats with minor variation purely to extend the document toward the target length while preserving normal sentence boundaries for the splitter to find. This sentence repeats with minor variation purely to extend the document toward the target length while preserving normal sentence boun"""

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
        position = position + (chunk_size - overlap)

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
