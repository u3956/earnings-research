# 3. Extraction

Three extraction agents, referred to as readers, converted the line-numbered text into fixed tables in which every
figure carries its file, line and verbatim quote. The rules they followed are set out in [CRITERIA.md](../CRITERIA.md),
sections 3 to 5.

## Table definitions

The table definitions specify the tables each reader completes: their columns, the values allowed in each, the units
and the citation rules.
- [reader_form.md](reader_form.md) is the version used for this report.
- [reader_form_revised.md](reader_form_revised.md) is the version revised after verification, for the next report.
  Each change is marked "(v2)".

| Revision | Reason |
|---|---|
| Every product and customer metric named, together with the year-to-date columns and additional statement lines | The two independent extraction models (below) omitted 12 metrics that the letters reported but the brief did not name |
| An entry for every outlook item: capital expenditure, restructuring, the acquisition's guidance, the timing of new ARR, other income | The readers had found six outlook items but left them in their notes, because the first version had no entry for them |
| A single vocabulary for scale: ones, thousands, millions, billions | The first version left the scale terms open |
| A "—" cell produces no entry | One of the independent models recorded 25 such cells as 0 |
| Guidance restated for an earlier quarter is recorded under that quarter | The Q1 guidance was found in a look-back table with no place to record it |
| Exact table figures take precedence over rounded headlines | The readers' only disagreements were between a headline figure and the corresponding table figure |

## One reader per source group

| Reader | Sources | Tables (entries) |
|---|---|---|
| Filings | The three 10-Qs, the 10-K and the other 8-Ks; not the earnings releases | facts 532, changes 60 |
| Release | The four earnings releases, the shareholder letters, the Q1 call presentation, the supplementals, the modeling sheet, the earnings history and the consensus snapshot | results 127, guidance 69, reconciliations 164, consensus 36, compare 26 (derived) |
| Call | The official transcripts, the in-house investor-day transcripts and the investor-day presentation ([2_transcripts](../2_transcripts/README.md)) | statements 720, Q&A 81, wording 43 |

Each reader works only from the line-numbered text and receives its own brief. It returns its tables, a notes file and
a short report. The notes file lists what the reader could not find, the judgment calls it made, and anything in the
sources that appeared wrong, each with a citation. The briefs are kept exactly as sent.

## No corrections before verification

The tables passed a format check (headers, identifiers, allowed values, citations present) and nothing else, so the
verification measures the readers' own error rate. Departures from the brief are documented and left in place:
- the release reader recorded the Q1 guidance under the preceding quarter, which the first version did not allow;
- the call reader has no scale column (its unit field carries the scale) and records a guidance range as two entries;
- two readers saved their helper scripts outside their own folders;
- each reader reported that it had re-checked its own quotes, a claim that was confirmed only once the script ran.

## Independent extraction of the earnings release

Two other models, run through Codex CLI, repeated the release extraction from the same brief on a clean copy of the
text. A script then scored all three:
- all three quoted every line exactly and matched every filed figure to XBRL;
- where they disagreed, the difference was rounding: a headline figure against the table figure;
- the most complete recorded 231 result entries against the original's 127, adding the year-to-date columns, gross
  profit, share counts, capital expenditure and the tax rate;
- both omitted the 12 product metrics reported in the letters' prose, because the brief did not name them; the
  original reader had recorded them without being asked;
- one recorded 25 dash cells as 0, and the other missed the Q1 guidance restated in the Q1 presentation.

The revised table definitions therefore name every item, and the most complete model will extract the next quarter's
release using them.

## Samples

A few entries from each table, as the readers recorded them, with the verification results for each:

| Column | Meaning |
|---|---|
| `text`, `line`, `quote` | The citation: the file (within the text copies), the line number and the verbatim quote |
| `quote_on_line` | The quote was found exactly on that line |
| `value_in_quote` | The value is one of the figures in the quote |
| `xbrl_check` | `ok`: the filed figure matches the filing's XBRL. `other_period`: the XBRL tag carries a different date. `not_found`: no tag covers that period. Blank: not a filed figure |
| `xbrl_concept`, `xbrl_value` | The XBRL concept compared, and its value |

- [filings_facts.csv](samples/filings_facts.csv): five entries, including a goodwill figure that the filing tags at a
  later date than the reader gave (F252) and the employee count, which no tag covers (F531).
- [filings_changes.csv](samples/filings_changes.csv): four entries: a new risk that AI lowers barriers to entry, a new
  risk concerning charges for AI agents' traffic, a pricing risk, and the restructuring 8-K.
- [release_results.csv](samples/release_results.csv): seven entries from the release, a letter, the presentation and a
  supplemental spreadsheet.
- [release_guidance.csv](samples/release_guidance.csv): six entries, including the Q1 guidance from a look-back table
  (G001) and the FY27 ARR range that a web summary presented as revenue (G061).
