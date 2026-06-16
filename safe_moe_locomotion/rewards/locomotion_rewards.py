"""Locomotion reward term names and defaults."""

DEFAULT_LOCOMOTION_REWARD_TERMS = {
    "linear_velocity_tracking": 1.0,
    "angular_velocity_tracking": 0.5,
    "vertical_velocity_penalty": -2.0,
    "roll_pitch_penalty": -1.0,
    "torque_penalty": -1.0e-5,
    "joint_acceleration_penalty": -2.5e-7,
    "action_rate_penalty": -0.01,
    "collision_penalty": -1.0,
    "feet_air_time_reward": 1.0,
}

