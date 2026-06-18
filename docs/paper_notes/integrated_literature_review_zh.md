# 整合文献综述

## 范围

本文整合 `docs/references/papers/` 下 26 篇论文，目标不是平均总结每篇论文，而是把文献转化为 2RL 项目的开发路线。

## 1. 先做 baseline，再做 MoE

第一组 locomotion 论文给出的核心结论是：先复现稳定的 command-conditioned locomotion policy，再加入 MoE、感知和 safety。`Learning to Walk in Minutes` 给出了实践入口：GPU 并行仿真、PPO、joint-position target offset、PD controller、速度跟踪奖励、姿态稳定奖励和 terrain curriculum。

因此 2RL 的第一阶段应该产出：

- flat terrain velocity tracking policy；
- rough terrain policy；
- reward curve、fall rate、tracking error 和 rollout video；
- 清晰的 observation / action / reward contract。

## 2. 鲁棒性本质上是 hidden-state estimation

RMA 和复杂地形论文说明，真实机器人无法直接知道摩擦、负载、地形参数、电机偏差和延迟。history encoder 可以从近期本体感知和动作响应中估计这些隐变量。

因此 MoE gate 不应只看当前 observation，还应看：

- proprioception history embedding；
- previous action；
- command tracking error history；
- terrain embedding；
- previous gate weights。

risk estimator 也应使用历史状态和地形上下文，而不是只看当前 roll/pitch。

## 3. 不同地形对应不同目标

flat terrain 看速度和 tracking error；rough terrain 看稳定性；stairs 和 gaps 看脚步、身体 clearance 和成功率；risky terrain 更关心 fall rate、collision rate 和 foot placement safety。

这支持专家划分：

- flat expert：高效速度跟踪；
- rough expert：粗糙地形鲁棒性；
- stair expert：台阶和垂直位移；
- gap expert：稀疏落脚点和跨越；
- recovery expert：高风险状态恢复。

评估必须按地形拆分，不能只给 mixed terrain 平均分。

## 4. 感知要逐步加入

Parkour 和 local navigation 论文说明，机器人需要提前感知台阶、间隙、障碍物和可通行区域。但 resilient navigation 论文也说明，感知会失效：噪声、空洞、遮挡、延迟都会影响策略。

推荐开发顺序：

1. privileged terrain label，用于验证 MoE 是否有效；
2. height samples，作为较容易部署的地形信息；
3. local height map encoder；
4. depth image encoder。

任何 perception-based 结果都应包含 degraded perception 评估。

## 5. Safety 需要显式 routing

`Agile But Safe` 是 safety-aware gate 的直接参考。只靠 reward penalty 不能保证策略在危险状态下及时切换到 recovery behavior。需要 risk estimator 或 safety supervisor 显式影响 routing。

第一版 safety-aware MoE 可以这样做：

- 用未来 N 步内 fall/collision 构造 risk label；
- risk estimator 输出 `[0, 1]` 风险分数；
- 风险高时给 recovery expert 加 gate bias；
- 超过阈值时可 hard override；
- 加 hysteresis 或 temporal smoothness 避免 gate 抖动。

## 6. MoE 有用，但 routing 会失败

MoE-Loco 说明 MoE 可以缓解多任务 locomotion 的冲突。CMoE 和 MoRE 提醒两个风险：

- gate collapse 或均匀分配，专家没有分工；
- 直接 action mixture 破坏 gait phase，导致动作不自然。

推荐路线：

1. rule switch baseline；
2. frozen experts + vanilla soft gate；
3. hard / top-k routing；
4. residual experts；
5. contrastive routing；
6. 最后再 joint fine-tuning。

关键诊断指标：

- expert utilization；
- gate entropy；
- switching frequency；
- activation by terrain；
- per-expert failure case；
- action smoothness 和 torque。

## 7. 人形机器人是后期扩展

Humanoid-Gym、BeamDojo、H2O、OmniH2O、WoCoCo 等论文很有价值，但不应定义第一阶段任务。人形机器人引入更小支撑多边形、全身平衡、上身耦合和多接触序列。2RL 当前应先在四足上验证 MoE 与 safety-aware routing。

## 8. VLA 拓展动作生成视角

ACT、Diffusion Policy 和 pi0 把阅读范围从 locomotion 扩展到 vision-language-action 和 visuomotor manipulation。它们不是当前 2RL 第一复现目标，但能帮助理解现代机器人策略如何输出一段动作序列，而不是每一步独立回归动作。

推荐理解顺序：

1. ACT：用 transformer 做 action chunking；
2. Diffusion Policy：用 diffusion 生成连续动作序列；
3. pi0：把 VLM 条件、flow matching 和机器人 foundation policy 连接起来。

对 2RL 的近期价值主要是架构理解：未来高层 VLA 可以输出语言/视觉条件下的目标、技能或短时动作 horizon，低层仍由 safety-aware locomotion controller 执行。

## 推荐阅读顺序

1. Learning to Walk in Minutes。
2. RMA。
3. Learning Quadrupedal Locomotion over Challenging Terrain。
4. Agile But Safe。
5. MoE-Loco。
6. MoRE。
7. CMoE。
8. Parkour / risky terrain 系列。
9. Humanoid 系列。
10. VLA 拓展：ACT、Diffusion Policy、pi0。

## 对 2RL 的直接实施路线

### Stage A: baseline

- 安装 Isaac Lab 或 legacy legged_gym。
- 训练 flat / rough quadruped PPO policy。
- 记录 observation/action/reward。
- 保存曲线、视频、metrics。

### Stage B: expert library

- 训练 flat、rough、stair、gap、recovery experts。
- 统一 expert observation/action dimensions。
- 单独评估每个 expert。

### Stage C: routing

- 做 rule switch baseline。
- 训练 vanilla gate。
- 可视化 utilization、entropy、switching frequency。

### Stage D: safety

- 构造 risk label。
- 训练 risk estimator。
- 高风险时 bias 或 override 到 recovery expert。
- 对比 vanilla MoE。

### Stage E: specialization

- 加 terrain encoder。
- 加 load balancing 和 temporal smoothness。
- gate 仍不分工时再加 contrastive routing。
- action mixture 不稳定时尝试 residual experts。

### Stage F: VLA optional expansion

- 读 ACT，理解 action chunking。
- 读 Diffusion Policy，理解生成式连续动作 head。
- 读 pi0，把 VLM conditioning、flow matching 和 robot foundation policy 连起来。
- VLA 实验应和第一阶段 locomotion MoE 复现分开。

## 结论边界

当前项目可以声称：已有本地论文库、论文笔记和文献驱动开发路线。还不能声称：已经训练策略、证明 safety-aware MoE 有效或完成 sim-to-real。
