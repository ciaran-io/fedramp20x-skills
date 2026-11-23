# Tests

## Repository tests (run in CI)

```bash
pip install pytest python-docx openpyxl
python shared/scripts/frmr.py fetch
python -m pytest -q tests
```

They check that each skill is well formed, the shared files are in sync, the scripts work, and that every example deliverable in `examples/orrinwick/` passes `check_deliverable.py` and `frmr.py lint`, matches the report its builder writes, and scores fully against its baseline case.

## Skill test cases

Each skill has a folder here with one or more cases:

| Case | Inputs | What it checks |
|---|---|---|
| `baseline` | The Orrinwick inputs in `examples/orrinwick/engagement/inputs` | The example deliverable reports the findings already known from fedramp20x |
| `seeded` | Inputs with known faults in `<case>/inputs` | A run of the skill reports each seeded fault and does not invent what the inputs do not contain |
| `fedramp20x-findings` (assessor review only) | fedramp20x at commit `31c11e5`, before the fixes | A run reproduces the author's own assessor findings A1 to A10 and A12 (A11 was never recorded) |

`expected.json` lists the findings a run must report (`expect`) and the ones it must not (`must_not`), such as a tool name that appears in no input or a decision the skill must leave to the consultant. `tools/score.py` scores a deliverable against it.

Running a seeded case needs a model, so it is not part of CI. On a machine with Claude Code signed in:

```bash
ENG=/tmp/eng-policy-seeded tools/run_skill_test.sh 20x-policy-review seeded
```

Each case has a `prompt.txt`; a prompt given as the third argument replaces it. Use a new engagement folder for every run: the script refuses one that already holds inputs or deliverables. A case with no `inputs` folder runs on the example engagement's inputs, with the other skills' example deliverables (never the skill's own). The `fedramp20x-findings` case clones fedramp20x at `31c11e5`.

`tools/score.py` matches IDs, test codes and ratings exactly, and phrases without regard to case or spacing. A phrase in `mentions` can be a list of alternatives. Put the facts that make a finding right in `mentions`, not the example's wording.

Read the deliverable as well as the score. The score shows that expected findings are present; it does not show that the wording is right.
