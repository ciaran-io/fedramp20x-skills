"""{KSI-ID} {name}: automated methods. Built by 20x-validator-build from design {design ref}.

The official statement is not copied here; read it with `frmr.py show {KSI-ID}`.
Every method takes the parsed inputs and the run date, and returns the result format in
references/check-patterns.md.

  python {module}.py {INPUT ...} [--as-of YYYY-MM-DD]
"""
import argparse
import json
from datetime import date
from pathlib import Path

KSI = "{KSI-ID}"


def result(method_id, kind, source, expected, observed, findings, notes=None):
    return {"ksi": KSI, "method_id": method_id, "kind": kind, "source": source, "expected": expected,
            "observed": observed, "status": "fail" if findings else "pass", "findings": findings, "notes": notes or []}


def static_method(declared: dict) -> dict:
    findings = []
    # One check per pass condition in the design. One message per failure.
    return result("{xxx-yyy-static}", "static", "{source}", "{pass condition}", "{what was seen}", findings)


def live_method(observed: dict, as_of: date) -> dict:
    findings = []
    # Measure every age against as_of. Read records as lists; the newest entry counts.
    return result("{xxx-yyy-live}", "live", "{source}", "{pass condition}", "{what was seen}", findings)


def run(paths: dict, as_of: date) -> list:
    data = {k: json.loads(Path(p).read_text(encoding="utf-8")) for k, p in paths.items()}
    return [static_method(data), live_method(data, as_of)]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+", help="NAME=PATH")
    ap.add_argument("--as-of", type=date.fromisoformat, default=date.today())
    a = ap.parse_args()
    print(json.dumps(run(dict(x.split("=", 1) for x in a.inputs), a.as_of), indent=2))
