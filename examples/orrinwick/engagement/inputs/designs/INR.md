# INR: Incident response

> FICTIONAL DEMO PROJECT. Orrinwick Labs, Inc. and Orrinwick Beacon are invented.

Policy: [POL-INR](../policies/POL-INR.md). Plan: [incident response plan](../incident-response-plan.md).

## KSI-INR-RIR Reviewing Incident Response Procedures

| Field | Design |
|---|---|
| Requirement | Orrinwick must keep reviewing whether its documented incident response procedures work. FedRAMP defines "persistently" (FRD-PER) as a repeated cycle that is intentional, documented and always known. POL-INR documents that cycle for this KSI |
| Policy requirement | POL-INR / INR-1 and INR-3 |
| Resource type | Non-machine (the incident response plan and its review, owned by the CISO) |
| Validation cadence | Every build. VDR-TFR-NMV requires at least every 3 months |
| Static method | `inr-rir-static`. Reads `ir_plan` in `environment/grc-records.json`, `policies/policy-set.json` and the plan. Passes when a POL-INR requirement lists INR-RIR, POL-INR names an owner, `review_cadence_days` is a positive number of 365 or less, and the plan exists with no `TODO` lines |
| Live method | `inr-rir-live`. Reads `ir_plan`, `incidents`, `incident_pattern_reviews`, and measures ages against the run date. Passes when the newest entry in `ir_plan.reviews` is inside the cadence, its `reviewed_by` matches the POL-INR owner, and the review date is on or after every after action report and every quarterly incident review that sets `plan_change_required` |
| Fails when | No POL-INR requirement covers INR-RIR, or POL-INR names no owner. The cadence is missing or longer than 365 days. The plan is missing or still has `TODO` lines. No review is recorded, it is after the run date or older than the cadence, or a person other than the owner recorded it. A report or review required a plan change and no plan review follows it |
| Break test | Static: the outline plan failed the method with "The incident response plan is not finished: TODO on line(s) 14, 17, 20, 23, 26, 29, 32". Live: on 2026-11-21 I set `reviewed_by` to "GRC Lead". The build showed 35 pass and 3 fail, and the method failed with "The plan review was recorded by 'GRC Lead', POL-INR names 'CISO'". Unit tests also cover an overdue review, a review by the wrong person and a plan change with no later review |
| Production source | The document management system or GRC tool: the plan's version history and the CISO's dated approval. The incident tracker for after action reports that require a plan change |
| Gap | The methods prove that the owner reviewed the plan on time and after each required change. They do not prove that the review judged the procedures effective, or that a report correctly decided whether a plan change was needed |
| Status | Verified |

**Decisions.**
- I defined the cycle as annual, and when an after action report (INR-AAR) or a quarterly incident review (INR-RPI) finds that the plan needs to change. A full review after every incident would repeat the after action report. This trigger reviews the plan when the evidence says it is wrong, and it connects the three INR KSIs.
- An outline plan fails the static method. A plan file that exists but has no content is not evidence that procedures are documented.
- The review must be recorded by the role that POL-INR names (CISO). A review with no named owner is weak evidence.
- Plan reviews are a list, and each review is added as a new entry. The approval of version 1.0 on 2026-11-21 is recorded as a review, so the record matches the plan header. Earlier reviews stay as they were.
