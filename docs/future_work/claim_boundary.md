# Claim Boundary

This document records what the project can and cannot honestly claim at each
stage.

## Bootstrap Stage

Can claim:

- The repository is organized for a legged-locomotion MoE research project.
- Paper and package indexes identify the intended learning and reproduction
  path.
- Core code modules define interfaces for MoE routing, terrain encoding, risk
  estimation, and evaluation.

Cannot claim yet:

- Any policy has been trained.
- Any Isaac Lab or legged_gym experiment has run.
- Safety-aware MoE improves performance.
- Sim-to-real transfer has been demonstrated.

## Baseline Stage

Add claims only after recording:

- exact framework version and commit,
- training command,
- seed,
- config,
- reward curve,
- rollout video or deterministic evaluation summary.

## Safety-Aware MoE Stage

Do not claim safety improvement from reward alone. Require at least:

- vanilla MoE comparison,
- recovery trigger frequency,
- fall/collision rate,
- failure case analysis,
- OOD terrain or perturbation evaluation.

