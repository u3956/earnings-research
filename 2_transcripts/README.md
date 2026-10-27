# 2. Transcripts

Management commentary and the analyst Q&A exist only in the call transcripts. This folder documents how the
transcripts were obtained, produced, extracted and verified. The transcripts are not published: the official versions
are licensed, and both versions reproduce the company's own words. A few short lines are quoted here and in the
samples.

## Official and in-house transcripts

| | Official transcripts | In-house transcripts |
|---|---|---|
| Coverage | The four FY26 earnings calls | The Q4 call (63 minutes) and the six recorded sections of the investor day (3 hours 27 minutes) |
| Source | The company's investor relations site; edited, with speakers identified | The call replay and the company's recordings, transcribed on a local GPU |
| Strengths | Speaker attribution | A timestamp on every line; the only text of the investor day |
| Weaknesses | No timestamps; edited, and occasionally wrong | No speaker labels; names and figures can be misheard |

The Q4 call was transcribed both ways so that each version could be checked against the other.

## In-house transcription

- **Audio as published.** The Q4 call is taken from its replay, and the investor day from the company's six section
  recordings. The full-length investor-day recording was not used, as it duplicates the sections, which omit only
  about four minutes of introductions and transitions.
- **Whisper large-v3 on a local GPU**, with English forced and a list of the company's own spellings of its products,
  executives and acquisitions. A lock file prevents two transcriptions from running on the GPU at once.
- **A timestamp on every line** (`[hh:mm:ss]`), so any quote can be located in the audio.

The excerpt at the end of this page shows this step.

## Extraction

The call reader processed the four official transcripts, the in-house investor-day transcripts and the investor-day
presentation, and completed three tables. Every entry references the exact line it came from.

| Table | Entries | Content |
|---|---|---|
| statements | 720 | One figure or claim from management, with speaker, topic and period, a one-line statement and its source line. By event: Q1 94, Q2 138, Q3 137, Q4 155, investor day 196 (137 from the recordings, 59 from the presentation) |
| qa | 81 | One analyst question: the analyst, the question and the answer summarized in a line each, and a grade. 43 were answered directly, 33 partially and 5 were dodged; where an answer was not direct, the entry states what was asked and not answered |
| wording | 43 | The change in management's wording on one topic from one event to the next (stronger, weaker, new, dropped or unchanged), with both quotes |

Samples: [call_statements.csv](samples/call_statements.csv) (with the verification results for each entry),
[call_qa.csv](samples/call_qa.csv) (one direct, one partial and one dodged answer; quotes withheld) and
[call_wording.csv](samples/call_wording.csv).

## Verification

1. **Citations (script).** Every quote appears exactly on its cited line, and every figure appears within its quote.
2. **Speaker attribution (script).** For each cited line of an official transcript, the label above it matches the
   entry's speaker, analyst or respondent: 642 of 642.
3. **Coverage of the Q&A.** Every analyst question on the four calls has an entry. The 11 analyst turns without one are
   closing thanks, one sound check and one follow-up merged into its question.
4. **Review agents.** Review agents re-read all 844 entries against the lines they rest on and raised 17 flags. Each
   flag was verified against the source before it was accepted, and 13 entries were corrected. No correction changed a
   figure; all concerned overstatement:
   - "a big part of that is ZIA and ZPA" had been recorded as "mostly ZIA/ZPA";
   - a qualifier was dropped: Z-Flex "doesn't have necessarily a different impact" on ARR became "does not change" it;
   - "not seats" was the reader's inference rather than a statement made on the call;
   - three restructuring entries were assigned a quarter that management had not given;
   - one value retained the in-house transcript's "200,000 locations", although the entry's own statement noted that
     the presentation says 200+.

   Every correction keeps its original value in [corrections.csv](../4_checks/corrections.csv). Two of the 17 flags
   were themselves wrong: one read the CFO's restatement of a full-year figure as a new Q4-only figure, and the other
   attributed an executive's own arithmetic to the reader.
5. **Manual sample.** Nine of the 30 figures in the manual sample come from these tables. Each was checked against the
   transcript page, the presentation page or the recording timestamp; all nine were correct.

## Errors in the transcripts and in management's figures

**Official transcripts:**
- the Q4 transcript attributes to the CFO an answer to a question put to the CEO;
- it renders as "a legacy fiber-based SaaS platform" what the presentation calls a firewall-based SASE platform;
- misheard words: "fiscal 2017" for fiscal 2027, and "final vendors" for firewall vendors;
- one analyst's firm is listed as "Citibank Cameroon SA (Douala Branch)".

**In-house transcripts:**
- "$20 billion" for the $220B total market shown on the slide;
- "over 200,000 locations" where the presentation says 200+;
- "$8 to $10 billion by fiscal." lost its year (the presentation says FY31);
- most personal names were garbled, and the company's own name was rendered five different ways despite the names
  list.

**Management's figures across calls and presentations:**
- **A metric redefined without reconciliation.** "AI Security ARR" passed $400M on the Q1 call, with a target of over
  $0.5B by the end of FY26. The investor day put "Security for AI" at about $70M under new categories, and nothing
  reconciles the two.
- **Data Security ARR** went from about $450M (Q1) to over $500M (Q3), then to $410M at the investor day, after one
  product moved to another category.
- **The target market** was defined as enterprises with "over two thousand user seats" on one call and 1,500+ employees
  in the presentation, and was sized at 4,400, then 4,500, then 4,600 enterprises.
- **One customer example** carries three sets of figures: "$5 million plus" of ARR on the Q4 call, "$5 million worth of
  ARR expansion" at the investor day, and $3.1M to $8.0M on the presentation's chart.
- **The chief revenue officer's arithmetic:** $15B of "white space" was described as "a 5x expansion potential" on $3.8B
  of ARR. $15B is about 4x; the presentation's 5x refers to the $19B total.

## Excerpt from calls.py

The download step is not shown. The excerpt below is the transcription step (`…` marks omissions): the names list is
supplied, the lock limits the GPU to one job, and each segment is written with its timestamp.

```python
NAMES = {"ZS": "Zscaler, …, Red Canary, SPLX, Zero Trust Exchange, "
               "Zero Trust Everywhere, ZDX, ARR"}       # as spelled in the company's own releases
# …
    if LOCK.exists():
        sys.exit(f"GPU lock held ({LOCK}): another transcription is running; try again later")
    names.write_text(NAMES.get(sym, ""), encoding="utf-8")
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    LOCK.write_text(str(os.getpid()))
    try:
        subprocess.run([…, audio, tsv, names, "en", "0.5"], check=True)    # Whisper large-v3 on the GPU
    finally:
        LOCK.unlink(missing_ok=True)
    add_to_manifest(base, tsv, "whisper large-v3 of " + audio.relative_to(base).as_posix())

    lines = tsv.read_text(encoding="utf-8").splitlines()
    head = dict(x.split("\t", 1) for x in lines[:2])
    segs = [x.split("\t", 2) for x in lines[2:] if x.count("\t") >= 2]
    txt.write_text(f"{sym} {quarter} | {head.get('label', '')} | language {head.get('language', '')}\n\n"
                   + "\n".join(f"{stamp(a)} {t.strip()}" for a, _, t in segs) + "\n", encoding="utf-8")
```
