"""KSI-INR-RIR Reviewing Incident Response Procedures: two automated methods.

FICTIONAL EXAMPLE for Orrinwick Labs, Inc. Built by the 20x-validator-build skill from the
validator design in inputs/designs/INR.md (status Verified in fedramp20x). The official
statement is not copied here; read it with `frmr.py show KSI-INR-RIR`.

Each method takes the client's files and a run date, and returns a result. Ages are always
measured against the run date (lesson L3). Reviews are read as a list and the newest
entry counts (lesson L4). The reviewer is compared with the policy owner (lesson L5).

  python inr_rir.py POLICY.md PLAN.md RECORDS.json [--as-of YYYY-MM-DD]
"""
import argparse
import json
import re
from datetime import date
from pathlib import Path

KSI = "KSI-INR-RIR"
MAX_CADENCE_DAYS = 365


def result(method_id, kind, source, expected, observed, findings):
    return {"ksi": KSI, "method_id": method_id, "kind": kind, "source": source, "expected": expected,
            "observed": observed, "status": "fail" if findings else "pass", "findings": findings}


def policy_owner(policy_text: str):
    m = re.search(r"^\|\s*Owner\s*\|\s*([^|]+?)\s*\|", policy_text, re.MULTILINE)
    return m.group(1).strip() if m else None


def requirements_for(policy_text: str, ksi: str):
    """Requirement IDs in the policy's requirements table whose KSI column lists the KSI."""
    out = []
    for line in policy_text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 3 and re.match(r"^[A-Z]{2,4}-\d+[a-z]?$", cells[0]) and ksi in cells[-1]:
            out.append(cells[0])
    return out


def todo_lines(plan_text: str):
    return [n for n, line in enumerate(plan_text.splitlines(), 1) if "TODO" in line]


def parse_date(v):
    try:
        return date.fromisoformat(v) if v else None
    except (TypeError, ValueError):
        return None


def inr_rir_static(policy_text: str, plan_text, records: dict) -> dict:
    findings = []
    reqs = requirements_for(policy_text, KSI)
    owner = policy_owner(policy_text)
    cadence = records.get("ir_plan", {}).get("review_cadence_days")
    if not reqs:
        findings.append(f"No POL-INR requirement lists {KSI}")
    if not owner:
        findings.append("POL-INR names no owner")
    if not isinstance(cadence, (int, float)) or isinstance(cadence, bool) or cadence <= 0:
        findings.append(f"The plan review cadence is missing or not a positive number: {cadence!r}")
    elif cadence > MAX_CADENCE_DAYS:
        findings.append(f"The plan review cadence is {cadence} days, longer than {MAX_CADENCE_DAYS}")
    if plan_text is None:
        findings.append("The incident response plan is missing")
    else:
        todo = todo_lines(plan_text)
        if todo:
            findings.append(f"The incident response plan is not finished: TODO on line(s) {', '.join(map(str, todo))}")
    return result("inr-rir-static", "static", "POL-INR; incident response plan; records ir_plan",
                  f"a requirement lists {KSI}; owner named; cadence 1 to {MAX_CADENCE_DAYS} days; plan with no TODO",
                  f"requirements {reqs or 'none'}; owner {owner!r}; cadence {cadence!r}", findings)


def inr_rir_live(policy_text: str, records: dict, as_of: date) -> dict:
    findings = []
    owner = policy_owner(policy_text)
    plan = records.get("ir_plan", {})
    cadence = plan.get("review_cadence_days")
    reviews = [r for r in plan.get("reviews", []) if parse_date(r.get("date"))]
    if not reviews:
        findings.append("No plan review is recorded")
        return result("inr-rir-live", "live", "records ir_plan.reviews", "a review inside the cadence by the owner",
                      "no review recorded", findings)
    newest = max(reviews, key=lambda r: r["date"])
    when = parse_date(newest["date"])
    age = (as_of - when).days
    if when > as_of:
        findings.append(f"The newest plan review is dated {when}, after the run date {as_of}")
    elif isinstance(cadence, (int, float)) and age > cadence:
        findings.append(f"The newest plan review is {age} days old, the cadence is {cadence} days")
    if newest.get("reviewed_by") != owner:
        findings.append(f"The plan review dated {when} was recorded by {newest.get('reviewed_by')!r}, POL-INR names {owner!r}")
    triggers = []
    for inc in records.get("incidents", []):
        d = parse_date(inc.get("aar_completed"))
        if d and inc.get("plan_change_required"):
            triggers.append((d, f"after action report for {inc.get('id')}"))
    for rv in records.get("incident_pattern_reviews", []):
        d = parse_date(rv.get("date"))
        if d and rv.get("plan_change_required"):
            triggers.append((d, f"past incident review dated {d}"))
    for d, what in triggers:
        if d <= as_of and not any(d <= parse_date(r["date"]) <= as_of for r in reviews):
            findings.append(f"The {what} required a plan change and no plan review follows it")
    return result("inr-rir-live", "live", "records ir_plan.reviews, incidents, incident_pattern_reviews",
                  f"newest review within {cadence} days of {as_of}, by {owner}, after each required plan change",
                  f"newest review {when}, {age} days old, by {newest.get('reviewed_by')!r}", findings)


def run(policy: Path, plan: Path, records: Path, as_of: date) -> list:
    pt = policy.read_text(encoding="utf-8")
    plt = plan.read_text(encoding="utf-8") if plan.exists() else None
    rec = json.loads(records.read_text(encoding="utf-8"))
    return [inr_rir_static(pt, plt, rec), inr_rir_live(pt, rec, as_of)]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("policy", type=Path)
    ap.add_argument("plan", type=Path)
    ap.add_argument("records", type=Path)
    ap.add_argument("--as-of", type=date.fromisoformat, default=date.today())
    a = ap.parse_args()
    print(json.dumps(run(a.policy, a.plan, a.records, a.as_of), indent=2))
