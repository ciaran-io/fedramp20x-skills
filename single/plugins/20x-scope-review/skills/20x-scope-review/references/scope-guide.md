# Scope guide

## Decision values

| Value | Meaning | Needs |
|---|---|---|
| `in_scope` | Part of the cloud service offering (MAS-CSO-IIR) | A reason: it handles federal customer data, or it can affect its confidentiality, integrity or availability |
| `third_party` | Used by the offering but run by another company (FRD-TPR) | The information MAS-CSO-TPR lists |
| `out_conditional` | Outside only while named conditions hold | Each condition: text, evidence, owner, cadence, record location (lesson L10) |
| `out_of_scope` | Neither handles federal customer data nor can affect it | A reason that states both |
| `supplement` | Described in a package supplement, not certified (MAS-CSO-SUP) | Clearly marked and separated |
| `undecided` | The consultant has not decided | An open decision in the deliverable |

## Record fields

| Section | Fields |
|---|---|
| Data classes | id, name, federal customer data (yes, no, mixed, metadata), basis, security category as the client set it |
| Resources | id, name, kind (machine-based, non-machine), zone, handles (data class IDs), impact on federal customer data, decision, rationale, conditions |
| Flows | id, source, destination, data classes, protocol, authentication, encryption in transit, crosses boundary (yes or no) |
| Prohibited flows | id, from, to, data classes, the control that prevents it, evidence |
| Third parties | id, resource, the items MAS-CSO-TPR lists, authorization status only if the client states it with a source |
| Metadata | metadata about federal customer data included under MAS-CSO-MDI, and where it is stored |
| Conditions | id, resource, text, evidence, owner, cadence, record location, check that reads the evidence |

## Tests for review mode

| Test | Finding when | Usual rating | Lesson |
|---|---|---|---|
| M1 Completeness | A system in the inventory or diagrams is missing from the record | High if it handles federal customer data, otherwise Moderate | |
| M2 Rationale | A decision has no reason, or the reason does not address both handling and impact | Low to Moderate | |
| M3 Conditions | An exclusion condition has no evidence, or no owner, cadence or record for checking it, or no check reads the evidence | Moderate | L10 |
| M4 Flows | A data class has no flow, a flow ends at a resource with no decision, or a flow crosses the boundary with no stated protection | Moderate | |
| M5 Third parties | A third party lacks any item MAS-CSO-TPR lists | Moderate | |
| M6 Metadata | Provider metadata about federal customer data leaves the in-scope resources with no MAS-CSO-MDI entry | Moderate | |
| M7 Categories | A data class has no security category, or a category the client did not set. A resource with no category of its own is not a finding when the data classes it handles have categories: the usual rule is that a resource takes the highest category of its data classes. If the record or its tooling states no rule, ask the consultant to confirm that one as an open question; do not report it as a finding | Low; ask | |
| M8 Change log | The record changed with no change log entry, or the change log check, run on a changed copy, does not detect a change to a decision, condition, flow or third party | Moderate | L3, L7 |
| M9 Open questions | The record says decided while an open question is unresolved, or a decision has no recorded owner | Low | |
| M10 Status | The record is a draft while other work relies on it | Observation | |
