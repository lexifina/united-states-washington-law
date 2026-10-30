# Washington: law history in git

The Constitution of the State of Washington and Title 9A of the Revised Code of Washington (the Criminal Code) as a git repository: one file per section, committed with the Washington Office of the Code Reviser as its publisher. It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law), which places it at `united-states/washington/`.

**What is in it now**

| Folder | Act | Versions | History |
| --- | --- | ---: | --- |
| `constitution/` | Constitution of the State of Washington (1889, as amended): Preamble and Articles I to XXXII, 270 units | 1 | One version, the current text in the Legislature's PDF printed 11 December 2025 |
| `title-9a-criminal-code/` | Title 9A RCW, Washington Criminal Code (402 sections) | 1 | One version, the Code Reviser's current text |

That is all the law this repository holds today. This is a first build: the other RCW titles, session laws and the Washington Administrative Code are not in it, and it has no amendment history yet.

## Where the text comes from

The Constitution is read from part (A) of the Legislature's PDF (leg.wa.gov), which sets each current section in regular type and the earlier texts of amended sections in italics; this build keeps the regular type only and leaves out the bracketed amendment history notes and the Reviser's notes. A section is one line, because the PDF does not mark paragraph breaks reliably. The Code Reviser publishes every RCW section as its own file at lawfilesext.leg.wa.gov. This build takes the Text of each section from those files and nothing else. It leaves out the history line (the session laws that enacted and amended the section), the notes, cross references and annotations.

## Dates

- Each title has a single version, dated by the latest modification date the publisher's directory listings show for that title's section files. It is the oldest version available: the Code Reviser's annual RCW archive (2023 to 2026) is published as certified PDFs, which this build did not read, so no earlier text is here. Each first commit is credited to the publisher as "oldest version available".
- The Constitution has one version, dated by the print date on the PDF (11 December 2025). It is the oldest version available; its earlier texts are shown in the PDF only as superseded italics and are not built into dated versions.

## What it does not show

- Any amendment history: which session law changed which section and when. The history line of each section names them, but past texts are not read yet.
- The history lines, notes and annotations.
- Nothing here is an official publication.

## How it is checked

- Every unit is read back from git on its day and compared with the corpus (`tools/check_repo.py`; results in `REPRODUCE.md`).
- The source of each version is identified by a sha256 in `data/versions.json`.
