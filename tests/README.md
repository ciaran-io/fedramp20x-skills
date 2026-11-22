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

`expected.json` lists the findings a run must report (`expect`) and the ones it must not (`must_not`), such as a tool name that appears in no input or a decision the skill must leave to the consultant. `tools/score.py` scores a deliverable against it.

Running a seeded case needs a model, so it is not part of CI. On a machine with Claude Code signed in:

```bash
tools/run_skill_test.sh 20x-policy-review seeded "Review the policies in the inputs folder. Engagement folder: /tmp/eng. Client: Test Co. Consultant: A. Tester. Where you would ask me, use your recommended option and record that you did."
```

Read the deliverable as well as the score. The score shows that expected findings are present; it does not show that the wording is right.
