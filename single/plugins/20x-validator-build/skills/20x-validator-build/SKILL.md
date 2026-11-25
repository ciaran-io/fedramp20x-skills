---
name: 20x-validator-build
description: Build the check code for an SME-validated FedRAMP 20x (Class A, B or C) validator design, with at least two automated methods, unit tests that fix the run date, and recorded break tests that prove each method can fail. Use when a consultant has an approved validator design and sample data and wants working checks.
---

# 20x validator build

Turns an approved design from `20x-validator-design` into code. A method is not evidence until a break test has made it fail (lesson L3), so this skill runs a break test for every method and records the message the method actually gave.

## Read first

- `references/method.md`, `references/sme-validation.md`, `references/lessons.md` (L3, L4, L5, L6, L11)
- `references/classes.md`: Class A, B and C differences; pass the client's class to every script
- `references/validator-design-template.md`
- `references/check-patterns.md`: the result format, run date, record lists, reviewer and deadline patterns
- `references/engagement-folder.md`

## Inputs

| Input | Required | Notes |
|---|---|---|
| The validator design | Yes | Status Designed or later, and SME-validated. If the design is a draft or has unconfirmed items, stop and say which; do not build from it |
| Sample data for every source the methods read | Yes | Real exports with client data removed, or files in the client's own format. Never invent a format; if a sample is missing, ask for it |
| Language and where the code will run | Ask | Python by default. Ask whether the client has a runner, a scheduler or a GRC tool the checks must fit |

## Steps

1. **Check the design.** Confirm it is SME-validated and lists at least two automated methods (`python scripts/frmr.py show FRC-CSX-VVK`). List any method whose source has no sample; stop and ask for the sample.

2. **Set up** in `deliverables/20x-validator-build/<ksi>/`. Register inputs. Copy `templates/check_template.py` and `templates/test_template.py` as a start.

3. **Write each method** as a function that takes the parsed inputs and the run date, and returns the result format in `references/check-patterns.md`. Implement every pass condition and every "fails when" condition in the design, one finding message per condition. Follow the patterns: ages against the run date, records as lists with the newest entry counting, reviewer compared with the policy owner, change deadlines with "due by" notes.

4. **Write the unit tests.** One test that the sample data passes as the design expects, and at least one test per "fails when" condition. Every test fixes the run date. Run them; all must pass.

5. **Run the break tests** in the design with `scripts/break_test.py`, one per method at least, and append each record to `break-tests.json`. Also run the check once with no change and confirm it passes. Use the observed message in the deliverable. If a method does not fail, it is a defect: fix the method, or report to the consultant that the method cannot fail in that way.

6. **Record the gap.** Copy the design's gap. If the code proves less than the design (for example a field is missing from the sample), add it to the gap and to the open questions.

7. **Propose the status.** Built when the methods exist and the unit tests pass. Verified only when every method has a break test that failed as required. The design's status changes only after SME Validate.

8. **Stop and ask** about anything the design or the samples leave open: an unclear field, a format the sample does not show, a timezone for dates. Record answers in `decisions.json`.

9. **Write the deliverable**: `<date>-<ksi>-validator-build.json` following `templates/deliverable.json`, then `python scripts/build_report.py <json>`. It lists each method, its tests, its break tests with the observed messages, and the proposed status.

10. **Check** with `scripts/check_deliverable.py` and `scripts/frmr.py lint` on the Markdown and JSON.

11. **SME Validate.** Follow `references/sme-validation.md`. The SME runs the tests and at least one break test themselves. Add to the checklist: every break test message in the deliverable matches `break-tests.json`.

12. **Hand over** the code, the tests, `break-tests.json` and the deliverable. Give the commands to run them. Render the report with `scripts/render.py` after validation.

## Must not

- Build from a design that is not SME-validated.
- Write a break test result that was not produced by running the check.
- Mark a method Verified without a break test that made it fail.
- Make a method pass by default when its source is empty or missing.
