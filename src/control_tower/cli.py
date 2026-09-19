"""Command-line entry point for the control tower."""

from __future__ import annotations

import argparse
from pathlib import Path

from .report import build_report, render_markdown, report_json


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path(__file__).parents[2] / "data")
    parser.add_argument("--json", action="store_true", help="render JSON")
    parser.add_argument("--markdown", action="store_true", help="render Markdown")
    args = parser.parse_args()
    report = build_report(args.data_dir)
    if args.json:
        print(report_json(report))
    else:
        print(render_markdown(report) if args.markdown else render_markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
