# dos-platformnotes-doc

**A checklist for the MS-DOS-era subset of the PC family**, to be carried from
one documentation pipeline to the next and added to by each.

→ **[dos-platform-notes.md](dos-platform-notes.md)**

## It is a subset, not a family, and it says so in its first section

[pc-gamelist-doc](https://github.com/vs-sr-dev/pc-gamelist-doc) says in its
second paragraph that the PC family has **no** shared platform checklist,
because a DOS game from 1987 and a PhyreEngine remaster from 2018 have almost
nothing in common. That decision stands and this repository does not reopen it.
It answers the narrower question the decision leaves open — whether the DOS-era
*subset* has enough in common — and it answers it with a count rather than an
opinion:

```
python tools/sweep.py
repositories swept: 49  (../pc-* with a docs/, index excluded)

an MZ header field                       25 of 49
a DOS-era packer                         16 of 49
```

Half the family has independently done MZ header arithmetic and a third of it
has independently met a DOS packer. That is what a shared document is for.

**Its primary index is
[pc-gamelist-doc](https://github.com/vs-sr-dev/pc-gamelist-doc)**, not the
profile README. The profile README's platform-notes slot is for a document that
covers a whole family; a subset document in that slot would assert exactly what
the paragraph above denies.

## It was written out of a sweep, not out of an object

The CD-i and Amiga CD checklists were written out of their first pipeline; the
Dreamcast one was written before its first pipeline. **This one was written out
of forty-nine finished repositories at once and out of none of them
individually**, which is deliberate: the chapter that first argued for it,
[pc-kingsofthebeach-doc/docs/14](https://github.com/vs-sr-dev/pc-kingsofthebeach-doc/blob/master/docs/14-against-the-collection.md),
concluded that the checklist was worth writing and then **refused to write it**,
because a family document written on the strength of one object is the error the
pipeline exists to avoid.

So there are no `[unverified]` marks here. Every item carries either `[n of 49]`
— repositories whose chapters mention it — or `[n objects]`, naming the
repositories that actually exercised it. Where an item rests on a single object,
it says `[1 object]` next to that item and does not round up. Two of the six do.

## The six items

| # | item | support |
|---|---|---|
| 1 | The tool you have is not the tool you remember | `[5 objects]` — five copies of `exepack.py`, five distinct files, three different command lines |
| 2 | The declared image is not the file | `[25 of 49]`, and 28 copies of `mzcensus.py` in two versions |
| 3 | After unpacking, the relocation table is the only content check | `[5 objects]`, the defect itself `[1 object]` |
| 4 | A reader that refuses is worth more than a reader that answers | `[5 objects, 3 families]`, `[8 of 107]` |
| 5 | DOS timestamps have two-second granularity | `[22 of 49]`, both halves of the question closed |
| 6 | State the chance rate before the count, and say which way it runs | `[4 of 49]`, the DOS inversion `[1 object]` |

**What is not in it: anything about content.** Eleven repositories mention EGA
and seven mention CGA, and the formats behind them are per title and were
derived from the bytes every time. A checklist entry for `.PAK` would be wrong
before it was written — in this collection `.PAK` already means three unrelated
formats.

## The tool

`tools/sweep.py` reprints every figure in the document.

```
python tools/sweep.py                     # the term table
python tools/sweep.py --tools             # copies and distinct versions per tool
python tools/sweep.py --list EXEPACK      # which repositories a term hits
python tools/sweep.py --pattern '*'       # the whole collection, 107 repositories
```

It counts repositories rather than mentions, excludes every `*gamelist-doc` so
that an index does not count its titles twice, and refuses to print a table over
an empty population — which is item 4 applied to itself.

No game assets or executables are in this repository: only measurements and the
code to reproduce them.
