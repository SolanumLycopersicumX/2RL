"""Residual expert composition utilities."""

from __future__ import annotations


class TorchResidualExpertPolicy:
    """Compose a base policy with weighted residual expert corrections."""

    def __init__(self, base_policy: object, residual_experts: list[object], gate: object) -> None:
        if not residual_experts:
            raise ValueError("residual_experts must be non-empty")
        self.base_policy = base_policy
        self.residual_experts = residual_experts
        self.gate = gate

    def __call__(self, obs: object, gate_obs: object) -> tuple[object, object]:
        import torch

        base_action = self.base_policy(obs)
        weights = self.gate(gate_obs)
        residuals = torch.stack([expert(obs) for expert in self.residual_experts], dim=1)
        residual = torch.sum(weights.unsqueeze(-1) * residuals, dim=1)
        return base_action + residual, weights

