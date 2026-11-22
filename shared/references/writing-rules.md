# Writing rules for deliverables

These rules apply to every client deliverable. A client's own template takes priority where it sets different rules.

## Language

- Formal, plain English. Short sentences. One point per sentence.
- No em dashes.
- No introductions that describe what the document will do, and no conclusions that repeat it.
- No "not X, but Y" contrast sentences. State the point.
- No benefit statement at the end of each paragraph or section.
- No groups of three used for rhythm.
- No hedge stacks such as "may potentially", "could possibly" or "generally tends to".
- Do not use: delve, leverage, robust, seamless, comprehensive, crucial, holistic, navigate, landscape, streamline, foster, underscore, additionally, furthermore, moreover. The words are allowed in quoted text and in official names.
- Do not use: "It is important to note", "It should be noted", "In today's landscape", "plays a critical role", "This ensures that".

`scripts/frmr.py lint` reports em dashes and the listed words and phrases.

## FedRAMP content

- Cite rule, KSI and definition IDs, for example KSI-INR-RIR, VDR-TFR-NMV, FRD-PER.
- Describe what a rule requires in plain words. Do not copy statement text. A short quotation is allowed only where the exact words decide the point, in quotation marks, with the ID.
- State the class: "Class C (CR26)".
- Never state that the client is compliant. Write what the evidence shows and where it falls short.

## Requirements

A requirement that a deliverable recommends names all three of:

| Element | Example |
|---|---|
| Owner | The role that does the activity and records it (Platform Lead) |
| Cadence or deadline | Every 90 days; within 10 business days after a failed change |
| Record location | Where the record is kept (the GRC tool, change ticket, file path) |

If the client has not given one of these, write a placeholder in square brackets and list it as an open question.

## Tables and IDs

- Each finding, gap, decision and open question has a stable ID within the deliverable (F-001, G-001, DQ-001, Q-001).
- Keep the client's own IDs (policy and requirement IDs) unchanged.
