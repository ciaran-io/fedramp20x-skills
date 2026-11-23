#!/usr/bin/env python3
"""Build the validator build Markdown and Excel tables JSON from the deliverable JSON.

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
    c, u = d["code"], d["unit_tests"]
    L = front_matter(d)
    L += kv_table([("KSI", d["ksi"]), ("Design", d["design"]), ("Methods", len(d["items"])),
                   ("Unit tests", f"{u['passed']} of {u['count']} passed on {u['run_on']}"),
                   ("Break tests", sum(len(i["break_tests"]) for i in d["items"])),
                   ("Proposed status", d["proposed_status"] + " (changes only after SME Validate)")])
    L += ["## Code", ""] + kv_table([("Module", f"`{c['module']}`"), ("Tests", f"`{c['tests']}`"), ("Break test record", f"`{c['break_tests']}`"),
                                     ("Run", f"`{c['run']}`"), ("Test", f"`{c['test_command']}`")])
    L += inputs_table(d)
    for i in d["items"]:
        L += [f"## {i['method']} ({i['kind']})", ""]
        L += kv_table([("Reads", i["reads"]), ("Conditions checked", "; ".join(i["conditions_checked"])), ("Gap", i["gap"]), ("Sources", src(i["sources"]))])
        L += ["| Break test change | Observed message | Result |", "|---|---|---|"]
        for b in i["break_tests"]:
            L.append(f"| {cell(b['change'])} | {cell(b['observed_message'])} | {b['result']} |")
        L.append("")
    L += decisions_and_questions(d) + sme_section(d)
    sheets = [{"name": "Break tests", "columns": ["Method", "Change", "Observed message", "Result"],
               "rows": [[i["method"], b["change"], b["observed_message"], b["result"]] for i in d["items"] for b in i["break_tests"]]},
              {"name": "Methods", "columns": ["Method", "Kind", "Reads", "Conditions", "Gap"],
               "rows": [[i["method"], i["kind"], i["reads"], i["conditions_checked"], i["gap"]] for i in d["items"]]},
              questions_sheet(d)]
    write(path, L, sheets, d)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import report_lib  # noqa: E402
    report_lib.main(build, __doc__)
