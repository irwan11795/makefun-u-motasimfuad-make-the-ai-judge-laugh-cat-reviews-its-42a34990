#!/usr/bin/env python3
"""Cat Reviews Its Human — a one-star review, written by the cat.

Writes a single-line entry (1-200 chars, no trailing newline) to
/output/entry.txt, with fallback chain:
  MAKEFUN_OUTPUT_DIR -> /output -> output/ in repo -> temp dir
"""

import os
import sys
import tempfile

# Entry built additively from two literals (thinking_revised).
ENTRY_PART1 = "One star. He moved my food bowl two inches left. "
ENTRY_PART2 = "I have not forgiven him. I never will."
ENTRY = ENTRY_PART1 + ENTRY_PART2


def resolve_output_dir():
    """Return the first usable output directory in the fallback chain."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    if os.path.isdir("/output"):
        return "/output"
    repo_out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    try:
        os.makedirs(repo_out, exist_ok=True)
        return repo_out
    except OSError:
        return tempfile.mkdtemp(prefix="cat-reviews-")


def validate(text):
    """Gate: 1-200 chars, single line, not whitespace-only."""
    if not isinstance(text, str):
        return False
    if len(text) < 1 or len(text) > 200:
        return False
    if "\n" in text or "\r" in text:
        return False
    if not text.strip():
        return False
    return True


def main():
    entry = ENTRY
    if not validate(entry):
        print("ERROR: entry failed validation", file=sys.stderr)
        sys.exit(1)
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(entry)
    print(f"Wrote {len(entry)} chars to {path}")


if __name__ == "__main__":
    main()
