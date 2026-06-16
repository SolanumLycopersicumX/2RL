"""Mixture-of-experts policy composition."""

from __future__ import annotations

from typing import Sequence


def validate_moe_shapes(num_experts: int, action_dim: int) -> None:
    if num_experts < 2:
        raise ValueError("MoE needs at least two experts")
    if action_dim <= 0:
        raise ValueError("action_dim must be positive")


class TorchMoEPolicy:
    """Torch implementation of action-space MoE.

    Experts are expected to be callables returning tensors shaped
    `[batch, action_dim]`. The gate returns weights shaped `[batch, experts]`.
    """

    def __init__(self, experts: Sequence[object], gate: object) -> None:
        validate_moe_shapes(len(experts), action_dim=1)
        self.experts = list(experts)
        self.gate = gate

    def __call__(self, obs: object, gate_obs: object) -> tuple[object, object]:
        import torch

        weights = self.gate(gate_obs)
        expert_actions = torch.stack([expert(obs) for expert in self.experts], dim=1)
        action = torch.sum(weights.unsqueeze(-1) * expert_actions, dim=1)
        return action, weights

