---
title: Validator designs: KSI-INR-RPI and KSI-INR-AAR
client: Orrinwick Labs, Inc.
class: C (CR26)
frmr_version: 2026.11.02.01 (commit 64fa769)
date: 2026-11-22
prepared_by: Claude, for A. Example
sme_validation: Draft: pending SME validation
---

# Validator designs: KSI-INR-RPI and KSI-INR-AAR

| | |
|---|---|
| KSIs designed | KSI-INR-RPI, KSI-INR-AAR |
| Status | KSI-INR-RPI: Designed; KSI-INR-AAR: Designed |

Each design states how its methods fail and the break test that will prove it. Status Designed means no method has been built or tested yet.

## Inputs

| ID | File | Description |
|---|---|---|
| I-01 | `policies/POL-INR.md` | POL-INR Incident response policy, version 1.1 |
| I-05 | `plans/incident-response-plan.md` | Incident response plan, version 1.0 |
| I-06 | `records/grc-records.json` | GRC records export: incidents, incident_pattern_reviews, ir_plan |
| I-07 | `../deliverables/20x-policy-review/2026-11-22-policy-review.json` | KSI policy coverage review, 2026-11-22 (draft) |

## KSI-INR-RPI Reviewing Past Incidents

| Field | Design |
|---|---|
| Requirement | Orrinwick must review its past incidents on a repeated, documented cycle to find patterns and weaknesses that no single incident showed. FRD-PER requires the cycle to be documented and its status always known. |
| Policy requirement | POL-INR / INR-4; incident response plan section 9 (past incident review) |
| Resource type | Non-machine: the quarterly past incident review and its record |
| Validation cadence | Every validation run. VDR-TFR-NMV sets a minimum of every 3 months for the check; the review's own cycle comes from INR-4 and the plan |
| Static method | `inr-rpi-static`. Reads POL-INR INR-4 and the past incident review row in plan section 9. Passes when a POL-INR requirement lists KSI-INR-RPI, it states a cycle of 92 days or less, it names one owner role, and the plan names the record location |
| Live method | `inr-rpi-live`. Reads incident_pattern_reviews and incidents in the GRC records export, measured against the run date. Passes when the newest review is no older than the cycle, is not dated after the run date, was recorded by the owner role, lists the incidents it covered, includes every incident and near miss opened since the previous review, and has a findings summary |
| Fails when | No POL-INR requirement lists KSI-INR-RPI. The cycle is missing or longer than 92 days. No owner role is named, or the owner is a group with no lead. No review is recorded, or the newest review is dated after the run date or is older than the cycle. The review was recorded by a role other than the owner. The review does not list the incidents it covered, or misses an incident or near miss opened since the previous review. The review has no findings summary. |
| Break test | inr-rpi-static (Planned): Remove the cycle from INR-4 in a copy of the policy. Expected: POL-INR INR-4 states no review cycle for KSI-INR-RPI inr-rpi-live (Planned): Add an incident opened after the newest review's start date and leave it out of incidents_covered. Expected: Past incident review dated <date> does not cover INC-<id> opened <date> inr-rpi-live (Planned): Set the run date 93 days after the newest review. Expected: Past incident review is 93 days old, the cycle is <cycle> days |
| Production source | The incident tracker named in plan section 10, for incidents and near misses by opened date. The review record in incident_pattern_reviews. The tracker's product and API are not named in the material: [source: client to confirm] |
| Gap | The methods prove that a review happened on time, by the owner, and covered every incident. They do not prove that the review found the patterns that exist, or that its findings led to action. Near misses are covered only if they are recorded in the incident tracker. |
| Status | Designed |
| Sources | I-01 INR-4; I-05 section 9; section 10; I-06 incident_pattern_reviews; incidents; I-07 G-010; Q-006; KSI-INR-RPI; FRD-PER; VDR-TFR-NMV; FRC-CSX-VVK |
| Confirmed | no, see open questions and decisions |

**Decisions.**

- The cycle limit is 92 days pending DQ-001: the plan says at least every 90 days and INR-4 says every quarter. A quarter can be 92 days long.
- The reviewer check waits for DQ-002: the policy names the security team and the plan names the team led by the Security Operations Lead.
- The live method needs reviewed_by, incidents_covered and findings fields that the record does not hold yet (DQ-003).

## KSI-INR-AAR Generating After Action Reports

| Field | Design |
|---|---|
| Requirement | Orrinwick must write an after action report for each incident that needs one, and keep carrying the lessons from those reports into its procedures and service on a documented cycle. |
| Policy requirement | POL-INR / INR-2; incident response plan section 8 |
| Resource type | Non-machine: after action reports and the lessons they record |
| Validation cadence | Every validation run. VDR-TFR-NMV sets a minimum of every 3 months for the check |
| Static method | `inr-aar-static`. Reads POL-INR INR-2 and plan section 8. Passes when a POL-INR requirement lists KSI-INR-AAR, sets the reports' scope (reportable incidents and N2 or above) and a 10 business day deadline, and the plan requires each lesson to carry a ticket or change reference |
| Live method | `inr-aar-reports`. Reads incidents in the GRC records export (pain_rating, reportable, closed, aar_completed), measured against the run date. Passes when every closed incident that is reportable or rated N2 or above has aar_completed within 10 business days of closed. A reportable incident with no rating is treated as N5. A report not yet due is a due-by note |
| Live method | `inr-aar-lessons`. Reads the lessons recorded for each completed report, with their ticket or change reference and status. Passes when every lesson in a completed report has a ticket or change reference, and every open lesson has an owner and a due date that has not passed |
| Fails when | No POL-INR requirement lists KSI-INR-AAR, or it sets no scope or no deadline. The plan does not require a ticket or change reference for each lesson. A closed incident that needs a report has none 10 business days after closing, or the report is dated after the run date. A reportable incident with no rating is not treated as N5. A lesson has no ticket or change reference. An open lesson has no owner, no due date, or a due date before the run date. |
| Break test | inr-aar-static (Planned): Remove the 10 business day deadline from INR-2 in a copy of the policy. Expected: POL-INR INR-2 sets no deadline for after action reports inr-aar-reports (Planned): Add a closed reportable incident with no rating and no aar_completed, and set the run date 11 business days after it closed. Expected: INC-<id> (reportable, unrated, treated as N5) has no after action report 11 business days after closing inr-aar-lessons (Planned): Add a lesson with no ticket reference to a completed report. Expected: Lesson <n> in the report for INC-<id> has no ticket or change reference |
| Production source | The incident tracker named in plan section 10, where after action reports are linked from the incident record, and the backlog that holds the lesson tickets. Neither tool is named in the material: [source: client to confirm] |
| Gap | The methods prove that reports exist on time and that each lesson has a tracked ticket. They do not prove that a report found the right root cause, or that a closed ticket changed what it should have. The record field lessons_incorporated is a single value and cannot show each lesson, so inr-aar-lessons needs a lessons list (DQ-003). |
| Status | Designed |
| Sources | I-01 INR-2; I-05 section 8; section 10; I-06 incidents; I-07 G-001; R-001; KSI-INR-AAR; IEC-CSO-DPR; VDR-TFR-NMV; FRC-CSX-VVK |
| Confirmed | no, see open questions and decisions |

**Decisions.**

- The deadline counts from the date the incident is closed, as plan section 8 states. INR-2 does not say where the 10 days start; the plan settles it.
- Lessons are checked by a third method so the evidence shows reports and lessons separately. This answers policy review gap G-001 only if the client adopts a lesson cycle (R-001).
- An unrated reportable incident is treated as N5, following INR-2 and IEC-CSO-DPR.

## Decisions for the consultant

| ID | Question | Options | Recommendation | Decision |
|---|---|---|---|---|
| DQ-001 | Which cycle applies to the past incident review: every quarter (INR-4) or at least every 90 days (plan section 9)? | 90 days, and change INR-4 to match, One calendar quarter, and change the plan to match, Keep both and check against 92 days | 90 days, and change INR-4 to match: A fixed number of days gives a check one limit, and the plan already uses it | open |
| DQ-002 | Which role must record the past incident review? | Security Operations Lead (plan section 9), CISO, Another role the client names | Security Operations Lead (plan section 9): The plan already names this role as the lead, and it closes policy review gap G-010 once INR-4 uses the same role | open |
| DQ-003 | Will the client add fields to the records: reviewed_by, incidents_covered and findings on each past incident review, and a lessons list (reference, owner, due date, status) on each incident? | Yes, add the fields, No: design against the fields that exist and record the gap | Yes, add the fields: Without them inr-rpi-live cannot check the reviewer or coverage, and inr-aar-lessons cannot run | open |

## Open questions

| ID | Question | Why it matters | Blocks | Answer |
|---|---|---|---|---|
| Q-001 | Which product is the incident tracker, and can it export incidents, near misses and linked after action reports with their dates? | Both designs read it in production. The plan names it only as the incident tracker | V-001, V-002 | open |
| Q-002 | Are near misses recorded in the incident tracker, or somewhere else? | INR-4 and the plan include near misses. The live method can only check what is recorded | V-001 | open |

## SME validation

Draft: pending SME validation.

