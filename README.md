# FedRAMP 20x consultant skills

> **NOT ADVICE.** These skills are a learning and portfolio project. They are **not** a FedRAMP assessment, certification or legal advice. A skill's output says what the evidence shows and where it falls short. It never says that a client is compliant. All examples use Orrinwick Labs, Inc., a fictional company.

This repository is a set of Claude skills for a consultant who reviews a cloud service provider's FedRAMP 20x Class C program. Each skill takes the client's own material (policies, asset lists, diagrams, Terraform plans, records, evidence exports) and returns a finished deliverable. Every finding cites a FedRAMP rule or Key Security Indicator (KSI) ID.

The skills apply the method used in [fedramp20x](https://github.com/ciaran-io/fedramp20x), a worked Class C example for the fictional Orrinwick Labs:

- the scope is settled before anything else
- policies are reviewed against the KSIs, and each requirement names an owner, a cadence or deadline, and where the record is kept
- each KSI check has a written design that states how it fails
- each check is proven able to fail by a recorded break test
- finished work gets an assessor's review
- each decision gets a sanity check for the other places it applies

## Skills

| Skill | Status | Deliverable |
|---|---|---|
| `20x-policy-review` | To do | KSI coverage matrix, gaps, and rewritten requirement text |
| `20x-validator-design` | To do | One validator design per KSI, with failure conditions and a break test |
| `20x-assessor-review` | To do | Findings table: observation, criteria, rating, recommendation |
| `20x-scope-review` | To do | Minimum Assessment Scope record, boundary decisions and open questions |
| `20x-change-evaluation` | To do | Change type, notice timeline, scope log entry and review deadline |
| `20x-sanity-check` | To do | Where else a decision applies, and the documents that now disagree |
| `20x-validator-build` | To do | Check code with two automated methods, unit tests and a break test |
| `20x-incident-reporting` | To do | PAIN rating, reportability decision and reporting timeline |
| `20x-package-builder` | To do | Security Decision Record entries, Ongoing Certification Report draft, package outline |

The skills are built in the order listed.

## Rules the skills follow

- **Official data at run time.** The skills read the FedRAMP Consolidated Rules from [FedRAMP/rules](https://github.com/FedRAMP/rules) at a pinned commit. `scripts/fetch_frmr.py` downloads the data to `.frmr/` and checks its hashes. The data is not stored in this repository, because upstream has no licence file. Outputs cite rule and KSI IDs and do not copy statement text.
- **Class C (CR26) only.** Version 1 covers Class C. Each output states the class it assumed.
- **No compliance verdicts.** Outputs report what the evidence shows and where it falls short.
- **The consultant decides.** A skill drafts the deliverable, lists the decisions it needs, and recommends one option for each. It does not make scope or risk decisions.
- **Client data stays local.** The skills work on files the consultant provides and do not send client material anywhere. Keep client files outside this repository. The `client/` folder is ignored by Git as a safeguard.

## Install

Install all the skills as one plugin, or install one skill on its own.

**Claude Code, all skills:**

```bash
/plugin install fedramp20x-skills --marketplace ciaran-io/fedramp20x-skills
```

**Claude Code, one skill.** Each finished skill is also listed as its own plugin with the same name as the skill, for example:

```bash
/plugin install 20x-policy-review --marketplace ciaran-io/fedramp20x-skills
```

**claude.ai.** Each release includes a `.zip` file for each skill and one for the full set. Upload a `.zip` to claude.ai as a custom skill.

Before the first run, download the FedRAMP rules data (Python 3.10 or newer):

```bash
python scripts/fetch_frmr.py
```

## Deliverable formats

Each skill writes its deliverable as Markdown and JSON. The JSON is the source of truth for tests and for other skills. Client-facing deliverables are also produced as Word (`.docx`) documents, and tables such as the KSI coverage matrix and findings lists as Excel (`.xlsx`) workbooks.

## Relation to other FedRAMP plugins

General plugins already cover KSI checks, Minimum Assessment Scope review, vulnerability detection and response, and audit evidence review. These skills do not repeat them. They add the method above: traceability from policy to check, validator designs with break tests, review records measured against the run date, records that are only added to, and an assessor's review of the consultant's own work.

## Repository layout

| Folder | Contents |
|---|---|
| `.claude-plugin/` | `plugin.json`, so the repository installs as one plugin |
| `skills/` | One folder per skill: `SKILL.md`, `templates/` for deliverables, `references/` for rule notes (IDs only) |
| `scripts/` | Shared scripts, such as the FedRAMP rules download |
| `examples/orrinwick/` | Fictional inputs and the output each skill produced from them |
| `tests/` | Sample inputs with seeded faults and the findings each skill must report |

## How this project was built

An AI assistant (Claude) drafts the skills, templates and test cases. I decide what each skill must do, set the method it follows, and review, correct and test every skill before I commit it.

## License

MIT (see `LICENSE`). FedRAMP's data is not in this repository.
