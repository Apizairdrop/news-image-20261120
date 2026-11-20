#!/usr/bin/env python3
"""Entrypoint for the news-image-20261120 entry (Python 3.13, stdlib only).

The front page is drawn at build time by render.py and committed here as
entry.png. The grader runs this program twice, offline, and both runs must
produce identical bytes, so this does the one deterministic thing it can:
copy entry.png into the output directory named by MAKEFUN_OUTPUT_DIR
(default /output). It draws nothing and reads no clock or network.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    src = HERE / "entry.png"
    if not src.is_file():
        raise SystemExit(f"entry.png missing next to {__file__}")
    shutil.copyfile(src, out_dir / "entry.png")


if __name__ == "__main__":
    main()
