# Incident guide

## Rules to read

Read each with `frmr.py show <ID>` before using it.

| ID | Use |
|---|---|
| IEC-CSO-EFR | Evaluate reportability |
| IEC-CSO-EFI | Estimate the PAIN rating (Incident Rating) |
| IEC-CSO-DPR | Default rating of N5 for a reportable incident until estimated |
| IEC-CSO-IIR, IEC-CSO-OIR, IEC-CSO-FIR | Content of the initial, ongoing and final reports |
| IEC-CSO-AIR | Automation of reporting |
| VER-EVA-EPA | The N0 to N5 scale |
| VER-TFR-IRI, VER-TFR-NRI | Vulnerabilities treated as reportable incidents |
| FRD-FRI, FRD-FCD, FRD-INT | Definitions: reportable incident, federal customer data, incident |

The rules data gives IEC-CSO-IIR, IEC-CSO-OIR and IEC-CSO-FIR a timeframe for each PAIN rating (`pain_timeframes`, shown by `frmr.py show`). For example, at N5 the pinned data gives 1 hour for the initial report, 6 hours for ongoing reports and 6 hours for the final report; at N1 it gives 1 business day for each. Read the values for the rating in force from the rules data at run time; never type them from this page. The rule statements do not name the event each timeframe counts from. `incident_timeline.py --rating N` counts the initial report from the reportability decision ("after identifying"), repeats ongoing reports from the clock, and counts the final report from resolution ("once the incident has been resolved"). That is a reading of the statements: confirm it with the consultant. The client's plan may set tighter targets; it may not set looser ones.

## Evaluation questions

| # | Question | Evidence |
|---|---|---|
| 1 | Which resources and data classes are involved? | The incident record and the scope record |
| 2 | Is any involved data class federal customer data? | The scope record's data classes |
| 3 | Is confidentiality or integrity of that data affected, or likely to be? | What was exposed, altered or accessed |
| 4 | How many agencies, and what effect on each? | The client's tenant records; the effect words in VER-EVA-EPA |
| 5 | Is a vulnerability involved that the plan treats as an incident? | VER-TFR-IRI and VER-TFR-NRI, and the plan's own choice for the MAY rule |

## Plan review tests

| Test | Finding when | Lesson |
|---|---|---|
| I1 Reportability | The plan does not define how and by whom reportability is decided, or uses a test other than confidentiality or integrity of federal customer data | |
| I2 Rating | The plan has no PAIN rating step, or no approver for ratings | L5 |
| I3 Default N5 | The plan allows a reportable incident to be treated below N5 before a rating is approved | L8 |
| I4 Clock start | The plan starts reporting targets at detection, or does not say when the clock starts | L8 |
| I5 Report content | The plan's report contents omit an item the IEC report rules list | |
| I6 Ongoing reports | The plan sets no cadence for ongoing reports, or no rule for reports when nothing has changed | |
| I7 Final report | The plan sets no point at which the final report is sent | |
| I8 Automation | The plan does not say which steps are automated (IEC-CSO-AIR is a SHOULD) | |
| I9 Vulnerabilities | The plan does not say how vulnerabilities under VER-TFR-IRI are handled as incidents | |
| I10 Targets named as rules | The plan presents its own hour targets as FedRAMP requirements, or states hours for FedRAMP that differ from the rules data | |
| I12 Looser than the rules | For any PAIN rating, a plan target for the initial, ongoing or final report is longer than the timeframe in the rules data. Run `incident_timeline.py --rating N` for N1 to N5 with the plan's targets; each line in `plan_later_than_rules` is a High finding | L8 |
| I11 Records | The plan does not say where each rating, decision and report is recorded | L1 |
