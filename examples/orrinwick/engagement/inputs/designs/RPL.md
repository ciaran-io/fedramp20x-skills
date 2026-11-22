# RPL: Recovery planning

> FICTIONAL DEMO PROJECT. Orrinwick Labs, Inc. and Orrinwick Beacon are invented.

Policy: [POL-RPL](../policies/POL-RPL.md). Recovery strategy: backup and restore (SD-003).

## KSI-RPL-RRO Reviewing Recovery Objectives

| Field | Design |
|---|---|
| Requirement | Orrinwick must set its own recovery time and recovery point objectives and keep reviewing them, so they stay correct as the service changes |
| Policy requirement | POL-RPL / RPL-1 |
| Resource type | Non-machine (a review process owned by the Platform Lead) |
| Validation cadence | Every build. VDR-TFR-NMV requires at least every 3 months |
| Static method | `rpl-rro-static`. Reads `environment/recovery-objectives.json` and `policies/policy-set.json`. Passes when `rto_hours`, `rpo_hours` and `review_cadence_days` are positive numbers and a POL-RPL requirement lists RPL-RRO |
| Live method | `rpl-rro-live`. Reads `reviews` from `environment/recovery-objectives.json` and measures the newest review's age against the run date. Passes when that review is no older than `review_cadence_days` and its `reviewed_by` matches the POL-RPL owner (Platform Lead) |
| Fails when | An objective or the cadence is missing, zero or not a number. No POL-RPL requirement covers RPL-RRO. No review exists, the newest review is dated after the run date or is older than the cadence, or a person other than the Platform Lead recorded it |
| Break test | Live: I set `last_reviewed` to 2024-11-19. The method failed with "Last review was 730 days ago, cadence is 90 days". A unit test covers a review recorded by the wrong person. Static: not yet run |
| Production source | The review record in the GRC tool or change ticket system, with the Platform Lead's approval and date. The RTO and RPO values from the recovery plan |
| Gap | The methods prove that the objectives exist and that a review took place inside the cadence. They do not prove what the review concluded, or that the objectives still match the architecture and the restore test results (RPL-TRC) |
| Status | Built |

**Decision.** I set the review cadence to 90 days. This is my choice as the provider and is stricter than the annual review the policy first stated. VDR-TFR-NMV sets how often the status of a non-machine resource must be validated. It does not set how often the review itself must happen.

**Decision.** The review must be recorded by the POL-RPL owner (Platform Lead), as for INR-RIR and CNA-RVP. Reviews are a list, and each review is added as a new entry. The review on 2026-11-19 had no reviewer recorded. I left it as it was and recorded a new review by the Platform Lead on 2026-11-22.

## KSI-RPL-ABO Aligning Backups with Objectives

| Field | Design |
|---|---|
| Requirement | The backups of machine resources must keep matching the recovery objectives, and Orrinwick must keep checking that they do |
| Policy requirement | POL-RPL / RPL-2 |
| Resource type | Machine-based (AWS Backup plans, vaults, recovery points and job history) |
| Validation cadence | Every build. VDR-TFR-MVX requires at least every 3 days |
| Static method | `abo-iac-backup-policy`. Reads the AWS Backup resources in `environment/iac-plan.json` and the objectives in `environment/recovery-objectives.json`. Passes when every backup rule runs at least every 2 hours (`backup_interval_hours_max`), keeps recovery points for at least 14 days, copies to a vault in us-west-2 with a compliance-mode lock, every vault uses a customer-managed key, and every protected data store is in a backup selection |
| Live method | `abo-live-backup-currency`. Reads `aws_backup` in `environment/live-state.json`. Passes when the newest recovery point of each protected resource is inside the RPO, each copy job to us-west-2 completed inside the RPO, and the us-west-2 vault has a compliance-mode lock |
| Alert method | `abo-live-failed-job-alerts`. Reads `environment/backup-jobs.json`, a job history prefilled from 2026-11-16 to 2027-11-22, and only counts jobs on or before the run date. Passes when a backup job and a copy job completed in the last day, and every failed job in the last 30 days has an alert raised within 60 minutes and acknowledged by a named person. The limits are `failed_job_alert_minutes_max` and `job_history_window_days` in `environment/recovery-objectives.json` |
| Fails when | A rule runs less often than every 2 hours, keeps data too briefly or has no copy to us-west-2. A vault has no customer-managed key, no lock or a lock that is not in compliance mode. A protected data store has no backup selection. A recovery point or copy is older than the RPO, or a copy job did not complete. No backup or copy job completed in the last day. A failed job in the last 30 days has no alert, an alert raised more than 60 minutes after the failure, or an alert nobody acknowledged |
| Break test | Unit tests: a 3-hour schedule fails the static method, and a governance-mode lock fails both methods. Unit tests for the alert method: on 2027-05-22 the planned failure with no alert fails, an alert raised after 3 hours fails, an unacknowledged alert fails, and a run after the history ends (2027-11-25) fails for having no recent jobs. Manual test on 2026-11-22, running the method for chosen dates: it passes on 2027-05-21, fails from 2027-05-22 to 2027-06-21 with "Failed backup job BJ-20270522 raised no alert", and passes again from 2027-06-22, when the failure leaves the 30-day window. Planned: set `latest_recovery_point_age_hours` for `db:primary` to 6 in `live-state.json` (live) |
| Production source | Static: the Terraform plan JSON for the AWS Backup resources. Live: AWS Backup `ListRecoveryPointsByResource`, `ListCopyJobs` and `DescribeBackupVault`. Alerts: `ListBackupJobs` and `ListCopyJobs` filtered to failed jobs, matched with the alert records in the on-call or incident tool, which receives the AWS Backup job state change events from EventBridge |
| Gap | The methods do not prove that a backup can be restored or that a restore meets the RTO. RPL-TRC covers that. Each job entry stands for one day of jobs, not each 2-hourly run. The history ends on 2027-11-22, after which the alert method fails until more history is added. It proves that an alert was raised and acknowledged, not what the person did next |
| Status | Built |

**Design review.** I found three points where the checks were weaker than POL-RPL. (1) The static method compared the backup interval with the 4-hour RPO, so a 3-hour schedule passed although RPL-2 requires every 2 hours. (2) Both methods checked that the vault was locked, but not that the lock was in compliance mode. (3) No method checks the alert for a failed backup or copy job. I closed (1) and (2) and added a unit test for each. On 2026-11-22 I closed (3) with a third method that checks the backup job history and the alert for each failed job.

**Decisions.**
- The job history is prefilled for a year, and the method reads only the entries up to the run date. This lets the method check that jobs ran recently, which a fixed snapshot could not, and the history grows day by day like a real one.
- The history has two planned failures. The failure on 2026-11-17 has its alert, so the evidence shows the alert path working. The failure on 2027-05-22 has no alert, so KSI-RPL-ABO fails from that date and shows the failure path on the trust center.
- Failed jobs are checked over the last 30 days. A missed alert stays visible as a failure for a month, then leaves the window, as it would in a monitoring tool. The finding itself is handled outside the check, through the incident and change records.
