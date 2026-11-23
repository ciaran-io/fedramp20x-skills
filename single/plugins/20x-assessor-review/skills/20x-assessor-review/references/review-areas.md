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

When the policies have not been reviewed, check that every requirement a KSI depends on names an owner, a cycle and a record location (the core of the policy review's tests T1 to T3), and recommend a full policy review. When a policy review deliverable exists, review that deliverable instead (area "deliverable") and spot-check five requirements against the policies.

| Test | Finding when | Lesson |
|---|---|---|
| P1 Reference | A requirement points to a document that does not say what the requirement needs | L9 |
| P2 Rule IDs | A cited ID is unknown or does not apply at Class C for 20x | L12 |
| P3 Cycle | A "persistently" KSI has no documented cycle | L1 |
| P4 Policy and plan agree | A policy and its plan state different owners, cycles or records for the same activity | |
| P5 Claims match reality | A plan or policy describes automation, a link, a report or a record as in place, and the inputs show it is planned, missing or broken | |
| P6 Required exercise | A plan requires an exercise or test (tabletop, restore test, failover, incident exercise) and no dated record of one exists within its cycle. List every exercise each plan names, then look for its record; a record type the plan names but no record file holds is itself the finding | L1 |
| P7 Approval trace | A policy or plan approval is only a role and a date, with no record that can be traced (decision record entry, tagged commit, signed approval) | |

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
| D8 Break test | A method has no break test, or its result is stated without being observed. A test suite should show every registered method failing at least once on bad data | L3 |
| D9 Gap | The design's gap leaves part of the KSI unproven but the status claims more | L11 |

## Results and evidence

| Test | Finding when | Lesson |
|---|---|---|
| R1 Coverage note | A KSI reports pass while a coverage note or design gap says the methods prove less than the KSI. Under a status model where a known gap means partial, this overstates the evidence | L11 |
| R2 Cannot fail | A method's result never changes across the history while its inputs change, or a method passes on empty input. Run `scripts/empty_probe.py` on a copy of the client's checks: each method that still passes when an input is emptied is a finding. If the checks read fixed paths, use the adapter pattern in the validator build skill's `check-patterns.md`. If no check code is in the inputs, say in the deliverable that R2 was applied to the results only | L3 |
| R3 Freshness | The newest result is older than the cadence rule (VDR-TFR-MVX for machine-based, VDR-TFR-NMV for non-machine) | |
| R4 Edited history | A past record or result was changed rather than a new entry added. Where the inputs are a git repository, read the history of each record file (`git log -p -- <file>`) and look for a change to an entry dated before the commit, not only for added entries | L4 |
| R5 Reviewer | A review record names a role other than the policy owner | L5 |
| R6 Method count | A result lists fewer methods than the design | |
| R7 Not passing | A KSI's latest result is fail, partial or not implemented. Report the KSI, how long it has held that status in the history, and whether a plan with an owner and a date exists. Rate by the KSI's effect on federal customer data, not by the count | |

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

For a rule family this table does not name (for example AFC, CDS, CPO, FRC-CSO, SDR, VER reporting, IEC reporting), read the rule statement for its trigger, such as "with Class C Certifications", "after certification" or "when applying". If the statement names a trigger the client has not reached, put the rule in `not_assessed` with that trigger as the reason. If it names none, treat the rule as actionable now. Ask the consultant when two readings are possible; do not decide by family name alone. A rule for providers "seeking" certification (for example FRC-CSX-VVK) is treated as actionable while preparing, because the work it sets is done before applying; record this reading as a decision for the consultant.

Rules that affect only FedRAMP, agencies or assessors are never provider findings. Use `frmr.py rules --affects Providers`.

A rule that is not yet actionable can still shape a recommendation. For example, a design can record what an Ongoing Certification Report will need later.
