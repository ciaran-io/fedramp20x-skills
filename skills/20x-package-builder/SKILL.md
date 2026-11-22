---
name: 20x-package-builder
description: Assemble FedRAMP 20x Class C Certification Package material from a client's scope, policies, validator designs, evidence history and decisions, and return Security Decision Record entries for each KSI, a draft Ongoing Certification Report and a package outline that shows what is ready and what is missing. Use when a consultant is preparing a client's package or a quarterly report.
---

# 20x package builder

Drafts the parts of the Certification Package that come from the client's own work, and shows the gaps. It never writes the independent assessor's parts: independent verification, independent validation and the overall summary of assessment come from a FedRAMP Recognized assessor and are left empty and labelled.

## Read first

- `references/method.md`, `references/sme-validation.md`, `references/writing-rules.md`, `references/lessons.md` (L1, L11)
- `references/engagement-folder.md`, `references/validator-design-template.md`
- `references/package-structure.md`: the parts of the package, the rules that define them, and where each piece comes from

## Inputs

| Input | Required | Notes |
|---|---|---|
| Scope record | Yes | For the overview's scope parts |
| Policies | Yes | For the relevant policies part |
| Validator designs and the latest results | Yes | For the KSI summaries |
| Daily validation history | Yes for metrics | One file per day. Without it, the metrics part is missing, not estimated |
| Decision log and earlier deliverables | Yes | `decisions.json` and the deliverables of the other skills |
| Changes, incidents, accepted vulnerabilities and agency list for the period | For the Ongoing Certification Report | From the client's records. A part with no record is stated as missing, not as "none" |
| The accountable official | For the overview metadata | Name, title and contact, from the client |

## Steps

1. **Set up.** Find the engagement folder. Register inputs. Run `python scripts/frmr.py info`. Read FRC-CSO-PKG, CPO-CSO-OVR, CPO-CSO-MTD, SDR-CSO-FRR, SDR-CSO-MTD, SDR-CSX-KSI, SDR-CSX-KMT and CCM-OCR-AVL with `python scripts/frmr.py show <ID>`. Ask the consultant which parts to draft now and the reporting period for the Ongoing Certification Report.

2. **Package outline.** For each part in `references/package-structure.md`, record whether the inputs supply it (`ready`, `partial`, `missing`, or `assessor` for parts only an assessor can supply), with the source. Do not mark a part ready because a file with the right name exists; read it.

3. **KSI summaries (SDR-CSX-KSI).** For each KSI with a design and a result, draft the summary items the rule lists, each from its source:
   - measures and their objectives: from the design's methods
   - the cycle for persistent measures: from the policy requirement (lesson L1)
   - verification that the measures demonstrate the KSI: from the design's gap; where the gap leaves part of the KSI unproven, say so (lesson L11)
   - verification of the automation: from the break tests and their status
   - validation that the measures work: from the latest result and the history
   A KSI with no design or no result gets an entry that says so and gives the reason and resulting risk only if the client has stated them; otherwise it is an open question.

4. **Metrics (SDR-CSX-KMT).** Run `python scripts/kmt_metrics.py <history folder> --as-of <date> [--ksi ...]`. Copy its summaries. Report the window, the days present and the missing days. Never fill a missing day.

5. **Rule entries (SDR-CSO-FRR).** Only when the consultant asks for them: for each applicable rule, draft the provider's explanation, verification and validation from the inputs. The independent verification and independent validation fields stay empty, labelled "assessor".

6. **Ongoing Certification Report (CCM-OCR-AVL).** For each item the rule lists, draft a short summary for the period from the client's records, with sources. "None in the period" is written only when a record shows there were none (for example the incident log for the period). An example report for an initial package is labelled as an example.

7. **Stop and ask.** Ask for the accountable official, the reporting period, any record that is missing, and the stated reason and risk for any KSI without measures. Record answers in `decisions.json`.

8. **Write the deliverable** in `deliverables/20x-package-builder/`: `<date>-package.json` following `templates/deliverable.json`, then `python scripts/build_report.py <json>`.

9. **Check** with `scripts/check_deliverable.py` and `scripts/frmr.py lint`.

10. **SME Validate.** Follow `references/sme-validation.md`. Add to the checklist: no assessor field is filled; every "ready" part was read; every metric matches the script output.

11. **Render** after validation with `scripts/render.py`. FedRAMP also requires JSON that validates against its schemas (FRC-CSO-JSN); this skill's JSON is a working format, not the FedRAMP schema. Say so when you hand it over.

## Must not

- Write, summarise or imply an independent assessment result.
- State that the package is complete or that the client is ready for certification.
- Estimate a metric, or turn missing history into a pass.
- Write "none" for an Ongoing Certification Report item without a record that shows none.
