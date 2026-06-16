# 项目结构指南

本文档记录 `/home/tomato/2RL` 的目录整理规则，防止后续再次出现大量零散顶层文件夹。

## 目标结构

```text
2RL/
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

## 为什么这样整理

早期 bootstrap 同时混用了两种结构：

- 3YP 风格编号目录，例如 `03_Experiments/`、`07_References/`；
- 标准 Python 项目目录，例如 `docs/`、`configs/`、`scripts/`、`safe_moe_locomotion/`。

这会让顶层目录过多、职责重复。现在保留 Python 科研项目结构，把研究资料统一放入 `docs/`。

## 迁移映射

| 旧路径 | 新路径 |
|---|---|
| `05_Documentation/PROJECT_INDEX.md` | `docs/project_index.md` |
| `07_References/` | `docs/references/` |
| `03_Experiments/` | `experiments/` |
| `04_Trained_Models/` | `models/` |
| `06_Data/` | `data/` |
| `08_External/` | `external/` |
| `02_Code/README.md` | `docs/code_organization.md` |
| `01_Reports/` | `docs/reports/` |

## 新文件应该放哪里

| 文件类型 | 位置 |
|---|---|
| 可复用源代码 | `safe_moe_locomotion/` |
| 测试 | `tests/` |
| YAML 配置 | `configs/` |
| CLI 和维护脚本 | `scripts/` |
| 环境部署文档 | `docs/setup/` |
| 论文、引用、外部 repo 记录 | `docs/references/` |
| 论文笔记 | `docs/paper_notes/` |
| 实验输出 | `experiments/` |
| checkpoint / policy export | `models/` |
| 本地数据集 | `data/` |
| 外部仓库克隆 | `external/` |
| 图、视频、GIF | `assets/` |
| notebook | `notebooks/` |

## 规则

1. 不再新增编号式顶层目录。
2. PDF、全文提取、数据集、模型、视频默认不进 git。
3. 重要实验目录需要有 `README.md` 或 `summary.json`。
4. 新增主要区域时更新 `docs/project_index.md` 和 `docs/project_index_zh.md`。
