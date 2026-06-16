#!/usr/bin/env bash
set -euo pipefail

# The shared machine has ROS 2 pytest plugins on PYTHONPATH. Disable automatic
# third-party plugin loading so project tests do not fail due to unrelated
# system packages.
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests "$@"

