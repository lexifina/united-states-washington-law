# How this repository was made (Washington)

This file is written by the build on 2026-10-30, the day the source data was retrieved.

## Sources

| Source | Address | Retrieved | Licence |
| --- | --- | --- | --- |
| Washington Office of the Code Reviser: Revised Code of Washington, section files | <https://lawfilesext.leg.wa.gov/law/RCW/> | 2026-10-30 | The site footer states "Copyright. All Rights Reserved." site-wide; no claim specific to the RCW text was found, and the Code Reviser publishes the RCW for public use. Statute text of a state is not copyrightable (Georgia v. Public.Resource.Org, 590 U.S. 255 (2020)). Only statute text is taken, not the notes that follow it. |

Every word of law in this repository comes from these sources. Lexifina reads them and records each act's dated versions, and the laws that made each change, in one corpus file. This repository is built from that file.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `constitution` | Constitution of the State of Washington | 1 | 2025-12-11 to 2025-12-11 |
| `title-9a-criminal-code` | Title 9A RCW, Washington Criminal Code | 1 | 2026-10-22 to 2026-10-22 |

The build made 2 commits:

| Commits | Kind |
| ---: | --- |
| 2 | first version of an act |
| 0 | one law on its in-force day |
| 0 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `future`: laws not yet in force on 2026-10-30.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 0 laws in the record.
- 2 tags.

## Dates

Each commit is dated at noon (America/Los_Angeles) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: Each section file is the Code Reviser's current text of the section; the latest modification date shown for the title is used as the version date (oldest version available). https://app.leg.wa.gov/rcw/

## How the history is built

`tools/build.py` turns the corpus into this history in one pass: one commit per law, on the day it took effect. The same corpus always gives the same commit hashes. `tools/check_repo.py` reads every version back from git and compares it with the corpus. `tools/on.py` shows the law as it stood on any date. The corpus format is described in `tools/SCHEMA.md`.

- Corpus: sha256 `b0f202bb992af00c3f3ef7ef444090b08008285de60727fefc08bb9366ac25a4` (856291 bytes).
- Builder blob hashes (`git hash-object`): `build.py` `a4faa25af85facb64b956b372f6b528aafdd7ec1`, `check.py` `3e59cb6f05eccb94a9ec14431a7f6781221e83ef`, `on.py` `644a6c0857fbcc72562032b58d57aa113fee0641`.
- Python 3.12.10; git version 2.46.0.windows.1.

## Checks

Not yet run for this build.

No second build of this corpus has been compared yet.

## Decisions made by hand

- Only these parts of Washington law were taken for this build: the Constitution, RCW Title 9A (Washington Criminal Code). The other RCW titles, the session laws and the Administrative Code are not in it.
- The Constitution is read from part (A) of the Legislature’s PDF (printed 2025-12-11), which sets each current section in regular type and the superseded texts of amended sections in italics under bold "Amendment N" or "Original text" lines. Only regular-type text under a bold "SECTION n" heading is kept; the superseded texts, the bracketed "[AMENDMENT n ...]" history notes, the Reviser’s notes at the foot of six sections and the page footers are left out. Line-end hyphens were joined unless the same hyphenated word appears inside a line elsewhere in the PDF. A section is one line, because the PDF does not mark paragraph breaks reliably. The version is dated by the print date on the PDF; the 270 sections match the list of sections on the Legislature’s web page for the Constitution.
- Each title is a set of per-section HTML files. The publisher's annual RCW archive (2023 to 2026) holds only certified PDFs, which were not read. Each title is therefore one version, the oldest version available, dated by the latest modification date shown in the publisher's directory listings for that title.
- Only the Text field of each section file is kept. The history line (session laws), notes, cross references and annotations are left out.
- Unit keys are the section citation split into digit and letter runs, with each digit run padded to three places and lower-cased (RCW 9A.04.010 is rcw-009-a-004-010); the label is the citation.
- Typographic quotes and dashes were made plain, non-breaking spaces were made ordinary spaces and runs of spaces were collapsed.

## What AI did and did not do

The scripts that read the sources and build this repository were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- none
