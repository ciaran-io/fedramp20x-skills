# Orrinwick Labs example engagement

> **FICTIONAL.** Orrinwick Labs, Inc., the Orrinwick Beacon service, the agencies, the consultant (A. Example) and the change and incident records are invented. No real client data is stored in this repository.

`engagement/` is laid out the way the skills expect (see `shared/references/engagement-folder.md`). The inputs come from [fedramp20x](https://github.com/ciaran-io/fedramp20x), plus three invented client records: change request CR-014, incident INC-2027-001 and one example decision (D-001). Every deliverable is a **draft pending SME validation**. Each one has Markdown and JSON (the sources of truth) and Word and Excel copies.

| Skill | Deliverable | What it found in the Orrinwick material |
|---|---|---|
| `20x-policy-review` | `deliverables/20x-policy-review/2026-11-22-policy-review` | 14 gaps across POL-INR, POL-CNA, POL-RPL and POL-CMT; 2 of 19 KSIs fully covered; CMT-7 cites FRC-CCL rules that apply to Rev5 only |
| `20x-validator-design` | `deliverables/20x-validator-design/2026-11-22-validator-design` | Designs for KSI-INR-RPI and KSI-INR-AAR; the policy and the plan disagree on the review cycle and owner |
| `20x-assessor-review` | `deliverables/20x-assessor-review/2026-11-22-assessor-review` | 28 KSIs report pass while their coverage notes describe a gap; a past review record was edited; a method has no break test |
| `20x-scope-review` | `deliverables/20x-scope-review/2026-11-22-scope-review` | 10 exclusion conditions have no owner, cycle or check; the scope change check cannot see a changed condition |
| `20x-change-evaluation` | `deliverables/20x-change-evaluation/2026-11-22-CR-014-change-evaluation` | CR-014 proposed as transformative; notice dates from the rules data; the final plans notice falls on a federal holiday if holidays are not skipped |
| `20x-sanity-check` | `deliverables/20x-sanity-check/2026-11-22-D-001-sanity-check` | Where decision D-001 (past incident review every 90 days, by the Security Operations Lead) applies: 3 places disagree, 1 is silent, 4 are affected |
| `20x-validator-build` | `deliverables/20x-validator-build/` | KSI-INR-RIR checks as portable code, 9 unit tests and 4 break tests that each made a method fail |
| `20x-incident-reporting` | `deliverables/20x-incident-reporting/2027-01-12-INC-2027-001-incident-reporting` | Reportable (responder contact data); N5 in force until the CISO approves an estimate; timeline from the plan's targets |
| `20x-package-builder` | `deliverables/20x-package-builder/2026-11-22-package` | Package outline (5 parts missing, 5 partial, 2 for the assessor), KSI summaries for 3 KSIs, metrics from 5 days of history, an example Ongoing Certification Report |
