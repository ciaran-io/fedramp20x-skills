---
title: Validator build: KSI-INR-RIR
client: Orrinwick Labs, Inc.
class: C (CR26)
frmr_version: 2026.11.02.01 (commit 64fa769)
date: 2026-11-22
prepared_by: Claude, for A. Example
sme_validation: Draft: pending SME validation
---

# Validator build: KSI-INR-RIR

| | |
|---|---|
| KSI | KSI-INR-RIR |
| Design | I-18, KSI-INR-RIR. Reviewed and marked Verified by the fedramp20x repository owner; used here as the validated design |
| Methods | 2 |
| Unit tests | 9 of 9 passed on 2026-11-22 |
| Break tests | 4 |
| Proposed status | Verified (changes only after SME Validate) |

## Code

| | |
|---|---|
| Module | `inr-rir/inr_rir.py` |
| Tests | `inr-rir/test_inr_rir.py` |
| Break test record | `inr-rir/break-tests.json` |
| Run | `python inr_rir.py ../../../inputs/policies/POL-INR.md ../../../inputs/plans/incident-response-plan.md ../../../inputs/records/grc-records.json --as-of 2026-11-22` |
| Test | `python -m pytest inr-rir/test_inr_rir.py` |

## Inputs

| ID | File | Description |
|---|---|---|
| I-18 | `designs/INR.md` | Validator design, INR theme: KSI-INR-RIR, status Verified in fedramp20x |
| I-01 | `policies/POL-INR.md` | POL-INR Incident response policy, version 1.1 |
| I-05 | `plans/incident-response-plan.md` | Incident response plan, version 1.0 |
| I-06 | `records/grc-records.json` | GRC records export |

## inr-rir-static (static)

| | |
|---|---|
| Reads | POL-INR (owner and requirements table), the incident response plan, ir_plan.review_cadence_days in the GRC records |
| Conditions checked | a POL-INR requirement lists KSI-INR-RIR; POL-INR names an owner; the cadence is a positive number of 365 days or less; the plan exists and has no TODO lines |
| Gap | Proves the plan is written and the cycle is documented. Does not prove the plan's procedures are effective. |
| Sources | I-18 KSI-INR-RIR static method; KSI-INR-RIR |

| Break test change | Observed message | Result |
|---|---|---|
| plan: appended 'TODO: write the containment steps' | The incident response plan is not finished: TODO on line(s) 148 | failed as required |
| policy: replaced '\| Owner \| CISO \|' with '\| Owner \| \|' | POL-INR names no owner | failed as required |

## inr-rir-live (live)

| | |
|---|---|
| Reads | ir_plan.reviews, incidents and incident_pattern_reviews in the GRC records, measured against the run date |
| Conditions checked | a dated review exists; the newest review is not after the run date; the newest review is no older than the cadence; the newest review was recorded by the POL-INR owner; a review follows each after action report or past incident review that required a plan change |
| Gap | Proves the owner reviewed the plan on time and after each required change. Does not prove the review judged the procedures effective, or that a report correctly decided whether a change was needed. The current incident and past incident review records hold no dated entries, so the plan-change condition is tested only by the unit tests. |
| Sources | I-18 KSI-INR-RIR live method; I-06 ir_plan; incidents; incident_pattern_reviews; KSI-INR-RIR; VDR-TFR-NMV |

| Break test change | Observed message | Result |
|---|---|---|
| records: set ir_plan.reviews.-1.reviewed_by to "GRC Lead" | The plan review dated 2026-11-21 was recorded by 'GRC Lead', POL-INR names 'CISO' | failed as required |
| run date set to 2027-11-22 | The newest plan review is 366 days old, the cadence is 365 days | failed as required |

## Decisions for the consultant

None.

## Open questions

None.

## SME validation

Draft: pending SME validation.

