"""Gate training adapter placeholder."""


def require_frozen_expert_paths(paths: list[str]) -> None:
    if len(paths) < 2:
        raise ValueError("gate training requires at least two frozen experts")

