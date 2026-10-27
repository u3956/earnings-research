# 4. Checks

Every row was checked in three layers. A script checked every row; a second pass, by script and by checker agents,
covered what the first one cannot see; and 30 numbers were checked by hand. The rules are in
[CRITERIA.md](../CRITERIA.md) (section 6). What the checks found is on the [errors page](ERRORS.md).

"Second opinion" below is the release reader redone by another model ([3_readers](../3_readers/README.md)); in the
code its folder is `readers/release_b`.

## 1. The script: every citation, every filed figure

[check.py](check.py) re-reads every citation and writes one line per row and citation.

| | The three readers | Second opinion |
|---|---|---|
| Quote exactly on its cited line | 1,983 / 1,983 | 540 / 540 |
| Quotes over 200 characters | 0 | 0 |
| Value inside its own quote | 1,452 / 1,452 | 515 / 540 (the other 25: "—" cells written as 0) |
| Filed figures matching XBRL | 562 | 44 |
| Filed figures that XBRL contradicts | 0 | 0 |
| Derived table: copied values and above/within/below labels | 26 / 26 | 16 / 16 |

- **Dated differently: 3 rows.** The filings reader dates a goodwill figure ($39.2M, after an adjustment) to the
  acquisition, Oct 31, 2025. The 10-Q tags it at the quarter end, Jan 31, 2026. Both dates can be defended; the tag's
  date is the filing's own convention.
- **No tag: 12 rows.** The employee count, and release figures for periods the filings do not tag: Q4's three months,
  and the quarterly cash flow, which the 10-Qs tag only year to date.

What a script cannot see: a quote such as "Revenue | $898,185 | $719,226 | $3,352,523 | $2,673,115" holds four
numbers, so the script cannot tell whether a row took the right column, item or basis. The next two layers cover that.

## 2. The second pass

**By script** ([second_pass.py](second_pass.py)):

| Check | The three readers | Second opinion |
|---|---|---|
| Each GAAP to non-GAAP reconciliation adds up (GAAP + the adjustments = non-GAAP, with the pre-tax and tax steps) | 35 / 35 | 35 / 35 |
| Stated margins and free cash flow recompute from their parts | 15 / 15 | 49 / 49 |
| Rows on a table line with several numbers took the right column | 209 / 209 | 338 / 338 |
| Consensus rows sit under the right period, estimate and field | 36 / 36 | 36 / 36 |

- **Speaker labels:** 642 of 642 match the official transcript.
- **Every analyst question has a row.**
- **Filing changes:** 52 of 52 hold up. No "added" passage was already in the earlier filing, no "removed" one is still
  in the new filing, and each "changed" row's two quotes appear only in their own filing.
- **The checks can fail:** two errors planted on purpose (a shifted value and a relabeled period) were both caught by
  the sums.
- **Completeness.** A scan found 114 lines in the releases, letters, slides and supplementals that name a metric next
  to a number and that no row cites. Most repeat a figure already taken from another document. The rest were:
  - six outlook items that both release readers had found but kept in their notes, because the form had no row for
    them;
  - six product and customer metrics that both missed.

  The revised form now names all twelve.

**By checker agents.** Agents read the 904 rows that need judgment (every call row and every filing change), each
next to the text it rests on. They raised 17 flags, and every flag was checked against the source:

| Outcome | Rows |
|---|---|
| Fixed: an overstatement, a dropped hedge, a guessed period or a kept mishearing (none changed a number) | 13 |
| Left as they were: one row already marked unverified, and one speaker that the text cannot settle | 2 |
| The flag was wrong | 2 |

The 13 fixes, with every old and new value, are in [corrections.csv](corrections.csv). The owner approved them and
left four borderline labels as they were. Three answers labeled *dodged* gave a direction but not the specifics asked
for, which a literal reading would call *partial*, and one *partial* answer was of the same kind.

## 3. Thirty numbers by hand

[sample.py](sample.py) drew [hand_check_30.csv](hand_check_30.csv) with a fixed seed (the script names the file
`hand30.csv`). It drew only numbers that the scripts could not confirm against XBRL, because the scripts had already
confirmed the rest:

| Drawn from | Numbers |
|---|---|
| Filed figures with no matching XBRL tag | 2 |
| Release results (5 product metrics, 3 non-GAAP, 1 GAAP) | 9 |
| Guidance | 6 |
| Consensus | 2 |
| Call statements (one per event, the rest at random) | 9 |
| Rows only the second opinion had | 2 |

Each row names the original document, the PDF page, sheet or timestamp, and the quote to search for. The owner opened
each original and checked the item, period, basis and column: 30 of 30 were right. In this file the eight quotes from
transcripts are blanked; two of the same rows, C446 and C609, appear with their quotes in the
[transcripts sample](../2_transcripts/samples/call_statements.csv).

## 4. The error rate after both passes

| | Rows | Wrong numbers | Rows needing a fix |
|---|---|---|---|
| Filing facts | 532 | 0 | 0 |
| Filing changes | 60 | | 0 |
| Release tables | 422 | 0 | 0; the completeness gaps above |
| Release tables, second opinion | 556 | 0 | 0 (25 "—" cells written as 0, 2 growth-only guidance rows in the wrong columns) |
| Call statements | 720 | 0 | 9 (1.3%) |
| Q&A | 81 | 0 | 3, plus the 4 borderline labels |
| Wording | 43 | | 1 |

## The code

- [check.py](check.py): the citation and XBRL check.
- [second_pass.py](second_pass.py): the second pass by script.
- [sample.py](sample.py): draws the hand check.

All three are published in full. They read the private text copies and tables, so they do not run from this repo;
they are here to be read.
