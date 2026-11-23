#!/usr/bin/env bash
# Run one skill on one test case with Claude Code, headless, then score the result.
#
#   tools/run_skill_test.sh <skill> <case> ["<prompt>"]
#
# Without a prompt, tests/<skill>/<case>/prompt.txt is used. SETUP_ONLY=1 builds the engagement
# folder and writes the prompt to it without running Claude (for a run by another agent); score
# afterwards with tools/score.py. A baseline case has no inputs
# folder of its own; it runs on examples/orrinwick/engagement/inputs.
#   tools/run_skill_test.sh 20x-policy-review seeded "Review the policies in tests/20x-policy-review/seeded/inputs. Engagement folder: /tmp/eng. Client: Test Co. Consultant: A. Tester. Answer your own questions with the recommended option and record that you did."
#
# Needs Claude Code signed in. The skill writes its deliverable JSON into the engagement
# folder; this script then scores every deliverable JSON it finds there against
# tests/<skill>/<case>/expected.json. Read the deliverable too: a score only checks
# that the expected findings are present and the forbidden ones are absent.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
SKILL=$1; CASE=$2; PROMPT=${3:-}
ENG=${ENG:-/tmp/eng}
CASE_DIR="$ROOT/tests/$SKILL/$CASE"
if [ -e "$ENG/deliverables" ] || [ -n "$(ls -A "$ENG/inputs" 2>/dev/null)" ]; then
  echo "ERROR: $ENG is not empty. Use a new folder (ENG=/tmp/eng-$SKILL-$CASE) so runs do not mix." >&2
  exit 2
fi
mkdir -p "$ENG/inputs"
if [ -d "$CASE_DIR/inputs" ]; then
  cp -r "$CASE_DIR/inputs/." "$ENG/inputs/"
elif [ "$CASE" != "fedramp20x-findings" ]; then
  # A case with no inputs folder (baseline, inr-rir) runs on the example engagement.
  cp -r "$ROOT/examples/orrinwick/engagement/inputs/." "$ENG/inputs/"
  cp "$ROOT/examples/orrinwick/engagement/decisions.json" "$ROOT/examples/orrinwick/engagement/engagement.json" "$ENG/" 2>/dev/null || true
  # Other skills' example deliverables are inputs to some skills; the skill's own never is.
  for d in "$ROOT/examples/orrinwick/engagement/deliverables/"*/; do
    name=$(basename "$d")
    [ "$name" = "$SKILL" ] && continue
    mkdir -p "$ENG/deliverables/$name" && cp -r "$d." "$ENG/deliverables/$name/"
  done
elif [ "$CASE" = "fedramp20x-findings" ]; then
  git clone -q https://github.com/ciaran-io/fedramp20x.git "$ENG/inputs"
  git -C "$ENG/inputs" checkout -q 31c11e5
else
  echo "ERROR: $CASE_DIR has no inputs folder" >&2
  exit 2
fi
if [ -z "$PROMPT" ] && [ -f "$CASE_DIR/prompt.txt" ]; then
  PROMPT=$(sed "s#{ENG}#$ENG#g" "$CASE_DIR/prompt.txt")
fi
[ -n "$PROMPT" ] || { echo "ERROR: no prompt given and no $CASE_DIR/prompt.txt" >&2; exit 2; }
if [ -n "${SETUP_ONLY:-}" ]; then
  echo "engagement folder ready: $ENG"; printf '%s\n' "$PROMPT" > "$ENG/prompt.txt"; exit 0
fi
claude -p --plugin-dir "$ROOT" --permission-mode acceptEdits "Use the $SKILL skill. $PROMPT" | tee "$ENG/run.log"
for j in $(find "$ENG/deliverables/$SKILL" -maxdepth 1 -name "*.json" ! -name "*-tables.json"); do
  echo "== $j"
  python "$ROOT/tools/score.py" "$j" "$ROOT/tests/$SKILL/$CASE/expected.json" || true
done
