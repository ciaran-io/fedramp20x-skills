# Lessons the skills apply

These come from the fedramp20x worked example. Each is a test the relevant skill applies to client material.

| # | Lesson | Test to apply | Skills |
|---|---|---|---|
| L1 | "Persistently" (FRD-PER) means a repeated cycle that is intentional, documented and whose status is always known. The provider sets the cycle | Does the policy state the cycle, who runs it and where its status is recorded? "Regularly" or "as needed" is not a cycle | policy review, validator design |
| L2 | VDR-TFR-NMV sets how often the status of a non-machine resource is validated. It does not set how often the activity itself happens | Do not tell a client that a review must happen every 3 months because of NMV. The check that reads the review record must run at least that often | policy review, validator design |
| L3 | A check that cannot fail is not evidence | Every method has a recorded break test. Record ages are measured against the real run date, not a fixed date | validator design, validator build, assessor review |
| L4 | Review records only grow | Each review is a new entry. A past entry is never edited. A check reads the newest entry | validator design, validator build |
| L5 | A review must be recorded by the role the policy names | The check compares the reviewer with the policy owner | policy review, validator design |
| L6 | A change-triggered review needs a deadline by change type, with a "due by" note before it is overdue | The policy sets a deadline for each SCN change type. The check reports pending reviews as notes, overdue ones as failures | validator design, change evaluation |
| L7 | Every change gets one of the four change types | No "not applicable". "Not significant" records that someone decided | change evaluation |
| L8 | The incident reporting clock starts at the reportability decision and rating, not at detection. An unrated reportable incident is treated as N5 | Check the plan's clock start and its default rating (IEC-CSO-DPR) | incident reporting |
| L9 | A policy can point to the wrong document | Open each document a requirement references and check that it says what the requirement needs | policy review, assessor review |
| L10 | A conditional exclusion from scope is valid only while its evidence exists | Each condition names its evidence, and a check or review confirms it | scope review, assessor review |
| L11 | A pass with a coverage note can overstate the evidence | A KSI whose methods prove less than the statement is reported as partial, with the gap | validator design, assessor review |
| L12 | A rule cited by a policy may not apply to the offering | Check each cited ID with `frmr.py lint`. For example, the FRC-CCL class change rules apply to Rev5 only | policy review, assessor review, sanity check |
