"""Terrain encoders."""

from __future__ import annotations


class TorchTerrainEncoder:
    def __init__(self, input_dim: int, latent_dim: int, hidden_dim: int = 128) -> None:
        if input_dim <= 0 or latent_dim <= 0:
            raise ValueError("input_dim and latent_dim must be positive")

        import torch.nn as nn

        self.model = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ELU(),
            nn.Linear(hidden_dim, latent_dim),
            nn.ELU(),
        )

    def __call__(self, terrain_obs: object) -> object:
        return self.model(terrain_obs)

