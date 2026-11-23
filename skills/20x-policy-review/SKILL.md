---
name: 20x-policy-review
description: Review a cloud service provider's security policies against every FedRAMP 20x Class C Key Security Indicator and return a KSI coverage matrix, rated gaps and rewritten requirement text with an owner, cadence and record location. Use when a consultant gives you a client's policies to review for FedRAMP 20x.
---

# 20x policy review

Reviews a client's policies against all KSIs that apply at Class C (CR26). The deliverable shows which policy requirement covers each KSI, where a requirement falls short, and the rewritten text the client could adopt.

## Read first

Read these before step 1. They override the steps below where they differ.

- `references/method.md`: never make anything up, stop and ask, SME Validate
- `references/sme-validation.md`
- `references/writing-rules.md`
- `references/lessons.md`
- `references/engagement-folder.md`
- `references/finding-ratings.md`
- `references/policy-tests.md`: the tests applied to each requirement in step 5

Scripts are in `scripts/` in this skill's folder. `scripts/frmr.py` needs Python 3.10 or newer and downloads the FedRAMP rules data on first use.

## Inputs

| Input | Required | Notes |
|---|---|---|
| The client's policies | Yes | Any format: Markdown, Word, PDF, JSON. All policies, not a sample, if the coverage matrix is to be complete |
| Documents the policies reference | When available | Plans, procedures, standards. Needed for test T6 |
| Scope record or asset list | Optional | Lets the review check that the resources a policy names exist |
| Engagement folder | Yes | Ask for its path. See `references/engagement-folder.md` |

If no policies are given, stop and ask for them. If a policy refers to a document that is not provided, continue, and list the document as an open question.

## Steps

1. **Set up.** Find or create `engagement.json` (ask for any field that is missing; do not guess). Copy nothing out of the engagement folder. Run `python scripts/frmr.py info` and record the FRMR version and commit. Give each input an ID (I-01, I-02) and record its SHA-256.

2. **Load the KSIs.** Run `python scripts/frmr.py ksis --statements`. Every KSI in the output appears in the coverage matrix. Read each statement there (or with `python scripts/frmr.py show <KSI-ID>`), and read each term it lists (for example `python scripts/frmr.py term persistently`). Do not copy statement text into the deliverable.

3. **Build the requirement inventory.** Start with `python scripts/inventory.py <policy files> --role <each role the client names> --out <engagement>/deliverables/20x-policy-review/work/inventory.json`. It lists each requirement with its exact text and candidate values found by pattern. Candidates are not answers: confirm or correct each one against the text, and read anything listed under `unsplit`. For each policy, list every requirement with its policy ID, requirement ID and the client's exact text. If the client gives no requirement IDs, number them (POL-X/R1) and tell the consultant. For each requirement, record the three elements as the text states them:
   - owner (the role that does it and records it)
   - cadence or deadline
   - record location

   Record "not stated" when the text does not state it. Do not fill it in from the policy header, from another policy or from what is typical. If the policy header names an owner and the requirement names none, ask the consultant once for the whole set whether the header owner owns every requirement that names no actor (step 7). Until answered, those items have `confirmed: false`.

4. **Map requirements to KSIs.** For each KSI, list the requirements that address it, using the client's own KSI mapping where one exists and the requirement text otherwise. Give each KSI one coverage value:

   | Coverage | Meaning |
   |---|---|
   | covered | At least one requirement addresses every part of the KSI and passes tests T2, T4 and T5 (gaps under T1 and T3 are listed separately) |
   | partial | A requirement addresses the KSI, but part of the KSI is not addressed, or a test other than T1 (owner) or T3 (record) fails. A missing owner or record location is a gap of its own and does not lower coverage |
   | not covered | No requirement in the policies provided addresses the KSI |
   | not reviewed | The policy that would cover it was not provided. Say which theme |

   A client mapping that names a KSI the requirement does not address is a gap (test T7). A requirement that addresses a KSI the client did not map is noted, not counted against the client.

5. **Apply the tests.** Apply tests T1 to T10 in `references/policy-tests.md` to each requirement and record each failure as a gap with an ID (G-001), the requirement, the test, the criteria (KSI or rule ID plus the client requirement), the rating from `references/finding-ratings.md`, and its sources. Run `python scripts/frmr.py lint` on a text file of the policies to find cited FedRAMP IDs that do not exist or do not apply at Class C (test T8).

6. **Draft rewritten text.** For each gap that a change of wording would close, draft the requirement as the client could adopt it. Keep the client's requirement ID. A rewrite states what a role must do, by when, and where it is recorded. It does not describe how a system behaves.
   - Use only owners, cadences, deadlines, numbers, system names and record locations that the client's material or a recorded decision states. List each source on the rewrite (`sources`, same form as an item's sources).
   - Where one is missing, write a placeholder such as `[owner: client to confirm]` and add an open question. Never invent a system name, a record location or a number.
   - Do not add a fact about the environment to explain the requirement (for example that a lock prevents deletion, or that staging holds no customer data). If the requirement depends on such a fact, it is a placeholder or an open question, even when one input seems to show it: a setting on one resource is not true of all of them.
   - Before you finish, read each rewrite against its sources. Every number and every named thing in `recommended` must appear in `current` or in a listed source. `check_deliverable.py --inputs` reports a number that does not.
   - Group a fix that applies to several requirements (for example one review cycle for several KSIs) as one decision for the consultant.

7. **Stop and ask.** Collect the decisions and open questions. Ask the consultant with AskUserQuestion, at most four at a time, each with the options and a recommended option. Typical questions:
   - Does the policy header owner own every requirement that names no actor?
   - What does a referenced document (plan, procedure) say, or can it be provided?
   - Which cycle does the client run for a "persistently" activity that the policy does not state?
   - Is a cited rule meant for a different program type or class?

   Record each answer in `decisions.json` as a new entry. Update the affected items and set `confirmed: true` only where the answer confirms them. Do not continue past a question whose answer changes a rating or a rewrite.

8. **Write the deliverable** in `deliverables/20x-policy-review/`:
   - write `<date>-policy-review.json` following `templates/deliverable.json`. `items` holds the gaps; `coverage` holds one row for every KSI; `requirements` holds the inventory
   - run `python scripts/build_report.py <date>-policy-review.json`. It writes the Markdown report (layout in `templates/report.md`) and `<date>-policy-review-tables.json` for the Excel copy. Do not edit the Markdown by hand; change the JSON and rebuild

9. **Check.** Run `python scripts/check_deliverable.py <json> --inputs <engagement>/inputs --decisions <engagement>/decisions.json` and `python scripts/frmr.py lint <md> <json>`. Fix every error before step 10.

10. **SME Validate.** Follow `references/sme-validation.md`. Present the validation pack: counts by rating, the KSIs not covered, every unconfirmed item, every open question. Ask who validates. Apply corrections. Set the status to validated only when the consultant confirms it with the SME's name, role and the date.

11. **Render.** After validation, run `python scripts/render.py docx <md> <docx>` and `python scripts/render.py xlsx <tables.json> <xlsx>`. If the consultant asks for a copy before validation, render it; the copy shows "Draft: pending SME validation".

## What the deliverable must not contain

- A statement that the client is compliant, or that a KSI is "met". Use the coverage values above.
- An owner, cadence, deadline, record location, tool or system that the client's material or a recorded decision does not contain.
- FedRAMP statement text.
- Findings on KSIs whose policies were not provided. Mark them "not reviewed".

## Related skills

- `20x-validator-design` takes the reviewed requirements and designs a check for each KSI.
- `20x-assessor-review` reviews this deliverable.
- `20x-sanity-check` runs after the client adopts a rewrite, to find other documents that now disagree.
