#!/usr/bin/env python3
"""Compute an incident's reporting timeline from the client's own targets.

  incident_timeline.py --event declared=2027-01-12T09:40-05:00 --event reportable=2027-01-12T10:20-05:00 \
      --target "reportability:1h:declared" --target "rating:4h:reportable" \
      --target "initial_report:1h:clock" --target "ongoing_report:24h:clock:repeat" \
      --target "final_report:5bd:resolved" [--clock-start reportable] [--holidays FILE] [--now ...]

The FedRAMP incident rules set no fixed hours: the times come from the client's plan, each
passed as NAME:AMOUNT:FROM, where AMOUNT ends in m, h, d (calendar) or bd (business days),
and FROM is an event name or "clock". The reporting clock starts at the event named by
--clock-start (default: reportable, the reportability decision; lesson L8), never at
detection unless the client's plan says so. A target whose event is unknown shows "needs <event>".
With --now, each due time already passed is marked overdue unless --done NAME=TIME was given.
Business days count Monday to Friday; --holidays skips listed dates (YYYY-MM-DD per line).
"""
import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path


def add(t: datetime, amount: str, holidays: set) -> datetime:
    if amount.endswith("bd"):
        n, d = int(amount[:-2]), t
        while n:
            d += timedelta(days=1)
            if d.weekday() < 5 and d.date() not in holidays:
                n -= 1
        return d
    n, unit = int(amount[:-1]), amount[-1]
    return t + {"m": timedelta(minutes=n), "h": timedelta(hours=n), "d": timedelta(days=n)}[unit]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--event", action="append", default=[], help="NAME=ISO time with offset")
    ap.add_argument("--target", action="append", default=[], help="NAME:AMOUNT:FROM[:repeat]")
    ap.add_argument("--clock-start", default="reportable")
    ap.add_argument("--done", action="append", default=[], help="NAME=ISO time the target was met")
    ap.add_argument("--now")
    ap.add_argument("--holidays")
    a = ap.parse_args(argv)
    from datetime import date
    hol = {date.fromisoformat(x.strip()) for x in Path(a.holidays).read_text().splitlines() if x.strip()} if a.holidays else set()
    ev = {k: datetime.fromisoformat(v) for k, v in (e.split("=", 1) for e in a.event)}
    if a.clock_start in ev:
        ev["clock"] = ev[a.clock_start]
    done = {k: datetime.fromisoformat(v) for k, v in (x.split("=", 1) for x in a.done)}
    now = datetime.fromisoformat(a.now) if a.now else None
    out = []
    for t in a.target:
        parts = t.split(":")
        name, amount, frm = parts[0], parts[1], parts[2]
        repeat = len(parts) > 3 and parts[3] == "repeat"
        item = {"target": name, "amount": amount, "from": frm, "repeats": repeat}
        if frm not in ev:
            item["due"] = None
            item["status"] = f"needs {frm}"
        else:
            due = add(ev[frm], amount, hol)
            item["due"] = due.isoformat()
            if name in done:
                item["status"] = "met" if done[name] <= due else f"late by {done[name] - due}"
            elif now and now > due:
                item["status"] = "overdue"
            else:
                item["status"] = "due"
        out.append(item)
    print(json.dumps({"clock_starts_at": a.clock_start, "clock": ev.get("clock").isoformat() if "clock" in ev else None,
                      "business_days": f"Monday to Friday, holidays from {a.holidays}" if a.holidays else "Monday to Friday, no holidays skipped",
                      "timeline": out}, indent=2))


if __name__ == "__main__":
    main()
