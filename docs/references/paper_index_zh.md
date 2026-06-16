# 论文清单

完整英文索引见 `paper_index.md`。本文件给出中文阅读用途说明。

## 四足 RL locomotion 基础

| 论文 | 用途 |
|---|---|
| Learning to Walk in Minutes Using Massively Parallel Deep Reinforcement Learning | Isaac Gym / legged_gym / PPO baseline。 |
| Sim-to-Real: Learning Agile Locomotion For Quadruped Robots | sim-to-real、actuator model、domain randomization。 |
| Learning agile and dynamic motor skills for legged robots | 敏捷 gait、动态技能、恢复能力。 |
| Learning Quadrupedal Locomotion over Challenging Terrain | 粗糙地形、本体感知和鲁棒 locomotion。 |
| RMA: Rapid Motor Adaptation for Legged Robots | history encoder 和 latent adaptation。 |

## 感知导航、Parkour、风险地形

| 论文 | 用途 |
|---|---|
| Advanced Skills by Learning Locomotion and Local Navigation End-to-End | 从速度跟踪升级到局部导航。 |
| Robot Parkour Learning | parkour skills、障碍专家、蒸馏路线。 |
| Extreme Parkour with Legged Robots | 深度感知下的极端地形。 |
| Learning Agile Locomotion on Risky Terrains | stepping stones、稀疏落脚点、风险地形。 |
| Resilient Legged Local Navigation | 感知失效下的鲁棒导航。 |
| Agile But Safe | safety switch、recovery policy、risk estimator。 |

## 人形机器人扩展

| 论文 | 用途 |
|---|---|
| Real-World Humanoid Locomotion with Reinforcement Learning | 真实人形机器人 RL locomotion。 |
| Humanoid-Gym | 人形机器人开源训练框架。 |
| H2O | human-to-humanoid teleoperation。 |
| OmniH2O | 更通用的全身遥操作。 |
| WoCoCo | sequential contacts / whole-body control。 |
| BeamDojo | 人形机器人 sparse footholds。 |

## MoE 与专家组合

| 论文 | 用途 |
|---|---|
| MoE-Loco | locomotion MoE 核心参考。 |
| CMoE | contrastive routing 和 expert specialization。 |
| MoRE | residual experts，避免直接 action mixture 不稳定。 |
| Parkour in the Wild | 多专家蒸馏和 RL fine-tuning。 |
| Reliable Sim-to-Real Predictability for MoE-based Robust Quadrupedal Locomotion | MoE sim-to-real 可靠性评估。 |
| Quadruped Parkour Learning: Sparsely Gated Mixture of Experts with Visual Input | sparse-gated visual MoE parkour 进阶参考。 |

## 本地资料入口

- PDF manifest: `docs/references/papers/papers_manifest.csv`
- 单篇中文笔记: `docs/paper_notes/individual/README_zh.md`
- 整合中文综述: `docs/paper_notes/integrated_literature_review_zh.md`
