---
title: Assessor review: KSI results, CNA and RPL designs, and two draft deliverables
client: Orrinwick Labs, Inc.
class: C (CR26)
frmr_version: 2026.11.02.01 (commit 64fa769)
date: 2026-11-22
prepared_by: Claude, for A. Example
sme_validation: Draft: pending SME validation
---

# Assessor review: KSI results, CNA and RPL designs, and two draft deliverables

| | |
|---|---|
| Client stage | preparing |
| Areas reviewed | results, design, deliverable |
| Independence | Example only: the two draft deliverables and this review were produced in the same session to show the skills working together. In an engagement, run this skill in a new session or as a separate agent. |
| Findings | 0 High, 1 Moderate, 1 Low, 3 Observation |

The findings report what the evidence shows and where it falls short. They do not state whether the client is compliant.

## Inputs

| ID | File | Description |
|---|---|---|
| I-05 | `plans/incident-response-plan.md` | Incident response plan, version 1.0 |
| I-07 | `../deliverables/20x-policy-review/2026-11-22-policy-review.json` | KSI policy coverage review, 2026-11-22 (draft) |
| I-08 | `../deliverables/20x-validator-design/2026-11-22-validator-design.json` | Validator designs for KSI-INR-RPI and KSI-INR-AAR, 2026-11-22 (draft) |
| I-09 | `evidence/latest.json` | Latest KSI validation result, generated 2026-11-22T17:22:41Z |
| I-10 | `evidence/status-model.md` | Status model for KSI results (README section) |
| I-11 | `designs/CNA.md` | Validator design, CNA theme |
| I-12 | `designs/RPL.md` | Validator design, RPL theme |
| I-13 | `scope/scope-changes.json` | Scope change log, SC-001 and SC-002 |

## Findings

| ID | Title | Area | Rating | Criteria |
|---|---|---|---|---|
| F-001 | 28 KSIs report pass while their coverage notes describe a gap | results | Moderate | FRC-CSX-VVK, KSI-CNA-EIS |
| F-002 | The policy review was written without the incident response plan | deliverable | Low | KSI-INR-RPI, KSI-INR-AAR, KSI-INR-RIR |
| F-003 | A past protection review was edited | results | Observation | KSI-CNA-RVP |
| F-004 | A recovery objectives method has no break test | design | Observation | KSI-RPL-RRO, FRC-CSX-VVK |
| F-005 | Both example deliverables are drafts with open questions | deliverable | Observation | none |

### F-001 28 KSIs report pass while their coverage notes describe a gap

| | |
|---|---|
| Area and test | results, R1 Coverage note |
| Lesson | L11 |
| Observation | The status model defines pass as two or more passing methods with no known gap, and partial as passing with a known gap against the official statement. In the latest result, 28 of the 38 passing KSIs carry a coverage note that says the methods prove less than the KSI, and every one has coverage_gap set to null. For example, the note on KSI-CNA-EIS says the methods detect drift but do not check automatic enforcement, which is a part of that KSI. The result therefore reports pass where the status model's own definition gives partial. |
| Criteria | FRC-CSX-VVK, KSI-CNA-EIS |
| Rating | Moderate |
| Recommendation | For each KSI listed, decide whether the note describes a part of the KSI that no method proves. If it does, record it as a known gap so the KSI rolls up to partial, or add a method that proves the missing part. Keep a coverage note only for limits that leave every part of the KSI proven. |
| Occurrences | KSI-CMT-LMC, KSI-CNA-DFP, KSI-CNA-EIS, KSI-CNA-IBP, KSI-CNA-MAT, KSI-CNA-OFA, KSI-CNA-ULN, KSI-IAM-AAM, KSI-IAM-JIT, KSI-IAM-SUS, KSI-MLA-ALA, KSI-MLA-EVC, KSI-MLA-LET, KSI-MLA-OSM, KSI-MLA-RVL, KSI-PIY-GIV, KSI-PIY-RSD, KSI-RPL-ABO, KSI-RPL-ARP, KSI-RPL-TRC, KSI-SCR-MIT, KSI-SCR-MON, KSI-SVC-ASM, KSI-SVC-PRR, KSI-SVC-RUD, KSI-SVC-SIN, KSI-SVC-VCM, KSI-SVC-VRI |
| Sources | I-09 ksis[].coverage_note and coverage_gap; I-10 Honest status model; FRC-CSX-VVK; KSI-CNA-EIS |
| Confirmed | yes |

### F-002 The policy review was written without the incident response plan

| | |
|---|---|
| Area and test | deliverable, X5 Inputs missing |
| Lesson | L9 |
| Observation | The policy review lists the incident response plan as not provided (Q-001). The plan answers part of three of its items: section 9 names the Security Operations Lead as lead of the past incident review and sets at least every 90 days (G-010, Q-006); section 10 states where plan reviews and past incident reviews are recorded (G-009 for INR-3 and INR-4); section 8 requires a ticket or change reference for each lesson (G-001). The plan also differs from INR-4 on the owner and the cycle, which the policy review could not see. |
| Criteria | KSI-INR-RPI, KSI-INR-AAR, KSI-INR-RIR |
| Rating | Low |
| Recommendation | Add the plan as an input and rerun the policy review for POL-INR. Keep G-010 open as a difference between policy and plan until the client decides the owner and cycle (validator design decisions DQ-001 and DQ-002). |
| Occurrences | G-001, G-009, G-010, Q-001, Q-006 |
| Sources | I-07 not_provided; G-001; G-009; G-010; Q-001; Q-006; I-05 sections 8, 9 and 10; I-08 DQ-001; DQ-002 |
| Confirmed | yes |

### F-003 A past protection review was edited

| | |
|---|---|
| Area and test | results, R4 Edited history |
| Lesson | L4 |
| Observation | The CNA design records that the 2026-06-10 protection review had its resources_covered list added on 2026-11-21, before the rule that records only grow was adopted. The design discloses the edit. The record no longer shows what the 2026 June review covered at the time. |
| Criteria | KSI-CNA-RVP |
| Rating | Observation |
| Recommendation | Keep the disclosure. If the original coverage of the June review is known, record it in a new entry that states it was added on 2026-11-21, rather than relying on the edited entry. |
| Occurrences | protection_reviews 2026-06-10 |
| Sources | I-11 KSI-CNA-RVP decisions; KSI-CNA-RVP |
| Confirmed | yes |

### F-004 A recovery objectives method has no break test

| | |
|---|---|
| Area and test | design, D8 Break test |
| Lesson | L3 |
| Observation | The RPL design records a break test for rpl-rro-live and states for the static method: not yet run. The design status is Built, which is consistent, but KSI-RPL-RRO cannot reach Verified until rpl-rro-static is shown to fail. |
| Criteria | KSI-RPL-RRO, FRC-CSX-VVK |
| Rating | Observation |
| Recommendation | Run a break test for rpl-rro-static, for example with the review cadence removed, and record the message. |
| Occurrences | rpl-rro-static |
| Sources | I-12 KSI-RPL-RRO break test; KSI-RPL-RRO |
| Confirmed | yes |

### F-005 Both example deliverables are drafts with open questions

| | |
|---|---|
| Area and test | deliverable, X3 Status |
| Lesson | none |
| Observation | The policy review and the validator designs are marked draft, with unconfirmed items and open questions. This is the correct status. They cannot be relied on as client deliverables until SME validation. |
| Criteria | none |
| Rating | Observation |
| Recommendation | Complete SME validation for each before sharing it with the client. |
| Occurrences | policy review: G-004, G-008 unconfirmed, validator designs: V-001, V-002 unconfirmed |
| Sources | I-07 sme_validation; items; I-08 sme_validation; items |
| Confirmed | yes |

## Not assessed now

| Rules | Reason | Starts when | Basis |
|---|---|---|---|
| FRC-APP subset, MKT | The client is preparing and has not applied for certification or a Marketplace listing | The client applies | Consultant: client stage is preparing |
| CCM-OCR subset, CCM-QTR subset, IVV-CSO-FIA | Ongoing reports, quarterly reviews and annual assessments follow certification | Certification | Consultant: client stage is preparing |
| SCN notification rules (SCN-ADP-NTF, SCN-TRF-NIP, SCN-TRF-NFP, SCN-TRF-NAF) | No agency relies on the offering yet, as the scope change log records for SC-001 | The first agency uses the offering | I-13 SC-001 evaluation |

## Decisions for the consultant

None.

## Open questions

| ID | Question | Why it matters | Blocks | Answer |
|---|---|---|---|---|
| Q-001 | Can the earlier assessor findings (A1 to A12) be provided? | Their status, open or closed, can only be reported from the findings themselves | none | open |

## SME validation

Draft: pending SME validation.

