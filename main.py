#!/usr/bin/env python3
"""Entry point for the news-image-20261124 bounty.

Copies the pre-rendered front page (entry.png, committed next to this
file) to the grader's output directory. Standard library only: no
imports beyond os, shutil and sys, so it runs in a bare Python 3.13
container with no network and no third-party packages.
"""
import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("missing entry.png next to main.py", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote %s (%d bytes)" % (dst, os.path.getsize(dst)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
