# Check patterns

## Result format

Every method returns one result. `scripts/break_test.py` reads `method_id`, `status` and `findings`.

```python
{"ksi": "KSI-INR-RIR", "method_id": "inr-rir-live", "kind": "static | live | change",
 "source": "what it read", "expected": "the pass condition in words", "observed": "what it saw",
 "status": "pass | fail", "findings": ["one message per failed condition"]}
```

A method with findings fails. A method with no findings passes. There is no other status. A "due by" note for a pending change review goes in `notes`, not `findings`.

## Run date

Every method takes `as_of` (a date) and measures every age against it. The command line takes `--as-of`, defaulting to today. Tests always pass a fixed date. A record dated after `as_of` is a finding.

```python
age = (as_of - review_date).days
if review_date > as_of:
    findings.append(f"The newest review is dated {review_date}, after the run date {as_of}")
elif age > cadence:
    findings.append(f"The newest review is {age} days old, the cadence is {cadence} days")
```

## Records as lists

Reviews are a list. The newest dated entry counts. Entries with no date are ignored, and if none remain the method fails with "No review is recorded". Never read a single overwritten field.

## Reviewer

Read the owner from the policy, not from a constant in the code. Compare it with the record's reviewer field. Report both values in the message.

## Change deadlines

For each change, find a review dated on or after the change and on or before its deadline. If the deadline has not passed and no review exists, add a note "due by <date>". If it has passed, add a finding. Count business days the way the consultant decided (see the change evaluation skill); do not assume holidays.

## Empty input

A method whose source is missing, empty or unparseable fails with a finding that says so. It never passes by default.

## Client checks that read fixed paths

`break_test.py` and `empty_probe.py` copy each input to a temporary folder and pass the copies' paths to the check command. A client check that reads files from fixed paths in its own repository cannot be pointed at the copies. Do not edit the client's check to test it. Write a small adapter next to the deliverable that:

- takes the file paths and the run date as arguments,
- replaces only the client's file loading function, in memory, so each fixed path reads the given file instead,
- runs the client's methods unchanged and prints the JSON list of results.

Name the adapter in the deliverable (`code.run`) and record that the client's code was not changed. Recommend, as a decision for the consultant, that the client's checks take file paths, so no adapter is needed.

## Messages

One finding per failed condition. Each message names the record, the value seen and the value required, in plain words, so a break test can show exactly which condition failed.
