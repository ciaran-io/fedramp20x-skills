# Engagement folder and deliverable format

## Folder

The consultant keeps one folder per client engagement, outside the skills repository. Every skill reads from and writes to it.

```
<engagement>/
  engagement.json        client name, class, consultant, SMEs, FRMR commit
  decisions.json         decision log: entries are only added, never edited
  inputs/                client files as received; never edited by a skill
  deliverables/
    <skill>/
      <YYYY-MM-DD>-<name>.md     report for people (source of truth with the JSON)
      <YYYY-MM-DD>-<name>.json   the same content for tests and other skills
      <YYYY-MM-DD>-<name>.docx   Word copy for the client, rendered after SME Validate
      <YYYY-MM-DD>-<name>.xlsx   Excel copy of the tables, rendered after SME Validate
```

If `engagement.json` does not exist, the first skill run asks for the client name, the class (A, B or C), the consultant's name and the SME names, then creates it. Do not guess them. `stage` (preparing, applying or certified) is asked for by the first skill that needs it, usually the assessor review, and written back here; a later change of stage is also recorded in `decisions.json`. `fedramp_package_uri` (the Certification Package Overview URI) is added when the consultant gives it, for the FedRAMP JSON export.

```json
{
  "client": "Orrinwick Labs, Inc.",
  "offering": "Orrinwick Beacon",
  "class": "C",
  "consultant": "A. Example",
  "smes": [{"name": "B. Example", "role": "Cloud security architect", "areas": ["CNA", "SVC"]}],
  "frmr_commit": "64fa769510416fa75fd00a4689466094265b8083",
  "stage": "preparing"
}
```

A folder of records (for example a daily results history) is registered as one input with the folder's path; `check_deliverable.py --sha256 <folder>` hashes its file list and contents together. An input that is another skill's deliverable is registered with its path from the engagement folder, for example `deliverables/20x-scope-review/2026-11-22-scope-review.json`. `check_deliverable.py --inputs <engagement>/inputs` looks for an input's file in `inputs/` first and then in the engagement folder.

## Decision log

`decisions.json` holds every decision the consultant makes during the engagement. A skill adds an entry only after the consultant answers. A changed decision is a new entry that names the one it supersedes.

```json
{"decisions": [
  {
    "id": "D-001",
    "date": "2026-11-22",
    "question": "Is the support ticketing tool (S1) inside the boundary?",
    "options": ["In scope", "Excluded with conditions", "Excluded"],
    "recommended": "Excluded with conditions",
    "decided": "Excluded with conditions",
    "decided_by": "A. Example (consultant), confirmed with the client CISO",
    "reason": "Intake redaction keeps customer content out; evidence is the DLP test result each quarter",
    "skill": "20x-scope-review",
    "affects": ["S1", "MAS-CSO-IIR"],
    "supersedes": null
  }
]}
```

## Deliverable JSON

Every deliverable JSON has this envelope. `scripts/check_deliverable.py` checks it.

| Field | Content |
|---|---|
| `skill`, `skill_version` | The skill that produced it |
| `title`, `client`, `class`, `date` | Class is `A`, `B` or `C` (see `classes.md`) |
| `frmr_version`, `frmr_commit` | From `scripts/frmr.py info` |
| `inputs` | Each client file used: `id` (I-01), `file`, `sha256` (from `scripts/check_deliverable.py --sha256 <file>`, which ignores Windows and Unix line-ending differences in text files), `description` |
| `items` | The findings, rows or entries. Each has an `id`, `sources` and `confirmed` |
| `decisions_needed` | Each decision for the consultant: `id` (DQ-001, local to the deliverable), `question`, `options`, `recommendation`, `reason`, and `decision_ref`: the decision log ID (D-001) once decided |
| `open_questions` | Each question for an SME: `id`, `question`, `why`, `blocks` (item IDs), `answer` |
| `sme_validation` | See `sme-validation.md` |

Each entry in `sources` is one of:

```json
{"input": "I-01", "location": "INR-3"}
{"frmr": "KSI-INR-RIR"}
{"decision": "D-004"}      (decision log ID)
{"decision": "DQ-002"}     (a decision question in this deliverable, still open)
```

`confirmed` is `false` when the item rests on an inference the consultant has not yet confirmed. A deliverable cannot be validated while any item is unconfirmed or any open question that blocks an item is unanswered.

## Markdown front matter

```
---
title: KSI policy coverage review
client: Orrinwick Labs, Inc.
class: C (CR26)
frmr_version: 2026.11.02.01
date: 2026-11-22
prepared_by: Claude, for A. Example
sme_validation: Draft: pending SME validation
---
```
