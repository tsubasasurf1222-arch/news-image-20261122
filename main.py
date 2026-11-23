"""news-image-20261122: one picture that sums up the world news of
Sunday 22 November 2026.

The picture is entry.png, sitting next to this file: a 1024x1024 poster
drawn in code with Pillow from the day's reporting. COP31 collapses in
Antalya with no deal; a Russian drone flattens a block near Kyiv; a
Russian warship is hit at Benghazi; Iran strikes near Hormuz; the
Democrats take 258 House seats; the SEC probes Nvidia; BepiColombo
reaches Mercury. This script checks the picture against the contest
gate — a whole PNG or JPEG, no more than 1 MiB, no side over 1024 —
then copies it to the output directory, as the kit's starter does.
It uses only the standard library, and its output never varies.

Try it outside the grading container with MAKEFUN_OUTPUT_DIR set
to a scratch folder:
    MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os, struct

HERE = os.path.dirname(os.path.abspath(__file__))
ENTRY = os.path.join(HERE, "entry.png")
DEST = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

MAX_BYTES = 1048576  # the gate caps the image at 1 MiB
MAX_SIDE = 1024  # and at 1024 pixels on a side

PNG_SIG = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
JPG_SIG = bytes([0xFF, 0xD8, 0xFF])
PNG_TAIL = bytes([0, 0, 0, 0]) + b"IEND" + bytes([0xAE, 0x42, 0x60, 0x82])


def check(blob):
    """Return a reason the image fails the gate, or an empty string."""
    if len(blob) > MAX_BYTES:
        return "entry.png is %d bytes, over the 1 MiB cap" % len(blob)
    if blob[:8] == PNG_SIG:
        if blob[-12:] != PNG_TAIL:
            return "entry.png is a PNG cut short: no IEND chunk at the end"
        wide, high = struct.unpack(">II", blob[16:24])
        if wide > MAX_SIDE or high > MAX_SIDE:
            return "entry.png is %dx%d, over the 1024x1024 cap" % (wide, high)
        return ""
    if blob[:3] == JPG_SIG:
        return ""
    return "entry.png is not a PNG or a JPEG"


def run():
    with open(ENTRY, "rb") as handle:
        blob = handle.read()
    problem = check(blob)
    if problem:
        raise RuntimeError(problem)
    os.makedirs(DEST, exist_ok=True)
    with open(os.path.join(DEST, "entry.png"), "wb") as handle:
        handle.write(blob)
    with open(os.path.join(DEST, "entry.png"), "rb") as handle:
        if handle.read() != blob:
            raise RuntimeError("the copied entry.png does not match the source")


__name__ == "__main__" and run()
