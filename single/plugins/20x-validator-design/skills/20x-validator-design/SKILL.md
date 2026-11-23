---
name: 20x-validator-design
description: Write a FedRAMP 20x Class C validator design for one or more KSIs, from the client's policy requirement and the client's own tools, stating every way each automated method fails and the break test that proves it. Use when a consultant needs to design how a KSI will be checked before any check code is written.
---

# 20x validator design

Writes one validator design per KSI, using the template in `references/validator-design-template.md`. A design says what each automated method reads, when it passes, every way it fails, the break test that will prove it can fail, and where it proves less than the KSI. Code is written later by `20x-validator-build`.

## Read first

- `references/method.md`, `references/sme-validation.md`, `references/writing-rules.md`
- `references/lessons.md`: L1 to L6 and L11 apply to every design
- `references/validator-design-template.md`: the fields, statuses and design checks
- `references/engagement-folder.md`, `references/design-guide.md`

## Inputs

| Input | Required | Notes |
|---|---|---|
| The KSI IDs to design | Yes | One or more. Ask if not given |
| The client's policy requirement for each KSI | Yes | Best from a validated `20x-policy-review` deliverable. Otherwise the policy itself |
| The client's tools and records | Yes | What systems, exports, APIs, infrastructure code or record files exist, and what fields they hold. Samples or schemas, not descriptions from memory |
| Plans and procedures the requirement depends on | When they exist | For example the incident response plan for INR KSIs |
| Existing designs | Optional | To update rather than replace |

If the client has not said which system holds a record, do not choose one. Write `[source: client to confirm]` and ask.

## Steps

1. **Set up.** Find the engagement folder and `engagement.json`. Register each input with an ID and SHA-256. Run `python scripts/frmr.py info`.

2. **Read the KSI.** For each KSI run `python scripts/frmr.py show <KSI-ID>` and read each listed term with `python scripts/frmr.py term <term>`. Split the statement into its parts (see `references/design-guide.md`). Write the Requirement field in plain words; do not copy the statement.

3. **Find the policy requirement.** Use the policy review deliverable if there is one. If the requirement has an open gap that changes what a check must prove (no owner, no cycle, no record location), stop and ask the consultant whether to design against the current text or against an agreed rewrite. Record the answer as a decision.

4. **Classify the resource.** Machine-based or non-machine (see `references/design-guide.md`). This sets the minimum cadence: run `python scripts/frmr.py show VDR-TFR-MVX` or `VDR-TFR-NMV` and use the timeframe it gives.

5. **Choose the methods.** At least two automated methods per KSI (`python scripts/frmr.py show FRC-CSX-VVK`). Name each method `<theme>-<ksi>-<kind>`, for example `inr-rpi-live`; where two methods have the same kind, add a short suffix (`iam-aam-live-review`). For each method record what it reads (a named client file, field, API or export), and when it passes. The static and live methods must read different sources. Add a change method where the policy sets a review after a change. A trigger that is not a significant change (for example an after action report or a past incident review) still needs a deadline the policy states; if it states none, ask (L6). Use only sources in the client's material. Where the record a method needs does not exist yet, or lacks a field, say so in the design and list the field the client must add as a decision.

6. **Write "Fails when".** One condition for every pass condition, plus: no record, a record dated after the run date, a record older than the cadence measured against the run date, a reviewer other than the role the policy names, and a change with no review by its deadline. Pending change reviews are notes, not failures.

7. **Plan the break tests.** For each method, the smallest change to the input that must make it fail, and the message you expect. Mark each "Planned". `20x-validator-build` runs them.

8. **Production source.** Name the client system the check reads in production, only from the client's material.

9. **Gap.** State what the methods do not prove against each part of the KSI. If a part is not covered by any method, the KSI's best result is partial (lesson L11).

10. **Run the design checks** in `references/validator-design-template.md`. Fix each failure, or record why it does not apply.

11. **Stop and ask.** Present the decisions (source choices, cadence where policy and plan differ, reviewer role, record fields to add) and open questions with AskUserQuestion, at most four at a time, each with a recommended option. Record answers in `decisions.json`. Do not finish a design whose methods depend on an unanswered question; leave its status as Draft with `confirmed: false`.

12. **Write the deliverable** in `deliverables/20x-validator-design/`: `<date>-validator-design.json` following `templates/deliverable.json` (each design is one item), then run `python scripts/build_report.py <json>` to write the Markdown and the tables JSON.

13. **Check.** `python scripts/check_deliverable.py <json> --inputs <engagement>/inputs --decisions <engagement>/decisions.json` and `python scripts/frmr.py lint <md> <json>`.

14. **SME Validate.** Follow `references/sme-validation.md`. The SME for a design is someone who knows the client's tools: ask the consultant to name one. Add to the checklist: each source named in a method exists and holds the field the method reads.

15. **Render** after validation: `python scripts/render.py docx <md> <docx>` and `python scripts/render.py xlsx <tables.json> <xlsx>`.

## Rules for designs

- Status is Draft until SME Validate, then Designed. A design becomes Built or Verified only through `20x-validator-build`.
- Never write a break test result that was not observed.
- Never name an API, field or file that the client's material does not show. A placeholder and an open question are always acceptable.
- A coverage note never turns a partial into a pass.
