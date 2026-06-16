"""Checkpoint path helpers."""

from __future__ import annotations

from pathlib import Path


def default_checkpoint_path(experiment_name: str, run_name: str, model_name: str) -> Path:
    if not experiment_name or not run_name or not model_name:
        raise ValueError("experiment_name, run_name, and model_name are required")
    return Path("models") / experiment_name / run_name / model_name
