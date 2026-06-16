# 代码组织说明

主 Python 包位于：

```text
safe_moe_locomotion/
```

早期曾保留 `02_Code/` 以模仿 3YP 的编号目录结构。现在该目录已合并到标准 Python 项目布局中，新的可复用代码不应再放到零散目录里。

建议：

- 可复用模块放 `safe_moe_locomotion/`。
- 可执行入口和维护脚本放 `scripts/`。
- 配置放 `configs/`。
- 实验结果放 `experiments/`。
- 临时分析放 `notebooks/`，但不要把 notebook 当成唯一实现。
