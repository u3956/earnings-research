# 2. Transcripts

What management says on a call, and how it answers the analysts, is only in the transcripts. This page shows how they
were gathered, made, read and checked. The transcripts themselves are not published: the official ones are licensed,
and both kinds are the company's words. A few short lines are quoted below and in the samples.

## Two kinds of transcript

| | Official transcripts | Our own transcripts |
|---|---|---|
| Covers | The four FY26 earnings calls | The Q4 call (63 minutes) and the six recorded sections of the investor day (3 hours 27 minutes) |
| Comes from | The company's investor relations site, edited, with speakers named | The call's replay and the company's recordings, transcribed on a local GPU |
| Good at | Who said what | A timestamp on every line; the only text there is of the investor day |
| Weak at | No timestamps; edited, and sometimes wrong | No speaker labels; mishears names and numbers |

The Q4 call was transcribed both ways, so each version could check the other.

## How our own transcripts are made

- **The audio as served.** The Q4 call comes from its replay. The investor day comes from the company's six section
  recordings; its full-length recording was skipped as a duplicate (the sections miss only about four minutes of
  introductions and transitions).
- **Whisper large-v3 on a local GPU**, with English forced and a list of the company's own spellings of its products,
  executives and acquisitions, so the names come out right. A lock file keeps two transcriptions off the GPU at once.
- **A timestamp on every line** (`[hh:mm:ss]`), so any quote can be found again in the audio.

The excerpt at the end of this page is that step.

## What the call reader built

One reader agent read the four official transcripts, our investor-day transcripts and the investor-day deck, and
filled three tables. Every row points to the exact line it came from.

| Table | Rows | What a row holds |
|---|---|---|
| statements | 720 | One number or claim from management, with its speaker, topic and period, a one-line statement, and the exact line it came from. By event: Q1 94, Q2 138, Q3 137, Q4 155, investor day 196 (137 from the recordings, 59 from the deck) |
| qa | 81 | One analyst question: who asked it, the question and the answer in a line each, and a grade. 43 were answered directly, 33 in part and 5 dodged; when not direct, the row says what was asked and not answered |
| wording | 43 | How management's wording on one topic moved from one event to the next: stronger, weaker, new, dropped or the same, with both quotes |

Samples: [call_statements.csv](samples/call_statements.csv) (with the check results of each row),
[call_qa.csv](samples/call_qa.csv) (one answered directly, one in part, one dodged; the quotes are not published) and
[call_wording.csv](samples/call_wording.csv).

## How they were checked

1. **Every quote found again by script:** each sits exactly on its cited line, and each number is inside its quote.
2. **Every speaker label checked by script:** for each cited line of an official transcript, the label above it matches
   the row's speaker, analyst or answerer. All 642 matched.
3. **Every question covered.** Every analyst question on the four calls has a row. The 11 analyst turns without one are
   thank-yous, one sound check and one follow-up folded into its question.
4. **A second reading of every row.** Checker agents read all 844 rows, each next to the lines it rests on. They raised
   17 flags. Each flag was checked against the source before it counted, and 13 rows were fixed. None of the fixes
   changed a number; all were overstatements:
   - "a big part of that is ZIA and ZPA" had been written as "mostly ZIA/ZPA";
   - a hedge was dropped: Z-Flex "doesn't have necessarily a different impact" on ARR became "does not change" it;
   - "not seats" was the reader's own inference, not something said;
   - three restructuring rows were given a quarter that nobody gave;
   - one value kept our transcript's "200,000 locations", although its own sentence flagged that the deck says 200+.

   Every fix keeps its old value in [corrections.csv](../4_checks/corrections.csv). The checker agents were wrong too,
   on 2 of their 17 flags. One read the CFO restating a full-year figure as a new, Q4-only figure. The other blamed the
   reader for an executive's own arithmetic.
5. **By hand.** Nine of the 30 hand-checked numbers come from these tables. Each was checked against the transcript's
   page, the deck's page or the recording's timestamp, and all nine were right.

## What the transcripts got wrong

**The official transcripts:**
- the Q4 text labels an answer to a question put to the CEO as the CFO's;
- it has "a legacy fiber-based SaaS platform" for what the deck calls a firewall-based SASE platform;
- misheard words: "fiscal 2017" for fiscal 2027, "final vendors" for firewall vendors;
- one analyst's firm is listed as "Citibank Cameroon SA (Douala Branch)".

**Our own transcripts:**
- "$20 billion" for the $220B total market shown on the slide;
- "over 200,000 locations" where the deck says 200+;
- "$8 to $10 billion by fiscal." lost its year (the deck says FY31);
- most people's names were garbled, and the company's own name came out five different ways, even with the names
  list.

**Management's own numbers, between calls and slides:**
- **A metric changed meaning without a bridge.** "AI Security ARR" passed $400M on the Q1 call, with a target of over
  $0.5B by the end of FY26. The investor day put
  "Security for AI" at about $70M under new categories, and nothing reconciles the two.
- **Data security ARR** went from about $450M (Q1) to over $500M (Q3), then to $410M at the investor day, after one
  product moved to another category.
- **The target market** was enterprises with "over two thousand user seats" on one call, and 1,500+ employees in the
  deck. Its size went from 4,400 to 4,500, then to 4,600 enterprises.
- **One customer story** has three sets of figures: "$5 million plus" of ARR on the Q4 call, "$5 million worth of ARR
  expansion" at the investor day, and $3.1M to $8.0M on the deck's chart.
- **The sales chief's arithmetic:** $15B of "white space" called "a 5x expansion potential" on $3.8B of ARR. $15B is
  about 4x; the deck's 5x is the $19B total.

## Excerpt from calls.py

The download step is not shown. This is the transcription step (`…` marks cuts): the names list goes in, the lock
keeps the GPU to one job, and every segment comes out with its timestamp.

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
