#!/usr/bin/env python3
"""Update the recorded SHA-256 of example inputs after an example file is edited on purpose.

Example deliverables record the hash of each input, including other example deliverables
(../deliverables/...). After an intended edit, run this until it reports no change, then
review the diff. Never run it to silence a hash error you do not understand.

  python tools/rehash_examples.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "shared" / "scripts"))
import check_deliverable as c  # noqa: E402

E = ROOT / "examples" / "orrinwick" / "engagement"


def once() -> int:
    n = 0
    for j in sorted((E / "deliverables").rglob("*.json")):
        if j.name.endswith("-tables.json"):
            continue
        try:
            d = json.loads(j.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        if not isinstance(d, dict) or "inputs" not in d:
            continue
        changed = False
        for i in d["inputs"]:
            f = c.resolve_input(E / "inputs", i.get("file", ""))
            if f.exists() and i.get("sha256") and c.file_sha256(f) != i["sha256"]:
                i["sha256"] = c.file_sha256(f)
                changed = True
                print(f"rehashed {j.relative_to(ROOT)} {i['id']}")
        if changed:
            j.write_text(json.dumps(d, indent=2) + "\n", encoding="utf-8")
            n += 1
    return n


if __name__ == "__main__":
    for _ in range(10):
        if not once():
            break
