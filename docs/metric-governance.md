# Security Metric Governance

## Principle
A security metric is only useful when its scope, denominator, ownership, exclusions, refresh interval, and validation method are explicit.

## Core metric definitions

### Vulnerability backlog
Population: all open findings in the approved reporting scope.
Exclusions: approved duplicates and findings outside the reporting boundary.
Validation: reconcile counts to the source export before transformation.

### SLA compliance
Formula: `(findings within SLA / total in-scope findings) * 100`.
Controls: verify severity-to-SLA policy, exception handling, and reopened findings.

### Risk-weighted backlog
A directional workload metric that weights critical findings more heavily than lower-severity findings. It is not a replacement for formal risk assessment.

### Asset coverage
Compare assets represented in security telemetry with the authoritative asset population. Missing telemetry must not silently improve compliance percentages.

## Ownership controls
Owner mappings should be versioned, reviewed with stakeholders, and validated when organizational structures change. Unmapped assets should remain visible as a quality exception rather than being excluded.

## Change management
Changes to denominators, SLA policy, exclusions, or severity weights should be documented with effective dates so trend breaks are explainable.

## Reporting control checklist
- source extract timestamp recorded;
- asset scope reconciled;
- duplicate IDs rejected;
- orphan findings rejected;
- unmapped ownership visible;
- metric formulas version controlled;
- exceptions independently governed.
