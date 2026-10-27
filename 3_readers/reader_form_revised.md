# The readers' form, revised (v2, for the next report)

v1 (`reader_form.md`) is the form the readers used, kept as it was. v2 adds what the checks and the second-opinion
test showed a reader needs spelled out. A model follows a list exactly, so this file names
everything. Changes from v1 are marked **(v2)**.

## Rules for every table

- **Read only `text/ZS/`**, the line-for-line text of the sources (`extract.py` built it from
  `sources/ZS/`). The one file you may also read under `sources/` is `sources/ZS/filings.csv`, the list of
  filings with their fiscal quarter. **(v2)** Do not open the XBRL files.
- **Every value is cited.** Three columns say where it came from:
  - `text`: the file's path under `text/ZS/`
  - `line`: the 1-based line number in that file
  - `quote`: an exact substring of that line, copied character for character (no edits, no "..."), at most
    200 characters, containing the value as printed there.
- **Values** are plain numbers in the `scale` the source uses, with no commas or currency signs. A value in
  parentheses is negative. Percentages are numbers with unit `%`.
- **`scale` is one of `ones`, `thousands`, `millions`, `billions`.** **(v2)**
- **A cell printed "—" is nil: leave it out (no row).** **(v2)**
- **Take the exact figure from the financial tables** (e.g. `$850,475` thousands) rather than a rounded
  headline (`$850.5 million`). Use the headline only when no table prints the figure. **(v2)**
- **Never cite a quote that does not contain the value.** A computed number belongs only in a table marked
  *derived*, which points to the rows it uses by `id`.
- **Missing is fine; guessing is not.** List anything not found in `notes.md`.
- Write CSVs with Python's `csv` module (UTF-8, header exactly as below).
- `notes.md` in each folder: (1) items not found, (2) judgment calls, (3) anything in the sources that looked
  wrong or inconsistent, with its citation.
- Quarters are Zscaler's fiscal quarters; the year ends July 31. FY27Q1 = Aug-Oct 2026, FY27Q2 = Nov 2026-
  Jan 2027, FY27Q3 = Feb-Apr 2027, FY27Q4 = May-Jul 2027 (FY26Q1 = Aug-Oct 2025, and so on).
- **Quarter labels** may be any fiscal quarter (FY25Q4, FY26Q1, FY27Q1, ...) or year (FY26, FY27): a document
  that reprints older figures or guidance is recorded under the quarter they belong to. **(v2)**
- Transcript text is licensed: keep quotes to what the citation needs.

## Filings reader (`facts.csv`, `changes.csv`)

As in v1 (`reader_form.md`), with the v2 rules above.

## Release reader

### results.csv

`id,quarter,item,basis,duration,value,unit,scale,yoy_stated,text,line,quote`

- `quarter`: the fiscal quarter, or the fiscal year for full-year rows
- `duration`: 3M, 6M, 9M, 12M, or instant. Take the year-to-date columns where printed. **(v2)**
- `basis`: gaap, non_gaap, kpi
- `yoy_stated`: the growth rate as the source states it, else blank
- `item`, one of:
  - **Income statement and cash flow:** revenue, gross_profit **(v2)**, gross_margin, operating_income,
    operating_margin, net_income, eps_diluted, shares_diluted **(v2)**, tax_rate **(v2)**,
    operating_cash_flow, operating_cash_flow_margin **(v2)**, capex_ppe **(v2)**,
    capitalized_software **(v2)**, fcf, fcf_margin
  - **Balance sheet:** cash_and_investments, deferred_revenue, rpo, crpo, crpo_pct_of_rpo **(v2)**
  - **ARR:** arr, net_new_arr, arr_ex_acq, arr_growth_ex_acq, net_new_arr_ex_acq, red_canary_arr,
    red_canary_net_new_arr, red_canary_revenue, revenue_ex_acq **(v2)**
  - **Product and customer metrics (v2), every quarter they appear in a release, letter, call
    presentation or supplemental:**
    - zte_enterprises: Zero Trust Everywhere enterprises
    - zflex_tcv: Z-Flex TCV or bookings
    - ai_security_arr, and its later parts security_for_ai_arr and agentic_secops_arr
    - data_security_arr
    - zdx_advanced_plus_bookings, ai_protect_bookings
    - deals_1m_plus: count or record of $1M+ ARR or ACV deals
    - customers_100k_arr, customers_1m_arr, customers_10m_arr, total_customers
    - g2k_customer_pct and f500_customer_pct: share of the Forbes Global 2000 / Fortune 500 that are
      customers
    - nrr, gross_retention
  - `other:<name>` for **any** other product, customer, bookings or segment metric the documents report,
    even if mentioned only once in a letter's text. Read the letters' prose, not only their tables.

### guidance.csv

`id,given_in,target_period,item,basis,low,high,unit,scale,growth_stated,text,line,quote`

- `given_in`: the release that first gave it, including earlier ones whose figures a later document
  reprints (a look-back table) **(v2)**; `target_period`: any fiscal quarter or year **(v2)**
- `item`: revenue, arr, gross_margin, operating_income, operating_margin, eps_diluted, fcf_margin,
  shares_diluted, tax_rate, red_canary_arr, and **(v2)** capex_pct_revenue, net_other_income,
  red_canary_revenue, red_canary_net_new_arr, net_new_arr_share (the share of a year's net new ARR expected in a
  quarter or half, unit %), restructuring_charges, or `other:<name>` for any other figure the outlook gives. Every
  outlook number goes in this table, including the ones in a letter's bullets and not in the release.
- a single figure ("approximately 80%") goes in both `low` and `high`; a growth-only figure ("16-17%")
  leaves `low` and `high` blank and goes in `growth_stated`
- raised or cut guidance appears once per release that states it

### bridge.csv, consensus.csv, compare.csv

As in v1, with the v2 rules above. In bridge.csv, keep every printed line of each reconciliation
(pre-tax, tax, the diluted-share steps) as `other:<name>` when its name is not in the list. **(v2)**

## Call reader

As in v1. (The second-opinion test covered the release reader only; the call reader is judgment-heavy and
was not redone by another model.)
