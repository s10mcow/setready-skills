#!/usr/bin/env python3
"""Write the editable parts of a SetReady skill report to a spreadsheet.

    python3 sheet.py report.json report.xlsx

Needs openpyxl (pip install openpyxl). It reads the same report.json as report.py and
writes one sheet for each table section that has a "sheet" name. Extra keys a section can
carry for the spreadsheet:

    "sheet": "Budget"                       the sheet's name
    "money_columns": [1]                    columns holding dollar amounts; "-" becomes blank
    "extra_columns": ["Quote date", "Notes"]  empty columns the user fills in
    "choices": {"Status": ["Not started", "Applied", "Approved"]}  drop-down lists
    "target": {"label": "Target sale price", "amount": "$270,000"}  only when selling

A "workbook" list at the top level orders the sheets by name. Amounts are only ever the
user's numbers; the sheet adds them up and counts the lines still waiting on a quote.
"""

import json
import re
import sys

try:
    from openpyxl import Workbook
    from openpyxl.formatting.rule import FormulaRule
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.datavalidation import DataValidation
except ImportError:
    sys.exit("openpyxl is missing. Install it with: pip install openpyxl")

INK = "171717"
MUTE = "888888"
HAIR = "EBEBEB"
NEEDS_QUOTE = "FFF8EC"
MONEY = '"$"#,##0'
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")

TITLE = Font(name="Arial", size=14, bold=True, color=INK)
SUBTITLE = Font(name="Arial", size=9, color=MUTE)
HEAD = Font(name="Arial", size=9, bold=True, color="FFFFFF")
BODY = Font(name="Arial", size=10, color="333333")
BOLD = Font(name="Arial", size=10, bold=True, color=INK)
NOTE = Font(name="Arial", size=8, italic=True, color=MUTE)
LINK = Font(name="Arial", size=10, color="0070F3", underline="single")
HEAD_FILL = PatternFill("solid", fgColor=INK)
QUOTE_FILL = PatternFill("solid", fgColor=NEEDS_QUOTE)
WRAP = Alignment(wrap_text=True, vertical="top")
RULE = Border(bottom=Side(style="thin", color=HAIR))
TOP_RULE = Border(top=Side(style="medium", color=INK))


def plain(value):
    """Text without markdown: **bold** loses its stars and [label](link) keeps the label."""
    text = str(value if value is not None else "")
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    return LINK_RE.sub(r"\1", text)


def only_link(value):
    match = LINK_RE.fullmatch(str(value or "").strip())
    return (match.group(1), match.group(2)) if match else None


def money(value):
    """$162,300 -> 162300. Blank, "-" and anything that isn't a single amount -> None."""
    text = str(value if value is not None else "").strip()
    if re.fullmatch(r"\$?\s*-?[\d,]+(\.\d+)?", text):
        return float(text.replace("$", "").replace(",", "").strip())
    return None


def is_blank_amount(value):
    return str(value if value is not None else "").strip() in ("", "-", "–", "—")


def write_sheet(book, data, section):
    ws = book.create_sheet(section["sheet"][:31])
    columns = list(section.get("columns") or [])
    extras = list(section.get("extra_columns") or [])
    headers = columns + extras
    money_cols = set(section.get("money_columns") or [])
    weights = section.get("widths") or [1] * len(columns)
    total_weight = float(sum(weights)) or 1.0

    ws["A1"] = section.get("title", section["sheet"])
    ws["A1"].font = TITLE
    subtitle = " · ".join(plain(x) for x in [data.get("title"), data.get("subtitle")] if x)
    date = next((value for label, value in data.get("meta") or [] if str(label).lower() == "date"), "")
    ws["A2"] = subtitle + (" · " + str(date) if date else "")
    ws["A2"].font = SUBTITLE

    head_row = 4
    for col, name in enumerate(headers, start=1):
        cell = ws.cell(row=head_row, column=col, value=plain(name))
        cell.font = HEAD
        cell.fill = HEAD_FILL
        cell.alignment = Alignment(vertical="center", wrap_text=True)
    ws.row_dimensions[head_row].height = 20
    for col in range(len(columns)):
        ws.column_dimensions[get_column_letter(col + 1)].width = max(10, round(110 * weights[col] / total_weight))
    for col in range(len(columns), len(headers)):
        ws.column_dimensions[get_column_letter(col + 1)].width = 28 if "note" in headers[col].lower() else 16

    first = head_row + 1
    rows = section.get("rows") or []
    for offset, row in enumerate(rows):
        r = first + offset
        row = list(row) + [""] * (len(columns) - len(row))
        for col, value in enumerate(row[:len(columns)]):
            cell = ws.cell(row=r, column=col + 1)
            if col in money_cols:
                amount = money(value)
                if amount is not None:
                    cell.value = amount
                    cell.number_format = MONEY
                elif is_blank_amount(value):
                    cell.number_format = MONEY
                else:
                    cell.value = plain(value)
            else:
                link = only_link(value)
                if link:
                    cell.value, cell.hyperlink = link
                    cell.font = LINK
                    cell.alignment = WRAP
                    cell.border = RULE
                    continue
                cell.value = plain(value)
            cell.font = BODY
            cell.alignment = WRAP
            cell.border = RULE
        for col in range(len(columns), len(headers)):
            cell = ws.cell(row=r, column=col + 1)
            cell.alignment = WRAP
            cell.border = RULE
            cell.font = BODY
    last = first + len(rows) - 1

    for name, options in (section.get("choices") or {}).items():
        if name not in headers or not options:
            continue
        letter = get_column_letter(headers.index(name) + 1)
        rule = DataValidation(type="list", formula1='"%s"' % ",".join(str(o).replace(",", " ") for o in options), allow_blank=True)
        ws.add_data_validation(rule)
        rule.add("%s%d:%s%d" % (letter, first, letter, max(last, first) + 50))

    for col in sorted(money_cols):
        if rows:
            letter = get_column_letter(col + 1)
            span = "%s%d:%s%d" % (letter, first, letter, last)
            ws.conditional_formatting.add(span, FormulaRule(formula=["ISBLANK(%s%d)" % (letter, first)], fill=QUOTE_FILL))

    r = last + 2
    if money_cols and rows:
        label_col = 1
        amount_col = min(money_cols) + 1
        letter = get_column_letter(amount_col)
        span = "%s%d:%s%d" % (letter, first, letter, last)
        ws.cell(row=r, column=label_col, value="Total of the lines with amounts").font = BOLD
        total = ws.cell(row=r, column=amount_col, value="=SUM(%s)" % span)
        total.font = BOLD
        total.number_format = MONEY
        for col in range(1, len(headers) + 1):
            ws.cell(row=r, column=col).border = TOP_RULE
        ws.cell(row=r + 1, column=label_col, value="Lines still waiting on a quote").font = BODY
        ws.cell(row=r + 1, column=amount_col, value="=COUNTBLANK(%s)" % span).font = BOLD
        total_ref = "%s%d" % (letter, r)
        r += 2
        target = section.get("target")
        if target and money(target.get("amount")) is not None:
            ws.cell(row=r, column=label_col, value=plain(target.get("label", "Target sale price"))).font = BODY
            cell = ws.cell(row=r, column=amount_col, value=money(target["amount"]))
            cell.number_format = MONEY
            cell.font = BOLD
            ws.cell(row=r + 1, column=label_col, value="Target minus the lines with amounts").font = BODY
            cell = ws.cell(row=r + 1, column=amount_col, value="=%s%d-%s" % (letter, r, total_ref))
            cell.number_format = MONEY
            cell.font = BOLD
            ws.cell(row=r + 1, column=amount_col + 1, value="Not a profit until every line has a quote.").font = NOTE
            r += 2
        ws.cell(row=r, column=label_col, value="Shaded amounts still need a quote. Type a quote in and the totals update.").font = NOTE
        r += 1

    for line in [data.get("footer")] + list(data.get("closing") or []):
        if line:
            cell = ws.cell(row=r + 1, column=1, value=plain(line))
            cell.font = NOTE
            if plain(line).split(":", 1)[0] in ("http", "https"):
                cell.hyperlink = plain(line)
            r += 1

    ws.freeze_panes = ws.cell(row=first, column=1)
    if rows:
        ws.auto_filter.ref = "A%d:%s%d" % (head_row, get_column_letter(len(headers)), last)
    ws.sheet_view.showGridLines = False
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True


def build(data, out_path):
    sections = [s for s in data.get("sections") or [] if s.get("kind") == "table" and s.get("sheet")]
    if not sections:
        sys.exit('report.json has no table section with a "sheet" name')
    order = data.get("workbook") or []
    sections.sort(key=lambda s: order.index(s["sheet"]) if s["sheet"] in order else len(order))
    book = Workbook()
    book.remove(book.active)
    for section in sections:
        write_sheet(book, data, section)
    book.properties.title = plain(data.get("title", ""))
    book.properties.creator = "SetReady agent skill"
    book.save(out_path)


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python3 sheet.py report.json report.xlsx")
    with open(sys.argv[1], encoding="utf-8") as handle:
        data = json.load(handle)
    build(data, sys.argv[2])
    print("Wrote " + sys.argv[2])


if __name__ == "__main__":
    main()
