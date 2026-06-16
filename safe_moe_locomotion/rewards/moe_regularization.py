"""Regularization terms for MoE routing."""

from __future__ import annotations


def torch_gate_entropy(weights: object, eps: float = 1e-8) -> object:
    import torch

    return -torch.sum(weights * torch.log(weights + eps), dim=-1).mean()


def torch_load_balance_loss(weights: object) -> object:
    import torch

    return torch.var(weights.mean(dim=0))


def torch_temporal_smoothness(weights_t: object, weights_prev: object) -> object:
    import torch

    return torch.mean((weights_t - weights_prev) ** 2)


def torch_contrastive_routing_loss(
    gate_a: object,
    gate_b: object,
    same_terrain: object,
    margin: float = 0.5,
) -> object:
    import torch

    distance = torch.norm(gate_a - gate_b, dim=-1)
    positive = same_terrain.float() * distance.pow(2)
    negative = (1.0 - same_terrain.float()) * torch.relu(margin - distance).pow(2)
    return (positive + negative).mean()

