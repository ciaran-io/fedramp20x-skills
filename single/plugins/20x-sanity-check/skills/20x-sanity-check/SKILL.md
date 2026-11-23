---
name: 20x-sanity-check
description: After a FedRAMP 20x decision or change is made, find every other document, record, check or deliverable it applies to, list the ones that now disagree with it, and draft the follow-up items for approval. Use right after a consultant or client decides something (an owner, a cycle, a scope decision, a rewrite adopted) so nothing is left inconsistent.
---

# 20x sanity check

A decision made in one document usually applies in others: the policy, the plan, the records a check reads, the validator design, the scope record, earlier deliverables. This skill finds each place, states whether it agrees, and drafts follow-up items. It changes nothing itself; the consultant approves each follow-up.

## Read first

- `references/method.md`, `references/sme-validation.md`, `references/writing-rules.md`, `references/lessons.md` (L9, L12)
- `references/engagement-folder.md`
- `references/where-decisions-land.md`: the places to search for each kind of decision

## Inputs

| Input | Required | Notes |
|---|---|---|
| The decision or change | Yes | Its decision log ID, or the text the consultant gives. If it is not in `decisions.json`, ask whether to record it first |
| The document set | Yes | The engagement inputs and deliverables, and any client folder the consultant names |

## Steps

1. **Set up.** Find the engagement folder and read `decisions.json`. Register inputs. Run `python scripts/frmr.py info`.

2. **State the decision** in one sentence, and break it into its elements: IDs it concerns, the value it sets (owner, cycle, deadline, record location, decision value), and the old value it replaces where known. Each element cites the decision log entry.

3. **Choose search terms** from `references/where-decisions-land.md`: the IDs, the old and new values in the forms documents use (for example "every quarter", "quarterly", "90 days"), role names, and the names of related KSIs and rules.

4. **Search.** Run `python scripts/find_refs.py <folder> <term> [<term> ...] --context 1` on each folder in the document set. Read each hit in its document. A search term can miss a paraphrase, so also read the sections that `references/where-decisions-land.md` lists for this kind of decision.

5. **Classify each place**:

   | Status | Meaning |
   |---|---|
   | agrees | States the decided value |
   | disagrees | States a different value. Quote the location, not the full text |
   | silent | Should state it (by `where-decisions-land.md`) but does not |
   | affected | Does not state the value but depends on it: a check, a design, an open question or decision question in a deliverable |

   Every status rests on what the document says at that location. If a place is ambiguous, ask the SME.

6. **Draft follow-ups.** One item per place that disagrees, is silent or is affected: what to change, where, and who approves it (from the decision or the policy owner). Mark each item `proposed`. Do not edit any client document.

7. **Check rule IDs.** Run `python scripts/frmr.py lint --client` on the documents that the decision touches. A cited ID that is unknown or out of scope is a follow-up (lesson L12).

8. **Stop and ask.** Present the follow-ups with AskUserQuestion, grouped by owner, and ask which to approve. Record approvals in the deliverable; do not record them as done until the consultant says the change was made.

9. **Write the deliverable** in `deliverables/20x-sanity-check/`: `<date>-<decision-id>-sanity-check.json` following `templates/deliverable.json`, then `python scripts/build_report.py <json>`.

10. **Check** with `scripts/check_deliverable.py` and `scripts/frmr.py lint`.

11. **SME Validate.** Follow `references/sme-validation.md`. Add to the checklist: every "agrees" was read in the document, not inferred from the search hit alone.

12. **Render** after validation with `scripts/render.py`.

## Must not

- Edit a document. This skill lists and drafts; people change documents.
- Mark a place as agreeing because it was not found by a search.
- Add a follow-up that does not trace to the decision.
