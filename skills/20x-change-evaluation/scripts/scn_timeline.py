#!/usr/bin/env python3
"""Compute Significant Change Notification dates for a change, from the FedRAMP rules data.

  scn_timeline.py notices --type TYPE [--start DATE] [--finish DATE] [--verified DATE] [--holidays FILE]
  scn_timeline.py bizdays --from DATE --days N [--before] [--holidays FILE]

TYPE is one of: transformative, adaptive, routine_recurring, not_significant, class_change.
Each notice's timeframe (number and unit) is read from the rule with frmr.py, never typed here.
The direction of each rule (before the start, after the finish, after verification) is
listed in RULES below, from the rule statements.

Business days: the FedRAMP rules do not define them. By default this script counts Monday to
Friday and skips US federal holidays on their observed dates. --no-federal-holidays counts
weekdays only; --holidays adds a file of extra YYYY-MM-DD dates to skip (for example a client's
own holidays). The output states which basis was used, so the consultant can confirm it.
"""
import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bizdays  # noqa: E402
import frmr  # noqa: E402

# rule ID -> (event the timeframe counts from, direction)
RULES = {
    "transformative": [("SCN-TRF-NIP", "start", "before"), ("SCN-TRF-NFP", "start", "before"),
                       ("SCN-TRF-NAF", "finish", "after"), ("SCN-TRF-NAV", "verified", "after"),
                       ("SCN-TRF-UPD", "finish", "after")],
    "adaptive": [("SCN-ADP-NTF", "finish", "after")],
    "routine_recurring": [],
    "not_significant": [],
    "class_change": [],
}
NOTES = {
    "routine_recurring": "No notice: read SCN-RTR-NNR. Record the evaluation (SCN-CSO-MAR).",
    "not_significant": "Not a significant change: no notice. Record the evaluation and who decided (SCN-CSO-EVA, SCN-CSO-MAR).",
    "class_change": "A change of certification class needs a new assessment and is not handled under the notification rules: read the evaluation steps under SCN-CSO-EVA.",
    "transformative": "Read SCN-TRF-TPR (third-party review before starting) and SCN-CSO-INF (required content).",
    "adaptive": "Read SCN-CSO-INF (required content).",
}


def add_bizdays(d: date, n: int, holidays: set, before: bool = False) -> date:
    step = -1 if before else 1
    left = n
    while left:
        d += timedelta(days=step)
        if d.weekday() < 5 and d not in holidays:
            left -= 1
    return d


def notices(a):
    data = frmr.load()
    known = [date.fromisoformat(x) for x in (a.start, a.finish, a.verified) if x] or [date.today()]
    hol = bizdays.holiday_set(min(known), max(known), not a.no_federal_holidays, a.holidays)
    events = {"start": a.start, "finish": a.finish, "verified": a.verified}
    out = []
    for rid, event, direction in RULES[a.type]:
        found = [r for i, f, s, r in frmr.iter_rules(data, "c", "20x") if i == rid]
        if not found:
            sys.exit(f"{rid} is not in the rules data for Class C 20x; check the pinned FRMR version")
        r = found[0]
        unit, num = r.get("timeframe_type"), r.get("timeframe_num")
        item = {"rule": rid, "name": r["name"], "force": r.get("force"), "counts_from": event,
                "direction": direction, "timeframe": f"{num} {unit}"}
        ev = events[event]
        if ev and unit == "bizdays":
            due = add_bizdays(date.fromisoformat(ev), int(num), hol, before=(direction == "before"))
            item["due"] = due.isoformat()
            item["due_meaning"] = "latest date to send" if direction == "after" else "send on or before"
        elif ev:
            item["due"] = None
            item["due_meaning"] = f"timeframe unit {unit} is not business days; compute by hand"
        else:
            item["due"] = None
            item["due_meaning"] = f"needs the {event} date"
        out.append(item)
    print(json.dumps({"type": a.type, "frmr_commit": frmr.COMMIT,
                      "business_days": bizdays.basis(not a.no_federal_holidays, a.holidays) + " (FedRAMP does not define business days; confirm with the consultant)",
                      "notices": out, "note": NOTES[a.type]}, indent=2))


def cmd_bizdays(a):
    start = date.fromisoformat(a.from_)
    d = add_bizdays(start, a.days, bizdays.holiday_set(start, start, not a.no_federal_holidays, a.holidays), before=a.before)
    print(d.isoformat())


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("notices")
    p.add_argument("--type", required=True, choices=list(RULES))
    p.add_argument("--start")
    p.add_argument("--finish")
    p.add_argument("--verified")
    p.add_argument("--holidays")
    p.add_argument("--no-federal-holidays", action="store_true")
    q = sub.add_parser("bizdays")
    q.add_argument("--from", dest="from_", required=True)
    q.add_argument("--days", type=int, required=True)
    q.add_argument("--before", action="store_true")
    q.add_argument("--holidays")
    q.add_argument("--no-federal-holidays", action="store_true")
    a = ap.parse_args(argv)
    (notices if a.cmd == "notices" else cmd_bizdays)(a)


if __name__ == "__main__":
    main()
