"""Typed rows used by the control tower."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


def _int(row: Mapping[str, str], key: str) -> int:
    return int(float(row[key]))


def _float(row: Mapping[str, str], key: str) -> float:
    return float(row[key])


@dataclass(frozen=True)
class CampaignRow:
    date: str
    platform: str
    campaign: str
    ad_set: str
    creative: str
    spend: float
    impressions: int
    link_clicks: int
    landing_page_views: int
    view_item: int
    add_to_cart: int
    begin_checkout: int
    purchases: int
    revenue: float

    @classmethod
    def from_row(cls, row: Mapping[str, str]) -> "CampaignRow":
        return cls(
            date=row["date"],
            platform=row["platform"],
            campaign=row["campaign"],
            ad_set=row["ad_set"],
            creative=row["creative"],
            spend=_float(row, "spend"),
            impressions=_int(row, "impressions"),
            link_clicks=_int(row, "link_clicks"),
            landing_page_views=_int(row, "landing_page_views"),
            view_item=_int(row, "view_item"),
            add_to_cart=_int(row, "add_to_cart"),
            begin_checkout=_int(row, "begin_checkout"),
            purchases=_int(row, "purchases"),
            revenue=_float(row, "revenue"),
        )


@dataclass(frozen=True)
class ReconciliationRow:
    date: str
    platform: str
    event: str
    platform_count: int
    site_count: int
    scope: str

    @classmethod
    def from_row(cls, row: Mapping[str, str]) -> "ReconciliationRow":
        return cls(
            date=row["date"],
            platform=row["platform"],
            event=row["event"],
            platform_count=_int(row, "platform_count"),
            site_count=_int(row, "site_count"),
            scope=row["scope"],
        )
