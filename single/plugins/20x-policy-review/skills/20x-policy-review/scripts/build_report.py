#!/usr/bin/env python3
"""Build the policy review Markdown report and the Excel tables JSON from the deliverable JSON.

  build_report.py DELIVERABLE.json

Writes <name>.md and <name>-tables.json next to the JSON. The JSON is the source of truth;
edit it and rebuild, never edit the Markdown by hand.
"""
import json
import sys
from collections import Counter
from pathlib import Path

RATINGS = ["High", "Moderate", "Low", "Observation"]
COVERAGE = ["covered", "partial", "not covered", "not reviewed"]


def cell(v):
    if v is None or v == "":
        return "not stated"
    if isinstance(v, list):
        return ", ".join(v) if v else "none"
    return str(v).replace("|", "\\|").replace("\n", " ")


def src(sources):
    out = []
    for s in sources:
        if "input" in s:
            out.append(f"{s['input']} {s.get('location', '')}".strip())
        elif "frmr" in s:
            out.append(s["frmr"])
        elif "decision" in s:
            out.append(s["decision"])
    return "; ".join(out)


def status_line(sv):
    if sv.get("status") == "validated":
        return f"Validated by {sv['validated_by']} ({sv['role']}) on {sv['date']}"
    return "Draft: pending SME validation"


def build(path: Path):
    d = json.loads(path.read_text(encoding="utf-8"))
    sv = d["sme_validation"]
    inputs = {i["id"]: i for i in d["inputs"]}
    cov = Counter(c["coverage"] for c in d["coverage"])
    rat = Counter(i["rating"] for i in d["items"])
    L = []
    L += ["---", f"title: {d['title']}", f"client: {d['client']}", "class: C (CR26)",
          f"frmr_version: {d['frmr_version']} (commit {d['frmr_commit'][:7]})", f"date: {d['date']}",
          f"prepared_by: {d.get('prepared_by', 'Claude')}", f"sme_validation: {status_line(sv)}", "---", ""]
    L += [f"# {d['title']}", "", "## Basis", "", "| | |", "|---|---|"]
    L.append("| Policies reviewed | " + "; ".join(f"{i['description']} ({k})" for k, i in inputs.items()) + " |")
    L.append("| Documents referenced but not provided | " + (cell(d.get("not_provided")) if d.get("not_provided") else "None") + " |")
    L.append(f"| KSIs at Class C | {len(d['coverage'])} |")
    L.append("| Coverage | " + ", ".join(f"{cov.get(c, 0)} {c}" for c in COVERAGE) + " |")
    L.append("| Gaps | " + ", ".join(f"{rat.get(r, 0)} {r}" for r in RATINGS) + " |")
    L.append(f"| SME validation | {status_line(sv)} |")
    L += ["", "This review reports what the policies state. It does not assess evidence, and it does not state whether the client is compliant.", ""]
    L += ["## Coverage matrix", "", "| KSI | Name | Requirements | Coverage | Gaps | Note |", "|---|---|---|---|---|---|"]
    for c in d["coverage"]:
        L.append(f"| {c['ksi']} | {cell(c['name'])} | {cell(c['requirements'])} | {c['coverage']} | {cell(c.get('gaps', []))} | {cell(c.get('note', ''))} |")
    L += ["", "## Gaps", ""]
    for r in RATINGS:
        for g in [i for i in d["items"] if i["rating"] == r]:
            L += [f"### {g['id']} {g['title']}", "", "| | |", "|---|---|",
                  f"| Requirement | {cell(g['requirement'])} |", f"| Test | {g['test']} |",
                  f"| Criteria | {cell(g['criteria'])} |", f"| Rating | {g['rating']} |",
                  f"| Observation | {cell(g['observation'])} |", f"| Recommendation | {cell(g['recommendation'])} |",
                  f"| Rewrite | {cell(g.get('rewrite') or 'none')} |", f"| Sources | {src(g['sources'])} |",
                  f"| Confirmed | {'yes' if g.get('confirmed', True) else 'no, see open questions'} |", ""]
    L += ["## Rewritten requirements", "", "| ID | Requirement | Current text | Recommended text | Closes |", "|---|---|---|---|---|"]
    for w in d["rewrites"]:
        L.append(f"| {w['id']} | {w['requirement']} | {cell(w['current'])} | {cell(w['recommended'])} | {cell(w['closes'])} |")
    L += ["", "## Decisions for the consultant", "", "| ID | Question | Options | Recommendation | Decision |", "|---|---|---|---|---|"]
    for q in d["decisions_needed"]:
        L.append(f"| {q['id']} | {cell(q['question'])} | {cell(q['options'])} | {cell(q['recommendation'])}: {cell(q['reason'])} | {cell(q.get('decision_ref') or 'open')} |")
    L += ["", "## Open questions", "", "| ID | Question | Why it matters | Blocks | Answer |", "|---|---|---|---|---|"]
    for q in d["open_questions"]:
        L.append(f"| {q['id']} | {cell(q['question'])} | {cell(q['why'])} | {cell(q['blocks'])} | {cell(q.get('answer') or 'open')} |")
    L += ["", "## Requirement inventory", "", "| Requirement | Owner | Cadence or deadline | Record location | KSIs (client mapping) |", "|---|---|---|---|---|"]
    for q in d["requirements"]:
        L.append(f"| {q['policy']} / {q['id']} | {cell(q['owner'])} | {cell(q['cadence'])} | {cell(q['record_location'])} | {cell(q['client_ksis'])} |")
    L += ["", "## SME validation", "", status_line(sv) + "."]
    for c in sv.get("corrections", []):
        L.append(f"- {c['item']}: {c['change']}")
    L.append("")
    md = path.with_suffix(".md")
    md.write_text("\n".join(L), encoding="utf-8")

    tables = {
        "title": d["title"], "client": d["client"], "class": "C (CR26)", "frmr_version": d["frmr_version"],
        "date": d["date"], "sme_validation": status_line(sv),
        "sheets": [
            {"name": "Coverage", "columns": ["KSI", "Name", "Requirements", "Coverage", "Gaps", "Note"],
             "rows": [[c["ksi"], c["name"], c["requirements"], c["coverage"], c.get("gaps", []), c.get("note", "")] for c in d["coverage"]]},
            {"name": "Gaps", "columns": ["ID", "Title", "Requirement", "Test", "Criteria", "Rating", "Observation", "Recommendation", "Rewrite", "Sources", "Confirmed"],
             "rows": [[g["id"], g["title"], g["requirement"], g["test"], g["criteria"], g["rating"], g["observation"], g["recommendation"], g.get("rewrite") or "", src(g["sources"]), "yes" if g.get("confirmed", True) else "no"] for g in d["items"]]},
            {"name": "Rewrites", "columns": ["ID", "Requirement", "Current text", "Recommended text", "Closes"],
             "rows": [[w["id"], w["requirement"], w["current"], w["recommended"], w["closes"]] for w in d["rewrites"]]},
            {"name": "Requirements", "columns": ["Policy", "Requirement", "Text", "Owner", "Cadence or deadline", "Record location", "KSIs (client mapping)"],
             "rows": [[q["policy"], q["id"], q["text"], q["owner"] or "not stated", q["cadence"] or "not stated", q["record_location"] or "not stated", q["client_ksis"]] for q in d["requirements"]]},
            {"name": "Questions", "columns": ["ID", "Type", "Question", "Detail", "Recommendation or blocks", "Answer"],
             "rows": [[q["id"], "Decision", q["question"], "; ".join(q["options"]), q["recommendation"], q.get("decision_ref") or "open"] for q in d["decisions_needed"]]
                     + [[q["id"], "Open question", q["question"], q["why"], q["blocks"], q.get("answer") or "open"] for q in d["open_questions"]]},
        ],
    }
    tpath = path.with_name(path.stem + "-tables.json")
    tpath.write_text(json.dumps(tables, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {md} and {tpath}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    build(Path(sys.argv[1]))
