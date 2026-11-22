# Method and ground rules

Every skill in fedramp20x-skills follows these rules. They take priority over the steps in a skill when the two disagree.

## 1. Never make anything up

Every statement in a deliverable must trace to one of three sources:

| Source | How it is cited |
|---|---|
| A file the consultant provided | File name and location: section, requirement ID, row, line or page |
| The FedRAMP rules data | The rule, KSI or definition ID, read with `scripts/frmr.py` |
| A decision the consultant recorded | The decision ID in the engagement decision log (`D-001`) |

If none of these supports a statement, the statement does not go in the deliverable. In particular, do not:

- invent an owner, a cadence, a deadline, a tool, a system name, a record location or a date
- assume what a client tool does, how it is configured or what it logs
- fill a gap in the client's material with what a typical provider would do
- state a rule's timeframe, force or applicability from memory; read it with `scripts/frmr.py show <ID>`
- state that no rule covers something until `scripts/frmr.py search <words>` has searched every field (statements, following information and notes)
- cite a rule or KSI ID that `scripts/frmr.py lint` reports as unknown or not applicable at Class C

When the material is silent, say so: "The policy names no owner for this review." A gap is a finding, not a blank to fill.

Recommended text (for example a rewritten policy requirement) is allowed, because it is marked as a recommendation for the client to adopt. Any owner, cadence or record location in recommended text that the client has not given is written as a placeholder in square brackets, such as `[owner: client to confirm]`, and listed as an open question.

## 2. Stop and ask when SME input is needed

Stop and ask the consultant before continuing when a step needs any of the following:

- a scope or boundary decision, or a decision to accept a risk
- the meaning of a client term, system or record that the material does not explain
- how a client tool works, what it records, or where its records are kept
- an owner, cadence, deadline or threshold the client has not set
- a choice between two readings of a FedRAMP rule that change the result
- confirmation that an inferred link (for example "this ticket queue is the incident tracker") is correct

Ask with the AskUserQuestion tool when it is available, otherwise in plain text. Each question names what was found, why the answer matters, and the options, with one recommended option and the reason. Ask related questions together, at most four at a time. Do not carry on with a guess. If the consultant is not available, stop at the last step that needs no answer, record the open questions in the deliverable, and leave its status as draft.

## 3. SME Validate before a deliverable is final

The last step of every skill is SME Validate. The consultant, or a subject matter expert the consultant names, checks the draft against its sources. A deliverable has one of two statuses:

| Status | Meaning |
|---|---|
| `draft` | Written by the skill. Not yet checked by an SME. Every Markdown, Word and Excel copy shows "Draft: pending SME validation" |
| `validated` | An SME checked each item against its sources and the open questions are closed. The deliverable records who validated it, their role and the date |

The skill never sets `validated` itself. It sets it only when the consultant states, in the conversation, the name and role of the SME and that the validation is complete. See `sme-validation.md` for the checklist.

## 4. The working method

1. Scope comes first. Do not review policies or design checks for resources whose scope is not settled.
2. Policies are reviewed against the KSIs. Each requirement names an owner, a cadence or deadline, and where the record is kept.
3. Each KSI check has a written design that states every way it fails.
4. Each method in a check is proven able to fail by a recorded break test.
5. Finished work gets an assessor's review.
6. After each decision or change, a sanity check finds every other place it applies.

## 5. Other ground rules

- **Official data at run time.** Read rules with `scripts/frmr.py`. Cite IDs. Do not copy statement text into deliverables; describe the requirement in plain words. `scripts/frmr.py lint` flags copied text.
- **Class C (CR26) only** in version 1. State the class in every deliverable.
- **No compliance verdicts.** Say what the evidence shows and where it falls short. Never write that a client is compliant, meets all requirements or has achieved compliance.
- **The consultant decides.** Draft, list the decisions needed and recommend one option for each. Do not make scope or risk decisions.
- **Client data stays local.** Work only on the files the consultant provides. Do not send client material to any other service, and do not put it in the skills repository.
- **Writing.** Follow `writing-rules.md`.
