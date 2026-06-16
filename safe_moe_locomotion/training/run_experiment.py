"""Lightweight training command dispatcher.

This module validates project configs and prints the intended backend command.
Real Isaac Lab or legged_gym training adapters should be added here once the
heavy simulator environment is installed.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from safe_moe_locomotion.utils.config import load_yaml


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="2RL experiment dispatcher")
    parser.add_argument("--config", required=True, help="Path to YAML config")
    parser.add_argument("--dry-run", action="store_true", help="Validate without launching training")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config_path = Path(args.config)
    config = load_yaml(config_path)

    summary = {
        "config": str(config_path),
        "experiment": config.get("experiment", {}),
        "backend": config.get("backend", "unassigned"),
        "dry_run": args.dry_run,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))

    if not args.dry_run:
        raise SystemExit(
            "Real training adapter is not enabled yet. Install Isaac Lab or "
            "legacy legged_gym, then implement backend dispatch here."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

