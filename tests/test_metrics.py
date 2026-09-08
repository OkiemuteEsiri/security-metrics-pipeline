import unittest
from src.metrics import aging_bucket, calculate_metrics
from src.quality import validate_assets, validate_findings


class MetricsTests(unittest.TestCase):
    def test_aging_buckets(self):
        self.assertEqual(aging_bucket(10), "0-30")
        self.assertEqual(aging_bucket(45), "31-60")
        self.assertEqual(aging_bucket(75), "61-90")
        self.assertEqual(aging_bucket(120), "90+")

    def test_owner_sla_and_weighted_backlog(self):
        assets = [{"asset_id":"A1","owner":"team-a","criticality":"5"}]
        findings = [
            {"finding_id":"F1","asset_id":"A1","severity":"critical","days_open":"20","overdue":"true"},
            {"finding_id":"F2","asset_id":"A1","severity":"medium","days_open":"5","overdue":"false"},
        ]
        metrics = calculate_metrics(assets, findings)
        self.assertEqual(metrics["owner_sla_percent"]["team-a"], 50.0)
        self.assertEqual(metrics["risk_weighted_backlog"]["team-a"], 7)

    def test_duplicate_asset_detected(self):
        rows = [
            {"asset_id":"A1","owner":"a","criticality":"3"},
            {"asset_id":"A1","owner":"b","criticality":"4"},
        ]
        self.assertTrue(any("duplicate" in e for e in validate_assets(rows)))

    def test_orphan_finding_detected(self):
        rows = [{"finding_id":"F1","asset_id":"MISSING","severity":"high","days_open":"1","overdue":"false"}]
        self.assertTrue(any("asset not present" in e for e in validate_findings(rows, {"A1"})))


if __name__ == "__main__":
    unittest.main()
