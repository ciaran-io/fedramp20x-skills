# Validator design template

Used by `20x-validator-design` (to write designs), `20x-validator-build` (to build from them) and `20x-assessor-review` (to review them). One design per KSI.

| Field | Content |
|---|---|
| Requirement | What the KSI requires, in plain words, with the KSI ID. Do not copy the statement |
| Policy requirement | The client policy ID and requirement ID |
| Resource type | Machine-based or non-machine, and what the resource is |
| Validation cadence | How often the check runs, and the rule that sets the minimum (VDR-TFR-MVX for machine-based, VDR-TFR-NMV for non-machine) |
| Static method | Method ID. What declared state it reads (policy, infrastructure code, configuration file) and when it passes |
| Live method | Method ID. What observed state it reads (API, export, record) and when it passes |
| Change method | Optional. What event triggers a review, the deadline by change type, and how a pending review is shown |
| Fails when | Every condition that fails each method |
| Break test | For each method: the change made to prove it fails, and the message it gave. "Planned" until it is run |
| Production source | The real system or API the check reads for the client, named from the client's material |
| Gap | What the methods do not prove against the KSI |
| Status | Designed, Built or Verified |
| Decisions | Each choice made, with the option rejected and why, and the decision log ID |

## Status

| Status | Meaning |
|---|---|
| Designed | The design is written and SME-validated. No method exists yet |
| Built | At least two automated methods exist (FRC-CSX-VVK) |
| Verified | A break test made each method fail, and the result is recorded in the design |

## Roll-up of a KSI result

| Result | Meaning |
|---|---|
| pass | Two or more automated methods, all passing, no known gap against the KSI |
| partial | Passing, but fewer than two methods, or a known gap against the KSI |
| fail | At least one method fails |
| not_implemented | No automated method yet |

A coverage note never turns a partial into a pass (lesson L11).

## Design checks

A design is not ready for SME Validate until each of these holds:

1. The static and live methods read different sources, so one fault does not hide in both.
2. Every pass condition has a matching "fails when" condition.
3. Record ages are measured against the run date (lesson L3).
4. Review records are read as a list; the newest entry counts (lesson L4).
5. The reviewer is compared with the role the policy names (lesson L5).
6. A change method has a deadline for each change type and a "due by" note before it (lesson L6).
7. The production source is a real system named in the client's material, or a placeholder listed as an open question.
