# 2RL VLA-First SO-101 Design

Date: 2026-06-19

## Status

Approved design direction for the next 2RL phase. This document defines the
project pivot before implementation planning. It does not change code behavior.

## Project Positioning

2RL will pivot from a reinforcement-learning locomotion workspace into a
VLA-first robot learning project centered on the SO-101 arm with a wrist camera.

The first project identity is:

> VLA-guided SO-101 point-and-touch robot learning, with RL plugins for later
> improvement, safety correction, and failure recovery.

The first demo task is language-conditioned pointing or touching:

```text
wrist camera image + language instruction + robot state
        -> imitation-learned VLA policy
        -> SO-101 arm action
        -> point to or touch the target object
```

The old legged locomotion and MoE work remains useful as background, but it is
no longer the main project surface. It becomes a historical research line or a
future plugin reference rather than the first implementation target.

## Core Decisions

- Hardware target: two SO-101 arms in a leader-follower teleoperation setup.
- Sensor target: wrist camera on the follower arm.
- First task family: point to or touch a language-specified tabletop object.
- First object setup: closed object set, then open-vocabulary extension.
- First learning method: imitation learning from demonstrations.
- First action interface: SO-101 joint-space actions or joint targets.
- First algorithm baseline: ACT-style action chunking through LeRobot.
- RL role: later plugin, not first-version action execution.

## Why VLA First

For internship positioning, a VLA-first SO-101 project is easier to explain as a
modern robot learning system than another small RL locomotion reproduction. It
connects directly to vision-language-action policies, low-cost robot data
collection, action sequence modeling, and embodied AI evaluation.

RL still matters, but it should not define the first demo. In this design, RL is
reserved for:

- policy improvement after a supervised imitation baseline exists;
- local recovery from stuck, off-target, or near-limit states;
- safety correction when the policy risks collision or joint-limit violation;
- later fine-tuning of specific subskills such as final contact.

## Focused SOTA Method Scan

The experiment design should follow a focused method scan rather than treating
"VLA" as a broad label. The relevant method families are:

| Method family | Role in 2RL | Reason |
|---|---|---|
| ACT / Action Chunking Transformer | First baseline | Designed for teleoperated robot demonstrations and action chunks; fits SO-101 data collection well. |
| LeRobot | First engineering stack | Provides SO-101 setup, recording, dataset handling, training, and policy evaluation patterns. |
| Diffusion Policy | Second baseline | Strong for multimodal continuous actions, but more complex than ACT for the first pass. |
| SmolVLA | Near-term VLA extension | Lightweight vision-language-action policy line suitable after the ACT pipeline works. |
| OpenVLA / Octo / pi0 | Positioning and later extension | Useful to frame the project against generalist robot policies; too large for first reproduction. |
| RT-1 / RT-2 / Open X-Embodiment | Background | Useful for understanding large-scale language-conditioned robot data and evaluation, not the first implementation target. |

Primary references:

- ACT: https://arxiv.org/abs/2304.13705
- Diffusion Policy: https://arxiv.org/abs/2303.04137
- LeRobot: https://huggingface.co/docs/lerobot/en/index
- LeRobot ACT: https://huggingface.co/docs/lerobot/en/act
- SO-101 setup: https://huggingface.co/docs/lerobot/so101
- SmolVLA: https://huggingface.co/docs/lerobot/en/smolvla
- OpenVLA: https://arxiv.org/abs/2406.09246
- Octo: https://arxiv.org/abs/2405.12213
- pi0: https://arxiv.org/abs/2410.24164
- RT-1: https://arxiv.org/abs/2212.06817
- RT-2: https://arxiv.org/abs/2307.15818
- Open X-Embodiment: https://arxiv.org/abs/2310.08864

## First Demo Scope

The first real demo should stay narrow:

- 3 to 5 tabletop objects.
- Simple instructions such as `touch the red cube`, `point to the blue cup`,
  and `touch the object on the left`.
- One wrist camera view.
- One follower SO-101 arm executing actions.
- Demonstrations collected through a leader SO-101.
- Success judged by correct target contact or stable pointing near the target.

Open-vocabulary instructions, relational instructions, external cameras,
multi-step manipulation, grasping, and RL fine-tuning are later phases.

## Architecture

### Data Collection

Leader-follower teleoperation collects demonstrations. Each episode records:

- language instruction;
- wrist camera frames;
- follower joint positions;
- follower actions or target joint positions;
- timestamps;
- object set metadata;
- success or failure label after rollout.

### Dataset Layer

Data is stored as episodes. The first schema is:

```text
episode_id
task_instruction
object_set
success
frames:
  - timestamp
    wrist_image
    joint_positions
    action
```

Optional later annotations include target object bounding boxes, end-effector
pose, failure reason, contact signal, and human correction notes.

### VLA Policy

The first policy consumes wrist image, instruction, and robot state, then
predicts an action chunk or next joint target:

```text
image_t, instruction, q_t -> action_chunk_t
```

ACT is the first baseline because action chunking reduces single-step
behavior-cloning drift and matches teleoperation trajectories. Diffusion Policy
is the second comparison after data collection and evaluation are stable.

### Evaluation

The first evaluation suite reports:

- target success rate;
- wrong-object touch rate;
- near-target pointing rate;
- timeout or stuck rate;
- collision or joint-limit event rate;
- average rollout length;
- qualitative wrist-camera videos.

Evaluation should separate seen-object/seen-layout episodes from held-out
layouts. Open-vocabulary evaluation waits until the closed-set baseline works.

### RL Plugin Layer

RL is not used as the first action executor. It is a later plugin layer with
three planned entry points:

1. Recovery policy: escape stuck or failed states.
2. Safety correction: constrain or override risky action chunks.
3. Fine-tuning: optimize success rate or final-contact behavior after an
   imitation policy exists.

This keeps the project VLA-first while preserving a credible RL extension.

## Milestones

### Phase 0: Pre-Hardware

- Finalize this design and implementation plan.
- Update README and reading roadmap to reflect the VLA-first pivot.
- Add a focused paper/method index for ACT, LeRobot, Diffusion Policy, SmolVLA,
  OpenVLA, Octo, pi0, RT-1, RT-2, and Open X-Embodiment.
- Define the episode schema and experiment record format.
- Build a mock dataset/training check only after the design is accepted.

### Phase 1: Hardware Bring-Up

- Assemble two SO-101 arms.
- Configure leader-follower teleoperation.
- Mount and test the wrist camera.
- Record small sanity-check episodes.
- Verify synchronization among images, joint states, actions, and instructions.

### Phase 2: First Imitation Baseline

- Collect closed-set point/touch demonstrations.
- Train ACT through the LeRobot-style pipeline.
- Evaluate on seen and held-out tabletop layouts.
- Record videos and failure cases.

### Phase 3: VLA Extension

- Add richer language instructions.
- Compare ACT with Diffusion Policy or SmolVLA-style policies.
- Explore open-vocabulary object targeting.

### Phase 4: RL Plugins

- Add recovery, safety correction, or local fine-tuning as plugins.
- Keep RL experiments separate from the first imitation baseline.
- Evaluate whether RL improves success or safety over the supervised policy.

## Out of Scope for the First Version

- Legged locomotion.
- MoE locomotion routing.
- Full pi0 or OpenVLA-scale model training from scratch.
- Grasping and object relocation.
- Multi-camera calibration.
- Real-time RL training on hardware.
- Open-vocabulary target selection before the closed-set baseline works.

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Too little demonstration data | Keep the first task closed-set and short-horizon. |
| Wrist camera view is unstable | Start with simple tabletop layouts and fixed camera mounting. |
| ACT overfits to object positions | Use held-out layouts and randomize object placement during collection. |
| Language is ignored by the policy | Include paired instructions where the same scene has different target objects. |
| RL scope distracts from VLA | Keep RL as a documented plugin phase after imitation evaluation. |
| Hardware is delayed | Use the pre-hardware phase for schema, docs, and mock pipeline only. |

## Acceptance Criteria

The design is accepted when the project can clearly answer:

- What is the first hardware task?
- What data will be recorded?
- Which algorithm is the first baseline?
- How will success be measured?
- Why is RL not the first action executor?
- Which SOTA methods guide the experiment design?

The current answers are: SO-101 point/touch, leader-follower demonstrations,
ACT/LeRobot, target success and failure metrics, VLA-first imitation learning,
and a focused SOTA scan centered on ACT, Diffusion Policy, LeRobot, SmolVLA,
OpenVLA, Octo, pi0, RT-1, RT-2, and Open X-Embodiment.
