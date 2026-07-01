from pathlib import Path
from typing import Any

import cv2
import numpy as np
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from app.core.exceptions import InferenceError, InvalidPathError, ModelLoadError
from app.core.logger import logger
from app.core.settings import load_config
from app.schemas import ModelInfoResponse, PredictImageResponse
from app.services.drawing import BoundingBoxDrawer
from app.services.inference import InferenceEngine
from app.utils.image_utils import save_image

router = APIRouter()
config = load_config()
engine = InferenceEngine(config)
drawer = BoundingBoxDrawer(config)


def read_upload_image(upload_file: UploadFile) -> np.ndarray:
    content = upload_file.file.read()
    image_array = np.frombuffer(content, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    if image is None:
        raise InvalidPathError("Uploaded file is not a valid image.")
    return image


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy", "message": "PPE Detection API is running."}


@router.get("/model/info", response_model=ModelInfoResponse)
def model_info() -> dict[str, Any]:
    return {
        "model_path": str(config.model.path),
        "device": config.model.device,
        "confidence_threshold": config.model.confidence_threshold,
        "iou_threshold": config.model.iou_threshold,
        "image_size": config.model.image_size,
    }


@router.post("/predict/image", response_model=PredictImageResponse)
async def predict_image(file: UploadFile = File(...)) -> JSONResponse:
    try:
        image = read_upload_image(file)
        result = engine.predict_array(image)
        annotated = drawer.draw(image, result.boxes, result.scores, result.classes)

        output_path = config.output.image_dir / f"prediction_{file.filename}"
        save_image(annotated, output_path)
        logger.info("Image saved to %s", output_path)

        return JSONResponse(
            content={
                "detections": result.to_dict(),
                "output_path": str(output_path),
            }
        )
    except (InvalidPathError, InferenceError, ModelLoadError) as error:
        logger.error("Predict image failed: %s", error)
        raise HTTPException(status_code=400, detail=str(error))
    except Exception as error:
        logger.exception("Unexpected error during image prediction")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/predict/video")
async def predict_video(file: UploadFile = File(...)) -> JSONResponse:
    try:
        video_bytes = await file.read()
        upload_dir = Path("input")
        upload_dir.mkdir(parents=True, exist_ok=True)
        video_path = upload_dir / file.filename
        video_path.write_bytes(video_bytes)

        from app.utils.video_utils import VideoProcessor

        processor = VideoProcessor(config)
        output_path = config.output.video_dir / f"prediction_{file.filename}"
        metrics = processor.process(video_path, output_path)

        return JSONResponse(
            content={
                "detections": "saved_video",
                "metrics": metrics,
                "output_path": str(output_path),
            }
        )
    except (InvalidPathError, InferenceError, ModelLoadError) as error:
        logger.error("Predict video failed: %s", error)
        raise HTTPException(status_code=400, detail=str(error))
    except Exception as error:
        logger.exception("Unexpected error during video prediction")
        raise HTTPException(status_code=500, detail="Internal server error")
