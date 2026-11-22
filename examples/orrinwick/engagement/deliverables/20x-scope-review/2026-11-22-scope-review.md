---
title: Minimum Assessment Scope review
client: Orrinwick Labs, Inc.
class: C (CR26)
frmr_version: 2026.11.02.01 (commit 64fa769)
date: 2026-11-22
prepared_by: Claude, for A. Example
sme_validation: Draft: pending SME validation
---

# Minimum Assessment Scope review

| | |
|---|---|
| Mode | review |
| Record reviewed | I-14, version 0.1.0 |
| Findings | 0 High, 2 Moderate, 0 Low, 2 Observation |
| Exclusion conditions | 10 |

The scope decisions belong to the consultant and the client. Proposed decisions are marked as proposals until a decision log entry records them.

## Inputs

| ID | File | Description |
|---|---|---|
| I-14 | `scope/mas-record.json` | Minimum Assessment Scope record, version 0.1.0, status draft |
| I-13 | `scope/scope-changes.json` | Scope change log, SC-001 and SC-002 |
| I-15 | `tools/check_scope_changes.py` | Check that compares the scope record with the change log |

## Findings

| Id | Title | Test | Rating | Observation | Criteria | Recommendation | Sources |
|---|---|---|---|---|---|---|---|
| F-001 | Exclusion conditions have evidence but no owner, cycle, record or check | M3 Conditions | Moderate | 10 conditions keep 8 resources out of scope (C4, C5, E10, E11, S1, S2, S3, T4). Each names the evidence that shows it holds. None names who checks the evidence, how often, or where the result is recorded, and no validator in the inputs reads the evidence. An exclusion is valid only while its condition holds, so the record cannot show that these resources are still outside the offering. | MAS-CSO-IIR | Give each condition an owner, a cycle and a record location, and add a check that reads the named evidence. Until then, treat each excluded resource as a scope risk. | I-14 information_resources[].conditions: COND-E10-1, COND-E10-2, COND-E11-1, COND-S1-1, COND-S1-2, COND-S2-1, COND-S3-1, COND-C4-1, COND-C5-1, COND-T4-1; MAS-CSO-IIR |
| F-002 | The change log check cannot see a change to a condition | M8 Change log | Moderate | The fingerprint in check_scope_changes.py records conditions only when they are text. The conditions in the record are objects with an ID, text and evidence, so the fingerprint falls back to the list of resources that have conditions. A change to a condition's text or evidence does not change the fingerprint. In a test on 2026-11-22, COND-S1-1 was changed to allow alert content in tickets and its evidence was removed; the check still reported that the change log matches the scope record. The log has a condition_changed type that this check cannot trigger. | SCN-CSO-EVA, SCN-CSO-MAR | Include each condition's ID, text and evidence in the fingerprint, and add a test that edits a condition and expects the check to fail. | I-15 fingerprint(), conditions key; I-14 S1 COND-S1-1; I-13 change types; SCN-CSO-EVA; SCN-CSO-MAR |
| F-003 | Third-party providers are not yet selected | M5 Third parties | Observation | All 7 third-party entries record each item that MAS-CSO-TPR lists. The authorization status of 7 of them is 'To be verified before provider selection', so the usage and configuration describe a planned setup, not a selected provider. | MAS-CSO-TPR | When each provider is selected, update its entry with the provider and its actual configuration, and log the change in the scope change log. | I-14 third_party_resources: TPR-T1, TPR-T2, TPR-T3, TPR-T5, TPR-E1, TPR-E7, TPR-E9; MAS-CSO-TPR |
| F-004 | The scope record is still a draft | M10 Status | Observation | The record has status 'draft' and version 0.1.0. The policies and validator designs cite its resource IDs, and the change log treats SC-001 as the baseline. | MAS-CSO-IIR | Approve the record, or state in it which parts are still open, so that work that relies on it can cite an approved version. | I-14 status; record_version; I-13 SC-001 |

## Exclusion conditions

| Id | Resource | Text | Evidence | Owner | Cadence | Record location | Check | Sources |
|---|---|---|---|---|---|---|---|---|
| COND-E10-1 | E10 | Staging runs in separate cloud accounts with no network path or shared credentials to production. | Account and network configuration checks; credential-sharing scan. | not stated | not stated | not stated | none in the inputs | I-14 E10 COND-E10-1 |
| COND-E10-2 | E10 | Production data, snapshots and backups are never restored or copied into staging. | Snapshot sharing deny policy and restore-event audit. | not stated | not stated | not stated | none in the inputs | I-14 E10 COND-E10-2 |
| COND-E11-1 | E11 | Only company-managed devices passing posture checks can use the production access gateway (E6). | Gateway device posture policy and denied-access logs. | not stated | not stated | not stated | none in the inputs | I-14 E11 COND-E11-1 |
| COND-S1-1 | S1 | Structured intake rejects attachments and free-text alert content; redaction is applied to inbound text. | Intake configuration test with sample payloads. | not stated | not stated | not stated | none in the inputs | I-14 S1 COND-S1-1 |
| COND-S1-2 | S1 | Support staff are trained and attest that tickets carry no customer alert content. | Training records and quarterly ticket sampling. | not stated | not stated | not stated | none in the inputs | I-14 S1 COND-S1-2 |
| COND-S2-1 | S2 | Data loss prevention rules block alert content, contact lists and credentials in outbound and internal mail. | DLP rule export and test messages. | not stated | not stated | not stated | none in the inputs | I-14 S2 COND-S2-1 |
| COND-S3-1 | S3 | Chat retention and DLP detect and remove customer content; policy prohibits sharing it. | DLP configuration and sampled search results. | not stated | not stated | not stated | none in the inputs | I-14 S3 COND-S3-1 |
| COND-C4-1 | C4 | Only aggregate monthly counts per tenant leave the platform; no alert, user or content detail is exported. | Billing export schema check and sample review. | not stated | not stated | not stated | none in the inputs | I-14 C4 COND-C4-1 |
| COND-C5-1 | C5 | Secret scanning and policy keep credentials and customer data out of the wiki; access limited to staff. | Secret scan results and access list. | not stated | not stated | not stated | none in the inputs | I-14 C5 COND-C5-1 |
| COND-T4-1 | T4 | Scrubbing removes tenant, user and alert identifiers and all D1 to D4 content before any telemetry leaves the platform. | Automated outbound payload test in the pipeline. | not stated | not stated | not stated | none in the inputs | I-14 T4 COND-T4-1 |

## Decisions for the consultant

| ID | Question | Options | Recommendation | Decision |
|---|---|---|---|---|
| DQ-001 | Who checks the exclusion conditions, and how often? | The GRC Lead, every 3 months, recorded in the GRC records, Each resource owner, on a cycle the client sets, Automated checks where the evidence is machine-readable, plus a 3-monthly review by the GRC Lead for the rest | Automated checks where the evidence is machine-readable, plus a 3-monthly review by the GRC Lead for the rest: Several conditions name machine evidence (configuration checks, scans, pipeline tests) and others name people evidence (training, sampling). The GRC Lead already records exceptions in the policies. Three months matches the minimum check cadence for non-machine resources (VDR-TFR-NMV); the client may choose a shorter cycle | open |

## Open questions

None.

## SME validation

Draft: pending SME validation.

