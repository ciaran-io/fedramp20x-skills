# Tests for each policy requirement

Apply each test to each requirement. Record a failure as a gap. Each test lists the evidence to look for and the usual rating; adjust the rating with `finding-ratings.md` and ask the SME when the rating depends on a fact the policy does not show.

| Test | Question | Fails when | Usual rating | Lesson |
|---|---|---|---|---|
| T1 Owner | Does the requirement name the role that does the activity and records it? | No role is named, or a group ("the security team") is named where a review must be recorded by one accountable role | Low; Moderate for a review KSI | L5 |
| T2 Cycle | For a KSI whose terms include "Persistently" (FRD-PER), does the requirement state the cycle: how often, or which event starts it, and that its status is recorded? | No cadence or trigger; or vague words such as "regularly", "periodically", "as needed", "promptly", "ongoing" | Moderate | L1 |
| T3 Record | Does the requirement say where the record is kept? | No record location | Low | |
| T4 Reviewer | For a review KSI (names ending in "Reviewing" or statements about reviewing effectiveness), does the requirement name who reviews, and is that the role whose record a check will compare? | The reviewer is not named, or differs from the role that owns the policy without a stated reason | Moderate | L5 |
| T5 Change deadline | Where a review is triggered by a change, is there a deadline for each SCN change type (transformative, adaptive, not significant, routine recurring), and does each deadline fit the notice timelines (read SCN-ADP-NTF, SCN-TRF-NIP, SCN-TRF-NFP, SCN-RTR-NNR with `frmr.py show`)? | No deadline, one deadline for all types without a reason, or a deadline that falls after the notice it should inform | Low to Moderate | L6 |
| T6 Reference | Does each document, policy or requirement the text points to exist in the inputs and say what the requirement needs? | The reference is missing from the inputs (open question), or the referenced document covers something else | Moderate when it covers something else; open question when not provided | L9 |
| T7 Mapping | Does the requirement address each KSI the client mapped it to? | The text does not address part or all of a mapped KSI | Moderate | |
| T8 Rule IDs | Does each FedRAMP ID cited exist, and apply at Class C for 20x? Use `frmr.py lint` | Unknown ID, or an ID outside Class C 20x applicability | Moderate | L12 |
| T9 NMV reading | Does the policy treat VDR-TFR-NMV (3 months) as how often the activity must happen? | The text sets an activity's cadence "because of" NMV, or states NMV forces a quarterly review | Low; Moderate if a required cycle is then missing | L2 |
| T10 Consistency | Do numbers, owners and names agree across policies (objectives, deadlines, role titles)? | Two policies state different values for the same thing | Moderate | |

## Parts of a KSI

Split each KSI statement into its parts before mapping. For example, a KSI about after action reports has two parts: reports are generated, and lessons are persistently incorporated. A requirement that covers only the first part gives "partial", with a gap for the second part.

## What is not a gap

- A requirement that is stricter than the rule. Note it only when it creates a check the client cannot meet.
- A KSI the client mapped to a different requirement than you would, when the mapped requirement addresses it.
- Missing evidence. This skill reviews what the policies say. Evidence is reviewed by `20x-assessor-review`.
