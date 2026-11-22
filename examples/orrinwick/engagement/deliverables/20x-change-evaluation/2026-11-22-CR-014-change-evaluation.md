---
title: Change evaluation: CR-014 team chat notification channel
client: Orrinwick Labs, Inc.
class: C (CR26)
frmr_version: 2026.11.02.01 (commit 64fa769)
date: 2026-11-22
prepared_by: Claude, for A. Example
sme_validation: Draft: pending SME validation
---

# Change evaluation: CR-014 team chat notification channel

| | |
|---|---|
| Change | CR-014: Team chat notification channel |
| Proposed type | transformative |
| Decided type | open: the consultant decides |
| Planned start | 2027-02-01 |
| Planned finish | 2027-02-26 |
| Emergency | No |

## Inputs

| ID | File | Description |
|---|---|---|
| I-16 | `changes/CR-014.md` | Change request CR-014: team chat notification channel |
| I-14 | `scope/mas-record.json` | Minimum Assessment Scope record, version 0.1.0 |
| I-13 | `scope/scope-changes.json` | Scope change log, SC-001 and SC-002 |
| I-02 | `policies/POL-CNA.md` | POL-CNA Cloud-native architecture policy, version 1.0 |

## The change

Adds a fifth notification channel: messages to an agency's team chat channel through a chat messaging service run by another company (T6). Notification workers (P2) gain an outbound HTTPS connection to it. Messages carry an alert reference ID and fixed text only (PF3). Agency administrators turn the channel on and add chat channel addresses to escalation rules; addresses are stored with the routing policy (D2).

## Evaluation

| ID | Question | Answer | Evidence |
|---|---|---|---|
| EV-1 | Is the change likely to substantively affect the security posture? (FRD-SGC) | Yes. It adds a third-party service in the alert delivery path (T6), a new outbound flow from the notification workers (P2), and a new kind of address stored with the routing policy (D2). Each of these changes the scope record. | I-16 What changes; I-14 P2; D2; PF3; third_party_resources; FRD-SGC; SCN-CSO-EVA |
| EV-2 | Is it likely to change the certification class? (FRD-CCC) | No. The request adds no new data class and describes no change to impact levels. | I-16 What changes; FRD-CCC |
| EV-3 | Does it recur routinely as part of ongoing operations? (FRD-RTR) | No. It is the first chat channel, and the change log has no earlier change of this kind. | I-16 What changes; I-13 entries; FRD-RTR |
| EV-4 | Does it introduce substantive risks that must be assessed in depth? (FRD-TRF) | Proposed yes, for the SME to confirm. The change adds a capability agencies configure and use, and a new third party that needs the MAS-CSO-TPR documentation. Against that, messages follow the existing payload policy (PF3), which could make it adaptive if the SME judges that existing checks verify it with minor changes. See DQ-001. | I-16 What changes; I-14 PF3; FRD-TRF; FRD-ADP; MAS-CSO-TPR |

## Notices

Business days: Monday to Friday, skipping US federal holidays on their observed dates (5 U.S.C. 6103) (FedRAMP does not define business days; confirm with the consultant).

| Rule | Name | Counts from | Timeframe | Date | Meaning |
|---|---|---|---|---|---|
| SCN-TRF-NIP | Notification of Initial Plans | start | 30 bizdays before | 2026-12-16 | send on or before |
| SCN-TRF-NFP | Notification of Final Plans | start | 10 bizdays before | 2027-01-15 | send on or before |
| SCN-TRF-NAF | Notification After Finishing | finish | 5 bizdays after | 2027-03-05 | latest date to send |
| SCN-TRF-NAV | Notification After Verification | verified | 5 bizdays after | not stated | needs the verified date |
| SCN-TRF-UPD | Update Documentation | finish | 30 bizdays after | 2027-04-09 | latest date to send |

Read SCN-TRF-TPR (third-party review before starting) and SCN-CSO-INF (required content).

## Notice content (SCN-CSO-INF)

| ID | Item | Supplied by the inputs | Sources |
|---|---|---|---|
| NC-01 | Service Offering FedRAMP ID | No: not in the inputs | I-16 whole request; SCN-CSO-INF |
| NC-02 | Assessor Name (if applicable) | No: no assessor is named | I-16 whole request; SCN-CSO-INF |
| NC-03 | Related Vulnerability (if applicable) | None stated | I-16 whole request; SCN-CSO-INF |
| NC-04 | Significant Change type and explanation of categorization | Yes, once DQ-001 is decided: EV-1 to EV-4 | I-16 whole request; SCN-CSO-INF |
| NC-05 | Short description of change | Yes: CR-014 What changes | I-16 whole request; SCN-CSO-INF |
| NC-06 | Reason for change | Yes: CR-014 Why | I-16 whole request; SCN-CSO-INF |
| NC-07 | Summary of customer impact, including changes to services and customer configuration responsibilities | Partly: agency administrators turn the channel on and add addresses; who is responsible for the chat channel's own settings is not stated | I-16 whole request; SCN-CSO-INF |
| NC-08 | Plan and timeline for the change, including for the verification, assessment, and/or validation of impacted Key Security Indicators or Rev5 Controls | Partly: dates and testing are stated; the impacted KSIs are not identified | I-16 whole request; SCN-CSO-INF |
| NC-09 | Copy of the business or security impact analysis | No: not provided | I-16 whole request; SCN-CSO-INF |
| NC-10 | Name and title of approver | No: the requester is named, the approver is not | I-16 whole request; SCN-CSO-INF |

## Scope log entry and client review

### SL-1 Draft scope change log entry

| | |
|---|---|
| Id | SC-003 (draft, not yet in the log) |
| Date | 2027-02-26 (planned finish) |
| Change type | added |
| Resources | T6, P2 |
| Scn category | transformative (proposed, DQ-001) |
| Summary | Team chat notification channel through a new third-party chat messaging service (T6), with a new outbound flow from P2 and chat channel addresses stored with the routing policy (D2). |
| Evaluation | EV-1 to EV-4 in this deliverable |
| Needs before entry | T6 entry with the MAS-CSO-TPR information (Q-004), new flow ID, consultant decision on the type |
| Sources | I-16 What changes; I-13 entry format; SCN-CSO-MAR |

### CRV-1 Protection review under POL-CNA CNA-7b

| | |
|---|---|
| Requirement | CNA-7b, transformative: before the change starts, and again within 5 business days after it is finished |
| Before start | before 2027-02-01 |
| After finish | by 2027-03-05 |
| Owner | Platform Lead (CNA-7b) |
| Note | The policy review recommended moving the pre-change review before the final plans notice (R-007). If the client adopts it, the pre-change review is due before the SCN-TRF-NFP date in the notices table |
| Sources | I-02 CNA-7b; KSI-CNA-RVP |

## Decisions for the consultant

| ID | Question | Options | Recommendation | Decision |
|---|---|---|---|---|
| DQ-001 | Is CR-014 transformative or adaptive? | Transformative, Adaptive | Transformative: It adds a capability agencies configure and a new third party in the delivery path, which needs new MAS-CSO-TPR documentation and an assessment of the new flow. Choosing adaptive drops the 30 and 10 business day notices before the start | open |
| DQ-002 | Confirm the business day basis: Monday to Friday, skipping US federal holidays. | Confirm the default, Also skip the client's own holidays (client supplies the dates), Monday to Friday only | Confirm the default: FedRAMP does not define business days. Counting weekdays only would put the final plans notice on 2027-01-18, the Martin Luther King Jr. federal holiday; the default moves it to 2027-01-15 | open |

## Open questions

| ID | Question | Why it matters | Blocks | Answer |
|---|---|---|---|---|
| Q-001 | Are the two pilot agencies using the offering, and what is the offering's FedRAMP ID? | All necessary parties include any agency using the offering (FRD-ANP). The change log recorded on 2026-11-19 that no agency was relying on it | NC-01 | open |
| Q-002 | Who approves CR-014 (name and title)? | SCN-CSO-INF requires it in the notice | NC-10 | open |
| Q-003 | Is there a security impact analysis for CR-014? | SCN-CSO-INF requires a copy | NC-09 | open |
| Q-004 | Which chat messaging service is T6, and what are its usage and configuration, justification, mitigation measures and compensating controls? | MAS-CSO-TPR requires them before the scope log entry | SL-1 | open |
| Q-005 | Which KSIs does the change affect, and how will they be validated? | SCN-CSO-INF requires the plan for validating impacted KSIs. The SME identifies them from the change and the validator designs | NC-08 | open |

## SME validation

Draft: pending SME validation.

