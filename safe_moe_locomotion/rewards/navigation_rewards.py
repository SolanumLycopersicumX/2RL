"""Navigation reward term names and defaults."""

DEFAULT_NAVIGATION_REWARD_TERMS = {
    "goal_progress": 1.0,
    "goal_reached": 5.0,
    "heading_alignment": 0.5,
    "obstacle_clearance": 0.25,
    "collision_penalty": -5.0,
}

