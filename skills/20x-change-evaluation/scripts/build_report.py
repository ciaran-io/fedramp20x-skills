#!/usr/bin/env python3
"""Build the change evaluation Markdown and Excel tables JSON from the deliverable JSON.

  build_report.py DELIVERABLE.json
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from report_lib import (cell, decisions_and_questions, front_matter, inputs_table, kv_table,  # noqa: E402
                        questions_sheet, sme_section, src, write)


def build(path: Path):
    d = json.loads(path.read_text(encoding="utf-8"))
    c = d["change"]
    L = front_matter(d)
    L += kv_table([("Change", f"{c['id']}: {c['title']}"), ("Proposed type", d["proposed_type"]),
                   ("Decided type", d.get("decided_type") or "open: the consultant decides"),
                   ("Planned start", c.get("start")), ("Planned finish", c.get("finish")), ("Emergency", c.get("emergency"))])
    L += inputs_table(d)
    L += ["## The change", "", cell(c["description"]), ""]
    L += ["## Evaluation", "", "| ID | Question | Answer | Evidence |", "|---|---|---|---|"]
    ev = [i for i in d["items"] if i["kind"] == "evaluation"]
    for i in ev:
        L.append(f"| {i['id']} | {cell(i['question'])} | {cell(i['answer'])} | {src(i['sources'])} |")
    L += ["", "## Notices", "", f"Business days: {d['timeline']['business_days']}.", "",
          "| Rule | Name | Counts from | Timeframe | Date | Meaning |", "|---|---|---|---|---|---|"]
    for n in d["timeline"]["notices"]:
        L.append(f"| {n['rule']} | {n['name']} | {n['counts_from']} | {n['timeframe']} {n['direction']} | {cell(n.get('due'))} | {cell(n['due_meaning'])} |")
    L += ["", cell(d["timeline"].get("note")), ""]
    content = [i for i in d["items"] if i["kind"] == "notice_content"]
    if content:
        L += ["## Notice content (SCN-CSO-INF)", "", "| ID | Item | Supplied by the inputs | Sources |", "|---|---|---|---|"]
        for i in content:
            L.append(f"| {i['id']} | {cell(i['item'])} | {cell(i['supplied'])} | {src(i['sources'])} |")
        L.append("")
    other = [i for i in d["items"] if i["kind"] in ("scope_log", "client_review")]
    if other:
        L += ["## Scope log entry and client review", ""]
        for i in other:
            L += [f"### {i['id']} {i['title']}", ""] + kv_table([(k.replace("_", " ").capitalize(), v) for k, v in i["detail"].items()] + [("Sources", src(i["sources"]))])
    L += decisions_and_questions(d) + sme_section(d)
    sheets = [{"name": "Evaluation", "columns": ["ID", "Question", "Answer", "Sources"], "rows": [[i["id"], i["question"], i["answer"], src(i["sources"])] for i in ev]},
              {"name": "Notices", "columns": ["Rule", "Name", "Counts from", "Timeframe", "Direction", "Date", "Meaning"],
               "rows": [[n["rule"], n["name"], n["counts_from"], n["timeframe"], n["direction"], n.get("due") or "", n["due_meaning"]] for n in d["timeline"]["notices"]]},
              {"name": "Notice content", "columns": ["ID", "Item", "Supplied", "Sources"], "rows": [[i["id"], i["item"], i["supplied"], src(i["sources"])] for i in content]},
              questions_sheet(d)]
    write(path, L, sheets, d)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import report_lib  # noqa: E402
    report_lib.main(build, __doc__)
