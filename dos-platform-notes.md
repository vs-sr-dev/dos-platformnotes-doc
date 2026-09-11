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
not the family's — `pc-gamelist-doc` lists **61** titles and the remote holds
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

**The first non-zero one has now been measured** `[1 object]`:
[pc-hugoshouseofhorrors-doc/docs/04](https://github.com/vs-sr-dev/pc-hugoshouseofhorrors-doc/blob/master/docs/04-the-executable.md)
reports `overlay past image` **+9** on `HHH.EXE`, 114,419 bytes, against
**0 on ten executables across the three repositories above**. The nine bytes
are `36 15 90 22 ef 90 ef 15 22`; they occur nowhere else on that object, at
nine bytes or at four, against a chance expectation of 0.0002 for a four-byte
needle in 866,684; and **what they are is not identified**. One object is one
object: what this row now says is that the quantity is not always 0, not that
anybody knows what a non-zero value means.

Two consequences worth carrying:

1. **`e_cblp` is the file length modulo 512 and nothing else.** A briefing read
   `4d 5a 50 00` as the Borland `MZP` marker; the file is 4,176 bytes, 4176 mod
   512 is 80, and 80 is `P`
   ([pc-1000miglia-doc/docs/10](https://github.com/vs-sr-dev/pc-1000miglia-doc/blob/master/docs/10-turbo-pascal-six.md)).
   The column proves it for every executable at once rather than one at a time.

   **Amended: it is the LOAD IMAGE modulo 512, and the two are the same number
   only when there is no slack.** `e_cblp` is defined against the image
   `(e_cp - 1) * 512 + e_cblp`, not against the file, so on any executable
   with a payload behind its image the comparison to the file length is
   mechanically wrong and the column reports a `DIFFER` that means nothing. On
   `pc-hexxagon-doc`'s `HEXX01.EXE` — 583,613 bytes of which 567,843 are a ZIP
   sitting behind a 15,770-byte PKLITE'd stub — 15,770 mod 512 is **410**,
   which is `e_cblp` exactly, while the file-length comparison says 445 and
   DIFFERs. **The original wording is right for every unpacked program and
   wrong for every self-extractor**, which is why it survived so long: the
   objects that break it are the ones with something hidden behind the image,
   and those are the objects the column gets quoted about. `mzcensus.py` now
   prints both comparisons — nothing was removed, because repositories quote
   the old column — and the summary counts both
   ([pc-hexxagon-doc/docs/10](https://github.com/vs-sr-dev/pc-hexxagon-doc/blob/master/docs/10-the-tools.md),
   after `pc-rovescino-doc/docs/10` C.3 named the defect and declined to touch
   it).
2. **`e_crlc == 0` on a program of any size is a packer**, not a program with no
   fixups. A Turbo Pascal program has hundreds; a packed image declares none,
   because the packer's stub applies them itself.

   **And the negative control, which three objects of packed binaries never
   supplied `[1 object]`.** A non-zero `e_crlc` is the rule read the other way:
   a program that declares relocations is one whose loader still has fixups to
   apply, which a packer's stub would have consumed. `pc-bianconatale-doc`'s
   `BN.EXE` (BIANCO NATALE, Tecnoart, 1994) is the family's **first unpacked
   DOS executable in three objects** — `e_crlc` **83**, whole-file entropy
   **6.6052** bits/byte where a packed image runs near 8, and `dospack.py`'s
   33-signature sweep finding no packer in the right place, only a `Borland`
   banner. It is a 70 KB Turbo-C binary that nobody packed, and it matters here
   because a rule with only positive cases has never been shown to *not* fire:
   the three objects before it were a bare program with no packer, then PKLITE
   and LZEXE together, then a modern repackaging, and none of them exercised the
   converse. See
   [pc-bianconatale-doc/docs/06](https://github.com/vs-sr-dev/pc-bianconatale-doc/blob/master/docs/06-the-program.md).

   **And the second unpacked one in a row `[1 object]`.** `pc-outrun-doc`'s
   `OUTRUN.EXE` (OUT RUN, SEGA / Unlimited Software Inc., 1989) is Turbo-C,
   `e_crlc` **1**, entropy **5.9987**, no packer — the rule read straight this
   time confirms the converse: its three *sibling* files `CORV/CHEVY/BEETLE.PES`
   declare `e_crlc` **0** and are packed, EXEPACK'd, and the rule fires on them
   correctly ([pc-outrun-doc/docs/03](https://github.com/vs-sr-dev/pc-outrun-doc/blob/master/docs/03-three-cars-that-are-engines.md)).

### 2a. And when `e_lfanew` points at a signature, the arithmetic describes the stub `[2 objects]`

The rule above has a case where it is still correct and no longer *useful*, and
it is worth separating because the same column reports two unrelated
quantities.

**If the `u32` at `0x3C` points inside the file and the bytes there are `NE`,
`LE`, `LX` or `PE\0\0`, the MZ header is describing a stub.** Everything the
`img` arithmetic calls "beyond the declared image" is then the actual program,
not an appendix, and reporting it beside
[pc-hugoshouseofhorrors-doc](https://github.com/vs-sr-dev/pc-hugoshouseofhorrors-doc/blob/master/docs/04-the-executable.md)'s
nine appended bytes puts a whole executable and a nine-byte curiosity under one
heading.

[pc-themepark-doc/docs/09](https://github.com/vs-sr-dev/pc-themepark-doc/blob/master/docs/09-the-programs.md)
`[1 object]` has three files of one game where the quantity reads **+830,805**,
**+168,885** and **+80,340**:

```
python tools/mz.py <GAME/MAIN.EXE>
  pages x 512 + last page    : (21 - 1) * 512 + 178 = 10418
  against the file length    : 841223  residue +830805
  e_lfanew points at 0x28B8, where the signature is b'LE'
```

All three carry the **same byte-identical 10,424-byte stub**, which is what a
Watcom link against DOS/4GW produces, and all three then hold an `LE` linear
executable that accounts for the rest of the file exactly — 661,511, 143,463
and 65,670 bytes of page data, residue **0** on each, read with that
repository's `tools/le.py`. The stub's whole job is to print a message when the
program is run without an extender.

[pc-samandmaxhittheroad-doc](https://github.com/vs-sr-dev/pc-samandmaxhittheroad-doc)
`[+1 object]` has **thirteen** linear executables at the same `0x28B8`, and its
`DOS4GW.EXE` is 254,196 bytes against *Theme Park*'s 265,396 — two versions of
Rational Systems' extender, in two repositories, one diff apart.

**The check is one line and `tools/mz.py` already does it**: it reads `0x3C`,
looks for the four signatures, and names the one it finds. What no copy of
`mzcensus.py` does is suppress or relabel `overlay past image` when that
signature is present, and until one does, the column means two things.

**The prior art is real and this document says so rather than implying the
family had never opened one.** `pc-hurl-doc/tools/hurlle.py` is a working LE
loader — object mapping, `dis`, `xref`, `func`, `strings` — written against one
object; `pc-themepark-doc/tools/le.py` is a second, generic one that cites it.
Two independent implementations in the family is the threshold at which an item
belongs here rather than in a repository.

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

## 4. A reader that refuses is worth more than a reader that answers `[5 objects, 3 families]` `[8 of 107]` `[+2 objects, a filtered denominator]` `[+1 object, an exception in a data column]`

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

**A sixth instance is a different shape and is recorded separately** `[1 object]`.
On [pc-hugoshouseofhorrors-doc/docs/15](https://github.com/vs-sr-dev/pc-hugoshouseofhorrors-doc/blob/master/docs/15-the-tools.md)
the failure was not a table over **zero** but a table over a **filtered
population**: `mzcensus.py` printed `=== the 1 MZ executables ===` on an object
with **three** MZ files, because it globs `*.EXE` and the other two are called
`.FON`; every figure in its table was correct and its denominator was true of
its filter and false of the object. The same run printed
`third-party software in this folder: 0` on an object carrying two Microsoft
font modules. On the same object `bmp.py` and `tga.py` read a valid PCX file
and printed full header reports — `dimensions : -1442840576 x 43520, 170 bpp`
and `75 x 75, 0 bits per pixel` — both exiting 0.

**A population of one looks like an answer in a way a population of zero does
not**, and a report over garbage looks like an answer in a way an empty table
does not. The instruction below — *read the population size, not the exit code*
— is necessary and, on those two, not sufficient: the population size was 1 and
it was printed.

**A seventh and an eighth instance arrive together, on one object, and the
seventh completes the sixth** `[1 object]`.
[pc-finalfantasy7-doc/docs/15](https://github.com/vs-sr-dev/pc-finalfantasy7-doc/blob/master/docs/15-the-tools.md)
is four raw CD images holding 662 files, of which **268 begin `MZ`**.

* **`mzcensus.py` does both things on that one object.** Pointed at the four
  `.bin` images it raises `AssertionError: no .EXE found under '...' -- this
  census has nothing to do` and exits **1**: loud, reasoned, non-zero, correct.
  Pointed at the extracted tree it prints `=== the 26 MZ executables ===`,
  because 26 files are called `.EXE` and the other 242 are called `.DLL`,
  `.DRV`, `.VXD`, `.ACV`, `.CPL`, `.HDI`, `.NEC`, `.X86`, `.MPD`, `.CRL` and
  `.LRC`. **9.7015 % of the population, in a header that names the object.**
  So the defect was never *this tool answers over nothing*: it is **the
  denominator is its filter's and not the object's**, and when the filter is
  empty the assertion catches it and when it is not, nothing does. Both halves
  of one tool, on one tree, in one session.
* **`pecensus.py` prints an exception message in a data column and exits 0.**
  On the same tree, over 267 PE files, every row reads `fmt n/a`, no linker, no
  COFF timestamp, and — in the **CompanyName** column — the truncated string
  `'PE' object has no attribute 'e_lf`. That is a Python `AttributeError`
  formatted as a table cell, 267 times, with exit status 0. It is a worse shape
  than the empty table the same tool printed on the raw images: **an empty
  table says nothing and this one says something false with a column heading
  over it.**

A fourth instruction follows from the pair, and it is about writing rather than
running: **a census must print its filter beside its count.** `26 of 268 files
beginning MZ` would have been true; `the 26 MZ executables` is not. And **a
value a reader could not compute must not be rendered in the column it would
have gone in** — a dash, an empty cell or a refusal, never the reason.

Three of the first five are PC objects and two are not, which is why this item is
stated for the toolbox rather than for DOS: it is not a DOS defect, it is what
happens when a reader written for one format is pointed at another. The DOS-era
half is that these objects are small enough that a wrong answer is cheap to
believe — there is no size cue to make an empty result look implausible.

**Three instructions:**

- **run every candidate reader for its refusal first**, on an input you know it
  should reject, before you run it on the input you care about;
- **read the population size, not the exit code.** `0 of 0  AGREE` is not
  agreement — and neither is `1 of 1` when the object holds three. **A census
  should print what it examined next to what it matched**; `protscan.py`'s
  `files searched : 3 of 107` is a defect that reports itself, `mzcensus.py`'s
  `the 1` is one that does not;
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

## 6. State the chance rate before quoting the count, and say which way it runs `[4 of 49]` `[+1 object, the rate as a floor]`

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

**And there is a third case, at the opposite end of the same axis, which is
that on large structured data the rate is a FLOOR and not a ceiling.** A DOS
object is small enough that a four-byte hit is a finding; an object of a few
gigabytes is large enough that the uniform model predicts a handful of hits --
and the *observed* count runs well above the model, because packed data is not
uniform and every position in a multi-byte pattern is correlated with the
others.

```
python _work/abspaths.py <the 22 containers>          (pc-inquisitor-doc)

pattern [A-Za-z]:\ + four or more path characters
bytes scanned                     2,321,841,673
uniform-random expectation             35.8255
observed                                   174     = 4.86 x the model
```

Every one of the 174 is garbage inside compressed texture and audio data --
`J:\JJJX`, `Y:\4RPP`, `r:\SQRB_RSs` -- while the same pattern over the same
object's 3.1 MB executable returns **one** match and it is real. The same
effect on a four-byte needle, measured on the container magic that session
derived: **five accidental `DRPK` against an expectation of 0.5466, and one of
the five is inside a PDF.**

So the discipline has three parts and not two: **state the rate, then say which
way it runs, then say what the hit is.** A session that computes 35.8 and
concludes that 174 must therefore mean something has made the same mistake as a
session that never computed it, one step later. The instance that prompted this
is `mzcensus.py` reporting `LZEXE 0.91` inside a 160 MB texture container on an
object with no DOS program on it at all -- a four-byte needle, a model of
0.5466 over the population the tool actually searched, and one observed hit,
which is what chance produces
([pc-inquisitor-doc/docs/14](https://github.com/vs-sr-dev/pc-inquisitor-doc/blob/master/docs/14-the-chance-rate.md)).
**That object is Win32 and not DOS**, and it is here for the same reason the
Win9x `KERNEL32` instance above is: this section is about arithmetic, and the
only part of it that is era-specific is the paragraph that says so. The
`[4 of 49]` mark above is left as it stands because it was counted at a
denominator of 49 and has not been re-counted at one; `sweep.py` on the
machine that added this reports **8 of 53** repositories stating a rate, on a
different denominator, and the two figures are not the same measurement.

**The same tool made the same false positive a second time, on a different
object, and the second one added a part to this discipline that the first could
not.** `mzcensus.py` reported `LZEXE 0.91` inside a 279,883,198-byte Unity asset
bundle on a 2023 Windows game with no DOS program on it at all
([pc-themurderofsonicthehedgehog-doc/docs/15](https://github.com/vs-sr-dev/pc-themurderofsonicthehedgehog-doc/blob/master/docs/15-the-tools.md)).
That session computed the rate three ways over the 468,913,725 bytes the tool
actually scans, and **the first two ways were both wrong in the same
direction**:

```
uniform model, 4-byte needle       expected 0.109177   observed 1   =  9.16 x
independent bytes, this corpus's
  own measured frequencies         expected 0.0228     observed 1   = 43.85 x
240 control needles of the same
  shape (two letters, two digits)  20 of 240 score 1 or more; one scores 10
                                   -> LZ91 is in the top 8.33 % of pure noise
```

The better model made the hit look **more** significant, because `Z` and `9` are
rarer than uniform in that corpus. Only the measured control distribution
settled it.

**So the fourth part of the discipline is a direction.** Arguing a count is
*above* chance is robust to a bad model, because a bad model errs low. Arguing a
count is *within* chance is not, and it needs a control distribution of needles
of the same shape over the same bytes rather than a closed-form rate. **A rate
is enough to raise a finding and is not enough to dismiss one.** That is stated
for the toolbox rather than for DOS, and the era-specific part of it is this
sentence saying so.

### And the same signature, on the object it exists for `[1 object]`

Two false positives and no recorded true one is a lopsided record for a check,
and it invites the wrong conclusion — that `LZ91` is simply a bad needle.
`pc-hexxagon-doc` is the case it is supposed to fire on, and it is here so that
both halves of the check have an entry.

`HEXX.EXE` (HEXXAGON, Argo Games / Software Creations, 1993) is a 42,309-byte
real-mode MZ with **`e_crlc == 0`** — rule 2 above, a program of that size
declaring no fixups — and **zero slack past its declared image**, so the header
arithmetic agrees and there is no payload to find a four-byte string in.

```
python tools/sigcount.py Hexxagon --text LZ91 --label "LZEXE 0.91"
files searched                       : 20        (1,297,836 bytes)
files BEGINNING with the signature   : 0 of 20
occurrences ANYWHERE                 : 1, in 1 files
```

**One occurrence in the whole object, at offset 0x1C**, which is the MZ
header's reserved area and where LZEXE puts it. The two recorded false
positives were single hits in 160 MB and 280 MB of non-DOS container, where a
four-byte needle finds itself; this is a single hit in 1.3 MB, at the defined
offset, on a DOS program from 1993 whose relocation count already said it was
packed. **A hit at a computed offset is an identification and a hit anywhere is
a lead**, which is the distinction `dospack.py` prints in two separate columns
and which those two false positives are the reason for.

That object also supplies the **second PKLITE specimen** the family's only
PKLITE unpacker had never had — `PKLITE Copr. **1990-92**` against the 1990
build the tool was written on — and the outcome is worth one line here because
it is about a check and not about a game: the unpacker **refused**, which is
the correct outcome, but reported `no PKLITE signature at 0x1E` about a file
that has one, because its test was a whole-sentence string compare.
`mzcensus.py`'s banner table failed the same way from the other side and
printed `none`. **A signature table that matches whole version strings cannot
see a build it was not shown**, and `dospack.py`'s wider sweep found it on the
first run, in the right place. Both were repaired as instances; the class was
not
([pc-hexxagon-doc/docs/06](https://github.com/vs-sr-dev/pc-hexxagon-doc/blob/master/docs/06-two-executables.md),
[pc-hexxagon-doc/docs/10](https://github.com/vs-sr-dev/pc-hexxagon-doc/blob/master/docs/10-the-tools.md)).

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
repositories present where the sweep runs. `pc-gamelist-doc` lists 61 titles and
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
