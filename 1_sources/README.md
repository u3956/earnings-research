# 1. Sources

Everything collected for Zscaler's fiscal 2026 (Aug 1, 2025 to Jul 31, 2026). None of these files is in this repo:
they belong to the company, the SEC or a data vendor. This page says what was kept and how.

| Source | What was kept |
|---|---|
| SEC EDGAR | Every 10-Q, 10-K and 8-K since Nov 2025: the index page, the main document, the press-release exhibit, and the XBRL instance with its labels. Plus dated snapshots of the company's filing list and of all its XBRL facts |
| The company's investor relations site | The official call transcripts for all four quarters, the shareholder letters (Q2-Q4), the Q1 call slides, the supplemental financials (spreadsheets for Q2-Q4, a PDF for Q1), a "modeling considerations" sheet, and the investor-day deck |
| The Q4 call replay and the investor-day recordings | The audio, transcribed by us ([2_transcripts](../2_transcripts/README.md)) |
| Analyst consensus | A dated snapshot of Yahoo Finance's estimates: revenue and EPS by quarter and year, the estimate history, the ratings |
| Our own price and earnings data | The company's daily prices and earnings history, copied with a date |

| Quarter | Ends | Press release filed (8-K, exhibit 99.1) | Report |
|---|---|---|---|
| FY26 Q1 | 2025-10-31 | 2025-11-25 16:07 ET | 10-Q |
| FY26 Q2 | 2026-01-31 | 2026-02-26 16:07 ET | 10-Q |
| FY26 Q3 | 2026-04-30 | 2026-05-26 16:08 ET | 10-Q |
| FY26 Q4 | 2026-07-31 | 2026-09-03 16:08 ET | 10-K |

The other 8-Ks: Jan 15, 2026 (item 5.07, the shareholder vote), Apr 16 and Sep 24, 2026 (item 5.02, officer changes)
and Oct 6, 2026 (item 7.01, the investor-day release).

## Kept exactly as fetched

- **No file enters without its record.** One function writes every file, and the same call adds its row to the
  manifest: the address it came from, the fetch time in UTC, its size and its md5 checksum (excerpt 1).
- **A filing already on disk is never fetched again**, so a source stays as it was first read (excerpt 2).
- **The SEC's lists are dated.** The filing list and the XBRL facts are saved as new dated files on each run, so a change
  on the SEC's side shows up as a difference between two dated files instead of silently replacing the old one.
- **The investor relations site blocks scripts**, so its files were downloaded in a browser and logged with their
  addresses like every other file.

## Every source becomes line-numbered text

[extract.py](extract.py) (in full) turns each file into a text copy that a reader can quote and a checker can find again:
- a filing or release: one line per paragraph or table row, with a row's cells joined by " | ";
- a PDF: a `=== page N ===` line before each page;
- a spreadsheet: a `=== sheet NAME ===` line before each sheet, then one line per row;
- our own transcripts: copied as they are, one timestamped line per segment.

The text copies depend only on the source files and the script, so they can be rebuilt at any time.

## Found while collecting

1. **Two downloads of the same SEC data disagreed.** A fresh EDGAR download gives the Q4 release an acceptance time of
   20:08 UTC, which is 16:08 ET, just after the close. Copies of the same filing list taken two weeks earlier read four
   hours later, exactly the gap between UTC and New York time. The same held for three other companies checked, while a
   fourth was right in both copies. Whatever the cause, a copy can differ from the next download, which is why every
   file here carries its fetch time and checksum.
2. **A web search summary called the ARR guidance "revenue".** It gave FY27 revenue guidance as $4.396-4.426B. The
   release says that range is ARR; revenue is guided to $3.908-3.938B. Every number in the tables is cited to the
   primary document for exactly this reason.
3. **Headline growth includes an acquisition.** Red Canary was bought in the first quarter. Revenue and ARR grew 25-26%,
   but ARR without Red Canary grew 21%, 21% and 20% in Q2, Q3 and Q4, and FY27 is guided to about 17%.
4. **The analysts sit at the top of the guidance.** The consensus on Oct 25, 2026: FY27 Q1 revenue $938.2M (42
   analysts) against $935-939M guided; FY27 EPS $4.91 against $4.86-4.90.
5. **The company publishes its own transcripts.** A web search found only partial third-party copies. The investor
   relations site has the official transcript for every quarter, plus shareholder letters and supplementals that are
   not on EDGAR.

## Excerpts from fetch.py

`fetch.py` is not published in full: part of it reads the consensus snapshot and our private price and earnings data. These
are the two parts that keep the sources honest.

**1. Every file is recorded the moment it is written.**

```python
def add_to_manifest(base, path, url, data=None):
    """Record one file of the pack; data is its bytes (read from disk when None)."""
    data = path.read_bytes() if data is None else data
    m = base / "manifest.csv"
    new = not m.exists()
    with open(m, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(MANIFEST_COLS)
        w.writerow([path.relative_to(base).as_posix(), url, now_utc(), len(data),
                    hashlib.md5(data).hexdigest()])


def save(base, rel, url, data):
    p = base / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
    add_to_manifest(base, p, url, data)
    return p
```

**2. Sources stay as first read:** a filing folder already on disk is skipped, never overwritten.

```python
    for x in sorted(rows, key=lambda y: y["accepted_utc"]):
        x["folder"] = f"sec/{x['filed']}_{x['form']}_{x['accession']}"
        if (base / x["folder"]).exists():
            print("kept   ", x["folder"])
            continue
        page, page_url, docs = filing_docs(cik, x["accession"])
        save(base, f"{x['folder']}/index.htm", page_url, page)
        for typ, name, doc_url in docs:
            if typ == x["form"] or typ.startswith(KEEP):
                save(base, f"{x['folder']}/{name}", doc_url, get(doc_url))
```
