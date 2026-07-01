from pathlib import Path

from app.core.settings import load_config


def test_load_config_returns_defaults():
    config = load_config()
    assert config.model.confidence_threshold == 0.5
    assert config.model.iou_threshold == 0.45
    assert config.output.image_dir == Path("output/images")


def test_load_config_model_path_as_path():
    config = load_config()
    assert isinstance(config.model.path, Path)
