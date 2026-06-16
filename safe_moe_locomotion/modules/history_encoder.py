"""Proprioception history encoders."""

from __future__ import annotations


class TorchHistoryEncoder:
    def __init__(self, input_dim: int, latent_dim: int, hidden_dim: int = 128) -> None:
        if input_dim <= 0 or latent_dim <= 0:
            raise ValueError("input_dim and latent_dim must be positive")

        import torch.nn as nn

        self.model = nn.GRU(input_dim, hidden_dim, batch_first=True)
        self.projection = nn.Sequential(nn.Linear(hidden_dim, latent_dim), nn.ELU())

    def __call__(self, history: object) -> object:
        _, hidden = self.model(history)
        return self.projection(hidden[-1])

