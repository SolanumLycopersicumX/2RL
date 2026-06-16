# 项目结构重构执行计划

## 目标

把仓库从 3YP 编号目录与 Python 项目目录混合的结构，整理为更紧凑的科研 Python 项目结构。

## 目标结构

```text
configs/
docs/
experiments/
models/
data/
external/
assets/
notebooks/
scripts/
safe_moe_locomotion/
tests/
```

## 已执行任务

1. 先修改测试，让测试期望新路径，并确认测试失败。
2. 移动目录：
   - `07_References/` -> `docs/references/`
   - `03_Experiments/` -> `experiments/`
   - `04_Trained_Models/` -> `models/`
   - `06_Data/` -> `data/`
   - `08_External/` -> `external/`
   - `05_Documentation/PROJECT_INDEX.md` -> `docs/project_index.md`
   - `02_Code/README.md` -> `docs/code_organization.md`
3. 更新 README、脚本、配置、测试和文档中的旧路径。
4. 重新生成论文笔记和 manifest。
5. 跑验证命令。

## 验证命令

```bash
python3 scripts/validate_project.py
sh scripts/run_tests.sh
python3 -m compileall scripts safe_moe_locomotion tests
python3 -m safe_moe_locomotion.training.run_experiment --config configs/train/ppo_gate.yaml --dry-run
```
