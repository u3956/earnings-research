"""Draw the 30 numbers for the hand check: only numbers the script could not confirm against XBRL.

    python -B checks/sample.py            # after checks/check.py; writes checks/hand30.csv (fixed seed)

The script already showed every quote is on its line and holds its value, so the hand check asks what it cannot:
is it the right item, period and basis, read from the right column? Strata (the three readers' tables, plus release B's
rows that reader A does not have):
  filings facts not confirmed by XBRL 2, release results 9 (5 KPI, 3 non-GAAP, 1 GAAP), guidance 6, consensus 2,
  call statements 9 (one per event, the rest at random), release-B-only results 2.
Fill `check` with ok or wrong, and `note` with what is wrong. `source` is the original file (open it, not the
text copy); `where` is the PDF page, sheet or timestamp; search for `quote`.
"""
import csv
import random
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
TEXT = HERE / "text" / "ZS"
SEED = 20261026


def read(p):
    return list(csv.DictReader(open(HERE / p, newline="", encoding="utf-8")))


def confirmed(out):
    return {r["id"] for r in read(out) if r["truth"] == "ok"}


def where(rel, line):
    """The PDF page, spreadsheet sheet or transcript timestamp of a cited line."""
    lines = (TEXT / rel).read_text(encoding="utf-8").splitlines()[:int(line)]
    for x in reversed(lines):
        m = re.match(r"=== (page \d+|sheet .+?) ===", x) or re.match(r"\[(\d\d:\d\d:\d\d)\]", x)
        if m:
            return m[1]
    return "search the quote"


def says(table, r):
    if table == "facts":
        return f"{r['filing']} {r['statement']}: {r['item']} ({r['member']}) {r['duration']} to {r['period_end']}"
    if table == "results":
        y = f", stated growth {r['yoy_stated']}%" if r["yoy_stated"] else ""
        return f"{r['quarter']} {r['item']} ({r['basis']}, {r['duration']}){y}"
    if table == "guidance":
        g = f", growth {r['growth_stated']}%" if r["growth_stated"] else ""
        return f"guidance given in {r['given_in']} for {r['target_period']}: {r['item']} ({r['basis']}){g}"
    if table == "consensus":
        return f"{r['quarter']} {r['item']} as of {r['as_of']}"
    return f"{r['event']}, {r['speaker']} ({r['role']}): {r['statement']}"


def value(table, r):
    v = f"{r['low']} to {r['high']}" if table == "guidance" else r.get("estimate") or r.get("value")
    return f"{v} {r.get('unit', '')} {r.get('scale', '')}".strip()


def main():
    rnd = random.Random(SEED)
    drawn = []

    def take(reader, table, rows, n):
        for r in rnd.sample(rows, min(n, len(rows))):
            drawn.append((reader, table, r))

    ok = confirmed("checks/out/readers_filings.csv")
    take("filings", "facts", [r for r in read("readers/filings/facts.csv") if r["id"] not in ok], 2)
    ok = confirmed("checks/out/readers_release.csv")
    res = [r for r in read("readers/release/results.csv") if r["id"] not in ok]
    take("release", "results", [r for r in res if r["basis"] == "kpi"], 5)
    take("release", "results", [r for r in res if r["basis"] == "non_gaap"], 3)
    take("release", "results", [r for r in res if r["basis"] == "gaap"], 1)
    take("release", "guidance", read("readers/release/guidance.csv"), 6)
    take("release", "consensus", read("readers/release/consensus.csv"), 2)
    st = [r for r in read("readers/call/statements.csv") if r["value"]]
    events = sorted({r["event"] for r in st})
    for e in events:
        take("call", "statements", [r for r in st if r["event"] == e], 1)
    chosen = {r["id"] for _, t, r in drawn if t == "statements"}
    take("call", "statements", [r for r in st if r["id"] not in chosen], 9 - len(events))
    key = lambda r: (r["quarter"], r["item"], r["basis"], r["duration"])
    first = {key(r) for r in read("readers/release/results.csv")}
    ok = confirmed("checks/out/readers_release_b.csv")
    take("release B", "results", [r for r in read("readers/release_b/results.csv")
                                      if key(r) not in first and r["id"] not in ok], 2)
    with open(HERE / "checks" / "hand30.csv", "w", newline="", encoding="utf-8-sig") as fh:  # BOM: Excel reads UTF-8
        w = csv.writer(fh)
        w.writerow(["n", "reader", "table", "id", "reader_says", "value", "source", "where", "quote", "check", "note"])
        for n, (reader, table, r) in enumerate(drawn, 1):
            src = "sources/ZS/" + r["text"][:-4] if r["text"].endswith(".txt") else r["text"]
            w.writerow([n, reader, table, r["id"], says(table, r), value(table, r), src,
                        where(r["text"], r["line"]), r["quote"], "", ""])
    print(f"{len(drawn)} rows -> checks/hand30.csv")


if __name__ == "__main__":
    main()
