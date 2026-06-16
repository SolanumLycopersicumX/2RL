# Safety-Aware MoE-Gated Locomotion for Legged Local Navigation

中文入口：[README_zh.md](README_zh.md)

This repository is a research-style workspace for learning, reproducing, and
extending reinforcement-learning locomotion methods for legged robots.

The target project is:

**Safety-Aware Mixture-of-Experts Locomotion for Legged Local Navigation**

The plan is derived from `rl_locomotion_moe_research_plan.md` and organized
with the maintainable research-project style used in `/home/tomato/3YP`.

## Goals

1. Reproduce a quadruped RL locomotion baseline.
2. Train terrain-specialized experts for flat, rough, stair, gap, and recovery
   behaviors.
3. Implement MoE routing over frozen or fine-tuned experts.
4. Add terrain-conditioned routing and risk-aware recovery switching.
5. Run ablations against single-policy, rule-switch, vanilla MoE, safety MoE,
   contrastive MoE, and residual-expert variants.
6. Produce readable paper notes, experiment logs, plots, videos, and final
   report material.

## Repository Layout

```text
2RL/
├── configs/                # YAML configs for robots, terrains, training, MoE
├── docs/                   # Project index, setup docs, references, paper notes
├── experiments/            # Reproduction outputs and experiment summaries
├── models/                 # Local checkpoints; large files ignored by git
├── data/                   # Local datasets/assets; large files ignored by git
├── external/               # Optional local clones/submodules; ignored by git
├── assets/                 # Figures, GIFs, videos for README/report
├── notebooks/              # Analysis notebooks
├── scripts/                # Reproduction and maintenance entrypoints
├── safe_moe_locomotion/    # Main Python package
└── tests/                  # Lightweight checks
```

See `docs/project_index.md` for a complete navigation guide and
`docs/project_structure.md` for the restructuring rules. Chinese versions are
available at `docs/project_index_zh.md` and `docs/project_structure_zh.md`.

## Quick Start

The system Python in this machine is currently `3.13`, but Isaac Lab/Isaac Sim
workflows should use a dedicated conda environment. Start with:

```bash
conda env create -f environment.yml
conda activate 2rl
pip install -r requirements-dev.txt
python -m compileall safe_moe_locomotion
python scripts/validate_project.py
sh scripts/run_tests.sh
```

For Isaac Lab, legged_gym, rsl_rl, Unitree RL Gym, MuJoCo, and optional ROS 2
installation paths, follow `docs/setup/ENVIRONMENT.md`.

## Reproduction Roadmap

| Stage | Target | Main Files |
|---|---|---|
| 1 | Baseline locomotion | `configs/train/ppo_flat.yaml`, `scripts/train_flat_expert.sh` |
| 2 | Specialized experts | `scripts/train_*_expert.sh`, `configs/terrain/*.yaml` |
| 3 | Vanilla MoE gate | `safe_moe_locomotion/policies/moe_policy.py` |
| 4 | Terrain encoder | `safe_moe_locomotion/modules/terrain_encoder.py` |
| 5 | Safety-aware routing | `safe_moe_locomotion/modules/risk_estimator.py` |
| 6 | Contrastive routing | `safe_moe_locomotion/rewards/moe_regularization.py` |
| 7 | Ablation study | `safe_moe_locomotion/evaluation/ablation.py` |

## External Dependencies

Large robotics frameworks are intentionally not vendored into this repository.
Use `external/` for local clones if needed, and record commit hashes in
`docs/references/external_repos.md`.

Primary frameworks:

- Isaac Lab / Isaac Sim
- rsl_rl
- legged_gym for legacy Isaac Gym reproduction
- Unitree RL Gym for Go2/G1/H1-style reproduction
- MuJoCo for sim-to-sim verification
- ROS 2 for later deployment integration

## Current Status

This repository is at the project bootstrap stage. The paper index, dependency
inventory, environment guide, config templates, Python module skeleton, and
validation scripts are intended to make the first real reproduction stage easy
to start and easy to audit.

Persistent task progress is recorded in `Codex_Log.md`.

## GitHub Remote Note

The target remote is:

```text
https://github.com/SolanumLycopersicumX/2RL.git
```

This workspace currently has a read-only `tmpfs` mounted at `.git`, so standard
`git init` cannot write there. A fallback git directory has been initialized at
`.git-local/` with the remote above. Use:

```bash
sh scripts/git_local.sh status
sh scripts/git_local.sh remote -v
```

After the `.git` mount is removed by an interactive admin shell, run normal
`git init` and add the same remote.
