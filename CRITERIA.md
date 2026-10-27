# Criteria and rationale

This document sets out the rules applied at each stage of the workflow. Each rule states the practice, the reason for
it and, where relevant, the issue it identified. The folders document the work; this page documents the method.

## 1. Sources

**1.1 Primary sources only.** All figures are taken from documents published by the company or filed with the SEC:
filings, earnings releases, shareholder letters, presentations, supplemental financials and call transcripts. Web
summaries and vendor restatements are not used. Analyst consensus is the only external input and is stored as a dated
snapshot.
*Rationale:* a web search summary presented the FY27 ARR guidance ($4.396-4.426B) as revenue guidance. Revenue
guidance was $3.908-3.938B.

**1.2 Each source is relied on for what it does best.**

| Source | Relied on for |
|---|---|
| 10-Q and 10-K | Filed figures, verified against the filing's XBRL data (the machine-readable version of the financial statements filed with the SEC) |
| Earnings release (8-K exhibit) | Quarterly results and guidance as stated by the company |
| Shareholder letters, presentations, supplementals | Information not in the filings or the release: ARR detail, product and customer metrics, guidance restated for earlier quarters, the timing of new business |
| Official call transcripts | Management commentary and speaker attribution |
| In-house transcripts | Timestamps, and a cross-check on the official text. Where only a recording exists (the investor day), the in-house transcript is the text of record, and the presentation settles any disputed figure |
| Analyst consensus | Estimates as of a stated date, never combined with reported figures |

**1.3 Exact table figures over rounded headlines.** An entry takes $850,475 thousand from the income statement rather
than "$850.5 million" from the headline, unless no table reports the figure.
*Rationale:* headline figures are rounded, and only table figures can be matched exactly to XBRL.

**1.4 Sources are kept as retrieved.** Each file is retrieved once and logged with its URL, retrieval time (UTC), size
and checksum. A filing already stored is never downloaded again. The SEC's filing index and XBRL data are saved as new
dated files on every run.
*Rationale:* two downloads of the same SEC data disagreed. Copies of the filing index taken two weeks earlier showed
acceptance times four hours later than a fresh download, exactly the offset between UTC and New York time. Whatever the
cause, a copy can differ from the next download, so every file records when it was retrieved.

## 2. Transcripts

**2.1 Two transcripts of the same call.** The official transcript of each call is taken from the company's investor
relations site. The Q4 call was also transcribed in-house from the replay.
*Rationale:* the official text has no timestamps and can contain errors; the in-house text has timestamps and can
contain different errors. Comparing the two identified errors in both (see the [error log](4_checks/ERRORS.md)).

**2.2 In-house transcription follows a fixed procedure.** Whisper large-v3 runs on a local GPU, with English forced and
a list of the company's own spellings of its products, executives and acquisitions. Every line keeps its timestamp. The
six recorded sections of the investor day (3 hours 27 minutes) exist only as recordings, so the in-house transcript is
their only text.

**2.3 Speaker attribution.** Speakers are taken from the official transcript's labels, and a script checks that the
label above every cited line matches the entry (642 of 642). The in-house transcripts carry no labels; there, the
speaker is inferred from introductions and section titles, and the reader's notes record how.

**2.4 Quotation is limited to what a citation requires.** The official transcripts are licensed, so an entry quotes a
phrase rather than a passage, and this repository publishes only a few lines.

## 3. Citations

**3.1 Every value carries its own evidence.** Three fields record where a figure came from:
- the file;
- the line number in that file, counting from 1;
- a verbatim quote from that line, copied character for character (no edits, no ellipses), at most 200 characters
  long, containing the value as printed.

*Rationale:* a script can then locate every figure without judgment, and a reviewer can open the exact line.

**3.2 Every source is first converted to line-numbered text.** One line per table row (cells joined by " | ") or per
paragraph, with markers for each PDF page and spreadsheet sheet.
*Rationale:* a citation requires stable line numbers, and a reviewer needs the page or sheet.

**3.3 Computed figures are kept separate.** Because a quote must contain its value, a figure that has to be calculated
goes only into a table marked *derived*, which references the entries it was computed from.

**3.4 Gaps are recorded, not filled.** Each reader keeps notes in three parts: what it could not find, the judgment
calls it made, and anything in the sources that appeared wrong, each with a citation.

## 4. Table definitions

The table definitions specify the tables each reader completes: their columns, the values allowed in each column, the
units and the citation rules. There are two versions:
- [reader_form.md](3_readers/reader_form.md), the version used for this report;
- [reader_form_revised.md](3_readers/reader_form_revised.md), revised after verification for the next report.

**4.1 Values as printed, in the source's own scale.** Scale is one of ones, thousands, millions or billions. A value in
parentheses is negative, and a percentage is recorded as a plain number with the unit "%".

**4.2 The company's fiscal calendar.** Every entry carries a fiscal quarter or year (Zscaler's fiscal year ends July 31).
A figure restated in a later document is recorded under the period it belongs to.
*Issue identified:* the readers found the Q1 guidance restated in a look-back table and had no place to record it; the
revised definitions allow it.

**4.3 A dash means nothing was reported.** A cell printed "—" produces no entry.
*Issue identified:* one of the independent extraction models (rule 5.5) recorded 25 such cells as 0.

**4.4 Scope.** Recorded:
- reported results;
- guidance;
- reconciliations from GAAP to non-GAAP;
- consensus;
- changes in each filing against the previous one (risk factors, accounting, management, acquisitions);
- management commentary on each call;
- every analyst question, with how fully it was answered;
- changes in management's wording on the same topic from one call to the next.

Not recorded:
- XBRL data, which serves as the verification reference and is therefore withheld from the readers;
- most customer anecdotes;
- anything not present in the line-numbered text.

**4.5 Everything required is named explicitly.** The revised definitions name every product and customer metric, the
year-to-date columns and the additional lines of each statement.
*Rationale:* both independent extraction models (rule 5.5) followed the brief's list literally. They omitted 12 product
metrics that the letters reported but the brief did not name.

## 5. Extraction agents

**5.1 One reader per source group.** The filings, the earnings materials and the calls each have their own agent and
brief. The briefs are kept exactly as sent.

**5.2 No corrections before verification.** The tables pass a format check (headers, identifiers, allowed values,
citations present) and nothing more.
*Rationale:* the measured error rate is then the readers' own. Where a reader departed from its brief, the departure is
documented and left in place.

**5.3 Every analyst question is graded on a fixed scale:**
- *direct*: the specific request was addressed;
- *partial*: one part, or the figure requested, was missing;
- *dodged*: the specific request was not addressed, and the entry states what was asked and not answered.

Of 81 questions, 43 were answered directly, 33 partially and 5 were dodged.

**5.4 Wording is tracked between consecutive events on fixed topics:** demand, guidance tone, the acquisition,
margins, cash flow and capital expenditure, sales leadership, and AI. Each change is classified as stronger, weaker,
new, dropped or unchanged.

**5.5 Independent extraction of the earnings release.** Two other models repeated the release extraction from the same
brief, and a script scored all three. All three were exact on every citation and on the filed figures, differing only
in rounding. The most complete recorded 231 result entries against 127, but omitted what the brief did not name
(rule 4.5).

## 6. Verification

**6.1 Scripted checks on every entry.** A script confirms that:
- every quote appears exactly on its cited line;
- every value appears within its quote;
- no quote exceeds 200 characters;
- every filed figure matches the filing's XBRL data;
- the derived table recomputes.

*Result:* 1,983 of 1,983 quotes and 1,452 of 1,452 values confirmed; 562 filed figures matched, none contradicted.

**6.2 A second scripted pass for what the first cannot detect.** It checks that:
- each reconciliation adds up within the rounding of its printed terms;
- stated margins and free cash flow recompute;
- an entry cited on a line with several figures took the correct column;
- each consensus figure sits under the correct period and field;
- each filing change was genuinely added, removed or changed.

Two errors were planted deliberately (a shifted value and a mislabeled period), and the sums caught both.

**6.3 Review agents for judgment-based entries.** Every transcript-based entry and every filing change (904 entries)
was re-read against its source text, looking for a wrong item or period, an unfair summary or a dropped qualifier.
*Rule:* every flag is verified against the source before it is accepted.
*Result:*
- 17 flags: 13 entries corrected, 2 left unchanged, 2 flags incorrect.
- None of the 13 corrections changed a figure.

**6.4 Corrections are logged.** Every corrected field keeps its original value
([corrections.csv](4_checks/corrections.csv)). Four borderline answered/dodged grades were left unchanged after manual
review.

**6.5 A manual sample where the scripts cannot reach.** Thirty figures are drawn with a fixed random seed, so the same
sample can be reproduced.
- They are drawn only from entries the scripts could not confirm against XBRL, across the filings, release and call
  tables.
- Each was checked in the original document, at its PDF page, sheet or timestamp, for the correct item, period, basis
  and column.

*Result:* 30 of 30 correct ([hand_check_30.csv](4_checks/hand_check_30.csv)).

**6.6 A single error log.** Errors made by the agents and errors found in the sources are recorded together, each with
its citation and how it was detected.

## 7. Peer comparison

**7.1 A common template and no ranking.** All 19 companies in the cybersecurity peer group receive the same one-page
template and the same columns. They are not ranked.

**7.2 Every figure shows its calculation.** Each figure on a profile references a row of the company's figures file,
which gives the calculation and the source lines used.
- Growth is revenue filed in XBRL against the same quarter a year earlier.
- Free cash flow is operating cash flow less capital expenditure and capitalized software, over four quarters.
- A revenue beat is measured against the top of the range guided the previous quarter, in %. An EPS beat is measured in
  dollars per share, because a ratio turns a smaller-than-guided loss into a "miss".
- Full-year guidance counts as raised or cut when its midpoint moved by more than 0.05%, and as held otherwise.

The full set of definitions is in the [comparison README](5_comparison/README.md).

**7.3 Rules are corrected when a profile exposes a flaw.** On Oct 27, one company's profile revealed problems, so the
rules were changed and every profile rebuilt:
- Next-twelve-month revenue now takes the same quarters a year later, grown at next year's consensus growth rate. The
  previous flat share overstated growth by up to 5 points.
- Next-twelve-month EPS is now a time-weighted blend of the current and next year's consensus.
- EPS beats are counted from the sign of the reported surprise, because the stored two-decimal figures can tie.
- Guidance is printed exactly as the company gave it.
- The full-year line also names any other full-year guidance that moved differently from revenue, for example ARR
  raised while revenue was held.

## 8. Limitations

- **One company, one year of reports.** The rules held up here; that does not establish that they hold generally.
- **Independent extraction covered the release reader only.** The call reader's tables were checked by the review
  agents and by the manual sample, but were not repeated by a second model.
- **Revenue is measured against guidance, not consensus.** The free consensus data provides EPS history only.
