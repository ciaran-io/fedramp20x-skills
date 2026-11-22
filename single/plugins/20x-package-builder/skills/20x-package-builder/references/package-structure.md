# Package structure

Read each rule with `frmr.py show <ID>` for the full list of items it requires. This page maps the parts to their sources in an engagement.

| Part | Rule | Usual source in the engagement | Who supplies it |
|---|---|---|---|
| Certification Package | FRC-CSO-PKG | All parts below | Provider |
| Certification Package Overview | CPO-CSO-OVR | The parts listed in the rule | Provider |
| Overview metadata: accountable official, version, date and time of last update, source of update | CPO-CSO-MTD | The client | Provider |
| Public information and service list | CDS-CSO-PUB, CDS-CSO-SVC | The client's public material | Provider |
| Relevant policies | CDS-CSO-IRP | The policies, after `20x-policy-review` | Provider |
| Scope: resources, flows and categories, third parties | MAS-CSO-IIR, MAS-CSO-FLO, MAS-CSO-TPR | The scope record, after `20x-scope-review` | Provider |
| Cryptographic module documentation | CMU-CSO-CMD | The client's module list | Provider |
| Independent assessment in the package | IVV-CSO-ICP | The assessor | Assessor |
| Overall summary of assessment | CPO-CSO-OSA | The assessor | Assessor |
| Security Decision Record, per rule | SDR-CSO-FRR | Policies, designs, results, decisions | Provider, with independent fields from the assessor |
| Security Decision Record metadata | SDR-CSO-MTD | The deliverable itself | Provider |
| KSI summaries | SDR-CSX-KSI | Validator designs, results, policy cycles | Provider |
| KSI metrics | SDR-CSX-KMT | Daily validation history, via `kmt_metrics.py` | Provider |
| Ongoing Certification Report | CCM-OCR-AVL | The period's change log, incident log, vulnerability records, agency list | Provider |
| JSON valid against FedRAMP schemas | FRC-CSO-JSN | Not produced by this skill | Provider |
| Package kept up to date | CPO-CSX-CPM | A cycle the client sets within the rule's timeframe | Provider |

## Status values for the outline

| Status | Meaning |
|---|---|
| ready | The inputs contain the part and it was read |
| partial | Some required items are present; the missing items are listed |
| missing | No input contains it |
| assessor | Only an assessor can supply it. Never drafted |
