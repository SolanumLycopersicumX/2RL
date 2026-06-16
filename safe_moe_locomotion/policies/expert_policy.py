"""Expert policy wrappers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ExpertMetadata:
    name: str
    terrain: str
    checkpoint_path: Path
    observation_dim: int
    action_dim: int


class ExpertLoadError(RuntimeError):
    """Raised when an expert checkpoint cannot be loaded."""


def validate_expert_metadata(expert: ExpertMetadata) -> None:
    if not expert.name:
        raise ValueError("expert name must be non-empty")
    if expert.observation_dim <= 0:
        raise ValueError("observation_dim must be positive")
    if expert.action_dim <= 0:
        raise ValueError("action_dim must be positive")

