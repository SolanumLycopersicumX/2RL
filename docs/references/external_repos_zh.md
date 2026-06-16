# 外部仓库清单

不要把这些外部仓库直接复制进主 Python 包。需要时克隆到 `external/`，并在实验记录中保存 commit hash。

| 仓库 | 用途 | 建议位置 | 备注 |
|---|---|---|---|
| https://github.com/isaac-sim/IsaacLab | 现代 Isaac Lab / Isaac Sim 训练框架 | `external/IsaacLab` | 新工作优先路线。 |
| https://github.com/leggedrobotics/rsl_rl | PPO 和 robotics RL 算法 | PyPI 或 `external/rsl_rl` | 修改源码时再 clone。 |
| https://github.com/leggedrobotics/legged_gym | legacy Isaac Gym locomotion baseline | `external/legged_gym` | 用于经典 ANYmal baseline 复现。 |
| https://github.com/unitreerobotics/unitree_rl_gym | Unitree Go2/G1/H1 示例 | `external/unitree_rl_gym` | 迁移到 Unitree 机器人时参考。 |
| https://github.com/roboterax/humanoid-gym | 人形机器人 locomotion baseline | `external/humanoid-gym` | 四足 MoE 稳定后再看。 |
| https://github.com/google-deepmind/mujoco | MuJoCo 仿真器 | pip 或外部依赖 | 用于 sim-to-sim 验证。 |
| https://github.com/stack-of-tasks/pinocchio | 刚体动力学库 | optional dependency | 后期动力学分析。 |
