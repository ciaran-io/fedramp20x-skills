#!/usr/bin/env python3
"""Run one break test: change a copy of an input, run the check, and record what it reported.

  break_test.py --cmd "python checks.py {policy} {records} --as-of 2026-11-22" \
      --file policy=PATH --file records=PATH \
      --method inr-rir-live \
      (--set records:ir_plan.reviews.-1.reviewed_by='"GRC Lead"' | --replace policy:'OLD=>NEW' |
       --append plan:'TEXT' | --as-of 2027-11-22) \
      [--out break-tests.json]

The check command must print a JSON list of method results, each with method_id, status and
findings. The files are copied to a temporary folder; the originals are never changed.
--set takes a dotted path into a JSON file (list indexes allowed, -1 is the last item) and a
JSON value. --as-of replaces the value after --as-of in the command.

The record states the change, the method, the status observed and the first finding, and
whether the method failed. A break test passes only when the method reported "fail".
With --out, the record is appended to that JSON file (a list), never overwriting earlier ones.
"""
import argparse
import json
import shlex
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


def set_path(obj, path, value):
    keys = path.split(".")
    for k in keys[:-1]:
        obj = obj[int(k)] if isinstance(obj, list) else obj[k]
    last = keys[-1]
    if isinstance(obj, list):
        obj[int(last)] = value
    else:
        obj[last] = value


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cmd", required=True)
    ap.add_argument("--file", action="append", default=[], help="NAME=PATH, used as {NAME} in --cmd")
    ap.add_argument("--method", required=True)
    ap.add_argument("--set", dest="sets", action="append", default=[])
    ap.add_argument("--replace", action="append", default=[])
    ap.add_argument("--append", action="append", default=[])
    ap.add_argument("--as-of")
    ap.add_argument("--out", type=Path)
    a = ap.parse_args(argv)
    tmp = Path(tempfile.mkdtemp(prefix="break-test-"))
    files, changes = {}, []
    try:
        for f in a.file:
            name, path = f.split("=", 1)
            dst = tmp / f"{name}{Path(path).suffix}"
            shutil.copy2(path, dst)
            files[name] = dst
        for s in a.sets:
            target, rest = s.split(":", 1)
            path, value = rest.split("=", 1)
            data = json.loads(files[target].read_text(encoding="utf-8"))
            set_path(data, path, json.loads(value))
            files[target].write_text(json.dumps(data, indent=2), encoding="utf-8")
            changes.append(f"{target}: set {path} to {value}")
        for r in a.replace:
            target, rest = r.split(":", 1)
            old, new = rest.split("=>", 1)
            text = files[target].read_text(encoding="utf-8")
            if old not in text:
                sys.exit(f"--replace: '{old}' not found in {target}")
            files[target].write_text(text.replace(old, new, 1), encoding="utf-8")
            changes.append(f"{target}: replaced '{old}' with '{new}'")
        for p in a.append:
            target, text = p.split(":", 1)
            with files[target].open("a", encoding="utf-8") as fh:
                fh.write("\n" + text + "\n")
            changes.append(f"{target}: appended '{text}'")
        cmd = a.cmd.format(**{k: str(v) for k, v in files.items()})
        parts = shlex.split(cmd)
        if a.as_of:
            if "--as-of" in parts:
                parts[parts.index("--as-of") + 1] = a.as_of
            else:
                parts += ["--as-of", a.as_of]
            changes.append(f"run date set to {a.as_of}")
        proc = subprocess.run(parts, capture_output=True, text=True)
        try:
            results = json.loads(proc.stdout)
        except json.JSONDecodeError:
            sys.exit(f"the check did not print JSON. stderr:\n{proc.stderr}")
        res = next((r for r in results if r.get("method_id") == a.method), None)
        if res is None:
            sys.exit(f"method {a.method} not in the check output")
        record = {"method": a.method, "date": datetime.now().astimezone().date().isoformat(), "run_at": datetime.now().astimezone().isoformat(timespec="seconds"), "change": "; ".join(changes),
                  "observed_status": res["status"], "observed_message": (res.get("findings") or [""])[0],
                  "result": "failed as required" if res["status"] == "fail" else "DID NOT FAIL"}
        print(json.dumps(record, indent=2))
        if a.out:
            existing = json.loads(a.out.read_text(encoding="utf-8")) if a.out.exists() else []
            existing.append(record)
            a.out.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")
        sys.exit(0 if res["status"] == "fail" else 1)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
