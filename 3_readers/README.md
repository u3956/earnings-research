# 3. Readers

Three reader agents turned the line-numbered text into fixed tables, in which every number carries its file, line and
exact quote. The rules they worked to are in [CRITERIA.md](../CRITERIA.md) (sections 3 to 5).

## The readers' form

The form is the fixed set of tables each reader fills in: their columns, the values allowed in each, the units and the
citation rules.
- [reader_form.md](reader_form.md) is the form the readers used for this report.
- [reader_form_revised.md](reader_form_revised.md) is the form revised after the checks, for the next report. Each
  change is marked "(v2)".

| What the revision added | Why |
|---|---|
| Every product and customer metric named, plus the year-to-date columns and extra statement lines | Two other models (below) skipped 12 metrics that the letters reported but the brief did not name |
| A row for every outlook item: capital spending, restructuring, the acquisition's guidance, the timing of new ARR, other income | The readers had found six outlook items but kept them in their notes, because the first form had no row for them |
| One vocabulary for scale: ones, thousands, millions, billions | The first form left the scale words open |
| A "—" cell gets no row | One of the other models wrote 25 such cells as 0 |
| Guidance reprinted for an earlier quarter goes under that quarter | The Q1 guidance was found in a look-back table, with nowhere to put it |
| Exact table figures over rounded headlines | The readers' only disagreements were a headline figure against the table figure |

## One reader per source

| Reader | Reads | Tables (rows) |
|---|---|---|
| Filings | The three 10-Qs, the 10-K and the other 8-Ks; not the press releases | facts 532, changes 60 |
| Release | The four press releases, the shareholder letters, the Q1 call slides, the supplementals, the modeling sheet, the earnings history and the consensus snapshot | results 127, guidance 69, reconciliations 164, consensus 36, compare 26 (derived) |
| Call | The official transcripts, our investor-day transcripts and the investor-day deck ([2_transcripts](../2_transcripts/README.md)) | statements 720, Q&A 81, wording 43 |

Each reader works only from the line-numbered text and gets its own brief. It hands back its tables, a notes file and a
short report. The notes file lists what it could not find, its judgment calls, and what looked wrong in the sources,
each with its citation. The briefs are kept exactly as they were sent.

## Nothing corrected before the checks

The tables passed a shape check (headers, ids, allowed values, citations filled in) and nothing else, so the checks
measure the readers' own error rate. Where a reader departed from its brief, the departure is written down and left in
place:
- the release reader recorded the Q1 guidance under the quarter before, which the first form did not allow;
- the call reader has no scale column (its unit carries the scale), and it writes a guidance range as two rows;
- two readers saved their helper scripts outside their own folders;
- each reader said it had re-checked its own quotes. That was a claim until the script checked it.

## A second opinion on the release reader

Two other models, run through Codex CLI, redid the release reader from the same brief in a clean copy of the text. A
script then scored all three:
- all three quoted every line exactly and matched every filed figure to XBRL;
- where they disagreed, it was rounding: a headline figure against the table figure;
- the most complete recorded 231 result rows against the original's 127: the year-to-date columns, gross profit, the
  share counts, capital spending, the tax rate;
- both skipped the 12 product metrics the letters report in their prose, because the brief did not name them. The
  original reader had found them unasked;
- one wrote 25 dash cells as 0, and the other missed the Q1 guidance reprinted in the Q1 slides.

So the revised form names everything, and the most complete model reads the next quarter's release with it.

## The samples

A handful of rows from each table, as the readers wrote them, with the check results for each row:

| Column | Meaning |
|---|---|
| `text`, `line`, `quote` | The citation: the file (under the text copies), the line number, the exact quote |
| `quote_on_line` | The quote was found exactly on that line |
| `value_in_quote` | The value is one of the numbers in the quote |
| `xbrl_check` | `ok`: the filed figure matches the filing's XBRL. `other_period`: the tag is dated differently. `not_found`: no tag covers that period. Blank: not a filed figure |
| `xbrl_concept`, `xbrl_value` | The XBRL tag that was compared, and its value |

- [filings_facts.csv](samples/filings_facts.csv): five rows. They include a goodwill figure that the filing tags at a
  later date than the reader gave (F252) and the employee count, which no tag covers (F531).
- [filings_changes.csv](samples/filings_changes.csv): four rows. A new risk that AI lowers the barriers to entry, a new
  risk about charging for AI agents' traffic, a pricing risk, and the restructuring 8-K.
- [release_results.csv](samples/release_results.csv): seven rows from the release, a letter, the slides and a
  supplemental spreadsheet.
- [release_guidance.csv](samples/release_guidance.csv): six rows. They include the Q1 guidance from a look-back table
  (G001), and the FY27 ARR range that a web summary called revenue (G061).
