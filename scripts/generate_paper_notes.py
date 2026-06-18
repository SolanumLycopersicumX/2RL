#!/usr/bin/env python3
"""Generate Chinese paper notes for all downloaded 2RL papers."""

from __future__ import annotations

import csv
import re
from pathlib import Path


NOTES: dict[str, dict[str, object]] = {
    "2109.11978": {
        "category": "四足 RL locomotion baseline",
        "priority": "必读，第一篇",
        "summary": "这篇论文是本项目的 baseline 入口。核心价值不是某个复杂网络结构，而是证明 Isaac Gym 大规模并行仿真加 PPO 可以把四足 locomotion 训练从数小时压到分钟级，并形成后来 legged_gym 工作流的工程基础。",
        "problem": "传统腿式机器人 RL 训练慢、环境吞吐不足、调参反馈周期长，导致 locomotion baseline 难以快速复现。",
        "method": "用 GPU 并行物理仿真同时跑大量环境，训练 command-conditioned actor-critic。策略主要输出关节位置 target offset，再由 PD 控制器落到电机层；奖励以速度跟踪、姿态稳定、能耗、动作平滑、接触行为等项组成。",
        "robot_env": "ANYmal 类四足机器人；Isaac Gym；平地、粗糙地形和 curriculum 风格 terrain。",
        "reuse": "2RL 的 Milestone 1 应按它的接口建立 observation/action/reward/config：先跑 flat velocity tracking，再加 rough terrain。MoE 之前不要过早引入感知、gate 或 safety，否则 baseline 不可诊断。",
        "cautions": "不要直接把 reward 权重当成固定真理；先复现可走，再逐项做 reward ablation。Isaac Gym legacy 路径和 Isaac Lab 现代路径要分开。",
    },
    "1804.10332": {
        "category": "Sim-to-real 与 agile locomotion",
        "priority": "必读",
        "summary": "这篇论文关注从仿真训练到真实四足机器人部署。它强调 actuator model、domain randomization、延迟和动力学不确定性，是理解 sim-to-real gap 的基础论文。",
        "problem": "仿真中学到的 gait 往往在真实机器人上失败，原因包括电机响应、摩擦、质量分布、传感噪声和延迟不匹配。",
        "method": "在仿真中训练神经网络控制器，并通过更真实的执行器建模和随机化提升真实部署鲁棒性。策略通常仍是本体感知输入和关节目标输出，而不是直接开环动作。",
        "robot_env": "ANYmal 四足机器人；仿真训练后真实机器人验证。",
        "reuse": "2RL 的环境包和 config 要显式记录 actuator、latency、friction、mass randomization。后续 safety-aware MoE 的 OOD 测试要覆盖这些变量。",
        "cautions": "只在仿真 ablation 中提高 reward 不等于真实可迁移。记录每次训练的随机化范围比只保存 checkpoint 更重要。",
    },
    "1901.08652": {
        "category": "动态运动技能",
        "priority": "必读",
        "summary": "这篇论文展示 RL 可以学习敏捷、动态的腿式运动技能，包括速度跟踪、转向、复杂步态和扰动恢复。它是从“能走”走向“动态技能库”的关键参考。",
        "problem": "单一慢速步态不足以覆盖真实任务；机器人需要在命令变化、外力扰动和不同速度范围内保持稳定。",
        "method": "训练命令条件策略，通过 reward shaping 把速度、姿态、能耗、关节平滑、接触行为等目标组合起来。技能不是单独硬编码，而是通过统一策略在不同 command 下表现出来。",
        "robot_env": "ANYmal 类四足；仿真到真实部署。",
        "reuse": "2RL 的 expert 不应只按地形分，也要记录 command distribution。flat expert 可以作为高速/低风险专家，recovery expert 则覆盖大姿态扰动。",
        "cautions": "动态技能更容易出现 reward hacking。训练视频、fall rate、动作平滑和能耗必须一起看。",
    },
    "2010.11251": {
        "category": "复杂地形 locomotion",
        "priority": "必读",
        "summary": "这篇论文强调四足机器人在挑战性自然地形上的本体感知 locomotion。它说明复杂地形不一定一开始就依赖视觉，历史观测和鲁棒控制也能承载大量适应能力。",
        "problem": "粗糙地面、坡度、障碍和接触不确定性会破坏简单速度跟踪策略。",
        "method": "通过复杂 terrain curriculum、扰动、随机化和本体感知输入训练鲁棒策略，使策略能够在 unseen terrain 上保持移动。",
        "robot_env": "四足机器人；仿真训练，复杂地形和真实/类真实地形评估。",
        "reuse": "2RL 的 rough expert 先用 proprioception + height samples，不急于上 depth image。evaluation 需要按坡度、粗糙度、随机推力拆分，而不是只报告平均成功率。",
        "cautions": "如果只看 mixed terrain 平均分，可能掩盖 stair/gap 的失败模式。专家训练阶段必须记录 per-terrain failure cases。",
    },
    "2107.04034": {
        "category": "Rapid Motor Adaptation",
        "priority": "必读，第二篇",
        "summary": "RMA 是 history encoder 和 latent adaptation 的核心参考。它把不可直接观测的环境因素，如摩擦、负载、地形和电机状态，通过近期本体感知历史估计成 latent，再让 base policy 使用。",
        "problem": "真实机器人不能直接知道摩擦、质量偏差、地形参数等 privileged variables，但这些变量强烈影响动作效果。",
        "method": "两阶段训练：先训练能使用 privileged latent 的 teacher/base policy，再训练 adaptation module 从历史观测预测 latent。部署时只使用真实可观测历史。",
        "robot_env": "腿式机器人；仿真训练，真实环境适应实验。",
        "reuse": "2RL 的 `history_encoder.py` 和 gate input 应借鉴这个思想：gate 不只看当前 obs，也看过去若干步的动作、姿态和速度误差。",
        "cautions": "不要把 privileged terrain label 直接作为最终部署输入。可以先用 label 做 MoE sanity check，再 distill 到 height/history encoder。",
    },
    "2209.12827": {
        "category": "Locomotion + local navigation",
        "priority": "高",
        "summary": "这篇论文把 low-level locomotion 和 local navigation 合到一个学习框架中，目标从简单 velocity tracking 升级为在局部环境中到达目标、避障或通过障碍。",
        "problem": "传统 pipeline 常把导航和运动控制切开，局部 planner 给速度命令，locomotion policy 只负责跟踪；复杂地形下这种分层容易信息断裂。",
        "method": "把目标、局部环境信息和机器人状态纳入策略输入，让策略学习 navigation-aware locomotion。训练中通常需要 curriculum 和任务成功奖励。",
        "robot_env": "腿式机器人；局部导航任务；仿真为主。",
        "reuse": "2RL 的 `mixed_nav_env.py` 后续应把 command velocity 扩展为 goal-conditioned input。MoE gate 可根据 terrain embedding 和 goal context 选择专家。",
        "cautions": "导航奖励会和 locomotion 稳定奖励冲突。先稳定速度跟踪，再加入 goal-reaching，否则 debug 空间太大。",
    },
    "2309.05665": {
        "category": "Robot parkour",
        "priority": "高",
        "summary": "Robot Parkour Learning 把复杂障碍通过技能学习和感知结合起来，是 stair、gap、crawl、jump 等专家设计的重要参考。",
        "problem": "Parkour 障碍需要跨越、攀爬、低姿态通过和恢复等离散技能，单一连续 velocity policy 难以覆盖全部。",
        "method": "训练多个与障碍类型相关的运动技能，并通过感知、课程或蒸馏方法把技能组织成可部署策略。",
        "robot_env": "四足机器人；复杂人工障碍；感知输入和仿真到真实验证。",
        "reuse": "2RL 的 expert 划分 flat/rough/stair/gap/recovery 与 parkour 技能库类似。后续可用 expert checkpoint 生成 teacher，再训练统一 gate 或 student。",
        "cautions": "Parkour 类任务依赖精心设计的课程和初始状态分布。不要直接把 gap expert 放进 mixed terrain，先单独评估失败边界。",
    },
    "2309.14341": {
        "category": "Extreme parkour with perception",
        "priority": "高",
        "summary": "Extreme Parkour 关注视觉/深度感知下的极端障碍穿越。它说明只靠本体感知不足以处理远处障碍和需要提前决策的动作。",
        "problem": "机器人需要在接触之前识别障碍形状、距离和可通行区域，否则 gap、high step、crawl 等动作来不及准备。",
        "method": "使用深度或局部地形感知构造 terrain representation，再结合 locomotion policy 做 end-to-end 或半端到端控制。",
        "robot_env": "四足机器人；深度感知；极端 parkour 地形。",
        "reuse": "2RL 的 terrain encoder 开发顺序可参考：先 label，再 height samples，再 height map/depth image。不要一开始上视觉大模型。",
        "cautions": "视觉策略的 failure mode 包括深度噪声、遮挡、视角延迟。评估必须包含 perception failure 或 noise。",
    },
    "2311.10484": {
        "category": "Risky terrain",
        "priority": "高",
        "summary": "这篇论文把 risky terrain，如 stepping stones、窄梁和稀疏落脚点，建模成更强的局部导航和落脚控制问题。",
        "problem": "普通 rough terrain policy 可以容忍随机接触，但 sparse foothold 任务要求脚落在安全区域，错误一步就可能摔倒。",
        "method": "通过风险地形 curriculum、地形观测和任务奖励训练策略在有限安全支撑区域移动。",
        "robot_env": "四足机器人；stepping stones、窄支撑和危险地形。",
        "reuse": "2RL 的 gap expert 不应只看 body collision，也要记录 foot placement safety。risk estimator 可以把未来 N 步 fall/collision 作为标签。",
        "cautions": "速度指标在 risky terrain 上可能误导；应该优先 success rate、fall rate、foot placement error。",
    },
    "2310.03581": {
        "category": "Resilient local navigation",
        "priority": "高",
        "summary": "这篇论文关注感知受损时的局部导航鲁棒性。它对 2RL 的 safety-aware routing 很重要，因为真实系统的危险往往来自感知失效，而不只是动力学扰动。",
        "problem": "深度相机、height map 或局部地图在真实环境中会有空洞、延迟、噪声和遮挡，端到端 policy 可能过度依赖错误感知。",
        "method": "在训练中显式加入 compromised perception 或 sensor degradation，使策略学会在感知不完美时仍能安全通过。",
        "robot_env": "腿式机器人；局部导航；感知失败场景。",
        "reuse": "2RL 的 OOD evaluation 应加入 sensor noise、missing height samples、stale terrain embedding。safety supervisor 可以在感知置信度低时降低速度或切 recovery。",
        "cautions": "只在 clean depth/height map 上评估 MoE gate 会高估部署可靠性。",
    },
    "2401.17583": {
        "category": "Safety-aware high-speed locomotion",
        "priority": "必读",
        "summary": "Agile But Safe 是 2RL safety-aware gate 的直接参考。它讨论高速敏捷移动中如何在速度和碰撞/摔倒风险之间做权衡，并引入 safety switch 或类似 reach-avoid 的安全判断。",
        "problem": "高 reward 的 agile policy 可能在危险状态继续追求速度，不能保证及时避障或恢复。",
        "method": "训练/使用安全评估模块识别高风险状态，在必要时切换到更保守或 recovery 行为。核心思想是让 safety 不是 reward 的附属项，而是 routing/supervision 的显式输入。",
        "robot_env": "腿式机器人；高速、障碍、collision-free local locomotion。",
        "reuse": "2RL 的 `risk_estimator.py`、`safety_supervisor.py` 和 recovery expert 设计应以它为主要参考。评价必须比较 vanilla MoE 与 safety-aware MoE 的 fall/collision。",
        "cautions": "阈值型 safety switch 简单但可能抖动。需要 temporal smoothing、hysteresis 或 recovery cooldown。",
    },
    "2303.03381": {
        "category": "Humanoid RL locomotion",
        "priority": "中，高价值延伸",
        "summary": "这篇论文展示真实人形机器人可以通过 RL 学会 locomotion，是从四足扩展到 humanoid 的重要参考。它强调历史信息、鲁棒性和真实部署。",
        "problem": "人形机器人比四足更容易因支撑多边形小、接触切换复杂和上身姿态耦合而摔倒。",
        "method": "训练适合真实部署的 humanoid policy，通常需要更强的历史建模、动力学随机化和姿态/接触稳定约束。",
        "robot_env": "真实人形机器人；仿真训练和真实部署。",
        "reuse": "2RL 初期不做人形，但 G1/H1 配置和 MoE residual policy 可以为后续迁移保留接口。",
        "cautions": "不要把四足 reward 直接搬到 humanoid。humanoid 需要 CoM、上身、脚接触和摔倒边界的额外设计。",
    },
    "2404.05695": {
        "category": "Humanoid-Gym framework",
        "priority": "中，环境参考",
        "summary": "Humanoid-Gym 是开源 humanoid RL 框架，目标是让 humanoid locomotion 训练、评估和 sim-to-real 路径更容易复现。",
        "problem": "人形机器人 RL 项目常缺少可复现环境、统一配置和 sim-to-sim 验证。",
        "method": "提供 Isaac Gym 风格训练框架、任务配置、机器人模型和 MuJoCo 等 sim-to-sim 验证接口。",
        "robot_env": "Unitree H1/G1 等 humanoid；Isaac Gym 和 MuJoCo。",
        "reuse": "2RL 的 `docs/setup/ENVIRONMENT.md` 已把 Humanoid-Gym 放到后期路径。后续做人形 MoE 时可参考它的 config 分层和 zero-shot sim-to-real 检查。",
        "cautions": "Humanoid-Gym 是后期扩展，不应阻塞当前四足 baseline。",
    },
    "2403.04436": {
        "category": "Human-to-humanoid teleoperation",
        "priority": "中",
        "summary": "H2O 关注从人体动作到人形机器人实时全身遥操作。它不是 2RL 第一阶段的 locomotion baseline，但对 motion imitation、whole-body control 和 humanoid skill prior 很有价值。",
        "problem": "人体动作和 humanoid 机器人形态相近但动力学不同，直接 retarget 会产生不可执行或不稳定动作。",
        "method": "把人类动作重定向到机器人，再通过学习和仿真优化得到实时可执行的全身控制策略。",
        "robot_env": "人形机器人；人体动作输入；全身遥操作。",
        "reuse": "后续 humanoid MoE 可把不同人类动作或 gait style 作为专家来源。residual expert 思路也可从 imitation policy 上叠加。",
        "cautions": "该方向偏 imitation/teleoperation，不应和 quadruped local navigation 主线混淆。",
    },
    "2406.08858": {
        "category": "Universal humanoid teleoperation",
        "priority": "中",
        "summary": "OmniH2O 扩展 H2O 到更通用、更灵巧的人形全身遥操作和学习，强调泛化到多任务和多身体部位控制。",
        "problem": "单一遥操作策略难覆盖手臂、躯干、腿部和全身协调，特别是在任务和人体动作变化时。",
        "method": "结合人体动作重定向、学习策略和全身控制，让 humanoid 能实时跟随更丰富的人体动作。",
        "robot_env": "人形机器人；全身遥操作；学习型控制。",
        "reuse": "对 2RL 的启发是：humanoid MoE 可以按全身技能或 contact pattern 分专家，而不只按地形分专家。",
        "cautions": "它依赖人类动作数据和遥操作 pipeline，和本项目第一阶段 PPO locomotion 复现不是同一工程闭环。",
    },
    "2406.06005": {
        "category": "Sequential contacts for humanoids",
        "priority": "中",
        "summary": "WoCoCo 聚焦 sequential contacts 下的 humanoid whole-body control。它对 BeamDojo、parkour 和 humanoid recovery 有参考价值。",
        "problem": "人形机器人在攀爬、支撑、翻越等任务中会发生手、脚和身体多部位接触，接触顺序复杂且非平滑。",
        "method": "把复杂任务拆成接触序列或 contact-aware 控制问题，通过学习控制策略处理不同接触阶段。",
        "robot_env": "人形机器人；全身接触任务。",
        "reuse": "2RL 后期可以把 contact mode 作为 MoE gate 的输入或专家标签，例如 walking、hand support、recovery contact。",
        "cautions": "四足 baseline 阶段不需要 whole-body contact complexity；先保留概念，不要过早实现。",
    },
    "2502.10363": {
        "category": "Humanoid sparse footholds",
        "priority": "中高",
        "summary": "BeamDojo 把 sparse foothold 和 humanoid agility 结合起来，是人形机器人 risky terrain 的重要参考。",
        "problem": "稀疏落脚点对人形机器人尤其困难，因为平衡裕度小，错误落脚会导致快速失败。",
        "method": "构建针对窄梁、稀疏支撑和危险地形的训练环境与课程，让策略学习精确落脚和平衡恢复。",
        "robot_env": "人形机器人；sparse footholds、beam、危险地形。",
        "reuse": "2RL 的 gap/stepping-stone expert 可借鉴其 evaluation 指标：落脚成功率、摔倒率、恢复率，而不是只看速度。",
        "cautions": "BeamDojo 是 humanoid 高难度任务，不适合作为第一复现目标。",
    },
    "2503.08564": {
        "category": "MoE locomotion",
        "priority": "必读",
        "summary": "MoE-Loco 是本项目 MoE 方向的核心论文。它把多任务 locomotion 中的专家分工和 gate routing 明确化，用 MoE 缓解单一策略在多技能、多地形或多 gait 上的冲突。",
        "problem": "单一大 policy 在多任务 locomotion 中容易出现 gradient conflict、技能互相干扰、特定任务性能下降。",
        "method": "训练多个 expert 或在网络中引入 expert modules，由 gate 根据状态/任务选择或混合专家输出。通常需要 load balancing、entropy 或 routing regularization。",
        "robot_env": "腿式机器人，多任务 locomotion。",
        "reuse": "2RL 的 `moe_policy.py`、`gating_network.py`、`ppo_gate.yaml` 应以它为第一版参考。先固定 expert 训练 gate，再考虑 joint fine-tune。",
        "cautions": "直接 action mixture 可能破坏 gait phase。要比较 hard routing、top-k、soft mixture 和 residual experts。",
    },
    "2603.03067": {
        "category": "Contrastive MoE routing",
        "priority": "高",
        "summary": "CMoE 关注用 contrastive routing 促进专家分工，避免 gate 在所有地形上输出接近均匀的分布。",
        "problem": "普通 MoE gate 可能 collapse 到单个 expert，或在所有 terrain 上平均分配，导致专家没有明确职责。",
        "method": "引入 contrastive loss：同类地形/任务的 gate activation 更接近，不同地形/任务的 activation 更分离，同时结合 load balancing 和 temporal smoothness。",
        "robot_env": "humanoid motion control 与 terrain adaptation。",
        "reuse": "2RL 的 `moe_regularization.py` 已预留 contrastive routing loss。Milestone 6 可以用 terrain label 先构造正负样本。",
        "cautions": "contrastive label 如果太粗会强迫错误分工；例如 rough 和 stairs 之间可能共享部分专家。",
    },
    "2506.08840": {
        "category": "Residual experts",
        "priority": "高",
        "summary": "MoRE 提出 mixture of residual experts，用 residual action 或 residual latent 改善直接混合多个完整动作策略的不稳定问题。",
        "problem": "不同 expert 的 gait phase、动作尺度和隐式控制风格不同，直接加权 action 可能产生不可自然执行的关节目标。",
        "method": "使用 base policy 产生主动作，多个 residual expert 只输出修正量。gate 混合 residual，而不是混合完整策略动作。",
        "robot_env": "humanoid lifelike gaits 与复杂地形。",
        "reuse": "2RL 已有 `residual_expert_policy.py`。如果 vanilla soft MoE 出现动作抖动，下一步优先试 residual expert，而不是盲目调 gate 网络。",
        "cautions": "residual 方法要求 base policy 足够稳定。base 不稳时 residual 只会掩盖问题。",
    },
    "2505.11164": {
        "category": "Multi-expert distillation",
        "priority": "高",
        "summary": "Parkour in the Wild 关注多专家蒸馏和 RL fine-tuning，把多个地形/障碍专家整合成更通用的敏捷 locomotion policy。",
        "problem": "单独专家容易在各自地形表现好，但部署时需要跨地形连续切换，手写规则或频繁切换会造成不稳定。",
        "method": "先训练 terrain-specific experts，再通过 DAgger 或 distillation 让 unified policy 学习专家行为，最后用 RL fine-tuning 提升真实任务表现。",
        "robot_env": "腿式机器人；parkour in the wild；多障碍技能。",
        "reuse": "2RL 的专家训练路线可以在 MoE gate 之外保留 distillation 备选方案：experts -> gate/MoE 或 experts -> student policy。",
        "cautions": "蒸馏会压缩专家差异。若研究目标是解释 expert utilization，MoE gate 比完全蒸馏更容易分析。",
    },
    "2602.00678": {
        "category": "MoE sim-to-real predictability",
        "priority": "高",
        "summary": "这篇论文关注 MoE robust quadrupedal locomotion 的 sim-to-real 可预测性。它提醒我们：MoE 在仿真中表现好，不代表真实部署风险可控。",
        "problem": "多专家策略增加了策略空间复杂度，也增加了仿真评估与真实表现之间的不确定性。",
        "method": "通过更系统的 sim-to-real predictability framework 或 benchmark 评估 MoE 策略在真实部署前的可靠性。",
        "robot_env": "Unitree Go2 等四足机器人；MoE locomotion；sim-to-real 评估。",
        "reuse": "2RL 的最终 ablation 不应只看平均 success；要加入 OOD friction/mass/latency、expert switching frequency、gate entropy 和 recovery trigger。",
        "cautions": "如果没有真实机器人，报告中必须清楚写明 claim boundary，只能说 simulation evidence。",
    },
    "2604.19344": {
        "category": "Visual sparse-gated MoE parkour",
        "priority": "进阶参考",
        "summary": "这篇论文把 quadruped parkour、视觉输入和 sparse-gated MoE 结合起来，是 2RL 的进阶目标参考。",
        "problem": "复杂 parkour 场景需要根据视觉判断障碍类型，同时避免所有 expert 都被激活导致计算和动作混合复杂。",
        "method": "使用视觉输入构造环境表示，通过 sparse gate 或 top-k gate 激活少数 expert，提升任务专门化和部署效率。",
        "robot_env": "四足机器人；parkour；视觉感知；MoE。",
        "reuse": "2RL 在 vanilla MoE 稳定后可以尝试 top-k routing 和 terrain/depth encoder。它也支持本项目把 perception 放到后期，而非第一阶段。",
        "cautions": "视觉 MoE 是高复杂度组合，不应在 baseline 未稳定时引入。",
    },
    "2304.13705": {
        "category": "VLA / imitation learning / action chunking",
        "priority": "拓展阅读，VLA 第一篇",
        "summary": "ACT 不是 locomotion 论文，但它是理解机器人动作序列建模的关键入口。它把 imitation policy 建模为 action chunk generator，用 transformer 一次预测未来一段动作，缓解长时序模仿学习中的误差累积。",
        "problem": "高精度双臂操作需要连续闭环控制，普通 behavioral cloning 容易因为单步误差累积而偏离示范轨迹，尤其是在低成本、不精确硬件上更明显。",
        "method": "Action Chunking with Transformers 使用图像和机器人状态作为条件，预测一段未来动作序列，并在执行时通过 temporal ensembling 平滑多个 chunk 的重叠预测。",
        "robot_env": "ALOHA 低成本双臂平台；真实机器人示范；精细双臂 manipulation 任务。",
        "reuse": "2RL 可借鉴 action chunking 的思想来理解高层策略输出短时 horizon 动作序列，而不是每步独立动作。它也为后续阅读 Diffusion Policy 和 pi0 的 action decoder 打基础。",
        "cautions": "ACT 偏真实机器人 imitation learning，不是 PPO locomotion baseline。不要把它的训练流程直接套到当前四足 RL 主线；应作为 VLA/动作序列建模拓展阅读。",
    },
    "2303.04137": {
        "category": "VLA / diffusion policy / visuomotor control",
        "priority": "拓展阅读，VLA 第二篇",
        "summary": "Diffusion Policy 把机器人策略看成条件扩散模型，生成一段连续动作序列。它是理解后续 diffusion/flow action head 的基础，也是 pi0 这类连续动作 VLA 的重要前置概念。",
        "problem": "机器人示范数据常有多模态动作分布，单峰回归会平均掉不同可行轨迹，导致动作不稳定或不可执行。",
        "method": "把观测条件输入扩散模型，通过去噪过程生成未来动作序列，并用 receding horizon control 执行前几个动作后重新规划。",
        "robot_env": "多种仿真和真实机器人 manipulation benchmark；视觉输入和机器人状态条件。",
        "reuse": "2RL 可把它作为“连续动作生成器”的参考：如果未来做 mobile manipulation 或 VLA locomotion-command interface，diffusion/flow decoder 比离散动作 token 更适合高维连续控制。",
        "cautions": "扩散推理计算成本高，且论文重点是 manipulation imitation，不是腿式 locomotion RL。读它时关注 action representation，不要过早迁移到 2RL 主训练代码。",
    },
    "2410.24164": {
        "category": "VLA / robot foundation model / flow matching",
        "priority": "拓展阅读，VLA 第三篇",
        "summary": "pi0 是通用 VLA robot policy 的代表：用预训练 VLM 提供视觉语言理解，再用 flow matching 风格的 action expert 输出连续机器人动作。",
        "problem": "传统单任务机器人策略难以跨任务、跨机器人和跨语言指令泛化；离散动作 token 又可能限制高频、精细、连续控制。",
        "method": "在视觉语言模型基础上加入动作生成模块，用大规模多机器人轨迹训练 generalist policy，并通过 flow matching 生成连续动作序列。",
        "robot_env": "多种真实机器人平台，包括单臂、双臂和移动操作任务；语言指令、视觉观测和连续动作。",
        "reuse": "2RL 可用它拓展研究视野：locomotion MoE 解决地形/技能 routing，VLA 解决语言和视觉条件下的通用动作生成。未来可以把 VLA 作为高层任务指令接口，低层仍由安全 locomotion policy 执行。",
        "cautions": "pi0 是大规模 foundation model 方向，复现成本远高于当前 2RL。当前目标应是理解架构和 action head，不应把训练 pi0 作为近期里程碑。",
    },
}


def slugify(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "_", text.lower()).strip("_")[:80]


def load_manifest(root: Path) -> list[dict[str, str]]:
    manifest = root / "docs" / "references" / "papers" / "papers_manifest.csv"
    with manifest.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def make_note(row: dict[str, str], note: dict[str, object]) -> str:
    title = row["title"]
    arxiv_id = row["arxiv_id"]
    filename = row["filename"]
    text_file = Path(filename).with_suffix(".txt").name
    return f"""# {title}

## Metadata

- arXiv: [{arxiv_id}]({row["abs_url"]})
- PDF: [local PDF](../../references/papers/{filename})
- Extracted text: [local text](../extracted_text/{text_file})
- Category: {note["category"]}
- Reading priority: {note["priority"]}

## One-Sentence Takeaway

{note["summary"]}

## Problem

{note["problem"]}

## Core Method

{note["method"]}

## Environment / Robot / Simulator

{note["robot_env"]}

## What To Reuse In 2RL

{note["reuse"]}

## Cautions

{note["cautions"]}

## Reading Checklist

- Identify observation space and which parts are deployable without privileged information.
- Identify action representation and low-level controller assumption.
- List reward terms and termination conditions.
- Record simulator/framework versions if the paper provides them.
- Record evaluation metrics that can map to `experiments/README.md`.
"""


def write_individual_notes(root: Path, rows: list[dict[str, str]]) -> list[tuple[str, str]]:
    output_dir = root / "docs" / "paper_notes" / "individual"
    output_dir.mkdir(parents=True, exist_ok=True)
    index_rows: list[tuple[str, str]] = []
    for row in rows:
        arxiv_id = row["arxiv_id"]
        if arxiv_id not in NOTES:
            raise KeyError(f"Missing note data for {arxiv_id}: {row['title']}")
        note_path = output_dir / f"{arxiv_id}_{slugify(row['title'])}.md"
        note_path.write_text(make_note(row, NOTES[arxiv_id]), encoding="utf-8")
        index_rows.append((row["title"], str(note_path.relative_to(root))))
    return index_rows


def write_notes_index(root: Path, index_rows: list[tuple[str, str]]) -> None:
    lines = [
        "# Individual Paper Notes",
        "",
        "Generated from `docs/references/papers/papers_manifest.csv`.",
        "",
    ]
    for title, path in index_rows:
        lines.append(f"- [{title}](../../{path})")
    lines.append("")
    (root / "docs" / "paper_notes" / "individual" / "README.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def write_integrated_review(root: Path) -> None:
    text = """# Integrated Literature Review

## Scope

This synthesis covers the 26 papers downloaded under `docs/references/papers/`.
The goal is not to summarize every result equally, but to convert the literature
into a concrete development path for **Safety-Aware MoE-Gated Locomotion for
Legged Local Navigation**.

## 1. Baseline Comes Before MoE

The first cluster of papers shows a clear lesson: start with a stable
command-conditioned locomotion policy before adding routing, perception, or
safety. `Learning to Walk in Minutes` provides the practical baseline: GPU
parallel simulation, PPO, joint-position target offsets, PD control, reward
terms for velocity tracking and stability, and curriculum/randomization. The
sim-to-real and agile locomotion papers add that actuator modeling, latency,
friction, mass variation, and action smoothness must be part of the training
contract, not afterthoughts.

For 2RL, this means Milestone 1 should produce:

- one flat-terrain velocity tracking policy;
- one rough-terrain policy with randomization;
- saved reward curves, fall rate, command tracking error, and rollout videos;
- a documented observation/action/reward contract.

MoE should not start until these baselines are reproducible.

## 2. Robustness Is Mostly Hidden-State Estimation

RMA and the challenging-terrain papers frame robustness as inference over hidden
environment state. The robot cannot directly observe friction, payload, terrain
compliance, actuator mismatch, or sensor delay. A history encoder can infer some
of these variables from recent proprioception and action-response mismatch.

For 2RL, this suggests the gate input should include:

- proprioception history embedding;
- previous action and action-rate features;
- command tracking error history;
- terrain embedding if available;
- previous gate weights for temporal smoothing.

The same logic applies to the risk estimator: risk should be predicted from
state history and terrain context, not just current roll/pitch.

## 3. Terrain Difficulty Changes The Objective

Rough terrain, stairs, gaps, sparse footholds, and parkour are not just harder
versions of flat locomotion. They require different success definitions. For
flat terrain, speed and tracking error matter. For risky terrain, fall rate,
foot placement safety, collision rate, recovery success, and goal completion are
more important.

This motivates the planned expert split:

- flat expert: efficient command tracking;
- rough expert: robust terrain adaptation;
- stair expert: vertical stepping and body clearance;
- gap expert: sparse foothold and contact precision;
- recovery expert: high-risk state stabilization.

The evaluation must report per-terrain metrics. A single mixed-terrain average
can hide expert failure.

## 4. Perception Should Be Added Gradually

Parkour and local-navigation papers show why perception matters: the robot must
anticipate stairs, gaps, crawl spaces, and obstacles before contact. However,
the resilient-navigation papers also show that perception can fail through
noise, missing depth, latency, or occlusion.

The development order should be:

1. privileged terrain label for MoE sanity checks;
2. height samples for deployable terrain cues;
3. local height map encoder;
4. depth image encoder only after earlier stages are stable.

Every perception-based result should include a degraded-perception evaluation.

## 5. Safety Needs Explicit Routing

`Agile But Safe` is the most direct reference for the safety-aware part of 2RL.
Reward penalties alone do not guarantee that a high-speed or high-reward policy
will switch to conservative behavior at the right time. A separate risk
estimator or safety supervisor gives the policy a mechanism to bias or force
recovery behavior.

The first 2RL safety implementation should be simple:

- train or label risk from future fall/collision within N steps;
- output a scalar risk score;
- add recovery-expert bias when risk is high;
- optionally use hard override above a threshold;
- add hysteresis or temporal smoothing to avoid gate chatter.

The ablation should compare vanilla MoE and safety-aware MoE on fall rate,
collision rate, recovery trigger frequency, and OOD terrain performance.

## 6. MoE Helps, But Routing Can Fail

MoE-Loco motivates expert specialization for multitask locomotion. CMoE and
MoRE describe two important failure modes:

- gate collapse or uniform routing, where experts do not specialize;
- unsafe action mixing, where complete expert actions are blended despite
  incompatible gait phase or control style.

For 2RL, the safe progression is:

1. frozen experts + rule switch baseline;
2. frozen experts + vanilla soft gate;
3. hard or top-k gate if soft mixture is unstable;
4. residual expert MoE if action mixture causes unnatural motion;
5. contrastive routing if gate activation is not terrain-specific;
6. joint fine-tuning only after routing diagnostics are reliable.

Key diagnostics:

- expert utilization;
- gate entropy;
- switching frequency;
- activation by terrain;
- per-expert failure cases;
- action-rate and torque smoothness.

## 7. Humanoid Papers Are A Later Extension

The humanoid papers are valuable but should not define the first implementation
target. They add smaller support polygons, whole-body balance, upper-body
coupling, contact sequences, and motion imitation. Humanoid-Gym, BeamDojo,
H2O, OmniH2O, WoCoCo, and real-world humanoid locomotion papers should guide a
second phase after quadruped MoE works.

For now, keep humanoid support as config/interface readiness:

- `configs/robot/unitree_g1.yaml`;
- residual expert policy;
- later Humanoid-Gym external path;
- claim boundary that humanoid results are future work.

## 8. VLA Papers Broaden The Action-Generation View

ACT, Diffusion Policy, and pi0 extend the reading set beyond locomotion into
vision-language-action and visuomotor manipulation. Their direct training
pipelines are not the first 2RL implementation target, but they are useful for
understanding how modern robot policies generate action sequences instead of
single-step commands.

The useful progression is:

1. ACT: transformer-based action chunking for imitation learning;
2. Diffusion Policy: conditional diffusion over continuous action sequences;
3. pi0: VLM-conditioned flow matching for general robot control.

For 2RL, the near-term takeaway is architectural rather than implementation
heavy: a high-level language or vision-conditioned policy can eventually
produce goals, skills, or short action horizons, while the safety-aware
locomotion controller remains the low-level execution layer.

## Recommended Reading Order

1. `2109.11978` Learning to Walk in Minutes.
2. `2107.04034` RMA.
3. `2010.11251` Challenging Terrain.
4. `2401.17583` Agile But Safe.
5. `2503.08564` MoE-Loco.
6. `2506.08840` MoRE.
7. `2603.03067` CMoE.
8. Parkour and risky-terrain papers.
9. Humanoid papers.
10. VLA expansion: ACT, Diffusion Policy, pi0.

## Direct Implementation Plan Derived From The Literature

### Stage A: Reproducible Baseline

- Install Isaac Lab or legacy legged_gym.
- Train flat and rough quadruped PPO policies.
- Record observation/action/reward.
- Save curves, videos, and metrics.

### Stage B: Expert Library

- Train flat, rough, stair, gap, and recovery experts.
- Standardize expert observation/action dimensions.
- Evaluate each expert on both in-domain and mixed terrain.

### Stage C: Routing

- Implement rule switch as a non-learned baseline.
- Train vanilla gate over frozen experts.
- Plot utilization, entropy, and switching frequency.

### Stage D: Safety

- Build risk labels from future fall/collision.
- Train risk estimator.
- Bias or override routing to recovery expert.
- Compare against vanilla MoE.

### Stage E: Specialization

- Add terrain encoder.
- Add load balancing and temporal smoothness.
- Add contrastive routing only after baseline gate is diagnosable.
- Try residual experts if action mixture is unstable.

### Stage F: Optional VLA Expansion

- Read ACT to understand action chunking.
- Read Diffusion Policy to understand generative continuous action heads.
- Read pi0 to connect VLM conditioning, flow matching, and robot foundation
  policies.
- Keep VLA experiments separate from the first locomotion MoE milestone.

## Claim Boundary

After reading and note generation, 2RL can claim it has a literature-backed
development roadmap and local paper archive. It still cannot claim trained
policies, safety improvement, or sim-to-real reliability until actual
experiments under `experiments/` support those claims.
"""
    (root / "docs" / "paper_notes" / "integrated_literature_review.md").write_text(
        text, encoding="utf-8"
    )


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    rows = load_manifest(root)
    index_rows = write_individual_notes(root, rows)
    write_notes_index(root, index_rows)
    write_integrated_review(root)
    print(f"Wrote {len(index_rows)} individual notes.")
    print("Wrote docs/paper_notes/integrated_literature_review.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
