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
