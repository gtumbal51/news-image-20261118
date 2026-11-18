#!/usr/bin/env python3
"""Copy entry.png to the output directory and verify the copy.

Reads MAKEFUN_OUTPUT_DIR (default /output) and writes entry.png there.
After copying, it verifies the destination: the file exists, its size
matches the source, and its first 8 bytes are the PNG signature.
Uses only the Python standard library. Deterministic: a byte-for-byte copy.
"""

import os
import shutil
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print("error:", message, file=sys.stderr)
    return 1


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    dst = os.path.join(outdir, "entry.png")
    shutil.copyfile(src, dst)

    # Verify the copy succeeded before reporting success.
    if not os.path.isfile(dst):
        return fail("destination file missing after copy: %s" % dst)
    src_size = os.path.getsize(src)
    dst_size = os.path.getsize(dst)
    if dst_size != src_size:
        return fail(
            "size mismatch: source %d bytes, destination %d bytes"
            % (src_size, dst_size)
        )
    with open(dst, "rb") as f:
        header = f.read(8)
    if header != PNG_SIGNATURE:
        return fail("destination is not a PNG (bad signature): %s" % dst)

    print("wrote %s (%d bytes, PNG verified)" % (dst, dst_size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
