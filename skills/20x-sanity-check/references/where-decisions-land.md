# Where decisions land

For each kind of decision, the places to search and the sections to read even when a search finds nothing.

| Decision about | Search for | Places to read |
|---|---|---|
| An owner or reviewer role | The role names (old and new), the requirement ID, the KSI ID | The policy requirement and header; the plan's roles and review tables; the record fields that hold the reviewer (`reviewed_by`); the validator design's live method; deliverables with open questions about the owner |
| A review cycle or deadline | The old and new values in every form ("quarterly", "every quarter", "90 days", "3 months", "annual", "each year", "365"); the requirement ID | The policy requirement; the plan; the cadence field in the records (`review_cadence_days`); the validator design's static method and fails-when; the check code's limit |
| A record location | The old and new file or system names | The policy requirement; the plan's records table; the validator design's methods and production source |
| A scope decision | The resource ID, its name, its data classes, its conditions and flows | The scope record; the scope change log; diagrams; the third-party entries; the policies' scope tables; validator designs that read the resource |
| A change type | The change ID, the resources, the notice rule IDs | The change log and the scope change log; the significant change log; the client review records triggered by the change |
| A policy rewrite adopted | The requirement ID, the KSIs it maps to, every value in the rewrite | Other policies that refer to it; the plan; the policy review deliverable; validator designs for its KSIs |
| A cited rule ID | The ID | Every policy and plan that cites it; run `frmr.py lint` on them |

Deliverables of the other skills are always in scope for the search. An open question or decision question that the new decision answers is an "affected" place: the follow-up is to record the decision log ID in it.
