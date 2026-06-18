# Tutorial 04 — Code Debugging in Python (VSCode)

## What you'll build

Debugging fluency: you'll set up VSCode's Python debugger, run Tutorial 03's
chunking code under it, and systematically inspect objects to understand how
data transforms at each step.

## Why it matters

Reading code tells you what *should* happen. Debugging tells you what *actually*
happens. When a chunking strategy produces wrong output, print-debugging is
slow. A proper debugger lets you freeze execution, inspect every variable, and
step through logic line by line.

## Prerequisites

- VSCode with the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) installed
- Tutorial 03's code (specifically `chunking_strategies.py`)
- A generated PDF converted to Markdown (from Tutorial 03)

## Setup

The `.vscode/launch.json` in this folder provides pre-configured debug
configurations. Copy it to your workspace root if needed:

```bash
cp tutorials/04-debugging/.vscode/launch.json .vscode/launch.json
```

## Exercises

Work through these in order. Each builds on the previous.

### Exercise 1 — Set a Breakpoint and Inspect Locals

1. Open `tutorials/03-chunking-strategies/chunking_strategies.py`
2. Set a breakpoint on the first line inside `chunk_fixed_char()`
3. Run the debugger (F5) using the "Debug: chunk_fixed_char" configuration
4. When execution pauses:
   - Inspect the `text` variable in the Variables panel — how long is it?
   - Check `chunk_size` and `overlap` values
   - Look at the Call Stack panel — what called this function?

**Record in `findings.md`**: The text length, and what the call stack shows.

### Exercise 2 — Step In, Step Over, Step Out

1. Set a breakpoint at the start of `chunk_recursive()`
2. Run with the "Debug: chunk_recursive" configuration
3. Practice:
   - **Step Over (F10)**: Execute the current line without entering functions
   - **Step Into (F11)**: Enter the function call on the current line
   - **Step Out (Shift+F11)**: Finish the current function and return to caller
4. Step into the recursive call — observe how the separator list shrinks

**Record**: How many times does the function recurse for a 2000-char text?

### Exercise 3 — Watch Expressions and Conditional Breakpoints

1. Add a **Watch expression**: `len(chunks)` while inside `chunk_fixed_char()`
2. Set a **Conditional Breakpoint** on the line that appends to the chunks list:
   - Right-click the breakpoint → "Edit Breakpoint" → Condition: `len(chunks) > 5`
3. Run — execution will only pause after the 6th chunk is created
4. Inspect the chunks list — are the overlaps correct?

**Record**: The content of `chunks[4]` and `chunks[5]` — do they overlap correctly?

### Exercise 4 — Find and Fix a Bug

`debug_target.py` in this folder has an intentional bug in a chunking function.
The function is supposed to split text with overlap, but it produces gaps
(missing characters between chunks).

1. Run `debug_target.py` — it will print "BUG: chunks have gaps!" and show where
2. Set a breakpoint inside the buggy function
3. Step through the loop, watching `position` and the slice boundaries
4. Find the off-by-one error and fix it
5. Run again — it should print "All chunks are correct!"

**Record**: What was the bug? What line was it on? How did you fix it?

### Exercise 5 — Inspect Complex Objects

1. Set a breakpoint inside `pdf_to_markdown()` (from Tutorial 03) after `blocks`
   is populated
2. Run with the "Debug: pdf_to_markdown" configuration
3. In the Variables panel, expand the `blocks` list:
   - How many blocks are there?
   - What does a "heading" block look like vs a "table" block?
   - What is the `top` value used for?
4. Use the Debug Console (Ctrl+Shift+Y) to run expressions:
   ```python
   [b["md"][:50] for b in blocks[:5]]
   len([b for b in blocks if b["md"].startswith("#")])
   ```

**Record**: Number of blocks, number of headings, and the first 5 block previews.

## Definition of done

- [ ] You can launch the debugger from VSCode without errors
- [ ] You've completed all 5 exercises
- [ ] `findings.md` is filled in with your observations
- [ ] `debug_target.py` bug is identified and fixed
- [ ] You can explain: breakpoint, step-in, step-out, step-over, watch, conditional breakpoint
