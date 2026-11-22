---
name: 20x-change-evaluation
description: Evaluate a described change to a FedRAMP 20x Class C cloud service offering and return its change type, the notice dates the Significant Change Notification rules set, the scope change log entry, and the review deadline the client's own policy sets. Use when a consultant or client describes a planned or finished change and needs to know what FedRAMP requires.
---

# 20x change evaluation

Every change gets one of four types: transformative, adaptive, routine recurring, or not significant (lesson L7). "Not applicable" is not a type. A change of certification class is handled separately: it needs a new assessment. The skill proposes the type with its reasons; the consultant decides.

## Read first

- `references/method.md`, `references/sme-validation.md`, `references/writing-rules.md`, `references/lessons.md` (L6, L7)
- `references/engagement-folder.md`
- `references/change-types.md`: the evaluation questions and the evidence each type needs

## Inputs

| Input | Required | Notes |
|---|---|---|
| The change | Yes | What changes, why, which resources, planned start and finish dates, whether it is an emergency |
| Scope record | Yes | To tell whether the change alters the boundary, a flow or a condition |
| The client's change policy and review rules | When they exist | For the client's own review deadlines by change type |
| Earlier evaluations of the same kind of change | Optional | A routine recurring change must recur as part of ongoing operations |

If the description does not say what changes in the offering, stop and ask. Do not infer the change from its title.

## Steps

1. **Set up.** Find the engagement folder. Register inputs. Run `python scripts/frmr.py info`. Read the definitions with `python scripts/frmr.py term significant`, `term transformative`, `term adaptive`, `term routine`, `term "certification class"`, and the rules with `python scripts/frmr.py rules --family SCN --affects Providers`.

2. **Describe the change** in plain words: what changes, which resources and data classes (by scope record ID), and what changes for agency customers. Every element comes from the inputs.

3. **Evaluate** with the questions in `references/change-types.md`, in order. For each question, record the answer and the evidence. Where an answer depends on something the inputs do not show (for example whether a change needs in-depth assessment, or whether it recurs), stop and ask the SME. Propose one type.

4. **Scope effect.** If the change adds, removes or moves a resource, changes a decision, a flow or an exclusion condition, draft a scope change log entry: change type, resources, summary, evaluation, and the change type. The entry is a draft until the consultant approves it.

5. **Notice dates.** Run `python scripts/scn_timeline.py notices --type <type> --start <date> --finish <date>` (add `--verified` for transformative changes when known). Business days skip US federal holidays by default; add `--holidays <file>` for a client's extra holidays, or `--no-federal-holidays` if the consultant decides on weekdays only. Copy the dates and the business day basis into the deliverable. Never type a timeframe from memory. For an emergency, read SCN-CSO-EMG and record what must be provided after the event.

6. **Notice content.** For a transformative or adaptive change, list the information SCN-CSO-INF requires and, for each item, whether the inputs supply it. A missing item is an open question.

7. **Client review deadline.** If the client's policy sets a review after a change by type (for example a protection review), compute it with `python scripts/scn_timeline.py bizdays --from <date> --days <n>` and say which policy requirement sets it. If the policy sets none, say so; do not invent one.

8. **Stop and ask.** Present the proposed type, the reasons and the alternatives with AskUserQuestion. Also confirm the business day basis printed by the script. Record the decision in `decisions.json`.

9. **Write the deliverable** in `deliverables/20x-change-evaluation/`: `<date>-<change-id>-change-evaluation.json` following `templates/deliverable.json`, then `python scripts/build_report.py <json>`.

10. **Check** with `scripts/check_deliverable.py` and `scripts/frmr.py lint`.

11. **SME Validate.** Follow `references/sme-validation.md`. Add to the checklist: the type matches the definitions, every date was computed by the script, and the business day basis is confirmed.

12. **Render** after validation with `scripts/render.py`.

## Must not

- Record "not applicable" as a change type.
- State a notice timeframe or date that the script did not compute from the rules data.
- Decide the type on the consultant's behalf.
