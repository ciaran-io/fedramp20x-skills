#!/usr/bin/env bash
# Run one skill on one test case with Claude Code, headless, then score the result.
#
#   tools/run_skill_test.sh <skill> <case> "<prompt>"
#   tools/run_skill_test.sh 20x-policy-review seeded "Review the policies in tests/20x-policy-review/seeded/inputs. Engagement folder: /tmp/eng. Client: Test Co. Consultant: A. Tester. Answer your own questions with the recommended option and record that you did."
#
# Needs Claude Code signed in. The skill writes its deliverable JSON into the engagement
# folder; this script then scores every deliverable JSON it finds there against
# tests/<skill>/<case>/expected.json. Read the deliverable too: a score only checks
# that the expected findings are present and the forbidden ones are absent.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
SKILL=$1; CASE=$2; PROMPT=$3
ENG=${ENG:-/tmp/eng}
mkdir -p "$ENG/inputs"
cp -r "$ROOT/tests/$SKILL/$CASE/inputs/." "$ENG/inputs/" 2>/dev/null || true
claude -p --plugin-dir "$ROOT" --permission-mode acceptEdits "Use the $SKILL skill. $PROMPT" | tee "$ENG/run.log"
for j in $(find "$ENG/deliverables/$SKILL" -name "*.json" ! -name "*-tables.json"); do
  echo "== $j"
  python "$ROOT/tools/score.py" "$j" "$ROOT/tests/$SKILL/$CASE/expected.json" || true
done
