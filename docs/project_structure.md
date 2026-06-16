# Project Structure Guide

This document records the approved structure cleanup for `/home/tomato/2RL`.
It is meant to prevent the repository from slowly growing many unrelated
top-level folders.

## Goal

Use a compact research Python project layout:

```text
2RL/
├── README.md
├── Codex_Log.md
├── rl_locomotion_moe_research_plan.md
├── pyproject.toml
├── environment.yml
├── requirements*.txt
├── configs/
├── docs/
├── experiments/
├── models/
├── data/
├── external/
├── assets/
├── notebooks/
├── scripts/
├── safe_moe_locomotion/
└── tests/
```

## Why This Structure

The first bootstrap layout mixed two styles:

- 3YP-style numbered folders such as `03_Experiments/` and `07_References/`;
- standard Python project folders such as `docs/`, `configs/`, `scripts/`, and
  `safe_moe_locomotion/`.

That made the top level noisy and created duplicate documentation locations.
The new structure keeps the Python project layout and moves research lifecycle
material into clear conventional folders.

## Migration Map

| Old Path | New Path | Reason |
|---|---|---|
| `05_Documentation/PROJECT_INDEX.md` | `docs/project_index.md` | Single documentation entrypoint. |
| `07_References/` | `docs/references/` | Papers and external references belong under docs. |
| `03_Experiments/` | `experiments/` | Conventional experiment output folder. |
| `04_Trained_Models/` | `models/` | Shorter checkpoint/model artifact folder. |
| `06_Data/` | `data/` | Conventional dataset folder. |
| `08_External/` | `external/` | Conventional location for local third-party clones. |
| `02_Code/README.md` | `docs/code_organization.md` | Code organization note belongs in docs. |
| `01_Reports/` | `docs/reports/` | Reports are documentation artifacts. |

## Where New Files Go

| File Type | Location |
|---|---|
| Reusable source code | `safe_moe_locomotion/` |
| Tests | `tests/` |
| YAML configs | `configs/` |
| CLI and maintenance scripts | `scripts/` |
| Environment setup docs | `docs/setup/` |
| Paper PDFs, manifests, references | `docs/references/` |
| Paper notes and synthesis | `docs/paper_notes/` |
| Experiment outputs | `experiments/` |
| Checkpoints and exported policies | `models/` |
| Large local datasets | `data/` |
| Optional external repo clones | `external/` |
| Figures, GIFs, videos | `assets/` |
| Analysis notebooks | `notebooks/` |

## Maintenance Rules

1. Do not create new numbered top-level folders.
2. Keep large PDFs, extracted full text, datasets, models, and videos out of git
   unless there is a specific release reason.
3. Add a `README.md` to any experiment folder that becomes important.
4. Update `docs/project_index.md` when adding a new major project area.
5. Update `Codex_Log.md` after large automated changes.
6. Prefer scripts over manual one-off commands for repeatable maintenance.

