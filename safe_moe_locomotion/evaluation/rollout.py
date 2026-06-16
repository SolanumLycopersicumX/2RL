"""Rollout helpers."""

from __future__ import annotations


def rollout_not_implemented_message(backend: str) -> str:
    return (
        f"Rollout backend '{backend}' is not wired yet. Install the simulator "
        "and add an adapter under safe_moe_locomotion/envs/."
    )

