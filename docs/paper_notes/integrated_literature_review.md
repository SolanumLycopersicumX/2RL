# Integrated Literature Review

## Scope

This synthesis covers the 28 papers downloaded under `docs/references/papers/`.
The goal is not to summarize every result equally, but to convert the literature
into a concrete development path for **Safety-Aware MoE-Gated Locomotion for
Legged Local Navigation**.

## 1. Baseline Comes Before MoE

The first cluster of papers shows a clear lesson: start with a stable
command-conditioned locomotion policy before adding routing, perception, or
safety. `Learning to Walk in Minutes` provides the practical baseline: GPU
parallel simulation, PPO, joint-position target offsets, PD control, reward
terms for velocity tracking and stability, and curriculum/randomization. The
sim-to-real and agile locomotion papers add that actuator modeling, latency,
friction, mass variation, and action smoothness must be part of the training
contract, not afterthoughts.

For 2RL, this means Milestone 1 should produce:

- one flat-terrain velocity tracking policy;
- one rough-terrain policy with randomization;
- saved reward curves, fall rate, command tracking error, and rollout videos;
- a documented observation/action/reward contract.

MoE should not start until these baselines are reproducible.

## 2. Robustness Is Mostly Hidden-State Estimation

RMA and the challenging-terrain papers frame robustness as inference over hidden
environment state. The robot cannot directly observe friction, payload, terrain
compliance, actuator mismatch, or sensor delay. A history encoder can infer some
of these variables from recent proprioception and action-response mismatch.

For 2RL, this suggests the gate input should include:

- proprioception history embedding;
- previous action and action-rate features;
- command tracking error history;
- terrain embedding if available;
- previous gate weights for temporal smoothing.

The same logic applies to the risk estimator: risk should be predicted from
state history and terrain context, not just current roll/pitch.

## 3. Terrain Difficulty Changes The Objective

Rough terrain, stairs, gaps, sparse footholds, and parkour are not just harder
versions of flat locomotion. They require different success definitions. For
flat terrain, speed and tracking error matter. For risky terrain, fall rate,
foot placement safety, collision rate, recovery success, and goal completion are
more important.

This motivates the planned expert split:

- flat expert: efficient command tracking;
- rough expert: robust terrain adaptation;
- stair expert: vertical stepping and body clearance;
- gap expert: sparse foothold and contact precision;
- recovery expert: high-risk state stabilization.

The evaluation must report per-terrain metrics. A single mixed-terrain average
can hide expert failure.

## 4. Perception Should Be Added Gradually

Parkour and local-navigation papers show why perception matters: the robot must
anticipate stairs, gaps, crawl spaces, and obstacles before contact. However,
the resilient-navigation papers also show that perception can fail through
noise, missing depth, latency, or occlusion.

The development order should be:

1. privileged terrain label for MoE sanity checks;
2. height samples for deployable terrain cues;
3. local height map encoder;
4. depth image encoder only after earlier stages are stable.

Every perception-based result should include a degraded-perception evaluation.

## 5. Safety Needs Explicit Routing

`Agile But Safe` is the most direct reference for the safety-aware part of 2RL.
Reward penalties alone do not guarantee that a high-speed or high-reward policy
will switch to conservative behavior at the right time. A separate risk
estimator or safety supervisor gives the policy a mechanism to bias or force
recovery behavior.

The first 2RL safety implementation should be simple:

- train or label risk from future fall/collision within N steps;
- output a scalar risk score;
- add recovery-expert bias when risk is high;
- optionally use hard override above a threshold;
- add hysteresis or temporal smoothing to avoid gate chatter.

The ablation should compare vanilla MoE and safety-aware MoE on fall rate,
collision rate, recovery trigger frequency, and OOD terrain performance.

## 6. MoE Helps, But Routing Can Fail

MoE-Loco motivates expert specialization for multitask locomotion. CMoE and
MoRE describe two important failure modes:

- gate collapse or uniform routing, where experts do not specialize;
- unsafe action mixing, where complete expert actions are blended despite
  incompatible gait phase or control style.

For 2RL, the safe progression is:

1. frozen experts + rule switch baseline;
2. frozen experts + vanilla soft gate;
3. hard or top-k gate if soft mixture is unstable;
4. residual expert MoE if action mixture causes unnatural motion;
5. contrastive routing if gate activation is not terrain-specific;
6. joint fine-tuning only after routing diagnostics are reliable.

Key diagnostics:

- expert utilization;
- gate entropy;
- switching frequency;
- activation by terrain;
- per-expert failure cases;
- action-rate and torque smoothness.

## 7. Humanoid Papers Are A Later Extension

The humanoid papers are valuable but should not define the first implementation
target. They add smaller support polygons, whole-body balance, upper-body
coupling, contact sequences, and motion imitation. Humanoid-Gym, BeamDojo,
H2O, OmniH2O, WoCoCo, and real-world humanoid locomotion papers should guide a
second phase after quadruped MoE works.

For now, keep humanoid support as config/interface readiness:

- `configs/robot/unitree_g1.yaml`;
- residual expert policy;
- later Humanoid-Gym external path;
- claim boundary that humanoid results are future work.

## 8. VLA And Diffusion Papers Broaden The Action-Generation View

DDPM, DDIM, ACT, Diffusion Policy, and pi0 extend the reading set beyond
locomotion into diffusion foundations, vision-language-action, and visuomotor
manipulation. Their direct training pipelines are not the first 2RL
implementation target, but they are useful for understanding how modern robot
policies generate action sequences instead of single-step commands.

The useful progression is:

1. DDPM: denoising objective and Markov-chain diffusion foundation;
2. DDIM: fast deterministic or low-stochasticity diffusion sampling;
3. ACT: transformer-based action chunking for imitation learning;
4. Diffusion Policy: conditional diffusion over continuous action sequences;
5. pi0: VLM-conditioned flow matching for general robot control.

For 2RL, the near-term takeaway is architectural rather than implementation
heavy: a high-level language or vision-conditioned policy can eventually
produce goals, skills, or short action horizons, while the safety-aware
locomotion controller remains the low-level execution layer.

## Recommended Reading Order

1. `2109.11978` Learning to Walk in Minutes.
2. `2107.04034` RMA.
3. `2010.11251` Challenging Terrain.
4. `2401.17583` Agile But Safe.
5. `2503.08564` MoE-Loco.
6. `2506.08840` MoRE.
7. `2603.03067` CMoE.
8. Parkour and risky-terrain papers.
9. Humanoid papers.
10. VLA/diffusion expansion: DDPM, DDIM, ACT, Diffusion Policy, pi0.

## Direct Implementation Plan Derived From The Literature

### Stage A: Reproducible Baseline

- Install Isaac Lab or legacy legged_gym.
- Train flat and rough quadruped PPO policies.
- Record observation/action/reward.
- Save curves, videos, and metrics.

### Stage B: Expert Library

- Train flat, rough, stair, gap, and recovery experts.
- Standardize expert observation/action dimensions.
- Evaluate each expert on both in-domain and mixed terrain.

### Stage C: Routing

- Implement rule switch as a non-learned baseline.
- Train vanilla gate over frozen experts.
- Plot utilization, entropy, and switching frequency.

### Stage D: Safety

- Build risk labels from future fall/collision.
- Train risk estimator.
- Bias or override routing to recovery expert.
- Compare against vanilla MoE.

### Stage E: Specialization

- Add terrain encoder.
- Add load balancing and temporal smoothness.
- Add contrastive routing only after baseline gate is diagnosable.
- Try residual experts if action mixture is unstable.

### Stage F: Optional VLA Expansion

- Read DDPM to understand the denoising training objective.
- Read DDIM to understand fast sampling and latency trade-offs.
- Read ACT to understand action chunking.
- Read Diffusion Policy to understand generative continuous action heads.
- Read pi0 to connect VLM conditioning, flow matching, and robot foundation
  policies.
- Keep VLA experiments separate from the first locomotion MoE milestone.

## Claim Boundary

After reading and note generation, 2RL can claim it has a literature-backed
development roadmap and local paper archive. It still cannot claim trained
policies, safety improvement, or sim-to-real reliability until actual
experiments under `experiments/` support those claims.
