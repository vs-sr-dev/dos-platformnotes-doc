#!/usr/bin/env python3
"""sweep.py -- count what the PC repositories have already done, one term per row.

Every figure in `dos-platform-notes.md` comes from this script. It reads the
`docs/` of sibling repositories and counts *repositories*, never mentions:
a document that names EXEPACK forty times counts once.

    python tools/sweep.py                  # terms, against ../pc-*
    python tools/sweep.py --root ..        # explicit collection root
    python tools/sweep.py --tools          # the shared-toolbox measurements
    python tools/sweep.py --list EXEPACK   # which repositories a term hits

The denominator is repositories that exist on the machine the sweep runs on,
which is not the whole family: `pc-gamelist-doc` lists more titles than there
are directories here, and the remote holds more `pc-*` repositories still. The
script prints the denominator it used, and a figure quoted without it is not a
figure.
"""
import argparse
import glob
import hashlib
import os
import re
import sys

TERMS = [
    ("MS-DOS",                              r"MS-DOS"),
    ("MZ",                                  r"\bMZ\b"),
    ("an MZ header field",                  r"e_cblp|e_lfanew|e_cparhdr|e_crlc|MZ header"),
    ("a DOS-era packer",                    r"EXEPACK|PKLITE|LZEXE"),
    ("EXEPACK",                             r"EXEPACK"),
    ("a relocation table",                  r"relocation table|relocation entr|reloc table"),
    ("bytes past the declared image",       r"past (the )?image|beyond the load image|overlay past"),
    ("DOS two-second timestamps",           r"even[- ]second|odd[- ]second|two-second granularit"),
    ("a reader that answered over nothing", r"exited 0|exit code 0|exit status 0|population of zero|over an empty|table of zero"),
    ("a chance rate stated",                r"chance rate|expected by chance"),
    ("EGA",                                 r"\bEGA\b"),
    ("planar graphics",                     r"planar"),
    ("CGA",                                 r"\bCGA\b"),
    ("INT 10h",                             r"INT\s*10h"),
]

TOOLS = ["mzcensus.py", "exepack.py", "mz.py", "dosimage.py", "cga.py"]


def repos(root, pattern):
    out = []
    for d in sorted(glob.glob(os.path.join(root, pattern))):
        if os.path.isdir(os.path.join(d, "docs")) and not d.endswith("gamelist-doc"):
            out.append(d)
    return out


def hits(repo, rx):
    for f in sorted(glob.glob(os.path.join(repo, "docs", "*.md"))):
        with open(f, encoding="utf-8", errors="replace") as fh:
            if rx.search(fh.read()):
                return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="..")
    ap.add_argument("--pattern", default="pc-*")
    ap.add_argument("--tools", action="store_true")
    ap.add_argument("--list", metavar="TERM")
    a = ap.parse_args()

    rs = repos(a.root, a.pattern)
    if not rs:
        sys.exit("no repositories with a docs/ under %s/%s -- refusing to print "
                 "a table over an empty population" % (a.root, a.pattern))
    print("repositories swept: %d  (%s/%s with a docs/, index excluded)"
          % (len(rs), a.root, a.pattern))

    if a.list:
        rx = re.compile(dict(TERMS).get(a.list, a.list), re.I)
        got = [os.path.basename(r) for r in rs if hits(r, rx)]
        print("%s: %d of %d" % (a.list, len(got), len(rs)))
        for g in got:
            print("  " + g)
        return 0

    if a.tools:
        print("\n%-14s %6s %9s %s" % ("tool", "copies", "distinct", "repositories"))
        for t in TOOLS:
            found = [r for r in rs if os.path.isfile(os.path.join(r, "tools", t))]
            digests = set()
            for r in found:
                with open(os.path.join(r, "tools", t), "rb") as fh:
                    digests.add(hashlib.sha1(fh.read()).hexdigest())
            print("%-14s %6d %9d %s"
                  % (t, len(found), len(digests),
                     ", ".join(os.path.basename(r) for r in found[:6])
                     + (" ..." if len(found) > 6 else "")))
        return 0

    print("\n%-38s %s" % ("what a repository's chapters mention", "repositories"))
    for name, pat in TERMS:
        rx = re.compile(pat, 0 if name in ("MZ", "EGA", "CGA") else re.I)
        n = sum(1 for r in rs if hits(r, rx))
        print("%-38s %3d of %d" % (name, n, len(rs)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
