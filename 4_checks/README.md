# 4. Verification

Every entry was verified in three layers: a script checked every entry; a second pass, by script and by review agents,
covered what the first cannot detect; and 30 figures were checked manually. The rules are set out in
[CRITERIA.md](../CRITERIA.md), section 6, and every issue found is recorded in the [error log](ERRORS.md).

"Independent extraction" below refers to the release extraction repeated by two other models
([3_readers](../3_readers/README.md)); in the code, its folder is `readers/release_b`.

## 1. Scripted check of every citation and filed figure

[check.py](check.py) re-reads every citation and writes one line per entry and citation.

| | Three readers | Independent extraction |
|---|---|---|
| Quote found exactly on its cited line | 1,983 / 1,983 | 540 / 540 |
| Quotes over 200 characters | 0 | 0 |
| Value found within its own quote | 1,452 / 1,452 | 515 / 540 (the remaining 25: "—" cells recorded as 0) |
| Filed figures matching XBRL | 562 | 44 |
| Filed figures contradicted by XBRL | 0 | 0 |
| Derived table: copied values and above/within/below labels | 26 / 26 | 16 / 16 |

- **Dated differently: 3 entries.** The filings reader dates a goodwill figure ($39.2M, after an adjustment) to the
  acquisition date, Oct 31, 2025, while the 10-Q tags it at the quarter end, Jan 31, 2026. Both dates are defensible;
  the tag follows the filing's own convention.
- **No XBRL tag: 12 entries.** The employee count, and release figures for periods the filings do not tag: Q4's three
  months, and quarterly cash flow, which the 10-Qs tag only on a year-to-date basis.

A script cannot judge context. A quote such as "Revenue | $898,185 | $719,226 | $3,352,523 | $2,673,115" contains four
figures, so the script cannot tell whether an entry took the right column, item or basis. The next two layers address
that.

## 2. Second pass

**Scripted** ([second_pass.py](second_pass.py)):

| Check | Three readers | Independent extraction |
|---|---|---|
| Each GAAP to non-GAAP reconciliation adds up (GAAP plus adjustments equals non-GAAP, including the pre-tax and tax steps) | 35 / 35 | 35 / 35 |
| Stated margins and free cash flow recompute from their components | 15 / 15 | 49 / 49 |
| Entries on a table line with several figures took the correct column | 209 / 209 | 338 / 338 |
| Consensus entries sit under the correct period, estimate and field | 36 / 36 | 36 / 36 |

- **Speaker attribution:** 642 of 642 labels match the official transcript.
- **Q&A coverage:** every analyst question has an entry.
- **Filing changes:** 52 of 52 are confirmed. No "added" passage already appeared in the earlier filing, no "removed"
  passage remains in the new one, and each "changed" entry's two quotes appear only in their own filings.
- **Sensitivity:** two deliberately planted errors (a shifted value and a mislabeled period) were both caught by the
  sums.
- **Completeness.** A scan found 114 lines in the releases, letters, presentations and supplementals that name a metric
  next to a figure but are not cited by any entry. Most repeat a figure already taken from another document. The
  remainder were:
  - six outlook items that both release extractions had found but left in their notes, because the first version of
    the table definitions had no entry for them;
  - six product and customer metrics that both missed.

  The revised table definitions name all twelve.

**Review agents.** Review agents re-read the 904 judgment-based entries (every call entry and every filing change),
each against the text it rests on. They raised 17 flags, each verified against the source:

| Outcome | Entries |
|---|---|
| Corrected: an overstatement, a dropped qualifier, an unsupported period or a retained mishearing (none changed a figure) | 13 |
| Left unchanged: one entry already marked unverified, and one speaker the text cannot determine | 2 |
| Flag incorrect | 2 |

The 13 corrections, with every original and revised value, are in [corrections.csv](corrections.csv). They were
approved after manual review, and four borderline grades were left unchanged: three answers graded *dodged* gave a
direction but not the specifics requested, which a strict reading would grade *partial*, and one *partial* answer was
of the same kind.

## 3. Manual sample of 30 figures

[sample.py](sample.py) drew [hand_check_30.csv](hand_check_30.csv) with a fixed random seed (the script writes the
file as `hand30.csv`). It draws only figures the scripts could not confirm against XBRL, since the scripts had already
confirmed the rest:

| Drawn from | Figures |
|---|---|
| Filed figures with no matching XBRL tag | 2 |
| Release results (5 product metrics, 3 non-GAAP, 1 GAAP) | 9 |
| Guidance | 6 |
| Consensus | 2 |
| Call statements (one per event, the rest at random) | 9 |
| Entries found only in the independent extraction | 2 |

Each row identifies the original document, the PDF page, sheet or timestamp, and the quote to search for. Each figure
was checked in the original for the correct item, period, basis and column: 30 of 30 were correct. In this file the
eight quotes from transcripts are withheld; two of the same entries, C446 and C609, appear with their quotes in the
[transcripts sample](../2_transcripts/samples/call_statements.csv).

## 4. Error rates after both passes

| | Entries | Incorrect figures | Entries needing correction |
|---|---|---|---|
| Filing facts | 532 | 0 | 0 |
| Filing changes | 60 | | 0 |
| Release tables | 422 | 0 | 0; see the completeness gaps above |
| Release tables, independent extraction | 556 | 0 | 0 (25 "—" cells recorded as 0, 2 growth-only guidance entries in the wrong columns) |
| Call statements | 720 | 0 | 9 (1.3%) |
| Q&A | 81 | 0 | 3, plus the 4 borderline grades |
| Wording | 43 | | 1 |

## Code

- [check.py](check.py): the citation and XBRL check.
- [second_pass.py](second_pass.py): the scripted second pass.
- [sample.py](sample.py): draws the manual sample.

All three are published in full. They read the private text copies and tables, so they do not run from this
repository; they are included for reference.
