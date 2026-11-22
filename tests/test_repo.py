"""Repository tests for fedramp20x-skills. Run: python -m pytest tests

They check that the skills are well formed, the shared files are in sync, the scripts work,
and every example deliverable passes its checks and scores fully against its test case.
The FedRAMP rules data is downloaded on first use (scripts/frmr.py fetch).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SHARED = ROOT / "shared" / "scripts"
sys.path.insert(0, str(SHARED))
sys.path.insert(0, str(ROOT / "tools"))
import check_deliverable  # noqa: E402
import frmr  # noqa: E402
import score  # noqa: E402

ENG = ROOT / "examples" / "orrinwick" / "engagement"
SKILLS = sorted(p for p in (ROOT / "skills").iterdir() if (p / "SKILL.md").exists())
PY = sys.executable


def run(*args, cwd=ROOT):
    return subprocess.run([PY, *map(str, args)], capture_output=True, text=True, cwd=cwd)


@pytest.fixture(scope="session")
def data():
    return frmr.load()


# ---------- skills ----------

def test_nine_skills():
    assert len(SKILLS) == 9


@pytest.mark.parametrize("skill", SKILLS, ids=lambda p: p.name)
def test_skill_is_well_formed(skill):
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"^---\nname: (.+)\ndescription: (.+)\n---\n", text)
    assert m, "front matter with name and description"
    assert m.group(1) == skill.name
    assert len(m.group(2)) <= 1024 and "<" not in m.group(2)
    for needed in ("## Read first", "## Inputs", "## Steps", "SME Validate", "Stop and ask", "references/method.md"):
        assert needed in text, f"{skill.name}: SKILL.md lacks '{needed}'"
    assert (skill / "templates" / "deliverable.json").exists()
    json.loads((skill / "templates" / "deliverable.json").read_text(encoding="utf-8"))
    assert (skill / "scripts" / "build_report.py").exists()
    for ref in re.findall(r"`(references/[\w.-]+|scripts/[\w.-]+|templates/[\w.-]+)`", text):
        assert (skill / ref).exists(), f"{skill.name}: {ref} is referenced but missing"


def test_shared_files_in_sync():
    r = run(ROOT / "tools" / "sync_shared.py", "--check")
    assert r.returncode == 0, r.stdout


def test_marketplace_lists_every_skill():
    m = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    names = {p["name"] for p in m["plugins"]}
    assert "fedramp20x-skills" in names
    for s in SKILLS:
        assert s.name in names
        entry = next(p for p in m["plugins"] if p["name"] == s.name)
        assert entry["skills"] == [f"./skills/{s.name}"]


def test_skill_text_has_no_lint_errors():
    files = [str(p) for p in (ROOT / "skills").rglob("*.md")] + [str(ROOT / "README.md")]
    r = run(SHARED / "frmr.py", "lint", *files)
    assert r.returncode == 0, r.stdout[-2000:]


def test_test_cases_cite_real_ids():
    files = [str(p) for p in (ROOT / "tests").rglob("expected.json")]
    r = run(SHARED / "frmr.py", "lint", *files)
    assert r.returncode == 0, r.stdout[-2000:]


# ---------- examples ----------

EXAMPLES = sorted(p for p in (ENG / "deliverables").rglob("*.json")
                  if not p.name.endswith("-tables.json") and p.name != "break-tests.json")


def test_every_skill_has_an_example():
    assert {p.parent.name for p in EXAMPLES} == {s.name for s in SKILLS}


@pytest.mark.parametrize("path", EXAMPLES, ids=lambda p: p.parent.name)
def test_example_passes_checks(path):
    r = run(SHARED / "check_deliverable.py", path, "--inputs", ENG / "inputs", "--decisions", ENG / "decisions.json")
    assert r.returncode == 0, r.stdout
    md = path.with_suffix(".md")
    assert md.exists()
    r = run(SHARED / "frmr.py", "lint", md, path)
    assert r.returncode == 0, r.stdout


@pytest.mark.parametrize("path", EXAMPLES, ids=lambda p: p.parent.name)
def test_example_report_is_built_from_its_json(path, tmp_path):
    skill = ROOT / "skills" / path.parent.name
    copy = tmp_path / path.name
    copy.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    r = run(skill / "scripts" / "build_report.py", copy)
    assert r.returncode == 0, r.stderr
    assert copy.with_suffix(".md").read_text(encoding="utf-8") == path.with_suffix(".md").read_text(encoding="utf-8"), \
        "the example Markdown differs from what build_report.py writes: rebuild it"


def baseline_cases():
    for exp in sorted((ROOT / "tests").glob("*/baseline/expected.json")):
        e = json.loads(exp.read_text(encoding="utf-8"))
        if e.get("output"):
            yield exp, ROOT / e["output"]


@pytest.mark.parametrize("case", list(baseline_cases()), ids=lambda c: c[0].parent.parent.name)
def test_example_scores_fully(case):
    exp, out = case
    missed, bad = score.score(json.loads(out.read_text(encoding="utf-8")), json.loads(exp.read_text(encoding="utf-8")))
    assert not missed, [m["id"] for m in missed]
    assert not bad, [b["id"] for b in bad]


def test_validator_build_example_tests_pass():
    folder = ENG / "deliverables" / "20x-validator-build" / "inr-rir"
    r = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "test_inr_rir.py"], capture_output=True, text=True, cwd=folder)
    assert r.returncode == 0, r.stdout


def test_break_tests_in_example_all_failed():
    bt = json.loads((ENG / "deliverables" / "20x-validator-build" / "inr-rir" / "break-tests.json").read_text(encoding="utf-8"))
    assert bt and all(b["result"] == "failed as required" for b in bt)


# ---------- scripts ----------

def test_lint_catches_seeded_faults(tmp_path):
    bad = tmp_path / "bad.md"
    bad.write_text("The client is compliant with KSI-INR-RIR.\nThis — dash.\nWe cite KSI-ABC-XYZ.\n"
                   "The effectiveness of documented incident response procedures is persistently reviewed here.\n", encoding="utf-8")
    r = run(SHARED / "frmr.py", "lint", bad)
    assert r.returncode == 1
    for msg in ("compliance verdict", "em dash", "unknown FedRAMP ID KSI-ABC-XYZ", "copied from the statement of KSI-INR-RIR"):
        assert msg in r.stdout


def test_lint_allows_negated_verdicts(tmp_path):
    ok = tmp_path / "ok.md"
    ok.write_text("This review does not state whether the client is compliant.\nNever write that a client is compliant.\n", encoding="utf-8")
    assert run(SHARED / "frmr.py", "lint", ok).returncode == 0


def test_frmr_class_c_ksis(data):
    ksis = [k for k, *_ in frmr.iter_ksis(data, "c")]
    assert len(ksis) == 46 and "KSI-INR-RIR" in ksis


def test_frmr_ccl_rules_are_rev5_only(data):
    ids = {r for r, *_ in frmr.iter_rules(data, "c", "20x")}
    assert "FRC-CCL-UCC" not in ids and "SCN-CSO-EVA" in ids


def test_search_reads_following_information():
    r = run(SHARED / "frmr.py", "search", "class change")
    assert "SCN-CSO-EVA" in r.stdout


def deliverable(**over):
    d = {"skill": "x", "skill_version": "0", "title": "t", "client": "c", "class": "C", "date": "2026-11-22",
         "frmr_version": "v", "frmr_commit": "c", "inputs": [{"id": "I-01", "file": "f"}],
         "items": [{"id": "F-001", "sources": [{"input": "I-01", "location": "A-1"}], "confirmed": True}],
         "decisions_needed": [], "open_questions": [], "sme_validation": {"status": "draft"}}
    d.update(over)
    return d


def test_check_deliverable_rules(data):
    known = set(frmr.all_ids(data))
    assert check_deliverable.check(deliverable(), None, None, known)[0] == []
    err, _ = check_deliverable.check(deliverable(items=[{"id": "F-001", "sources": [], "confirmed": True}]), None, None, known)
    assert any("no sources" in e for e in err)
    err, _ = check_deliverable.check(deliverable(items=[{"id": "F-001", "sources": [{"frmr": "KSI-ABC-XYZ"}]}]), None, None, known)
    assert any("not in the FedRAMP rules data" in e for e in err)
    err, _ = check_deliverable.check(deliverable(sme_validation={"status": "validated"}), None, None, known)
    assert any("validated without" in e for e in err)
    err, _ = check_deliverable.check(deliverable(
        sme_validation={"status": "validated", "validated_by": "A", "role": "B", "date": "2026-11-22"},
        open_questions=[{"id": "Q-001", "blocks": ["F-001"], "answer": None}]), None, None, known)
    assert any("open questions have no answer" in e for e in err)
    err, _ = check_deliverable.check(deliverable(class_="B", **{"class": "B"}), None, None, known)
    assert any("Class C only" in e for e in err)


def test_input_hash_ignores_line_endings(tmp_path):
    a, b = tmp_path / "a.md", tmp_path / "b.md"
    a.write_bytes(b"line one\nline two\n")
    b.write_bytes(b"line one\r\nline two\r\n")
    assert check_deliverable.file_sha256(a) == check_deliverable.file_sha256(b)


def test_scn_timeline_reads_rules():
    r = run(ROOT / "skills" / "20x-change-evaluation" / "scripts" / "scn_timeline.py", "notices", "--type", "transformative",
            "--start", "2027-02-01", "--finish", "2027-02-26")
    out = json.loads(r.stdout)
    due = {n["rule"]: n["due"] for n in out["notices"]}
    # Federal holidays skipped by default: 25 Dec, 1 Jan and 18 Jan (Martin Luther King Jr. Day)
    assert due["SCN-TRF-NIP"] == "2026-12-16" and due["SCN-TRF-NFP"] == "2027-01-15" and due["SCN-TRF-NAF"] == "2027-03-05"
    assert "skipping US federal holidays" in out["business_days"]
    r = run(ROOT / "skills" / "20x-change-evaluation" / "scripts" / "scn_timeline.py", "notices", "--type", "transformative",
            "--start", "2027-02-01", "--no-federal-holidays")
    assert {n["rule"]: n["due"] for n in json.loads(r.stdout)["notices"]}["SCN-TRF-NFP"] == "2027-01-18"


def test_federal_holidays_observed_dates():
    import bizdays
    from datetime import date
    h = bizdays.federal_holidays(2027)
    assert date(2027, 7, 5) in h and date(2027, 6, 18) in h and date(2027, 12, 24) in h and date(2027, 12, 31) in h
    assert date(2027, 1, 18) in h and date(2027, 11, 25) in h and len(h) == 12


def test_incident_timeline_clock_starts_at_reportability():
    r = run(ROOT / "skills" / "20x-incident-reporting" / "scripts" / "incident_timeline.py",
            "--event", "detected=2027-01-12T09:10-05:00", "--event", "reportable=2027-01-12T10:20-05:00",
            "--target", "initial_report:1h:clock")
    out = json.loads(r.stdout)
    assert out["timeline"][0]["due"] == "2027-01-12T11:20:00-05:00"


def test_kmt_metrics():
    r = run(ROOT / "skills" / "20x-package-builder" / "scripts" / "kmt_metrics.py", ENG / "inputs" / "evidence" / "history",
            "--as-of", "2026-11-22", "--ksi", "KSI-INR-RIR")
    out = json.loads(r.stdout)
    assert out["days_with_history"] == 5 and out["ksis"]["KSI-INR-RIR"]["latest"] == "pass"


def test_find_refs():
    r = run(ROOT / "skills" / "20x-sanity-check" / "scripts" / "find_refs.py", ENG / "inputs", "INR-4")
    assert '"file": "policies/POL-INR.md"' in r.stdout


def test_render_word_and_excel(tmp_path):
    pytest.importorskip("docx")
    pytest.importorskip("openpyxl")
    src = ENG / "deliverables" / "20x-policy-review" / "2026-11-22-policy-review"
    assert run(SHARED / "render.py", "docx", src.with_suffix(".md"), tmp_path / "r.docx").returncode == 0
    assert run(SHARED / "render.py", "xlsx", Path(str(src) + "-tables.json"), tmp_path / "r.xlsx").returncode == 0
    from docx import Document
    assert "DRAFT: PENDING SME VALIDATION" in "\n".join(p.text for p in Document(tmp_path / "r.docx").paragraphs)
