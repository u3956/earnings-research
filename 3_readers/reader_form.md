# The readers' form (v1, as the readers used it)

Three readers, one source each. Each fills fixed CSV tables in its own folder, `readers/<reader>/`.
The tables are what step 3 checks, so the rules below are strict.

## Rules for every table

- **Read only `text/ZS/`**, the line-for-line text of the sources (`extract.py` built it from
  `sources/ZS/`). Do not open the XBRL files: they are the checker's.
- **Every value is cited.** Three columns say where it came from:
  - `text`: the file's path under `text/ZS/`, e.g. `sec/2026-05-26_10-Q_0001713683-26-000096/zs-20260430.htm.txt`
  - `line`: the 1-based line number in that file
  - `quote`: an exact substring of that line, copied character for character (no edits, no "..."), at most
    200 characters, containing the value as printed there.
- **Values** are plain numbers in the `scale` the source uses (`850475` with scale `thousands`), with no
  commas or currency signs. A value in parentheses is negative (`-0.09`). Percentages are numbers with
  unit `%` (`25` for 25%).
- **Never cite a quote that does not contain the value.** If a number has to be computed, it belongs only in
  a table marked *derived*, which points to the rows it uses by `id`.
- **Missing is fine; guessing is not.** List anything not found in `notes.md`.
- Write CSVs with Python's `csv` module (UTF-8, header exactly as below) so quoting is right.
- `notes.md` in each folder: (1) items not found, (2) judgment calls, (3) anything in the sources that looked
  wrong or inconsistent, with its citation.
- Quarters are Zscaler's fiscal quarters: the year ends July 31. FY26Q1 = Aug-Oct 2025, FY26Q2 = Nov 2025-
  Jan 2026, FY26Q3 = Feb-Apr 2026, FY26Q4 = May-Jul 2026, FY27Q1 = Aug-Oct 2026.
- Transcript text is licensed: keep quotes to what the citation needs.

## Filings reader (`readers/filings/`)

Sources: the 10-Qs (FY26Q1-Q3), the 10-K (FY26), and the other 8-Ks (5.07 vote, 5.02 officers, 2.05
restructuring in the 2026-09-03 8-K, 7.01 investor day). Not the press releases (EX-99.1): those are the
release reader's.

### facts.csv

`id,filing,statement,item,member,period_end,duration,value,unit,scale,text,line,quote`

- `id`: F001, F002, ...
- `filing`: FY26Q1, FY26Q2, FY26Q3 (10-Qs) or FY26 (10-K)
- `statement`: income, balance, cashflow, note, cover
- `item`, one of: revenue, cost_of_revenue, gross_profit, rd, sm, ga, total_opex, operating_income,
  interest_income, interest_expense, other_income, pretax_income, tax, net_income, eps_basic, eps_diluted,
  shares_basic, shares_diluted, sbc, depreciation_amortization, amortization_intangibles, restructuring,
  operating_cash_flow, capex_ppe, capitalized_software, acquisitions_cash, buyback, cash,
  short_term_investments, total_assets, goodwill, deferred_revenue_current, deferred_revenue_noncurrent,
  convertible_notes, total_liabilities, stockholders_equity, rpo, rpo_next12m_pct, revenue_geo,
  shares_outstanding_cover, employees
- `member`: `total`, or the breakdown as written (a geography for revenue_geo)
- `period_end`: YYYY-MM-DD the value belongs to (current or prior-year column: take both)
- `duration`: 3M, 6M, 9M, 12M, or instant (balance sheet, RPO, cover)
- `unit`: USD, USD/share, shares, %, count

### changes.csv

`id,filing,kind,change,summary,text,line,quote,prior_filing,prior_text,prior_line,prior_quote`

- What changed in each filing against the one before: FY26Q2 vs FY26Q1, FY26Q3 vs FY26Q2, FY26 10-K vs
  FY26Q3. Plus each 8-K event.
- `kind`: risk_factor, accounting, legal, capital, management, restructuring, acquisition, other
- `change`: added, removed, changed, event
- `summary`: one plain sentence
- `prior_*`: the matching passage in the earlier filing (blank when added or an event)

## Release reader (`readers/release/`)

Sources: the four press releases (8-K EX-99.1), the shareholder letters (FY26Q2-Q4), the FY26Q1 call
presentation, the supplemental financials, "Modeling Considerations for FY26", our earnings-history copy
(`store/earnings_ZS_2026-10-25.csv.txt`, EPS estimate vs reported per report date) and the Yahoo snapshot
(`yahoo/quote_summary_2026-10-25.json.txt`, consensus for FY27Q1, FY27Q2, FY27 and FY28 as of Oct 25).

### results.csv

`id,quarter,item,basis,duration,value,unit,scale,yoy_stated,text,line,quote`

- `id`: R001, ...
- `quarter`: FY26Q1-FY26Q4, or FY26 for full-year rows
- `item`, one of: revenue, gross_margin, operating_income, operating_margin, net_income, eps_diluted, arr,
  arr_growth_ex_acq, net_new_arr, red_canary_arr, fcf, fcf_margin, operating_cash_flow, deferred_revenue,
  rpo, crpo, customers_100k_arr, customers_1m_arr, nrr, gross_retention, cash_and_investments, or
  `other:<name>` for a metric the company reports that is not listed
- `basis`: gaap, non_gaap, kpi
- `yoy_stated`: the growth rate as the source states it, else blank

### guidance.csv

`id,given_in,target_period,item,basis,low,high,unit,scale,growth_stated,text,line,quote`

- `given_in`: the release that gave it (FY26Q1 ... FY26Q4); `target_period`: FY26Q2 ... FY27Q1, FY26, FY27
- `item`: revenue, arr, gross_margin, operating_income, operating_margin, eps_diluted, fcf_margin,
  shares_diluted, tax_rate, red_canary_arr
- a single figure ("approximately 80%") goes in both `low` and `high`
- raised or cut full-year guidance appears once per release that states it

### bridge.csv

`id,quarter,measure,line_item,value,unit,scale,text,line,quote`

- The GAAP to non-GAAP reconciliation in each release
- `measure`: gross_profit, operating_income, net_income, eps_diluted
- `line_item`: gaap, sbc, amortization_intangibles, acquisition_costs, restructuring, debt_amortization,
  tax_adjustment, non_gaap, or `other:<name>`

### consensus.csv

`id,quarter,item,estimate,unit,as_of,text,line,quote`

- EPS estimate before each FY26 report (store copy), and every Yahoo consensus figure for FY27Q1, FY27Q2,
  FY27, FY28 (revenue and EPS: average, low, high, number of analysts)
- `as_of`: the report date (store) or 2026-10-25 (Yahoo)

### compare.csv (derived)

`id,quarter,item,reported_id,guide_id,consensus_id,reported,guide_low,guide_high,consensus,vs_guide,vs_consensus,note`

- Each reported quarter against the guidance given the quarter before and the consensus, where both exist
- `vs_guide`: above, within, below; `vs_consensus`: beat, inline, miss; blank when there is nothing to compare
- Values copied from the rows the ids point to; nothing new

## Call reader (`readers/call/`)

Sources: the official call transcripts (`ir/FY26Qn/ZS-USQ_Transcript_*.pdf.txt`, speakers named),
the investor day (`calls/investor_day_2026-10-06/<part>/transcript.txt.txt`, Whisper with [hh:mm:ss]
stamps, no speaker labels) and the investor day deck (`ir/investor_day_2026-10-06/...pdf.txt`).

### statements.csv

`id,event,speaker,role,topic,kind,value,unit,period,statement,text,line,quote`

- `id`: C001, ...
- `event`: FY26Q1_call, FY26Q2_call, FY26Q3_call, FY26Q4_call, investor_day
- `role`: ceo, cfo, ir, cpo, cro, evp, analyst, operator, other
- `topic`: guidance, arr, revenue, margins, fcf_capex, demand, pricing, products_ai, competition,
  go_to_market, red_canary, macro, capital_allocation, long_term_targets, management, other
- `kind`: number, guidance, claim
- `value`, `unit`, `period`: when a number is said, else blank
- `statement`: one plain sentence

### qa.csv

`id,event,n,analyst,firm,topic,question,answer,answered,why,q_text,q_line,q_quote,a_text,a_line,a_quote`

- Every analyst question on the four calls and the investor day panel, in order (`n`)
- `answered`: direct, partial, dodged; `why`: one line when partial or dodged (what was asked and not said)

### wording.csv

`id,topic,from_event,to_event,from_text,from_line,from_quote,to_text,to_line,to_quote,change,note`

- How management's wording on the same topic moved from one call to the next (FY26Q2 to Q3, Q3 to Q4, Q4
  to the investor day), e.g. demand, guidance tone, Red Canary, margins, FCF and capex, sales leadership
- `change`: stronger, weaker, new, dropped, same
