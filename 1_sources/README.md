# 1. Sources

This folder documents the source collection for Zscaler's fiscal 2026 (Aug 1, 2025 to Jul 31, 2026). The source files
themselves are not included, as they belong to the company, the SEC or data vendors.

| Source | Contents retained |
|---|---|
| SEC EDGAR | Every 10-Q, 10-K and 8-K since Nov 2025: the index page, the main document, the earnings-release exhibit, and the XBRL instance with its labels; plus dated snapshots of the company's filing index and of its full XBRL data |
| Company investor relations site | Official call transcripts for all four quarters, shareholder letters (Q2-Q4), the Q1 call presentation, supplemental financials (spreadsheets for Q2-Q4, a PDF for Q1), a "modeling considerations" sheet, and the investor-day presentation |
| Q4 call replay and investor-day recordings | Audio, transcribed in-house ([2_transcripts](../2_transcripts/README.md)) |
| Analyst consensus | A dated snapshot of Yahoo Finance estimates: revenue and EPS by quarter and year, estimate history, ratings |
| In-house market data | The company's daily prices and earnings history, copied with a date |

| Quarter | Period end | Earnings release filed (8-K, exhibit 99.1) | Periodic report |
|---|---|---|---|
| FY26 Q1 | 2025-10-31 | 2025-11-25 16:07 ET | 10-Q |
| FY26 Q2 | 2026-01-31 | 2026-02-26 16:07 ET | 10-Q |
| FY26 Q3 | 2026-04-30 | 2026-05-26 16:08 ET | 10-Q |
| FY26 Q4 | 2026-07-31 | 2026-09-03 16:08 ET | 10-K |

Other 8-K filings: Jan 15, 2026 (item 5.07, shareholder vote), Apr 16 and Sep 24, 2026 (item 5.02, officer changes)
and Oct 6, 2026 (item 7.01, investor-day release).

## Record-keeping

- Every file is written by a single function, which in the same call appends a row to the manifest: source URL,
  retrieval time (UTC), size and MD5 checksum (excerpt 1).
- A filing already stored is never downloaded again, so each source remains as first retrieved (excerpt 2).
- The SEC's filing index and XBRL data are saved as new dated files on every run. A change on the SEC's side therefore
  appears as a difference between two dated files rather than silently replacing the earlier copy.
- The investor relations site blocks automated downloads, so its files were saved through a browser and logged with
  their URLs in the same way.

## Conversion to line-numbered text

[extract.py](extract.py), published in full, converts each file into a text copy that a reader can quote and a script
can verify:
- filings and releases: one line per paragraph or table row, with cells joined by " | ";
- PDFs: a `=== page N ===` marker before each page;
- spreadsheets: a `=== sheet NAME ===` marker before each sheet, then one line per row;
- in-house transcripts: copied unchanged, one timestamped line per segment.

The text copies depend only on the source files and the script, and can be regenerated at any time.

## Observations during collection

1. **Two downloads of the same SEC data disagreed.** A fresh EDGAR download gives the Q4 release an acceptance time of
   20:08 UTC (16:08 ET, shortly after the market close). Copies of the same filing index taken two weeks earlier show a
   time four hours later, exactly the offset between UTC and New York time. The same applied to three other companies
   checked; a fourth was correct in both copies. Whatever the cause, a copy can differ from the next download, which is
   why every file records its retrieval time and checksum.
2. **A web search summary presented the ARR guidance as revenue guidance.** It gave FY27 revenue guidance as
   $4.396-4.426B; the release identifies that range as ARR, with revenue guided to $3.908-3.938B. This is why every
   figure in the tables is cited to the primary document.
3. **Headline growth includes an acquisition.** Red Canary was acquired in the first quarter. Revenue and ARR grew
   25-26%, but ARR excluding Red Canary grew 21%, 21% and 20% in Q2, Q3 and Q4, and FY27 ARR is guided to grow about
   17%.
4. **Consensus sits at the top of the guidance range.** As of Oct 25, 2026: FY27 Q1 revenue $938.2M (42 analysts)
   against guidance of $935-939M; FY27 EPS $4.91 against $4.86-4.90.
5. **The company publishes its own transcripts.** A web search found only partial third-party copies. The investor
   relations site carries the official transcript for every quarter, together with shareholder letters and supplementals
   that are not filed on EDGAR.

## Excerpts from fetch.py

`fetch.py` is not published in full, because part of it reads the consensus snapshot and private market data. The two
excerpts below are the parts that keep the sources intact.

**1. Every file is recorded as it is written.**

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

**2. Stored sources are not overwritten:** a filing folder already on disk is skipped.

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
