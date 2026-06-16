"""Shared contracts for legged-locomotion environments.

Concrete Isaac Lab, legged_gym, or Unitree adapters should satisfy these
contracts so policy and evaluation code does not depend on one simulator.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ObservationSpec:
    proprioception_dim: int
    command_dim: int
    action_dim: int
    terrain_dim: int = 0
    history_steps: int = 1


@dataclass(frozen=True)
class StepResult:
    observation: object
    reward: float
    terminated: bool
    truncated: bool
    info: dict[str, object]


class LeggedEnv(Protocol):
    """Minimal simulator-agnostic interface used by trainers/evaluators."""

    observation_spec: ObservationSpec

    def reset(self, seed: int | None = None) -> object:
        """Reset the environment and return the initial observation."""

    def step(self, action: object) -> StepResult:
        """Advance one simulation step."""

