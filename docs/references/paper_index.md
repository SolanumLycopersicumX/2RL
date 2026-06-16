# Paper Index

Last updated: 2026-06-15.

This index collects the papers mentioned or recommended in
`rl_locomotion_moe_research_plan.md`. Links point to arXiv or project pages
where available. Use `docs/paper_notes/README.md` for note templates.

## Quadruped RL Locomotion Foundations

| Priority | Paper | Link | Use in 2RL |
|---:|---|---|---|
| 1 | Learning to Walk in Minutes Using Massively Parallel Deep Reinforcement Learning | https://arxiv.org/abs/2109.11978 | Isaac Gym / legged_gym baseline, PPO, terrain curriculum. |
| 1 | Sim-to-Real: Learning Agile Locomotion For Quadruped Robots | https://arxiv.org/abs/1804.10332 | Sim-to-real basics, actuator model, latency, domain randomization. |
| 1 | Learning agile and dynamic motor skills for legged robots | https://arxiv.org/abs/1901.08652 | ANYmal dynamic locomotion, fall recovery, energy-efficient command following. |
| 1 | Learning Quadrupedal Locomotion over Challenging Terrain | https://arxiv.org/abs/2010.11251 | Proprioceptive robust locomotion on challenging natural terrain. |
| 1 | RMA: Rapid Motor Adaptation for Legged Robots | https://arxiv.org/abs/2107.04034 | History adaptation, latent environment factors, terrain and payload robustness. |

## Perceptive Navigation, Parkour, and Risky Terrain

| Priority | Paper | Link | Use in 2RL |
|---:|---|---|---|
| 1 | Advanced Skills by Learning Locomotion and Local Navigation End-to-End | https://arxiv.org/abs/2209.12827 | Upgrade velocity tracking into goal-conditioned local navigation. |
| 1 | Robot Parkour Learning | https://arxiv.org/abs/2309.05665 | Vision-based parkour skills, skill distillation, obstacle traversal. |
| 1 | Extreme Parkour with Legged Robots | https://arxiv.org/abs/2309.14341 | Depth-based end-to-end agile parkour policy. |
| 1 | Learning Agile Locomotion on Risky Terrains | https://arxiv.org/abs/2311.10484 | Sparse footholds, stepping stones, navigation framing instead of velocity tracking. |
| 1 | Resilient Legged Local Navigation: Learning to Traverse with Compromised Perception End-to-End | https://arxiv.org/abs/2310.03581 | Robust navigation under perception failures. |
| 1 | Agile But Safe: Learning Collision-Free High-Speed Legged Locomotion | https://arxiv.org/abs/2401.17583 | Safety switch, recovery policy, reach-avoid value network. |

## Humanoid Locomotion and Whole-Body Control

| Priority | Paper | Link | Use in 2RL |
|---:|---|---|---|
| 2 | Real-World Humanoid Locomotion with Reinforcement Learning | https://arxiv.org/abs/2303.03381 | Transformer policy, history-conditioned adaptation, zero-shot real-world deployment. |
| 2 | Humanoid-Gym: Reinforcement Learning for Humanoid Robot with Zero-Shot Sim2Real Transfer | https://arxiv.org/abs/2404.05695 | Humanoid Isaac Gym workflow and sim-to-sim through MuJoCo. |
| 2 | Learning Human-to-Humanoid Real-Time Whole-Body Teleoperation | https://arxiv.org/abs/2403.04436 | H2O, sim-to-data, motion imitation for humanoid control. |
| 2 | OmniH2O: Universal and Dexterous Human-to-Humanoid Whole-Body Teleoperation and Learning | https://arxiv.org/abs/2406.08858 | Humanoid whole-body teleoperation and learning from demonstrations. |
| 2 | WoCoCo: Learning Whole-Body Humanoid Control with Sequential Contacts | https://arxiv.org/abs/2406.06005 | Sequential contact decomposition for whole-body humanoid tasks. |
| 2 | BeamDojo: Learning Agile Humanoid Locomotion on Sparse Footholds | https://arxiv.org/abs/2502.10363 | Humanoid sparse footholds and risky terrain curriculum. |

## MoE, Expert Composition, and Routing

| Priority | Paper | Link | Use in 2RL |
|---:|---|---|---|
| 1 | MoE-Loco: Mixture of Experts for Multitask Locomotion | https://arxiv.org/abs/2503.08564 | Core MoE locomotion motivation, expert specialization, multitask gradients. |
| 1 | CMoE: Contrastive Mixture of Experts for Motion Control and Terrain Adaptation of Humanoid Robots | https://arxiv.org/abs/2603.03067 | Contrastive routing, expert activation separation, terrain adaptation. |
| 1 | MoRE: Mixture of Residual Experts for Humanoid Lifelike Gaits Learning on Complex Terrains | https://arxiv.org/abs/2506.08840 | Residual experts and latent residual mixture for more stable action composition. |
| 1 | Parkour in the Wild: Learning a General and Extensible Agile Locomotion Policy Using Multi-expert Distillation and RL Fine-tuning | https://arxiv.org/abs/2505.11164 | Terrain-specific expert policies, DAgger distillation, RL fine-tuning. |
| 1 | Toward Reliable Sim-to-Real Predictability for MoE-based Robust Quadrupedal Locomotion | https://arxiv.org/abs/2602.00678 | MoE policy selection, RoboGauge-style sim-to-real predictability checks. |

## Extra Current Reference

| Priority | Paper | Link | Use in 2RL |
|---:|---|---|---|
| 2 | Quadruped Parkour Learning: Sparsely Gated Mixture of Experts with Visual Input | https://arxiv.org/abs/2604.19344 | Recent 2026 visual MoE parkour reference; useful after baseline MoE is working. |

## Reading Deliverables

For each priority-1 paper, create a note under `docs/paper_notes/` that records:

- observation space,
- action space,
- reward terms,
- simulator and robot,
- training algorithm,
- sim-to-real assumptions,
- exact ideas to reuse in this project.

