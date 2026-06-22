# Debugging Findings

Fill this in as you complete the exercises in the README.

## Exercise 1 — Breakpoint and Inspect Locals

- **Text length**: 563
- **chunk_size**: 1000
- **overlap**: 200
- **Call stack** (top to bottom):
  1. chunk_fixed_char
  2. run_strategy_demo
  3. <module> 

## Exercise 2 — Step In / Step Over / Step Out

- **Number of recursive calls** for a 2000-char text with chunk_size=300: 5
- **Separator sequence observed**: '\n\n' -> '\n' -> '. ' -> ' '
- **What happens when no separator works?**: ___

## Exercise 3 — Watch Expressions and Conditional Breakpoints

- **Content of chunks[4]** (first 50 chars): uaranteeing the chunk size constraint is respected
- **Content of chunks[4]** (last 50 chars): must fall through every separator tier before reac
- **Content of chunks[5]** (first 50 chars): must fall through every separator tier before reac
- **Do they overlap correctly?** (yes/no): yes
- **Overlap content**: must fall through every separator tier before reac

## Exercise 4 — Find and Fix the Bug

- **File**: debug_target.py
- **Line number**:55
- **The bug**: position = position + (chunk_size - overlap + 1)
- **The fix**: position = position + (chunk_size - overlap)
- **Why it caused gaps**: each iteration position advanced one character too far.so the overlap between the chunks is 19 instead of 20, leaving the one-character gap.

## Exercise 5 — Inspect Complex Objects

- **Number of blocks in `blocks` list**: 132
- **Number of heading blocks**: 64
- **First 5 block previews**:
  1. # Embeddings and Large Language Models
  2. ## A Comprehensive Introduction to Modern NLP
  3. From Word Vectors to Generative Pre-trained Transformers Part I: Embeddings (Chapters 1-4) Part II: Large Language Models (Chapters 5-8)'
  4. # Chapter 1: What Are Embeddings?
  5. ## 1.1 Definition and Motivation
- **What is `top` used for?**: stores the vertical position (y-coordinate) of each block on the page, used to sort all blocks from top to bottom into correct reading order.
