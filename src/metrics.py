from collections import Counter, defaultdict
from datetime import date

SEVERITY_WEIGHT = {"critical": 5, "high": 4, "medium": 2, "low": 1}


def aging_bucket(days_open: int) -> str:
    if days_open <= 30:
        return "0-30"
    if days_open <= 60:
        return "31-60"
    if days_open <= 90:
        return "61-90"
    return "90+"


def calculate_metrics(assets: list[dict], findings: list[dict]) -> dict:
    asset_by_id = {a["asset_id"]: a for a in assets}
    severity = Counter()
    aging = Counter()
    owner_total = Counter()
    owner_overdue = Counter()
    weighted_backlog = defaultdict(int)

    for finding in findings:
        sev = finding["severity"].lower()
        days_open = int(finding["days_open"])
        asset = asset_by_id.get(finding["asset_id"], {})
        owner = asset.get("owner", "unmapped")
        overdue = str(finding.get("overdue", "false")).lower() == "true"
        severity[sev] += 1
        aging[aging_bucket(days_open)] += 1
        owner_total[owner] += 1
        if overdue:
            owner_overdue[owner] += 1
        weighted_backlog[owner] += SEVERITY_WEIGHT.get(sev, 0)

    owner_sla = {}
    for owner, total in owner_total.items():
        overdue_count = owner_overdue[owner]
        owner_sla[owner] = round(((total - overdue_count) / total) * 100, 1) if total else 100.0

    return {
        "generated_on": date.today().isoformat(),
        "asset_count": len(assets),
        "finding_count": len(findings),
        "severity": dict(severity),
        "aging": dict(aging),
        "owner_sla_percent": owner_sla,
        "risk_weighted_backlog": dict(weighted_backlog),
    }
