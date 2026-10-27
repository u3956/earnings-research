"""Each name's GAAP figures by fiscal quarter, from its newest companyfacts snapshot (the SEC's XBRL store).

    python -B cyber/xbrl.py [TICKER ...]          (no ticker: every name in the cybersecurity group)

sources/<T>/sec/companyfacts_<date>.json -> cyber/xbrl/<T>.csv, one row per item and period:
  id, item, period (FY26Q3, or FY26 for a year), start, end, value, how, concept, accn, form, filed
how:
  3M       a quarter as filed
  YTD-YTD  a quarter as the difference of two year-to-date figures of the same year (the cash-flow lines,
           and Q4 = year - 9 months); never for per-share or share-count items
  12M      a fiscal year as filed
  instant  a balance-sheet figure at the period end
  cover    the shares on the cover of the newest 10-Q/10-K/20-F (all classes summed, from its own XBRL instance
           when on disk, else the companyfacts dei figure)
A period filed more than once keeps the newest filing's figure (a restated comparative wins); among an item's
concepts the first listed that has the period wins. 10-Q, 10-K and 20-F facts only; a 20-F filer has years only.
"""
import csv
import json
import re
import sys
from datetime import date
from pathlib import Path

PACK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PACK))
from fetch import COMPANIES, fiscal_q  # noqa: E402

THEMES = Path("themes.csv")  # the peer-group table, one row per group (not published)
FORMS = ("10-Q", "10-K", "20-F", "10-Q/A", "10-K/A", "20-F/A")
SINCE = "2023-01-01"                              # quarters ending from here: three years of y/y
ITEMS = [  # item, kind, additive (may be derived by subtraction), concepts in order of preference
    ("revenue", "dur", 1, "Revenues RevenueFromContractWithCustomerExcludingAssessedTax "
                          "RevenueFromContractWithCustomerIncludingAssessedTax"),
    ("gross_profit", "dur", 1, "GrossProfit"),
    ("rd", "dur", 1, "ResearchAndDevelopmentExpense ResearchAndDevelopmentExpenseExcludingAcquiredInProcessCost"),
    ("sm", "dur", 1, "SellingAndMarketingExpense"),
    ("ga", "dur", 1, "GeneralAndAdministrativeExpense"),
    ("operating_income", "dur", 1, "OperatingIncomeLoss"),
    ("net_income", "dur", 1, "NetIncomeLoss"),
    ("eps_diluted", "dur", 0, "EarningsPerShareDiluted"),
    ("shares_diluted", "dur", 0, "WeightedAverageNumberOfDilutedSharesOutstanding"),
    ("sbc", "dur", 1, "ShareBasedCompensation AllocatedShareBasedCompensationExpense"),
    ("ocf", "dur", 1, "NetCashProvidedByUsedInOperatingActivities"),
    ("capex", "dur", 1, "PaymentsToAcquirePropertyPlantAndEquipment PaymentsToAcquireProductiveAssets"),
    ("cap_software", "dur", 1, "PaymentsToDevelopSoftware PaymentsForSoftware"),
    ("acquisitions", "dur", 1, "PaymentsToAcquireBusinessesNetOfCashAcquired PaymentsToAcquireBusinessesGross"),
    ("buybacks", "dur", 1, "PaymentsForRepurchaseOfCommonStock"),
    ("cash", "inst", 0, "CashAndCashEquivalentsAtCarryingValue CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"),
    ("st_investments", "inst", 0, "ShortTermInvestments AvailableForSaleSecuritiesDebtSecuritiesCurrent "
                                  "MarketableSecuritiesCurrent DebtSecuritiesAvailableForSaleExcludingAccruedInterestCurrent"),
    ("lt_investments", "inst", 0, "LongTermInvestments AvailableForSaleSecuritiesDebtSecuritiesNoncurrent "
                                  "MarketableSecuritiesNoncurrent "
                                  "DebtSecuritiesAvailableForSaleExcludingAccruedInterestNoncurrent"),
    ("debt", "inst", 0, "LongTermDebt ConvertibleNotesPayable ConvertibleDebt DebtLongtermAndShorttermCombinedAmount "
                        "SecuredLongTermDebt"),
    ("debt_noncurrent", "inst", 0, "LongTermDebtNoncurrent ConvertibleDebtNoncurrent ConvertibleLongTermNotesPayable "
                                   "LongTermNotesPayable"),
    ("debt_current", "inst", 0, "LongTermDebtCurrent ConvertibleDebtCurrent ConvertibleNotesPayableCurrent"),
    ("deferred_revenue_current", "inst", 0, "ContractWithCustomerLiabilityCurrent DeferredRevenueCurrent"),
    ("deferred_revenue_noncurrent", "inst", 0, "ContractWithCustomerLiabilityNoncurrent DeferredRevenueNoncurrent"),
    ("rpo", "inst", 0, "RevenueRemainingPerformanceObligation"),
    ("goodwill", "inst", 0, "Goodwill"),
]
COLS = ["id", "item", "period", "start", "end", "value", "how", "concept", "accn", "form", "filed"]


def days(f):
    return (date.fromisoformat(f["end"]) - date.fromisoformat(f["start"])).days + 1


def months(f):
    """3, 6, 9 or 12 for a quarter or a year-to-date span (52/53-week years included), else None."""
    d = days(f)
    return next((m for m, lo, hi in ((3, 84, 100), (6, 175, 190), (9, 266, 282), (12, 357, 375)) if lo <= d <= hi),
                None)


def facts(us, concepts, unit):
    """{(start, end): fact}, the newest filing per period; an earlier concept in the list wins a period."""
    out = {}
    for c in concepts.split():
        best = {}
        for f in us.get(c, {}).get("units", {}).get(unit, []):
            if f["form"] in FORMS:
                k = (f.get("start", ""), f["end"])
                if k not in best or f["filed"] > best[k]["filed"]:
                    best[k] = dict(f, concept=c)
        for k, f in best.items():
            out.setdefault(k, f)
    return out


def cover_shares(sym, dei):
    """(value, end, concept, accn, form, filed, how) from the newest periodic filing's XBRL instance on disk."""
    fl = PACK / "sources" / sym / "filings.csv"
    rows = [r for r in csv.DictReader(open(fl, encoding="utf-8"))] if fl.exists() else []
    for r in sorted((r for r in rows if r["form"] in FORMS), key=lambda r: r["accepted_utc"], reverse=True):
        for x in (PACK / "sources" / sym / r["folder"]).glob("*.xml"):
            s = x.read_text(encoding="utf-8", errors="replace")
            vals = re.findall(r"<dei:EntityCommonStockSharesOutstanding\b[^>]*contextRef=\"([^\"]+)\"[^>]*>([\d.]+)<", s)
            if vals:
                ctx = vals[0][0]
                when = re.search(r'<(?:xbrli:)?context id="%s">.*?<(?:xbrli:)?instant>([\d-]+)<' % re.escape(ctx), s, re.S)
                return (sum(float(v) for _, v in vals), when.group(1) if when else "",
                        f"dei:EntityCommonStockSharesOutstanding, {len(vals)} class(es), {x.name}",
                        r["accession"], r["form"], r["filed"], "cover")
    best = max(dei.get("EntityCommonStockSharesOutstanding", {}).get("units", {}).get("shares", []),
               key=lambda f: f["end"], default=None)
    if best:
        return (best["val"], best["end"], "dei:EntityCommonStockSharesOutstanding (companyfacts)", best["accn"],
                best["form"], best["filed"], "cover")
    return None


def build(sym):
    snap = sorted((PACK / "sources" / sym / "sec").glob("companyfacts_*.json"))[-1]
    d = json.loads(snap.read_bytes())["facts"]
    us, fy_end = d.get("us-gaap", {}), COMPANIES[sym]["fy_end"]
    rows = []

    def add(item, period, f, value, how):
        rows.append(dict(item=item, period=period, start=f.get("start", ""), end=f["end"], value=value, how=how,
                         concept=f["concept"], accn=f["accn"], form=f["form"], filed=f["filed"]))

    ends = {e for (s, e), f in facts(us, ITEMS[0][3], "USD").items() if s and months(f)}  # the period ends
    for item, kind, additive, concepts in ITEMS:
        unit = "USD/shares" if item == "eps_diluted" else "shares" if item == "shares_diluted" else "USD"
        fx = facts(us, concepts, unit)
        if kind == "inst":
            for (_, end), f in sorted(fx.items()):
                if end >= SINCE and (end in ends or not ends):
                    add(item, fiscal_q(end, fy_end), f, f["val"], "instant")
            continue
        for c in concepts.split():           # a concept's whole series first, so one item keeps one concept
            spans = {k: f for k, f in facts(us, c, unit).items() if k[0] and months(f)}
            for (start, end), f in sorted(spans.items(), key=lambda kv: kv[0][1]):
                m = months(f)
                if end < SINCE:
                    continue
                if m == 12:
                    add(item, fiscal_q(end, fy_end)[:4], f, f["val"], "12M")
                if m == 3:
                    add(item, fiscal_q(end, fy_end), f, f["val"], "3M")
                elif additive and not any(k[1] == end and months(g) == 3 for k, g in spans.items()):
                    prev = [g for (s, e), g in spans.items() if s == start and months(g) == m - 3]
                    if prev:                 # same year start, three months shorter
                        p = prev[0]
                        q = dict(f, start=(date.fromordinal(date.fromisoformat(p["end"]).toordinal() + 1)).isoformat(),
                                 concept=f"{c} {f['start']}..{f['end']} minus {p['start']}..{p['end']}")
                        add(item, fiscal_q(end, fy_end), q, f["val"] - p["val"], "YTD-YTD")
    c = cover_shares(sym, d.get("dei", {}))
    if c:
        rows.append(dict(item="cover_shares", period="", start="", end=c[1], value=c[0], how=c[6], concept=c[2],
                         accn=c[3], form=c[4], filed=c[5]))
    seen, out = set(), []
    for r in rows:                           # one row per item, period and how (a 12M year and its Q4 both stay)
        k = (r["item"], r["period"], r["how"] if r["how"] in ("12M",) else "q")
        if k not in seen:
            seen.add(k)
            out.append(r)
    out.sort(key=lambda r: ([i[0] for i in ITEMS] + ["cover_shares"]).index(r["item"]) * 10**6 + int(
        r["end"].replace("-", "")[2:]) if r["end"] else 0)
    for i, r in enumerate(out, 1):
        r["id"] = f"X{i:03d}"
    dest = PACK / "cyber" / "xbrl" / f"{sym}.csv"
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(dest, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, COLS)
        w.writeheader()
        w.writerows(out)
    rev = {r["period"]: r["value"] for r in out if r["item"] == "revenue" and r["how"] in ("3M", "YTD-YTD")}
    qs = sorted(rev, key=lambda q: (q[2:4], q[5:]))[-4:]
    yoy = []
    for q in qs:
        ago = f"FY{int(q[2:4]) - 1:02d}{q[4:]}"
        yoy.append(f"{q} {rev[q] / 1e6:,.0f}" + (f" {rev[q] / rev[ago] - 1:+.0%}" if ago in rev else ""))
    print(f"{sym:5} {len(out):4} rows  {snap.name}  revenue: {' | '.join(yoy) or 'no quarters (20-F filer)'}")


def names():
    return [r["symbol"] for r in csv.DictReader(open(THEMES, encoding="utf-8")) if r["theme"] == "Cybersecurity"]


if __name__ == "__main__":
    for s in sys.argv[1:] or names():
        build(s)
