---
name: 20x-incident-reporting
description: For a FedRAMP 20x Class C provider, evaluate an incident (reportability, PAIN rating, reporting timeline that starts at the reportability decision, report content) or review a draft incident response plan against the incident rules. Use when a consultant brings an incident to evaluate, or an incident response plan to check.
---

# 20x incident reporting

Two modes.

| Mode | Input | Output |
|---|---|---|
| Evaluate | An incident record or description, and the client's incident response plan | Proposed reportability decision and PAIN rating with reasons, the reporting timeline from the client's targets, and the content each report still needs |
| Plan review | A draft or current incident response plan | Rated gaps against the IEC rules and lessons L8 and L5 |

The reporting clock starts when the incident is judged reportable and rated, or the default N5 is applied, not at detection (lesson L8). An unrated reportable incident is treated as N5 (IEC-CSO-DPR). The skill proposes; the consultant and the client's named approver decide.

## Read first

- `references/method.md`, `references/sme-validation.md`, `references/writing-rules.md`, `references/lessons.md` (L5, L8)
- `references/engagement-folder.md`, `references/finding-ratings.md`
- `references/incident-guide.md`: the rules to read, the evaluation questions and the plan tests

## Inputs

| Input | Required | Notes |
|---|---|---|
| The incident | Evaluate mode | What happened, which resources and data, times of start, detection and declaration, what is known and not known |
| The client's incident response plan | Yes | The plan's targets set the timeline. Without a plan, say so: FedRAMP sets no fixed hours, so no timeline can be computed |
| Scope record | Yes | Which data classes are federal customer data, and which resources handle them |
| Affected agencies | Evaluate mode | From the client's tenant records. Never guess which agencies are affected |

## Steps

1. **Set up.** Find the engagement folder. Register inputs. Run `python scripts/frmr.py info`. Read the IEC rules with `python scripts/frmr.py rules --family IEC --affects Providers` and each with `show`. Read the N-rating scale with `python scripts/frmr.py show VER-EVA-EPA` and the definitions with `term "reportable incident"` and `term "federal customer data"`.

2. **Evaluate mode: reportability.** Using the scope record, identify the data classes and resources involved. Answer the reportability test in IEC-CSO-EFR and FRD-FRI: is confidentiality or integrity of federal customer data affected now, or probably going to be? An incident that affects only availability is not reportable under that test; say so and still rate it. Give the evidence for the answer. If the facts are not known yet, say what would decide it and stop to ask.

3. **Evaluate mode: PAIN rating.** Propose an N-rating using the scale in VER-EVA-EPA and the client's own examples in its plan. Give the reason, the number of agencies affected (from the client's records) and the effect (minimal, narrow, disruptive, debilitating). While no rating is approved, a reportable incident is N5. Where the evidence supports two ratings, the plan may say the higher applies; follow the plan.

4. **Evaluate mode: timeline.** Take each target from the client's plan (reportability decision, rating, initial report, ongoing reports, final report) with its section reference. Run `python scripts/incident_timeline.py` with the incident's event times and those targets. Set `--clock-start` to the event the plan names; if the plan does not name one, ask. Copy the output into the deliverable.

5. **Evaluate mode: report content.** For the initial, ongoing and final reports, list the information the IEC rules require (IEC-CSO-IIR, IEC-CSO-OIR, IEC-CSO-FIR) and, for each item, whether the incident record supplies it. A missing item is an open question for the incident lead, not a gap to fill.

6. **Plan review mode.** Apply the tests in `references/incident-guide.md` to the plan. Rate each finding with `references/finding-ratings.md`.

7. **Stop and ask.** The reportability decision and the rating belong to the client's approver (the plan names who). Present the proposals with AskUserQuestion, with the evidence and the alternative. Record answers in `decisions.json`.

8. **Write the deliverable** in `deliverables/20x-incident-reporting/`: `<date>-<incident or plan>-incident-reporting.json` following `templates/deliverable.json`, then `python scripts/build_report.py <json>`.

9. **Check** with `scripts/check_deliverable.py` and `scripts/frmr.py lint`.

10. **SME Validate.** Follow `references/sme-validation.md`. Add to the checklist: every time in the timeline came from the plan and the incident record, and the clock start matches the plan.

11. **Render** after validation with `scripts/render.py`.

## Must not

- Start the reporting clock at detection unless the client's plan says so.
- Lower a rating below N5 for a reportable incident before the client's approver accepts an estimate.
- State a reporting deadline in hours as a FedRAMP requirement. The hours are the client's targets.
- Name an affected agency that the client's records do not name.
