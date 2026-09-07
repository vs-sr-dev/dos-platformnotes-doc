# MS-DOS-era platform notes — a checklist assembled from a sweep

A running checklist for the **DOS-era subset** of the PC family, to be carried
from one pipeline to the next and added to by each.

**It was not written out of an object.** The CD-i and Amiga CD checklists in
this collection were written out of their first pipeline; the Dreamcast one was
written before its first pipeline. This one was written out of **forty-nine
finished PC repositories at once and out of none of them individually**, which
is why it has no `[unverified]` marks and no scaffolding: every item below
carries a count, the count names the repositories it came from, and
`tools/sweep.py` reprints it.

---

## What this does not contradict, and why it had to say so first

[pc-gamelist-doc](https://github.com/vs-sr-dev/pc-gamelist-doc) states the
family's position in its second paragraph, and it is a decision rather than an
omission:

> *"This family has no shared platform checklist: a DOS game from 1987 and a
> PhyreEngine remaster from 2018 have almost nothing in common except the
> machine they end up on, which is exactly why the index is per platform and
> not per engine."*

**That is correct about the family and this document does not touch it.** A 1987
DOS game and a 2018 PhyreEngine remaster still have almost nothing in common,
and there is still no PC platform checklist. What the family decision does not
answer is the narrower question — whether the *DOS-era subset* has enough in
common — and that question is answerable by counting rather than by opinion:

```
python tools/sweep.py
repositories swept: 49  (../pc-* with a docs/, index excluded)

an MZ header field                       25 of 49
a DOS-era packer                         16 of 49
```

**Twenty-five repositories have independently done MZ header arithmetic and
sixteen have independently met a DOS-era packer.** That is half the family and a
third of it, and it is the whole justification for this file existing. The
argument was first made in
[pc-kingsofthebeach-doc/docs/14](https://github.com/vs-sr-dev/pc-kingsofthebeach-doc/blob/master/docs/14-against-the-collection.md),
which concluded that the checklist was worth writing and **declined to write
it**, because writing a family document on the strength of one object is the
error the pipeline exists to avoid. This file is the sweep that chapter asked
for.

## The name, and the index this repository belongs to

`dos-platformnotes-doc` follows the `<family>-platformnotes-doc` shape used by
[cd32](https://github.com/vs-sr-dev/cd32-platformnotes-doc),
[cdi](https://github.com/vs-sr-dev/cdi-platformnotes-doc),
[3do](https://github.com/vs-sr-dev/3do-platformnotes-doc),
[dc](https://github.com/vs-sr-dev/dc-platformnotes-doc) and
[vis](https://github.com/vs-sr-dev/vis-platformnotes-doc), because a reader who
knows five of those should not have to learn a sixth naming scheme. **`dos` is
not a family here**, though, and the difference matters: there is no
`dos-gamelist-doc` and there will not be one, because the titles are already
indexed by the machine they run on.

So the primary index of this repository is
**[pc-gamelist-doc](https://github.com/vs-sr-dev/pc-gamelist-doc)**, not the
profile README. Every repository has one primary index and any number of
crosslinks; the profile README's platform-notes slot is for a document that
covers a whole family, and putting a subset document in it would assert exactly
what the paragraph above denies. Reachability is unaffected — `pc-gamelist-doc`
is on the profile README and links here.

## How to read the marks

There are no `[unverified]` marks. Instead:

| mark | meaning |
|---|---|
| `[n of 49]` | *n* PC repositories with a `docs/` on the sweeping machine mention it; `tools/sweep.py` counts repositories, not mentions |
| `[n objects]` | *n* objects actually exercised it, named individually |
| `[1 object]` | **one** object supports this and nobody else has met it yet |

`[n of 49]` is weaker than `[n objects]`: mentioning a term is not doing the
work. Where both are available both are given. The denominator is the machine's,
not the family's — `pc-gamelist-doc` lists **58** titles and the remote holds
more `pc-*` repositories than either number. `tools/sweep.py` prints the
denominator it used, and a figure quoted without one is not a figure.

---

## 1. The tool you have is not the tool you remember `[5 objects]`

Five repositories ship `tools/exepack.py`. **All five files are different**, and
they are different in ways that change the answer:

```
python tools/sweep.py --tools

tool           copies  distinct
mzcensus.py        28         2
exepack.py          5         5
mz.py               6         2
dosimage.py         2         1
cga.py              2         1
```

| copy | lines | how it writes the image | restores the verbatim head | tests relocation targets |
|---|---:|---|:--:|:--:|
| `pc-heroquest-doc` | 143 | `exepack.py FILE -o OUT`, hand-parsed from `sys.argv` | no | no |
| `pc-megaman-doc` | 240 | `exepack.py FILE --out OUT` (and `--exe` to rebuild an MZ) | no | locates the table only |
| `pc-megaman3-doc` | 245 | `exepack.py FILE --out OUT` (and `--exe`) | no | locates the table only |
| `pc-popcorn-doc` | 326 | `exepack.py --unpack OUT FILE`, argparse (and `--refuse`) | no | no |
| `pc-kingsofthebeach-doc` | 422 | `exepack.py --unpack OUT FILE`, argparse (and `--refuse`) | **yes** | **yes** |

**The instruction is not "`exepack.py` has a `--unpack` flag".** Two of the five
copies have one; two take `--out`; one takes `-o`. And in the two that do have
it, **the flag's own docstring gets the argument order wrong**: it reads
`--unpack FILE OUT`, while the `argparse` block eight lines below takes the
output path as the flag's *value* and the input as a positional, so the working
invocation is `--unpack OUT FILE`. The usage line is a comment; the parser is
the tool.

So the instruction is: *the toolbox is copied wholesale between repositories and
the copies drift, so run the copy in front of you with `--help` and read what it
parses before asserting what it can or cannot do.* Two of the five also ship a
`--refuse` flag, which is section 4's discipline built into the tool — it
asserts that none of its inputs is EXEPACK and exits 1 if one is.

A pre-briefing asserted three times that this tool had no unpack flag, and the
session lost a prediction to that claim in three minutes
([pc-kingsofthebeach-doc/docs/04](https://github.com/vs-sr-dev/pc-kingsofthebeach-doc/blob/master/docs/04-the-programs.md)).
A toolbox does not tell you what its tools can do, and neither does a briefing.

**The contrast is the useful half.** `mzcensus.py` has 28 copies and **two**
distinct versions; `exepack.py` has five copies and **five**. The stable tool is
the one nobody had to fix. A tool with as many versions as copies is a tool
whose output you check before you quote it.

## 2. The declared image is not the file `[25 of 49]` `[28 copies of one tool]`

An MZ header states its own load-image length in two fields, and the arithmetic
has a special case that is wrong by 512 bytes if you miss it:

```
img = (e_cp - 1) * 512 + e_cblp        when e_cblp != 0
img = e_cp * 512                       when e_cblp == 0
```

All **28** copies of `mzcensus.py` state that rule, in both of its two distinct
versions. `e_cblp == 0` does not mean an empty last page; it means a **full**
one.

**Anything between `img` and the file size is data appended after the image**,
which DOS loads for nobody — the program reads it back itself. Four
repositories report that quantity as a named row (`overlay past image`), and
three of them report **0** on every executable they have, which is what would
make a non-zero one interesting:
[pc-baronbaldric-doc/docs/05](https://github.com/vs-sr-dev/pc-baronbaldric-doc/blob/main/docs/05-executables-and-the-boot-chain.md)
(0 on four executables),
[pc-heroquest-doc/docs/04](https://github.com/vs-sr-dev/pc-heroquest-doc/blob/main/docs/04-executables.md)
(0 on three), `pc-mystictowers-doc`, and `pc-kingsofthebeach-doc`, whose main
program holds under a third of its own code with the rest in separate overlay
files.

Two consequences worth carrying:

1. **`e_cblp` is the file length modulo 512 and nothing else.** A briefing read
   `4d 5a 50 00` as the Borland `MZP` marker; the file is 4,176 bytes, 4176 mod
   512 is 80, and 80 is `P`
   ([pc-1000miglia-doc/docs/10](https://github.com/vs-sr-dev/pc-1000miglia-doc/blob/master/docs/10-turbo-pascal-six.md)).
   The column proves it for every executable at once rather than one at a time.
2. **`e_crlc == 0` on a program of any size is a packer**, not a program with no
   fixups. A Turbo Pascal program has hundreds; a packed image declares none,
   because the packer's stub applies them itself.

## 3. After unpacking, the relocation table is the only content check `[5 objects, the defect on 1]`

**Length arithmetic cannot see a hole.** EXEPACK relocates the packed data to
the *top* of the destination buffer and unpacks downwards, so the leading part
of the load image is left verbatim at the bottom of the packed region and is
never overwritten. A decompressor that does not copy it back produces a buffer
that is **exactly `dest_len` bytes long** and wrong.

On *Kings of the Beach* the hole was **11,184 bytes on both overlays** —
identical on two different programs, which is what gave it away — and the bytes
that belong there are 8086 code beginning `2B C0 50 E8 FE 01 83 C4 02 C3 55 8B
EC 83 EC 0C`, a Microsoft C module prologue
([docs/04](https://github.com/vs-sr-dev/pc-kingsofthebeach-doc/blob/master/docs/04-the-programs.md),
correction in
[docs/17](https://github.com/vs-sr-dev/pc-kingsofthebeach-doc/blob/master/docs/17-corrections.md)).

The check that caught it was the packer's own relocation table:

```
relocation targets      : 99, 0 outside the image, 0 above segment 16813,
                          10 holding 0000 (legal: the load base)
targets inside the head : 8, of which 8 are non-zero -- they read 0000
                          before the head was restored
relocation check        : PASSES, 99 of 99 addressable
```

**The criterion is addressability, not non-zero.** The first version of that
check treated a stored segment of `0x0000` as impossible and failed both files.
It is not impossible: `0x0000` is the program's own load base, and ten entries
in each file hold it legitimately.

Three instructions:

- parse the sixteen relocation groups after the `Packed file is corrupt` message
  and test **every** target against the unpacked image;
- if the decompressor reports *destination bytes never written at the head* and
  *packed bytes left unread* and the two are **equal and non-zero**, the image
  has a hole of that size at offset 0, and the bytes that belong there are the
  first *N* of the packed region, at file offset `e_cparhdr × 16`;
- any string offset, needle count or entropy figure quoted from an image
  unpacked with a copy that does not restore the head is computed over a buffer
  with a zero hole in it, and needle **counts** are only ever too low.

`[1 object]` **on the defect itself.** Thirteen repositories mention EXEPACK,
sixteen meet a DOS-era packer, and exactly one has been through this. Whether
the other four `exepack.py` copies produce a hole on their own objects depends
on where each packer stopped, and **this document cannot say** — the table in
section 1 says only that four of the five do not restore the head. Run the
check.

## 4. A reader that refuses is worth more than a reader that answers `[5 objects, 3 families]` `[8 of 107]`

The failure, in one sentence: **a reader that does not recognise its input can
print a complete, confident, correctly formatted summary table computed over a
population of zero, and exit 0.**

| object | tool | what it printed |
|---|---|---|
| [vis-thesecretsofhoseafreeman-doc/docs/04](https://github.com/vs-sr-dev/vis-thesecretsofhoseafreeman-doc/blob/master/docs/04-the-anim-format.md) | `avicheck.py` | `VID001.VID  NOT AN AVI`, then a complete table of zeroes ending `files where the two disagree : 0 of 1` and `frames, header-declared 0 / frames counted 0  AGREE` |
| [pc-kingsofthebeach-doc/docs/05](https://github.com/vs-sr-dev/pc-kingsofthebeach-doc/blob/master/docs/05-pak.md) | `pakraster.py` | a full summary over zero inputs, ending `direct-colour backgrounds examined : 0` |
| [pc-samandmaxseasonone-doc/docs/16](https://github.com/vs-sr-dev/pc-samandmaxseasonone-doc/blob/master/docs/16-corrections.md) | a packer scanner | filtered on executable extensions, matched none of the `.bin` blobs, printed a clean table of zeros; with `--all-files` it fires in 5 of 5 and the trail leads to SecuROM |
| [pc-linksthechallengeofgolf-doc/docs/02](https://github.com/vs-sr-dev/pc-linksthechallengeofgolf-doc/blob/master/docs/02-the-technical-sheet.md) | the same scanner | opened 7 of 32 files and still printed a full table of zeroes |
| [dc-sonicadventure-doc/docs/17](https://github.com/vs-sr-dev/dc-sonicadventure-doc/blob/master/docs/17-corrections.md) | `iso9660.py` | `files : 0` on a GD-ROM, **exit status 0** |

Three of the five are PC objects and two are not, which is why this item is
stated for the toolbox rather than for DOS: it is not a DOS defect, it is what
happens when a reader written for one format is pointed at another. The DOS-era
half is that these objects are small enough that a wrong answer is cheap to
believe — there is no size cue to make an empty result look implausible.

**Three instructions:**

- **run every candidate reader for its refusal first**, on an input you know it
  should reject, before you run it on the input you care about;
- **read the population size, not the exit code.** `0 of 0  AGREE` is not
  agreement;
- **make the reader raise.** `iso9660.py`'s fix was a control that raises when a
  non-empty root yields no entries — a tool that cannot answer should say so in
  its exit code, and until it does, the population line is the only guard.

## 5. DOS timestamps have two-second granularity, so an all-even distribution is not an observation `[22 of 49]`

FAT stores a file time in a 16-bit field with five bits of seconds, counting in
units of two. **Every DOS timestamp is even, and the evenness carries no
information about the object.** Twenty-two repositories have touched this, and
it ran as a numbered open question across several sessions before closing.

```
python tools/clockwork.py "1000 Miglia"
odd second values     : 0 of 124
distinct second values: 30 of the 30 even ones
```

Both halves are settled now, and the negative half is the one that makes the
rule usable:

- **positive** — on an object whose dates are bytes rather than filesystem
  metadata, 99 % even seconds means *the files reached this medium from a PC*.
  On a Macintosh-mastered hybrid the evenness survives because ISO 9660 has a
  whole byte for seconds and copied a number that only ever had half of one; 27
  of 2,879 records have an odd seconds field, and they concentrate in the
  directories that also carry impossible dates
  ([pc-clic0297-doc/docs/07](https://github.com/vs-sr-dev/pc-clic0297-doc/blob/master/docs/07-clocks.md));
- **negative** — NTFS has no such granularity. On a downloaded modern object the
  split was **138 even to 143 odd**, all sixty values present
  ([pc-allodsonline-doc](https://github.com/vs-sr-dev/pc-allodsonline-doc)).

So: **quote the even/odd split before drawing anything from a second value**,
and say which filesystem the timestamps came off. An all-even set of DOS mtimes
is one fact about FAT, not *n* facts about the object.

The companion trap is the opposite one. A set of mtimes that agree to the second
across every file is **one copy operation recorded n times, not n observations**
— fourteen files carrying one identical stamp is a single event
([pc-leathergoddessesofphobos-doc](https://github.com/vs-sr-dev/pc-leathergoddessesofphobos-doc))
— and an installer or a storefront that rewrites every mtime into a six-minute
window leaves a filesystem that dates the *download* and nothing else.

## 6. State the chance rate before quoting the count, and say which way it runs `[4 of 49]`

A needle count means nothing without the rate at which that needle occurs by
accident in a population of that size, and **the rate has to be declared before
the count is quoted**, or it will be chosen to fit it.

```
positions examined : 194828
0xBFF70000-0xBFF80000  KERNEL32.DLL base on Win9x   4229  expected 3.0   x1423
0xBFF00000-0xBFFFFFFF  rest of the Win9x arena      5272  expected 47.6  x111
```
([pc-canediterracotta-doc/docs/10](https://github.com/vs-sr-dev/pc-canediterracotta-doc/blob/master/docs/10-kernel32.md))

**On a DOS object the arithmetic inverts, and that is the part specific to the
era.** A DOS object is 10³ to 10⁵ times smaller than an optical one: a four-byte
needle in 524,839 bytes has a chance rate of 0.0000 — one expected occurrence
per 4,294,967,296 bytes — so **a single four-byte hit is a finding**, where the
same hit on a seven-gigabyte install is noise. The inversion is `[1 object]`;
the discipline is `[4 of 49]`, and four of forty-nine is the honest statement
that this is the exception rather than the habit.

The other objects that state a rate before a count:
[pc-megaman-doc/docs/07](https://github.com/vs-sr-dev/pc-megaman-doc/blob/master/docs/07-blk-the-tile-banks.md)
(322 or 323 of 328 record boundaries land on a token boundary, against roughly
24 expected by chance) and
[pc-skunnybacktotheforest-doc/docs/13](https://github.com/vs-sr-dev/pc-skunnybacktotheforest-doc/blob/master/docs/13-leftovers.md)
(3.1 % against a chance rate of 1/56 = 1.8 %, which is the useful case of a rate
that makes a result *weaker*).

---

## What is deliberately not in this document

**Nothing about content, and nothing about graphics.** The sweep is the reason:

```
EGA                                      11 of 49
planar graphics                          13 of 49
CGA                                       7 of 49
INT 10h                                   8 of 49
```

Those look like a quorum and are not one. The formats behind them are **per
title**, and they were derived from the bytes in every repository that met them,
because there is nothing to inherit: an EGA image in one object is
row-interleaved four-plane behind a run-length stream, and in the next it is
something else. A checklist entry for `.PAK` would be actively wrong — in this
collection `.PAK` already means **three unrelated formats**.

The line is: **this document is about executables and tool discipline.** If an
item would have to name a game format, it does not belong here; it belongs in
the repository for the title that has it.

The EGA and CGA figures also correct the counts in
`pc-kingsofthebeach-doc/docs/14`, which read 17 and 9. That sweep matched `EGA`
and `CGA` as bare substrings, so `MEGA` and `OMEGA` counted; `tools/sweep.py`
matches them on word boundaries. The two figures that carried the decision — 25
and 16 — are unaffected.

## The sweep, and how to re-run it

```
python tools/sweep.py                     # the term table above
python tools/sweep.py --tools             # copies and distinct versions
python tools/sweep.py --list EXEPACK      # which repositories a term hits
python tools/sweep.py --pattern '*'       # the whole collection, 107 repositories
```

It counts **repositories, not mentions**: a chapter that names EXEPACK forty
times counts once. It excludes any `*gamelist-doc`, because an index quoting its
titles' findings would count them twice. And it refuses to print a table when
the population is empty, which is section 4 applied to itself.

## Open questions

**Q1 — do the other four `exepack.py` copies have the hole?** Section 3's defect
is `[1 object]`. Four repositories hold a copy that does not restore the
verbatim head, and whether their unpacked images actually have a hole depends on
where each packer stopped. **What would close it:** re-running the corrected
copy against the four objects and comparing.

**Q2 — is `[n of 49]` measuring the family or the machine?** The denominator is
repositories present where the sweep runs. `pc-gamelist-doc` lists 58 titles and
the remote holds more `pc-*` repositories than that; twelve of the listed titles
have no directory on the machine this sweep ran on. **What would close it:** a
sweep that reads the remote rather than the working copy.

**Q3 — is the packer population representative?** Sixteen of forty-nine met a
DOS-era packer, but the three packers named (EXEPACK, PKLITE, LZEXE) are the
three the toolbox can identify. A fourth would be invisible to this sweep and
would look like an unpacked program with an implausible `e_crlc`. **What would
close it:** an entropy-and-`e_crlc` census over every MZ in the family rather
than a name search.

**Q4 — how many of the twenty-eight `mzcensus.py` copies were ever run?**
Shipping a tool is not running it, and this document counts files on disk. The
distinction matters most for section 2, whose `[25 of 49]` is a mention count.
**What would close it:** the `toolclass.py` "inherited, applicable, not needed"
tables, which several repositories already publish.
