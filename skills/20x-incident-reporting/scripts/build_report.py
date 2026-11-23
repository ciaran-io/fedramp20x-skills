#!/usr/bin/env python3
"""Build the incident reporting Markdown and Excel tables JSON from the deliverable JSON.

  build_report.py DELIVERABLE.json

Items are grouped by "kind": evaluation, report_content (evaluate mode) and finding (plan review mode).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from report_lib import (cell, decisions_and_questions, front_matter, inputs_table, kv_table,  # noqa: E402
                        questions_sheet, sme_section, src, write)

RATINGS = ["High", "Moderate", "Low", "Observation"]


def build(path: Path):
    d = json.loads(path.read_text(encoding="utf-8"))
    L = front_matter(d)
    rows = [("Mode", d["mode"])]
    if d["mode"] == "evaluate":
        p = d["proposal"]
        rows += [("Incident", d["incident"]), ("Reportable", p["reportable"]), ("Rating in force", p["rating_in_force"]),
                 ("Proposed PAIN rating", p["proposed_rating"]), ("Reporting clock", d["timeline"]["clock"] or "not started")]
    L += kv_table(rows)
    L += inputs_table(d)
    ev = [i for i in d["items"] if i["kind"] == "evaluation"]
    if ev:
        L += ["## Evaluation", "", "| ID | Question | Answer | Sources |", "|---|---|---|---|"]
        for i in ev:
            L.append(f"| {i['id']} | {cell(i['question'])} | {cell(i['answer'])} | {src(i['sources'])} |")
        L.append("")
    if d.get("timeline"):
        t = d["timeline"]
        L += ["## Reporting timeline", "", f"The clock starts at: {t['clock_starts_at']} ({cell(t['clock'])}). Business days: {t['business_days']}. "
              "Targets marked client plan are the client's own; targets ending _rule come from the PAIN timeframes in the pinned rules data for the rating shown.", "",
              "| Target | Amount | From | Due | Status | Plan reference |", "|---|---|---|---|---|---|"]
        refs = d.get("target_refs", {})
        for x in t["timeline"]:
            L.append(f"| {x['target']}{' (repeats)' if x['repeats'] else ''} | {x['amount']} | {x['from']} | {cell(x['due'])} | {x['status']} | {cell(refs.get(x['target']) or x.get('set_by'))} |")
        L.append("")
        if t.get("plan_later_than_rules"):
            L += [f"Plan targets later than the rules for N{t.get('rating')}:", ""] + [f"- {cell(w)}" for w in t["plan_later_than_rules"]] + [""]
    rc = [i for i in d["items"] if i["kind"] == "report_content"]
    if rc:
        L += ["## Report content", "", "| ID | Report | Item | Supplied by the record | Sources |", "|---|---|---|---|---|"]
        for i in rc:
            L.append(f"| {i['id']} | {i['report']} | {cell(i['item'])} | {cell(i['supplied'])} | {src(i['sources'])} |")
        L.append("")
    fs = sorted([i for i in d["items"] if i["kind"] == "finding"], key=lambda i: (RATINGS.index(i["rating"]), i["id"]))
    if fs:
        L += ["## Plan findings", "", "| ID | Test | Rating | Observation | Criteria | Recommendation | Sources |", "|---|---|---|---|---|---|---|"]
        for i in fs:
            L.append(f"| {i['id']} | {i['test']} | {i['rating']} | {cell(i['observation'])} | {cell(i.get('criteria'))} | {cell(i['recommendation'])} | {src(i['sources'])} |")
        L.append("")
    L += decisions_and_questions(d) + sme_section(d)
    sheets = []
    if d.get("timeline"):
        sheets.append({"name": "Timeline", "columns": ["Target", "Amount", "From", "Due", "Status"],
                       "rows": [[x["target"], x["amount"], x["from"], x["due"] or "", x["status"]] for x in d["timeline"]["timeline"]]})
    if rc:
        sheets.append({"name": "Report content", "columns": ["ID", "Report", "Item", "Supplied"], "rows": [[i["id"], i["report"], i["item"], i["supplied"]] for i in rc]})
    if fs:
        sheets.append({"name": "Plan findings", "columns": ["ID", "Test", "Rating", "Observation", "Recommendation"], "rows": [[i["id"], i["test"], i["rating"], i["observation"], i["recommendation"]] for i in fs]})
    sheets.append(questions_sheet(d))
    write(path, L, sheets, d)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import report_lib  # noqa: E402
    report_lib.main(build, __doc__)
