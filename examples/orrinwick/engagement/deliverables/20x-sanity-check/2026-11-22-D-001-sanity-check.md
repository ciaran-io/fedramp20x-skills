---
title: Sanity check: D-001 past incident review cycle and owner
client: Orrinwick Labs, Inc.
class: C (CR26)
frmr_version: 2026.11.02.01 (commit 64fa769)
date: 2026-11-22
prepared_by: Claude, for A. Example
sme_validation: Draft: pending SME validation
---

# Sanity check: D-001 past incident review cycle and owner

| | |
|---|---|
| Decision | D-001: The past incident review (KSI-INR-RPI) runs at least every 90 days and is recorded by the Security Operations Lead. |
| Decided by | A. Example (consultant), confirmed with the Orrinwick CISO |
| Search terms | INR-4, KSI-INR-RPI, every quarter, quarterly, 90 days, security team, Security Operations Lead, incident_pattern_reviews |
| Places | 3 disagrees, 1 silent, 4 affected, 1 agrees |
| Follow-ups | 7 |

This check lists where the decision applies. It changes no document. Each follow-up needs approval by the owner named.

## Inputs

| ID | File | Description |
|---|---|---|
| I-01 | `policies/POL-INR.md` | POL-INR Incident response policy, version 1.1 |
| I-05 | `plans/incident-response-plan.md` | Incident response plan, version 1.0 |
| I-06 | `records/grc-records.json` | GRC records export |
| I-07 | `../deliverables/20x-policy-review/2026-11-22-policy-review.json` | KSI policy coverage review (draft) |
| I-08 | `../deliverables/20x-validator-design/2026-11-22-validator-design.json` | Validator designs for KSI-INR-RPI and KSI-INR-AAR (draft) |
| I-17 | `../deliverables/20x-assessor-review/2026-11-22-assessor-review.json` | Assessor review (draft) |

## Places

| ID | Document and location | Status | What it says or needs |
|---|---|---|---|
| P-01 | I-01 INR-4 (line 36); D-001 | disagrees | INR-4 names the security team and sets every quarter. |
| P-02 | I-01 INR-3 (line 35); D-001 | disagrees | INR-3 calls the review a quarterly incident review. |
| P-05 | I-05 section 9, plan review (line 130); D-001 | disagrees | The plan review row calls the trigger a quarterly incident review. |
| P-04 | I-05 section 9, past incident review (line 131); D-001 | silent | The same row names the security team, led by the Security Operations Lead, as owner. It does not say who records the review. |
| P-06 | I-06 incident_pattern_reviews; D-001 | affected | Each incident_pattern_reviews entry holds date and summary only. A check of the reviewer needs a reviewed_by field. |
| P-07 | I-08 V-001; DQ-001; DQ-002; D-001 | affected | inr-rpi-static allows a cycle of 92 days or less, and the reviewer check waits for DQ-001 and DQ-002. D-001 answers both. |
| P-08 | I-07 G-010; Q-006; D-001 | affected | G-010 and Q-006 ask which role runs and records the review. D-001 answers Q-006. |
| P-09 | I-17 F-002; D-001 | affected | F-002 recommends keeping G-010 open until the owner and cycle are decided. D-001 decides them. |
| P-03 | I-05 section 9, past incident review (line 131); D-001 | agrees | The past incident review row sets at least every 90 days. |

## Follow-ups

| ID | Change | Where | Approver | Status | For place |
|---|---|---|---|---|---|
| FU-01 | Change INR-4 to name the Security Operations Lead and to set at least every 90 days. | POL-INR INR-4 | CISO (POL-INR approver) | proposed | P-01 |
| FU-02 | Call the trigger in INR-3 and in the plan review row the past incident review, so neither says quarterly. | POL-INR INR-3; plan section 9, plan review row | CISO | proposed | P-02, P-05 |
| FU-03 | State in the past incident review row that the Security Operations Lead records each review. | Plan section 9, past incident review row | CISO (plan approver) | proposed | P-04 |
| FU-04 | Add reviewed_by to each incident_pattern_reviews entry. Validator design DQ-003 also asks for incidents_covered and findings. | GRC records, incident_pattern_reviews | [approver: client to confirm] | proposed | P-06 |
| FU-05 | Record D-001 against DQ-001 and DQ-002, set the inr-rpi-static limit to 90 days, and compare reviewed_by with the Security Operations Lead. | Validator design V-001 | A. Example (consultant) | proposed | P-07 |
| FU-06 | Record D-001 as the answer to Q-006, and update G-010 and rewrite R-006 with the Security Operations Lead. | Policy review G-010, Q-006, R-006 | A. Example (consultant) | proposed | P-08 |
| FU-07 | Note in F-002 that D-001 decided the owner and cycle. | Assessor review F-002 | A. Example (consultant) | proposed | P-09 |

## Decisions for the consultant

None.

## Open questions

| ID | Question | Why it matters | Blocks | Answer |
|---|---|---|---|---|
| Q-001 | Who approves changes to the fields of the GRC records? | FU-04 needs an approver; the inputs do not name one | FU-04 | open |

## SME validation

Draft: pending SME validation.

