#!/usr/bin/env python3
"""Validate that the project scaffold is complete enough to resume safely."""

from __future__ import annotations

from pathlib import Path


REQUIRED_PATHS = [
    "README.md",
    "Codex_Log.md",
    "rl_locomotion_moe_research_plan.md",
    "environment.yml",
    "requirements.txt",
    "requirements-dev.txt",
    "pyproject.toml",
    "docs/project_index.md",
    "docs/project_structure.md",
    "experiments/README.md",
    "docs/references/paper_index.md",
    "docs/references/external_repos.md",
    "docs/references/papers/papers_manifest.csv",
    "docs/setup/ENVIRONMENT.md",
    "docs/setup/PACKAGE_INVENTORY.md",
    "docs/future_work/claim_boundary.md",
    "configs/robot/anymal.yaml",
    "configs/terrain/mixed.yaml",
    "configs/train/ppo_flat.yaml",
    "configs/moe/safety_moe.yaml",
    "safe_moe_locomotion/modules/gating_network.py",
    "safe_moe_locomotion/modules/risk_estimator.py",
    "safe_moe_locomotion/policies/moe_policy.py",
    "safe_moe_locomotion/policies/safety_moe_policy.py",
    "safe_moe_locomotion/rewards/moe_regularization.py",
    "safe_moe_locomotion/evaluation/ablation.py",
]


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    missing = [path for path in REQUIRED_PATHS if not (root / path).exists()]
    if missing:
        print("Missing required paths:")
        for path in missing:
            print(f"- {path}")
        return 1

    paper_index = (root / "docs/references/paper_index.md").read_text(encoding="utf-8")
    arxiv_count = paper_index.count("https://arxiv.org/abs/")
    if arxiv_count < 26:
        print(f"Expected at least 26 arXiv paper links, found {arxiv_count}")
        return 1

    print("Project scaffold validation passed.")
    print(f"Found {len(REQUIRED_PATHS)} required paths.")
    print(f"Found {arxiv_count} arXiv paper links.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
