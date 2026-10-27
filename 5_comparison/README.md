# 5. Peer comparison: 19 cybersecurity companies

The same extraction and verification, applied in reduced form to a 19-company cybersecurity peer group. Each company
receives a one-page profile built to a common template, and a single table compares them. The companies are not ranked
and no recommendation is made. This is a dated snapshot, with prices to the Oct 23, 2026 close (Oct 26 for two
companies). For research purposes only; not investment advice.

| | |
|---|---|
| [compare.md](compare.md) | The comparison table, ordered by each company's next report date |
| [pages/](pages/) | One profile per company |
| [figures/](figures/) | One file per company: every figure on its profile, with its calculation and sources |
| [reader_brief.md](reader_brief.md) | The release reader's brief as sent, before the company-specific details are filled in |
| [xbrl.py](xbrl.py) | Quarterly figures from the SEC's XBRL data (published in full) |

The ZS profile follows the same template but draws on the full set of tables in this repository: its release entries
(`R`, `G`) come from the independent extraction, and the FY26 Q1 guidance, issued with the FY25 Q4 results, comes from
the original release reader's look-back entries (`CG`).

## Status as of Oct 27, 2026

- **Profiles:** all 19 are built. Sections that depend on the release reader show "pending" until it has run.
- **Release reader:** run for 8 of the 19 (ZS and the seven companies that report last). Every quote and value passes.
  Against XBRL:
  - PANW 27 matches, OKTA 34, RBRK 34, S 34, SAIL 34, NTSK 27;
  - CRWD 29 matches and 5 differences, resulting from the company's revision of earlier quarters (finding 7 below).
- **The remaining eleven:** ten are read after each company's next report. VRNS receives no reader run because it is
  being acquired; its profile opens with the transaction and shows "pending" where the reader's figures would appear.

## Reading a profile

Each figure carries a bracketed reference. Only `P:` references resolve within this repository; the others point to
private files.

| Reference | Points to |
|---|---|
| `P:key` | A row of [figures/](figures/)`<T>.csv`, giving the figure's calculation and its own sources |
| `X012` | A row of the company's XBRL table: the SEC's figure, with its concept, accession number and form |
| `R012`, `G012` | A row of the release reader's results or guidance table, each quoting its line of the release (sample format in [3_readers](../3_readers/README.md)) |
| `CG005` | ZS only: a row of the original release reader's guidance table |
| `D:n`, `E:n` | Line n of the copy of the company's daily prices or earnings history |
| `Y:n` | Line n of the consensus snapshot, as text |
| `V:n` | Line n of the list of 8-K and 6-K events, each with its text file and line |

A script verifies every profile and every reader table:
- every reference on a profile resolves;
- each reader entry's quote sits on its cited line, and its value appears in the quote;
- each GAAP figure taken from a release matches XBRL within 0.5% (EPS within one cent).

Capital expenditure is compared in absolute value, because a release prints the payment in parentheses while XBRL
files it as a positive number. On Oct 27, every reference on all 19 profiles resolved, and ZS's 294 reader entries
passed, with 19 XBRL matches and no differences.

## How a profile is built

1. **Collection and conversion**, as for ZS ([1_sources](../1_sources/README.md)): SEC filings since Jul 1, 2025
   (10-Q, 10-K and 8-K, plus 6-K and 20-F for the two foreign filers), the SEC's filing index and XBRL data, a
   consensus snapshot, and copies of the company's price and earnings history, all converted to line-numbered text.
2. **Quarterly XBRL figures** ([xbrl.py](xbrl.py)). A quarter filed only on a year-to-date basis is derived as the
   difference of two year-to-date figures, and the row says so. A period filed twice keeps the most recent filing's
   figure. Companies with a 52/53-week year keep each quarter in its correct position.
3. **Events.** Every 8-K and 6-K is listed with its headline. Fixed rules determine which filings are earnings releases
   and which quarter each one reports.
4. **Release extraction.** The brief is completed with the company's releases, quarters, period ends and fiscal
   calendar.
   - For the two foreign filers, which file no quarterly XBRL, it requests every GAAP line.
   - Where goodwill rose by 10% or more of a year's revenue, it lists the filings to search for acquired revenue.
   - Codex CLI runs it on a clean copy of the text, with plugins, skill search and apps disabled.
5. **Verification**, as described above.
6. **Profile generation:** a script writes the figures file and the profile.
7. **Comparison table:** one figure key per cell.

## Definitions

- **Growth:** revenue filed in XBRL against the same quarter a year earlier.
- **Free cash flow:** operating cash flow less capital expenditure and capitalized software, over four quarters.
- **Market capitalization:** the last close multiplied by the shares reported on the cover of the latest periodic
  report.
- **Enterprise value:** market capitalization less cash and investments, plus debt, at the latest balance sheet.
- **Next-twelve-month consensus revenue:** the current fiscal year's consensus, less the quarters already reported,
  plus the same quarters a year later grown at next year's consensus growth rate. For the foreign filers, quarters are
  assumed equal.
- **Next-twelve-month consensus EPS:** the current year's consensus plus the elapsed share of the step to next year's
  (n/4 when n quarters have been reported). A step rather than a ratio is used because EPS can be negative.
- **Organic growth** (revenue growth excluding acquisitions): revenue less the acquired revenue identified by the reader
  (or the revenue the company reports excluding acquisitions), over revenue a year earlier. To date: PANW +14% in FY26
  Q3 against +31% reported, ZS +20% in FY26 against +25%.
- **Guidance track:** revenue against the top of the range guided the previous quarter, in %. Non-GAAP EPS against the
  top of its range is measured in dollars per share, because a ratio turns a smaller-than-guided loss into a "miss".
  The "usual beat" is the average of the last four; "at the usual beat" adds it to the top of the next guidance range.
- **Full-year guidance at the latest report:** raised, held or cut against the same year's guidance one release
  earlier.
  - Midpoints are compared, and a move of 0.05% or less counts as held. "First given" means the previous release gave
    no guidance for that year.
  - The profile also names any other full-year guidance that moved in the opposite direction: non-GAAP EPS, operating
    income or margin, ARR, or free cash flow margin.
  - EPS guidance issued before a stock split is divided by the split ratio.
  - Guidance is printed as the company gave it, and the consensus alongside it is printed to the same precision.
- **EPS beats:** earnings-history rows with a positive surprise, computed from unrounded figures. A row that equals the
  quarter's GAAP EPS rather than its non-GAAP EPS is identified on the profile.
- **Next-session move:** for a report after the close, the next close over the report-day close; for a report before
  the open, the report-day close over the prior close.
- **Moving averages:** exponential, with weight 2/(n+1), over every close in the copy.

## Corrections made on Oct 27

One profile exposed problems in the rules, so the rules were corrected and every profile rebuilt; earlier versions
differ only as listed.
- **Next-twelve-month revenue** now uses the same quarters a year later, grown at next year's consensus growth rate. It
  previously took a flat share of next year's revenue, which overstated growth for growing companies, whose first
  quarters are the smallest: growth fell by up to 5 points (SAIL +23% to +19%, NET +35% to +30%, CRWD +27% to +23%).
- **Next-twelve-month EPS** is now a time-weighted blend of the current and next year's consensus. It previously
  subtracted the reported EPS in the in-house earnings data. S's rows there are partly GAAP (finding 8), which had put
  its P/E at 31x instead of 62x.
- **EPS beats** count positive surprises. The stored two-decimal figures can tie, so CRWD's beats went from 2 of 4 to
  4 of 4.
- **Guidance is printed as given**, for example $1.265bn-$1.275bn rather than $1.26bn-$1.27bn. Previously one
  company's consensus appeared to sit at the top of its full-year guidance.
- **The full-year line names other guidance that moved differently.** For SAIL, revenue was held and ARR raised; for
  S, revenue was raised and non-GAAP EPS cut; for NTSK, the free cash flow margin was cut.

## Findings

1. **Varonis is being acquired.** On Oct 15, Proofpoint (owned by Thoma Bravo) agreed to pay $49.75 per share in
   cash, with closing expected in the first half of 2027. The stock trades on the deal terms, so VRNS has a transaction
   profile and no reader run.
2. **The in-house earnings data had the wrong next report date for at least five companies.** The companies' own
   announcements confirm Yahoo's dates for FTNT, GEN, CHKP, RPD and VRNS; the in-house data was off by 1-8 days.
3. **Eleven companies report by about Nov 9, six of them by Oct 29.** Until then, their profiles describe the June
   quarter.
4. **Acquisitions inflate two headline growth rates.** PANW's growth rises from 15-16% to 31-34% once CyberArk is
   included (the deal closed Feb 11, 2026). GEN's falls from 25-27% to 6% once MoneyLion is a year old (closed
   Apr 17, 2025). Goodwill also rose by about a quarter of a year's revenue at CRWD, S, ZS and VRNS.
5. **CrowdStrike split 4-for-1 after the close on Jul 1, 2026.**
   - The price history and the consensus are split-adjusted. XBRL keeps each quarter as filed, so CRWD's XBRL EPS and
     share counts mix the two bases.
   - EPS guidance issued before the split is divided by 4.
6. **Two foreign filers (CHKP and RDWR) file 20-F and 6-K.** Their quarterly figures exist only in the 6-K releases,
   with no XBRL to verify them against.
7. **CrowdStrike revised earlier quarters.** Its FY26 10-K corrected an immaterial error in the timing of stock-based
   compensation.
   - XBRL now holds revised figures for some quarters and the original figure for one.
   - The check therefore shows 5 differences, while the release figures are correct as published.
   - On the profile, four-quarter stock-based compensation is about $14M too low.
8. **The in-house earnings data mixes GAAP and non-GAAP rows for S.** Three of its rows match S's GAAP EPS, each set
   against a GAAP consensus; two match its non-GAAP EPS. S's "2 of the last 4" beats are therefore two non-GAAP beats
   and two GAAP misses. The profile and the comparison identify the GAAP rows.

## Limitations against the full ZS set

- No call transcripts and no investor-relations materials (letters, supplementals, presentations), and therefore no
  management commentary, no Q&A and no metric reported only there.
- No independent extraction and no manual sample: verification is by script only.
- No revenue surprise history against consensus. The free consensus data provides EPS history only, so revenue is
  measured against guidance.
- Risks are limited to what the figures and the 8-Ks show; the 10-K risk factors are not read.
- A profile whose reader has not run shows "pending" for guidance, the usual beat, the non-GAAP margin, ARR and organic
  growth.
- The two foreign filers' quarterly figures come from the 6-K text alone. NTSK, listed in Sep 2025, has three quarters
  of guidance history.
- Price dates differ between companies; the comparison's "Prices to" column shows each one.

## Excerpts from the profile script

The profile script is not published in full, because it also reads private data files. Four of its rules:

**Next-twelve-month revenue and EPS:**

```python
        if done:                             # the same quarters a year later, grown at next year's consensus growth
            ytd = sum(float(rq[q]["value"]) for q in done)
            ntm = c0y["rev"] - ytd + ytd * c1y["rev"] / c0y["rev"]
# …
        if c0y["eps"] is not None and c1y["eps"] is not None:   # a step, not a ratio: EPS can be a loss
            eps = c0y["eps"] + (c1y["eps"] - c0y["eps"]) * (4 - k) / 4
```

**Guidance track** (a stock split divides EPS guidance issued before it):

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
