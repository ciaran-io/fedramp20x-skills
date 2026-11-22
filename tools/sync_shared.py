#!/usr/bin/env python3
"""Copy shared/scripts and shared/references into every skill folder.

Each skill folder must work on its own (copied into ~/.claude/skills, or uploaded to
claude.ai as a .zip), so it carries its own copy of the shared files. Edit the files in
shared/, then run this script. tests/test_repo.py fails when a copy differs.

  python tools/sync_shared.py          copy
  python tools/sync_shared.py --check  report differences, exit 1 if any
"""
import filecmp
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHARED = {"scripts": ROOT / "shared" / "scripts", "references": ROOT / "shared" / "references"}


def skills():
    return sorted(p for p in (ROOT / "skills").iterdir() if (p / "SKILL.md").exists())


def pairs():
    for skill in skills():
        for sub, src_dir in SHARED.items():
            for f in sorted(src_dir.iterdir()):
                if f.is_file() and f.suffix in (".py", ".md"):
                    yield f, skill / sub / f.name


def main():
    check = "--check" in sys.argv
    bad = []
    for src, dst in pairs():
        if check:
            if not dst.exists() or not filecmp.cmp(src, dst, shallow=False):
                bad.append(dst.relative_to(ROOT))
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    if check:
        for b in bad:
            print(f"out of date: {b}")
        print(f"sync check: {len(bad)} file(s) out of date")
        sys.exit(1 if bad else 0)
    print(f"copied shared files into {len(skills())} skill(s)")


if __name__ == "__main__":
    main()
