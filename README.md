# Security Metrics Pipeline

A defensive security data-engineering project for turning synthetic vulnerability and asset records into trustworthy operational metrics. The pipeline focuses on metric correctness, ownership integrity, SLA transparency, and reproducible reporting rather than dashboard cosmetics.

## Problems addressed
Security metrics can be misleading when denominator logic, ownership mappings, asset scope, or exception handling are inconsistent. This project demonstrates how to build a governed metrics layer that calculates:

- vulnerability backlog by severity;
- overdue findings and SLA compliance;
- patch/compliance percentage by owner;
- asset coverage and data-quality exceptions;
- aging buckets;
- risk-weighted backlog.

## Architecture

```text
Synthetic findings + asset inventory
        |
        v
Schema validation -> ownership join -> metric engine -> quality gates -> report
```

## Structure

```text
src/
  metrics.py
  quality.py
  pipeline.py
data/
  findings.csv
  assets.csv
tests/
  test_metrics.py
docs/
  metric-governance.md
  data-quality.md
reports/
  example-report.md
.github/workflows/
  tests.yml
```

## Key design principle
A metric is not considered trustworthy simply because it can be calculated. Each metric needs a defined population, denominator, exclusions, ownership rule, refresh expectation, and validation control.

## Usage

```bash
python -m src.pipeline data/assets.csv data/findings.csv
python -m unittest discover -s tests -v
```

## Safe data model
All assets, owners, and vulnerability records are synthetic. No employer, client, or production information is included.

## Skills demonstrated
Python data engineering, security KPI/KRI design, vulnerability management analytics, SLA governance, data-quality validation, asset ownership modeling, reporting controls, and unit testing.

## Limitations
The included calculations are reference implementations. Enterprise metrics require organization-specific SLA policies, risk acceptance logic, source-system reconciliation, and governance approval.

## Roadmap
Add historical snapshots, trend deltas, API adapters, CSV/JSON exports, and automated schema contracts.
