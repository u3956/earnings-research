"""Step 3, the script layer: re-read every citation of the reader tables and check the filed figures against XBRL.

    python -B checks/check.py readers/filings readers/release readers/call readers/release_b

Each folder's tables are found by name. For every citation (text, line, quote; a table can carry two):
  exact   the quote is an exact substring of the cited line (else where: other line, spacing, nowhere)
  long    the quote is over 200 characters
  value   every value of the row is one of the numbers in the quote (rows that carry a value)
Truth, against the XBRL instances of the 10-Qs and the 10-K:
  facts       every row: its own filing's instance has a fact for the same period whose value matches the row
              within half its last printed digit (any concept, dimensional ones too; sign ignored: outflows are
              printed negative and tagged positive). The concept found is written out. Else other_period when
              the filing tags that value at another date, else not_found.
  results     GAAP rows of the items in CONCEPTS: a fact of that concept, without dimensions, in any instance (the
              release itself is not tagged); not_found means the tagged figure differs (closest one written out)
  bridge      the GAAP line of each reconciliation, the same way
  no_period   nothing of that concept is tagged for the period (Q4's three months: the 10-K tags the year only;
              quarterly cash flow: the 10-Qs tag the year to date)
compare.csv (derived): its copied values equal the rows its ids point to, and above/within/below and
beat/inline/miss follow from them.
Writes checks/out/<folder>.csv (one line per row and citation) and prints the summary as Markdown.
"""
import csv
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
TEXT = HERE / "text" / "ZS"
SEC = HERE / "sources" / "ZS" / "sec"
OUT = HERE / "checks" / "out"
NUM = re.compile(r"\d[\d,]*(?:\.\d+)?")
CITES = {"facts": [("text", "line", "quote")], "results": [("text", "line", "quote")],
         "guidance": [("text", "line", "quote")], "bridge": [("text", "line", "quote")],
         "consensus": [("text", "line", "quote")], "statements": [("text", "line", "quote")],
         "changes": [("text", "line", "quote"), ("prior_text", "prior_line", "prior_quote")],
         "qa": [("q_text", "q_line", "q_quote"), ("a_text", "a_line", "a_quote")],
         "wording": [("from_text", "from_line", "from_quote"), ("to_text", "to_line", "to_quote")]}
VALUES = {"facts": ("value",), "results": ("value",), "guidance": ("low", "high"), "bridge": ("value",),
          "consensus": ("estimate",), "statements": ("value",)}
QEND = {"FY26Q1": "2025-10-31", "FY26Q2": "2026-01-31", "FY26Q3": "2026-04-30", "FY26Q4": "2026-07-31",
        "FY26": "2026-07-31"}
CONCEPTS = {"revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"],
            "gross_profit": ["GrossProfit"], "operating_income": ["OperatingIncomeLoss"],
            "net_income": ["NetIncomeLoss"], "eps_diluted": ["EarningsPerShareDiluted", "EarningsPerShareBasicAndDiluted"],
            "operating_cash_flow": ["NetCashProvidedByUsedInOperatingActivities"],
            "capex_ppe": ["PaymentsToAcquirePropertyPlantAndEquipment"], "capitalized_software": ["PaymentsToDevelopSoftware"],
            "shares_diluted": ["WeightedAverageNumberOfDilutedSharesOutstanding"],
            "rpo": ["RevenueRemainingPerformanceObligation"]}         # GAAP items the release shares with XBRL
_lines = {}


def lines(rel):
    if rel not in _lines:
        p = TEXT / rel
        _lines[rel] = p.read_text(encoding="utf-8").splitlines() if rel and p.is_file() else None
    return _lines[rel]


def num(s):
    try:
        return float(str(s).replace(",", "").replace("$", "").strip())
    except ValueError:
        return None


def mult(scale):
    s = (scale or "").lower()
    return 1e9 if "bill" in s else 1e6 if "mill" in s else 1e3 if "thous" in s else 1.0


def in_quote(v, quote):
    return any(abs(abs(v) - float(m.replace(",", ""))) < 1e-9 * max(1.0, abs(v)) for m in NUM.findall(quote))


def months(start, end):
    return round((date.fromisoformat(end) - date.fromisoformat(start)).days / 30.4)


def xbrl():
    """{instance folder: {(months or 0 for an instant, end): [(concept, dims, value)]}} for every 10-Q / 10-K."""
    out = {}
    for f in sorted(SEC.glob("*_10-[QK]_*/*_htm.xml")):
        x = f.read_text(encoding="utf-8")
        ctx = {}
        for cid, body in re.findall(r'<context id="([^"]+)">(.*?)</context>', x, re.S):
            s, e = re.search(r"<startDate>([^<]+)", body), re.search(r"<(?:endDate|instant)>([^<]+)", body)
            dims = ";".join(re.findall(r">([^<]+)</xbrldi:(?:explicit|typed)Member", body))
            ctx[cid] = (months(s[1], e[1]) if s else 0, e[1].strip(), dims)
        facts = defaultdict(list)
        for concept, cid, val in re.findall(r'<(\w[\w-]*:\w+)\b[^>]*contextRef="([^"]+)"[^>]*>([^<]+)<', x):
            if cid in ctx and num(val) is not None:
                m, e, dims = ctx[cid]
                facts[(m, e)].append((concept, dims, num(val)))
        out[f.parent.name] = facts
    return out


def tolerance(s, m):
    s = str(s).replace(",", "")
    return 0.5 * 10 ** -(len(s.split(".")[1]) if "." in s else 0) * m + 1e-9


def lookup(instances, period, value, m, raw, concepts=None):
    """('ok', concept, dims, xbrl value, note) for the closest fact of that period (of those concepts, when given,
    without dimensions), else ('other_period', ...) when the filing tags the value at another date (facts only),
    ('not_found', ...) or ('no_period', ...) when nothing of that period (or concept) is tagged."""
    v, tol = value * m, tolerance(raw, m)

    def best(cands):
        hits = sorted((abs(abs(xv) - abs(v)), c, d, xv) for c, d, xv in cands)
        ok = [h for h in hits if h[0] <= tol]
        undimmed = [h for h in ok if not h[2]]                              # prefer a fact without dimensions
        return (undimmed or ok or [None])[0], hits

    if concepts:
        cands = [(c, d, xv) for facts in instances for c, d, xv in facts.get(period, [])
                 if not d and c.split(":")[1] in concepts]
    else:
        cands = [x for facts in instances for x in facts.get(period, [])]
    if not cands:
        return "no_period", "", "", "", ""
    hit, hits = best(cands)
    if hit:
        return "ok", hit[1], hit[2], hit[3], ""
    if concepts:
        return "not_found", hits[0][1], "", hits[0][3], "closest fact of that concept and period"
    for p, facts in ((p, f) for inst in instances for p, f in inst.items() if p != period):
        hit, _ = best(facts)
        if hit:
            return "other_period", hit[1], hit[2], hit[3], f"tagged at {p[1]}" + (f", {p[0]} months" if p[0] else "")
    return "not_found", "", "", "", ""


def truth(table, r, facts):
    """The XBRL check of one row, or None when the row is not a filed figure."""
    raw = r.get("value")
    v = num(raw)
    if v is None:
        return None
    unit = r.get("unit") or ""
    m = 0.01 if unit == "%" else 1 if "share" in unit and "/" in unit else mult(r.get("scale"))
    if table == "facts":
        folder = Path(r.get("text", "")).parent.name
        if folder not in facts:
            return None
        dur = r.get("duration")
        period = (0 if dur == "instant" else int(dur.rstrip("M")), r.get("period_end"))
        return lookup([facts[folder]], period, v, m, raw)
    if table == "results":
        item = r.get("item")
        if item not in CONCEPTS or (r.get("basis") != "gaap" and item != "revenue"):
            return None
        q = r.get("quarter")
        if q not in QEND:
            return None
        dur = r.get("duration") or "3M"
        period = (12 if q == "FY26" else 0 if dur == "instant" else int(dur.rstrip("M")), QEND[q])
    elif table == "bridge":
        item = r.get("measure")
        if r.get("line_item") != "gaap" or item not in CONCEPTS or r.get("quarter") not in QEND:
            return None
        period = (12 if r["quarter"] == "FY26" else 3, QEND[r["quarter"]])
    else:
        return None
    return lookup(facts.values(), period, v, m, raw, CONCEPTS[item])


def cite(L, ln, q):
    """(exact, where) for one citation."""
    line = L[ln - 1] if L and 1 <= ln <= len(L) else None
    if line is not None and q and q in line:
        return True, ""
    if L is None:
        return False, "no file"
    if line is None:
        return False, "no line"
    squash = lambda s: re.sub(r"\s+", " ", s).strip()
    if squash(q) and squash(q) in squash(line):
        return False, "spacing"
    return False, "other line" if any(q in x for x in L) else "nowhere"


def check_compare(rows, tables):
    """Problems of the derived compare.csv: each copied value against its source row, and the labels."""
    by_id = {r["id"]: r for t in ("results", "guidance", "consensus") for r in tables.get(t, [])}
    out = []
    for r in rows:
        probs = []
        pairs = [("reported", "reported_id", "value"), ("guide_low", "guide_id", "low"),
                 ("guide_high", "guide_id", "high"), ("consensus", "consensus_id", "estimate")]
        for col, idcol, src in pairs:
            x, rid = num(r.get(col)), r.get(idcol)
            if x is None or not rid:
                continue
            ids = [i.strip() for i in re.split(r"[;,+ ]+", rid) if i.strip()]
            vals = [num(by_id[i].get(src)) for i in ids if i in by_id]
            if not vals:
                probs.append(f"{idcol} {rid} not found")
            elif all(y is None or abs(x - y) > 1e-9 * max(1, abs(x)) and
                     all(abs(x - y * f) > 1e-6 * max(1, abs(x)) for f in (1e-3, 1e3)) for y in vals):
                probs.append(f"{col} {x} vs {src} {vals} in {rid}")
        rep, lo, hi, con = (num(r.get(k)) for k in ("reported", "guide_low", "guide_high", "consensus"))
        if None not in (rep, lo, hi) and r.get("vs_guide"):
            want = "above" if rep > hi else "below" if rep < lo else "within"
            if r["vs_guide"] != want:
                probs.append(f"vs_guide {r['vs_guide']}, numbers say {want}")
        if None not in (rep, con) and r.get("vs_consensus"):
            want = "beat" if rep > con else "miss" if rep < con else "inline"
            if r["vs_consensus"] != want:
                probs.append(f"vs_consensus {r['vs_consensus']}, numbers say {want}")
        out.append({"table": "compare", "id": r.get("id"), "ok": not probs, "note": "; ".join(probs)})
    return out


def check(folder, facts):
    tables = {}
    for p in sorted(folder.glob("*.csv")):
        tables[p.stem] = list(csv.DictReader(open(p, newline="", encoding="utf-8")))
    out, summary = [], {}
    for table, rows in tables.items():
        if table not in CITES:
            continue
        c = Counter(rows=len(rows))
        for r in rows:
            row_ok = True
            for tcol, lcol, qcol in CITES[table]:
                rel, q = r.get(tcol) or "", r.get(qcol) or ""
                if not (rel or q):                          # a side left blank (added or removed text)
                    continue
                L = lines(rel)
                ln = int(r[lcol]) if str(r.get(lcol, "")).strip().isdigit() else 0
                exact, where = cite(L, ln, q)
                c["cites"] += 1
                c["exact"] += exact
                c["long"] += len(q) > 200
                row_ok &= exact
                res = {"table": table, "id": r.get("id"), "cite": tcol, "text": rel, "line": ln,
                       "exact": exact, "where": where, "long": len(q) > 200}
                if tcol == CITES[table][0][0] and table in VALUES:
                    vals = [num(r.get(k)) for k in VALUES[table] if num(r.get(k)) is not None]
                    if not vals and table == "guidance":    # a growth-only row ("16-17%"): its stated growth
                        vals = [float(m.replace(",", "")) for m in NUM.findall(r.get("growth_stated", ""))]
                    if vals:
                        res["value"] = exact and all(in_quote(v, q) for v in vals)
                        if not res["value"] and exact and all(v == 0 for v in vals) and "—" in q:
                            res["value"], res["note"] = "", "a dash recorded as 0"
                        c["valued"] += 1
                        c["value_ok"] += res["value"] is True
                    t = truth(table, r, facts)
                    if t:
                        res["truth"], res["concept"], res["dims"], res["xbrl"], res["note"] = t
                        c["truth_" + t[0]] += 1
                res["quote"] = q
                out.append(res)
            c["rows_ok"] += row_ok
        summary[table] = c
    if "compare" in tables:
        cmp_rows = check_compare(tables["compare"], tables)
        out += cmp_rows
        summary["compare"] = Counter(rows=len(cmp_rows), rows_ok=sum(x["ok"] for x in cmp_rows))
    return out, summary


def main(args):
    facts = xbrl()
    OUT.mkdir(exist_ok=True)
    cols = ["table", "id", "cite", "text", "line", "exact", "where", "long", "value", "truth", "concept", "dims",
            "xbrl", "ok", "note", "quote"]
    print("| Folder | Table | Rows | Citations exact | Over 200 chars | Value in quote | "
          "XBRL ok / other date / not found / not tagged |")
    print("|---|---|---|---|---|---|---|")
    for a in args:
        folder = (HERE / a).resolve()
        rows, summary = check(folder, facts)
        name = folder.relative_to(HERE).as_posix().replace("/", "_")
        with open(OUT / f"{name}.csv", "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, cols)
            w.writeheader()
            w.writerows(rows)
        for table, c in summary.items():
            if table == "compare":
                print(f"| {name} | compare | {c['rows']} | | | copies and labels right: {c['rows_ok']}/{c['rows']} | |")
                continue
            n = [c[f"truth_{k}"] for k in ("ok", "other_period", "not_found", "no_period")]
            t = " / ".join(map(str, n)) if sum(n) else ""
            v = f"{c['value_ok']}/{c['valued']}" if c["valued"] else ""
            print(f"| {name} | {table} | {c['rows']} | {c['exact']}/{c['cites']} | {c['long']} | {v} | {t} |")


if __name__ == "__main__":
    main(sys.argv[1:])
