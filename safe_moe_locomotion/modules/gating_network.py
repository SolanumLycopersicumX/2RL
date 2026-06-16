"""Gating networks for expert routing."""

from __future__ import annotations


class TorchGatingNetwork:
    """Small MLP gate with softmax output.

    This wrapper delays importing torch until construction so lightweight
    repository checks can run before the deep-learning stack is installed.
    """

    def __init__(self, input_dim: int, num_experts: int, hidden_dim: int = 256) -> None:
        if input_dim <= 0:
            raise ValueError("input_dim must be positive")
        if num_experts < 2:
            raise ValueError("num_experts must be at least 2")

        import torch.nn as nn

        class _Gate(nn.Module):
            def __init__(self) -> None:
                super().__init__()
                self.net = nn.Sequential(
                    nn.Linear(input_dim, hidden_dim),
                    nn.ELU(),
                    nn.Linear(hidden_dim, hidden_dim),
                    nn.ELU(),
                    nn.Linear(hidden_dim, num_experts),
                )

            def forward(self, x):
                import torch

                logits = self.net(x)
                return torch.softmax(logits, dim=-1)

            def get_logits(self, x):
                return self.net(x)

        self.model = _Gate()

    def __call__(self, x: object) -> object:
        return self.model(x)

    def get_logits(self, x: object) -> object:
        return self.model.get_logits(x)

