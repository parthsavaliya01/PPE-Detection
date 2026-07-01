from pathlib import Path
from typing import Any

import cv2
import numpy as np

from app.core.logger import logger
from app.core.settings import AppConfig, load_config
from app.models.detector import DetectionResult, PPEDetector
from app.models.model_loader import ModelLoader
from app.utils.image_utils import load_image


class InferenceEngine:
    """Manage model loading and running inference requests."""

    def __init__(self, config: AppConfig | None = None) -> None:
        self.config = config or load_config()
        self.model = ModelLoader(self.config).get_model()
        self.detector = PPEDetector(self.model, self.config)

    def predict_image(self, image_path: Path) -> DetectionResult:
        image = load_image(image_path)
        logger.info("Predicting image: %s", image_path)
        return self.detector.predict(image)

    def predict_array(self, image: np.ndarray) -> DetectionResult:
        logger.info("Predicting image array")
        return self.detector.predict(image)
