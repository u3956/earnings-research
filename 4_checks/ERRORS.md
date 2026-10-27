# What the agents and the sources got wrong

Part 1 is the agents' own mistakes. Part 2 is what the agents found wrong in the sources, including our own tools.
Line numbers refer to the private text copies.

## After both checks, in one table

| | Rows | Wrong numbers | Rows needing a fix |
|---|---|---|---|
| Filings: facts and changes | 592 | 0 | 0 |
| Release tables (original / second opinion) | 422 / 556 | 0 / 0 | 0 / 0; both missed 6 product and customer metrics |
| Call statements | 720 | 0 | 9 overstatements of wording or period |
| Q&A and wording | 124 | 0 | 4, plus 4 borderline answered/dodged labels |

The checker agents were wrong on 2 of their 17 flags, and on one side claim.

## 1. The agents' mistakes

**What a script can see: nothing.** Every quote sits on its cited line, every value is inside its quote, and no filed
figure is contradicted by XBRL ([the checks](README.md)).

**What the scripts cannot see:**

1. **The other models skipped what the brief did not list.** Both second-opinion models recorded none of the 12
   product metrics that the original reader found in the letters' prose: Zero Trust Everywhere enterprises, Z-Flex
   bookings, AI Security ARR, Data Security ARR and others. The brief named specific metrics, and they kept to that
   list. The revised form now names every metric.
2. **One missed the Q1 guidance.** It said the guidance was not in the sources; it is reprinted in the Q1 call slides.
   The original reader recorded it under the quarter before, which the form did not allow. The other model found it
   but left it in its notes. The revised form allows it.
3. **One wrote 25 "—" cells as 0.** That is a convention, not a wrong number. The revised form says to leave such
   cells out.
4. **Format departures.** The call reader has no scale column and writes a guidance range as two rows. Two readers
   saved their helper scripts outside their own folders.
5. **The self-checks were claims.** Each reader said it had re-checked its quotes. The script now confirms it.
6. **Overstatement is the call reader's one habit.** The second pass found 13 rows to fix out of 844, and no number was
   wrong: a dropped hedge, a part written as a whole, an inference written as if it had been said, three quarters that
   nobody gave, and one kept mishearing. The examples are on the
   [transcripts page](../2_transcripts/README.md#how-they-were-checked), and every old and new value is in
   [corrections.csv](corrections.csv).
7. **The checker agents made mistakes too.** Two of their 17 flags were wrong:
   - one read the CFO restating the full-year figure (9.5%) in the Q&A as a new, Q4-only figure;
   - one blamed the reader for the sales chief's own arithmetic.

   One agent also said a name appears in no source, when it is in five files. Every flag needs a look at the source
   before it counts.
8. **Completeness gaps follow the form.** Six outlook items were left out of the release tables because the first form
   had no row for them, although both readers had found them and noted them:
   - FY27 capital spending at "low teens" % of revenue;
   - $30-33M of restructuring;
   - the Red Canary revenue guidance, and its net new ARR guidance by quarter;
   - the timing of net new ARR (15% of FY27's in Q1);
   - net other income.

   Both readers also missed six metrics that the letters mention once: two bookings figures, total customers, $10M+
   customers, the Fortune 500 share, and Z-Flex bookings growth. The revised form names all twelve.

## 2. What the agents found wrong in the sources

### Data that changed, or was summarized wrongly

- **Two downloads of the same SEC data disagreed.** EDGAR's acceptance times for ZS, and for three other companies,
  read four hours late in copies taken on Oct 12, exactly the gap between UTC and New York time. A fresh download on
  Oct 25 fit the releases, just after the close. So every file here carries its fetch time and checksum.
- **A web search summary called the ARR guidance "revenue":** FY27 $4.396-4.426B is ARR; revenue is guided to
  $3.908-3.938B.

### Our own tools

- **Whisper misheard the total market**: our investor-day transcript says $20 billion where the deck shows $220B.
- **Our own earnings data mixes rounded and unrounded estimates.** EPS estimates are kept to two decimals, but the
  surprise percentage comes from the unrounded ones: 12.56% shown, 12.2% from the stored figures.

### The transcripts, and management's own numbers

Listed once, on the [transcripts page](../2_transcripts/README.md#what-the-transcripts-got-wrong):
- the official Q4 transcript credits the CFO with an answer to a question put to the CEO, and mishears words;
- our own transcripts mishear numbers and names and lose a year;
- management restated metrics between calls and slides without a bridge (AI Security ARR, Data Security ARR, the size
  of the target market, one customer's figures);
- the sales chief's "5x" works out to about 4x.

### The company's own documents

- **Per-share guidance printed as millions:** "$3.78 to $3.82 million" (Q2 release) and "$3.99 to $4.02 million" (Q3).
- **The Q2 supplemental spreadsheet is broken.**
  - Its "YTD" columns add up the wrong three quarters: 2,323,089 thousand against the release's 1,603,863.
  - It has `#REF!` cells, and two share counts for one quarter.
  - Its ARR row is in dollars under an "(in millions)" header.
- **The Q4 release dropped the Red Canary clause from its ARR definition**, while the Q4 letter and supplemental still
  carry it.
- **The Q4 letter's footnotes don't match the release.** They label quarterly stock-pay amounts as fiscal years and
  leave out FY25's $33.1M.
- **The Q3 letter says gross margin "Exceeded" guidance in one place, and was "in-line" in another.**
- **The filings disagree with themselves.**
  - The SquareX deal is "approximately $113.0 million" in one place and $112.8M in another.
  - The Symmetry deal is $175.0M in one place, against $152.9M cash plus $16.9M of stock ($169.8M) in another.
  - A per-share option value is printed as "$118.8 million".
  - The Q1 10-Q carries a stale quarter.
  - The 10-K still gives the headquarters as San Jose.
- **The Q4 supplemental's Key Metrics sheet heads its first column "Q4 FY23"**, where the sheet's series starts at FY25.

The comparison of 19 companies found more of the same kind, from an acquisition that doubles a growth rate to a stock
split that mixes two bases in the SEC's data ([5_comparison](../5_comparison/README.md#found-while-building)).
