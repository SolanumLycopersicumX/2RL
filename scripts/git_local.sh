#!/usr/bin/env bash
set -euo pipefail

# The workspace currently has a read-only tmpfs mounted at .git. Until that
# mount is removed, use this helper to operate the fallback git directory.
git --git-dir=.git-local --work-tree=. "$@"
