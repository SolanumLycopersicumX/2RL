# Codex 进度日志中文摘要

本文档是 `Codex_Log.md` 的中文摘要版，用来快速了解当前项目状态。

## 当前项目目标

构建 `/home/tomato/2RL`，用于学习和复现：

**Safety-Aware Mixture-of-Experts Locomotion for Legged Local Navigation**

也就是：面向腿式机器人局部导航的安全感知 MoE 门控运动控制。

## 已完成内容

### 项目结构

- 已采用精简后的科研 Python 项目结构。
- 目录整理规则已写入：
  [docs/project_structure_zh.md](docs/project_structure_zh.md)
- 中文项目索引已写入：
  [docs/project_index_zh.md](docs/project_index_zh.md)

### 论文与资料

- 已下载 23 篇 arXiv PDF 到：
  `docs/references/papers/`
- 已生成 PDF manifest：
  `docs/references/papers/papers_manifest.csv`
- 已提取 23 篇论文文本到：
  `docs/paper_notes/extracted_text/`
- 已生成 23 篇单篇中文论文笔记：
  [docs/paper_notes/individual/README_zh.md](docs/paper_notes/individual/README_zh.md)
- 已生成所有论文整合中文综述：
  [docs/paper_notes/integrated_literature_review_zh.md](docs/paper_notes/integrated_literature_review_zh.md)

### 环境与依赖

- 中文环境部署指南：
  [docs/setup/ENVIRONMENT_zh.md](docs/setup/ENVIRONMENT_zh.md)
- 中文依赖清单：
  [docs/setup/PACKAGE_INVENTORY_zh.md](docs/setup/PACKAGE_INVENTORY_zh.md)
- 当前机器适合先建独立 conda 环境，不建议直接使用系统 Python 跑 Isaac。

### 代码骨架

- 主 Python 包：`safe_moe_locomotion/`
- 配置模板：`configs/`
- 训练/维护脚本：`scripts/`
- 测试：`tests/`

### Git 状态

- 标准 `.git` 目录当前被只读 tmpfs 挂载阻塞。
- 已创建 fallback git-dir：`.git-local/`
- 可用命令：

```bash
sh scripts/git_local.sh status
sh scripts/git_local.sh remote -v
```

## 最近验证

已通过：

```bash
python3 scripts/validate_project.py
sh scripts/run_tests.sh
python3 -m compileall scripts safe_moe_locomotion tests
python3 -m safe_moe_locomotion.training.run_experiment --config configs/train/ppo_gate.yaml --dry-run
```

## 下一步建议

1. 先读：
   [docs/paper_notes/integrated_literature_review_zh.md](docs/paper_notes/integrated_literature_review_zh.md)
2. 再读前 5 篇单篇论文笔记：
   - Learning to Walk in Minutes
   - RMA
   - Challenging Terrain
   - Agile But Safe
   - MoE-Loco
3. 同步按：
   [docs/setup/ENVIRONMENT_zh.md](docs/setup/ENVIRONMENT_zh.md)
   准备 Isaac Lab 或 legacy legged_gym 环境。
