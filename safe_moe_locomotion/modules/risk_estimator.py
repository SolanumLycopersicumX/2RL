"""Risk estimator for safety-aware routing."""

from __future__ import annotations


class TorchRiskEstimator:
    def __init__(self, input_dim: int, hidden_dim: int = 128) -> None:
        if input_dim <= 0:
            raise ValueError("input_dim must be positive")

        import torch.nn as nn

        self.model = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ELU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ELU(),
            nn.Linear(hidden_dim, 1),
            nn.Sigmoid(),
        )

    def __call__(self, risk_obs: object) -> object:
        return self.model(risk_obs)

