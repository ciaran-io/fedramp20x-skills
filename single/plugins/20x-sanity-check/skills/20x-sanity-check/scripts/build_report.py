#!/usr/bin/env python3
"""Build the sanity check Markdown and Excel tables JSON from the deliverable JSON.

  build_report.py DELIVERABLE.json
"""
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from report_lib import (cell, decisions_and_questions, front_matter, inputs_table, kv_table,  # noqa: E402
                        questions_sheet, sme_section, src, write)

ORDER = ["disagrees", "silent", "affected", "agrees"]


def build(path: Path):
    d = json.loads(path.read_text(encoding="utf-8"))
    places = sorted([i for i in d["items"] if i["kind"] == "place"], key=lambda i: (ORDER.index(i["status"]), i["id"]))
    fus = [i for i in d["items"] if i["kind"] == "followup"]
    st = Counter(p["status"] for p in places)
    dec = d["decision"]
    L = front_matter(d)
    L += kv_table([("Decision", f"{dec['id']}: {dec['text']}"), ("Decided by", dec.get("decided_by")), ("Search terms", d["search_terms"]),
                   ("Places", ", ".join(f"{st.get(s, 0)} {s}" for s in ORDER)), ("Follow-ups", len(fus))])
    L += ["This check lists where the decision applies. It changes no document. Each follow-up needs approval by the owner named.", ""]
    L += inputs_table(d)
    L += ["## Places", "", "| ID | Document and location | Status | What it says or needs |", "|---|---|---|---|"]
    for p in places:
        L.append(f"| {p['id']} | {src(p['sources'])} | {p['status']} | {cell(p['finding'])} |")
    L += ["", "## Follow-ups", "", "| ID | Change | Where | Approver | Status | For place |", "|---|---|---|---|---|---|"]
    for f in fus:
        L.append(f"| {f['id']} | {cell(f['change'])} | {cell(f['where'])} | {cell(f['approver'])} | {f['status']} | {cell(f['places'])} |")
    L.append("")
    L += decisions_and_questions(d) + sme_section(d)
    sheets = [{"name": "Places", "columns": ["ID", "Location", "Status", "Finding"], "rows": [[p["id"], src(p["sources"]), p["status"], p["finding"]] for p in places]},
              {"name": "Follow-ups", "columns": ["ID", "Change", "Where", "Approver", "Status", "Places"], "rows": [[f["id"], f["change"], f["where"], f["approver"], f["status"], f["places"]] for f in fus]},
              questions_sheet(d)]
    write(path, L, sheets, d)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    build(Path(sys.argv[1]))
