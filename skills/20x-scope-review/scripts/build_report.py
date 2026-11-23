#!/usr/bin/env python3
"""Build the scope review Markdown and Excel tables JSON from the deliverable JSON.

  build_report.py DELIVERABLE.json

Items are grouped by "kind": finding, data_class, resource, flow, third_party, condition.
"""
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from report_lib import (cell, decisions_and_questions, front_matter, inputs_table, kv_table,  # noqa: E402
                        questions_sheet, sme_section, src, write)

COLUMNS = {
    "finding": ("Findings", ["id", "title", "test", "rating", "observation", "criteria", "recommendation"]),
    "data_class": ("Data classes", ["id", "name", "federal_customer_data", "basis", "security_category"]),
    "resource": ("Resources", ["id", "name", "kind_of_resource", "handles", "decision", "rationale"]),
    "flow": ("Flows", ["id", "source", "destination", "data_classes", "protocol", "crosses_boundary"]),
    "third_party": ("Third parties", ["id", "resource", "usage_and_configuration", "justification", "mitigation_measures", "compensating_controls"]),
    "condition": ("Exclusion conditions", ["id", "resource", "text", "evidence", "owner", "cadence", "record_location", "check"]),
}
RATINGS = ["High", "Moderate", "Low", "Observation"]


def build(path: Path):
    d = json.loads(path.read_text(encoding="utf-8"))
    kinds = Counter(i["kind"] for i in d["items"])
    rat = Counter(i["rating"] for i in d["items"] if i["kind"] == "finding")
    L = front_matter(d)
    rows = [("Mode", d["mode"]), ("Record reviewed", d.get("record_reviewed") or "none (build mode)")]
    if d["mode"] == "review":
        rows.append(("Findings", ", ".join(f"{rat.get(r, 0)} {r}" for r in RATINGS)))
    rows += [(COLUMNS[k][0], kinds[k]) for k in COLUMNS if k != "finding" and kinds.get(k)]
    L += kv_table(rows)
    L += ["The scope decisions belong to the consultant and the client. Proposed decisions are marked as proposals until a decision log entry records them.", ""]
    L += inputs_table(d)
    sheets = []
    for kind, (title, cols) in COLUMNS.items():
        group = [i for i in d["items"] if i["kind"] == kind]
        if kind == "finding":
            group.sort(key=lambda i: (RATINGS.index(i["rating"]), i["id"]))
        if not group:
            continue
        L += [f"## {title}", "", "| " + " | ".join(c.replace("_", " ").capitalize() for c in cols) + " | Sources |",
              "|" + "---|" * (len(cols) + 1)]
        for i in group:
            L.append("| " + " | ".join(cell(i.get(c)) for c in cols) + f" | {src(i['sources'])} |")
        L.append("")
        sheets.append({"name": title, "columns": [c.replace("_", " ").capitalize() for c in cols] + ["Sources", "Confirmed"],
                       "rows": [[i.get(c) if i.get(c) is not None else "not stated" for c in cols] + [src(i["sources"]), "yes" if i.get("confirmed", True) else "no"] for i in group]})
    L += decisions_and_questions(d) + sme_section(d)
    sheets.append(questions_sheet(d))
    write(path, L, sheets, d)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import report_lib  # noqa: E402
    report_lib.main(build, __doc__)
