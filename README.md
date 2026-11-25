# FedRAMP 20x consultant skills

> **NOT ADVICE.** These skills are a learning and portfolio project. They are **not** a FedRAMP assessment, certification or legal advice. A skill's output says what the evidence shows and where it falls short. It never says that a client is compliant. All examples use Orrinwick Labs, Inc., a fictional company.

Claude skills for a consultant who reviews a cloud service provider's FedRAMP 20x Class A, B or C program. Each skill takes the client's own material (policies, plans, scope records, records exports, change and incident records, validation history) and returns a draft deliverable in Markdown, JSON, Word and Excel. Every finding cites a FedRAMP rule or Key Security Indicator (KSI) ID and the client source it rests on.

The skills apply the method from [fedramp20x](https://github.com/ciaran-io/fedramp20x), a worked Class C example:

- the scope is settled before anything else
- policies are reviewed against the KSIs, and each requirement names an owner, a cadence or deadline, and where the record is kept
- each KSI check has a written design that states how it fails
- each check is proven able to fail by a recorded break test
- finished work gets an assessor's review
- each decision gets a sanity check for the other places it applies

## Skills

| Skill | Use it to | Deliverable |
|---|---|---|
| `20x-policy-review` | Review policies against every KSI at the client's class (46 at Class C) | Coverage matrix, rated gaps, rewritten requirements |
| `20x-validator-design` | Design how a KSI will be checked | One design per KSI: methods, how each fails, planned break tests, gaps |
| `20x-assessor-review` | Challenge finished work as an assessor would | Findings with observation, criteria, rating and recommendation |
| `20x-scope-review` | Build or review the Minimum Assessment Scope | Scope record or findings, boundary decisions, exclusion conditions and their evidence |
| `20x-change-evaluation` | Evaluate a change | Change type, notice dates from the rules data, scope log entry, the client's review deadline |
| `20x-sanity-check` | Follow a decision through every document | Places that agree, disagree, are silent or are affected, and follow-ups to approve |
| `20x-class-a-readiness` | Check readiness for Class A | Alternative framework and materials findings (FRC-CLA-ASF, FRC-CLA-EAM), a mapping of every mandatory Class A rule and KSI, recommendations for the recommended and optional rules |
| `20x-validator-build` | Build checks from an approved design | Code, unit tests and break test records |
| `20x-incident-reporting` | Evaluate an incident or review an incident response plan | Reportability, PAIN rating, timeline from the reportability decision, report content |
| `20x-package-builder` | Prepare Certification Package material | Package outline, KSI summaries and metrics, a draft Ongoing Certification Report |

**Status: v0.2.0 beta.** All ten skills are built, each with a worked example, and the repository tests pass. The nine v0.1 skills were run by a model against their test cases in v0.1.1 (`tests/T1-RESULTS.md`); `20x-class-a-readiness` has not yet had a model run (see [`CHANGELOG.md`](CHANGELOG.md)).

## Rules every skill follows

- **Never make anything up.** Every statement in a deliverable traces to a client file and location, a FedRAMP ID, or a decision the consultant recorded. When the client's material is silent, the deliverable says so, or writes a placeholder such as `[owner: client to confirm]` and lists an open question. `scripts/check_deliverable.py` fails any item without a source.
- **Stop and ask.** A skill stops and asks the consultant when it needs a scope or risk decision, the meaning of a client term, how a client tool works, an owner or cadence the client has not set, or a choice between two readings of a rule. It does not carry on with a guess.
- **SME Validate.** The last step of every skill. The consultant or a subject matter expert they name checks each item against its source. Until then, every copy is marked "Draft: pending SME validation". A deliverable cannot be marked validated while any item is unconfirmed or any blocking question is open, and the skill never marks it validated on its own.
- **Official data at run time.** The skills read the FedRAMP Consolidated Rules from [FedRAMP/rules](https://github.com/FedRAMP/rules) at a pinned commit, with hash checks. The data is not stored here, because upstream has no licence file. Deliverables cite IDs and do not copy statement text; `scripts/frmr.py lint` reports copied text.
- **Class A, B and C.** Set the class in `engagement.json`; each skill passes it to the scripts and rates findings against the force a rule has at that class (`shared/references/classes.md`). Class D is out of scope. `20x-class-a-readiness` checks a client's alternative framework certification and the Class A rule lists. **No compliance verdicts.** **The consultant decides** scope and risk. **Client data stays local**: the skills work on the files the consultant provides and send nothing elsewhere.

## How a skill runs

1. The consultant names an engagement folder (see `shared/references/engagement-folder.md`). Client files go in `inputs/`, decisions in `decisions.json`.
2. The skill reads the rules it needs with `scripts/frmr.py`, works through its steps and asks its questions.
3. It writes the deliverable as JSON and builds the Markdown report and Excel tables from it with `scripts/build_report.py`.
4. It runs `scripts/check_deliverable.py` and `scripts/frmr.py lint` and fixes every error.
5. SME Validate.
6. It renders the Word and Excel copies with `scripts/render.py`.
7. Where a FedRAMP rule links a JSON schema, it exports schema-valid JSON with `scripts/fedramp_export.py` (incident reports, significant change notifications, Security Decision Record, Ongoing Certification Report, package overview, third-party resources).

## Install

Install the full plugin or single skills, not both. With both, each skill is listed twice.

**Claude Code, all skills.** In a session:

```bash
/plugin marketplace add ciaran-io/fedramp20x-skills
/plugin install fedramp20x-skills@fedramp20x-skills
```

Run a skill as `/fedramp20x-skills:<skill>`, for example `/fedramp20x-skills:20x-policy-review`.

**Claude Code, one skill.** The single-skill plugins are in a second marketplace in this repository. Add it by the URL of its file:

```bash
/plugin marketplace add https://raw.githubusercontent.com/ciaran-io/fedramp20x-skills/main/single/.claude-plugin/marketplace.json
/plugin install 20x-policy-review@fedramp20x-skills-single
```

Run it as `/20x-policy-review:20x-policy-review`. The same pattern applies to each skill.

From a shell, `claude plugin marketplace add` and `claude plugin install` take the same arguments.

**First run of Claude Code on Windows.** The installer puts `claude.exe` in `%USERPROFILE%\.local\bin`. If PowerShell says `claude` is not recognised, add that folder to your user PATH and open a new terminal:

```powershell
[Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path", "User") + ";$env:USERPROFILE\.local\bin", "User")
```

Claude Code asks whether to trust a folder the first time it starts there. Start it inside your engagement folder or your clone, and answer Yes.

**If an install fails.** After the marketplace file changes, run `claude plugin marketplace update <marketplace>` before installing again; the marketplace is cached. "Host key verification failed" means a plugin source used SSH: check `git config --global --get-regexp "^url\."` for an `insteadOf` rule that rewrites HTTPS to SSH.

**Updates.** Auto-update is off by default for marketplaces outside Anthropic's own. Turn it on in `/plugin`, on the Marketplaces tab, or update by hand:

```bash
claude plugin marketplace update fedramp20x-skills
claude plugin update fedramp20x-skills@fedramp20x-skills
```

For single skills, use the marketplace name `fedramp20x-skills-single`. Claude Code installs a new copy only when the version number changes, and every release changes it.

**claude.ai.** Download the zip files from the [latest release](https://github.com/ciaran-io/fedramp20x-skills/releases/latest), or run `python tools/package_skills.py` to build `dist/<skill>.zip` for each skill and `dist/fedramp20x-skills.zip` for the full set, then upload a `.zip` as a custom skill. Each skill folder carries its own copy of the shared scripts and references, so it works on its own.

**Requirements.** Python 3.10 or newer, `pip install python-docx openpyxl` for the Word and Excel copies, and `pip install jsonschema` for the FedRAMP JSON export. The first run downloads the FedRAMP rules data to `~/.cache/fedramp20x-skills/` (set `FRMR_DIR` to use another folder):

```bash
python shared/scripts/frmr.py fetch
python shared/scripts/fedramp_export.py fetch
```

The second command downloads the pinned FedRAMP JSON schemas from fedramp.gov into the same cache, checking each SHA-256. If fedramp.gov is blocked where you work, save the files by hand into a folder and set `FEDRAMP_SCHEMA_DIR` to it. Neither the rules data nor the schemas are committed to this repository.

## Example engagement

[`examples/orrinwick/`](examples/orrinwick/) holds a fictional engagement with one deliverable from each skill, built from the fedramp20x material. The findings are real findings about that material, for example a scope change check that cannot detect a changed exclusion condition, and 28 KSIs that report pass while their coverage notes describe a gap.

## Tests

```bash
pip install pytest python-docx openpyxl
python -m pytest -q tests
```

CI runs these on every push. They check the skills' structure, the shared files, the scripts, and that every example passes its checks and scores fully against its test case. Each skill also has seeded test cases in `tests/<skill>/seeded/` with faults a run must report and things it must not invent. Running those needs a model: see [`tests/README.md`](tests/README.md) and `tools/run_skill_test.sh`.

## Repository layout

| Folder | Contents |
|---|---|
| `.claude-plugin/` | `plugin.json` and `marketplace.json` for the full plugin |
| `single/` | The second marketplace: one plugin per skill. Built by `python tools/sync_shared.py`; never edit it by hand |
| `shared/` | The scripts and references every skill uses. Edit here, then run `python tools/sync_shared.py` |
| `skills/<skill>/` | `SKILL.md`, `references/`, `scripts/`, `templates/` |
| `tools/` | Sync, packaging, scoring and the headless test runner |
| `examples/orrinwick/` | The fictional engagement |
| `tests/` | Repository tests and each skill's test cases |

## Relation to other FedRAMP plugins

General plugins already cover KSI checks, Minimum Assessment Scope review, vulnerability detection and response, and audit evidence review. These skills do not repeat them. They add the method above: traceability from policy to check, validator designs with break tests, review records measured against the run date, records that are only added to, an assessor's review of the consultant's own work, and SME validation of every deliverable.

## How this project was built

An AI assistant (Claude) drafts the skills, scripts, templates and test cases. I decide what each skill must do, set the method it follows, and review, correct and test every skill before I commit it.

## License

MIT (see `LICENSE`). FedRAMP's data is not in this repository.
