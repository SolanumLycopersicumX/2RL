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
