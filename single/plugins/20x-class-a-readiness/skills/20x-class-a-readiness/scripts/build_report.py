#!/usr/bin/env python3
"""Build the Class A readiness Markdown and Excel tables JSON from the deliverable JSON.

  build_report.py DELIVERABLE.json
"""
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from report_lib import (cell, decisions_and_questions, front_matter, inputs_table, kv_table,  # noqa: E402
                        questions_sheet, sme_section, src, write)

RATINGS = ["High", "Moderate", "Low", "Observation", "none"]


def build(path: Path):
    d = json.loads(path.read_text(encoding="utf-8"))
    items = d["items"]
    fw = [i for i in items if i["kind"] == "framework"]
    mat = [i for i in items if i["kind"] == "material"]
    mp = [i for i in items if i["kind"] == "mapping"]
    rec = [i for i in items if i["kind"] == "recommendation"]
    rated = Counter(i["rating"] for i in fw + mat + mp)
    st = Counter(i["status"] for i in mp)
    L = front_matter(d)
    L += kv_table([("Planned submission", d.get("planned_submission")),
                   ("Framework", "; ".join(dict.fromkeys(f"{f['framework']}, completed {f['completed']}" for f in fw)) or "none found"),
                   ("Findings", ", ".join(f"{rated.get(r, 0)} {r}" for r in RATINGS[:4])),
                   ("Mandatory rules and KSIs", ", ".join(f"{st.get(s, 0)} {s.replace('_', ' ')}" for s in ("mapped", "partial", "unmapped", "not_reviewed"))),
                   ("Recommendations", len(rec))])
    L += ["This report states what the evidence shows against the Class A rules. It does not state that the client is ready or certified.", ""]
    L += inputs_table(d)
    L += ["## Alternative framework (FRC-CLA-ASF)", "", "| ID | Framework | Completed | Assessor | Period | Window closes | Within window | Finding | Rating | Recommendation | Sources |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for f in fw:
        L.append(f"| {f['id']} | {cell(f['framework'])} | {cell(f['completed'])} | {cell(f['assessor'])} | {cell(f['period'])} | {cell(f['window_closes'])} | "
                 f"{f['within_window']} | {cell(f['finding'])} | {f['rating']} | {cell(f['recommendation'] or 'none')} | {src(f['sources'])} |")
    L += ["", "## Assessment materials (FRC-CLA-EAM)", "", "| ID | Material | Status | Finding | Rating | Recommendation | Sources |", "|---|---|---|---|---|---|---|"]
    for m in mat:
        L.append(f"| {m['id']} | {cell(m['material'])} | {m['status']} | {cell(m['finding'])} | {m['rating']} | {cell(m['recommendation'] or 'none')} | {src(m['sources'])} |")
    L += ["", "## Mandatory rules and KSIs (FRC-CLA-MFR)", "", "| ID | Rule or KSI | Status | Mapped to | Package location | Finding | Rating | Recommendation |",
          "|---|---|---|---|---|---|---|---|"]
    for p in sorted(mp, key=lambda i: (RATINGS.index(i["rating"]), i["id"])):
        L.append(f"| {p['id']} | {p['rule']} | {p['status'].replace('_', ' ')} | {cell(p['mapped_to'])} | {cell(p['package_location'])} | "
                 f"{cell(p['finding'])} | {p['rating']} | {cell(p['recommendation'])} |")
    L += ["", "## Recommended and optional rules (FRC-CLA-RFR, FRC-CLA-OFR)", "", "These are not gaps.", "",
          "| ID | Rule | Force | Today | Recommendation |", "|---|---|---|---|---|"]
    for c in rec:
        L.append(f"| {c['id']} | {c['rule']} | {c['force']} | {cell(c['today'])} | {cell(c['recommendation'])} |")
    L.append("")
    L += decisions_and_questions(d) + sme_section(d)
    sheets = [{"name": "Framework and materials", "columns": ["ID", "Kind", "Subject", "Status", "Finding", "Rating", "Recommendation", "Sources"],
               "rows": [[i["id"], i["kind"], i.get("framework") or i.get("material"), i.get("within_window") or i.get("status"), i["finding"], i["rating"],
                         i["recommendation"], src(i["sources"])] for i in fw + mat]},
              {"name": "Mandatory mapping", "columns": ["ID", "Rule or KSI", "Status", "Mapped to", "Package location", "Finding", "Rating", "Recommendation"],
               "rows": [[p["id"], p["rule"], p["status"], p["mapped_to"], p["package_location"], p["finding"], p["rating"], p["recommendation"]] for p in mp]},
              {"name": "Recommendations", "columns": ["ID", "Rule", "Force", "Today", "Recommendation"],
               "rows": [[c["id"], c["rule"], c["force"], c["today"], c["recommendation"]] for c in rec]},
              questions_sheet(d)]
    write(path, L, sheets, d)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import report_lib  # noqa: E402
    report_lib.main(build, __doc__)
