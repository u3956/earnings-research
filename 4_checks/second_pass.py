"""Step 3, second pass, the script part: what check.py cannot see, as far as a script can see it.

    python -B checks/second_pass.py > checks/out/second_pass_script.md

Release tables (reader A's and release B's):
  sums      each GAAP to non-GAAP reconciliation adds up: GAAP + the adjustments = non-GAAP, within the rounding of
            every printed term (per share: each term rounded to the cent)
  margins   stated margins against the reported figures they come from (operating, gross, FCF margin; FCF itself)
  columns   a row cited on a table line took the right column: the current quarter (or the balance sheet date) is
            the first number, the year to date the third; in the supplementals, the column under the quarter's header
  guidance  the heading each guidance row sits under, for reading by eye (printed for every row)
  consensus Yahoo rows sit under the right period, estimate and field; store rows in the right column of the right date
Call tables: the speaker label above each cited line of the official transcripts matches the row's speaker
(statements), the analyst (qa questions), and is not the analyst or the operator (qa answers).
Filing changes: an "added" passage is not already in the prior filing, a "removed" one is not still in the new one,
and a "changed" row's two quotes each appear only in their own filing.
"""
import csv
import re
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
TEXT = HERE / "text" / "ZS"
RELEASES = {"readers/release": "A", "readers/release_b": "B"}
RELEASE_Q = {"2025-11-25": "FY26Q1", "2026-02-26": "FY26Q2", "2026-05-26": "FY26Q3", "2026-09-03": "FY26Q4"}
FILINGS = {"FY26Q1": "sec/2025-11-25_10-Q_0001713683-25-000205/zs-20251031.htm.txt",
           "FY26Q2": "sec/2026-02-26_10-Q_0001713683-26-000048/zs-20260131.htm.txt",
           "FY26Q3": "sec/2026-05-26_10-Q_0001713683-26-000096/zs-20260430.htm.txt",
           "FY26": "sec/2026-09-03_10-K_0001713683-26-000157/zs-20260731.htm.txt"}
PRIOR = {"FY26Q2": "FY26Q1", "FY26Q3": "FY26Q2", "FY26": "FY26Q3"}
ADJ = {"gross_profit": ["sbc", "amortization_intangibles", "restructuring"],
       "operating_income": ["sbc", "amortization_intangibles", "acquisition_costs", "restructuring"],
       "net_income": ["sbc", "amortization_intangibles", "acquisition_costs", "restructuring", "debt_amortization",
                      "tax_adjustment"],
       "eps_diluted": ["sbc", "amortization_intangibles", "acquisition_costs", "restructuring", "debt_amortization",
                       "tax_adjustment", "other:share_count_adjustment", "other:fully_diluted_eps_adjustment",
                       "other:convertible_interest_net_of_tax_per_share"]}
_lines = {}


def lines(rel):
    if rel not in _lines:
        _lines[rel] = (TEXT / rel).read_text(encoding="utf-8").splitlines()
    return _lines[rel]


def read(p):
    return list(csv.DictReader(open(HERE / p, newline="", encoding="utf-8")))


def num(s):
    s = str(s).replace(",", "").replace("$", "").replace("%", "").strip()
    neg = s.startswith("(") and s.endswith(")")
    try:
        x = float(s.strip("()"))
    except ValueError:
        return None
    return -x if neg else x


def half(s):
    """Half the last printed digit of a value as written."""
    s = str(s).replace(",", "")
    return 0.5 * 10 ** -(len(s.split(".")[1]) if "." in s else 0)


def mult(scale):
    s = (scale or "").lower()
    return 1e9 if "bill" in s else 1e6 if "mill" in s else 1e3 if "thous" in s else 1.0


def money(r):
    """(value in dollars or units, its rounding) of a row."""
    m = 1 if "share" in (r.get("unit") or "") and "/" in r.get("unit", "") or r.get("unit") == "%" else mult(r.get("scale"))
    return num(r["value"]) * m, half(r["value"]) * m


def release_q(rel):
    m = re.match(r"sec/(\d{4}-\d\d-\d\d)_8-K", rel) or re.match(r"ir/(FY\d\dQ\d)/", rel)
    return RELEASE_Q.get(m[1], m[1]) if m else None


def sums(rows, who):
    out = []
    by = defaultdict(lambda: defaultdict(list))
    for r in rows:
        if num(r["value"]) is not None:
            by[(r["quarter"], r["measure"])][r["line_item"]].append(r)
    for (q, measure), items in sorted(by.items()):
        if measure not in ADJ or "gaap" not in items or "non_gaap" not in items:
            continue
        terms = [items["gaap"][0]] + [x for k in ADJ[measure] for x in items.get(k, [])]
        # net income: the tax adjustment is printed as an add to the GAAP tax provision, so it comes off net income
        sign = lambda x: -1 if measure == "net_income" and x["line_item"] == "tax_adjustment" else 1
        total = sum(sign(x) * money(x)[0] for x in terms)
        tol = sum(money(x)[1] for x in terms + items["non_gaap"][:1])
        if measure == "eps_diluted":
            tol = max(tol, 0.005 * len(terms) + 0.005)
        got = money(items["non_gaap"][0])[0]
        ok = abs(total - got) <= tol + 1e-9
        out.append(ok)
        if not ok:
            print(f"- {who} {q} {measure}: GAAP + {len(terms) - 1} adjustments = {total:,.2f}, non-GAAP {got:,.2f} "
                  f"(rows {', '.join(x['id'] for x in terms)}, {items['non_gaap'][0]['id']})")
        if measure == "net_income":                     # the pre-tax steps: GAAP + tax = pre-tax; pre-tax - tax = net
            first_of = lambda *names: next((items[n][0] for n in names if n in items), None)
            gtax = first_of("other:add_gaap_tax_provision", "other:gaap_tax_provision")
            steps = [(items["gaap"][0], gtax, first_of("other:gaap_pretax_income"), 1),
                     (gtax, first_of("tax_adjustment"), first_of("other:non_gaap_tax_provision"), 1),
                     (first_of("other:non_gaap_pretax_income"), first_of("other:non_gaap_tax_provision"), items["non_gaap"][0], -1)]
            for a, b, c, s in steps:
                if a and b and c:
                    ok = abs(money(a)[0] + s * money(b)[0] - money(c)[0]) <= money(a)[1] + money(b)[1] + money(c)[1]
                    out.append(ok)
                    if not ok:
                        print(f"- {who} {q} net income step {a['id']} {'+' if s > 0 else '-'} {b['id']} != {c['id']}")
    return out


def margins(rows, who):
    out = []
    by = {}
    for r in rows:
        if num(r["value"]) is not None:
            by.setdefault((r["quarter"], r["item"].replace("other:", ""), r["basis"], r["duration"] or "3M"), r)
    tests = [("operating_margin", "operating_income", "revenue"), ("gross_margin", "gross_profit", "revenue"),
             ("fcf_margin", "fcf", "revenue"), ("operating_cash_flow_margin", "operating_cash_flow", "revenue")]
    for (q, item, basis, dur), r in sorted(by.items()):
        for margin, top, bottom in tests:
            if item != margin:
                continue
            t = by.get((q, top, basis, dur)) or by.get((q, top, "non_gaap" if top == "fcf" else basis, dur))
            b = by.get((q, bottom, "gaap", dur))
            if not (t and b):
                continue
            (tv, tt), (bv, bt) = money(t), money(b)
            calc = 100 * tv / bv
            tol = half(r["value"]) + 100 * (tt / abs(bv) + abs(tv) * bt / bv ** 2) + 1e-9
            ok = abs(calc - num(r["value"])) <= tol
            out.append(ok)
            if not ok:
                print(f"- {who} {q} {basis} {margin} {r['value']}% ({r['id']}), from {t['id']}/{b['id']} {calc:.2f}%")
        if item == "fcf":
            parts = [by.get((q, "operating_cash_flow", "gaap", dur)), by.get((q, "capex_ppe", "gaap", dur)),
                     by.get((q, "capitalized_software", "gaap", dur))]
            if all(parts):
                vals = [money(x) for x in parts]
                calc = vals[0][0] - abs(vals[1][0]) - abs(vals[2][0])
                ok = abs(calc - money(r)[0]) <= sum(x[1] for x in vals) + money(r)[1]
                out.append(ok)
                if not ok:
                    print(f"- {who} {q} fcf {r['value']} ({r['id']}) vs OCF - capex - software {calc:,.0f}")
    return out


def cells(line):
    """Numbers of a table line, in order, after its label cell."""
    return [num(c) for c in line.split(" | ")[1:] if num(c) is not None]


def header(L, ln):
    """The quarter labels of the nearest header line above, in a supplemental sheet."""
    for x in reversed(L[:ln - 1]):
        if x.startswith("=== sheet"):
            return None
        labels = re.findall(r"Q(\d) FY(\d\d)", x)
        if len(labels) >= 2:
            return [f"FY{y}Q{n}" for n, y in labels]
    return None


def columns(table, rows, who):
    out = []
    for r in rows:
        line = lines(r["text"])[int(r["line"]) - 1]
        if " | " not in line or num(r["value"]) is None:
            continue
        nums = cells(line)
        v = num(r["value"])
        pos = [i for i, x in enumerate(nums) if abs(abs(x) - abs(v)) < 1e-9 * max(1, abs(v))]
        if len(nums) < 2 or not pos:
            continue
        q, dur = r["quarter"], r.get("duration") or "3M"
        if r["text"].endswith(".xlsx.txt"):
            h = header(lines(r["text"]), int(r["line"]))
            if not h or q not in h or dur not in ("3M", "instant"):
                continue
            want = h.index(q) + len(nums) - len(h)          # labels and numbers align from the right
        else:
            rq = release_q(r["text"])
            if q == rq and dur in ("3M", "instant"):
                want = 0
            elif (q == rq and dur in ("6M", "9M")) or (q == "FY26" and rq == "FY26Q4"):
                want = 2
            else:
                continue
        ok = want in pos
        out.append(ok)
        if not ok:
            print(f"- {who} {table} {r['id']} {q} {r.get('item') or r.get('measure')} {r.get('line_item', '')} {dur} "
                  f"= {r['value']}: number {pos[0] + 1} of {len(nums)} on {r['text'].split('/')[-1]}:{r['line']}, "
                  f"expected number {want + 1}")
    return out


def guidance(rows, who):
    print(f"\n#### {who}\n")
    print("| id | given in | for | item | basis | low-high | heading above it |")
    print("|---|---|---|---|---|---|---|")
    pat = re.compile(r"(first|second|third|fourth) quarter|full (fiscal )?year|fiscal (year )?20\d\d|\bQ[1-4]\b|FY ?2\d",
                     re.I)
    for r in rows:
        L, ln = lines(r["text"]), int(r["line"])
        head = next((x for x in reversed(L[max(0, ln - 25):ln]) if pat.search(x) and len(x) < 160), "")
        rng = f"{r['low']}-{r['high']}" if r["low"] else f"growth {r['growth_stated']}"
        print(f"| {r['id']} | {r['given_in']} | {r['target_period']} | {r['item']} | {r['basis']} | {rng} | "
              f"{head[:90].replace('|', '/')} |")


def consensus(rows, who):
    out = []
    period = {"FY27Q1": "0q", "FY27Q2": "+1q", "FY27": "0y", "FY28": "+1y"}
    field = {"avg": "avg", "low": "low", "high": "high", "analysts": "numberOfAnalysts", "count": "numberOfAnalysts"}
    store_head = lines("store/earnings_ZS_2026-10-25.csv.txt")[0].split(",")
    for r in rows:
        L, ln = lines(r["text"]), int(r["line"])
        if r["text"].startswith("store/"):
            row = dict(zip(store_head, L[ln - 1].split(",")))
            col = "estimate" if re.search(r"estimate|avg", r["item"]) else "reported"
            ok = row["date"] == r["as_of"] and num(row[col]) == num(r["estimate"])
            why = f"store line is {row['date']} {col} {row.get(col)}"
        else:
            keys, depth = [], 0                         # the objects that enclose the line, innermost first
            for x in reversed(L[:ln - 1]):
                depth += x.count("}") + x.count("]")
                opens = x.count("{") + x.count("[")
                if opens:
                    depth -= opens
                    if depth < 0:
                        m = re.match(r'\s*"(\w+)": [{\[]', x)
                        keys.append(m[1] if m else "")
                        depth = 0
                if len(keys) >= 2 and depth == 0 and (m := re.match(r'\s*"period": "([^"]+)"', x)):
                    keys.append(m[1])
                    break
            want = [field[r["item"].rsplit("_", 1)[1]],
                    "earningsEstimate" if r["item"].startswith("eps") else "revenueEstimate", period.get(r["quarter"])]
            ok = keys[:2] + keys[-1:] == want
            why = f"line sits under {' < '.join(keys)}; expected {' < '.join(want)}"
        out.append(ok)
        if not ok:
            print(f"- {who} {r['id']} {r['quarter']} {r['item']} = {r['estimate']}: {why}")
    return out


def speaker_at(L, ln):
    for x in reversed(L[:ln]):
        if x.strip() == "Operator":
            return "Operator"
        m = re.match(r"^([A-Z][^|=]{2,40}?) - .{2,60} - .{2,80}$", x)
        if m:
            return m[1].strip()
    return ""


def same(a, b):
    a, b = a.lower(), b.lower()
    return bool(a and b) and (a.split()[-1] in b or b.split()[-1] in a)


def speakers():
    out = []
    for r in read("readers/call/statements.csv"):
        if not r["text"].startswith("ir/FY"):
            continue
        s = speaker_at(lines(r["text"]), int(r["line"]))
        ok = same(s, r["speaker"])
        out.append(ok)
        if not ok:
            print(f"- statements {r['id']} {r['event']}: row says {r['speaker']}, label above line {r['line']} is {s!r}")
    for r in read("readers/call/qa.csv"):
        if not r["q_text"].startswith("ir/FY"):
            continue
        q = speaker_at(lines(r["q_text"]), int(r["q_line"]))
        a = speaker_at(lines(r["a_text"]), int(r["a_line"]))
        ok_q, ok_a = same(q, r["analyst"]), a not in ("Operator", "") and not same(a, r["analyst"])
        out += [ok_q, ok_a]
        if not ok_q:
            print(f"- qa {r['id']} question: row says {r['analyst']}, label above line {r['q_line']} is {q!r}")
        if not ok_a:
            print(f"- qa {r['id']} answer: label above line {r['a_line']} is {a!r} (analyst {r['analyst']})")
    return out


def changes():
    out = []
    squash = lambda s: re.sub(r"\s+", " ", s).strip()
    text = {f: squash("\n".join(lines(p))) for f, p in FILINGS.items()}
    for r in read("readers/filings/changes.csv"):
        f, kind = r["filing"], r["change"]
        if f not in PRIOR or kind == "event":
            continue
        new, old = text[f], text[PRIOR[f]]
        q, pq = squash(r["quote"]), squash(r["prior_quote"])
        probs = []
        if kind in ("added", "changed") and q and q in old:
            probs.append("its quote is already in the prior filing")
        if kind in ("removed", "changed") and pq and pq in new:
            probs.append("its prior quote is still in the new filing")
        if kind == "changed" and not pq:
            probs.append("no prior quote")
        out.append(not probs)
        if probs:
            print(f"- {r['id']} {f} {kind} {r['kind']}: {'; '.join(probs)}. {r['summary'][:110]}")
    return out


def count(name, oks):
    print(f"\n{name}: {sum(oks)} of {len(oks)} pass\n")


def main():
    print("# Second pass, script part\n")
    for folder, who in RELEASES.items():
        print(f"## {who}: release tables\n")
        res, br = read(f"{folder}/results.csv"), read(f"{folder}/bridge.csv")
        print("### Reconciliations add up")
        count("sums", sums(br, who))
        print("### Margins and FCF from their parts")
        count("margins", margins(res, who))
        print("### Right column")
        count("columns", columns("results", res, who) + columns("bridge", br, who))
        print("### Consensus rows")
        count("consensus", consensus(read(f"{folder}/consensus.csv"), who))
    print("## Call tables: speaker labels (official transcripts)\n")
    count("speakers", speakers())
    print("## Filing changes: added, removed, changed\n")
    count("changes", changes())
    print("## Guidance: the heading above each row (read by eye)")
    for folder, who in RELEASES.items():
        guidance(read(f"{folder}/guidance.csv"), who)


if __name__ == "__main__":
    main()
