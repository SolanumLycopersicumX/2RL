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
