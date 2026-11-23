#!/usr/bin/env python3
"""Summarise daily KSI validation history for the Security Decision Record metrics (SDR-CSX-KMT).

  kmt_metrics.py HISTORY_FOLDER --as-of YYYY-MM-DD [--ksi KSI-ID ...]

HISTORY_FOLDER holds one JSON file per day: {"date": "YYYY-MM-DD", "ksi_status": {KSI-ID: status}}.
Files marked "synthetic": true are counted separately and never mixed into the summaries.
For each KSI it prints the days covered, the count of each status over the past 30 days and
up to the past year (only days on or before --as-of), the first and last day, and the daily
statuses. Each window is the full 30 or 365 days ending on --as-of. Days in the window before the
first history file are counted as days_before_history, and days after it with no file as
missing_days, so a short history is never reported as a complete window.
"""
import argparse
import json
from collections import Counter
from datetime import date, timedelta
from pathlib import Path


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder", type=Path)
    ap.add_argument("--as-of", type=date.fromisoformat, required=True)
    ap.add_argument("--ksi", action="extend", nargs="+", help="one or more KSI IDs; may repeat")
    a = ap.parse_args(argv)
    days, synthetic = {}, []
    for p in sorted(a.folder.glob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        day = date.fromisoformat(d["date"])
        if day > a.as_of:
            continue
        if d.get("synthetic"):
            synthetic.append(d["date"])
            continue
        days[day] = d["ksi_status"]
    if not days:
        raise SystemExit("no real history on or before the run date")
    first = min(days)
    ksis = a.ksi or sorted({k for v in days.values() for k in v})
    out = {"as_of": a.as_of.isoformat(), "first_day": first.isoformat(), "days_with_history": len(days),
           "synthetic_days_excluded": synthetic, "ksis": {}}
    for window, name in ((30, "past_30_days"), (365, "up_to_past_year")):
        start = a.as_of - timedelta(days=window - 1)
        present = [d for d in days if d >= start]
        before = max(0, (first - start).days)
        out[f"{name}_window"] = {"from": start.isoformat(), "to": a.as_of.isoformat(), "days_in_window": window,
                                 "days_present": len(present), "days_before_history": before,
                                 "missing_days": [(start + timedelta(days=i)).isoformat() for i in range(window)
                                                  if start + timedelta(days=i) >= first and (start + timedelta(days=i)) not in days],
                                 "coverage": f"covers {len(present)} days, not {window}" if len(present) < window else f"covers all {window} days"}
    for k in ksis:
        daily = {d.isoformat(): days[d].get(k, "absent") for d in sorted(days)}
        entry = {"daily": daily}
        for window, name in ((30, "past_30_days"), (365, "up_to_past_year")):
            start = date.fromisoformat(out[f"{name}_window"]["from"])
            c = Counter(v for d, v in daily.items() if date.fromisoformat(d) >= start)
            entry[name] = dict(c)
        entry["latest"] = daily[max(daily)]
        out["ksis"][k] = entry
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
