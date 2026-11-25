# Finding ratings

All skills that rate findings use this scale. The rating describes the gap in the evidence. It is not a verdict on compliance.

| Rating | Use when |
|---|---|
| High | A KSI or a MUST rule that applies at the client's class has no implementation, no policy requirement or no evidence, or the evidence contradicts the requirement |
| Moderate | Something is in place, but it proves less than the requirement: a check that cannot fail, a review by the wrong role, a cycle with no stated cadence, a change review with no deadline, a reference to the wrong document, a cited rule that does not apply |
| Low | The requirement is met in substance but the record is imprecise: a missing record location, an unclear owner title, inconsistent IDs |
| Observation | No gap against a rule now. An improvement, a SHOULD or MAY rule not followed with a recorded reason, or a risk to watch |

Rules for rating:

- Rate against the rule's force at the client's class, read with `scripts/frmr.py show <ID> --class <class>` (at Class A, use `class_a_force` from `frmr.py rules --class a`). A gap against a SHOULD rule is at most Moderate. A MAY rule gives at most an Observation.
- Rate the gap, not the effort to fix it.
- When the rating depends on a fact the material does not show, ask the SME. Do not pick the lower rating to be safe or the higher one to be cautious.
- Each rated finding has: observation (what the evidence shows, with sources), criteria (rule or KSI ID, and the client's own policy requirement where there is one), rating, and recommendation.
