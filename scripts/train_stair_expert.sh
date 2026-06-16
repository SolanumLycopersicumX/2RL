#!/usr/bin/env bash
set -euo pipefail
python -m safe_moe_locomotion.training.run_experiment --config configs/train/ppo_stair.yaml "$@"

