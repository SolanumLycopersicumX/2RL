# 引用资料与 Attribution

该目录用于把外部论文、外部仓库和引用信息与本项目自写代码分开。

## 文件说明

- `paper_index.md` / `paper_index_zh.md`：论文清单。
- `reading_queue.md` / `reading_queue_zh.md`：推荐阅读顺序。
- `recommended_reading_order_zh.md`：覆盖 26 篇论文的详细中文阅读顺序。
- `external_repos.md` / `external_repos_zh.md`：外部代码仓库、用途和建议克隆位置。
- `papers/`：已下载的 arXiv PDF 和 `papers_manifest.csv`。

## 规则

1. 记录论文标题、链接、用途和阅读优先级。
2. PDF 默认不进 git，只保留 manifest 和笔记。
3. 外部代码放 `external/` 或作为 submodule，不复制进主包。
4. 改写第三方代码前先确认 license。
