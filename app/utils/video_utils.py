from pathlib import Path
import time

import cv2
import numpy as np

from app.core.exceptions import InvalidPathError, VideoProcessingError
from app.core.logger import logger
from app.core.settings import AppConfig, load_config
from app.services.drawing import BoundingBoxDrawer
from app.services.inference import InferenceEngine


class VideoProcessor:
    """Process video frames for PPE detection and output annotated video."""

    def __init__(self, config: AppConfig | None = None) -> None:
        self.config = config or load_config()
        self.engine = InferenceEngine(self.config)
        self.drawer = BoundingBoxDrawer(self.config)

    def validate_input(self, video_path: Path) -> None:
        if not video_path.exists():
            raise InvalidPathError(f"Video not found: {video_path}")

    def process(self, input_path: Path, output_path: Path | None = None) -> dict[str, float]:
        self.validate_input(input_path)

        capture = cv2.VideoCapture(str(input_path))
        if not capture.isOpened():
            raise VideoProcessingError("Unable to open video file.")

        frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = capture.get(cv2.CAP_PROP_FPS) or 25.0

        writer = None
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            writer = cv2.VideoWriter(str(output_path), fourcc, fps, (frame_width, frame_height))

        total_frames = 0
        processed_frames = 0
        total_inference_time = 0.0

        while capture.isOpened():
            success, frame = capture.read()
            if not success:
                break

            total_frames += 1
            start_time = time.time()
            result = self.engine.predict_array(frame)
            annotated = self.drawer.draw(frame, result.boxes, result.scores, result.classes)
            total_inference_time += time.time() - start_time
            processed_frames += 1

            if writer:
                writer.write(annotated)

        capture.release()
        if writer:
            writer.release()
            logger.info("Saved annotated video to %s", output_path)

        fps_average = processed_frames / total_inference_time if total_inference_time else 0.0
        return {
            "total_frames": float(total_frames),
            "processed_frames": float(processed_frames),
            "average_fps": fps_average,
            "total_inference_time": total_inference_time,
        }
