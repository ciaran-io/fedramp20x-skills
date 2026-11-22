# Design guide

## Split the KSI into parts

Each part needs at least one method, or a stated gap.

| KSI pattern | Parts |
|---|---|
| "X is generated and Y is persistently incorporated" | X exists for each case that needs it; Y happens on a cycle |
| "The effectiveness of X is persistently reviewed" | X is documented; a review happens on the cycle; the review is by the named role; the review judged effectiveness (usually a gap: a check cannot judge it) |
| "Machine-based resources are persistently reviewed to ensure Z" | The declared configuration requires Z; the observed state shows Z; the check runs at least every 3 days |
| "X is defined and persistently reviewed for alignment with Y" | X is defined; a review compares X with Y; the review is on the cycle |

## Machine-based or non-machine

Read the definition: `python scripts/frmr.py term machine-based`.

| Resource | Type | Minimum cadence rule |
|---|---|---|
| Cloud configuration, network, identity settings, backup jobs, pipeline logs | Machine-based | VDR-TFR-MVX |
| Policies, plans, reviews, reports, training, people's decisions | Non-machine | VDR-TFR-NMV |

The rule sets how often the check runs. It does not set how often the activity happens (lesson L2). The activity's cycle comes from the client's policy.

## Static and live methods

| Method | Reads | Example |
|---|---|---|
| Static | Declared state: the policy, the plan, infrastructure code, configuration as written | The policy names an owner and a cycle of 365 days or less; the plan has no TODO lines |
| Live | Observed state: records, exports, API results | The newest review is no older than the cycle, measured against the run date, and was recorded by the named role |
| Change | Events that trigger a review | Each failed change has a review within 10 business days; a pending one is a "due by" note |

## Record rules

- Read reviews as a list. The newest entry counts. Entries are never edited (lesson L4).
- Measure every age against the run date. A check with a fixed date cannot fail as time passes (lesson L3).
- Compare the reviewer with the role the policy names (lesson L5).
- A record dated after the run date is a failure.

## Break tests

| Method kind | Typical break test |
|---|---|
| Static | Remove the owner from the policy; set the cycle to 400 days; add a TODO line to the plan |
| Live | Change the reviewer to another role; move the run date past the cycle; remove an item the review must cover |
| Change | Add a change with no review and move the run date past its deadline; check the "due by" note before it |

## When the policy and the plan disagree

If a policy and a plan state different owners, cycles or records for the same activity, do not choose. List it as a decision for the consultant with both sources, and recommend one. Design against the answer.
