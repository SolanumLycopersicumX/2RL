# Safety-Aware MoE-Gated Locomotion for Legged Local Navigation

本仓库是一个面向腿式机器人强化学习运动控制的研究型工作区，目标是学习、复现并扩展：

**面向腿式局部导航的安全感知 MoE 门控运动控制**

项目来源于 `rl_locomotion_moe_research_plan.md`，并参考 `/home/tomato/3YP` 的研究项目管理方式，但最终采用更紧凑的 Python 科研项目结构。

## 项目目标

1. 复现四足机器人 RL locomotion baseline。
2. 训练 flat、rough、stair、gap、recovery 等地形/功能专家策略。
3. 实现固定专家上的 MoE gate。
4. 加入 terrain encoder 和 risk estimator，实现 safety-aware routing。
5. 对比 single policy、rule switch、vanilla MoE、safety MoE、contrastive MoE、residual expert MoE。
6. 输出可读的论文笔记、实验日志、曲线图、视频和最终报告材料。

## 当前目录结构

```text
2RL/
├── configs/                # robot / terrain / train / MoE YAML 配置
├── docs/                   # 项目索引、环境部署、引用资料、论文笔记
├── experiments/            # 实验输出和 summary
├── models/                 # checkpoint 和导出策略，本地大文件默认不进 git
├── data/                   # 本地数据，本地大文件默认不进 git
├── external/               # Isaac Lab、legged_gym 等外部仓库克隆位置
├── assets/                 # figures / videos / gifs
├── notebooks/              # 分析 notebook
├── scripts/                # 训练、验证、下载和维护脚本
├── safe_moe_locomotion/    # 主 Python 包
└── tests/                  # 轻量测试
```

## 推荐阅读入口

- [项目索引](docs/project_index_zh.md)
- [目录结构规则](docs/project_structure_zh.md)
- [环境部署指南](docs/setup/ENVIRONMENT_zh.md)
- [28 篇论文推荐阅读顺序](docs/references/recommended_reading_order_zh.md)
- [整合文献综述](docs/paper_notes/integrated_literature_review_zh.md)
- [单篇论文笔记索引](docs/paper_notes/individual/README_zh.md)

## 快速验证

```bash
python scripts/validate_project.py
sh scripts/run_tests.sh
python -m safe_moe_locomotion.training.run_experiment --config configs/train/ppo_gate.yaml --dry-run
```

## 当前状态

当前仓库完成的是学习、复现和开发环境的 bootstrap：论文、环境、项目结构、配置模板、代码骨架和验证脚本已经齐备。真实 Isaac Lab / legged_gym 训练 adapter 需要在仿真环境安装完成后继续接入。
