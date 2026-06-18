#!/usr/bin/env python3
"""Generate Chinese Markdown counterparts for the project documentation."""

from __future__ import annotations

from pathlib import Path

from generate_paper_notes import NOTES, load_manifest, slugify


ROOT = Path(__file__).resolve().parents[1]


def write(path: str, content: str) -> None:
    output = ROOT / path
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"wrote {path}")


def paper_note_zh(row: dict[str, str], note: dict[str, object]) -> str:
    filename = row["filename"]
    text_file = Path(filename).with_suffix(".txt").name
    return f"""# {row["title"]}

## 元数据

- arXiv: [{row["arxiv_id"]}]({row["abs_url"]})
- 本地 PDF: [local PDF](../../references/papers/{filename})
- 提取文本: [local text](../extracted_text/{text_file})
- 类别: {note["category"]}
- 阅读优先级: {note["priority"]}

## 一句话结论

{note["summary"]}

## 研究问题

{note["problem"]}

## 核心方法

{note["method"]}

## 环境 / 机器人 / 仿真器

{note["robot_env"]}

## 对 2RL 的可复用点

{note["reuse"]}

## 注意事项

{note["cautions"]}

## 阅读检查清单

- 明确 observation space，并区分哪些输入是真实部署可观测的，哪些是 privileged 信息。
- 明确 action representation 和底层控制器假设。
- 记录 reward terms、termination conditions 和 curriculum 设计。
- 如果论文给出 simulator/framework 版本，记录版本和仓库来源。
- 把 evaluation metrics 映射到 `experiments/README.md` 的实验记录格式。
"""


def generate_individual_notes() -> None:
    rows = load_manifest(ROOT)
    lines = [
        "# 单篇论文笔记",
        "",
        "这些中文笔记根据 `docs/references/papers/papers_manifest.csv` 和英文版单篇笔记生成。",
        "",
    ]
    for row in rows:
        arxiv_id = row["arxiv_id"]
        note = NOTES[arxiv_id]
        path = (
            ROOT
            / "docs"
            / "paper_notes"
            / "individual"
            / f"{arxiv_id}_{slugify(row['title'])}_zh.md"
        )
        path.write_text(paper_note_zh(row, note), encoding="utf-8")
        rel = path.relative_to(ROOT)
        lines.append(f"- [{row['title']}](../../{rel})")
    write("docs/paper_notes/individual/README_zh.md", "\n".join(lines))


def main() -> int:
    write(
        "README_zh.md",
        """
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
- [26 篇论文推荐阅读顺序](docs/references/recommended_reading_order_zh.md)
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
""",
    )

    write(
        "docs/project_index_zh.md",
        """
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
""",
    )

    write(
        "docs/project_structure_zh.md",
        """
# 项目结构指南

本文档记录 `/home/tomato/2RL` 的目录整理规则，防止后续再次出现大量零散顶层文件夹。

## 目标结构

```text
2RL/
├── configs/
├── docs/
├── experiments/
├── models/
├── data/
├── external/
├── assets/
├── notebooks/
├── scripts/
├── safe_moe_locomotion/
└── tests/
```

## 为什么这样整理

早期 bootstrap 同时混用了两种结构：

- 3YP 风格编号目录，例如 `03_Experiments/`、`07_References/`；
- 标准 Python 项目目录，例如 `docs/`、`configs/`、`scripts/`、`safe_moe_locomotion/`。

这会让顶层目录过多、职责重复。现在保留 Python 科研项目结构，把研究资料统一放入 `docs/`。

## 迁移映射

| 旧路径 | 新路径 |
|---|---|
| `05_Documentation/PROJECT_INDEX.md` | `docs/project_index.md` |
| `07_References/` | `docs/references/` |
| `03_Experiments/` | `experiments/` |
| `04_Trained_Models/` | `models/` |
| `06_Data/` | `data/` |
| `08_External/` | `external/` |
| `02_Code/README.md` | `docs/code_organization.md` |
| `01_Reports/` | `docs/reports/` |

## 新文件应该放哪里

| 文件类型 | 位置 |
|---|---|
| 可复用源代码 | `safe_moe_locomotion/` |
| 测试 | `tests/` |
| YAML 配置 | `configs/` |
| CLI 和维护脚本 | `scripts/` |
| 环境部署文档 | `docs/setup/` |
| 论文、引用、外部 repo 记录 | `docs/references/` |
| 论文笔记 | `docs/paper_notes/` |
| 实验输出 | `experiments/` |
| checkpoint / policy export | `models/` |
| 本地数据集 | `data/` |
| 外部仓库克隆 | `external/` |
| 图、视频、GIF | `assets/` |
| notebook | `notebooks/` |

## 规则

1. 不再新增编号式顶层目录。
2. PDF、全文提取、数据集、模型、视频默认不进 git。
3. 重要实验目录需要有 `README.md` 或 `summary.json`。
4. 新增主要区域时更新 `docs/project_index.md` 和 `docs/project_index_zh.md`。
""",
    )

    write(
        "docs/code_organization_zh.md",
        """
# 代码组织说明

主 Python 包位于：

```text
safe_moe_locomotion/
```

早期曾保留 `02_Code/` 以模仿 3YP 的编号目录结构。现在该目录已合并到标准 Python 项目布局中，新的可复用代码不应再放到零散目录里。

建议：

- 可复用模块放 `safe_moe_locomotion/`。
- 可执行入口和维护脚本放 `scripts/`。
- 配置放 `configs/`。
- 实验结果放 `experiments/`。
- 临时分析放 `notebooks/`，但不要把 notebook 当成唯一实现。
""",
    )

    write(
        "docs/future_work/claim_boundary_zh.md",
        """
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
""",
    )

    write(
        "docs/setup/ENVIRONMENT_zh.md",
        """
# 环境部署指南

最后更新：2026-06-15。

本指南采用保守安装策略：先安装本项目轻量依赖，再分别安装 Isaac Lab、legacy Isaac Gym / legged_gym、Unitree RL Gym 等大型机器人框架。

## 0. 当前机器环境

```text
Python: 3.13.5
NVIDIA driver: 580.159.03
CUDA shown by nvidia-smi: 13.0
GPU: NVIDIA GeForce RTX 5090, 32607 MiB VRAM
```

系统 Python 太新，不适合直接跑 Isaac Lab / Isaac Gym。请使用 conda 或 mamba。

## 1. 本项目轻量环境

```bash
conda env create -f environment.yml
conda activate 2rl
pip install -r requirements-dev.txt
pip install -e .
python scripts/validate_project.py
sh scripts/run_tests.sh
```

这一步只验证仓库结构和轻量 Python 模块，不会安装 Isaac Lab，也不会训练策略。

## 2. PyTorch

使用官方 selector 安装：

https://pytorch.org/get-started/locally/

不要随意安装和 Python / CUDA / Isaac 版本不匹配的 wheel。Isaac Lab 如果指定 PyTorch 版本，应以 Isaac Lab 文档为准。

## 3. 推荐现代路线：Isaac Lab

官方资料：

- https://isaac-sim.github.io/IsaacLab/main/source/setup/installation/index.html
- https://github.com/isaac-sim/IsaacLab

建议克隆位置：

```bash
mkdir -p external
git clone https://github.com/isaac-sim/IsaacLab external/IsaacLab
cd external/IsaacLab
# 然后按官方 Isaac Lab 文档继续
```

记录 commit：

```bash
cd /home/tomato/2RL
git -C external/IsaacLab rev-parse HEAD >> docs/references/external_commits.txt
```

## 4. Legacy 复现路线：Isaac Gym + legged_gym

如果要复现经典 `Learning to Walk in Minutes` / legged_gym baseline，建议单独建 Python 3.8 环境：

```bash
conda create -n 2rl-legacy-gym python=3.8
conda activate 2rl-legacy-gym
```

然后按 `legged_gym` 当前 README 安装 Isaac Gym Preview 和依赖。不要把 legacy Isaac Gym 环境和现代 Isaac Lab 环境混在一起。

## 5. rsl_rl

普通安装：

```bash
pip install rsl-rl-lib
```

开发安装：

```bash
git clone https://github.com/leggedrobotics/rsl_rl external/rsl_rl
pip install -e external/rsl_rl
```

## 6. Unitree RL Gym

```bash
git clone https://github.com/unitreerobotics/unitree_rl_gym external/unitree_rl_gym
```

适合后续迁移到 Unitree Go2 / G1 / H1 等机器人时参考。

## 7. Humanoid-Gym

官方项目：

- https://arxiv.org/abs/2404.05695
- https://github.com/roboterax/humanoid-gym

这是后期做人形机器人时的参考，不是第一阶段四足 baseline 的阻塞项。

## 8. MuJoCo

```bash
pip install mujoco
```

用于后续 sim-to-sim 验证，不作为第一训练后端。

## 9. 验证命令

```bash
python --version
python -c "import numpy, yaml; print('core ok')"
python -m compileall safe_moe_locomotion
python scripts/validate_project.py
sh scripts/run_tests.sh
nvidia-smi
```

注意：本机普通 `python -m pytest` 可能自动加载 ROS 2 pytest 插件。请使用 `scripts/run_tests.sh`。
""",
    )

    write(
        "docs/setup/PACKAGE_INVENTORY_zh.md",
        """
# 依赖包与框架清单

最后更新：2026-06-15。

本文档区分“本项目轻量依赖”和“大型机器人仿真框架”。

## 系统级依赖

| 工具 | 是否必需 | 用途 |
|---|---:|---|
| Git | 是 | 源码管理、记录外部 repo commit |
| Conda / Mamba | 是 | 创建独立 Python 环境 |
| NVIDIA Driver | GPU 训练必需 | GPU 仿真与 PyTorch |
| CUDA Toolkit / runtime | GPU 训练必需 | 与 PyTorch / Isaac 环境匹配 |
| Linux shell tools | 是 | 运行脚本和维护命令 |

## 本项目轻量依赖

| 包 | 用途 |
|---|---|
| Python 3.11 | 现代 Isaac Lab 路线推荐环境 |
| NumPy | 数组、metrics、辅助验证 |
| PyYAML | YAML 配置读取 |
| Matplotlib | reward curve 和 ablation plot |
| tqdm | 进度条 |
| TensorBoard | 训练曲线 |
| Gymnasium | 简单环境接口兼容 |
| pytest | 测试 |
| ruff | lint |
| mypy | 可选类型检查 |

## 机器人与 RL 框架

| 框架 | 优先级 | 用途 | 建议位置 |
|---|---:|---|---|
| Isaac Lab / Isaac Sim | 1 | 现代主训练路线 | `external/IsaacLab` |
| rsl_rl | 1 | PPO / robotics RL | PyPI 或 `external/rsl_rl` |
| legged_gym | legacy 1 | 经典 ANYmal baseline 复现 | `external/legged_gym` |
| Isaac Gym Preview | legacy 1 | old legged_gym 依赖 | NVIDIA 下载，不进仓库 |
| Unitree RL Gym | 2 | Go2 / G1 / H1 参考 | `external/unitree_rl_gym` |
| MuJoCo | 2 | sim-to-sim 验证 | pip |
| ROS 2 | 3 | 后期真实机器人集成 | 系统安装 |
| Pinocchio | 3 | 刚体动力学分析 | conda/pip/system |
| Humanoid-Gym | 3 | 人形机器人扩展 | `external/humanoid-gym` |

## 当前机器信息

```text
Python: 3.13.5
NVIDIA driver: 580.159.03
CUDA shown by nvidia-smi: 13.0
GPU: NVIDIA GeForce RTX 5090, 32607 MiB VRAM
```

结论：不要直接用系统 Python 跑 Isaac；现代 Isaac Lab 建 Python 3.11 环境，legacy legged_gym 建 Python 3.8 环境。
""",
    )

    write(
        "docs/references/README_zh.md",
        """
# 引用资料与 Attribution

该目录用于把外部论文、外部仓库和引用信息与本项目自写代码分开。

## 文件说明

- `paper_index.md` / `paper_index_zh.md`：论文清单。
- `reading_queue.md` / `reading_queue_zh.md`：推荐阅读顺序。
- `recommended_reading_order_zh.md`：覆盖 26 篇论文的详细中文阅读顺序。
- `external_repos.md` / `external_repos_zh.md`：外部代码仓库、用途和建议克隆位置。
- `papers/`：已下载的 arXiv PDF 和 `papers_manifest.csv`。

## 规则

1. 记录论文标题、链接、用途和阅读优先级。
2. PDF 默认不进 git，只保留 manifest 和笔记。
3. 外部代码放 `external/` 或作为 submodule，不复制进主包。
4. 改写第三方代码前先确认 license。
""",
    )

    write(
        "docs/references/external_repos_zh.md",
        """
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
""",
    )

    write(
        "docs/references/reading_queue_zh.md",
        """
# 推荐阅读顺序

## 第一批：马上服务 baseline 复现

1. Learning to Walk in Minutes Using Massively Parallel Deep Reinforcement Learning
2. RMA: Rapid Motor Adaptation for Legged Robots
3. Learning Quadrupedal Locomotion over Challenging Terrain
4. Sim-to-Real: Learning Agile Locomotion For Quadruped Robots
5. Learning agile and dynamic motor skills for legged robots
6. Agile But Safe
7. MoE-Loco

## 第二批：导航、Parkour、风险地形

8. Advanced Skills by Learning Locomotion and Local Navigation End-to-End
9. Robot Parkour Learning
10. Extreme Parkour with Legged Robots
11. Learning Agile Locomotion on Risky Terrains
12. Resilient Legged Local Navigation

## 第三批：MoE 改进

13. MoRE
14. CMoE
15. Parkour in the Wild
16. Reliable Sim-to-Real Predictability for MoE-based Robust Quadrupedal Locomotion
17. Quadruped Parkour Learning: Sparsely Gated Mixture of Experts with Visual Input

## 第四批：人形机器人扩展

18. Real-World Humanoid Locomotion with Reinforcement Learning
19. Humanoid-Gym
20. H2O
21. OmniH2O
22. WoCoCo
23. BeamDojo

## 第五批：VLA 拓展阅读

24. Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware
25. Diffusion Policy: Visuomotor Policy Learning via Action Diffusion
26. pi0: A Vision-Language-Action Flow Model for General Robot Control

建议：不要等所有论文都读完再动手。读完 1、2、3 后就可以同步准备 baseline 复现环境；VLA 三篇作为拓展，不阻塞 2RL 主线复现。
""",
    )

    write(
        "docs/references/paper_index_zh.md",
        """
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

## VLA、动作序列建模与 Diffusion Policy

| 论文 | 用途 |
|---|---|
| Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware | ACT / action chunking，理解机器人动作序列模仿学习。 |
| Diffusion Policy: Visuomotor Policy Learning via Action Diffusion | 用 diffusion 生成连续动作序列，理解现代 visuomotor policy。 |
| pi0: A Vision-Language-Action Flow Model for General Robot Control | VLM + flow matching 的通用 VLA robot policy。 |

## 本地资料入口

- PDF manifest: `docs/references/papers/papers_manifest.csv`
- 单篇中文笔记: `docs/paper_notes/individual/README_zh.md`
- 整合中文综述: `docs/paper_notes/integrated_literature_review_zh.md`
""",
    )

    write(
        "docs/paper_notes/README_zh.md",
        """
# 论文笔记

## 已生成内容

- [单篇论文中文笔记](individual/README_zh.md)
- [所有论文整合综述](integrated_literature_review_zh.md)
- [PDF 提取文本 manifest](extracted_text/text_manifest.csv)
- [PDF 下载 manifest](../references/papers/papers_manifest.csv)

## 建议阅读方式

1. 先读 `integrated_literature_review_zh.md`，理解整体路线。
2. 再读前 5 篇单篇笔记：baseline、RMA、复杂地形、Agile But Safe、MoE-Loco。
3. 每读一篇论文，把 observation、action、reward、simulator、evaluation metrics 记录到自己的实验计划里。
4. 不要等 26 篇全部读完再开始环境复现。
""",
    )

    write(
        "docs/paper_notes/integrated_literature_review_zh.md",
        """
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
""",
    )

    write(
        "experiments/README_zh.md",
        """
# 实验输出规范

每个实验都应该有独立目录，并保存足够信息以便之后复现。

推荐结构：

```text
experiments/<YYYY-MM-DD>_<short_name>/
├── config.yaml
├── command.txt
├── git_state.txt
├── summary.json
├── metrics.json
├── plots/
├── videos/
└── checkpoints/
```

## `summary.json` 必填字段

- `method`
- `robot`
- `terrain`
- `seed`
- `train_steps` 或 `iterations`
- `success_rate`
- `fall_rate`
- `collision_rate`
- `tracking_error`
- `energy`
- MoE 实验需要 `expert_utilization`
- MoE 实验需要 `gate_entropy`
- `notes`

## 实验组

- `baseline_locomotion`
- `experts_flat_rough_stairs_gap_recovery`
- `vanilla_moe`
- `terrain_conditioned_moe`
- `safety_moe`
- `contrastive_moe`
- `residual_moe`
- `ablation`
- `sim2real`

大 checkpoint 和视频默认不要提交到 git，只提交轻量配置、summary、曲线和说明。
""",
    )

    write(
        "docs/superpowers/plans/2026-06-15-restructure-project-layout_zh.md",
        """
# 项目结构重构执行计划

## 目标

把仓库从 3YP 编号目录与 Python 项目目录混合的结构，整理为更紧凑的科研 Python 项目结构。

## 目标结构

```text
configs/
docs/
experiments/
models/
data/
external/
assets/
notebooks/
scripts/
safe_moe_locomotion/
tests/
```

## 已执行任务

1. 先修改测试，让测试期望新路径，并确认测试失败。
2. 移动目录：
   - `07_References/` -> `docs/references/`
   - `03_Experiments/` -> `experiments/`
   - `04_Trained_Models/` -> `models/`
   - `06_Data/` -> `data/`
   - `08_External/` -> `external/`
   - `05_Documentation/PROJECT_INDEX.md` -> `docs/project_index.md`
   - `02_Code/README.md` -> `docs/code_organization.md`
3. 更新 README、脚本、配置、测试和文档中的旧路径。
4. 重新生成论文笔记和 manifest。
5. 跑验证命令。

## 验证命令

```bash
python3 scripts/validate_project.py
sh scripts/run_tests.sh
python3 -m compileall scripts safe_moe_locomotion tests
python3 -m safe_moe_locomotion.training.run_experiment --config configs/train/ppo_gate.yaml --dry-run
```
""",
    )

    generate_individual_notes()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
