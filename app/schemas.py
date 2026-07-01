from pydantic import BaseModel
from typing import Any


class DetectionResponse(BaseModel):
    boxes: list[list[float]]
    scores: list[float]
    classes: list[str]


class PredictImageResponse(BaseModel):
    detections: DetectionResponse
    output_path: str


class ModelInfoResponse(BaseModel):
    model_path: str
    device: str
    confidence_threshold: float
    iou_threshold: float
    image_size: int
