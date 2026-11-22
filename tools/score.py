#!/usr/bin/env python3
"""Score a skill's deliverable JSON against a test case's expected findings.

  python tools/score.py DELIVERABLE.json tests/<skill>/<case>/expected.json

expected.json:
{
  "case": "seeded",
  "expect": [
    {"id": "E-01", "fault": "what was seeded",
     "match": {"cites": ["KSI-..."], "mentions": ["POL-TST/TST-2"], "test": "T2", "rating_in": ["Moderate"],
               "in": "items | open_questions | decisions_needed | not_assessed | coverage"}}
  ],
  "must_not": [
    {"id": "N-01", "reason": "...", "match": {"mentions": ["..."], "in": "items"}}
  ]
}

An expectation is met when one entry in the named section (default items) cites every
ID in "cites" (in criteria or sources), contains every string in "mentions" anywhere in
the entry, starts its test with "test", and has a rating in "rating_in". A must_not entry
fails the score when any entry matches. Exit 1 if any expectation is missed or any
must_not matches.
"""
import json
import sys
from pathlib import Path


def ids_in(entry) -> set:
    out = set()
    for c in entry.get("criteria", []) or []:
        out.add(c)
    for s in entry.get("sources", []) or []:
        if "frmr" in s:
            out.add(s["frmr"])
    for k in ("ksi", "rule", "rules"):
        v = entry.get(k)
        if isinstance(v, str):
            out.add(v)
        elif isinstance(v, list):
            out.update(v)
    return out


def matches(entry, m) -> bool:
    text = json.dumps(entry)
    if not set(m.get("cites", [])) <= ids_in(entry) and not all(c in text for c in m.get("cites", [])):
        return False
    if not all(s in text for s in m.get("mentions", [])):
        return False
    if m.get("test") and not str(entry.get("test", "")).startswith(m["test"]):
        return False
    if m.get("rating_in") and entry.get("rating") not in m["rating_in"]:
        return False
    if m.get("coverage") and entry.get("coverage") != m["coverage"]:
        return False
    return True


def score(doc: dict, exp: dict) -> tuple[list, list]:
    met, missed = [], []
    for e in exp.get("expect", []):
        sec = doc.get(e["match"].get("in", "items"), [])
        (met if any(matches(x, e["match"]) for x in sec) else missed).append(e)
    bad = []
    for n in exp.get("must_not", []):
        sec = doc.get(n["match"].get("in", "items"), [])
        if any(matches(x, n["match"]) for x in sec):
            bad.append(n)
    return missed, bad


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    doc = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    exp = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    missed, bad = score(doc, exp)
    total = len(exp.get("expect", []))
    for e in missed:
        print(f"MISSED {e['id']}: {e['fault']}")
    for n in bad:
        print(f"MUST NOT {n['id']}: {n['reason']}")
    print(f"score: {total - len(missed)}/{total} expected findings, {len(bad)} must-not violation(s)")
    sys.exit(1 if missed or bad else 0)


if __name__ == "__main__":
    main()
