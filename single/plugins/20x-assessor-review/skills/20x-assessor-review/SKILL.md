---
name: 20x-assessor-review
description: Review a FedRAMP 20x (Class A, B or C) client's finished work (scope record, policies, validator designs, check results, evidence, or deliverables from the other 20x skills) as an assessor would, and return rated findings with observation, criteria, rating and recommendation. Use when a consultant wants finished work challenged before a client or an assessor sees it.
---

# 20x assessor review

Reviews finished work the way an independent assessor would, and reports what the evidence shows and where it falls short. It does not certify anything and does not state that the client is compliant. It skips rules the client cannot act on yet and lists them separately.

## Read first

- `references/method.md`, `references/sme-validation.md`, `references/writing-rules.md`
- `references/classes.md`: Class A, B and C differences; pass the client's class to every script
- `references/lessons.md` and `references/finding-ratings.md`
- `references/validator-design-template.md` (to review designs and results)
- `references/review-areas.md`: what to test in each kind of work
- `references/engagement-folder.md`

## Independence

An assessor review is worth more when the reviewer did not produce the work. If this session wrote the work under review, tell the consultant and recommend running this skill in a new session, or as a separate agent given only the work and the inputs. Proceed only after the consultant answers, and record the answer in the deliverable.

## Inputs

| Input | Required | Notes |
|---|---|---|
| The work to review | Yes | Any of: scope record, policies, plans, validator designs, check code, check results and history, evidence exports, deliverables of the other 20x skills |
| The client's stage | Yes | Ask: preparing, applying for certification, or certified. It decides which rules the client can act on now |
| The client sources the work relies on | When available | So each claim in the work can be traced |
| Earlier assessor reviews | Optional | To report which earlier findings are closed |

## Steps

1. **Set up.** Find the engagement folder. Register each input with an ID and SHA-256. Run `python scripts/frmr.py info`. Ask for the client's stage if it is not in `engagement.json`, and write the answer there as `stage`.

2. **Decide the review areas** from the inputs: scope, policy, design, results, evidence, deliverable. List them for the consultant and ask whether any area is out of the review. Each area's tests are in `references/review-areas.md`.

3. **List the rules in play.** Run `python scripts/frmr.py rules --affects Providers` and `python scripts/frmr.py ksis`. For each rule, decide from its subset and the client's stage whether the client can act on it now (see "Rules the client cannot act on yet" in `references/review-areas.md`). Put the rest in the `not_assessed` list with the reason and the event that brings them in. Do not guess the stage of a rule; if unclear, ask.

4. **Run the tests** for each area. For every finding record: the observation (what the evidence shows, with its source), the criteria (rule or KSI ID, and the client's own policy requirement where there is one), the rating from `references/finding-ratings.md`, the lesson it applies (L1 to L12) and a recommendation. Read each rule you cite with `python scripts/frmr.py show <ID>` before you rate against it. Where the client's checks are in the inputs, run `python scripts/empty_probe.py` on a copy of them (test R2), so a method that cannot fail is found by running it, not by reading it.

5. **Run the mechanical checks.** On each deliverable of the other skills: `python scripts/check_deliverable.py <json>` and `python scripts/frmr.py lint <md> <json>`. On the client's policies and documents: `python scripts/frmr.py lint --client <files>`. An unknown FedRAMP ID, or a cited rule that does not apply at Class C, is a finding (P2) unless it is already reported. In the client's own documents, copied statement text is an Observation at most; a placeholder ID in a template is not a finding.

6. **Compare with earlier reviews.** For each earlier finding, record closed, open or partly closed, with the evidence. Never mark a finding closed without evidence in the inputs.

7. **Stop and ask.** A finding whose rating depends on a fact the inputs do not show gets `confirmed: false` and an open question. Ask the consultant with AskUserQuestion, at most four at a time. Typical questions: whether a record exists outside the inputs, what a tool does, whether a condition on an exclusion still holds.

8. **Write the deliverable** in `deliverables/20x-assessor-review/`: `<date>-assessor-review.json` following `templates/deliverable.json`, then `python scripts/build_report.py <json>` for the Markdown and the tables JSON.

9. **Check.** `python scripts/check_deliverable.py <json> --inputs <engagement>/inputs --decisions <engagement>/decisions.json` and `python scripts/frmr.py lint <md> <json>`.

10. **SME Validate.** Follow `references/sme-validation.md`. Add to the checklist: every High finding has been read against its source by the SME, and no finding was dropped because it was inconvenient.

11. **Render** after validation with `scripts/render.py`.

## What a finding must not be

- A statement that the client is or is not compliant.
- A finding without a source in the inputs, or against a rule the client cannot act on yet.
- A finding based on what the reviewer expects a tool to do, rather than what the evidence shows.
- A duplicate: report a pattern once, and list every place it occurs.
