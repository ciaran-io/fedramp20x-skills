#!/usr/bin/env python3
"""Download the FedRAMP rules data at one pinned upstream commit for the skills to read.

The files are NOT stored in this repository (the upstream repository has no licence
file). They are downloaded to .frmr/ (or the folder given as the first argument),
listed in .gitignore, and checked against the SHA-256 hashes below so every skill run
reads exactly the same data. Skills cite rule and KSI IDs and do not copy statement text.
The commit and hashes match tools/fetch_frmr.py in github.com/ciaran-io/fedramp20x.
To move to a newer dataset: change COMMIT, run this script, copy the new hashes it
prints into FILES, and rerun the tests in tests/.
"""
import hashlib
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = "https://raw.githubusercontent.com/FedRAMP/rules"
COMMIT = "64fa769510416fa75fd00a4689466094265b8083"
FILES = {  # local name -> (path in upstream repository, sha256)
    "fedramp-consolidated-rules.json": ("fedramp-consolidated-rules.json", "782faecae3eee4aa2aa9d32cdb0de4c929524f2e41dc1f3d143a94a9ca64c4e3"),
    "fedramp-consolidated-rules.schema.json": ("schemas/fedramp-consolidated-rules.schema.json", "2fb59963b5b9161acb1354a2b76fda8b8a832275e1ac1ad93315c031ca350f8d"),
}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / ".frmr"
    out.mkdir(exist_ok=True)
    for local, (path, want) in FILES.items():
        dest = out / local
        if dest.exists() and sha(dest.read_bytes()) == want:
            continue
        url = f"{REPO}/{COMMIT}/{path}"
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                data = r.read()
        except Exception as e:  # network problem or file moved
            print(f"could not download {url}: {e}", file=sys.stderr)
            return 1
        if sha(data) != want:
            print(f"hash mismatch for {local}: got {sha(data)}", file=sys.stderr)
            return 1
        dest.write_bytes(data)
        print(f"downloaded {dest}")
    print(f"FedRAMP rules data ready in {out} at commit {COMMIT[:7]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
