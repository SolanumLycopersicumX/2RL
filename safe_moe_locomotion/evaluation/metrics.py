"""Experiment metric helpers."""

from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class EvaluationSummary:
    episodes: int
    success_rate: float
    fall_rate: float
    collision_rate: float
    average_speed: float
    tracking_error: float
    energy: float

    def to_dict(self) -> dict[str, float | int]:
        return asdict(self)


def validate_rate(name: str, value: float) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be in [0, 1]")

