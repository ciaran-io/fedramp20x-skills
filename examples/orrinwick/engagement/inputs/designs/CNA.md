# CNA: Cloud native architecture

> FICTIONAL DEMO PROJECT. Orrinwick Labs, Inc. and Orrinwick Beacon are invented.

Policy: [POL-CNA](../policies/POL-CNA.md).

## KSI-CNA-RVP Reviewing Protections

| Field | Design |
|---|---|
| Requirement | Orrinwick must keep reviewing whether its protection against denial of service and other unwanted traffic still works, each year and after the offering changes |
| Policy requirement | POL-CNA / CNA-7a (annual) and CNA-7b (after each recorded change) |
| Resource type | Non-machine (the review of protections, owned by the Platform Lead). The protections themselves are machine-based and are checked on every run by other CNA KSIs |
| Validation cadence | Every build. VDR-TFR-NMV requires at least every 3 months |
| Static method | `cna-rvp-static`. Reads `policies/policy-set.json`. Passes when POL-CNA requires an annual review and a review after each change recorded in `mas/scope-changes.json`, with a deadline for each SCN change type |
| Live method | `cna-rvp-live`. Reads `protection_reviews` in `environment/grc-records.json`, measured against the run date, and the resources in `environment/iac-plan.json`. Passes when the newest review is no older than 365 days, has a summary, was recorded by the Platform Lead, and lists every WAF, load balancer listener and threat detection resource in the plan |
| Change method | `cna-rvp-change`. Reads `mas/scope-changes.json` and the review dates. For each change, passes when a review falls between the change date and its deadline: 5 business days for a transformative change (plus a review before it starts), 10 for adaptive, 20 for not significant, and none for routine recurring. A review that is not yet overdue shows as a "due by" note, not a failure |
| Fails when | POL-CNA lacks the annual review, the change review or a deadline for any change type. No review in 365 days, no summary, a reviewer other than the Platform Lead, or a protection resource missing from the review. A change with no review by its deadline, or a transformative change with no review before it |
| Break test | Unit tests: a review that leaves out a protection resource fails the live method, and the change function fails an adaptive change with no review in 10 business days, notes a pending one, fails a transformative change with no review before it, and ignores routine recurring changes. Manual test on 2026-11-22: with the review after SC-001 and SC-002 removed and `FEDRAMP20X_AS_OF=2026-12-18`, the change method failed with "SC-001 (not_significant, 2026-11-19) has no protection review by the deadline 2026-12-17" |
| Production source | The Platform Lead's review record in the GRC tool, listing the WAF, rate-limit, load balancer and threat detection settings reviewed. The change records from the change management system and the significant change log |
| Gap | The methods prove that dated reviews by the right person cover every protection resource and follow every recorded change on time. They do not prove that a review judged the protections effective. Changes that are not recorded in `mas/scope-changes.json` cannot trigger a review |
| Status | Built |

**Decisions.**
- I split the policy into an annual review (CNA-7a) and a review after each change (CNA-7b), and I check them with separate methods so the evidence shows each one.
- Deadlines follow FedRAMP's change types. An adaptive change is reviewed within 10 business days, so the review is ready before the notice that SCN-ADP-NTF requires within 10 business days. A transformative change is reviewed before it starts, to inform the final plans notice, and again within 5 business days after. Routine recurring changes need no separate review, because they are frequent and exempt from notices (SCN-RTR-NNR).
- The change check is a shared function. CMT-RVP, INR-RIR and RPL-RRO will use it for their own triggers.
- The Platform Lead reviewed the protections on 2026-11-22, after SC-001 and SC-002, inside both deadlines. The review lists the changes it covers in `changes_reviewed`.
- Reviews are added as new records. A past review is never edited, so the history shows what was reviewed and when. One exception came before this rule: the 2026-06-10 review had its `resources_covered` list added on 2026-11-21.
