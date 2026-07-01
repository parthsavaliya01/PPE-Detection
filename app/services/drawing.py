from typing import Iterable

import cv2
import numpy as np

from app.core.settings import AppConfig


class BoundingBoxDrawer:
    """Draw bounding boxes and labels on images."""

    def __init__(self, config: AppConfig) -> None:
        self.config = config

    def draw(self, image: np.ndarray, boxes: Iterable[list[float]], scores: Iterable[float], classes: Iterable[str]) -> np.ndarray:
        annotated = image.copy()

        for box, score, class_name in zip(boxes, scores, classes):
            x1, y1, x2, y2 = map(int, box)
            label = f"{class_name}: {score:.2f}"

            cv2.rectangle(
                annotated,
                (x1, y1),
                (x2, y2),
                self.config.draw.box_color,
                self.config.draw.thickness,
            )

            text_size, _ = cv2.getTextSize(
                label,
                cv2.FONT_HERSHEY_SIMPLEX,
                self.config.draw.font_scale,
                self.config.draw.thickness,
            )
            text_y = max(y1 - 10, text_size[1] + 10)

            cv2.rectangle(
                annotated,
                (x1, text_y - text_size[1] - 5),
                (x1 + text_size[0], text_y + 5),
                self.config.draw.box_color,
                cv2.FILLED,
            )
            cv2.putText(
                annotated,
                label,
                (x1, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                self.config.draw.font_scale,
                self.config.draw.text_color,
                self.config.draw.thickness,
                cv2.LINE_AA,
            )

        return annotated
