"""Deterministic metrics for campaign and funnel diagnosis."""

from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from .models import CampaignRow, ReconciliationRow


def _safe_div(numerator: float, denominator: float) -> float | None:
    return round(numerator / denominator, 4) if denominator else None


def _pct(numerator: float, denominator: float) -> float | None:
    result = _safe_div(numerator, denominator)
    return round(result * 100, 2) if result is not None else None


def aggregate_campaigns(rows: Iterable[CampaignRow]) -> list[dict[str, object]]:
    buckets: dict[tuple[str, str], dict[str, object]] = {}
    for row in rows:
        key = (row.platform, row.campaign)
        bucket = buckets.setdefault(
            key,
            {
                "platform": row.platform,
                "campaign": row.campaign,
                "spend": 0.0,
                "impressions": 0,
                "link_clicks": 0,
                "landing_page_views": 0,
                "view_item": 0,
                "add_to_cart": 0,
                "begin_checkout": 0,
                "purchases": 0,
                "revenue": 0.0,
            },
        )
        for key_name in (
            "spend",
            "impressions",
            "link_clicks",
            "landing_page_views",
            "view_item",
            "add_to_cart",
            "begin_checkout",
            "purchases",
            "revenue",
        ):
            bucket[key_name] = bucket[key_name] + getattr(row, key_name)

    output: list[dict[str, object]] = []
    for bucket in buckets.values():
        spend = float(bucket["spend"])
        impressions = int(bucket["impressions"])
        clicks = int(bucket["link_clicks"])
        purchases = int(bucket["purchases"])
        revenue = float(bucket["revenue"])
        bucket.update(
            {
                "ctr_pct": _pct(clicks, impressions),
                "cpc": round(spend / clicks, 4) if clicks else None,
                "landing_view_rate_pct": _pct(int(bucket["landing_page_views"]), clicks),
                "add_to_cart_rate_pct": _pct(int(bucket["add_to_cart"]), int(bucket["view_item"])),
                "purchase_rate_pct": _pct(purchases, clicks),
                "roas": round(revenue / spend, 2) if spend else None,
            }
        )
        output.append(bucket)
    return sorted(output, key=lambda item: (str(item["platform"]), str(item["campaign"])))


def funnel_report(rows: Iterable[CampaignRow]) -> list[dict[str, object]]:
    totals = defaultdict(int)
    for row in rows:
        for field in ("landing_page_views", "view_item", "add_to_cart", "begin_checkout", "purchases"):
            totals[field] += getattr(row, field)
    stages = [
        ("landing_page_views", "Landing page views"),
        ("view_item", "View item"),
        ("add_to_cart", "Add to cart"),
        ("begin_checkout", "Begin checkout"),
        ("purchases", "Purchases"),
    ]
    output = []
    previous_count: int | None = None
    for field, label in stages:
        count = totals[field]
        output.append(
            {
                "stage": label,
                "count": count,
                "previous_stage_rate_pct": _pct(count, previous_count or 0),
                "drop_from_previous": None if previous_count is None else previous_count - count,
            }
        )
        previous_count = count
    return output


def reconciliation_report(rows: Iterable[ReconciliationRow], threshold_pct: float = 15.0) -> list[dict[str, object]]:
    output = []
    for row in rows:
        difference = row.platform_count - row.site_count
        discrepancy_pct = round(abs(difference) / row.site_count * 100, 2) if row.site_count else None
        output.append(
            {
                "date": row.date,
                "platform": row.platform,
                "event": row.event,
                "platform_count": row.platform_count,
                "site_count": row.site_count,
                "difference": difference,
                "discrepancy_pct": discrepancy_pct,
                "status": "investigate" if discrepancy_pct is not None and discrepancy_pct >= threshold_pct else "within_guardrail",
                "scope": row.scope,
            }
        )
    return output


def creative_fatigue_report(rows: Iterable[CampaignRow], drop_threshold_pct_points: float = 1.0) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str, str], list[CampaignRow]] = defaultdict(list)
    for row in rows:
        grouped[(row.platform, row.campaign, row.creative)].append(row)
    output = []
    for (platform, campaign, creative), creative_rows in grouped.items():
        ordered = sorted(creative_rows, key=lambda item: item.date)
        first, last = ordered[0], ordered[-1]
        first_ctr = _pct(first.link_clicks, first.impressions) or 0.0
        last_ctr = _pct(last.link_clicks, last.impressions) or 0.0
        drop = round(first_ctr - last_ctr, 2)
        output.append(
            {
                "platform": platform,
                "campaign": campaign,
                "creative": creative,
                "first_ctr_pct": first_ctr,
                "last_ctr_pct": last_ctr,
                "ctr_change_points": round(last_ctr - first_ctr, 2),
                "status": "watch" if drop >= drop_threshold_pct_points else "stable",
            }
        )
    return sorted(output, key=lambda item: (str(item["platform"]), str(item["campaign"]), str(item["creative"])))
