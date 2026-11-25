#!/usr/bin/env python3
"""Read the FedRAMP Consolidated Rules (FRMR) for the fedramp20x-skills.

The rules data is downloaded at one pinned upstream commit and checked against SHA-256
hashes, so every skill run reads the same data. The data is never stored in the
repository (upstream has no licence file). Skills cite rule and KSI IDs; they read the
statement text here and must not copy it into deliverables.

Commands (all output is JSON unless noted):
  fetch                      download the data if it is missing or does not match the hashes
  info                       FRMR version, commit and data folder
  ksis [--class c]           every KSI that applies at the class, with theme, name and controls
                             (at Class A, the KSIs FRC-CLA-MFR names carry class_a_list)
  rules [--class c] [--family VDR] [--type 20x] [--affects Providers]
                             every rule that applies at the class and type, without statement text.
                             At Class A the rules named in FRC-CLA-MFR, -RFR and -OFR are added,
                             with class_a_list and class_a_force (MUST, SHOULD or MAY)
  show ID [--class c]        one rule, KSI or definition, statement included (for reading only)
  term WORD                  definitions whose term or alternative names match WORD
  search TEXT [--class c]    rules and KSIs whose name, statement, following information or notes
                             contain every word of TEXT (search all fields, not only the statement)
  compare --class b [--to c] differences between two classes for 20x provider rules and KSIs:
                             rules and KSIs at one class only, changed force and timeframes,
                             changed statement text (named, not shown), KSIs optional at the class
  lint FILE... [--class c]   check deliverables: unknown IDs, copied statement text,
                             em dashes, compliance verdicts and banned words (exit 1 on errors)

Data folder: $FRMR_DIR if set, else ~/.cache/fedramp20x-skills/frmr-<commit>.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

REPO = "https://raw.githubusercontent.com/FedRAMP/rules"
COMMIT = "64fa769510416fa75fd00a4689466094265b8083"
FILES = {  # local name -> (path in upstream repository, sha256)
    "fedramp-consolidated-rules.json": ("fedramp-consolidated-rules.json", "782faecae3eee4aa2aa9d32cdb0de4c929524f2e41dc1f3d143a94a9ca64c4e3"),
    "fedramp-consolidated-rules.schema.json": ("schemas/fedramp-consolidated-rules.schema.json", "2fb59963b5b9161acb1354a2b76fda8b8a832275e1ac1ad93315c031ca350f8d"),
}
DATA_FILE = "fedramp-consolidated-rules.json"

# IDs look like KSI-IAM-MFA, VDR-TFR-NMV, FRD-PER.
ID_RE = re.compile(r"\b(KSI-[A-Z]{3}-[A-Z]{3}|FRD-[A-Z]{3}|[A-Z]{3}-[A-Z]{3}-[A-Z]{3})\b")
# Families of IDs that are FedRAMP IDs. Other three-part IDs (client policy IDs and so on) are ignored.
FEDRAMP_PREFIXES = None  # filled from the data at load time

BANNED_WORDS = [
    "delve", "leverage", "robust", "seamless", "comprehensive", "crucial", "holistic",
    "navigate", "landscape", "streamline", "foster", "underscore", "additionally",
    "furthermore", "moreover",
]
BANNED_PHRASES = [
    "it is important to note", "it should be noted", "in today's landscape",
    "plays a critical role", "this ensures that", "may potentially", "could possibly",
    "generally tends to",
]
VERDICT_RE = re.compile(
    r"\b(is|are|was|were|be|being|remains?|deemed|found to be|considered)\s+(fully\s+)?"
    r"(fedramp[- ])?compliant\b|\bachieves? compliance\b|\bmeets all\b",
    re.IGNORECASE,
)


def is_verdict(line: str) -> bool:
    """True when the line states compliance. Negated or conditional uses are allowed:
    'does not state whether the client is compliant', 'never write that a client is compliant'."""
    for m in VERDICT_RE.finditer(line):
        before = line[max(0, m.start() - 60):m.start()].lower()
        if re.search(r"\b(whether|not|never|no|if|nothing|statement|claims?)\b", before):
            continue
        return True
    return False


def data_dir() -> Path:
    env = os.environ.get("FRMR_DIR")
    if env:
        return Path(env).expanduser()
    return Path.home() / ".cache" / "fedramp20x-skills" / f"frmr-{COMMIT[:7]}"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def fetch(quiet: bool = False) -> Path:
    out = data_dir()
    out.mkdir(parents=True, exist_ok=True)
    for local, (path, want) in FILES.items():
        dest = out / local
        if dest.exists() and sha(dest.read_bytes()) == want:
            continue
        url = f"{REPO}/{COMMIT}/{path}"
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                data = r.read()
        except Exception as e:  # network problem or file moved
            sys.exit(f"could not download {url}: {e}\n"
                     f"Download the two files at commit {COMMIT} by hand into {out}, or set FRMR_DIR.")
        if sha(data) != want:
            sys.exit(f"hash mismatch for {local}: got {sha(data)}")
        dest.write_bytes(data)
        if not quiet:
            print(f"downloaded {dest}", file=sys.stderr)
    return out


def load() -> dict:
    path = data_dir() / DATA_FILE
    if not path.exists() or sha(path.read_bytes()) != FILES[DATA_FILE][1]:
        fetch(quiet=True)
    return json.loads(path.read_text(encoding="utf-8"))


def resolve(rec: dict, cls: str) -> dict | None:
    """Apply the class variant. Returns None when the record does not apply at the class."""
    variants = rec.get("varies_by_class")
    if not variants:
        return dict(rec)
    if cls not in variants:
        return None
    out = {k: v for k, v in rec.items() if k != "varies_by_class"}
    out.update(variants[cls])
    return out


CLASS_A_LISTS = {"FRC-CLA-MFR": "MUST", "FRC-CLA-RFR": "SHOULD", "FRC-CLA-OFR": "MAY"}
LISTED_ID_RE = re.compile(r"\b(?:KSI|[A-Z]{3})-[A-Z]{3}-[A-Z]{3}\b")


def class_a_lists(d: dict) -> dict:
    """IDs named in the Class A lists (FRC-CLA-MFR, -RFR, -OFR), mapped to (list ID, force).

    At Class A these lists, not the subset applicability, say which other rules and KSIs apply.
    """
    out = {}
    cla = d["FRR"].get("FRC", {}).get("data", {}).get("all", {}).get("CLA", {})
    for lid, force in CLASS_A_LISTS.items():
        for line in cla.get(lid, {}).get("following_information", []):
            for i in LISTED_ID_RE.findall(line):
                out.setdefault(i, (lid, force))
    return out


def _class_a_mark(rid: str, r: dict, listed: dict) -> dict:
    if rid in listed:
        r["class_a_list"], r["class_a_force"] = listed[rid]
    return r


def iter_rules(d: dict, cls: str, typ: str):
    """Yield (id, family, subset, record) for every rule that applies at the class and type.

    At Class A for 20x, the rules named in FRC-CLA-MFR, -RFR and -OFR are added, each with
    class_a_list and class_a_force (MUST, SHOULD or MAY from the list).
    """
    listed = class_a_lists(d) if cls == "a" and typ == "20x" else {}
    seen = set()
    for rid, fam, sname, r in _iter_rules_by_subset(d, cls, typ):
        seen.add(rid)
        yield rid, fam, sname, _class_a_mark(rid, r, listed)
    if not listed:
        return
    for fam, f in d["FRR"].items():
        for sub in f["data"].values():
            for sname, rules in sub.items():
                for rid, rec in rules.items():
                    if rid in listed and rid not in seen:
                        seen.add(rid)
                        r = resolve(rec, cls)
                        if r is None:  # no Class A variant: the list applies the rule as written
                            r = {k: v for k, v in rec.items() if k != "varies_by_class"}
                        yield rid, fam, sname, _class_a_mark(rid, r, listed)


def _iter_rules_by_subset(d: dict, cls: str, typ: str):
    for fam, f in d["FRR"].items():
        subsets = f["info"].get("subsets", {})
        for key, sub in f["data"].items():
            if key not in ("all", typ.lower()):
                continue
            for sname, rules in sub.items():
                app = subsets.get(sname, {}).get("applicability", {})
                if app.get("types") and typ not in app["types"]:
                    continue
                if app.get("classes") and cls.upper() not in app["classes"]:
                    continue
                for rid, rec in rules.items():
                    r = resolve(rec, cls)
                    if r is not None:
                        yield rid, fam, sname, r


def iter_ksis(d: dict, cls: str):
    for theme_key, theme in d["KSI"].items():
        for kid, rec in theme["indicators"].items():
            r = resolve(rec, cls)
            if r is not None:
                yield kid, theme_key, theme, r


def all_ids(d: dict) -> dict:
    """Every ID in the data (any class or type) mapped to its kind."""
    ids = {}
    for fam, f in d["FRR"].items():
        for sub in f["data"].values():
            for rules in sub.values():
                for rid in rules:
                    ids[rid] = "rule"
    for theme in d["KSI"].values():
        for kid in theme["indicators"]:
            ids[kid] = "ksi"
    for fid in d["FRD"]["data"]["all"]:
        ids[fid] = "definition"
    return ids


def cmd_info(d, a):
    print(json.dumps({"frmr_version": d["info"]["version"], "last_updated": d["info"]["last_updated"],
                      "commit": COMMIT, "data_dir": str(data_dir())}, indent=2))


def cmd_ksis(d, a):
    out = []
    listed = class_a_lists(d)
    for kid, tkey, theme, r in iter_ksis(d, a.cls):
        st = r.get("statement") or ""
        out.append({"id": kid, "theme": tkey, "theme_name": theme["name"], "name": r["name"],
                    "optional_at_class": st.startswith("**Optional:**"),
                    "controls": r.get("controls", []), "terms": r.get("terms", [])})
        if a.cls == "a" and kid in listed:
            out[-1]["class_a_list"], out[-1]["class_a_force"] = listed[kid]
        if getattr(a, "statements", False):
            out[-1]["statement"] = st
    print(json.dumps({"class": a.cls.upper(), "count": len(out), "ksis": out}, indent=2))


def cmd_rules(d, a):
    out = []
    for rid, fam, sname, r in iter_rules(d, a.cls, a.type):
        if a.family and fam != a.family.upper():
            continue
        if a.affects and a.affects not in r.get("affects", []):
            continue
        item = {"id": rid, "family": fam, "subset": sname, "name": r.get("name"),
                "force": r.get("force"), "affects": r.get("affects", [])}
        for k in ("timeframe_type", "timeframe_num", "class_a_list", "class_a_force"):
            if k in r:
                item[k] = r[k]
        out.append(item)
    print(json.dumps({"class": a.cls.upper(), "type": a.type, "count": len(out), "rules": out}, indent=2))


COMPARE_FIELDS = ("force", "class_a_force", "timeframe_type", "timeframe_num", "pain_timeframes")


def cmd_compare(d, a):
    """Differences between two classes for 20x provider rules and KSIs, read from the data."""
    def rules(c):
        return {rid: r for rid, _f, _s, r in iter_rules(d, c, "20x") if "Providers" in r.get("affects", [])}

    def ksis(c):
        return {k: r for k, _t, _th, r in iter_ksis(d, c)}

    def opt(r):
        return (r.get("statement") or "").startswith("**Optional:**")

    ra, rb = rules(a.cls), rules(a.to)
    changed = []
    for rid in sorted(set(ra) & set(rb)):
        x, y = ra[rid], rb[rid]
        diff = {k: {a.cls.upper(): x.get(k), a.to.upper(): y.get(k)} for k in COMPARE_FIELDS if x.get(k) != y.get(k)}
        text = [k for k in ("statement", "following_information") if x.get(k) != y.get(k)]
        if diff or text:
            changed.append({"id": rid, "name": x.get("name"), "fields": diff, "text_differs": text})
    ka, kb = ksis(a.cls), ksis(a.to)
    out = {"class": a.cls.upper(), "compared_with": a.to.upper(), "commit": COMMIT,
           "rules_only_at_class": sorted(set(ra) - set(rb)), "rules_only_at_other": sorted(set(rb) - set(ra)),
           "rules_changed": changed,
           "ksis_only_at_class": sorted(set(ka) - set(kb)), "ksis_only_at_other": sorted(set(kb) - set(ka)),
           "ksis_optional_at_class": sorted(k for k in ka if opt(ka[k]) and not (k in kb and opt(kb[k])))}
    print(json.dumps(out, indent=2))


def cmd_show(d, a):
    want = a.id.upper()
    if want.startswith("FRD-"):
        rec = d["FRD"]["data"]["all"].get(want)
        if rec:
            print(json.dumps({"id": want, "kind": "definition", **rec}, indent=2))
            return
    for kid, tkey, theme, r in iter_ksis(d, a.cls):
        if kid == want:
            print(json.dumps({"id": kid, "kind": "ksi", "theme": tkey, **r}, indent=2))
            return
    for rid, fam, sname, r in iter_rules(d, a.cls, a.type):
        if rid == want:
            print(json.dumps({"id": rid, "kind": "rule", "family": fam, "subset": sname, **r}, indent=2))
            return
    if want in all_ids(d):
        sys.exit(f"{want} exists but does not apply at class {a.cls.upper()} for {a.type}")
    sys.exit(f"{want} not found in FRMR {d['info']['version']}")


def cmd_term(d, a):
    w = a.word.lower()
    hits = []
    for fid, rec in d["FRD"]["data"]["all"].items():
        names = [rec.get("term", "")] + rec.get("alts", [])
        if fid.lower() == w or any(w in n.lower() for n in names):
            hits.append({"id": fid, **rec})
    print(json.dumps(hits, indent=2))


def cmd_search(d, a):
    text = " ".join(a.text) if isinstance(a.text, list) else a.text
    words = [w.lower() for w in text.split()]
    hits = []

    def text_of(r):
        parts = [r.get("name", ""), r.get("statement", "") or ""]
        for k in ("following_information", "notes", "following_information_bullets"):
            v = r.get(k)
            parts += v if isinstance(v, list) else [v or ""]
        parts.append(r.get("note", "") or "")
        return " ".join(str(p) for p in parts).lower()

    for rid, fam, sname, r in iter_rules(d, a.cls, a.type):
        if all(w in text_of(r) for w in words):
            hits.append({"id": rid, "kind": "rule", "name": r.get("name")})
    for kid, tkey, theme, r in iter_ksis(d, a.cls):
        if all(w in text_of(r) for w in words):
            hits.append({"id": kid, "kind": "ksi", "name": r.get("name")})
    print(json.dumps({"query": " ".join(a.text) if isinstance(a.text, list) else a.text, "class": a.cls.upper(), "hits": hits}, indent=2))


def statement_ngrams(d: dict, n: int = 10) -> dict:
    """Map each n-word sequence in any statement or definition to the ID it came from."""
    grams = {}

    def add(text, src):
        words = re.findall(r"[a-z0-9]+", (text or "").lower())
        for i in range(len(words) - n + 1):
            grams.setdefault(" ".join(words[i:i + n]), src)

    for rid, fam, sname, r in iter_rules(d, "c", "20x"):
        add(r.get("statement"), rid)
    for kid, tkey, theme, r in iter_ksis(d, "c"):
        add(r.get("statement"), kid)
    for fid, rec in d["FRD"]["data"]["all"].items():
        add(rec.get("definition"), fid)
    return grams


def strip_quotes(text: str) -> str:
    """Remove text inside double quotes and blockquote lines, where quoting is allowed."""
    text = re.sub(r"^>.*$", "", text, flags=re.MULTILINE)
    return re.sub(r"[\"“][^\"”\n]{0,400}[\"”]", "", text)


CLIENT_TEXT_KEYS = {"text", "current", "client_text", "quote"}


def json_strings(obj, key=None):
    """Split a deliverable's string values into its own words and client text it quotes."""
    own, quoted = [], []

    def walk(o, k):
        if isinstance(o, dict):
            for kk, v in o.items():
                walk(v, kk)
        elif isinstance(o, list):
            for v in o:
                walk(v, k)
        elif isinstance(o, str):
            (quoted if k in CLIENT_TEXT_KEYS else own).append(o)

    walk(obj, key)
    return own, "\n".join(quoted)


def text_problems(text: str, grams: dict, unit: str = "line") -> list:
    """Copied statement text, em dashes, compliance verdicts and banned words in a deliverable's own words."""
    problems = []
    body = strip_quotes(text)
    words = re.findall(r"[a-z0-9]+", body.lower())
    seen = set()
    for i in range(len(words) - 9):
        g = " ".join(words[i:i + 10])
        if g in grams and grams[g] not in seen:
            seen.add(grams[g])
            problems.append(("error", f"text copied from the statement of {grams[g]}: '{g}...'"))
    for ln, line in enumerate(text.splitlines(), 1):
        if "\u2014" in line:
            problems.append(("error", f"{unit} {ln}: em dash"))
        if is_verdict(strip_quotes(line)):
            problems.append(("error", f"{unit} {ln}: reads as a compliance verdict"))
        low = strip_quotes(line).lower()
        for w in BANNED_WORDS:
            if re.search(rf"\b{w}\b", low):
                problems.append(("warning", f"{unit} {ln}: avoid the word '{w}'"))
        for ph in BANNED_PHRASES:
            if ph in low:
                problems.append(("warning", f"{unit} {ln}: avoid the phrase '{ph}'"))
    return problems


def cmd_lint(d, a):
    ids = all_ids(d)
    prefixes = {i.split("-")[0] for i in ids}
    applicable = {rid for rid, *_ in iter_rules(d, a.cls, "20x")} | {k for k, *_ in iter_ksis(d, a.cls)}
    applicable |= set(d["FRD"]["data"]["all"])
    grams = statement_ngrams(d)
    errors = warnings = 0
    for f in a.files:
        p = Path(f)
        if not p.exists():
            print(f"ERROR: {f}: file not found (run build_report.py first for the .md)")
            errors += 1
            continue
        text = p.read_text(encoding="utf-8")
        problems = []
        # In a deliverable JSON, client text quoted in these keys is not the deliverable's own words.
        quoted = ""
        own = [text]
        if p.suffix.lower() == ".json":
            try:
                own, quoted = json_strings(json.loads(text))
            except json.JSONDecodeError as e:
                problems.append(("error", f"not valid JSON: {e}"))
                own = []
        own_text = "\n".join(own)
        for m in sorted(set(ID_RE.findall(own_text + "\n" + quoted))):
            if m.split("-")[0] not in prefixes:
                continue  # not a FedRAMP ID (for example a client policy ID)
            if m not in ids:
                problems.append(("error", f"unknown FedRAMP ID {m}"))
            elif m not in applicable and m in ID_RE.findall(own_text):
                problems.append(("warning", f"{m} does not apply at class {a.cls.upper()} for 20x"))
        if p.suffix.lower() in (".md", ".txt", ".json") and not a.ids_only:
            problems += text_problems(own_text, grams, "string" if p.suffix.lower() == ".json" else "line")
        if getattr(a, "client", False):
            problems = [("warning" if lv == "error" and not m.startswith("unknown FedRAMP ID") else lv, m) for lv, m in problems]
        for level, msg in problems:
            print(f"{level.upper()}: {f}: {msg}")
            errors += level == "error"
            warnings += level == "warning"
    print(f"lint: {errors} error(s), {warnings} warning(s) in {len(a.files)} file(s)")
    sys.exit(1 if errors else 0)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("fetch")
    sub.add_parser("info")
    for name in ("ksis", "rules", "show", "lint", "search", "compare"):
        p = sub.add_parser(name)
        p.add_argument("--class", dest="cls", default="c", choices=["a", "b", "c", "d"])
        p.add_argument("--type", default="20x", choices=["20x", "Rev5"])
        if name == "rules":
            p.add_argument("--family")
            p.add_argument("--affects", help="keep rules that affect this party, for example Providers")
        if name == "show":
            p.add_argument("id")
        if name == "ksis":
            p.add_argument("--statements", action="store_true", help="include each KSI statement (read, do not copy)")
        if name == "lint":
            p.add_argument("files", nargs="+")
            p.add_argument("--ids-only", action="store_true", help="check FedRAMP IDs only (for test case files)")
            p.add_argument("--client", action="store_true",
                           help="the files are the client's documents: copied text, em dashes and wording are "
                                "reported as warnings; unknown IDs stay errors")
        if name == "search":
            p.add_argument("text", nargs="+", help="words to search for (quoting is optional)")
        if name == "compare":
            p.add_argument("--to", default="c", choices=["a", "b", "c", "d"], help="class to compare with (default c)")
    p = sub.add_parser("term")
    p.add_argument("word")
    a = ap.parse_args(argv)
    if a.cmd == "fetch":
        print(f"FedRAMP rules data ready in {fetch()} at commit {COMMIT[:7]}")
        return
    d = load()
    {"info": cmd_info, "ksis": cmd_ksis, "rules": cmd_rules, "show": cmd_show,
     "term": cmd_term, "lint": cmd_lint, "search": cmd_search, "compare": cmd_compare}[a.cmd](d, a)


if __name__ == "__main__":
    main()
