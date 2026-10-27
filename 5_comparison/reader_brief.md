You are the release reader for <<COMPANY>> (<<T>>), one of 19 cybersecurity companies that will be compared side by
side. Read its earnings releases and fill two fixed tables, `results.csv` and `guidance.csv`, in which every number
points to the exact line it came from. A script will re-read every citation and check the GAAP figures against the
company's own XBRL filings, so accuracy and exact quotes come first, then completeness.

Working folder: the current directory. The sources are under `text/<<T>>/`: plain text with stable lines (a table row
is one line, its cells joined with " | "). The releases, one per quarter:

<<RELEASES>>

Quarters are <<T>>'s fiscal quarters. <<FY>>
<<EXTRA>>
Write everything to `out/`: `results.csv`, `guidance.csv` and `notes.md`. Write the CSVs with Python's `csv` module
(UTF-8, the header exactly as below). Helper scripts, if you write any, also go in `out/`.

## Rules for every table

- **Every value is cited** by three columns:
  - `text`: the file's path as listed above, starting `text/<<T>>/`
  - `line`: the 1-based line number in that file
  - `quote`: an exact substring of that line, copied character for character (no edits, no "..."), at most 200
    characters, containing the value as printed there.
- **Values** are plain numbers as printed, without commas or currency signs. A value in parentheses is negative.
  Percentages are numbers with unit `%`.
- `unit` is one of `USD`, `USD/share`, `%`, `count`, `shares`.
- `scale` is one of `ones`, `thousands`, `millions`, `billions`: the scale the source prints (a table headed
  "in thousands" is `thousands`; "$1.2 billion" is `billions`; a percentage or per-share figure is `ones`).
- **A cell printed "—" or "-" is nil: leave it out (no row).**
- **Take the exact figure from the financial tables** rather than a rounded headline. Use the headline only when no
  table prints the figure.
- **Record the current-quarter column** of each release, and in a fourth-quarter release also the full-year column.
  Skip the prior-year comparison columns and any 6- or 9-month columns.
- **Never cite a quote that does not contain the value, and never compute a value.** Missing is fine; guessing is not:
  list what you could not find in `notes.md`.
- Labels: `FY26Q3` for a fiscal quarter, `FY26` for a fiscal year.

## results.csv

`id,quarter,item,basis,duration,value,unit,scale,yoy_stated,text,line,quote`

- `id`: R001, R002, ...
- `quarter`: the fiscal quarter (or the fiscal year, for a full-year column)
- `duration`: `3M` for a quarter, `12M` for a fiscal year, `instant` for a balance-sheet figure
- `basis`: `gaap`, `non_gaap` or `kpi`
- `yoy_stated`: the year-over-year growth as the release states it (`22` for "22%"), else blank
- `item`, one of the following. Take every one the release prints, every quarter:
  - **Income statement, GAAP** (from the GAAP statements) **and non-GAAP** (from the non-GAAP tables or the
    reconciliations' totals): `revenue`, `subscription_revenue` (the recurring line: subscription, subscription and
    support, or SaaS revenue; other revenue lines as `other:<name>_revenue`), `gross_profit`, `gross_margin`,
    `operating_income`, `operating_margin`, `net_income`, `eps_diluted`, `shares_diluted` (the share count behind
    diluted EPS)
  - **Cash flow:** `operating_cash_flow`, `capex` (purchases of property and equipment), `capitalized_software`
    (capitalized internal-use software, when shown on its own line), `fcf` (free cash flow as the company defines it;
    basis `non_gaap`), `fcf_margin`; `other:adjusted_fcf` and `other:adjusted_fcf_margin` when the company also reports
    an adjusted version
  - **Balance sheet** (`instant`): `cash_and_investments` (when the release states the total of cash, equivalents and
    investments; otherwise each line as `other:<name>`), `deferred_revenue_current`, `deferred_revenue_noncurrent`,
    `other:convertible_notes` or `other:debt` for borrowings
  - **Operating metrics** (basis `kpi`):
    - `arr`: the company's headline annual recurring revenue, whatever it is called (ARR, total ARR, subscription
      ARR, Next-Generation Security ARR, ...); `net_new_arr`; other ARR measures as `other:<name>_arr`
    - `rpo`, `crpo` (remaining performance obligations, current RPO)
    - `billings` (and `other:calculated_billings` if printed)
    - `customers_100k`, `customers_1m`, or `other:customers_<threshold>` for the company's large-customer counts
    - `total_customers`, `nrr` (net retention, dollar-based net retention or net expansion rate), `gross_retention`
    - `other:<name>` for every other operating metric the release reports (module or platform adoption, paying
      customers, large deals, and so on), even when it appears only once in a sentence
  - **Acquisitions:** `acquired_revenue`, `acquired_arr`, `revenue_ex_acq`, `arr_ex_acq`, `organic_growth` (growth
    excluding acquisitions, %), for every quarter a source states them. Name the acquisition in `notes.md`.

## guidance.csv

`id,given_in,target_period,item,basis,low,high,unit,scale,growth_stated,text,line,quote`

- `id`: G001, G002, ...
- `given_in`: the quarter of the release that gives it (the quarter that release reports, from the list above);
  `target_period`: the quarter or fiscal year the guidance is for
- `item`: `revenue`, `subscription_revenue`, `arr`, `net_new_arr`, `billings`, `crpo`, `rpo`, `gross_margin`,
  `operating_income`, `operating_margin`, `net_income`, `eps_diluted`, `fcf`, `fcf_margin`, `operating_cash_flow`,
  `shares_diluted`, `tax_rate`, or `other:<name>` for any other outlook figure
- `basis`: as the outlook states it; revenue is `gaap` unless called non-GAAP, ARR and billings are `kpi`, and most
  margins, operating income, EPS and free cash flow are `non_gaap`
- Record **every outlook figure of every release**, the next quarter and the full year, each time it is given, also
  when unchanged. A single figure ("approximately $X") goes in both `low` and `high`. A growth-only figure ("12% to
  14% growth") leaves `low` and `high` blank and goes in `growth_stated` as `12-14`. When a range is printed as dollars
  and growth, record the dollars and put the growth in `growth_stated`.

## notes.md

1. Items not found.
2. Judgment calls, such as which line you took as `arr`.
3. Anything in the sources that looks wrong or inconsistent, with its citation.
4. One line per release on what the company itself says changed: a new or redefined metric, an acquisition, a
   restructuring, a change in how it guides, a management change.

Rules: write only inside `out/`; change nothing else; no web access. Everything you need is in this brief: there is
no AGENTS.md to look for, and no skill or plugin to use. Keep searches narrow, since your usage is limited: read the
releases with a line-numbered search, and in any 10-Q or 10-K print only the matching lines (`rg -n -m 30
--max-columns 300` with a specific pattern), never a whole file. Before finishing, check that every quote is an exact
substring of its cited line and contains its value.

When done, reply with: rows per table; the guidance track, one line per quarter (reported revenue and non-GAAP EPS
against the range guided the quarter before); and anything inconsistent you found, each with its citation.
