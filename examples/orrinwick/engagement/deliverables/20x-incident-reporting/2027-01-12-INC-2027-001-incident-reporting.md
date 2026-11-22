---
title: Incident evaluation: INC-2027-001
client: Orrinwick Labs, Inc.
class: C (CR26)
frmr_version: 2026.11.02.01 (commit 64fa769)
date: 2027-01-12
prepared_by: Claude, for A. Example
sme_validation: Draft: pending SME validation
---

# Incident evaluation: INC-2027-001

| | |
|---|---|
| Mode | evaluate |
| Incident | INC-2027-001 |
| Reportable | Yes, decided by the CISO at 2027-01-12 10:20 ET |
| Rating in force | N5 (default until an estimate is approved) |
| Proposed PAIN rating | N4 (EV-4) |
| Reporting clock | 2027-01-12T10:20:00-05:00 |

## Inputs

| ID | File | Description |
|---|---|---|
| I-19 | `incidents/INC-2027-001.md` | Incident record INC-2027-001 (open) |
| I-05 | `plans/incident-response-plan.md` | Incident response plan, version 1.0 |
| I-14 | `scope/mas-record.json` | Minimum Assessment Scope record, version 0.1.0 |

## Evaluation

| ID | Question | Answer | Sources |
|---|---|---|---|
| EV-1 | Which resources and data classes are involved? | The web console's escalation rule page (part of application compute, P2) showed responder names and work and personal mobile numbers. In the scope record these are responder contact data, D1. | I-19 What happened; I-14 D1; P2 |
| EV-2 | Is the data federal customer data? | Yes. The scope record marks D1 as federal customer data. | I-14 D1 federal_customer_data; FRD-FCD |
| EV-3 | Is confidentiality or integrity affected, or likely to be? | Confidentiality: AGY-07 responder contact data was shown to an AGY-03 administrator. Integrity: the record says the data was shown, not changed. This agrees with the CISO's reportability decision at 10:20 ET. | I-19 What happened; Reportability decision; IEC-CSO-EFR; FRD-FRI |
| EV-4 | Which PAIN rating fits, and which applies now? | Proposed N4, for the CISO to approve: the plan's own example for N4 is responder contact details for one agency being exposed, and the record shows one agency's data (AGY-07) exposed. Until an estimate is approved, N5 applies (IEC-CSO-DPR and plan section 2). A lower rating is arguable because one administrator viewed the page twice and the release was rolled back; the plan says the higher rating applies while evidence is unclear. | I-19 Affected tenants; PAIN rating; I-05 section 2 rating table; section 4; VER-EVA-EPA; IEC-CSO-EFI; IEC-CSO-DPR |
| EV-5 | Is a vulnerability involved that is treated as an incident? | The record names a release defect, not a detected vulnerability. The root cause is not yet known, so this stays open. | I-19 Not yet known; VER-TFR-IRI |

## Reporting timeline

The clock starts at: reportable (2027-01-12T10:20:00-05:00). Business days: Monday to Friday, no holidays skipped. The times are the client's targets from its plan; the FedRAMP rules set no fixed hours.

| Target | Amount | From | Due | Status | Plan reference |
|---|---|---|---|---|---|
| reportability | 1h | declared | 2027-01-12T10:40:00-05:00 | met | Plan section 4: within 1 hour of declaration |
| rating | 4h | reportable | 2027-01-12T14:20:00-05:00 | due | Plan section 4: within 4 hours of the reportability decision |
| initial_report | 1h | clock | 2027-01-12T11:20:00-05:00 | due | Plan section 5: within 1 hour after the clock starts |
| ongoing_report (repeats) | 24h | clock | 2027-01-13T10:20:00-05:00 | due | Plan section 5: at least every 24 hours while open |
| final_report | 5bd | resolved | not stated | needs resolved | Plan section 5: within 5 business days after resolution and recovery |

## Report content

| ID | Report | Item | Supplied by the record | Sources |
|---|---|---|---|---|
| RC-01 | initial | Contact information for the federal incident response coordinator | No: not known for AGY-07 | I-19 record; IEC-CSO-IIR |
| RC-02 | initial | Provider's tracking identifier | Yes: INC-2027-001 | I-19 record; IEC-CSO-IIR |
| RC-03 | initial | Description of the incident | Yes | I-19 record; IEC-CSO-IIR |
| RC-04 | initial | Timeline: start, detection time and source, evaluation completed, milestones | Yes: start 06:55, detection 09:10 by agency report, reportability decision 10:20, containment 10:05 | I-19 record; IEC-CSO-IIR |
| RC-05 | initial | Current and earlier PAIN ratings with the explanation | Partly: N5 default in force; estimate due by 14:20 ET | I-19 record; IEC-CSO-IIR |
| RC-06 | initial | Functional impact, including confidentiality or integrity and data types | Yes: confidentiality of D1 for AGY-07 | I-19 record; IEC-CSO-IIR |
| RC-07 | initial | Estimated recovery plan, milestones and timelines | Partly: rolled back at 10:05 ET; no further milestones recorded | I-19 record; IEC-CSO-IIR |
| RC-08 | initial | List of likely affected agencies | Partly: AGY-07; whether other tenants were affected is not yet known | I-19 record; IEC-CSO-IIR |

## Decisions for the consultant

| ID | Question | Options | Recommendation | Decision |
|---|---|---|---|---|
| DQ-001 | Which PAIN rating does the CISO approve for INC-2027-001? | N4, N3, Keep N5 until the other tenants are checked | Keep N5 until the other tenants are checked: The record does not yet show whether other tenant pairs were affected. The plan applies the higher rating while evidence is unclear. N4 fits if only AGY-07 was exposed | open |

## Open questions

| ID | Question | Why it matters | Blocks | Answer |
|---|---|---|---|---|
| Q-001 | Who is the federal incident response coordinator for AGY-07, and how are they contacted? | The initial report needs the contact; the GRC Lead keeps the agency contacts (plan section 5) | RC-01 | open |
| Q-002 | Were other tenant pairs affected between 06:55 and 10:05 ET? | It decides the list of affected agencies and the rating | RC-08, EV-4 | open |

## SME validation

Draft: pending SME validation.

