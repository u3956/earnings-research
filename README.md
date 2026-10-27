# Earnings Research

A workflow for analyzing company earnings disclosures that combines scripted automation with AI agents. Scripts handle
collection, conversion, transcription, verification and reporting; AI agents handle extraction and review, and their
output is accepted only after independent checks. The aim is to cover everything a company publishes for a reporting
period with minimal manual work, with every figure tied to its source and verified before use.

Coverage to date: Zscaler (ZS), fiscal 2026, processed in full; a 19-company cybersecurity peer group, processed from
SEC filings and earnings releases.

## Workflow

```mermaid
flowchart LR
  A["Collection"] --> B["Conversion"] --> C["Extraction"] --> D["Verification"] --> E["Reporting"]
```

1. **Collection.** The workflow gathers a period's primary disclosures: SEC filings and their XBRL data, earnings
   releases, shareholder letters, investor presentations, supplemental financials, call transcripts and recordings, and
   a dated snapshot of analyst consensus. SEC material is downloaded by script; investor-relations material is saved
   manually. Every file is logged with its source URL, retrieval time (UTC) and checksum, and stored files are never
   overwritten.
2. **Conversion.** Each document is converted to line-numbered text, one line per paragraph or table row, with page and
   sheet markers. Calls are also transcribed from the audio with Whisper large-v3 on a local GPU, both to cross-check
   the official transcripts and to cover events without one.
3. **Extraction.** A separate AI agent reads each group of sources (SEC filings; earnings releases and investor
   materials; calls) and fills a fixed set of tables covering reported figures, guidance, reconciliations, consensus,
   changes between filings, management commentary, analyst Q&A, and changes in management's wording between calls. An
   entry is accepted only with its file, line and verbatim quote.
4. **Verification.** Nine checks, described below. Corrections are logged together with the original values.
5. **Reporting.** A one-page profile is generated for each company from the verified tables, showing the calculation and
   sources behind every figure, together with a peer comparison.

## Verification

Each check targets a different type of error.

| Check | Method |
|---|---|
| Citations | Every quote must appear verbatim on its cited line and contain the extracted value (script) |
| XBRL | Reported figures are matched against the company's XBRL data (script) |
| Arithmetic | Non-GAAP reconciliations, margins and multi-column table rows are recomputed (script) |
| Independent extraction | Two other models repeat the earnings-release extraction from the same instructions, and the results are compared (script) |
| Review agents | Every judgment-based entry, such as a summary of management commentary, is re-read against its source |
| Transcripts | Speaker attribution is checked against the official transcript (script), and the in-house and official transcripts are compared |
| Cross-document consistency | Discrepancies between the release, shareholder letter, presentation and supplementals are recorded |
| Completeness | Lines pairing a metric with a figure that no table captures are listed and reviewed |
| Manual sample | 30 figures, drawn at random from those no script could confirm, are checked against the source documents |

Results for Zscaler: all 1,983 quotes were found on their cited lines, no reported figure was contradicted by XBRL, and
all 30 sampled figures were correct; no check found an incorrect figure. Review of the 904 judgment-based entries led to
13 corrections, mainly to wording that went further than management's statements. Every issue identified, whether in
the agents' output or in the source documents, is recorded in the [error log](4_checks/ERRORS.md).

## Issues found in the source material

- A web search summary presented Zscaler's ARR guidance as revenue guidance.
- The official transcript of the Q4 call attributed an answer to the wrong executive.
- The company's own documents contained errors, including EPS guidance printed as "$3.78 to $3.82 million" and a
  supplemental spreadsheet whose year-to-date columns summed the wrong quarters.
- A metric was redefined without reconciliation: "AI Security ARR" passed $400M on one call, while the investor day
  later put "Security for AI" at about $70M under new categories.
- Headline ARR growth of 25% in Q4 included an acquisition; excluding Red Canary, growth was 20%.

## Repository

| | |
|---|---|
| [CRITERIA.md](CRITERIA.md) | The rules applied at each stage, and the reasons for them |
| [1_sources/](1_sources/README.md) | Source collection and record-keeping |
| [2_transcripts/](2_transcripts/README.md) | Official and in-house transcripts: extraction and checks |
| [3_readers/](3_readers/README.md) | The extraction agents, their table definitions and sample output |
| [4_checks/](4_checks/README.md) | Verification methods, results and the error log |
| [5_comparison/](5_comparison/README.md) | The 19-company cybersecurity peer comparison |

## Not included

- Source documents, which belong to the companies, the SEC or data vendors. The official call transcripts are
  licensed, so only brief excerpts are quoted.
- The full extraction tables; samples are provided.
- A forecasting model and research note built on these tables, both in progress.

## Tools

Python (standard library, pypdf, openpyxl), SEC EDGAR and XBRL data, Whisper large-v3 on a local GPU, AI agents for
extraction and review (including Codex CLI), and an AI coding agent to build and run the workflows.

For research purposes only; not investment advice.
