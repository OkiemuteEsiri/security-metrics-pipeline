import csv
import json
import sys
from pathlib import Path
from .metrics import calculate_metrics
from .quality import validate_assets, validate_findings


def read_csv(path: str) -> list[dict]:
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def run(asset_path: str, finding_path: str) -> dict:
    assets = read_csv(asset_path)
    findings = read_csv(finding_path)
    errors = validate_assets(assets)
    errors += validate_findings(findings, {a.get("asset_id", "") for a in assets})
    if errors:
        raise ValueError("Data quality gate failed:\n" + "\n".join(errors))
    return calculate_metrics(assets, findings)


if __name__ == "__main__":
    result = run(sys.argv[1], sys.argv[2])
    print(json.dumps(result, indent=2, sort_keys=True))
