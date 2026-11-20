#!/usr/bin/env python3
"""Copy the pre-rendered front page to the grader's output directory.

The entry image is rendered at build time by render.py and committed as
entry.png beside this file. The grader runs this program twice with no
network, and both runs must write the same bytes, so this only copies the
file instead of drawing anything at grade time.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", out_dir / "entry.png")


if __name__ == "__main__":
    main()
