"""Build and render a complete control-tower report."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .analytics import aggregate_campaigns, creative_fatigue_report, funnel_report, reconciliation_report
from .ingest import load_campaigns, load_reconciliation
from .recommendations import recommend


def build_report(data_dir: Path) -> dict[str, Any]:
    campaign_rows = load_campaigns(data_dir / "campaign_daily.csv")
    reconciliation_rows = load_reconciliation(data_dir / "reconciliation.csv")
    campaign_metrics = aggregate_campaigns(campaign_rows)
    return {
        "project": "E-commerce Growth Control Tower",
        "data_status": "synthetic portfolio data",
        "campaigns": campaign_metrics,
        "funnel": funnel_report(campaign_rows),
        "reconciliation": reconciliation_report(reconciliation_rows),
        "creative_fatigue": creative_fatigue_report(campaign_rows),
        "recommendations": recommend(campaign_metrics),
        "warnings": [
            "The sample is synthetic and does not establish client performance.",
            "Platform and site counts may have different attribution windows, timezones, and event definitions.",
            "ROAS is illustrative only when the synthetic revenue field is present.",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# {report['project']}",
        "",
        f"**Data status:** {report['data_status']}",
        "",
        "## Campaign summary",
        "",
        "| Platform | Campaign | Spend | Clicks | CTR | Purchases | ROAS |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for campaign in report["campaigns"]:
        roas = "—" if campaign["roas"] is None else f"{campaign['roas']:.2f}"
        ctr = "—" if campaign["ctr_pct"] is None else f"{campaign['ctr_pct']:.2f}%"
        lines.append(
            f"| {campaign['platform']} | {campaign['campaign']} | {campaign['spend']:.2f} | "
            f"{campaign['link_clicks']} | {ctr} | {campaign['purchases']} | {roas} |"
        )
    lines.extend(["", "## Funnel", "", "| Stage | Count | Previous-stage rate | Drop |", "| --- | ---: | ---: | ---: |"])
    for stage in report["funnel"]:
        rate = "—" if stage["previous_stage_rate_pct"] is None else f"{stage['previous_stage_rate_pct']:.2f}%"
        drop = "—" if stage["drop_from_previous"] is None else str(stage["drop_from_previous"])
        lines.append(f"| {stage['stage']} | {stage['count']} | {rate} | {drop} |")
    lines.extend(["", "## Recommendations", ""])
    for item in report["recommendations"]:
        lines.append(f"- **{item['platform']} / {item['campaign']}: {item['action']}** — {item['reason']}")
    lines.extend(["", "## Guardrails", ""])
    lines.extend(f"- {warning}" for warning in report["warnings"])
    return "\n".join(lines) + "\n"


def report_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, sort_keys=False)
