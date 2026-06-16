# Experiment Output Rules

Each experiment must live in its own folder and preserve enough metadata to be
reproduced later.

Recommended layout:

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

## Required Fields in `summary.json`

- `method`
- `robot`
- `terrain`
- `seed`
- `train_steps` or `iterations`
- `success_rate`
- `fall_rate`
- `collision_rate`
- `tracking_error`
- `energy`
- `expert_utilization` when using MoE
- `gate_entropy` when using MoE
- `notes`

## Canonical Experiment Groups

- `baseline_locomotion`
- `experts_flat_rough_stairs_gap_recovery`
- `vanilla_moe`
- `terrain_conditioned_moe`
- `safety_moe`
- `contrastive_moe`
- `residual_moe`
- `ablation`
- `sim2real`

Large checkpoints and videos should stay local or be released separately.
Commit lightweight configs, summaries, logs, and plots.
