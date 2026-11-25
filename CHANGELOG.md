# Changelog

## v0.2.0 (beta), 25 November 2026

Class A and Class B (v0.2 issue, items A1 to A6).

### New skill: `20x-class-a-readiness` (A4)

- Checks the alternative framework certification (FRC-CLA-ASF: framework on the list, completed within 12 months before the planned submission, when the window closes), the assessment materials (FRC-CLA-EAM), and whether the assessed scope covers the offering (MAS-CSO-IIR). Maps every mandatory rule and KSI that FRC-CLA-MFR names, with Class A force and timeframes, and gives recommendations, not gaps, for the FRC-CLA-RFR and FRC-CLA-OFR rules and FRC-CLA-IVV. Tests R1 to R9 in `references/class-a-tests.md`. It never states that a client is ready or certified.
- Worked example (A5): `examples/orrinwick/engagement/deliverables/20x-class-a-readiness/`, from an invented consultant's summary of a SOC 2 Type II report (`inputs/alternative-framework/soc2-type2-summary.md`). Test case `tests/20x-class-a-readiness/baseline` (5 expected findings, 2 must-nots); the example scores 5/5. No model run yet.

### Class A and B in the other skills

- **Class A rules (A1).** At Class A, FRC-CLA-MFR, FRC-CLA-RFR and FRC-CLA-OFR list the other rules and KSIs that apply, as MUST, SHOULD or MAY. `frmr.py rules --class a` now adds every listed rule, marked with `class_a_list` and `class_a_force`; `ksis --class a` marks the KSIs FRC-CLA-MFR names. Before, `rules --class a --affects Providers` found 29 rules; it now finds 57. `lint --class a` and `check_deliverable.py` use the same list.
- **Class setting (A2).** Every skill reads the class from `engagement.json` and passes it to the scripts. `check_deliverable.py` accepts Class A, B and C and checks rewrite sources against the deliverable's class. Report front matter states the deliverable's class (it said Class C on every report). `finding-ratings.md` rates against the force at the client's class. `incident_timeline.py --class` reads the PAIN timeframes for the class and reports each rule's force (`rule_force`); at Class A, IEC-CSO-IIR and IEC-CSO-OIR are SHOULD and IEC-CSO-FIR is MUST. `scn_timeline.py notices --class` stops when a notification rule does not apply at the class.
- **Class differences (A3).** New `frmr.py compare --class b --to c` lists, from the pinned data, the rules and KSIs at one class only, changed force and timeframes, rules whose statement text differs, and KSIs optional at the class. New reference `classes.md` (copied into every skill) covers Class B (12 rules change force or timeframe, own PAIN timeframes, 5 optional KSIs) and Class A (the three lists, 41 KSIs, FRC-CLA-ASF, FRC-CLA-EAM, FRC-CLA-IVV), and how to rate findings by class.
- **Lint by class (A6).** `frmr.py lint --class a|b|c` warns on IDs that do not apply at the class, including rules that apply at Class A only through FRC-CLA-MFR.
- **Placeholder check.** `check_deliverable.py` looked for `[placeholders]` in an item's JSON text, so a list of sources or criteria could raise a false warning (13 in the 23 November assessor re-run). It now reads string values only.
- Tests: Class A lists, the Class B comparison, lint at each class, the incident timeline at Class A, the class check, the placeholder check, the front matter class, and ten skills.
- Version 0.2.0 in every `plugin.json`.

## v0.1.1 (beta), 23 November 2026

Fixes from the first model test run on 22 November 2026.

### Installation

- The main marketplace now lists the full plugin only. The single-skill plugins moved to a second marketplace in the same repository, `single/.claude-plugin/marketplace.json` (named `fedramp20x-skills-single`), so a skill is no longer listed twice.
- Each single-skill plugin has its own folder, `single/plugins/<skill>/`, with a `plugin.json` whose name matches its marketplace entry. In v0.1.0 all nine entries pointed at the repository root, whose `plugin.json` is named `fedramp20x-skills`. Claude Code requires the two names to match.
- `tools/sync_shared.py` builds `single/` from `skills/` and the root `plugin.json`. `--check`, the repository tests and CI fail when a copy differs.
- Version 0.1.1 in every `plugin.json`. Claude Code installs a new copy only when the version changes, which is the likely reason a v0.1.0 install kept an older commit.
- The README gives the exact install and run commands for both marketplaces, and how to update.
- Each single-skill marketplace entry now uses the full HTTPS URL, `https://github.com/ciaran-io/fedramp20x-skills.git`, because the short form `ciaran-io/fedramp20x-skills` cloned over SSH and failed with "Host key verification failed".

### Incident reporting: FedRAMP timeframes

- v0.1.0 said the FedRAMP incident rules set no fixed hours. That was wrong: the rules data gives IEC-CSO-IIR, IEC-CSO-OIR and IEC-CSO-FIR a timeframe for each PAIN rating (`pain_timeframes`). `incident_timeline.py --rating N` now adds those timeframes from the pinned rules data and lists every plan target that falls later. New plan review test I12. The example evaluation of INC-2027-001 now shows that the plan's 24-hour ongoing reports and 5 business day final report are longer than the N5 timeframes. Found by the T1 model runs.

### T1 model runs

- All 17 test cases were run by fresh agents following the skills (`SETUP_ONLY=1` engagement folders). Results and the fixes they led to are in `tests/T1-RESULTS.md`.

### Policy review (S8)

- A rewrite states what a role must do, by when, and where it is recorded, and lists its `sources`. It never adds a fact about the environment to explain a requirement. `check_deliverable.py --inputs` reports a rewrite with no sources, and any number in a rewrite that is not in its current text or its sources.
- `scripts/inventory.py` drafts the requirement inventory: each requirement's exact text with candidate owner, cadence and record values found by pattern, for the model to confirm.
- `frmr.py ksis --statements` prints every KSI statement in one call.

### FedRAMP JSON export (J1 to J5, FRC-CSO-JSN)

- `scripts/fedramp_export.py` writes JSON valid against the FedRAMP schema a rule links: incident reports, significant change notifications, the Security Decision Record, the Ongoing Certification Report, the package overview and its third-party resources. It refuses a draft, a field the schema does not define, a null or placeholder value, an unsourced field and anything the schema rejects.
- The schemas (dated 2026-06-24, and the common definitions they reference) are pinned by SHA-256 and downloaded at run time, never committed. `FEDRAMP_SCHEMA_DIR` points at hand-saved copies where fedramp.gov is blocked.
- Export steps in the incident reporting, change evaluation, package builder and scope review skills; field maps in `references/fedramp-export.md`. The Orrinwick examples carry export blocks; tests check them against the schemas, run a test-only export and run six break tests. CI downloads the schemas; the monthly update check opens an issue when one changes.

### Checks and scripts

- `check_deliverable.py` checks every field the skill's template has, at the top level and per item kind, so `build_report.py` never stops on a missing field. `build_report.py` reports a missing field by name, and `--help` works. `check_deliverable.py --help` lists `--sha256`.
- `frmr.py lint` checks the text of a deliverable JSON (copied statement text, em dashes, compliance verdicts, banned words), not only the Markdown. Client text quoted in `text` and `current` is not treated as the deliverable's own words. A missing file is an error, not a traceback. `--ids-only` is for test case files.
- An input can be another skill's deliverable, registered by its path from the engagement folder.
- `kmt_metrics.py` reports the full 30 and 365 day windows, with the days before the history begins and a coverage line such as "covers 5 days, not 30".
- `scn_timeline.py` warns when a start, finish or count date falls on a weekend or holiday.
- `find_refs.py` takes `--include` and `--exclude` globs and counts hits per term. It prints paths with forward slashes on Windows too (a v0.1.0 bug that failed `test_find_refs` on Windows).
- `empty_probe.py` runs a client's checks with each input emptied and lists the methods that still pass.
- `tools/rehash_examples.py` updates the recorded hashes after an intended edit to an example.

### Skill instructions

- Assessor review: test R7 for KSIs that fail or are not implemented; R2 uses `empty_probe.py`; P6 lists every exercise a plan names and looks for its record; rules outside the stage table are decided by the trigger in their statement; the client's stage is written to `engagement.json` as `stage`; lint errors in client documents are rated by kind.
- Validator design: a design is Draft until SME validation, then Designed. The checker refuses another status on a draft. Validator build: an adapter pattern for client checks that read fixed paths.
- Scope review: test M8 runs the client's change check on changed copies of the record. Change evaluation: a change that rests on an exclusion condition is flagged before question 1.

### Test harness

- `tools/score.py` ignores case and spacing in phrases, accepts a list of alternatives for each phrase, and can match the whole deliverable (`"in": "document"`). The validator build must-not N-01 now fails only a deliverable proposed as Verified while a break test did not fail; before, it failed an honest report of a break test that did not fail.
- `tools/run_skill_test.sh` gives a case without its own inputs the example engagement's inputs and the other skills' example deliverables, clones fedramp20x at `31c11e5` for the findings case, refuses a used engagement folder, reads `prompt.txt` from the case, and has `SETUP_ONLY=1`. Each case has a `prompt.txt`.

### Documentation

- README: Windows PATH step for a first run of Claude Code, the folder trust prompt, what to do when an install fails, and the schema download.

## v0.1.0 (beta), 22 November 2026

First release. Class C (CR26) only.

**Status.** The scripts, examples and repository tests are complete and pass in CI. The skills have not yet been run end to end by a model against their seeded and fedramp20x test cases; that is the work for v0.1.1. Treat every output as a draft for SME validation, which is what the skills already require.

### Skills

| Skill | Deliverable |
|---|---|
| `20x-policy-review` | KSI coverage matrix, rated gaps, rewritten requirements |
| `20x-validator-design` | One validator design per KSI, with failure conditions and planned break tests |
| `20x-assessor-review` | Rated findings with observation, criteria and recommendation |
| `20x-scope-review` | Minimum Assessment Scope record or findings, boundary decisions, exclusion conditions |
| `20x-change-evaluation` | Change type, notice dates from the rules data, scope log entry, client review deadline |
| `20x-sanity-check` | Where a decision applies, what disagrees, follow-ups to approve |
| `20x-validator-build` | Check code, unit tests, recorded break tests |
| `20x-incident-reporting` | Reportability, PAIN rating, timeline from the reportability decision, report content |
| `20x-package-builder` | Package outline, KSI summaries and metrics, draft Ongoing Certification Report |

### Built in to every skill

- Never make anything up: every item cites a client file and location, a FedRAMP ID or a recorded decision. `check_deliverable.py` rejects items without a source.
- Stop and ask when SME input is needed.
- SME Validate as the last step. A deliverable stays a draft until a named SME validates it.
- FedRAMP rules read at run time from a pinned commit, with hash checks. `frmr.py lint` reports unknown IDs, copied statement text, em dashes and compliance verdicts.
- Word and Excel copies of each deliverable.

### Decisions in this release

- Business days skip US federal holidays on their observed dates by default. FedRAMP does not define business days, so each deliverable records the basis for the consultant to confirm.
- A monthly workflow opens an issue when FedRAMP/rules moves past the pinned commit.
- Install the full set or one skill at a time (Claude Code marketplace), or upload the per-skill zip files to claude.ai.

### Known limits

- Class C only. Classes A and B are planned for v0.2.
- Seeded and fedramp20x test cases need a model run (`tools/run_skill_test.sh`).
- The skills' JSON is a working format, not FedRAMP's package schema (FRC-CSO-JSN).
