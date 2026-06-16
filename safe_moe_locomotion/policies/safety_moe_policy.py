"""Safety-aware MoE routing."""

from __future__ import annotations

from typing import Sequence


class TorchSafetyAwareMoEPolicy:
    """Bias or override MoE routing using a risk estimator."""

    def __init__(
        self,
        experts: Sequence[object],
        gate: object,
        risk_estimator: object,
        recovery_id: int,
        alpha: float = 2.0,
    ) -> None:
        if not 0 <= recovery_id < len(experts):
            raise ValueError("recovery_id must index an expert")
        self.experts = list(experts)
        self.gate = gate
        self.risk_estimator = risk_estimator
        self.recovery_id = recovery_id
        self.alpha = alpha

    def __call__(self, obs: object, gate_obs: object, risk_obs: object) -> tuple[object, object, object]:
        import torch

        logits = self.gate.get_logits(gate_obs)
        risk_score = self.risk_estimator(risk_obs)
        logits[:, self.recovery_id] = logits[:, self.recovery_id] + self.alpha * risk_score.squeeze(-1)
        weights = torch.softmax(logits, dim=-1)
        expert_actions = torch.stack([expert(obs) for expert in self.experts], dim=1)
        action = torch.sum(weights.unsqueeze(-1) * expert_actions, dim=1)
        return action, weights, risk_score

