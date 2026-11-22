#!/usr/bin/env python3
"""Find every place a decision's terms appear in a set of documents.

  find_refs.py FOLDER TERM [TERM ...] [--context 1]

Searches Markdown, text, JSON, YAML, CSV, Python and Word (.docx) files under FOLDER,
case-insensitive, and prints one JSON object per hit: file, line, the matched term and
the line text (with neighbouring lines when --context is set). Use IDs (KSI-INR-RPI,
INR-4, COND-S1-1), role names, numbers with units ("90 days", "every quarter") and
system names as terms. The output lists where to look; it does not judge agreement.
"""
import argparse
import json
import re
from pathlib import Path

TEXT = {".md", ".txt", ".json", ".yaml", ".yml", ".csv", ".py"}


def lines_of(p: Path):
    if p.suffix.lower() == ".docx":
        try:
            from docx import Document
        except ImportError:
            return [f"[python-docx not installed: {p.name} not searched]"]
        doc = Document(p)
        out = [par.text for par in doc.paragraphs]
        for t in doc.tables:
            for row in t.rows:
                out.append(" | ".join(c.text for c in row.cells))
        return out
    return p.read_text(encoding="utf-8", errors="replace").splitlines()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder", type=Path)
    ap.add_argument("terms", nargs="+")
    ap.add_argument("--context", type=int, default=0)
    a = ap.parse_args(argv)
    pats = [(t, re.compile(re.escape(t), re.IGNORECASE)) for t in a.terms]
    hits = 0
    for p in sorted(a.folder.rglob("*")):
        if not p.is_file() or (p.suffix.lower() not in TEXT and p.suffix.lower() != ".docx"):
            continue
        ls = lines_of(p)
        for n, line in enumerate(ls):
            for term, pat in pats:
                if pat.search(line):
                    lo, hi = max(0, n - a.context), min(len(ls), n + a.context + 1)
                    print(json.dumps({"file": str(p.relative_to(a.folder)), "line": n + 1, "term": term,
                                      "text": " / ".join(x.strip() for x in ls[lo:hi])[:400]}))
                    hits += 1
    print(json.dumps({"hits": hits, "terms": a.terms}))


if __name__ == "__main__":
    main()
