#!/usr/bin/env python3
"""Build the validator design Markdown and Excel tables JSON from the deliverable JSON.

  build_report.py DELIVERABLE.json
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from report_lib import (cell, decisions_and_questions, front_matter, inputs_table, kv_table,  # noqa: E402
                        questions_sheet, sme_section, src, write)

FIELDS = [("Requirement", "requirement"), ("Policy requirement", "policy_requirement"), ("Resource type", "resource_type"),
          ("Validation cadence", "cadence")]


def method_text(m):
    return f"`{m['id']}`. Reads {m['reads']}. Passes when {m['passes_when']}"


def build(path: Path):
    d = json.loads(path.read_text(encoding="utf-8"))
    L = front_matter(d)
    L += kv_table([("KSIs designed", ", ".join(i["ksi"] for i in d["items"])),
                   ("Status", "; ".join(f"{i['ksi']}: {i['status']}" for i in d["items"]))])
    L += ["Each design states how its methods fail and the break test that will prove it. Status Designed means no method has been built or tested yet.", ""]
    L += inputs_table(d)
    for i in d["items"]:
        L += [f"## {i['ksi']} {i['name']}", "", "| Field | Design |", "|---|---|"]
        for label, key in FIELDS:
            L.append(f"| {label} | {cell(i[key])} |")
        for m in i["methods"]:
            L.append(f"| {m['kind'].capitalize()} method | {cell(method_text(m))} |")
        L.append(f"| Fails when | {cell(' '.join(i['fails_when']))} |")
        L.append("| Break test | " + cell(" ".join(f"{b['method']} ({b['status']}): {b['change']} Expected: {b['expected']}" for b in i["break_tests"])) + " |")
        L.append(f"| Production source | {cell(i['production_source'])} |")
        L.append(f"| Gap | {cell(i['gap'])} |")
        L.append(f"| Status | {i['status']} |")
        L.append(f"| Sources | {src(i['sources'])} |")
        L.append(f"| Confirmed | {'yes' if i.get('confirmed', True) else 'no, see open questions and decisions'} |")
        L += ["", "**Decisions.**", ""]
        for x in i.get("decisions", []):
            L.append(f"- {x}")
        L.append("")
    L += decisions_and_questions(d) + sme_section(d)
    rows = []
    for i in d["items"]:
        for m in i["methods"]:
            bt = next((b for b in i["break_tests"] if b["method"] == m["id"]), None)
            rows.append([i["ksi"], m["id"], m["kind"], m["reads"], m["passes_when"],
                         bt["change"] if bt else "", bt["expected"] if bt else "", bt["status"] if bt else "missing", i["status"]])
    sheets = [{"name": "Methods", "columns": ["KSI", "Method", "Kind", "Reads", "Passes when", "Break test", "Expected message", "Break test status", "Design status"], "rows": rows},
              {"name": "Designs", "columns": ["KSI", "Name", "Policy requirement", "Resource type", "Cadence", "Fails when", "Production source", "Gap", "Status"],
               "rows": [[i["ksi"], i["name"], i["policy_requirement"], i["resource_type"], i["cadence"], " ".join(i["fails_when"]), i["production_source"], i["gap"], i["status"]] for i in d["items"]]},
              questions_sheet(d)]
    write(path, L, sheets, d)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    build(Path(sys.argv[1]))
