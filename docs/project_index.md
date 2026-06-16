# Project Index

Chinese version: `docs/project_index_zh.md`

This file is the human navigation layer for the project. It follows the same
purpose as `/home/tomato/3YP/05_Documentation/PROJECT_INDEX.md`: make the
repository understandable without reading every file.

## Main Entry Points

- `README.md`: project overview and quick start.
- `rl_locomotion_moe_research_plan.md`: original long-form research plan.
- `Codex_Log.md`: persistent task and progress log.
- `docs/setup/ENVIRONMENT.md`: environment deployment guide.
- `docs/setup/PACKAGE_INVENTORY.md`: package and framework inventory.
- `docs/project_structure.md`: folder organization and maintenance rules.
- `docs/references/paper_index.md`: papers mentioned in the plan.
- `docs/paper_notes/`: individual and integrated literature notes.
- `experiments/README.md`: experiment output rules.

## Code

- `safe_moe_locomotion/envs/`: environment adapters and observation contracts.
- `safe_moe_locomotion/policies/`: expert, MoE, safety-aware, residual policies.
- `safe_moe_locomotion/modules/`: encoders, gating network, risk estimator,
  safety supervisor.
- `safe_moe_locomotion/rewards/`: locomotion, navigation, recovery, and MoE
  regularization terms.
- `safe_moe_locomotion/training/`: trainer entrypoints and framework adapters.
- `safe_moe_locomotion/evaluation/`: rollout, metrics, terrain sweep, ablation.
- `safe_moe_locomotion/utils/`: config, logging, checkpoint, video helpers.

## Configs

- `configs/robot/`: robot-specific dimensions, PD defaults, action scale.
- `configs/terrain/`: flat, rough, stair, gap, mixed terrain templates.
- `configs/train/`: PPO and experiment templates.
- `configs/moe/`: vanilla, safety-aware, contrastive MoE settings.

## External Material

- `docs/references/`: citations, paper reading order, external repo links.
- `external/`: optional local clones of Isaac Lab, legged_gym, Unitree RL Gym,
  or other third-party repositories. This directory is ignored by git.

## Maintenance Rules

1. Put reusable code in `safe_moe_locomotion/`, not in notebooks.
2. Put experiment outputs under `experiments/` with a `summary.json`.
3. Put large checkpoints under `models/` or external storage.
4. Record external repo URLs and commit hashes in `docs/references/`.
5. Update `Codex_Log.md` after each major automation step.
