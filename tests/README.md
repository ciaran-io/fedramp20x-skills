# Tests

Each skill has a folder here with sample inputs and the findings the skill must report. A skill passes when its output reports every expected finding and no finding that the inputs do not support.

Each test set has two parts:

1. **Baseline.** The Orrinwick inputs, compared with the outputs already reviewed in fedramp20x.
2. **Seeded faults.** Copies of the inputs with known faults added, such as a policy requirement with no owner, a review recorded by the wrong role, or a change with no change type. `expected-findings.md` lists each fault and the rule or KSI ID the finding must cite.
