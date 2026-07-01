from pathlib import Path

from ultralytics import YOLO

from app.core.exceptions import InvalidPathError, ModelLoadError
from app.core.logger import logger
from app.core.settings import AppConfig, load_config


class ModelLoader:
    """Load and validate a YOLO model from disk."""

    def __init__(self, config: AppConfig | None = None) -> None:
        self.config = config or load_config()
        self.model: YOLO | None = None

    def validate(self) -> None:
        if not self.config.model.path.exists():
            raise InvalidPathError(
                f"Model file not found: {self.config.model.path}"
            )

    def load(self) -> YOLO:
        self.validate()

        try:
            logger.info("Loading YOLO model from %s", self.config.model.path)
            self.model = YOLO(str(self.config.model.path))
            logger.info("Model loaded successfully: %s", self.config.model.name)
            return self.model
        except Exception as error:
            raise ModelLoadError(
                "Unable to load the YOLO model.",
                details=str(error),
            ) from error

    def get_model(self) -> YOLO:
        if self.model is None:
            return self.load()
        return self.model
