REQUIRED_ASSET_FIELDS = {"asset_id", "owner", "criticality"}
REQUIRED_FINDING_FIELDS = {"finding_id", "asset_id", "severity", "days_open", "overdue"}
VALID_SEVERITIES = {"critical", "high", "medium", "low"}


def validate_assets(rows: list[dict]) -> list[str]:
    errors = []
    seen = set()
    for index, row in enumerate(rows, start=1):
        missing = REQUIRED_ASSET_FIELDS - row.keys()
        if missing:
            errors.append(f"asset row {index}: missing {sorted(missing)}")
        asset_id = row.get("asset_id", "")
        if asset_id in seen:
            errors.append(f"asset row {index}: duplicate asset_id {asset_id}")
        seen.add(asset_id)
        if not row.get("owner"):
            errors.append(f"asset row {index}: blank owner")
    return errors


def validate_findings(rows: list[dict], asset_ids: set[str]) -> list[str]:
    errors = []
    for index, row in enumerate(rows, start=1):
        missing = REQUIRED_FINDING_FIELDS - row.keys()
        if missing:
            errors.append(f"finding row {index}: missing {sorted(missing)}")
        if row.get("severity", "").lower() not in VALID_SEVERITIES:
            errors.append(f"finding row {index}: invalid severity")
        if row.get("asset_id") not in asset_ids:
            errors.append(f"finding row {index}: asset not present in inventory")
        try:
            if int(row.get("days_open", -1)) < 0:
                errors.append(f"finding row {index}: negative days_open")
        except ValueError:
            errors.append(f"finding row {index}: days_open is not numeric")
    return errors
