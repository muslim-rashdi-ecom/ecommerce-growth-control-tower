import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from control_tower.analytics import creative_fatigue_report, funnel_report, reconciliation_report
from control_tower.ingest import load_campaigns, load_reconciliation
from control_tower.recommendations import recommend
from control_tower.report import build_report


DATA_DIR = Path(__file__).parents[1] / "data"


class ControlTowerTests(unittest.TestCase):
    def setUp(self):
        self.campaigns = load_campaigns(DATA_DIR / "campaign_daily.csv")
        self.reconciliation = load_reconciliation(DATA_DIR / "reconciliation.csv")
        self.report = build_report(DATA_DIR)

    def test_funnel_report_preserves_stage_order(self):
        funnel = funnel_report(self.campaigns)
        self.assertEqual([row["stage"] for row in funnel], ["Landing page views", "View item", "Add to cart", "Begin checkout", "Purchases"])
        self.assertGreater(funnel[0]["count"], funnel[-1]["count"])

    def test_reconciliation_flags_large_discrepancy(self):
        rows = reconciliation_report(self.reconciliation)
        flagged = [row for row in rows if row["status"] == "investigate"]
        self.assertTrue(flagged)
        self.assertTrue(any(row["platform"] == "TikTok" for row in flagged))

    def test_creative_fatigue_detects_tiktok_ctr_drop(self):
        rows = creative_fatigue_report(self.campaigns)
        tiktok = next(row for row in rows if row["platform"] == "TikTok")
        self.assertEqual(tiktok["status"], "watch")
        self.assertLess(tiktok["ctr_change_points"], 0)

    def test_recommendations_are_explainable(self):
        actions = {(row["platform"], row["campaign"]): row["action"] for row in self.report["recommendations"]}
        self.assertEqual(actions[("Meta", "LED Prospecting")], "scale_cautiously")
        self.assertEqual(actions[("TikTok", "LED Creative Test")], "audit_attribution")
        for row in self.report["recommendations"]:
            self.assertTrue(row["reason"])

    def test_report_labels_data_as_synthetic(self):
        self.assertEqual(self.report["data_status"], "synthetic portfolio data")
        self.assertTrue(self.report["warnings"])


if __name__ == "__main__":
    unittest.main()
