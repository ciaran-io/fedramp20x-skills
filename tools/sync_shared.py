#!/usr/bin/env python3
"""Keep every copy of the shared files and the single-skill plugins in step.

Each skill folder must work on its own (copied into ~/.claude/skills, or uploaded to
claude.ai as a .zip), so it carries its own copy of shared/scripts and shared/references.

Each skill is also published as a plugin of its own in the second marketplace,
single/.claude-plugin/marketplace.json. A plugin's name must match its marketplace entry,
so each one has its own folder, single/plugins/<skill>/, with its own plugin.json and a
copy of the skill folder. The version and the other plugin.json fields come from the
root .claude-plugin/plugin.json; the description comes from the skill's SKILL.md.

Edit the files in shared/ and skills/, never in single/, then run this script.
tests/test_repo.py and CI fail when any copy differs.

  python tools/sync_shared.py          copy
  python tools/sync_shared.py --check  report differences, exit 1 if any
"""
import filecmp
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHARED = {"scripts": ROOT / "shared" / "scripts", "references": ROOT / "shared" / "references"}
SINGLE = ROOT / "single"
REPO = "ciaran-io/fedramp20x-skills"
SKIP = {"__pycache__", ".pytest_cache"}


def skills():
    return sorted(p for p in (ROOT / "skills").iterdir() if (p / "SKILL.md").exists())


def shared_pairs():
    for skill in skills():
        for sub, src_dir in SHARED.items():
            for f in sorted(src_dir.iterdir()):
                if f.is_file() and f.suffix in (".py", ".md"):
                    yield f, skill / sub / f.name


def tree_files(folder: Path):
    return sorted(p.relative_to(folder) for p in folder.rglob("*")
                  if p.is_file() and not (set(p.parts) & SKIP) and p.suffix != ".pyc")


def description(skill: Path) -> str:
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    m = re.search(r"^description:\s*(.+)$", text, re.M)
    if not m:
        sys.exit(f"{skill.name}: SKILL.md has no description line")
    return m.group(1).strip()


def root_manifest() -> dict:
    return json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))


def plugin_json(skill: Path) -> str:
    root = root_manifest()
    m = {"name": skill.name, "version": root["version"], "description": description(skill)}
    for k in ("author", "homepage", "repository", "license", "keywords"):
        if k in root:
            m[k] = root[k]
    return json.dumps(m, indent=2, ensure_ascii=False) + "\n"


def single_marketplace() -> str:
    main = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    m = {
        "name": "fedramp20x-skills-single",
        "description": "FedRAMP 20x consultant skills, one plugin per skill. "
                       "For all skills in one plugin, add the marketplace ciaran-io/fedramp20x-skills instead.",
        "owner": main["owner"],
        "plugins": [
            {
                "name": s.name,
                "source": {"source": "git-subdir", "url": REPO, "path": f"single/plugins/{s.name}"},
                "description": description(s),
                "version": root_manifest()["version"],
            }
            for s in skills()
        ],
    }
    return json.dumps(m, indent=2, ensure_ascii=False) + "\n"


def expected_single():
    """Yield (path, content) for every generated text file, and (dst, src) for copies."""
    texts = {SINGLE / ".claude-plugin" / "marketplace.json": single_marketplace()}
    copies = {}
    for s in skills():
        base = SINGLE / "plugins" / s.name
        texts[base / ".claude-plugin" / "plugin.json"] = plugin_json(s)
        for rel in tree_files(s):
            copies[base / "skills" / s.name / rel] = s / rel
    return texts, copies


def main():
    check = "--check" in sys.argv
    bad = []

    for src, dst in shared_pairs():
        if check:
            if not dst.exists() or not filecmp.cmp(src, dst, shallow=False):
                bad.append(dst)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    texts, copies = expected_single()
    wanted = set(texts) | set(copies)
    present = {SINGLE / p for p in tree_files(SINGLE)} if SINGLE.exists() else set()
    for extra in sorted(present - wanted):
        if check:
            bad.append(extra)
        else:
            extra.unlink()
    for path, content in texts.items():
        if check:
            if not path.exists() or path.read_text(encoding="utf-8").replace("\r\n", "\n") != content:
                bad.append(path)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
    for dst, src in copies.items():
        if check:
            if not dst.exists() or not filecmp.cmp(src, dst, shallow=False):
                bad.append(dst)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    if check:
        for b in bad:
            print(f"out of date: {b.relative_to(ROOT).as_posix()}")
        print(f"sync check: {len(bad)} file(s) out of date")
        sys.exit(1 if bad else 0)
    if SINGLE.exists():
        for d in sorted((p for p in SINGLE.rglob("*") if p.is_dir()), reverse=True):
            if not any(d.iterdir()):
                d.rmdir()
    print(f"copied shared files into {len(skills())} skill(s) and built {len(skills())} single-skill plugin(s)")


if __name__ == "__main__":
    main()
