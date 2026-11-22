#!/usr/bin/env python3
"""Check that every change to the scope record has an entry in mas/scope-changes.json.

The log stores a fingerprint of the scope after each change. The newest entry's
fingerprint must equal the fingerprint of the current record. When they differ,
the scope changed without a log entry (rule SCN-CSO-MAR, auditable evaluation
records). Run with --print to show the current fingerprint when you add an entry.

The fingerprint covers what defines the boundary: each resource's id, decision,
zone and kind, each flow's id, endpoints and data classes, the prohibited flows,
the third-party resources and the conditional exclusions.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TYPES = {"added", "removed", "moved", "decision_changed", "condition_changed", "flow_changed", "other"}
SCN = {"routine", "adaptive", "transformative", "not_significant"}


def fingerprint(rec: dict) -> str:
    core = {
        "resources": sorted((r["id"], r["decision"], r["zone"], r["kind"]) for r in rec["information_resources"]),
        "flows": sorted((f["id"], f["source"], f["destination"], tuple(f["data_classes"])) for f in rec["information_flows"]),
        "prohibited": sorted(f["id"] for f in rec["prohibited_flows"]),
        "tpr": sorted(t["id"] for t in rec["third_party_resources"]),
        "conditions": sorted((r["id"], c) for r in rec["information_resources"] for c in (r.get("conditions") or [])
                             if isinstance(c, str)) or sorted(r["id"] for r in rec["information_resources"] if r.get("conditions")),
    }
    return hashlib.sha256(json.dumps(core, sort_keys=True, default=str).encode()).hexdigest()[:16]


def main() -> int:
    rec = json.loads((ROOT / "mas/mas-record.json").read_text())
    now = fingerprint(rec)
    if "--print" in sys.argv:
        print(now)
        return 0
    log = json.loads((ROOT / "mas/scope-changes.json").read_text())
    problems = []
    ids = {r["id"] for r in rec["information_resources"]}
    seen = set()
    for e in log["entries"]:
        if e["id"] in seen:
            problems.append(f"duplicate entry id {e['id']}")
        seen.add(e["id"])
        if e["change_type"] not in TYPES:
            problems.append(f"{e['id']}: unknown change_type {e['change_type']}")
        if e["scn_category"] not in SCN:
            problems.append(f"{e['id']}: unknown scn_category {e['scn_category']}")
        for r in e.get("resources", []):
            if r not in ids and e["change_type"] != "removed":
                problems.append(f"{e['id']}: resource {r} is not in the scope record")
        if e["scn_category"] in ("adaptive", "transformative") and not e.get("notification"):
            problems.append(f"{e['id']}: {e['scn_category']} change needs a notification record")
    dates = [e["date"] for e in log["entries"]]
    if dates != sorted(dates):
        problems.append("entries are not in date order")
    if not log["entries"] or log["entries"][-1]["scope_fingerprint_after"] != now:
        last = log["entries"][-1]["scope_fingerprint_after"] if log["entries"] else "none"
        problems.append(f"scope record changed without a log entry (log fingerprint {last}, record {now}). "
                        f"Add an entry to mas/scope-changes.json with scope_fingerprint_after {now}")
    for p in problems:
        print("PROBLEM:", p, file=sys.stderr)
    print("scope change log matches the scope record" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
