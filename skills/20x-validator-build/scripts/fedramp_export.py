#!/usr/bin/env python3
"""Export an SME-validated deliverable as JSON that is valid against the FedRAMP schema its rule links.

  fedramp_export.py fetch                         download the pinned schemas into the cache
  fedramp_export.py fields SCHEMA [--fragment F]  list every field path the schema defines
  fedramp_export.py export DELIVERABLE.json --schema NAME --out FILE.json

The deliverable holds a "fedramp_export" block that the skill fills after SME Validate:

  "fedramp_export": [{
    "schema": "incident-report",           one of SCHEMAS below
    "fragment": null,                      or a top-level property, for example
                                           "thirdPartyInformationResources" (scope review)
    "document": { ... },                   the JSON to export, field names as the schema defines them
    "sources": {"timeline.detectedAt": [{"item": "RC-3"}], ...},
    "missing": ["certificationPackageOverviewUri"]   values the deliverable does not hold
  }]

One block per schema (the package builder can hold three). Sources name an item of the
deliverable ({"item": "RC-03"}), an input, a rule or a decision, as item sources do.

The export refuses, and writes nothing, when:
  - the deliverable is a draft (sme_validation.status is not "validated")
  - "missing" is not empty, or a value is null or holds a [placeholder]
  - the document uses a field the schema does not define
  - a field in the document has no entry in "sources"
  - the document is not valid against the schema

Schemas are pinned by URL and SHA-256 and downloaded at run time, never committed. If the
download is blocked, save the files by hand into a folder and set FEDRAMP_SCHEMA_DIR to it;
the hashes are still checked.
"""
import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import frmr  # noqa: E402

BASE = "https://fedramp.gov/schemas/fedramp-{name}-schema-2026-06-24.json"
SCHEMAS = {  # name -> sha256 of the published file
    "common-definitions": "19dd37691779171f745ab887444f3604287006af78d261ad76c0cf2dd718e16d",
    "incident-report": "e0871781b6a99c395b8b4854d10ca11e7600ce81c4f3dc6404caddb8ef3105e8",
    "significant-change-notifications": "e0f624b7996c2d8dfb1891c4663fb1df2ec6487a65f03fb43f1ce6ed59910372",
    "security-decision-record": "6a6d7dca1a9ae0031c06df6213bf5c5631e9b9b5fb81c050403cfd723484be86",
    "certification-package-overview": "3870303570bf608dc723cf338cbc3b2295ebd79475003c63699876ac0b89262d",
    "ongoing-certification-report": "c67f4e79a107f106abc2dce50043e798f9708e80a5df2c52e41ed700a3a542c8",
}
# Which skill exports to which schema (the rules that link each schema in the pinned rules data).
SKILL_SCHEMAS = {
    "20x-incident-reporting": {"incident-report": "IEC-CSO-IIR, IEC-CSO-OIR, IEC-CSO-FIR"},
    "20x-change-evaluation": {"significant-change-notifications": "SCN-CSO-INF, SCN-CSO-HRM"},
    "20x-package-builder": {"security-decision-record": "SDR-CSO-FRR, SDR-CSX-KSI, SDR-CSX-KMT",
                            "ongoing-certification-report": "CCM-OCR-AVL",
                            "certification-package-overview": "CPO-CSO-OVR, FRC-CSO-PKG"},
    "20x-scope-review": {"certification-package-overview": "MAS-CSO-TPR (thirdPartyInformationResources only)"},
}
PLACEHOLDER = re.compile(r"\[[^\]]*(confirm|client|owner|tbd|todo)[^\]]*\]", re.IGNORECASE)


def schema_dir() -> Path:
    env = os.environ.get("FEDRAMP_SCHEMA_DIR")
    return Path(env).expanduser() if env else frmr.data_dir() / "schemas"


def fetch(quiet: bool = False) -> Path:
    out = schema_dir()
    out.mkdir(parents=True, exist_ok=True)
    for name, want in SCHEMAS.items():
        dest = out / Path(BASE.format(name=name)).name
        if dest.exists() and frmr.sha(dest.read_bytes()) == want:
            continue
        url = BASE.format(name=name)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "fedramp20x-skills"})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
        except Exception as e:
            sys.exit(f"could not download {url}: {e}\n"
                     f"Save the schema files by hand into a folder and set FEDRAMP_SCHEMA_DIR to it.")
        if frmr.sha(data) != want:
            sys.exit(f"hash mismatch for {dest.name}: got {frmr.sha(data)}. FedRAMP may have changed it; "
                     f"read the new file in full before updating the pin.")
        dest.write_bytes(data)
        if not quiet:
            print(f"downloaded {dest}", file=sys.stderr)
    return out


def load_schemas() -> dict:
    """URL -> schema, every pinned schema, hash checked."""
    d = schema_dir()
    out = {}
    for name, want in SCHEMAS.items():
        url = BASE.format(name=name)
        p = d / Path(url).name
        if not p.exists() or frmr.sha(p.read_bytes()) != want:
            fetch(quiet=True)
        if frmr.sha(p.read_bytes()) != want:
            sys.exit(f"{p}: hash does not match the pin")
        out[url] = json.loads(p.read_text(encoding="utf-8"))
    return out


def resolve(ref: str, here: str, schemas: dict) -> tuple[dict, str]:
    url, _, frag = ref.partition("#")
    url = url or here
    node = schemas[url]
    for part in [p for p in frag.split("/") if p]:
        node = node[part.replace("~1", "/").replace("~0", "~")]
    return node, url


def field_paths(node: dict, here: str, schemas: dict, prefix: str = "", depth: int = 0) -> set:
    """Every field path the schema defines. Array items are written as name[]."""
    if depth > 12:
        return set()
    if "$ref" in node:
        target, url = resolve(node["$ref"], here, schemas)
        merged = {**target, **{k: v for k, v in node.items() if k != "$ref"}}
        return field_paths(merged, url, schemas, prefix, depth + 1)
    out = set()
    for k, sub in (node.get("properties") or {}).items():
        p = f"{prefix}.{k}" if prefix else k
        out.add(p)
        out |= field_paths(sub, here, schemas, p, depth + 1)
    if "items" in node and isinstance(node["items"], dict):
        out.add(prefix + "[]")
        out |= field_paths(node["items"], here, schemas, prefix + "[]", depth + 1)
    for key in ("allOf", "anyOf", "oneOf"):
        for sub in node.get(key, []):
            out |= field_paths(sub, here, schemas, prefix, depth + 1)
    for key in ("then", "else"):
        if isinstance(node.get(key), dict):
            out |= field_paths(node[key], here, schemas, prefix, depth + 1)
    return out


def doc_paths(obj, prefix: str = "") -> list:
    """(path, value) for every leaf in the document, arrays written as name[]."""
    out = []
    if isinstance(obj, dict):
        if not obj and prefix:
            out.append((prefix, obj))
        for k, v in obj.items():
            out += doc_paths(v, f"{prefix}.{k}" if prefix else k)
    elif isinstance(obj, list):
        if not obj:
            out.append((prefix, obj))
        for v in obj:
            out += doc_paths(v, prefix + "[]")
    else:
        out.append((prefix, obj))
    return out


def target(name: str, fragment: str | None, schemas: dict) -> tuple[dict, str]:
    url = BASE.format(name=name)
    root = schemas[url]
    if not fragment:
        return root, url
    if fragment not in root.get("properties", {}):
        sys.exit(f"{fragment} is not a top-level property of {name}")
    sub = dict(root["properties"][fragment])
    sub["$defs"] = root.get("$defs", {})
    return sub, url


def blocks(doc: dict) -> list:
    ex = doc.get("fedramp_export") or []
    return ex if isinstance(ex, list) else [ex]


def check_export(doc: dict, schemas: dict, name: str | None = None, require_validated: bool = True,
                 allow_missing: bool = False) -> tuple[list, dict | None]:
    """Errors, and the document to write when there are none.

    allow_missing is for tests only: schema errors for a required field that the block lists as
    missing are not reported, so a draft example can be checked for everything else."""
    from jsonschema import Draft202012Validator, FormatChecker
    from referencing import Registry, Resource

    err = []
    bl = blocks(doc)
    if not bl:
        return ["the deliverable has no fedramp_export block"], None
    if name is None and len(bl) == 1:
        ex = bl[0]
    else:
        match = [b for b in bl if b.get("schema") == name]
        if len(match) != 1:
            return [f"choose one block with --schema; the deliverable has {[b.get('schema') for b in bl]}"], None
        ex = match[0]
    if require_validated and doc.get("sme_validation", {}).get("status") != "validated":
        err.append("the deliverable is a draft; the export runs only after SME validation")
    name = ex.get("schema")
    if name not in SCHEMAS or name == "common-definitions":
        return err + [f"unknown schema '{name}'; use one of {sorted(set(SCHEMAS) - {'common-definitions'})}"], None
    allowed = SKILL_SCHEMAS.get(doc.get("skill"), {})
    if name not in allowed:
        err.append(f"{doc.get('skill')} does not export to {name}")
    if ex.get("missing") and not allow_missing:
        err.append("values the deliverable does not hold: " + ", ".join(ex["missing"]) + ". Ask the consultant.")
    schema, url = target(name, ex.get("fragment"), schemas)
    defined = field_paths(schema, url, schemas)
    document = ex.get("document")
    if not isinstance(document, dict):
        return err + ["fedramp_export.document must be an object"], None
    sources = ex.get("sources") or {}
    item_ids = {i.get("id") for i in doc.get("items", [])}
    for path, srcs in sources.items():
        for src in srcs:
            if "item" in src and src["item"] not in item_ids:
                err.append(f"sources for {path}: item {src['item']} is not in the deliverable")
    for path, value in doc_paths(document):
        if path not in defined:
            err.append(f"field {path} is not defined in the {name} schema")
        if value is None:
            err.append(f"field {path} is null; leave it out or list it in missing")
        elif isinstance(value, str) and PLACEHOLDER.search(value):
            err.append(f"field {path} holds a placeholder")
        top = path.split("[]")[0]
        if not any(path == s or path.startswith(s + ".") or path.startswith(s + "[]") or top == s for s in sources):
            err.append(f"field {path} has no entry in fedramp_export.sources")
    registry = Registry().with_resources([(u, Resource.from_contents(s)) for u, s in schemas.items()])
    v = Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())
    missing = set(ex.get("missing") or [])
    for e in sorted(v.iter_errors(document), key=lambda e: list(e.absolute_path)):
        if allow_missing and e.validator == "required":
            names = {n for n in e.validator_value if n not in (e.instance or {})}
            if names <= missing:
                continue
        loc = "/".join(str(p) for p in e.absolute_path) or "(document)"
        err.append(f"schema: {loc}: {e.message}")
    return err, (None if err else document)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("fetch")
    f = sub.add_parser("fields")
    f.add_argument("schema", choices=sorted(set(SCHEMAS) - {"common-definitions"}))
    f.add_argument("--fragment")
    e = sub.add_parser("export")
    e.add_argument("file", type=Path)
    e.add_argument("--schema", help="which block, when the deliverable has more than one")
    e.add_argument("--out", type=Path, required=True)
    a = ap.parse_args(argv)
    if a.cmd == "fetch":
        print(fetch())
        return
    schemas = load_schemas()
    if a.cmd == "fields":
        s, url = target(a.schema, a.fragment, schemas)
        print("\n".join(sorted(field_paths(s, url, schemas))))
        return
    doc = json.loads(a.file.read_text(encoding="utf-8"))
    err, out = check_export(doc, schemas, a.schema)
    for x in err:
        print(f"ERROR: {x}")
    if err:
        sys.exit(f"export: {len(err)} error(s); nothing written")
    a.out.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {a.out} (valid against its pinned FedRAMP schema)")


if __name__ == "__main__":
    main()
