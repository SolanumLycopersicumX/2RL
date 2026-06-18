# 推荐论文阅读顺序

本文档给出 2RL 项目的完整论文阅读顺序，覆盖当前已下载和已做笔记的 **26 篇论文**。

目标不是按年份读完所有论文，而是按项目开发依赖关系阅读：

```text
baseline locomotion
→ robustness / sim-to-real
→ terrain / navigation / safety
→ MoE expert composition
→ humanoid extension
→ VLA extension
```

开始前先读：

- [整合文献综述](../paper_notes/integrated_literature_review_zh.md)
- [单篇论文笔记索引](../paper_notes/individual/README_zh.md)

## 阅读方法

每篇论文按这个顺序读：

1. 先读对应中文单篇笔记。
2. 再读 PDF 的 Abstract、Introduction、Method、Experiments。
3. 最后自己记录：
   - observation
   - action
   - reward
   - training pipeline
   - evaluation metrics
   - 能迁移到 2RL 的设计
   - 现在暂时不用实现的内容

---

## Phase 1：先建立四足 RL Locomotion Baseline

这一阶段服务 Milestone 1：先跑通 PPO locomotion baseline，不碰 MoE。

### 1. Learning to Walk in Minutes Using Massively Parallel Deep Reinforcement Learning

- 笔记：[中文笔记](../paper_notes/individual/2109.11978_learning_to_walk_in_minutes_using_massively_parallel_deep_reinforcement_learning_zh.md)
- PDF: [local PDF](papers/2109.11978_learning_to_walk_in_minutes_using_massively_parallel_deep_reinforcement_learning.pdf)
- 为什么先读：这是 legged_gym / Isaac Gym / PPO baseline 的核心入口。
- 重点看：
  - observation space；
  - action 是 joint position target offset；
  - reward terms；
  - massive parallel simulation；
  - terrain curriculum。
- 读完应能回答：为什么先训练 flat velocity tracking policy？

### 2. RMA: Rapid Motor Adaptation for Legged Robots

- 笔记：[中文笔记](../paper_notes/individual/2107.04034_rma_rapid_motor_adaptation_for_legged_robots_zh.md)
- PDF: [local PDF](papers/2107.04034_rma_rapid_motor_adaptation_for_legged_robots.pdf)
- 为什么第二篇读：它解释 history encoder 和 latent adaptation，后续 gate/risk estimator 都会用到这个思想。
- 重点看：
  - privileged information；
  - adaptation module；
  - proprioception history；
  - sim-to-real robustness。
- 读完应能回答：为什么 gate 不应该只看当前 observation？

### 3. Learning Quadrupedal Locomotion over Challenging Terrain

- 笔记：[中文笔记](../paper_notes/individual/2010.11251_learning_quadrupedal_locomotion_over_challenging_terrain_zh.md)
- PDF: [local PDF](papers/2010.11251_learning_quadrupedal_locomotion_over_challenging_terrain.pdf)
- 为什么第三篇读：它把 baseline 从 flat terrain 推到 rough / challenging terrain。
- 重点看：
  - rough terrain curriculum；
  - proprioceptive locomotion；
  - failure cases；
  - terrain generalization。
- 读完应能回答：rough expert 和 flat expert 的训练目标有什么区别？

### 4. Sim-to-Real: Learning Agile Locomotion For Quadruped Robots

- 笔记：[中文笔记](../paper_notes/individual/1804.10332_sim_to_real_learning_agile_locomotion_for_quadruped_robots_zh.md)
- PDF: [local PDF](papers/1804.10332_sim_to_real_learning_agile_locomotion_for_quadruped_robots.pdf)
- 为什么这时读：baseline 跑通后，需要理解为什么仿真策略不一定能真实部署。
- 重点看：
  - actuator model；
  - latency；
  - friction / mass randomization；
  - sim-to-real gap。
- 读完应能回答：2RL 的 config 为什么要记录 randomization 范围？

### 5. Learning agile and dynamic motor skills for legged robots

- 笔记：[中文笔记](../paper_notes/individual/1901.08652_learning_agile_and_dynamic_motor_skills_for_legged_robots_zh.md)
- PDF: [local PDF](papers/1901.08652_learning_agile_and_dynamic_motor_skills_for_legged_robots.pdf)
- 为什么第五篇读：它补充动态技能、速度范围、扰动恢复和敏捷 gait。
- 重点看：
  - dynamic skills；
  - command distribution；
  - recovery from perturbations；
  - reward shaping。
- 读完应能回答：flat expert 是否只代表“平地慢走”？为什么不是？

**Phase 1 读完后的动作：**

- 开始看 [环境部署指南](../setup/ENVIRONMENT_zh.md)。
- 尝试准备 Isaac Lab 或 legacy legged_gym。
- 不要急着做 MoE。

---

## Phase 2：地形、导航、感知和安全

这一阶段服务 Milestone 2、4、5：训练专家、加入 terrain encoder 和 safety-aware routing。

### 6. Advanced Skills by Learning Locomotion and Local Navigation End-to-End

- 笔记：[中文笔记](../paper_notes/individual/2209.12827_advanced_skills_by_learning_locomotion_and_local_navigation_end_to_end_zh.md)
- PDF: [local PDF](papers/2209.12827_advanced_skills_by_learning_locomotion_and_local_navigation_end_to_end.pdf)
- 重点：从 velocity tracking 过渡到 local navigation。
- 读完应能回答：goal-conditioned locomotion 和 command tracking 有什么区别？

### 7. Learning Agile Locomotion on Risky Terrains

- 笔记：[中文笔记](../paper_notes/individual/2311.10484_learning_agile_locomotion_on_risky_terrains_zh.md)
- PDF: [local PDF](papers/2311.10484_learning_agile_locomotion_on_risky_terrains.pdf)
- 重点：stepping stones、sparse footholds、风险地形。
- 读完应能回答：gap expert 为什么不能只用平均速度评价？

### 8. Resilient Legged Local Navigation: Learning to Traverse with Compromised Perception End-to-End

- 笔记：[中文笔记](../paper_notes/individual/2310.03581_resilient_legged_local_navigation_learning_to_traverse_with_compromised_percepti_zh.md)
- PDF: [local PDF](papers/2310.03581_resilient_legged_local_navigation_learning_to_traverse_with_compromised_perception_end_to_.pdf)
- 重点：感知失效、噪声、鲁棒导航。
- 读完应能回答：为什么 terrain encoder 需要 degraded perception evaluation？

### 9. Agile But Safe: Learning Collision-Free High-Speed Legged Locomotion

- 笔记：[中文笔记](../paper_notes/individual/2401.17583_agile_but_safe_learning_collision_free_high_speed_legged_locomotion_zh.md)
- PDF: [local PDF](papers/2401.17583_agile_but_safe_learning_collision_free_high_speed_legged_locomotion.pdf)
- 重点：risk estimator、safety switch、recovery behavior。
- 读完应能回答：为什么 reward penalty 不等于 safety guarantee？

### 10. Robot Parkour Learning

- 笔记：[中文笔记](../paper_notes/individual/2309.05665_robot_parkour_learning_zh.md)
- PDF: [local PDF](papers/2309.05665_robot_parkour_learning.pdf)
- 重点：parkour skills、障碍专家、技能组合。
- 读完应能回答：stair / gap / recovery expert 怎么定义任务边界？

### 11. Extreme Parkour with Legged Robots

- 笔记：[中文笔记](../paper_notes/individual/2309.14341_extreme_parkour_with_legged_robots_zh.md)
- PDF: [local PDF](papers/2309.14341_extreme_parkour_with_legged_robots.pdf)
- 重点：深度感知、极端地形、提前决策。
- 读完应能回答：为什么视觉/depth encoder 应该放到后期，而不是第一阶段？

**Phase 2 读完后的动作：**

- 设计 flat、rough、stair、gap、recovery 五个 expert 的训练边界。
- 明确 risk label 如何构造：未来 N 步 fall / collision / excessive tilt。
- 明确 terrain input 开发顺序：label -> height samples -> height map -> depth image。

---

## Phase 3：MoE、专家组合和 Routing

这一阶段服务 Milestone 3、6、7：MoE gate、contrastive routing、residual experts、ablation。

### 12. MoE-Loco: Mixture of Experts for Multitask Locomotion

- 笔记：[中文笔记](../paper_notes/individual/2503.08564_moe_loco_mixture_of_experts_for_multitask_locomotion_zh.md)
- PDF: [local PDF](papers/2503.08564_moe_loco_mixture_of_experts_for_multitask_locomotion.pdf)
- 重点：为什么 locomotion 多任务适合 MoE。
- 读完应能回答：single policy 的 gradient conflict 是什么？

### 13. MoRE: Mixture of Residual Experts for Humanoid Lifelike Gaits Learning on Complex Terrains

- 笔记：[中文笔记](../paper_notes/individual/2506.08840_more_mixture_of_residual_experts_for_humanoid_lifelike_gaits_learning_on_complex_zh.md)
- PDF: [local PDF](papers/2506.08840_more_mixture_of_residual_experts_for_humanoid_lifelike_gaits_learning_on_complex_terrains.pdf)
- 重点：residual experts，避免直接 action mixture 不稳定。
- 读完应能回答：为什么多个 expert 的 action 直接加权可能破坏 gait phase？

### 14. CMoE: Contrastive Mixture of Experts for Motion Control and Terrain Adaptation of Humanoid Robots

- 笔记：[中文笔记](../paper_notes/individual/2603.03067_cmoe_contrastive_mixture_of_experts_for_motion_control_and_terrain_adaptation_of_zh.md)
- PDF: [local PDF](papers/2603.03067_cmoe_contrastive_mixture_of_experts_for_motion_control_and_terrain_adaptation_of_humanoid_.pdf)
- 重点：contrastive routing、expert specialization。
- 读完应能回答：如何判断 gate 是否真的按地形分工？

### 15. Parkour in the Wild: Learning a General and Extensible Agile Locomotion Policy Using Multi-expert Distillation and RL Fine-tuning

- 笔记：[中文笔记](../paper_notes/individual/2505.11164_parkour_in_the_wild_learning_a_general_and_extensible_agile_locomotion_policy_us_zh.md)
- PDF: [local PDF](papers/2505.11164_parkour_in_the_wild_learning_a_general_and_extensible_agile_locomotion_policy_using_multi_.pdf)
- 重点：multi-expert distillation、DAgger、RL fine-tuning。
- 读完应能回答：MoE gate 和 expert distillation 分别适合什么目标？

### 16. Toward Reliable Sim-to-Real Predictability for MoE-based Robust Quadrupedal Locomotion

- 笔记：[中文笔记](../paper_notes/individual/2602.00678_toward_reliable_sim_to_real_predictability_for_moe_based_robust_quadrupedal_loco_zh.md)
- PDF: [local PDF](papers/2602.00678_toward_reliable_sim_to_real_predictability_for_moe_based_robust_quadrupedal_locomotion.pdf)
- 重点：MoE sim-to-real predictability、真实部署前可靠性评估。
- 读完应能回答：为什么 MoE 在仿真中成功不等于真实可靠？

### 17. Quadruped Parkour Learning: Sparsely Gated Mixture of Experts with Visual Input

- 笔记：[中文笔记](../paper_notes/individual/2604.19344_quadruped_parkour_learning_sparsely_gated_mixture_of_experts_with_visual_input_zh.md)
- PDF: [local PDF](papers/2604.19344_quadruped_parkour_learning_sparsely_gated_mixture_of_experts_with_visual_input.pdf)
- 重点：sparse gate、top-k experts、visual MoE parkour。
- 读完应能回答：top-k routing 相比 soft routing 有什么工程优势？

**Phase 3 读完后的动作：**

- 先实现 rule switch baseline。
- 再训练 frozen experts + vanilla gate。
- 再看是否需要 hard routing、top-k routing、residual experts、contrastive routing。

---

## Phase 4：人形机器人扩展

这一阶段不是当前第一复现目标。它服务未来 Unitree G1/H1 或 humanoid locomotion 扩展。

### 18. Real-World Humanoid Locomotion with Reinforcement Learning

- 笔记：[中文笔记](../paper_notes/individual/2303.03381_real_world_humanoid_locomotion_with_reinforcement_learning_zh.md)
- PDF: [local PDF](papers/2303.03381_real_world_humanoid_locomotion_with_reinforcement_learning.pdf)
- 重点：真实人形机器人 RL locomotion。
- 读完应能回答：人形相比四足难在哪里？

### 19. Humanoid-Gym: Reinforcement Learning for Humanoid Robot with Zero-Shot Sim2Real Transfer

- 笔记：[中文笔记](../paper_notes/individual/2404.05695_humanoid_gym_reinforcement_learning_for_humanoid_robot_with_zero_shot_sim2real_t_zh.md)
- PDF: [local PDF](papers/2404.05695_humanoid_gym_reinforcement_learning_for_humanoid_robot_with_zero_shot_sim2real_transfer.pdf)
- 重点：Humanoid-Gym 框架、zero-shot sim-to-real、MuJoCo sim-to-sim。
- 读完应能回答：如果后续做人形，环境结构应该参考什么？

### 20. Learning Human-to-Humanoid Real-Time Whole-Body Teleoperation

- 笔记：[中文笔记](../paper_notes/individual/2403.04436_learning_human_to_humanoid_real_time_whole_body_teleoperation_zh.md)
- PDF: [local PDF](papers/2403.04436_learning_human_to_humanoid_real_time_whole_body_teleoperation.pdf)
- 重点：H2O、人到人形机器人遥操作、motion retargeting。
- 读完应能回答：teleoperation / imitation 和 RL locomotion 的关系是什么？

### 21. OmniH2O: Universal and Dexterous Human-to-Humanoid Whole-Body Teleoperation and Learning

- 笔记：[中文笔记](../paper_notes/individual/2406.08858_omnih2o_universal_and_dexterous_human_to_humanoid_whole_body_teleoperation_and_l_zh.md)
- PDF: [local PDF](papers/2406.08858_omnih2o_universal_and_dexterous_human_to_humanoid_whole_body_teleoperation_and_learning.pdf)
- 重点：更通用的 humanoid whole-body teleoperation。
- 读完应能回答：humanoid MoE 是否可以按 whole-body skill 分专家？

### 22. WoCoCo: Learning Whole-Body Humanoid Control with Sequential Contacts

- 笔记：[中文笔记](../paper_notes/individual/2406.06005_wococo_learning_whole_body_humanoid_control_with_sequential_contacts_zh.md)
- PDF: [local PDF](papers/2406.06005_wococo_learning_whole_body_humanoid_control_with_sequential_contacts.pdf)
- 重点：sequential contacts、whole-body contact control。
- 读完应能回答：contact mode 能否作为 gate input 或 expert label？

### 23. BeamDojo: Learning Agile Humanoid Locomotion on Sparse Footholds

- 笔记：[中文笔记](../paper_notes/individual/2502.10363_beamdojo_learning_agile_humanoid_locomotion_on_sparse_footholds_zh.md)
- PDF: [local PDF](papers/2502.10363_beamdojo_learning_agile_humanoid_locomotion_on_sparse_footholds.pdf)
- 重点：人形机器人 sparse footholds、危险地形、精确落脚。
- 读完应能回答：gap / stepping-stone expert 在人形机器人上会新增哪些困难？

**Phase 4 读完后的动作：**

- 暂时不要把人形机器人作为第一开发目标。
- 把 humanoid 相关结论记录到 future work。
- 四足 MoE 路线稳定后，再评估 Unitree G1/H1 路线。

---

## Phase 5：VLA 拓展阅读

这一阶段用于拓展 vision-language-action、动作序列建模和 imitation-heavy manipulation 的视野。它不是当前 2RL 第一复现目标，但能帮助你理解 ACT、Diffusion Policy、pi0 之间的技术关系。

### 24. Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware

- 笔记：[中文笔记](../paper_notes/individual/2304.13705_learning_fine_grained_bimanual_manipulation_with_low_cost_hardware_zh.md)
- PDF: [local PDF](papers/2304.13705_learning_fine_grained_bimanual_manipulation_with_low_cost_hardware.pdf)
- 重点：ACT、action chunking、transformer imitation learning。
- 读完应能回答：为什么预测一段未来动作可以缓解单步 behavioral cloning 的误差累积？

### 25. Diffusion Policy: Visuomotor Policy Learning via Action Diffusion

- 笔记：[中文笔记](../paper_notes/individual/2303.04137_diffusion_policy_visuomotor_policy_learning_via_action_diffusion_zh.md)
- PDF: [local PDF](papers/2303.04137_diffusion_policy_visuomotor_policy_learning_via_action_diffusion.pdf)
- 重点：条件扩散模型、连续动作序列、receding horizon control。
- 读完应能回答：diffusion action head 为什么比单峰回归更适合多模态示范动作？

### 26. pi0: A Vision-Language-Action Flow Model for General Robot Control

- 笔记：[中文笔记](../paper_notes/individual/2410.24164_pi0_a_vision_language_action_flow_model_for_general_robot_control_zh.md)
- PDF: [local PDF](papers/2410.24164_pi0_a_vision_language_action_flow_model_for_general_robot_control.pdf)
- 重点：VLM backbone、flow matching action expert、generalist robot policy。
- 读完应能回答：pi0 如何把视觉语言理解和连续机器人动作生成连接起来？

**Phase 5 读完后的动作：**

- 把 ACT / Diffusion Policy / pi0 作为 VLA 拓展笔记，不要混入第一阶段 PPO locomotion 实验。
- 记录它们对 action representation 的启发：action chunk、diffusion sequence、flow-matching continuous action。
- 如果未来做 mobile manipulation 或语言条件导航，再考虑把 VLA 作为高层任务接口。

---

## 总结版顺序

```text
0. Integrated literature review
1. Learning to Walk in Minutes
2. RMA
3. Challenging Terrain
4. Sim-to-Real Agile Locomotion
5. Agile and Dynamic Motor Skills
6. Advanced Skills: Locomotion + Local Navigation
7. Risky Terrains
8. Resilient Local Navigation
9. Agile But Safe
10. Robot Parkour Learning
11. Extreme Parkour
12. MoE-Loco
13. MoRE
14. CMoE
15. Parkour in the Wild
16. Reliable Sim-to-Real Predictability for MoE
17. Sparse-Gated Visual MoE Parkour
18. Real-World Humanoid Locomotion
19. Humanoid-Gym
20. H2O
21. OmniH2O
22. WoCoCo
23. BeamDojo
24. ACT / Learning Fine-Grained Bimanual Manipulation
25. Diffusion Policy
26. pi0
```

## 最短可执行路线

如果你现在想尽快开始复现，不需要等 26 篇全读完。最短路线是：

```text
整合综述
→ Learning to Walk in Minutes
→ RMA
→ Challenging Terrain
→ Agile But Safe
→ MoE-Loco
→ 开始配置 Isaac Lab / legged_gym 环境
```
