# External Repositories

Do not vendor these repositories into the main package. Clone them under
`external/` if needed and record the commit hash used for an experiment.

| Repository | Role | Suggested Location | Notes |
|---|---|---|---|
| https://github.com/isaac-sim/IsaacLab | Primary modern simulation and RL task framework | `external/IsaacLab` | Recommended path for new work. |
| https://github.com/leggedrobotics/rsl_rl | PPO and robotics RL algorithms | dependency or `external/rsl_rl` | Install from PyPI for normal use; clone for modification. |
| https://github.com/leggedrobotics/legged_gym | Legacy Isaac Gym locomotion baseline | `external/legged_gym` | Useful for reproducing classic ANYmal baselines; limited updates. |
| https://github.com/unitreerobotics/unitree_rl_gym | Unitree Go2/G1 training and deployment examples | `external/unitree_rl_gym` | Useful once moving from ANYmal-style baseline to Unitree robots. |
| https://github.com/roboterax/humanoid-gym | Humanoid locomotion baseline and sim-to-sim reference | `external/humanoid-gym` | Use after quadruped MoE path is stable. |
| https://github.com/google-deepmind/mujoco | MuJoCo simulator | package dependency | Use for sim-to-sim validation. |
| https://github.com/stack-of-tasks/pinocchio | Rigid-body dynamics library | optional dependency | Useful for dynamics analysis and later control integration. |
