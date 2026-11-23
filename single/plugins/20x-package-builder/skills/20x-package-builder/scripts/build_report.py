#!/usr/bin/env python3
"""Build the package builder Markdown and Excel tables JSON from the deliverable JSON.

  build_report.py DELIVERABLE.json

Items are grouped by "kind": outline, ksi_summary, ocr_item.
"""
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from report_lib import (cell, decisions_and_questions, front_matter, inputs_table, kv_table,  # noqa: E402
                        questions_sheet, sme_section, src, write)

SUMMARY = [("measures", "Measures and objectives"), ("cycle", "Cycle"), ("verification_measures", "Verification: measures demonstrate the KSI"),
           ("verification_automation", "Verification: automation"), ("validation", "Validation: measures work"),
           ("independent", "Independent verification and validation")]


def build(path: Path):
    d = json.loads(path.read_text(encoding="utf-8"))
    out = [i for i in d["items"] if i["kind"] == "outline"]
    ks = [i for i in d["items"] if i["kind"] == "ksi_summary"]
    oc = [i for i in d["items"] if i["kind"] == "ocr_item"]
    st = Counter(i["status"] for i in out)
    L = front_matter(d)
    L += kv_table([("Parts", ", ".join(f"{st.get(s, 0)} {s}" for s in ("ready", "partial", "missing", "assessor"))),
                   ("KSI summaries drafted", len(ks)), ("Ongoing Certification Report", d.get("ocr_period", "not drafted"))])
    L += ["This is a working draft of the provider's parts of the package. It does not contain or imply an independent assessment, and it does not state that the package is complete.", ""]
    L += inputs_table(d)
    L += ["## Package outline", "", "| ID | Part | Rule | Status | Detail | Sources |", "|---|---|---|---|---|---|"]
    for i in out:
        L.append(f"| {i['id']} | {cell(i['part'])} | {i['rule']} | {i['status']} | {cell(i['detail'])} | {src(i['sources'])} |")
    L.append("")
    if ks:
        L += ["## KSI summaries (SDR-CSX-KSI)", ""]
        for i in ks:
            L += [f"### {i['ksi']}", ""] + kv_table([(lbl, i[key]) for key, lbl in SUMMARY] + [("Sources", src(i["sources"]))])
    m = d.get("metrics")
    if m:
        L += ["## KSI metrics (SDR-CSX-KMT)", "", f"History from {m['first_day']} to {m['as_of']}: {m['days_with_history']} days. "
              f"Past 30 days window {m['past_30_days_window']['from']} to {m['as_of']}: {m['past_30_days_window']['coverage']} "
              f"({m['past_30_days_window']['days_before_history']} days before the history begins, "
              f"{len(m['past_30_days_window']['missing_days'])} missing days after it). Synthetic days excluded: {cell(m['synthetic_days_excluded']) if m['synthetic_days_excluded'] else 'none'}.", "",
              "| KSI | Latest | Past 30 days | Up to past year |", "|---|---|---|---|"]
        for k, v in m["ksis"].items():
            fmt = lambda c: ", ".join(f"{n} {s}" for s, n in sorted(c.items()))
            L.append(f"| {k} | {v['latest']} | {fmt(v['past_30_days'])} | {fmt(v['up_to_past_year'])} |")
        L.append("")
    if oc:
        L += [f"## Ongoing Certification Report (CCM-OCR-AVL): {d.get('ocr_period')}", "", "| ID | Item | Summary | Status | Sources |", "|---|---|---|---|---|"]
        for i in oc:
            L.append(f"| {i['id']} | {cell(i['item'])} | {cell(i['summary'])} | {i['status']} | {src(i['sources'])} |")
        L.append("")
    L += decisions_and_questions(d) + sme_section(d)
    sheets = [{"name": "Outline", "columns": ["ID", "Part", "Rule", "Status", "Detail", "Sources"], "rows": [[i["id"], i["part"], i["rule"], i["status"], i["detail"], src(i["sources"])] for i in out]},
              {"name": "KSI summaries", "columns": ["KSI"] + [lbl for _, lbl in SUMMARY], "rows": [[i["ksi"]] + [i[k] for k, _ in SUMMARY] for i in ks]},
              {"name": "OCR", "columns": ["ID", "Item", "Summary", "Status"], "rows": [[i["id"], i["item"], i["summary"], i["status"]] for i in oc]},
              questions_sheet(d)]
    if m:
        sheets.insert(2, {"name": "Metrics daily", "columns": ["KSI"] + sorted(next(iter(m["ksis"].values()))["daily"]),
                          "rows": [[k] + [v["daily"][x] for x in sorted(v["daily"])] for k, v in m["ksis"].items()]})
    write(path, L, sheets, d)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import report_lib  # noqa: E402
    report_lib.main(build, __doc__)
