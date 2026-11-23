# FedRAMP JSON export

FRC-CSO-JSN requires information to be shared as JSON valid against the FedRAMP schema a rule links, where one is linked. The deliverable JSON is a working format. After SME Validate, `scripts/fedramp_export.py` writes the FedRAMP JSON from a `fedramp_export` block in the deliverable and checks it against the pinned schema.

## Rules

- Export only after SME validation. The script refuses a draft.
- Read the schema before mapping: `python scripts/fedramp_export.py fields <schema>` lists every field it defines. Never map a field it does not list.
- Every value comes from the validated deliverable: an item, the change or incident record, or a recorded decision. Name its source in `sources`, by field path.
- Where the schema needs a value the deliverable does not hold, do not guess. Put the field name in `missing`, ask the consultant, and leave the export unfinished. Optional fields the deliverable does not hold are left out, not listed.
- Dates are ISO 8601. A date-time carries the time zone offset the record states.
- The script refuses a value that is null or holds a `[placeholder]`.
- Schemas are downloaded at run time and never committed. If fedramp.gov is blocked, save the files by hand into a folder and set `FEDRAMP_SCHEMA_DIR`; the hashes are still checked.

## Block

```json
"fedramp_export": [{
  "schema": "incident-report",
  "fragment": null,
  "document": {"reportType": "Initial", "providerTrackingId": "INC-2027-001"},
  "sources": {"reportType": [{"item": "RC-02"}], "providerTrackingId": [{"item": "RC-02"}]},
  "missing": ["certificationPackageOverviewUri"]
}]
```

Run `python scripts/fedramp_export.py export DELIVERABLE.json --schema <schema> --out <file>.json`. Keep the output next to the deliverable.

## Field maps

`certificationPackageOverviewUri` is required by every provider schema except the package overview. No skill holds it; ask the consultant for it once and record it as a decision.

### 20x-incident-reporting: `incident-report` (IEC-CSO-IIR, IEC-CSO-OIR, IEC-CSO-FIR)

| Field | From |
|---|---|
| `reportType` | Initial, Ongoing or Final: the report being sent |
| `providerTrackingId` | The incident record's tracking identifier |
| `federalIncidentCoordinator` | Report content item for the coordinator contact, when supplied |
| `incidentDescription` | Evaluation answers describing what happened |
| `timeline.startedAt`, `detectedAt`, `detectionSource`, `evaluationCompletedAt` | Incident record; `evaluationCompletedAt` is the reportability decision |
| `timeline.milestones[]` | Recorded events with times |
| `potentialImpact.currentRating` | The rating in force, as an integer 0 to 5 (N5 default until an estimate is approved) |
| `potentialImpact.historicalRating[]`, `evaluationNotes` | Rating history and the PAIN explanation, when recorded |
| `functionalImpact`, `affectedAgencies[]`, `recoveryPlan` | Report content items |
| `observedActivity`, `indicatorsOfCompromise[]`, `relatedCveIds[]`, `rootCause`, `responseAndRecoveryActivities` | Ongoing reports, when recorded |
| `resolvedAt` | Required for Final |

### 20x-change-evaluation: `significant-change-notifications` (SCN-CSO-INF, SCN-CSO-HRM)

Export only an adaptive or transformative change. The schema has no value for not significant or routine recurring changes.

| Field | From |
|---|---|
| `changeType` | The decided type (`decided_type`), Adaptive or Transformative. Never the proposed type |
| `changeTypeExplanation` | Evaluation answers EV-1 to EV-4 |
| `changeDescription`, `reason`, `customerImpact` | The change record and notice content items |
| `planAndTimeline.summary`, `plannedStart`, `plannedCompletion`, `milestones[]` | Change start and finish dates and the plan the client states |
| `impactedControls[]` | KSI IDs the client names for verification |
| `impactAnalysis`, `assessorName`, `relatedVulnerability` | Notice content items, when supplied |

### 20x-package-builder: `security-decision-record`, `ongoing-certification-report`, `certification-package-overview`

| Schema | Field | From |
|---|---|---|
| security-decision-record | `metadata.version`, `lastUpdated`, `updateSource` | Package metadata the client supplies |
| security-decision-record | `fedRampRequirements[]` (`frrID`, `frrImplementation[]`, `frrValidation[]`, `frrImplementationStatus`) | SDR-CSO-FRR entries, one per rule |
| security-decision-record | `keySecurityIndicators[]` (`ksiId`, `ksiImplementation[]`, `ksiValidation[]`, `ksiAssessment[]`, `ksiTests[]`, `ksiEvidence[]`) | KSI summaries: method IDs as `ksiTests`, the latest result as `ksiValidation`, evidence files as `ksiEvidence`. All six are required for each KSI |
| ongoing-certification-report | every required field | OCR items. An empty `reportableIncidents.incidents` attests that none occurred: use it only when the incident records show none, never because none were provided |
| certification-package-overview | `serviceIdentification`, `serviceProperties`, `contactInformation` | Overview metadata the client supplies |

### 20x-scope-review: `certification-package-overview`, fragment `thirdPartyInformationResources` (MAS-CSO-TPR)

| Field | From |
|---|---|
| `certified[]` (`fedRampCertifiedThirdPartyInformationResource`, `useCase`) | Third-party resources with a FedRAMP ID |
| `nonCertified[]` (`name`, `provider`, `useCase`, `website`) | Third-party resources without one. The provider's name must be stated in the scope record |
