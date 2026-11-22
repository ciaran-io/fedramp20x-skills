# Changelog

## v0.1.1 (in progress)

Fixes from the first model test run on 22 November 2026.

### Installation

- The main marketplace now lists the full plugin only. The single-skill plugins moved to a second marketplace in the same repository, `single/.claude-plugin/marketplace.json` (named `fedramp20x-skills-single`), so a skill is no longer listed twice.
- Each single-skill plugin has its own folder, `single/plugins/<skill>/`, with a `plugin.json` whose name matches its marketplace entry. In v0.1.0 all nine entries pointed at the repository root, whose `plugin.json` is named `fedramp20x-skills`. Claude Code requires the two names to match.
- `tools/sync_shared.py` builds `single/` from `skills/` and the root `plugin.json`. `--check`, the repository tests and CI fail when a copy differs.
- Version 0.1.1 in every `plugin.json`. Claude Code installs a new copy only when the version changes, which is the likely reason a v0.1.0 install kept an older commit.
- The README gives the exact install and run commands for both marketplaces, and how to update.

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
