#!/usr/bin/env python3
"""Compute an incident's reporting timeline from the client's own targets.

  incident_timeline.py --event declared=2027-01-12T09:40-05:00 --event reportable=2027-01-12T10:20-05:00 \
      --target "reportability:1h:declared" --target "rating:4h:reportable" \
      --target "initial_report:1h:clock" --target "ongoing_report:24h:clock:repeat" \
      --target "final_report:5bd:resolved" [--clock-start reportable] [--holidays FILE] [--now ...]

Two sets of times. FedRAMP's own: the rules data gives IEC-CSO-IIR, IEC-CSO-OIR and IEC-CSO-FIR
a timeframe for each PAIN rating (pain_timeframes). Pass --rating N (the rating in force, 5 by
default under IEC-CSO-DPR) and the script adds them as rule targets: the initial report counted
from the reportable event (the rule says "after identifying"), ongoing reports repeating from the
clock, and the final report counted from the resolved event (the rule says "once the incident has
been resolved"). These starting events are this script's reading of the rule statements; confirm
them with the consultant. The client's plan adds its own targets, each
passed as NAME:AMOUNT:FROM, where AMOUNT ends in m, h, d (calendar) or bd (business days),
and FROM is an event name or "clock". The reporting clock starts at the event named by
--clock-start (default: reportable, the reportability decision; lesson L8), never at
detection unless the client's plan says so. A target whose event is unknown shows "needs <event>".
With --now, each due time already passed is marked overdue unless --done NAME=TIME was given.
Business days count Monday to Friday and skip US federal holidays on their observed dates by
default; --no-federal-holidays counts weekdays only, and --holidays skips extra listed dates.
"""
import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bizdays  # noqa: E402
import frmr  # noqa: E402

RULE_REPORTS = (("IEC-CSO-IIR", "iir", "initial_report", "reportable", False),
                ("IEC-CSO-OIR", "oir", "ongoing_report", "clock", True),
                ("IEC-CSO-FIR", "fir", "final_report", "resolved", False))


def rule_targets(rating: int, cls: str = "c") -> list:
    """FedRAMP's timeframes for one PAIN rating at the class, from the pinned rules data.

    At Class A, IEC-CSO-FIR is a MUST (FRC-CLA-MFR) and IEC-CSO-IIR and OIR are SHOULD
    (FRC-CLA-RFR); the output names the force for each.
    """
    d = frmr.load()
    recs = {rid: r for rid, _f, _s, r in frmr.iter_rules(d, cls, "20x")}
    out = []
    for rid, key, name, frm, repeat in RULE_REPORTS:
        tf = ((recs.get(rid) or {}).get("pain_timeframes") or {}).get(str(rating), {}).get(key)
        if not tf:
            sys.exit(f"{rid} has no timeframe for N{rating} at class {cls.upper()} in the pinned rules data")
        unit = {"hours": "h", "bizdays": "bd", "days": "d", "minutes": "m"}.get(tf["timeframe_type"])
        if not unit:
            sys.exit(f"{rid}: timeframe unit {tf['timeframe_type']} is not handled; compute by hand")
        out.append((f"{name}_rule", f"{tf['timeframe_num']}{unit}", frm, repeat, rid))
        FORCES[rid] = recs[rid].get("class_a_force") or recs[rid].get("force")
    return out


FORCES = {}


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
    ap.add_argument("--no-federal-holidays", action="store_true")
    ap.add_argument("--rating", type=int, choices=range(0, 6), help="PAIN rating in force; adds FedRAMP's timeframes")
    ap.add_argument("--class", dest="cls", default="c", choices=["a", "b", "c"], help="certification class (default c)")
    a = ap.parse_args(argv)
    from datetime import date
    ev = {k: datetime.fromisoformat(v) for k, v in (e.split("=", 1) for e in a.event)}
    span = [t.date() for t in ev.values()] or [date.today()]
    hol = bizdays.holiday_set(min(span), max(span), not a.no_federal_holidays, a.holidays)
    if a.clock_start in ev:
        ev["clock"] = ev[a.clock_start]
    done = {k: datetime.fromisoformat(v) for k, v in (x.split("=", 1) for x in a.done)}
    now = datetime.fromisoformat(a.now) if a.now else None
    out = []
    targets = []
    for t in a.target:
        parts = t.split(":")
        targets.append((parts[0], parts[1], parts[2], len(parts) > 3 and parts[3] == "repeat", "client plan"))
    if a.rating is not None and a.rating > 0:
        targets += rule_targets(a.rating, a.cls)
    for name, amount, frm, repeat, source in targets:
        item = {"target": name, "amount": amount, "from": frm, "repeats": repeat, "set_by": source}
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
    later = []
    for it in out:
        if it["set_by"] == "client plan":
            rule = next((r for r in out if r["target"] == it["target"] + "_rule"), None)
            if rule and it["due"] and rule["due"] and it["due"] > rule["due"]:
                later.append(f"{it['target']}: the plan's target ({it['amount']} from {it['from']}) falls after "
                             f"{rule['set_by']} for N{a.rating} ({rule['amount']} from {rule['from']})")
            elif rule and it["from"] == rule["from"] and add(datetime(2000, 1, 3), it["amount"], set()) > add(datetime(2000, 1, 3), rule["amount"], set()):
                later.append(f"{it['target']}: the plan's interval {it['amount']} is longer than {rule['set_by']} for N{a.rating} ({rule['amount']})")
    print(json.dumps({"class": a.cls.upper(), "rule_force": FORCES, "clock_starts_at": a.clock_start, "rating": a.rating, "plan_later_than_rules": later, "clock": ev.get("clock").isoformat() if "clock" in ev else None,
                      "business_days": bizdays.basis(not a.no_federal_holidays, a.holidays),
                      "timeline": out}, indent=2))


if __name__ == "__main__":
    main()
