"""Explainable, guardrail-based campaign recommendations."""

from __future__ import annotations

from typing import Iterable


def recommend(campaign_metrics: Iterable[dict[str, object]]) -> list[dict[str, object]]:
    recommendations = []
    for campaign in campaign_metrics:
        clicks = int(campaign["link_clicks"])
        spend = float(campaign["spend"])
        add_to_cart = int(campaign["add_to_cart"])
        begin_checkout = int(campaign["begin_checkout"])
        purchases = int(campaign["purchases"])
        roas = campaign["roas"]
        ctr = float(campaign["ctr_pct"] or 0)
        landing_rate = float(campaign["landing_view_rate_pct"] or 0)

        if clicks >= 100 and landing_rate < 75:
            action = "audit_attribution"
            reason = "Landing-page views are materially below link clicks; inspect redirects, page load, consent, and attribution scope."
        elif add_to_cart > 0 and begin_checkout == 0:
            action = "fix_checkout"
            reason = "Add-to-cart activity exists but no checkout progression is visible in the sample."
        elif purchases > 0 and isinstance(roas, (int, float)) and roas >= 2 and ctr >= 1.5:
            action = "scale_cautiously"
            reason = "The sample shows purchases, a positive ROAS guardrail, and healthy click-through; increase budget only with a controlled test."
        elif spend > 0 and purchases == 0 and clicks >= 20:
            action = "retest_offer_or_creative"
            reason = "The campaign has spend and engagement but no purchase evidence; change one test variable before scaling."
        else:
            action = "monitor"
            reason = "The sample is not strong enough for a more aggressive decision."

        recommendations.append(
            {
                "platform": campaign["platform"],
                "campaign": campaign["campaign"],
                "action": action,
                "reason": reason,
                "evidence": {
                    "spend": round(spend, 2),
                    "link_clicks": clicks,
                    "add_to_cart": add_to_cart,
                    "begin_checkout": begin_checkout,
                    "purchases": purchases,
                    "roas": roas,
                },
            }
        )
    return recommendations
