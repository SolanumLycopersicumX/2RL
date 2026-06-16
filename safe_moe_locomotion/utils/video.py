"""Video artifact conventions."""

from __future__ import annotations

from pathlib import Path


def video_output_path(experiment_name: str, run_name: str, suffix: str = "mp4") -> Path:
    return Path("assets/videos") / experiment_name / f"{run_name}.{suffix}"

