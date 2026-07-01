from pathlib import Path
from typing import Any

import cv2
import numpy as np
from ultralytics import YOLO

from app.core.exceptions import InferenceError
from app.core.logger import logger
from app.core.settings import AppConfig


class DetectionResult:
    """Structured detection output."""

    def __init__(self, boxes: list[list[float]], scores: list[float], classes: list[str]):
        self.boxes = boxes
        self.scores = scores
        self.classes = classes

    def to_dict(self) -> dict[str, list[Any]]:
        return {
            "boxes": self.boxes,
            "scores": self.scores,
            "classes": self.classes,
        }


class PPEDetector:
    """Run PPE detection using a loaded YOLO model."""

    def __init__(self, model: YOLO, config: AppConfig) -> None:
        self.model = model
        self.config = config

    def predict(self, image: np.ndarray) -> DetectionResult:
        if image is None or image.size == 0:
            raise InferenceError("Input image is empty or invalid.")

        try:
            logger.info("Starting inference on image")
            results = self.model(
                image,
                imgsz=self.config.model.image_size,
                conf=self.config.model.confidence_threshold,
                iou=self.config.model.iou_threshold,
                device=self.config.model.device,
            )

            boxes: list[list[float]] = []
            scores: list[float] = []
            classes: list[str] = []

            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    boxes.append([x1, y1, x2, y2])
                    scores.append(float(box.conf[0]))
                    classes.append(self.model.names[int(box.cls[0])])

            logger.info("Inference completed with %d detections", len(boxes))
            return DetectionResult(boxes=boxes, scores=scores, classes=classes)
        except Exception as error:
            raise InferenceError("Inference failed.", details=str(error)) from error
