#!/usr/bin/env bash
set -euo pipefail

python --version
python -c "import platform; print(platform.platform())"
if command -v nvidia-smi >/dev/null 2>&1; then
  nvidia-smi
else
  echo "nvidia-smi not found"
fi

