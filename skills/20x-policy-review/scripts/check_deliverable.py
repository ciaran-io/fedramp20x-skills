#!/usr/bin/env python3
"""Check a deliverable JSON against the shared envelope rules.

  check_deliverable.py DELIVERABLE.json [--inputs DIR] [--decisions decisions.json]

Errors (exit 1):
  - a required envelope field is missing, or class is not C
  - an item has no sources, or a source points to an input or decision that does not exist
  - a source cites a FedRAMP ID that is not in the rules data
  - status is "validated" but the SME name, role or date is missing, an item is
    unconfirmed, or an open question that blocks an item has no answer
  - with --inputs, an input file is missing or its sha256 does not match

Warnings: placeholders in square brackets in an item that is marked confirmed.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import frmr  # noqa: E402

REQUIRED = ["skill", "skill_version", "title", "client", "class", "date", "frmr_version",
            "frmr_commit", "inputs", "items", "decisions_needed", "open_questions", "sme_validation"]
PLACEHOLDER = re.compile(r"\[(owner|cadence|deadline|record|tool|system|date|client)[^\]]*\]", re.IGNORECASE)


def check(doc: dict, inputs_dir: Path | None, decisions: set | None, known_ids: set) -> tuple[list, list]:
    err, warn = [], []
    for k in REQUIRED:
        if k not in doc:
            err.append(f"missing field '{k}'")
    if err:
        return err, warn
    if str(doc["class"]).upper() != "C":
        err.append(f"class is {doc['class']}; version 1 covers Class C only")
    input_ids = set()
    for inp in doc["inputs"]:
        input_ids.add(inp.get("id"))
        if inputs_dir is not None:
            p = inputs_dir / inp.get("file", "")
            if not p.exists():
                err.append(f"input {inp.get('id')}: file {p} not found")
            elif inp.get("sha256") and hashlib.sha256(p.read_bytes()).hexdigest() != inp["sha256"]:
                err.append(f"input {inp.get('id')}: {p} changed since the deliverable was written")
    local_decisions = {d.get("id") for d in doc["decisions_needed"]}
    item_ids = set()
    unconfirmed = []
    for it in doc["items"]:
        iid = it.get("id", "?")
        if iid in item_ids:
            err.append(f"item {iid}: duplicate ID")
        item_ids.add(iid)
        srcs = it.get("sources") or []
        if not srcs:
            err.append(f"item {iid}: no sources (every statement must trace to an input, a rule or a decision)")
        for s in srcs:
            if "input" in s:
                if s["input"] not in input_ids:
                    err.append(f"item {iid}: source input {s['input']} is not listed in inputs")
                if not s.get("location"):
                    err.append(f"item {iid}: source input {s['input']} has no location")
            elif "frmr" in s:
                if s["frmr"] not in known_ids:
                    err.append(f"item {iid}: {s['frmr']} is not in the FedRAMP rules data")
            elif "decision" in s:
                ok = s["decision"] in local_decisions or (decisions is not None and s["decision"] in decisions)
                if not ok and decisions is not None:
                    err.append(f"item {iid}: decision {s['decision']} is not in the decision log")
            else:
                err.append(f"item {iid}: source {s} is not an input, frmr or decision source")
        if it.get("confirmed") is False:
            unconfirmed.append(iid)
        elif PLACEHOLDER.search(json.dumps(it)):
            warn.append(f"item {iid}: has a placeholder in square brackets but is marked confirmed")
    blocking = []
    for q in doc["open_questions"]:
        for b in q.get("blocks", []):
            if b not in item_ids:
                err.append(f"open question {q.get('id')}: blocks unknown item {b}")
        if not q.get("answer"):
            blocking.append(q.get("id"))
    sv = doc["sme_validation"]
    status = sv.get("status")
    if status not in ("draft", "validated"):
        err.append(f"sme_validation.status is '{status}'; use draft or validated")
    if status == "validated":
        for k in ("validated_by", "role", "date"):
            if not sv.get(k):
                err.append(f"validated without sme_validation.{k}")
        if unconfirmed:
            err.append(f"validated while items are unconfirmed: {', '.join(unconfirmed)}")
        if blocking:
            err.append(f"validated while open questions have no answer: {', '.join(blocking)}")
    return err, warn


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--inputs", type=Path)
    ap.add_argument("--decisions", type=Path)
    a = ap.parse_args(argv)
    doc = json.loads(Path(a.file).read_text(encoding="utf-8"))
    decisions = None
    if a.decisions:
        decisions = {d["id"] for d in json.loads(a.decisions.read_text(encoding="utf-8"))["decisions"]}
    known = set(frmr.all_ids(frmr.load()))
    err, warn = check(doc, a.inputs, decisions, known)
    for w in warn:
        print(f"WARNING: {w}")
    for e in err:
        print(f"ERROR: {e}")
    status = doc.get("sme_validation", {}).get("status")
    print(f"check: {len(err)} error(s), {len(warn)} warning(s); {len(doc.get('items', []))} items; status {status}")
    sys.exit(1 if err else 0)


if __name__ == "__main__":
    main()
