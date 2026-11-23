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
ID in "cites" (in criteria or sources), contains every element of "mentions" anywhere in
the entry, starts its test with "test", and has a rating in "rating_in". A must_not entry
fails the score when any entry matches.

Each element of "mentions" is a string or a list of alternatives (any one is enough).
Matching ignores case and runs of spaces, so a correct finding is not missed for wording
alone; put the facts that make a finding right (IDs, numbers, the observed message) in
"mentions", not the example's sentence. "in": "document" matches the whole deliverable,
for rules about its top-level fields (for example a status). Exit 1 if any expectation is missed or any
must_not matches.
"""
import json
import re
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


def norm(t: str) -> str:
    return re.sub(r"\s+", " ", t).lower()


def mentioned(text: str, m) -> bool:
    alts = m if isinstance(m, list) else [m]
    return any(norm(a) in text for a in alts)


def matches(entry, m) -> bool:
    raw = json.dumps(entry)
    text = norm(raw)
    if not set(m.get("cites", [])) <= ids_in(entry) and not all(c in raw for c in m.get("cites", [])):
        return False
    if not all(mentioned(text, s) for s in m.get("mentions", [])):
        return False
    if m.get("test") and not str(entry.get("test", "")).startswith(m["test"]):
        return False
    if m.get("rating_in") and entry.get("rating") not in m["rating_in"]:
        return False
    if m.get("coverage") and entry.get("coverage") != m["coverage"]:
        return False
    return True


def section(doc: dict, name: str) -> list:
    if name == "document":
        return [doc]
    sec = doc.get(name, [])
    return sec if isinstance(sec, list) else [sec]


def score(doc: dict, exp: dict) -> tuple[list, list]:
    met, missed = [], []
    for e in exp.get("expect", []):
        sec = section(doc, e["match"].get("in", "items"))
        (met if any(matches(x, e["match"]) for x in sec) else missed).append(e)
    bad = []
    for n in exp.get("must_not", []):
        sec = section(doc, n["match"].get("in", "items"))
        if any(matches(x, n["match"]) for x in sec):
            bad.append(n)
    return missed, bad


def per_change(doc: dict, exp: dict) -> tuple[list, int]:
    """For a case run once per change: check the deliverable for its change against expect_per_change."""
    cid = (doc.get("change") or {}).get("id")
    want = (exp.get("expect_per_change") or {}).get(cid)
    if not want:
        return [], 0
    text = json.dumps(doc)
    missed = []
    types = [t.strip() for t in re.split(r",| or ", want["type"]) if t.strip() in
             ("routine_recurring", "adaptive", "transformative", "not_significant", "class_change")]
    if doc.get("proposed_type") not in types:
        missed.append({"id": f"{cid}-type", "fault": f"proposed type {doc.get('proposed_type')}, expected {want['type']}"})
    for c in want.get("cites", []):
        if c not in text:
            missed.append({"id": f"{cid}-{c}", "fault": f"does not cite {c}"})
    if want.get("must_ask") and (doc.get("decided_type") or not doc.get("decisions_needed")):
        missed.append({"id": f"{cid}-ask", "fault": "the type must be left to the SME as a decision question"})
    if "notices" in want:
        n = len([x for x in (doc.get("timeline") or {}).get("notices", []) if x])
        if n != want["notices"]:
            missed.append({"id": f"{cid}-notices", "fault": f"{n} notices, expected {want['notices']}"})
    return missed, 2 + len(want.get("cites", [])) + bool(want.get("must_ask"))


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    doc = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    exp = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    missed, bad = score(doc, exp)
    total = len(exp.get("expect", []))
    pm, pt = per_change(doc, exp)
    missed += pm
    total += pt
    for e in missed:
        print(f"MISSED {e['id']}: {e['fault']}")
    for n in bad:
        print(f"MUST NOT {n['id']}: {n['reason']}")
    print(f"score: {total - len(missed)}/{total} expected findings, {len(bad)} must-not violation(s)")
    sys.exit(1 if missed or bad else 0)


if __name__ == "__main__":
    main()
