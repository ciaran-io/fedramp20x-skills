"""Business day counting for the fedramp20x-skills timeline scripts.

FedRAMP does not define business days. The skills count Monday to Friday and skip US
federal holidays on their observed dates by default (decision of 22 Nov 2026), and record
that basis in each deliverable so the consultant can confirm or change it.
"""
def federal_holidays(year: int) -> set:
    """US federal holidays for a year, on their observed dates (5 U.S.C. 6103).

    A holiday on a Saturday is observed on the Friday before, and one on a Sunday on the
    Monday after. Inauguration Day is not included.
    """
    from datetime import date, timedelta

    def nth(month, weekday, n):
        d = date(year, month, 1)
        d += timedelta(days=(weekday - d.weekday()) % 7)
        return d + timedelta(weeks=n - 1)

    def last(month, weekday):
        d = date(year, month + 1, 1) - timedelta(days=1)
        return d - timedelta(days=(d.weekday() - weekday) % 7)

    def observed(d):
        return d - timedelta(days=1) if d.weekday() == 5 else d + timedelta(days=1) if d.weekday() == 6 else d

    fixed = [date(year, 1, 1), date(year, 6, 19), date(year, 7, 4), date(year, 11, 11), date(year, 12, 25)]
    floating = [nth(1, 0, 3), nth(2, 0, 3), last(5, 0), nth(9, 0, 1), nth(10, 0, 2), nth(11, 3, 4)]
    days = {observed(d) for d in fixed} | set(floating)
    nxt = date(year + 1, 1, 1)
    if nxt.weekday() == 5:  # next New Year's Day on a Saturday is observed on 31 December
        days.add(date(year, 12, 31))
    return days


def holidays_between(start, end) -> set:
    out = set()
    for y in range(min(start.year, end.year) - 1, max(start.year, end.year) + 2):
        out |= federal_holidays(y)
    return out


BASIS_DEFAULT = "Monday to Friday, skipping US federal holidays on their observed dates (5 U.S.C. 6103)"
BASIS_WEEKDAYS = "Monday to Friday only; holidays not skipped"


def holiday_set(start, end, use_federal=True, extra_file=None):
    from datetime import date
    from pathlib import Path
    days = holidays_between(start, end) if use_federal else set()
    if extra_file:
        days |= {date.fromisoformat(x.strip()) for x in Path(extra_file).read_text().splitlines() if x.strip()}
    return days


def basis(use_federal=True, extra_file=None):
    b = BASIS_DEFAULT if use_federal else BASIS_WEEKDAYS
    return b + (f"; also skipping the dates in {extra_file}" if extra_file else "")
