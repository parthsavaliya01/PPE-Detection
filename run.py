from __future__ import annotations

import argparse
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

from app.api.routes import router
from app.core.logger import logger
from app.core.settings import load_config
from app.services.inference import InferenceEngine


def create_app() -> FastAPI:
    config = load_config()
    app = FastAPI(title="PPE Detection API")
    
    # Mount static files
    static_dir = Path(__file__).parent / "app" / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    
    # Root endpoint - serve UI
    @app.get("/")
    async def root():
        ui_path = static_dir / "index.html"
        if ui_path.exists():
            return FileResponse(str(ui_path))
        return {"message": "PPE Detection API. Visit /docs for Swagger UI"}
    
    app.include_router(router, prefix=config.api.prefix)
    return app


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="PPE Detection application")
    parser.add_argument("--image", type=Path, help="Path to an image file for inference.")
    parser.add_argument("--video", type=Path, help="Path to a video file for inference.")
    parser.add_argument("--camera", type=int, help="Camera device index for live webcam inference.")
    parser.add_argument("--save", action="store_true", help="Save prediction outputs to disk.")
    parser.add_argument("--conf", type=float, help="Override confidence threshold.")
    parser.add_argument("--host", default=None, help="API host to bind.")
    parser.add_argument("--port", type=int, default=None, help="API port to bind.")
    return parser.parse_args()


def main() -> None:
    config = load_config()
    args = parse_arguments()

    if args.conf is not None:
        config.model.confidence_threshold = args.conf

    if args.image:
        engine = InferenceEngine(config)
        result = engine.predict_image(args.image)
        logger.info("Image inference complete: detections=%s", result.to_dict())
        return

    if args.video:
        from app.utils.video_utils import VideoProcessor

        processor = VideoProcessor(config)
        output_path = None
        if args.save:
            output_path = config.output.video_dir / f"prediction_{args.video.name}"
        metrics = processor.process(args.video, output_path)
        logger.info("Video inference metrics: %s", metrics)
        return

    if args.camera is not None:
        logger.warning("Camera mode not implemented yet; use API or add webcam support later.")
        return

    app = create_app()
    uvicorn.run(
        app,
        host=args.host or config.api.host,
        port=args.port or config.api.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()
