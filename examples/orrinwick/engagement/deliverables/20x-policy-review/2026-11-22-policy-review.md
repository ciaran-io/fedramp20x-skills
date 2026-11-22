---
title: KSI policy coverage review
client: Orrinwick Labs, Inc.
class: C (CR26)
frmr_version: 2026.11.02.01 (commit 64fa769)
date: 2026-11-22
prepared_by: Claude, for A. Example
sme_validation: Draft: pending SME validation
---

# KSI policy coverage review

## Basis

| | |
|---|---|
| Policies reviewed | POL-INR Incident response policy, version 1.1 (I-01); POL-CNA Cloud-native architecture policy, version 1.0 (I-02); POL-RPL Recovery planning policy, version 1.2 (I-03); POL-CMT Change management policy, version 1.0 (I-04) |
| Documents referenced but not provided | Incident response plan (INR-1), Recovery plan (RPL-3), POL-IAM and POL-SVC (referenced by CNA-1), Scope record mas/mas-record.json (CNA-1, CNA-4, CNA-6), Security decision record (exception process) |
| KSIs at Class C | 46 |
| Coverage | 2 covered, 17 partial, 0 not covered, 27 not reviewed |
| Gaps | 0 High, 7 Moderate, 5 Low, 2 Observation |
| SME validation | Draft: pending SME validation |

This review reports what the policies state. It does not assess evidence, and it does not state whether the client is compliant.

## Coverage matrix

| KSI | Name | Requirements | Coverage | Gaps | Note |
|---|---|---|---|---|---|
| KSI-CED-RAT | Reviewing All Training | none | not reviewed | none | POL-CED was not provided |
| KSI-CMT-LMC | Logging Changes | POL-CMT/CMT-1, POL-CMT/CMT-5, POL-CMT/CMT-6 | partial | G-006 | Logging stated; monitoring not stated |
| KSI-CMT-RMV | Redeploying vs Modifying | POL-CMT/CMT-2 | partial | G-008 | Covered in substance; actor pending DQ-001 |
| KSI-CMT-RVP | Reviewing Change Procedures | POL-CMT/CMT-3 | covered | G-014 | Owner, yearly and failed-change cycle, and record location stated |
| KSI-CMT-VTD | Validating Throughout Deployment | POL-CMT/CMT-4 | partial | G-008, G-009 | Every deployment; actor and record location not stated |
| KSI-CNA-DFP | Defining Functionality and Privileges | POL-CNA/CNA-1 | partial | G-008 | Covered in substance; actor pending DQ-001 |
| KSI-CNA-EIS | Enforcing Intended State | POL-CNA/CNA-2 | partial | G-002, G-003, G-008 | No review cycle; no automated enforcement |
| KSI-CNA-IBP | Implementing Best Practices | POL-CNA/CNA-3 | partial | G-008, G-009 | Cycle stated; actor and record location not stated |
| KSI-CNA-MAT | Minimizing Attack Surface | POL-CNA/CNA-4 | partial | G-002, G-004, G-008 | No review cycle; lateral movement not addressed |
| KSI-CNA-OFA | Optimizing for Availability | POL-CNA/CNA-5 | partial | G-002, G-008 | No review cycle |
| KSI-CNA-RNT | Restricting Network Traffic | POL-CNA/CNA-6 | partial | G-002, G-008 | No review cycle |
| KSI-CNA-RVP | Reviewing Protections | POL-CNA/CNA-7a, POL-CNA/CNA-7b | partial | G-009, G-011 | Owner, cycle and change deadlines stated; record location not stated |
| KSI-CNA-ULN | Using Logical Networking | POL-CNA/CNA-8 | partial | G-002, G-008 | No review cycle |
| KSI-IAM-AAM | Automating Account Management | none | not reviewed | none | POL-IAM was not provided |
| KSI-IAM-APM | Adopting Passwordless Methods | none | not reviewed | none | POL-IAM was not provided |
| KSI-IAM-ELP | Ensuring Least Privilege | none | not reviewed | none | POL-IAM was not provided |
| KSI-IAM-JIT | Authorizing Just-in-Time | none | not reviewed | none | POL-IAM was not provided |
| KSI-IAM-SNU | Securing Non-User Authentication | none | not reviewed | none | POL-IAM was not provided |
| KSI-IAM-SUS | Responding to Suspicious Activity | none | not reviewed | none | POL-IAM was not provided |
| KSI-INR-AAR | Generating After Action Reports | POL-INR/INR-2 | partial | G-001, G-008 | Reports are required; incorporating lessons is not |
| KSI-INR-RIR | Reviewing Incident Response Procedures | POL-INR/INR-1, POL-INR/INR-3 | partial | G-008, G-009 | Owner and cycle stated; record location not stated |
| KSI-INR-RPI | Reviewing Past Incidents | POL-INR/INR-4 | partial | G-010, G-009 | Cycle stated; owner is a team; record location not stated |
| KSI-MLA-ALA | Authorizing Log Access | none | not reviewed | none | POL-MLA was not provided |
| KSI-MLA-EVC | Evaluating Configurations | none | not reviewed | none | POL-MLA was not provided |
| KSI-MLA-LET | Logging Event Types | none | not reviewed | none | POL-MLA was not provided |
| KSI-MLA-OSM | Operating SIEM Capability | none | not reviewed | none | POL-MLA was not provided |
| KSI-MLA-RVL | Reviewing Logs | none | not reviewed | none | POL-MLA was not provided |
| KSI-PIY-GIV | Generating Inventories | none | not reviewed | none | POL-PIY was not provided |
| KSI-PIY-RES | Reviewing Executive Support | none | not reviewed | none | POL-PIY was not provided |
| KSI-PIY-RIS | Reviewing Investments in Security | none | not reviewed | none | POL-PIY was not provided |
| KSI-PIY-RSD | Reviewing Security in the SDLC | none | not reviewed | none | POL-PIY was not provided |
| KSI-PIY-RVD | Reviewing Vulnerability Disclosures | none | not reviewed | none | POL-PIY was not provided |
| KSI-RPL-ABO | Aligning Backups with Objectives | POL-RPL/RPL-2 | partial | G-008, G-009 | Cycle stated; acknowledging role and record location not stated |
| KSI-RPL-ARP | Aligning Recovery Plan | POL-RPL/RPL-3, POL-RPL/RPL-5 | partial | G-005, G-008, G-013 | No review against the objectives |
| KSI-RPL-RRO | Reviewing Recovery Objectives | POL-RPL/RPL-1 | covered | none | Owner, 90-day cycle and record location stated |
| KSI-RPL-TRC | Testing Recovery Capabilities | POL-RPL/RPL-4 | partial | G-012, G-008, G-009 | Six-month cycle stated; no comparison with the objectives |
| KSI-SCR-MIT | Mitigating Supply Chain Risk | none | not reviewed | none | POL-SCR was not provided |
| KSI-SCR-MON | Monitoring Supply Chain Risk | none | not reviewed | none | POL-SCR was not provided |
| KSI-SVC-ACM | Automating Configuration Management | none | not reviewed | none | POL-SVC was not provided |
| KSI-SVC-ASM | Automating Secret Management | none | not reviewed | none | POL-SVC was not provided |
| KSI-SVC-EIS | Evaluating and Improving Security | none | not reviewed | none | POL-SVC was not provided |
| KSI-SVC-PRR | Preventing Residual Risk | none | not reviewed | none | POL-SVC was not provided |
| KSI-SVC-RUD | Removing Unwanted Data | none | not reviewed | none | POL-SVC was not provided |
| KSI-SVC-SIN | Securing Information | none | not reviewed | none | POL-SVC was not provided |
| KSI-SVC-VCM | Validating Communications | none | not reviewed | none | POL-SVC was not provided |
| KSI-SVC-VRI | Validating Resource Integrity | none | not reviewed | none | POL-SVC was not provided |

## Gaps

### G-001 Lessons learned have no cycle, owner or record

| | |
|---|---|
| Requirement | POL-INR/INR-2 |
| Test | T2 Cycle; T7 Mapping |
| Criteria | KSI-INR-AAR, FRD-PER, POL-INR/INR-2 |
| Rating | Moderate |
| Observation | INR-2 requires an after action report within 10 business days. KSI-INR-AAR has a second part: lessons learned are persistently incorporated. INR-3 covers lessons that change the incident response plan. No requirement covers lessons that change anything else, and none states who tracks them, how often, or where. |
| Recommendation | Add a sentence to INR-2 that records each lesson as an action with an owner and a due date, and reviews open actions in the quarterly review under INR-4. |
| Rewrite | R-001 |
| Sources | I-01 INR-2; I-01 INR-3; I-01 INR-4; KSI-INR-AAR; FRD-PER |
| Confirmed | yes |

### G-002 Five CNA KSIs have no stated review cycle

| | |
|---|---|
| Requirement | POL-CNA/CNA-2, CNA-4, CNA-5, CNA-6, CNA-8 |
| Test | T2 Cycle |
| Criteria | KSI-CNA-EIS, KSI-CNA-MAT, KSI-CNA-OFA, KSI-CNA-RNT, KSI-CNA-ULN, FRD-PER, VDR-TFR-MVX |
| Rating | Moderate |
| Observation | Each of these KSIs requires that the resources are persistently reviewed or assessed. CNA-2, CNA-4, CNA-5, CNA-6 and CNA-8 state the configuration rule but no cycle for reviewing it, no owner of the review and no record. CNA-3 is the only CNA requirement that states a cycle (every validation run, and at least every 3 days). |
| Recommendation | Add one requirement that applies the CNA-3 cycle to the configuration rules in CNA-2, CNA-4, CNA-5, CNA-6 and CNA-8 (decision DQ-002). |
| Rewrite | R-002 |
| Sources | I-02 CNA-2; I-02 CNA-3; I-02 CNA-4; I-02 CNA-5; I-02 CNA-6; I-02 CNA-8; KSI-CNA-EIS; KSI-CNA-MAT; KSI-CNA-OFA; KSI-CNA-RNT; KSI-CNA-ULN; FRD-PER; VDR-TFR-MVX; DQ-002 |
| Confirmed | yes |

### G-003 Intended state is not enforced automatically

| | |
|---|---|
| Requirement | POL-CNA/CNA-2 |
| Test | T7 Mapping |
| Criteria | KSI-CNA-EIS, POL-CNA/CNA-2 |
| Rating | Moderate |
| Observation | KSI-CNA-EIS requires automated services that assess machine-based resources and enforce their intended state automatically. CNA-2 treats a resource outside the code as a defect to be removed or brought into code within 5 business days. It names no automated assessment and allows the correction to be manual. |
| Recommendation | State the automated service that detects drift and restores the declared state, and keep the 5 business day limit for differences it cannot restore. The tool must come from the client (Q-007). |
| Rewrite | R-003 |
| Sources | I-02 CNA-2; KSI-CNA-EIS |
| Confirmed | yes |

### G-004 Lateral movement is not addressed

| | |
|---|---|
| Requirement | POL-CNA/CNA-4 |
| Test | T7 Mapping |
| Criteria | KSI-CNA-MAT, POL-CNA/CNA-4 |
| Rating | Moderate |
| Observation | KSI-CNA-MAT has two parts: a minimal attack surface, and minimal lateral movement if a resource is compromised. CNA-4 limits public exposure. No requirement mapped to KSI-CNA-MAT addresses lateral movement. CNA-8 separates tenants' workloads from operations tooling and other trust zones, which may be meant to cover it, but it is mapped only to KSI-CNA-ULN. |
| Recommendation | If CNA-8 is meant to limit lateral movement, map it to KSI-CNA-MAT and say so in the text. Otherwise add a requirement. Confirm with the client (Q-005). |
| Rewrite | none |
| Sources | I-02 CNA-4; I-02 CNA-8; KSI-CNA-MAT |
| Confirmed | no, see open questions |

### G-005 Recovery plan is not reviewed against the objectives

| | |
|---|---|
| Requirement | POL-RPL/RPL-3 |
| Test | T2 Cycle; T7 Mapping |
| Criteria | KSI-RPL-ARP, FRD-PER, POL-RPL/RPL-3 |
| Rating | Moderate |
| Observation | KSI-RPL-ARP requires that the alignment of the recovery plan with the recovery objectives is persistently reviewed. RPL-3 says the plan is kept in step with the architecture. It does not require a review against the RTO and RPO in RPL-1, and names no owner, cycle or record. |
| Recommendation | Add a review of the recovery plan against RPL-1, with an owner, a cycle and a record location the client sets. |
| Rewrite | R-004 |
| Sources | I-03 RPL-1; I-03 RPL-3; KSI-RPL-ARP; FRD-PER |
| Confirmed | yes |

### G-006 Change logs are kept but monitoring is not stated

| | |
|---|---|
| Requirement | POL-CMT/CMT-1 |
| Test | T7 Mapping |
| Criteria | KSI-CMT-LMC, POL-CMT/CMT-1 |
| Rating | Moderate |
| Observation | KSI-CMT-LMC requires that changes are logged and monitored. CMT-1 requires the pipeline to log each change. No requirement in POL-CMT states that anyone monitors the log, how often, or what happens when a change did not follow CMT-1 to CMT-6. |
| Recommendation | Add who monitors the change log, how often, and where the review is recorded (Q-008). |
| Rewrite | R-005 |
| Sources | I-04 CMT-1; I-04 CMT-6; KSI-CMT-LMC |
| Confirmed | yes |

### G-010 Past incident review is owned by a team

| | |
|---|---|
| Requirement | POL-INR/INR-4 |
| Test | T1 Owner; T4 Reviewer |
| Criteria | KSI-INR-RPI, POL-INR/INR-4 |
| Rating | Moderate |
| Observation | INR-4 assigns the quarterly review of past incidents to the security team. A check that compares the reviewer with the policy needs one accountable role. INR-3 names the CISO for the plan review. |
| Recommendation | Name the role that runs and records the quarterly review (Q-006). |
| Rewrite | R-006 |
| Sources | I-01 INR-3; I-01 INR-4; KSI-INR-RPI |
| Confirmed | yes |

### G-007 CMT-7 cites rules that apply to Rev5 only

| | |
|---|---|
| Requirement | POL-CMT/CMT-7 |
| Test | T8 Rule IDs |
| Criteria | FRC-CCL-UCC, FRC-CCL-DCC, SCN-CSO-EVA |
| Rating | Low |
| Observation | CMT-7 cites FRC-CCL-UCC and FRC-CCL-DCC. In FRMR 2026.11.02.01 these rules sit in the FRC-CCL subset, which applies to Rev5 only. For 20x, the evaluation steps listed under SCN-CSO-EVA say that a change of certification class needs a new assessment and is not handled under the significant change rules. CMT-7 states the same in substance, so only the citation is wrong. |
| Recommendation | Cite SCN-CSO-EVA in CMT-7 in place of FRC-CCL-UCC and FRC-CCL-DCC. |
| Rewrite | R-009 |
| Sources | I-04 CMT-7; FRC-CCL-UCC; FRC-CCL-DCC; SCN-CSO-EVA |
| Confirmed | yes |

### G-008 Eighteen requirements name no actor

| | |
|---|---|
| Requirement | INR-1, INR-2, CNA-1 to CNA-6, CNA-8, RPL-2 to RPL-5, CMT-1, CMT-2, CMT-4, CMT-6, CMT-7 |
| Test | T1 Owner |
| Criteria | FRD-PER |
| Rating | Low |
| Observation | Each policy names an owner in its header (CISO for POL-INR, Platform Lead for the others). The listed requirements name no role that does the activity. RPL-2 says a failed job alert is acknowledged by a named person but does not say which role. Whether the header owner owns these requirements is not stated. |
| Recommendation | If the header owner owns every requirement that names no actor, say so once in each policy (decision DQ-001). Name the role that acknowledges RPL-2 alerts. |
| Rewrite | none |
| Sources | I-01 INR-1; I-01 INR-2; I-02 CNA-1; I-03 RPL-2; I-03 RPL-3; I-04 CMT-2; FRD-PER; DQ-001 |
| Confirmed | no, see open questions |

### G-009 Review and test records have no stated location

| | |
|---|---|
| Requirement | INR-3, INR-4, CNA-3, CNA-7a, CNA-7b, RPL-2, RPL-4, CMT-4 |
| Test | T3 Record |
| Criteria | FRD-PER, VDR-TFR-NMV |
| Rating | Low |
| Observation | These requirements set a cycle but do not say where its record is kept. RPL-1 and CMT-3 do state a record location. A check cannot confirm the status of a cycle without a known record. |
| Recommendation | State the record location in each requirement (decision DQ-003). |
| Rewrite | none |
| Sources | I-01 INR-3; I-01 INR-4; I-02 CNA-3; I-02 CNA-7a; I-02 CNA-7b; I-03 RPL-2; I-03 RPL-4; I-04 CMT-4; I-03 RPL-1; I-04 CMT-3; FRD-PER; VDR-TFR-NMV; DQ-003 |
| Confirmed | yes |

### G-011 Transformative change review may come after the notices

| | |
|---|---|
| Requirement | POL-CNA/CNA-7b |
| Test | T5 Change deadline |
| Criteria | KSI-CNA-RVP, SCN-TRF-NIP, SCN-TRF-NFP, POL-CNA/CNA-7b |
| Rating | Low |
| Observation | CNA-7b requires a review of protections before a transformative change starts. SCN-TRF-NIP and SCN-TRF-NFP require notices of initial and final plans 30 and 10 business days before the change starts. A review held just before the start meets CNA-7b but cannot inform those notices. |
| Recommendation | Set the pre-change review before the final plans notice under SCN-TRF-NFP. |
| Rewrite | R-007 |
| Sources | I-02 CNA-7b; KSI-CNA-RVP; SCN-TRF-NIP; SCN-TRF-NFP |
| Confirmed | yes |

### G-012 Restore test results are not compared with the objectives

| | |
|---|---|
| Requirement | POL-RPL/RPL-4 |
| Test | T7 Mapping |
| Criteria | KSI-RPL-TRC, POL-RPL/RPL-4 |
| Rating | Low |
| Observation | KSI-RPL-TRC requires recovery testing aligned with the recovery objectives. RPL-4 records the time taken and the data age restored, but does not require a comparison with the RTO and RPO in RPL-1 or say what happens when a result falls outside them. |
| Recommendation | Require the comparison with RPL-1 and record a result outside an objective as a finding. |
| Rewrite | R-008 |
| Sources | I-03 RPL-1; I-03 RPL-4; KSI-RPL-TRC |
| Confirmed | yes |

### G-013 RPL-5 is mapped to plan alignment but is a scope rule

| | |
|---|---|
| Requirement | POL-RPL/RPL-5 |
| Test | T7 Mapping |
| Criteria | KSI-RPL-ARP, MAS-CSO-IIR |
| Rating | Observation |
| Observation | RPL-5 places the recovery environment under the same scope record and controls as production. That is a scope requirement. It does not address the review of plan alignment that KSI-RPL-ARP requires. RPL-3 is the requirement that maps to KSI-RPL-ARP. |
| Recommendation | Keep RPL-5, and map it to the scope record rather than to KSI-RPL-ARP. |
| Rewrite | none |
| Sources | I-03 RPL-3; I-03 RPL-5; KSI-RPL-ARP; MAS-CSO-IIR |
| Confirmed | yes |

### G-014 CMT-5 is mapped to procedure review but covers notices

| | |
|---|---|
| Requirement | POL-CMT/CMT-5 |
| Test | T7 Mapping |
| Criteria | KSI-CMT-RVP |
| Rating | Observation |
| Observation | CMT-5 is mapped to KSI-CMT-RVP. It covers the significant change log and notices, not the review of the change procedure. CMT-3 covers KSI-CMT-RVP. |
| Recommendation | Remove KSI-CMT-RVP from the CMT-5 mapping. |
| Rewrite | none |
| Sources | I-04 CMT-3; I-04 CMT-5; KSI-CMT-RVP |
| Confirmed | yes |

## Rewritten requirements

| ID | Requirement | Current text | Recommended text | Closes |
|---|---|---|---|---|
| R-001 | POL-INR/INR-2 | Each FedRAMP Reportable Incident, and each incident rated N2 or above, ends with an after action report within 10 business days. A reportable incident with no rating is treated as N5 (IEC-CSO-DPR). | Each FedRAMP Reportable Incident, and each incident rated N2 or above, ends with an after action report within 10 business days. A reportable incident with no rating is treated as N5 (IEC-CSO-DPR). [owner: client to confirm] records each lesson learned as an action with an owner and a due date in [record: client to confirm]. The quarterly review under INR-4 checks the open actions. | G-001 |
| R-002 | POL-CNA/CNA-9 (new) | None | The Platform Lead's automated validation checks the configuration that CNA-2, CNA-4, CNA-5, CNA-6 and CNA-8 require on every validation run, and at least every 3 days. Each run's result is kept in [record: client to confirm]. A failed check is fixed or accepted as an exception under the policy exception process. | G-002 |
| R-003 | POL-CNA/CNA-2 | Infrastructure is declared in code. A resource that exists outside the code is a defect and is removed or brought into the code within 5 business days. | Infrastructure is declared in code. [tool: client to confirm] compares the running state with the code on every validation run, and at least every 3 days, and restores the declared state automatically. A difference it cannot restore is a defect and is removed or brought into the code within 5 business days. | G-003 |
| R-004 | POL-RPL/RPL-3 | The recovery plan describes how a recovery environment is built from infrastructure code and how data is restored into it. It is kept in step with the architecture. | The recovery plan describes how a recovery environment is built from infrastructure code and how data is restored into it. It is kept in step with the architecture. [owner: client to confirm] reviews the plan against the recovery objectives in RPL-1 [cadence: client to confirm] and after each restore test under RPL-4, and records the review in [record: client to confirm]. | G-005 |
| R-005 | POL-CMT/CMT-1 | Every change to a production resource is made through the pipeline. The pipeline logs the change, the author, the reviewer and the result. | Every change to a production resource is made through the pipeline. The pipeline logs the change, the author, the reviewer and the result. [owner: client to confirm] reviews the pipeline log [cadence: client to confirm] for changes that did not follow CMT-1 to CMT-6, and records the review in [record: client to confirm]. | G-006 |
| R-006 | POL-INR/INR-4 | The security team reviews all past incidents and near misses, of any rating, every quarter for repeated causes. The review lists the incidents it covered and records its findings. | [owner: client to confirm] reviews all past incidents and near misses, of any rating, every quarter for repeated causes. The review lists the incidents it covered and records its findings. The review is recorded in [record: client to confirm]. | G-010, G-009 |
| R-007 | POL-CNA/CNA-7b | The Platform Lead also reviews protections after each change recorded in mas/scope-changes.json. The deadline depends on the change type in the SCN rules. Transformative: before the change starts, and again within 5 business days after it is finished. Adaptive: within 10 business days after the change is finished, before the notice under SCN-ADP-NTF. Not significant: within 20 business days after the change is finished. Routine recurring: no separate review, because the annual review covers these changes. | The Platform Lead also reviews protections after each change recorded in mas/scope-changes.json. The deadline depends on the change type in the SCN rules. Transformative: before the notice of final plans under SCN-TRF-NFP, and again within 5 business days after it is finished. Adaptive: within 10 business days after the change is finished, before the notice under SCN-ADP-NTF. Not significant: within 20 business days after the change is finished. Routine recurring: no separate review, because the annual review covers these changes. | G-011 |
| R-009 | POL-CMT/CMT-7 | A change of certification class is not a significant change. It needs a new certification before the offering operates at the new class (FRC-CCL-UCC, FRC-CCL-DCC). | A change of certification class is not a significant change. It needs a new certification before the offering operates at the new class (SCN-CSO-EVA). | G-007 |
| R-008 | POL-RPL/RPL-4 | A restore test runs at least every 6 months. It records the time taken, the data age restored and any failure. | A restore test runs at least every 6 months. It records the time taken, the data age restored and any failure. The results are compared with the recovery objectives in RPL-1. A result outside an objective is recorded as a finding in [record: client to confirm]. | G-012 |

## Decisions for the consultant

| ID | Question | Options | Recommendation | Decision |
|---|---|---|---|---|
| DQ-001 | Does the policy header owner own every requirement that names no actor? | Yes: add one sentence to each policy saying so, No: name the actor in each requirement, Mixed: name the actor where it differs from the header owner | Mixed: name the actor where it differs from the header owner: It closes G-008 with the fewest changes and still names a different actor where one exists, such as the GRC Lead in CMT-5 | open |
| DQ-002 | How should the review cycle for KSI-CNA-EIS, MAT, OFA, RNT and ULN be stated? | One new requirement (CNA-9) that applies the CNA-3 cycle to all five, Add the cycle to each of CNA-2, CNA-4, CNA-5, CNA-6 and CNA-8 | One new requirement (CNA-9) that applies the CNA-3 cycle to all five: One requirement gives one record and one check, and uses a cycle the client already states in CNA-3 | open |
| DQ-003 | Where should review and test records be kept for the requirements in G-009? | The same records as RPL-1 and CMT-3 (environment/recovery-objectives.json and environment/grc-records.json), A location the client names for each requirement | The same records as RPL-1 and CMT-3 (environment/recovery-objectives.json and environment/grc-records.json): The client already uses these records for two review cycles, so a check can read every cycle from the same place | open |

## Open questions

| ID | Question | Why it matters | Blocks | Answer |
|---|---|---|---|---|
| Q-001 | Can the client provide the incident response plan? | INR-1 depends on the plan defining roles, evaluation steps and timelines. Test T6 cannot be applied without it | none | open |
| Q-002 | Can the client provide the recovery plan? | G-005 and test T6 for RPL-3 depend on what the plan contains | G-005 | open |
| Q-003 | Can the client provide POL-CED, POL-IAM, POL-MLA, POL-PIY, POL-SCR and POL-SVC, and the scope record? | 27 KSIs are not reviewed without them, and CNA-1, CNA-4 and CNA-6 refer to them | none | open |
| Q-005 | Is CNA-8 meant to limit lateral movement for KSI-CNA-MAT? | Decides whether G-004 needs a new requirement or a change of mapping | G-004 | open |
| Q-006 | Which role runs and records the quarterly past incident review in INR-4? | A check compares the reviewer with the role the policy names | G-010 | open |
| Q-007 | Which service detects drift and restores the declared state? | R-003 names it; it cannot be assumed | G-003 | open |
| Q-008 | Who reviews the pipeline log, how often, and where is the review recorded? | R-005 needs all three | G-006 | open |

## Requirement inventory

| Requirement | Owner | Cadence or deadline | Record location | KSIs (client mapping) |
|---|---|---|---|---|
| POL-INR / INR-1 | not stated | not stated | not stated | KSI-INR-RIR |
| POL-INR / INR-2 | not stated | within 10 business days | not stated | KSI-INR-AAR |
| POL-INR / INR-3 | CISO | each year, and when an after action report or a quarterly incident review finds that the plan needs to change | not stated | KSI-INR-RIR, KSI-INR-RPI |
| POL-INR / INR-4 | The security team | every quarter | not stated | KSI-INR-RPI |
| POL-CNA / CNA-1 | not stated | permissions unused for 90 days are removed | not stated | KSI-CNA-DFP |
| POL-CNA / CNA-2 | not stated | within 5 business days (drift removal) | not stated | KSI-CNA-EIS |
| POL-CNA / CNA-3 | not stated | on every validation run, and at least every 3 days | not stated | KSI-CNA-IBP |
| POL-CNA / CNA-4 | not stated | not stated | scope record (justification of each open port and endpoint) | KSI-CNA-MAT |
| POL-CNA / CNA-5 | not stated | not stated | not stated | KSI-CNA-OFA |
| POL-CNA / CNA-6 | not stated | not stated | not stated | KSI-CNA-RNT |
| POL-CNA / CNA-7a | Platform Lead | at least once a year | not stated | KSI-CNA-RVP |
| POL-CNA / CNA-7b | Platform Lead | deadline by SCN change type after each change in mas/scope-changes.json | not stated | KSI-CNA-RVP |
| POL-CNA / CNA-8 | not stated | not stated | not stated | KSI-CNA-ULN |
| POL-RPL / RPL-1 | Platform Lead | at least every 90 days | environment/recovery-objectives.json | KSI-RPL-RRO |
| POL-RPL / RPL-2 | a named person (alert acknowledgement) | backups at least every 2 hours; jobs monitored every day; alert within 60 minutes | not stated | KSI-RPL-ABO |
| POL-RPL / RPL-3 | not stated | not stated | not stated | KSI-RPL-ARP |
| POL-RPL / RPL-4 | not stated | at least every 6 months | not stated | KSI-RPL-TRC |
| POL-RPL / RPL-5 | not stated | not stated | not stated | KSI-RPL-ARP |
| POL-CMT / CMT-1 | not stated | every change | pipeline log | KSI-CMT-LMC |
| POL-CMT / CMT-2 | not stated | not stated | not stated | KSI-CMT-RMV |
| POL-CMT / CMT-3 | Platform Lead | each year, and within 10 business days after any failed or emergency change | environment/grc-records.json | KSI-CMT-RVP |
| POL-CMT / CMT-4 | not stated | every deployment | not stated | KSI-CMT-VTD |
| POL-CMT / CMT-5 | GRC Lead (notice) | within the rule timeline (SCN rules) | significant change log | KSI-CMT-LMC, KSI-CMT-RVP |
| POL-CMT / CMT-6 | not stated | before release | pipeline log; mas/scope-changes.json for scope changes | KSI-CMT-LMC |
| POL-CMT / CMT-7 | not stated | not stated | not stated | none |

## SME validation

Draft: pending SME validation.
