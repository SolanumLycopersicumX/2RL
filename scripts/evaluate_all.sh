#!/usr/bin/env bash
set -euo pipefail
python - <<'PY'
from safe_moe_locomotion.evaluation.ablation import ABLATION_GROUPS
from safe_moe_locomotion.evaluation.terrain_sweep import TERRAIN_SWEEP

print("Ablation groups:")
for key, value in ABLATION_GROUPS.items():
    print(f"{key}: {value}")

print("\nTerrain sweep:")
for terrain in TERRAIN_SWEEP:
    print(f"- {terrain}")
PY

