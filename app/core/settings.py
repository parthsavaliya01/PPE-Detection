from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import yaml
from pydantic import BaseModel, Field, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelConfig(BaseModel):
    path: Path = Field(default_factory=lambda: Path("weights/best.pt"))
    name: str = "yolov8n"
    device: str = "cpu"
    confidence_threshold: float = 0.25
    iou_threshold: float = 0.45
    image_size: int = 640
    classes: List[str] = Field(default_factory=list)


class OutputConfig(BaseModel):
    output_dir: Path = Field(default_factory=lambda: Path("output"))
    image_dir: Path = Field(default_factory=lambda: Path("output/images"))
    video_dir: Path = Field(default_factory=lambda: Path("output/videos"))
    json_dir: Path = Field(default_factory=lambda: Path("output/json"))
    log_dir: Path = Field(default_factory=lambda: Path("logs"))


class DrawConfig(BaseModel):
    font_scale: float = 0.5
    thickness: int = 2
    box_color: tuple[int, int, int] = (0, 255, 0)
    text_color: tuple[int, int, int] = (255, 255, 255)


class APIConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    prefix: str = ""


class AppConfig(BaseSettings):
    model: ModelConfig = ModelConfig()
    output: OutputConfig = OutputConfig()
    draw: DrawConfig = DrawConfig()
    api: APIConfig = APIConfig()

    model_config = SettingsConfigDict(
        env_prefix="PPE_",
        env_file=".env",
        case_sensitive=False,
    )

    @classmethod
    def validate(cls, values):
        model_data = values.get("model") or {}
        output_data = values.get("output") or {}

        if isinstance(model_data, dict):
            model_data["path"] = Path(model_data.get("path", "weights/best.pt"))
            values["model"] = model_data

        if isinstance(output_data, dict):
            for key in ["output_dir", "image_dir", "video_dir", "json_dir", "log_dir"]:
                if key in output_data:
                    output_data[key] = Path(output_data[key])
            values["output"] = output_data

        return values

    @classmethod
    def model_validate(cls, obj):
        return cls.validate(obj)


def load_config(config_path: Optional[Path] = None) -> AppConfig:
    root = Path(__file__).resolve().parents[2]
    config_path = config_path or root / "config.yaml"
    config_data: dict = {}

    if config_path.exists():
        with config_path.open("r", encoding="utf-8") as file:
            config_data = yaml.safe_load(file) or {}

    return AppConfig(**config_data)
