"""CSV ingestion with a small, explicit schema."""

from __future__ import annotations

import csv
from pathlib import Path

from .models import CampaignRow, ReconciliationRow


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_campaigns(path: Path) -> list[CampaignRow]:
    return [CampaignRow.from_row(row) for row in _read(path)]


def load_reconciliation(path: Path) -> list[ReconciliationRow]:
    return [ReconciliationRow.from_row(row) for row in _read(path)]
