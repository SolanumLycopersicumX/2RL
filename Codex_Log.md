# Codex Progress Log

This log records task progress so the project can be resumed after a network
drop, UI interruption, or context reset.

## 2026-06-15

### Current Objective

Build `/home/tomato/2RL` into a maintainable research project for:

**Safety-Aware Mixture-of-Experts Locomotion for Legged Local Navigation**

The project should follow the learning and reproduction goals in
`rl_locomotion_moe_research_plan.md` and borrow the research-project
organization style from `/home/tomato/3YP`.

### User Requirements Captured

- Collect and organize all papers mentioned or recommended in the markdown plan.
- Collect and organize all environment packages and installation instructions
  needed for learning and reproduction.
- Reference the layered architecture of `/home/tomato/3YP`.
- Keep the new project folder maintainable and readable.
- Use subagents to confirm completion status.
- Link the folder to GitHub repository:
  `https://github.com/SolanumLycopersicumX/2RL.git`.
- Keep a persistent progress log during the task.

### Completed

- Read `rl_locomotion_moe_research_plan.md`.
- Found reference project `/home/tomato/3YP`.
- Spawned a read-only subagent to analyze `/home/tomato/3YP` architecture.
- Received subagent summary recommending:
  - Keep standard Python package layout for code.
  - Add 3YP-style project index, experiment rules, references, and claim
    boundary docs.
  - Avoid vendoring large external repos or generated artifacts.
- Created initial top-level project directories:
  - `01_Reports/`
  - `02_Code/`
  - `03_Experiments/`
  - `04_Trained_Models/`
  - `05_Documentation/`
  - `06_Data/`
  - `07_References/`
  - `08_External/`
  - `configs/`
  - `docs/`
  - `scripts/`
  - `safe_moe_locomotion/`
  - `tests/`
  - `assets/`
  - `notebooks/`
- Created persistent progress log `Codex_Log.md`.
- Created first maintainability layer:
  - `README.md`
  - `.gitignore`
  - `pyproject.toml`
  - `requirements.txt`
  - `requirements-dev.txt`
  - `environment.yml`
  - `05_Documentation/PROJECT_INDEX.md`
  - `docs/PROJECT_INDEX.md`
  - `03_Experiments/README.md`
  - `docs/future_work/claim_boundary.md`
  - `07_References/README.md`
  - `07_References/external_repos.md`
  - `07_References/reading_queue.md`
  - `docs/paper_notes/README.md`
- Created paper and environment indexes:
  - `07_References/paper_index.md`
  - `docs/setup/PACKAGE_INVENTORY.md`
  - `docs/setup/ENVIRONMENT.md`
- Created config templates:
  - `configs/robot/*.yaml`
  - `configs/terrain/*.yaml`
  - `configs/train/*.yaml`
  - `configs/moe/*.yaml`
- Created Python package skeleton under `safe_moe_locomotion/`.
- Created script entrypoints under `scripts/`.
- Created lightweight tests under `tests/`.
- Verification passed:
  - `python3 scripts/validate_project.py`
  - `python3 -m compileall safe_moe_locomotion scripts tests`
  - `sh scripts/run_tests.sh`
  - `python3 -m safe_moe_locomotion.training.run_experiment --config configs/train/ppo_flat.yaml --dry-run`
- Applied final subagent review fixes:
  - fixed Isaac Lab commit-recording command path in `docs/setup/ENVIRONMENT.md`;
  - added Git, Conda/Mamba, CUDA Toolkit, NVIDIA Driver, and Humanoid-Gym to
    package/framework inventory;
  - added Humanoid-Gym to external repo registry;
  - expanded tests from 2 to 7 cases.
- Verification after final review fixes passed:
  - `python3 scripts/validate_project.py`
  - `python3 -m compileall safe_moe_locomotion scripts tests`
  - `sh scripts/run_tests.sh` -> 7 passed
  - `python3 -m safe_moe_locomotion.training.run_experiment --config configs/train/ppo_gate.yaml --dry-run`
- Final verification passed:
  - `python3 scripts/validate_project.py` -> scaffold validation passed,
    24 required paths, 23 arXiv links.
  - `sh scripts/run_tests.sh` -> 7 passed.
  - `python3 -m safe_moe_locomotion.training.run_experiment --config configs/train/ppo_gate.yaml --dry-run`
    -> dry-run config dispatch succeeded.
  - `sh scripts/git_local.sh remote -v` -> origin points to
    `https://github.com/SolanumLycopersicumX/2RL.git`.
- Cleaned generated `.pytest_cache` and `__pycache__` directories after final
  tests.

### Current Blockers / Notes

- `.git`, `.agents`, and `.codex` appear as read-only placeholder directories.
- `git status` reports that `/home/tomato/2RL` is not currently a valid git
  repository.
- Initial `git init` attempt failed because the placeholder directories were
  read-only or unavailable under the escalated command context. This needs a
  separate cleanup/init step after files are created.
- Plain `python3 -m pytest tests` auto-loaded ROS 2 pytest plugins from
  `/opt/ros/jazzy` and failed because that external plugin path lacked `lark`.
  Project tests pass when run with `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, now
  wrapped by `scripts/run_tests.sh`.
- Final subagent review found:
  - Isaac Lab commit-recording command used the wrong relative path after `cd`.
  - package inventory did not explicitly list Git, Conda/Mamba, CUDA Toolkit,
    NVIDIA Driver, or Humanoid-Gym.
  - tests were too shallow.
  - real Isaac Lab / legged_gym training adapters are intentionally not wired
    at bootstrap stage.
- Standard git binding remains blocked because `/home/tomato/2RL/.git` is a
  read-only `tmpfs` mount. `umount` requires superuser privileges, and both
  interactive `sudo` and non-interactive `sudo -n` are unavailable from this
  tool session.
- Fallback created:
  - `.git-local/` initialized as git dir;
  - remote `origin` set to `https://github.com/SolanumLycopersicumX/2RL.git`;
  - `scripts/git_local.sh` wraps `git --git-dir=.git-local --work-tree=.`;
  - `.git-local/` is ignored by `.gitignore`.

### Next Steps

1. If a standard `.git` directory is required, open an interactive shell and
   run:
   `sudo umount /home/tomato/2RL/.git`
   then:
   `git init && git branch -m main && git remote add origin https://github.com/SolanumLycopersicumX/2RL.git`
2. To use the fallback git-dir now:
   `sh scripts/git_local.sh status`
   `sh scripts/git_local.sh add .`
   `sh scripts/git_local.sh commit -m "Bootstrap safe MoE locomotion project"`
   `sh scripts/git_local.sh push -u origin main`
3. Install Isaac Lab or legacy legged_gym according to `docs/setup/ENVIRONMENT.md`.

## 2026-06-15 Literature Download and Notes

### Current Objective

Download all publicly indexed papers from `07_References/paper_index.md`, then
create:

- one note per paper under `docs/paper_notes/individual/`;
- one integrated literature synthesis under `docs/paper_notes/integrated_literature_review.md`;
- a download/metadata manifest under `07_References/papers/`.

### Status

- Started literature download and note generation task.
- Created `07_References/papers/`, `docs/paper_notes/individual/`, and
  `docs/paper_notes/extracted_text/`.
- Added reusable downloader script `scripts/download_papers.py`.
- First sandboxed download attempt failed with `Operation not permitted`.
- Re-ran with approved network access.
- Downloaded 23/23 indexed arXiv PDFs successfully.
- Generated `07_References/papers/papers_manifest.csv`.
- Added `scripts/extract_paper_text.py`.
- Extracted text for 23/23 PDFs into `docs/paper_notes/extracted_text/`.
- Added `scripts/generate_paper_notes.py`.
- Generated:
  - 23 individual notes under `docs/paper_notes/individual/`;
  - `docs/paper_notes/individual/README.md`;
  - `docs/paper_notes/integrated_literature_review.md`.
- Updated note entrypoints:
  - `docs/paper_notes/README.md`;
  - `07_References/README.md`.
- Updated `.gitignore` so downloaded PDFs and extracted full text stay local by
  default, while manifests and notes remain trackable.
- Final verification for literature task:
  - 23 PDFs in `07_References/papers/`;
  - 23 extracted text files in `docs/paper_notes/extracted_text/`;
  - 23 individual paper notes in `docs/paper_notes/individual/`;
  - integrated literature review exists and has 196 lines;
  - `python3 -m compileall scripts safe_moe_locomotion tests` passed;
  - `sh scripts/run_tests.sh` -> 7 passed.
- Cleaned generated `.pytest_cache` and `__pycache__` after verification.

## 2026-06-15 Project Structure Cleanup

### Objective

Reduce top-level folder clutter by applying the approved compact research
Python layout, documented in `docs/project_structure.md`.

### Completed

- Added restructure implementation plan:
  `docs/superpowers/plans/2026-06-15-restructure-project-layout.md`.
- Added long-term structure guide:
  `docs/project_structure.md`.
- Updated tests first to expect the new layout and confirmed the tests failed
  before moving files.
- Moved folders:
  - `05_Documentation/PROJECT_INDEX.md` -> `docs/project_index.md`
  - `07_References/` -> `docs/references/`
  - `03_Experiments/` -> `experiments/`
  - `04_Trained_Models/` -> `models/`
  - `06_Data/` -> `data/`
  - `08_External/` -> `external/`
  - `02_Code/README.md` -> `docs/code_organization.md`
- Removed empty numbered directories:
  - `01_Reports/`
  - `02_Code/`
  - `05_Documentation/`
- Removed old duplicate `docs/PROJECT_INDEX.md`.
- Updated active references in:
  - `README.md`
  - `docs/project_index.md`
  - `docs/setup/ENVIRONMENT.md`
  - `docs/setup/PACKAGE_INVENTORY.md`
  - `docs/references/README.md`
  - `docs/references/external_repos.md`
  - `docs/paper_notes/README.md`
  - `experiments/README.md`
  - scripts under `scripts/`
  - training configs under `configs/train/`
  - `safe_moe_locomotion/utils/checkpoints.py`
- Regenerated:
  - `docs/paper_notes/extracted_text/text_manifest.csv`
  - 23 individual paper notes
  - `docs/paper_notes/integrated_literature_review.md`
- Cleaned generated caches and empty `.github` placeholder directory.

### Verification

- `python3 scripts/validate_project.py` passed:
  - 26 required paths.
  - 23 arXiv links.
- `sh scripts/run_tests.sh` passed:
  - 7 tests passed.
- `python3 -m compileall scripts safe_moe_locomotion tests` passed.
- `python3 -m safe_moe_locomotion.training.run_experiment --config configs/train/ppo_gate.yaml --dry-run` passed.
- Confirmed:
  - no visible numbered top-level folders remain;
  - 23 PDFs remain in `docs/references/papers/`;
  - 23 individual paper notes remain in `docs/paper_notes/individual/`.

## 2026-06-15 Chinese Documentation Counterparts

### Objective

Generate Chinese counterparts for the project documentation layer without
overwriting the existing English or mixed-language files.

### Completed

- Added generator script:
  `scripts/generate_chinese_docs.py`.
- Generated Chinese entry documents:
  - `README_zh.md`
  - `Codex_Log_zh.md`
  - `docs/project_index_zh.md`
  - `docs/project_structure_zh.md`
  - `docs/code_organization_zh.md`
- Generated Chinese setup and dependency docs:
  - `docs/setup/ENVIRONMENT_zh.md`
  - `docs/setup/PACKAGE_INVENTORY_zh.md`
- Generated Chinese reference docs:
  - `docs/references/README_zh.md`
  - `docs/references/external_repos_zh.md`
  - `docs/references/paper_index_zh.md`
  - `docs/references/reading_queue_zh.md`
- Generated Chinese paper-note docs:
  - `docs/paper_notes/README_zh.md`
  - `docs/paper_notes/integrated_literature_review_zh.md`
  - `docs/paper_notes/individual/README_zh.md`
  - 23 individual `*_zh.md` paper notes.
- Generated Chinese experiment documentation:
  - `experiments/README_zh.md`
- Generated Chinese restructure-plan summary:
  - `docs/superpowers/plans/2026-06-15-restructure-project-layout_zh.md`
- Added Chinese entry links to key English docs.
- Expanded tests to verify key Chinese docs and 23 Chinese individual paper notes.

### Verification

- `python3 scripts/validate_project.py` passed.
- `python3 -m compileall scripts safe_moe_locomotion tests` passed.
- `sh scripts/run_tests.sh` passed:
  - 9 tests passed.
- Count checks:
  - 40 `*_zh.md` files.
  - 23 individual Chinese paper notes.
- Cleaned generated `.pytest_cache` and `__pycache__`.

## 2026-06-17 Recommended Reading Order

### Objective

Create a complete Chinese recommended reading order covering all 23 papers.

### Completed

- Added `docs/references/recommended_reading_order_zh.md`.
- The guide covers all 23 papers in a project-driven sequence:
  baseline locomotion -> robustness/sim-to-real -> terrain/navigation/safety
  -> MoE routing -> humanoid extension.
- Linked the guide from:
  - `README_zh.md`
  - `docs/project_index_zh.md`
  - `docs/references/README_zh.md`
  - `docs/references/reading_queue_zh.md`
- Added a test to verify the reading order contains 23 paper sections.

### Verification

- `python3 scripts/validate_project.py` passed.
- `python3 -m compileall scripts safe_moe_locomotion tests` passed.
- `sh scripts/run_tests.sh` passed:
  - 10 tests passed.
- `rg -n "^### " docs/references/recommended_reading_order_zh.md | wc -l`
  returned 23.

### GitHub Sync

- Committed reading-order updates:
  `c8ce8b1 docs: add complete paper reading order`.
- Pushed `main` to:
  `https://github.com/SolanumLycopersicumX/2RL.git`.
- Verified local `HEAD` and `origin/main` both resolve to:
  `c8ce8b156901d047732b20d4afe4532c952fe01a`.
- Note: PDF files and extracted full-text files remain local by `.gitignore`
  policy. GitHub contains manifests, scripts, project docs, and paper notes so
  the local paper archive can be reproduced without republishing full papers.
