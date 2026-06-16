# Project Layout Restructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the repository from mixed 3YP-numbered and Python-project layout into the approved compact research Python layout.

**Architecture:** Keep code, configs, scripts, tests, assets, notebooks, and root metadata at the top level. Move research documentation and references under `docs/`, and rename generated-output folders to conventional names: `experiments/`, `models/`, `data/`, and `external/`.

**Tech Stack:** Python project files, Markdown docs, YAML configs, shell/Python scripts, pytest.

---

### Task 1: Add Failing Layout Tests

**Files:**
- Modify: `tests/test_scaffold.py`

- [x] Add assertions for the approved layout:
  - `docs/project_index.md`
  - `docs/references/paper_index.md`
  - `docs/references/papers/papers_manifest.csv`
  - `experiments/README.md`
  - `models/.gitkeep`
  - `data/.gitkeep`
  - `external/.gitkeep`

- [x] Run `sh scripts/run_tests.sh` and confirm it fails because paths have not moved yet.

### Task 2: Move Directories

**Files:**
- Move `05_Documentation/PROJECT_INDEX.md` to `docs/project_index.md`
- Move `07_References/` to `docs/references/`
- Move `03_Experiments/` to `experiments/`
- Move `04_Trained_Models/` to `models/`
- Move `06_Data/` to `data/`
- Move `08_External/` to `external/`
- Move `01_Reports/` to `docs/reports/` if it contains files; otherwise remove the empty directory
- Move `02_Code/README.md` to `docs/code_organization.md`

### Task 3: Update References

**Files:**
- Modify: `README.md`
- Modify: `Codex_Log.md`
- Modify: `.gitignore`
- Modify: `scripts/download_papers.py`
- Modify: `scripts/extract_paper_text.py`
- Modify: `scripts/generate_paper_notes.py`
- Modify: `scripts/validate_project.py`
- Modify: `safe_moe_locomotion/utils/checkpoints.py`
- Modify: docs that reference old numbered paths

### Task 4: Verify

- [ ] Run `python3 scripts/validate_project.py`
- [ ] Run `python3 -m compileall scripts safe_moe_locomotion tests`
- [ ] Run `sh scripts/run_tests.sh`
- [ ] Run `python3 scripts/generate_paper_notes.py`
- [ ] Clean generated caches
- [ ] Update `Codex_Log.md`
