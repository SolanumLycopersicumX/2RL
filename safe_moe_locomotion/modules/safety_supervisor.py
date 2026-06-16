"""Simple safety supervisor policies."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SafetyDecision:
    use_recovery: bool
    risk_score: float
    threshold: float


def threshold_recovery_decision(risk_score: float, threshold: float) -> SafetyDecision:
    if not 0.0 <= risk_score <= 1.0:
        raise ValueError("risk_score must be in [0, 1]")
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("threshold must be in [0, 1]")
    return SafetyDecision(
        use_recovery=risk_score > threshold,
        risk_score=risk_score,
        threshold=threshold,
    )

