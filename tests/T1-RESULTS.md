# T1 model runs, v0.1.1

Run 22 and 23 November 2026. Each case was set up with `SETUP_ONLY=1 tools/run_skill_test.sh <skill> <case>` and run by a fresh Claude agent that read only the skill's own files and the case's engagement folder. Questions for the consultant were answered by the case prompt: the agent took its recommended option, recorded that, and left the deliverable a draft. Scores are from `tools/score.py` as it stands in v0.1.1, after the scoring fixes below.

| Skill | Case | Score | Notes |
|---|---|---|---|
| 20x-assessor-review | baseline | 5/5 | 29 findings |
| 20x-assessor-review | fedramp20x-findings | 11/11 | Re-run 23 Nov with git history kept: A4 found (F-017, past records changed after the fact). A6 found as "records only last_reviewed, with no reviewer"; the scorer now accepts "no reviewer". First run: 10/11, A4 missed because the runner deleted git history |
| 20x-assessor-review | seeded | 5/5 | |
| 20x-change-evaluation | baseline | 5/5 | CR-014 proposed adaptive |
| 20x-change-evaluation | seeded | 13/14 | CH-2 did not cite SCN-CSO-EVA; the skill now requires it on every evaluation item |
| 20x-incident-reporting | baseline | 4/4 | Found the PAIN timeframes in the rules data (see below) |
| 20x-incident-reporting | seeded | 6/6 | |
| 20x-package-builder | baseline | 5/5 | |
| 20x-policy-review | baseline | 10/10 | |
| 20x-policy-review | seeded | 8/8 | |
| 20x-sanity-check | baseline | 5/5 | |
| 20x-scope-review | baseline | 3/3, 1 must-not | N-01: reported resources with no category of their own. The M7 test now says this is an open question, not a finding |
| 20x-scope-review | seeded | 5/5 | |
| 20x-validator-build | baseline | 3/3 | 23 unit tests, 6 break tests, proposed Verified |
| 20x-validator-design | baseline | 4/4 | |
| 20x-validator-design | inr-rir | 5/5 | |
| 20x-validator-design | seeded | 3/3 | |

## Findings that changed the skills

- **Incident timeframes.** Two runs found that IEC-CSO-IIR, IEC-CSO-OIR and IEC-CSO-FIR carry `pain_timeframes` in the rules data, while the skill said FedRAMP sets no fixed hours. The skill, the timeline script and the example are corrected (CHANGELOG).
- **Choices made without the consultant.** All 13 runs that reported unclear points named this one. `method.md` now sets `unattended_choice` on the decision question and never writes it to `decisions.json`.
- **Scripts under `python -I`.** Every `build_report.py` failed under `-I`. A test now runs every script with `-I --help`.
- **Checking other skills' deliverables.** The assessor's `check_deliverable.py` checked them against its own template. It now uses the template of the skill that wrote the deliverable.
- **Smaller instruction fixes:** scope review M7 and the `scope` field; validator design method names and non-SCN triggers; change evaluation proposed type when an exclusion condition is unchecked, scope log change types, and client reviews the policy does not set; policy review coverage when only owner or record gaps exist; assessor stage reading for rules aimed at providers "seeking" certification; `frmr.py search` with unquoted words; `kmt_metrics.py --ksi` with several IDs; `frmr.py lint --client`; a folder as one input; `inventory.py` IDs with digits and table rows; local dates in `break_test.py`.

## Scoring fixes

Eight expectations were widened or narrowed after reading the run and the inputs:

| Case | ID | Change | Why |
|---|---|---|---|
| sanity-check baseline | E-03 | "affected" or "silent" | The run correctly classed the record as silent |
| package-builder baseline | E-05 | adds "no break test" | The run said exactly that |
| policy-review baseline | E-02 | one KSI per gap accepted | The run gave one gap per KSI instead of one grouped gap |
| scope-review baseline | N-02 | narrowed to "a TPR item is missing" | The run found a real contradiction: TPR-T3 says no alert identifiers reach the provider, but F16 and F18 carry D3, which includes the alert ID |
| scope-review baseline | E-03 | "evidence" accepted | The run listed every condition and its evidence state without quoting the example text |
| assessor fedramp20x-findings | A6 | "no reviewer field" and "no reviewer" accepted | Same finding, other words |
| change-evaluation seeded | all | `expect_per_change` is now scored | `score.py` ignored it before |
| validator-build baseline | N-01 | fails only a Verified proposal with a break test that did not fail | Before, it failed an honest report |
