#!/usr/bin/env python3
"""Find check methods that still pass when an input they read is emptied (review test R2, lesson L3).

  empty_probe.py --cmd "python checks.py {policy} {records} --as-of 2026-11-22" \
      --file policy=PATH --file records=PATH [--out probe.json]

The check command must print a JSON list of method results, each with method_id, status and
findings (the same contract as break_test.py). For each file in turn, a copy is replaced by an
empty value of the same kind (a JSON object becomes {}, a JSON list becomes [], any other file
becomes empty text) and the check runs on the copies. The originals are never changed.

A method that reports "pass" on an emptied input cannot have checked that input. The report
lists, for each file, the methods that still passed. A method that passes on every emptied
file is listed under "passes_on_all": it may read none of them.
"""
import argparse
import json
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def empty_copy(src: Path, dst: Path):
    text = src.read_text(encoding="utf-8", errors="replace")
    try:
        data = json.loads(text)
        dst.write_text("{}" if isinstance(data, dict) else "[]" if isinstance(data, list) else "null", encoding="utf-8")
    except json.JSONDecodeError:
        dst.write_text("", encoding="utf-8")


def run(cmd: str, files: dict) -> list:
    parts = shlex.split(cmd.format(**{k: str(v) for k, v in files.items()}))
    proc = subprocess.run(parts, capture_output=True, text=True)
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return [{"method_id": "(check)", "status": "error", "findings": [proc.stderr.strip()[-300:]]}]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cmd", required=True)
    ap.add_argument("--file", action="append", default=[], help="NAME=PATH, used as {NAME} in --cmd")
    ap.add_argument("--out", type=Path)
    a = ap.parse_args(argv)
    if not a.file:
        ap.error("give at least one --file")
    tmp = Path(tempfile.mkdtemp(prefix="empty-probe-"))
    try:
        originals = {}
        for f in a.file:
            name, path = f.split("=", 1)
            originals[name] = Path(path)
        base = {}
        for name, path in originals.items():
            base[name] = tmp / "base" / f"{name}{path.suffix}"
            base[name].parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, base[name])
        baseline = {r.get("method_id"): r.get("status") for r in run(a.cmd, base)}
        report = {"baseline": baseline, "emptied": {}}
        still = None
        for name, path in originals.items():
            files = dict(base)
            files[name] = tmp / "empty" / f"{name}{path.suffix}"
            files[name].parent.mkdir(parents=True, exist_ok=True)
            empty_copy(path, files[name])
            results = run(a.cmd, files)
            passed = sorted(r.get("method_id") for r in results if r.get("status") == "pass")
            report["emptied"][name] = {"still_pass": passed}
            still = set(passed) if still is None else still & set(passed)
        report["passes_on_all"] = sorted(still or [])
        print(json.dumps(report, indent=2))
        if a.out:
            a.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
