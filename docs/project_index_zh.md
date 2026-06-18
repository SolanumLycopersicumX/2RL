# 项目索引

这个文件是 `/home/tomato/2RL` 的中文导航入口。第一次打开项目时，建议先读这里。

## 主要入口

- `README_zh.md`：中文项目总览。
- `README.md`：英文项目总览。
- `rl_locomotion_moe_research_plan.md`：原始中文长期研究计划。
- `Codex_Log.md`：任务进度日志。
- `docs/project_structure_zh.md`：目录结构和维护规则。
- `docs/setup/ENVIRONMENT_zh.md`：中文环境部署指南。
- `docs/setup/PACKAGE_INVENTORY_zh.md`：依赖包和外部框架清单。
- `docs/references/paper_index_zh.md`：论文清单。
- `docs/references/recommended_reading_order_zh.md`：26 篇论文推荐阅读顺序。
- `docs/paper_notes/integrated_literature_review_zh.md`：所有论文的整合笔记。
- `experiments/README_zh.md`：实验输出规范。

## 代码区域

- `safe_moe_locomotion/envs/`：环境接口和 observation contract。
- `safe_moe_locomotion/policies/`：expert、MoE、safety-aware、residual policy。
- `safe_moe_locomotion/modules/`：terrain/history encoder、gating network、risk estimator、safety supervisor。
- `safe_moe_locomotion/rewards/`：locomotion、navigation、recovery、MoE regularization。
- `safe_moe_locomotion/training/`：训练入口和后续 simulator adapter。
- `safe_moe_locomotion/evaluation/`：rollout、metrics、terrain sweep、ablation。
- `safe_moe_locomotion/utils/`：config、logging、checkpoint、video 工具。

## 维护规则

1. 可复用代码放 `safe_moe_locomotion/`。
2. 实验输出放 `experiments/`，并保留 `summary.json`。
3. 大模型权重放 `models/` 或外部存储。
4. 外部 repo 链接和 commit 记录放 `docs/references/`。
5. 大规模自动化修改后更新 `Codex_Log.md`。
