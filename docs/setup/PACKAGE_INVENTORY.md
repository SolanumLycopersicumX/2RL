# Package Inventory

中文版本：[PACKAGE_INVENTORY_zh.md](PACKAGE_INVENTORY_zh.md)

Last updated: 2026-06-15.

This file separates lightweight project dependencies from large robotics
frameworks. The goal is to keep the repository installable while documenting
the full reproduction environment.

## System-Level Requirements

| Tool | Required | Purpose | Notes |
|---|---:|---|---|
| Git | Yes | source control, external repo commit tracking | GitHub remote target: `https://github.com/SolanumLycopersicumX/2RL.git`. |
| Conda or Mamba | Yes | isolated Python environments | Use Python 3.11 for modern Isaac Lab; Python 3.8 for legacy Isaac Gym reproduction. |
| NVIDIA Driver | Yes for GPU training | GPU simulation and PyTorch training | Local `nvidia-smi` shows driver `580.159.03`. |
| CUDA Toolkit / CUDA runtime | Yes for GPU training | PyTorch and simulator GPU execution | Match PyTorch and simulator guidance; do not mix arbitrary CUDA wheels. |
| Linux shell tools | Yes | scripts and reproducibility commands | `bash`, `sed`, `find`, `nvidia-smi`. |

## Local Core

| Package | Required | Purpose | Install Source |
|---|---:|---|---|
| Python 3.11 | Yes | Isaac Lab / Isaac Sim 5.x-compatible project environment | `environment.yml` |
| NumPy | Yes | arrays, metrics, config validation helpers | `requirements.txt` |
| PyYAML | Yes | YAML config loading | `requirements.txt` |
| Matplotlib | Yes | plots for reward curves and ablations | `requirements.txt` |
| tqdm | Yes | progress bars | `requirements.txt` |
| TensorBoard | Yes | training curves | `requirements.txt` |
| Gymnasium | Recommended | interface compatibility for simple local wrappers | `requirements.txt` |
| pytest | Dev | validation tests | `requirements-dev.txt` |
| ruff | Dev | linting | `requirements-dev.txt` |
| mypy | Dev | optional type checking | `requirements-dev.txt` |

## Deep Learning

| Package | Required | Purpose | Notes |
|---|---:|---|---|
| PyTorch | Yes for training | policy networks and PPO | Install using the official selector for the CUDA/Python combination. |
| torchvision / torchaudio | No | usually unnecessary for proprioceptive locomotion | Install only if perception experiments need them. |
| Weights & Biases | Optional | experiment tracking | Use only if online logging is acceptable. |

## Simulation and RL Frameworks

| Framework | Priority | Purpose | Install Location |
|---|---:|---|---|
| Isaac Lab / Isaac Sim | 1 | primary modern simulator and RL task framework | external install, optionally clone to `external/IsaacLab` |
| rsl_rl | 1 | PPO and robotics RL algorithms | PyPI or `external/rsl_rl` |
| legged_gym | 1 legacy | reproduce classic ANYmal Isaac Gym baseline | `external/legged_gym` |
| Isaac Gym Preview | 1 legacy | required by old legged_gym | NVIDIA download, not committed |
| Unitree RL Gym | 2 | Go2/G1/H1/H1_2 reproduction and deployment examples | `external/unitree_rl_gym` |
| MuJoCo | 2 | sim-to-sim validation | pip package |
| ROS 2 | 3 | later robot integration | system install |
| Pinocchio | 3 | rigid-body dynamics analysis | conda/pip/system package |
| RBDL | 3 | alternative rigid-body dynamics library | system/source package |
| Humanoid-Gym | 3 | humanoid locomotion baseline and sim-to-sim reference | clone under `external/humanoid-gym` after quadruped baseline |

## Machine Check on 2026-06-15

Observed locally:

```text
Python: 3.13.5
NVIDIA driver: 580.159.03
CUDA shown by nvidia-smi: 13.0
GPU: NVIDIA GeForce RTX 5090, 32607 MiB VRAM
```

Implication:

- Do not use the system Python for Isaac Lab work.
- Create a dedicated Python 3.11 environment for modern Isaac Lab.
- If reproducing legacy legged_gym exactly, use a separate Python 3.8
  environment because the legacy README pins old Isaac Gym-era dependencies.
