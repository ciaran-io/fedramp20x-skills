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

def test_ten_skills():
    assert len(SKILLS) == 10


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


def _json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_main_marketplace_lists_the_full_plugin_only():
    # Single-skill plugins live in the second marketplace, so no skill is listed twice.
    m = _json(ROOT / ".claude-plugin" / "marketplace.json")
    assert [p["name"] for p in m["plugins"]] == ["fedramp20x-skills"]
    assert m["plugins"][0]["source"] == "./"
    assert _json(ROOT / ".claude-plugin" / "plugin.json")["name"] == "fedramp20x-skills"


def test_single_marketplace_lists_every_skill_with_matching_names():
    # Each entry name must equal the name in that plugin's plugin.json (Claude Code rule).
    m = _json(ROOT / "single" / ".claude-plugin" / "marketplace.json")
    assert m["name"] == "fedramp20x-skills-single"
    assert sorted(p["name"] for p in m["plugins"]) == [s.name for s in SKILLS]
    for entry in m["plugins"]:
        src = entry["source"]
        assert src["source"] == "git-subdir" and src["url"] == "https://github.com/ciaran-io/fedramp20x-skills.git"
        folder = ROOT / src["path"]
        assert src["path"] == f"single/plugins/{entry['name']}"
        assert _json(folder / ".claude-plugin" / "plugin.json")["name"] == entry["name"]
        assert (folder / "skills" / entry["name"] / "SKILL.md").exists()


def test_one_version_everywhere():
    version = _json(ROOT / ".claude-plugin" / "plugin.json")["version"]
    m = _json(ROOT / "single" / ".claude-plugin" / "marketplace.json")
    for entry in m["plugins"]:
        assert entry["version"] == version
        assert _json(ROOT / entry["source"]["path"] / ".claude-plugin" / "plugin.json")["version"] == version
    assert f"## v{version}" in (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")


def test_skill_text_has_no_lint_errors():
    files = [str(p) for p in (ROOT / "skills").rglob("*.md")] + [str(ROOT / "README.md")]
    r = run(SHARED / "frmr.py", "lint", *files)
    assert r.returncode == 0, r.stdout[-2000:]


def test_test_cases_cite_real_ids():
    files = [str(p) for p in (ROOT / "tests").rglob("expected.json")]
    r = run(SHARED / "frmr.py", "lint", "--ids-only", *files)
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
    for cls in ("A", "B", "C"):
        err, _ = check_deliverable.check(deliverable(**{"class": cls}), None, None, known)
        assert not any("the skills cover" in e for e in err)
    err, _ = check_deliverable.check(deliverable(**{"class": "D"}), None, None, known)
    assert any("Class A, B and C" in e for e in err)


def test_class_a_lists(data):
    """A1: at Class A the rules and KSIs named in FRC-CLA-MFR, -RFR and -OFR apply, with the list's force."""
    listed = frmr.class_a_lists(data)
    assert listed["FRC-CSO-PKG"] == ("FRC-CLA-MFR", "MUST")
    assert listed["IEC-CSO-IIR"] == ("FRC-CLA-RFR", "SHOULD")
    assert listed["CMU-CSO-UVM"] == ("FRC-CLA-OFR", "MAY")
    assert listed["KSI-INR-RIR"][0] == "FRC-CLA-MFR"
    rules_a = {rid: r for rid, _f, _s, r in frmr.iter_rules(data, "a", "20x")}
    for rid, (lid, force) in listed.items():
        if not rid.startswith("KSI-"):
            assert rules_a[rid]["class_a_list"] == lid and rules_a[rid]["class_a_force"] == force
    assert "MAS-CSO-IIR" in rules_a  # listed in MFR, not in the subset applicability for A
    rules_c = {rid: r for rid, _f, _s, r in frmr.iter_rules(data, "c", "20x")}
    assert not any("class_a_list" in r for r in rules_c.values())
    ksis_a = {k for k, *_ in frmr.iter_ksis(data, "a")}
    assert len(ksis_a) == 41 and "KSI-CNA-EIS" not in ksis_a


def test_compare_classes(data, capsys):
    """A3: Class B against Class C, read from the data."""
    frmr.cmd_compare(data, type("A", (), {"cls": "b", "to": "c"})())
    out = json.loads(capsys.readouterr().out)
    assert out["rules_only_at_class"] == [] and out["rules_only_at_other"] == []
    forced = {c["id"] for c in out["rules_changed"]
              if set(c["fields"]) & {"force", "timeframe_type", "timeframe_num"}}
    assert forced == {"CCM-QTR-MTG", "CMU-CSO-UVM", "CPO-CSX-CPM", "FRC-CSX-VVK", "SDR-CSX-KMT", "VDR-TFR-MVX",
                      "VDR-TFR-PCD", "VDR-TFR-PDD", "VDR-TFR-PSD", "VER-TFR-EVU", "VER-TFR-IRI", "VER-TFR-MRH"}
    assert out["ksis_optional_at_class"] == ["KSI-CNA-EIS", "KSI-MLA-ALA", "KSI-SVC-PRR", "KSI-SVC-RUD", "KSI-SVC-VCM"]


def test_lint_class_a_and_b(tmp_path):
    """A6: lint applies the class. MAS-CSO-IIR applies at A only through FRC-CLA-MFR; SCN-ADP-NTF does not apply at A."""
    f = tmp_path / "d.md"
    f.write_text("MAS-CSO-IIR and SCN-ADP-NTF and KSI-CNA-EIS.\n", encoding="utf-8")
    script = ROOT / "shared" / "scripts" / "frmr.py"
    out = {}
    for cls in ("a", "b", "c"):
        r = subprocess.run([sys.executable, "-I", str(script), "lint", "--class", cls, "--ids-only", str(f)],
                           capture_output=True, text=True)
        out[cls] = r.stdout
    assert "SCN-ADP-NTF does not apply at class A" in out["a"] and "MAS-CSO-IIR" not in out["a"]
    assert "KSI-CNA-EIS does not apply at class A" in out["a"]
    assert "does not apply" not in out["b"] and "does not apply" not in out["c"]


def test_placeholder_check_reads_strings_only():
    """A source list is not a [placeholder]; a bracketed placeholder in a confirmed fact is."""
    known = set()
    base = {"id": "F-001", "sources": [{"frmr": "MAS-CSO-IIR"}, {"frmr": "KSI-INR-RIR"}], "confirmed": True,
            "finding": "The scope record lists P4 in scope."}
    _, warn = check_deliverable.check(deliverable(items=[base]), None, None, known)
    assert not any("placeholder" in w for w in warn)
    _, warn = check_deliverable.check(deliverable(items=[dict(base, finding="[owner to confirm] reviews it")]), None, None, known)
    assert any("placeholder" in w for w in warn)


def test_front_matter_states_the_class():
    import report_lib
    assert "class: A" in report_lib.front_matter(deliverable(**{"class": "A"}))
    assert "class: C (CR26)" in report_lib.front_matter(deliverable())


def test_incident_timeline_class_a():
    script = ROOT / "skills" / "20x-incident-reporting" / "scripts" / "incident_timeline.py"
    r = subprocess.run([sys.executable, "-I", str(script), "--event", "reportable=2026-11-24T10:00:00-05:00",
                        "--rating", "3", "--class", "a"], capture_output=True, text=True, check=True)
    out = json.loads(r.stdout)
    assert out["class"] == "A"
    assert out["rule_force"] == {"IEC-CSO-IIR": "SHOULD", "IEC-CSO-OIR": "SHOULD", "IEC-CSO-FIR": "MUST"}


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


# ---------- FedRAMP schema export (J1 to J4) ----------

@pytest.fixture(scope="session")
def schemas():
    import fedramp_export
    pytest.importorskip("jsonschema")
    try:
        return fedramp_export.load_schemas()
    except SystemExit as e:  # schemas not reachable and FEDRAMP_SCHEMA_DIR not set
        pytest.skip(f"FedRAMP schemas not available: {e}")


def export_examples():
    import fedramp_export
    out = []
    for p in sorted((ENG / "deliverables").rglob("*.json")):
        if p.name.endswith("-tables.json"):
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(d, dict) and "fedramp_export" in d:
            for b in fedramp_export.blocks(d):
                out.append((p, b["schema"]))
    return out


def test_export_examples_exist():
    skills = {p.parent.name for p, _ in export_examples()}
    assert {"20x-incident-reporting", "20x-change-evaluation", "20x-package-builder", "20x-scope-review"} <= skills


@pytest.mark.parametrize("path,schema", export_examples(), ids=lambda x: getattr(x, "name", x))
def test_export_example_matches_schema(schemas, path, schema):
    """Every field the example maps is defined in the schema and sourced; the only schema errors
    left are required fields the example lists as missing; the real export refuses the draft."""
    import fedramp_export
    d = json.loads(path.read_text(encoding="utf-8"))
    err, _ = fedramp_export.check_export(d, schemas, schema, require_validated=False, allow_missing=True)
    assert err == []
    err, out = fedramp_export.check_export(d, schemas, schema)
    assert out is None and any("draft" in e for e in err)


def test_export_after_test_only_validation(schemas, tmp_path):
    """A test-only validation with the missing value filled exports valid JSON."""
    import fedramp_export
    p = next(p for p, s in export_examples() if s == "incident-report")
    d = json.loads(p.read_text(encoding="utf-8"))
    d["items"] = [dict(i, confirmed=True) for i in d["items"]]
    d["open_questions"] = []
    d["sme_validation"] = {"status": "validated", "validated_by": "TEST ONLY", "role": "test", "date": "2026-11-22",
                           "corrections": [], "rejected": []}
    b = d["fedramp_export"][0]
    b["document"]["certificationPackageOverviewUri"] = "https://example.invalid/orrinwick/package-overview.json"
    b["sources"]["certificationPackageOverviewUri"] = [{"item": "RC-02"}]
    b["missing"] = []
    f = tmp_path / "d.json"
    f.write_text(json.dumps(d))
    r = run(SHARED / "fedramp_export.py", "export", f, "--out", tmp_path / "out.json")
    assert r.returncode == 0, r.stdout + r.stderr
    assert json.loads((tmp_path / "out.json").read_text())["reportType"] == "Initial"


@pytest.mark.parametrize("change,expect", [
    (lambda doc: doc.update(severity="High"), "not defined"),
    (lambda doc: doc.update(functionalImpact=None), "is null"),
    (lambda doc: doc.update(functionalImpact="[owner: client to confirm]"), "placeholder"),
    (lambda doc: doc.update(reportType="Interim"), "schema: reportType"),
    (lambda doc: doc["potentialImpact"].update(currentRating=7), "schema: potentialImpact/currentRating"),
    (lambda doc: doc.update(rootCause="Unknown"), "no entry in fedramp_export.sources"),
], ids=["undefined-field", "null", "placeholder", "bad-enum", "bad-rating", "unsourced"])
def test_export_break_tests(schemas, change, expect):
    """Each way an export can go wrong is refused."""
    import fedramp_export
    p = next(p for p, s in export_examples() if s == "incident-report")
    d = json.loads(p.read_text(encoding="utf-8"))
    change(d["fedramp_export"][0]["document"])
    err, out = fedramp_export.check_export(d, schemas, "incident-report", require_validated=False, allow_missing=True)
    assert out is None and any(expect in e for e in err), err


@pytest.mark.parametrize("script", sorted(p for p in (ROOT / "skills").glob("*/scripts/*.py")), ids=lambda p: f"{p.parent.parent.name}/{p.name}")
def test_scripts_run_isolated(script, tmp_path):
    """Every script answers --help under python -I, the way the skills tell the model to run it."""
    r = subprocess.run([sys.executable, "-I", str(script), "--help"], capture_output=True, text=True, cwd=tmp_path)
    assert r.returncode == 0, r.stderr[-500:]
