---
title: Class A readiness: Orrinwick Beacon
client: Orrinwick Labs, Inc.
class: A
frmr_version: 2026.11.02.01 (commit 64fa769)
date: 2026-11-24
prepared_by: Claude, for A. Example
sme_validation: Draft: pending SME validation
---

# Class A readiness: Orrinwick Beacon

| | |
|---|---|
| Planned submission | not stated |
| Framework | SOC 2 Type II, completed 2026-08-14 (report date); examination period ended 2026-06-30 |
| Findings | 1 High, 6 Moderate, 0 Low, 2 Observation |
| Mandatory rules and KSIs | 0 mapped, 5 partial, 0 unmapped, 19 not reviewed |
| Recommendations | 20 |

This report states what the evidence shows against the Class A rules. It does not state that the client is ready or certified.

## Inputs

| ID | File | Description |
|---|---|---|
| I-01 | `alternative-framework/soc2-type2-summary.md` | Consultant's summary of the SOC 2 Type II materials (fictional) |
| I-02 | `scope/mas-record.json` | Minimum Assessment Scope record |
| I-03 | `plans/incident-response-plan.md` | Incident response plan, version 1.0 |
| I-04 | `../deliverables/20x-policy-review/2026-11-22-policy-review.json` | KSI policy coverage review (draft) |

## Alternative framework (FRC-CLA-ASF)

| ID | Framework | Completed | Assessor | Period | Window closes | Within window | Finding | Rating | Recommendation | Sources |
|---|---|---|---|---|---|---|---|---|---|---|
| A-01 | SOC 2 Type II | 2026-08-14 (report date); examination period ended 2026-06-30 | Example Assurance LLP, an independent CPA firm | 2026-01-01 to 2026-06-30 | 2027-06-30 if the period end counts; 2027-08-14 if the report date counts | yes | SOC 2 Type II is on the FRC-CLA-ASF list and was performed by an independent service auditor. The completion date is within 12 months of today under either reading. | none | none | I-01 section 1; FRC-CLA-ASF |
| A-02 | SOC 2 Type II | 2026-08-14 (report date); examination period ended 2026-06-30 | Example Assurance LLP | 2026-01-01 to 2026-06-30 | 2027-06-30 if the period end counts; 2027-08-14 if the report date counts | unclear | The client plans to submit in the second quarter of 2027 but has set no date. If the period end counts as completion, the window closes on 2027-06-30, inside that quarter. The next report, expected in February 2027, would open a new window. | Observation | Set the submission date, decide DQ-001, and plan to submit with the February 2027 report if the date falls after the window closes. | I-01 sections 1, 3 and 4; FRC-CLA-ASF; DQ-001 |

## Assessment materials (FRC-CLA-EAM)

| ID | Material | Status | Finding | Rating | Recommendation | Sources |
|---|---|---|---|---|---|---|
| M-01 | Complete SOC 2 Type II report | present | The consultant received the full report. | none | none | I-01 section 1; FRC-CLA-EAM |
| M-02 | Bridge or gap letter | missing | The examination period ended on 2026-06-30 and no letter covers the time since. The GRC Lead says the auditor issues one on request. | High | Request a bridge letter from the service auditor covering 2026-07-01 to the submission date. | I-01 section 3; FRC-CLA-EAM |
| M-03 | Verified audit engagement documentation | partial | The signed engagement letter was supplied. Nothing shows how the engagement can be verified with the auditor. | Moderate | Ask the auditor how a party can verify the engagement, and record the contact and method in the package. | I-01 section 3; FRC-CLA-EAM |
| M-04 | Estimated schedule for the next report | present | An email from the auditor gives the next period (2026-07-01 to 2026-12-31) and a report expected in February 2027. | none | none | I-01 section 3; FRC-CLA-EAM |
| M-05 | Supplemental compliance evidence, if applicable | missing | None was supplied. The material does not show whether any is applicable. | Observation | Answer Q-001. | I-01 section 3; FRC-CLA-EAM |

## Mandatory rules and KSIs (FRC-CLA-MFR)

| ID | Rule or KSI | Status | Mapped to | Package location | Finding | Rating | Recommendation |
|---|---|---|---|---|---|---|---|
| P-01 | MAS-CSO-IIR | partial | Scope record, information resource P4 (object storage) | Class A mapping table in the Certification Package (FRC-CLA-MFR) | The scope record puts P4, which holds customer exports and backup copies, in scope. The SOC 2 examination excludes the data export and backup store, so part of the offering is outside the assessed scope. | Moderate | Ask the auditor to bring the export and backup store into the next examination, or record how the client covers it until then. |
| P-02 | IEC-CSO-FIR | partial | Incident response plan, Final Incident Report paragraph | Class A mapping table in the Certification Package (FRC-CLA-MFR) | The plan sends the final report within 5 business days after resolution. At Class A, incident_timeline.py gives 3 business days for every PAIN rating. | Moderate | Change the plan to the Class A timeframe from the rules data, and say which class's timeframes apply. |
| P-03 | KSI-CMT-LMC | partial | POL-CMT/CMT-1, POL-CMT/CMT-5, POL-CMT/CMT-6 | Class A mapping table in the Certification Package (FRC-CLA-MFR) | The policy review rated coverage partial (G-006): Logging stated; monitoring not stated. | Moderate | Close G-006 from the policy review before submission. |
| P-04 | KSI-CNA-RNT | partial | POL-CNA/CNA-6 | Class A mapping table in the Certification Package (FRC-CLA-MFR) | The policy review rated coverage partial (G-002, G-008): No review cycle. | Moderate | Close G-002, G-008 from the policy review before submission. |
| P-08 | KSI-INR-RIR | partial | POL-INR/INR-1, POL-INR/INR-3 | Class A mapping table in the Certification Package (FRC-CLA-MFR) | The policy review rated coverage partial (G-008, G-009): Owner and cycle stated; record location not stated. | Moderate | Close G-008, G-009 from the policy review before submission. |
| P-05 | KSI-CED-RAT | not reviewed | not stated | Class A mapping table in the Certification Package (FRC-CLA-MFR) | The policy review did not cover this KSI: POL-CED was not provided. | none | Answer Q-002. |
| P-06 | KSI-IAM-AAM | not reviewed | not stated | Class A mapping table in the Certification Package (FRC-CLA-MFR) | The policy review did not cover this KSI: POL-IAM was not provided. | none | Answer Q-002. |
| P-07 | KSI-IAM-APM | not reviewed | not stated | Class A mapping table in the Certification Package (FRC-CLA-MFR) | The policy review did not cover this KSI: POL-IAM was not provided. | none | Answer Q-002. |
| P-09 | KSI-SVC-SIN | not reviewed | not stated | Class A mapping table in the Certification Package (FRC-CLA-MFR) | The policy review did not cover this KSI: POL-SVC was not provided. | none | Answer Q-002. |
| P-10 | AFC-CSO-CRA | not reviewed | not stated | Class A mapping table in the Certification Package (FRC-CLA-MFR) | The inputs for this review do not include material for this rule. | none | Answer Q-003. |
| P-11 | AFC-CSO-INB | not reviewed | not stated | Class A mapping table in the Certification Package (FRC-CLA-MFR) | The inputs for this review do not include material for this rule. | none | Answer Q-003. |
| P-12 | AFC-CSO-RCV | not reviewed | not stated | Class A mapping table in the Certification Package (FRC-CLA-MFR) | The inputs for this review do not include material for this rule. | none | Answer Q-003. |
| P-13 | CCM-OCR-AVL | not reviewed | not stated | Class A mapping table in the Certification Package (FRC-CLA-MFR) | The inputs for this review do not include material for this rule. | none | Answer Q-003. |
| P-14 | CCM-OCR-NRD | not reviewed | not stated | Class A mapping table in the Certification Package (FRC-CLA-MFR) | The inputs for this review do not include material for this rule. | none | Answer Q-003. |
| P-15 | CDS-CSO-PUB | not reviewed | not stated | Class A mapping table in the Certification Package (FRC-CLA-MFR) | The inputs for this review do not include material for this rule. | none | Answer Q-003. |
| P-16 | CDS-CSO-UTC | not reviewed | not stated | Class A mapping table in the Certification Package (FRC-CLA-MFR) | The inputs for this review do not include material for this rule. | none | Answer Q-003. |
| P-17 | CDS-UTC-AAD | not reviewed | not stated | Class A mapping table in the Certification Package (FRC-CLA-MFR) | The inputs for this review do not include material for this rule. | none | Answer Q-003. |
| P-18 | FRC-CSO-JSN | not reviewed | not stated | Class A mapping table in the Certification Package (FRC-CLA-MFR) | The inputs for this review do not include material for this rule. | none | Answer Q-003. |
| P-19 | FRC-CSO-PKG | not reviewed | not stated | Class A mapping table in the Certification Package (FRC-CLA-MFR) | The inputs for this review do not include material for this rule. | none | Answer Q-003. |
| P-20 | FRC-CSO-POP | not reviewed | not stated | Class A mapping table in the Certification Package (FRC-CLA-MFR) | The inputs for this review do not include material for this rule. | none | Answer Q-003. |
| P-21 | IEC-CSO-EFR | not reviewed | not stated | Class A mapping table in the Certification Package (FRC-CLA-MFR) | The inputs for this review do not include material for this rule. | none | Answer Q-003. |
| P-22 | IVV-CSX-AIA | not reviewed | not stated | Class A mapping table in the Certification Package (FRC-CLA-MFR) | The inputs for this review do not include material for this rule. | none | Answer Q-003. |
| P-23 | SDR-CSX-KSI | not reviewed | not stated | Class A mapping table in the Certification Package (FRC-CLA-MFR) | The inputs for this review do not include material for this rule. | none | Answer Q-003. |
| P-24 | VDR-CSO-DET | not reviewed | not stated | Class A mapping table in the Certification Package (FRC-CLA-MFR) | The inputs for this review do not include material for this rule. | none | Answer Q-003. |

## Recommended and optional rules (FRC-CLA-RFR, FRC-CLA-OFR)

These are not gaps.

| ID | Rule | Force | Today | Recommendation |
|---|---|---|---|---|
| C-01 | CCM-QTR-MTG | MAY | Not reviewed: the inputs do not include material for this rule. | Decide whether to address this rule, and record the decision in decisions.json. |
| C-02 | CDS-CSO-PSM | MAY | Not reviewed: the inputs do not include material for this rule. | Decide whether to address this rule, and record the decision in decisions.json. |
| C-03 | CMU-CSO-UVM | MAY | Not reviewed: the inputs do not include material for this rule. | Decide whether to address this rule, and record the decision in decisions.json. |
| C-04 | FRC-APP-FIA | MAY | Not reviewed: the inputs do not include material for this rule. | Decide whether to address this rule, and record the decision in decisions.json. |
| C-05 | IVV-CSO-FIA | MAY | Not reviewed: the inputs do not include material for this rule. | Decide whether to address this rule, and record the decision in decisions.json. |
| C-06 | SDR-CSX-KMT | MAY | Not reviewed: the inputs do not include material for this rule. | Decide whether to address this rule, and record the decision in decisions.json. |
| C-07 | VER-TFR-IRI | MAY | Not reviewed: the inputs do not include material for this rule. | Decide whether to address this rule, and record the decision in decisions.json. |
| C-08 | VER-TFR-MRH | MAY | Not reviewed: the inputs do not include material for this rule. | Decide whether to address this rule, and record the decision in decisions.json. |
| C-09 | VER-TFR-NRI | MAY | Not reviewed: the inputs do not include material for this rule. | Decide whether to address this rule, and record the decision in decisions.json. |
| C-10 | CDS-CSO-AVR | SHOULD | Not reviewed: the inputs do not include material for this rule. | Decide whether to address this rule, and record the decision in decisions.json. |
| C-11 | CPO-CSX-CPM | SHOULD | Not reviewed: the inputs do not include material for this rule. | Decide whether to address this rule, and record the decision in decisions.json. |
| C-12 | IEC-CSO-IIR | SHOULD | The incident response plan sets initial and ongoing report targets (see the 20x-incident-reporting example). | Compare the plan with incident_timeline.py --class a and decide whether to adopt the Class A timeframes. |
| C-13 | IEC-CSO-OIR | SHOULD | The incident response plan sets initial and ongoing report targets (see the 20x-incident-reporting example). | Compare the plan with incident_timeline.py --class a and decide whether to adopt the Class A timeframes. |
| C-14 | VDR-TFR-MVX | SHOULD | Not reviewed: the inputs do not include material for this rule. | Decide whether to address this rule, and record the decision in decisions.json. |
| C-15 | VDR-TFR-PCD | SHOULD | Not reviewed: the inputs do not include material for this rule. | Decide whether to address this rule, and record the decision in decisions.json. |
| C-16 | VDR-TFR-PDD | SHOULD | Not reviewed: the inputs do not include material for this rule. | Decide whether to address this rule, and record the decision in decisions.json. |
| C-17 | VDR-TFR-PSD | SHOULD | Not reviewed: the inputs do not include material for this rule. | Decide whether to address this rule, and record the decision in decisions.json. |
| C-18 | VDR-TFR-PVR | SHOULD | Not reviewed: the inputs do not include material for this rule. | Decide whether to address this rule, and record the decision in decisions.json. |
| C-19 | VER-TFR-EVU | SHOULD | Not reviewed: the inputs do not include material for this rule. | Decide whether to address this rule, and record the decision in decisions.json. |
| C-20 | FRC-CLA-IVV | MAY | No independent verification of the package is planned in the material. | Decide whether a FedRAMP Recognized assessor should verify the package before submission. |

## Decisions for the consultant

| ID | Question | Options | Recommendation | Decision |
|---|---|---|---|---|
| DQ-001 | Which date counts as completion of the SOC 2 Type II for the 12-month window in FRC-CLA-ASF? | Report date (2026-08-14), End of the examination period (2026-06-30) | End of the examination period (2026-06-30): It gives the earlier closing date, so the plan does not depend on a reading FedRAMP may not accept. Confirm with FedRAMP before relying on the later date | open |

## Open questions

| ID | Question | Why it matters | Blocks | Answer |
|---|---|---|---|---|
| Q-001 | Does the client have supplemental compliance evidence for the SOC 2 Type II, such as the corrective action for the two exceptions? | FRC-CLA-EAM lists it where applicable | M-05 | open |
| Q-002 | Can the client provide POL-CED, POL-IAM and POL-SVC? | Four KSIs that FRC-CLA-MFR names were not reviewed without them | P-05, P-06, P-07, P-09 | open |
| Q-003 | Can the client provide its package, trust center, communication and monitoring material for the other mandatory rules? | These rules are not reviewed without it | P-10, P-11, P-12, P-13, P-14, P-15, P-16, P-17, P-18, P-19, P-20, P-21, P-22, P-23, P-24 | open |
| Q-004 | What is the planned submission date? | The 12-month window in FRC-CLA-ASF counts back from it | A-02 | open |

## SME validation

Draft: pending SME validation.

