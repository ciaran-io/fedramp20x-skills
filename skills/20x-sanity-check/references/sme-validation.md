# SME Validate step

The last step of every skill. The skill prepares the check; a person does it.

## What the skill does

1. Runs `scripts/check_deliverable.py <deliverable>.json` and `scripts/frmr.py lint <deliverable>.md <deliverable>.json`, and fixes every error.
2. Presents a validation pack to the consultant in the conversation:
   - the number of items, findings and recommendations, by rating where the skill rates them
   - every open question that is still unanswered
   - every item that rests on an inference the consultant has not confirmed, marked `confirmed: false` in the JSON
   - the checklist below
3. Asks the consultant who will validate it (name and role), and waits.
4. Applies the corrections the SME gives. Each correction is recorded in `sme_validation.corrections` with the item ID and what changed. An item the SME rejects is removed and recorded as rejected, not silently deleted.
5. Sets `sme_validation.status` to `validated` only when the consultant states that the validation is complete, with the SME's name, role and the date. Then renders the Word or Excel copy.

If the consultant ends the session first, the deliverable stays `draft`.

## Checklist for the SME

| # | Check |
|---|---|
| 1 | Each item cites a source, and the source says what the item says |
| 2 | No owner, cadence, deadline, tool, system or date appears that the client's material or a recorded decision does not contain |
| 3 | Each FedRAMP ID cited applies at Class C and is the right rule for the point made |
| 4 | Placeholders in square brackets are listed as open questions, not left as if final |
| 5 | Ratings follow `finding-ratings.md` and are consistent across items |
| 6 | Nothing reads as a statement that the client is compliant |
| 7 | Open questions are answered, or accepted as open with an owner and a date |
| 8 | The decisions recorded match what the consultant decided |

## How it is recorded in the JSON

```json
"sme_validation": {
  "status": "validated",
  "validated_by": "A. Example",
  "role": "Lead consultant",
  "date": "2026-11-22",
  "corrections": [
    {"item": "F-003", "change": "Rating lowered from High to Moderate: the tool does keep a log, shown in export X"}
  ],
  "rejected": []
}
```

In Markdown, the front matter carries `sme_validation: Validated by A. Example (Lead consultant) on 2026-11-22`, or `Draft: pending SME validation`.
