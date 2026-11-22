"""Unit tests for inr_rir.py. FICTIONAL EXAMPLE. Every test fixes the run date."""
import copy
import json
from datetime import date
from pathlib import Path

import inr_rir as m

HERE = Path(__file__).resolve().parent
INPUTS = HERE.parents[2] / "inputs"
POLICY = (INPUTS / "policies" / "POL-INR.md").read_text(encoding="utf-8")
PLAN = (INPUTS / "plans" / "incident-response-plan.md").read_text(encoding="utf-8")
RECORDS = json.loads((INPUTS / "records" / "grc-records.json").read_text(encoding="utf-8"))
AS_OF = date(2026, 11, 22)


def test_baseline_passes():
    assert m.inr_rir_static(POLICY, PLAN, RECORDS)["status"] == "pass"
    assert m.inr_rir_live(POLICY, RECORDS, AS_OF)["status"] == "pass"


def test_static_fails_on_todo():
    r = m.inr_rir_static(POLICY, PLAN + "\nTODO: write the containment steps\n", RECORDS)
    assert r["status"] == "fail" and "TODO" in r["findings"][0]


def test_static_fails_without_owner():
    r = m.inr_rir_static(POLICY.replace("| Owner | CISO |", "| Owner | |"), PLAN, RECORDS)
    assert any("names no owner" in f for f in r["findings"])


def test_static_fails_on_long_cadence():
    rec = copy.deepcopy(RECORDS)
    rec["ir_plan"]["review_cadence_days"] = 400
    assert m.inr_rir_static(POLICY, PLAN, rec)["status"] == "fail"


def test_live_fails_when_overdue():
    r = m.inr_rir_live(POLICY, RECORDS, date(2027, 11, 22))
    assert r["status"] == "fail" and "366 days old" in r["findings"][0]


def test_live_fails_on_wrong_reviewer():
    rec = copy.deepcopy(RECORDS)
    rec["ir_plan"]["reviews"][-1]["reviewed_by"] = "GRC Lead"
    r = m.inr_rir_live(POLICY, rec, AS_OF)
    assert any("'GRC Lead', POL-INR names 'CISO'" in f for f in r["findings"])


def test_live_fails_on_future_review():
    rec = copy.deepcopy(RECORDS)
    rec["ir_plan"]["reviews"].append({"date": "2026-12-01", "reviewed_by": "CISO"})
    assert m.inr_rir_live(POLICY, rec, AS_OF)["status"] == "fail"


def test_live_fails_when_plan_change_has_no_later_review():
    rec = copy.deepcopy(RECORDS)
    rec["incident_pattern_reviews"] = [{"date": "2026-11-22", "plan_change_required": True}]
    r = m.inr_rir_live(POLICY, rec, AS_OF)
    assert any("required a plan change" in f for f in r["findings"])


def test_live_fails_with_no_reviews():
    rec = copy.deepcopy(RECORDS)
    rec["ir_plan"]["reviews"] = []
    assert m.inr_rir_live(POLICY, rec, AS_OF)["findings"] == ["No plan review is recorded"]
