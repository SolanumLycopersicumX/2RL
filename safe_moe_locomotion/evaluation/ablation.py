"""Ablation group definitions."""

ABLATION_GROUPS = {
    "A": "single_policy",
    "B": "rule_based_switch",
    "C": "frozen_experts_vanilla_gate",
    "D": "frozen_experts_safety_gate",
    "E": "joint_finetuned_moe",
    "F": "safety_aware_cmoe",
    "G": "residual_expert_moe",
}

