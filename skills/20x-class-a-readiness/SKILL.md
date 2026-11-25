---
name: 20x-class-a-readiness
description: Check whether a cloud service provider is ready to seek FedRAMP 20x Class A certification, from its alternative framework certification (SOC 2 Type II, FedRAMP Rev5 or Ready, GovRAMP), the materials from that assessment, and its own policies, scope and package material, and return the framework and materials findings, a mapping of every mandatory Class A rule and KSI, and recommendations for the recommended and optional rules. Use when a consultant is preparing a client for Class A.
---

# 20x Class A readiness

Class A rests on a certification from an approved alternative security framework, plus a set of FedRAMP rules and KSIs that FedRAMP lists for Class A. This skill checks the certification and its materials, maps each mandatory rule and KSI to the client's material, and recommends action on the recommended and optional rules. It states what the evidence shows; it does not state that a client is ready or certified.

## Read first

- `references/method.md`, `references/sme-validation.md`, `references/writing-rules.md`, `references/finding-ratings.md`
- `references/classes.md`: Class A section; pass `--class a` to every script
- `references/engagement-folder.md`
- `references/class-a-tests.md`: tests R1 to R9 for this skill

## Inputs

| Input | Required | Notes |
|---|---|---|
| Alternative framework material | Yes | The report or certificate and the related materials (for SOC 2 Type II: the report, a bridge or gap letter, engagement documentation, the schedule of the next report). A summary the consultant writes is acceptable; list it as such |
| Planned submission date | Yes | Ask for it. The 12-month window in FRC-CLA-ASF counts back from when the client seeks certification |
| Client policies, scope record, plans, records | No | Used to map the mandatory rules and KSIs. Earlier deliverables of the other skills are inputs too |

## Steps

1. **Set up.** Find the engagement folder (`references/engagement-folder.md`), read `engagement.json` and `decisions.json`, and register each input with an ID and SHA-256. Run `python scripts/frmr.py info`. The deliverable's `class` is `A`. If `engagement.json` records another class, ask whether the client is moving to Class A before you continue.

2. **Read the Class A rules.** Run `python scripts/frmr.py rules --class a --affects Providers` and `python scripts/frmr.py ksis --class a`. Read FRC-CLA-ASF, FRC-CLA-EAM, FRC-CLA-MFR, FRC-CLA-RFR, FRC-CLA-OFR and FRC-CLA-IVV with `python scripts/frmr.py show <ID> --class a`. Cite the IDs; do not copy their text.

3. **Framework (tests R1 to R3).** Record one `framework` item: which framework, the date the certification or examination was completed, who assessed it, the period covered, whether an independent assessment was part of it, and whether the completion date falls within 12 months before the planned submission date. If the material does not show which date counts as completion (for example the end of a SOC 2 period or the report date), add a decision question and recommend one reading. A framework not on the FRC-CLA-ASF list is a High finding.

4. **Materials (tests R4 and R5).** For the framework found, list each material FRC-CLA-EAM names for it as a `material` item with status `present`, `partial` or `missing`, and the input that shows it. A missing MUST material is High. A material that exists but is out of date or covers less than the scope is Moderate.

5. **Scope match (test R6).** Compare the scope of the alternative framework assessment with the client's offering and scope record. A part of the offering outside the assessed scope is a finding against FRC-CLA-ASF and MAS-CSO-IIR.

6. **Mandatory mapping (test R7).** For each rule with `class_a_force` MUST, each rule in the FRC-CLA subset, and each KSI that FRC-CLA-MFR names, record a `mapping` item: status `mapped`, `partial`, `unmapped` or `not_reviewed`, what in the client's material (or the framework report) it maps to, and a rating for any shortfall. Use the timeframes and force at Class A, not Class C (for example `python scripts/incident_timeline.py --rating N --class a` for the incident reports). Use `not_reviewed` only when the inputs do not include the material, and add an open question for it. FRC-CLA-MFR requires the artifacts or mapping to be in the Certification Package; say where each mapping will sit.

7. **Recommended and optional rules (test R8).** For each rule with `class_a_force` SHOULD or MAY, record a `recommendation` item: what the client could do and what the material shows today. These are not gaps. FRC-CLA-IVV (optional independent verification) is a recommendation too.

8. **Stop and ask** with AskUserQuestion: the planned submission date if not given, any decision question, and each unanswered open question. Record the answers in the deliverable.

9. **Write the deliverable** in `deliverables/20x-class-a-readiness/`: `<date>-class-a-readiness.json` following `templates/deliverable.json`, then `python scripts/build_report.py <json>`.

10. **Check** with `python scripts/check_deliverable.py <json> --inputs <inputs folder> --decisions <decisions.json>` and `python scripts/frmr.py lint --class a <md> <json>` (test R9). Fix every error.

11. **SME Validate.** Follow `references/sme-validation.md`. Add to the checklist: the 12-month window was counted from the date the SME agrees is the completion date; every `mapped` item was read in the source, not inferred from a title.

12. **Render** after validation with `scripts/render.py`.

## Must not

- State that the client is ready, eligible or certified for Class A.
- Treat a SHOULD or MAY rule as a gap.
- Rate against Class C force or timeframes.
- Accept a framework certificate or report the inputs do not include. Record what is missing.
- Copy text from the alternative framework report beyond a short quote of a scope or opinion statement where the exact words matter.

## Related skills

- `20x-scope-review` for the scope record that test R6 compares against.
- `20x-package-builder` to place the Class A mapping in the Certification Package.
- `20x-assessor-review` to challenge the finished readiness work.
