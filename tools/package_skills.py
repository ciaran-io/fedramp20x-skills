#!/usr/bin/env python3
"""Build .zip files for claude.ai: one per skill and one for the full plugin.

  python tools/package_skills.py   writes dist/<skill>.zip and dist/fedramp20x-skills.zip

Runs the shared file check first, so every zip carries current copies of the shared
scripts and references. Each skill zip holds one folder named after the skill, with
SKILL.md at its top, which is the layout claude.ai expects for an uploaded skill.
"""
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"__pycache__", ".pytest_cache"}


def add_tree(z: zipfile.ZipFile, folder: Path, arc_root: str):
    for p in sorted(folder.rglob("*")):
        if p.is_file() and not (set(p.parts) & SKIP) and p.suffix != ".pyc":
            z.write(p, f"{arc_root}/{p.relative_to(folder).as_posix()}")


def main():
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "sync_shared.py"), "--check"])
    if r.returncode:
        sys.exit("shared files are out of date: run python tools/sync_shared.py first")
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    skills = sorted(p for p in (ROOT / "skills").iterdir() if (p / "SKILL.md").exists())
    for s in skills:
        with zipfile.ZipFile(dist / f"{s.name}.zip", "w", zipfile.ZIP_DEFLATED) as z:
            add_tree(z, s, s.name)
    with zipfile.ZipFile(dist / "fedramp20x-skills.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in (".claude-plugin/plugin.json", "README.md", "LICENSE"):
            z.write(ROOT / f, f"fedramp20x-skills/{f}")
        for s in skills:
            add_tree(z, s, f"fedramp20x-skills/skills/{s.name}")
    print(f"wrote {len(skills) + 1} zip files to {dist}")


if __name__ == "__main__":
    main()
