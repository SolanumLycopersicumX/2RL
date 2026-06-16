"""Expert training adapter placeholder."""

EXPERT_NAMES = ("flat", "rough", "stair", "gap", "recovery")


def validate_expert_name(name: str) -> None:
    if name not in EXPERT_NAMES:
        allowed = ", ".join(EXPERT_NAMES)
        raise ValueError(f"unknown expert '{name}', expected one of: {allowed}")

