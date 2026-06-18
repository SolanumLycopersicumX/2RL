from pathlib import Path

import pytest

from safe_moe_locomotion.modules.safety_supervisor import threshold_recovery_decision
from safe_moe_locomotion.policies.moe_policy import validate_moe_shapes
from safe_moe_locomotion.utils.config import load_yaml


def test_required_scaffold_files_exist() -> None:
    root = Path(__file__).resolve().parents[1]
    required = [
        root / "README.md",
        root / "README_zh.md",
        root / "Codex_Log.md",
        root / "Codex_Log_zh.md",
        root / "docs" / "project_index.md",
        root / "docs" / "project_index_zh.md",
        root / "docs" / "references" / "paper_index.md",
        root / "docs" / "references" / "paper_index_zh.md",
        root / "docs" / "references" / "recommended_reading_order_zh.md",
        root / "docs" / "references" / "papers" / "papers_manifest.csv",
        root / "experiments" / "README.md",
        root / "experiments" / "README_zh.md",
        root / "models" / ".gitkeep",
        root / "data" / ".gitkeep",
        root / "external" / ".gitkeep",
        root / "docs" / "setup" / "ENVIRONMENT.md",
        root / "docs" / "setup" / "ENVIRONMENT_zh.md",
        root / "safe_moe_locomotion" / "modules" / "gating_network.py",
    ]
    assert all(path.exists() for path in required)


def test_paper_index_has_expected_minimum() -> None:
    root = Path(__file__).resolve().parents[1]
    paper_index = (root / "docs" / "references" / "paper_index.md").read_text(encoding="utf-8")
    assert paper_index.count("https://arxiv.org/abs/") >= 26


def test_paper_index_covers_expected_categories() -> None:
    root = Path(__file__).resolve().parents[1]
    paper_index = (root / "docs" / "references" / "paper_index.md").read_text(encoding="utf-8")
    expected = [
        "Quadruped RL Locomotion Foundations",
        "Perceptive Navigation, Parkour, and Risky Terrain",
        "Humanoid Locomotion and Whole-Body Control",
        "MoE, Expert Composition, and Routing",
        "VLA, Action Sequence Modeling, and Diffusion Policy",
    ]
    for heading in expected:
        assert heading in paper_index
    for title in [
        "Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware",
        "Diffusion Policy: Visuomotor Policy Learning via Action Diffusion",
        "pi0: A Vision-Language-Action Flow Model for General Robot Control",
    ]:
        assert title in paper_index


def test_chinese_paper_notes_have_expected_count() -> None:
    root = Path(__file__).resolve().parents[1]
    notes = list((root / "docs" / "paper_notes" / "individual").glob("*_zh.md"))
    notes = [path for path in notes if path.name != "README_zh.md"]
    assert len(notes) == 26


def test_chinese_integrated_review_exists() -> None:
    root = Path(__file__).resolve().parents[1]
    review = root / "docs" / "paper_notes" / "integrated_literature_review_zh.md"
    text = review.read_text(encoding="utf-8")
    assert "整合文献综述" in text
    assert "Safety" in text or "safety" in text


def test_recommended_reading_order_covers_all_papers() -> None:
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "references" / "recommended_reading_order_zh.md").read_text(
        encoding="utf-8"
    )
    assert text.count("### ") == 26
    assert "最短可执行路线" in text
    assert "VLA 拓展阅读" in text


def test_config_loader_reads_training_config() -> None:
    root = Path(__file__).resolve().parents[1]
    config = load_yaml(root / "configs" / "train" / "ppo_flat.yaml")
    assert config["experiment"]["name"] == "flat_expert"
    assert config["backend"] == "isaac_lab"


def test_config_loader_rejects_missing_path() -> None:
    with pytest.raises(FileNotFoundError):
        load_yaml("missing_config.yaml")


def test_moe_shape_validation() -> None:
    validate_moe_shapes(num_experts=2, action_dim=12)
    with pytest.raises(ValueError):
        validate_moe_shapes(num_experts=1, action_dim=12)
    with pytest.raises(ValueError):
        validate_moe_shapes(num_experts=2, action_dim=0)


def test_safety_supervisor_threshold_decision() -> None:
    safe = threshold_recovery_decision(risk_score=0.2, threshold=0.6)
    unsafe = threshold_recovery_decision(risk_score=0.8, threshold=0.6)
    assert safe.use_recovery is False
    assert unsafe.use_recovery is True
    with pytest.raises(ValueError):
        threshold_recovery_decision(risk_score=1.2, threshold=0.6)
