# RL Locomotion & Navigation for Legged Robots 实习前学习与复现计划

> 目标方向：**RL-based locomotion / perceptive navigation / MoE skill composition / safety-aware control for humanoid and quadruped robots**  
> 适用场景：准备进入 **VLA / Embodied AI / Legged Robotics / Humanoid Robotics / Robot Learning** 相关科研团队或公司实习。  
> 使用方式：可以将本文档直接放入 Codex / Cursor / Claude Code / ChatGPT Projects 中，作为长期执行计划与项目说明。

---

## 0. 总目标

本计划的最终目标不是“只读论文”，而是做出一个可以放进简历、GitHub、面试展示和科研申请中的项目：

> **Safety-Aware Mixture-of-Experts Locomotion for Legged Local Navigation**

核心思路：

```text
observation / terrain / command / goal
        ↓
terrain encoder / proprioception history encoder / risk estimator
        ↓
MoE gate / safety switch
        ↓
flat expert / rough terrain expert / stair expert / gap expert / recovery expert
        ↓
joint targets / torque / gait command
        ↓
quadruped or humanoid locomotion and navigation
```

最终希望实现：

1. 跑通一个四足机器人 RL locomotion baseline。
2. 在仿真中训练多个 terrain-specialized experts。
3. 实现一个 MoE gating policy 来选择或混合不同专家策略。
4. 加入 safety-aware routing / recovery expert。
5. 做 ablation study，对比 single policy、rule-based switch、vanilla MoE、safety-aware MoE。
6. 输出一份完整的 GitHub repo、实验报告、demo video/GIF、简历项目描述。

---

## 1. 方向定位

这个方向可以命名为：

```text
RL Locomotion + Perceptive Navigation + MoE Skill Composition + Sim-to-Real
```

对应岗位包括：

- Robot Learning Research Intern
- Legged Locomotion Intern
- Humanoid Robotics Intern
- Embodied AI Research Intern
- Robotics Software / RL Infrastructure Intern
- Sim-to-Real Research Intern
- VLA Robotics Intern with locomotion/navigation focus

和纯 VLA 的区别：

| 方向 | 核心输入 | 核心输出 | 重点 |
|---|---|---|---|
| VLA manipulation | image + language + robot state | arm action / gripper action | 视觉语言理解、机械臂操作 |
| RL locomotion | proprioception + command + terrain | joint target / torque / gait | 稳定移动、平衡、控制、sim-to-real |
| Perceptive navigation | depth / height map + goal + state | local motion command / joint action | 避障、寻路、复杂地形 |
| MoE locomotion | state + terrain embedding + risk | expert weights / expert selection | 多技能组合、安全切换 |

---

## 2. 必学知识点总览

### 2.1 机器人运动与控制基础

必须理解以下概念：

| 模块 | 关键词 | 需要达到的程度 |
|---|---|---|
| Rigid Body Dynamics | mass matrix, Coriolis, gravity term | 看懂机器人动力学方程含义 |
| Contact Dynamics | friction cone, contact constraint, ground reaction force | 理解脚接触地面的限制 |
| Hybrid Dynamics | contact / flight phase switching | 理解为什么腿式机器人难控制 |
| Centroidal Dynamics | CoM, centroidal momentum | 理解平衡和身体整体运动 |
| ZMP / Capture Point | humanoid balance | 人形机器人重点 |
| Whole-Body Control | inverse dynamics QP, task-space control | 理解传统控制器如何接 RL |
| MPC / NMPC | predictive control, footstep planning | 理解 model-based locomotion |
| PD Control | joint target, stiffness, damping | 理解 RL action 如何落到电机控制 |

关键问题：

```text
1. 机器人为什么会摔倒？
2. 什么是 support polygon？
3. 为什么摩擦系数变化会导致 sim-to-real 失败？
4. 为什么 RL policy 通常输出 joint position target，而不是直接输出 torque？
5. 为什么人形机器人比四足机器人更难？
6. 为什么真实机器人需要 safety controller / recovery behavior？
```

---

### 2.2 强化学习基础

必须掌握：

| 模块 | 关键词 |
|---|---|
| RL 基础 | state, observation, action, reward, policy, value |
| Actor-Critic | actor, critic, value function |
| PPO | clipped objective, advantage, entropy |
| GAE | generalized advantage estimation |
| Reward Shaping | tracking reward, energy penalty, fall penalty |
| Curriculum Learning | 从简单地形逐渐增加难度 |
| Domain Randomization | mass, friction, latency, noise, motor strength |
| Privileged Learning | teacher 用完整信息，student 用真实可观测信息 |
| Recurrent Policy | GRU/LSTM history encoder |
| Sim-to-Real | actuator model, system identification, latency modeling |
| Evaluation | success rate, fall rate, collision rate, cost of transport |

必须能解释这个 pipeline：

```text
observation
    ↓
actor policy
    ↓
action
    ↓
PD controller / torque controller
    ↓
physics simulator
    ↓
reward
    ↓
PPO update
```

---

### 2.3 腿式机器人 RL 特有知识点

必须理解：

| 内容 | 解释 |
|---|---|
| Observation space | base velocity, angular velocity, gravity vector, joint position, joint velocity, previous action |
| Action space | joint position target, joint velocity target, torque |
| Command space | desired linear velocity, desired yaw velocity, heading command |
| Reward terms | velocity tracking, orientation, torque penalty, action smoothness, foot clearance |
| Termination | fall, body collision, excessive tilt |
| Terrain curriculum | plane, slope, stairs, rough terrain, gaps |
| Random pushes | 模拟外力扰动 |
| Actuator model | 模拟真实电机延迟和非线性 |
| History adaptation | 通过历史观测估计隐含动力学参数 |

---

### 2.4 感知寻路与局部导航

从普通 locomotion 到 navigation 的变化：

```text
普通 locomotion:
    track commanded velocity

perceptive navigation:
    reach goal while avoiding obstacles and unsafe terrain
```

需要补：

| 内容 | 作用 |
|---|---|
| Height map | 地形高度信息 |
| Depth image | 前方障碍物/地形视觉 |
| Terrain encoder | 将地形编码成 latent vector |
| Local planner | 给出局部目标或速度命令 |
| Goal-conditioned policy | 输入目标位置或 heading |
| Collision avoidance | 避免身体/腿撞障碍物 |
| Risk estimation | 判断当前动作是否可能导致失败 |
| Recovery policy | 危险时恢复稳定 |

---

### 2.5 MoE / 多策略组合

你要重点研究：

```text
多个 expert policy 如何组合？
gate 根据什么决定专家权重？
如何避免 expert collapse？
如何避免 gate 高频抖动？
如何保证切换动作连续？
如何加入安全判断？
```

相关概念：

| 内容 | 解释 |
|---|---|
| Mixture of Experts | 多个专家网络 + 一个 gate |
| Hard Routing | 只选择一个 expert |
| Soft Routing | 多个 expert action 加权平均 |
| Top-k Routing | 选择前 k 个 expert |
| Load Balancing Loss | 避免只用一个 expert |
| Entropy Regularization | 控制 gate 分布 |
| Contrastive Routing | 让不同地形激活不同 expert |
| Temporal Smoothness | 避免 gate 抖动 |
| Residual Experts | 每个 expert 输出 residual action |
| Safety Supervisor | 高风险时强制切到 recovery expert |

---

## 3. 必读论文路线

### 3.1 四足 RL locomotion 基础论文

建议阅读顺序：

1. **Learning to Walk in Minutes Using Massively Parallel Deep Reinforcement Learning**
   - 关键词：Isaac Gym, massively parallel simulation, PPO, legged_gym
   - 学习点：为什么大规模并行仿真能让腿式机器人 RL 快速训练。

2. **Sim-to-Real: Learning Agile Locomotion for Quadruped Robots**
   - 关键词：sim-to-real, actuator model, domain randomization
   - 学习点：如何让仿真训练出的策略迁移到真实四足机器人。

3. **Learning Agile and Dynamic Motor Skills for Legged Robots**
   - 关键词：dynamic locomotion, ANYmal, agile skills
   - 学习点：如何训练动态运动技能。

4. **Learning Quadrupedal Locomotion over Challenging Terrain**
   - 关键词：rough terrain, proprioceptive locomotion
   - 学习点：不依赖视觉时如何通过本体感知完成复杂地形移动。

5. **RMA: Rapid Motor Adaptation for Legged Robots**
   - 关键词：adaptation module, base policy, latent environment factors
   - 学习点：如何通过历史观测估计摩擦、负载、地形等隐变量。

---

### 3.2 感知寻路 / Parkour / Agile Navigation 论文

1. **Advanced Skills by Learning Locomotion and Local Navigation End-to-End**
   - 关键词：local navigation, end-to-end locomotion
   - 学习点：从 velocity tracking 升级到 navigation。

2. **Robot Parkour Learning**
   - 关键词：parkour skills, depth camera, DAgger, distillation
   - 学习点：如何让机器人学会 climb / leap / crawl / squeeze / run 等技能。

3. **Extreme Parkour with Legged Robots**
   - 关键词：depth camera, extreme terrain, agile locomotion
   - 学习点：单目/深度感知下的复杂动作。

4. **Learning Agile Locomotion on Risky Terrains**
   - 关键词：risky terrain, stepping stones, narrow beams
   - 学习点：将 risky terrain 建模成 navigation 问题，而不是简单速度跟踪。

5. **Resilient Legged Local Navigation**
   - 关键词：local navigation, robustness, perception failure
   - 学习点：感知不完美时如何仍然安全导航。

6. **Agile But Safe: Learning Collision-Free High-Speed Legged Locomotion**
   - 关键词：agile policy, recovery policy, reach-avoid value network, safety switch
   - 学习点：高速运动中如何平衡速度和安全。

---

### 3.3 人形机器人 RL locomotion 论文

1. **Real-World Humanoid Locomotion with Reinforcement Learning**
   - 关键词：humanoid locomotion, transformer policy, sim-to-real
   - 学习点：真实人形机器人 locomotion 的训练和部署。

2. **Humanoid-Gym**
   - 关键词：Isaac Gym, humanoid locomotion, zero-shot sim-to-real
   - 学习点：开源人形机器人 RL 训练框架。

3. **H2O: Learning Human-to-Humanoid Real-Time Whole-Body Teleoperation**
   - 关键词：whole-body teleoperation, motion imitation, sim-to-data
   - 学习点：如何从人体动作到人形机器人全身控制。

4. **OmniH2O**
   - 关键词：humanoid teleoperation, autonomy, whole-body control
   - 学习点：更通用的人形机器人遥操作/自主框架。

5. **WoCoCo**
   - 关键词：whole-body contacts, sequential contacts
   - 学习点：复杂接触序列下的人形机器人运动。

6. **BeamDojo**
   - 关键词：sparse footholds, humanoid risky terrain
   - 学习点：人形机器人在稀疏落脚点和危险地形上的移动。

---

### 3.4 MoE / 多策略 gating 论文

1. **MoE-Loco: Mixture of Experts for Multitask Locomotion**
   - 关键词：Mixture of Experts, multitask locomotion, quadruped, bipedal gait
   - 学习点：如何用 MoE 缓解多任务 locomotion 的 gradient conflicts。

2. **CMoE: Contrastive Mixture of Experts for Motion Control and Terrain Adaptation**
   - 关键词：contrastive routing, expert specialization, terrain adaptation
   - 学习点：如何防止 gate 变成均匀分配，增强专家分工。

3. **MoRE: Mixture of Residual Experts for Humanoid Lifelike Gaits**
   - 关键词：residual experts, humanoid gait, terrain adaptation
   - 学习点：为什么 residual expert 可能比直接 action mixture 更稳定。

4. **Parkour in the Wild**
   - 关键词：terrain-specific experts, DAgger distillation, RL fine-tuning
   - 学习点：多专家到统一策略的蒸馏路线。

5. **Toward Reliable Sim-to-Real Predictability for MoE-based Robust Quadrupedal Locomotion**
   - 关键词：MoE, robust quadrupedal locomotion, sim-to-real predictability
   - 学习点：MoE 策略在真实部署前如何评估可靠性。

---

## 4. 推荐工具栈

### 4.1 必装工具

```text
Python >= 3.10
PyTorch
NumPy
Matplotlib
TensorBoard / Weights & Biases
Git
Conda / Mamba
CUDA Toolkit
NVIDIA Driver
```

### 4.2 仿真与训练框架

优先级如下：

| 优先级 | 工具 | 用途 |
|---|---|---|
| 1 | Isaac Gym / Isaac Lab | 大规模并行机器人 RL |
| 1 | rsl_rl | PPO 训练框架 |
| 1 | legged_gym | 四足 locomotion baseline |
| 2 | Unitree RL Gym | Go2 / H1 / G1 等 Unitree 机器人 |
| 2 | Humanoid-Gym | 人形机器人 locomotion baseline |
| 3 | MuJoCo | sim-to-sim 验证 |
| 3 | ROS 2 | 后期真实机器人系统集成 |
| 3 | Pinocchio / RBDL | 机器人动力学计算 |

### 4.3 建议先选的机器人模型

先做四足，再做人形：

```text
阶段 1：ANYmal / Unitree A1 / Unitree Go2
阶段 2：Unitree G1 / H1
阶段 3：humanoid whole-body locomotion / teleoperation
```

原因：

```text
四足更容易稳定训练；
人形更容易卡在平衡、奖励、接触、摔倒恢复；
先在四足上验证 MoE gating，再迁移到人形更稳。
```

---

## 5. 项目总路线

### 项目名称

```text
Safety-Aware MoE-Gated Locomotion for Legged Local Navigation
```

### 项目目标

实现一个基于 MoE gating 的四足机器人局部导航系统：

```text
输入：
    proprioception history
    velocity command / goal command
    terrain embedding
    risk estimate

输出：
    selected expert / expert weights
    joint position target or action residual

专家：
    flat locomotion expert
    rough terrain expert
    stair expert
    gap / stepping-stone expert
    recovery expert
```

### 最终对比实验

| 方法 | 描述 |
|---|---|
| Single Policy | 一个大 policy 处理所有地形 |
| Rule-Based Switch | 手写规则切换不同 expert |
| Vanilla MoE | 普通 softmax gate |
| Safety-Aware MoE | 加 risk estimator / safety switch |
| Safety-Aware CMoE | 加 contrastive routing / temporal smoothness |

### 评价指标

```text
success rate
fall rate
collision rate
average speed
velocity tracking error
goal reaching error
energy consumption
cost of transport
expert utilization
gate entropy
gate switching frequency
OOD terrain performance
recovery success rate
```

---

## 6. 推荐仓库结构

Codex 可以按这个结构创建项目：

```text
safe-moe-locomotion/
├── README.md
├── requirements.txt
├── environment.yml
├── scripts/
│   ├── train_flat_expert.sh
│   ├── train_rough_expert.sh
│   ├── train_stair_expert.sh
│   ├── train_gap_expert.sh
│   ├── train_recovery_expert.sh
│   ├── train_gate.sh
│   ├── evaluate_all.sh
│   └── export_policy.sh
├── configs/
│   ├── robot/
│   │   ├── anymal.yaml
│   │   ├── unitree_a1.yaml
│   │   ├── unitree_go2.yaml
│   │   └── unitree_g1.yaml
│   ├── terrain/
│   │   ├── flat.yaml
│   │   ├── rough.yaml
│   │   ├── stairs.yaml
│   │   ├── gaps.yaml
│   │   └── mixed.yaml
│   ├── train/
│   │   ├── ppo_flat.yaml
│   │   ├── ppo_rough.yaml
│   │   ├── ppo_stair.yaml
│   │   ├── ppo_gap.yaml
│   │   ├── ppo_recovery.yaml
│   │   └── ppo_gate.yaml
│   └── moe/
│       ├── vanilla_moe.yaml
│       ├── safety_moe.yaml
│       └── contrastive_moe.yaml
├── safe_moe_locomotion/
│   ├── __init__.py
│   ├── envs/
│   │   ├── base_legged_env.py
│   │   ├── flat_env.py
│   │   ├── rough_env.py
│   │   ├── stair_env.py
│   │   ├── gap_env.py
│   │   ├── recovery_env.py
│   │   └── mixed_nav_env.py
│   ├── policies/
│   │   ├── actor_critic.py
│   │   ├── expert_policy.py
│   │   ├── moe_policy.py
│   │   ├── safety_moe_policy.py
│   │   └── residual_expert_policy.py
│   ├── modules/
│   │   ├── terrain_encoder.py
│   │   ├── history_encoder.py
│   │   ├── risk_estimator.py
│   │   ├── gating_network.py
│   │   └── safety_supervisor.py
│   ├── rewards/
│   │   ├── locomotion_rewards.py
│   │   ├── navigation_rewards.py
│   │   ├── recovery_rewards.py
│   │   └── moe_regularization.py
│   ├── training/
│   │   ├── ppo_trainer.py
│   │   ├── expert_trainer.py
│   │   ├── gate_trainer.py
│   │   └── distillation_trainer.py
│   ├── evaluation/
│   │   ├── metrics.py
│   │   ├── rollout.py
│   │   ├── terrain_sweep.py
│   │   ├── ablation.py
│   │   └── visualize_gate.py
│   └── utils/
│       ├── config.py
│       ├── logging.py
│       ├── checkpoints.py
│       └── video.py
├── notebooks/
│   ├── 01_reward_analysis.ipynb
│   ├── 02_gate_visualization.ipynb
│   └── 03_ablation_plots.ipynb
├── docs/
│   ├── paper_notes/
│   ├── experiment_log.md
│   ├── implementation_notes.md
│   └── final_report.md
└── assets/
    ├── figures/
    ├── videos/
    └── gifs/
```

---

## 7. Milestone 1：跑通 RL locomotion baseline

### 目标

先不要上 MoE，先跑通一个标准四足 velocity tracking policy。

### 任务

```text
1. 安装 Isaac Gym / Isaac Lab / legged_gym / rsl_rl。
2. 选择 ANYmal 或 Unitree A1 / Go2 作为初始机器人。
3. 跑通官方 PPO 训练。
4. 训练 flat terrain walking/running policy。
5. 训练 rough terrain locomotion policy。
6. 记录 reward curve、episode length、fall rate。
7. 导出视频。
```

### 必须理解的文件

```text
env config
robot config
terrain config
reward config
PPO config
actor-critic network
observation construction
action scaling
termination condition
```

### Baseline observation space

```text
obs = [
    base_angular_velocity,
    projected_gravity,
    command_velocity,
    joint_positions,
    joint_velocities,
    previous_actions
]
```

### Baseline action space

推荐先用：

```text
action = desired_joint_position_offset
joint_target = default_joint_position + action_scale * action
```

不要一开始直接 torque control。

### Baseline rewards

```text
reward =
    + linear_velocity_tracking
    + angular_velocity_tracking
    - vertical_velocity_penalty
    - roll_pitch_penalty
    - torque_penalty
    - joint_acceleration_penalty
    - action_rate_penalty
    - collision_penalty
    - feet_air_time_reward
```

### 阶段交付物

```text
1. 训练脚本
2. baseline config
3. reward curve
4. rollout video
5. README 说明：
   - observation space
   - action space
   - reward terms
   - domain randomization
   - training command
```

---

## 8. Milestone 2：训练多个 expert policies

### 目标

训练多个不同地形或不同功能的 expert policy。

### Experts 设计

| Expert | 任务 | 环境 |
|---|---|---|
| flat expert | 高速平地移动 | flat plane |
| rough expert | 崎岖地形移动 | random rough terrain |
| stair expert | 上下楼梯 | stairs |
| gap expert | 跨越间隙 / stepping stones | gaps / sparse footholds |
| recovery expert | 摔倒边缘恢复 / 被推恢复 | random pushes / high tilt |

### Expert policy 输入

初期所有 expert 使用相同 observation space，方便后续 gate 调用：

```text
expert_obs = [
    proprioception,
    command,
    previous_action,
    optional_height_samples
]
```

### Expert policy 输出

```text
expert_action = joint_position_target_offset
```

### 训练方式

每个 expert 单独 PPO 训练：

```bash
bash scripts/train_flat_expert.sh
bash scripts/train_rough_expert.sh
bash scripts/train_stair_expert.sh
bash scripts/train_gap_expert.sh
bash scripts/train_recovery_expert.sh
```

### 保存 checkpoint

```text
checkpoints/
├── flat_expert.pt
├── rough_expert.pt
├── stair_expert.pt
├── gap_expert.pt
└── recovery_expert.pt
```

### 阶段交付物

```text
1. 5 个专家策略 checkpoint
2. 每个 expert 的单独评估结果
3. 每个 expert 的失败案例分析
4. 一个 expert comparison table
```

---

## 9. Milestone 3：实现 Vanilla MoE gating

### 目标

固定专家网络，只训练 gate。

### MoE 结构

```text
experts = [
    flat_policy,
    rough_policy,
    stair_policy,
    gap_policy,
    recovery_policy
]

gate_input = [
    proprioception_history,
    command,
    terrain_embedding,
    previous_gate_weights
]

gate_weights = softmax(gate_network(gate_input))

action = sum_i gate_weights[i] * experts[i](obs)
```

### 第一版 gating network

```python
class GatingNetwork(nn.Module):
    def __init__(self, input_dim, num_experts):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.ELU(),
            nn.Linear(256, 256),
            nn.ELU(),
            nn.Linear(256, num_experts)
        )

    def forward(self, x):
        logits = self.net(x)
        weights = torch.softmax(logits, dim=-1)
        return weights
```

### MoE policy 伪代码

```python
class MoEPolicy(nn.Module):
    def __init__(self, experts, gate):
        super().__init__()
        self.experts = experts
        self.gate = gate

    def forward(self, obs, gate_obs):
        weights = self.gate(gate_obs)

        expert_actions = []
        for expert in self.experts:
            with torch.no_grad():
                expert_actions.append(expert(obs))

        expert_actions = torch.stack(expert_actions, dim=1)
        action = torch.sum(weights.unsqueeze(-1) * expert_actions, dim=1)

        return action, weights
```

### 注意事项

直接混合 action 有风险：

```text
如果不同 expert 的 gait phase 不一致，
soft action mixture 可能产生不自然动作。
```

可选改进：

```text
1. hard routing：只选最大权重 expert
2. top-k routing：只混合前 k 个 expert
3. residual experts：base policy + residual correction
4. latent mixture：混合 latent，而不是直接混合 action
5. 加 action smoothness penalty
```

### Gate regularization

添加：

```text
entropy loss
load balancing loss
temporal smoothness loss
```

示例：

```python
gate_entropy = -torch.sum(weights * torch.log(weights + 1e-8), dim=-1).mean()

load_balance = torch.var(weights.mean(dim=0))

temporal_smoothness = torch.mean((weights_t - weights_t_minus_1) ** 2)
```

### 阶段交付物

```text
1. moe_policy.py
2. gating_network.py
3. train_gate.sh
4. gate visualization
5. expert utilization statistics
6. 与 single policy 的初步对比
```

---

## 10. Milestone 4：加入 terrain encoder

### 目标

让 gate 根据地形信息选择 expert。

### 输入选择

可以从简单到复杂：

```text
Level 1: terrain type label
Level 2: height samples
Level 3: local height map
Level 4: depth image
```

建议开发顺序：

```text
先用 privileged terrain type label 验证 MoE 是否有效；
再换成 height samples；
最后再考虑 depth image encoder。
```

### Terrain encoder 设计

```python
class TerrainEncoder(nn.Module):
    def __init__(self, input_dim, latent_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ELU(),
            nn.Linear(128, latent_dim),
            nn.ELU()
        )

    def forward(self, terrain_obs):
        return self.net(terrain_obs)
```

### Gate input

```text
gate_input = concat(
    proprioception_history_embedding,
    command,
    terrain_embedding,
    previous_gate_weights
)
```

### 阶段交付物

```text
1. terrain_encoder.py
2. 对比：
   - no terrain input
   - terrain label
   - height samples
   - height map encoder
3. gate heatmap 可视化
4. 不同地形下 expert activation 图
```

---

## 11. Milestone 5：加入 risk estimator / safety-aware gating

### 目标

参考 Agile But Safe 思路，引入风险估计，让系统在危险时主动切换到 recovery expert。

### Risk estimator 输入

```text
risk_input = [
    base orientation,
    base angular velocity,
    base height,
    joint state,
    contact state,
    terrain embedding,
    obstacle distance,
    previous action
]
```

### Risk estimator 输出

```text
risk_score ∈ [0, 1]
```

含义：

```text
0 = safe
1 = high risk of collision / fall / failure
```

### Safety-aware gating 规则

第一版可以用简单规则：

```python
if risk_score > threshold:
    force recovery expert
else:
    use MoE gate
```

第二版可以用 soft bias：

```python
gate_logits[recovery_expert_id] += alpha * risk_score
gate_weights = softmax(gate_logits)
```

第三版可以让 risk estimator 和 gate 一起学习。

### Safety-aware MoE 伪代码

```python
class SafetyAwareMoEPolicy(nn.Module):
    def __init__(self, experts, gate, risk_estimator, recovery_id):
        super().__init__()
        self.experts = experts
        self.gate = gate
        self.risk_estimator = risk_estimator
        self.recovery_id = recovery_id

    def forward(self, obs, gate_obs, risk_obs):
        logits = self.gate.get_logits(gate_obs)
        risk_score = self.risk_estimator(risk_obs)

        logits[:, self.recovery_id] += self.alpha * risk_score.squeeze(-1)

        weights = torch.softmax(logits, dim=-1)
        expert_actions = torch.stack([expert(obs) for expert in self.experts], dim=1)
        action = torch.sum(weights.unsqueeze(-1) * expert_actions, dim=1)

        return action, weights, risk_score
```

### Risk label 构造方法

可以用以下方式构造 supervised risk label：

```text
1. 未来 N 步内是否 fall
2. 未来 N 步内是否 collision
3. base height 是否低于阈值
4. roll/pitch 是否超过阈值
5. recovery policy 是否优于 locomotion policy
```

### 阶段交付物

```text
1. risk_estimator.py
2. safety_supervisor.py
3. recovery expert integration
4. risk score visualization
5. safety-aware MoE vs vanilla MoE 对比
```

---

## 12. Milestone 6：加入 contrastive routing / CMoE 思路

### 目标

避免 gate 在所有地形上都输出差不多的均匀分布。

### 问题

Vanilla MoE 容易出现：

```text
flat terrain:   [0.22, 0.18, 0.20, 0.19, 0.21]
rough terrain:  [0.21, 0.20, 0.19, 0.20, 0.20]
stairs:         [0.20, 0.21, 0.18, 0.20, 0.21]
```

这说明 experts 没有明显分工。

### 目标 gate 分布

希望类似：

```text
flat terrain:   [0.75, 0.10, 0.05, 0.03, 0.07]
rough terrain:  [0.08, 0.72, 0.07, 0.05, 0.08]
stairs:         [0.05, 0.10, 0.70, 0.05, 0.10]
danger state:   [0.05, 0.05, 0.05, 0.05, 0.80]
```

### Contrastive routing 思路

```text
同一地形 / 同一任务的 gate activation 应该相似；
不同地形 / 不同任务的 gate activation 应该分离。
```

### Loss 设计

可以先实现简单版本：

```python
positive_loss = distance(gate_i, gate_j) for same terrain
negative_loss = max(0, margin - distance(gate_i, gate_k)) for different terrain

contrastive_loss = positive_loss + negative_loss
```

### 总 loss

```text
total_loss =
    PPO_loss
    + lambda_entropy * entropy_loss
    + lambda_balance * load_balance_loss
    + lambda_smooth * temporal_smoothness_loss
    + lambda_contrastive * contrastive_routing_loss
```

### 阶段交付物

```text
1. contrastive routing loss
2. expert activation clustering plot
3. t-SNE / PCA visualization of gate embedding
4. ablation:
   - vanilla MoE
   - MoE + load balancing
   - MoE + contrastive routing
   - safety-aware CMoE
```

---

## 13. Milestone 7：完整 ablation study

### 实验组

| Group | 方法 |
|---|---|
| A | Single policy |
| B | Rule-based switch |
| C | Frozen experts + vanilla gate |
| D | Frozen experts + safety-aware gate |
| E | Joint fine-tuned MoE |
| F | Safety-aware CMoE |
| G | Residual expert MoE |

### 测试地形

```text
flat
rough
stairs
gaps
mixed terrain
obstacle course
OOD friction
OOD mass
OOD latency
random pushes
sensor noise
```

### 指标

```text
success rate
fall rate
collision rate
average speed
tracking error
goal reaching error
energy consumption
cost of transport
gate entropy
expert utilization
switching frequency
recovery trigger frequency
OOD generalization score
```

### 表格模板

```markdown
| Method | Success ↑ | Fall ↓ | Collision ↓ | Speed ↑ | Energy ↓ | Gate Entropy | OOD Success ↑ |
|---|---:|---:|---:|---:|---:|---:|---:|
| Single Policy | | | | | | N/A | |
| Rule Switch | | | | | | N/A | |
| Vanilla MoE | | | | | | | |
| Safety MoE | | | | | | | |
| Safety CMoE | | | | | | | |
```

### 阶段交付物

```text
1. ablation.py
2. terrain_sweep.py
3. metrics.py
4. final result table
5. gate visualization plots
6. demo videos
7. final report
```

---

## 14. Milestone 8：整理成 GitHub 项目

### README 必须包含

```text
1. Project overview
2. Motivation
3. Method
4. Installation
5. Training
6. Evaluation
7. Results
8. Ablation
9. Videos / GIFs
10. Paper notes
11. Future work
```

### README 项目简介示例

```markdown
# Safety-Aware MoE-Gated Locomotion for Legged Local Navigation

This project implements a safety-aware Mixture-of-Experts locomotion framework for legged robot local navigation. Multiple PPO-trained locomotion experts specialize in flat terrain, rough terrain, stairs, gaps, and recovery behaviors. A learned gating network selects or blends expert policies based on proprioceptive history, terrain embeddings, command inputs, and risk estimates.

The system is evaluated in simulation across mixed terrains, obstacle courses, perturbations, and out-of-distribution dynamics settings. We compare single-policy baselines, rule-based switching, vanilla MoE, and safety-aware MoE variants.
```

### 简历描述

```text
Implemented a safety-aware Mixture-of-Experts locomotion framework for quadruped local navigation in Isaac Gym/Isaac Lab. Trained terrain-specialized PPO experts for flat, rough, stair, gap, and recovery behaviors, and learned a gating policy conditioned on proprioceptive history, terrain embeddings, and risk estimates. Evaluated success rate, collision rate, fall recovery, expert utilization, and out-of-distribution terrain generalization.
```

### 面试讲解结构

```text
1. 为什么做 MoE？
   Single policy 在多地形多技能上容易互相干扰。

2. 为什么需要 safety-aware gating？
   普通 gate 只优化 reward，不一定在危险状态及时切 recovery。

3. 为什么不能简单 action mixture？
   不同 expert 的 gait phase 可能不同，直接混合 joint target 可能导致不连续动作。

4. 你怎么验证有效？
   做 single policy / rule switch / vanilla MoE / safety MoE / contrastive MoE 对比。

5. 最大技术难点是什么？
   reward design、expert specialization、gate stability、safe switching、sim-to-real gap。
```

---

## 15. 12 周执行计划

### Week 1：环境和基础

任务：

```text
1. 安装 Linux / Conda / CUDA / PyTorch。
2. 安装 Isaac Gym 或 Isaac Lab。
3. 跑通一个官方 locomotion demo。
4. 阅读 legged_gym / rsl_rl 代码结构。
5. 建立项目仓库。
```

输出：

```text
- environment.yml
- README 初版
- baseline demo video
```

---

### Week 2：PPO 与 baseline locomotion

任务：

```text
1. 学 PPO / Actor-Critic / GAE。
2. 跑通 flat terrain policy。
3. 分析 observation/action/reward。
4. 改 reward 权重，观察训练变化。
```

输出：

```text
- flat expert checkpoint
- reward analysis note
- first experiment log
```

---

### Week 3：Rough terrain locomotion

任务：

```text
1. 加 rough terrain curriculum。
2. 加 domain randomization。
3. 训练 rough expert。
4. 评估不同摩擦、坡度、随机推力。
```

输出：

```text
- rough expert checkpoint
- terrain curriculum config
- rough terrain demo
```

---

### Week 4：Stair / gap expert

任务：

```text
1. 构造 stairs terrain。
2. 构造 gap / stepping-stone terrain。
3. 分别训练 stair expert 和 gap expert。
4. 记录失败模式。
```

输出：

```text
- stair expert checkpoint
- gap expert checkpoint
- failure case report
```

---

### Week 5：Recovery expert

任务：

```text
1. 构造 recovery 环境。
2. 加 random pushes。
3. 加 high tilt / collision near-failure states。
4. 训练 recovery expert。
```

输出：

```text
- recovery expert checkpoint
- recovery success rate
- recovery demo video
```

---

### Week 6：Vanilla MoE gate

任务：

```text
1. 实现 GatingNetwork。
2. 实现 MoEPolicy。
3. 冻结 expert。
4. 训练 gate。
5. 可视化 expert utilization。
```

输出：

```text
- moe_policy.py
- gating_network.py
- vanilla MoE result
- gate activation plot
```

---

### Week 7：Terrain encoder

任务：

```text
1. 先用 terrain label 做 privileged gate。
2. 再换成 height samples。
3. 实现 terrain encoder。
4. 对比 no terrain / label / height samples。
```

输出：

```text
- terrain_encoder.py
- terrain input ablation
- expert activation by terrain
```

---

### Week 8：Safety-aware gating

任务：

```text
1. 实现 risk estimator。
2. 构造 risk label。
3. 将 risk score 加入 gate。
4. 高风险时 bias recovery expert。
5. 对比 vanilla MoE 和 safety MoE。
```

输出：

```text
- risk_estimator.py
- safety_supervisor.py
- safety MoE results
- recovery trigger visualization
```

---

### Week 9：Contrastive routing

任务：

```text
1. 实现 contrastive routing loss。
2. 加 load balancing loss。
3. 加 temporal smoothness loss。
4. 观察 expert 是否更专门化。
```

输出：

```text
- moe_regularization.py
- CMoE result
- gate clustering visualization
```

---

### Week 10：完整评估

任务：

```text
1. 实现 terrain_sweep.py。
2. 实现 ablation.py。
3. 统一跑所有方法。
4. 收集 metrics。
5. 生成结果表格。
```

输出：

```text
- ablation result table
- metrics plots
- OOD evaluation
```

---

### Week 11：报告和可视化

任务：

```text
1. 整理实验图。
2. 录制 demo video/GIF。
3. 写 final_report.md。
4. 写 paper notes。
5. 补 README。
```

输出：

```text
- final_report.md
- demo video
- README 完整版
```

---

### Week 12：简历与面试包装

任务：

```text
1. 写简历 bullet points。
2. 准备 3 分钟项目讲解。
3. 准备技术问答。
4. 清理 repo。
5. 生成项目 poster / slide outline。
```

输出：

```text
- resume bullets
- interview notes
- project summary
```

---

## 16. Codex 执行指令

可以将下面这段作为 Codex 的长期项目 prompt。

```markdown
# Codex Project Instruction

You are helping me implement a research-style robotics project:

**Safety-Aware Mixture-of-Experts Locomotion for Legged Local Navigation**

The goal is to build a simulation-based reinforcement learning project for quadruped legged locomotion and local navigation. The project should progressively implement:

1. PPO-based locomotion baselines.
2. Multiple terrain-specialized expert policies.
3. A Mixture-of-Experts gating policy.
4. Terrain-conditioned routing.
5. Risk-aware safety switching with a recovery expert.
6. Contrastive / regularized routing for expert specialization.
7. Evaluation and ablation scripts.

Please follow this repository structure:

```text
safe-moe-locomotion/
├── README.md
├── requirements.txt
├── environment.yml
├── scripts/
├── configs/
├── safe_moe_locomotion/
│   ├── envs/
│   ├── policies/
│   ├── modules/
│   ├── rewards/
│   ├── training/
│   ├── evaluation/
│   └── utils/
├── notebooks/
├── docs/
└── assets/
```

Implementation priorities:

1. Start with minimal runnable code.
2. Prefer clean abstractions over overly complex implementations.
3. Keep all configs in YAML.
4. Each module should be independently testable.
5. Add comments explaining robotics and RL assumptions.
6. Avoid hard-coding robot-specific values inside core policy code.
7. Design the code so that experts can be frozen, loaded from checkpoints, and called by the MoE policy.
8. Log gate weights, expert utilization, risk scores, and evaluation metrics.
9. Provide training and evaluation scripts for each milestone.
10. Keep README updated with commands and experiment results.

First tasks:

1. Create the repository skeleton.
2. Add placeholder config files.
3. Implement `GatingNetwork`.
4. Implement `MoEPolicy`.
5. Implement `SafetyAwareMoEPolicy`.
6. Implement metrics for success rate, fall rate, collision rate, expert utilization, and gate entropy.
7. Add simple unit tests with dummy expert networks before connecting to Isaac Gym / Isaac Lab.

Do not attempt full sim-to-real deployment initially. The first target is a clean simulation-only prototype.
```

---

## 17. 最小可行版本 MVP

如果时间不够，先做 MVP：

```text
1. 不接 Isaac Gym，先用 dummy env + dummy experts 验证 MoE framework。
2. 实现 expert loading / gating / action mixture。
3. 加 gate regularization。
4. 用 toy terrain label 测 expert routing。
5. 再接 legged_gym / Isaac Lab。
```

MVP 代码目标：

```text
dummy_obs → experts → gate → action
```

需要实现：

```text
GatingNetwork
DummyExpert
MoEPolicy
SafetyAwareMoEPolicy
gate entropy metric
expert utilization metric
simple training loop
visualization script
```

这样可以先保证项目代码架构跑通，再接真实机器人仿真。

---

## 18. 常见坑

### 18.1 一开始就做人形机器人

风险：

```text
balance 太难；
reward 很难调；
训练容易摔；
sim-to-real gap 更大。
```

建议：

```text
先四足，后人形。
```

---

### 18.2 一开始就 full MoE joint training

风险：

```text
expert 不专门化；
gate collapse；
训练不稳定；
debug 困难。
```

建议：

```text
先单独训练 experts；
冻结 experts；
只训练 gate；
最后再 joint fine-tuning。
```

---

### 18.3 直接混合 torque

风险：

```text
动作不连续；
不同 gait phase 冲突；
机器人容易摔。
```

建议：

```text
优先混合 joint target；
或者用 hard routing / top-k routing / residual action。
```

---

### 18.4 reward 过于复杂

风险：

```text
不知道是哪一项导致训练失败；
policy 学到奇怪行为。
```

建议：

```text
先用成熟 baseline reward；
一次只改一两项；
记录每次实验。
```

---

### 18.5 只看 success rate

还要看：

```text
fall rate
collision rate
energy
gate switching frequency
expert utilization
OOD performance
recovery success rate
```

---

## 19. 学习资料 checklist

### 强化学习

```text
[ ] PPO
[ ] Actor-Critic
[ ] GAE
[ ] entropy regularization
[ ] reward shaping
[ ] curriculum learning
[ ] domain randomization
[ ] offline evaluation
```

### 机器人

```text
[ ] rigid body dynamics
[ ] contact dynamics
[ ] friction cone
[ ] centroidal dynamics
[ ] ZMP / capture point
[ ] whole-body control
[ ] MPC
[ ] PD control
```

### 腿式机器人 RL

```text
[ ] observation design
[ ] action design
[ ] command-conditioned locomotion
[ ] terrain curriculum
[ ] actuator modeling
[ ] random pushes
[ ] privileged learning
[ ] history adaptation
[ ] sim-to-real
```

### 感知导航

```text
[ ] height map
[ ] depth camera
[ ] terrain encoder
[ ] local navigation
[ ] goal-conditioned policy
[ ] collision avoidance
[ ] risk estimation
```

### MoE

```text
[ ] gating network
[ ] soft routing
[ ] hard routing
[ ] top-k routing
[ ] load balancing loss
[ ] contrastive routing
[ ] temporal smoothness
[ ] residual experts
[ ] safety-aware routing
```

---

## 20. 最终交付物 checklist

```text
[ ] GitHub repo
[ ] README
[ ] installation guide
[ ] training scripts
[ ] evaluation scripts
[ ] pretrained expert checkpoints
[ ] MoE gating implementation
[ ] safety-aware gating implementation
[ ] ablation study
[ ] result tables
[ ] plots
[ ] demo videos/GIFs
[ ] final report
[ ] resume bullets
[ ] interview notes
```

---

## 21. 推荐最终项目标题

可选标题：

```text
Safety-Aware MoE-Gated Locomotion for Legged Local Navigation
```

```text
Mixture-of-Experts Skill Routing for Quadruped Navigation over Challenging Terrain
```

```text
Risk-Aware Multi-Expert Reinforcement Learning for Agile Legged Locomotion
```

```text
Terrain-Conditioned Expert Routing for Robust Quadruped Locomotion
```

如果面向 humanoid：

```text
Safety-Aware Multi-Expert Locomotion for Humanoid Navigation
```

---

## 22. 最终简历 bullet points

```text
- Implemented a safety-aware Mixture-of-Experts locomotion framework for quadruped local navigation in simulation, combining terrain-specialized PPO experts with a learned gating policy.

- Trained expert policies for flat, rough, stair, gap, and recovery behaviors, and evaluated them under mixed terrains, random pushes, friction changes, and sensor noise.

- Designed a terrain- and risk-conditioned gating network using proprioceptive history, terrain embeddings, and safety estimates to route between locomotion and recovery experts.

- Conducted ablation studies comparing single-policy baselines, rule-based switching, vanilla MoE, safety-aware MoE, and contrastive routing variants using success rate, collision rate, fall rate, expert utilization, and OOD generalization metrics.

- Built a reproducible robot learning pipeline with YAML configs, training scripts, evaluation tools, rollout videos, and visualization of expert activation patterns.
```

---

## 23. 面试时可以这样讲

### 23.1 项目动机

```text
Single locomotion policies often struggle when one model has to cover many different terrain types and safety-critical behaviors. I wanted to explore whether a Mixture-of-Experts architecture can improve specialization and robustness by assigning different experts to flat locomotion, rough terrain, stairs, gaps, and recovery.
```

### 23.2 方法

```text
I first trained separate PPO experts in different terrain environments. Then I froze the experts and trained a gating network conditioned on proprioceptive history, terrain embeddings, commands, and risk estimates. The gate either softly combines expert actions or selects the most appropriate expert. I also added a safety-aware bias that increases the probability of the recovery expert when the risk estimator predicts a high chance of falling or collision.
```

### 23.3 难点

```text
The main challenges were expert specialization, stable switching between policies, avoiding gate collapse, and designing evaluation metrics beyond simple task success. Directly averaging actions from experts can be unstable because different experts may have different gait phases, so I explored hard routing, top-k routing, and residual expert variants.
```

### 23.4 结果

```text
I evaluated the system on flat terrain, rough terrain, stairs, gaps, mixed terrain, and out-of-distribution settings such as friction changes and random pushes. I compared single policy, rule-based switching, vanilla MoE, and safety-aware MoE using success rate, fall rate, collision rate, expert utilization, gate entropy, and OOD success.
```

---

## 24. 下一步扩展

完成四足版本后，可以继续扩展：

```text
1. 将 Go2 / ANYmal 四足版本迁移到 Unitree G1 / H1 人形机器人。
2. 将 terrain encoder 从 height samples 升级到 depth image encoder。
3. 将 local navigation 接入 VLA / language instruction。
4. 用 language command 控制 expert routing。
5. 将 MoE policy distill 成 single student policy。
6. 加入 WBC / MPC safety layer。
7. 尝试 real robot sim-to-real deployment。
```

---

## 25. 最建议的执行顺序总结

```text
Step 1: 跑通 legged_gym / Isaac Lab baseline
Step 2: 训练 flat / rough / stair / gap / recovery experts
Step 3: 冻结 experts，训练 vanilla MoE gate
Step 4: 加 terrain encoder
Step 5: 加 risk estimator 和 recovery switch
Step 6: 加 contrastive routing / load balancing
Step 7: 做完整 ablation
Step 8: 写 README、报告、简历和面试讲稿
Step 9: 再考虑人形机器人和 VLA 结合
```

---

## 26. 最重要原则

```text
先跑通，再创新；
先四足，再人形；
先冻结专家，再联合训练；
先仿真验证，再想真机；
先可复现，再做复杂改进。
```

