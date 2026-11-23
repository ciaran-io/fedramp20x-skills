#!/usr/bin/env python3
"""Draft the requirement inventory (step 3) from a client's policy files.

  inventory.py POLICY_FILE... [--role "GRC Lead" --role "Platform Lead"] [--out inventory.json]

Reads Markdown or text policies (a requirement is a line, list item or table row that starts
with an ID such as CED-1, CNA-7b or POL-X/R1) and JSON policy sets (any object with "id" and
"text"). For each requirement it prints the client's exact text and CANDIDATE values for owner,
cadence or deadline, and record location, found by pattern only:

  owner      a role named with --role or in an "Owner:" line of the same file, or a phrase ending in
             Lead, Officer, Manager, Team and similar, that appears in the requirement text
  cadence    phrases such as "every 90 days", "each quarter", "within 10 business days", "annually"
  record     file paths and phrases such as "recorded in ..." or "kept in ..."

Candidates are not answers. Read each requirement and confirm or correct every value in the
deliverable; record "not stated" where the text does not state it. Never fill a value from the
policy header or from another requirement. The script never guesses an ID: text it cannot split
into requirements is listed under "unsplit" for the model to read.
"""
import argparse
import json
import re
import sys
from pathlib import Path

REQ_RE = re.compile(r"^\s*(?:[-*|]\s*)?(?:\*\*)?\(?((?:POL-[A-Z][A-Z0-9]{1,4}/)?[A-Z][A-Z0-9]{1,4}-\d+[a-z]?|POL-[A-Z][A-Z0-9]{1,4}/R\d+)\)?(?:\*\*)?[\s:.|)-]+(.+)$")
CADENCE_RE = re.compile(
    r"\b(every\s+(?:\d+\s+)?(?:business\s+)?(?:days?|weeks?|months?|years?|quarters?|deployments?|releases?|validation runs?)"
    r"|each\s+(?:day|week|month|quarter|year|release|deployment)|at least (?:once )?(?:every|each|once)[^.,;]*"
    r"|within\s+\d+\s+(?:business\s+)?(?:hours?|days?|weeks?|months?)[^.,;]*"
    r"|(?:daily|weekly|monthly|quarterly|annually|yearly)|once (?:a|every) (?:year|quarter|month)"
    r"|before [a-z ]{3,40}(?:is|are) (?:granted|released|deployed|made)|after (?:each|every) [a-z ]{3,40})",
    re.IGNORECASE)
RECORD_RE = re.compile(r"((?:[\w.-]+/)+[\w.-]+\.\w+|(?:recorded|kept|logged|stored|filed) (?:in|as) [^.;]{3,80})", re.IGNORECASE)
ROLE_RE = re.compile(r"\b(?:[A-Z][a-z]+ ){1,3}(?:Lead|Officer|Manager|Director|Administrator|Engineer|Owner|Team|team)\b|\b(?:CISO|CTO|CIO|CEO)\b")
OWNER_LINE_RE = re.compile(r"^\s*(?:\*\*)?owner(?:\*\*)?\s*[:|]\s*(?:\*\*)?([^|*\n]+)", re.IGNORECASE | re.MULTILINE)


def from_text(path: Path, roles: set) -> tuple[list, list]:
    text = path.read_text(encoding="utf-8", errors="replace")
    local_roles = set(roles) | {m.strip() for m in OWNER_LINE_RE.findall(text) if m.strip()}
    reqs, unsplit = [], []
    for ln, line in enumerate(text.splitlines(), 1):
        m = REQ_RE.match(line)
        if m and len(m.group(2).strip()) > 15:
            body = m.group(2)
            if line.lstrip().startswith("|"):
                cells = [c.strip(" *") for c in body.split("|") if c.strip(" *")]
                body = max(cells, key=len) if cells else body  # the requirement text, not the other columns
                extra = [c for c in cells if c != body]
            else:
                extra = []
            r = candidates(str(path), m.group(1), body.strip(" |*"), local_roles, f"line {ln}")
            if extra:
                r["other_columns"] = extra
            reqs.append(r)
        elif re.search(r"\b(must|shall|will|is required to)\b", line, re.IGNORECASE):
            unsplit.append({"file": str(path), "location": f"line {ln}", "text": line.strip()})
    return reqs, unsplit


def from_json(path: Path, roles: set) -> tuple[list, list]:
    data = json.loads(path.read_text(encoding="utf-8"))
    reqs = []

    def walk(o, policy=None, owner=None):
        if isinstance(o, dict):
            pid = o.get("id") if "requirements" in o else policy
            own = o.get("owner", owner) if "requirements" in o else owner
            if "id" in o and isinstance(o.get("text"), str):
                r = candidates(str(path), o["id"], o["text"], set(roles) | ({own} if own else set()), f"{policy or ''} {o['id']}".strip())
                r["policy"] = policy
                r["client_ksis"] = o.get("ksis")
                reqs.append(r)
            for v in o.values():
                walk(v, pid, own)
        elif isinstance(o, list):
            for v in o:
                walk(v, policy, owner)

    walk(data)
    return reqs, []


def candidates(file: str, rid: str, text: str, roles: set, location: str) -> dict:
    low = text.lower()
    owners = sorted({r for r in roles if r and r.lower() in low} | {re.sub(r"^(The|A|An|Each|Every) ", "", m.group(0)) for m in ROLE_RE.finditer(text)})
    return {"file": file, "location": location, "id": rid, "text": text,
            "owner_candidates": owners,
            "cadence_candidates": sorted({m.group(0).strip() for m in CADENCE_RE.finditer(text)}),
            "record_candidates": sorted({m.group(0).strip() for m in RECORD_RE.finditer(text)})}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument("--role", action="append", default=[], help="a role name the client uses; repeat")
    ap.add_argument("--out", type=Path)
    a = ap.parse_args(argv)
    reqs, unsplit = [], []
    for f in a.files:
        if not f.exists():
            sys.exit(f"{f} not found")
        r, u = (from_json if f.suffix.lower() == ".json" else from_text)(f, set(a.role))
        reqs += r
        unsplit += u
    out = {"note": "Candidates found by pattern. Confirm every value against the text; record 'not stated' where the text does not state it.",
           "requirements": reqs, "unsplit": unsplit,
           "summary": {"requirements": len(reqs),
                       "no_owner_candidate": sum(1 for r in reqs if not r["owner_candidates"]),
                       "no_cadence_candidate": sum(1 for r in reqs if not r["cadence_candidates"]),
                       "no_record_candidate": sum(1 for r in reqs if not r["record_candidates"])}}
    text = json.dumps(out, indent=2)
    if a.out:
        a.out.write_text(text + "\n", encoding="utf-8")
        print(json.dumps(out["summary"]))
    else:
        print(text)


if __name__ == "__main__":
    main()
