# Environment Deployment Guide

中文版本：[ENVIRONMENT_zh.md](ENVIRONMENT_zh.md)

Last updated: 2026-06-15.

This guide is intentionally conservative. It installs the local project first,
then adds heavy robotics frameworks in separate steps so failures are easier to
debug.

## 0. Machine Context

Current machine check:

```text
Python: 3.13.5
NVIDIA driver: 580.159.03
CUDA shown by nvidia-smi: 13.0
GPU: NVIDIA GeForce RTX 5090, 32607 MiB VRAM
```

The system Python is too new for most robotics stacks. Use conda/mamba.

## 1. Local Project Environment

```bash
conda env create -f environment.yml
conda activate 2rl
pip install -r requirements-dev.txt
pip install -e .
python scripts/validate_project.py
```

This verifies the repository structure and lightweight Python files. It does
not install Isaac Lab or train policies.

## 2. PyTorch

Install PyTorch inside the active conda environment using the official selector:

https://pytorch.org/get-started/locally/

Do not blindly install a CUDA wheel that does not match the available Python,
driver, and framework constraints. For Isaac Lab, follow Isaac Lab's PyTorch
guidance if it pins a specific build.

## 3. Modern Path: Isaac Lab

Use this path for new work.

Official docs:

- https://isaac-sim.github.io/IsaacLab/main/source/setup/installation/index.html
- https://github.com/isaac-sim/IsaacLab

Key compatibility notes from the official docs:

- Isaac Lab is built on Isaac Sim.
- Isaac Sim 5.x requires Python 3.11.
- Isaac Sim 4.x requires Python 3.10.
- Ubuntu 22.04 and 32 GB RAM / 16 GB VRAM are baseline requirements in the
  official local-install guide.

Recommended local clone location:

```bash
mkdir -p external
git clone https://github.com/isaac-sim/IsaacLab external/IsaacLab
cd external/IsaacLab
# Follow the current official Isaac Lab installation guide from here.
```

After installing, return to this repository root and record the commit:

```bash
cd /home/tomato/2RL
git -C external/IsaacLab rev-parse HEAD >> docs/references/external_commits.txt
```

## 4. Legacy Reproduction Path: Isaac Gym + legged_gym

Use this path to reproduce the classic "Learning to Walk in Minutes" baseline.

Official repositories:

- https://github.com/leggedrobotics/legged_gym
- https://github.com/leggedrobotics/rsl_rl

The legacy legged_gym README recommends Python 3.8 and old PyTorch/CUDA builds.
Do not mix this with the modern Isaac Lab environment.

Suggested separate environment:

```bash
conda create -n 2rl-legacy-gym python=3.8
conda activate 2rl-legacy-gym
```

Then follow the current `legged_gym` README and install Isaac Gym Preview from
NVIDIA. Isaac Gym is not vendored in this repository.

## 5. rsl_rl

Official repo:

https://github.com/leggedrobotics/rsl_rl

Normal install:

```bash
pip install rsl-rl-lib
```

Development install:

```bash
git clone https://github.com/leggedrobotics/rsl_rl external/rsl_rl
pip install -e external/rsl_rl
```

## 6. Unitree RL Gym

Official repo:

https://github.com/unitreerobotics/unitree_rl_gym

Use this after the ANYmal/legged_gym baseline if you want Go2, G1, H1, or H1_2
reproduction paths.

```bash
git clone https://github.com/unitreerobotics/unitree_rl_gym external/unitree_rl_gym
```

Follow its `doc/setup_en.md`. Record commit hash before running experiments.

## 7. Humanoid-Gym

Official project/repo:

- https://arxiv.org/abs/2404.05695
- https://github.com/roboterax/humanoid-gym

Use this only after the quadruped baseline and MoE routing path are stable.
Humanoid-Gym is useful for studying humanoid zero-shot sim-to-real and
Isaac-Gym-to-MuJoCo sim-to-sim verification, but it is not the first target for
this repository.

## 8. MuJoCo

Official Python docs:

https://mujoco.readthedocs.io/en/stable/python.html

Install:

```bash
pip install mujoco
```

Use MuJoCo for sim-to-sim verification, not as the first training backend.

## 9. Optional Later Dependencies

ROS 2:

- Use for physical robot integration only after simulation results are stable.
- Install from the official ROS 2 docs for the target Ubuntu distribution.

Pinocchio:

- Use for rigid-body dynamics analysis and later whole-body control tooling.

RBDL:

- Optional alternative dynamics library.

## 10. Sanity Commands

```bash
python --version
python -c "import numpy, yaml; print('core ok')"
python -m compileall safe_moe_locomotion
python scripts/validate_project.py
sh scripts/run_tests.sh
nvidia-smi
```

On this shared machine, plain `python -m pytest` may auto-load ROS 2 pytest
plugins from `/opt/ros/jazzy`. Use `scripts/run_tests.sh`, which disables
external pytest plugin autoloading for this project.

## 11. Reproducibility Rules

For every real training run, save:

- command,
- config,
- framework repo commits,
- `pip freeze`,
- GPU and driver info,
- seed,
- metrics,
- checkpoint path,
- video path if generated.
