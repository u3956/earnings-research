# Error log

This log records every issue identified during the Zscaler work. Part 1 covers errors made by the AI agents; part 2
covers errors found in the sources, including the in-house tools. Line numbers refer to the private text copies.

## Summary after both verification passes

| | Entries | Incorrect figures | Entries needing correction |
|---|---|---|---|
| Filings: facts and changes | 592 | 0 | 0 |
| Release tables (original / independent extraction) | 422 / 556 | 0 / 0 | 0 / 0; both omitted 6 product and customer metrics |
| Call statements | 720 | 0 | 9 overstatements of wording or period |
| Q&A and wording | 124 | 0 | 4, plus 4 borderline answered/dodged grades |

The review agents were themselves wrong on 2 of their 17 flags, and on one further claim.

## 1. Errors made by the agents

**Detectable by script: none.** Every quote sits on its cited line, every value appears within its quote, and no filed
figure is contradicted by XBRL ([verification](README.md)).

**Not detectable by script:**

1. **The independent extraction models omitted what the brief did not list.** Neither recorded any of the 12 product
   metrics that the original reader found in the letters' prose, among them Zero Trust Everywhere enterprises, Z-Flex
   bookings, AI Security ARR and Data Security ARR. The brief named specific metrics, and both models kept strictly to
   that list. The revised table definitions name every metric.
2. **One model missed the Q1 guidance**, reporting that it was not in the sources; it is restated in the Q1 call
   presentation. The original reader recorded it under the preceding quarter, which the table definitions did not
   allow, and the other model found it but left it in its notes. The revised definitions provide for it.
3. **One model recorded 25 "—" cells as 0.** This is a convention rather than an incorrect figure; the revised
   definitions exclude such cells.
4. **Format departures.** The call reader has no scale column and records a guidance range as two entries. Two readers
   saved their helper scripts outside their own folders.
5. **Self-checks were unverified claims.** Each reader reported that it had re-checked its quotes; the script now
   confirms this independently.
6. **Overstatement was the call reader's one recurring error.** The second pass found 13 of 844 entries to correct,
   none involving an incorrect figure: a dropped qualifier, a part presented as the whole, an inference presented as a
   statement, three periods that management had not given, and one retained mishearing. Examples are on the
   [transcripts page](../2_transcripts/README.md#verification), and every original and revised value is in
   [corrections.csv](corrections.csv).
7. **The review agents also made errors.** Two of their 17 flags were wrong:
   - one read the CFO's restatement of the full-year figure (9.5%) in the Q&A as a new Q4-only figure;
   - one attributed the chief revenue officer's own arithmetic to the reader.

   One agent also stated that a name appears in no source, when it appears in five files. Every flag is verified
   against the source before it is accepted.
8. **Completeness gaps followed the table definitions.** Six outlook items were left out of the release tables because
   the first version had no entry for them, although both release extractions had found and noted them:
   - FY27 capital expenditure at "low teens" % of revenue;
   - $30-33M of restructuring;
   - the Red Canary revenue guidance, and its net new ARR guidance by quarter;
   - the timing of net new ARR (15% of FY27's in Q1);
   - net other income.

   Both also missed six metrics mentioned once in the letters: two bookings figures, total customers, $10M+ customers,
   the Fortune 500 share and Z-Flex bookings growth. The revised definitions name all twelve.

## 2. Errors found in the sources

### Data that changed or was misreported

- **Two downloads of the same SEC data disagreed.** EDGAR acceptance times for ZS, and for three other companies, were
  four hours late in copies taken on Oct 12, exactly the offset between UTC and New York time. A fresh download on
  Oct 25 matched the release times, shortly after the market close. Every file therefore records its retrieval time
  and checksum.
- **A web search summary presented the ARR guidance as revenue:** the FY27 range of $4.396-4.426B is ARR; revenue
  guidance is $3.908-3.938B.

### In-house tools

- **Whisper misheard the total market:** the in-house investor-day transcript reads $20 billion where the presentation
  shows $220B.
- **The in-house earnings data mixes rounded and unrounded estimates.** EPS estimates are stored to two decimals, but
  the surprise percentage is computed from unrounded figures: 12.56% reported, against 12.2% from the stored figures.

### Transcripts and management's figures

These are listed once, on the
[transcripts page](../2_transcripts/README.md#errors-in-the-transcripts-and-in-managements-figures):
- the official Q4 transcript attributes to the CFO an answer to a question put to the CEO, and contains misheard words;
- the in-house transcripts mishear figures and names, and lose a year;
- management restated metrics between calls and presentations without reconciliation (AI Security ARR, Data Security
  ARR, the size of the target market, one customer's figures);
- the chief revenue officer's "5x" works out to about 4x.

### The company's own documents

- **Per-share guidance printed in millions:** "$3.78 to $3.82 million" (Q2 release) and "$3.99 to $4.02 million" (Q3).
- **The Q2 supplemental spreadsheet contains several errors.**
  - Its "YTD" columns sum the wrong three quarters: 2,323,089 thousand against the release's 1,603,863.
  - It contains `#REF!` cells and two share counts for one quarter.
  - Its ARR row is in dollars under an "(in millions)" header.
- **The Q4 release dropped the Red Canary clause from its ARR definition**, which the Q4 letter and supplemental still
  carry.
- **The Q4 letter's footnotes do not match the release.** They label quarterly stock-based compensation amounts as
  fiscal years and omit FY25's $33.1M.
- **The Q3 letter states that gross margin "Exceeded" guidance in one place and was "in-line" in another.**
- **The filings are internally inconsistent.**
  - The SquareX acquisition is "approximately $113.0 million" in one place and $112.8M in another.
  - The Symmetry acquisition is $175.0M in one place, against $152.9M in cash plus $16.9M in stock ($169.8M) in
    another.
  - A per-share option value is printed as "$118.8 million".
  - The Q1 10-Q carries a stale quarter.
  - The 10-K still gives the headquarters as San Jose.
- **The Q4 supplemental's Key Metrics sheet heads its first column "Q4 FY23"**, although the series starts at FY25.

The 19-company peer comparison found further issues of the same kind, from an acquisition that doubles a growth rate
to a stock split that mixes two bases in the SEC's data ([5_comparison](../5_comparison/README.md#findings)).
