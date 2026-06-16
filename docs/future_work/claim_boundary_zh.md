# 结论边界

本文档说明当前项目可以声称什么，不能声称什么。

## Bootstrap 阶段

可以声称：

- 仓库已经按 legged-locomotion MoE 研究项目组织。
- 已整理论文、依赖、环境和复现路线。
- 已有 MoE routing、terrain encoder、risk estimator、evaluation 等模块接口。

不能声称：

- 已训练出任何策略。
- 已跑通 Isaac Lab 或 legged_gym 实验。
- safety-aware MoE 已经提升性能。
- 已完成 sim-to-real。

## Baseline 阶段

只有记录以下内容后，才能声称 baseline 复现有效：

- framework 版本和 commit；
- 训练命令；
- seed；
- config；
- reward curve；
- rollout video 或确定性 evaluation summary。

## Safety-Aware MoE 阶段

不能只根据 reward 说“更安全”。至少需要：

- vanilla MoE 对比；
- recovery trigger frequency；
- fall / collision rate；
- failure case analysis；
- OOD terrain 或扰动评估。
