#!/usr/bin/env python3
"""Copy the generated letter image into the make.fun output directory.

Stdlib only (os, shutil): the grading sandbox runs this with no network and
no third-party packages, so the image itself (letter.png) must already live
in this repo.
"""
import os
import shutil

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(REPO_DIR, "letter.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(OUT_DIR, "entry.png")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, DST)
    src_size = os.path.getsize(SRC)
    dst_size = os.path.getsize(DST)
    identical = open(SRC, "rb").read() == open(DST, "rb").read()
    print(f"Copied {SRC} -> {DST}")
    print(f"Byte size: {dst_size}")
    print(f"Byte-identical to letter.png: {identical}")


if __name__ == "__main__":
    main()
