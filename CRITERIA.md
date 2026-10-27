# The rules behind the report

These are the rules the tables were built and checked by. Each one says what is done, why, and what it caught. The
folders show the work; this page is the method.

## 1. Sources

**1.1 Primary documents only.** Every number comes from a document the company or the SEC published: the filings, the
press releases, the shareholder letters, slides and supplemental spreadsheets, and the call transcripts. Nothing comes
from a web summary or a data vendor's restatement. The analysts' consensus is the one outside figure, and it is kept as
a dated snapshot.
*Why:* a web search summary gave the FY27 ARR guidance ($4.396-4.426B) as revenue guidance. Revenue is guided to
$3.908-3.938B.

**1.2 Each source is trusted for what it is good at.**

| Source | Trusted for |
|---|---|
| 10-Q and 10-K | Filed figures, judged against the filing's own XBRL tags (the machine-readable copy the company files with the SEC) |
| Press release (the 8-K exhibit) | The quarter's results and guidance as the company states them |
| Shareholder letters, slides, supplementals | What the filings and the release leave out: ARR detail, product and customer metrics, guidance reprinted for earlier quarters, the timing of new business |
| Official call transcripts | What management said, and who said it |
| Our own transcripts | Timestamps, and a check on the official text. Where only a recording exists (the investor day), our transcript is the text, and the slides decide any number in doubt |
| Analyst consensus | Estimates as of a stated date, never mixed with reported figures |

**1.3 Exact table figures over rounded headlines.** A row takes $850,475 thousand from the income statement rather than
"$850.5 million" from the headline, unless no table prints the figure.
*Why:* a headline is rounded, and only a table figure can be matched to XBRL exactly.

**1.4 Kept exactly as fetched.** Each file is fetched once and logged with its address, its fetch time in UTC, its
size and its checksum. A filing already on disk is never fetched again. The SEC's lists of filings and facts are kept
as new dated files on every run.
*Why:* two downloads of the same SEC data disagreed. Copies of the filing list taken two weeks earlier gave acceptance
times four hours later than a fresh download, exactly the gap between UTC and New York time. Whatever the cause, a copy
can differ from the next download, so every file says when it was read.

## 2. Transcripts

**2.1 Two transcripts of the same call.** The official transcript of each call comes from the company's investor
relations site. We also transcribed the Q4 call ourselves from its replay.
*Why:* the official text has no timestamps and can be wrong. Ours has timestamps, and it can be wrong in other ways.
Comparing the two caught errors in both (§2 of the [errors page](4_checks/ERRORS.md)).

**2.2 Our own transcripts are made the same way every time.** The model is Whisper large-v3 on a local GPU, with English
forced and a list of the company's own spellings of its products, people and acquisitions. Every line keeps its
timestamp. The investor day's six recorded sections (3 hours 27 minutes) exist only as recordings, so our transcript is
their only text.

**2.3 Who said it.** Speakers come from the official transcript's labels, and a script checks that the label above every
cited line matches the row (642 of 642). Our own transcripts have no labels. There, the speaker is worked out from the
introductions and the section titles, and the reader's notes say how.

**2.4 Quote only what the citation needs.** The official transcripts are licensed for local use and short quotes, so a
row quotes a phrase, not a passage, and this repo publishes only a few lines.

## 3. Citations

**3.1 Every value carries its own proof.** Three columns say where a number came from:
- the file;
- the line number in that file, counting from 1;
- an exact quote from that line, copied character for character (no edits, no "..."), at most 200 characters long,
  that contains the value as printed.

*Why:* a script can then find every number again without judgment, and a person can open the exact line.

**3.2 Every source becomes line-numbered text first.** One line per table row (its cells joined by " | ") or per
paragraph, with markers for each PDF page and spreadsheet sheet.
*Why:* a citation needs lines that stay the same, and a person checking it needs the page or the sheet.

**3.3 A computed number never hides in a cited table.** A quote must contain its value, so a number that had to be
worked out goes only into a table marked *derived*, which points to the rows it was computed from.

**3.4 Missing is fine; guessing is not.** Each reader keeps notes in three parts: what it could not find, the judgment
calls it made, and anything in the sources that looked wrong, each with its citation.

## 4. The readers' form

The form is the fixed set of tables each reader fills in: their columns, the values allowed in each column, the units,
and the citation rules. There are two versions:
- [reader_form.md](3_readers/reader_form.md) is the form the readers used for this report;
- [reader_form_revised.md](3_readers/reader_form_revised.md) is the form revised after the checks, ready for the next
  report.

**4.1 Values as printed, in the source's own scale.** The scale is one of ones, thousands, millions or billions. A value
in parentheses is negative, and a percentage is a plain number with the unit "%".

**4.2 The company's own calendar.** Every row carries a fiscal quarter or year (Zscaler's year ends July 31). A figure
that a later document reprints is recorded under the quarter it belongs to.
*Caught:* the readers found the Q1 guidance reprinted in a look-back table and had nowhere to put it; the revised form
allows it.

**4.3 A dash means nothing was reported.** A cell printed "—" gets no row.
*Caught:* one of the second-opinion readers (rule 5.5) had written 25 such cells as 0.

**4.4 What is recorded:**
- reported results;
- guidance;
- the reconciliations from GAAP to non-GAAP;
- the consensus;
- what changed in each filing against the one before (risk factors, accounting, management, acquisitions);
- what management said on each call;
- every analyst question, with how fully it was answered;
- how management's wording on the same topic changed from one call to the next.

**What is left out:**
- the XBRL files: they are the checker's ground truth, so the readers never see them;
- most customer anecdotes;
- anything not in the line-numbered text.

**4.5 Name everything you want.** The revised form names every product and customer metric, the year-to-date columns
and the extra lines of each statement.
*Why:* both second-opinion models (rule 5.5) kept to the brief's list word for word. They skipped 12 product metrics that
the letters reported but the brief did not name.

## 5. The readers

**5.1 One reader per source.** The filings, the release and the call each get their own agent and their own brief. The
briefs are kept exactly as they were sent.

**5.2 Nothing is corrected before the checks.** The tables pass a shape check (headers, ids, allowed values, citations
filled in), and nothing more.
*Why:* the error count is then the readers' own. Where a reader departed from its brief, the departure is written down
and left in place.

**5.3 Every analyst question is graded on a fixed scale:**
- *direct*: the specific ask was addressed;
- *partial*: one part, or the number asked for, was missing;
- *dodged*: the specific ask was not addressed. The row then says what was asked and not answered.

Of 81 questions, 43 were answered directly, 33 in part and 5 dodged.

**5.4 Wording is tracked between consecutive events on the same topics:** demand, guidance tone, the acquisition,
margins, cash flow and capital spending, sales leadership, and AI. Each change is marked stronger, weaker, new, dropped
or the same.

**5.5 A second opinion on the release reader.** Two other models redid it from the same brief, and a script scored all
three. All were exact on every citation and on the filed figures; they differed only in rounding. The most complete
of them recorded 231 result rows against 127, but it skipped what the brief did not name (rule 4.5).

## 6. The checks

**6.1 Script first, on every row.** A script checks that:
- every quote sits exactly on its cited line;
- every value is inside its quote;
- no quote runs over 200 characters;
- every filed figure matches the filing's own XBRL;
- the derived table recomputes.

*Result:* 1,983 of 1,983 quotes, 1,452 of 1,452 values, and 562 filed figures matched, with none contradicted.

**6.2 A second pass by script, for what the first cannot see.** It checks that:
- each reconciliation adds up within the rounding of its printed terms;
- stated margins and free cash flow recompute;
- a row cited on a line with several numbers took the right column;
- each consensus figure sits under the right period and field;
- each filing change was really added, removed or changed.

Two errors were planted on purpose (a shifted value and a relabeled period), and the sums caught both.

**6.3 Checker agents for what only a reader can judge.** Every transcript row and every filing change (904 rows) was
read next to the text it rests on, looking for a wrong item or period, an unfair summary, or a dropped hedge.
*Rule:* every flag is checked against the source before it counts.
*Result:*
- 17 flags. 13 rows were fixed, 2 were left as they were, and 2 flags were wrong.
- None of the 13 fixes changed a number.

**6.4 Fixes are logged, not hidden.** Every fixed field keeps its old value ([corrections.csv](4_checks/corrections.csv)).
Four borderline answered/dodged labels were left as they were: the owner's call.

**6.5 Thirty numbers by hand, where the scripts are blind.** The 30 are drawn with a fixed seed, so anyone can redraw
the same sample.
- They come only from rows the scripts could not confirm against XBRL, spread over the filings, release and call
  tables.
- Each one was opened in the original document, at its PDF page, sheet or timestamp, and checked for the right item,
  period, basis and column.

*Result:* 30 of 30 right ([hand_check_30.csv](4_checks/hand_check_30.csv)).

**6.6 One errors page for both sides.** The agents' mistakes and the sources' mistakes go on the same page, each with
its citation and how it was caught.

## 7. The comparison

**7.1 The same page for every company, and no verdict.** All 19 companies in the cybersecurity group get the same
one-page template and the same columns. They are not ranked.

**7.2 Every figure shows its arithmetic.** Each page number points to a row of the company's figures file. The row gives
the calculation and the lines of the sources it used.
- Growth is the revenue filed in XBRL against the same quarter a year earlier.
- Free cash flow is operating cash flow less capital spending and capitalized software, over four quarters.
- A revenue beat is measured against the top of the range guided the quarter before, in %. An EPS beat is measured in
  dollars a share, because a ratio turns a smaller-than-guided loss into a "miss".
- A full-year guide counts as raised, held or cut when its midpoint moved by more than 0.05%.

All the column rules are in the [comparison's README](5_comparison/README.md).

**7.3 Fix the rule when a page shows it is wrong.** On Oct 27, one company's page showed problems, so the rules changed
and every page was rebuilt:
- **Next-twelve-month revenue** now takes the same quarters a year later, grown at next year's consensus growth. The old
  flat share overstated growth by up to 5 points.
- **Next-twelve-month EPS** is now a time-weighted blend of this year's and next year's consensus.
- **EPS beats** are counted from the sign of the reported surprise, because the stored two-decimal figures can tie.
- **Guidance** is printed exactly as the company gave it.
- **The full-year line** also names any other full-year guide that moved differently from revenue, for example ARR raised
  while revenue was held.

## 8. Limits

- **One company, one year of reports.** The rules held up here; that does not prove they hold everywhere.
- **The second opinion covered the release reader only.** The call reader's tables were checked by the checker agents
  and by hand, but no second model redid them.
- **Revenue is measured against guidance, not consensus.** The free consensus data gives EPS history only.
