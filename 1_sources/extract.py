"""Step 2 prep: every source as plain text with stable lines, so a reader can quote a line and a checker can
find that exact line again.

    python -B extract.py ZS

sources/<TICKER>/<path> -> text/<TICKER>/<path>.txt
  .htm   filing documents: text only (scripts, styles and the hidden iXBRL header dropped). Block tags and
         table rows end a line; a table row's cells are joined with " | ", a lone "$" joined to the next cell
         and a lone ")" or "%" to the one before.
  .pdf   a "=== page N ===" line before each page's text (pypdf)
  .xlsx  a "=== sheet NAME ===" line before each sheet, then one line per non-empty row, cells joined with
         " | " (values as Excel last saved them)
  transcript.txt (Whisper) and store/earnings_*.csv copied as is
  yahoo/*.json  pretty-printed, one key per line
Whitespace inside a line is collapsed to single spaces. Index pages, XBRL, the SEC JSON snapshots, audio
and the daily bars are not converted. The output depends only on the source bytes and this script, so it can be rebuilt.
"""
import json
import re
import sys
from datetime import date, datetime
from html.parser import HTMLParser
from pathlib import Path

import openpyxl
import pypdf

HERE = Path(__file__).resolve().parent
BLOCK = {"p", "div", "br", "li", "h1", "h2", "h3", "h4", "h5", "h6", "table", "title", "hr", "section"}
SKIP = {"script", "style", "ix:header"}


def clean(s):
    return re.sub(r"\s+", " ", s.replace("\xa0", " ")).strip()


def join_cells(cells):
    out = []
    for c in cells:
        if out and out[-1] == "$":
            out[-1] = "$" + c
        elif out and c in (")", "%", ")%", "%)"):
            out[-1] += c
        else:
            out.append(c)
    return " | ".join(out)


class Html(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lines, self.buf, self.cells, self.cell, self.skip, self.row = [], [], [], [], 0, False

    def end_line(self):
        s = clean("".join(self.buf))
        if s:
            self.lines.append(s)
        self.buf = []

    def handle_starttag(self, tag, attrs):
        if tag in SKIP:
            self.skip += 1
        elif self.skip:
            return
        elif tag == "tr":
            self.end_line()
            self.row, self.cells = True, []
        elif tag in ("td", "th"):
            self.cell = []
        elif tag in BLOCK and not self.row:
            self.end_line()

    def handle_endtag(self, tag):
        if tag in SKIP:
            self.skip = max(0, self.skip - 1)
        elif self.skip:
            return
        elif tag in ("td", "th") and self.row:
            c = clean("".join(self.cell))
            if c:
                self.cells.append(c)
            self.cell = []
        elif tag == "tr" and self.row:
            s = join_cells(self.cells)
            if s:
                self.lines.append(s)
            self.row, self.cells = False, []
        elif tag in BLOCK and not self.row:
            self.end_line()

    def handle_data(self, data):
        if self.skip:
            return
        (self.cell if self.row else self.buf).append(data)


def html_text(p):
    h = Html()
    h.feed(p.read_bytes().decode("utf-8", errors="replace"))
    h.end_line()
    return h.lines


def pdf_text(p):
    lines = []
    for i, page in enumerate(pypdf.PdfReader(p).pages, 1):
        lines.append(f"=== page {i} ===")
        lines += [s for s in (clean(x) for x in (page.extract_text() or "").splitlines()) if s]
    return lines


def cell(v):
    if isinstance(v, float):
        return str(int(v)) if v.is_integer() else repr(round(v, 6))
    if isinstance(v, (datetime, date)):
        return v.isoformat()[:10]
    return clean(str(v))


def xlsx_text(p):
    lines = []
    wb = openpyxl.load_workbook(p, data_only=True, read_only=True)
    for ws in wb.worksheets:
        lines.append(f"=== sheet {ws.title} ===")
        for row in ws.iter_rows(values_only=True):
            cells = [cell(v) for v in row if v is not None and cell(v)]
            if cells:
                lines.append(" | ".join(cells))
    wb.close()
    return lines


def convert(p):
    if p.suffix == ".htm" and p.name != "index.htm":
        return html_text(p)
    if p.suffix == ".pdf":
        return pdf_text(p)
    if p.suffix == ".xlsx":
        return xlsx_text(p)
    if p.name == "transcript.txt" or (p.parent.name == "store" and p.name.startswith("earnings_")):
        return p.read_text(encoding="utf-8").splitlines()
    if p.parent.name == "yahoo" and p.suffix == ".json":
        return json.dumps(json.loads(p.read_bytes()), indent=1).splitlines()
    return None


def main(sym):
    src, out = HERE / "sources" / sym, HERE / "text" / sym
    for p in sorted(src.rglob("*")):
        if not p.is_file():
            continue
        lines = convert(p)
        if lines is None:
            continue
        t = out / (p.relative_to(src).as_posix() + ".txt")
        t.parent.mkdir(parents=True, exist_ok=True)
        t.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"{len(lines):7d} lines  {t.relative_to(HERE).as_posix()}")


if __name__ == "__main__":
    main(sys.argv[1])
