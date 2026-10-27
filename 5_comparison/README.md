# 5. The comparison: 19 cybersecurity companies

The same reading and checking, run on a 19-company cybersecurity peer group. Each company gets a page built to the
same template, and one table sets them side by side. There is no ranking and no verdict. This is a dated
snapshot, with prices to the Oct 23, 2026 close (two companies to Oct 26). Analysis, not investment advice.

| | |
|---|---|
| [compare.md](compare.md) | The comparison table, in order of each company's next report |
| [pages/](pages/) | One page per company |
| [figures/](figures/) | One file per company: every figure on its page, with its arithmetic and its sources |
| [reader_brief.md](reader_brief.md) | The release reader's brief as sent, before the company's details are filled in |
| [xbrl.py](xbrl.py) | The SEC's figures by quarter (in full) |

ZS's page follows the same template but draws on its own tables (the rest of this repo): its release rows (`R`, `G`)
are the second-opinion reader's, and the FY26 Q1 guidance, given with the FY25 Q4 results, comes from the original
reader's look-back rows (`CG`).

## Status on Oct 27, 2026

- **Pages:** all 19 are built. The parts that need the release reader say "pending" until it has run.
- **Release reader:** run for 8 of the 19, ZS and the seven companies that report last. Every quote and value passes.
  Against XBRL:
  - PANW 27 matches, OKTA 34, RBRK 34, S 34, SAIL 34, NTSK 27;
  - CRWD 29 matches and 5 differences, from its own revision of earlier quarters (finding 7 below).
- **The other eleven:** ten are read after each one's report. VRNS gets no reader, because it is being acquired; its
  page opens with the deal and shows "pending" where the reader's figures would go.

## Reading a page

Each number has a reference in brackets. Only `P:` references resolve inside this repo; the rest point to private
files.

| Ref | Points to |
|---|---|
| `P:key` | A row of [figures/](figures/)`<T>.csv`, which gives the figure's arithmetic and its own sources |
| `X012` | A row of the company's XBRL table: the SEC's figure, with its concept, accession and form |
| `R012`, `G012` | A row of the release reader's results or guidance table, each quoting its line of the release (samples of the format in [3_readers](../3_readers/README.md)) |
| `CG005` | ZS only: a row of the original release reader's guidance table |
| `D:n`, `E:n` | Line n of the copy of the company's daily prices or earnings history |
| `Y:n` | Line n of the consensus snapshot, as text |
| `V:n` | Line n of the list of 8-K and 6-K events, each with its text file and line |

A script checks every page and every reader table:
- every reference on a page resolves;
- a reader row's quote sits on its cited line, and its value appears in the quote;
- a GAAP figure the reader took from a release matches XBRL within 0.5% (EPS within a cent).

Capital spending is compared by size, because a release prints the payment in brackets while XBRL files it as a
positive number. On Oct 27, every reference on all 19 pages resolved, and ZS's 294 reader rows passed, with 19 XBRL
matches and no differences.

## How a page is built

1. **Fetch and extract**, as for ZS ([1_sources](../1_sources/README.md)). This covers the SEC filings since Jul 1,
   2025 (10-Q, 10-K and 8-K, plus 6-K and 20-F for the two foreign filers), the SEC's lists, a consensus snapshot and
   copies of the company's price and earnings history. Everything then becomes line-numbered text.
2. **The SEC's figures by quarter** ([xbrl.py](xbrl.py)). A quarter filed only as year-to-date is the difference of two
   year-to-date figures, and the row says so. A period filed twice keeps the newest filing's figure. A company with a
   52/53-week year keeps each quarter in its right place.
3. **The events.** Every 8-K and 6-K is listed with its headline. A filing counts as a release by fixed rules, and so
   does the quarter it reports.
4. **The release reader.** The brief is filled in with the company's releases, quarters, period ends and fiscal
   calendar.
   - For the two foreign filers, which file no quarterly XBRL, it asks for every GAAP line.
   - Where goodwill rose by 10%+ of a year's revenue, it lists the filings to search for the acquired revenue.
   - Codex CLI runs it on a clean copy of the text, with plugins, skill search and apps turned off.
5. **The checks** above.
6. **The page script** writes the figures file and the page.
7. **The comparison table**, one figure key per cell.

## How each figure is defined

- **Growth:** revenue filed in XBRL against the same quarter a year earlier.
- **Free cash flow:** operating cash flow less capital spending and capitalized software, over four quarters.
- **Market cap:** the last close times the shares on the cover of the latest report.
- **EV:** market cap less cash and investments, plus debt, at the last balance sheet.
- **Next-twelve-month consensus revenue:** this fiscal year's consensus, less the quarters already reported, plus the
  same quarters a year later, grown at next year's consensus growth. For the foreign filers, quarters are assumed even.
- **Next-twelve-month consensus EPS:** this year's consensus, plus the reported share of the step to next year's (n/4
  when n quarters are reported). It is a step, not a ratio, because EPS can be a loss.
- **Growth without acquisitions:** revenue less the acquired revenue the reader found (or the revenue the company states
  without them), over the revenue a year earlier. So far: PANW +14% in FY26 Q3 against +31% headline, ZS +20% in FY26
  against +25%.
- **Guidance track:** revenue against the top of the range guided the quarter before, in %. Non-GAAP EPS against its
  top is in dollars a share, because a ratio turns a smaller-than-guided loss into a "miss". The "usual beat" is the
  average of the last four; "at the usual beat" adds it to the next guide's top.
- **Full-year guide at the last report:** raised, held or cut against the same year's guide one release earlier.
  - It compares the midpoints, and a move of 0.05% or less counts as held. "First given" means the release before had
    no guide for that year.
  - The page also names any other full-year guide that moved the other way: non-GAAP EPS, operating income or margin,
    ARR, or free cash flow margin.
  - An EPS guide given before a stock split is divided by the split's ratio.
  - Guidance prints as the company gave it, and the consensus beside it prints to the same precision.
- **EPS beats:** earnings-history rows with a positive surprise, computed from unrounded figures. A row that equals the
  quarter's GAAP EPS, and not its non-GAAP EPS, is named on the page.
- **Next-session move:** for a report after the close, the next close over the report-day close. For a report before the
  open, the report-day close over the prior close.
- **Moving averages:** exponential, with weight 2/(n+1), over every close in the copy.

## Fixed on Oct 27, after one page showed the problems

Every page was rebuilt; the old pages differ only as listed.
- **Next-twelve-month revenue** now takes the same quarters a year later, grown at next year's consensus growth. Before,
  it took a flat share of next year's revenue. That overstated growth for growing companies, whose first quarters are
  the smallest: growth fell by up to 5 points (SAIL +23% to +19%, NET +35% to +30%, CRWD +27% to +23%).
- **Next-twelve-month EPS** is now a time-weighted blend of this year's and next year's consensus. Before, it subtracted
  the reported EPS in our earnings data. S's rows there are partly GAAP (finding 8), which had put its P/E at 31x instead of 62x.
- **EPS beats** count positive surprises. The stored two-decimal figures can tie, so CRWD's beats went from 2 of 4 to 4
  of 4.
- **Guidance prints as given**, for example $1.265bn-$1.275bn rather than $1.26bn-$1.27bn. Before, one company's
  consensus looked as if it sat at the top of its full-year guide.
- **The full-year line names the other guides that moved differently.** For SAIL, revenue was held and ARR raised; for
  S, revenue was raised and non-GAAP EPS cut; for NTSK, the free cash flow margin was cut.

## Found while building

1. **Varonis is being bought.** On Oct 15, Proofpoint (owned by Thoma Bravo) agreed to pay $49.75 a share in cash, to
   close in the first half of 2027. The stock trades on the deal, so VRNS gets a deal page and no reader run.
2. **Our own earnings data had the wrong next report date for at least five companies.** The companies' own
   announcements confirm Yahoo's dates for FTNT, GEN, CHKP, RPD and VRNS; our data was off by 1-8 days.
3. **Eleven companies report by about Nov 9, six of them by Oct 29.** Until then, their pages describe the June
   quarter.
4. **Acquisitions flatter two headline growth rates.** PANW's growth jumps from 15-16% to 31-34% once CyberArk is in
   (the deal closed Feb 11, 2026). GEN's falls from 25-27% to 6% once MoneyLion is a year old (closed Apr 17, 2025).
   Goodwill also rose by about a quarter of a year's revenue at CRWD, S, ZS and VRNS.
5. **CrowdStrike split 4-for-1 after the close on Jul 1, 2026.**
   - The price history and the consensus are split-adjusted. XBRL keeps each quarter as filed, so CRWD's XBRL EPS and
     share counts mix the two bases.
   - EPS guides given before the split are divided by 4.
6. **Two foreign filers (CHKP and RDWR) file 20-F and 6-K.** Their quarterly figures exist only in the 6-K releases,
   with no XBRL to check them against.
7. **CrowdStrike revised earlier quarters.** Its FY26 10-K corrected an immaterial error in the timing of stock pay.
   - XBRL now holds revised figures for some quarters and the original figure for one.
   - So the check shows 5 differences, while the release figures are right as published.
   - On the page, four-quarter stock pay is about $14M too low.
8. **Our own earnings data mixes GAAP and non-GAAP rows for S.** Three of its rows match S's GAAP EPS, each set against a
   GAAP consensus; two match the non-GAAP EPS. So S's "2 of the last 4" beats are two non-GAAP beats and two GAAP
   misses. The page and the comparison name the GAAP rows.

## What each page lacks, against ZS's full set

- No call transcripts and no investor-relations files (letters, supplementals, slides). So there is no management
  commentary, no Q&A, and no metric that appears only there.
- No second reading and no hand check: the checks are the scripts.
- No revenue surprise history against consensus. The free consensus data gives EPS history only, so revenue is
  measured against the guidance.
- Risks are what the numbers and the 8-Ks show. The 10-K risk factors are not read.
- A page whose reader has not run shows "pending" for the guidance, the usual beat, the non-GAAP margin, ARR and growth
  without acquisitions.
- The two foreign filers have quarterly numbers from the 6-K text alone. NTSK, listed in Sep 2025, has three quarters of
  guidance history.
- Price dates differ between rows; the comparison's "Prices to" column shows each one.

## Excerpts from the page script

The page script is not published in full, because it also reads our private data files. Four of its rules:

**Next-twelve-month revenue and EPS:**

```python
        if done:                             # the same quarters a year later, grown at next year's consensus growth
            ytd = sum(float(rq[q]["value"]) for q in done)
            ntm = c0y["rev"] - ytd + ytd * c1y["rev"] / c0y["rev"]
# …
        if c0y["eps"] is not None and c1y["eps"] is not None:   # a step, not a ratio: EPS can be a loss
            eps = c0y["eps"] + (c1y["eps"] - c0y["eps"]) * (4 - k) / 4
```

**The guidance track** (a split divides an EPS guide given before it):

```python
            sp = next((s for s in SPLITS.get(sym, []) if filed.get(prev, "") <= s[0] < filed.get(q, "")), None)
            if sp and ehi is not None:
                elo, ehi = (elo / sp[1] if elo is not None else None), ehi / sp[1]
            if hi_ and rv:                   # EPS beat in $ a share: a ratio turns a smaller loss into a "miss"
                track.append(dict(q=q, rev=rv, lo=lo, hi=hi_, beat=rv / hi_ - 1, eps=ev_, elo=elo, ehi=ehi,
                                  ebeat=(ev_ - ehi) if ev_ is not None and ehi is not None else None, split=sp,
                                  refs=[rid, gid] + ([eid, egid] if ev_ is not None and egid else [])))
```

**Raised, held or cut:**

```python
def move(lo, hi, plo, phi):
    """raised, cut or held: a guide's midpoint against the same period's guide one release earlier, within 0.05%."""
    d = (hi if lo is None else (lo + hi) / 2) - (phi if plo is None else (plo + phi) / 2)
    tol = abs(phi if plo is None else (plo + phi) / 2) * 0.0005
    return "raised" if d > tol else "cut" if d < -tol else "held"
```

**EPS beats from the sign of the surprise:**

```python
    if er:                                   # a beat is a positive surprise: the store rounds 0.235 and 0.24 alike
        beats = sum(float(r["surprise_pct"]) > 0 if r["surprise_pct"] else float(r["reported"]) > float(r["estimate"])
                    for _, r in er)
```
