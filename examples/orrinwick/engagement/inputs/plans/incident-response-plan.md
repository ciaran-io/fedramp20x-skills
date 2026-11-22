# Incident Response Plan

> FICTIONAL DEMO DOCUMENT. Orrinwick Labs, Inc. is invented. Nothing here is a real security record or FedRAMP certification.

| | |
|---|---|
| Owner | CISO (fictional) |
| Version | 1.0, approved by the CISO on 2026-11-21 |
| Last reviewed | 2026-11-21, by the CISO, when version 1.0 was approved (recorded in `environment/grc-records.json`) |
| Rules | `IEC-CSO-*`, `VER-TFR-IRI`, `VER-TFR-NRI` in `rules-matrix.md` |
| KSIs | KSI-INR-AAR, KSI-INR-RIR, KSI-INR-RPI |
| Policy | `POL-INR` |

## Scope

This plan applies to every incident that affects, or could affect, an information resource marked in scope in `mas/mas-record.json`, including incidents at the third parties listed there. An incident has the meaning given in 44 USC 3552(b)(2): an occurrence that actually or imminently jeopardizes the integrity, confidentiality or availability of information or an information system without lawful authority, or that violates or threatens to violate law, security policy or acceptable use policy.

The IEC rules require prompt and responsible evaluation and notification, and they do not set fixed hours. The times in this plan are Orrinwick's own targets. Missing a target is recorded in the incident record and reviewed in the after action report.

## 1. Roles and contacts

| Role | Held by | Responsibilities |
|---|---|---|
| On-call responder | Security Operations rota | Acknowledges an alert within 15 minutes, opens the incident record and starts the evaluation |
| Incident lead | Security Operations Lead, or the on-call responder until the lead joins | Runs the response, records the timeline, decides containment steps with the Platform Lead |
| Federal incident response coordinator | CISO | Decides FedRAMP reportability, approves the Potential Agency Impact N-rating, approves every report sent to agencies and FedRAMP, and is the named contact in each report |
| FedRAMP and agency communications | GRC Lead | Prepares the initial, ongoing and final incident reports, keeps the list of affected agencies, files the reports in the incident record |
| Technical recovery | Platform Lead | Containment, eradication and recovery of affected resources, including a restore under the recovery plan (POL-RPL, SD-003) |
| Executive sponsor | Executive team | Receives a briefing on every reportable incident and every incident rated N3 or above |

A person may hold more than one role during an incident. The CISO names a deputy for the coordinator role when absent. The GRC Lead keeps the contact list for every agency tenant and for FedRAMP.

## 2. Incident rating

Each incident receives two ratings. They answer different questions and both are recorded in the incident record.

**Reportability (IEC-CSO-EFR).** An incident is a FedRAMP Reportable Incident when it affects, or is likely to affect, the confidentiality or integrity of federal customer data. Federal customer data is defined by data class in the scope record. For Orrinwick Beacon it includes responder contact details and alert content. An incident that affects only availability is not reportable under this test, but it is still rated below.

**Potential Agency Impact N-rating (IEC-CSO-EFI).** The PAIN rating estimates the likely effect of the incident on the agencies that use Orrinwick Beacon.

| Rating | Likely effect on agencies | Example for Orrinwick Beacon |
|---|---|---|
| N0 | No adverse effect is likely | A blocked phishing email sent to one staff member |
| N1 | Minimal effect on one or more agencies | A short delay in a non-urgent notification channel for one tenant |
| N2 | Narrow effect on one or more agencies | One agency's escalation rule was changed without approval and was corrected before it affected an alert |
| N3 | Disruptive effect on one agency | Alerts for one agency were not delivered for two hours |
| N4 | Debilitating effect on one agency, or disruptive effect on more than one | Responder contact details for one agency were exposed, or alert delivery failed for several agencies |
| N5 | Debilitating effect on more than one agency | Contact data or alert content for several agencies was altered or exposed |

**Default rating (IEC-CSO-DPR).** A reportable incident is treated as N5 until the CISO approves an estimate. An unrated reportable incident is never treated as a lower rating.

**After action reports.** Every FedRAMP Reportable Incident, and every incident rated N2 or above, ends with an after action report (section 7, POL-INR INR-2).

## 3. Detection and declaration

1. Alerts reach the on-call responder from the monitoring and logging service, the identity provider, the vulnerability disclosure inbox, third-party notices and staff reports.
2. The responder acknowledges the alert within 15 minutes. This is the same response time that applies to suspicious account activity (POL-IAM IAM-6).
3. If the event meets the definition in the Scope section, the responder declares an incident within 30 minutes of acknowledgement and opens an incident record with a tracking identifier in the form `INC-YYYY-NNN`.
4. The incident record holds the timeline, the ratings and the reasons for them, the reports sent, and links to tickets and evidence. It is the single source for every report in section 5.

## 4. Evaluation

| Step | Rule | Target | Recorded as |
|---|---|---|---|
| Decide whether the incident is a FedRAMP Reportable Incident | IEC-CSO-EFR | Within 1 hour of declaration | `reportable`, with the time and the reason |
| Estimate the PAIN rating | IEC-CSO-EFI | Within 4 hours of the reportability decision | `pain_rating`, with the explanation |
| Until the estimate is approved, treat a reportable incident as N5 | IEC-CSO-DPR | Immediately | Rating history in the incident record |
| Revise both ratings when new facts change them | IEC-CSO-EFI | As facts change | Rating history in the incident record |

The incident lead proposes both ratings. The CISO approves them. When the evidence is not clear, the higher rating applies until the facts are known.

**Vulnerabilities treated as incidents (VER-TFR-IRI, VER-TFR-NRI).** A likely exploitable vulnerability that is reachable from the internet and has a PAIN rating above N3 is handled as a FedRAMP Reportable Incident until it is partially mitigated to N3 or below. Orrinwick also applies this to a likely exploitable vulnerability that is not internet-reachable and is rated N5, until it is partially mitigated to N4 or below. The vulnerability report (`docs/vdr-report.md`) records each such case with its incident identifier.

## 5. Reporting to agencies and FedRAMP

**When the reporting clock starts.** The reporting targets in this section start once Orrinwick has evaluated the event, determined that it is a FedRAMP Reportable Incident (IEC-CSO-EFR), and assigned its PAIN rating or applied the default of N5 (IEC-CSO-EFI, IEC-CSO-DPR). They do not start at initial detection. A later estimate that changes the rating does not restart the clock. The evaluation targets in section 4 start at declaration.

Reports go to FedRAMP and to every affected agency, using the contacts the GRC Lead keeps. Each report is approved by the CISO and is written so that it does not expose sensitive details that would harm the service or other customers.

**Initial Incident Report (IEC-CSO-IIR).** Sent within 1 hour after the reporting clock starts. It contains as much of the following as is known at that time, and states which items are not yet known:

- contact information for the federal incident response coordinator
- the Orrinwick tracking identifier
- a description of the incident
- the timeline: start time, time and source of detection, time the reportability evaluation was completed, and other major milestones
- the current and earlier PAIN ratings, with the explanation
- the functional impact on agencies, including the effect on confidentiality or integrity and the federal customer data types affected
- the estimated recovery plan, milestones and timelines
- the list of agencies likely to be affected

**Ongoing Incident Reports (IEC-CSO-OIR).** Sent at least every 24 hours while the incident is open, and sooner when significant new information is known. When nothing has changed, the report says so. Each report updates every item in the initial report and adds, as known: observed incident activity, indicators of compromise, related CVE identifiers, the root cause, and response and recovery activities.

**Final Incident Report (IEC-CSO-FIR).** Sent within 5 business days after the incident is resolved and recovery is complete. It gives the final status of every item in the earlier reports.

## 6. Automation (IEC-CSO-AIR)

| Part of the process | Automated | Manual |
|---|---|---|
| Alert routing to the on-call responder | Yes | |
| Incident record and tracking identifier | Created from the alert | Declaration by the responder |
| Timeline | Detection and acknowledgement times captured from the alerting system | Other milestones entered by the incident lead |
| List of affected agencies | Built from the tenants of the affected resources | Checked by the GRC Lead |
| Report drafts | Initial and ongoing report drafts generated from the incident record fields | Text reviewed by the GRC Lead |
| Sending reports | Sent from the incident record to the stored contacts | Approval by the CISO before each send |
| 24-hour ongoing report reminder | Yes | |

The CISO's approval stays manual because each report states ratings and impact that need human judgement.

## 7. Containment, eradication and recovery

The incident lead and the Platform Lead decide containment steps. Changes made during an incident follow the emergency change path in POL-CMT and are reviewed after the incident (KSI-CMT-RVP). When data or a service must be restored, recovery follows the backup and restore strategy in SD-003 and the recovery objectives in `environment/recovery-objectives.json`. Using the recovery environment is logged as a significant change event (SD-004, OQ9).

## 8. After action reports (KSI-INR-AAR)

An after action report is completed within 10 business days after the incident is closed, for every reportable incident and every incident rated N2 or above. The incident lead writes it and the CISO approves it. It contains:

1. a summary, the final ratings and the reasons for any change in rating
2. the timeline, with each target in this plan and whether it was met
3. the root cause and the factors that contributed to it
4. what worked and what did not
5. each lesson, with the ticket or change reference that carries it into the backlog
6. whether this plan needs to change (`plan_change_required`)

A lesson without a ticket or change reference is not complete. When the report finds that this plan needs to change, the CISO reviews the plan (section 9).

## 9. Reviews (KSI-INR-RIR, KSI-INR-RPI)

| Review | Owner | When | Recorded in |
|---|---|---|---|
| Plan review | CISO | Each year, and when an after action report or a quarterly incident review finds that the plan needs to change | `ir_plan.reviews`, one new entry for each review with its date and reviewer | |
| Past incident review | Security team, led by the Security Operations Lead | At least every 90 days. Covers all incidents and near misses of any rating since the previous review, and lists each incident covered | `incident_pattern_reviews` |
| Tabletop exercise | Security Operations Lead | At least once a year, with the incident and recovery roster (POL-CED CED-4) | Training records |

The past incident review looks for repeated causes and weaknesses that single incidents do not show. When it finds that this plan needs to change, it sets `plan_change_required` and the CISO reviews the plan.

## 10. Records

| Record | Location |
|---|---|
| Incident record, timeline, ratings and reports | Incident tracker. Summary fields in `environment/grc-records.json` under `incidents` |
| After action reports | Incident tracker, linked from the incident record |
| Plan reviews | `environment/grc-records.json` under `ir_plan` |
| Past incident reviews | `environment/grc-records.json` under `incident_pattern_reviews` |
| Vulnerabilities treated as incidents | `docs/vdr-report.md` |

Records are kept for at least three years.
