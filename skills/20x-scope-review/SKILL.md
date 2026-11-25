---
name: 20x-scope-review
description: Build or review a FedRAMP 20x (Class A, B or C) Minimum Assessment Scope from a client's asset inventory, diagrams, data flows and third-party list, and return the scope record, the boundary decisions the consultant must make, and the evidence each conditional exclusion needs. Use when a consultant needs to set or check what is inside a client's cloud service offering.
---

# 20x scope review

Scope comes first: the other skills assume the scope is settled. This skill works in one of two modes.

| Mode | Use when | Output |
|---|---|---|
| Build | The client has an inventory, diagrams or a list of systems, but no scope record | A draft scope record, with every boundary decision listed for the consultant |
| Review | The client already has a scope record or scope document | Rated findings against the MAS rules, and the decisions still open |

The skill never decides that a resource is in or out of scope. It proposes, gives the reason and the rule, and the consultant decides.

## Read first

- `references/method.md`, `references/sme-validation.md`, `references/writing-rules.md`, `references/lessons.md` (L10)
- `references/classes.md`: Class A, B and C differences; pass the client's class to every script
- `references/engagement-folder.md`, `references/finding-ratings.md`
- `references/scope-guide.md`: the scope record fields, the decision values and the tests

## Inputs

| Input | Required | Notes |
|---|---|---|
| Asset inventory or system list | Yes (build) | Every system, service, tool, team and process the offering depends on |
| Architecture and data flow diagrams | Yes | Diagrams as files. If a diagram is an image, read it and list what it shows; ask about anything unclear |
| Third-party services list | Yes | Every service run by another company |
| Data types the service handles | Yes | What agencies supply to the service, and what the provider generates about it |
| Existing scope record or document | Yes (review) | |
| Security categories | When set | The client's own FIPS 199 categories. Never assign one yourself |

## Steps

1. **Set up.** Find the engagement folder. Register inputs with IDs and SHA-256. Run `python scripts/frmr.py info`. Read MAS-CSO-IIR, MAS-CSO-FLO, MAS-CSO-TPR, MAS-CSO-MDI and MAS-CSO-SUP with `python scripts/frmr.py show <ID>`, and the terms federal customer data, information resource, machine-based and third-party information resource with `python scripts/frmr.py term <word>`.

2. **List the data classes.** For each kind of data, record whether it is federal customer data, provider metadata about it, or neither, using only the client's description. If the client has not said who supplies the data, ask. Do not assign security categories; record the client's, or `[category: client to set]`.

3. **List the resources.** Every machine-based and non-machine resource in the inputs, including teams, processes and third-party services. Each gets an ID, its kind, what it handles (data class IDs) and how it could affect federal customer data, each with a source. A resource the inputs mention but do not describe is listed with an open question, not filled in.

4. **Propose a decision for each resource** using the values in `references/scope-guide.md`. Each proposal names the rule and the reason. Resources that probably handle federal customer data, or could change its confidentiality, integrity or availability, are proposed in scope (MAS-CSO-IIR). An exclusion that depends on a condition gets the condition, the evidence that shows it holds, who checks it, how often, and where that is recorded (lesson L10). Leave any part the client has not given as a placeholder and an open question.

5. **Trace the flows.** Every flow of each data class between resources and across the boundary, with protocol and protection as the inputs state them. A data class with no flow, or a flow to a resource with no decision, is a gap.

6. **Third parties.** For each third-party resource, record the information MAS-CSO-TPR lists, from the client's material only. A missing item is a gap and an open question.

7. **Review mode only.** Apply the tests in `references/scope-guide.md` to the existing record, and rate each finding with `references/finding-ratings.md`. For M8, if the client has a check that detects scope changes (for example a fingerprint of the record compared with the change log), test it by running it, not only by reading it: on a copy of the record, change one exclusion condition, one flow's protection and one third party's details, run the check after each change, and record whether it reported the change. A check that reports no change is a finding with the observed output as evidence.

8. **Stop and ask.** Every boundary decision is the consultant's. Present them with AskUserQuestion, at most four at a time, each with options, the recommended option and the reason. Record the consultant's answers in `decisions.json`. A resource stays `undecided` until the consultant answers.

9. **Write the deliverable** in `deliverables/20x-scope-review/`: `<date>-scope-review.json` following `templates/deliverable.json`, then `python scripts/build_report.py <json>`. In build mode, `items` holds the resources, flows, third parties and exclusion conditions. In review mode, it holds the findings, and `record_reviewed` names the record and its version (the record itself stays in the inputs).

10. **Check.** `python scripts/check_deliverable.py <json> --inputs <engagement>/inputs --decisions <engagement>/decisions.json` and `python scripts/frmr.py lint <md> <json>`.

11. **SME Validate.** Follow `references/sme-validation.md`. The SME should know the architecture; ask the consultant to name one. Add to the checklist: every system in the inventory appears in the record, and every exclusion condition has evidence the client can produce.

12. **Render** after validation with `scripts/render.py`.

13. **Export to FedRAMP JSON** after validation, following `references/fedramp-export.md`: schema `certification-package-overview` (fragment `thirdPartyInformationResources`). Export the third-party resources only. Fill the `fedramp_export` block from the validated deliverable only, list every value it does not hold in `missing` and ask the consultant for it, then run `python scripts/fedramp_export.py export <json> --schema <schema> --out <file>`. The script refuses a draft, an undefined field, a null or placeholder, an unsourced field and anything the schema rejects. If it reports errors, fix the block or stop and ask; never edit the output by hand.

## Must not

- Decide a boundary, a security category or an exclusion.
- Add a resource, flow or third party that no input mentions.
- Treat a third party's authorization status as known unless the client's material states it with its source.
