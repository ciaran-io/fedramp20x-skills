# Evaluating a change

Read the definitions before each evaluation: `frmr.py term significant`, `term transformative`, `term adaptive`, `term routine`, `term "certification class"`. This page gives the order of questions and the evidence each answer needs. It does not replace the definitions.

## Questions, in order

The order follows the evaluation steps listed under SCN-CSO-EVA.

| # | Question | Evidence to look for | If yes |
|---|---|---|---|
| 1 | Does the change meet the definition of a significant change (FRD-SGC): a likely, substantive effect on the offering's security or privacy? | What the change alters: boundary, data flows, authentication, encryption, logging, a third party, an exclusion condition, a control's implementation | Go to 2 |
| | | | If no: **not significant**. Record who decided and why (SCN-CSO-MAR) |
| 2 | Is it likely to change the certification class of the whole offering? (FRD-CCC) | A change to the data handled or the impact level that would move the offering to another class | **Class change**: a new assessment, outside the notification rules. Stop and tell the consultant |
| 3 | Does it recur regularly and routinely as part of ongoing operations, vulnerability mitigation or remediation? (FRD-RTR) | Earlier changes of the same kind, a documented recurring procedure | **Routine recurring**. No notice (SCN-RTR-NNR) |
| 4 | Does it meet the definition of a transformative change (FRD-TRF): new risks that need in-depth assessment and could change existing risk decisions? | New features or capabilities that change how customers use the service, extensive updates to assessments, procedures or documentation | **Transformative** |
| 5 | Otherwise | | **Adaptive** (FRD-ADP) |

## Changes that rest on an exclusion condition

Before question 1, check whether the change moves data or a flow that the scope record keeps out of scope, or keeps safe, only through an exclusion condition (for example a flow that carries only company data while a condition on the source holds). If it does, the evaluation depends on that condition still holding. Name the condition, say whether the inputs show it is checked (an owner, a cycle, a record), and if they do not, still give `proposed_type` (the type if the condition holds), mark the evaluation items unconfirmed, and add a decision question for the SME that names the condition. A change to an exclusion condition itself is a change to the scope (step 4).

## Points that need SME input

- Whether a change "substantively" affects the posture (question 1) when the change touches a control but not the boundary.
- Whether a change recurs "routinely" (question 3) when it has happened only a few times.
- Whether the risks need in-depth assessment (question 4). The definition's note describes typical signs; the SME decides.

## Records

- Every evaluation is recorded, including "not significant" ones. The record names who decided.
- A change that alters the scope record gets a scope change log entry with its change type.
- Notices and related audit records are kept in human-readable and JSON form (SCN-CSO-HRM), and 12 months of notices stay available (SCN-CSO-HIS).
