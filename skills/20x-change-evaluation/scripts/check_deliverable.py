#!/usr/bin/env python3
"""Check a deliverable JSON against the shared envelope rules.

  check_deliverable.py DELIVERABLE.json [--inputs DIR] [--decisions decisions.json]
  check_deliverable.py --sha256 FILE      print the hash to record for an input file

Errors (exit 1):
  - a required envelope field is missing, or class is not A, B or C
  - an item has no sources, or a source points to an input or decision that does not exist
  - a source cites a FedRAMP ID that is not in the rules data
  - status is "validated" but the SME name, role or date is missing, an item is
    unconfirmed, or an open question that blocks an item has no answer
  - with --inputs, an input file is missing or its sha256 does not match. An input's file is
    read from the inputs folder, or from the engagement folder above it (for example
    deliverables/20x-scope-review/...)
  - a field this skill's template (templates/deliverable.json) has is missing, at the top level
    or in an item of the same kind, so build_report.py would fail

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
TEXT_SUFFIXES = {".md", ".txt", ".json", ".csv", ".py", ".yml", ".yaml", ".xml", ".html"}


def file_sha256(path: Path) -> str:
    """SHA-256 of a file. Text files are hashed with CRLF line endings turned into LF, so a
    checkout on Windows gives the same hash as one on Linux or macOS. A folder (for example a
    daily history) is hashed as the sorted list of its files' relative paths and hashes."""
    if path.is_dir():
        lines = [f"{f.relative_to(path).as_posix()} {file_sha256(f)}" for f in sorted(path.rglob("*")) if f.is_file()]
        return hashlib.sha256("\n".join(lines).encode()).hexdigest()
    data = path.read_bytes()
    if path.suffix.lower() in TEXT_SUFFIXES:
        data = data.replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


PLACEHOLDER = re.compile(r"\[[^\]]*(owner|cadence|deadline|record|tool|system|date|client|category|confirm|source)[^\]]*\]", re.IGNORECASE)
# Recommended text may hold a placeholder for the client to fill (method.md); facts may not.
PLACEHOLDER_OK = {"recommendation", "recommended", "rewrite", "change", "remediation"}


TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "deliverable.json"
# Fields a template shows that a deliverable may leave out.
OPTIONAL_TOP = {"plan_review": {"incident", "proposal", "timeline", "target_refs"}}
OPTIONAL_ITEM = {"rewrite", "lesson", "occurrences"}


def template_for(skill: str) -> Path | None:
    """The template of the skill that wrote the deliverable: this skill's own, or a sibling skill
    installed beside it (the full plugin). None when that skill is not installed here."""
    own = TEMPLATE.parent.parent.name
    if skill == own:
        return TEMPLATE
    sib = TEMPLATE.parent.parent.parent / str(skill) / "templates" / "deliverable.json"
    return sib if sib.exists() else None


def template_fields(doc: dict, template: Path | None = None) -> list:
    """Errors for fields the skill's template has and the deliverable lacks."""
    template = template or template_for(doc.get("skill", ""))
    if template is None or not template.exists():
        return []
    t = json.loads(template.read_text(encoding="utf-8"))
    err = []
    optional = OPTIONAL_TOP.get(str(doc.get("mode", "")), set())
    for k in t:
        if k not in doc and k not in optional:
            err.append(f"missing field '{k}' (in templates/deliverable.json)")
    shapes = {}
    for it in t.get("items", []):
        kinds = [x.strip() for x in str(it.get("kind", "*")).split("|")]
        for kd in kinds:
            shapes[kd] = set(it) - OPTIONAL_ITEM - {"kind"}
    for it in doc.get("items", []):
        kd = it.get("kind", "*")
        want = shapes.get(kd) if kd in shapes else shapes.get("*")
        if want is None and len(shapes) == 1:
            want = next(iter(shapes.values()))
        if want is None:
            if shapes and kd != "*":
                err.append(f"item {it.get('id', '?')}: kind '{kd}' is not one of {sorted(shapes)}")
            continue
        missing = sorted(want - set(it))
        if missing:
            err.append(f"item {it.get('id', '?')}: missing {', '.join(missing)} (in templates/deliverable.json)")
    return err


_RECS = {}
CLASSES = ("A", "B", "C")


def rule_records(cls: str = "c") -> dict:
    """Each 20x rule and KSI record at the class, and each definition, by ID."""
    cls = cls.lower()
    if cls not in _RECS:
        d = frmr.load()
        recs = {}
        for rid, _f, _s, r in frmr.iter_rules(d, cls, "20x"):
            recs[rid] = r
        for kid, _t, _th, r in frmr.iter_ksis(d, cls):
            recs[kid] = r
        recs.update(d["FRD"]["data"]["all"])
        _RECS[cls] = recs
    return _RECS[cls]


NUMBER = re.compile(r"(?<![\w.-])\d+(?:\.\d+)?(?![\w-])")


def rewrite_checks(doc: dict, inputs_dir, input_ids: set, local_decisions: set, decisions) -> list:
    """A rewrite needs sources, and every number in its recommended text must appear in its
    current text or in one of its source input files (policy review, S8)."""
    err = []
    for w in doc.get("rewrites", []) or []:
        rid = w.get("id", "?")
        srcs = w.get("sources") or []
        if not srcs:
            err.append(f"rewrite {rid}: no sources (list where each owner, cadence, number and record comes from)")
            continue
        texts = [w.get("current", "") or ""]
        for s in srcs:
            if "input" in s:
                if s["input"] not in input_ids:
                    err.append(f"rewrite {rid}: source input {s['input']} is not listed in inputs")
                elif inputs_dir is not None:
                    inp = next(i for i in doc["inputs"] if i.get("id") == s["input"])
                    f = resolve_input(inputs_dir, inp.get("file", ""))
                    if f.exists():
                        texts.append(f.read_text(encoding="utf-8", errors="replace"))
            elif "frmr" in s:
                recs = rule_records(str(doc.get("class", "c")))
                if s["frmr"] not in recs:
                    err.append(f"rewrite {rid}: {s['frmr']} does not apply at class {doc.get('class')} in the FedRAMP rules data")
                else:
                    texts.append(json.dumps(recs[s["frmr"]]))
            elif "decision" in s:
                ok = s["decision"] in local_decisions or (decisions is not None and s["decision"] in decisions)
                if not ok and decisions is not None:
                    err.append(f"rewrite {rid}: decision {s['decision']} is not in the decision log")
                texts.append(s["decision"])
                for dq in doc.get("decisions_needed", []):
                    if dq.get("id") == s["decision"]:
                        texts.append(json.dumps(dq))
        if inputs_dir is None:
            continue
        rec = re.sub(r"\[[^\]]*\]", "", w.get("recommended", "") or "")
        rec = re.sub(r"\b[A-Z]{2,}-[A-Z0-9-]+\b", "", rec)  # IDs such as KSI-CED-RAT or POL-X/X-1
        joined = "\n".join(texts)
        for n in sorted(set(NUMBER.findall(rec))):
            if not re.search(rf"(?<![\d.]){re.escape(n)}(?![\d])", joined):
                err.append(f"rewrite {rid}: the number {n} is not in its current text or its sources")
    return err


def resolve_input(inputs_dir: Path, rel: str) -> Path:
    p = inputs_dir / rel
    if not p.exists() and (inputs_dir.parent / rel).exists():
        return inputs_dir.parent / rel
    return p


def check(doc: dict, inputs_dir: Path | None, decisions: set | None, known_ids: set) -> tuple[list, list]:
    err, warn = [], []
    for k in REQUIRED:
        if k not in doc:
            err.append(f"missing field '{k}'")
    if err:
        return err, warn
    if template_for(doc.get("skill", "")) is None and TEMPLATE.exists():
        warn.append(f"the {doc.get('skill')} template is not installed beside this skill; its field check was skipped")
    err += template_fields(doc)
    if str(doc["class"]).upper() not in CLASSES:
        err.append(f"class is {doc['class']}; the skills cover Class A, B and C (20x) only")
    input_ids = set()
    for inp in doc["inputs"]:
        input_ids.add(inp.get("id"))
        if inputs_dir is not None:
            p = resolve_input(inputs_dir, inp.get("file", ""))
            if not p.exists():
                err.append(f"input {inp.get('id')}: file {p} not found")
            elif inp.get("sha256") and file_sha256(p) != inp["sha256"]:
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
        elif PLACEHOLDER.search(json.dumps({k: v for k, v in it.items() if k not in PLACEHOLDER_OK})):
            warn.append(f"item {iid}: has a placeholder in square brackets but is marked confirmed")
    err += rewrite_checks(doc, inputs_dir, input_ids, local_decisions, decisions)
    blocking = []
    for q in doc["open_questions"]:
        for b in q.get("blocks", []):
            if b not in item_ids:
                err.append(f"open question {q.get('id')}: blocks unknown item {b}")
        if not q.get("answer"):
            blocking.append(q.get("id"))
    sv = doc["sme_validation"]
    status = sv.get("status")
    if doc.get("skill") == "20x-validator-design" and status != "validated":
        for it in doc["items"]:
            if it.get("status") not in (None, "Draft"):
                err.append(f"item {it.get('id', '?')}: design status {it.get('status')} before SME validation; use Draft")
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
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?", help="deliverable JSON")
    ap.add_argument("--inputs", type=Path, help="the engagement's inputs folder")
    ap.add_argument("--decisions", type=Path, help="the engagement's decisions.json")
    ap.add_argument("--sha256", type=Path, metavar="FILE", help="print the hash to record for an input file")
    a = ap.parse_args(argv)
    if a.sha256:
        print(file_sha256(a.sha256))
        return
    if not a.file:
        ap.error("give a deliverable JSON, or --sha256 FILE")
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
