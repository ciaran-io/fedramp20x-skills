#!/usr/bin/env python3
"""Build the assessor review Markdown and Excel tables JSON from the deliverable JSON.

  build_report.py DELIVERABLE.json
"""
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from report_lib import (cell, decisions_and_questions, front_matter, inputs_table, kv_table,  # noqa: E402
                        questions_sheet, sme_section, src, write)

RATINGS = ["High", "Moderate", "Low", "Observation"]


def build(path: Path):
    d = json.loads(path.read_text(encoding="utf-8"))
    rat = Counter(i["rating"] for i in d["items"])
    L = front_matter(d)
    L += kv_table([("Client stage", d["client_stage"]), ("Areas reviewed", d["areas"]),
                   ("Independence", d["independence"]),
                   ("Findings", ", ".join(f"{rat.get(r, 0)} {r}" for r in RATINGS))])
    L += ["The findings report what the evidence shows and where it falls short. They do not state whether the client is compliant.", ""]
    L += inputs_table(d)
    L += ["## Findings", "", "| ID | Title | Area | Rating | Criteria |", "|---|---|---|---|---|"]
    order = sorted(d["items"], key=lambda i: (RATINGS.index(i["rating"]), i["id"]))
    for i in order:
        L.append(f"| {i['id']} | {cell(i['title'])} | {i['area']} | {i['rating']} | {cell(i['criteria'])} |")
    L.append("")
    for i in order:
        L += [f"### {i['id']} {i['title']}", ""]
        L += kv_table([("Area and test", f"{i['area']}, {i['test']}"), ("Lesson", i.get("lesson") or "none"),
                       ("Observation", i["observation"]), ("Criteria", i["criteria"]), ("Rating", i["rating"]),
                       ("Recommendation", i["recommendation"]), ("Occurrences", i.get("occurrences") or "this item only"),
                       ("Sources", src(i["sources"])), ("Confirmed", "yes" if i.get("confirmed", True) else "no, see open questions")])
    if d.get("earlier_findings"):
        L += ["## Earlier findings", "", "| ID | Status | Evidence |", "|---|---|---|"]
        for e in d["earlier_findings"]:
            L.append(f"| {e['id']} | {e['status']} | {cell(e['evidence'])} |")
        L.append("")
    L += ["## Not assessed now", "", "| Rules | Reason | Starts when | Basis |", "|---|---|---|---|"]
    for n in d["not_assessed"]:
        L.append(f"| {cell(n['rules'])} | {cell(n['reason'])} | {cell(n['starts_when'])} | {cell(n.get('basis'))} |")
    L.append("")
    L += decisions_and_questions(d) + sme_section(d)
    sheets = [{"name": "Findings", "columns": ["ID", "Title", "Area", "Test", "Lesson", "Observation", "Criteria", "Rating", "Recommendation", "Occurrences", "Sources", "Confirmed"],
               "rows": [[i["id"], i["title"], i["area"], i["test"], i.get("lesson") or "", i["observation"], i["criteria"], i["rating"], i["recommendation"],
                         i.get("occurrences") or [], src(i["sources"]), "yes" if i.get("confirmed", True) else "no"] for i in order]},
              {"name": "Not assessed", "columns": ["Rules", "Reason", "Starts when", "Basis"],
               "rows": [[n["rules"], n["reason"], n["starts_when"], n.get("basis", "")] for n in d["not_assessed"]]},
              questions_sheet(d)]
    write(path, L, sheets, d)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import report_lib  # noqa: E402
    report_lib.main(build, __doc__)
