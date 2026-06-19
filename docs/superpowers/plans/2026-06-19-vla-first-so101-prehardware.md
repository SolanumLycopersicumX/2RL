# VLA-First SO-101 Pre-Hardware Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prepare 2RL for the VLA-first SO-101 direction before the hardware arrives.

**Architecture:** Keep the existing `safe_moe_locomotion` package intact as the historical RL/MoE line, and add a separate `vla_so101` package for the new SO-101 data and mock pipeline. Documentation becomes VLA-first at the project entry points, while old locomotion material is preserved as background and future plugin reference.

**Tech Stack:** Python 3.10, dataclasses, JSON, pytest, Markdown docs, LeRobot-oriented method references, and the existing local git wrapper `sh scripts/git_local.sh`.

---

## File Structure

- Modify `README.md`: make the repository entry point VLA-first and explain RL plugins.
- Modify `README_zh.md`: mirror the new project identity in Chinese.
- Modify `docs/project_index.md`: update navigation so `vla_so101/` and VLA docs are first-class.
- Modify `docs/project_index_zh.md`: Chinese navigation update.
- Modify `docs/references/paper_index.md`: add a VLA-first method scan section while keeping the old paper index.
- Modify `docs/references/reading_queue.md`: move ACT, LeRobot, Diffusion Policy, and VLA references into the first reading pass.
- Create `docs/references/vla_method_scan.md`: focused algorithm scan for ACT, LeRobot, Diffusion Policy, SmolVLA, OpenVLA, Octo, pi0, RT-1, RT-2, and Open X-Embodiment.
- Create `vla_so101/__init__.py`: package marker and public package description.
- Create `vla_so101/data/__init__.py`: exports SO-101 data helpers.
- Create `vla_so101/data/episode.py`: typed episode schema and JSON round-trip helpers.
- Create `vla_so101/data/mock_dataset.py`: deterministic mock dataset generator for pre-hardware tests.
- Create `vla_so101/training/__init__.py`: training helper package marker.
- Create `vla_so101/training/mock_train.py`: mock training-readiness check that summarizes recorded episodes.
- Create `scripts/create_mock_so101_dataset.py`: command-line entry point for mock dataset generation.
- Create `scripts/run_mock_so101_training.py`: command-line entry point for mock training summary.
- Modify `pyproject.toml`: include `vla_so101*` in package discovery without renaming the existing project package.
- Modify `scripts/validate_project.py`: validate the new VLA-first pre-hardware files.
- Modify `tests/test_scaffold.py`: add project identity, method scan, and validation checks.
- Create `tests/test_so101_episode_schema.py`: tests for schema validation and JSON persistence.
- Create `tests/test_so101_mock_dataset.py`: tests for deterministic mock dataset creation.
- Create `tests/test_so101_mock_training.py`: tests for mock training summary.
- Modify `Codex_Log.md`: record the VLA-first pre-hardware pivot after implementation.
- Modify `Codex_Log_zh.md`: Chinese progress note after implementation.

## Task 1: Reframe Project Entry Docs

**Files:**
- Modify: `README.md`
- Modify: `README_zh.md`
- Modify: `docs/project_index.md`
- Modify: `docs/project_index_zh.md`
- Modify: `tests/test_scaffold.py`

- [ ] **Step 1: Write the failing identity test**

Append this test to `tests/test_scaffold.py`:

```python
def test_project_identity_reflects_vla_first_pivot() -> None:
    root = Path(__file__).resolve().parents[1]
    readme = (root / "README.md").read_text(encoding="utf-8")
    readme_zh = (root / "README_zh.md").read_text(encoding="utf-8")
    project_index = (root / "docs" / "project_index.md").read_text(encoding="utf-8")
    project_index_zh = (root / "docs" / "project_index_zh.md").read_text(
        encoding="utf-8"
    )

    assert "# VLA-First SO-101 Robot Learning" in readme
    assert "RL plugins" in readme
    assert "SO-101" in readme
    assert "VLA-first" in project_index
    assert "vla_so101/" in project_index

    assert "# VLA-First SO-101 机器人学习" in readme_zh
    assert "RL 插件" in readme_zh
    assert "VLA-first" in project_index_zh
    assert "vla_so101/" in project_index_zh
```

- [ ] **Step 2: Run the identity test and verify it fails**

Run:

```bash
pytest tests/test_scaffold.py::test_project_identity_reflects_vla_first_pivot -v
```

Expected: `FAILED` because the current README and project index still describe
the old safety-aware MoE locomotion project as the main identity.

- [ ] **Step 3: Replace the top of `README.md`**

In `README.md`, replace the title and the section from the first line through
the end of the current `## Goals` list with this content:

````markdown
# VLA-First SO-101 Robot Learning

中文入口：[README_zh.md](README_zh.md)

This repository is a research-style workspace for building a VLA-first robot
learning project around the SO-101 arm with a wrist camera.

The current target project is:

**VLA-Guided SO-101 Point-and-Touch Robot Learning with RL Plugins**

The first demo is language-conditioned pointing or touching:

```text
wrist camera image + language instruction + robot state
        -> imitation-learned VLA policy
        -> SO-101 arm action
        -> point to or touch the target object
```

The earlier safety-aware MoE locomotion plan remains in this repository as
background research and future plugin reference. The active project surface is
now VLA-first: ACT/LeRobot-style imitation learning first, then Diffusion
Policy, SmolVLA, or RL plugins after the closed-set SO-101 baseline works.

## Goals

1. Prepare a pre-hardware SO-101 VLA project scaffold.
2. Define an episode schema for wrist-camera demonstrations collected through a
   dual SO-101 leader-follower setup.
3. Use ACT / LeRobot as the first imitation-learning baseline for point/touch
   target-object tasks.
4. Compare against Diffusion Policy or SmolVLA-style policies after the first
   baseline works.
5. Keep RL as a plugin layer for recovery, safety correction, or local
   fine-tuning rather than the first action executor.
6. Preserve the older RL locomotion and MoE notes as background and future
   plugin material.
````

- [ ] **Step 4: Replace the top of `README_zh.md`**

In `README_zh.md`, replace the title and the first project-goal section with
this content:

````markdown
# VLA-First SO-101 机器人学习

English entry: [README.md](README.md)

这个仓库现在的主线是一个围绕 SO-101 机械臂和 wrist camera 的
**VLA-first robot learning** 项目。

当前目标项目是：

**带 RL 插件的 VLA-Guided SO-101 指向/触碰机器人学习项目**

第一版 demo：

```text
wrist camera 图像 + 语言指令 + 机器人状态
        -> imitation-learned VLA policy
        -> SO-101 机械臂动作
        -> 指向或触碰目标物体
```

早期 safety-aware MoE locomotion 计划保留为背景研究和未来插件参考。
当前项目主线改为 VLA-first：先做 ACT / LeRobot 风格的模仿学习基线，
再考虑 Diffusion Policy、SmolVLA 或 RL 插件。

## 目标

1. 在硬件到货前准备 SO-101 VLA 项目骨架。
2. 定义双 SO-101 leader-follower 示范数据的 episode schema。
3. 用 ACT / LeRobot 作为第一版 point/touch 任务模仿学习基线。
4. 第一版稳定后再比较 Diffusion Policy 或 SmolVLA 风格策略。
5. RL 作为 recovery、safety correction、local fine-tuning 插件，而不是第一版动作执行主体。
6. 保留旧的 RL locomotion / MoE 文献和代码作为背景与未来插件材料。
````

- [ ] **Step 5: Update `docs/project_index.md` main entry points and code sections**

In `docs/project_index.md`, replace the `## Main Entry Points` and `## Code`
sections with this content:

```markdown
## Main Entry Points

- `README.md`: VLA-first SO-101 project overview and quick start.
- `docs/superpowers/specs/2026-06-19-vla-first-so101-design.md`: approved
  design for the VLA-first SO-101 pivot.
- `docs/references/vla_method_scan.md`: focused method scan for ACT, LeRobot,
  Diffusion Policy, SmolVLA, OpenVLA, Octo, pi0, RT-1, RT-2, and Open
  X-Embodiment.
- `rl_locomotion_moe_research_plan.md`: original RL locomotion and MoE research
  plan, kept as background and future plugin reference.
- `Codex_Log.md`: persistent task and progress log.
- `docs/setup/ENVIRONMENT.md`: environment deployment guide.
- `docs/setup/PACKAGE_INVENTORY.md`: package and framework inventory.
- `docs/project_structure.md`: folder organization and maintenance rules.
- `docs/references/paper_index.md`: papers and methods mentioned in the plan.
- `docs/paper_notes/`: individual and integrated literature notes.
- `experiments/README.md`: experiment output rules.

## Code

- `vla_so101/`: SO-101 wrist-camera data schemas, mock datasets, and
  pre-hardware training checks for the VLA-first line.
- `safe_moe_locomotion/envs/`: historical environment adapters and observation
  contracts for the RL locomotion line.
- `safe_moe_locomotion/policies/`: expert, MoE, safety-aware, residual policies.
- `safe_moe_locomotion/modules/`: encoders, gating network, risk estimator,
  safety supervisor.
- `safe_moe_locomotion/rewards/`: locomotion, navigation, recovery, and MoE
  regularization terms.
- `safe_moe_locomotion/training/`: trainer entrypoints and framework adapters.
- `safe_moe_locomotion/evaluation/`: rollout, metrics, terrain sweep, ablation.
- `safe_moe_locomotion/utils/`: config, logging, checkpoint, video helpers.
```

- [ ] **Step 6: Update `docs/project_index_zh.md` main entry points and code sections**

In `docs/project_index_zh.md`, replace the corresponding entry and code
sections with this content:

```markdown
## 主要入口

- `README_zh.md`：VLA-first SO-101 项目概览和快速入口。
- `docs/superpowers/specs/2026-06-19-vla-first-so101-design.md`：已经确认的
  VLA-first SO-101 pivot 设计。
- `docs/references/vla_method_scan.md`：ACT、LeRobot、Diffusion Policy、
  SmolVLA、OpenVLA、Octo、pi0、RT-1、RT-2、Open X-Embodiment 方法扫描。
- `rl_locomotion_moe_research_plan.md`：旧的 RL locomotion / MoE 研究计划，
  保留为背景和未来插件参考。
- `Codex_Log_zh.md`：长期任务进展记录。
- `docs/setup/ENVIRONMENT_zh.md`：环境部署说明。
- `docs/setup/PACKAGE_INVENTORY_zh.md`：依赖和框架清单。
- `docs/project_structure_zh.md`：目录维护规则。
- `docs/references/paper_index_zh.md`：论文和方法索引。
- `docs/paper_notes/`：单篇和综合文献笔记。
- `experiments/README_zh.md`：实验输出记录规则。

## 代码

- `vla_so101/`：SO-101 wrist-camera 数据 schema、mock dataset 和硬件到货前的
  VLA-first 训练检查。
- `safe_moe_locomotion/envs/`：旧 RL locomotion 线的环境适配和 observation contract。
- `safe_moe_locomotion/policies/`：expert、MoE、safety-aware、residual policy。
- `safe_moe_locomotion/modules/`：encoder、gating network、risk estimator、
  safety supervisor。
- `safe_moe_locomotion/rewards/`：locomotion、navigation、recovery、MoE regularization。
- `safe_moe_locomotion/training/`：trainer 入口和框架适配。
- `safe_moe_locomotion/evaluation/`：rollout、metrics、terrain sweep、ablation。
- `safe_moe_locomotion/utils/`：config、logging、checkpoint、video helper。
```

- [ ] **Step 7: Run the identity test and the scaffold tests**

Run:

```bash
pytest tests/test_scaffold.py::test_project_identity_reflects_vla_first_pivot -v
pytest tests/test_scaffold.py -v
```

Expected: both commands pass.

- [ ] **Step 8: Commit Task 1**

Run:

```bash
sh scripts/git_local.sh add README.md README_zh.md docs/project_index.md docs/project_index_zh.md tests/test_scaffold.py
sh scripts/git_local.sh commit -m "docs: reframe project as vla-first so101"
```

Expected: a commit is created with only the Task 1 files.

## Task 2: Add Focused VLA Method Scan

**Files:**
- Create: `docs/references/vla_method_scan.md`
- Modify: `docs/references/paper_index.md`
- Modify: `docs/references/reading_queue.md`
- Modify: `tests/test_scaffold.py`

- [ ] **Step 1: Write the failing method scan test**

Append this test to `tests/test_scaffold.py`:

```python
def test_vla_method_scan_covers_first_baseline_and_sota_context() -> None:
    root = Path(__file__).resolve().parents[1]
    method_scan = root / "docs" / "references" / "vla_method_scan.md"
    assert method_scan.exists()

    scan_text = method_scan.read_text(encoding="utf-8")
    for phrase in [
        "ACT / Action Chunking Transformer",
        "LeRobot",
        "Diffusion Policy",
        "SmolVLA",
        "OpenVLA",
        "Octo",
        "pi0",
        "RT-1",
        "RT-2",
        "Open X-Embodiment",
        "RL plugin",
    ]:
        assert phrase in scan_text

    assert scan_text.index("ACT / Action Chunking Transformer") < scan_text.index(
        "Diffusion Policy"
    )
    assert scan_text.count("https://") >= 10

    paper_index = (root / "docs" / "references" / "paper_index.md").read_text(
        encoding="utf-8"
    )
    assert "VLA-First SO-101 Method Scan" in paper_index

    reading_queue = (root / "docs" / "references" / "reading_queue.md").read_text(
        encoding="utf-8"
    )
    assert "Pre-Hardware VLA First Pass" in reading_queue
    assert reading_queue.index("ACT") < reading_queue.index("RT-1")
```

- [ ] **Step 2: Run the method scan test and verify it fails**

Run:

```bash
pytest tests/test_scaffold.py::test_vla_method_scan_covers_first_baseline_and_sota_context -v
```

Expected: `FAILED` because `docs/references/vla_method_scan.md` does not exist.

- [ ] **Step 3: Create `docs/references/vla_method_scan.md`**

Create the file with this content:

````markdown
# VLA Method Scan for SO-101 Point-and-Touch

Last updated: 2026-06-19.

This scan supports the VLA-first 2RL pivot. It is intentionally focused on
methods that can inform a dual SO-101 leader-follower setup with a wrist camera
and language-conditioned point/touch tasks.

## Method Priority

| Priority | Method | Role in 2RL | Reference |
|---:|---|---|---|
| 1 | ACT / Action Chunking Transformer | First imitation-learning baseline for teleoperated SO-101 demonstrations. | https://arxiv.org/abs/2304.13705 |
| 1 | LeRobot | First engineering stack for SO-101 setup, data collection, policy training, and evaluation patterns. | https://huggingface.co/docs/lerobot/en/index |
| 1 | LeRobot SO-101 | Hardware setup and leader-follower workflow reference. | https://huggingface.co/docs/lerobot/so101 |
| 2 | Diffusion Policy | Second baseline for multimodal continuous action sequence generation. | https://arxiv.org/abs/2303.04137 |
| 2 | SmolVLA | Near-term lightweight VLA policy extension after the ACT baseline works. | https://huggingface.co/docs/lerobot/en/smolvla |
| 3 | OpenVLA | Larger open VLA reference for positioning and possible fine-tuning direction. | https://arxiv.org/abs/2406.09246 |
| 3 | Octo | Generalist robot policy reference for multi-task, language-conditioned robotics. | https://arxiv.org/abs/2405.12213 |
| 3 | pi0 | VLM plus flow-matching action model reference for continuous robot action generation. | https://arxiv.org/abs/2410.24164 |
| 4 | RT-1 | Background for language-conditioned robotics transformer policies. | https://arxiv.org/abs/2212.06817 |
| 4 | RT-2 | Background for vision-language-action transfer from web-scale VLMs to robot control. | https://arxiv.org/abs/2307.15818 |
| 4 | Open X-Embodiment | Background for large-scale cross-robot data and RT-X style transfer. | https://arxiv.org/abs/2310.08864 |

## Recommended First Baseline

Use ACT through a LeRobot-style pipeline as the first baseline:

```text
wrist image + language instruction + joint state
        -> action chunk
        -> SO-101 joint target sequence
```

This matches the project constraints: teleoperated demonstrations, low-cost
robot hardware, short-horizon point/touch behavior, and a closed object set.

## Second Baseline

Use Diffusion Policy only after the ACT baseline has:

- a stable episode schema;
- reproducible mock data checks;
- real SO-101 demonstration episodes;
- a held-out layout evaluation split.

Diffusion Policy is useful because point/touch behavior can be multimodal when
the same object is reachable through different approach paths.

## VLA Extension Path

SmolVLA, OpenVLA, Octo, and pi0 should frame the project but not replace the
first baseline. The practical extension path is:

1. ACT closed-set point/touch.
2. Diffusion Policy comparison.
3. SmolVLA-style language-conditioned policy.
4. Open-vocabulary target selection.
5. Larger OpenVLA, Octo, or pi0-inspired fine-tuning only if data and hardware
   capacity justify it.

## RL Plugin Role

RL is not the first action executor. It becomes a plugin after imitation
learning works:

- recovery from stuck or off-target states;
- safety correction near joint limits or collision;
- local fine-tuning for final-contact behavior.
````

- [ ] **Step 4: Add a VLA-first section to `docs/references/paper_index.md`**

Insert this section after the introductory paragraph and before
`## Quadruped RL Locomotion Foundations`:

```markdown
## VLA-First SO-101 Method Scan

The active project direction is now VLA-first SO-101 point/touch learning. The
focused method scan lives in `docs/references/vla_method_scan.md`.

| Priority | Method | Link | Use in 2RL |
|---:|---|---|---|
| 1 | ACT / Action Chunking Transformer | https://arxiv.org/abs/2304.13705 | First imitation-learning baseline for leader-follower SO-101 demonstrations. |
| 1 | LeRobot | https://huggingface.co/docs/lerobot/en/index | First engineering stack for SO-101 data, training, and evaluation patterns. |
| 1 | LeRobot SO-101 | https://huggingface.co/docs/lerobot/so101 | Hardware setup and leader-follower workflow reference. |
| 2 | Diffusion Policy | https://arxiv.org/abs/2303.04137 | Second baseline for action-sequence generation. |
| 2 | SmolVLA | https://huggingface.co/docs/lerobot/en/smolvla | Near-term lightweight VLA extension. |
| 3 | OpenVLA | https://arxiv.org/abs/2406.09246 | Larger open VLA reference and positioning. |
| 3 | Octo | https://arxiv.org/abs/2405.12213 | Generalist robot policy reference. |
| 3 | pi0 | https://arxiv.org/abs/2410.24164 | VLM plus flow-matching action generation reference. |
```

- [ ] **Step 5: Reorder `docs/references/reading_queue.md`**

Replace the content of `docs/references/reading_queue.md` with:

```markdown
# Reading Queue

## Pre-Hardware VLA First Pass

1. ACT / Action Chunking Transformer
2. LeRobot SO-101 setup and leader-follower workflow
3. LeRobot ACT policy documentation
4. Diffusion Policy: Visuomotor Policy Learning via Action Diffusion
5. SmolVLA documentation
6. OpenVLA
7. Octo
8. pi0: A Vision-Language-Action Flow Model for General Robot Control

## VLA Background

9. RT-1
10. RT-2
11. Open X-Embodiment

## RL Plugin Background

12. Agile But Safe
13. RMA
14. MoE-Loco
15. CMoE
16. MoRE

## Historical Locomotion Background

17. Learning to Walk in Minutes Using Massively Parallel Deep Reinforcement Learning
18. Sim-to-Real: Learning Agile Locomotion For Quadruped Robots
19. Learning agile and dynamic motor skills for legged robots
20. Learning Quadrupedal Locomotion over Challenging Terrain
21. Advanced Skills by Learning Locomotion and Local Navigation End-to-End
22. Robot Parkour Learning
23. Extreme Parkour with Legged Robots
24. Learning Agile Locomotion on Risky Terrains
25. Resilient Legged Local Navigation
26. Humanoid-Gym and later humanoid extensions
```

- [ ] **Step 6: Run the method scan and paper index tests**

Run:

```bash
pytest tests/test_scaffold.py::test_vla_method_scan_covers_first_baseline_and_sota_context -v
pytest tests/test_scaffold.py::test_paper_index_has_expected_minimum -v
pytest tests/test_scaffold.py::test_paper_index_covers_expected_categories -v
```

Expected: all commands pass. The arXiv count remains at least 26 because the
old paper index content is preserved.

- [ ] **Step 7: Commit Task 2**

Run:

```bash
sh scripts/git_local.sh add docs/references/vla_method_scan.md docs/references/paper_index.md docs/references/reading_queue.md tests/test_scaffold.py
sh scripts/git_local.sh commit -m "docs: add vla method scan"
```

Expected: a commit is created with the method scan and reading queue updates.

## Task 3: Add SO-101 Episode Schema

**Files:**
- Create: `vla_so101/__init__.py`
- Create: `vla_so101/data/__init__.py`
- Create: `vla_so101/data/episode.py`
- Modify: `pyproject.toml`
- Create: `tests/test_so101_episode_schema.py`

- [ ] **Step 1: Write the failing schema tests**

Create `tests/test_so101_episode_schema.py` with this content:

```python
from pathlib import Path

import pytest

from vla_so101.data.episode import EpisodeFrame, EpisodeRecord


def make_episode() -> EpisodeRecord:
    return EpisodeRecord(
        episode_id="episode_0001",
        task_instruction="touch the red cube",
        object_set=["red cube", "blue cup"],
        success=True,
        frames=[
            EpisodeFrame(
                timestamp=0.0,
                wrist_image="images/episode_0001/frame_000.ppm",
                joint_positions=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
                action=[0.01, 0.02, 0.03, 0.04, 0.05, 0.06],
            ),
            EpisodeFrame(
                timestamp=0.1,
                wrist_image="images/episode_0001/frame_001.ppm",
                joint_positions=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                action=[0.02, 0.03, 0.04, 0.05, 0.06, 0.07],
            ),
        ],
    )


def test_episode_record_round_trips_through_dict() -> None:
    episode = make_episode()

    restored = EpisodeRecord.from_dict(episode.to_dict())

    assert restored == episode
    assert restored.action_dim == 6
    assert restored.joint_dim == 6


def test_episode_record_saves_and_loads_json(tmp_path: Path) -> None:
    episode = make_episode()
    output = tmp_path / "episode.json"

    episode.save_json(output)
    restored = EpisodeRecord.load_json(output)

    assert restored == episode


def test_episode_record_rejects_empty_instruction() -> None:
    data = make_episode().to_dict()
    data["task_instruction"] = " "

    with pytest.raises(ValueError, match="task_instruction"):
        EpisodeRecord.from_dict(data)


def test_episode_record_rejects_inconsistent_action_dimensions() -> None:
    data = make_episode().to_dict()
    data["frames"][1]["action"] = [0.1, 0.2]

    with pytest.raises(ValueError, match="action dimension"):
        EpisodeRecord.from_dict(data)
```

- [ ] **Step 2: Run the schema tests and verify they fail**

Run:

```bash
pytest tests/test_so101_episode_schema.py -v
```

Expected: `FAILED` with `ModuleNotFoundError: No module named 'vla_so101'`.

- [ ] **Step 3: Create `vla_so101/__init__.py`**

Create the file with this content:

```python
"""VLA-first SO-101 robot learning helpers."""

__all__ = ["data"]
```

- [ ] **Step 4: Create `vla_so101/data/__init__.py`**

Create the file with this content:

```python
"""Data schemas for SO-101 wrist-camera demonstrations."""

from vla_so101.data.episode import EpisodeFrame, EpisodeRecord

__all__ = ["EpisodeFrame", "EpisodeRecord"]
```

- [ ] **Step 5: Create `vla_so101/data/episode.py`**

Create the file with this content:

```python
"""Episode schema for SO-101 wrist-camera point/touch demonstrations."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


Number = int | float


def _validate_number_list(name: str, values: list[Any]) -> list[float]:
    if not values:
        raise ValueError(f"{name} must not be empty")
    result: list[float] = []
    for value in values:
        if not isinstance(value, (int, float)):
            raise ValueError(f"{name} must contain only numbers")
        result.append(float(value))
    return result


@dataclass(frozen=True)
class EpisodeFrame:
    """One time step from an SO-101 demonstration episode."""

    timestamp: float
    wrist_image: str
    joint_positions: list[float]
    action: list[float]

    def __post_init__(self) -> None:
        if self.timestamp < 0:
            raise ValueError("timestamp must be non-negative")
        if not self.wrist_image.strip():
            raise ValueError("wrist_image must not be empty")
        object.__setattr__(
            self,
            "joint_positions",
            _validate_number_list("joint_positions", list(self.joint_positions)),
        )
        object.__setattr__(
            self,
            "action",
            _validate_number_list("action", list(self.action)),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "wrist_image": self.wrist_image,
            "joint_positions": self.joint_positions,
            "action": self.action,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EpisodeFrame":
        return cls(
            timestamp=float(data["timestamp"]),
            wrist_image=str(data["wrist_image"]),
            joint_positions=list(data["joint_positions"]),
            action=list(data["action"]),
        )


@dataclass(frozen=True)
class EpisodeRecord:
    """A language-conditioned SO-101 demonstration episode."""

    episode_id: str
    task_instruction: str
    object_set: list[str]
    success: bool
    frames: list[EpisodeFrame]

    def __post_init__(self) -> None:
        if not self.episode_id.strip():
            raise ValueError("episode_id must not be empty")
        if not self.task_instruction.strip():
            raise ValueError("task_instruction must not be empty")
        if not self.object_set:
            raise ValueError("object_set must not be empty")
        if any(not item.strip() for item in self.object_set):
            raise ValueError("object_set entries must not be empty")
        if not isinstance(self.success, bool):
            raise ValueError("success must be a boolean")
        if not self.frames:
            raise ValueError("frames must not be empty")

        joint_dim = len(self.frames[0].joint_positions)
        action_dim = len(self.frames[0].action)
        for frame in self.frames:
            if len(frame.joint_positions) != joint_dim:
                raise ValueError("joint_positions dimension must be consistent")
            if len(frame.action) != action_dim:
                raise ValueError("action dimension must be consistent")

    @property
    def joint_dim(self) -> int:
        return len(self.frames[0].joint_positions)

    @property
    def action_dim(self) -> int:
        return len(self.frames[0].action)

    def to_dict(self) -> dict[str, Any]:
        return {
            "episode_id": self.episode_id,
            "task_instruction": self.task_instruction,
            "object_set": self.object_set,
            "success": self.success,
            "frames": [frame.to_dict() for frame in self.frames],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EpisodeRecord":
        return cls(
            episode_id=str(data["episode_id"]),
            task_instruction=str(data["task_instruction"]),
            object_set=[str(item) for item in data["object_set"]],
            success=bool(data["success"]),
            frames=[EpisodeFrame.from_dict(frame) for frame in data["frames"]],
        )

    def save_json(self, path: str | Path) -> None:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(self.to_dict(), indent=2, sort_keys=True),
            encoding="utf-8",
        )

    @classmethod
    def load_json(cls, path: str | Path) -> "EpisodeRecord":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("episode JSON root must be an object")
        return cls.from_dict(data)
```

- [ ] **Step 6: Update `pyproject.toml` package discovery**

Replace the `[tool.setuptools.packages.find]` section with:

```toml
[tool.setuptools.packages.find]
include = ["safe_moe_locomotion*", "vla_so101*"]
```

- [ ] **Step 7: Run schema tests**

Run:

```bash
pytest tests/test_so101_episode_schema.py -v
```

Expected: all tests pass.

- [ ] **Step 8: Run import and scaffold tests**

Run:

```bash
python -m compileall vla_so101
pytest tests/test_scaffold.py tests/test_so101_episode_schema.py -v
```

Expected: compileall succeeds and pytest passes.

- [ ] **Step 9: Commit Task 3**

Run:

```bash
sh scripts/git_local.sh add pyproject.toml vla_so101 tests/test_so101_episode_schema.py
sh scripts/git_local.sh commit -m "feat: add so101 episode schema"
```

Expected: a commit is created with the new `vla_so101` schema package.

## Task 4: Add Mock SO-101 Dataset Generator

**Files:**
- Create: `vla_so101/data/mock_dataset.py`
- Create: `scripts/create_mock_so101_dataset.py`
- Create: `tests/test_so101_mock_dataset.py`

- [ ] **Step 1: Write the failing mock dataset tests**

Create `tests/test_so101_mock_dataset.py` with this content:

```python
import json
from pathlib import Path

from vla_so101.data.episode import EpisodeRecord
from vla_so101.data.mock_dataset import write_mock_dataset


def test_write_mock_dataset_creates_manifest_episodes_and_images(tmp_path: Path) -> None:
    manifest = write_mock_dataset(tmp_path, num_episodes=2, frames_per_episode=3)

    manifest_path = tmp_path / "manifest.json"
    assert manifest_path.exists()
    assert manifest["dataset_name"] == "mock_so101_point_touch"
    assert manifest["num_episodes"] == 2
    assert len(manifest["episodes"]) == 2

    saved_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert saved_manifest == manifest

    first_episode_path = tmp_path / manifest["episodes"][0]
    first_episode = EpisodeRecord.load_json(first_episode_path)
    assert first_episode.task_instruction == "touch the red cube"
    assert len(first_episode.frames) == 3

    first_image_path = tmp_path / first_episode.frames[0].wrist_image
    assert first_image_path.exists()
    assert first_image_path.read_text(encoding="ascii").startswith("P3")


def test_write_mock_dataset_is_deterministic(tmp_path: Path) -> None:
    first_dir = tmp_path / "first"
    second_dir = tmp_path / "second"

    first_manifest = write_mock_dataset(first_dir, num_episodes=1, frames_per_episode=2)
    second_manifest = write_mock_dataset(second_dir, num_episodes=1, frames_per_episode=2)

    first_episode = (first_dir / first_manifest["episodes"][0]).read_text(
        encoding="utf-8"
    )
    second_episode = (second_dir / second_manifest["episodes"][0]).read_text(
        encoding="utf-8"
    )

    assert first_episode == second_episode
```

- [ ] **Step 2: Run the mock dataset tests and verify they fail**

Run:

```bash
pytest tests/test_so101_mock_dataset.py -v
```

Expected: `FAILED` with `ModuleNotFoundError` or import failure for
`vla_so101.data.mock_dataset`.

- [ ] **Step 3: Create `vla_so101/data/mock_dataset.py`**

Create the file with this content:

```python
"""Deterministic mock SO-101 datasets for pre-hardware checks."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from vla_so101.data.episode import EpisodeFrame, EpisodeRecord


DEFAULT_OBJECT_SET = ["red cube", "blue cup", "yellow block"]
DEFAULT_INSTRUCTIONS = [
    "touch the red cube",
    "point to the blue cup",
    "touch the yellow block",
]


def _write_ppm(path: Path, red: int, green: int, blue: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pixels = " ".join(f"{red} {green} {blue}" for _ in range(4))
    path.write_text(f"P3\n2 2\n255\n{pixels}\n", encoding="ascii")


def _make_frame(
    *,
    episode_index: int,
    frame_index: int,
    image_path: str,
) -> EpisodeFrame:
    base = episode_index * 0.1 + frame_index * 0.01
    joint_positions = [round(base + joint * 0.05, 4) for joint in range(6)]
    action = [round(value + 0.01, 4) for value in joint_positions]
    return EpisodeFrame(
        timestamp=round(frame_index * 0.1, 4),
        wrist_image=image_path,
        joint_positions=joint_positions,
        action=action,
    )


def write_mock_dataset(
    output_dir: str | Path,
    *,
    num_episodes: int = 3,
    frames_per_episode: int = 4,
) -> dict[str, Any]:
    if num_episodes <= 0:
        raise ValueError("num_episodes must be positive")
    if frames_per_episode <= 0:
        raise ValueError("frames_per_episode must be positive")

    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    episode_paths: list[str] = []

    for episode_index in range(num_episodes):
        episode_id = f"episode_{episode_index:04d}"
        instruction = DEFAULT_INSTRUCTIONS[episode_index % len(DEFAULT_INSTRUCTIONS)]
        frames: list[EpisodeFrame] = []

        for frame_index in range(frames_per_episode):
            image_rel = f"images/{episode_id}/frame_{frame_index:03d}.ppm"
            color = 40 + episode_index * 20 + frame_index * 5
            _write_ppm(
                root / image_rel,
                red=color,
                green=80 + frame_index * 3,
                blue=120 + episode_index * 7,
            )
            frames.append(
                _make_frame(
                    episode_index=episode_index,
                    frame_index=frame_index,
                    image_path=image_rel,
                )
            )

        episode = EpisodeRecord(
            episode_id=episode_id,
            task_instruction=instruction,
            object_set=DEFAULT_OBJECT_SET,
            success=episode_index % 2 == 0,
            frames=frames,
        )
        episode_rel = f"episodes/{episode_id}.json"
        episode.save_json(root / episode_rel)
        episode_paths.append(episode_rel)

    manifest: dict[str, Any] = {
        "dataset_name": "mock_so101_point_touch",
        "num_episodes": num_episodes,
        "frames_per_episode": frames_per_episode,
        "object_set": DEFAULT_OBJECT_SET,
        "episodes": episode_paths,
    }
    (root / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return manifest
```

- [ ] **Step 4: Create `scripts/create_mock_so101_dataset.py`**

Create the file with this content:

```python
#!/usr/bin/env python3
"""Create a deterministic mock SO-101 point/touch dataset."""

from __future__ import annotations

import argparse
from pathlib import Path

from vla_so101.data.mock_dataset import write_mock_dataset


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--num-episodes", type=int, default=3)
    parser.add_argument("--frames-per-episode", type=int, default=4)
    args = parser.parse_args()

    manifest = write_mock_dataset(
        args.output_dir,
        num_episodes=args.num_episodes,
        frames_per_episode=args.frames_per_episode,
    )
    print(f"Wrote {manifest['num_episodes']} episodes to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 5: Run the mock dataset tests**

Run:

```bash
pytest tests/test_so101_mock_dataset.py -v
```

Expected: all tests pass.

- [ ] **Step 6: Run the dataset CLI smoke check**

Run:

```bash
python scripts/create_mock_so101_dataset.py /tmp/2rl_mock_so101_dataset --num-episodes 2 --frames-per-episode 3
```

Expected output contains:

```text
Wrote 2 episodes to /tmp/2rl_mock_so101_dataset
```

- [ ] **Step 7: Commit Task 4**

Run:

```bash
sh scripts/git_local.sh add vla_so101/data/mock_dataset.py scripts/create_mock_so101_dataset.py tests/test_so101_mock_dataset.py
sh scripts/git_local.sh commit -m "feat: add so101 mock dataset generator"
```

Expected: a commit is created with the mock dataset generator and tests.

## Task 5: Add Mock Training-Readiness Check

**Files:**
- Create: `vla_so101/training/__init__.py`
- Create: `vla_so101/training/mock_train.py`
- Create: `scripts/run_mock_so101_training.py`
- Create: `tests/test_so101_mock_training.py`

- [ ] **Step 1: Write the failing mock training tests**

Create `tests/test_so101_mock_training.py` with this content:

```python
import json
from pathlib import Path

from vla_so101.data.mock_dataset import write_mock_dataset
from vla_so101.training.mock_train import summarize_dataset, write_training_summary


def test_summarize_dataset_counts_episodes_frames_and_actions(tmp_path: Path) -> None:
    write_mock_dataset(tmp_path, num_episodes=3, frames_per_episode=4)

    summary = summarize_dataset(tmp_path)

    assert summary["dataset_name"] == "mock_so101_point_touch"
    assert summary["num_episodes"] == 3
    assert summary["num_frames"] == 12
    assert summary["action_dim"] == 6
    assert summary["joint_dim"] == 6
    assert summary["success_rate"] == 2 / 3
    assert summary["unique_instructions"] == [
        "point to the blue cup",
        "touch the red cube",
        "touch the yellow block",
    ]


def test_write_training_summary_persists_json(tmp_path: Path) -> None:
    dataset_dir = tmp_path / "dataset"
    output_path = tmp_path / "summary.json"
    write_mock_dataset(dataset_dir, num_episodes=2, frames_per_episode=2)

    summary = write_training_summary(dataset_dir, output_path)

    saved = json.loads(output_path.read_text(encoding="utf-8"))
    assert saved == summary
    assert saved["num_frames"] == 4
```

- [ ] **Step 2: Run the mock training tests and verify they fail**

Run:

```bash
pytest tests/test_so101_mock_training.py -v
```

Expected: `FAILED` with `ModuleNotFoundError` or import failure for
`vla_so101.training.mock_train`.

- [ ] **Step 3: Create `vla_so101/training/__init__.py`**

Create the file with this content:

```python
"""Training-readiness checks for the SO-101 VLA line."""

from vla_so101.training.mock_train import summarize_dataset, write_training_summary

__all__ = ["summarize_dataset", "write_training_summary"]
```

- [ ] **Step 4: Create `vla_so101/training/mock_train.py`**

Create the file with this content:

```python
"""Mock training-readiness summary for SO-101 episode datasets."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from vla_so101.data.episode import EpisodeRecord


def _load_manifest(dataset_dir: Path) -> dict[str, Any]:
    manifest_path = dataset_dir / "manifest.json"
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("manifest JSON root must be an object")
    if "episodes" not in data or not isinstance(data["episodes"], list):
        raise ValueError("manifest must contain an episodes list")
    return data


def summarize_dataset(dataset_dir: str | Path) -> dict[str, Any]:
    root = Path(dataset_dir)
    manifest = _load_manifest(root)
    episodes = [EpisodeRecord.load_json(root / path) for path in manifest["episodes"]]
    if not episodes:
        raise ValueError("dataset must contain at least one episode")

    num_frames = sum(len(episode.frames) for episode in episodes)
    successes = sum(1 for episode in episodes if episode.success)
    unique_instructions = sorted({episode.task_instruction for episode in episodes})
    action_dims = {episode.action_dim for episode in episodes}
    joint_dims = {episode.joint_dim for episode in episodes}
    if len(action_dims) != 1:
        raise ValueError("all episodes must share one action dimension")
    if len(joint_dims) != 1:
        raise ValueError("all episodes must share one joint dimension")

    return {
        "dataset_name": manifest.get("dataset_name", "unknown"),
        "num_episodes": len(episodes),
        "num_frames": num_frames,
        "action_dim": action_dims.pop(),
        "joint_dim": joint_dims.pop(),
        "success_rate": successes / len(episodes),
        "unique_instructions": unique_instructions,
    }


def write_training_summary(
    dataset_dir: str | Path,
    output_path: str | Path,
) -> dict[str, Any]:
    summary = summarize_dataset(dataset_dir)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(summary, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return summary
```

- [ ] **Step 5: Create `scripts/run_mock_so101_training.py`**

Create the file with this content:

```python
#!/usr/bin/env python3
"""Run a mock training-readiness summary for an SO-101 dataset."""

from __future__ import annotations

import argparse
from pathlib import Path

from vla_so101.training.mock_train import write_training_summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset_dir", type=Path)
    parser.add_argument("output_path", type=Path)
    args = parser.parse_args()

    summary = write_training_summary(args.dataset_dir, args.output_path)
    print(
        "Mock training summary: "
        f"{summary['num_episodes']} episodes, "
        f"{summary['num_frames']} frames, "
        f"action_dim={summary['action_dim']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 6: Run mock training tests**

Run:

```bash
pytest tests/test_so101_mock_training.py -v
```

Expected: all tests pass.

- [ ] **Step 7: Run mock dataset plus training CLI smoke check**

Run:

```bash
python scripts/create_mock_so101_dataset.py /tmp/2rl_mock_so101_dataset --num-episodes 2 --frames-per-episode 3
python scripts/run_mock_so101_training.py /tmp/2rl_mock_so101_dataset /tmp/2rl_mock_so101_summary.json
```

Expected output contains:

```text
Wrote 2 episodes to /tmp/2rl_mock_so101_dataset
Mock training summary: 2 episodes, 6 frames, action_dim=6
```

- [ ] **Step 8: Commit Task 5**

Run:

```bash
sh scripts/git_local.sh add vla_so101/training scripts/run_mock_so101_training.py tests/test_so101_mock_training.py
sh scripts/git_local.sh commit -m "feat: add so101 mock training check"
```

Expected: a commit is created with the mock training-readiness check.

## Task 6: Update Project Validation and Logs

**Files:**
- Modify: `scripts/validate_project.py`
- Modify: `tests/test_scaffold.py`
- Modify: `Codex_Log.md`
- Modify: `Codex_Log_zh.md`

- [ ] **Step 1: Write the failing validation path test**

Append this test to `tests/test_scaffold.py`:

```python
def test_validate_project_tracks_vla_first_paths() -> None:
    validate_script = Path(__file__).resolve().parents[1] / "scripts" / "validate_project.py"
    text = validate_script.read_text(encoding="utf-8")

    for path in [
        "docs/superpowers/specs/2026-06-19-vla-first-so101-design.md",
        "docs/references/vla_method_scan.md",
        "vla_so101/data/episode.py",
        "vla_so101/data/mock_dataset.py",
        "vla_so101/training/mock_train.py",
    ]:
        assert path in text
```

- [ ] **Step 2: Run the validation path test and verify it fails**

Run:

```bash
pytest tests/test_scaffold.py::test_validate_project_tracks_vla_first_paths -v
```

Expected: `FAILED` because `scripts/validate_project.py` does not list the new
VLA-first paths.

- [ ] **Step 3: Add VLA-first paths to `scripts/validate_project.py`**

In `scripts/validate_project.py`, append these entries to `REQUIRED_PATHS`:

```python
    "docs/superpowers/specs/2026-06-19-vla-first-so101-design.md",
    "docs/references/vla_method_scan.md",
    "vla_so101/data/episode.py",
    "vla_so101/data/mock_dataset.py",
    "vla_so101/training/mock_train.py",
    "scripts/create_mock_so101_dataset.py",
    "scripts/run_mock_so101_training.py",
```

- [ ] **Step 4: Add progress entries to `Codex_Log.md`**

Append this entry to `Codex_Log.md`:

```markdown
## 2026-06-19 - VLA-first SO-101 pre-hardware pivot

- Reframed 2RL as a VLA-first SO-101 wrist-camera robot learning project.
- Kept RL as a future plugin layer for recovery, safety correction, and local
  fine-tuning.
- Added the pre-hardware SO-101 episode schema and mock dataset/training checks.
- Added a focused VLA method scan centered on ACT, LeRobot, Diffusion Policy,
  SmolVLA, OpenVLA, Octo, pi0, RT-1, RT-2, and Open X-Embodiment.
```

- [ ] **Step 5: Add progress entries to `Codex_Log_zh.md`**

Append this entry to `Codex_Log_zh.md`:

```markdown
## 2026-06-19 - VLA-first SO-101 硬件到货前 pivot

- 将 2RL 重定位为 VLA-first SO-101 wrist-camera 机器人学习项目。
- RL 保留为后续 recovery、safety correction、local fine-tuning 插件。
- 添加 SO-101 episode schema、mock dataset 和 mock training 检查。
- 添加以 ACT、LeRobot、Diffusion Policy、SmolVLA、OpenVLA、Octo、pi0、
  RT-1、RT-2、Open X-Embodiment 为核心的方法扫描。
```

- [ ] **Step 6: Run validation and full tests**

Run:

```bash
python scripts/validate_project.py
python -m compileall safe_moe_locomotion vla_so101
pytest -v
```

Expected output includes:

```text
Project scaffold validation passed.
```

Expected: compileall succeeds and all pytest tests pass.

- [ ] **Step 7: Commit Task 6**

Run:

```bash
sh scripts/git_local.sh add scripts/validate_project.py tests/test_scaffold.py Codex_Log.md Codex_Log_zh.md
sh scripts/git_local.sh commit -m "chore: validate vla-first prehardware scaffold"
```

Expected: a commit is created with validation and progress log updates.

## Final Verification

- [ ] **Step 1: Check the worktree is clean**

Run:

```bash
sh scripts/git_local.sh status --short
```

Expected: no output.

- [ ] **Step 2: Review recent commits**

Run:

```bash
sh scripts/git_local.sh log --oneline -8
```

Expected: the latest commits include:

```text
chore: validate vla-first prehardware scaffold
feat: add so101 mock training check
feat: add so101 mock dataset generator
feat: add so101 episode schema
docs: add vla method scan
docs: reframe project as vla-first so101
```

- [ ] **Step 3: Report completion**

Report:

```text
Pre-hardware VLA-first SO-101 scaffold is complete. README and docs now present
the VLA-first direction, the focused method scan is in place, the SO-101 episode
schema exists, and mock dataset/training checks pass.
```

## Self-Review Notes

- Spec coverage: this plan covers pre-hardware documentation, method scan,
  episode schema, mock dataset generation, mock training-readiness checks, and
  validation. It intentionally does not mount hardware, collect real data, train
  ACT, or add RL plugins.
- Boundary choice: `safe_moe_locomotion` is preserved; new SO-101 code lives in
  `vla_so101` to avoid mixing the VLA-first line with the historical locomotion
  scaffold.
- Test coverage: each new behavior has a pytest test before implementation, and
  the final verification runs scaffold validation, compileall, and the full test
  suite.
