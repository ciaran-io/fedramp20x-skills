# Review areas and tests

Each test names the lesson it applies (see `lessons.md`). Report a pattern once, with every place it occurs.

## Scope (scope record, inventory, data flows, third parties)

| Test | Finding when | Lesson |
|---|---|---|
| S1 Every resource decided | A resource has no in-scope or excluded decision, or no rationale | |
| S2 Conditional exclusions | An exclusion depends on a condition that names no evidence, or the evidence is missing or older than its own cycle | L10 |
| S3 Flows | A data flow crosses the boundary with no recorded control, or a federal customer data class has no flow showing where it goes | |
| S4 Third parties | A third-party resource lacks any of the information MAS-CSO-TPR lists (read it with `frmr.py show MAS-CSO-TPR`) | |
| S5 Change log | The scope changed with no change log entry, or an entry has no change type | L7 |

## Policies

Apply the tests in the `20x-policy-review` skill's `policy-tests.md` when the policies have not been reviewed. When a policy review deliverable exists, review that deliverable instead (area "deliverable") and spot-check five requirements against the policies.

| Test | Finding when | Lesson |
|---|---|---|
| P1 Reference | A requirement points to a document that does not say what the requirement needs | L9 |
| P2 Rule IDs | A cited ID is unknown or does not apply at Class C for 20x | L12 |
| P3 Cycle | A "persistently" KSI has no documented cycle | L1 |
| P4 Policy and plan agree | A policy and its plan state different owners, cycles or records for the same activity | |

## Validator designs

| Test | Finding when | Lesson |
|---|---|---|
| D1 Two methods | A KSI has fewer than two automated methods (FRC-CSX-VVK) | |
| D2 Different sources | The static and live methods read the same source | |
| D3 Fails when | A pass condition has no matching failure condition | |
| D4 Run date | A method measures record ages against a fixed date | L3 |
| D5 Records only grow | A method reads a single record that is overwritten, not a list | L4 |
| D6 Reviewer | A review method does not compare the reviewer with the policy owner | L5 |
| D7 Change deadline | A change method has no deadline for a change type, or no "due by" note | L6 |
| D8 Break test | A method has no break test, or its result is stated without being observed | L3 |
| D9 Gap | The design's gap leaves part of the KSI unproven but the status claims more | L11 |

## Results and evidence

| Test | Finding when | Lesson |
|---|---|---|
| R1 Coverage note | A KSI reports pass while a coverage note or design gap says the methods prove less than the KSI. Under a status model where a known gap means partial, this overstates the evidence | L11 |
| R2 Cannot fail | A method's result never changes across the history while its inputs change, or a method passes on empty input | L3 |
| R3 Freshness | The newest result is older than the cadence rule (VDR-TFR-MVX for machine-based, VDR-TFR-NMV for non-machine) | |
| R4 Edited history | A past record or result was changed rather than a new entry added | L4 |
| R5 Reviewer | A review record names a role other than the policy owner | L5 |
| R6 Method count | A result lists fewer methods than the design | |

## Deliverables of the other 20x skills

| Test | Finding when |
|---|---|
| X1 Sources | An item has no source, or its source does not say what the item says |
| X2 Made up | An owner, cadence, tool, system, field or date appears that no input or decision contains |
| X3 Status | The deliverable is marked validated while items are unconfirmed or questions are open |
| X4 Lint | `frmr.py lint` reports an error |
| X5 Inputs missing | The deliverable relies on a document it lists as not provided, without saying so |

## Rules the client cannot act on yet

Report these in `not_assessed`, not as findings. Decide from the rule's subset and the client's stage, then confirm the list with the consultant.

| Client stage | Usually not yet actionable | Reason |
|---|---|---|
| Preparing (not yet applying) | FRC-APP subset; MKT; CCM-OCR and CCM-QTR; IVV assessments; SCN notifications to agencies | They start when the client applies, is listed or is certified, or when an agency relies on the offering |
| Applying | CCM-OCR and CCM-QTR reports; SCN notifications to agencies | They start after certification |
| Certified | None by stage | All provider rules apply |

Rules that affect only FedRAMP, agencies or assessors are never provider findings. Use `frmr.py rules --affects Providers`.

A rule that is not yet actionable can still shape a recommendation. For example, a design can record what an Ongoing Certification Report will need later.
