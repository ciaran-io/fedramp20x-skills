"""Shared helpers for the skills' build_report.py scripts.

Each skill keeps its deliverable in JSON and builds the Markdown report and the Excel
tables JSON from it with these helpers, so every report has the same front matter,
decision and question sections and SME validation line.
"""
import json
import sys
from pathlib import Path


def cell(v) -> str:
    if v is None or v == "":
        return "not stated"
    if isinstance(v, list):
        return ", ".join(str(x) for x in v) if v else "none"
    return str(v).replace("|", "\\|").replace("\n", " ")


def src(sources) -> str:
    out = []
    for s in sources or []:
        if "input" in s:
            out.append(f"{s['input']} {s.get('location', '')}".strip())
        elif "frmr" in s:
            out.append(s["frmr"])
        elif "decision" in s:
            out.append(s["decision"])
    return "; ".join(out)


def status_line(sv: dict) -> str:
    if sv.get("status") == "validated":
        return f"Validated by {sv['validated_by']} ({sv['role']}) on {sv['date']}"
    return "Draft: pending SME validation"


def front_matter(d: dict) -> list:
    return ["---", f"title: {d['title']}", f"client: {d['client']}", "class: C (CR26)",
            f"frmr_version: {d['frmr_version']} (commit {d['frmr_commit'][:7]})", f"date: {d['date']}",
            f"prepared_by: {d.get('prepared_by', 'Claude')}", f"sme_validation: {status_line(d['sme_validation'])}",
            "---", "", f"# {d['title']}", ""]


def inputs_table(d: dict) -> list:
    L = ["## Inputs", "", "| ID | File | Description |", "|---|---|---|"]
    for i in d["inputs"]:
        L.append(f"| {i['id']} | `{i['file']}` | {cell(i['description'])} |")
    return L + [""]


def kv_table(rows) -> list:
    L = ["| | |", "|---|---|"]
    for k, v in rows:
        L.append(f"| {k} | {cell(v)} |")
    return L + [""]


def decisions_and_questions(d: dict) -> list:
    L = ["## Decisions for the consultant", ""]
    if d["decisions_needed"]:
        L += ["| ID | Question | Options | Recommendation | Decision |", "|---|---|---|---|---|"]
        for q in d["decisions_needed"]:
            L.append(f"| {q['id']} | {cell(q['question'])} | {cell(q['options'])} | {cell(q['recommendation'])}: {cell(q['reason'])} | {cell(q.get('decision_ref') or (('open; this run used: ' + q['unattended_choice']) if q.get('unattended_choice') else 'open'))} |")
    else:
        L.append("None.")
    L += ["", "## Open questions", ""]
    if d["open_questions"]:
        L += ["| ID | Question | Why it matters | Blocks | Answer |", "|---|---|---|---|---|"]
        for q in d["open_questions"]:
            L.append(f"| {q['id']} | {cell(q['question'])} | {cell(q['why'])} | {cell(q['blocks'])} | {cell(q.get('answer') or 'open')} |")
    else:
        L.append("None.")
    return L + [""]


def sme_section(d: dict) -> list:
    sv = d["sme_validation"]
    L = ["## SME validation", "", status_line(sv) + "."]
    for c in sv.get("corrections", []):
        L.append(f"- {c['item']}: {c['change']}")
    for r in sv.get("rejected", []):
        L.append(f"- Rejected {r.get('item')}: {r.get('reason', '')}")
    return L + [""]


def questions_sheet(d: dict) -> dict:
    return {"name": "Questions", "columns": ["ID", "Type", "Question", "Detail", "Recommendation or blocks", "Answer"],
            "rows": [[q["id"], "Decision", q["question"], "; ".join(q["options"]), q["recommendation"], q.get("decision_ref") or (("open; this run used: " + q["unattended_choice"]) if q.get("unattended_choice") else "open")] for q in d["decisions_needed"]]
            + [[q["id"], "Open question", q["question"], q["why"], q["blocks"], q.get("answer") or "open"] for q in d["open_questions"]]}


def write(path: Path, lines: list, sheets: list, d: dict):
    md = path.with_suffix(".md")
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    tables = {"title": d["title"], "client": d["client"], "class": "C (CR26)", "frmr_version": d["frmr_version"],
              "date": d["date"], "sme_validation": status_line(d["sme_validation"]), "sheets": sheets}
    t = path.with_name(path.stem + "-tables.json")
    t.write_text(json.dumps(tables, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {md} and {t}")


def main(build, doc: str):
    """Command line for build_report.py: help, one argument, and a clear message for a missing field."""
    args = sys.argv[1:]
    if len(args) != 1 or args[0] in ("-h", "--help"):
        print(doc)
        sys.exit(0 if args[:1] in (["-h"], ["--help"]) else 2)
    path = Path(args[0])
    if not path.exists():
        sys.exit(f"ERROR: {path} not found")
    try:
        build(path)
    except KeyError as e:
        sys.exit(f"ERROR: {path}: field {e} is missing. Run check_deliverable.py on it for the full list.")
